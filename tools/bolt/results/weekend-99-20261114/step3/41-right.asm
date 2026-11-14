
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003c23ac0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3c23ac0:      	movq	%rsi, %rcx
 3c23ac3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3c23acd:      	subq	%rdi, %rsi
 3c23ad0:      	cmpq	$0x40, %rsi
 3c23ad4:      	ja	0x3c23ae4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3c23ad6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3c23adc:      	movq	%rax, %rdx
 3c23adf:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3c23ae4:      	pushq	%rbp
 3c23ae5:      	pushq	%r15
 3c23ae7:      	pushq	%r14
 3c23ae9:      	pushq	%r13
 3c23aeb:      	pushq	%r12
 3c23aed:      	pushq	%rbx
 3c23aee:      	movq	%rcx, -0x18(%rsp)
 3c23af3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3c23afd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3c23b07:      	movq	%rsi, -0x10(%rsp)
 3c23b0c:      	movq	%rsi, %r14
 3c23b0f:      	andq	$-0x40, %r14
 3c23b13:      	movq	0x8(%rdi), %r13
 3c23b17:      	movq	0x10(%rdi), %rcx
 3c23b1b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3c23b25:      	addq	%r13, %rdx
 3c23b28:      	rolq	$0x1b, %rdx
 3c23b2c:      	imulq	%r9, %rdx
 3c23b30:      	movq	0x30(%rdi), %rsi
 3c23b34:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3c23b3e:      	addq	%rsi, %r10
 3c23b41:      	rolq	$0x16, %r10
 3c23b45:      	imulq	%r9, %r10
 3c23b49:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3c23b53:      	xorq	%rdx, %rbp
 3c23b56:      	movq	0x28(%rdi), %r12
 3c23b5a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3c23b64:      	addq	%r12, %r9
 3c23b67:      	addq	%r10, %r9
 3c23b6a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3c23b74:      	addq	(%rdi), %r10
 3c23b77:      	movq	0x18(%rdi), %r11
 3c23b7b:      	addq	%r10, %rax
 3c23b7e:      	addq	%r11, %rax
 3c23b81:      	addq	%rbp, %rax
 3c23b84:      	rolq	$0x2b, %rax
 3c23b88:      	addq	%rcx, %r13
 3c23b8b:      	addq	%r10, %r13
 3c23b8e:      	movq	%r13, %rdx
 3c23b91:      	rolq	$0x14, %rdx
 3c23b95:      	addq	%r10, %rdx
 3c23b98:      	addq	%rax, %rdx
 3c23b9b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3c23ba5:      	addq	0x20(%rdi), %rax
 3c23ba9:      	addq	%r11, %r13
 3c23bac:      	movq	0x38(%rdi), %r10
 3c23bb0:      	addq	%rax, %rcx
 3c23bb3:      	addq	%r10, %rcx
 3c23bb6:      	addq	%r9, %rcx
 3c23bb9:      	rolq	$0x2b, %rcx
 3c23bbd:      	addq	%rsi, %r12
 3c23bc0:      	addq	%rax, %r12
 3c23bc3:      	movq	%r12, %rbx
 3c23bc6:      	rolq	$0x14, %rbx
 3c23bca:      	addq	%rax, %rbx
 3c23bcd:      	addq	%rcx, %rbx
 3c23bd0:      	addq	%r10, %r12
 3c23bd3:      	movq	%r14, -0x20(%rsp)
 3c23bd8:      	cmpq	$0x40, %r14
 3c23bdc:      	jne	0x3c23bf2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3c23bde:      	movq	%rbx, %rsi
 3c23be1:      	movq	%r12, %r11
 3c23be4:      	movq	%rdx, %rax
 3c23be7:      	movq	%r13, %r14
 3c23bea:      	movq	%rbp, %r15
 3c23bed:      	jmp	0x3c23cdd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3c23bf2:      	addq	$-0x40, -0x20(%rsp)
 3c23bf8:      	xorl	%ecx, %ecx
 3c23bfa:      	nopw	(%rax,%rax)
 3c23c00:      	addq	%r9, %r8
 3c23c03:      	addq	%r13, %r8
 3c23c06:      	movq	0x48(%rdi,%rcx), %r14
 3c23c0b:      	movq	0x50(%rdi,%rcx), %r10
 3c23c10:      	addq	%r14, %r8
 3c23c13:      	rolq	$0x1b, %r8
 3c23c17:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3c23c21:      	imulq	%rsi, %r8
 3c23c25:      	addq	%rdx, %r9
 3c23c28:      	movq	0x70(%rdi,%rcx), %rax
 3c23c2d:      	movq	%rax, -0x8(%rsp)
 3c23c32:      	addq	%rax, %r9
 3c23c35:      	rolq	$0x16, %r9
 3c23c39:      	imulq	%rsi, %r9
 3c23c3d:      	movq	%r8, %r15
 3c23c40:      	xorq	%rbx, %r15
 3c23c43:      	movq	0x68(%rdi,%rcx), %r11
 3c23c48:      	addq	%r11, %r13
 3c23c4b:      	addq	%r12, %rbp
 3c23c4e:      	rolq	$0x1f, %rbp
 3c23c52:      	addq	%r13, %r9
 3c23c55:      	imulq	%rsi, %rdx
 3c23c59:      	addq	0x40(%rdi,%rcx), %rdx
 3c23c5e:      	movq	%rbp, %r8
 3c23c61:      	movq	0x58(%rdi,%rcx), %r13
 3c23c66:      	addq	%rdx, %r12
 3c23c69:      	addq	%r13, %r12
 3c23c6c:      	addq	%r15, %r12
 3c23c6f:      	rolq	$0x2b, %r12
 3c23c73:      	addq	%r10, %r14
 3c23c76:      	addq	%rdx, %r14
 3c23c79:      	movq	%r14, %rax
 3c23c7c:      	rolq	$0x14, %rax
 3c23c80:      	imulq	%rsi, %r8
 3c23c84:      	addq	%rdx, %rax
 3c23c87:      	addq	%r12, %rax
 3c23c8a:      	addq	%r8, %rbx
 3c23c8d:      	addq	%r9, %r10
 3c23c90:      	addq	0x60(%rdi,%rcx), %rbx
 3c23c95:      	movq	0x78(%rdi,%rcx), %rdx
 3c23c9a:      	addq	%rbx, %r10
 3c23c9d:      	addq	%rdx, %r10
 3c23ca0:      	rolq	$0x2b, %r10
 3c23ca4:      	addq	%r13, %r14
 3c23ca7:      	addq	-0x8(%rsp), %r11
 3c23cac:      	addq	%rbx, %r11
 3c23caf:      	movq	%r11, %rsi
 3c23cb2:      	rolq	$0x14, %rsi
 3c23cb6:      	addq	%rbx, %rsi
 3c23cb9:      	addq	%r10, %rsi
 3c23cbc:      	addq	%rdx, %r11
 3c23cbf:      	addq	$0x40, %rcx
 3c23cc3:      	movq	%r15, %rbp
 3c23cc6:      	movq	%r14, %r13
 3c23cc9:      	movq	%rax, %rdx
 3c23ccc:      	movq	%r11, %r12
 3c23ccf:      	movq	%rsi, %rbx
 3c23cd2:      	cmpq	%rcx, -0x20(%rsp)
 3c23cd7:      	jne	0x3c23c00 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3c23cdd:      	movq	-0x10(%rsp), %r12
 3c23ce2:      	testb	$0x3f, %r12b
 3c23ce6:      	je	0x3c23db2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 3c23cec:      	movq	-0x18(%rsp), %rbp
 3c23cf1:      	movq	-0x38(%rbp), %rcx
 3c23cf5:      	movq	-0x30(%rbp), %rdx
 3c23cf9:      	addq	%rcx, %r8
 3c23cfc:      	addq	%r9, %r8
 3c23cff:      	addq	%r14, %r8
 3c23d02:      	rolq	$0x1b, %r8
 3c23d06:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3c23d10:      	imulq	%r13, %r8
 3c23d14:      	addq	%rax, %r9
 3c23d17:      	movq	-0x10(%rbp), %r10
 3c23d1b:      	addq	%r10, %r9
 3c23d1e:      	rolq	$0x16, %r9
 3c23d22:      	imulq	%r13, %r9
 3c23d26:      	xorq	%rsi, %r8
 3c23d29:      	movq	-0x18(%rbp), %rdi
 3c23d2d:      	addq	%rdi, %r14
 3c23d30:      	addq	%r14, %r9
 3c23d33:      	addq	%r11, %r15
 3c23d36:      	rolq	$0x1f, %r15
 3c23d3a:      	movq	%r15, %rbx
 3c23d3d:      	imulq	%r13, %rax
 3c23d41:      	addq	%r8, %r11
 3c23d44:      	addq	-0x40(%rbp), %rax
 3c23d48:      	movq	-0x28(%rbp), %r15
 3c23d4c:      	addq	%r15, %r11
 3c23d4f:      	addq	%rax, %r11
 3c23d52:      	rolq	$0x2b, %r11
 3c23d56:      	imulq	%r13, %rbx
 3c23d5a:      	addq	%rdx, %rcx
 3c23d5d:      	addq	%rax, %rcx
 3c23d60:      	movq	%rcx, %r14
 3c23d63:      	rolq	$0x14, %r14
 3c23d67:      	addq	%rax, %r14
 3c23d6a:      	addq	%r11, %r14
 3c23d6d:      	addq	%r15, %rcx
 3c23d70:      	addq	%rbx, %rsi
 3c23d73:      	addq	-0x20(%rbp), %rsi
 3c23d77:      	addq	%r9, %rdx
 3c23d7a:      	movq	-0x8(%rbp), %rax
 3c23d7e:      	addq	%rax, %rdx
 3c23d81:      	addq	%rsi, %rdx
 3c23d84:      	rolq	$0x2b, %rdx
 3c23d88:      	addq	%r10, %rdi
 3c23d8b:      	addq	%rsi, %rdi
 3c23d8e:      	movq	%rdi, %r10
 3c23d91:      	rolq	$0x14, %r10
 3c23d95:      	addq	%rsi, %r10
 3c23d98:      	addq	%rdx, %r10
 3c23d9b:      	addq	%rax, %rdi
 3c23d9e:      	movq	%r10, %rsi
 3c23da1:      	movq	%rdi, %r11
 3c23da4:      	movq	%r14, %rax
 3c23da7:      	movq	%rcx, %r14
 3c23daa:      	movq	%r8, %r15
 3c23dad:      	movq	%rbx, %r8
 3c23db0:      	jmp	0x3c23dbc <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 3c23db2:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3c23dbc:      	xorq	%r11, %r14
 3c23dbf:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3c23dc9:      	imulq	%rcx, %r14
 3c23dcd:      	xorq	%r14, %r11
 3c23dd0:      	shrq	$0x2f, %r14
 3c23dd4:      	xorq	%r11, %r14
 3c23dd7:      	imulq	%rcx, %r14
 3c23ddb:      	movq	%r14, %rdi
 3c23dde:      	shrq	$0x2f, %rdi
 3c23de2:      	xorq	%r14, %rdi
 3c23de5:      	imulq	%rcx, %rdi
 3c23de9:      	movq	%r9, %rdx
 3c23dec:      	shrq	$0x2f, %rdx
 3c23df0:      	xorq	%r9, %rdx
 3c23df3:      	imulq	%r13, %rdx
 3c23df7:      	addq	%r15, %rdx
 3c23dfa:      	addq	%rdi, %rdx
 3c23dfd:      	xorq	%rsi, %rax
 3c23e00:      	imulq	%rcx, %rax
 3c23e04:      	xorq	%rax, %rsi
 3c23e07:      	shrq	$0x2f, %rax
 3c23e0b:      	xorq	%rsi, %rax
 3c23e0e:      	imulq	%rcx, %rax
 3c23e12:      	movq	%rax, %rsi
 3c23e15:      	shrq	$0x2f, %rsi
 3c23e19:      	xorq	%rax, %rsi
 3c23e1c:      	imulq	%rcx, %rsi
 3c23e20:      	movq	%r12, %rax
 3c23e23:      	shrq	$0x2f, %rax
 3c23e27:      	xorq	%r12, %rax
 3c23e2a:      	imulq	%r13, %rax
 3c23e2e:      	addq	%r8, %rax
 3c23e31:      	addq	%rsi, %rax
 3c23e34:      	xorq	%rax, %rdx
 3c23e37:      	imulq	%rcx, %rdx
 3c23e3b:      	xorq	%rdx, %rax
 3c23e3e:      	shrq	$0x2f, %rdx
 3c23e42:      	xorq	%rax, %rdx
 3c23e45:      	imulq	%rcx, %rdx
 3c23e49:      	movq	%rdx, %rax
 3c23e4c:      	shrq	$0x2f, %rax
 3c23e50:      	xorq	%rdx, %rax
 3c23e53:      	imulq	%rcx, %rax
 3c23e57:      	popq	%rbx
 3c23e58:      	popq	%r12
 3c23e5a:      	popq	%r13
 3c23e5c:      	popq	%r14
 3c23e5e:      	popq	%r15
 3c23e60:      	popq	%rbp
 3c23e61:      	retq
