
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000059b4b10 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 59b4b10:      	movq	%rsi, %rcx
 59b4b13:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 59b4b1d:      	subq	%rdi, %rsi
 59b4b20:      	cmpq	$0x40, %rsi
 59b4b24:      	ja	0x59b4b34 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 59b4b26:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 59b4b2c:      	movq	%rax, %rdx
 59b4b2f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 59b4b34:      	pushq	%rbp
 59b4b35:      	pushq	%r15
 59b4b37:      	pushq	%r14
 59b4b39:      	pushq	%r13
 59b4b3b:      	pushq	%r12
 59b4b3d:      	pushq	%rbx
 59b4b3e:      	movq	%rcx, -0x18(%rsp)
 59b4b43:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 59b4b4d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 59b4b57:      	movq	%rsi, -0x10(%rsp)
 59b4b5c:      	movq	%rsi, %r14
 59b4b5f:      	andq	$-0x40, %r14
 59b4b63:      	movq	0x8(%rdi), %r13
 59b4b67:      	movq	0x10(%rdi), %rcx
 59b4b6b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 59b4b75:      	addq	%r13, %rdx
 59b4b78:      	rolq	$0x1b, %rdx
 59b4b7c:      	imulq	%r9, %rdx
 59b4b80:      	movq	0x30(%rdi), %rsi
 59b4b84:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 59b4b8e:      	addq	%rsi, %r10
 59b4b91:      	rolq	$0x16, %r10
 59b4b95:      	imulq	%r9, %r10
 59b4b99:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 59b4ba3:      	xorq	%rdx, %rbp
 59b4ba6:      	movq	0x28(%rdi), %r12
 59b4baa:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 59b4bb4:      	addq	%r12, %r9
 59b4bb7:      	addq	%r10, %r9
 59b4bba:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 59b4bc4:      	addq	(%rdi), %r10
 59b4bc7:      	movq	0x18(%rdi), %r11
 59b4bcb:      	addq	%r10, %rax
 59b4bce:      	addq	%r11, %rax
 59b4bd1:      	addq	%rbp, %rax
 59b4bd4:      	rolq	$0x2b, %rax
 59b4bd8:      	addq	%rcx, %r13
 59b4bdb:      	addq	%r10, %r13
 59b4bde:      	movq	%r13, %rdx
 59b4be1:      	rolq	$0x14, %rdx
 59b4be5:      	addq	%r10, %rdx
 59b4be8:      	addq	%rax, %rdx
 59b4beb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 59b4bf5:      	addq	0x20(%rdi), %rax
 59b4bf9:      	addq	%r11, %r13
 59b4bfc:      	movq	0x38(%rdi), %r10
 59b4c00:      	addq	%rax, %rcx
 59b4c03:      	addq	%r10, %rcx
 59b4c06:      	addq	%r9, %rcx
 59b4c09:      	rolq	$0x2b, %rcx
 59b4c0d:      	addq	%rsi, %r12
 59b4c10:      	addq	%rax, %r12
 59b4c13:      	movq	%r12, %rbx
 59b4c16:      	rolq	$0x14, %rbx
 59b4c1a:      	addq	%rax, %rbx
 59b4c1d:      	addq	%rcx, %rbx
 59b4c20:      	addq	%r10, %r12
 59b4c23:      	movq	%r14, -0x20(%rsp)
 59b4c28:      	cmpq	$0x40, %r14
 59b4c2c:      	jne	0x59b4c42 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 59b4c2e:      	movq	%rbx, %rsi
 59b4c31:      	movq	%r12, %r11
 59b4c34:      	movq	%rdx, %rax
 59b4c37:      	movq	%r13, %r14
 59b4c3a:      	movq	%rbp, %r15
 59b4c3d:      	jmp	0x59b4d2d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 59b4c42:      	addq	$-0x40, -0x20(%rsp)
 59b4c48:      	xorl	%ecx, %ecx
 59b4c4a:      	nopw	(%rax,%rax)
 59b4c50:      	addq	%r9, %r8
 59b4c53:      	addq	%r13, %r8
 59b4c56:      	movq	0x48(%rdi,%rcx), %r14
 59b4c5b:      	movq	0x50(%rdi,%rcx), %r10
 59b4c60:      	addq	%r14, %r8
 59b4c63:      	rolq	$0x1b, %r8
 59b4c67:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 59b4c71:      	imulq	%rsi, %r8
 59b4c75:      	addq	%rdx, %r9
 59b4c78:      	movq	0x70(%rdi,%rcx), %rax
 59b4c7d:      	movq	%rax, -0x8(%rsp)
 59b4c82:      	addq	%rax, %r9
 59b4c85:      	rolq	$0x16, %r9
 59b4c89:      	imulq	%rsi, %r9
 59b4c8d:      	movq	%r8, %r15
 59b4c90:      	xorq	%rbx, %r15
 59b4c93:      	movq	0x68(%rdi,%rcx), %r11
 59b4c98:      	addq	%r11, %r13
 59b4c9b:      	addq	%r12, %rbp
 59b4c9e:      	rolq	$0x1f, %rbp
 59b4ca2:      	addq	%r13, %r9
 59b4ca5:      	imulq	%rsi, %rdx
 59b4ca9:      	addq	0x40(%rdi,%rcx), %rdx
 59b4cae:      	movq	%rbp, %r8
 59b4cb1:      	movq	0x58(%rdi,%rcx), %r13
 59b4cb6:      	addq	%rdx, %r12
 59b4cb9:      	addq	%r13, %r12
 59b4cbc:      	addq	%r15, %r12
 59b4cbf:      	rolq	$0x2b, %r12
 59b4cc3:      	addq	%r10, %r14
 59b4cc6:      	addq	%rdx, %r14
 59b4cc9:      	movq	%r14, %rax
 59b4ccc:      	rolq	$0x14, %rax
 59b4cd0:      	imulq	%rsi, %r8
 59b4cd4:      	addq	%rdx, %rax
 59b4cd7:      	addq	%r12, %rax
 59b4cda:      	addq	%r8, %rbx
 59b4cdd:      	addq	%r9, %r10
 59b4ce0:      	addq	0x60(%rdi,%rcx), %rbx
 59b4ce5:      	movq	0x78(%rdi,%rcx), %rdx
 59b4cea:      	addq	%rbx, %r10
 59b4ced:      	addq	%rdx, %r10
 59b4cf0:      	rolq	$0x2b, %r10
 59b4cf4:      	addq	%r13, %r14
 59b4cf7:      	addq	-0x8(%rsp), %r11
 59b4cfc:      	addq	%rbx, %r11
 59b4cff:      	movq	%r11, %rsi
 59b4d02:      	rolq	$0x14, %rsi
 59b4d06:      	addq	%rbx, %rsi
 59b4d09:      	addq	%r10, %rsi
 59b4d0c:      	addq	%rdx, %r11
 59b4d0f:      	addq	$0x40, %rcx
 59b4d13:      	movq	%r15, %rbp
 59b4d16:      	movq	%r14, %r13
 59b4d19:      	movq	%rax, %rdx
 59b4d1c:      	movq	%r11, %r12
 59b4d1f:      	movq	%rsi, %rbx
 59b4d22:      	cmpq	%rcx, -0x20(%rsp)
 59b4d27:      	jne	0x59b4c50 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 59b4d2d:      	movq	-0x10(%rsp), %r12
 59b4d32:      	testb	$0x3f, %r12b
 59b4d36:      	je	0x59b4e02 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 59b4d3c:      	movq	-0x18(%rsp), %rbp
 59b4d41:      	movq	-0x38(%rbp), %rcx
 59b4d45:      	movq	-0x30(%rbp), %rdx
 59b4d49:      	addq	%rcx, %r8
 59b4d4c:      	addq	%r9, %r8
 59b4d4f:      	addq	%r14, %r8
 59b4d52:      	rolq	$0x1b, %r8
 59b4d56:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 59b4d60:      	imulq	%r13, %r8
 59b4d64:      	addq	%rax, %r9
 59b4d67:      	movq	-0x10(%rbp), %r10
 59b4d6b:      	addq	%r10, %r9
 59b4d6e:      	rolq	$0x16, %r9
 59b4d72:      	imulq	%r13, %r9
 59b4d76:      	xorq	%rsi, %r8
 59b4d79:      	movq	-0x18(%rbp), %rdi
 59b4d7d:      	addq	%rdi, %r14
 59b4d80:      	addq	%r14, %r9
 59b4d83:      	addq	%r11, %r15
 59b4d86:      	rolq	$0x1f, %r15
 59b4d8a:      	movq	%r15, %rbx
 59b4d8d:      	imulq	%r13, %rax
 59b4d91:      	addq	%r8, %r11
 59b4d94:      	addq	-0x40(%rbp), %rax
 59b4d98:      	movq	-0x28(%rbp), %r15
 59b4d9c:      	addq	%r15, %r11
 59b4d9f:      	addq	%rax, %r11
 59b4da2:      	rolq	$0x2b, %r11
 59b4da6:      	imulq	%r13, %rbx
 59b4daa:      	addq	%rdx, %rcx
 59b4dad:      	addq	%rax, %rcx
 59b4db0:      	movq	%rcx, %r14
 59b4db3:      	rolq	$0x14, %r14
 59b4db7:      	addq	%rax, %r14
 59b4dba:      	addq	%r11, %r14
 59b4dbd:      	addq	%r15, %rcx
 59b4dc0:      	addq	%rbx, %rsi
 59b4dc3:      	addq	-0x20(%rbp), %rsi
 59b4dc7:      	addq	%r9, %rdx
 59b4dca:      	movq	-0x8(%rbp), %rax
 59b4dce:      	addq	%rax, %rdx
 59b4dd1:      	addq	%rsi, %rdx
 59b4dd4:      	rolq	$0x2b, %rdx
 59b4dd8:      	addq	%r10, %rdi
 59b4ddb:      	addq	%rsi, %rdi
 59b4dde:      	movq	%rdi, %r10
 59b4de1:      	rolq	$0x14, %r10
 59b4de5:      	addq	%rsi, %r10
 59b4de8:      	addq	%rdx, %r10
 59b4deb:      	addq	%rax, %rdi
 59b4dee:      	movq	%r10, %rsi
 59b4df1:      	movq	%rdi, %r11
 59b4df4:      	movq	%r14, %rax
 59b4df7:      	movq	%rcx, %r14
 59b4dfa:      	movq	%r8, %r15
 59b4dfd:      	movq	%rbx, %r8
 59b4e00:      	jmp	0x59b4e0c <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8LoadInstEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 59b4e02:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 59b4e0c:      	xorq	%r11, %r14
 59b4e0f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 59b4e19:      	imulq	%rcx, %r14
 59b4e1d:      	xorq	%r14, %r11
 59b4e20:      	shrq	$0x2f, %r14
 59b4e24:      	xorq	%r11, %r14
 59b4e27:      	imulq	%rcx, %r14
 59b4e2b:      	movq	%r14, %rdi
 59b4e2e:      	shrq	$0x2f, %rdi
 59b4e32:      	xorq	%r14, %rdi
 59b4e35:      	imulq	%rcx, %rdi
 59b4e39:      	movq	%r9, %rdx
 59b4e3c:      	shrq	$0x2f, %rdx
 59b4e40:      	xorq	%r9, %rdx
 59b4e43:      	imulq	%r13, %rdx
 59b4e47:      	addq	%r15, %rdx
 59b4e4a:      	addq	%rdi, %rdx
 59b4e4d:      	xorq	%rsi, %rax
 59b4e50:      	imulq	%rcx, %rax
 59b4e54:      	xorq	%rax, %rsi
 59b4e57:      	shrq	$0x2f, %rax
 59b4e5b:      	xorq	%rsi, %rax
 59b4e5e:      	imulq	%rcx, %rax
 59b4e62:      	movq	%rax, %rsi
 59b4e65:      	shrq	$0x2f, %rsi
 59b4e69:      	xorq	%rax, %rsi
 59b4e6c:      	imulq	%rcx, %rsi
 59b4e70:      	movq	%r12, %rax
 59b4e73:      	shrq	$0x2f, %rax
 59b4e77:      	xorq	%r12, %rax
 59b4e7a:      	imulq	%r13, %rax
 59b4e7e:      	addq	%r8, %rax
 59b4e81:      	addq	%rsi, %rax
 59b4e84:      	xorq	%rax, %rdx
 59b4e87:      	imulq	%rcx, %rdx
 59b4e8b:      	xorq	%rdx, %rax
 59b4e8e:      	shrq	$0x2f, %rdx
 59b4e92:      	xorq	%rax, %rdx
 59b4e95:      	imulq	%rcx, %rdx
 59b4e99:      	movq	%rdx, %rax
 59b4e9c:      	shrq	$0x2f, %rax
 59b4ea0:      	xorq	%rdx, %rax
 59b4ea3:      	imulq	%rcx, %rax
 59b4ea7:      	popq	%rbx
 59b4ea8:      	popq	%r12
 59b4eaa:      	popq	%r13
 59b4eac:      	popq	%r14
 59b4eae:      	popq	%r15
 59b4eb0:      	popq	%rbp
 59b4eb1:      	retq
