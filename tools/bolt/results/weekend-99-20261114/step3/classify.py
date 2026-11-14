from pathlib import Path
import subprocess,json,gzip,re,hashlib,difflib,collections,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=Path(__file__).resolve().parent
old=B/'tools/bolt/results/night-82-84-20261113/83'
rows=json.load(gzip.open(old/'machine-code-68.json.gz','rt'));tools=json.loads((old/'platform-tools.json').read_text());root=Path(tools['root']);obj=root/'usr/bin/llvm-objdump'
assert obj.exists()
argv0=[tools['tools']['loader']['path'],'--library-path',tools['library_path'],str(obj)]
inputs={};ident={}
for side,proj,sha in [('left','toolchain','ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c'),('right','basedev','bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501')]:
 p=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials')/proj/'reference-relocs-clang-22';h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest();assert h==sha;inputs[side]=p;ident[side]={'path':str(p),'bytes':p.stat().st_size,'sha256':h}
ident['objdump']={'path':str(obj),'sha256':hashlib.file_digest(obj.open('rb'),'sha256').hexdigest(),'argv_prefix':argv0}
(E/'identities.json').write_text(json.dumps(ident,indent=2)+'\n')
outputs=[]
def instructions(text,rec):
 parsed=[]
 for line in text.splitlines():
  m=re.match(r'\s*([0-9a-f]+):\s+(.+)',line)
  if m and rec['address']<=int(m[1],16)<rec['address']+rec['size']:parsed.append((int(m[1],16),m[2]))
 assert parsed,(rec['name'],text[:200])
 ords={a:i for i,(a,t) in enumerate(parsed)};norm=[]
 for j,(a,t) in enumerate(parsed):
  end=parsed[j+1][0] if j+1<len(parsed) else rec['address']+rec['size']
  t=t.split(' #',1)[0];t=re.sub(r'\.llvm\.\d+','',t)
  t=re.sub(r'\s+',' ',t).strip()
  rels=[r for r in rec['relocations'] if a-rec['address']<=r[0]<end-rec['address']]
  if rels:
   # Classification excludes address-bearing fields; raw text/diff retained.
   t=re.sub(r'-?0x[0-9a-f]+(?=\(%rip\))','RELOC',t)
   if re.match(r'(call|jmp|j[a-z]+)\w* ',t):t=t.split(' ',1)[0]+' RELOC_TARGET'
  else:
   def tgt(m):
    a2=int(m[1],16);return 'I'+str(ords[a2]) if a2 in ords else 'EXTERNAL:'+re.sub(r'\.llvm\.\d+','',m[2])
   t=re.sub(r'0x([0-9a-f]+) <([^>]+)>',tgt,t)
  t=re.sub(r' <[^>]+>','',t)
  norm.append(t)
 return norm
for i,row in enumerate(rows,1):
 texts={};norms={};cmds={}
 for side in ['left','right']:
  rec=row[side];argv=argv0+['-d','--no-show-raw-insn','--start-address='+hex(rec['address']),'--stop-address='+hex(rec['address']+rec['size']),str(inputs[side])]
  p=subprocess.run(argv,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert p.returncode==0,p.stderr
  texts[side]=p.stdout;norms[side]=instructions(p.stdout,rec);cmds[side]=argv
  (E/f'{i:02d}-{side}.asm').write_text(p.stdout)
 a,c=norms['left'],norms['right'];reg=lambda x:re.sub(r'%[a-z][a-z0-9]*','%REG',x);num=lambda x:re.sub(r'(?<![A-Za-z_])(?:-?0x[0-9a-f]+|\b\d+\b)','NUM',x)
 mnem=lambda seq:[x.split()[0] for x in seq]
 if a==c:cat='encoding_or_layout_only'
 elif [reg(x) for x in a]==[reg(x) for x in c]:cat='register_operands_only'
 elif [num(x) for x in a]==[num(x) for x in c]:cat='constants_or_offsets_only'
 elif collections.Counter(a)==collections.Counter(c):cat='instruction_order_only'
 elif len(a)==len(c) and sum(x!=y for x,y in zip(mnem(a),mnem(c)))<=3 and sum(x!=y for x,y in zip(mnem(a),mnem(c)))>0:cat='limited_opcode_changes'
 else:cat='mixed_or_other'
 diff=''.join(difflib.unified_diff(a,c,fromfile='T-normalized',tofile='D-normalized',lineterm='\n'))
 # Preserve newlines of individual instruction records.
 diff=''.join(difflib.unified_diff([x+'\n' for x in a],[x+'\n' for x in c],fromfile='T-normalized',tofile='D-normalized'))
 (E/f'{i:02d}-instruction.diff').write_text(diff)
 with gzip.open(E/f'{i:02d}-raw.diff.gz','wt') as f:f.write(''.join(difflib.unified_diff(texts['left'].splitlines(True),texts['right'].splitlines(True),fromfile='T',tofile='D')))
 outputs.append({'index':i,'name':row['key'][0],'category':cat,'T_size':row['left']['size'],'D_size':row['right']['size'],'T_instructions':len(a),'D_instructions':len(c),'argv':cmds,'diff':f'{i:02d}-instruction.diff','sample':diff[:5000]})
 print(i,cat,row['key'][0][:80],flush=True)
(E/'classification.json').write_text(json.dumps(outputs,indent=2)+'\n');(E/'result.json').write_text(json.dumps({'status':'PASS','functions':len(outputs),'categories':dict(collections.Counter(x['category'] for x in outputs)),'time':datetime.datetime.now().astimezone().isoformat()},indent=2)+'\n')
