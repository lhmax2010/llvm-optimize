
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000049124b0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>:
 49124b0:      	xorl	%eax, %eax
 49124b2:      	testq	%rsi, %rsi
 49124b5:      	je	0x4913322 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe72>
 49124bb:      	cmpb	$0x30, 0x10(%rsi)
 49124bf:      	jne	0x4913322 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe72>
 49124c5:      	pushq	%rbp
 49124c6:      	pushq	%r15
 49124c8:      	pushq	%r14
 49124ca:      	pushq	%r13
 49124cc:      	pushq	%r12
 49124ce:      	pushq	%rbx
 49124cf:      	subq	$0x218, %rsp            # imm = 0x218
 49124d6:      	movq	%rdi, %rbp
 49124d9:      	movq	%rsi, 0x28(%rsp)
 49124de:      	movq	0x18(%rsi), %rdi
 49124e2:      	callq	0x754ddb0 <_ZNK5clang7TagDecl13getDefinitionEv>
 49124e7:      	movq	%rax, %rbx
 49124ea:      	movq	(%rbp), %rdi
 49124ee:      	movq	%rax, %rsi
 49124f1:      	callq	0x7b74a90 <_ZNK5clang10ASTContext18getASTRecordLayoutEPKNS_10RecordDeclE>
 49124f6:      	movq	%rax, 0x30(%rsp)
 49124fb:      	leaq	0x98(%rsp), %rax
 4912503:      	movq	%rax, 0x88(%rsp)
 491250b:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 4912515:      	movq	%rax, 0x90(%rsp)
 491251d:      	movq	%rbx, 0x10(%rsp)
 4912522:      	testq	%rbx, %rbx
 4912525:      	movq	%rbp, 0x18(%rsp)
 491252a:      	je	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 4912530:      	movq	0x10(%rsp), %rax
 4912535:      	movl	0x1c(%rax), %eax
 4912538:      	andl	$0x7f, %eax
 491253b:      	addl	$-0x3e, %eax
 491253e:      	cmpl	$-0x3, %eax
 4912541:      	jb	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 4912547:      	movq	0x18(%rbp), %rax
 491254b:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 4912555:      	testq	%rcx, 0x30(%rax)
 4912559:      	je	0x4912581 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd1>
 491255b:      	movq	0x10(%rsp), %rbx
 4912560:      	movq	0x68(%rbx), %rsi
 4912564:      	leaq	0x60(%rsi), %rdi
 4912568:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 491256d:      	movq	0x80(%rbx), %rax
 4912574:      	cmpl	$0x0, 0x14(%rax)
 4912578:      	je	0x4912581 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd1>
 491257a:      	xorl	%ebx, %ebx
 491257c:      	jmp	0x49132f4 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe44>
 4912581:      	movq	0x10(%rsp), %rdi
 4912586:      	callq	0x43ecaa0 <_ZNK5clang13CXXRecordDecl5basesEv>
 491258b:      	cmpq	%rdx, %rax
 491258e:      	je	0x491295b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x4ab>
 4912594:      	movq	%rax, %rbx
 4912597:      	movq	%rdx, %r13
 491259a:      	leaq	0x50(%rbp), %rax
 491259e:      	movq	%rax, 0x20(%rsp)
 49125a3:      	leaq	0x100(%rsp), %r14
 49125ab:      	movq	%rdx, 0x8(%rsp)
 49125b0:      	jmp	0x491266a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ba>
 49125b5:      	nopw	%cs:(%rax,%rax)
 49125bf:      	nop
 49125c0:      	movq	0x58(%rax), %rax
 49125c4:      	movq	%rax, 0x100(%rsp)
 49125cc:      	movq	0x30(%rsp), %rax
 49125d1:      	movq	0x48(%rax), %rdi
 49125d5:      	addq	$0x40, %rdi
 49125d9:      	movq	%r14, %rsi
 49125dc:      	callq	0x449b490 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang13CXXRecordDeclENS2_9CharUnitsENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S6_EEEES5_S6_S8_SB_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSB_bEOT_DpOT0_>
 49125e1:      	movq	%r14, %r13
 49125e4:      	movq	0x8(%rax), %r14
 49125e8:      	movq	(%rbp), %rdi
 49125ec:      	movq	%r12, %rsi
 49125ef:      	callq	0x7b74a90 <_ZNK5clang10ASTContext18getASTRecordLayoutEPKNS_10RecordDeclE>
 49125f4:      	movq	0x8(%rax), %rax
 49125f8:      	movq	%r14, 0x100(%rsp)
 4912600:      	movq	%rax, 0x108(%rsp)
 4912608:      	movq	%r15, 0x110(%rsp)
 4912610:      	movl	0x90(%rsp), %edx
 4912617:      	movq	0x88(%rsp), %rax
 491261f:      	cmpl	0x94(%rsp), %edx
 4912626:      	jae	0x49128e9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x439>
 491262c:      	movq	%r13, %r15
 491262f:      	movq	%r13, %r14
 4912632:      	movl	0x90(%rsp), %ecx
 4912639:      	leaq	(%rcx,%rcx,2), %rcx
 491263d:      	movq	0x10(%r14), %rdx
 4912641:      	movq	%rdx, 0x10(%rax,%rcx,8)
 4912646:      	movups	(%r14), %xmm0
 491264a:      	movups	%xmm0, (%rax,%rcx,8)
 491264e:      	incl	0x90(%rsp)
 4912655:      	movq	%r15, %r14
 4912658:      	movq	0x8(%rsp), %r13
 491265d:      	addq	$0x18, %rbx
 4912661:      	cmpq	%r13, %rbx
 4912664:      	je	0x491295b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x4ab>
 491266a:      	testb	$0x1, 0xc(%rbx)
 491266e:      	jne	0x491265d <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ad>
 4912670:      	movq	0x10(%rbx), %rax
 4912674:      	movq	(%rax), %rdi
 4912677:      	movq	%rdi, %rax
 491267a:      	andq	$-0x10, %rax
 491267e:      	movq	(%rax), %r15
 4912681:      	testb	$0xf, 0x8(%r15)
 4912686:      	je	0x4912690 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1e0>
 4912688:      	callq	0x7c383d0 <_ZN5clang8QualType27getSplitUnqualifiedTypeImplES0_>
 491268d:      	movq	%rax, %r15
 4912690:      	andq	$-0x10, %r15
 4912694:      	movq	(%r15), %rax
 4912697:      	movq	0x8(%rax), %rax
 491269b:      	andq	$-0x10, %rax
 491269f:      	movq	(%rax), %rax
 49126a2:      	movzbl	0x10(%rax), %ecx
 49126a6:      	leal	-0x2e(%rcx), %edx
 49126a9:      	cmpb	$0x3, %dl
 49126ac:      	setb	%dl
 49126af:      	testq	%rax, %rax
 49126b2:      	setne	%sil
 49126b6:      	leal	-0x2f(%rcx), %edi
 49126b9:      	cmpb	$0x2, %dil
 49126bd:      	setb	%dil
 49126c1:      	andb	%dl, %dil
 49126c4:      	andb	%sil, %dil
 49126c7:      	cmpb	$0x1, %dil
 49126cb:      	jne	0x4912720 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x270>
 49126cd:      	movq	0x18(%rax), %r12
 49126d1:      	cmpb	$0x30, %cl
 49126d4:      	jne	0x49126e6 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x236>
 49126d6:      	movl	0x1c(%r12), %eax
 49126db:      	andl	$0x7f, %eax
 49126de:      	addl	$-0x3b, %eax
 49126e1:      	cmpl	$0x2, %eax
 49126e4:      	ja	0x4912720 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x270>
 49126e6:      	movq	0x80(%r12), %rax
 49126ee:      	testq	%rax, %rax
 49126f1:      	jne	0x4912712 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x262>
 49126f3:      	movq	0x68(%r12), %rsi
 49126f8:      	leaq	0x60(%rsi), %rdi
 49126fc:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 4912701:      	movq	0x80(%r12), %rax
 4912709:      	testq	%rax, %rax
 491270c:      	je	0x491288e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3de>
 4912712:      	movq	0x58(%rax), %rax
 4912716:      	testq	%rax, %rax
 4912719:      	cmovneq	%rax, %r12
 491271d:      	jmp	0x4912723 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x273>
 491271f:      	nop
 4912720:      	xorl	%r12d, %r12d
 4912723:      	movq	0x68(%r12), %rsi
 4912728:      	leaq	0x60(%rsi), %rdi
 491272c:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 4912731:      	movq	0x80(%r12), %rax
 4912739:      	testb	$0x2, 0x1(%rax)
 491273d:      	jne	0x491265d <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x1ad>
 4912743:      	movq	(%r15), %rax
 4912746:      	movq	0x8(%rax), %rax
 491274a:      	andq	$-0x10, %rax
 491274e:      	movq	(%rax), %rax
 4912751:      	movzbl	0x10(%rax), %ecx
 4912755:      	leal	-0x2e(%rcx), %edx
 4912758:      	cmpb	$0x3, %dl
 491275b:      	setb	%dl
 491275e:      	testq	%rax, %rax
 4912761:      	setne	%sil
 4912765:      	addb	$-0x2f, %cl
 4912768:      	cmpb	$0x2, %cl
 491276b:      	setb	%cl
 491276e:      	andb	%dl, %cl
 4912770:      	andb	%sil, %cl
 4912773:      	cmpb	$0x1, %cl
 4912776:      	jne	0x4912840 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 491277c:      	movq	0x18(%rax), %rbp
 4912780:      	movq	%rbp, %rdi
 4912783:      	callq	0x754ddb0 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912788:      	testq	%rax, %rax
 491278b:      	cmoveq	%rbp, %rax
 491278f:      	movq	0x18(%rsp), %rbp
 4912794:      	testb	$0x1, 0x4a(%rax)
 4912798:      	je	0x4912840 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 491279e:      	movq	0x48(%rax), %rax
 49127a2:      	testl	$0x800000, %eax         # imm = 0x800000
 49127a7:      	jne	0x4912840 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 49127ad:      	movzwl	%ax, %eax
 49127b0:      	cmpl	$0x2000, %eax           # imm = 0x2000
 49127b5:      	setae	%cl
 49127b8:      	cwtl
 49127b9:      	cmpl	$0x6000, %eax           # imm = 0x6000
 49127be:      	setl	%al
 49127c1:      	testb	%al, %cl
 49127c3:      	jne	0x4912840 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x390>
 49127c5:      	movq	0x8(%r15), %rax
 49127c9:      	andq	$-0x10, %rax
 49127cd:      	movq	(%rax), %r13
 49127d0:      	movq	0x50(%rbp), %rax
 49127d4:      	movl	0x60(%rbp), %ecx
 49127d7:      	testq	%rcx, %rcx
 49127da:      	je	0x4912895 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3e5>
 49127e0:      	movl	%r13d, %esi
 49127e3:      	shrl	$0x4, %esi
 49127e6:      	movl	%r13d, %edx
 49127e9:      	shrl	$0x9, %edx
 49127ec:      	xorl	%esi, %edx
 49127ee:      	leal	-0x1(%rcx), %esi
 49127f1:      	andl	%esi, %edx
 49127f3:      	movl	%edx, %edi
 49127f5:      	shll	$0x4, %edi
 49127f8:      	movq	(%rax,%rdi), %r9
 49127fc:      	cmpq	%r9, %r13
 49127ff:      	je	0x491289c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3ec>
 4912805:      	movl	$0x1, %r8d
 491280b:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 4912812:      	je	0x4912895 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3e5>
 4912818:      	addl	%r8d, %edx
 491281b:      	incl	%r8d
 491281e:      	andl	%esi, %edx
 4912820:      	movq	%rdx, %r9
 4912823:      	shlq	$0x4, %r9
 4912827:      	leaq	(%rax,%r9), %rdi
 491282b:      	movq	(%rax,%r9), %r9
 491282f:      	cmpq	%r9, %r13
 4912832:      	je	0x491289f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x3ef>
 4912834:      	jmp	0x491280b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x35b>
 4912836:      	nopw	%cs:(%rax,%rax)
 4912840:      	movq	%rbp, %rdi
 4912843:      	movq	%r15, %rsi
 4912846:      	callq	0x49113a0 <_ZN5clang7CodeGen11CodeGenTBAA11getTypeInfoENS_8QualTypeE>
 491284b:      	movq	%rax, %r15
 491284e:      	testq	%r15, %r15
 4912851:      	je	0x491257a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912857:      	movq	0x80(%r12), %rax
 491285f:      	testq	%rax, %rax
 4912862:      	jne	0x49125c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x110>
 4912868:      	movq	0x68(%r12), %rsi
 491286d:      	leaq	0x60(%rsi), %rdi
 4912871:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 4912876:      	movq	0x80(%r12), %rax
 491287e:      	testq	%rax, %rax
 4912881:      	jne	0x49125c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x110>
 4912887:      	xorl	%eax, %eax
 4912889:      	jmp	0x49125c4 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x114>
 491288e:      	xorl	%eax, %eax
 4912890:      	jmp	0x4912716 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x266>
 4912895:      	movq	%rcx, %rdi
 4912898:      	shlq	$0x4, %rdi
 491289c:      	addq	%rax, %rdi
 491289f:      	shlq	$0x4, %rcx
 49128a3:      	addq	%rcx, %rax
 49128a6:      	cmpq	%rax, %rdi
 49128a9:      	je	0x49128b1 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x401>
 49128ab:      	movq	0x8(%rdi), %r15
 49128af:      	jmp	0x491284e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x39e>
 49128b1:      	movq	%rbp, %rdi
 49128b4:      	movq	%r13, %rsi
 49128b7:      	callq	0x49124b0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>
 49128bc:      	movq	%rax, %r15
 49128bf:      	movq	%r13, 0x100(%rsp)
 49128c7:      	movq	%rax, 0x108(%rsp)
 49128cf:      	movq	0x20(%rsp), %rdi
 49128d4:      	movq	%r14, %rsi
 49128d7:      	leaq	0x108(%rsp), %rdx
 49128df:      	callq	0x4913fe0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeEPNS_6MDNodeENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIS5_JS7_EEESt4pairIPSC_bEOT_DpOT0_>
 49128e4:      	jmp	0x491284e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x39e>
 49128e9:      	leaq	(%rdx,%rdx,2), %rcx
 49128ed:      	incq	%rdx
 49128f0:      	leaq	(%rax,%rcx,8), %rcx
 49128f4:      	movq	%r13, %r14
 49128f7:      	subq	%rax, %r14
 49128fa:      	setb	%al
 49128fd:      	cmpq	%rcx, %r13
 4912900:      	setae	%cl
 4912903:      	orb	%al, %cl
 4912905:      	je	0x491292e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x47e>
 4912907:      	movl	$0x18, %ecx
 491290c:      	leaq	0x88(%rsp), %rdi
 4912914:      	leaq	0x98(%rsp), %rsi
 491291c:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 4912921:      	movq	0x88(%rsp), %rax
 4912929:      	jmp	0x491262c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x17c>
 491292e:      	movq	%r13, %r15
 4912931:      	movl	$0x18, %ecx
 4912936:      	leaq	0x88(%rsp), %rdi
 491293e:      	leaq	0x98(%rsp), %rsi
 4912946:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 491294b:      	movq	0x88(%rsp), %rax
 4912953:      	addq	%rax, %r14
 4912956:      	jmp	0x4912632 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x182>
 491295b:      	movl	0x90(%rsp), %r14d
 4912963:      	testq	%r14, %r14
 4912966:      	je	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 491296c:      	movq	0x88(%rsp), %rbx
 4912974:      	leaq	(%r14,%r14,2), %rax
 4912978:      	leaq	(%rbx,%rax,8), %r12
 491297c:      	bsrq	%r14, %rdx
 4912980:      	xorl	$0x3f, %edx
 4912983:      	addl	%edx, %edx
 4912985:      	xorq	$0x7e, %rdx
 4912989:      	movq	%rbx, %rdi
 491298c:      	movq	%r12, %rsi
 491298f:      	callq	0x4913b40 <_ZSt16__introsort_loopIPN4llvm9MDBuilder15TBAAStructFieldElN9__gnu_cxx5__ops15_Iter_comp_iterIZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS7_4TypeEE3$_0EEEvT_SF_T0_T1_>
 4912994:      	leaq	0x18(%rbx), %r15
 4912998:      	cmpl	$0x11, %r14d
 491299c:      	jb	0x4912a8f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5df>
 49129a2:      	leaq	0x18(%rbx), %r14
 49129a6:      	movl	$0x18, %r13d
 49129ac:      	movq	%rbx, %rax
 49129af:      	jmp	0x49129e7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x537>
 49129b1:      	nopw	%cs:(%rax,%rax)
 49129bb:      	nopl	(%rax,%rax)
 49129c0:      	movq	%rcx, (%rdx)
 49129c3:      	movaps	0x100(%rsp), %xmm0
 49129cb:      	movups	%xmm0, 0x8(%rdx)
 49129cf:      	addq	$0x18, %r13
 49129d3:      	addq	$0x18, %r14
 49129d7:      	movq	%rbp, %rax
 49129da:      	cmpq	$0x180, %r13            # imm = 0x180
 49129e1:      	je	0x4913183 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xcd3>
 49129e7:      	leaq	(%rbx,%r13), %rbp
 49129eb:      	movq	(%rbx,%r13), %rcx
 49129ef:      	cmpq	(%rbx), %rcx
 49129f2:      	jae	0x4912a40 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x590>
 49129f4:      	movq	0x10(%rbp), %rcx
 49129f8:      	movq	%rcx, 0x110(%rsp)
 4912a00:      	movups	(%rbp), %xmm0
 4912a04:      	movaps	%xmm0, 0x100(%rsp)
 4912a0c:      	cmpq	$0x19, %r13
 4912a10:      	jb	0x4912a7e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5ce>
 4912a12:      	movq	%r15, %rdi
 4912a15:      	movq	%rbx, %rsi
 4912a18:      	movq	%r13, %rdx
 4912a1b:      	callq	0x828abc0 <memmove@plt>
 4912a20:      	movq	0x110(%rsp), %rax
 4912a28:      	movq	%rax, 0x10(%rbx)
 4912a2c:      	movaps	0x100(%rsp), %xmm0
 4912a34:      	movups	%xmm0, (%rbx)
 4912a37:      	jmp	0x49129cf <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x51f>
 4912a39:      	nopl	(%rax)
 4912a40:      	movups	0x20(%rax), %xmm0
 4912a44:      	movaps	%xmm0, 0x100(%rsp)
 4912a4c:      	movq	%rbp, %rdx
 4912a4f:      	cmpq	(%rax), %rcx
 4912a52:      	jae	0x49129c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x510>
 4912a58:      	movq	%r14, %rdx
 4912a5b:      	nopl	(%rax,%rax)
 4912a60:      	movq	-0x8(%rdx), %rax
 4912a64:      	movq	%rax, 0x10(%rdx)
 4912a68:      	movups	-0x18(%rdx), %xmm0
 4912a6c:      	movups	%xmm0, (%rdx)
 4912a6f:      	cmpq	-0x30(%rdx), %rcx
 4912a73:      	leaq	-0x18(%rdx), %rdx
 4912a77:      	jb	0x4912a60 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5b0>
 4912a79:      	jmp	0x49129c0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x510>
 4912a7e:      	movq	0x10(%rbx), %rcx
 4912a82:      	movq	%rcx, 0x28(%rax)
 4912a86:      	movups	(%rbx), %xmm0
 4912a89:      	movups	%xmm0, 0x18(%rax)
 4912a8d:      	jmp	0x4912a20 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x570>
 4912a8f:      	cmpl	$0x1, %r14d
 4912a93:      	jne	0x4913323 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe73>
 4912a99:      	movq	0x10(%rsp), %rax
 4912a9e:      	nop
 4912aa0:      	movq	%rax, %rbx
 4912aa3:      	testb	$-0x80, 0x48(%rax)
 4912aa7:      	je	0x4912ab7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x607>
 4912aa9:      	testb	$0x8, 0x4b(%rbx)
 4912aad:      	jne	0x4912ab7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x607>
 4912aaf:      	movq	%rbx, %rdi
 4912ab2:      	callq	0x7550020 <_ZNK5clang10RecordDecl29LoadFieldsFromExternalStorageEv>
 4912ab7:      	movq	%rbx, %rdi
 4912aba:      	callq	0x754ddb0 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912abf:      	testq	%rax, %rax
 4912ac2:      	je	0x4912ac9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x619>
 4912ac4:      	cmpq	%rbx, %rax
 4912ac7:      	jne	0x4912aa0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5f0>
 4912ac9:      	movq	0x50(%rbx), %rbx
 4912acd:      	testq	%rbx, %rbx
 4912ad0:      	je	0x4912afc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x64c>
 4912ad2:      	nopw	%cs:(%rax,%rax)
 4912adc:      	nopl	(%rax)
 4912ae0:      	movl	0x1c(%rbx), %eax
 4912ae3:      	andl	$0x7f, %eax
 4912ae6:      	addl	$-0x31, %eax
 4912ae9:      	cmpl	$0x3, %eax
 4912aec:      	jb	0x4912caf <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7ff>
 4912af2:      	movq	0x8(%rbx), %rbx
 4912af6:      	andq	$-0x8, %rbx
 4912afa:      	jne	0x4912ae0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x630>
 4912afc:      	leaq	0x118(%rsp), %r14
 4912b04:      	movq	%r14, 0x100(%rsp)
 4912b0c:      	movq	$0x0, 0x108(%rsp)
 4912b18:      	movq	$0x100, 0x110(%rsp)     # imm = 0x100
 4912b24:      	movq	0x20(%rbp), %rax
 4912b28:      	testb	$0x8, 0x1(%rax)
 4912b2c:      	jne	0x4912b59 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x6a9>
 4912b2e:      	movq	0x10(%rsp), %rax
 4912b33:      	movq	0x28(%rax), %rax
 4912b37:      	testb	$0x7, %al
 4912b39:      	setne	%cl
 4912b3c:      	andq	$-0x8, %rax
 4912b40:      	sete	%dl
 4912b43:      	orb	%cl, %dl
 4912b45:      	movq	0x28(%rsp), %rbx
 4912b4a:      	je	0x4913107 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc57>
 4912b50:      	xorl	%eax, %eax
 4912b52:      	xorl	%ecx, %ecx
 4912b54:      	jmp	0x4913227 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd77>
 4912b59:      	movl	$0x2, 0x40(%rsp)
 4912b61:      	movb	$0x0, 0x60(%rsp)
 4912b66:      	leaq	0x3a1bbb3(%rip), %rax   # 0x832e720 <_ZTVN4llvm19raw_svector_ostreamE>
 4912b6d:      	addq	$0x10, %rax
 4912b71:      	movq	%rax, 0x38(%rsp)
 4912b76:      	leaq	0x100(%rsp), %rax
 4912b7e:      	movq	%rax, 0x68(%rsp)
 4912b83:      	movl	$0x0, 0x64(%rsp)
 4912b8b:      	xorps	%xmm0, %xmm0
 4912b8e:      	movups	%xmm0, 0x48(%rsp)
 4912b93:      	movq	$0x0, 0x58(%rsp)
 4912b9c:      	movq	0x8(%rbp), %rax
 4912ba0:      	movq	(%rax), %rax
 4912ba3:      	movq	0xe0(%rax), %rax
 4912baa:      	movq	0x10(%rax), %rdi
 4912bae:      	movq	0x28(%rsp), %rbx
 4912bb3:      	movq	%rbx, %rsi
 4912bb6:      	andq	$-0x10, %rsi
 4912bba:      	movq	(%rdi), %rax
 4912bbd:      	leaq	0x38(%rsp), %rdx
 4912bc2:      	xorl	%ecx, %ecx
 4912bc4:      	callq	*0xb8(%rax)
 4912bca:      	leaq	0x3a1b65f(%rip), %rax   # 0x832e230 <_ZTVN4llvm11raw_ostreamE>
 4912bd1:      	addq	$0x10, %rax
 4912bd5:      	movq	%rax, 0x38(%rsp)
 4912bda:      	cmpl	$0x1, 0x64(%rsp)
 4912bdf:      	jne	0x4912bf0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x740>
 4912be1:      	movq	0x48(%rsp), %rdi
 4912be6:      	testq	%rdi, %rdi
 4912be9:      	je	0x4912bf0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x740>
 4912beb:      	callq	0x828a7b0 <_ZdaPv@plt>
 4912bf0:      	movq	0x18(%rbp), %rax
 4912bf4:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 4912bfe:      	testq	%rcx, 0x30(%rax)
 4912c02:      	jne	0x491324a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd9a>
 4912c08:      	leaq	0x48(%rsp), %r15
 4912c0d:      	movq	%r15, 0x38(%rsp)
 4912c12:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 4912c1c:      	movq	%rax, 0x40(%rsp)
 4912c21:      	movl	0x90(%rsp), %eax
 4912c28:      	xorl	%r8d, %r8d
 4912c2b:      	testq	%rax, %rax
 4912c2e:      	je	0x4913149 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc99>
 4912c34:      	movq	0x88(%rsp), %r14
 4912c3c:      	shlq	$0x3, %rax
 4912c40:      	leaq	(%rax,%rax,2), %r13
 4912c44:      	xorl	%ebp, %ebp
 4912c46:      	nopw	%cs:(%rax,%rax)
 4912c50:      	movq	(%r14,%rbp), %r12
 4912c54:      	movq	0x10(%r14,%rbp), %rbx
 4912c59:      	cmpl	0x44(%rsp), %r8d
 4912c5e:      	jae	0x4912c90 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7e0>
 4912c60:      	movq	0x38(%rsp), %rax
 4912c65:      	movl	%r8d, %ecx
 4912c68:      	shlq	$0x4, %rcx
 4912c6c:      	movq	%rbx, (%rax,%rcx)
 4912c70:      	movq	%r12, 0x8(%rax,%rcx)
 4912c75:      	movl	0x40(%rsp), %r8d
 4912c7a:      	incl	%r8d
 4912c7d:      	movl	%r8d, 0x40(%rsp)
 4912c82:      	addq	$0x18, %rbp
 4912c86:      	cmpq	%rbp, %r13
 4912c89:      	jne	0x4912c50 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7a0>
 4912c8b:      	jmp	0x49130f0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc40>
 4912c90:      	movl	%r8d, %edx
 4912c93:      	incq	%rdx
 4912c96:      	movl	$0x10, %ecx
 4912c9b:      	leaq	0x38(%rsp), %rdi
 4912ca0:      	movq	%r15, %rsi
 4912ca3:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 4912ca8:      	movl	0x40(%rsp), %r8d
 4912cad:      	jmp	0x4912c60 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x7b0>
 4912caf:      	leaq	0x50(%rbp), %rax
 4912cb3:      	movq	%rax, 0xf8(%rsp)
 4912cbb:      	leaq	0x100(%rsp), %r13
 4912cc3:      	jmp	0x4912cd9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x829>
 4912cc5:      	nopw	%cs:(%rax,%rax)
 4912ccf:      	nop
 4912cd0:      	testq	%rbx, %rbx
 4912cd3:      	je	0x4912afc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x64c>
 4912cd9:      	movq	(%rbp), %rsi
 4912cdd:      	movq	%rbx, %rdi
 4912ce0:      	callq	0x754d450 <_ZNK5clang9FieldDecl10isZeroSizeERKNS_10ASTContextE>
 4912ce5:      	testb	%al, %al
 4912ce7:      	jne	0x4913060 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xbb0>
 4912ced:      	testb	$0x1, 0x44(%rbx)
 4912cf1:      	je	0x4912cfe <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x84e>
 4912cf3:      	cmpq	$0x0, 0x28(%rbx)
 4912cf8:      	je	0x4913060 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xbb0>
 4912cfe:      	movq	0x30(%rbx), %r12
 4912d02:      	movq	%r12, %r14
 4912d05:      	andq	$-0x10, %r14
 4912d09:      	movq	(%r14), %rax
 4912d0c:      	movq	0x8(%rax), %rax
 4912d10:      	andq	$-0x10, %rax
 4912d14:      	movq	(%rax), %rax
 4912d17:      	movzbl	0x10(%rax), %ecx
 4912d1b:      	leal	-0x2e(%rcx), %edx
 4912d1e:      	cmpb	$0x3, %dl
 4912d21:      	setb	%dl
 4912d24:      	testq	%rax, %rax
 4912d27:      	setne	%sil
 4912d2b:      	addb	$-0x2f, %cl
 4912d2e:      	cmpb	$0x2, %cl
 4912d31:      	setb	%cl
 4912d34:      	andb	%dl, %cl
 4912d36:      	andb	%sil, %cl
 4912d39:      	cmpb	$0x1, %cl
 4912d3c:      	jne	0x4912e00 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x950>
 4912d42:      	movq	0x18(%rax), %r15
 4912d46:      	movq	%r15, %rdi
 4912d49:      	callq	0x754ddb0 <_ZNK5clang7TagDecl13getDefinitionEv>
 4912d4e:      	testq	%rax, %rax
 4912d51:      	cmoveq	%r15, %rax
 4912d55:      	testb	$0x1, 0x4a(%rax)
 4912d59:      	je	0x4912e00 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x950>
 4912d5f:      	movq	0x48(%rax), %rax
 4912d63:      	testl	$0x800000, %eax         # imm = 0x800000
 4912d68:      	jne	0x4912e00 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x950>
 4912d6e:      	movzwl	%ax, %eax
 4912d71:      	cmpl	$0x2000, %eax           # imm = 0x2000
 4912d76:      	setae	%cl
 4912d79:      	cwtl
 4912d7a:      	cmpl	$0x6000, %eax           # imm = 0x6000
 4912d7f:      	setl	%al
 4912d82:      	testb	%al, %cl
 4912d84:      	jne	0x4912e00 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x950>
 4912d86:      	movq	0x8(%r14), %rax
 4912d8a:      	andq	$-0x10, %rax
 4912d8e:      	movq	(%rax), %r15
 4912d91:      	movq	0x50(%rbp), %rax
 4912d95:      	movl	0x60(%rbp), %ecx
 4912d98:      	testq	%rcx, %rcx
 4912d9b:      	je	0x4912eb7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa07>
 4912da1:      	movl	%r15d, %esi
 4912da4:      	shrl	$0x4, %esi
 4912da7:      	movl	%r15d, %edx
 4912daa:      	shrl	$0x9, %edx
 4912dad:      	xorl	%esi, %edx
 4912daf:      	leal	-0x1(%rcx), %esi
 4912db2:      	andl	%esi, %edx
 4912db4:      	movl	%edx, %edi
 4912db6:      	shll	$0x4, %edi
 4912db9:      	movq	(%rax,%rdi), %r9
 4912dbd:      	cmpq	%r9, %r15
 4912dc0:      	je	0x4912ebe <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa0e>
 4912dc6:      	movl	$0x1, %r8d
 4912dcc:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 4912dd3:      	je	0x4912eb7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa07>
 4912dd9:      	addl	%r8d, %edx
 4912ddc:      	incl	%r8d
 4912ddf:      	andl	%esi, %edx
 4912de1:      	movq	%rdx, %r9
 4912de4:      	shlq	$0x4, %r9
 4912de8:      	leaq	(%rax,%r9), %rdi
 4912dec:      	movq	(%rax,%r9), %r9
 4912df0:      	cmpq	%r9, %r15
 4912df3:      	je	0x4912ec1 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa11>
 4912df9:      	jmp	0x4912dcc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x91c>
 4912dfb:      	nopl	(%rax,%rax)
 4912e00:      	movq	%rbp, %rdi
 4912e03:      	movq	%r12, %rsi
 4912e06:      	callq	0x49113a0 <_ZN5clang7CodeGen11CodeGenTBAA11getTypeInfoENS_8QualTypeE>
 4912e0b:      	movq	%rax, 0x8(%rsp)
 4912e10:      	cmpq	$0x0, 0x8(%rsp)
 4912e16:      	je	0x491257a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912e1c:      	testb	$-0x80, 0x1d(%rbx)
 4912e20:      	movq	%rbx, %r15
 4912e23:      	je	0x4912e30 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x980>
 4912e25:      	movq	%rbx, %rdi
 4912e28:      	callq	0x753cf50 <_ZN5clang20getPrimaryMergedDeclEPNS_4DeclE>
 4912e2d:      	movq	%rax, %r15
 4912e30:      	movl	0x44(%r15), %eax
 4912e34:      	cmpl	$0xf, %eax
 4912e37:      	ja	0x4912e45 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x995>
 4912e39:      	movq	%r15, %rdi
 4912e3c:      	callq	0x754d7b0 <_ZNK5clang9FieldDecl19setCachedFieldIndexEv>
 4912e41:      	movl	0x44(%r15), %eax
 4912e45:      	shrl	$0x4, %eax
 4912e48:      	decl	%eax
 4912e4a:      	movq	0x30(%rsp), %rcx
 4912e4f:      	movq	0x30(%rcx), %rcx
 4912e53:      	movq	(%rcx,%rax,8), %r14
 4912e57:      	movq	(%rbp), %rsi
 4912e5b:      	movq	0x49a0(%rsi), %rax
 4912e62:      	andq	$-0x10, %rax
 4912e66:      	movq	(%rax), %rax
 4912e69:      	movq	%rax, 0x100(%rsp)
 4912e71:      	movq	0x478(%rsi), %rcx
 4912e78:      	movl	0x488(%rsi), %edx
 4912e7e:      	testq	%rdx, %rdx
 4912e81:      	je	0x4912f5b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xaab>
 4912e87:      	movl	%eax, %r8d
 4912e8a:      	shrl	$0x4, %r8d
 4912e8e:      	movl	%eax, %edi
 4912e90:      	shrl	$0x9, %edi
 4912e93:      	xorl	%r8d, %edi
 4912e96:      	leal	-0x1(%rdx), %r8d
 4912e9a:      	andl	%r8d, %edi
 4912e9d:      	leaq	(%rdi,%rdi,2), %r9
 4912ea1:      	movq	(%rcx,%r9,8), %r11
 4912ea5:      	cmpq	%r11, %rax
 4912ea8:      	jne	0x4912f30 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa80>
 4912eae:      	leaq	(%rcx,%r9,8), %r10
 4912eb2:      	jmp	0x4912f63 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xab3>
 4912eb7:      	movq	%rcx, %rdi
 4912eba:      	shlq	$0x4, %rdi
 4912ebe:      	addq	%rax, %rdi
 4912ec1:      	shlq	$0x4, %rcx
 4912ec5:      	addq	%rcx, %rax
 4912ec8:      	cmpq	%rax, %rdi
 4912ecb:      	je	0x4912ee7 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa37>
 4912ecd:      	movq	0x8(%rdi), %rax
 4912ed1:      	movq	%rax, 0x8(%rsp)
 4912ed6:      	cmpq	$0x0, 0x8(%rsp)
 4912edc:      	jne	0x4912e1c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x96c>
 4912ee2:      	jmp	0x491257a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912ee7:      	movq	%rbp, %rdi
 4912eea:      	movq	%r15, %rsi
 4912eed:      	callq	0x49124b0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE>
 4912ef2:      	movq	%r15, 0x100(%rsp)
 4912efa:      	movq	%rax, 0x8(%rsp)
 4912eff:      	movq	%rax, 0x108(%rsp)
 4912f07:      	movq	0xf8(%rsp), %rdi
 4912f0f:      	movq	%r13, %rsi
 4912f12:      	leaq	0x108(%rsp), %rdx
 4912f1a:      	callq	0x4913fe0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeEPNS_6MDNodeENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIS5_JS7_EEESt4pairIPSC_bEOT_DpOT0_>
 4912f1f:      	cmpq	$0x0, 0x8(%rsp)
 4912f25:      	jne	0x4912e1c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x96c>
 4912f2b:      	jmp	0x491257a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xca>
 4912f30:      	movl	$0x1, %r9d
 4912f36:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 4912f3d:      	je	0x4912f5b <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xaab>
 4912f3f:      	addl	%r9d, %edi
 4912f42:      	incl	%r9d
 4912f45:      	andl	%r8d, %edi
 4912f48:      	leaq	(%rdi,%rdi,2), %r11
 4912f4c:      	leaq	(%rcx,%r11,8), %r10
 4912f50:      	movq	(%rcx,%r11,8), %r11
 4912f54:      	cmpq	%r11, %rax
 4912f57:      	je	0x4912f63 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xab3>
 4912f59:      	jmp	0x4912f36 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xa86>
 4912f5b:      	leaq	(%rdx,%rdx,2), %rdi
 4912f5f:      	leaq	(%rcx,%rdi,8), %r10
 4912f63:      	leaq	(%rdx,%rdx,2), %rdx
 4912f67:      	leaq	(%rcx,%rdx,8), %rcx
 4912f6b:      	cmpq	%rcx, %r10
 4912f6e:      	je	0x4912f8d <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xadd>
 4912f70:      	movq	0x8(%r10), %rbp
 4912f74:      	movq	%r14, %rax
 4912f77:      	orq	%rbp, %rax
 4912f7a:      	shrq	$0x20, %rax
 4912f7e:      	je	0x4912fd9 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb29>
 4912f80:      	movq	%r14, %rax
 4912f83:      	xorl	%edx, %edx
 4912f85:      	divq	%rbp
 4912f88:      	movq	%rax, %r15
 4912f8b:      	jmp	0x4912fe3 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb33>
 4912f8d:      	leaq	0x478(%rsi), %rcx
 4912f94:      	movq	%rcx, 0x20(%rsp)
 4912f99:      	movq	%rsi, %rdi
 4912f9c:      	movq	%rax, %rsi
 4912f9f:      	callq	0x734fd90 <_ZNK5clang10ASTContext15getTypeInfoImplEPKNS_4TypeE>
 4912fa4:      	movq	%rax, %rbp
 4912fa7:      	movq	%r12, %r15
 4912faa:      	movq	%rdx, %r12
 4912fad:      	movq	0x20(%rsp), %rdi
 4912fb2:      	movq	%r13, %rsi
 4912fb5:      	callq	0x73a1190 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang4TypeENS2_8TypeInfoENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S6_EEEES5_S6_S8_SB_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSB_bEOT_DpOT0_>
 4912fba:      	movq	%rbp, 0x8(%rax)
 4912fbe:      	movq	%r12, 0x10(%rax)
 4912fc2:      	movq	%r15, %r12
 4912fc5:      	movq	0x18(%rsp), %rax
 4912fca:      	movq	(%rax), %rsi
 4912fcd:      	movq	%r14, %rax
 4912fd0:      	orq	%rbp, %rax
 4912fd3:      	shrq	$0x20, %rax
 4912fd7:      	jne	0x4912f80 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xad0>
 4912fd9:      	movl	%r14d, %eax
 4912fdc:      	xorl	%edx, %edx
 4912fde:      	divl	%ebp
 4912fe0:      	movl	%eax, %r15d
 4912fe3:      	movq	%r13, %rdi
 4912fe6:      	movq	%r12, %rdx
 4912fe9:      	callq	0x73519b0 <_ZNK5clang10ASTContext18getTypeInfoInCharsENS_8QualTypeE>
 4912fee:      	movq	0x100(%rsp), %rax
 4912ff6:      	movq	%r15, 0x100(%rsp)
 4912ffe:      	movq	%rax, 0x108(%rsp)
 4913006:      	movq	0x8(%rsp), %rax
 491300b:      	movq	%rax, 0x110(%rsp)
 4913013:      	movl	0x90(%rsp), %edx
 491301a:      	movq	0x88(%rsp), %rax
 4913022:      	cmpl	0x94(%rsp), %edx
 4913029:      	movq	0x18(%rsp), %rbp
 491302e:      	jae	0x4913081 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xbd1>
 4913030:      	movq	%r13, %r14
 4913033:      	movl	0x90(%rsp), %ecx
 491303a:      	leaq	(%rcx,%rcx,2), %rcx
 491303e:      	movq	0x10(%r14), %rdx
 4913042:      	movq	%rdx, 0x10(%rax,%rcx,8)
 4913047:      	movups	(%r14), %xmm0
 491304b:      	movups	%xmm0, (%rax,%rcx,8)
 491304f:      	incl	0x90(%rsp)
 4913056:      	nopw	%cs:(%rax,%rax)
 4913060:      	movq	0x8(%rbx), %rbx
 4913064:      	andq	$-0x8, %rbx
 4913068:      	je	0x4912cd0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x820>
 491306e:      	movl	0x1c(%rbx), %eax
 4913071:      	andl	$0x7f, %eax
 4913074:      	addl	$-0x31, %eax
 4913077:      	cmpl	$0x3, %eax
 491307a:      	jae	0x4913060 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xbb0>
 491307c:      	jmp	0x4912cd0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x820>
 4913081:      	leaq	(%rdx,%rdx,2), %rcx
 4913085:      	incq	%rdx
 4913088:      	leaq	(%rax,%rcx,8), %rcx
 491308c:      	movq	%r13, %r14
 491308f:      	subq	%rax, %r14
 4913092:      	setb	%al
 4913095:      	cmpq	%rcx, %r13
 4913098:      	setae	%cl
 491309b:      	orb	%al, %cl
 491309d:      	je	0x49130c6 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc16>
 491309f:      	movl	$0x18, %ecx
 49130a4:      	leaq	0x88(%rsp), %rdi
 49130ac:      	leaq	0x98(%rsp), %rsi
 49130b4:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 49130b9:      	movq	0x88(%rsp), %rax
 49130c1:      	jmp	0x4913030 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb80>
 49130c6:      	movl	$0x18, %ecx
 49130cb:      	leaq	0x88(%rsp), %rdi
 49130d3:      	leaq	0x98(%rsp), %rsi
 49130db:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 49130e0:      	movq	0x88(%rsp), %rax
 49130e8:      	addq	%rax, %r14
 49130eb:      	jmp	0x4913033 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xb83>
 49130f0:      	movq	0x38(%rsp), %rcx
 49130f5:      	movl	%r8d, %r8d
 49130f8:      	movq	0x18(%rsp), %rbp
 49130fd:      	leaq	0x118(%rsp), %r14
 4913105:      	jmp	0x491314c <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xc9c>
 4913107:      	movq	0x10(%rax), %r12
 491310b:      	movl	(%r12), %r15d
 491310f:      	cmpq	$0x101, %r15            # imm = 0x101
 4913116:      	jb	0x49131fb <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd4b>
 491311c:      	leaq	0x100(%rsp), %rdi
 4913124:      	movl	$0x1, %ecx
 4913129:      	movq	%r14, %rsi
 491312c:      	movq	%r15, %rdx
 491312f:      	callq	0x40f8880 <_ZN4llvm15SmallVectorBaseImE8grow_podEPvmm>
 4913134:      	movq	0x100(%rsp), %rdi
 491313c:      	movq	0x108(%rsp), %rax
 4913144:      	jmp	0x491320a <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd5a>
 4913149:      	movq	%r15, %rcx
 491314c:      	addq	$0x30, %rbp
 4913150:      	movq	0x100(%rsp), %rsi
 4913158:      	movq	0x108(%rsp), %rdx
 4913160:      	movq	%rbp, %rdi
 4913163:      	callq	0x3bd08b0 <_ZN4llvm9MDBuilder24createTBAAStructTypeNodeENS_9StringRefENS_8ArrayRefISt4pairIPNS_6MDNodeEmEEE>
 4913168:      	movq	%rax, %rbx
 491316b:      	movq	0x38(%rsp), %rdi
 4913170:      	cmpq	%r15, %rdi
 4913173:      	je	0x49132e2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe32>
 4913179:      	callq	0x828a640 <free@plt>
 491317e:      	jmp	0x49132e2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe32>
 4913183:      	addq	$0x180, %rbx            # imm = 0x180
 491318a:      	movq	0x18(%rsp), %rbp
 491318f:      	jmp	0x49131bc <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd0c>
 4913191:      	nopw	%cs:(%rax,%rax)
 491319b:      	nopl	(%rax,%rax)
 49131a0:      	movq	%rax, (%rcx)
 49131a3:      	movaps	0x100(%rsp), %xmm0
 49131ab:      	movups	%xmm0, 0x8(%rcx)
 49131af:      	addq	$0x18, %rbx
 49131b3:      	cmpq	%r12, %rbx
 49131b6:      	je	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 49131bc:      	movq	(%rbx), %rax
 49131bf:      	movups	0x8(%rbx), %xmm0
 49131c3:      	movaps	%xmm0, 0x100(%rsp)
 49131cb:      	movq	%rbx, %rcx
 49131ce:      	cmpq	-0x18(%rbx), %rax
 49131d2:      	jae	0x49131a0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xcf0>
 49131d4:      	movq	%rbx, %rcx
 49131d7:      	nopw	(%rax,%rax)
 49131e0:      	movq	-0x8(%rcx), %rdx
 49131e4:      	movq	%rdx, 0x10(%rcx)
 49131e8:      	movups	-0x18(%rcx), %xmm0
 49131ec:      	movups	%xmm0, (%rcx)
 49131ef:      	cmpq	-0x30(%rcx), %rax
 49131f3:      	leaq	-0x18(%rcx), %rcx
 49131f7:      	jb	0x49131e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd30>
 49131f9:      	jmp	0x49131a0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xcf0>
 49131fb:      	xorl	%eax, %eax
 49131fd:      	movq	%r14, %rdi
 4913200:      	movl	$0x0, %ecx
 4913205:      	testq	%r15, %r15
 4913208:      	je	0x4913227 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xd77>
 491320a:      	addq	%rax, %rdi
 491320d:      	addq	$0x10, %r12
 4913211:      	movq	%r12, %rsi
 4913214:      	movq	%r15, %rdx
 4913217:      	callq	0x828ac50 <memcpy@plt>
 491321c:      	movq	0x108(%rsp), %rcx
 4913224:      	movq	%r15, %rax
 4913227:      	addq	%rcx, %rax
 491322a:      	movq	%rax, 0x108(%rsp)
 4913232:      	movq	0x18(%rbp), %rax
 4913236:      	movabsq	$0x1000000000, %rcx     # imm = 0x1000000000
 4913240:      	testq	%rcx, 0x30(%rax)
 4913244:      	je	0x4912c08 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x758>
 491324a:      	movq	%rbp, %rdi
 491324d:      	callq	0x49103d0 <_ZN5clang7CodeGen11CodeGenTBAA7getCharEv>
 4913252:      	movq	%rax, %r15
 4913255:      	movq	(%rbp), %rsi
 4913259:      	leaq	0x38(%rsp), %rdi
 491325e:      	movq	%rbx, %rdx
 4913261:      	callq	0x7351cf0 <_ZNK5clang10ASTContext18getTypeInfoInCharsEPKNS_4TypeE>
 4913266:      	movq	0x38(%rsp), %r12
 491326b:      	movq	0x100(%rsp), %r14
 4913273:      	movq	0x108(%rsp), %r13
 491327b:      	movq	0x30(%rbp), %rax
 491327f:      	addq	$0x30, %rbp
 4913283:      	movq	%rbp, %rbx
 4913286:      	movl	$0x178, %ebp            # imm = 0x178
 491328b:      	addq	(%rax), %rbp
 491328e:      	movq	%r14, %rdi
 4913291:      	movq	%r13, %rsi
 4913294:      	callq	0x414fb70 <_ZN4llvm11xxh3_64bitsENS_8ArrayRefIhEE>
 4913299:      	movq	%rbp, %rdi
 491329c:      	movq	%r14, %rsi
 491329f:      	movq	%r13, %rdx
 49132a2:      	movl	%eax, %ecx
 49132a4:      	callq	0x3bed130 <_ZN4llvm9StringMapINS_8MDStringENS_20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EEEE21try_emplace_with_hashIJEEESt4pairINS_17StringMapIterBaseIS1_Lb0EEEbENS_9StringRefEjDpOT_>
 49132a9:      	movq	(%rax), %rcx
 49132ac:      	cmpb	$0x1, %dl
 49132af:      	jne	0x49132b5 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe05>
 49132b1:      	movq	%rcx, 0x10(%rcx)
 49132b5:      	addq	$0x8, %rcx
 49132b9:      	movq	0x88(%rsp), %r8
 49132c1:      	movl	0x90(%rsp), %r9d
 49132c9:      	movq	%rbx, %rdi
 49132cc:      	movq	%r15, %rsi
 49132cf:      	movq	%r12, %rdx
 49132d2:      	callq	0x3bd10a0 <_ZN4llvm9MDBuilder18createTBAATypeNodeEPNS_6MDNodeEmPNS_8MetadataENS_8ArrayRefINS0_15TBAAStructFieldEEE>
 49132d7:      	movq	%rax, %rbx
 49132da:      	leaq	0x118(%rsp), %r14
 49132e2:      	movq	0x100(%rsp), %rdi
 49132ea:      	cmpq	%r14, %rdi
 49132ed:      	je	0x49132f4 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe44>
 49132ef:      	callq	0x828a640 <free@plt>
 49132f4:      	movq	0x88(%rsp), %rdi
 49132fc:      	leaq	0x98(%rsp), %rax
 4913304:      	cmpq	%rax, %rdi
 4913307:      	je	0x491330e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe5e>
 4913309:      	callq	0x828a640 <free@plt>
 491330e:      	movq	%rbx, %rax
 4913311:      	addq	$0x218, %rsp            # imm = 0x218
 4913318:      	popq	%rbx
 4913319:      	popq	%r12
 491331b:      	popq	%r13
 491331d:      	popq	%r14
 491331f:      	popq	%r15
 4913321:      	popq	%rbp
 4913322:      	retq
 4913323:      	movabsq	$-0x5555555555555555, %r14 # imm = 0xAAAAAAAAAAAAAAAB
 491332d:      	movq	%rbx, %rax
 4913330:      	jmp	0x491335f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xeaf>
 4913332:      	nopw	%cs:(%rax,%rax)
 491333c:      	nopl	(%rax)
 4913340:      	movq	%rcx, (%rdx)
 4913343:      	movaps	0x100(%rsp), %xmm0
 491334b:      	movups	%xmm0, 0x8(%rdx)
 491334f:      	leaq	0x18(%r13), %r15
 4913353:      	movq	%r13, %rax
 4913356:      	cmpq	%r12, %r15
 4913359:      	je	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 491335f:      	movq	%r15, %r13
 4913362:      	movq	(%r15), %rcx
 4913365:      	cmpq	(%rbx), %rcx
 4913368:      	jae	0x49133e0 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf30>
 491336a:      	movq	0x10(%r13), %rcx
 491336e:      	movq	%rcx, 0x110(%rsp)
 4913376:      	movups	(%r13), %xmm0
 491337b:      	movaps	%xmm0, 0x100(%rsp)
 4913383:      	movq	%r13, %rdx
 4913386:      	subq	%rbx, %rdx
 4913389:      	cmpq	$0x19, %rdx
 491338d:      	jl	0x491341e <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf6e>
 4913393:      	movq	%rdx, %rcx
 4913396:      	shrq	$0x3, %rcx
 491339a:      	imulq	%r14, %rcx
 491339e:      	negq	%rcx
 49133a1:      	leaq	(%rcx,%rcx,2), %rcx
 49133a5:      	leaq	0x30(%rax,%rcx,8), %rdi
 49133aa:      	movq	%rbx, %rsi
 49133ad:      	callq	0x828abc0 <memmove@plt>
 49133b2:      	movq	0x110(%rsp), %rax
 49133ba:      	movq	%rax, 0x10(%rbx)
 49133be:      	movaps	0x100(%rsp), %xmm0
 49133c6:      	movups	%xmm0, (%rbx)
 49133c9:      	leaq	0x18(%r13), %r15
 49133cd:      	movq	%r13, %rax
 49133d0:      	cmpq	%r12, %r15
 49133d3:      	jne	0x491335f <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xeaf>
 49133d5:      	jmp	0x4912a99 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0x5e9>
 49133da:      	nopw	(%rax,%rax)
 49133e0:      	movups	0x20(%rax), %xmm0
 49133e4:      	movaps	%xmm0, 0x100(%rsp)
 49133ec:      	movq	%r13, %rdx
 49133ef:      	cmpq	(%rax), %rcx
 49133f2:      	jae	0x4913340 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe90>
 49133f8:      	movq	%r13, %rdx
 49133fb:      	nopl	(%rax,%rax)
 4913400:      	movq	-0x8(%rdx), %rax
 4913404:      	movq	%rax, 0x10(%rdx)
 4913408:      	movups	-0x18(%rdx), %xmm0
 491340c:      	movups	%xmm0, (%rdx)
 491340f:      	cmpq	-0x30(%rdx), %rcx
 4913413:      	leaq	-0x18(%rdx), %rdx
 4913417:      	jb	0x4913400 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf50>
 4913419:      	jmp	0x4913340 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xe90>
 491341e:      	cmpq	$0x18, %rdx
 4913422:      	jne	0x49133b2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf02>
 4913424:      	movq	0x10(%rbx), %rcx
 4913428:      	movq	%rcx, 0x28(%rax)
 491342c:      	movups	(%rbx), %xmm0
 491342f:      	movups	%xmm0, 0x18(%rax)
 4913433:      	jmp	0x49133b2 <_ZN5clang7CodeGen11CodeGenTBAA21getBaseTypeInfoHelperEPKNS_4TypeE+0xf02>
