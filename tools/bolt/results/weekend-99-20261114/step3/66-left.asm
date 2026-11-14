
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000283a540 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE>:
 283a540:      	pushq	%rbp
 283a541:      	pushq	%r15
 283a543:      	pushq	%r14
 283a545:      	pushq	%r13
 283a547:      	pushq	%r12
 283a549:      	pushq	%rbx
 283a54a:      	subq	$0x58, %rsp
 283a54e:      	movq	%rcx, %r15
 283a551:      	movl	%edx, %r14d
 283a554:      	movq	%rsi, %r12
 283a557:      	movq	%rdi, %rbx
 283a55a:      	movl	$0x1, 0x20(%rsp)
 283a562:      	movq	$0x0, 0x18(%rsp)
 283a56b:      	leaq	0x18(%rsp), %rsi
 283a570:      	movq	%r8, %rdi
 283a573:      	callq	0x5df6560 <_ZN4llvm3ISD21isConstantSplatVectorEPKNS_6SDNodeERNS_5APIntE>
 283a578:      	testb	%al, %al
 283a57a:      	je	0x283a6f1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1b1>
 283a580:      	leaq	0x40(%rsp), %rdi
 283a585:      	movq	%rbx, %rsi
 283a588:      	movq	%r12, %rdx
 283a58b:      	movl	%r14d, %ecx
 283a58e:      	movq	%r15, %r8
 283a591:      	callq	0x3912b60 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
 283a596:      	cmpb	$0x0, 0x40(%rsp)
 283a59b:      	je	0x283a606 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xc6>
 283a59d:      	leaq	0x40(%rsp), %r13
 283a5a2:      	jmp	0x283a5ea <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xaa>
 283a5a4:      	nopw	%cs:(%rax,%rax)
 283a5ae:      	nop
 283a5b0:      	movq	%r13, %rdi
 283a5b3:      	movq	%rbx, %rsi
 283a5b6:      	movq	%r12, %rdx
 283a5b9:      	movl	%r14d, %ecx
 283a5bc:      	movq	%r15, %r8
 283a5bf:      	callq	0x3912b60 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
 283a5c4:      	movzwl	0x48(%rsp), %r14d
 283a5ca:      	movq	0x50(%rsp), %r15
 283a5cf:      	movq	%r13, %rdi
 283a5d2:      	movq	%rbx, %rsi
 283a5d5:      	movq	%r12, %rdx
 283a5d8:      	movl	%r14d, %ecx
 283a5db:      	movq	%r15, %r8
 283a5de:      	callq	0x3912b60 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
 283a5e3:      	cmpb	$0x0, 0x40(%rsp)
 283a5e8:      	je	0x283a606 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xc6>
 283a5ea:      	cmpw	$0x10, %r14w
 283a5ef:      	jne	0x283a5b0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x70>
 283a5f1:      	movq	%r12, %rdi
 283a5f4:      	movl	$0x60, %esi
 283a5f9:      	callq	0x3c203d0 <_ZN4llvm11IntegerType3getERNS_11LLVMContextEj>
 283a5fe:      	movq	%rax, %r15
 283a601:      	xorl	%r14d, %r14d
 283a604:      	jmp	0x283a5cf <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x8f>
 283a606:      	movzwl	%r14w, %r12d
 283a60a:      	testw	%r14w, %r14w
 283a60e:      	je	0x283a676 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x136>
 283a610:      	leal	-0x13(%r14), %eax
 283a614:      	movzwl	%ax, %eax
 283a617:      	cmpl	$0xc1, %eax
 283a61c:      	jae	0x283a698 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x158>
 283a61e:      	leaq	-0x1960d45(%rip), %rax  # 0xed98e0 <_ZZNK4llvm3MVT20getVectorElementTypeEvE10EltTyTable>
 283a625:      	movzwl	-0x2(%rax,%r12,2), %eax
 283a62b:      	xorl	%r15d, %r15d
 283a62e:      	testw	%ax, %ax
 283a631:      	jne	0x283a6a0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x160>
 283a633:      	movl	0x8(%r15), %eax
 283a637:      	movzbl	%al, %ecx
 283a63a:      	cmpl	$0xc, %ecx
 283a63d:      	setne	%dl
 283a640:      	testq	%r15, %r15
 283a643:      	sete	%sil
 283a647:      	orb	%dl, %sil
 283a64a:      	je	0x283a6f9 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1b9>
 283a650:      	testq	%r15, %r15
 283a653:      	sete	%al
 283a656:      	addl	$-0x13, %ecx
 283a659:      	cmpl	$-0x2, %ecx
 283a65c:      	setb	%cl
 283a65f:      	orb	%al, %cl
 283a661:      	jne	0x283a6b2 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x172>
 283a663:      	movq	%r15, %rdi
 283a666:      	callq	0x3c1ff30 <_ZNK4llvm4Type22getPrimitiveSizeInBitsEv>
 283a66b:      	testw	%r14w, %r14w
 283a66f:      	jne	0x283a6b8 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x178>
 283a671:      	jmp	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a676:      	movzbl	0x8(%r15), %eax
 283a67b:      	addl	$-0x11, %eax
 283a67e:      	cmpl	$0x2, %eax
 283a681:      	jae	0x283a698 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x158>
 283a683:      	movq	0x18(%r15), %rdi
 283a687:      	xorl	%esi, %esi
 283a689:      	callq	0x39f7ce0 <_ZN4llvm3EVT6getEVTEPNS_4TypeEb>
 283a68e:      	movq	%rdx, %r15
 283a691:      	testw	%ax, %ax
 283a694:      	jne	0x283a6a0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x160>
 283a696:      	jmp	0x283a633 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xf3>
 283a698:      	movl	%r14d, %eax
 283a69b:      	testw	%ax, %ax
 283a69e:      	je	0x283a633 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xf3>
 283a6a0:      	movzwl	%ax, %eax
 283a6a3:      	shll	$0x4, %eax
 283a6a6:      	leaq	-0x1960bad(%rip), %rcx  # 0xed9b00 <_ZZNK4llvm3MVT13getSizeInBitsEvE9SizeTable>
 283a6ad:      	movq	-0x10(%rax,%rcx), %rax
 283a6b2:      	testw	%r14w, %r14w
 283a6b6:      	je	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a6b8:      	cmpl	$0x1, %r12d
 283a6bc:      	je	0x283a6c6 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x186>
 283a6be:      	cmpq	$0x0, 0x68(%rbx,%r12,8)
 283a6c4:      	je	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a6c6:      	cmpl	$0x20, %eax
 283a6c9:      	ja	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a6cb:      	imulq	$0x207, %r12, %rcx      # imm = 0x207
 283a6d2:      	cmpb	$0x0, 0x1801(%rbx,%rcx)
 283a6da:      	jne	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a6dc:      	cmpl	$0x20, %eax
 283a6df:      	jne	0x283a6f1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1b1>
 283a6e1:      	movq	0x7a400(%rbx), %rax
 283a6e8:      	cmpb	$0x1, 0x1e7(%rax)
 283a6ef:      	je	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a6f1:      	xorl	%r12d, %r12d
 283a6f4:      	jmp	0x283ac57 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x717>
 283a6f9:      	shrl	$0x8, %eax
 283a6fc:      	testw	%r14w, %r14w
 283a700:      	jne	0x283a6b8 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x178>
 283a702:      	movl	0x20(%rsp), %r14d
 283a707:      	cmpq	$0x41, %r14
 283a70b:      	jae	0x283a793 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x253>
 283a711:      	movq	0x18(%rsp), %rdx
 283a716:      	movl	%r14d, %ecx
 283a719:      	negb	%cl
 283a71b:      	movq	$-0x1, %rax
 283a722:      	shrq	%cl, %rax
 283a725:      	leaq	0x1(%rdx), %rcx
 283a729:      	testq	%r14, %r14
 283a72c:      	cmoveq	%r14, %rax
 283a730:      	andq	%rax, %rcx
 283a733:      	popcntq	%rcx, %rsi
 283a738:      	movb	$0x1, %r12b
 283a73b:      	cmpl	$0x1, %esi
 283a73e:      	je	0x283ac57 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x717>
 283a744:      	leaq	-0x1(%rdx), %rsi
 283a748:      	andq	%rax, %rsi
 283a74b:      	popcntq	%rsi, %rsi
 283a750:      	cmpl	$0x1, %esi
 283a753:      	je	0x283ac57 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x717>
 283a759:      	notq	%rdx
 283a75c:      	andq	%rax, %rdx
 283a75f:      	incq	%rdx
 283a762:      	andq	%rax, %rdx
 283a765:      	incq	%rdx
 283a768:      	andq	%rax, %rdx
 283a76b:      	popcntq	%rdx, %rdx
 283a770:      	cmpl	$0x1, %edx
 283a773:      	je	0x283ac57 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x717>
 283a779:      	xorq	%rax, %rcx
 283a77c:      	incq	%rcx
 283a77f:      	andq	%rax, %rcx
 283a782:      	popcntq	%rcx, %rax
 283a787:      	cmpl	$0x1, %eax
 283a78a:      	sete	%r12b
 283a78e:      	jmp	0x283ac57 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x717>
 283a793:      	leaq	0x3f(%r14), %r15
 283a797:      	movq	%r15, %rbp
 283a79a:      	shrq	$0x3, %rbp
 283a79e:      	movq	%rbp, 0x38(%rsp)
 283a7a3:      	andl	$-0x8, %ebp
 283a7a6:      	movq	%rbp, %rdi
 283a7a9:      	callq	0x828a830 <_Znam@plt>
 283a7ae:      	movq	%rax, %rbx
 283a7b1:      	movq	0x18(%rsp), %rsi
 283a7b6:      	movq	%rax, %rdi
 283a7b9:      	movq	%rsi, 0x10(%rsp)
 283a7be:      	movq	%rbp, %rdx
 283a7c1:      	callq	0x828ace0 <memcpy@plt>
 283a7c6:      	shrq	$0x6, %r15
 283a7ca:      	incq	(%rbx)
 283a7cd:      	jne	0x283a7f0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2b0>
 283a7cf:      	leaq	-0x2(%r15), %rax
 283a7d3:      	xorl	%ecx, %ecx
 283a7d5:      	nopw	%cs:(%rax,%rax)
 283a7df:      	nop
 283a7e0:      	incq	0x8(%rbx,%rcx,8)
 283a7e5:      	jne	0x283a7f0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2b0>
 283a7e7:      	cmpq	%rcx, %rax
 283a7ea:      	leaq	0x1(%rcx), %rcx
 283a7ee:      	jne	0x283a7e0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2a0>
 283a7f0:      	movl	%r14d, %ecx
 283a7f3:      	negb	%cl
 283a7f5:      	movq	$-0x1, %r10
 283a7fc:      	shrq	%cl, %r10
 283a7ff:      	leal	-0x1(%r15), %r11d
 283a803:      	andq	%r10, (%rbx,%r11,8)
 283a807:      	leaq	-0x1(%r15), %r13
 283a80b:      	movl	%r15d, %eax
 283a80e:      	andl	$0x3, %eax
 283a811:      	cmpq	$0x3, %r13
 283a815:      	jae	0x283a81d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2dd>
 283a817:      	xorl	%edx, %edx
 283a819:      	xorl	%ecx, %ecx
 283a81b:      	jmp	0x283a864 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x324>
 283a81d:      	movl	%r15d, %esi
 283a820:      	andl	$-0x4, %esi
 283a823:      	xorl	%edx, %edx
 283a825:      	xorl	%ecx, %ecx
 283a827:      	nopw	(%rax,%rax)
 283a830:      	popcntq	(%rbx,%rdx,8), %rdi
 283a836:      	popcntq	0x8(%rbx,%rdx,8), %r8
 283a83d:      	popcntq	0x10(%rbx,%rdx,8), %r9
 283a844:      	addl	%ecx, %edi
 283a846:      	addl	%r8d, %r9d
 283a849:      	popcntq	0x18(%rbx,%rdx,8), %rcx
 283a850:      	addl	%edi, %r9d
 283a853:      	addl	%r9d, %ecx
 283a856:      	addq	$0x4, %rdx
 283a85a:      	cmpq	%rdx, %rsi
 283a85d:      	jne	0x283a830 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2f0>
 283a85f:      	testq	%rax, %rax
 283a862:      	je	0x283a880 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x340>
 283a864:      	leaq	(%rbx,%rdx,8), %rdx
 283a868:      	xorl	%esi, %esi
 283a86a:      	nopw	(%rax,%rax)
 283a870:      	popcntq	(%rdx,%rsi,8), %rdi
 283a876:      	addl	%edi, %ecx
 283a878:      	incq	%rsi
 283a87b:      	cmpq	%rsi, %rax
 283a87e:      	jne	0x283a870 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x330>
 283a880:      	movb	$0x1, %r12b
 283a883:      	cmpl	$0x1, %ecx
 283a886:      	je	0x283ac4f <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x70f>
 283a88c:      	movq	%r14, 0x30(%rsp)
 283a891:      	movq	%r11, (%rsp)
 283a895:      	movq	%r10, 0x8(%rsp)
 283a89a:      	movq	%rbp, %rdi
 283a89d:      	callq	0x828a830 <_Znam@plt>
 283a8a2:      	movq	%rax, %r14
 283a8a5:      	movq	%rax, %rdi
 283a8a8:      	movq	0x10(%rsp), %rsi
 283a8ad:      	movq	%rbp, 0x28(%rsp)
 283a8b2:      	movq	%rbp, %rdx
 283a8b5:      	callq	0x828ace0 <memcpy@plt>
 283a8ba:      	subq	$0x1, (%r14)
 283a8be:      	jae	0x283a8e1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3a1>
 283a8c0:      	leaq	-0x2(%r15), %rax
 283a8c4:      	xorl	%ecx, %ecx
 283a8c6:      	nopw	%cs:(%rax,%rax)
 283a8d0:      	addq	$-0x1, 0x8(%r14,%rcx,8)
 283a8d6:      	jb	0x283a8e1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3a1>
 283a8d8:      	cmpq	%rcx, %rax
 283a8db:      	leaq	0x1(%rcx), %rcx
 283a8df:      	jne	0x283a8d0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x390>
 283a8e1:      	movq	0x8(%rsp), %rax
 283a8e6:      	movq	(%rsp), %rcx
 283a8ea:      	andq	%rax, (%r14,%rcx,8)
 283a8ee:      	movl	%r15d, %ebp
 283a8f1:      	andl	$0x3, %ebp
 283a8f4:      	cmpl	$0x3, %r13d
 283a8f8:      	jae	0x283a900 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3c0>
 283a8fa:      	xorl	%ecx, %ecx
 283a8fc:      	xorl	%eax, %eax
 283a8fe:      	jmp	0x283a944 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x404>
 283a900:      	movl	%r15d, %edx
 283a903:      	andl	$-0x4, %edx
 283a906:      	xorl	%ecx, %ecx
 283a908:      	xorl	%eax, %eax
 283a90a:      	nopw	(%rax,%rax)
 283a910:      	popcntq	(%r14,%rcx,8), %rsi
 283a916:      	popcntq	0x8(%r14,%rcx,8), %rdi
 283a91d:      	popcntq	0x10(%r14,%rcx,8), %r8
 283a924:      	addl	%eax, %esi
 283a926:      	addl	%edi, %r8d
 283a929:      	popcntq	0x18(%r14,%rcx,8), %rax
 283a930:      	addl	%esi, %r8d
 283a933:      	addl	%r8d, %eax
 283a936:      	addq	$0x4, %rcx
 283a93a:      	cmpq	%rcx, %rdx
 283a93d:      	jne	0x283a910 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3d0>
 283a93f:      	testq	%rbp, %rbp
 283a942:      	je	0x283a960 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x420>
 283a944:      	leaq	(%r14,%rcx,8), %rcx
 283a948:      	xorl	%edx, %edx
 283a94a:      	nopw	(%rax,%rax)
 283a950:      	popcntq	(%rcx,%rdx,8), %rsi
 283a956:      	addl	%esi, %eax
 283a958:      	incq	%rdx
 283a95b:      	cmpq	%rdx, %rbp
 283a95e:      	jne	0x283a950 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x410>
 283a960:      	movb	$0x1, %r12b
 283a963:      	cmpl	$0x1, %eax
 283a966:      	je	0x283ac47 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x707>
 283a96c:      	movq	0x28(%rsp), %r12
 283a971:      	movq	%r12, %rdi
 283a974:      	callq	0x828a830 <_Znam@plt>
 283a979:      	movq	%rax, %r13
 283a97c:      	movq	%rax, %rdi
 283a97f:      	movq	0x10(%rsp), %rsi
 283a984:      	movq	%r12, %rdx
 283a987:      	callq	0x828ace0 <memcpy@plt>
 283a98c:      	cmpl	$0xc1, 0x30(%rsp)
 283a994:      	jae	0x283a9a3 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x463>
 283a996:      	xorl	%eax, %eax
 283a998:      	movq	0x8(%rsp), %rsi
 283a99d:      	movq	(%rsp), %rdi
 283a9a1:      	jmp	0x283aa00 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4c0>
 283a9a3:      	movl	%r15d, %eax
 283a9a6:      	andl	$-0x4, %eax
 283a9a9:      	movq	0x38(%rsp), %rcx
 283a9ae:      	andl	$-0x20, %ecx
 283a9b1:      	xorl	%edx, %edx
 283a9b3:      	pcmpeqd	%xmm0, %xmm0
 283a9b7:      	movq	0x8(%rsp), %rsi
 283a9bc:      	movq	(%rsp), %rdi
 283a9c0:      	movdqu	(%r13,%rdx), %xmm1
 283a9c7:      	movdqu	0x10(%r13,%rdx), %xmm2
 283a9ce:      	pxor	%xmm0, %xmm1
 283a9d2:      	pxor	%xmm0, %xmm2
 283a9d6:      	movdqu	%xmm1, (%r13,%rdx)
 283a9dd:      	movdqu	%xmm2, 0x10(%r13,%rdx)
 283a9e4:      	addq	$0x20, %rdx
 283a9e8:      	cmpq	%rdx, %rcx
 283a9eb:      	jne	0x283a9c0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x480>
 283a9ed:      	cmpl	%eax, %r15d
 283a9f0:      	je	0x283aa0d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4cd>
 283a9f2:      	nopw	%cs:(%rax,%rax)
 283a9fc:      	nopl	(%rax)
 283aa00:      	notq	(%r13,%rax,8)
 283aa05:      	incq	%rax
 283aa08:      	cmpq	%rax, %r15
 283aa0b:      	jne	0x283aa00 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4c0>
 283aa0d:      	andq	%rsi, (%r13,%rdi,8)
 283aa12:      	incq	(%r13)
 283aa16:      	jne	0x283aa30 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4f0>
 283aa18:      	leaq	-0x2(%r15), %rax
 283aa1c:      	xorl	%ecx, %ecx
 283aa1e:      	nop
 283aa20:      	incq	0x8(%r13,%rcx,8)
 283aa25:      	jne	0x283aa30 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4f0>
 283aa27:      	cmpq	%rcx, %rax
 283aa2a:      	leaq	0x1(%rcx), %rcx
 283aa2e:      	jne	0x283aa20 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4e0>
 283aa30:      	andq	%rsi, (%r13,%rdi,8)
 283aa35:      	incq	(%r13)
 283aa39:      	jne	0x283aa60 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x520>
 283aa3b:      	leaq	-0x2(%r15), %rax
 283aa3f:      	xorl	%ecx, %ecx
 283aa41:      	nopw	%cs:(%rax,%rax)
 283aa4b:      	nopl	(%rax,%rax)
 283aa50:      	incq	0x8(%r13,%rcx,8)
 283aa55:      	jne	0x283aa60 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x520>
 283aa57:      	cmpq	%rcx, %rax
 283aa5a:      	leaq	0x1(%rcx), %rcx
 283aa5e:      	jne	0x283aa50 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x510>
 283aa60:      	andq	%rsi, (%r13,%rdi,8)
 283aa65:      	leaq	-0x1(%r15), %rax
 283aa69:      	cmpl	$0x3, %eax
 283aa6c:      	jae	0x283aa74 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x534>
 283aa6e:      	xorl	%ecx, %ecx
 283aa70:      	xorl	%eax, %eax
 283aa72:      	jmp	0x283aab6 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x576>
 283aa74:      	movl	%r15d, %edx
 283aa77:      	andl	$-0x4, %edx
 283aa7a:      	xorl	%ecx, %ecx
 283aa7c:      	xorl	%eax, %eax
 283aa7e:      	nop
 283aa80:      	popcntq	(%r13,%rcx,8), %rsi
 283aa87:      	popcntq	0x8(%r13,%rcx,8), %rdi
 283aa8e:      	popcntq	0x10(%r13,%rcx,8), %r8
 283aa95:      	addl	%eax, %esi
 283aa97:      	addl	%edi, %r8d
 283aa9a:      	popcntq	0x18(%r13,%rcx,8), %rax
 283aaa1:      	addl	%esi, %r8d
 283aaa4:      	addl	%r8d, %eax
 283aaa7:      	addq	$0x4, %rcx
 283aaab:      	cmpq	%rcx, %rdx
 283aaae:      	jne	0x283aa80 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x540>
 283aab0:      	testb	$0x3, %r15b
 283aab4:      	je	0x283aad0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x590>
 283aab6:      	leaq	(%r13,%rcx,8), %rcx
 283aabb:      	xorl	%edx, %edx
 283aabd:      	nopl	(%rax)
 283aac0:      	popcntq	(%rcx,%rdx,8), %rsi
 283aac6:      	addl	%esi, %eax
 283aac8:      	incq	%rdx
 283aacb:      	cmpq	%rdx, %rbp
 283aace:      	jne	0x283aac0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x580>
 283aad0:      	movb	$0x1, %r12b
 283aad3:      	cmpl	$0x1, %eax
 283aad6:      	je	0x283ac3f <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6ff>
 283aadc:      	movq	0x28(%rsp), %r12
 283aae1:      	movq	%r12, %rdi
 283aae4:      	callq	0x828a830 <_Znam@plt>
 283aae9:      	movq	%rax, %rbp
 283aaec:      	movq	%rax, %rdi
 283aaef:      	movq	0x10(%rsp), %rsi
 283aaf4:      	movq	%r12, %rdx
 283aaf7:      	callq	0x828ace0 <memcpy@plt>
 283aafc:      	incq	(%rbp)
 283ab00:      	jne	0x283ab20 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5e0>
 283ab02:      	leaq	-0x2(%r15), %rax
 283ab06:      	xorl	%ecx, %ecx
 283ab08:      	nopl	(%rax,%rax)
 283ab10:      	incq	0x8(%rbp,%rcx,8)
 283ab15:      	jne	0x283ab20 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5e0>
 283ab17:      	cmpq	%rcx, %rax
 283ab1a:      	leaq	0x1(%rcx), %rcx
 283ab1e:      	jne	0x283ab10 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5d0>
 283ab20:      	movq	0x8(%rsp), %rdx
 283ab25:      	movq	(%rsp), %rdi
 283ab29:      	andq	%rdx, (%rbp,%rdi,8)
 283ab2e:      	cmpl	$0xc1, 0x30(%rsp)
 283ab36:      	movq	0x38(%rsp), %rsi
 283ab3b:      	jae	0x283ab41 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x601>
 283ab3d:      	xorl	%eax, %eax
 283ab3f:      	jmp	0x283ab80 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x640>
 283ab41:      	movl	%r15d, %eax
 283ab44:      	andl	$-0x4, %eax
 283ab47:      	andl	$-0x20, %esi
 283ab4a:      	xorl	%ecx, %ecx
 283ab4c:      	pcmpeqd	%xmm0, %xmm0
 283ab50:      	movdqu	(%rbp,%rcx), %xmm1
 283ab56:      	movdqu	0x10(%rbp,%rcx), %xmm2
 283ab5c:      	pxor	%xmm0, %xmm1
 283ab60:      	pxor	%xmm0, %xmm2
 283ab64:      	movdqu	%xmm1, (%rbp,%rcx)
 283ab6a:      	movdqu	%xmm2, 0x10(%rbp,%rcx)
 283ab70:      	addq	$0x20, %rcx
 283ab74:      	cmpq	%rcx, %rsi
 283ab77:      	jne	0x283ab50 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x610>
 283ab79:      	cmpl	%eax, %r15d
 283ab7c:      	je	0x283ab8d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x64d>
 283ab7e:      	nop
 283ab80:      	notq	(%rbp,%rax,8)
 283ab85:      	incq	%rax
 283ab88:      	cmpq	%rax, %r15
 283ab8b:      	jne	0x283ab80 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x640>
 283ab8d:      	andq	%rdx, (%rbp,%rdi,8)
 283ab92:      	incq	(%rbp)
 283ab96:      	jne	0x283abb0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x670>
 283ab98:      	leaq	-0x2(%r15), %rax
 283ab9c:      	xorl	%ecx, %ecx
 283ab9e:      	nop
 283aba0:      	incq	0x8(%rbp,%rcx,8)
 283aba5:      	jne	0x283abb0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x670>
 283aba7:      	cmpq	%rcx, %rax
 283abaa:      	leaq	0x1(%rcx), %rcx
 283abae:      	jne	0x283aba0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x660>
 283abb0:      	andq	%rdx, (%rbp,%rdi,8)
 283abb5:      	movl	%r15d, %eax
 283abb8:      	andl	$0x3, %eax
 283abbb:      	leaq	-0x1(%r15), %rcx
 283abbf:      	cmpl	$0x3, %ecx
 283abc2:      	jae	0x283abca <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x68a>
 283abc4:      	xorl	%edx, %edx
 283abc6:      	xorl	%ecx, %ecx
 283abc8:      	jmp	0x283ac15 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6d5>
 283abca:      	andl	$-0x4, %r15d
 283abce:      	xorl	%edx, %edx
 283abd0:      	xorl	%ecx, %ecx
 283abd2:      	nopw	%cs:(%rax,%rax)
 283abdc:      	nopl	(%rax)
 283abe0:      	popcntq	(%rbp,%rdx,8), %rsi
 283abe7:      	popcntq	0x8(%rbp,%rdx,8), %rdi
 283abee:      	popcntq	0x10(%rbp,%rdx,8), %r8
 283abf5:      	addl	%ecx, %esi
 283abf7:      	addl	%edi, %r8d
 283abfa:      	popcntq	0x18(%rbp,%rdx,8), %rcx
 283ac01:      	addl	%esi, %r8d
 283ac04:      	addl	%r8d, %ecx
 283ac07:      	addq	$0x4, %rdx
 283ac0b:      	cmpq	%rdx, %r15
 283ac0e:      	jne	0x283abe0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6a0>
 283ac10:      	testq	%rax, %rax
 283ac13:      	je	0x283ac30 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6f0>
 283ac15:      	leaq	(%rbp,%rdx,8), %rdx
 283ac1a:      	xorl	%esi, %esi
 283ac1c:      	nopl	(%rax)
 283ac20:      	popcntq	(%rdx,%rsi,8), %rdi
 283ac26:      	addl	%edi, %ecx
 283ac28:      	incq	%rsi
 283ac2b:      	cmpq	%rsi, %rax
 283ac2e:      	jne	0x283ac20 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6e0>
 283ac30:      	cmpl	$0x1, %ecx
 283ac33:      	sete	%r12b
 283ac37:      	movq	%rbp, %rdi
 283ac3a:      	callq	0x828a840 <_ZdaPv@plt>
 283ac3f:      	movq	%r13, %rdi
 283ac42:      	callq	0x828a840 <_ZdaPv@plt>
 283ac47:      	movq	%r14, %rdi
 283ac4a:      	callq	0x828a840 <_ZdaPv@plt>
 283ac4f:      	movq	%rbx, %rdi
 283ac52:      	callq	0x828a840 <_ZdaPv@plt>
 283ac57:      	cmpl	$0x41, 0x20(%rsp)
 283ac5c:      	jb	0x283ac6d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x72d>
 283ac5e:      	movq	0x18(%rsp), %rdi
 283ac63:      	testq	%rdi, %rdi
 283ac66:      	je	0x283ac6d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x72d>
 283ac68:      	callq	0x828a840 <_ZdaPv@plt>
 283ac6d:      	movl	%r12d, %eax
 283ac70:      	addq	$0x58, %rsp
 283ac74:      	popq	%rbx
 283ac75:      	popq	%r12
 283ac77:      	popq	%r13
 283ac79:      	popq	%r14
 283ac7b:      	popq	%r15
 283ac7d:      	popq	%rbp
 283ac7e:      	retq
