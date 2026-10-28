import probe as p
import lzma,time
rows={}
for role in ['final','symbols']:
 f=p.D/('clang.'+role);c=lzma.LZMACompressor(format=lzma.FORMAT_XZ,preset=5);n=0;start=time.monotonic()
 with f.open('rb') as stream:
  while block:=stream.read(1024*1024):n+=len(c.compress(block))
 n+=len(c.flush());rows[role]={'bytes':f.stat().st_size,'sha256':p.sha(f),'xz5_stream_bytes':n,'compression_seconds':time.monotonic()-start}
 p.save('sizes-followup.json',{'method':'xz preset5 single stream for each ELF, based on RPM xz 5T payload metadata; estimated marginal delta excludes cpio/header/cross-file compression; no RPM built','files':rows,'symbols_only':'not produced: llvm-objcopy SIGSEGV'})
 print(role,rows[role],flush=True)
p.save('size-estimate.json',{'uncompressed_delta_bytes':rows['symbols']['bytes']-rows['final']['bytes'],'estimated_rpm_delta_bytes':rows['symbols']['xz5_stream_bytes']-rows['final']['xz5_stream_bytes'],'files':rows})
p.run('symbolizer-version',[*p.LOADER,p.BUILD/'bin/llvm-symbolizer','--version'])
p.run('objcopy-version',[*p.LOADER,p.BUILD/'bin/llvm-objcopy','--version'])
