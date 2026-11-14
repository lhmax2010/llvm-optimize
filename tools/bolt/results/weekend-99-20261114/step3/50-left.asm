
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000562f740 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_>:
 562f740:      	movq	%rsi, %rcx
 562f743:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 562f74d:      	subq	%rdi, %rsi
 562f750:      	cmpq	$0x40, %rsi
 562f754:      	ja	0x562f764 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x24>
 562f756:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 562f75c:      	movq	%rax, %rdx
 562f75f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 562f764:      	pushq	%rbp
 562f765:      	pushq	%r15
 562f767:      	pushq	%r14
 562f769:      	pushq	%r13
 562f76b:      	pushq	%r12
 562f76d:      	pushq	%rbx
 562f76e:      	movq	%rcx, -0x18(%rsp)
 562f773:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 562f77d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 562f787:      	movq	%rsi, -0x10(%rsp)
 562f78c:      	movq	%rsi, %r14
 562f78f:      	andq	$-0x40, %r14
 562f793:      	movq	0x8(%rdi), %r13
 562f797:      	movq	0x10(%rdi), %rcx
 562f79b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 562f7a5:      	addq	%r13, %rdx
 562f7a8:      	rolq	$0x1b, %rdx
 562f7ac:      	imulq	%r9, %rdx
 562f7b0:      	movq	0x30(%rdi), %rsi
 562f7b4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 562f7be:      	addq	%rsi, %r10
 562f7c1:      	rolq	$0x16, %r10
 562f7c5:      	imulq	%r9, %r10
 562f7c9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 562f7d3:      	xorq	%rdx, %rbp
 562f7d6:      	movq	0x28(%rdi), %r12
 562f7da:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 562f7e4:      	addq	%r12, %r9
 562f7e7:      	addq	%r10, %r9
 562f7ea:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 562f7f4:      	addq	(%rdi), %r10
 562f7f7:      	movq	0x18(%rdi), %r11
 562f7fb:      	addq	%r10, %rax
 562f7fe:      	addq	%r11, %rax
 562f801:      	addq	%rbp, %rax
 562f804:      	rolq	$0x2b, %rax
 562f808:      	addq	%rcx, %r13
 562f80b:      	addq	%r10, %r13
 562f80e:      	movq	%r13, %rdx
 562f811:      	rolq	$0x14, %rdx
 562f815:      	addq	%r10, %rdx
 562f818:      	addq	%rax, %rdx
 562f81b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 562f825:      	addq	0x20(%rdi), %rax
 562f829:      	addq	%r11, %r13
 562f82c:      	movq	0x38(%rdi), %r10
 562f830:      	addq	%rax, %rcx
 562f833:      	addq	%r10, %rcx
 562f836:      	addq	%r9, %rcx
 562f839:      	rolq	$0x2b, %rcx
 562f83d:      	addq	%rsi, %r12
 562f840:      	addq	%rax, %r12
 562f843:      	movq	%r12, %rbx
 562f846:      	rolq	$0x14, %rbx
 562f84a:      	addq	%rax, %rbx
 562f84d:      	addq	%rcx, %rbx
 562f850:      	addq	%r10, %r12
 562f853:      	movq	%r14, -0x20(%rsp)
 562f858:      	cmpq	$0x40, %r14
 562f85c:      	jne	0x562f872 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x132>
 562f85e:      	movq	%rbx, %rsi
 562f861:      	movq	%r12, %r11
 562f864:      	movq	%rdx, %rax
 562f867:      	movq	%r13, %r14
 562f86a:      	movq	%rbp, %r15
 562f86d:      	jmp	0x562f95d <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x21d>
 562f872:      	addq	$-0x40, -0x20(%rsp)
 562f878:      	xorl	%ecx, %ecx
 562f87a:      	nopw	(%rax,%rax)
 562f880:      	addq	%r9, %r8
 562f883:      	addq	%r13, %r8
 562f886:      	movq	0x48(%rdi,%rcx), %r14
 562f88b:      	movq	0x50(%rdi,%rcx), %r10
 562f890:      	addq	%r14, %r8
 562f893:      	rolq	$0x1b, %r8
 562f897:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 562f8a1:      	imulq	%rsi, %r8
 562f8a5:      	addq	%rdx, %r9
 562f8a8:      	movq	0x70(%rdi,%rcx), %rax
 562f8ad:      	movq	%rax, -0x8(%rsp)
 562f8b2:      	addq	%rax, %r9
 562f8b5:      	rolq	$0x16, %r9
 562f8b9:      	imulq	%rsi, %r9
 562f8bd:      	movq	%r8, %r15
 562f8c0:      	xorq	%rbx, %r15
 562f8c3:      	movq	0x68(%rdi,%rcx), %r11
 562f8c8:      	addq	%r11, %r13
 562f8cb:      	addq	%r12, %rbp
 562f8ce:      	rolq	$0x1f, %rbp
 562f8d2:      	addq	%r13, %r9
 562f8d5:      	imulq	%rsi, %rdx
 562f8d9:      	addq	0x40(%rdi,%rcx), %rdx
 562f8de:      	movq	%rbp, %r8
 562f8e1:      	movq	0x58(%rdi,%rcx), %r13
 562f8e6:      	addq	%rdx, %r12
 562f8e9:      	addq	%r13, %r12
 562f8ec:      	addq	%r15, %r12
 562f8ef:      	rolq	$0x2b, %r12
 562f8f3:      	addq	%r10, %r14
 562f8f6:      	addq	%rdx, %r14
 562f8f9:      	movq	%r14, %rax
 562f8fc:      	rolq	$0x14, %rax
 562f900:      	imulq	%rsi, %r8
 562f904:      	addq	%rdx, %rax
 562f907:      	addq	%r12, %rax
 562f90a:      	addq	%r8, %rbx
 562f90d:      	addq	%r9, %r10
 562f910:      	addq	0x60(%rdi,%rcx), %rbx
 562f915:      	movq	0x78(%rdi,%rcx), %rdx
 562f91a:      	addq	%rbx, %r10
 562f91d:      	addq	%rdx, %r10
 562f920:      	rolq	$0x2b, %r10
 562f924:      	addq	%r13, %r14
 562f927:      	addq	-0x8(%rsp), %r11
 562f92c:      	addq	%rbx, %r11
 562f92f:      	movq	%r11, %rsi
 562f932:      	rolq	$0x14, %rsi
 562f936:      	addq	%rbx, %rsi
 562f939:      	addq	%r10, %rsi
 562f93c:      	addq	%rdx, %r11
 562f93f:      	addq	$0x40, %rcx
 562f943:      	movq	%r15, %rbp
 562f946:      	movq	%r14, %r13
 562f949:      	movq	%rax, %rdx
 562f94c:      	movq	%r11, %r12
 562f94f:      	movq	%rsi, %rbx
 562f952:      	cmpq	%rcx, -0x20(%rsp)
 562f957:      	jne	0x562f880 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x140>
 562f95d:      	movq	-0x10(%rsp), %r12
 562f962:      	testb	$0x3f, %r12b
 562f966:      	je	0x562fa33 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x2f3>
 562f96c:      	leaq	(%r9,%r14), %rdi
 562f970:      	movq	-0x18(%rsp), %rbp
 562f975:      	movq	-0x38(%rbp), %rcx
 562f979:      	movq	-0x30(%rbp), %rdx
 562f97d:      	addq	%rcx, %r8
 562f980:      	addq	%rdi, %r8
 562f983:      	rolq	$0x1b, %r8
 562f987:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 562f991:      	imulq	%r13, %r8
 562f995:      	addq	%rax, %r9
 562f998:      	movq	-0x10(%rbp), %r10
 562f99c:      	addq	%r10, %r9
 562f99f:      	rolq	$0x16, %r9
 562f9a3:      	imulq	%r13, %r9
 562f9a7:      	xorq	%rsi, %r8
 562f9aa:      	movq	-0x18(%rbp), %rdi
 562f9ae:      	addq	%rdi, %r14
 562f9b1:      	addq	%r14, %r9
 562f9b4:      	addq	%r11, %r15
 562f9b7:      	rolq	$0x1f, %r15
 562f9bb:      	movq	%r15, %rbx
 562f9be:      	imulq	%r13, %rax
 562f9c2:      	addq	%r8, %r11
 562f9c5:      	addq	-0x40(%rbp), %rax
 562f9c9:      	movq	-0x28(%rbp), %r15
 562f9cd:      	addq	%r15, %r11
 562f9d0:      	addq	%rax, %r11
 562f9d3:      	rolq	$0x2b, %r11
 562f9d7:      	imulq	%r13, %rbx
 562f9db:      	addq	%rdx, %rcx
 562f9de:      	addq	%rax, %rcx
 562f9e1:      	movq	%rcx, %r14
 562f9e4:      	rolq	$0x14, %r14
 562f9e8:      	addq	%rax, %r14
 562f9eb:      	addq	%r11, %r14
 562f9ee:      	addq	%r15, %rcx
 562f9f1:      	addq	%rbx, %rsi
 562f9f4:      	addq	-0x20(%rbp), %rsi
 562f9f8:      	addq	%r9, %rdx
 562f9fb:      	movq	-0x8(%rbp), %rax
 562f9ff:      	addq	%rax, %rdx
 562fa02:      	addq	%rsi, %rdx
 562fa05:      	rolq	$0x2b, %rdx
 562fa09:      	addq	%r10, %rdi
 562fa0c:      	addq	%rsi, %rdi
 562fa0f:      	movq	%rdi, %r10
 562fa12:      	rolq	$0x14, %r10
 562fa16:      	addq	%rsi, %r10
 562fa19:      	addq	%rdx, %r10
 562fa1c:      	addq	%rax, %rdi
 562fa1f:      	movq	%r10, %rsi
 562fa22:      	movq	%rdi, %r11
 562fa25:      	movq	%r14, %rax
 562fa28:      	movq	%rcx, %r14
 562fa2b:      	movq	%r8, %r15
 562fa2e:      	movq	%rbx, %r8
 562fa31:      	jmp	0x562fa3d <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x2fd>
 562fa33:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 562fa3d:      	xorq	%r11, %r14
 562fa40:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 562fa4a:      	imulq	%rcx, %r14
 562fa4e:      	xorq	%r14, %r11
 562fa51:      	shrq	$0x2f, %r14
 562fa55:      	xorq	%r11, %r14
 562fa58:      	imulq	%rcx, %r14
 562fa5c:      	movq	%r14, %rdi
 562fa5f:      	shrq	$0x2f, %rdi
 562fa63:      	xorq	%r14, %rdi
 562fa66:      	imulq	%rcx, %rdi
 562fa6a:      	movq	%r9, %rdx
 562fa6d:      	shrq	$0x2f, %rdx
 562fa71:      	xorq	%r9, %rdx
 562fa74:      	imulq	%r13, %rdx
 562fa78:      	addq	%r15, %rdx
 562fa7b:      	addq	%rdi, %rdx
 562fa7e:      	xorq	%rsi, %rax
 562fa81:      	imulq	%rcx, %rax
 562fa85:      	xorq	%rax, %rsi
 562fa88:      	shrq	$0x2f, %rax
 562fa8c:      	xorq	%rsi, %rax
 562fa8f:      	imulq	%rcx, %rax
 562fa93:      	movq	%rax, %rsi
 562fa96:      	shrq	$0x2f, %rsi
 562fa9a:      	xorq	%rax, %rsi
 562fa9d:      	imulq	%rcx, %rsi
 562faa1:      	movq	%r12, %rax
 562faa4:      	shrq	$0x2f, %rax
 562faa8:      	xorq	%r12, %rax
 562faab:      	imulq	%r13, %rax
 562faaf:      	addq	%r8, %rax
 562fab2:      	addq	%rsi, %rax
 562fab5:      	xorq	%rax, %rdx
 562fab8:      	imulq	%rcx, %rdx
 562fabc:      	xorq	%rdx, %rax
 562fabf:      	shrq	$0x2f, %rdx
 562fac3:      	xorq	%rax, %rdx
 562fac6:      	imulq	%rcx, %rdx
 562faca:      	movq	%rdx, %rax
 562facd:      	shrq	$0x2f, %rax
 562fad1:      	xorq	%rdx, %rax
 562fad4:      	imulq	%rcx, %rax
 562fad8:      	popq	%rbx
 562fad9:      	popq	%r12
 562fadb:      	popq	%r13
 562fadd:      	popq	%r14
 562fadf:      	popq	%r15
 562fae1:      	popq	%rbp
 562fae2:      	retq
