"""Owned-process check: a process whose comm is not valid UTF-8.
Only Popen objects created here are signalled (via Popen.kill / pidfd of own children)."""
import importlib.util, json, locale, os, signal, subprocess, sys, time
H = sys.argv[1]
spec = importlib.util.spec_from_file_location('h', H); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
SETNAME = ("import ctypes,sys,time,os\n"
           "if len(sys.argv)>1: os.setpgid(0,0)\n"
           "ctypes.CDLL(None).prctl(15, b'\\xffbad\\xfe', 0, 0, 0)\n"
           "print('ready', flush=True); time.sleep(30)\n")
out = {'encoding': locale.getpreferredencoding(False), 'python': sys.version.split()[0]}
def started(args, **kw):
    p = subprocess.Popen([sys.executable, '-c', SETNAME] + args, stdout=subprocess.PIPE, text=True, **kw)
    assert p.stdout.readline().strip() == 'ready'
    return p
owned = []
try:
    # A: unrelated (non-member) process with a non-UTF-8 comm, then a trivially successful step.
    bad = started([], start_new_session=True); owned.append(bad)
    out['stat_bytes'] = open('/proc/%d/stat' % bad.pid, 'rb').read()[:40].decode('latin-1')
    try:
        h.live_session_members(os.getpid()); out['A_scan'] = 'ok'
    except BaseException as e:
        out['A_scan'] = '%s: %s' % (type(e).__name__, str(e)[:120])
    t = time.monotonic()
    try:
        h.call(['/bin/sh', '-c', 'exit 0'], os.path.join(sys.argv[2], 'a.log')); out['A_call'] = 'OK'
    except BaseException as e:
        out['A_call'] = '%s: %s' % (type(e).__name__, str(e)[:300])
    out['A_call_s'] = round(time.monotonic() - t, 2)
    bad.kill(); bad.wait(5); owned.remove(bad)
    # B: timed-out step whose session contains a member in its own process group with a bad comm.
    t = time.monotonic()
    marker = os.path.join(sys.argv[2], 'b.pid')
    member = os.path.join(sys.argv[2], 'member.py'); open(member, 'w').write(SETNAME)
    script = "%s %s x & echo $! > %s; sleep 40" % (sys.executable, member, marker)
    try:
        h.call(['/bin/sh', '-c', script], os.path.join(sys.argv[2], 'b.log'), timeout=1); out['B_call'] = 'OK'
    except BaseException as e:
        out['B_call'] = '%s: %s' % (type(e).__name__, str(e)[:400])
    out['B_call_s'] = round(time.monotonic() - t, 2)
finally:
    for p in owned:
        p.kill(); p.wait(5)
print(json.dumps(out))
