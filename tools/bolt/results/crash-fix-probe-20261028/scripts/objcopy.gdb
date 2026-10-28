set pagination off
set confirm off
set debuginfod enabled off
set auto-load python-scripts off
set debug-file-directory /nonexistent
run
bt
info registers
frame 1
info registers
disassemble
info proc mappings
