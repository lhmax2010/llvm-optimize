
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003882ce0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_>:
 3882ce0:      	movq	%rsi, %rcx
 3882ce3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3882ced:      	subq	%rdi, %rsi
 3882cf0:      	cmpq	$0x40, %rsi
 3882cf4:      	ja	0x3882d04 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x24>
 3882cf6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3882cfc:      	movq	%rax, %rdx
 3882cff:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3882d04:      	pushq	%rbp
 3882d05:      	pushq	%r15
 3882d07:      	pushq	%r14
 3882d09:      	pushq	%r13
 3882d0b:      	pushq	%r12
 3882d0d:      	pushq	%rbx
 3882d0e:      	movq	%rcx, -0x18(%rsp)
 3882d13:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3882d1d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3882d27:      	movq	%rsi, -0x10(%rsp)
 3882d2c:      	movq	%rsi, %r14
 3882d2f:      	andq	$-0x40, %r14
 3882d33:      	movq	0x8(%rdi), %r13
 3882d37:      	movq	0x10(%rdi), %rcx
 3882d3b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3882d45:      	addq	%r13, %rdx
 3882d48:      	rolq	$0x1b, %rdx
 3882d4c:      	imulq	%r9, %rdx
 3882d50:      	movq	0x30(%rdi), %rsi
 3882d54:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3882d5e:      	addq	%rsi, %r10
 3882d61:      	rolq	$0x16, %r10
 3882d65:      	imulq	%r9, %r10
 3882d69:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3882d73:      	xorq	%rdx, %rbp
 3882d76:      	movq	0x28(%rdi), %r12
 3882d7a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3882d84:      	addq	%r12, %r9
 3882d87:      	addq	%r10, %r9
 3882d8a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3882d94:      	addq	(%rdi), %r10
 3882d97:      	movq	0x18(%rdi), %r11
 3882d9b:      	addq	%r10, %rax
 3882d9e:      	addq	%r11, %rax
 3882da1:      	addq	%rbp, %rax
 3882da4:      	rolq	$0x2b, %rax
 3882da8:      	addq	%rcx, %r13
 3882dab:      	addq	%r10, %r13
 3882dae:      	movq	%r13, %rdx
 3882db1:      	rolq	$0x14, %rdx
 3882db5:      	addq	%r10, %rdx
 3882db8:      	addq	%rax, %rdx
 3882dbb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3882dc5:      	addq	0x20(%rdi), %rax
 3882dc9:      	addq	%r11, %r13
 3882dcc:      	movq	0x38(%rdi), %r10
 3882dd0:      	addq	%rax, %rcx
 3882dd3:      	addq	%r10, %rcx
 3882dd6:      	addq	%r9, %rcx
 3882dd9:      	rolq	$0x2b, %rcx
 3882ddd:      	addq	%rsi, %r12
 3882de0:      	addq	%rax, %r12
 3882de3:      	movq	%r12, %rbx
 3882de6:      	rolq	$0x14, %rbx
 3882dea:      	addq	%rax, %rbx
 3882ded:      	addq	%rcx, %rbx
 3882df0:      	addq	%r10, %r12
 3882df3:      	movq	%r14, -0x20(%rsp)
 3882df8:      	cmpq	$0x40, %r14
 3882dfc:      	jne	0x3882e12 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x132>
 3882dfe:      	movq	%rbx, %rsi
 3882e01:      	movq	%r12, %r11
 3882e04:      	movq	%rdx, %rax
 3882e07:      	movq	%r13, %r14
 3882e0a:      	movq	%rbp, %r15
 3882e0d:      	jmp	0x3882efd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x21d>
 3882e12:      	addq	$-0x40, -0x20(%rsp)
 3882e18:      	xorl	%ecx, %ecx
 3882e1a:      	nopw	(%rax,%rax)
 3882e20:      	addq	%r9, %r8
 3882e23:      	addq	%r13, %r8
 3882e26:      	movq	0x48(%rdi,%rcx), %r14
 3882e2b:      	movq	0x50(%rdi,%rcx), %r10
 3882e30:      	addq	%r14, %r8
 3882e33:      	rolq	$0x1b, %r8
 3882e37:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3882e41:      	imulq	%rsi, %r8
 3882e45:      	addq	%rdx, %r9
 3882e48:      	movq	0x70(%rdi,%rcx), %rax
 3882e4d:      	movq	%rax, -0x8(%rsp)
 3882e52:      	addq	%rax, %r9
 3882e55:      	rolq	$0x16, %r9
 3882e59:      	imulq	%rsi, %r9
 3882e5d:      	movq	%r8, %r15
 3882e60:      	xorq	%rbx, %r15
 3882e63:      	movq	0x68(%rdi,%rcx), %r11
 3882e68:      	addq	%r11, %r13
 3882e6b:      	addq	%r12, %rbp
 3882e6e:      	rolq	$0x1f, %rbp
 3882e72:      	addq	%r13, %r9
 3882e75:      	imulq	%rsi, %rdx
 3882e79:      	addq	0x40(%rdi,%rcx), %rdx
 3882e7e:      	movq	%rbp, %r8
 3882e81:      	movq	0x58(%rdi,%rcx), %r13
 3882e86:      	addq	%rdx, %r12
 3882e89:      	addq	%r13, %r12
 3882e8c:      	addq	%r15, %r12
 3882e8f:      	rolq	$0x2b, %r12
 3882e93:      	addq	%r10, %r14
 3882e96:      	addq	%rdx, %r14
 3882e99:      	movq	%r14, %rax
 3882e9c:      	rolq	$0x14, %rax
 3882ea0:      	imulq	%rsi, %r8
 3882ea4:      	addq	%rdx, %rax
 3882ea7:      	addq	%r12, %rax
 3882eaa:      	addq	%r8, %rbx
 3882ead:      	addq	%r9, %r10
 3882eb0:      	addq	0x60(%rdi,%rcx), %rbx
 3882eb5:      	movq	0x78(%rdi,%rcx), %rdx
 3882eba:      	addq	%rbx, %r10
 3882ebd:      	addq	%rdx, %r10
 3882ec0:      	rolq	$0x2b, %r10
 3882ec4:      	addq	%r13, %r14
 3882ec7:      	addq	-0x8(%rsp), %r11
 3882ecc:      	addq	%rbx, %r11
 3882ecf:      	movq	%r11, %rsi
 3882ed2:      	rolq	$0x14, %rsi
 3882ed6:      	addq	%rbx, %rsi
 3882ed9:      	addq	%r10, %rsi
 3882edc:      	addq	%rdx, %r11
 3882edf:      	addq	$0x40, %rcx
 3882ee3:      	movq	%r15, %rbp
 3882ee6:      	movq	%r14, %r13
 3882ee9:      	movq	%rax, %rdx
 3882eec:      	movq	%r11, %r12
 3882eef:      	movq	%rsi, %rbx
 3882ef2:      	cmpq	%rcx, -0x20(%rsp)
 3882ef7:      	jne	0x3882e20 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x140>
 3882efd:      	movq	-0x10(%rsp), %r12
 3882f02:      	testb	$0x3f, %r12b
 3882f06:      	je	0x3882fd2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x2f2>
 3882f0c:      	movq	-0x18(%rsp), %rbp
 3882f11:      	movq	-0x38(%rbp), %rcx
 3882f15:      	movq	-0x30(%rbp), %rdx
 3882f19:      	addq	%rcx, %r8
 3882f1c:      	addq	%r9, %r8
 3882f1f:      	addq	%r14, %r8
 3882f22:      	rolq	$0x1b, %r8
 3882f26:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3882f30:      	imulq	%r13, %r8
 3882f34:      	addq	%rax, %r9
 3882f37:      	movq	-0x10(%rbp), %r10
 3882f3b:      	addq	%r10, %r9
 3882f3e:      	rolq	$0x16, %r9
 3882f42:      	imulq	%r13, %r9
 3882f46:      	xorq	%rsi, %r8
 3882f49:      	movq	-0x18(%rbp), %rdi
 3882f4d:      	addq	%rdi, %r14
 3882f50:      	addq	%r14, %r9
 3882f53:      	addq	%r11, %r15
 3882f56:      	rolq	$0x1f, %r15
 3882f5a:      	movq	%r15, %rbx
 3882f5d:      	imulq	%r13, %rax
 3882f61:      	addq	%r8, %r11
 3882f64:      	addq	-0x40(%rbp), %rax
 3882f68:      	movq	-0x28(%rbp), %r15
 3882f6c:      	addq	%r15, %r11
 3882f6f:      	addq	%rax, %r11
 3882f72:      	rolq	$0x2b, %r11
 3882f76:      	imulq	%r13, %rbx
 3882f7a:      	addq	%rdx, %rcx
 3882f7d:      	addq	%rax, %rcx
 3882f80:      	movq	%rcx, %r14
 3882f83:      	rolq	$0x14, %r14
 3882f87:      	addq	%rax, %r14
 3882f8a:      	addq	%r11, %r14
 3882f8d:      	addq	%r15, %rcx
 3882f90:      	addq	%rbx, %rsi
 3882f93:      	addq	-0x20(%rbp), %rsi
 3882f97:      	addq	%r9, %rdx
 3882f9a:      	movq	-0x8(%rbp), %rax
 3882f9e:      	addq	%rax, %rdx
 3882fa1:      	addq	%rsi, %rdx
 3882fa4:      	rolq	$0x2b, %rdx
 3882fa8:      	addq	%r10, %rdi
 3882fab:      	addq	%rsi, %rdi
 3882fae:      	movq	%rdi, %r10
 3882fb1:      	rolq	$0x14, %r10
 3882fb5:      	addq	%rsi, %r10
 3882fb8:      	addq	%rdx, %r10
 3882fbb:      	addq	%rax, %rdi
 3882fbe:      	movq	%r10, %rsi
 3882fc1:      	movq	%rdi, %r11
 3882fc4:      	movq	%r14, %rax
 3882fc7:      	movq	%rcx, %r14
 3882fca:      	movq	%r8, %r15
 3882fcd:      	movq	%rbx, %r8
 3882fd0:      	jmp	0x3882fdc <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_16RegisterBankInfo12ValueMappingEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS9_SD_+0x2fc>
 3882fd2:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3882fdc:      	xorq	%r11, %r14
 3882fdf:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3882fe9:      	imulq	%rcx, %r14
 3882fed:      	xorq	%r14, %r11
 3882ff0:      	shrq	$0x2f, %r14
 3882ff4:      	xorq	%r11, %r14
 3882ff7:      	imulq	%rcx, %r14
 3882ffb:      	movq	%r14, %rdi
 3882ffe:      	shrq	$0x2f, %rdi
 3883002:      	xorq	%r14, %rdi
 3883005:      	imulq	%rcx, %rdi
 3883009:      	movq	%r9, %rdx
 388300c:      	shrq	$0x2f, %rdx
 3883010:      	xorq	%r9, %rdx
 3883013:      	imulq	%r13, %rdx
 3883017:      	addq	%r15, %rdx
 388301a:      	addq	%rdi, %rdx
 388301d:      	xorq	%rsi, %rax
 3883020:      	imulq	%rcx, %rax
 3883024:      	xorq	%rax, %rsi
 3883027:      	shrq	$0x2f, %rax
 388302b:      	xorq	%rsi, %rax
 388302e:      	imulq	%rcx, %rax
 3883032:      	movq	%rax, %rsi
 3883035:      	shrq	$0x2f, %rsi
 3883039:      	xorq	%rax, %rsi
 388303c:      	imulq	%rcx, %rsi
 3883040:      	movq	%r12, %rax
 3883043:      	shrq	$0x2f, %rax
 3883047:      	xorq	%r12, %rax
 388304a:      	imulq	%r13, %rax
 388304e:      	addq	%r8, %rax
 3883051:      	addq	%rsi, %rax
 3883054:      	xorq	%rax, %rdx
 3883057:      	imulq	%rcx, %rdx
 388305b:      	xorq	%rdx, %rax
 388305e:      	shrq	$0x2f, %rdx
 3883062:      	xorq	%rax, %rdx
 3883065:      	imulq	%rcx, %rdx
 3883069:      	movq	%rdx, %rax
 388306c:      	shrq	$0x2f, %rax
 3883070:      	xorq	%rdx, %rax
 3883073:      	imulq	%rcx, %rax
 3883077:      	popq	%rbx
 3883078:      	popq	%r12
 388307a:      	popq	%r13
 388307c:      	popq	%r14
 388307e:      	popq	%r15
 3883080:      	popq	%rbp
 3883081:      	retq
