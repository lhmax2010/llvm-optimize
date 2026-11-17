import importlib.util, os, signal, sys
spec = importlib.util.spec_from_file_location('helper', sys.argv[1]); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
    if signal.getsignal(sig) != signal.SIG_IGN: signal.signal(sig, h.record_cancel)
print('parent SIGCHLD before', signal.getsignal(signal.SIGCHLD))
out = h.call(['grep', '^Sig[BIC]', '/proc/self/status'], sys.argv[2], timeout=10)
print('child:', ' '.join(out.split()))
print('parent SIGCHLD after', signal.getsignal(signal.SIGCHLD))
print('parent self:', ' '.join(l for l in open('/proc/self/status').read().split('\n') if l.startswith(('SigBlk','SigIgn'))))
