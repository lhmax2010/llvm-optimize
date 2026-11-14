
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000038fb170 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE>:
 38fb170:      	pushq	%rbp
 38fb171:      	pushq	%r15
 38fb173:      	pushq	%r14
 38fb175:      	pushq	%r13
 38fb177:      	pushq	%r12
 38fb179:      	pushq	%rbx
 38fb17a:      	subq	$0x468, %rsp            # imm = 0x468
 38fb181:      	movq	0x10(%rdi), %rcx
 38fb185:      	xorl	%eax, %eax
 38fb187:      	cmpl	$0x0, 0x80(%rcx)
 38fb18e:      	je	0x38fe138 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fc8>
 38fb194:      	cmpb	$0x0, 0x155(%rsi)
 38fb19b:      	jne	0x38fe138 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fc8>
 38fb1a1:      	movq	(%rdi), %rax
 38fb1a4:      	movq	0x10(%rax), %rcx
 38fb1a8:      	subq	0x8(%rax), %rcx
 38fb1ac:      	shrq	$0x3, %rcx
 38fb1b0:      	imull	$0xcccccccd, %ecx, %r15d # imm = 0xCCCCCCCD
 38fb1b7:      	subl	0x20(%rax), %r15d
 38fb1bb:      	leaq	0x40(%rdi), %rax
 38fb1bf:      	movq	%rax, 0x38(%rsp)
 38fb1c4:      	movslq	%r15d, %r14
 38fb1c7:      	movl	0x48(%rdi), %eax
 38fb1ca:      	cmpq	%rax, %r14
 38fb1cd:      	movq	%rdi, (%rsp)
 38fb1d1:      	movq	%rsi, 0x58(%rsp)
 38fb1d6:      	je	0x38fb42b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bb>
 38fb1dc:      	jae	0x38fb222 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb2>
 38fb1de:      	movq	%rdi, %rbp
 38fb1e1:      	movq	0x38(%rsp), %rcx
 38fb1e6:      	movq	(%rcx), %rbx
 38fb1e9:      	leaq	-0x40(%rbx), %r12
 38fb1ed:      	shlq	$0x4, %rax
 38fb1f1:      	leaq	(%rax,%rax,4), %r13
 38fb1f5:      	shlq	$0x4, %r14
 38fb1f9:      	leaq	(%r14,%r14,4), %r14
 38fb1fd:      	jmp	0x38fb20d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9d>
 38fb1ff:      	nop
 38fb200:      	addq	$-0x50, %r13
 38fb204:      	cmpq	%r13, %r14
 38fb207:      	je	0x38fb422 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb20d:      	movq	-0x50(%rbx,%r13), %rdi
 38fb212:      	leaq	(%r12,%r13), %rax
 38fb216:      	cmpq	%rdi, %rax
 38fb219:      	je	0x38fb200 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x90>
 38fb21b:      	callq	0x828a640 <free@plt>
 38fb220:      	jmp	0x38fb200 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x90>
 38fb222:      	movl	0x4c(%rdi), %ecx
 38fb225:      	cmpq	%rcx, %r14
 38fb228:      	jbe	0x38fb33d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cd>
 38fb22e:      	leaq	0x50(%rdi), %r13
 38fb232:      	leaq	0x258(%rsp), %r8
 38fb23a:      	movl	$0x50, %ecx
 38fb23f:      	movq	%rdi, %rbx
 38fb242:      	movq	0x38(%rsp), %rdi
 38fb247:      	movq	%r13, %rsi
 38fb24a:      	movq	%r14, %rdx
 38fb24d:      	callq	0x40f84d0 <_ZN4llvm15SmallVectorBaseIjE13mallocForGrowEPvmmRm>
 38fb252:      	movq	%rax, %r12
 38fb255:      	movq	0x40(%rbx), %rbp
 38fb259:      	movl	0x48(%rbx), %eax
 38fb25c:      	testq	%rax, %rax
 38fb25f:      	je	0x38fb3b4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x244>
 38fb265:      	movq	%r13, 0x18(%rsp)
 38fb26a:      	shlq	$0x4, %rax
 38fb26e:      	leaq	(%rax,%rax,4), %rbx
 38fb272:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb27c:      	movq	%r12, 0x8(%rsp)
 38fb281:      	jmp	0x38fb2c5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x155>
 38fb283:      	nopw	%cs:(%rax,%rax)
 38fb28d:      	nopl	(%rax)
 38fb290:      	movq	%rsi, (%r12)
 38fb294:      	movl	%r13d, 0x8(%r12)
 38fb299:      	movl	0xc(%rbp), %eax
 38fb29c:      	movl	%eax, 0xc(%r12)
 38fb2a1:      	movq	%rcx, (%rbp)
 38fb2a5:      	movl	$0x0, 0xc(%rbp)
 38fb2ac:      	movl	$0x0, 0x8(%rbp)
 38fb2b3:      	addq	$0x50, %rbp
 38fb2b7:      	addq	$0x50, %r12
 38fb2bb:      	addq	$-0x50, %rbx
 38fb2bf:      	je	0x38fb356 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e6>
 38fb2c5:      	leaq	0x10(%r12), %rax
 38fb2ca:      	movq	%rax, (%r12)
 38fb2ce:      	movq	%rdx, 0x8(%r12)
 38fb2d3:      	cmpq	%r12, %rbp
 38fb2d6:      	je	0x38fb2b3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x143>
 38fb2d8:      	movl	0x8(%rbp), %r13d
 38fb2dc:      	testl	%r13d, %r13d
 38fb2df:      	je	0x38fb2b3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x143>
 38fb2e1:      	movq	(%rbp), %rsi
 38fb2e5:      	leaq	0x10(%rbp), %rcx
 38fb2e9:      	cmpq	%rsi, %rcx
 38fb2ec:      	jne	0x38fb290 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x120>
 38fb2ee:      	cmpl	$0x9, %r13d
 38fb2f2:      	jb	0x38fb318 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a8>
 38fb2f4:      	movl	$0x8, %ecx
 38fb2f9:      	movq	%r12, %rdi
 38fb2fc:      	movq	%rax, %rsi
 38fb2ff:      	movq	%r13, %rdx
 38fb302:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fb307:      	movl	0x8(%rbp), %ecx
 38fb30a:      	testl	%ecx, %ecx
 38fb30c:      	je	0x38fb329 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b9>
 38fb30e:      	movq	(%rbp), %rsi
 38fb312:      	movq	(%r12), %rax
 38fb316:      	jmp	0x38fb31b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ab>
 38fb318:      	movl	%r13d, %ecx
 38fb31b:      	movl	%ecx, %edx
 38fb31d:      	shlq	$0x3, %rdx
 38fb321:      	movq	%rax, %rdi
 38fb324:      	callq	0x828ac50 <memcpy@plt>
 38fb329:      	movl	%r13d, 0x8(%r12)
 38fb32e:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb338:      	jmp	0x38fb2ac <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x13c>
 38fb33d:      	movq	%rdi, %rbp
 38fb340:      	movq	0x38(%rsp), %rcx
 38fb345:      	movq	(%rcx), %r12
 38fb348:      	cmpq	%r14, %rax
 38fb34b:      	jne	0x38fb3df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26f>
 38fb351:      	jmp	0x38fb422 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb356:      	movq	(%rsp), %rax
 38fb35a:      	movq	0x40(%rax), %rbp
 38fb35e:      	movl	0x48(%rax), %eax
 38fb361:      	testq	%rax, %rax
 38fb364:      	je	0x38fb3aa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a>
 38fb366:      	shlq	$0x4, %rax
 38fb36a:      	leaq	(%rax,%rax,4), %rbx
 38fb36e:      	leaq	-0x40(%rbp), %r12
 38fb372:      	movq	0x18(%rsp), %r13
 38fb377:      	jmp	0x38fb386 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x216>
 38fb379:      	nopl	(%rax)
 38fb380:      	addq	$-0x50, %rbx
 38fb384:      	je	0x38fb39b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22b>
 38fb386:      	movq	-0x50(%rbp,%rbx), %rdi
 38fb38b:      	leaq	(%r12,%rbx), %rax
 38fb38f:      	cmpq	%rdi, %rax
 38fb392:      	je	0x38fb380 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x210>
 38fb394:      	callq	0x828a640 <free@plt>
 38fb399:      	jmp	0x38fb380 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x210>
 38fb39b:      	movq	0x38(%rsp), %rax
 38fb3a0:      	movq	(%rax), %rbp
 38fb3a3:      	movq	0x8(%rsp), %r12
 38fb3a8:      	jmp	0x38fb3b4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x244>
 38fb3aa:      	movq	0x8(%rsp), %r12
 38fb3af:      	movq	0x18(%rsp), %r13
 38fb3b4:      	movq	0x258(%rsp), %rbx
 38fb3bc:      	cmpq	%r13, %rbp
 38fb3bf:      	je	0x38fb3c9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x259>
 38fb3c1:      	movq	%rbp, %rdi
 38fb3c4:      	callq	0x828a640 <free@plt>
 38fb3c9:      	movq	(%rsp), %rax
 38fb3cd:      	movq	%r12, 0x40(%rax)
 38fb3d1:      	movl	%ebx, 0x4c(%rax)
 38fb3d4:      	movq	%rax, %rbp
 38fb3d7:      	movl	0x48(%rax), %eax
 38fb3da:      	cmpq	%r14, %rax
 38fb3dd:      	je	0x38fb422 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b2>
 38fb3df:      	shlq	$0x4, %r14
 38fb3e3:      	leaq	(%r14,%r14,4), %rcx
 38fb3e7:      	shlq	$0x4, %rax
 38fb3eb:      	leaq	(%rax,%rax,4), %rax
 38fb3ef:      	subq	%rax, %rcx
 38fb3f2:      	leaq	0x10(%r12,%rax), %rax
 38fb3f7:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 38fb401:      	nopw	%cs:(%rax,%rax)
 38fb40b:      	nopl	(%rax,%rax)
 38fb410:      	movq	%rax, -0x10(%rax)
 38fb414:      	movq	%rdx, -0x8(%rax)
 38fb418:      	addq	$0x50, %rax
 38fb41c:      	addq	$-0x50, %rcx
 38fb420:      	jne	0x38fb410 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a0>
 38fb422:      	movl	%r15d, 0x48(%rbp)
 38fb426:      	movq	0x58(%rsp), %rsi
 38fb42b:      	leaq	0x140(%rsi), %rax
 38fb432:      	movq	0x148(%rsi), %rcx
 38fb439:      	movq	%rax, 0x88(%rsp)
 38fb441:      	cmpq	%rax, %rcx
 38fb444:      	je	0x38fb7f9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x689>
 38fb44a:      	movss	-0x2cc515a(%rip), %xmm3 # 0xc362f8 <.LCPI43_3>
 38fb452:      	movsd	-0x2ae645a(%rip), %xmm4 # 0xe15000 <.LCPI84_0>
 38fb45a:      	movapd	-0x2ae9702(%rip), %xmm5 # 0xe11d60 <.LCPI84_1>
 38fb462:      	jmp	0x38fb48d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x31d>
 38fb464:      	nopw	%cs:(%rax,%rax)
 38fb46e:      	nop
 38fb470:      	movq	0x8(%rsp), %rcx
 38fb475:      	movq	0x8(%rcx), %rcx
 38fb479:      	movq	0x58(%rsp), %rax
 38fb47e:      	addq	$0x140, %rax            # imm = 0x140
 38fb484:      	cmpq	%rax, %rcx
 38fb487:      	je	0x38fb7f9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x689>
 38fb48d:      	leaq	0x30(%rcx), %r13
 38fb491:      	movq	%rcx, 0x8(%rsp)
 38fb496:      	movq	0x38(%rcx), %rbp
 38fb49a:      	jmp	0x38fb4a4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x334>
 38fb49c:      	nopl	(%rax)
 38fb4a0:      	movq	0x8(%rbp), %rbp
 38fb4a4:      	cmpq	%r13, %rbp
 38fb4a7:      	je	0x38fb470 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x300>
 38fb4a9:      	movzwl	0x28(%rbp), %eax
 38fb4ad:      	movzbl	0x2a(%rbp), %r8d
 38fb4b2:      	shll	$0x10, %r8d
 38fb4b6:      	orl	%eax, %r8d
 38fb4b9:      	testl	%r8d, %r8d
 38fb4bc:      	je	0x38fb6f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x580>
 38fb4c2:      	movq	0x20(%rbp), %r9
 38fb4c6:      	shll	$0x5, %r8d
 38fb4ca:      	addq	%r9, %r8
 38fb4cd:      	movq	(%rsp), %rax
 38fb4d1:      	movq	0x10(%rax), %r10
 38fb4d5:      	movq	0x18(%rax), %r11
 38fb4d9:      	leaq	0x78(%r10), %rbx
 38fb4dd:      	jmp	0x38fb52d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3bd>
 38fb4df:      	movq	0x8(%rax), %rax
 38fb4e3:      	movsd	0x10(%rax), %xmm1
 38fb4e8:      	unpcklps	%xmm4, %xmm1            # xmm1 = xmm1[0],xmm4[0],xmm1[1],xmm4[1]
 38fb4eb:      	subpd	%xmm5, %xmm1
 38fb4ef:      	movapd	%xmm1, %xmm2
 38fb4f3:      	unpckhpd	%xmm1, %xmm2            # xmm2 = xmm2[1],xmm1[1]
 38fb4f7:      	addsd	%xmm1, %xmm2
 38fb4fb:      	divsd	%xmm2, %xmm0
 38fb4ff:      	cvtsd2ss	%xmm0, %xmm0
 38fb503:      	addss	0x84(%r14), %xmm0
 38fb50c:      	movss	%xmm0, 0x84(%r14)
 38fb515:      	nopw	%cs:(%rax,%rax)
 38fb51f:      	nop
 38fb520:      	addq	$0x20, %r9
 38fb524:      	cmpq	%r8, %r9
 38fb527:      	je	0x38fb6f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x580>
 38fb52d:      	cmpb	$0x5, (%r9)
 38fb531:      	jne	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb533:      	movslq	0x10(%r9), %rcx
 38fb537:      	testq	%rcx, %rcx
 38fb53a:      	js	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb53c:      	movq	0x80(%r10), %r12
 38fb543:      	testq	%r12, %r12
 38fb546:      	je	0x38fb5ba <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x44a>
 38fb548:      	movq	0x70(%r10), %r15
 38fb54c:      	movq	%rcx, %rsi
 38fb54f:      	cmpq	%r15, %rcx
 38fb552:      	jb	0x38fb55d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3ed>
 38fb554:      	movl	%ecx, %eax
 38fb556:      	xorl	%edx, %edx
 38fb558:      	divl	%r15d
 38fb55b:      	movl	%edx, %esi
 38fb55d:      	movq	0x68(%r10), %rax
 38fb561:      	movq	(%rax,%rsi,8), %rax
 38fb565:      	testq	%rax, %rax
 38fb568:      	je	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb56a:      	movq	(%rax), %r14
 38fb56d:      	cmpl	0x8(%r14), %ecx
 38fb571:      	je	0x38fb619 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb577:      	jmp	0x38fb590 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x420>
 38fb579:      	nopl	(%rax)
 38fb580:      	movl	%edi, %eax
 38fb582:      	xorl	%edx, %edx
 38fb584:      	divl	%r15d
 38fb587:      	cmpq	%rsi, %rdx
 38fb58a:      	jne	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb58c:      	cmpl	%edi, %ecx
 38fb58e:      	je	0x38fb5d1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x461>
 38fb590:      	movq	(%r14), %r14
 38fb593:      	testq	%r14, %r14
 38fb596:      	je	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb598:      	movslq	0x8(%r14), %rdi
 38fb59c:      	movq	%rdi, %rax
 38fb59f:      	orq	%r15, %rax
 38fb5a2:      	shrq	$0x20, %rax
 38fb5a6:      	je	0x38fb580 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x410>
 38fb5a8:      	movq	%rdi, %rax
 38fb5ab:      	xorl	%edx, %edx
 38fb5ad:      	divq	%r15
 38fb5b0:      	cmpq	%rsi, %rdx
 38fb5b3:      	je	0x38fb58c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x41c>
 38fb5b5:      	jmp	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb5ba:      	movq	%rbx, %rax
 38fb5bd:      	nopl	(%rax)
 38fb5c0:      	movq	(%rax), %rax
 38fb5c3:      	testq	%rax, %rax
 38fb5c6:      	je	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb5cc:      	cmpl	0x8(%rax), %ecx
 38fb5cf:      	jne	0x38fb5c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x450>
 38fb5d1:      	testq	%r12, %r12
 38fb5d4:      	je	0x38fb60b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x49b>
 38fb5d6:      	movq	0x68(%r10), %rsi
 38fb5da:      	movq	0x70(%r10), %rdi
 38fb5de:      	movq	%rcx, %rdx
 38fb5e1:      	cmpq	%rdi, %rcx
 38fb5e4:      	jb	0x38fb5ec <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x47c>
 38fb5e6:      	movl	%ecx, %eax
 38fb5e8:      	xorl	%edx, %edx
 38fb5ea:      	divl	%edi
 38fb5ec:      	movq	(%rsi,%rdx,8), %rax
 38fb5f0:      	movq	(%rax), %r14
 38fb5f3:      	cmpl	0x8(%r14), %ecx
 38fb5f7:      	je	0x38fb619 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb5f9:      	nopl	(%rax)
 38fb600:      	movq	(%r14), %r14
 38fb603:      	cmpl	0x8(%r14), %ecx
 38fb607:      	jne	0x38fb600 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x490>
 38fb609:      	jmp	0x38fb619 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a9>
 38fb60b:      	movq	%rbx, %r14
 38fb60e:      	nop
 38fb610:      	movq	(%r14), %r14
 38fb613:      	cmpl	0x8(%r14), %ecx
 38fb617:      	jne	0x38fb610 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x4a0>
 38fb619:      	movl	0x44(%rbp), %eax
 38fb61c:      	addl	$-0xe, %eax
 38fb61f:      	cmpw	$0x5, %ax
 38fb623:      	jb	0x38fb520 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3b0>
 38fb629:      	movq	(%r11), %rax
 38fb62c:      	movapd	%xmm3, %xmm0
 38fb630:      	testq	%rax, %rax
 38fb633:      	je	0x38fb503 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x393>
 38fb639:      	movl	0xb0(%rax), %edx
 38fb63f:      	xorpd	%xmm0, %xmm0
 38fb643:      	testl	%edx, %edx
 38fb645:      	je	0x38fb4df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb64b:      	movq	0x18(%rbp), %rdi
 38fb64f:      	movq	0xa0(%rax), %rcx
 38fb656:      	movl	%edi, %r15d
 38fb659:      	shrl	$0x4, %r15d
 38fb65d:      	movl	%edi, %esi
 38fb65f:      	shrl	$0x9, %esi
 38fb662:      	xorl	%r15d, %esi
 38fb665:      	decl	%edx
 38fb667:      	andl	%edx, %esi
 38fb669:      	movl	%esi, %r15d
 38fb66c:      	shll	$0x4, %r15d
 38fb670:      	movq	(%rcx,%r15), %r12
 38fb674:      	cmpq	%r12, %rdi
 38fb677:      	jne	0x38fb6b5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x545>
 38fb679:      	shlq	$0x4, %rsi
 38fb67d:      	movl	0x8(%rcx,%rsi), %ecx
 38fb681:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 38fb686:      	cmpq	%rdx, %rcx
 38fb689:      	je	0x38fb4df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb68f:      	movq	0x8(%rax), %rdx
 38fb693:      	leaq	(%rcx,%rcx,2), %rcx
 38fb697:      	movsd	0x10(%rdx,%rcx,8), %xmm1
 38fb69d:      	unpcklps	%xmm4, %xmm1            # xmm1 = xmm1[0],xmm4[0],xmm1[1],xmm4[1]
 38fb6a0:      	subpd	%xmm5, %xmm1
 38fb6a4:      	movapd	%xmm1, %xmm0
 38fb6a8:      	unpckhpd	%xmm1, %xmm0            # xmm0 = xmm0[1],xmm1[1]
 38fb6ac:      	addsd	%xmm1, %xmm0
 38fb6b0:      	jmp	0x38fb4df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb6b5:      	movl	$0x1, %r15d
 38fb6bb:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 38fb6c2:      	je	0x38fb4df <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x36f>
 38fb6c8:      	addl	%r15d, %esi
 38fb6cb:      	incl	%r15d
 38fb6ce:      	andl	%edx, %esi
 38fb6d0:      	movq	%rsi, %r12
 38fb6d3:      	shlq	$0x4, %r12
 38fb6d7:      	movq	(%rcx,%r12), %r12
 38fb6db:      	cmpq	%r12, %rdi
 38fb6de:      	je	0x38fb679 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x509>
 38fb6e0:      	jmp	0x38fb6bb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x54b>
 38fb6e2:      	nopw	%cs:(%rax,%rax)
 38fb6ec:      	nopl	(%rax)
 38fb6f0:      	movq	0x30(%rbp), %rax
 38fb6f4:      	cmpq	$0x8, %rax
 38fb6f8:      	jb	0x38fb7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb6fe:      	movl	%eax, %ecx
 38fb700:      	andl	$0x7, %ecx
 38fb703:      	cmpq	$0x3, %rcx
 38fb707:      	je	0x38fb720 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5b0>
 38fb709:      	testq	%rcx, %rcx
 38fb70c:      	jne	0x38fb7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb712:      	leaq	0x30(%rbp), %r15
 38fb716:      	movq	%rax, 0x30(%rbp)
 38fb71a:      	leaq	0x38(%rbp), %rbx
 38fb71e:      	jmp	0x38fb759 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e9>
 38fb720:      	andq	$-0x8, %rax
 38fb724:      	movslq	(%rax), %rcx
 38fb727:      	testq	%rcx, %rcx
 38fb72a:      	je	0x38fb7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb730:      	leaq	0x10(%rax,%rcx,8), %rbx
 38fb735:      	addq	$0x10, %rax
 38fb739:      	movq	%rax, %r15
 38fb73c:      	jmp	0x38fb759 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e9>
 38fb73e:      	movq	(%r14), %rax
 38fb741:      	movl	%edx, %ecx
 38fb743:      	movq	%r12, (%rax,%rcx,8)
 38fb747:      	incl	0x8(%r14)
 38fb74b:      	nopl	(%rax,%rax)
 38fb750:      	addq	$0x8, %r15
 38fb754:      	cmpq	%rbx, %r15
 38fb757:      	je	0x38fb7d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x660>
 38fb759:      	movq	(%r15), %r12
 38fb75c:      	movq	(%r12), %rax
 38fb760:      	testb	$0x4, %al
 38fb762:      	je	0x38fb750 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb764:      	andq	$-0x8, %rax
 38fb768:      	je	0x38fb750 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb76a:      	cmpl	$0x4, 0x8(%rax)
 38fb76e:      	jne	0x38fb750 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb770:      	movslq	0x10(%rax), %rax
 38fb774:      	testq	%rax, %rax
 38fb777:      	js	0x38fb750 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5e0>
 38fb779:      	movq	0x38(%rsp), %rcx
 38fb77e:      	movq	(%rcx), %rcx
 38fb781:      	leaq	(%rax,%rax,4), %rax
 38fb785:      	shlq	$0x4, %rax
 38fb789:      	leaq	(%rcx,%rax), %r14
 38fb78d:      	movl	0x8(%rcx,%rax), %edx
 38fb791:      	cmpl	0xc(%rcx,%rax), %edx
 38fb795:      	jb	0x38fb73e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5ce>
 38fb797:      	incq	%rdx
 38fb79a:      	leaq	0x10(%r14), %rsi
 38fb79e:      	movl	$0x8, %ecx
 38fb7a3:      	movq	%r14, %rdi
 38fb7a6:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fb7ab:      	movapd	-0x2ae9a53(%rip), %xmm5 # 0xe11d60 <.LCPI84_1>
 38fb7b3:      	movsd	-0x2ae67bb(%rip), %xmm4 # 0xe15000 <.LCPI84_0>
 38fb7bb:      	movss	-0x2cc54cb(%rip), %xmm3 # 0xc362f8 <.LCPI43_3>
 38fb7c3:      	movl	0x8(%r14), %edx
 38fb7c7:      	jmp	0x38fb73e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x5ce>
 38fb7cc:      	nopl	(%rax)
 38fb7d0:      	testb	$0x4, (%rbp)
 38fb7d4:      	jne	0x38fb4a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb7da:      	nopw	(%rax,%rax)
 38fb7e0:      	testb	$0x8, 0x2c(%rbp)
 38fb7e4:      	je	0x38fb4a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb7ea:      	movq	0x8(%rbp), %rbp
 38fb7ee:      	testb	$0x8, 0x2c(%rbp)
 38fb7f2:      	jne	0x38fb7ea <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x67a>
 38fb7f4:      	jmp	0x38fb4a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x330>
 38fb7f9:      	movq	(%rsp), %r12
 38fb7fd:      	movq	(%r12), %rax
 38fb801:      	movq	0x10(%rax), %rcx
 38fb805:      	subq	0x8(%rax), %rcx
 38fb809:      	shrq	$0x3, %rcx
 38fb80d:      	imull	$0xcccccccd, %ecx, %ecx # imm = 0xCCCCCCCD
 38fb813:      	subl	0x20(%rax), %ecx
 38fb816:      	movq	%rcx, 0x20(%rsp)
 38fb81b:      	leaq	0x5c8(%r12), %rax
 38fb823:      	movq	%rax, 0x18(%rsp)
 38fb828:      	movl	0x5d0(%r12), %eax
 38fb830:      	testq	%rax, %rax
 38fb833:      	je	0x38fb883 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x713>
 38fb835:      	cmpl	$0x1, %eax
 38fb838:      	je	0x38fba22 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8b2>
 38fb83e:      	leaq	0x5c8(%r12), %rcx
 38fb846:      	movq	(%rcx), %rbx
 38fb849:      	shlq	$0x3, %rax
 38fb84d:      	leaq	(%rax,%rax,8), %r14
 38fb851:      	leaq	-0x38(%rbx), %r15
 38fb855:      	jmp	0x38fb86e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6fe>
 38fb857:      	nopw	(%rax,%rax)
 38fb860:      	addq	$-0x48, %r14
 38fb864:      	cmpq	$0x48, %r14
 38fb868:      	je	0x38fba16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb86e:      	movq	-0x48(%rbx,%r14), %rdi
 38fb873:      	leaq	(%r15,%r14), %rax
 38fb877:      	cmpq	%rdi, %rax
 38fb87a:      	je	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6f0>
 38fb87c:      	callq	0x828a640 <free@plt>
 38fb881:      	jmp	0x38fb860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x6f0>
 38fb883:      	cmpl	$0x0, 0x5d4(%r12)
 38fb88c:      	je	0x38fb892 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x722>
 38fb88e:      	xorl	%eax, %eax
 38fb890:      	jmp	0x38fb8b6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x746>
 38fb892:      	movl	$0x1, %esi
 38fb897:      	leaq	0x5c8(%r12), %rdi
 38fb89f:      	callq	0x38febd0 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fb8a4:      	movl	0x5d0(%r12), %eax
 38fb8ac:      	cmpq	$0x1, %rax
 38fb8b0:      	je	0x38fba16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb8b6:      	leaq	0x5c8(%r12), %rcx
 38fb8be:      	movq	(%rcx), %rsi
 38fb8c1:      	leaq	(%rax,%rax,8), %rdi
 38fb8c5:      	shlq	$0x3, %rax
 38fb8c9:      	leaq	(%rax,%rax,8), %rcx
 38fb8cd:      	negq	%rcx
 38fb8d0:      	movabsq	$-0x1c71c71c71c71c71, %rdx # imm = 0xE38E38E38E38E38F
 38fb8da:      	movq	%rcx, %rax
 38fb8dd:      	mulq	%rdx
 38fb8e0:      	shrq	$0x6, %rdx
 38fb8e4:      	movl	%edx, %eax
 38fb8e6:      	notl	%eax
 38fb8e8:      	testb	$0x3, %al
 38fb8ea:      	jne	0x38fb8fe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x78e>
 38fb8ec:      	leaq	(%rsi,%rdi,8), %rax
 38fb8f0:      	cmpq	$0xd8, %rcx
 38fb8f7:      	jae	0x38fb955 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x7e5>
 38fb8f9:      	jmp	0x38fba16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb8fe:      	incl	%edx
 38fb900:      	andl	$0x3, %edx
 38fb903:      	leaq	0x10(%rsi,%rdi,8), %rax
 38fb908:      	xorps	%xmm0, %xmm0
 38fb90b:      	movabsq	$0x600000000, %rdi      # imm = 0x600000000
 38fb915:      	nopw	%cs:(%rax,%rax)
 38fb91f:      	nop
 38fb920:      	movups	%xmm0, 0x20(%rax)
 38fb924:      	movups	%xmm0, 0x10(%rax)
 38fb928:      	movups	%xmm0, (%rax)
 38fb92b:      	movq	$0x0, 0x30(%rax)
 38fb933:      	movq	%rax, -0x10(%rax)
 38fb937:      	movq	%rdi, -0x8(%rax)
 38fb93b:      	addq	$0x48, %rax
 38fb93f:      	decq	%rdx
 38fb942:      	jne	0x38fb920 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x7b0>
 38fb944:      	addq	$-0x10, %rax
 38fb948:      	cmpq	$0xd8, %rcx
 38fb94f:      	jb	0x38fba16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8a6>
 38fb955:      	addq	$0x58, %rax
 38fb959:      	xorps	%xmm0, %xmm0
 38fb95c:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 38fb966:      	nopw	%cs:(%rax,%rax)
 38fb970:      	leaq	-0x48(%rax), %rdx
 38fb974:      	movups	%xmm0, -0x28(%rax)
 38fb978:      	movups	%xmm0, -0x38(%rax)
 38fb97c:      	movups	%xmm0, -0x48(%rax)
 38fb980:      	movq	$0x0, -0x18(%rax)
 38fb988:      	movq	%rdx, -0x58(%rax)
 38fb98c:      	movq	%rcx, -0x50(%rax)
 38fb990:      	movups	%xmm0, (%rax)
 38fb993:      	movups	%xmm0, 0x10(%rax)
 38fb997:      	movups	%xmm0, 0x20(%rax)
 38fb99b:      	movq	$0x0, 0x30(%rax)
 38fb9a3:      	movq	%rax, -0x10(%rax)
 38fb9a7:      	movq	%rcx, -0x8(%rax)
 38fb9ab:      	leaq	0x48(%rax), %rdx
 38fb9af:      	movups	%xmm0, 0x48(%rax)
 38fb9b3:      	movups	%xmm0, 0x58(%rax)
 38fb9b7:      	movups	%xmm0, 0x68(%rax)
 38fb9bb:      	movq	$0x0, 0x78(%rax)
 38fb9c3:      	movq	%rdx, 0x38(%rax)
 38fb9c7:      	movq	%rcx, 0x40(%rax)
 38fb9cb:      	leaq	0x80(%rax), %rdx
 38fb9d2:      	leaq	0x90(%rax), %rdi
 38fb9d9:      	movups	%xmm0, 0xb0(%rax)
 38fb9e0:      	movups	%xmm0, 0xa0(%rax)
 38fb9e7:      	movups	%xmm0, 0x90(%rax)
 38fb9ee:      	movq	$0x0, 0xc0(%rax)
 38fb9f9:      	movq	%rdi, 0x80(%rax)
 38fba00:      	movq	%rcx, 0x88(%rax)
 38fba07:      	addq	$0x120, %rax            # imm = 0x120
 38fba0d:      	cmpq	%rsi, %rdx
 38fba10:      	jne	0x38fb970 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x800>
 38fba16:      	movl	$0x1, 0x5d0(%r12)
 38fba22:      	leaq	0x680(%r12), %rax
 38fba2a:      	movq	%rax, 0x40(%rsp)
 38fba2f:      	movl	0x688(%r12), %eax
 38fba37:      	testq	%rax, %rax
 38fba3a:      	je	0x38fba83 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x913>
 38fba3c:      	cmpl	$0x1, %eax
 38fba3f:      	je	0x38fbc22 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xab2>
 38fba45:      	leaq	0x680(%r12), %rcx
 38fba4d:      	movq	(%rcx), %rbx
 38fba50:      	shlq	$0x3, %rax
 38fba54:      	leaq	(%rax,%rax,8), %r14
 38fba58:      	leaq	-0x38(%rbx), %r15
 38fba5c:      	jmp	0x38fba6e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8fe>
 38fba5e:      	nop
 38fba60:      	addq	$-0x48, %r14
 38fba64:      	cmpq	$0x48, %r14
 38fba68:      	je	0x38fbc16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fba6e:      	movq	-0x48(%rbx,%r14), %rdi
 38fba73:      	leaq	(%r15,%r14), %rax
 38fba77:      	cmpq	%rdi, %rax
 38fba7a:      	je	0x38fba60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8f0>
 38fba7c:      	callq	0x828a640 <free@plt>
 38fba81:      	jmp	0x38fba60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x8f0>
 38fba83:      	cmpl	$0x0, 0x68c(%r12)
 38fba8c:      	je	0x38fba92 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x922>
 38fba8e:      	xorl	%eax, %eax
 38fba90:      	jmp	0x38fbab6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x946>
 38fba92:      	movl	$0x1, %esi
 38fba97:      	leaq	0x680(%r12), %rdi
 38fba9f:      	callq	0x38febd0 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fbaa4:      	movl	0x688(%r12), %eax
 38fbaac:      	cmpq	$0x1, %rax
 38fbab0:      	je	0x38fbc16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbab6:      	leaq	0x680(%r12), %rcx
 38fbabe:      	movq	(%rcx), %rsi
 38fbac1:      	leaq	(%rax,%rax,8), %rdi
 38fbac5:      	shlq	$0x3, %rax
 38fbac9:      	leaq	(%rax,%rax,8), %rcx
 38fbacd:      	negq	%rcx
 38fbad0:      	movabsq	$-0x1c71c71c71c71c71, %rdx # imm = 0xE38E38E38E38E38F
 38fbada:      	movq	%rcx, %rax
 38fbadd:      	mulq	%rdx
 38fbae0:      	shrq	$0x6, %rdx
 38fbae4:      	movl	%edx, %eax
 38fbae6:      	notl	%eax
 38fbae8:      	testb	$0x3, %al
 38fbaea:      	jne	0x38fbafe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x98e>
 38fbaec:      	leaq	(%rsi,%rdi,8), %rax
 38fbaf0:      	cmpq	$0xd8, %rcx
 38fbaf7:      	jae	0x38fbb55 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9e5>
 38fbaf9:      	jmp	0x38fbc16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbafe:      	incl	%edx
 38fbb00:      	andl	$0x3, %edx
 38fbb03:      	leaq	0x10(%rsi,%rdi,8), %rax
 38fbb08:      	xorps	%xmm0, %xmm0
 38fbb0b:      	movabsq	$0x600000000, %rdi      # imm = 0x600000000
 38fbb15:      	nopw	%cs:(%rax,%rax)
 38fbb1f:      	nop
 38fbb20:      	movups	%xmm0, 0x20(%rax)
 38fbb24:      	movups	%xmm0, 0x10(%rax)
 38fbb28:      	movups	%xmm0, (%rax)
 38fbb2b:      	movq	$0x0, 0x30(%rax)
 38fbb33:      	movq	%rax, -0x10(%rax)
 38fbb37:      	movq	%rdi, -0x8(%rax)
 38fbb3b:      	addq	$0x48, %rax
 38fbb3f:      	decq	%rdx
 38fbb42:      	jne	0x38fbb20 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x9b0>
 38fbb44:      	addq	$-0x10, %rax
 38fbb48:      	cmpq	$0xd8, %rcx
 38fbb4f:      	jb	0x38fbc16 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaa6>
 38fbb55:      	addq	$0x58, %rax
 38fbb59:      	xorps	%xmm0, %xmm0
 38fbb5c:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 38fbb66:      	nopw	%cs:(%rax,%rax)
 38fbb70:      	leaq	-0x48(%rax), %rdx
 38fbb74:      	movups	%xmm0, -0x28(%rax)
 38fbb78:      	movups	%xmm0, -0x38(%rax)
 38fbb7c:      	movups	%xmm0, -0x48(%rax)
 38fbb80:      	movq	$0x0, -0x18(%rax)
 38fbb88:      	movq	%rdx, -0x58(%rax)
 38fbb8c:      	movq	%rcx, -0x50(%rax)
 38fbb90:      	movups	%xmm0, (%rax)
 38fbb93:      	movups	%xmm0, 0x10(%rax)
 38fbb97:      	movups	%xmm0, 0x20(%rax)
 38fbb9b:      	movq	$0x0, 0x30(%rax)
 38fbba3:      	movq	%rax, -0x10(%rax)
 38fbba7:      	movq	%rcx, -0x8(%rax)
 38fbbab:      	leaq	0x48(%rax), %rdx
 38fbbaf:      	movups	%xmm0, 0x48(%rax)
 38fbbb3:      	movups	%xmm0, 0x58(%rax)
 38fbbb7:      	movups	%xmm0, 0x68(%rax)
 38fbbbb:      	movq	$0x0, 0x78(%rax)
 38fbbc3:      	movq	%rdx, 0x38(%rax)
 38fbbc7:      	movq	%rcx, 0x40(%rax)
 38fbbcb:      	leaq	0x80(%rax), %rdx
 38fbbd2:      	leaq	0x90(%rax), %rdi
 38fbbd9:      	movups	%xmm0, 0xb0(%rax)
 38fbbe0:      	movups	%xmm0, 0xa0(%rax)
 38fbbe7:      	movups	%xmm0, 0x90(%rax)
 38fbbee:      	movq	$0x0, 0xc0(%rax)
 38fbbf9:      	movq	%rdi, 0x80(%rax)
 38fbc00:      	movq	%rcx, 0x88(%rax)
 38fbc07:      	addq	$0x120, %rax            # imm = 0x120
 38fbc0d:      	cmpq	%rsi, %rdx
 38fbc10:      	jne	0x38fbb70 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xa00>
 38fbc16:      	movl	$0x1, 0x688(%r12)
 38fbc22:      	leaq	0x550(%r12), %r14
 38fbc2a:      	movslq	0x20(%rsp), %rbx
 38fbc2f:      	movq	0x558(%r12), %rdi
 38fbc37:      	cmpq	%rbx, %rdi
 38fbc3a:      	je	0x38fbc82 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb12>
 38fbc3c:      	ja	0x38fbc7a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb0a>
 38fbc3e:      	cmpq	%rbx, 0x560(%r12)
 38fbc46:      	jae	0x38fbc68 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xaf8>
 38fbc48:      	leaq	0x568(%r12), %rsi
 38fbc50:      	movl	$0x1, %ecx
 38fbc55:      	movq	%r14, %rdi
 38fbc58:      	movq	%rbx, %rdx
 38fbc5b:      	callq	0x40f8880 <_ZN4llvm15SmallVectorBaseImE8grow_podEPvmm>
 38fbc60:      	movq	0x558(%r12), %rdi
 38fbc68:      	movq	%rbx, %rdx
 38fbc6b:      	subq	%rdi, %rdx
 38fbc6e:      	je	0x38fbc7a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb0a>
 38fbc70:      	addq	(%r14), %rdi
 38fbc73:      	xorl	%esi, %esi
 38fbc75:      	callq	0x828ab90 <memset@plt>
 38fbc7a:      	movq	%rbx, 0x558(%r12)
 38fbc82:      	leaq	0x578(%r12), %rax
 38fbc8a:      	movq	%rax, 0xb8(%rsp)
 38fbc92:      	movl	0x580(%r12), %edi
 38fbc9a:      	cmpq	%rdi, %rbx
 38fbc9d:      	je	0x38fbd02 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb92>
 38fbc9f:      	jb	0x38fbcf5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb85>
 38fbca1:      	movl	0x584(%r12), %eax
 38fbca9:      	cmpq	%rax, %rbx
 38fbcac:      	jbe	0x38fbcd3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb63>
 38fbcae:      	leaq	0x588(%r12), %rsi
 38fbcb6:      	movl	$0x4, %ecx
 38fbcbb:      	leaq	0x578(%r12), %rdi
 38fbcc3:      	movq	%rbx, %rdx
 38fbcc6:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fbccb:      	movl	0x580(%r12), %edi
 38fbcd3:      	movq	%rbx, %rdx
 38fbcd6:      	subq	%rdi, %rdx
 38fbcd9:      	je	0x38fbcf5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xb85>
 38fbcdb:      	shlq	$0x2, %rdi
 38fbcdf:      	leaq	0x578(%r12), %rax
 38fbce7:      	addq	(%rax), %rdi
 38fbcea:      	shlq	$0x2, %rdx
 38fbcee:      	xorl	%esi, %esi
 38fbcf0:      	callq	0x828ab90 <memset@plt>
 38fbcf5:      	movq	0x20(%rsp), %rax
 38fbcfa:      	movl	%eax, 0x580(%r12)
 38fbd02:      	movq	%rbx, 0x8(%rsp)
 38fbd07:      	movq	0x18(%rsp), %rax
 38fbd0c:      	movq	(%rax), %r13
 38fbd0f:      	movl	0x40(%r13), %ecx
 38fbd13:      	andq	$0x3f, %rcx
 38fbd17:      	je	0x38fbd35 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbc5>
 38fbd19:      	movq	$-0x1, %rax
 38fbd20:      	shlq	%cl, %rax
 38fbd23:      	notq	%rax
 38fbd26:      	movq	(%r13), %rcx
 38fbd2a:      	movl	0x8(%r13), %edi
 38fbd2e:      	andq	%rax, -0x8(%rcx,%rdi,8)
 38fbd33:      	jmp	0x38fbd39 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbc9>
 38fbd35:      	movl	0x8(%r13), %edi
 38fbd39:      	movl	%edi, %ebx
 38fbd3b:      	movq	0x20(%rsp), %r15
 38fbd40:      	movl	%r15d, 0x40(%r13)
 38fbd44:      	leal	0x3f(%r15), %esi
 38fbd48:      	shrl	$0x6, %esi
 38fbd4b:      	cmpl	%edi, %esi
 38fbd4d:      	movq	%rsi, 0x28(%rsp)
 38fbd52:      	movl	%r15d, %ebp
 38fbd55:      	je	0x38fbd95 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc25>
 38fbd57:      	movl	%esi, %eax
 38fbd59:      	jb	0x38fbd8f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc1f>
 38fbd5b:      	movq	%rsi, %r14
 38fbd5e:      	subq	%rdi, %r14
 38fbd61:      	movl	%r15d, %ebp
 38fbd64:      	cmpl	0xc(%r13), %esi
 38fbd68:      	ja	0x38fe1f8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3088>
 38fbd6e:      	shlq	$0x3, %rdi
 38fbd72:      	addq	(%r13), %rdi
 38fbd76:      	leal	(,%r14,8), %edx
 38fbd7e:      	xorl	%esi, %esi
 38fbd80:      	callq	0x828ab90 <memset@plt>
 38fbd85:      	addl	%r14d, %ebx
 38fbd88:      	movl	%ebx, %eax
 38fbd8a:      	movq	0x28(%rsp), %rsi
 38fbd8f:      	movl	%eax, 0x8(%r13)
 38fbd93:      	movl	%eax, %ebx
 38fbd95:      	andl	$0x3f, %ebp
 38fbd98:      	je	0x38fbdb4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc44>
 38fbd9a:      	movq	$-0x1, %rax
 38fbda1:      	movl	%ebp, %ecx
 38fbda3:      	shlq	%cl, %rax
 38fbda6:      	notq	%rax
 38fbda9:      	movq	(%r13), %rcx
 38fbdad:      	movl	%ebx, %edx
 38fbdaf:      	andq	%rax, -0x8(%rcx,%rdx,8)
 38fbdb4:      	movq	0x40(%rsp), %rax
 38fbdb9:      	movq	(%rax), %r13
 38fbdbc:      	movl	0x40(%r13), %ecx
 38fbdc0:      	andq	$0x3f, %rcx
 38fbdc4:      	je	0x38fbde2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc72>
 38fbdc6:      	movq	$-0x1, %rax
 38fbdcd:      	shlq	%cl, %rax
 38fbdd0:      	notq	%rax
 38fbdd3:      	movq	(%r13), %rcx
 38fbdd7:      	movl	0x8(%r13), %edi
 38fbddb:      	andq	%rax, -0x8(%rcx,%rdi,8)
 38fbde0:      	jmp	0x38fbde6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc76>
 38fbde2:      	movl	0x8(%r13), %edi
 38fbde6:      	movl	%edi, %ebx
 38fbde8:      	movl	%r15d, 0x40(%r13)
 38fbdec:      	movl	%esi, %eax
 38fbdee:      	movl	%r15d, %ebp
 38fbdf1:      	cmpl	%edi, %esi
 38fbdf3:      	je	0x38fbe2f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcbf>
 38fbdf5:      	movl	%r15d, %ebp
 38fbdf8:      	movl	%esi, %eax
 38fbdfa:      	jb	0x38fbe2b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcbb>
 38fbdfc:      	movq	%rsi, %r14
 38fbdff:      	subq	%rdi, %r14
 38fbe02:      	movl	%r15d, %ebp
 38fbe05:      	cmpl	0xc(%r13), %esi
 38fbe09:      	ja	0x38fe21d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x30ad>
 38fbe0f:      	shlq	$0x3, %rdi
 38fbe13:      	addq	(%r13), %rdi
 38fbe17:      	leal	(,%r14,8), %edx
 38fbe1f:      	xorl	%esi, %esi
 38fbe21:      	callq	0x828ab90 <memset@plt>
 38fbe26:      	addl	%r14d, %ebx
 38fbe29:      	movl	%ebx, %eax
 38fbe2b:      	movl	%eax, 0x8(%r13)
 38fbe2f:      	andl	$0x3f, %ebp
 38fbe32:      	je	0x38fbe4e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xcde>
 38fbe34:      	movq	$-0x1, %rdx
 38fbe3b:      	movl	%ebp, %ecx
 38fbe3d:      	shlq	%cl, %rdx
 38fbe40:      	notq	%rdx
 38fbe43:      	movq	(%r13), %rcx
 38fbe47:      	movl	%eax, %eax
 38fbe49:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fbe4e:      	movq	(%rsp), %rbp
 38fbe52:      	leaq	0x788(%rbp), %rax
 38fbe59:      	movq	%rax, 0x78(%rsp)
 38fbe5e:      	movl	0x790(%rbp), %ecx
 38fbe64:      	movq	0x8(%rsp), %r13
 38fbe69:      	cmpq	%rcx, %r13
 38fbe6c:      	je	0x38fc20d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x109d>
 38fbe72:      	jae	0x38fbf3b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xdcb>
 38fbe78:      	leaq	0x788(%rbp), %rax
 38fbe7f:      	movq	(%rax), %rbx
 38fbe82:      	imulq	$0xe8, %rcx, %r15
 38fbe89:      	imulq	$0xe8, %r13, %r12
 38fbe90:      	leaq	-0x3416f7(%rip), %r14   # 0x35ba7a0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fbe97:      	jmp	0x38fbebb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd4b>
 38fbe99:      	nopl	(%rax)
 38fbea0:      	movl	$0x0, 0xcc(%r13)
 38fbeab:      	addq	$-0xe8, %r15
 38fbeb2:      	cmpq	%r15, %r12
 38fbeb5:      	je	0x38fc202 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fbebb:      	movq	-0xe0(%rbx,%r15), %r13
 38fbec3:      	testq	%r13, %r13
 38fbec6:      	je	0x38fbeab <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd3b>
 38fbec8:      	cmpl	$0x0, 0xc8(%r13)
 38fbed0:      	je	0x38fbea0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd30>
 38fbed2:      	leaq	0x8(%r13), %rdi
 38fbed6:      	movq	%r14, %rsi
 38fbed9:      	xorl	%edx, %edx
 38fbedb:      	callq	0x35ba460 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fbee0:      	xorps	%xmm0, %xmm0
 38fbee3:      	movups	%xmm0, 0xb8(%r13)
 38fbeeb:      	movups	%xmm0, 0xa8(%r13)
 38fbef3:      	movups	%xmm0, 0x98(%r13)
 38fbefb:      	movups	%xmm0, 0x88(%r13)
 38fbf03:      	movl	$0x0, 0xc8(%r13)
 38fbf0e:      	movups	%xmm0, 0x18(%r13)
 38fbf13:      	movups	%xmm0, 0x8(%r13)
 38fbf18:      	movups	%xmm0, 0x38(%r13)
 38fbf1d:      	movups	%xmm0, 0x28(%r13)
 38fbf22:      	movups	%xmm0, 0x58(%r13)
 38fbf27:      	movups	%xmm0, 0x48(%r13)
 38fbf2c:      	movups	%xmm0, 0x78(%r13)
 38fbf31:      	movups	%xmm0, 0x68(%r13)
 38fbf36:      	jmp	0x38fbea0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xd30>
 38fbf3b:      	movl	0x794(%rbp), %eax
 38fbf41:      	cmpq	%rax, %r13
 38fbf44:      	jbe	0x38fc168 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xff8>
 38fbf4a:      	leaq	0x798(%rbp), %r15
 38fbf51:      	leaq	0x258(%rsp), %r8
 38fbf59:      	movl	$0xe8, %ecx
 38fbf5e:      	leaq	0x788(%rbp), %rdi
 38fbf65:      	movq	%r15, %rsi
 38fbf68:      	movq	%r13, %rdx
 38fbf6b:      	callq	0x40f84d0 <_ZN4llvm15SmallVectorBaseIjE13mallocForGrowEPvmmRm>
 38fbf70:      	movq	%rax, %r14
 38fbf73:      	movq	0x788(%rbp), %r12
 38fbf7a:      	movl	0x790(%rbp), %eax
 38fbf80:      	testq	%rax, %rax
 38fbf83:      	je	0x38fc195 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1025>
 38fbf89:      	movq	%r15, 0x48(%rsp)
 38fbf8e:      	imulq	$0xe8, %rax, %rbx
 38fbf95:      	leaq	-0xe8(%rbx), %r15
 38fbf9c:      	movq	%r15, %rax
 38fbf9f:      	shrq	$0x3, %rax
 38fbfa3:      	movabsq	$0x8d3dcb08d3dcb09, %rcx # imm = 0x8D3DCB08D3DCB09
 38fbfad:      	mulq	%rcx
 38fbfb0:      	movq	%r14, %r13
 38fbfb3:      	movq	%rdx, %r14
 38fbfb6:      	movl	%r14d, %eax
 38fbfb9:      	notl	%eax
 38fbfbb:      	movq	%r13, 0x30(%rsp)
 38fbfc0:      	movq	%r12, %rbp
 38fbfc3:      	testb	$0x3, %al
 38fbfc5:      	je	0x38fc003 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xe93>
 38fbfc7:      	incl	%r14d
 38fbfca:      	andl	$0x3, %r14d
 38fbfce:      	movq	0x30(%rsp), %r13
 38fbfd3:      	movq	%r12, %rbp
 38fbfd6:      	nopw	%cs:(%rax,%rax)
 38fbfe0:      	movl	$0xe8, %edx
 38fbfe5:      	movq	%r13, %rdi
 38fbfe8:      	movq	%rbp, %rsi
 38fbfeb:      	callq	0x828ac50 <memcpy@plt>
 38fbff0:      	addq	$0xe8, %rbp
 38fbff7:      	addq	$0xe8, %r13
 38fbffe:      	decq	%r14
 38fc001:      	jne	0x38fbfe0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xe70>
 38fc003:      	cmpq	$0x2b8, %r15            # imm = 0x2B8
 38fc00a:      	jb	0x38fc096 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf26>
 38fc010:      	addq	%rbx, %r12
 38fc013:      	xorl	%ebx, %ebx
 38fc015:      	nopw	%cs:(%rax,%rax)
 38fc01f:      	nop
 38fc020:      	leaq	(%r13,%rbx), %rdi
 38fc025:      	leaq	(%rbp,%rbx), %rsi
 38fc02a:      	movl	$0xe8, %edx
 38fc02f:      	callq	0x828ac50 <memcpy@plt>
 38fc034:      	leaq	0xe8(%r13,%rbx), %rdi
 38fc03c:      	leaq	0xe8(%rbp,%rbx), %rsi
 38fc044:      	movl	$0xe8, %edx
 38fc049:      	callq	0x828ac50 <memcpy@plt>
 38fc04e:      	leaq	0x1d0(%r13,%rbx), %rdi
 38fc056:      	leaq	0x1d0(%rbp,%rbx), %rsi
 38fc05e:      	movl	$0xe8, %edx
 38fc063:      	callq	0x828ac50 <memcpy@plt>
 38fc068:      	leaq	0x2b8(%r13,%rbx), %rdi
 38fc070:      	leaq	0x2b8(%rbp,%rbx), %rsi
 38fc078:      	movl	$0xe8, %edx
 38fc07d:      	callq	0x828ac50 <memcpy@plt>
 38fc082:      	leaq	0x3a0(%rbp,%rbx), %rax
 38fc08a:      	addq	$0x3a0, %rbx            # imm = 0x3A0
 38fc091:      	cmpq	%r12, %rax
 38fc094:      	jne	0x38fc020 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xeb0>
 38fc096:      	movq	(%rsp), %rbp
 38fc09a:      	movq	0x788(%rbp), %r12
 38fc0a1:      	movl	0x790(%rbp), %eax
 38fc0a7:      	testq	%rax, %rax
 38fc0aa:      	je	0x38fc186 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1016>
 38fc0b0:      	imulq	$0xe8, %rax, %rbx
 38fc0b7:      	leaq	-0x34191e(%rip), %r14   # 0x35ba7a0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fc0be:      	movq	0x8(%rsp), %r13
 38fc0c3:      	jmp	0x38fc0e8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf78>
 38fc0c5:      	nopw	%cs:(%rax,%rax)
 38fc0cf:      	nop
 38fc0d0:      	movl	$0x0, 0xcc(%r15)
 38fc0db:      	addq	$-0xe8, %rbx
 38fc0e2:      	je	0x38fc17c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x100c>
 38fc0e8:      	movq	-0xe0(%r12,%rbx), %r15
 38fc0f0:      	testq	%r15, %r15
 38fc0f3:      	je	0x38fc0db <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf6b>
 38fc0f5:      	cmpl	$0x0, 0xc8(%r15)
 38fc0fd:      	je	0x38fc0d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf60>
 38fc0ff:      	leaq	0x8(%r15), %rdi
 38fc103:      	movq	%r14, %rsi
 38fc106:      	xorl	%edx, %edx
 38fc108:      	callq	0x35ba460 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fc10d:      	xorps	%xmm0, %xmm0
 38fc110:      	movups	%xmm0, 0xb8(%r15)
 38fc118:      	movups	%xmm0, 0xa8(%r15)
 38fc120:      	movups	%xmm0, 0x98(%r15)
 38fc128:      	movups	%xmm0, 0x88(%r15)
 38fc130:      	movl	$0x0, 0xc8(%r15)
 38fc13b:      	movups	%xmm0, 0x18(%r15)
 38fc140:      	movups	%xmm0, 0x8(%r15)
 38fc145:      	movups	%xmm0, 0x38(%r15)
 38fc14a:      	movups	%xmm0, 0x28(%r15)
 38fc14f:      	movups	%xmm0, 0x58(%r15)
 38fc154:      	movups	%xmm0, 0x48(%r15)
 38fc159:      	movups	%xmm0, 0x78(%r15)
 38fc15e:      	movups	%xmm0, 0x68(%r15)
 38fc163:      	jmp	0x38fc0d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xf60>
 38fc168:      	leaq	0x788(%rbp), %rax
 38fc16f:      	movq	(%rax), %r14
 38fc172:      	subq	%rcx, %r13
 38fc175:      	jne	0x38fc1c2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1052>
 38fc177:      	jmp	0x38fc202 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fc17c:      	movq	0x78(%rsp), %rax
 38fc181:      	movq	(%rax), %r12
 38fc184:      	jmp	0x38fc18b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x101b>
 38fc186:      	movq	0x8(%rsp), %r13
 38fc18b:      	movq	0x30(%rsp), %r14
 38fc190:      	movq	0x48(%rsp), %r15
 38fc195:      	movq	0x258(%rsp), %rbx
 38fc19d:      	cmpq	%r15, %r12
 38fc1a0:      	je	0x38fc1aa <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x103a>
 38fc1a2:      	movq	%r12, %rdi
 38fc1a5:      	callq	0x828a640 <free@plt>
 38fc1aa:      	movq	%r14, 0x788(%rbp)
 38fc1b1:      	movl	%ebx, 0x794(%rbp)
 38fc1b7:      	movl	0x790(%rbp), %ecx
 38fc1bd:      	subq	%rcx, %r13
 38fc1c0:      	je	0x38fc202 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1092>
 38fc1c2:      	imulq	$0xe8, %r13, %rax
 38fc1c9:      	addq	$-0xe8, %rax
 38fc1cf:      	shrq	$0x3, %rax
 38fc1d3:      	movabsq	$0x8d3dcb08d3dcb09, %rdx # imm = 0x8D3DCB08D3DCB09
 38fc1dd:      	mulq	%rdx
 38fc1e0:      	imulq	$0xe8, %rcx, %rax
 38fc1e7:      	addq	%rax, %r14
 38fc1ea:      	imulq	$0xe8, %rdx, %rdx
 38fc1f1:      	addq	$0xe8, %rdx
 38fc1f8:      	movq	%r14, %rdi
 38fc1fb:      	xorl	%esi, %esi
 38fc1fd:      	callq	0x828ab90 <memset@plt>
 38fc202:      	movq	0x20(%rsp), %rax
 38fc207:      	movl	%eax, 0x790(%rbp)
 38fc20d:      	leaq	0x268(%rsp), %rax
 38fc215:      	movq	%rax, 0x68(%rsp)
 38fc21a:      	movq	%rax, 0x258(%rsp)
 38fc222:      	movabsq	$0x1000000000, %rax     # imm = 0x1000000000
 38fc22c:      	movq	%rax, 0x260(%rsp)
 38fc234:      	movq	0x10(%rbp), %rcx
 38fc238:      	movl	0x80(%rcx), %edx
 38fc23e:      	xorl	%eax, %eax
 38fc240:      	cmpq	$0x11, %rdx
 38fc244:      	jb	0x38fc26b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x10fb>
 38fc246:      	leaq	0x258(%rsp), %rdi
 38fc24e:      	movl	$0x8, %ecx
 38fc253:      	leaq	0x268(%rsp), %rsi
 38fc25b:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc260:      	movq	0x10(%rbp), %rcx
 38fc264:      	movl	0x260(%rsp), %eax
 38fc26b:      	movq	0x78(%rcx), %rbx
 38fc26f:      	testq	%rbx, %rbx
 38fc272:      	je	0x38fc2d8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1168>
 38fc274:      	leaq	0x258(%rsp), %r14
 38fc27c:      	nopl	(%rax)
 38fc280:      	cmpl	0x264(%rsp), %eax
 38fc287:      	jae	0x38fc2b5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1145>
 38fc289:      	leaq	0x8(%rbx), %rcx
 38fc28d:      	movq	0x258(%rsp), %rdx
 38fc295:      	movl	%eax, %eax
 38fc297:      	movq	%rcx, (%rdx,%rax,8)
 38fc29b:      	movl	0x260(%rsp), %eax
 38fc2a2:      	incl	%eax
 38fc2a4:      	movl	%eax, 0x260(%rsp)
 38fc2ab:      	movq	(%rbx), %rbx
 38fc2ae:      	testq	%rbx, %rbx
 38fc2b1:      	jne	0x38fc280 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1110>
 38fc2b3:      	jmp	0x38fc2d8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1168>
 38fc2b5:      	movl	%eax, %edx
 38fc2b7:      	incq	%rdx
 38fc2ba:      	movl	$0x8, %ecx
 38fc2bf:      	movq	%r14, %rdi
 38fc2c2:      	leaq	0x268(%rsp), %rsi
 38fc2ca:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc2cf:      	movl	0x260(%rsp), %eax
 38fc2d6:      	jmp	0x38fc289 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1119>
 38fc2d8:      	testl	%eax, %eax
 38fc2da:      	je	0x38fc3b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fc2e0:      	movq	0x258(%rsp), %r12
 38fc2e8:      	movl	%eax, %ebx
 38fc2ea:      	leaq	(%r12,%rbx,8), %r15
 38fc2ee:      	bsrq	%rbx, %rdx
 38fc2f2:      	xorl	$0x3f, %edx
 38fc2f5:      	addl	%edx, %edx
 38fc2f7:      	xorq	$0x7e, %rdx
 38fc2fb:      	movq	%r12, %rdi
 38fc2fe:      	movq	%r15, %rsi
 38fc301:      	callq	0x38fecd0 <_ZSt16__introsort_loopIPPSt4pairIKiN4llvm12LiveIntervalEElN9__gnu_cxx5__ops15_Iter_comp_iterIZN12_GLOBAL__N_117StackSlotColoring15InitializeSlotsEvE3$_0EEEvT_SE_T0_T1_>
 38fc306:      	leaq	0x8(%r12), %rbp
 38fc30b:      	cmpl	$0x11, %ebx
 38fc30e:      	jb	0x38fc3a7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1237>
 38fc314:      	movq	%r15, 0x8(%rsp)
 38fc319:      	leaq	0x8(%r12), %rbx
 38fc31e:      	movl	$0x8, %r14d
 38fc324:      	movq	%r12, %r15
 38fc327:      	jmp	0x38fc35f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11ef>
 38fc329:      	nopl	(%rax)
 38fc330:      	cmpq	$0x9, %r14
 38fc334:      	jb	0x38fc3a1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1231>
 38fc336:      	movq	%rbp, %rdi
 38fc339:      	movq	%r12, %rsi
 38fc33c:      	movq	%r14, %rdx
 38fc33f:      	callq	0x828abc0 <memmove@plt>
 38fc344:      	movq	%r12, %rcx
 38fc347:      	movq	%r13, (%rcx)
 38fc34a:      	addq	$0x8, %r14
 38fc34e:      	addq	$0x8, %rbx
 38fc352:      	cmpq	$0x80, %r14
 38fc359:      	je	0x38fcbfe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a8e>
 38fc35f:      	movq	%r15, %rcx
 38fc362:      	leaq	(%r12,%r14), %r15
 38fc366:      	movq	(%r12,%r14), %r13
 38fc36a:      	movq	(%r12), %rdx
 38fc36e:      	movl	(%r13), %eax
 38fc372:      	cmpl	(%rdx), %eax
 38fc374:      	jl	0x38fc330 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11c0>
 38fc376:      	movq	(%rcx), %rdx
 38fc379:      	movq	%r15, %rcx
 38fc37c:      	cmpl	(%rdx), %eax
 38fc37e:      	jge	0x38fc347 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d7>
 38fc380:      	movq	%rbx, %rcx
 38fc383:      	nopw	%cs:(%rax,%rax)
 38fc38d:      	nopl	(%rax)
 38fc390:      	movq	%rdx, (%rcx)
 38fc393:      	movq	-0x10(%rcx), %rdx
 38fc397:      	addq	$-0x8, %rcx
 38fc39b:      	cmpl	(%rdx), %eax
 38fc39d:      	jl	0x38fc390 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1220>
 38fc39f:      	jmp	0x38fc347 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d7>
 38fc3a1:      	movq	%rdx, 0x8(%rcx)
 38fc3a5:      	jmp	0x38fc344 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x11d4>
 38fc3a7:      	cmpl	$0x1, %ebx
 38fc3aa:      	jne	0x38fe160 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ff0>
 38fc3b0:      	movl	0x260(%rsp), %eax
 38fc3b7:      	testq	%rax, %rax
 38fc3ba:      	movq	(%rsp), %rbp
 38fc3be:      	movq	0x20(%rsp), %r12
 38fc3c3:      	je	0x38fc8f6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1786>
 38fc3c9:      	movq	0x258(%rsp), %rsi
 38fc3d1:      	leaq	(%rsi,%rax,8), %rax
 38fc3d5:      	movq	%rax, 0x70(%rsp)
 38fc3da:      	xorps	%xmm0, %xmm0
 38fc3dd:      	jmp	0x38fc421 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x12b1>
 38fc3df:      	nop
 38fc3e0:      	movq	0x18(%rsp), %rax
 38fc3e5:      	movq	(%rax), %rax
 38fc3e8:      	leaq	(%r14,%r14,8), %rdx
 38fc3ec:      	movl	$0x1, %esi
 38fc3f1:      	movq	0x48(%rsp), %rcx
 38fc3f6:      	shlq	%cl, %rsi
 38fc3f9:      	movq	(%rax,%rdx,8), %rax
 38fc3fd:      	movq	0x8(%rsp), %rcx
 38fc402:      	shrl	$0x6, %ecx
 38fc405:      	orq	%rsi, (%rax,%rcx,8)
 38fc409:      	movq	(%rsp), %rbp
 38fc40d:      	movq	0x30(%rsp), %rsi
 38fc412:      	addq	$0x8, %rsi
 38fc416:      	cmpq	0x70(%rsp), %rsi
 38fc41b:      	je	0x38fc8f6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1786>
 38fc421:      	movq	(%rsi), %r15
 38fc424:      	movl	0x78(%r15), %edi
 38fc428:      	leal	(,%rdi,4), %r8d
 38fc430:      	sarl	$0x2, %r8d
 38fc434:      	movq	(%rbp), %rbx
 38fc438:      	movl	0x20(%rbx), %eax
 38fc43b:      	addl	%r8d, %eax
 38fc43e:      	movq	0x8(%rbx), %rcx
 38fc442:      	leaq	(%rax,%rax,4), %rdx
 38fc446:      	cmpq	$-0x1, 0x8(%rcx,%rdx,8)
 38fc44c:      	je	0x38fc412 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x12a2>
 38fc44e:      	movq	%rdi, 0x48(%rsp)
 38fc453:      	addq	$0x8, %r15
 38fc457:      	movq	0x30(%rbp), %r14
 38fc45b:      	cmpq	0x38(%rbp), %r14
 38fc45f:      	movq	%rsi, 0x30(%rsp)
 38fc464:      	movq	%r8, 0x8(%rsp)
 38fc469:      	je	0x38fc480 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1310>
 38fc46b:      	movq	%r15, (%r14)
 38fc46e:      	addq	$0x8, %r14
 38fc472:      	movq	%r14, 0x30(%rbp)
 38fc476:      	jmp	0x38fc538 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x13c8>
 38fc47b:      	nopl	(%rax,%rax)
 38fc480:      	movq	0x28(%rbp), %r13
 38fc484:      	subq	%r13, %r14
 38fc487:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 38fc491:      	cmpq	%rax, %r14
 38fc494:      	je	0x38fe242 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x30d2>
 38fc49a:      	movq	%r14, %rax
 38fc49d:      	sarq	$0x3, %rax
 38fc4a1:      	cmpq	$0x1, %rax
 38fc4a5:      	movq	%rax, %rcx
 38fc4a8:      	adcq	$0x0, %rcx
 38fc4ac:      	leaq	(%rcx,%rax), %r12
 38fc4b0:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 38fc4ba:      	cmpq	%rdx, %r12
 38fc4bd:      	cmovaeq	%rdx, %r12
 38fc4c1:      	addq	%rax, %rcx
 38fc4c4:      	cmovbq	%rdx, %r12
 38fc4c8:      	leaq	(,%r12,8), %rdi
 38fc4d0:      	callq	0x828a620 <_Znwm@plt>
 38fc4d5:      	movq	%rax, %rbp
 38fc4d8:      	movq	%r15, (%rax,%r14)
 38fc4dc:      	testq	%r14, %r14
 38fc4df:      	jle	0x38fc4ef <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x137f>
 38fc4e1:      	movq	%rbp, %rdi
 38fc4e4:      	movq	%r13, %rsi
 38fc4e7:      	movq	%r14, %rdx
 38fc4ea:      	callq	0x828ac50 <memcpy@plt>
 38fc4ef:      	testq	%r13, %r13
 38fc4f2:      	movq	(%rsp), %r15
 38fc4f6:      	je	0x38fc506 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1396>
 38fc4f8:      	movq	%r13, %rdi
 38fc4fb:      	movq	%r14, %rsi
 38fc4fe:      	callq	0x828a660 <_ZdlPvm@plt>
 38fc503:      	movq	(%r15), %rbx
 38fc506:      	addq	%rbp, %r14
 38fc509:      	addq	$0x8, %r14
 38fc50d:      	movq	%rbp, 0x28(%r15)
 38fc511:      	movq	%r14, 0x30(%r15)
 38fc515:      	leaq	(%rbp,%r12,8), %rax
 38fc51a:      	movq	%rax, 0x38(%r15)
 38fc51e:      	movq	0x8(%rbx), %rcx
 38fc522:      	movl	0x20(%rbx), %eax
 38fc525:      	movq	0x8(%rsp), %r8
 38fc52a:      	addl	%r8d, %eax
 38fc52d:      	movq	%r15, %rbp
 38fc530:      	movq	0x20(%rsp), %r12
 38fc535:      	xorps	%xmm0, %xmm0
 38fc538:      	leaq	(%rax,%rax,4), %rax
 38fc53c:      	movzbl	0x10(%rcx,%rax,8), %eax
 38fc541:      	movslq	%r8d, %rcx
 38fc544:      	movq	0x550(%rbp), %rdx
 38fc54b:      	movb	%al, (%rdx,%rcx)
 38fc54e:      	movq	(%rbp), %rax
 38fc552:      	movl	0x20(%rax), %edx
 38fc555:      	addl	%r8d, %edx
 38fc558:      	movq	0x8(%rax), %rsi
 38fc55c:      	leaq	(%rdx,%rdx,4), %rdx
 38fc560:      	movl	0x8(%rsi,%rdx,8), %edx
 38fc564:      	movq	0x578(%rbp), %rdi
 38fc56b:      	movl	%edx, (%rdi,%rcx,4)
 38fc56e:      	movl	0x20(%rax), %eax
 38fc571:      	addl	%r8d, %eax
 38fc574:      	leaq	(%rax,%rax,4), %rax
 38fc578:      	movzbl	0x15(%rsi,%rax,8), %r14d
 38fc57e:      	testq	%r14, %r14
 38fc581:      	je	0x38fc3e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc587:      	movq	(%rsp), %rbx
 38fc58b:      	movl	0x5d0(%rbx), %eax
 38fc591:      	cmpq	%r14, %rax
 38fc594:      	ja	0x38fc72f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15bf>
 38fc59a:      	leaq	0x1(%r14), %r13
 38fc59e:      	cmpl	%r14d, 0x5d4(%rbx)
 38fc5a5:      	ja	0x38fc5bd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x144d>
 38fc5a7:      	movq	0x18(%rsp), %rdi
 38fc5ac:      	movq	%r13, %rsi
 38fc5af:      	callq	0x38febd0 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fc5b4:      	xorps	%xmm0, %xmm0
 38fc5b7:      	movl	0x5d0(%rbx), %eax
 38fc5bd:      	cmpl	%eax, %r13d
 38fc5c0:      	movabsq	$0x600000000, %rsi      # imm = 0x600000000
 38fc5ca:      	je	0x38fc625 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x14b5>
 38fc5cc:      	movq	0x18(%rsp), %rcx
 38fc5d1:      	movq	(%rcx), %rdx
 38fc5d4:      	leal	(,%r14,8), %ecx
 38fc5dc:      	leaq	(%rcx,%rcx,8), %rcx
 38fc5e0:      	shlq	$0x3, %rax
 38fc5e4:      	leaq	(%rax,%rax,8), %rax
 38fc5e8:      	subq	%rax, %rcx
 38fc5eb:      	addq	$0x48, %rcx
 38fc5ef:      	leaq	0x10(%rdx,%rax), %rax
 38fc5f4:      	nopw	%cs:(%rax,%rax)
 38fc5fe:      	nop
 38fc600:      	movups	%xmm0, 0x20(%rax)
 38fc604:      	movups	%xmm0, 0x10(%rax)
 38fc608:      	movups	%xmm0, (%rax)
 38fc60b:      	movq	$0x0, 0x30(%rax)
 38fc613:      	movq	%rax, -0x10(%rax)
 38fc617:      	movq	%rsi, -0x8(%rax)
 38fc61b:      	addq	$0x48, %rax
 38fc61f:      	addq	$-0x48, %rcx
 38fc623:      	jne	0x38fc600 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1490>
 38fc625:      	movl	%r13d, 0x5d0(%rbx)
 38fc62c:      	movl	0x688(%rbx), %eax
 38fc632:      	cmpq	%rax, %r13
 38fc635:      	je	0x38fc72f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15bf>
 38fc63b:      	cmpl	%eax, %r13d
 38fc63e:      	jae	0x38fc695 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1525>
 38fc640:      	movq	0x40(%rsp), %rcx
 38fc645:      	movq	(%rcx), %rbx
 38fc648:      	leaq	-0x38(%rbx), %r15
 38fc64c:      	shlq	$0x3, %rax
 38fc650:      	leaq	(%rax,%rax,8), %r12
 38fc654:      	leaq	(%r14,%r14,8), %rax
 38fc658:      	leaq	0x48(,%rax,8), %rbp
 38fc660:      	jmp	0x38fc67d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x150d>
 38fc662:      	nopw	%cs:(%rax,%rax)
 38fc66c:      	nopl	(%rax)
 38fc670:      	addq	$-0x48, %r12
 38fc674:      	cmpq	%r12, %rbp
 38fc677:      	je	0x38fc71f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15af>
 38fc67d:      	movq	-0x48(%rbx,%r12), %rdi
 38fc682:      	leaq	(%r15,%r12), %rax
 38fc686:      	cmpq	%rdi, %rax
 38fc689:      	je	0x38fc670 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1500>
 38fc68b:      	callq	0x828a640 <free@plt>
 38fc690:      	xorps	%xmm0, %xmm0
 38fc693:      	jmp	0x38fc670 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1500>
 38fc695:      	cmpl	%r14d, 0x68c(%rbx)
 38fc69c:      	ja	0x38fc6b4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1544>
 38fc69e:      	movq	0x40(%rsp), %rdi
 38fc6a3:      	movq	%r13, %rsi
 38fc6a6:      	callq	0x38febd0 <_ZN4llvm23SmallVectorTemplateBaseINS_9BitVectorELb0EE4growEm>
 38fc6ab:      	xorps	%xmm0, %xmm0
 38fc6ae:      	movl	0x688(%rbx), %eax
 38fc6b4:      	cmpl	%eax, %r13d
 38fc6b7:      	je	0x38fc71f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15af>
 38fc6b9:      	movq	0x40(%rsp), %rcx
 38fc6be:      	movq	(%rcx), %rdx
 38fc6c1:      	leal	(,%r14,8), %ecx
 38fc6c9:      	leaq	(%rcx,%rcx,8), %rcx
 38fc6cd:      	shlq	$0x3, %rax
 38fc6d1:      	leaq	(%rax,%rax,8), %rax
 38fc6d5:      	subq	%rax, %rcx
 38fc6d8:      	addq	$0x48, %rcx
 38fc6dc:      	leaq	0x10(%rdx,%rax), %rax
 38fc6e1:      	nopw	%cs:(%rax,%rax)
 38fc6eb:      	nopl	(%rax,%rax)
 38fc6f0:      	movups	%xmm0, 0x20(%rax)
 38fc6f4:      	movups	%xmm0, 0x10(%rax)
 38fc6f8:      	movups	%xmm0, (%rax)
 38fc6fb:      	movq	$0x0, 0x30(%rax)
 38fc703:      	movq	%rax, -0x10(%rax)
 38fc707:      	movabsq	$0x600000000, %rdx      # imm = 0x600000000
 38fc711:      	movq	%rdx, -0x8(%rax)
 38fc715:      	addq	$0x48, %rax
 38fc719:      	addq	$-0x48, %rcx
 38fc71d:      	jne	0x38fc6f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1580>
 38fc71f:      	movq	(%rsp), %rax
 38fc723:      	movl	%r13d, 0x688(%rax)
 38fc72a:      	movq	0x20(%rsp), %r12
 38fc72f:      	movq	0x18(%rsp), %rax
 38fc734:      	movq	(%rax), %rax
 38fc737:      	leaq	(%r14,%r14,8), %rdi
 38fc73b:      	leaq	(%rax,%rdi,8), %r13
 38fc73f:      	movl	0x40(%rax,%rdi,8), %ecx
 38fc743:      	andq	$0x3f, %rcx
 38fc747:      	movq	0x28(%rsp), %rsi
 38fc74c:      	je	0x38fc76a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15fa>
 38fc74e:      	movq	$-0x1, %rax
 38fc755:      	shlq	%cl, %rax
 38fc758:      	notq	%rax
 38fc75b:      	movq	(%r13), %rcx
 38fc75f:      	movl	0x8(%r13), %ebx
 38fc763:      	andq	%rax, -0x8(%rcx,%rbx,8)
 38fc768:      	jmp	0x38fc76e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x15fe>
 38fc76a:      	movl	0x8(%r13), %ebx
 38fc76e:      	movl	%ebx, %r15d
 38fc771:      	movl	%r12d, 0x40(%r13)
 38fc775:      	movl	%esi, %eax
 38fc777:      	movl	%r12d, %ebp
 38fc77a:      	cmpl	%ebx, %esi
 38fc77c:      	je	0x38fc7cd <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x165d>
 38fc77e:      	movl	%r12d, %ebp
 38fc781:      	movl	%esi, %eax
 38fc783:      	jb	0x38fc7c9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1659>
 38fc785:      	movl	%r12d, %ebp
 38fc788:      	movq	%rbx, %rdi
 38fc78b:      	cmpl	0xc(%r13), %esi
 38fc78f:      	ja	0x38fc8a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1730>
 38fc795:      	movq	%rsi, %r12
 38fc798:      	subq	%rbx, %r12
 38fc79b:      	shlq	$0x3, %rdi
 38fc79f:      	addq	(%r13), %rdi
 38fc7a3:      	leal	(,%r12,8), %edx
 38fc7ab:      	xorl	%esi, %esi
 38fc7ad:      	callq	0x828ab90 <memset@plt>
 38fc7b2:      	movq	0x28(%rsp), %rsi
 38fc7b7:      	addl	%r12d, %r15d
 38fc7ba:      	movl	%r15d, %eax
 38fc7bd:      	movq	0x20(%rsp), %r12
 38fc7c2:      	xorps	%xmm0, %xmm0
 38fc7c5:      	leaq	(%r14,%r14,8), %rdi
 38fc7c9:      	movl	%eax, 0x8(%r13)
 38fc7cd:      	andl	$0x3f, %ebp
 38fc7d0:      	je	0x38fc7ec <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x167c>
 38fc7d2:      	movq	$-0x1, %rdx
 38fc7d9:      	movl	%ebp, %ecx
 38fc7db:      	shlq	%cl, %rdx
 38fc7de:      	notq	%rdx
 38fc7e1:      	movq	(%r13), %rcx
 38fc7e5:      	movl	%eax, %eax
 38fc7e7:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fc7ec:      	movq	0x40(%rsp), %rax
 38fc7f1:      	movq	(%rax), %rax
 38fc7f4:      	leaq	(%rax,%rdi,8), %r13
 38fc7f8:      	movl	0x40(%rax,%rdi,8), %ecx
 38fc7fc:      	andq	$0x3f, %rcx
 38fc800:      	je	0x38fc81e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16ae>
 38fc802:      	movq	$-0x1, %rax
 38fc809:      	shlq	%cl, %rax
 38fc80c:      	notq	%rax
 38fc80f:      	movq	(%r13), %rcx
 38fc813:      	movl	0x8(%r13), %ebx
 38fc817:      	andq	%rax, -0x8(%rcx,%rbx,8)
 38fc81c:      	jmp	0x38fc822 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16b2>
 38fc81e:      	movl	0x8(%r13), %ebx
 38fc822:      	movl	%ebx, %r15d
 38fc825:      	movl	%r12d, 0x40(%r13)
 38fc829:      	movl	%esi, %eax
 38fc82b:      	movl	%r12d, %ebp
 38fc82e:      	cmpl	%ebx, %esi
 38fc830:      	je	0x38fc878 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1708>
 38fc832:      	movl	%r12d, %ebp
 38fc835:      	movl	%esi, %eax
 38fc837:      	jb	0x38fc874 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1704>
 38fc839:      	movl	%r12d, %ebp
 38fc83c:      	movq	%rbx, %rdi
 38fc83f:      	cmpl	0xc(%r13), %esi
 38fc843:      	ja	0x38fc8cb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x175b>
 38fc849:      	movq	%rsi, %r12
 38fc84c:      	subq	%rbx, %r12
 38fc84f:      	shlq	$0x3, %rdi
 38fc853:      	addq	(%r13), %rdi
 38fc857:      	leal	(,%r12,8), %edx
 38fc85f:      	xorl	%esi, %esi
 38fc861:      	callq	0x828ab90 <memset@plt>
 38fc866:      	addl	%r12d, %r15d
 38fc869:      	movl	%r15d, %eax
 38fc86c:      	movq	0x20(%rsp), %r12
 38fc871:      	xorps	%xmm0, %xmm0
 38fc874:      	movl	%eax, 0x8(%r13)
 38fc878:      	andl	$0x3f, %ebp
 38fc87b:      	je	0x38fc3e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc881:      	movq	$-0x1, %rdx
 38fc888:      	movl	%ebp, %ecx
 38fc88a:      	shlq	%cl, %rdx
 38fc88d:      	notq	%rdx
 38fc890:      	movq	(%r13), %rcx
 38fc894:      	movl	%eax, %eax
 38fc896:      	andq	%rdx, -0x8(%rcx,%rax,8)
 38fc89b:      	jmp	0x38fc3e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1270>
 38fc8a0:      	leaq	0x10(%r13), %rsi
 38fc8a4:      	movl	$0x8, %ecx
 38fc8a9:      	movq	%r13, %rdi
 38fc8ac:      	movq	0x28(%rsp), %rdx
 38fc8b1:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc8b6:      	movq	0x28(%rsp), %rsi
 38fc8bb:      	movl	0x8(%r13), %edi
 38fc8bf:      	movl	0x40(%r13), %ebp
 38fc8c3:      	movl	%edi, %r15d
 38fc8c6:      	jmp	0x38fc795 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1625>
 38fc8cb:      	leaq	0x10(%r13), %rsi
 38fc8cf:      	movl	$0x8, %ecx
 38fc8d4:      	movq	%r13, %rdi
 38fc8d7:      	movq	0x28(%rsp), %rdx
 38fc8dc:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc8e1:      	movq	0x28(%rsp), %rsi
 38fc8e6:      	movl	0x8(%r13), %edi
 38fc8ea:      	movl	0x40(%r13), %ebp
 38fc8ee:      	movl	%edi, %r15d
 38fc8f1:      	jmp	0x38fc849 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x16d9>
 38fc8f6:      	movq	0x28(%rbp), %rdi
 38fc8fa:      	movq	0x30(%rbp), %rsi
 38fc8fe:      	callq	0x38feac0 <_ZN4llvm11stable_sortIRSt6vectorIPNS_12LiveIntervalESaIS3_EEN12_GLOBAL__N_114IntervalSorterEEEvOT_T0_>
 38fc903:      	leaq	0x668(%rbp), %rax
 38fc90a:      	movq	%rax, 0x48(%rsp)
 38fc90f:      	movl	0x5d0(%rbp), %r14d
 38fc916:      	movl	0x670(%rbp), %eax
 38fc91c:      	cmpl	%eax, %r14d
 38fc91f:      	je	0x38fc985 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1815>
 38fc921:      	jb	0x38fc977 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1807>
 38fc923:      	cmpl	0x674(%rbp), %r14d
 38fc92a:      	jbe	0x38fc94d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x17dd>
 38fc92c:      	leaq	0x678(%rbp), %rsi
 38fc933:      	movl	$0x4, %ecx
 38fc938:      	leaq	0x668(%rbp), %rdi
 38fc93f:      	movq	%r14, %rdx
 38fc942:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fc947:      	movl	0x670(%rbp), %eax
 38fc94d:      	cmpl	%eax, %r14d
 38fc950:      	je	0x38fc977 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1807>
 38fc952:      	movl	%eax, %eax
 38fc954:      	leaq	(,%rax,4), %rdi
 38fc95c:      	leaq	0x668(%rbp), %rcx
 38fc963:      	addq	(%rcx), %rdi
 38fc966:      	movq	%r14, %rdx
 38fc969:      	subq	%rax, %rdx
 38fc96c:      	shlq	$0x2, %rdx
 38fc970:      	xorl	%esi, %esi
 38fc972:      	callq	0x828ab90 <memset@plt>
 38fc977:      	movl	%r14d, 0x670(%rbp)
 38fc97e:      	movl	0x5d0(%rbp), %r14d
 38fc985:      	testl	%r14d, %r14d
 38fc988:      	je	0x38fca49 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18d9>
 38fc98e:      	movq	0x18(%rsp), %rax
 38fc993:      	movq	(%rax), %rax
 38fc996:      	leaq	0x668(%rbp), %rcx
 38fc99d:      	movq	(%rcx), %rdx
 38fc9a0:      	movl	%r14d, %esi
 38fc9a3:      	xorl	%edi, %edi
 38fc9a5:      	jmp	0x38fc9c8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1858>
 38fc9a7:      	nopw	(%rax,%rax)
 38fc9b0:      	tzcntq	%r14, %r8
 38fc9b5:      	orl	%ecx, %r8d
 38fc9b8:      	movl	%r8d, (%rdx,%rdi,4)
 38fc9bc:      	incq	%rdi
 38fc9bf:      	cmpq	%rsi, %rdi
 38fc9c2:      	je	0x38fca49 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18d9>
 38fc9c8:      	leaq	(%rdi,%rdi,8), %r11
 38fc9cc:      	movl	0x40(%rax,%r11,8), %ecx
 38fc9d1:      	movl	$0xffffffff, %r8d       # imm = 0xFFFFFFFF
 38fc9d7:      	testl	%ecx, %ecx
 38fc9d9:      	je	0x38fc9b8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fc9db:      	decl	%ecx
 38fc9dd:      	movl	%ecx, %r9d
 38fc9e0:      	notb	%cl
 38fc9e2:      	movq	$-0x1, %r10
 38fc9e9:      	shrq	%cl, %r10
 38fc9ec:      	leaq	(%rax,%r11,8), %r11
 38fc9f0:      	shrl	$0x6, %r9d
 38fc9f4:      	xorl	%ecx, %ecx
 38fc9f6:      	movl	%r9d, %ebx
 38fc9f9:      	negl	%ebx
 38fc9fb:      	movl	$0x0, %r14d
 38fca01:      	sbbq	%r14, %r14
 38fca04:      	movq	(%r11), %r11
 38fca07:      	orq	%r10, %r14
 38fca0a:      	andq	(%r11), %r14
 38fca0d:      	jne	0x38fc9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1840>
 38fca0f:      	testq	%r9, %r9
 38fca12:      	je	0x38fc9b8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fca14:      	leaq	-0x1(%r9), %rbx
 38fca18:      	movl	$0x40, %ecx
 38fca1d:      	xorl	%r15d, %r15d
 38fca20:      	cmpq	%r15, %rbx
 38fca23:      	movq	$-0x1, %r14
 38fca2a:      	cmoveq	%r10, %r14
 38fca2e:      	andq	0x8(%r11,%r15,8), %r14
 38fca33:      	jne	0x38fc9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1840>
 38fca39:      	addl	$0x40, %ecx
 38fca3c:      	incq	%r15
 38fca3f:      	cmpq	%r15, %r9
 38fca42:      	jne	0x38fca20 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18b0>
 38fca44:      	jmp	0x38fc9b8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1848>
 38fca49:      	movq	0x258(%rsp), %rdi
 38fca51:      	leaq	0x268(%rsp), %rax
 38fca59:      	cmpq	%rax, %rdi
 38fca5c:      	je	0x38fca63 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x18f3>
 38fca5e:      	callq	0x828a640 <free@plt>
 38fca63:      	movq	(%rbp), %rcx
 38fca67:      	movq	0x10(%rcx), %rax
 38fca6b:      	subq	0x8(%rcx), %rax
 38fca6f:      	shrq	$0x3, %rax
 38fca73:      	imull	$0xcccccccd, %eax, %eax # imm = 0xCCCCCCCD
 38fca79:      	movl	0x20(%rcx), %ecx
 38fca7c:      	movl	%eax, %r14d
 38fca7f:      	subl	%ecx, %r14d
 38fca82:      	leaq	0x218(%rsp), %rsi
 38fca8a:      	movq	%rsi, 0x208(%rsp)
 38fca92:      	movabsq	$0x1000000000, %rbx     # imm = 0x1000000000
 38fca9c:      	movq	%rbx, 0x210(%rsp)
 38fcaa4:      	cmpl	$0x11, %r14d
 38fcaa8:      	jb	0x38fcb7e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1a0e>
 38fcaae:      	leaq	0x208(%rsp), %rdi
 38fcab6:      	movl	$0x4, %ecx
 38fcabb:      	movq	%r14, %rdx
 38fcabe:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcac3:      	movq	0x208(%rsp), %rdi
 38fcacb:      	leaq	(,%r14,4), %r12
 38fcad3:      	movl	$0xff, %esi
 38fcad8:      	movq	%r12, %rdx
 38fcadb:      	callq	0x828ab90 <memset@plt>
 38fcae0:      	movl	%r14d, 0x210(%rsp)
 38fcae8:      	leaq	0x180(%rsp), %rsi
 38fcaf0:      	movq	%rsi, 0x170(%rsp)
 38fcaf8:      	movq	%rbx, 0x178(%rsp)
 38fcb00:      	leaq	0x170(%rsp), %rdi
 38fcb08:      	movl	$0x4, %ecx
 38fcb0d:      	movq	%rsi, 0x60(%rsp)
 38fcb12:      	movq	%r14, %rdx
 38fcb15:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcb1a:      	movq	0x170(%rsp), %rdi
 38fcb22:      	xorl	%esi, %esi
 38fcb24:      	movq	%r12, %rdx
 38fcb27:      	callq	0x828ab90 <memset@plt>
 38fcb2c:      	movl	%r14d, 0x178(%rsp)
 38fcb34:      	leaq	0x268(%rsp), %rax
 38fcb3c:      	movq	%rax, 0x68(%rsp)
 38fcb41:      	movq	%rax, 0x258(%rsp)
 38fcb49:      	movq	%rbx, 0x260(%rsp)
 38fcb51:      	leaq	0x258(%rsp), %rdi
 38fcb59:      	movq	%r14, %rsi
 38fcb5c:      	callq	0x36af620 <_ZN4llvm23SmallVectorTemplateBaseINS_11SmallVectorIiLj4EEELb0EE4growEm>
 38fcb61:      	movl	0x260(%rsp), %ebx
 38fcb68:      	cmpl	%ebx, %r14d
 38fcb6b:      	je	0x38fccf2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b82>
 38fcb71:      	movq	0x258(%rsp), %rcx
 38fcb79:      	jmp	0x38fccc3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b53>
 38fcb7e:      	cmpl	%ecx, %eax
 38fcb80:      	jne	0x38fcc51 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ae1>
 38fcb86:      	movl	%r14d, 0x210(%rsp)
 38fcb8e:      	leaq	0x180(%rsp), %rax
 38fcb96:      	movq	%rax, 0x60(%rsp)
 38fcb9b:      	movq	%rax, 0x170(%rsp)
 38fcba3:      	movl	$0x10, 0x17c(%rsp)
 38fcbae:      	movl	%r14d, 0x178(%rsp)
 38fcbb6:      	leaq	0x268(%rsp), %rax
 38fcbbe:      	movq	%rax, 0x68(%rsp)
 38fcbc3:      	movq	%rax, 0x258(%rsp)
 38fcbcb:      	movq	%rbx, 0x260(%rsp)
 38fcbd3:      	leaq	0x1d0(%rsp), %rax
 38fcbdb:      	movq	%rax, 0x80(%rsp)
 38fcbe3:      	movq	%rax, 0x1c0(%rsp)
 38fcbeb:      	movl	$0x6, 0x1cc(%rsp)
 38fcbf6:      	xorl	%r12d, %r12d
 38fcbf9:      	jmp	0x38fcd7c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c0c>
 38fcbfe:      	subq	$-0x80, %r12
 38fcc02:      	movq	0x8(%rsp), %rdi
 38fcc07:      	jmp	0x38fcc20 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ab0>
 38fcc09:      	nopl	(%rax)
 38fcc10:      	movq	%rax, (%rsi)
 38fcc13:      	addq	$0x8, %r12
 38fcc17:      	cmpq	%rdi, %r12
 38fcc1a:      	je	0x38fc3b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fcc20:      	movq	-0x8(%r12), %rcx
 38fcc25:      	movq	(%r12), %rax
 38fcc29:      	movl	(%rax), %edx
 38fcc2b:      	movq	%r12, %rsi
 38fcc2e:      	cmpl	(%rcx), %edx
 38fcc30:      	jge	0x38fcc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1aa0>
 38fcc32:      	movq	%r12, %rsi
 38fcc35:      	nopw	%cs:(%rax,%rax)
 38fcc3f:      	nop
 38fcc40:      	movq	%rcx, (%rsi)
 38fcc43:      	movq	-0x10(%rsi), %rcx
 38fcc47:      	addq	$-0x8, %rsi
 38fcc4b:      	cmpl	(%rcx), %edx
 38fcc4d:      	jl	0x38fcc40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1ad0>
 38fcc4f:      	jmp	0x38fcc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1aa0>
 38fcc51:      	leaq	0x180(%rsp), %r15
 38fcc59:      	leaq	(,%r14,4), %r12
 38fcc61:      	movq	%rsi, %rdi
 38fcc64:      	movl	$0xff, %esi
 38fcc69:      	movq	%rbx, %r13
 38fcc6c:      	movq	%r12, %rdx
 38fcc6f:      	callq	0x828ab90 <memset@plt>
 38fcc74:      	movl	%r14d, 0x210(%rsp)
 38fcc7c:      	movq	%r15, 0x170(%rsp)
 38fcc84:      	movl	$0x10, 0x17c(%rsp)
 38fcc8f:      	xorl	%ebx, %ebx
 38fcc91:      	movq	%r15, 0x60(%rsp)
 38fcc96:      	movq	%r15, %rdi
 38fcc99:      	xorl	%esi, %esi
 38fcc9b:      	movq	%r12, %rdx
 38fcc9e:      	callq	0x828ab90 <memset@plt>
 38fcca3:      	movl	%r14d, 0x178(%rsp)
 38fccab:      	leaq	0x268(%rsp), %rcx
 38fccb3:      	movq	%rcx, 0x258(%rsp)
 38fccbb:      	movq	%r13, 0x260(%rsp)
 38fccc3:      	movabsq	$0x400000000, %rdx      # imm = 0x400000000
 38fcccd:      	movq	%r14, %rax
 38fccd0:      	shlq	$0x5, %rax
 38fccd4:      	shlq	$0x5, %rbx
 38fccd8:      	subq	%rbx, %rax
 38fccdb:      	leaq	0x10(%rbx,%rcx), %rcx
 38fcce0:      	movq	%rcx, -0x10(%rcx)
 38fcce4:      	movq	%rdx, -0x8(%rcx)
 38fcce8:      	addq	$0x20, %rcx
 38fccec:      	addq	$-0x20, %rax
 38fccf0:      	jne	0x38fcce0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1b70>
 38fccf2:      	movl	%r14d, 0x260(%rsp)
 38fccfa:      	leal	0x3f(%r14), %eax
 38fccfe:      	movl	%eax, %r12d
 38fcd01:      	shrl	$0x6, %r12d
 38fcd05:      	leaq	0x1d0(%rsp), %rsi
 38fcd0d:      	movq	%rsi, 0x1c0(%rsp)
 38fcd15:      	movl	$0x6, 0x1cc(%rsp)
 38fcd20:      	cmpl	$0x1c0, %eax            # imm = 0x1C0
 38fcd25:      	movq	%rsi, 0x80(%rsp)
 38fcd2d:      	jb	0x38fcd61 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1bf1>
 38fcd2f:      	movl	$0x0, 0x1c8(%rsp)
 38fcd3a:      	leaq	0x1c0(%rsp), %rdi
 38fcd42:      	movl	$0x8, %ecx
 38fcd47:      	movq	%r12, %rdx
 38fcd4a:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fcd4f:      	movq	0x1c0(%rsp), %rdi
 38fcd57:      	leal	(,%r12,8), %edx
 38fcd5f:      	jmp	0x38fcd75 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c05>
 38fcd61:      	testl	%r12d, %r12d
 38fcd64:      	je	0x38fe1f0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3080>
 38fcd6a:      	leal	(,%r12,8), %edx
 38fcd72:      	movq	%rsi, %rdi
 38fcd75:      	xorl	%esi, %esi
 38fcd77:      	callq	0x828ab90 <memset@plt>
 38fcd7c:      	movl	%r12d, 0x1c8(%rsp)
 38fcd84:      	movl	%r14d, 0x200(%rsp)
 38fcd8c:      	movq	0x28(%rbp), %r14
 38fcd90:      	movq	0x30(%rbp), %rsi
 38fcd94:      	cmpq	%rsi, %r14
 38fcd97:      	je	0x38fd48c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x231c>
 38fcd9d:      	leaq	0x720(%rbp), %rax
 38fcda4:      	movq	%rax, 0xb0(%rsp)
 38fcdac:      	xorl	%ebx, %ebx
 38fcdae:      	movq	%rsi, 0x70(%rsp)
 38fcdb3:      	nopw	%cs:(%rax,%rax)
 38fcdbd:      	nopl	(%rax)
 38fcdc0:      	movq	%rbx, 0x30(%rsp)
 38fcdc5:      	movq	(%r14), %rax
 38fcdc8:      	movq	%rax, 0x8(%rsp)
 38fcdcd:      	movl	0x70(%rax), %r15d
 38fcdd1:      	shll	$0x2, %r15d
 38fcdd5:      	sarl	$0x2, %r15d
 38fcdd9:      	movq	(%rbp), %rax
 38fcddd:      	movl	0x20(%rax), %ecx
 38fcde0:      	addl	%r15d, %ecx
 38fcde3:      	movq	0x8(%rax), %rax
 38fcde7:      	leaq	(%rcx,%rcx,4), %rcx
 38fcdeb:      	movzbl	0x15(%rax,%rcx,8), %ebx
 38fcdf0:      	movq	0x680(%rbp), %rdx
 38fcdf7:      	cmpb	$0x0, 0x4cb2b7a(%rip)   # 0x85af978 <_ZL14DisableSharing+0x78>
 38fcdfe:      	jne	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fce04:      	leaq	(%rbx,%rbx,8), %r11
 38fce08:      	movl	0x40(%rdx,%r11,8), %ecx
 38fce0d:      	testl	%ecx, %ecx
 38fce0f:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fce15:      	decl	%ecx
 38fce17:      	movl	%ecx, %eax
 38fce19:      	notb	%cl
 38fce1b:      	movq	$-0x1, %rsi
 38fce22:      	shrq	%cl, %rsi
 38fce25:      	leaq	(%rdx,%r11,8), %rdi
 38fce29:      	shrl	$0x6, %eax
 38fce2c:      	xorl	%ecx, %ecx
 38fce2e:      	movl	%eax, %r8d
 38fce31:      	negl	%r8d
 38fce34:      	movl	$0x0, %r9d
 38fce3a:      	sbbq	%r9, %r9
 38fce3d:      	movq	(%rdi), %rdi
 38fce40:      	orq	%rsi, %r9
 38fce43:      	andq	(%rdi), %r9
 38fce46:      	je	0x38fce66 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cf6>
 38fce48:      	tzcntq	%r9, %r12
 38fce4d:      	orl	%ecx, %r12d
 38fce50:      	cmpl	$-0x1, %r12d
 38fce54:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fce5a:      	movq	%rbx, 0x28(%rsp)
 38fce5f:      	movq	%r11, 0x20(%rsp)
 38fce64:      	jmp	0x38fcebe <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d4e>
 38fce66:      	testq	%rax, %rax
 38fce69:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fce6f:      	leaq	-0x1(%rax), %r8
 38fce73:      	movl	$0x40, %ecx
 38fce78:      	xorl	%r10d, %r10d
 38fce7b:      	nopl	(%rax,%rax)
 38fce80:      	cmpq	%r10, %r8
 38fce83:      	movq	$-0x1, %r9
 38fce8a:      	cmoveq	%rsi, %r9
 38fce8e:      	andq	0x8(%rdi,%r10,8), %r9
 38fce93:      	jne	0x38fce48 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1cd8>
 38fce95:      	addl	$0x40, %ecx
 38fce98:      	incq	%r10
 38fce9b:      	cmpq	%r10, %rax
 38fce9e:      	jne	0x38fce80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d10>
 38fcea0:      	jmp	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcea5:      	incl	%eax
 38fcea7:      	movl	%eax, %edi
 38fcea9:      	tzcntq	%rcx, %r12
 38fceae:      	shll	$0x6, %edi
 38fceb1:      	orl	%edi, %r12d
 38fceb4:      	cmpl	$-0x1, %r12d
 38fceb8:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcebe:      	movslq	%r12d, %r13
 38fcec1:      	movq	0x78(%rsp), %rax
 38fcec6:      	movq	(%rax), %rax
 38fcec9:      	imulq	$0xe8, %r13, %rcx
 38fced0:      	movq	0x8(%rax,%rcx), %rdx
 38fced5:      	testq	%rdx, %rdx
 38fced8:      	je	0x38fcfb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e40>
 38fcede:      	movq	%rdx, 0xc0(%rsp)
 38fcee6:      	movq	0x8(%rsp), %rax
 38fceeb:      	movq	%rax, 0xc8(%rsp)
 38fcef3:      	movq	$0x0, 0xd8(%rsp)
 38fceff:      	leaq	0xf0(%rsp), %rax
 38fcf07:      	movq	%rax, 0xe0(%rsp)
 38fcf0f:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 38fcf19:      	movq	%rax, 0xe8(%rsp)
 38fcf21:      	leaq	0x140(%rsp), %rbx
 38fcf29:      	movq	%rbx, 0x130(%rsp)
 38fcf31:      	movq	%rax, 0x138(%rsp)
 38fcf39:      	movw	$0x0, 0x160(%rsp)
 38fcf43:      	movq	$0x0, 0x164(%rsp)
 38fcf4f:      	leaq	0xc0(%rsp), %rdi
 38fcf57:      	movl	$0x1, %esi
 38fcf5c:      	callq	0x35bb9a0 <_ZN4llvm17LiveIntervalUnion5Query23collectInterferingVRegsEj>
 38fcf61:      	movl	%eax, %ebp
 38fcf63:      	movq	0x130(%rsp), %rdi
 38fcf6b:      	cmpq	%rbx, %rdi
 38fcf6e:      	je	0x38fcf75 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e05>
 38fcf70:      	callq	0x828a640 <free@plt>
 38fcf75:      	movq	0xe0(%rsp), %rdi
 38fcf7d:      	leaq	0xf0(%rsp), %rax
 38fcf85:      	cmpq	%rax, %rdi
 38fcf88:      	je	0x38fcf8f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e1f>
 38fcf8a:      	callq	0x828a640 <free@plt>
 38fcf8f:      	testl	%ebp, %ebp
 38fcf91:      	movq	(%rsp), %rbp
 38fcf95:      	movq	0x28(%rsp), %rbx
 38fcf9a:      	jne	0x38fcfe1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1e71>
 38fcf9c:      	jmp	0x38fd419 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fcfa1:      	nopw	%cs:(%rax,%rax)
 38fcfab:      	nopl	(%rax,%rax)
 38fcfb0:      	movq	(%rax,%rcx), %rdi
 38fcfb4:      	testq	%rdi, %rdi
 38fcfb7:      	je	0x38fd419 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fcfbd:      	movq	0x8(%rsp), %rax
 38fcfc2:      	cmpl	$0x0, 0x8(%rax)
 38fcfc6:      	je	0x38fd419 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fcfcc:      	movq	0x8(%rsp), %rsi
 38fcfd1:      	movq	(%rsi), %rdx
 38fcfd4:      	callq	0x35aa860 <_ZNK4llvm9LiveRange12overlapsFromERKS0_PKNS0_7SegmentE>
 38fcfd9:      	testb	%al, %al
 38fcfdb:      	je	0x38fd419 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22a9>
 38fcfe1:      	movq	0x40(%rsp), %rax
 38fcfe6:      	movq	(%rax), %rdx
 38fcfe9:      	incl	%r12d
 38fcfec:      	movq	0x20(%rsp), %r11
 38fcff1:      	movl	0x40(%rdx,%r11,8), %eax
 38fcff6:      	cmpl	%eax, %r12d
 38fcff9:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fcfff:      	movl	%r12d, %edi
 38fd002:      	shrl	$0x6, %edi
 38fd005:      	decl	%eax
 38fd007:      	movl	%eax, %r8d
 38fd00a:      	shrl	$0x6, %r8d
 38fd00e:      	cmpl	%r8d, %edi
 38fd011:      	ja	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd017:      	leaq	(%rdx,%r11,8), %rcx
 38fd01b:      	movq	(%rcx), %rsi
 38fd01e:      	andl	$0x3f, %r12d
 38fd022:      	movl	%r12d, %ecx
 38fd025:      	negb	%cl
 38fd027:      	movq	$-0x1, %r9
 38fd02e:      	shrq	%cl, %r9
 38fd031:      	cmpl	$0x1, %r12d
 38fd035:      	movl	$0x0, %r10d
 38fd03b:      	sbbq	%r10, %r10
 38fd03e:      	notq	%r9
 38fd041:      	orq	%r9, %r10
 38fd044:      	notb	%al
 38fd046:      	movq	$-0x1, %r9
 38fd04d:      	movl	%eax, %ecx
 38fd04f:      	shrq	%cl, %r9
 38fd052:      	cmpl	%r8d, %edi
 38fd055:      	movq	$-0x1, %rcx
 38fd05c:      	cmoveq	%r9, %rcx
 38fd060:      	movl	%edi, %eax
 38fd062:      	andq	%r10, %rcx
 38fd065:      	andq	(%rsi,%rax,8), %rcx
 38fd069:      	jne	0x38fcea9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d39>
 38fd06f:      	leal	0x1(%r8), %ecx
 38fd073:      	leal	0x1(%rax), %edi
 38fd076:      	cmpl	%ecx, %edi
 38fd078:      	je	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd07a:      	movl	%r8d, %edi
 38fd07d:      	leaq	-0x1(%rdi), %r8
 38fd081:      	nopw	%cs:(%rax,%rax)
 38fd08b:      	nopl	(%rax,%rax)
 38fd090:      	cmpq	%rax, %r8
 38fd093:      	movq	$-0x1, %rcx
 38fd09a:      	cmoveq	%r9, %rcx
 38fd09e:      	andq	0x8(%rsi,%rax,8), %rcx
 38fd0a3:      	jne	0x38fcea5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1d35>
 38fd0a9:      	incq	%rax
 38fd0ac:      	cmpq	%rax, %rdi
 38fd0af:      	jne	0x38fd090 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f20>
 38fd0b1:      	nopw	%cs:(%rax,%rax)
 38fd0bb:      	nopl	(%rax,%rax)
 38fd0c0:      	movq	0x48(%rsp), %rax
 38fd0c5:      	movq	(%rax), %rsi
 38fd0c8:      	movl	(%rsi,%rbx,4), %r12d
 38fd0cc:      	leal	(,%rbx,8), %eax
 38fd0d3:      	movl	$0x1, %edi
 38fd0d8:      	movl	%r12d, %ecx
 38fd0db:      	shlq	%cl, %rdi
 38fd0de:      	leaq	(%rax,%rax,8), %rcx
 38fd0e2:      	movq	(%rdx,%rcx), %rax
 38fd0e6:      	movl	%r12d, %edx
 38fd0e9:      	shrl	$0x6, %edx
 38fd0ec:      	orq	%rdi, (%rax,%rdx,8)
 38fd0f0:      	movq	0x18(%rsp), %rax
 38fd0f5:      	movq	(%rax), %rdi
 38fd0f8:      	leal	0x1(%r12), %r10d
 38fd0fd:      	movl	0x40(%rdi,%rcx), %eax
 38fd101:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 38fd106:      	cmpl	%eax, %r10d
 38fd109:      	je	0x38fd1e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd10f:      	movl	%r10d, %r8d
 38fd112:      	shrl	$0x6, %r8d
 38fd116:      	decl	%eax
 38fd118:      	movl	%eax, %r9d
 38fd11b:      	shrl	$0x6, %r9d
 38fd11f:      	cmpl	%r9d, %r8d
 38fd122:      	ja	0x38fd1e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd128:      	addq	%rcx, %rdi
 38fd12b:      	movq	(%rdi), %rdi
 38fd12e:      	andl	$0x3f, %r10d
 38fd132:      	movl	%r10d, %ecx
 38fd135:      	negb	%cl
 38fd137:      	movq	$-0x1, %r11
 38fd13e:      	shrq	%cl, %r11
 38fd141:      	cmpl	$0x1, %r10d
 38fd145:      	movq	%rbx, %r13
 38fd148:      	movl	$0x0, %ebx
 38fd14d:      	sbbq	%rbx, %rbx
 38fd150:      	notq	%r11
 38fd153:      	orq	%r11, %rbx
 38fd156:      	notb	%al
 38fd158:      	movq	$-0x1, %r10
 38fd15f:      	movl	%eax, %ecx
 38fd161:      	shrq	%cl, %r10
 38fd164:      	cmpl	%r9d, %r8d
 38fd167:      	movq	$-0x1, %rcx
 38fd16e:      	cmoveq	%r10, %rcx
 38fd172:      	movl	%r8d, %eax
 38fd175:      	andq	%rbx, %rcx
 38fd178:      	movq	%r13, %rbx
 38fd17b:      	andq	(%rdi,%rax,8), %rcx
 38fd17f:      	je	0x38fd18f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x201f>
 38fd181:      	tzcntq	%rcx, %rdx
 38fd186:      	shll	$0x6, %r8d
 38fd18a:      	orl	%r8d, %edx
 38fd18d:      	jmp	0x38fd1e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd18f:      	leal	0x1(%r9), %ecx
 38fd193:      	leal	0x1(%rax), %r8d
 38fd197:      	cmpl	%ecx, %r8d
 38fd19a:      	je	0x38fd1e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2070>
 38fd19c:      	movl	%r9d, %r8d
 38fd19f:      	leaq	-0x1(%r8), %r9
 38fd1a3:      	nopw	%cs:(%rax,%rax)
 38fd1ad:      	nopl	(%rax)
 38fd1b0:      	cmpq	%rax, %r9
 38fd1b3:      	movq	$-0x1, %rcx
 38fd1ba:      	cmoveq	%r10, %rcx
 38fd1be:      	andq	0x8(%rdi,%rax,8), %rcx
 38fd1c3:      	jne	0x38fd457 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22e7>
 38fd1c9:      	incq	%rax
 38fd1cc:      	cmpq	%rax, %r8
 38fd1cf:      	jne	0x38fd1b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2040>
 38fd1d1:      	nopw	%cs:(%rax,%rax)
 38fd1db:      	nopl	(%rax,%rax)
 38fd1e0:      	movslq	%r12d, %r13
 38fd1e3:      	movl	%edx, (%rsi,%rbx,4)
 38fd1e6:      	xorl	%ebx, %ebx
 38fd1e8:      	movq	0x78(%rsp), %rax
 38fd1ed:      	movq	(%rax), %rbp
 38fd1f0:      	imulq	$0xe8, %r13, %rax
 38fd1f7:      	movq	0x8(%rbp,%rax), %rdi
 38fd1fc:      	testq	%rdi, %rdi
 38fd1ff:      	je	0x38fd220 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x20b0>
 38fd201:      	movq	0x8(%rsp), %rdx
 38fd206:      	movq	%rdx, %rsi
 38fd209:      	callq	0x35ba960 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd20e:      	jmp	0x38fd2d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2160>
 38fd213:      	nopw	%cs:(%rax,%rax)
 38fd21d:      	nopl	(%rax)
 38fd220:      	addq	%rax, %rbp
 38fd223:      	movq	(%rbp), %rdx
 38fd227:      	testq	%rdx, %rdx
 38fd22a:      	je	0x38fd2be <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x214e>
 38fd230:      	leaq	0x10(%rbp), %rdi
 38fd234:      	movl	$0x0, 0x10(%rbp)
 38fd23b:      	movq	$0x0, 0xd8(%rbp)
 38fd246:      	movq	0xb0(%rsp), %rax
 38fd24e:      	movq	%rax, 0xe0(%rbp)
 38fd255:      	xorps	%xmm0, %xmm0
 38fd258:      	movups	%xmm0, 0x98(%rbp)
 38fd25f:      	movups	%xmm0, 0xa8(%rbp)
 38fd266:      	movups	%xmm0, 0xb8(%rbp)
 38fd26d:      	movups	%xmm0, 0xc8(%rbp)
 38fd274:      	movups	%xmm0, 0x28(%rbp)
 38fd278:      	movups	%xmm0, 0x18(%rbp)
 38fd27c:      	movups	%xmm0, 0x48(%rbp)
 38fd280:      	movups	%xmm0, 0x38(%rbp)
 38fd284:      	movups	%xmm0, 0x68(%rbp)
 38fd288:      	movups	%xmm0, 0x58(%rbp)
 38fd28c:      	movups	%xmm0, 0x88(%rbp)
 38fd293:      	movups	%xmm0, 0x78(%rbp)
 38fd297:      	movq	%rdi, 0x8(%rbp)
 38fd29b:      	movq	%rdx, %rsi
 38fd29e:      	callq	0x35ba960 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd2a3:      	movq	0x8(%rbp), %rdi
 38fd2a7:      	movq	0x8(%rsp), %rdx
 38fd2ac:      	movq	%rdx, %rsi
 38fd2af:      	callq	0x35ba960 <_ZN4llvm17LiveIntervalUnion5unifyERKNS_12LiveIntervalERKNS_9LiveRangeE>
 38fd2b4:      	movq	$0x0, (%rbp)
 38fd2bc:      	jmp	0x38fd2d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2160>
 38fd2be:      	movq	0x8(%rsp), %rax
 38fd2c3:      	movq	%rax, (%rbp)
 38fd2c7:      	nopw	(%rax,%rax)
 38fd2d0:      	movslq	%r15d, %rax
 38fd2d3:      	movq	(%rsp), %r9
 38fd2d7:      	movq	0x550(%r9), %rcx
 38fd2de:      	movzbl	(%rcx,%rax), %esi
 38fd2e2:      	movq	(%r9), %rdi
 38fd2e5:      	testb	%bl, %bl
 38fd2e7:      	je	0x38fd310 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21a0>
 38fd2e9:      	movl	0x20(%rdi), %ecx
 38fd2ec:      	addl	%r12d, %ecx
 38fd2ef:      	movq	0x8(%rdi), %rdx
 38fd2f3:      	leaq	(%rcx,%rcx,4), %r8
 38fd2f7:      	cmpb	0x10(%rdx,%r8,8), %sil
 38fd2fc:      	ja	0x38fd31a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21aa>
 38fd2fe:      	movq	0xb8(%rsp), %rsi
 38fd306:      	movq	(%rsi), %rsi
 38fd309:      	movl	(%rsi,%rax,4), %esi
 38fd30c:      	jmp	0x38fd36a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21fa>
 38fd30e:      	nop
 38fd310:      	movq	0x8(%rdi), %rdx
 38fd314:      	movl	0x20(%rdi), %ecx
 38fd317:      	addl	%r12d, %ecx
 38fd31a:      	leaq	(%rcx,%rcx,4), %rcx
 38fd31e:      	movb	%sil, 0x10(%rdx,%rcx,8)
 38fd323:      	movl	0x20(%rdi), %ecx
 38fd326:      	addl	%r12d, %ecx
 38fd329:      	movq	0x8(%rdi), %rdx
 38fd32d:      	leaq	(%rcx,%rcx,4), %rcx
 38fd331:      	movzbl	0x15(%rdx,%rcx,8), %ecx
 38fd336:      	cmpl	$0x4, %ecx
 38fd339:      	ja	0x38fd34f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd33b:      	movl	$0x15, %edx
 38fd340:      	btl	%ecx, %edx
 38fd343:      	jae	0x38fd34f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd345:      	cmpb	%sil, 0x40(%rdi)
 38fd349:      	jae	0x38fd34f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x21df>
 38fd34b:      	movb	%sil, 0x40(%rdi)
 38fd34f:      	movq	0x578(%r9), %rcx
 38fd356:      	movl	(%rcx,%rax,4), %esi
 38fd359:      	movq	(%r9), %rcx
 38fd35c:      	movq	0x8(%rcx), %rdx
 38fd360:      	movl	0x20(%rcx), %ecx
 38fd363:      	addl	%r12d, %ecx
 38fd366:      	testb	%bl, %bl
 38fd368:      	je	0x38fd375 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2205>
 38fd36a:      	leaq	(%rcx,%rcx,4), %rdi
 38fd36e:      	cmpq	%rsi, 0x8(%rdx,%rdi,8)
 38fd373:      	jge	0x38fd37e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x220e>
 38fd375:      	leaq	(%rcx,%rcx,4), %rcx
 38fd379:      	movq	%rsi, 0x8(%rdx,%rcx,8)
 38fd37e:      	movq	0x208(%rsp), %rcx
 38fd386:      	movl	%r12d, (%rcx,%rax,4)
 38fd38a:      	movslq	%r12d, %rbx
 38fd38d:      	movq	0x258(%rsp), %rax
 38fd395:      	movq	%rbx, %rcx
 38fd398:      	shlq	$0x5, %rcx
 38fd39c:      	leaq	(%rax,%rcx), %rbp
 38fd3a0:      	movl	0x8(%rax,%rcx), %edx
 38fd3a4:      	cmpl	0xc(%rax,%rcx), %edx
 38fd3a8:      	jae	0x38fd461 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x22f1>
 38fd3ae:      	movq	(%rbp), %rax
 38fd3b2:      	movl	%edx, %ecx
 38fd3b4:      	movl	%r15d, (%rax,%rcx,4)
 38fd3b8:      	incl	0x8(%rbp)
 38fd3bb:      	movq	0x8(%rsp), %rax
 38fd3c0:      	movss	0x74(%rax), %xmm0
 38fd3c5:      	movq	0x170(%rsp), %rax
 38fd3cd:      	addss	(%rax,%rbx,4), %xmm0
 38fd3d2:      	movl	$0x1, %edx
 38fd3d7:      	movl	%r12d, %ecx
 38fd3da:      	shlq	%cl, %rdx
 38fd3dd:      	movss	%xmm0, (%rax,%rbx,4)
 38fd3e2:      	movq	0x1c0(%rsp), %rax
 38fd3ea:      	movl	%r12d, %ecx
 38fd3ed:      	shrl	$0x6, %ecx
 38fd3f0:      	orq	%rdx, (%rax,%rcx,8)
 38fd3f4:      	cmpl	%r12d, %r15d
 38fd3f7:      	setne	%al
 38fd3fa:      	movq	0x30(%rsp), %rbx
 38fd3ff:      	orb	%al, %bl
 38fd401:      	addq	$0x8, %r14
 38fd405:      	movq	0x70(%rsp), %rsi
 38fd40a:      	cmpq	%rsi, %r14
 38fd40d:      	movq	(%rsp), %rbp
 38fd411:      	jne	0x38fcdc0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c50>
 38fd417:      	jmp	0x38fd47d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x230d>
 38fd419:      	movq	%rbx, %rsi
 38fd41c:      	movq	(%rbp), %rax
 38fd420:      	movl	0x20(%rax), %ecx
 38fd423:      	leal	(%rcx,%r12), %edx
 38fd427:      	movq	0x8(%rax), %rax
 38fd42b:      	leaq	(%rdx,%rdx,4), %rdx
 38fd42f:      	movzbl	0x15(%rax,%rdx,8), %edx
 38fd434:      	addl	%r15d, %ecx
 38fd437:      	leaq	(%rcx,%rcx,4), %rcx
 38fd43b:      	movb	$0x1, %bl
 38fd43d:      	cmpb	0x15(%rax,%rcx,8), %dl
 38fd441:      	je	0x38fd1e8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2078>
 38fd447:      	movq	0x40(%rsp), %rax
 38fd44c:      	movq	(%rax), %rdx
 38fd44f:      	movq	%rsi, %rbx
 38fd452:      	jmp	0x38fd0c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1f50>
 38fd457:      	incl	%eax
 38fd459:      	movl	%eax, %r8d
 38fd45c:      	jmp	0x38fd181 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2011>
 38fd461:      	incq	%rdx
 38fd464:      	leaq	0x10(%rbp), %rsi
 38fd468:      	movl	$0x4, %ecx
 38fd46d:      	movq	%rbp, %rdi
 38fd470:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fd475:      	movl	0x8(%rbp), %edx
 38fd478:      	jmp	0x38fd3ae <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x223e>
 38fd47d:      	movq	0x28(%rbp), %r14
 38fd481:      	movq	0x30(%rbp), %rsi
 38fd485:      	cmpq	%rsi, %r14
 38fd488:      	jne	0x38fd493 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2323>
 38fd48a:      	jmp	0x38fd4c1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2351>
 38fd48c:      	xorl	%ebx, %ebx
 38fd48e:      	cmpq	%rsi, %r14
 38fd491:      	je	0x38fd4c1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2351>
 38fd493:      	movq	0x170(%rsp), %rax
 38fd49b:      	movq	%r14, %rcx
 38fd49e:      	nop
 38fd4a0:      	movq	(%rcx), %rdx
 38fd4a3:      	movl	0x70(%rdx), %edi
 38fd4a6:      	shlq	$0x22, %rdi
 38fd4aa:      	sarq	$0x22, %rdi
 38fd4ae:      	movss	(%rax,%rdi,4), %xmm0
 38fd4b3:      	movss	%xmm0, 0x74(%rdx)
 38fd4b8:      	addq	$0x8, %rcx
 38fd4bc:      	cmpq	%rsi, %rcx
 38fd4bf:      	jne	0x38fd4a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2330>
 38fd4c1:      	movq	%r14, %rdi
 38fd4c4:      	callq	0x38feac0 <_ZN4llvm11stable_sortIRSt6vectorIPNS_12LiveIntervalESaIS3_EEN12_GLOBAL__N_114IntervalSorterEEEvOT_T0_>
 38fd4c9:      	movq	%rbx, 0x30(%rsp)
 38fd4ce:      	testb	$0x1, %bl
 38fd4d1:      	je	0x38fddd6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fd4d7:      	movq	(%rsp), %rbp
 38fd4db:      	movl	0x48(%rbp), %r9d
 38fd4df:      	testq	%r9, %r9
 38fd4e2:      	je	0x38fd695 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2525>
 38fd4e8:      	xorl	%r15d, %r15d
 38fd4eb:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd4f1:      	leaq	0x4a17950(%rip), %rax   # 0x8314e48 <_ZTVN4llvm27FixedStackPseudoSourceValueE>
 38fd4f8:      	addq	$0x10, %rax
 38fd4fc:      	movq	%rax, 0x18(%rsp)
 38fd501:      	movq	%r9, 0x8(%rsp)
 38fd506:      	jmp	0x38fd51c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23ac>
 38fd508:      	nopl	(%rax,%rax)
 38fd510:      	incq	%r15
 38fd513:      	cmpq	%r9, %r15
 38fd516:      	je	0x38fd695 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2525>
 38fd51c:      	movq	0x208(%rsp), %rax
 38fd524:      	movl	(%rax,%r15,4), %r13d
 38fd528:      	cmpq	%r10, %r13
 38fd52b:      	je	0x38fd510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd52d:      	cmpq	%r13, %r15
 38fd530:      	je	0x38fd510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd532:      	movq	0x58(%rsp), %rax
 38fd537:      	movq	0x160(%rax), %r12
 38fd53e:      	leal	(%r13,%r13), %eax
 38fd543:      	movl	%r13d, %ebp
 38fd546:      	sarl	$0x1f, %ebp
 38fd549:      	xorl	%eax, %ebp
 38fd54b:      	leaq	0x48(%r12), %r14
 38fd550:      	cmpl	%ebp, 0x50(%r12)
 38fd555:      	ja	0x38fd56d <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23fd>
 38fd557:      	leal	0x1(%rbp), %esi
 38fd55a:      	movq	%r14, %rdi
 38fd55d:      	callq	0x37a5130 <_ZN4llvm15SmallVectorImplISt10unique_ptrINS_27FixedStackPseudoSourceValueESt14default_deleteIS2_EEE10resizeImplILb0EEEvm>
 38fd562:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd568:      	movq	0x8(%rsp), %r9
 38fd56d:      	movq	(%r14), %rbx
 38fd570:      	movq	(%rbx,%rbp,8), %r14
 38fd574:      	testq	%r14, %r14
 38fd577:      	jne	0x38fd5d5 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2465>
 38fd579:      	movq	(%r12), %r12
 38fd57d:      	movl	$0x18, %edi
 38fd582:      	callq	0x828a620 <_Znwm@plt>
 38fd587:      	movq	%rax, %r14
 38fd58a:      	movl	$0x4, 0x8(%rax)
 38fd591:      	movq	(%r12), %rax
 38fd595:      	movq	%r12, %rdi
 38fd598:      	movl	$0x4, %esi
 38fd59d:      	callq	*0xa8(%rax)
 38fd5a3:      	movl	%eax, 0xc(%r14)
 38fd5a7:      	movq	0x18(%rsp), %rax
 38fd5ac:      	movq	%rax, (%r14)
 38fd5af:      	movl	%r13d, 0x10(%r14)
 38fd5b3:      	movq	(%rbx,%rbp,8), %rdi
 38fd5b7:      	movq	%r14, (%rbx,%rbp,8)
 38fd5bb:      	testq	%rdi, %rdi
 38fd5be:      	je	0x38fd5ca <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x245a>
 38fd5c0:      	movq	(%rdi), %rax
 38fd5c3:      	callq	*0x10(%rax)
 38fd5c6:      	movq	(%rbx,%rbp,8), %r14
 38fd5ca:      	movq	0x8(%rsp), %r9
 38fd5cf:      	movl	$0xffffffff, %r10d      # imm = 0xFFFFFFFF
 38fd5d5:      	movq	0x38(%rsp), %rax
 38fd5da:      	movq	(%rax), %rcx
 38fd5dd:      	leaq	(%r15,%r15,4), %rdx
 38fd5e1:      	shlq	$0x4, %rdx
 38fd5e5:      	movl	0x8(%rcx,%rdx), %eax
 38fd5e9:      	testq	%rax, %rax
 38fd5ec:      	movq	(%rsp), %rbp
 38fd5f0:      	je	0x38fd510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd5f6:      	movq	(%rcx,%rdx), %rdx
 38fd5fa:      	leaq	(,%rax,8), %rsi
 38fd602:      	orq	$0x4, %r14
 38fd606:      	addq	$-0x8, %rsi
 38fd60a:      	movl	%esi, %edi
 38fd60c:      	notl	%edi
 38fd60e:      	movq	%rdx, %rcx
 38fd611:      	testb	$0x38, %dil
 38fd615:      	je	0x38fd63f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24cf>
 38fd617:      	movl	%esi, %edi
 38fd619:      	shrl	$0x3, %edi
 38fd61c:      	incl	%edi
 38fd61e:      	andl	$0x7, %edi
 38fd621:      	movq	%rdx, %rcx
 38fd624:      	nopw	%cs:(%rax,%rax)
 38fd62e:      	nop
 38fd630:      	movq	(%rcx), %r8
 38fd633:      	movq	%r14, (%r8)
 38fd636:      	addq	$0x8, %rcx
 38fd63a:      	decq	%rdi
 38fd63d:      	jne	0x38fd630 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24c0>
 38fd63f:      	cmpq	$0x38, %rsi
 38fd643:      	jb	0x38fd510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd649:      	leaq	(%rdx,%rax,8), %rax
 38fd64d:      	nopl	(%rax)
 38fd650:      	movq	(%rcx), %rdx
 38fd653:      	movq	%r14, (%rdx)
 38fd656:      	movq	0x8(%rcx), %rdx
 38fd65a:      	movq	%r14, (%rdx)
 38fd65d:      	movq	0x10(%rcx), %rdx
 38fd661:      	movq	%r14, (%rdx)
 38fd664:      	movq	0x18(%rcx), %rdx
 38fd668:      	movq	%r14, (%rdx)
 38fd66b:      	movq	0x20(%rcx), %rdx
 38fd66f:      	movq	%r14, (%rdx)
 38fd672:      	movq	0x28(%rcx), %rdx
 38fd676:      	movq	%r14, (%rdx)
 38fd679:      	movq	0x30(%rcx), %rdx
 38fd67d:      	movq	%r14, (%rdx)
 38fd680:      	movq	0x38(%rcx), %rdx
 38fd684:      	movq	%r14, (%rdx)
 38fd687:      	addq	$0x40, %rcx
 38fd68b:      	cmpq	%rax, %rcx
 38fd68e:      	jne	0x38fd650 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x24e0>
 38fd690:      	jmp	0x38fd510 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x23a0>
 38fd695:      	movq	0x58(%rsp), %rax
 38fd69a:      	movq	0x148(%rax), %rbx
 38fd6a1:      	jmp	0x38fd6b4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2544>
 38fd6a3:      	nopw	%cs:(%rax,%rax)
 38fd6ad:      	nopl	(%rax)
 38fd6b0:      	movq	0x8(%rbx), %rbx
 38fd6b4:      	cmpq	0x88(%rsp), %rbx
 38fd6bc:      	je	0x38fdc89 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b19>
 38fd6c2:      	leaq	0x30(%rbx), %r15
 38fd6c6:      	movq	0x38(%rbx), %r12
 38fd6ca:      	cmpq	%r15, %r12
 38fd6cd:      	je	0x38fd774 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2604>
 38fd6d3:      	movq	0x208(%rsp), %rax
 38fd6db:      	jmp	0x38fd6ee <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x257e>
 38fd6dd:      	nopl	(%rax)
 38fd6e0:      	movq	0x8(%r12), %r12
 38fd6e5:      	cmpq	%r15, %r12
 38fd6e8:      	je	0x38fd770 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2600>
 38fd6ee:      	movzwl	0x28(%r12), %edx
 38fd6f4:      	movzbl	0x2a(%r12), %ecx
 38fd6fa:      	shll	$0x10, %ecx
 38fd6fd:      	orl	%edx, %ecx
 38fd6ff:      	testl	%ecx, %ecx
 38fd701:      	je	0x38fd740 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25d0>
 38fd703:      	movq	0x20(%r12), %rdx
 38fd708:      	shll	$0x5, %ecx
 38fd70b:      	xorl	%esi, %esi
 38fd70d:      	jmp	0x38fd719 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a9>
 38fd70f:      	nop
 38fd710:      	addq	$0x20, %rsi
 38fd714:      	cmpq	%rsi, %rcx
 38fd717:      	je	0x38fd740 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25d0>
 38fd719:      	cmpb	$0x5, (%rdx,%rsi)
 38fd71d:      	jne	0x38fd710 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd71f:      	movslq	0x10(%rdx,%rsi), %rdi
 38fd724:      	testq	%rdi, %rdi
 38fd727:      	js	0x38fd710 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd729:      	movl	(%rax,%rdi,4), %r8d
 38fd72d:      	cmpl	$-0x1, %r8d
 38fd731:      	je	0x38fd710 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd733:      	cmpl	%edi, %r8d
 38fd736:      	je	0x38fd710 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd738:      	movl	%r8d, 0x10(%rdx,%rsi)
 38fd73d:      	jmp	0x38fd710 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25a0>
 38fd73f:      	nop
 38fd740:      	testb	$0x4, (%r12)
 38fd745:      	jne	0x38fd6e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd747:      	nopw	(%rax,%rax)
 38fd750:      	testb	$0x8, 0x2c(%r12)
 38fd756:      	je	0x38fd6e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd758:      	movq	0x8(%r12), %r12
 38fd75d:      	testb	$0x8, 0x2c(%r12)
 38fd763:      	jne	0x38fd758 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x25e8>
 38fd765:      	jmp	0x38fd6e0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2570>
 38fd76a:      	nopw	(%rax,%rax)
 38fd770:      	movq	0x38(%rbx), %r12
 38fd774:      	leaq	0xd0(%rsp), %rax
 38fd77c:      	movq	%rax, 0xc0(%rsp)
 38fd784:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 38fd78e:      	movq	%rax, 0xc8(%rsp)
 38fd796:      	cmpq	%r15, %r12
 38fd799:      	je	0x38fd6b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fd79f:      	leaq	0x14(%rsp), %r14
 38fd7a4:      	jmp	0x38fd7be <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x264e>
 38fd7a6:      	nopw	%cs:(%rax,%rax)
 38fd7b0:      	movq	0x8(%r12), %r12
 38fd7b5:      	cmpq	%r15, %r12
 38fd7b8:      	je	0x38fdb50 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29e0>
 38fd7be:      	movl	0x4cb226c(%rip), %eax   # 0x85afa30 <_ZL8DCELimit+0x78>
 38fd7c4:      	cmpl	$-0x1, %eax
 38fd7c7:      	setne	%cl
 38fd7ca:      	testl	%eax, %eax
 38fd7cc:      	setle	%al
 38fd7cf:      	testb	%al, %cl
 38fd7d1:      	jne	0x38fdb50 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29e0>
 38fd7d7:      	movq	0x8(%rbp), %rdi
 38fd7db:      	movq	(%rdi), %rax
 38fd7de:      	movq	%r12, %rsi
 38fd7e1:      	movq	%r14, %rdx
 38fd7e4:      	leaq	0x54(%rsp), %rcx
 38fd7e9:      	callq	*0x98(%rax)
 38fd7ef:      	testb	%al, %al
 38fd7f1:      	je	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd7f3:      	movl	0x14(%rsp), %eax
 38fd7f7:      	cmpl	$-0x1, %eax
 38fd7fa:      	je	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd7fc:      	cmpl	0x54(%rsp), %eax
 38fd800:      	jne	0x38fd840 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26d0>
 38fd802:      	movl	0xc8(%rsp), %edx
 38fd809:      	cmpl	0xcc(%rsp), %edx
 38fd810:      	jae	0x38fdaf3 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2983>
 38fd816:      	movq	0xc0(%rsp), %rax
 38fd81e:      	movl	%edx, %ecx
 38fd820:      	movq	%r12, (%rax,%rcx,8)
 38fd824:      	incl	0xc8(%rsp)
 38fd82b:      	testb	$0x4, (%r12)
 38fd830:      	je	0x38fd9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fd836:      	jmp	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd83b:      	nopl	(%rax,%rax)
 38fd840:      	testb	$0x4, (%r12)
 38fd845:      	movq	%r12, %rax
 38fd848:      	jne	0x38fd86a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26fa>
 38fd84a:      	testb	$0x8, 0x2c(%r12)
 38fd850:      	movq	%r12, %rax
 38fd853:      	je	0x38fd86a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26fa>
 38fd855:      	movq	%r12, %rax
 38fd858:      	nopl	(%rax,%rax)
 38fd860:      	movq	0x8(%rax), %rax
 38fd864:      	testb	$0x8, 0x2c(%rax)
 38fd868:      	jne	0x38fd860 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26f0>
 38fd86a:      	movq	0x8(%rax), %r13
 38fd86e:      	movq	$0x0, 0xa0(%rsp)
 38fd87a:      	movb	$0x0, 0xa8(%rsp)
 38fd882:      	movq	$0x0, 0x90(%rsp)
 38fd88e:      	movb	$0x0, 0x98(%rsp)
 38fd896:      	movq	0x8(%rbp), %rdi
 38fd89a:      	movq	(%rdi), %rax
 38fd89d:      	movq	%r12, %rsi
 38fd8a0:      	movq	%r14, %rdx
 38fd8a3:      	leaq	0xa0(%rsp), %rcx
 38fd8ab:      	callq	*0x60(%rax)
 38fd8ae:      	testl	%eax, %eax
 38fd8b0:      	je	0x38fd9a0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2830>
 38fd8b6:      	movl	%eax, %ebp
 38fd8b8:      	movq	%r12, %r14
 38fd8bb:      	jmp	0x38fd8c8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2758>
 38fd8bd:      	nopl	(%rax)
 38fd8c0:      	movq	0x8(%r13), %r13
 38fd8c4:      	movq	0x8(%r14), %r14
 38fd8c8:      	cmpq	%r15, %r13
 38fd8cb:      	je	0x38fd930 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27c0>
 38fd8cd:      	movl	0x44(%r13), %eax
 38fd8d1:      	addl	$-0xe, %eax
 38fd8d4:      	cmpw	$0x4, %ax
 38fd8d8:      	ja	0x38fd930 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27c0>
 38fd8da:      	testb	$0x4, (%r13)
 38fd8df:      	jne	0x38fd902 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2792>
 38fd8e1:      	nopw	%cs:(%rax,%rax)
 38fd8eb:      	nopl	(%rax,%rax)
 38fd8f0:      	testb	$0x8, 0x2c(%r13)
 38fd8f5:      	je	0x38fd902 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2792>
 38fd8f7:      	movq	0x8(%r13), %r13
 38fd8fb:      	testb	$0x8, 0x2c(%r13)
 38fd900:      	jne	0x38fd8f7 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2787>
 38fd902:      	testb	$0x4, (%r14)
 38fd906:      	jne	0x38fd8c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd908:      	nopl	(%rax,%rax)
 38fd910:      	testb	$0x8, 0x2c(%r14)
 38fd915:      	je	0x38fd8c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd917:      	movq	0x8(%r14), %r14
 38fd91b:      	testb	$0x8, 0x2c(%r14)
 38fd920:      	jne	0x38fd917 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x27a7>
 38fd922:      	jmp	0x38fd8c0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2750>
 38fd924:      	nopw	%cs:(%rax,%rax)
 38fd92e:      	nop
 38fd930:      	cmpq	%r15, %r13
 38fd933:      	je	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd935:      	movq	(%rsp), %rax
 38fd939:      	movq	0x8(%rax), %rdi
 38fd93d:      	movq	(%rdi), %rax
 38fd940:      	movq	%r13, %rsi
 38fd943:      	leaq	0x54(%rsp), %rdx
 38fd948:      	leaq	0x90(%rsp), %rcx
 38fd950:      	callq	*0x80(%rax)
 38fd956:      	testl	%eax, %eax
 38fd958:      	je	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd95a:      	movl	0x14(%rsp), %ecx
 38fd95e:      	cmpl	0x54(%rsp), %ecx
 38fd962:      	jne	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd964:      	cmpl	%eax, %ebp
 38fd966:      	setne	%al
 38fd969:      	cmpl	$-0x1, %ecx
 38fd96c:      	sete	%dl
 38fd96f:      	orb	%al, %dl
 38fd971:      	je	0x38fd9ce <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x285e>
 38fd973:      	nopw	%cs:(%rax,%rax)
 38fd97d:      	nopl	(%rax)
 38fd980:      	movq	%r14, %r12
 38fd983:      	movq	(%rsp), %rbp
 38fd987:      	leaq	0x14(%rsp), %r14
 38fd98c:      	testb	$0x4, (%r12)
 38fd991:      	jne	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd997:      	jmp	0x38fd9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fd999:      	nopl	(%rax)
 38fd9a0:      	movq	(%rsp), %rbp
 38fd9a4:      	testb	$0x4, (%r12)
 38fd9a9:      	jne	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd9af:      	nop
 38fd9b0:      	testb	$0x8, 0x2c(%r12)
 38fd9b6:      	je	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd9bc:      	movq	0x8(%r12), %r12
 38fd9c1:      	testb	$0x8, 0x2c(%r12)
 38fd9c7:      	jne	0x38fd9bc <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x284c>
 38fd9c9:      	jmp	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fd9ce:      	movq	0xa0(%rsp), %rax
 38fd9d6:      	cmpq	0x90(%rsp), %rax
 38fd9de:      	jne	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd9e0:      	movzbl	0x98(%rsp), %eax
 38fd9e8:      	cmpb	%al, 0xa8(%rsp)
 38fd9ef:      	jne	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fd9f1:      	movq	(%rsp), %rax
 38fd9f5:      	movq	(%rax), %rax
 38fd9f8:      	addl	0x20(%rax), %ecx
 38fd9fb:      	movq	0x8(%rax), %rax
 38fd9ff:      	leaq	(%rcx,%rcx,4), %rcx
 38fda03:      	cmpb	$0x1, 0x12(%rax,%rcx,8)
 38fda08:      	jne	0x38fd980 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2810>
 38fda0e:      	movq	%r13, %rdi
 38fda11:      	movl	%ebp, %esi
 38fda13:      	xorl	%edx, %edx
 38fda15:      	movl	$0x1, %ecx
 38fda1a:      	callq	0x36556b0 <_ZNK4llvm12MachineInstr25findRegisterUseOperandIdxENS_8RegisterEPKNS_18TargetRegisterInfoEb>
 38fda1f:      	movl	0xc8(%rsp), %edx
 38fda26:      	cmpl	$-0x1, %eax
 38fda29:      	je	0x38fdabb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x294b>
 38fda2f:      	cmpl	0xcc(%rsp), %edx
 38fda36:      	movq	(%rsp), %rbp
 38fda3a:      	jae	0x38fdb1c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x29ac>
 38fda40:      	movq	0xc0(%rsp), %rax
 38fda48:      	movl	%edx, %ecx
 38fda4a:      	movq	%r12, (%rax,%rcx,8)
 38fda4e:      	movl	0xc8(%rsp), %edx
 38fda55:      	incl	%edx
 38fda57:      	movl	%edx, 0xc8(%rsp)
 38fda5e:      	cmpl	0xcc(%rsp), %edx
 38fda65:      	jae	0x38fdac8 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2958>
 38fda67:      	movq	0xc0(%rsp), %rax
 38fda6f:      	movl	%edx, %ecx
 38fda71:      	movq	%r13, (%rax,%rcx,8)
 38fda75:      	incl	0xc8(%rsp)
 38fda7c:      	testb	$0x4, (%r14)
 38fda80:      	jne	0x38fdaa2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2932>
 38fda82:      	nopw	%cs:(%rax,%rax)
 38fda8c:      	nopl	(%rax)
 38fda90:      	testb	$0x8, 0x2c(%r14)
 38fda95:      	je	0x38fdaa2 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2932>
 38fda97:      	movq	0x8(%r14), %r14
 38fda9b:      	testb	$0x8, 0x2c(%r14)
 38fdaa0:      	jne	0x38fda97 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2927>
 38fdaa2:      	movq	0x8(%r14), %r12
 38fdaa6:      	leaq	0x14(%rsp), %r14
 38fdaab:      	testb	$0x4, (%r12)
 38fdab0:      	je	0x38fd9b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2840>
 38fdab6:      	jmp	0x38fd7b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2640>
 38fdabb:      	movq	(%rsp), %rbp
 38fdabf:      	cmpl	0xcc(%rsp), %edx
 38fdac6:      	jb	0x38fda67 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28f7>
 38fdac8:      	movl	%edx, %edx
 38fdaca:      	incq	%rdx
 38fdacd:      	movl	$0x8, %ecx
 38fdad2:      	leaq	0xc0(%rsp), %rdi
 38fdada:      	leaq	0xd0(%rsp), %rsi
 38fdae2:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdae7:      	movl	0xc8(%rsp), %edx
 38fdaee:      	jmp	0x38fda67 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28f7>
 38fdaf3:      	incq	%rdx
 38fdaf6:      	movl	$0x8, %ecx
 38fdafb:      	leaq	0xc0(%rsp), %rdi
 38fdb03:      	leaq	0xd0(%rsp), %rsi
 38fdb0b:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdb10:      	movl	0xc8(%rsp), %edx
 38fdb17:      	jmp	0x38fd816 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x26a6>
 38fdb1c:      	incq	%rdx
 38fdb1f:      	movl	$0x8, %ecx
 38fdb24:      	leaq	0xc0(%rsp), %rdi
 38fdb2c:      	leaq	0xd0(%rsp), %rsi
 38fdb34:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fdb39:      	movl	0xc8(%rsp), %edx
 38fdb40:      	jmp	0x38fda40 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x28d0>
 38fdb45:      	nopw	%cs:(%rax,%rax)
 38fdb4f:      	nop
 38fdb50:      	movq	0xc0(%rsp), %r14
 38fdb58:      	movl	0xc8(%rsp), %eax
 38fdb5f:      	testq	%rax, %rax
 38fdb62:      	je	0x38fdc6b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2afb>
 38fdb68:      	movq	%rbx, %r15
 38fdb6b:      	leaq	(%r14,%rax,8), %rbx
 38fdb6f:      	jmp	0x38fdb92 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a22>
 38fdb71:      	nopw	%cs:(%rax,%rax)
 38fdb7b:      	nopl	(%rax,%rax)
 38fdb80:      	callq	0x36546c0 <_ZN4llvm12MachineInstr15eraseFromParentEv>
 38fdb85:      	addq	$0x8, %r14
 38fdb89:      	cmpq	%rbx, %r14
 38fdb8c:      	je	0x38fdc60 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2af0>
 38fdb92:      	movq	(%r14), %rdi
 38fdb95:      	movq	0x20(%rbp), %rax
 38fdb99:      	testq	%rax, %rax
 38fdb9c:      	je	0x38fdb80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdb9e:      	movq	0x78(%rax), %rcx
 38fdba2:      	movl	0x88(%rax), %edx
 38fdba8:      	testq	%rdx, %rdx
 38fdbab:      	je	0x38fdc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa0>
 38fdbad:      	movl	%edi, %r8d
 38fdbb0:      	shrl	$0x4, %r8d
 38fdbb4:      	movl	%edi, %esi
 38fdbb6:      	shrl	$0x9, %esi
 38fdbb9:      	xorl	%r8d, %esi
 38fdbbc:      	leal	-0x1(%rdx), %r8d
 38fdbc0:      	andl	%r8d, %esi
 38fdbc3:      	movl	%esi, %r9d
 38fdbc6:      	shll	$0x4, %r9d
 38fdbca:      	movq	(%rcx,%r9), %r11
 38fdbce:      	cmpq	%r11, %rdi
 38fdbd1:      	je	0x38fdc17 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa7>
 38fdbd3:      	movl	$0x1, %r10d
 38fdbd9:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 38fdbe0:      	je	0x38fdc10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aa0>
 38fdbe2:      	addl	%r10d, %esi
 38fdbe5:      	incl	%r10d
 38fdbe8:      	andl	%r8d, %esi
 38fdbeb:      	movq	%rsi, %r11
 38fdbee:      	shlq	$0x4, %r11
 38fdbf2:      	leaq	(%rcx,%r11), %r9
 38fdbf6:      	movq	(%rcx,%r11), %r11
 38fdbfa:      	cmpq	%r11, %rdi
 38fdbfd:      	je	0x38fdc1a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2aaa>
 38fdbff:      	jmp	0x38fdbd9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a69>
 38fdc01:      	nopw	%cs:(%rax,%rax)
 38fdc0b:      	nopl	(%rax,%rax)
 38fdc10:      	movq	%rdx, %r9
 38fdc13:      	shlq	$0x4, %r9
 38fdc17:      	addq	%rcx, %r9
 38fdc1a:      	shlq	$0x4, %rdx
 38fdc1e:      	addq	%rdx, %rcx
 38fdc21:      	cmpq	%rcx, %r9
 38fdc24:      	je	0x38fdb80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdc2a:      	movq	0x8(%r9), %rcx
 38fdc2e:      	andq	$-0x8, %rcx
 38fdc32:      	movq	$-0x2000, (%r9)         # imm = 0xE000
 38fdc39:      	movq	0x80(%rax), %xmm0
 38fdc41:      	paddd	-0x2ada919(%rip), %xmm0 # 0xe23330 <.LCPI9_4>
 38fdc49:      	movq	%xmm0, 0x80(%rax)
 38fdc51:      	movq	$0x0, 0x10(%rcx)
 38fdc59:      	jmp	0x38fdb80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2a10>
 38fdc5e:      	nop
 38fdc60:      	movq	0xc0(%rsp), %r14
 38fdc68:      	movq	%r15, %rbx
 38fdc6b:      	leaq	0xd0(%rsp), %rax
 38fdc73:      	cmpq	%rax, %r14
 38fdc76:      	je	0x38fd6b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fdc7c:      	movq	%r14, %rdi
 38fdc7f:      	callq	0x828a640 <free@plt>
 38fdc84:      	jmp	0x38fd6b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2540>
 38fdc89:      	movl	0x5d0(%rbp), %eax
 38fdc8f:      	movq	%rax, 0x38(%rsp)
 38fdc94:      	testq	%rax, %rax
 38fdc97:      	je	0x38fddd6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fdc9d:      	movq	(%rsp), %rax
 38fdca1:      	movq	0x668(%rax), %rcx
 38fdca8:      	movq	%rcx, 0x8(%rsp)
 38fdcad:      	movq	(%rax), %rcx
 38fdcb0:      	movq	%rcx, 0x18(%rsp)
 38fdcb5:      	movq	0x5c8(%rax), %rdi
 38fdcbc:      	xorl	%r8d, %r8d
 38fdcbf:      	jmp	0x38fdcde <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b6e>
 38fdcc1:      	nopw	%cs:(%rax,%rax)
 38fdccb:      	nopl	(%rax,%rax)
 38fdcd0:      	incq	%r8
 38fdcd3:      	cmpq	0x38(%rsp), %r8
 38fdcd8:      	je	0x38fddd6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c66>
 38fdcde:      	movq	0x8(%rsp), %rax
 38fdce3:      	movl	(%rax,%r8,4), %ebp
 38fdce7:      	cmpl	$-0x1, %ebp
 38fdcea:      	je	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdcec:      	movq	0x18(%rsp), %rax
 38fdcf1:      	movl	0x20(%rax), %r9d
 38fdcf5:      	movq	0x8(%rax), %r10
 38fdcf9:      	leaq	(%r8,%r8,8), %rax
 38fdcfd:      	leaq	(%rdi,%rax,8), %r11
 38fdd01:      	movl	0x40(%rdi,%rax,8), %ebx
 38fdd05:      	leal	-0x1(%rbx), %ecx
 38fdd08:      	movl	%ecx, %r14d
 38fdd0b:      	notb	%cl
 38fdd0d:      	movq	$-0x1, %r15
 38fdd14:      	shrq	%cl, %r15
 38fdd17:      	shrl	$0x6, %r14d
 38fdd1b:      	movl	%r14d, %r12d
 38fdd1e:      	incl	%r12d
 38fdd21:      	leaq	-0x1(%r14), %r13
 38fdd25:      	jmp	0x38fdd3a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bca>
 38fdd27:      	incl	%ebp
 38fdd29:      	movl	%ebp, %edx
 38fdd2b:      	tzcntq	%rax, %rbp
 38fdd30:      	shll	$0x6, %edx
 38fdd33:      	orl	%edx, %ebp
 38fdd35:      	cmpl	$-0x1, %ebp
 38fdd38:      	je	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdd3a:      	leal	(%rbp,%r9), %eax
 38fdd3f:      	leaq	(%rax,%rax,4), %rax
 38fdd43:      	movq	$-0x1, 0x8(%r10,%rax,8)
 38fdd4c:      	incl	%ebp
 38fdd4e:      	cmpl	%ebx, %ebp
 38fdd50:      	je	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdd56:      	movl	%ebp, %edx
 38fdd58:      	shrl	$0x6, %edx
 38fdd5b:      	cmpl	%r14d, %edx
 38fdd5e:      	ja	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fdd64:      	andl	$0x3f, %ebp
 38fdd67:      	movl	%ebp, %ecx
 38fdd69:      	negb	%cl
 38fdd6b:      	movq	$-0x1, %rax
 38fdd72:      	shrq	%cl, %rax
 38fdd75:      	movq	(%r11), %rcx
 38fdd78:      	notq	%rax
 38fdd7b:      	cmpl	$0x1, %ebp
 38fdd7e:      	movl	$0x0, %esi
 38fdd83:      	sbbq	%rsi, %rsi
 38fdd86:      	orq	%rax, %rsi
 38fdd89:      	cmpl	%r14d, %edx
 38fdd8c:      	movq	$-0x1, %rax
 38fdd93:      	cmoveq	%r15, %rax
 38fdd97:      	movl	%edx, %ebp
 38fdd99:      	andq	%rsi, %rax
 38fdd9c:      	andq	(%rcx,%rbp,8), %rax
 38fdda0:      	jne	0x38fdd2b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bbb>
 38fdda2:      	leal	0x1(%rbp), %eax
 38fdda5:      	cmpl	%r12d, %eax
 38fdda8:      	je	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fddae:      	nop
 38fddb0:      	cmpq	%rbp, %r13
 38fddb3:      	movq	$-0x1, %rax
 38fddba:      	cmoveq	%r15, %rax
 38fddbe:      	andq	0x8(%rcx,%rbp,8), %rax
 38fddc3:      	jne	0x38fdd27 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2bb7>
 38fddc9:      	incq	%rbp
 38fddcc:      	cmpq	%rbp, %r14
 38fddcf:      	jne	0x38fddb0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c40>
 38fddd1:      	jmp	0x38fdcd0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2b60>
 38fddd6:      	movq	0x1c0(%rsp), %rdi
 38fddde:      	cmpq	0x80(%rsp), %rdi
 38fdde6:      	je	0x38fdded <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2c7d>
 38fdde8:      	callq	0x828a640 <free@plt>
 38fdded:      	movq	0x258(%rsp), %rdi
 38fddf5:      	movl	0x260(%rsp), %ebx
 38fddfc:      	testq	%rbx, %rbx
 38fddff:      	leaq	0x218(%rsp), %r15
 38fde07:      	je	0x38fe14c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fdc>
 38fde0d:      	shlq	$0x5, %rbx
 38fde11:      	leaq	-0x10(%rbx,%rdi), %r14
 38fde16:      	negq	%rbx
 38fde19:      	movq	(%rsp), %r13
 38fde1d:      	jmp	0x38fde2a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cba>
 38fde1f:      	nop
 38fde20:      	addq	$-0x20, %r14
 38fde24:      	addq	$0x20, %rbx
 38fde28:      	je	0x38fde3a <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cca>
 38fde2a:      	movq	-0x10(%r14), %rdi
 38fde2e:      	cmpq	%rdi, %r14
 38fde31:      	je	0x38fde20 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cb0>
 38fde33:      	callq	0x828a640 <free@plt>
 38fde38:      	jmp	0x38fde20 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cb0>
 38fde3a:      	movq	0x258(%rsp), %rdi
 38fde42:      	cmpq	0x68(%rsp), %rdi
 38fde47:      	je	0x38fde4e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cde>
 38fde49:      	callq	0x828a640 <free@plt>
 38fde4e:      	movq	0x170(%rsp), %rdi
 38fde56:      	cmpq	0x60(%rsp), %rdi
 38fde5b:      	je	0x38fde62 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cf2>
 38fde5d:      	callq	0x828a640 <free@plt>
 38fde62:      	movq	0x208(%rsp), %rdi
 38fde6a:      	cmpq	%r15, %rdi
 38fde6d:      	je	0x38fde74 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d04>
 38fde6f:      	callq	0x828a640 <free@plt>
 38fde74:      	movl	0x670(%r13), %edx
 38fde7b:      	testq	%rdx, %rdx
 38fde7e:      	je	0x38fde96 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d26>
 38fde80:      	shlq	$0x2, %rdx
 38fde84:      	movq	0x48(%rsp), %rax
 38fde89:      	movq	(%rax), %rdi
 38fde8c:      	movl	$0xff, %esi
 38fde91:      	callq	0x828ab90 <memset@plt>
 38fde96:      	movq	0x28(%r13), %rax
 38fde9a:      	cmpq	%rax, 0x30(%r13)
 38fde9e:      	je	0x38fdea4 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d34>
 38fdea0:      	movq	%rax, 0x30(%r13)
 38fdea4:      	movl	0x48(%r13), %eax
 38fdea8:      	testq	%rax, %rax
 38fdeab:      	je	0x38fdf9b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fdeb1:      	movq	0x40(%r13), %rbx
 38fdeb5:      	shlq	$0x4, %rax
 38fdeb9:      	leaq	(%rax,%rax,4), %rsi
 38fdebd:      	leaq	-0x50(%rsi), %rcx
 38fdec1:      	movabsq	$-0x3333333333333333, %rdx # imm = 0xCCCCCCCCCCCCCCCD
 38fdecb:      	movq	%rcx, %rax
 38fdece:      	mulq	%rdx
 38fded1:      	shrq	$0x6, %rdx
 38fded5:      	movl	%edx, %edi
 38fded7:      	notl	%edi
 38fded9:      	movq	%rbx, %rax
 38fdedc:      	testb	$0x7, %dil
 38fdee0:      	je	0x38fdf00 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d90>
 38fdee2:      	incl	%edx
 38fdee4:      	andl	$0x7, %edx
 38fdee7:      	movq	%rbx, %rax
 38fdeea:      	nopw	(%rax,%rax)
 38fdef0:      	movl	$0x0, 0x8(%rax)
 38fdef7:      	addq	$0x50, %rax
 38fdefb:      	decq	%rdx
 38fdefe:      	jne	0x38fdef0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2d80>
 38fdf00:      	cmpq	$0x230, %rcx            # imm = 0x230
 38fdf07:      	jb	0x38fdf65 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2df5>
 38fdf09:      	addq	%rbx, %rsi
 38fdf0c:      	nopl	(%rax)
 38fdf10:      	movl	$0x0, 0x8(%rax)
 38fdf17:      	movl	$0x0, 0x58(%rax)
 38fdf1e:      	movl	$0x0, 0xa8(%rax)
 38fdf28:      	movl	$0x0, 0xf8(%rax)
 38fdf32:      	movl	$0x0, 0x148(%rax)
 38fdf3c:      	movl	$0x0, 0x198(%rax)
 38fdf46:      	movl	$0x0, 0x1e8(%rax)
 38fdf50:      	movl	$0x0, 0x238(%rax)
 38fdf5a:      	addq	$0x280, %rax            # imm = 0x280
 38fdf60:      	cmpq	%rsi, %rax
 38fdf63:      	jne	0x38fdf10 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2da0>
 38fdf65:      	movl	0x48(%r13), %eax
 38fdf69:      	testq	%rax, %rax
 38fdf6c:      	je	0x38fdf9b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fdf6e:      	shlq	$0x4, %rax
 38fdf72:      	leaq	(%rax,%rax,4), %r14
 38fdf76:      	leaq	-0x40(%rbx), %r15
 38fdf7a:      	jmp	0x38fdf86 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e16>
 38fdf7c:      	nopl	(%rax)
 38fdf80:      	addq	$-0x50, %r14
 38fdf84:      	je	0x38fdf9b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e2b>
 38fdf86:      	movq	-0x50(%rbx,%r14), %rdi
 38fdf8b:      	leaq	(%r15,%r14), %rax
 38fdf8f:      	cmpq	%rdi, %rax
 38fdf92:      	je	0x38fdf80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e10>
 38fdf94:      	callq	0x828a640 <free@plt>
 38fdf99:      	jmp	0x38fdf80 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e10>
 38fdf9b:      	movl	$0x0, 0x48(%r13)
 38fdfa3:      	movq	$0x0, 0x558(%r13)
 38fdfae:      	movl	$0x0, 0x580(%r13)
 38fdfb9:      	movl	0x5d0(%r13), %eax
 38fdfc0:      	testq	%rax, %rax
 38fdfc3:      	je	0x38fdffb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e8b>
 38fdfc5:      	movq	0x5c8(%r13), %rbx
 38fdfcc:      	shlq	$0x3, %rax
 38fdfd0:      	leaq	(%rax,%rax,8), %r14
 38fdfd4:      	leaq	-0x38(%rbx), %r15
 38fdfd8:      	jmp	0x38fdfe6 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e76>
 38fdfda:      	nopw	(%rax,%rax)
 38fdfe0:      	addq	$-0x48, %r14
 38fdfe4:      	je	0x38fdffb <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e8b>
 38fdfe6:      	movq	-0x48(%rbx,%r14), %rdi
 38fdfeb:      	leaq	(%r15,%r14), %rax
 38fdfef:      	cmpq	%rdi, %rax
 38fdff2:      	je	0x38fdfe0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e70>
 38fdff4:      	callq	0x828a640 <free@plt>
 38fdff9:      	jmp	0x38fdfe0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2e70>
 38fdffb:      	movl	$0x0, 0x5d0(%r13)
 38fe006:      	movl	0x688(%r13), %eax
 38fe00d:      	testq	%rax, %rax
 38fe010:      	je	0x38fe04b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2edb>
 38fe012:      	movq	0x680(%r13), %rbx
 38fe019:      	shlq	$0x3, %rax
 38fe01d:      	leaq	(%rax,%rax,8), %r14
 38fe021:      	leaq	-0x38(%rbx), %r15
 38fe025:      	jmp	0x38fe036 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec6>
 38fe027:      	nopw	(%rax,%rax)
 38fe030:      	addq	$-0x48, %r14
 38fe034:      	je	0x38fe04b <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2edb>
 38fe036:      	movq	-0x48(%rbx,%r14), %rdi
 38fe03b:      	leaq	(%r15,%r14), %rax
 38fe03f:      	cmpq	%rdi, %rax
 38fe042:      	je	0x38fe030 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec0>
 38fe044:      	callq	0x828a640 <free@plt>
 38fe049:      	jmp	0x38fe030 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2ec0>
 38fe04b:      	movl	$0x0, 0x688(%r13)
 38fe056:      	movl	0x790(%r13), %eax
 38fe05d:      	testq	%rax, %rax
 38fe060:      	je	0x38fe128 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fb8>
 38fe066:      	movq	0x788(%r13), %rbx
 38fe06d:      	imulq	$0xe8, %rax, %r15
 38fe074:      	leaq	-0x3438db(%rip), %r14   # 0x35ba7a0 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10deleteNodeENS_15IntervalMapImpl7NodeRefEj>
 38fe07b:      	jmp	0x38fe099 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f29>
 38fe07d:      	nopl	(%rax)
 38fe080:      	movl	$0x0, 0xcc(%r12)
 38fe08c:      	addq	$-0xe8, %r15
 38fe093:      	je	0x38fe128 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2fb8>
 38fe099:      	movq	-0xe0(%rbx,%r15), %r12
 38fe0a1:      	testq	%r12, %r12
 38fe0a4:      	je	0x38fe08c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f1c>
 38fe0a6:      	cmpl	$0x0, 0xc8(%r12)
 38fe0af:      	je	0x38fe080 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f10>
 38fe0b1:      	leaq	0x8(%r12), %rdi
 38fe0b6:      	movq	%r14, %rsi
 38fe0b9:      	xorl	%edx, %edx
 38fe0bb:      	callq	0x35ba460 <_ZN4llvm11IntervalMapINS_9SlotIndexEPKNS_12LiveIntervalELj8ENS_15IntervalMapInfoIS1_EEE10visitNodesEMS7_FvNS_15IntervalMapImpl7NodeRefEjE>
 38fe0c0:      	xorps	%xmm0, %xmm0
 38fe0c3:      	movups	%xmm0, 0xb8(%r12)
 38fe0cc:      	movups	%xmm0, 0xa8(%r12)
 38fe0d5:      	movups	%xmm0, 0x98(%r12)
 38fe0de:      	movups	%xmm0, 0x88(%r12)
 38fe0e7:      	movl	$0x0, 0xc8(%r12)
 38fe0f3:      	movups	%xmm0, 0x18(%r12)
 38fe0f9:      	movups	%xmm0, 0x8(%r12)
 38fe0ff:      	movups	%xmm0, 0x38(%r12)
 38fe105:      	movups	%xmm0, 0x28(%r12)
 38fe10b:      	movups	%xmm0, 0x58(%r12)
 38fe111:      	movups	%xmm0, 0x48(%r12)
 38fe117:      	movups	%xmm0, 0x78(%r12)
 38fe11d:      	movups	%xmm0, 0x68(%r12)
 38fe123:      	jmp	0x38fe080 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2f10>
 38fe128:      	movl	$0x0, 0x790(%r13)
 38fe133:      	movq	0x30(%rsp), %rax
 38fe138:      	andb	$0x1, %al
 38fe13a:      	addq	$0x468, %rsp            # imm = 0x468
 38fe141:      	popq	%rbx
 38fe142:      	popq	%r12
 38fe144:      	popq	%r13
 38fe146:      	popq	%r14
 38fe148:      	popq	%r15
 38fe14a:      	popq	%rbp
 38fe14b:      	retq
 38fe14c:      	movq	(%rsp), %r13
 38fe150:      	cmpq	0x68(%rsp), %rdi
 38fe155:      	jne	0x38fde49 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cd9>
 38fe15b:      	jmp	0x38fde4e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x2cde>
 38fe160:      	movq	%r12, %rbx
 38fe163:      	jmp	0x38fe1a9 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3039>
 38fe165:      	nopw	%cs:(%rax,%rax)
 38fe16f:      	nop
 38fe170:      	movq	%rbx, %rdx
 38fe173:      	subq	%r12, %rdx
 38fe176:      	movq	%rdx, %rax
 38fe179:      	sarq	$0x3, %rax
 38fe17d:      	cmpq	$0x2, %rax
 38fe181:      	jl	0x38fe1e1 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3071>
 38fe183:      	shlq	$0x3, %rax
 38fe187:      	subq	%rax, %rdi
 38fe18a:      	addq	$0x10, %rdi
 38fe18e:      	movq	%r12, %rsi
 38fe191:      	callq	0x828abc0 <memmove@plt>
 38fe196:      	movq	%r12, %rax
 38fe199:      	movq	%r14, (%rax)
 38fe19c:      	leaq	0x8(%rbx), %rbp
 38fe1a0:      	cmpq	%r15, %rbp
 38fe1a3:      	je	0x38fc3b0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1240>
 38fe1a9:      	movq	%rbx, %rdi
 38fe1ac:      	movq	%rbp, %rbx
 38fe1af:      	movq	(%rbp), %r14
 38fe1b3:      	movq	(%r12), %rsi
 38fe1b7:      	movl	(%r14), %ecx
 38fe1ba:      	cmpl	(%rsi), %ecx
 38fe1bc:      	jl	0x38fe170 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3000>
 38fe1be:      	movq	(%rdi), %rdx
 38fe1c1:      	movq	%rbx, %rax
 38fe1c4:      	cmpl	(%rdx), %ecx
 38fe1c6:      	jge	0x38fe199 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe1c8:      	movq	%rbx, %rax
 38fe1cb:      	nopl	(%rax,%rax)
 38fe1d0:      	movq	%rdx, (%rax)
 38fe1d3:      	movq	-0x10(%rax), %rdx
 38fe1d7:      	addq	$-0x8, %rax
 38fe1db:      	cmpl	(%rdx), %ecx
 38fe1dd:      	jl	0x38fe1d0 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3060>
 38fe1df:      	jmp	0x38fe199 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe1e1:      	movq	%r12, %rax
 38fe1e4:      	cmpq	$0x8, %rdx
 38fe1e8:      	jne	0x38fe199 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3029>
 38fe1ea:      	movq	%rsi, 0x8(%rdi)
 38fe1ee:      	jmp	0x38fe196 <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x3026>
 38fe1f0:      	xorl	%r12d, %r12d
 38fe1f3:      	jmp	0x38fcd7c <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0x1c0c>
 38fe1f8:      	leaq	0x10(%r13), %rsi
 38fe1fc:      	movl	$0x8, %ecx
 38fe201:      	movq	%r13, %rdi
 38fe204:      	movq	0x28(%rsp), %rdx
 38fe209:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fe20e:      	movl	0x8(%r13), %edi
 38fe212:      	movl	0x40(%r13), %ebp
 38fe216:      	movl	%edi, %ebx
 38fe218:      	jmp	0x38fbd6e <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xbfe>
 38fe21d:      	leaq	0x10(%r13), %rsi
 38fe221:      	movl	$0x8, %ecx
 38fe226:      	movq	%r13, %rdi
 38fe229:      	movq	0x28(%rsp), %rdx
 38fe22e:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 38fe233:      	movl	0x8(%r13), %edi
 38fe237:      	movl	0x40(%r13), %ebp
 38fe23b:      	movl	%edi, %ebx
 38fe23d:      	jmp	0x38fbe0f <_ZN12_GLOBAL__N_117StackSlotColoring3runERN4llvm15MachineFunctionE+0xc9f>
 38fe242:      	leaq	-0x2c6385f(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 38fe249:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
