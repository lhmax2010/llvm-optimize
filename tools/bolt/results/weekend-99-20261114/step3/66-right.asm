
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

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
 283a55a:      	movl	$0x1, 0x28(%rsp)
 283a562:      	movq	$0x0, 0x20(%rsp)
 283a56b:      	leaq	0x20(%rsp), %rsi
 283a570:      	movq	%r8, %rdi
 283a573:      	callq	0x5df64e0 <_ZN4llvm3ISD21isConstantSplatVectorEPKNS_6SDNodeERNS_5APIntE>
 283a578:      	testb	%al, %al
 283a57a:      	je	0x283a6f1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1b1>
 283a580:      	leaq	0x40(%rsp), %rdi
 283a585:      	movq	%rbx, %rsi
 283a588:      	movq	%r12, %rdx
 283a58b:      	movl	%r14d, %ecx
 283a58e:      	movq	%r15, %r8
 283a591:      	callq	0x3912ad0 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
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
 283a5bf:      	callq	0x3912ad0 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
 283a5c4:      	movzwl	0x48(%rsp), %r14d
 283a5ca:      	movq	0x50(%rsp), %r15
 283a5cf:      	movq	%r13, %rdi
 283a5d2:      	movq	%rbx, %rsi
 283a5d5:      	movq	%r12, %rdx
 283a5d8:      	movl	%r14d, %ecx
 283a5db:      	movq	%r15, %r8
 283a5de:      	callq	0x3912ad0 <_ZNK4llvm18TargetLoweringBase17getTypeConversionERNS_11LLVMContextENS_3EVTE>
 283a5e3:      	cmpb	$0x0, 0x40(%rsp)
 283a5e8:      	je	0x283a606 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0xc6>
 283a5ea:      	cmpw	$0x10, %r14w
 283a5ef:      	jne	0x283a5b0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x70>
 283a5f1:      	movq	%r12, %rdi
 283a5f4:      	movl	$0x60, %esi
 283a5f9:      	callq	0x3c20350 <_ZN4llvm11IntegerType3getERNS_11LLVMContextEj>
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
 283a666:      	callq	0x3c1feb0 <_ZNK4llvm4Type22getPrimitiveSizeInBitsEv>
 283a66b:      	testw	%r14w, %r14w
 283a66f:      	jne	0x283a6b8 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x178>
 283a671:      	jmp	0x283a702 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x1c2>
 283a676:      	movzbl	0x8(%r15), %eax
 283a67b:      	addl	$-0x11, %eax
 283a67e:      	cmpl	$0x2, %eax
 283a681:      	jae	0x283a698 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x158>
 283a683:      	movq	0x18(%r15), %rdi
 283a687:      	xorl	%esi, %esi
 283a689:      	callq	0x39f7c50 <_ZN4llvm3EVT6getEVTEPNS_4TypeEb>
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
 283a6f4:      	jmp	0x283ac77 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x737>
 283a6f9:      	shrl	$0x8, %eax
 283a6fc:      	testw	%r14w, %r14w
 283a700:      	jne	0x283a6b8 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x178>
 283a702:      	movl	0x28(%rsp), %r14d
 283a707:      	cmpq	$0x41, %r14
 283a70b:      	jae	0x283a793 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x253>
 283a711:      	movq	0x20(%rsp), %rdx
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
 283a73e:      	je	0x283ac77 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x737>
 283a744:      	leaq	-0x1(%rdx), %rsi
 283a748:      	andq	%rax, %rsi
 283a74b:      	popcntq	%rsi, %rsi
 283a750:      	cmpl	$0x1, %esi
 283a753:      	je	0x283ac77 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x737>
 283a759:      	notq	%rdx
 283a75c:      	andq	%rax, %rdx
 283a75f:      	incq	%rdx
 283a762:      	andq	%rax, %rdx
 283a765:      	incq	%rdx
 283a768:      	andq	%rax, %rdx
 283a76b:      	popcntq	%rdx, %rdx
 283a770:      	cmpl	$0x1, %edx
 283a773:      	je	0x283ac77 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x737>
 283a779:      	xorq	%rax, %rcx
 283a77c:      	incq	%rcx
 283a77f:      	andq	%rax, %rcx
 283a782:      	popcntq	%rcx, %rax
 283a787:      	cmpl	$0x1, %eax
 283a78a:      	sete	%r12b
 283a78e:      	jmp	0x283ac77 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x737>
 283a793:      	leaq	0x3f(%r14), %r15
 283a797:      	movq	%r15, %r12
 283a79a:      	shrq	$0x3, %r12
 283a79e:      	movq	%r12, 0x38(%rsp)
 283a7a3:      	andl	$-0x8, %r12d
 283a7a7:      	movq	%r12, %rdi
 283a7aa:      	callq	0x828a7a0 <_Znam@plt>
 283a7af:      	movq	%rax, %rbx
 283a7b2:      	movq	0x20(%rsp), %rsi
 283a7b7:      	movq	%rax, %rdi
 283a7ba:      	movq	%rsi, 0x10(%rsp)
 283a7bf:      	movq	%r12, 0x18(%rsp)
 283a7c4:      	movq	%r12, %rdx
 283a7c7:      	callq	0x828ac50 <memcpy@plt>
 283a7cc:      	shrq	$0x6, %r15
 283a7d0:      	incq	(%rbx)
 283a7d3:      	jne	0x283a7f0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2b0>
 283a7d5:      	leaq	-0x2(%r15), %rax
 283a7d9:      	xorl	%ecx, %ecx
 283a7db:      	nopl	(%rax,%rax)
 283a7e0:      	incq	0x8(%rbx,%rcx,8)
 283a7e5:      	jne	0x283a7f0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2b0>
 283a7e7:      	cmpq	%rcx, %rax
 283a7ea:      	leaq	0x1(%rcx), %rcx
 283a7ee:      	jne	0x283a7e0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x2a0>
 283a7f0:      	movl	%r14d, %ecx
 283a7f3:      	negb	%cl
 283a7f5:      	movq	$-0x1, %rbp
 283a7fc:      	shrq	%cl, %rbp
 283a7ff:      	leal	-0x1(%r15), %r10d
 283a803:      	andq	%rbp, (%rbx,%r10,8)
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
 283a886:      	je	0x283ac6f <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x72f>
 283a88c:      	movq	%r14, 0x30(%rsp)
 283a891:      	movq	%r10, (%rsp)
 283a895:      	movq	0x18(%rsp), %r12
 283a89a:      	movq	%r12, %rdi
 283a89d:      	callq	0x828a7a0 <_Znam@plt>
 283a8a2:      	movq	%rax, %r14
 283a8a5:      	movq	%rax, %rdi
 283a8a8:      	movq	0x10(%rsp), %rsi
 283a8ad:      	movq	%r12, %rdx
 283a8b0:      	callq	0x828ac50 <memcpy@plt>
 283a8b5:      	subq	$0x1, (%r14)
 283a8b9:      	jae	0x283a8e1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3a1>
 283a8bb:      	leaq	-0x2(%r15), %rax
 283a8bf:      	xorl	%ecx, %ecx
 283a8c1:      	nopw	%cs:(%rax,%rax)
 283a8cb:      	nopl	(%rax,%rax)
 283a8d0:      	addq	$-0x1, 0x8(%r14,%rcx,8)
 283a8d6:      	jb	0x283a8e1 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3a1>
 283a8d8:      	cmpq	%rcx, %rax
 283a8db:      	leaq	0x1(%rcx), %rcx
 283a8df:      	jne	0x283a8d0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x390>
 283a8e1:      	movq	(%rsp), %rax
 283a8e5:      	andq	%rbp, (%r14,%rax,8)
 283a8e9:      	movl	%r15d, %eax
 283a8ec:      	andl	$0x3, %eax
 283a8ef:      	cmpl	$0x3, %r13d
 283a8f3:      	jae	0x283a8fb <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3bb>
 283a8f5:      	xorl	%edx, %edx
 283a8f7:      	xorl	%ecx, %ecx
 283a8f9:      	jmp	0x283a944 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x404>
 283a8fb:      	movl	%r15d, %esi
 283a8fe:      	andl	$-0x4, %esi
 283a901:      	xorl	%edx, %edx
 283a903:      	xorl	%ecx, %ecx
 283a905:      	nopw	%cs:(%rax,%rax)
 283a90f:      	nop
 283a910:      	popcntq	(%r14,%rdx,8), %rdi
 283a916:      	popcntq	0x8(%r14,%rdx,8), %r8
 283a91d:      	popcntq	0x10(%r14,%rdx,8), %r9
 283a924:      	addl	%ecx, %edi
 283a926:      	addl	%r8d, %r9d
 283a929:      	popcntq	0x18(%r14,%rdx,8), %rcx
 283a930:      	addl	%edi, %r9d
 283a933:      	addl	%r9d, %ecx
 283a936:      	addq	$0x4, %rdx
 283a93a:      	cmpq	%rdx, %rsi
 283a93d:      	jne	0x283a910 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x3d0>
 283a93f:      	testq	%rax, %rax
 283a942:      	je	0x283a960 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x420>
 283a944:      	leaq	(%r14,%rdx,8), %rdx
 283a948:      	xorl	%esi, %esi
 283a94a:      	nopw	(%rax,%rax)
 283a950:      	popcntq	(%rdx,%rsi,8), %rdi
 283a956:      	addl	%edi, %ecx
 283a958:      	incq	%rsi
 283a95b:      	cmpq	%rsi, %rax
 283a95e:      	jne	0x283a950 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x410>
 283a960:      	movb	$0x1, %r12b
 283a963:      	cmpl	$0x1, %ecx
 283a966:      	je	0x283ac67 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x727>
 283a96c:      	movq	0x18(%rsp), %r12
 283a971:      	movq	%r12, %rdi
 283a974:      	callq	0x828a7a0 <_Znam@plt>
 283a979:      	movq	%rax, %r13
 283a97c:      	movq	%rax, %rdi
 283a97f:      	movq	0x10(%rsp), %rsi
 283a984:      	movq	%r12, %rdx
 283a987:      	callq	0x828ac50 <memcpy@plt>
 283a98c:      	cmpl	$0xc1, 0x30(%rsp)
 283a994:      	jae	0x283a99e <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x45e>
 283a996:      	xorl	%eax, %eax
 283a998:      	movq	(%rsp), %rsi
 283a99c:      	jmp	0x283aa00 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x4c0>
 283a99e:      	movl	%r15d, %eax
 283a9a1:      	andl	$-0x4, %eax
 283a9a4:      	movq	0x38(%rsp), %rcx
 283a9a9:      	andl	$-0x20, %ecx
 283a9ac:      	xorl	%edx, %edx
 283a9ae:      	pcmpeqd	%xmm0, %xmm0
 283a9b2:      	movq	(%rsp), %rsi
 283a9b6:      	nopw	%cs:(%rax,%rax)
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
 283aa0d:      	andq	%rbp, (%r13,%rsi,8)
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
 283aa30:      	andq	%rbp, (%r13,%rsi,8)
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
 283aa60:      	andq	%rbp, (%r13,%rsi,8)
 283aa65:      	movl	%r15d, %eax
 283aa68:      	andl	$0x3, %eax
 283aa6b:      	leaq	-0x1(%r15), %rcx
 283aa6f:      	cmpl	$0x3, %ecx
 283aa72:      	jae	0x283aa7a <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x53a>
 283aa74:      	xorl	%edx, %edx
 283aa76:      	xorl	%ecx, %ecx
 283aa78:      	jmp	0x283aac5 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x585>
 283aa7a:      	movl	%r15d, %esi
 283aa7d:      	andl	$-0x4, %esi
 283aa80:      	xorl	%edx, %edx
 283aa82:      	xorl	%ecx, %ecx
 283aa84:      	nopw	%cs:(%rax,%rax)
 283aa8e:      	nop
 283aa90:      	popcntq	(%r13,%rdx,8), %rdi
 283aa97:      	popcntq	0x8(%r13,%rdx,8), %r8
 283aa9e:      	popcntq	0x10(%r13,%rdx,8), %r9
 283aaa5:      	addl	%ecx, %edi
 283aaa7:      	addl	%r8d, %r9d
 283aaaa:      	popcntq	0x18(%r13,%rdx,8), %rcx
 283aab1:      	addl	%edi, %r9d
 283aab4:      	addl	%r9d, %ecx
 283aab7:      	addq	$0x4, %rdx
 283aabb:      	cmpq	%rdx, %rsi
 283aabe:      	jne	0x283aa90 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x550>
 283aac0:      	testq	%rax, %rax
 283aac3:      	je	0x283aae0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5a0>
 283aac5:      	leaq	(%r13,%rdx,8), %rdx
 283aaca:      	xorl	%esi, %esi
 283aacc:      	nopl	(%rax)
 283aad0:      	popcntq	(%rdx,%rsi,8), %rdi
 283aad6:      	addl	%edi, %ecx
 283aad8:      	incq	%rsi
 283aadb:      	cmpq	%rsi, %rax
 283aade:      	jne	0x283aad0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x590>
 283aae0:      	movb	$0x1, %r12b
 283aae3:      	cmpl	$0x1, %ecx
 283aae6:      	je	0x283ac5f <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x71f>
 283aaec:      	movq	%rbp, 0x8(%rsp)
 283aaf1:      	movq	0x18(%rsp), %r12
 283aaf6:      	movq	%r12, %rdi
 283aaf9:      	callq	0x828a7a0 <_Znam@plt>
 283aafe:      	movq	%rax, %rbp
 283ab01:      	movq	%rax, %rdi
 283ab04:      	movq	0x10(%rsp), %rsi
 283ab09:      	movq	%r12, %rdx
 283ab0c:      	callq	0x828ac50 <memcpy@plt>
 283ab11:      	incq	(%rbp)
 283ab15:      	jne	0x283ab30 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5f0>
 283ab17:      	leaq	-0x2(%r15), %rax
 283ab1b:      	xorl	%ecx, %ecx
 283ab1d:      	nopl	(%rax)
 283ab20:      	incq	0x8(%rbp,%rcx,8)
 283ab25:      	jne	0x283ab30 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5f0>
 283ab27:      	cmpq	%rcx, %rax
 283ab2a:      	leaq	0x1(%rcx), %rcx
 283ab2e:      	jne	0x283ab20 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x5e0>
 283ab30:      	movq	(%rsp), %rsi
 283ab34:      	movq	0x8(%rsp), %rax
 283ab39:      	andq	%rax, (%rbp,%rsi,8)
 283ab3e:      	cmpl	$0xc1, 0x30(%rsp)
 283ab46:      	movq	0x38(%rsp), %rdx
 283ab4b:      	jae	0x283ab51 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x611>
 283ab4d:      	xorl	%eax, %eax
 283ab4f:      	jmp	0x283ab90 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x650>
 283ab51:      	movl	%r15d, %eax
 283ab54:      	andl	$-0x4, %eax
 283ab57:      	andl	$-0x20, %edx
 283ab5a:      	xorl	%ecx, %ecx
 283ab5c:      	pcmpeqd	%xmm0, %xmm0
 283ab60:      	movdqu	(%rbp,%rcx), %xmm1
 283ab66:      	movdqu	0x10(%rbp,%rcx), %xmm2
 283ab6c:      	pxor	%xmm0, %xmm1
 283ab70:      	pxor	%xmm0, %xmm2
 283ab74:      	movdqu	%xmm1, (%rbp,%rcx)
 283ab7a:      	movdqu	%xmm2, 0x10(%rbp,%rcx)
 283ab80:      	addq	$0x20, %rcx
 283ab84:      	cmpq	%rcx, %rdx
 283ab87:      	jne	0x283ab60 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x620>
 283ab89:      	cmpl	%eax, %r15d
 283ab8c:      	je	0x283ab9d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x65d>
 283ab8e:      	nop
 283ab90:      	notq	(%rbp,%rax,8)
 283ab95:      	incq	%rax
 283ab98:      	cmpq	%rax, %r15
 283ab9b:      	jne	0x283ab90 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x650>
 283ab9d:      	movq	0x8(%rsp), %rax
 283aba2:      	andq	%rax, (%rbp,%rsi,8)
 283aba7:      	incq	(%rbp)
 283abab:      	jne	0x283abd0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x690>
 283abad:      	leaq	-0x2(%r15), %rax
 283abb1:      	xorl	%ecx, %ecx
 283abb3:      	nopw	%cs:(%rax,%rax)
 283abbd:      	nopl	(%rax)
 283abc0:      	incq	0x8(%rbp,%rcx,8)
 283abc5:      	jne	0x283abd0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x690>
 283abc7:      	cmpq	%rcx, %rax
 283abca:      	leaq	0x1(%rcx), %rcx
 283abce:      	jne	0x283abc0 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x680>
 283abd0:      	movq	0x8(%rsp), %rax
 283abd5:      	andq	%rax, (%rbp,%rsi,8)
 283abda:      	movl	%r15d, %eax
 283abdd:      	andl	$0x3, %eax
 283abe0:      	leaq	-0x1(%r15), %rcx
 283abe4:      	cmpl	$0x3, %ecx
 283abe7:      	jae	0x283abef <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6af>
 283abe9:      	xorl	%edx, %edx
 283abeb:      	xorl	%ecx, %ecx
 283abed:      	jmp	0x283ac35 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6f5>
 283abef:      	andl	$-0x4, %r15d
 283abf3:      	xorl	%edx, %edx
 283abf5:      	xorl	%ecx, %ecx
 283abf7:      	nopw	(%rax,%rax)
 283ac00:      	popcntq	(%rbp,%rdx,8), %rsi
 283ac07:      	popcntq	0x8(%rbp,%rdx,8), %rdi
 283ac0e:      	popcntq	0x10(%rbp,%rdx,8), %r8
 283ac15:      	addl	%ecx, %esi
 283ac17:      	addl	%edi, %r8d
 283ac1a:      	popcntq	0x18(%rbp,%rdx,8), %rcx
 283ac21:      	addl	%esi, %r8d
 283ac24:      	addl	%r8d, %ecx
 283ac27:      	addq	$0x4, %rdx
 283ac2b:      	cmpq	%rdx, %r15
 283ac2e:      	jne	0x283ac00 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x6c0>
 283ac30:      	testq	%rax, %rax
 283ac33:      	je	0x283ac50 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x710>
 283ac35:      	leaq	(%rbp,%rdx,8), %rdx
 283ac3a:      	xorl	%esi, %esi
 283ac3c:      	nopl	(%rax)
 283ac40:      	popcntq	(%rdx,%rsi,8), %rdi
 283ac46:      	addl	%edi, %ecx
 283ac48:      	incq	%rsi
 283ac4b:      	cmpq	%rsi, %rax
 283ac4e:      	jne	0x283ac40 <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x700>
 283ac50:      	cmpl	$0x1, %ecx
 283ac53:      	sete	%r12b
 283ac57:      	movq	%rbp, %rdi
 283ac5a:      	callq	0x828a7b0 <_ZdaPv@plt>
 283ac5f:      	movq	%r13, %rdi
 283ac62:      	callq	0x828a7b0 <_ZdaPv@plt>
 283ac67:      	movq	%r14, %rdi
 283ac6a:      	callq	0x828a7b0 <_ZdaPv@plt>
 283ac6f:      	movq	%rbx, %rdi
 283ac72:      	callq	0x828a7b0 <_ZdaPv@plt>
 283ac77:      	cmpl	$0x41, 0x28(%rsp)
 283ac7c:      	jb	0x283ac8d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x74d>
 283ac7e:      	movq	0x20(%rsp), %rdi
 283ac83:      	testq	%rdi, %rdi
 283ac86:      	je	0x283ac8d <_ZNK4llvm17X86TargetLowering22decomposeMulByConstantERNS_11LLVMContextENS_3EVTENS_7SDValueE+0x74d>
 283ac88:      	callq	0x828a7b0 <_ZdaPv@plt>
 283ac8d:      	movl	%r12d, %eax
 283ac90:      	addq	$0x58, %rsp
 283ac94:      	popq	%rbx
 283ac95:      	popq	%r12
 283ac97:      	popq	%r13
 283ac99:      	popq	%r14
 283ac9b:      	popq	%r15
 283ac9d:      	popq	%rbp
 283ac9e:      	retq
