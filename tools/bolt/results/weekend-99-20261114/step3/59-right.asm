
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007d2f370 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE>:
 7d2f370:      	pushq	%rbp
 7d2f371:      	pushq	%r15
 7d2f373:      	pushq	%r14
 7d2f375:      	pushq	%r13
 7d2f377:      	pushq	%r12
 7d2f379:      	pushq	%rbx
 7d2f37a:      	subq	$0x58, %rsp
 7d2f37e:      	movq	%rdi, 0x28(%rsp)
 7d2f383:      	movq	%rsi, 0x30(%rsp)
 7d2f388:      	movl	0x48(%rsi), %eax
 7d2f38b:      	movq	%rax, 0x18(%rsp)
 7d2f390:      	cmpq	$0x2, %rax
 7d2f394:      	jae	0x7d2f3a5 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x35>
 7d2f396:      	addq	$0x58, %rsp
 7d2f39a:      	popq	%rbx
 7d2f39b:      	popq	%r12
 7d2f39d:      	popq	%r13
 7d2f39f:      	popq	%r14
 7d2f3a1:      	popq	%r15
 7d2f3a3:      	popq	%rbp
 7d2f3a4:      	retq
 7d2f3a5:      	movq	0x30(%rsp), %rax
 7d2f3aa:      	movq	0x40(%rax), %rax
 7d2f3ae:      	movq	0x18(%rsp), %rcx
 7d2f3b3:      	shlq	$0x2, %rcx
 7d2f3b7:      	movq	%rax, 0x38(%rsp)
 7d2f3bc:      	movl	(%rax), %eax
 7d2f3be:      	xorl	%edx, %edx
 7d2f3c0:      	movq	0x38(%rsp), %rsi
 7d2f3c5:      	nopw	%cs:(%rax,%rax)
 7d2f3cf:      	nop
 7d2f3d0:      	cmpl	%eax, (%rsi,%rdx)
 7d2f3d3:      	jne	0x7d2f396 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f3d5:      	addq	$0x4, %rdx
 7d2f3d9:      	cmpq	%rdx, %rcx
 7d2f3dc:      	jne	0x7d2f3d0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x60>
 7d2f3de:      	movq	0x28(%rsp), %rcx
 7d2f3e3:      	movq	0x8c8(%rcx), %rcx
 7d2f3ea:      	xorl	%edx, %edx
 7d2f3ec:      	cmpb	$0x0, 0xdc(%rcx)
 7d2f3f3:      	sete	%cl
 7d2f3f6:      	testl	%eax, %eax
 7d2f3f8:      	je	0x7d2f396 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f3fa:      	movb	%cl, %dl
 7d2f3fc:      	movl	%edx, 0xc(%rsp)
 7d2f400:      	movq	0x30(%rsp), %rax
 7d2f405:      	movq	(%rax), %r14
 7d2f408:      	movq	0x28(%rsp), %rcx
 7d2f40d:      	movq	(%rcx), %rbx
 7d2f410:      	movl	0x80(%rax), %eax
 7d2f416:      	movl	%eax, 0x4(%rsp)
 7d2f41a:      	xorl	%ebp, %ebp
 7d2f41c:      	movl	$0x1, %r15d
 7d2f422:      	movq	%r14, 0x10(%rsp)
 7d2f427:      	movl	$0x0, 0x8(%rsp)
 7d2f42f:      	jmp	0x7d2f460 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xf0>
 7d2f431:      	nopw	%cs:(%rax,%rax)
 7d2f43b:      	nopl	(%rax,%rax)
 7d2f440:      	movl	0x8(%rsp), %ecx
 7d2f444:      	incl	%ecx
 7d2f446:      	movq	0x20(%rsp), %r14
 7d2f44b:      	addq	$0x18, %r14
 7d2f44f:      	movq	0x38(%rsp), %rax
 7d2f454:      	movl	%ecx, 0x8(%rsp)
 7d2f458:      	cmpl	(%rax), %ecx
 7d2f45a:      	jae	0x7d2f396 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x26>
 7d2f460:      	cmpb	$0x0, 0xc(%r14)
 7d2f465:      	jne	0x7d2f483 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x113>
 7d2f467:      	movq	%r14, %rax
 7d2f46a:      	nopw	(%rax,%rax)
 7d2f470:      	movq	0x10(%rax), %rax
 7d2f474:      	testq	%rax, %rax
 7d2f477:      	je	0x7d2f570 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x200>
 7d2f47d:      	cmpb	$0x1, 0xc(%rax)
 7d2f481:      	jne	0x7d2f470 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x100>
 7d2f483:      	movl	0x4(%rsp), %eax
 7d2f487:      	cmpq	%r14, 0x10(%rsp)
 7d2f48c:      	je	0x7d2f572 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x202>
 7d2f492:      	movq	0x10(%rsp), %rcx
 7d2f497:      	movl	0x4(%rsp), %eax
 7d2f49b:      	jmp	0x7d2f4d5 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x165>
 7d2f49d:      	nopl	(%rax)
 7d2f4a0:      	movq	%rdi, %r8
 7d2f4a3:      	shlq	$0x7, %r8
 7d2f4a7:      	leaq	(%r8,%rdi,8), %rdi
 7d2f4ab:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f4b0:      	cmovnel	%ebp, %esi
 7d2f4b3:      	addl	0x6c(%rbx,%rdi), %esi
 7d2f4b7:      	addl	0x64(%rbx,%rdi), %esi
 7d2f4bb:      	incl	%eax
 7d2f4bd:      	cmpl	$0x0, 0x1c(%rbx,%rdx)
 7d2f4c2:      	cmovnel	%r15d, %eax
 7d2f4c6:      	addl	%esi, %eax
 7d2f4c8:      	addq	$0x18, %rcx
 7d2f4cc:      	cmpq	%r14, %rcx
 7d2f4cf:      	je	0x7d2f572 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x202>
 7d2f4d5:      	movl	(%rcx), %edi
 7d2f4d7:      	movl	0x8(%rcx), %r8d
 7d2f4db:      	movq	%rdi, %rdx
 7d2f4de:      	shlq	$0x7, %rdx
 7d2f4e2:      	leaq	(%rdx,%rdi,8), %rdx
 7d2f4e6:      	xorl	%esi, %esi
 7d2f4e8:      	cmpl	%r8d, %edi
 7d2f4eb:      	jae	0x7d2f4bb <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x14b>
 7d2f4ed:      	leaq	-0x1(%r8), %r9
 7d2f4f1:      	xorl	%esi, %esi
 7d2f4f3:      	cmpq	%rdi, %r9
 7d2f4f6:      	je	0x7d2f4a0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x130>
 7d2f4f8:      	subq	%rdi, %r8
 7d2f4fb:      	leaq	0xf4(%rbx), %rsi
 7d2f502:      	leaq	(%rsi,%rdx), %r10
 7d2f506:      	movq	%r8, %r11
 7d2f509:      	andq	$-0x2, %r11
 7d2f50d:      	negq	%r11
 7d2f510:      	xorl	%esi, %esi
 7d2f512:      	xorl	%r9d, %r9d
 7d2f515:      	nopw	%cs:(%rax,%rax)
 7d2f51f:      	nop
 7d2f520:      	cmpl	$0x0, -0xd8(%r10)
 7d2f528:      	cmovnel	%ebp, %esi
 7d2f52b:      	addl	-0x88(%r10), %esi
 7d2f532:      	addl	-0x90(%r10), %esi
 7d2f539:      	cmpl	$0x0, -0x50(%r10)
 7d2f53e:      	cmovnel	%ebp, %esi
 7d2f541:      	addl	(%r10), %esi
 7d2f544:      	addl	-0x8(%r10), %esi
 7d2f548:      	addq	$0x110, %r10            # imm = 0x110
 7d2f54f:      	addq	$-0x2, %r9
 7d2f553:      	cmpq	%r9, %r11
 7d2f556:      	jne	0x7d2f520 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x1b0>
 7d2f558:      	testb	$0x1, %r8b
 7d2f55c:      	je	0x7d2f4bb <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x14b>
 7d2f562:      	subq	%r9, %rdi
 7d2f565:      	jmp	0x7d2f4a0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x130>
 7d2f56a:      	nopw	(%rax,%rax)
 7d2f570:      	xorl	%eax, %eax
 7d2f572:      	movl	(%r14), %edx
 7d2f575:      	movl	0x8(%r14), %ecx
 7d2f579:      	xorl	%r8d, %r8d
 7d2f57c:      	cmpl	%edx, %ecx
 7d2f57e:      	jbe	0x7d2f622 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2b2>
 7d2f584:      	leaq	-0x1(%rcx), %rdi
 7d2f588:      	xorl	%r8d, %r8d
 7d2f58b:      	movq	%rdx, %rsi
 7d2f58e:      	cmpq	%rdx, %rdi
 7d2f591:      	je	0x7d2f604 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x294>
 7d2f593:      	movq	%rcx, %rsi
 7d2f596:      	subq	%rdx, %rsi
 7d2f599:      	movq	%rdx, %rdi
 7d2f59c:      	shlq	$0x7, %rdi
 7d2f5a0:      	leaq	(%rdi,%rdx,8), %rdi
 7d2f5a4:      	leaq	0xf4(%rbx), %r8
 7d2f5ab:      	addq	%r8, %rdi
 7d2f5ae:      	movq	%rsi, %r10
 7d2f5b1:      	andq	$-0x2, %r10
 7d2f5b5:      	negq	%r10
 7d2f5b8:      	xorl	%r8d, %r8d
 7d2f5bb:      	xorl	%r9d, %r9d
 7d2f5be:      	nop
 7d2f5c0:      	cmpl	$0x0, -0xd8(%rdi)
 7d2f5c7:      	cmovnel	%ebp, %r8d
 7d2f5cb:      	addl	-0x88(%rdi), %r8d
 7d2f5d2:      	addl	-0x90(%rdi), %r8d
 7d2f5d9:      	cmpl	$0x0, -0x50(%rdi)
 7d2f5dd:      	cmovnel	%ebp, %r8d
 7d2f5e1:      	addl	(%rdi), %r8d
 7d2f5e4:      	addl	-0x8(%rdi), %r8d
 7d2f5e8:      	addq	$0x110, %rdi            # imm = 0x110
 7d2f5ef:      	addq	$-0x2, %r9
 7d2f5f3:      	cmpq	%r9, %r10
 7d2f5f6:      	jne	0x7d2f5c0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x250>
 7d2f5f8:      	testb	$0x1, %sil
 7d2f5fc:      	je	0x7d2f622 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2b2>
 7d2f5fe:      	movq	%rdx, %rsi
 7d2f601:      	subq	%r9, %rsi
 7d2f604:      	movq	%rsi, %rdi
 7d2f607:      	shlq	$0x7, %rdi
 7d2f60b:      	leaq	(%rdi,%rsi,8), %rsi
 7d2f60f:      	cmpl	$0x0, 0x1c(%rbx,%rsi)
 7d2f614:      	cmovnel	%ebp, %r8d
 7d2f618:      	addl	0x6c(%rbx,%rsi), %r8d
 7d2f61d:      	addl	0x64(%rbx,%rsi), %r8d
 7d2f622:      	movq	%rdx, %rsi
 7d2f625:      	shlq	$0x7, %rsi
 7d2f629:      	leaq	(%rsi,%rdx,8), %r13
 7d2f62d:      	movl	0x1c(%rbx,%r13), %esi
 7d2f632:      	movl	%esi, 0x40(%rsp)
 7d2f636:      	testl	%esi, %esi
 7d2f638:      	movl	$0x0, %esi
 7d2f63d:      	cmovel	%eax, %esi
 7d2f640:      	addl	%r8d, %esi
 7d2f643:      	movq	%r14, 0x20(%rsp)
 7d2f648:      	movq	0x10(%r14), %r14
 7d2f64c:      	testq	%r14, %r14
 7d2f64f:      	je	0x7d2f750 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x3e0>
 7d2f655:      	movq	%r14, %r8
 7d2f658:      	jmp	0x7d2f6b1 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x341>
 7d2f65a:      	nopw	(%rax,%rax)
 7d2f660:      	movq	%r15, %rdi
 7d2f663:      	shlq	$0x7, %rdi
 7d2f667:      	leaq	(%rdi,%r15,8), %rdi
 7d2f66b:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f670:      	cmovnel	%ebp, %r11d
 7d2f674:      	addl	0x6c(%rbx,%rdi), %r11d
 7d2f679:      	addl	0x64(%rbx,%rdi), %r11d
 7d2f67e:      	movl	$0x1, %r15d
 7d2f684:      	movq	%r10, %rdi
 7d2f687:      	shlq	$0x7, %rdi
 7d2f68b:      	leaq	(%rdi,%r10,8), %rdi
 7d2f68f:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f694:      	movl	$0x0, %edi
 7d2f699:      	cmovel	%eax, %edi
 7d2f69c:      	addl	%r11d, %edi
 7d2f69f:      	cmpl	%edi, %esi
 7d2f6a1:      	cmovbel	%edi, %esi
 7d2f6a4:      	movq	0x10(%r8), %r8
 7d2f6a8:      	testq	%r8, %r8
 7d2f6ab:      	je	0x7d2f750 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x3e0>
 7d2f6b1:      	movl	(%r8), %r10d
 7d2f6b4:      	movl	0x8(%r8), %edi
 7d2f6b8:      	xorl	%r11d, %r11d
 7d2f6bb:      	cmpl	%edi, %r10d
 7d2f6be:      	jae	0x7d2f684 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x314>
 7d2f6c0:      	leaq	-0x1(%rdi), %r9
 7d2f6c4:      	xorl	%r11d, %r11d
 7d2f6c7:      	movq	%r10, %r15
 7d2f6ca:      	cmpq	%r10, %r9
 7d2f6cd:      	je	0x7d2f660 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2f0>
 7d2f6cf:      	subq	%r10, %rdi
 7d2f6d2:      	movq	%r10, %r9
 7d2f6d5:      	shlq	$0x7, %r9
 7d2f6d9:      	leaq	(%r9,%r10,8), %r15
 7d2f6dd:      	leaq	0xf4(%rbx), %r9
 7d2f6e4:      	addq	%r9, %r15
 7d2f6e7:      	movq	%rdi, %r12
 7d2f6ea:      	andq	$-0x2, %r12
 7d2f6ee:      	negq	%r12
 7d2f6f1:      	xorl	%r11d, %r11d
 7d2f6f4:      	xorl	%r9d, %r9d
 7d2f6f7:      	nopw	(%rax,%rax)
 7d2f700:      	cmpl	$0x0, -0xd8(%r15)
 7d2f708:      	cmovnel	%ebp, %r11d
 7d2f70c:      	addl	-0x88(%r15), %r11d
 7d2f713:      	addl	-0x90(%r15), %r11d
 7d2f71a:      	cmpl	$0x0, -0x50(%r15)
 7d2f71f:      	cmovnel	%ebp, %r11d
 7d2f723:      	addl	(%r15), %r11d
 7d2f726:      	addl	-0x8(%r15), %r11d
 7d2f72a:      	addq	$0x110, %r15            # imm = 0x110
 7d2f731:      	addq	$-0x2, %r9
 7d2f735:      	cmpq	%r9, %r12
 7d2f738:      	jne	0x7d2f700 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x390>
 7d2f73a:      	testb	$0x1, %dil
 7d2f73e:      	je	0x7d2f67e <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x30e>
 7d2f744:      	movq	%r10, %r15
 7d2f747:      	subq	%r9, %r15
 7d2f74a:      	jmp	0x7d2f660 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x2f0>
 7d2f74f:      	nop
 7d2f750:      	leaq	(%rbx,%r13), %r8
 7d2f754:      	movq	(%r8), %rdi
 7d2f757:      	cmpw	$0x19, 0x10(%rdi)
 7d2f75c:      	jne	0x7d2f7b0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x440>
 7d2f75e:      	movq	0x20(%rsp), %rax
 7d2f763:      	movl	0xc(%rsp), %esi
 7d2f767:      	jmp	0x7d2f77d <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x40d>
 7d2f769:      	nopl	(%rax)
 7d2f770:      	movq	0x10(%rax), %rax
 7d2f774:      	testq	%rax, %rax
 7d2f777:      	je	0x7d2f880 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x510>
 7d2f77d:      	movl	(%rax), %ecx
 7d2f77f:      	movq	%rcx, %rdx
 7d2f782:      	shlq	$0x7, %rdx
 7d2f786:      	leaq	(%rdx,%rcx,8), %rcx
 7d2f78a:      	movq	(%rbx,%rcx), %rdx
 7d2f78e:      	movq	0xd0(%rdx), %rdx
 7d2f795:      	testq	%rdx, %rdx
 7d2f798:      	je	0x7d2f770 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f79a:      	cmpb	$0x50, 0x43(%rdx)
 7d2f79e:      	je	0x7d2f770 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f7a0:      	addq	%rbx, %rcx
 7d2f7a3:      	movl	%esi, 0x64(%rcx)
 7d2f7a6:      	movl	$0x0, 0x1c(%rcx)
 7d2f7ad:      	jmp	0x7d2f770 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x400>
 7d2f7af:      	nop
 7d2f7b0:      	xorl	%r10d, %r10d
 7d2f7b3:      	cmpl	%ecx, %edx
 7d2f7b5:      	jae	0x7d2f855 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4e5>
 7d2f7bb:      	leaq	-0x1(%rcx), %r9
 7d2f7bf:      	xorl	%r10d, %r10d
 7d2f7c2:      	movq	%rdx, %rdi
 7d2f7c5:      	cmpq	%rdx, %r9
 7d2f7c8:      	je	0x7d2f837 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4c7>
 7d2f7ca:      	movq	%rcx, %r11
 7d2f7cd:      	subq	%rdx, %r11
 7d2f7d0:      	leaq	0xf4(%rbx), %rdi
 7d2f7d7:      	addq	%rdi, %r13
 7d2f7da:      	movq	%r11, %rdi
 7d2f7dd:      	andq	$-0x2, %rdi
 7d2f7e1:      	negq	%rdi
 7d2f7e4:      	xorl	%r10d, %r10d
 7d2f7e7:      	xorl	%r9d, %r9d
 7d2f7ea:      	nopw	(%rax,%rax)
 7d2f7f0:      	cmpl	$0x0, -0xd8(%r13)
 7d2f7f8:      	cmovnel	%ebp, %r10d
 7d2f7fc:      	addl	-0x88(%r13), %r10d
 7d2f803:      	addl	-0x90(%r13), %r10d
 7d2f80a:      	cmpl	$0x0, -0x50(%r13)
 7d2f80f:      	cmovnel	%ebp, %r10d
 7d2f813:      	addl	(%r13), %r10d
 7d2f817:      	addl	-0x8(%r13), %r10d
 7d2f81b:      	addq	$0x110, %r13            # imm = 0x110
 7d2f822:      	addq	$-0x2, %r9
 7d2f826:      	cmpq	%r9, %rdi
 7d2f829:      	jne	0x7d2f7f0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x480>
 7d2f82b:      	testb	$0x1, %r11b
 7d2f82f:      	je	0x7d2f855 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x4e5>
 7d2f831:      	movq	%rdx, %rdi
 7d2f834:      	subq	%r9, %rdi
 7d2f837:      	movq	%rdi, %r9
 7d2f83a:      	shlq	$0x7, %r9
 7d2f83e:      	leaq	(%r9,%rdi,8), %rdi
 7d2f842:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2f847:      	cmovnel	%ebp, %r10d
 7d2f84b:      	addl	0x6c(%rbx,%rdi), %r10d
 7d2f850:      	addl	0x64(%rbx,%rdi), %r10d
 7d2f855:      	cmpl	$0x0, 0x40(%rsp)
 7d2f85a:      	je	0x7d2fb36 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7c6>
 7d2f860:      	movl	%ecx, %edi
 7d2f862:      	subl	%edx, %edi
 7d2f864:      	cmpl	$0x2, %edi
 7d2f867:      	jae	0x7d2fb60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7f0>
 7d2f86d:      	jmp	0x7d2fbb0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2f872:      	nopw	%cs:(%rax,%rax)
 7d2f87c:      	nopl	(%rax)
 7d2f880:      	movq	0x20(%rsp), %rcx
 7d2f885:      	movq	0x10(%rsp), %rax
 7d2f88a:      	subq	%rax, %rcx
 7d2f88d:      	movq	%rcx, 0x40(%rsp)
 7d2f892:      	je	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2f898:      	movl	0x4(%rsp), %r12d
 7d2f89d:      	jmp	0x7d2f8d9 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x569>
 7d2f89f:      	nop
 7d2f8a0:      	movq	%rsi, %rdi
 7d2f8a3:      	shlq	$0x7, %rdi
 7d2f8a7:      	leaq	(%rdi,%rsi,8), %rsi
 7d2f8ab:      	cmpl	$0x0, 0x1c(%rbx,%rsi)
 7d2f8b0:      	cmovnel	%ebp, %edx
 7d2f8b3:      	addl	0x6c(%rbx,%rsi), %edx
 7d2f8b7:      	addl	0x64(%rbx,%rsi), %edx
 7d2f8bb:      	incl	%r12d
 7d2f8be:      	cmpl	$0x0, 0x1c(%rbx,%rcx)
 7d2f8c3:      	cmovnel	%r15d, %r12d
 7d2f8c7:      	addl	%edx, %r12d
 7d2f8ca:      	addq	$0x18, %rax
 7d2f8ce:      	cmpq	0x20(%rsp), %rax
 7d2f8d3:      	je	0x7d2f970 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x600>
 7d2f8d9:      	movl	(%rax), %esi
 7d2f8db:      	movl	0x8(%rax), %edi
 7d2f8de:      	movq	%rsi, %rcx
 7d2f8e1:      	shlq	$0x7, %rcx
 7d2f8e5:      	leaq	(%rcx,%rsi,8), %rcx
 7d2f8e9:      	xorl	%edx, %edx
 7d2f8eb:      	cmpl	%edi, %esi
 7d2f8ed:      	jae	0x7d2f8bb <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x54b>
 7d2f8ef:      	leaq	-0x1(%rdi), %r8
 7d2f8f3:      	xorl	%edx, %edx
 7d2f8f5:      	cmpq	%rsi, %r8
 7d2f8f8:      	je	0x7d2f8a0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x530>
 7d2f8fa:      	subq	%rsi, %rdi
 7d2f8fd:      	leaq	0xf4(%rbx), %rdx
 7d2f904:      	leaq	(%rdx,%rcx), %r8
 7d2f908:      	movq	%rdi, %r10
 7d2f90b:      	andq	$-0x2, %r10
 7d2f90f:      	negq	%r10
 7d2f912:      	xorl	%edx, %edx
 7d2f914:      	xorl	%r9d, %r9d
 7d2f917:      	nopw	(%rax,%rax)
 7d2f920:      	cmpl	$0x0, -0xd8(%r8)
 7d2f928:      	cmovnel	%ebp, %edx
 7d2f92b:      	addl	-0x88(%r8), %edx
 7d2f932:      	addl	-0x90(%r8), %edx
 7d2f939:      	cmpl	$0x0, -0x50(%r8)
 7d2f93e:      	cmovnel	%ebp, %edx
 7d2f941:      	addl	(%r8), %edx
 7d2f944:      	addl	-0x8(%r8), %edx
 7d2f948:      	addq	$0x110, %r8             # imm = 0x110
 7d2f94f:      	addq	$-0x2, %r9
 7d2f953:      	cmpq	%r9, %r10
 7d2f956:      	jne	0x7d2f920 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x5b0>
 7d2f958:      	testb	$0x1, %dil
 7d2f95c:      	je	0x7d2f8bb <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x54b>
 7d2f962:      	subq	%r9, %rsi
 7d2f965:      	jmp	0x7d2f8a0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x530>
 7d2f96a:      	nopw	(%rax,%rax)
 7d2f970:      	movq	0x38(%rsp), %rax
 7d2f975:      	movl	(%rax), %r8d
 7d2f978:      	movq	0x28(%rsp), %rax
 7d2f97d:      	movq	(%rax), %rdi
 7d2f980:      	movq	%rdi, 0x50(%rsp)
 7d2f985:      	movq	0x10(%rsp), %rsi
 7d2f98a:      	movq	0x20(%rsp), %rdx
 7d2f98f:      	movl	0x4(%rsp), %ecx
 7d2f993:      	movq	0x18(%rsp), %r9
 7d2f998:      	callq	0x7d30cc0 <_ZNK5clang6format17WhitespaceManager18getMaximumNetWidthIPNS1_15CellDescriptionEEEjRKT_S7_jjj>
 7d2f99d:      	movl	%eax, 0x4c(%rsp)
 7d2f9a1:      	subl	%r12d, %eax
 7d2f9a4:      	jbe	0x7d2f9b0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x640>
 7d2f9a6:      	movq	0x50(%rsp), %rcx
 7d2f9ab:      	movl	%eax, 0x64(%rcx,%r13)
 7d2f9b0:      	testq	%r14, %r14
 7d2f9b3:      	setne	%al
 7d2f9b6:      	movq	0x30(%rsp), %rcx
 7d2f9bb:      	movl	0x48(%rcx), %ecx
 7d2f9be:      	movq	%rcx, 0x18(%rsp)
 7d2f9c3:      	cmpl	$0x2, %ecx
 7d2f9c6:      	setae	%cl
 7d2f9c9:      	andb	%al, %cl
 7d2f9cb:      	cmpb	$0x1, %cl
 7d2f9ce:      	jne	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2f9d4:      	movq	0x28(%rsp), %rax
 7d2f9d9:      	movq	(%rax), %rcx
 7d2f9dc:      	movl	$0x1, %esi
 7d2f9e1:      	nopw	%cs:(%rax,%rax)
 7d2f9eb:      	nopl	(%rax,%rax)
 7d2f9f0:      	movq	0x38(%rsp), %rax
 7d2f9f5:      	movl	(%rax), %eax
 7d2f9f7:      	imull	%esi, %eax
 7d2f9fa:      	leaq	(%rax,%rax,2), %rax
 7d2f9fe:      	movq	0x10(%rsp), %rdx
 7d2fa03:      	leaq	(%rdx,%rax,8), %rdi
 7d2fa07:      	movq	0x40(%rsp), %rax
 7d2fa0c:      	leaq	(%rdi,%rax), %r10
 7d2fa10:      	movl	0x4(%rsp), %r8d
 7d2fa15:      	jmp	0x7d2fa5b <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6eb>
 7d2fa17:      	nopw	(%rax,%rax)
 7d2fa20:      	movq	%r13, %rax
 7d2fa23:      	shlq	$0x7, %rax
 7d2fa27:      	leaq	(%rax,%r13,8), %rax
 7d2fa2b:      	cmpl	$0x0, 0x1c(%rcx,%rax)
 7d2fa30:      	cmovnel	%ebp, %r12d
 7d2fa34:      	addl	0x6c(%rcx,%rax), %r12d
 7d2fa39:      	addl	0x64(%rcx,%rax), %r12d
 7d2fa3e:      	incl	%r8d
 7d2fa41:      	cmpl	$0x0, 0x1c(%rcx,%r11)
 7d2fa47:      	cmovnel	%r15d, %r8d
 7d2fa4b:      	addl	%r12d, %r8d
 7d2fa4e:      	addq	$0x18, %rdi
 7d2fa52:      	cmpq	%r10, %rdi
 7d2fa55:      	je	0x7d2faf0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x780>
 7d2fa5b:      	movl	(%rdi), %r13d
 7d2fa5e:      	movl	0x8(%rdi), %eax
 7d2fa61:      	movq	%r13, %rdx
 7d2fa64:      	shlq	$0x7, %rdx
 7d2fa68:      	leaq	(%rdx,%r13,8), %r11
 7d2fa6c:      	xorl	%r12d, %r12d
 7d2fa6f:      	cmpl	%eax, %r13d
 7d2fa72:      	jae	0x7d2fa3e <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6ce>
 7d2fa74:      	leaq	-0x1(%rax), %rdx
 7d2fa78:      	xorl	%r12d, %r12d
 7d2fa7b:      	cmpq	%r13, %rdx
 7d2fa7e:      	je	0x7d2fa20 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6b0>
 7d2fa80:      	subq	%r13, %rax
 7d2fa83:      	leaq	0xf4(%rcx), %rdx
 7d2fa8a:      	addq	%r11, %rdx
 7d2fa8d:      	movq	%rax, %r15
 7d2fa90:      	andq	$-0x2, %r15
 7d2fa94:      	negq	%r15
 7d2fa97:      	xorl	%r12d, %r12d
 7d2fa9a:      	xorl	%r9d, %r9d
 7d2fa9d:      	nopl	(%rax)
 7d2faa0:      	cmpl	$0x0, -0xd8(%rdx)
 7d2faa7:      	cmovnel	%ebp, %r12d
 7d2faab:      	addl	-0x88(%rdx), %r12d
 7d2fab2:      	addl	-0x90(%rdx), %r12d
 7d2fab9:      	cmpl	$0x0, -0x50(%rdx)
 7d2fabd:      	cmovnel	%ebp, %r12d
 7d2fac1:      	addl	(%rdx), %r12d
 7d2fac4:      	addl	-0x8(%rdx), %r12d
 7d2fac8:      	addq	$0x110, %rdx            # imm = 0x110
 7d2facf:      	addq	$-0x2, %r9
 7d2fad3:      	cmpq	%r9, %r15
 7d2fad6:      	jne	0x7d2faa0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x730>
 7d2fad8:      	testb	$0x1, %al
 7d2fada:      	movl	$0x1, %r15d
 7d2fae0:      	je	0x7d2fa3e <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6ce>
 7d2fae6:      	subq	%r9, %r13
 7d2fae9:      	jmp	0x7d2fa20 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x6b0>
 7d2faee:      	nop
 7d2faf0:      	movl	0x4c(%rsp), %eax
 7d2faf4:      	subl	%r8d, %eax
 7d2faf7:      	jbe	0x7d2fb18 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x7a8>
 7d2faf9:      	movl	(%r14), %edx
 7d2fafc:      	movq	%rdx, %rdi
 7d2faff:      	shlq	$0x7, %rdi
 7d2fb03:      	leaq	(%rdi,%rdx,8), %rdx
 7d2fb07:      	movl	%eax, 0x64(%rcx,%rdx)
 7d2fb0b:      	movq	0x30(%rsp), %rax
 7d2fb10:      	movl	0x48(%rax), %eax
 7d2fb13:      	movq	%rax, 0x18(%rsp)
 7d2fb18:      	movq	0x10(%r14), %r14
 7d2fb1c:      	testq	%r14, %r14
 7d2fb1f:      	je	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fb25:      	incl	%esi
 7d2fb27:      	cmpl	%esi, 0x18(%rsp)
 7d2fb2b:      	ja	0x7d2f9f0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x680>
 7d2fb31:      	jmp	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fb36:      	cmpl	$0x0, 0x8(%rsp)
 7d2fb3b:      	movl	$0x1, %r9d
 7d2fb41:      	cmovel	0xc(%rsp), %r9d
 7d2fb47:      	subl	%eax, %r9d
 7d2fb4a:      	subl	%eax, %r9d
 7d2fb4d:      	addl	%esi, %r9d
 7d2fb50:      	subl	%r10d, %r9d
 7d2fb53:      	movl	%r9d, 0x64(%r8)
 7d2fb57:      	movl	%ecx, %edi
 7d2fb59:      	subl	%edx, %edi
 7d2fb5b:      	cmpl	$0x2, %edi
 7d2fb5e:      	jb	0x7d2fbb0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fb60:      	leal	0x1(%rdx), %edi
 7d2fb63:      	cmpl	%ecx, %edi
 7d2fb65:      	jae	0x7d2fbb0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fb67:      	movl	%edi, %edi
 7d2fb69:      	movl	%edx, %r9d
 7d2fb6c:      	subl	%ecx, %r9d
 7d2fb6f:      	testb	$0x1, %r9b
 7d2fb73:      	jne	0x7d2fb96 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x826>
 7d2fb75:      	movq	%rdi, %r9
 7d2fb78:      	shlq	$0x7, %r9
 7d2fb7c:      	leaq	(%r9,%rdi,8), %r9
 7d2fb80:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fb86:      	je	0x7d2fb93 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x823>
 7d2fb88:      	addq	%rbx, %r9
 7d2fb8b:      	movl	0x64(%r8), %r10d
 7d2fb8f:      	movl	%r10d, 0x64(%r9)
 7d2fb93:      	incq	%rdi
 7d2fb96:      	leal	-0x2(%rcx), %r9d
 7d2fb9a:      	cmpl	%edx, %r9d
 7d2fb9d:      	jne	0x7d2fd83 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa13>
 7d2fba3:      	nopw	%cs:(%rax,%rax)
 7d2fbad:      	nopl	(%rax)
 7d2fbb0:      	testq	%r14, %r14
 7d2fbb3:      	je	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fbb9:      	cmpl	$0x0, 0x8(%rsp)
 7d2fbbe:      	movl	$0x1, %ecx
 7d2fbc3:      	cmovel	0xc(%rsp), %ecx
 7d2fbc8:      	addl	%esi, %ecx
 7d2fbca:      	jmp	0x7d2fbdd <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x86d>
 7d2fbcc:      	nopl	(%rax)
 7d2fbd0:      	movq	0x10(%r14), %r14
 7d2fbd4:      	testq	%r14, %r14
 7d2fbd7:      	je	0x7d2f440 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xd0>
 7d2fbdd:      	movl	(%r14), %esi
 7d2fbe0:      	movl	0x8(%r14), %edx
 7d2fbe4:      	xorl	%r8d, %r8d
 7d2fbe7:      	cmpl	%esi, %edx
 7d2fbe9:      	jbe	0x7d2fc94 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x924>
 7d2fbef:      	leaq	-0x1(%rdx), %r9
 7d2fbf3:      	xorl	%r8d, %r8d
 7d2fbf6:      	movq	%rsi, %rdi
 7d2fbf9:      	cmpq	%rsi, %r9
 7d2fbfc:      	je	0x7d2fc76 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x906>
 7d2fc02:      	movq	%rdx, %rdi
 7d2fc05:      	subq	%rsi, %rdi
 7d2fc08:      	movq	%rsi, %r8
 7d2fc0b:      	shlq	$0x7, %r8
 7d2fc0f:      	leaq	(%r8,%rsi,8), %r10
 7d2fc13:      	leaq	0xf4(%rbx), %r8
 7d2fc1a:      	addq	%r8, %r10
 7d2fc1d:      	movq	%rdi, %r11
 7d2fc20:      	andq	$-0x2, %r11
 7d2fc24:      	negq	%r11
 7d2fc27:      	xorl	%r8d, %r8d
 7d2fc2a:      	xorl	%r9d, %r9d
 7d2fc2d:      	nopl	(%rax)
 7d2fc30:      	cmpl	$0x0, -0xd8(%r10)
 7d2fc38:      	cmovnel	%ebp, %r8d
 7d2fc3c:      	addl	-0x88(%r10), %r8d
 7d2fc43:      	addl	-0x90(%r10), %r8d
 7d2fc4a:      	cmpl	$0x0, -0x50(%r10)
 7d2fc4f:      	cmovnel	%ebp, %r8d
 7d2fc53:      	addl	(%r10), %r8d
 7d2fc56:      	addl	-0x8(%r10), %r8d
 7d2fc5a:      	addq	$0x110, %r10            # imm = 0x110
 7d2fc61:      	addq	$-0x2, %r9
 7d2fc65:      	cmpq	%r9, %r11
 7d2fc68:      	jne	0x7d2fc30 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x8c0>
 7d2fc6a:      	testb	$0x1, %dil
 7d2fc6e:      	je	0x7d2fc94 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x924>
 7d2fc70:      	movq	%rsi, %rdi
 7d2fc73:      	subq	%r9, %rdi
 7d2fc76:      	movq	%rdi, %r9
 7d2fc79:      	shlq	$0x7, %r9
 7d2fc7d:      	leaq	(%r9,%rdi,8), %rdi
 7d2fc81:      	cmpl	$0x0, 0x1c(%rbx,%rdi)
 7d2fc86:      	cmovnel	%ebp, %r8d
 7d2fc8a:      	addl	0x6c(%rbx,%rdi), %r8d
 7d2fc8f:      	addl	0x64(%rbx,%rdi), %r8d
 7d2fc94:      	movq	%rsi, %rdi
 7d2fc97:      	shlq	$0x7, %rdi
 7d2fc9b:      	leaq	(%rdi,%rsi,8), %r9
 7d2fc9f:      	leaq	(%rbx,%r9), %rdi
 7d2fca3:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fca9:      	je	0x7d2fcc0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x950>
 7d2fcab:      	movl	%edx, %r8d
 7d2fcae:      	subl	%esi, %r8d
 7d2fcb1:      	cmpl	$0x2, %r8d
 7d2fcb5:      	jb	0x7d2fbd0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fcbb:      	jmp	0x7d2fcdd <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x96d>
 7d2fcbd:      	nopl	(%rax)
 7d2fcc0:      	addl	%eax, %r8d
 7d2fcc3:      	movl	%ecx, %r9d
 7d2fcc6:      	subl	%r8d, %r9d
 7d2fcc9:      	movl	%r9d, 0x64(%rdi)
 7d2fccd:      	movl	%edx, %r8d
 7d2fcd0:      	subl	%esi, %r8d
 7d2fcd3:      	cmpl	$0x2, %r8d
 7d2fcd7:      	jb	0x7d2fbd0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fcdd:      	leal	0x1(%rsi), %r8d
 7d2fce1:      	cmpl	%edx, %r8d
 7d2fce4:      	jae	0x7d2fbd0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fcea:      	movl	%r8d, %r8d
 7d2fced:      	movl	%esi, %r9d
 7d2fcf0:      	subl	%edx, %r9d
 7d2fcf3:      	testb	$0x1, %r9b
 7d2fcf7:      	jne	0x7d2fd1a <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9aa>
 7d2fcf9:      	movq	%r8, %r9
 7d2fcfc:      	shlq	$0x7, %r9
 7d2fd00:      	leaq	(%r9,%r8,8), %r9
 7d2fd04:      	cmpl	$0x0, 0x1c(%rbx,%r9)
 7d2fd0a:      	je	0x7d2fd17 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9a7>
 7d2fd0c:      	addq	%rbx, %r9
 7d2fd0f:      	movl	0x64(%rdi), %r10d
 7d2fd13:      	movl	%r10d, 0x64(%r9)
 7d2fd17:      	incq	%r8
 7d2fd1a:      	leal	-0x2(%rdx), %r9d
 7d2fd1e:      	cmpl	%esi, %r9d
 7d2fd21:      	je	0x7d2fbd0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fd27:      	movq	%r8, %rsi
 7d2fd2a:      	shlq	$0x7, %rsi
 7d2fd2e:      	leaq	(%rsi,%r8,8), %rsi
 7d2fd32:      	leaq	0xec(%rbx), %r9
 7d2fd39:      	addq	%r9, %rsi
 7d2fd3c:      	subl	%r8d, %edx
 7d2fd3f:      	jmp	0x7d2fd60 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9f0>
 7d2fd41:      	nopw	%cs:(%rax,%rax)
 7d2fd4b:      	nopl	(%rax,%rax)
 7d2fd50:      	addq	$0x110, %rsi            # imm = 0x110
 7d2fd57:      	addl	$-0x2, %edx
 7d2fd5a:      	je	0x7d2fbd0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x860>
 7d2fd60:      	cmpl	$0x0, -0xd0(%rsi)
 7d2fd67:      	je	0x7d2fd74 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa04>
 7d2fd69:      	movl	0x64(%rdi), %r8d
 7d2fd6d:      	movl	%r8d, -0x88(%rsi)
 7d2fd74:      	cmpl	$0x0, -0x48(%rsi)
 7d2fd78:      	je	0x7d2fd50 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9e0>
 7d2fd7a:      	movl	0x64(%rdi), %r8d
 7d2fd7e:      	movl	%r8d, (%rsi)
 7d2fd81:      	jmp	0x7d2fd50 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x9e0>
 7d2fd83:      	movq	%rdi, %rdx
 7d2fd86:      	shlq	$0x7, %rdx
 7d2fd8a:      	leaq	(%rdx,%rdi,8), %rdx
 7d2fd8e:      	leaq	0xec(%rbx), %r9
 7d2fd95:      	addq	%r9, %rdx
 7d2fd98:      	subl	%edi, %ecx
 7d2fd9a:      	jmp	0x7d2fdb0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa40>
 7d2fd9c:      	nopl	(%rax)
 7d2fda0:      	addq	$0x110, %rdx            # imm = 0x110
 7d2fda7:      	addl	$-0x2, %ecx
 7d2fdaa:      	je	0x7d2fbb0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0x840>
 7d2fdb0:      	cmpl	$0x0, -0xd0(%rdx)
 7d2fdb7:      	je	0x7d2fdc3 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa53>
 7d2fdb9:      	movl	0x64(%r8), %edi
 7d2fdbd:      	movl	%edi, -0x88(%rdx)
 7d2fdc3:      	cmpl	$0x0, -0x48(%rdx)
 7d2fdc7:      	je	0x7d2fda0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa30>
 7d2fdc9:      	movl	0x64(%r8), %edi
 7d2fdcd:      	movl	%edi, (%rdx)
 7d2fdcf:      	jmp	0x7d2fda0 <_ZN5clang6format17WhitespaceManager36alignArrayInitializersRightJustifiedEONS1_16CellDescriptionsE+0xa30>
