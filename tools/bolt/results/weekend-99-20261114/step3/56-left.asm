
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000722a490 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE>:
 722a490:      	pushq	%rbp
 722a491:      	pushq	%r15
 722a493:      	pushq	%r14
 722a495:      	pushq	%r13
 722a497:      	pushq	%r12
 722a499:      	pushq	%rbx
 722a49a:      	subq	$0xce8, %rsp            # imm = 0xCE8
 722a4a1:      	movq	%rsi, 0x70(%rsp)
 722a4a6:      	movq	0x8(%rdi), %rdi
 722a4aa:      	movl	0x118(%rdi), %r14d
 722a4b1:      	testq	%r14, %r14
 722a4b4:      	je	0x722a51f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x8f>
 722a4b6:      	movq	%rdi, %rbx
 722a4b9:      	leaq	(,%r14,8), %rdi
 722a4c1:      	callq	0x828a6b0 <_Znwm@plt>
 722a4c6:      	movq	%rbx, %rdi
 722a4c9:      	movq	%rax, %rbx
 722a4cc:      	leaq	(%rax,%r14,8), %r8
 722a4d0:      	movq	0x110(%rdi), %rax
 722a4d7:      	movl	0x120(%rdi), %r15d
 722a4de:      	movq	%r15, %rcx
 722a4e1:      	shlq	$0x5, %rcx
 722a4e5:      	leaq	(%rax,%rcx), %r12
 722a4e9:      	testq	%r15, %r15
 722a4ec:      	je	0x722a761 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2d1>
 722a4f2:      	xorl	%r13d, %r13d
 722a4f5:      	movl	$0x1000, %edx           # imm = 0x1000
 722a4fa:      	nopw	(%rax,%rax)
 722a500:      	movq	(%rax,%r13), %rsi
 722a504:      	orq	%rdx, %rsi
 722a507:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 722a50e:      	jne	0x722a7bd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x32d>
 722a514:      	addq	$0x20, %r13
 722a518:      	cmpq	%r13, %rcx
 722a51b:      	jne	0x722a500 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x70>
 722a51d:      	jmp	0x722a53c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xac>
 722a51f:      	movq	0x110(%rdi), %rax
 722a526:      	movl	0x120(%rdi), %r15d
 722a52d:      	movq	%r15, %r12
 722a530:      	shlq	$0x5, %r12
 722a534:      	addq	%rax, %r12
 722a537:      	xorl	%r8d, %r8d
 722a53a:      	xorl	%ebx, %ebx
 722a53c:      	movq	%r12, %r13
 722a53f:      	shlq	$0x5, %r15
 722a543:      	addq	%rax, %r15
 722a546:      	cmpq	%r15, %r13
 722a549:      	je	0x722a777 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2e7>
 722a54f:      	addq	$0x110, %rdi            # imm = 0x110
 722a556:      	xorl	%ebp, %ebp
 722a558:      	movl	$0x1000, %ecx           # imm = 0x1000
 722a55d:      	movq	%r13, %rdx
 722a560:      	jmp	0x722a579 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe9>
 722a562:      	nopw	%cs:(%rax,%rax)
 722a56c:      	nopl	(%rax)
 722a570:      	leaq	0x1(%rax), %rbp
 722a574:      	cmpq	%r15, %rdx
 722a577:      	je	0x722a59a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10a>
 722a579:      	movq	%rbp, %rax
 722a57c:      	nopl	(%rax)
 722a580:      	addq	$0x20, %rdx
 722a584:      	cmpq	%r12, %rdx
 722a587:      	je	0x722a570 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe0>
 722a589:      	movq	(%rdx), %rsi
 722a58c:      	orq	%rcx, %rsi
 722a58f:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 722a596:      	je	0x722a580 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf0>
 722a598:      	jmp	0x722a570 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe0>
 722a59a:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 722a5a4:      	movq	%r8, %r14
 722a5a7:      	subq	%rbx, %r14
 722a5aa:      	movq	%r14, %rcx
 722a5ad:      	sarq	$0x3, %rcx
 722a5b1:      	cmpq	%rax, %rcx
 722a5b4:      	movq	%rdi, 0x40(%rsp)
 722a5b9:      	jbe	0x722a5fb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16b>
 722a5bb:      	movl	$0x1000, %eax           # imm = 0x1000
 722a5c0:      	movq	%rbx, %rcx
 722a5c3:      	jmp	0x722a5d9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x149>
 722a5c5:      	nopw	%cs:(%rax,%rax)
 722a5cf:      	nop
 722a5d0:      	addq	$0x8, %rcx
 722a5d4:      	cmpq	%r15, %r13
 722a5d7:      	je	0x722a64b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1bb>
 722a5d9:      	movq	(%r13), %rdx
 722a5dd:      	movq	%rdx, (%rcx)
 722a5e0:      	addq	$0x20, %r13
 722a5e4:      	cmpq	%r12, %r13
 722a5e7:      	je	0x722a5d0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x140>
 722a5e9:      	movq	(%r13), %rdx
 722a5ed:      	orq	%rax, %rdx
 722a5f0:      	cmpq	$-0x1000, %rdx          # imm = 0xF000
 722a5f7:      	je	0x722a5e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x150>
 722a5f9:      	jmp	0x722a5d0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x140>
 722a5fb:      	cmpq	%rdx, %rax
 722a5fe:      	jae	0x722c0f4 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c64>
 722a604:      	leaq	(,%rbp,8), %rdi
 722a60c:      	callq	0x828a6b0 <_Znwm@plt>
 722a611:      	movl	$0x1000, %edx           # imm = 0x1000
 722a616:      	movq	%rax, 0x10(%rsp)
 722a61b:      	jmp	0x722a629 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x199>
 722a61d:      	nopl	(%rax)
 722a620:      	addq	$0x8, %rax
 722a624:      	cmpq	%r15, %r13
 722a627:      	je	0x722a659 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c9>
 722a629:      	movq	(%r13), %rcx
 722a62d:      	movq	%rcx, (%rax)
 722a630:      	addq	$0x20, %r13
 722a634:      	cmpq	%r12, %r13
 722a637:      	je	0x722a620 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x190>
 722a639:      	movq	(%r13), %rcx
 722a63d:      	orq	%rdx, %rcx
 722a640:      	cmpq	$-0x1000, %rcx          # imm = 0xF000
 722a647:      	je	0x722a630 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0>
 722a649:      	jmp	0x722a620 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x190>
 722a64b:      	movq	%r8, 0x38(%rsp)
 722a650:      	leaq	(%rbx,%rbp,8), %r15
 722a654:      	movq	%rbx, %r12
 722a657:      	jmp	0x722a67a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1ea>
 722a659:      	movq	%rax, %r15
 722a65c:      	testq	%rbx, %rbx
 722a65f:      	je	0x722a66c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1dc>
 722a661:      	movq	%rbx, %rdi
 722a664:      	movq	%r14, %rsi
 722a667:      	callq	0x828a6f0 <_ZdlPvm@plt>
 722a66c:      	movq	0x10(%rsp), %r12
 722a671:      	leaq	(%r12,%rbp,8), %rax
 722a675:      	movq	%rax, 0x38(%rsp)
 722a67a:      	movq	%r15, %r14
 722a67d:      	subq	%r12, %r14
 722a680:      	movq	%r14, %rax
 722a683:      	sarq	$0x3, %rax
 722a687:      	bsrq	%rax, %rdx
 722a68b:      	xorl	$0x3f, %edx
 722a68e:      	addl	%edx, %edx
 722a690:      	xorq	$0x7e, %rdx
 722a694:      	movq	%r12, %rdi
 722a697:      	movq	%r15, %rsi
 722a69a:      	callq	0x7231e30 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN5clang8CFGBlockESt6vectorIS5_SaIS5_EEEElNS0_5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117LiveVariablesImpl17dumpBlockLivenessERKNS2_13SourceManagerEE3$_0EEEvT_SK_T0_T1_>
 722a69f:      	leaq	0x8(%r12), %rbx
 722a6a4:      	cmpq	$0x81, %r14
 722a6ab:      	movq	%r12, 0x10(%rsp)
 722a6b0:      	movq	%r15, 0x28(%rsp)
 722a6b5:      	jl	0x722a6c5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x235>
 722a6b7:      	movl	$0x8, %r14d
 722a6bd:      	movq	%rbx, %r15
 722a6c0:      	jmp	0x722a7f5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x365>
 722a6c5:      	cmpq	%r15, %rbx
 722a6c8:      	je	0x722a8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a6ce:      	movq	%r12, %r14
 722a6d1:      	jmp	0x722a71b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x28b>
 722a6d3:      	nopw	%cs:(%rax,%rax)
 722a6dd:      	nopl	(%rax)
 722a6e0:      	movq	%r14, %rdx
 722a6e3:      	subq	%r12, %rdx
 722a6e6:      	movq	%rdx, %rax
 722a6e9:      	sarq	$0x3, %rax
 722a6ed:      	cmpq	$0x2, %rax
 722a6f1:      	jl	0x722a752 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2c2>
 722a6f3:      	shlq	$0x3, %rax
 722a6f7:      	subq	%rax, %rdi
 722a6fa:      	addq	$0x10, %rdi
 722a6fe:      	movq	%r12, %rsi
 722a701:      	callq	0x828ac50 <memmove@plt>
 722a706:      	movq	%r12, %rax
 722a709:      	movq	%rbx, (%rax)
 722a70c:      	leaq	0x8(%r14), %rbx
 722a710:      	cmpq	0x28(%rsp), %rbx
 722a715:      	je	0x722a8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a71b:      	movq	%r14, %rdi
 722a71e:      	movq	%rbx, %r14
 722a721:      	movq	(%rbx), %rbx
 722a724:      	movq	(%r12), %rsi
 722a728:      	movl	0x30(%rbx), %ecx
 722a72b:      	cmpl	0x30(%rsi), %ecx
 722a72e:      	jb	0x722a6e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x250>
 722a730:      	movq	(%rdi), %rdx
 722a733:      	movq	%r14, %rax
 722a736:      	cmpl	0x30(%rdx), %ecx
 722a739:      	jae	0x722a709 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a73b:      	movq	%r14, %rax
 722a73e:      	nop
 722a740:      	movq	%rdx, (%rax)
 722a743:      	movq	-0x10(%rax), %rdx
 722a747:      	addq	$-0x8, %rax
 722a74b:      	cmpl	0x30(%rdx), %ecx
 722a74e:      	jb	0x722a740 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2b0>
 722a750:      	jmp	0x722a709 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a752:      	movq	%r12, %rax
 722a755:      	cmpq	$0x8, %rdx
 722a759:      	jne	0x722a709 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x279>
 722a75b:      	movq	%rsi, 0x8(%rdi)
 722a75f:      	jmp	0x722a706 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x276>
 722a761:      	xorl	%r15d, %r15d
 722a764:      	movq	%rax, %r13
 722a767:      	shlq	$0x5, %r15
 722a76b:      	addq	%rax, %r15
 722a76e:      	cmpq	%r15, %r13
 722a771:      	jne	0x722a54f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbf>
 722a777:      	movq	%r8, 0x38(%rsp)
 722a77c:      	xorl	%r14d, %r14d
 722a77f:      	movq	$0x0, 0x20(%rsp)
 722a788:      	callq	0x4146170 <_ZN4llvm4errsEv>
 722a78d:      	movq	0x20(%rax), %rcx
 722a791:      	cmpq	%rcx, 0x18(%rax)
 722a795:      	jne	0x722c0b1 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c21>
 722a79b:      	leaq	-0x64d230d(%rip), %rsi  # 0xd58495 <.str.llvm.17982220806007074922>
 722a7a2:      	movl	$0x1, %edx
 722a7a7:      	movq	%rax, %rdi
 722a7aa:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a7af:      	testq	%r14, %r14
 722a7b2:      	jne	0x722c0bd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c2d>
 722a7b8:      	jmp	0x722c0cd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c3d>
 722a7bd:      	addq	%rax, %r13
 722a7c0:      	shlq	$0x5, %r15
 722a7c4:      	addq	%rax, %r15
 722a7c7:      	cmpq	%r15, %r13
 722a7ca:      	jne	0x722a54f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbf>
 722a7d0:      	jmp	0x722a777 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x2e7>
 722a7d2:      	movq	%rdx, 0x8(%rcx)
 722a7d6:      	movq	0x10(%rsp), %rbp
 722a7db:      	nopl	(%rax,%rax)
 722a7e0:      	movq	%r13, (%rbp)
 722a7e4:      	addq	$0x8, %r14
 722a7e8:      	addq	$0x8, %r15
 722a7ec:      	cmpq	$0x80, %r14
 722a7f3:      	je	0x722a853 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3c3>
 722a7f5:      	movq	%r12, %rcx
 722a7f8:      	movq	0x10(%rsp), %rax
 722a7fd:      	leaq	(%rax,%r14), %r12
 722a801:      	movq	(%rax,%r14), %r13
 722a805:      	movq	(%rax), %rdx
 722a808:      	movl	0x30(%r13), %eax
 722a80c:      	cmpl	0x30(%rdx), %eax
 722a80f:      	jae	0x722a830 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3a0>
 722a811:      	cmpq	$0x9, %r14
 722a815:      	jb	0x722a7d2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x342>
 722a817:      	movq	%rbx, %rdi
 722a81a:      	movq	0x10(%rsp), %rbp
 722a81f:      	movq	%rbp, %rsi
 722a822:      	movq	%r14, %rdx
 722a825:      	callq	0x828ac50 <memmove@plt>
 722a82a:      	jmp	0x722a7e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a82c:      	nopl	(%rax)
 722a830:      	movq	(%rcx), %rdx
 722a833:      	movq	%r12, %rbp
 722a836:      	cmpl	0x30(%rdx), %eax
 722a839:      	jae	0x722a7e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a83b:      	movq	%r15, %rbp
 722a83e:      	nop
 722a840:      	movq	%rdx, (%rbp)
 722a844:      	movq	-0x10(%rbp), %rdx
 722a848:      	addq	$-0x8, %rbp
 722a84c:      	cmpl	0x30(%rdx), %eax
 722a84f:      	jb	0x722a840 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3b0>
 722a851:      	jmp	0x722a7e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x350>
 722a853:      	movq	0x10(%rsp), %r12
 722a858:      	leaq	0x80(%r12), %rax
 722a860:      	jmp	0x722a877 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e7>
 722a862:      	nopw	%cs:(%rax,%rax)
 722a86c:      	nopl	(%rax)
 722a870:      	movq	%rcx, (%rdi)
 722a873:      	addq	$0x8, %rax
 722a877:      	cmpq	0x28(%rsp), %rax
 722a87c:      	je	0x722a8b2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x422>
 722a87e:      	movq	-0x8(%rax), %rdx
 722a882:      	movq	(%rax), %rcx
 722a885:      	movl	0x30(%rcx), %esi
 722a888:      	movq	%rax, %rdi
 722a88b:      	cmpl	0x30(%rdx), %esi
 722a88e:      	jae	0x722a870 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e0>
 722a890:      	movq	%rax, %rdi
 722a893:      	nopw	%cs:(%rax,%rax)
 722a89d:      	nopl	(%rax)
 722a8a0:      	movq	%rdx, (%rdi)
 722a8a3:      	movq	-0x10(%rdi), %rdx
 722a8a7:      	addq	$-0x8, %rdi
 722a8ab:      	cmpl	0x30(%rdx), %esi
 722a8ae:      	jb	0x722a8a0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x410>
 722a8b0:      	jmp	0x722a870 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x3e0>
 722a8b2:      	leaq	0x1103e7f(%rip), %rax   # 0x832e738 <_ZTVN4llvm18raw_string_ostreamE>
 722a8b9:      	addq	$0x10, %rax
 722a8bd:      	movq	%rax, 0x68(%rsp)
 722a8c2:      	leaq	0x11039f7(%rip), %rax   # 0x832e2c0 <_ZTVN4llvm11raw_ostreamE>
 722a8c9:      	addq	$0x10, %rax
 722a8cd:      	movq	%rax, 0x60(%rsp)
 722a8d2:      	movq	$0x0, (%rsp)
 722a8da:      	xorl	%r13d, %r13d
 722a8dd:      	movq	$0x0, 0x20(%rsp)
 722a8e6:      	jmp	0x722a904 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x474>
 722a8e8:      	nopl	(%rax,%rax)
 722a8f0:      	movq	0x50(%rsp), %r12
 722a8f5:      	addq	$0x8, %r12
 722a8f9:      	cmpq	0x28(%rsp), %r12
 722a8fe:      	je	0x722c095 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c05>
 722a904:      	movq	%r12, 0x50(%rsp)
 722a909:      	movq	(%r12), %r15
 722a90d:      	callq	0x4146170 <_ZN4llvm4errsEv>
 722a912:      	movq	%rax, %r12
 722a915:      	movq	0x18(%rax), %rcx
 722a919:      	movq	0x20(%rax), %rax
 722a91d:      	subq	%rax, %rcx
 722a920:      	cmpq	$0x3, %rcx
 722a924:      	ja	0x722a940 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x4b0>
 722a926:      	movl	$0x4, %edx
 722a92b:      	movq	%r12, %rdi
 722a92e:      	leaq	-0x652bdca(%rip), %rsi  # 0xcfeb6b <.L.str.1>
 722a935:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a93a:      	movq	%rax, %r12
 722a93d:      	jmp	0x722a94c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x4bc>
 722a93f:      	nop
 722a940:      	movl	$0x42205b0a, (%rax)     # imm = 0x42205B0A
 722a946:      	addq	$0x4, 0x20(%r12)
 722a94c:      	movl	0x30(%r15), %esi
 722a950:      	movq	%r12, %rdi
 722a953:      	xorl	%edx, %edx
 722a955:      	xorl	%ecx, %ecx
 722a957:      	xorl	%r8d, %r8d
 722a95a:      	callq	0x40f1850 <_ZL14write_unsignedImEvRN4llvm11raw_ostreamET_mNS0_12IntegerStyleEb.llvm.1874658309496332414>
 722a95f:      	movq	0x18(%r12), %rcx
 722a964:      	movq	0x20(%r12), %rax
 722a969:      	subq	%rax, %rcx
 722a96c:      	cmpq	$0x21, %rcx
 722a970:      	ja	0x722a990 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x500>
 722a972:      	movl	$0x22, %edx
 722a977:      	movq	%r12, %rdi
 722a97a:      	leaq	-0x65d992a(%rip), %rsi  # 0xc51057 <.L.str.2>
 722a981:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722a986:      	jmp	0x722a9b1 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x521>
 722a988:      	nopl	(%rax,%rax)
 722a990:      	movups	-0x65d9930(%rip), %xmm0 # 0xc51067 <.L.str.2+0x10>
 722a997:      	movups	%xmm0, 0x10(%rax)
 722a99b:      	movups	-0x65d994b(%rip), %xmm0 # 0xc51057 <.L.str.2>
 722a9a2:      	movups	%xmm0, (%rax)
 722a9a5:      	movw	$0xa5d, 0x20(%rax)      # imm = 0xA5D
 722a9ab:      	addq	$0x22, 0x20(%r12)
 722a9b1:      	movq	0x40(%rsp), %rdi
 722a9b6:      	movq	(%rsp), %rax
 722a9ba:      	cmpq	%rax, %r13
 722a9bd:      	cmovneq	%rax, %r13
 722a9c1:      	movq	%r15, %rsi
 722a9c4:      	callq	0x7236810 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPKN5clang8CFGBlockENS2_13LiveVariables14LivenessValuesENS_12DenseMapInfoIS5_vEENS_6detail12DenseMapPairIS5_S7_EEEES5_S7_S9_SC_E24lookupOrInsertIntoBucketIRKS5_JEEESt4pairIPSC_bEOT_DpOT0_>
 722a9c9:      	movq	0x10(%rax), %rsi
 722a9cd:      	leaq	0x4a8(%rsp), %rax
 722a9d5:      	movq	%rax, 0x498(%rsp)
 722a9dd:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722a9e7:      	movq	%rax, 0x4a0(%rsp)
 722a9ef:      	testq	%rsi, %rsi
 722a9f2:      	je	0x722ab10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722a9f8:      	movq	%rsi, 0x4a8(%rsp)
 722aa00:      	movl	$0x1, 0x4a0(%rsp)
 722aa0b:      	movl	$0x1, %eax
 722aa10:      	leaq	0x4a8(%rsp), %rcx
 722aa18:      	jmp	0x722aa40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x5b0>
 722aa1a:      	orq	$0x3, %rsi
 722aa1e:      	movq	%rsi, -0x8(%rcx,%rdx,8)
 722aa23:      	movq	0x498(%rsp), %rcx
 722aa2b:      	movl	%eax, %edx
 722aa2d:      	movq	-0x8(%rcx,%rdx,8), %rsi
 722aa32:      	movl	%esi, %edx
 722aa34:      	andl	$0x3, %edx
 722aa37:      	cmpl	$0x1, %edx
 722aa3a:      	je	0x722ad40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x8b0>
 722aa40:      	movl	%esi, %edi
 722aa42:      	andl	$0x3, %edi
 722aa45:      	cmpq	$0x3, %rdi
 722aa49:      	je	0x722aa70 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x5e0>
 722aa4b:      	movl	%eax, %edx
 722aa4d:      	movq	%rsi, %r8
 722aa50:      	andq	$-0x4, %r8
 722aa54:      	cmpl	$0x1, %edi
 722aa57:      	jne	0x722aaa0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x610>
 722aa59:      	movq	0x10(%r8), %rbx
 722aa5d:      	testq	%rbx, %rbx
 722aa60:      	jne	0x722aaa9 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x619>
 722aa62:      	jmp	0x722aa1a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x58a>
 722aa64:      	nopw	%cs:(%rax,%rax)
 722aa6e:      	nop
 722aa70:      	decl	%eax
 722aa72:      	movl	%eax, 0x4a0(%rsp)
 722aa79:      	je	0x722ab10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722aa7f:      	movl	%eax, %edx
 722aa81:      	movq	-0x8(%rcx,%rdx,8), %rsi
 722aa86:      	xorl	%edi, %edi
 722aa88:      	testb	$0x3, %sil
 722aa8c:      	setne	%dil
 722aa90:      	addl	%edi, %edi
 722aa92:      	orq	%rsi, %rdi
 722aa95:      	orq	$0x1, %rdi
 722aa99:      	movq	%rdi, -0x8(%rcx,%rdx,8)
 722aa9e:      	jmp	0x722aa23 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x593>
 722aaa0:      	movq	0x8(%r8), %rbx
 722aaa4:      	testq	%rbx, %rbx
 722aaa7:      	je	0x722aace <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x63e>
 722aaa9:      	cmpl	0x4a4(%rsp), %eax
 722aab0:      	jae	0x722aad7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x647>
 722aab2:      	movq	%rbx, (%rcx,%rdx,8)
 722aab6:      	movl	0x4a0(%rsp), %eax
 722aabd:      	incl	%eax
 722aabf:      	movl	%eax, 0x4a0(%rsp)
 722aac6:      	jne	0x722aa23 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x593>
 722aacc:      	jmp	0x722ab10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x680>
 722aace:      	orq	$0x1, %rsi
 722aad2:      	jmp	0x722aa1e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x58e>
 722aad7:      	incq	%rdx
 722aada:      	movl	$0x8, %ecx
 722aadf:      	leaq	0x498(%rsp), %rdi
 722aae7:      	leaq	0x4a8(%rsp), %rsi
 722aaef:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722aaf4:      	movl	0x4a0(%rsp), %edx
 722aafb:      	movq	0x498(%rsp), %rcx
 722ab03:      	jmp	0x722aab2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x622>
 722ab05:      	nopw	%cs:(%rax,%rax)
 722ab0f:      	nop
 722ab10:      	leaq	0x828(%rsp), %rax
 722ab18:      	movq	%rax, 0x818(%rsp)
 722ab20:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ab2a:      	movq	%rax, 0x820(%rsp)
 722ab32:      	movq	0x498(%rsp), %rdi
 722ab3a:      	leaq	0x4a8(%rsp), %rax
 722ab42:      	cmpq	%rax, %rdi
 722ab45:      	je	0x722ab4c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6bc>
 722ab47:      	callq	0x828a6d0 <free@plt>
 722ab4c:      	leaq	0xc48(%rsp), %rax
 722ab54:      	xorps	%xmm0, %xmm0
 722ab57:      	movups	%xmm0, 0x90(%rax)
 722ab5e:      	movups	%xmm0, 0x80(%rax)
 722ab65:      	movups	%xmm0, 0x70(%rax)
 722ab69:      	movups	%xmm0, 0x60(%rax)
 722ab6d:      	movups	%xmm0, 0x50(%rax)
 722ab71:      	movups	%xmm0, 0x40(%rax)
 722ab75:      	movups	%xmm0, 0x30(%rax)
 722ab79:      	movups	%xmm0, 0x20(%rax)
 722ab7d:      	movups	%xmm0, 0x10(%rax)
 722ab81:      	movups	%xmm0, (%rax)
 722ab84:      	movq	%rax, 0xc38(%rsp)
 722ab8c:      	movabsq	$0x1400000000, %rdx     # imm = 0x1400000000
 722ab96:      	movq	%rdx, 0xc40(%rsp)
 722ab9e:      	leaq	0x138(%rsp), %rax
 722aba6:      	movq	%rax, 0x128(%rsp)
 722abae:      	movq	%rdx, 0x130(%rsp)
 722abb6:      	movl	0x820(%rsp), %ebp
 722abbd:      	testq	%rbp, %rbp
 722abc0:      	je	0x722ad10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x880>
 722abc6:      	movq	%rax, %rdi
 722abc9:      	movl	%ebp, %eax
 722abcb:      	cmpl	$0x15, %ebp
 722abce:      	jb	0x722ac00 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x770>
 722abd0:      	movl	$0x8, %ecx
 722abd5:      	leaq	0x128(%rsp), %rdi
 722abdd:      	leaq	0x138(%rsp), %rsi
 722abe5:      	movq	%rbp, %rdx
 722abe8:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722abed:      	movl	0x820(%rsp), %eax
 722abf4:      	testl	%eax, %eax
 722abf6:      	je	0x722ac13 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x783>
 722abf8:      	movq	0x128(%rsp), %rdi
 722ac00:      	movl	%eax, %edx
 722ac02:      	movq	0x818(%rsp), %rsi
 722ac0a:      	shlq	$0x3, %rdx
 722ac0e:      	callq	0x828ace0 <memcpy@plt>
 722ac13:      	movl	%ebp, 0x130(%rsp)
 722ac1a:      	movl	0xc40(%rsp), %r15d
 722ac22:      	leaq	0x1e8(%rsp), %rsi
 722ac2a:      	movq	%rsi, 0x1d8(%rsp)
 722ac32:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ac3c:      	movq	%rax, 0x1e0(%rsp)
 722ac44:      	testq	%r15, %r15
 722ac47:      	je	0x722ada0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x910>
 722ac4d:      	movq	%r15, %rdx
 722ac50:      	movq	%rsi, %rdi
 722ac53:      	cmpl	$0x15, %r15d
 722ac57:      	jb	0x722ac82 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x7f2>
 722ac59:      	movl	$0x8, %ecx
 722ac5e:      	leaq	0x1d8(%rsp), %rdi
 722ac66:      	movq	%r15, %rdx
 722ac69:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722ac6e:      	movl	0xc40(%rsp), %edx
 722ac75:      	testq	%rdx, %rdx
 722ac78:      	je	0x722ac93 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x803>
 722ac7a:      	movq	0x1d8(%rsp), %rdi
 722ac82:      	movq	0xc38(%rsp), %rsi
 722ac8a:      	shlq	$0x3, %rdx
 722ac8e:      	callq	0x828ace0 <memcpy@plt>
 722ac93:      	movl	%r15d, 0x1e0(%rsp)
 722ac9b:      	movl	0x130(%rsp), %ebp
 722aca2:      	cmpl	%r15d, %ebp
 722aca5:      	jne	0x722adb7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x927>
 722acab:      	leaq	(,%r15,8), %rdx
 722acb3:      	movq	0x128(%rsp), %rdi
 722acbb:      	movq	0x1d8(%rsp), %rsi
 722acc3:      	callq	0x828a750 <bcmp@plt>
 722acc8:      	testl	%eax, %eax
 722acca:      	je	0x722aecf <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa3f>
 722acd0:      	leaq	0x88(%rsp), %rax
 722acd8:      	movq	%rax, 0x78(%rsp)
 722acdd:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ace7:      	movq	%rax, 0x80(%rsp)
 722acef:      	movl	%r15d, %ebp
 722acf2:      	cmpl	$0x15, %ebp
 722acf5:      	jae	0x722adf2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x962>
 722acfb:      	leaq	0x88(%rsp), %rdi
 722ad03:      	jmp	0x722ae29 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x999>
 722ad08:      	nopl	(%rax,%rax)
 722ad10:      	leaq	0x1e8(%rsp), %rcx
 722ad18:      	movq	%rcx, 0x1d8(%rsp)
 722ad20:      	movq	%rdx, 0x1e0(%rsp)
 722ad28:      	leaq	0x88(%rsp), %rbp
 722ad30:      	jmp	0x722b84e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13be>
 722ad35:      	nopw	%cs:(%rax,%rax)
 722ad3f:      	nop
 722ad40:      	leaq	0x828(%rsp), %rax
 722ad48:      	movq	%rax, 0x818(%rsp)
 722ad50:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ad5a:      	movq	%rax, 0x820(%rsp)
 722ad62:      	leaq	0x818(%rsp), %rdi
 722ad6a:      	leaq	0x498(%rsp), %rsi
 722ad72:      	callq	0x2a30b90 <_ZN4llvm15SmallVectorImplImEaSEOS1_>
 722ad77:      	movq	0x498(%rsp), %rdi
 722ad7f:      	leaq	0x4a8(%rsp), %rax
 722ad87:      	cmpq	%rax, %rdi
 722ad8a:      	jne	0x722ab47 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6b7>
 722ad90:      	jmp	0x722ab4c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x6bc>
 722ad95:      	nopw	%cs:(%rax,%rax)
 722ad9f:      	nop
 722ada0:      	leaq	0x88(%rsp), %rcx
 722ada8:      	movq	%rcx, 0x78(%rsp)
 722adad:      	movq	%rax, 0x80(%rsp)
 722adb5:      	jmp	0x722ade6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x956>
 722adb7:      	leaq	0x88(%rsp), %rax
 722adbf:      	movq	%rax, 0x78(%rsp)
 722adc4:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722adce:      	movq	%rax, 0x80(%rsp)
 722add6:      	testl	%ebp, %ebp
 722add8:      	leaq	0x348(%rsp), %rdi
 722ade0:      	je	0x722aeec <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa5c>
 722ade6:      	movl	%ebp, %r15d
 722ade9:      	cmpl	$0x15, %ebp
 722adec:      	jb	0x722acfb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x86b>
 722adf2:      	movl	$0x0, 0x80(%rsp)
 722adfd:      	movl	$0x8, %ecx
 722ae02:      	leaq	0x78(%rsp), %rdi
 722ae07:      	leaq	0x88(%rsp), %rsi
 722ae0f:      	movq	%r15, %rdx
 722ae12:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722ae17:      	movl	0x130(%rsp), %r15d
 722ae1f:      	testq	%r15, %r15
 722ae22:      	je	0x722ae3d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x9ad>
 722ae24:      	movq	0x78(%rsp), %rdi
 722ae29:      	movq	0x128(%rsp), %rsi
 722ae31:      	shlq	$0x3, %r15
 722ae35:      	movq	%r15, %rdx
 722ae38:      	callq	0x828ace0 <memcpy@plt>
 722ae3d:      	movl	%ebp, 0x80(%rsp)
 722ae44:      	movl	0x1e0(%rsp), %r15d
 722ae4c:      	leaq	0x348(%rsp), %rdi
 722ae54:      	movq	%rdi, 0x338(%rsp)
 722ae5c:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722ae66:      	movq	%rax, 0x340(%rsp)
 722ae6e:      	testl	%r15d, %r15d
 722ae71:      	je	0x722aeb2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa22>
 722ae73:      	movl	%r15d, %eax
 722ae76:      	cmpl	$0x15, %r15d
 722ae7a:      	jb	0x722af10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa80>
 722ae80:      	movl	%r15d, %edx
 722ae83:      	movl	$0x8, %ecx
 722ae88:      	leaq	0x338(%rsp), %rdi
 722ae90:      	leaq	0x348(%rsp), %rsi
 722ae98:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722ae9d:      	movl	0x1e0(%rsp), %eax
 722aea4:      	testl	%eax, %eax
 722aea6:      	je	0x722af23 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa93>
 722aea8:      	movq	0x338(%rsp), %rdi
 722aeb0:      	jmp	0x722af10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xa80>
 722aeb2:      	leaq	0x4a8(%rsp), %rdi
 722aeba:      	movq	%rdi, 0x498(%rsp)
 722aec2:      	movq	%rax, 0x4a0(%rsp)
 722aeca:      	jmp	0x722af5c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xacc>
 722aecf:      	leaq	0x138(%rsp), %rax
 722aed7:      	leaq	0x1e8(%rsp), %rcx
 722aedf:      	leaq	0x88(%rsp), %rbp
 722aee7:      	jmp	0x722b84e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13be>
 722aeec:      	movq	%rdi, 0x338(%rsp)
 722aef4:      	movq	%rax, 0x340(%rsp)
 722aefc:      	movl	%r15d, %eax
 722aeff:      	cmpl	$0x15, %r15d
 722af03:      	jae	0x722ae80 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x9f0>
 722af09:      	nopl	(%rax)
 722af10:      	movl	%eax, %edx
 722af12:      	movq	0x1d8(%rsp), %rsi
 722af1a:      	shlq	$0x3, %rdx
 722af1e:      	callq	0x828ace0 <memcpy@plt>
 722af23:      	movl	%r15d, 0x340(%rsp)
 722af2b:      	movl	0x80(%rsp), %ebp
 722af32:      	leaq	0x4a8(%rsp), %rdi
 722af3a:      	movq	%rdi, 0x498(%rsp)
 722af42:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722af4c:      	movq	%rax, 0x4a0(%rsp)
 722af54:      	testl	%ebp, %ebp
 722af56:      	je	0x722afe8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb58>
 722af5c:      	movl	%ebp, %eax
 722af5e:      	cmpl	$0x15, %ebp
 722af61:      	jb	0x722af92 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb02>
 722af63:      	movl	%ebp, %edx
 722af65:      	movl	$0x8, %ecx
 722af6a:      	leaq	0x498(%rsp), %rdi
 722af72:      	leaq	0x4a8(%rsp), %rsi
 722af7a:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722af7f:      	movl	0x80(%rsp), %eax
 722af86:      	testl	%eax, %eax
 722af88:      	je	0x722afa2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb12>
 722af8a:      	movq	0x498(%rsp), %rdi
 722af92:      	movl	%eax, %edx
 722af94:      	movq	0x78(%rsp), %rsi
 722af99:      	shlq	$0x3, %rdx
 722af9d:      	callq	0x828ace0 <memcpy@plt>
 722afa2:      	movl	%ebp, 0x4a0(%rsp)
 722afa9:      	movl	0x340(%rsp), %r15d
 722afb1:      	leaq	0x298(%rsp), %rdi
 722afb9:      	movq	%rdi, 0x288(%rsp)
 722afc1:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722afcb:      	movq	%rax, 0x290(%rsp)
 722afd3:      	testl	%r15d, %r15d
 722afd6:      	je	0x722afe3 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb53>
 722afd8:      	movl	%r15d, %eax
 722afdb:      	cmpl	$0x15, %r15d
 722afdf:      	jae	0x722b009 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xb79>
 722afe1:      	jmp	0x722b039 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xba9>
 722afe3:      	xorl	%r15d, %r15d
 722afe6:      	jmp	0x722b05b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbcb>
 722afe8:      	leaq	0x298(%rsp), %rdi
 722aff0:      	movq	%rdi, 0x288(%rsp)
 722aff8:      	movq	%rax, 0x290(%rsp)
 722b000:      	movl	%r15d, %eax
 722b003:      	cmpl	$0x15, %r15d
 722b007:      	jb	0x722b039 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xba9>
 722b009:      	movl	%r15d, %edx
 722b00c:      	movl	$0x8, %ecx
 722b011:      	leaq	0x288(%rsp), %rdi
 722b019:      	leaq	0x298(%rsp), %rsi
 722b021:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b026:      	movl	0x340(%rsp), %eax
 722b02d:      	testl	%eax, %eax
 722b02f:      	je	0x722b04c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbbc>
 722b031:      	movq	0x288(%rsp), %rdi
 722b039:      	movl	%eax, %edx
 722b03b:      	movq	0x338(%rsp), %rsi
 722b043:      	shlq	$0x3, %rdx
 722b047:      	callq	0x828ace0 <memcpy@plt>
 722b04c:      	movl	%r15d, 0x290(%rsp)
 722b054:      	movl	0x4a0(%rsp), %ebp
 722b05b:      	movq	%r13, %rax
 722b05e:      	subq	(%rsp), %rax
 722b062:      	movq	%rax, 0x8(%rsp)
 722b067:      	xorl	%ebx, %ebx
 722b069:      	jmp	0x722b07d <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbed>
 722b06b:      	nopl	(%rax,%rax)
 722b070:      	xorl	%ebp, %ebp
 722b072:      	incq	%rbx
 722b075:      	movl	0x290(%rsp), %r15d
 722b07d:      	cmpl	%r15d, %ebp
 722b080:      	jne	0x722b0c0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc30>
 722b082:      	movq	0x288(%rsp), %r12
 722b08a:      	testl	%r15d, %r15d
 722b08d:      	je	0x722b1f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd60>
 722b093:      	movl	%r15d, %r14d
 722b096:      	leaq	(,%r14,8), %rdx
 722b09e:      	movq	0x498(%rsp), %r15
 722b0a6:      	movq	%r15, %rdi
 722b0a9:      	movq	%r12, %rsi
 722b0ac:      	callq	0x828a750 <bcmp@plt>
 722b0b1:      	testl	%eax, %eax
 722b0b3:      	jne	0x722b0cb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc3b>
 722b0b5:      	jmp	0x722b1f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd60>
 722b0ba:      	nopw	(%rax,%rax)
 722b0c0:      	movq	0x498(%rsp), %r15
 722b0c8:      	movl	%ebp, %r14d
 722b0cb:      	movq	-0x8(%r15,%r14,8), %rax
 722b0d0:      	jmp	0x722b0fe <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc6e>
 722b0d2:      	orq	$0x3, %rax
 722b0d6:      	movq	%rax, -0x8(%r15,%rdx,8)
 722b0db:      	testl	%ebp, %ebp
 722b0dd:      	jne	0x722b1a0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd10>
 722b0e3:      	jmp	0x722b070 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b0e5:      	nopw	%cs:(%rax,%rax)
 722b0ef:      	nop
 722b0f0:      	movl	%eax, %ecx
 722b0f2:      	andl	$0x3, %ecx
 722b0f5:      	cmpl	$0x1, %ecx
 722b0f8:      	je	0x722b072 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe2>
 722b0fe:      	movl	%eax, %ecx
 722b100:      	andl	$0x3, %ecx
 722b103:      	cmpq	$0x3, %rcx
 722b107:      	je	0x722b130 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xca0>
 722b109:      	movl	%ebp, %edx
 722b10b:      	movq	%rax, %rsi
 722b10e:      	andq	$-0x4, %rsi
 722b112:      	cmpl	$0x1, %ecx
 722b115:      	jne	0x722b160 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcd0>
 722b117:      	movq	0x10(%rsi), %r14
 722b11b:      	testq	%r14, %r14
 722b11e:      	jne	0x722b169 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcd9>
 722b120:      	jmp	0x722b0d2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc42>
 722b122:      	nopw	%cs:(%rax,%rax)
 722b12c:      	nopl	(%rax)
 722b130:      	decl	%ebp
 722b132:      	movl	%ebp, 0x4a0(%rsp)
 722b139:      	je	0x722b070 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b13f:      	movl	%ebp, %ecx
 722b141:      	movq	-0x8(%r15,%rcx,8), %rdx
 722b146:      	xorl	%eax, %eax
 722b148:      	testb	$0x3, %dl
 722b14b:      	setne	%al
 722b14e:      	addl	%eax, %eax
 722b150:      	orq	%rdx, %rax
 722b153:      	orq	$0x1, %rax
 722b157:      	movq	%rax, -0x8(%r15,%rcx,8)
 722b15c:      	jmp	0x722b0f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc60>
 722b15e:      	nop
 722b160:      	movq	0x8(%rsi), %r14
 722b164:      	testq	%r14, %r14
 722b167:      	je	0x722b18f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xcff>
 722b169:      	cmpl	0x4a4(%rsp), %ebp
 722b170:      	jae	0x722b1b4 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd24>
 722b172:      	movq	%r14, (%r15,%rdx,8)
 722b176:      	movl	0x4a0(%rsp), %ebp
 722b17d:      	incl	%ebp
 722b17f:      	movl	%ebp, 0x4a0(%rsp)
 722b186:      	testl	%ebp, %ebp
 722b188:      	jne	0x722b1a0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd10>
 722b18a:      	jmp	0x722b070 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b18f:      	orq	$0x1, %rax
 722b193:      	movq	%rax, -0x8(%r15,%rdx,8)
 722b198:      	testl	%ebp, %ebp
 722b19a:      	je	0x722b070 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xbe0>
 722b1a0:      	movq	0x498(%rsp), %r15
 722b1a8:      	movl	%ebp, %eax
 722b1aa:      	movq	-0x8(%r15,%rax,8), %rax
 722b1af:      	jmp	0x722b0f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xc60>
 722b1b4:      	incq	%rdx
 722b1b7:      	movl	$0x8, %ecx
 722b1bc:      	leaq	0x498(%rsp), %rdi
 722b1c4:      	leaq	0x4a8(%rsp), %rsi
 722b1cc:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b1d1:      	movl	0x4a0(%rsp), %edx
 722b1d8:      	movq	0x498(%rsp), %r15
 722b1e0:      	jmp	0x722b172 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xce2>
 722b1e2:      	nopw	%cs:(%rax,%rax)
 722b1ec:      	nopl	(%rax)
 722b1f0:      	leaq	0x298(%rsp), %rax
 722b1f8:      	cmpq	%rax, %r12
 722b1fb:      	je	0x722b205 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd75>
 722b1fd:      	movq	%r12, %rdi
 722b200:      	callq	0x828a6d0 <free@plt>
 722b205:      	movq	0x498(%rsp), %rdi
 722b20d:      	leaq	0x4a8(%rsp), %rax
 722b215:      	cmpq	%rax, %rdi
 722b218:      	leaq	0x88(%rsp), %rbp
 722b220:      	je	0x722b227 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xd97>
 722b222:      	callq	0x828a6d0 <free@plt>
 722b227:      	movq	0x338(%rsp), %rdi
 722b22f:      	leaq	0x348(%rsp), %rax
 722b237:      	cmpq	%rax, %rdi
 722b23a:      	je	0x722b241 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xdb1>
 722b23c:      	callq	0x828a6d0 <free@plt>
 722b241:      	movq	0x78(%rsp), %rdi
 722b246:      	cmpq	%rbp, %rdi
 722b249:      	je	0x722b250 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xdc0>
 722b24b:      	callq	0x828a6d0 <free@plt>
 722b250:      	movq	0x20(%rsp), %rax
 722b255:      	subq	%r13, %rax
 722b258:      	sarq	$0x3, %rax
 722b25c:      	cmpq	%rbx, %rax
 722b25f:      	jae	0x722b460 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfd0>
 722b265:      	movq	0x8(%rsp), %r13
 722b26a:      	movq	%r13, %rax
 722b26d:      	sarq	$0x3, %rax
 722b271:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 722b27b:      	movq	%rdx, %rcx
 722b27e:      	subq	%rax, %rcx
 722b281:      	cmpq	%rbx, %rcx
 722b284:      	jb	0x722c0f4 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c64>
 722b28a:      	cmpq	%rbx, %rax
 722b28d:      	cmovaq	%rax, %rbx
 722b291:      	leaq	(%rbx,%rax), %r12
 722b295:      	cmpq	%rdx, %r12
 722b298:      	cmovaeq	%rdx, %r12
 722b29c:      	addq	%rax, %rbx
 722b29f:      	cmovbq	%rdx, %r12
 722b2a3:      	testq	%r12, %r12
 722b2a6:      	je	0x722b561 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10d1>
 722b2ac:      	leaq	(,%r12,8), %rdi
 722b2b4:      	callq	0x828a6b0 <_Znwm@plt>
 722b2b9:      	movq	%rax, %r15
 722b2bc:      	cmpq	$0x9, %r13
 722b2c0:      	jl	0x722b56e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10de>
 722b2c6:      	movq	%r15, %rdi
 722b2c9:      	movq	(%rsp), %rsi
 722b2cd:      	movq	%r13, %rdx
 722b2d0:      	callq	0x828ac50 <memmove@plt>
 722b2d5:      	leaq	0x8d8(%rsp), %rax
 722b2dd:      	movq	%rax, 0x8c8(%rsp)
 722b2e5:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b2ef:      	movq	%rax, 0x8d0(%rsp)
 722b2f7:      	movl	0x130(%rsp), %ebx
 722b2fe:      	testq	%rbx, %rbx
 722b301:      	je	0x722b366 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xed6>
 722b303:      	leaq	0x8d8(%rsp), %rdi
 722b30b:      	movl	%ebx, %eax
 722b30d:      	cmpl	$0x15, %ebx
 722b310:      	jb	0x722b342 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xeb2>
 722b312:      	movl	$0x8, %ecx
 722b317:      	leaq	0x8c8(%rsp), %rdi
 722b31f:      	leaq	0x8d8(%rsp), %rsi
 722b327:      	movq	%rbx, %rdx
 722b32a:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b32f:      	movl	0x130(%rsp), %eax
 722b336:      	testl	%eax, %eax
 722b338:      	je	0x722b355 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xec5>
 722b33a:      	movq	0x8c8(%rsp), %rdi
 722b342:      	movl	%eax, %edx
 722b344:      	movq	0x128(%rsp), %rsi
 722b34c:      	shlq	$0x3, %rdx
 722b350:      	callq	0x828ace0 <memcpy@plt>
 722b355:      	movl	%ebx, 0x8d0(%rsp)
 722b35c:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b366:      	leaq	0xa38(%rsp), %r14
 722b36e:      	movq	%r14, 0xa28(%rsp)
 722b376:      	movq	%rax, 0xa30(%rsp)
 722b37e:      	movl	0x1e0(%rsp), %ebx
 722b385:      	testq	%rbx, %rbx
 722b388:      	je	0x722b3e6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf56>
 722b38a:      	movq	%r14, %rdi
 722b38d:      	movl	%ebx, %eax
 722b38f:      	cmpl	$0x15, %ebx
 722b392:      	jb	0x722b3c4 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf34>
 722b394:      	movl	$0x8, %ecx
 722b399:      	leaq	0xa28(%rsp), %rdi
 722b3a1:      	leaq	0xa38(%rsp), %rsi
 722b3a9:      	movq	%rbx, %rdx
 722b3ac:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b3b1:      	movl	0x1e0(%rsp), %eax
 722b3b8:      	testl	%eax, %eax
 722b3ba:      	je	0x722b3d7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf47>
 722b3bc:      	movq	0xa28(%rsp), %rdi
 722b3c4:      	movl	%eax, %edx
 722b3c6:      	movq	0x1d8(%rsp), %rsi
 722b3ce:      	shlq	$0x3, %rdx
 722b3d2:      	callq	0x828ace0 <memcpy@plt>
 722b3d7:      	movl	%ebx, 0xa30(%rsp)
 722b3de:      	leaq	0xa38(%rsp), %r14
 722b3e6:      	addq	%r15, %r13
 722b3e9:      	leaq	0x8c8(%rsp), %rdi
 722b3f1:      	leaq	0xa28(%rsp), %rsi
 722b3f9:      	movq	%r13, %rdx
 722b3fc:      	callq	0x72325b0 <_ZSt22__uninitialized_copy_aIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEPS6_S6_ET0_T_SD_SC_RSaIT1_E>
 722b401:      	movq	%rax, %r13
 722b404:      	movq	0xa28(%rsp), %rdi
 722b40c:      	cmpq	%r14, %rdi
 722b40f:      	je	0x722b416 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xf86>
 722b411:      	callq	0x828a6d0 <free@plt>
 722b416:      	movq	0x8c8(%rsp), %rdi
 722b41e:      	leaq	0x8d8(%rsp), %rax
 722b426:      	cmpq	%rax, %rdi
 722b429:      	je	0x722b430 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfa0>
 722b42b:      	callq	0x828a6d0 <free@plt>
 722b430:      	movq	(%rsp), %rdi
 722b434:      	testq	%rdi, %rdi
 722b437:      	je	0x722b446 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xfb6>
 722b439:      	movq	0x20(%rsp), %rsi
 722b43e:      	subq	%rdi, %rsi
 722b441:      	callq	0x828a6f0 <_ZdlPvm@plt>
 722b446:      	leaq	(%r15,%r12,8), %rax
 722b44a:      	movq	%rax, 0x20(%rsp)
 722b44f:      	movq	%r15, (%rsp)
 722b453:      	jmp	0x722b83e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13ae>
 722b458:      	nopl	(%rax,%rax)
 722b460:      	leaq	0x4a8(%rsp), %rax
 722b468:      	movq	%rax, 0x498(%rsp)
 722b470:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b47a:      	movq	%rax, 0x4a0(%rsp)
 722b482:      	movl	0x130(%rsp), %r15d
 722b48a:      	testq	%r15, %r15
 722b48d:      	je	0x722b53a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10aa>
 722b493:      	cmpl	$0x15, %r15d
 722b497:      	jb	0x722b587 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x10f7>
 722b49d:      	movl	$0x8, %ecx
 722b4a2:      	leaq	0x498(%rsp), %rdi
 722b4aa:      	leaq	0x4a8(%rsp), %rsi
 722b4b2:      	movq	%r15, %rdx
 722b4b5:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b4ba:      	movl	0x130(%rsp), %edx
 722b4c1:      	testq	%rdx, %rdx
 722b4c4:      	je	0x722b4df <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x104f>
 722b4c6:      	movq	0x498(%rsp), %rdi
 722b4ce:      	movq	0x128(%rsp), %rsi
 722b4d6:      	shlq	$0x3, %rdx
 722b4da:      	callq	0x828ace0 <memcpy@plt>
 722b4df:      	movl	%r15d, 0x4a0(%rsp)
 722b4e7:      	leaq	0x3f8(%rsp), %rsi
 722b4ef:      	movq	%rsi, 0x3e8(%rsp)
 722b4f7:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b501:      	movq	%rax, 0x3f0(%rsp)
 722b509:      	movl	$0x8, %ecx
 722b50e:      	leaq	0x3e8(%rsp), %rdi
 722b516:      	movq	%r15, %rdx
 722b519:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b51e:      	movl	0x4a0(%rsp), %eax
 722b525:      	testl	%eax, %eax
 722b527:      	je	0x722b5e8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1158>
 722b52d:      	movq	0x3e8(%rsp), %rdi
 722b535:      	jmp	0x722b5d5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1145>
 722b53a:      	leaq	0x3f8(%rsp), %rax
 722b542:      	movq	%rax, 0x3e8(%rsp)
 722b54a:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b554:      	movq	%rax, 0x3f0(%rsp)
 722b55c:      	jmp	0x722b5fa <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x116a>
 722b561:      	xorl	%r15d, %r15d
 722b564:      	cmpq	$0x9, %r13
 722b568:      	jge	0x722b2c6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe36>
 722b56e:      	cmpq	$0x8, %r13
 722b572:      	jne	0x722b2d5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe45>
 722b578:      	movq	(%rsp), %rax
 722b57c:      	movq	(%rax), %rax
 722b57f:      	movq	%rax, (%r15)
 722b582:      	jmp	0x722b2d5 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0xe45>
 722b587:      	movq	0x128(%rsp), %rsi
 722b58f:      	movq	%r15, %rdx
 722b592:      	shlq	$0x3, %rdx
 722b596:      	movl	$0xa0, %ecx
 722b59b:      	leaq	0x4a8(%rsp), %rdi
 722b5a3:      	callq	0x828a730 <__memcpy_chk@plt>
 722b5a8:      	movl	%r15d, 0x4a0(%rsp)
 722b5b0:      	leaq	0x3f8(%rsp), %rdi
 722b5b8:      	movq	%rdi, 0x3e8(%rsp)
 722b5c0:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b5ca:      	movq	%rax, 0x3f0(%rsp)
 722b5d2:      	movl	%r15d, %eax
 722b5d5:      	movl	%eax, %edx
 722b5d7:      	movq	0x498(%rsp), %rsi
 722b5df:      	shlq	$0x3, %rdx
 722b5e3:      	callq	0x828ace0 <memcpy@plt>
 722b5e8:      	movl	%r15d, 0x3f0(%rsp)
 722b5f0:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b5fa:      	leaq	0xb98(%rsp), %r14
 722b602:      	movq	%r14, 0xb88(%rsp)
 722b60a:      	movq	%rax, 0xb90(%rsp)
 722b612:      	movl	0x1e0(%rsp), %r15d
 722b61a:      	testq	%r15, %r15
 722b61d:      	je	0x722b67e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11ee>
 722b61f:      	movq	%r14, %rdi
 722b622:      	movl	%r15d, %eax
 722b625:      	cmpl	$0x15, %r15d
 722b629:      	jb	0x722b65b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11cb>
 722b62b:      	movl	$0x8, %ecx
 722b630:      	leaq	0xb88(%rsp), %rdi
 722b638:      	leaq	0xb98(%rsp), %rsi
 722b640:      	movq	%r15, %rdx
 722b643:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b648:      	movl	0x1e0(%rsp), %eax
 722b64f:      	testl	%eax, %eax
 722b651:      	je	0x722b66e <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x11de>
 722b653:      	movq	0xb88(%rsp), %rdi
 722b65b:      	movl	%eax, %edx
 722b65d:      	movq	0x1d8(%rsp), %rsi
 722b665:      	shlq	$0x3, %rdx
 722b669:      	callq	0x828ace0 <memcpy@plt>
 722b66e:      	movl	%r15d, 0xb90(%rsp)
 722b676:      	leaq	0xb98(%rsp), %r14
 722b67e:      	leaq	0x3e8(%rsp), %rdi
 722b686:      	leaq	0xb88(%rsp), %rsi
 722b68e:      	movq	%r13, %rdx
 722b691:      	callq	0x72325b0 <_ZSt22__uninitialized_copy_aIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEPS6_S6_ET0_T_SD_SC_RSaIT1_E>
 722b696:      	movq	0xb88(%rsp), %rdi
 722b69e:      	cmpq	%r14, %rdi
 722b6a1:      	je	0x722b6a8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1218>
 722b6a3:      	callq	0x828a6d0 <free@plt>
 722b6a8:      	movq	0x3e8(%rsp), %rdi
 722b6b0:      	leaq	0x3f8(%rsp), %rax
 722b6b8:      	cmpq	%rax, %rdi
 722b6bb:      	je	0x722b6c2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1232>
 722b6bd:      	callq	0x828a6d0 <free@plt>
 722b6c2:      	leaq	0x988(%rsp), %rax
 722b6ca:      	movq	%rax, 0x978(%rsp)
 722b6d2:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b6dc:      	movq	%rax, 0x980(%rsp)
 722b6e4:      	movl	0x130(%rsp), %r15d
 722b6ec:      	testq	%r15, %r15
 722b6ef:      	je	0x722b757 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12c7>
 722b6f1:      	leaq	0x988(%rsp), %rdi
 722b6f9:      	movl	%r15d, %eax
 722b6fc:      	cmpl	$0x15, %r15d
 722b700:      	jb	0x722b732 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12a2>
 722b702:      	movl	$0x8, %ecx
 722b707:      	leaq	0x978(%rsp), %rdi
 722b70f:      	leaq	0x988(%rsp), %rsi
 722b717:      	movq	%r15, %rdx
 722b71a:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b71f:      	movl	0x130(%rsp), %eax
 722b726:      	testl	%eax, %eax
 722b728:      	je	0x722b745 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x12b5>
 722b72a:      	movq	0x978(%rsp), %rdi
 722b732:      	movl	%eax, %edx
 722b734:      	movq	0x128(%rsp), %rsi
 722b73c:      	shlq	$0x3, %rdx
 722b740:      	callq	0x828ace0 <memcpy@plt>
 722b745:      	movl	%r15d, 0x980(%rsp)
 722b74d:      	movabsq	$0x1400000000, %rax     # imm = 0x1400000000
 722b757:      	leaq	0xae8(%rsp), %r14
 722b75f:      	movq	%r14, 0xad8(%rsp)
 722b767:      	movq	%rax, 0xae0(%rsp)
 722b76f:      	movl	0x4a0(%rsp), %r15d
 722b777:      	testq	%r15, %r15
 722b77a:      	je	0x722b7db <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x134b>
 722b77c:      	movq	%r14, %rdi
 722b77f:      	movl	%r15d, %eax
 722b782:      	cmpl	$0x15, %r15d
 722b786:      	jb	0x722b7b8 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1328>
 722b788:      	movl	$0x8, %ecx
 722b78d:      	leaq	0xad8(%rsp), %rdi
 722b795:      	leaq	0xae8(%rsp), %rsi
 722b79d:      	movq	%r15, %rdx
 722b7a0:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 722b7a5:      	movl	0x4a0(%rsp), %eax
 722b7ac:      	testl	%eax, %eax
 722b7ae:      	je	0x722b7cb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x133b>
 722b7b0:      	movq	0xad8(%rsp), %rdi
 722b7b8:      	movl	%eax, %edx
 722b7ba:      	movq	0x498(%rsp), %rsi
 722b7c2:      	shlq	$0x3, %rdx
 722b7c6:      	callq	0x828ace0 <memcpy@plt>
 722b7cb:      	movl	%r15d, 0xae0(%rsp)
 722b7d3:      	leaq	0xae8(%rsp), %r14
 722b7db:      	leaq	0x978(%rsp), %rdi
 722b7e3:      	leaq	0xad8(%rsp), %rsi
 722b7eb:      	movq	%r13, %rdx
 722b7ee:      	callq	0x7232260 <_ZSt4copyIN4llvm20ImutAVLValueIteratorINS0_12ImmutableSetIPKN5clang7VarDeclENS0_17ImutContainerInfoIS6_EEEEEEN9__gnu_cxx17__normal_iteratorIPS6_St6vectorIS6_SaIS6_EEEEET0_T_SJ_SI_>
 722b7f3:      	movq	0xad8(%rsp), %rdi
 722b7fb:      	cmpq	%r14, %rdi
 722b7fe:      	je	0x722b805 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1375>
 722b800:      	callq	0x828a6d0 <free@plt>
 722b805:      	movq	0x978(%rsp), %rdi
 722b80d:      	leaq	0x988(%rsp), %rax
 722b815:      	cmpq	%rax, %rdi
 722b818:      	je	0x722b81f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x138f>
 722b81a:      	callq	0x828a6d0 <free@plt>
 722b81f:      	movq	0x498(%rsp), %rdi
 722b827:      	leaq	0x4a8(%rsp), %rax
 722b82f:      	cmpq	%rax, %rdi
 722b832:      	je	0x722b839 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13a9>
 722b834:      	callq	0x828a6d0 <free@plt>
 722b839:      	leaq	(%r13,%rbx,8), %r13
 722b83e:      	leaq	0x138(%rsp), %rax
 722b846:      	leaq	0x1e8(%rsp), %rcx
 722b84e:      	movq	0x1d8(%rsp), %rdi
 722b856:      	cmpq	%rcx, %rdi
 722b859:      	je	0x722b868 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13d8>
 722b85b:      	callq	0x828a6d0 <free@plt>
 722b860:      	leaq	0x138(%rsp), %rax
 722b868:      	movq	0x128(%rsp), %rdi
 722b870:      	cmpq	%rax, %rdi
 722b873:      	je	0x722b87a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x13ea>
 722b875:      	callq	0x828a6d0 <free@plt>
 722b87a:      	movq	0xc38(%rsp), %rdi
 722b882:      	leaq	0xc48(%rsp), %rax
 722b88a:      	cmpq	%rax, %rdi
 722b88d:      	je	0x722b894 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1404>
 722b88f:      	callq	0x828a6d0 <free@plt>
 722b894:      	movq	0x818(%rsp), %rdi
 722b89c:      	leaq	0x828(%rsp), %rax
 722b8a4:      	cmpq	%rax, %rdi
 722b8a7:      	je	0x722b8ae <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x141e>
 722b8a9:      	callq	0x828a6d0 <free@plt>
 722b8ae:      	cmpq	%r13, (%rsp)
 722b8b2:      	je	0x722a8f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722b8b8:      	movq	%r13, %rbx
 722b8bb:      	movq	(%rsp), %r14
 722b8bf:      	subq	%r14, %rbx
 722b8c2:      	movq	%rbx, %rax
 722b8c5:      	sarq	$0x3, %rax
 722b8c9:      	bsrq	%rax, %rdx
 722b8cd:      	xorl	$0x3f, %edx
 722b8d0:      	addl	%edx, %edx
 722b8d2:      	xorq	$0x7e, %rdx
 722b8d6:      	movq	%r14, %rdi
 722b8d9:      	movq	%r13, %rsi
 722b8dc:      	callq	0x7232f60 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN5clang7VarDeclESt6vectorIS5_SaIS5_EEEElNS0_5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117LiveVariablesImpl17dumpBlockLivenessERKNS2_13SourceManagerEE3$_1EEEvT_SK_T0_T1_>
 722b8e1:      	leaq	0x8(%r14), %rcx
 722b8e5:      	cmpq	$0x81, %rbx
 722b8ec:      	movq	%r13, 0x18(%rsp)
 722b8f1:      	jl	0x722b910 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1480>
 722b8f3:      	movl	$0x8, %ebp
 722b8f8:      	movq	%rcx, 0x58(%rsp)
 722b8fd:      	movq	%rcx, 0x48(%rsp)
 722b902:      	movq	%r14, %rax
 722b905:      	movq	%r14, %rbx
 722b908:      	jmp	0x722ba63 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15d3>
 722b90d:      	nopl	(%rax)
 722b910:      	movq	%r14, %rbx
 722b913:      	cmpq	%r13, %rcx
 722b916:      	je	0x722bbca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722b91c:      	movq	(%rsp), %r12
 722b920:      	jmp	0x722b981 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14f1>
 722b922:      	nopw	%cs:(%rax,%rax)
 722b92c:      	nopl	(%rax)
 722b930:      	subq	%r13, %rbx
 722b933:      	movq	%rbx, %rax
 722b936:      	sarq	$0x3, %rax
 722b93a:      	cmpq	$0x2, %rax
 722b93e:      	jl	0x722ba09 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1579>
 722b944:      	shlq	$0x3, %rax
 722b948:      	subq	%rax, %r12
 722b94b:      	addq	$0x10, %r12
 722b94f:      	movq	%r12, %rdi
 722b952:      	movq	%r13, %rsi
 722b955:      	movq	%rbx, %rdx
 722b958:      	callq	0x828ac50 <memmove@plt>
 722b95d:      	movq	0x18(%rsp), %rbp
 722b962:      	movq	%r15, (%r13)
 722b966:      	movq	0x8(%rsp), %r12
 722b96b:      	leaq	0x8(%r12), %rcx
 722b970:      	cmpq	%rbp, %rcx
 722b973:      	leaq	0x88(%rsp), %rbp
 722b97b:      	je	0x722bba0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1710>
 722b981:      	movq	%rcx, %rbx
 722b984:      	movq	(%rcx), %r15
 722b987:      	movq	(%rsp), %r13
 722b98b:      	movq	(%r13), %rbp
 722b98f:      	movq	(%r15), %r14
 722b992:      	movq	%r15, %rdi
 722b995:      	callq	*0x10(%r14)
 722b999:      	movq	(%rbp), %rcx
 722b99d:      	movq	%rbp, 0x30(%rsp)
 722b9a2:      	movq	%rbp, %rdi
 722b9a5:      	movq	%rax, %rbp
 722b9a8:      	callq	*0x10(%rcx)
 722b9ab:      	cmpl	%eax, %ebp
 722b9ad:      	movq	%rbx, 0x8(%rsp)
 722b9b2:      	jb	0x722b930 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14a0>
 722b9b8:      	movq	(%r12), %r12
 722b9bc:      	movq	(%r12), %rax
 722b9c0:      	movq	%r12, %rdi
 722b9c3:      	callq	*0x10(%rax)
 722b9c6:      	movq	%rbx, %r13
 722b9c9:      	cmpl	%eax, %ebp
 722b9cb:      	movq	0x18(%rsp), %rbp
 722b9d0:      	jae	0x722b962 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722b9d2:      	movq	0x8(%rsp), %r13
 722b9d7:      	nopw	(%rax,%rax)
 722b9e0:      	movq	%r12, (%r13)
 722b9e4:      	movq	-0x10(%r13), %r12
 722b9e8:      	movq	%r15, %rdi
 722b9eb:      	callq	*0x10(%r14)
 722b9ef:      	movq	%rax, %rbx
 722b9f2:      	movq	(%r12), %rax
 722b9f6:      	movq	%r12, %rdi
 722b9f9:      	callq	*0x10(%rax)
 722b9fc:      	addq	$-0x8, %r13
 722ba00:      	cmpl	%eax, %ebx
 722ba02:      	jb	0x722b9e0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1550>
 722ba04:      	jmp	0x722b962 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722ba09:      	cmpq	$0x8, %rbx
 722ba0d:      	movq	0x18(%rsp), %rbp
 722ba12:      	jne	0x722b962 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722ba18:      	movq	0x30(%rsp), %rax
 722ba1d:      	movq	%rax, 0x8(%r12)
 722ba22:      	movq	(%rsp), %r13
 722ba26:      	jmp	0x722b962 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x14d2>
 722ba2b:      	movq	%r13, 0x8(%rax)
 722ba2f:      	movq	(%rsp), %r14
 722ba33:      	nopw	%cs:(%rax,%rax)
 722ba3d:      	nopl	(%rax)
 722ba40:      	movq	%r12, (%r14)
 722ba43:      	addq	$0x8, %rbp
 722ba47:      	addq	$0x8, 0x48(%rsp)
 722ba4d:      	cmpq	$0x80, %rbp
 722ba54:      	movq	(%rsp), %rbx
 722ba58:      	movq	0x8(%rsp), %rax
 722ba5d:      	je	0x722bb10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1680>
 722ba63:      	movq	%rax, 0x30(%rsp)
 722ba68:      	leaq	(%rbx,%rbp), %r14
 722ba6c:      	movq	(%rbx,%rbp), %r12
 722ba70:      	movq	(%rbx), %r13
 722ba73:      	movq	(%r12), %r15
 722ba77:      	movq	%r12, %rdi
 722ba7a:      	callq	*0x10(%r15)
 722ba7e:      	movq	%rax, %rbx
 722ba81:      	movq	(%r13), %rax
 722ba85:      	movq	%r13, %rdi
 722ba88:      	callq	*0x10(%rax)
 722ba8b:      	cmpl	%eax, %ebx
 722ba8d:      	movq	%r14, 0x8(%rsp)
 722ba92:      	jae	0x722bac0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1630>
 722ba94:      	movq	0x30(%rsp), %rax
 722ba99:      	cmpq	$0x9, %rbp
 722ba9d:      	jb	0x722ba2b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x159b>
 722ba9f:      	movq	0x58(%rsp), %rdi
 722baa4:      	movq	(%rsp), %r14
 722baa8:      	movq	%r14, %rsi
 722baab:      	movq	%rbp, %rdx
 722baae:      	callq	0x828ac50 <memmove@plt>
 722bab3:      	jmp	0x722ba40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722bab5:      	nopw	%cs:(%rax,%rax)
 722babf:      	nop
 722bac0:      	movq	0x30(%rsp), %rax
 722bac5:      	movq	(%rax), %r13
 722bac8:      	movq	(%r13), %rax
 722bacc:      	movq	%r13, %rdi
 722bacf:      	callq	*0x10(%rax)
 722bad2:      	cmpl	%eax, %ebx
 722bad4:      	jae	0x722ba40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722bada:      	movq	0x48(%rsp), %r14
 722badf:      	nop
 722bae0:      	movq	%r13, (%r14)
 722bae3:      	movq	-0x10(%r14), %r13
 722bae7:      	movq	%r12, %rdi
 722baea:      	callq	*0x10(%r15)
 722baee:      	movq	%rax, %rbx
 722baf1:      	movq	(%r13), %rax
 722baf5:      	movq	%r13, %rdi
 722baf8:      	callq	*0x10(%rax)
 722bafb:      	addq	$-0x8, %r14
 722baff:      	cmpl	%eax, %ebx
 722bb01:      	jb	0x722bae0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1650>
 722bb03:      	jmp	0x722ba40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x15b0>
 722bb08:      	nopl	(%rax,%rax)
 722bb10:      	leaq	0x80(%rbx), %r14
 722bb17:      	cmpq	0x18(%rsp), %r14
 722bb1c:      	leaq	0x88(%rsp), %rbp
 722bb24:      	jne	0x722bb47 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16b7>
 722bb26:      	jmp	0x722bbca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722bb2b:      	nopl	(%rax,%rax)
 722bb30:      	movq	%r15, (%rbp)
 722bb34:      	addq	$0x8, %r14
 722bb38:      	cmpq	0x18(%rsp), %r14
 722bb3d:      	leaq	0x88(%rsp), %rbp
 722bb45:      	je	0x722bba0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1710>
 722bb47:      	movq	-0x8(%r14), %r12
 722bb4b:      	movq	(%r14), %r15
 722bb4e:      	movq	(%r15), %r13
 722bb51:      	movq	%r15, %rdi
 722bb54:      	callq	*0x10(%r13)
 722bb58:      	movq	%rax, %rbx
 722bb5b:      	movq	(%r12), %rax
 722bb5f:      	movq	%r12, %rdi
 722bb62:      	callq	*0x10(%rax)
 722bb65:      	movq	%r14, %rbp
 722bb68:      	cmpl	%eax, %ebx
 722bb6a:      	jae	0x722bb30 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16a0>
 722bb6c:      	movq	%r14, %rbp
 722bb6f:      	nop
 722bb70:      	movq	%r12, (%rbp)
 722bb74:      	movq	-0x10(%rbp), %r12
 722bb78:      	movq	%r15, %rdi
 722bb7b:      	callq	*0x10(%r13)
 722bb7f:      	movq	%rax, %rbx
 722bb82:      	movq	(%r12), %rax
 722bb86:      	movq	%r12, %rdi
 722bb89:      	callq	*0x10(%rax)
 722bb8c:      	addq	$-0x8, %rbp
 722bb90:      	cmpl	%eax, %ebx
 722bb92:      	jb	0x722bb70 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16e0>
 722bb94:      	jmp	0x722bb30 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x16a0>
 722bb96:      	nopw	%cs:(%rax,%rax)
 722bba0:      	movq	(%rsp), %rbx
 722bba4:      	jmp	0x722bbca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722bba6:      	nopw	%cs:(%rax,%rax)
 722bbb0:      	movw	$0xa3e, (%rax)          # imm = 0xA3E
 722bbb5:      	addq	$0x2, 0x13976eb(%rip)   # 0x85c32a8 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x20>
 722bbbd:      	addq	$0x8, %rbx
 722bbc1:      	cmpq	%r13, %rbx
 722bbc4:      	je	0x722a8f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722bbca:      	movq	(%rbx), %r12
 722bbcd:      	movzbl	0x13976ac(%rip), %eax   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bbd4:      	testb	%al, %al
 722bbd6:      	je	0x722bf1b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a8b>
 722bbdc:      	movzbl	0x1397705(%rip), %eax   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bbe3:      	testb	%al, %al
 722bbe5:      	je	0x722bf40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1ab0>
 722bbeb:      	movq	0x13976b6(%rip), %rax   # 0x85c32a8 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x20>
 722bbf2:      	cmpq	%rax, 0x13976a7(%rip)   # 0x85c32a0 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x18>
 722bbf9:      	je	0x722bc10 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1780>
 722bbfb:      	movb	$0x20, (%rax)
 722bbfe:      	incq	0x13976a3(%rip)         # 0x85c32a8 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x20>
 722bc05:      	leaq	0x139767c(%rip), %r15   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bc0c:      	jmp	0x722bc2b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x179b>
 722bc0e:      	nop
 722bc10:      	movl	$0x1, %edx
 722bc15:      	leaq	0x139766c(%rip), %rdi   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bc1c:      	leaq	-0x65d7756(%rip), %rsi  # 0xc544cd <.str.llvm.5983392213627075592>
 722bc23:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722bc28:      	movq	%rax, %r15
 722bc2b:      	movq	%r12, 0x8(%rsp)
 722bc30:      	movq	0x28(%r12), %rax
 722bc35:      	movq	%rbp, 0x78(%rsp)
 722bc3a:      	movq	$0x0, 0x80(%rsp)
 722bc46:      	movb	$0x0, 0x88(%rsp)
 722bc4e:      	movl	$0x0, 0x290(%rsp)
 722bc59:      	movb	$0x0, 0x2b0(%rsp)
 722bc61:      	movq	0x68(%rsp), %rcx
 722bc66:      	movq	%rcx, 0x288(%rsp)
 722bc6e:      	leaq	0x78(%rsp), %rcx
 722bc73:      	movq	%rcx, 0x2b8(%rsp)
 722bc7b:      	movl	$0x0, 0x2b4(%rsp)
 722bc86:      	leaq	0x298(%rsp), %rcx
 722bc8e:      	xorps	%xmm0, %xmm0
 722bc91:      	movups	%xmm0, (%rcx)
 722bc94:      	movq	$0x0, 0x10(%rcx)
 722bc9c:      	movq	%rax, 0x3e8(%rsp)
 722bca4:      	leaq	0x498(%rsp), %r13
 722bcac:      	movq	%r13, %rdi
 722bcaf:      	callq	0x4608510 <_ZN5clang11LangOptionsC2Ev>
 722bcb4:      	movq	0x498(%rsp), %rsi
 722bcbc:      	movl	%esi, %edx
 722bcbe:      	shrl	$0x2, %edx
 722bcc1:      	andl	$0x200, %edx            # imm = 0x200
 722bcc7:      	movl	%esi, %eax
 722bcc9:      	shrl	$0x3, %eax
 722bccc:      	andl	$0x800000, %eax         # imm = 0x800000
 722bcd1:      	movl	%esi, %ecx
 722bcd3:      	andl	$0x8, %ecx
 722bcd6:      	shll	$0x15, %ecx
 722bcd9:      	testl	$0x1000, %esi           # imm = 0x1000
 722bcdf:      	movl	$0x1000000, %edi        # imm = 0x1000000
 722bce4:      	cmovneq	%rdi, %rcx
 722bce8:      	movl	%esi, %r8d
 722bceb:      	shll	$0xe, %r8d
 722bcef:      	andl	$0x2000000, %r8d        # imm = 0x2000000
 722bcf6:      	movl	%esi, %r9d
 722bcf9:      	andl	$0x1, %r9d
 722bcfd:      	shll	$0x1a, %r9d
 722bd01:      	movl	%esi, %r10d
 722bd04:      	shll	$0xf, %r10d
 722bd08:      	andl	$0x8000000, %r10d       # imm = 0x8000000
 722bd0f:      	movl	%esi, %r11d
 722bd12:      	andl	$0x2, %r11d
 722bd16:      	shll	$0x1b, %r11d
 722bd1a:      	movl	%esi, %ebp
 722bd1c:      	shll	$0x12, %ebp
 722bd1f:      	andl	$0x60000000, %ebp       # imm = 0x60000000
 722bd25:      	movq	%rsi, %rdi
 722bd28:      	shlq	$0x6, %rdi
 722bd2c:      	movq	%rdi, %r14
 722bd2f:      	movabsq	$0x200000000, %r12      # imm = 0x200000000
 722bd39:      	andq	%r12, %r14
 722bd3c:      	movabsq	$0x400000000, %r12      # imm = 0x400000000
 722bd46:      	andq	%r12, %rdi
 722bd49:      	movabsq	$0x660c00000000, %r12   # imm = 0x660C00000000
 722bd53:      	xorq	%r12, %rdi
 722bd56:      	testb	%sil, %sil
 722bd59:      	movabsq	$0x660800000000, %rsi   # imm = 0x660800000000
 722bd63:      	cmovnsq	%rsi, %rdi
 722bd67:      	orl	%edx, %eax
 722bd69:      	orl	%r8d, %eax
 722bd6c:      	orl	%r9d, %eax
 722bd6f:      	orl	%r10d, %eax
 722bd72:      	orl	%r11d, %eax
 722bd75:      	orl	%ebp, %eax
 722bd77:      	orq	%r14, %rax
 722bd7a:      	orq	%rcx, %rax
 722bd7d:      	movq	0x4f0(%rsp), %rcx
 722bd85:      	andl	$0x100, %ecx            # imm = 0x100
 722bd8b:      	shlq	$0x27, %rcx
 722bd8f:      	orq	%rcx, %rax
 722bd92:      	orq	%rdi, %rax
 722bd95:      	xorq	$0x60444002, %rax       # imm = 0x60444002
 722bd9b:      	movq	%rax, 0x338(%rsp)
 722bda3:      	movq	$0x0, 0x340(%rsp)
 722bdaf:      	leaq	0x3e8(%rsp), %rdi
 722bdb7:      	leaq	0x288(%rsp), %rsi
 722bdbf:      	leaq	0x338(%rsp), %rdx
 722bdc7:      	callq	0x7555570 <_ZNK5clang15DeclarationName5printERN4llvm11raw_ostreamERKNS_14PrintingPolicyE>
 722bdcc:      	movq	%r13, %rdi
 722bdcf:      	callq	0x4374820 <_ZN5clang11LangOptionsD2Ev>
 722bdd4:      	movq	0x60(%rsp), %rax
 722bdd9:      	movq	%rax, 0x288(%rsp)
 722bde1:      	cmpl	$0x1, 0x2b4(%rsp)
 722bde9:      	jne	0x722bdfd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x196d>
 722bdeb:      	movq	0x298(%rsp), %rdi
 722bdf3:      	testq	%rdi, %rdi
 722bdf6:      	je	0x722bdfd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x196d>
 722bdf8:      	callq	0x828a840 <_ZdaPv@plt>
 722bdfd:      	movq	0x78(%rsp), %rsi
 722be02:      	movq	0x80(%rsp), %rdx
 722be0a:      	movq	%r15, %rdi
 722be0d:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722be12:      	movq	0x18(%rax), %rdx
 722be16:      	movq	0x20(%rax), %rcx
 722be1a:      	subq	%rcx, %rdx
 722be1d:      	cmpq	$0x1, %rdx
 722be21:      	ja	0x722be40 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19b0>
 722be23:      	movl	$0x2, %edx
 722be28:      	movq	%rax, %rdi
 722be2b:      	leaq	-0x6526c27(%rip), %rsi  # 0xd0520b <.str.564.llvm.14097904587116808248>
 722be32:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722be37:      	jmp	0x722be4a <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19ba>
 722be39:      	nopl	(%rax)
 722be40:      	movw	$0x3c20, (%rcx)         # imm = 0x3C20
 722be45:      	addq	$0x2, 0x20(%rax)
 722be4a:      	movq	0x18(%rsp), %r13
 722be4f:      	leaq	0x88(%rsp), %rbp
 722be57:      	movq	0x8(%rsp), %r14
 722be5c:      	movq	0x78(%rsp), %rdi
 722be61:      	cmpq	%rbp, %rdi
 722be64:      	je	0x722be76 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x19e6>
 722be66:      	movq	0x88(%rsp), %rsi
 722be6e:      	incq	%rsi
 722be71:      	callq	0x828a6f0 <_ZdlPvm@plt>
 722be76:      	movl	0x18(%r14), %eax
 722be7a:      	movl	%eax, 0x498(%rsp)
 722be81:      	movzbl	0x13973f8(%rip), %eax   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722be88:      	testb	%al, %al
 722be8a:      	je	0x722bf99 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b09>
 722be90:      	movzbl	0x1397451(%rip), %eax   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722be97:      	testb	%al, %al
 722be99:      	je	0x722bfbe <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b2e>
 722be9f:      	leaq	0x498(%rsp), %rdi
 722bea7:      	leaq	0x13973da(%rip), %rsi   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722beae:      	movq	0x70(%rsp), %rdx
 722beb3:      	callq	0x437b4b0 <_ZNK5clang14SourceLocation5printERN4llvm11raw_ostreamERKNS_13SourceManagerE>
 722beb8:      	movzbl	0x13973c1(%rip), %eax   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bebf:      	testb	%al, %al
 722bec1:      	je	0x722c017 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1b87>
 722bec7:      	movzbl	0x139741a(%rip), %eax   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bece:      	testb	%al, %al
 722bed0:      	je	0x722c03c <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1bac>
 722bed6:      	movq	0x13973c3(%rip), %rcx   # 0x85c32a0 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x18>
 722bedd:      	movq	0x13973c4(%rip), %rax   # 0x85c32a8 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287+0x20>
 722bee4:      	subq	%rax, %rcx
 722bee7:      	cmpq	$0x1, %rcx
 722beeb:      	ja	0x722bbb0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1720>
 722bef1:      	movl	$0x2, %edx
 722bef6:      	leaq	0x139738b(%rip), %rdi   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722befd:      	leaq	-0x6498e2c(%rip), %rsi  # 0xd930d8 <.L.str.965>
 722bf04:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 722bf09:      	addq	$0x8, %rbx
 722bf0d:      	cmpq	%r13, %rbx
 722bf10:      	jne	0x722bbca <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x173a>
 722bf16:      	jmp	0x722a8f0 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x460>
 722bf1b:      	leaq	0x139735e(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bf22:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722bf27:      	testl	%eax, %eax
 722bf29:      	je	0x722bbdc <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x174c>
 722bf2f:      	leaq	0x139734a(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bf36:      	callq	0x828a890 <__cxa_guard_release@plt>
 722bf3b:      	jmp	0x722bbdc <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x174c>
 722bf40:      	leaq	0x13973a1(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bf47:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722bf4c:      	testl	%eax, %eax
 722bf4e:      	je	0x722bbeb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x175b>
 722bf54:      	leaq	0x139732d(%rip), %r14   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bf5b:      	movq	%r14, %rdi
 722bf5e:      	movl	$0x2, %esi
 722bf63:      	xorl	%edx, %edx
 722bf65:      	movl	$0x1, %ecx
 722bf6a:      	xorl	%r8d, %r8d
 722bf6d:      	callq	0x4145ba0 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722bf72:      	leaq	-0x30e5269(%rip), %rdi  # 0x4146d10 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722bf79:      	movq	%r14, %rsi
 722bf7c:      	leaq	0x133f325(%rip), %rdx   # 0x856b2a8 <__dso_handle>
 722bf83:      	callq	0x828a760 <__cxa_atexit@plt>
 722bf88:      	leaq	0x1397359(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bf8f:      	callq	0x828a890 <__cxa_guard_release@plt>
 722bf94:      	jmp	0x722bbeb <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x175b>
 722bf99:      	leaq	0x13972e0(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bfa0:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722bfa5:      	testl	%eax, %eax
 722bfa7:      	je	0x722be90 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a00>
 722bfad:      	leaq	0x13972cc(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722bfb4:      	callq	0x828a890 <__cxa_guard_release@plt>
 722bfb9:      	jmp	0x722be90 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a00>
 722bfbe:      	leaq	0x1397323(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bfc5:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722bfca:      	testl	%eax, %eax
 722bfcc:      	je	0x722be9f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0f>
 722bfd2:      	leaq	0x13972af(%rip), %r14   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722bfd9:      	movq	%r14, %rdi
 722bfdc:      	movl	$0x2, %esi
 722bfe1:      	xorl	%edx, %edx
 722bfe3:      	movl	$0x1, %ecx
 722bfe8:      	xorl	%r8d, %r8d
 722bfeb:      	callq	0x4145ba0 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722bff0:      	leaq	-0x30e52e7(%rip), %rdi  # 0x4146d10 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722bff7:      	movq	%r14, %rsi
 722bffa:      	leaq	0x133f2a7(%rip), %rdx   # 0x856b2a8 <__dso_handle>
 722c001:      	callq	0x828a760 <__cxa_atexit@plt>
 722c006:      	leaq	0x13972db(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722c00d:      	callq	0x828a890 <__cxa_guard_release@plt>
 722c012:      	jmp	0x722be9f <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a0f>
 722c017:      	leaq	0x1397262(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722c01e:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722c023:      	testl	%eax, %eax
 722c025:      	je	0x722bec7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a37>
 722c02b:      	leaq	0x139724e(%rip), %rdi   # 0x85c3280 <_ZGVZN4llvm4errsEvE2EC.llvm.8189526126256621287>
 722c032:      	callq	0x828a890 <__cxa_guard_release@plt>
 722c037:      	jmp	0x722bec7 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a37>
 722c03c:      	leaq	0x13972a5(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722c043:      	callq	0x828a880 <__cxa_guard_acquire@plt>
 722c048:      	testl	%eax, %eax
 722c04a:      	je	0x722bed6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a46>
 722c050:      	leaq	0x1397231(%rip), %r14   # 0x85c3288 <_ZZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722c057:      	movq	%r14, %rdi
 722c05a:      	movl	$0x2, %esi
 722c05f:      	xorl	%edx, %edx
 722c061:      	movl	$0x1, %ecx
 722c066:      	xorl	%r8d, %r8d
 722c069:      	callq	0x4145ba0 <_ZN4llvm14raw_fd_ostreamC2EibbNS_11raw_ostream11OStreamKindE>
 722c06e:      	leaq	-0x30e5365(%rip), %rdi  # 0x4146d10 <_ZN4llvm14raw_fd_ostreamD2Ev>
 722c075:      	movq	%r14, %rsi
 722c078:      	leaq	0x133f229(%rip), %rdx   # 0x856b2a8 <__dso_handle>
 722c07f:      	callq	0x828a760 <__cxa_atexit@plt>
 722c084:      	leaq	0x139725d(%rip), %rdi   # 0x85c32e8 <_ZGVZN4llvm4errsEvE1S.llvm.8189526126256621287>
 722c08b:      	callq	0x828a890 <__cxa_guard_release@plt>
 722c090:      	jmp	0x722bed6 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1a46>
 722c095:      	movq	0x10(%rsp), %rbx
 722c09a:      	movq	(%rsp), %r14
 722c09e:      	callq	0x4146170 <_ZN4llvm4errsEv>
 722c0a3:      	movq	0x20(%rax), %rcx
 722c0a7:      	cmpq	%rcx, 0x18(%rax)
 722c0ab:      	je	0x722a79b <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x30b>
 722c0b1:      	movb	$0xa, (%rcx)
 722c0b4:      	incq	0x20(%rax)
 722c0b8:      	testq	%r14, %r14
 722c0bb:      	je	0x722c0cd <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c3d>
 722c0bd:      	movq	0x20(%rsp), %rsi
 722c0c2:      	subq	%r14, %rsi
 722c0c5:      	movq	%r14, %rdi
 722c0c8:      	callq	0x828a6f0 <_ZdlPvm@plt>
 722c0cd:      	testq	%rbx, %rbx
 722c0d0:      	je	0x722c0e2 <_ZN5clang13LiveVariables17dumpBlockLivenessERKNS_13SourceManagerE+0x1c52>
 722c0d2:      	movq	0x38(%rsp), %rsi
 722c0d7:      	subq	%rbx, %rsi
 722c0da:      	movq	%rbx, %rdi
 722c0dd:      	callq	0x828a6f0 <_ZdlPvm@plt>
 722c0e2:      	addq	$0xce8, %rsp            # imm = 0xCE8
 722c0e9:      	popq	%rbx
 722c0ea:      	popq	%r12
 722c0ec:      	popq	%r13
 722c0ee:      	popq	%r14
 722c0f0:      	popq	%r15
 722c0f2:      	popq	%rbp
 722c0f3:      	retq
 722c0f4:      	leaq	-0x65d810c(%rip), %rdi  # 0xc53fef <.L.str.979>
 722c0fb:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
