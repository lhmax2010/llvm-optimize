
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000562f6b0 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_>:
 562f6b0:      	movq	%rsi, %rcx
 562f6b3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 562f6bd:      	subq	%rdi, %rsi
 562f6c0:      	cmpq	$0x40, %rsi
 562f6c4:      	ja	0x562f6d4 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x24>
 562f6c6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 562f6cc:      	movq	%rax, %rdx
 562f6cf:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 562f6d4:      	pushq	%rbp
 562f6d5:      	pushq	%r15
 562f6d7:      	pushq	%r14
 562f6d9:      	pushq	%r13
 562f6db:      	pushq	%r12
 562f6dd:      	pushq	%rbx
 562f6de:      	movq	%rcx, -0x18(%rsp)
 562f6e3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 562f6ed:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 562f6f7:      	movq	%rsi, -0x10(%rsp)
 562f6fc:      	movq	%rsi, %r14
 562f6ff:      	andq	$-0x40, %r14
 562f703:      	movq	0x8(%rdi), %r13
 562f707:      	movq	0x10(%rdi), %rcx
 562f70b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 562f715:      	addq	%r13, %rdx
 562f718:      	rolq	$0x1b, %rdx
 562f71c:      	imulq	%r9, %rdx
 562f720:      	movq	0x30(%rdi), %rsi
 562f724:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 562f72e:      	addq	%rsi, %r10
 562f731:      	rolq	$0x16, %r10
 562f735:      	imulq	%r9, %r10
 562f739:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 562f743:      	xorq	%rdx, %rbp
 562f746:      	movq	0x28(%rdi), %r12
 562f74a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 562f754:      	addq	%r12, %r9
 562f757:      	addq	%r10, %r9
 562f75a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 562f764:      	addq	(%rdi), %r10
 562f767:      	movq	0x18(%rdi), %r11
 562f76b:      	addq	%r10, %rax
 562f76e:      	addq	%r11, %rax
 562f771:      	addq	%rbp, %rax
 562f774:      	rolq	$0x2b, %rax
 562f778:      	addq	%rcx, %r13
 562f77b:      	addq	%r10, %r13
 562f77e:      	movq	%r13, %rdx
 562f781:      	rolq	$0x14, %rdx
 562f785:      	addq	%r10, %rdx
 562f788:      	addq	%rax, %rdx
 562f78b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 562f795:      	addq	0x20(%rdi), %rax
 562f799:      	addq	%r11, %r13
 562f79c:      	movq	0x38(%rdi), %r10
 562f7a0:      	addq	%rax, %rcx
 562f7a3:      	addq	%r10, %rcx
 562f7a6:      	addq	%r9, %rcx
 562f7a9:      	rolq	$0x2b, %rcx
 562f7ad:      	addq	%rsi, %r12
 562f7b0:      	addq	%rax, %r12
 562f7b3:      	movq	%r12, %rbx
 562f7b6:      	rolq	$0x14, %rbx
 562f7ba:      	addq	%rax, %rbx
 562f7bd:      	addq	%rcx, %rbx
 562f7c0:      	addq	%r10, %r12
 562f7c3:      	movq	%r14, -0x20(%rsp)
 562f7c8:      	cmpq	$0x40, %r14
 562f7cc:      	jne	0x562f7e2 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x132>
 562f7ce:      	movq	%rbx, %rsi
 562f7d1:      	movq	%r12, %r11
 562f7d4:      	movq	%rdx, %rax
 562f7d7:      	movq	%r13, %r14
 562f7da:      	movq	%rbp, %r15
 562f7dd:      	jmp	0x562f8cd <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x21d>
 562f7e2:      	addq	$-0x40, -0x20(%rsp)
 562f7e8:      	xorl	%ecx, %ecx
 562f7ea:      	nopw	(%rax,%rax)
 562f7f0:      	addq	%r9, %r8
 562f7f3:      	addq	%r13, %r8
 562f7f6:      	movq	0x48(%rdi,%rcx), %r14
 562f7fb:      	movq	0x50(%rdi,%rcx), %r10
 562f800:      	addq	%r14, %r8
 562f803:      	rolq	$0x1b, %r8
 562f807:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 562f811:      	imulq	%rsi, %r8
 562f815:      	addq	%rdx, %r9
 562f818:      	movq	0x70(%rdi,%rcx), %rax
 562f81d:      	movq	%rax, -0x8(%rsp)
 562f822:      	addq	%rax, %r9
 562f825:      	rolq	$0x16, %r9
 562f829:      	imulq	%rsi, %r9
 562f82d:      	movq	%r8, %r15
 562f830:      	xorq	%rbx, %r15
 562f833:      	movq	0x68(%rdi,%rcx), %r11
 562f838:      	addq	%r11, %r13
 562f83b:      	addq	%r12, %rbp
 562f83e:      	rolq	$0x1f, %rbp
 562f842:      	addq	%r13, %r9
 562f845:      	imulq	%rsi, %rdx
 562f849:      	addq	0x40(%rdi,%rcx), %rdx
 562f84e:      	movq	%rbp, %r8
 562f851:      	movq	0x58(%rdi,%rcx), %r13
 562f856:      	addq	%rdx, %r12
 562f859:      	addq	%r13, %r12
 562f85c:      	addq	%r15, %r12
 562f85f:      	rolq	$0x2b, %r12
 562f863:      	addq	%r10, %r14
 562f866:      	addq	%rdx, %r14
 562f869:      	movq	%r14, %rax
 562f86c:      	rolq	$0x14, %rax
 562f870:      	imulq	%rsi, %r8
 562f874:      	addq	%rdx, %rax
 562f877:      	addq	%r12, %rax
 562f87a:      	addq	%r8, %rbx
 562f87d:      	addq	%r9, %r10
 562f880:      	addq	0x60(%rdi,%rcx), %rbx
 562f885:      	movq	0x78(%rdi,%rcx), %rdx
 562f88a:      	addq	%rbx, %r10
 562f88d:      	addq	%rdx, %r10
 562f890:      	rolq	$0x2b, %r10
 562f894:      	addq	%r13, %r14
 562f897:      	addq	-0x8(%rsp), %r11
 562f89c:      	addq	%rbx, %r11
 562f89f:      	movq	%r11, %rsi
 562f8a2:      	rolq	$0x14, %rsi
 562f8a6:      	addq	%rbx, %rsi
 562f8a9:      	addq	%r10, %rsi
 562f8ac:      	addq	%rdx, %r11
 562f8af:      	addq	$0x40, %rcx
 562f8b3:      	movq	%r15, %rbp
 562f8b6:      	movq	%r14, %r13
 562f8b9:      	movq	%rax, %rdx
 562f8bc:      	movq	%r11, %r12
 562f8bf:      	movq	%rsi, %rbx
 562f8c2:      	cmpq	%rcx, -0x20(%rsp)
 562f8c7:      	jne	0x562f7f0 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x140>
 562f8cd:      	movq	-0x10(%rsp), %r12
 562f8d2:      	testb	$0x3f, %r12b
 562f8d6:      	je	0x562f9a2 <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x2f2>
 562f8dc:      	movq	-0x18(%rsp), %rbp
 562f8e1:      	movq	-0x38(%rbp), %rcx
 562f8e5:      	movq	-0x30(%rbp), %rdx
 562f8e9:      	addq	%rcx, %r8
 562f8ec:      	addq	%r9, %r8
 562f8ef:      	addq	%r14, %r8
 562f8f2:      	rolq	$0x1b, %r8
 562f8f6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 562f900:      	imulq	%r13, %r8
 562f904:      	addq	%rax, %r9
 562f907:      	movq	-0x10(%rbp), %r10
 562f90b:      	addq	%r10, %r9
 562f90e:      	rolq	$0x16, %r9
 562f912:      	imulq	%r13, %r9
 562f916:      	xorq	%rsi, %r8
 562f919:      	movq	-0x18(%rbp), %rdi
 562f91d:      	addq	%rdi, %r14
 562f920:      	addq	%r14, %r9
 562f923:      	addq	%r11, %r15
 562f926:      	rolq	$0x1f, %r15
 562f92a:      	movq	%r15, %rbx
 562f92d:      	imulq	%r13, %rax
 562f931:      	addq	%r8, %r11
 562f934:      	addq	-0x40(%rbp), %rax
 562f938:      	movq	-0x28(%rbp), %r15
 562f93c:      	addq	%r15, %r11
 562f93f:      	addq	%rax, %r11
 562f942:      	rolq	$0x2b, %r11
 562f946:      	imulq	%r13, %rbx
 562f94a:      	addq	%rdx, %rcx
 562f94d:      	addq	%rax, %rcx
 562f950:      	movq	%rcx, %r14
 562f953:      	rolq	$0x14, %r14
 562f957:      	addq	%rax, %r14
 562f95a:      	addq	%r11, %r14
 562f95d:      	addq	%r15, %rcx
 562f960:      	addq	%rbx, %rsi
 562f963:      	addq	-0x20(%rbp), %rsi
 562f967:      	addq	%r9, %rdx
 562f96a:      	movq	-0x8(%rbp), %rax
 562f96e:      	addq	%rax, %rdx
 562f971:      	addq	%rsi, %rdx
 562f974:      	rolq	$0x2b, %rdx
 562f978:      	addq	%r10, %rdi
 562f97b:      	addq	%rsi, %rdi
 562f97e:      	movq	%rdi, %r10
 562f981:      	rolq	$0x14, %r10
 562f985:      	addq	%rsi, %r10
 562f988:      	addq	%rdx, %r10
 562f98b:      	addq	%rax, %rdi
 562f98e:      	movq	%r10, %rsi
 562f991:      	movq	%rdi, %r11
 562f994:      	movq	%r14, %rax
 562f997:      	movq	%rcx, %r14
 562f99a:      	movq	%r8, %r15
 562f99d:      	movq	%rbx, %r8
 562f9a0:      	jmp	0x562f9ac <_ZN4llvm7hashing6detail23hash_combine_range_implIPNS_4TypeEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS6_SA_+0x2fc>
 562f9a2:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 562f9ac:      	xorq	%r11, %r14
 562f9af:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 562f9b9:      	imulq	%rcx, %r14
 562f9bd:      	xorq	%r14, %r11
 562f9c0:      	shrq	$0x2f, %r14
 562f9c4:      	xorq	%r11, %r14
 562f9c7:      	imulq	%rcx, %r14
 562f9cb:      	movq	%r14, %rdi
 562f9ce:      	shrq	$0x2f, %rdi
 562f9d2:      	xorq	%r14, %rdi
 562f9d5:      	imulq	%rcx, %rdi
 562f9d9:      	movq	%r9, %rdx
 562f9dc:      	shrq	$0x2f, %rdx
 562f9e0:      	xorq	%r9, %rdx
 562f9e3:      	imulq	%r13, %rdx
 562f9e7:      	addq	%r15, %rdx
 562f9ea:      	addq	%rdi, %rdx
 562f9ed:      	xorq	%rsi, %rax
 562f9f0:      	imulq	%rcx, %rax
 562f9f4:      	xorq	%rax, %rsi
 562f9f7:      	shrq	$0x2f, %rax
 562f9fb:      	xorq	%rsi, %rax
 562f9fe:      	imulq	%rcx, %rax
 562fa02:      	movq	%rax, %rsi
 562fa05:      	shrq	$0x2f, %rsi
 562fa09:      	xorq	%rax, %rsi
 562fa0c:      	imulq	%rcx, %rsi
 562fa10:      	movq	%r12, %rax
 562fa13:      	shrq	$0x2f, %rax
 562fa17:      	xorq	%r12, %rax
 562fa1a:      	imulq	%r13, %rax
 562fa1e:      	addq	%r8, %rax
 562fa21:      	addq	%rsi, %rax
 562fa24:      	xorq	%rax, %rdx
 562fa27:      	imulq	%rcx, %rdx
 562fa2b:      	xorq	%rdx, %rax
 562fa2e:      	shrq	$0x2f, %rdx
 562fa32:      	xorq	%rax, %rdx
 562fa35:      	imulq	%rcx, %rdx
 562fa39:      	movq	%rdx, %rax
 562fa3c:      	shrq	$0x2f, %rax
 562fa40:      	xorq	%rdx, %rax
 562fa43:      	imulq	%rcx, %rax
 562fa47:      	popq	%rbx
 562fa48:      	popq	%r12
 562fa4a:      	popq	%r13
 562fa4c:      	popq	%r14
 562fa4e:      	popq	%r15
 562fa50:      	popq	%rbp
 562fa51:      	retq
