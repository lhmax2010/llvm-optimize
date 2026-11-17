from pathlib import Path
import subprocess,sys,json,os,datetime
P=Path(__file__).parent
H='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-122/source/packaging/clang-bolt-helper.py'
baselines=[json.loads(s) for s in (P/'baseline-results.jsonl').read_text().splitlines()]
rows=[]
def kind(row):
 if row['runner_rc']!=0:return 'signal:'+str(row['runner_rc'])
 return json.loads(row['runner_out'])['result'].split(':',1)[0]
for base in baselines:
 name=base['scenario'];cmd=[sys.executable,'-B',str(P/'harness.py'),H,name,str(P/'work'/name)]
 env=dict(os.environ,PATH=str(P/'bin')+':'+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
 proc=subprocess.run(cmd,capture_output=True,text=True,env=env)
 (P/(name+'.stdout')).write_text(proc.stdout);(P/(name+'.stderr')).write_text(proc.stderr)
 assert proc.returncode==0,(name,proc.returncode,proc.stderr)
 row=json.loads(proc.stdout);row['expected_kind']=kind(base);row['actual_kind']=kind(row)
 row['PASS']=(row['runner_rc']==base['runner_rc'] and row['actual_kind']==row['expected_kind'] and row['survivors']==base['survivors'] and row['mode_line']==base['mode_line'])
 if row['runner_rc']==0:row['PASS']=row['PASS'] and json.loads(row['runner_out'])['sigchld_restored']
 rows.append(row);(P/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,row['PASS'],row['actual_kind'],'harness-cleaned=',row['survivors'],flush=True)
 if not row['PASS']:raise SystemExit(1)
print('已结束 '+datetime.datetime.now().astimezone().isoformat()+' probes=PASS count='+str(len(rows)),flush=True)
