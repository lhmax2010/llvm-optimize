# usage: adv.py helper scenario workdir
import importlib.util, os, sys, time, signal, subprocess, json, types
H, scen, work = sys.argv[1:4]; os.makedirs(work, exist_ok=True)
T = 'ADV-%s-%d' % (scen, os.getpid())
# Child runs the helper; the parent observes and sends signals.
code = r'''
import importlib.util, os, sys, time, signal, types, json
H, scen, T, work = sys.argv[1:5]
spec = importlib.util.spec_from_file_location('helper', H); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s, h.record_cancel)
real_kill = os.kill
target = {}
def target_pid():
    # the "special" member: lowest-PID process whose cmdline has the marker 'SPECIAL'
    if 'pid' not in target:
        for d in os.listdir('/proc'):
            if d.isdecimal():
                try:
                    if b'SPECIAL-'+T.encode() in open('/proc/%s/cmdline' % d, 'rb').read(): target['pid'] = int(d); break
                except OSError: pass
    return target.get('pid')
def fake_kill(pid, sig):
    if pid == target_pid() and sig == signal.SIGKILL:
        if scen.startswith('eperm'): raise PermissionError(1, 'Operation not permitted')
        return  # unkillable (D-state simulation)
    return real_kill(pid, sig)
fos = types.ModuleType('os'); fos.__dict__.update(os.__dict__); fos.kill = fake_kill
h.os = fos
# SPECIAL member is in its own process group (like a ninja job), so killpg(sid) does not reach it.
special = "python3 -I -c 'import os,time; os.setpgid(0,0); time.sleep(40)' SPECIAL-%s" % T
others = "(sleep 40; : %s) & (sleep 40; : %s) &" % (T, T)
argv = ['/bin/sh', '-c', '%s %s & sleep 40; : %s' % (others, special, T)]
t0 = time.monotonic()
try:
    h.call(argv, work + '/x.log', timeout=1); r = 'OK'
except h.GateError as e:
    r = 'ERR ' + str(e)
print(json.dumps({'call_elapsed': round(time.monotonic() - t0, 2), 'result': r[:330]}), flush=True)
'''
child = subprocess.Popen([sys.executable, '-I', '-c', code, H, scen, T, work], stdout=subprocess.PIPE, text=True)
t0 = time.monotonic()
if scen.endswith('-signal2'):
    time.sleep(0.5); child.send_signal(signal.SIGTERM)   # first: cancel
    time.sleep(1.5); child.send_signal(signal.SIGTERM)   # second: during cleanup
if scen.endswith('-signal3'):
    time.sleep(0.5); child.send_signal(signal.SIGTERM)
    time.sleep(1.5); child.send_signal(signal.SIGTERM); time.sleep(0.2); child.send_signal(signal.SIGTERM)
out, _ = child.communicate(); el = time.monotonic() - t0
time.sleep(.3)
left = subprocess.run(['pgrep', '-f', T], capture_output=True, text=True).stdout.split()
desc = subprocess.run(['ps', '-o', 'pid,pgid,sid,stat,args', '-p', ','.join(left)], capture_output=True, text=True).stdout if left else ''
print(json.dumps({'scenario': scen, 'rc': child.returncode, 'total': round(el, 2), 'child_out': out.strip()[:400], 'survivors': len(left)}))
if desc: print(desc.rstrip())
for p in left:
    try: os.kill(int(p), 9)
    except ProcessLookupError: pass
