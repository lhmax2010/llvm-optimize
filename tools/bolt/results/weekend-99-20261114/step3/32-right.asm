
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bd7440 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv>:
 3bd7440:      	pushq	%rbp
 3bd7441:      	pushq	%r15
 3bd7443:      	pushq	%r14
 3bd7445:      	pushq	%r13
 3bd7447:      	pushq	%r12
 3bd7449:      	pushq	%rbx
 3bd744a:      	subq	$0x58, %rsp
 3bd744e:      	movq	%rdi, 0x10(%rsp)
 3bd7453:      	leaq	0x28(%rsp), %rax
 3bd7458:      	movq	%rax, 0x18(%rsp)
 3bd745d:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd7467:      	movq	%r14, 0x20(%rsp)
 3bd746c:      	movl	0x10(%rsi), %edi
 3bd746f:      	leaq	0x18(%rsi), %rax
 3bd7473:      	testb	$0x1, %dil
 3bd7477:      	cmoveq	0x18(%rsi), %rax
 3bd747c:      	movl	$0x4, %ecx
 3bd7481:      	movq	%rsi, 0x8(%rsp)
 3bd7486:      	cmovel	0x20(%rsi), %ecx
 3bd748a:      	leaq	(,%rcx,8), %rdx
 3bd7492:      	leaq	(%rdx,%rdx,2), %rdx
 3bd7496:      	leaq	(%rax,%rdx), %r13
 3bd749a:      	movq	%r13, %rbp
 3bd749d:      	cmpl	$0x2, %edi
 3bd74a0:      	jb	0x3bd74da <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd74a2:      	movq	%rax, %rbp
 3bd74a5:      	testq	%rcx, %rcx
 3bd74a8:      	je	0x3bd74da <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd74aa:      	movl	$0x1000, %esi           # imm = 0x1000
 3bd74af:      	movq	%rax, %rbp
 3bd74b2:      	nopw	%cs:(%rax,%rax)
 3bd74bc:      	nopl	(%rax)
 3bd74c0:      	movq	(%rbp), %rdi
 3bd74c4:      	orq	%rsi, %rdi
 3bd74c7:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 3bd74ce:      	jne	0x3bd74da <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x9a>
 3bd74d0:      	addq	$0x18, %rbp
 3bd74d4:      	addq	$-0x18, %rdx
 3bd74d8:      	jne	0x3bd74c0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x80>
 3bd74da:      	leaq	(%rcx,%rcx,2), %rcx
 3bd74de:      	leaq	(%rax,%rcx,8), %r15
 3bd74e2:      	cmpq	%r15, %rbp
 3bd74e5:      	je	0x3bd75fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1ba>
 3bd74eb:      	addq	$0x10, 0x8(%rsp)
 3bd74f1:      	xorl	%r12d, %r12d
 3bd74f4:      	movl	$0x1000, %r14d          # imm = 0x1000
 3bd74fa:      	jmp	0x3bd7509 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc9>
 3bd74fc:      	nopl	(%rax)
 3bd7500:      	cmpq	%r15, %rbp
 3bd7503:      	je	0x3bd759d <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x15d>
 3bd7509:      	movq	0x8(%rbp), %rax
 3bd750d:      	cmpq	$0x4, %rax
 3bd7511:      	setb	%cl
 3bd7514:      	andl	$0x3, %eax
 3bd7517:      	cmpl	$0x2, %eax
 3bd751a:      	setne	%al
 3bd751d:      	orb	%cl, %al
 3bd751f:      	jne	0x3bd7560 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x120>
 3bd7521:      	movq	(%rbp), %rsi
 3bd7525:      	movq	0x8(%rsp), %rdi
 3bd752a:      	callq	0x3beb210 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPvSt4pairINS_12PointerUnionIJPNS_15MetadataAsValueEPNS_8MetadataEPNS_14DebugValueUserEEEEmELj4ENS_12DenseMapInfoIS2_vEENS_6detail12DenseMapPairIS2_SC_EEEES2_SC_SE_SH_E24lookupOrInsertIntoBucketIRKS2_JEEES3_IPSH_bEOT_DpOT0_>
 3bd752f:      	movl	0x20(%rsp), %edx
 3bd7533:      	cmpl	0x24(%rsp), %edx
 3bd7537:      	jae	0x3bd757a <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x13a>
 3bd7539:      	addq	$0x8, %rax
 3bd753d:      	movq	0x18(%rsp), %rcx
 3bd7542:      	movl	%edx, %edx
 3bd7544:      	movq	%rax, (%rcx,%rdx,8)
 3bd7548:      	movl	0x20(%rsp), %r12d
 3bd754d:      	incl	%r12d
 3bd7550:      	movl	%r12d, 0x20(%rsp)
 3bd7555:      	nopw	%cs:(%rax,%rax)
 3bd755f:      	nop
 3bd7560:      	addq	$0x18, %rbp
 3bd7564:      	cmpq	%r13, %rbp
 3bd7567:      	je	0x3bd7500 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc0>
 3bd7569:      	movq	(%rbp), %rax
 3bd756d:      	orq	%r14, %rax
 3bd7570:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 3bd7576:      	je	0x3bd7560 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x120>
 3bd7578:      	jmp	0x3bd7500 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xc0>
 3bd757a:      	incq	%rdx
 3bd757d:      	movl	$0x8, %ecx
 3bd7582:      	leaq	0x18(%rsp), %rdi
 3bd7587:      	leaq	0x28(%rsp), %rsi
 3bd758c:      	movq	%rax, %r12
 3bd758f:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd7594:      	movq	%r12, %rax
 3bd7597:      	movl	0x20(%rsp), %edx
 3bd759b:      	jmp	0x3bd7539 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0xf9>
 3bd759d:      	testl	%r12d, %r12d
 3bd75a0:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd75aa:      	je	0x3bd75fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1ba>
 3bd75ac:      	movq	0x18(%rsp), %r15
 3bd75b1:      	movl	%r12d, %eax
 3bd75b4:      	leaq	(%r15,%rax,8), %rbp
 3bd75b8:      	bsrq	%rax, %rdx
 3bd75bc:      	xorl	$0x3f, %edx
 3bd75bf:      	addl	%edx, %edx
 3bd75c1:      	xorq	$0x7e, %rdx
 3bd75c5:      	movq	%r15, %rdi
 3bd75c8:      	movq	%rbp, %rsi
 3bd75cb:      	callq	0x3bebc30 <_ZSt16__introsort_loopIPPSt4pairIN4llvm12PointerUnionIJPNS1_15MetadataAsValueEPNS1_8MetadataEPNS1_14DebugValueUserEEEEmElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEvE3$_0EEEvT_SJ_T0_T1_>
 3bd75d0:      	leaq	0x8(%r15), %rbx
 3bd75d4:      	cmpl	$0x11, %r12d
 3bd75d8:      	jb	0x3bd75f0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1b0>
 3bd75da:      	movq	%rbp, 0x8(%rsp)
 3bd75df:      	leaq	0x8(%r15), %r12
 3bd75e3:      	movl	$0x8, %ebp
 3bd75e8:      	movq	%r15, %r14
 3bd75eb:      	jmp	0x3bd7767 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x327>
 3bd75f0:      	cmpl	$0x1, %r12d
 3bd75f4:      	jne	0x3bd76ad <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x26d>
 3bd75fa:      	movq	0x10(%rsp), %rbx
 3bd75ff:      	leaq	0x10(%rbx), %r15
 3bd7603:      	movq	%r15, (%rbx)
 3bd7606:      	movq	%r14, 0x8(%rbx)
 3bd760a:      	movq	0x18(%rsp), %rdi
 3bd760f:      	movl	0x20(%rsp), %r14d
 3bd7614:      	testq	%r14, %r14
 3bd7617:      	je	0x3bd768c <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x24c>
 3bd7619:      	shlq	$0x3, %r14
 3bd761d:      	xorl	%eax, %eax
 3bd761f:      	xorl	%r12d, %r12d
 3bd7622:      	nopw	%cs:(%rax,%rax)
 3bd762c:      	nopl	(%rax)
 3bd7630:      	movq	(%rdi,%r12), %rcx
 3bd7634:      	movq	(%rcx), %r13
 3bd7637:      	cmpl	0xc(%rbx), %eax
 3bd763a:      	jae	0x3bd7660 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x220>
 3bd763c:      	andq	$-0x4, %r13
 3bd7640:      	movq	(%rbx), %rcx
 3bd7643:      	movl	%eax, %eax
 3bd7645:      	addq	$-0x28, %r13
 3bd7649:      	movq	%r13, (%rcx,%rax,8)
 3bd764d:      	movl	0x8(%rbx), %eax
 3bd7650:      	incl	%eax
 3bd7652:      	movl	%eax, 0x8(%rbx)
 3bd7655:      	addq	$0x8, %r12
 3bd7659:      	cmpq	%r12, %r14
 3bd765c:      	jne	0x3bd7630 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1f0>
 3bd765e:      	jmp	0x3bd7687 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x247>
 3bd7660:      	movl	%eax, %edx
 3bd7662:      	incq	%rdx
 3bd7665:      	movl	$0x8, %ecx
 3bd766a:      	movq	%rdi, %rbp
 3bd766d:      	movq	0x10(%rsp), %rdi
 3bd7672:      	movq	%r15, %rsi
 3bd7675:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd767a:      	movq	%rbp, %rdi
 3bd767d:      	movq	0x10(%rsp), %rbx
 3bd7682:      	movl	0x8(%rbx), %eax
 3bd7685:      	jmp	0x3bd763c <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1fc>
 3bd7687:      	movq	0x18(%rsp), %rdi
 3bd768c:      	leaq	0x28(%rsp), %rax
 3bd7691:      	cmpq	%rax, %rdi
 3bd7694:      	je	0x3bd769b <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x25b>
 3bd7696:      	callq	0x828a640 <free@plt>
 3bd769b:      	movq	%rbx, %rax
 3bd769e:      	addq	$0x58, %rsp
 3bd76a2:      	popq	%rbx
 3bd76a3:      	popq	%r12
 3bd76a5:      	popq	%r13
 3bd76a7:      	popq	%r14
 3bd76a9:      	popq	%r15
 3bd76ab:      	popq	%rbp
 3bd76ac:      	retq
 3bd76ad:      	movq	%r15, %r12
 3bd76b0:      	jmp	0x3bd76fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2ba>
 3bd76b2:      	nopw	%cs:(%rax,%rax)
 3bd76bc:      	nopl	(%rax)
 3bd76c0:      	movq	%r12, %rdx
 3bd76c3:      	subq	%r15, %rdx
 3bd76c6:      	movq	%rdx, %rax
 3bd76c9:      	sarq	$0x3, %rax
 3bd76cd:      	cmpq	$0x2, %rax
 3bd76d1:      	jl	0x3bd7733 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2f3>
 3bd76d3:      	shlq	$0x3, %rax
 3bd76d7:      	subq	%rax, %rdi
 3bd76da:      	addq	$0x10, %rdi
 3bd76de:      	movq	%r15, %rsi
 3bd76e1:      	callq	0x828abc0 <memmove@plt>
 3bd76e6:      	movq	%r15, %rax
 3bd76e9:      	movq	%r13, (%rax)
 3bd76ec:      	leaq	0x8(%r12), %rbx
 3bd76f1:      	cmpq	%rbp, %rbx
 3bd76f4:      	je	0x3bd75fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1ba>
 3bd76fa:      	movq	%r12, %rdi
 3bd76fd:      	movq	%rbx, %r12
 3bd7700:      	movq	(%rbx), %r13
 3bd7703:      	movq	(%r15), %rsi
 3bd7706:      	movq	0x8(%r13), %rcx
 3bd770a:      	cmpq	0x8(%rsi), %rcx
 3bd770e:      	ja	0x3bd76c0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x280>
 3bd7710:      	movq	(%rdi), %rdx
 3bd7713:      	movq	%r12, %rax
 3bd7716:      	cmpq	0x8(%rdx), %rcx
 3bd771a:      	jbe	0x3bd76e9 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd771c:      	movq	%r12, %rax
 3bd771f:      	nop
 3bd7720:      	movq	%rdx, (%rax)
 3bd7723:      	movq	-0x10(%rax), %rdx
 3bd7727:      	addq	$-0x8, %rax
 3bd772b:      	cmpq	0x8(%rdx), %rcx
 3bd772f:      	ja	0x3bd7720 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2e0>
 3bd7731:      	jmp	0x3bd76e9 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd7733:      	movq	%r15, %rax
 3bd7736:      	cmpq	$0x8, %rdx
 3bd773a:      	jne	0x3bd76e9 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a9>
 3bd773c:      	movq	%rsi, 0x8(%rdi)
 3bd7740:      	jmp	0x3bd76e6 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x2a6>
 3bd7742:      	movq	%rdx, 0x8(%rcx)
 3bd7746:      	nopw	%cs:(%rax,%rax)
 3bd7750:      	movq	%r15, %rcx
 3bd7753:      	movq	%r13, (%rcx)
 3bd7756:      	addq	$0x8, %rbp
 3bd775a:      	addq	$0x8, %r12
 3bd775e:      	cmpq	$0x80, %rbp
 3bd7765:      	je	0x3bd77c3 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x383>
 3bd7767:      	movq	%r14, %rcx
 3bd776a:      	leaq	(%r15,%rbp), %r14
 3bd776e:      	movq	(%r15,%rbp), %r13
 3bd7772:      	movq	(%r15), %rdx
 3bd7775:      	movq	0x8(%r13), %rax
 3bd7779:      	cmpq	0x8(%rdx), %rax
 3bd777d:      	jbe	0x3bd77a0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x360>
 3bd777f:      	cmpq	$0x9, %rbp
 3bd7783:      	jb	0x3bd7742 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x302>
 3bd7785:      	movq	%rbx, %rdi
 3bd7788:      	movq	%r15, %rsi
 3bd778b:      	movq	%rbp, %rdx
 3bd778e:      	callq	0x828abc0 <memmove@plt>
 3bd7793:      	jmp	0x3bd7750 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x310>
 3bd7795:      	nopw	%cs:(%rax,%rax)
 3bd779f:      	nop
 3bd77a0:      	movq	(%rcx), %rdx
 3bd77a3:      	movq	%r14, %rcx
 3bd77a6:      	cmpq	0x8(%rdx), %rax
 3bd77aa:      	jbe	0x3bd7753 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x313>
 3bd77ac:      	movq	%r12, %rcx
 3bd77af:      	nop
 3bd77b0:      	movq	%rdx, (%rcx)
 3bd77b3:      	movq	-0x10(%rcx), %rdx
 3bd77b7:      	addq	$-0x8, %rcx
 3bd77bb:      	cmpq	0x8(%rdx), %rax
 3bd77bf:      	ja	0x3bd77b0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x370>
 3bd77c1:      	jmp	0x3bd7753 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x313>
 3bd77c3:      	subq	$-0x80, %r15
 3bd77c7:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd77d1:      	movq	0x8(%rsp), %rdi
 3bd77d6:      	jmp	0x3bd77f0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3b0>
 3bd77d8:      	nopl	(%rax,%rax)
 3bd77e0:      	movq	%rax, (%rsi)
 3bd77e3:      	addq	$0x8, %r15
 3bd77e7:      	cmpq	%rdi, %r15
 3bd77ea:      	je	0x3bd75fa <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x1ba>
 3bd77f0:      	movq	-0x8(%r15), %rcx
 3bd77f4:      	movq	(%r15), %rax
 3bd77f7:      	movq	0x8(%rax), %rdx
 3bd77fb:      	movq	%r15, %rsi
 3bd77fe:      	cmpq	0x8(%rcx), %rdx
 3bd7802:      	jbe	0x3bd77e0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3a0>
 3bd7804:      	movq	%r15, %rsi
 3bd7807:      	nopw	(%rax,%rax)
 3bd7810:      	movq	%rcx, (%rsi)
 3bd7813:      	movq	-0x10(%rsi), %rcx
 3bd7817:      	addq	$-0x8, %rsi
 3bd781b:      	cmpq	0x8(%rcx), %rdx
 3bd781f:      	ja	0x3bd7810 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3d0>
 3bd7821:      	jmp	0x3bd77e0 <_ZN4llvm23ReplaceableMetadataImpl28getAllDbgVariableRecordUsersEv+0x3a0>
