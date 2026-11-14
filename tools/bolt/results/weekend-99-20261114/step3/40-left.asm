
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003b479f0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3b479f0:      	movq	%rsi, %rcx
 3b479f3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3b479fd:      	subq	%rdi, %rsi
 3b47a00:      	cmpq	$0x40, %rsi
 3b47a04:      	ja	0x3b47a14 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3b47a06:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3b47a0c:      	movq	%rax, %rdx
 3b47a0f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3b47a14:      	pushq	%rbp
 3b47a15:      	pushq	%r15
 3b47a17:      	pushq	%r14
 3b47a19:      	pushq	%r13
 3b47a1b:      	pushq	%r12
 3b47a1d:      	pushq	%rbx
 3b47a1e:      	movq	%rcx, -0x18(%rsp)
 3b47a23:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3b47a2d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3b47a37:      	movq	%rsi, -0x10(%rsp)
 3b47a3c:      	movq	%rsi, %r14
 3b47a3f:      	andq	$-0x40, %r14
 3b47a43:      	movq	0x8(%rdi), %r13
 3b47a47:      	movq	0x10(%rdi), %rcx
 3b47a4b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3b47a55:      	addq	%r13, %rdx
 3b47a58:      	rolq	$0x1b, %rdx
 3b47a5c:      	imulq	%r9, %rdx
 3b47a60:      	movq	0x30(%rdi), %rsi
 3b47a64:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3b47a6e:      	addq	%rsi, %r10
 3b47a71:      	rolq	$0x16, %r10
 3b47a75:      	imulq	%r9, %r10
 3b47a79:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3b47a83:      	xorq	%rdx, %rbp
 3b47a86:      	movq	0x28(%rdi), %r12
 3b47a8a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3b47a94:      	addq	%r12, %r9
 3b47a97:      	addq	%r10, %r9
 3b47a9a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3b47aa4:      	addq	(%rdi), %r10
 3b47aa7:      	movq	0x18(%rdi), %r11
 3b47aab:      	addq	%r10, %rax
 3b47aae:      	addq	%r11, %rax
 3b47ab1:      	addq	%rbp, %rax
 3b47ab4:      	rolq	$0x2b, %rax
 3b47ab8:      	addq	%rcx, %r13
 3b47abb:      	addq	%r10, %r13
 3b47abe:      	movq	%r13, %rdx
 3b47ac1:      	rolq	$0x14, %rdx
 3b47ac5:      	addq	%r10, %rdx
 3b47ac8:      	addq	%rax, %rdx
 3b47acb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3b47ad5:      	addq	0x20(%rdi), %rax
 3b47ad9:      	addq	%r11, %r13
 3b47adc:      	movq	0x38(%rdi), %r10
 3b47ae0:      	addq	%rax, %rcx
 3b47ae3:      	addq	%r10, %rcx
 3b47ae6:      	addq	%r9, %rcx
 3b47ae9:      	rolq	$0x2b, %rcx
 3b47aed:      	addq	%rsi, %r12
 3b47af0:      	addq	%rax, %r12
 3b47af3:      	movq	%r12, %rbx
 3b47af6:      	rolq	$0x14, %rbx
 3b47afa:      	addq	%rax, %rbx
 3b47afd:      	addq	%rcx, %rbx
 3b47b00:      	addq	%r10, %r12
 3b47b03:      	movq	%r14, -0x20(%rsp)
 3b47b08:      	cmpq	$0x40, %r14
 3b47b0c:      	jne	0x3b47b22 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3b47b0e:      	movq	%rbx, %rsi
 3b47b11:      	movq	%r12, %r11
 3b47b14:      	movq	%rdx, %rax
 3b47b17:      	movq	%r13, %r14
 3b47b1a:      	movq	%rbp, %r15
 3b47b1d:      	jmp	0x3b47c0d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3b47b22:      	addq	$-0x40, -0x20(%rsp)
 3b47b28:      	xorl	%ecx, %ecx
 3b47b2a:      	nopw	(%rax,%rax)
 3b47b30:      	addq	%r9, %r8
 3b47b33:      	addq	%r13, %r8
 3b47b36:      	movq	0x48(%rdi,%rcx), %r14
 3b47b3b:      	movq	0x50(%rdi,%rcx), %r10
 3b47b40:      	addq	%r14, %r8
 3b47b43:      	rolq	$0x1b, %r8
 3b47b47:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3b47b51:      	imulq	%rsi, %r8
 3b47b55:      	addq	%rdx, %r9
 3b47b58:      	movq	0x70(%rdi,%rcx), %rax
 3b47b5d:      	movq	%rax, -0x8(%rsp)
 3b47b62:      	addq	%rax, %r9
 3b47b65:      	rolq	$0x16, %r9
 3b47b69:      	imulq	%rsi, %r9
 3b47b6d:      	movq	%r8, %r15
 3b47b70:      	xorq	%rbx, %r15
 3b47b73:      	movq	0x68(%rdi,%rcx), %r11
 3b47b78:      	addq	%r11, %r13
 3b47b7b:      	addq	%r12, %rbp
 3b47b7e:      	rolq	$0x1f, %rbp
 3b47b82:      	addq	%r13, %r9
 3b47b85:      	imulq	%rsi, %rdx
 3b47b89:      	addq	0x40(%rdi,%rcx), %rdx
 3b47b8e:      	movq	%rbp, %r8
 3b47b91:      	movq	0x58(%rdi,%rcx), %r13
 3b47b96:      	addq	%rdx, %r12
 3b47b99:      	addq	%r13, %r12
 3b47b9c:      	addq	%r15, %r12
 3b47b9f:      	rolq	$0x2b, %r12
 3b47ba3:      	addq	%r10, %r14
 3b47ba6:      	addq	%rdx, %r14
 3b47ba9:      	movq	%r14, %rax
 3b47bac:      	rolq	$0x14, %rax
 3b47bb0:      	imulq	%rsi, %r8
 3b47bb4:      	addq	%rdx, %rax
 3b47bb7:      	addq	%r12, %rax
 3b47bba:      	addq	%r8, %rbx
 3b47bbd:      	addq	%r9, %r10
 3b47bc0:      	addq	0x60(%rdi,%rcx), %rbx
 3b47bc5:      	movq	0x78(%rdi,%rcx), %rdx
 3b47bca:      	addq	%rbx, %r10
 3b47bcd:      	addq	%rdx, %r10
 3b47bd0:      	rolq	$0x2b, %r10
 3b47bd4:      	addq	%r13, %r14
 3b47bd7:      	addq	-0x8(%rsp), %r11
 3b47bdc:      	addq	%rbx, %r11
 3b47bdf:      	movq	%r11, %rsi
 3b47be2:      	rolq	$0x14, %rsi
 3b47be6:      	addq	%rbx, %rsi
 3b47be9:      	addq	%r10, %rsi
 3b47bec:      	addq	%rdx, %r11
 3b47bef:      	addq	$0x40, %rcx
 3b47bf3:      	movq	%r15, %rbp
 3b47bf6:      	movq	%r14, %r13
 3b47bf9:      	movq	%rax, %rdx
 3b47bfc:      	movq	%r11, %r12
 3b47bff:      	movq	%rsi, %rbx
 3b47c02:      	cmpq	%rcx, -0x20(%rsp)
 3b47c07:      	jne	0x3b47b30 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3b47c0d:      	movq	-0x10(%rsp), %r12
 3b47c12:      	testb	$0x3f, %r12b
 3b47c16:      	je	0x3b47ce3 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 3b47c1c:      	leaq	(%r9,%r14), %rdi
 3b47c20:      	movq	-0x18(%rsp), %rbp
 3b47c25:      	movq	-0x38(%rbp), %rcx
 3b47c29:      	movq	-0x30(%rbp), %rdx
 3b47c2d:      	addq	%rcx, %r8
 3b47c30:      	addq	%rdi, %r8
 3b47c33:      	rolq	$0x1b, %r8
 3b47c37:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3b47c41:      	imulq	%r13, %r8
 3b47c45:      	addq	%rax, %r9
 3b47c48:      	movq	-0x10(%rbp), %r10
 3b47c4c:      	addq	%r10, %r9
 3b47c4f:      	rolq	$0x16, %r9
 3b47c53:      	imulq	%r13, %r9
 3b47c57:      	xorq	%rsi, %r8
 3b47c5a:      	movq	-0x18(%rbp), %rdi
 3b47c5e:      	addq	%rdi, %r14
 3b47c61:      	addq	%r14, %r9
 3b47c64:      	addq	%r11, %r15
 3b47c67:      	rolq	$0x1f, %r15
 3b47c6b:      	movq	%r15, %rbx
 3b47c6e:      	imulq	%r13, %rax
 3b47c72:      	addq	%r8, %r11
 3b47c75:      	addq	-0x40(%rbp), %rax
 3b47c79:      	movq	-0x28(%rbp), %r15
 3b47c7d:      	addq	%r15, %r11
 3b47c80:      	addq	%rax, %r11
 3b47c83:      	rolq	$0x2b, %r11
 3b47c87:      	imulq	%r13, %rbx
 3b47c8b:      	addq	%rdx, %rcx
 3b47c8e:      	addq	%rax, %rcx
 3b47c91:      	movq	%rcx, %r14
 3b47c94:      	rolq	$0x14, %r14
 3b47c98:      	addq	%rax, %r14
 3b47c9b:      	addq	%r11, %r14
 3b47c9e:      	addq	%r15, %rcx
 3b47ca1:      	addq	%rbx, %rsi
 3b47ca4:      	addq	-0x20(%rbp), %rsi
 3b47ca8:      	addq	%r9, %rdx
 3b47cab:      	movq	-0x8(%rbp), %rax
 3b47caf:      	addq	%rax, %rdx
 3b47cb2:      	addq	%rsi, %rdx
 3b47cb5:      	rolq	$0x2b, %rdx
 3b47cb9:      	addq	%r10, %rdi
 3b47cbc:      	addq	%rsi, %rdi
 3b47cbf:      	movq	%rdi, %r10
 3b47cc2:      	rolq	$0x14, %r10
 3b47cc6:      	addq	%rsi, %r10
 3b47cc9:      	addq	%rdx, %r10
 3b47ccc:      	addq	%rax, %rdi
 3b47ccf:      	movq	%r10, %rsi
 3b47cd2:      	movq	%rdi, %r11
 3b47cd5:      	movq	%r14, %rax
 3b47cd8:      	movq	%rcx, %r14
 3b47cdb:      	movq	%r8, %r15
 3b47cde:      	movq	%rbx, %r8
 3b47ce1:      	jmp	0x3b47ced <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 3b47ce3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3b47ced:      	xorq	%r11, %r14
 3b47cf0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3b47cfa:      	imulq	%rcx, %r14
 3b47cfe:      	xorq	%r14, %r11
 3b47d01:      	shrq	$0x2f, %r14
 3b47d05:      	xorq	%r11, %r14
 3b47d08:      	imulq	%rcx, %r14
 3b47d0c:      	movq	%r14, %rdi
 3b47d0f:      	shrq	$0x2f, %rdi
 3b47d13:      	xorq	%r14, %rdi
 3b47d16:      	imulq	%rcx, %rdi
 3b47d1a:      	movq	%r9, %rdx
 3b47d1d:      	shrq	$0x2f, %rdx
 3b47d21:      	xorq	%r9, %rdx
 3b47d24:      	imulq	%r13, %rdx
 3b47d28:      	addq	%r15, %rdx
 3b47d2b:      	addq	%rdi, %rdx
 3b47d2e:      	xorq	%rsi, %rax
 3b47d31:      	imulq	%rcx, %rax
 3b47d35:      	xorq	%rax, %rsi
 3b47d38:      	shrq	$0x2f, %rax
 3b47d3c:      	xorq	%rsi, %rax
 3b47d3f:      	imulq	%rcx, %rax
 3b47d43:      	movq	%rax, %rsi
 3b47d46:      	shrq	$0x2f, %rsi
 3b47d4a:      	xorq	%rax, %rsi
 3b47d4d:      	imulq	%rcx, %rsi
 3b47d51:      	movq	%r12, %rax
 3b47d54:      	shrq	$0x2f, %rax
 3b47d58:      	xorq	%r12, %rax
 3b47d5b:      	imulq	%r13, %rax
 3b47d5f:      	addq	%r8, %rax
 3b47d62:      	addq	%rsi, %rax
 3b47d65:      	xorq	%rax, %rdx
 3b47d68:      	imulq	%rcx, %rdx
 3b47d6c:      	xorq	%rdx, %rax
 3b47d6f:      	shrq	$0x2f, %rdx
 3b47d73:      	xorq	%rax, %rdx
 3b47d76:      	imulq	%rcx, %rdx
 3b47d7a:      	movq	%rdx, %rax
 3b47d7d:      	shrq	$0x2f, %rax
 3b47d81:      	xorq	%rdx, %rax
 3b47d84:      	imulq	%rcx, %rax
 3b47d88:      	popq	%rbx
 3b47d89:      	popq	%r12
 3b47d8b:      	popq	%r13
 3b47d8d:      	popq	%r14
 3b47d8f:      	popq	%r15
 3b47d91:      	popq	%rbp
 3b47d92:      	retq
