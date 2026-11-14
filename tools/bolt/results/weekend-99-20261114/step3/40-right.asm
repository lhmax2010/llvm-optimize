
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003b47960 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3b47960:      	movq	%rsi, %rcx
 3b47963:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3b4796d:      	subq	%rdi, %rsi
 3b47970:      	cmpq	$0x40, %rsi
 3b47974:      	ja	0x3b47984 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3b47976:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3b4797c:      	movq	%rax, %rdx
 3b4797f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3b47984:      	pushq	%rbp
 3b47985:      	pushq	%r15
 3b47987:      	pushq	%r14
 3b47989:      	pushq	%r13
 3b4798b:      	pushq	%r12
 3b4798d:      	pushq	%rbx
 3b4798e:      	movq	%rcx, -0x18(%rsp)
 3b47993:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3b4799d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3b479a7:      	movq	%rsi, -0x10(%rsp)
 3b479ac:      	movq	%rsi, %r14
 3b479af:      	andq	$-0x40, %r14
 3b479b3:      	movq	0x8(%rdi), %r13
 3b479b7:      	movq	0x10(%rdi), %rcx
 3b479bb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3b479c5:      	addq	%r13, %rdx
 3b479c8:      	rolq	$0x1b, %rdx
 3b479cc:      	imulq	%r9, %rdx
 3b479d0:      	movq	0x30(%rdi), %rsi
 3b479d4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3b479de:      	addq	%rsi, %r10
 3b479e1:      	rolq	$0x16, %r10
 3b479e5:      	imulq	%r9, %r10
 3b479e9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3b479f3:      	xorq	%rdx, %rbp
 3b479f6:      	movq	0x28(%rdi), %r12
 3b479fa:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3b47a04:      	addq	%r12, %r9
 3b47a07:      	addq	%r10, %r9
 3b47a0a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3b47a14:      	addq	(%rdi), %r10
 3b47a17:      	movq	0x18(%rdi), %r11
 3b47a1b:      	addq	%r10, %rax
 3b47a1e:      	addq	%r11, %rax
 3b47a21:      	addq	%rbp, %rax
 3b47a24:      	rolq	$0x2b, %rax
 3b47a28:      	addq	%rcx, %r13
 3b47a2b:      	addq	%r10, %r13
 3b47a2e:      	movq	%r13, %rdx
 3b47a31:      	rolq	$0x14, %rdx
 3b47a35:      	addq	%r10, %rdx
 3b47a38:      	addq	%rax, %rdx
 3b47a3b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3b47a45:      	addq	0x20(%rdi), %rax
 3b47a49:      	addq	%r11, %r13
 3b47a4c:      	movq	0x38(%rdi), %r10
 3b47a50:      	addq	%rax, %rcx
 3b47a53:      	addq	%r10, %rcx
 3b47a56:      	addq	%r9, %rcx
 3b47a59:      	rolq	$0x2b, %rcx
 3b47a5d:      	addq	%rsi, %r12
 3b47a60:      	addq	%rax, %r12
 3b47a63:      	movq	%r12, %rbx
 3b47a66:      	rolq	$0x14, %rbx
 3b47a6a:      	addq	%rax, %rbx
 3b47a6d:      	addq	%rcx, %rbx
 3b47a70:      	addq	%r10, %r12
 3b47a73:      	movq	%r14, -0x20(%rsp)
 3b47a78:      	cmpq	$0x40, %r14
 3b47a7c:      	jne	0x3b47a92 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3b47a7e:      	movq	%rbx, %rsi
 3b47a81:      	movq	%r12, %r11
 3b47a84:      	movq	%rdx, %rax
 3b47a87:      	movq	%r13, %r14
 3b47a8a:      	movq	%rbp, %r15
 3b47a8d:      	jmp	0x3b47b7d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3b47a92:      	addq	$-0x40, -0x20(%rsp)
 3b47a98:      	xorl	%ecx, %ecx
 3b47a9a:      	nopw	(%rax,%rax)
 3b47aa0:      	addq	%r9, %r8
 3b47aa3:      	addq	%r13, %r8
 3b47aa6:      	movq	0x48(%rdi,%rcx), %r14
 3b47aab:      	movq	0x50(%rdi,%rcx), %r10
 3b47ab0:      	addq	%r14, %r8
 3b47ab3:      	rolq	$0x1b, %r8
 3b47ab7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3b47ac1:      	imulq	%rsi, %r8
 3b47ac5:      	addq	%rdx, %r9
 3b47ac8:      	movq	0x70(%rdi,%rcx), %rax
 3b47acd:      	movq	%rax, -0x8(%rsp)
 3b47ad2:      	addq	%rax, %r9
 3b47ad5:      	rolq	$0x16, %r9
 3b47ad9:      	imulq	%rsi, %r9
 3b47add:      	movq	%r8, %r15
 3b47ae0:      	xorq	%rbx, %r15
 3b47ae3:      	movq	0x68(%rdi,%rcx), %r11
 3b47ae8:      	addq	%r11, %r13
 3b47aeb:      	addq	%r12, %rbp
 3b47aee:      	rolq	$0x1f, %rbp
 3b47af2:      	addq	%r13, %r9
 3b47af5:      	imulq	%rsi, %rdx
 3b47af9:      	addq	0x40(%rdi,%rcx), %rdx
 3b47afe:      	movq	%rbp, %r8
 3b47b01:      	movq	0x58(%rdi,%rcx), %r13
 3b47b06:      	addq	%rdx, %r12
 3b47b09:      	addq	%r13, %r12
 3b47b0c:      	addq	%r15, %r12
 3b47b0f:      	rolq	$0x2b, %r12
 3b47b13:      	addq	%r10, %r14
 3b47b16:      	addq	%rdx, %r14
 3b47b19:      	movq	%r14, %rax
 3b47b1c:      	rolq	$0x14, %rax
 3b47b20:      	imulq	%rsi, %r8
 3b47b24:      	addq	%rdx, %rax
 3b47b27:      	addq	%r12, %rax
 3b47b2a:      	addq	%r8, %rbx
 3b47b2d:      	addq	%r9, %r10
 3b47b30:      	addq	0x60(%rdi,%rcx), %rbx
 3b47b35:      	movq	0x78(%rdi,%rcx), %rdx
 3b47b3a:      	addq	%rbx, %r10
 3b47b3d:      	addq	%rdx, %r10
 3b47b40:      	rolq	$0x2b, %r10
 3b47b44:      	addq	%r13, %r14
 3b47b47:      	addq	-0x8(%rsp), %r11
 3b47b4c:      	addq	%rbx, %r11
 3b47b4f:      	movq	%r11, %rsi
 3b47b52:      	rolq	$0x14, %rsi
 3b47b56:      	addq	%rbx, %rsi
 3b47b59:      	addq	%r10, %rsi
 3b47b5c:      	addq	%rdx, %r11
 3b47b5f:      	addq	$0x40, %rcx
 3b47b63:      	movq	%r15, %rbp
 3b47b66:      	movq	%r14, %r13
 3b47b69:      	movq	%rax, %rdx
 3b47b6c:      	movq	%r11, %r12
 3b47b6f:      	movq	%rsi, %rbx
 3b47b72:      	cmpq	%rcx, -0x20(%rsp)
 3b47b77:      	jne	0x3b47aa0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3b47b7d:      	movq	-0x10(%rsp), %r12
 3b47b82:      	testb	$0x3f, %r12b
 3b47b86:      	je	0x3b47c52 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 3b47b8c:      	movq	-0x18(%rsp), %rbp
 3b47b91:      	movq	-0x38(%rbp), %rcx
 3b47b95:      	movq	-0x30(%rbp), %rdx
 3b47b99:      	addq	%rcx, %r8
 3b47b9c:      	addq	%r9, %r8
 3b47b9f:      	addq	%r14, %r8
 3b47ba2:      	rolq	$0x1b, %r8
 3b47ba6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3b47bb0:      	imulq	%r13, %r8
 3b47bb4:      	addq	%rax, %r9
 3b47bb7:      	movq	-0x10(%rbp), %r10
 3b47bbb:      	addq	%r10, %r9
 3b47bbe:      	rolq	$0x16, %r9
 3b47bc2:      	imulq	%r13, %r9
 3b47bc6:      	xorq	%rsi, %r8
 3b47bc9:      	movq	-0x18(%rbp), %rdi
 3b47bcd:      	addq	%rdi, %r14
 3b47bd0:      	addq	%r14, %r9
 3b47bd3:      	addq	%r11, %r15
 3b47bd6:      	rolq	$0x1f, %r15
 3b47bda:      	movq	%r15, %rbx
 3b47bdd:      	imulq	%r13, %rax
 3b47be1:      	addq	%r8, %r11
 3b47be4:      	addq	-0x40(%rbp), %rax
 3b47be8:      	movq	-0x28(%rbp), %r15
 3b47bec:      	addq	%r15, %r11
 3b47bef:      	addq	%rax, %r11
 3b47bf2:      	rolq	$0x2b, %r11
 3b47bf6:      	imulq	%r13, %rbx
 3b47bfa:      	addq	%rdx, %rcx
 3b47bfd:      	addq	%rax, %rcx
 3b47c00:      	movq	%rcx, %r14
 3b47c03:      	rolq	$0x14, %r14
 3b47c07:      	addq	%rax, %r14
 3b47c0a:      	addq	%r11, %r14
 3b47c0d:      	addq	%r15, %rcx
 3b47c10:      	addq	%rbx, %rsi
 3b47c13:      	addq	-0x20(%rbp), %rsi
 3b47c17:      	addq	%r9, %rdx
 3b47c1a:      	movq	-0x8(%rbp), %rax
 3b47c1e:      	addq	%rax, %rdx
 3b47c21:      	addq	%rsi, %rdx
 3b47c24:      	rolq	$0x2b, %rdx
 3b47c28:      	addq	%r10, %rdi
 3b47c2b:      	addq	%rsi, %rdi
 3b47c2e:      	movq	%rdi, %r10
 3b47c31:      	rolq	$0x14, %r10
 3b47c35:      	addq	%rsi, %r10
 3b47c38:      	addq	%rdx, %r10
 3b47c3b:      	addq	%rax, %rdi
 3b47c3e:      	movq	%r10, %rsi
 3b47c41:      	movq	%rdi, %r11
 3b47c44:      	movq	%r14, %rax
 3b47c47:      	movq	%rcx, %r14
 3b47c4a:      	movq	%r8, %r15
 3b47c4d:      	movq	%rbx, %r8
 3b47c50:      	jmp	0x3b47c5c <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_15ValueAsMetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 3b47c52:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3b47c5c:      	xorq	%r11, %r14
 3b47c5f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3b47c69:      	imulq	%rcx, %r14
 3b47c6d:      	xorq	%r14, %r11
 3b47c70:      	shrq	$0x2f, %r14
 3b47c74:      	xorq	%r11, %r14
 3b47c77:      	imulq	%rcx, %r14
 3b47c7b:      	movq	%r14, %rdi
 3b47c7e:      	shrq	$0x2f, %rdi
 3b47c82:      	xorq	%r14, %rdi
 3b47c85:      	imulq	%rcx, %rdi
 3b47c89:      	movq	%r9, %rdx
 3b47c8c:      	shrq	$0x2f, %rdx
 3b47c90:      	xorq	%r9, %rdx
 3b47c93:      	imulq	%r13, %rdx
 3b47c97:      	addq	%r15, %rdx
 3b47c9a:      	addq	%rdi, %rdx
 3b47c9d:      	xorq	%rsi, %rax
 3b47ca0:      	imulq	%rcx, %rax
 3b47ca4:      	xorq	%rax, %rsi
 3b47ca7:      	shrq	$0x2f, %rax
 3b47cab:      	xorq	%rsi, %rax
 3b47cae:      	imulq	%rcx, %rax
 3b47cb2:      	movq	%rax, %rsi
 3b47cb5:      	shrq	$0x2f, %rsi
 3b47cb9:      	xorq	%rax, %rsi
 3b47cbc:      	imulq	%rcx, %rsi
 3b47cc0:      	movq	%r12, %rax
 3b47cc3:      	shrq	$0x2f, %rax
 3b47cc7:      	xorq	%r12, %rax
 3b47cca:      	imulq	%r13, %rax
 3b47cce:      	addq	%r8, %rax
 3b47cd1:      	addq	%rsi, %rax
 3b47cd4:      	xorq	%rax, %rdx
 3b47cd7:      	imulq	%rcx, %rdx
 3b47cdb:      	xorq	%rdx, %rax
 3b47cde:      	shrq	$0x2f, %rdx
 3b47ce2:      	xorq	%rax, %rdx
 3b47ce5:      	imulq	%rcx, %rdx
 3b47ce9:      	movq	%rdx, %rax
 3b47cec:      	shrq	$0x2f, %rax
 3b47cf0:      	xorq	%rdx, %rax
 3b47cf3:      	imulq	%rcx, %rax
 3b47cf7:      	popq	%rbx
 3b47cf8:      	popq	%r12
 3b47cfa:      	popq	%r13
 3b47cfc:      	popq	%r14
 3b47cfe:      	popq	%r15
 3b47d00:      	popq	%rbp
 3b47d01:      	retq
