import importlib.util, os, signal, subprocess, sys
spec = importlib.util.spec_from_file_location('helper', sys.argv[1]); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
mode, log = sys.argv[2], sys.argv[3]
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
for s in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT): signal.signal(s, h.record_cancel)
pids, events = [], []
real_popen, real_signal = subprocess.Popen, signal.signal
def popen(*a, **k):
    p = real_popen(*a, **k); pids.append(p.pid); return p
def sig(num, handler):
    if num == signal.SIGCHLD and pids:
        events.append(('restore' if handler == signal.SIG_IGN else 'set', os.path.exists('/proc/%d' % pids[0])))
    return real_signal(num, handler)
subprocess.Popen = popen; signal.signal = sig
argv = {'ok': ['true'], 'fail': ['sh', '-c', 'exit 7'], 'timeout': ['sleep', '30'],
        'cancel': ['sh', '-c', 'kill -TERM $PPID; sleep 30'], 'sysexit': ['sleep', '30'], 'kbint': ['sleep', '30']}[mode]
if mode in ('sysexit', 'kbint'):
    real_peek = h.peek_child_exit
    def peek(p, t):
        raise SystemExit(3) if mode == 'sysexit' else KeyboardInterrupt()
    h.peek_child_exit = peek
try:
    h.call(argv, log, timeout=1)
    res = 'returned'
except BaseException as e:
    res = type(e).__name__ + ': ' + str(e)[:70]
print(f'{mode:8} {res:80} SIGCHLD_after={real_signal and signal.getsignal(signal.SIGCHLD)} restore_events(child_pid_still_exists)={events[-1:] }')
