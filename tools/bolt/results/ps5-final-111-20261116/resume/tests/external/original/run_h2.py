import os, subprocess, sys, time, tempfile, signal
helper, harness = sys.argv[1], sys.argv[2]
cases = [('second-at-line', L) for L in range(254, 266)] + [('two-real-at-line', 258), ('two-real-at-line', 265), ('popen-ok', 0), ('popen-fail', 0)] + [('deferred-then-third', L) for L in range(257, 266)]
def alive(pid):
    try:
        st = open('/proc/%d/stat' % pid).read().rsplit(')', 1)[1].split()[0]
        return st not in ('Z', 'X')
    except FileNotFoundError:
        return False
for mode, line in cases:
    d = tempfile.mkdtemp(dir=os.path.dirname(harness))
    p = subprocess.run([sys.executable, '-I', harness, helper, mode, str(line), d, '254'],
                       capture_output=True, text=True, timeout=60)
    pid = None
    try: pid = int(open(os.path.join(d, 'popen.pid')).read())
    except FileNotFoundError: pass
    survivor = None
    if pid:
        deadline = time.time() + 3
        while time.time() < deadline and alive(pid): time.sleep(.05)
        survivor = alive(pid)
        if survivor: os.kill(pid, signal.SIGKILL)
    print(f'{mode:17} L={line:3} helper_rc={p.returncode:4} child={"none" if pid is None else ("ALIVE" if survivor else "dead")} out={p.stdout.strip()[:90]!r}')
