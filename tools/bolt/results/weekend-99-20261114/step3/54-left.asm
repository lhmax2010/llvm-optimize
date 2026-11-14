
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000008063550 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE>:
 8063550:      	pushq	%rbp
 8063551:      	pushq	%r15
 8063553:      	pushq	%r14
 8063555:      	pushq	%r13
 8063557:      	pushq	%r12
 8063559:      	pushq	%rbx
 806355a:      	subq	$0x28, %rsp
 806355e:      	movq	%rdx, %r13
 8063561:      	movq	%rsi, %r15
 8063564:      	movq	%rdi, %rbx
 8063567:      	movabsq	$-0xae502812ab8d92, %r8 # imm = 0xFF51AFD7ED54726E
 8063571:      	cmpq	$0x40, %rdx
 8063575:      	ja	0x8063591 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x41>
 8063577:      	addq	$0x11a5f, %r8           # imm = 0x11A5F
 806357e:      	movq	%r15, %rdi
 8063581:      	movq	%r13, %rsi
 8063584:      	movq	%r8, %rdx
 8063587:      	callq	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 806358c:      	jmp	0x806390b <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x3bb>
 8063591:      	movq	%rbx, 0x8(%rsp)
 8063596:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 80635a0:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 80635aa:      	movq	%r13, 0x18(%rsp)
 80635af:      	movq	%r13, %r11
 80635b2:      	andq	$-0x40, %r11
 80635b6:      	movq	0x8(%r15), %r13
 80635ba:      	movq	0x10(%r15), %rax
 80635be:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 80635c8:      	addq	%r13, %rdx
 80635cb:      	rolq	$0x1b, %rdx
 80635cf:      	imulq	%rsi, %rdx
 80635d3:      	movq	0x30(%r15), %rdi
 80635d7:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 80635e1:      	addq	%rdi, %r9
 80635e4:      	rolq	$0x16, %r9
 80635e8:      	imulq	%rsi, %r9
 80635ec:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 80635f6:      	xorq	%rdx, %rbp
 80635f9:      	movq	0x28(%r15), %r12
 80635fd:      	movabsq	$-0x7323d61940a0da1f, %rsi # imm = 0x8CDC29E6BF5F25E1
 8063607:      	addq	%r12, %rsi
 806360a:      	addq	%r9, %rsi
 806360d:      	movabsq	$0x298df016a9f64655, %r9 # imm = 0x298DF016A9F64655
 8063617:      	addq	(%r15), %r9
 806361a:      	movq	0x18(%r15), %r10
 806361e:      	addq	%r9, %r8
 8063621:      	addq	%r10, %r8
 8063624:      	addq	%rbp, %r8
 8063627:      	rolq	$0x2b, %r8
 806362b:      	addq	%rax, %r13
 806362e:      	addq	%r9, %r13
 8063631:      	movq	%r13, %rdx
 8063634:      	rolq	$0x14, %rdx
 8063638:      	addq	%r9, %rdx
 806363b:      	addq	%r8, %rdx
 806363e:      	movabsq	$0x4bf62cb950c3753a, %r8 # imm = 0x4BF62CB950C3753A
 8063648:      	addq	0x20(%r15), %r8
 806364c:      	addq	%r10, %r13
 806364f:      	movq	0x38(%r15), %r10
 8063653:      	addq	%r8, %rax
 8063656:      	addq	%r10, %rax
 8063659:      	addq	%rsi, %rax
 806365c:      	rolq	$0x2b, %rax
 8063660:      	addq	%rdi, %r12
 8063663:      	addq	%r8, %r12
 8063666:      	movq	%r12, %r9
 8063669:      	rolq	$0x14, %r9
 806366d:      	addq	%r8, %r9
 8063670:      	addq	%rax, %r9
 8063673:      	addq	%r10, %r12
 8063676:      	movq	%r11, 0x10(%rsp)
 806367b:      	cmpq	$0x40, %r11
 806367f:      	jne	0x8063695 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x145>
 8063681:      	movq	%r9, %rax
 8063684:      	movq	%r12, %r8
 8063687:      	movq	%rdx, %r14
 806368a:      	movq	%r13, %r10
 806368d:      	movq	%rbp, %r11
 8063690:      	jmp	0x8063783 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x233>
 8063695:      	addq	$-0x40, 0x10(%rsp)
 806369b:      	xorl	%ebx, %ebx
 806369d:      	nopl	(%rax)
 80636a0:      	addq	%rsi, %rcx
 80636a3:      	addq	%r13, %rcx
 80636a6:      	movq	0x48(%r15,%rbx), %r10
 80636ab:      	movq	0x50(%r15,%rbx), %rdi
 80636b0:      	addq	%r10, %rcx
 80636b3:      	rolq	$0x1b, %rcx
 80636b7:      	movq	%r15, %rax
 80636ba:      	movabsq	$-0x4b6d499041670d8d, %r15 # imm = 0xB492B66FBE98F273
 80636c4:      	imulq	%r15, %rcx
 80636c8:      	addq	%rdx, %rsi
 80636cb:      	movq	0x70(%rax,%rbx), %r8
 80636d0:      	movq	%r8, 0x20(%rsp)
 80636d5:      	addq	%r8, %rsi
 80636d8:      	rolq	$0x16, %rsi
 80636dc:      	imulq	%r15, %rsi
 80636e0:      	movq	%rcx, %r11
 80636e3:      	xorq	%r9, %r11
 80636e6:      	movq	0x68(%rax,%rbx), %r8
 80636eb:      	addq	%r8, %r13
 80636ee:      	addq	%r12, %rbp
 80636f1:      	rolq	$0x1f, %rbp
 80636f5:      	addq	%r13, %rsi
 80636f8:      	imulq	%r15, %rdx
 80636fc:      	addq	0x40(%rax,%rbx), %rdx
 8063701:      	movq	%rbp, %rcx
 8063704:      	movq	0x58(%rax,%rbx), %r13
 8063709:      	addq	%rdx, %r12
 806370c:      	addq	%r13, %r12
 806370f:      	addq	%r11, %r12
 8063712:      	rolq	$0x2b, %r12
 8063716:      	addq	%rdi, %r10
 8063719:      	addq	%rdx, %r10
 806371c:      	movq	%r10, %r14
 806371f:      	rolq	$0x14, %r14
 8063723:      	imulq	%r15, %rcx
 8063727:      	movq	%rax, %r15
 806372a:      	addq	%rdx, %r14
 806372d:      	addq	%r12, %r14
 8063730:      	addq	%rcx, %r9
 8063733:      	addq	%rsi, %rdi
 8063736:      	addq	0x60(%rax,%rbx), %r9
 806373b:      	movq	0x78(%rax,%rbx), %rdx
 8063740:      	addq	%r9, %rdi
 8063743:      	addq	%rdx, %rdi
 8063746:      	rolq	$0x2b, %rdi
 806374a:      	addq	%r13, %r10
 806374d:      	addq	0x20(%rsp), %r8
 8063752:      	addq	%r9, %r8
 8063755:      	movq	%r8, %rax
 8063758:      	rolq	$0x14, %rax
 806375c:      	addq	%r9, %rax
 806375f:      	addq	%rdi, %rax
 8063762:      	addq	%rdx, %r8
 8063765:      	addq	$0x40, %rbx
 8063769:      	movq	%r11, %rbp
 806376c:      	movq	%r10, %r13
 806376f:      	movq	%r14, %rdx
 8063772:      	movq	%r8, %r12
 8063775:      	movq	%rax, %r9
 8063778:      	cmpq	%rbx, 0x10(%rsp)
 806377d:      	jne	0x80636a0 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x150>
 8063783:      	movq	0x18(%rsp), %r13
 8063788:      	testb	$0x3f, %r13b
 806378c:      	je	0x8063861 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x311>
 8063792:      	leaq	(%rsi,%r10), %r9
 8063796:      	movq	-0x38(%r15,%r13), %rdx
 806379b:      	movq	-0x30(%r15,%r13), %rdi
 80637a0:      	addq	%rdx, %rcx
 80637a3:      	addq	%r9, %rcx
 80637a6:      	rolq	$0x1b, %rcx
 80637aa:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 80637b4:      	imulq	%rbp, %rcx
 80637b8:      	addq	%r14, %rsi
 80637bb:      	movq	-0x10(%r15,%r13), %rbx
 80637c0:      	addq	%rbx, %rsi
 80637c3:      	rolq	$0x16, %rsi
 80637c7:      	imulq	%rbp, %rsi
 80637cb:      	xorq	%rax, %rcx
 80637ce:      	movq	-0x18(%r15,%r13), %r9
 80637d3:      	addq	%r9, %r10
 80637d6:      	addq	%r10, %rsi
 80637d9:      	addq	%r8, %r11
 80637dc:      	rolq	$0x1f, %r11
 80637e0:      	movq	%r11, %r12
 80637e3:      	imulq	%rbp, %r14
 80637e7:      	addq	%rcx, %r8
 80637ea:      	addq	-0x40(%r15,%r13), %r14
 80637ef:      	movq	-0x28(%r15,%r13), %r11
 80637f4:      	addq	%r11, %r8
 80637f7:      	addq	%r14, %r8
 80637fa:      	rolq	$0x2b, %r8
 80637fe:      	imulq	%rbp, %r12
 8063802:      	addq	%rdi, %rdx
 8063805:      	addq	%r14, %rdx
 8063808:      	movq	%rdx, %r10
 806380b:      	rolq	$0x14, %r10
 806380f:      	addq	%r14, %r10
 8063812:      	addq	%r8, %r10
 8063815:      	addq	%r11, %rdx
 8063818:      	addq	%r12, %rax
 806381b:      	addq	-0x20(%r15,%r13), %rax
 8063820:      	addq	%rsi, %rdi
 8063823:      	movq	-0x8(%r15,%r13), %r8
 8063828:      	addq	%r8, %rdi
 806382b:      	addq	%rax, %rdi
 806382e:      	rolq	$0x2b, %rdi
 8063832:      	addq	%rbx, %r9
 8063835:      	addq	%rax, %r9
 8063838:      	movq	%r9, %r11
 806383b:      	rolq	$0x14, %r11
 806383f:      	addq	%rax, %r11
 8063842:      	addq	%rdi, %r11
 8063845:      	addq	%r8, %r9
 8063848:      	movq	%r11, %rax
 806384b:      	movq	%r9, %r8
 806384e:      	movq	%r10, %r14
 8063851:      	movq	%rdx, %r10
 8063854:      	movq	%rcx, %r11
 8063857:      	movq	%r12, %rcx
 806385a:      	movq	0x8(%rsp), %rbx
 806385f:      	jmp	0x8063870 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x320>
 8063861:      	movq	0x8(%rsp), %rbx
 8063866:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 8063870:      	xorq	%r8, %r10
 8063873:      	movabsq	$-0x622015f714c7d297, %rdx # imm = 0x9DDFEA08EB382D69
 806387d:      	imulq	%rdx, %r10
 8063881:      	xorq	%r10, %r8
 8063884:      	shrq	$0x2f, %r10
 8063888:      	xorq	%r8, %r10
 806388b:      	imulq	%rdx, %r10
 806388f:      	movq	%r10, %r8
 8063892:      	shrq	$0x2f, %r8
 8063896:      	xorq	%r10, %r8
 8063899:      	imulq	%rdx, %r8
 806389d:      	movq	%rsi, %rdi
 80638a0:      	shrq	$0x2f, %rdi
 80638a4:      	xorq	%rsi, %rdi
 80638a7:      	imulq	%rbp, %rdi
 80638ab:      	addq	%r11, %rdi
 80638ae:      	addq	%r8, %rdi
 80638b1:      	xorq	%rax, %r14
 80638b4:      	imulq	%rdx, %r14
 80638b8:      	xorq	%r14, %rax
 80638bb:      	shrq	$0x2f, %r14
 80638bf:      	xorq	%rax, %r14
 80638c2:      	imulq	%rdx, %r14
 80638c6:      	movq	%r14, %rax
 80638c9:      	shrq	$0x2f, %rax
 80638cd:      	xorq	%r14, %rax
 80638d0:      	imulq	%rdx, %rax
 80638d4:      	movq	%r13, %rsi
 80638d7:      	shrq	$0x2f, %rsi
 80638db:      	xorq	%r13, %rsi
 80638de:      	imulq	%rbp, %rsi
 80638e2:      	addq	%rcx, %rsi
 80638e5:      	addq	%rax, %rsi
 80638e8:      	xorq	%rsi, %rdi
 80638eb:      	imulq	%rdx, %rdi
 80638ef:      	xorq	%rdi, %rsi
 80638f2:      	shrq	$0x2f, %rdi
 80638f6:      	xorq	%rsi, %rdi
 80638f9:      	imulq	%rdx, %rdi
 80638fd:      	movq	%rdi, %rax
 8063900:      	shrq	$0x2f, %rax
 8063904:      	xorq	%rdi, %rax
 8063907:      	imulq	%rdx, %rax
 806390b:      	movq	%rax, (%rbx)
 806390e:      	movq	%r15, 0x8(%rbx)
 8063912:      	movq	%r13, 0x10(%rbx)
 8063916:      	movq	%rbx, %rax
 8063919:      	addq	$0x28, %rsp
 806391d:      	popq	%rbx
 806391e:      	popq	%r12
 8063920:      	popq	%r13
 8063922:      	popq	%r14
 8063924:      	popq	%r15
 8063926:      	popq	%rbp
 8063927:      	retq
