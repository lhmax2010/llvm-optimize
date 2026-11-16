import importlib.util, os, sys, time, signal, subprocess, json
H = sys.argv[1]; case = sys.argv[2]; work = sys.argv[3]
spec = importlib.util.spec_from_file_location('helper', H); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s, h.record_cancel)
os.makedirs(work, exist_ok=True); os.chdir(work)
tag = lambda: 'PROBE-%s-%d' % (case, os.getpid())
T = tag()
argv = {
 'bg-short':   ['/bin/sh', '-c', 'exec 1>&- 2>&-; (sleep 3; : %s) & exit 0' % T],
 'bg-long':    ['/bin/sh', '-c', 'exec 1>&- 2>&-; (sleep 40; : %s) & exit 0' % T],
 'bg-setpgid': ['/bin/sh', '-c', 'set -m; (sleep 40; : %s) & exit 0' % T],
 'ninja-straggler': ['ninja', '-f', 'straggler.ninja'],
 'ninja-timeout':   ['ninja', '-j2', '-f', 'long.ninja'],
}[case]
open('straggler.ninja','w').write('rule s\n  command = sh -c "exec >/dev/null 2>&1; (sleep 40; : %s) &"\nbuild x: s\n' % T)
open('long.ninja','w').write('rule s\n  command = sh -c "sleep 40; : %s"\nbuild a: s\nbuild b: s\n' % T)
timeout = 2 if case == 'ninja-timeout' else 60
t0 = time.monotonic()
try:
    h.call(argv, os.path.join(work, case+'.log'), timeout=timeout); res = 'OK'
except h.GateError as e:
    res = 'ERR ' + str(e)
el = time.monotonic() - t0
time.sleep(0.5)
left = subprocess.run(['pgrep', '-f', T], capture_output=True, text=True).stdout.split()
left = [p for p in left if p != str(os.getpid())]
info = subprocess.run(['ps', '-o', 'pid,ppid,pgid,sid,stat,args', '-p', ','.join(left)], capture_output=True, text=True).stdout if left else ''
print(json.dumps({'case': case, 'elapsed': round(el, 2), 'result': res[:260], 'survivors': len(left)}))
if info: print(info.rstrip())
for p in left:
    try: os.kill(int(p), signal.SIGKILL)
    except ProcessLookupError: pass
