"""Ownership-safe probe harness.
The harness makes itself a child subreaper, runs one scenario in a child it owns,
and afterwards signals only its own unreaped children (PIDs pinned by being
unreaped children), via pidfd. It never kills by name or by an arbitrary PID."""
import ctypes, json, os, signal, subprocess, sys, time
H, scen, work = sys.argv[1:4]
os.makedirs(work, exist_ok=True)
libc = ctypes.CDLL(None, use_errno=True)
assert libc.prctl(36, 1, 0, 0, 0) == 0          # PR_SET_CHILD_SUBREAPER
ME = os.getpid()
RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runner.py')
def my_children():
    out = []
    for d in os.listdir('/proc'):
        if not d.isdecimal(): continue
        try:
            t = open('/proc/%s/stat' % d).read()
        except OSError: continue
        f = t.rsplit(')', 1)[1].split()
        if int(f[1]) == ME and f[0] not in 'ZX':
            out.append((int(d), f[0], int(f[2]), int(f[3])))
    return out
env = dict(os.environ)
t0 = time.monotonic()
child = subprocess.Popen([sys.executable, '-I', RUNNER, H, scen, work], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
plan = {'first-wait': [1.0], 'second-wait': [1.0, 1.0], 'hammer-unkillable': [0.5] + [0.3] * 20,
        'second-cleanup-unkillable': [0.5, 1.5]}.get(scen, [])
sent = []
for delay in plan:
    time.sleep(delay)
    if child.poll() is not None: break
    child.send_signal(signal.SIGTERM); sent.append(round(time.monotonic() - t0, 2))
out, err = child.communicate(timeout=120)
total = round(time.monotonic() - t0, 2)
time.sleep(0.4)
survivors = []
for _ in range(20):           # killed survivors' children reparent to us; repeat
    kids = my_children()
    if not kids: break
    for pid, state, pgrp, sid in kids:
        survivors.append((pid, state, pgrp, sid))
        fd = os.pidfd_open(pid)
        try: signal.pidfd_send_signal(fd, signal.SIGKILL)
        finally: os.close(fd)
    time.sleep(0.1)
# reap everything we adopted
while True:
    try:
        pid, _ = os.waitpid(-1, os.WNOHANG)
    except ChildProcessError: break
    if pid == 0:
        time.sleep(0.05)
        if not my_children(): 
            try: os.waitpid(-1, os.WNOHANG)
            except ChildProcessError: pass
            break
print(json.dumps({'scenario': scen, 'runner_rc': child.returncode, 'total_s': total, 'signals_at': sent,
                  'runner_out': out.strip()[-3200:], 'mode_line': [l for l in err.splitlines() if 'SESSION_KILL_MODE' in l][:1], 'err_tail': err.strip()[-400:],
                  'survivors': len(survivors), 'survivor_detail': survivors[:12]}))
