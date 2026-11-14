
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000059b4ba0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 59b4ba0:      	movq	%rsi, %rcx
 59b4ba3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 59b4bad:      	subq	%rdi, %rsi
 59b4bb0:      	cmpq	$0x40, %rsi
 59b4bb4:      	ja	0x59b4bc4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 59b4bb6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 59b4bbc:      	movq	%rax, %rdx
 59b4bbf:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 59b4bc4:      	pushq	%rbp
 59b4bc5:      	pushq	%r15
 59b4bc7:      	pushq	%r14
 59b4bc9:      	pushq	%r13
 59b4bcb:      	pushq	%r12
 59b4bcd:      	pushq	%rbx
 59b4bce:      	movq	%rcx, -0x18(%rsp)
 59b4bd3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 59b4bdd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 59b4be7:      	movq	%rsi, -0x10(%rsp)
 59b4bec:      	movq	%rsi, %r14
 59b4bef:      	andq	$-0x40, %r14
 59b4bf3:      	movq	0x8(%rdi), %r13
 59b4bf7:      	movq	0x10(%rdi), %rcx
 59b4bfb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 59b4c05:      	addq	%r13, %rdx
 59b4c08:      	rolq	$0x1b, %rdx
 59b4c0c:      	imulq	%r9, %rdx
 59b4c10:      	movq	0x30(%rdi), %rsi
 59b4c14:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 59b4c1e:      	addq	%rsi, %r10
 59b4c21:      	rolq	$0x16, %r10
 59b4c25:      	imulq	%r9, %r10
 59b4c29:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 59b4c33:      	xorq	%rdx, %rbp
 59b4c36:      	movq	0x28(%rdi), %r12
 59b4c3a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 59b4c44:      	addq	%r12, %r9
 59b4c47:      	addq	%r10, %r9
 59b4c4a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 59b4c54:      	addq	(%rdi), %r10
 59b4c57:      	movq	0x18(%rdi), %r11
 59b4c5b:      	addq	%r10, %rax
 59b4c5e:      	addq	%r11, %rax
 59b4c61:      	addq	%rbp, %rax
 59b4c64:      	rolq	$0x2b, %rax
 59b4c68:      	addq	%rcx, %r13
 59b4c6b:      	addq	%r10, %r13
 59b4c6e:      	movq	%r13, %rdx
 59b4c71:      	rolq	$0x14, %rdx
 59b4c75:      	addq	%r10, %rdx
 59b4c78:      	addq	%rax, %rdx
 59b4c7b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 59b4c85:      	addq	0x20(%rdi), %rax
 59b4c89:      	addq	%r11, %r13
 59b4c8c:      	movq	0x38(%rdi), %r10
 59b4c90:      	addq	%rax, %rcx
 59b4c93:      	addq	%r10, %rcx
 59b4c96:      	addq	%r9, %rcx
 59b4c99:      	rolq	$0x2b, %rcx
 59b4c9d:      	addq	%rsi, %r12
 59b4ca0:      	addq	%rax, %r12
 59b4ca3:      	movq	%r12, %rbx
 59b4ca6:      	rolq	$0x14, %rbx
 59b4caa:      	addq	%rax, %rbx
 59b4cad:      	addq	%rcx, %rbx
 59b4cb0:      	addq	%r10, %r12
 59b4cb3:      	movq	%r14, -0x20(%rsp)
 59b4cb8:      	cmpq	$0x40, %r14
 59b4cbc:      	jne	0x59b4cd2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 59b4cbe:      	movq	%rbx, %rsi
 59b4cc1:      	movq	%r12, %r11
 59b4cc4:      	movq	%rdx, %rax
 59b4cc7:      	movq	%r13, %r14
 59b4cca:      	movq	%rbp, %r15
 59b4ccd:      	jmp	0x59b4dbd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 59b4cd2:      	addq	$-0x40, -0x20(%rsp)
 59b4cd8:      	xorl	%ecx, %ecx
 59b4cda:      	nopw	(%rax,%rax)
 59b4ce0:      	addq	%r9, %r8
 59b4ce3:      	addq	%r13, %r8
 59b4ce6:      	movq	0x48(%rdi,%rcx), %r14
 59b4ceb:      	movq	0x50(%rdi,%rcx), %r10
 59b4cf0:      	addq	%r14, %r8
 59b4cf3:      	rolq	$0x1b, %r8
 59b4cf7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 59b4d01:      	imulq	%rsi, %r8
 59b4d05:      	addq	%rdx, %r9
 59b4d08:      	movq	0x70(%rdi,%rcx), %rax
 59b4d0d:      	movq	%rax, -0x8(%rsp)
 59b4d12:      	addq	%rax, %r9
 59b4d15:      	rolq	$0x16, %r9
 59b4d19:      	imulq	%rsi, %r9
 59b4d1d:      	movq	%r8, %r15
 59b4d20:      	xorq	%rbx, %r15
 59b4d23:      	movq	0x68(%rdi,%rcx), %r11
 59b4d28:      	addq	%r11, %r13
 59b4d2b:      	addq	%r12, %rbp
 59b4d2e:      	rolq	$0x1f, %rbp
 59b4d32:      	addq	%r13, %r9
 59b4d35:      	imulq	%rsi, %rdx
 59b4d39:      	addq	0x40(%rdi,%rcx), %rdx
 59b4d3e:      	movq	%rbp, %r8
 59b4d41:      	movq	0x58(%rdi,%rcx), %r13
 59b4d46:      	addq	%rdx, %r12
 59b4d49:      	addq	%r13, %r12
 59b4d4c:      	addq	%r15, %r12
 59b4d4f:      	rolq	$0x2b, %r12
 59b4d53:      	addq	%r10, %r14
 59b4d56:      	addq	%rdx, %r14
 59b4d59:      	movq	%r14, %rax
 59b4d5c:      	rolq	$0x14, %rax
 59b4d60:      	imulq	%rsi, %r8
 59b4d64:      	addq	%rdx, %rax
 59b4d67:      	addq	%r12, %rax
 59b4d6a:      	addq	%r8, %rbx
 59b4d6d:      	addq	%r9, %r10
 59b4d70:      	addq	0x60(%rdi,%rcx), %rbx
 59b4d75:      	movq	0x78(%rdi,%rcx), %rdx
 59b4d7a:      	addq	%rbx, %r10
 59b4d7d:      	addq	%rdx, %r10
 59b4d80:      	rolq	$0x2b, %r10
 59b4d84:      	addq	%r13, %r14
 59b4d87:      	addq	-0x8(%rsp), %r11
 59b4d8c:      	addq	%rbx, %r11
 59b4d8f:      	movq	%r11, %rsi
 59b4d92:      	rolq	$0x14, %rsi
 59b4d96:      	addq	%rbx, %rsi
 59b4d99:      	addq	%r10, %rsi
 59b4d9c:      	addq	%rdx, %r11
 59b4d9f:      	addq	$0x40, %rcx
 59b4da3:      	movq	%r15, %rbp
 59b4da6:      	movq	%r14, %r13
 59b4da9:      	movq	%rax, %rdx
 59b4dac:      	movq	%r11, %r12
 59b4daf:      	movq	%rsi, %rbx
 59b4db2:      	cmpq	%rcx, -0x20(%rsp)
 59b4db7:      	jne	0x59b4ce0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 59b4dbd:      	movq	-0x10(%rsp), %r12
 59b4dc2:      	testb	$0x3f, %r12b
 59b4dc6:      	je	0x59b4e93 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 59b4dcc:      	leaq	(%r9,%r14), %rdi
 59b4dd0:      	movq	-0x18(%rsp), %rbp
 59b4dd5:      	movq	-0x38(%rbp), %rcx
 59b4dd9:      	movq	-0x30(%rbp), %rdx
 59b4ddd:      	addq	%rcx, %r8
 59b4de0:      	addq	%rdi, %r8
 59b4de3:      	rolq	$0x1b, %r8
 59b4de7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 59b4df1:      	imulq	%r13, %r8
 59b4df5:      	addq	%rax, %r9
 59b4df8:      	movq	-0x10(%rbp), %r10
 59b4dfc:      	addq	%r10, %r9
 59b4dff:      	rolq	$0x16, %r9
 59b4e03:      	imulq	%r13, %r9
 59b4e07:      	xorq	%rsi, %r8
 59b4e0a:      	movq	-0x18(%rbp), %rdi
 59b4e0e:      	addq	%rdi, %r14
 59b4e11:      	addq	%r14, %r9
 59b4e14:      	addq	%r11, %r15
 59b4e17:      	rolq	$0x1f, %r15
 59b4e1b:      	movq	%r15, %rbx
 59b4e1e:      	imulq	%r13, %rax
 59b4e22:      	addq	%r8, %r11
 59b4e25:      	addq	-0x40(%rbp), %rax
 59b4e29:      	movq	-0x28(%rbp), %r15
 59b4e2d:      	addq	%r15, %r11
 59b4e30:      	addq	%rax, %r11
 59b4e33:      	rolq	$0x2b, %r11
 59b4e37:      	imulq	%r13, %rbx
 59b4e3b:      	addq	%rdx, %rcx
 59b4e3e:      	addq	%rax, %rcx
 59b4e41:      	movq	%rcx, %r14
 59b4e44:      	rolq	$0x14, %r14
 59b4e48:      	addq	%rax, %r14
 59b4e4b:      	addq	%r11, %r14
 59b4e4e:      	addq	%r15, %rcx
 59b4e51:      	addq	%rbx, %rsi
 59b4e54:      	addq	-0x20(%rbp), %rsi
 59b4e58:      	addq	%r9, %rdx
 59b4e5b:      	movq	-0x8(%rbp), %rax
 59b4e5f:      	addq	%rax, %rdx
 59b4e62:      	addq	%rsi, %rdx
 59b4e65:      	rolq	$0x2b, %rdx
 59b4e69:      	addq	%r10, %rdi
 59b4e6c:      	addq	%rsi, %rdi
 59b4e6f:      	movq	%rdi, %r10
 59b4e72:      	rolq	$0x14, %r10
 59b4e76:      	addq	%rsi, %r10
 59b4e79:      	addq	%rdx, %r10
 59b4e7c:      	addq	%rax, %rdi
 59b4e7f:      	movq	%r10, %rsi
 59b4e82:      	movq	%rdi, %r11
 59b4e85:      	movq	%r14, %rax
 59b4e88:      	movq	%rcx, %r14
 59b4e8b:      	movq	%r8, %r15
 59b4e8e:      	movq	%rbx, %r8
 59b4e91:      	jmp	0x59b4e9d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 59b4e93:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 59b4e9d:      	xorq	%r11, %r14
 59b4ea0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 59b4eaa:      	imulq	%rcx, %r14
 59b4eae:      	xorq	%r14, %r11
 59b4eb1:      	shrq	$0x2f, %r14
 59b4eb5:      	xorq	%r11, %r14
 59b4eb8:      	imulq	%rcx, %r14
 59b4ebc:      	movq	%r14, %rdi
 59b4ebf:      	shrq	$0x2f, %rdi
 59b4ec3:      	xorq	%r14, %rdi
 59b4ec6:      	imulq	%rcx, %rdi
 59b4eca:      	movq	%r9, %rdx
 59b4ecd:      	shrq	$0x2f, %rdx
 59b4ed1:      	xorq	%r9, %rdx
 59b4ed4:      	imulq	%r13, %rdx
 59b4ed8:      	addq	%r15, %rdx
 59b4edb:      	addq	%rdi, %rdx
 59b4ede:      	xorq	%rsi, %rax
 59b4ee1:      	imulq	%rcx, %rax
 59b4ee5:      	xorq	%rax, %rsi
 59b4ee8:      	shrq	$0x2f, %rax
 59b4eec:      	xorq	%rsi, %rax
 59b4eef:      	imulq	%rcx, %rax
 59b4ef3:      	movq	%rax, %rsi
 59b4ef6:      	shrq	$0x2f, %rsi
 59b4efa:      	xorq	%rax, %rsi
 59b4efd:      	imulq	%rcx, %rsi
 59b4f01:      	movq	%r12, %rax
 59b4f04:      	shrq	$0x2f, %rax
 59b4f08:      	xorq	%r12, %rax
 59b4f0b:      	imulq	%r13, %rax
 59b4f0f:      	addq	%r8, %rax
 59b4f12:      	addq	%rsi, %rax
 59b4f15:      	xorq	%rax, %rdx
 59b4f18:      	imulq	%rcx, %rdx
 59b4f1c:      	xorq	%rdx, %rax
 59b4f1f:      	shrq	$0x2f, %rdx
 59b4f23:      	xorq	%rax, %rdx
 59b4f26:      	imulq	%rcx, %rdx
 59b4f2a:      	movq	%rdx, %rax
 59b4f2d:      	shrq	$0x2f, %rax
 59b4f31:      	xorq	%rdx, %rax
 59b4f34:      	imulq	%rcx, %rax
 59b4f38:      	popq	%rbx
 59b4f39:      	popq	%r12
 59b4f3b:      	popq	%r13
 59b4f3d:      	popq	%r14
 59b4f3f:      	popq	%r15
 59b4f41:      	popq	%rbp
 59b4f42:      	retq
