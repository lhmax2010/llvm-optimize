set pagination off
set confirm off
set debuginfod enabled off
set auto-load python-scripts off
set debug-file-directory /nonexistent
run
frame 1
set $seg=*(unsigned long long*)$r14
set $buf=*(unsigned long long*)($rbx+16)
printf "SEGMENT pointer=%p\n",$seg
x/12gx $seg
printf "BUFFER pointer=%p\n",$buf
x/8gx $buf
printf "SEGMENT type=%u offset=%llu size=%llu\n",*(unsigned int*)$seg,*(unsigned long long*)($seg+8),*(unsigned long long*)($seg+32)
printf "BUFFER start=%p end=%p size=%llu\n",*(unsigned long long*)($buf+8),*(unsigned long long*)($buf+16),*(unsigned long long*)($buf+16)-*(unsigned long long*)($buf+8)
