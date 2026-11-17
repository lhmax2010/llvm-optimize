import importlib.util, json, os, signal, sys, time, types, errno
H, scen, work = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('helper', H); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP): signal.signal(s, h.record_cancel)
MARK = 'SPECIAL-%d' % os.getpid()
def is_special(pid):
    try: return MARK.encode() in open('/proc/%d/cmdline' % pid, 'rb').read()
    except OSError: return False
def fd_pid(fd):
    for line in open('/proc/self/fdinfo/%d' % fd):
        if line.startswith('Pid:'): return int(line.split()[1])
    return -1
real_send = signal.pidfd_send_signal; real_open = os.pidfd_open
inject = None
if scen.startswith('eperm-delay'):
    def send(fd, sig, info=None, flags=0):
        if sig == signal.SIGKILL and is_special(fd_pid(fd)):
            time.sleep(0.3); raise PermissionError(errno.EPERM, 'Operation not permitted (injected)')
        return real_send(fd, sig, info, flags)
    inject = ('signal', 'pidfd_send_signal', send)
elif scen.startswith('unkillable') or scen in ('hammer-unkillable', 'second-cleanup-unkillable'):
    def send(fd, sig, info=None, flags=0):
        if sig == signal.SIGKILL and is_special(fd_pid(fd)):
            time.sleep(0.3 if scen == 'unkillable-delay' else 0); return None
        return real_send(fd, sig, info, flags)
    inject = ('signal', 'pidfd_send_signal', send)
elif scen.startswith('emfile') and scen != 'allemfile':
    def popen(pid, flags=0):
        if is_special(pid): raise OSError(errno.EMFILE, 'Too many open files (injected)')
        return real_open(pid, flags)
    inject = ('os', 'pidfd_open', popen)
elif scen.startswith('fallback'):
    inject = ('os', 'pidfd_open', None)
elif scen == 'allemfile':
    def popen(pid, flags=0):
        if pid != os.getpid(): raise OSError(errno.EMFILE, 'Too many open files (injected)')
        return real_open(pid, flags)
    inject = ('os', 'pidfd_open', popen)
elif scen in ('eacces-probe', 'einval-probe'):
    code = errno.EACCES if scen == 'eacces-probe' else errno.EINVAL
    def popen(pid, flags=0):
        raise OSError(code, os.strerror(code) + ' (injected)')
    inject = ('os', 'pidfd_open', popen)
elif scen in ('transient-scan', 'persistent-scan'):
    real_stat = h.proc_stat
    state = {'n': 0}
    def ps(path):
        # inject a scan-time EACCES on the runner's own /proc entry (not a session member)
        if path == '/proc/%d/stat' % os.getpid():
            state['n'] += 1
            if scen == 'persistent-scan' or state['n'] == 2:
                raise PermissionError(errno.EACCES, 'Permission denied (injected)')
        return real_stat(path)
    h.proc_stat = ps
if inject:
    modname, attr, fn = inject
    proxy = types.ModuleType(modname); proxy.__dict__.update(getattr(h, modname).__dict__)
    if fn is None: del proxy.__dict__[attr]
    else: setattr(proxy, attr, fn)
    setattr(h, modname, proxy)
special = "%s -I -c 'import os,time; os.setpgid(0,0); time.sleep(40)' %s" % (sys.executable, MARK)
spawner = ("%s -I -c 'import os,time\nos.setpgid(0,0)\nwhile True:\n if os.fork()==0:\n  time.sleep(40); os._exit(0)\n time.sleep(0.05)'" % sys.executable)
bg = "(sleep 40) & (sleep 40) &"
cases = {
 'bg-short': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 3) & exit 0'], 60),
 'bg-long': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 40) & exit 0'], 60),
 'first-wait': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 40) & exit 0'], 60),
 'second-wait': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 40) & exit 0'], 60),
 'ninja-straggler': (['ninja', '-f', 'straggler.ninja'], 60),
 'ninja-timeout': (['ninja', '-j2', '-f', 'long.ninja'], 2),
 'fallback-ninja-timeout': (['ninja', '-j2', '-f', 'long.ninja'], 2),
 'eacces-probe': (['/bin/sh', '-c', 'exit 0'], 60),
 'einval-probe': (['/bin/sh', '-c', 'exit 0'], 60),
 'transient-scan': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 0.5) & exit 0'], 60),
 'persistent-scan': (['/bin/sh', '-c', 'exit 0'], 60),
 'kill-deadline-msg': (['/bin/sh', '-c', 'exec >/dev/null 2>&1; (sleep 40) & sleep 40'], 1),
}
os.chdir(work)
open('straggler.ninja', 'w').write('rule s\n  command = sh -c "exec >/dev/null 2>&1; (sleep 40) &"\nbuild x: s\n')
open('long.ninja', 'w').write('rule s\n  command = sleep 40\nbuild a: s\nbuild b: s\n')
if scen in cases:
    argv, timeout = cases[scen]
else:   # adversarial: SPECIAL (own pgid, lowest pid) then a forking spawner (own pgid), timeout 1 s
    argv, timeout = (['/bin/sh', '-c', '%s %s & sleep 0.2; %s & sleep 40' % (bg, special, spawner)], 1)
prev = signal.signal(signal.SIGCHLD, lambda *a: None) if scen == 'bg-short' else None
before = signal.getsignal(signal.SIGCHLD)
t0 = time.monotonic()
try:
    h.call(argv, os.path.join(work, scen + '.log'), timeout=timeout); r = 'OK'
except h.GateError as e:
    r = 'ERR ' + str(e)
except Exception as e:
    r = 'EXC %s %s' % (type(e).__name__, e)
res = {'call_s': round(time.monotonic() - t0, 2), 'result': r[:3000], 'sigchld_restored': signal.getsignal(signal.SIGCHLD) is before}
print(json.dumps(res), flush=True)
