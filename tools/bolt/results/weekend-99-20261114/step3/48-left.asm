
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000033ee720 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 33ee720:      	movq	%rsi, %rcx
 33ee723:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 33ee72d:      	subq	%rdi, %rsi
 33ee730:      	cmpq	$0x40, %rsi
 33ee734:      	ja	0x33ee744 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 33ee736:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 33ee73c:      	movq	%rax, %rdx
 33ee73f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 33ee744:      	pushq	%rbp
 33ee745:      	pushq	%r15
 33ee747:      	pushq	%r14
 33ee749:      	pushq	%r13
 33ee74b:      	pushq	%r12
 33ee74d:      	pushq	%rbx
 33ee74e:      	movq	%rcx, -0x18(%rsp)
 33ee753:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 33ee75d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 33ee767:      	movq	%rsi, -0x10(%rsp)
 33ee76c:      	movq	%rsi, %r14
 33ee76f:      	andq	$-0x40, %r14
 33ee773:      	movq	0x8(%rdi), %r13
 33ee777:      	movq	0x10(%rdi), %rcx
 33ee77b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 33ee785:      	addq	%r13, %rdx
 33ee788:      	rolq	$0x1b, %rdx
 33ee78c:      	imulq	%r9, %rdx
 33ee790:      	movq	0x30(%rdi), %rsi
 33ee794:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 33ee79e:      	addq	%rsi, %r10
 33ee7a1:      	rolq	$0x16, %r10
 33ee7a5:      	imulq	%r9, %r10
 33ee7a9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 33ee7b3:      	xorq	%rdx, %rbp
 33ee7b6:      	movq	0x28(%rdi), %r12
 33ee7ba:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 33ee7c4:      	addq	%r12, %r9
 33ee7c7:      	addq	%r10, %r9
 33ee7ca:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 33ee7d4:      	addq	(%rdi), %r10
 33ee7d7:      	movq	0x18(%rdi), %r11
 33ee7db:      	addq	%r10, %rax
 33ee7de:      	addq	%r11, %rax
 33ee7e1:      	addq	%rbp, %rax
 33ee7e4:      	rolq	$0x2b, %rax
 33ee7e8:      	addq	%rcx, %r13
 33ee7eb:      	addq	%r10, %r13
 33ee7ee:      	movq	%r13, %rdx
 33ee7f1:      	rolq	$0x14, %rdx
 33ee7f5:      	addq	%r10, %rdx
 33ee7f8:      	addq	%rax, %rdx
 33ee7fb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 33ee805:      	addq	0x20(%rdi), %rax
 33ee809:      	addq	%r11, %r13
 33ee80c:      	movq	0x38(%rdi), %r10
 33ee810:      	addq	%rax, %rcx
 33ee813:      	addq	%r10, %rcx
 33ee816:      	addq	%r9, %rcx
 33ee819:      	rolq	$0x2b, %rcx
 33ee81d:      	addq	%rsi, %r12
 33ee820:      	addq	%rax, %r12
 33ee823:      	movq	%r12, %rbx
 33ee826:      	rolq	$0x14, %rbx
 33ee82a:      	addq	%rax, %rbx
 33ee82d:      	addq	%rcx, %rbx
 33ee830:      	addq	%r10, %r12
 33ee833:      	movq	%r14, -0x20(%rsp)
 33ee838:      	cmpq	$0x40, %r14
 33ee83c:      	jne	0x33ee852 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 33ee83e:      	movq	%rbx, %rsi
 33ee841:      	movq	%r12, %r11
 33ee844:      	movq	%rdx, %rax
 33ee847:      	movq	%r13, %r14
 33ee84a:      	movq	%rbp, %r15
 33ee84d:      	jmp	0x33ee93d <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 33ee852:      	addq	$-0x40, -0x20(%rsp)
 33ee858:      	xorl	%ecx, %ecx
 33ee85a:      	nopw	(%rax,%rax)
 33ee860:      	addq	%r9, %r8
 33ee863:      	addq	%r13, %r8
 33ee866:      	movq	0x48(%rdi,%rcx), %r14
 33ee86b:      	movq	0x50(%rdi,%rcx), %r10
 33ee870:      	addq	%r14, %r8
 33ee873:      	rolq	$0x1b, %r8
 33ee877:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 33ee881:      	imulq	%rsi, %r8
 33ee885:      	addq	%rdx, %r9
 33ee888:      	movq	0x70(%rdi,%rcx), %rax
 33ee88d:      	movq	%rax, -0x8(%rsp)
 33ee892:      	addq	%rax, %r9
 33ee895:      	rolq	$0x16, %r9
 33ee899:      	imulq	%rsi, %r9
 33ee89d:      	movq	%r8, %r15
 33ee8a0:      	xorq	%rbx, %r15
 33ee8a3:      	movq	0x68(%rdi,%rcx), %r11
 33ee8a8:      	addq	%r11, %r13
 33ee8ab:      	addq	%r12, %rbp
 33ee8ae:      	rolq	$0x1f, %rbp
 33ee8b2:      	addq	%r13, %r9
 33ee8b5:      	imulq	%rsi, %rdx
 33ee8b9:      	addq	0x40(%rdi,%rcx), %rdx
 33ee8be:      	movq	%rbp, %r8
 33ee8c1:      	movq	0x58(%rdi,%rcx), %r13
 33ee8c6:      	addq	%rdx, %r12
 33ee8c9:      	addq	%r13, %r12
 33ee8cc:      	addq	%r15, %r12
 33ee8cf:      	rolq	$0x2b, %r12
 33ee8d3:      	addq	%r10, %r14
 33ee8d6:      	addq	%rdx, %r14
 33ee8d9:      	movq	%r14, %rax
 33ee8dc:      	rolq	$0x14, %rax
 33ee8e0:      	imulq	%rsi, %r8
 33ee8e4:      	addq	%rdx, %rax
 33ee8e7:      	addq	%r12, %rax
 33ee8ea:      	addq	%r8, %rbx
 33ee8ed:      	addq	%r9, %r10
 33ee8f0:      	addq	0x60(%rdi,%rcx), %rbx
 33ee8f5:      	movq	0x78(%rdi,%rcx), %rdx
 33ee8fa:      	addq	%rbx, %r10
 33ee8fd:      	addq	%rdx, %r10
 33ee900:      	rolq	$0x2b, %r10
 33ee904:      	addq	%r13, %r14
 33ee907:      	addq	-0x8(%rsp), %r11
 33ee90c:      	addq	%rbx, %r11
 33ee90f:      	movq	%r11, %rsi
 33ee912:      	rolq	$0x14, %rsi
 33ee916:      	addq	%rbx, %rsi
 33ee919:      	addq	%r10, %rsi
 33ee91c:      	addq	%rdx, %r11
 33ee91f:      	addq	$0x40, %rcx
 33ee923:      	movq	%r15, %rbp
 33ee926:      	movq	%r14, %r13
 33ee929:      	movq	%rax, %rdx
 33ee92c:      	movq	%r11, %r12
 33ee92f:      	movq	%rsi, %rbx
 33ee932:      	cmpq	%rcx, -0x20(%rsp)
 33ee937:      	jne	0x33ee860 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 33ee93d:      	movq	-0x10(%rsp), %r12
 33ee942:      	testb	$0x3f, %r12b
 33ee946:      	je	0x33eea13 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f3>
 33ee94c:      	leaq	(%r9,%r14), %rdi
 33ee950:      	movq	-0x18(%rsp), %rbp
 33ee955:      	movq	-0x38(%rbp), %rcx
 33ee959:      	movq	-0x30(%rbp), %rdx
 33ee95d:      	addq	%rcx, %r8
 33ee960:      	addq	%rdi, %r8
 33ee963:      	rolq	$0x1b, %r8
 33ee967:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 33ee971:      	imulq	%r13, %r8
 33ee975:      	addq	%rax, %r9
 33ee978:      	movq	-0x10(%rbp), %r10
 33ee97c:      	addq	%r10, %r9
 33ee97f:      	rolq	$0x16, %r9
 33ee983:      	imulq	%r13, %r9
 33ee987:      	xorq	%rsi, %r8
 33ee98a:      	movq	-0x18(%rbp), %rdi
 33ee98e:      	addq	%rdi, %r14
 33ee991:      	addq	%r14, %r9
 33ee994:      	addq	%r11, %r15
 33ee997:      	rolq	$0x1f, %r15
 33ee99b:      	movq	%r15, %rbx
 33ee99e:      	imulq	%r13, %rax
 33ee9a2:      	addq	%r8, %r11
 33ee9a5:      	addq	-0x40(%rbp), %rax
 33ee9a9:      	movq	-0x28(%rbp), %r15
 33ee9ad:      	addq	%r15, %r11
 33ee9b0:      	addq	%rax, %r11
 33ee9b3:      	rolq	$0x2b, %r11
 33ee9b7:      	imulq	%r13, %rbx
 33ee9bb:      	addq	%rdx, %rcx
 33ee9be:      	addq	%rax, %rcx
 33ee9c1:      	movq	%rcx, %r14
 33ee9c4:      	rolq	$0x14, %r14
 33ee9c8:      	addq	%rax, %r14
 33ee9cb:      	addq	%r11, %r14
 33ee9ce:      	addq	%r15, %rcx
 33ee9d1:      	addq	%rbx, %rsi
 33ee9d4:      	addq	-0x20(%rbp), %rsi
 33ee9d8:      	addq	%r9, %rdx
 33ee9db:      	movq	-0x8(%rbp), %rax
 33ee9df:      	addq	%rax, %rdx
 33ee9e2:      	addq	%rsi, %rdx
 33ee9e5:      	rolq	$0x2b, %rdx
 33ee9e9:      	addq	%r10, %rdi
 33ee9ec:      	addq	%rsi, %rdi
 33ee9ef:      	movq	%rdi, %r10
 33ee9f2:      	rolq	$0x14, %r10
 33ee9f6:      	addq	%rsi, %r10
 33ee9f9:      	addq	%rdx, %r10
 33ee9fc:      	addq	%rax, %rdi
 33ee9ff:      	movq	%r10, %rsi
 33eea02:      	movq	%rdi, %r11
 33eea05:      	movq	%r14, %rax
 33eea08:      	movq	%rcx, %r14
 33eea0b:      	movq	%r8, %r15
 33eea0e:      	movq	%rbx, %r8
 33eea11:      	jmp	0x33eea1d <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fd>
 33eea13:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 33eea1d:      	xorq	%r11, %r14
 33eea20:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 33eea2a:      	imulq	%rcx, %r14
 33eea2e:      	xorq	%r14, %r11
 33eea31:      	shrq	$0x2f, %r14
 33eea35:      	xorq	%r11, %r14
 33eea38:      	imulq	%rcx, %r14
 33eea3c:      	movq	%r14, %rdi
 33eea3f:      	shrq	$0x2f, %rdi
 33eea43:      	xorq	%r14, %rdi
 33eea46:      	imulq	%rcx, %rdi
 33eea4a:      	movq	%r9, %rdx
 33eea4d:      	shrq	$0x2f, %rdx
 33eea51:      	xorq	%r9, %rdx
 33eea54:      	imulq	%r13, %rdx
 33eea58:      	addq	%r15, %rdx
 33eea5b:      	addq	%rdi, %rdx
 33eea5e:      	xorq	%rsi, %rax
 33eea61:      	imulq	%rcx, %rax
 33eea65:      	xorq	%rax, %rsi
 33eea68:      	shrq	$0x2f, %rax
 33eea6c:      	xorq	%rsi, %rax
 33eea6f:      	imulq	%rcx, %rax
 33eea73:      	movq	%rax, %rsi
 33eea76:      	shrq	$0x2f, %rsi
 33eea7a:      	xorq	%rax, %rsi
 33eea7d:      	imulq	%rcx, %rsi
 33eea81:      	movq	%r12, %rax
 33eea84:      	shrq	$0x2f, %rax
 33eea88:      	xorq	%r12, %rax
 33eea8b:      	imulq	%r13, %rax
 33eea8f:      	addq	%r8, %rax
 33eea92:      	addq	%rsi, %rax
 33eea95:      	xorq	%rax, %rdx
 33eea98:      	imulq	%rcx, %rdx
 33eea9c:      	xorq	%rdx, %rax
 33eea9f:      	shrq	$0x2f, %rdx
 33eeaa3:      	xorq	%rax, %rdx
 33eeaa6:      	imulq	%rcx, %rdx
 33eeaaa:      	movq	%rdx, %rax
 33eeaad:      	shrq	$0x2f, %rax
 33eeab1:      	xorq	%rdx, %rax
 33eeab4:      	imulq	%rcx, %rax
 33eeab8:      	popq	%rbx
 33eeab9:      	popq	%r12
 33eeabb:      	popq	%r13
 33eeabd:      	popq	%r14
 33eeabf:      	popq	%r15
 33eeac1:      	popq	%rbp
 33eeac2:      	retq
