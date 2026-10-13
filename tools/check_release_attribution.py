#!/usr/bin/env python3
"""Release certification helpers; the ten-rule ELF comparator remains unchanged.

Only explicit per-command input/output path substitutions are accepted. The
caller must supply compiler entity SHA, working directory, and environment
identity backed by contemporaneous recording or a documented same-process
inheritance proof. No implicit removal of arbitrary -g* or path-like options.
"""
import collections
import copy
import json
import re
import check_release_debug_independence as elf

DEBUG_OPTIONS = ('-g', '-gdwarf-4')


def parameter_gate(debug, release):
    def normalize(record):
        argv = list(record['argv']); mapping = record['path_map']
        if set(mapping.values()) != {'<INPUT>', '<OUTPUT>'} or len(mapping) != 2:
            raise ValueError('expected exactly input/output path mapping')
        for path in mapping:
            if argv.count(path) != 1: raise ValueError('ambiguous input/output path')
        return [mapping.get(token, token) for token in argv]
    d,r = normalize(debug),normalize(release)
    removed = [x for x in d if x in DEBUG_OPTIONS]
    checks = dict(debug_options=removed == list(DEBUG_OPTIONS),
                  release_no_debug=not any(x in DEBUG_OPTIONS for x in r),
                  ordered_non_debug=[x for x in d if x not in DEBUG_OPTIONS] == r,
                  compiler_sha=bool(debug['compiler_sha256']) and debug['compiler_sha256']==release['compiler_sha256'],
                  cwd=debug['cwd']==release['cwd'],
                  environment=bool(debug['environment_identity']) and debug['environment_identity']==release['environment_identity'])
    return dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,
                removed_debug_options=removed,debug_normalized=d,release_normalized=r)


def k(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'))


def is_mapping(s):
    return s['binding']==0 and s['type']==0 and bool(re.fullmatch(r'\$[atdx](?:\..*)?',s['name']))


def changed_function_sections(debug,release):
    """Locate unique function sections, without granting permission to ignore them."""
    d=elf.canonical(debug);r=elf.canonical(release)
    def buckets(obj):
        out=collections.defaultdict(list)
        for s in obj['alloc']:out[k(s['identity'])].append(s)
        return out
    left,right=buckets(d),buckets(r);sections=[];functions=[]
    for ident in sorted(left.keys()|right.keys()):
        if left[ident]==right[ident]:continue
        if len(left[ident])!=1 or len(right[ident])!=1:raise ValueError('changed/missing/duplicate section identity')
        a,b=left[ident][0],right[ident][0]
        if not (a['flags']&4 and b['flags']&4):raise ValueError('difference outside executable function section')
        ds=[s for s in d['symbols'] if s['type']==2 and s['section']==a['identity']]
        rs=[s for s in r['symbols'] if s['type']==2 and s['section']==a['identity']]
        if len(ds)!=1 or len(rs)!=1 or ds[0]['name']!=rs[0]['name']:
            raise ValueError('function section has no unique common function symbol')
        sections.append(a['identity']);functions.append(ds[0]['name'])
    if not sections:raise ValueError('ELF difference has no changed function payload')
    return dict(sections=sections,functions=functions)


def difference_scope(debug,release,sections):
    """All differences outside attributed function payload/relocs/maps/size fail."""
    ids={k(s) for s in sections}
    def remove(obj):
        out=copy.deepcopy(obj)
        out['alloc']=[s for s in out['alloc'] if k(s['identity']) not in ids]
        out['relocations']=[s for s in out['relocations'] if k(s['target'][0]) not in ids]
        syms=[]
        for s in out['symbols']:
            if k(s['section']) in ids:
                if is_mapping(s):continue
                if s['type']==2:s['size']=0  # Only function size is attributable.
            syms.append(s)
        out['symbols']=syms
        return out
    return elf.compare(remove(debug),remove(release))


def backend_function_gate(stripped_debug,release,sections):
    ids={k(s) for s in sections}
    def select(obj):
        out=copy.deepcopy(obj)
        out['alloc']=[s for s in out['alloc'] if k(s['identity']) in ids]
        out['relocations']=[s for s in out['relocations'] if k(s['target'][0]) in ids]
        out['symbols']=[s for s in out['symbols'] if k(s['section']) in ids and (s['type']==2 or is_mapping(s))]
        # Full original groups/addrsig are checked by difference_scope. This
        # isolated backend replay checks the specified functions, not unrelated IR.
        out['groups']=[];out['addrsig']=[]
        return out
    return elf.compare(select(stripped_debug),select(release))


def llvm_diff_changed_function(function, exit_code, output):
    if 'No function named' in output or 'error:' in output.lower():
        raise ValueError('llvm-diff parse/missing-function error')
    if exit_code not in (0,1):raise ValueError('llvm-diff abnormal exit')
    marker='in function '+function+':'
    changed=exit_code==1 and marker in output
    if exit_code==1 and not changed:raise ValueError('llvm-diff difference not scoped to requested function')
    return changed


def attribution_gate(debug,release,ir_changed_functions,backend=None):
    original=elf.compare(debug,release)
    if original['status']=='PASS':return dict(status='PASS_IDENTICAL',original=original)
    try:affected=changed_function_sections(debug,release)
    except ValueError as e:return dict(status='FAIL',reason=str(e),original=original)
    scope=difference_scope(debug,release,affected['sections'])
    if scope['status']!='PASS':return dict(status='FAIL',reason='difference outside attributed functions',scope=scope,affected=affected)
    rows=[]
    for function,section in zip(affected['functions'],affected['sections']):
        if function in ir_changed_functions:rows.append(dict(function=function,route='a',status='PASS'))
        elif backend is not None:
            check=backend_function_gate(backend,release,[section]);rows.append(dict(function=function,route='b',status=check['status'],comparison=check))
        else:rows.append(dict(function=function,route='unattributed',status='FAIL'))
    return dict(status='PASS_ATTRIBUTED' if all(x['status']=='PASS' for x in rows) else 'FAIL',affected=affected,scope=scope,functions=rows)
