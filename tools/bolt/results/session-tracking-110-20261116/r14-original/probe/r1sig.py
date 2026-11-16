import os, sys, time, signal, subprocess, json
H, mode, work = sys.argv[1], sys.argv[2], sys.argv[3]
T = 'PROBESIG-%s-%d' % (mode, os.getpid())
child = subprocess.Popen([sys.executable, '-I', '-c', r'''
import importlib.util, os, sys, signal, time
spec = importlib.util.spec_from_file_location('helper', sys.argv[1]); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s, h.record_cancel)
t0 = time.monotonic()
try:
    h.call(['/bin/sh', '-c', 'exec 1>&- 2>&-; (sleep 40; : %s) & exit 0' % sys.argv[2]], sys.argv[3] + '/x.log', timeout=60); print('OK', flush=True)
except h.GateError as e:
    print('ERR %.2f %s' % (time.monotonic() - t0, str(e)[:200]), flush=True)
try: h.check_cancel(); print('no-cancel')
except h.GateError as e: print('check_cancel ->', str(e))
''', H, T, work], stdout=subprocess.PIPE, text=True)
time.sleep(1); t1 = time.monotonic(); child.send_signal(signal.SIGTERM)
if mode == 'second':
    time.sleep(1); child.send_signal(signal.SIGTERM)
out, _ = child.communicate(); el = time.monotonic() - t1
time.sleep(.3)
left = [p for p in subprocess.run(['pgrep', '-f', T], capture_output=True, text=True).stdout.split()]
print(json.dumps({'mode': mode, 'rc': child.returncode, 'since_first_signal': round(el, 2), 'out': out.strip()[:400], 'survivors': len(left)}))
for p in left:
    try: os.kill(int(p), 9)
    except ProcessLookupError: pass
