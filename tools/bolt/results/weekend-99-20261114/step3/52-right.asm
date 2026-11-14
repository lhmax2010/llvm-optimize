
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003660c20 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_>:
 3660c20:      	movq	%rsi, %rcx
 3660c23:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3660c2d:      	subq	%rdi, %rsi
 3660c30:      	cmpq	$0x40, %rsi
 3660c34:      	ja	0x3660c44 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x24>
 3660c36:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3660c3c:      	movq	%rax, %rdx
 3660c3f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3660c44:      	pushq	%rbp
 3660c45:      	pushq	%r15
 3660c47:      	pushq	%r14
 3660c49:      	pushq	%r13
 3660c4b:      	pushq	%r12
 3660c4d:      	pushq	%rbx
 3660c4e:      	movq	%rcx, -0x18(%rsp)
 3660c53:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3660c5d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3660c67:      	movq	%rsi, -0x10(%rsp)
 3660c6c:      	movq	%rsi, %r14
 3660c6f:      	andq	$-0x40, %r14
 3660c73:      	movq	0x8(%rdi), %r13
 3660c77:      	movq	0x10(%rdi), %rcx
 3660c7b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3660c85:      	addq	%r13, %rdx
 3660c88:      	rolq	$0x1b, %rdx
 3660c8c:      	imulq	%r9, %rdx
 3660c90:      	movq	0x30(%rdi), %rsi
 3660c94:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3660c9e:      	addq	%rsi, %r10
 3660ca1:      	rolq	$0x16, %r10
 3660ca5:      	imulq	%r9, %r10
 3660ca9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3660cb3:      	xorq	%rdx, %rbp
 3660cb6:      	movq	0x28(%rdi), %r12
 3660cba:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3660cc4:      	addq	%r12, %r9
 3660cc7:      	addq	%r10, %r9
 3660cca:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3660cd4:      	addq	(%rdi), %r10
 3660cd7:      	movq	0x18(%rdi), %r11
 3660cdb:      	addq	%r10, %rax
 3660cde:      	addq	%r11, %rax
 3660ce1:      	addq	%rbp, %rax
 3660ce4:      	rolq	$0x2b, %rax
 3660ce8:      	addq	%rcx, %r13
 3660ceb:      	addq	%r10, %r13
 3660cee:      	movq	%r13, %rdx
 3660cf1:      	rolq	$0x14, %rdx
 3660cf5:      	addq	%r10, %rdx
 3660cf8:      	addq	%rax, %rdx
 3660cfb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3660d05:      	addq	0x20(%rdi), %rax
 3660d09:      	addq	%r11, %r13
 3660d0c:      	movq	0x38(%rdi), %r10
 3660d10:      	addq	%rax, %rcx
 3660d13:      	addq	%r10, %rcx
 3660d16:      	addq	%r9, %rcx
 3660d19:      	rolq	$0x2b, %rcx
 3660d1d:      	addq	%rsi, %r12
 3660d20:      	addq	%rax, %r12
 3660d23:      	movq	%r12, %rbx
 3660d26:      	rolq	$0x14, %rbx
 3660d2a:      	addq	%rax, %rbx
 3660d2d:      	addq	%rcx, %rbx
 3660d30:      	addq	%r10, %r12
 3660d33:      	movq	%r14, -0x20(%rsp)
 3660d38:      	cmpq	$0x40, %r14
 3660d3c:      	jne	0x3660d52 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x132>
 3660d3e:      	movq	%rbx, %rsi
 3660d41:      	movq	%r12, %r11
 3660d44:      	movq	%rdx, %rax
 3660d47:      	movq	%r13, %r14
 3660d4a:      	movq	%rbp, %r15
 3660d4d:      	jmp	0x3660e3d <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x21d>
 3660d52:      	addq	$-0x40, -0x20(%rsp)
 3660d58:      	xorl	%ecx, %ecx
 3660d5a:      	nopw	(%rax,%rax)
 3660d60:      	addq	%r9, %r8
 3660d63:      	addq	%r13, %r8
 3660d66:      	movq	0x48(%rdi,%rcx), %r14
 3660d6b:      	movq	0x50(%rdi,%rcx), %r10
 3660d70:      	addq	%r14, %r8
 3660d73:      	rolq	$0x1b, %r8
 3660d77:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3660d81:      	imulq	%rsi, %r8
 3660d85:      	addq	%rdx, %r9
 3660d88:      	movq	0x70(%rdi,%rcx), %rax
 3660d8d:      	movq	%rax, -0x8(%rsp)
 3660d92:      	addq	%rax, %r9
 3660d95:      	rolq	$0x16, %r9
 3660d99:      	imulq	%rsi, %r9
 3660d9d:      	movq	%r8, %r15
 3660da0:      	xorq	%rbx, %r15
 3660da3:      	movq	0x68(%rdi,%rcx), %r11
 3660da8:      	addq	%r11, %r13
 3660dab:      	addq	%r12, %rbp
 3660dae:      	rolq	$0x1f, %rbp
 3660db2:      	addq	%r13, %r9
 3660db5:      	imulq	%rsi, %rdx
 3660db9:      	addq	0x40(%rdi,%rcx), %rdx
 3660dbe:      	movq	%rbp, %r8
 3660dc1:      	movq	0x58(%rdi,%rcx), %r13
 3660dc6:      	addq	%rdx, %r12
 3660dc9:      	addq	%r13, %r12
 3660dcc:      	addq	%r15, %r12
 3660dcf:      	rolq	$0x2b, %r12
 3660dd3:      	addq	%r10, %r14
 3660dd6:      	addq	%rdx, %r14
 3660dd9:      	movq	%r14, %rax
 3660ddc:      	rolq	$0x14, %rax
 3660de0:      	imulq	%rsi, %r8
 3660de4:      	addq	%rdx, %rax
 3660de7:      	addq	%r12, %rax
 3660dea:      	addq	%r8, %rbx
 3660ded:      	addq	%r9, %r10
 3660df0:      	addq	0x60(%rdi,%rcx), %rbx
 3660df5:      	movq	0x78(%rdi,%rcx), %rdx
 3660dfa:      	addq	%rbx, %r10
 3660dfd:      	addq	%rdx, %r10
 3660e00:      	rolq	$0x2b, %r10
 3660e04:      	addq	%r13, %r14
 3660e07:      	addq	-0x8(%rsp), %r11
 3660e0c:      	addq	%rbx, %r11
 3660e0f:      	movq	%r11, %rsi
 3660e12:      	rolq	$0x14, %rsi
 3660e16:      	addq	%rbx, %rsi
 3660e19:      	addq	%r10, %rsi
 3660e1c:      	addq	%rdx, %r11
 3660e1f:      	addq	$0x40, %rcx
 3660e23:      	movq	%r15, %rbp
 3660e26:      	movq	%r14, %r13
 3660e29:      	movq	%rax, %rdx
 3660e2c:      	movq	%r11, %r12
 3660e2f:      	movq	%rsi, %rbx
 3660e32:      	cmpq	%rcx, -0x20(%rsp)
 3660e37:      	jne	0x3660d60 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x140>
 3660e3d:      	movq	-0x10(%rsp), %r12
 3660e42:      	testb	$0x3f, %r12b
 3660e46:      	je	0x3660f12 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2f2>
 3660e4c:      	movq	-0x18(%rsp), %rbp
 3660e51:      	movq	-0x38(%rbp), %rcx
 3660e55:      	movq	-0x30(%rbp), %rdx
 3660e59:      	addq	%rcx, %r8
 3660e5c:      	addq	%r9, %r8
 3660e5f:      	addq	%r14, %r8
 3660e62:      	rolq	$0x1b, %r8
 3660e66:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3660e70:      	imulq	%r13, %r8
 3660e74:      	addq	%rax, %r9
 3660e77:      	movq	-0x10(%rbp), %r10
 3660e7b:      	addq	%r10, %r9
 3660e7e:      	rolq	$0x16, %r9
 3660e82:      	imulq	%r13, %r9
 3660e86:      	xorq	%rsi, %r8
 3660e89:      	movq	-0x18(%rbp), %rdi
 3660e8d:      	addq	%rdi, %r14
 3660e90:      	addq	%r14, %r9
 3660e93:      	addq	%r11, %r15
 3660e96:      	rolq	$0x1f, %r15
 3660e9a:      	movq	%r15, %rbx
 3660e9d:      	imulq	%r13, %rax
 3660ea1:      	addq	%r8, %r11
 3660ea4:      	addq	-0x40(%rbp), %rax
 3660ea8:      	movq	-0x28(%rbp), %r15
 3660eac:      	addq	%r15, %r11
 3660eaf:      	addq	%rax, %r11
 3660eb2:      	rolq	$0x2b, %r11
 3660eb6:      	imulq	%r13, %rbx
 3660eba:      	addq	%rdx, %rcx
 3660ebd:      	addq	%rax, %rcx
 3660ec0:      	movq	%rcx, %r14
 3660ec3:      	rolq	$0x14, %r14
 3660ec7:      	addq	%rax, %r14
 3660eca:      	addq	%r11, %r14
 3660ecd:      	addq	%r15, %rcx
 3660ed0:      	addq	%rbx, %rsi
 3660ed3:      	addq	-0x20(%rbp), %rsi
 3660ed7:      	addq	%r9, %rdx
 3660eda:      	movq	-0x8(%rbp), %rax
 3660ede:      	addq	%rax, %rdx
 3660ee1:      	addq	%rsi, %rdx
 3660ee4:      	rolq	$0x2b, %rdx
 3660ee8:      	addq	%r10, %rdi
 3660eeb:      	addq	%rsi, %rdi
 3660eee:      	movq	%rdi, %r10
 3660ef1:      	rolq	$0x14, %r10
 3660ef5:      	addq	%rsi, %r10
 3660ef8:      	addq	%rdx, %r10
 3660efb:      	addq	%rax, %rdi
 3660efe:      	movq	%r10, %rsi
 3660f01:      	movq	%rdi, %r11
 3660f04:      	movq	%r14, %rax
 3660f07:      	movq	%rcx, %r14
 3660f0a:      	movq	%r8, %r15
 3660f0d:      	movq	%rbx, %r8
 3660f10:      	jmp	0x3660f1c <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2fc>
 3660f12:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3660f1c:      	xorq	%r11, %r14
 3660f1f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3660f29:      	imulq	%rcx, %r14
 3660f2d:      	xorq	%r14, %r11
 3660f30:      	shrq	$0x2f, %r14
 3660f34:      	xorq	%r11, %r14
 3660f37:      	imulq	%rcx, %r14
 3660f3b:      	movq	%r14, %rdi
 3660f3e:      	shrq	$0x2f, %rdi
 3660f42:      	xorq	%r14, %rdi
 3660f45:      	imulq	%rcx, %rdi
 3660f49:      	movq	%r9, %rdx
 3660f4c:      	shrq	$0x2f, %rdx
 3660f50:      	xorq	%r9, %rdx
 3660f53:      	imulq	%r13, %rdx
 3660f57:      	addq	%r15, %rdx
 3660f5a:      	addq	%rdi, %rdx
 3660f5d:      	xorq	%rsi, %rax
 3660f60:      	imulq	%rcx, %rax
 3660f64:      	xorq	%rax, %rsi
 3660f67:      	shrq	$0x2f, %rax
 3660f6b:      	xorq	%rsi, %rax
 3660f6e:      	imulq	%rcx, %rax
 3660f72:      	movq	%rax, %rsi
 3660f75:      	shrq	$0x2f, %rsi
 3660f79:      	xorq	%rax, %rsi
 3660f7c:      	imulq	%rcx, %rsi
 3660f80:      	movq	%r12, %rax
 3660f83:      	shrq	$0x2f, %rax
 3660f87:      	xorq	%r12, %rax
 3660f8a:      	imulq	%r13, %rax
 3660f8e:      	addq	%r8, %rax
 3660f91:      	addq	%rsi, %rax
 3660f94:      	xorq	%rax, %rdx
 3660f97:      	imulq	%rcx, %rdx
 3660f9b:      	xorq	%rdx, %rax
 3660f9e:      	shrq	$0x2f, %rdx
 3660fa2:      	xorq	%rax, %rdx
 3660fa5:      	imulq	%rcx, %rdx
 3660fa9:      	movq	%rdx, %rax
 3660fac:      	shrq	$0x2f, %rax
 3660fb0:      	xorq	%rdx, %rax
 3660fb3:      	imulq	%rcx, %rax
 3660fb7:      	popq	%rbx
 3660fb8:      	popq	%r12
 3660fba:      	popq	%r13
 3660fbc:      	popq	%r14
 3660fbe:      	popq	%r15
 3660fc0:      	popq	%rbp
 3660fc1:      	retq
