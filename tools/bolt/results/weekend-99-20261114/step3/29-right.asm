
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003266360 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_>:
 3266360:      	pushq	%rbp
 3266361:      	pushq	%r15
 3266363:      	pushq	%r14
 3266365:      	pushq	%r13
 3266367:      	pushq	%r12
 3266369:      	pushq	%rbx
 326636a:      	subq	$0xf8, %rsp
 3266371:      	movq	%rdx, (%rsp)
 3266375:      	movq	%rdi, 0x20(%rsp)
 326637a:      	movq	%rsi, 0x18(%rsp)
 326637f:      	movl	0x8(%rsi), %eax
 3266382:      	testq	%rax, %rax
 3266385:      	sete	%sil
 3266389:      	movq	%rcx, 0x8(%rsp)
 326638e:      	testq	%rcx, %rcx
 3266391:      	sete	%dl
 3266394:      	orb	%sil, %dl
 3266397:      	jne	0x3266972 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 326639d:      	movq	0x18(%rsp), %rcx
 32663a2:      	movq	(%rcx), %rbx
 32663a5:      	leaq	(%rbx,%rax,8), %rax
 32663a9:      	movq	%rax, 0x10(%rsp)
 32663ae:      	leaq	0x60(%rsp), %rbp
 32663b3:      	movl	$0x3f60, %r15d          # imm = 0x3F60
 32663b9:      	nopl	(%rax)
 32663c0:      	movq	(%rbx), %rax
 32663c3:      	movb	$0x0, 0x28(%rsp)
 32663c8:      	leaq	0x28(%rsp), %rcx
 32663cd:      	movq	%rcx, 0x48(%rsp)
 32663d2:      	movq	%rbp, 0x50(%rsp)
 32663d7:      	movabsq	$0x800000000, %rcx      # imm = 0x800000000
 32663e1:      	movq	%rcx, 0x58(%rsp)
 32663e6:      	leaq	0xb8(%rsp), %rcx
 32663ee:      	movq	%rcx, 0xa0(%rsp)
 32663f6:      	movabsq	$0x100000008, %rcx      # imm = 0x100000008
 3266400:      	movq	%rcx, 0xa8(%rsp)
 3266408:      	movl	$0x0, 0xb0(%rsp)
 3266413:      	movb	$0x1, 0xb4(%rsp)
 326641b:      	movq	%rax, 0xb8(%rsp)
 3266423:      	cmpw	$0xf, 0x18(%rax)
 3266428:      	jne	0x3266440 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xe0>
 326642a:      	movb	$0x1, 0x28(%rsp)
 326642f:      	jmp	0x3266707 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3a7>
 3266434:      	nopw	%cs:(%rax,%rax)
 326643e:      	nop
 3266440:      	movq	%rax, 0x60(%rsp)
 3266445:      	movl	$0x1, 0x58(%rsp)
 326644d:      	movl	$0x1, %eax
 3266452:      	xorl	%ecx, %ecx
 3266454:      	jmp	0x326646a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 3266456:      	nopw	%cs:(%rax,%rax)
 3266460:      	xorl	%ecx, %ecx
 3266462:      	testl	%eax, %eax
 3266464:      	je	0x32666f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 326646a:      	testb	$0x1, %cl
 326646d:      	jne	0x32666f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 3266473:      	movq	0x50(%rsp), %rcx
 3266478:      	movl	%eax, %edx
 326647a:      	movq	-0x8(%rcx,%rdx,8), %r13
 326647f:      	decl	%eax
 3266481:      	movl	%eax, 0x58(%rsp)
 3266485:      	movzwl	0x18(%r13), %ecx
 326648a:      	leal	-0x2(%rcx), %edx
 326648d:      	cmpw	$0xc, %dx
 3266491:      	ja	0x3266460 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x100>
 3266493:      	movl	$0x8, %eax
 3266498:      	btl	%ecx, %r15d
 326649c:      	jae	0x32664b6 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x156>
 326649e:      	movq	0x28(%r13), %rax
 32664a2:      	testq	%rax, %rax
 32664a5:      	je	0x32666c7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x367>
 32664ab:      	movq	0x20(%r13), %r13
 32664af:      	leaq	(%r13,%rax,8), %r14
 32664b4:      	jmp	0x32664d0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x170>
 32664b6:      	movl	$0x401c, %edx           # imm = 0x401C
 32664bb:      	btl	%ecx, %edx
 32664be:      	jae	0x32666d7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x377>
 32664c4:      	leaq	0x20(%r13,%rax), %r14
 32664c9:      	addq	$0x20, %r13
 32664cd:      	nopl	(%rax)
 32664d0:      	movq	(%r13), %r12
 32664d4:      	movl	0xac(%rsp), %eax
 32664db:      	cmpb	$0x0, 0xb4(%rsp)
 32664e3:      	je	0x3266560 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x200>
 32664e5:      	movq	0xa0(%rsp), %rcx
 32664ed:      	testq	%rax, %rax
 32664f0:      	je	0x3266513 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1b3>
 32664f2:      	leaq	(,%rax,8), %rdx
 32664fa:      	xorl	%esi, %esi
 32664fc:      	nopl	(%rax)
 3266500:      	cmpq	%r12, (%rcx,%rsi)
 3266504:      	je	0x32665ef <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326650a:      	addq	$0x8, %rsi
 326650e:      	cmpq	%rsi, %rdx
 3266511:      	jne	0x3266500 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1a0>
 3266513:      	movl	0xa8(%rsp), %esi
 326651a:      	cmpl	%esi, %eax
 326651c:      	jae	0x3266567 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x207>
 326651e:      	leal	0x1(%rax), %edx
 3266521:      	movl	%edx, 0xac(%rsp)
 3266528:      	movq	%r12, (%rcx,%rax,8)
 326652c:      	cmpw	$0xf, 0x18(%r12)
 3266533:      	je	0x32665e7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x287>
 3266539:      	movl	0x58(%rsp), %edx
 326653d:      	cmpl	0x5c(%rsp), %edx
 3266541:      	jae	0x3266689 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x329>
 3266547:      	movq	0x50(%rsp), %rax
 326654c:      	movl	%edx, %ecx
 326654e:      	movq	%r12, (%rax,%rcx,8)
 3266552:      	incl	0x58(%rsp)
 3266556:      	jmp	0x32665ef <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326655b:      	nopl	(%rax,%rax)
 3266560:      	movl	0xa8(%rsp), %esi
 3266567:      	leal	(,%rax,4), %ecx
 326656e:      	leal	(%rsi,%rsi,2), %edx
 3266571:      	cmpl	%edx, %ecx
 3266573:      	jae	0x3266663 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x303>
 3266579:      	addl	0xb0(%rsp), %eax
 3266580:      	movl	%esi, %ecx
 3266582:      	subl	%eax, %ecx
 3266584:      	movl	%esi, %eax
 3266586:      	shrl	$0x3, %eax
 3266589:      	cmpl	%eax, %ecx
 326658b:      	jb	0x3266670 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x310>
 3266591:      	movl	%r12d, %eax
 3266594:      	shrl	$0x4, %eax
 3266597:      	movl	%r12d, %ecx
 326659a:      	shrl	$0x9, %ecx
 326659d:      	xorl	%eax, %ecx
 326659f:      	decl	%esi
 32665a1:      	movq	0xa0(%rsp), %rdx
 32665a9:      	andl	%esi, %ecx
 32665ab:      	leaq	(%rdx,%rcx,8), %rax
 32665af:      	movq	(%rdx,%rcx,8), %r9
 32665b3:      	cmpq	$-0x1, %r9
 32665b7:      	jne	0x326662f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2cf>
 32665b9:      	xorl	%edi, %edi
 32665bb:      	testq	%rdi, %rdi
 32665be:      	cmovneq	%rdi, %rax
 32665c2:      	movq	(%rax), %rcx
 32665c5:      	cmpq	%r12, %rcx
 32665c8:      	je	0x32665ef <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 32665ca:      	cmpq	$-0x2, %rcx
 32665ce:      	je	0x326660f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2af>
 32665d0:      	incl	0xac(%rsp)
 32665d7:      	movq	%r12, (%rax)
 32665da:      	cmpw	$0xf, 0x18(%r12)
 32665e1:      	jne	0x3266539 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1d9>
 32665e7:      	movq	0x48(%rsp), %rax
 32665ec:      	movb	$0x1, (%rax)
 32665ef:      	movq	0x48(%rsp), %rax
 32665f4:      	cmpb	$0x1, (%rax)
 32665f7:      	je	0x32666a7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x347>
 32665fd:      	addq	$0x8, %r13
 3266601:      	cmpq	%r14, %r13
 3266604:      	jne	0x32664d0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x170>
 326660a:      	jmp	0x32666b7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x357>
 326660f:      	decl	0xb0(%rsp)
 3266616:      	incl	0xac(%rsp)
 326661d:      	movq	%r12, (%rax)
 3266620:      	cmpw	$0xf, 0x18(%r12)
 3266627:      	jne	0x3266539 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1d9>
 326662d:      	jmp	0x32665e7 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x287>
 326662f:      	movl	$0x1, %r8d
 3266635:      	xorl	%edi, %edi
 3266637:      	cmpq	%r12, %r9
 326663a:      	je	0x32665ef <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x28f>
 326663c:      	xorq	$-0x2, %r9
 3266640:      	orq	%rdi, %r9
 3266643:      	cmoveq	%rax, %rdi
 3266647:      	addl	%r8d, %ecx
 326664a:      	incl	%r8d
 326664d:      	andl	%esi, %ecx
 326664f:      	leaq	(%rdx,%rcx,8), %rax
 3266653:      	movq	(%rdx,%rcx,8), %r9
 3266657:      	cmpq	$-0x1, %r9
 326665b:      	je	0x32665bb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x25b>
 3266661:      	jmp	0x3266637 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x2d7>
 3266663:      	cmpl	$0x41, %esi
 3266666:      	movl	$0x40, %eax
 326666b:      	cmovbl	%eax, %esi
 326666e:      	addl	%esi, %esi
 3266670:      	leaq	0xa0(%rsp), %rdi
 3266678:      	callq	0x40f7cc0 <_ZN4llvm19SmallPtrSetImplBase4GrowEj>
 326667d:      	movl	0xa8(%rsp), %esi
 3266684:      	jmp	0x3266591 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x231>
 3266689:      	incq	%rdx
 326668c:      	movl	$0x8, %ecx
 3266691:      	leaq	0x50(%rsp), %rdi
 3266696:      	movq	%rbp, %rsi
 3266699:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 326669e:      	movl	0x58(%rsp), %edx
 32666a2:      	jmp	0x3266547 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x1e7>
 32666a7:      	movb	$0x1, %cl
 32666a9:      	movl	0x58(%rsp), %eax
 32666ad:      	testl	%eax, %eax
 32666af:      	jne	0x326646a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 32666b5:      	jmp	0x32666f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32666b7:      	xorl	%ecx, %ecx
 32666b9:      	movl	0x58(%rsp), %eax
 32666bd:      	testl	%eax, %eax
 32666bf:      	jne	0x326646a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 32666c5:      	jmp	0x32666f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32666c7:      	xorl	%ecx, %ecx
 32666c9:      	movl	0x58(%rsp), %eax
 32666cd:      	testl	%eax, %eax
 32666cf:      	jne	0x326646a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x10a>
 32666d5:      	jmp	0x32666f0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x390>
 32666d7:      	movl	$0x10, %eax
 32666dc:      	jmp	0x32664c4 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x164>
 32666e1:      	nopw	%cs:(%rax,%rax)
 32666eb:      	nopl	(%rax,%rax)
 32666f0:      	cmpb	$0x0, 0xb4(%rsp)
 32666f8:      	jne	0x3266707 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3a7>
 32666fa:      	movq	0xa0(%rsp), %rdi
 3266702:      	callq	0x828a640 <free@plt>
 3266707:      	movq	0x50(%rsp), %rdi
 326670c:      	cmpq	%rbp, %rdi
 326670f:      	je	0x3266716 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3b6>
 3266711:      	callq	0x828a640 <free@plt>
 3266716:      	cmpb	$0x1, 0x28(%rsp)
 326671b:      	je	0x3266731 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3d1>
 326671d:      	addq	$0x8, %rbx
 3266721:      	cmpq	0x10(%rsp), %rbx
 3266726:      	jne	0x32663c0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x60>
 326672c:      	jmp	0x3266972 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 3266731:      	movq	0x18(%rsp), %r15
 3266736:      	movl	0x8(%r15), %esi
 326673a:      	movq	(%r15), %r13
 326673d:      	cmpq	$0x2, %rsi
 3266741:      	jb	0x326675e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x3fe>
 3266743:      	leaq	0x3a16(%rip), %rcx      # 0x326a160 <_ZN4llvm25array_pod_sort_comparatorIPKNS_4SCEVEEEiPKvS5_>
 326674a:      	movl	$0x8, %edx
 326674f:      	movq	%r13, %rdi
 3266752:      	callq	0x828a810 <qsort@plt>
 3266757:      	movq	(%r15), %r13
 326675a:      	movl	0x8(%r15), %esi
 326675e:      	movq	0x8(%rsp), %rbp
 3266763:      	movl	%esi, %edi
 3266765:      	leaq	(%r13,%rdi,8), %r14
 326676a:      	testl	%esi, %esi
 326676c:      	je	0x32667bf <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x45f>
 326676e:      	shlq	$0x3, %rdi
 3266772:      	addq	$-0x10, %rdi
 3266776:      	leaq	0x8(%r13), %rax
 326677a:      	nopw	(%rax,%rax)
 3266780:      	cmpq	$-0x8, %rdi
 3266784:      	je	0x32667bf <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x45f>
 3266786:      	movq	-0x8(%rax), %rdx
 326678a:      	addq	$-0x8, %rdi
 326678e:      	leaq	0x8(%rax), %rcx
 3266792:      	cmpq	(%rax), %rdx
 3266795:      	movq	%rcx, %rax
 3266798:      	jne	0x3266780 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x420>
 326679a:      	leaq	-0x10(%rcx), %rax
 326679e:      	cmpq	$-0x8, %rdi
 32667a2:      	je	0x32667b8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x458>
 32667a4:      	movl	%edi, %esi
 32667a6:      	notl	%esi
 32667a8:      	testb	$0x18, %sil
 32667ac:      	jne	0x3266c7e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x91e>
 32667b2:      	cmpq	$0x18, %rdi
 32667b6:      	jae	0x3266829 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c9>
 32667b8:      	addq	$0x8, %rax
 32667bc:      	movq	%rax, %r14
 32667bf:      	subq	%r13, %r14
 32667c2:      	shrq	$0x3, %r14
 32667c6:      	movl	%r14d, 0x8(%r15)
 32667ca:      	testl	%r14d, %r14d
 32667cd:      	je	0x326693f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5df>
 32667d3:      	movl	%r14d, %eax
 32667d6:      	leaq	(%r13,%rax,8), %r12
 32667db:      	bsrq	%rax, %rdx
 32667df:      	xorl	$0x3f, %edx
 32667e2:      	addl	%edx, %edx
 32667e4:      	xorq	$0x7e, %rdx
 32667e8:      	movq	%r13, %rdi
 32667eb:      	movq	%r12, %rsi
 32667ee:      	callq	0x326a180 <_ZSt16__introsort_loopIPPKN4llvm4SCEVElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_19findArrayDimensionsERNS0_15ScalarEvolutionERNS0_15SmallVectorImplIS3_EESC_S3_E3$_0EEEvT_SF_T0_T1_>
 32667f3:      	leaq	0x8(%r13), %rbx
 32667f7:      	cmpl	$0x11, %r14d
 32667fb:      	jb	0x326686e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x50e>
 32667fd:      	movq	%r12, 0x10(%rsp)
 3266802:      	leaq	0x8(%r13), %r14
 3266806:      	movl	$0x8, %r12d
 326680c:      	movq	%r13, %rbp
 326680f:      	jmp	0x3266ceb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x98b>
 3266814:      	nopw	%cs:(%rax,%rax)
 326681e:      	nop
 3266820:      	addq	$0x20, %rcx
 3266824:      	cmpq	%r14, %rcx
 3266827:      	je	0x32667b8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x458>
 3266829:      	movq	(%rcx), %rsi
 326682c:      	cmpq	%rsi, %rdx
 326682f:      	je	0x3266839 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4d9>
 3266831:      	movq	%rsi, 0x8(%rax)
 3266835:      	addq	$0x8, %rax
 3266839:      	movq	0x8(%rcx), %rdx
 326683d:      	cmpq	%rdx, %rsi
 3266840:      	je	0x326684a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4ea>
 3266842:      	movq	%rdx, 0x8(%rax)
 3266846:      	addq	$0x8, %rax
 326684a:      	movq	0x10(%rcx), %rsi
 326684e:      	cmpq	%rsi, %rdx
 3266851:      	je	0x326685b <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4fb>
 3266853:      	movq	%rsi, 0x8(%rax)
 3266857:      	addq	$0x8, %rax
 326685b:      	movq	0x18(%rcx), %rdx
 326685f:      	cmpq	%rdx, %rsi
 3266862:      	je	0x3266820 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c0>
 3266864:      	movq	%rdx, 0x8(%rax)
 3266868:      	addq	$0x8, %rax
 326686c:      	jmp	0x3266820 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x4c0>
 326686e:      	cmpl	$0x1, %r14d
 3266872:      	jne	0x3266b3c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7dc>
 3266878:      	movl	0x8(%r15), %eax
 326687c:      	testq	%rax, %rax
 326687f:      	je	0x326693f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5df>
 3266885:      	movq	(%r15), %r14
 3266888:      	leaq	(%r14,%rax,8), %r15
 326688c:      	leaq	0x48(%rsp), %rbx
 3266891:      	leaq	0x28(%rsp), %r12
 3266896:      	jmp	0x32668b0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x550>
 3266898:      	cmpq	$0x0, 0x18(%rdx)
 326689d:      	je	0x32668a3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x543>
 326689f:      	nop
 32668a0:      	movq	%rax, (%r14)
 32668a3:      	addq	$0x8, %r14
 32668a7:      	cmpq	%r15, %r14
 32668aa:      	je	0x3266984 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x624>
 32668b0:      	movq	(%r14), %rsi
 32668b3:      	movq	0x20(%rsp), %rdi
 32668b8:      	movq	%rbp, %rdx
 32668bb:      	movq	%rbx, %rcx
 32668be:      	movq	%r12, %r8
 32668c1:      	callq	0x33fd3e0 <_ZN4llvm12SCEVDivision6divideERNS_15ScalarEvolutionEPKNS_4SCEVES5_PS5_S6_>
 32668c6:      	movq	0x48(%rsp), %rax
 32668cb:      	cmpw	$0x0, 0x18(%rax)
 32668d0:      	jne	0x32668a0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x540>
 32668d2:      	movq	0x20(%rax), %rdx
 32668d6:      	movl	0x20(%rdx), %ecx
 32668d9:      	cmpq	$0x41, %rcx
 32668dd:      	jb	0x3266898 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x538>
 32668df:      	leaq	0x3f(%rcx), %rsi
 32668e3:      	shrq	$0x6, %rsi
 32668e7:      	movq	0x18(%rdx), %r8
 32668eb:      	movl	%esi, %edx
 32668ed:      	shll	$0x6, %edx
 32668f0:      	incq	%rsi
 32668f3:      	xorl	%edi, %edi
 32668f5:      	nopw	%cs:(%rax,%rax)
 32668ff:      	nop
 3266900:      	movq	-0x10(%r8,%rsi,8), %r9
 3266905:      	testq	%r9, %r9
 3266908:      	jne	0x3266918 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5b8>
 326690a:      	addl	$0x40, %edi
 326690d:      	decq	%rsi
 3266910:      	cmpq	$0x1, %rsi
 3266914:      	ja	0x3266900 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5a0>
 3266916:      	jmp	0x3266921 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5c1>
 3266918:      	bsrq	%r9, %rdx
 326691c:      	xorl	$0x3f, %edx
 326691f:      	addl	%edi, %edx
 3266921:      	movl	%ecx, %esi
 3266923:      	andl	$0x3f, %esi
 3266926:      	movl	%ecx, %edi
 3266928:      	orl	$-0x40, %edi
 326692b:      	testl	%esi, %esi
 326692d:      	cmovel	%esi, %edi
 3266930:      	addl	%edx, %edi
 3266932:      	cmpl	%ecx, %edi
 3266934:      	jne	0x32668a0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x540>
 326693a:      	jmp	0x32668a3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x543>
 326693f:      	leaq	0x58(%rsp), %r15
 3266944:      	movq	%r15, 0x48(%rsp)
 3266949:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 3266953:      	movq	%rax, 0x50(%rsp)
 3266958:      	movq	(%rsp), %rbx
 326695c:      	movl	$0x0, 0x8(%rbx)
 3266963:      	movq	0x48(%rsp), %rdi
 3266968:      	cmpq	%r15, %rdi
 326696b:      	je	0x3266972 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 326696d:      	callq	0x828a640 <free@plt>
 3266972:      	addq	$0xf8, %rsp
 3266979:      	popq	%rbx
 326697a:      	popq	%r12
 326697c:      	popq	%r13
 326697e:      	popq	%r14
 3266980:      	popq	%r15
 3266982:      	popq	%rbp
 3266983:      	retq
 3266984:      	movq	0x18(%rsp), %rax
 3266989:      	movq	(%rax), %r14
 326698c:      	movl	0x8(%rax), %eax
 326698f:      	leaq	0x58(%rsp), %r15
 3266994:      	movq	%r15, 0x48(%rsp)
 3266999:      	movabsq	$0x400000000, %rcx      # imm = 0x400000000
 32669a3:      	movq	%rcx, 0x50(%rsp)
 32669a8:      	testq	%rax, %rax
 32669ab:      	je	0x3266958 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5f8>
 32669ad:      	leaq	(%r14,%rax,8), %r15
 32669b1:      	leaq	0x38(%rsp), %rbx
 32669b6:      	movq	%r15, 0x10(%rsp)
 32669bb:      	jmp	0x32669ea <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x68a>
 32669bd:      	nopl	(%rax)
 32669c0:      	movl	0x50(%rsp), %edx
 32669c4:      	cmpl	0x54(%rsp), %edx
 32669c8:      	jae	0x3266abb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x75b>
 32669ce:      	movq	0x48(%rsp), %rax
 32669d3:      	movl	%edx, %ecx
 32669d5:      	movq	%rbp, (%rax,%rcx,8)
 32669d9:      	incl	0x50(%rsp)
 32669dd:      	addq	$0x8, %r14
 32669e1:      	cmpq	%r15, %r14
 32669e4:      	je	0x3266adb <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x77b>
 32669ea:      	movq	(%r14), %rbp
 32669ed:      	movzwl	0x18(%rbp), %eax
 32669f1:      	testl	%eax, %eax
 32669f3:      	je	0x32669dd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x67d>
 32669f5:      	cmpl	$0x6, %eax
 32669f8:      	jne	0x32669c0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x660>
 32669fa:      	movq	%rbx, %r15
 32669fd:      	movq	%rbx, 0x28(%rsp)
 3266a02:      	movabsq	$0x200000000, %rax      # imm = 0x200000000
 3266a0c:      	movq	%rax, 0x30(%rsp)
 3266a11:      	movq	0x28(%rbp), %r13
 3266a15:      	testq	%r13, %r13
 3266a18:      	je	0x3266a80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x720>
 3266a1a:      	movq	0x20(%rbp), %rbp
 3266a1e:      	shlq	$0x3, %r13
 3266a22:      	xorl	%eax, %eax
 3266a24:      	xorl	%r12d, %r12d
 3266a27:      	jmp	0x3266a4e <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6ee>
 3266a29:      	nopl	(%rax)
 3266a30:      	movq	0x28(%rsp), %rcx
 3266a35:      	movl	%eax, %eax
 3266a37:      	movq	%rbx, (%rcx,%rax,8)
 3266a3b:      	movl	0x30(%rsp), %eax
 3266a3f:      	incl	%eax
 3266a41:      	movl	%eax, 0x30(%rsp)
 3266a45:      	addq	$0x8, %r12
 3266a49:      	cmpq	%r12, %r13
 3266a4c:      	je	0x3266a80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x720>
 3266a4e:      	movq	(%rbp,%r12), %rbx
 3266a53:      	cmpw	$0x0, 0x18(%rbx)
 3266a58:      	je	0x3266a45 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6e5>
 3266a5a:      	cmpl	0x34(%rsp), %eax
 3266a5e:      	jb	0x3266a30 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6d0>
 3266a60:      	movl	%eax, %edx
 3266a62:      	incq	%rdx
 3266a65:      	movl	$0x8, %ecx
 3266a6a:      	leaq	0x28(%rsp), %rdi
 3266a6f:      	movq	%r15, %rsi
 3266a72:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266a77:      	movl	0x30(%rsp), %eax
 3266a7b:      	jmp	0x3266a30 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x6d0>
 3266a7d:      	nopl	(%rax)
 3266a80:      	movq	0x20(%rsp), %rdi
 3266a85:      	leaq	0x28(%rsp), %rsi
 3266a8a:      	xorl	%edx, %edx
 3266a8c:      	xorl	%ecx, %ecx
 3266a8e:      	callq	0x3380710 <_ZN4llvm15ScalarEvolution10getMulExprERNS_15SmallVectorImplIPKNS_4SCEVEEENS2_11NoWrapFlagsEj>
 3266a93:      	movq	%rax, %rbp
 3266a96:      	movq	0x28(%rsp), %rdi
 3266a9b:      	movq	%r15, %rbx
 3266a9e:      	cmpq	%r15, %rdi
 3266aa1:      	je	0x3266aa8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x748>
 3266aa3:      	callq	0x828a640 <free@plt>
 3266aa8:      	testq	%rbp, %rbp
 3266aab:      	movq	0x10(%rsp), %r15
 3266ab0:      	jne	0x32669c0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x660>
 3266ab6:      	jmp	0x32669dd <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x67d>
 3266abb:      	incq	%rdx
 3266abe:      	movl	$0x8, %ecx
 3266ac3:      	leaq	0x48(%rsp), %rdi
 3266ac8:      	leaq	0x58(%rsp), %rsi
 3266acd:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266ad2:      	movl	0x50(%rsp), %edx
 3266ad6:      	jmp	0x32669ce <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x66e>
 3266adb:      	cmpl	$0x0, 0x50(%rsp)
 3266ae0:      	je	0x3266cb2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x952>
 3266ae6:      	leaq	0x48(%rsp), %rsi
 3266aeb:      	movq	0x20(%rsp), %rdi
 3266af0:      	movq	(%rsp), %rbx
 3266af4:      	movq	%rbx, %rdx
 3266af7:      	callq	0x3266ef0 <_ZL22findArrayDimensionsRecRN4llvm15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_>
 3266afc:      	testb	%al, %al
 3266afe:      	leaq	0x58(%rsp), %r15
 3266b03:      	je	0x326695c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5fc>
 3266b09:      	movl	0x8(%rbx), %edx
 3266b0c:      	cmpl	0xc(%rbx), %edx
 3266b0f:      	movq	%rbx, %rdi
 3266b12:      	jae	0x3266eca <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb6a>
 3266b18:      	movq	0x8(%rsp), %rsi
 3266b1d:      	movq	(%rdi), %rax
 3266b20:      	movl	%edx, %ecx
 3266b22:      	movq	%rsi, (%rax,%rcx,8)
 3266b26:      	incl	0x8(%rdi)
 3266b29:      	movq	0x48(%rsp), %rdi
 3266b2e:      	cmpq	%r15, %rdi
 3266b31:      	jne	0x326696d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x60d>
 3266b37:      	jmp	0x3266972 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x612>
 3266b3c:      	movq	%r13, %r14
 3266b3f:      	jmp	0x3266b8d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x82d>
 3266b41:      	nopw	%cs:(%rax,%rax)
 3266b4b:      	nopl	(%rax,%rax)
 3266b50:      	movq	%r14, %rdx
 3266b53:      	subq	%r13, %rdx
 3266b56:      	movq	%rdx, %rax
 3266b59:      	sarq	$0x3, %rax
 3266b5d:      	cmpq	$0x2, %rax
 3266b61:      	jl	0x3266c68 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x908>
 3266b67:      	shlq	$0x3, %rax
 3266b6b:      	subq	%rax, %rdi
 3266b6e:      	addq	$0x10, %rdi
 3266b72:      	movq	%r13, %rsi
 3266b75:      	callq	0x828abc0 <memmove@plt>
 3266b7a:      	movq	%r13, %rax
 3266b7d:      	movq	%rbx, (%rax)
 3266b80:      	leaq	0x8(%r14), %rbx
 3266b84:      	cmpq	%r12, %rbx
 3266b87:      	je	0x3266878 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x518>
 3266b8d:      	movq	%r14, %rdi
 3266b90:      	movq	%rbx, %r14
 3266b93:      	movq	(%rbx), %rbx
 3266b96:      	cmpw	$0x6, 0x18(%rbx)
 3266b9b:      	setne	%cl
 3266b9e:      	testq	%rbx, %rbx
 3266ba1:      	sete	%al
 3266ba4:      	orb	%cl, %al
 3266ba6:      	movl	$0x1, %edx
 3266bab:      	movl	$0x1, %esi
 3266bb0:      	jne	0x3266bb5 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x855>
 3266bb2:      	movl	0x28(%rbx), %esi
 3266bb5:      	movq	(%r13), %rcx
 3266bb9:      	testq	%rcx, %rcx
 3266bbc:      	je	0x3266bc8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x868>
 3266bbe:      	cmpw	$0x6, 0x18(%rcx)
 3266bc3:      	jne	0x3266bc8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x868>
 3266bc5:      	movl	0x28(%rcx), %edx
 3266bc8:      	cmpl	%edx, %esi
 3266bca:      	jg	0x3266b50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7f0>
 3266bcc:      	testb	%al, %al
 3266bce:      	je	0x3266c20 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8c0>
 3266bd0:      	movq	-0x8(%r14), %rcx
 3266bd4:      	movq	%r14, %rax
 3266bd7:      	testq	%rcx, %rcx
 3266bda:      	je	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266bdc:      	cmpw	$0x6, 0x18(%rcx)
 3266be1:      	movq	%r14, %rax
 3266be4:      	jne	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266be6:      	movq	%r14, %rax
 3266be9:      	nopl	(%rax)
 3266bf0:      	cmpl	$0x0, 0x28(%rcx)
 3266bf4:      	jg	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266bf6:      	movq	%rcx, (%rax)
 3266bf9:      	movq	-0x10(%rax), %rcx
 3266bfd:      	addq	$-0x8, %rax
 3266c01:      	testq	%rcx, %rcx
 3266c04:      	je	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c0a:      	cmpw	$0x6, 0x18(%rcx)
 3266c0f:      	je	0x3266bf0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x890>
 3266c11:      	jmp	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c16:      	nopw	%cs:(%rax,%rax)
 3266c20:      	movl	0x28(%rbx), %ecx
 3266c23:      	movq	%r14, %rax
 3266c26:      	movq	-0x8(%rax), %rdx
 3266c2a:      	movl	$0x1, %esi
 3266c2f:      	testq	%rdx, %rdx
 3266c32:      	jne	0x3266c55 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8f5>
 3266c34:      	jmp	0x3266c5f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c36:      	nopw	%cs:(%rax,%rax)
 3266c40:      	movq	%rdx, (%rax)
 3266c43:      	addq	$-0x8, %rax
 3266c47:      	movq	-0x8(%rax), %rdx
 3266c4b:      	movl	$0x1, %esi
 3266c50:      	testq	%rdx, %rdx
 3266c53:      	je	0x3266c5f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c55:      	cmpw	$0x6, 0x18(%rdx)
 3266c5a:      	jne	0x3266c5f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8ff>
 3266c5c:      	movl	0x28(%rdx), %esi
 3266c5f:      	cmpl	%ecx, %esi
 3266c61:      	jl	0x3266c40 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x8e0>
 3266c63:      	jmp	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c68:      	movq	%r13, %rax
 3266c6b:      	cmpq	$0x8, %rdx
 3266c6f:      	jne	0x3266b7d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81d>
 3266c75:      	movq	%rcx, 0x8(%rdi)
 3266c79:      	jmp	0x3266b7a <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x81a>
 3266c7e:      	movl	%edi, %esi
 3266c80:      	shrb	$0x3, %sil
 3266c84:      	incb	%sil
 3266c87:      	movzbl	%sil, %esi
 3266c8b:      	andl	$0x3, %esi
 3266c8e:      	jmp	0x3266c9d <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x93d>
 3266c90:      	addq	$0x8, %rcx
 3266c94:      	decq	%rsi
 3266c97:      	je	0x32667b2 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x452>
 3266c9d:      	movq	%rdx, %r8
 3266ca0:      	movq	(%rcx), %rdx
 3266ca3:      	cmpq	%rdx, %r8
 3266ca6:      	je	0x3266c90 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x930>
 3266ca8:      	movq	%rdx, 0x8(%rax)
 3266cac:      	addq	$0x8, %rax
 3266cb0:      	jmp	0x3266c90 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x930>
 3266cb2:      	movq	(%rsp), %rbx
 3266cb6:      	leaq	0x58(%rsp), %r15
 3266cbb:      	jmp	0x326695c <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x5fc>
 3266cc0:      	movq	%rdx, 0x8(%rax)
 3266cc4:      	nopw	%cs:(%rax,%rax)
 3266cce:      	nop
 3266cd0:      	movq	%r13, %rax
 3266cd3:      	movq	%r15, (%rax)
 3266cd6:      	addq	$0x8, %r12
 3266cda:      	addq	$0x8, %r14
 3266cde:      	cmpq	$0x80, %r12
 3266ce5:      	je	0x3266df8 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa98>
 3266ceb:      	movq	%rbp, %rax
 3266cee:      	movq	(%r13,%r12), %r15
 3266cf3:      	cmpw	$0x6, 0x18(%r15)
 3266cf9:      	setne	%dl
 3266cfc:      	testq	%r15, %r15
 3266cff:      	sete	%cl
 3266d02:      	orb	%dl, %cl
 3266d04:      	movl	$0x1, %esi
 3266d09:      	movl	$0x1, %edi
 3266d0e:      	jne	0x3266d14 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9b4>
 3266d10:      	movl	0x28(%r15), %edi
 3266d14:      	movq	(%r13), %rdx
 3266d18:      	testq	%rdx, %rdx
 3266d1b:      	je	0x3266d27 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9c7>
 3266d1d:      	cmpw	$0x6, 0x18(%rdx)
 3266d22:      	jne	0x3266d27 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9c7>
 3266d24:      	movl	0x28(%rdx), %esi
 3266d27:      	leaq	(%r13,%r12), %rbp
 3266d2c:      	cmpl	%esi, %edi
 3266d2e:      	jle	0x3266d50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x9f0>
 3266d30:      	cmpq	$0x9, %r12
 3266d34:      	jb	0x3266cc0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x960>
 3266d36:      	movq	%rbx, %rdi
 3266d39:      	movq	%r13, %rsi
 3266d3c:      	movq	%r12, %rdx
 3266d3f:      	callq	0x828abc0 <memmove@plt>
 3266d44:      	jmp	0x3266cd0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x970>
 3266d46:      	nopw	%cs:(%rax,%rax)
 3266d50:      	testb	%cl, %cl
 3266d52:      	je	0x3266db0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa50>
 3266d54:      	movq	-0x8(%rbp), %rcx
 3266d58:      	movq	%rbp, %rax
 3266d5b:      	testq	%rcx, %rcx
 3266d5e:      	je	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266d64:      	cmpw	$0x6, 0x18(%rcx)
 3266d69:      	movq	%rbp, %rax
 3266d6c:      	jne	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266d72:      	movq	%r14, %rax
 3266d75:      	nopw	%cs:(%rax,%rax)
 3266d7f:      	nop
 3266d80:      	cmpl	$0x0, 0x28(%rcx)
 3266d84:      	jg	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266d8a:      	movq	%rcx, (%rax)
 3266d8d:      	movq	-0x10(%rax), %rcx
 3266d91:      	addq	$-0x8, %rax
 3266d95:      	testq	%rcx, %rcx
 3266d98:      	je	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266d9e:      	cmpw	$0x6, 0x18(%rcx)
 3266da3:      	je	0x3266d80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa20>
 3266da5:      	jmp	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266daa:      	nopw	(%rax,%rax)
 3266db0:      	movl	0x28(%r15), %ecx
 3266db4:      	movq	%rbp, %rax
 3266db7:      	movq	-0x8(%rax), %rdx
 3266dbb:      	movl	$0x1, %esi
 3266dc0:      	testq	%rdx, %rdx
 3266dc3:      	jne	0x3266de5 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa85>
 3266dc5:      	jmp	0x3266def <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266dc7:      	nopw	(%rax,%rax)
 3266dd0:      	movq	%rdx, (%rax)
 3266dd3:      	addq	$-0x8, %rax
 3266dd7:      	movq	-0x8(%rax), %rdx
 3266ddb:      	movl	$0x1, %esi
 3266de0:      	testq	%rdx, %rdx
 3266de3:      	je	0x3266def <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266de5:      	cmpw	$0x6, 0x18(%rdx)
 3266dea:      	jne	0x3266def <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa8f>
 3266dec:      	movl	0x28(%rdx), %esi
 3266def:      	cmpl	%ecx, %esi
 3266df1:      	jl	0x3266dd0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xa70>
 3266df3:      	jmp	0x3266cd3 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x973>
 3266df8:      	subq	$-0x80, %r13
 3266dfc:      	movq	0x8(%rsp), %rbp
 3266e01:      	movq	0x18(%rsp), %r15
 3266e06:      	movq	0x10(%rsp), %r8
 3266e0b:      	jmp	0x3266e20 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xac0>
 3266e0d:      	nopl	(%rax)
 3266e10:      	movq	%rax, (%rcx)
 3266e13:      	addq	$0x8, %r13
 3266e17:      	cmpq	%r8, %r13
 3266e1a:      	je	0x3266878 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x518>
 3266e20:      	movq	(%r13), %rax
 3266e24:      	testq	%rax, %rax
 3266e27:      	je	0x3266e80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb20>
 3266e29:      	cmpw	$0x6, 0x18(%rax)
 3266e2e:      	jne	0x3266e80 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb20>
 3266e30:      	movl	0x28(%rax), %edx
 3266e33:      	movq	%r13, %rcx
 3266e36:      	movq	-0x8(%rcx), %rsi
 3266e3a:      	movl	$0x1, %edi
 3266e3f:      	testq	%rsi, %rsi
 3266e42:      	jne	0x3266e65 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb05>
 3266e44:      	jmp	0x3266e6f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266e46:      	nopw	%cs:(%rax,%rax)
 3266e50:      	movq	%rsi, (%rcx)
 3266e53:      	addq	$-0x8, %rcx
 3266e57:      	movq	-0x8(%rcx), %rsi
 3266e5b:      	movl	$0x1, %edi
 3266e60:      	testq	%rsi, %rsi
 3266e63:      	je	0x3266e6f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266e65:      	cmpw	$0x6, 0x18(%rsi)
 3266e6a:      	jne	0x3266e6f <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb0f>
 3266e6c:      	movl	0x28(%rsi), %edi
 3266e6f:      	cmpl	%edx, %edi
 3266e71:      	jl	0x3266e50 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xaf0>
 3266e73:      	jmp	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266e75:      	nopw	%cs:(%rax,%rax)
 3266e7f:      	nop
 3266e80:      	movq	-0x8(%r13), %rdx
 3266e84:      	movq	%r13, %rcx
 3266e87:      	testq	%rdx, %rdx
 3266e8a:      	je	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266e8c:      	cmpw	$0x6, 0x18(%rdx)
 3266e91:      	movq	%r13, %rcx
 3266e94:      	jne	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266e9a:      	movq	%r13, %rcx
 3266e9d:      	nopl	(%rax)
 3266ea0:      	cmpl	$0x0, 0x28(%rdx)
 3266ea4:      	jg	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266eaa:      	movq	%rdx, (%rcx)
 3266ead:      	movq	-0x10(%rcx), %rdx
 3266eb1:      	addq	$-0x8, %rcx
 3266eb5:      	testq	%rdx, %rdx
 3266eb8:      	je	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266ebe:      	cmpw	$0x6, 0x18(%rdx)
 3266ec3:      	je	0x3266ea0 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xb40>
 3266ec5:      	jmp	0x3266e10 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0xab0>
 3266eca:      	incq	%rdx
 3266ecd:      	leaq	0x10(%rdi), %rsi
 3266ed1:      	movl	$0x8, %ecx
 3266ed6:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3266edb:      	movq	(%rsp), %rdi
 3266edf:      	movl	0x8(%rdi), %edx
 3266ee2:      	jmp	0x3266b18 <_ZN4llvm19findArrayDimensionsERNS_15ScalarEvolutionERNS_15SmallVectorImplIPKNS_4SCEVEEES7_S5_+0x7b8>
