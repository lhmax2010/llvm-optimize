
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002cfd1b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE>:
 2cfd1b0:      	pushq	%rbp
 2cfd1b1:      	pushq	%r15
 2cfd1b3:      	pushq	%r14
 2cfd1b5:      	pushq	%r13
 2cfd1b7:      	pushq	%r12
 2cfd1b9:      	pushq	%rbx
 2cfd1ba:      	subq	$0x2c8, %rsp            # imm = 0x2C8
 2cfd1c1:      	leaq	0x248(%rsp), %rax
 2cfd1c9:      	movq	%rax, 0x238(%rsp)
 2cfd1d1:      	movabsq	$0x800000000, %rax      # imm = 0x800000000
 2cfd1db:      	movq	%rax, 0x240(%rsp)
 2cfd1e3:      	movb	$0x0, 0x200(%rdi)
 2cfd1ea:      	leaq	0x30(%rsi), %r10
 2cfd1ee:      	movq	%rsi, 0x18(%rsp)
 2cfd1f3:      	cmpq	0x38(%rsi), %r10
 2cfd1f7:      	movq	%rdi, (%rsp)
 2cfd1fb:      	je	0x2cfe609 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1459>
 2cfd201:      	leaq	0x298(%rdi), %rax
 2cfd208:      	movq	%rax, 0x1f8(%rsp)
 2cfd210:      	leaq	0x2a8(%rdi), %rax
 2cfd217:      	movq	%rax, 0x220(%rsp)
 2cfd21f:      	movl	$0xe, 0x118(%rsp)
 2cfd22a:      	movl	$0xffffffff, 0x180(%rsp) # imm = 0xFFFFFFFF
 2cfd235:      	movq	$0x0, 0x80(%rsp)
 2cfd241:      	xorl	%r9d, %r9d
 2cfd244:      	jmp	0x2cfd26b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbb>
 2cfd246:      	nopw	%cs:(%rax,%rax)
 2cfd250:      	movq	%rbp, %r15
 2cfd253:      	movl	%ebx, %r12d
 2cfd256:      	movl	%r12d, %r9d
 2cfd259:      	movq	%r15, %r10
 2cfd25c:      	movq	0x18(%rsp), %rax
 2cfd261:      	cmpq	0x38(%rax), %r15
 2cfd265:      	je	0x2cfe5ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x143e>
 2cfd26b:      	movq	(%r10), %r15
 2cfd26e:      	andq	$-0x8, %r15
 2cfd272:      	testb	$0x4, (%r15)
 2cfd276:      	jne	0x2cfd295 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe5>
 2cfd278:      	nopl	(%rax,%rax)
 2cfd280:      	testb	$0x4, 0x2c(%r15)
 2cfd285:      	je	0x2cfd295 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe5>
 2cfd287:      	movq	(%r15), %r15
 2cfd28a:      	andq	$-0x8, %r15
 2cfd28e:      	testb	$0x4, 0x2c(%r15)
 2cfd293:      	jne	0x2cfd287 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd7>
 2cfd295:      	movzwl	0x44(%r15), %edx
 2cfd29a:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd2a0:      	je	0x2cfd2b6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x106>
 2cfd2a2:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd2a8:      	je	0x2cfd2b6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x106>
 2cfd2aa:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd2b0:      	jne	0x2cfd3ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23d>
 2cfd2b6:      	movq	%r10, 0x8(%rsp)
 2cfd2bb:      	movq	%r9, 0x90(%rsp)
 2cfd2c3:      	movq	0x20(%r15), %rax
 2cfd2c7:      	movl	0x44(%rax), %r13d
 2cfd2cb:      	movl	0x4(%rax), %ebx
 2cfd2ce:      	movq	%rax, 0x98(%rsp)
 2cfd2d6:      	movl	0x24(%rax), %r14d
 2cfd2da:      	movq	%rdi, %rbp
 2cfd2dd:      	movq	0x48(%rdi), %rdi
 2cfd2e1:      	movq	(%rdi), %rax
 2cfd2e4:      	xorl	%r12d, %r12d
 2cfd2e7:      	movl	%ebx, %esi
 2cfd2e9:      	movl	%edx, 0x10(%rsp)
 2cfd2ed:      	xorl	%edx, %edx
 2cfd2ef:      	callq	*0x10(%rax)
 2cfd2f2:      	movq	%rax, 0x20(%rsp)
 2cfd2f7:      	movq	0x48(%rbp), %rdi
 2cfd2fb:      	movq	(%rdi), %rax
 2cfd2fe:      	movl	%r14d, 0x120(%rsp)
 2cfd306:      	movl	%r14d, %esi
 2cfd309:      	movq	%r13, %r14
 2cfd30c:      	xorl	%edx, %edx
 2cfd30e:      	callq	*0x10(%rax)
 2cfd311:      	movl	0x10(%rsp), %edx
 2cfd315:      	movq	%rax, %r8
 2cfd318:      	movq	%rbx, 0x78(%rsp)
 2cfd31d:      	cmpl	%r14d, %ebx
 2cfd320:      	jne	0x2cfd349 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x199>
 2cfd322:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd328:      	je	0x2cfd336 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x186>
 2cfd32a:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd330:      	jne	0x2cfd4e2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x332>
 2cfd336:      	movq	(%rsp), %rax
 2cfd33a:      	movq	0x50(%rax), %rax
 2cfd33e:      	cmpl	$0xe, 0x1c0(%rax)
 2cfd345:      	sete	%r12b
 2cfd349:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd34f:      	je	0x2cfd359 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a9>
 2cfd351:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd357:      	jne	0x2cfd3d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x220>
 2cfd359:      	movq	0x20(%rsp), %rcx
 2cfd35e:      	movl	%ecx, %eax
 2cfd360:      	andl	$0x1, %eax
 2cfd363:      	incl	%ecx
 2cfd365:      	xorl	%r8d, %ecx
 2cfd368:      	orl	%eax, %ecx
 2cfd36a:      	setne	%al
 2cfd36d:      	movq	0x8(%rsp), %r10
 2cfd372:      	orb	%al, %r12b
 2cfd375:      	cmpb	$0x1, %r12b
 2cfd379:      	jne	0x2cfd3e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x230>
 2cfd37b:      	movzwl	%dx, %eax
 2cfd37e:      	cmpl	$0x3ba, %eax            # imm = 0x3BA
 2cfd383:      	sete	%sil
 2cfd387:      	movl	%eax, 0xc0(%rsp)
 2cfd38e:      	cmpl	$0x102f, %eax           # imm = 0x102F
 2cfd393:      	sete	%dil
 2cfd397:      	movq	0x20(%r15), %rbp
 2cfd39b:      	movl	(%rbp), %r13d
 2cfd39f:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd3a5:      	je	0x2cfd3b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x203>
 2cfd3a7:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd3ad:      	jne	0x2cfd4f6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x346>
 2cfd3b3:      	movl	%r13d, %eax
 2cfd3b6:      	notl	%eax
 2cfd3b8:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfd3bd:      	sete	%al
 2cfd3c0:      	movl	%eax, 0xe8(%rsp)
 2cfd3c7:      	jmp	0x2cfd511 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x361>
 2cfd3cc:      	nopl	(%rax)
 2cfd3d0:      	xorl	%eax, %eax
 2cfd3d2:      	movq	0x8(%rsp), %r10
 2cfd3d7:      	orb	%al, %r12b
 2cfd3da:      	cmpb	$0x1, %r12b
 2cfd3de:      	je	0x2cfd37b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb>
 2cfd3e0:      	movzwl	0x44(%r15), %edx
 2cfd3e5:      	movq	0x90(%rsp), %r9
 2cfd3ed:      	leal	0x1(%r9), %r12d
 2cfd3f1:      	movzwl	%dx, %r14d
 2cfd3f5:      	cmpl	$0x104b, %r14d          # imm = 0x104B
 2cfd3fc:      	jle	0x2cfd430 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x280>
 2cfd3fe:      	leal	-0x117a(%r14), %eax
 2cfd405:      	cmpl	$0x1f, %eax
 2cfd408:      	jbe	0x2cfd456 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a6>
 2cfd40a:      	leal	-0x110f(%r14), %eax
 2cfd411:      	cmpl	$0x2, %eax
 2cfd414:      	jb	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd416:      	leal	-0x104c(%r14), %eax
 2cfd41d:      	cmpl	$0x1, %eax
 2cfd420:      	jbe	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd422:      	jmp	0x2cfd4d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x320>
 2cfd427:      	nopw	(%rax,%rax)
 2cfd430:      	cmpl	$0xb52, %r14d           # imm = 0xB52
 2cfd437:      	jg	0x2cfd4b5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x305>
 2cfd439:      	cmpl	$0x3d7, %r14d           # imm = 0x3D7
 2cfd440:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd442:      	cmpl	$0x7f9, %r14d           # imm = 0x7F9
 2cfd449:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd44b:      	cmpl	$0xb51, %r14d           # imm = 0xB51
 2cfd452:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd454:      	jmp	0x2cfd4d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x320>
 2cfd456:      	movl	$0xa0000009, %ecx       # imm = 0xA0000009
 2cfd45b:      	btl	%eax, %ecx
 2cfd45e:      	jae	0x2cfd40a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25a>
 2cfd460:      	movq	0x20(%r15), %rax
 2cfd464:      	cmpb	$0x0, 0x20(%rax)
 2cfd468:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd46e:      	movq	0x30(%r15), %rcx
 2cfd472:      	cmpq	$0x8, %rcx
 2cfd476:      	jb	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd47c:      	movl	%edx, %r13d
 2cfd47f:      	movq	%rcx, %rdx
 2cfd482:      	andq	$0x7, %rdx
 2cfd486:      	je	0x2cfdcd4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb24>
 2cfd48c:      	cmpl	$0x3, %edx
 2cfd48f:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd495:      	andq	$-0x8, %rcx
 2cfd499:      	cmpl	$0x1, (%rcx)
 2cfd49c:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4a2:      	movq	0x10(%rcx), %rcx
 2cfd4a6:      	testb	$0x4, 0x20(%rcx)
 2cfd4aa:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4b0:      	jmp	0x2cfdce2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb32>
 2cfd4b5:      	cmpl	$0xb53, %r14d           # imm = 0xB53
 2cfd4bc:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4be:      	cmpl	$0xf2e, %r14d           # imm = 0xF2E
 2cfd4c5:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4c7:      	cmpl	$0xf30, %r14d           # imm = 0xF30
 2cfd4ce:      	je	0x2cfd460 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4d0:      	addl	$-0xe, %edx
 2cfd4d3:      	cmpw	$0x5, %dx
 2cfd4d7:      	jb	0x2cfe075 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfd4dd:      	jmp	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4e2:      	xorl	%r12d, %r12d
 2cfd4e5:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd4eb:      	jne	0x2cfd351 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a1>
 2cfd4f1:      	jmp	0x2cfd359 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a9>
 2cfd4f6:      	movl	%r13d, %eax
 2cfd4f9:      	shrl	$0x1a, %eax
 2cfd4fc:      	xorl	%ecx, %ecx
 2cfd4fe:      	testl	$0x1000000, %r13d       # imm = 0x1000000
 2cfd505:      	sete	%cl
 2cfd508:      	andl	%eax, %ecx
 2cfd50a:      	movl	%ecx, 0xe8(%rsp)
 2cfd511:      	movq	0x98(%rsp), %r9
 2cfd519:      	movl	0x20(%rbp), %ecx
 2cfd51c:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd522:      	movq	%r14, 0x28(%rsp)
 2cfd527:      	movb	%sil, 0x230(%rsp)
 2cfd52f:      	movb	%dil, 0x228(%rsp)
 2cfd537:      	movq	%r8, 0x88(%rsp)
 2cfd53f:      	je	0x2cfd549 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x399>
 2cfd541:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd547:      	jne	0x2cfd55e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ae>
 2cfd549:      	movl	%ecx, %r12d
 2cfd54c:      	movl	%ecx, %eax
 2cfd54e:      	notl	%eax
 2cfd550:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfd555:      	sete	%al
 2cfd558:      	movl	%eax, 0x8(%rsp)
 2cfd55c:      	jmp	0x2cfd577 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c7>
 2cfd55e:      	movl	%ecx, %eax
 2cfd560:      	shrl	$0x1a, %eax
 2cfd563:      	xorl	%edx, %edx
 2cfd565:      	movl	%ecx, %r12d
 2cfd568:      	testl	$0x1000000, %ecx        # imm = 0x1000000
 2cfd56e:      	sete	%dl
 2cfd571:      	andl	%eax, %edx
 2cfd573:      	movl	%edx, 0x8(%rsp)
 2cfd577:      	movl	0x40(%r9), %eax
 2cfd57b:      	movq	%rax, %r14
 2cfd57e:      	testl	$0x1000000, %eax        # imm = 0x1000000
 2cfd583:      	sete	%bl
 2cfd586:      	movq	%r15, %rdi
 2cfd589:      	callq	0x2cf7a30 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfd58e:      	movq	0x10(%r15), %r9
 2cfd592:      	movl	$0xe, %r8d
 2cfd598:      	xorl	%r10d, %r10d
 2cfd59b:      	testb	$0x40, 0x12(%r9)
 2cfd5a0:      	jne	0x2cfd5b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x409>
 2cfd5a2:      	leaq	0x30(%rsp), %rdi
 2cfd5a7:      	xorl	%esi, %esi
 2cfd5a9:      	movl	%r12d, %r11d
 2cfd5ac:      	movq	%r14, %r12
 2cfd5af:      	movq	0x28(%rsp), %r9
 2cfd5b4:      	jmp	0x2cfd650 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4a0>
 2cfd5b9:      	movl	%eax, %r10d
 2cfd5bc:      	movzwl	0x28(%r15), %edx
 2cfd5c1:      	movzbl	0x2a(%r15), %ecx
 2cfd5c6:      	shll	$0x10, %ecx
 2cfd5c9:      	orl	%edx, %ecx
 2cfd5cb:      	testl	%ecx, %ecx
 2cfd5cd:      	leaq	0x30(%rsp), %rdi
 2cfd5d2:      	movl	%r12d, %r11d
 2cfd5d5:      	je	0x2cfd625 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x475>
 2cfd5d7:      	movzwl	(%r9), %edx
 2cfd5db:      	movzwl	0xa(%r9), %esi
 2cfd5e0:      	addq	$0x10, %rbp
 2cfd5e4:      	addl	%ecx, %ecx
 2cfd5e6:      	leaq	(%rcx,%rcx,2), %rcx
 2cfd5ea:      	shll	$0x5, %edx
 2cfd5ed:      	leaq	(%rsi,%rsi,2), %rsi
 2cfd5f1:      	leaq	(%rdx,%rsi,2), %rdx
 2cfd5f5:      	leaq	0x22(%r9,%rdx), %rax
 2cfd5fa:      	xorl	%edx, %edx
 2cfd5fc:      	xorl	%esi, %esi
 2cfd5fe:      	movq	%r14, %r12
 2cfd601:      	movq	0x28(%rsp), %r9
 2cfd606:      	nopw	%cs:(%rax,%rax)
 2cfd610:      	testb	$0x2, (%rax,%rdx)
 2cfd614:      	jne	0x2cfd637 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x487>
 2cfd616:      	addq	$0x20, %rbp
 2cfd61a:      	addq	$0x6, %rdx
 2cfd61e:      	cmpq	%rdx, %rcx
 2cfd621:      	jne	0x2cfd610 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x460>
 2cfd623:      	jmp	0x2cfd62f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47f>
 2cfd625:      	xorl	%esi, %esi
 2cfd627:      	movq	%r14, %r12
 2cfd62a:      	movq	0x28(%rsp), %r9
 2cfd62f:      	movl	%r10d, %eax
 2cfd632:      	xorl	%r10d, %r10d
 2cfd635:      	jmp	0x2cfd650 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4a0>
 2cfd637:      	movl	(%rbp), %r8d
 2cfd63b:      	movl	0x14(%rbp), %ecx
 2cfd63e:      	movl	%r10d, %eax
 2cfd641:      	movq	%rcx, %r10
 2cfd644:      	nopw	%cs:(%rax,%rax)
 2cfd64e:      	nop
 2cfd650:      	andl	$0x10000000, %r13d      # imm = 0x10000000
 2cfd657:      	andl	$0x10000000, %r11d      # imm = 0x10000000
 2cfd65e:      	movl	%r12d, %ecx
 2cfd661:      	shrl	$0x1a, %ecx
 2cfd664:      	movb	%bl, %sil
 2cfd667:      	andl	%ecx, %esi
 2cfd669:      	movq	0x88(%rsp), %rcx
 2cfd671:      	cmpl	0x20(%rsp), %ecx
 2cfd675:      	movl	0x10(%rsp), %ecx
 2cfd679:      	movq	%r8, 0x98(%rsp)
 2cfd681:      	jbe	0x2cfd8e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x736>
 2cfd687:      	testl	%eax, %eax
 2cfd689:      	jne	0x2cfd8e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x736>
 2cfd68f:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd695:      	je	0x2cfd6a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f4>
 2cfd697:      	movl	$0x7db, %ebx            # imm = 0x7DB
 2cfd69c:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd6a2:      	jne	0x2cfd6bd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d>
 2cfd6a4:      	cmpl	$0x102f, 0xc0(%rsp)     # imm = 0x102F
 2cfd6af:      	movl	$0x3ae, %ebx            # imm = 0x3AE
 2cfd6b4:      	movl	$0x1024, %eax           # imm = 0x1024
 2cfd6b9:      	cmoveq	%rax, %rbx
 2cfd6bd:      	movq	%rsi, %rbp
 2cfd6c0:      	movq	%r10, 0x70(%rsp)
 2cfd6c5:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd6cb:      	je	0x2cfd6d9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x529>
 2cfd6cd:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd6d3:      	jne	0x2cfdabf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x90f>
 2cfd6d9:      	movq	0x38(%r15), %rsi
 2cfd6dd:      	movq	%rsi, 0xa0(%rsp)
 2cfd6e5:      	movq	%rdi, %r14
 2cfd6e8:      	testq	%rsi, %rsi
 2cfd6eb:      	je	0x2cfd726 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x576>
 2cfd6ed:      	movl	$0x1, %edx
 2cfd6f2:      	leaq	0xa0(%rsp), %rdi
 2cfd6fa:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfd6ff:      	movq	0xa0(%rsp), %rsi
 2cfd707:      	movq	%rsi, 0x30(%rsp)
 2cfd70c:      	testq	%rsi, %rsi
 2cfd70f:      	je	0x2cfd72d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x57d>
 2cfd711:      	leaq	0xa0(%rsp), %r14
 2cfd719:      	movq	%r14, %rdi
 2cfd71c:      	leaq	0x30(%rsp), %rdx
 2cfd721:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cfd726:      	movq	$0x0, (%r14)
 2cfd72d:      	leaq	0x38(%rsp), %rax
 2cfd732:      	xorps	%xmm0, %xmm0
 2cfd735:      	movups	%xmm0, (%rax)
 2cfd738:      	movq	$0x0, 0x10(%rax)
 2cfd740:      	movq	(%rsp), %rax
 2cfd744:      	movq	0x40(%rax), %rax
 2cfd748:      	movq	0x8(%rax), %rcx
 2cfd74c:      	shll	$0x5, %ebx
 2cfd74f:      	subq	%rbx, %rcx
 2cfd752:      	movq	0x18(%rsp), %rdi
 2cfd757:      	movq	%r15, %rsi
 2cfd75a:      	leaq	0x30(%rsp), %r13
 2cfd75f:      	movq	%r13, %rdx
 2cfd762:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cfd767:      	movq	%rax, %r14
 2cfd76a:      	movq	%rdx, %r12
 2cfd76d:      	movq	$0x0, 0x138(%rsp)
 2cfd779:      	shll	$0x1a, %ebp
 2cfd77c:      	movq	0x28(%rsp), %rax
 2cfd781:      	movl	%eax, 0x134(%rsp)
 2cfd788:      	leaq	0x140(%rsp), %rbx
 2cfd790:      	xorps	%xmm0, %xmm0
 2cfd793:      	movups	%xmm0, (%rbx)
 2cfd796:      	movl	%ebp, 0x130(%rsp)
 2cfd79d:      	movq	%rdx, %rdi
 2cfd7a0:      	movq	%r14, %rsi
 2cfd7a3:      	leaq	0x130(%rsp), %rbp
 2cfd7ab:      	movq	%rbp, %rdx
 2cfd7ae:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd7b3:      	movl	0x98(%rsp), %eax
 2cfd7ba:      	movl	$0x1, 0x130(%rsp)
 2cfd7c5:      	movq	$0x0, 0x138(%rsp)
 2cfd7d1:      	movq	%rax, 0x140(%rsp)
 2cfd7d9:      	movq	%r12, %rdi
 2cfd7dc:      	movq	%r14, %rsi
 2cfd7df:      	movq	%rbp, %rdx
 2cfd7e2:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd7e7:      	movq	$0x0, 0x138(%rsp)
 2cfd7f3:      	movq	0x70(%rsp), %rax
 2cfd7f8:      	movl	%eax, 0x134(%rsp)
 2cfd7ff:      	xorps	%xmm0, %xmm0
 2cfd802:      	movups	%xmm0, (%rbx)
 2cfd805:      	movl	$0x0, 0x130(%rsp)
 2cfd810:      	movq	%r12, %rdi
 2cfd813:      	movq	%r14, %rsi
 2cfd816:      	movq	%rbp, %rdx
 2cfd819:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd81e:      	movq	$0x0, 0x138(%rsp)
 2cfd82a:      	movq	0x78(%rsp), %rax
 2cfd82f:      	movl	%eax, 0x134(%rsp)
 2cfd836:      	movzbl	0xe8(%rsp), %eax
 2cfd83e:      	shll	$0x1a, %eax
 2cfd841:      	orl	$0x1000000, %eax        # imm = 0x1000000
 2cfd846:      	xorps	%xmm0, %xmm0
 2cfd849:      	movups	%xmm0, (%rbx)
 2cfd84c:      	movl	%eax, 0x130(%rsp)
 2cfd853:      	movq	%r12, %rdi
 2cfd856:      	movq	%r14, %rsi
 2cfd859:      	movq	%rbp, %rdx
 2cfd85c:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd861:      	movq	$0x0, 0x138(%rsp)
 2cfd86d:      	movl	0x120(%rsp), %eax
 2cfd874:      	movl	%eax, 0x134(%rsp)
 2cfd87b:      	movzbl	0x8(%rsp), %eax
 2cfd880:      	shll	$0x1a, %eax
 2cfd883:      	orl	$0x1000000, %eax        # imm = 0x1000000
 2cfd888:      	xorps	%xmm0, %xmm0
 2cfd88b:      	movups	%xmm0, (%rbx)
 2cfd88e:      	movl	%eax, 0x130(%rsp)
 2cfd895:      	movq	%r12, %rdi
 2cfd898:      	movq	%r14, %rsi
 2cfd89b:      	movq	%rbp, %rdx
 2cfd89e:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd8a3:      	movq	%r12, %rdi
 2cfd8a6:      	movq	%r14, %rsi
 2cfd8a9:      	movq	%r15, %rdx
 2cfd8ac:      	callq	0x3651d00 <_ZN4llvm12MachineInstr12cloneMemRefsERNS_15MachineFunctionERKS0_>
 2cfd8b1:      	movq	0x30(%rsp), %rsi
 2cfd8b6:      	testq	%rsi, %rsi
 2cfd8b9:      	je	0x2cfd8c3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x713>
 2cfd8bb:      	movq	%r13, %rdi
 2cfd8be:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfd8c3:      	movq	0xa0(%rsp), %rsi
 2cfd8cb:      	testq	%rsi, %rsi
 2cfd8ce:      	je	0x2cfe029 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfd8d4:      	leaq	0xa0(%rsp), %rdi
 2cfd8dc:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfd8e1:      	jmp	0x2cfe029 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfd8e6:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd8ec:      	movq	0x78(%rsp), %rbx
 2cfd8f1:      	movq	%rsi, 0xe0(%rsp)
 2cfd8f9:      	je	0x2cfd903 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x753>
 2cfd8fb:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd901:      	jne	0x2cfd94b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x79b>
 2cfd903:      	movl	0xc0(%rsp), %ecx
 2cfd90a:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd910:      	jne	0x2cfd91f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x76f>
 2cfd912:      	movl	%eax, %ecx
 2cfd914:      	shrl	$0x1f, %ecx
 2cfd917:      	orl	$0x104c, %ecx           # imm = 0x104C
 2cfd91d:      	jmp	0x2cfd969 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x7b9>
 2cfd91f:      	movl	%eax, %r14d
 2cfd922:      	movl	$0x7f9, %edx            # imm = 0x7F9
 2cfd927:      	movl	$0x3d7, %r8d            # imm = 0x3D7
 2cfd92d:      	movl	$0x3d7, 0x10(%rsp)      # imm = 0x3D7
 2cfd935:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd93b:      	jne	0x2cfdf09 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd59>
 2cfd941:      	cmpl	%r9d, %ebx
 2cfd944:      	jne	0x2cfd98a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x7da>
 2cfd946:      	jmp	0x2cfda1a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfd94b:      	movl	0xc0(%rsp), %ecx
 2cfd952:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd958:      	jne	0x2cfdeeb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd3b>
 2cfd95e:      	movl	%eax, %ecx
 2cfd960:      	shrl	$0x1f, %ecx
 2cfd963:      	addl	$0x110f, %ecx           # imm = 0x110F
 2cfd969:      	movl	%ecx, 0x10(%rsp)
 2cfd96d:      	xorl	%r8d, %r8d
 2cfd970:      	movl	%eax, %r14d
 2cfd973:      	cmpl	$-0x4, %eax
 2cfd976:      	setl	%r8b
 2cfd97a:      	orl	$0x104c, %r8d           # imm = 0x104C
 2cfd981:      	cmpl	%r9d, %ebx
 2cfd984:      	je	0x2cfda1a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfd98a:      	leal	-0x1(%rbx), %eax
 2cfd98d:      	cmpl	$0x3fffffff, %eax       # imm = 0x3FFFFFFF
 2cfd992:      	setae	%al
 2cfd995:      	leal	-0x1(%r9), %ecx
 2cfd999:      	cmpl	$0x3fffffff, %ecx       # imm = 0x3FFFFFFF
 2cfd99f:      	setae	%cl
 2cfd9a2:      	orb	%al, %cl
 2cfd9a4:      	jne	0x2cfda12 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x862>
 2cfd9a6:      	movq	(%rsp), %rax
 2cfd9aa:      	movq	0x48(%rax), %rax
 2cfd9ae:      	leaq	(%rbx,%rbx,2), %rcx
 2cfd9b2:      	movq	0x8(%rax), %rdx
 2cfd9b6:      	movq	0x38(%rax), %rsi
 2cfd9ba:      	movl	0x10(%rdx,%rcx,8), %ecx
 2cfd9be:      	movl	%ecx, %eax
 2cfd9c0:      	andl	$0xfff, %eax            # imm = 0xFFF
 2cfd9c5:      	shrl	$0xc, %ecx
 2cfd9c8:      	leaq	(%rsi,%rcx,2), %rcx
 2cfd9cc:      	leaq	(%r9,%r9,2), %rdi
 2cfd9d0:      	movl	0x10(%rdx,%rdi,8), %edi
 2cfd9d4:      	movl	%edi, %edx
 2cfd9d6:      	andl	$0xfff, %edx            # imm = 0xFFF
 2cfd9dc:      	shrl	$0xc, %edi
 2cfd9df:      	leaq	(%rsi,%rdi,2), %rsi
 2cfd9e3:      	nopw	%cs:(%rax,%rax)
 2cfd9ed:      	nopl	(%rax)
 2cfd9f0:      	cmpl	%edx, %eax
 2cfd9f2:      	je	0x2cfda1a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfd9f4:      	jae	0x2cfda05 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x855>
 2cfd9f6:      	movswl	(%rcx), %edi
 2cfd9f9:      	addq	$0x2, %rcx
 2cfd9fd:      	addl	%edi, %eax
 2cfd9ff:      	testl	%edi, %edi
 2cfda01:      	jne	0x2cfd9f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x840>
 2cfda03:      	jmp	0x2cfda12 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x862>
 2cfda05:      	movswl	(%rsi), %edi
 2cfda08:      	addq	$0x2, %rsi
 2cfda0c:      	addl	%edi, %edx
 2cfda0e:      	testl	%edi, %edi
 2cfda10:      	jne	0x2cfd9f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x840>
 2cfda12:      	movl	%r8d, %edx
 2cfda15:      	jmp	0x2cfdf09 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd59>
 2cfda1a:      	shrl	$0x1c, %r12d
 2cfda1e:      	andl	$0x1, %r12d
 2cfda22:      	movl	%r14d, %edx
 2cfda25:      	addl	$0x4, %edx
 2cfda28:      	subq	$0x8, %rsp
 2cfda2c:      	movzbl	0x10(%rsp), %eax
 2cfda31:      	movq	%r12, %r13
 2cfda34:      	movq	%r12, 0x28(%rsp)
 2cfda39:      	movq	0x20(%rsp), %r12
 2cfda3e:      	movq	%r12, %rdi
 2cfda41:      	movq	%r15, %rsi
 2cfda44:      	movl	$0x1, %ecx
 2cfda49:      	movq	%r9, %r11
 2cfda4c:      	movl	0x128(%rsp), %r9d
 2cfda54:      	pushq	%r15
 2cfda56:      	movq	0x10(%rsp), %rbx
 2cfda5b:      	pushq	0x40(%rbx)
 2cfda5e:      	pushq	%r10
 2cfda60:      	movq	0xb8(%rsp), %rbp
 2cfda68:      	pushq	%rbp
 2cfda69:      	pushq	%r13
 2cfda6b:      	pushq	$0x0
 2cfda6d:      	pushq	%r11
 2cfda6f:      	pushq	$0x0
 2cfda71:      	pushq	%rax
 2cfda72:      	movq	%r10, %r13
 2cfda75:      	callq	0x2d049c0 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfda7a:      	addq	$0x48, %rsp
 2cfda7e:      	movzbl	0xf0(%rsp), %eax
 2cfda86:      	movq	%r12, %rdi
 2cfda89:      	movq	%r15, %rsi
 2cfda8c:      	movl	%r14d, %edx
 2cfda8f:      	movl	$0x1, %ecx
 2cfda94:      	movl	0x18(%rsp), %r8d
 2cfda99:      	movq	0x80(%rsp), %r9
 2cfdaa1:      	pushq	%r15
 2cfdaa3:      	pushq	0x40(%rbx)
 2cfdaa6:      	pushq	%r13
 2cfdaa8:      	pushq	%rbp
 2cfdaa9:      	pushq	0x48(%rsp)
 2cfdaad:      	pushq	0x110(%rsp)
 2cfdab4:      	pushq	0x60(%rsp)
 2cfdab8:      	pushq	$0x0
 2cfdaba:      	jmp	0x2cfe01f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe6f>
 2cfdabf:      	movl	%r11d, 0x20(%rsp)
 2cfdac4:      	movl	%r13d, 0x10(%rsp)
 2cfdac9:      	movq	0x38(%r15), %rsi
 2cfdacd:      	movq	%rsi, 0xf0(%rsp)
 2cfdad5:      	movq	%rdi, %r14
 2cfdad8:      	testq	%rsi, %rsi
 2cfdadb:      	je	0x2cfdb16 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x966>
 2cfdadd:      	movl	$0x1, %edx
 2cfdae2:      	leaq	0xf0(%rsp), %rdi
 2cfdaea:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfdaef:      	movq	0xf0(%rsp), %rsi
 2cfdaf7:      	movq	%rsi, 0x30(%rsp)
 2cfdafc:      	testq	%rsi, %rsi
 2cfdaff:      	je	0x2cfdb1d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x96d>
 2cfdb01:      	leaq	0xf0(%rsp), %r14
 2cfdb09:      	movq	%r14, %rdi
 2cfdb0c:      	leaq	0x30(%rsp), %rdx
 2cfdb11:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cfdb16:      	movq	$0x0, (%r14)
 2cfdb1d:      	leaq	0x38(%rsp), %rax
 2cfdb22:      	xorps	%xmm0, %xmm0
 2cfdb25:      	movups	%xmm0, (%rax)
 2cfdb28:      	movq	$0x0, 0x10(%rax)
 2cfdb30:      	movq	(%rsp), %rax
 2cfdb34:      	movq	0x40(%rax), %rax
 2cfdb38:      	movq	0x8(%rax), %rcx
 2cfdb3c:      	shll	$0x5, %ebx
 2cfdb3f:      	subq	%rbx, %rcx
 2cfdb42:      	movq	0x18(%rsp), %rdi
 2cfdb47:      	movq	%r15, %rsi
 2cfdb4a:      	leaq	0x30(%rsp), %r13
 2cfdb4f:      	movq	%r13, %rdx
 2cfdb52:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cfdb57:      	movq	%rax, %r14
 2cfdb5a:      	movq	%rdx, %r12
 2cfdb5d:      	movq	$0x0, 0x138(%rsp)
 2cfdb69:      	shll	$0x1a, %ebp
 2cfdb6c:      	movq	0x28(%rsp), %rax
 2cfdb71:      	movl	%eax, 0x134(%rsp)
 2cfdb78:      	leaq	0x140(%rsp), %rbx
 2cfdb80:      	xorps	%xmm0, %xmm0
 2cfdb83:      	movups	%xmm0, (%rbx)
 2cfdb86:      	movl	%ebp, 0x130(%rsp)
 2cfdb8d:      	movq	%rdx, %rdi
 2cfdb90:      	movq	%r14, %rsi
 2cfdb93:      	leaq	0x130(%rsp), %rbp
 2cfdb9b:      	movq	%rbp, %rdx
 2cfdb9e:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdba3:      	movl	0x98(%rsp), %eax
 2cfdbaa:      	movl	$0x1, 0x130(%rsp)
 2cfdbb5:      	movq	$0x0, 0x138(%rsp)
 2cfdbc1:      	movq	%rax, 0x140(%rsp)
 2cfdbc9:      	movq	%r12, %rdi
 2cfdbcc:      	movq	%r14, %rsi
 2cfdbcf:      	movq	%rbp, %rdx
 2cfdbd2:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdbd7:      	movq	$0x0, 0x138(%rsp)
 2cfdbe3:      	movq	0x70(%rsp), %rax
 2cfdbe8:      	movl	%eax, 0x134(%rsp)
 2cfdbef:      	xorps	%xmm0, %xmm0
 2cfdbf2:      	movups	%xmm0, (%rbx)
 2cfdbf5:      	movl	$0x0, 0x130(%rsp)
 2cfdc00:      	movq	%r12, %rdi
 2cfdc03:      	movq	%r14, %rsi
 2cfdc06:      	movq	%rbp, %rdx
 2cfdc09:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc0e:      	movq	$0x0, 0x138(%rsp)
 2cfdc1a:      	movzbl	0xe8(%rsp), %eax
 2cfdc22:      	shll	$0x1a, %eax
 2cfdc25:      	movq	0x78(%rsp), %rcx
 2cfdc2a:      	movl	%ecx, 0x134(%rsp)
 2cfdc31:      	orl	0x10(%rsp), %eax
 2cfdc35:      	xorps	%xmm0, %xmm0
 2cfdc38:      	movups	%xmm0, (%rbx)
 2cfdc3b:      	movl	%eax, 0x130(%rsp)
 2cfdc42:      	movq	%r12, %rdi
 2cfdc45:      	movq	%r14, %rsi
 2cfdc48:      	movq	%rbp, %rdx
 2cfdc4b:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc50:      	movq	$0x0, 0x138(%rsp)
 2cfdc5c:      	movzbl	0x8(%rsp), %eax
 2cfdc61:      	shll	$0x1a, %eax
 2cfdc64:      	movl	0x120(%rsp), %ecx
 2cfdc6b:      	movl	%ecx, 0x134(%rsp)
 2cfdc72:      	orl	0x20(%rsp), %eax
 2cfdc76:      	xorps	%xmm0, %xmm0
 2cfdc79:      	movups	%xmm0, (%rbx)
 2cfdc7c:      	movl	%eax, 0x130(%rsp)
 2cfdc83:      	movq	%r12, %rdi
 2cfdc86:      	movq	%r14, %rsi
 2cfdc89:      	movq	%rbp, %rdx
 2cfdc8c:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc91:      	movq	%r12, %rdi
 2cfdc94:      	movq	%r14, %rsi
 2cfdc97:      	movq	%r15, %rdx
 2cfdc9a:      	callq	0x3651d00 <_ZN4llvm12MachineInstr12cloneMemRefsERNS_15MachineFunctionERKS0_>
 2cfdc9f:      	movq	0x30(%rsp), %rsi
 2cfdca4:      	testq	%rsi, %rsi
 2cfdca7:      	je	0x2cfdcb1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb01>
 2cfdca9:      	movq	%r13, %rdi
 2cfdcac:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfdcb1:      	movq	0xf0(%rsp), %rsi
 2cfdcb9:      	testq	%rsi, %rsi
 2cfdcbc:      	je	0x2cfe029 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfdcc2:      	leaq	0xf0(%rsp), %rdi
 2cfdcca:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfdccf:      	jmp	0x2cfe029 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfdcd4:      	movq	%rcx, 0x30(%r15)
 2cfdcd8:      	testb	$0x4, 0x20(%rcx)
 2cfdcdc:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdce2:      	testb	$0xf, 0x25(%rcx)
 2cfdce6:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdcec:      	movzbl	0x22(%rcx), %edx
 2cfdcf0:      	movq	0x8(%rcx), %rcx
 2cfdcf4:      	btsq	%rdx, %rcx
 2cfdcf8:      	movq	%rcx, %rdx
 2cfdcfb:      	negq	%rdx
 2cfdcfe:      	andq	%rcx, %rdx
 2cfdd01:      	movl	$0x7f, %ecx
 2cfdd06:      	bsrq	%rdx, %rcx
 2cfdd0a:      	xorl	$0x3e, %ecx
 2cfdd0d:      	andl	$-0x2, %ecx
 2cfdd10:      	cmpl	$0x3e, %ecx
 2cfdd13:      	je	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd19:      	movl	(%rax), %ecx
 2cfdd1b:      	movl	$0x100000ff, %edx       # imm = 0x100000FF
 2cfdd20:      	andl	%edx, %ecx
 2cfdd22:      	cmpl	$0x10000000, %ecx       # imm = 0x10000000
 2cfdd28:      	je	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd2e:      	testb	$0x10, 0x23(%rax)
 2cfdd32:      	jne	0x2cfde40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd38:      	movq	0x10(%r15), %rdx
 2cfdd3c:      	testb	$0x40, 0x12(%rdx)
 2cfdd40:      	movq	%r10, 0x8(%rsp)
 2cfdd45:      	je	0x2cfdd95 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbe5>
 2cfdd47:      	movzwl	0x28(%r15), %ecx
 2cfdd4c:      	movzbl	0x2a(%r15), %esi
 2cfdd51:      	shll	$0x10, %esi
 2cfdd54:      	orl	%ecx, %esi
 2cfdd56:      	testl	%esi, %esi
 2cfdd58:      	je	0x2cfdd95 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbe5>
 2cfdd5a:      	movzwl	(%rdx), %edi
 2cfdd5d:      	movzwl	0xa(%rdx), %r8d
 2cfdd62:      	leaq	0x10(%rax), %rcx
 2cfdd66:      	addl	%esi, %esi
 2cfdd68:      	leaq	(%rsi,%rsi,2), %rsi
 2cfdd6c:      	shll	$0x5, %edi
 2cfdd6f:      	leaq	(%r8,%r8,2), %r8
 2cfdd73:      	leaq	(%rdi,%r8,2), %rdi
 2cfdd77:      	leaq	0x22(%rdx,%rdi), %rdx
 2cfdd7c:      	xorl	%edi, %edi
 2cfdd7e:      	testb	$0x2, (%rdx,%rdi)
 2cfdd82:      	jne	0x2cfe2a2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10f2>
 2cfdd88:      	addq	$0x20, %rcx
 2cfdd8c:      	addq	$0x6, %rdi
 2cfdd90:      	cmpq	%rdi, %rsi
 2cfdd93:      	jne	0x2cfdd7e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbce>
 2cfdd95:      	movl	$0xe, %ebx
 2cfdd9a:      	movq	%r9, %rbp
 2cfdd9d:      	movl	0x4(%rax), %ecx
 2cfdda0:      	movq	%rcx, 0x20(%rsp)
 2cfdda5:      	movl	0x24(%rax), %eax
 2cfdda8:      	movl	%eax, 0x10(%rsp)
 2cfddac:      	movq	%r15, %rdi
 2cfddaf:      	callq	0x2cf7a30 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfddb4:      	cmpl	$0x0, 0x80(%rsp)
 2cfddbc:      	je	0x2cfe244 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1094>
 2cfddc2:      	cmpl	%r14d, 0x180(%rsp)
 2cfddca:      	movq	(%rsp), %rdi
 2cfddce:      	jne	0x2cfe3f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1247>
 2cfddd4:      	movl	0x10(%rsp), %ecx
 2cfddd8:      	cmpl	%ecx, 0x80(%rsp)
 2cfdddf:      	jne	0x2cfe3f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1247>
 2cfdde5:      	cmpl	%ebx, 0x118(%rsp)
 2cfddec:      	movq	%rbp, %rbx
 2cfddef:      	jne	0x2cfe2d8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1128>
 2cfddf5:      	movzwl	%r13w, %ecx
 2cfddf9:      	cmpl	$0x104b, %ecx           # imm = 0x104B
 2cfddff:      	movq	0x8(%rsp), %rbp
 2cfde04:      	jle	0x2cfe2e2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1132>
 2cfde0a:      	leal	-0x104c(%rcx), %edx
 2cfde10:      	cmpl	$0x2, %edx
 2cfde13:      	jb	0x2cfe2fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde19:      	cmpl	$0x117a, %ecx           # imm = 0x117A
 2cfde1f:      	je	0x2cfe2fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde25:      	cmpl	$0x117d, %ecx           # imm = 0x117D
 2cfde2b:      	je	0x2cfe2fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde31:      	jmp	0x2cfe418 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1268>
 2cfde36:      	nopw	%cs:(%rax,%rax)
 2cfde40:      	cmpl	$0x1101, %r14d          # imm = 0x1101
 2cfde47:      	je	0x2cfde52 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xca2>
 2cfde49:      	cmpl	$0x102f, %r14d          # imm = 0x102F
 2cfde50:      	jne	0x2cfde90 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce0>
 2cfde52:      	movq	(%rsp), %rax
 2cfde56:      	movl	0x2a0(%rax), %edx
 2cfde5c:      	cmpl	0x2a4(%rax), %edx
 2cfde62:      	jae	0x2cfe2ac <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10fc>
 2cfde68:      	movq	0x298(%rax), %rax
 2cfde6f:      	movl	%edx, %ecx
 2cfde71:      	movq	%r15, (%rax,%rcx,8)
 2cfde75:      	movq	(%rsp), %rdi
 2cfde79:      	incl	0x2a0(%rdi)
 2cfde7f:      	movq	%r15, %rbp
 2cfde82:      	movl	%r12d, %ebx
 2cfde85:      	jmp	0x2cfde9a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfde87:      	nopw	(%rax,%rax)
 2cfde90:      	movq	%r15, %rbp
 2cfde93:      	movl	%r12d, %ebx
 2cfde96:      	movq	(%rsp), %rdi
 2cfde9a:      	cmpl	$0x0, 0x240(%rsp)
 2cfdea2:      	je	0x2cfd250 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa0>
 2cfdea8:      	leaq	0x238(%rsp), %rsi
 2cfdeb0:      	callq	0x2d02350 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt14FormCandidatesERKN4llvm11SmallVectorINS0_15MemOpQueueEntryELj8EEE>
 2cfdeb5:      	movq	(%rsp), %rdi
 2cfdeb9:      	movl	$0x0, 0x240(%rsp)
 2cfdec4:      	movq	$0x0, 0x80(%rsp)
 2cfded0:      	movl	$0xffffffff, 0x180(%rsp) # imm = 0xFFFFFFFF
 2cfdedb:      	movl	$0xe, 0x118(%rsp)
 2cfdee6:      	jmp	0x2cfd250 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa0>
 2cfdeeb:      	movl	%eax, %r14d
 2cfdeee:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfdef4:      	movl	$0x7f9, 0x10(%rsp)      # imm = 0x7F9
 2cfdefc:      	movl	$0x7f9, %edx            # imm = 0x7F9
 2cfdf01:      	movl	$0x3d7, %eax            # imm = 0x3D7
 2cfdf06:      	cmovel	%eax, %edx
 2cfdf09:      	movl	%edx, 0x88(%rsp)
 2cfdf10:      	movzbl	0x230(%rsp), %r8d
 2cfdf19:      	orb	0x228(%rsp), %r8b
 2cfdf21:      	shrl	$0x1c, %r12d
 2cfdf25:      	andl	$0x1, %r12d
 2cfdf29:      	movl	0xe8(%rsp), %esi
 2cfdf30:      	xorl	%eax, %eax
 2cfdf32:      	testl	%r11d, %r11d
 2cfdf35:      	setne	%al
 2cfdf38:      	movq	%rax, 0x20(%rsp)
 2cfdf3d:      	xorl	%eax, %eax
 2cfdf3f:      	testl	%r13d, %r13d
 2cfdf42:      	setne	%al
 2cfdf45:      	cmpl	%r9d, %ebx
 2cfdf48:      	setne	%cl
 2cfdf4b:      	movq	%r9, %r11
 2cfdf4e:      	cmpl	%ebx, 0x120(%rsp)
 2cfdf55:      	sete	%dl
 2cfdf58:      	andb	%sil, %dl
 2cfdf5b:      	movl	0x8(%rsp), %edi
 2cfdf5f:      	orb	%dl, %dil
 2cfdf62:      	movl	%edi, 0x8(%rsp)
 2cfdf66:      	xorb	%sil, %dl
 2cfdf69:      	andb	%cl, %dl
 2cfdf6b:      	subq	$0x8, %rsp
 2cfdf6f:      	movq	%r10, 0x78(%rsp)
 2cfdf74:      	movzbl	%dl, %ecx
 2cfdf77:      	movq	%rcx, 0xc8(%rsp)
 2cfdf7f:      	movzbl	%r8b, %ecx
 2cfdf83:      	movl	%ecx, 0xf0(%rsp)
 2cfdf8a:      	movq	0x20(%rsp), %rbp
 2cfdf8f:      	movq	%rbp, %rdi
 2cfdf92:      	movq	%r15, %rsi
 2cfdf95:      	movl	%r14d, %r13d
 2cfdf98:      	movl	%r14d, %edx
 2cfdf9b:      	movl	0x18(%rsp), %r8d
 2cfdfa0:      	movl	%ebx, %r9d
 2cfdfa3:      	pushq	%r15
 2cfdfa5:      	movq	0x10(%rsp), %rbx
 2cfdfaa:      	pushq	0x40(%rbx)
 2cfdfad:      	pushq	%r10
 2cfdfaf:      	movq	0xb8(%rsp), %r14
 2cfdfb7:      	pushq	%r14
 2cfdfb9:      	pushq	%r12
 2cfdfbb:      	pushq	$0x0
 2cfdfbd:      	pushq	%r11
 2cfdfbf:      	pushq	%rax
 2cfdfc0:      	pushq	0x108(%rsp)
 2cfdfc7:      	callq	0x2d049c0 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfdfcc:      	addq	$0x50, %rsp
 2cfdfd0:      	addl	$0x4, %r13d
 2cfdfd4:      	subq	$0x8, %rsp
 2cfdfd8:      	movzbl	0x10(%rsp), %eax
 2cfdfdd:      	andl	$0x1, %eax
 2cfdfe0:      	movq	%rbp, %rdi
 2cfdfe3:      	movq	%r15, %rsi
 2cfdfe6:      	movl	%r13d, %edx
 2cfdfe9:      	movl	0xf0(%rsp), %ecx
 2cfdff0:      	movl	0x90(%rsp), %r8d
 2cfdff8:      	movl	0x128(%rsp), %r9d
 2cfe000:      	pushq	%r15
 2cfe002:      	pushq	0x40(%rbx)
 2cfe005:      	pushq	0x88(%rsp)
 2cfe00c:      	pushq	%r14
 2cfe00e:      	pushq	%r12
 2cfe010:      	pushq	0x110(%rsp)
 2cfe017:      	pushq	0x60(%rsp)
 2cfe01b:      	pushq	0x60(%rsp)
 2cfe01f:      	pushq	%rax
 2cfe020:      	callq	0x2d049c0 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfe025:      	addq	$0x50, %rsp
 2cfe029:      	testb	$0x4, (%r15)
 2cfe02d:      	movq	%r15, %rax
 2cfe030:      	xorps	%xmm0, %xmm0
 2cfe033:      	jne	0x2cfe05a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeaa>
 2cfe035:      	testb	$0x8, 0x2c(%r15)
 2cfe03a:      	movq	%r15, %rax
 2cfe03d:      	je	0x2cfe05a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeaa>
 2cfe03f:      	movq	%r15, %rax
 2cfe042:      	nopw	%cs:(%rax,%rax)
 2cfe04c:      	nopl	(%rax)
 2cfe050:      	movq	0x8(%rax), %rax
 2cfe054:      	testb	$0x8, 0x2c(%rax)
 2cfe058:      	jne	0x2cfe050 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xea0>
 2cfe05a:      	movq	0x8(%rax), %rax
 2cfe05e:      	movq	%rax, 0x10(%rsp)
 2cfe063:      	cmpq	%rax, %r15
 2cfe066:      	jne	0x2cfe0af <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeff>
 2cfe068:      	movq	0x10(%rsp), %r15
 2cfe06d:      	movq	0x90(%rsp), %r12
 2cfe075:      	movq	(%rsp), %rdi
 2cfe079:      	jmp	0x2cfd256 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa6>
 2cfe07e:      	nop
 2cfe080:      	movl	%ecx, 0xf0(%rbp)
 2cfe086:      	movq	(%r14), %rax
 2cfe089:      	movq	(%rax,%r12,8), %rcx
 2cfe08d:      	movq	%rcx, (%rbx)
 2cfe090:      	movq	%rbx, (%rax,%r12,8)
 2cfe094:      	movq	0xe0(%rbp), %rax
 2cfe09b:      	movq	%rax, (%r15)
 2cfe09e:      	movq	%r15, 0xe0(%rbp)
 2cfe0a5:      	movq	%r13, %r15
 2cfe0a8:      	cmpq	0x10(%rsp), %r13
 2cfe0ad:      	je	0x2cfe068 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeb8>
 2cfe0af:      	movq	0x8(%r15), %r13
 2cfe0b3:      	movq	0x18(%r15), %rax
 2cfe0b7:      	movq	0x20(%rax), %rbx
 2cfe0bb:      	testq	%rbx, %rbx
 2cfe0be:      	je	0x2cfe170 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe0c4:      	movq	0x288(%rbx), %rdi
 2cfe0cb:      	testq	%rdi, %rdi
 2cfe0ce:      	je	0x2cfe0dc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf2c>
 2cfe0d0:      	movq	(%rdi), %rax
 2cfe0d3:      	movq	%r15, %rsi
 2cfe0d6:      	callq	*0x20(%rax)
 2cfe0d9:      	xorps	%xmm0, %xmm0
 2cfe0dc:      	movzwl	0x28(%r15), %ecx
 2cfe0e1:      	movzbl	0x2a(%r15), %eax
 2cfe0e6:      	shll	$0x10, %eax
 2cfe0e9:      	orl	%ecx, %eax
 2cfe0eb:      	testl	%eax, %eax
 2cfe0ed:      	je	0x2cfe170 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe0f3:      	movq	0x20(%r15), %rcx
 2cfe0f7:      	shll	$0x5, %eax
 2cfe0fa:      	movq	0x20(%rbx), %rdx
 2cfe0fe:      	jmp	0x2cfe121 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf71>
 2cfe100:      	movq	%rdi, 0x18(%r8)
 2cfe104:      	leaq	0x10(%rcx), %r9
 2cfe108:      	testq	%rdi, %rdi
 2cfe10b:      	cmovneq	%rdi, %rsi
 2cfe10f:      	movq	%r8, 0x10(%rsi)
 2cfe113:      	movups	%xmm0, (%r9)
 2cfe117:      	addq	$0x20, %rcx
 2cfe11b:      	addq	$-0x20, %rax
 2cfe11f:      	je	0x2cfe170 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe121:      	cmpb	$0x0, (%rcx)
 2cfe124:      	jne	0x2cfe117 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf67>
 2cfe126:      	movl	0x4(%rcx), %esi
 2cfe129:      	movl	%esi, %edi
 2cfe12b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2cfe131:      	shlq	$0x4, %rdi
 2cfe135:      	movq	%rsi, %r8
 2cfe138:      	shlq	$0x3, %r8
 2cfe13c:      	addq	0x128(%rdx), %r8
 2cfe143:      	testl	%esi, %esi
 2cfe145:      	movq	0x30(%rdx), %rsi
 2cfe149:      	leaq	0x8(%rsi,%rdi), %r9
 2cfe14e:      	cmovnsq	%r8, %r9
 2cfe152:      	movq	(%r9), %rsi
 2cfe155:      	movq	0x18(%rcx), %rdi
 2cfe159:      	movq	0x10(%rcx), %r8
 2cfe15d:      	cmpq	%rsi, %rcx
 2cfe160:      	jne	0x2cfe100 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf50>
 2cfe162:      	movq	%rdi, (%r9)
 2cfe165:      	jmp	0x2cfe104 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf54>
 2cfe167:      	nopw	(%rax,%rax)
 2cfe170:      	movq	$0x0, 0x18(%r15)
 2cfe178:      	movq	(%r15), %rax
 2cfe17b:      	movq	0x8(%r15), %rcx
 2cfe17f:      	andq	$-0x8, %rax
 2cfe183:      	movq	(%rcx), %rdx
 2cfe186:      	andl	$0x7, %edx
 2cfe189:      	orq	%rax, %rdx
 2cfe18c:      	movq	%rdx, (%rcx)
 2cfe18f:      	movq	%rcx, 0x8(%rax)
 2cfe193:      	andq	$0x7, (%r15)
 2cfe197:      	movq	$0x0, 0x8(%r15)
 2cfe19f:      	movq	0x18(%rsp), %rax
 2cfe1a4:      	movq	0x28(%rax), %rax
 2cfe1a8:      	movq	0x20(%rax), %rbp
 2cfe1ac:      	movq	0x20(%r15), %rbx
 2cfe1b0:      	testq	%rbx, %rbx
 2cfe1b3:      	je	0x2cfe094 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xee4>
 2cfe1b9:      	movzbl	0x2b(%r15), %r12d
 2cfe1be:      	leaq	0xe8(%rbp), %r14
 2cfe1c5:      	movl	0xf0(%rbp), %eax
 2cfe1cb:      	cmpl	%r12d, %eax
 2cfe1ce:      	ja	0x2cfe086 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed6>
 2cfe1d4:      	leaq	0x1(%r12), %rcx
 2cfe1d9:      	cmpl	%r12d, 0xf4(%rbp)
 2cfe1e0:      	ja	0x2cfe209 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1059>
 2cfe1e2:      	leaq	0xf8(%rbp), %rsi
 2cfe1e9:      	movl	$0x8, %ecx
 2cfe1ee:      	movq	%r14, %rdi
 2cfe1f1:      	leaq	0x1(%r12), %rdx
 2cfe1f6:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe1fb:      	leaq	0x1(%r12), %rcx
 2cfe200:      	xorps	%xmm0, %xmm0
 2cfe203:      	movl	0xf0(%rbp), %eax
 2cfe209:      	cmpl	%eax, %ecx
 2cfe20b:      	je	0x2cfe080 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed0>
 2cfe211:      	movl	%eax, %eax
 2cfe213:      	leaq	(,%rax,8), %rdi
 2cfe21b:      	addq	(%r14), %rdi
 2cfe21e:      	movq	%rcx, %r14
 2cfe221:      	movq	%rcx, %rdx
 2cfe224:      	subq	%rax, %rdx
 2cfe227:      	shlq	$0x3, %rdx
 2cfe22b:      	xorl	%esi, %esi
 2cfe22d:      	callq	0x828ab90 <memset@plt>
 2cfe232:      	movq	%r14, %rcx
 2cfe235:      	leaq	0xe8(%rbp), %r14
 2cfe23c:      	xorps	%xmm0, %xmm0
 2cfe23f:      	jmp	0x2cfe080 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed0>
 2cfe244:      	movl	0x240(%rsp), %edx
 2cfe24b:      	cmpl	0x244(%rsp), %edx
 2cfe252:      	jae	0x2cfe541 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1391>
 2cfe258:      	movq	%r12, %rcx
 2cfe25b:      	shlq	$0x20, %rcx
 2cfe25f:      	movl	%eax, %eax
 2cfe261:      	orq	%rcx, %rax
 2cfe264:      	movq	0x238(%rsp), %rcx
 2cfe26c:      	movl	%edx, %edx
 2cfe26e:      	shlq	$0x4, %rdx
 2cfe272:      	movq	%r15, (%rcx,%rdx)
 2cfe276:      	movq	%rax, 0x8(%rcx,%rdx)
 2cfe27b:      	incl	0x240(%rsp)
 2cfe282:      	movl	%ebx, 0x118(%rsp)
 2cfe289:      	movl	%r14d, 0x180(%rsp)
 2cfe291:      	movl	0x10(%rsp), %eax
 2cfe295:      	movq	%rax, 0x80(%rsp)
 2cfe29d:      	jmp	0x2cfe075 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe2a2:      	movq	%r9, %rbp
 2cfe2a5:      	movl	(%rcx), %ebx
 2cfe2a7:      	jmp	0x2cfdd9d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbed>
 2cfe2ac:      	incq	%rdx
 2cfe2af:      	movl	$0x8, %ecx
 2cfe2b4:      	movq	0x1f8(%rsp), %rdi
 2cfe2bc:      	movq	0x220(%rsp), %rsi
 2cfe2c4:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe2c9:      	movq	(%rsp), %rax
 2cfe2cd:      	movl	0x2a0(%rax), %edx
 2cfe2d3:      	jmp	0x2cfde68 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcb8>
 2cfe2d8:      	movq	0x8(%rsp), %rbp
 2cfe2dd:      	jmp	0x2cfde9a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe2e2:      	cmpl	$0x3d7, %ecx            # imm = 0x3D7
 2cfe2e8:      	je	0x2cfe2fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfe2ea:      	cmpl	$0xb51, %ecx            # imm = 0xB51
 2cfe2f0:      	je	0x2cfe2fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfe2f2:      	cmpl	$0xb53, %ecx            # imm = 0xB53
 2cfe2f8:      	jne	0x2cfe418 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1268>
 2cfe2fe:      	movq	0x20(%rsp), %rcx
 2cfe303:      	cmpl	%ecx, 0x80(%rsp)
 2cfe30a:      	je	0x2cfde96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe310:      	movq	0x238(%rsp), %r13
 2cfe318:      	movl	0x240(%rsp), %edx
 2cfe31f:      	testq	%rdx, %rdx
 2cfe322:      	je	0x2cfe404 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1254>
 2cfe328:      	movq	%rbx, %rbp
 2cfe32b:      	movq	%rdx, %rcx
 2cfe32e:      	shlq	$0x4, %rcx
 2cfe332:      	movq	0x20(%rsp), %rsi
 2cfe337:      	leal	-0x1(%rsi), %edi
 2cfe33a:      	movq	(%rsp), %rsi
 2cfe33e:      	movq	0x48(%rsi), %r8
 2cfe342:      	movq	%r13, %r9
 2cfe345:      	jmp	0x2cfe359 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x11a9>
 2cfe347:      	addq	$0x10, %r9
 2cfe34b:      	leaq	(%r13,%rcx), %rsi
 2cfe350:      	cmpq	%rsi, %r9
 2cfe353:      	je	0x2cfe46a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12ba>
 2cfe359:      	movq	(%r9), %r10
 2cfe35c:      	movq	0x20(%r10), %r10
 2cfe360:      	movl	0x4(%r10), %ebx
 2cfe364:      	cmpl	%ebx, 0x20(%rsp)
 2cfe368:      	je	0x2cfe3f3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1243>
 2cfe36e:      	cmpl	$0x3ffffffe, %edi       # imm = 0x3FFFFFFE
 2cfe374:      	ja	0x2cfe347 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe376:      	leal	-0x1(%rbx), %r10d
 2cfe37a:      	cmpl	$0x3ffffffe, %r10d      # imm = 0x3FFFFFFE
 2cfe381:      	ja	0x2cfe347 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe383:      	movq	0x20(%rsp), %rsi
 2cfe388:      	leaq	(%rsi,%rsi,2), %r10
 2cfe38c:      	movq	0x8(%r8), %r14
 2cfe390:      	movq	0x38(%r8), %rsi
 2cfe394:      	movl	0x10(%r14,%r10,8), %r11d
 2cfe399:      	movl	%r11d, %r10d
 2cfe39c:      	andl	$0xfff, %r10d           # imm = 0xFFF
 2cfe3a3:      	shrl	$0xc, %r11d
 2cfe3a7:      	leaq	(%rsi,%r11,2), %r11
 2cfe3ab:      	leaq	(%rbx,%rbx,2), %rbx
 2cfe3af:      	movl	0x10(%r14,%rbx,8), %r14d
 2cfe3b4:      	movl	%r14d, %ebx
 2cfe3b7:      	andl	$0xfff, %ebx            # imm = 0xFFF
 2cfe3bd:      	shrl	$0xc, %r14d
 2cfe3c1:      	leaq	(%rsi,%r14,2), %r14
 2cfe3c5:      	cmpl	%ebx, %r10d
 2cfe3c8:      	je	0x2cfe3f3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1243>
 2cfe3ca:      	jae	0x2cfe3e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1230>
 2cfe3cc:      	movswl	(%r11), %esi
 2cfe3d0:      	addq	$0x2, %r11
 2cfe3d4:      	addl	%esi, %r10d
 2cfe3d7:      	testl	%esi, %esi
 2cfe3d9:      	jne	0x2cfe3c5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1215>
 2cfe3db:      	jmp	0x2cfe347 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe3e0:      	movswl	(%r14), %esi
 2cfe3e4:      	addq	$0x2, %r14
 2cfe3e8:      	addl	%esi, %ebx
 2cfe3ea:      	testl	%esi, %esi
 2cfe3ec:      	jne	0x2cfe3c5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1215>
 2cfe3ee:      	jmp	0x2cfe347 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe3f3:      	movq	(%rsp), %rdi
 2cfe3f7:      	movq	%rbp, %rbx
 2cfe3fa:      	movq	0x8(%rsp), %rbp
 2cfe3ff:      	jmp	0x2cfde9a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe404:      	cmpl	-0x8(%r13), %eax
 2cfe408:      	movq	(%rsp), %rdi
 2cfe40c:      	jle	0x2cfde9a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe412:      	xorl	%edx, %edx
 2cfe414:      	xorl	%esi, %esi
 2cfe416:      	jmp	0x2cfe437 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1287>
 2cfe418:      	movl	0x240(%rsp), %edx
 2cfe41f:      	movq	0x238(%rsp), %r13
 2cfe427:      	movq	%rdx, %rcx
 2cfe42a:      	shlq	$0x4, %rcx
 2cfe42e:      	movl	%edx, %esi
 2cfe430:      	cmpl	-0x8(%r13,%rcx), %eax
 2cfe435:      	jle	0x2cfe47b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12cb>
 2cfe437:      	cmpl	0x244(%rsp), %esi
 2cfe43e:      	jae	0x2cfe56e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x13be>
 2cfe444:      	movq	%r12, %rcx
 2cfe447:      	shlq	$0x20, %rcx
 2cfe44b:      	movl	%eax, %eax
 2cfe44d:      	orq	%rcx, %rax
 2cfe450:      	shlq	$0x4, %rdx
 2cfe454:      	movq	%r15, (%r13,%rdx)
 2cfe459:      	movq	%rax, 0x8(%r13,%rdx)
 2cfe45e:      	incl	0x240(%rsp)
 2cfe465:      	jmp	0x2cfe075 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe46a:      	movl	%edx, %esi
 2cfe46c:      	movq	%rbp, %rbx
 2cfe46f:      	movq	0x8(%rsp), %rbp
 2cfe474:      	cmpl	-0x8(%r13,%rcx), %eax
 2cfe479:      	jg	0x2cfe437 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1287>
 2cfe47b:      	testl	%esi, %esi
 2cfe47d:      	je	0x2cfe4a7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12f7>
 2cfe47f:      	leaq	-0x10(%rcx), %rdi
 2cfe483:      	movq	%r13, %r14
 2cfe486:      	movl	0x8(%r14), %r8d
 2cfe48a:      	cmpl	%r8d, %eax
 2cfe48d:      	jl	0x2cfe4ac <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12fc>
 2cfe48f:      	je	0x2cfde96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe495:      	addq	$0x10, %r14
 2cfe499:      	testq	%rdi, %rdi
 2cfe49c:      	leaq	-0x10(%rdi), %rdi
 2cfe4a0:      	jne	0x2cfe486 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12d6>
 2cfe4a2:      	jmp	0x2cfde96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe4a7:      	xorl	%edx, %edx
 2cfe4a9:      	movq	%r13, %r14
 2cfe4ac:      	addq	%r13, %rcx
 2cfe4af:      	cmpq	%rcx, %r14
 2cfe4b2:      	movq	(%rsp), %rdi
 2cfe4b6:      	je	0x2cfde9a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe4bc:      	cmpl	0x244(%rsp), %esi
 2cfe4c3:      	jae	0x2cfe5a3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x13f3>
 2cfe4c9:      	movq	%r13, %rcx
 2cfe4cc:      	movl	%eax, %ebx
 2cfe4ce:      	subq	%r13, %r14
 2cfe4d1:      	addq	%rcx, %r14
 2cfe4d4:      	shlq	$0x4, %rdx
 2cfe4d8:      	movups	-0x10(%rcx,%rdx), %xmm0
 2cfe4dd:      	movups	%xmm0, (%rcx,%rdx)
 2cfe4e1:      	movq	0x238(%rsp), %rdi
 2cfe4e9:      	movl	0x240(%rsp), %ecx
 2cfe4f0:      	shlq	$0x4, %rcx
 2cfe4f4:      	leaq	-0x10(%rdi,%rcx), %rax
 2cfe4f9:      	movq	%rax, %rdx
 2cfe4fc:      	subq	%r14, %rdx
 2cfe4ff:      	movq	%rdx, %rsi
 2cfe502:      	sarq	$0x4, %rsi
 2cfe506:      	cmpq	$0x2, %rsi
 2cfe50a:      	jl	0x2cfe5d8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1428>
 2cfe510:      	addq	%rcx, %rdi
 2cfe513:      	shlq	$0x4, %rsi
 2cfe517:      	subq	%rsi, %rdi
 2cfe51a:      	movq	%r14, %rsi
 2cfe51d:      	callq	0x828abc0 <memmove@plt>
 2cfe522:      	movl	%ebx, %eax
 2cfe524:      	movq	%r12, %rcx
 2cfe527:      	incl	0x240(%rsp)
 2cfe52e:      	shlq	$0x20, %rcx
 2cfe532:      	orq	%rax, %rcx
 2cfe535:      	movq	%r15, (%r14)
 2cfe538:      	movq	%rcx, 0x8(%r14)
 2cfe53c:      	jmp	0x2cfe075 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe541:      	incq	%rdx
 2cfe544:      	movl	$0x10, %ecx
 2cfe549:      	leaq	0x238(%rsp), %rdi
 2cfe551:      	leaq	0x248(%rsp), %rsi
 2cfe559:      	movl	%eax, %ebp
 2cfe55b:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe560:      	movl	%ebp, %eax
 2cfe562:      	movl	0x240(%rsp), %edx
 2cfe569:      	jmp	0x2cfe258 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10a8>
 2cfe56e:      	incq	%rdx
 2cfe571:      	movl	$0x10, %ecx
 2cfe576:      	leaq	0x238(%rsp), %rdi
 2cfe57e:      	leaq	0x248(%rsp), %rsi
 2cfe586:      	movl	%eax, %ebx
 2cfe588:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe58d:      	movl	%ebx, %eax
 2cfe58f:      	movl	0x240(%rsp), %edx
 2cfe596:      	movq	0x238(%rsp), %r13
 2cfe59e:      	jmp	0x2cfe444 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1294>
 2cfe5a3:      	incq	%rdx
 2cfe5a6:      	movl	$0x10, %ecx
 2cfe5ab:      	leaq	0x238(%rsp), %rdi
 2cfe5b3:      	leaq	0x248(%rsp), %rsi
 2cfe5bb:      	movl	%eax, %ebx
 2cfe5bd:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe5c2:      	movl	%ebx, %eax
 2cfe5c4:      	movq	0x238(%rsp), %rcx
 2cfe5cc:      	movl	0x240(%rsp), %edx
 2cfe5d3:      	jmp	0x2cfe4cc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x131c>
 2cfe5d8:      	cmpq	$0x10, %rdx
 2cfe5dc:      	jne	0x2cfe522 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1372>
 2cfe5e2:      	movups	(%r14), %xmm0
 2cfe5e6:      	movups	%xmm0, (%rax)
 2cfe5e9:      	jmp	0x2cfe522 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1372>
 2cfe5ee:      	cmpl	$0x0, 0x240(%rsp)
 2cfe5f6:      	je	0x2cfe609 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1459>
 2cfe5f8:      	leaq	0x238(%rsp), %rsi
 2cfe600:      	callq	0x2d02350 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt14FormCandidatesERKN4llvm11SmallVectorINS0_15MemOpQueueEntryELj8EEE>
 2cfe605:      	movq	(%rsp), %rdi
 2cfe609:      	movl	0x270(%rdi), %r14d
 2cfe610:      	testq	%r14, %r14
 2cfe613:      	je	0x2d02161 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb1>
 2cfe619:      	movq	0x268(%rdi), %rbx
 2cfe620:      	leaq	(%rbx,%r14,8), %r13
 2cfe624:      	bsrq	%r14, %rdx
 2cfe628:      	xorl	$0x3f, %edx
 2cfe62b:      	addl	%edx, %edx
 2cfe62d:      	xorq	$0x7e, %rdx
 2cfe631:      	movq	%rbx, %rdi
 2cfe634:      	movq	%r13, %rsi
 2cfe637:      	callq	0x2d04cf0 <_ZSt16__introsort_loopIPPKN12_GLOBAL__N_115ARMLoadStoreOpt14MergeCandidateElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockEE3$_0EEEvT_SE_T0_T1_>
 2cfe63c:      	leaq	0x8(%rbx), %r15
 2cfe640:      	cmpl	$0x11, %r14d
 2cfe644:      	jb	0x2cfe65d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14ad>
 2cfe646:      	movq	%r13, 0x18(%rsp)
 2cfe64b:      	leaq	0x8(%rbx), %r13
 2cfe64f:      	movl	$0x8, %r12d
 2cfe655:      	movq	%rbx, %rbp
 2cfe658:      	jmp	0x2d02297 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50e7>
 2cfe65d:      	cmpl	$0x1, %r14d
 2cfe661:      	jne	0x2d021e1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5031>
 2cfe667:      	movq	(%rsp), %rdi
 2cfe66b:      	movl	0x270(%rdi), %eax
 2cfe671:      	testq	%rax, %rax
 2cfe674:      	je	0x2d02161 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb1>
 2cfe67a:      	movq	0x268(%rdi), %rcx
 2cfe681:      	leaq	(%rcx,%rax,8), %rax
 2cfe685:      	movq	%rax, 0xe8(%rsp)
 2cfe68d:      	leaq	0x68(%rdi), %rax
 2cfe691:      	movq	%rax, 0x118(%rsp)
 2cfe699:      	leaq	0x70(%rdi), %rax
 2cfe69d:      	movq	%rax, 0xe0(%rsp)
 2cfe6a5:      	leaq	0x80(%rdi), %rax
 2cfe6ac:      	movq	%rax, 0x220(%rsp)
 2cfe6b4:      	leaq	0xb8(%rdi), %rax
 2cfe6bb:      	movq	%rax, 0x1f8(%rsp)
 2cfe6c3:      	xorps	%xmm0, %xmm0
 2cfe6c6:      	xorl	%eax, %eax
 2cfe6c8:      	jmp	0x2cfe709 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1559>
 2cfe6ca:      	nopw	(%rax,%rax)
 2cfe6d0:      	movq	(%rax), %rax
 2cfe6d3:      	movq	(%rax), %rsi
 2cfe6d6:      	callq	0x2d03380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt24MergeBaseUpdateLoadStoreEPN4llvm12MachineInstrE>
 2cfe6db:      	movq	(%rsp), %rdi
 2cfe6df:      	movq	0x98(%rsp), %rcx
 2cfe6e7:      	orb	%al, %cl
 2cfe6e9:      	movq	%rcx, %rax
 2cfe6ec:      	movq	0x120(%rsp), %rcx
 2cfe6f4:      	addq	$0x8, %rcx
 2cfe6f8:      	cmpq	0xe8(%rsp), %rcx
 2cfe700:      	xorps	%xmm0, %xmm0
 2cfe703:      	je	0x2d02163 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb3>
 2cfe709:      	movq	%rax, 0x98(%rsp)
 2cfe711:      	movq	(%rcx), %rax
 2cfe714:      	cmpb	$0x0, 0x3c(%rax)
 2cfe718:      	movq	%rcx, 0x120(%rsp)
 2cfe720:      	jne	0x2cfe728 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1578>
 2cfe722:      	cmpb	$0x1, 0x3d(%rax)
 2cfe726:      	jne	0x2cfe6d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1520>
 2cfe728:      	movq	%rax, 0x90(%rsp)
 2cfe730:      	movq	(%rax), %r14
 2cfe733:      	movq	(%r14), %rbp
 2cfe736:      	movzwl	0x44(%rbp), %ebx
 2cfe73a:      	movb	$0x1, %al
 2cfe73c:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cfe742:      	je	0x2cfe761 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe744:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cfe74a:      	je	0x2cfe761 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe74c:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cfe752:      	je	0x2cfe761 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe754:      	movl	%ebx, %eax
 2cfe756:      	andl	$-0x2, %eax
 2cfe759:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cfe75e:      	sete	%al
 2cfe761:      	movl	%ebx, %ecx
 2cfe763:      	andl	$-0x3, %ecx
 2cfe766:      	movl	%ecx, 0xc0(%rsp)
 2cfe76d:      	cmpl	$0xb51, %ecx            # imm = 0xB51
 2cfe773:      	sete	%r15b
 2cfe777:      	leaq	0x140(%rsp), %rcx
 2cfe77f:      	movq	%rcx, 0x130(%rsp)
 2cfe787:      	movabsq	$0x800000000, %rcx      # imm = 0x800000000
 2cfe791:      	movq	%rcx, 0x138(%rsp)
 2cfe799:      	leaq	0x1d0(%rsp), %rcx
 2cfe7a1:      	movq	%rcx, 0x1c0(%rsp)
 2cfe7a9:      	movabsq	$0x400000000, %rcx      # imm = 0x400000000
 2cfe7b3:      	movq	%rcx, 0x1c8(%rsp)
 2cfe7bb:      	movaps	%xmm0, 0x200(%rsp)
 2cfe7c3:      	movl	$0x0, 0x210(%rsp)
 2cfe7ce:      	movaps	%xmm0, 0x1e0(%rsp)
 2cfe7d6:      	movl	$0x0, 0x1f0(%rsp)
 2cfe7e1:      	movq	0x90(%rsp), %rcx
 2cfe7e9:      	movl	0x8(%rcx), %ecx
 2cfe7ec:      	testq	%rcx, %rcx
 2cfe7ef:      	movq	%rbx, 0x78(%rsp)
 2cfe7f4:      	je	0x2cfed70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bc0>
 2cfe7fa:      	movq	%rbp, 0x10(%rsp)
 2cfe7ff:      	orb	%al, %r15b
 2cfe802:      	leaq	(%r14,%rcx,8), %rax
 2cfe806:      	movq	%rax, 0x18(%rsp)
 2cfe80b:      	jmp	0x2cfe81f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x166f>
 2cfe80d:      	nopl	(%rax)
 2cfe810:      	addq	$0x8, %r14
 2cfe814:      	cmpq	0x18(%rsp), %r14
 2cfe819:      	je	0x2cfed50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ba0>
 2cfe81f:      	movq	(%r14), %rbx
 2cfe822:      	movq	0x20(%rbx), %rax
 2cfe826:      	movl	(%rax), %ecx
 2cfe828:      	movl	0x4(%rax), %ebp
 2cfe82b:      	movl	%ecx, %eax
 2cfe82d:      	shrl	$0x1a, %eax
 2cfe830:      	xorl	%r12d, %r12d
 2cfe833:      	testl	$0x1000000, %ecx        # imm = 0x1000000
 2cfe839:      	sete	%r12b
 2cfe83d:      	andl	%eax, %r12d
 2cfe840:      	je	0x2cfe8fc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe846:      	movl	0x210(%rsp), %esi
 2cfe84d:      	testl	%esi, %esi
 2cfe84f:      	je	0x2cfe8b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1700>
 2cfe851:      	movq	0x200(%rsp), %rcx
 2cfe859:      	leal	(%rbp,%rbp,8), %eax
 2cfe85d:      	leal	(%rbp,%rax,4), %edx
 2cfe861:      	leal	-0x1(%rsi), %edi
 2cfe864:      	andl	%edi, %edx
 2cfe866:      	movl	(%rcx,%rdx,4), %r10d
 2cfe86a:      	cmpl	%r10d, %ebp
 2cfe86d:      	je	0x2cfe8fc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe873:      	leaq	(%rcx,%rdx,4), %rax
 2cfe877:      	movl	$0x1, %r8d
 2cfe87d:      	xorl	%r9d, %r9d
 2cfe880:      	cmpl	$-0x1, %r10d
 2cfe884:      	je	0x2cfec09 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a59>
 2cfe88a:      	testq	%r9, %r9
 2cfe88d:      	cmovneq	%r9, %rax
 2cfe891:      	cmpl	$-0x2, %r10d
 2cfe895:      	cmoveq	%rax, %r9
 2cfe899:      	addl	%r8d, %edx
 2cfe89c:      	incl	%r8d
 2cfe89f:      	andl	%edi, %edx
 2cfe8a1:      	leaq	(%rcx,%rdx,4), %rax
 2cfe8a5:      	movl	(%rcx,%rdx,4), %r10d
 2cfe8a9:      	cmpl	%r10d, %ebp
 2cfe8ac:      	je	0x2cfe8fc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe8ae:      	jmp	0x2cfe880 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x16d0>
 2cfe8b0:      	xorl	%eax, %eax
 2cfe8b2:      	movl	0x208(%rsp), %ecx
 2cfe8b9:      	leal	0x4(,%rcx,4), %edx
 2cfe8c0:      	leal	(%rsi,%rsi,2), %edi
 2cfe8c3:      	cmpl	%edi, %edx
 2cfe8c5:      	jae	0x2cfeca6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1af6>
 2cfe8cb:      	movl	%ecx, %edx
 2cfe8cd:      	notl	%edx
 2cfe8cf:      	addl	%esi, %edx
 2cfe8d1:      	subl	0x20c(%rsp), %edx
 2cfe8d8:      	movl	%esi, %edi
 2cfe8da:      	shrl	$0x3, %edi
 2cfe8dd:      	cmpl	%edi, %edx
 2cfe8df:      	jbe	0x2cfeca8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1af8>
 2cfe8e5:      	incl	%ecx
 2cfe8e7:      	movl	%ecx, 0x208(%rsp)
 2cfe8ee:      	cmpl	$-0x1, (%rax)
 2cfe8f1:      	je	0x2cfe8fa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174a>
 2cfe8f3:      	decl	0x20c(%rsp)
 2cfe8fa:      	movl	%ebp, (%rax)
 2cfe8fc:      	movl	0x138(%rsp), %edx
 2cfe903:      	cmpl	0x13c(%rsp), %edx
 2cfe90a:      	jae	0x2cfebd4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a24>
 2cfe910:      	shlq	$0x20, %r12
 2cfe914:      	orq	%rbp, %r12
 2cfe917:      	movq	0x130(%rsp), %rax
 2cfe91f:      	movl	%edx, %ecx
 2cfe921:      	movq	%r12, (%rax,%rcx,8)
 2cfe925:      	incl	0x138(%rsp)
 2cfe92c:      	movl	0x1f0(%rsp), %esi
 2cfe933:      	testl	%esi, %esi
 2cfe935:      	je	0x2cfe9a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17f0>
 2cfe937:      	movq	0x1e0(%rsp), %rcx
 2cfe93f:      	leal	(%rbp,%rbp,8), %eax
 2cfe943:      	leal	(%rbp,%rax,4), %edx
 2cfe947:      	leal	-0x1(%rsi), %edi
 2cfe94a:      	andl	%edi, %edx
 2cfe94c:      	movl	(%rcx,%rdx,4), %r10d
 2cfe950:      	cmpl	%r10d, %ebp
 2cfe953:      	je	0x2cfe9ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183c>
 2cfe959:      	leaq	(%rcx,%rdx,4), %rax
 2cfe95d:      	movl	$0x1, %r8d
 2cfe963:      	xorl	%r9d, %r9d
 2cfe966:      	cmpl	$-0x1, %r10d
 2cfe96a:      	je	0x2cfebfd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a4d>
 2cfe970:      	testq	%r9, %r9
 2cfe973:      	cmovneq	%r9, %rax
 2cfe977:      	cmpl	$-0x2, %r10d
 2cfe97b:      	cmoveq	%rax, %r9
 2cfe97f:      	addl	%r8d, %edx
 2cfe982:      	incl	%r8d
 2cfe985:      	andl	%edi, %edx
 2cfe987:      	leaq	(%rcx,%rdx,4), %rax
 2cfe98b:      	movl	(%rcx,%rdx,4), %r10d
 2cfe98f:      	cmpl	%r10d, %ebp
 2cfe992:      	je	0x2cfe9ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183c>
 2cfe994:      	jmp	0x2cfe966 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17b6>
 2cfe996:      	nopw	%cs:(%rax,%rax)
 2cfe9a0:      	xorl	%eax, %eax
 2cfe9a2:      	movl	0x1e8(%rsp), %ecx
 2cfe9a9:      	leal	0x4(,%rcx,4), %edx
 2cfe9b0:      	leal	(%rsi,%rsi,2), %edi
 2cfe9b3:      	cmpl	%edi, %edx
 2cfe9b5:      	jae	0x2cfec15 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a65>
 2cfe9bb:      	movl	%ecx, %edx
 2cfe9bd:      	notl	%edx
 2cfe9bf:      	addl	%esi, %edx
 2cfe9c1:      	subl	0x1ec(%rsp), %edx
 2cfe9c8:      	movl	%esi, %edi
 2cfe9ca:      	shrl	$0x3, %edi
 2cfe9cd:      	cmpl	%edi, %edx
 2cfe9cf:      	jbe	0x2cfec17 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a67>
 2cfe9d5:      	incl	%ecx
 2cfe9d7:      	movl	%ecx, 0x1e8(%rsp)
 2cfe9de:      	cmpl	$-0x1, (%rax)
 2cfe9e1:      	je	0x2cfe9ea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183a>
 2cfe9e3:      	decl	0x1ec(%rsp)
 2cfe9ea:      	movl	%ebp, (%rax)
 2cfe9ec:      	testb	%r15b, %r15b
 2cfe9ef:      	je	0x2cfe810 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfe9f5:      	movq	0x10(%rbx), %rdx
 2cfe9f9:      	movq	0x20(%rbx), %rax
 2cfe9fd:      	movzwl	0x28(%rbx), %ecx
 2cfea01:      	movzbl	0x2a(%rbx), %r12d
 2cfea06:      	shll	$0x10, %r12d
 2cfea0a:      	orq	%rcx, %r12
 2cfea0d:      	movzwl	0x2(%rdx), %ecx
 2cfea11:      	testb	$0x2, 0x10(%rdx)
 2cfea15:      	je	0x2cfea50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea17:      	movl	%ecx, %edx
 2cfea19:      	cmpq	%r12, %rdx
 2cfea1c:      	movl	$0x20000ff, %r8d        # imm = 0x20000FF
 2cfea22:      	je	0x2cfea50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea24:      	movl	%r12d, %esi
 2cfea27:      	shll	$0x5, %esi
 2cfea2a:      	shll	$0x5, %edx
 2cfea2d:      	nopl	(%rax)
 2cfea30:      	movl	(%rax,%rdx), %edi
 2cfea33:      	andl	%r8d, %edi
 2cfea36:      	cmpl	$0x2000000, %edi        # imm = 0x2000000
 2cfea3c:      	je	0x2cfea50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea3e:      	incl	%ecx
 2cfea40:      	addq	$0x20, %rdx
 2cfea44:      	cmpq	%rdx, %rsi
 2cfea47:      	jne	0x2cfea30 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1880>
 2cfea49:      	nopl	(%rax)
 2cfea50:      	movl	%ecx, %r13d
 2cfea53:      	cmpq	%r12, %r13
 2cfea56:      	je	0x2cfe810 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfea5c:      	shll	$0x5, %r12d
 2cfea60:      	addq	%rax, %r12
 2cfea63:      	shlq	$0x5, %r13
 2cfea67:      	addq	%rax, %r13
 2cfea6a:      	jmp	0x2cfea8a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18da>
 2cfea6c:      	movq	%rdx, %rsi
 2cfea6f:      	nop
 2cfea70:      	leaq	(%rax,%rcx,4), %rax
 2cfea74:      	cmpq	%rax, %rsi
 2cfea77:      	je	0x2cfeb53 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19a3>
 2cfea7d:      	addq	$0x20, %r13
 2cfea81:      	cmpq	%r12, %r13
 2cfea84:      	je	0x2cfe810 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfea8a:      	movl	(%r13), %eax
 2cfea8e:      	movl	%eax, %ecx
 2cfea90:      	andl	$0x10000ff, %ecx        # imm = 0x10000FF
 2cfea96:      	cmpl	$0x1000000, %ecx        # imm = 0x1000000
 2cfea9c:      	setne	%cl
 2cfea9f:      	notl	%eax
 2cfeaa1:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfeaa6:      	sete	%al
 2cfeaa9:      	orb	%cl, %al
 2cfeaab:      	jne	0x2cfea7d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfeaad:      	movl	0x4(%r13), %ebp
 2cfeab1:      	movq	0x1c0(%rsp), %rax
 2cfeab9:      	movl	0x1c8(%rsp), %ecx
 2cfeac0:      	movl	%ecx, %edi
 2cfeac2:      	shrl	$0x2, %edi
 2cfeac5:      	je	0x2cfeb1c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x196c>
 2cfeac7:      	leaq	(,%rcx,4), %rdx
 2cfeacf:      	andq	$-0x10, %rdx
 2cfead3:      	addq	%rax, %rdx
 2cfead6:      	incq	%rdi
 2cfead9:      	leaq	0x8(%rax), %rsi
 2cfeadd:      	nopl	(%rax)
 2cfeae0:      	cmpl	%ebp, -0x8(%rsi)
 2cfeae3:      	je	0x2cfeb93 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19e3>
 2cfeae9:      	cmpl	%ebp, -0x4(%rsi)
 2cfeaec:      	je	0x2cfeb9c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19ec>
 2cfeaf2:      	cmpl	%ebp, (%rsi)
 2cfeaf4:      	je	0x2cfea70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfeafa:      	cmpl	%ebp, 0x4(%rsi)
 2cfeafd:      	je	0x2cfeba5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19f5>
 2cfeb03:      	decq	%rdi
 2cfeb06:      	addq	$0x10, %rsi
 2cfeb0a:      	cmpq	$0x1, %rdi
 2cfeb0e:      	jg	0x2cfeae0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1930>
 2cfeb10:      	movl	%ecx, %esi
 2cfeb12:      	andl	$0x3, %esi
 2cfeb15:      	cmpl	$0x1, %esi
 2cfeb18:      	jne	0x2cfeb26 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1976>
 2cfeb1a:      	jmp	0x2cfeb48 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1998>
 2cfeb1c:      	movl	%ecx, %esi
 2cfeb1e:      	movq	%rax, %rdx
 2cfeb21:      	cmpl	$0x1, %esi
 2cfeb24:      	je	0x2cfeb48 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1998>
 2cfeb26:      	cmpl	$0x2, %esi
 2cfeb29:      	je	0x2cfeb3c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x198c>
 2cfeb2b:      	cmpl	$0x3, %esi
 2cfeb2e:      	jne	0x2cfeb53 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19a3>
 2cfeb30:      	cmpl	%ebp, (%rdx)
 2cfeb32:      	je	0x2cfea6c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18bc>
 2cfeb38:      	addq	$0x4, %rdx
 2cfeb3c:      	cmpl	%ebp, (%rdx)
 2cfeb3e:      	je	0x2cfea6c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18bc>
 2cfeb44:      	addq	$0x4, %rdx
 2cfeb48:      	movq	%rdx, %rsi
 2cfeb4b:      	cmpl	%ebp, (%rdx)
 2cfeb4d:      	je	0x2cfea70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfeb53:      	movq	%rbx, %rdi
 2cfeb56:      	movl	%ebp, %esi
 2cfeb58:      	xorl	%edx, %edx
 2cfeb5a:      	xorl	%ecx, %ecx
 2cfeb5c:      	callq	0x36556b0 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2cfeb61:      	cmpl	$-0x1, %eax
 2cfeb64:      	jne	0x2cfea7d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfeb6a:      	movl	0x1c8(%rsp), %edx
 2cfeb71:      	cmpl	0x1cc(%rsp), %edx
 2cfeb78:      	jae	0x2cfebae <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19fe>
 2cfeb7a:      	movq	0x1c0(%rsp), %rax
 2cfeb82:      	movl	%edx, %ecx
 2cfeb84:      	movl	%ebp, (%rax,%rcx,4)
 2cfeb87:      	incl	0x1c8(%rsp)
 2cfeb8e:      	jmp	0x2cfea7d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfeb93:      	addq	$-0x8, %rsi
 2cfeb97:      	jmp	0x2cfea70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfeb9c:      	addq	$-0x4, %rsi
 2cfeba0:      	jmp	0x2cfea70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfeba5:      	addq	$0x4, %rsi
 2cfeba9:      	jmp	0x2cfea70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfebae:      	incq	%rdx
 2cfebb1:      	movl	$0x4, %ecx
 2cfebb6:      	leaq	0x1c0(%rsp), %rdi
 2cfebbe:      	leaq	0x1d0(%rsp), %rsi
 2cfebc6:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfebcb:      	movl	0x1c8(%rsp), %edx
 2cfebd2:      	jmp	0x2cfeb7a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19ca>
 2cfebd4:      	incq	%rdx
 2cfebd7:      	movl	$0x8, %ecx
 2cfebdc:      	leaq	0x130(%rsp), %rdi
 2cfebe4:      	leaq	0x140(%rsp), %rsi
 2cfebec:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfebf1:      	movl	0x138(%rsp), %edx
 2cfebf8:      	jmp	0x2cfe910 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1760>
 2cfebfd:      	testq	%r9, %r9
 2cfec00:      	cmovneq	%r9, %rax
 2cfec04:      	jmp	0x2cfe9a2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17f2>
 2cfec09:      	testq	%r9, %r9
 2cfec0c:      	cmovneq	%r9, %rax
 2cfec10:      	jmp	0x2cfe8b2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1702>
 2cfec15:      	addl	%esi, %esi
 2cfec17:      	leaq	0x1e0(%rsp), %rdi
 2cfec1f:      	callq	0x2cbbc10 <_ZN4llvm12DenseMapBaseINS_8DenseMapIjNS_6detail13DenseSetEmptyENS_12DenseMapInfoIjvEENS2_12DenseSetPairIjEEEEjS3_S5_S7_E4growEj>
 2cfec24:      	movl	0x1f0(%rsp), %ecx
 2cfec2b:      	testl	%ecx, %ecx
 2cfec2d:      	je	0x2cfec86 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad6>
 2cfec2f:      	movq	0x1e0(%rsp), %rdx
 2cfec37:      	leal	(%rbp,%rbp,8), %eax
 2cfec3b:      	leal	(%rbp,%rax,4), %esi
 2cfec3f:      	decl	%ecx
 2cfec41:      	andl	%ecx, %esi
 2cfec43:      	leaq	(%rdx,%rsi,4), %rax
 2cfec47:      	movl	(%rdx,%rsi,4), %r9d
 2cfec4b:      	cmpl	%r9d, %ebp
 2cfec4e:      	je	0x2cfec88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfec50:      	movl	$0x1, %edi
 2cfec55:      	xorl	%r8d, %r8d
 2cfec58:      	cmpl	$-0x1, %r9d
 2cfec5c:      	je	0x2cfed33 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b83>
 2cfec62:      	testq	%r8, %r8
 2cfec65:      	cmovneq	%r8, %rax
 2cfec69:      	cmpl	$-0x2, %r9d
 2cfec6d:      	cmoveq	%rax, %r8
 2cfec71:      	addl	%edi, %esi
 2cfec73:      	incl	%edi
 2cfec75:      	andl	%ecx, %esi
 2cfec77:      	leaq	(%rdx,%rsi,4), %rax
 2cfec7b:      	movl	(%rdx,%rsi,4), %r9d
 2cfec7f:      	cmpl	%r9d, %ebp
 2cfec82:      	je	0x2cfec88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfec84:      	jmp	0x2cfec58 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1aa8>
 2cfec86:      	xorl	%eax, %eax
 2cfec88:      	movl	0x1e8(%rsp), %ecx
 2cfec8f:      	incl	%ecx
 2cfec91:      	movl	%ecx, 0x1e8(%rsp)
 2cfec98:      	cmpl	$-0x1, (%rax)
 2cfec9b:      	jne	0x2cfe9e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1833>
 2cfeca1:      	jmp	0x2cfe9ea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183a>
 2cfeca6:      	addl	%esi, %esi
 2cfeca8:      	leaq	0x200(%rsp), %rdi
 2cfecb0:      	callq	0x2cbbc10 <_ZN4llvm12DenseMapBaseINS_8DenseMapIjNS_6detail13DenseSetEmptyENS_12DenseMapInfoIjvEENS2_12DenseSetPairIjEEEEjS3_S5_S7_E4growEj>
 2cfecb5:      	movl	0x210(%rsp), %ecx
 2cfecbc:      	testl	%ecx, %ecx
 2cfecbe:      	je	0x2cfed13 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b63>
 2cfecc0:      	movq	0x200(%rsp), %rdx
 2cfecc8:      	leal	(%rbp,%rbp,8), %eax
 2cfeccc:      	leal	(%rbp,%rax,4), %esi
 2cfecd0:      	decl	%ecx
 2cfecd2:      	andl	%ecx, %esi
 2cfecd4:      	leaq	(%rdx,%rsi,4), %rax
 2cfecd8:      	movl	(%rdx,%rsi,4), %r9d
 2cfecdc:      	cmpl	%r9d, %ebp
 2cfecdf:      	je	0x2cfed15 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfece1:      	movl	$0x1, %edi
 2cfece6:      	xorl	%r8d, %r8d
 2cfece9:      	cmpl	$-0x1, %r9d
 2cfeced:      	je	0x2cfed3f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b8f>
 2cfecef:      	testq	%r8, %r8
 2cfecf2:      	cmovneq	%r8, %rax
 2cfecf6:      	cmpl	$-0x2, %r9d
 2cfecfa:      	cmoveq	%rax, %r8
 2cfecfe:      	addl	%edi, %esi
 2cfed00:      	incl	%edi
 2cfed02:      	andl	%ecx, %esi
 2cfed04:      	leaq	(%rdx,%rsi,4), %rax
 2cfed08:      	movl	(%rdx,%rsi,4), %r9d
 2cfed0c:      	cmpl	%r9d, %ebp
 2cfed0f:      	je	0x2cfed15 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfed11:      	jmp	0x2cfece9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b39>
 2cfed13:      	xorl	%eax, %eax
 2cfed15:      	movl	0x208(%rsp), %ecx
 2cfed1c:      	incl	%ecx
 2cfed1e:      	movl	%ecx, 0x208(%rsp)
 2cfed25:      	cmpl	$-0x1, (%rax)
 2cfed28:      	jne	0x2cfe8f3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1743>
 2cfed2e:      	jmp	0x2cfe8fa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174a>
 2cfed33:      	testq	%r8, %r8
 2cfed36:      	cmovneq	%r8, %rax
 2cfed3a:      	jmp	0x2cfec88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfed3f:      	testq	%r8, %r8
 2cfed42:      	cmovneq	%r8, %rax
 2cfed46:      	jmp	0x2cfed15 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfed48:      	nopl	(%rax,%rax)
 2cfed50:      	movq	0x90(%rsp), %rax
 2cfed58:      	movq	(%rax), %r14
 2cfed5b:      	movq	0x78(%rsp), %rbx
 2cfed60:      	movq	0x10(%rsp), %rbp
 2cfed65:      	jmp	0x2cfed78 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bc8>
 2cfed67:      	nopw	(%rax,%rax)
 2cfed70:      	movq	0x90(%rsp), %rax
 2cfed78:      	movl	0x30(%rax), %eax
 2cfed7b:      	movq	(%r14,%rax,8), %r14
 2cfed7f:      	testb	$0x4, (%r14)
 2cfed83:      	movq	%r14, %rax
 2cfed86:      	jne	0x2cfedaa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bfa>
 2cfed88:      	testb	$0x8, 0x2c(%r14)
 2cfed8d:      	movq	%r14, %rax
 2cfed90:      	je	0x2cfedaa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bfa>
 2cfed92:      	movq	%r14, %rax
 2cfed95:      	nopw	%cs:(%rax,%rax)
 2cfed9f:      	nop
 2cfeda0:      	movq	0x8(%rax), %rax
 2cfeda4:      	testb	$0x8, 0x2c(%rax)
 2cfeda8:      	jne	0x2cfeda0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bf0>
 2cfedaa:      	movq	0x8(%rax), %rax
 2cfedae:      	movq	%rax, 0x20(%rsp)
 2cfedb3:      	movq	0x18(%r14), %rax
 2cfedb7:      	movq	%rax, 0x10(%rsp)
 2cfedbc:      	movq	%rbp, %rdi
 2cfedbf:      	callq	0x2cf7a30 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfedc4:      	movl	%eax, 0x18(%rsp)
 2cfedc8:      	movq	0x20(%rbp), %rax
 2cfedcc:      	movl	0x24(%rax), %r12d
 2cfedd0:      	xorl	%r15d, %r15d
 2cfedd3:      	movq	%r14, %rdi
 2cfedd6:      	movl	%r12d, %esi
 2cfedd9:      	xorl	%edx, %edx
 2cfeddb:      	movl	$0x1, %ecx
 2cfede0:      	callq	0x36556b0 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2cfede5:      	movq	%rbp, %rsi
 2cfede8:      	movl	%eax, 0x70(%rsp)
 2cfedec:      	cmpl	$-0x1, %eax
 2cfedef:      	setne	%r13b
 2cfedf3:      	movq	0x10(%rbp), %rcx
 2cfedf7:      	movl	$0xe, %r14d
 2cfedfd:      	testb	$0x40, 0x12(%rcx)
 2cfee01:      	je	0x2cfee60 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb0>
 2cfee03:      	movzwl	0x28(%rsi), %edx
 2cfee07:      	movzbl	0x2a(%rsi), %eax
 2cfee0b:      	shll	$0x10, %eax
 2cfee0e:      	orl	%edx, %eax
 2cfee10:      	testl	%eax, %eax
 2cfee12:      	je	0x2cfee60 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb0>
 2cfee14:      	movzwl	(%rcx), %edx
 2cfee17:      	movzwl	0xa(%rcx), %esi
 2cfee1b:      	shll	$0x5, %eax
 2cfee1e:      	shll	$0x5, %edx
 2cfee21:      	leaq	(%rsi,%rsi,2), %rsi
 2cfee25:      	leaq	(%rdx,%rsi,2), %rdx
 2cfee29:      	movq	%rbp, %rsi
 2cfee2c:      	leaq	0x22(%rcx,%rdx), %rdx
 2cfee31:      	xorl	%ecx, %ecx
 2cfee33:      	nopw	%cs:(%rax,%rax)
 2cfee3d:      	nopl	(%rax)
 2cfee40:      	testb	$0x2, (%rdx)
 2cfee43:      	jne	0x2cfefec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e3c>
 2cfee49:      	addq	$0x20, %rcx
 2cfee4d:      	addq	$0x6, %rdx
 2cfee51:      	cmpq	%rcx, %rax
 2cfee54:      	jne	0x2cfee40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1c90>
 2cfee56:      	nopw	%cs:(%rax,%rax)
 2cfee60:      	movq	0x38(%rsi), %rsi
 2cfee64:      	movq	%rsi, 0xc8(%rsp)
 2cfee6c:      	testq	%rsi, %rsi
 2cfee6f:      	je	0x2cfee83 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cd3>
 2cfee71:      	movl	$0x1, %edx
 2cfee76:      	leaq	0xc8(%rsp), %rdi
 2cfee7e:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfee83:      	movq	0x90(%rsp), %rax
 2cfee8b:      	cmpb	$0x0, 0x3d(%rax)
 2cfee8f:      	je	0x2cfef10 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1d60>
 2cfee91:      	movq	%r12, 0x8(%rsp)
 2cfee96:      	movq	%r15, 0x88(%rsp)
 2cfee9e:      	movq	$-0x102f, %rbp          # imm = 0xEFD1
 2cfeea5:      	movb	$0x1, %r12b
 2cfeea8:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cfeeae:      	movl	%r14d, 0x28(%rsp)
 2cfeeb3:      	je	0x2cff014 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e64>
 2cfeeb9:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cfeebf:      	leaq	0x30(%rsp), %rdx
 2cfeec4:      	je	0x2cff019 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfeeca:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cfeed0:      	je	0x2cff019 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfeed6:      	movl	%ebx, %eax
 2cfeed8:      	andl	$-0x2, %eax
 2cfeedb:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cfeee0:      	sete	%r12b
 2cfeee4:      	movq	$-0x1101, %rbp          # imm = 0xEEFF
 2cfeeeb:      	movq	$-0x102f, %rax          # imm = 0xEFD1
 2cfeef2:      	cmoveq	%rax, %rbp
 2cfeef6:      	movq	0x90(%rsp), %rax
 2cfeefe:      	jmp	0x2cff019 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfef03:      	nopw	%cs:(%rax,%rax)
 2cfef0d:      	nopl	(%rax)
 2cfef10:      	cmpb	$0x1, 0x3c(%rax)
 2cfef14:      	jne	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfef1a:      	movq	%r12, 0x8(%rsp)
 2cfef1f:      	movq	%r15, 0x88(%rsp)
 2cfef27:      	movl	%r14d, 0x28(%rsp)
 2cfef2c:      	movq	0x130(%rsp), %r14
 2cfef34:      	movl	0x138(%rsp), %r9d
 2cfef3c:      	movq	(%rax), %rcx
 2cfef3f:      	movq	%rcx, 0x230(%rsp)
 2cfef47:      	movl	0x8(%rax), %eax
 2cfef4a:      	movq	%rax, 0x228(%rsp)
 2cfef52:      	xorl	%eax, %eax
 2cfef54:      	movq	(%rsp), %rcx
 2cfef58:      	cmpb	$0x1, 0x202(%rcx)
 2cfef5f:      	movl	$0x0, %r15d
 2cfef65:      	movl	$0x0, %ecx
 2cfef6a:      	jne	0x2cffafc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cfef70:      	movq	%r9, %r12
 2cfef73:      	movq	(%rsp), %rbx
 2cfef77:      	movq	0x48(%rbx), %rsi
 2cfef7b:      	movq	0x10(%rsp), %rdi
 2cfef80:      	movl	$0x3, %edx
 2cfef85:      	movq	0x20(%rsp), %rcx
 2cfef8a:      	movl	$0x14, %r8d
 2cfef90:      	callq	0x35d98e0 <_ZNK4llvm17MachineBasicBlock23computeRegisterLivenessEPKNS_18TargetRegisterInfoENS_10MCRegisterENS_26MachineInstrBundleIteratorIKNS_12MachineInstrELb0EEEj>
 2cfef95:      	cmpl	$0x1, %eax
 2cfef98:      	setne	%r15b
 2cfef9c:      	xorl	%ecx, %ecx
 2cfef9e:      	xorl	%eax, %eax
 2cfefa0:      	cmpb	$0x1, 0x202(%rbx)
 2cfefa7:      	jne	0x2cffaf9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2949>
 2cfefad:      	movq	%r12, %r9
 2cfefb0:      	testq	%r12, %r12
 2cfefb3:      	je	0x2cfefe3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e33>
 2cfefb5:      	leaq	(,%r9,8), %rax
 2cfefbd:      	xorl	%ecx, %ecx
 2cfefbf:      	movq	0x78(%rsp), %rbx
 2cfefc4:      	movq	0x8(%rsp), %r12
 2cfefc9:      	movl	0x18(%rsp), %r8d
 2cfefce:      	nop
 2cfefd0:      	cmpl	%r12d, (%r14,%rcx)
 2cfefd4:      	je	0x2cffd83 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bd3>
 2cfefda:      	addq	$0x8, %rcx
 2cfefde:      	cmpq	%rcx, %rax
 2cfefe1:      	jne	0x2cfefd0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e20>
 2cfefe3:      	movb	$0x1, %al
 2cfefe5:      	movb	$0x1, %cl
 2cfefe7:      	jmp	0x2cffafc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cfefec:      	movq	0x20(%rsi), %rax
 2cfeff0:      	movl	0x10(%rax,%rcx), %r14d
 2cfeff5:      	movl	0x24(%rax,%rcx), %r15d
 2cfeffa:      	movq	0x38(%rsi), %rsi
 2cfeffe:      	movq	%rsi, 0xc8(%rsp)
 2cff006:      	testq	%rsi, %rsi
 2cff009:      	jne	0x2cfee71 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cc1>
 2cff00f:      	jmp	0x2cfee83 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cd3>
 2cff014:      	leaq	0x30(%rsp), %rdx
 2cff019:      	movq	0x130(%rsp), %rbx
 2cff021:      	movq	(%rax), %rcx
 2cff024:      	movq	%rcx, 0xc0(%rsp)
 2cff02c:      	movl	0x8(%rax), %r15d
 2cff030:      	movq	0xc8(%rsp), %rsi
 2cff038:      	movq	%rsi, 0xa0(%rsp)
 2cff040:      	movq	%rdx, %r13
 2cff043:      	testq	%rsi, %rsi
 2cff046:      	je	0x2cff086 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ed6>
 2cff048:      	movl	$0x1, %edx
 2cff04d:      	leaq	0xa0(%rsp), %rdi
 2cff055:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cff05a:      	leaq	0x30(%rsp), %rdx
 2cff05f:      	movq	0xa0(%rsp), %rsi
 2cff067:      	movq	%rsi, 0x30(%rsp)
 2cff06c:      	testq	%rsi, %rsi
 2cff06f:      	je	0x2cff08e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ede>
 2cff071:      	leaq	0xa0(%rsp), %r13
 2cff079:      	movq	%r13, %rdi
 2cff07c:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cff081:      	leaq	0x30(%rsp), %rdx
 2cff086:      	movq	$0x0, (%r13)
 2cff08e:      	leaq	0x40(%rsp), %rax
 2cff093:      	xorps	%xmm0, %xmm0
 2cff096:      	movups	%xmm0, -0x8(%rax)
 2cff09a:      	movq	$0x0, 0x8(%rax)
 2cff0a2:      	movq	(%rsp), %rax
 2cff0a6:      	movq	0x40(%rax), %rax
 2cff0aa:      	shlq	$0x5, %rbp
 2cff0ae:      	addq	0x8(%rax), %rbp
 2cff0b2:      	movq	0x10(%rsp), %rdi
 2cff0b7:      	movq	0x20(%rsp), %rsi
 2cff0bc:      	movq	%rdx, %r13
 2cff0bf:      	movq	%rbp, %rcx
 2cff0c2:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cff0c7:      	movq	%rax, %rbp
 2cff0ca:      	movq	%rdx, %r14
 2cff0cd:      	movq	0x30(%rsp), %rsi
 2cff0d2:      	testq	%rsi, %rsi
 2cff0d5:      	je	0x2cff0df <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1f2f>
 2cff0d7:      	movq	%r13, %rdi
 2cff0da:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff0df:      	movq	0xa0(%rsp), %rsi
 2cff0e7:      	testq	%rsi, %rsi
 2cff0ea:      	je	0x2cff0f9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1f49>
 2cff0ec:      	leaq	0xa0(%rsp), %rdi
 2cff0f4:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff0f9:      	movl	(%rbx), %eax
 2cff0fb:      	testb	%r12b, %r12b
 2cff0fe:      	je	0x2cff157 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1fa7>
 2cff100:      	movq	$0x0, 0x38(%rsp)
 2cff109:      	movl	%eax, 0x34(%rsp)
 2cff10d:      	leaq	0x40(%rsp), %r12
 2cff112:      	xorps	%xmm0, %xmm0
 2cff115:      	movups	%xmm0, (%r12)
 2cff11a:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2cff122:      	movq	%r14, %rdi
 2cff125:      	movq	%rbp, %rsi
 2cff128:      	leaq	0x30(%rsp), %r13
 2cff12d:      	movq	%r13, %rdx
 2cff130:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff135:      	movl	0x8(%rbx), %eax
 2cff138:      	movq	$0x0, 0x38(%rsp)
 2cff141:      	movl	%eax, 0x34(%rsp)
 2cff145:      	xorps	%xmm0, %xmm0
 2cff148:      	movups	%xmm0, (%r12)
 2cff14d:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2cff155:      	jmp	0x2cff1b2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2002>
 2cff157:      	movzbl	0x4(%rbx), %ecx
 2cff15b:      	movq	$0x0, 0x38(%rsp)
 2cff164:      	shll	$0x1a, %ecx
 2cff167:      	movl	%eax, 0x34(%rsp)
 2cff16b:      	leaq	0x40(%rsp), %r12
 2cff170:      	xorps	%xmm0, %xmm0
 2cff173:      	movups	%xmm0, (%r12)
 2cff178:      	movl	%ecx, 0x30(%rsp)
 2cff17c:      	movq	%r14, %rdi
 2cff17f:      	movq	%rbp, %rsi
 2cff182:      	leaq	0x30(%rsp), %r13
 2cff187:      	movq	%r13, %rdx
 2cff18a:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff18f:      	movl	0x8(%rbx), %eax
 2cff192:      	movzbl	0xc(%rbx), %ecx
 2cff196:      	movq	$0x0, 0x38(%rsp)
 2cff19f:      	shll	$0x1a, %ecx
 2cff1a2:      	movl	%eax, 0x34(%rsp)
 2cff1a6:      	xorps	%xmm0, %xmm0
 2cff1a9:      	movups	%xmm0, (%r12)
 2cff1ae:      	movl	%ecx, 0x30(%rsp)
 2cff1b2:      	movq	%r14, %rdi
 2cff1b5:      	movq	%rbp, %rsi
 2cff1b8:      	movq	%r13, %rdx
 2cff1bb:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff1c0:      	movq	$0x0, 0x38(%rsp)
 2cff1c9:      	movq	0x8(%rsp), %rax
 2cff1ce:      	movl	%eax, 0x34(%rsp)
 2cff1d2:      	xorps	%xmm0, %xmm0
 2cff1d5:      	movups	%xmm0, (%r12)
 2cff1da:      	movl	$0x0, 0x30(%rsp)
 2cff1e2:      	movq	%r14, %rdi
 2cff1e5:      	movq	%rbp, %rsi
 2cff1e8:      	movq	%r13, %rdx
 2cff1eb:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff1f0:      	movslq	0x18(%rsp), %rax
 2cff1f5:      	movl	$0x1, 0x30(%rsp)
 2cff1fd:      	movq	$0x0, 0x38(%rsp)
 2cff206:      	movq	%rax, 0x40(%rsp)
 2cff20b:      	movq	%r14, %rdi
 2cff20e:      	movq	%rbp, %rsi
 2cff211:      	movq	%r13, %rdx
 2cff214:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff219:      	movl	0x28(%rsp), %eax
 2cff21d:      	movl	$0x1, 0x30(%rsp)
 2cff225:      	movq	$0x0, 0x38(%rsp)
 2cff22e:      	movq	%rax, 0x40(%rsp)
 2cff233:      	movq	%r14, %rdi
 2cff236:      	movq	%rbp, %rsi
 2cff239:      	movq	%r13, %rdx
 2cff23c:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff241:      	movq	$0x0, 0x38(%rsp)
 2cff24a:      	movq	0x88(%rsp), %rax
 2cff252:      	movl	%eax, 0x34(%rsp)
 2cff256:      	xorps	%xmm0, %xmm0
 2cff259:      	movups	%xmm0, (%r12)
 2cff25e:      	movl	$0x0, 0x30(%rsp)
 2cff266:      	movq	%r14, %rdi
 2cff269:      	movq	%rbp, %rsi
 2cff26c:      	movq	%r13, %rdx
 2cff26f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff274:      	movq	%r14, %rdi
 2cff277:      	movq	%rbp, %rsi
 2cff27a:      	movq	0xc0(%rsp), %rdx
 2cff282:      	movq	%r15, %rcx
 2cff285:      	callq	0x3651fe0 <_ZN4llvm12MachineInstr18cloneMergedMemRefsERNS_15MachineFunctionENS_8ArrayRefIPKS0_EE>
 2cff28a:      	movq	0x90(%rsp), %rcx
 2cff292:      	movl	0x34(%rcx), %eax
 2cff295:      	movq	(%rcx), %rdx
 2cff298:      	movq	(%rdx,%rax,8), %rcx
 2cff29c:      	movq	0x10(%rsp), %rax
 2cff2a1:      	movq	0x38(%rax), %rsi
 2cff2a5:      	movq	%rcx, %rax
 2cff2a8:      	movq	%rsi, 0xc0(%rsp)
 2cff2b0:      	cmpq	%rsi, %rcx
 2cff2b3:      	xorps	%xmm0, %xmm0
 2cff2b6:      	je	0x2cff2e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff2b8:      	movq	(%rcx), %rax
 2cff2bb:      	andq	$-0x8, %rax
 2cff2bf:      	testb	$0x4, (%rax)
 2cff2c2:      	jne	0x2cff2e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff2c4:      	nopw	%cs:(%rax,%rax)
 2cff2ce:      	nop
 2cff2d0:      	testb	$0x4, 0x2c(%rax)
 2cff2d4:      	je	0x2cff2e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff2d6:      	movq	(%rax), %rax
 2cff2d9:      	andq	$-0x8, %rax
 2cff2dd:      	testb	$0x4, 0x2c(%rax)
 2cff2e1:      	jne	0x2cff2d6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2126>
 2cff2e3:      	movq	%rcx, 0x88(%rsp)
 2cff2eb:      	movq	%rax, 0x70(%rsp)
 2cff2f0:      	movq	%r14, 0x28(%rsp)
 2cff2f5:      	movq	0x90(%rsp), %rax
 2cff2fd:      	movl	0x8(%rax), %eax
 2cff300:      	testq	%rax, %rax
 2cff303:      	je	0x2cff560 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23b0>
 2cff309:      	leaq	(%rdx,%rax,8), %rax
 2cff30d:      	movq	%rax, 0x8(%rsp)
 2cff312:      	jmp	0x2cff334 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2184>
 2cff314:      	nopw	%cs:(%rax,%rax)
 2cff31e:      	nop
 2cff320:      	movq	0x20(%rsp), %rdx
 2cff325:      	addq	$0x8, %rdx
 2cff329:      	cmpq	0x8(%rsp), %rdx
 2cff32e:      	je	0x2cff560 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23b0>
 2cff334:      	movq	%rdx, 0x20(%rsp)
 2cff339:      	movq	(%rdx), %r14
 2cff33c:      	testb	$0x4, (%r14)
 2cff340:      	movq	%r14, %rax
 2cff343:      	jne	0x2cff36a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21ba>
 2cff345:      	testb	$0x8, 0x2c(%r14)
 2cff34a:      	movq	%r14, %rax
 2cff34d:      	je	0x2cff36a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21ba>
 2cff34f:      	movq	%r14, %rax
 2cff352:      	nopw	%cs:(%rax,%rax)
 2cff35c:      	nopl	(%rax)
 2cff360:      	movq	0x8(%rax), %rax
 2cff364:      	testb	$0x8, 0x2c(%rax)
 2cff368:      	jne	0x2cff360 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21b0>
 2cff36a:      	movq	0x8(%rax), %rax
 2cff36e:      	movq	%rax, 0x18(%rsp)
 2cff373:      	cmpq	%rax, %r14
 2cff376:      	jne	0x2cff3b7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2207>
 2cff378:      	jmp	0x2cff320 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2170>
 2cff37a:      	nopw	(%rax,%rax)
 2cff380:      	movl	%ecx, 0xf0(%r12)
 2cff388:      	movq	(%r15), %rax
 2cff38b:      	movq	(%rax,%rbp,8), %rcx
 2cff38f:      	movq	%rcx, (%rbx)
 2cff392:      	movq	%rbx, (%rax,%rbp,8)
 2cff396:      	movq	0xe0(%r12), %rax
 2cff39e:      	movq	%rax, (%r14)
 2cff3a1:      	movq	%r14, 0xe0(%r12)
 2cff3a9:      	movq	%r13, %r14
 2cff3ac:      	cmpq	0x18(%rsp), %r13
 2cff3b1:      	je	0x2cff320 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2170>
 2cff3b7:      	movq	0x8(%r14), %r13
 2cff3bb:      	movq	0x18(%r14), %rax
 2cff3bf:      	movq	0x20(%rax), %rbx
 2cff3c3:      	testq	%rbx, %rbx
 2cff3c6:      	je	0x2cff480 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff3cc:      	movq	0x288(%rbx), %rdi
 2cff3d3:      	testq	%rdi, %rdi
 2cff3d6:      	je	0x2cff3e4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2234>
 2cff3d8:      	movq	(%rdi), %rax
 2cff3db:      	movq	%r14, %rsi
 2cff3de:      	callq	*0x20(%rax)
 2cff3e1:      	xorps	%xmm0, %xmm0
 2cff3e4:      	movzwl	0x28(%r14), %ecx
 2cff3e9:      	movzbl	0x2a(%r14), %eax
 2cff3ee:      	shll	$0x10, %eax
 2cff3f1:      	orl	%ecx, %eax
 2cff3f3:      	testl	%eax, %eax
 2cff3f5:      	je	0x2cff480 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff3fb:      	movq	0x20(%r14), %rcx
 2cff3ff:      	shll	$0x5, %eax
 2cff402:      	movq	0x20(%rbx), %rdx
 2cff406:      	jmp	0x2cff431 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2281>
 2cff408:      	nopl	(%rax,%rax)
 2cff410:      	movq	%rdi, 0x18(%r8)
 2cff414:      	leaq	0x10(%rcx), %r9
 2cff418:      	testq	%rdi, %rdi
 2cff41b:      	cmovneq	%rdi, %rsi
 2cff41f:      	movq	%r8, 0x10(%rsi)
 2cff423:      	movups	%xmm0, (%r9)
 2cff427:      	addq	$0x20, %rcx
 2cff42b:      	addq	$-0x20, %rax
 2cff42f:      	je	0x2cff480 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff431:      	cmpb	$0x0, (%rcx)
 2cff434:      	jne	0x2cff427 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2277>
 2cff436:      	movl	0x4(%rcx), %esi
 2cff439:      	movl	%esi, %edi
 2cff43b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2cff441:      	shlq	$0x4, %rdi
 2cff445:      	movq	%rsi, %r8
 2cff448:      	shlq	$0x3, %r8
 2cff44c:      	addq	0x128(%rdx), %r8
 2cff453:      	testl	%esi, %esi
 2cff455:      	movq	0x30(%rdx), %rsi
 2cff459:      	leaq	0x8(%rsi,%rdi), %r9
 2cff45e:      	cmovnsq	%r8, %r9
 2cff462:      	movq	(%r9), %rsi
 2cff465:      	movq	0x18(%rcx), %rdi
 2cff469:      	movq	0x10(%rcx), %r8
 2cff46d:      	cmpq	%rsi, %rcx
 2cff470:      	jne	0x2cff410 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2260>
 2cff472:      	movq	%rdi, (%r9)
 2cff475:      	jmp	0x2cff414 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2264>
 2cff477:      	nopw	(%rax,%rax)
 2cff480:      	movq	$0x0, 0x18(%r14)
 2cff488:      	movq	(%r14), %rax
 2cff48b:      	movq	0x8(%r14), %rcx
 2cff48f:      	andq	$-0x8, %rax
 2cff493:      	movq	(%rcx), %rdx
 2cff496:      	andl	$0x7, %edx
 2cff499:      	orq	%rax, %rdx
 2cff49c:      	movq	%rdx, (%rcx)
 2cff49f:      	movq	%rcx, 0x8(%rax)
 2cff4a3:      	andq	$0x7, (%r14)
 2cff4a7:      	movq	$0x0, 0x8(%r14)
 2cff4af:      	movq	0x10(%rsp), %rax
 2cff4b4:      	movq	0x28(%rax), %rax
 2cff4b8:      	movq	0x20(%rax), %r12
 2cff4bc:      	movq	0x20(%r14), %rbx
 2cff4c0:      	testq	%rbx, %rbx
 2cff4c3:      	je	0x2cff396 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21e6>
 2cff4c9:      	movzbl	0x2b(%r14), %ebp
 2cff4ce:      	leaq	0xe8(%r12), %r15
 2cff4d6:      	movl	0xf0(%r12), %eax
 2cff4de:      	cmpl	%ebp, %eax
 2cff4e0:      	ja	0x2cff388 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d8>
 2cff4e6:      	leaq	0x1(%rbp), %rcx
 2cff4ea:      	cmpl	%ebp, 0xf4(%r12)
 2cff4f2:      	ja	0x2cff51c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x236c>
 2cff4f4:      	leaq	0xf8(%r12), %rsi
 2cff4fc:      	movl	$0x8, %ecx
 2cff501:      	movq	%r15, %rdi
 2cff504:      	leaq	0x1(%rbp), %rdx
 2cff508:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cff50d:      	leaq	0x1(%rbp), %rcx
 2cff511:      	xorps	%xmm0, %xmm0
 2cff514:      	movl	0xf0(%r12), %eax
 2cff51c:      	cmpl	%eax, %ecx
 2cff51e:      	je	0x2cff380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d0>
 2cff524:      	movl	%eax, %eax
 2cff526:      	leaq	(,%rax,8), %rdi
 2cff52e:      	addq	(%r15), %rdi
 2cff531:      	movq	%rcx, %r15
 2cff534:      	movq	%rcx, %rdx
 2cff537:      	subq	%rax, %rdx
 2cff53a:      	shlq	$0x3, %rdx
 2cff53e:      	xorl	%esi, %esi
 2cff540:      	callq	0x828ab90 <memset@plt>
 2cff545:      	movq	%r15, %rcx
 2cff548:      	leaq	0xe8(%r12), %r15
 2cff550:      	xorps	%xmm0, %xmm0
 2cff553:      	jmp	0x2cff380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d0>
 2cff558:      	nopl	(%rax,%rax)
 2cff560:      	movq	0xc0(%rsp), %rax
 2cff568:      	cmpq	%rax, 0x88(%rsp)
 2cff570:      	je	0x2cff58e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23de>
 2cff572:      	movq	0x70(%rsp), %rax
 2cff577:      	testb	$0x4, (%rax)
 2cff57a:      	movl	$0x20000ff, %ebx        # imm = 0x20000FF
 2cff57f:      	jne	0x2cff587 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23d7>
 2cff581:      	testb	$0x8, 0x2c(%rax)
 2cff585:      	jne	0x2cff5ce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x241e>
 2cff587:      	movq	0x28(%rsp), %r13
 2cff58c:      	jmp	0x2cff5ea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x243a>
 2cff58e:      	movq	0x10(%rsp), %rax
 2cff593:      	addq	$0x38, %rax
 2cff597:      	movl	$0x20000ff, %ebx        # imm = 0x20000FF
 2cff59c:      	movq	0x28(%rsp), %r13
 2cff5a1:      	movq	(%rax), %rax
 2cff5a4:      	movq	0x78(%rsp), %rdx
 2cff5a9:      	cmpl	$0x104b, %edx           # imm = 0x104B
 2cff5af:      	jg	0x2cff5fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x244e>
 2cff5b1:      	cmpl	$0x3d7, %edx            # imm = 0x3D7
 2cff5b7:      	je	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff5b9:      	cmpl	$0xb51, %edx            # imm = 0xB51
 2cff5bf:      	je	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff5c1:      	cmpl	$0xb53, %edx            # imm = 0xB53
 2cff5c7:      	je	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff5c9:      	jmp	0x2cff774 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c4>
 2cff5ce:      	movq	0x28(%rsp), %r13
 2cff5d3:      	nopw	%cs:(%rax,%rax)
 2cff5dd:      	nopl	(%rax)
 2cff5e0:      	movq	0x8(%rax), %rax
 2cff5e4:      	testb	$0x8, 0x2c(%rax)
 2cff5e8:      	jne	0x2cff5e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2430>
 2cff5ea:      	addq	$0x8, %rax
 2cff5ee:      	movq	(%rax), %rax
 2cff5f1:      	movq	0x78(%rsp), %rdx
 2cff5f6:      	cmpl	$0x104b, %edx           # imm = 0x104B
 2cff5fc:      	jle	0x2cff5b1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2401>
 2cff5fe:      	leal	-0x104c(%rdx), %ecx
 2cff604:      	cmpl	$0x2, %ecx
 2cff607:      	jb	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff609:      	cmpl	$0x117a, %edx           # imm = 0x117A
 2cff60f:      	je	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff611:      	cmpl	$0x117d, %edx           # imm = 0x117D
 2cff617:      	je	0x2cff624 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff619:      	jmp	0x2cff774 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c4>
 2cff61e:      	nop
 2cff620:      	movq	0x8(%rax), %rax
 2cff624:      	cmpq	%r13, %rax
 2cff627:      	je	0x2cff8c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2710>
 2cff62d:      	movl	0x1c8(%rsp), %edx
 2cff634:      	testq	%rdx, %rdx
 2cff637:      	je	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2590>
 2cff63d:      	movq	0x1c0(%rsp), %rcx
 2cff645:      	leaq	(%rcx,%rdx,4), %rdx
 2cff649:      	jmp	0x2cff65d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24ad>
 2cff64b:      	nopl	(%rax,%rax)
 2cff650:      	addq	$0x4, %rcx
 2cff654:      	cmpq	%rdx, %rcx
 2cff657:      	je	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2590>
 2cff65d:      	movq	0x10(%rax), %r9
 2cff661:      	movq	0x20(%rax), %rsi
 2cff665:      	movzwl	0x28(%rax), %r8d
 2cff66a:      	movzbl	0x2a(%rax), %edi
 2cff66e:      	shll	$0x10, %edi
 2cff671:      	orq	%r8, %rdi
 2cff674:      	movzwl	0x2(%r9), %r8d
 2cff679:      	testb	$0x2, 0x10(%r9)
 2cff67e:      	je	0x2cff6c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff680:      	movl	%r8d, %r9d
 2cff683:      	cmpq	%rdi, %r9
 2cff686:      	je	0x2cff6c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff688:      	movl	%edi, %r10d
 2cff68b:      	shll	$0x5, %r10d
 2cff68f:      	shll	$0x5, %r9d
 2cff693:      	nopw	%cs:(%rax,%rax)
 2cff69d:      	nopl	(%rax)
 2cff6a0:      	movl	(%rsi,%r9), %r11d
 2cff6a4:      	andl	%ebx, %r11d
 2cff6a7:      	cmpl	$0x2000000, %r11d       # imm = 0x2000000
 2cff6ae:      	je	0x2cff6c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff6b0:      	incl	%r8d
 2cff6b3:      	addq	$0x20, %r9
 2cff6b7:      	cmpq	%r9, %r10
 2cff6ba:      	jne	0x2cff6a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24f0>
 2cff6bc:      	nopl	(%rax)
 2cff6c0:      	movl	%r8d, %r8d
 2cff6c3:      	cmpq	%rdi, %r8
 2cff6c6:      	je	0x2cff650 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24a0>
 2cff6c8:      	shll	$0x5, %edi
 2cff6cb:      	shlq	$0x5, %r8
 2cff6cf:      	jmp	0x2cff6ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x253d>
 2cff6d1:      	orl	$0x10000000, %r9d       # imm = 0x10000000
 2cff6d8:      	movl	%r9d, (%rsi,%r8)
 2cff6dc:      	nopl	(%rax)
 2cff6e0:      	addq	$0x20, %r8
 2cff6e4:      	cmpq	%r8, %rdi
 2cff6e7:      	je	0x2cff650 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24a0>
 2cff6ed:      	movl	(%rsi,%r8), %r9d
 2cff6f1:      	testb	%r9b, %r9b
 2cff6f4:      	jne	0x2cff6e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff6f6:      	movl	0x4(%rsi,%r8), %r10d
 2cff6fb:      	cmpl	(%rcx), %r10d
 2cff6fe:      	jne	0x2cff6e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff700:      	testl	$0x30000000, %r9d       # imm = 0x30000000
 2cff707:      	setne	%r10b
 2cff70b:      	movl	%r9d, %r11d
 2cff70e:      	andl	$0x10fff00, %r11d       # imm = 0x10FFF00
 2cff715:      	cmpl	$0x1000000, %r11d       # imm = 0x1000000
 2cff71c:      	sete	%r11b
 2cff720:      	orb	%r10b, %r11b
 2cff723:      	je	0x2cff6d1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2521>
 2cff725:      	testl	$0x1000000, %r9d        # imm = 0x1000000
 2cff72c:      	je	0x2cff6e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff72e:      	movl	$0x0, (%rcx)
 2cff734:      	jmp	0x2cff6e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff736:      	nopw	%cs:(%rax,%rax)
 2cff740:      	testb	$0x4, (%rax)
 2cff743:      	jne	0x2cff620 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff749:      	nopl	(%rax)
 2cff750:      	testb	$0x8, 0x2c(%rax)
 2cff754:      	je	0x2cff620 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff75a:      	movq	0x8(%rax), %rax
 2cff75e:      	testb	$0x8, 0x2c(%rax)
 2cff762:      	jne	0x2cff75a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25aa>
 2cff764:      	jmp	0x2cff620 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff769:      	nopl	(%rax)
 2cff770:      	movq	0x8(%rax), %rax
 2cff774:      	cmpq	%r13, %rax
 2cff777:      	je	0x2cff93d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x278d>
 2cff77d:      	movq	0x10(%rax), %rdi
 2cff781:      	movq	0x20(%rax), %rsi
 2cff785:      	movzwl	0x28(%rax), %edx
 2cff789:      	movzbl	0x2a(%rax), %ecx
 2cff78d:      	shll	$0x10, %ecx
 2cff790:      	orq	%rdx, %rcx
 2cff793:      	movzbl	0x4(%rdi), %edx
 2cff797:      	testb	$0x2, 0x10(%rdi)
 2cff79b:      	je	0x2cff7a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff79d:      	movl	%edx, %edi
 2cff79f:      	cmpq	%rcx, %rdi
 2cff7a2:      	jne	0x2cff7e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2630>
 2cff7a4:      	movl	%edx, %edx
 2cff7a6:      	cmpq	%rcx, %rdx
 2cff7a9:      	jne	0x2cff7d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2620>
 2cff7ab:      	testb	$0x4, (%rax)
 2cff7ae:      	jne	0x2cff770 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff7b0:      	testb	$0x8, 0x2c(%rax)
 2cff7b4:      	je	0x2cff770 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff7b6:      	movq	0x8(%rax), %rax
 2cff7ba:      	testb	$0x8, 0x2c(%rax)
 2cff7be:      	jne	0x2cff7b6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2606>
 2cff7c0:      	jmp	0x2cff770 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff7c2:      	nopw	%cs:(%rax,%rax)
 2cff7cc:      	nopl	(%rax)
 2cff7d0:      	shll	$0x5, %ecx
 2cff7d3:      	addq	%rsi, %rcx
 2cff7d6:      	shlq	$0x5, %rdx
 2cff7da:      	addq	%rsi, %rdx
 2cff7dd:      	jmp	0x2cff85d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26ad>
 2cff7df:      	nop
 2cff7e0:      	movl	%ecx, %r8d
 2cff7e3:      	shll	$0x5, %r8d
 2cff7e7:      	addq	$-0x20, %r8
 2cff7eb:      	shll	$0x5, %edi
 2cff7ee:      	nop
 2cff7f0:      	movl	(%rsi,%rdi), %r9d
 2cff7f4:      	movl	%r9d, %r10d
 2cff7f7:      	andl	$0x10000ff, %r10d       # imm = 0x10000FF
 2cff7fe:      	cmpl	$0x1000000, %r10d       # imm = 0x1000000
 2cff805:      	jne	0x2cff7a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff807:      	shrl	$0x19, %r9d
 2cff80b:      	andl	$0x1, %r9d
 2cff80f:      	movl	%r9d, %r10d
 2cff812:      	xorl	$0x1, %r10d
 2cff816:      	addl	%r10d, %edx
 2cff819:      	testl	%r9d, %r9d
 2cff81c:      	jne	0x2cff7a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff81e:      	cmpq	%rdi, %r8
 2cff821:      	leaq	0x20(%rdi), %rdi
 2cff825:      	jne	0x2cff7f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2640>
 2cff827:      	jmp	0x2cff7a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff82c:      	cmpl	$-0x1, %ebx
 2cff82f:      	je	0x2cff850 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff831:      	addl	%r11d, %r10d
 2cff834:      	incl	%r11d
 2cff837:      	andl	%edi, %r10d
 2cff83a:      	movl	(%r9,%r10,4), %ebx
 2cff83e:      	cmpl	%ebx, %r8d
 2cff841:      	jne	0x2cff82c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x267c>
 2cff843:      	andl	$0xfbffff00, %esi       # imm = 0xFBFFFF00
 2cff849:      	movl	%esi, (%rdx)
 2cff84b:      	nopl	(%rax,%rax)
 2cff850:      	addq	$0x20, %rdx
 2cff854:      	cmpq	%rcx, %rdx
 2cff857:      	je	0x2cff7ab <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25fb>
 2cff85d:      	movl	(%rdx), %esi
 2cff85f:      	testb	%sil, %sil
 2cff862:      	jne	0x2cff850 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff864:      	movl	%esi, %edi
 2cff866:      	shrl	$0x1a, %edi
 2cff869:      	xorl	%r8d, %r8d
 2cff86c:      	testl	$0x1000000, %esi        # imm = 0x1000000
 2cff872:      	sete	%r8b
 2cff876:      	testl	%edi, %r8d
 2cff879:      	je	0x2cff850 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff87b:      	movl	0x1f0(%rsp), %edi
 2cff882:      	testl	%edi, %edi
 2cff884:      	je	0x2cff850 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff886:      	movl	0x4(%rdx), %r8d
 2cff88a:      	movq	0x1e0(%rsp), %r9
 2cff892:      	leal	(%r8,%r8,8), %r10d
 2cff896:      	leal	(%r8,%r10,4), %r10d
 2cff89a:      	decl	%edi
 2cff89c:      	andl	%edi, %r10d
 2cff89f:      	movl	(%r9,%r10,4), %ebx
 2cff8a3:      	cmpl	%ebx, %r8d
 2cff8a6:      	je	0x2cff843 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2693>
 2cff8a8:      	movl	$0x1, %r11d
 2cff8ae:      	jmp	0x2cff82c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x267c>
 2cff8b3:      	nopw	%cs:(%rax,%rax)
 2cff8bd:      	nopl	(%rax)
 2cff8c0:      	movl	0x1c8(%rsp), %eax
 2cff8c7:      	movq	%rax, 0x18(%rsp)
 2cff8cc:      	testq	%rax, %rax
 2cff8cf:      	je	0x2cff93d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x278d>
 2cff8d1:      	movq	0x18(%r13), %rax
 2cff8d5:      	movq	0x20(%rax), %rbx
 2cff8d9:      	movq	0x1c0(%rsp), %r15
 2cff8e1:      	shlq	$0x2, 0x18(%rsp)
 2cff8e7:      	xorl	%r12d, %r12d
 2cff8ea:      	movq	%r13, %r14
 2cff8ed:      	leaq	0x40(%rsp), %r13
 2cff8f2:      	leaq	0x30(%rsp), %rbp
 2cff8f7:      	nopw	(%rax,%rax)
 2cff900:      	movl	(%r15,%r12), %eax
 2cff904:      	movq	$0x0, 0x38(%rsp)
 2cff90d:      	movl	%eax, 0x34(%rsp)
 2cff911:      	movups	%xmm0, (%r13)
 2cff916:      	movl	$0x3000000, 0x30(%rsp)  # imm = 0x3000000
 2cff91e:      	movq	%r14, %rdi
 2cff921:      	movq	%rbx, %rsi
 2cff924:      	movq	%rbp, %rdx
 2cff927:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff92c:      	xorps	%xmm0, %xmm0
 2cff92f:      	addq	$0x4, %r12
 2cff933:      	cmpq	%r12, 0x18(%rsp)
 2cff938:      	jne	0x2cff900 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2750>
 2cff93a:      	movq	%r14, %r13
 2cff93d:      	movq	0xc8(%rsp), %rsi
 2cff945:      	testq	%rsi, %rsi
 2cff948:      	je	0x2cff957 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27a7>
 2cff94a:      	leaq	0xc8(%rsp), %rdi
 2cff952:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff957:      	movq	0x1e0(%rsp), %rdi
 2cff95f:      	movl	0x1f0(%rsp), %esi
 2cff966:      	shlq	$0x2, %rsi
 2cff96a:      	movl	$0x4, %edx
 2cff96f:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 2cff974:      	movq	0x200(%rsp), %rdi
 2cff97c:      	movl	0x210(%rsp), %esi
 2cff983:      	shlq	$0x2, %rsi
 2cff987:      	movl	$0x4, %edx
 2cff98c:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 2cff991:      	movq	0x1c0(%rsp), %rdi
 2cff999:      	leaq	0x1d0(%rsp), %rax
 2cff9a1:      	cmpq	%rax, %rdi
 2cff9a4:      	je	0x2cff9ab <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27fb>
 2cff9a6:      	callq	0x828a640 <free@plt>
 2cff9ab:      	movq	0x130(%rsp), %rdi
 2cff9b3:      	leaq	0x140(%rsp), %rax
 2cff9bb:      	cmpq	%rax, %rdi
 2cff9be:      	je	0x2cff9c5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2815>
 2cff9c0:      	callq	0x828a640 <free@plt>
 2cff9c5:      	testq	%r13, %r13
 2cff9c8:      	je	0x2cffa00 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2850>
 2cff9ca:      	movzwl	0x44(%r13), %eax
 2cff9cf:      	cmpl	$0x1101, %eax           # imm = 0x1101
 2cff9d4:      	movq	(%rsp), %rdi
 2cff9d8:      	je	0x2cff9e1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2831>
 2cff9da:      	cmpl	$0x102f, %eax           # imm = 0x102F
 2cff9df:      	jne	0x2cffa54 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x28a4>
 2cff9e1:      	movq	%r13, %rsi
 2cff9e4:      	callq	0x2d02970 <_ZNK12_GLOBAL__N_115ARMLoadStoreOpt23MergeBaseUpdateLSDoubleERN4llvm12MachineInstrE>
 2cff9e9:      	movq	(%rsp), %rdi
 2cff9ed:      	movb	$0x1, %al
 2cff9ef:      	jmp	0x2cfe6ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cff9f4:      	nopw	%cs:(%rax,%rax)
 2cff9fe:      	nop
 2cffa00:      	movq	0x90(%rsp), %rax
 2cffa08:      	movl	0x8(%rax), %ebx
 2cffa0b:      	testq	%rbx, %rbx
 2cffa0e:      	movq	(%rsp), %rdi
 2cffa12:      	je	0x2cffaec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x293c>
 2cffa18:      	movq	(%rax), %r14
 2cffa1b:      	shlq	$0x3, %rbx
 2cffa1f:      	xorl	%r15d, %r15d
 2cffa22:      	movq	0x98(%rsp), %rax
 2cffa2a:      	nopw	(%rax,%rax)
 2cffa30:      	movq	(%r14,%r15), %rsi
 2cffa34:      	movq	%rax, %r12
 2cffa37:      	callq	0x2d03380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt24MergeBaseUpdateLoadStoreEPN4llvm12MachineInstrE>
 2cffa3c:      	movq	(%rsp), %rdi
 2cffa40:      	orb	%al, %r12b
 2cffa43:      	movq	%r12, %rax
 2cffa46:      	addq	$0x8, %r15
 2cffa4a:      	cmpq	%r15, %rbx
 2cffa4d:      	jne	0x2cffa30 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2880>
 2cffa4f:      	jmp	0x2cfe6ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cffa54:      	cmpb	$0x0, 0x202(%rdi)
 2cffa5b:      	jne	0x2cff9ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x283d>
 2cffa5d:      	movq	%rax, 0x20(%rsp)
 2cffa62:      	movq	0x10(%r13), %rcx
 2cffa66:      	movq	0x20(%r13), %rax
 2cffa6a:      	movl	(%rax), %r12d
 2cffa6d:      	testl	$0x1000000, %r12d       # imm = 0x1000000
 2cffa74:      	sete	%r14b
 2cffa78:      	movl	$0xe, 0x8(%rsp)
 2cffa80:      	xorl	%ebx, %ebx
 2cffa82:      	testb	$0x40, 0x12(%rcx)
 2cffa86:      	je	0x2cffdad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffa8c:      	movzwl	0x28(%r13), %edx
 2cffa91:      	movzbl	0x2a(%r13), %esi
 2cffa96:      	shll	$0x10, %esi
 2cffa99:      	orl	%edx, %esi
 2cffa9b:      	testl	%esi, %esi
 2cffa9d:      	je	0x2cffdad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffaa3:      	movzwl	(%rcx), %edi
 2cffaa6:      	movzwl	0xa(%rcx), %r8d
 2cffaab:      	leaq	0x10(%rax), %rdx
 2cffaaf:      	addl	%esi, %esi
 2cffab1:      	leaq	(%rsi,%rsi,2), %rsi
 2cffab5:      	shll	$0x5, %edi
 2cffab8:      	leaq	(%r8,%r8,2), %r8
 2cffabc:      	leaq	(%rdi,%r8,2), %rdi
 2cffac0:      	leaq	0x22(%rcx,%rdi), %rcx
 2cffac5:      	xorl	%edi, %edi
 2cffac7:      	nopw	(%rax,%rax)
 2cffad0:      	testb	$0x2, (%rcx,%rdi)
 2cffad4:      	jne	0x2cffda4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bf4>
 2cffada:      	addq	$0x20, %rdx
 2cffade:      	addq	$0x6, %rdi
 2cffae2:      	cmpq	%rdi, %rsi
 2cffae5:      	jne	0x2cffad0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2920>
 2cffae7:      	jmp	0x2cffdad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffaec:      	movq	0x98(%rsp), %rax
 2cffaf4:      	jmp	0x2cfe6ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cffaf9:      	movq	%r12, %r9
 2cffafc:      	movb	$0x1, %dl
 2cffafe:      	movq	0x78(%rsp), %rbx
 2cffb03:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffb09:      	je	0x2cffb3b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x298b>
 2cffb0b:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffb11:      	movq	0x8(%rsp), %r12
 2cffb16:      	movl	0x18(%rsp), %r8d
 2cffb1b:      	je	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffb1d:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffb23:      	je	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffb25:      	movl	%ebx, %esi
 2cffb27:      	andl	$-0x2, %esi
 2cffb2a:      	cmpl	$0x104c, %esi           # imm = 0x104C
 2cffb30:      	jne	0x2cffd4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b9d>
 2cffb36:      	movl	%eax, %r10d
 2cffb39:      	jmp	0x2cffb48 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2998>
 2cffb3b:      	movl	%eax, %r10d
 2cffb3e:      	movq	0x8(%rsp), %r12
 2cffb43:      	movl	0x18(%rsp), %r8d
 2cffb48:      	movq	(%rsp), %rsi
 2cffb4c:      	movzbl	0x203(%rsi), %esi
 2cffb53:      	orb	%sil, %cl
 2cffb56:      	sete	%cl
 2cffb59:      	andb	%dl, %cl
 2cffb5b:      	cmpl	$0x4, %r8d
 2cffb5f:      	jne	0x2cffb80 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29d0>
 2cffb61:      	testb	%cl, %cl
 2cffb63:      	je	0x2cffb80 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29d0>
 2cffb65:      	xorl	%eax, %eax
 2cffb67:      	movl	$0x2, %ecx
 2cffb6c:      	movb	$0x1, %sil
 2cffb6f:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffb75:      	jne	0x2cffc69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2cffb7b:      	jmp	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffb80:      	leal	(,%r9,4), %edi
 2cffb88:      	movl	%r8d, %r11d
 2cffb8b:      	movl	$0x4, %r8d
 2cffb91:      	subl	%edi, %r8d
 2cffb94:      	cmpl	%r8d, %r11d
 2cffb97:      	sete	%r8b
 2cffb9b:      	testb	%cl, %r8b
 2cffb9e:      	je	0x2cffbaa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29fa>
 2cffba0:      	movl	$0x3, %ecx
 2cffba5:      	jmp	0x2cffc5c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2aac>
 2cffbaa:      	negl	%edi
 2cffbac:      	cmpl	%edi, %r11d
 2cffbaf:      	setne	%cl
 2cffbb2:      	xorb	$0x1, %dl
 2cffbb5:      	orb	%dl, %al
 2cffbb7:      	orb	%cl, %al
 2cffbb9:      	cmpb	$0x1, %al
 2cffbbb:      	jne	0x2cffc57 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2aa7>
 2cffbc1:      	testl	%r11d, %r11d
 2cffbc4:      	je	0x2d00606 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3456>
 2cffbca:      	cmpl	$0x3, %r9d
 2cffbce:      	setb	%al
 2cffbd1:      	orb	%r15b, %al
 2cffbd4:      	jne	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffbda:      	movq	0x78(%rsp), %rbx
 2cffbdf:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffbe5:      	je	0x2cffc07 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffbe7:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffbed:      	je	0x2cffc07 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffbef:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffbf5:      	je	0x2cffc07 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffbf7:      	movl	%ebx, %eax
 2cffbf9:      	andl	$-0x2, %eax
 2cffbfc:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cffc01:      	jne	0x2d0126c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40bc>
 2cffc07:      	leal	-0x1(%r9), %eax
 2cffc0b:      	movl	(%r14,%rax,8), %r12d
 2cffc0f:      	xorl	%eax, %eax
 2cffc11:      	movq	(%rsp), %rcx
 2cffc15:      	movl	0x18(%rsp), %r8d
 2cffc1a:      	movl	%eax, 0xdc(%rsp)
 2cffc21:      	testb	%sil, %sil
 2cffc24:      	je	0x2d01620 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4470>
 2cffc2a:      	cmpl	$-0x1, 0x70(%rsp)
 2cffc2f:      	setne	%al
 2cffc32:      	cmpl	$0x11, 0x8(%rsp)
 2cffc37:      	sete	%cl
 2cffc3a:      	andb	%al, %cl
 2cffc3c:      	movzbl	%cl, %eax
 2cffc3f:      	movq	%r9, %rbx
 2cffc42:      	testl	%r8d, %r8d
 2cffc45:      	js	0x2d0125d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40ad>
 2cffc4b:      	leal	0xfc5(,%rax,4), %esi
 2cffc52:      	jmp	0x2d01685 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d5>
 2cffc57:      	movl	$0x4, %ecx
 2cffc5c:      	xorl	%eax, %eax
 2cffc5e:      	movb	$0x1, %sil
 2cffc61:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffc67:      	je	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffc69:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffc6f:      	je	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffc71:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffc77:      	je	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffc79:      	movl	%ebx, %edx
 2cffc7b:      	andl	$-0x2, %edx
 2cffc7e:      	cmpl	$0x104c, %edx           # imm = 0x104C
 2cffc84:      	sete	%sil
 2cffc88:      	cmpl	$0xb51, 0xc0(%rsp)      # imm = 0xB51
 2cffc93:      	sete	%dil
 2cffc97:      	cmpl	$0x104b, %ebx           # imm = 0x104B
 2cffc9d:      	jle	0x2cffcc8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b18>
 2cffc9f:      	leal	-0x117a(%rbx), %ecx
 2cffca5:      	cmpl	$0x1f, %ecx
 2cffca8:      	jbe	0x2cffcf8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b48>
 2cffcaa:      	leal	-0x104c(%rbx), %ecx
 2cffcb0:      	movzbl	%al, %eax
 2cffcb3:      	cmpl	$0x2, %ecx
 2cffcb6:      	jae	0x2cffd41 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b91>
 2cffcbc:      	leal	0x1022(%rax,%rax), %ebx
 2cffcc3:      	jmp	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffcc8:      	cmpl	$0xb52, %ebx            # imm = 0xB52
 2cffcce:      	jg	0x2cffd17 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b67>
 2cffcd0:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffcd6:      	je	0x2cfff98 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2de8>
 2cffcdc:      	cmpl	$0x7f9, %ebx            # imm = 0x7F9
 2cffce2:      	jne	0x2cfffb3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e03>
 2cffce8:      	leaq	-0x1edc01f(%rip), %rax  # 0xe23cd0 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.150>
 2cffcef:      	movl	-0x4(%rax,%rcx,4), %ebx
 2cffcf3:      	jmp	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffcf8:      	movl	$0x1173, %ebx           # imm = 0x1173
 2cffcfd:      	leaq	-0x19b0b9c(%rip), %rdx  # 0x134f168 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x4d2>
 2cffd04:      	movslq	(%rdx,%rcx,4), %rax
 2cffd08:      	addq	%rdx, %rax
 2cffd0b:      	jmpq	*%rax
 2cffd0d:      	movl	$0x1192, %ebx           # imm = 0x1192
 2cffd12:      	jmp	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd17:      	cmpl	$0xb53, %ebx            # imm = 0xB53
 2cffd1d:      	je	0x2cfffa5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2df5>
 2cffd23:      	cmpl	$0xf2e, %ebx            # imm = 0xF2E
 2cffd29:      	jne	0x2cfffc1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e11>
 2cffd2f:      	movl	$0xf28, %ebx            # imm = 0xF28
 2cffd34:      	testb	%al, %al
 2cffd36:      	jne	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd3c:      	jmp	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffd41:      	leal	0x10f5(%rax,%rax), %ebx
 2cffd48:      	jmp	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd4d:      	cmpl	$0x7f9, %ebx            # imm = 0x7F9
 2cffd53:      	je	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffd59:      	cmpl	$0x1197, %ebx           # imm = 0x1197
 2cffd5f:      	je	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffd65:      	cmpl	$0x1199, %ebx           # imm = 0x1199
 2cffd6b:      	je	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffd71:      	leal	-0x110f(%rbx), %edx
 2cffd77:      	cmpw	$0x2, %dx
 2cffd7b:      	setb	%dl
 2cffd7e:      	jmp	0x2cffb36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffd83:      	movb	$0x1, %al
 2cffd85:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffd8b:      	je	0x2d00d82 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bd2>
 2cffd91:      	movb	$0x1, %cl
 2cffd93:      	cmpl	$0x1197, %ebx           # imm = 0x1197
 2cffd99:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffd9f:      	jmp	0x2cffafc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cffda4:      	movl	(%rdx), %ecx
 2cffda6:      	movl	%ecx, 0x8(%rsp)
 2cffdaa:      	movl	0x14(%rdx), %ebx
 2cffdad:      	movl	0x4(%rax), %ebp
 2cffdb0:      	movq	0x38(%r13), %rsi
 2cffdb4:      	movq	%rsi, 0xa0(%rsp)
 2cffdbc:      	testq	%rsi, %rsi
 2cffdbf:      	je	0x2cffdd7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c27>
 2cffdc1:      	movl	$0x1, %edx
 2cffdc6:      	leaq	0xa0(%rsp), %rdi
 2cffdce:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cffdd3:      	movq	0x20(%r13), %rax
 2cffdd7:      	movzwl	0x28(%r13), %edx
 2cffddc:      	movzbl	0x2a(%r13), %ecx
 2cffde1:      	shll	$0x10, %ecx
 2cffde4:      	orl	%edx, %ecx
 2cffde6:      	cmpl	$0x2, %ecx
 2cffde9:      	je	0x2cffe13 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c63>
 2cffdeb:      	shll	$0x5, %ecx
 2cffdee:      	addq	$-0x40, %rcx
 2cffdf2:      	xorl	%edx, %edx
 2cffdf4:      	nopw	%cs:(%rax,%rax)
 2cffdfe:      	nop
 2cffe00:      	cmpl	%ebp, 0x44(%rax,%rdx)
 2cffe04:      	je	0x2d0102b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2cffe0a:      	addq	$0x20, %rdx
 2cffe0e:      	cmpq	%rdx, %rcx
 2cffe11:      	jne	0x2cffe00 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c50>
 2cffe13:      	movl	%ebp, 0x90(%rsp)
 2cffe1a:      	movq	%r13, %rdi
 2cffe1d:      	callq	0x2cf9d70 <_ZL25getLSMultipleTransferSizePKN4llvm12MachineInstrE>
 2cffe22:      	movl	%eax, 0x10(%rsp)
 2cffe26:      	movq	0x18(%r13), %rcx
 2cffe2a:      	movl	$0x0, 0x1c0(%rsp)
 2cffe35:      	movq	0x38(%rcx), %rax
 2cffe39:      	movq	%rcx, 0x18(%rsp)
 2cffe3e:      	leaq	0x30(%rcx), %r15
 2cffe42:      	cmpq	%rax, %r13
 2cffe45:      	movl	%ebx, 0x78(%rsp)
 2cffe49:      	je	0x2cffee9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d39>
 2cffe4f:      	movq	(%r13), %rbp
 2cffe53:      	andq	$-0x8, %rbp
 2cffe57:      	testb	$0x4, (%rbp)
 2cffe5b:      	jne	0x2cffe74 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cc4>
 2cffe5d:      	nopl	(%rax)
 2cffe60:      	testb	$0x4, 0x2c(%rbp)
 2cffe64:      	je	0x2cffe74 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cc4>
 2cffe66:      	movq	(%rbp), %rbp
 2cffe6a:      	andq	$-0x8, %rbp
 2cffe6e:      	testb	$0x4, 0x2c(%rbp)
 2cffe72:      	jne	0x2cffe66 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cb6>
 2cffe74:      	cmpq	%rax, %rbp
 2cffe77:      	je	0x2cffec5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cffe79:      	movl	0x44(%rbp), %ecx
 2cffe7c:      	addl	$-0xe, %ecx
 2cffe7f:      	cmpw	$0x4, %cx
 2cffe83:      	ja	0x2cffec5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cffe85:      	nopw	%cs:(%rax,%rax)
 2cffe8f:      	nop
 2cffe90:      	movq	(%rbp), %rbp
 2cffe94:      	andq	$-0x8, %rbp
 2cffe98:      	testb	$0x4, (%rbp)
 2cffe9c:      	jne	0x2cffeb4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d04>
 2cffe9e:      	nop
 2cffea0:      	testb	$0x4, 0x2c(%rbp)
 2cffea4:      	je	0x2cffeb4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d04>
 2cffea6:      	movq	(%rbp), %rbp
 2cffeaa:      	andq	$-0x8, %rbp
 2cffeae:      	testb	$0x4, 0x2c(%rbp)
 2cffeb2:      	jne	0x2cffea6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cf6>
 2cffeb4:      	cmpq	%rax, %rbp
 2cffeb7:      	je	0x2cffec5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cffeb9:      	movl	0x44(%rbp), %ecx
 2cffebc:      	addl	$-0xe, %ecx
 2cffebf:      	cmpw	$0x5, %cx
 2cffec3:      	jb	0x2cffe90 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ce0>
 2cffec5:      	movq	%rbp, %rdi
 2cffec8:      	movl	0x90(%rsp), %esi
 2cffecf:      	movl	0x8(%rsp), %edx
 2cffed3:      	movl	%ebx, %ecx
 2cffed5:      	callq	0x2d052c0 <_ZL22isIncrementOrDecrementRKN4llvm12MachineInstrENS_8RegisterENS_5ARMCC9CondCodesES3_>
 2cffeda:      	movl	%eax, 0x1c0(%rsp)
 2cffee1:      	testl	%eax, %eax
 2cffee3:      	cmoveq	%r15, %rbp
 2cffee7:      	jmp	0x2cffeee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d3e>
 2cffee9:      	xorl	%eax, %eax
 2cffeeb:      	movq	%r15, %rbp
 2cffeee:      	shrl	$0x1a, %r12d
 2cffef2:      	xorl	%ecx, %ecx
 2cffef4:      	movb	%r14b, %cl
 2cffef7:      	andl	%r12d, %ecx
 2cffefa:      	movl	%ecx, 0x98(%rsp)
 2cfff01:      	movb	$0x1, %bl
 2cfff03:      	movq	0x20(%rsp), %rcx
 2cfff08:      	cmpl	$0xb49, %ecx            # imm = 0xB49
 2cfff0e:      	xorps	%xmm0, %xmm0
 2cfff11:      	movq	%r13, 0x28(%rsp)
 2cfff16:      	jle	0x2cfff4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d9d>
 2cfff18:      	cmpl	$0x1021, %ecx           # imm = 0x1021
 2cfff1e:      	jg	0x2cfff64 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2db4>
 2cfff20:      	addl	$0xfffff4b6, %ecx       # imm = 0xFFFFF4B6
 2cfff26:      	cmpl	$0x6, %ecx
 2cfff29:      	jbe	0x2d00639 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3489>
 2cfff2f:      	movq	0x20(%rsp), %rcx
 2cfff34:      	addl	$0xfffff0d9, %ecx       # imm = 0xFFFFF0D9
 2cfff3a:      	movl	$0x66, %edx
 2cfff3f:      	btl	%ecx, %edx
 2cfff42:      	jb	0x2d00966 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cfff48:      	jmp	0x2d0098e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cfff4d:      	cmpl	$0x3a9, %ecx            # imm = 0x3A9
 2cfff53:      	jg	0x2d005d5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3425>
 2cfff59:      	cmpl	$0x16b, %ecx            # imm = 0x16B
 2cfff5f:      	jmp	0x2d00966 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cfff64:      	cmpl	$0x10f6, %ecx           # imm = 0x10F6
 2cfff6a:      	jg	0x2d0095d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37ad>
 2cfff70:      	addl	$0xffffefde, %ecx       # imm = 0xFFFFEFDE
 2cfff76:      	cmpl	$0x2, %ecx
 2cfff79:      	jb	0x2d0098e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cfff7f:      	movq	0x20(%rsp), %rcx
 2cfff84:      	addl	$0xffffefdc, %ecx       # imm = 0xFFFFEFDC
 2cfff8a:      	cmpl	$0x2, %ecx
 2cfff8d:      	jae	0x2d0098e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cfff93:      	jmp	0x2d00966 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cfff98:      	leaq	-0x1eee33f(%rip), %rax  # 0xe11c60 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE>
 2cfff9f:      	movl	-0x4(%rax,%rcx,4), %ebx
 2cfffa3:      	jmp	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cfffa5:      	movl	$0xb4f, %ebx            # imm = 0xB4F
 2cfffaa:      	testb	%al, %al
 2cfffac:      	jne	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cfffae:      	jmp	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfffb3:      	movl	$0xb4b, %ebx            # imm = 0xB4B
 2cfffb8:      	testb	%al, %al
 2cfffba:      	jne	0x2cfffce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cfffbc:      	jmp	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfffc1:      	movl	$0xf2c, %ebx            # imm = 0xF2C
 2cfffc6:      	testb	%al, %al
 2cfffc8:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfffce:      	movq	(%rsp), %rax
 2cfffd2:      	andb	0x202(%rax), %r15b
 2cfffd9:      	andb	%r10b, %r15b
 2cfffdc:      	xorb	$0x1, %r15b
 2cfffe0:      	orb	%r13b, %r15b
 2cfffe3:      	cmpb	$0x1, %r15b
 2cfffe7:      	jne	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfffed:      	movb	%dil, 0xc0(%rsp)
 2cffff5:      	movb	%sil, 0x8(%rsp)
 2cffffa:      	movq	%r9, 0x80(%rsp)
 2d00002:      	movzbl	%r13b, %ebp
 2d00006:      	testb	%r10b, %r10b
 2d00009:      	movq	%r14, 0x180(%rsp)
 2d00011:      	je	0x2d0018c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2fdc>
 2d00017:      	cmpl	$0x1173, %ebx           # imm = 0x1173
 2d0001d:      	movl	$0x30a, %eax            # imm = 0x30A
 2d00022:      	cmovel	%eax, %ebx
 2d00025:      	movq	0xc8(%rsp), %rsi
 2d0002d:      	movq	%rsi, 0x190(%rsp)
 2d00035:      	leaq	0x30(%rsp), %rax
 2d0003a:      	testq	%rsi, %rsi
 2d0003d:      	je	0x2d0007b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ecb>
 2d0003f:      	movl	$0x1, %edx
 2d00044:      	leaq	0x190(%rsp), %rdi
 2d0004c:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d00051:      	movq	0x190(%rsp), %rsi
 2d00059:      	movq	%rsi, 0x30(%rsp)
 2d0005e:      	testq	%rsi, %rsi
 2d00061:      	je	0x2d00082 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ed2>
 2d00063:      	leaq	0x190(%rsp), %r15
 2d0006b:      	movq	%r15, %rdi
 2d0006e:      	leaq	0x30(%rsp), %rdx
 2d00073:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d00078:      	movq	%r15, %rax
 2d0007b:      	movq	$0x0, (%rax)
 2d00082:      	leaq	0x40(%rsp), %rax
 2d00087:      	xorps	%xmm0, %xmm0
 2d0008a:      	movups	%xmm0, -0x8(%rax)
 2d0008e:      	movq	$0x0, 0x8(%rax)
 2d00096:      	movq	(%rsp), %rax
 2d0009a:      	movq	0x40(%rax), %rax
 2d0009e:      	movq	0x8(%rax), %rcx
 2d000a2:      	movl	%ebx, %eax
 2d000a4:      	shlq	$0x5, %rax
 2d000a8:      	subq	%rax, %rcx
 2d000ab:      	movq	0x10(%rsp), %rdi
 2d000b0:      	movq	0x20(%rsp), %rsi
 2d000b5:      	leaq	0x30(%rsp), %rbx
 2d000ba:      	movq	%rbx, %rdx
 2d000bd:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d000c2:      	movq	%rax, 0x70(%rsp)
 2d000c7:      	movq	%rdx, %r15
 2d000ca:      	movq	0x30(%rsp), %rsi
 2d000cf:      	testq	%rsi, %rsi
 2d000d2:      	je	0x2d000dc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2f2c>
 2d000d4:      	movq	%rbx, %rdi
 2d000d7:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d000dc:      	movq	0x190(%rsp), %rsi
 2d000e4:      	testq	%rsi, %rsi
 2d000e7:      	je	0x2d000f6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2f46>
 2d000e9:      	leaq	0x190(%rsp), %rdi
 2d000f1:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d000f6:      	movq	$0x0, 0x38(%rsp)
 2d000ff:      	movl	%r12d, 0x34(%rsp)
 2d00104:      	leaq	0x40(%rsp), %rbx
 2d00109:      	xorps	%xmm0, %xmm0
 2d0010c:      	movups	%xmm0, (%rbx)
 2d0010f:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2d00117:      	movq	%r15, %rdi
 2d0011a:      	movq	0x70(%rsp), %r14
 2d0011f:      	movq	%r14, %rsi
 2d00122:      	movq	%r12, %r13
 2d00125:      	leaq	0x30(%rsp), %r12
 2d0012a:      	movq	%r12, %rdx
 2d0012d:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00132:      	movq	$0x0, 0x38(%rsp)
 2d0013b:      	movl	%ebp, %eax
 2d0013d:      	shll	$0x1a, %eax
 2d00140:      	movq	%r13, 0x18(%rsp)
 2d00145:      	movl	%r13d, 0x34(%rsp)
 2d0014a:      	xorps	%xmm0, %xmm0
 2d0014d:      	movups	%xmm0, (%rbx)
 2d00150:      	movl	%eax, 0x30(%rsp)
 2d00154:      	movq	%r15, %rdi
 2d00157:      	movq	%r14, %rsi
 2d0015a:      	movq	%r12, %rdx
 2d0015d:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00162:      	testb	%bpl, %bpl
 2d00165:      	jne	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0016b:      	movq	0x10(%rsp), %rax
 2d00170:      	leaq	0x30(%rax), %rbp
 2d00174:      	movq	0x20(%rsp), %r13
 2d00179:      	cmpq	%rbp, %r13
 2d0017c:      	je	0x2d0065a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x34aa>
 2d00182:      	movq	0x18(%rsp), %r12
 2d00187:      	jmp	0x2d002ad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30fd>
 2d0018c:      	movq	0xc8(%rsp), %rsi
 2d00194:      	movq	%rsi, 0x188(%rsp)
 2d0019c:      	leaq	0x30(%rsp), %rax
 2d001a1:      	testq	%rsi, %rsi
 2d001a4:      	je	0x2d001e2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3032>
 2d001a6:      	movl	$0x1, %edx
 2d001ab:      	leaq	0x188(%rsp), %rdi
 2d001b3:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d001b8:      	movq	0x188(%rsp), %rsi
 2d001c0:      	movq	%rsi, 0x30(%rsp)
 2d001c5:      	testq	%rsi, %rsi
 2d001c8:      	je	0x2d001e9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3039>
 2d001ca:      	leaq	0x188(%rsp), %r15
 2d001d2:      	movq	%r15, %rdi
 2d001d5:      	leaq	0x30(%rsp), %rdx
 2d001da:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d001df:      	movq	%r15, %rax
 2d001e2:      	movq	$0x0, (%rax)
 2d001e9:      	leaq	0x40(%rsp), %rax
 2d001ee:      	xorps	%xmm0, %xmm0
 2d001f1:      	movups	%xmm0, -0x8(%rax)
 2d001f5:      	movq	$0x0, 0x8(%rax)
 2d001fd:      	movq	(%rsp), %rax
 2d00201:      	movq	0x40(%rax), %rax
 2d00205:      	movq	0x8(%rax), %rcx
 2d00209:      	movl	%ebx, %eax
 2d0020b:      	shlq	$0x5, %rax
 2d0020f:      	subq	%rax, %rcx
 2d00212:      	movq	0x10(%rsp), %rdi
 2d00217:      	movq	0x20(%rsp), %rsi
 2d0021c:      	leaq	0x30(%rsp), %rbx
 2d00221:      	movq	%rbx, %rdx
 2d00224:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d00229:      	movq	%rax, %r14
 2d0022c:      	movq	%rdx, %r15
 2d0022f:      	movq	0x30(%rsp), %rsi
 2d00234:      	testq	%rsi, %rsi
 2d00237:      	je	0x2d00241 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3091>
 2d00239:      	movq	%rbx, %rdi
 2d0023c:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00241:      	movq	0x188(%rsp), %rsi
 2d00249:      	testq	%rsi, %rsi
 2d0024c:      	je	0x2d0025b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30ab>
 2d0024e:      	leaq	0x188(%rsp), %rdi
 2d00256:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d0025b:      	movq	$0x0, 0x38(%rsp)
 2d00264:      	shll	$0x1a, %ebp
 2d00267:      	movl	%r12d, 0x34(%rsp)
 2d0026c:      	leaq	0x40(%rsp), %rbx
 2d00271:      	xorps	%xmm0, %xmm0
 2d00274:      	movups	%xmm0, (%rbx)
 2d00277:      	movl	%ebp, 0x30(%rsp)
 2d0027b:      	movq	%r15, %rdi
 2d0027e:      	movq	%r14, %rsi
 2d00281:      	leaq	0x30(%rsp), %r13
 2d00286:      	movq	%r13, %rdx
 2d00289:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d0028e:      	jmp	0x2d00862 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36b2>
 2d00293:      	nopw	%cs:(%rax,%rax)
 2d0029d:      	nopl	(%rax)
 2d002a0:      	movq	0x8(%r13), %r13
 2d002a4:      	cmpq	%rbp, %r13
 2d002a7:      	je	0x2d0065f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x34af>
 2d002ad:      	movzwl	0x44(%r13), %ebx
 2d002b2:      	movq	%r13, %rdi
 2d002b5:      	movl	%r12d, %esi
 2d002b8:      	xorl	%edx, %edx
 2d002ba:      	xorl	%ecx, %ecx
 2d002bc:      	callq	0x36556b0 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2d002c1:      	cmpl	$-0x1, %eax
 2d002c4:      	movq	%r13, %r12
 2d002c7:      	je	0x2d00346 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3196>
 2d002c9:      	leal	-0x1174(%rbx), %esi
 2d002cf:      	cmpl	$0x23, %esi
 2d002d2:      	movq	0x80(%rsp), %r9
 2d002da:      	ja	0x2d02059 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ea9>
 2d002e0:      	movabsq	$0xa80000045, %rax      # imm = 0xA80000045
 2d002ea:      	btq	%rsi, %rax
 2d002ee:      	jae	0x2d02059 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ea9>
 2d002f4:      	movq	0x10(%r13), %rcx
 2d002f8:      	movq	0x20(%r13), %rax
 2d002fc:      	movzwl	0x2(%rcx), %ecx
 2d00300:      	movl	$0xfffffffd, %edx       # imm = 0xFFFFFFFD
 2d00305:      	addl	%ecx, %edx
 2d00307:      	shlq	$0x5, %rdx
 2d0030b:      	leaq	(%rax,%rdx), %rcx
 2d0030f:      	movq	0x10(%rax,%rdx), %rdx
 2d00314:      	movl	$0xffffffff, %edi       # imm = 0xFFFFFFFF
 2d00319:      	movabsq	$0x800000240, %r8       # imm = 0x800000240
 2d00323:      	btq	%rsi, %r8
 2d00327:      	jb	0x2d003d3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3223>
 2d0032d:      	movl	$0x80000001, %edi       # imm = 0x80000001
 2d00332:      	btq	%rsi, %rdi
 2d00336:      	jae	0x2d003ce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x321e>
 2d0033c:      	movl	$0xfffffffc, %edi       # imm = 0xFFFFFFFC
 2d00341:      	jmp	0x2d003d3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3223>
 2d00346:      	movzwl	0x28(%r13), %ecx
 2d0034b:      	movzbl	0x2a(%r13), %eax
 2d00350:      	shll	$0x10, %eax
 2d00353:      	orl	%ecx, %eax
 2d00355:      	testl	%eax, %eax
 2d00357:      	je	0x2d003a2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31f2>
 2d00359:      	movq	0x20(%r12), %rcx
 2d0035e:      	shll	$0x5, %eax
 2d00361:      	xorl	%edx, %edx
 2d00363:      	jmp	0x2d00379 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c9>
 2d00365:      	nopw	%cs:(%rax,%rax)
 2d0036f:      	nop
 2d00370:      	addq	$0x20, %rdx
 2d00374:      	cmpq	%rdx, %rax
 2d00377:      	je	0x2d003a2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31f2>
 2d00379:      	movl	(%rcx,%rdx), %esi
 2d0037c:      	movl	%esi, %edi
 2d0037e:      	andl	$0x10000ff, %edi        # imm = 0x10000FF
 2d00384:      	cmpl	$0x1000000, %edi        # imm = 0x1000000
 2d0038a:      	jne	0x2d00370 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d0038c:      	notl	%esi
 2d0038e:      	testl	$0x5000000, %esi        # imm = 0x5000000
 2d00394:      	je	0x2d00370 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d00396:      	cmpl	$0x3, 0x4(%rcx,%rdx)
 2d0039b:      	jne	0x2d00370 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d0039d:      	jmp	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d003a2:      	movl	0x2c(%r12), %eax
 2d003a7:      	testb	$0xc, %al
 2d003a9:      	setne	%cl
 2d003ac:      	testb	$0x4, %al
 2d003ae:      	sete	%dl
 2d003b1:      	movq	0x10(%r12), %rax
 2d003b6:      	movq	0x10(%rax), %rax
 2d003ba:      	testb	%dl, %cl
 2d003bc:      	jne	0x2d0047b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32cb>
 2d003c2:      	testl	$0x480, %eax            # imm = 0x480
 2d003c7:      	je	0x2d0040a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x325a>
 2d003c9:      	jmp	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d003ce:      	movl	$0xfffffffe, %edi       # imm = 0xFFFFFFFE
 2d003d3:      	movl	%r9d, %esi
 2d003d6:      	imull	%edi, %esi
 2d003d9:      	addl	%esi, %edx
 2d003db:      	js	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d003e1:      	addl	$0xffffee6d, %ebx       # imm = 0xFFFFEE6D
 2d003e7:      	cmpl	$0x4, %ebx
 2d003ea:      	ja	0x2d00404 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3254>
 2d003ec:      	movl	$0x15, %esi
 2d003f1:      	btl	%ebx, %esi
 2d003f4:      	jae	0x2d00404 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3254>
 2d003f6:      	movq	0x18(%rsp), %rsi
 2d003fb:      	cmpl	%esi, 0x4(%rax)
 2d003fe:      	je	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d00404:      	movl	%edx, %eax
 2d00406:      	movq	%rax, 0x10(%rcx)
 2d0040a:      	movq	%r12, %r13
 2d0040d:      	movq	%r12, %rdi
 2d00410:      	movq	0x18(%rsp), %r12
 2d00415:      	movl	%r12d, %esi
 2d00418:      	xorl	%edx, %edx
 2d0041a:      	movl	$0x1, %ecx
 2d0041f:      	callq	0x36556b0 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2d00424:      	cmpl	$-0x1, %eax
 2d00427:      	jne	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0042d:      	movq	%r13, %rdi
 2d00430:      	movl	%r12d, %esi
 2d00433:      	xorl	%edx, %edx
 2d00435:      	xorl	%ecx, %ecx
 2d00437:      	xorl	%r8d, %r8d
 2d0043a:      	callq	0x3655bb0 <_ZNK4llvm12MachineInstr25findRegisterDefOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEbb>
 2d0043f:      	cmpl	$-0x1, %eax
 2d00442:      	jne	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d00448:      	testb	$0x4, (%r13)
 2d0044d:      	jne	0x2d002a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d00453:      	nopw	%cs:(%rax,%rax)
 2d0045d:      	nopl	(%rax)
 2d00460:      	testb	$0x8, 0x2c(%r13)
 2d00465:      	je	0x2d002a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d0046b:      	movq	0x8(%r13), %r13
 2d0046f:      	testb	$0x8, 0x2c(%r13)
 2d00474:      	jne	0x2d0046b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32bb>
 2d00476:      	jmp	0x2d002a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d0047b:      	testb	%al, %al
 2d0047d:      	js	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d0047f:      	movq	%r12, %rcx
 2d00482:      	nopw	%cs:(%rax,%rax)
 2d0048c:      	nopl	(%rax)
 2d00490:      	testb	$0x8, 0x2c(%rcx)
 2d00494:      	je	0x2d004a6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32f6>
 2d00496:      	movq	0x8(%rcx), %rcx
 2d0049a:      	movq	0x10(%rcx), %rdx
 2d0049e:      	testb	$-0x80, 0x10(%rdx)
 2d004a2:      	je	0x2d00490 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32e0>
 2d004a4:      	jmp	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d004a6:      	testl	$0x400, %eax            # imm = 0x400
 2d004ab:      	jne	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d004ad:      	movq	%r12, %rax
 2d004b0:      	testb	$0x8, 0x2c(%rax)
 2d004b4:      	je	0x2d0040a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x325a>
 2d004ba:      	movq	0x8(%rax), %rax
 2d004be:      	movq	0x10(%rax), %rcx
 2d004c2:      	testb	$0x4, 0x11(%rcx)
 2d004c6:      	je	0x2d004b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3300>
 2d004c8:      	movq	0xc8(%rsp), %rsi
 2d004d0:      	movq	%rsi, 0xd0(%rsp)
 2d004d8:      	leaq	0xa0(%rsp), %rax
 2d004e0:      	testq	%rsi, %rsi
 2d004e3:      	je	0x2d00527 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3377>
 2d004e5:      	movl	$0x1, %edx
 2d004ea:      	leaq	0xd0(%rsp), %rdi
 2d004f2:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d004f7:      	movq	0xd0(%rsp), %rsi
 2d004ff:      	movq	%rsi, 0xa0(%rsp)
 2d00507:      	testq	%rsi, %rsi
 2d0050a:      	je	0x2d0052e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x337e>
 2d0050c:      	leaq	0xd0(%rsp), %rbx
 2d00514:      	movq	%rbx, %rdi
 2d00517:      	leaq	0xa0(%rsp), %rdx
 2d0051f:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d00524:      	movq	%rbx, %rax
 2d00527:      	movq	$0x0, (%rax)
 2d0052e:      	leaq	0xa8(%rsp), %rax
 2d00536:      	xorps	%xmm0, %xmm0
 2d00539:      	movups	%xmm0, (%rax)
 2d0053c:      	movq	$0x0, 0x10(%rax)
 2d00544:      	movq	(%rsp), %rax
 2d00548:      	movq	0x40(%rax), %rax
 2d0054c:      	movq	0x8(%rax), %rcx
 2d00550:      	movq	$-0x23360, %rax         # imm = 0xFFFDCCA0
 2d00557:      	addq	%rax, %rcx
 2d0055a:      	movq	0x10(%rsp), %rdi
 2d0055f:      	movq	%r12, %rsi
 2d00562:      	leaq	0xa0(%rsp), %r13
 2d0056a:      	movq	%r13, %rdx
 2d0056d:      	movq	0x18(%rsp), %rbx
 2d00572:      	movl	%ebx, %r8d
 2d00575:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d0057a:      	movq	%rax, %r14
 2d0057d:      	movq	%rdx, %rbp
 2d00580:      	movq	$0x0, 0xf8(%rsp)
 2d0058c:      	movl	$0x3, 0xf4(%rsp)
 2d00597:      	leaq	0x100(%rsp), %rax
 2d0059f:      	xorps	%xmm0, %xmm0
 2d005a2:      	movups	%xmm0, (%rax)
 2d005a5:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d005b0:      	movq	%rdx, %rdi
 2d005b3:      	movq	%r14, %rsi
 2d005b6:      	leaq	0xf0(%rsp), %rdx
 2d005be:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d005c3:      	movq	$0x0, 0x38(%rsp)
 2d005cc:      	movl	%ebx, 0x34(%rsp)
 2d005d0:      	jmp	0x2d00772 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x35c2>
 2d005d5:      	movl	$0x3, %r12d
 2d005db:      	xorl	%r14d, %r14d
 2d005de:      	movq	%rcx, %rdx
 2d005e1:      	addl	$0xfffffc56, %ecx       # imm = 0xFFFFFC56
 2d005e7:      	cmpl	$0x7, %ecx
 2d005ea:      	jbe	0x2d0097e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37ce>
 2d005f0:      	leal	-0x7d7(%rdx), %ecx
 2d005f6:      	leaq	-0x19b13f5(%rip), %rdx  # 0x134f208 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x572>
 2d005fd:      	movslq	(%rdx,%rcx,4), %rcx
 2d00601:      	addq	%rdx, %rcx
 2d00604:      	jmpq	*%rcx
 2d00606:      	cmpl	$0x1199, %ebx           # imm = 0x1199
 2d0060c:      	je	0x2cffbca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a1a>
 2d00612:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2d00618:      	je	0x2cffbca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a1a>
 2d0061e:      	movl	$0x1, %ecx
 2d00623:      	movb	$0x1, %al
 2d00625:      	movb	$0x1, %sil
 2d00628:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d0062e:      	jne	0x2cffc69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2d00634:      	jmp	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2d00639:      	movl	$0x66, %edx
 2d0063e:      	btl	%ecx, %edx
 2d00641:      	jb	0x2d00966 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2d00647:      	movl	$0x11, %edx
 2d0064c:      	btl	%ecx, %edx
 2d0064f:      	jb	0x2d0098e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2d00655:      	jmp	0x2cfff2f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d7f>
 2d0065a:      	movq	0x18(%rsp), %r12
 2d0065f:      	movq	0x10(%rsp), %rax
 2d00664:      	cmpl	$0x0, 0x78(%rax)
 2d00668:      	je	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0066e:      	movq	0xc8(%rsp), %rsi
 2d00676:      	movq	%rsi, 0xd0(%rsp)
 2d0067e:      	leaq	0xa0(%rsp), %rax
 2d00686:      	testq	%rsi, %rsi
 2d00689:      	je	0x2d006cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x351d>
 2d0068b:      	movl	$0x1, %edx
 2d00690:      	leaq	0xd0(%rsp), %rdi
 2d00698:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d0069d:      	movq	0xd0(%rsp), %rsi
 2d006a5:      	movq	%rsi, 0xa0(%rsp)
 2d006ad:      	testq	%rsi, %rsi
 2d006b0:      	je	0x2d006d4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3524>
 2d006b2:      	leaq	0xd0(%rsp), %rbx
 2d006ba:      	movq	%rbx, %rdi
 2d006bd:      	leaq	0xa0(%rsp), %rdx
 2d006c5:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d006ca:      	movq	%rbx, %rax
 2d006cd:      	movq	$0x0, (%rax)
 2d006d4:      	leaq	0xa8(%rsp), %rax
 2d006dc:      	xorps	%xmm0, %xmm0
 2d006df:      	movups	%xmm0, (%rax)
 2d006e2:      	movq	$0x0, 0x10(%rax)
 2d006ea:      	movq	(%rsp), %rax
 2d006ee:      	movq	0x40(%rax), %rax
 2d006f2:      	movq	0x8(%rax), %rcx
 2d006f6:      	movq	$-0x23360, %rax         # imm = 0xFFFDCCA0
 2d006fd:      	addq	%rax, %rcx
 2d00700:      	movq	0x10(%rsp), %rdi
 2d00705:      	movq	%r13, %rsi
 2d00708:      	leaq	0xa0(%rsp), %r13
 2d00710:      	movq	%r13, %rdx
 2d00713:      	movl	%r12d, %r8d
 2d00716:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d0071b:      	movq	%rax, %r14
 2d0071e:      	movq	%rdx, %rbp
 2d00721:      	movq	$0x0, 0xf8(%rsp)
 2d0072d:      	movl	$0x3, 0xf4(%rsp)
 2d00738:      	leaq	0x100(%rsp), %rax
 2d00740:      	xorps	%xmm0, %xmm0
 2d00743:      	movups	%xmm0, (%rax)
 2d00746:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d00751:      	movq	%rdx, %rdi
 2d00754:      	movq	%r14, %rsi
 2d00757:      	leaq	0xf0(%rsp), %rdx
 2d0075f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00764:      	movq	$0x0, 0x38(%rsp)
 2d0076d:      	movl	%r12d, 0x34(%rsp)
 2d00772:      	leaq	0x40(%rsp), %rbx
 2d00777:      	xorps	%xmm0, %xmm0
 2d0077a:      	movups	%xmm0, (%rbx)
 2d0077d:      	movl	$0x0, 0x30(%rsp)
 2d00785:      	movq	%rbp, %rdi
 2d00788:      	movq	%r14, %rsi
 2d0078b:      	leaq	0x30(%rsp), %r12
 2d00790:      	movq	%r12, %rdx
 2d00793:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00798:      	movq	0x80(%rsp), %rax
 2d007a0:      	leal	(,%rax,4), %eax
 2d007a7:      	movl	$0x1, 0x30(%rsp)
 2d007af:      	movq	$0x0, 0x38(%rsp)
 2d007b8:      	movq	%rax, 0x40(%rsp)
 2d007bd:      	movq	%rbp, %rdi
 2d007c0:      	movq	%r14, %rsi
 2d007c3:      	movq	%r12, %rdx
 2d007c6:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d007cb:      	movl	0x28(%rsp), %eax
 2d007cf:      	movl	$0x1, 0x30(%rsp)
 2d007d7:      	movq	$0x0, 0x38(%rsp)
 2d007e0:      	movq	%rax, 0x40(%rsp)
 2d007e5:      	movq	%rbp, %rdi
 2d007e8:      	movq	%r14, %rsi
 2d007eb:      	movq	%r12, %rdx
 2d007ee:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d007f3:      	movq	$0x0, 0x38(%rsp)
 2d007fc:      	movq	0x88(%rsp), %rax
 2d00804:      	movl	%eax, 0x34(%rsp)
 2d00808:      	xorps	%xmm0, %xmm0
 2d0080b:      	movups	%xmm0, (%rbx)
 2d0080e:      	movl	$0x0, 0x30(%rsp)
 2d00816:      	movq	%rbp, %rdi
 2d00819:      	movq	%r14, %rsi
 2d0081c:      	movq	%r12, %rdx
 2d0081f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00824:      	movq	0xa0(%rsp), %rsi
 2d0082c:      	testq	%rsi, %rsi
 2d0082f:      	je	0x2d00839 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3689>
 2d00831:      	movq	%r13, %rdi
 2d00834:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00839:      	movq	0xd0(%rsp), %rsi
 2d00841:      	testq	%rsi, %rsi
 2d00844:      	je	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d00846:      	leaq	0xd0(%rsp), %rdi
 2d0084e:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00853:      	leaq	0x40(%rsp), %rbx
 2d00858:      	leaq	0x30(%rsp), %r13
 2d0085d:      	movq	0x70(%rsp), %r14
 2d00862:      	movl	0x28(%rsp), %eax
 2d00866:      	movl	$0x1, 0x30(%rsp)
 2d0086e:      	movq	$0x0, 0x38(%rsp)
 2d00877:      	movq	%rax, 0x40(%rsp)
 2d0087c:      	movq	%r15, %rdi
 2d0087f:      	movq	%r14, %rsi
 2d00882:      	movq	%r13, %rdx
 2d00885:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d0088a:      	movq	$0x0, 0x38(%rsp)
 2d00893:      	movq	0x88(%rsp), %rax
 2d0089b:      	movl	%eax, 0x34(%rsp)
 2d0089f:      	xorps	%xmm0, %xmm0
 2d008a2:      	movups	%xmm0, (%rbx)
 2d008a5:      	movl	$0x0, 0x30(%rsp)
 2d008ad:      	movq	%r15, %rdi
 2d008b0:      	movq	%r14, %rsi
 2d008b3:      	movq	%r13, %rdx
 2d008b6:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d008bb:      	movq	0x80(%rsp), %rax
 2d008c3:      	testq	%rax, %rax
 2d008c6:      	movq	%r14, %rsi
 2d008c9:      	movq	0x180(%rsp), %r12
 2d008d1:      	movq	%r15, %r14
 2d008d4:      	je	0x2d00945 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3795>
 2d008d6:      	movq	%r13, %rdx
 2d008d9:      	movzbl	0xc0(%rsp), %ecx
 2d008e1:      	orb	0x8(%rsp), %cl
 2d008e5:      	leaq	(%r12,%rax,8), %rax
 2d008e9:      	movq	%rax, 0x18(%rsp)
 2d008ee:      	movzbl	%cl, %ebp
 2d008f1:      	shll	$0x18, %ebp
 2d008f4:      	nopw	%cs:(%rax,%rax)
 2d008fe:      	nop
 2d00900:      	movl	(%r12), %eax
 2d00904:      	movzbl	0x4(%r12), %ecx
 2d0090a:      	movq	$0x0, 0x38(%rsp)
 2d00913:      	shll	$0x1a, %ecx
 2d00916:      	orl	%ebp, %ecx
 2d00918:      	movl	%eax, 0x34(%rsp)
 2d0091c:      	xorps	%xmm0, %xmm0
 2d0091f:      	movups	%xmm0, (%rbx)
 2d00922:      	movl	%ecx, 0x30(%rsp)
 2d00926:      	movq	%r14, %rdi
 2d00929:      	movq	%rsi, %r13
 2d0092c:      	movq	%rdx, %r15
 2d0092f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00934:      	movq	%r15, %rdx
 2d00937:      	movq	%r13, %rsi
 2d0093a:      	addq	$0x8, %r12
 2d0093e:      	cmpq	0x18(%rsp), %r12
 2d00943:      	jne	0x2d00900 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3750>
 2d00945:      	movq	%r14, %rdi
 2d00948:      	movq	0x230(%rsp), %rdx
 2d00950:      	movq	0x228(%rsp), %rcx
 2d00958:      	jmp	0x2cff285 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x20d5>
 2d0095d:      	addl	$0xffffef09, %ecx       # imm = 0xFFFFEF09
 2d00963:      	cmpl	$0x2, %ecx
 2d00966:      	movl	$0x4, %esi
 2d0096b:      	addl	0x10(%rsp), %eax
 2d0096f:      	je	0x2d009ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383d>
 2d00971:      	movl	$0x1, %r12d
 2d00977:      	movb	$0x1, %r14b
 2d0097a:      	xorl	%ebx, %ebx
 2d0097c:      	jmp	0x2d00997 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37e7>
 2d0097e:      	leaq	-0x19b179d(%rip), %rdx  # 0x134f1e8 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x552>
 2d00985:      	movslq	(%rdx,%rcx,4), %rcx
 2d00989:      	addq	%rdx, %rcx
 2d0098c:      	jmpq	*%rcx
 2d0098e:      	movl	$0x4, %r12d
 2d00994:      	xorl	%r14d, %r14d
 2d00997:      	movq	(%rsp), %rax
 2d0099b:      	movq	0x48(%rax), %r9
 2d0099f:      	movq	%r13, %rdi
 2d009a2:      	movl	0x90(%rsp), %esi
 2d009a9:      	movl	0x8(%rsp), %edx
 2d009ad:      	movl	0x78(%rsp), %ecx
 2d009b1:      	leaq	0x1c0(%rsp), %r8
 2d009b9:      	callq	0x2d05100 <_ZL15findIncDecAfterN4llvm26MachineInstrBundleIteratorINS_12MachineInstrELb0EEENS_8RegisterENS_5ARMCC9CondCodesES3_RiPKNS_18TargetRegisterInfoE>
 2d009be:      	movq	%rax, %rbp
 2d009c1:      	movl	0x1c0(%rsp), %eax
 2d009c8:      	testb	%r14b, %r14b
 2d009cb:      	je	0x2d009d8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3828>
 2d009cd:      	cmpl	0x10(%rsp), %eax
 2d009d1:      	jne	0x2d009d8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3828>
 2d009d3:      	xorps	%xmm0, %xmm0
 2d009d6:      	jmp	0x2d009ea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383a>
 2d009d8:      	addl	0x10(%rsp), %eax
 2d009dc:      	sete	%al
 2d009df:      	testb	%al, %bl
 2d009e1:      	xorps	%xmm0, %xmm0
 2d009e4:      	je	0x2d00c96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ae6>
 2d009ea:      	movl	%r12d, %esi
 2d009ed:      	cmpq	%r15, %rbp
 2d009f0:      	je	0x2d00cf4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b44>
 2d009f6:      	testb	$0x4, (%rbp)
 2d009fa:      	movq	%rbp, %rax
 2d009fd:      	leaq	0x30(%rsp), %rdx
 2d00a02:      	movq	0x20(%rsp), %rcx
 2d00a07:      	jne	0x2d00a2a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x387a>
 2d00a09:      	testb	$0x8, 0x2c(%rbp)
 2d00a0d:      	movq	%rbp, %rax
 2d00a10:      	je	0x2d00a2a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x387a>
 2d00a12:      	movq	%rbp, %rax
 2d00a15:      	nopw	%cs:(%rax,%rax)
 2d00a1f:      	nop
 2d00a20:      	movq	0x8(%rax), %rax
 2d00a24:      	testb	$0x8, 0x2c(%rax)
 2d00a28:      	jne	0x2d00a20 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3870>
 2d00a2a:      	movq	0x8(%rax), %rax
 2d00a2e:      	movq	%rax, 0x10(%rsp)
 2d00a33:      	cmpq	%rax, %rbp
 2d00a36:      	je	0x2d00c36 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a86>
 2d00a3c:      	movl	%esi, 0x88(%rsp)
 2d00a43:      	jmp	0x2d00a8b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38db>
 2d00a45:      	nopw	%cs:(%rax,%rax)
 2d00a4f:      	nop
 2d00a50:      	movl	%ecx, 0xf0(%r13)
 2d00a57:      	movq	(%r14), %rax
 2d00a5a:      	movq	(%rax,%r15,8), %rcx
 2d00a5e:      	movq	%rcx, (%r12)
 2d00a62:      	movq	%r12, (%rax,%r15,8)
 2d00a66:      	movq	0xe0(%r13), %rax
 2d00a6d:      	movq	%rax, (%rbp)
 2d00a71:      	movq	%rbp, 0xe0(%r13)
 2d00a78:      	movq	%rbx, %rbp
 2d00a7b:      	cmpq	0x10(%rsp), %rbx
 2d00a80:      	movq	0x28(%rsp), %r13
 2d00a85:      	je	0x2d00c25 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a75>
 2d00a8b:      	movq	0x8(%rbp), %rbx
 2d00a8f:      	movq	0x18(%rbp), %rax
 2d00a93:      	movq	0x20(%rax), %r14
 2d00a97:      	testq	%r14, %r14
 2d00a9a:      	je	0x2d00b50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00aa0:      	movq	0x288(%r14), %rdi
 2d00aa7:      	testq	%rdi, %rdi
 2d00aaa:      	je	0x2d00ab8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3908>
 2d00aac:      	movq	(%rdi), %rax
 2d00aaf:      	movq	%rbp, %rsi
 2d00ab2:      	callq	*0x20(%rax)
 2d00ab5:      	xorps	%xmm0, %xmm0
 2d00ab8:      	movzwl	0x28(%rbp), %ecx
 2d00abc:      	movzbl	0x2a(%rbp), %eax
 2d00ac0:      	shll	$0x10, %eax
 2d00ac3:      	orl	%ecx, %eax
 2d00ac5:      	testl	%eax, %eax
 2d00ac7:      	je	0x2d00b50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00acd:      	movq	0x20(%rbp), %rcx
 2d00ad1:      	shll	$0x5, %eax
 2d00ad4:      	movq	0x20(%r14), %rdx
 2d00ad8:      	jmp	0x2d00b01 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3951>
 2d00ada:      	nopw	(%rax,%rax)
 2d00ae0:      	movq	%rdi, 0x18(%r8)
 2d00ae4:      	leaq	0x10(%rcx), %r9
 2d00ae8:      	testq	%rdi, %rdi
 2d00aeb:      	cmovneq	%rdi, %rsi
 2d00aef:      	movq	%r8, 0x10(%rsi)
 2d00af3:      	movups	%xmm0, (%r9)
 2d00af7:      	addq	$0x20, %rcx
 2d00afb:      	addq	$-0x20, %rax
 2d00aff:      	je	0x2d00b50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00b01:      	cmpb	$0x0, (%rcx)
 2d00b04:      	jne	0x2d00af7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3947>
 2d00b06:      	movl	0x4(%rcx), %esi
 2d00b09:      	movl	%esi, %edi
 2d00b0b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2d00b11:      	shlq	$0x4, %rdi
 2d00b15:      	movq	%rsi, %r8
 2d00b18:      	shlq	$0x3, %r8
 2d00b1c:      	addq	0x128(%rdx), %r8
 2d00b23:      	testl	%esi, %esi
 2d00b25:      	movq	0x30(%rdx), %rsi
 2d00b29:      	leaq	0x8(%rsi,%rdi), %r9
 2d00b2e:      	cmovnsq	%r8, %r9
 2d00b32:      	movq	(%r9), %rsi
 2d00b35:      	movq	0x18(%rcx), %rdi
 2d00b39:      	movq	0x10(%rcx), %r8
 2d00b3d:      	cmpq	%rsi, %rcx
 2d00b40:      	jne	0x2d00ae0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3930>
 2d00b42:      	movq	%rdi, (%r9)
 2d00b45:      	jmp	0x2d00ae4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3934>
 2d00b47:      	nopw	(%rax,%rax)
 2d00b50:      	movq	$0x0, 0x18(%rbp)
 2d00b58:      	movq	(%rbp), %rax
 2d00b5c:      	movq	0x8(%rbp), %rcx
 2d00b60:      	andq	$-0x8, %rax
 2d00b64:      	movq	(%rcx), %rdx
 2d00b67:      	andl	$0x7, %edx
 2d00b6a:      	orq	%rax, %rdx
 2d00b6d:      	movq	%rdx, (%rcx)
 2d00b70:      	movq	%rcx, 0x8(%rax)
 2d00b74:      	andq	$0x7, (%rbp)
 2d00b79:      	movq	$0x0, 0x8(%rbp)
 2d00b81:      	movq	0x18(%rsp), %rax
 2d00b86:      	movq	0x28(%rax), %rax
 2d00b8a:      	movq	0x20(%rax), %r13
 2d00b8e:      	movq	0x20(%rbp), %r12
 2d00b92:      	testq	%r12, %r12
 2d00b95:      	je	0x2d00a66 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38b6>
 2d00b9b:      	movzbl	0x2b(%rbp), %r15d
 2d00ba0:      	leaq	0xe8(%r13), %r14
 2d00ba7:      	movl	0xf0(%r13), %eax
 2d00bae:      	cmpl	%r15d, %eax
 2d00bb1:      	ja	0x2d00a57 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a7>
 2d00bb7:      	leaq	0x1(%r15), %rcx
 2d00bbb:      	cmpl	%r15d, 0xf4(%r13)
 2d00bc2:      	ja	0x2d00bea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a3a>
 2d00bc4:      	leaq	0xf8(%r13), %rsi
 2d00bcb:      	movl	$0x8, %ecx
 2d00bd0:      	movq	%r14, %rdi
 2d00bd3:      	leaq	0x1(%r15), %rdx
 2d00bd7:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d00bdc:      	leaq	0x1(%r15), %rcx
 2d00be0:      	xorps	%xmm0, %xmm0
 2d00be3:      	movl	0xf0(%r13), %eax
 2d00bea:      	cmpl	%eax, %ecx
 2d00bec:      	je	0x2d00a50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a0>
 2d00bf2:      	movl	%eax, %eax
 2d00bf4:      	leaq	(,%rax,8), %rdi
 2d00bfc:      	addq	(%r14), %rdi
 2d00bff:      	movq	%rcx, %r14
 2d00c02:      	movq	%rcx, %rdx
 2d00c05:      	subq	%rax, %rdx
 2d00c08:      	shlq	$0x3, %rdx
 2d00c0c:      	xorl	%esi, %esi
 2d00c0e:      	callq	0x828ab90 <memset@plt>
 2d00c13:      	movq	%r14, %rcx
 2d00c16:      	leaq	0xe8(%r13), %r14
 2d00c1d:      	xorps	%xmm0, %xmm0
 2d00c20:      	jmp	0x2d00a50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a0>
 2d00c25:      	leaq	0x30(%rsp), %rdx
 2d00c2a:      	movq	0x20(%rsp), %rcx
 2d00c2f:      	movl	0x88(%rsp), %esi
 2d00c36:      	cmpl	$0xb4a, %ecx            # imm = 0xB4A
 2d00c3c:      	jg	0x2d00d0a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b5a>
 2d00c42:      	leal	-0x3aa(%rcx), %eax
 2d00c48:      	cmpl	$0x6, %eax
 2d00c4b:      	jbe	0x2d00c74 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ac4>
 2d00c4d:      	addl	$0xfffff829, %ecx       # imm = 0xFFFFF829
 2d00c53:      	movl	$0x55, %eax
 2d00c58:      	btl	%ecx, %eax
 2d00c5b:      	jae	0x2d02342 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5192>
 2d00c61:      	movl	%esi, %eax
 2d00c63:      	leaq	-0x1e72f3a(%rip), %rcx  # 0xe8dd30 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.152>
 2d00c6a:      	movq	-0x8(%rcx,%rax,8), %r14
 2d00c6f:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00c74:      	movl	$0x55, %ecx
 2d00c79:      	btl	%eax, %ecx
 2d00c7c:      	movq	0x20(%rsp), %rcx
 2d00c81:      	jae	0x2d00c4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a9d>
 2d00c83:      	movl	%esi, %eax
 2d00c85:      	leaq	-0x1e7383c(%rip), %rcx  # 0xe8d450 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.151>
 2d00c8c:      	movq	-0x8(%rcx,%rax,8), %r14
 2d00c91:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00c96:      	movl	0x98(%rsp), %edi
 2d00c9d:      	testl	%edi, %edi
 2d00c9f:      	je	0x2d0102b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00ca5:      	movq	(%rsp), %rax
 2d00ca9:      	movq	0x50(%rax), %rax
 2d00cad:      	cmpb	$0x0, 0x208(%rax)
 2d00cb4:      	je	0x2d0102b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00cba:      	movl	%r12d, %esi
 2d00cbd:      	movzwl	0x28(%r13), %ecx
 2d00cc2:      	movzbl	0x2a(%r13), %eax
 2d00cc7:      	shll	$0x10, %eax
 2d00cca:      	orl	%ecx, %eax
 2d00ccc:      	cmpl	$0x2, %eax
 2d00ccf:      	je	0x2d00cf4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b44>
 2d00cd1:      	movq	0x20(%r13), %rcx
 2d00cd5:      	shll	$0x5, %eax
 2d00cd8:      	addq	$-0x40, %rax
 2d00cdc:      	xorl	%edx, %edx
 2d00cde:      	nop
 2d00ce0:      	cmpl	$0x52, 0x44(%rcx,%rdx)
 2d00ce5:      	jae	0x2d0102b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00ceb:      	addq	$0x20, %rdx
 2d00cef:      	cmpq	%rdx, %rax
 2d00cf2:      	jne	0x2d00ce0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b30>
 2d00cf4:      	leaq	0x30(%rsp), %rdx
 2d00cf9:      	movq	0x20(%rsp), %rcx
 2d00cfe:      	cmpl	$0xb4a, %ecx            # imm = 0xB4A
 2d00d04:      	jle	0x2d00c42 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a92>
 2d00d0a:      	cmpl	$0x1021, %ecx           # imm = 0x1021
 2d00d10:      	jg	0x2d00d38 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b88>
 2d00d12:      	cmpl	$0xf27, %ecx            # imm = 0xF27
 2d00d18:      	jg	0x2d00d52 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ba2>
 2d00d1a:      	xorl	%r14d, %r14d
 2d00d1d:      	cmpl	$0xb4b, %ecx            # imm = 0xB4B
 2d00d23:      	jne	0x2d00d8e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bde>
 2d00d25:      	cmpl	$0x1, %esi
 2d00d28:      	setne	%r14b
 2d00d2c:      	addl	%r14d, %r14d
 2d00d2f:      	orq	$-0xb4c, %r14           # imm = 0xF4B4
 2d00d36:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00d38:      	cmpl	$0x10f4, %ecx           # imm = 0x10F4
 2d00d3e:      	jg	0x2d00d6c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bbc>
 2d00d40:      	xorl	%eax, %eax
 2d00d42:      	cmpl	$0x1, %esi
 2d00d45:      	setne	%al
 2d00d48:      	leaq	-0x1025(%rax,%rax), %r14
 2d00d50:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00d52:      	xorl	%eax, %eax
 2d00d54:      	cmpl	$0xf28, %ecx            # imm = 0xF28
 2d00d5a:      	jne	0x2d00da1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bf1>
 2d00d5c:      	cmpl	$0x1, %esi
 2d00d5f:      	setne	%al
 2d00d62:      	leaq	-0xf29(%rax,%rax), %r14
 2d00d6a:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00d6c:      	xorl	%r14d, %r14d
 2d00d6f:      	cmpl	$0x1, %esi
 2d00d72:      	setne	%r14b
 2d00d76:      	addl	%r14d, %r14d
 2d00d79:      	orq	$-0x10f8, %r14          # imm = 0xEF08
 2d00d80:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00d82:      	xorl	%r10d, %r10d
 2d00d85:      	movb	$0x1, %cl
 2d00d87:      	movb	$0x1, %dl
 2d00d89:      	jmp	0x2cffb48 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2998>
 2d00d8e:      	cmpl	$0x1, %esi
 2d00d91:      	setne	%r14b
 2d00d95:      	addl	%r14d, %r14d
 2d00d98:      	orq	$-0xb50, %r14           # imm = 0xF4B0
 2d00d9f:      	jmp	0x2d00daf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00da1:      	cmpl	$0x1, %esi
 2d00da4:      	setne	%al
 2d00da7:      	leaq	-0xf2d(%rax,%rax), %r14
 2d00daf:      	movq	0xa0(%rsp), %rsi
 2d00db7:      	movq	%rsi, 0xf0(%rsp)
 2d00dbf:      	movq	%rdx, %rbx
 2d00dc2:      	testq	%rsi, %rsi
 2d00dc5:      	je	0x2d00e05 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c55>
 2d00dc7:      	movl	$0x1, %edx
 2d00dcc:      	leaq	0xf0(%rsp), %rdi
 2d00dd4:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d00dd9:      	leaq	0x30(%rsp), %rdx
 2d00dde:      	movq	0xf0(%rsp), %rsi
 2d00de6:      	movq	%rsi, 0x30(%rsp)
 2d00deb:      	testq	%rsi, %rsi
 2d00dee:      	je	0x2d00e0c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c5c>
 2d00df0:      	leaq	0xf0(%rsp), %rbx
 2d00df8:      	movq	%rbx, %rdi
 2d00dfb:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d00e00:      	leaq	0x30(%rsp), %rdx
 2d00e05:      	movq	$0x0, (%rbx)
 2d00e0c:      	leaq	0x40(%rsp), %rax
 2d00e11:      	xorps	%xmm0, %xmm0
 2d00e14:      	movups	%xmm0, -0x8(%rax)
 2d00e18:      	movq	$0x0, 0x8(%rax)
 2d00e20:      	movq	(%rsp), %rax
 2d00e24:      	movq	0x40(%rax), %rax
 2d00e28:      	shlq	$0x5, %r14
 2d00e2c:      	addq	0x8(%rax), %r14
 2d00e30:      	movq	0x18(%rsp), %rdi
 2d00e35:      	movq	%r13, %rsi
 2d00e38:      	movq	%rdx, %r12
 2d00e3b:      	movq	%r14, %rcx
 2d00e3e:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d00e43:      	movq	%rax, %r14
 2d00e46:      	movq	%rdx, %r15
 2d00e49:      	movq	$0x0, 0x138(%rsp)
 2d00e55:      	movl	0x90(%rsp), %ebp
 2d00e5c:      	movl	%ebp, 0x134(%rsp)
 2d00e63:      	leaq	0x140(%rsp), %rbx
 2d00e6b:      	xorps	%xmm0, %xmm0
 2d00e6e:      	movups	%xmm0, (%rbx)
 2d00e71:      	movl	$0x1000000, 0x130(%rsp) # imm = 0x1000000
 2d00e7c:      	movq	%rdx, %rdi
 2d00e7f:      	movq	%rax, %rsi
 2d00e82:      	leaq	0x130(%rsp), %r13
 2d00e8a:      	movq	%r13, %rdx
 2d00e8d:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00e92:      	movq	$0x0, 0x138(%rsp)
 2d00e9e:      	movl	0x98(%rsp), %eax
 2d00ea5:      	shll	$0x1a, %eax
 2d00ea8:      	movl	%ebp, 0x134(%rsp)
 2d00eaf:      	xorps	%xmm0, %xmm0
 2d00eb2:      	movups	%xmm0, (%rbx)
 2d00eb5:      	movl	%eax, 0x130(%rsp)
 2d00ebc:      	movq	%r15, %rdi
 2d00ebf:      	movq	%r14, %rsi
 2d00ec2:      	movq	%r13, %rdx
 2d00ec5:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00eca:      	movl	0x8(%rsp), %eax
 2d00ece:      	movl	$0x1, 0x130(%rsp)
 2d00ed9:      	movq	$0x0, 0x138(%rsp)
 2d00ee5:      	movq	%rax, 0x140(%rsp)
 2d00eed:      	movq	%r15, %rdi
 2d00ef0:      	movq	%r14, %rsi
 2d00ef3:      	movq	%r13, %rdx
 2d00ef6:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00efb:      	movq	$0x0, 0x138(%rsp)
 2d00f07:      	movl	0x78(%rsp), %eax
 2d00f0b:      	movl	%eax, 0x134(%rsp)
 2d00f12:      	xorps	%xmm0, %xmm0
 2d00f15:      	movups	%xmm0, (%rbx)
 2d00f18:      	movl	$0x0, 0x130(%rsp)
 2d00f23:      	movq	%r15, %rdi
 2d00f26:      	movq	%r14, %rsi
 2d00f29:      	movq	%r13, %rdx
 2d00f2c:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00f31:      	movq	0x30(%rsp), %rsi
 2d00f36:      	testq	%rsi, %rsi
 2d00f39:      	je	0x2d00f43 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3d93>
 2d00f3b:      	movq	%r12, %rdi
 2d00f3e:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00f43:      	movq	0xf0(%rsp), %rsi
 2d00f4b:      	testq	%rsi, %rsi
 2d00f4e:      	je	0x2d00f5d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3dad>
 2d00f50:      	leaq	0xf0(%rsp), %rdi
 2d00f58:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00f5d:      	movq	0x28(%rsp), %rcx
 2d00f62:      	movzwl	0x28(%rcx), %eax
 2d00f66:      	movzbl	0x2a(%rcx), %ebx
 2d00f6a:      	shll	$0x10, %ebx
 2d00f6d:      	orl	%eax, %ebx
 2d00f6f:      	cmpl	$0x3, %ebx
 2d00f72:      	je	0x2d00fa8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3df8>
 2d00f74:      	movq	0x28(%rsp), %rax
 2d00f79:      	movq	0x20(%rax), %r13
 2d00f7d:      	shll	$0x5, %ebx
 2d00f80:      	addq	$0x60, %r13
 2d00f84:      	addq	$-0x60, %rbx
 2d00f88:      	nopl	(%rax,%rax)
 2d00f90:      	movq	%r15, %rdi
 2d00f93:      	movq	%r14, %rsi
 2d00f96:      	movq	%r13, %rdx
 2d00f99:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00f9e:      	addq	$0x20, %r13
 2d00fa2:      	addq	$-0x20, %rbx
 2d00fa6:      	jne	0x2d00f90 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3de0>
 2d00fa8:      	movq	0x28(%rsp), %r12
 2d00fad:      	movq	0x30(%r12), %rax
 2d00fb2:      	cmpq	$0x8, %rax
 2d00fb6:      	jb	0x2d00fdb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2b>
 2d00fb8:      	movl	%eax, %ecx
 2d00fba:      	andl	$0x7, %ecx
 2d00fbd:      	cmpq	$0x3, %rcx
 2d00fc1:      	je	0x2d01230 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4080>
 2d00fc7:      	testq	%rcx, %rcx
 2d00fca:      	jne	0x2d00fdb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2b>
 2d00fcc:      	leaq	0x30(%r12), %rdx
 2d00fd1:      	movq	%rax, (%rdx)
 2d00fd4:      	movl	$0x1, %ecx
 2d00fd9:      	jmp	0x2d00fdf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2f>
 2d00fdb:      	xorl	%edx, %edx
 2d00fdd:      	xorl	%ecx, %ecx
 2d00fdf:      	movq	%r15, %rdi
 2d00fe2:      	movq	%r14, %rsi
 2d00fe5:      	callq	0x36518d0 <_ZN4llvm12MachineInstr10setMemRefsERNS_15MachineFunctionENS_8ArrayRefIPNS_17MachineMemOperandEEE>
 2d00fea:      	testb	$0x4, (%r12)
 2d00fef:      	movq	%r12, %rax
 2d00ff2:      	jne	0x2d0101a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e6a>
 2d00ff4:      	testb	$0x8, 0x2c(%r12)
 2d00ffa:      	movq	%r12, %rax
 2d00ffd:      	je	0x2d0101a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e6a>
 2d00fff:      	movq	%r12, %rax
 2d01002:      	nopw	%cs:(%rax,%rax)
 2d0100c:      	nopl	(%rax)
 2d01010:      	movq	0x8(%rax), %rax
 2d01014:      	testb	$0x8, 0x2c(%rax)
 2d01018:      	jne	0x2d01010 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e60>
 2d0101a:      	movq	0x8(%rax), %rax
 2d0101e:      	movq	%rax, 0x10(%rsp)
 2d01023:      	cmpq	%rax, %r12
 2d01026:      	xorps	%xmm0, %xmm0
 2d01029:      	jne	0x2d01085 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ed5>
 2d0102b:      	movq	0xa0(%rsp), %rsi
 2d01033:      	testq	%rsi, %rsi
 2d01036:      	je	0x2cff9e9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2839>
 2d0103c:      	leaq	0xa0(%rsp), %rdi
 2d01044:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01049:      	jmp	0x2cff9e9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2839>
 2d0104e:      	nop
 2d01050:      	movl	%ecx, 0xf0(%r13)
 2d01057:      	movq	(%r14), %rax
 2d0105a:      	movq	(%rax,%r12,8), %rcx
 2d0105e:      	movq	%rcx, (%rbp)
 2d01062:      	movq	%rbp, (%rax,%r12,8)
 2d01066:      	movq	%r15, %r12
 2d01069:      	movq	0xe0(%r13), %rax
 2d01070:      	movq	%rax, (%r12)
 2d01074:      	movq	%r12, 0xe0(%r13)
 2d0107b:      	movq	%rbx, %r12
 2d0107e:      	cmpq	0x10(%rsp), %rbx
 2d01083:      	je	0x2d0102b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d01085:      	movq	0x8(%r12), %rbx
 2d0108a:      	movq	0x18(%r12), %rax
 2d0108f:      	movq	0x20(%rax), %r14
 2d01093:      	testq	%r14, %r14
 2d01096:      	je	0x2d01150 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d0109c:      	movq	0x288(%r14), %rdi
 2d010a3:      	testq	%rdi, %rdi
 2d010a6:      	je	0x2d010b4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f04>
 2d010a8:      	movq	(%rdi), %rax
 2d010ab:      	movq	%r12, %rsi
 2d010ae:      	callq	*0x20(%rax)
 2d010b1:      	xorps	%xmm0, %xmm0
 2d010b4:      	movzwl	0x28(%r12), %ecx
 2d010ba:      	movzbl	0x2a(%r12), %eax
 2d010c0:      	shll	$0x10, %eax
 2d010c3:      	orl	%ecx, %eax
 2d010c5:      	testl	%eax, %eax
 2d010c7:      	je	0x2d01150 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d010cd:      	movq	0x20(%r12), %rcx
 2d010d2:      	shll	$0x5, %eax
 2d010d5:      	movq	0x20(%r14), %rdx
 2d010d9:      	jmp	0x2d01101 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f51>
 2d010db:      	nopl	(%rax,%rax)
 2d010e0:      	movq	%rdi, 0x18(%r8)
 2d010e4:      	leaq	0x10(%rcx), %r9
 2d010e8:      	testq	%rdi, %rdi
 2d010eb:      	cmovneq	%rdi, %rsi
 2d010ef:      	movq	%r8, 0x10(%rsi)
 2d010f3:      	movups	%xmm0, (%r9)
 2d010f7:      	addq	$0x20, %rcx
 2d010fb:      	addq	$-0x20, %rax
 2d010ff:      	je	0x2d01150 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d01101:      	cmpb	$0x0, (%rcx)
 2d01104:      	jne	0x2d010f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f47>
 2d01106:      	movl	0x4(%rcx), %esi
 2d01109:      	movl	%esi, %edi
 2d0110b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2d01111:      	shlq	$0x4, %rdi
 2d01115:      	movq	%rsi, %r8
 2d01118:      	shlq	$0x3, %r8
 2d0111c:      	addq	0x128(%rdx), %r8
 2d01123:      	testl	%esi, %esi
 2d01125:      	movq	0x30(%rdx), %rsi
 2d01129:      	leaq	0x8(%rsi,%rdi), %r9
 2d0112e:      	cmovnsq	%r8, %r9
 2d01132:      	movq	(%r9), %rsi
 2d01135:      	movq	0x18(%rcx), %rdi
 2d01139:      	movq	0x10(%rcx), %r8
 2d0113d:      	cmpq	%rsi, %rcx
 2d01140:      	jne	0x2d010e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f30>
 2d01142:      	movq	%rdi, (%r9)
 2d01145:      	jmp	0x2d010e4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f34>
 2d01147:      	nopw	(%rax,%rax)
 2d01150:      	movq	$0x0, 0x18(%r12)
 2d01159:      	movq	(%r12), %rax
 2d0115d:      	movq	0x8(%r12), %rcx
 2d01162:      	andq	$-0x8, %rax
 2d01166:      	movq	(%rcx), %rdx
 2d01169:      	andl	$0x7, %edx
 2d0116c:      	orq	%rax, %rdx
 2d0116f:      	movq	%rdx, (%rcx)
 2d01172:      	movq	%rcx, 0x8(%rax)
 2d01176:      	andq	$0x7, (%r12)
 2d0117b:      	movq	$0x0, 0x8(%r12)
 2d01184:      	movq	0x18(%rsp), %rax
 2d01189:      	movq	0x28(%rax), %rax
 2d0118d:      	movq	0x20(%rax), %r13
 2d01191:      	movq	0x20(%r12), %rbp
 2d01196:      	testq	%rbp, %rbp
 2d01199:      	je	0x2d01069 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3eb9>
 2d0119f:      	movq	%r12, %r15
 2d011a2:      	movzbl	0x2b(%r12), %r12d
 2d011a8:      	leaq	0xe8(%r13), %r14
 2d011af:      	movl	0xf0(%r13), %eax
 2d011b6:      	cmpl	%r12d, %eax
 2d011b9:      	ja	0x2d01057 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea7>
 2d011bf:      	leaq	0x1(%r12), %rcx
 2d011c4:      	cmpl	%r12d, 0xf4(%r13)
 2d011cb:      	ja	0x2d011f5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4045>
 2d011cd:      	leaq	0xf8(%r13), %rsi
 2d011d4:      	movl	$0x8, %ecx
 2d011d9:      	movq	%r14, %rdi
 2d011dc:      	leaq	0x1(%r12), %rdx
 2d011e1:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d011e6:      	leaq	0x1(%r12), %rcx
 2d011eb:      	xorps	%xmm0, %xmm0
 2d011ee:      	movl	0xf0(%r13), %eax
 2d011f5:      	cmpl	%eax, %ecx
 2d011f7:      	je	0x2d01050 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea0>
 2d011fd:      	movl	%eax, %eax
 2d011ff:      	leaq	(,%rax,8), %rdi
 2d01207:      	addq	(%r14), %rdi
 2d0120a:      	movq	%rcx, %r14
 2d0120d:      	movq	%rcx, %rdx
 2d01210:      	subq	%rax, %rdx
 2d01213:      	shlq	$0x3, %rdx
 2d01217:      	xorl	%esi, %esi
 2d01219:      	callq	0x828ab90 <memset@plt>
 2d0121e:      	movq	%r14, %rcx
 2d01221:      	leaq	0xe8(%r13), %r14
 2d01228:      	xorps	%xmm0, %xmm0
 2d0122b:      	jmp	0x2d01050 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea0>
 2d01230:      	andq	$-0x8, %rax
 2d01234:      	movslq	(%rax), %rcx
 2d01237:      	addq	$0x10, %rax
 2d0123b:      	movq	%rax, %rdx
 2d0123e:      	jmp	0x2d00fdf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2f>
 2d01243:      	movl	$0x3, %esi
 2d01248:      	addl	0x10(%rsp), %eax
 2d0124c:      	je	0x2d009ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383d>
 2d01252:      	movl	$0x2, %r12d
 2d01258:      	jmp	0x2d00977 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37c7>
 2d0125d:      	negl	%r8d
 2d01260:      	leal	0x1113(,%rax,4), %esi
 2d01267:      	jmp	0x2d01685 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d5>
 2d0126c:      	movq	(%rsp), %rcx
 2d01270:      	cmpb	$0x1, 0x200(%rcx)
 2d01277:      	movl	%r10d, 0xdc(%rsp)
 2d0127f:      	movq	%r9, 0x80(%rsp)
 2d01287:      	jne	0x2d01295 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40e5>
 2d01289:      	movq	0x1f8(%rcx), %rax
 2d01290:      	jmp	0x2d013bf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x420f>
 2d01295:      	movq	0x48(%rcx), %r12
 2d01299:      	movq	%r12, 0x68(%rcx)
 2d0129d:      	movl	0x78(%rcx), %ebx
 2d012a0:      	testq	%rbx, %rbx
 2d012a3:      	je	0x2d012c3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4113>
 2d012a5:      	leaq	(,%rbx,8), %rdx
 2d012ad:      	movq	0xe0(%rsp), %rax
 2d012b5:      	movq	(%rax), %rdi
 2d012b8:      	xorl	%esi, %esi
 2d012ba:      	callq	0x828ab90 <memset@plt>
 2d012bf:      	movq	(%rsp), %rcx
 2d012c3:      	movl	0x2c(%r12), %ebp
 2d012c8:      	movl	0xb0(%rcx), %ecx
 2d012ce:      	andq	$0x3f, %rcx
 2d012d2:      	je	0x2d012f1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4141>
 2d012d4:      	movq	$-0x1, %rax
 2d012db:      	shlq	%cl, %rax
 2d012de:      	notq	%rax
 2d012e1:      	movq	0xe0(%rsp), %rcx
 2d012e9:      	movq	(%rcx), %rcx
 2d012ec:      	andq	%rax, -0x8(%rcx,%rbx,8)
 2d012f1:      	movq	(%rsp), %rax
 2d012f5:      	movl	%ebp, 0xb0(%rax)
 2d012fb:      	leal	0x3f(%rbp), %edx
 2d012fe:      	shrl	$0x6, %edx
 2d01301:      	cmpl	%ebx, %edx
 2d01303:      	je	0x2d01348 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4198>
 2d01305:      	jb	0x2d01343 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4193>
 2d01307:      	movq	%rbx, %rdi
 2d0130a:      	movl	%ebx, %r12d
 2d0130d:      	cmpl	0x7c(%rax), %edx
 2d01310:      	ja	0x2d0212c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f7c>
 2d01316:      	subq	%rbx, %rdx
 2d01319:      	shlq	$0x3, %rdi
 2d0131d:      	movq	0xe0(%rsp), %rax
 2d01325:      	addq	(%rax), %rdi
 2d01328:      	movq	%rdx, %rbx
 2d0132b:      	leal	(,%rdx,8), %edx
 2d01332:      	xorl	%esi, %esi
 2d01334:      	callq	0x828ab90 <memset@plt>
 2d01339:      	addl	%ebx, %r12d
 2d0133c:      	movl	%r12d, %edx
 2d0133f:      	movq	(%rsp), %rax
 2d01343:      	movl	%edx, 0x78(%rax)
 2d01346:      	movl	%edx, %ebx
 2d01348:      	andl	$0x3f, %ebp
 2d0134b:      	je	0x2d0136e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41be>
 2d0134d:      	movq	$-0x1, %rax
 2d01354:      	movl	%ebp, %ecx
 2d01356:      	shlq	%cl, %rax
 2d01359:      	notq	%rax
 2d0135c:      	movq	0xe0(%rsp), %rcx
 2d01364:      	movq	(%rcx), %rcx
 2d01367:      	movl	%ebx, %edx
 2d01369:      	andq	%rax, -0x8(%rcx,%rdx,8)
 2d0136e:      	movq	0x118(%rsp), %rdi
 2d01376:      	movq	0x10(%rsp), %rbx
 2d0137b:      	movq	%rbx, %rsi
 2d0137e:      	callq	0x35c0c30 <_ZN4llvm12LiveRegUnits11addLiveOutsERKNS_17MachineBasicBlockE>
 2d01383:      	leaq	0x30(%rbx), %rax
 2d01387:      	movq	(%rsp), %rcx
 2d0138b:      	movq	%rax, 0x1f8(%rcx)
 2d01392:      	movb	$0x1, 0x200(%rcx)
 2d01399:      	movq	0x78(%rsp), %rbx
 2d0139e:      	jmp	0x2d013bf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x420f>
 2d013a0:      	movq	%rsi, 0x1f8(%rcx)
 2d013a7:      	movq	0x118(%rsp), %rdi
 2d013af:      	callq	0x35c02a0 <_ZN4llvm12LiveRegUnits12stepBackwardERKNS_12MachineInstrE>
 2d013b4:      	movq	(%rsp), %rcx
 2d013b8:      	movq	0x1f8(%rcx), %rax
 2d013bf:      	cmpq	0x20(%rsp), %rax
 2d013c4:      	je	0x2d013f5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4245>
 2d013c6:      	movq	(%rax), %rsi
 2d013c9:      	andq	$-0x8, %rsi
 2d013cd:      	testb	$0x4, (%rsi)
 2d013d0:      	jne	0x2d013a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d013d2:      	nopw	%cs:(%rax,%rax)
 2d013dc:      	nopl	(%rax)
 2d013e0:      	testb	$0x4, 0x2c(%rsi)
 2d013e4:      	je	0x2d013a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d013e6:      	movq	(%rsi), %rsi
 2d013e9:      	andq	$-0x8, %rsi
 2d013ed:      	testb	$0x4, 0x2c(%rsi)
 2d013f1:      	jne	0x2d013e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4236>
 2d013f3:      	jmp	0x2d013a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d013f5:      	cmpl	$0x104b, %ebx           # imm = 0x104B
 2d013fb:      	jle	0x2d01426 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4276>
 2d013fd:      	leal	-0x104c(%rbx), %eax
 2d01403:      	cmpl	$0x2, %eax
 2d01406:      	jb	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0140c:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2d01412:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01418:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2d0141e:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01424:      	jmp	0x2d0144a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x429a>
 2d01426:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d0142c:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01432:      	cmpl	$0xb51, %ebx            # imm = 0xB51
 2d01438:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0143e:      	cmpl	$0xb53, %ebx            # imm = 0xB53
 2d01444:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0144a:      	movq	0x118(%rsp), %rax
 2d01452:      	movq	(%rax), %rcx
 2d01455:      	movq	0x38(%rcx), %rax
 2d01459:      	testq	%rax, %rax
 2d0145c:      	je	0x2d014cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0145e:      	movq	0x80(%rsp), %rdx
 2d01466:      	leaq	(%r14,%rdx,8), %rdx
 2d0146a:      	movq	0xe0(%rsp), %rsi
 2d01472:      	movq	(%rsi), %rsi
 2d01475:      	movq	0x8(%rcx), %rdi
 2d01479:      	movq	%r14, %r8
 2d0147c:      	movl	(%r8), %ecx
 2d0147f:      	leaq	(%rcx,%rcx,2), %rcx
 2d01483:      	movl	0x10(%rdi,%rcx,8), %ecx
 2d01487:      	movl	%ecx, %r9d
 2d0148a:      	shrl	$0xc, %r9d
 2d0148e:      	leaq	(%rax,%r9,2), %r9
 2d01492:      	andl	$0xfff, %ecx            # imm = 0xFFF
 2d01498:      	nopl	(%rax,%rax)
 2d014a0:      	movl	$0x1, %r10d
 2d014a6:      	shlq	%cl, %r10
 2d014a9:      	movl	%ecx, %r11d
 2d014ac:      	shrl	$0x6, %r11d
 2d014b0:      	orq	%r10, (%rsi,%r11,8)
 2d014b4:      	movswl	(%r9), %r10d
 2d014b8:      	addq	$0x2, %r9
 2d014bc:      	addl	%r10d, %ecx
 2d014bf:      	testl	%r10d, %r10d
 2d014c2:      	jne	0x2d014a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x42f0>
 2d014c4:      	addq	$0x8, %r8
 2d014c8:      	cmpq	%rdx, %r8
 2d014cb:      	jne	0x2d0147c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x42cc>
 2d014cd:      	movq	(%rsp), %rcx
 2d014d1:      	cmpb	$0x0, 0x202(%rcx)
 2d014d8:      	leaq	0x55aa889(%rip), %rbp   # 0x82abd68 <_ZN4llvm3ARM11GPRRegClassE>
 2d014df:      	leaq	0x55a7fe2(%rip), %rax   # 0x82a94c8 <_ZN4llvm3ARM12tGPRRegClassE>
 2d014e6:      	cmovneq	%rax, %rbp
 2d014ea:      	cmpb	$0x0, 0x201(%rcx)
 2d014f1:      	jne	0x2d01511 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4361>
 2d014f3:      	movq	0x38(%rcx), %rsi
 2d014f7:      	movq	0x1f8(%rsp), %rdi
 2d014ff:      	xorl	%edx, %edx
 2d01501:      	callq	0x3853640 <_ZN4llvm17RegisterClassInfo20runOnMachineFunctionERKNS_15MachineFunctionEb>
 2d01506:      	movq	(%rsp), %rcx
 2d0150a:      	movb	$0x1, 0x201(%rcx)
 2d01511:      	movq	(%rbp), %rax
 2d01515:      	movzwl	0x18(%rax), %eax
 2d01519:      	movq	0xb8(%rcx), %rbx
 2d01520:      	leaq	(%rax,%rax,2), %r12
 2d01524:      	movl	0xc0(%rcx), %eax
 2d0152a:      	cmpl	(%rbx,%r12,8), %eax
 2d0152e:      	je	0x2d01540 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4390>
 2d01530:      	movq	0x1f8(%rsp), %rdi
 2d01538:      	movq	%rbp, %rsi
 2d0153b:      	callq	0x3853e30 <_ZNK4llvm17RegisterClassInfo7computeEPKNS_19TargetRegisterClassE>
 2d01540:      	leaq	(%rbx,%r12,8), %rax
 2d01544:      	movl	0x4(%rax), %esi
 2d01547:      	testq	%rsi, %rsi
 2d0154a:      	movq	0x80(%rsp), %rbx
 2d01552:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01558:      	movq	0x10(%rax), %rax
 2d0155c:      	movq	(%rsp), %rdi
 2d01560:      	movq	0x38(%rdi), %rcx
 2d01564:      	movq	0x68(%rdi), %r8
 2d01568:      	movq	0x38(%r8), %rdx
 2d0156c:      	testq	%rdx, %rdx
 2d0156f:      	je	0x2d01ef6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d46>
 2d01575:      	leaq	(%rax,%rsi,2), %rsi
 2d01579:      	movq	0x70(%rdi), %rdi
 2d0157d:      	movq	0x8(%r8), %r8
 2d01581:      	jmp	0x2d01590 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43e0>
 2d01583:      	addq	$0x2, %rax
 2d01587:      	cmpq	%rsi, %rax
 2d0158a:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01590:      	movzwl	(%rax), %r12d
 2d01594:      	leaq	(%r12,%r12,2), %r9
 2d01598:      	movl	0x10(%r8,%r9,8), %r9d
 2d0159d:      	movl	%r9d, %r10d
 2d015a0:      	shrl	$0xc, %r10d
 2d015a4:      	leaq	(%rdx,%r10,2), %r10
 2d015a8:      	andl	$0xfff, %r9d            # imm = 0xFFF
 2d015af:      	nop
 2d015b0:      	movl	%r9d, %r11d
 2d015b3:      	shrl	$0x6, %r11d
 2d015b7:      	movq	(%rdi,%r11,8), %r11
 2d015bb:      	btq	%r9, %r11
 2d015bf:      	jb	0x2d01583 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43d3>
 2d015c1:      	movswl	(%r10), %r11d
 2d015c5:      	addq	$0x2, %r10
 2d015c9:      	addl	%r11d, %r9d
 2d015cc:      	testl	%r11d, %r11d
 2d015cf:      	jne	0x2d015b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4400>
 2d015d1:      	movq	0x20(%rcx), %r9
 2d015d5:      	movq	0x178(%r9), %r9
 2d015dc:      	movl	%r12d, %r10d
 2d015df:      	shrl	$0x6, %r10d
 2d015e3:      	movq	(%r9,%r10,8), %r9
 2d015e7:      	btq	%r12, %r9
 2d015eb:      	jb	0x2d01583 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43d3>
 2d015ed:      	testl	%r12d, %r12d
 2d015f0:      	movl	0xdc(%rsp), %eax
 2d015f7:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d015fd:      	movq	%rbx, %r9
 2d01600:      	movq	(%rsp), %rcx
 2d01604:      	movzbl	0x203(%rcx), %esi
 2d0160b:      	movl	0x18(%rsp), %r8d
 2d01610:      	movl	%eax, 0xdc(%rsp)
 2d01617:      	testb	%sil, %sil
 2d0161a:      	jne	0x2cffc2a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a7a>
 2d01620:      	movq	%r9, %rbx
 2d01623:      	movzbl	0x202(%rcx), %eax
 2d0162a:      	xorl	%esi, %esi
 2d0162c:      	cmpl	$0x8, %r8d
 2d01630:      	setge	%sil
 2d01634:      	addl	$0x1151, %esi           # imm = 0x1151
 2d0163a:      	cmpl	$0x11, 0x8(%rsp)
 2d0163f:      	movl	$0x1154, %edx           # imm = 0x1154
 2d01644:      	cmovel	%edx, %esi
 2d01647:      	testb	%al, %al
 2d01649:      	movl	$0x325, %edx            # imm = 0x325
 2d0164e:      	cmovel	%edx, %esi
 2d01651:      	testl	%r8d, %r8d
 2d01654:      	jns	0x2d01689 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d9>
 2d01656:      	movl	%r8d, %ecx
 2d01659:      	negl	%ecx
 2d0165b:      	cmpl	$-0x7, %r8d
 2d0165f:      	setae	%dl
 2d01662:      	cmpl	$0x11, 0x8(%rsp)
 2d01667:      	setne	%sil
 2d0166b:      	andb	%dl, %sil
 2d0166e:      	movzbl	%sil, %esi
 2d01672:      	xorl	$0x119b, %esi           # imm = 0x119B
 2d01678:      	testb	%al, %al
 2d0167a:      	movl	$0x7fb, %eax            # imm = 0x7FB
 2d0167f:      	cmovel	%eax, %esi
 2d01682:      	movl	%ecx, %r8d
 2d01685:      	movq	(%rsp), %rcx
 2d01689:      	movq	%rsi, 0x128(%rsp)
 2d01691:      	movq	0x58(%rcx), %rdi
 2d01695:      	movl	%r8d, %ebp
 2d01698:      	movq	(%rdi), %rax
 2d0169b:      	movq	%rbp, %rsi
 2d0169e:      	callq	*0x530(%rax)
 2d016a4:      	testb	%al, %al
 2d016a6:      	je	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d016ac:      	movq	%rbx, %rdx
 2d016af:      	movq	%r12, 0x18(%rsp)
 2d016b4:      	cmpl	$-0x1, 0x70(%rsp)
 2d016b9:      	je	0x2d0171a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x456a>
 2d016bb:      	movq	0x78(%rsp), %rax
 2d016c0:      	cmpl	$0x7f9, %eax            # imm = 0x7F9
 2d016c5:      	movq	0x20(%rsp), %r12
 2d016ca:      	je	0x2d016e8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d016cc:      	cmpl	$0x1197, %eax           # imm = 0x1197
 2d016d1:      	je	0x2d016e8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d016d3:      	cmpl	$0x1199, %eax           # imm = 0x1199
 2d016d8:      	je	0x2d016e8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d016da:      	addl	$0xffffeef1, %eax       # imm = 0xFFFFEEF1
 2d016df:      	movb	$0x1, %r13b
 2d016e2:      	cmpw	$0x1, %ax
 2d016e6:      	ja	0x2d01722 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d016e8:      	leaq	-0x8(,%rdx,8), %rax
 2d016f0:      	xorl	%ecx, %ecx
 2d016f2:      	nopw	%cs:(%rax,%rax)
 2d016fc:      	nopl	(%rax)
 2d01700:      	movq	0x8(%rsp), %rsi
 2d01705:      	cmpl	%esi, (%r14,%rcx)
 2d01709:      	setne	%r13b
 2d0170d:      	je	0x2d01722 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d0170f:      	cmpq	%rcx, %rax
 2d01712:      	leaq	0x8(%rcx), %rcx
 2d01716:      	jne	0x2d01700 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4550>
 2d01718:      	jmp	0x2d01722 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d0171a:      	xorl	%r13d, %r13d
 2d0171d:      	movq	0x20(%rsp), %r12
 2d01722:      	movq	(%rsp), %rcx
 2d01726:      	cmpb	$0x1, 0x202(%rcx)
 2d0172d:      	movq	%rdx, 0x80(%rsp)
 2d01735:      	jne	0x2d01af1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4941>
 2d0173b:      	movq	0x8(%rsp), %rax
 2d01740:      	cmpl	0x18(%rsp), %eax
 2d01744:      	leaq	0xa0(%rsp), %rax
 2d0174c:      	je	0x2d01933 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4783>
 2d01752:      	movq	0x128(%rsp), %rcx
 2d0175a:      	cmpl	$0x119b, %ecx           # imm = 0x119B
 2d01760:      	je	0x2d0176e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x45be>
 2d01762:      	cmpl	$0x1152, %ecx           # imm = 0x1152
 2d01768:      	jne	0x2d0193b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x478b>
 2d0176e:      	movq	0x18(%rsp), %rax
 2d01773:      	addl	$-0x4a, %eax
 2d01776:      	movq	0x8(%rsp), %rcx
 2d0177b:      	addl	$-0x4a, %ecx
 2d0177e:      	orl	%eax, %ecx
 2d01780:      	cmpl	$0x7, %ecx
 2d01783:      	movq	(%rsp), %rcx
 2d01787:      	ja	0x2d0179a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x45ea>
 2d01789:      	movq	0x50(%rcx), %rax
 2d0178d:      	cmpb	$0x0, 0x181(%rax)
 2d01794:      	je	0x2d01f2d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d7d>
 2d0179a:      	movq	0xc8(%rsp), %rsi
 2d017a2:      	movq	%rsi, 0x1b0(%rsp)
 2d017aa:      	leaq	0xa0(%rsp), %rax
 2d017b2:      	testq	%rsi, %rsi
 2d017b5:      	je	0x2d01801 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4651>
 2d017b7:      	movl	$0x1, %edx
 2d017bc:      	leaq	0x1b0(%rsp), %rdi
 2d017c4:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d017c9:      	movq	(%rsp), %rcx
 2d017cd:      	movq	0x1b0(%rsp), %rsi
 2d017d5:      	movq	%rsi, 0xa0(%rsp)
 2d017dd:      	testq	%rsi, %rsi
 2d017e0:      	je	0x2d01808 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4658>
 2d017e2:      	leaq	0x1b0(%rsp), %rbx
 2d017ea:      	movq	%rbx, %rdi
 2d017ed:      	leaq	0xa0(%rsp), %rdx
 2d017f5:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d017fa:      	movq	(%rsp), %rcx
 2d017fe:      	movq	%rbx, %rax
 2d01801:      	movq	$0x0, (%rax)
 2d01808:      	movq	%rbp, 0x70(%rsp)
 2d0180d:      	leaq	0xa8(%rsp), %rax
 2d01815:      	xorps	%xmm0, %xmm0
 2d01818:      	movups	%xmm0, (%rax)
 2d0181b:      	movq	$0x0, 0x10(%rax)
 2d01823:      	movq	0x40(%rcx), %rax
 2d01827:      	movq	0x8(%rax), %rcx
 2d0182b:      	movq	$-0x23080, %rax         # imm = 0xFFFDCF80
 2d01832:      	addq	%rax, %rcx
 2d01835:      	movq	0x10(%rsp), %rdi
 2d0183a:      	movq	%r12, %rsi
 2d0183d:      	leaq	0xa0(%rsp), %rbx
 2d01845:      	movq	%rbx, %rdx
 2d01848:      	movq	0x18(%rsp), %r12
 2d0184d:      	movl	%r12d, %r8d
 2d01850:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01855:      	movq	%rax, 0xf0(%rsp)
 2d0185d:      	movq	%rdx, 0xf8(%rsp)
 2d01865:      	movzbl	%r13b, %edx
 2d01869:      	shll	$0x3, %edx
 2d0186c:      	leaq	0xf0(%rsp), %rdi
 2d01874:      	movq	0x8(%rsp), %rsi
 2d01879:      	xorl	%ecx, %ecx
 2d0187b:      	callq	0x27f0690 <_ZNK4llvm19MachineInstrBuilder6addRegENS_8RegisterEjj>
 2d01880:      	movq	%rax, %rbp
 2d01883:      	movl	0x28(%rsp), %eax
 2d01887:      	movl	$0x1, 0x30(%rsp)
 2d0188f:      	movq	$0x0, 0x38(%rsp)
 2d01898:      	movq	%rax, 0x40(%rsp)
 2d0189d:      	movq	$0x0, 0x58(%rsp)
 2d018a6:      	movq	0x88(%rsp), %rax
 2d018ae:      	movl	%eax, 0x54(%rsp)
 2d018b2:      	leaq	0x40(%rsp), %rax
 2d018b7:      	xorps	%xmm0, %xmm0
 2d018ba:      	movups	%xmm0, 0x20(%rax)
 2d018be:      	movl	$0x0, 0x50(%rsp)
 2d018c6:      	movq	(%rbp), %rsi
 2d018ca:      	movq	0x8(%rbp), %rdi
 2d018ce:      	leaq	0x30(%rsp), %rdx
 2d018d3:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d018d8:      	movq	(%rbp), %rsi
 2d018dc:      	movq	0x8(%rbp), %rdi
 2d018e0:      	leaq	0x50(%rsp), %rdx
 2d018e5:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d018ea:      	movq	0xa0(%rsp), %rsi
 2d018f2:      	testq	%rsi, %rsi
 2d018f5:      	je	0x2d018ff <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x474f>
 2d018f7:      	movq	%rbx, %rdi
 2d018fa:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d018ff:      	movq	0x1b0(%rsp), %rsi
 2d01907:      	testq	%rsi, %rsi
 2d0190a:      	je	0x2d01919 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4769>
 2d0190c:      	leaq	0x1b0(%rsp), %rdi
 2d01914:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01919:      	movb	$0x1, %r13b
 2d0191c:      	movq	%r12, 0x8(%rsp)
 2d01921:      	leaq	0xa0(%rsp), %rax
 2d01929:      	movq	0x20(%rsp), %r12
 2d0192e:      	movq	0x70(%rsp), %rbp
 2d01933:      	movq	0x128(%rsp), %rcx
 2d0193b:      	cmpl	$0x1154, %ecx           # imm = 0x1154
 2d01941:      	jne	0x2d01cd1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b21>
 2d01947:      	movq	0xc8(%rsp), %rsi
 2d0194f:      	movq	%rsi, 0x1a8(%rsp)
 2d01957:      	testq	%rsi, %rsi
 2d0195a:      	je	0x2d0199e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47ee>
 2d0195c:      	movl	$0x1, %edx
 2d01961:      	leaq	0x1a8(%rsp), %rdi
 2d01969:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d0196e:      	movq	0x1a8(%rsp), %rsi
 2d01976:      	movq	%rsi, 0xa0(%rsp)
 2d0197e:      	testq	%rsi, %rsi
 2d01981:      	je	0x2d019a5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47f5>
 2d01983:      	leaq	0x1a8(%rsp), %rbx
 2d0198b:      	movq	%rbx, %rdi
 2d0198e:      	leaq	0xa0(%rsp), %rdx
 2d01996:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d0199b:      	movq	%rbx, %rax
 2d0199e:      	movq	$0x0, (%rax)
 2d019a5:      	leaq	0xa8(%rsp), %rax
 2d019ad:      	xorps	%xmm0, %xmm0
 2d019b0:      	movups	%xmm0, (%rax)
 2d019b3:      	movq	$0x0, 0x10(%rax)
 2d019bb:      	movq	(%rsp), %rax
 2d019bf:      	movq	0x40(%rax), %rax
 2d019c3:      	movq	0x8(%rax), %rcx
 2d019c7:      	movq	$-0x22a80, %rax         # imm = 0xFFFDD580
 2d019ce:      	addq	%rax, %rcx
 2d019d1:      	movq	0x10(%rsp), %rdi
 2d019d6:      	movq	%r12, %rsi
 2d019d9:      	leaq	0xa0(%rsp), %rdx
 2d019e1:      	movq	0x18(%rsp), %r8
 2d019e6:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d019eb:      	movq	%rax, %rsi
 2d019ee:      	movq	%rdx, %rbx
 2d019f1:      	movq	$0x0, 0x38(%rsp)
 2d019fa:      	movzbl	%r13b, %eax
 2d019fe:      	shll	$0x1a, %eax
 2d01a01:      	movq	0x8(%rsp), %rcx
 2d01a06:      	movl	%ecx, 0x34(%rsp)
 2d01a0a:      	leaq	0x40(%rsp), %rcx
 2d01a0f:      	xorps	%xmm0, %xmm0
 2d01a12:      	movups	%xmm0, (%rcx)
 2d01a15:      	movl	%eax, 0x30(%rsp)
 2d01a19:      	movq	%rdx, %rdi
 2d01a1c:      	movq	%rsi, %r13
 2d01a1f:      	leaq	0x30(%rsp), %r12
 2d01a24:      	movq	%r12, %rdx
 2d01a27:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01a2c:      	shrl	$0x2, %ebp
 2d01a2f:      	movl	$0x1, 0x30(%rsp)
 2d01a37:      	movq	$0x0, 0x38(%rsp)
 2d01a40:      	movq	%rbp, 0x40(%rsp)
 2d01a45:      	movq	%rbx, %rdi
 2d01a48:      	movq	%r13, %rsi
 2d01a4b:      	movq	%r12, %rdx
 2d01a4e:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01a53:      	movl	0x28(%rsp), %eax
 2d01a57:      	movl	$0x1, 0x30(%rsp)
 2d01a5f:      	movq	$0x0, 0x38(%rsp)
 2d01a68:      	movq	%rax, 0x40(%rsp)
 2d01a6d:      	movq	$0x0, 0x58(%rsp)
 2d01a76:      	movq	0x88(%rsp), %rax
 2d01a7e:      	movl	%eax, 0x54(%rsp)
 2d01a82:      	xorps	%xmm0, %xmm0
 2d01a85:      	leaq	0x40(%rsp), %rax
 2d01a8a:      	movups	%xmm0, 0x20(%rax)
 2d01a8e:      	movl	$0x0, 0x50(%rsp)
 2d01a96:      	movq	%rbx, %rdi
 2d01a99:      	movq	%r13, %rsi
 2d01a9c:      	movq	%r12, %rdx
 2d01a9f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01aa4:      	movq	%rbx, %rdi
 2d01aa7:      	movq	%r13, %rsi
 2d01aaa:      	leaq	0x50(%rsp), %rdx
 2d01aaf:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01ab4:      	movq	0xa0(%rsp), %rsi
 2d01abc:      	testq	%rsi, %rsi
 2d01abf:      	je	0x2d01ace <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x491e>
 2d01ac1:      	leaq	0xa0(%rsp), %rdi
 2d01ac9:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01ace:      	movq	0x1a8(%rsp), %rsi
 2d01ad6:      	testq	%rsi, %rsi
 2d01ad9:      	movq	0x78(%rsp), %rbx
 2d01ade:      	je	0x2d01ec3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01ae4:      	leaq	0x1a8(%rsp), %rdi
 2d01aec:      	jmp	0x2d01ebe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d0e>
 2d01af1:      	movq	0xc8(%rsp), %rsi
 2d01af9:      	movq	%rsi, 0x198(%rsp)
 2d01b01:      	leaq	0xa0(%rsp), %rax
 2d01b09:      	testq	%rsi, %rsi
 2d01b0c:      	je	0x2d01b58 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x49a8>
 2d01b0e:      	movl	$0x1, %edx
 2d01b13:      	leaq	0x198(%rsp), %rdi
 2d01b1b:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01b20:      	movq	(%rsp), %rcx
 2d01b24:      	movq	0x198(%rsp), %rsi
 2d01b2c:      	movq	%rsi, 0xa0(%rsp)
 2d01b34:      	testq	%rsi, %rsi
 2d01b37:      	je	0x2d01b5f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x49af>
 2d01b39:      	leaq	0x198(%rsp), %rbx
 2d01b41:      	movq	%rbx, %rdi
 2d01b44:      	leaq	0xa0(%rsp), %rdx
 2d01b4c:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01b51:      	movq	(%rsp), %rcx
 2d01b55:      	movq	%rbx, %rax
 2d01b58:      	movq	$0x0, (%rax)
 2d01b5f:      	leaq	0xa8(%rsp), %rax
 2d01b67:      	xorps	%xmm0, %xmm0
 2d01b6a:      	movups	%xmm0, (%rax)
 2d01b6d:      	movq	$0x0, 0x10(%rax)
 2d01b75:      	movq	0x40(%rcx), %rax
 2d01b79:      	movq	0x8(%rax), %rcx
 2d01b7d:      	movq	0x128(%rsp), %rax
 2d01b85:      	shll	$0x5, %eax
 2d01b88:      	subq	%rax, %rcx
 2d01b8b:      	movq	0x10(%rsp), %rdi
 2d01b90:      	movq	%r12, %rsi
 2d01b93:      	leaq	0xa0(%rsp), %rdx
 2d01b9b:      	movq	0x18(%rsp), %r8
 2d01ba0:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01ba5:      	movq	%rbp, %rbx
 2d01ba8:      	movq	%rdx, %rbp
 2d01bab:      	movq	$0x0, 0x38(%rsp)
 2d01bb4:      	movzbl	%r13b, %edx
 2d01bb8:      	shll	$0x1a, %edx
 2d01bbb:      	movq	0x8(%rsp), %rcx
 2d01bc0:      	movl	%ecx, 0x34(%rsp)
 2d01bc4:      	leaq	0x40(%rsp), %rcx
 2d01bc9:      	xorps	%xmm0, %xmm0
 2d01bcc:      	movups	%xmm0, (%rcx)
 2d01bcf:      	movl	%edx, 0x30(%rsp)
 2d01bd3:      	movq	%rbp, %rdi
 2d01bd6:      	movq	%rax, %r13
 2d01bd9:      	movq	%rax, %rsi
 2d01bdc:      	leaq	0x30(%rsp), %r12
 2d01be1:      	movq	%r12, %rdx
 2d01be4:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01be9:      	movl	$0x1, 0x30(%rsp)
 2d01bf1:      	movq	$0x0, 0x38(%rsp)
 2d01bfa:      	movq	%rbx, 0x40(%rsp)
 2d01bff:      	movq	%rbp, %rdi
 2d01c02:      	movq	%r13, %rsi
 2d01c05:      	movq	%r12, %rdx
 2d01c08:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c0d:      	movl	0x28(%rsp), %eax
 2d01c11:      	movl	$0x1, 0x30(%rsp)
 2d01c19:      	movq	$0x0, 0x38(%rsp)
 2d01c22:      	movq	%rax, 0x40(%rsp)
 2d01c27:      	movq	$0x0, 0x58(%rsp)
 2d01c30:      	movq	0x88(%rsp), %rax
 2d01c38:      	movl	%eax, 0x54(%rsp)
 2d01c3c:      	xorps	%xmm0, %xmm0
 2d01c3f:      	leaq	0x40(%rsp), %rax
 2d01c44:      	movups	%xmm0, 0x20(%rax)
 2d01c48:      	movl	$0x0, 0x50(%rsp)
 2d01c50:      	movq	%rbp, %rdi
 2d01c53:      	movq	%r13, %rsi
 2d01c56:      	movq	%r12, %rdx
 2d01c59:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c5e:      	movq	%rbp, %rdi
 2d01c61:      	movq	%r13, %rsi
 2d01c64:      	leaq	0x50(%rsp), %rdx
 2d01c69:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c6e:      	xorps	%xmm0, %xmm0
 2d01c71:      	movaps	%xmm0, 0x100(%rsp)
 2d01c79:      	movaps	%xmm0, 0xf0(%rsp)
 2d01c81:      	movq	%rbp, %rdi
 2d01c84:      	movq	%r13, %rsi
 2d01c87:      	leaq	0xf0(%rsp), %rdx
 2d01c8f:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c94:      	movq	0xa0(%rsp), %rsi
 2d01c9c:      	testq	%rsi, %rsi
 2d01c9f:      	je	0x2d01cae <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4afe>
 2d01ca1:      	leaq	0xa0(%rsp), %rdi
 2d01ca9:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01cae:      	movq	0x198(%rsp), %rsi
 2d01cb6:      	testq	%rsi, %rsi
 2d01cb9:      	movq	0x78(%rsp), %rbx
 2d01cbe:      	je	0x2d01ec3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01cc4:      	leaq	0x198(%rsp), %rdi
 2d01ccc:      	jmp	0x2d01ebe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d0e>
 2d01cd1:      	movq	0xc8(%rsp), %rsi
 2d01cd9:      	movq	%rsi, 0x1a0(%rsp)
 2d01ce1:      	testq	%rsi, %rsi
 2d01ce4:      	je	0x2d01d28 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b78>
 2d01ce6:      	movl	$0x1, %edx
 2d01ceb:      	leaq	0x1a0(%rsp), %rdi
 2d01cf3:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01cf8:      	movq	0x1a0(%rsp), %rsi
 2d01d00:      	movq	%rsi, 0xa0(%rsp)
 2d01d08:      	testq	%rsi, %rsi
 2d01d0b:      	je	0x2d01d2f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b7f>
 2d01d0d:      	leaq	0x1a0(%rsp), %rbx
 2d01d15:      	movq	%rbx, %rdi
 2d01d18:      	leaq	0xa0(%rsp), %rdx
 2d01d20:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01d25:      	movq	%rbx, %rax
 2d01d28:      	movq	$0x0, (%rax)
 2d01d2f:      	leaq	0xa8(%rsp), %rax
 2d01d37:      	xorps	%xmm0, %xmm0
 2d01d3a:      	movups	%xmm0, (%rax)
 2d01d3d:      	movq	$0x0, 0x10(%rax)
 2d01d45:      	movq	(%rsp), %rax
 2d01d49:      	movq	0x40(%rax), %rax
 2d01d4d:      	movq	0x8(%rax), %rcx
 2d01d51:      	movq	0x128(%rsp), %rax
 2d01d59:      	shll	$0x5, %eax
 2d01d5c:      	subq	%rax, %rcx
 2d01d5f:      	movq	0x10(%rsp), %rdi
 2d01d64:      	movq	%r12, %rsi
 2d01d67:      	leaq	0xa0(%rsp), %rdx
 2d01d6f:      	movq	0x18(%rsp), %r8
 2d01d74:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01d79:      	movq	%rax, %rbx
 2d01d7c:      	movq	%rbp, 0x70(%rsp)
 2d01d81:      	movq	%rdx, %rbp
 2d01d84:      	movq	$0x0, 0xf8(%rsp)
 2d01d90:      	movl	$0x3, 0xf4(%rsp)
 2d01d9b:      	leaq	0x100(%rsp), %rax
 2d01da3:      	xorps	%xmm0, %xmm0
 2d01da6:      	movups	%xmm0, (%rax)
 2d01da9:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d01db4:      	movq	%rdx, %rdi
 2d01db7:      	movq	%rbx, %rsi
 2d01dba:      	leaq	0xf0(%rsp), %rdx
 2d01dc2:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01dc7:      	movq	$0x0, 0x38(%rsp)
 2d01dd0:      	movzbl	%r13b, %eax
 2d01dd4:      	shll	$0x1a, %eax
 2d01dd7:      	movq	0x8(%rsp), %rcx
 2d01ddc:      	movl	%ecx, 0x34(%rsp)
 2d01de0:      	leaq	0x40(%rsp), %r13
 2d01de5:      	xorps	%xmm0, %xmm0
 2d01de8:      	movups	%xmm0, (%r13)
 2d01ded:      	movl	%eax, 0x30(%rsp)
 2d01df1:      	movq	%rbp, %rdi
 2d01df4:      	movq	%rbx, %rsi
 2d01df7:      	leaq	0x30(%rsp), %r12
 2d01dfc:      	movq	%r12, %rdx
 2d01dff:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e04:      	movl	$0x1, 0x30(%rsp)
 2d01e0c:      	movq	$0x0, 0x38(%rsp)
 2d01e15:      	movq	0x70(%rsp), %rax
 2d01e1a:      	movq	%rax, 0x40(%rsp)
 2d01e1f:      	movq	%rbp, %rdi
 2d01e22:      	movq	%rbx, %rsi
 2d01e25:      	movq	%r12, %rdx
 2d01e28:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e2d:      	movl	0x28(%rsp), %eax
 2d01e31:      	movl	$0x1, 0x30(%rsp)
 2d01e39:      	movq	$0x0, 0x38(%rsp)
 2d01e42:      	movq	%rax, 0x40(%rsp)
 2d01e47:      	movq	$0x0, 0x58(%rsp)
 2d01e50:      	movq	0x88(%rsp), %rax
 2d01e58:      	movl	%eax, 0x54(%rsp)
 2d01e5c:      	xorps	%xmm0, %xmm0
 2d01e5f:      	movups	%xmm0, 0x20(%r13)
 2d01e64:      	movl	$0x0, 0x50(%rsp)
 2d01e6c:      	movq	%rbp, %rdi
 2d01e6f:      	movq	%rbx, %rsi
 2d01e72:      	movq	%r12, %rdx
 2d01e75:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e7a:      	movq	%rbp, %rdi
 2d01e7d:      	movq	%rbx, %rsi
 2d01e80:      	leaq	0x50(%rsp), %rdx
 2d01e85:      	callq	0x36505e0 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e8a:      	movq	0xa0(%rsp), %rsi
 2d01e92:      	testq	%rsi, %rsi
 2d01e95:      	je	0x2d01ea4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4cf4>
 2d01e97:      	leaq	0xa0(%rsp), %rdi
 2d01e9f:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01ea4:      	movq	0x1a0(%rsp), %rsi
 2d01eac:      	testq	%rsi, %rsi
 2d01eaf:      	movq	0x78(%rsp), %rbx
 2d01eb4:      	je	0x2d01ec3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01eb6:      	leaq	0x1a0(%rsp), %rdi
 2d01ebe:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01ec3:      	movl	$0x1, %ecx
 2d01ec8:      	movb	$0x1, %al
 2d01eca:      	movb	$0x1, %r13b
 2d01ecd:      	movq	0x80(%rsp), %r9
 2d01ed5:      	movq	0x18(%rsp), %r12
 2d01eda:      	movl	0xdc(%rsp), %r10d
 2d01ee2:      	movb	$0x1, %sil
 2d01ee5:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d01eeb:      	jne	0x2cffc69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2d01ef1:      	jmp	0x2cffc88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2d01ef6:      	addq	%rsi, %rsi
 2d01ef9:      	movq	0x20(%rcx), %rcx
 2d01efd:      	movq	0x178(%rcx), %rcx
 2d01f04:      	xorl	%edx, %edx
 2d01f06:      	movzwl	(%rax,%rdx), %r12d
 2d01f0b:      	movl	%r12d, %edi
 2d01f0e:      	shrl	$0x6, %edi
 2d01f11:      	movq	(%rcx,%rdi,8), %rdi
 2d01f15:      	btq	%r12, %rdi
 2d01f19:      	jae	0x2d015ed <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x443d>
 2d01f1f:      	addq	$0x2, %rdx
 2d01f23:      	cmpq	%rdx, %rsi
 2d01f26:      	jne	0x2d01f06 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d56>
 2d01f28:      	jmp	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01f2d:      	cmpl	$0xe, 0x28(%rsp)
 2d01f32:      	movq	0x18(%rsp), %r12
 2d01f37:      	jne	0x2d02040 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01f3d:      	movq	%rbp, 0x70(%rsp)
 2d01f42:      	movq	0xc8(%rsp), %rsi
 2d01f4a:      	movq	%rsi, 0x1b8(%rsp)
 2d01f52:      	leaq	0x30(%rsp), %rax
 2d01f57:      	testq	%rsi, %rsi
 2d01f5a:      	je	0x2d01f98 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4de8>
 2d01f5c:      	movl	$0x1, %edx
 2d01f61:      	leaq	0x1b8(%rsp), %rdi
 2d01f69:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01f6e:      	movq	0x1b8(%rsp), %rsi
 2d01f76:      	movq	%rsi, 0x30(%rsp)
 2d01f7b:      	testq	%rsi, %rsi
 2d01f7e:      	je	0x2d01f9f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4def>
 2d01f80:      	leaq	0x1b8(%rsp), %rbx
 2d01f88:      	movq	%rbx, %rdi
 2d01f8b:      	leaq	0x30(%rsp), %rdx
 2d01f90:      	callq	0x3bd6df0 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01f95:      	movq	%rbx, %rax
 2d01f98:      	movq	$0x0, (%rax)
 2d01f9f:      	leaq	0x40(%rsp), %rax
 2d01fa4:      	xorps	%xmm0, %xmm0
 2d01fa7:      	movups	%xmm0, -0x8(%rax)
 2d01fab:      	movq	$0x0, 0x8(%rax)
 2d01fb3:      	movq	(%rsp), %rax
 2d01fb7:      	movq	0x40(%rax), %rax
 2d01fbb:      	movq	0x8(%rax), %rcx
 2d01fbf:      	movq	$-0x23040, %rax         # imm = 0xFFFDCFC0
 2d01fc6:      	addq	%rax, %rcx
 2d01fc9:      	movq	0x10(%rsp), %rdi
 2d01fce:      	movq	0x20(%rsp), %rsi
 2d01fd3:      	leaq	0x30(%rsp), %rbx
 2d01fd8:      	movq	%rbx, %rdx
 2d01fdb:      	movl	%r12d, %r8d
 2d01fde:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01fe3:      	movq	%rax, 0xa0(%rsp)
 2d01feb:      	movq	%rdx, 0xa8(%rsp)
 2d01ff3:      	movzbl	%r13b, %edx
 2d01ff7:      	shll	$0x3, %edx
 2d01ffa:      	leaq	0xa0(%rsp), %rdi
 2d02002:      	movq	0x8(%rsp), %rsi
 2d02007:      	xorl	%ecx, %ecx
 2d02009:      	callq	0x27f0690 <_ZNK4llvm19MachineInstrBuilder6addRegENS_8RegisterEjj>
 2d0200e:      	movq	0x30(%rsp), %rsi
 2d02013:      	testq	%rsi, %rsi
 2d02016:      	je	0x2d02020 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e70>
 2d02018:      	movq	%rbx, %rdi
 2d0201b:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d02020:      	movq	0x1b8(%rsp), %rsi
 2d02028:      	testq	%rsi, %rsi
 2d0202b:      	je	0x2d01919 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4769>
 2d02031:      	leaq	0x1b8(%rsp), %rdi
 2d02039:      	jmp	0x2d01914 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4764>
 2d0203e:      	nop
 2d02040:      	xorl	%r13d, %r13d
 2d02043:      	movq	0xc8(%rsp), %rsi
 2d0204b:      	testq	%rsi, %rsi
 2d0204e:      	jne	0x2cff94a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x279a>
 2d02054:      	jmp	0x2cff957 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27a7>
 2d02059:      	cmpl	$0x119b, %ebx           # imm = 0x119B
 2d0205f:      	je	0x2d0206d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ebd>
 2d02061:      	cmpl	$0x1152, %ebx           # imm = 0x1152
 2d02067:      	jne	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d0206d:      	movq	0x20(%r12), %r13
 2d02072:      	movzwl	0x28(%r12), %ecx
 2d02078:      	movzbl	0x2a(%r12), %eax
 2d0207e:      	shll	$0x10, %eax
 2d02081:      	orl	%ecx, %eax
 2d02083:      	testl	%eax, %eax
 2d02085:      	je	0x2d020c3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f13>
 2d02087:      	shll	$0x5, %eax
 2d0208a:      	xorl	%ecx, %ecx
 2d0208c:      	jmp	0x2d02097 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ee7>
 2d0208e:      	addq	$0x20, %rcx
 2d02092:      	cmpq	%rcx, %rax
 2d02095:      	je	0x2d020c3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f13>
 2d02097:      	movl	(%r13,%rcx), %edx
 2d0209c:      	movl	%edx, %esi
 2d0209e:      	andl	$0x10000ff, %esi        # imm = 0x10000FF
 2d020a4:      	cmpl	$0x1000000, %esi        # imm = 0x1000000
 2d020aa:      	jne	0x2d0208e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d020ac:      	notl	%edx
 2d020ae:      	testl	$0x5000000, %edx        # imm = 0x5000000
 2d020b4:      	je	0x2d0208e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d020b6:      	cmpl	$0x3, 0x4(%r13,%rcx)
 2d020bc:      	jne	0x2d0208e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d020be:      	jmp	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d020c3:      	movq	0x10(%r12), %rax
 2d020c8:      	movzwl	0x2(%rax), %eax
 2d020cc:      	movl	$0xfffffffd, %ecx       # imm = 0xFFFFFFFD
 2d020d1:      	leal	(%rcx,%rax), %r14d
 2d020d5:      	shlq	$0x5, %r14
 2d020d9:      	leal	(,%r9,4), %eax
 2d020e1:      	movq	%rax, %rbp
 2d020e4:      	negq	%rbp
 2d020e7:      	cmpl	$0x119b, %ebx           # imm = 0x119B
 2d020ed:      	cmoveq	%rax, %rbp
 2d020f1:      	addq	0x10(%r13,%r14), %rbp
 2d020f6:      	testl	%ebp, %ebp
 2d020f8:      	js	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d020fe:      	movq	(%rsp), %rax
 2d02102:      	movq	0x58(%rax), %rdi
 2d02106:      	andl	$0x7fffffff, %ebp       # imm = 0x7FFFFFFF
 2d0210c:      	movq	(%rdi), %rax
 2d0210f:      	movq	%rbp, %rsi
 2d02112:      	callq	*0x530(%rax)
 2d02118:      	testb	%al, %al
 2d0211a:      	je	0x2d004c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d02120:      	addq	%r14, %r13
 2d02123:      	movq	%rbp, 0x10(%r13)
 2d02127:      	jmp	0x2d00853 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0212c:      	movl	$0x8, %ecx
 2d02131:      	movq	0xe0(%rsp), %rdi
 2d02139:      	movq	0x220(%rsp), %rsi
 2d02141:      	movq	%rdx, %r12
 2d02144:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d02149:      	movq	%r12, %rdx
 2d0214c:      	movq	(%rsp), %rax
 2d02150:      	movl	0x78(%rax), %edi
 2d02153:      	movl	0xb0(%rax), %ebp
 2d02159:      	movl	%edi, %r12d
 2d0215c:      	jmp	0x2d01316 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4166>
 2d02161:      	xorl	%eax, %eax
 2d02163:      	movq	%rax, %r12
 2d02166:      	movl	$0x0, 0x270(%rdi)
 2d02170:      	movl	0x2a0(%rdi), %ebx
 2d02176:      	testq	%rbx, %rbx
 2d02179:      	je	0x2d021a6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ff6>
 2d0217b:      	movq	0x298(%rdi), %r14
 2d02182:      	shlq	$0x3, %rbx
 2d02186:      	xorl	%r15d, %r15d
 2d02189:      	nopl	(%rax)
 2d02190:      	movq	(%r14,%r15), %rsi
 2d02194:      	callq	0x2d02970 <_ZNK12_GLOBAL__N_115ARMLoadStoreOpt23MergeBaseUpdateLSDoubleERN4llvm12MachineInstrE>
 2d02199:      	movq	(%rsp), %rdi
 2d0219d:      	addq	$0x8, %r15
 2d021a1:      	cmpq	%r15, %rbx
 2d021a4:      	jne	0x2d02190 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fe0>
 2d021a6:      	movl	$0x0, 0x2a0(%rdi)
 2d021b0:      	movq	0x238(%rsp), %rdi
 2d021b8:      	leaq	0x248(%rsp), %rax
 2d021c0:      	cmpq	%rax, %rdi
 2d021c3:      	je	0x2d021ca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x501a>
 2d021c5:      	callq	0x828a640 <free@plt>
 2d021ca:      	movq	%r12, %rax
 2d021cd:      	andb	$0x1, %al
 2d021cf:      	addq	$0x2c8, %rsp            # imm = 0x2C8
 2d021d6:      	popq	%rbx
 2d021d7:      	popq	%r12
 2d021d9:      	popq	%r13
 2d021db:      	popq	%r14
 2d021dd:      	popq	%r15
 2d021df:      	popq	%rbp
 2d021e0:      	retq
 2d021e1:      	movq	%rbx, %r12
 2d021e4:      	jmp	0x2d0222a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x507a>
 2d021e6:      	nopw	%cs:(%rax,%rax)
 2d021f0:      	movq	%r12, %rdx
 2d021f3:      	subq	%rbx, %rdx
 2d021f6:      	movq	%rdx, %rax
 2d021f9:      	sarq	$0x3, %rax
 2d021fd:      	cmpq	$0x2, %rax
 2d02201:      	jl	0x2d02262 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50b2>
 2d02203:      	shlq	$0x3, %rax
 2d02207:      	subq	%rax, %rdi
 2d0220a:      	addq	$0x10, %rdi
 2d0220e:      	movq	%rbx, %rsi
 2d02211:      	callq	0x828abc0 <memmove@plt>
 2d02216:      	movq	%rbx, %rax
 2d02219:      	movq	%r15, (%rax)
 2d0221c:      	leaq	0x8(%r12), %r15
 2d02221:      	cmpq	%r13, %r15
 2d02224:      	je	0x2cfe667 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14b7>
 2d0222a:      	movq	%r12, %rdi
 2d0222d:      	movq	%r15, %r12
 2d02230:      	movq	(%r15), %r15
 2d02233:      	movq	(%rbx), %rsi
 2d02236:      	movl	0x38(%r15), %ecx
 2d0223a:      	cmpl	0x38(%rsi), %ecx
 2d0223d:      	jb	0x2d021f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5040>
 2d0223f:      	movq	(%rdi), %rdx
 2d02242:      	movq	%r12, %rax
 2d02245:      	cmpl	0x38(%rdx), %ecx
 2d02248:      	jae	0x2d02219 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d0224a:      	movq	%r12, %rax
 2d0224d:      	nopl	(%rax)
 2d02250:      	movq	%rdx, (%rax)
 2d02253:      	movq	-0x10(%rax), %rdx
 2d02257:      	addq	$-0x8, %rax
 2d0225b:      	cmpl	0x38(%rdx), %ecx
 2d0225e:      	jb	0x2d02250 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50a0>
 2d02260:      	jmp	0x2d02219 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d02262:      	movq	%rbx, %rax
 2d02265:      	cmpq	$0x8, %rdx
 2d02269:      	jne	0x2d02219 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d0226b:      	movq	%rsi, 0x8(%rdi)
 2d0226f:      	jmp	0x2d02216 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5066>
 2d02271:      	movq	%rdx, 0x8(%rcx)
 2d02275:      	nopw	%cs:(%rax,%rax)
 2d0227f:      	nop
 2d02280:      	movq	%rbx, %rcx
 2d02283:      	movq	%r14, (%rcx)
 2d02286:      	addq	$0x8, %r12
 2d0228a:      	addq	$0x8, %r13
 2d0228e:      	cmpq	$0x80, %r12
 2d02295:      	je	0x2d022f2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5142>
 2d02297:      	movq	%rbp, %rcx
 2d0229a:      	leaq	(%rbx,%r12), %rbp
 2d0229e:      	movq	(%rbx,%r12), %r14
 2d022a2:      	movq	(%rbx), %rdx
 2d022a5:      	movl	0x38(%r14), %eax
 2d022a9:      	cmpl	0x38(%rdx), %eax
 2d022ac:      	jae	0x2d022d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5120>
 2d022ae:      	cmpq	$0x9, %r12
 2d022b2:      	jb	0x2d02271 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50c1>
 2d022b4:      	movq	%r15, %rdi
 2d022b7:      	movq	%rbx, %rsi
 2d022ba:      	movq	%r12, %rdx
 2d022bd:      	callq	0x828abc0 <memmove@plt>
 2d022c2:      	jmp	0x2d02280 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d0>
 2d022c4:      	nopw	%cs:(%rax,%rax)
 2d022ce:      	nop
 2d022d0:      	movq	(%rcx), %rdx
 2d022d3:      	movq	%rbp, %rcx
 2d022d6:      	cmpl	0x38(%rdx), %eax
 2d022d9:      	jae	0x2d02283 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d3>
 2d022db:      	movq	%r13, %rcx
 2d022de:      	nop
 2d022e0:      	movq	%rdx, (%rcx)
 2d022e3:      	movq	-0x10(%rcx), %rdx
 2d022e7:      	addq	$-0x8, %rcx
 2d022eb:      	cmpl	0x38(%rdx), %eax
 2d022ee:      	jb	0x2d022e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5130>
 2d022f0:      	jmp	0x2d02283 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d3>
 2d022f2:      	subq	$-0x80, %rbx
 2d022f6:      	movq	0x18(%rsp), %rdi
 2d022fb:      	jmp	0x2d02310 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5160>
 2d022fd:      	nopl	(%rax)
 2d02300:      	movq	%rax, (%rsi)
 2d02303:      	addq	$0x8, %rbx
 2d02307:      	cmpq	%rdi, %rbx
 2d0230a:      	je	0x2cfe667 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14b7>
 2d02310:      	movq	-0x8(%rbx), %rcx
 2d02314:      	movq	(%rbx), %rax
 2d02317:      	movl	0x38(%rax), %edx
 2d0231a:      	movq	%rbx, %rsi
 2d0231d:      	cmpl	0x38(%rcx), %edx
 2d02320:      	jae	0x2d02300 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5150>
 2d02322:      	movq	%rbx, %rsi
 2d02325:      	nopw	%cs:(%rax,%rax)
 2d0232f:      	nop
 2d02330:      	movq	%rcx, (%rsi)
 2d02333:      	movq	-0x10(%rsi), %rcx
 2d02337:      	addq	$-0x8, %rsi
 2d0233b:      	cmpl	0x38(%rcx), %edx
 2d0233e:      	jb	0x2d02330 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5180>
 2d02340:      	jmp	0x2d02300 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5150>
