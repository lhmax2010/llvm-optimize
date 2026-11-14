
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bd74c0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv>:
 3bd74c0:      	pushq	%rbp
 3bd74c1:      	pushq	%r15
 3bd74c3:      	pushq	%r14
 3bd74c5:      	pushq	%r13
 3bd74c7:      	pushq	%r12
 3bd74c9:      	pushq	%rbx
 3bd74ca:      	subq	$0x58, %rsp
 3bd74ce:      	movq	%rdi, 0x10(%rsp)
 3bd74d3:      	leaq	0x28(%rsp), %rax
 3bd74d8:      	movq	%rax, 0x18(%rsp)
 3bd74dd:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd74e7:      	movq	%r14, 0x20(%rsp)
 3bd74ec:      	movl	0x10(%rsi), %edi
 3bd74ef:      	leaq	0x18(%rsi), %rax
 3bd74f3:      	testb	$0x1, %dil
 3bd74f7:      	cmoveq	0x18(%rsi), %rax
 3bd74fc:      	movl	$0x4, %ecx
 3bd7501:      	movq	%rsi, 0x8(%rsp)
 3bd7506:      	cmovel	0x20(%rsi), %ecx
 3bd750a:      	leaq	(,%rcx,8), %rdx
 3bd7512:      	leaq	(%rdx,%rdx,2), %rdx
 3bd7516:      	leaq	(%rax,%rdx), %r13
 3bd751a:      	movq	%r13, %rbp
 3bd751d:      	cmpl	$0x2, %edi
 3bd7520:      	jb	0x3bd755a <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd7522:      	movq	%rax, %rbp
 3bd7525:      	testq	%rcx, %rcx
 3bd7528:      	je	0x3bd755a <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd752a:      	movl	$0x1000, %esi           # imm = 0x1000
 3bd752f:      	movq	%rax, %rbp
 3bd7532:      	nopw	%cs:(%rax,%rax)
 3bd753c:      	nopl	(%rax)
 3bd7540:      	movq	(%rbp), %rdi
 3bd7544:      	orq	%rsi, %rdi
 3bd7547:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 3bd754e:      	jne	0x3bd755a <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd7550:      	addq	$0x18, %rbp
 3bd7554:      	addq	$-0x18, %rdx
 3bd7558:      	jne	0x3bd7540 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x80>
 3bd755a:      	leaq	(%rcx,%rcx,2), %rcx
 3bd755e:      	leaq	(%rax,%rcx,8), %r15
 3bd7562:      	cmpq	%r15, %rbp
 3bd7565:      	je	0x3bd7679 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1b9>
 3bd756b:      	addq	$0x10, 0x8(%rsp)
 3bd7571:      	xorl	%r12d, %r12d
 3bd7574:      	movl	$0x1000, %r14d          # imm = 0x1000
 3bd757a:      	jmp	0x3bd7589 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc9>
 3bd757c:      	nopl	(%rax)
 3bd7580:      	cmpq	%r15, %rbp
 3bd7583:      	je	0x3bd761d <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x15d>
 3bd7589:      	movq	0x8(%rbp), %rax
 3bd758d:      	cmpq	$0x4, %rax
 3bd7591:      	setb	%cl
 3bd7594:      	andl	$0x3, %eax
 3bd7597:      	cmpl	$0x2, %eax
 3bd759a:      	setne	%al
 3bd759d:      	orb	%cl, %al
 3bd759f:      	jne	0x3bd75e0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x120>
 3bd75a1:      	movq	(%rbp), %rsi
 3bd75a5:      	movq	0x8(%rsp), %rdi
 3bd75aa:      	callq	0x3beb290 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPvSt4pairINS_12PointerUnionIJPNS_15MetadataAsValueEPNS_8MetadataEPNS_14DebugValueUserEEEEmELj4ENS_12DenseMapInfoIS2_vEENS_6detail12DenseMapPairIS2_SC_EEEES2_SC_SE_SH_E24lookupOrInsertIntoBucketIRKS2_JEEES3_IPSH_bEOT_DpOT0_>
 3bd75af:      	movl	0x20(%rsp), %edx
 3bd75b3:      	cmpl	0x24(%rsp), %edx
 3bd75b7:      	jae	0x3bd75fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x13a>
 3bd75b9:      	addq	$0x8, %rax
 3bd75bd:      	movq	0x18(%rsp), %rcx
 3bd75c2:      	movl	%edx, %edx
 3bd75c4:      	movq	%rax, (%rcx,%rdx,8)
 3bd75c8:      	movl	0x20(%rsp), %r12d
 3bd75cd:      	incl	%r12d
 3bd75d0:      	movl	%r12d, 0x20(%rsp)
 3bd75d5:      	nopw	%cs:(%rax,%rax)
 3bd75df:      	nop
 3bd75e0:      	addq	$0x18, %rbp
 3bd75e4:      	cmpq	%r13, %rbp
 3bd75e7:      	je	0x3bd7580 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc0>
 3bd75e9:      	movq	(%rbp), %rax
 3bd75ed:      	orq	%r14, %rax
 3bd75f0:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 3bd75f6:      	je	0x3bd75e0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x120>
 3bd75f8:      	jmp	0x3bd7580 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc0>
 3bd75fa:      	incq	%rdx
 3bd75fd:      	movl	$0x8, %ecx
 3bd7602:      	leaq	0x18(%rsp), %rdi
 3bd7607:      	leaq	0x28(%rsp), %rsi
 3bd760c:      	movq	%rax, %r12
 3bd760f:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd7614:      	movq	%r12, %rax
 3bd7617:      	movl	0x20(%rsp), %edx
 3bd761b:      	jmp	0x3bd75b9 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xf9>
 3bd761d:      	testl	%r12d, %r12d
 3bd7620:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd762a:      	je	0x3bd7679 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1b9>
 3bd762c:      	movq	0x18(%rsp), %r15
 3bd7631:      	movl	%r12d, %eax
 3bd7634:      	leaq	(%r15,%rax,8), %rbp
 3bd7638:      	bsrq	%rax, %rdx
 3bd763c:      	xorl	$0x3f, %edx
 3bd763f:      	addl	%edx, %edx
 3bd7641:      	xorq	$0x7e, %rdx
 3bd7645:      	movq	%r15, %rdi
 3bd7648:      	movq	%rbp, %rsi
 3bd764b:      	callq	0x3bebcb0 <_ZSt16__introsort_loopIPPSt4pairIN4llvm12PointerUnionIJPNS1_15MetadataAsValueEPNS1_8MetadataEPNS1_14DebugValueUserEEEEmElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEvE3$_0EEEvT_SJ_T0_T1_>
 3bd7650:      	leaq	0x8(%r15), %rbx
 3bd7654:      	cmpl	$0x11, %r12d
 3bd7658:      	jb	0x3bd766f <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1af>
 3bd765a:      	movq	%rbp, 0x8(%rsp)
 3bd765f:      	movl	$0x8, %ebp
 3bd7664:      	movq	%rbx, %r12
 3bd7667:      	movq	%r15, %r14
 3bd766a:      	jmp	0x3bd77e7 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x327>
 3bd766f:      	cmpl	$0x1, %r12d
 3bd7673:      	jne	0x3bd772d <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x26d>
 3bd7679:      	movq	0x10(%rsp), %rbx
 3bd767e:      	leaq	0x10(%rbx), %r15
 3bd7682:      	movq	%r15, (%rbx)
 3bd7685:      	movq	%r14, 0x8(%rbx)
 3bd7689:      	movq	0x18(%rsp), %rdi
 3bd768e:      	movl	0x20(%rsp), %r14d
 3bd7693:      	testq	%r14, %r14
 3bd7696:      	je	0x3bd770c <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x24c>
 3bd7698:      	shlq	$0x3, %r14
 3bd769c:      	xorl	%eax, %eax
 3bd769e:      	xorl	%r12d, %r12d
 3bd76a1:      	nopw	%cs:(%rax,%rax)
 3bd76ab:      	nopl	(%rax,%rax)
 3bd76b0:      	movq	(%rdi,%r12), %rcx
 3bd76b4:      	movq	(%rcx), %r13
 3bd76b7:      	cmpl	0xc(%rbx), %eax
 3bd76ba:      	jae	0x3bd76e0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x220>
 3bd76bc:      	andq	$-0x4, %r13
 3bd76c0:      	movq	(%rbx), %rcx
 3bd76c3:      	movl	%eax, %eax
 3bd76c5:      	addq	$-0x28, %r13
 3bd76c9:      	movq	%r13, (%rcx,%rax,8)
 3bd76cd:      	movl	0x8(%rbx), %eax
 3bd76d0:      	incl	%eax
 3bd76d2:      	movl	%eax, 0x8(%rbx)
 3bd76d5:      	addq	$0x8, %r12
 3bd76d9:      	cmpq	%r12, %r14
 3bd76dc:      	jne	0x3bd76b0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1f0>
 3bd76de:      	jmp	0x3bd7707 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x247>
 3bd76e0:      	movl	%eax, %edx
 3bd76e2:      	incq	%rdx
 3bd76e5:      	movl	$0x8, %ecx
 3bd76ea:      	movq	%rdi, %rbp
 3bd76ed:      	movq	0x10(%rsp), %rdi
 3bd76f2:      	movq	%r15, %rsi
 3bd76f5:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd76fa:      	movq	%rbp, %rdi
 3bd76fd:      	movq	0x10(%rsp), %rbx
 3bd7702:      	movl	0x8(%rbx), %eax
 3bd7705:      	jmp	0x3bd76bc <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1fc>
 3bd7707:      	movq	0x18(%rsp), %rdi
 3bd770c:      	leaq	0x28(%rsp), %rax
 3bd7711:      	cmpq	%rax, %rdi
 3bd7714:      	je	0x3bd771b <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x25b>
 3bd7716:      	callq	0x828a6d0 <free@plt>
 3bd771b:      	movq	%rbx, %rax
 3bd771e:      	addq	$0x58, %rsp
 3bd7722:      	popq	%rbx
 3bd7723:      	popq	%r12
 3bd7725:      	popq	%r13
 3bd7727:      	popq	%r14
 3bd7729:      	popq	%r15
 3bd772b:      	popq	%rbp
 3bd772c:      	retq
 3bd772d:      	movq	%r15, %r12
 3bd7730:      	jmp	0x3bd777a <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2ba>
 3bd7732:      	nopw	%cs:(%rax,%rax)
 3bd773c:      	nopl	(%rax)
 3bd7740:      	movq	%r12, %rdx
 3bd7743:      	subq	%r15, %rdx
 3bd7746:      	movq	%rdx, %rax
 3bd7749:      	sarq	$0x3, %rax
 3bd774d:      	cmpq	$0x2, %rax
 3bd7751:      	jl	0x3bd77b3 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2f3>
 3bd7753:      	shlq	$0x3, %rax
 3bd7757:      	subq	%rax, %rdi
 3bd775a:      	addq	$0x10, %rdi
 3bd775e:      	movq	%r15, %rsi
 3bd7761:      	callq	0x828ac50 <memmove@plt>
 3bd7766:      	movq	%r15, %rax
 3bd7769:      	movq	%r13, (%rax)
 3bd776c:      	leaq	0x8(%r12), %rbx
 3bd7771:      	cmpq	%rbp, %rbx
 3bd7774:      	je	0x3bd7679 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1b9>
 3bd777a:      	movq	%r12, %rdi
 3bd777d:      	movq	%rbx, %r12
 3bd7780:      	movq	(%rbx), %r13
 3bd7783:      	movq	(%r15), %rsi
 3bd7786:      	movq	0x8(%r13), %rcx
 3bd778a:      	cmpq	0x8(%rsi), %rcx
 3bd778e:      	ja	0x3bd7740 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x280>
 3bd7790:      	movq	(%rdi), %rdx
 3bd7793:      	movq	%r12, %rax
 3bd7796:      	cmpq	0x8(%rdx), %rcx
 3bd779a:      	jbe	0x3bd7769 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd779c:      	movq	%r12, %rax
 3bd779f:      	nop
 3bd77a0:      	movq	%rdx, (%rax)
 3bd77a3:      	movq	-0x10(%rax), %rdx
 3bd77a7:      	addq	$-0x8, %rax
 3bd77ab:      	cmpq	0x8(%rdx), %rcx
 3bd77af:      	ja	0x3bd77a0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2e0>
 3bd77b1:      	jmp	0x3bd7769 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd77b3:      	movq	%r15, %rax
 3bd77b6:      	cmpq	$0x8, %rdx
 3bd77ba:      	jne	0x3bd7769 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd77bc:      	movq	%rsi, 0x8(%rdi)
 3bd77c0:      	jmp	0x3bd7766 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a6>
 3bd77c2:      	movq	%rdx, 0x8(%rcx)
 3bd77c6:      	nopw	%cs:(%rax,%rax)
 3bd77d0:      	movq	%r15, %rcx
 3bd77d3:      	movq	%r13, (%rcx)
 3bd77d6:      	addq	$0x8, %rbp
 3bd77da:      	addq	$0x8, %r12
 3bd77de:      	cmpq	$0x80, %rbp
 3bd77e5:      	je	0x3bd7843 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x383>
 3bd77e7:      	movq	%r14, %rcx
 3bd77ea:      	leaq	(%r15,%rbp), %r14
 3bd77ee:      	movq	(%r15,%rbp), %r13
 3bd77f2:      	movq	(%r15), %rdx
 3bd77f5:      	movq	0x8(%r13), %rax
 3bd77f9:      	cmpq	0x8(%rdx), %rax
 3bd77fd:      	jbe	0x3bd7820 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x360>
 3bd77ff:      	cmpq	$0x9, %rbp
 3bd7803:      	jb	0x3bd77c2 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x302>
 3bd7805:      	movq	%rbx, %rdi
 3bd7808:      	movq	%r15, %rsi
 3bd780b:      	movq	%rbp, %rdx
 3bd780e:      	callq	0x828ac50 <memmove@plt>
 3bd7813:      	jmp	0x3bd77d0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x310>
 3bd7815:      	nopw	%cs:(%rax,%rax)
 3bd781f:      	nop
 3bd7820:      	movq	(%rcx), %rdx
 3bd7823:      	movq	%r14, %rcx
 3bd7826:      	cmpq	0x8(%rdx), %rax
 3bd782a:      	jbe	0x3bd77d3 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x313>
 3bd782c:      	movq	%r12, %rcx
 3bd782f:      	nop
 3bd7830:      	movq	%rdx, (%rcx)
 3bd7833:      	movq	-0x10(%rcx), %rdx
 3bd7837:      	addq	$-0x8, %rcx
 3bd783b:      	cmpq	0x8(%rdx), %rax
 3bd783f:      	ja	0x3bd7830 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x370>
 3bd7841:      	jmp	0x3bd77d3 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x313>
 3bd7843:      	subq	$-0x80, %r15
 3bd7847:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd7851:      	movq	0x8(%rsp), %rdi
 3bd7856:      	jmp	0x3bd7870 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3b0>
 3bd7858:      	nopl	(%rax,%rax)
 3bd7860:      	movq	%rax, (%rsi)
 3bd7863:      	addq	$0x8, %r15
 3bd7867:      	cmpq	%rdi, %r15
 3bd786a:      	je	0x3bd7679 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1b9>
 3bd7870:      	movq	-0x8(%r15), %rcx
 3bd7874:      	movq	(%r15), %rax
 3bd7877:      	movq	0x8(%rax), %rdx
 3bd787b:      	movq	%r15, %rsi
 3bd787e:      	cmpq	0x8(%rcx), %rdx
 3bd7882:      	jbe	0x3bd7860 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3a0>
 3bd7884:      	movq	%r15, %rsi
 3bd7887:      	nopw	(%rax,%rax)
 3bd7890:      	movq	%rcx, (%rsi)
 3bd7893:      	movq	-0x10(%rsi), %rcx
 3bd7897:      	addq	$-0x8, %rsi
 3bd789b:      	cmpq	0x8(%rcx), %rdx
 3bd789f:      	ja	0x3bd7890 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3d0>
 3bd78a1:      	jmp	0x3bd7860 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3a0>
