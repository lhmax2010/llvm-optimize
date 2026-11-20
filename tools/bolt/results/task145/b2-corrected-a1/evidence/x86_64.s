.section .text
.globl _start
.type _start,@function
_start:
  call value
  mov %eax,%edi
  mov $60,%eax
  syscall
.size _start, .-_start
.section .text.value,"ax",@progbits
.type value,@function
value:
  mov $37,%eax
  ret
.size value, .-value
.section .note.GNU-stack,"",@progbits
