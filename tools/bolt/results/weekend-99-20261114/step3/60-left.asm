
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004912550 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>:
 4912550:      	xorl	%eax, %eax
 4912552:      	testq	%rsi, %rsi
 4912555:      	je	0x49133b2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe62>
 491255b:      	cmpb	$0x30, 0x10(%rsi)
 491255f:      	jne	0x49133b2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe62>
 4912565:      	pushq	%rbp
 4912566:      	pushq	%r15
 4912568:      	pushq	%r14
 491256a:      	pushq	%r13
 491256c:      	pushq	%r12
 491256e:      	pushq	%rbx
 491256f:      	subq	$0x218, %rsp            # imm = 0x218
 4912576:      	movq	%rdi, %rbp
 4912579:      	movq	%rsi, 0x28(%rsp)
 491257e:      	movq	0x18(%rsi), %rdi
 4912582:      	callq	0x754de40 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912587:      	movq	%rax, %rbx
 491258a:      	movq	(%rbp), %rdi
 491258e:      	movq	%rax, %rsi
 4912591:      	callq	0x7b74b20 <_ZNK5clang10ASTContext18getASTRecordLayoutEPKNS_10RecordDeclE>
 4912596:      	movq	%rax, 0x30(%rsp)
 491259b:      	leaq	0x98(%rsp), %rax
 49125a3:      	movq	%rax, 0x88(%rsp)
 49125ab:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 49125b5:      	movq	%rax, 0x90(%rsp)
 49125bd:      	movq	%rbx, 0x10(%rsp)
 49125c2:      	testq	%rbx, %rbx
 49125c5:      	movq	%rbp, 0x18(%rsp)
 49125ca:      	je	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 49125d0:      	movq	0x10(%rsp), %rax
 49125d5:      	movl	0x1c(%rax), %eax
 49125d8:      	andl	$0x7f, %eax
 49125db:      	addl	$-0x3e, %eax
 49125de:      	cmpl	$-0x3, %eax
 49125e1:      	jb	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 49125e7:      	movq	0x18(%rbp), %rax
 49125eb:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 49125f5:      	testq	%rcx, 0x30(%rax)
 49125f9:      	je	0x4912621 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd1>
 49125fb:      	movq	0x10(%rsp), %rbx
 4912600:      	movq	0x68(%rbx), %rsi
 4912604:      	leaq	0x60(%rsi), %rdi
 4912608:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 491260d:      	movq	0x80(%rbx), %rax
 4912614:      	cmpl	$0x0, 0x14(%rax)
 4912618:      	je	0x4912621 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd1>
 491261a:      	xorl	%ebx, %ebx
 491261c:      	jmp	0x4913384 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe34>
 4912621:      	movq	0x10(%rsp), %rdi
 4912626:      	callq	0x43ecb30 <_ZNK5clang13CXXRecordDecl5basesEv>
 491262b:      	cmpq	%rdx, %rax
 491262e:      	je	0x49129fb <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x4ab>
 4912634:      	movq	%rax, %rbx
 4912637:      	movq	%rdx, %r13
 491263a:      	leaq	0x50(%rbp), %rax
 491263e:      	movq	%rax, 0x20(%rsp)
 4912643:      	leaq	0x100(%rsp), %r14
 491264b:      	movq	%rdx, 0x8(%rsp)
 4912650:      	jmp	0x491270a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ba>
 4912655:      	nopw	%cs:(%rax,%rax)
 491265f:      	nop
 4912660:      	movq	0x58(%rax), %rax
 4912664:      	movq	%rax, 0x100(%rsp)
 491266c:      	movq	0x30(%rsp), %rax
 4912671:      	movq	0x48(%rax), %rdi
 4912675:      	addq	$0x40, %rdi
 4912679:      	movq	%r14, %rsi
 491267c:      	callq	0x449b520 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang13CXXRecordDeclENS2_9CharUnitsENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S6_EEEES5_S6_S8_SB_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSB_bEOT_DpOT0_>
 4912681:      	movq	%r14, %r13
 4912684:      	movq	0x8(%rax), %r14
 4912688:      	movq	(%rbp), %rdi
 491268c:      	movq	%r12, %rsi
 491268f:      	callq	0x7b74b20 <_ZNK5clang10ASTContext18getASTRecordLayoutEPKNS_10RecordDeclE>
 4912694:      	movq	0x8(%rax), %rax
 4912698:      	movq	%r14, 0x100(%rsp)
 49126a0:      	movq	%rax, 0x108(%rsp)
 49126a8:      	movq	%r15, 0x110(%rsp)
 49126b0:      	movl	0x90(%rsp), %edx
 49126b7:      	movq	0x88(%rsp), %rax
 49126bf:      	cmpl	0x94(%rsp), %edx
 49126c6:      	jae	0x4912989 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x439>
 49126cc:      	movq	%r13, %r15
 49126cf:      	movq	%r13, %r14
 49126d2:      	movl	0x90(%rsp), %ecx
 49126d9:      	leaq	(%rcx,%rcx,2), %rcx
 49126dd:      	movq	0x10(%r14), %rdx
 49126e1:      	movq	%rdx, 0x10(%rax,%rcx,8)
 49126e6:      	movups	(%r14), %xmm0
 49126ea:      	movups	%xmm0, (%rax,%rcx,8)
 49126ee:      	incl	0x90(%rsp)
 49126f5:      	movq	%r15, %r14
 49126f8:      	movq	0x8(%rsp), %r13
 49126fd:      	addq	$0x18, %rbx
 4912701:      	cmpq	%r13, %rbx
 4912704:      	je	0x49129fb <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x4ab>
 491270a:      	testb	$0x1, 0xc(%rbx)
 491270e:      	jne	0x49126fd <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ad>
 4912710:      	movq	0x10(%rbx), %rax
 4912714:      	movq	(%rax), %rdi
 4912717:      	movq	%rdi, %rax
 491271a:      	andq	$-0x10, %rax
 491271e:      	movq	(%rax), %r15
 4912721:      	testb	$0xf, 0x8(%r15)
 4912726:      	je	0x4912730 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1e0>
 4912728:      	callq	0x7c38460 <_ZN5clang8QualType27getSplitUnqualifiedTypeImplES0_>
 491272d:      	movq	%rax, %r15
 4912730:      	andq	$-0x10, %r15
 4912734:      	movq	(%r15), %rax
 4912737:      	movq	0x8(%rax), %rax
 491273b:      	andq	$-0x10, %rax
 491273f:      	movq	(%rax), %rax
 4912742:      	movzbl	0x10(%rax), %ecx
 4912746:      	leal	-0x2e(%rcx), %edx
 4912749:      	cmpb	$0x3, %dl
 491274c:      	setb	%dl
 491274f:      	testq	%rax, %rax
 4912752:      	setne	%sil
 4912756:      	leal	-0x2f(%rcx), %edi
 4912759:      	cmpb	$0x2, %dil
 491275d:      	setb	%dil
 4912761:      	andb	%dl, %dil
 4912764:      	andb	%sil, %dil
 4912767:      	cmpb	$0x1, %dil
 491276b:      	jne	0x49127c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x270>
 491276d:      	movq	0x18(%rax), %r12
 4912771:      	cmpb	$0x30, %cl
 4912774:      	jne	0x4912786 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x236>
 4912776:      	movl	0x1c(%r12), %eax
 491277b:      	andl	$0x7f, %eax
 491277e:      	addl	$-0x3b, %eax
 4912781:      	cmpl	$0x2, %eax
 4912784:      	ja	0x49127c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x270>
 4912786:      	movq	0x80(%r12), %rax
 491278e:      	testq	%rax, %rax
 4912791:      	jne	0x49127b2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x262>
 4912793:      	movq	0x68(%r12), %rsi
 4912798:      	leaq	0x60(%rsi), %rdi
 491279c:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 49127a1:      	movq	0x80(%r12), %rax
 49127a9:      	testq	%rax, %rax
 49127ac:      	je	0x491292e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3de>
 49127b2:      	movq	0x58(%rax), %rax
 49127b6:      	testq	%rax, %rax
 49127b9:      	cmovneq	%rax, %r12
 49127bd:      	jmp	0x49127c3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x273>
 49127bf:      	nop
 49127c0:      	xorl	%r12d, %r12d
 49127c3:      	movq	0x68(%r12), %rsi
 49127c8:      	leaq	0x60(%rsi), %rdi
 49127cc:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 49127d1:      	movq	0x80(%r12), %rax
 49127d9:      	testb	$0x2, 0x1(%rax)
 49127dd:      	jne	0x49126fd <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ad>
 49127e3:      	movq	(%r15), %rax
 49127e6:      	movq	0x8(%rax), %rax
 49127ea:      	andq	$-0x10, %rax
 49127ee:      	movq	(%rax), %rax
 49127f1:      	movzbl	0x10(%rax), %ecx
 49127f5:      	leal	-0x2e(%rcx), %edx
 49127f8:      	cmpb	$0x3, %dl
 49127fb:      	setb	%dl
 49127fe:      	testq	%rax, %rax
 4912801:      	setne	%sil
 4912805:      	addb	$-0x2f, %cl
 4912808:      	cmpb	$0x2, %cl
 491280b:      	setb	%cl
 491280e:      	andb	%dl, %cl
 4912810:      	andb	%sil, %cl
 4912813:      	cmpb	$0x1, %cl
 4912816:      	jne	0x49128e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 491281c:      	movq	0x18(%rax), %rbp
 4912820:      	movq	%rbp, %rdi
 4912823:      	callq	0x754de40 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912828:      	testq	%rax, %rax
 491282b:      	cmoveq	%rbp, %rax
 491282f:      	movq	0x18(%rsp), %rbp
 4912834:      	testb	$0x1, 0x4a(%rax)
 4912838:      	je	0x49128e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 491283e:      	movq	0x48(%rax), %rax
 4912842:      	testl	$0x800000, %eax         # imm = 0x800000
 4912847:      	jne	0x49128e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 491284d:      	movzwl	%ax, %eax
 4912850:      	cmpl	$0x2000, %eax           # imm = 0x2000
 4912855:      	setae	%cl
 4912858:      	cwtl
 4912859:      	cmpl	$0x6000, %eax           # imm = 0x6000
 491285e:      	setl	%al
 4912861:      	testb	%al, %cl
 4912863:      	jne	0x49128e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 4912865:      	movq	0x8(%r15), %rax
 4912869:      	andq	$-0x10, %rax
 491286d:      	movq	(%rax), %r13
 4912870:      	movq	0x50(%rbp), %rax
 4912874:      	movl	0x60(%rbp), %ecx
 4912877:      	testq	%rcx, %rcx
 491287a:      	je	0x4912935 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3e5>
 4912880:      	movl	%r13d, %esi
 4912883:      	shrl	$0x4, %esi
 4912886:      	movl	%r13d, %edx
 4912889:      	shrl	$0x9, %edx
 491288c:      	xorl	%esi, %edx
 491288e:      	leal	-0x1(%rcx), %esi
 4912891:      	andl	%esi, %edx
 4912893:      	movl	%edx, %edi
 4912895:      	shll	$0x4, %edi
 4912898:      	movq	(%rax,%rdi), %r9
 491289c:      	cmpq	%r9, %r13
 491289f:      	je	0x491293c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3ec>
 49128a5:      	movl	$0x1, %r8d
 49128ab:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 49128b2:      	je	0x4912935 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3e5>
 49128b8:      	addl	%r8d, %edx
 49128bb:      	incl	%r8d
 49128be:      	andl	%esi, %edx
 49128c0:      	movq	%rdx, %r9
 49128c3:      	shlq	$0x4, %r9
 49128c7:      	leaq	(%rax,%r9), %rdi
 49128cb:      	movq	(%rax,%r9), %r9
 49128cf:      	cmpq	%r9, %r13
 49128d2:      	je	0x491293f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3ef>
 49128d4:      	jmp	0x49128ab <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x35b>
 49128d6:      	nopw	%cs:(%rax,%rax)
 49128e0:      	movq	%rbp, %rdi
 49128e3:      	movq	%r15, %rsi
 49128e6:      	callq	0x4911440 <_ZN5clang7CodeGen11CodeGenTBAA11getTypeInfoENS_8QualTypeE>
 49128eb:      	movq	%rax, %r15
 49128ee:      	testq	%r15, %r15
 49128f1:      	je	0x491261a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 49128f7:      	movq	0x80(%r12), %rax
 49128ff:      	testq	%rax, %rax
 4912902:      	jne	0x4912660 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x110>
 4912908:      	movq	0x68(%r12), %rsi
 491290d:      	leaq	0x60(%rsi), %rdi
 4912911:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 4912916:      	movq	0x80(%r12), %rax
 491291e:      	testq	%rax, %rax
 4912921:      	jne	0x4912660 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x110>
 4912927:      	xorl	%eax, %eax
 4912929:      	jmp	0x4912664 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x114>
 491292e:      	xorl	%eax, %eax
 4912930:      	jmp	0x49127b6 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x266>
 4912935:      	movq	%rcx, %rdi
 4912938:      	shlq	$0x4, %rdi
 491293c:      	addq	%rax, %rdi
 491293f:      	shlq	$0x4, %rcx
 4912943:      	addq	%rcx, %rax
 4912946:      	cmpq	%rax, %rdi
 4912949:      	je	0x4912951 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x401>
 491294b:      	movq	0x8(%rdi), %r15
 491294f:      	jmp	0x49128ee <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x39e>
 4912951:      	movq	%rbp, %rdi
 4912954:      	movq	%r13, %rsi
 4912957:      	callq	0x4912550 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>
 491295c:      	movq	%rax, %r15
 491295f:      	movq	%r13, 0x100(%rsp)
 4912967:      	movq	%rax, 0x108(%rsp)
 491296f:      	movq	0x20(%rsp), %rdi
 4912974:      	movq	%r14, %rsi
 4912977:      	leaq	0x108(%rsp), %rdx
 491297f:      	callq	0x4914070 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeEPNS_6MDNodeENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIS5_JS7_EEESt4pairIPSC_bEOT_DpOT0_>
 4912984:      	jmp	0x49128ee <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x39e>
 4912989:      	leaq	(%rdx,%rdx,2), %rcx
 491298d:      	incq	%rdx
 4912990:      	leaq	(%rax,%rcx,8), %rcx
 4912994:      	movq	%r13, %r14
 4912997:      	subq	%rax, %r14
 491299a:      	setb	%al
 491299d:      	cmpq	%rcx, %r13
 49129a0:      	setae	%cl
 49129a3:      	orb	%al, %cl
 49129a5:      	je	0x49129ce <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x47e>
 49129a7:      	movl	$0x18, %ecx
 49129ac:      	leaq	0x88(%rsp), %rdi
 49129b4:      	leaq	0x98(%rsp), %rsi
 49129bc:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 49129c1:      	movq	0x88(%rsp), %rax
 49129c9:      	jmp	0x49126cc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x17c>
 49129ce:      	movq	%r13, %r15
 49129d1:      	movl	$0x18, %ecx
 49129d6:      	leaq	0x88(%rsp), %rdi
 49129de:      	leaq	0x98(%rsp), %rsi
 49129e6:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 49129eb:      	movq	0x88(%rsp), %rax
 49129f3:      	addq	%rax, %r14
 49129f6:      	jmp	0x49126d2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x182>
 49129fb:      	movl	0x90(%rsp), %r14d
 4912a03:      	testq	%r14, %r14
 4912a06:      	je	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 4912a0c:      	movq	0x88(%rsp), %rbx
 4912a14:      	leaq	(%r14,%r14,2), %rax
 4912a18:      	leaq	(%rbx,%rax,8), %r12
 4912a1c:      	bsrq	%r14, %rdx
 4912a20:      	xorl	$0x3f, %edx
 4912a23:      	addl	%edx, %edx
 4912a25:      	xorq	$0x7e, %rdx
 4912a29:      	movq	%rbx, %rdi
 4912a2c:      	movq	%r12, %rsi
 4912a2f:      	callq	0x4913bd0 <_ZSt16__introsort_loopIPN4llvm9MDBuilder15TBAAStructFieldElN9__gnu_cxx5__ops15_Iter_comp_iterIZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS7_4TypeEE3$_0EEEvT_SF_T0_T1_>
 4912a34:      	leaq	0x18(%rbx), %r15
 4912a38:      	cmpl	$0x11, %r14d
 4912a3c:      	jb	0x4912b1f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5cf>
 4912a42:      	movl	$0x18, %r13d
 4912a48:      	movq	%r15, %r14
 4912a4b:      	movq	%rbx, %rax
 4912a4e:      	jmp	0x4912a77 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x527>
 4912a50:      	movq	%rcx, (%rdx)
 4912a53:      	movaps	0x100(%rsp), %xmm0
 4912a5b:      	movups	%xmm0, 0x8(%rdx)
 4912a5f:      	addq	$0x18, %r13
 4912a63:      	addq	$0x18, %r14
 4912a67:      	movq	%rbp, %rax
 4912a6a:      	cmpq	$0x180, %r13            # imm = 0x180
 4912a71:      	je	0x4913213 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xcc3>
 4912a77:      	leaq	(%rbx,%r13), %rbp
 4912a7b:      	movq	(%rbx,%r13), %rcx
 4912a7f:      	cmpq	(%rbx), %rcx
 4912a82:      	jae	0x4912ad0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x580>
 4912a84:      	movq	0x10(%rbp), %rcx
 4912a88:      	movq	%rcx, 0x110(%rsp)
 4912a90:      	movups	(%rbp), %xmm0
 4912a94:      	movaps	%xmm0, 0x100(%rsp)
 4912a9c:      	cmpq	$0x19, %r13
 4912aa0:      	jb	0x4912b0e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5be>
 4912aa2:      	movq	%r15, %rdi
 4912aa5:      	movq	%rbx, %rsi
 4912aa8:      	movq	%r13, %rdx
 4912aab:      	callq	0x828ac50 <memmove@plt>
 4912ab0:      	movq	0x110(%rsp), %rax
 4912ab8:      	movq	%rax, 0x10(%rbx)
 4912abc:      	movaps	0x100(%rsp), %xmm0
 4912ac4:      	movups	%xmm0, (%rbx)
 4912ac7:      	jmp	0x4912a5f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x50f>
 4912ac9:      	nopl	(%rax)
 4912ad0:      	movups	0x20(%rax), %xmm0
 4912ad4:      	movaps	%xmm0, 0x100(%rsp)
 4912adc:      	movq	%rbp, %rdx
 4912adf:      	cmpq	(%rax), %rcx
 4912ae2:      	jae	0x4912a50 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x500>
 4912ae8:      	movq	%r14, %rdx
 4912aeb:      	nopl	(%rax,%rax)
 4912af0:      	movq	-0x8(%rdx), %rax
 4912af4:      	movq	%rax, 0x10(%rdx)
 4912af8:      	movups	-0x18(%rdx), %xmm0
 4912afc:      	movups	%xmm0, (%rdx)
 4912aff:      	cmpq	-0x30(%rdx), %rcx
 4912b03:      	leaq	-0x18(%rdx), %rdx
 4912b07:      	jb	0x4912af0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5a0>
 4912b09:      	jmp	0x4912a50 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x500>
 4912b0e:      	movq	0x10(%rbx), %rcx
 4912b12:      	movq	%rcx, 0x28(%rax)
 4912b16:      	movups	(%rbx), %xmm0
 4912b19:      	movups	%xmm0, 0x18(%rax)
 4912b1d:      	jmp	0x4912ab0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x560>
 4912b1f:      	cmpl	$0x1, %r14d
 4912b23:      	jne	0x49133b3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe63>
 4912b29:      	movq	0x10(%rsp), %rax
 4912b2e:      	nop
 4912b30:      	movq	%rax, %rbx
 4912b33:      	testb	$-0x80, 0x48(%rax)
 4912b37:      	je	0x4912b47 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5f7>
 4912b39:      	testb	$0x8, 0x4b(%rbx)
 4912b3d:      	jne	0x4912b47 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5f7>
 4912b3f:      	movq	%rbx, %rdi
 4912b42:      	callq	0x75500b0 <_ZNK5clang10RecordDecl29LoadFieldsFromExternalStorageEv>
 4912b47:      	movq	%rbx, %rdi
 4912b4a:      	callq	0x754de40 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912b4f:      	testq	%rax, %rax
 4912b52:      	je	0x4912b59 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x609>
 4912b54:      	cmpq	%rbx, %rax
 4912b57:      	jne	0x4912b30 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e0>
 4912b59:      	movq	0x50(%rbx), %rbx
 4912b5d:      	testq	%rbx, %rbx
 4912b60:      	je	0x4912b8c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x63c>
 4912b62:      	nopw	%cs:(%rax,%rax)
 4912b6c:      	nopl	(%rax)
 4912b70:      	movl	0x1c(%rbx), %eax
 4912b73:      	andl	$0x7f, %eax
 4912b76:      	addl	$-0x31, %eax
 4912b79:      	cmpl	$0x3, %eax
 4912b7c:      	jb	0x4912d3f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7ef>
 4912b82:      	movq	0x8(%rbx), %rbx
 4912b86:      	andq	$-0x8, %rbx
 4912b8a:      	jne	0x4912b70 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x620>
 4912b8c:      	leaq	0x118(%rsp), %r14
 4912b94:      	movq	%r14, 0x100(%rsp)
 4912b9c:      	movq	$0x0, 0x108(%rsp)
 4912ba8:      	movq	$0x100, 0x110(%rsp)     # imm = 0x100
 4912bb4:      	movq	0x20(%rbp), %rax
 4912bb8:      	testb	$0x8, 0x1(%rax)
 4912bbc:      	jne	0x4912be9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x699>
 4912bbe:      	movq	0x10(%rsp), %rax
 4912bc3:      	movq	0x28(%rax), %rax
 4912bc7:      	testb	$0x7, %al
 4912bc9:      	setne	%cl
 4912bcc:      	andq	$-0x8, %rax
 4912bd0:      	sete	%dl
 4912bd3:      	orb	%cl, %dl
 4912bd5:      	movq	0x28(%rsp), %rbx
 4912bda:      	je	0x4913197 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc47>
 4912be0:      	xorl	%eax, %eax
 4912be2:      	xorl	%ecx, %ecx
 4912be4:      	jmp	0x49132b7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd67>
 4912be9:      	movl	$0x2, 0x40(%rsp)
 4912bf1:      	movb	$0x0, 0x60(%rsp)
 4912bf6:      	leaq	0x3a1bbb3(%rip), %rax   # 0x832e7b0 <_ZTVN4llvm19raw_svector_ostreamE>
 4912bfd:      	addq	$0x10, %rax
 4912c01:      	movq	%rax, 0x38(%rsp)
 4912c06:      	leaq	0x100(%rsp), %rax
 4912c0e:      	movq	%rax, 0x68(%rsp)
 4912c13:      	movl	$0x0, 0x64(%rsp)
 4912c1b:      	xorps	%xmm0, %xmm0
 4912c1e:      	movups	%xmm0, 0x48(%rsp)
 4912c23:      	movq	$0x0, 0x58(%rsp)
 4912c2c:      	movq	0x8(%rbp), %rax
 4912c30:      	movq	(%rax), %rax
 4912c33:      	movq	0xe0(%rax), %rax
 4912c3a:      	movq	0x10(%rax), %rdi
 4912c3e:      	movq	0x28(%rsp), %rbx
 4912c43:      	movq	%rbx, %rsi
 4912c46:      	andq	$-0x10, %rsi
 4912c4a:      	movq	(%rdi), %rax
 4912c4d:      	leaq	0x38(%rsp), %rdx
 4912c52:      	xorl	%ecx, %ecx
 4912c54:      	callq	*0xb8(%rax)
 4912c5a:      	leaq	0x3a1b65f(%rip), %rax   # 0x832e2c0 <_ZTVN4llvm11raw_ostreamE>
 4912c61:      	addq	$0x10, %rax
 4912c65:      	movq	%rax, 0x38(%rsp)
 4912c6a:      	cmpl	$0x1, 0x64(%rsp)
 4912c6f:      	jne	0x4912c80 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x730>
 4912c71:      	movq	0x48(%rsp), %rdi
 4912c76:      	testq	%rdi, %rdi
 4912c79:      	je	0x4912c80 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x730>
 4912c7b:      	callq	0x828a840 <_ZdaPv@plt>
 4912c80:      	movq	0x18(%rbp), %rax
 4912c84:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 4912c8e:      	testq	%rcx, 0x30(%rax)
 4912c92:      	jne	0x49132da <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd8a>
 4912c98:      	leaq	0x48(%rsp), %r15
 4912c9d:      	movq	%r15, 0x38(%rsp)
 4912ca2:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 4912cac:      	movq	%rax, 0x40(%rsp)
 4912cb1:      	movl	0x90(%rsp), %eax
 4912cb8:      	xorl	%r8d, %r8d
 4912cbb:      	testq	%rax, %rax
 4912cbe:      	je	0x49131d9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc89>
 4912cc4:      	movq	0x88(%rsp), %r14
 4912ccc:      	shlq	$0x3, %rax
 4912cd0:      	leaq	(%rax,%rax,2), %r13
 4912cd4:      	xorl	%ebp, %ebp
 4912cd6:      	nopw	%cs:(%rax,%rax)
 4912ce0:      	movq	(%r14,%rbp), %r12
 4912ce4:      	movq	0x10(%r14,%rbp), %rbx
 4912ce9:      	cmpl	0x44(%rsp), %r8d
 4912cee:      	jae	0x4912d20 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7d0>
 4912cf0:      	movq	0x38(%rsp), %rax
 4912cf5:      	movl	%r8d, %ecx
 4912cf8:      	shlq	$0x4, %rcx
 4912cfc:      	movq	%rbx, (%rax,%rcx)
 4912d00:      	movq	%r12, 0x8(%rax,%rcx)
 4912d05:      	movl	0x40(%rsp), %r8d
 4912d0a:      	incl	%r8d
 4912d0d:      	movl	%r8d, 0x40(%rsp)
 4912d12:      	addq	$0x18, %rbp
 4912d16:      	cmpq	%rbp, %r13
 4912d19:      	jne	0x4912ce0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x790>
 4912d1b:      	jmp	0x4913180 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc30>
 4912d20:      	movl	%r8d, %edx
 4912d23:      	incq	%rdx
 4912d26:      	movl	$0x10, %ecx
 4912d2b:      	leaq	0x38(%rsp), %rdi
 4912d30:      	movq	%r15, %rsi
 4912d33:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 4912d38:      	movl	0x40(%rsp), %r8d
 4912d3d:      	jmp	0x4912cf0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7a0>
 4912d3f:      	leaq	0x50(%rbp), %rax
 4912d43:      	movq	%rax, 0xf8(%rsp)
 4912d4b:      	leaq	0x100(%rsp), %r13
 4912d53:      	jmp	0x4912d69 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x819>
 4912d55:      	nopw	%cs:(%rax,%rax)
 4912d5f:      	nop
 4912d60:      	testq	%rbx, %rbx
 4912d63:      	je	0x4912b8c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x63c>
 4912d69:      	movq	(%rbp), %rsi
 4912d6d:      	movq	%rbx, %rdi
 4912d70:      	callq	0x754d4e0 <_ZNK5clang9FieldDecl10isZeroSizeERKNS_10ASTContextE>
 4912d75:      	testb	%al, %al
 4912d77:      	jne	0x49130f0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xba0>
 4912d7d:      	testb	$0x1, 0x44(%rbx)
 4912d81:      	je	0x4912d8e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x83e>
 4912d83:      	cmpq	$0x0, 0x28(%rbx)
 4912d88:      	je	0x49130f0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xba0>
 4912d8e:      	movq	0x30(%rbx), %r12
 4912d92:      	movq	%r12, %r14
 4912d95:      	andq	$-0x10, %r14
 4912d99:      	movq	(%r14), %rax
 4912d9c:      	movq	0x8(%rax), %rax
 4912da0:      	andq	$-0x10, %rax
 4912da4:      	movq	(%rax), %rax
 4912da7:      	movzbl	0x10(%rax), %ecx
 4912dab:      	leal	-0x2e(%rcx), %edx
 4912dae:      	cmpb	$0x3, %dl
 4912db1:      	setb	%dl
 4912db4:      	testq	%rax, %rax
 4912db7:      	setne	%sil
 4912dbb:      	addb	$-0x2f, %cl
 4912dbe:      	cmpb	$0x2, %cl
 4912dc1:      	setb	%cl
 4912dc4:      	andb	%dl, %cl
 4912dc6:      	andb	%sil, %cl
 4912dc9:      	cmpb	$0x1, %cl
 4912dcc:      	jne	0x4912e90 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x940>
 4912dd2:      	movq	0x18(%rax), %r15
 4912dd6:      	movq	%r15, %rdi
 4912dd9:      	callq	0x754de40 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912dde:      	testq	%rax, %rax
 4912de1:      	cmoveq	%r15, %rax
 4912de5:      	testb	$0x1, 0x4a(%rax)
 4912de9:      	je	0x4912e90 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x940>
 4912def:      	movq	0x48(%rax), %rax
 4912df3:      	testl	$0x800000, %eax         # imm = 0x800000
 4912df8:      	jne	0x4912e90 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x940>
 4912dfe:      	movzwl	%ax, %eax
 4912e01:      	cmpl	$0x2000, %eax           # imm = 0x2000
 4912e06:      	setae	%cl
 4912e09:      	cwtl
 4912e0a:      	cmpl	$0x6000, %eax           # imm = 0x6000
 4912e0f:      	setl	%al
 4912e12:      	testb	%al, %cl
 4912e14:      	jne	0x4912e90 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x940>
 4912e16:      	movq	0x8(%r14), %rax
 4912e1a:      	andq	$-0x10, %rax
 4912e1e:      	movq	(%rax), %r15
 4912e21:      	movq	0x50(%rbp), %rax
 4912e25:      	movl	0x60(%rbp), %ecx
 4912e28:      	testq	%rcx, %rcx
 4912e2b:      	je	0x4912f47 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x9f7>
 4912e31:      	movl	%r15d, %esi
 4912e34:      	shrl	$0x4, %esi
 4912e37:      	movl	%r15d, %edx
 4912e3a:      	shrl	$0x9, %edx
 4912e3d:      	xorl	%esi, %edx
 4912e3f:      	leal	-0x1(%rcx), %esi
 4912e42:      	andl	%esi, %edx
 4912e44:      	movl	%edx, %edi
 4912e46:      	shll	$0x4, %edi
 4912e49:      	movq	(%rax,%rdi), %r9
 4912e4d:      	cmpq	%r9, %r15
 4912e50:      	je	0x4912f4e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x9fe>
 4912e56:      	movl	$0x1, %r8d
 4912e5c:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 4912e63:      	je	0x4912f47 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x9f7>
 4912e69:      	addl	%r8d, %edx
 4912e6c:      	incl	%r8d
 4912e6f:      	andl	%esi, %edx
 4912e71:      	movq	%rdx, %r9
 4912e74:      	shlq	$0x4, %r9
 4912e78:      	leaq	(%rax,%r9), %rdi
 4912e7c:      	movq	(%rax,%r9), %r9
 4912e80:      	cmpq	%r9, %r15
 4912e83:      	je	0x4912f51 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa01>
 4912e89:      	jmp	0x4912e5c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x90c>
 4912e8b:      	nopl	(%rax,%rax)
 4912e90:      	movq	%rbp, %rdi
 4912e93:      	movq	%r12, %rsi
 4912e96:      	callq	0x4911440 <_ZN5clang7CodeGen11CodeGenTBAA11getTypeInfoENS_8QualTypeE>
 4912e9b:      	movq	%rax, 0x8(%rsp)
 4912ea0:      	cmpq	$0x0, 0x8(%rsp)
 4912ea6:      	je	0x491261a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912eac:      	testb	$-0x80, 0x1d(%rbx)
 4912eb0:      	movq	%rbx, %r15
 4912eb3:      	je	0x4912ec0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x970>
 4912eb5:      	movq	%rbx, %rdi
 4912eb8:      	callq	0x753cfe0 <_ZN5clang20getPrimaryMergedDeclEPNS_4DeclE>
 4912ebd:      	movq	%rax, %r15
 4912ec0:      	movl	0x44(%r15), %eax
 4912ec4:      	cmpl	$0xf, %eax
 4912ec7:      	ja	0x4912ed5 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x985>
 4912ec9:      	movq	%r15, %rdi
 4912ecc:      	callq	0x754d840 <_ZNK5clang9FieldDecl19setCachedFieldIndexEv>
 4912ed1:      	movl	0x44(%r15), %eax
 4912ed5:      	shrl	$0x4, %eax
 4912ed8:      	decl	%eax
 4912eda:      	movq	0x30(%rsp), %rcx
 4912edf:      	movq	0x30(%rcx), %rcx
 4912ee3:      	movq	(%rcx,%rax,8), %r14
 4912ee7:      	movq	(%rbp), %rsi
 4912eeb:      	movq	0x49a0(%rsi), %rax
 4912ef2:      	andq	$-0x10, %rax
 4912ef6:      	movq	(%rax), %rax
 4912ef9:      	movq	%rax, 0x100(%rsp)
 4912f01:      	movq	0x478(%rsi), %rcx
 4912f08:      	movl	0x488(%rsi), %edx
 4912f0e:      	testq	%rdx, %rdx
 4912f11:      	je	0x4912feb <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa9b>
 4912f17:      	movl	%eax, %r8d
 4912f1a:      	shrl	$0x4, %r8d
 4912f1e:      	movl	%eax, %edi
 4912f20:      	shrl	$0x9, %edi
 4912f23:      	xorl	%r8d, %edi
 4912f26:      	leal	-0x1(%rdx), %r8d
 4912f2a:      	andl	%r8d, %edi
 4912f2d:      	leaq	(%rdi,%rdi,2), %r9
 4912f31:      	movq	(%rcx,%r9,8), %r11
 4912f35:      	cmpq	%r11, %rax
 4912f38:      	jne	0x4912fc0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa70>
 4912f3e:      	leaq	(%rcx,%r9,8), %r10
 4912f42:      	jmp	0x4912ff3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xaa3>
 4912f47:      	movq	%rcx, %rdi
 4912f4a:      	shlq	$0x4, %rdi
 4912f4e:      	addq	%rax, %rdi
 4912f51:      	shlq	$0x4, %rcx
 4912f55:      	addq	%rcx, %rax
 4912f58:      	cmpq	%rax, %rdi
 4912f5b:      	je	0x4912f77 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa27>
 4912f5d:      	movq	0x8(%rdi), %rax
 4912f61:      	movq	%rax, 0x8(%rsp)
 4912f66:      	cmpq	$0x0, 0x8(%rsp)
 4912f6c:      	jne	0x4912eac <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x95c>
 4912f72:      	jmp	0x491261a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912f77:      	movq	%rbp, %rdi
 4912f7a:      	movq	%r15, %rsi
 4912f7d:      	callq	0x4912550 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>
 4912f82:      	movq	%r15, 0x100(%rsp)
 4912f8a:      	movq	%rax, 0x8(%rsp)
 4912f8f:      	movq	%rax, 0x108(%rsp)
 4912f97:      	movq	0xf8(%rsp), %rdi
 4912f9f:      	movq	%r13, %rsi
 4912fa2:      	leaq	0x108(%rsp), %rdx
 4912faa:      	callq	0x4914070 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeEPNS_6MDNodeENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIS5_JS7_EEESt4pairIPSC_bEOT_DpOT0_>
 4912faf:      	cmpq	$0x0, 0x8(%rsp)
 4912fb5:      	jne	0x4912eac <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x95c>
 4912fbb:      	jmp	0x491261a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912fc0:      	movl	$0x1, %r9d
 4912fc6:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 4912fcd:      	je	0x4912feb <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa9b>
 4912fcf:      	addl	%r9d, %edi
 4912fd2:      	incl	%r9d
 4912fd5:      	andl	%r8d, %edi
 4912fd8:      	leaq	(%rdi,%rdi,2), %r11
 4912fdc:      	leaq	(%rcx,%r11,8), %r10
 4912fe0:      	movq	(%rcx,%r11,8), %r11
 4912fe4:      	cmpq	%r11, %rax
 4912fe7:      	je	0x4912ff3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xaa3>
 4912fe9:      	jmp	0x4912fc6 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa76>
 4912feb:      	leaq	(%rdx,%rdx,2), %rdi
 4912fef:      	leaq	(%rcx,%rdi,8), %r10
 4912ff3:      	leaq	(%rdx,%rdx,2), %rdx
 4912ff7:      	leaq	(%rcx,%rdx,8), %rcx
 4912ffb:      	cmpq	%rcx, %r10
 4912ffe:      	je	0x491301d <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xacd>
 4913000:      	movq	0x8(%r10), %rbp
 4913004:      	movq	%r14, %rax
 4913007:      	orq	%rbp, %rax
 491300a:      	shrq	$0x20, %rax
 491300e:      	je	0x4913069 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb19>
 4913010:      	movq	%r14, %rax
 4913013:      	xorl	%edx, %edx
 4913015:      	divq	%rbp
 4913018:      	movq	%rax, %r15
 491301b:      	jmp	0x4913073 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb23>
 491301d:      	leaq	0x478(%rsi), %rcx
 4913024:      	movq	%rcx, 0x20(%rsp)
 4913029:      	movq	%rsi, %rdi
 491302c:      	movq	%rax, %rsi
 491302f:      	callq	0x734fe20 <_ZNK5clang10ASTContext15getTypeInfoImplEPKNS_4TypeE>
 4913034:      	movq	%rax, %rbp
 4913037:      	movq	%r12, %r15
 491303a:      	movq	%rdx, %r12
 491303d:      	movq	0x20(%rsp), %rdi
 4913042:      	movq	%r13, %rsi
 4913045:      	callq	0x73a1220 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeENS2_8TypeInfoENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S6_EEEES5_S6_S8_SB_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSB_bEOT_DpOT0_>
 491304a:      	movq	%rbp, 0x8(%rax)
 491304e:      	movq	%r12, 0x10(%rax)
 4913052:      	movq	%r15, %r12
 4913055:      	movq	0x18(%rsp), %rax
 491305a:      	movq	(%rax), %rsi
 491305d:      	movq	%r14, %rax
 4913060:      	orq	%rbp, %rax
 4913063:      	shrq	$0x20, %rax
 4913067:      	jne	0x4913010 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xac0>
 4913069:      	movl	%r14d, %eax
 491306c:      	xorl	%edx, %edx
 491306e:      	divl	%ebp
 4913070:      	movl	%eax, %r15d
 4913073:      	movq	%r13, %rdi
 4913076:      	movq	%r12, %rdx
 4913079:      	callq	0x7351a40 <_ZNK5clang10ASTContext18getTypeInfoInCharsENS_8QualTypeE>
 491307e:      	movq	0x100(%rsp), %rax
 4913086:      	movq	%r15, 0x100(%rsp)
 491308e:      	movq	%rax, 0x108(%rsp)
 4913096:      	movq	0x8(%rsp), %rax
 491309b:      	movq	%rax, 0x110(%rsp)
 49130a3:      	movl	0x90(%rsp), %edx
 49130aa:      	movq	0x88(%rsp), %rax
 49130b2:      	cmpl	0x94(%rsp), %edx
 49130b9:      	movq	0x18(%rsp), %rbp
 49130be:      	jae	0x4913111 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xbc1>
 49130c0:      	movq	%r13, %r14
 49130c3:      	movl	0x90(%rsp), %ecx
 49130ca:      	leaq	(%rcx,%rcx,2), %rcx
 49130ce:      	movq	0x10(%r14), %rdx
 49130d2:      	movq	%rdx, 0x10(%rax,%rcx,8)
 49130d7:      	movups	(%r14), %xmm0
 49130db:      	movups	%xmm0, (%rax,%rcx,8)
 49130df:      	incl	0x90(%rsp)
 49130e6:      	nopw	%cs:(%rax,%rax)
 49130f0:      	movq	0x8(%rbx), %rbx
 49130f4:      	andq	$-0x8, %rbx
 49130f8:      	je	0x4912d60 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x810>
 49130fe:      	movl	0x1c(%rbx), %eax
 4913101:      	andl	$0x7f, %eax
 4913104:      	addl	$-0x31, %eax
 4913107:      	cmpl	$0x3, %eax
 491310a:      	jae	0x49130f0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xba0>
 491310c:      	jmp	0x4912d60 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x810>
 4913111:      	leaq	(%rdx,%rdx,2), %rcx
 4913115:      	incq	%rdx
 4913118:      	leaq	(%rax,%rcx,8), %rcx
 491311c:      	movq	%r13, %r14
 491311f:      	subq	%rax, %r14
 4913122:      	setb	%al
 4913125:      	cmpq	%rcx, %r13
 4913128:      	setae	%cl
 491312b:      	orb	%al, %cl
 491312d:      	je	0x4913156 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc06>
 491312f:      	movl	$0x18, %ecx
 4913134:      	leaq	0x88(%rsp), %rdi
 491313c:      	leaq	0x98(%rsp), %rsi
 4913144:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 4913149:      	movq	0x88(%rsp), %rax
 4913151:      	jmp	0x49130c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb70>
 4913156:      	movl	$0x18, %ecx
 491315b:      	leaq	0x88(%rsp), %rdi
 4913163:      	leaq	0x98(%rsp), %rsi
 491316b:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 4913170:      	movq	0x88(%rsp), %rax
 4913178:      	addq	%rax, %r14
 491317b:      	jmp	0x49130c3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb73>
 4913180:      	movq	0x38(%rsp), %rcx
 4913185:      	movl	%r8d, %r8d
 4913188:      	movq	0x18(%rsp), %rbp
 491318d:      	leaq	0x118(%rsp), %r14
 4913195:      	jmp	0x49131dc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc8c>
 4913197:      	movq	0x10(%rax), %r12
 491319b:      	movl	(%r12), %r15d
 491319f:      	cmpq	$0x101, %r15            # imm = 0x101
 49131a6:      	jb	0x491328b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd3b>
 49131ac:      	leaq	0x100(%rsp), %rdi
 49131b4:      	movl	$0x1, %ecx
 49131b9:      	movq	%r14, %rsi
 49131bc:      	movq	%r15, %rdx
 49131bf:      	callq	0x40f8910 <_ZN4llvm15SmallVectorBaseImE8grow_podEPvmm>
 49131c4:      	movq	0x100(%rsp), %rdi
 49131cc:      	movq	0x108(%rsp), %rax
 49131d4:      	jmp	0x491329a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd4a>
 49131d9:      	movq	%r15, %rcx
 49131dc:      	addq	$0x30, %rbp
 49131e0:      	movq	0x100(%rsp), %rsi
 49131e8:      	movq	0x108(%rsp), %rdx
 49131f0:      	movq	%rbp, %rdi
 49131f3:      	callq	0x3bd0940 <_ZN4llvm9MDBuilder24createTBAAStructTypeNodeENS_9StringRefENS_8ArrayRefISt4pairIPNS_6MDNodeEmEEE>
 49131f8:      	movq	%rax, %rbx
 49131fb:      	movq	0x38(%rsp), %rdi
 4913200:      	cmpq	%r15, %rdi
 4913203:      	je	0x4913372 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe22>
 4913209:      	callq	0x828a6d0 <free@plt>
 491320e:      	jmp	0x4913372 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe22>
 4913213:      	addq	$0x180, %rbx            # imm = 0x180
 491321a:      	movq	0x18(%rsp), %rbp
 491321f:      	jmp	0x491324c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xcfc>
 4913221:      	nopw	%cs:(%rax,%rax)
 491322b:      	nopl	(%rax,%rax)
 4913230:      	movq	%rax, (%rcx)
 4913233:      	movaps	0x100(%rsp), %xmm0
 491323b:      	movups	%xmm0, 0x8(%rcx)
 491323f:      	addq	$0x18, %rbx
 4913243:      	cmpq	%r12, %rbx
 4913246:      	je	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 491324c:      	movq	(%rbx), %rax
 491324f:      	movups	0x8(%rbx), %xmm0
 4913253:      	movaps	%xmm0, 0x100(%rsp)
 491325b:      	movq	%rbx, %rcx
 491325e:      	cmpq	-0x18(%rbx), %rax
 4913262:      	jae	0x4913230 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xce0>
 4913264:      	movq	%rbx, %rcx
 4913267:      	nopw	(%rax,%rax)
 4913270:      	movq	-0x8(%rcx), %rdx
 4913274:      	movq	%rdx, 0x10(%rcx)
 4913278:      	movups	-0x18(%rcx), %xmm0
 491327c:      	movups	%xmm0, (%rcx)
 491327f:      	cmpq	-0x30(%rcx), %rax
 4913283:      	leaq	-0x18(%rcx), %rcx
 4913287:      	jb	0x4913270 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd20>
 4913289:      	jmp	0x4913230 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xce0>
 491328b:      	xorl	%eax, %eax
 491328d:      	movq	%r14, %rdi
 4913290:      	movl	$0x0, %ecx
 4913295:      	testq	%r15, %r15
 4913298:      	je	0x49132b7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd67>
 491329a:      	addq	%rax, %rdi
 491329d:      	addq	$0x10, %r12
 49132a1:      	movq	%r12, %rsi
 49132a4:      	movq	%r15, %rdx
 49132a7:      	callq	0x828ace0 <memcpy@plt>
 49132ac:      	movq	0x108(%rsp), %rcx
 49132b4:      	movq	%r15, %rax
 49132b7:      	addq	%rcx, %rax
 49132ba:      	movq	%rax, 0x108(%rsp)
 49132c2:      	movq	0x18(%rbp), %rax
 49132c6:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 49132d0:      	testq	%rcx, 0x30(%rax)
 49132d4:      	je	0x4912c98 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x748>
 49132da:      	movq	%rbp, %rdi
 49132dd:      	callq	0x4910470 <_ZN5clang7CodeGen11CodeGenTBAA7getCharEv>
 49132e2:      	movq	%rax, %r15
 49132e5:      	movq	(%rbp), %rsi
 49132e9:      	leaq	0x38(%rsp), %rdi
 49132ee:      	movq	%rbx, %rdx
 49132f1:      	callq	0x7351d80 <_ZNK5clang10ASTContext18getTypeInfoInCharsEPKNS_4TypeE>
 49132f6:      	movq	0x38(%rsp), %r12
 49132fb:      	movq	0x100(%rsp), %r14
 4913303:      	movq	0x108(%rsp), %r13
 491330b:      	movq	0x30(%rbp), %rax
 491330f:      	addq	$0x30, %rbp
 4913313:      	movq	%rbp, %rbx
 4913316:      	movl	$0x178, %ebp            # imm = 0x178
 491331b:      	addq	(%rax), %rbp
 491331e:      	movq	%r14, %rdi
 4913321:      	movq	%r13, %rsi
 4913324:      	callq	0x414fc00 <_ZN4llvm11xxh3_64bitsENS_8ArrayRefIhEE>
 4913329:      	movq	%rbp, %rdi
 491332c:      	movq	%r14, %rsi
 491332f:      	movq	%r13, %rdx
 4913332:      	movl	%eax, %ecx
 4913334:      	callq	0x3bed1b0 <_ZN4llvm9StringMapINS_8MDStringENS_20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EEEE21try_emplace_with_hashIJEEESt4pairINS_17StringMapIterBaseIS1_Lb0EEEbENS_9StringRefEjDpOT_>
 4913339:      	movq	(%rax), %rcx
 491333c:      	cmpb	$0x1, %dl
 491333f:      	jne	0x4913345 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xdf5>
 4913341:      	movq	%rcx, 0x10(%rcx)
 4913345:      	addq	$0x8, %rcx
 4913349:      	movq	0x88(%rsp), %r8
 4913351:      	movl	0x90(%rsp), %r9d
 4913359:      	movq	%rbx, %rdi
 491335c:      	movq	%r15, %rsi
 491335f:      	movq	%r12, %rdx
 4913362:      	callq	0x3bd1130 <_ZN4llvm9MDBuilder18createTBAATypeNodeEPNS_6MDNodeEmPNS_8MetadataENS_8ArrayRefINS0_15TBAAStructFieldEEE>
 4913367:      	movq	%rax, %rbx
 491336a:      	leaq	0x118(%rsp), %r14
 4913372:      	movq	0x100(%rsp), %rdi
 491337a:      	cmpq	%r14, %rdi
 491337d:      	je	0x4913384 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe34>
 491337f:      	callq	0x828a6d0 <free@plt>
 4913384:      	movq	0x88(%rsp), %rdi
 491338c:      	leaq	0x98(%rsp), %rax
 4913394:      	cmpq	%rax, %rdi
 4913397:      	je	0x491339e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe4e>
 4913399:      	callq	0x828a6d0 <free@plt>
 491339e:      	movq	%rbx, %rax
 49133a1:      	addq	$0x218, %rsp            # imm = 0x218
 49133a8:      	popq	%rbx
 49133a9:      	popq	%r12
 49133ab:      	popq	%r13
 49133ad:      	popq	%r14
 49133af:      	popq	%r15
 49133b1:      	popq	%rbp
 49133b2:      	retq
 49133b3:      	movabsq	$-0x5555555555555555, %r14 # imm = 0xAAAAAAAAAAAAAAAB
 49133bd:      	movq	%rbx, %rax
 49133c0:      	jmp	0x49133ef <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe9f>
 49133c2:      	nopw	%cs:(%rax,%rax)
 49133cc:      	nopl	(%rax)
 49133d0:      	movq	%rcx, (%rdx)
 49133d3:      	movaps	0x100(%rsp), %xmm0
 49133db:      	movups	%xmm0, 0x8(%rdx)
 49133df:      	leaq	0x18(%r13), %r15
 49133e3:      	movq	%r13, %rax
 49133e6:      	cmpq	%r12, %r15
 49133e9:      	je	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 49133ef:      	movq	%r15, %r13
 49133f2:      	movq	(%r15), %rcx
 49133f5:      	cmpq	(%rbx), %rcx
 49133f8:      	jae	0x4913470 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf20>
 49133fa:      	movq	0x10(%r13), %rcx
 49133fe:      	movq	%rcx, 0x110(%rsp)
 4913406:      	movups	(%r13), %xmm0
 491340b:      	movaps	%xmm0, 0x100(%rsp)
 4913413:      	movq	%r13, %rdx
 4913416:      	subq	%rbx, %rdx
 4913419:      	cmpq	$0x19, %rdx
 491341d:      	jl	0x49134ae <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf5e>
 4913423:      	movq	%rdx, %rcx
 4913426:      	shrq	$0x3, %rcx
 491342a:      	imulq	%r14, %rcx
 491342e:      	negq	%rcx
 4913431:      	leaq	(%rcx,%rcx,2), %rcx
 4913435:      	leaq	0x30(%rax,%rcx,8), %rdi
 491343a:      	movq	%rbx, %rsi
 491343d:      	callq	0x828ac50 <memmove@plt>
 4913442:      	movq	0x110(%rsp), %rax
 491344a:      	movq	%rax, 0x10(%rbx)
 491344e:      	movaps	0x100(%rsp), %xmm0
 4913456:      	movups	%xmm0, (%rbx)
 4913459:      	leaq	0x18(%r13), %r15
 491345d:      	movq	%r13, %rax
 4913460:      	cmpq	%r12, %r15
 4913463:      	jne	0x49133ef <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe9f>
 4913465:      	jmp	0x4912b29 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5d9>
 491346a:      	nopw	(%rax,%rax)
 4913470:      	movups	0x20(%rax), %xmm0
 4913474:      	movaps	%xmm0, 0x100(%rsp)
 491347c:      	movq	%r13, %rdx
 491347f:      	cmpq	(%rax), %rcx
 4913482:      	jae	0x49133d0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe80>
 4913488:      	movq	%r13, %rdx
 491348b:      	nopl	(%rax,%rax)
 4913490:      	movq	-0x8(%rdx), %rax
 4913494:      	movq	%rax, 0x10(%rdx)
 4913498:      	movups	-0x18(%rdx), %xmm0
 491349c:      	movups	%xmm0, (%rdx)
 491349f:      	cmpq	-0x30(%rdx), %rcx
 49134a3:      	leaq	-0x18(%rdx), %rdx
 49134a7:      	jb	0x4913490 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf40>
 49134a9:      	jmp	0x49133d0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe80>
 49134ae:      	cmpq	$0x18, %rdx
 49134b2:      	jne	0x4913442 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xef2>
 49134b4:      	movq	0x10(%rbx), %rcx
 49134b8:      	movq	%rcx, 0x28(%rax)
 49134bc:      	movups	(%rbx), %xmm0
 49134bf:      	movups	%xmm0, 0x18(%rax)
 49134c3:      	jmp	0x4913442 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xef2>
