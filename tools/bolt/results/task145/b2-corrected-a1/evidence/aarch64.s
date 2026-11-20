.section .text
.globl _start
.type _start,%function
_start:
  bl value
  mov x8, #93
  svc #0
.size _start, .-_start
.section .text.value,"ax",%progbits
.type value,%function
value:
  mov x0, #37
  ret
.size value, .-value
.section .note.GNU-stack,"",%progbits
