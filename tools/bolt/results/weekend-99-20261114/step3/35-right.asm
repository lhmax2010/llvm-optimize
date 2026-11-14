
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005de1300 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_>:
 5de1300:      	testl	%esi, %esi
 5de1302:      	je	0x5de1432 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x132>
 5de1308:      	pushq	%rbp
 5de1309:      	pushq	%r15
 5de130b:      	pushq	%r14
 5de130d:      	pushq	%r13
 5de130f:      	pushq	%r12
 5de1311:      	pushq	%rbx
 5de1312:      	subq	$0x18, %rsp
 5de1316:      	movl	%esi, %ebp
 5de1318:      	movq	%rdi, %rbx
 5de131b:      	movl	%esi, %eax
 5de131d:      	leaq	(%rax,%rax,2), %rcx
 5de1321:      	leaq	(%rdi,%rcx,8), %r14
 5de1325:      	bsrq	%rax, %rdx
 5de1329:      	xorl	$0x3f, %edx
 5de132c:      	addl	%edx, %edx
 5de132e:      	xorq	$0x7e, %rdx
 5de1332:      	movq	%r14, %rsi
 5de1335:      	callq	0x5df40d0 <_ZSt16__introsort_loopIPZN4llvm19SelectionDAGBuilder18visitIntrinsicCallERKNS0_8CallInstEjE18BranchFunnelTargetlN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_18visitIntrinsicCallES4_jE3$_1EEEvT_SC_T0_T1_>
 5de133a:      	leaq	0x18(%rbx), %r15
 5de133e:      	cmpl	$0x11, %ebp
 5de1341:      	jb	0x5de141f <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x11f>
 5de1347:      	leaq	0x18(%rbx), %r13
 5de134b:      	movl	$0x18, %r12d
 5de1351:      	movq	%rbx, %rax
 5de1354:      	jmp	0x5de1383 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x83>
 5de1356:      	nopw	%cs:(%rax,%rax)
 5de1360:      	movq	%rcx, (%rdx)
 5de1363:      	movaps	(%rsp), %xmm0
 5de1367:      	movups	%xmm0, 0x8(%rdx)
 5de136b:      	addq	$0x18, %r12
 5de136f:      	addq	$0x18, %r13
 5de1373:      	movq	%rbp, %rax
 5de1376:      	cmpq	$0x180, %r12            # imm = 0x180
 5de137d:      	je	0x5de1433 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x133>
 5de1383:      	leaq	(%rbx,%r12), %rbp
 5de1387:      	movq	(%rbx,%r12), %rcx
 5de138b:      	cmpq	(%rbx), %rcx
 5de138e:      	jge	0x5de13d0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xd0>
 5de1390:      	movq	0x10(%rbp), %rcx
 5de1394:      	movq	%rcx, 0x10(%rsp)
 5de1399:      	movups	(%rbp), %xmm0
 5de139d:      	movaps	%xmm0, (%rsp)
 5de13a1:      	cmpq	$0x19, %r12
 5de13a5:      	jb	0x5de140e <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x10e>
 5de13a7:      	movq	%r15, %rdi
 5de13aa:      	movq	%rbx, %rsi
 5de13ad:      	movq	%r12, %rdx
 5de13b0:      	callq	0x828abc0 <memmove@plt>
 5de13b5:      	movq	0x10(%rsp), %rax
 5de13ba:      	movq	%rax, 0x10(%rbx)
 5de13be:      	movaps	(%rsp), %xmm0
 5de13c2:      	movups	%xmm0, (%rbx)
 5de13c5:      	jmp	0x5de136b <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x6b>
 5de13c7:      	nopw	(%rax,%rax)
 5de13d0:      	movups	0x20(%rax), %xmm0
 5de13d4:      	movaps	%xmm0, (%rsp)
 5de13d8:      	movq	%rbp, %rdx
 5de13db:      	cmpq	(%rax), %rcx
 5de13de:      	jge	0x5de1360 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x60>
 5de13e0:      	movq	%r13, %rdx
 5de13e3:      	nopw	%cs:(%rax,%rax)
 5de13ed:      	nopl	(%rax)
 5de13f0:      	movq	-0x8(%rdx), %rax
 5de13f4:      	movq	%rax, 0x10(%rdx)
 5de13f8:      	movups	-0x18(%rdx), %xmm0
 5de13fc:      	movups	%xmm0, (%rdx)
 5de13ff:      	cmpq	-0x30(%rdx), %rcx
 5de1403:      	leaq	-0x18(%rdx), %rdx
 5de1407:      	jl	0x5de13f0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xf0>
 5de1409:      	jmp	0x5de1360 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x60>
 5de140e:      	movq	0x10(%rbx), %rcx
 5de1412:      	movq	%rcx, 0x28(%rax)
 5de1416:      	movups	(%rbx), %xmm0
 5de1419:      	movups	%xmm0, 0x18(%rax)
 5de141d:      	jmp	0x5de13b5 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0xb5>
 5de141f:      	cmpl	$0x1, %ebp
 5de1422:      	jne	0x5de148b <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x18b>
 5de1424:      	addq	$0x18, %rsp
 5de1428:      	popq	%rbx
 5de1429:      	popq	%r12
 5de142b:      	popq	%r13
 5de142d:      	popq	%r14
 5de142f:      	popq	%r15
 5de1431:      	popq	%rbp
 5de1432:      	retq
 5de1433:      	addq	$0x180, %rbx            # imm = 0x180
 5de143a:      	jmp	0x5de1454 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x154>
 5de143c:      	nopl	(%rax)
 5de1440:      	movq	%rax, (%rcx)
 5de1443:      	movaps	(%rsp), %xmm0
 5de1447:      	movups	%xmm0, 0x8(%rcx)
 5de144b:      	addq	$0x18, %rbx
 5de144f:      	cmpq	%r14, %rbx
 5de1452:      	je	0x5de1424 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de1454:      	movq	(%rbx), %rax
 5de1457:      	movups	0x8(%rbx), %xmm0
 5de145b:      	movaps	%xmm0, (%rsp)
 5de145f:      	movq	%rbx, %rcx
 5de1462:      	cmpq	-0x18(%rbx), %rax
 5de1466:      	jge	0x5de1440 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x140>
 5de1468:      	movq	%rbx, %rcx
 5de146b:      	nopl	(%rax,%rax)
 5de1470:      	movq	-0x8(%rcx), %rdx
 5de1474:      	movq	%rdx, 0x10(%rcx)
 5de1478:      	movups	-0x18(%rcx), %xmm0
 5de147c:      	movups	%xmm0, (%rcx)
 5de147f:      	cmpq	-0x30(%rcx), %rax
 5de1483:      	leaq	-0x18(%rcx), %rcx
 5de1487:      	jl	0x5de1470 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x170>
 5de1489:      	jmp	0x5de1440 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x140>
 5de148b:      	movabsq	$-0x5555555555555555, %r12 # imm = 0xAAAAAAAAAAAAAAAB
 5de1495:      	movq	%rbx, %rax
 5de1498:      	jmp	0x5de14bb <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1bb>
 5de149a:      	nopw	(%rax,%rax)
 5de14a0:      	movq	%rcx, (%rdx)
 5de14a3:      	movaps	(%rsp), %xmm0
 5de14a7:      	movups	%xmm0, 0x8(%rdx)
 5de14ab:      	leaq	0x18(%r13), %r15
 5de14af:      	movq	%r13, %rax
 5de14b2:      	cmpq	%r14, %r15
 5de14b5:      	je	0x5de1424 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de14bb:      	movq	%r15, %r13
 5de14be:      	movq	(%r15), %rcx
 5de14c1:      	cmpq	(%rbx), %rcx
 5de14c4:      	jge	0x5de1530 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x230>
 5de14c6:      	movq	0x10(%r13), %rcx
 5de14ca:      	movq	%rcx, 0x10(%rsp)
 5de14cf:      	movups	(%r13), %xmm0
 5de14d4:      	movaps	%xmm0, (%rsp)
 5de14d8:      	movq	%r13, %rdx
 5de14db:      	subq	%rbx, %rdx
 5de14de:      	cmpq	$0x19, %rdx
 5de14e2:      	jl	0x5de156e <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x26e>
 5de14e8:      	movq	%rdx, %rcx
 5de14eb:      	shrq	$0x3, %rcx
 5de14ef:      	imulq	%r12, %rcx
 5de14f3:      	negq	%rcx
 5de14f6:      	leaq	(%rcx,%rcx,2), %rcx
 5de14fa:      	leaq	0x30(%rax,%rcx,8), %rdi
 5de14ff:      	movq	%rbx, %rsi
 5de1502:      	callq	0x828abc0 <memmove@plt>
 5de1507:      	movq	0x10(%rsp), %rax
 5de150c:      	movq	%rax, 0x10(%rbx)
 5de1510:      	movaps	(%rsp), %xmm0
 5de1514:      	movups	%xmm0, (%rbx)
 5de1517:      	leaq	0x18(%r13), %r15
 5de151b:      	movq	%r13, %rax
 5de151e:      	cmpq	%r14, %r15
 5de1521:      	jne	0x5de14bb <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1bb>
 5de1523:      	jmp	0x5de1424 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x124>
 5de1528:      	nopl	(%rax,%rax)
 5de1530:      	movups	0x20(%rax), %xmm0
 5de1534:      	movaps	%xmm0, (%rsp)
 5de1538:      	movq	%r13, %rdx
 5de153b:      	cmpq	(%rax), %rcx
 5de153e:      	jge	0x5de14a0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1a0>
 5de1544:      	movq	%r13, %rdx
 5de1547:      	nopw	(%rax,%rax)
 5de1550:      	movq	-0x8(%rdx), %rax
 5de1554:      	movq	%rax, 0x10(%rdx)
 5de1558:      	movups	-0x18(%rdx), %xmm0
 5de155c:      	movups	%xmm0, (%rdx)
 5de155f:      	cmpq	-0x30(%rdx), %rcx
 5de1563:      	leaq	-0x18(%rdx), %rdx
 5de1567:      	jl	0x5de1550 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x250>
 5de1569:      	jmp	0x5de14a0 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x1a0>
 5de156e:      	cmpq	$0x18, %rdx
 5de1572:      	jne	0x5de1507 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x207>
 5de1574:      	movq	0x10(%rbx), %rcx
 5de1578:      	movq	%rcx, 0x28(%rax)
 5de157c:      	movups	(%rbx), %xmm0
 5de157f:      	movups	%xmm0, 0x18(%rax)
 5de1583:      	jmp	0x5de1507 <_ZN4llvm4sortIRNS_11SmallVectorIZNS_19SelectionDAGBuilder18visitIntrinsicCallERKNS_8CallInstEjE18BranchFunnelTargetLj8EEEZNS2_18visitIntrinsicCallES5_jE3$_1EEvOT_T0_+0x207>
