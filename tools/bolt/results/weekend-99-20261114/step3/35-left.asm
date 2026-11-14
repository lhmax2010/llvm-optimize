
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005de1380 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_>:
 5de1380:      	testl	%esi, %esi
 5de1382:      	je	0x5de14b2 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x132>
 5de1388:      	pushq	%rbp
 5de1389:      	pushq	%r15
 5de138b:      	pushq	%r14
 5de138d:      	pushq	%r13
 5de138f:      	pushq	%r12
 5de1391:      	pushq	%rbx
 5de1392:      	subq	$0x18, %rsp
 5de1396:      	movl	%esi, %ebp
 5de1398:      	movq	%rdi, %rbx
 5de139b:      	movl	%esi, %eax
 5de139d:      	leaq	(%rax,%rax,2), %rcx
 5de13a1:      	leaq	(%rdi,%rcx,8), %r14
 5de13a5:      	bsrq	%rax, %rdx
 5de13a9:      	xorl	$0x3f, %edx
 5de13ac:      	addl	%edx, %edx
 5de13ae:      	xorq	$0x7e, %rdx
 5de13b2:      	movq	%r14, %rsi
 5de13b5:      	callq	0x5df4150 <_ZSt16__introsort_loopIPZN4llvm19SelectionDAGBuilder18visitIntrinsicCallERKNS0_8CallInstEjE18BranchFunnelTargetlN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_18visitIntrinsicCallES4_jE3$_1EEEvT_SC_T0_T1_>
 5de13ba:      	leaq	0x18(%rbx), %r15
 5de13be:      	cmpl	$0x11, %ebp
 5de13c1:      	jb	0x5de149f <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x11f>
 5de13c7:      	movl	$0x18, %r12d
 5de13cd:      	movq	%r15, %r13
 5de13d0:      	movq	%rbx, %rax
 5de13d3:      	jmp	0x5de1403 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x83>
 5de13d5:      	nopw	%cs:(%rax,%rax)
 5de13df:      	nop
 5de13e0:      	movq	%rcx, (%rdx)
 5de13e3:      	movaps	(%rsp), %xmm0
 5de13e7:      	movups	%xmm0, 0x8(%rdx)
 5de13eb:      	addq	$0x18, %r12
 5de13ef:      	addq	$0x18, %r13
 5de13f3:      	movq	%rbp, %rax
 5de13f6:      	cmpq	$0x180, %r12            # imm = 0x180
 5de13fd:      	je	0x5de14b3 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x133>
 5de1403:      	leaq	(%rbx,%r12), %rbp
 5de1407:      	movq	(%rbx,%r12), %rcx
 5de140b:      	cmpq	(%rbx), %rcx
 5de140e:      	jge	0x5de1450 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xd0>
 5de1410:      	movq	0x10(%rbp), %rcx
 5de1414:      	movq	%rcx, 0x10(%rsp)
 5de1419:      	movups	(%rbp), %xmm0
 5de141d:      	movaps	%xmm0, (%rsp)
 5de1421:      	cmpq	$0x19, %r12
 5de1425:      	jb	0x5de148e <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x10e>
 5de1427:      	movq	%r15, %rdi
 5de142a:      	movq	%rbx, %rsi
 5de142d:      	movq	%r12, %rdx
 5de1430:      	callq	0x828ac50 <memmove@plt>
 5de1435:      	movq	0x10(%rsp), %rax
 5de143a:      	movq	%rax, 0x10(%rbx)
 5de143e:      	movaps	(%rsp), %xmm0
 5de1442:      	movups	%xmm0, (%rbx)
 5de1445:      	jmp	0x5de13eb <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x6b>
 5de1447:      	nopw	(%rax,%rax)
 5de1450:      	movups	0x20(%rax), %xmm0
 5de1454:      	movaps	%xmm0, (%rsp)
 5de1458:      	movq	%rbp, %rdx
 5de145b:      	cmpq	(%rax), %rcx
 5de145e:      	jge	0x5de13e0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x60>
 5de1460:      	movq	%r13, %rdx
 5de1463:      	nopw	%cs:(%rax,%rax)
 5de146d:      	nopl	(%rax)
 5de1470:      	movq	-0x8(%rdx), %rax
 5de1474:      	movq	%rax, 0x10(%rdx)
 5de1478:      	movups	-0x18(%rdx), %xmm0
 5de147c:      	movups	%xmm0, (%rdx)
 5de147f:      	cmpq	-0x30(%rdx), %rcx
 5de1483:      	leaq	-0x18(%rdx), %rdx
 5de1487:      	jl	0x5de1470 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xf0>
 5de1489:      	jmp	0x5de13e0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x60>
 5de148e:      	movq	0x10(%rbx), %rcx
 5de1492:      	movq	%rcx, 0x28(%rax)
 5de1496:      	movups	(%rbx), %xmm0
 5de1499:      	movups	%xmm0, 0x18(%rax)
 5de149d:      	jmp	0x5de1435 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xb5>
 5de149f:      	cmpl	$0x1, %ebp
 5de14a2:      	jne	0x5de150b <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x18b>
 5de14a4:      	addq	$0x18, %rsp
 5de14a8:      	popq	%rbx
 5de14a9:      	popq	%r12
 5de14ab:      	popq	%r13
 5de14ad:      	popq	%r14
 5de14af:      	popq	%r15
 5de14b1:      	popq	%rbp
 5de14b2:      	retq
 5de14b3:      	addq	$0x180, %rbx            # imm = 0x180
 5de14ba:      	jmp	0x5de14d4 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x154>
 5de14bc:      	nopl	(%rax)
 5de14c0:      	movq	%rax, (%rcx)
 5de14c3:      	movaps	(%rsp), %xmm0
 5de14c7:      	movups	%xmm0, 0x8(%rcx)
 5de14cb:      	addq	$0x18, %rbx
 5de14cf:      	cmpq	%r14, %rbx
 5de14d2:      	je	0x5de14a4 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de14d4:      	movq	(%rbx), %rax
 5de14d7:      	movups	0x8(%rbx), %xmm0
 5de14db:      	movaps	%xmm0, (%rsp)
 5de14df:      	movq	%rbx, %rcx
 5de14e2:      	cmpq	-0x18(%rbx), %rax
 5de14e6:      	jge	0x5de14c0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x140>
 5de14e8:      	movq	%rbx, %rcx
 5de14eb:      	nopl	(%rax,%rax)
 5de14f0:      	movq	-0x8(%rcx), %rdx
 5de14f4:      	movq	%rdx, 0x10(%rcx)
 5de14f8:      	movups	-0x18(%rcx), %xmm0
 5de14fc:      	movups	%xmm0, (%rcx)
 5de14ff:      	cmpq	-0x30(%rcx), %rax
 5de1503:      	leaq	-0x18(%rcx), %rcx
 5de1507:      	jl	0x5de14f0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x170>
 5de1509:      	jmp	0x5de14c0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x140>
 5de150b:      	movabsq	$-0x5555555555555555, %r12 # imm = 0xAAAAAAAAAAAAAAAB
 5de1515:      	movq	%rbx, %rax
 5de1518:      	jmp	0x5de153b <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1bb>
 5de151a:      	nopw	(%rax,%rax)
 5de1520:      	movq	%rcx, (%rdx)
 5de1523:      	movaps	(%rsp), %xmm0
 5de1527:      	movups	%xmm0, 0x8(%rdx)
 5de152b:      	leaq	0x18(%r13), %r15
 5de152f:      	movq	%r13, %rax
 5de1532:      	cmpq	%r14, %r15
 5de1535:      	je	0x5de14a4 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de153b:      	movq	%r15, %r13
 5de153e:      	movq	(%r15), %rcx
 5de1541:      	cmpq	(%rbx), %rcx
 5de1544:      	jge	0x5de15b0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x230>
 5de1546:      	movq	0x10(%r13), %rcx
 5de154a:      	movq	%rcx, 0x10(%rsp)
 5de154f:      	movups	(%r13), %xmm0
 5de1554:      	movaps	%xmm0, (%rsp)
 5de1558:      	movq	%r13, %rdx
 5de155b:      	subq	%rbx, %rdx
 5de155e:      	cmpq	$0x19, %rdx
 5de1562:      	jl	0x5de15ee <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x26e>
 5de1568:      	movq	%rdx, %rcx
 5de156b:      	shrq	$0x3, %rcx
 5de156f:      	imulq	%r12, %rcx
 5de1573:      	negq	%rcx
 5de1576:      	leaq	(%rcx,%rcx,2), %rcx
 5de157a:      	leaq	0x30(%rax,%rcx,8), %rdi
 5de157f:      	movq	%rbx, %rsi
 5de1582:      	callq	0x828ac50 <memmove@plt>
 5de1587:      	movq	0x10(%rsp), %rax
 5de158c:      	movq	%rax, 0x10(%rbx)
 5de1590:      	movaps	(%rsp), %xmm0
 5de1594:      	movups	%xmm0, (%rbx)
 5de1597:      	leaq	0x18(%r13), %r15
 5de159b:      	movq	%r13, %rax
 5de159e:      	cmpq	%r14, %r15
 5de15a1:      	jne	0x5de153b <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1bb>
 5de15a3:      	jmp	0x5de14a4 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de15a8:      	nopl	(%rax,%rax)
 5de15b0:      	movups	0x20(%rax), %xmm0
 5de15b4:      	movaps	%xmm0, (%rsp)
 5de15b8:      	movq	%r13, %rdx
 5de15bb:      	cmpq	(%rax), %rcx
 5de15be:      	jge	0x5de1520 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1a0>
 5de15c4:      	movq	%r13, %rdx
 5de15c7:      	nopw	(%rax,%rax)
 5de15d0:      	movq	-0x8(%rdx), %rax
 5de15d4:      	movq	%rax, 0x10(%rdx)
 5de15d8:      	movups	-0x18(%rdx), %xmm0
 5de15dc:      	movups	%xmm0, (%rdx)
 5de15df:      	cmpq	-0x30(%rdx), %rcx
 5de15e3:      	leaq	-0x18(%rdx), %rdx
 5de15e7:      	jl	0x5de15d0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x250>
 5de15e9:      	jmp	0x5de1520 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1a0>
 5de15ee:      	cmpq	$0x18, %rdx
 5de15f2:      	jne	0x5de1587 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x207>
 5de15f4:      	movq	0x10(%rbx), %rcx
 5de15f8:      	movq	%rcx, 0x28(%rax)
 5de15fc:      	movups	(%rbx), %xmm0
 5de15ff:      	movups	%xmm0, 0x18(%rax)
 5de1603:      	jmp	0x5de1587 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x207>
