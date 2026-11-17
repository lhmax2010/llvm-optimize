import ctypes,sys,time,os
if len(sys.argv)>1: os.setpgid(0,0)
ctypes.CDLL(None).prctl(15, b'\xffbad\xfe', 0, 0, 0)
print('ready', flush=True); time.sleep(30)
