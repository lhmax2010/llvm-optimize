import importlib.util, os, signal, subprocess, sys, time, json
helper_path, mode, line, workdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location('helper', helper_path)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
pidfile = os.path.join(workdir, 'child.pid')
argv = ['/bin/sh', '-c', 'echo $$ > %s; exec sleep 30' % pidfile]
fired = {'first': False, 'second': False}
spawn_line = int(sys.argv[5])
def local(frame, event, arg):
    if event == 'line':
        if frame.f_lineno == spawn_line and not fired['first']:
            fired['first'] = True
            if mode in ('second-at-line', 'popen-ok', 'popen-fail', 'deferred-then-third'):
                h._CANCEL_SIGNAL = signal.SIGTERM          # first signal already handled
            elif mode == 'two-real-at-line':
                pass
        if mode == 'deferred-then-third' and frame.f_lineno == 464 and not fired.get('d'):
            fired['d'] = True
            os.kill(os.getpid(), signal.SIGTERM)
        if mode == 'deferred-then-third' and frame.f_lineno == line and fired.get('d') and not fired['second'] and line != 464:
            fired['second'] = True
            os.kill(os.getpid(), signal.SIGHUP)
        if frame.f_lineno == line and not fired['second'] and mode in ('second-at-line', 'two-real-at-line'):
            fired['second'] = True
            if mode == 'two-real-at-line':
                os.kill(os.getpid(), signal.SIGTERM)
            os.kill(os.getpid(), signal.SIGTERM)
    return local
def tracer(frame, event, arg):
    return local if frame.f_code.co_name == 'call' else None
real_popen = subprocess.Popen
def popen(*a, **k):
    if mode == 'popen-fail':
        os.kill(os.getpid(), signal.SIGTERM)
        raise FileNotFoundError('simulated exec failure')
    p = real_popen(*a, **k)
    open(os.path.join(workdir, 'popen.pid'), 'w').write(str(p.pid))
    if mode == 'popen-ok':
        while not os.path.exists(pidfile): time.sleep(.005)
        os.kill(os.getpid(), signal.SIGTERM)   # second signal inside Popen, after the child exists
    return p
subprocess.Popen = popen
signal.signal(signal.SIGTERM, h.record_cancel); signal.signal(signal.SIGHUP, h.record_cancel)
import atexit
sys.settrace(tracer)
try:
    h.call(argv, os.path.join(workdir, 'log.txt'), timeout=5)
    print('RETURNED')
except BaseException as e:
    print('RAISED', type(e).__name__, str(e)[:120])
