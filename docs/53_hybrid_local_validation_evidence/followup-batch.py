import subprocess,time,json
from pathlib import Path
from validate import D,E,save
start=time.time_ns()
with (E/'followup.stdout').open('wb') as out,(E/'followup.stderr').open('wb') as err:
 rc=subprocess.run(['python3','-B',str(D/'followup.py')],stdout=out,stderr=err).returncode
save('followup-result.json',{'rc':rc,'start_ns':start,'end_ns':time.time_ns()})
