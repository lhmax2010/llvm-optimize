from pathlib import Path
import json,datetime
from compare_functions import compare
E=Path(__file__).resolve().parent
d=json.loads((E/'inputs.json').read_text())
result=compare(d['toolchain']['path'],d['basedev']['path'],E/'td')
print(json.dumps(result,indent=2))
print('已结束',datetime.datetime.now().astimezone().isoformat(),'TD-compare PASS')
