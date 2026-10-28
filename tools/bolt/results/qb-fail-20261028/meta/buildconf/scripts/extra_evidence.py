from pathlib import Path
import subprocess,json,difflib,hashlib,collections
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';F=B/'tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots';R=W/'temp/qb-meta-20261028/repo'
for name in ('project_config','project_meta','meta-dod-Targets-Ubuntu-24.04.xml','project_config_dod-Targets-Ubuntu-24.04'):
 p=R/'TIZEN/Tools/Tools-devbase-tools'/name;(E/('tools-example-'+name)).write_bytes(p.read_bytes())
for label,args in [('tools-explicit-config-history',['log','--format=fuller','-p','--','TIZEN/Tools/Tools-devbase-tools/project_config_dod-Targets-Ubuntu-24.04','TIZEN/Tools/Tools-devbase-tools/meta-dod-Targets-Ubuntu-24.04.xml']),('config-loader-history-search',['log','--all','--format=fuller','--stat','-G','get_build_conf|buildconf|build.conf|ngbs','--','TIZEN'])]:
 p=subprocess.run(['git','-C',str(R),*args],capture_output=True,text=True);(E/(label+'.txt')).write_text(p.stdout+p.stderr)
old=(F/'toolchain/build.conf').read_text().splitlines(keepends=True);conf=(R/'TIZEN/Tizen/Tizen-Base-Toolchain/project_config').read_text().splitlines(keepends=True)
# Keep wrapper lines; differences explicitly reveal snapshot versus current project config.
(E/'snapshot-vs-current-project-config.diff').write_text(''.join(difflib.unified_diff(old,conf,fromfile='Toolchain20261013/build.conf',tofile='meta-master/project_config')))
results=[]
for side in ('toolchain','base'):
 for arch in ('x86_64','armv7l','aarch64'):
  for query in ('rawmacros','optflags','repotype','target'):
   args=['/usr/lib/build/queryconfig','--dist',str(F/side/'build.conf'),'--archpath',arch,query]
   p=subprocess.run(args,capture_output=True,text=True);name=f'query-{side}-{arch}-{query}';(E/(name+'.txt')).write_text(p.stdout);(E/(name+'.stderr')).write_text(p.stderr);results.append(dict(name=name,argv=args,rc=p.returncode))
(E/'query-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('config queries',len(results),'success',sum(x['rc']==0 for x in results))
