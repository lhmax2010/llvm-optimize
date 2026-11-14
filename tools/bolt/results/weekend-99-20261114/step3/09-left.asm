
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002cfd210 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE>:
 2cfd210:      	pushq	%rbp
 2cfd211:      	pushq	%r15
 2cfd213:      	pushq	%r14
 2cfd215:      	pushq	%r13
 2cfd217:      	pushq	%r12
 2cfd219:      	pushq	%rbx
 2cfd21a:      	subq	$0x2c8, %rsp            # imm = 0x2C8
 2cfd221:      	leaq	0x248(%rsp), %rax
 2cfd229:      	movq	%rax, 0x238(%rsp)
 2cfd231:      	movabsq	$0x800000000, %rax      # imm = 0x800000000
 2cfd23b:      	movq	%rax, 0x240(%rsp)
 2cfd243:      	movb	$0x0, 0x200(%rdi)
 2cfd24a:      	leaq	0x30(%rsi), %r10
 2cfd24e:      	movq	%rsi, 0x18(%rsp)
 2cfd253:      	cmpq	0x38(%rsi), %r10
 2cfd257:      	movq	%rdi, (%rsp)
 2cfd25b:      	je	0x2cfe669 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1459>
 2cfd261:      	leaq	0x298(%rdi), %rax
 2cfd268:      	movq	%rax, 0x1f8(%rsp)
 2cfd270:      	leaq	0x2a8(%rdi), %rax
 2cfd277:      	movq	%rax, 0x220(%rsp)
 2cfd27f:      	movl	$0xe, 0x118(%rsp)
 2cfd28a:      	movl	$0xffffffff, 0x180(%rsp) # imm = 0xFFFFFFFF
 2cfd295:      	movq	$0x0, 0x80(%rsp)
 2cfd2a1:      	xorl	%r9d, %r9d
 2cfd2a4:      	jmp	0x2cfd2cb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbb>
 2cfd2a6:      	nopw	%cs:(%rax,%rax)
 2cfd2b0:      	movq	%rbp, %r15
 2cfd2b3:      	movl	%ebx, %r12d
 2cfd2b6:      	movl	%r12d, %r9d
 2cfd2b9:      	movq	%r15, %r10
 2cfd2bc:      	movq	0x18(%rsp), %rax
 2cfd2c1:      	cmpq	0x38(%rax), %r15
 2cfd2c5:      	je	0x2cfe64e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x143e>
 2cfd2cb:      	movq	(%r10), %r15
 2cfd2ce:      	andq	$-0x8, %r15
 2cfd2d2:      	testb	$0x4, (%r15)
 2cfd2d6:      	jne	0x2cfd2f5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe5>
 2cfd2d8:      	nopl	(%rax,%rax)
 2cfd2e0:      	testb	$0x4, 0x2c(%r15)
 2cfd2e5:      	je	0x2cfd2f5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe5>
 2cfd2e7:      	movq	(%r15), %r15
 2cfd2ea:      	andq	$-0x8, %r15
 2cfd2ee:      	testb	$0x4, 0x2c(%r15)
 2cfd2f3:      	jne	0x2cfd2e7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd7>
 2cfd2f5:      	movzwl	0x44(%r15), %edx
 2cfd2fa:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd300:      	je	0x2cfd316 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x106>
 2cfd302:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd308:      	je	0x2cfd316 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x106>
 2cfd30a:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd310:      	jne	0x2cfd44d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23d>
 2cfd316:      	movq	%r10, 0x8(%rsp)
 2cfd31b:      	movq	%r9, 0x90(%rsp)
 2cfd323:      	movq	0x20(%r15), %rax
 2cfd327:      	movl	0x44(%rax), %r13d
 2cfd32b:      	movl	0x4(%rax), %ebx
 2cfd32e:      	movq	%rax, 0x98(%rsp)
 2cfd336:      	movl	0x24(%rax), %r14d
 2cfd33a:      	movq	%rdi, %rbp
 2cfd33d:      	movq	0x48(%rdi), %rdi
 2cfd341:      	movq	(%rdi), %rax
 2cfd344:      	xorl	%r12d, %r12d
 2cfd347:      	movl	%ebx, %esi
 2cfd349:      	movl	%edx, 0x10(%rsp)
 2cfd34d:      	xorl	%edx, %edx
 2cfd34f:      	callq	*0x10(%rax)
 2cfd352:      	movq	%rax, 0x20(%rsp)
 2cfd357:      	movq	0x48(%rbp), %rdi
 2cfd35b:      	movq	(%rdi), %rax
 2cfd35e:      	movl	%r14d, 0x120(%rsp)
 2cfd366:      	movl	%r14d, %esi
 2cfd369:      	movq	%r13, %r14
 2cfd36c:      	xorl	%edx, %edx
 2cfd36e:      	callq	*0x10(%rax)
 2cfd371:      	movl	0x10(%rsp), %edx
 2cfd375:      	movq	%rax, %r8
 2cfd378:      	movq	%rbx, 0x78(%rsp)
 2cfd37d:      	cmpl	%r14d, %ebx
 2cfd380:      	jne	0x2cfd3a9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x199>
 2cfd382:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd388:      	je	0x2cfd396 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x186>
 2cfd38a:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd390:      	jne	0x2cfd542 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x332>
 2cfd396:      	movq	(%rsp), %rax
 2cfd39a:      	movq	0x50(%rax), %rax
 2cfd39e:      	cmpl	$0xe, 0x1c0(%rax)
 2cfd3a5:      	sete	%r12b
 2cfd3a9:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd3af:      	je	0x2cfd3b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a9>
 2cfd3b1:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd3b7:      	jne	0x2cfd430 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x220>
 2cfd3b9:      	movq	0x20(%rsp), %rcx
 2cfd3be:      	movl	%ecx, %eax
 2cfd3c0:      	andl	$0x1, %eax
 2cfd3c3:      	incl	%ecx
 2cfd3c5:      	xorl	%r8d, %ecx
 2cfd3c8:      	orl	%eax, %ecx
 2cfd3ca:      	setne	%al
 2cfd3cd:      	movq	0x8(%rsp), %r10
 2cfd3d2:      	orb	%al, %r12b
 2cfd3d5:      	cmpb	$0x1, %r12b
 2cfd3d9:      	jne	0x2cfd440 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x230>
 2cfd3db:      	movzwl	%dx, %eax
 2cfd3de:      	cmpl	$0x3ba, %eax            # imm = 0x3BA
 2cfd3e3:      	sete	%sil
 2cfd3e7:      	movl	%eax, 0xc0(%rsp)
 2cfd3ee:      	cmpl	$0x102f, %eax           # imm = 0x102F
 2cfd3f3:      	sete	%dil
 2cfd3f7:      	movq	0x20(%r15), %rbp
 2cfd3fb:      	movl	(%rbp), %r13d
 2cfd3ff:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd405:      	je	0x2cfd413 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x203>
 2cfd407:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd40d:      	jne	0x2cfd556 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x346>
 2cfd413:      	movl	%r13d, %eax
 2cfd416:      	notl	%eax
 2cfd418:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfd41d:      	sete	%al
 2cfd420:      	movl	%eax, 0xe8(%rsp)
 2cfd427:      	jmp	0x2cfd571 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x361>
 2cfd42c:      	nopl	(%rax)
 2cfd430:      	xorl	%eax, %eax
 2cfd432:      	movq	0x8(%rsp), %r10
 2cfd437:      	orb	%al, %r12b
 2cfd43a:      	cmpb	$0x1, %r12b
 2cfd43e:      	je	0x2cfd3db <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb>
 2cfd440:      	movzwl	0x44(%r15), %edx
 2cfd445:      	movq	0x90(%rsp), %r9
 2cfd44d:      	leal	0x1(%r9), %r12d
 2cfd451:      	movzwl	%dx, %r14d
 2cfd455:      	cmpl	$0x104b, %r14d          # imm = 0x104B
 2cfd45c:      	jle	0x2cfd490 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x280>
 2cfd45e:      	leal	-0x117a(%r14), %eax
 2cfd465:      	cmpl	$0x1f, %eax
 2cfd468:      	jbe	0x2cfd4b6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a6>
 2cfd46a:      	leal	-0x110f(%r14), %eax
 2cfd471:      	cmpl	$0x2, %eax
 2cfd474:      	jb	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd476:      	leal	-0x104c(%r14), %eax
 2cfd47d:      	cmpl	$0x1, %eax
 2cfd480:      	jbe	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd482:      	jmp	0x2cfd530 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x320>
 2cfd487:      	nopw	(%rax,%rax)
 2cfd490:      	cmpl	$0xb52, %r14d           # imm = 0xB52
 2cfd497:      	jg	0x2cfd515 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x305>
 2cfd499:      	cmpl	$0x3d7, %r14d           # imm = 0x3D7
 2cfd4a0:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4a2:      	cmpl	$0x7f9, %r14d           # imm = 0x7F9
 2cfd4a9:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4ab:      	cmpl	$0xb51, %r14d           # imm = 0xB51
 2cfd4b2:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd4b4:      	jmp	0x2cfd530 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x320>
 2cfd4b6:      	movl	$0xa0000009, %ecx       # imm = 0xA0000009
 2cfd4bb:      	btl	%eax, %ecx
 2cfd4be:      	jae	0x2cfd46a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25a>
 2cfd4c0:      	movq	0x20(%r15), %rax
 2cfd4c4:      	cmpb	$0x0, 0x20(%rax)
 2cfd4c8:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4ce:      	movq	0x30(%r15), %rcx
 2cfd4d2:      	cmpq	$0x8, %rcx
 2cfd4d6:      	jb	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4dc:      	movl	%edx, %r13d
 2cfd4df:      	movq	%rcx, %rdx
 2cfd4e2:      	andq	$0x7, %rdx
 2cfd4e6:      	je	0x2cfdd34 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb24>
 2cfd4ec:      	cmpl	$0x3, %edx
 2cfd4ef:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd4f5:      	andq	$-0x8, %rcx
 2cfd4f9:      	cmpl	$0x1, (%rcx)
 2cfd4fc:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd502:      	movq	0x10(%rcx), %rcx
 2cfd506:      	testb	$0x4, 0x20(%rcx)
 2cfd50a:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd510:      	jmp	0x2cfdd42 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb32>
 2cfd515:      	cmpl	$0xb53, %r14d           # imm = 0xB53
 2cfd51c:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd51e:      	cmpl	$0xf2e, %r14d           # imm = 0xF2E
 2cfd525:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd527:      	cmpl	$0xf30, %r14d           # imm = 0xF30
 2cfd52e:      	je	0x2cfd4c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b0>
 2cfd530:      	addl	$-0xe, %edx
 2cfd533:      	cmpw	$0x5, %dx
 2cfd537:      	jb	0x2cfe0d5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfd53d:      	jmp	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfd542:      	xorl	%r12d, %r12d
 2cfd545:      	cmpl	$0x7e7, %edx            # imm = 0x7E7
 2cfd54b:      	jne	0x2cfd3b1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a1>
 2cfd551:      	jmp	0x2cfd3b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a9>
 2cfd556:      	movl	%r13d, %eax
 2cfd559:      	shrl	$0x1a, %eax
 2cfd55c:      	xorl	%ecx, %ecx
 2cfd55e:      	testl	$0x1000000, %r13d       # imm = 0x1000000
 2cfd565:      	sete	%cl
 2cfd568:      	andl	%eax, %ecx
 2cfd56a:      	movl	%ecx, 0xe8(%rsp)
 2cfd571:      	movq	0x98(%rsp), %r9
 2cfd579:      	movl	0x20(%rbp), %ecx
 2cfd57c:      	cmpl	$0x102f, %edx           # imm = 0x102F
 2cfd582:      	movq	%r14, 0x28(%rsp)
 2cfd587:      	movb	%sil, 0x230(%rsp)
 2cfd58f:      	movb	%dil, 0x228(%rsp)
 2cfd597:      	movq	%r8, 0x88(%rsp)
 2cfd59f:      	je	0x2cfd5a9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x399>
 2cfd5a1:      	cmpl	$0x3ba, %edx            # imm = 0x3BA
 2cfd5a7:      	jne	0x2cfd5be <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ae>
 2cfd5a9:      	movl	%ecx, %r12d
 2cfd5ac:      	movl	%ecx, %eax
 2cfd5ae:      	notl	%eax
 2cfd5b0:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfd5b5:      	sete	%al
 2cfd5b8:      	movl	%eax, 0x8(%rsp)
 2cfd5bc:      	jmp	0x2cfd5d7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c7>
 2cfd5be:      	movl	%ecx, %eax
 2cfd5c0:      	shrl	$0x1a, %eax
 2cfd5c3:      	xorl	%edx, %edx
 2cfd5c5:      	movl	%ecx, %r12d
 2cfd5c8:      	testl	$0x1000000, %ecx        # imm = 0x1000000
 2cfd5ce:      	sete	%dl
 2cfd5d1:      	andl	%eax, %edx
 2cfd5d3:      	movl	%edx, 0x8(%rsp)
 2cfd5d7:      	movl	0x40(%r9), %eax
 2cfd5db:      	movq	%rax, %r14
 2cfd5de:      	testl	$0x1000000, %eax        # imm = 0x1000000
 2cfd5e3:      	sete	%bl
 2cfd5e6:      	movq	%r15, %rdi
 2cfd5e9:      	callq	0x2cf7a90 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfd5ee:      	movq	0x10(%r15), %r9
 2cfd5f2:      	movl	$0xe, %r8d
 2cfd5f8:      	xorl	%r10d, %r10d
 2cfd5fb:      	testb	$0x40, 0x12(%r9)
 2cfd600:      	jne	0x2cfd619 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x409>
 2cfd602:      	leaq	0x30(%rsp), %rdi
 2cfd607:      	xorl	%esi, %esi
 2cfd609:      	movl	%r12d, %r11d
 2cfd60c:      	movq	%r14, %r12
 2cfd60f:      	movq	0x28(%rsp), %r9
 2cfd614:      	jmp	0x2cfd6b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4a0>
 2cfd619:      	movl	%eax, %r10d
 2cfd61c:      	movzwl	0x28(%r15), %edx
 2cfd621:      	movzbl	0x2a(%r15), %ecx
 2cfd626:      	shll	$0x10, %ecx
 2cfd629:      	orl	%edx, %ecx
 2cfd62b:      	testl	%ecx, %ecx
 2cfd62d:      	leaq	0x30(%rsp), %rdi
 2cfd632:      	movl	%r12d, %r11d
 2cfd635:      	je	0x2cfd685 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x475>
 2cfd637:      	movzwl	(%r9), %edx
 2cfd63b:      	movzwl	0xa(%r9), %esi
 2cfd640:      	addq	$0x10, %rbp
 2cfd644:      	addl	%ecx, %ecx
 2cfd646:      	leaq	(%rcx,%rcx,2), %rcx
 2cfd64a:      	shll	$0x5, %edx
 2cfd64d:      	leaq	(%rsi,%rsi,2), %rsi
 2cfd651:      	leaq	(%rdx,%rsi,2), %rdx
 2cfd655:      	leaq	0x22(%r9,%rdx), %rax
 2cfd65a:      	xorl	%edx, %edx
 2cfd65c:      	xorl	%esi, %esi
 2cfd65e:      	movq	%r14, %r12
 2cfd661:      	movq	0x28(%rsp), %r9
 2cfd666:      	nopw	%cs:(%rax,%rax)
 2cfd670:      	testb	$0x2, (%rax,%rdx)
 2cfd674:      	jne	0x2cfd697 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x487>
 2cfd676:      	addq	$0x20, %rbp
 2cfd67a:      	addq	$0x6, %rdx
 2cfd67e:      	cmpq	%rdx, %rcx
 2cfd681:      	jne	0x2cfd670 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x460>
 2cfd683:      	jmp	0x2cfd68f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47f>
 2cfd685:      	xorl	%esi, %esi
 2cfd687:      	movq	%r14, %r12
 2cfd68a:      	movq	0x28(%rsp), %r9
 2cfd68f:      	movl	%r10d, %eax
 2cfd692:      	xorl	%r10d, %r10d
 2cfd695:      	jmp	0x2cfd6b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4a0>
 2cfd697:      	movl	(%rbp), %r8d
 2cfd69b:      	movl	0x14(%rbp), %ecx
 2cfd69e:      	movl	%r10d, %eax
 2cfd6a1:      	movq	%rcx, %r10
 2cfd6a4:      	nopw	%cs:(%rax,%rax)
 2cfd6ae:      	nop
 2cfd6b0:      	andl	$0x10000000, %r13d      # imm = 0x10000000
 2cfd6b7:      	andl	$0x10000000, %r11d      # imm = 0x10000000
 2cfd6be:      	movl	%r12d, %ecx
 2cfd6c1:      	shrl	$0x1a, %ecx
 2cfd6c4:      	movb	%bl, %sil
 2cfd6c7:      	andl	%ecx, %esi
 2cfd6c9:      	movq	0x88(%rsp), %rcx
 2cfd6d1:      	cmpl	0x20(%rsp), %ecx
 2cfd6d5:      	movl	0x10(%rsp), %ecx
 2cfd6d9:      	movq	%r8, 0x98(%rsp)
 2cfd6e1:      	jbe	0x2cfd946 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x736>
 2cfd6e7:      	testl	%eax, %eax
 2cfd6e9:      	jne	0x2cfd946 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x736>
 2cfd6ef:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd6f5:      	je	0x2cfd704 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f4>
 2cfd6f7:      	movl	$0x7db, %ebx            # imm = 0x7DB
 2cfd6fc:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd702:      	jne	0x2cfd71d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d>
 2cfd704:      	cmpl	$0x102f, 0xc0(%rsp)     # imm = 0x102F
 2cfd70f:      	movl	$0x3ae, %ebx            # imm = 0x3AE
 2cfd714:      	movl	$0x1024, %eax           # imm = 0x1024
 2cfd719:      	cmoveq	%rax, %rbx
 2cfd71d:      	movq	%rsi, %rbp
 2cfd720:      	movq	%r10, 0x70(%rsp)
 2cfd725:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd72b:      	je	0x2cfd739 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x529>
 2cfd72d:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd733:      	jne	0x2cfdb1f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x90f>
 2cfd739:      	movq	0x38(%r15), %rsi
 2cfd73d:      	movq	%rsi, 0xa0(%rsp)
 2cfd745:      	movq	%rdi, %r14
 2cfd748:      	testq	%rsi, %rsi
 2cfd74b:      	je	0x2cfd786 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x576>
 2cfd74d:      	movl	$0x1, %edx
 2cfd752:      	leaq	0xa0(%rsp), %rdi
 2cfd75a:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfd75f:      	movq	0xa0(%rsp), %rsi
 2cfd767:      	movq	%rsi, 0x30(%rsp)
 2cfd76c:      	testq	%rsi, %rsi
 2cfd76f:      	je	0x2cfd78d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x57d>
 2cfd771:      	leaq	0xa0(%rsp), %r14
 2cfd779:      	movq	%r14, %rdi
 2cfd77c:      	leaq	0x30(%rsp), %rdx
 2cfd781:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cfd786:      	movq	$0x0, (%r14)
 2cfd78d:      	leaq	0x38(%rsp), %rax
 2cfd792:      	xorps	%xmm0, %xmm0
 2cfd795:      	movups	%xmm0, (%rax)
 2cfd798:      	movq	$0x0, 0x10(%rax)
 2cfd7a0:      	movq	(%rsp), %rax
 2cfd7a4:      	movq	0x40(%rax), %rax
 2cfd7a8:      	movq	0x8(%rax), %rcx
 2cfd7ac:      	shll	$0x5, %ebx
 2cfd7af:      	subq	%rbx, %rcx
 2cfd7b2:      	movq	0x18(%rsp), %rdi
 2cfd7b7:      	movq	%r15, %rsi
 2cfd7ba:      	leaq	0x30(%rsp), %r13
 2cfd7bf:      	movq	%r13, %rdx
 2cfd7c2:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cfd7c7:      	movq	%rax, %r14
 2cfd7ca:      	movq	%rdx, %r12
 2cfd7cd:      	movq	$0x0, 0x138(%rsp)
 2cfd7d9:      	shll	$0x1a, %ebp
 2cfd7dc:      	movq	0x28(%rsp), %rax
 2cfd7e1:      	movl	%eax, 0x134(%rsp)
 2cfd7e8:      	leaq	0x140(%rsp), %rbx
 2cfd7f0:      	xorps	%xmm0, %xmm0
 2cfd7f3:      	movups	%xmm0, (%rbx)
 2cfd7f6:      	movl	%ebp, 0x130(%rsp)
 2cfd7fd:      	movq	%rdx, %rdi
 2cfd800:      	movq	%r14, %rsi
 2cfd803:      	leaq	0x130(%rsp), %rbp
 2cfd80b:      	movq	%rbp, %rdx
 2cfd80e:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd813:      	movl	0x98(%rsp), %eax
 2cfd81a:      	movl	$0x1, 0x130(%rsp)
 2cfd825:      	movq	$0x0, 0x138(%rsp)
 2cfd831:      	movq	%rax, 0x140(%rsp)
 2cfd839:      	movq	%r12, %rdi
 2cfd83c:      	movq	%r14, %rsi
 2cfd83f:      	movq	%rbp, %rdx
 2cfd842:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd847:      	movq	$0x0, 0x138(%rsp)
 2cfd853:      	movq	0x70(%rsp), %rax
 2cfd858:      	movl	%eax, 0x134(%rsp)
 2cfd85f:      	xorps	%xmm0, %xmm0
 2cfd862:      	movups	%xmm0, (%rbx)
 2cfd865:      	movl	$0x0, 0x130(%rsp)
 2cfd870:      	movq	%r12, %rdi
 2cfd873:      	movq	%r14, %rsi
 2cfd876:      	movq	%rbp, %rdx
 2cfd879:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd87e:      	movq	$0x0, 0x138(%rsp)
 2cfd88a:      	movq	0x78(%rsp), %rax
 2cfd88f:      	movl	%eax, 0x134(%rsp)
 2cfd896:      	movzbl	0xe8(%rsp), %eax
 2cfd89e:      	shll	$0x1a, %eax
 2cfd8a1:      	orl	$0x1000000, %eax        # imm = 0x1000000
 2cfd8a6:      	xorps	%xmm0, %xmm0
 2cfd8a9:      	movups	%xmm0, (%rbx)
 2cfd8ac:      	movl	%eax, 0x130(%rsp)
 2cfd8b3:      	movq	%r12, %rdi
 2cfd8b6:      	movq	%r14, %rsi
 2cfd8b9:      	movq	%rbp, %rdx
 2cfd8bc:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd8c1:      	movq	$0x0, 0x138(%rsp)
 2cfd8cd:      	movl	0x120(%rsp), %eax
 2cfd8d4:      	movl	%eax, 0x134(%rsp)
 2cfd8db:      	movzbl	0x8(%rsp), %eax
 2cfd8e0:      	shll	$0x1a, %eax
 2cfd8e3:      	orl	$0x1000000, %eax        # imm = 0x1000000
 2cfd8e8:      	xorps	%xmm0, %xmm0
 2cfd8eb:      	movups	%xmm0, (%rbx)
 2cfd8ee:      	movl	%eax, 0x130(%rsp)
 2cfd8f5:      	movq	%r12, %rdi
 2cfd8f8:      	movq	%r14, %rsi
 2cfd8fb:      	movq	%rbp, %rdx
 2cfd8fe:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfd903:      	movq	%r12, %rdi
 2cfd906:      	movq	%r14, %rsi
 2cfd909:      	movq	%r15, %rdx
 2cfd90c:      	callq	0x3651d90 <_ZN4llvm12MachineInstr12cloneMemRefsERNS_15MachineFunctionERKS0_>
 2cfd911:      	movq	0x30(%rsp), %rsi
 2cfd916:      	testq	%rsi, %rsi
 2cfd919:      	je	0x2cfd923 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x713>
 2cfd91b:      	movq	%r13, %rdi
 2cfd91e:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfd923:      	movq	0xa0(%rsp), %rsi
 2cfd92b:      	testq	%rsi, %rsi
 2cfd92e:      	je	0x2cfe089 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfd934:      	leaq	0xa0(%rsp), %rdi
 2cfd93c:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfd941:      	jmp	0x2cfe089 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfd946:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd94c:      	movq	0x78(%rsp), %rbx
 2cfd951:      	movq	%rsi, 0xe0(%rsp)
 2cfd959:      	je	0x2cfd963 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x753>
 2cfd95b:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd961:      	jne	0x2cfd9ab <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x79b>
 2cfd963:      	movl	0xc0(%rsp), %ecx
 2cfd96a:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd970:      	jne	0x2cfd97f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x76f>
 2cfd972:      	movl	%eax, %ecx
 2cfd974:      	shrl	$0x1f, %ecx
 2cfd977:      	orl	$0x104c, %ecx           # imm = 0x104C
 2cfd97d:      	jmp	0x2cfd9c9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x7b9>
 2cfd97f:      	movl	%eax, %r14d
 2cfd982:      	movl	$0x7f9, %edx            # imm = 0x7F9
 2cfd987:      	movl	$0x3d7, %r8d            # imm = 0x3D7
 2cfd98d:      	movl	$0x3d7, 0x10(%rsp)      # imm = 0x3D7
 2cfd995:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfd99b:      	jne	0x2cfdf69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd59>
 2cfd9a1:      	cmpl	%r9d, %ebx
 2cfd9a4:      	jne	0x2cfd9ea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x7da>
 2cfd9a6:      	jmp	0x2cfda7a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfd9ab:      	movl	0xc0(%rsp), %ecx
 2cfd9b2:      	cmpl	$0x102f, %ecx           # imm = 0x102F
 2cfd9b8:      	jne	0x2cfdf4b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd3b>
 2cfd9be:      	movl	%eax, %ecx
 2cfd9c0:      	shrl	$0x1f, %ecx
 2cfd9c3:      	addl	$0x110f, %ecx           # imm = 0x110F
 2cfd9c9:      	movl	%ecx, 0x10(%rsp)
 2cfd9cd:      	xorl	%r8d, %r8d
 2cfd9d0:      	movl	%eax, %r14d
 2cfd9d3:      	cmpl	$-0x4, %eax
 2cfd9d6:      	setl	%r8b
 2cfd9da:      	orl	$0x104c, %r8d           # imm = 0x104C
 2cfd9e1:      	cmpl	%r9d, %ebx
 2cfd9e4:      	je	0x2cfda7a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfd9ea:      	leal	-0x1(%rbx), %eax
 2cfd9ed:      	cmpl	$0x3fffffff, %eax       # imm = 0x3FFFFFFF
 2cfd9f2:      	setae	%al
 2cfd9f5:      	leal	-0x1(%r9), %ecx
 2cfd9f9:      	cmpl	$0x3fffffff, %ecx       # imm = 0x3FFFFFFF
 2cfd9ff:      	setae	%cl
 2cfda02:      	orb	%al, %cl
 2cfda04:      	jne	0x2cfda72 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x862>
 2cfda06:      	movq	(%rsp), %rax
 2cfda0a:      	movq	0x48(%rax), %rax
 2cfda0e:      	leaq	(%rbx,%rbx,2), %rcx
 2cfda12:      	movq	0x8(%rax), %rdx
 2cfda16:      	movq	0x38(%rax), %rsi
 2cfda1a:      	movl	0x10(%rdx,%rcx,8), %ecx
 2cfda1e:      	movl	%ecx, %eax
 2cfda20:      	andl	$0xfff, %eax            # imm = 0xFFF
 2cfda25:      	shrl	$0xc, %ecx
 2cfda28:      	leaq	(%rsi,%rcx,2), %rcx
 2cfda2c:      	leaq	(%r9,%r9,2), %rdi
 2cfda30:      	movl	0x10(%rdx,%rdi,8), %edi
 2cfda34:      	movl	%edi, %edx
 2cfda36:      	andl	$0xfff, %edx            # imm = 0xFFF
 2cfda3c:      	shrl	$0xc, %edi
 2cfda3f:      	leaq	(%rsi,%rdi,2), %rsi
 2cfda43:      	nopw	%cs:(%rax,%rax)
 2cfda4d:      	nopl	(%rax)
 2cfda50:      	cmpl	%edx, %eax
 2cfda52:      	je	0x2cfda7a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x86a>
 2cfda54:      	jae	0x2cfda65 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x855>
 2cfda56:      	movswl	(%rcx), %edi
 2cfda59:      	addq	$0x2, %rcx
 2cfda5d:      	addl	%edi, %eax
 2cfda5f:      	testl	%edi, %edi
 2cfda61:      	jne	0x2cfda50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x840>
 2cfda63:      	jmp	0x2cfda72 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x862>
 2cfda65:      	movswl	(%rsi), %edi
 2cfda68:      	addq	$0x2, %rsi
 2cfda6c:      	addl	%edi, %edx
 2cfda6e:      	testl	%edi, %edi
 2cfda70:      	jne	0x2cfda50 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x840>
 2cfda72:      	movl	%r8d, %edx
 2cfda75:      	jmp	0x2cfdf69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xd59>
 2cfda7a:      	shrl	$0x1c, %r12d
 2cfda7e:      	andl	$0x1, %r12d
 2cfda82:      	movl	%r14d, %edx
 2cfda85:      	addl	$0x4, %edx
 2cfda88:      	subq	$0x8, %rsp
 2cfda8c:      	movzbl	0x10(%rsp), %eax
 2cfda91:      	movq	%r12, %r13
 2cfda94:      	movq	%r12, 0x28(%rsp)
 2cfda99:      	movq	0x20(%rsp), %r12
 2cfda9e:      	movq	%r12, %rdi
 2cfdaa1:      	movq	%r15, %rsi
 2cfdaa4:      	movl	$0x1, %ecx
 2cfdaa9:      	movq	%r9, %r11
 2cfdaac:      	movl	0x128(%rsp), %r9d
 2cfdab4:      	pushq	%r15
 2cfdab6:      	movq	0x10(%rsp), %rbx
 2cfdabb:      	pushq	0x40(%rbx)
 2cfdabe:      	pushq	%r10
 2cfdac0:      	movq	0xb8(%rsp), %rbp
 2cfdac8:      	pushq	%rbp
 2cfdac9:      	pushq	%r13
 2cfdacb:      	pushq	$0x0
 2cfdacd:      	pushq	%r11
 2cfdacf:      	pushq	$0x0
 2cfdad1:      	pushq	%rax
 2cfdad2:      	movq	%r10, %r13
 2cfdad5:      	callq	0x2d04a20 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfdada:      	addq	$0x48, %rsp
 2cfdade:      	movzbl	0xf0(%rsp), %eax
 2cfdae6:      	movq	%r12, %rdi
 2cfdae9:      	movq	%r15, %rsi
 2cfdaec:      	movl	%r14d, %edx
 2cfdaef:      	movl	$0x1, %ecx
 2cfdaf4:      	movl	0x18(%rsp), %r8d
 2cfdaf9:      	movq	0x80(%rsp), %r9
 2cfdb01:      	pushq	%r15
 2cfdb03:      	pushq	0x40(%rbx)
 2cfdb06:      	pushq	%r13
 2cfdb08:      	pushq	%rbp
 2cfdb09:      	pushq	0x48(%rsp)
 2cfdb0d:      	pushq	0x110(%rsp)
 2cfdb14:      	pushq	0x60(%rsp)
 2cfdb18:      	pushq	$0x0
 2cfdb1a:      	jmp	0x2cfe07f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe6f>
 2cfdb1f:      	movl	%r11d, 0x20(%rsp)
 2cfdb24:      	movl	%r13d, 0x10(%rsp)
 2cfdb29:      	movq	0x38(%r15), %rsi
 2cfdb2d:      	movq	%rsi, 0xf0(%rsp)
 2cfdb35:      	movq	%rdi, %r14
 2cfdb38:      	testq	%rsi, %rsi
 2cfdb3b:      	je	0x2cfdb76 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x966>
 2cfdb3d:      	movl	$0x1, %edx
 2cfdb42:      	leaq	0xf0(%rsp), %rdi
 2cfdb4a:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfdb4f:      	movq	0xf0(%rsp), %rsi
 2cfdb57:      	movq	%rsi, 0x30(%rsp)
 2cfdb5c:      	testq	%rsi, %rsi
 2cfdb5f:      	je	0x2cfdb7d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x96d>
 2cfdb61:      	leaq	0xf0(%rsp), %r14
 2cfdb69:      	movq	%r14, %rdi
 2cfdb6c:      	leaq	0x30(%rsp), %rdx
 2cfdb71:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cfdb76:      	movq	$0x0, (%r14)
 2cfdb7d:      	leaq	0x38(%rsp), %rax
 2cfdb82:      	xorps	%xmm0, %xmm0
 2cfdb85:      	movups	%xmm0, (%rax)
 2cfdb88:      	movq	$0x0, 0x10(%rax)
 2cfdb90:      	movq	(%rsp), %rax
 2cfdb94:      	movq	0x40(%rax), %rax
 2cfdb98:      	movq	0x8(%rax), %rcx
 2cfdb9c:      	shll	$0x5, %ebx
 2cfdb9f:      	subq	%rbx, %rcx
 2cfdba2:      	movq	0x18(%rsp), %rdi
 2cfdba7:      	movq	%r15, %rsi
 2cfdbaa:      	leaq	0x30(%rsp), %r13
 2cfdbaf:      	movq	%r13, %rdx
 2cfdbb2:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cfdbb7:      	movq	%rax, %r14
 2cfdbba:      	movq	%rdx, %r12
 2cfdbbd:      	movq	$0x0, 0x138(%rsp)
 2cfdbc9:      	shll	$0x1a, %ebp
 2cfdbcc:      	movq	0x28(%rsp), %rax
 2cfdbd1:      	movl	%eax, 0x134(%rsp)
 2cfdbd8:      	leaq	0x140(%rsp), %rbx
 2cfdbe0:      	xorps	%xmm0, %xmm0
 2cfdbe3:      	movups	%xmm0, (%rbx)
 2cfdbe6:      	movl	%ebp, 0x130(%rsp)
 2cfdbed:      	movq	%rdx, %rdi
 2cfdbf0:      	movq	%r14, %rsi
 2cfdbf3:      	leaq	0x130(%rsp), %rbp
 2cfdbfb:      	movq	%rbp, %rdx
 2cfdbfe:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc03:      	movl	0x98(%rsp), %eax
 2cfdc0a:      	movl	$0x1, 0x130(%rsp)
 2cfdc15:      	movq	$0x0, 0x138(%rsp)
 2cfdc21:      	movq	%rax, 0x140(%rsp)
 2cfdc29:      	movq	%r12, %rdi
 2cfdc2c:      	movq	%r14, %rsi
 2cfdc2f:      	movq	%rbp, %rdx
 2cfdc32:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc37:      	movq	$0x0, 0x138(%rsp)
 2cfdc43:      	movq	0x70(%rsp), %rax
 2cfdc48:      	movl	%eax, 0x134(%rsp)
 2cfdc4f:      	xorps	%xmm0, %xmm0
 2cfdc52:      	movups	%xmm0, (%rbx)
 2cfdc55:      	movl	$0x0, 0x130(%rsp)
 2cfdc60:      	movq	%r12, %rdi
 2cfdc63:      	movq	%r14, %rsi
 2cfdc66:      	movq	%rbp, %rdx
 2cfdc69:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdc6e:      	movq	$0x0, 0x138(%rsp)
 2cfdc7a:      	movzbl	0xe8(%rsp), %eax
 2cfdc82:      	shll	$0x1a, %eax
 2cfdc85:      	movq	0x78(%rsp), %rcx
 2cfdc8a:      	movl	%ecx, 0x134(%rsp)
 2cfdc91:      	orl	0x10(%rsp), %eax
 2cfdc95:      	xorps	%xmm0, %xmm0
 2cfdc98:      	movups	%xmm0, (%rbx)
 2cfdc9b:      	movl	%eax, 0x130(%rsp)
 2cfdca2:      	movq	%r12, %rdi
 2cfdca5:      	movq	%r14, %rsi
 2cfdca8:      	movq	%rbp, %rdx
 2cfdcab:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdcb0:      	movq	$0x0, 0x138(%rsp)
 2cfdcbc:      	movzbl	0x8(%rsp), %eax
 2cfdcc1:      	shll	$0x1a, %eax
 2cfdcc4:      	movl	0x120(%rsp), %ecx
 2cfdccb:      	movl	%ecx, 0x134(%rsp)
 2cfdcd2:      	orl	0x20(%rsp), %eax
 2cfdcd6:      	xorps	%xmm0, %xmm0
 2cfdcd9:      	movups	%xmm0, (%rbx)
 2cfdcdc:      	movl	%eax, 0x130(%rsp)
 2cfdce3:      	movq	%r12, %rdi
 2cfdce6:      	movq	%r14, %rsi
 2cfdce9:      	movq	%rbp, %rdx
 2cfdcec:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cfdcf1:      	movq	%r12, %rdi
 2cfdcf4:      	movq	%r14, %rsi
 2cfdcf7:      	movq	%r15, %rdx
 2cfdcfa:      	callq	0x3651d90 <_ZN4llvm12MachineInstr12cloneMemRefsERNS_15MachineFunctionERKS0_>
 2cfdcff:      	movq	0x30(%rsp), %rsi
 2cfdd04:      	testq	%rsi, %rsi
 2cfdd07:      	je	0x2cfdd11 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xb01>
 2cfdd09:      	movq	%r13, %rdi
 2cfdd0c:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfdd11:      	movq	0xf0(%rsp), %rsi
 2cfdd19:      	testq	%rsi, %rsi
 2cfdd1c:      	je	0x2cfe089 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfdd22:      	leaq	0xf0(%rsp), %rdi
 2cfdd2a:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cfdd2f:      	jmp	0x2cfe089 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xe79>
 2cfdd34:      	movq	%rcx, 0x30(%r15)
 2cfdd38:      	testb	$0x4, 0x20(%rcx)
 2cfdd3c:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd42:      	testb	$0xf, 0x25(%rcx)
 2cfdd46:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd4c:      	movzbl	0x22(%rcx), %edx
 2cfdd50:      	movq	0x8(%rcx), %rcx
 2cfdd54:      	btsq	%rdx, %rcx
 2cfdd58:      	movq	%rcx, %rdx
 2cfdd5b:      	negq	%rdx
 2cfdd5e:      	andq	%rcx, %rdx
 2cfdd61:      	movl	$0x7f, %ecx
 2cfdd66:      	bsrq	%rdx, %rcx
 2cfdd6a:      	xorl	$0x3e, %ecx
 2cfdd6d:      	andl	$-0x2, %ecx
 2cfdd70:      	cmpl	$0x3e, %ecx
 2cfdd73:      	je	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd79:      	movl	(%rax), %ecx
 2cfdd7b:      	movl	$0x100000ff, %edx       # imm = 0x100000FF
 2cfdd80:      	andl	%edx, %ecx
 2cfdd82:      	cmpl	$0x10000000, %ecx       # imm = 0x10000000
 2cfdd88:      	je	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd8e:      	testb	$0x10, 0x23(%rax)
 2cfdd92:      	jne	0x2cfdea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xc90>
 2cfdd98:      	movq	0x10(%r15), %rdx
 2cfdd9c:      	testb	$0x40, 0x12(%rdx)
 2cfdda0:      	movq	%r10, 0x8(%rsp)
 2cfdda5:      	je	0x2cfddf5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbe5>
 2cfdda7:      	movzwl	0x28(%r15), %ecx
 2cfddac:      	movzbl	0x2a(%r15), %esi
 2cfddb1:      	shll	$0x10, %esi
 2cfddb4:      	orl	%ecx, %esi
 2cfddb6:      	testl	%esi, %esi
 2cfddb8:      	je	0x2cfddf5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbe5>
 2cfddba:      	movzwl	(%rdx), %edi
 2cfddbd:      	movzwl	0xa(%rdx), %r8d
 2cfddc2:      	leaq	0x10(%rax), %rcx
 2cfddc6:      	addl	%esi, %esi
 2cfddc8:      	leaq	(%rsi,%rsi,2), %rsi
 2cfddcc:      	shll	$0x5, %edi
 2cfddcf:      	leaq	(%r8,%r8,2), %r8
 2cfddd3:      	leaq	(%rdi,%r8,2), %rdi
 2cfddd7:      	leaq	0x22(%rdx,%rdi), %rdx
 2cfdddc:      	xorl	%edi, %edi
 2cfddde:      	testb	$0x2, (%rdx,%rdi)
 2cfdde2:      	jne	0x2cfe302 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10f2>
 2cfdde8:      	addq	$0x20, %rcx
 2cfddec:      	addq	$0x6, %rdi
 2cfddf0:      	cmpq	%rdi, %rsi
 2cfddf3:      	jne	0x2cfddde <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbce>
 2cfddf5:      	movl	$0xe, %ebx
 2cfddfa:      	movq	%r9, %rbp
 2cfddfd:      	movl	0x4(%rax), %ecx
 2cfde00:      	movq	%rcx, 0x20(%rsp)
 2cfde05:      	movl	0x24(%rax), %eax
 2cfde08:      	movl	%eax, 0x10(%rsp)
 2cfde0c:      	movq	%r15, %rdi
 2cfde0f:      	callq	0x2cf7a90 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfde14:      	cmpl	$0x0, 0x80(%rsp)
 2cfde1c:      	je	0x2cfe2a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1094>
 2cfde22:      	cmpl	%r14d, 0x180(%rsp)
 2cfde2a:      	movq	(%rsp), %rdi
 2cfde2e:      	jne	0x2cfe457 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1247>
 2cfde34:      	movl	0x10(%rsp), %ecx
 2cfde38:      	cmpl	%ecx, 0x80(%rsp)
 2cfde3f:      	jne	0x2cfe457 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1247>
 2cfde45:      	cmpl	%ebx, 0x118(%rsp)
 2cfde4c:      	movq	%rbp, %rbx
 2cfde4f:      	jne	0x2cfe338 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1128>
 2cfde55:      	movzwl	%r13w, %ecx
 2cfde59:      	cmpl	$0x104b, %ecx           # imm = 0x104B
 2cfde5f:      	movq	0x8(%rsp), %rbp
 2cfde64:      	jle	0x2cfe342 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1132>
 2cfde6a:      	leal	-0x104c(%rcx), %edx
 2cfde70:      	cmpl	$0x2, %edx
 2cfde73:      	jb	0x2cfe35e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde79:      	cmpl	$0x117a, %ecx           # imm = 0x117A
 2cfde7f:      	je	0x2cfe35e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde85:      	cmpl	$0x117d, %ecx           # imm = 0x117D
 2cfde8b:      	je	0x2cfe35e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfde91:      	jmp	0x2cfe478 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1268>
 2cfde96:      	nopw	%cs:(%rax,%rax)
 2cfdea0:      	cmpl	$0x1101, %r14d          # imm = 0x1101
 2cfdea7:      	je	0x2cfdeb2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xca2>
 2cfdea9:      	cmpl	$0x102f, %r14d          # imm = 0x102F
 2cfdeb0:      	jne	0x2cfdef0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce0>
 2cfdeb2:      	movq	(%rsp), %rax
 2cfdeb6:      	movl	0x2a0(%rax), %edx
 2cfdebc:      	cmpl	0x2a4(%rax), %edx
 2cfdec2:      	jae	0x2cfe30c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10fc>
 2cfdec8:      	movq	0x298(%rax), %rax
 2cfdecf:      	movl	%edx, %ecx
 2cfded1:      	movq	%r15, (%rax,%rcx,8)
 2cfded5:      	movq	(%rsp), %rdi
 2cfded9:      	incl	0x2a0(%rdi)
 2cfdedf:      	movq	%r15, %rbp
 2cfdee2:      	movl	%r12d, %ebx
 2cfdee5:      	jmp	0x2cfdefa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfdee7:      	nopw	(%rax,%rax)
 2cfdef0:      	movq	%r15, %rbp
 2cfdef3:      	movl	%r12d, %ebx
 2cfdef6:      	movq	(%rsp), %rdi
 2cfdefa:      	cmpl	$0x0, 0x240(%rsp)
 2cfdf02:      	je	0x2cfd2b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa0>
 2cfdf08:      	leaq	0x238(%rsp), %rsi
 2cfdf10:      	callq	0x2d023b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt14FormCandidatesERKN4llvm11SmallVectorINS0_15MemOpQueueEntryELj8EEE>
 2cfdf15:      	movq	(%rsp), %rdi
 2cfdf19:      	movl	$0x0, 0x240(%rsp)
 2cfdf24:      	movq	$0x0, 0x80(%rsp)
 2cfdf30:      	movl	$0xffffffff, 0x180(%rsp) # imm = 0xFFFFFFFF
 2cfdf3b:      	movl	$0xe, 0x118(%rsp)
 2cfdf46:      	jmp	0x2cfd2b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa0>
 2cfdf4b:      	movl	%eax, %r14d
 2cfdf4e:      	cmpl	$0x3ba, %ecx            # imm = 0x3BA
 2cfdf54:      	movl	$0x7f9, 0x10(%rsp)      # imm = 0x7F9
 2cfdf5c:      	movl	$0x7f9, %edx            # imm = 0x7F9
 2cfdf61:      	movl	$0x3d7, %eax            # imm = 0x3D7
 2cfdf66:      	cmovel	%eax, %edx
 2cfdf69:      	movl	%edx, 0x88(%rsp)
 2cfdf70:      	movzbl	0x230(%rsp), %r8d
 2cfdf79:      	orb	0x228(%rsp), %r8b
 2cfdf81:      	shrl	$0x1c, %r12d
 2cfdf85:      	andl	$0x1, %r12d
 2cfdf89:      	movl	0xe8(%rsp), %esi
 2cfdf90:      	xorl	%eax, %eax
 2cfdf92:      	testl	%r11d, %r11d
 2cfdf95:      	setne	%al
 2cfdf98:      	movq	%rax, 0x20(%rsp)
 2cfdf9d:      	xorl	%eax, %eax
 2cfdf9f:      	testl	%r13d, %r13d
 2cfdfa2:      	setne	%al
 2cfdfa5:      	cmpl	%r9d, %ebx
 2cfdfa8:      	setne	%cl
 2cfdfab:      	movq	%r9, %r11
 2cfdfae:      	cmpl	%ebx, 0x120(%rsp)
 2cfdfb5:      	sete	%dl
 2cfdfb8:      	andb	%sil, %dl
 2cfdfbb:      	movl	0x8(%rsp), %edi
 2cfdfbf:      	orb	%dl, %dil
 2cfdfc2:      	movl	%edi, 0x8(%rsp)
 2cfdfc6:      	xorb	%sil, %dl
 2cfdfc9:      	andb	%cl, %dl
 2cfdfcb:      	subq	$0x8, %rsp
 2cfdfcf:      	movq	%r10, 0x78(%rsp)
 2cfdfd4:      	movzbl	%dl, %ecx
 2cfdfd7:      	movq	%rcx, 0xc8(%rsp)
 2cfdfdf:      	movzbl	%r8b, %ecx
 2cfdfe3:      	movl	%ecx, 0xf0(%rsp)
 2cfdfea:      	movq	0x20(%rsp), %rbp
 2cfdfef:      	movq	%rbp, %rdi
 2cfdff2:      	movq	%r15, %rsi
 2cfdff5:      	movl	%r14d, %r13d
 2cfdff8:      	movl	%r14d, %edx
 2cfdffb:      	movl	0x18(%rsp), %r8d
 2cfe000:      	movl	%ebx, %r9d
 2cfe003:      	pushq	%r15
 2cfe005:      	movq	0x10(%rsp), %rbx
 2cfe00a:      	pushq	0x40(%rbx)
 2cfe00d:      	pushq	%r10
 2cfe00f:      	movq	0xb8(%rsp), %r14
 2cfe017:      	pushq	%r14
 2cfe019:      	pushq	%r12
 2cfe01b:      	pushq	$0x0
 2cfe01d:      	pushq	%r11
 2cfe01f:      	pushq	%rax
 2cfe020:      	pushq	0x108(%rsp)
 2cfe027:      	callq	0x2d04a20 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfe02c:      	addq	$0x50, %rsp
 2cfe030:      	addl	$0x4, %r13d
 2cfe034:      	subq	$0x8, %rsp
 2cfe038:      	movzbl	0x10(%rsp), %eax
 2cfe03d:      	andl	$0x1, %eax
 2cfe040:      	movq	%rbp, %rdi
 2cfe043:      	movq	%r15, %rsi
 2cfe046:      	movl	%r13d, %edx
 2cfe049:      	movl	0xf0(%rsp), %ecx
 2cfe050:      	movl	0x90(%rsp), %r8d
 2cfe058:      	movl	0x128(%rsp), %r9d
 2cfe060:      	pushq	%r15
 2cfe062:      	pushq	0x40(%rbx)
 2cfe065:      	pushq	0x88(%rsp)
 2cfe06c:      	pushq	%r14
 2cfe06e:      	pushq	%r12
 2cfe070:      	pushq	0x110(%rsp)
 2cfe077:      	pushq	0x60(%rsp)
 2cfe07b:      	pushq	0x60(%rsp)
 2cfe07f:      	pushq	%rax
 2cfe080:      	callq	0x2d04a20 <_ZL13InsertLDR_STRRN4llvm17MachineBasicBlockERNS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEEibjjbbjbbNS_5ARMCC9CondCodesEjPKNS_15TargetInstrInfoEPS3_>
 2cfe085:      	addq	$0x50, %rsp
 2cfe089:      	testb	$0x4, (%r15)
 2cfe08d:      	movq	%r15, %rax
 2cfe090:      	xorps	%xmm0, %xmm0
 2cfe093:      	jne	0x2cfe0ba <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeaa>
 2cfe095:      	testb	$0x8, 0x2c(%r15)
 2cfe09a:      	movq	%r15, %rax
 2cfe09d:      	je	0x2cfe0ba <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeaa>
 2cfe09f:      	movq	%r15, %rax
 2cfe0a2:      	nopw	%cs:(%rax,%rax)
 2cfe0ac:      	nopl	(%rax)
 2cfe0b0:      	movq	0x8(%rax), %rax
 2cfe0b4:      	testb	$0x8, 0x2c(%rax)
 2cfe0b8:      	jne	0x2cfe0b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xea0>
 2cfe0ba:      	movq	0x8(%rax), %rax
 2cfe0be:      	movq	%rax, 0x10(%rsp)
 2cfe0c3:      	cmpq	%rax, %r15
 2cfe0c6:      	jne	0x2cfe10f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeff>
 2cfe0c8:      	movq	0x10(%rsp), %r15
 2cfe0cd:      	movq	0x90(%rsp), %r12
 2cfe0d5:      	movq	(%rsp), %rdi
 2cfe0d9:      	jmp	0x2cfd2b6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xa6>
 2cfe0de:      	nop
 2cfe0e0:      	movl	%ecx, 0xf0(%rbp)
 2cfe0e6:      	movq	(%r14), %rax
 2cfe0e9:      	movq	(%rax,%r12,8), %rcx
 2cfe0ed:      	movq	%rcx, (%rbx)
 2cfe0f0:      	movq	%rbx, (%rax,%r12,8)
 2cfe0f4:      	movq	0xe0(%rbp), %rax
 2cfe0fb:      	movq	%rax, (%r15)
 2cfe0fe:      	movq	%r15, 0xe0(%rbp)
 2cfe105:      	movq	%r13, %r15
 2cfe108:      	cmpq	0x10(%rsp), %r13
 2cfe10d:      	je	0x2cfe0c8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xeb8>
 2cfe10f:      	movq	0x8(%r15), %r13
 2cfe113:      	movq	0x18(%r15), %rax
 2cfe117:      	movq	0x20(%rax), %rbx
 2cfe11b:      	testq	%rbx, %rbx
 2cfe11e:      	je	0x2cfe1d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe124:      	movq	0x288(%rbx), %rdi
 2cfe12b:      	testq	%rdi, %rdi
 2cfe12e:      	je	0x2cfe13c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf2c>
 2cfe130:      	movq	(%rdi), %rax
 2cfe133:      	movq	%r15, %rsi
 2cfe136:      	callq	*0x20(%rax)
 2cfe139:      	xorps	%xmm0, %xmm0
 2cfe13c:      	movzwl	0x28(%r15), %ecx
 2cfe141:      	movzbl	0x2a(%r15), %eax
 2cfe146:      	shll	$0x10, %eax
 2cfe149:      	orl	%ecx, %eax
 2cfe14b:      	testl	%eax, %eax
 2cfe14d:      	je	0x2cfe1d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe153:      	movq	0x20(%r15), %rcx
 2cfe157:      	shll	$0x5, %eax
 2cfe15a:      	movq	0x20(%rbx), %rdx
 2cfe15e:      	jmp	0x2cfe181 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf71>
 2cfe160:      	movq	%rdi, 0x18(%r8)
 2cfe164:      	leaq	0x10(%rcx), %r9
 2cfe168:      	testq	%rdi, %rdi
 2cfe16b:      	cmovneq	%rdi, %rsi
 2cfe16f:      	movq	%r8, 0x10(%rsi)
 2cfe173:      	movups	%xmm0, (%r9)
 2cfe177:      	addq	$0x20, %rcx
 2cfe17b:      	addq	$-0x20, %rax
 2cfe17f:      	je	0x2cfe1d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xfc0>
 2cfe181:      	cmpb	$0x0, (%rcx)
 2cfe184:      	jne	0x2cfe177 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf67>
 2cfe186:      	movl	0x4(%rcx), %esi
 2cfe189:      	movl	%esi, %edi
 2cfe18b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2cfe191:      	shlq	$0x4, %rdi
 2cfe195:      	movq	%rsi, %r8
 2cfe198:      	shlq	$0x3, %r8
 2cfe19c:      	addq	0x128(%rdx), %r8
 2cfe1a3:      	testl	%esi, %esi
 2cfe1a5:      	movq	0x30(%rdx), %rsi
 2cfe1a9:      	leaq	0x8(%rsi,%rdi), %r9
 2cfe1ae:      	cmovnsq	%r8, %r9
 2cfe1b2:      	movq	(%r9), %rsi
 2cfe1b5:      	movq	0x18(%rcx), %rdi
 2cfe1b9:      	movq	0x10(%rcx), %r8
 2cfe1bd:      	cmpq	%rsi, %rcx
 2cfe1c0:      	jne	0x2cfe160 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf50>
 2cfe1c2:      	movq	%rdi, (%r9)
 2cfe1c5:      	jmp	0x2cfe164 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xf54>
 2cfe1c7:      	nopw	(%rax,%rax)
 2cfe1d0:      	movq	$0x0, 0x18(%r15)
 2cfe1d8:      	movq	(%r15), %rax
 2cfe1db:      	movq	0x8(%r15), %rcx
 2cfe1df:      	andq	$-0x8, %rax
 2cfe1e3:      	movq	(%rcx), %rdx
 2cfe1e6:      	andl	$0x7, %edx
 2cfe1e9:      	orq	%rax, %rdx
 2cfe1ec:      	movq	%rdx, (%rcx)
 2cfe1ef:      	movq	%rcx, 0x8(%rax)
 2cfe1f3:      	andq	$0x7, (%r15)
 2cfe1f7:      	movq	$0x0, 0x8(%r15)
 2cfe1ff:      	movq	0x18(%rsp), %rax
 2cfe204:      	movq	0x28(%rax), %rax
 2cfe208:      	movq	0x20(%rax), %rbp
 2cfe20c:      	movq	0x20(%r15), %rbx
 2cfe210:      	testq	%rbx, %rbx
 2cfe213:      	je	0x2cfe0f4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xee4>
 2cfe219:      	movzbl	0x2b(%r15), %r12d
 2cfe21e:      	leaq	0xe8(%rbp), %r14
 2cfe225:      	movl	0xf0(%rbp), %eax
 2cfe22b:      	cmpl	%r12d, %eax
 2cfe22e:      	ja	0x2cfe0e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed6>
 2cfe234:      	leaq	0x1(%r12), %rcx
 2cfe239:      	cmpl	%r12d, 0xf4(%rbp)
 2cfe240:      	ja	0x2cfe269 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1059>
 2cfe242:      	leaq	0xf8(%rbp), %rsi
 2cfe249:      	movl	$0x8, %ecx
 2cfe24e:      	movq	%r14, %rdi
 2cfe251:      	leaq	0x1(%r12), %rdx
 2cfe256:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe25b:      	leaq	0x1(%r12), %rcx
 2cfe260:      	xorps	%xmm0, %xmm0
 2cfe263:      	movl	0xf0(%rbp), %eax
 2cfe269:      	cmpl	%eax, %ecx
 2cfe26b:      	je	0x2cfe0e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed0>
 2cfe271:      	movl	%eax, %eax
 2cfe273:      	leaq	(,%rax,8), %rdi
 2cfe27b:      	addq	(%r14), %rdi
 2cfe27e:      	movq	%rcx, %r14
 2cfe281:      	movq	%rcx, %rdx
 2cfe284:      	subq	%rax, %rdx
 2cfe287:      	shlq	$0x3, %rdx
 2cfe28b:      	xorl	%esi, %esi
 2cfe28d:      	callq	0x828ac20 <memset@plt>
 2cfe292:      	movq	%r14, %rcx
 2cfe295:      	leaq	0xe8(%rbp), %r14
 2cfe29c:      	xorps	%xmm0, %xmm0
 2cfe29f:      	jmp	0x2cfe0e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xed0>
 2cfe2a4:      	movl	0x240(%rsp), %edx
 2cfe2ab:      	cmpl	0x244(%rsp), %edx
 2cfe2b2:      	jae	0x2cfe5a1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1391>
 2cfe2b8:      	movq	%r12, %rcx
 2cfe2bb:      	shlq	$0x20, %rcx
 2cfe2bf:      	movl	%eax, %eax
 2cfe2c1:      	orq	%rcx, %rax
 2cfe2c4:      	movq	0x238(%rsp), %rcx
 2cfe2cc:      	movl	%edx, %edx
 2cfe2ce:      	shlq	$0x4, %rdx
 2cfe2d2:      	movq	%r15, (%rcx,%rdx)
 2cfe2d6:      	movq	%rax, 0x8(%rcx,%rdx)
 2cfe2db:      	incl	0x240(%rsp)
 2cfe2e2:      	movl	%ebx, 0x118(%rsp)
 2cfe2e9:      	movl	%r14d, 0x180(%rsp)
 2cfe2f1:      	movl	0x10(%rsp), %eax
 2cfe2f5:      	movq	%rax, 0x80(%rsp)
 2cfe2fd:      	jmp	0x2cfe0d5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe302:      	movq	%r9, %rbp
 2cfe305:      	movl	(%rcx), %ebx
 2cfe307:      	jmp	0x2cfddfd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xbed>
 2cfe30c:      	incq	%rdx
 2cfe30f:      	movl	$0x8, %ecx
 2cfe314:      	movq	0x1f8(%rsp), %rdi
 2cfe31c:      	movq	0x220(%rsp), %rsi
 2cfe324:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe329:      	movq	(%rsp), %rax
 2cfe32d:      	movl	0x2a0(%rax), %edx
 2cfe333:      	jmp	0x2cfdec8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcb8>
 2cfe338:      	movq	0x8(%rsp), %rbp
 2cfe33d:      	jmp	0x2cfdefa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe342:      	cmpl	$0x3d7, %ecx            # imm = 0x3D7
 2cfe348:      	je	0x2cfe35e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfe34a:      	cmpl	$0xb51, %ecx            # imm = 0xB51
 2cfe350:      	je	0x2cfe35e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x114e>
 2cfe352:      	cmpl	$0xb53, %ecx            # imm = 0xB53
 2cfe358:      	jne	0x2cfe478 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1268>
 2cfe35e:      	movq	0x20(%rsp), %rcx
 2cfe363:      	cmpl	%ecx, 0x80(%rsp)
 2cfe36a:      	je	0x2cfdef6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe370:      	movq	0x238(%rsp), %r13
 2cfe378:      	movl	0x240(%rsp), %edx
 2cfe37f:      	testq	%rdx, %rdx
 2cfe382:      	je	0x2cfe464 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1254>
 2cfe388:      	movq	%rbx, %rbp
 2cfe38b:      	movq	%rdx, %rcx
 2cfe38e:      	shlq	$0x4, %rcx
 2cfe392:      	movq	0x20(%rsp), %rsi
 2cfe397:      	leal	-0x1(%rsi), %edi
 2cfe39a:      	movq	(%rsp), %rsi
 2cfe39e:      	movq	0x48(%rsi), %r8
 2cfe3a2:      	movq	%r13, %r9
 2cfe3a5:      	jmp	0x2cfe3b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x11a9>
 2cfe3a7:      	addq	$0x10, %r9
 2cfe3ab:      	leaq	(%r13,%rcx), %rsi
 2cfe3b0:      	cmpq	%rsi, %r9
 2cfe3b3:      	je	0x2cfe4ca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12ba>
 2cfe3b9:      	movq	(%r9), %r10
 2cfe3bc:      	movq	0x20(%r10), %r10
 2cfe3c0:      	movl	0x4(%r10), %ebx
 2cfe3c4:      	cmpl	%ebx, 0x20(%rsp)
 2cfe3c8:      	je	0x2cfe453 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1243>
 2cfe3ce:      	cmpl	$0x3ffffffe, %edi       # imm = 0x3FFFFFFE
 2cfe3d4:      	ja	0x2cfe3a7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe3d6:      	leal	-0x1(%rbx), %r10d
 2cfe3da:      	cmpl	$0x3ffffffe, %r10d      # imm = 0x3FFFFFFE
 2cfe3e1:      	ja	0x2cfe3a7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe3e3:      	movq	0x20(%rsp), %rsi
 2cfe3e8:      	leaq	(%rsi,%rsi,2), %r10
 2cfe3ec:      	movq	0x8(%r8), %r14
 2cfe3f0:      	movq	0x38(%r8), %rsi
 2cfe3f4:      	movl	0x10(%r14,%r10,8), %r11d
 2cfe3f9:      	movl	%r11d, %r10d
 2cfe3fc:      	andl	$0xfff, %r10d           # imm = 0xFFF
 2cfe403:      	shrl	$0xc, %r11d
 2cfe407:      	leaq	(%rsi,%r11,2), %r11
 2cfe40b:      	leaq	(%rbx,%rbx,2), %rbx
 2cfe40f:      	movl	0x10(%r14,%rbx,8), %r14d
 2cfe414:      	movl	%r14d, %ebx
 2cfe417:      	andl	$0xfff, %ebx            # imm = 0xFFF
 2cfe41d:      	shrl	$0xc, %r14d
 2cfe421:      	leaq	(%rsi,%r14,2), %r14
 2cfe425:      	cmpl	%ebx, %r10d
 2cfe428:      	je	0x2cfe453 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1243>
 2cfe42a:      	jae	0x2cfe440 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1230>
 2cfe42c:      	movswl	(%r11), %esi
 2cfe430:      	addq	$0x2, %r11
 2cfe434:      	addl	%esi, %r10d
 2cfe437:      	testl	%esi, %esi
 2cfe439:      	jne	0x2cfe425 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1215>
 2cfe43b:      	jmp	0x2cfe3a7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe440:      	movswl	(%r14), %esi
 2cfe444:      	addq	$0x2, %r14
 2cfe448:      	addl	%esi, %ebx
 2cfe44a:      	testl	%esi, %esi
 2cfe44c:      	jne	0x2cfe425 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1215>
 2cfe44e:      	jmp	0x2cfe3a7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1197>
 2cfe453:      	movq	(%rsp), %rdi
 2cfe457:      	movq	%rbp, %rbx
 2cfe45a:      	movq	0x8(%rsp), %rbp
 2cfe45f:      	jmp	0x2cfdefa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe464:      	cmpl	-0x8(%r13), %eax
 2cfe468:      	movq	(%rsp), %rdi
 2cfe46c:      	jle	0x2cfdefa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe472:      	xorl	%edx, %edx
 2cfe474:      	xorl	%esi, %esi
 2cfe476:      	jmp	0x2cfe497 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1287>
 2cfe478:      	movl	0x240(%rsp), %edx
 2cfe47f:      	movq	0x238(%rsp), %r13
 2cfe487:      	movq	%rdx, %rcx
 2cfe48a:      	shlq	$0x4, %rcx
 2cfe48e:      	movl	%edx, %esi
 2cfe490:      	cmpl	-0x8(%r13,%rcx), %eax
 2cfe495:      	jle	0x2cfe4db <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12cb>
 2cfe497:      	cmpl	0x244(%rsp), %esi
 2cfe49e:      	jae	0x2cfe5ce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x13be>
 2cfe4a4:      	movq	%r12, %rcx
 2cfe4a7:      	shlq	$0x20, %rcx
 2cfe4ab:      	movl	%eax, %eax
 2cfe4ad:      	orq	%rcx, %rax
 2cfe4b0:      	shlq	$0x4, %rdx
 2cfe4b4:      	movq	%r15, (%r13,%rdx)
 2cfe4b9:      	movq	%rax, 0x8(%r13,%rdx)
 2cfe4be:      	incl	0x240(%rsp)
 2cfe4c5:      	jmp	0x2cfe0d5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe4ca:      	movl	%edx, %esi
 2cfe4cc:      	movq	%rbp, %rbx
 2cfe4cf:      	movq	0x8(%rsp), %rbp
 2cfe4d4:      	cmpl	-0x8(%r13,%rcx), %eax
 2cfe4d9:      	jg	0x2cfe497 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1287>
 2cfe4db:      	testl	%esi, %esi
 2cfe4dd:      	je	0x2cfe507 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12f7>
 2cfe4df:      	leaq	-0x10(%rcx), %rdi
 2cfe4e3:      	movq	%r13, %r14
 2cfe4e6:      	movl	0x8(%r14), %r8d
 2cfe4ea:      	cmpl	%r8d, %eax
 2cfe4ed:      	jl	0x2cfe50c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12fc>
 2cfe4ef:      	je	0x2cfdef6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe4f5:      	addq	$0x10, %r14
 2cfe4f9:      	testq	%rdi, %rdi
 2cfe4fc:      	leaq	-0x10(%rdi), %rdi
 2cfe500:      	jne	0x2cfe4e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x12d6>
 2cfe502:      	jmp	0x2cfdef6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xce6>
 2cfe507:      	xorl	%edx, %edx
 2cfe509:      	movq	%r13, %r14
 2cfe50c:      	addq	%r13, %rcx
 2cfe50f:      	cmpq	%rcx, %r14
 2cfe512:      	movq	(%rsp), %rdi
 2cfe516:      	je	0x2cfdefa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xcea>
 2cfe51c:      	cmpl	0x244(%rsp), %esi
 2cfe523:      	jae	0x2cfe603 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x13f3>
 2cfe529:      	movq	%r13, %rcx
 2cfe52c:      	movl	%eax, %ebx
 2cfe52e:      	subq	%r13, %r14
 2cfe531:      	addq	%rcx, %r14
 2cfe534:      	shlq	$0x4, %rdx
 2cfe538:      	movups	-0x10(%rcx,%rdx), %xmm0
 2cfe53d:      	movups	%xmm0, (%rcx,%rdx)
 2cfe541:      	movq	0x238(%rsp), %rdi
 2cfe549:      	movl	0x240(%rsp), %ecx
 2cfe550:      	shlq	$0x4, %rcx
 2cfe554:      	leaq	-0x10(%rdi,%rcx), %rax
 2cfe559:      	movq	%rax, %rdx
 2cfe55c:      	subq	%r14, %rdx
 2cfe55f:      	movq	%rdx, %rsi
 2cfe562:      	sarq	$0x4, %rsi
 2cfe566:      	cmpq	$0x2, %rsi
 2cfe56a:      	jl	0x2cfe638 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1428>
 2cfe570:      	addq	%rcx, %rdi
 2cfe573:      	shlq	$0x4, %rsi
 2cfe577:      	subq	%rsi, %rdi
 2cfe57a:      	movq	%r14, %rsi
 2cfe57d:      	callq	0x828ac50 <memmove@plt>
 2cfe582:      	movl	%ebx, %eax
 2cfe584:      	movq	%r12, %rcx
 2cfe587:      	incl	0x240(%rsp)
 2cfe58e:      	shlq	$0x20, %rcx
 2cfe592:      	orq	%rax, %rcx
 2cfe595:      	movq	%r15, (%r14)
 2cfe598:      	movq	%rcx, 0x8(%r14)
 2cfe59c:      	jmp	0x2cfe0d5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0xec5>
 2cfe5a1:      	incq	%rdx
 2cfe5a4:      	movl	$0x10, %ecx
 2cfe5a9:      	leaq	0x238(%rsp), %rdi
 2cfe5b1:      	leaq	0x248(%rsp), %rsi
 2cfe5b9:      	movl	%eax, %ebp
 2cfe5bb:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe5c0:      	movl	%ebp, %eax
 2cfe5c2:      	movl	0x240(%rsp), %edx
 2cfe5c9:      	jmp	0x2cfe2b8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x10a8>
 2cfe5ce:      	incq	%rdx
 2cfe5d1:      	movl	$0x10, %ecx
 2cfe5d6:      	leaq	0x238(%rsp), %rdi
 2cfe5de:      	leaq	0x248(%rsp), %rsi
 2cfe5e6:      	movl	%eax, %ebx
 2cfe5e8:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe5ed:      	movl	%ebx, %eax
 2cfe5ef:      	movl	0x240(%rsp), %edx
 2cfe5f6:      	movq	0x238(%rsp), %r13
 2cfe5fe:      	jmp	0x2cfe4a4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1294>
 2cfe603:      	incq	%rdx
 2cfe606:      	movl	$0x10, %ecx
 2cfe60b:      	leaq	0x238(%rsp), %rdi
 2cfe613:      	leaq	0x248(%rsp), %rsi
 2cfe61b:      	movl	%eax, %ebx
 2cfe61d:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfe622:      	movl	%ebx, %eax
 2cfe624:      	movq	0x238(%rsp), %rcx
 2cfe62c:      	movl	0x240(%rsp), %edx
 2cfe633:      	jmp	0x2cfe52c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x131c>
 2cfe638:      	cmpq	$0x10, %rdx
 2cfe63c:      	jne	0x2cfe582 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1372>
 2cfe642:      	movups	(%r14), %xmm0
 2cfe646:      	movups	%xmm0, (%rax)
 2cfe649:      	jmp	0x2cfe582 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1372>
 2cfe64e:      	cmpl	$0x0, 0x240(%rsp)
 2cfe656:      	je	0x2cfe669 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1459>
 2cfe658:      	leaq	0x238(%rsp), %rsi
 2cfe660:      	callq	0x2d023b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt14FormCandidatesERKN4llvm11SmallVectorINS0_15MemOpQueueEntryELj8EEE>
 2cfe665:      	movq	(%rsp), %rdi
 2cfe669:      	movl	0x270(%rdi), %r14d
 2cfe670:      	testq	%r14, %r14
 2cfe673:      	je	0x2d021c1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb1>
 2cfe679:      	movq	0x268(%rdi), %rbx
 2cfe680:      	leaq	(%rbx,%r14,8), %r13
 2cfe684:      	bsrq	%r14, %rdx
 2cfe688:      	xorl	$0x3f, %edx
 2cfe68b:      	addl	%edx, %edx
 2cfe68d:      	xorq	$0x7e, %rdx
 2cfe691:      	movq	%rbx, %rdi
 2cfe694:      	movq	%r13, %rsi
 2cfe697:      	callq	0x2d04d50 <_ZSt16__introsort_loopIPPKN12_GLOBAL__N_115ARMLoadStoreOpt14MergeCandidateElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockEE3$_0EEEvT_SE_T0_T1_>
 2cfe69c:      	leaq	0x8(%rbx), %r15
 2cfe6a0:      	cmpl	$0x11, %r14d
 2cfe6a4:      	jb	0x2cfe6bc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14ac>
 2cfe6a6:      	movq	%r13, 0x18(%rsp)
 2cfe6ab:      	movl	$0x8, %r12d
 2cfe6b1:      	movq	%r15, %r13
 2cfe6b4:      	movq	%rbx, %rbp
 2cfe6b7:      	jmp	0x2d022f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50e7>
 2cfe6bc:      	cmpl	$0x1, %r14d
 2cfe6c0:      	jne	0x2d02241 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5031>
 2cfe6c6:      	movq	(%rsp), %rdi
 2cfe6ca:      	movl	0x270(%rdi), %eax
 2cfe6d0:      	testq	%rax, %rax
 2cfe6d3:      	je	0x2d021c1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb1>
 2cfe6d9:      	movq	0x268(%rdi), %rcx
 2cfe6e0:      	leaq	(%rcx,%rax,8), %rax
 2cfe6e4:      	movq	%rax, 0xe8(%rsp)
 2cfe6ec:      	leaq	0x68(%rdi), %rax
 2cfe6f0:      	movq	%rax, 0x118(%rsp)
 2cfe6f8:      	leaq	0x70(%rdi), %rax
 2cfe6fc:      	movq	%rax, 0xe0(%rsp)
 2cfe704:      	leaq	0x80(%rdi), %rax
 2cfe70b:      	movq	%rax, 0x220(%rsp)
 2cfe713:      	leaq	0xb8(%rdi), %rax
 2cfe71a:      	movq	%rax, 0x1f8(%rsp)
 2cfe722:      	xorps	%xmm0, %xmm0
 2cfe725:      	xorl	%eax, %eax
 2cfe727:      	jmp	0x2cfe769 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1559>
 2cfe729:      	nopl	(%rax)
 2cfe730:      	movq	(%rax), %rax
 2cfe733:      	movq	(%rax), %rsi
 2cfe736:      	callq	0x2d033e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt24MergeBaseUpdateLoadStoreEPN4llvm12MachineInstrE>
 2cfe73b:      	movq	(%rsp), %rdi
 2cfe73f:      	movq	0x98(%rsp), %rcx
 2cfe747:      	orb	%al, %cl
 2cfe749:      	movq	%rcx, %rax
 2cfe74c:      	movq	0x120(%rsp), %rcx
 2cfe754:      	addq	$0x8, %rcx
 2cfe758:      	cmpq	0xe8(%rsp), %rcx
 2cfe760:      	xorps	%xmm0, %xmm0
 2cfe763:      	je	0x2d021c3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fb3>
 2cfe769:      	movq	%rax, 0x98(%rsp)
 2cfe771:      	movq	(%rcx), %rax
 2cfe774:      	cmpb	$0x0, 0x3c(%rax)
 2cfe778:      	movq	%rcx, 0x120(%rsp)
 2cfe780:      	jne	0x2cfe788 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1578>
 2cfe782:      	cmpb	$0x1, 0x3d(%rax)
 2cfe786:      	jne	0x2cfe730 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1520>
 2cfe788:      	movq	%rax, 0x90(%rsp)
 2cfe790:      	movq	(%rax), %r14
 2cfe793:      	movq	(%r14), %rbp
 2cfe796:      	movzwl	0x44(%rbp), %ebx
 2cfe79a:      	movb	$0x1, %al
 2cfe79c:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cfe7a2:      	je	0x2cfe7c1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe7a4:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cfe7aa:      	je	0x2cfe7c1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe7ac:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cfe7b2:      	je	0x2cfe7c1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x15b1>
 2cfe7b4:      	movl	%ebx, %eax
 2cfe7b6:      	andl	$-0x2, %eax
 2cfe7b9:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cfe7be:      	sete	%al
 2cfe7c1:      	movl	%ebx, %ecx
 2cfe7c3:      	andl	$-0x3, %ecx
 2cfe7c6:      	movl	%ecx, 0xc0(%rsp)
 2cfe7cd:      	cmpl	$0xb51, %ecx            # imm = 0xB51
 2cfe7d3:      	sete	%r15b
 2cfe7d7:      	leaq	0x140(%rsp), %rcx
 2cfe7df:      	movq	%rcx, 0x130(%rsp)
 2cfe7e7:      	movabsq	$0x800000000, %rcx      # imm = 0x800000000
 2cfe7f1:      	movq	%rcx, 0x138(%rsp)
 2cfe7f9:      	leaq	0x1d0(%rsp), %rcx
 2cfe801:      	movq	%rcx, 0x1c0(%rsp)
 2cfe809:      	movabsq	$0x400000000, %rcx      # imm = 0x400000000
 2cfe813:      	movq	%rcx, 0x1c8(%rsp)
 2cfe81b:      	movaps	%xmm0, 0x200(%rsp)
 2cfe823:      	movl	$0x0, 0x210(%rsp)
 2cfe82e:      	movaps	%xmm0, 0x1e0(%rsp)
 2cfe836:      	movl	$0x0, 0x1f0(%rsp)
 2cfe841:      	movq	0x90(%rsp), %rcx
 2cfe849:      	movl	0x8(%rcx), %ecx
 2cfe84c:      	testq	%rcx, %rcx
 2cfe84f:      	movq	%rbx, 0x78(%rsp)
 2cfe854:      	je	0x2cfedd0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bc0>
 2cfe85a:      	movq	%rbp, 0x10(%rsp)
 2cfe85f:      	orb	%al, %r15b
 2cfe862:      	leaq	(%r14,%rcx,8), %rax
 2cfe866:      	movq	%rax, 0x18(%rsp)
 2cfe86b:      	jmp	0x2cfe87f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x166f>
 2cfe86d:      	nopl	(%rax)
 2cfe870:      	addq	$0x8, %r14
 2cfe874:      	cmpq	0x18(%rsp), %r14
 2cfe879:      	je	0x2cfedb0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ba0>
 2cfe87f:      	movq	(%r14), %rbx
 2cfe882:      	movq	0x20(%rbx), %rax
 2cfe886:      	movl	(%rax), %ecx
 2cfe888:      	movl	0x4(%rax), %ebp
 2cfe88b:      	movl	%ecx, %eax
 2cfe88d:      	shrl	$0x1a, %eax
 2cfe890:      	xorl	%r12d, %r12d
 2cfe893:      	testl	$0x1000000, %ecx        # imm = 0x1000000
 2cfe899:      	sete	%r12b
 2cfe89d:      	andl	%eax, %r12d
 2cfe8a0:      	je	0x2cfe95c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe8a6:      	movl	0x210(%rsp), %esi
 2cfe8ad:      	testl	%esi, %esi
 2cfe8af:      	je	0x2cfe910 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1700>
 2cfe8b1:      	movq	0x200(%rsp), %rcx
 2cfe8b9:      	leal	(%rbp,%rbp,8), %eax
 2cfe8bd:      	leal	(%rbp,%rax,4), %edx
 2cfe8c1:      	leal	-0x1(%rsi), %edi
 2cfe8c4:      	andl	%edi, %edx
 2cfe8c6:      	movl	(%rcx,%rdx,4), %r10d
 2cfe8ca:      	cmpl	%r10d, %ebp
 2cfe8cd:      	je	0x2cfe95c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe8d3:      	leaq	(%rcx,%rdx,4), %rax
 2cfe8d7:      	movl	$0x1, %r8d
 2cfe8dd:      	xorl	%r9d, %r9d
 2cfe8e0:      	cmpl	$-0x1, %r10d
 2cfe8e4:      	je	0x2cfec69 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a59>
 2cfe8ea:      	testq	%r9, %r9
 2cfe8ed:      	cmovneq	%r9, %rax
 2cfe8f1:      	cmpl	$-0x2, %r10d
 2cfe8f5:      	cmoveq	%rax, %r9
 2cfe8f9:      	addl	%r8d, %edx
 2cfe8fc:      	incl	%r8d
 2cfe8ff:      	andl	%edi, %edx
 2cfe901:      	leaq	(%rcx,%rdx,4), %rax
 2cfe905:      	movl	(%rcx,%rdx,4), %r10d
 2cfe909:      	cmpl	%r10d, %ebp
 2cfe90c:      	je	0x2cfe95c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174c>
 2cfe90e:      	jmp	0x2cfe8e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x16d0>
 2cfe910:      	xorl	%eax, %eax
 2cfe912:      	movl	0x208(%rsp), %ecx
 2cfe919:      	leal	0x4(,%rcx,4), %edx
 2cfe920:      	leal	(%rsi,%rsi,2), %edi
 2cfe923:      	cmpl	%edi, %edx
 2cfe925:      	jae	0x2cfed06 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1af6>
 2cfe92b:      	movl	%ecx, %edx
 2cfe92d:      	notl	%edx
 2cfe92f:      	addl	%esi, %edx
 2cfe931:      	subl	0x20c(%rsp), %edx
 2cfe938:      	movl	%esi, %edi
 2cfe93a:      	shrl	$0x3, %edi
 2cfe93d:      	cmpl	%edi, %edx
 2cfe93f:      	jbe	0x2cfed08 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1af8>
 2cfe945:      	incl	%ecx
 2cfe947:      	movl	%ecx, 0x208(%rsp)
 2cfe94e:      	cmpl	$-0x1, (%rax)
 2cfe951:      	je	0x2cfe95a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174a>
 2cfe953:      	decl	0x20c(%rsp)
 2cfe95a:      	movl	%ebp, (%rax)
 2cfe95c:      	movl	0x138(%rsp), %edx
 2cfe963:      	cmpl	0x13c(%rsp), %edx
 2cfe96a:      	jae	0x2cfec34 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a24>
 2cfe970:      	shlq	$0x20, %r12
 2cfe974:      	orq	%rbp, %r12
 2cfe977:      	movq	0x130(%rsp), %rax
 2cfe97f:      	movl	%edx, %ecx
 2cfe981:      	movq	%r12, (%rax,%rcx,8)
 2cfe985:      	incl	0x138(%rsp)
 2cfe98c:      	movl	0x1f0(%rsp), %esi
 2cfe993:      	testl	%esi, %esi
 2cfe995:      	je	0x2cfea00 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17f0>
 2cfe997:      	movq	0x1e0(%rsp), %rcx
 2cfe99f:      	leal	(%rbp,%rbp,8), %eax
 2cfe9a3:      	leal	(%rbp,%rax,4), %edx
 2cfe9a7:      	leal	-0x1(%rsi), %edi
 2cfe9aa:      	andl	%edi, %edx
 2cfe9ac:      	movl	(%rcx,%rdx,4), %r10d
 2cfe9b0:      	cmpl	%r10d, %ebp
 2cfe9b3:      	je	0x2cfea4c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183c>
 2cfe9b9:      	leaq	(%rcx,%rdx,4), %rax
 2cfe9bd:      	movl	$0x1, %r8d
 2cfe9c3:      	xorl	%r9d, %r9d
 2cfe9c6:      	cmpl	$-0x1, %r10d
 2cfe9ca:      	je	0x2cfec5d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a4d>
 2cfe9d0:      	testq	%r9, %r9
 2cfe9d3:      	cmovneq	%r9, %rax
 2cfe9d7:      	cmpl	$-0x2, %r10d
 2cfe9db:      	cmoveq	%rax, %r9
 2cfe9df:      	addl	%r8d, %edx
 2cfe9e2:      	incl	%r8d
 2cfe9e5:      	andl	%edi, %edx
 2cfe9e7:      	leaq	(%rcx,%rdx,4), %rax
 2cfe9eb:      	movl	(%rcx,%rdx,4), %r10d
 2cfe9ef:      	cmpl	%r10d, %ebp
 2cfe9f2:      	je	0x2cfea4c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183c>
 2cfe9f4:      	jmp	0x2cfe9c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17b6>
 2cfe9f6:      	nopw	%cs:(%rax,%rax)
 2cfea00:      	xorl	%eax, %eax
 2cfea02:      	movl	0x1e8(%rsp), %ecx
 2cfea09:      	leal	0x4(,%rcx,4), %edx
 2cfea10:      	leal	(%rsi,%rsi,2), %edi
 2cfea13:      	cmpl	%edi, %edx
 2cfea15:      	jae	0x2cfec75 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a65>
 2cfea1b:      	movl	%ecx, %edx
 2cfea1d:      	notl	%edx
 2cfea1f:      	addl	%esi, %edx
 2cfea21:      	subl	0x1ec(%rsp), %edx
 2cfea28:      	movl	%esi, %edi
 2cfea2a:      	shrl	$0x3, %edi
 2cfea2d:      	cmpl	%edi, %edx
 2cfea2f:      	jbe	0x2cfec77 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1a67>
 2cfea35:      	incl	%ecx
 2cfea37:      	movl	%ecx, 0x1e8(%rsp)
 2cfea3e:      	cmpl	$-0x1, (%rax)
 2cfea41:      	je	0x2cfea4a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183a>
 2cfea43:      	decl	0x1ec(%rsp)
 2cfea4a:      	movl	%ebp, (%rax)
 2cfea4c:      	testb	%r15b, %r15b
 2cfea4f:      	je	0x2cfe870 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfea55:      	movq	0x10(%rbx), %rdx
 2cfea59:      	movq	0x20(%rbx), %rax
 2cfea5d:      	movzwl	0x28(%rbx), %ecx
 2cfea61:      	movzbl	0x2a(%rbx), %r12d
 2cfea66:      	shll	$0x10, %r12d
 2cfea6a:      	orq	%rcx, %r12
 2cfea6d:      	movzwl	0x2(%rdx), %ecx
 2cfea71:      	testb	$0x2, 0x10(%rdx)
 2cfea75:      	je	0x2cfeab0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea77:      	movl	%ecx, %edx
 2cfea79:      	cmpq	%r12, %rdx
 2cfea7c:      	movl	$0x20000ff, %r8d        # imm = 0x20000FF
 2cfea82:      	je	0x2cfeab0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea84:      	movl	%r12d, %esi
 2cfea87:      	shll	$0x5, %esi
 2cfea8a:      	shll	$0x5, %edx
 2cfea8d:      	nopl	(%rax)
 2cfea90:      	movl	(%rax,%rdx), %edi
 2cfea93:      	andl	%r8d, %edi
 2cfea96:      	cmpl	$0x2000000, %edi        # imm = 0x2000000
 2cfea9c:      	je	0x2cfeab0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18a0>
 2cfea9e:      	incl	%ecx
 2cfeaa0:      	addq	$0x20, %rdx
 2cfeaa4:      	cmpq	%rdx, %rsi
 2cfeaa7:      	jne	0x2cfea90 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1880>
 2cfeaa9:      	nopl	(%rax)
 2cfeab0:      	movl	%ecx, %r13d
 2cfeab3:      	cmpq	%r12, %r13
 2cfeab6:      	je	0x2cfe870 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfeabc:      	shll	$0x5, %r12d
 2cfeac0:      	addq	%rax, %r12
 2cfeac3:      	shlq	$0x5, %r13
 2cfeac7:      	addq	%rax, %r13
 2cfeaca:      	jmp	0x2cfeaea <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18da>
 2cfeacc:      	movq	%rdx, %rsi
 2cfeacf:      	nop
 2cfead0:      	leaq	(%rax,%rcx,4), %rax
 2cfead4:      	cmpq	%rax, %rsi
 2cfead7:      	je	0x2cfebb3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19a3>
 2cfeadd:      	addq	$0x20, %r13
 2cfeae1:      	cmpq	%r12, %r13
 2cfeae4:      	je	0x2cfe870 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1660>
 2cfeaea:      	movl	(%r13), %eax
 2cfeaee:      	movl	%eax, %ecx
 2cfeaf0:      	andl	$0x10000ff, %ecx        # imm = 0x10000FF
 2cfeaf6:      	cmpl	$0x1000000, %ecx        # imm = 0x1000000
 2cfeafc:      	setne	%cl
 2cfeaff:      	notl	%eax
 2cfeb01:      	testl	$0x5000000, %eax        # imm = 0x5000000
 2cfeb06:      	sete	%al
 2cfeb09:      	orb	%cl, %al
 2cfeb0b:      	jne	0x2cfeadd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfeb0d:      	movl	0x4(%r13), %ebp
 2cfeb11:      	movq	0x1c0(%rsp), %rax
 2cfeb19:      	movl	0x1c8(%rsp), %ecx
 2cfeb20:      	movl	%ecx, %edi
 2cfeb22:      	shrl	$0x2, %edi
 2cfeb25:      	je	0x2cfeb7c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x196c>
 2cfeb27:      	leaq	(,%rcx,4), %rdx
 2cfeb2f:      	andq	$-0x10, %rdx
 2cfeb33:      	addq	%rax, %rdx
 2cfeb36:      	incq	%rdi
 2cfeb39:      	leaq	0x8(%rax), %rsi
 2cfeb3d:      	nopl	(%rax)
 2cfeb40:      	cmpl	%ebp, -0x8(%rsi)
 2cfeb43:      	je	0x2cfebf3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19e3>
 2cfeb49:      	cmpl	%ebp, -0x4(%rsi)
 2cfeb4c:      	je	0x2cfebfc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19ec>
 2cfeb52:      	cmpl	%ebp, (%rsi)
 2cfeb54:      	je	0x2cfead0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfeb5a:      	cmpl	%ebp, 0x4(%rsi)
 2cfeb5d:      	je	0x2cfec05 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19f5>
 2cfeb63:      	decq	%rdi
 2cfeb66:      	addq	$0x10, %rsi
 2cfeb6a:      	cmpq	$0x1, %rdi
 2cfeb6e:      	jg	0x2cfeb40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1930>
 2cfeb70:      	movl	%ecx, %esi
 2cfeb72:      	andl	$0x3, %esi
 2cfeb75:      	cmpl	$0x1, %esi
 2cfeb78:      	jne	0x2cfeb86 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1976>
 2cfeb7a:      	jmp	0x2cfeba8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1998>
 2cfeb7c:      	movl	%ecx, %esi
 2cfeb7e:      	movq	%rax, %rdx
 2cfeb81:      	cmpl	$0x1, %esi
 2cfeb84:      	je	0x2cfeba8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1998>
 2cfeb86:      	cmpl	$0x2, %esi
 2cfeb89:      	je	0x2cfeb9c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x198c>
 2cfeb8b:      	cmpl	$0x3, %esi
 2cfeb8e:      	jne	0x2cfebb3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19a3>
 2cfeb90:      	cmpl	%ebp, (%rdx)
 2cfeb92:      	je	0x2cfeacc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18bc>
 2cfeb98:      	addq	$0x4, %rdx
 2cfeb9c:      	cmpl	%ebp, (%rdx)
 2cfeb9e:      	je	0x2cfeacc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18bc>
 2cfeba4:      	addq	$0x4, %rdx
 2cfeba8:      	movq	%rdx, %rsi
 2cfebab:      	cmpl	%ebp, (%rdx)
 2cfebad:      	je	0x2cfead0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfebb3:      	movq	%rbx, %rdi
 2cfebb6:      	movl	%ebp, %esi
 2cfebb8:      	xorl	%edx, %edx
 2cfebba:      	xorl	%ecx, %ecx
 2cfebbc:      	callq	0x3655740 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2cfebc1:      	cmpl	$-0x1, %eax
 2cfebc4:      	jne	0x2cfeadd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfebca:      	movl	0x1c8(%rsp), %edx
 2cfebd1:      	cmpl	0x1cc(%rsp), %edx
 2cfebd8:      	jae	0x2cfec0e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19fe>
 2cfebda:      	movq	0x1c0(%rsp), %rax
 2cfebe2:      	movl	%edx, %ecx
 2cfebe4:      	movl	%ebp, (%rax,%rcx,4)
 2cfebe7:      	incl	0x1c8(%rsp)
 2cfebee:      	jmp	0x2cfeadd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18cd>
 2cfebf3:      	addq	$-0x8, %rsi
 2cfebf7:      	jmp	0x2cfead0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfebfc:      	addq	$-0x4, %rsi
 2cfec00:      	jmp	0x2cfead0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfec05:      	addq	$0x4, %rsi
 2cfec09:      	jmp	0x2cfead0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x18c0>
 2cfec0e:      	incq	%rdx
 2cfec11:      	movl	$0x4, %ecx
 2cfec16:      	leaq	0x1c0(%rsp), %rdi
 2cfec1e:      	leaq	0x1d0(%rsp), %rsi
 2cfec26:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfec2b:      	movl	0x1c8(%rsp), %edx
 2cfec32:      	jmp	0x2cfebda <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x19ca>
 2cfec34:      	incq	%rdx
 2cfec37:      	movl	$0x8, %ecx
 2cfec3c:      	leaq	0x130(%rsp), %rdi
 2cfec44:      	leaq	0x140(%rsp), %rsi
 2cfec4c:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cfec51:      	movl	0x138(%rsp), %edx
 2cfec58:      	jmp	0x2cfe970 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1760>
 2cfec5d:      	testq	%r9, %r9
 2cfec60:      	cmovneq	%r9, %rax
 2cfec64:      	jmp	0x2cfea02 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x17f2>
 2cfec69:      	testq	%r9, %r9
 2cfec6c:      	cmovneq	%r9, %rax
 2cfec70:      	jmp	0x2cfe912 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1702>
 2cfec75:      	addl	%esi, %esi
 2cfec77:      	leaq	0x1e0(%rsp), %rdi
 2cfec7f:      	callq	0x2cbbc70 <_ZN4llvm12DenseMapBaseINS_8DenseMapIjNS_6detail13DenseSetEmptyENS_12DenseMapInfoIjvEENS2_12DenseSetPairIjEEEEjS3_S5_S7_E4growEj>
 2cfec84:      	movl	0x1f0(%rsp), %ecx
 2cfec8b:      	testl	%ecx, %ecx
 2cfec8d:      	je	0x2cfece6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad6>
 2cfec8f:      	movq	0x1e0(%rsp), %rdx
 2cfec97:      	leal	(%rbp,%rbp,8), %eax
 2cfec9b:      	leal	(%rbp,%rax,4), %esi
 2cfec9f:      	decl	%ecx
 2cfeca1:      	andl	%ecx, %esi
 2cfeca3:      	leaq	(%rdx,%rsi,4), %rax
 2cfeca7:      	movl	(%rdx,%rsi,4), %r9d
 2cfecab:      	cmpl	%r9d, %ebp
 2cfecae:      	je	0x2cfece8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfecb0:      	movl	$0x1, %edi
 2cfecb5:      	xorl	%r8d, %r8d
 2cfecb8:      	cmpl	$-0x1, %r9d
 2cfecbc:      	je	0x2cfed93 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b83>
 2cfecc2:      	testq	%r8, %r8
 2cfecc5:      	cmovneq	%r8, %rax
 2cfecc9:      	cmpl	$-0x2, %r9d
 2cfeccd:      	cmoveq	%rax, %r8
 2cfecd1:      	addl	%edi, %esi
 2cfecd3:      	incl	%edi
 2cfecd5:      	andl	%ecx, %esi
 2cfecd7:      	leaq	(%rdx,%rsi,4), %rax
 2cfecdb:      	movl	(%rdx,%rsi,4), %r9d
 2cfecdf:      	cmpl	%r9d, %ebp
 2cfece2:      	je	0x2cfece8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfece4:      	jmp	0x2cfecb8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1aa8>
 2cfece6:      	xorl	%eax, %eax
 2cfece8:      	movl	0x1e8(%rsp), %ecx
 2cfecef:      	incl	%ecx
 2cfecf1:      	movl	%ecx, 0x1e8(%rsp)
 2cfecf8:      	cmpl	$-0x1, (%rax)
 2cfecfb:      	jne	0x2cfea43 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1833>
 2cfed01:      	jmp	0x2cfea4a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x183a>
 2cfed06:      	addl	%esi, %esi
 2cfed08:      	leaq	0x200(%rsp), %rdi
 2cfed10:      	callq	0x2cbbc70 <_ZN4llvm12DenseMapBaseINS_8DenseMapIjNS_6detail13DenseSetEmptyENS_12DenseMapInfoIjvEENS2_12DenseSetPairIjEEEEjS3_S5_S7_E4growEj>
 2cfed15:      	movl	0x210(%rsp), %ecx
 2cfed1c:      	testl	%ecx, %ecx
 2cfed1e:      	je	0x2cfed73 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b63>
 2cfed20:      	movq	0x200(%rsp), %rdx
 2cfed28:      	leal	(%rbp,%rbp,8), %eax
 2cfed2c:      	leal	(%rbp,%rax,4), %esi
 2cfed30:      	decl	%ecx
 2cfed32:      	andl	%ecx, %esi
 2cfed34:      	leaq	(%rdx,%rsi,4), %rax
 2cfed38:      	movl	(%rdx,%rsi,4), %r9d
 2cfed3c:      	cmpl	%r9d, %ebp
 2cfed3f:      	je	0x2cfed75 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfed41:      	movl	$0x1, %edi
 2cfed46:      	xorl	%r8d, %r8d
 2cfed49:      	cmpl	$-0x1, %r9d
 2cfed4d:      	je	0x2cfed9f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b8f>
 2cfed4f:      	testq	%r8, %r8
 2cfed52:      	cmovneq	%r8, %rax
 2cfed56:      	cmpl	$-0x2, %r9d
 2cfed5a:      	cmoveq	%rax, %r8
 2cfed5e:      	addl	%edi, %esi
 2cfed60:      	incl	%edi
 2cfed62:      	andl	%ecx, %esi
 2cfed64:      	leaq	(%rdx,%rsi,4), %rax
 2cfed68:      	movl	(%rdx,%rsi,4), %r9d
 2cfed6c:      	cmpl	%r9d, %ebp
 2cfed6f:      	je	0x2cfed75 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfed71:      	jmp	0x2cfed49 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b39>
 2cfed73:      	xorl	%eax, %eax
 2cfed75:      	movl	0x208(%rsp), %ecx
 2cfed7c:      	incl	%ecx
 2cfed7e:      	movl	%ecx, 0x208(%rsp)
 2cfed85:      	cmpl	$-0x1, (%rax)
 2cfed88:      	jne	0x2cfe953 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1743>
 2cfed8e:      	jmp	0x2cfe95a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x174a>
 2cfed93:      	testq	%r8, %r8
 2cfed96:      	cmovneq	%r8, %rax
 2cfed9a:      	jmp	0x2cfece8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ad8>
 2cfed9f:      	testq	%r8, %r8
 2cfeda2:      	cmovneq	%r8, %rax
 2cfeda6:      	jmp	0x2cfed75 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1b65>
 2cfeda8:      	nopl	(%rax,%rax)
 2cfedb0:      	movq	0x90(%rsp), %rax
 2cfedb8:      	movq	(%rax), %r14
 2cfedbb:      	movq	0x78(%rsp), %rbx
 2cfedc0:      	movq	0x10(%rsp), %rbp
 2cfedc5:      	jmp	0x2cfedd8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bc8>
 2cfedc7:      	nopw	(%rax,%rax)
 2cfedd0:      	movq	0x90(%rsp), %rax
 2cfedd8:      	movl	0x30(%rax), %eax
 2cfeddb:      	movq	(%r14,%rax,8), %r14
 2cfeddf:      	testb	$0x4, (%r14)
 2cfede3:      	movq	%r14, %rax
 2cfede6:      	jne	0x2cfee0a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bfa>
 2cfede8:      	testb	$0x8, 0x2c(%r14)
 2cfeded:      	movq	%r14, %rax
 2cfedf0:      	je	0x2cfee0a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bfa>
 2cfedf2:      	movq	%r14, %rax
 2cfedf5:      	nopw	%cs:(%rax,%rax)
 2cfedff:      	nop
 2cfee00:      	movq	0x8(%rax), %rax
 2cfee04:      	testb	$0x8, 0x2c(%rax)
 2cfee08:      	jne	0x2cfee00 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1bf0>
 2cfee0a:      	movq	0x8(%rax), %rax
 2cfee0e:      	movq	%rax, 0x20(%rsp)
 2cfee13:      	movq	0x18(%r14), %rax
 2cfee17:      	movq	%rax, 0x10(%rsp)
 2cfee1c:      	movq	%rbp, %rdi
 2cfee1f:      	callq	0x2cf7a90 <_ZL17getMemoryOpOffsetRKN4llvm12MachineInstrE>
 2cfee24:      	movl	%eax, 0x18(%rsp)
 2cfee28:      	movq	0x20(%rbp), %rax
 2cfee2c:      	movl	0x24(%rax), %r12d
 2cfee30:      	xorl	%r15d, %r15d
 2cfee33:      	movq	%r14, %rdi
 2cfee36:      	movl	%r12d, %esi
 2cfee39:      	xorl	%edx, %edx
 2cfee3b:      	movl	$0x1, %ecx
 2cfee40:      	callq	0x3655740 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2cfee45:      	movq	%rbp, %rsi
 2cfee48:      	movl	%eax, 0x70(%rsp)
 2cfee4c:      	cmpl	$-0x1, %eax
 2cfee4f:      	setne	%r13b
 2cfee53:      	movq	0x10(%rbp), %rcx
 2cfee57:      	movl	$0xe, %r14d
 2cfee5d:      	testb	$0x40, 0x12(%rcx)
 2cfee61:      	je	0x2cfeec0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb0>
 2cfee63:      	movzwl	0x28(%rsi), %edx
 2cfee67:      	movzbl	0x2a(%rsi), %eax
 2cfee6b:      	shll	$0x10, %eax
 2cfee6e:      	orl	%edx, %eax
 2cfee70:      	testl	%eax, %eax
 2cfee72:      	je	0x2cfeec0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cb0>
 2cfee74:      	movzwl	(%rcx), %edx
 2cfee77:      	movzwl	0xa(%rcx), %esi
 2cfee7b:      	shll	$0x5, %eax
 2cfee7e:      	shll	$0x5, %edx
 2cfee81:      	leaq	(%rsi,%rsi,2), %rsi
 2cfee85:      	leaq	(%rdx,%rsi,2), %rdx
 2cfee89:      	movq	%rbp, %rsi
 2cfee8c:      	leaq	0x22(%rcx,%rdx), %rdx
 2cfee91:      	xorl	%ecx, %ecx
 2cfee93:      	nopw	%cs:(%rax,%rax)
 2cfee9d:      	nopl	(%rax)
 2cfeea0:      	testb	$0x2, (%rdx)
 2cfeea3:      	jne	0x2cff04c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e3c>
 2cfeea9:      	addq	$0x20, %rcx
 2cfeead:      	addq	$0x6, %rdx
 2cfeeb1:      	cmpq	%rcx, %rax
 2cfeeb4:      	jne	0x2cfeea0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1c90>
 2cfeeb6:      	nopw	%cs:(%rax,%rax)
 2cfeec0:      	movq	0x38(%rsi), %rsi
 2cfeec4:      	movq	%rsi, 0xc8(%rsp)
 2cfeecc:      	testq	%rsi, %rsi
 2cfeecf:      	je	0x2cfeee3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cd3>
 2cfeed1:      	movl	$0x1, %edx
 2cfeed6:      	leaq	0xc8(%rsp), %rdi
 2cfeede:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cfeee3:      	movq	0x90(%rsp), %rax
 2cfeeeb:      	cmpb	$0x0, 0x3d(%rax)
 2cfeeef:      	je	0x2cfef70 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1d60>
 2cfeef1:      	movq	%r12, 0x8(%rsp)
 2cfeef6:      	movq	%r15, 0x88(%rsp)
 2cfeefe:      	movq	$-0x102f, %rbp          # imm = 0xEFD1
 2cfef05:      	movb	$0x1, %r12b
 2cfef08:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cfef0e:      	movl	%r14d, 0x28(%rsp)
 2cfef13:      	je	0x2cff074 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e64>
 2cfef19:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cfef1f:      	leaq	0x30(%rsp), %rdx
 2cfef24:      	je	0x2cff079 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfef2a:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cfef30:      	je	0x2cff079 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfef36:      	movl	%ebx, %eax
 2cfef38:      	andl	$-0x2, %eax
 2cfef3b:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cfef40:      	sete	%r12b
 2cfef44:      	movq	$-0x1101, %rbp          # imm = 0xEEFF
 2cfef4b:      	movq	$-0x102f, %rax          # imm = 0xEFD1
 2cfef52:      	cmoveq	%rax, %rbp
 2cfef56:      	movq	0x90(%rsp), %rax
 2cfef5e:      	jmp	0x2cff079 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e69>
 2cfef63:      	nopw	%cs:(%rax,%rax)
 2cfef6d:      	nopl	(%rax)
 2cfef70:      	cmpb	$0x1, 0x3c(%rax)
 2cfef74:      	jne	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cfef7a:      	movq	%r12, 0x8(%rsp)
 2cfef7f:      	movq	%r15, 0x88(%rsp)
 2cfef87:      	movl	%r14d, 0x28(%rsp)
 2cfef8c:      	movq	0x130(%rsp), %r14
 2cfef94:      	movl	0x138(%rsp), %r9d
 2cfef9c:      	movq	(%rax), %rcx
 2cfef9f:      	movq	%rcx, 0x230(%rsp)
 2cfefa7:      	movl	0x8(%rax), %eax
 2cfefaa:      	movq	%rax, 0x228(%rsp)
 2cfefb2:      	xorl	%eax, %eax
 2cfefb4:      	movq	(%rsp), %rcx
 2cfefb8:      	cmpb	$0x1, 0x202(%rcx)
 2cfefbf:      	movl	$0x0, %r15d
 2cfefc5:      	movl	$0x0, %ecx
 2cfefca:      	jne	0x2cffb5c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cfefd0:      	movq	%r9, %r12
 2cfefd3:      	movq	(%rsp), %rbx
 2cfefd7:      	movq	0x48(%rbx), %rsi
 2cfefdb:      	movq	0x10(%rsp), %rdi
 2cfefe0:      	movl	$0x3, %edx
 2cfefe5:      	movq	0x20(%rsp), %rcx
 2cfefea:      	movl	$0x14, %r8d
 2cfeff0:      	callq	0x35d9970 <_ZNK4llvm17MachineBasicBlock23computeRegisterLivenessEPKNS_18TargetRegisterInfoENS_10MCRegisterENS_26MachineInstrBundleIteratorIKNS_12MachineInstrELb0EEEj>
 2cfeff5:      	cmpl	$0x1, %eax
 2cfeff8:      	setne	%r15b
 2cfeffc:      	xorl	%ecx, %ecx
 2cfeffe:      	xorl	%eax, %eax
 2cff000:      	cmpb	$0x1, 0x202(%rbx)
 2cff007:      	jne	0x2cffb59 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2949>
 2cff00d:      	movq	%r12, %r9
 2cff010:      	testq	%r12, %r12
 2cff013:      	je	0x2cff043 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e33>
 2cff015:      	leaq	(,%r9,8), %rax
 2cff01d:      	xorl	%ecx, %ecx
 2cff01f:      	movq	0x78(%rsp), %rbx
 2cff024:      	movq	0x8(%rsp), %r12
 2cff029:      	movl	0x18(%rsp), %r8d
 2cff02e:      	nop
 2cff030:      	cmpl	%r12d, (%r14,%rcx)
 2cff034:      	je	0x2cffde3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bd3>
 2cff03a:      	addq	$0x8, %rcx
 2cff03e:      	cmpq	%rcx, %rax
 2cff041:      	jne	0x2cff030 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1e20>
 2cff043:      	movb	$0x1, %al
 2cff045:      	movb	$0x1, %cl
 2cff047:      	jmp	0x2cffb5c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cff04c:      	movq	0x20(%rsi), %rax
 2cff050:      	movl	0x10(%rax,%rcx), %r14d
 2cff055:      	movl	0x24(%rax,%rcx), %r15d
 2cff05a:      	movq	0x38(%rsi), %rsi
 2cff05e:      	movq	%rsi, 0xc8(%rsp)
 2cff066:      	testq	%rsi, %rsi
 2cff069:      	jne	0x2cfeed1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cc1>
 2cff06f:      	jmp	0x2cfeee3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1cd3>
 2cff074:      	leaq	0x30(%rsp), %rdx
 2cff079:      	movq	0x130(%rsp), %rbx
 2cff081:      	movq	(%rax), %rcx
 2cff084:      	movq	%rcx, 0xc0(%rsp)
 2cff08c:      	movl	0x8(%rax), %r15d
 2cff090:      	movq	0xc8(%rsp), %rsi
 2cff098:      	movq	%rsi, 0xa0(%rsp)
 2cff0a0:      	movq	%rdx, %r13
 2cff0a3:      	testq	%rsi, %rsi
 2cff0a6:      	je	0x2cff0e6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ed6>
 2cff0a8:      	movl	$0x1, %edx
 2cff0ad:      	leaq	0xa0(%rsp), %rdi
 2cff0b5:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cff0ba:      	leaq	0x30(%rsp), %rdx
 2cff0bf:      	movq	0xa0(%rsp), %rsi
 2cff0c7:      	movq	%rsi, 0x30(%rsp)
 2cff0cc:      	testq	%rsi, %rsi
 2cff0cf:      	je	0x2cff0ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1ede>
 2cff0d1:      	leaq	0xa0(%rsp), %r13
 2cff0d9:      	movq	%r13, %rdi
 2cff0dc:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2cff0e1:      	leaq	0x30(%rsp), %rdx
 2cff0e6:      	movq	$0x0, (%r13)
 2cff0ee:      	leaq	0x40(%rsp), %rax
 2cff0f3:      	xorps	%xmm0, %xmm0
 2cff0f6:      	movups	%xmm0, -0x8(%rax)
 2cff0fa:      	movq	$0x0, 0x8(%rax)
 2cff102:      	movq	(%rsp), %rax
 2cff106:      	movq	0x40(%rax), %rax
 2cff10a:      	shlq	$0x5, %rbp
 2cff10e:      	addq	0x8(%rax), %rbp
 2cff112:      	movq	0x10(%rsp), %rdi
 2cff117:      	movq	0x20(%rsp), %rsi
 2cff11c:      	movq	%rdx, %r13
 2cff11f:      	movq	%rbp, %rcx
 2cff122:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2cff127:      	movq	%rax, %rbp
 2cff12a:      	movq	%rdx, %r14
 2cff12d:      	movq	0x30(%rsp), %rsi
 2cff132:      	testq	%rsi, %rsi
 2cff135:      	je	0x2cff13f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1f2f>
 2cff137:      	movq	%r13, %rdi
 2cff13a:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff13f:      	movq	0xa0(%rsp), %rsi
 2cff147:      	testq	%rsi, %rsi
 2cff14a:      	je	0x2cff159 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1f49>
 2cff14c:      	leaq	0xa0(%rsp), %rdi
 2cff154:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff159:      	movl	(%rbx), %eax
 2cff15b:      	testb	%r12b, %r12b
 2cff15e:      	je	0x2cff1b7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x1fa7>
 2cff160:      	movq	$0x0, 0x38(%rsp)
 2cff169:      	movl	%eax, 0x34(%rsp)
 2cff16d:      	leaq	0x40(%rsp), %r12
 2cff172:      	xorps	%xmm0, %xmm0
 2cff175:      	movups	%xmm0, (%r12)
 2cff17a:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2cff182:      	movq	%r14, %rdi
 2cff185:      	movq	%rbp, %rsi
 2cff188:      	leaq	0x30(%rsp), %r13
 2cff18d:      	movq	%r13, %rdx
 2cff190:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff195:      	movl	0x8(%rbx), %eax
 2cff198:      	movq	$0x0, 0x38(%rsp)
 2cff1a1:      	movl	%eax, 0x34(%rsp)
 2cff1a5:      	xorps	%xmm0, %xmm0
 2cff1a8:      	movups	%xmm0, (%r12)
 2cff1ad:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2cff1b5:      	jmp	0x2cff212 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2002>
 2cff1b7:      	movzbl	0x4(%rbx), %ecx
 2cff1bb:      	movq	$0x0, 0x38(%rsp)
 2cff1c4:      	shll	$0x1a, %ecx
 2cff1c7:      	movl	%eax, 0x34(%rsp)
 2cff1cb:      	leaq	0x40(%rsp), %r12
 2cff1d0:      	xorps	%xmm0, %xmm0
 2cff1d3:      	movups	%xmm0, (%r12)
 2cff1d8:      	movl	%ecx, 0x30(%rsp)
 2cff1dc:      	movq	%r14, %rdi
 2cff1df:      	movq	%rbp, %rsi
 2cff1e2:      	leaq	0x30(%rsp), %r13
 2cff1e7:      	movq	%r13, %rdx
 2cff1ea:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff1ef:      	movl	0x8(%rbx), %eax
 2cff1f2:      	movzbl	0xc(%rbx), %ecx
 2cff1f6:      	movq	$0x0, 0x38(%rsp)
 2cff1ff:      	shll	$0x1a, %ecx
 2cff202:      	movl	%eax, 0x34(%rsp)
 2cff206:      	xorps	%xmm0, %xmm0
 2cff209:      	movups	%xmm0, (%r12)
 2cff20e:      	movl	%ecx, 0x30(%rsp)
 2cff212:      	movq	%r14, %rdi
 2cff215:      	movq	%rbp, %rsi
 2cff218:      	movq	%r13, %rdx
 2cff21b:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff220:      	movq	$0x0, 0x38(%rsp)
 2cff229:      	movq	0x8(%rsp), %rax
 2cff22e:      	movl	%eax, 0x34(%rsp)
 2cff232:      	xorps	%xmm0, %xmm0
 2cff235:      	movups	%xmm0, (%r12)
 2cff23a:      	movl	$0x0, 0x30(%rsp)
 2cff242:      	movq	%r14, %rdi
 2cff245:      	movq	%rbp, %rsi
 2cff248:      	movq	%r13, %rdx
 2cff24b:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff250:      	movslq	0x18(%rsp), %rax
 2cff255:      	movl	$0x1, 0x30(%rsp)
 2cff25d:      	movq	$0x0, 0x38(%rsp)
 2cff266:      	movq	%rax, 0x40(%rsp)
 2cff26b:      	movq	%r14, %rdi
 2cff26e:      	movq	%rbp, %rsi
 2cff271:      	movq	%r13, %rdx
 2cff274:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff279:      	movl	0x28(%rsp), %eax
 2cff27d:      	movl	$0x1, 0x30(%rsp)
 2cff285:      	movq	$0x0, 0x38(%rsp)
 2cff28e:      	movq	%rax, 0x40(%rsp)
 2cff293:      	movq	%r14, %rdi
 2cff296:      	movq	%rbp, %rsi
 2cff299:      	movq	%r13, %rdx
 2cff29c:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff2a1:      	movq	$0x0, 0x38(%rsp)
 2cff2aa:      	movq	0x88(%rsp), %rax
 2cff2b2:      	movl	%eax, 0x34(%rsp)
 2cff2b6:      	xorps	%xmm0, %xmm0
 2cff2b9:      	movups	%xmm0, (%r12)
 2cff2be:      	movl	$0x0, 0x30(%rsp)
 2cff2c6:      	movq	%r14, %rdi
 2cff2c9:      	movq	%rbp, %rsi
 2cff2cc:      	movq	%r13, %rdx
 2cff2cf:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff2d4:      	movq	%r14, %rdi
 2cff2d7:      	movq	%rbp, %rsi
 2cff2da:      	movq	0xc0(%rsp), %rdx
 2cff2e2:      	movq	%r15, %rcx
 2cff2e5:      	callq	0x3652070 <_ZN4llvm12MachineInstr18cloneMergedMemRefsERNS_15MachineFunctionENS_8ArrayRefIPKS0_EE>
 2cff2ea:      	movq	0x90(%rsp), %rcx
 2cff2f2:      	movl	0x34(%rcx), %eax
 2cff2f5:      	movq	(%rcx), %rdx
 2cff2f8:      	movq	(%rdx,%rax,8), %rcx
 2cff2fc:      	movq	0x10(%rsp), %rax
 2cff301:      	movq	0x38(%rax), %rsi
 2cff305:      	movq	%rcx, %rax
 2cff308:      	movq	%rsi, 0xc0(%rsp)
 2cff310:      	cmpq	%rsi, %rcx
 2cff313:      	xorps	%xmm0, %xmm0
 2cff316:      	je	0x2cff343 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff318:      	movq	(%rcx), %rax
 2cff31b:      	andq	$-0x8, %rax
 2cff31f:      	testb	$0x4, (%rax)
 2cff322:      	jne	0x2cff343 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff324:      	nopw	%cs:(%rax,%rax)
 2cff32e:      	nop
 2cff330:      	testb	$0x4, 0x2c(%rax)
 2cff334:      	je	0x2cff343 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2133>
 2cff336:      	movq	(%rax), %rax
 2cff339:      	andq	$-0x8, %rax
 2cff33d:      	testb	$0x4, 0x2c(%rax)
 2cff341:      	jne	0x2cff336 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2126>
 2cff343:      	movq	%rcx, 0x88(%rsp)
 2cff34b:      	movq	%rax, 0x70(%rsp)
 2cff350:      	movq	%r14, 0x28(%rsp)
 2cff355:      	movq	0x90(%rsp), %rax
 2cff35d:      	movl	0x8(%rax), %eax
 2cff360:      	testq	%rax, %rax
 2cff363:      	je	0x2cff5c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23b0>
 2cff369:      	leaq	(%rdx,%rax,8), %rax
 2cff36d:      	movq	%rax, 0x8(%rsp)
 2cff372:      	jmp	0x2cff394 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2184>
 2cff374:      	nopw	%cs:(%rax,%rax)
 2cff37e:      	nop
 2cff380:      	movq	0x20(%rsp), %rdx
 2cff385:      	addq	$0x8, %rdx
 2cff389:      	cmpq	0x8(%rsp), %rdx
 2cff38e:      	je	0x2cff5c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23b0>
 2cff394:      	movq	%rdx, 0x20(%rsp)
 2cff399:      	movq	(%rdx), %r14
 2cff39c:      	testb	$0x4, (%r14)
 2cff3a0:      	movq	%r14, %rax
 2cff3a3:      	jne	0x2cff3ca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21ba>
 2cff3a5:      	testb	$0x8, 0x2c(%r14)
 2cff3aa:      	movq	%r14, %rax
 2cff3ad:      	je	0x2cff3ca <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21ba>
 2cff3af:      	movq	%r14, %rax
 2cff3b2:      	nopw	%cs:(%rax,%rax)
 2cff3bc:      	nopl	(%rax)
 2cff3c0:      	movq	0x8(%rax), %rax
 2cff3c4:      	testb	$0x8, 0x2c(%rax)
 2cff3c8:      	jne	0x2cff3c0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21b0>
 2cff3ca:      	movq	0x8(%rax), %rax
 2cff3ce:      	movq	%rax, 0x18(%rsp)
 2cff3d3:      	cmpq	%rax, %r14
 2cff3d6:      	jne	0x2cff417 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2207>
 2cff3d8:      	jmp	0x2cff380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2170>
 2cff3da:      	nopw	(%rax,%rax)
 2cff3e0:      	movl	%ecx, 0xf0(%r12)
 2cff3e8:      	movq	(%r15), %rax
 2cff3eb:      	movq	(%rax,%rbp,8), %rcx
 2cff3ef:      	movq	%rcx, (%rbx)
 2cff3f2:      	movq	%rbx, (%rax,%rbp,8)
 2cff3f6:      	movq	0xe0(%r12), %rax
 2cff3fe:      	movq	%rax, (%r14)
 2cff401:      	movq	%r14, 0xe0(%r12)
 2cff409:      	movq	%r13, %r14
 2cff40c:      	cmpq	0x18(%rsp), %r13
 2cff411:      	je	0x2cff380 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2170>
 2cff417:      	movq	0x8(%r14), %r13
 2cff41b:      	movq	0x18(%r14), %rax
 2cff41f:      	movq	0x20(%rax), %rbx
 2cff423:      	testq	%rbx, %rbx
 2cff426:      	je	0x2cff4e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff42c:      	movq	0x288(%rbx), %rdi
 2cff433:      	testq	%rdi, %rdi
 2cff436:      	je	0x2cff444 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2234>
 2cff438:      	movq	(%rdi), %rax
 2cff43b:      	movq	%r14, %rsi
 2cff43e:      	callq	*0x20(%rax)
 2cff441:      	xorps	%xmm0, %xmm0
 2cff444:      	movzwl	0x28(%r14), %ecx
 2cff449:      	movzbl	0x2a(%r14), %eax
 2cff44e:      	shll	$0x10, %eax
 2cff451:      	orl	%ecx, %eax
 2cff453:      	testl	%eax, %eax
 2cff455:      	je	0x2cff4e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff45b:      	movq	0x20(%r14), %rcx
 2cff45f:      	shll	$0x5, %eax
 2cff462:      	movq	0x20(%rbx), %rdx
 2cff466:      	jmp	0x2cff491 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2281>
 2cff468:      	nopl	(%rax,%rax)
 2cff470:      	movq	%rdi, 0x18(%r8)
 2cff474:      	leaq	0x10(%rcx), %r9
 2cff478:      	testq	%rdi, %rdi
 2cff47b:      	cmovneq	%rdi, %rsi
 2cff47f:      	movq	%r8, 0x10(%rsi)
 2cff483:      	movups	%xmm0, (%r9)
 2cff487:      	addq	$0x20, %rcx
 2cff48b:      	addq	$-0x20, %rax
 2cff48f:      	je	0x2cff4e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x22d0>
 2cff491:      	cmpb	$0x0, (%rcx)
 2cff494:      	jne	0x2cff487 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2277>
 2cff496:      	movl	0x4(%rcx), %esi
 2cff499:      	movl	%esi, %edi
 2cff49b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2cff4a1:      	shlq	$0x4, %rdi
 2cff4a5:      	movq	%rsi, %r8
 2cff4a8:      	shlq	$0x3, %r8
 2cff4ac:      	addq	0x128(%rdx), %r8
 2cff4b3:      	testl	%esi, %esi
 2cff4b5:      	movq	0x30(%rdx), %rsi
 2cff4b9:      	leaq	0x8(%rsi,%rdi), %r9
 2cff4be:      	cmovnsq	%r8, %r9
 2cff4c2:      	movq	(%r9), %rsi
 2cff4c5:      	movq	0x18(%rcx), %rdi
 2cff4c9:      	movq	0x10(%rcx), %r8
 2cff4cd:      	cmpq	%rsi, %rcx
 2cff4d0:      	jne	0x2cff470 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2260>
 2cff4d2:      	movq	%rdi, (%r9)
 2cff4d5:      	jmp	0x2cff474 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2264>
 2cff4d7:      	nopw	(%rax,%rax)
 2cff4e0:      	movq	$0x0, 0x18(%r14)
 2cff4e8:      	movq	(%r14), %rax
 2cff4eb:      	movq	0x8(%r14), %rcx
 2cff4ef:      	andq	$-0x8, %rax
 2cff4f3:      	movq	(%rcx), %rdx
 2cff4f6:      	andl	$0x7, %edx
 2cff4f9:      	orq	%rax, %rdx
 2cff4fc:      	movq	%rdx, (%rcx)
 2cff4ff:      	movq	%rcx, 0x8(%rax)
 2cff503:      	andq	$0x7, (%r14)
 2cff507:      	movq	$0x0, 0x8(%r14)
 2cff50f:      	movq	0x10(%rsp), %rax
 2cff514:      	movq	0x28(%rax), %rax
 2cff518:      	movq	0x20(%rax), %r12
 2cff51c:      	movq	0x20(%r14), %rbx
 2cff520:      	testq	%rbx, %rbx
 2cff523:      	je	0x2cff3f6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21e6>
 2cff529:      	movzbl	0x2b(%r14), %ebp
 2cff52e:      	leaq	0xe8(%r12), %r15
 2cff536:      	movl	0xf0(%r12), %eax
 2cff53e:      	cmpl	%ebp, %eax
 2cff540:      	ja	0x2cff3e8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d8>
 2cff546:      	leaq	0x1(%rbp), %rcx
 2cff54a:      	cmpl	%ebp, 0xf4(%r12)
 2cff552:      	ja	0x2cff57c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x236c>
 2cff554:      	leaq	0xf8(%r12), %rsi
 2cff55c:      	movl	$0x8, %ecx
 2cff561:      	movq	%r15, %rdi
 2cff564:      	leaq	0x1(%rbp), %rdx
 2cff568:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2cff56d:      	leaq	0x1(%rbp), %rcx
 2cff571:      	xorps	%xmm0, %xmm0
 2cff574:      	movl	0xf0(%r12), %eax
 2cff57c:      	cmpl	%eax, %ecx
 2cff57e:      	je	0x2cff3e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d0>
 2cff584:      	movl	%eax, %eax
 2cff586:      	leaq	(,%rax,8), %rdi
 2cff58e:      	addq	(%r15), %rdi
 2cff591:      	movq	%rcx, %r15
 2cff594:      	movq	%rcx, %rdx
 2cff597:      	subq	%rax, %rdx
 2cff59a:      	shlq	$0x3, %rdx
 2cff59e:      	xorl	%esi, %esi
 2cff5a0:      	callq	0x828ac20 <memset@plt>
 2cff5a5:      	movq	%r15, %rcx
 2cff5a8:      	leaq	0xe8(%r12), %r15
 2cff5b0:      	xorps	%xmm0, %xmm0
 2cff5b3:      	jmp	0x2cff3e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x21d0>
 2cff5b8:      	nopl	(%rax,%rax)
 2cff5c0:      	movq	0xc0(%rsp), %rax
 2cff5c8:      	cmpq	%rax, 0x88(%rsp)
 2cff5d0:      	je	0x2cff5ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23de>
 2cff5d2:      	movq	0x70(%rsp), %rax
 2cff5d7:      	testb	$0x4, (%rax)
 2cff5da:      	movl	$0x20000ff, %ebx        # imm = 0x20000FF
 2cff5df:      	jne	0x2cff5e7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x23d7>
 2cff5e1:      	testb	$0x8, 0x2c(%rax)
 2cff5e5:      	jne	0x2cff62e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x241e>
 2cff5e7:      	movq	0x28(%rsp), %r13
 2cff5ec:      	jmp	0x2cff64a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x243a>
 2cff5ee:      	movq	0x10(%rsp), %rax
 2cff5f3:      	addq	$0x38, %rax
 2cff5f7:      	movl	$0x20000ff, %ebx        # imm = 0x20000FF
 2cff5fc:      	movq	0x28(%rsp), %r13
 2cff601:      	movq	(%rax), %rax
 2cff604:      	movq	0x78(%rsp), %rdx
 2cff609:      	cmpl	$0x104b, %edx           # imm = 0x104B
 2cff60f:      	jg	0x2cff65e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x244e>
 2cff611:      	cmpl	$0x3d7, %edx            # imm = 0x3D7
 2cff617:      	je	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff619:      	cmpl	$0xb51, %edx            # imm = 0xB51
 2cff61f:      	je	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff621:      	cmpl	$0xb53, %edx            # imm = 0xB53
 2cff627:      	je	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff629:      	jmp	0x2cff7d4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c4>
 2cff62e:      	movq	0x28(%rsp), %r13
 2cff633:      	nopw	%cs:(%rax,%rax)
 2cff63d:      	nopl	(%rax)
 2cff640:      	movq	0x8(%rax), %rax
 2cff644:      	testb	$0x8, 0x2c(%rax)
 2cff648:      	jne	0x2cff640 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2430>
 2cff64a:      	addq	$0x8, %rax
 2cff64e:      	movq	(%rax), %rax
 2cff651:      	movq	0x78(%rsp), %rdx
 2cff656:      	cmpl	$0x104b, %edx           # imm = 0x104B
 2cff65c:      	jle	0x2cff611 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2401>
 2cff65e:      	leal	-0x104c(%rdx), %ecx
 2cff664:      	cmpl	$0x2, %ecx
 2cff667:      	jb	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff669:      	cmpl	$0x117a, %edx           # imm = 0x117A
 2cff66f:      	je	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff671:      	cmpl	$0x117d, %edx           # imm = 0x117D
 2cff677:      	je	0x2cff684 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2474>
 2cff679:      	jmp	0x2cff7d4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c4>
 2cff67e:      	nop
 2cff680:      	movq	0x8(%rax), %rax
 2cff684:      	cmpq	%r13, %rax
 2cff687:      	je	0x2cff920 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2710>
 2cff68d:      	movl	0x1c8(%rsp), %edx
 2cff694:      	testq	%rdx, %rdx
 2cff697:      	je	0x2cff7a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2590>
 2cff69d:      	movq	0x1c0(%rsp), %rcx
 2cff6a5:      	leaq	(%rcx,%rdx,4), %rdx
 2cff6a9:      	jmp	0x2cff6bd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24ad>
 2cff6ab:      	nopl	(%rax,%rax)
 2cff6b0:      	addq	$0x4, %rcx
 2cff6b4:      	cmpq	%rdx, %rcx
 2cff6b7:      	je	0x2cff7a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2590>
 2cff6bd:      	movq	0x10(%rax), %r9
 2cff6c1:      	movq	0x20(%rax), %rsi
 2cff6c5:      	movzwl	0x28(%rax), %r8d
 2cff6ca:      	movzbl	0x2a(%rax), %edi
 2cff6ce:      	shll	$0x10, %edi
 2cff6d1:      	orq	%r8, %rdi
 2cff6d4:      	movzwl	0x2(%r9), %r8d
 2cff6d9:      	testb	$0x2, 0x10(%r9)
 2cff6de:      	je	0x2cff720 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff6e0:      	movl	%r8d, %r9d
 2cff6e3:      	cmpq	%rdi, %r9
 2cff6e6:      	je	0x2cff720 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff6e8:      	movl	%edi, %r10d
 2cff6eb:      	shll	$0x5, %r10d
 2cff6ef:      	shll	$0x5, %r9d
 2cff6f3:      	nopw	%cs:(%rax,%rax)
 2cff6fd:      	nopl	(%rax)
 2cff700:      	movl	(%rsi,%r9), %r11d
 2cff704:      	andl	%ebx, %r11d
 2cff707:      	cmpl	$0x2000000, %r11d       # imm = 0x2000000
 2cff70e:      	je	0x2cff720 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2510>
 2cff710:      	incl	%r8d
 2cff713:      	addq	$0x20, %r9
 2cff717:      	cmpq	%r9, %r10
 2cff71a:      	jne	0x2cff700 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24f0>
 2cff71c:      	nopl	(%rax)
 2cff720:      	movl	%r8d, %r8d
 2cff723:      	cmpq	%rdi, %r8
 2cff726:      	je	0x2cff6b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24a0>
 2cff728:      	shll	$0x5, %edi
 2cff72b:      	shlq	$0x5, %r8
 2cff72f:      	jmp	0x2cff74d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x253d>
 2cff731:      	orl	$0x10000000, %r9d       # imm = 0x10000000
 2cff738:      	movl	%r9d, (%rsi,%r8)
 2cff73c:      	nopl	(%rax)
 2cff740:      	addq	$0x20, %r8
 2cff744:      	cmpq	%r8, %rdi
 2cff747:      	je	0x2cff6b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x24a0>
 2cff74d:      	movl	(%rsi,%r8), %r9d
 2cff751:      	testb	%r9b, %r9b
 2cff754:      	jne	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff756:      	movl	0x4(%rsi,%r8), %r10d
 2cff75b:      	cmpl	(%rcx), %r10d
 2cff75e:      	jne	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff760:      	testl	$0x30000000, %r9d       # imm = 0x30000000
 2cff767:      	setne	%r10b
 2cff76b:      	movl	%r9d, %r11d
 2cff76e:      	andl	$0x10fff00, %r11d       # imm = 0x10FFF00
 2cff775:      	cmpl	$0x1000000, %r11d       # imm = 0x1000000
 2cff77c:      	sete	%r11b
 2cff780:      	orb	%r10b, %r11b
 2cff783:      	je	0x2cff731 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2521>
 2cff785:      	testl	$0x1000000, %r9d        # imm = 0x1000000
 2cff78c:      	je	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff78e:      	movl	$0x0, (%rcx)
 2cff794:      	jmp	0x2cff740 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2530>
 2cff796:      	nopw	%cs:(%rax,%rax)
 2cff7a0:      	testb	$0x4, (%rax)
 2cff7a3:      	jne	0x2cff680 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff7a9:      	nopl	(%rax)
 2cff7b0:      	testb	$0x8, 0x2c(%rax)
 2cff7b4:      	je	0x2cff680 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff7ba:      	movq	0x8(%rax), %rax
 2cff7be:      	testb	$0x8, 0x2c(%rax)
 2cff7c2:      	jne	0x2cff7ba <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25aa>
 2cff7c4:      	jmp	0x2cff680 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2470>
 2cff7c9:      	nopl	(%rax)
 2cff7d0:      	movq	0x8(%rax), %rax
 2cff7d4:      	cmpq	%r13, %rax
 2cff7d7:      	je	0x2cff99d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x278d>
 2cff7dd:      	movq	0x10(%rax), %rdi
 2cff7e1:      	movq	0x20(%rax), %rsi
 2cff7e5:      	movzwl	0x28(%rax), %edx
 2cff7e9:      	movzbl	0x2a(%rax), %ecx
 2cff7ed:      	shll	$0x10, %ecx
 2cff7f0:      	orq	%rdx, %rcx
 2cff7f3:      	movzbl	0x4(%rdi), %edx
 2cff7f7:      	testb	$0x2, 0x10(%rdi)
 2cff7fb:      	je	0x2cff804 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff7fd:      	movl	%edx, %edi
 2cff7ff:      	cmpq	%rcx, %rdi
 2cff802:      	jne	0x2cff840 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2630>
 2cff804:      	movl	%edx, %edx
 2cff806:      	cmpq	%rcx, %rdx
 2cff809:      	jne	0x2cff830 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2620>
 2cff80b:      	testb	$0x4, (%rax)
 2cff80e:      	jne	0x2cff7d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff810:      	testb	$0x8, 0x2c(%rax)
 2cff814:      	je	0x2cff7d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff816:      	movq	0x8(%rax), %rax
 2cff81a:      	testb	$0x8, 0x2c(%rax)
 2cff81e:      	jne	0x2cff816 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2606>
 2cff820:      	jmp	0x2cff7d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25c0>
 2cff822:      	nopw	%cs:(%rax,%rax)
 2cff82c:      	nopl	(%rax)
 2cff830:      	shll	$0x5, %ecx
 2cff833:      	addq	%rsi, %rcx
 2cff836:      	shlq	$0x5, %rdx
 2cff83a:      	addq	%rsi, %rdx
 2cff83d:      	jmp	0x2cff8bd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26ad>
 2cff83f:      	nop
 2cff840:      	movl	%ecx, %r8d
 2cff843:      	shll	$0x5, %r8d
 2cff847:      	addq	$-0x20, %r8
 2cff84b:      	shll	$0x5, %edi
 2cff84e:      	nop
 2cff850:      	movl	(%rsi,%rdi), %r9d
 2cff854:      	movl	%r9d, %r10d
 2cff857:      	andl	$0x10000ff, %r10d       # imm = 0x10000FF
 2cff85e:      	cmpl	$0x1000000, %r10d       # imm = 0x1000000
 2cff865:      	jne	0x2cff804 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff867:      	shrl	$0x19, %r9d
 2cff86b:      	andl	$0x1, %r9d
 2cff86f:      	movl	%r9d, %r10d
 2cff872:      	xorl	$0x1, %r10d
 2cff876:      	addl	%r10d, %edx
 2cff879:      	testl	%r9d, %r9d
 2cff87c:      	jne	0x2cff804 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff87e:      	cmpq	%rdi, %r8
 2cff881:      	leaq	0x20(%rdi), %rdi
 2cff885:      	jne	0x2cff850 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2640>
 2cff887:      	jmp	0x2cff804 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25f4>
 2cff88c:      	cmpl	$-0x1, %ebx
 2cff88f:      	je	0x2cff8b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff891:      	addl	%r11d, %r10d
 2cff894:      	incl	%r11d
 2cff897:      	andl	%edi, %r10d
 2cff89a:      	movl	(%r9,%r10,4), %ebx
 2cff89e:      	cmpl	%ebx, %r8d
 2cff8a1:      	jne	0x2cff88c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x267c>
 2cff8a3:      	andl	$0xfbffff00, %esi       # imm = 0xFBFFFF00
 2cff8a9:      	movl	%esi, (%rdx)
 2cff8ab:      	nopl	(%rax,%rax)
 2cff8b0:      	addq	$0x20, %rdx
 2cff8b4:      	cmpq	%rcx, %rdx
 2cff8b7:      	je	0x2cff80b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x25fb>
 2cff8bd:      	movl	(%rdx), %esi
 2cff8bf:      	testb	%sil, %sil
 2cff8c2:      	jne	0x2cff8b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff8c4:      	movl	%esi, %edi
 2cff8c6:      	shrl	$0x1a, %edi
 2cff8c9:      	xorl	%r8d, %r8d
 2cff8cc:      	testl	$0x1000000, %esi        # imm = 0x1000000
 2cff8d2:      	sete	%r8b
 2cff8d6:      	testl	%edi, %r8d
 2cff8d9:      	je	0x2cff8b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff8db:      	movl	0x1f0(%rsp), %edi
 2cff8e2:      	testl	%edi, %edi
 2cff8e4:      	je	0x2cff8b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x26a0>
 2cff8e6:      	movl	0x4(%rdx), %r8d
 2cff8ea:      	movq	0x1e0(%rsp), %r9
 2cff8f2:      	leal	(%r8,%r8,8), %r10d
 2cff8f6:      	leal	(%r8,%r10,4), %r10d
 2cff8fa:      	decl	%edi
 2cff8fc:      	andl	%edi, %r10d
 2cff8ff:      	movl	(%r9,%r10,4), %ebx
 2cff903:      	cmpl	%ebx, %r8d
 2cff906:      	je	0x2cff8a3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2693>
 2cff908:      	movl	$0x1, %r11d
 2cff90e:      	jmp	0x2cff88c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x267c>
 2cff913:      	nopw	%cs:(%rax,%rax)
 2cff91d:      	nopl	(%rax)
 2cff920:      	movl	0x1c8(%rsp), %eax
 2cff927:      	movq	%rax, 0x18(%rsp)
 2cff92c:      	testq	%rax, %rax
 2cff92f:      	je	0x2cff99d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x278d>
 2cff931:      	movq	0x18(%r13), %rax
 2cff935:      	movq	0x20(%rax), %rbx
 2cff939:      	movq	0x1c0(%rsp), %r15
 2cff941:      	shlq	$0x2, 0x18(%rsp)
 2cff947:      	xorl	%r12d, %r12d
 2cff94a:      	movq	%r13, %r14
 2cff94d:      	leaq	0x40(%rsp), %r13
 2cff952:      	leaq	0x30(%rsp), %rbp
 2cff957:      	nopw	(%rax,%rax)
 2cff960:      	movl	(%r15,%r12), %eax
 2cff964:      	movq	$0x0, 0x38(%rsp)
 2cff96d:      	movl	%eax, 0x34(%rsp)
 2cff971:      	movups	%xmm0, (%r13)
 2cff976:      	movl	$0x3000000, 0x30(%rsp)  # imm = 0x3000000
 2cff97e:      	movq	%r14, %rdi
 2cff981:      	movq	%rbx, %rsi
 2cff984:      	movq	%rbp, %rdx
 2cff987:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2cff98c:      	xorps	%xmm0, %xmm0
 2cff98f:      	addq	$0x4, %r12
 2cff993:      	cmpq	%r12, 0x18(%rsp)
 2cff998:      	jne	0x2cff960 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2750>
 2cff99a:      	movq	%r14, %r13
 2cff99d:      	movq	0xc8(%rsp), %rsi
 2cff9a5:      	testq	%rsi, %rsi
 2cff9a8:      	je	0x2cff9b7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27a7>
 2cff9aa:      	leaq	0xc8(%rsp), %rdi
 2cff9b2:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2cff9b7:      	movq	0x1e0(%rsp), %rdi
 2cff9bf:      	movl	0x1f0(%rsp), %esi
 2cff9c6:      	shlq	$0x2, %rsi
 2cff9ca:      	movl	$0x4, %edx
 2cff9cf:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 2cff9d4:      	movq	0x200(%rsp), %rdi
 2cff9dc:      	movl	0x210(%rsp), %esi
 2cff9e3:      	shlq	$0x2, %rsi
 2cff9e7:      	movl	$0x4, %edx
 2cff9ec:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 2cff9f1:      	movq	0x1c0(%rsp), %rdi
 2cff9f9:      	leaq	0x1d0(%rsp), %rax
 2cffa01:      	cmpq	%rax, %rdi
 2cffa04:      	je	0x2cffa0b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27fb>
 2cffa06:      	callq	0x828a6d0 <free@plt>
 2cffa0b:      	movq	0x130(%rsp), %rdi
 2cffa13:      	leaq	0x140(%rsp), %rax
 2cffa1b:      	cmpq	%rax, %rdi
 2cffa1e:      	je	0x2cffa25 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2815>
 2cffa20:      	callq	0x828a6d0 <free@plt>
 2cffa25:      	testq	%r13, %r13
 2cffa28:      	je	0x2cffa60 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2850>
 2cffa2a:      	movzwl	0x44(%r13), %eax
 2cffa2f:      	cmpl	$0x1101, %eax           # imm = 0x1101
 2cffa34:      	movq	(%rsp), %rdi
 2cffa38:      	je	0x2cffa41 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2831>
 2cffa3a:      	cmpl	$0x102f, %eax           # imm = 0x102F
 2cffa3f:      	jne	0x2cffab4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x28a4>
 2cffa41:      	movq	%r13, %rsi
 2cffa44:      	callq	0x2d029d0 <_ZNK12_GLOBAL__N_115ARMLoadStoreOpt23MergeBaseUpdateLSDoubleERN4llvm12MachineInstrE>
 2cffa49:      	movq	(%rsp), %rdi
 2cffa4d:      	movb	$0x1, %al
 2cffa4f:      	jmp	0x2cfe74c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cffa54:      	nopw	%cs:(%rax,%rax)
 2cffa5e:      	nop
 2cffa60:      	movq	0x90(%rsp), %rax
 2cffa68:      	movl	0x8(%rax), %ebx
 2cffa6b:      	testq	%rbx, %rbx
 2cffa6e:      	movq	(%rsp), %rdi
 2cffa72:      	je	0x2cffb4c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x293c>
 2cffa78:      	movq	(%rax), %r14
 2cffa7b:      	shlq	$0x3, %rbx
 2cffa7f:      	xorl	%r15d, %r15d
 2cffa82:      	movq	0x98(%rsp), %rax
 2cffa8a:      	nopw	(%rax,%rax)
 2cffa90:      	movq	(%r14,%r15), %rsi
 2cffa94:      	movq	%rax, %r12
 2cffa97:      	callq	0x2d033e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt24MergeBaseUpdateLoadStoreEPN4llvm12MachineInstrE>
 2cffa9c:      	movq	(%rsp), %rdi
 2cffaa0:      	orb	%al, %r12b
 2cffaa3:      	movq	%r12, %rax
 2cffaa6:      	addq	$0x8, %r15
 2cffaaa:      	cmpq	%r15, %rbx
 2cffaad:      	jne	0x2cffa90 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2880>
 2cffaaf:      	jmp	0x2cfe74c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cffab4:      	cmpb	$0x0, 0x202(%rdi)
 2cffabb:      	jne	0x2cffa4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x283d>
 2cffabd:      	movq	%rax, 0x20(%rsp)
 2cffac2:      	movq	0x10(%r13), %rcx
 2cffac6:      	movq	0x20(%r13), %rax
 2cffaca:      	movl	(%rax), %r12d
 2cffacd:      	testl	$0x1000000, %r12d       # imm = 0x1000000
 2cffad4:      	sete	%r14b
 2cffad8:      	movl	$0xe, 0x8(%rsp)
 2cffae0:      	xorl	%ebx, %ebx
 2cffae2:      	testb	$0x40, 0x12(%rcx)
 2cffae6:      	je	0x2cffe0d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffaec:      	movzwl	0x28(%r13), %edx
 2cffaf1:      	movzbl	0x2a(%r13), %esi
 2cffaf6:      	shll	$0x10, %esi
 2cffaf9:      	orl	%edx, %esi
 2cffafb:      	testl	%esi, %esi
 2cffafd:      	je	0x2cffe0d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffb03:      	movzwl	(%rcx), %edi
 2cffb06:      	movzwl	0xa(%rcx), %r8d
 2cffb0b:      	leaq	0x10(%rax), %rdx
 2cffb0f:      	addl	%esi, %esi
 2cffb11:      	leaq	(%rsi,%rsi,2), %rsi
 2cffb15:      	shll	$0x5, %edi
 2cffb18:      	leaq	(%r8,%r8,2), %r8
 2cffb1c:      	leaq	(%rdi,%r8,2), %rdi
 2cffb20:      	leaq	0x22(%rcx,%rdi), %rcx
 2cffb25:      	xorl	%edi, %edi
 2cffb27:      	nopw	(%rax,%rax)
 2cffb30:      	testb	$0x2, (%rcx,%rdi)
 2cffb34:      	jne	0x2cffe04 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bf4>
 2cffb3a:      	addq	$0x20, %rdx
 2cffb3e:      	addq	$0x6, %rdi
 2cffb42:      	cmpq	%rdi, %rsi
 2cffb45:      	jne	0x2cffb30 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2920>
 2cffb47:      	jmp	0x2cffe0d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2bfd>
 2cffb4c:      	movq	0x98(%rsp), %rax
 2cffb54:      	jmp	0x2cfe74c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x153c>
 2cffb59:      	movq	%r12, %r9
 2cffb5c:      	movb	$0x1, %dl
 2cffb5e:      	movq	0x78(%rsp), %rbx
 2cffb63:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffb69:      	je	0x2cffb9b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x298b>
 2cffb6b:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffb71:      	movq	0x8(%rsp), %r12
 2cffb76:      	movl	0x18(%rsp), %r8d
 2cffb7b:      	je	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffb7d:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffb83:      	je	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffb85:      	movl	%ebx, %esi
 2cffb87:      	andl	$-0x2, %esi
 2cffb8a:      	cmpl	$0x104c, %esi           # imm = 0x104C
 2cffb90:      	jne	0x2cffdad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b9d>
 2cffb96:      	movl	%eax, %r10d
 2cffb99:      	jmp	0x2cffba8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2998>
 2cffb9b:      	movl	%eax, %r10d
 2cffb9e:      	movq	0x8(%rsp), %r12
 2cffba3:      	movl	0x18(%rsp), %r8d
 2cffba8:      	movq	(%rsp), %rsi
 2cffbac:      	movzbl	0x203(%rsi), %esi
 2cffbb3:      	orb	%sil, %cl
 2cffbb6:      	sete	%cl
 2cffbb9:      	andb	%dl, %cl
 2cffbbb:      	cmpl	$0x4, %r8d
 2cffbbf:      	jne	0x2cffbe0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29d0>
 2cffbc1:      	testb	%cl, %cl
 2cffbc3:      	je	0x2cffbe0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29d0>
 2cffbc5:      	xorl	%eax, %eax
 2cffbc7:      	movl	$0x2, %ecx
 2cffbcc:      	movb	$0x1, %sil
 2cffbcf:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffbd5:      	jne	0x2cffcc9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2cffbdb:      	jmp	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffbe0:      	leal	(,%r9,4), %edi
 2cffbe8:      	movl	%r8d, %r11d
 2cffbeb:      	movl	$0x4, %r8d
 2cffbf1:      	subl	%edi, %r8d
 2cffbf4:      	cmpl	%r8d, %r11d
 2cffbf7:      	sete	%r8b
 2cffbfb:      	testb	%cl, %r8b
 2cffbfe:      	je	0x2cffc0a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x29fa>
 2cffc00:      	movl	$0x3, %ecx
 2cffc05:      	jmp	0x2cffcbc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2aac>
 2cffc0a:      	negl	%edi
 2cffc0c:      	cmpl	%edi, %r11d
 2cffc0f:      	setne	%cl
 2cffc12:      	xorb	$0x1, %dl
 2cffc15:      	orb	%dl, %al
 2cffc17:      	orb	%cl, %al
 2cffc19:      	cmpb	$0x1, %al
 2cffc1b:      	jne	0x2cffcb7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2aa7>
 2cffc21:      	testl	%r11d, %r11d
 2cffc24:      	je	0x2d00666 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3456>
 2cffc2a:      	cmpl	$0x3, %r9d
 2cffc2e:      	setb	%al
 2cffc31:      	orb	%r15b, %al
 2cffc34:      	jne	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffc3a:      	movq	0x78(%rsp), %rbx
 2cffc3f:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffc45:      	je	0x2cffc67 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffc47:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffc4d:      	je	0x2cffc67 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffc4f:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffc55:      	je	0x2cffc67 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a57>
 2cffc57:      	movl	%ebx, %eax
 2cffc59:      	andl	$-0x2, %eax
 2cffc5c:      	cmpl	$0x104c, %eax           # imm = 0x104C
 2cffc61:      	jne	0x2d012cc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40bc>
 2cffc67:      	leal	-0x1(%r9), %eax
 2cffc6b:      	movl	(%r14,%rax,8), %r12d
 2cffc6f:      	xorl	%eax, %eax
 2cffc71:      	movq	(%rsp), %rcx
 2cffc75:      	movl	0x18(%rsp), %r8d
 2cffc7a:      	movl	%eax, 0xdc(%rsp)
 2cffc81:      	testb	%sil, %sil
 2cffc84:      	je	0x2d01680 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4470>
 2cffc8a:      	cmpl	$-0x1, 0x70(%rsp)
 2cffc8f:      	setne	%al
 2cffc92:      	cmpl	$0x11, 0x8(%rsp)
 2cffc97:      	sete	%cl
 2cffc9a:      	andb	%al, %cl
 2cffc9c:      	movzbl	%cl, %eax
 2cffc9f:      	movq	%r9, %rbx
 2cffca2:      	testl	%r8d, %r8d
 2cffca5:      	js	0x2d012bd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40ad>
 2cffcab:      	leal	0xfc5(,%rax,4), %esi
 2cffcb2:      	jmp	0x2d016e5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d5>
 2cffcb7:      	movl	$0x4, %ecx
 2cffcbc:      	xorl	%eax, %eax
 2cffcbe:      	movb	$0x1, %sil
 2cffcc1:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffcc7:      	je	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffcc9:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffccf:      	je	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffcd1:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2cffcd7:      	je	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2cffcd9:      	movl	%ebx, %edx
 2cffcdb:      	andl	$-0x2, %edx
 2cffcde:      	cmpl	$0x104c, %edx           # imm = 0x104C
 2cffce4:      	sete	%sil
 2cffce8:      	cmpl	$0xb51, 0xc0(%rsp)      # imm = 0xB51
 2cffcf3:      	sete	%dil
 2cffcf7:      	cmpl	$0x104b, %ebx           # imm = 0x104B
 2cffcfd:      	jle	0x2cffd28 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b18>
 2cffcff:      	leal	-0x117a(%rbx), %ecx
 2cffd05:      	cmpl	$0x1f, %ecx
 2cffd08:      	jbe	0x2cffd58 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b48>
 2cffd0a:      	leal	-0x104c(%rbx), %ecx
 2cffd10:      	movzbl	%al, %eax
 2cffd13:      	cmpl	$0x2, %ecx
 2cffd16:      	jae	0x2cffda1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b91>
 2cffd1c:      	leal	0x1022(%rax,%rax), %ebx
 2cffd23:      	jmp	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd28:      	cmpl	$0xb52, %ebx            # imm = 0xB52
 2cffd2e:      	jg	0x2cffd77 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2b67>
 2cffd30:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2cffd36:      	je	0x2cffff8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2de8>
 2cffd3c:      	cmpl	$0x7f9, %ebx            # imm = 0x7F9
 2cffd42:      	jne	0x2d00013 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e03>
 2cffd48:      	leaq	-0x1edc07f(%rip), %rax  # 0xe23cd0 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.150>
 2cffd4f:      	movl	-0x4(%rax,%rcx,4), %ebx
 2cffd53:      	jmp	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd58:      	movl	$0x1173, %ebx           # imm = 0x1173
 2cffd5d:      	leaq	-0x19b0bfc(%rip), %rdx  # 0x134f168 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x4d2>
 2cffd64:      	movslq	(%rdx,%rcx,4), %rax
 2cffd68:      	addq	%rdx, %rax
 2cffd6b:      	jmpq	*%rax
 2cffd6d:      	movl	$0x1192, %ebx           # imm = 0x1192
 2cffd72:      	jmp	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd77:      	cmpl	$0xb53, %ebx            # imm = 0xB53
 2cffd7d:      	je	0x2d00005 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2df5>
 2cffd83:      	cmpl	$0xf2e, %ebx            # imm = 0xF2E
 2cffd89:      	jne	0x2d00021 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e11>
 2cffd8f:      	movl	$0xf28, %ebx            # imm = 0xF28
 2cffd94:      	testb	%al, %al
 2cffd96:      	jne	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffd9c:      	jmp	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffda1:      	leal	0x10f5(%rax,%rax), %ebx
 2cffda8:      	jmp	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2cffdad:      	cmpl	$0x7f9, %ebx            # imm = 0x7F9
 2cffdb3:      	je	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffdb9:      	cmpl	$0x1197, %ebx           # imm = 0x1197
 2cffdbf:      	je	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffdc5:      	cmpl	$0x1199, %ebx           # imm = 0x1199
 2cffdcb:      	je	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffdd1:      	leal	-0x110f(%rbx), %edx
 2cffdd7:      	cmpw	$0x2, %dx
 2cffddb:      	setb	%dl
 2cffdde:      	jmp	0x2cffb96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2986>
 2cffde3:      	movb	$0x1, %al
 2cffde5:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2cffdeb:      	je	0x2d00de2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bd2>
 2cffdf1:      	movb	$0x1, %cl
 2cffdf3:      	cmpl	$0x1197, %ebx           # imm = 0x1197
 2cffdf9:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2cffdff:      	jmp	0x2cffb5c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x294c>
 2cffe04:      	movl	(%rdx), %ecx
 2cffe06:      	movl	%ecx, 0x8(%rsp)
 2cffe0a:      	movl	0x14(%rdx), %ebx
 2cffe0d:      	movl	0x4(%rax), %ebp
 2cffe10:      	movq	0x38(%r13), %rsi
 2cffe14:      	movq	%rsi, 0xa0(%rsp)
 2cffe1c:      	testq	%rsi, %rsi
 2cffe1f:      	je	0x2cffe37 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c27>
 2cffe21:      	movl	$0x1, %edx
 2cffe26:      	leaq	0xa0(%rsp), %rdi
 2cffe2e:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2cffe33:      	movq	0x20(%r13), %rax
 2cffe37:      	movzwl	0x28(%r13), %edx
 2cffe3c:      	movzbl	0x2a(%r13), %ecx
 2cffe41:      	shll	$0x10, %ecx
 2cffe44:      	orl	%edx, %ecx
 2cffe46:      	cmpl	$0x2, %ecx
 2cffe49:      	je	0x2cffe73 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c63>
 2cffe4b:      	shll	$0x5, %ecx
 2cffe4e:      	addq	$-0x40, %rcx
 2cffe52:      	xorl	%edx, %edx
 2cffe54:      	nopw	%cs:(%rax,%rax)
 2cffe5e:      	nop
 2cffe60:      	cmpl	%ebp, 0x44(%rax,%rdx)
 2cffe64:      	je	0x2d0108b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2cffe6a:      	addq	$0x20, %rdx
 2cffe6e:      	cmpq	%rdx, %rcx
 2cffe71:      	jne	0x2cffe60 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2c50>
 2cffe73:      	movl	%ebp, 0x90(%rsp)
 2cffe7a:      	movq	%r13, %rdi
 2cffe7d:      	callq	0x2cf9dd0 <_ZL25getLSMultipleTransferSizePKN4llvm12MachineInstrE>
 2cffe82:      	movl	%eax, 0x10(%rsp)
 2cffe86:      	movq	0x18(%r13), %rcx
 2cffe8a:      	movl	$0x0, 0x1c0(%rsp)
 2cffe95:      	movq	0x38(%rcx), %rax
 2cffe99:      	movq	%rcx, 0x18(%rsp)
 2cffe9e:      	leaq	0x30(%rcx), %r15
 2cffea2:      	cmpq	%rax, %r13
 2cffea5:      	movl	%ebx, 0x78(%rsp)
 2cffea9:      	je	0x2cfff49 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d39>
 2cffeaf:      	movq	(%r13), %rbp
 2cffeb3:      	andq	$-0x8, %rbp
 2cffeb7:      	testb	$0x4, (%rbp)
 2cffebb:      	jne	0x2cffed4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cc4>
 2cffebd:      	nopl	(%rax)
 2cffec0:      	testb	$0x4, 0x2c(%rbp)
 2cffec4:      	je	0x2cffed4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cc4>
 2cffec6:      	movq	(%rbp), %rbp
 2cffeca:      	andq	$-0x8, %rbp
 2cffece:      	testb	$0x4, 0x2c(%rbp)
 2cffed2:      	jne	0x2cffec6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cb6>
 2cffed4:      	cmpq	%rax, %rbp
 2cffed7:      	je	0x2cfff25 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cffed9:      	movl	0x44(%rbp), %ecx
 2cffedc:      	addl	$-0xe, %ecx
 2cffedf:      	cmpw	$0x4, %cx
 2cffee3:      	ja	0x2cfff25 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cffee5:      	nopw	%cs:(%rax,%rax)
 2cffeef:      	nop
 2cffef0:      	movq	(%rbp), %rbp
 2cffef4:      	andq	$-0x8, %rbp
 2cffef8:      	testb	$0x4, (%rbp)
 2cffefc:      	jne	0x2cfff14 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d04>
 2cffefe:      	nop
 2cfff00:      	testb	$0x4, 0x2c(%rbp)
 2cfff04:      	je	0x2cfff14 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d04>
 2cfff06:      	movq	(%rbp), %rbp
 2cfff0a:      	andq	$-0x8, %rbp
 2cfff0e:      	testb	$0x4, 0x2c(%rbp)
 2cfff12:      	jne	0x2cfff06 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2cf6>
 2cfff14:      	cmpq	%rax, %rbp
 2cfff17:      	je	0x2cfff25 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d15>
 2cfff19:      	movl	0x44(%rbp), %ecx
 2cfff1c:      	addl	$-0xe, %ecx
 2cfff1f:      	cmpw	$0x5, %cx
 2cfff23:      	jb	0x2cffef0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ce0>
 2cfff25:      	movq	%rbp, %rdi
 2cfff28:      	movl	0x90(%rsp), %esi
 2cfff2f:      	movl	0x8(%rsp), %edx
 2cfff33:      	movl	%ebx, %ecx
 2cfff35:      	callq	0x2d05320 <_ZL22isIncrementOrDecrementRKN4llvm12MachineInstrENS_8RegisterENS_5ARMCC9CondCodesES3_>
 2cfff3a:      	movl	%eax, 0x1c0(%rsp)
 2cfff41:      	testl	%eax, %eax
 2cfff43:      	cmoveq	%r15, %rbp
 2cfff47:      	jmp	0x2cfff4e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d3e>
 2cfff49:      	xorl	%eax, %eax
 2cfff4b:      	movq	%r15, %rbp
 2cfff4e:      	shrl	$0x1a, %r12d
 2cfff52:      	xorl	%ecx, %ecx
 2cfff54:      	movb	%r14b, %cl
 2cfff57:      	andl	%r12d, %ecx
 2cfff5a:      	movl	%ecx, 0x98(%rsp)
 2cfff61:      	movb	$0x1, %bl
 2cfff63:      	movq	0x20(%rsp), %rcx
 2cfff68:      	cmpl	$0xb49, %ecx            # imm = 0xB49
 2cfff6e:      	xorps	%xmm0, %xmm0
 2cfff71:      	movq	%r13, 0x28(%rsp)
 2cfff76:      	jle	0x2cfffad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d9d>
 2cfff78:      	cmpl	$0x1021, %ecx           # imm = 0x1021
 2cfff7e:      	jg	0x2cfffc4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2db4>
 2cfff80:      	addl	$0xfffff4b6, %ecx       # imm = 0xFFFFF4B6
 2cfff86:      	cmpl	$0x6, %ecx
 2cfff89:      	jbe	0x2d00699 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3489>
 2cfff8f:      	movq	0x20(%rsp), %rcx
 2cfff94:      	addl	$0xfffff0d9, %ecx       # imm = 0xFFFFF0D9
 2cfff9a:      	movl	$0x66, %edx
 2cfff9f:      	btl	%ecx, %edx
 2cfffa2:      	jb	0x2d009c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cfffa8:      	jmp	0x2d009ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cfffad:      	cmpl	$0x3a9, %ecx            # imm = 0x3A9
 2cfffb3:      	jg	0x2d00635 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3425>
 2cfffb9:      	cmpl	$0x16b, %ecx            # imm = 0x16B
 2cfffbf:      	jmp	0x2d009c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cfffc4:      	cmpl	$0x10f6, %ecx           # imm = 0x10F6
 2cfffca:      	jg	0x2d009bd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37ad>
 2cfffd0:      	addl	$0xffffefde, %ecx       # imm = 0xFFFFEFDE
 2cfffd6:      	cmpl	$0x2, %ecx
 2cfffd9:      	jb	0x2d009ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cfffdf:      	movq	0x20(%rsp), %rcx
 2cfffe4:      	addl	$0xffffefdc, %ecx       # imm = 0xFFFFEFDC
 2cfffea:      	cmpl	$0x2, %ecx
 2cfffed:      	jae	0x2d009ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2cffff3:      	jmp	0x2d009c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2cffff8:      	leaq	-0x1eee39f(%rip), %rax  # 0xe11c60 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE>
 2cfffff:      	movl	-0x4(%rax,%rcx,4), %ebx
 2d00003:      	jmp	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2d00005:      	movl	$0xb4f, %ebx            # imm = 0xB4F
 2d0000a:      	testb	%al, %al
 2d0000c:      	jne	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2d0000e:      	jmp	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d00013:      	movl	$0xb4b, %ebx            # imm = 0xB4B
 2d00018:      	testb	%al, %al
 2d0001a:      	jne	0x2d0002e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2e1e>
 2d0001c:      	jmp	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d00021:      	movl	$0xf2c, %ebx            # imm = 0xF2C
 2d00026:      	testb	%al, %al
 2d00028:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d0002e:      	movq	(%rsp), %rax
 2d00032:      	andb	0x202(%rax), %r15b
 2d00039:      	andb	%r10b, %r15b
 2d0003c:      	xorb	$0x1, %r15b
 2d00040:      	orb	%r13b, %r15b
 2d00043:      	cmpb	$0x1, %r15b
 2d00047:      	jne	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d0004d:      	movb	%dil, 0xc0(%rsp)
 2d00055:      	movb	%sil, 0x8(%rsp)
 2d0005a:      	movq	%r9, 0x80(%rsp)
 2d00062:      	movzbl	%r13b, %ebp
 2d00066:      	testb	%r10b, %r10b
 2d00069:      	movq	%r14, 0x180(%rsp)
 2d00071:      	je	0x2d001ec <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2fdc>
 2d00077:      	cmpl	$0x1173, %ebx           # imm = 0x1173
 2d0007d:      	movl	$0x30a, %eax            # imm = 0x30A
 2d00082:      	cmovel	%eax, %ebx
 2d00085:      	movq	0xc8(%rsp), %rsi
 2d0008d:      	movq	%rsi, 0x190(%rsp)
 2d00095:      	leaq	0x30(%rsp), %rax
 2d0009a:      	testq	%rsi, %rsi
 2d0009d:      	je	0x2d000db <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ecb>
 2d0009f:      	movl	$0x1, %edx
 2d000a4:      	leaq	0x190(%rsp), %rdi
 2d000ac:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d000b1:      	movq	0x190(%rsp), %rsi
 2d000b9:      	movq	%rsi, 0x30(%rsp)
 2d000be:      	testq	%rsi, %rsi
 2d000c1:      	je	0x2d000e2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ed2>
 2d000c3:      	leaq	0x190(%rsp), %r15
 2d000cb:      	movq	%r15, %rdi
 2d000ce:      	leaq	0x30(%rsp), %rdx
 2d000d3:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d000d8:      	movq	%r15, %rax
 2d000db:      	movq	$0x0, (%rax)
 2d000e2:      	leaq	0x40(%rsp), %rax
 2d000e7:      	xorps	%xmm0, %xmm0
 2d000ea:      	movups	%xmm0, -0x8(%rax)
 2d000ee:      	movq	$0x0, 0x8(%rax)
 2d000f6:      	movq	(%rsp), %rax
 2d000fa:      	movq	0x40(%rax), %rax
 2d000fe:      	movq	0x8(%rax), %rcx
 2d00102:      	movl	%ebx, %eax
 2d00104:      	shlq	$0x5, %rax
 2d00108:      	subq	%rax, %rcx
 2d0010b:      	movq	0x10(%rsp), %rdi
 2d00110:      	movq	0x20(%rsp), %rsi
 2d00115:      	leaq	0x30(%rsp), %rbx
 2d0011a:      	movq	%rbx, %rdx
 2d0011d:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d00122:      	movq	%rax, 0x70(%rsp)
 2d00127:      	movq	%rdx, %r15
 2d0012a:      	movq	0x30(%rsp), %rsi
 2d0012f:      	testq	%rsi, %rsi
 2d00132:      	je	0x2d0013c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2f2c>
 2d00134:      	movq	%rbx, %rdi
 2d00137:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d0013c:      	movq	0x190(%rsp), %rsi
 2d00144:      	testq	%rsi, %rsi
 2d00147:      	je	0x2d00156 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2f46>
 2d00149:      	leaq	0x190(%rsp), %rdi
 2d00151:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00156:      	movq	$0x0, 0x38(%rsp)
 2d0015f:      	movl	%r12d, 0x34(%rsp)
 2d00164:      	leaq	0x40(%rsp), %rbx
 2d00169:      	xorps	%xmm0, %xmm0
 2d0016c:      	movups	%xmm0, (%rbx)
 2d0016f:      	movl	$0x1000000, 0x30(%rsp)  # imm = 0x1000000
 2d00177:      	movq	%r15, %rdi
 2d0017a:      	movq	0x70(%rsp), %r14
 2d0017f:      	movq	%r14, %rsi
 2d00182:      	movq	%r12, %r13
 2d00185:      	leaq	0x30(%rsp), %r12
 2d0018a:      	movq	%r12, %rdx
 2d0018d:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00192:      	movq	$0x0, 0x38(%rsp)
 2d0019b:      	movl	%ebp, %eax
 2d0019d:      	shll	$0x1a, %eax
 2d001a0:      	movq	%r13, 0x18(%rsp)
 2d001a5:      	movl	%r13d, 0x34(%rsp)
 2d001aa:      	xorps	%xmm0, %xmm0
 2d001ad:      	movups	%xmm0, (%rbx)
 2d001b0:      	movl	%eax, 0x30(%rsp)
 2d001b4:      	movq	%r15, %rdi
 2d001b7:      	movq	%r14, %rsi
 2d001ba:      	movq	%r12, %rdx
 2d001bd:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d001c2:      	testb	%bpl, %bpl
 2d001c5:      	jne	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d001cb:      	movq	0x10(%rsp), %rax
 2d001d0:      	leaq	0x30(%rax), %rbp
 2d001d4:      	movq	0x20(%rsp), %r13
 2d001d9:      	cmpq	%rbp, %r13
 2d001dc:      	je	0x2d006ba <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x34aa>
 2d001e2:      	movq	0x18(%rsp), %r12
 2d001e7:      	jmp	0x2d0030d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30fd>
 2d001ec:      	movq	0xc8(%rsp), %rsi
 2d001f4:      	movq	%rsi, 0x188(%rsp)
 2d001fc:      	leaq	0x30(%rsp), %rax
 2d00201:      	testq	%rsi, %rsi
 2d00204:      	je	0x2d00242 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3032>
 2d00206:      	movl	$0x1, %edx
 2d0020b:      	leaq	0x188(%rsp), %rdi
 2d00213:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d00218:      	movq	0x188(%rsp), %rsi
 2d00220:      	movq	%rsi, 0x30(%rsp)
 2d00225:      	testq	%rsi, %rsi
 2d00228:      	je	0x2d00249 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3039>
 2d0022a:      	leaq	0x188(%rsp), %r15
 2d00232:      	movq	%r15, %rdi
 2d00235:      	leaq	0x30(%rsp), %rdx
 2d0023a:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d0023f:      	movq	%r15, %rax
 2d00242:      	movq	$0x0, (%rax)
 2d00249:      	leaq	0x40(%rsp), %rax
 2d0024e:      	xorps	%xmm0, %xmm0
 2d00251:      	movups	%xmm0, -0x8(%rax)
 2d00255:      	movq	$0x0, 0x8(%rax)
 2d0025d:      	movq	(%rsp), %rax
 2d00261:      	movq	0x40(%rax), %rax
 2d00265:      	movq	0x8(%rax), %rcx
 2d00269:      	movl	%ebx, %eax
 2d0026b:      	shlq	$0x5, %rax
 2d0026f:      	subq	%rax, %rcx
 2d00272:      	movq	0x10(%rsp), %rdi
 2d00277:      	movq	0x20(%rsp), %rsi
 2d0027c:      	leaq	0x30(%rsp), %rbx
 2d00281:      	movq	%rbx, %rdx
 2d00284:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d00289:      	movq	%rax, %r14
 2d0028c:      	movq	%rdx, %r15
 2d0028f:      	movq	0x30(%rsp), %rsi
 2d00294:      	testq	%rsi, %rsi
 2d00297:      	je	0x2d002a1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3091>
 2d00299:      	movq	%rbx, %rdi
 2d0029c:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d002a1:      	movq	0x188(%rsp), %rsi
 2d002a9:      	testq	%rsi, %rsi
 2d002ac:      	je	0x2d002bb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30ab>
 2d002ae:      	leaq	0x188(%rsp), %rdi
 2d002b6:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d002bb:      	movq	$0x0, 0x38(%rsp)
 2d002c4:      	shll	$0x1a, %ebp
 2d002c7:      	movl	%r12d, 0x34(%rsp)
 2d002cc:      	leaq	0x40(%rsp), %rbx
 2d002d1:      	xorps	%xmm0, %xmm0
 2d002d4:      	movups	%xmm0, (%rbx)
 2d002d7:      	movl	%ebp, 0x30(%rsp)
 2d002db:      	movq	%r15, %rdi
 2d002de:      	movq	%r14, %rsi
 2d002e1:      	leaq	0x30(%rsp), %r13
 2d002e6:      	movq	%r13, %rdx
 2d002e9:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d002ee:      	jmp	0x2d008c2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36b2>
 2d002f3:      	nopw	%cs:(%rax,%rax)
 2d002fd:      	nopl	(%rax)
 2d00300:      	movq	0x8(%r13), %r13
 2d00304:      	cmpq	%rbp, %r13
 2d00307:      	je	0x2d006bf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x34af>
 2d0030d:      	movzwl	0x44(%r13), %ebx
 2d00312:      	movq	%r13, %rdi
 2d00315:      	movl	%r12d, %esi
 2d00318:      	xorl	%edx, %edx
 2d0031a:      	xorl	%ecx, %ecx
 2d0031c:      	callq	0x3655740 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2d00321:      	cmpl	$-0x1, %eax
 2d00324:      	movq	%r13, %r12
 2d00327:      	je	0x2d003a6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3196>
 2d00329:      	leal	-0x1174(%rbx), %esi
 2d0032f:      	cmpl	$0x23, %esi
 2d00332:      	movq	0x80(%rsp), %r9
 2d0033a:      	ja	0x2d020b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ea9>
 2d00340:      	movabsq	$0xa80000045, %rax      # imm = 0xA80000045
 2d0034a:      	btq	%rsi, %rax
 2d0034e:      	jae	0x2d020b9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ea9>
 2d00354:      	movq	0x10(%r13), %rcx
 2d00358:      	movq	0x20(%r13), %rax
 2d0035c:      	movzwl	0x2(%rcx), %ecx
 2d00360:      	movl	$0xfffffffd, %edx       # imm = 0xFFFFFFFD
 2d00365:      	addl	%ecx, %edx
 2d00367:      	shlq	$0x5, %rdx
 2d0036b:      	leaq	(%rax,%rdx), %rcx
 2d0036f:      	movq	0x10(%rax,%rdx), %rdx
 2d00374:      	movl	$0xffffffff, %edi       # imm = 0xFFFFFFFF
 2d00379:      	movabsq	$0x800000240, %r8       # imm = 0x800000240
 2d00383:      	btq	%rsi, %r8
 2d00387:      	jb	0x2d00433 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3223>
 2d0038d:      	movl	$0x80000001, %edi       # imm = 0x80000001
 2d00392:      	btq	%rsi, %rdi
 2d00396:      	jae	0x2d0042e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x321e>
 2d0039c:      	movl	$0xfffffffc, %edi       # imm = 0xFFFFFFFC
 2d003a1:      	jmp	0x2d00433 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3223>
 2d003a6:      	movzwl	0x28(%r13), %ecx
 2d003ab:      	movzbl	0x2a(%r13), %eax
 2d003b0:      	shll	$0x10, %eax
 2d003b3:      	orl	%ecx, %eax
 2d003b5:      	testl	%eax, %eax
 2d003b7:      	je	0x2d00402 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31f2>
 2d003b9:      	movq	0x20(%r12), %rcx
 2d003be:      	shll	$0x5, %eax
 2d003c1:      	xorl	%edx, %edx
 2d003c3:      	jmp	0x2d003d9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c9>
 2d003c5:      	nopw	%cs:(%rax,%rax)
 2d003cf:      	nop
 2d003d0:      	addq	$0x20, %rdx
 2d003d4:      	cmpq	%rdx, %rax
 2d003d7:      	je	0x2d00402 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31f2>
 2d003d9:      	movl	(%rcx,%rdx), %esi
 2d003dc:      	movl	%esi, %edi
 2d003de:      	andl	$0x10000ff, %edi        # imm = 0x10000FF
 2d003e4:      	cmpl	$0x1000000, %edi        # imm = 0x1000000
 2d003ea:      	jne	0x2d003d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d003ec:      	notl	%esi
 2d003ee:      	testl	$0x5000000, %esi        # imm = 0x5000000
 2d003f4:      	je	0x2d003d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d003f6:      	cmpl	$0x3, 0x4(%rcx,%rdx)
 2d003fb:      	jne	0x2d003d0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x31c0>
 2d003fd:      	jmp	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d00402:      	movl	0x2c(%r12), %eax
 2d00407:      	testb	$0xc, %al
 2d00409:      	setne	%cl
 2d0040c:      	testb	$0x4, %al
 2d0040e:      	sete	%dl
 2d00411:      	movq	0x10(%r12), %rax
 2d00416:      	movq	0x10(%rax), %rax
 2d0041a:      	testb	%dl, %cl
 2d0041c:      	jne	0x2d004db <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32cb>
 2d00422:      	testl	$0x480, %eax            # imm = 0x480
 2d00427:      	je	0x2d0046a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x325a>
 2d00429:      	jmp	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d0042e:      	movl	$0xfffffffe, %edi       # imm = 0xFFFFFFFE
 2d00433:      	movl	%r9d, %esi
 2d00436:      	imull	%edi, %esi
 2d00439:      	addl	%esi, %edx
 2d0043b:      	js	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d00441:      	addl	$0xffffee6d, %ebx       # imm = 0xFFFFEE6D
 2d00447:      	cmpl	$0x4, %ebx
 2d0044a:      	ja	0x2d00464 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3254>
 2d0044c:      	movl	$0x15, %esi
 2d00451:      	btl	%ebx, %esi
 2d00454:      	jae	0x2d00464 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3254>
 2d00456:      	movq	0x18(%rsp), %rsi
 2d0045b:      	cmpl	%esi, 0x4(%rax)
 2d0045e:      	je	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d00464:      	movl	%edx, %eax
 2d00466:      	movq	%rax, 0x10(%rcx)
 2d0046a:      	movq	%r12, %r13
 2d0046d:      	movq	%r12, %rdi
 2d00470:      	movq	0x18(%rsp), %r12
 2d00475:      	movl	%r12d, %esi
 2d00478:      	xorl	%edx, %edx
 2d0047a:      	movl	$0x1, %ecx
 2d0047f:      	callq	0x3655740 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 2d00484:      	cmpl	$-0x1, %eax
 2d00487:      	jne	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0048d:      	movq	%r13, %rdi
 2d00490:      	movl	%r12d, %esi
 2d00493:      	xorl	%edx, %edx
 2d00495:      	xorl	%ecx, %ecx
 2d00497:      	xorl	%r8d, %r8d
 2d0049a:      	callq	0x3655c40 <_ZNK4llvm12MachineInstr25findRegisterDefOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEbb>
 2d0049f:      	cmpl	$-0x1, %eax
 2d004a2:      	jne	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d004a8:      	testb	$0x4, (%r13)
 2d004ad:      	jne	0x2d00300 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d004b3:      	nopw	%cs:(%rax,%rax)
 2d004bd:      	nopl	(%rax)
 2d004c0:      	testb	$0x8, 0x2c(%r13)
 2d004c5:      	je	0x2d00300 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d004cb:      	movq	0x8(%r13), %r13
 2d004cf:      	testb	$0x8, 0x2c(%r13)
 2d004d4:      	jne	0x2d004cb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32bb>
 2d004d6:      	jmp	0x2d00300 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x30f0>
 2d004db:      	testb	%al, %al
 2d004dd:      	js	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d004df:      	movq	%r12, %rcx
 2d004e2:      	nopw	%cs:(%rax,%rax)
 2d004ec:      	nopl	(%rax)
 2d004f0:      	testb	$0x8, 0x2c(%rcx)
 2d004f4:      	je	0x2d00506 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32f6>
 2d004f6:      	movq	0x8(%rcx), %rcx
 2d004fa:      	movq	0x10(%rcx), %rdx
 2d004fe:      	testb	$-0x80, 0x10(%rdx)
 2d00502:      	je	0x2d004f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x32e0>
 2d00504:      	jmp	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d00506:      	testl	$0x400, %eax            # imm = 0x400
 2d0050b:      	jne	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d0050d:      	movq	%r12, %rax
 2d00510:      	testb	$0x8, 0x2c(%rax)
 2d00514:      	je	0x2d0046a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x325a>
 2d0051a:      	movq	0x8(%rax), %rax
 2d0051e:      	movq	0x10(%rax), %rcx
 2d00522:      	testb	$0x4, 0x11(%rcx)
 2d00526:      	je	0x2d00510 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3300>
 2d00528:      	movq	0xc8(%rsp), %rsi
 2d00530:      	movq	%rsi, 0xd0(%rsp)
 2d00538:      	leaq	0xa0(%rsp), %rax
 2d00540:      	testq	%rsi, %rsi
 2d00543:      	je	0x2d00587 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3377>
 2d00545:      	movl	$0x1, %edx
 2d0054a:      	leaq	0xd0(%rsp), %rdi
 2d00552:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d00557:      	movq	0xd0(%rsp), %rsi
 2d0055f:      	movq	%rsi, 0xa0(%rsp)
 2d00567:      	testq	%rsi, %rsi
 2d0056a:      	je	0x2d0058e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x337e>
 2d0056c:      	leaq	0xd0(%rsp), %rbx
 2d00574:      	movq	%rbx, %rdi
 2d00577:      	leaq	0xa0(%rsp), %rdx
 2d0057f:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d00584:      	movq	%rbx, %rax
 2d00587:      	movq	$0x0, (%rax)
 2d0058e:      	leaq	0xa8(%rsp), %rax
 2d00596:      	xorps	%xmm0, %xmm0
 2d00599:      	movups	%xmm0, (%rax)
 2d0059c:      	movq	$0x0, 0x10(%rax)
 2d005a4:      	movq	(%rsp), %rax
 2d005a8:      	movq	0x40(%rax), %rax
 2d005ac:      	movq	0x8(%rax), %rcx
 2d005b0:      	movq	$-0x23360, %rax         # imm = 0xFFFDCCA0
 2d005b7:      	addq	%rax, %rcx
 2d005ba:      	movq	0x10(%rsp), %rdi
 2d005bf:      	movq	%r12, %rsi
 2d005c2:      	leaq	0xa0(%rsp), %r13
 2d005ca:      	movq	%r13, %rdx
 2d005cd:      	movq	0x18(%rsp), %rbx
 2d005d2:      	movl	%ebx, %r8d
 2d005d5:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d005da:      	movq	%rax, %r14
 2d005dd:      	movq	%rdx, %rbp
 2d005e0:      	movq	$0x0, 0xf8(%rsp)
 2d005ec:      	movl	$0x3, 0xf4(%rsp)
 2d005f7:      	leaq	0x100(%rsp), %rax
 2d005ff:      	xorps	%xmm0, %xmm0
 2d00602:      	movups	%xmm0, (%rax)
 2d00605:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d00610:      	movq	%rdx, %rdi
 2d00613:      	movq	%r14, %rsi
 2d00616:      	leaq	0xf0(%rsp), %rdx
 2d0061e:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00623:      	movq	$0x0, 0x38(%rsp)
 2d0062c:      	movl	%ebx, 0x34(%rsp)
 2d00630:      	jmp	0x2d007d2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x35c2>
 2d00635:      	movl	$0x3, %r12d
 2d0063b:      	xorl	%r14d, %r14d
 2d0063e:      	movq	%rcx, %rdx
 2d00641:      	addl	$0xfffffc56, %ecx       # imm = 0xFFFFFC56
 2d00647:      	cmpl	$0x7, %ecx
 2d0064a:      	jbe	0x2d009de <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37ce>
 2d00650:      	leal	-0x7d7(%rdx), %ecx
 2d00656:      	leaq	-0x19b1455(%rip), %rdx  # 0x134f208 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x572>
 2d0065d:      	movslq	(%rdx,%rcx,4), %rcx
 2d00661:      	addq	%rdx, %rcx
 2d00664:      	jmpq	*%rcx
 2d00666:      	cmpl	$0x1199, %ebx           # imm = 0x1199
 2d0066c:      	je	0x2cffc2a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a1a>
 2d00672:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2d00678:      	je	0x2cffc2a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a1a>
 2d0067e:      	movl	$0x1, %ecx
 2d00683:      	movb	$0x1, %al
 2d00685:      	movb	$0x1, %sil
 2d00688:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d0068e:      	jne	0x2cffcc9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2d00694:      	jmp	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2d00699:      	movl	$0x66, %edx
 2d0069e:      	btl	%ecx, %edx
 2d006a1:      	jb	0x2d009c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37b6>
 2d006a7:      	movl	$0x11, %edx
 2d006ac:      	btl	%ecx, %edx
 2d006af:      	jb	0x2d009ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37de>
 2d006b5:      	jmp	0x2cfff8f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2d7f>
 2d006ba:      	movq	0x18(%rsp), %r12
 2d006bf:      	movq	0x10(%rsp), %rax
 2d006c4:      	cmpl	$0x0, 0x78(%rax)
 2d006c8:      	je	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d006ce:      	movq	0xc8(%rsp), %rsi
 2d006d6:      	movq	%rsi, 0xd0(%rsp)
 2d006de:      	leaq	0xa0(%rsp), %rax
 2d006e6:      	testq	%rsi, %rsi
 2d006e9:      	je	0x2d0072d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x351d>
 2d006eb:      	movl	$0x1, %edx
 2d006f0:      	leaq	0xd0(%rsp), %rdi
 2d006f8:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d006fd:      	movq	0xd0(%rsp), %rsi
 2d00705:      	movq	%rsi, 0xa0(%rsp)
 2d0070d:      	testq	%rsi, %rsi
 2d00710:      	je	0x2d00734 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3524>
 2d00712:      	leaq	0xd0(%rsp), %rbx
 2d0071a:      	movq	%rbx, %rdi
 2d0071d:      	leaq	0xa0(%rsp), %rdx
 2d00725:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d0072a:      	movq	%rbx, %rax
 2d0072d:      	movq	$0x0, (%rax)
 2d00734:      	leaq	0xa8(%rsp), %rax
 2d0073c:      	xorps	%xmm0, %xmm0
 2d0073f:      	movups	%xmm0, (%rax)
 2d00742:      	movq	$0x0, 0x10(%rax)
 2d0074a:      	movq	(%rsp), %rax
 2d0074e:      	movq	0x40(%rax), %rax
 2d00752:      	movq	0x8(%rax), %rcx
 2d00756:      	movq	$-0x23360, %rax         # imm = 0xFFFDCCA0
 2d0075d:      	addq	%rax, %rcx
 2d00760:      	movq	0x10(%rsp), %rdi
 2d00765:      	movq	%r13, %rsi
 2d00768:      	leaq	0xa0(%rsp), %r13
 2d00770:      	movq	%r13, %rdx
 2d00773:      	movl	%r12d, %r8d
 2d00776:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d0077b:      	movq	%rax, %r14
 2d0077e:      	movq	%rdx, %rbp
 2d00781:      	movq	$0x0, 0xf8(%rsp)
 2d0078d:      	movl	$0x3, 0xf4(%rsp)
 2d00798:      	leaq	0x100(%rsp), %rax
 2d007a0:      	xorps	%xmm0, %xmm0
 2d007a3:      	movups	%xmm0, (%rax)
 2d007a6:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d007b1:      	movq	%rdx, %rdi
 2d007b4:      	movq	%r14, %rsi
 2d007b7:      	leaq	0xf0(%rsp), %rdx
 2d007bf:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d007c4:      	movq	$0x0, 0x38(%rsp)
 2d007cd:      	movl	%r12d, 0x34(%rsp)
 2d007d2:      	leaq	0x40(%rsp), %rbx
 2d007d7:      	xorps	%xmm0, %xmm0
 2d007da:      	movups	%xmm0, (%rbx)
 2d007dd:      	movl	$0x0, 0x30(%rsp)
 2d007e5:      	movq	%rbp, %rdi
 2d007e8:      	movq	%r14, %rsi
 2d007eb:      	leaq	0x30(%rsp), %r12
 2d007f0:      	movq	%r12, %rdx
 2d007f3:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d007f8:      	movq	0x80(%rsp), %rax
 2d00800:      	leal	(,%rax,4), %eax
 2d00807:      	movl	$0x1, 0x30(%rsp)
 2d0080f:      	movq	$0x0, 0x38(%rsp)
 2d00818:      	movq	%rax, 0x40(%rsp)
 2d0081d:      	movq	%rbp, %rdi
 2d00820:      	movq	%r14, %rsi
 2d00823:      	movq	%r12, %rdx
 2d00826:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d0082b:      	movl	0x28(%rsp), %eax
 2d0082f:      	movl	$0x1, 0x30(%rsp)
 2d00837:      	movq	$0x0, 0x38(%rsp)
 2d00840:      	movq	%rax, 0x40(%rsp)
 2d00845:      	movq	%rbp, %rdi
 2d00848:      	movq	%r14, %rsi
 2d0084b:      	movq	%r12, %rdx
 2d0084e:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00853:      	movq	$0x0, 0x38(%rsp)
 2d0085c:      	movq	0x88(%rsp), %rax
 2d00864:      	movl	%eax, 0x34(%rsp)
 2d00868:      	xorps	%xmm0, %xmm0
 2d0086b:      	movups	%xmm0, (%rbx)
 2d0086e:      	movl	$0x0, 0x30(%rsp)
 2d00876:      	movq	%rbp, %rdi
 2d00879:      	movq	%r14, %rsi
 2d0087c:      	movq	%r12, %rdx
 2d0087f:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00884:      	movq	0xa0(%rsp), %rsi
 2d0088c:      	testq	%rsi, %rsi
 2d0088f:      	je	0x2d00899 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3689>
 2d00891:      	movq	%r13, %rdi
 2d00894:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00899:      	movq	0xd0(%rsp), %rsi
 2d008a1:      	testq	%rsi, %rsi
 2d008a4:      	je	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d008a6:      	leaq	0xd0(%rsp), %rdi
 2d008ae:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d008b3:      	leaq	0x40(%rsp), %rbx
 2d008b8:      	leaq	0x30(%rsp), %r13
 2d008bd:      	movq	0x70(%rsp), %r14
 2d008c2:      	movl	0x28(%rsp), %eax
 2d008c6:      	movl	$0x1, 0x30(%rsp)
 2d008ce:      	movq	$0x0, 0x38(%rsp)
 2d008d7:      	movq	%rax, 0x40(%rsp)
 2d008dc:      	movq	%r15, %rdi
 2d008df:      	movq	%r14, %rsi
 2d008e2:      	movq	%r13, %rdx
 2d008e5:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d008ea:      	movq	$0x0, 0x38(%rsp)
 2d008f3:      	movq	0x88(%rsp), %rax
 2d008fb:      	movl	%eax, 0x34(%rsp)
 2d008ff:      	xorps	%xmm0, %xmm0
 2d00902:      	movups	%xmm0, (%rbx)
 2d00905:      	movl	$0x0, 0x30(%rsp)
 2d0090d:      	movq	%r15, %rdi
 2d00910:      	movq	%r14, %rsi
 2d00913:      	movq	%r13, %rdx
 2d00916:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d0091b:      	movq	0x80(%rsp), %rax
 2d00923:      	testq	%rax, %rax
 2d00926:      	movq	%r14, %rsi
 2d00929:      	movq	0x180(%rsp), %r12
 2d00931:      	movq	%r15, %r14
 2d00934:      	je	0x2d009a5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3795>
 2d00936:      	movq	%r13, %rdx
 2d00939:      	movzbl	0xc0(%rsp), %ecx
 2d00941:      	orb	0x8(%rsp), %cl
 2d00945:      	leaq	(%r12,%rax,8), %rax
 2d00949:      	movq	%rax, 0x18(%rsp)
 2d0094e:      	movzbl	%cl, %ebp
 2d00951:      	shll	$0x18, %ebp
 2d00954:      	nopw	%cs:(%rax,%rax)
 2d0095e:      	nop
 2d00960:      	movl	(%r12), %eax
 2d00964:      	movzbl	0x4(%r12), %ecx
 2d0096a:      	movq	$0x0, 0x38(%rsp)
 2d00973:      	shll	$0x1a, %ecx
 2d00976:      	orl	%ebp, %ecx
 2d00978:      	movl	%eax, 0x34(%rsp)
 2d0097c:      	xorps	%xmm0, %xmm0
 2d0097f:      	movups	%xmm0, (%rbx)
 2d00982:      	movl	%ecx, 0x30(%rsp)
 2d00986:      	movq	%r14, %rdi
 2d00989:      	movq	%rsi, %r13
 2d0098c:      	movq	%rdx, %r15
 2d0098f:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00994:      	movq	%r15, %rdx
 2d00997:      	movq	%r13, %rsi
 2d0099a:      	addq	$0x8, %r12
 2d0099e:      	cmpq	0x18(%rsp), %r12
 2d009a3:      	jne	0x2d00960 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3750>
 2d009a5:      	movq	%r14, %rdi
 2d009a8:      	movq	0x230(%rsp), %rdx
 2d009b0:      	movq	0x228(%rsp), %rcx
 2d009b8:      	jmp	0x2cff2e5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x20d5>
 2d009bd:      	addl	$0xffffef09, %ecx       # imm = 0xFFFFEF09
 2d009c3:      	cmpl	$0x2, %ecx
 2d009c6:      	movl	$0x4, %esi
 2d009cb:      	addl	0x10(%rsp), %eax
 2d009cf:      	je	0x2d00a4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383d>
 2d009d1:      	movl	$0x1, %r12d
 2d009d7:      	movb	$0x1, %r14b
 2d009da:      	xorl	%ebx, %ebx
 2d009dc:      	jmp	0x2d009f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37e7>
 2d009de:      	leaq	-0x19b17fd(%rip), %rdx  # 0x134f1e8 <_ZTSN4llvm2cl11opt_storageINS0_13boolOrDefaultELb0ELb0EEE+0x552>
 2d009e5:      	movslq	(%rdx,%rcx,4), %rcx
 2d009e9:      	addq	%rdx, %rcx
 2d009ec:      	jmpq	*%rcx
 2d009ee:      	movl	$0x4, %r12d
 2d009f4:      	xorl	%r14d, %r14d
 2d009f7:      	movq	(%rsp), %rax
 2d009fb:      	movq	0x48(%rax), %r9
 2d009ff:      	movq	%r13, %rdi
 2d00a02:      	movl	0x90(%rsp), %esi
 2d00a09:      	movl	0x8(%rsp), %edx
 2d00a0d:      	movl	0x78(%rsp), %ecx
 2d00a11:      	leaq	0x1c0(%rsp), %r8
 2d00a19:      	callq	0x2d05160 <_ZL15findIncDecAfterN4llvm26MachineInstrBundleIteratorINS_12MachineInstrELb0EEENS_8RegisterENS_5ARMCC9CondCodesES3_RiPKNS_18TargetRegisterInfoE>
 2d00a1e:      	movq	%rax, %rbp
 2d00a21:      	movl	0x1c0(%rsp), %eax
 2d00a28:      	testb	%r14b, %r14b
 2d00a2b:      	je	0x2d00a38 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3828>
 2d00a2d:      	cmpl	0x10(%rsp), %eax
 2d00a31:      	jne	0x2d00a38 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3828>
 2d00a33:      	xorps	%xmm0, %xmm0
 2d00a36:      	jmp	0x2d00a4a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383a>
 2d00a38:      	addl	0x10(%rsp), %eax
 2d00a3c:      	sete	%al
 2d00a3f:      	testb	%al, %bl
 2d00a41:      	xorps	%xmm0, %xmm0
 2d00a44:      	je	0x2d00cf6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ae6>
 2d00a4a:      	movl	%r12d, %esi
 2d00a4d:      	cmpq	%r15, %rbp
 2d00a50:      	je	0x2d00d54 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b44>
 2d00a56:      	testb	$0x4, (%rbp)
 2d00a5a:      	movq	%rbp, %rax
 2d00a5d:      	leaq	0x30(%rsp), %rdx
 2d00a62:      	movq	0x20(%rsp), %rcx
 2d00a67:      	jne	0x2d00a8a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x387a>
 2d00a69:      	testb	$0x8, 0x2c(%rbp)
 2d00a6d:      	movq	%rbp, %rax
 2d00a70:      	je	0x2d00a8a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x387a>
 2d00a72:      	movq	%rbp, %rax
 2d00a75:      	nopw	%cs:(%rax,%rax)
 2d00a7f:      	nop
 2d00a80:      	movq	0x8(%rax), %rax
 2d00a84:      	testb	$0x8, 0x2c(%rax)
 2d00a88:      	jne	0x2d00a80 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3870>
 2d00a8a:      	movq	0x8(%rax), %rax
 2d00a8e:      	movq	%rax, 0x10(%rsp)
 2d00a93:      	cmpq	%rax, %rbp
 2d00a96:      	je	0x2d00c96 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a86>
 2d00a9c:      	movl	%esi, 0x88(%rsp)
 2d00aa3:      	jmp	0x2d00aeb <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38db>
 2d00aa5:      	nopw	%cs:(%rax,%rax)
 2d00aaf:      	nop
 2d00ab0:      	movl	%ecx, 0xf0(%r13)
 2d00ab7:      	movq	(%r14), %rax
 2d00aba:      	movq	(%rax,%r15,8), %rcx
 2d00abe:      	movq	%rcx, (%r12)
 2d00ac2:      	movq	%r12, (%rax,%r15,8)
 2d00ac6:      	movq	0xe0(%r13), %rax
 2d00acd:      	movq	%rax, (%rbp)
 2d00ad1:      	movq	%rbp, 0xe0(%r13)
 2d00ad8:      	movq	%rbx, %rbp
 2d00adb:      	cmpq	0x10(%rsp), %rbx
 2d00ae0:      	movq	0x28(%rsp), %r13
 2d00ae5:      	je	0x2d00c85 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a75>
 2d00aeb:      	movq	0x8(%rbp), %rbx
 2d00aef:      	movq	0x18(%rbp), %rax
 2d00af3:      	movq	0x20(%rax), %r14
 2d00af7:      	testq	%r14, %r14
 2d00afa:      	je	0x2d00bb0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00b00:      	movq	0x288(%r14), %rdi
 2d00b07:      	testq	%rdi, %rdi
 2d00b0a:      	je	0x2d00b18 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3908>
 2d00b0c:      	movq	(%rdi), %rax
 2d00b0f:      	movq	%rbp, %rsi
 2d00b12:      	callq	*0x20(%rax)
 2d00b15:      	xorps	%xmm0, %xmm0
 2d00b18:      	movzwl	0x28(%rbp), %ecx
 2d00b1c:      	movzbl	0x2a(%rbp), %eax
 2d00b20:      	shll	$0x10, %eax
 2d00b23:      	orl	%ecx, %eax
 2d00b25:      	testl	%eax, %eax
 2d00b27:      	je	0x2d00bb0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00b2d:      	movq	0x20(%rbp), %rcx
 2d00b31:      	shll	$0x5, %eax
 2d00b34:      	movq	0x20(%r14), %rdx
 2d00b38:      	jmp	0x2d00b61 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3951>
 2d00b3a:      	nopw	(%rax,%rax)
 2d00b40:      	movq	%rdi, 0x18(%r8)
 2d00b44:      	leaq	0x10(%rcx), %r9
 2d00b48:      	testq	%rdi, %rdi
 2d00b4b:      	cmovneq	%rdi, %rsi
 2d00b4f:      	movq	%r8, 0x10(%rsi)
 2d00b53:      	movups	%xmm0, (%r9)
 2d00b57:      	addq	$0x20, %rcx
 2d00b5b:      	addq	$-0x20, %rax
 2d00b5f:      	je	0x2d00bb0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x39a0>
 2d00b61:      	cmpb	$0x0, (%rcx)
 2d00b64:      	jne	0x2d00b57 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3947>
 2d00b66:      	movl	0x4(%rcx), %esi
 2d00b69:      	movl	%esi, %edi
 2d00b6b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2d00b71:      	shlq	$0x4, %rdi
 2d00b75:      	movq	%rsi, %r8
 2d00b78:      	shlq	$0x3, %r8
 2d00b7c:      	addq	0x128(%rdx), %r8
 2d00b83:      	testl	%esi, %esi
 2d00b85:      	movq	0x30(%rdx), %rsi
 2d00b89:      	leaq	0x8(%rsi,%rdi), %r9
 2d00b8e:      	cmovnsq	%r8, %r9
 2d00b92:      	movq	(%r9), %rsi
 2d00b95:      	movq	0x18(%rcx), %rdi
 2d00b99:      	movq	0x10(%rcx), %r8
 2d00b9d:      	cmpq	%rsi, %rcx
 2d00ba0:      	jne	0x2d00b40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3930>
 2d00ba2:      	movq	%rdi, (%r9)
 2d00ba5:      	jmp	0x2d00b44 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3934>
 2d00ba7:      	nopw	(%rax,%rax)
 2d00bb0:      	movq	$0x0, 0x18(%rbp)
 2d00bb8:      	movq	(%rbp), %rax
 2d00bbc:      	movq	0x8(%rbp), %rcx
 2d00bc0:      	andq	$-0x8, %rax
 2d00bc4:      	movq	(%rcx), %rdx
 2d00bc7:      	andl	$0x7, %edx
 2d00bca:      	orq	%rax, %rdx
 2d00bcd:      	movq	%rdx, (%rcx)
 2d00bd0:      	movq	%rcx, 0x8(%rax)
 2d00bd4:      	andq	$0x7, (%rbp)
 2d00bd9:      	movq	$0x0, 0x8(%rbp)
 2d00be1:      	movq	0x18(%rsp), %rax
 2d00be6:      	movq	0x28(%rax), %rax
 2d00bea:      	movq	0x20(%rax), %r13
 2d00bee:      	movq	0x20(%rbp), %r12
 2d00bf2:      	testq	%r12, %r12
 2d00bf5:      	je	0x2d00ac6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38b6>
 2d00bfb:      	movzbl	0x2b(%rbp), %r15d
 2d00c00:      	leaq	0xe8(%r13), %r14
 2d00c07:      	movl	0xf0(%r13), %eax
 2d00c0e:      	cmpl	%r15d, %eax
 2d00c11:      	ja	0x2d00ab7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a7>
 2d00c17:      	leaq	0x1(%r15), %rcx
 2d00c1b:      	cmpl	%r15d, 0xf4(%r13)
 2d00c22:      	ja	0x2d00c4a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a3a>
 2d00c24:      	leaq	0xf8(%r13), %rsi
 2d00c2b:      	movl	$0x8, %ecx
 2d00c30:      	movq	%r14, %rdi
 2d00c33:      	leaq	0x1(%r15), %rdx
 2d00c37:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d00c3c:      	leaq	0x1(%r15), %rcx
 2d00c40:      	xorps	%xmm0, %xmm0
 2d00c43:      	movl	0xf0(%r13), %eax
 2d00c4a:      	cmpl	%eax, %ecx
 2d00c4c:      	je	0x2d00ab0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a0>
 2d00c52:      	movl	%eax, %eax
 2d00c54:      	leaq	(,%rax,8), %rdi
 2d00c5c:      	addq	(%r14), %rdi
 2d00c5f:      	movq	%rcx, %r14
 2d00c62:      	movq	%rcx, %rdx
 2d00c65:      	subq	%rax, %rdx
 2d00c68:      	shlq	$0x3, %rdx
 2d00c6c:      	xorl	%esi, %esi
 2d00c6e:      	callq	0x828ac20 <memset@plt>
 2d00c73:      	movq	%r14, %rcx
 2d00c76:      	leaq	0xe8(%r13), %r14
 2d00c7d:      	xorps	%xmm0, %xmm0
 2d00c80:      	jmp	0x2d00ab0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x38a0>
 2d00c85:      	leaq	0x30(%rsp), %rdx
 2d00c8a:      	movq	0x20(%rsp), %rcx
 2d00c8f:      	movl	0x88(%rsp), %esi
 2d00c96:      	cmpl	$0xb4a, %ecx            # imm = 0xB4A
 2d00c9c:      	jg	0x2d00d6a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b5a>
 2d00ca2:      	leal	-0x3aa(%rcx), %eax
 2d00ca8:      	cmpl	$0x6, %eax
 2d00cab:      	jbe	0x2d00cd4 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ac4>
 2d00cad:      	addl	$0xfffff829, %ecx       # imm = 0xFFFFF829
 2d00cb3:      	movl	$0x55, %eax
 2d00cb8:      	btl	%ecx, %eax
 2d00cbb:      	jae	0x2d023a2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5192>
 2d00cc1:      	movl	%esi, %eax
 2d00cc3:      	leaq	-0x1e72f9a(%rip), %rcx  # 0xe8dd30 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.152>
 2d00cca:      	movq	-0x8(%rcx,%rax,8), %r14
 2d00ccf:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00cd4:      	movl	$0x55, %ecx
 2d00cd9:      	btl	%eax, %ecx
 2d00cdc:      	movq	0x20(%rsp), %rcx
 2d00ce1:      	jae	0x2d00cad <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a9d>
 2d00ce3:      	movl	%esi, %eax
 2d00ce5:      	leaq	-0x1e7389c(%rip), %rcx  # 0xe8d450 <.Lswitch.table._ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE.151>
 2d00cec:      	movq	-0x8(%rcx,%rax,8), %r14
 2d00cf1:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00cf6:      	movl	0x98(%rsp), %edi
 2d00cfd:      	testl	%edi, %edi
 2d00cff:      	je	0x2d0108b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00d05:      	movq	(%rsp), %rax
 2d00d09:      	movq	0x50(%rax), %rax
 2d00d0d:      	cmpb	$0x0, 0x208(%rax)
 2d00d14:      	je	0x2d0108b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00d1a:      	movl	%r12d, %esi
 2d00d1d:      	movzwl	0x28(%r13), %ecx
 2d00d22:      	movzbl	0x2a(%r13), %eax
 2d00d27:      	shll	$0x10, %eax
 2d00d2a:      	orl	%ecx, %eax
 2d00d2c:      	cmpl	$0x2, %eax
 2d00d2f:      	je	0x2d00d54 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b44>
 2d00d31:      	movq	0x20(%r13), %rcx
 2d00d35:      	shll	$0x5, %eax
 2d00d38:      	addq	$-0x40, %rax
 2d00d3c:      	xorl	%edx, %edx
 2d00d3e:      	nop
 2d00d40:      	cmpl	$0x52, 0x44(%rcx,%rdx)
 2d00d45:      	jae	0x2d0108b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d00d4b:      	addq	$0x20, %rdx
 2d00d4f:      	cmpq	%rdx, %rax
 2d00d52:      	jne	0x2d00d40 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b30>
 2d00d54:      	leaq	0x30(%rsp), %rdx
 2d00d59:      	movq	0x20(%rsp), %rcx
 2d00d5e:      	cmpl	$0xb4a, %ecx            # imm = 0xB4A
 2d00d64:      	jle	0x2d00ca2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3a92>
 2d00d6a:      	cmpl	$0x1021, %ecx           # imm = 0x1021
 2d00d70:      	jg	0x2d00d98 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3b88>
 2d00d72:      	cmpl	$0xf27, %ecx            # imm = 0xF27
 2d00d78:      	jg	0x2d00db2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ba2>
 2d00d7a:      	xorl	%r14d, %r14d
 2d00d7d:      	cmpl	$0xb4b, %ecx            # imm = 0xB4B
 2d00d83:      	jne	0x2d00dee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bde>
 2d00d85:      	cmpl	$0x1, %esi
 2d00d88:      	setne	%r14b
 2d00d8c:      	addl	%r14d, %r14d
 2d00d8f:      	orq	$-0xb4c, %r14           # imm = 0xF4B4
 2d00d96:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00d98:      	cmpl	$0x10f4, %ecx           # imm = 0x10F4
 2d00d9e:      	jg	0x2d00dcc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bbc>
 2d00da0:      	xorl	%eax, %eax
 2d00da2:      	cmpl	$0x1, %esi
 2d00da5:      	setne	%al
 2d00da8:      	leaq	-0x1025(%rax,%rax), %r14
 2d00db0:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00db2:      	xorl	%eax, %eax
 2d00db4:      	cmpl	$0xf28, %ecx            # imm = 0xF28
 2d00dba:      	jne	0x2d00e01 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bf1>
 2d00dbc:      	cmpl	$0x1, %esi
 2d00dbf:      	setne	%al
 2d00dc2:      	leaq	-0xf29(%rax,%rax), %r14
 2d00dca:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00dcc:      	xorl	%r14d, %r14d
 2d00dcf:      	cmpl	$0x1, %esi
 2d00dd2:      	setne	%r14b
 2d00dd6:      	addl	%r14d, %r14d
 2d00dd9:      	orq	$-0x10f8, %r14          # imm = 0xEF08
 2d00de0:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00de2:      	xorl	%r10d, %r10d
 2d00de5:      	movb	$0x1, %cl
 2d00de7:      	movb	$0x1, %dl
 2d00de9:      	jmp	0x2cffba8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2998>
 2d00dee:      	cmpl	$0x1, %esi
 2d00df1:      	setne	%r14b
 2d00df5:      	addl	%r14d, %r14d
 2d00df8:      	orq	$-0xb50, %r14           # imm = 0xF4B0
 2d00dff:      	jmp	0x2d00e0f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3bff>
 2d00e01:      	cmpl	$0x1, %esi
 2d00e04:      	setne	%al
 2d00e07:      	leaq	-0xf2d(%rax,%rax), %r14
 2d00e0f:      	movq	0xa0(%rsp), %rsi
 2d00e17:      	movq	%rsi, 0xf0(%rsp)
 2d00e1f:      	movq	%rdx, %rbx
 2d00e22:      	testq	%rsi, %rsi
 2d00e25:      	je	0x2d00e65 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c55>
 2d00e27:      	movl	$0x1, %edx
 2d00e2c:      	leaq	0xf0(%rsp), %rdi
 2d00e34:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d00e39:      	leaq	0x30(%rsp), %rdx
 2d00e3e:      	movq	0xf0(%rsp), %rsi
 2d00e46:      	movq	%rsi, 0x30(%rsp)
 2d00e4b:      	testq	%rsi, %rsi
 2d00e4e:      	je	0x2d00e6c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3c5c>
 2d00e50:      	leaq	0xf0(%rsp), %rbx
 2d00e58:      	movq	%rbx, %rdi
 2d00e5b:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d00e60:      	leaq	0x30(%rsp), %rdx
 2d00e65:      	movq	$0x0, (%rbx)
 2d00e6c:      	leaq	0x40(%rsp), %rax
 2d00e71:      	xorps	%xmm0, %xmm0
 2d00e74:      	movups	%xmm0, -0x8(%rax)
 2d00e78:      	movq	$0x0, 0x8(%rax)
 2d00e80:      	movq	(%rsp), %rax
 2d00e84:      	movq	0x40(%rax), %rax
 2d00e88:      	shlq	$0x5, %r14
 2d00e8c:      	addq	0x8(%rax), %r14
 2d00e90:      	movq	0x18(%rsp), %rdi
 2d00e95:      	movq	%r13, %rsi
 2d00e98:      	movq	%rdx, %r12
 2d00e9b:      	movq	%r14, %rcx
 2d00e9e:      	callq	0x27efb50 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescE>
 2d00ea3:      	movq	%rax, %r14
 2d00ea6:      	movq	%rdx, %r15
 2d00ea9:      	movq	$0x0, 0x138(%rsp)
 2d00eb5:      	movl	0x90(%rsp), %ebp
 2d00ebc:      	movl	%ebp, 0x134(%rsp)
 2d00ec3:      	leaq	0x140(%rsp), %rbx
 2d00ecb:      	xorps	%xmm0, %xmm0
 2d00ece:      	movups	%xmm0, (%rbx)
 2d00ed1:      	movl	$0x1000000, 0x130(%rsp) # imm = 0x1000000
 2d00edc:      	movq	%rdx, %rdi
 2d00edf:      	movq	%rax, %rsi
 2d00ee2:      	leaq	0x130(%rsp), %r13
 2d00eea:      	movq	%r13, %rdx
 2d00eed:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00ef2:      	movq	$0x0, 0x138(%rsp)
 2d00efe:      	movl	0x98(%rsp), %eax
 2d00f05:      	shll	$0x1a, %eax
 2d00f08:      	movl	%ebp, 0x134(%rsp)
 2d00f0f:      	xorps	%xmm0, %xmm0
 2d00f12:      	movups	%xmm0, (%rbx)
 2d00f15:      	movl	%eax, 0x130(%rsp)
 2d00f1c:      	movq	%r15, %rdi
 2d00f1f:      	movq	%r14, %rsi
 2d00f22:      	movq	%r13, %rdx
 2d00f25:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00f2a:      	movl	0x8(%rsp), %eax
 2d00f2e:      	movl	$0x1, 0x130(%rsp)
 2d00f39:      	movq	$0x0, 0x138(%rsp)
 2d00f45:      	movq	%rax, 0x140(%rsp)
 2d00f4d:      	movq	%r15, %rdi
 2d00f50:      	movq	%r14, %rsi
 2d00f53:      	movq	%r13, %rdx
 2d00f56:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00f5b:      	movq	$0x0, 0x138(%rsp)
 2d00f67:      	movl	0x78(%rsp), %eax
 2d00f6b:      	movl	%eax, 0x134(%rsp)
 2d00f72:      	xorps	%xmm0, %xmm0
 2d00f75:      	movups	%xmm0, (%rbx)
 2d00f78:      	movl	$0x0, 0x130(%rsp)
 2d00f83:      	movq	%r15, %rdi
 2d00f86:      	movq	%r14, %rsi
 2d00f89:      	movq	%r13, %rdx
 2d00f8c:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00f91:      	movq	0x30(%rsp), %rsi
 2d00f96:      	testq	%rsi, %rsi
 2d00f99:      	je	0x2d00fa3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3d93>
 2d00f9b:      	movq	%r12, %rdi
 2d00f9e:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00fa3:      	movq	0xf0(%rsp), %rsi
 2d00fab:      	testq	%rsi, %rsi
 2d00fae:      	je	0x2d00fbd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3dad>
 2d00fb0:      	leaq	0xf0(%rsp), %rdi
 2d00fb8:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d00fbd:      	movq	0x28(%rsp), %rcx
 2d00fc2:      	movzwl	0x28(%rcx), %eax
 2d00fc6:      	movzbl	0x2a(%rcx), %ebx
 2d00fca:      	shll	$0x10, %ebx
 2d00fcd:      	orl	%eax, %ebx
 2d00fcf:      	cmpl	$0x3, %ebx
 2d00fd2:      	je	0x2d01008 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3df8>
 2d00fd4:      	movq	0x28(%rsp), %rax
 2d00fd9:      	movq	0x20(%rax), %r13
 2d00fdd:      	shll	$0x5, %ebx
 2d00fe0:      	addq	$0x60, %r13
 2d00fe4:      	addq	$-0x60, %rbx
 2d00fe8:      	nopl	(%rax,%rax)
 2d00ff0:      	movq	%r15, %rdi
 2d00ff3:      	movq	%r14, %rsi
 2d00ff6:      	movq	%r13, %rdx
 2d00ff9:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d00ffe:      	addq	$0x20, %r13
 2d01002:      	addq	$-0x20, %rbx
 2d01006:      	jne	0x2d00ff0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3de0>
 2d01008:      	movq	0x28(%rsp), %r12
 2d0100d:      	movq	0x30(%r12), %rax
 2d01012:      	cmpq	$0x8, %rax
 2d01016:      	jb	0x2d0103b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2b>
 2d01018:      	movl	%eax, %ecx
 2d0101a:      	andl	$0x7, %ecx
 2d0101d:      	cmpq	$0x3, %rcx
 2d01021:      	je	0x2d01290 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4080>
 2d01027:      	testq	%rcx, %rcx
 2d0102a:      	jne	0x2d0103b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2b>
 2d0102c:      	leaq	0x30(%r12), %rdx
 2d01031:      	movq	%rax, (%rdx)
 2d01034:      	movl	$0x1, %ecx
 2d01039:      	jmp	0x2d0103f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2f>
 2d0103b:      	xorl	%edx, %edx
 2d0103d:      	xorl	%ecx, %ecx
 2d0103f:      	movq	%r15, %rdi
 2d01042:      	movq	%r14, %rsi
 2d01045:      	callq	0x3651960 <_ZN4llvm12MachineInstr10setMemRefsERNS_15MachineFunctionENS_8ArrayRefIPNS_17MachineMemOperandEEE>
 2d0104a:      	testb	$0x4, (%r12)
 2d0104f:      	movq	%r12, %rax
 2d01052:      	jne	0x2d0107a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e6a>
 2d01054:      	testb	$0x8, 0x2c(%r12)
 2d0105a:      	movq	%r12, %rax
 2d0105d:      	je	0x2d0107a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e6a>
 2d0105f:      	movq	%r12, %rax
 2d01062:      	nopw	%cs:(%rax,%rax)
 2d0106c:      	nopl	(%rax)
 2d01070:      	movq	0x8(%rax), %rax
 2d01074:      	testb	$0x8, 0x2c(%rax)
 2d01078:      	jne	0x2d01070 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e60>
 2d0107a:      	movq	0x8(%rax), %rax
 2d0107e:      	movq	%rax, 0x10(%rsp)
 2d01083:      	cmpq	%rax, %r12
 2d01086:      	xorps	%xmm0, %xmm0
 2d01089:      	jne	0x2d010e5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ed5>
 2d0108b:      	movq	0xa0(%rsp), %rsi
 2d01093:      	testq	%rsi, %rsi
 2d01096:      	je	0x2cffa49 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2839>
 2d0109c:      	leaq	0xa0(%rsp), %rdi
 2d010a4:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d010a9:      	jmp	0x2cffa49 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2839>
 2d010ae:      	nop
 2d010b0:      	movl	%ecx, 0xf0(%r13)
 2d010b7:      	movq	(%r14), %rax
 2d010ba:      	movq	(%rax,%r12,8), %rcx
 2d010be:      	movq	%rcx, (%rbp)
 2d010c2:      	movq	%rbp, (%rax,%r12,8)
 2d010c6:      	movq	%r15, %r12
 2d010c9:      	movq	0xe0(%r13), %rax
 2d010d0:      	movq	%rax, (%r12)
 2d010d4:      	movq	%r12, 0xe0(%r13)
 2d010db:      	movq	%rbx, %r12
 2d010de:      	cmpq	0x10(%rsp), %rbx
 2d010e3:      	je	0x2d0108b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e7b>
 2d010e5:      	movq	0x8(%r12), %rbx
 2d010ea:      	movq	0x18(%r12), %rax
 2d010ef:      	movq	0x20(%rax), %r14
 2d010f3:      	testq	%r14, %r14
 2d010f6:      	je	0x2d011b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d010fc:      	movq	0x288(%r14), %rdi
 2d01103:      	testq	%rdi, %rdi
 2d01106:      	je	0x2d01114 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f04>
 2d01108:      	movq	(%rdi), %rax
 2d0110b:      	movq	%r12, %rsi
 2d0110e:      	callq	*0x20(%rax)
 2d01111:      	xorps	%xmm0, %xmm0
 2d01114:      	movzwl	0x28(%r12), %ecx
 2d0111a:      	movzbl	0x2a(%r12), %eax
 2d01120:      	shll	$0x10, %eax
 2d01123:      	orl	%ecx, %eax
 2d01125:      	testl	%eax, %eax
 2d01127:      	je	0x2d011b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d0112d:      	movq	0x20(%r12), %rcx
 2d01132:      	shll	$0x5, %eax
 2d01135:      	movq	0x20(%r14), %rdx
 2d01139:      	jmp	0x2d01161 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f51>
 2d0113b:      	nopl	(%rax,%rax)
 2d01140:      	movq	%rdi, 0x18(%r8)
 2d01144:      	leaq	0x10(%rcx), %r9
 2d01148:      	testq	%rdi, %rdi
 2d0114b:      	cmovneq	%rdi, %rsi
 2d0114f:      	movq	%r8, 0x10(%rsi)
 2d01153:      	movups	%xmm0, (%r9)
 2d01157:      	addq	$0x20, %rcx
 2d0115b:      	addq	$-0x20, %rax
 2d0115f:      	je	0x2d011b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3fa0>
 2d01161:      	cmpb	$0x0, (%rcx)
 2d01164:      	jne	0x2d01157 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f47>
 2d01166:      	movl	0x4(%rcx), %esi
 2d01169:      	movl	%esi, %edi
 2d0116b:      	andl	$0x7fffffff, %edi       # imm = 0x7FFFFFFF
 2d01171:      	shlq	$0x4, %rdi
 2d01175:      	movq	%rsi, %r8
 2d01178:      	shlq	$0x3, %r8
 2d0117c:      	addq	0x128(%rdx), %r8
 2d01183:      	testl	%esi, %esi
 2d01185:      	movq	0x30(%rdx), %rsi
 2d01189:      	leaq	0x8(%rsi,%rdi), %r9
 2d0118e:      	cmovnsq	%r8, %r9
 2d01192:      	movq	(%r9), %rsi
 2d01195:      	movq	0x18(%rcx), %rdi
 2d01199:      	movq	0x10(%rcx), %r8
 2d0119d:      	cmpq	%rsi, %rcx
 2d011a0:      	jne	0x2d01140 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f30>
 2d011a2:      	movq	%rdi, (%r9)
 2d011a5:      	jmp	0x2d01144 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3f34>
 2d011a7:      	nopw	(%rax,%rax)
 2d011b0:      	movq	$0x0, 0x18(%r12)
 2d011b9:      	movq	(%r12), %rax
 2d011bd:      	movq	0x8(%r12), %rcx
 2d011c2:      	andq	$-0x8, %rax
 2d011c6:      	movq	(%rcx), %rdx
 2d011c9:      	andl	$0x7, %edx
 2d011cc:      	orq	%rax, %rdx
 2d011cf:      	movq	%rdx, (%rcx)
 2d011d2:      	movq	%rcx, 0x8(%rax)
 2d011d6:      	andq	$0x7, (%r12)
 2d011db:      	movq	$0x0, 0x8(%r12)
 2d011e4:      	movq	0x18(%rsp), %rax
 2d011e9:      	movq	0x28(%rax), %rax
 2d011ed:      	movq	0x20(%rax), %r13
 2d011f1:      	movq	0x20(%r12), %rbp
 2d011f6:      	testq	%rbp, %rbp
 2d011f9:      	je	0x2d010c9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3eb9>
 2d011ff:      	movq	%r12, %r15
 2d01202:      	movzbl	0x2b(%r12), %r12d
 2d01208:      	leaq	0xe8(%r13), %r14
 2d0120f:      	movl	0xf0(%r13), %eax
 2d01216:      	cmpl	%r12d, %eax
 2d01219:      	ja	0x2d010b7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea7>
 2d0121f:      	leaq	0x1(%r12), %rcx
 2d01224:      	cmpl	%r12d, 0xf4(%r13)
 2d0122b:      	ja	0x2d01255 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4045>
 2d0122d:      	leaq	0xf8(%r13), %rsi
 2d01234:      	movl	$0x8, %ecx
 2d01239:      	movq	%r14, %rdi
 2d0123c:      	leaq	0x1(%r12), %rdx
 2d01241:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d01246:      	leaq	0x1(%r12), %rcx
 2d0124b:      	xorps	%xmm0, %xmm0
 2d0124e:      	movl	0xf0(%r13), %eax
 2d01255:      	cmpl	%eax, %ecx
 2d01257:      	je	0x2d010b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea0>
 2d0125d:      	movl	%eax, %eax
 2d0125f:      	leaq	(,%rax,8), %rdi
 2d01267:      	addq	(%r14), %rdi
 2d0126a:      	movq	%rcx, %r14
 2d0126d:      	movq	%rcx, %rdx
 2d01270:      	subq	%rax, %rdx
 2d01273:      	shlq	$0x3, %rdx
 2d01277:      	xorl	%esi, %esi
 2d01279:      	callq	0x828ac20 <memset@plt>
 2d0127e:      	movq	%r14, %rcx
 2d01281:      	leaq	0xe8(%r13), %r14
 2d01288:      	xorps	%xmm0, %xmm0
 2d0128b:      	jmp	0x2d010b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3ea0>
 2d01290:      	andq	$-0x8, %rax
 2d01294:      	movslq	(%rax), %rcx
 2d01297:      	addq	$0x10, %rax
 2d0129b:      	movq	%rax, %rdx
 2d0129e:      	jmp	0x2d0103f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3e2f>
 2d012a3:      	movl	$0x3, %esi
 2d012a8:      	addl	0x10(%rsp), %eax
 2d012ac:      	je	0x2d00a4d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x383d>
 2d012b2:      	movl	$0x2, %r12d
 2d012b8:      	jmp	0x2d009d7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x37c7>
 2d012bd:      	negl	%r8d
 2d012c0:      	leal	0x1113(,%rax,4), %esi
 2d012c7:      	jmp	0x2d016e5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d5>
 2d012cc:      	movq	(%rsp), %rcx
 2d012d0:      	cmpb	$0x1, 0x200(%rcx)
 2d012d7:      	movl	%r10d, 0xdc(%rsp)
 2d012df:      	movq	%r9, 0x80(%rsp)
 2d012e7:      	jne	0x2d012f5 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x40e5>
 2d012e9:      	movq	0x1f8(%rcx), %rax
 2d012f0:      	jmp	0x2d0141f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x420f>
 2d012f5:      	movq	0x48(%rcx), %r12
 2d012f9:      	movq	%r12, 0x68(%rcx)
 2d012fd:      	movl	0x78(%rcx), %ebx
 2d01300:      	testq	%rbx, %rbx
 2d01303:      	je	0x2d01323 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4113>
 2d01305:      	leaq	(,%rbx,8), %rdx
 2d0130d:      	movq	0xe0(%rsp), %rax
 2d01315:      	movq	(%rax), %rdi
 2d01318:      	xorl	%esi, %esi
 2d0131a:      	callq	0x828ac20 <memset@plt>
 2d0131f:      	movq	(%rsp), %rcx
 2d01323:      	movl	0x2c(%r12), %ebp
 2d01328:      	movl	0xb0(%rcx), %ecx
 2d0132e:      	andq	$0x3f, %rcx
 2d01332:      	je	0x2d01351 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4141>
 2d01334:      	movq	$-0x1, %rax
 2d0133b:      	shlq	%cl, %rax
 2d0133e:      	notq	%rax
 2d01341:      	movq	0xe0(%rsp), %rcx
 2d01349:      	movq	(%rcx), %rcx
 2d0134c:      	andq	%rax, -0x8(%rcx,%rbx,8)
 2d01351:      	movq	(%rsp), %rax
 2d01355:      	movl	%ebp, 0xb0(%rax)
 2d0135b:      	leal	0x3f(%rbp), %edx
 2d0135e:      	shrl	$0x6, %edx
 2d01361:      	cmpl	%ebx, %edx
 2d01363:      	je	0x2d013a8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4198>
 2d01365:      	jb	0x2d013a3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4193>
 2d01367:      	movq	%rbx, %rdi
 2d0136a:      	movl	%ebx, %r12d
 2d0136d:      	cmpl	0x7c(%rax), %edx
 2d01370:      	ja	0x2d0218c <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f7c>
 2d01376:      	subq	%rbx, %rdx
 2d01379:      	shlq	$0x3, %rdi
 2d0137d:      	movq	0xe0(%rsp), %rax
 2d01385:      	addq	(%rax), %rdi
 2d01388:      	movq	%rdx, %rbx
 2d0138b:      	leal	(,%rdx,8), %edx
 2d01392:      	xorl	%esi, %esi
 2d01394:      	callq	0x828ac20 <memset@plt>
 2d01399:      	addl	%ebx, %r12d
 2d0139c:      	movl	%r12d, %edx
 2d0139f:      	movq	(%rsp), %rax
 2d013a3:      	movl	%edx, 0x78(%rax)
 2d013a6:      	movl	%edx, %ebx
 2d013a8:      	andl	$0x3f, %ebp
 2d013ab:      	je	0x2d013ce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41be>
 2d013ad:      	movq	$-0x1, %rax
 2d013b4:      	movl	%ebp, %ecx
 2d013b6:      	shlq	%cl, %rax
 2d013b9:      	notq	%rax
 2d013bc:      	movq	0xe0(%rsp), %rcx
 2d013c4:      	movq	(%rcx), %rcx
 2d013c7:      	movl	%ebx, %edx
 2d013c9:      	andq	%rax, -0x8(%rcx,%rdx,8)
 2d013ce:      	movq	0x118(%rsp), %rdi
 2d013d6:      	movq	0x10(%rsp), %rbx
 2d013db:      	movq	%rbx, %rsi
 2d013de:      	callq	0x35c0cc0 <_ZN4llvm12LiveRegUnits11addLiveOutsERKNS_17MachineBasicBlockE>
 2d013e3:      	leaq	0x30(%rbx), %rax
 2d013e7:      	movq	(%rsp), %rcx
 2d013eb:      	movq	%rax, 0x1f8(%rcx)
 2d013f2:      	movb	$0x1, 0x200(%rcx)
 2d013f9:      	movq	0x78(%rsp), %rbx
 2d013fe:      	jmp	0x2d0141f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x420f>
 2d01400:      	movq	%rsi, 0x1f8(%rcx)
 2d01407:      	movq	0x118(%rsp), %rdi
 2d0140f:      	callq	0x35c0330 <_ZN4llvm12LiveRegUnits12stepBackwardERKNS_12MachineInstrE>
 2d01414:      	movq	(%rsp), %rcx
 2d01418:      	movq	0x1f8(%rcx), %rax
 2d0141f:      	cmpq	0x20(%rsp), %rax
 2d01424:      	je	0x2d01455 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4245>
 2d01426:      	movq	(%rax), %rsi
 2d01429:      	andq	$-0x8, %rsi
 2d0142d:      	testb	$0x4, (%rsi)
 2d01430:      	jne	0x2d01400 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d01432:      	nopw	%cs:(%rax,%rax)
 2d0143c:      	nopl	(%rax)
 2d01440:      	testb	$0x4, 0x2c(%rsi)
 2d01444:      	je	0x2d01400 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d01446:      	movq	(%rsi), %rsi
 2d01449:      	andq	$-0x8, %rsi
 2d0144d:      	testb	$0x4, 0x2c(%rsi)
 2d01451:      	jne	0x2d01446 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4236>
 2d01453:      	jmp	0x2d01400 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x41f0>
 2d01455:      	cmpl	$0x104b, %ebx           # imm = 0x104B
 2d0145b:      	jle	0x2d01486 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4276>
 2d0145d:      	leal	-0x104c(%rbx), %eax
 2d01463:      	cmpl	$0x2, %eax
 2d01466:      	jb	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0146c:      	cmpl	$0x117a, %ebx           # imm = 0x117A
 2d01472:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01478:      	cmpl	$0x117d, %ebx           # imm = 0x117D
 2d0147e:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01484:      	jmp	0x2d014aa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x429a>
 2d01486:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d0148c:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d01492:      	cmpl	$0xb51, %ebx            # imm = 0xB51
 2d01498:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d0149e:      	cmpl	$0xb53, %ebx            # imm = 0xB53
 2d014a4:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d014aa:      	movq	0x118(%rsp), %rax
 2d014b2:      	movq	(%rax), %rcx
 2d014b5:      	movq	0x38(%rcx), %rax
 2d014b9:      	testq	%rax, %rax
 2d014bc:      	je	0x2d0152d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x431d>
 2d014be:      	movq	0x80(%rsp), %rdx
 2d014c6:      	leaq	(%r14,%rdx,8), %rdx
 2d014ca:      	movq	0xe0(%rsp), %rsi
 2d014d2:      	movq	(%rsi), %rsi
 2d014d5:      	movq	0x8(%rcx), %rdi
 2d014d9:      	movq	%r14, %r8
 2d014dc:      	movl	(%r8), %ecx
 2d014df:      	leaq	(%rcx,%rcx,2), %rcx
 2d014e3:      	movl	0x10(%rdi,%rcx,8), %ecx
 2d014e7:      	movl	%ecx, %r9d
 2d014ea:      	shrl	$0xc, %r9d
 2d014ee:      	leaq	(%rax,%r9,2), %r9
 2d014f2:      	andl	$0xfff, %ecx            # imm = 0xFFF
 2d014f8:      	nopl	(%rax,%rax)
 2d01500:      	movl	$0x1, %r10d
 2d01506:      	shlq	%cl, %r10
 2d01509:      	movl	%ecx, %r11d
 2d0150c:      	shrl	$0x6, %r11d
 2d01510:      	orq	%r10, (%rsi,%r11,8)
 2d01514:      	movswl	(%r9), %r10d
 2d01518:      	addq	$0x2, %r9
 2d0151c:      	addl	%r10d, %ecx
 2d0151f:      	testl	%r10d, %r10d
 2d01522:      	jne	0x2d01500 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x42f0>
 2d01524:      	addq	$0x8, %r8
 2d01528:      	cmpq	%rdx, %r8
 2d0152b:      	jne	0x2d014dc <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x42cc>
 2d0152d:      	movq	(%rsp), %rcx
 2d01531:      	cmpb	$0x0, 0x202(%rcx)
 2d01538:      	leaq	0x55aa8b9(%rip), %rbp   # 0x82abdf8 <_ZN4llvm3ARM11GPRRegClassE>
 2d0153f:      	leaq	0x55a8012(%rip), %rax   # 0x82a9558 <_ZN4llvm3ARM12tGPRRegClassE>
 2d01546:      	cmovneq	%rax, %rbp
 2d0154a:      	cmpb	$0x0, 0x201(%rcx)
 2d01551:      	jne	0x2d01571 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4361>
 2d01553:      	movq	0x38(%rcx), %rsi
 2d01557:      	movq	0x1f8(%rsp), %rdi
 2d0155f:      	xorl	%edx, %edx
 2d01561:      	callq	0x38536d0 <_ZN4llvm17RegisterClassInfo20runOnMachineFunctionERKNS_15MachineFunctionEb>
 2d01566:      	movq	(%rsp), %rcx
 2d0156a:      	movb	$0x1, 0x201(%rcx)
 2d01571:      	movq	(%rbp), %rax
 2d01575:      	movzwl	0x18(%rax), %eax
 2d01579:      	movq	0xb8(%rcx), %rbx
 2d01580:      	leaq	(%rax,%rax,2), %r12
 2d01584:      	movl	0xc0(%rcx), %eax
 2d0158a:      	cmpl	(%rbx,%r12,8), %eax
 2d0158e:      	je	0x2d015a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4390>
 2d01590:      	movq	0x1f8(%rsp), %rdi
 2d01598:      	movq	%rbp, %rsi
 2d0159b:      	callq	0x3853ec0 <_ZNK4llvm17RegisterClassInfo7computeEPKNS_19TargetRegisterClassE>
 2d015a0:      	leaq	(%rbx,%r12,8), %rax
 2d015a4:      	movl	0x4(%rax), %esi
 2d015a7:      	testq	%rsi, %rsi
 2d015aa:      	movq	0x80(%rsp), %rbx
 2d015b2:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d015b8:      	movq	0x10(%rax), %rax
 2d015bc:      	movq	(%rsp), %rdi
 2d015c0:      	movq	0x38(%rdi), %rcx
 2d015c4:      	movq	0x68(%rdi), %r8
 2d015c8:      	movq	0x38(%r8), %rdx
 2d015cc:      	testq	%rdx, %rdx
 2d015cf:      	je	0x2d01f56 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d46>
 2d015d5:      	leaq	(%rax,%rsi,2), %rsi
 2d015d9:      	movq	0x70(%rdi), %rdi
 2d015dd:      	movq	0x8(%r8), %r8
 2d015e1:      	jmp	0x2d015f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43e0>
 2d015e3:      	addq	$0x2, %rax
 2d015e7:      	cmpq	%rsi, %rax
 2d015ea:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d015f0:      	movzwl	(%rax), %r12d
 2d015f4:      	leaq	(%r12,%r12,2), %r9
 2d015f8:      	movl	0x10(%r8,%r9,8), %r9d
 2d015fd:      	movl	%r9d, %r10d
 2d01600:      	shrl	$0xc, %r10d
 2d01604:      	leaq	(%rdx,%r10,2), %r10
 2d01608:      	andl	$0xfff, %r9d            # imm = 0xFFF
 2d0160f:      	nop
 2d01610:      	movl	%r9d, %r11d
 2d01613:      	shrl	$0x6, %r11d
 2d01617:      	movq	(%rdi,%r11,8), %r11
 2d0161b:      	btq	%r9, %r11
 2d0161f:      	jb	0x2d015e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43d3>
 2d01621:      	movswl	(%r10), %r11d
 2d01625:      	addq	$0x2, %r10
 2d01629:      	addl	%r11d, %r9d
 2d0162c:      	testl	%r11d, %r11d
 2d0162f:      	jne	0x2d01610 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4400>
 2d01631:      	movq	0x20(%rcx), %r9
 2d01635:      	movq	0x178(%r9), %r9
 2d0163c:      	movl	%r12d, %r10d
 2d0163f:      	shrl	$0x6, %r10d
 2d01643:      	movq	(%r9,%r10,8), %r9
 2d01647:      	btq	%r12, %r9
 2d0164b:      	jb	0x2d015e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x43d3>
 2d0164d:      	testl	%r12d, %r12d
 2d01650:      	movl	0xdc(%rsp), %eax
 2d01657:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d0165d:      	movq	%rbx, %r9
 2d01660:      	movq	(%rsp), %rcx
 2d01664:      	movzbl	0x203(%rcx), %esi
 2d0166b:      	movl	0x18(%rsp), %r8d
 2d01670:      	movl	%eax, 0xdc(%rsp)
 2d01677:      	testb	%sil, %sil
 2d0167a:      	jne	0x2cffc8a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2a7a>
 2d01680:      	movq	%r9, %rbx
 2d01683:      	movzbl	0x202(%rcx), %eax
 2d0168a:      	xorl	%esi, %esi
 2d0168c:      	cmpl	$0x8, %r8d
 2d01690:      	setge	%sil
 2d01694:      	addl	$0x1151, %esi           # imm = 0x1151
 2d0169a:      	cmpl	$0x11, 0x8(%rsp)
 2d0169f:      	movl	$0x1154, %edx           # imm = 0x1154
 2d016a4:      	cmovel	%edx, %esi
 2d016a7:      	testb	%al, %al
 2d016a9:      	movl	$0x325, %edx            # imm = 0x325
 2d016ae:      	cmovel	%edx, %esi
 2d016b1:      	testl	%r8d, %r8d
 2d016b4:      	jns	0x2d016e9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x44d9>
 2d016b6:      	movl	%r8d, %ecx
 2d016b9:      	negl	%ecx
 2d016bb:      	cmpl	$-0x7, %r8d
 2d016bf:      	setae	%dl
 2d016c2:      	cmpl	$0x11, 0x8(%rsp)
 2d016c7:      	setne	%sil
 2d016cb:      	andb	%dl, %sil
 2d016ce:      	movzbl	%sil, %esi
 2d016d2:      	xorl	$0x119b, %esi           # imm = 0x119B
 2d016d8:      	testb	%al, %al
 2d016da:      	movl	$0x7fb, %eax            # imm = 0x7FB
 2d016df:      	cmovel	%eax, %esi
 2d016e2:      	movl	%ecx, %r8d
 2d016e5:      	movq	(%rsp), %rcx
 2d016e9:      	movq	%rsi, 0x128(%rsp)
 2d016f1:      	movq	0x58(%rcx), %rdi
 2d016f5:      	movl	%r8d, %ebp
 2d016f8:      	movq	(%rdi), %rax
 2d016fb:      	movq	%rbp, %rsi
 2d016fe:      	callq	*0x530(%rax)
 2d01704:      	testb	%al, %al
 2d01706:      	je	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d0170c:      	movq	%rbx, %rdx
 2d0170f:      	movq	%r12, 0x18(%rsp)
 2d01714:      	cmpl	$-0x1, 0x70(%rsp)
 2d01719:      	je	0x2d0177a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x456a>
 2d0171b:      	movq	0x78(%rsp), %rax
 2d01720:      	cmpl	$0x7f9, %eax            # imm = 0x7F9
 2d01725:      	movq	0x20(%rsp), %r12
 2d0172a:      	je	0x2d01748 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d0172c:      	cmpl	$0x1197, %eax           # imm = 0x1197
 2d01731:      	je	0x2d01748 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d01733:      	cmpl	$0x1199, %eax           # imm = 0x1199
 2d01738:      	je	0x2d01748 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4538>
 2d0173a:      	addl	$0xffffeef1, %eax       # imm = 0xFFFFEEF1
 2d0173f:      	movb	$0x1, %r13b
 2d01742:      	cmpw	$0x1, %ax
 2d01746:      	ja	0x2d01782 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d01748:      	leaq	-0x8(,%rdx,8), %rax
 2d01750:      	xorl	%ecx, %ecx
 2d01752:      	nopw	%cs:(%rax,%rax)
 2d0175c:      	nopl	(%rax)
 2d01760:      	movq	0x8(%rsp), %rsi
 2d01765:      	cmpl	%esi, (%r14,%rcx)
 2d01769:      	setne	%r13b
 2d0176d:      	je	0x2d01782 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d0176f:      	cmpq	%rcx, %rax
 2d01772:      	leaq	0x8(%rcx), %rcx
 2d01776:      	jne	0x2d01760 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4550>
 2d01778:      	jmp	0x2d01782 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4572>
 2d0177a:      	xorl	%r13d, %r13d
 2d0177d:      	movq	0x20(%rsp), %r12
 2d01782:      	movq	(%rsp), %rcx
 2d01786:      	cmpb	$0x1, 0x202(%rcx)
 2d0178d:      	movq	%rdx, 0x80(%rsp)
 2d01795:      	jne	0x2d01b51 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4941>
 2d0179b:      	movq	0x8(%rsp), %rax
 2d017a0:      	cmpl	0x18(%rsp), %eax
 2d017a4:      	leaq	0xa0(%rsp), %rax
 2d017ac:      	je	0x2d01993 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4783>
 2d017b2:      	movq	0x128(%rsp), %rcx
 2d017ba:      	cmpl	$0x119b, %ecx           # imm = 0x119B
 2d017c0:      	je	0x2d017ce <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x45be>
 2d017c2:      	cmpl	$0x1152, %ecx           # imm = 0x1152
 2d017c8:      	jne	0x2d0199b <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x478b>
 2d017ce:      	movq	0x18(%rsp), %rax
 2d017d3:      	addl	$-0x4a, %eax
 2d017d6:      	movq	0x8(%rsp), %rcx
 2d017db:      	addl	$-0x4a, %ecx
 2d017de:      	orl	%eax, %ecx
 2d017e0:      	cmpl	$0x7, %ecx
 2d017e3:      	movq	(%rsp), %rcx
 2d017e7:      	ja	0x2d017fa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x45ea>
 2d017e9:      	movq	0x50(%rcx), %rax
 2d017ed:      	cmpb	$0x0, 0x181(%rax)
 2d017f4:      	je	0x2d01f8d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d7d>
 2d017fa:      	movq	0xc8(%rsp), %rsi
 2d01802:      	movq	%rsi, 0x1b0(%rsp)
 2d0180a:      	leaq	0xa0(%rsp), %rax
 2d01812:      	testq	%rsi, %rsi
 2d01815:      	je	0x2d01861 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4651>
 2d01817:      	movl	$0x1, %edx
 2d0181c:      	leaq	0x1b0(%rsp), %rdi
 2d01824:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01829:      	movq	(%rsp), %rcx
 2d0182d:      	movq	0x1b0(%rsp), %rsi
 2d01835:      	movq	%rsi, 0xa0(%rsp)
 2d0183d:      	testq	%rsi, %rsi
 2d01840:      	je	0x2d01868 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4658>
 2d01842:      	leaq	0x1b0(%rsp), %rbx
 2d0184a:      	movq	%rbx, %rdi
 2d0184d:      	leaq	0xa0(%rsp), %rdx
 2d01855:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d0185a:      	movq	(%rsp), %rcx
 2d0185e:      	movq	%rbx, %rax
 2d01861:      	movq	$0x0, (%rax)
 2d01868:      	movq	%rbp, 0x70(%rsp)
 2d0186d:      	leaq	0xa8(%rsp), %rax
 2d01875:      	xorps	%xmm0, %xmm0
 2d01878:      	movups	%xmm0, (%rax)
 2d0187b:      	movq	$0x0, 0x10(%rax)
 2d01883:      	movq	0x40(%rcx), %rax
 2d01887:      	movq	0x8(%rax), %rcx
 2d0188b:      	movq	$-0x23080, %rax         # imm = 0xFFFDCF80
 2d01892:      	addq	%rax, %rcx
 2d01895:      	movq	0x10(%rsp), %rdi
 2d0189a:      	movq	%r12, %rsi
 2d0189d:      	leaq	0xa0(%rsp), %rbx
 2d018a5:      	movq	%rbx, %rdx
 2d018a8:      	movq	0x18(%rsp), %r12
 2d018ad:      	movl	%r12d, %r8d
 2d018b0:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d018b5:      	movq	%rax, 0xf0(%rsp)
 2d018bd:      	movq	%rdx, 0xf8(%rsp)
 2d018c5:      	movzbl	%r13b, %edx
 2d018c9:      	shll	$0x3, %edx
 2d018cc:      	leaq	0xf0(%rsp), %rdi
 2d018d4:      	movq	0x8(%rsp), %rsi
 2d018d9:      	xorl	%ecx, %ecx
 2d018db:      	callq	0x27f0690 <_ZNK4llvm19MachineInstrBuilder6addRegENS_8RegisterEjj>
 2d018e0:      	movq	%rax, %rbp
 2d018e3:      	movl	0x28(%rsp), %eax
 2d018e7:      	movl	$0x1, 0x30(%rsp)
 2d018ef:      	movq	$0x0, 0x38(%rsp)
 2d018f8:      	movq	%rax, 0x40(%rsp)
 2d018fd:      	movq	$0x0, 0x58(%rsp)
 2d01906:      	movq	0x88(%rsp), %rax
 2d0190e:      	movl	%eax, 0x54(%rsp)
 2d01912:      	leaq	0x40(%rsp), %rax
 2d01917:      	xorps	%xmm0, %xmm0
 2d0191a:      	movups	%xmm0, 0x20(%rax)
 2d0191e:      	movl	$0x0, 0x50(%rsp)
 2d01926:      	movq	(%rbp), %rsi
 2d0192a:      	movq	0x8(%rbp), %rdi
 2d0192e:      	leaq	0x30(%rsp), %rdx
 2d01933:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01938:      	movq	(%rbp), %rsi
 2d0193c:      	movq	0x8(%rbp), %rdi
 2d01940:      	leaq	0x50(%rsp), %rdx
 2d01945:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d0194a:      	movq	0xa0(%rsp), %rsi
 2d01952:      	testq	%rsi, %rsi
 2d01955:      	je	0x2d0195f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x474f>
 2d01957:      	movq	%rbx, %rdi
 2d0195a:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d0195f:      	movq	0x1b0(%rsp), %rsi
 2d01967:      	testq	%rsi, %rsi
 2d0196a:      	je	0x2d01979 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4769>
 2d0196c:      	leaq	0x1b0(%rsp), %rdi
 2d01974:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01979:      	movb	$0x1, %r13b
 2d0197c:      	movq	%r12, 0x8(%rsp)
 2d01981:      	leaq	0xa0(%rsp), %rax
 2d01989:      	movq	0x20(%rsp), %r12
 2d0198e:      	movq	0x70(%rsp), %rbp
 2d01993:      	movq	0x128(%rsp), %rcx
 2d0199b:      	cmpl	$0x1154, %ecx           # imm = 0x1154
 2d019a1:      	jne	0x2d01d31 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b21>
 2d019a7:      	movq	0xc8(%rsp), %rsi
 2d019af:      	movq	%rsi, 0x1a8(%rsp)
 2d019b7:      	testq	%rsi, %rsi
 2d019ba:      	je	0x2d019fe <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47ee>
 2d019bc:      	movl	$0x1, %edx
 2d019c1:      	leaq	0x1a8(%rsp), %rdi
 2d019c9:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d019ce:      	movq	0x1a8(%rsp), %rsi
 2d019d6:      	movq	%rsi, 0xa0(%rsp)
 2d019de:      	testq	%rsi, %rsi
 2d019e1:      	je	0x2d01a05 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x47f5>
 2d019e3:      	leaq	0x1a8(%rsp), %rbx
 2d019eb:      	movq	%rbx, %rdi
 2d019ee:      	leaq	0xa0(%rsp), %rdx
 2d019f6:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d019fb:      	movq	%rbx, %rax
 2d019fe:      	movq	$0x0, (%rax)
 2d01a05:      	leaq	0xa8(%rsp), %rax
 2d01a0d:      	xorps	%xmm0, %xmm0
 2d01a10:      	movups	%xmm0, (%rax)
 2d01a13:      	movq	$0x0, 0x10(%rax)
 2d01a1b:      	movq	(%rsp), %rax
 2d01a1f:      	movq	0x40(%rax), %rax
 2d01a23:      	movq	0x8(%rax), %rcx
 2d01a27:      	movq	$-0x22a80, %rax         # imm = 0xFFFDD580
 2d01a2e:      	addq	%rax, %rcx
 2d01a31:      	movq	0x10(%rsp), %rdi
 2d01a36:      	movq	%r12, %rsi
 2d01a39:      	leaq	0xa0(%rsp), %rdx
 2d01a41:      	movq	0x18(%rsp), %r8
 2d01a46:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01a4b:      	movq	%rax, %rsi
 2d01a4e:      	movq	%rdx, %rbx
 2d01a51:      	movq	$0x0, 0x38(%rsp)
 2d01a5a:      	movzbl	%r13b, %eax
 2d01a5e:      	shll	$0x1a, %eax
 2d01a61:      	movq	0x8(%rsp), %rcx
 2d01a66:      	movl	%ecx, 0x34(%rsp)
 2d01a6a:      	leaq	0x40(%rsp), %rcx
 2d01a6f:      	xorps	%xmm0, %xmm0
 2d01a72:      	movups	%xmm0, (%rcx)
 2d01a75:      	movl	%eax, 0x30(%rsp)
 2d01a79:      	movq	%rdx, %rdi
 2d01a7c:      	movq	%rsi, %r13
 2d01a7f:      	leaq	0x30(%rsp), %r12
 2d01a84:      	movq	%r12, %rdx
 2d01a87:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01a8c:      	shrl	$0x2, %ebp
 2d01a8f:      	movl	$0x1, 0x30(%rsp)
 2d01a97:      	movq	$0x0, 0x38(%rsp)
 2d01aa0:      	movq	%rbp, 0x40(%rsp)
 2d01aa5:      	movq	%rbx, %rdi
 2d01aa8:      	movq	%r13, %rsi
 2d01aab:      	movq	%r12, %rdx
 2d01aae:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01ab3:      	movl	0x28(%rsp), %eax
 2d01ab7:      	movl	$0x1, 0x30(%rsp)
 2d01abf:      	movq	$0x0, 0x38(%rsp)
 2d01ac8:      	movq	%rax, 0x40(%rsp)
 2d01acd:      	movq	$0x0, 0x58(%rsp)
 2d01ad6:      	movq	0x88(%rsp), %rax
 2d01ade:      	movl	%eax, 0x54(%rsp)
 2d01ae2:      	xorps	%xmm0, %xmm0
 2d01ae5:      	leaq	0x40(%rsp), %rax
 2d01aea:      	movups	%xmm0, 0x20(%rax)
 2d01aee:      	movl	$0x0, 0x50(%rsp)
 2d01af6:      	movq	%rbx, %rdi
 2d01af9:      	movq	%r13, %rsi
 2d01afc:      	movq	%r12, %rdx
 2d01aff:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01b04:      	movq	%rbx, %rdi
 2d01b07:      	movq	%r13, %rsi
 2d01b0a:      	leaq	0x50(%rsp), %rdx
 2d01b0f:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01b14:      	movq	0xa0(%rsp), %rsi
 2d01b1c:      	testq	%rsi, %rsi
 2d01b1f:      	je	0x2d01b2e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x491e>
 2d01b21:      	leaq	0xa0(%rsp), %rdi
 2d01b29:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01b2e:      	movq	0x1a8(%rsp), %rsi
 2d01b36:      	testq	%rsi, %rsi
 2d01b39:      	movq	0x78(%rsp), %rbx
 2d01b3e:      	je	0x2d01f23 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01b44:      	leaq	0x1a8(%rsp), %rdi
 2d01b4c:      	jmp	0x2d01f1e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d0e>
 2d01b51:      	movq	0xc8(%rsp), %rsi
 2d01b59:      	movq	%rsi, 0x198(%rsp)
 2d01b61:      	leaq	0xa0(%rsp), %rax
 2d01b69:      	testq	%rsi, %rsi
 2d01b6c:      	je	0x2d01bb8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x49a8>
 2d01b6e:      	movl	$0x1, %edx
 2d01b73:      	leaq	0x198(%rsp), %rdi
 2d01b7b:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01b80:      	movq	(%rsp), %rcx
 2d01b84:      	movq	0x198(%rsp), %rsi
 2d01b8c:      	movq	%rsi, 0xa0(%rsp)
 2d01b94:      	testq	%rsi, %rsi
 2d01b97:      	je	0x2d01bbf <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x49af>
 2d01b99:      	leaq	0x198(%rsp), %rbx
 2d01ba1:      	movq	%rbx, %rdi
 2d01ba4:      	leaq	0xa0(%rsp), %rdx
 2d01bac:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01bb1:      	movq	(%rsp), %rcx
 2d01bb5:      	movq	%rbx, %rax
 2d01bb8:      	movq	$0x0, (%rax)
 2d01bbf:      	leaq	0xa8(%rsp), %rax
 2d01bc7:      	xorps	%xmm0, %xmm0
 2d01bca:      	movups	%xmm0, (%rax)
 2d01bcd:      	movq	$0x0, 0x10(%rax)
 2d01bd5:      	movq	0x40(%rcx), %rax
 2d01bd9:      	movq	0x8(%rax), %rcx
 2d01bdd:      	movq	0x128(%rsp), %rax
 2d01be5:      	shll	$0x5, %eax
 2d01be8:      	subq	%rax, %rcx
 2d01beb:      	movq	0x10(%rsp), %rdi
 2d01bf0:      	movq	%r12, %rsi
 2d01bf3:      	leaq	0xa0(%rsp), %rdx
 2d01bfb:      	movq	0x18(%rsp), %r8
 2d01c00:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01c05:      	movq	%rbp, %rbx
 2d01c08:      	movq	%rdx, %rbp
 2d01c0b:      	movq	$0x0, 0x38(%rsp)
 2d01c14:      	movzbl	%r13b, %edx
 2d01c18:      	shll	$0x1a, %edx
 2d01c1b:      	movq	0x8(%rsp), %rcx
 2d01c20:      	movl	%ecx, 0x34(%rsp)
 2d01c24:      	leaq	0x40(%rsp), %rcx
 2d01c29:      	xorps	%xmm0, %xmm0
 2d01c2c:      	movups	%xmm0, (%rcx)
 2d01c2f:      	movl	%edx, 0x30(%rsp)
 2d01c33:      	movq	%rbp, %rdi
 2d01c36:      	movq	%rax, %r13
 2d01c39:      	movq	%rax, %rsi
 2d01c3c:      	leaq	0x30(%rsp), %r12
 2d01c41:      	movq	%r12, %rdx
 2d01c44:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c49:      	movl	$0x1, 0x30(%rsp)
 2d01c51:      	movq	$0x0, 0x38(%rsp)
 2d01c5a:      	movq	%rbx, 0x40(%rsp)
 2d01c5f:      	movq	%rbp, %rdi
 2d01c62:      	movq	%r13, %rsi
 2d01c65:      	movq	%r12, %rdx
 2d01c68:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01c6d:      	movl	0x28(%rsp), %eax
 2d01c71:      	movl	$0x1, 0x30(%rsp)
 2d01c79:      	movq	$0x0, 0x38(%rsp)
 2d01c82:      	movq	%rax, 0x40(%rsp)
 2d01c87:      	movq	$0x0, 0x58(%rsp)
 2d01c90:      	movq	0x88(%rsp), %rax
 2d01c98:      	movl	%eax, 0x54(%rsp)
 2d01c9c:      	xorps	%xmm0, %xmm0
 2d01c9f:      	leaq	0x40(%rsp), %rax
 2d01ca4:      	movups	%xmm0, 0x20(%rax)
 2d01ca8:      	movl	$0x0, 0x50(%rsp)
 2d01cb0:      	movq	%rbp, %rdi
 2d01cb3:      	movq	%r13, %rsi
 2d01cb6:      	movq	%r12, %rdx
 2d01cb9:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01cbe:      	movq	%rbp, %rdi
 2d01cc1:      	movq	%r13, %rsi
 2d01cc4:      	leaq	0x50(%rsp), %rdx
 2d01cc9:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01cce:      	xorps	%xmm0, %xmm0
 2d01cd1:      	movaps	%xmm0, 0x100(%rsp)
 2d01cd9:      	movaps	%xmm0, 0xf0(%rsp)
 2d01ce1:      	movq	%rbp, %rdi
 2d01ce4:      	movq	%r13, %rsi
 2d01ce7:      	leaq	0xf0(%rsp), %rdx
 2d01cef:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01cf4:      	movq	0xa0(%rsp), %rsi
 2d01cfc:      	testq	%rsi, %rsi
 2d01cff:      	je	0x2d01d0e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4afe>
 2d01d01:      	leaq	0xa0(%rsp), %rdi
 2d01d09:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01d0e:      	movq	0x198(%rsp), %rsi
 2d01d16:      	testq	%rsi, %rsi
 2d01d19:      	movq	0x78(%rsp), %rbx
 2d01d1e:      	je	0x2d01f23 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01d24:      	leaq	0x198(%rsp), %rdi
 2d01d2c:      	jmp	0x2d01f1e <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d0e>
 2d01d31:      	movq	0xc8(%rsp), %rsi
 2d01d39:      	movq	%rsi, 0x1a0(%rsp)
 2d01d41:      	testq	%rsi, %rsi
 2d01d44:      	je	0x2d01d88 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b78>
 2d01d46:      	movl	$0x1, %edx
 2d01d4b:      	leaq	0x1a0(%rsp), %rdi
 2d01d53:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01d58:      	movq	0x1a0(%rsp), %rsi
 2d01d60:      	movq	%rsi, 0xa0(%rsp)
 2d01d68:      	testq	%rsi, %rsi
 2d01d6b:      	je	0x2d01d8f <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4b7f>
 2d01d6d:      	leaq	0x1a0(%rsp), %rbx
 2d01d75:      	movq	%rbx, %rdi
 2d01d78:      	leaq	0xa0(%rsp), %rdx
 2d01d80:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01d85:      	movq	%rbx, %rax
 2d01d88:      	movq	$0x0, (%rax)
 2d01d8f:      	leaq	0xa8(%rsp), %rax
 2d01d97:      	xorps	%xmm0, %xmm0
 2d01d9a:      	movups	%xmm0, (%rax)
 2d01d9d:      	movq	$0x0, 0x10(%rax)
 2d01da5:      	movq	(%rsp), %rax
 2d01da9:      	movq	0x40(%rax), %rax
 2d01dad:      	movq	0x8(%rax), %rcx
 2d01db1:      	movq	0x128(%rsp), %rax
 2d01db9:      	shll	$0x5, %eax
 2d01dbc:      	subq	%rax, %rcx
 2d01dbf:      	movq	0x10(%rsp), %rdi
 2d01dc4:      	movq	%r12, %rsi
 2d01dc7:      	leaq	0xa0(%rsp), %rdx
 2d01dcf:      	movq	0x18(%rsp), %r8
 2d01dd4:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d01dd9:      	movq	%rax, %rbx
 2d01ddc:      	movq	%rbp, 0x70(%rsp)
 2d01de1:      	movq	%rdx, %rbp
 2d01de4:      	movq	$0x0, 0xf8(%rsp)
 2d01df0:      	movl	$0x3, 0xf4(%rsp)
 2d01dfb:      	leaq	0x100(%rsp), %rax
 2d01e03:      	xorps	%xmm0, %xmm0
 2d01e06:      	movups	%xmm0, (%rax)
 2d01e09:      	movl	$0x5000000, 0xf0(%rsp)  # imm = 0x5000000
 2d01e14:      	movq	%rdx, %rdi
 2d01e17:      	movq	%rbx, %rsi
 2d01e1a:      	leaq	0xf0(%rsp), %rdx
 2d01e22:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e27:      	movq	$0x0, 0x38(%rsp)
 2d01e30:      	movzbl	%r13b, %eax
 2d01e34:      	shll	$0x1a, %eax
 2d01e37:      	movq	0x8(%rsp), %rcx
 2d01e3c:      	movl	%ecx, 0x34(%rsp)
 2d01e40:      	leaq	0x40(%rsp), %r13
 2d01e45:      	xorps	%xmm0, %xmm0
 2d01e48:      	movups	%xmm0, (%r13)
 2d01e4d:      	movl	%eax, 0x30(%rsp)
 2d01e51:      	movq	%rbp, %rdi
 2d01e54:      	movq	%rbx, %rsi
 2d01e57:      	leaq	0x30(%rsp), %r12
 2d01e5c:      	movq	%r12, %rdx
 2d01e5f:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e64:      	movl	$0x1, 0x30(%rsp)
 2d01e6c:      	movq	$0x0, 0x38(%rsp)
 2d01e75:      	movq	0x70(%rsp), %rax
 2d01e7a:      	movq	%rax, 0x40(%rsp)
 2d01e7f:      	movq	%rbp, %rdi
 2d01e82:      	movq	%rbx, %rsi
 2d01e85:      	movq	%r12, %rdx
 2d01e88:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01e8d:      	movl	0x28(%rsp), %eax
 2d01e91:      	movl	$0x1, 0x30(%rsp)
 2d01e99:      	movq	$0x0, 0x38(%rsp)
 2d01ea2:      	movq	%rax, 0x40(%rsp)
 2d01ea7:      	movq	$0x0, 0x58(%rsp)
 2d01eb0:      	movq	0x88(%rsp), %rax
 2d01eb8:      	movl	%eax, 0x54(%rsp)
 2d01ebc:      	xorps	%xmm0, %xmm0
 2d01ebf:      	movups	%xmm0, 0x20(%r13)
 2d01ec4:      	movl	$0x0, 0x50(%rsp)
 2d01ecc:      	movq	%rbp, %rdi
 2d01ecf:      	movq	%rbx, %rsi
 2d01ed2:      	movq	%r12, %rdx
 2d01ed5:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01eda:      	movq	%rbp, %rdi
 2d01edd:      	movq	%rbx, %rsi
 2d01ee0:      	leaq	0x50(%rsp), %rdx
 2d01ee5:      	callq	0x3650670 <_ZN4llvm12MachineInstr10addOperandERNS_15MachineFunctionERKNS_14MachineOperandE>
 2d01eea:      	movq	0xa0(%rsp), %rsi
 2d01ef2:      	testq	%rsi, %rsi
 2d01ef5:      	je	0x2d01f04 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4cf4>
 2d01ef7:      	leaq	0xa0(%rsp), %rdi
 2d01eff:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01f04:      	movq	0x1a0(%rsp), %rsi
 2d01f0c:      	testq	%rsi, %rsi
 2d01f0f:      	movq	0x78(%rsp), %rbx
 2d01f14:      	je	0x2d01f23 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d13>
 2d01f16:      	leaq	0x1a0(%rsp), %rdi
 2d01f1e:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d01f23:      	movl	$0x1, %ecx
 2d01f28:      	movb	$0x1, %al
 2d01f2a:      	movb	$0x1, %r13b
 2d01f2d:      	movq	0x80(%rsp), %r9
 2d01f35:      	movq	0x18(%rsp), %r12
 2d01f3a:      	movl	0xdc(%rsp), %r10d
 2d01f42:      	movb	$0x1, %sil
 2d01f45:      	cmpl	$0x3d7, %ebx            # imm = 0x3D7
 2d01f4b:      	jne	0x2cffcc9 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ab9>
 2d01f51:      	jmp	0x2cffce8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x2ad8>
 2d01f56:      	addq	%rsi, %rsi
 2d01f59:      	movq	0x20(%rcx), %rcx
 2d01f5d:      	movq	0x178(%rcx), %rcx
 2d01f64:      	xorl	%edx, %edx
 2d01f66:      	movzwl	(%rax,%rdx), %r12d
 2d01f6b:      	movl	%r12d, %edi
 2d01f6e:      	shrl	$0x6, %edi
 2d01f71:      	movq	(%rcx,%rdi,8), %rdi
 2d01f75:      	btq	%r12, %rdi
 2d01f79:      	jae	0x2d0164d <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x443d>
 2d01f7f:      	addq	$0x2, %rdx
 2d01f83:      	cmpq	%rdx, %rsi
 2d01f86:      	jne	0x2d01f66 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4d56>
 2d01f88:      	jmp	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01f8d:      	cmpl	$0xe, 0x28(%rsp)
 2d01f92:      	movq	0x18(%rsp), %r12
 2d01f97:      	jne	0x2d020a0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e90>
 2d01f9d:      	movq	%rbp, 0x70(%rsp)
 2d01fa2:      	movq	0xc8(%rsp), %rsi
 2d01faa:      	movq	%rsi, 0x1b8(%rsp)
 2d01fb2:      	leaq	0x30(%rsp), %rax
 2d01fb7:      	testq	%rsi, %rsi
 2d01fba:      	je	0x2d01ff8 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4de8>
 2d01fbc:      	movl	$0x1, %edx
 2d01fc1:      	leaq	0x1b8(%rsp), %rdi
 2d01fc9:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2d01fce:      	movq	0x1b8(%rsp), %rsi
 2d01fd6:      	movq	%rsi, 0x30(%rsp)
 2d01fdb:      	testq	%rsi, %rsi
 2d01fde:      	je	0x2d01fff <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4def>
 2d01fe0:      	leaq	0x1b8(%rsp), %rbx
 2d01fe8:      	movq	%rbx, %rdi
 2d01feb:      	leaq	0x30(%rsp), %rdx
 2d01ff0:      	callq	0x3bd6e80 <_ZN4llvm16MetadataTracking7retrackEPvRNS_8MetadataES1_>
 2d01ff5:      	movq	%rbx, %rax
 2d01ff8:      	movq	$0x0, (%rax)
 2d01fff:      	leaq	0x40(%rsp), %rax
 2d02004:      	xorps	%xmm0, %xmm0
 2d02007:      	movups	%xmm0, -0x8(%rax)
 2d0200b:      	movq	$0x0, 0x8(%rax)
 2d02013:      	movq	(%rsp), %rax
 2d02017:      	movq	0x40(%rax), %rax
 2d0201b:      	movq	0x8(%rax), %rcx
 2d0201f:      	movq	$-0x23040, %rax         # imm = 0xFFFDCFC0
 2d02026:      	addq	%rax, %rcx
 2d02029:      	movq	0x10(%rsp), %rdi
 2d0202e:      	movq	0x20(%rsp), %rsi
 2d02033:      	leaq	0x30(%rsp), %rbx
 2d02038:      	movq	%rbx, %rdx
 2d0203b:      	movl	%r12d, %r8d
 2d0203e:      	callq	0x27f2c80 <_ZN4llvm7BuildMIERNS_17MachineBasicBlockENS_26MachineInstrBundleIteratorINS_12MachineInstrELb0EEERKNS_10MIMetadataERKNS_11MCInstrDescENS_8RegisterE>
 2d02043:      	movq	%rax, 0xa0(%rsp)
 2d0204b:      	movq	%rdx, 0xa8(%rsp)
 2d02053:      	movzbl	%r13b, %edx
 2d02057:      	shll	$0x3, %edx
 2d0205a:      	leaq	0xa0(%rsp), %rdi
 2d02062:      	movq	0x8(%rsp), %rsi
 2d02067:      	xorl	%ecx, %ecx
 2d02069:      	callq	0x27f0690 <_ZNK4llvm19MachineInstrBuilder6addRegENS_8RegisterEjj>
 2d0206e:      	movq	0x30(%rsp), %rsi
 2d02073:      	testq	%rsi, %rsi
 2d02076:      	je	0x2d02080 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4e70>
 2d02078:      	movq	%rbx, %rdi
 2d0207b:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 2d02080:      	movq	0x1b8(%rsp), %rsi
 2d02088:      	testq	%rsi, %rsi
 2d0208b:      	je	0x2d01979 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4769>
 2d02091:      	leaq	0x1b8(%rsp), %rdi
 2d02099:      	jmp	0x2d01974 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4764>
 2d0209e:      	nop
 2d020a0:      	xorl	%r13d, %r13d
 2d020a3:      	movq	0xc8(%rsp), %rsi
 2d020ab:      	testq	%rsi, %rsi
 2d020ae:      	jne	0x2cff9aa <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x279a>
 2d020b4:      	jmp	0x2cff9b7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x27a7>
 2d020b9:      	cmpl	$0x119b, %ebx           # imm = 0x119B
 2d020bf:      	je	0x2d020cd <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ebd>
 2d020c1:      	cmpl	$0x1152, %ebx           # imm = 0x1152
 2d020c7:      	jne	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d020cd:      	movq	0x20(%r12), %r13
 2d020d2:      	movzwl	0x28(%r12), %ecx
 2d020d8:      	movzbl	0x2a(%r12), %eax
 2d020de:      	shll	$0x10, %eax
 2d020e1:      	orl	%ecx, %eax
 2d020e3:      	testl	%eax, %eax
 2d020e5:      	je	0x2d02123 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f13>
 2d020e7:      	shll	$0x5, %eax
 2d020ea:      	xorl	%ecx, %ecx
 2d020ec:      	jmp	0x2d020f7 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ee7>
 2d020ee:      	addq	$0x20, %rcx
 2d020f2:      	cmpq	%rcx, %rax
 2d020f5:      	je	0x2d02123 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4f13>
 2d020f7:      	movl	(%r13,%rcx), %edx
 2d020fc:      	movl	%edx, %esi
 2d020fe:      	andl	$0x10000ff, %esi        # imm = 0x10000FF
 2d02104:      	cmpl	$0x1000000, %esi        # imm = 0x1000000
 2d0210a:      	jne	0x2d020ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d0210c:      	notl	%edx
 2d0210e:      	testl	$0x5000000, %edx        # imm = 0x5000000
 2d02114:      	je	0x2d020ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d02116:      	cmpl	$0x3, 0x4(%r13,%rcx)
 2d0211c:      	jne	0x2d020ee <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ede>
 2d0211e:      	jmp	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d02123:      	movq	0x10(%r12), %rax
 2d02128:      	movzwl	0x2(%rax), %eax
 2d0212c:      	movl	$0xfffffffd, %ecx       # imm = 0xFFFFFFFD
 2d02131:      	leal	(%rcx,%rax), %r14d
 2d02135:      	shlq	$0x5, %r14
 2d02139:      	leal	(,%r9,4), %eax
 2d02141:      	movq	%rax, %rbp
 2d02144:      	negq	%rbp
 2d02147:      	cmpl	$0x119b, %ebx           # imm = 0x119B
 2d0214d:      	cmoveq	%rax, %rbp
 2d02151:      	addq	0x10(%r13,%r14), %rbp
 2d02156:      	testl	%ebp, %ebp
 2d02158:      	js	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d0215e:      	movq	(%rsp), %rax
 2d02162:      	movq	0x58(%rax), %rdi
 2d02166:      	andl	$0x7fffffff, %ebp       # imm = 0x7FFFFFFF
 2d0216c:      	movq	(%rdi), %rax
 2d0216f:      	movq	%rbp, %rsi
 2d02172:      	callq	*0x530(%rax)
 2d02178:      	testb	%al, %al
 2d0217a:      	je	0x2d00528 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x3318>
 2d02180:      	addq	%r14, %r13
 2d02183:      	movq	%rbp, 0x10(%r13)
 2d02187:      	jmp	0x2d008b3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x36a3>
 2d0218c:      	movl	$0x8, %ecx
 2d02191:      	movq	0xe0(%rsp), %rdi
 2d02199:      	movq	0x220(%rsp), %rsi
 2d021a1:      	movq	%rdx, %r12
 2d021a4:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 2d021a9:      	movq	%r12, %rdx
 2d021ac:      	movq	(%rsp), %rax
 2d021b0:      	movl	0x78(%rax), %edi
 2d021b3:      	movl	0xb0(%rax), %ebp
 2d021b9:      	movl	%edi, %r12d
 2d021bc:      	jmp	0x2d01376 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4166>
 2d021c1:      	xorl	%eax, %eax
 2d021c3:      	movq	%rax, %r12
 2d021c6:      	movl	$0x0, 0x270(%rdi)
 2d021d0:      	movl	0x2a0(%rdi), %ebx
 2d021d6:      	testq	%rbx, %rbx
 2d021d9:      	je	0x2d02206 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4ff6>
 2d021db:      	movq	0x298(%rdi), %r14
 2d021e2:      	shlq	$0x3, %rbx
 2d021e6:      	xorl	%r15d, %r15d
 2d021e9:      	nopl	(%rax)
 2d021f0:      	movq	(%r14,%r15), %rsi
 2d021f4:      	callq	0x2d029d0 <_ZNK12_GLOBAL__N_115ARMLoadStoreOpt23MergeBaseUpdateLSDoubleERN4llvm12MachineInstrE>
 2d021f9:      	movq	(%rsp), %rdi
 2d021fd:      	addq	$0x8, %r15
 2d02201:      	cmpq	%r15, %rbx
 2d02204:      	jne	0x2d021f0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x4fe0>
 2d02206:      	movl	$0x0, 0x2a0(%rdi)
 2d02210:      	movq	0x238(%rsp), %rdi
 2d02218:      	leaq	0x248(%rsp), %rax
 2d02220:      	cmpq	%rax, %rdi
 2d02223:      	je	0x2d0222a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x501a>
 2d02225:      	callq	0x828a6d0 <free@plt>
 2d0222a:      	movq	%r12, %rax
 2d0222d:      	andb	$0x1, %al
 2d0222f:      	addq	$0x2c8, %rsp            # imm = 0x2C8
 2d02236:      	popq	%rbx
 2d02237:      	popq	%r12
 2d02239:      	popq	%r13
 2d0223b:      	popq	%r14
 2d0223d:      	popq	%r15
 2d0223f:      	popq	%rbp
 2d02240:      	retq
 2d02241:      	movq	%rbx, %r12
 2d02244:      	jmp	0x2d0228a <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x507a>
 2d02246:      	nopw	%cs:(%rax,%rax)
 2d02250:      	movq	%r12, %rdx
 2d02253:      	subq	%rbx, %rdx
 2d02256:      	movq	%rdx, %rax
 2d02259:      	sarq	$0x3, %rax
 2d0225d:      	cmpq	$0x2, %rax
 2d02261:      	jl	0x2d022c2 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50b2>
 2d02263:      	shlq	$0x3, %rax
 2d02267:      	subq	%rax, %rdi
 2d0226a:      	addq	$0x10, %rdi
 2d0226e:      	movq	%rbx, %rsi
 2d02271:      	callq	0x828ac50 <memmove@plt>
 2d02276:      	movq	%rbx, %rax
 2d02279:      	movq	%r15, (%rax)
 2d0227c:      	leaq	0x8(%r12), %r15
 2d02281:      	cmpq	%r13, %r15
 2d02284:      	je	0x2cfe6c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14b6>
 2d0228a:      	movq	%r12, %rdi
 2d0228d:      	movq	%r15, %r12
 2d02290:      	movq	(%r15), %r15
 2d02293:      	movq	(%rbx), %rsi
 2d02296:      	movl	0x38(%r15), %ecx
 2d0229a:      	cmpl	0x38(%rsi), %ecx
 2d0229d:      	jb	0x2d02250 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5040>
 2d0229f:      	movq	(%rdi), %rdx
 2d022a2:      	movq	%r12, %rax
 2d022a5:      	cmpl	0x38(%rdx), %ecx
 2d022a8:      	jae	0x2d02279 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d022aa:      	movq	%r12, %rax
 2d022ad:      	nopl	(%rax)
 2d022b0:      	movq	%rdx, (%rax)
 2d022b3:      	movq	-0x10(%rax), %rdx
 2d022b7:      	addq	$-0x8, %rax
 2d022bb:      	cmpl	0x38(%rdx), %ecx
 2d022be:      	jb	0x2d022b0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50a0>
 2d022c0:      	jmp	0x2d02279 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d022c2:      	movq	%rbx, %rax
 2d022c5:      	cmpq	$0x8, %rdx
 2d022c9:      	jne	0x2d02279 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5069>
 2d022cb:      	movq	%rsi, 0x8(%rdi)
 2d022cf:      	jmp	0x2d02276 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5066>
 2d022d1:      	movq	%rdx, 0x8(%rcx)
 2d022d5:      	nopw	%cs:(%rax,%rax)
 2d022df:      	nop
 2d022e0:      	movq	%rbx, %rcx
 2d022e3:      	movq	%r14, (%rcx)
 2d022e6:      	addq	$0x8, %r12
 2d022ea:      	addq	$0x8, %r13
 2d022ee:      	cmpq	$0x80, %r12
 2d022f5:      	je	0x2d02352 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5142>
 2d022f7:      	movq	%rbp, %rcx
 2d022fa:      	leaq	(%rbx,%r12), %rbp
 2d022fe:      	movq	(%rbx,%r12), %r14
 2d02302:      	movq	(%rbx), %rdx
 2d02305:      	movl	0x38(%r14), %eax
 2d02309:      	cmpl	0x38(%rdx), %eax
 2d0230c:      	jae	0x2d02330 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5120>
 2d0230e:      	cmpq	$0x9, %r12
 2d02312:      	jb	0x2d022d1 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50c1>
 2d02314:      	movq	%r15, %rdi
 2d02317:      	movq	%rbx, %rsi
 2d0231a:      	movq	%r12, %rdx
 2d0231d:      	callq	0x828ac50 <memmove@plt>
 2d02322:      	jmp	0x2d022e0 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d0>
 2d02324:      	nopw	%cs:(%rax,%rax)
 2d0232e:      	nop
 2d02330:      	movq	(%rcx), %rdx
 2d02333:      	movq	%rbp, %rcx
 2d02336:      	cmpl	0x38(%rdx), %eax
 2d02339:      	jae	0x2d022e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d3>
 2d0233b:      	movq	%r13, %rcx
 2d0233e:      	nop
 2d02340:      	movq	%rdx, (%rcx)
 2d02343:      	movq	-0x10(%rcx), %rdx
 2d02347:      	addq	$-0x8, %rcx
 2d0234b:      	cmpl	0x38(%rdx), %eax
 2d0234e:      	jb	0x2d02340 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5130>
 2d02350:      	jmp	0x2d022e3 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x50d3>
 2d02352:      	subq	$-0x80, %rbx
 2d02356:      	movq	0x18(%rsp), %rdi
 2d0235b:      	jmp	0x2d02370 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5160>
 2d0235d:      	nopl	(%rax)
 2d02360:      	movq	%rax, (%rsi)
 2d02363:      	addq	$0x8, %rbx
 2d02367:      	cmpq	%rdi, %rbx
 2d0236a:      	je	0x2cfe6c6 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x14b6>
 2d02370:      	movq	-0x8(%rbx), %rcx
 2d02374:      	movq	(%rbx), %rax
 2d02377:      	movl	0x38(%rax), %edx
 2d0237a:      	movq	%rbx, %rsi
 2d0237d:      	cmpl	0x38(%rcx), %edx
 2d02380:      	jae	0x2d02360 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5150>
 2d02382:      	movq	%rbx, %rsi
 2d02385:      	nopw	%cs:(%rax,%rax)
 2d0238f:      	nop
 2d02390:      	movq	%rcx, (%rsi)
 2d02393:      	movq	-0x10(%rsi), %rcx
 2d02397:      	addq	$-0x8, %rsi
 2d0239b:      	cmpl	0x38(%rcx), %edx
 2d0239e:      	jb	0x2d02390 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5180>
 2d023a0:      	jmp	0x2d02360 <_ZN12_GLOBAL__N_115ARMLoadStoreOpt21LoadStoreMultipleOptiERN4llvm17MachineBasicBlockE+0x5150>
