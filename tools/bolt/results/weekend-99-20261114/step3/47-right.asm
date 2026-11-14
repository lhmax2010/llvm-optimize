
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000036848e0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 36848e0:      	movq	%rsi, %rcx
 36848e3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 36848ed:      	subq	%rdi, %rsi
 36848f0:      	cmpq	$0x40, %rsi
 36848f4:      	ja	0x3684904 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 36848f6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 36848fc:      	movq	%rax, %rdx
 36848ff:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3684904:      	pushq	%rbp
 3684905:      	pushq	%r15
 3684907:      	pushq	%r14
 3684909:      	pushq	%r13
 368490b:      	pushq	%r12
 368490d:      	pushq	%rbx
 368490e:      	movq	%rcx, -0x18(%rsp)
 3684913:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 368491d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3684927:      	movq	%rsi, -0x10(%rsp)
 368492c:      	movq	%rsi, %r14
 368492f:      	andq	$-0x40, %r14
 3684933:      	movq	0x8(%rdi), %r13
 3684937:      	movq	0x10(%rdi), %rcx
 368493b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3684945:      	addq	%r13, %rdx
 3684948:      	rolq	$0x1b, %rdx
 368494c:      	imulq	%r9, %rdx
 3684950:      	movq	0x30(%rdi), %rsi
 3684954:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 368495e:      	addq	%rsi, %r10
 3684961:      	rolq	$0x16, %r10
 3684965:      	imulq	%r9, %r10
 3684969:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3684973:      	xorq	%rdx, %rbp
 3684976:      	movq	0x28(%rdi), %r12
 368497a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3684984:      	addq	%r12, %r9
 3684987:      	addq	%r10, %r9
 368498a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3684994:      	addq	(%rdi), %r10
 3684997:      	movq	0x18(%rdi), %r11
 368499b:      	addq	%r10, %rax
 368499e:      	addq	%r11, %rax
 36849a1:      	addq	%rbp, %rax
 36849a4:      	rolq	$0x2b, %rax
 36849a8:      	addq	%rcx, %r13
 36849ab:      	addq	%r10, %r13
 36849ae:      	movq	%r13, %rdx
 36849b1:      	rolq	$0x14, %rdx
 36849b5:      	addq	%r10, %rdx
 36849b8:      	addq	%rax, %rdx
 36849bb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 36849c5:      	addq	0x20(%rdi), %rax
 36849c9:      	addq	%r11, %r13
 36849cc:      	movq	0x38(%rdi), %r10
 36849d0:      	addq	%rax, %rcx
 36849d3:      	addq	%r10, %rcx
 36849d6:      	addq	%r9, %rcx
 36849d9:      	rolq	$0x2b, %rcx
 36849dd:      	addq	%rsi, %r12
 36849e0:      	addq	%rax, %r12
 36849e3:      	movq	%r12, %rbx
 36849e6:      	rolq	$0x14, %rbx
 36849ea:      	addq	%rax, %rbx
 36849ed:      	addq	%rcx, %rbx
 36849f0:      	addq	%r10, %r12
 36849f3:      	movq	%r14, -0x20(%rsp)
 36849f8:      	cmpq	$0x40, %r14
 36849fc:      	jne	0x3684a12 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 36849fe:      	movq	%rbx, %rsi
 3684a01:      	movq	%r12, %r11
 3684a04:      	movq	%rdx, %rax
 3684a07:      	movq	%r13, %r14
 3684a0a:      	movq	%rbp, %r15
 3684a0d:      	jmp	0x3684afd <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 3684a12:      	addq	$-0x40, -0x20(%rsp)
 3684a18:      	xorl	%ecx, %ecx
 3684a1a:      	nopw	(%rax,%rax)
 3684a20:      	addq	%r9, %r8
 3684a23:      	addq	%r13, %r8
 3684a26:      	movq	0x48(%rdi,%rcx), %r14
 3684a2b:      	movq	0x50(%rdi,%rcx), %r10
 3684a30:      	addq	%r14, %r8
 3684a33:      	rolq	$0x1b, %r8
 3684a37:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3684a41:      	imulq	%rsi, %r8
 3684a45:      	addq	%rdx, %r9
 3684a48:      	movq	0x70(%rdi,%rcx), %rax
 3684a4d:      	movq	%rax, -0x8(%rsp)
 3684a52:      	addq	%rax, %r9
 3684a55:      	rolq	$0x16, %r9
 3684a59:      	imulq	%rsi, %r9
 3684a5d:      	movq	%r8, %r15
 3684a60:      	xorq	%rbx, %r15
 3684a63:      	movq	0x68(%rdi,%rcx), %r11
 3684a68:      	addq	%r11, %r13
 3684a6b:      	addq	%r12, %rbp
 3684a6e:      	rolq	$0x1f, %rbp
 3684a72:      	addq	%r13, %r9
 3684a75:      	imulq	%rsi, %rdx
 3684a79:      	addq	0x40(%rdi,%rcx), %rdx
 3684a7e:      	movq	%rbp, %r8
 3684a81:      	movq	0x58(%rdi,%rcx), %r13
 3684a86:      	addq	%rdx, %r12
 3684a89:      	addq	%r13, %r12
 3684a8c:      	addq	%r15, %r12
 3684a8f:      	rolq	$0x2b, %r12
 3684a93:      	addq	%r10, %r14
 3684a96:      	addq	%rdx, %r14
 3684a99:      	movq	%r14, %rax
 3684a9c:      	rolq	$0x14, %rax
 3684aa0:      	imulq	%rsi, %r8
 3684aa4:      	addq	%rdx, %rax
 3684aa7:      	addq	%r12, %rax
 3684aaa:      	addq	%r8, %rbx
 3684aad:      	addq	%r9, %r10
 3684ab0:      	addq	0x60(%rdi,%rcx), %rbx
 3684ab5:      	movq	0x78(%rdi,%rcx), %rdx
 3684aba:      	addq	%rbx, %r10
 3684abd:      	addq	%rdx, %r10
 3684ac0:      	rolq	$0x2b, %r10
 3684ac4:      	addq	%r13, %r14
 3684ac7:      	addq	-0x8(%rsp), %r11
 3684acc:      	addq	%rbx, %r11
 3684acf:      	movq	%r11, %rsi
 3684ad2:      	rolq	$0x14, %rsi
 3684ad6:      	addq	%rbx, %rsi
 3684ad9:      	addq	%r10, %rsi
 3684adc:      	addq	%rdx, %r11
 3684adf:      	addq	$0x40, %rcx
 3684ae3:      	movq	%r15, %rbp
 3684ae6:      	movq	%r14, %r13
 3684ae9:      	movq	%rax, %rdx
 3684aec:      	movq	%r11, %r12
 3684aef:      	movq	%rsi, %rbx
 3684af2:      	cmpq	%rcx, -0x20(%rsp)
 3684af7:      	jne	0x3684a20 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 3684afd:      	movq	-0x10(%rsp), %r12
 3684b02:      	testb	$0x3f, %r12b
 3684b06:      	je	0x3684bd2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f2>
 3684b0c:      	movq	-0x18(%rsp), %rbp
 3684b11:      	movq	-0x38(%rbp), %rcx
 3684b15:      	movq	-0x30(%rbp), %rdx
 3684b19:      	addq	%rcx, %r8
 3684b1c:      	addq	%r9, %r8
 3684b1f:      	addq	%r14, %r8
 3684b22:      	rolq	$0x1b, %r8
 3684b26:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3684b30:      	imulq	%r13, %r8
 3684b34:      	addq	%rax, %r9
 3684b37:      	movq	-0x10(%rbp), %r10
 3684b3b:      	addq	%r10, %r9
 3684b3e:      	rolq	$0x16, %r9
 3684b42:      	imulq	%r13, %r9
 3684b46:      	xorq	%rsi, %r8
 3684b49:      	movq	-0x18(%rbp), %rdi
 3684b4d:      	addq	%rdi, %r14
 3684b50:      	addq	%r14, %r9
 3684b53:      	addq	%r11, %r15
 3684b56:      	rolq	$0x1f, %r15
 3684b5a:      	movq	%r15, %rbx
 3684b5d:      	imulq	%r13, %rax
 3684b61:      	addq	%r8, %r11
 3684b64:      	addq	-0x40(%rbp), %rax
 3684b68:      	movq	-0x28(%rbp), %r15
 3684b6c:      	addq	%r15, %r11
 3684b6f:      	addq	%rax, %r11
 3684b72:      	rolq	$0x2b, %r11
 3684b76:      	imulq	%r13, %rbx
 3684b7a:      	addq	%rdx, %rcx
 3684b7d:      	addq	%rax, %rcx
 3684b80:      	movq	%rcx, %r14
 3684b83:      	rolq	$0x14, %r14
 3684b87:      	addq	%rax, %r14
 3684b8a:      	addq	%r11, %r14
 3684b8d:      	addq	%r15, %rcx
 3684b90:      	addq	%rbx, %rsi
 3684b93:      	addq	-0x20(%rbp), %rsi
 3684b97:      	addq	%r9, %rdx
 3684b9a:      	movq	-0x8(%rbp), %rax
 3684b9e:      	addq	%rax, %rdx
 3684ba1:      	addq	%rsi, %rdx
 3684ba4:      	rolq	$0x2b, %rdx
 3684ba8:      	addq	%r10, %rdi
 3684bab:      	addq	%rsi, %rdi
 3684bae:      	movq	%rdi, %r10
 3684bb1:      	rolq	$0x14, %r10
 3684bb5:      	addq	%rsi, %r10
 3684bb8:      	addq	%rdx, %r10
 3684bbb:      	addq	%rax, %rdi
 3684bbe:      	movq	%r10, %rsi
 3684bc1:      	movq	%rdi, %r11
 3684bc4:      	movq	%r14, %rax
 3684bc7:      	movq	%rcx, %r14
 3684bca:      	movq	%r8, %r15
 3684bcd:      	movq	%rbx, %r8
 3684bd0:      	jmp	0x3684bdc <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fc>
 3684bd2:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3684bdc:      	xorq	%r11, %r14
 3684bdf:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3684be9:      	imulq	%rcx, %r14
 3684bed:      	xorq	%r14, %r11
 3684bf0:      	shrq	$0x2f, %r14
 3684bf4:      	xorq	%r11, %r14
 3684bf7:      	imulq	%rcx, %r14
 3684bfb:      	movq	%r14, %rdi
 3684bfe:      	shrq	$0x2f, %rdi
 3684c02:      	xorq	%r14, %rdi
 3684c05:      	imulq	%rcx, %rdi
 3684c09:      	movq	%r9, %rdx
 3684c0c:      	shrq	$0x2f, %rdx
 3684c10:      	xorq	%r9, %rdx
 3684c13:      	imulq	%r13, %rdx
 3684c17:      	addq	%r15, %rdx
 3684c1a:      	addq	%rdi, %rdx
 3684c1d:      	xorq	%rsi, %rax
 3684c20:      	imulq	%rcx, %rax
 3684c24:      	xorq	%rax, %rsi
 3684c27:      	shrq	$0x2f, %rax
 3684c2b:      	xorq	%rsi, %rax
 3684c2e:      	imulq	%rcx, %rax
 3684c32:      	movq	%rax, %rsi
 3684c35:      	shrq	$0x2f, %rsi
 3684c39:      	xorq	%rax, %rsi
 3684c3c:      	imulq	%rcx, %rsi
 3684c40:      	movq	%r12, %rax
 3684c43:      	shrq	$0x2f, %rax
 3684c47:      	xorq	%r12, %rax
 3684c4a:      	imulq	%r13, %rax
 3684c4e:      	addq	%r8, %rax
 3684c51:      	addq	%rsi, %rax
 3684c54:      	xorq	%rax, %rdx
 3684c57:      	imulq	%rcx, %rdx
 3684c5b:      	xorq	%rdx, %rax
 3684c5e:      	shrq	$0x2f, %rdx
 3684c62:      	xorq	%rax, %rdx
 3684c65:      	imulq	%rcx, %rdx
 3684c69:      	movq	%rdx, %rax
 3684c6c:      	shrq	$0x2f, %rax
 3684c70:      	xorq	%rdx, %rax
 3684c73:      	imulq	%rcx, %rax
 3684c77:      	popq	%rbx
 3684c78:      	popq	%r12
 3684c7a:      	popq	%r13
 3684c7c:      	popq	%r14
 3684c7e:      	popq	%r15
 3684c80:      	popq	%rbp
 3684c81:      	retq
