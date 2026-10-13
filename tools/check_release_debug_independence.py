#!/usr/bin/env python3
"""Read-only debug/release ET_REL comparison under docs/49's final contract.

Section identity: name/type/COMDAT signature/link-order target identity. Only
same-identity duplicates and runtime-ordered sections retain file order.
REL implicit addends are covered by exact target payload equality; RELA
addends are explicit. No Source/compiler invocation or codegen exemptions.
"""
import argparse
import collections
import difflib
import hashlib
import json
from pathlib import Path
import re
import struct


def key(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def is_debug(name):
    return name.startswith(('.debug', '.rel.debug', '.rela.debug'))


def parse(data):
    if len(data) < 52 or data[:4] != b'\x7fELF' or data[4] not in (1, 2) or data[5] not in (1, 2):
        raise ValueError('expected ELF32/ELF64')
    bits = data[4]; endian = '<' if data[5] == 1 else '>'
    def take(start, size):
        if start < 0 or size < 0 or start > len(data) or size > len(data)-start:
            raise ValueError('ELF data outside file')
        return data[start:start+size]
    def unpack(fmt, offset):
        return struct.unpack(endian+fmt, take(offset, struct.calcsize(endian+fmt)))
    if unpack('H',16)[0] != 1:
        raise ValueError('expected ET_REL')
    header = dict(elf_class=bits, byte_order=data[5], machine=unpack('H',18)[0],
                  e_flags=unpack('I',36 if bits==1 else 48)[0])
    shoff = unpack('I' if bits==1 else 'Q',32 if bits==1 else 40)[0]
    stride,count,names = unpack('HHH',46 if bits==1 else 58)
    fmt = 'IIIIIIIIII' if bits==1 else 'IIQQQQIIQQ'
    if stride < struct.calcsize(endian+fmt): raise ValueError('invalid section header stride')
    zero=unpack(fmt,shoff);count=count or zero[5];names=zero[6] if names==0xffff else names
    take(shoff,count*stride)
    sections=[unpack(fmt,shoff+i*stride) for i in range(count)]
    def payload(i):
        if not 0 <= i < count: raise ValueError('section outside table')
        s=sections[i];return b'' if s[1]==8 else take(s[4],s[5])
    def string(blob,offset):
        if not 0 <= offset < len(blob): raise ValueError('string offset outside table')
        return blob[offset:blob.index(b'\0',offset)].decode('utf-8')
    if not 0 < names < count or sections[names][1]!=3: raise ValueError('invalid section name table')
    strings=payload(names);section_names=[string(strings,s[0]) for s in sections]
    symbols={};extensions={}
    for i,s in enumerate(sections):
        if s[1]==18:
            if s[6] in extensions or s[9]!=4 or s[5]%4: raise ValueError('invalid extended symbol index table')
            extensions[s[6]]=struct.unpack(endian+'I'*(s[5]//4),payload(i))
    for i,s in enumerate(sections):
        if s[1]!=2:continue
        sfmt='IIIBBH' if bits==1 else 'IBBHQQ'
        if s[9]<struct.calcsize(endian+sfmt) or s[5]%s[9] or not 0<=s[6]<count or sections[s[6]][1]!=3:
            raise ValueError('invalid symbol table')
        table=payload(i);strings=payload(s[6]);rows=[]
        for n,pos in enumerate(range(0,len(table),s[9])):
            f=struct.unpack_from(endian+sfmt,table,pos)
            name,value,size,info,other,idx=f if bits==1 else (f[0],f[4],f[5],f[1],f[2],f[3])
            special=idx in (0,0xfff1,0xfff2)
            if idx==0xffff:
                if i not in extensions or n>=len(extensions[i]): raise ValueError('missing extended symbol section')
                idx=extensions[i][n];special=False
                if not 0<idx<count:raise ValueError('invalid extended symbol section')
            elif not special and (idx>=0xff00 or idx>=count):raise ValueError('uncertified symbol section index')
            rows.append(dict(name=string(strings,name),type=info&15,binding=info>>4,visibility=other&3,
                             section_index=idx,special=special,value=value,size=size))
        symbols[i]=rows
    groups_raw=[];owners={}
    for i,s in enumerate(sections):
        if s[1]!=17:continue
        if s[9]!=4 or s[5]<4 or s[5]%4 or s[6] not in symbols or s[7]>=len(symbols[s[6]]):
            raise ValueError('invalid section group')
        words=struct.unpack(endian+'I'*(s[5]//4),payload(i))
        if any(not 0<n<count for n in words[1:]):raise ValueError('invalid section group member')
        signature=symbols[s[6]][s[7]]['name'];groups_raw.append((signature,words[0],words[1:]))
        if words[0]&1:
            for n in words[1:]:
                if n in owners:raise ValueError('multiple COMDAT owners')
                owners[n]=signature
    identities={};visiting=set()
    def identity(i):
        if i in identities:return identities[i]
        if not 0<i<count or i in visiting:raise ValueError('invalid/cyclic link-order identity')
        visiting.add(i);s=sections[i]
        result=[section_names[i],s[1],owners.get(i,''),identity(s[6]) if s[2]&0x80 else None]
        visiting.remove(i);identities[i]=result;return result
    for i in range(1,count):identity(i)
    def symsection(s):return s['section_index'] if s['special'] else identity(s['section_index'])
    def symidentity(s):
        if s['type']==3:return ['SECTION',symsection(s)]
        if s['binding']==0:return ['LOCAL',s['name'],symsection(s),s['value']]
        return ['SYMBOL',s['name']]
    rawrelocs=[];references=collections.defaultdict(set)
    for i,s in enumerate(sections):
        if s[1] not in (4,9):continue
        if not 0<s[7]<count or s[6] not in symbols:raise ValueError('invalid relocation target/symbol table')
        rfmt=('IIi' if s[1]==4 else 'II') if bits==1 else ('QQq' if s[1]==4 else 'QQ')
        if s[9]<struct.calcsize(endian+rfmt) or s[5]%s[9]:raise ValueError('invalid relocation stride')
        for pos in range(0,s[5],s[9]):
            f=struct.unpack_from(endian+rfmt,payload(i),pos)
            kind,si=(f[1]&255,f[1]>>8) if bits==1 else (f[1]&0xffffffff,f[1]>>32)
            if si>=len(symbols[s[6]]):raise ValueError('relocation symbol outside table')
            references[(s[6],si)].add('debug' if is_debug(section_names[s[7]]) else 'other')
            rawrelocs.append((s[7],s[6],si,f[0],kind,f[2] if s[1]==4 else 'implicit: target bytes checked',s[1]))
    # A group signature is a non-debug use, even without a relocation.
    for s in sections:
        if s[1]==17:references[(s[6],s[7])].add('other')
    debug_only=set()
    for ti,rows in symbols.items():
        for si,s in enumerate(rows):
            if ((s['binding']==0 and not s['special'] and section_names[s['section_index']].startswith('.debug')) or
                (s['special'] and s['section_index']==0 and references[(ti,si)]=={'debug'})):
                debug_only.add((ti,si))
    alloc=[];occurrences=collections.Counter();targets={}
    for i,s in enumerate(sections):
        if not s[2]&2:continue
        ident=identity(i);ordinal=occurrences[key(ident)];occurrences[key(ident)]+=1
        targets[i]=[ident,ordinal]
        alloc.append(dict(identity=ident,section=section_names[i],type=s[1],flags=s[2],size=s[5],
                          alignment=s[8],entsize=s[9],nobits=s[1]==8,content=payload(i)))
    relocs=[]
    for target,ti,si,offset,kind,addend,form in rawrelocs:
        if target in targets:
            relocs.append(dict(target=targets[target],offset=offset,type=kind,symbol=symidentity(symbols[ti][si]),
                               addend=addend,format='RELA' if form==4 else 'REL'))
    groups=[dict(signature=sig,flags=flags,members=[identity(n) for n in members if not is_debug(section_names[n])])
            for sig,flags,members in groups_raw]
    kept=[];excluded=[]
    for ti,rows in symbols.items():
        for si,s in enumerate(rows):
            row={k:v for k,v in s.items() if k not in ('special','section_index')};row['section']=symsection(s)
            if ((ti,si) in debug_only or s['type'] in (3,4) or
                (s['binding']==0 and (not s['name'] or s['name'].startswith('.L')))):
                excluded.append(row)
            else:kept.append(row)
    addrsig={}
    for i,s in enumerate(sections):
        if section_names[i]!='.llvm_addrsig':continue
        if s[6] not in symbols:raise ValueError('addrsig missing symbol table')
        blob=payload(i);pos=0
        while pos<len(blob):
            value=0;shift=0
            while True:
                if pos>=len(blob) or shift>63:raise ValueError('invalid addrsig ULEB128')
                byte=blob[pos];pos+=1;value|=(byte&127)<<shift
                if not byte&128:break
                shift+=7
            if value>=len(symbols[s[6]]):raise ValueError('addrsig symbol outside table')
            if (s[6],value) not in debug_only:
                item=symidentity(symbols[s[6]][value]);addrsig[key(item)]=item
    return dict(header=header,alloc=alloc,relocations=relocs,symbols=kept,groups=groups,
                addrsig=sorted(addrsig.values(),key=key),excluded_symbols=excluded,
                debug_sections=[n for n in section_names if n.startswith('.debug')])


def canonical(obj):
    def grouped(rows, field):
        groups=collections.defaultdict(list)
        for r in rows:groups[key(r[field])].append(r)
        return [r for k in sorted(groups) for r in groups[k]]
    ordered=collections.defaultdict(list)
    for s in obj['alloc']:
        name=s['section']
        if (re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',name) or
            any(name==p or name.startswith(p+'.') for p in ('.init_array','.fini_array','.preinit_array','.ctors','.dtors'))):
            ordered[name].append(s['identity'])
    return {**obj,'alloc':grouped(obj['alloc'],'identity'),'relocations':grouped(obj['relocations'],'target'),
            'ordered_sections':dict(ordered),**{k:sorted(obj[k],key=key) for k in ('symbols','groups','addrsig')}}


def serializable(obj):
    return {**obj,'alloc':[{**s,'content':dict(bytes=len(s['content']),sha256=hashlib.sha256(s['content']).hexdigest())} for s in obj['alloc']]}


def compare(debug,release):
    order_changed=[s['identity'] for s in debug['alloc']]!=[s['identity'] for s in release['alloc']]
    debug,release=canonical(debug),canonical(release)
    result={k:debug[k]==release[k] for k in ('header','alloc','ordered_sections','relocations','symbols','groups','addrsig')}
    result['release_no_debug']=not release['debug_sections'];delta={}
    left,right=serializable(debug),serializable(release)
    for k,equal in result.items():
        if not equal and k!='release_no_debug':
            delta[k]=''.join(difflib.unified_diff(json.dumps(left[k],indent=2).splitlines(True),json.dumps(right[k],indent=2).splitlines(True),fromfile='debug/'+k,tofile='release/'+k))
    if not result['release_no_debug']:delta['release_no_debug']=json.dumps(release['debug_sections'])
    return dict(status='PASS' if all(result.values()) else 'FAIL',checks=result,differences=delta,alloc_order_changed=order_changed)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('debug',type=Path);p.add_argument('release',type=Path)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    d,r=parse(a.debug.read_bytes()),parse(a.release.read_bytes());result=compare(d,r)
    result.update(debug=serializable(d),release=serializable(r));a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('debug','release')},indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
