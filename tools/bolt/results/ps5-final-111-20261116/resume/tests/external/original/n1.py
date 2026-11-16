import importlib.util, signal, sys
spec = importlib.util.spec_from_file_location('helper', sys.argv[1]); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
real = signal.getsignal
signal.getsignal = lambda s: None if s == signal.SIGCHLD else real(s)
try:
    h.call(['true'], sys.argv[2], timeout=5); print('returned; SIGCHLD now', real(signal.SIGCHLD))
except BaseException as e:
    print('raised', type(e).__name__, str(e)[:90])
