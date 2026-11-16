import time,pathlib,subprocess,json,datetime
p=pathlib.Path(__file__).with_name("watchdog.jsonl")
while True:
 values=dict(line.split(":",1) for line in pathlib.Path("/proc/meminfo").read_text().splitlines())
 kb=int(values["MemAvailable"].split()[0])
 with p.open("a") as f:f.write(json.dumps({"time":datetime.datetime.now().astimezone().isoformat(),"MemAvailable_kB":kb,"stop":kb<6*1024*1024})+"\n")
 if kb<6*1024*1024:
  subprocess.run(["systemctl","--user","stop","task111-ps5-20261116.service"]);break
 time.sleep(30)
