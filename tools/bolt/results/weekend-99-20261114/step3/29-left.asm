
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000032663a0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_>:
 32663a0:      	pushq	%rbp
 32663a1:      	pushq	%r15
 32663a3:      	pushq	%r14
 32663a5:      	pushq	%r13
 32663a7:      	pushq	%r12
 32663a9:      	pushq	%rbx
 32663aa:      	subq	$0xf8, %rsp
 32663b1:      	movq	%rdx, (%rsp)
 32663b5:      	movq	%rdi, 0x20(%rsp)
 32663ba:      	movq	%rsi, 0x18(%rsp)
 32663bf:      	movl	0x8(%rsi), %eax
 32663c2:      	testq	%rax, %rax
 32663c5:      	sete	%sil
 32663c9:      	movq	%rcx, 0x8(%rsp)
 32663ce:      	testq	%rcx, %rcx
 32663d1:      	sete	%dl
 32663d4:      	orb	%sil, %dl
 32663d7:      	jne	0x32669b2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 32663dd:      	movq	0x18(%rsp), %rcx
 32663e2:      	movq	(%rcx), %rbx
 32663e5:      	leaq	(%rbx,%rax,8), %rax
 32663e9:      	movq	%rax, 0x10(%rsp)
 32663ee:      	leaq	0x60(%rsp), %rbp
 32663f3:      	movl	$0x3f60, %r15d          # imm = 0x3F60
 32663f9:      	nopl	(%rax)
 3266400:      	movq	(%rbx), %rax
 3266403:      	movb	$0x0, 0x28(%rsp)
 3266408:      	leaq	0x28(%rsp), %rcx
 326640d:      	movq	%rcx, 0x48(%rsp)
 3266412:      	movq	%rbp, 0x50(%rsp)
 3266417:      	movabsq	$0x800000000, %rcx      # imm = 0x800000000
 3266421:      	movq	%rcx, 0x58(%rsp)
 3266426:      	leaq	0xb8(%rsp), %rcx
 326642e:      	movq	%rcx, 0xa0(%rsp)
 3266436:      	movabsq	$0x100000008, %rcx      # imm = 0x100000008
 3266440:      	movq	%rcx, 0xa8(%rsp)
 3266448:      	movl	$0x0, 0xb0(%rsp)
 3266453:      	movb	$0x1, 0xb4(%rsp)
 326645b:      	movq	%rax, 0xb8(%rsp)
 3266463:      	cmpw	$0xf, 0x18(%rax)
 3266468:      	jne	0x3266480 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xe0>
 326646a:      	movb	$0x1, 0x28(%rsp)
 326646f:      	jmp	0x3266747 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3a7>
 3266474:      	nopw	%cs:(%rax,%rax)
 326647e:      	nop
 3266480:      	movq	%rax, 0x60(%rsp)
 3266485:      	movl	$0x1, 0x58(%rsp)
 326648d:      	movl	$0x1, %eax
 3266492:      	xorl	%ecx, %ecx
 3266494:      	jmp	0x32664aa <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 3266496:      	nopw	%cs:(%rax,%rax)
 32664a0:      	xorl	%ecx, %ecx
 32664a2:      	testl	%eax, %eax
 32664a4:      	je	0x3266730 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32664aa:      	testb	$0x1, %cl
 32664ad:      	jne	0x3266730 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32664b3:      	movq	0x50(%rsp), %rcx
 32664b8:      	movl	%eax, %edx
 32664ba:      	movq	-0x8(%rcx,%rdx,8), %r13
 32664bf:      	decl	%eax
 32664c1:      	movl	%eax, 0x58(%rsp)
 32664c5:      	movzwl	0x18(%r13), %ecx
 32664ca:      	leal	-0x2(%rcx), %edx
 32664cd:      	cmpw	$0xc, %dx
 32664d1:      	ja	0x32664a0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x100>
 32664d3:      	movl	$0x8, %eax
 32664d8:      	btl	%ecx, %r15d
 32664dc:      	jae	0x32664f6 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x156>
 32664de:      	movq	0x28(%r13), %rax
 32664e2:      	testq	%rax, %rax
 32664e5:      	je	0x3266707 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x367>
 32664eb:      	movq	0x20(%r13), %r13
 32664ef:      	leaq	(%r13,%rax,8), %r14
 32664f4:      	jmp	0x3266510 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x170>
 32664f6:      	movl	$0x401c, %edx           # imm = 0x401C
 32664fb:      	btl	%ecx, %edx
 32664fe:      	jae	0x3266717 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x377>
 3266504:      	leaq	0x20(%r13,%rax), %r14
 3266509:      	addq	$0x20, %r13
 326650d:      	nopl	(%rax)
 3266510:      	movq	(%r13), %r12
 3266514:      	movl	0xac(%rsp), %eax
 326651b:      	cmpb	$0x0, 0xb4(%rsp)
 3266523:      	je	0x32665a0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x200>
 3266525:      	movq	0xa0(%rsp), %rcx
 326652d:      	testq	%rax, %rax
 3266530:      	je	0x3266553 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1b3>
 3266532:      	leaq	(,%rax,8), %rdx
 326653a:      	xorl	%esi, %esi
 326653c:      	nopl	(%rax)
 3266540:      	cmpq	%r12, (%rcx,%rsi)
 3266544:      	je	0x326662f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326654a:      	addq	$0x8, %rsi
 326654e:      	cmpq	%rsi, %rdx
 3266551:      	jne	0x3266540 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1a0>
 3266553:      	movl	0xa8(%rsp), %esi
 326655a:      	cmpl	%esi, %eax
 326655c:      	jae	0x32665a7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x207>
 326655e:      	leal	0x1(%rax), %edx
 3266561:      	movl	%edx, 0xac(%rsp)
 3266568:      	movq	%r12, (%rcx,%rax,8)
 326656c:      	cmpw	$0xf, 0x18(%r12)
 3266573:      	je	0x3266627 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x287>
 3266579:      	movl	0x58(%rsp), %edx
 326657d:      	cmpl	0x5c(%rsp), %edx
 3266581:      	jae	0x32666c9 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x329>
 3266587:      	movq	0x50(%rsp), %rax
 326658c:      	movl	%edx, %ecx
 326658e:      	movq	%r12, (%rax,%rcx,8)
 3266592:      	incl	0x58(%rsp)
 3266596:      	jmp	0x326662f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326659b:      	nopl	(%rax,%rax)
 32665a0:      	movl	0xa8(%rsp), %esi
 32665a7:      	leal	(,%rax,4), %ecx
 32665ae:      	leal	(%rsi,%rsi,2), %edx
 32665b1:      	cmpl	%edx, %ecx
 32665b3:      	jae	0x32666a3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x303>
 32665b9:      	addl	0xb0(%rsp), %eax
 32665c0:      	movl	%esi, %ecx
 32665c2:      	subl	%eax, %ecx
 32665c4:      	movl	%esi, %eax
 32665c6:      	shrl	$0x3, %eax
 32665c9:      	cmpl	%eax, %ecx
 32665cb:      	jb	0x32666b0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x310>
 32665d1:      	movl	%r12d, %eax
 32665d4:      	shrl	$0x4, %eax
 32665d7:      	movl	%r12d, %ecx
 32665da:      	shrl	$0x9, %ecx
 32665dd:      	xorl	%eax, %ecx
 32665df:      	decl	%esi
 32665e1:      	movq	0xa0(%rsp), %rdx
 32665e9:      	andl	%esi, %ecx
 32665eb:      	leaq	(%rdx,%rcx,8), %rax
 32665ef:      	movq	(%rdx,%rcx,8), %r9
 32665f3:      	cmpq	$-0x1, %r9
 32665f7:      	jne	0x326666f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2cf>
 32665f9:      	xorl	%edi, %edi
 32665fb:      	testq	%rdi, %rdi
 32665fe:      	cmovneq	%rdi, %rax
 3266602:      	movq	(%rax), %rcx
 3266605:      	cmpq	%r12, %rcx
 3266608:      	je	0x326662f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326660a:      	cmpq	$-0x2, %rcx
 326660e:      	je	0x326664f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2af>
 3266610:      	incl	0xac(%rsp)
 3266617:      	movq	%r12, (%rax)
 326661a:      	cmpw	$0xf, 0x18(%r12)
 3266621:      	jne	0x3266579 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1d9>
 3266627:      	movq	0x48(%rsp), %rax
 326662c:      	movb	$0x1, (%rax)
 326662f:      	movq	0x48(%rsp), %rax
 3266634:      	cmpb	$0x1, (%rax)
 3266637:      	je	0x32666e7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x347>
 326663d:      	addq	$0x8, %r13
 3266641:      	cmpq	%r14, %r13
 3266644:      	jne	0x3266510 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x170>
 326664a:      	jmp	0x32666f7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x357>
 326664f:      	decl	0xb0(%rsp)
 3266656:      	incl	0xac(%rsp)
 326665d:      	movq	%r12, (%rax)
 3266660:      	cmpw	$0xf, 0x18(%r12)
 3266667:      	jne	0x3266579 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1d9>
 326666d:      	jmp	0x3266627 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x287>
 326666f:      	movl	$0x1, %r8d
 3266675:      	xorl	%edi, %edi
 3266677:      	cmpq	%r12, %r9
 326667a:      	je	0x326662f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326667c:      	xorq	$-0x2, %r9
 3266680:      	orq	%rdi, %r9
 3266683:      	cmoveq	%rax, %rdi
 3266687:      	addl	%r8d, %ecx
 326668a:      	incl	%r8d
 326668d:      	andl	%esi, %ecx
 326668f:      	leaq	(%rdx,%rcx,8), %rax
 3266693:      	movq	(%rdx,%rcx,8), %r9
 3266697:      	cmpq	$-0x1, %r9
 326669b:      	je	0x32665fb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x25b>
 32666a1:      	jmp	0x3266677 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2d7>
 32666a3:      	cmpl	$0x41, %esi
 32666a6:      	movl	$0x40, %eax
 32666ab:      	cmovbl	%eax, %esi
 32666ae:      	addl	%esi, %esi
 32666b0:      	leaq	0xa0(%rsp), %rdi
 32666b8:      	callq	0x40f7d50 <_ZN4llvm19SmallPtrSetImplBase4GrowEj>
 32666bd:      	movl	0xa8(%rsp), %esi
 32666c4:      	jmp	0x32665d1 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x231>
 32666c9:      	incq	%rdx
 32666cc:      	movl	$0x8, %ecx
 32666d1:      	leaq	0x50(%rsp), %rdi
 32666d6:      	movq	%rbp, %rsi
 32666d9:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 32666de:      	movl	0x58(%rsp), %edx
 32666e2:      	jmp	0x3266587 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1e7>
 32666e7:      	movb	$0x1, %cl
 32666e9:      	movl	0x58(%rsp), %eax
 32666ed:      	testl	%eax, %eax
 32666ef:      	jne	0x32664aa <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 32666f5:      	jmp	0x3266730 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32666f7:      	xorl	%ecx, %ecx
 32666f9:      	movl	0x58(%rsp), %eax
 32666fd:      	testl	%eax, %eax
 32666ff:      	jne	0x32664aa <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 3266705:      	jmp	0x3266730 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 3266707:      	xorl	%ecx, %ecx
 3266709:      	movl	0x58(%rsp), %eax
 326670d:      	testl	%eax, %eax
 326670f:      	jne	0x32664aa <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 3266715:      	jmp	0x3266730 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 3266717:      	movl	$0x10, %eax
 326671c:      	jmp	0x3266504 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x164>
 3266721:      	nopw	%cs:(%rax,%rax)
 326672b:      	nopl	(%rax,%rax)
 3266730:      	cmpb	$0x0, 0xb4(%rsp)
 3266738:      	jne	0x3266747 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3a7>
 326673a:      	movq	0xa0(%rsp), %rdi
 3266742:      	callq	0x828a6d0 <free@plt>
 3266747:      	movq	0x50(%rsp), %rdi
 326674c:      	cmpq	%rbp, %rdi
 326674f:      	je	0x3266756 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3b6>
 3266751:      	callq	0x828a6d0 <free@plt>
 3266756:      	cmpb	$0x1, 0x28(%rsp)
 326675b:      	je	0x3266771 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3d1>
 326675d:      	addq	$0x8, %rbx
 3266761:      	cmpq	0x10(%rsp), %rbx
 3266766:      	jne	0x3266400 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x60>
 326676c:      	jmp	0x32669b2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 3266771:      	movq	0x18(%rsp), %r15
 3266776:      	movl	0x8(%r15), %esi
 326677a:      	movq	(%r15), %r13
 326677d:      	cmpq	$0x2, %rsi
 3266781:      	jb	0x326679e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3fe>
 3266783:      	leaq	0x3a16(%rip), %rcx      # 0x326a1a0 <_ZN4llvm25array_pod_sort_comparatorIPKNS_4SCEVEEEiPKvS5_>
 326678a:      	movl	$0x8, %edx
 326678f:      	movq	%r13, %rdi
 3266792:      	callq	0x828a8a0 <qsort@plt>
 3266797:      	movq	(%r15), %r13
 326679a:      	movl	0x8(%r15), %esi
 326679e:      	movq	0x8(%rsp), %rbp
 32667a3:      	movl	%esi, %edi
 32667a5:      	leaq	(%r13,%rdi,8), %r14
 32667aa:      	testl	%esi, %esi
 32667ac:      	je	0x32667ff <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x45f>
 32667ae:      	shlq	$0x3, %rdi
 32667b2:      	addq	$-0x10, %rdi
 32667b6:      	leaq	0x8(%r13), %rax
 32667ba:      	nopw	(%rax,%rax)
 32667c0:      	cmpq	$-0x8, %rdi
 32667c4:      	je	0x32667ff <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x45f>
 32667c6:      	movq	-0x8(%rax), %rdx
 32667ca:      	addq	$-0x8, %rdi
 32667ce:      	leaq	0x8(%rax), %rcx
 32667d2:      	cmpq	(%rax), %rdx
 32667d5:      	movq	%rcx, %rax
 32667d8:      	jne	0x32667c0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x420>
 32667da:      	leaq	-0x10(%rcx), %rax
 32667de:      	cmpq	$-0x8, %rdi
 32667e2:      	je	0x32667f8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x458>
 32667e4:      	movl	%edi, %esi
 32667e6:      	notl	%esi
 32667e8:      	testb	$0x18, %sil
 32667ec:      	jne	0x3266cbe <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x91e>
 32667f2:      	cmpq	$0x18, %rdi
 32667f6:      	jae	0x3266869 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c9>
 32667f8:      	addq	$0x8, %rax
 32667fc:      	movq	%rax, %r14
 32667ff:      	subq	%r13, %r14
 3266802:      	shrq	$0x3, %r14
 3266806:      	movl	%r14d, 0x8(%r15)
 326680a:      	testl	%r14d, %r14d
 326680d:      	je	0x326697f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5df>
 3266813:      	movl	%r14d, %eax
 3266816:      	leaq	(%r13,%rax,8), %r12
 326681b:      	bsrq	%rax, %rdx
 326681f:      	xorl	$0x3f, %edx
 3266822:      	addl	%edx, %edx
 3266824:      	xorq	$0x7e, %rdx
 3266828:      	movq	%r13, %rdi
 326682b:      	movq	%r12, %rsi
 326682e:      	callq	0x326a1c0 <_ZSt16__introsort_loopIPPKN4llvm4SCEVElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_19findArrayDimensionsERNS0_15ScalarEvolutionERNS0_15SmallVectorImplIS3_EESC_S3_E3$_0EEEvT_SF_T0_T1_>
 3266833:      	leaq	0x8(%r13), %rbx
 3266837:      	cmpl	$0x11, %r14d
 326683b:      	jb	0x32668ae <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x50e>
 326683d:      	movq	%r12, 0x10(%rsp)
 3266842:      	movl	$0x8, %r12d
 3266848:      	movq	%rbx, %r14
 326684b:      	movq	%r13, %rbp
 326684e:      	jmp	0x3266d2b <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x98b>
 3266853:      	nopw	%cs:(%rax,%rax)
 326685d:      	nopl	(%rax)
 3266860:      	addq	$0x20, %rcx
 3266864:      	cmpq	%r14, %rcx
 3266867:      	je	0x32667f8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x458>
 3266869:      	movq	(%rcx), %rsi
 326686c:      	cmpq	%rsi, %rdx
 326686f:      	je	0x3266879 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4d9>
 3266871:      	movq	%rsi, 0x8(%rax)
 3266875:      	addq	$0x8, %rax
 3266879:      	movq	0x8(%rcx), %rdx
 326687d:      	cmpq	%rdx, %rsi
 3266880:      	je	0x326688a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4ea>
 3266882:      	movq	%rdx, 0x8(%rax)
 3266886:      	addq	$0x8, %rax
 326688a:      	movq	0x10(%rcx), %rsi
 326688e:      	cmpq	%rsi, %rdx
 3266891:      	je	0x326689b <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4fb>
 3266893:      	movq	%rsi, 0x8(%rax)
 3266897:      	addq	$0x8, %rax
 326689b:      	movq	0x18(%rcx), %rdx
 326689f:      	cmpq	%rdx, %rsi
 32668a2:      	je	0x3266860 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c0>
 32668a4:      	movq	%rdx, 0x8(%rax)
 32668a8:      	addq	$0x8, %rax
 32668ac:      	jmp	0x3266860 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c0>
 32668ae:      	cmpl	$0x1, %r14d
 32668b2:      	jne	0x3266b7c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7dc>
 32668b8:      	movl	0x8(%r15), %eax
 32668bc:      	testq	%rax, %rax
 32668bf:      	je	0x326697f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5df>
 32668c5:      	movq	(%r15), %r14
 32668c8:      	leaq	(%r14,%rax,8), %r15
 32668cc:      	leaq	0x48(%rsp), %rbx
 32668d1:      	leaq	0x28(%rsp), %r12
 32668d6:      	jmp	0x32668f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x550>
 32668d8:      	cmpq	$0x0, 0x18(%rdx)
 32668dd:      	je	0x32668e3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x543>
 32668df:      	nop
 32668e0:      	movq	%rax, (%r14)
 32668e3:      	addq	$0x8, %r14
 32668e7:      	cmpq	%r15, %r14
 32668ea:      	je	0x32669c4 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x624>
 32668f0:      	movq	(%r14), %rsi
 32668f3:      	movq	0x20(%rsp), %rdi
 32668f8:      	movq	%rbp, %rdx
 32668fb:      	movq	%rbx, %rcx
 32668fe:      	movq	%r12, %r8
 3266901:      	callq	0x33fd470 <_ZN4llvm12SCEVDivision6divideERNS_15ScalarEvolutionEPKNS_4SCEVES5_PS5_S6_>
 3266906:      	movq	0x48(%rsp), %rax
 326690b:      	cmpw	$0x0, 0x18(%rax)
 3266910:      	jne	0x32668e0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x540>
 3266912:      	movq	0x20(%rax), %rdx
 3266916:      	movl	0x20(%rdx), %ecx
 3266919:      	cmpq	$0x41, %rcx
 326691d:      	jb	0x32668d8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x538>
 326691f:      	leaq	0x3f(%rcx), %rsi
 3266923:      	shrq	$0x6, %rsi
 3266927:      	movq	0x18(%rdx), %r8
 326692b:      	movl	%esi, %edx
 326692d:      	shll	$0x6, %edx
 3266930:      	incq	%rsi
 3266933:      	xorl	%edi, %edi
 3266935:      	nopw	%cs:(%rax,%rax)
 326693f:      	nop
 3266940:      	movq	-0x10(%r8,%rsi,8), %r9
 3266945:      	testq	%r9, %r9
 3266948:      	jne	0x3266958 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5b8>
 326694a:      	addl	$0x40, %edi
 326694d:      	decq	%rsi
 3266950:      	cmpq	$0x1, %rsi
 3266954:      	ja	0x3266940 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5a0>
 3266956:      	jmp	0x3266961 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5c1>
 3266958:      	bsrq	%r9, %rdx
 326695c:      	xorl	$0x3f, %edx
 326695f:      	addl	%edi, %edx
 3266961:      	movl	%ecx, %esi
 3266963:      	andl	$0x3f, %esi
 3266966:      	movl	%ecx, %edi
 3266968:      	orl	$-0x40, %edi
 326696b:      	testl	%esi, %esi
 326696d:      	cmovel	%esi, %edi
 3266970:      	addl	%edx, %edi
 3266972:      	cmpl	%ecx, %edi
 3266974:      	jne	0x32668e0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x540>
 326697a:      	jmp	0x32668e3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x543>
 326697f:      	leaq	0x58(%rsp), %r15
 3266984:      	movq	%r15, 0x48(%rsp)
 3266989:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 3266993:      	movq	%rax, 0x50(%rsp)
 3266998:      	movq	(%rsp), %rbx
 326699c:      	movl	$0x0, 0x8(%rbx)
 32669a3:      	movq	0x48(%rsp), %rdi
 32669a8:      	cmpq	%r15, %rdi
 32669ab:      	je	0x32669b2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 32669ad:      	callq	0x828a6d0 <free@plt>
 32669b2:      	addq	$0xf8, %rsp
 32669b9:      	popq	%rbx
 32669ba:      	popq	%r12
 32669bc:      	popq	%r13
 32669be:      	popq	%r14
 32669c0:      	popq	%r15
 32669c2:      	popq	%rbp
 32669c3:      	retq
 32669c4:      	movq	0x18(%rsp), %rax
 32669c9:      	movq	(%rax), %r14
 32669cc:      	movl	0x8(%rax), %eax
 32669cf:      	leaq	0x58(%rsp), %r15
 32669d4:      	movq	%r15, 0x48(%rsp)
 32669d9:      	movabsq	$0x400000000, %rcx      # imm = 0x400000000
 32669e3:      	movq	%rcx, 0x50(%rsp)
 32669e8:      	testq	%rax, %rax
 32669eb:      	je	0x3266998 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5f8>
 32669ed:      	leaq	(%r14,%rax,8), %r15
 32669f1:      	leaq	0x38(%rsp), %rbx
 32669f6:      	movq	%r15, 0x10(%rsp)
 32669fb:      	jmp	0x3266a2a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x68a>
 32669fd:      	nopl	(%rax)
 3266a00:      	movl	0x50(%rsp), %edx
 3266a04:      	cmpl	0x54(%rsp), %edx
 3266a08:      	jae	0x3266afb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x75b>
 3266a0e:      	movq	0x48(%rsp), %rax
 3266a13:      	movl	%edx, %ecx
 3266a15:      	movq	%rbp, (%rax,%rcx,8)
 3266a19:      	incl	0x50(%rsp)
 3266a1d:      	addq	$0x8, %r14
 3266a21:      	cmpq	%r15, %r14
 3266a24:      	je	0x3266b1b <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x77b>
 3266a2a:      	movq	(%r14), %rbp
 3266a2d:      	movzwl	0x18(%rbp), %eax
 3266a31:      	testl	%eax, %eax
 3266a33:      	je	0x3266a1d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x67d>
 3266a35:      	cmpl	$0x6, %eax
 3266a38:      	jne	0x3266a00 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x660>
 3266a3a:      	movq	%rbx, %r15
 3266a3d:      	movq	%rbx, 0x28(%rsp)
 3266a42:      	movabsq	$0x200000000, %rax      # imm = 0x200000000
 3266a4c:      	movq	%rax, 0x30(%rsp)
 3266a51:      	movq	0x28(%rbp), %r13
 3266a55:      	testq	%r13, %r13
 3266a58:      	je	0x3266ac0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x720>
 3266a5a:      	movq	0x20(%rbp), %rbp
 3266a5e:      	shlq	$0x3, %r13
 3266a62:      	xorl	%eax, %eax
 3266a64:      	xorl	%r12d, %r12d
 3266a67:      	jmp	0x3266a8e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6ee>
 3266a69:      	nopl	(%rax)
 3266a70:      	movq	0x28(%rsp), %rcx
 3266a75:      	movl	%eax, %eax
 3266a77:      	movq	%rbx, (%rcx,%rax,8)
 3266a7b:      	movl	0x30(%rsp), %eax
 3266a7f:      	incl	%eax
 3266a81:      	movl	%eax, 0x30(%rsp)
 3266a85:      	addq	$0x8, %r12
 3266a89:      	cmpq	%r12, %r13
 3266a8c:      	je	0x3266ac0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x720>
 3266a8e:      	movq	(%rbp,%r12), %rbx
 3266a93:      	cmpw	$0x0, 0x18(%rbx)
 3266a98:      	je	0x3266a85 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6e5>
 3266a9a:      	cmpl	0x34(%rsp), %eax
 3266a9e:      	jb	0x3266a70 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6d0>
 3266aa0:      	movl	%eax, %edx
 3266aa2:      	incq	%rdx
 3266aa5:      	movl	$0x8, %ecx
 3266aaa:      	leaq	0x28(%rsp), %rdi
 3266aaf:      	movq	%r15, %rsi
 3266ab2:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266ab7:      	movl	0x30(%rsp), %eax
 3266abb:      	jmp	0x3266a70 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6d0>
 3266abd:      	nopl	(%rax)
 3266ac0:      	movq	0x20(%rsp), %rdi
 3266ac5:      	leaq	0x28(%rsp), %rsi
 3266aca:      	xorl	%edx, %edx
 3266acc:      	xorl	%ecx, %ecx
 3266ace:      	callq	0x33807a0 <_ZN4llvm15ScalarEvolution10getMulExprERNS_15SmallVectorImplIPKNS_4SCEVEEENS2_11NoWrapFlagsEj>
 3266ad3:      	movq	%rax, %rbp
 3266ad6:      	movq	0x28(%rsp), %rdi
 3266adb:      	movq	%r15, %rbx
 3266ade:      	cmpq	%r15, %rdi
 3266ae1:      	je	0x3266ae8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x748>
 3266ae3:      	callq	0x828a6d0 <free@plt>
 3266ae8:      	testq	%rbp, %rbp
 3266aeb:      	movq	0x10(%rsp), %r15
 3266af0:      	jne	0x3266a00 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x660>
 3266af6:      	jmp	0x3266a1d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x67d>
 3266afb:      	incq	%rdx
 3266afe:      	movl	$0x8, %ecx
 3266b03:      	leaq	0x48(%rsp), %rdi
 3266b08:      	leaq	0x58(%rsp), %rsi
 3266b0d:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266b12:      	movl	0x50(%rsp), %edx
 3266b16:      	jmp	0x3266a0e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x66e>
 3266b1b:      	cmpl	$0x0, 0x50(%rsp)
 3266b20:      	je	0x3266cf2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x952>
 3266b26:      	leaq	0x48(%rsp), %rsi
 3266b2b:      	movq	0x20(%rsp), %rdi
 3266b30:      	movq	(%rsp), %rbx
 3266b34:      	movq	%rbx, %rdx
 3266b37:      	callq	0x3266f30 <_ZL22findArrayDimensionsRecRN4llvm15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_>
 3266b3c:      	testb	%al, %al
 3266b3e:      	leaq	0x58(%rsp), %r15
 3266b43:      	je	0x326699c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5fc>
 3266b49:      	movl	0x8(%rbx), %edx
 3266b4c:      	cmpl	0xc(%rbx), %edx
 3266b4f:      	movq	%rbx, %rdi
 3266b52:      	jae	0x3266f0a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb6a>
 3266b58:      	movq	0x8(%rsp), %rsi
 3266b5d:      	movq	(%rdi), %rax
 3266b60:      	movl	%edx, %ecx
 3266b62:      	movq	%rsi, (%rax,%rcx,8)
 3266b66:      	incl	0x8(%rdi)
 3266b69:      	movq	0x48(%rsp), %rdi
 3266b6e:      	cmpq	%r15, %rdi
 3266b71:      	jne	0x32669ad <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x60d>
 3266b77:      	jmp	0x32669b2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 3266b7c:      	movq	%r13, %r14
 3266b7f:      	jmp	0x3266bcd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x82d>
 3266b81:      	nopw	%cs:(%rax,%rax)
 3266b8b:      	nopl	(%rax,%rax)
 3266b90:      	movq	%r14, %rdx
 3266b93:      	subq	%r13, %rdx
 3266b96:      	movq	%rdx, %rax
 3266b99:      	sarq	$0x3, %rax
 3266b9d:      	cmpq	$0x2, %rax
 3266ba1:      	jl	0x3266ca8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x908>
 3266ba7:      	shlq	$0x3, %rax
 3266bab:      	subq	%rax, %rdi
 3266bae:      	addq	$0x10, %rdi
 3266bb2:      	movq	%r13, %rsi
 3266bb5:      	callq	0x828ac50 <memmove@plt>
 3266bba:      	movq	%r13, %rax
 3266bbd:      	movq	%rbx, (%rax)
 3266bc0:      	leaq	0x8(%r14), %rbx
 3266bc4:      	cmpq	%r12, %rbx
 3266bc7:      	je	0x32668b8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x518>
 3266bcd:      	movq	%r14, %rdi
 3266bd0:      	movq	%rbx, %r14
 3266bd3:      	movq	(%rbx), %rbx
 3266bd6:      	cmpw	$0x6, 0x18(%rbx)
 3266bdb:      	setne	%cl
 3266bde:      	testq	%rbx, %rbx
 3266be1:      	sete	%al
 3266be4:      	orb	%cl, %al
 3266be6:      	movl	$0x1, %edx
 3266beb:      	movl	$0x1, %esi
 3266bf0:      	jne	0x3266bf5 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x855>
 3266bf2:      	movl	0x28(%rbx), %esi
 3266bf5:      	movq	(%r13), %rcx
 3266bf9:      	testq	%rcx, %rcx
 3266bfc:      	je	0x3266c08 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x868>
 3266bfe:      	cmpw	$0x6, 0x18(%rcx)
 3266c03:      	jne	0x3266c08 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x868>
 3266c05:      	movl	0x28(%rcx), %edx
 3266c08:      	cmpl	%edx, %esi
 3266c0a:      	jg	0x3266b90 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7f0>
 3266c0c:      	testb	%al, %al
 3266c0e:      	je	0x3266c60 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8c0>
 3266c10:      	movq	-0x8(%r14), %rcx
 3266c14:      	movq	%r14, %rax
 3266c17:      	testq	%rcx, %rcx
 3266c1a:      	je	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c1c:      	cmpw	$0x6, 0x18(%rcx)
 3266c21:      	movq	%r14, %rax
 3266c24:      	jne	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c26:      	movq	%r14, %rax
 3266c29:      	nopl	(%rax)
 3266c30:      	cmpl	$0x0, 0x28(%rcx)
 3266c34:      	jg	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c36:      	movq	%rcx, (%rax)
 3266c39:      	movq	-0x10(%rax), %rcx
 3266c3d:      	addq	$-0x8, %rax
 3266c41:      	testq	%rcx, %rcx
 3266c44:      	je	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c4a:      	cmpw	$0x6, 0x18(%rcx)
 3266c4f:      	je	0x3266c30 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x890>
 3266c51:      	jmp	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c56:      	nopw	%cs:(%rax,%rax)
 3266c60:      	movl	0x28(%rbx), %ecx
 3266c63:      	movq	%r14, %rax
 3266c66:      	movq	-0x8(%rax), %rdx
 3266c6a:      	movl	$0x1, %esi
 3266c6f:      	testq	%rdx, %rdx
 3266c72:      	jne	0x3266c95 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8f5>
 3266c74:      	jmp	0x3266c9f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c76:      	nopw	%cs:(%rax,%rax)
 3266c80:      	movq	%rdx, (%rax)
 3266c83:      	addq	$-0x8, %rax
 3266c87:      	movq	-0x8(%rax), %rdx
 3266c8b:      	movl	$0x1, %esi
 3266c90:      	testq	%rdx, %rdx
 3266c93:      	je	0x3266c9f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c95:      	cmpw	$0x6, 0x18(%rdx)
 3266c9a:      	jne	0x3266c9f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c9c:      	movl	0x28(%rdx), %esi
 3266c9f:      	cmpl	%ecx, %esi
 3266ca1:      	jl	0x3266c80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8e0>
 3266ca3:      	jmp	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266ca8:      	movq	%r13, %rax
 3266cab:      	cmpq	$0x8, %rdx
 3266caf:      	jne	0x3266bbd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266cb5:      	movq	%rcx, 0x8(%rdi)
 3266cb9:      	jmp	0x3266bba <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81a>
 3266cbe:      	movl	%edi, %esi
 3266cc0:      	shrb	$0x3, %sil
 3266cc4:      	incb	%sil
 3266cc7:      	movzbl	%sil, %esi
 3266ccb:      	andl	$0x3, %esi
 3266cce:      	jmp	0x3266cdd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x93d>
 3266cd0:      	addq	$0x8, %rcx
 3266cd4:      	decq	%rsi
 3266cd7:      	je	0x32667f2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x452>
 3266cdd:      	movq	%rdx, %r8
 3266ce0:      	movq	(%rcx), %rdx
 3266ce3:      	cmpq	%rdx, %r8
 3266ce6:      	je	0x3266cd0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x930>
 3266ce8:      	movq	%rdx, 0x8(%rax)
 3266cec:      	addq	$0x8, %rax
 3266cf0:      	jmp	0x3266cd0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x930>
 3266cf2:      	movq	(%rsp), %rbx
 3266cf6:      	leaq	0x58(%rsp), %r15
 3266cfb:      	jmp	0x326699c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5fc>
 3266d00:      	movq	%rdx, 0x8(%rax)
 3266d04:      	nopw	%cs:(%rax,%rax)
 3266d0e:      	nop
 3266d10:      	movq	%r13, %rax
 3266d13:      	movq	%r15, (%rax)
 3266d16:      	addq	$0x8, %r12
 3266d1a:      	addq	$0x8, %r14
 3266d1e:      	cmpq	$0x80, %r12
 3266d25:      	je	0x3266e38 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa98>
 3266d2b:      	movq	%rbp, %rax
 3266d2e:      	movq	(%r13,%r12), %r15
 3266d33:      	cmpw	$0x6, 0x18(%r15)
 3266d39:      	setne	%dl
 3266d3c:      	testq	%r15, %r15
 3266d3f:      	sete	%cl
 3266d42:      	orb	%dl, %cl
 3266d44:      	movl	$0x1, %esi
 3266d49:      	movl	$0x1, %edi
 3266d4e:      	jne	0x3266d54 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9b4>
 3266d50:      	movl	0x28(%r15), %edi
 3266d54:      	movq	(%r13), %rdx
 3266d58:      	testq	%rdx, %rdx
 3266d5b:      	je	0x3266d67 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9c7>
 3266d5d:      	cmpw	$0x6, 0x18(%rdx)
 3266d62:      	jne	0x3266d67 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9c7>
 3266d64:      	movl	0x28(%rdx), %esi
 3266d67:      	leaq	(%r13,%r12), %rbp
 3266d6c:      	cmpl	%esi, %edi
 3266d6e:      	jle	0x3266d90 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9f0>
 3266d70:      	cmpq	$0x9, %r12
 3266d74:      	jb	0x3266d00 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x960>
 3266d76:      	movq	%rbx, %rdi
 3266d79:      	movq	%r13, %rsi
 3266d7c:      	movq	%r12, %rdx
 3266d7f:      	callq	0x828ac50 <memmove@plt>
 3266d84:      	jmp	0x3266d10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x970>
 3266d86:      	nopw	%cs:(%rax,%rax)
 3266d90:      	testb	%cl, %cl
 3266d92:      	je	0x3266df0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa50>
 3266d94:      	movq	-0x8(%rbp), %rcx
 3266d98:      	movq	%rbp, %rax
 3266d9b:      	testq	%rcx, %rcx
 3266d9e:      	je	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266da4:      	cmpw	$0x6, 0x18(%rcx)
 3266da9:      	movq	%rbp, %rax
 3266dac:      	jne	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266db2:      	movq	%r14, %rax
 3266db5:      	nopw	%cs:(%rax,%rax)
 3266dbf:      	nop
 3266dc0:      	cmpl	$0x0, 0x28(%rcx)
 3266dc4:      	jg	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266dca:      	movq	%rcx, (%rax)
 3266dcd:      	movq	-0x10(%rax), %rcx
 3266dd1:      	addq	$-0x8, %rax
 3266dd5:      	testq	%rcx, %rcx
 3266dd8:      	je	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266dde:      	cmpw	$0x6, 0x18(%rcx)
 3266de3:      	je	0x3266dc0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa20>
 3266de5:      	jmp	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266dea:      	nopw	(%rax,%rax)
 3266df0:      	movl	0x28(%r15), %ecx
 3266df4:      	movq	%rbp, %rax
 3266df7:      	movq	-0x8(%rax), %rdx
 3266dfb:      	movl	$0x1, %esi
 3266e00:      	testq	%rdx, %rdx
 3266e03:      	jne	0x3266e25 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa85>
 3266e05:      	jmp	0x3266e2f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266e07:      	nopw	(%rax,%rax)
 3266e10:      	movq	%rdx, (%rax)
 3266e13:      	addq	$-0x8, %rax
 3266e17:      	movq	-0x8(%rax), %rdx
 3266e1b:      	movl	$0x1, %esi
 3266e20:      	testq	%rdx, %rdx
 3266e23:      	je	0x3266e2f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266e25:      	cmpw	$0x6, 0x18(%rdx)
 3266e2a:      	jne	0x3266e2f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266e2c:      	movl	0x28(%rdx), %esi
 3266e2f:      	cmpl	%ecx, %esi
 3266e31:      	jl	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa70>
 3266e33:      	jmp	0x3266d13 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266e38:      	subq	$-0x80, %r13
 3266e3c:      	movq	0x8(%rsp), %rbp
 3266e41:      	movq	0x18(%rsp), %r15
 3266e46:      	movq	0x10(%rsp), %r8
 3266e4b:      	jmp	0x3266e60 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xac0>
 3266e4d:      	nopl	(%rax)
 3266e50:      	movq	%rax, (%rcx)
 3266e53:      	addq	$0x8, %r13
 3266e57:      	cmpq	%r8, %r13
 3266e5a:      	je	0x32668b8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x518>
 3266e60:      	movq	(%r13), %rax
 3266e64:      	testq	%rax, %rax
 3266e67:      	je	0x3266ec0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb20>
 3266e69:      	cmpw	$0x6, 0x18(%rax)
 3266e6e:      	jne	0x3266ec0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb20>
 3266e70:      	movl	0x28(%rax), %edx
 3266e73:      	movq	%r13, %rcx
 3266e76:      	movq	-0x8(%rcx), %rsi
 3266e7a:      	movl	$0x1, %edi
 3266e7f:      	testq	%rsi, %rsi
 3266e82:      	jne	0x3266ea5 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb05>
 3266e84:      	jmp	0x3266eaf <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266e86:      	nopw	%cs:(%rax,%rax)
 3266e90:      	movq	%rsi, (%rcx)
 3266e93:      	addq	$-0x8, %rcx
 3266e97:      	movq	-0x8(%rcx), %rsi
 3266e9b:      	movl	$0x1, %edi
 3266ea0:      	testq	%rsi, %rsi
 3266ea3:      	je	0x3266eaf <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266ea5:      	cmpw	$0x6, 0x18(%rsi)
 3266eaa:      	jne	0x3266eaf <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266eac:      	movl	0x28(%rsi), %edi
 3266eaf:      	cmpl	%edx, %edi
 3266eb1:      	jl	0x3266e90 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xaf0>
 3266eb3:      	jmp	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266eb5:      	nopw	%cs:(%rax,%rax)
 3266ebf:      	nop
 3266ec0:      	movq	-0x8(%r13), %rdx
 3266ec4:      	movq	%r13, %rcx
 3266ec7:      	testq	%rdx, %rdx
 3266eca:      	je	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266ecc:      	cmpw	$0x6, 0x18(%rdx)
 3266ed1:      	movq	%r13, %rcx
 3266ed4:      	jne	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266eda:      	movq	%r13, %rcx
 3266edd:      	nopl	(%rax)
 3266ee0:      	cmpl	$0x0, 0x28(%rdx)
 3266ee4:      	jg	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266eea:      	movq	%rdx, (%rcx)
 3266eed:      	movq	-0x10(%rcx), %rdx
 3266ef1:      	addq	$-0x8, %rcx
 3266ef5:      	testq	%rdx, %rdx
 3266ef8:      	je	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266efe:      	cmpw	$0x6, 0x18(%rdx)
 3266f03:      	je	0x3266ee0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb40>
 3266f05:      	jmp	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266f0a:      	incq	%rdx
 3266f0d:      	leaq	0x10(%rdi), %rsi
 3266f11:      	movl	$0x8, %ecx
 3266f16:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266f1b:      	movq	(%rsp), %rdi
 3266f1f:      	movl	0x8(%rdi), %edx
 3266f22:      	jmp	0x3266b58 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7b8>
