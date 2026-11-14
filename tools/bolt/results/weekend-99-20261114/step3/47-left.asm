
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003684970 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 3684970:      	movq	%rsi, %rcx
 3684973:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 368497d:      	subq	%rdi, %rsi
 3684980:      	cmpq	$0x40, %rsi
 3684984:      	ja	0x3684994 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 3684986:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 368498c:      	movq	%rax, %rdx
 368498f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3684994:      	pushq	%rbp
 3684995:      	pushq	%r15
 3684997:      	pushq	%r14
 3684999:      	pushq	%r13
 368499b:      	pushq	%r12
 368499d:      	pushq	%rbx
 368499e:      	movq	%rcx, -0x18(%rsp)
 36849a3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 36849ad:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 36849b7:      	movq	%rsi, -0x10(%rsp)
 36849bc:      	movq	%rsi, %r14
 36849bf:      	andq	$-0x40, %r14
 36849c3:      	movq	0x8(%rdi), %r13
 36849c7:      	movq	0x10(%rdi), %rcx
 36849cb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 36849d5:      	addq	%r13, %rdx
 36849d8:      	rolq	$0x1b, %rdx
 36849dc:      	imulq	%r9, %rdx
 36849e0:      	movq	0x30(%rdi), %rsi
 36849e4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 36849ee:      	addq	%rsi, %r10
 36849f1:      	rolq	$0x16, %r10
 36849f5:      	imulq	%r9, %r10
 36849f9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3684a03:      	xorq	%rdx, %rbp
 3684a06:      	movq	0x28(%rdi), %r12
 3684a0a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3684a14:      	addq	%r12, %r9
 3684a17:      	addq	%r10, %r9
 3684a1a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3684a24:      	addq	(%rdi), %r10
 3684a27:      	movq	0x18(%rdi), %r11
 3684a2b:      	addq	%r10, %rax
 3684a2e:      	addq	%r11, %rax
 3684a31:      	addq	%rbp, %rax
 3684a34:      	rolq	$0x2b, %rax
 3684a38:      	addq	%rcx, %r13
 3684a3b:      	addq	%r10, %r13
 3684a3e:      	movq	%r13, %rdx
 3684a41:      	rolq	$0x14, %rdx
 3684a45:      	addq	%r10, %rdx
 3684a48:      	addq	%rax, %rdx
 3684a4b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3684a55:      	addq	0x20(%rdi), %rax
 3684a59:      	addq	%r11, %r13
 3684a5c:      	movq	0x38(%rdi), %r10
 3684a60:      	addq	%rax, %rcx
 3684a63:      	addq	%r10, %rcx
 3684a66:      	addq	%r9, %rcx
 3684a69:      	rolq	$0x2b, %rcx
 3684a6d:      	addq	%rsi, %r12
 3684a70:      	addq	%rax, %r12
 3684a73:      	movq	%r12, %rbx
 3684a76:      	rolq	$0x14, %rbx
 3684a7a:      	addq	%rax, %rbx
 3684a7d:      	addq	%rcx, %rbx
 3684a80:      	addq	%r10, %r12
 3684a83:      	movq	%r14, -0x20(%rsp)
 3684a88:      	cmpq	$0x40, %r14
 3684a8c:      	jne	0x3684aa2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 3684a8e:      	movq	%rbx, %rsi
 3684a91:      	movq	%r12, %r11
 3684a94:      	movq	%rdx, %rax
 3684a97:      	movq	%r13, %r14
 3684a9a:      	movq	%rbp, %r15
 3684a9d:      	jmp	0x3684b8d <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 3684aa2:      	addq	$-0x40, -0x20(%rsp)
 3684aa8:      	xorl	%ecx, %ecx
 3684aaa:      	nopw	(%rax,%rax)
 3684ab0:      	addq	%r9, %r8
 3684ab3:      	addq	%r13, %r8
 3684ab6:      	movq	0x48(%rdi,%rcx), %r14
 3684abb:      	movq	0x50(%rdi,%rcx), %r10
 3684ac0:      	addq	%r14, %r8
 3684ac3:      	rolq	$0x1b, %r8
 3684ac7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3684ad1:      	imulq	%rsi, %r8
 3684ad5:      	addq	%rdx, %r9
 3684ad8:      	movq	0x70(%rdi,%rcx), %rax
 3684add:      	movq	%rax, -0x8(%rsp)
 3684ae2:      	addq	%rax, %r9
 3684ae5:      	rolq	$0x16, %r9
 3684ae9:      	imulq	%rsi, %r9
 3684aed:      	movq	%r8, %r15
 3684af0:      	xorq	%rbx, %r15
 3684af3:      	movq	0x68(%rdi,%rcx), %r11
 3684af8:      	addq	%r11, %r13
 3684afb:      	addq	%r12, %rbp
 3684afe:      	rolq	$0x1f, %rbp
 3684b02:      	addq	%r13, %r9
 3684b05:      	imulq	%rsi, %rdx
 3684b09:      	addq	0x40(%rdi,%rcx), %rdx
 3684b0e:      	movq	%rbp, %r8
 3684b11:      	movq	0x58(%rdi,%rcx), %r13
 3684b16:      	addq	%rdx, %r12
 3684b19:      	addq	%r13, %r12
 3684b1c:      	addq	%r15, %r12
 3684b1f:      	rolq	$0x2b, %r12
 3684b23:      	addq	%r10, %r14
 3684b26:      	addq	%rdx, %r14
 3684b29:      	movq	%r14, %rax
 3684b2c:      	rolq	$0x14, %rax
 3684b30:      	imulq	%rsi, %r8
 3684b34:      	addq	%rdx, %rax
 3684b37:      	addq	%r12, %rax
 3684b3a:      	addq	%r8, %rbx
 3684b3d:      	addq	%r9, %r10
 3684b40:      	addq	0x60(%rdi,%rcx), %rbx
 3684b45:      	movq	0x78(%rdi,%rcx), %rdx
 3684b4a:      	addq	%rbx, %r10
 3684b4d:      	addq	%rdx, %r10
 3684b50:      	rolq	$0x2b, %r10
 3684b54:      	addq	%r13, %r14
 3684b57:      	addq	-0x8(%rsp), %r11
 3684b5c:      	addq	%rbx, %r11
 3684b5f:      	movq	%r11, %rsi
 3684b62:      	rolq	$0x14, %rsi
 3684b66:      	addq	%rbx, %rsi
 3684b69:      	addq	%r10, %rsi
 3684b6c:      	addq	%rdx, %r11
 3684b6f:      	addq	$0x40, %rcx
 3684b73:      	movq	%r15, %rbp
 3684b76:      	movq	%r14, %r13
 3684b79:      	movq	%rax, %rdx
 3684b7c:      	movq	%r11, %r12
 3684b7f:      	movq	%rsi, %rbx
 3684b82:      	cmpq	%rcx, -0x20(%rsp)
 3684b87:      	jne	0x3684ab0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 3684b8d:      	movq	-0x10(%rsp), %r12
 3684b92:      	testb	$0x3f, %r12b
 3684b96:      	je	0x3684c63 <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f3>
 3684b9c:      	leaq	(%r9,%r14), %rdi
 3684ba0:      	movq	-0x18(%rsp), %rbp
 3684ba5:      	movq	-0x38(%rbp), %rcx
 3684ba9:      	movq	-0x30(%rbp), %rdx
 3684bad:      	addq	%rcx, %r8
 3684bb0:      	addq	%rdi, %r8
 3684bb3:      	rolq	$0x1b, %r8
 3684bb7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3684bc1:      	imulq	%r13, %r8
 3684bc5:      	addq	%rax, %r9
 3684bc8:      	movq	-0x10(%rbp), %r10
 3684bcc:      	addq	%r10, %r9
 3684bcf:      	rolq	$0x16, %r9
 3684bd3:      	imulq	%r13, %r9
 3684bd7:      	xorq	%rsi, %r8
 3684bda:      	movq	-0x18(%rbp), %rdi
 3684bde:      	addq	%rdi, %r14
 3684be1:      	addq	%r14, %r9
 3684be4:      	addq	%r11, %r15
 3684be7:      	rolq	$0x1f, %r15
 3684beb:      	movq	%r15, %rbx
 3684bee:      	imulq	%r13, %rax
 3684bf2:      	addq	%r8, %r11
 3684bf5:      	addq	-0x40(%rbp), %rax
 3684bf9:      	movq	-0x28(%rbp), %r15
 3684bfd:      	addq	%r15, %r11
 3684c00:      	addq	%rax, %r11
 3684c03:      	rolq	$0x2b, %r11
 3684c07:      	imulq	%r13, %rbx
 3684c0b:      	addq	%rdx, %rcx
 3684c0e:      	addq	%rax, %rcx
 3684c11:      	movq	%rcx, %r14
 3684c14:      	rolq	$0x14, %r14
 3684c18:      	addq	%rax, %r14
 3684c1b:      	addq	%r11, %r14
 3684c1e:      	addq	%r15, %rcx
 3684c21:      	addq	%rbx, %rsi
 3684c24:      	addq	-0x20(%rbp), %rsi
 3684c28:      	addq	%r9, %rdx
 3684c2b:      	movq	-0x8(%rbp), %rax
 3684c2f:      	addq	%rax, %rdx
 3684c32:      	addq	%rsi, %rdx
 3684c35:      	rolq	$0x2b, %rdx
 3684c39:      	addq	%r10, %rdi
 3684c3c:      	addq	%rsi, %rdi
 3684c3f:      	movq	%rdi, %r10
 3684c42:      	rolq	$0x14, %r10
 3684c46:      	addq	%rsi, %r10
 3684c49:      	addq	%rdx, %r10
 3684c4c:      	addq	%rax, %rdi
 3684c4f:      	movq	%r10, %rsi
 3684c52:      	movq	%rdi, %r11
 3684c55:      	movq	%r14, %rax
 3684c58:      	movq	%rcx, %r14
 3684c5b:      	movq	%r8, %r15
 3684c5e:      	movq	%rbx, %r8
 3684c61:      	jmp	0x3684c6d <_ZN4llvm7hashing6detail23hash_combine_range_implIKiEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fd>
 3684c63:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3684c6d:      	xorq	%r11, %r14
 3684c70:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3684c7a:      	imulq	%rcx, %r14
 3684c7e:      	xorq	%r14, %r11
 3684c81:      	shrq	$0x2f, %r14
 3684c85:      	xorq	%r11, %r14
 3684c88:      	imulq	%rcx, %r14
 3684c8c:      	movq	%r14, %rdi
 3684c8f:      	shrq	$0x2f, %rdi
 3684c93:      	xorq	%r14, %rdi
 3684c96:      	imulq	%rcx, %rdi
 3684c9a:      	movq	%r9, %rdx
 3684c9d:      	shrq	$0x2f, %rdx
 3684ca1:      	xorq	%r9, %rdx
 3684ca4:      	imulq	%r13, %rdx
 3684ca8:      	addq	%r15, %rdx
 3684cab:      	addq	%rdi, %rdx
 3684cae:      	xorq	%rsi, %rax
 3684cb1:      	imulq	%rcx, %rax
 3684cb5:      	xorq	%rax, %rsi
 3684cb8:      	shrq	$0x2f, %rax
 3684cbc:      	xorq	%rsi, %rax
 3684cbf:      	imulq	%rcx, %rax
 3684cc3:      	movq	%rax, %rsi
 3684cc6:      	shrq	$0x2f, %rsi
 3684cca:      	xorq	%rax, %rsi
 3684ccd:      	imulq	%rcx, %rsi
 3684cd1:      	movq	%r12, %rax
 3684cd4:      	shrq	$0x2f, %rax
 3684cd8:      	xorq	%r12, %rax
 3684cdb:      	imulq	%r13, %rax
 3684cdf:      	addq	%r8, %rax
 3684ce2:      	addq	%rsi, %rax
 3684ce5:      	xorq	%rax, %rdx
 3684ce8:      	imulq	%rcx, %rdx
 3684cec:      	xorq	%rdx, %rax
 3684cef:      	shrq	$0x2f, %rdx
 3684cf3:      	xorq	%rax, %rdx
 3684cf6:      	imulq	%rcx, %rdx
 3684cfa:      	movq	%rdx, %rax
 3684cfd:      	shrq	$0x2f, %rax
 3684d01:      	xorq	%rdx, %rax
 3684d04:      	imulq	%rcx, %rax
 3684d08:      	popq	%rbx
 3684d09:      	popq	%r12
 3684d0b:      	popq	%r13
 3684d0d:      	popq	%r14
 3684d0f:      	popq	%r15
 3684d11:      	popq	%rbp
 3684d12:      	retq
