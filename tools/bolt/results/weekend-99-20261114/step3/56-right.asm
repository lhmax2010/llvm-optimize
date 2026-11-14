
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000722a3e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE>:
 722a3e0:      	pushq	%rbp
 722a3e1:      	pushq	%r15
 722a3e3:      	pushq	%r14
 722a3e5:      	pushq	%r13
 722a3e7:      	pushq	%r12
 722a3e9:      	pushq	%rbx
 722a3ea:      	subq	$0xce8, %rsp            # imm = 0xCE8
 722a3f1:      	movq	%rsi, 0x70(%rsp)
 722a3f6:      	movq	0x8(%rdi), %rdi
 722a3fa:      	movl	0x118(%rdi), %r14d
 722a401:      	testq	%r14, %r14
 722a404:      	je	0x722a46f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x8f>
 722a406:      	movq	%rdi, %rbx
 722a409:      	leaq	(,%r14,8), %rdi
 722a411:      	callq	0x828a620 <_Znwm@plt>
 722a416:      	movq	%rbx, %rdi
 722a419:      	movq	%rax, %rbx
 722a41c:      	leaq	(%rax,%r14,8), %r8
 722a420:      	movq	0x110(%rdi), %rax
 722a427:      	movl	0x120(%rdi), %r15d
 722a42e:      	movq	%r15, %rcx
 722a431:      	shlq	$0x5, %rcx
 722a435:      	leaq	(%rax,%rcx), %r12
 722a439:      	testq	%r15, %r15
 722a43c:      	je	0x722a6b1 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2d1>
 722a442:      	xorl	%r13d, %r13d
 722a445:      	movl	$0x1000, %edx           # imm = 0x1000
 722a44a:      	nopw	(%rax,%rax)
 722a450:      	movq	(%rax,%r13), %rsi
 722a454:      	orq	%rdx, %rsi
 722a457:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 722a45e:      	jne	0x722a70d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x32d>
 722a464:      	addq	$0x20, %r13
 722a468:      	cmpq	%r13, %rcx
 722a46b:      	jne	0x722a450 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x70>
 722a46d:      	jmp	0x722a48c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xac>
 722a46f:      	movq	0x110(%rdi), %rax
 722a476:      	movl	0x120(%rdi), %r15d
 722a47d:      	movq	%r15, %r12
 722a480:      	shlq	$0x5, %r12
 722a484:      	addq	%rax, %r12
 722a487:      	xorl	%r8d, %r8d
 722a48a:      	xorl	%ebx, %ebx
 722a48c:      	movq	%r12, %r13
 722a48f:      	shlq	$0x5, %r15
 722a493:      	addq	%rax, %r15
 722a496:      	cmpq	%r15, %r13
 722a499:      	je	0x722a6c7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2e7>
 722a49f:      	addq	$0x110, %rdi            # imm = 0x110
 722a4a6:      	xorl	%ebp, %ebp
 722a4a8:      	movl	$0x1000, %ecx           # imm = 0x1000
 722a4ad:      	movq	%r13, %rdx
 722a4b0:      	jmp	0x722a4c9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe9>
 722a4b2:      	nopw	%cs:(%rax,%rax)
 722a4bc:      	nopl	(%rax)
 722a4c0:      	leaq	0x1(%rax), %rbp
 722a4c4:      	cmpq	%r15, %rdx
 722a4c7:      	je	0x722a4ea <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10a>
 722a4c9:      	movq	%rbp, %rax
 722a4cc:      	nopl	(%rax)
 722a4d0:      	addq	$0x20, %rdx
 722a4d4:      	cmpq	%r12, %rdx
 722a4d7:      	je	0x722a4c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe0>
 722a4d9:      	movq	(%rdx), %rsi
 722a4dc:      	orq	%rcx, %rsi
 722a4df:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 722a4e6:      	je	0x722a4d0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf0>
 722a4e8:      	jmp	0x722a4c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe0>
 722a4ea:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 722a4f4:      	movq	%r8, %r14
 722a4f7:      	subq	%rbx, %r14
 722a4fa:      	movq	%r14, %rcx
 722a4fd:      	sarq	$0x3, %rcx
 722a501:      	cmpq	%rax, %rcx
 722a504:      	movq	%rdi, 0x40(%rsp)
 722a509:      	jbe	0x722a54b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16b>
 722a50b:      	movl	$0x1000, %eax           # imm = 0x1000
 722a510:      	movq	%rbx, %rcx
 722a513:      	jmp	0x722a529 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x149>
 722a515:      	nopw	%cs:(%rax,%rax)
 722a51f:      	nop
 722a520:      	addq	$0x8, %rcx
 722a524:      	cmpq	%r15, %r13
 722a527:      	je	0x722a59b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1bb>
 722a529:      	movq	(%r13), %rdx
 722a52d:      	movq	%rdx, (%rcx)
 722a530:      	addq	$0x20, %r13
 722a534:      	cmpq	%r12, %r13
 722a537:      	je	0x722a520 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x140>
 722a539:      	movq	(%r13), %rdx
 722a53d:      	orq	%rax, %rdx
 722a540:      	cmpq	$-0x1000, %rdx          # imm = 0xF000
 722a547:      	je	0x722a530 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x150>
 722a549:      	jmp	0x722a520 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x140>
 722a54b:      	cmpq	%rdx, %rax
 722a54e:      	jae	0x722c044 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c64>
 722a554:      	leaq	(,%rbp,8), %rdi
 722a55c:      	callq	0x828a620 <_Znwm@plt>
 722a561:      	movl	$0x1000, %edx           # imm = 0x1000
 722a566:      	movq	%rax, 0x10(%rsp)
 722a56b:      	jmp	0x722a579 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x199>
 722a56d:      	nopl	(%rax)
 722a570:      	addq	$0x8, %rax
 722a574:      	cmpq	%r15, %r13
 722a577:      	je	0x722a5a9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c9>
 722a579:      	movq	(%r13), %rcx
 722a57d:      	movq	%rcx, (%rax)
 722a580:      	addq	$0x20, %r13
 722a584:      	cmpq	%r12, %r13
 722a587:      	je	0x722a570 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x190>
 722a589:      	movq	(%r13), %rcx
 722a58d:      	orq	%rdx, %rcx
 722a590:      	cmpq	$-0x1000, %rcx          # imm = 0xF000
 722a597:      	je	0x722a580 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0>
 722a599:      	jmp	0x722a570 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x190>
 722a59b:      	movq	%r8, 0x38(%rsp)
 722a5a0:      	leaq	(%rbx,%rbp,8), %r15
 722a5a4:      	movq	%rbx, %r12
 722a5a7:      	jmp	0x722a5ca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1ea>
 722a5a9:      	movq	%rax, %r15
 722a5ac:      	testq	%rbx, %rbx
 722a5af:      	je	0x722a5bc <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1dc>
 722a5b1:      	movq	%rbx, %rdi
 722a5b4:      	movq	%r14, %rsi
 722a5b7:      	callq	0x828a660 <_ZdlPvm@plt>
 722a5bc:      	movq	0x10(%rsp), %r12
 722a5c1:      	leaq	(%r12,%rbp,8), %rax
 722a5c5:      	movq	%rax, 0x38(%rsp)
 722a5ca:      	movq	%r15, %r14
 722a5cd:      	subq	%r12, %r14
 722a5d0:      	movq	%r14, %rax
 722a5d3:      	sarq	$0x3, %rax
 722a5d7:      	bsrq	%rax, %rdx
 722a5db:      	xorl	$0x3f, %edx
 722a5de:      	addl	%edx, %edx
 722a5e0:      	xorq	$0x7e, %rdx
 722a5e4:      	movq	%r12, %rdi
 722a5e7:      	movq	%r15, %rsi
 722a5ea:      	callq	0x7231d80 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN5clang8CFGBlockESt6vectorIS5_SaIS5_EEEElNS0_5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117LiveVariablesImpl17dumpBlockLivenessERKNS2_13SourceManagerEE3$_0EEEvT_SK_T0_T1_>
 722a5ef:      	leaq	0x8(%r12), %rbx
 722a5f4:      	cmpq	$0x81, %r14
 722a5fb:      	movq	%r12, 0x10(%rsp)
 722a600:      	movq	%r15, 0x28(%rsp)
 722a605:      	jl	0x722a617 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x237>
 722a607:      	leaq	0x8(%r12), %r15
 722a60c:      	movl	$0x8, %r14d
 722a612:      	jmp	0x722a745 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x365>
 722a617:      	cmpq	%r15, %rbx
 722a61a:      	je	0x722a802 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a620:      	movq	%r12, %r14
 722a623:      	jmp	0x722a66b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x28b>
 722a625:      	nopw	%cs:(%rax,%rax)
 722a62f:      	nop
 722a630:      	movq	%r14, %rdx
 722a633:      	subq	%r12, %rdx
 722a636:      	movq	%rdx, %rax
 722a639:      	sarq	$0x3, %rax
 722a63d:      	cmpq	$0x2, %rax
 722a641:      	jl	0x722a6a2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2c2>
 722a643:      	shlq	$0x3, %rax
 722a647:      	subq	%rax, %rdi
 722a64a:      	addq	$0x10, %rdi
 722a64e:      	movq	%r12, %rsi
 722a651:      	callq	0x828abc0 <memmove@plt>
 722a656:      	movq	%r12, %rax
 722a659:      	movq	%rbx, (%rax)
 722a65c:      	leaq	0x8(%r14), %rbx
 722a660:      	cmpq	0x28(%rsp), %rbx
 722a665:      	je	0x722a802 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a66b:      	movq	%r14, %rdi
 722a66e:      	movq	%rbx, %r14
 722a671:      	movq	(%rbx), %rbx
 722a674:      	movq	(%r12), %rsi
 722a678:      	movl	0x30(%rbx), %ecx
 722a67b:      	cmpl	0x30(%rsi), %ecx
 722a67e:      	jb	0x722a630 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x250>
 722a680:      	movq	(%rdi), %rdx
 722a683:      	movq	%r14, %rax
 722a686:      	cmpl	0x30(%rdx), %ecx
 722a689:      	jae	0x722a659 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a68b:      	movq	%r14, %rax
 722a68e:      	nop
 722a690:      	movq	%rdx, (%rax)
 722a693:      	movq	-0x10(%rax), %rdx
 722a697:      	addq	$-0x8, %rax
 722a69b:      	cmpl	0x30(%rdx), %ecx
 722a69e:      	jb	0x722a690 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2b0>
 722a6a0:      	jmp	0x722a659 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a6a2:      	movq	%r12, %rax
 722a6a5:      	cmpq	$0x8, %rdx
 722a6a9:      	jne	0x722a659 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a6ab:      	movq	%rsi, 0x8(%rdi)
 722a6af:      	jmp	0x722a656 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x276>
 722a6b1:      	xorl	%r15d, %r15d
 722a6b4:      	movq	%rax, %r13
 722a6b7:      	shlq	$0x5, %r15
 722a6bb:      	addq	%rax, %r15
 722a6be:      	cmpq	%r15, %r13
 722a6c1:      	jne	0x722a49f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbf>
 722a6c7:      	movq	%r8, 0x38(%rsp)
 722a6cc:      	xorl	%r14d, %r14d
 722a6cf:      	movq	$0x0, 0x20(%rsp)
 722a6d8:      	callq	0x41460e0 <_ZN4llvm4errsEv>
 722a6dd:      	movq	0x20(%rax), %rcx
 722a6e1:      	cmpq	%rcx, 0x18(%rax)
 722a6e5:      	jne	0x722c001 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c21>
 722a6eb:      	leaq	-0x64d225d(%rip), %rsi  # 0xd58495 <.str.llvm.17513262558703275235>
 722a6f2:      	movl	$0x1, %edx
 722a6f7:      	movq	%rax, %rdi
 722a6fa:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a6ff:      	testq	%r14, %r14
 722a702:      	jne	0x722c00d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c2d>
 722a708:      	jmp	0x722c01d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c3d>
 722a70d:      	addq	%rax, %r13
 722a710:      	shlq	$0x5, %r15
 722a714:      	addq	%rax, %r15
 722a717:      	cmpq	%r15, %r13
 722a71a:      	jne	0x722a49f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbf>
 722a720:      	jmp	0x722a6c7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2e7>
 722a722:      	movq	%rdx, 0x8(%rcx)
 722a726:      	movq	0x10(%rsp), %rbp
 722a72b:      	nopl	(%rax,%rax)
 722a730:      	movq	%r13, (%rbp)
 722a734:      	addq	$0x8, %r14
 722a738:      	addq	$0x8, %r15
 722a73c:      	cmpq	$0x80, %r14
 722a743:      	je	0x722a7a3 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3c3>
 722a745:      	movq	%r12, %rcx
 722a748:      	movq	0x10(%rsp), %rax
 722a74d:      	leaq	(%rax,%r14), %r12
 722a751:      	movq	(%rax,%r14), %r13
 722a755:      	movq	(%rax), %rdx
 722a758:      	movl	0x30(%r13), %eax
 722a75c:      	cmpl	0x30(%rdx), %eax
 722a75f:      	jae	0x722a780 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3a0>
 722a761:      	cmpq	$0x9, %r14
 722a765:      	jb	0x722a722 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x342>
 722a767:      	movq	%rbx, %rdi
 722a76a:      	movq	0x10(%rsp), %rbp
 722a76f:      	movq	%rbp, %rsi
 722a772:      	movq	%r14, %rdx
 722a775:      	callq	0x828abc0 <memmove@plt>
 722a77a:      	jmp	0x722a730 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a77c:      	nopl	(%rax)
 722a780:      	movq	(%rcx), %rdx
 722a783:      	movq	%r12, %rbp
 722a786:      	cmpl	0x30(%rdx), %eax
 722a789:      	jae	0x722a730 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a78b:      	movq	%r15, %rbp
 722a78e:      	nop
 722a790:      	movq	%rdx, (%rbp)
 722a794:      	movq	-0x10(%rbp), %rdx
 722a798:      	addq	$-0x8, %rbp
 722a79c:      	cmpl	0x30(%rdx), %eax
 722a79f:      	jb	0x722a790 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3b0>
 722a7a1:      	jmp	0x722a730 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a7a3:      	movq	0x10(%rsp), %r12
 722a7a8:      	leaq	0x80(%r12), %rax
 722a7b0:      	jmp	0x722a7c7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e7>
 722a7b2:      	nopw	%cs:(%rax,%rax)
 722a7bc:      	nopl	(%rax)
 722a7c0:      	movq	%rcx, (%rdi)
 722a7c3:      	addq	$0x8, %rax
 722a7c7:      	cmpq	0x28(%rsp), %rax
 722a7cc:      	je	0x722a802 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a7ce:      	movq	-0x8(%rax), %rdx
 722a7d2:      	movq	(%rax), %rcx
 722a7d5:      	movl	0x30(%rcx), %esi
 722a7d8:      	movq	%rax, %rdi
 722a7db:      	cmpl	0x30(%rdx), %esi
 722a7de:      	jae	0x722a7c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e0>
 722a7e0:      	movq	%rax, %rdi
 722a7e3:      	nopw	%cs:(%rax,%rax)
 722a7ed:      	nopl	(%rax)
 722a7f0:      	movq	%rdx, (%rdi)
 722a7f3:      	movq	-0x10(%rdi), %rdx
 722a7f7:      	addq	$-0x8, %rdi
 722a7fb:      	cmpl	0x30(%rdx), %esi
 722a7fe:      	jb	0x722a7f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x410>
 722a800:      	jmp	0x722a7c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e0>
 722a802:      	leaq	0x1103e9f(%rip), %rax   # 0x832e6a8 <_ZTVN4llvm18raw_string_ostreamE>
 722a809:      	addq	$0x10, %rax
 722a80d:      	movq	%rax, 0x68(%rsp)
 722a812:      	leaq	0x1103a17(%rip), %rax   # 0x832e230 <_ZTVN4llvm11raw_ostreamE>
 722a819:      	addq	$0x10, %rax
 722a81d:      	movq	%rax, 0x60(%rsp)
 722a822:      	movq	$0x0, (%rsp)
 722a82a:      	xorl	%r13d, %r13d
 722a82d:      	movq	$0x0, 0x20(%rsp)
 722a836:      	jmp	0x722a854 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x474>
 722a838:      	nopl	(%rax,%rax)
 722a840:      	movq	0x50(%rsp), %r12
 722a845:      	addq	$0x8, %r12
 722a849:      	cmpq	0x28(%rsp), %r12
 722a84e:      	je	0x722bfe5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c05>
 722a854:      	movq	%r12, 0x50(%rsp)
 722a859:      	movq	(%r12), %r15
 722a85d:      	callq	0x41460e0 <_ZN4llvm4errsEv>
 722a862:      	movq	%rax, %r12
 722a865:      	movq	0x18(%rax), %rcx
 722a869:      	movq	0x20(%rax), %rax
 722a86d:      	subq	%rax, %rcx
 722a870:      	cmpq	$0x3, %rcx
 722a874:      	ja	0x722a890 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x4b0>
 722a876:      	movl	$0x4, %edx
 722a87b:      	movq	%r12, %rdi
 722a87e:      	leaq	-0x652bd1a(%rip), %rsi  # 0xcfeb6b <.L.str.1>
 722a885:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a88a:      	movq	%rax, %r12
 722a88d:      	jmp	0x722a89c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x4bc>
 722a88f:      	nop
 722a890:      	movl	$0x42205b0a, (%rax)     # imm = 0x42205B0A
 722a896:      	addq	$0x4, 0x20(%r12)
 722a89c:      	movl	0x30(%r15), %esi
 722a8a0:      	movq	%r12, %rdi
 722a8a3:      	xorl	%edx, %edx
 722a8a5:      	xorl	%ecx, %ecx
 722a8a7:      	xorl	%r8d, %r8d
 722a8aa:      	callq	0x40f17c0 <_ZL14write_unsignedImEvRN4llvm11raw_ostreamET_mNS0_12IntegerStyleEb.llvm.10233294383467268252>
 722a8af:      	movq	0x18(%r12), %rcx
 722a8b4:      	movq	0x20(%r12), %rax
 722a8b9:      	subq	%rax, %rcx
 722a8bc:      	cmpq	$0x21, %rcx
 722a8c0:      	ja	0x722a8e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x500>
 722a8c2:      	movl	$0x22, %edx
 722a8c7:      	movq	%r12, %rdi
 722a8ca:      	leaq	-0x65d987a(%rip), %rsi  # 0xc51057 <.L.str.2>
 722a8d1:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a8d6:      	jmp	0x722a901 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x521>
 722a8d8:      	nopl	(%rax,%rax)
 722a8e0:      	movups	-0x65d9880(%rip), %xmm0 # 0xc51067 <.L.str.2+0x10>
 722a8e7:      	movups	%xmm0, 0x10(%rax)
 722a8eb:      	movups	-0x65d989b(%rip), %xmm0 # 0xc51057 <.L.str.2>
 722a8f2:      	movups	%xmm0, (%rax)
 722a8f5:      	movw	$0xa5d, 0x20(%rax)      # imm = 0xA5D
 722a8fb:      	addq	$0x22, 0x20(%r12)
 722a901:      	movq	0x40(%rsp), %rdi
 722a906:      	movq	(%rsp), %rax
 722a90a:      	cmpq	%rax, %r13
 722a90d:      	cmovneq	%rax, %r13
 722a911:      	movq	%r15, %rsi
 722a914:      	callq	0x7236760 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang8CFGBlockENS2_13LiveVariables14LivenessValuesENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSC_bEOT_DpOT0_>
 722a919:      	movq	0x10(%rax), %rsi
 722a91d:      	leaq	0x4a8(%rsp), %rax
 722a925:      	movq	%rax, 0x498(%rsp)
 722a92d:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722a937:      	movq	%rax, 0x4a0(%rsp)
 722a93f:      	testq	%rsi, %rsi
 722a942:      	je	0x722aa60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722a948:      	movq	%rsi, 0x4a8(%rsp)
 722a950:      	movl	$0x1, 0x4a0(%rsp)
 722a95b:      	movl	$0x1, %eax
 722a960:      	leaq	0x4a8(%rsp), %rcx
 722a968:      	jmp	0x722a990 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x5b0>
 722a96a:      	orq	$0x3, %rsi
 722a96e:      	movq	%rsi, -0x8(%rcx,%rdx,8)
 722a973:      	movq	0x498(%rsp), %rcx
 722a97b:      	movl	%eax, %edx
 722a97d:      	movq	-0x8(%rcx,%rdx,8), %rsi
 722a982:      	movl	%esi, %edx
 722a984:      	andl	$0x3, %edx
 722a987:      	cmpl	$0x1, %edx
 722a98a:      	je	0x722ac90 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x8b0>
 722a990:      	movl	%esi, %edi
 722a992:      	andl	$0x3, %edi
 722a995:      	cmpq	$0x3, %rdi
 722a999:      	je	0x722a9c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x5e0>
 722a99b:      	movl	%eax, %edx
 722a99d:      	movq	%rsi, %r8
 722a9a0:      	andq	$-0x4, %r8
 722a9a4:      	cmpl	$0x1, %edi
 722a9a7:      	jne	0x722a9f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x610>
 722a9a9:      	movq	0x10(%r8), %rbx
 722a9ad:      	testq	%rbx, %rbx
 722a9b0:      	jne	0x722a9f9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x619>
 722a9b2:      	jmp	0x722a96a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x58a>
 722a9b4:      	nopw	%cs:(%rax,%rax)
 722a9be:      	nop
 722a9c0:      	decl	%eax
 722a9c2:      	movl	%eax, 0x4a0(%rsp)
 722a9c9:      	je	0x722aa60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722a9cf:      	movl	%eax, %edx
 722a9d1:      	movq	-0x8(%rcx,%rdx,8), %rsi
 722a9d6:      	xorl	%edi, %edi
 722a9d8:      	testb	$0x3, %sil
 722a9dc:      	setne	%dil
 722a9e0:      	addl	%edi, %edi
 722a9e2:      	orq	%rsi, %rdi
 722a9e5:      	orq	$0x1, %rdi
 722a9e9:      	movq	%rdi, -0x8(%rcx,%rdx,8)
 722a9ee:      	jmp	0x722a973 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x593>
 722a9f0:      	movq	0x8(%r8), %rbx
 722a9f4:      	testq	%rbx, %rbx
 722a9f7:      	je	0x722aa1e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x63e>
 722a9f9:      	cmpl	0x4a4(%rsp), %eax
 722aa00:      	jae	0x722aa27 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x647>
 722aa02:      	movq	%rbx, (%rcx,%rdx,8)
 722aa06:      	movl	0x4a0(%rsp), %eax
 722aa0d:      	incl	%eax
 722aa0f:      	movl	%eax, 0x4a0(%rsp)
 722aa16:      	jne	0x722a973 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x593>
 722aa1c:      	jmp	0x722aa60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722aa1e:      	orq	$0x1, %rsi
 722aa22:      	jmp	0x722a96e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x58e>
 722aa27:      	incq	%rdx
 722aa2a:      	movl	$0x8, %ecx
 722aa2f:      	leaq	0x498(%rsp), %rdi
 722aa37:      	leaq	0x4a8(%rsp), %rsi
 722aa3f:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722aa44:      	movl	0x4a0(%rsp), %edx
 722aa4b:      	movq	0x498(%rsp), %rcx
 722aa53:      	jmp	0x722aa02 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x622>
 722aa55:      	nopw	%cs:(%rax,%rax)
 722aa5f:      	nop
 722aa60:      	leaq	0x828(%rsp), %rax
 722aa68:      	movq	%rax, 0x818(%rsp)
 722aa70:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722aa7a:      	movq	%rax, 0x820(%rsp)
 722aa82:      	movq	0x498(%rsp), %rdi
 722aa8a:      	leaq	0x4a8(%rsp), %rax
 722aa92:      	cmpq	%rax, %rdi
 722aa95:      	je	0x722aa9c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6bc>
 722aa97:      	callq	0x828a640 <free@plt>
 722aa9c:      	leaq	0xc48(%rsp), %rax
 722aaa4:      	xorps	%xmm0, %xmm0
 722aaa7:      	movups	%xmm0, 0x90(%rax)
 722aaae:      	movups	%xmm0, 0x80(%rax)
 722aab5:      	movups	%xmm0, 0x70(%rax)
 722aab9:      	movups	%xmm0, 0x60(%rax)
 722aabd:      	movups	%xmm0, 0x50(%rax)
 722aac1:      	movups	%xmm0, 0x40(%rax)
 722aac5:      	movups	%xmm0, 0x30(%rax)
 722aac9:      	movups	%xmm0, 0x20(%rax)
 722aacd:      	movups	%xmm0, 0x10(%rax)
 722aad1:      	movups	%xmm0, (%rax)
 722aad4:      	movq	%rax, 0xc38(%rsp)
 722aadc:      	movabsq	$0x1400000000, %rdx     # imm = 0x1400000000
 722aae6:      	movq	%rdx, 0xc40(%rsp)
 722aaee:      	leaq	0x138(%rsp), %rax
 722aaf6:      	movq	%rax, 0x128(%rsp)
 722aafe:      	movq	%rdx, 0x130(%rsp)
 722ab06:      	movl	0x820(%rsp), %ebp
 722ab0d:      	testq	%rbp, %rbp
 722ab10:      	je	0x722ac60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x880>
 722ab16:      	movq	%rax, %rdi
 722ab19:      	movl	%ebp, %eax
 722ab1b:      	cmpl	$0x15, %ebp
 722ab1e:      	jb	0x722ab50 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x770>
 722ab20:      	movl	$0x8, %ecx
 722ab25:      	leaq	0x128(%rsp), %rdi
 722ab2d:      	leaq	0x138(%rsp), %rsi
 722ab35:      	movq	%rbp, %rdx
 722ab38:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722ab3d:      	movl	0x820(%rsp), %eax
 722ab44:      	testl	%eax, %eax
 722ab46:      	je	0x722ab63 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x783>
 722ab48:      	movq	0x128(%rsp), %rdi
 722ab50:      	movl	%eax, %edx
 722ab52:      	movq	0x818(%rsp), %rsi
 722ab5a:      	shlq	$0x3, %rdx
 722ab5e:      	callq	0x828ac50 <memcpy@plt>
 722ab63:      	movl	%ebp, 0x130(%rsp)
 722ab6a:      	movl	0xc40(%rsp), %r15d
 722ab72:      	leaq	0x1e8(%rsp), %rsi
 722ab7a:      	movq	%rsi, 0x1d8(%rsp)
 722ab82:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ab8c:      	movq	%rax, 0x1e0(%rsp)
 722ab94:      	testq	%r15, %r15
 722ab97:      	je	0x722acf0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x910>
 722ab9d:      	movq	%r15, %rdx
 722aba0:      	movq	%rsi, %rdi
 722aba3:      	cmpl	$0x15, %r15d
 722aba7:      	jb	0x722abd2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x7f2>
 722aba9:      	movl	$0x8, %ecx
 722abae:      	leaq	0x1d8(%rsp), %rdi
 722abb6:      	movq	%r15, %rdx
 722abb9:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722abbe:      	movl	0xc40(%rsp), %edx
 722abc5:      	testq	%rdx, %rdx
 722abc8:      	je	0x722abe3 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x803>
 722abca:      	movq	0x1d8(%rsp), %rdi
 722abd2:      	movq	0xc38(%rsp), %rsi
 722abda:      	shlq	$0x3, %rdx
 722abde:      	callq	0x828ac50 <memcpy@plt>
 722abe3:      	movl	%r15d, 0x1e0(%rsp)
 722abeb:      	movl	0x130(%rsp), %ebp
 722abf2:      	cmpl	%r15d, %ebp
 722abf5:      	jne	0x722ad07 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x927>
 722abfb:      	leaq	(,%r15,8), %rdx
 722ac03:      	movq	0x128(%rsp), %rdi
 722ac0b:      	movq	0x1d8(%rsp), %rsi
 722ac13:      	callq	0x828a6c0 <bcmp@plt>
 722ac18:      	testl	%eax, %eax
 722ac1a:      	je	0x722ae1f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa3f>
 722ac20:      	leaq	0x88(%rsp), %rax
 722ac28:      	movq	%rax, 0x78(%rsp)
 722ac2d:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ac37:      	movq	%rax, 0x80(%rsp)
 722ac3f:      	movl	%r15d, %ebp
 722ac42:      	cmpl	$0x15, %ebp
 722ac45:      	jae	0x722ad42 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x962>
 722ac4b:      	leaq	0x88(%rsp), %rdi
 722ac53:      	jmp	0x722ad79 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x999>
 722ac58:      	nopl	(%rax,%rax)
 722ac60:      	leaq	0x1e8(%rsp), %rcx
 722ac68:      	movq	%rcx, 0x1d8(%rsp)
 722ac70:      	movq	%rdx, 0x1e0(%rsp)
 722ac78:      	leaq	0x88(%rsp), %rbp
 722ac80:      	jmp	0x722b79e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13be>
 722ac85:      	nopw	%cs:(%rax,%rax)
 722ac8f:      	nop
 722ac90:      	leaq	0x828(%rsp), %rax
 722ac98:      	movq	%rax, 0x818(%rsp)
 722aca0:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722acaa:      	movq	%rax, 0x820(%rsp)
 722acb2:      	leaq	0x818(%rsp), %rdi
 722acba:      	leaq	0x498(%rsp), %rsi
 722acc2:      	callq	0x2a30b30 <_ZN4llvm15SmallVectorImplImEaSEOS1_>
 722acc7:      	movq	0x498(%rsp), %rdi
 722accf:      	leaq	0x4a8(%rsp), %rax
 722acd7:      	cmpq	%rax, %rdi
 722acda:      	jne	0x722aa97 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6b7>
 722ace0:      	jmp	0x722aa9c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6bc>
 722ace5:      	nopw	%cs:(%rax,%rax)
 722acef:      	nop
 722acf0:      	leaq	0x88(%rsp), %rcx
 722acf8:      	movq	%rcx, 0x78(%rsp)
 722acfd:      	movq	%rax, 0x80(%rsp)
 722ad05:      	jmp	0x722ad36 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x956>
 722ad07:      	leaq	0x88(%rsp), %rax
 722ad0f:      	movq	%rax, 0x78(%rsp)
 722ad14:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ad1e:      	movq	%rax, 0x80(%rsp)
 722ad26:      	testl	%ebp, %ebp
 722ad28:      	leaq	0x348(%rsp), %rdi
 722ad30:      	je	0x722ae3c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa5c>
 722ad36:      	movl	%ebp, %r15d
 722ad39:      	cmpl	$0x15, %ebp
 722ad3c:      	jb	0x722ac4b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x86b>
 722ad42:      	movl	$0x0, 0x80(%rsp)
 722ad4d:      	movl	$0x8, %ecx
 722ad52:      	leaq	0x78(%rsp), %rdi
 722ad57:      	leaq	0x88(%rsp), %rsi
 722ad5f:      	movq	%r15, %rdx
 722ad62:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722ad67:      	movl	0x130(%rsp), %r15d
 722ad6f:      	testq	%r15, %r15
 722ad72:      	je	0x722ad8d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x9ad>
 722ad74:      	movq	0x78(%rsp), %rdi
 722ad79:      	movq	0x128(%rsp), %rsi
 722ad81:      	shlq	$0x3, %r15
 722ad85:      	movq	%r15, %rdx
 722ad88:      	callq	0x828ac50 <memcpy@plt>
 722ad8d:      	movl	%ebp, 0x80(%rsp)
 722ad94:      	movl	0x1e0(%rsp), %r15d
 722ad9c:      	leaq	0x348(%rsp), %rdi
 722ada4:      	movq	%rdi, 0x338(%rsp)
 722adac:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722adb6:      	movq	%rax, 0x340(%rsp)
 722adbe:      	testl	%r15d, %r15d
 722adc1:      	je	0x722ae02 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa22>
 722adc3:      	movl	%r15d, %eax
 722adc6:      	cmpl	$0x15, %r15d
 722adca:      	jb	0x722ae60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa80>
 722add0:      	movl	%r15d, %edx
 722add3:      	movl	$0x8, %ecx
 722add8:      	leaq	0x338(%rsp), %rdi
 722ade0:      	leaq	0x348(%rsp), %rsi
 722ade8:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722aded:      	movl	0x1e0(%rsp), %eax
 722adf4:      	testl	%eax, %eax
 722adf6:      	je	0x722ae73 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa93>
 722adf8:      	movq	0x338(%rsp), %rdi
 722ae00:      	jmp	0x722ae60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa80>
 722ae02:      	leaq	0x4a8(%rsp), %rdi
 722ae0a:      	movq	%rdi, 0x498(%rsp)
 722ae12:      	movq	%rax, 0x4a0(%rsp)
 722ae1a:      	jmp	0x722aeac <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xacc>
 722ae1f:      	leaq	0x138(%rsp), %rax
 722ae27:      	leaq	0x1e8(%rsp), %rcx
 722ae2f:      	leaq	0x88(%rsp), %rbp
 722ae37:      	jmp	0x722b79e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13be>
 722ae3c:      	movq	%rdi, 0x338(%rsp)
 722ae44:      	movq	%rax, 0x340(%rsp)
 722ae4c:      	movl	%r15d, %eax
 722ae4f:      	cmpl	$0x15, %r15d
 722ae53:      	jae	0x722add0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x9f0>
 722ae59:      	nopl	(%rax)
 722ae60:      	movl	%eax, %edx
 722ae62:      	movq	0x1d8(%rsp), %rsi
 722ae6a:      	shlq	$0x3, %rdx
 722ae6e:      	callq	0x828ac50 <memcpy@plt>
 722ae73:      	movl	%r15d, 0x340(%rsp)
 722ae7b:      	movl	0x80(%rsp), %ebp
 722ae82:      	leaq	0x4a8(%rsp), %rdi
 722ae8a:      	movq	%rdi, 0x498(%rsp)
 722ae92:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ae9c:      	movq	%rax, 0x4a0(%rsp)
 722aea4:      	testl	%ebp, %ebp
 722aea6:      	je	0x722af38 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb58>
 722aeac:      	movl	%ebp, %eax
 722aeae:      	cmpl	$0x15, %ebp
 722aeb1:      	jb	0x722aee2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb02>
 722aeb3:      	movl	%ebp, %edx
 722aeb5:      	movl	$0x8, %ecx
 722aeba:      	leaq	0x498(%rsp), %rdi
 722aec2:      	leaq	0x4a8(%rsp), %rsi
 722aeca:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722aecf:      	movl	0x80(%rsp), %eax
 722aed6:      	testl	%eax, %eax
 722aed8:      	je	0x722aef2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb12>
 722aeda:      	movq	0x498(%rsp), %rdi
 722aee2:      	movl	%eax, %edx
 722aee4:      	movq	0x78(%rsp), %rsi
 722aee9:      	shlq	$0x3, %rdx
 722aeed:      	callq	0x828ac50 <memcpy@plt>
 722aef2:      	movl	%ebp, 0x4a0(%rsp)
 722aef9:      	movl	0x340(%rsp), %r15d
 722af01:      	leaq	0x298(%rsp), %rdi
 722af09:      	movq	%rdi, 0x288(%rsp)
 722af11:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722af1b:      	movq	%rax, 0x290(%rsp)
 722af23:      	testl	%r15d, %r15d
 722af26:      	je	0x722af33 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb53>
 722af28:      	movl	%r15d, %eax
 722af2b:      	cmpl	$0x15, %r15d
 722af2f:      	jae	0x722af59 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb79>
 722af31:      	jmp	0x722af89 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xba9>
 722af33:      	xorl	%r15d, %r15d
 722af36:      	jmp	0x722afab <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbcb>
 722af38:      	leaq	0x298(%rsp), %rdi
 722af40:      	movq	%rdi, 0x288(%rsp)
 722af48:      	movq	%rax, 0x290(%rsp)
 722af50:      	movl	%r15d, %eax
 722af53:      	cmpl	$0x15, %r15d
 722af57:      	jb	0x722af89 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xba9>
 722af59:      	movl	%r15d, %edx
 722af5c:      	movl	$0x8, %ecx
 722af61:      	leaq	0x288(%rsp), %rdi
 722af69:      	leaq	0x298(%rsp), %rsi
 722af71:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722af76:      	movl	0x340(%rsp), %eax
 722af7d:      	testl	%eax, %eax
 722af7f:      	je	0x722af9c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbbc>
 722af81:      	movq	0x288(%rsp), %rdi
 722af89:      	movl	%eax, %edx
 722af8b:      	movq	0x338(%rsp), %rsi
 722af93:      	shlq	$0x3, %rdx
 722af97:      	callq	0x828ac50 <memcpy@plt>
 722af9c:      	movl	%r15d, 0x290(%rsp)
 722afa4:      	movl	0x4a0(%rsp), %ebp
 722afab:      	movq	%r13, %rax
 722afae:      	subq	(%rsp), %rax
 722afb2:      	movq	%rax, 0x8(%rsp)
 722afb7:      	xorl	%ebx, %ebx
 722afb9:      	jmp	0x722afcd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbed>
 722afbb:      	nopl	(%rax,%rax)
 722afc0:      	xorl	%ebp, %ebp
 722afc2:      	incq	%rbx
 722afc5:      	movl	0x290(%rsp), %r15d
 722afcd:      	cmpl	%r15d, %ebp
 722afd0:      	jne	0x722b010 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc30>
 722afd2:      	movq	0x288(%rsp), %r12
 722afda:      	testl	%r15d, %r15d
 722afdd:      	je	0x722b140 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd60>
 722afe3:      	movl	%r15d, %r14d
 722afe6:      	leaq	(,%r14,8), %rdx
 722afee:      	movq	0x498(%rsp), %r15
 722aff6:      	movq	%r15, %rdi
 722aff9:      	movq	%r12, %rsi
 722affc:      	callq	0x828a6c0 <bcmp@plt>
 722b001:      	testl	%eax, %eax
 722b003:      	jne	0x722b01b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc3b>
 722b005:      	jmp	0x722b140 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd60>
 722b00a:      	nopw	(%rax,%rax)
 722b010:      	movq	0x498(%rsp), %r15
 722b018:      	movl	%ebp, %r14d
 722b01b:      	movq	-0x8(%r15,%r14,8), %rax
 722b020:      	jmp	0x722b04e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc6e>
 722b022:      	orq	$0x3, %rax
 722b026:      	movq	%rax, -0x8(%r15,%rdx,8)
 722b02b:      	testl	%ebp, %ebp
 722b02d:      	jne	0x722b0f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd10>
 722b033:      	jmp	0x722afc0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b035:      	nopw	%cs:(%rax,%rax)
 722b03f:      	nop
 722b040:      	movl	%eax, %ecx
 722b042:      	andl	$0x3, %ecx
 722b045:      	cmpl	$0x1, %ecx
 722b048:      	je	0x722afc2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe2>
 722b04e:      	movl	%eax, %ecx
 722b050:      	andl	$0x3, %ecx
 722b053:      	cmpq	$0x3, %rcx
 722b057:      	je	0x722b080 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xca0>
 722b059:      	movl	%ebp, %edx
 722b05b:      	movq	%rax, %rsi
 722b05e:      	andq	$-0x4, %rsi
 722b062:      	cmpl	$0x1, %ecx
 722b065:      	jne	0x722b0b0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcd0>
 722b067:      	movq	0x10(%rsi), %r14
 722b06b:      	testq	%r14, %r14
 722b06e:      	jne	0x722b0b9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcd9>
 722b070:      	jmp	0x722b022 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc42>
 722b072:      	nopw	%cs:(%rax,%rax)
 722b07c:      	nopl	(%rax)
 722b080:      	decl	%ebp
 722b082:      	movl	%ebp, 0x4a0(%rsp)
 722b089:      	je	0x722afc0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b08f:      	movl	%ebp, %ecx
 722b091:      	movq	-0x8(%r15,%rcx,8), %rdx
 722b096:      	xorl	%eax, %eax
 722b098:      	testb	$0x3, %dl
 722b09b:      	setne	%al
 722b09e:      	addl	%eax, %eax
 722b0a0:      	orq	%rdx, %rax
 722b0a3:      	orq	$0x1, %rax
 722b0a7:      	movq	%rax, -0x8(%r15,%rcx,8)
 722b0ac:      	jmp	0x722b040 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc60>
 722b0ae:      	nop
 722b0b0:      	movq	0x8(%rsi), %r14
 722b0b4:      	testq	%r14, %r14
 722b0b7:      	je	0x722b0df <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcff>
 722b0b9:      	cmpl	0x4a4(%rsp), %ebp
 722b0c0:      	jae	0x722b104 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd24>
 722b0c2:      	movq	%r14, (%r15,%rdx,8)
 722b0c6:      	movl	0x4a0(%rsp), %ebp
 722b0cd:      	incl	%ebp
 722b0cf:      	movl	%ebp, 0x4a0(%rsp)
 722b0d6:      	testl	%ebp, %ebp
 722b0d8:      	jne	0x722b0f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd10>
 722b0da:      	jmp	0x722afc0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b0df:      	orq	$0x1, %rax
 722b0e3:      	movq	%rax, -0x8(%r15,%rdx,8)
 722b0e8:      	testl	%ebp, %ebp
 722b0ea:      	je	0x722afc0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b0f0:      	movq	0x498(%rsp), %r15
 722b0f8:      	movl	%ebp, %eax
 722b0fa:      	movq	-0x8(%r15,%rax,8), %rax
 722b0ff:      	jmp	0x722b040 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc60>
 722b104:      	incq	%rdx
 722b107:      	movl	$0x8, %ecx
 722b10c:      	leaq	0x498(%rsp), %rdi
 722b114:      	leaq	0x4a8(%rsp), %rsi
 722b11c:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b121:      	movl	0x4a0(%rsp), %edx
 722b128:      	movq	0x498(%rsp), %r15
 722b130:      	jmp	0x722b0c2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xce2>
 722b132:      	nopw	%cs:(%rax,%rax)
 722b13c:      	nopl	(%rax)
 722b140:      	leaq	0x298(%rsp), %rax
 722b148:      	cmpq	%rax, %r12
 722b14b:      	je	0x722b155 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd75>
 722b14d:      	movq	%r12, %rdi
 722b150:      	callq	0x828a640 <free@plt>
 722b155:      	movq	0x498(%rsp), %rdi
 722b15d:      	leaq	0x4a8(%rsp), %rax
 722b165:      	cmpq	%rax, %rdi
 722b168:      	leaq	0x88(%rsp), %rbp
 722b170:      	je	0x722b177 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd97>
 722b172:      	callq	0x828a640 <free@plt>
 722b177:      	movq	0x338(%rsp), %rdi
 722b17f:      	leaq	0x348(%rsp), %rax
 722b187:      	cmpq	%rax, %rdi
 722b18a:      	je	0x722b191 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xdb1>
 722b18c:      	callq	0x828a640 <free@plt>
 722b191:      	movq	0x78(%rsp), %rdi
 722b196:      	cmpq	%rbp, %rdi
 722b199:      	je	0x722b1a0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xdc0>
 722b19b:      	callq	0x828a640 <free@plt>
 722b1a0:      	movq	0x20(%rsp), %rax
 722b1a5:      	subq	%r13, %rax
 722b1a8:      	sarq	$0x3, %rax
 722b1ac:      	cmpq	%rbx, %rax
 722b1af:      	jae	0x722b3b0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfd0>
 722b1b5:      	movq	0x8(%rsp), %r13
 722b1ba:      	movq	%r13, %rax
 722b1bd:      	sarq	$0x3, %rax
 722b1c1:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 722b1cb:      	movq	%rdx, %rcx
 722b1ce:      	subq	%rax, %rcx
 722b1d1:      	cmpq	%rbx, %rcx
 722b1d4:      	jb	0x722c044 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c64>
 722b1da:      	cmpq	%rbx, %rax
 722b1dd:      	cmovaq	%rax, %rbx
 722b1e1:      	leaq	(%rbx,%rax), %r12
 722b1e5:      	cmpq	%rdx, %r12
 722b1e8:      	cmovaeq	%rdx, %r12
 722b1ec:      	addq	%rax, %rbx
 722b1ef:      	cmovbq	%rdx, %r12
 722b1f3:      	testq	%r12, %r12
 722b1f6:      	je	0x722b4b1 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10d1>
 722b1fc:      	leaq	(,%r12,8), %rdi
 722b204:      	callq	0x828a620 <_Znwm@plt>
 722b209:      	movq	%rax, %r15
 722b20c:      	cmpq	$0x9, %r13
 722b210:      	jl	0x722b4be <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10de>
 722b216:      	movq	%r15, %rdi
 722b219:      	movq	(%rsp), %rsi
 722b21d:      	movq	%r13, %rdx
 722b220:      	callq	0x828abc0 <memmove@plt>
 722b225:      	leaq	0x8d8(%rsp), %rax
 722b22d:      	movq	%rax, 0x8c8(%rsp)
 722b235:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b23f:      	movq	%rax, 0x8d0(%rsp)
 722b247:      	movl	0x130(%rsp), %ebx
 722b24e:      	testq	%rbx, %rbx
 722b251:      	je	0x722b2b6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xed6>
 722b253:      	leaq	0x8d8(%rsp), %rdi
 722b25b:      	movl	%ebx, %eax
 722b25d:      	cmpl	$0x15, %ebx
 722b260:      	jb	0x722b292 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xeb2>
 722b262:      	movl	$0x8, %ecx
 722b267:      	leaq	0x8c8(%rsp), %rdi
 722b26f:      	leaq	0x8d8(%rsp), %rsi
 722b277:      	movq	%rbx, %rdx
 722b27a:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b27f:      	movl	0x130(%rsp), %eax
 722b286:      	testl	%eax, %eax
 722b288:      	je	0x722b2a5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xec5>
 722b28a:      	movq	0x8c8(%rsp), %rdi
 722b292:      	movl	%eax, %edx
 722b294:      	movq	0x128(%rsp), %rsi
 722b29c:      	shlq	$0x3, %rdx
 722b2a0:      	callq	0x828ac50 <memcpy@plt>
 722b2a5:      	movl	%ebx, 0x8d0(%rsp)
 722b2ac:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b2b6:      	leaq	0xa38(%rsp), %r14
 722b2be:      	movq	%r14, 0xa28(%rsp)
 722b2c6:      	movq	%rax, 0xa30(%rsp)
 722b2ce:      	movl	0x1e0(%rsp), %ebx
 722b2d5:      	testq	%rbx, %rbx
 722b2d8:      	je	0x722b336 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf56>
 722b2da:      	movq	%r14, %rdi
 722b2dd:      	movl	%ebx, %eax
 722b2df:      	cmpl	$0x15, %ebx
 722b2e2:      	jb	0x722b314 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf34>
 722b2e4:      	movl	$0x8, %ecx
 722b2e9:      	leaq	0xa28(%rsp), %rdi
 722b2f1:      	leaq	0xa38(%rsp), %rsi
 722b2f9:      	movq	%rbx, %rdx
 722b2fc:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b301:      	movl	0x1e0(%rsp), %eax
 722b308:      	testl	%eax, %eax
 722b30a:      	je	0x722b327 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf47>
 722b30c:      	movq	0xa28(%rsp), %rdi
 722b314:      	movl	%eax, %edx
 722b316:      	movq	0x1d8(%rsp), %rsi
 722b31e:      	shlq	$0x3, %rdx
 722b322:      	callq	0x828ac50 <memcpy@plt>
 722b327:      	movl	%ebx, 0xa30(%rsp)
 722b32e:      	leaq	0xa38(%rsp), %r14
 722b336:      	addq	%r15, %r13
 722b339:      	leaq	0x8c8(%rsp), %rdi
 722b341:      	leaq	0xa28(%rsp), %rsi
 722b349:      	movq	%r13, %rdx
 722b34c:      	callq	0x7232500 <_ZSt22__uninitialized_copy_aIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEPS6_S6_ET0_T_SD_SC_RSaIT1_E>
 722b351:      	movq	%rax, %r13
 722b354:      	movq	0xa28(%rsp), %rdi
 722b35c:      	cmpq	%r14, %rdi
 722b35f:      	je	0x722b366 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf86>
 722b361:      	callq	0x828a640 <free@plt>
 722b366:      	movq	0x8c8(%rsp), %rdi
 722b36e:      	leaq	0x8d8(%rsp), %rax
 722b376:      	cmpq	%rax, %rdi
 722b379:      	je	0x722b380 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfa0>
 722b37b:      	callq	0x828a640 <free@plt>
 722b380:      	movq	(%rsp), %rdi
 722b384:      	testq	%rdi, %rdi
 722b387:      	je	0x722b396 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfb6>
 722b389:      	movq	0x20(%rsp), %rsi
 722b38e:      	subq	%rdi, %rsi
 722b391:      	callq	0x828a660 <_ZdlPvm@plt>
 722b396:      	leaq	(%r15,%r12,8), %rax
 722b39a:      	movq	%rax, 0x20(%rsp)
 722b39f:      	movq	%r15, (%rsp)
 722b3a3:      	jmp	0x722b78e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13ae>
 722b3a8:      	nopl	(%rax,%rax)
 722b3b0:      	leaq	0x4a8(%rsp), %rax
 722b3b8:      	movq	%rax, 0x498(%rsp)
 722b3c0:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b3ca:      	movq	%rax, 0x4a0(%rsp)
 722b3d2:      	movl	0x130(%rsp), %r15d
 722b3da:      	testq	%r15, %r15
 722b3dd:      	je	0x722b48a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10aa>
 722b3e3:      	cmpl	$0x15, %r15d
 722b3e7:      	jb	0x722b4d7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10f7>
 722b3ed:      	movl	$0x8, %ecx
 722b3f2:      	leaq	0x498(%rsp), %rdi
 722b3fa:      	leaq	0x4a8(%rsp), %rsi
 722b402:      	movq	%r15, %rdx
 722b405:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b40a:      	movl	0x130(%rsp), %edx
 722b411:      	testq	%rdx, %rdx
 722b414:      	je	0x722b42f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x104f>
 722b416:      	movq	0x498(%rsp), %rdi
 722b41e:      	movq	0x128(%rsp), %rsi
 722b426:      	shlq	$0x3, %rdx
 722b42a:      	callq	0x828ac50 <memcpy@plt>
 722b42f:      	movl	%r15d, 0x4a0(%rsp)
 722b437:      	leaq	0x3f8(%rsp), %rsi
 722b43f:      	movq	%rsi, 0x3e8(%rsp)
 722b447:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b451:      	movq	%rax, 0x3f0(%rsp)
 722b459:      	movl	$0x8, %ecx
 722b45e:      	leaq	0x3e8(%rsp), %rdi
 722b466:      	movq	%r15, %rdx
 722b469:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b46e:      	movl	0x4a0(%rsp), %eax
 722b475:      	testl	%eax, %eax
 722b477:      	je	0x722b538 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1158>
 722b47d:      	movq	0x3e8(%rsp), %rdi
 722b485:      	jmp	0x722b525 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1145>
 722b48a:      	leaq	0x3f8(%rsp), %rax
 722b492:      	movq	%rax, 0x3e8(%rsp)
 722b49a:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b4a4:      	movq	%rax, 0x3f0(%rsp)
 722b4ac:      	jmp	0x722b54a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x116a>
 722b4b1:      	xorl	%r15d, %r15d
 722b4b4:      	cmpq	$0x9, %r13
 722b4b8:      	jge	0x722b216 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe36>
 722b4be:      	cmpq	$0x8, %r13
 722b4c2:      	jne	0x722b225 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe45>
 722b4c8:      	movq	(%rsp), %rax
 722b4cc:      	movq	(%rax), %rax
 722b4cf:      	movq	%rax, (%r15)
 722b4d2:      	jmp	0x722b225 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe45>
 722b4d7:      	movq	0x128(%rsp), %rsi
 722b4df:      	movq	%r15, %rdx
 722b4e2:      	shlq	$0x3, %rdx
 722b4e6:      	movl	$0xa0, %ecx
 722b4eb:      	leaq	0x4a8(%rsp), %rdi
 722b4f3:      	callq	0x828a6a0 <__memcpy_chk@plt>
 722b4f8:      	movl	%r15d, 0x4a0(%rsp)
 722b500:      	leaq	0x3f8(%rsp), %rdi
 722b508:      	movq	%rdi, 0x3e8(%rsp)
 722b510:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b51a:      	movq	%rax, 0x3f0(%rsp)
 722b522:      	movl	%r15d, %eax
 722b525:      	movl	%eax, %edx
 722b527:      	movq	0x498(%rsp), %rsi
 722b52f:      	shlq	$0x3, %rdx
 722b533:      	callq	0x828ac50 <memcpy@plt>
 722b538:      	movl	%r15d, 0x3f0(%rsp)
 722b540:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b54a:      	leaq	0xb98(%rsp), %r14
 722b552:      	movq	%r14, 0xb88(%rsp)
 722b55a:      	movq	%rax, 0xb90(%rsp)
 722b562:      	movl	0x1e0(%rsp), %r15d
 722b56a:      	testq	%r15, %r15
 722b56d:      	je	0x722b5ce <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11ee>
 722b56f:      	movq	%r14, %rdi
 722b572:      	movl	%r15d, %eax
 722b575:      	cmpl	$0x15, %r15d
 722b579:      	jb	0x722b5ab <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11cb>
 722b57b:      	movl	$0x8, %ecx
 722b580:      	leaq	0xb88(%rsp), %rdi
 722b588:      	leaq	0xb98(%rsp), %rsi
 722b590:      	movq	%r15, %rdx
 722b593:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b598:      	movl	0x1e0(%rsp), %eax
 722b59f:      	testl	%eax, %eax
 722b5a1:      	je	0x722b5be <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11de>
 722b5a3:      	movq	0xb88(%rsp), %rdi
 722b5ab:      	movl	%eax, %edx
 722b5ad:      	movq	0x1d8(%rsp), %rsi
 722b5b5:      	shlq	$0x3, %rdx
 722b5b9:      	callq	0x828ac50 <memcpy@plt>
 722b5be:      	movl	%r15d, 0xb90(%rsp)
 722b5c6:      	leaq	0xb98(%rsp), %r14
 722b5ce:      	leaq	0x3e8(%rsp), %rdi
 722b5d6:      	leaq	0xb88(%rsp), %rsi
 722b5de:      	movq	%r13, %rdx
 722b5e1:      	callq	0x7232500 <_ZSt22__uninitialized_copy_aIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEPS6_S6_ET0_T_SD_SC_RSaIT1_E>
 722b5e6:      	movq	0xb88(%rsp), %rdi
 722b5ee:      	cmpq	%r14, %rdi
 722b5f1:      	je	0x722b5f8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1218>
 722b5f3:      	callq	0x828a640 <free@plt>
 722b5f8:      	movq	0x3e8(%rsp), %rdi
 722b600:      	leaq	0x3f8(%rsp), %rax
 722b608:      	cmpq	%rax, %rdi
 722b60b:      	je	0x722b612 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1232>
 722b60d:      	callq	0x828a640 <free@plt>
 722b612:      	leaq	0x988(%rsp), %rax
 722b61a:      	movq	%rax, 0x978(%rsp)
 722b622:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b62c:      	movq	%rax, 0x980(%rsp)
 722b634:      	movl	0x130(%rsp), %r15d
 722b63c:      	testq	%r15, %r15
 722b63f:      	je	0x722b6a7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12c7>
 722b641:      	leaq	0x988(%rsp), %rdi
 722b649:      	movl	%r15d, %eax
 722b64c:      	cmpl	$0x15, %r15d
 722b650:      	jb	0x722b682 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12a2>
 722b652:      	movl	$0x8, %ecx
 722b657:      	leaq	0x978(%rsp), %rdi
 722b65f:      	leaq	0x988(%rsp), %rsi
 722b667:      	movq	%r15, %rdx
 722b66a:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b66f:      	movl	0x130(%rsp), %eax
 722b676:      	testl	%eax, %eax
 722b678:      	je	0x722b695 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12b5>
 722b67a:      	movq	0x978(%rsp), %rdi
 722b682:      	movl	%eax, %edx
 722b684:      	movq	0x128(%rsp), %rsi
 722b68c:      	shlq	$0x3, %rdx
 722b690:      	callq	0x828ac50 <memcpy@plt>
 722b695:      	movl	%r15d, 0x980(%rsp)
 722b69d:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b6a7:      	leaq	0xae8(%rsp), %r14
 722b6af:      	movq	%r14, 0xad8(%rsp)
 722b6b7:      	movq	%rax, 0xae0(%rsp)
 722b6bf:      	movl	0x4a0(%rsp), %r15d
 722b6c7:      	testq	%r15, %r15
 722b6ca:      	je	0x722b72b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x134b>
 722b6cc:      	movq	%r14, %rdi
 722b6cf:      	movl	%r15d, %eax
 722b6d2:      	cmpl	$0x15, %r15d
 722b6d6:      	jb	0x722b708 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1328>
 722b6d8:      	movl	$0x8, %ecx
 722b6dd:      	leaq	0xad8(%rsp), %rdi
 722b6e5:      	leaq	0xae8(%rsp), %rsi
 722b6ed:      	movq	%r15, %rdx
 722b6f0:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b6f5:      	movl	0x4a0(%rsp), %eax
 722b6fc:      	testl	%eax, %eax
 722b6fe:      	je	0x722b71b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x133b>
 722b700:      	movq	0xad8(%rsp), %rdi
 722b708:      	movl	%eax, %edx
 722b70a:      	movq	0x498(%rsp), %rsi
 722b712:      	shlq	$0x3, %rdx
 722b716:      	callq	0x828ac50 <memcpy@plt>
 722b71b:      	movl	%r15d, 0xae0(%rsp)
 722b723:      	leaq	0xae8(%rsp), %r14
 722b72b:      	leaq	0x978(%rsp), %rdi
 722b733:      	leaq	0xad8(%rsp), %rsi
 722b73b:      	movq	%r13, %rdx
 722b73e:      	callq	0x72321b0 <_ZSt4copyIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEN9__gnu_cxx17__normal_iteratorIPS6_St6vectorIS6_SaIS6_EEEEET0_T_SJ_SI_>
 722b743:      	movq	0xad8(%rsp), %rdi
 722b74b:      	cmpq	%r14, %rdi
 722b74e:      	je	0x722b755 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1375>
 722b750:      	callq	0x828a640 <free@plt>
 722b755:      	movq	0x978(%rsp), %rdi
 722b75d:      	leaq	0x988(%rsp), %rax
 722b765:      	cmpq	%rax, %rdi
 722b768:      	je	0x722b76f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x138f>
 722b76a:      	callq	0x828a640 <free@plt>
 722b76f:      	movq	0x498(%rsp), %rdi
 722b777:      	leaq	0x4a8(%rsp), %rax
 722b77f:      	cmpq	%rax, %rdi
 722b782:      	je	0x722b789 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13a9>
 722b784:      	callq	0x828a640 <free@plt>
 722b789:      	leaq	(%r13,%rbx,8), %r13
 722b78e:      	leaq	0x138(%rsp), %rax
 722b796:      	leaq	0x1e8(%rsp), %rcx
 722b79e:      	movq	0x1d8(%rsp), %rdi
 722b7a6:      	cmpq	%rcx, %rdi
 722b7a9:      	je	0x722b7b8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13d8>
 722b7ab:      	callq	0x828a640 <free@plt>
 722b7b0:      	leaq	0x138(%rsp), %rax
 722b7b8:      	movq	0x128(%rsp), %rdi
 722b7c0:      	cmpq	%rax, %rdi
 722b7c3:      	je	0x722b7ca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13ea>
 722b7c5:      	callq	0x828a640 <free@plt>
 722b7ca:      	movq	0xc38(%rsp), %rdi
 722b7d2:      	leaq	0xc48(%rsp), %rax
 722b7da:      	cmpq	%rax, %rdi
 722b7dd:      	je	0x722b7e4 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1404>
 722b7df:      	callq	0x828a640 <free@plt>
 722b7e4:      	movq	0x818(%rsp), %rdi
 722b7ec:      	leaq	0x828(%rsp), %rax
 722b7f4:      	cmpq	%rax, %rdi
 722b7f7:      	je	0x722b7fe <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x141e>
 722b7f9:      	callq	0x828a640 <free@plt>
 722b7fe:      	cmpq	%r13, (%rsp)
 722b802:      	je	0x722a840 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722b808:      	movq	%r13, %rbx
 722b80b:      	movq	(%rsp), %r14
 722b80f:      	subq	%r14, %rbx
 722b812:      	movq	%rbx, %rax
 722b815:      	sarq	$0x3, %rax
 722b819:      	bsrq	%rax, %rdx
 722b81d:      	xorl	$0x3f, %edx
 722b820:      	addl	%edx, %edx
 722b822:      	xorq	$0x7e, %rdx
 722b826:      	movq	%r14, %rdi
 722b829:      	movq	%r13, %rsi
 722b82c:      	callq	0x7232eb0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN5clang7VarDeclESt6vectorIS5_SaIS5_EEEElNS0_5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117LiveVariablesImpl17dumpBlockLivenessERKNS2_13SourceManagerEE3$_1EEEvT_SK_T0_T1_>
 722b831:      	leaq	0x8(%r14), %rcx
 722b835:      	cmpq	$0x81, %rbx
 722b83c:      	movq	%r13, 0x18(%rsp)
 722b841:      	jl	0x722b860 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1480>
 722b843:      	movl	$0x8, %ebp
 722b848:      	movq	%rcx, 0x58(%rsp)
 722b84d:      	movq	%rcx, 0x48(%rsp)
 722b852:      	movq	%r14, %rax
 722b855:      	movq	%r14, %rbx
 722b858:      	jmp	0x722b9b3 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15d3>
 722b85d:      	nopl	(%rax)
 722b860:      	movq	%r14, %rbx
 722b863:      	cmpq	%r13, %rcx
 722b866:      	je	0x722bb1a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722b86c:      	movq	(%rsp), %r12
 722b870:      	jmp	0x722b8d1 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14f1>
 722b872:      	nopw	%cs:(%rax,%rax)
 722b87c:      	nopl	(%rax)
 722b880:      	subq	%r13, %rbx
 722b883:      	movq	%rbx, %rax
 722b886:      	sarq	$0x3, %rax
 722b88a:      	cmpq	$0x2, %rax
 722b88e:      	jl	0x722b959 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1579>
 722b894:      	shlq	$0x3, %rax
 722b898:      	subq	%rax, %r12
 722b89b:      	addq	$0x10, %r12
 722b89f:      	movq	%r12, %rdi
 722b8a2:      	movq	%r13, %rsi
 722b8a5:      	movq	%rbx, %rdx
 722b8a8:      	callq	0x828abc0 <memmove@plt>
 722b8ad:      	movq	0x18(%rsp), %rbp
 722b8b2:      	movq	%r15, (%r13)
 722b8b6:      	movq	0x8(%rsp), %r12
 722b8bb:      	leaq	0x8(%r12), %rcx
 722b8c0:      	cmpq	%rbp, %rcx
 722b8c3:      	leaq	0x88(%rsp), %rbp
 722b8cb:      	je	0x722baf0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1710>
 722b8d1:      	movq	%rcx, %rbx
 722b8d4:      	movq	(%rcx), %r15
 722b8d7:      	movq	(%rsp), %r13
 722b8db:      	movq	(%r13), %rbp
 722b8df:      	movq	(%r15), %r14
 722b8e2:      	movq	%r15, %rdi
 722b8e5:      	callq	*0x10(%r14)
 722b8e9:      	movq	(%rbp), %rcx
 722b8ed:      	movq	%rbp, 0x30(%rsp)
 722b8f2:      	movq	%rbp, %rdi
 722b8f5:      	movq	%rax, %rbp
 722b8f8:      	callq	*0x10(%rcx)
 722b8fb:      	cmpl	%eax, %ebp
 722b8fd:      	movq	%rbx, 0x8(%rsp)
 722b902:      	jb	0x722b880 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14a0>
 722b908:      	movq	(%r12), %r12
 722b90c:      	movq	(%r12), %rax
 722b910:      	movq	%r12, %rdi
 722b913:      	callq	*0x10(%rax)
 722b916:      	movq	%rbx, %r13
 722b919:      	cmpl	%eax, %ebp
 722b91b:      	movq	0x18(%rsp), %rbp
 722b920:      	jae	0x722b8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722b922:      	movq	0x8(%rsp), %r13
 722b927:      	nopw	(%rax,%rax)
 722b930:      	movq	%r12, (%r13)
 722b934:      	movq	-0x10(%r13), %r12
 722b938:      	movq	%r15, %rdi
 722b93b:      	callq	*0x10(%r14)
 722b93f:      	movq	%rax, %rbx
 722b942:      	movq	(%r12), %rax
 722b946:      	movq	%r12, %rdi
 722b949:      	callq	*0x10(%rax)
 722b94c:      	addq	$-0x8, %r13
 722b950:      	cmpl	%eax, %ebx
 722b952:      	jb	0x722b930 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1550>
 722b954:      	jmp	0x722b8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722b959:      	cmpq	$0x8, %rbx
 722b95d:      	movq	0x18(%rsp), %rbp
 722b962:      	jne	0x722b8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722b968:      	movq	0x30(%rsp), %rax
 722b96d:      	movq	%rax, 0x8(%r12)
 722b972:      	movq	(%rsp), %r13
 722b976:      	jmp	0x722b8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722b97b:      	movq	%r13, 0x8(%rax)
 722b97f:      	movq	(%rsp), %r14
 722b983:      	nopw	%cs:(%rax,%rax)
 722b98d:      	nopl	(%rax)
 722b990:      	movq	%r12, (%r14)
 722b993:      	addq	$0x8, %rbp
 722b997:      	addq	$0x8, 0x48(%rsp)
 722b99d:      	cmpq	$0x80, %rbp
 722b9a4:      	movq	(%rsp), %rbx
 722b9a8:      	movq	0x8(%rsp), %rax
 722b9ad:      	je	0x722ba60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1680>
 722b9b3:      	movq	%rax, 0x30(%rsp)
 722b9b8:      	leaq	(%rbx,%rbp), %r14
 722b9bc:      	movq	(%rbx,%rbp), %r12
 722b9c0:      	movq	(%rbx), %r13
 722b9c3:      	movq	(%r12), %r15
 722b9c7:      	movq	%r12, %rdi
 722b9ca:      	callq	*0x10(%r15)
 722b9ce:      	movq	%rax, %rbx
 722b9d1:      	movq	(%r13), %rax
 722b9d5:      	movq	%r13, %rdi
 722b9d8:      	callq	*0x10(%rax)
 722b9db:      	cmpl	%eax, %ebx
 722b9dd:      	movq	%r14, 0x8(%rsp)
 722b9e2:      	jae	0x722ba10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1630>
 722b9e4:      	movq	0x30(%rsp), %rax
 722b9e9:      	cmpq	$0x9, %rbp
 722b9ed:      	jb	0x722b97b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x159b>
 722b9ef:      	movq	0x58(%rsp), %rdi
 722b9f4:      	movq	(%rsp), %r14
 722b9f8:      	movq	%r14, %rsi
 722b9fb:      	movq	%rbp, %rdx
 722b9fe:      	callq	0x828abc0 <memmove@plt>
 722ba03:      	jmp	0x722b990 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722ba05:      	nopw	%cs:(%rax,%rax)
 722ba0f:      	nop
 722ba10:      	movq	0x30(%rsp), %rax
 722ba15:      	movq	(%rax), %r13
 722ba18:      	movq	(%r13), %rax
 722ba1c:      	movq	%r13, %rdi
 722ba1f:      	callq	*0x10(%rax)
 722ba22:      	cmpl	%eax, %ebx
 722ba24:      	jae	0x722b990 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722ba2a:      	movq	0x48(%rsp), %r14
 722ba2f:      	nop
 722ba30:      	movq	%r13, (%r14)
 722ba33:      	movq	-0x10(%r14), %r13
 722ba37:      	movq	%r12, %rdi
 722ba3a:      	callq	*0x10(%r15)
 722ba3e:      	movq	%rax, %rbx
 722ba41:      	movq	(%r13), %rax
 722ba45:      	movq	%r13, %rdi
 722ba48:      	callq	*0x10(%rax)
 722ba4b:      	addq	$-0x8, %r14
 722ba4f:      	cmpl	%eax, %ebx
 722ba51:      	jb	0x722ba30 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1650>
 722ba53:      	jmp	0x722b990 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722ba58:      	nopl	(%rax,%rax)
 722ba60:      	leaq	0x80(%rbx), %r14
 722ba67:      	cmpq	0x18(%rsp), %r14
 722ba6c:      	leaq	0x88(%rsp), %rbp
 722ba74:      	jne	0x722ba97 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16b7>
 722ba76:      	jmp	0x722bb1a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722ba7b:      	nopl	(%rax,%rax)
 722ba80:      	movq	%r15, (%rbp)
 722ba84:      	addq	$0x8, %r14
 722ba88:      	cmpq	0x18(%rsp), %r14
 722ba8d:      	leaq	0x88(%rsp), %rbp
 722ba95:      	je	0x722baf0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1710>
 722ba97:      	movq	-0x8(%r14), %r12
 722ba9b:      	movq	(%r14), %r15
 722ba9e:      	movq	(%r15), %r13
 722baa1:      	movq	%r15, %rdi
 722baa4:      	callq	*0x10(%r13)
 722baa8:      	movq	%rax, %rbx
 722baab:      	movq	(%r12), %rax
 722baaf:      	movq	%r12, %rdi
 722bab2:      	callq	*0x10(%rax)
 722bab5:      	movq	%r14, %rbp
 722bab8:      	cmpl	%eax, %ebx
 722baba:      	jae	0x722ba80 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16a0>
 722babc:      	movq	%r14, %rbp
 722babf:      	nop
 722bac0:      	movq	%r12, (%rbp)
 722bac4:      	movq	-0x10(%rbp), %r12
 722bac8:      	movq	%r15, %rdi
 722bacb:      	callq	*0x10(%r13)
 722bacf:      	movq	%rax, %rbx
 722bad2:      	movq	(%r12), %rax
 722bad6:      	movq	%r12, %rdi
 722bad9:      	callq	*0x10(%rax)
 722badc:      	addq	$-0x8, %rbp
 722bae0:      	cmpl	%eax, %ebx
 722bae2:      	jb	0x722bac0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16e0>
 722bae4:      	jmp	0x722ba80 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16a0>
 722bae6:      	nopw	%cs:(%rax,%rax)
 722baf0:      	movq	(%rsp), %rbx
 722baf4:      	jmp	0x722bb1a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722baf6:      	nopw	%cs:(%rax,%rax)
 722bb00:      	movw	$0xa3e, (%rax)          # imm = 0xA3E
 722bb05:      	addq	$0x2, 0x139770b(%rip)   # 0x85c3218 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x20>
 722bb0d:      	addq	$0x8, %rbx
 722bb11:      	cmpq	%r13, %rbx
 722bb14:      	je	0x722a840 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722bb1a:      	movq	(%rbx), %r12
 722bb1d:      	movzbl	0x13976cc(%rip), %eax   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bb24:      	testb	%al, %al
 722bb26:      	je	0x722be6b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a8b>
 722bb2c:      	movzbl	0x1397725(%rip), %eax   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bb33:      	testb	%al, %al
 722bb35:      	je	0x722be90 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1ab0>
 722bb3b:      	movq	0x13976d6(%rip), %rax   # 0x85c3218 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x20>
 722bb42:      	cmpq	%rax, 0x13976c7(%rip)   # 0x85c3210 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x18>
 722bb49:      	je	0x722bb60 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1780>
 722bb4b:      	movb	$0x20, (%rax)
 722bb4e:      	incq	0x13976c3(%rip)         # 0x85c3218 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x20>
 722bb55:      	leaq	0x139769c(%rip), %r15   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bb5c:      	jmp	0x722bb7b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x179b>
 722bb5e:      	nop
 722bb60:      	movl	$0x1, %edx
 722bb65:      	leaq	0x139768c(%rip), %rdi   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bb6c:      	leaq	-0x65d76a6(%rip), %rsi  # 0xc544cd <.str.llvm.4650414281798228289>
 722bb73:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722bb78:      	movq	%rax, %r15
 722bb7b:      	movq	%r12, 0x8(%rsp)
 722bb80:      	movq	0x28(%r12), %rax
 722bb85:      	movq	%rbp, 0x78(%rsp)
 722bb8a:      	movq	$0x0, 0x80(%rsp)
 722bb96:      	movb	$0x0, 0x88(%rsp)
 722bb9e:      	movl	$0x0, 0x290(%rsp)
 722bba9:      	movb	$0x0, 0x2b0(%rsp)
 722bbb1:      	movq	0x68(%rsp), %rcx
 722bbb6:      	movq	%rcx, 0x288(%rsp)
 722bbbe:      	leaq	0x78(%rsp), %rcx
 722bbc3:      	movq	%rcx, 0x2b8(%rsp)
 722bbcb:      	movl	$0x0, 0x2b4(%rsp)
 722bbd6:      	leaq	0x298(%rsp), %rcx
 722bbde:      	xorps	%xmm0, %xmm0
 722bbe1:      	movups	%xmm0, (%rcx)
 722bbe4:      	movq	$0x0, 0x10(%rcx)
 722bbec:      	movq	%rax, 0x3e8(%rsp)
 722bbf4:      	leaq	0x498(%rsp), %r13
 722bbfc:      	movq	%r13, %rdi
 722bbff:      	callq	0x4608470 <_ZN5clang11LangOptionsC2Ev>
 722bc04:      	movq	0x498(%rsp), %rsi
 722bc0c:      	movl	%esi, %edx
 722bc0e:      	shrl	$0x2, %edx
 722bc11:      	andl	$0x200, %edx            # imm = 0x200
 722bc17:      	movl	%esi, %eax
 722bc19:      	shrl	$0x3, %eax
 722bc1c:      	andl	$0x800000, %eax         # imm = 0x800000
 722bc21:      	movl	%esi, %ecx
 722bc23:      	andl	$0x8, %ecx
 722bc26:      	shll	$0x15, %ecx
 722bc29:      	testl	$0x1000, %esi           # imm = 0x1000
 722bc2f:      	movl	$0x1000000, %edi        # imm = 0x1000000
 722bc34:      	cmovneq	%rdi, %rcx
 722bc38:      	movl	%esi, %r8d
 722bc3b:      	shll	$0xe, %r8d
 722bc3f:      	andl	$0x2000000, %r8d        # imm = 0x2000000
 722bc46:      	movl	%esi, %r9d
 722bc49:      	andl	$0x1, %r9d
 722bc4d:      	shll	$0x1a, %r9d
 722bc51:      	movl	%esi, %r10d
 722bc54:      	shll	$0xf, %r10d
 722bc58:      	andl	$0x8000000, %r10d       # imm = 0x8000000
 722bc5f:      	movl	%esi, %r11d
 722bc62:      	andl	$0x2, %r11d
 722bc66:      	shll	$0x1b, %r11d
 722bc6a:      	movl	%esi, %ebp
 722bc6c:      	shll	$0x12, %ebp
 722bc6f:      	andl	$0x60000000, %ebp       # imm = 0x60000000
 722bc75:      	movq	%rsi, %rdi
 722bc78:      	shlq	$0x6, %rdi
 722bc7c:      	movq	%rdi, %r14
 722bc7f:      	movabsq	$0x200000000, %r12      # imm = 0x200000000
 722bc89:      	andq	%r12, %r14
 722bc8c:      	movabsq	$0x400000000, %r12      # imm = 0x400000000
 722bc96:      	andq	%r12, %rdi
 722bc99:      	movabsq	$0x660c00000000, %r12   # imm = 0x660C00000000
 722bca3:      	xorq	%r12, %rdi
 722bca6:      	testb	%sil, %sil
 722bca9:      	movabsq	$0x660800000000, %rsi   # imm = 0x660800000000
 722bcb3:      	cmovnsq	%rsi, %rdi
 722bcb7:      	orl	%edx, %eax
 722bcb9:      	orl	%r8d, %eax
 722bcbc:      	orl	%r9d, %eax
 722bcbf:      	orl	%r10d, %eax
 722bcc2:      	orl	%r11d, %eax
 722bcc5:      	orl	%ebp, %eax
 722bcc7:      	orq	%r14, %rax
 722bcca:      	orq	%rcx, %rax
 722bccd:      	movq	0x4f0(%rsp), %rcx
 722bcd5:      	andl	$0x100, %ecx            # imm = 0x100
 722bcdb:      	shlq	$0x27, %rcx
 722bcdf:      	orq	%rcx, %rax
 722bce2:      	orq	%rdi, %rax
 722bce5:      	xorq	$0x60444002, %rax       # imm = 0x60444002
 722bceb:      	movq	%rax, 0x338(%rsp)
 722bcf3:      	movq	$0x0, 0x340(%rsp)
 722bcff:      	leaq	0x3e8(%rsp), %rdi
 722bd07:      	leaq	0x288(%rsp), %rsi
 722bd0f:      	leaq	0x338(%rsp), %rdx
 722bd17:      	callq	0x75554e0 <_ZNK5clang15DeclarationName5printERN4llvm11raw_ostreamERKNS_14PrintingPolicyE>
 722bd1c:      	movq	%r13, %rdi
 722bd1f:      	callq	0x4374790 <_ZN5clang11LangOptionsD2Ev>
 722bd24:      	movq	0x60(%rsp), %rax
 722bd29:      	movq	%rax, 0x288(%rsp)
 722bd31:      	cmpl	$0x1, 0x2b4(%rsp)
 722bd39:      	jne	0x722bd4d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x196d>
 722bd3b:      	movq	0x298(%rsp), %rdi
 722bd43:      	testq	%rdi, %rdi
 722bd46:      	je	0x722bd4d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x196d>
 722bd48:      	callq	0x828a7b0 <_ZdaPv@plt>
 722bd4d:      	movq	0x78(%rsp), %rsi
 722bd52:      	movq	0x80(%rsp), %rdx
 722bd5a:      	movq	%r15, %rdi
 722bd5d:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722bd62:      	movq	0x18(%rax), %rdx
 722bd66:      	movq	0x20(%rax), %rcx
 722bd6a:      	subq	%rcx, %rdx
 722bd6d:      	cmpq	$0x1, %rdx
 722bd71:      	ja	0x722bd90 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19b0>
 722bd73:      	movl	$0x2, %edx
 722bd78:      	movq	%rax, %rdi
 722bd7b:      	leaq	-0x6526b77(%rip), %rsi  # 0xd0520b <.str.564.llvm.14833847722900535170>
 722bd82:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722bd87:      	jmp	0x722bd9a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19ba>
 722bd89:      	nopl	(%rax)
 722bd90:      	movw	$0x3c20, (%rcx)         # imm = 0x3C20
 722bd95:      	addq	$0x2, 0x20(%rax)
 722bd9a:      	movq	0x18(%rsp), %r13
 722bd9f:      	leaq	0x88(%rsp), %rbp
 722bda7:      	movq	0x8(%rsp), %r14
 722bdac:      	movq	0x78(%rsp), %rdi
 722bdb1:      	cmpq	%rbp, %rdi
 722bdb4:      	je	0x722bdc6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19e6>
 722bdb6:      	movq	0x88(%rsp), %rsi
 722bdbe:      	incq	%rsi
 722bdc1:      	callq	0x828a660 <_ZdlPvm@plt>
 722bdc6:      	movl	0x18(%r14), %eax
 722bdca:      	movl	%eax, 0x498(%rsp)
 722bdd1:      	movzbl	0x1397418(%rip), %eax   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bdd8:      	testb	%al, %al
 722bdda:      	je	0x722bee9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b09>
 722bde0:      	movzbl	0x1397471(%rip), %eax   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bde7:      	testb	%al, %al
 722bde9:      	je	0x722bf0e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b2e>
 722bdef:      	leaq	0x498(%rsp), %rdi
 722bdf7:      	leaq	0x13973fa(%rip), %rsi   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bdfe:      	movq	0x70(%rsp), %rdx
 722be03:      	callq	0x437b420 <_ZNK5clang14SourceLocation5printERN4llvm11raw_ostreamERKNS_13SourceManagerE>
 722be08:      	movzbl	0x13973e1(%rip), %eax   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722be0f:      	testb	%al, %al
 722be11:      	je	0x722bf67 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b87>
 722be17:      	movzbl	0x139743a(%rip), %eax   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722be1e:      	testb	%al, %al
 722be20:      	je	0x722bf8c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1bac>
 722be26:      	movq	0x13973e3(%rip), %rcx   # 0x85c3210 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x18>
 722be2d:      	movq	0x13973e4(%rip), %rax   # 0x85c3218 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276+0x20>
 722be34:      	subq	%rax, %rcx
 722be37:      	cmpq	$0x1, %rcx
 722be3b:      	ja	0x722bb00 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1720>
 722be41:      	movl	$0x2, %edx
 722be46:      	leaq	0x13973ab(%rip), %rdi   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722be4d:      	leaq	-0x6498d7c(%rip), %rsi  # 0xd930d8 <.L.str.965>
 722be54:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 722be59:      	addq	$0x8, %rbx
 722be5d:      	cmpq	%r13, %rbx
 722be60:      	jne	0x722bb1a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722be66:      	jmp	0x722a840 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722be6b:      	leaq	0x139737e(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722be72:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722be77:      	testl	%eax, %eax
 722be79:      	je	0x722bb2c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x174c>
 722be7f:      	leaq	0x139736a(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722be86:      	callq	0x828a800 <__cxa_guard_release@plt>
 722be8b:      	jmp	0x722bb2c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x174c>
 722be90:      	leaq	0x13973c1(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722be97:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722be9c:      	testl	%eax, %eax
 722be9e:      	je	0x722bb3b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x175b>
 722bea4:      	leaq	0x139734d(%rip), %r14   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722beab:      	movq	%r14, %rdi
 722beae:      	movl	$0x2, %esi
 722beb3:      	xorl	%edx, %edx
 722beb5:      	movl	$0x1, %ecx
 722beba:      	xorl	%r8d, %r8d
 722bebd:      	callq	0x4145b10 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722bec2:      	leaq	-0x30e5249(%rip), %rdi  # 0x4146c80 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722bec9:      	movq	%r14, %rsi
 722becc:      	leaq	0x133f345(%rip), %rdx   # 0x856b218 <__dso_handle>
 722bed3:      	callq	0x828a6d0 <__cxa_atexit@plt>
 722bed8:      	leaq	0x1397379(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bedf:      	callq	0x828a800 <__cxa_guard_release@plt>
 722bee4:      	jmp	0x722bb3b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x175b>
 722bee9:      	leaq	0x1397300(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bef0:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722bef5:      	testl	%eax, %eax
 722bef7:      	je	0x722bde0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a00>
 722befd:      	leaq	0x13972ec(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bf04:      	callq	0x828a800 <__cxa_guard_release@plt>
 722bf09:      	jmp	0x722bde0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a00>
 722bf0e:      	leaq	0x1397343(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bf15:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722bf1a:      	testl	%eax, %eax
 722bf1c:      	je	0x722bdef <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0f>
 722bf22:      	leaq	0x13972cf(%rip), %r14   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bf29:      	movq	%r14, %rdi
 722bf2c:      	movl	$0x2, %esi
 722bf31:      	xorl	%edx, %edx
 722bf33:      	movl	$0x1, %ecx
 722bf38:      	xorl	%r8d, %r8d
 722bf3b:      	callq	0x4145b10 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722bf40:      	leaq	-0x30e52c7(%rip), %rdi  # 0x4146c80 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722bf47:      	movq	%r14, %rsi
 722bf4a:      	leaq	0x133f2c7(%rip), %rdx   # 0x856b218 <__dso_handle>
 722bf51:      	callq	0x828a6d0 <__cxa_atexit@plt>
 722bf56:      	leaq	0x13972fb(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bf5d:      	callq	0x828a800 <__cxa_guard_release@plt>
 722bf62:      	jmp	0x722bdef <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0f>
 722bf67:      	leaq	0x1397282(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bf6e:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722bf73:      	testl	%eax, %eax
 722bf75:      	je	0x722be17 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a37>
 722bf7b:      	leaq	0x139726e(%rip), %rdi   # 0x85c31f0 <_ZGVZN4llvm4errsEvE2EC.llvm.13088000499810600276>
 722bf82:      	callq	0x828a800 <__cxa_guard_release@plt>
 722bf87:      	jmp	0x722be17 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a37>
 722bf8c:      	leaq	0x13972c5(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bf93:      	callq	0x828a7f0 <__cxa_guard_acquire@plt>
 722bf98:      	testl	%eax, %eax
 722bf9a:      	je	0x722be26 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a46>
 722bfa0:      	leaq	0x1397251(%rip), %r14   # 0x85c31f8 <_ZZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bfa7:      	movq	%r14, %rdi
 722bfaa:      	movl	$0x2, %esi
 722bfaf:      	xorl	%edx, %edx
 722bfb1:      	movl	$0x1, %ecx
 722bfb6:      	xorl	%r8d, %r8d
 722bfb9:      	callq	0x4145b10 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722bfbe:      	leaq	-0x30e5345(%rip), %rdi  # 0x4146c80 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722bfc5:      	movq	%r14, %rsi
 722bfc8:      	leaq	0x133f249(%rip), %rdx   # 0x856b218 <__dso_handle>
 722bfcf:      	callq	0x828a6d0 <__cxa_atexit@plt>
 722bfd4:      	leaq	0x139727d(%rip), %rdi   # 0x85c3258 <_ZGVZN4llvm4errsEvE1S.llvm.13088000499810600276>
 722bfdb:      	callq	0x828a800 <__cxa_guard_release@plt>
 722bfe0:      	jmp	0x722be26 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a46>
 722bfe5:      	movq	0x10(%rsp), %rbx
 722bfea:      	movq	(%rsp), %r14
 722bfee:      	callq	0x41460e0 <_ZN4llvm4errsEv>
 722bff3:      	movq	0x20(%rax), %rcx
 722bff7:      	cmpq	%rcx, 0x18(%rax)
 722bffb:      	je	0x722a6eb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x30b>
 722c001:      	movb	$0xa, (%rcx)
 722c004:      	incq	0x20(%rax)
 722c008:      	testq	%r14, %r14
 722c00b:      	je	0x722c01d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c3d>
 722c00d:      	movq	0x20(%rsp), %rsi
 722c012:      	subq	%r14, %rsi
 722c015:      	movq	%r14, %rdi
 722c018:      	callq	0x828a660 <_ZdlPvm@plt>
 722c01d:      	testq	%rbx, %rbx
 722c020:      	je	0x722c032 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c52>
 722c022:      	movq	0x38(%rsp), %rsi
 722c027:      	subq	%rbx, %rsi
 722c02a:      	movq	%rbx, %rdi
 722c02d:      	callq	0x828a660 <_ZdlPvm@plt>
 722c032:      	addq	$0xce8, %rsp            # imm = 0xCE8
 722c039:      	popq	%rbx
 722c03a:      	popq	%r12
 722c03c:      	popq	%r13
 722c03e:      	popq	%r14
 722c040:      	popq	%r15
 722c042:      	popq	%rbp
 722c043:      	retq
 722c044:      	leaq	-0x65d805c(%rip), %rdi  # 0xc53fef <.L.str.979>
 722c04b:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
