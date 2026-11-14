
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007d2f400 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE>:
 7d2f400:      	pushq	%rbp
 7d2f401:      	pushq	%r15
 7d2f403:      	pushq	%r14
 7d2f405:      	pushq	%r13
 7d2f407:      	pushq	%r12
 7d2f409:      	pushq	%rbx
 7d2f40a:      	subq	$0x58, %rsp
 7d2f40e:      	movq	%rdi, 0x28(%rsp)
 7d2f413:      	movq	%rsi, 0x30(%rsp)
 7d2f418:      	movl	0x48(%rsi), %eax
 7d2f41b:      	movq	%rax, 0x18(%rsp)
 7d2f420:      	cmpq	$0x2, %rax
 7d2f424:      	jae	0x7d2f435 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x35>
 7d2f426:      	addq	$0x58, %rsp
 7d2f42a:      	popq	%rbx
 7d2f42b:      	popq	%r12
 7d2f42d:      	popq	%r13
 7d2f42f:      	popq	%r14
 7d2f431:      	popq	%r15
 7d2f433:      	popq	%rbp
 7d2f434:      	retq
 7d2f435:      	movq	0x30(%rsp), %rax
 7d2f43a:      	movq	0x40(%rax), %rax
 7d2f43e:      	movq	0x18(%rsp), %rcx
 7d2f443:      	shlq	$0x2, %rcx
 7d2f447:      	movq	%rax, 0x38(%rsp)
 7d2f44c:      	movl	(%rax), %eax
 7d2f44e:      	xorl	%edx, %edx
 7d2f450:      	movq	0x38(%rsp), %rsi
 7d2f455:      	nopw	%cs:(%rax,%rax)
 7d2f45f:      	nop
 7d2f460:      	cmpl	%eax, (%rsi,%rdx)
 7d2f463:      	jne	0x7d2f426 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f465:      	addq	$0x4, %rdx
 7d2f469:      	cmpq	%rdx, %rcx
 7d2f46c:      	jne	0x7d2f460 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x60>
 7d2f46e:      	movq	0x28(%rsp), %rcx
 7d2f473:      	movq	0x8c8(%rcx), %rcx
 7d2f47a:      	xorl	%edx, %edx
 7d2f47c:      	cmpb	$0x0, 0xdc(%rcx)
 7d2f483:      	sete	%cl
 7d2f486:      	testl	%eax, %eax
 7d2f488:      	je	0x7d2f426 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f48a:      	movb	%cl, %dl
 7d2f48c:      	movl	%edx, 0xc(%rsp)
 7d2f490:      	movq	0x30(%rsp), %rax
 7d2f495:      	movq	(%rax), %r14
 7d2f498:      	movq	0x28(%rsp), %rcx
 7d2f49d:      	movq	(%rcx), %rbx
 7d2f4a0:      	movl	0x80(%rax), %eax
 7d2f4a6:      	movl	%eax, 0x4(%rsp)
 7d2f4aa:      	xorl	%ebp, %ebp
 7d2f4ac:      	movl	$0x1, %r15d
 7d2f4b2:      	movq	%r14, 0x10(%rsp)
 7d2f4b7:      	movl	$0x0, 0x8(%rsp)
 7d2f4bf:      	jmp	0x7d2f4f0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xf0>
 7d2f4c1:      	nopw	%cs:(%rax,%rax)
 7d2f4cb:      	nopl	(%rax,%rax)
 7d2f4d0:      	movl	0x8(%rsp), %ecx
 7d2f4d4:      	incl	%ecx
 7d2f4d6:      	movq	0x20(%rsp), %r14
 7d2f4db:      	addq	$0x18, %r14
 7d2f4df:      	movq	0x38(%rsp), %rax
 7d2f4e4:      	movl	%ecx, 0x8(%rsp)
 7d2f4e8:      	cmpl	(%rax), %ecx
 7d2f4ea:      	jae	0x7d2f426 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f4f0:      	cmpb	$0x0, 0xc(%r14)
 7d2f4f5:      	jne	0x7d2f513 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x113>
 7d2f4f7:      	movq	%r14, %rax
 7d2f4fa:      	nopw	(%rax,%rax)
 7d2f500:      	movq	0x10(%rax), %rax
 7d2f504:      	testq	%rax, %rax
 7d2f507:      	je	0x7d2f600 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x200>
 7d2f50d:      	cmpb	$0x1, 0xc(%rax)
 7d2f511:      	jne	0x7d2f500 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x100>
 7d2f513:      	movl	0x4(%rsp), %eax
 7d2f517:      	cmpq	%r14, 0x10(%rsp)
 7d2f51c:      	je	0x7d2f602 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x202>
 7d2f522:      	movq	0x10(%rsp), %rcx
 7d2f527:      	movl	0x4(%rsp), %eax
 7d2f52b:      	jmp	0x7d2f565 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x165>
 7d2f52d:      	nopl	(%rax)
 7d2f530:      	movq	%rdi, %r8
 7d2f533:      	shlq	$0x7, %r8
 7d2f537:      	leaq	(%r8,%rdi,8), %rdi
 7d2f53b:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f540:      	cmovnel	%ebp, %esi
 7d2f543:      	addl	0x6c(%rbx,%rdi), %esi
 7d2f547:      	addl	0x64(%rbx,%rdi), %esi
 7d2f54b:      	incl	%eax
 7d2f54d:      	cmpl	$0x0, 0x1c(%rbx,%rdx)
 7d2f552:      	cmovnel	%r15d, %eax
 7d2f556:      	addl	%esi, %eax
 7d2f558:      	addq	$0x18, %rcx
 7d2f55c:      	cmpq	%r14, %rcx
 7d2f55f:      	je	0x7d2f602 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x202>
 7d2f565:      	movl	(%rcx), %edi
 7d2f567:      	movl	0x8(%rcx), %r8d
 7d2f56b:      	movq	%rdi, %rdx
 7d2f56e:      	shlq	$0x7, %rdx
 7d2f572:      	leaq	(%rdx,%rdi,8), %rdx
 7d2f576:      	xorl	%esi, %esi
 7d2f578:      	cmpl	%r8d, %edi
 7d2f57b:      	jae	0x7d2f54b <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x14b>
 7d2f57d:      	leaq	-0x1(%r8), %r9
 7d2f581:      	xorl	%esi, %esi
 7d2f583:      	cmpq	%rdi, %r9
 7d2f586:      	je	0x7d2f530 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x130>
 7d2f588:      	subq	%rdi, %r8
 7d2f58b:      	leaq	0xf4(%rbx), %rsi
 7d2f592:      	leaq	(%rsi,%rdx), %r10
 7d2f596:      	movq	%r8, %r11
 7d2f599:      	andq	$-0x2, %r11
 7d2f59d:      	negq	%r11
 7d2f5a0:      	xorl	%esi, %esi
 7d2f5a2:      	xorl	%r9d, %r9d
 7d2f5a5:      	nopw	%cs:(%rax,%rax)
 7d2f5af:      	nop
 7d2f5b0:      	cmpl	$0x0, -0xd8(%r10)
 7d2f5b8:      	cmovnel	%ebp, %esi
 7d2f5bb:      	addl	-0x88(%r10), %esi
 7d2f5c2:      	addl	-0x90(%r10), %esi
 7d2f5c9:      	cmpl	$0x0, -0x50(%r10)
 7d2f5ce:      	cmovnel	%ebp, %esi
 7d2f5d1:      	addl	(%r10), %esi
 7d2f5d4:      	addl	-0x8(%r10), %esi
 7d2f5d8:      	addq	$0x110, %r10            # imm = 0x110
 7d2f5df:      	addq	$-0x2, %r9
 7d2f5e3:      	cmpq	%r9, %r11
 7d2f5e6:      	jne	0x7d2f5b0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x1b0>
 7d2f5e8:      	testb	$0x1, %r8b
 7d2f5ec:      	je	0x7d2f54b <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x14b>
 7d2f5f2:      	subq	%r9, %rdi
 7d2f5f5:      	jmp	0x7d2f530 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x130>
 7d2f5fa:      	nopw	(%rax,%rax)
 7d2f600:      	xorl	%eax, %eax
 7d2f602:      	movl	(%r14), %edx
 7d2f605:      	movl	0x8(%r14), %ecx
 7d2f609:      	xorl	%r8d, %r8d
 7d2f60c:      	cmpl	%edx, %ecx
 7d2f60e:      	jbe	0x7d2f6b2 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2b2>
 7d2f614:      	leaq	-0x1(%rcx), %rdi
 7d2f618:      	xorl	%r8d, %r8d
 7d2f61b:      	movq	%rdx, %rsi
 7d2f61e:      	cmpq	%rdx, %rdi
 7d2f621:      	je	0x7d2f694 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x294>
 7d2f623:      	movq	%rcx, %rsi
 7d2f626:      	subq	%rdx, %rsi
 7d2f629:      	movq	%rdx, %rdi
 7d2f62c:      	shlq	$0x7, %rdi
 7d2f630:      	leaq	(%rdi,%rdx,8), %rdi
 7d2f634:      	leaq	0xf4(%rbx), %r8
 7d2f63b:      	addq	%r8, %rdi
 7d2f63e:      	movq	%rsi, %r10
 7d2f641:      	andq	$-0x2, %r10
 7d2f645:      	negq	%r10
 7d2f648:      	xorl	%r8d, %r8d
 7d2f64b:      	xorl	%r9d, %r9d
 7d2f64e:      	nop
 7d2f650:      	cmpl	$0x0, -0xd8(%rdi)
 7d2f657:      	cmovnel	%ebp, %r8d
 7d2f65b:      	addl	-0x88(%rdi), %r8d
 7d2f662:      	addl	-0x90(%rdi), %r8d
 7d2f669:      	cmpl	$0x0, -0x50(%rdi)
 7d2f66d:      	cmovnel	%ebp, %r8d
 7d2f671:      	addl	(%rdi), %r8d
 7d2f674:      	addl	-0x8(%rdi), %r8d
 7d2f678:      	addq	$0x110, %rdi            # imm = 0x110
 7d2f67f:      	addq	$-0x2, %r9
 7d2f683:      	cmpq	%r9, %r10
 7d2f686:      	jne	0x7d2f650 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x250>
 7d2f688:      	testb	$0x1, %sil
 7d2f68c:      	je	0x7d2f6b2 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2b2>
 7d2f68e:      	movq	%rdx, %rsi
 7d2f691:      	subq	%r9, %rsi
 7d2f694:      	movq	%rsi, %rdi
 7d2f697:      	shlq	$0x7, %rdi
 7d2f69b:      	leaq	(%rdi,%rsi,8), %rsi
 7d2f69f:      	cmpl	$0x0, 0x1c(%rbx,%rsi)
 7d2f6a4:      	cmovnel	%ebp, %r8d
 7d2f6a8:      	addl	0x6c(%rbx,%rsi), %r8d
 7d2f6ad:      	addl	0x64(%rbx,%rsi), %r8d
 7d2f6b2:      	movq	%rdx, %rsi
 7d2f6b5:      	shlq	$0x7, %rsi
 7d2f6b9:      	leaq	(%rsi,%rdx,8), %r13
 7d2f6bd:      	movl	0x1c(%rbx,%r13), %esi
 7d2f6c2:      	movl	%esi, 0x40(%rsp)
 7d2f6c6:      	testl	%esi, %esi
 7d2f6c8:      	movl	$0x0, %esi
 7d2f6cd:      	cmovel	%eax, %esi
 7d2f6d0:      	addl	%r8d, %esi
 7d2f6d3:      	movq	%r14, 0x20(%rsp)
 7d2f6d8:      	movq	0x10(%r14), %r14
 7d2f6dc:      	testq	%r14, %r14
 7d2f6df:      	je	0x7d2f7e0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x3e0>
 7d2f6e5:      	movq	%r14, %r8
 7d2f6e8:      	jmp	0x7d2f741 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x341>
 7d2f6ea:      	nopw	(%rax,%rax)
 7d2f6f0:      	movq	%r15, %rdi
 7d2f6f3:      	shlq	$0x7, %rdi
 7d2f6f7:      	leaq	(%rdi,%r15,8), %rdi
 7d2f6fb:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f700:      	cmovnel	%ebp, %r11d
 7d2f704:      	addl	0x6c(%rbx,%rdi), %r11d
 7d2f709:      	addl	0x64(%rbx,%rdi), %r11d
 7d2f70e:      	movl	$0x1, %r15d
 7d2f714:      	movq	%r10, %rdi
 7d2f717:      	shlq	$0x7, %rdi
 7d2f71b:      	leaq	(%rdi,%r10,8), %rdi
 7d2f71f:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f724:      	movl	$0x0, %edi
 7d2f729:      	cmovel	%eax, %edi
 7d2f72c:      	addl	%r11d, %edi
 7d2f72f:      	cmpl	%edi, %esi
 7d2f731:      	cmovbel	%edi, %esi
 7d2f734:      	movq	0x10(%r8), %r8
 7d2f738:      	testq	%r8, %r8
 7d2f73b:      	je	0x7d2f7e0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x3e0>
 7d2f741:      	movl	(%r8), %r10d
 7d2f744:      	movl	0x8(%r8), %edi
 7d2f748:      	xorl	%r11d, %r11d
 7d2f74b:      	cmpl	%edi, %r10d
 7d2f74e:      	jae	0x7d2f714 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x314>
 7d2f750:      	leaq	-0x1(%rdi), %r9
 7d2f754:      	xorl	%r11d, %r11d
 7d2f757:      	movq	%r10, %r15
 7d2f75a:      	cmpq	%r10, %r9
 7d2f75d:      	je	0x7d2f6f0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2f0>
 7d2f75f:      	subq	%r10, %rdi
 7d2f762:      	movq	%r10, %r9
 7d2f765:      	shlq	$0x7, %r9
 7d2f769:      	leaq	(%r9,%r10,8), %r15
 7d2f76d:      	leaq	0xf4(%rbx), %r9
 7d2f774:      	addq	%r9, %r15
 7d2f777:      	movq	%rdi, %r12
 7d2f77a:      	andq	$-0x2, %r12
 7d2f77e:      	negq	%r12
 7d2f781:      	xorl	%r11d, %r11d
 7d2f784:      	xorl	%r9d, %r9d
 7d2f787:      	nopw	(%rax,%rax)
 7d2f790:      	cmpl	$0x0, -0xd8(%r15)
 7d2f798:      	cmovnel	%ebp, %r11d
 7d2f79c:      	addl	-0x88(%r15), %r11d
 7d2f7a3:      	addl	-0x90(%r15), %r11d
 7d2f7aa:      	cmpl	$0x0, -0x50(%r15)
 7d2f7af:      	cmovnel	%ebp, %r11d
 7d2f7b3:      	addl	(%r15), %r11d
 7d2f7b6:      	addl	-0x8(%r15), %r11d
 7d2f7ba:      	addq	$0x110, %r15            # imm = 0x110
 7d2f7c1:      	addq	$-0x2, %r9
 7d2f7c5:      	cmpq	%r9, %r12
 7d2f7c8:      	jne	0x7d2f790 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x390>
 7d2f7ca:      	testb	$0x1, %dil
 7d2f7ce:      	je	0x7d2f70e <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x30e>
 7d2f7d4:      	movq	%r10, %r15
 7d2f7d7:      	subq	%r9, %r15
 7d2f7da:      	jmp	0x7d2f6f0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2f0>
 7d2f7df:      	nop
 7d2f7e0:      	leaq	(%rbx,%r13), %r8
 7d2f7e4:      	movq	(%r8), %rdi
 7d2f7e7:      	cmpw	$0x19, 0x10(%rdi)
 7d2f7ec:      	jne	0x7d2f840 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x440>
 7d2f7ee:      	movq	0x20(%rsp), %rax
 7d2f7f3:      	movl	0xc(%rsp), %esi
 7d2f7f7:      	jmp	0x7d2f80d <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x40d>
 7d2f7f9:      	nopl	(%rax)
 7d2f800:      	movq	0x10(%rax), %rax
 7d2f804:      	testq	%rax, %rax
 7d2f807:      	je	0x7d2f910 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x510>
 7d2f80d:      	movl	(%rax), %ecx
 7d2f80f:      	movq	%rcx, %rdx
 7d2f812:      	shlq	$0x7, %rdx
 7d2f816:      	leaq	(%rdx,%rcx,8), %rcx
 7d2f81a:      	movq	(%rbx,%rcx), %rdx
 7d2f81e:      	movq	0xd0(%rdx), %rdx
 7d2f825:      	testq	%rdx, %rdx
 7d2f828:      	je	0x7d2f800 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f82a:      	cmpb	$0x50, 0x43(%rdx)
 7d2f82e:      	je	0x7d2f800 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f830:      	addq	%rbx, %rcx
 7d2f833:      	movl	%esi, 0x64(%rcx)
 7d2f836:      	movl	$0x0, 0x1c(%rcx)
 7d2f83d:      	jmp	0x7d2f800 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f83f:      	nop
 7d2f840:      	xorl	%r10d, %r10d
 7d2f843:      	cmpl	%ecx, %edx
 7d2f845:      	jae	0x7d2f8e5 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4e5>
 7d2f84b:      	leaq	-0x1(%rcx), %r9
 7d2f84f:      	xorl	%r10d, %r10d
 7d2f852:      	movq	%rdx, %rdi
 7d2f855:      	cmpq	%rdx, %r9
 7d2f858:      	je	0x7d2f8c7 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4c7>
 7d2f85a:      	movq	%rcx, %r11
 7d2f85d:      	subq	%rdx, %r11
 7d2f860:      	leaq	0xf4(%rbx), %rdi
 7d2f867:      	addq	%rdi, %r13
 7d2f86a:      	movq	%r11, %rdi
 7d2f86d:      	andq	$-0x2, %rdi
 7d2f871:      	negq	%rdi
 7d2f874:      	xorl	%r10d, %r10d
 7d2f877:      	xorl	%r9d, %r9d
 7d2f87a:      	nopw	(%rax,%rax)
 7d2f880:      	cmpl	$0x0, -0xd8(%r13)
 7d2f888:      	cmovnel	%ebp, %r10d
 7d2f88c:      	addl	-0x88(%r13), %r10d
 7d2f893:      	addl	-0x90(%r13), %r10d
 7d2f89a:      	cmpl	$0x0, -0x50(%r13)
 7d2f89f:      	cmovnel	%ebp, %r10d
 7d2f8a3:      	addl	(%r13), %r10d
 7d2f8a7:      	addl	-0x8(%r13), %r10d
 7d2f8ab:      	addq	$0x110, %r13            # imm = 0x110
 7d2f8b2:      	addq	$-0x2, %r9
 7d2f8b6:      	cmpq	%r9, %rdi
 7d2f8b9:      	jne	0x7d2f880 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x480>
 7d2f8bb:      	testb	$0x1, %r11b
 7d2f8bf:      	je	0x7d2f8e5 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4e5>
 7d2f8c1:      	movq	%rdx, %rdi
 7d2f8c4:      	subq	%r9, %rdi
 7d2f8c7:      	movq	%rdi, %r9
 7d2f8ca:      	shlq	$0x7, %r9
 7d2f8ce:      	leaq	(%r9,%rdi,8), %rdi
 7d2f8d2:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f8d7:      	cmovnel	%ebp, %r10d
 7d2f8db:      	addl	0x6c(%rbx,%rdi), %r10d
 7d2f8e0:      	addl	0x64(%rbx,%rdi), %r10d
 7d2f8e5:      	cmpl	$0x0, 0x40(%rsp)
 7d2f8ea:      	je	0x7d2fbc6 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7c6>
 7d2f8f0:      	movl	%ecx, %edi
 7d2f8f2:      	subl	%edx, %edi
 7d2f8f4:      	cmpl	$0x2, %edi
 7d2f8f7:      	jae	0x7d2fbf0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7f0>
 7d2f8fd:      	jmp	0x7d2fc40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2f902:      	nopw	%cs:(%rax,%rax)
 7d2f90c:      	nopl	(%rax)
 7d2f910:      	movq	0x20(%rsp), %rcx
 7d2f915:      	movq	0x10(%rsp), %rax
 7d2f91a:      	subq	%rax, %rcx
 7d2f91d:      	movq	%rcx, 0x40(%rsp)
 7d2f922:      	je	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2f928:      	movl	0x4(%rsp), %r12d
 7d2f92d:      	jmp	0x7d2f969 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x569>
 7d2f92f:      	nop
 7d2f930:      	movq	%rsi, %rdi
 7d2f933:      	shlq	$0x7, %rdi
 7d2f937:      	leaq	(%rdi,%rsi,8), %rsi
 7d2f93b:      	cmpl	$0x0, 0x1c(%rbx,%rsi)
 7d2f940:      	cmovnel	%ebp, %edx
 7d2f943:      	addl	0x6c(%rbx,%rsi), %edx
 7d2f947:      	addl	0x64(%rbx,%rsi), %edx
 7d2f94b:      	incl	%r12d
 7d2f94e:      	cmpl	$0x0, 0x1c(%rbx,%rcx)
 7d2f953:      	cmovnel	%r15d, %r12d
 7d2f957:      	addl	%edx, %r12d
 7d2f95a:      	addq	$0x18, %rax
 7d2f95e:      	cmpq	0x20(%rsp), %rax
 7d2f963:      	je	0x7d2fa00 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x600>
 7d2f969:      	movl	(%rax), %esi
 7d2f96b:      	movl	0x8(%rax), %edi
 7d2f96e:      	movq	%rsi, %rcx
 7d2f971:      	shlq	$0x7, %rcx
 7d2f975:      	leaq	(%rcx,%rsi,8), %rcx
 7d2f979:      	xorl	%edx, %edx
 7d2f97b:      	cmpl	%edi, %esi
 7d2f97d:      	jae	0x7d2f94b <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x54b>
 7d2f97f:      	leaq	-0x1(%rdi), %r8
 7d2f983:      	xorl	%edx, %edx
 7d2f985:      	cmpq	%rsi, %r8
 7d2f988:      	je	0x7d2f930 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x530>
 7d2f98a:      	subq	%rsi, %rdi
 7d2f98d:      	leaq	0xf4(%rbx), %rdx
 7d2f994:      	leaq	(%rdx,%rcx), %r8
 7d2f998:      	movq	%rdi, %r10
 7d2f99b:      	andq	$-0x2, %r10
 7d2f99f:      	negq	%r10
 7d2f9a2:      	xorl	%edx, %edx
 7d2f9a4:      	xorl	%r9d, %r9d
 7d2f9a7:      	nopw	(%rax,%rax)
 7d2f9b0:      	cmpl	$0x0, -0xd8(%r8)
 7d2f9b8:      	cmovnel	%ebp, %edx
 7d2f9bb:      	addl	-0x88(%r8), %edx
 7d2f9c2:      	addl	-0x90(%r8), %edx
 7d2f9c9:      	cmpl	$0x0, -0x50(%r8)
 7d2f9ce:      	cmovnel	%ebp, %edx
 7d2f9d1:      	addl	(%r8), %edx
 7d2f9d4:      	addl	-0x8(%r8), %edx
 7d2f9d8:      	addq	$0x110, %r8             # imm = 0x110
 7d2f9df:      	addq	$-0x2, %r9
 7d2f9e3:      	cmpq	%r9, %r10
 7d2f9e6:      	jne	0x7d2f9b0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x5b0>
 7d2f9e8:      	testb	$0x1, %dil
 7d2f9ec:      	je	0x7d2f94b <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x54b>
 7d2f9f2:      	subq	%r9, %rsi
 7d2f9f5:      	jmp	0x7d2f930 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x530>
 7d2f9fa:      	nopw	(%rax,%rax)
 7d2fa00:      	movq	0x38(%rsp), %rax
 7d2fa05:      	movl	(%rax), %r8d
 7d2fa08:      	movq	0x28(%rsp), %rax
 7d2fa0d:      	movq	(%rax), %rdi
 7d2fa10:      	movq	%rdi, 0x50(%rsp)
 7d2fa15:      	movq	0x10(%rsp), %rsi
 7d2fa1a:      	movq	0x20(%rsp), %rdx
 7d2fa1f:      	movl	0x4(%rsp), %ecx
 7d2fa23:      	movq	0x18(%rsp), %r9
 7d2fa28:      	callq	0x7d30d50 <_ZNK5clang6format17WhitespaceManager18getMaximumNetWidthIPNS1_15CellDescriptionEEEjRKT_S7_jjj>
 7d2fa2d:      	movl	%eax, 0x4c(%rsp)
 7d2fa31:      	subl	%r12d, %eax
 7d2fa34:      	jbe	0x7d2fa40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x640>
 7d2fa36:      	movq	0x50(%rsp), %rcx
 7d2fa3b:      	movl	%eax, 0x64(%rcx,%r13)
 7d2fa40:      	testq	%r14, %r14
 7d2fa43:      	setne	%al
 7d2fa46:      	movq	0x30(%rsp), %rcx
 7d2fa4b:      	movl	0x48(%rcx), %ecx
 7d2fa4e:      	movq	%rcx, 0x18(%rsp)
 7d2fa53:      	cmpl	$0x2, %ecx
 7d2fa56:      	setae	%cl
 7d2fa59:      	andb	%al, %cl
 7d2fa5b:      	cmpb	$0x1, %cl
 7d2fa5e:      	jne	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fa64:      	movq	0x28(%rsp), %rax
 7d2fa69:      	movq	(%rax), %rcx
 7d2fa6c:      	movl	$0x1, %esi
 7d2fa71:      	nopw	%cs:(%rax,%rax)
 7d2fa7b:      	nopl	(%rax,%rax)
 7d2fa80:      	movq	0x38(%rsp), %rax
 7d2fa85:      	movl	(%rax), %eax
 7d2fa87:      	imull	%esi, %eax
 7d2fa8a:      	leaq	(%rax,%rax,2), %rax
 7d2fa8e:      	movq	0x10(%rsp), %rdx
 7d2fa93:      	leaq	(%rdx,%rax,8), %rdi
 7d2fa97:      	movq	0x40(%rsp), %rax
 7d2fa9c:      	leaq	(%rdi,%rax), %r10
 7d2faa0:      	movl	0x4(%rsp), %r8d
 7d2faa5:      	jmp	0x7d2faeb <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6eb>
 7d2faa7:      	nopw	(%rax,%rax)
 7d2fab0:      	movq	%r13, %rax
 7d2fab3:      	shlq	$0x7, %rax
 7d2fab7:      	leaq	(%rax,%r13,8), %rax
 7d2fabb:      	cmpl	$0x0, 0x1c(%rcx,%rax)
 7d2fac0:      	cmovnel	%ebp, %r12d
 7d2fac4:      	addl	0x6c(%rcx,%rax), %r12d
 7d2fac9:      	addl	0x64(%rcx,%rax), %r12d
 7d2face:      	incl	%r8d
 7d2fad1:      	cmpl	$0x0, 0x1c(%rcx,%r11)
 7d2fad7:      	cmovnel	%r15d, %r8d
 7d2fadb:      	addl	%r12d, %r8d
 7d2fade:      	addq	$0x18, %rdi
 7d2fae2:      	cmpq	%r10, %rdi
 7d2fae5:      	je	0x7d2fb80 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x780>
 7d2faeb:      	movl	(%rdi), %r13d
 7d2faee:      	movl	0x8(%rdi), %eax
 7d2faf1:      	movq	%r13, %rdx
 7d2faf4:      	shlq	$0x7, %rdx
 7d2faf8:      	leaq	(%rdx,%r13,8), %r11
 7d2fafc:      	xorl	%r12d, %r12d
 7d2faff:      	cmpl	%eax, %r13d
 7d2fb02:      	jae	0x7d2face <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6ce>
 7d2fb04:      	leaq	-0x1(%rax), %rdx
 7d2fb08:      	xorl	%r12d, %r12d
 7d2fb0b:      	cmpq	%r13, %rdx
 7d2fb0e:      	je	0x7d2fab0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6b0>
 7d2fb10:      	subq	%r13, %rax
 7d2fb13:      	leaq	0xf4(%rcx), %rdx
 7d2fb1a:      	addq	%r11, %rdx
 7d2fb1d:      	movq	%rax, %r15
 7d2fb20:      	andq	$-0x2, %r15
 7d2fb24:      	negq	%r15
 7d2fb27:      	xorl	%r12d, %r12d
 7d2fb2a:      	xorl	%r9d, %r9d
 7d2fb2d:      	nopl	(%rax)
 7d2fb30:      	cmpl	$0x0, -0xd8(%rdx)
 7d2fb37:      	cmovnel	%ebp, %r12d
 7d2fb3b:      	addl	-0x88(%rdx), %r12d
 7d2fb42:      	addl	-0x90(%rdx), %r12d
 7d2fb49:      	cmpl	$0x0, -0x50(%rdx)
 7d2fb4d:      	cmovnel	%ebp, %r12d
 7d2fb51:      	addl	(%rdx), %r12d
 7d2fb54:      	addl	-0x8(%rdx), %r12d
 7d2fb58:      	addq	$0x110, %rdx            # imm = 0x110
 7d2fb5f:      	addq	$-0x2, %r9
 7d2fb63:      	cmpq	%r9, %r15
 7d2fb66:      	jne	0x7d2fb30 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x730>
 7d2fb68:      	testb	$0x1, %al
 7d2fb6a:      	movl	$0x1, %r15d
 7d2fb70:      	je	0x7d2face <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6ce>
 7d2fb76:      	subq	%r9, %r13
 7d2fb79:      	jmp	0x7d2fab0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6b0>
 7d2fb7e:      	nop
 7d2fb80:      	movl	0x4c(%rsp), %eax
 7d2fb84:      	subl	%r8d, %eax
 7d2fb87:      	jbe	0x7d2fba8 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7a8>
 7d2fb89:      	movl	(%r14), %edx
 7d2fb8c:      	movq	%rdx, %rdi
 7d2fb8f:      	shlq	$0x7, %rdi
 7d2fb93:      	leaq	(%rdi,%rdx,8), %rdx
 7d2fb97:      	movl	%eax, 0x64(%rcx,%rdx)
 7d2fb9b:      	movq	0x30(%rsp), %rax
 7d2fba0:      	movl	0x48(%rax), %eax
 7d2fba3:      	movq	%rax, 0x18(%rsp)
 7d2fba8:      	movq	0x10(%r14), %r14
 7d2fbac:      	testq	%r14, %r14
 7d2fbaf:      	je	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fbb5:      	incl	%esi
 7d2fbb7:      	cmpl	%esi, 0x18(%rsp)
 7d2fbbb:      	ja	0x7d2fa80 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x680>
 7d2fbc1:      	jmp	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fbc6:      	leal	(%rax,%rax), %edi
 7d2fbc9:      	cmpl	$0x0, 0x8(%rsp)
 7d2fbce:      	movl	$0x1, %r9d
 7d2fbd4:      	cmovel	0xc(%rsp), %r9d
 7d2fbda:      	subl	%edi, %r9d
 7d2fbdd:      	addl	%esi, %r9d
 7d2fbe0:      	subl	%r10d, %r9d
 7d2fbe3:      	movl	%r9d, 0x64(%r8)
 7d2fbe7:      	movl	%ecx, %edi
 7d2fbe9:      	subl	%edx, %edi
 7d2fbeb:      	cmpl	$0x2, %edi
 7d2fbee:      	jb	0x7d2fc40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fbf0:      	leal	0x1(%rdx), %edi
 7d2fbf3:      	cmpl	%ecx, %edi
 7d2fbf5:      	jae	0x7d2fc40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fbf7:      	movl	%edi, %edi
 7d2fbf9:      	movl	%edx, %r9d
 7d2fbfc:      	subl	%ecx, %r9d
 7d2fbff:      	testb	$0x1, %r9b
 7d2fc03:      	jne	0x7d2fc26 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x826>
 7d2fc05:      	movq	%rdi, %r9
 7d2fc08:      	shlq	$0x7, %r9
 7d2fc0c:      	leaq	(%r9,%rdi,8), %r9
 7d2fc10:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fc16:      	je	0x7d2fc23 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x823>
 7d2fc18:      	addq	%rbx, %r9
 7d2fc1b:      	movl	0x64(%r8), %r10d
 7d2fc1f:      	movl	%r10d, 0x64(%r9)
 7d2fc23:      	incq	%rdi
 7d2fc26:      	leal	-0x2(%rcx), %r9d
 7d2fc2a:      	cmpl	%edx, %r9d
 7d2fc2d:      	jne	0x7d2fe13 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa13>
 7d2fc33:      	nopw	%cs:(%rax,%rax)
 7d2fc3d:      	nopl	(%rax)
 7d2fc40:      	testq	%r14, %r14
 7d2fc43:      	je	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fc49:      	cmpl	$0x0, 0x8(%rsp)
 7d2fc4e:      	movl	$0x1, %ecx
 7d2fc53:      	cmovel	0xc(%rsp), %ecx
 7d2fc58:      	addl	%esi, %ecx
 7d2fc5a:      	jmp	0x7d2fc6d <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x86d>
 7d2fc5c:      	nopl	(%rax)
 7d2fc60:      	movq	0x10(%r14), %r14
 7d2fc64:      	testq	%r14, %r14
 7d2fc67:      	je	0x7d2f4d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fc6d:      	movl	(%r14), %esi
 7d2fc70:      	movl	0x8(%r14), %edx
 7d2fc74:      	xorl	%r8d, %r8d
 7d2fc77:      	cmpl	%esi, %edx
 7d2fc79:      	jbe	0x7d2fd24 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x924>
 7d2fc7f:      	leaq	-0x1(%rdx), %r9
 7d2fc83:      	xorl	%r8d, %r8d
 7d2fc86:      	movq	%rsi, %rdi
 7d2fc89:      	cmpq	%rsi, %r9
 7d2fc8c:      	je	0x7d2fd06 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x906>
 7d2fc92:      	movq	%rdx, %rdi
 7d2fc95:      	subq	%rsi, %rdi
 7d2fc98:      	movq	%rsi, %r8
 7d2fc9b:      	shlq	$0x7, %r8
 7d2fc9f:      	leaq	(%r8,%rsi,8), %r10
 7d2fca3:      	leaq	0xf4(%rbx), %r8
 7d2fcaa:      	addq	%r8, %r10
 7d2fcad:      	movq	%rdi, %r11
 7d2fcb0:      	andq	$-0x2, %r11
 7d2fcb4:      	negq	%r11
 7d2fcb7:      	xorl	%r8d, %r8d
 7d2fcba:      	xorl	%r9d, %r9d
 7d2fcbd:      	nopl	(%rax)
 7d2fcc0:      	cmpl	$0x0, -0xd8(%r10)
 7d2fcc8:      	cmovnel	%ebp, %r8d
 7d2fccc:      	addl	-0x88(%r10), %r8d
 7d2fcd3:      	addl	-0x90(%r10), %r8d
 7d2fcda:      	cmpl	$0x0, -0x50(%r10)
 7d2fcdf:      	cmovnel	%ebp, %r8d
 7d2fce3:      	addl	(%r10), %r8d
 7d2fce6:      	addl	-0x8(%r10), %r8d
 7d2fcea:      	addq	$0x110, %r10            # imm = 0x110
 7d2fcf1:      	addq	$-0x2, %r9
 7d2fcf5:      	cmpq	%r9, %r11
 7d2fcf8:      	jne	0x7d2fcc0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x8c0>
 7d2fcfa:      	testb	$0x1, %dil
 7d2fcfe:      	je	0x7d2fd24 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x924>
 7d2fd00:      	movq	%rsi, %rdi
 7d2fd03:      	subq	%r9, %rdi
 7d2fd06:      	movq	%rdi, %r9
 7d2fd09:      	shlq	$0x7, %r9
 7d2fd0d:      	leaq	(%r9,%rdi,8), %rdi
 7d2fd11:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2fd16:      	cmovnel	%ebp, %r8d
 7d2fd1a:      	addl	0x6c(%rbx,%rdi), %r8d
 7d2fd1f:      	addl	0x64(%rbx,%rdi), %r8d
 7d2fd24:      	movq	%rsi, %rdi
 7d2fd27:      	shlq	$0x7, %rdi
 7d2fd2b:      	leaq	(%rdi,%rsi,8), %r9
 7d2fd2f:      	leaq	(%rbx,%r9), %rdi
 7d2fd33:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fd39:      	je	0x7d2fd50 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x950>
 7d2fd3b:      	movl	%edx, %r8d
 7d2fd3e:      	subl	%esi, %r8d
 7d2fd41:      	cmpl	$0x2, %r8d
 7d2fd45:      	jb	0x7d2fc60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fd4b:      	jmp	0x7d2fd6d <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x96d>
 7d2fd4d:      	nopl	(%rax)
 7d2fd50:      	addl	%eax, %r8d
 7d2fd53:      	movl	%ecx, %r9d
 7d2fd56:      	subl	%r8d, %r9d
 7d2fd59:      	movl	%r9d, 0x64(%rdi)
 7d2fd5d:      	movl	%edx, %r8d
 7d2fd60:      	subl	%esi, %r8d
 7d2fd63:      	cmpl	$0x2, %r8d
 7d2fd67:      	jb	0x7d2fc60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fd6d:      	leal	0x1(%rsi), %r8d
 7d2fd71:      	cmpl	%edx, %r8d
 7d2fd74:      	jae	0x7d2fc60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fd7a:      	movl	%r8d, %r8d
 7d2fd7d:      	movl	%esi, %r9d
 7d2fd80:      	subl	%edx, %r9d
 7d2fd83:      	testb	$0x1, %r9b
 7d2fd87:      	jne	0x7d2fdaa <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9aa>
 7d2fd89:      	movq	%r8, %r9
 7d2fd8c:      	shlq	$0x7, %r9
 7d2fd90:      	leaq	(%r9,%r8,8), %r9
 7d2fd94:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fd9a:      	je	0x7d2fda7 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9a7>
 7d2fd9c:      	addq	%rbx, %r9
 7d2fd9f:      	movl	0x64(%rdi), %r10d
 7d2fda3:      	movl	%r10d, 0x64(%r9)
 7d2fda7:      	incq	%r8
 7d2fdaa:      	leal	-0x2(%rdx), %r9d
 7d2fdae:      	cmpl	%esi, %r9d
 7d2fdb1:      	je	0x7d2fc60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fdb7:      	movq	%r8, %rsi
 7d2fdba:      	shlq	$0x7, %rsi
 7d2fdbe:      	leaq	(%rsi,%r8,8), %rsi
 7d2fdc2:      	leaq	0xec(%rbx), %r9
 7d2fdc9:      	addq	%r9, %rsi
 7d2fdcc:      	subl	%r8d, %edx
 7d2fdcf:      	jmp	0x7d2fdf0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9f0>
 7d2fdd1:      	nopw	%cs:(%rax,%rax)
 7d2fddb:      	nopl	(%rax,%rax)
 7d2fde0:      	addq	$0x110, %rsi            # imm = 0x110
 7d2fde7:      	addl	$-0x2, %edx
 7d2fdea:      	je	0x7d2fc60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fdf0:      	cmpl	$0x0, -0xd0(%rsi)
 7d2fdf7:      	je	0x7d2fe04 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa04>
 7d2fdf9:      	movl	0x64(%rdi), %r8d
 7d2fdfd:      	movl	%r8d, -0x88(%rsi)
 7d2fe04:      	cmpl	$0x0, -0x48(%rsi)
 7d2fe08:      	je	0x7d2fde0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9e0>
 7d2fe0a:      	movl	0x64(%rdi), %r8d
 7d2fe0e:      	movl	%r8d, (%rsi)
 7d2fe11:      	jmp	0x7d2fde0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9e0>
 7d2fe13:      	movq	%rdi, %rdx
 7d2fe16:      	shlq	$0x7, %rdx
 7d2fe1a:      	leaq	(%rdx,%rdi,8), %rdx
 7d2fe1e:      	leaq	0xec(%rbx), %r9
 7d2fe25:      	addq	%r9, %rdx
 7d2fe28:      	subl	%edi, %ecx
 7d2fe2a:      	jmp	0x7d2fe40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa40>
 7d2fe2c:      	nopl	(%rax)
 7d2fe30:      	addq	$0x110, %rdx            # imm = 0x110
 7d2fe37:      	addl	$-0x2, %ecx
 7d2fe3a:      	je	0x7d2fc40 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fe40:      	cmpl	$0x0, -0xd0(%rdx)
 7d2fe47:      	je	0x7d2fe53 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa53>
 7d2fe49:      	movl	0x64(%r8), %edi
 7d2fe4d:      	movl	%edi, -0x88(%rdx)
 7d2fe53:      	cmpl	$0x0, -0x48(%rdx)
 7d2fe57:      	je	0x7d2fe30 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa30>
 7d2fe59:      	movl	0x64(%r8), %edi
 7d2fe5d:      	movl	%edi, (%rdx)
 7d2fe5f:      	jmp	0x7d2fe30 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa30>
