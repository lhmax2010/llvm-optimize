
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000038fb200 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE>:
 38fb200:      	pushq	%rbp
 38fb201:      	pushq	%r15
 38fb203:      	pushq	%r14
 38fb205:      	pushq	%r13
 38fb207:      	pushq	%r12
 38fb209:      	pushq	%rbx
 38fb20a:      	subq	$0x468, %rsp            # imm = 0x468
 38fb211:      	movq	0x10(%rdi), %rcx
 38fb215:      	xorl	%eax, %eax
 38fb217:      	cmpl	$0x0, 0x80(%rcx)
 38fb21e:      	je	0x38fe1c8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fc8>
 38fb224:      	cmpb	$0x0, 0x155(%rsi)
 38fb22b:      	jne	0x38fe1c8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fc8>
 38fb231:      	movq	(%rdi), %rax
 38fb234:      	movq	0x10(%rax), %rcx
 38fb238:      	subq	0x8(%rax), %rcx
 38fb23c:      	shrq	$0x3, %rcx
 38fb240:      	imull	$0xcccccccd, %ecx, %r15d # imm = 0xCCCCCCCD
 38fb247:      	subl	0x20(%rax), %r15d
 38fb24b:      	leaq	0x40(%rdi), %rax
 38fb24f:      	movq	%rax, 0x38(%rsp)
 38fb254:      	movslq	%r15d, %r14
 38fb257:      	movl	0x48(%rdi), %eax
 38fb25a:      	cmpq	%rax, %r14
 38fb25d:      	movq	%rdi, (%rsp)
 38fb261:      	movq	%rsi, 0x58(%rsp)
 38fb266:      	je	0x38fb4bb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bb>
 38fb26c:      	jae	0x38fb2b2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb2>
 38fb26e:      	movq	%rdi, %rbp
 38fb271:      	movq	0x38(%rsp), %rcx
 38fb276:      	movq	(%rcx), %rbx
 38fb279:      	leaq	-0x40(%rbx), %r12
 38fb27d:      	shlq	$0x4, %rax
 38fb281:      	leaq	(%rax,%rax,4), %r13
 38fb285:      	shlq	$0x4, %r14
 38fb289:      	leaq	(%r14,%r14,4), %r14
 38fb28d:      	jmp	0x38fb29d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9d>
 38fb28f:      	nop
 38fb290:      	addq	$-0x50, %r13
 38fb294:      	cmpq	%r13, %r14
 38fb297:      	je	0x38fb4b2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb29d:      	movq	-0x50(%rbx,%r13), %rdi
 38fb2a2:      	leaq	(%r12,%r13), %rax
 38fb2a6:      	cmpq	%rdi, %rax
 38fb2a9:      	je	0x38fb290 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x90>
 38fb2ab:      	callq	0x828a6d0 <free@plt>
 38fb2b0:      	jmp	0x38fb290 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x90>
 38fb2b2:      	movl	0x4c(%rdi), %ecx
 38fb2b5:      	cmpq	%rcx, %r14
 38fb2b8:      	jbe	0x38fb3cd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cd>
 38fb2be:      	leaq	0x50(%rdi), %r13
 38fb2c2:      	leaq	0x258(%rsp), %r8
 38fb2ca:      	movl	$0x50, %ecx
 38fb2cf:      	movq	%rdi, %rbx
 38fb2d2:      	movq	0x38(%rsp), %rdi
 38fb2d7:      	movq	%r13, %rsi
 38fb2da:      	movq	%r14, %rdx
 38fb2dd:      	callq	0x40f8560 <_ZN4llvm15SmallVectorBaseIjE13mallocForGrowEPvmmRm>
 38fb2e2:      	movq	%rax, %r12
 38fb2e5:      	movq	0x40(%rbx), %rbp
 38fb2e9:      	movl	0x48(%rbx), %eax
 38fb2ec:      	testq	%rax, %rax
 38fb2ef:      	je	0x38fb444 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x244>
 38fb2f5:      	movq	%r13, 0x18(%rsp)
 38fb2fa:      	shlq	$0x4, %rax
 38fb2fe:      	leaq	(%rax,%rax,4), %rbx
 38fb302:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb30c:      	movq	%r12, 0x8(%rsp)
 38fb311:      	jmp	0x38fb355 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x155>
 38fb313:      	nopw	%cs:(%rax,%rax)
 38fb31d:      	nopl	(%rax)
 38fb320:      	movq	%rsi, (%r12)
 38fb324:      	movl	%r13d, 0x8(%r12)
 38fb329:      	movl	0xc(%rbp), %eax
 38fb32c:      	movl	%eax, 0xc(%r12)
 38fb331:      	movq	%rcx, (%rbp)
 38fb335:      	movl	$0x0, 0xc(%rbp)
 38fb33c:      	movl	$0x0, 0x8(%rbp)
 38fb343:      	addq	$0x50, %rbp
 38fb347:      	addq	$0x50, %r12
 38fb34b:      	addq	$-0x50, %rbx
 38fb34f:      	je	0x38fb3e6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e6>
 38fb355:      	leaq	0x10(%r12), %rax
 38fb35a:      	movq	%rax, (%r12)
 38fb35e:      	movq	%rdx, 0x8(%r12)
 38fb363:      	cmpq	%r12, %rbp
 38fb366:      	je	0x38fb343 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x143>
 38fb368:      	movl	0x8(%rbp), %r13d
 38fb36c:      	testl	%r13d, %r13d
 38fb36f:      	je	0x38fb343 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x143>
 38fb371:      	movq	(%rbp), %rsi
 38fb375:      	leaq	0x10(%rbp), %rcx
 38fb379:      	cmpq	%rsi, %rcx
 38fb37c:      	jne	0x38fb320 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x120>
 38fb37e:      	cmpl	$0x9, %r13d
 38fb382:      	jb	0x38fb3a8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a8>
 38fb384:      	movl	$0x8, %ecx
 38fb389:      	movq	%r12, %rdi
 38fb38c:      	movq	%rax, %rsi
 38fb38f:      	movq	%r13, %rdx
 38fb392:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fb397:      	movl	0x8(%rbp), %ecx
 38fb39a:      	testl	%ecx, %ecx
 38fb39c:      	je	0x38fb3b9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b9>
 38fb39e:      	movq	(%rbp), %rsi
 38fb3a2:      	movq	(%r12), %rax
 38fb3a6:      	jmp	0x38fb3ab <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ab>
 38fb3a8:      	movl	%r13d, %ecx
 38fb3ab:      	movl	%ecx, %edx
 38fb3ad:      	shlq	$0x3, %rdx
 38fb3b1:      	movq	%rax, %rdi
 38fb3b4:      	callq	0x828ace0 <memcpy@plt>
 38fb3b9:      	movl	%r13d, 0x8(%r12)
 38fb3be:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb3c8:      	jmp	0x38fb33c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x13c>
 38fb3cd:      	movq	%rdi, %rbp
 38fb3d0:      	movq	0x38(%rsp), %rcx
 38fb3d5:      	movq	(%rcx), %r12
 38fb3d8:      	cmpq	%r14, %rax
 38fb3db:      	jne	0x38fb46f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26f>
 38fb3e1:      	jmp	0x38fb4b2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb3e6:      	movq	(%rsp), %rax
 38fb3ea:      	movq	0x40(%rax), %rbp
 38fb3ee:      	movl	0x48(%rax), %eax
 38fb3f1:      	testq	%rax, %rax
 38fb3f4:      	je	0x38fb43a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a>
 38fb3f6:      	shlq	$0x4, %rax
 38fb3fa:      	leaq	(%rax,%rax,4), %rbx
 38fb3fe:      	leaq	-0x40(%rbp), %r12
 38fb402:      	movq	0x18(%rsp), %r13
 38fb407:      	jmp	0x38fb416 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x216>
 38fb409:      	nopl	(%rax)
 38fb410:      	addq	$-0x50, %rbx
 38fb414:      	je	0x38fb42b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22b>
 38fb416:      	movq	-0x50(%rbp,%rbx), %rdi
 38fb41b:      	leaq	(%r12,%rbx), %rax
 38fb41f:      	cmpq	%rdi, %rax
 38fb422:      	je	0x38fb410 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x210>
 38fb424:      	callq	0x828a6d0 <free@plt>
 38fb429:      	jmp	0x38fb410 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x210>
 38fb42b:      	movq	0x38(%rsp), %rax
 38fb430:      	movq	(%rax), %rbp
 38fb433:      	movq	0x8(%rsp), %r12
 38fb438:      	jmp	0x38fb444 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x244>
 38fb43a:      	movq	0x8(%rsp), %r12
 38fb43f:      	movq	0x18(%rsp), %r13
 38fb444:      	movq	0x258(%rsp), %rbx
 38fb44c:      	cmpq	%r13, %rbp
 38fb44f:      	je	0x38fb459 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x259>
 38fb451:      	movq	%rbp, %rdi
 38fb454:      	callq	0x828a6d0 <free@plt>
 38fb459:      	movq	(%rsp), %rax
 38fb45d:      	movq	%r12, 0x40(%rax)
 38fb461:      	movl	%ebx, 0x4c(%rax)
 38fb464:      	movq	%rax, %rbp
 38fb467:      	movl	0x48(%rax), %eax
 38fb46a:      	cmpq	%r14, %rax
 38fb46d:      	je	0x38fb4b2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb46f:      	shlq	$0x4, %r14
 38fb473:      	leaq	(%r14,%r14,4), %rcx
 38fb477:      	shlq	$0x4, %rax
 38fb47b:      	leaq	(%rax,%rax,4), %rax
 38fb47f:      	subq	%rax, %rcx
 38fb482:      	leaq	0x10(%r12,%rax), %rax
 38fb487:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb491:      	nopw	%cs:(%rax,%rax)
 38fb49b:      	nopl	(%rax,%rax)
 38fb4a0:      	movq	%rax, -0x10(%rax)
 38fb4a4:      	movq	%rdx, -0x8(%rax)
 38fb4a8:      	addq	$0x50, %rax
 38fb4ac:      	addq	$-0x50, %rcx
 38fb4b0:      	jne	0x38fb4a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a0>
 38fb4b2:      	movl	%r15d, 0x48(%rbp)
 38fb4b6:      	movq	0x58(%rsp), %rsi
 38fb4bb:      	leaq	0x140(%rsi), %rax
 38fb4c2:      	movq	0x148(%rsi), %rcx
 38fb4c9:      	movq	%rax, 0x88(%rsp)
 38fb4d1:      	cmpq	%rax, %rcx
 38fb4d4:      	je	0x38fb889 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x689>
 38fb4da:      	movss	-0x2cc51ea(%rip), %xmm3 # 0xc362f8 <.LCPI43_3>
 38fb4e2:      	movsd	-0x2ae64ea(%rip), %xmm4 # 0xe15000 <.LCPI84_0>
 38fb4ea:      	movapd	-0x2ae9792(%rip), %xmm5 # 0xe11d60 <.LCPI84_1>
 38fb4f2:      	jmp	0x38fb51d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x31d>
 38fb4f4:      	nopw	%cs:(%rax,%rax)
 38fb4fe:      	nop
 38fb500:      	movq	0x8(%rsp), %rcx
 38fb505:      	movq	0x8(%rcx), %rcx
 38fb509:      	movq	0x58(%rsp), %rax
 38fb50e:      	addq	$0x140, %rax            # imm = 0x140
 38fb514:      	cmpq	%rax, %rcx
 38fb517:      	je	0x38fb889 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x689>
 38fb51d:      	leaq	0x30(%rcx), %r13
 38fb521:      	movq	%rcx, 0x8(%rsp)
 38fb526:      	movq	0x38(%rcx), %rbp
 38fb52a:      	jmp	0x38fb534 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x334>
 38fb52c:      	nopl	(%rax)
 38fb530:      	movq	0x8(%rbp), %rbp
 38fb534:      	cmpq	%r13, %rbp
 38fb537:      	je	0x38fb500 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x300>
 38fb539:      	movzwl	0x28(%rbp), %eax
 38fb53d:      	movzbl	0x2a(%rbp), %r8d
 38fb542:      	shll	$0x10, %r8d
 38fb546:      	orl	%eax, %r8d
 38fb549:      	testl	%r8d, %r8d
 38fb54c:      	je	0x38fb780 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x580>
 38fb552:      	movq	0x20(%rbp), %r9
 38fb556:      	shll	$0x5, %r8d
 38fb55a:      	addq	%r9, %r8
 38fb55d:      	movq	(%rsp), %rax
 38fb561:      	movq	0x10(%rax), %r10
 38fb565:      	movq	0x18(%rax), %r11
 38fb569:      	leaq	0x78(%r10), %rbx
 38fb56d:      	jmp	0x38fb5bd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3bd>
 38fb56f:      	movq	0x8(%rax), %rax
 38fb573:      	movsd	0x10(%rax), %xmm1
 38fb578:      	unpcklps	%xmm4, %xmm1            # xmm1 = xmm1[0],xmm4[0],xmm1[1],xmm4[1]
 38fb57b:      	subpd	%xmm5, %xmm1
 38fb57f:      	movapd	%xmm1, %xmm2
 38fb583:      	unpckhpd	%xmm1, %xmm2            # xmm2 = xmm2[1],xmm1[1]
 38fb587:      	addsd	%xmm1, %xmm2
 38fb58b:      	divsd	%xmm2, %xmm0
 38fb58f:      	cvtsd2ss	%xmm0, %xmm0
 38fb593:      	addss	0x84(%r14), %xmm0
 38fb59c:      	movss	%xmm0, 0x84(%r14)
 38fb5a5:      	nopw	%cs:(%rax,%rax)
 38fb5af:      	nop
 38fb5b0:      	addq	$0x20, %r9
 38fb5b4:      	cmpq	%r8, %r9
 38fb5b7:      	je	0x38fb780 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x580>
 38fb5bd:      	cmpb	$0x5, (%r9)
 38fb5c1:      	jne	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb5c3:      	movslq	0x10(%r9), %rcx
 38fb5c7:      	testq	%rcx, %rcx
 38fb5ca:      	js	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb5cc:      	movq	0x80(%r10), %r12
 38fb5d3:      	testq	%r12, %r12
 38fb5d6:      	je	0x38fb64a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x44a>
 38fb5d8:      	movq	0x70(%r10), %r15
 38fb5dc:      	movq	%rcx, %rsi
 38fb5df:      	cmpq	%r15, %rcx
 38fb5e2:      	jb	0x38fb5ed <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3ed>
 38fb5e4:      	movl	%ecx, %eax
 38fb5e6:      	xorl	%edx, %edx
 38fb5e8:      	divl	%r15d
 38fb5eb:      	movl	%edx, %esi
 38fb5ed:      	movq	0x68(%r10), %rax
 38fb5f1:      	movq	(%rax,%rsi,8), %rax
 38fb5f5:      	testq	%rax, %rax
 38fb5f8:      	je	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb5fa:      	movq	(%rax), %r14
 38fb5fd:      	cmpl	0x8(%r14), %ecx
 38fb601:      	je	0x38fb6a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb607:      	jmp	0x38fb620 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x420>
 38fb609:      	nopl	(%rax)
 38fb610:      	movl	%edi, %eax
 38fb612:      	xorl	%edx, %edx
 38fb614:      	divl	%r15d
 38fb617:      	cmpq	%rsi, %rdx
 38fb61a:      	jne	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb61c:      	cmpl	%edi, %ecx
 38fb61e:      	je	0x38fb661 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x461>
 38fb620:      	movq	(%r14), %r14
 38fb623:      	testq	%r14, %r14
 38fb626:      	je	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb628:      	movslq	0x8(%r14), %rdi
 38fb62c:      	movq	%rdi, %rax
 38fb62f:      	orq	%r15, %rax
 38fb632:      	shrq	$0x20, %rax
 38fb636:      	je	0x38fb610 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x410>
 38fb638:      	movq	%rdi, %rax
 38fb63b:      	xorl	%edx, %edx
 38fb63d:      	divq	%r15
 38fb640:      	cmpq	%rsi, %rdx
 38fb643:      	je	0x38fb61c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x41c>
 38fb645:      	jmp	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb64a:      	movq	%rbx, %rax
 38fb64d:      	nopl	(%rax)
 38fb650:      	movq	(%rax), %rax
 38fb653:      	testq	%rax, %rax
 38fb656:      	je	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb65c:      	cmpl	0x8(%rax), %ecx
 38fb65f:      	jne	0x38fb650 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x450>
 38fb661:      	testq	%r12, %r12
 38fb664:      	je	0x38fb69b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x49b>
 38fb666:      	movq	0x68(%r10), %rsi
 38fb66a:      	movq	0x70(%r10), %rdi
 38fb66e:      	movq	%rcx, %rdx
 38fb671:      	cmpq	%rdi, %rcx
 38fb674:      	jb	0x38fb67c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x47c>
 38fb676:      	movl	%ecx, %eax
 38fb678:      	xorl	%edx, %edx
 38fb67a:      	divl	%edi
 38fb67c:      	movq	(%rsi,%rdx,8), %rax
 38fb680:      	movq	(%rax), %r14
 38fb683:      	cmpl	0x8(%r14), %ecx
 38fb687:      	je	0x38fb6a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb689:      	nopl	(%rax)
 38fb690:      	movq	(%r14), %r14
 38fb693:      	cmpl	0x8(%r14), %ecx
 38fb697:      	jne	0x38fb690 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x490>
 38fb699:      	jmp	0x38fb6a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb69b:      	movq	%rbx, %r14
 38fb69e:      	nop
 38fb6a0:      	movq	(%r14), %r14
 38fb6a3:      	cmpl	0x8(%r14), %ecx
 38fb6a7:      	jne	0x38fb6a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a0>
 38fb6a9:      	movl	0x44(%rbp), %eax
 38fb6ac:      	addl	$-0xe, %eax
 38fb6af:      	cmpw	$0x5, %ax
 38fb6b3:      	jb	0x38fb5b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb6b9:      	movq	(%r11), %rax
 38fb6bc:      	movapd	%xmm3, %xmm0
 38fb6c0:      	testq	%rax, %rax
 38fb6c3:      	je	0x38fb593 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x393>
 38fb6c9:      	movl	0xb0(%rax), %edx
 38fb6cf:      	xorpd	%xmm0, %xmm0
 38fb6d3:      	testl	%edx, %edx
 38fb6d5:      	je	0x38fb56f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb6db:      	movq	0x18(%rbp), %rdi
 38fb6df:      	movq	0xa0(%rax), %rcx
 38fb6e6:      	movl	%edi, %r15d
 38fb6e9:      	shrl	$0x4, %r15d
 38fb6ed:      	movl	%edi, %esi
 38fb6ef:      	shrl	$0x9, %esi
 38fb6f2:      	xorl	%r15d, %esi
 38fb6f5:      	decl	%edx
 38fb6f7:      	andl	%edx, %esi
 38fb6f9:      	movl	%esi, %r15d
 38fb6fc:      	shll	$0x4, %r15d
 38fb700:      	movq	(%rcx,%r15), %r12
 38fb704:      	cmpq	%r12, %rdi
 38fb707:      	jne	0x38fb745 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x545>
 38fb709:      	shlq	$0x4, %rsi
 38fb70d:      	movl	0x8(%rcx,%rsi), %ecx
 38fb711:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 38fb716:      	cmpq	%rdx, %rcx
 38fb719:      	je	0x38fb56f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb71f:      	movq	0x8(%rax), %rdx
 38fb723:      	leaq	(%rcx,%rcx,2), %rcx
 38fb727:      	movsd	0x10(%rdx,%rcx,8), %xmm1
 38fb72d:      	unpcklps	%xmm4, %xmm1            # xmm1 = xmm1[0],xmm4[0],xmm1[1],xmm4[1]
 38fb730:      	subpd	%xmm5, %xmm1
 38fb734:      	movapd	%xmm1, %xmm0
 38fb738:      	unpckhpd	%xmm1, %xmm0            # xmm0 = xmm0[1],xmm1[1]
 38fb73c:      	addsd	%xmm1, %xmm0
 38fb740:      	jmp	0x38fb56f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb745:      	movl	$0x1, %r15d
 38fb74b:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 38fb752:      	je	0x38fb56f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb758:      	addl	%r15d, %esi
 38fb75b:      	incl	%r15d
 38fb75e:      	andl	%edx, %esi
 38fb760:      	movq	%rsi, %r12
 38fb763:      	shlq	$0x4, %r12
 38fb767:      	movq	(%rcx,%r12), %r12
 38fb76b:      	cmpq	%r12, %rdi
 38fb76e:      	je	0x38fb709 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x509>
 38fb770:      	jmp	0x38fb74b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x54b>
 38fb772:      	nopw	%cs:(%rax,%rax)
 38fb77c:      	nopl	(%rax)
 38fb780:      	movq	0x30(%rbp), %rax
 38fb784:      	cmpq	$0x8, %rax
 38fb788:      	jb	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb78e:      	movl	%eax, %ecx
 38fb790:      	andl	$0x7, %ecx
 38fb793:      	cmpq	$0x3, %rcx
 38fb797:      	je	0x38fb7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5b0>
 38fb799:      	testq	%rcx, %rcx
 38fb79c:      	jne	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb7a2:      	leaq	0x30(%rbp), %r15
 38fb7a6:      	movq	%rax, 0x30(%rbp)
 38fb7aa:      	leaq	0x38(%rbp), %rbx
 38fb7ae:      	jmp	0x38fb7e9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e9>
 38fb7b0:      	andq	$-0x8, %rax
 38fb7b4:      	movslq	(%rax), %rcx
 38fb7b7:      	testq	%rcx, %rcx
 38fb7ba:      	je	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb7c0:      	leaq	0x10(%rax,%rcx,8), %rbx
 38fb7c5:      	addq	$0x10, %rax
 38fb7c9:      	movq	%rax, %r15
 38fb7cc:      	jmp	0x38fb7e9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e9>
 38fb7ce:      	movq	(%r14), %rax
 38fb7d1:      	movl	%edx, %ecx
 38fb7d3:      	movq	%r12, (%rax,%rcx,8)
 38fb7d7:      	incl	0x8(%r14)
 38fb7db:      	nopl	(%rax,%rax)
 38fb7e0:      	addq	$0x8, %r15
 38fb7e4:      	cmpq	%rbx, %r15
 38fb7e7:      	je	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb7e9:      	movq	(%r15), %r12
 38fb7ec:      	movq	(%r12), %rax
 38fb7f0:      	testb	$0x4, %al
 38fb7f2:      	je	0x38fb7e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb7f4:      	andq	$-0x8, %rax
 38fb7f8:      	je	0x38fb7e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb7fa:      	cmpl	$0x4, 0x8(%rax)
 38fb7fe:      	jne	0x38fb7e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb800:      	movslq	0x10(%rax), %rax
 38fb804:      	testq	%rax, %rax
 38fb807:      	js	0x38fb7e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb809:      	movq	0x38(%rsp), %rcx
 38fb80e:      	movq	(%rcx), %rcx
 38fb811:      	leaq	(%rax,%rax,4), %rax
 38fb815:      	shlq	$0x4, %rax
 38fb819:      	leaq	(%rcx,%rax), %r14
 38fb81d:      	movl	0x8(%rcx,%rax), %edx
 38fb821:      	cmpl	0xc(%rcx,%rax), %edx
 38fb825:      	jb	0x38fb7ce <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5ce>
 38fb827:      	incq	%rdx
 38fb82a:      	leaq	0x10(%r14), %rsi
 38fb82e:      	movl	$0x8, %ecx
 38fb833:      	movq	%r14, %rdi
 38fb836:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fb83b:      	movapd	-0x2ae9ae3(%rip), %xmm5 # 0xe11d60 <.LCPI84_1>
 38fb843:      	movsd	-0x2ae684b(%rip), %xmm4 # 0xe15000 <.LCPI84_0>
 38fb84b:      	movss	-0x2cc555b(%rip), %xmm3 # 0xc362f8 <.LCPI43_3>
 38fb853:      	movl	0x8(%r14), %edx
 38fb857:      	jmp	0x38fb7ce <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5ce>
 38fb85c:      	nopl	(%rax)
 38fb860:      	testb	$0x4, (%rbp)
 38fb864:      	jne	0x38fb530 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb86a:      	nopw	(%rax,%rax)
 38fb870:      	testb	$0x8, 0x2c(%rbp)
 38fb874:      	je	0x38fb530 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb87a:      	movq	0x8(%rbp), %rbp
 38fb87e:      	testb	$0x8, 0x2c(%rbp)
 38fb882:      	jne	0x38fb87a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x67a>
 38fb884:      	jmp	0x38fb530 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb889:      	movq	(%rsp), %r12
 38fb88d:      	movq	(%r12), %rax
 38fb891:      	movq	0x10(%rax), %rcx
 38fb895:      	subq	0x8(%rax), %rcx
 38fb899:      	shrq	$0x3, %rcx
 38fb89d:      	imull	$0xcccccccd, %ecx, %ecx # imm = 0xCCCCCCCD
 38fb8a3:      	subl	0x20(%rax), %ecx
 38fb8a6:      	movq	%rcx, 0x20(%rsp)
 38fb8ab:      	leaq	0x5c8(%r12), %rax
 38fb8b3:      	movq	%rax, 0x18(%rsp)
 38fb8b8:      	movl	0x5d0(%r12), %eax
 38fb8c0:      	testq	%rax, %rax
 38fb8c3:      	je	0x38fb913 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x713>
 38fb8c5:      	cmpl	$0x1, %eax
 38fb8c8:      	je	0x38fbab2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8b2>
 38fb8ce:      	leaq	0x5c8(%r12), %rcx
 38fb8d6:      	movq	(%rcx), %rbx
 38fb8d9:      	shlq	$0x3, %rax
 38fb8dd:      	leaq	(%rax,%rax,8), %r14
 38fb8e1:      	leaq	-0x38(%rbx), %r15
 38fb8e5:      	jmp	0x38fb8fe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6fe>
 38fb8e7:      	nopw	(%rax,%rax)
 38fb8f0:      	addq	$-0x48, %r14
 38fb8f4:      	cmpq	$0x48, %r14
 38fb8f8:      	je	0x38fbaa6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb8fe:      	movq	-0x48(%rbx,%r14), %rdi
 38fb903:      	leaq	(%r15,%r14), %rax
 38fb907:      	cmpq	%rdi, %rax
 38fb90a:      	je	0x38fb8f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6f0>
 38fb90c:      	callq	0x828a6d0 <free@plt>
 38fb911:      	jmp	0x38fb8f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6f0>
 38fb913:      	cmpl	$0x0, 0x5d4(%r12)
 38fb91c:      	je	0x38fb922 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x722>
 38fb91e:      	xorl	%eax, %eax
 38fb920:      	jmp	0x38fb946 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x746>
 38fb922:      	movl	$0x1, %esi
 38fb927:      	leaq	0x5c8(%r12), %rdi
 38fb92f:      	callq	0x38fec60 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fb934:      	movl	0x5d0(%r12), %eax
 38fb93c:      	cmpq	$0x1, %rax
 38fb940:      	je	0x38fbaa6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb946:      	leaq	0x5c8(%r12), %rcx
 38fb94e:      	movq	(%rcx), %rsi
 38fb951:      	leaq	(%rax,%rax,8), %rdi
 38fb955:      	shlq	$0x3, %rax
 38fb959:      	leaq	(%rax,%rax,8), %rcx
 38fb95d:      	negq	%rcx
 38fb960:      	movabsq	$-0x1c71c71c71c71c71, %rdx # imm = 0xE38E38E38E38E38F
 38fb96a:      	movq	%rcx, %rax
 38fb96d:      	mulq	%rdx
 38fb970:      	shrq	$0x6, %rdx
 38fb974:      	movl	%edx, %eax
 38fb976:      	notl	%eax
 38fb978:      	testb	$0x3, %al
 38fb97a:      	jne	0x38fb98e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x78e>
 38fb97c:      	leaq	(%rsi,%rdi,8), %rax
 38fb980:      	cmpq	$0xd8, %rcx
 38fb987:      	jae	0x38fb9e5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x7e5>
 38fb989:      	jmp	0x38fbaa6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb98e:      	incl	%edx
 38fb990:      	andl	$0x3, %edx
 38fb993:      	leaq	0x10(%rsi,%rdi,8), %rax
 38fb998:      	xorps	%xmm0, %xmm0
 38fb99b:      	movabsq	$0x600000000, %rdi      # imm = 0x600000000
 38fb9a5:      	nopw	%cs:(%rax,%rax)
 38fb9af:      	nop
 38fb9b0:      	movups	%xmm0, 0x20(%rax)
 38fb9b4:      	movups	%xmm0, 0x10(%rax)
 38fb9b8:      	movups	%xmm0, (%rax)
 38fb9bb:      	movq	$0x0, 0x30(%rax)
 38fb9c3:      	movq	%rax, -0x10(%rax)
 38fb9c7:      	movq	%rdi, -0x8(%rax)
 38fb9cb:      	addq	$0x48, %rax
 38fb9cf:      	decq	%rdx
 38fb9d2:      	jne	0x38fb9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x7b0>
 38fb9d4:      	addq	$-0x10, %rax
 38fb9d8:      	cmpq	$0xd8, %rcx
 38fb9df:      	jb	0x38fbaa6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb9e5:      	addq	$0x58, %rax
 38fb9e9:      	xorps	%xmm0, %xmm0
 38fb9ec:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 38fb9f6:      	nopw	%cs:(%rax,%rax)
 38fba00:      	leaq	-0x48(%rax), %rdx
 38fba04:      	movups	%xmm0, -0x28(%rax)
 38fba08:      	movups	%xmm0, -0x38(%rax)
 38fba0c:      	movups	%xmm0, -0x48(%rax)
 38fba10:      	movq	$0x0, -0x18(%rax)
 38fba18:      	movq	%rdx, -0x58(%rax)
 38fba1c:      	movq	%rcx, -0x50(%rax)
 38fba20:      	movups	%xmm0, (%rax)
 38fba23:      	movups	%xmm0, 0x10(%rax)
 38fba27:      	movups	%xmm0, 0x20(%rax)
 38fba2b:      	movq	$0x0, 0x30(%rax)
 38fba33:      	movq	%rax, -0x10(%rax)
 38fba37:      	movq	%rcx, -0x8(%rax)
 38fba3b:      	leaq	0x48(%rax), %rdx
 38fba3f:      	movups	%xmm0, 0x48(%rax)
 38fba43:      	movups	%xmm0, 0x58(%rax)
 38fba47:      	movups	%xmm0, 0x68(%rax)
 38fba4b:      	movq	$0x0, 0x78(%rax)
 38fba53:      	movq	%rdx, 0x38(%rax)
 38fba57:      	movq	%rcx, 0x40(%rax)
 38fba5b:      	leaq	0x80(%rax), %rdx
 38fba62:      	leaq	0x90(%rax), %rdi
 38fba69:      	movups	%xmm0, 0xb0(%rax)
 38fba70:      	movups	%xmm0, 0xa0(%rax)
 38fba77:      	movups	%xmm0, 0x90(%rax)
 38fba7e:      	movq	$0x0, 0xc0(%rax)
 38fba89:      	movq	%rdi, 0x80(%rax)
 38fba90:      	movq	%rcx, 0x88(%rax)
 38fba97:      	addq	$0x120, %rax            # imm = 0x120
 38fba9d:      	cmpq	%rsi, %rdx
 38fbaa0:      	jne	0x38fba00 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x800>
 38fbaa6:      	movl	$0x1, 0x5d0(%r12)
 38fbab2:      	leaq	0x680(%r12), %rax
 38fbaba:      	movq	%rax, 0x40(%rsp)
 38fbabf:      	movl	0x688(%r12), %eax
 38fbac7:      	testq	%rax, %rax
 38fbaca:      	je	0x38fbb13 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x913>
 38fbacc:      	cmpl	$0x1, %eax
 38fbacf:      	je	0x38fbcb2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xab2>
 38fbad5:      	leaq	0x680(%r12), %rcx
 38fbadd:      	movq	(%rcx), %rbx
 38fbae0:      	shlq	$0x3, %rax
 38fbae4:      	leaq	(%rax,%rax,8), %r14
 38fbae8:      	leaq	-0x38(%rbx), %r15
 38fbaec:      	jmp	0x38fbafe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8fe>
 38fbaee:      	nop
 38fbaf0:      	addq	$-0x48, %r14
 38fbaf4:      	cmpq	$0x48, %r14
 38fbaf8:      	je	0x38fbca6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbafe:      	movq	-0x48(%rbx,%r14), %rdi
 38fbb03:      	leaq	(%r15,%r14), %rax
 38fbb07:      	cmpq	%rdi, %rax
 38fbb0a:      	je	0x38fbaf0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8f0>
 38fbb0c:      	callq	0x828a6d0 <free@plt>
 38fbb11:      	jmp	0x38fbaf0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8f0>
 38fbb13:      	cmpl	$0x0, 0x68c(%r12)
 38fbb1c:      	je	0x38fbb22 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x922>
 38fbb1e:      	xorl	%eax, %eax
 38fbb20:      	jmp	0x38fbb46 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x946>
 38fbb22:      	movl	$0x1, %esi
 38fbb27:      	leaq	0x680(%r12), %rdi
 38fbb2f:      	callq	0x38fec60 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fbb34:      	movl	0x688(%r12), %eax
 38fbb3c:      	cmpq	$0x1, %rax
 38fbb40:      	je	0x38fbca6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbb46:      	leaq	0x680(%r12), %rcx
 38fbb4e:      	movq	(%rcx), %rsi
 38fbb51:      	leaq	(%rax,%rax,8), %rdi
 38fbb55:      	shlq	$0x3, %rax
 38fbb59:      	leaq	(%rax,%rax,8), %rcx
 38fbb5d:      	negq	%rcx
 38fbb60:      	movabsq	$-0x1c71c71c71c71c71, %rdx # imm = 0xE38E38E38E38E38F
 38fbb6a:      	movq	%rcx, %rax
 38fbb6d:      	mulq	%rdx
 38fbb70:      	shrq	$0x6, %rdx
 38fbb74:      	movl	%edx, %eax
 38fbb76:      	notl	%eax
 38fbb78:      	testb	$0x3, %al
 38fbb7a:      	jne	0x38fbb8e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x98e>
 38fbb7c:      	leaq	(%rsi,%rdi,8), %rax
 38fbb80:      	cmpq	$0xd8, %rcx
 38fbb87:      	jae	0x38fbbe5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9e5>
 38fbb89:      	jmp	0x38fbca6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbb8e:      	incl	%edx
 38fbb90:      	andl	$0x3, %edx
 38fbb93:      	leaq	0x10(%rsi,%rdi,8), %rax
 38fbb98:      	xorps	%xmm0, %xmm0
 38fbb9b:      	movabsq	$0x600000000, %rdi      # imm = 0x600000000
 38fbba5:      	nopw	%cs:(%rax,%rax)
 38fbbaf:      	nop
 38fbbb0:      	movups	%xmm0, 0x20(%rax)
 38fbbb4:      	movups	%xmm0, 0x10(%rax)
 38fbbb8:      	movups	%xmm0, (%rax)
 38fbbbb:      	movq	$0x0, 0x30(%rax)
 38fbbc3:      	movq	%rax, -0x10(%rax)
 38fbbc7:      	movq	%rdi, -0x8(%rax)
 38fbbcb:      	addq	$0x48, %rax
 38fbbcf:      	decq	%rdx
 38fbbd2:      	jne	0x38fbbb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9b0>
 38fbbd4:      	addq	$-0x10, %rax
 38fbbd8:      	cmpq	$0xd8, %rcx
 38fbbdf:      	jb	0x38fbca6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbbe5:      	addq	$0x58, %rax
 38fbbe9:      	xorps	%xmm0, %xmm0
 38fbbec:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 38fbbf6:      	nopw	%cs:(%rax,%rax)
 38fbc00:      	leaq	-0x48(%rax), %rdx
 38fbc04:      	movups	%xmm0, -0x28(%rax)
 38fbc08:      	movups	%xmm0, -0x38(%rax)
 38fbc0c:      	movups	%xmm0, -0x48(%rax)
 38fbc10:      	movq	$0x0, -0x18(%rax)
 38fbc18:      	movq	%rdx, -0x58(%rax)
 38fbc1c:      	movq	%rcx, -0x50(%rax)
 38fbc20:      	movups	%xmm0, (%rax)
 38fbc23:      	movups	%xmm0, 0x10(%rax)
 38fbc27:      	movups	%xmm0, 0x20(%rax)
 38fbc2b:      	movq	$0x0, 0x30(%rax)
 38fbc33:      	movq	%rax, -0x10(%rax)
 38fbc37:      	movq	%rcx, -0x8(%rax)
 38fbc3b:      	leaq	0x48(%rax), %rdx
 38fbc3f:      	movups	%xmm0, 0x48(%rax)
 38fbc43:      	movups	%xmm0, 0x58(%rax)
 38fbc47:      	movups	%xmm0, 0x68(%rax)
 38fbc4b:      	movq	$0x0, 0x78(%rax)
 38fbc53:      	movq	%rdx, 0x38(%rax)
 38fbc57:      	movq	%rcx, 0x40(%rax)
 38fbc5b:      	leaq	0x80(%rax), %rdx
 38fbc62:      	leaq	0x90(%rax), %rdi
 38fbc69:      	movups	%xmm0, 0xb0(%rax)
 38fbc70:      	movups	%xmm0, 0xa0(%rax)
 38fbc77:      	movups	%xmm0, 0x90(%rax)
 38fbc7e:      	movq	$0x0, 0xc0(%rax)
 38fbc89:      	movq	%rdi, 0x80(%rax)
 38fbc90:      	movq	%rcx, 0x88(%rax)
 38fbc97:      	addq	$0x120, %rax            # imm = 0x120
 38fbc9d:      	cmpq	%rsi, %rdx
 38fbca0:      	jne	0x38fbc00 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xa00>
 38fbca6:      	movl	$0x1, 0x688(%r12)
 38fbcb2:      	leaq	0x550(%r12), %r14
 38fbcba:      	movslq	0x20(%rsp), %rbx
 38fbcbf:      	movq	0x558(%r12), %rdi
 38fbcc7:      	cmpq	%rbx, %rdi
 38fbcca:      	je	0x38fbd12 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb12>
 38fbccc:      	ja	0x38fbd0a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb0a>
 38fbcce:      	cmpq	%rbx, 0x560(%r12)
 38fbcd6:      	jae	0x38fbcf8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaf8>
 38fbcd8:      	leaq	0x568(%r12), %rsi
 38fbce0:      	movl	$0x1, %ecx
 38fbce5:      	movq	%r14, %rdi
 38fbce8:      	movq	%rbx, %rdx
 38fbceb:      	callq	0x40f8910 <_ZN4llvm15SmallVectorBaseImE8grow_podEPvmm>
 38fbcf0:      	movq	0x558(%r12), %rdi
 38fbcf8:      	movq	%rbx, %rdx
 38fbcfb:      	subq	%rdi, %rdx
 38fbcfe:      	je	0x38fbd0a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb0a>
 38fbd00:      	addq	(%r14), %rdi
 38fbd03:      	xorl	%esi, %esi
 38fbd05:      	callq	0x828ac20 <memset@plt>
 38fbd0a:      	movq	%rbx, 0x558(%r12)
 38fbd12:      	leaq	0x578(%r12), %rax
 38fbd1a:      	movq	%rax, 0xb8(%rsp)
 38fbd22:      	movl	0x580(%r12), %edi
 38fbd2a:      	cmpq	%rdi, %rbx
 38fbd2d:      	je	0x38fbd92 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb92>
 38fbd2f:      	jb	0x38fbd85 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb85>
 38fbd31:      	movl	0x584(%r12), %eax
 38fbd39:      	cmpq	%rax, %rbx
 38fbd3c:      	jbe	0x38fbd63 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb63>
 38fbd3e:      	leaq	0x588(%r12), %rsi
 38fbd46:      	movl	$0x4, %ecx
 38fbd4b:      	leaq	0x578(%r12), %rdi
 38fbd53:      	movq	%rbx, %rdx
 38fbd56:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fbd5b:      	movl	0x580(%r12), %edi
 38fbd63:      	movq	%rbx, %rdx
 38fbd66:      	subq	%rdi, %rdx
 38fbd69:      	je	0x38fbd85 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb85>
 38fbd6b:      	shlq	$0x2, %rdi
 38fbd6f:      	leaq	0x578(%r12), %rax
 38fbd77:      	addq	(%rax), %rdi
 38fbd7a:      	shlq	$0x2, %rdx
 38fbd7e:      	xorl	%esi, %esi
 38fbd80:      	callq	0x828ac20 <memset@plt>
 38fbd85:      	movq	0x20(%rsp), %rax
 38fbd8a:      	movl	%eax, 0x580(%r12)
 38fbd92:      	movq	%rbx, 0x8(%rsp)
 38fbd97:      	movq	0x18(%rsp), %rax
 38fbd9c:      	movq	(%rax), %r13
 38fbd9f:      	movl	0x40(%r13), %ecx
 38fbda3:      	andq	$0x3f, %rcx
 38fbda7:      	je	0x38fbdc5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbc5>
 38fbda9:      	movq	$-0x1, %rax
 38fbdb0:      	shlq	%cl, %rax
 38fbdb3:      	notq	%rax
 38fbdb6:      	movq	(%r13), %rcx
 38fbdba:      	movl	0x8(%r13), %edi
 38fbdbe:      	andq	%rax, -0x8(%rcx,%rdi,8)
 38fbdc3:      	jmp	0x38fbdc9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbc9>
 38fbdc5:      	movl	0x8(%r13), %edi
 38fbdc9:      	movl	%edi, %ebx
 38fbdcb:      	movq	0x20(%rsp), %r15
 38fbdd0:      	movl	%r15d, 0x40(%r13)
 38fbdd4:      	leal	0x3f(%r15), %esi
 38fbdd8:      	shrl	$0x6, %esi
 38fbddb:      	cmpl	%edi, %esi
 38fbddd:      	movq	%rsi, 0x28(%rsp)
 38fbde2:      	movl	%r15d, %ebp
 38fbde5:      	je	0x38fbe25 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc25>
 38fbde7:      	movl	%esi, %eax
 38fbde9:      	jb	0x38fbe1f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc1f>
 38fbdeb:      	movq	%rsi, %r14
 38fbdee:      	subq	%rdi, %r14
 38fbdf1:      	movl	%r15d, %ebp
 38fbdf4:      	cmpl	0xc(%r13), %esi
 38fbdf8:      	ja	0x38fe288 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3088>
 38fbdfe:      	shlq	$0x3, %rdi
 38fbe02:      	addq	(%r13), %rdi
 38fbe06:      	leal	(,%r14,8), %edx
 38fbe0e:      	xorl	%esi, %esi
 38fbe10:      	callq	0x828ac20 <memset@plt>
 38fbe15:      	addl	%r14d, %ebx
 38fbe18:      	movl	%ebx, %eax
 38fbe1a:      	movq	0x28(%rsp), %rsi
 38fbe1f:      	movl	%eax, 0x8(%r13)
 38fbe23:      	movl	%eax, %ebx
 38fbe25:      	andl	$0x3f, %ebp
 38fbe28:      	je	0x38fbe44 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc44>
 38fbe2a:      	movq	$-0x1, %rax
 38fbe31:      	movl	%ebp, %ecx
 38fbe33:      	shlq	%cl, %rax
 38fbe36:      	notq	%rax
 38fbe39:      	movq	(%r13), %rcx
 38fbe3d:      	movl	%ebx, %edx
 38fbe3f:      	andq	%rax, -0x8(%rcx,%rdx,8)
 38fbe44:      	movq	0x40(%rsp), %rax
 38fbe49:      	movq	(%rax), %r13
 38fbe4c:      	movl	0x40(%r13), %ecx
 38fbe50:      	andq	$0x3f, %rcx
 38fbe54:      	je	0x38fbe72 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc72>
 38fbe56:      	movq	$-0x1, %rax
 38fbe5d:      	shlq	%cl, %rax
 38fbe60:      	notq	%rax
 38fbe63:      	movq	(%r13), %rcx
 38fbe67:      	movl	0x8(%r13), %edi
 38fbe6b:      	andq	%rax, -0x8(%rcx,%rdi,8)
 38fbe70:      	jmp	0x38fbe76 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc76>
 38fbe72:      	movl	0x8(%r13), %edi
 38fbe76:      	movl	%edi, %ebx
 38fbe78:      	movl	%r15d, 0x40(%r13)
 38fbe7c:      	movl	%esi, %eax
 38fbe7e:      	movl	%r15d, %ebp
 38fbe81:      	cmpl	%edi, %esi
 38fbe83:      	je	0x38fbebf <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcbf>
 38fbe85:      	movl	%r15d, %ebp
 38fbe88:      	movl	%esi, %eax
 38fbe8a:      	jb	0x38fbebb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcbb>
 38fbe8c:      	movq	%rsi, %r14
 38fbe8f:      	subq	%rdi, %r14
 38fbe92:      	movl	%r15d, %ebp
 38fbe95:      	cmpl	0xc(%r13), %esi
 38fbe99:      	ja	0x38fe2ad <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x30ad>
 38fbe9f:      	shlq	$0x3, %rdi
 38fbea3:      	addq	(%r13), %rdi
 38fbea7:      	leal	(,%r14,8), %edx
 38fbeaf:      	xorl	%esi, %esi
 38fbeb1:      	callq	0x828ac20 <memset@plt>
 38fbeb6:      	addl	%r14d, %ebx
 38fbeb9:      	movl	%ebx, %eax
 38fbebb:      	movl	%eax, 0x8(%r13)
 38fbebf:      	andl	$0x3f, %ebp
 38fbec2:      	je	0x38fbede <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcde>
 38fbec4:      	movq	$-0x1, %rdx
 38fbecb:      	movl	%ebp, %ecx
 38fbecd:      	shlq	%cl, %rdx
 38fbed0:      	notq	%rdx
 38fbed3:      	movq	(%r13), %rcx
 38fbed7:      	movl	%eax, %eax
 38fbed9:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fbede:      	movq	(%rsp), %rbp
 38fbee2:      	leaq	0x788(%rbp), %rax
 38fbee9:      	movq	%rax, 0x78(%rsp)
 38fbeee:      	movl	0x790(%rbp), %ecx
 38fbef4:      	movq	0x8(%rsp), %r13
 38fbef9:      	cmpq	%rcx, %r13
 38fbefc:      	je	0x38fc29d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x109d>
 38fbf02:      	jae	0x38fbfcb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xdcb>
 38fbf08:      	leaq	0x788(%rbp), %rax
 38fbf0f:      	movq	(%rax), %rbx
 38fbf12:      	imulq	$0xe8, %rcx, %r15
 38fbf19:      	imulq	$0xe8, %r13, %r12
 38fbf20:      	leaq	-0x3416f7(%rip), %r14   # 0x35ba830 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fbf27:      	jmp	0x38fbf4b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd4b>
 38fbf29:      	nopl	(%rax)
 38fbf30:      	movl	$0x0, 0xcc(%r13)
 38fbf3b:      	addq	$-0xe8, %r15
 38fbf42:      	cmpq	%r15, %r12
 38fbf45:      	je	0x38fc292 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fbf4b:      	movq	-0xe0(%rbx,%r15), %r13
 38fbf53:      	testq	%r13, %r13
 38fbf56:      	je	0x38fbf3b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd3b>
 38fbf58:      	cmpl	$0x0, 0xc8(%r13)
 38fbf60:      	je	0x38fbf30 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd30>
 38fbf62:      	leaq	0x8(%r13), %rdi
 38fbf66:      	movq	%r14, %rsi
 38fbf69:      	xorl	%edx, %edx
 38fbf6b:      	callq	0x35ba4f0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fbf70:      	xorps	%xmm0, %xmm0
 38fbf73:      	movups	%xmm0, 0xb8(%r13)
 38fbf7b:      	movups	%xmm0, 0xa8(%r13)
 38fbf83:      	movups	%xmm0, 0x98(%r13)
 38fbf8b:      	movups	%xmm0, 0x88(%r13)
 38fbf93:      	movl	$0x0, 0xc8(%r13)
 38fbf9e:      	movups	%xmm0, 0x18(%r13)
 38fbfa3:      	movups	%xmm0, 0x8(%r13)
 38fbfa8:      	movups	%xmm0, 0x38(%r13)
 38fbfad:      	movups	%xmm0, 0x28(%r13)
 38fbfb2:      	movups	%xmm0, 0x58(%r13)
 38fbfb7:      	movups	%xmm0, 0x48(%r13)
 38fbfbc:      	movups	%xmm0, 0x78(%r13)
 38fbfc1:      	movups	%xmm0, 0x68(%r13)
 38fbfc6:      	jmp	0x38fbf30 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd30>
 38fbfcb:      	movl	0x794(%rbp), %eax
 38fbfd1:      	cmpq	%rax, %r13
 38fbfd4:      	jbe	0x38fc1f8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xff8>
 38fbfda:      	leaq	0x798(%rbp), %r15
 38fbfe1:      	leaq	0x258(%rsp), %r8
 38fbfe9:      	movl	$0xe8, %ecx
 38fbfee:      	leaq	0x788(%rbp), %rdi
 38fbff5:      	movq	%r15, %rsi
 38fbff8:      	movq	%r13, %rdx
 38fbffb:      	callq	0x40f8560 <_ZN4llvm15SmallVectorBaseIjE13mallocForGrowEPvmmRm>
 38fc000:      	movq	%rax, %r14
 38fc003:      	movq	0x788(%rbp), %r12
 38fc00a:      	movl	0x790(%rbp), %eax
 38fc010:      	testq	%rax, %rax
 38fc013:      	je	0x38fc225 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1025>
 38fc019:      	movq	%r15, 0x48(%rsp)
 38fc01e:      	imulq	$0xe8, %rax, %rbx
 38fc025:      	leaq	-0xe8(%rbx), %r15
 38fc02c:      	movq	%r15, %rax
 38fc02f:      	shrq	$0x3, %rax
 38fc033:      	movabsq	$0x8d3dcb08d3dcb09, %rcx # imm = 0x8D3DCB08D3DCB09
 38fc03d:      	mulq	%rcx
 38fc040:      	movq	%r14, %r13
 38fc043:      	movq	%rdx, %r14
 38fc046:      	movl	%r14d, %eax
 38fc049:      	notl	%eax
 38fc04b:      	movq	%r13, 0x30(%rsp)
 38fc050:      	movq	%r12, %rbp
 38fc053:      	testb	$0x3, %al
 38fc055:      	je	0x38fc093 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xe93>
 38fc057:      	incl	%r14d
 38fc05a:      	andl	$0x3, %r14d
 38fc05e:      	movq	0x30(%rsp), %r13
 38fc063:      	movq	%r12, %rbp
 38fc066:      	nopw	%cs:(%rax,%rax)
 38fc070:      	movl	$0xe8, %edx
 38fc075:      	movq	%r13, %rdi
 38fc078:      	movq	%rbp, %rsi
 38fc07b:      	callq	0x828ace0 <memcpy@plt>
 38fc080:      	addq	$0xe8, %rbp
 38fc087:      	addq	$0xe8, %r13
 38fc08e:      	decq	%r14
 38fc091:      	jne	0x38fc070 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xe70>
 38fc093:      	cmpq	$0x2b8, %r15            # imm = 0x2B8
 38fc09a:      	jb	0x38fc126 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf26>
 38fc0a0:      	addq	%rbx, %r12
 38fc0a3:      	xorl	%ebx, %ebx
 38fc0a5:      	nopw	%cs:(%rax,%rax)
 38fc0af:      	nop
 38fc0b0:      	leaq	(%r13,%rbx), %rdi
 38fc0b5:      	leaq	(%rbp,%rbx), %rsi
 38fc0ba:      	movl	$0xe8, %edx
 38fc0bf:      	callq	0x828ace0 <memcpy@plt>
 38fc0c4:      	leaq	0xe8(%r13,%rbx), %rdi
 38fc0cc:      	leaq	0xe8(%rbp,%rbx), %rsi
 38fc0d4:      	movl	$0xe8, %edx
 38fc0d9:      	callq	0x828ace0 <memcpy@plt>
 38fc0de:      	leaq	0x1d0(%r13,%rbx), %rdi
 38fc0e6:      	leaq	0x1d0(%rbp,%rbx), %rsi
 38fc0ee:      	movl	$0xe8, %edx
 38fc0f3:      	callq	0x828ace0 <memcpy@plt>
 38fc0f8:      	leaq	0x2b8(%r13,%rbx), %rdi
 38fc100:      	leaq	0x2b8(%rbp,%rbx), %rsi
 38fc108:      	movl	$0xe8, %edx
 38fc10d:      	callq	0x828ace0 <memcpy@plt>
 38fc112:      	leaq	0x3a0(%rbp,%rbx), %rax
 38fc11a:      	addq	$0x3a0, %rbx            # imm = 0x3A0
 38fc121:      	cmpq	%r12, %rax
 38fc124:      	jne	0x38fc0b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xeb0>
 38fc126:      	movq	(%rsp), %rbp
 38fc12a:      	movq	0x788(%rbp), %r12
 38fc131:      	movl	0x790(%rbp), %eax
 38fc137:      	testq	%rax, %rax
 38fc13a:      	je	0x38fc216 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1016>
 38fc140:      	imulq	$0xe8, %rax, %rbx
 38fc147:      	leaq	-0x34191e(%rip), %r14   # 0x35ba830 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fc14e:      	movq	0x8(%rsp), %r13
 38fc153:      	jmp	0x38fc178 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf78>
 38fc155:      	nopw	%cs:(%rax,%rax)
 38fc15f:      	nop
 38fc160:      	movl	$0x0, 0xcc(%r15)
 38fc16b:      	addq	$-0xe8, %rbx
 38fc172:      	je	0x38fc20c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x100c>
 38fc178:      	movq	-0xe0(%r12,%rbx), %r15
 38fc180:      	testq	%r15, %r15
 38fc183:      	je	0x38fc16b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf6b>
 38fc185:      	cmpl	$0x0, 0xc8(%r15)
 38fc18d:      	je	0x38fc160 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf60>
 38fc18f:      	leaq	0x8(%r15), %rdi
 38fc193:      	movq	%r14, %rsi
 38fc196:      	xorl	%edx, %edx
 38fc198:      	callq	0x35ba4f0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fc19d:      	xorps	%xmm0, %xmm0
 38fc1a0:      	movups	%xmm0, 0xb8(%r15)
 38fc1a8:      	movups	%xmm0, 0xa8(%r15)
 38fc1b0:      	movups	%xmm0, 0x98(%r15)
 38fc1b8:      	movups	%xmm0, 0x88(%r15)
 38fc1c0:      	movl	$0x0, 0xc8(%r15)
 38fc1cb:      	movups	%xmm0, 0x18(%r15)
 38fc1d0:      	movups	%xmm0, 0x8(%r15)
 38fc1d5:      	movups	%xmm0, 0x38(%r15)
 38fc1da:      	movups	%xmm0, 0x28(%r15)
 38fc1df:      	movups	%xmm0, 0x58(%r15)
 38fc1e4:      	movups	%xmm0, 0x48(%r15)
 38fc1e9:      	movups	%xmm0, 0x78(%r15)
 38fc1ee:      	movups	%xmm0, 0x68(%r15)
 38fc1f3:      	jmp	0x38fc160 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf60>
 38fc1f8:      	leaq	0x788(%rbp), %rax
 38fc1ff:      	movq	(%rax), %r14
 38fc202:      	subq	%rcx, %r13
 38fc205:      	jne	0x38fc252 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1052>
 38fc207:      	jmp	0x38fc292 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fc20c:      	movq	0x78(%rsp), %rax
 38fc211:      	movq	(%rax), %r12
 38fc214:      	jmp	0x38fc21b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x101b>
 38fc216:      	movq	0x8(%rsp), %r13
 38fc21b:      	movq	0x30(%rsp), %r14
 38fc220:      	movq	0x48(%rsp), %r15
 38fc225:      	movq	0x258(%rsp), %rbx
 38fc22d:      	cmpq	%r15, %r12
 38fc230:      	je	0x38fc23a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x103a>
 38fc232:      	movq	%r12, %rdi
 38fc235:      	callq	0x828a6d0 <free@plt>
 38fc23a:      	movq	%r14, 0x788(%rbp)
 38fc241:      	movl	%ebx, 0x794(%rbp)
 38fc247:      	movl	0x790(%rbp), %ecx
 38fc24d:      	subq	%rcx, %r13
 38fc250:      	je	0x38fc292 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fc252:      	imulq	$0xe8, %r13, %rax
 38fc259:      	addq	$-0xe8, %rax
 38fc25f:      	shrq	$0x3, %rax
 38fc263:      	movabsq	$0x8d3dcb08d3dcb09, %rdx # imm = 0x8D3DCB08D3DCB09
 38fc26d:      	mulq	%rdx
 38fc270:      	imulq	$0xe8, %rcx, %rax
 38fc277:      	addq	%rax, %r14
 38fc27a:      	imulq	$0xe8, %rdx, %rdx
 38fc281:      	addq	$0xe8, %rdx
 38fc288:      	movq	%r14, %rdi
 38fc28b:      	xorl	%esi, %esi
 38fc28d:      	callq	0x828ac20 <memset@plt>
 38fc292:      	movq	0x20(%rsp), %rax
 38fc297:      	movl	%eax, 0x790(%rbp)
 38fc29d:      	leaq	0x268(%rsp), %rax
 38fc2a5:      	movq	%rax, 0x68(%rsp)
 38fc2aa:      	movq	%rax, 0x258(%rsp)
 38fc2b2:      	movabsq	$0x1000000000, %rax     # imm = 0x1000000000
 38fc2bc:      	movq	%rax, 0x260(%rsp)
 38fc2c4:      	movq	0x10(%rbp), %rcx
 38fc2c8:      	movl	0x80(%rcx), %edx
 38fc2ce:      	xorl	%eax, %eax
 38fc2d0:      	cmpq	$0x11, %rdx
 38fc2d4:      	jb	0x38fc2fb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x10fb>
 38fc2d6:      	leaq	0x258(%rsp), %rdi
 38fc2de:      	movl	$0x8, %ecx
 38fc2e3:      	leaq	0x268(%rsp), %rsi
 38fc2eb:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc2f0:      	movq	0x10(%rbp), %rcx
 38fc2f4:      	movl	0x260(%rsp), %eax
 38fc2fb:      	movq	0x78(%rcx), %rbx
 38fc2ff:      	testq	%rbx, %rbx
 38fc302:      	je	0x38fc368 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1168>
 38fc304:      	leaq	0x258(%rsp), %r14
 38fc30c:      	nopl	(%rax)
 38fc310:      	cmpl	0x264(%rsp), %eax
 38fc317:      	jae	0x38fc345 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1145>
 38fc319:      	leaq	0x8(%rbx), %rcx
 38fc31d:      	movq	0x258(%rsp), %rdx
 38fc325:      	movl	%eax, %eax
 38fc327:      	movq	%rcx, (%rdx,%rax,8)
 38fc32b:      	movl	0x260(%rsp), %eax
 38fc332:      	incl	%eax
 38fc334:      	movl	%eax, 0x260(%rsp)
 38fc33b:      	movq	(%rbx), %rbx
 38fc33e:      	testq	%rbx, %rbx
 38fc341:      	jne	0x38fc310 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1110>
 38fc343:      	jmp	0x38fc368 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1168>
 38fc345:      	movl	%eax, %edx
 38fc347:      	incq	%rdx
 38fc34a:      	movl	$0x8, %ecx
 38fc34f:      	movq	%r14, %rdi
 38fc352:      	leaq	0x268(%rsp), %rsi
 38fc35a:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc35f:      	movl	0x260(%rsp), %eax
 38fc366:      	jmp	0x38fc319 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1119>
 38fc368:      	testl	%eax, %eax
 38fc36a:      	je	0x38fc440 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fc370:      	movq	0x258(%rsp), %r12
 38fc378:      	movl	%eax, %ebx
 38fc37a:      	leaq	(%r12,%rbx,8), %r15
 38fc37e:      	bsrq	%rbx, %rdx
 38fc382:      	xorl	$0x3f, %edx
 38fc385:      	addl	%edx, %edx
 38fc387:      	xorq	$0x7e, %rdx
 38fc38b:      	movq	%r12, %rdi
 38fc38e:      	movq	%r15, %rsi
 38fc391:      	callq	0x38fed60 <_ZSt16__introsort_loopIPPSt4pairIKiN4llvm12LiveIntervalEElN9__gnu_cxx5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117StackSlotColoring15InitializeSlotsEvE3$_0EEEvT_SE_T0_T1_>
 38fc396:      	leaq	0x8(%r12), %rbp
 38fc39b:      	cmpl	$0x11, %ebx
 38fc39e:      	jb	0x38fc437 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1237>
 38fc3a4:      	movq	%r15, 0x8(%rsp)
 38fc3a9:      	movl	$0x8, %r14d
 38fc3af:      	movq	%rbp, %rbx
 38fc3b2:      	movq	%r12, %r15
 38fc3b5:      	jmp	0x38fc3ef <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11ef>
 38fc3b7:      	nopw	(%rax,%rax)
 38fc3c0:      	cmpq	$0x9, %r14
 38fc3c4:      	jb	0x38fc431 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1231>
 38fc3c6:      	movq	%rbp, %rdi
 38fc3c9:      	movq	%r12, %rsi
 38fc3cc:      	movq	%r14, %rdx
 38fc3cf:      	callq	0x828ac50 <memmove@plt>
 38fc3d4:      	movq	%r12, %rcx
 38fc3d7:      	movq	%r13, (%rcx)
 38fc3da:      	addq	$0x8, %r14
 38fc3de:      	addq	$0x8, %rbx
 38fc3e2:      	cmpq	$0x80, %r14
 38fc3e9:      	je	0x38fcc8e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a8e>
 38fc3ef:      	movq	%r15, %rcx
 38fc3f2:      	leaq	(%r12,%r14), %r15
 38fc3f6:      	movq	(%r12,%r14), %r13
 38fc3fa:      	movq	(%r12), %rdx
 38fc3fe:      	movl	(%r13), %eax
 38fc402:      	cmpl	(%rdx), %eax
 38fc404:      	jl	0x38fc3c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11c0>
 38fc406:      	movq	(%rcx), %rdx
 38fc409:      	movq	%r15, %rcx
 38fc40c:      	cmpl	(%rdx), %eax
 38fc40e:      	jge	0x38fc3d7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d7>
 38fc410:      	movq	%rbx, %rcx
 38fc413:      	nopw	%cs:(%rax,%rax)
 38fc41d:      	nopl	(%rax)
 38fc420:      	movq	%rdx, (%rcx)
 38fc423:      	movq	-0x10(%rcx), %rdx
 38fc427:      	addq	$-0x8, %rcx
 38fc42b:      	cmpl	(%rdx), %eax
 38fc42d:      	jl	0x38fc420 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1220>
 38fc42f:      	jmp	0x38fc3d7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d7>
 38fc431:      	movq	%rdx, 0x8(%rcx)
 38fc435:      	jmp	0x38fc3d4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d4>
 38fc437:      	cmpl	$0x1, %ebx
 38fc43a:      	jne	0x38fe1f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ff0>
 38fc440:      	movl	0x260(%rsp), %eax
 38fc447:      	testq	%rax, %rax
 38fc44a:      	movq	(%rsp), %rbp
 38fc44e:      	movq	0x20(%rsp), %r12
 38fc453:      	je	0x38fc986 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1786>
 38fc459:      	movq	0x258(%rsp), %rsi
 38fc461:      	leaq	(%rsi,%rax,8), %rax
 38fc465:      	movq	%rax, 0x70(%rsp)
 38fc46a:      	xorps	%xmm0, %xmm0
 38fc46d:      	jmp	0x38fc4b1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x12b1>
 38fc46f:      	nop
 38fc470:      	movq	0x18(%rsp), %rax
 38fc475:      	movq	(%rax), %rax
 38fc478:      	leaq	(%r14,%r14,8), %rdx
 38fc47c:      	movl	$0x1, %esi
 38fc481:      	movq	0x48(%rsp), %rcx
 38fc486:      	shlq	%cl, %rsi
 38fc489:      	movq	(%rax,%rdx,8), %rax
 38fc48d:      	movq	0x8(%rsp), %rcx
 38fc492:      	shrl	$0x6, %ecx
 38fc495:      	orq	%rsi, (%rax,%rcx,8)
 38fc499:      	movq	(%rsp), %rbp
 38fc49d:      	movq	0x30(%rsp), %rsi
 38fc4a2:      	addq	$0x8, %rsi
 38fc4a6:      	cmpq	0x70(%rsp), %rsi
 38fc4ab:      	je	0x38fc986 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1786>
 38fc4b1:      	movq	(%rsi), %r15
 38fc4b4:      	movl	0x78(%r15), %edi
 38fc4b8:      	leal	(,%rdi,4), %r8d
 38fc4c0:      	sarl	$0x2, %r8d
 38fc4c4:      	movq	(%rbp), %rbx
 38fc4c8:      	movl	0x20(%rbx), %eax
 38fc4cb:      	addl	%r8d, %eax
 38fc4ce:      	movq	0x8(%rbx), %rcx
 38fc4d2:      	leaq	(%rax,%rax,4), %rdx
 38fc4d6:      	cmpq	$-0x1, 0x8(%rcx,%rdx,8)
 38fc4dc:      	je	0x38fc4a2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x12a2>
 38fc4de:      	movq	%rdi, 0x48(%rsp)
 38fc4e3:      	addq	$0x8, %r15
 38fc4e7:      	movq	0x30(%rbp), %r14
 38fc4eb:      	cmpq	0x38(%rbp), %r14
 38fc4ef:      	movq	%rsi, 0x30(%rsp)
 38fc4f4:      	movq	%r8, 0x8(%rsp)
 38fc4f9:      	je	0x38fc510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1310>
 38fc4fb:      	movq	%r15, (%r14)
 38fc4fe:      	addq	$0x8, %r14
 38fc502:      	movq	%r14, 0x30(%rbp)
 38fc506:      	jmp	0x38fc5c8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x13c8>
 38fc50b:      	nopl	(%rax,%rax)
 38fc510:      	movq	0x28(%rbp), %r13
 38fc514:      	subq	%r13, %r14
 38fc517:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 38fc521:      	cmpq	%rax, %r14
 38fc524:      	je	0x38fe2d2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x30d2>
 38fc52a:      	movq	%r14, %rax
 38fc52d:      	sarq	$0x3, %rax
 38fc531:      	cmpq	$0x1, %rax
 38fc535:      	movq	%rax, %rcx
 38fc538:      	adcq	$0x0, %rcx
 38fc53c:      	leaq	(%rcx,%rax), %r12
 38fc540:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 38fc54a:      	cmpq	%rdx, %r12
 38fc54d:      	cmovaeq	%rdx, %r12
 38fc551:      	addq	%rax, %rcx
 38fc554:      	cmovbq	%rdx, %r12
 38fc558:      	leaq	(,%r12,8), %rdi
 38fc560:      	callq	0x828a6b0 <_Znwm@plt>
 38fc565:      	movq	%rax, %rbp
 38fc568:      	movq	%r15, (%rax,%r14)
 38fc56c:      	testq	%r14, %r14
 38fc56f:      	jle	0x38fc57f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x137f>
 38fc571:      	movq	%rbp, %rdi
 38fc574:      	movq	%r13, %rsi
 38fc577:      	movq	%r14, %rdx
 38fc57a:      	callq	0x828ace0 <memcpy@plt>
 38fc57f:      	testq	%r13, %r13
 38fc582:      	movq	(%rsp), %r15
 38fc586:      	je	0x38fc596 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1396>
 38fc588:      	movq	%r13, %rdi
 38fc58b:      	movq	%r14, %rsi
 38fc58e:      	callq	0x828a6f0 <_ZdlPvm@plt>
 38fc593:      	movq	(%r15), %rbx
 38fc596:      	addq	%rbp, %r14
 38fc599:      	addq	$0x8, %r14
 38fc59d:      	movq	%rbp, 0x28(%r15)
 38fc5a1:      	movq	%r14, 0x30(%r15)
 38fc5a5:      	leaq	(%rbp,%r12,8), %rax
 38fc5aa:      	movq	%rax, 0x38(%r15)
 38fc5ae:      	movq	0x8(%rbx), %rcx
 38fc5b2:      	movl	0x20(%rbx), %eax
 38fc5b5:      	movq	0x8(%rsp), %r8
 38fc5ba:      	addl	%r8d, %eax
 38fc5bd:      	movq	%r15, %rbp
 38fc5c0:      	movq	0x20(%rsp), %r12
 38fc5c5:      	xorps	%xmm0, %xmm0
 38fc5c8:      	leaq	(%rax,%rax,4), %rax
 38fc5cc:      	movzbl	0x10(%rcx,%rax,8), %eax
 38fc5d1:      	movslq	%r8d, %rcx
 38fc5d4:      	movq	0x550(%rbp), %rdx
 38fc5db:      	movb	%al, (%rdx,%rcx)
 38fc5de:      	movq	(%rbp), %rax
 38fc5e2:      	movl	0x20(%rax), %edx
 38fc5e5:      	addl	%r8d, %edx
 38fc5e8:      	movq	0x8(%rax), %rsi
 38fc5ec:      	leaq	(%rdx,%rdx,4), %rdx
 38fc5f0:      	movl	0x8(%rsi,%rdx,8), %edx
 38fc5f4:      	movq	0x578(%rbp), %rdi
 38fc5fb:      	movl	%edx, (%rdi,%rcx,4)
 38fc5fe:      	movl	0x20(%rax), %eax
 38fc601:      	addl	%r8d, %eax
 38fc604:      	leaq	(%rax,%rax,4), %rax
 38fc608:      	movzbl	0x15(%rsi,%rax,8), %r14d
 38fc60e:      	testq	%r14, %r14
 38fc611:      	je	0x38fc470 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc617:      	movq	(%rsp), %rbx
 38fc61b:      	movl	0x5d0(%rbx), %eax
 38fc621:      	cmpq	%r14, %rax
 38fc624:      	ja	0x38fc7bf <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15bf>
 38fc62a:      	leaq	0x1(%r14), %r13
 38fc62e:      	cmpl	%r14d, 0x5d4(%rbx)
 38fc635:      	ja	0x38fc64d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x144d>
 38fc637:      	movq	0x18(%rsp), %rdi
 38fc63c:      	movq	%r13, %rsi
 38fc63f:      	callq	0x38fec60 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fc644:      	xorps	%xmm0, %xmm0
 38fc647:      	movl	0x5d0(%rbx), %eax
 38fc64d:      	cmpl	%eax, %r13d
 38fc650:      	movabsq	$0x600000000, %rsi      # imm = 0x600000000
 38fc65a:      	je	0x38fc6b5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x14b5>
 38fc65c:      	movq	0x18(%rsp), %rcx
 38fc661:      	movq	(%rcx), %rdx
 38fc664:      	leal	(,%r14,8), %ecx
 38fc66c:      	leaq	(%rcx,%rcx,8), %rcx
 38fc670:      	shlq	$0x3, %rax
 38fc674:      	leaq	(%rax,%rax,8), %rax
 38fc678:      	subq	%rax, %rcx
 38fc67b:      	addq	$0x48, %rcx
 38fc67f:      	leaq	0x10(%rdx,%rax), %rax
 38fc684:      	nopw	%cs:(%rax,%rax)
 38fc68e:      	nop
 38fc690:      	movups	%xmm0, 0x20(%rax)
 38fc694:      	movups	%xmm0, 0x10(%rax)
 38fc698:      	movups	%xmm0, (%rax)
 38fc69b:      	movq	$0x0, 0x30(%rax)
 38fc6a3:      	movq	%rax, -0x10(%rax)
 38fc6a7:      	movq	%rsi, -0x8(%rax)
 38fc6ab:      	addq	$0x48, %rax
 38fc6af:      	addq	$-0x48, %rcx
 38fc6b3:      	jne	0x38fc690 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1490>
 38fc6b5:      	movl	%r13d, 0x5d0(%rbx)
 38fc6bc:      	movl	0x688(%rbx), %eax
 38fc6c2:      	cmpq	%rax, %r13
 38fc6c5:      	je	0x38fc7bf <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15bf>
 38fc6cb:      	cmpl	%eax, %r13d
 38fc6ce:      	jae	0x38fc725 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1525>
 38fc6d0:      	movq	0x40(%rsp), %rcx
 38fc6d5:      	movq	(%rcx), %rbx
 38fc6d8:      	leaq	-0x38(%rbx), %r15
 38fc6dc:      	shlq	$0x3, %rax
 38fc6e0:      	leaq	(%rax,%rax,8), %r12
 38fc6e4:      	leaq	(%r14,%r14,8), %rax
 38fc6e8:      	leaq	0x48(,%rax,8), %rbp
 38fc6f0:      	jmp	0x38fc70d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x150d>
 38fc6f2:      	nopw	%cs:(%rax,%rax)
 38fc6fc:      	nopl	(%rax)
 38fc700:      	addq	$-0x48, %r12
 38fc704:      	cmpq	%r12, %rbp
 38fc707:      	je	0x38fc7af <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15af>
 38fc70d:      	movq	-0x48(%rbx,%r12), %rdi
 38fc712:      	leaq	(%r15,%r12), %rax
 38fc716:      	cmpq	%rdi, %rax
 38fc719:      	je	0x38fc700 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1500>
 38fc71b:      	callq	0x828a6d0 <free@plt>
 38fc720:      	xorps	%xmm0, %xmm0
 38fc723:      	jmp	0x38fc700 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1500>
 38fc725:      	cmpl	%r14d, 0x68c(%rbx)
 38fc72c:      	ja	0x38fc744 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1544>
 38fc72e:      	movq	0x40(%rsp), %rdi
 38fc733:      	movq	%r13, %rsi
 38fc736:      	callq	0x38fec60 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fc73b:      	xorps	%xmm0, %xmm0
 38fc73e:      	movl	0x688(%rbx), %eax
 38fc744:      	cmpl	%eax, %r13d
 38fc747:      	je	0x38fc7af <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15af>
 38fc749:      	movq	0x40(%rsp), %rcx
 38fc74e:      	movq	(%rcx), %rdx
 38fc751:      	leal	(,%r14,8), %ecx
 38fc759:      	leaq	(%rcx,%rcx,8), %rcx
 38fc75d:      	shlq	$0x3, %rax
 38fc761:      	leaq	(%rax,%rax,8), %rax
 38fc765:      	subq	%rax, %rcx
 38fc768:      	addq	$0x48, %rcx
 38fc76c:      	leaq	0x10(%rdx,%rax), %rax
 38fc771:      	nopw	%cs:(%rax,%rax)
 38fc77b:      	nopl	(%rax,%rax)
 38fc780:      	movups	%xmm0, 0x20(%rax)
 38fc784:      	movups	%xmm0, 0x10(%rax)
 38fc788:      	movups	%xmm0, (%rax)
 38fc78b:      	movq	$0x0, 0x30(%rax)
 38fc793:      	movq	%rax, -0x10(%rax)
 38fc797:      	movabsq	$0x600000000, %rdx      # imm = 0x600000000
 38fc7a1:      	movq	%rdx, -0x8(%rax)
 38fc7a5:      	addq	$0x48, %rax
 38fc7a9:      	addq	$-0x48, %rcx
 38fc7ad:      	jne	0x38fc780 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1580>
 38fc7af:      	movq	(%rsp), %rax
 38fc7b3:      	movl	%r13d, 0x688(%rax)
 38fc7ba:      	movq	0x20(%rsp), %r12
 38fc7bf:      	movq	0x18(%rsp), %rax
 38fc7c4:      	movq	(%rax), %rax
 38fc7c7:      	leaq	(%r14,%r14,8), %rdi
 38fc7cb:      	leaq	(%rax,%rdi,8), %r13
 38fc7cf:      	movl	0x40(%rax,%rdi,8), %ecx
 38fc7d3:      	andq	$0x3f, %rcx
 38fc7d7:      	movq	0x28(%rsp), %rsi
 38fc7dc:      	je	0x38fc7fa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15fa>
 38fc7de:      	movq	$-0x1, %rax
 38fc7e5:      	shlq	%cl, %rax
 38fc7e8:      	notq	%rax
 38fc7eb:      	movq	(%r13), %rcx
 38fc7ef:      	movl	0x8(%r13), %ebx
 38fc7f3:      	andq	%rax, -0x8(%rcx,%rbx,8)
 38fc7f8:      	jmp	0x38fc7fe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15fe>
 38fc7fa:      	movl	0x8(%r13), %ebx
 38fc7fe:      	movl	%ebx, %r15d
 38fc801:      	movl	%r12d, 0x40(%r13)
 38fc805:      	movl	%esi, %eax
 38fc807:      	movl	%r12d, %ebp
 38fc80a:      	cmpl	%ebx, %esi
 38fc80c:      	je	0x38fc85d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x165d>
 38fc80e:      	movl	%r12d, %ebp
 38fc811:      	movl	%esi, %eax
 38fc813:      	jb	0x38fc859 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1659>
 38fc815:      	movl	%r12d, %ebp
 38fc818:      	movq	%rbx, %rdi
 38fc81b:      	cmpl	0xc(%r13), %esi
 38fc81f:      	ja	0x38fc930 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1730>
 38fc825:      	movq	%rsi, %r12
 38fc828:      	subq	%rbx, %r12
 38fc82b:      	shlq	$0x3, %rdi
 38fc82f:      	addq	(%r13), %rdi
 38fc833:      	leal	(,%r12,8), %edx
 38fc83b:      	xorl	%esi, %esi
 38fc83d:      	callq	0x828ac20 <memset@plt>
 38fc842:      	movq	0x28(%rsp), %rsi
 38fc847:      	addl	%r12d, %r15d
 38fc84a:      	movl	%r15d, %eax
 38fc84d:      	movq	0x20(%rsp), %r12
 38fc852:      	xorps	%xmm0, %xmm0
 38fc855:      	leaq	(%r14,%r14,8), %rdi
 38fc859:      	movl	%eax, 0x8(%r13)
 38fc85d:      	andl	$0x3f, %ebp
 38fc860:      	je	0x38fc87c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x167c>
 38fc862:      	movq	$-0x1, %rdx
 38fc869:      	movl	%ebp, %ecx
 38fc86b:      	shlq	%cl, %rdx
 38fc86e:      	notq	%rdx
 38fc871:      	movq	(%r13), %rcx
 38fc875:      	movl	%eax, %eax
 38fc877:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fc87c:      	movq	0x40(%rsp), %rax
 38fc881:      	movq	(%rax), %rax
 38fc884:      	leaq	(%rax,%rdi,8), %r13
 38fc888:      	movl	0x40(%rax,%rdi,8), %ecx
 38fc88c:      	andq	$0x3f, %rcx
 38fc890:      	je	0x38fc8ae <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16ae>
 38fc892:      	movq	$-0x1, %rax
 38fc899:      	shlq	%cl, %rax
 38fc89c:      	notq	%rax
 38fc89f:      	movq	(%r13), %rcx
 38fc8a3:      	movl	0x8(%r13), %ebx
 38fc8a7:      	andq	%rax, -0x8(%rcx,%rbx,8)
 38fc8ac:      	jmp	0x38fc8b2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16b2>
 38fc8ae:      	movl	0x8(%r13), %ebx
 38fc8b2:      	movl	%ebx, %r15d
 38fc8b5:      	movl	%r12d, 0x40(%r13)
 38fc8b9:      	movl	%esi, %eax
 38fc8bb:      	movl	%r12d, %ebp
 38fc8be:      	cmpl	%ebx, %esi
 38fc8c0:      	je	0x38fc908 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1708>
 38fc8c2:      	movl	%r12d, %ebp
 38fc8c5:      	movl	%esi, %eax
 38fc8c7:      	jb	0x38fc904 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1704>
 38fc8c9:      	movl	%r12d, %ebp
 38fc8cc:      	movq	%rbx, %rdi
 38fc8cf:      	cmpl	0xc(%r13), %esi
 38fc8d3:      	ja	0x38fc95b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x175b>
 38fc8d9:      	movq	%rsi, %r12
 38fc8dc:      	subq	%rbx, %r12
 38fc8df:      	shlq	$0x3, %rdi
 38fc8e3:      	addq	(%r13), %rdi
 38fc8e7:      	leal	(,%r12,8), %edx
 38fc8ef:      	xorl	%esi, %esi
 38fc8f1:      	callq	0x828ac20 <memset@plt>
 38fc8f6:      	addl	%r12d, %r15d
 38fc8f9:      	movl	%r15d, %eax
 38fc8fc:      	movq	0x20(%rsp), %r12
 38fc901:      	xorps	%xmm0, %xmm0
 38fc904:      	movl	%eax, 0x8(%r13)
 38fc908:      	andl	$0x3f, %ebp
 38fc90b:      	je	0x38fc470 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc911:      	movq	$-0x1, %rdx
 38fc918:      	movl	%ebp, %ecx
 38fc91a:      	shlq	%cl, %rdx
 38fc91d:      	notq	%rdx
 38fc920:      	movq	(%r13), %rcx
 38fc924:      	movl	%eax, %eax
 38fc926:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fc92b:      	jmp	0x38fc470 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc930:      	leaq	0x10(%r13), %rsi
 38fc934:      	movl	$0x8, %ecx
 38fc939:      	movq	%r13, %rdi
 38fc93c:      	movq	0x28(%rsp), %rdx
 38fc941:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc946:      	movq	0x28(%rsp), %rsi
 38fc94b:      	movl	0x8(%r13), %edi
 38fc94f:      	movl	0x40(%r13), %ebp
 38fc953:      	movl	%edi, %r15d
 38fc956:      	jmp	0x38fc825 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1625>
 38fc95b:      	leaq	0x10(%r13), %rsi
 38fc95f:      	movl	$0x8, %ecx
 38fc964:      	movq	%r13, %rdi
 38fc967:      	movq	0x28(%rsp), %rdx
 38fc96c:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc971:      	movq	0x28(%rsp), %rsi
 38fc976:      	movl	0x8(%r13), %edi
 38fc97a:      	movl	0x40(%r13), %ebp
 38fc97e:      	movl	%edi, %r15d
 38fc981:      	jmp	0x38fc8d9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16d9>
 38fc986:      	movq	0x28(%rbp), %rdi
 38fc98a:      	movq	0x30(%rbp), %rsi
 38fc98e:      	callq	0x38feb50 <_ZN4llvm11stable_sortIRSt6vectorIPNS_12LiveIntervalESaIS3_EEN12_GLOBAL__N_114IntervalSorterEEEvOT_T0_>
 38fc993:      	leaq	0x668(%rbp), %rax
 38fc99a:      	movq	%rax, 0x48(%rsp)
 38fc99f:      	movl	0x5d0(%rbp), %r14d
 38fc9a6:      	movl	0x670(%rbp), %eax
 38fc9ac:      	cmpl	%eax, %r14d
 38fc9af:      	je	0x38fca15 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1815>
 38fc9b1:      	jb	0x38fca07 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1807>
 38fc9b3:      	cmpl	0x674(%rbp), %r14d
 38fc9ba:      	jbe	0x38fc9dd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x17dd>
 38fc9bc:      	leaq	0x678(%rbp), %rsi
 38fc9c3:      	movl	$0x4, %ecx
 38fc9c8:      	leaq	0x668(%rbp), %rdi
 38fc9cf:      	movq	%r14, %rdx
 38fc9d2:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc9d7:      	movl	0x670(%rbp), %eax
 38fc9dd:      	cmpl	%eax, %r14d
 38fc9e0:      	je	0x38fca07 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1807>
 38fc9e2:      	movl	%eax, %eax
 38fc9e4:      	leaq	(,%rax,4), %rdi
 38fc9ec:      	leaq	0x668(%rbp), %rcx
 38fc9f3:      	addq	(%rcx), %rdi
 38fc9f6:      	movq	%r14, %rdx
 38fc9f9:      	subq	%rax, %rdx
 38fc9fc:      	shlq	$0x2, %rdx
 38fca00:      	xorl	%esi, %esi
 38fca02:      	callq	0x828ac20 <memset@plt>
 38fca07:      	movl	%r14d, 0x670(%rbp)
 38fca0e:      	movl	0x5d0(%rbp), %r14d
 38fca15:      	testl	%r14d, %r14d
 38fca18:      	je	0x38fcad9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18d9>
 38fca1e:      	movq	0x18(%rsp), %rax
 38fca23:      	movq	(%rax), %rax
 38fca26:      	leaq	0x668(%rbp), %rcx
 38fca2d:      	movq	(%rcx), %rdx
 38fca30:      	movl	%r14d, %esi
 38fca33:      	xorl	%edi, %edi
 38fca35:      	jmp	0x38fca58 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1858>
 38fca37:      	nopw	(%rax,%rax)
 38fca40:      	tzcntq	%r14, %r8
 38fca45:      	orl	%ecx, %r8d
 38fca48:      	movl	%r8d, (%rdx,%rdi,4)
 38fca4c:      	incq	%rdi
 38fca4f:      	cmpq	%rsi, %rdi
 38fca52:      	je	0x38fcad9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18d9>
 38fca58:      	leaq	(%rdi,%rdi,8), %r11
 38fca5c:      	movl	0x40(%rax,%r11,8), %ecx
 38fca61:      	movl	$0xffffffff, %r8d       # imm = 0xFFFFFFFF
 38fca67:      	testl	%ecx, %ecx
 38fca69:      	je	0x38fca48 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fca6b:      	decl	%ecx
 38fca6d:      	movl	%ecx, %r9d
 38fca70:      	notb	%cl
 38fca72:      	movq	$-0x1, %r10
 38fca79:      	shrq	%cl, %r10
 38fca7c:      	leaq	(%rax,%r11,8), %r11
 38fca80:      	shrl	$0x6, %r9d
 38fca84:      	xorl	%ecx, %ecx
 38fca86:      	movl	%r9d, %ebx
 38fca89:      	negl	%ebx
 38fca8b:      	movl	$0x0, %r14d
 38fca91:      	sbbq	%r14, %r14
 38fca94:      	movq	(%r11), %r11
 38fca97:      	orq	%r10, %r14
 38fca9a:      	andq	(%r11), %r14
 38fca9d:      	jne	0x38fca40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1840>
 38fca9f:      	testq	%r9, %r9
 38fcaa2:      	je	0x38fca48 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fcaa4:      	leaq	-0x1(%r9), %rbx
 38fcaa8:      	movl	$0x40, %ecx
 38fcaad:      	xorl	%r15d, %r15d
 38fcab0:      	cmpq	%r15, %rbx
 38fcab3:      	movq	$-0x1, %r14
 38fcaba:      	cmoveq	%r10, %r14
 38fcabe:      	andq	0x8(%r11,%r15,8), %r14
 38fcac3:      	jne	0x38fca40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1840>
 38fcac9:      	addl	$0x40, %ecx
 38fcacc:      	incq	%r15
 38fcacf:      	cmpq	%r15, %r9
 38fcad2:      	jne	0x38fcab0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18b0>
 38fcad4:      	jmp	0x38fca48 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fcad9:      	movq	0x258(%rsp), %rdi
 38fcae1:      	leaq	0x268(%rsp), %rax
 38fcae9:      	cmpq	%rax, %rdi
 38fcaec:      	je	0x38fcaf3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18f3>
 38fcaee:      	callq	0x828a6d0 <free@plt>
 38fcaf3:      	movq	(%rbp), %rcx
 38fcaf7:      	movq	0x10(%rcx), %rax
 38fcafb:      	subq	0x8(%rcx), %rax
 38fcaff:      	shrq	$0x3, %rax
 38fcb03:      	imull	$0xcccccccd, %eax, %eax # imm = 0xCCCCCCCD
 38fcb09:      	movl	0x20(%rcx), %ecx
 38fcb0c:      	movl	%eax, %r14d
 38fcb0f:      	subl	%ecx, %r14d
 38fcb12:      	leaq	0x218(%rsp), %rsi
 38fcb1a:      	movq	%rsi, 0x208(%rsp)
 38fcb22:      	movabsq	$0x1000000000, %rbx     # imm = 0x1000000000
 38fcb2c:      	movq	%rbx, 0x210(%rsp)
 38fcb34:      	cmpl	$0x11, %r14d
 38fcb38:      	jb	0x38fcc0e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a0e>
 38fcb3e:      	leaq	0x208(%rsp), %rdi
 38fcb46:      	movl	$0x4, %ecx
 38fcb4b:      	movq	%r14, %rdx
 38fcb4e:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcb53:      	movq	0x208(%rsp), %rdi
 38fcb5b:      	leaq	(,%r14,4), %r12
 38fcb63:      	movl	$0xff, %esi
 38fcb68:      	movq	%r12, %rdx
 38fcb6b:      	callq	0x828ac20 <memset@plt>
 38fcb70:      	movl	%r14d, 0x210(%rsp)
 38fcb78:      	leaq	0x180(%rsp), %rsi
 38fcb80:      	movq	%rsi, 0x170(%rsp)
 38fcb88:      	movq	%rbx, 0x178(%rsp)
 38fcb90:      	leaq	0x170(%rsp), %rdi
 38fcb98:      	movl	$0x4, %ecx
 38fcb9d:      	movq	%rsi, 0x60(%rsp)
 38fcba2:      	movq	%r14, %rdx
 38fcba5:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcbaa:      	movq	0x170(%rsp), %rdi
 38fcbb2:      	xorl	%esi, %esi
 38fcbb4:      	movq	%r12, %rdx
 38fcbb7:      	callq	0x828ac20 <memset@plt>
 38fcbbc:      	movl	%r14d, 0x178(%rsp)
 38fcbc4:      	leaq	0x268(%rsp), %rax
 38fcbcc:      	movq	%rax, 0x68(%rsp)
 38fcbd1:      	movq	%rax, 0x258(%rsp)
 38fcbd9:      	movq	%rbx, 0x260(%rsp)
 38fcbe1:      	leaq	0x258(%rsp), %rdi
 38fcbe9:      	movq	%r14, %rsi
 38fcbec:      	callq	0x36af6b0 <_ZN4llvm23SmallVectorTemplateBaseINS_11SmallVectorIiLj4EEELb0EE4growEm>
 38fcbf1:      	movl	0x260(%rsp), %ebx
 38fcbf8:      	cmpl	%ebx, %r14d
 38fcbfb:      	je	0x38fcd82 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b82>
 38fcc01:      	movq	0x258(%rsp), %rcx
 38fcc09:      	jmp	0x38fcd53 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b53>
 38fcc0e:      	cmpl	%ecx, %eax
 38fcc10:      	jne	0x38fcce1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ae1>
 38fcc16:      	movl	%r14d, 0x210(%rsp)
 38fcc1e:      	leaq	0x180(%rsp), %rax
 38fcc26:      	movq	%rax, 0x60(%rsp)
 38fcc2b:      	movq	%rax, 0x170(%rsp)
 38fcc33:      	movl	$0x10, 0x17c(%rsp)
 38fcc3e:      	movl	%r14d, 0x178(%rsp)
 38fcc46:      	leaq	0x268(%rsp), %rax
 38fcc4e:      	movq	%rax, 0x68(%rsp)
 38fcc53:      	movq	%rax, 0x258(%rsp)
 38fcc5b:      	movq	%rbx, 0x260(%rsp)
 38fcc63:      	leaq	0x1d0(%rsp), %rax
 38fcc6b:      	movq	%rax, 0x80(%rsp)
 38fcc73:      	movq	%rax, 0x1c0(%rsp)
 38fcc7b:      	movl	$0x6, 0x1cc(%rsp)
 38fcc86:      	xorl	%r12d, %r12d
 38fcc89:      	jmp	0x38fce0c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c0c>
 38fcc8e:      	subq	$-0x80, %r12
 38fcc92:      	movq	0x8(%rsp), %rdi
 38fcc97:      	jmp	0x38fccb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ab0>
 38fcc99:      	nopl	(%rax)
 38fcca0:      	movq	%rax, (%rsi)
 38fcca3:      	addq	$0x8, %r12
 38fcca7:      	cmpq	%rdi, %r12
 38fccaa:      	je	0x38fc440 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fccb0:      	movq	-0x8(%r12), %rcx
 38fccb5:      	movq	(%r12), %rax
 38fccb9:      	movl	(%rax), %edx
 38fccbb:      	movq	%r12, %rsi
 38fccbe:      	cmpl	(%rcx), %edx
 38fccc0:      	jge	0x38fcca0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1aa0>
 38fccc2:      	movq	%r12, %rsi
 38fccc5:      	nopw	%cs:(%rax,%rax)
 38fcccf:      	nop
 38fccd0:      	movq	%rcx, (%rsi)
 38fccd3:      	movq	-0x10(%rsi), %rcx
 38fccd7:      	addq	$-0x8, %rsi
 38fccdb:      	cmpl	(%rcx), %edx
 38fccdd:      	jl	0x38fccd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ad0>
 38fccdf:      	jmp	0x38fcca0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1aa0>
 38fcce1:      	leaq	0x180(%rsp), %r15
 38fcce9:      	leaq	(,%r14,4), %r12
 38fccf1:      	movq	%rsi, %rdi
 38fccf4:      	movl	$0xff, %esi
 38fccf9:      	movq	%rbx, %r13
 38fccfc:      	movq	%r12, %rdx
 38fccff:      	callq	0x828ac20 <memset@plt>
 38fcd04:      	movl	%r14d, 0x210(%rsp)
 38fcd0c:      	movq	%r15, 0x170(%rsp)
 38fcd14:      	movl	$0x10, 0x17c(%rsp)
 38fcd1f:      	xorl	%ebx, %ebx
 38fcd21:      	movq	%r15, 0x60(%rsp)
 38fcd26:      	movq	%r15, %rdi
 38fcd29:      	xorl	%esi, %esi
 38fcd2b:      	movq	%r12, %rdx
 38fcd2e:      	callq	0x828ac20 <memset@plt>
 38fcd33:      	movl	%r14d, 0x178(%rsp)
 38fcd3b:      	leaq	0x268(%rsp), %rcx
 38fcd43:      	movq	%rcx, 0x258(%rsp)
 38fcd4b:      	movq	%r13, 0x260(%rsp)
 38fcd53:      	movabsq	$0x400000000, %rdx      # imm = 0x400000000
 38fcd5d:      	movq	%r14, %rax
 38fcd60:      	shlq	$0x5, %rax
 38fcd64:      	shlq	$0x5, %rbx
 38fcd68:      	subq	%rbx, %rax
 38fcd6b:      	leaq	0x10(%rbx,%rcx), %rcx
 38fcd70:      	movq	%rcx, -0x10(%rcx)
 38fcd74:      	movq	%rdx, -0x8(%rcx)
 38fcd78:      	addq	$0x20, %rcx
 38fcd7c:      	addq	$-0x20, %rax
 38fcd80:      	jne	0x38fcd70 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b70>
 38fcd82:      	movl	%r14d, 0x260(%rsp)
 38fcd8a:      	leal	0x3f(%r14), %eax
 38fcd8e:      	movl	%eax, %r12d
 38fcd91:      	shrl	$0x6, %r12d
 38fcd95:      	leaq	0x1d0(%rsp), %rsi
 38fcd9d:      	movq	%rsi, 0x1c0(%rsp)
 38fcda5:      	movl	$0x6, 0x1cc(%rsp)
 38fcdb0:      	cmpl	$0x1c0, %eax            # imm = 0x1C0
 38fcdb5:      	movq	%rsi, 0x80(%rsp)
 38fcdbd:      	jb	0x38fcdf1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1bf1>
 38fcdbf:      	movl	$0x0, 0x1c8(%rsp)
 38fcdca:      	leaq	0x1c0(%rsp), %rdi
 38fcdd2:      	movl	$0x8, %ecx
 38fcdd7:      	movq	%r12, %rdx
 38fcdda:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcddf:      	movq	0x1c0(%rsp), %rdi
 38fcde7:      	leal	(,%r12,8), %edx
 38fcdef:      	jmp	0x38fce05 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c05>
 38fcdf1:      	testl	%r12d, %r12d
 38fcdf4:      	je	0x38fe280 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3080>
 38fcdfa:      	leal	(,%r12,8), %edx
 38fce02:      	movq	%rsi, %rdi
 38fce05:      	xorl	%esi, %esi
 38fce07:      	callq	0x828ac20 <memset@plt>
 38fce0c:      	movl	%r12d, 0x1c8(%rsp)
 38fce14:      	movl	%r14d, 0x200(%rsp)
 38fce1c:      	movq	0x28(%rbp), %r14
 38fce20:      	movq	0x30(%rbp), %rsi
 38fce24:      	cmpq	%rsi, %r14
 38fce27:      	je	0x38fd51c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x231c>
 38fce2d:      	leaq	0x720(%rbp), %rax
 38fce34:      	movq	%rax, 0xb0(%rsp)
 38fce3c:      	xorl	%ebx, %ebx
 38fce3e:      	movq	%rsi, 0x70(%rsp)
 38fce43:      	nopw	%cs:(%rax,%rax)
 38fce4d:      	nopl	(%rax)
 38fce50:      	movq	%rbx, 0x30(%rsp)
 38fce55:      	movq	(%r14), %rax
 38fce58:      	movq	%rax, 0x8(%rsp)
 38fce5d:      	movl	0x70(%rax), %r15d
 38fce61:      	shll	$0x2, %r15d
 38fce65:      	sarl	$0x2, %r15d
 38fce69:      	movq	(%rbp), %rax
 38fce6d:      	movl	0x20(%rax), %ecx
 38fce70:      	addl	%r15d, %ecx
 38fce73:      	movq	0x8(%rax), %rax
 38fce77:      	leaq	(%rcx,%rcx,4), %rcx
 38fce7b:      	movzbl	0x15(%rax,%rcx,8), %ebx
 38fce80:      	movq	0x680(%rbp), %rdx
 38fce87:      	cmpb	$0x0, 0x4cb2b7a(%rip)   # 0x85afa08 <_ZL14DisableSharing+0x78>
 38fce8e:      	jne	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fce94:      	leaq	(%rbx,%rbx,8), %r11
 38fce98:      	movl	0x40(%rdx,%r11,8), %ecx
 38fce9d:      	testl	%ecx, %ecx
 38fce9f:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcea5:      	decl	%ecx
 38fcea7:      	movl	%ecx, %eax
 38fcea9:      	notb	%cl
 38fceab:      	movq	$-0x1, %rsi
 38fceb2:      	shrq	%cl, %rsi
 38fceb5:      	leaq	(%rdx,%r11,8), %rdi
 38fceb9:      	shrl	$0x6, %eax
 38fcebc:      	xorl	%ecx, %ecx
 38fcebe:      	movl	%eax, %r8d
 38fcec1:      	negl	%r8d
 38fcec4:      	movl	$0x0, %r9d
 38fceca:      	sbbq	%r9, %r9
 38fcecd:      	movq	(%rdi), %rdi
 38fced0:      	orq	%rsi, %r9
 38fced3:      	andq	(%rdi), %r9
 38fced6:      	je	0x38fcef6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cf6>
 38fced8:      	tzcntq	%r9, %r12
 38fcedd:      	orl	%ecx, %r12d
 38fcee0:      	cmpl	$-0x1, %r12d
 38fcee4:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fceea:      	movq	%rbx, 0x28(%rsp)
 38fceef:      	movq	%r11, 0x20(%rsp)
 38fcef4:      	jmp	0x38fcf4e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d4e>
 38fcef6:      	testq	%rax, %rax
 38fcef9:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fceff:      	leaq	-0x1(%rax), %r8
 38fcf03:      	movl	$0x40, %ecx
 38fcf08:      	xorl	%r10d, %r10d
 38fcf0b:      	nopl	(%rax,%rax)
 38fcf10:      	cmpq	%r10, %r8
 38fcf13:      	movq	$-0x1, %r9
 38fcf1a:      	cmoveq	%rsi, %r9
 38fcf1e:      	andq	0x8(%rdi,%r10,8), %r9
 38fcf23:      	jne	0x38fced8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cd8>
 38fcf25:      	addl	$0x40, %ecx
 38fcf28:      	incq	%r10
 38fcf2b:      	cmpq	%r10, %rax
 38fcf2e:      	jne	0x38fcf10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d10>
 38fcf30:      	jmp	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcf35:      	incl	%eax
 38fcf37:      	movl	%eax, %edi
 38fcf39:      	tzcntq	%rcx, %r12
 38fcf3e:      	shll	$0x6, %edi
 38fcf41:      	orl	%edi, %r12d
 38fcf44:      	cmpl	$-0x1, %r12d
 38fcf48:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcf4e:      	movslq	%r12d, %r13
 38fcf51:      	movq	0x78(%rsp), %rax
 38fcf56:      	movq	(%rax), %rax
 38fcf59:      	imulq	$0xe8, %r13, %rcx
 38fcf60:      	movq	0x8(%rax,%rcx), %rdx
 38fcf65:      	testq	%rdx, %rdx
 38fcf68:      	je	0x38fd040 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e40>
 38fcf6e:      	movq	%rdx, 0xc0(%rsp)
 38fcf76:      	movq	0x8(%rsp), %rax
 38fcf7b:      	movq	%rax, 0xc8(%rsp)
 38fcf83:      	movq	$0x0, 0xd8(%rsp)
 38fcf8f:      	leaq	0xf0(%rsp), %rax
 38fcf97:      	movq	%rax, 0xe0(%rsp)
 38fcf9f:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 38fcfa9:      	movq	%rax, 0xe8(%rsp)
 38fcfb1:      	leaq	0x140(%rsp), %rbx
 38fcfb9:      	movq	%rbx, 0x130(%rsp)
 38fcfc1:      	movq	%rax, 0x138(%rsp)
 38fcfc9:      	movw	$0x0, 0x160(%rsp)
 38fcfd3:      	movq	$0x0, 0x164(%rsp)
 38fcfdf:      	leaq	0xc0(%rsp), %rdi
 38fcfe7:      	movl	$0x1, %esi
 38fcfec:      	callq	0x35bba30 <_ZN4llvm17LiveIntervalUnion5Query23collectInterferingVRegsEj>
 38fcff1:      	movl	%eax, %ebp
 38fcff3:      	movq	0x130(%rsp), %rdi
 38fcffb:      	cmpq	%rbx, %rdi
 38fcffe:      	je	0x38fd005 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e05>
 38fd000:      	callq	0x828a6d0 <free@plt>
 38fd005:      	movq	0xe0(%rsp), %rdi
 38fd00d:      	leaq	0xf0(%rsp), %rax
 38fd015:      	cmpq	%rax, %rdi
 38fd018:      	je	0x38fd01f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e1f>
 38fd01a:      	callq	0x828a6d0 <free@plt>
 38fd01f:      	testl	%ebp, %ebp
 38fd021:      	movq	(%rsp), %rbp
 38fd025:      	movq	0x28(%rsp), %rbx
 38fd02a:      	jne	0x38fd071 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e71>
 38fd02c:      	jmp	0x38fd4a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fd031:      	nopw	%cs:(%rax,%rax)
 38fd03b:      	nopl	(%rax,%rax)
 38fd040:      	movq	(%rax,%rcx), %rdi
 38fd044:      	testq	%rdi, %rdi
 38fd047:      	je	0x38fd4a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fd04d:      	movq	0x8(%rsp), %rax
 38fd052:      	cmpl	$0x0, 0x8(%rax)
 38fd056:      	je	0x38fd4a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fd05c:      	movq	0x8(%rsp), %rsi
 38fd061:      	movq	(%rsi), %rdx
 38fd064:      	callq	0x35aa8f0 <_ZNK4llvm9LiveRange12overlapsFromERKS0_PKNS0_7SegmentE>
 38fd069:      	testb	%al, %al
 38fd06b:      	je	0x38fd4a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fd071:      	movq	0x40(%rsp), %rax
 38fd076:      	movq	(%rax), %rdx
 38fd079:      	incl	%r12d
 38fd07c:      	movq	0x20(%rsp), %r11
 38fd081:      	movl	0x40(%rdx,%r11,8), %eax
 38fd086:      	cmpl	%eax, %r12d
 38fd089:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd08f:      	movl	%r12d, %edi
 38fd092:      	shrl	$0x6, %edi
 38fd095:      	decl	%eax
 38fd097:      	movl	%eax, %r8d
 38fd09a:      	shrl	$0x6, %r8d
 38fd09e:      	cmpl	%r8d, %edi
 38fd0a1:      	ja	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd0a7:      	leaq	(%rdx,%r11,8), %rcx
 38fd0ab:      	movq	(%rcx), %rsi
 38fd0ae:      	andl	$0x3f, %r12d
 38fd0b2:      	movl	%r12d, %ecx
 38fd0b5:      	negb	%cl
 38fd0b7:      	movq	$-0x1, %r9
 38fd0be:      	shrq	%cl, %r9
 38fd0c1:      	cmpl	$0x1, %r12d
 38fd0c5:      	movl	$0x0, %r10d
 38fd0cb:      	sbbq	%r10, %r10
 38fd0ce:      	notq	%r9
 38fd0d1:      	orq	%r9, %r10
 38fd0d4:      	notb	%al
 38fd0d6:      	movq	$-0x1, %r9
 38fd0dd:      	movl	%eax, %ecx
 38fd0df:      	shrq	%cl, %r9
 38fd0e2:      	cmpl	%r8d, %edi
 38fd0e5:      	movq	$-0x1, %rcx
 38fd0ec:      	cmoveq	%r9, %rcx
 38fd0f0:      	movl	%edi, %eax
 38fd0f2:      	andq	%r10, %rcx
 38fd0f5:      	andq	(%rsi,%rax,8), %rcx
 38fd0f9:      	jne	0x38fcf39 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d39>
 38fd0ff:      	leal	0x1(%r8), %ecx
 38fd103:      	leal	0x1(%rax), %edi
 38fd106:      	cmpl	%ecx, %edi
 38fd108:      	je	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd10a:      	movl	%r8d, %edi
 38fd10d:      	leaq	-0x1(%rdi), %r8
 38fd111:      	nopw	%cs:(%rax,%rax)
 38fd11b:      	nopl	(%rax,%rax)
 38fd120:      	cmpq	%rax, %r8
 38fd123:      	movq	$-0x1, %rcx
 38fd12a:      	cmoveq	%r9, %rcx
 38fd12e:      	andq	0x8(%rsi,%rax,8), %rcx
 38fd133:      	jne	0x38fcf35 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d35>
 38fd139:      	incq	%rax
 38fd13c:      	cmpq	%rax, %rdi
 38fd13f:      	jne	0x38fd120 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f20>
 38fd141:      	nopw	%cs:(%rax,%rax)
 38fd14b:      	nopl	(%rax,%rax)
 38fd150:      	movq	0x48(%rsp), %rax
 38fd155:      	movq	(%rax), %rsi
 38fd158:      	movl	(%rsi,%rbx,4), %r12d
 38fd15c:      	leal	(,%rbx,8), %eax
 38fd163:      	movl	$0x1, %edi
 38fd168:      	movl	%r12d, %ecx
 38fd16b:      	shlq	%cl, %rdi
 38fd16e:      	leaq	(%rax,%rax,8), %rcx
 38fd172:      	movq	(%rdx,%rcx), %rax
 38fd176:      	movl	%r12d, %edx
 38fd179:      	shrl	$0x6, %edx
 38fd17c:      	orq	%rdi, (%rax,%rdx,8)
 38fd180:      	movq	0x18(%rsp), %rax
 38fd185:      	movq	(%rax), %rdi
 38fd188:      	leal	0x1(%r12), %r10d
 38fd18d:      	movl	0x40(%rdi,%rcx), %eax
 38fd191:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 38fd196:      	cmpl	%eax, %r10d
 38fd199:      	je	0x38fd270 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd19f:      	movl	%r10d, %r8d
 38fd1a2:      	shrl	$0x6, %r8d
 38fd1a6:      	decl	%eax
 38fd1a8:      	movl	%eax, %r9d
 38fd1ab:      	shrl	$0x6, %r9d
 38fd1af:      	cmpl	%r9d, %r8d
 38fd1b2:      	ja	0x38fd270 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd1b8:      	addq	%rcx, %rdi
 38fd1bb:      	movq	(%rdi), %rdi
 38fd1be:      	andl	$0x3f, %r10d
 38fd1c2:      	movl	%r10d, %ecx
 38fd1c5:      	negb	%cl
 38fd1c7:      	movq	$-0x1, %r11
 38fd1ce:      	shrq	%cl, %r11
 38fd1d1:      	cmpl	$0x1, %r10d
 38fd1d5:      	movq	%rbx, %r13
 38fd1d8:      	movl	$0x0, %ebx
 38fd1dd:      	sbbq	%rbx, %rbx
 38fd1e0:      	notq	%r11
 38fd1e3:      	orq	%r11, %rbx
 38fd1e6:      	notb	%al
 38fd1e8:      	movq	$-0x1, %r10
 38fd1ef:      	movl	%eax, %ecx
 38fd1f1:      	shrq	%cl, %r10
 38fd1f4:      	cmpl	%r9d, %r8d
 38fd1f7:      	movq	$-0x1, %rcx
 38fd1fe:      	cmoveq	%r10, %rcx
 38fd202:      	movl	%r8d, %eax
 38fd205:      	andq	%rbx, %rcx
 38fd208:      	movq	%r13, %rbx
 38fd20b:      	andq	(%rdi,%rax,8), %rcx
 38fd20f:      	je	0x38fd21f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x201f>
 38fd211:      	tzcntq	%rcx, %rdx
 38fd216:      	shll	$0x6, %r8d
 38fd21a:      	orl	%r8d, %edx
 38fd21d:      	jmp	0x38fd270 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd21f:      	leal	0x1(%r9), %ecx
 38fd223:      	leal	0x1(%rax), %r8d
 38fd227:      	cmpl	%ecx, %r8d
 38fd22a:      	je	0x38fd270 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd22c:      	movl	%r9d, %r8d
 38fd22f:      	leaq	-0x1(%r8), %r9
 38fd233:      	nopw	%cs:(%rax,%rax)
 38fd23d:      	nopl	(%rax)
 38fd240:      	cmpq	%rax, %r9
 38fd243:      	movq	$-0x1, %rcx
 38fd24a:      	cmoveq	%r10, %rcx
 38fd24e:      	andq	0x8(%rdi,%rax,8), %rcx
 38fd253:      	jne	0x38fd4e7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22e7>
 38fd259:      	incq	%rax
 38fd25c:      	cmpq	%rax, %r8
 38fd25f:      	jne	0x38fd240 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2040>
 38fd261:      	nopw	%cs:(%rax,%rax)
 38fd26b:      	nopl	(%rax,%rax)
 38fd270:      	movslq	%r12d, %r13
 38fd273:      	movl	%edx, (%rsi,%rbx,4)
 38fd276:      	xorl	%ebx, %ebx
 38fd278:      	movq	0x78(%rsp), %rax
 38fd27d:      	movq	(%rax), %rbp
 38fd280:      	imulq	$0xe8, %r13, %rax
 38fd287:      	movq	0x8(%rbp,%rax), %rdi
 38fd28c:      	testq	%rdi, %rdi
 38fd28f:      	je	0x38fd2b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x20b0>
 38fd291:      	movq	0x8(%rsp), %rdx
 38fd296:      	movq	%rdx, %rsi
 38fd299:      	callq	0x35ba9f0 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd29e:      	jmp	0x38fd360 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2160>
 38fd2a3:      	nopw	%cs:(%rax,%rax)
 38fd2ad:      	nopl	(%rax)
 38fd2b0:      	addq	%rax, %rbp
 38fd2b3:      	movq	(%rbp), %rdx
 38fd2b7:      	testq	%rdx, %rdx
 38fd2ba:      	je	0x38fd34e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x214e>
 38fd2c0:      	leaq	0x10(%rbp), %rdi
 38fd2c4:      	movl	$0x0, 0x10(%rbp)
 38fd2cb:      	movq	$0x0, 0xd8(%rbp)
 38fd2d6:      	movq	0xb0(%rsp), %rax
 38fd2de:      	movq	%rax, 0xe0(%rbp)
 38fd2e5:      	xorps	%xmm0, %xmm0
 38fd2e8:      	movups	%xmm0, 0x98(%rbp)
 38fd2ef:      	movups	%xmm0, 0xa8(%rbp)
 38fd2f6:      	movups	%xmm0, 0xb8(%rbp)
 38fd2fd:      	movups	%xmm0, 0xc8(%rbp)
 38fd304:      	movups	%xmm0, 0x28(%rbp)
 38fd308:      	movups	%xmm0, 0x18(%rbp)
 38fd30c:      	movups	%xmm0, 0x48(%rbp)
 38fd310:      	movups	%xmm0, 0x38(%rbp)
 38fd314:      	movups	%xmm0, 0x68(%rbp)
 38fd318:      	movups	%xmm0, 0x58(%rbp)
 38fd31c:      	movups	%xmm0, 0x88(%rbp)
 38fd323:      	movups	%xmm0, 0x78(%rbp)
 38fd327:      	movq	%rdi, 0x8(%rbp)
 38fd32b:      	movq	%rdx, %rsi
 38fd32e:      	callq	0x35ba9f0 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd333:      	movq	0x8(%rbp), %rdi
 38fd337:      	movq	0x8(%rsp), %rdx
 38fd33c:      	movq	%rdx, %rsi
 38fd33f:      	callq	0x35ba9f0 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd344:      	movq	$0x0, (%rbp)
 38fd34c:      	jmp	0x38fd360 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2160>
 38fd34e:      	movq	0x8(%rsp), %rax
 38fd353:      	movq	%rax, (%rbp)
 38fd357:      	nopw	(%rax,%rax)
 38fd360:      	movslq	%r15d, %rax
 38fd363:      	movq	(%rsp), %r9
 38fd367:      	movq	0x550(%r9), %rcx
 38fd36e:      	movzbl	(%rcx,%rax), %esi
 38fd372:      	movq	(%r9), %rdi
 38fd375:      	testb	%bl, %bl
 38fd377:      	je	0x38fd3a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21a0>
 38fd379:      	movl	0x20(%rdi), %ecx
 38fd37c:      	addl	%r12d, %ecx
 38fd37f:      	movq	0x8(%rdi), %rdx
 38fd383:      	leaq	(%rcx,%rcx,4), %r8
 38fd387:      	cmpb	0x10(%rdx,%r8,8), %sil
 38fd38c:      	ja	0x38fd3aa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21aa>
 38fd38e:      	movq	0xb8(%rsp), %rsi
 38fd396:      	movq	(%rsi), %rsi
 38fd399:      	movl	(%rsi,%rax,4), %esi
 38fd39c:      	jmp	0x38fd3fa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21fa>
 38fd39e:      	nop
 38fd3a0:      	movq	0x8(%rdi), %rdx
 38fd3a4:      	movl	0x20(%rdi), %ecx
 38fd3a7:      	addl	%r12d, %ecx
 38fd3aa:      	leaq	(%rcx,%rcx,4), %rcx
 38fd3ae:      	movb	%sil, 0x10(%rdx,%rcx,8)
 38fd3b3:      	movl	0x20(%rdi), %ecx
 38fd3b6:      	addl	%r12d, %ecx
 38fd3b9:      	movq	0x8(%rdi), %rdx
 38fd3bd:      	leaq	(%rcx,%rcx,4), %rcx
 38fd3c1:      	movzbl	0x15(%rdx,%rcx,8), %ecx
 38fd3c6:      	cmpl	$0x4, %ecx
 38fd3c9:      	ja	0x38fd3df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd3cb:      	movl	$0x15, %edx
 38fd3d0:      	btl	%ecx, %edx
 38fd3d3:      	jae	0x38fd3df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd3d5:      	cmpb	%sil, 0x40(%rdi)
 38fd3d9:      	jae	0x38fd3df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd3db:      	movb	%sil, 0x40(%rdi)
 38fd3df:      	movq	0x578(%r9), %rcx
 38fd3e6:      	movl	(%rcx,%rax,4), %esi
 38fd3e9:      	movq	(%r9), %rcx
 38fd3ec:      	movq	0x8(%rcx), %rdx
 38fd3f0:      	movl	0x20(%rcx), %ecx
 38fd3f3:      	addl	%r12d, %ecx
 38fd3f6:      	testb	%bl, %bl
 38fd3f8:      	je	0x38fd405 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2205>
 38fd3fa:      	leaq	(%rcx,%rcx,4), %rdi
 38fd3fe:      	cmpq	%rsi, 0x8(%rdx,%rdi,8)
 38fd403:      	jge	0x38fd40e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x220e>
 38fd405:      	leaq	(%rcx,%rcx,4), %rcx
 38fd409:      	movq	%rsi, 0x8(%rdx,%rcx,8)
 38fd40e:      	movq	0x208(%rsp), %rcx
 38fd416:      	movl	%r12d, (%rcx,%rax,4)
 38fd41a:      	movslq	%r12d, %rbx
 38fd41d:      	movq	0x258(%rsp), %rax
 38fd425:      	movq	%rbx, %rcx
 38fd428:      	shlq	$0x5, %rcx
 38fd42c:      	leaq	(%rax,%rcx), %rbp
 38fd430:      	movl	0x8(%rax,%rcx), %edx
 38fd434:      	cmpl	0xc(%rax,%rcx), %edx
 38fd438:      	jae	0x38fd4f1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22f1>
 38fd43e:      	movq	(%rbp), %rax
 38fd442:      	movl	%edx, %ecx
 38fd444:      	movl	%r15d, (%rax,%rcx,4)
 38fd448:      	incl	0x8(%rbp)
 38fd44b:      	movq	0x8(%rsp), %rax
 38fd450:      	movss	0x74(%rax), %xmm0
 38fd455:      	movq	0x170(%rsp), %rax
 38fd45d:      	addss	(%rax,%rbx,4), %xmm0
 38fd462:      	movl	$0x1, %edx
 38fd467:      	movl	%r12d, %ecx
 38fd46a:      	shlq	%cl, %rdx
 38fd46d:      	movss	%xmm0, (%rax,%rbx,4)
 38fd472:      	movq	0x1c0(%rsp), %rax
 38fd47a:      	movl	%r12d, %ecx
 38fd47d:      	shrl	$0x6, %ecx
 38fd480:      	orq	%rdx, (%rax,%rcx,8)
 38fd484:      	cmpl	%r12d, %r15d
 38fd487:      	setne	%al
 38fd48a:      	movq	0x30(%rsp), %rbx
 38fd48f:      	orb	%al, %bl
 38fd491:      	addq	$0x8, %r14
 38fd495:      	movq	0x70(%rsp), %rsi
 38fd49a:      	cmpq	%rsi, %r14
 38fd49d:      	movq	(%rsp), %rbp
 38fd4a1:      	jne	0x38fce50 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c50>
 38fd4a7:      	jmp	0x38fd50d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x230d>
 38fd4a9:      	movq	%rbx, %rsi
 38fd4ac:      	movq	(%rbp), %rax
 38fd4b0:      	movl	0x20(%rax), %ecx
 38fd4b3:      	leal	(%rcx,%r12), %edx
 38fd4b7:      	movq	0x8(%rax), %rax
 38fd4bb:      	leaq	(%rdx,%rdx,4), %rdx
 38fd4bf:      	movzbl	0x15(%rax,%rdx,8), %edx
 38fd4c4:      	addl	%r15d, %ecx
 38fd4c7:      	leaq	(%rcx,%rcx,4), %rcx
 38fd4cb:      	movb	$0x1, %bl
 38fd4cd:      	cmpb	0x15(%rax,%rcx,8), %dl
 38fd4d1:      	je	0x38fd278 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2078>
 38fd4d7:      	movq	0x40(%rsp), %rax
 38fd4dc:      	movq	(%rax), %rdx
 38fd4df:      	movq	%rsi, %rbx
 38fd4e2:      	jmp	0x38fd150 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd4e7:      	incl	%eax
 38fd4e9:      	movl	%eax, %r8d
 38fd4ec:      	jmp	0x38fd211 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2011>
 38fd4f1:      	incq	%rdx
 38fd4f4:      	leaq	0x10(%rbp), %rsi
 38fd4f8:      	movl	$0x4, %ecx
 38fd4fd:      	movq	%rbp, %rdi
 38fd500:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fd505:      	movl	0x8(%rbp), %edx
 38fd508:      	jmp	0x38fd43e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x223e>
 38fd50d:      	movq	0x28(%rbp), %r14
 38fd511:      	movq	0x30(%rbp), %rsi
 38fd515:      	cmpq	%rsi, %r14
 38fd518:      	jne	0x38fd523 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2323>
 38fd51a:      	jmp	0x38fd551 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2351>
 38fd51c:      	xorl	%ebx, %ebx
 38fd51e:      	cmpq	%rsi, %r14
 38fd521:      	je	0x38fd551 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2351>
 38fd523:      	movq	0x170(%rsp), %rax
 38fd52b:      	movq	%r14, %rcx
 38fd52e:      	nop
 38fd530:      	movq	(%rcx), %rdx
 38fd533:      	movl	0x70(%rdx), %edi
 38fd536:      	shlq	$0x22, %rdi
 38fd53a:      	sarq	$0x22, %rdi
 38fd53e:      	movss	(%rax,%rdi,4), %xmm0
 38fd543:      	movss	%xmm0, 0x74(%rdx)
 38fd548:      	addq	$0x8, %rcx
 38fd54c:      	cmpq	%rsi, %rcx
 38fd54f:      	jne	0x38fd530 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2330>
 38fd551:      	movq	%r14, %rdi
 38fd554:      	callq	0x38feb50 <_ZN4llvm11stable_sortIRSt6vectorIPNS_12LiveIntervalESaIS3_EEN12_GLOBAL__N_114IntervalSorterEEEvOT_T0_>
 38fd559:      	movq	%rbx, 0x30(%rsp)
 38fd55e:      	testb	$0x1, %bl
 38fd561:      	je	0x38fde66 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fd567:      	movq	(%rsp), %rbp
 38fd56b:      	movl	0x48(%rbp), %r9d
 38fd56f:      	testq	%r9, %r9
 38fd572:      	je	0x38fd725 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2525>
 38fd578:      	xorl	%r15d, %r15d
 38fd57b:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd581:      	leaq	0x4a17950(%rip), %rax   # 0x8314ed8 <_ZTVN4llvm27FixedStackPseudoSourceValueE>
 38fd588:      	addq	$0x10, %rax
 38fd58c:      	movq	%rax, 0x18(%rsp)
 38fd591:      	movq	%r9, 0x8(%rsp)
 38fd596:      	jmp	0x38fd5ac <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23ac>
 38fd598:      	nopl	(%rax,%rax)
 38fd5a0:      	incq	%r15
 38fd5a3:      	cmpq	%r9, %r15
 38fd5a6:      	je	0x38fd725 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2525>
 38fd5ac:      	movq	0x208(%rsp), %rax
 38fd5b4:      	movl	(%rax,%r15,4), %r13d
 38fd5b8:      	cmpq	%r10, %r13
 38fd5bb:      	je	0x38fd5a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd5bd:      	cmpq	%r13, %r15
 38fd5c0:      	je	0x38fd5a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd5c2:      	movq	0x58(%rsp), %rax
 38fd5c7:      	movq	0x160(%rax), %r12
 38fd5ce:      	leal	(%r13,%r13), %eax
 38fd5d3:      	movl	%r13d, %ebp
 38fd5d6:      	sarl	$0x1f, %ebp
 38fd5d9:      	xorl	%eax, %ebp
 38fd5db:      	leaq	0x48(%r12), %r14
 38fd5e0:      	cmpl	%ebp, 0x50(%r12)
 38fd5e5:      	ja	0x38fd5fd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23fd>
 38fd5e7:      	leal	0x1(%rbp), %esi
 38fd5ea:      	movq	%r14, %rdi
 38fd5ed:      	callq	0x37a51c0 <_ZN4llvm15SmallVectorImplISt10unique_ptrINS_27FixedStackPseudoSourceValueESt14default_deleteIS2_EEE10resizeImplILb0EEEvm>
 38fd5f2:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd5f8:      	movq	0x8(%rsp), %r9
 38fd5fd:      	movq	(%r14), %rbx
 38fd600:      	movq	(%rbx,%rbp,8), %r14
 38fd604:      	testq	%r14, %r14
 38fd607:      	jne	0x38fd665 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2465>
 38fd609:      	movq	(%r12), %r12
 38fd60d:      	movl	$0x18, %edi
 38fd612:      	callq	0x828a6b0 <_Znwm@plt>
 38fd617:      	movq	%rax, %r14
 38fd61a:      	movl	$0x4, 0x8(%rax)
 38fd621:      	movq	(%r12), %rax
 38fd625:      	movq	%r12, %rdi
 38fd628:      	movl	$0x4, %esi
 38fd62d:      	callq	*0xa8(%rax)
 38fd633:      	movl	%eax, 0xc(%r14)
 38fd637:      	movq	0x18(%rsp), %rax
 38fd63c:      	movq	%rax, (%r14)
 38fd63f:      	movl	%r13d, 0x10(%r14)
 38fd643:      	movq	(%rbx,%rbp,8), %rdi
 38fd647:      	movq	%r14, (%rbx,%rbp,8)
 38fd64b:      	testq	%rdi, %rdi
 38fd64e:      	je	0x38fd65a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x245a>
 38fd650:      	movq	(%rdi), %rax
 38fd653:      	callq	*0x10(%rax)
 38fd656:      	movq	(%rbx,%rbp,8), %r14
 38fd65a:      	movq	0x8(%rsp), %r9
 38fd65f:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd665:      	movq	0x38(%rsp), %rax
 38fd66a:      	movq	(%rax), %rcx
 38fd66d:      	leaq	(%r15,%r15,4), %rdx
 38fd671:      	shlq	$0x4, %rdx
 38fd675:      	movl	0x8(%rcx,%rdx), %eax
 38fd679:      	testq	%rax, %rax
 38fd67c:      	movq	(%rsp), %rbp
 38fd680:      	je	0x38fd5a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd686:      	movq	(%rcx,%rdx), %rdx
 38fd68a:      	leaq	(,%rax,8), %rsi
 38fd692:      	orq	$0x4, %r14
 38fd696:      	addq	$-0x8, %rsi
 38fd69a:      	movl	%esi, %edi
 38fd69c:      	notl	%edi
 38fd69e:      	movq	%rdx, %rcx
 38fd6a1:      	testb	$0x38, %dil
 38fd6a5:      	je	0x38fd6cf <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24cf>
 38fd6a7:      	movl	%esi, %edi
 38fd6a9:      	shrl	$0x3, %edi
 38fd6ac:      	incl	%edi
 38fd6ae:      	andl	$0x7, %edi
 38fd6b1:      	movq	%rdx, %rcx
 38fd6b4:      	nopw	%cs:(%rax,%rax)
 38fd6be:      	nop
 38fd6c0:      	movq	(%rcx), %r8
 38fd6c3:      	movq	%r14, (%r8)
 38fd6c6:      	addq	$0x8, %rcx
 38fd6ca:      	decq	%rdi
 38fd6cd:      	jne	0x38fd6c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24c0>
 38fd6cf:      	cmpq	$0x38, %rsi
 38fd6d3:      	jb	0x38fd5a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd6d9:      	leaq	(%rdx,%rax,8), %rax
 38fd6dd:      	nopl	(%rax)
 38fd6e0:      	movq	(%rcx), %rdx
 38fd6e3:      	movq	%r14, (%rdx)
 38fd6e6:      	movq	0x8(%rcx), %rdx
 38fd6ea:      	movq	%r14, (%rdx)
 38fd6ed:      	movq	0x10(%rcx), %rdx
 38fd6f1:      	movq	%r14, (%rdx)
 38fd6f4:      	movq	0x18(%rcx), %rdx
 38fd6f8:      	movq	%r14, (%rdx)
 38fd6fb:      	movq	0x20(%rcx), %rdx
 38fd6ff:      	movq	%r14, (%rdx)
 38fd702:      	movq	0x28(%rcx), %rdx
 38fd706:      	movq	%r14, (%rdx)
 38fd709:      	movq	0x30(%rcx), %rdx
 38fd70d:      	movq	%r14, (%rdx)
 38fd710:      	movq	0x38(%rcx), %rdx
 38fd714:      	movq	%r14, (%rdx)
 38fd717:      	addq	$0x40, %rcx
 38fd71b:      	cmpq	%rax, %rcx
 38fd71e:      	jne	0x38fd6e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24e0>
 38fd720:      	jmp	0x38fd5a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd725:      	movq	0x58(%rsp), %rax
 38fd72a:      	movq	0x148(%rax), %rbx
 38fd731:      	jmp	0x38fd744 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2544>
 38fd733:      	nopw	%cs:(%rax,%rax)
 38fd73d:      	nopl	(%rax)
 38fd740:      	movq	0x8(%rbx), %rbx
 38fd744:      	cmpq	0x88(%rsp), %rbx
 38fd74c:      	je	0x38fdd19 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b19>
 38fd752:      	leaq	0x30(%rbx), %r15
 38fd756:      	movq	0x38(%rbx), %r12
 38fd75a:      	cmpq	%r15, %r12
 38fd75d:      	je	0x38fd804 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2604>
 38fd763:      	movq	0x208(%rsp), %rax
 38fd76b:      	jmp	0x38fd77e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x257e>
 38fd76d:      	nopl	(%rax)
 38fd770:      	movq	0x8(%r12), %r12
 38fd775:      	cmpq	%r15, %r12
 38fd778:      	je	0x38fd800 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2600>
 38fd77e:      	movzwl	0x28(%r12), %edx
 38fd784:      	movzbl	0x2a(%r12), %ecx
 38fd78a:      	shll	$0x10, %ecx
 38fd78d:      	orl	%edx, %ecx
 38fd78f:      	testl	%ecx, %ecx
 38fd791:      	je	0x38fd7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25d0>
 38fd793:      	movq	0x20(%r12), %rdx
 38fd798:      	shll	$0x5, %ecx
 38fd79b:      	xorl	%esi, %esi
 38fd79d:      	jmp	0x38fd7a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a9>
 38fd79f:      	nop
 38fd7a0:      	addq	$0x20, %rsi
 38fd7a4:      	cmpq	%rsi, %rcx
 38fd7a7:      	je	0x38fd7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25d0>
 38fd7a9:      	cmpb	$0x5, (%rdx,%rsi)
 38fd7ad:      	jne	0x38fd7a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd7af:      	movslq	0x10(%rdx,%rsi), %rdi
 38fd7b4:      	testq	%rdi, %rdi
 38fd7b7:      	js	0x38fd7a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd7b9:      	movl	(%rax,%rdi,4), %r8d
 38fd7bd:      	cmpl	$-0x1, %r8d
 38fd7c1:      	je	0x38fd7a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd7c3:      	cmpl	%edi, %r8d
 38fd7c6:      	je	0x38fd7a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd7c8:      	movl	%r8d, 0x10(%rdx,%rsi)
 38fd7cd:      	jmp	0x38fd7a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd7cf:      	nop
 38fd7d0:      	testb	$0x4, (%r12)
 38fd7d5:      	jne	0x38fd770 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd7d7:      	nopw	(%rax,%rax)
 38fd7e0:      	testb	$0x8, 0x2c(%r12)
 38fd7e6:      	je	0x38fd770 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd7e8:      	movq	0x8(%r12), %r12
 38fd7ed:      	testb	$0x8, 0x2c(%r12)
 38fd7f3:      	jne	0x38fd7e8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25e8>
 38fd7f5:      	jmp	0x38fd770 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd7fa:      	nopw	(%rax,%rax)
 38fd800:      	movq	0x38(%rbx), %r12
 38fd804:      	leaq	0xd0(%rsp), %rax
 38fd80c:      	movq	%rax, 0xc0(%rsp)
 38fd814:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 38fd81e:      	movq	%rax, 0xc8(%rsp)
 38fd826:      	cmpq	%r15, %r12
 38fd829:      	je	0x38fd740 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fd82f:      	leaq	0x14(%rsp), %r14
 38fd834:      	jmp	0x38fd84e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x264e>
 38fd836:      	nopw	%cs:(%rax,%rax)
 38fd840:      	movq	0x8(%r12), %r12
 38fd845:      	cmpq	%r15, %r12
 38fd848:      	je	0x38fdbe0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29e0>
 38fd84e:      	movl	0x4cb226c(%rip), %eax   # 0x85afac0 <_ZL8DCELimit+0x78>
 38fd854:      	cmpl	$-0x1, %eax
 38fd857:      	setne	%cl
 38fd85a:      	testl	%eax, %eax
 38fd85c:      	setle	%al
 38fd85f:      	testb	%al, %cl
 38fd861:      	jne	0x38fdbe0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29e0>
 38fd867:      	movq	0x8(%rbp), %rdi
 38fd86b:      	movq	(%rdi), %rax
 38fd86e:      	movq	%r12, %rsi
 38fd871:      	movq	%r14, %rdx
 38fd874:      	leaq	0x54(%rsp), %rcx
 38fd879:      	callq	*0x98(%rax)
 38fd87f:      	testb	%al, %al
 38fd881:      	je	0x38fd8d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd883:      	movl	0x14(%rsp), %eax
 38fd887:      	cmpl	$-0x1, %eax
 38fd88a:      	je	0x38fd8d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd88c:      	cmpl	0x54(%rsp), %eax
 38fd890:      	jne	0x38fd8d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd892:      	movl	0xc8(%rsp), %edx
 38fd899:      	cmpl	0xcc(%rsp), %edx
 38fd8a0:      	jae	0x38fdb83 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2983>
 38fd8a6:      	movq	0xc0(%rsp), %rax
 38fd8ae:      	movl	%edx, %ecx
 38fd8b0:      	movq	%r12, (%rax,%rcx,8)
 38fd8b4:      	incl	0xc8(%rsp)
 38fd8bb:      	testb	$0x4, (%r12)
 38fd8c0:      	je	0x38fda40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fd8c6:      	jmp	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd8cb:      	nopl	(%rax,%rax)
 38fd8d0:      	testb	$0x4, (%r12)
 38fd8d5:      	movq	%r12, %rax
 38fd8d8:      	jne	0x38fd8fa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26fa>
 38fd8da:      	testb	$0x8, 0x2c(%r12)
 38fd8e0:      	movq	%r12, %rax
 38fd8e3:      	je	0x38fd8fa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26fa>
 38fd8e5:      	movq	%r12, %rax
 38fd8e8:      	nopl	(%rax,%rax)
 38fd8f0:      	movq	0x8(%rax), %rax
 38fd8f4:      	testb	$0x8, 0x2c(%rax)
 38fd8f8:      	jne	0x38fd8f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26f0>
 38fd8fa:      	movq	0x8(%rax), %r13
 38fd8fe:      	movq	$0x0, 0xa0(%rsp)
 38fd90a:      	movb	$0x0, 0xa8(%rsp)
 38fd912:      	movq	$0x0, 0x90(%rsp)
 38fd91e:      	movb	$0x0, 0x98(%rsp)
 38fd926:      	movq	0x8(%rbp), %rdi
 38fd92a:      	movq	(%rdi), %rax
 38fd92d:      	movq	%r12, %rsi
 38fd930:      	movq	%r14, %rdx
 38fd933:      	leaq	0xa0(%rsp), %rcx
 38fd93b:      	callq	*0x60(%rax)
 38fd93e:      	testl	%eax, %eax
 38fd940:      	je	0x38fda30 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2830>
 38fd946:      	movl	%eax, %ebp
 38fd948:      	movq	%r12, %r14
 38fd94b:      	jmp	0x38fd958 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2758>
 38fd94d:      	nopl	(%rax)
 38fd950:      	movq	0x8(%r13), %r13
 38fd954:      	movq	0x8(%r14), %r14
 38fd958:      	cmpq	%r15, %r13
 38fd95b:      	je	0x38fd9c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27c0>
 38fd95d:      	movl	0x44(%r13), %eax
 38fd961:      	addl	$-0xe, %eax
 38fd964:      	cmpw	$0x4, %ax
 38fd968:      	ja	0x38fd9c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27c0>
 38fd96a:      	testb	$0x4, (%r13)
 38fd96f:      	jne	0x38fd992 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2792>
 38fd971:      	nopw	%cs:(%rax,%rax)
 38fd97b:      	nopl	(%rax,%rax)
 38fd980:      	testb	$0x8, 0x2c(%r13)
 38fd985:      	je	0x38fd992 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2792>
 38fd987:      	movq	0x8(%r13), %r13
 38fd98b:      	testb	$0x8, 0x2c(%r13)
 38fd990:      	jne	0x38fd987 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2787>
 38fd992:      	testb	$0x4, (%r14)
 38fd996:      	jne	0x38fd950 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd998:      	nopl	(%rax,%rax)
 38fd9a0:      	testb	$0x8, 0x2c(%r14)
 38fd9a5:      	je	0x38fd950 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd9a7:      	movq	0x8(%r14), %r14
 38fd9ab:      	testb	$0x8, 0x2c(%r14)
 38fd9b0:      	jne	0x38fd9a7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27a7>
 38fd9b2:      	jmp	0x38fd950 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd9b4:      	nopw	%cs:(%rax,%rax)
 38fd9be:      	nop
 38fd9c0:      	cmpq	%r15, %r13
 38fd9c3:      	je	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd9c5:      	movq	(%rsp), %rax
 38fd9c9:      	movq	0x8(%rax), %rdi
 38fd9cd:      	movq	(%rdi), %rax
 38fd9d0:      	movq	%r13, %rsi
 38fd9d3:      	leaq	0x54(%rsp), %rdx
 38fd9d8:      	leaq	0x90(%rsp), %rcx
 38fd9e0:      	callq	*0x80(%rax)
 38fd9e6:      	testl	%eax, %eax
 38fd9e8:      	je	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd9ea:      	movl	0x14(%rsp), %ecx
 38fd9ee:      	cmpl	0x54(%rsp), %ecx
 38fd9f2:      	jne	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd9f4:      	cmpl	%eax, %ebp
 38fd9f6:      	setne	%al
 38fd9f9:      	cmpl	$-0x1, %ecx
 38fd9fc:      	sete	%dl
 38fd9ff:      	orb	%al, %dl
 38fda01:      	je	0x38fda5e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x285e>
 38fda03:      	nopw	%cs:(%rax,%rax)
 38fda0d:      	nopl	(%rax)
 38fda10:      	movq	%r14, %r12
 38fda13:      	movq	(%rsp), %rbp
 38fda17:      	leaq	0x14(%rsp), %r14
 38fda1c:      	testb	$0x4, (%r12)
 38fda21:      	jne	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fda27:      	jmp	0x38fda40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fda29:      	nopl	(%rax)
 38fda30:      	movq	(%rsp), %rbp
 38fda34:      	testb	$0x4, (%r12)
 38fda39:      	jne	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fda3f:      	nop
 38fda40:      	testb	$0x8, 0x2c(%r12)
 38fda46:      	je	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fda4c:      	movq	0x8(%r12), %r12
 38fda51:      	testb	$0x8, 0x2c(%r12)
 38fda57:      	jne	0x38fda4c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x284c>
 38fda59:      	jmp	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fda5e:      	movq	0xa0(%rsp), %rax
 38fda66:      	cmpq	0x90(%rsp), %rax
 38fda6e:      	jne	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fda70:      	movzbl	0x98(%rsp), %eax
 38fda78:      	cmpb	%al, 0xa8(%rsp)
 38fda7f:      	jne	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fda81:      	movq	(%rsp), %rax
 38fda85:      	movq	(%rax), %rax
 38fda88:      	addl	0x20(%rax), %ecx
 38fda8b:      	movq	0x8(%rax), %rax
 38fda8f:      	leaq	(%rcx,%rcx,4), %rcx
 38fda93:      	cmpb	$0x1, 0x12(%rax,%rcx,8)
 38fda98:      	jne	0x38fda10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fda9e:      	movq	%r13, %rdi
 38fdaa1:      	movl	%ebp, %esi
 38fdaa3:      	xorl	%edx, %edx
 38fdaa5:      	movl	$0x1, %ecx
 38fdaaa:      	callq	0x3655740 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 38fdaaf:      	movl	0xc8(%rsp), %edx
 38fdab6:      	cmpl	$-0x1, %eax
 38fdab9:      	je	0x38fdb4b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x294b>
 38fdabf:      	cmpl	0xcc(%rsp), %edx
 38fdac6:      	movq	(%rsp), %rbp
 38fdaca:      	jae	0x38fdbac <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29ac>
 38fdad0:      	movq	0xc0(%rsp), %rax
 38fdad8:      	movl	%edx, %ecx
 38fdada:      	movq	%r12, (%rax,%rcx,8)
 38fdade:      	movl	0xc8(%rsp), %edx
 38fdae5:      	incl	%edx
 38fdae7:      	movl	%edx, 0xc8(%rsp)
 38fdaee:      	cmpl	0xcc(%rsp), %edx
 38fdaf5:      	jae	0x38fdb58 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2958>
 38fdaf7:      	movq	0xc0(%rsp), %rax
 38fdaff:      	movl	%edx, %ecx
 38fdb01:      	movq	%r13, (%rax,%rcx,8)
 38fdb05:      	incl	0xc8(%rsp)
 38fdb0c:      	testb	$0x4, (%r14)
 38fdb10:      	jne	0x38fdb32 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2932>
 38fdb12:      	nopw	%cs:(%rax,%rax)
 38fdb1c:      	nopl	(%rax)
 38fdb20:      	testb	$0x8, 0x2c(%r14)
 38fdb25:      	je	0x38fdb32 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2932>
 38fdb27:      	movq	0x8(%r14), %r14
 38fdb2b:      	testb	$0x8, 0x2c(%r14)
 38fdb30:      	jne	0x38fdb27 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2927>
 38fdb32:      	movq	0x8(%r14), %r12
 38fdb36:      	leaq	0x14(%rsp), %r14
 38fdb3b:      	testb	$0x4, (%r12)
 38fdb40:      	je	0x38fda40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fdb46:      	jmp	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fdb4b:      	movq	(%rsp), %rbp
 38fdb4f:      	cmpl	0xcc(%rsp), %edx
 38fdb56:      	jb	0x38fdaf7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28f7>
 38fdb58:      	movl	%edx, %edx
 38fdb5a:      	incq	%rdx
 38fdb5d:      	movl	$0x8, %ecx
 38fdb62:      	leaq	0xc0(%rsp), %rdi
 38fdb6a:      	leaq	0xd0(%rsp), %rsi
 38fdb72:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdb77:      	movl	0xc8(%rsp), %edx
 38fdb7e:      	jmp	0x38fdaf7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28f7>
 38fdb83:      	incq	%rdx
 38fdb86:      	movl	$0x8, %ecx
 38fdb8b:      	leaq	0xc0(%rsp), %rdi
 38fdb93:      	leaq	0xd0(%rsp), %rsi
 38fdb9b:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdba0:      	movl	0xc8(%rsp), %edx
 38fdba7:      	jmp	0x38fd8a6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26a6>
 38fdbac:      	incq	%rdx
 38fdbaf:      	movl	$0x8, %ecx
 38fdbb4:      	leaq	0xc0(%rsp), %rdi
 38fdbbc:      	leaq	0xd0(%rsp), %rsi
 38fdbc4:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdbc9:      	movl	0xc8(%rsp), %edx
 38fdbd0:      	jmp	0x38fdad0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28d0>
 38fdbd5:      	nopw	%cs:(%rax,%rax)
 38fdbdf:      	nop
 38fdbe0:      	movq	0xc0(%rsp), %r14
 38fdbe8:      	movl	0xc8(%rsp), %eax
 38fdbef:      	testq	%rax, %rax
 38fdbf2:      	je	0x38fdcfb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2afb>
 38fdbf8:      	movq	%rbx, %r15
 38fdbfb:      	leaq	(%r14,%rax,8), %rbx
 38fdbff:      	jmp	0x38fdc22 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a22>
 38fdc01:      	nopw	%cs:(%rax,%rax)
 38fdc0b:      	nopl	(%rax,%rax)
 38fdc10:      	callq	0x3654750 <_ZN4llvm12MachineInstr15eraseFromParentEv>
 38fdc15:      	addq	$0x8, %r14
 38fdc19:      	cmpq	%rbx, %r14
 38fdc1c:      	je	0x38fdcf0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2af0>
 38fdc22:      	movq	(%r14), %rdi
 38fdc25:      	movq	0x20(%rbp), %rax
 38fdc29:      	testq	%rax, %rax
 38fdc2c:      	je	0x38fdc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdc2e:      	movq	0x78(%rax), %rcx
 38fdc32:      	movl	0x88(%rax), %edx
 38fdc38:      	testq	%rdx, %rdx
 38fdc3b:      	je	0x38fdca0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa0>
 38fdc3d:      	movl	%edi, %r8d
 38fdc40:      	shrl	$0x4, %r8d
 38fdc44:      	movl	%edi, %esi
 38fdc46:      	shrl	$0x9, %esi
 38fdc49:      	xorl	%r8d, %esi
 38fdc4c:      	leal	-0x1(%rdx), %r8d
 38fdc50:      	andl	%r8d, %esi
 38fdc53:      	movl	%esi, %r9d
 38fdc56:      	shll	$0x4, %r9d
 38fdc5a:      	movq	(%rcx,%r9), %r11
 38fdc5e:      	cmpq	%r11, %rdi
 38fdc61:      	je	0x38fdca7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa7>
 38fdc63:      	movl	$0x1, %r10d
 38fdc69:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 38fdc70:      	je	0x38fdca0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa0>
 38fdc72:      	addl	%r10d, %esi
 38fdc75:      	incl	%r10d
 38fdc78:      	andl	%r8d, %esi
 38fdc7b:      	movq	%rsi, %r11
 38fdc7e:      	shlq	$0x4, %r11
 38fdc82:      	leaq	(%rcx,%r11), %r9
 38fdc86:      	movq	(%rcx,%r11), %r11
 38fdc8a:      	cmpq	%r11, %rdi
 38fdc8d:      	je	0x38fdcaa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aaa>
 38fdc8f:      	jmp	0x38fdc69 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a69>
 38fdc91:      	nopw	%cs:(%rax,%rax)
 38fdc9b:      	nopl	(%rax,%rax)
 38fdca0:      	movq	%rdx, %r9
 38fdca3:      	shlq	$0x4, %r9
 38fdca7:      	addq	%rcx, %r9
 38fdcaa:      	shlq	$0x4, %rdx
 38fdcae:      	addq	%rdx, %rcx
 38fdcb1:      	cmpq	%rcx, %r9
 38fdcb4:      	je	0x38fdc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdcba:      	movq	0x8(%r9), %rcx
 38fdcbe:      	andq	$-0x8, %rcx
 38fdcc2:      	movq	$-0x2000, (%r9)         # imm = 0xE000
 38fdcc9:      	movq	0x80(%rax), %xmm0
 38fdcd1:      	paddd	-0x2ada9a9(%rip), %xmm0 # 0xe23330 <.LCPI9_4>
 38fdcd9:      	movq	%xmm0, 0x80(%rax)
 38fdce1:      	movq	$0x0, 0x10(%rcx)
 38fdce9:      	jmp	0x38fdc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdcee:      	nop
 38fdcf0:      	movq	0xc0(%rsp), %r14
 38fdcf8:      	movq	%r15, %rbx
 38fdcfb:      	leaq	0xd0(%rsp), %rax
 38fdd03:      	cmpq	%rax, %r14
 38fdd06:      	je	0x38fd740 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fdd0c:      	movq	%r14, %rdi
 38fdd0f:      	callq	0x828a6d0 <free@plt>
 38fdd14:      	jmp	0x38fd740 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fdd19:      	movl	0x5d0(%rbp), %eax
 38fdd1f:      	movq	%rax, 0x38(%rsp)
 38fdd24:      	testq	%rax, %rax
 38fdd27:      	je	0x38fde66 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fdd2d:      	movq	(%rsp), %rax
 38fdd31:      	movq	0x668(%rax), %rcx
 38fdd38:      	movq	%rcx, 0x8(%rsp)
 38fdd3d:      	movq	(%rax), %rcx
 38fdd40:      	movq	%rcx, 0x18(%rsp)
 38fdd45:      	movq	0x5c8(%rax), %rdi
 38fdd4c:      	xorl	%r8d, %r8d
 38fdd4f:      	jmp	0x38fdd6e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b6e>
 38fdd51:      	nopw	%cs:(%rax,%rax)
 38fdd5b:      	nopl	(%rax,%rax)
 38fdd60:      	incq	%r8
 38fdd63:      	cmpq	0x38(%rsp), %r8
 38fdd68:      	je	0x38fde66 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fdd6e:      	movq	0x8(%rsp), %rax
 38fdd73:      	movl	(%rax,%r8,4), %ebp
 38fdd77:      	cmpl	$-0x1, %ebp
 38fdd7a:      	je	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdd7c:      	movq	0x18(%rsp), %rax
 38fdd81:      	movl	0x20(%rax), %r9d
 38fdd85:      	movq	0x8(%rax), %r10
 38fdd89:      	leaq	(%r8,%r8,8), %rax
 38fdd8d:      	leaq	(%rdi,%rax,8), %r11
 38fdd91:      	movl	0x40(%rdi,%rax,8), %ebx
 38fdd95:      	leal	-0x1(%rbx), %ecx
 38fdd98:      	movl	%ecx, %r14d
 38fdd9b:      	notb	%cl
 38fdd9d:      	movq	$-0x1, %r15
 38fdda4:      	shrq	%cl, %r15
 38fdda7:      	shrl	$0x6, %r14d
 38fddab:      	movl	%r14d, %r12d
 38fddae:      	incl	%r12d
 38fddb1:      	leaq	-0x1(%r14), %r13
 38fddb5:      	jmp	0x38fddca <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bca>
 38fddb7:      	incl	%ebp
 38fddb9:      	movl	%ebp, %edx
 38fddbb:      	tzcntq	%rax, %rbp
 38fddc0:      	shll	$0x6, %edx
 38fddc3:      	orl	%edx, %ebp
 38fddc5:      	cmpl	$-0x1, %ebp
 38fddc8:      	je	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fddca:      	leal	(%rbp,%r9), %eax
 38fddcf:      	leaq	(%rax,%rax,4), %rax
 38fddd3:      	movq	$-0x1, 0x8(%r10,%rax,8)
 38fdddc:      	incl	%ebp
 38fddde:      	cmpl	%ebx, %ebp
 38fdde0:      	je	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdde6:      	movl	%ebp, %edx
 38fdde8:      	shrl	$0x6, %edx
 38fddeb:      	cmpl	%r14d, %edx
 38fddee:      	ja	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fddf4:      	andl	$0x3f, %ebp
 38fddf7:      	movl	%ebp, %ecx
 38fddf9:      	negb	%cl
 38fddfb:      	movq	$-0x1, %rax
 38fde02:      	shrq	%cl, %rax
 38fde05:      	movq	(%r11), %rcx
 38fde08:      	notq	%rax
 38fde0b:      	cmpl	$0x1, %ebp
 38fde0e:      	movl	$0x0, %esi
 38fde13:      	sbbq	%rsi, %rsi
 38fde16:      	orq	%rax, %rsi
 38fde19:      	cmpl	%r14d, %edx
 38fde1c:      	movq	$-0x1, %rax
 38fde23:      	cmoveq	%r15, %rax
 38fde27:      	movl	%edx, %ebp
 38fde29:      	andq	%rsi, %rax
 38fde2c:      	andq	(%rcx,%rbp,8), %rax
 38fde30:      	jne	0x38fddbb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bbb>
 38fde32:      	leal	0x1(%rbp), %eax
 38fde35:      	cmpl	%r12d, %eax
 38fde38:      	je	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fde3e:      	nop
 38fde40:      	cmpq	%rbp, %r13
 38fde43:      	movq	$-0x1, %rax
 38fde4a:      	cmoveq	%r15, %rax
 38fde4e:      	andq	0x8(%rcx,%rbp,8), %rax
 38fde53:      	jne	0x38fddb7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bb7>
 38fde59:      	incq	%rbp
 38fde5c:      	cmpq	%rbp, %r14
 38fde5f:      	jne	0x38fde40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c40>
 38fde61:      	jmp	0x38fdd60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fde66:      	movq	0x1c0(%rsp), %rdi
 38fde6e:      	cmpq	0x80(%rsp), %rdi
 38fde76:      	je	0x38fde7d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c7d>
 38fde78:      	callq	0x828a6d0 <free@plt>
 38fde7d:      	movq	0x258(%rsp), %rdi
 38fde85:      	movl	0x260(%rsp), %ebx
 38fde8c:      	testq	%rbx, %rbx
 38fde8f:      	leaq	0x218(%rsp), %r15
 38fde97:      	je	0x38fe1dc <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fdc>
 38fde9d:      	shlq	$0x5, %rbx
 38fdea1:      	leaq	-0x10(%rbx,%rdi), %r14
 38fdea6:      	negq	%rbx
 38fdea9:      	movq	(%rsp), %r13
 38fdead:      	jmp	0x38fdeba <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cba>
 38fdeaf:      	nop
 38fdeb0:      	addq	$-0x20, %r14
 38fdeb4:      	addq	$0x20, %rbx
 38fdeb8:      	je	0x38fdeca <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cca>
 38fdeba:      	movq	-0x10(%r14), %rdi
 38fdebe:      	cmpq	%rdi, %r14
 38fdec1:      	je	0x38fdeb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cb0>
 38fdec3:      	callq	0x828a6d0 <free@plt>
 38fdec8:      	jmp	0x38fdeb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cb0>
 38fdeca:      	movq	0x258(%rsp), %rdi
 38fded2:      	cmpq	0x68(%rsp), %rdi
 38fded7:      	je	0x38fdede <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cde>
 38fded9:      	callq	0x828a6d0 <free@plt>
 38fdede:      	movq	0x170(%rsp), %rdi
 38fdee6:      	cmpq	0x60(%rsp), %rdi
 38fdeeb:      	je	0x38fdef2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cf2>
 38fdeed:      	callq	0x828a6d0 <free@plt>
 38fdef2:      	movq	0x208(%rsp), %rdi
 38fdefa:      	cmpq	%r15, %rdi
 38fdefd:      	je	0x38fdf04 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d04>
 38fdeff:      	callq	0x828a6d0 <free@plt>
 38fdf04:      	movl	0x670(%r13), %edx
 38fdf0b:      	testq	%rdx, %rdx
 38fdf0e:      	je	0x38fdf26 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d26>
 38fdf10:      	shlq	$0x2, %rdx
 38fdf14:      	movq	0x48(%rsp), %rax
 38fdf19:      	movq	(%rax), %rdi
 38fdf1c:      	movl	$0xff, %esi
 38fdf21:      	callq	0x828ac20 <memset@plt>
 38fdf26:      	movq	0x28(%r13), %rax
 38fdf2a:      	cmpq	%rax, 0x30(%r13)
 38fdf2e:      	je	0x38fdf34 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d34>
 38fdf30:      	movq	%rax, 0x30(%r13)
 38fdf34:      	movl	0x48(%r13), %eax
 38fdf38:      	testq	%rax, %rax
 38fdf3b:      	je	0x38fe02b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fdf41:      	movq	0x40(%r13), %rbx
 38fdf45:      	shlq	$0x4, %rax
 38fdf49:      	leaq	(%rax,%rax,4), %rsi
 38fdf4d:      	leaq	-0x50(%rsi), %rcx
 38fdf51:      	movabsq	$-0x3333333333333333, %rdx # imm = 0xCCCCCCCCCCCCCCCD
 38fdf5b:      	movq	%rcx, %rax
 38fdf5e:      	mulq	%rdx
 38fdf61:      	shrq	$0x6, %rdx
 38fdf65:      	movl	%edx, %edi
 38fdf67:      	notl	%edi
 38fdf69:      	movq	%rbx, %rax
 38fdf6c:      	testb	$0x7, %dil
 38fdf70:      	je	0x38fdf90 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d90>
 38fdf72:      	incl	%edx
 38fdf74:      	andl	$0x7, %edx
 38fdf77:      	movq	%rbx, %rax
 38fdf7a:      	nopw	(%rax,%rax)
 38fdf80:      	movl	$0x0, 0x8(%rax)
 38fdf87:      	addq	$0x50, %rax
 38fdf8b:      	decq	%rdx
 38fdf8e:      	jne	0x38fdf80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d80>
 38fdf90:      	cmpq	$0x230, %rcx            # imm = 0x230
 38fdf97:      	jb	0x38fdff5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2df5>
 38fdf99:      	addq	%rbx, %rsi
 38fdf9c:      	nopl	(%rax)
 38fdfa0:      	movl	$0x0, 0x8(%rax)
 38fdfa7:      	movl	$0x0, 0x58(%rax)
 38fdfae:      	movl	$0x0, 0xa8(%rax)
 38fdfb8:      	movl	$0x0, 0xf8(%rax)
 38fdfc2:      	movl	$0x0, 0x148(%rax)
 38fdfcc:      	movl	$0x0, 0x198(%rax)
 38fdfd6:      	movl	$0x0, 0x1e8(%rax)
 38fdfe0:      	movl	$0x0, 0x238(%rax)
 38fdfea:      	addq	$0x280, %rax            # imm = 0x280
 38fdff0:      	cmpq	%rsi, %rax
 38fdff3:      	jne	0x38fdfa0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2da0>
 38fdff5:      	movl	0x48(%r13), %eax
 38fdff9:      	testq	%rax, %rax
 38fdffc:      	je	0x38fe02b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fdffe:      	shlq	$0x4, %rax
 38fe002:      	leaq	(%rax,%rax,4), %r14
 38fe006:      	leaq	-0x40(%rbx), %r15
 38fe00a:      	jmp	0x38fe016 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e16>
 38fe00c:      	nopl	(%rax)
 38fe010:      	addq	$-0x50, %r14
 38fe014:      	je	0x38fe02b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fe016:      	movq	-0x50(%rbx,%r14), %rdi
 38fe01b:      	leaq	(%r15,%r14), %rax
 38fe01f:      	cmpq	%rdi, %rax
 38fe022:      	je	0x38fe010 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e10>
 38fe024:      	callq	0x828a6d0 <free@plt>
 38fe029:      	jmp	0x38fe010 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e10>
 38fe02b:      	movl	$0x0, 0x48(%r13)
 38fe033:      	movq	$0x0, 0x558(%r13)
 38fe03e:      	movl	$0x0, 0x580(%r13)
 38fe049:      	movl	0x5d0(%r13), %eax
 38fe050:      	testq	%rax, %rax
 38fe053:      	je	0x38fe08b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e8b>
 38fe055:      	movq	0x5c8(%r13), %rbx
 38fe05c:      	shlq	$0x3, %rax
 38fe060:      	leaq	(%rax,%rax,8), %r14
 38fe064:      	leaq	-0x38(%rbx), %r15
 38fe068:      	jmp	0x38fe076 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e76>
 38fe06a:      	nopw	(%rax,%rax)
 38fe070:      	addq	$-0x48, %r14
 38fe074:      	je	0x38fe08b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e8b>
 38fe076:      	movq	-0x48(%rbx,%r14), %rdi
 38fe07b:      	leaq	(%r15,%r14), %rax
 38fe07f:      	cmpq	%rdi, %rax
 38fe082:      	je	0x38fe070 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e70>
 38fe084:      	callq	0x828a6d0 <free@plt>
 38fe089:      	jmp	0x38fe070 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e70>
 38fe08b:      	movl	$0x0, 0x5d0(%r13)
 38fe096:      	movl	0x688(%r13), %eax
 38fe09d:      	testq	%rax, %rax
 38fe0a0:      	je	0x38fe0db <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2edb>
 38fe0a2:      	movq	0x680(%r13), %rbx
 38fe0a9:      	shlq	$0x3, %rax
 38fe0ad:      	leaq	(%rax,%rax,8), %r14
 38fe0b1:      	leaq	-0x38(%rbx), %r15
 38fe0b5:      	jmp	0x38fe0c6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec6>
 38fe0b7:      	nopw	(%rax,%rax)
 38fe0c0:      	addq	$-0x48, %r14
 38fe0c4:      	je	0x38fe0db <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2edb>
 38fe0c6:      	movq	-0x48(%rbx,%r14), %rdi
 38fe0cb:      	leaq	(%r15,%r14), %rax
 38fe0cf:      	cmpq	%rdi, %rax
 38fe0d2:      	je	0x38fe0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec0>
 38fe0d4:      	callq	0x828a6d0 <free@plt>
 38fe0d9:      	jmp	0x38fe0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec0>
 38fe0db:      	movl	$0x0, 0x688(%r13)
 38fe0e6:      	movl	0x790(%r13), %eax
 38fe0ed:      	testq	%rax, %rax
 38fe0f0:      	je	0x38fe1b8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fb8>
 38fe0f6:      	movq	0x788(%r13), %rbx
 38fe0fd:      	imulq	$0xe8, %rax, %r15
 38fe104:      	leaq	-0x3438db(%rip), %r14   # 0x35ba830 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fe10b:      	jmp	0x38fe129 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f29>
 38fe10d:      	nopl	(%rax)
 38fe110:      	movl	$0x0, 0xcc(%r12)
 38fe11c:      	addq	$-0xe8, %r15
 38fe123:      	je	0x38fe1b8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fb8>
 38fe129:      	movq	-0xe0(%rbx,%r15), %r12
 38fe131:      	testq	%r12, %r12
 38fe134:      	je	0x38fe11c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f1c>
 38fe136:      	cmpl	$0x0, 0xc8(%r12)
 38fe13f:      	je	0x38fe110 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f10>
 38fe141:      	leaq	0x8(%r12), %rdi
 38fe146:      	movq	%r14, %rsi
 38fe149:      	xorl	%edx, %edx
 38fe14b:      	callq	0x35ba4f0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fe150:      	xorps	%xmm0, %xmm0
 38fe153:      	movups	%xmm0, 0xb8(%r12)
 38fe15c:      	movups	%xmm0, 0xa8(%r12)
 38fe165:      	movups	%xmm0, 0x98(%r12)
 38fe16e:      	movups	%xmm0, 0x88(%r12)
 38fe177:      	movl	$0x0, 0xc8(%r12)
 38fe183:      	movups	%xmm0, 0x18(%r12)
 38fe189:      	movups	%xmm0, 0x8(%r12)
 38fe18f:      	movups	%xmm0, 0x38(%r12)
 38fe195:      	movups	%xmm0, 0x28(%r12)
 38fe19b:      	movups	%xmm0, 0x58(%r12)
 38fe1a1:      	movups	%xmm0, 0x48(%r12)
 38fe1a7:      	movups	%xmm0, 0x78(%r12)
 38fe1ad:      	movups	%xmm0, 0x68(%r12)
 38fe1b3:      	jmp	0x38fe110 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f10>
 38fe1b8:      	movl	$0x0, 0x790(%r13)
 38fe1c3:      	movq	0x30(%rsp), %rax
 38fe1c8:      	andb	$0x1, %al
 38fe1ca:      	addq	$0x468, %rsp            # imm = 0x468
 38fe1d1:      	popq	%rbx
 38fe1d2:      	popq	%r12
 38fe1d4:      	popq	%r13
 38fe1d6:      	popq	%r14
 38fe1d8:      	popq	%r15
 38fe1da:      	popq	%rbp
 38fe1db:      	retq
 38fe1dc:      	movq	(%rsp), %r13
 38fe1e0:      	cmpq	0x68(%rsp), %rdi
 38fe1e5:      	jne	0x38fded9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cd9>
 38fe1eb:      	jmp	0x38fdede <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cde>
 38fe1f0:      	movq	%r12, %rbx
 38fe1f3:      	jmp	0x38fe239 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3039>
 38fe1f5:      	nopw	%cs:(%rax,%rax)
 38fe1ff:      	nop
 38fe200:      	movq	%rbx, %rdx
 38fe203:      	subq	%r12, %rdx
 38fe206:      	movq	%rdx, %rax
 38fe209:      	sarq	$0x3, %rax
 38fe20d:      	cmpq	$0x2, %rax
 38fe211:      	jl	0x38fe271 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3071>
 38fe213:      	shlq	$0x3, %rax
 38fe217:      	subq	%rax, %rdi
 38fe21a:      	addq	$0x10, %rdi
 38fe21e:      	movq	%r12, %rsi
 38fe221:      	callq	0x828ac50 <memmove@plt>
 38fe226:      	movq	%r12, %rax
 38fe229:      	movq	%r14, (%rax)
 38fe22c:      	leaq	0x8(%rbx), %rbp
 38fe230:      	cmpq	%r15, %rbp
 38fe233:      	je	0x38fc440 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fe239:      	movq	%rbx, %rdi
 38fe23c:      	movq	%rbp, %rbx
 38fe23f:      	movq	(%rbp), %r14
 38fe243:      	movq	(%r12), %rsi
 38fe247:      	movl	(%r14), %ecx
 38fe24a:      	cmpl	(%rsi), %ecx
 38fe24c:      	jl	0x38fe200 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3000>
 38fe24e:      	movq	(%rdi), %rdx
 38fe251:      	movq	%rbx, %rax
 38fe254:      	cmpl	(%rdx), %ecx
 38fe256:      	jge	0x38fe229 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe258:      	movq	%rbx, %rax
 38fe25b:      	nopl	(%rax,%rax)
 38fe260:      	movq	%rdx, (%rax)
 38fe263:      	movq	-0x10(%rax), %rdx
 38fe267:      	addq	$-0x8, %rax
 38fe26b:      	cmpl	(%rdx), %ecx
 38fe26d:      	jl	0x38fe260 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3060>
 38fe26f:      	jmp	0x38fe229 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe271:      	movq	%r12, %rax
 38fe274:      	cmpq	$0x8, %rdx
 38fe278:      	jne	0x38fe229 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe27a:      	movq	%rsi, 0x8(%rdi)
 38fe27e:      	jmp	0x38fe226 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3026>
 38fe280:      	xorl	%r12d, %r12d
 38fe283:      	jmp	0x38fce0c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c0c>
 38fe288:      	leaq	0x10(%r13), %rsi
 38fe28c:      	movl	$0x8, %ecx
 38fe291:      	movq	%r13, %rdi
 38fe294:      	movq	0x28(%rsp), %rdx
 38fe299:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fe29e:      	movl	0x8(%r13), %edi
 38fe2a2:      	movl	0x40(%r13), %ebp
 38fe2a6:      	movl	%edi, %ebx
 38fe2a8:      	jmp	0x38fbdfe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbfe>
 38fe2ad:      	leaq	0x10(%r13), %rsi
 38fe2b1:      	movl	$0x8, %ecx
 38fe2b6:      	movq	%r13, %rdi
 38fe2b9:      	movq	0x28(%rsp), %rdx
 38fe2be:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fe2c3:      	movl	0x8(%r13), %edi
 38fe2c7:      	movl	0x40(%r13), %ebp
 38fe2cb:      	movl	%edi, %ebx
 38fe2cd:      	jmp	0x38fbe9f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc9f>
 38fe2d2:      	leaq	-0x2c638ef(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 38fe2d9:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
