
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003882d70 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_>:
 3882d70:      	movq	%rsi, %rcx
 3882d73:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3882d7d:      	subq	%rdi, %rsi
 3882d80:      	cmpq	$0x40, %rsi
 3882d84:      	ja	0x3882d94 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x24>
 3882d86:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3882d8c:      	movq	%rax, %rdx
 3882d8f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3882d94:      	pushq	%rbp
 3882d95:      	pushq	%r15
 3882d97:      	pushq	%r14
 3882d99:      	pushq	%r13
 3882d9b:      	pushq	%r12
 3882d9d:      	pushq	%rbx
 3882d9e:      	movq	%rcx, -0x18(%rsp)
 3882da3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3882dad:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3882db7:      	movq	%rsi, -0x10(%rsp)
 3882dbc:      	movq	%rsi, %r14
 3882dbf:      	andq	$-0x40, %r14
 3882dc3:      	movq	0x8(%rdi), %r13
 3882dc7:      	movq	0x10(%rdi), %rcx
 3882dcb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3882dd5:      	addq	%r13, %rdx
 3882dd8:      	rolq	$0x1b, %rdx
 3882ddc:      	imulq	%r9, %rdx
 3882de0:      	movq	0x30(%rdi), %rsi
 3882de4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3882dee:      	addq	%rsi, %r10
 3882df1:      	rolq	$0x16, %r10
 3882df5:      	imulq	%r9, %r10
 3882df9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3882e03:      	xorq	%rdx, %rbp
 3882e06:      	movq	0x28(%rdi), %r12
 3882e0a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3882e14:      	addq	%r12, %r9
 3882e17:      	addq	%r10, %r9
 3882e1a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3882e24:      	addq	(%rdi), %r10
 3882e27:      	movq	0x18(%rdi), %r11
 3882e2b:      	addq	%r10, %rax
 3882e2e:      	addq	%r11, %rax
 3882e31:      	addq	%rbp, %rax
 3882e34:      	rolq	$0x2b, %rax
 3882e38:      	addq	%rcx, %r13
 3882e3b:      	addq	%r10, %r13
 3882e3e:      	movq	%r13, %rdx
 3882e41:      	rolq	$0x14, %rdx
 3882e45:      	addq	%r10, %rdx
 3882e48:      	addq	%rax, %rdx
 3882e4b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3882e55:      	addq	0x20(%rdi), %rax
 3882e59:      	addq	%r11, %r13
 3882e5c:      	movq	0x38(%rdi), %r10
 3882e60:      	addq	%rax, %rcx
 3882e63:      	addq	%r10, %rcx
 3882e66:      	addq	%r9, %rcx
 3882e69:      	rolq	$0x2b, %rcx
 3882e6d:      	addq	%rsi, %r12
 3882e70:      	addq	%rax, %r12
 3882e73:      	movq	%r12, %rbx
 3882e76:      	rolq	$0x14, %rbx
 3882e7a:      	addq	%rax, %rbx
 3882e7d:      	addq	%rcx, %rbx
 3882e80:      	addq	%r10, %r12
 3882e83:      	movq	%r14, -0x20(%rsp)
 3882e88:      	cmpq	$0x40, %r14
 3882e8c:      	jne	0x3882ea2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x132>
 3882e8e:      	movq	%rbx, %rsi
 3882e91:      	movq	%r12, %r11
 3882e94:      	movq	%rdx, %rax
 3882e97:      	movq	%r13, %r14
 3882e9a:      	movq	%rbp, %r15
 3882e9d:      	jmp	0x3882f8d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x21d>
 3882ea2:      	addq	$-0x40, -0x20(%rsp)
 3882ea8:      	xorl	%ecx, %ecx
 3882eaa:      	nopw	(%rax,%rax)
 3882eb0:      	addq	%r9, %r8
 3882eb3:      	addq	%r13, %r8
 3882eb6:      	movq	0x48(%rdi,%rcx), %r14
 3882ebb:      	movq	0x50(%rdi,%rcx), %r10
 3882ec0:      	addq	%r14, %r8
 3882ec3:      	rolq	$0x1b, %r8
 3882ec7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3882ed1:      	imulq	%rsi, %r8
 3882ed5:      	addq	%rdx, %r9
 3882ed8:      	movq	0x70(%rdi,%rcx), %rax
 3882edd:      	movq	%rax, -0x8(%rsp)
 3882ee2:      	addq	%rax, %r9
 3882ee5:      	rolq	$0x16, %r9
 3882ee9:      	imulq	%rsi, %r9
 3882eed:      	movq	%r8, %r15
 3882ef0:      	xorq	%rbx, %r15
 3882ef3:      	movq	0x68(%rdi,%rcx), %r11
 3882ef8:      	addq	%r11, %r13
 3882efb:      	addq	%r12, %rbp
 3882efe:      	rolq	$0x1f, %rbp
 3882f02:      	addq	%r13, %r9
 3882f05:      	imulq	%rsi, %rdx
 3882f09:      	addq	0x40(%rdi,%rcx), %rdx
 3882f0e:      	movq	%rbp, %r8
 3882f11:      	movq	0x58(%rdi,%rcx), %r13
 3882f16:      	addq	%rdx, %r12
 3882f19:      	addq	%r13, %r12
 3882f1c:      	addq	%r15, %r12
 3882f1f:      	rolq	$0x2b, %r12
 3882f23:      	addq	%r10, %r14
 3882f26:      	addq	%rdx, %r14
 3882f29:      	movq	%r14, %rax
 3882f2c:      	rolq	$0x14, %rax
 3882f30:      	imulq	%rsi, %r8
 3882f34:      	addq	%rdx, %rax
 3882f37:      	addq	%r12, %rax
 3882f3a:      	addq	%r8, %rbx
 3882f3d:      	addq	%r9, %r10
 3882f40:      	addq	0x60(%rdi,%rcx), %rbx
 3882f45:      	movq	0x78(%rdi,%rcx), %rdx
 3882f4a:      	addq	%rbx, %r10
 3882f4d:      	addq	%rdx, %r10
 3882f50:      	rolq	$0x2b, %r10
 3882f54:      	addq	%r13, %r14
 3882f57:      	addq	-0x8(%rsp), %r11
 3882f5c:      	addq	%rbx, %r11
 3882f5f:      	movq	%r11, %rsi
 3882f62:      	rolq	$0x14, %rsi
 3882f66:      	addq	%rbx, %rsi
 3882f69:      	addq	%r10, %rsi
 3882f6c:      	addq	%rdx, %r11
 3882f6f:      	addq	$0x40, %rcx
 3882f73:      	movq	%r15, %rbp
 3882f76:      	movq	%r14, %r13
 3882f79:      	movq	%rax, %rdx
 3882f7c:      	movq	%r11, %r12
 3882f7f:      	movq	%rsi, %rbx
 3882f82:      	cmpq	%rcx, -0x20(%rsp)
 3882f87:      	jne	0x3882eb0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x140>
 3882f8d:      	movq	-0x10(%rsp), %r12
 3882f92:      	testb	$0x3f, %r12b
 3882f96:      	je	0x3883063 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x2f3>
 3882f9c:      	leaq	(%r9,%r14), %rdi
 3882fa0:      	movq	-0x18(%rsp), %rbp
 3882fa5:      	movq	-0x38(%rbp), %rcx
 3882fa9:      	movq	-0x30(%rbp), %rdx
 3882fad:      	addq	%rcx, %r8
 3882fb0:      	addq	%rdi, %r8
 3882fb3:      	rolq	$0x1b, %r8
 3882fb7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3882fc1:      	imulq	%r13, %r8
 3882fc5:      	addq	%rax, %r9
 3882fc8:      	movq	-0x10(%rbp), %r10
 3882fcc:      	addq	%r10, %r9
 3882fcf:      	rolq	$0x16, %r9
 3882fd3:      	imulq	%r13, %r9
 3882fd7:      	xorq	%rsi, %r8
 3882fda:      	movq	-0x18(%rbp), %rdi
 3882fde:      	addq	%rdi, %r14
 3882fe1:      	addq	%r14, %r9
 3882fe4:      	addq	%r11, %r15
 3882fe7:      	rolq	$0x1f, %r15
 3882feb:      	movq	%r15, %rbx
 3882fee:      	imulq	%r13, %rax
 3882ff2:      	addq	%r8, %r11
 3882ff5:      	addq	-0x40(%rbp), %rax
 3882ff9:      	movq	-0x28(%rbp), %r15
 3882ffd:      	addq	%r15, %r11
 3883000:      	addq	%rax, %r11
 3883003:      	rolq	$0x2b, %r11
 3883007:      	imulq	%r13, %rbx
 388300b:      	addq	%rdx, %rcx
 388300e:      	addq	%rax, %rcx
 3883011:      	movq	%rcx, %r14
 3883014:      	rolq	$0x14, %r14
 3883018:      	addq	%rax, %r14
 388301b:      	addq	%r11, %r14
 388301e:      	addq	%r15, %rcx
 3883021:      	addq	%rbx, %rsi
 3883024:      	addq	-0x20(%rbp), %rsi
 3883028:      	addq	%r9, %rdx
 388302b:      	movq	-0x8(%rbp), %rax
 388302f:      	addq	%rax, %rdx
 3883032:      	addq	%rsi, %rdx
 3883035:      	rolq	$0x2b, %rdx
 3883039:      	addq	%r10, %rdi
 388303c:      	addq	%rsi, %rdi
 388303f:      	movq	%rdi, %r10
 3883042:      	rolq	$0x14, %r10
 3883046:      	addq	%rsi, %r10
 3883049:      	addq	%rdx, %r10
 388304c:      	addq	%rax, %rdi
 388304f:      	movq	%r10, %rsi
 3883052:      	movq	%rdi, %r11
 3883055:      	movq	%r14, %rax
 3883058:      	movq	%rcx, %r14
 388305b:      	movq	%r8, %r15
 388305e:      	movq	%rbx, %r8
 3883061:      	jmp	0x388306d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x2fd>
 3883063:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 388306d:      	xorq	%r11, %r14
 3883070:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 388307a:      	imulq	%rcx, %r14
 388307e:      	xorq	%r14, %r11
 3883081:      	shrq	$0x2f, %r14
 3883085:      	xorq	%r11, %r14
 3883088:      	imulq	%rcx, %r14
 388308c:      	movq	%r14, %rdi
 388308f:      	shrq	$0x2f, %rdi
 3883093:      	xorq	%r14, %rdi
 3883096:      	imulq	%rcx, %rdi
 388309a:      	movq	%r9, %rdx
 388309d:      	shrq	$0x2f, %rdx
 38830a1:      	xorq	%r9, %rdx
 38830a4:      	imulq	%r13, %rdx
 38830a8:      	addq	%r15, %rdx
 38830ab:      	addq	%rdi, %rdx
 38830ae:      	xorq	%rsi, %rax
 38830b1:      	imulq	%rcx, %rax
 38830b5:      	xorq	%rax, %rsi
 38830b8:      	shrq	$0x2f, %rax
 38830bc:      	xorq	%rsi, %rax
 38830bf:      	imulq	%rcx, %rax
 38830c3:      	movq	%rax, %rsi
 38830c6:      	shrq	$0x2f, %rsi
 38830ca:      	xorq	%rax, %rsi
 38830cd:      	imulq	%rcx, %rsi
 38830d1:      	movq	%r12, %rax
 38830d4:      	shrq	$0x2f, %rax
 38830d8:      	xorq	%r12, %rax
 38830db:      	imulq	%r13, %rax
 38830df:      	addq	%r8, %rax
 38830e2:      	addq	%rsi, %rax
 38830e5:      	xorq	%rax, %rdx
 38830e8:      	imulq	%rcx, %rdx
 38830ec:      	xorq	%rdx, %rax
 38830ef:      	shrq	$0x2f, %rdx
 38830f3:      	xorq	%rax, %rdx
 38830f6:      	imulq	%rcx, %rdx
 38830fa:      	movq	%rdx, %rax
 38830fd:      	shrq	$0x2f, %rax
 3883101:      	xorq	%rdx, %rax
 3883104:      	imulq	%rcx, %rax
 3883108:      	popq	%rbx
 3883109:      	popq	%r12
 388310b:      	popq	%r13
 388310d:      	popq	%r14
 388310f:      	popq	%r15
 3883111:      	popq	%rbp
 3883112:      	retq
