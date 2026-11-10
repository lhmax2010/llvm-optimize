from pathlib import Path
import json,subprocess,re
E=Path(__file__).parent
msg=subprocess.check_output(['git','show','-s','--format=%B'],text=True).strip()+'\n'
key=re.search(r'^Change-Id: (.*)$',msg,re.M)[1]
new=json.loads((E/'messages.json').read_text())[key]
if msg!=new:
 p=E/(key+'.message');p.write_text(new)
 subprocess.run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','-F',str(p)],check=True)
