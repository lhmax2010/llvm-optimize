
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003c23b40 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3c23b40:      	movq	%rsi, %rcx
 3c23b43:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3c23b4d:      	subq	%rdi, %rsi
 3c23b50:      	cmpq	$0x40, %rsi
 3c23b54:      	ja	0x3c23b64 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3c23b56:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3c23b5c:      	movq	%rax, %rdx
 3c23b5f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3c23b64:      	pushq	%rbp
 3c23b65:      	pushq	%r15
 3c23b67:      	pushq	%r14
 3c23b69:      	pushq	%r13
 3c23b6b:      	pushq	%r12
 3c23b6d:      	pushq	%rbx
 3c23b6e:      	movq	%rcx, -0x18(%rsp)
 3c23b73:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3c23b7d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3c23b87:      	movq	%rsi, -0x10(%rsp)
 3c23b8c:      	movq	%rsi, %r14
 3c23b8f:      	andq	$-0x40, %r14
 3c23b93:      	movq	0x8(%rdi), %r13
 3c23b97:      	movq	0x10(%rdi), %rcx
 3c23b9b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3c23ba5:      	addq	%r13, %rdx
 3c23ba8:      	rolq	$0x1b, %rdx
 3c23bac:      	imulq	%r9, %rdx
 3c23bb0:      	movq	0x30(%rdi), %rsi
 3c23bb4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3c23bbe:      	addq	%rsi, %r10
 3c23bc1:      	rolq	$0x16, %r10
 3c23bc5:      	imulq	%r9, %r10
 3c23bc9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3c23bd3:      	xorq	%rdx, %rbp
 3c23bd6:      	movq	0x28(%rdi), %r12
 3c23bda:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3c23be4:      	addq	%r12, %r9
 3c23be7:      	addq	%r10, %r9
 3c23bea:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3c23bf4:      	addq	(%rdi), %r10
 3c23bf7:      	movq	0x18(%rdi), %r11
 3c23bfb:      	addq	%r10, %rax
 3c23bfe:      	addq	%r11, %rax
 3c23c01:      	addq	%rbp, %rax
 3c23c04:      	rolq	$0x2b, %rax
 3c23c08:      	addq	%rcx, %r13
 3c23c0b:      	addq	%r10, %r13
 3c23c0e:      	movq	%r13, %rdx
 3c23c11:      	rolq	$0x14, %rdx
 3c23c15:      	addq	%r10, %rdx
 3c23c18:      	addq	%rax, %rdx
 3c23c1b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3c23c25:      	addq	0x20(%rdi), %rax
 3c23c29:      	addq	%r11, %r13
 3c23c2c:      	movq	0x38(%rdi), %r10
 3c23c30:      	addq	%rax, %rcx
 3c23c33:      	addq	%r10, %rcx
 3c23c36:      	addq	%r9, %rcx
 3c23c39:      	rolq	$0x2b, %rcx
 3c23c3d:      	addq	%rsi, %r12
 3c23c40:      	addq	%rax, %r12
 3c23c43:      	movq	%r12, %rbx
 3c23c46:      	rolq	$0x14, %rbx
 3c23c4a:      	addq	%rax, %rbx
 3c23c4d:      	addq	%rcx, %rbx
 3c23c50:      	addq	%r10, %r12
 3c23c53:      	movq	%r14, -0x20(%rsp)
 3c23c58:      	cmpq	$0x40, %r14
 3c23c5c:      	jne	0x3c23c72 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3c23c5e:      	movq	%rbx, %rsi
 3c23c61:      	movq	%r12, %r11
 3c23c64:      	movq	%rdx, %rax
 3c23c67:      	movq	%r13, %r14
 3c23c6a:      	movq	%rbp, %r15
 3c23c6d:      	jmp	0x3c23d5d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3c23c72:      	addq	$-0x40, -0x20(%rsp)
 3c23c78:      	xorl	%ecx, %ecx
 3c23c7a:      	nopw	(%rax,%rax)
 3c23c80:      	addq	%r9, %r8
 3c23c83:      	addq	%r13, %r8
 3c23c86:      	movq	0x48(%rdi,%rcx), %r14
 3c23c8b:      	movq	0x50(%rdi,%rcx), %r10
 3c23c90:      	addq	%r14, %r8
 3c23c93:      	rolq	$0x1b, %r8
 3c23c97:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3c23ca1:      	imulq	%rsi, %r8
 3c23ca5:      	addq	%rdx, %r9
 3c23ca8:      	movq	0x70(%rdi,%rcx), %rax
 3c23cad:      	movq	%rax, -0x8(%rsp)
 3c23cb2:      	addq	%rax, %r9
 3c23cb5:      	rolq	$0x16, %r9
 3c23cb9:      	imulq	%rsi, %r9
 3c23cbd:      	movq	%r8, %r15
 3c23cc0:      	xorq	%rbx, %r15
 3c23cc3:      	movq	0x68(%rdi,%rcx), %r11
 3c23cc8:      	addq	%r11, %r13
 3c23ccb:      	addq	%r12, %rbp
 3c23cce:      	rolq	$0x1f, %rbp
 3c23cd2:      	addq	%r13, %r9
 3c23cd5:      	imulq	%rsi, %rdx
 3c23cd9:      	addq	0x40(%rdi,%rcx), %rdx
 3c23cde:      	movq	%rbp, %r8
 3c23ce1:      	movq	0x58(%rdi,%rcx), %r13
 3c23ce6:      	addq	%rdx, %r12
 3c23ce9:      	addq	%r13, %r12
 3c23cec:      	addq	%r15, %r12
 3c23cef:      	rolq	$0x2b, %r12
 3c23cf3:      	addq	%r10, %r14
 3c23cf6:      	addq	%rdx, %r14
 3c23cf9:      	movq	%r14, %rax
 3c23cfc:      	rolq	$0x14, %rax
 3c23d00:      	imulq	%rsi, %r8
 3c23d04:      	addq	%rdx, %rax
 3c23d07:      	addq	%r12, %rax
 3c23d0a:      	addq	%r8, %rbx
 3c23d0d:      	addq	%r9, %r10
 3c23d10:      	addq	0x60(%rdi,%rcx), %rbx
 3c23d15:      	movq	0x78(%rdi,%rcx), %rdx
 3c23d1a:      	addq	%rbx, %r10
 3c23d1d:      	addq	%rdx, %r10
 3c23d20:      	rolq	$0x2b, %r10
 3c23d24:      	addq	%r13, %r14
 3c23d27:      	addq	-0x8(%rsp), %r11
 3c23d2c:      	addq	%rbx, %r11
 3c23d2f:      	movq	%r11, %rsi
 3c23d32:      	rolq	$0x14, %rsi
 3c23d36:      	addq	%rbx, %rsi
 3c23d39:      	addq	%r10, %rsi
 3c23d3c:      	addq	%rdx, %r11
 3c23d3f:      	addq	$0x40, %rcx
 3c23d43:      	movq	%r15, %rbp
 3c23d46:      	movq	%r14, %r13
 3c23d49:      	movq	%rax, %rdx
 3c23d4c:      	movq	%r11, %r12
 3c23d4f:      	movq	%rsi, %rbx
 3c23d52:      	cmpq	%rcx, -0x20(%rsp)
 3c23d57:      	jne	0x3c23c80 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3c23d5d:      	movq	-0x10(%rsp), %r12
 3c23d62:      	testb	$0x3f, %r12b
 3c23d66:      	je	0x3c23e33 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 3c23d6c:      	leaq	(%r9,%r14), %rdi
 3c23d70:      	movq	-0x18(%rsp), %rbp
 3c23d75:      	movq	-0x38(%rbp), %rcx
 3c23d79:      	movq	-0x30(%rbp), %rdx
 3c23d7d:      	addq	%rcx, %r8
 3c23d80:      	addq	%rdi, %r8
 3c23d83:      	rolq	$0x1b, %r8
 3c23d87:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3c23d91:      	imulq	%r13, %r8
 3c23d95:      	addq	%rax, %r9
 3c23d98:      	movq	-0x10(%rbp), %r10
 3c23d9c:      	addq	%r10, %r9
 3c23d9f:      	rolq	$0x16, %r9
 3c23da3:      	imulq	%r13, %r9
 3c23da7:      	xorq	%rsi, %r8
 3c23daa:      	movq	-0x18(%rbp), %rdi
 3c23dae:      	addq	%rdi, %r14
 3c23db1:      	addq	%r14, %r9
 3c23db4:      	addq	%r11, %r15
 3c23db7:      	rolq	$0x1f, %r15
 3c23dbb:      	movq	%r15, %rbx
 3c23dbe:      	imulq	%r13, %rax
 3c23dc2:      	addq	%r8, %r11
 3c23dc5:      	addq	-0x40(%rbp), %rax
 3c23dc9:      	movq	-0x28(%rbp), %r15
 3c23dcd:      	addq	%r15, %r11
 3c23dd0:      	addq	%rax, %r11
 3c23dd3:      	rolq	$0x2b, %r11
 3c23dd7:      	imulq	%r13, %rbx
 3c23ddb:      	addq	%rdx, %rcx
 3c23dde:      	addq	%rax, %rcx
 3c23de1:      	movq	%rcx, %r14
 3c23de4:      	rolq	$0x14, %r14
 3c23de8:      	addq	%rax, %r14
 3c23deb:      	addq	%r11, %r14
 3c23dee:      	addq	%r15, %rcx
 3c23df1:      	addq	%rbx, %rsi
 3c23df4:      	addq	-0x20(%rbp), %rsi
 3c23df8:      	addq	%r9, %rdx
 3c23dfb:      	movq	-0x8(%rbp), %rax
 3c23dff:      	addq	%rax, %rdx
 3c23e02:      	addq	%rsi, %rdx
 3c23e05:      	rolq	$0x2b, %rdx
 3c23e09:      	addq	%r10, %rdi
 3c23e0c:      	addq	%rsi, %rdi
 3c23e0f:      	movq	%rdi, %r10
 3c23e12:      	rolq	$0x14, %r10
 3c23e16:      	addq	%rsi, %r10
 3c23e19:      	addq	%rdx, %r10
 3c23e1c:      	addq	%rax, %rdi
 3c23e1f:      	movq	%r10, %rsi
 3c23e22:      	movq	%rdi, %r11
 3c23e25:      	movq	%r14, %rax
 3c23e28:      	movq	%rcx, %r14
 3c23e2b:      	movq	%r8, %r15
 3c23e2e:      	movq	%rbx, %r8
 3c23e31:      	jmp	0x3c23e3d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 3c23e33:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3c23e3d:      	xorq	%r11, %r14
 3c23e40:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3c23e4a:      	imulq	%rcx, %r14
 3c23e4e:      	xorq	%r14, %r11
 3c23e51:      	shrq	$0x2f, %r14
 3c23e55:      	xorq	%r11, %r14
 3c23e58:      	imulq	%rcx, %r14
 3c23e5c:      	movq	%r14, %rdi
 3c23e5f:      	shrq	$0x2f, %rdi
 3c23e63:      	xorq	%r14, %rdi
 3c23e66:      	imulq	%rcx, %rdi
 3c23e6a:      	movq	%r9, %rdx
 3c23e6d:      	shrq	$0x2f, %rdx
 3c23e71:      	xorq	%r9, %rdx
 3c23e74:      	imulq	%r13, %rdx
 3c23e78:      	addq	%r15, %rdx
 3c23e7b:      	addq	%rdi, %rdx
 3c23e7e:      	xorq	%rsi, %rax
 3c23e81:      	imulq	%rcx, %rax
 3c23e85:      	xorq	%rax, %rsi
 3c23e88:      	shrq	$0x2f, %rax
 3c23e8c:      	xorq	%rsi, %rax
 3c23e8f:      	imulq	%rcx, %rax
 3c23e93:      	movq	%rax, %rsi
 3c23e96:      	shrq	$0x2f, %rsi
 3c23e9a:      	xorq	%rax, %rsi
 3c23e9d:      	imulq	%rcx, %rsi
 3c23ea1:      	movq	%r12, %rax
 3c23ea4:      	shrq	$0x2f, %rax
 3c23ea8:      	xorq	%r12, %rax
 3c23eab:      	imulq	%r13, %rax
 3c23eaf:      	addq	%r8, %rax
 3c23eb2:      	addq	%rsi, %rax
 3c23eb5:      	xorq	%rax, %rdx
 3c23eb8:      	imulq	%rcx, %rdx
 3c23ebc:      	xorq	%rdx, %rax
 3c23ebf:      	shrq	$0x2f, %rdx
 3c23ec3:      	xorq	%rax, %rdx
 3c23ec6:      	imulq	%rcx, %rdx
 3c23eca:      	movq	%rdx, %rax
 3c23ecd:      	shrq	$0x2f, %rax
 3c23ed1:      	xorq	%rdx, %rax
 3c23ed4:      	imulq	%rcx, %rax
 3c23ed8:      	popq	%rbx
 3c23ed9:      	popq	%r12
 3c23edb:      	popq	%r13
 3c23edd:      	popq	%r14
 3c23edf:      	popq	%r15
 3c23ee1:      	popq	%rbp
 3c23ee2:      	retq
