
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000080634c0 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE>:
 80634c0:      	pushq	%rbp
 80634c1:      	pushq	%r15
 80634c3:      	pushq	%r14
 80634c5:      	pushq	%r13
 80634c7:      	pushq	%r12
 80634c9:      	pushq	%rbx
 80634ca:      	subq	$0x28, %rsp
 80634ce:      	movq	%rdx, %r13
 80634d1:      	movq	%rsi, %r15
 80634d4:      	movq	%rdi, %rbx
 80634d7:      	movabsq	$-0xae502812ab8d92, %r8 # imm = 0xFF51AFD7ED54726E
 80634e1:      	cmpq	$0x40, %rdx
 80634e5:      	ja	0x8063501 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x41>
 80634e7:      	addq	$0x11a5f, %r8           # imm = 0x11A5F
 80634ee:      	movq	%r15, %rdi
 80634f1:      	movq	%r13, %rsi
 80634f4:      	movq	%r8, %rdx
 80634f7:      	callq	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 80634fc:      	jmp	0x806387a <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x3ba>
 8063501:      	movq	%rbx, 0x8(%rsp)
 8063506:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 8063510:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 806351a:      	movq	%r13, 0x18(%rsp)
 806351f:      	movq	%r13, %r11
 8063522:      	andq	$-0x40, %r11
 8063526:      	movq	0x8(%r15), %r13
 806352a:      	movq	0x10(%r15), %rax
 806352e:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 8063538:      	addq	%r13, %rdx
 806353b:      	rolq	$0x1b, %rdx
 806353f:      	imulq	%rsi, %rdx
 8063543:      	movq	0x30(%r15), %rdi
 8063547:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 8063551:      	addq	%rdi, %r9
 8063554:      	rolq	$0x16, %r9
 8063558:      	imulq	%rsi, %r9
 806355c:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 8063566:      	xorq	%rdx, %rbp
 8063569:      	movq	0x28(%r15), %r12
 806356d:      	movabsq	$-0x7323d61940a0da1f, %rsi # imm = 0x8CDC29E6BF5F25E1
 8063577:      	addq	%r12, %rsi
 806357a:      	addq	%r9, %rsi
 806357d:      	movabsq	$0x298df016a9f64655, %r9 # imm = 0x298DF016A9F64655
 8063587:      	addq	(%r15), %r9
 806358a:      	movq	0x18(%r15), %r10
 806358e:      	addq	%r9, %r8
 8063591:      	addq	%r10, %r8
 8063594:      	addq	%rbp, %r8
 8063597:      	rolq	$0x2b, %r8
 806359b:      	addq	%rax, %r13
 806359e:      	addq	%r9, %r13
 80635a1:      	movq	%r13, %rdx
 80635a4:      	rolq	$0x14, %rdx
 80635a8:      	addq	%r9, %rdx
 80635ab:      	addq	%r8, %rdx
 80635ae:      	movabsq	$0x4bf62cb950c3753a, %r8 # imm = 0x4BF62CB950C3753A
 80635b8:      	addq	0x20(%r15), %r8
 80635bc:      	addq	%r10, %r13
 80635bf:      	movq	0x38(%r15), %r10
 80635c3:      	addq	%r8, %rax
 80635c6:      	addq	%r10, %rax
 80635c9:      	addq	%rsi, %rax
 80635cc:      	rolq	$0x2b, %rax
 80635d0:      	addq	%rdi, %r12
 80635d3:      	addq	%r8, %r12
 80635d6:      	movq	%r12, %r9
 80635d9:      	rolq	$0x14, %r9
 80635dd:      	addq	%r8, %r9
 80635e0:      	addq	%rax, %r9
 80635e3:      	addq	%r10, %r12
 80635e6:      	movq	%r11, 0x10(%rsp)
 80635eb:      	cmpq	$0x40, %r11
 80635ef:      	jne	0x8063605 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x145>
 80635f1:      	movq	%r9, %rax
 80635f4:      	movq	%r12, %r8
 80635f7:      	movq	%rdx, %r14
 80635fa:      	movq	%r13, %r10
 80635fd:      	movq	%rbp, %r11
 8063600:      	jmp	0x80636f3 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x233>
 8063605:      	addq	$-0x40, 0x10(%rsp)
 806360b:      	xorl	%ebx, %ebx
 806360d:      	nopl	(%rax)
 8063610:      	addq	%rsi, %rcx
 8063613:      	addq	%r13, %rcx
 8063616:      	movq	0x48(%r15,%rbx), %r10
 806361b:      	movq	0x50(%r15,%rbx), %rdi
 8063620:      	addq	%r10, %rcx
 8063623:      	rolq	$0x1b, %rcx
 8063627:      	movq	%r15, %rax
 806362a:      	movabsq	$-0x4b6d499041670d8d, %r15 # imm = 0xB492B66FBE98F273
 8063634:      	imulq	%r15, %rcx
 8063638:      	addq	%rdx, %rsi
 806363b:      	movq	0x70(%rax,%rbx), %r8
 8063640:      	movq	%r8, 0x20(%rsp)
 8063645:      	addq	%r8, %rsi
 8063648:      	rolq	$0x16, %rsi
 806364c:      	imulq	%r15, %rsi
 8063650:      	movq	%rcx, %r11
 8063653:      	xorq	%r9, %r11
 8063656:      	movq	0x68(%rax,%rbx), %r8
 806365b:      	addq	%r8, %r13
 806365e:      	addq	%r12, %rbp
 8063661:      	rolq	$0x1f, %rbp
 8063665:      	addq	%r13, %rsi
 8063668:      	imulq	%r15, %rdx
 806366c:      	addq	0x40(%rax,%rbx), %rdx
 8063671:      	movq	%rbp, %rcx
 8063674:      	movq	0x58(%rax,%rbx), %r13
 8063679:      	addq	%rdx, %r12
 806367c:      	addq	%r13, %r12
 806367f:      	addq	%r11, %r12
 8063682:      	rolq	$0x2b, %r12
 8063686:      	addq	%rdi, %r10
 8063689:      	addq	%rdx, %r10
 806368c:      	movq	%r10, %r14
 806368f:      	rolq	$0x14, %r14
 8063693:      	imulq	%r15, %rcx
 8063697:      	movq	%rax, %r15
 806369a:      	addq	%rdx, %r14
 806369d:      	addq	%r12, %r14
 80636a0:      	addq	%rcx, %r9
 80636a3:      	addq	%rsi, %rdi
 80636a6:      	addq	0x60(%rax,%rbx), %r9
 80636ab:      	movq	0x78(%rax,%rbx), %rdx
 80636b0:      	addq	%r9, %rdi
 80636b3:      	addq	%rdx, %rdi
 80636b6:      	rolq	$0x2b, %rdi
 80636ba:      	addq	%r13, %r10
 80636bd:      	addq	0x20(%rsp), %r8
 80636c2:      	addq	%r9, %r8
 80636c5:      	movq	%r8, %rax
 80636c8:      	rolq	$0x14, %rax
 80636cc:      	addq	%r9, %rax
 80636cf:      	addq	%rdi, %rax
 80636d2:      	addq	%rdx, %r8
 80636d5:      	addq	$0x40, %rbx
 80636d9:      	movq	%r11, %rbp
 80636dc:      	movq	%r10, %r13
 80636df:      	movq	%r14, %rdx
 80636e2:      	movq	%r8, %r12
 80636e5:      	movq	%rax, %r9
 80636e8:      	cmpq	%rbx, 0x10(%rsp)
 80636ed:      	jne	0x8063610 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x150>
 80636f3:      	movq	0x18(%rsp), %r13
 80636f8:      	testb	$0x3f, %r13b
 80636fc:      	je	0x80637d0 <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x310>
 8063702:      	movq	-0x38(%r15,%r13), %rdx
 8063707:      	movq	-0x30(%r15,%r13), %rdi
 806370c:      	addq	%rdx, %rcx
 806370f:      	addq	%rsi, %rcx
 8063712:      	addq	%r10, %rcx
 8063715:      	rolq	$0x1b, %rcx
 8063719:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 8063723:      	imulq	%rbp, %rcx
 8063727:      	addq	%r14, %rsi
 806372a:      	movq	-0x10(%r15,%r13), %rbx
 806372f:      	addq	%rbx, %rsi
 8063732:      	rolq	$0x16, %rsi
 8063736:      	imulq	%rbp, %rsi
 806373a:      	xorq	%rax, %rcx
 806373d:      	movq	-0x18(%r15,%r13), %r9
 8063742:      	addq	%r9, %r10
 8063745:      	addq	%r10, %rsi
 8063748:      	addq	%r8, %r11
 806374b:      	rolq	$0x1f, %r11
 806374f:      	movq	%r11, %r12
 8063752:      	imulq	%rbp, %r14
 8063756:      	addq	%rcx, %r8
 8063759:      	addq	-0x40(%r15,%r13), %r14
 806375e:      	movq	-0x28(%r15,%r13), %r11
 8063763:      	addq	%r11, %r8
 8063766:      	addq	%r14, %r8
 8063769:      	rolq	$0x2b, %r8
 806376d:      	imulq	%rbp, %r12
 8063771:      	addq	%rdi, %rdx
 8063774:      	addq	%r14, %rdx
 8063777:      	movq	%rdx, %r10
 806377a:      	rolq	$0x14, %r10
 806377e:      	addq	%r14, %r10
 8063781:      	addq	%r8, %r10
 8063784:      	addq	%r11, %rdx
 8063787:      	addq	%r12, %rax
 806378a:      	addq	-0x20(%r15,%r13), %rax
 806378f:      	addq	%rsi, %rdi
 8063792:      	movq	-0x8(%r15,%r13), %r8
 8063797:      	addq	%r8, %rdi
 806379a:      	addq	%rax, %rdi
 806379d:      	rolq	$0x2b, %rdi
 80637a1:      	addq	%rbx, %r9
 80637a4:      	addq	%rax, %r9
 80637a7:      	movq	%r9, %r11
 80637aa:      	rolq	$0x14, %r11
 80637ae:      	addq	%rax, %r11
 80637b1:      	addq	%rdi, %r11
 80637b4:      	addq	%r8, %r9
 80637b7:      	movq	%r11, %rax
 80637ba:      	movq	%r9, %r8
 80637bd:      	movq	%r10, %r14
 80637c0:      	movq	%rdx, %r10
 80637c3:      	movq	%rcx, %r11
 80637c6:      	movq	%r12, %rcx
 80637c9:      	movq	0x8(%rsp), %rbx
 80637ce:      	jmp	0x80637df <_ZN4llvm8codeview17LocallyHashedType8hashTypeENS_8ArrayRefIhEE+0x31f>
 80637d0:      	movq	0x8(%rsp), %rbx
 80637d5:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 80637df:      	xorq	%r8, %r10
 80637e2:      	movabsq	$-0x622015f714c7d297, %rdx # imm = 0x9DDFEA08EB382D69
 80637ec:      	imulq	%rdx, %r10
 80637f0:      	xorq	%r10, %r8
 80637f3:      	shrq	$0x2f, %r10
 80637f7:      	xorq	%r8, %r10
 80637fa:      	imulq	%rdx, %r10
 80637fe:      	movq	%r10, %r8
 8063801:      	shrq	$0x2f, %r8
 8063805:      	xorq	%r10, %r8
 8063808:      	imulq	%rdx, %r8
 806380c:      	movq	%rsi, %rdi
 806380f:      	shrq	$0x2f, %rdi
 8063813:      	xorq	%rsi, %rdi
 8063816:      	imulq	%rbp, %rdi
 806381a:      	addq	%r11, %rdi
 806381d:      	addq	%r8, %rdi
 8063820:      	xorq	%rax, %r14
 8063823:      	imulq	%rdx, %r14
 8063827:      	xorq	%r14, %rax
 806382a:      	shrq	$0x2f, %r14
 806382e:      	xorq	%rax, %r14
 8063831:      	imulq	%rdx, %r14
 8063835:      	movq	%r14, %rax
 8063838:      	shrq	$0x2f, %rax
 806383c:      	xorq	%r14, %rax
 806383f:      	imulq	%rdx, %rax
 8063843:      	movq	%r13, %rsi
 8063846:      	shrq	$0x2f, %rsi
 806384a:      	xorq	%r13, %rsi
 806384d:      	imulq	%rbp, %rsi
 8063851:      	addq	%rcx, %rsi
 8063854:      	addq	%rax, %rsi
 8063857:      	xorq	%rsi, %rdi
 806385a:      	imulq	%rdx, %rdi
 806385e:      	xorq	%rdi, %rsi
 8063861:      	shrq	$0x2f, %rdi
 8063865:      	xorq	%rsi, %rdi
 8063868:      	imulq	%rdx, %rdi
 806386c:      	movq	%rdi, %rax
 806386f:      	shrq	$0x2f, %rax
 8063873:      	xorq	%rdi, %rax
 8063876:      	imulq	%rdx, %rax
 806387a:      	movq	%rax, (%rbx)
 806387d:      	movq	%r15, 0x8(%rbx)
 8063881:      	movq	%r13, 0x10(%rbx)
 8063885:      	movq	%rbx, %rax
 8063888:      	addq	$0x28, %rsp
 806388c:      	popq	%rbx
 806388d:      	popq	%r12
 806388f:      	popq	%r13
 8063891:      	popq	%r14
 8063893:      	popq	%r15
 8063895:      	popq	%rbp
 8063896:      	retq
