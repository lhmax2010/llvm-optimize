from pathlib import Path
import sys,subprocess,json,shutil,hashlib,datetime,mmap
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';F=W/'temp/ompd-relink-20261105';E=B/'tools/bolt/results/afternoon-20261105/item1'
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261103'));from rpm_extract import extract_selected
sys.path.insert(0,str(B/'tools/bolt/overnight-20261105'));from section_compare import layout,file_proof
R=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';br=Path('home/abuild/rpmbuild/BUILD/llvm-22.1.8/build');obj=Path('projects/openmp/libompd/gdb-plugin/python-module/ompd/ompdModule.so');name='usr/share/gdb/python/ompd/ompdModule.so';dbg='usr/lib/debug/'+name+'.debug'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for mode,pkgs in [('new',W/'temp/night-20261103/toolchain/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/RPMS'),('old',W/'temp/debuglink-20261028/full-20261030/products/RPMS')]:
 dest=F/(mode+'-rpm');extract_selected(next(pkgs.glob('llvm-devel-22*.rpm')),{name},dest);extract_selected(next(pkgs.glob('llvm-devel-debuginfo-*.rpm')),{dbg},dest)
 original=F/mode/obj; packaged=dest/name; a=packaged.read_bytes();print(mode,[s['name'] for s in layout(a)[2]])
 row={'mode':mode,'raw_link_sha':sha(original),'rpm_sha':sha(packaged),'raw_bytes_equal':sha(original)==sha(packaged),'rpm_debug_sha':sha(dest/dbg)}
 try:row['raw_proof']=file_proof(packaged,original)
 except Exception as x:row['raw_error']=str(x)
 # Apply platform eu-strip to a new copy and replace debuglink with the already-packaged matching symbol file.
 post=F/(mode+'-post');post.mkdir();p=post/'ompdModule.so';shutil.copy2(original,p)
 prefix=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')+':'+str(R/'lib64')]
 argv=prefix+[str(R/'usr/bin/eu-strip'),'--remove-comment','-f',str(post/'ompdModule.so.debug'),str(p)]
 q=subprocess.run(argv,capture_output=True,text=True);(E/(mode+'-post-strip.json')).write_text(json.dumps({'argv':argv,'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr},indent=2)+'\n');assert q.returncode==0
 # GNU debuglink CRC follows platform debugedit. Use the original RPM symbol file only to isolate link/strip bytes, not to certify symbol identity.
 argv=prefix+[str(R/'usr/bin/objcopy'),'--remove-section=.gnu_debuglink','--add-gnu-debuglink='+str(dest/dbg),str(p)]
 q=subprocess.run(argv,capture_output=True,text=True);(E/(mode+'-post-debuglink.json')).write_text(json.dumps({'argv':argv,'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr},indent=2)+'\n');assert q.returncode==0
 row['post_sha']=sha(p);row['post_bytes_equal']=sha(p)==sha(packaged)
 try:row['post_proof']=file_proof(packaged,p)
 except Exception as x:row['post_error']=str(x)
 # Full section-level raw comparison against matching historical unstripped binary.
 oldroot=R if mode=='new' else W/'temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
 _,h,ss=layout((oldroot/br/obj).read_bytes());_,hh,tt=layout(original.read_bytes());row['raw_section_differences']=[{'section':s['name'],'old_size':s['size'],'new_size':t['size'],'old_sha':hashlib.sha256(s['content']).hexdigest(),'new_sha':hashlib.sha256(t['content']).hexdigest()} for s,t in zip(ss,tt) if bytes(s['content'])!=bytes(t['content'])];rows.append(row)
(E/'packaged-comparison.json').write_text(json.dumps(rows,indent=2)+'\n');print([(r['mode'],r['post_bytes_equal'],r.get('post_error'),[d['section'] for d in r['raw_section_differences']]) for r in rows]);line='ITEM1 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=ok reason=isolated-links-and-packaging-comparison-complete';(E/'end.txt').write_text(line+'\n');print(line)
