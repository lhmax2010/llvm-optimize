
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003afe550 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3afe550:      	movq	%rsi, %rcx
 3afe553:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3afe55d:      	subq	%rdi, %rsi
 3afe560:      	cmpq	$0x40, %rsi
 3afe564:      	ja	0x3afe574 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3afe566:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3afe56c:      	movq	%rax, %rdx
 3afe56f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3afe574:      	pushq	%rbp
 3afe575:      	pushq	%r15
 3afe577:      	pushq	%r14
 3afe579:      	pushq	%r13
 3afe57b:      	pushq	%r12
 3afe57d:      	pushq	%rbx
 3afe57e:      	movq	%rcx, -0x18(%rsp)
 3afe583:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3afe58d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3afe597:      	movq	%rsi, -0x10(%rsp)
 3afe59c:      	movq	%rsi, %r14
 3afe59f:      	andq	$-0x40, %r14
 3afe5a3:      	movq	0x8(%rdi), %r13
 3afe5a7:      	movq	0x10(%rdi), %rcx
 3afe5ab:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3afe5b5:      	addq	%r13, %rdx
 3afe5b8:      	rolq	$0x1b, %rdx
 3afe5bc:      	imulq	%r9, %rdx
 3afe5c0:      	movq	0x30(%rdi), %rsi
 3afe5c4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3afe5ce:      	addq	%rsi, %r10
 3afe5d1:      	rolq	$0x16, %r10
 3afe5d5:      	imulq	%r9, %r10
 3afe5d9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3afe5e3:      	xorq	%rdx, %rbp
 3afe5e6:      	movq	0x28(%rdi), %r12
 3afe5ea:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3afe5f4:      	addq	%r12, %r9
 3afe5f7:      	addq	%r10, %r9
 3afe5fa:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3afe604:      	addq	(%rdi), %r10
 3afe607:      	movq	0x18(%rdi), %r11
 3afe60b:      	addq	%r10, %rax
 3afe60e:      	addq	%r11, %rax
 3afe611:      	addq	%rbp, %rax
 3afe614:      	rolq	$0x2b, %rax
 3afe618:      	addq	%rcx, %r13
 3afe61b:      	addq	%r10, %r13
 3afe61e:      	movq	%r13, %rdx
 3afe621:      	rolq	$0x14, %rdx
 3afe625:      	addq	%r10, %rdx
 3afe628:      	addq	%rax, %rdx
 3afe62b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3afe635:      	addq	0x20(%rdi), %rax
 3afe639:      	addq	%r11, %r13
 3afe63c:      	movq	0x38(%rdi), %r10
 3afe640:      	addq	%rax, %rcx
 3afe643:      	addq	%r10, %rcx
 3afe646:      	addq	%r9, %rcx
 3afe649:      	rolq	$0x2b, %rcx
 3afe64d:      	addq	%rsi, %r12
 3afe650:      	addq	%rax, %r12
 3afe653:      	movq	%r12, %rbx
 3afe656:      	rolq	$0x14, %rbx
 3afe65a:      	addq	%rax, %rbx
 3afe65d:      	addq	%rcx, %rbx
 3afe660:      	addq	%r10, %r12
 3afe663:      	movq	%r14, -0x20(%rsp)
 3afe668:      	cmpq	$0x40, %r14
 3afe66c:      	jne	0x3afe682 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3afe66e:      	movq	%rbx, %rsi
 3afe671:      	movq	%r12, %r11
 3afe674:      	movq	%rdx, %rax
 3afe677:      	movq	%r13, %r14
 3afe67a:      	movq	%rbp, %r15
 3afe67d:      	jmp	0x3afe76d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3afe682:      	addq	$-0x40, -0x20(%rsp)
 3afe688:      	xorl	%ecx, %ecx
 3afe68a:      	nopw	(%rax,%rax)
 3afe690:      	addq	%r9, %r8
 3afe693:      	addq	%r13, %r8
 3afe696:      	movq	0x48(%rdi,%rcx), %r14
 3afe69b:      	movq	0x50(%rdi,%rcx), %r10
 3afe6a0:      	addq	%r14, %r8
 3afe6a3:      	rolq	$0x1b, %r8
 3afe6a7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3afe6b1:      	imulq	%rsi, %r8
 3afe6b5:      	addq	%rdx, %r9
 3afe6b8:      	movq	0x70(%rdi,%rcx), %rax
 3afe6bd:      	movq	%rax, -0x8(%rsp)
 3afe6c2:      	addq	%rax, %r9
 3afe6c5:      	rolq	$0x16, %r9
 3afe6c9:      	imulq	%rsi, %r9
 3afe6cd:      	movq	%r8, %r15
 3afe6d0:      	xorq	%rbx, %r15
 3afe6d3:      	movq	0x68(%rdi,%rcx), %r11
 3afe6d8:      	addq	%r11, %r13
 3afe6db:      	addq	%r12, %rbp
 3afe6de:      	rolq	$0x1f, %rbp
 3afe6e2:      	addq	%r13, %r9
 3afe6e5:      	imulq	%rsi, %rdx
 3afe6e9:      	addq	0x40(%rdi,%rcx), %rdx
 3afe6ee:      	movq	%rbp, %r8
 3afe6f1:      	movq	0x58(%rdi,%rcx), %r13
 3afe6f6:      	addq	%rdx, %r12
 3afe6f9:      	addq	%r13, %r12
 3afe6fc:      	addq	%r15, %r12
 3afe6ff:      	rolq	$0x2b, %r12
 3afe703:      	addq	%r10, %r14
 3afe706:      	addq	%rdx, %r14
 3afe709:      	movq	%r14, %rax
 3afe70c:      	rolq	$0x14, %rax
 3afe710:      	imulq	%rsi, %r8
 3afe714:      	addq	%rdx, %rax
 3afe717:      	addq	%r12, %rax
 3afe71a:      	addq	%r8, %rbx
 3afe71d:      	addq	%r9, %r10
 3afe720:      	addq	0x60(%rdi,%rcx), %rbx
 3afe725:      	movq	0x78(%rdi,%rcx), %rdx
 3afe72a:      	addq	%rbx, %r10
 3afe72d:      	addq	%rdx, %r10
 3afe730:      	rolq	$0x2b, %r10
 3afe734:      	addq	%r13, %r14
 3afe737:      	addq	-0x8(%rsp), %r11
 3afe73c:      	addq	%rbx, %r11
 3afe73f:      	movq	%r11, %rsi
 3afe742:      	rolq	$0x14, %rsi
 3afe746:      	addq	%rbx, %rsi
 3afe749:      	addq	%r10, %rsi
 3afe74c:      	addq	%rdx, %r11
 3afe74f:      	addq	$0x40, %rcx
 3afe753:      	movq	%r15, %rbp
 3afe756:      	movq	%r14, %r13
 3afe759:      	movq	%rax, %rdx
 3afe75c:      	movq	%r11, %r12
 3afe75f:      	movq	%rsi, %rbx
 3afe762:      	cmpq	%rcx, -0x20(%rsp)
 3afe767:      	jne	0x3afe690 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3afe76d:      	movq	-0x10(%rsp), %r12
 3afe772:      	testb	$0x3f, %r12b
 3afe776:      	je	0x3afe842 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 3afe77c:      	movq	-0x18(%rsp), %rbp
 3afe781:      	movq	-0x38(%rbp), %rcx
 3afe785:      	movq	-0x30(%rbp), %rdx
 3afe789:      	addq	%rcx, %r8
 3afe78c:      	addq	%r9, %r8
 3afe78f:      	addq	%r14, %r8
 3afe792:      	rolq	$0x1b, %r8
 3afe796:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3afe7a0:      	imulq	%r13, %r8
 3afe7a4:      	addq	%rax, %r9
 3afe7a7:      	movq	-0x10(%rbp), %r10
 3afe7ab:      	addq	%r10, %r9
 3afe7ae:      	rolq	$0x16, %r9
 3afe7b2:      	imulq	%r13, %r9
 3afe7b6:      	xorq	%rsi, %r8
 3afe7b9:      	movq	-0x18(%rbp), %rdi
 3afe7bd:      	addq	%rdi, %r14
 3afe7c0:      	addq	%r14, %r9
 3afe7c3:      	addq	%r11, %r15
 3afe7c6:      	rolq	$0x1f, %r15
 3afe7ca:      	movq	%r15, %rbx
 3afe7cd:      	imulq	%r13, %rax
 3afe7d1:      	addq	%r8, %r11
 3afe7d4:      	addq	-0x40(%rbp), %rax
 3afe7d8:      	movq	-0x28(%rbp), %r15
 3afe7dc:      	addq	%r15, %r11
 3afe7df:      	addq	%rax, %r11
 3afe7e2:      	rolq	$0x2b, %r11
 3afe7e6:      	imulq	%r13, %rbx
 3afe7ea:      	addq	%rdx, %rcx
 3afe7ed:      	addq	%rax, %rcx
 3afe7f0:      	movq	%rcx, %r14
 3afe7f3:      	rolq	$0x14, %r14
 3afe7f7:      	addq	%rax, %r14
 3afe7fa:      	addq	%r11, %r14
 3afe7fd:      	addq	%r15, %rcx
 3afe800:      	addq	%rbx, %rsi
 3afe803:      	addq	-0x20(%rbp), %rsi
 3afe807:      	addq	%r9, %rdx
 3afe80a:      	movq	-0x8(%rbp), %rax
 3afe80e:      	addq	%rax, %rdx
 3afe811:      	addq	%rsi, %rdx
 3afe814:      	rolq	$0x2b, %rdx
 3afe818:      	addq	%r10, %rdi
 3afe81b:      	addq	%rsi, %rdi
 3afe81e:      	movq	%rdi, %r10
 3afe821:      	rolq	$0x14, %r10
 3afe825:      	addq	%rsi, %r10
 3afe828:      	addq	%rdx, %r10
 3afe82b:      	addq	%rax, %rdi
 3afe82e:      	movq	%r10, %rsi
 3afe831:      	movq	%rdi, %r11
 3afe834:      	movq	%r14, %rax
 3afe837:      	movq	%rcx, %r14
 3afe83a:      	movq	%r8, %r15
 3afe83d:      	movq	%rbx, %r8
 3afe840:      	jmp	0x3afe84c <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8ConstantEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 3afe842:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3afe84c:      	xorq	%r11, %r14
 3afe84f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3afe859:      	imulq	%rcx, %r14
 3afe85d:      	xorq	%r14, %r11
 3afe860:      	shrq	$0x2f, %r14
 3afe864:      	xorq	%r11, %r14
 3afe867:      	imulq	%rcx, %r14
 3afe86b:      	movq	%r14, %rdi
 3afe86e:      	shrq	$0x2f, %rdi
 3afe872:      	xorq	%r14, %rdi
 3afe875:      	imulq	%rcx, %rdi
 3afe879:      	movq	%r9, %rdx
 3afe87c:      	shrq	$0x2f, %rdx
 3afe880:      	xorq	%r9, %rdx
 3afe883:      	imulq	%r13, %rdx
 3afe887:      	addq	%r15, %rdx
 3afe88a:      	addq	%rdi, %rdx
 3afe88d:      	xorq	%rsi, %rax
 3afe890:      	imulq	%rcx, %rax
 3afe894:      	xorq	%rax, %rsi
 3afe897:      	shrq	$0x2f, %rax
 3afe89b:      	xorq	%rsi, %rax
 3afe89e:      	imulq	%rcx, %rax
 3afe8a2:      	movq	%rax, %rsi
 3afe8a5:      	shrq	$0x2f, %rsi
 3afe8a9:      	xorq	%rax, %rsi
 3afe8ac:      	imulq	%rcx, %rsi
 3afe8b0:      	movq	%r12, %rax
 3afe8b3:      	shrq	$0x2f, %rax
 3afe8b7:      	xorq	%r12, %rax
 3afe8ba:      	imulq	%r13, %rax
 3afe8be:      	addq	%r8, %rax
 3afe8c1:      	addq	%rsi, %rax
 3afe8c4:      	xorq	%rax, %rdx
 3afe8c7:      	imulq	%rcx, %rdx
 3afe8cb:      	xorq	%rdx, %rax
 3afe8ce:      	shrq	$0x2f, %rdx
 3afe8d2:      	xorq	%rax, %rdx
 3afe8d5:      	imulq	%rcx, %rdx
 3afe8d9:      	movq	%rdx, %rax
 3afe8dc:      	shrq	$0x2f, %rax
 3afe8e0:      	xorq	%rdx, %rax
 3afe8e3:      	imulq	%rcx, %rax
 3afe8e7:      	popq	%rbx
 3afe8e8:      	popq	%r12
 3afe8ea:      	popq	%r13
 3afe8ec:      	popq	%r14
 3afe8ee:      	popq	%r15
 3afe8f0:      	popq	%rbp
 3afe8f1:      	retq
