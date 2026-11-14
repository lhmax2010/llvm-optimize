
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003afe5e0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3afe5e0:      	movq	%rsi, %rcx
 3afe5e3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3afe5ed:      	subq	%rdi, %rsi
 3afe5f0:      	cmpq	$0x40, %rsi
 3afe5f4:      	ja	0x3afe604 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3afe5f6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3afe5fc:      	movq	%rax, %rdx
 3afe5ff:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3afe604:      	pushq	%rbp
 3afe605:      	pushq	%r15
 3afe607:      	pushq	%r14
 3afe609:      	pushq	%r13
 3afe60b:      	pushq	%r12
 3afe60d:      	pushq	%rbx
 3afe60e:      	movq	%rcx, -0x18(%rsp)
 3afe613:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3afe61d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3afe627:      	movq	%rsi, -0x10(%rsp)
 3afe62c:      	movq	%rsi, %r14
 3afe62f:      	andq	$-0x40, %r14
 3afe633:      	movq	0x8(%rdi), %r13
 3afe637:      	movq	0x10(%rdi), %rcx
 3afe63b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3afe645:      	addq	%r13, %rdx
 3afe648:      	rolq	$0x1b, %rdx
 3afe64c:      	imulq	%r9, %rdx
 3afe650:      	movq	0x30(%rdi), %rsi
 3afe654:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3afe65e:      	addq	%rsi, %r10
 3afe661:      	rolq	$0x16, %r10
 3afe665:      	imulq	%r9, %r10
 3afe669:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3afe673:      	xorq	%rdx, %rbp
 3afe676:      	movq	0x28(%rdi), %r12
 3afe67a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3afe684:      	addq	%r12, %r9
 3afe687:      	addq	%r10, %r9
 3afe68a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3afe694:      	addq	(%rdi), %r10
 3afe697:      	movq	0x18(%rdi), %r11
 3afe69b:      	addq	%r10, %rax
 3afe69e:      	addq	%r11, %rax
 3afe6a1:      	addq	%rbp, %rax
 3afe6a4:      	rolq	$0x2b, %rax
 3afe6a8:      	addq	%rcx, %r13
 3afe6ab:      	addq	%r10, %r13
 3afe6ae:      	movq	%r13, %rdx
 3afe6b1:      	rolq	$0x14, %rdx
 3afe6b5:      	addq	%r10, %rdx
 3afe6b8:      	addq	%rax, %rdx
 3afe6bb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3afe6c5:      	addq	0x20(%rdi), %rax
 3afe6c9:      	addq	%r11, %r13
 3afe6cc:      	movq	0x38(%rdi), %r10
 3afe6d0:      	addq	%rax, %rcx
 3afe6d3:      	addq	%r10, %rcx
 3afe6d6:      	addq	%r9, %rcx
 3afe6d9:      	rolq	$0x2b, %rcx
 3afe6dd:      	addq	%rsi, %r12
 3afe6e0:      	addq	%rax, %r12
 3afe6e3:      	movq	%r12, %rbx
 3afe6e6:      	rolq	$0x14, %rbx
 3afe6ea:      	addq	%rax, %rbx
 3afe6ed:      	addq	%rcx, %rbx
 3afe6f0:      	addq	%r10, %r12
 3afe6f3:      	movq	%r14, -0x20(%rsp)
 3afe6f8:      	cmpq	$0x40, %r14
 3afe6fc:      	jne	0x3afe712 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3afe6fe:      	movq	%rbx, %rsi
 3afe701:      	movq	%r12, %r11
 3afe704:      	movq	%rdx, %rax
 3afe707:      	movq	%r13, %r14
 3afe70a:      	movq	%rbp, %r15
 3afe70d:      	jmp	0x3afe7fd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3afe712:      	addq	$-0x40, -0x20(%rsp)
 3afe718:      	xorl	%ecx, %ecx
 3afe71a:      	nopw	(%rax,%rax)
 3afe720:      	addq	%r9, %r8
 3afe723:      	addq	%r13, %r8
 3afe726:      	movq	0x48(%rdi,%rcx), %r14
 3afe72b:      	movq	0x50(%rdi,%rcx), %r10
 3afe730:      	addq	%r14, %r8
 3afe733:      	rolq	$0x1b, %r8
 3afe737:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3afe741:      	imulq	%rsi, %r8
 3afe745:      	addq	%rdx, %r9
 3afe748:      	movq	0x70(%rdi,%rcx), %rax
 3afe74d:      	movq	%rax, -0x8(%rsp)
 3afe752:      	addq	%rax, %r9
 3afe755:      	rolq	$0x16, %r9
 3afe759:      	imulq	%rsi, %r9
 3afe75d:      	movq	%r8, %r15
 3afe760:      	xorq	%rbx, %r15
 3afe763:      	movq	0x68(%rdi,%rcx), %r11
 3afe768:      	addq	%r11, %r13
 3afe76b:      	addq	%r12, %rbp
 3afe76e:      	rolq	$0x1f, %rbp
 3afe772:      	addq	%r13, %r9
 3afe775:      	imulq	%rsi, %rdx
 3afe779:      	addq	0x40(%rdi,%rcx), %rdx
 3afe77e:      	movq	%rbp, %r8
 3afe781:      	movq	0x58(%rdi,%rcx), %r13
 3afe786:      	addq	%rdx, %r12
 3afe789:      	addq	%r13, %r12
 3afe78c:      	addq	%r15, %r12
 3afe78f:      	rolq	$0x2b, %r12
 3afe793:      	addq	%r10, %r14
 3afe796:      	addq	%rdx, %r14
 3afe799:      	movq	%r14, %rax
 3afe79c:      	rolq	$0x14, %rax
 3afe7a0:      	imulq	%rsi, %r8
 3afe7a4:      	addq	%rdx, %rax
 3afe7a7:      	addq	%r12, %rax
 3afe7aa:      	addq	%r8, %rbx
 3afe7ad:      	addq	%r9, %r10
 3afe7b0:      	addq	0x60(%rdi,%rcx), %rbx
 3afe7b5:      	movq	0x78(%rdi,%rcx), %rdx
 3afe7ba:      	addq	%rbx, %r10
 3afe7bd:      	addq	%rdx, %r10
 3afe7c0:      	rolq	$0x2b, %r10
 3afe7c4:      	addq	%r13, %r14
 3afe7c7:      	addq	-0x8(%rsp), %r11
 3afe7cc:      	addq	%rbx, %r11
 3afe7cf:      	movq	%r11, %rsi
 3afe7d2:      	rolq	$0x14, %rsi
 3afe7d6:      	addq	%rbx, %rsi
 3afe7d9:      	addq	%r10, %rsi
 3afe7dc:      	addq	%rdx, %r11
 3afe7df:      	addq	$0x40, %rcx
 3afe7e3:      	movq	%r15, %rbp
 3afe7e6:      	movq	%r14, %r13
 3afe7e9:      	movq	%rax, %rdx
 3afe7ec:      	movq	%r11, %r12
 3afe7ef:      	movq	%rsi, %rbx
 3afe7f2:      	cmpq	%rcx, -0x20(%rsp)
 3afe7f7:      	jne	0x3afe720 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3afe7fd:      	movq	-0x10(%rsp), %r12
 3afe802:      	testb	$0x3f, %r12b
 3afe806:      	je	0x3afe8d3 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 3afe80c:      	leaq	(%r9,%r14), %rdi
 3afe810:      	movq	-0x18(%rsp), %rbp
 3afe815:      	movq	-0x38(%rbp), %rcx
 3afe819:      	movq	-0x30(%rbp), %rdx
 3afe81d:      	addq	%rcx, %r8
 3afe820:      	addq	%rdi, %r8
 3afe823:      	rolq	$0x1b, %r8
 3afe827:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3afe831:      	imulq	%r13, %r8
 3afe835:      	addq	%rax, %r9
 3afe838:      	movq	-0x10(%rbp), %r10
 3afe83c:      	addq	%r10, %r9
 3afe83f:      	rolq	$0x16, %r9
 3afe843:      	imulq	%r13, %r9
 3afe847:      	xorq	%rsi, %r8
 3afe84a:      	movq	-0x18(%rbp), %rdi
 3afe84e:      	addq	%rdi, %r14
 3afe851:      	addq	%r14, %r9
 3afe854:      	addq	%r11, %r15
 3afe857:      	rolq	$0x1f, %r15
 3afe85b:      	movq	%r15, %rbx
 3afe85e:      	imulq	%r13, %rax
 3afe862:      	addq	%r8, %r11
 3afe865:      	addq	-0x40(%rbp), %rax
 3afe869:      	movq	-0x28(%rbp), %r15
 3afe86d:      	addq	%r15, %r11
 3afe870:      	addq	%rax, %r11
 3afe873:      	rolq	$0x2b, %r11
 3afe877:      	imulq	%r13, %rbx
 3afe87b:      	addq	%rdx, %rcx
 3afe87e:      	addq	%rax, %rcx
 3afe881:      	movq	%rcx, %r14
 3afe884:      	rolq	$0x14, %r14
 3afe888:      	addq	%rax, %r14
 3afe88b:      	addq	%r11, %r14
 3afe88e:      	addq	%r15, %rcx
 3afe891:      	addq	%rbx, %rsi
 3afe894:      	addq	-0x20(%rbp), %rsi
 3afe898:      	addq	%r9, %rdx
 3afe89b:      	movq	-0x8(%rbp), %rax
 3afe89f:      	addq	%rax, %rdx
 3afe8a2:      	addq	%rsi, %rdx
 3afe8a5:      	rolq	$0x2b, %rdx
 3afe8a9:      	addq	%r10, %rdi
 3afe8ac:      	addq	%rsi, %rdi
 3afe8af:      	movq	%rdi, %r10
 3afe8b2:      	rolq	$0x14, %r10
 3afe8b6:      	addq	%rsi, %r10
 3afe8b9:      	addq	%rdx, %r10
 3afe8bc:      	addq	%rax, %rdi
 3afe8bf:      	movq	%r10, %rsi
 3afe8c2:      	movq	%rdi, %r11
 3afe8c5:      	movq	%r14, %rax
 3afe8c8:      	movq	%rcx, %r14
 3afe8cb:      	movq	%r8, %r15
 3afe8ce:      	movq	%rbx, %r8
 3afe8d1:      	jmp	0x3afe8dd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 3afe8d3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3afe8dd:      	xorq	%r11, %r14
 3afe8e0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3afe8ea:      	imulq	%rcx, %r14
 3afe8ee:      	xorq	%r14, %r11
 3afe8f1:      	shrq	$0x2f, %r14
 3afe8f5:      	xorq	%r11, %r14
 3afe8f8:      	imulq	%rcx, %r14
 3afe8fc:      	movq	%r14, %rdi
 3afe8ff:      	shrq	$0x2f, %rdi
 3afe903:      	xorq	%r14, %rdi
 3afe906:      	imulq	%rcx, %rdi
 3afe90a:      	movq	%r9, %rdx
 3afe90d:      	shrq	$0x2f, %rdx
 3afe911:      	xorq	%r9, %rdx
 3afe914:      	imulq	%r13, %rdx
 3afe918:      	addq	%r15, %rdx
 3afe91b:      	addq	%rdi, %rdx
 3afe91e:      	xorq	%rsi, %rax
 3afe921:      	imulq	%rcx, %rax
 3afe925:      	xorq	%rax, %rsi
 3afe928:      	shrq	$0x2f, %rax
 3afe92c:      	xorq	%rsi, %rax
 3afe92f:      	imulq	%rcx, %rax
 3afe933:      	movq	%rax, %rsi
 3afe936:      	shrq	$0x2f, %rsi
 3afe93a:      	xorq	%rax, %rsi
 3afe93d:      	imulq	%rcx, %rsi
 3afe941:      	movq	%r12, %rax
 3afe944:      	shrq	$0x2f, %rax
 3afe948:      	xorq	%r12, %rax
 3afe94b:      	imulq	%r13, %rax
 3afe94f:      	addq	%r8, %rax
 3afe952:      	addq	%rsi, %rax
 3afe955:      	xorq	%rax, %rdx
 3afe958:      	imulq	%rcx, %rdx
 3afe95c:      	xorq	%rdx, %rax
 3afe95f:      	shrq	$0x2f, %rdx
 3afe963:      	xorq	%rax, %rdx
 3afe966:      	imulq	%rcx, %rdx
 3afe96a:      	movq	%rdx, %rax
 3afe96d:      	shrq	$0x2f, %rax
 3afe971:      	xorq	%rdx, %rax
 3afe974:      	imulq	%rcx, %rax
 3afe978:      	popq	%rbx
 3afe979:      	popq	%r12
 3afe97b:      	popq	%r13
 3afe97d:      	popq	%r14
 3afe97f:      	popq	%r15
 3afe981:      	popq	%rbp
 3afe982:      	retq
