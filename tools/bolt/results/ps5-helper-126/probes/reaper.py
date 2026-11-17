"""Subreaper wrapper: run argv as an owned child; afterwards kill only our own
unreaped (hence pinned) children via pidfd and reap them."""
import ctypes, json, os, signal, subprocess, sys, time
assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
ME = os.getpid()
def kids():
    r = []
    for d in os.listdir('/proc'):
        if not d.isdecimal(): continue
        try: f = open('/proc/%s/stat' % d, 'rb').read().rsplit(b')', 1)[1].split()
        except OSError: continue
        if int(f[1]) == ME and f[0] not in (b'Z', b'X'): r.append(int(d))
    return r
p = subprocess.run(sys.argv[1:])
time.sleep(0.3); n = 0
for _ in range(20):
    k = kids()
    if not k: break
    for pid in k:
        n += 1; fd = os.pidfd_open(pid)
        try: signal.pidfd_send_signal(fd, signal.SIGKILL)
        finally: os.close(fd)
    time.sleep(0.1)
while True:
    try:
        pid, _ = os.waitpid(-1, os.WNOHANG)
        if pid == 0:
            if not kids(): break
            time.sleep(0.05)
    except ChildProcessError: break
print(json.dumps({'child_rc': p.returncode, 'survivors_cleaned': n}))
