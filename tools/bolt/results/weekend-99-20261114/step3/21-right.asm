
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003ec1290 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv>:
 3ec1290:      	pushq	%rbp
 3ec1291:      	pushq	%r15
 3ec1293:      	pushq	%r14
 3ec1295:      	pushq	%r13
 3ec1297:      	pushq	%r12
 3ec1299:      	pushq	%rbx
 3ec129a:      	subq	$0x28, %rsp
 3ec129e:      	movq	0x38(%rdi), %rbp
 3ec12a2:      	movq	%rdi, 0x20(%rsp)
 3ec12a7:      	movq	0x40(%rdi), %rdx
 3ec12ab:      	cmpq	%rdx, %rbp
 3ec12ae:      	je	0x3ec1755 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4c5>
 3ec12b4:      	xorl	%r8d, %r8d
 3ec12b7:      	movabsq	$0xfffffffffffffff, %rsi # imm = 0xFFFFFFFFFFFFFFF
 3ec12c1:      	xorl	%r13d, %r13d
 3ec12c4:      	xorl	%eax, %eax
 3ec12c6:      	movq	%rdx, 0x8(%rsp)
 3ec12cb:      	jmp	0x3ec12e8 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x58>
 3ec12cd:      	nopl	(%rax)
 3ec12d0:      	movq	%r14, (%r13)
 3ec12d4:      	movq	%r13, %r15
 3ec12d7:      	leaq	0x8(%r15), %r13
 3ec12db:      	addq	$0x8, %rbp
 3ec12df:      	cmpq	%rdx, %rbp
 3ec12e2:      	je	0x3ec1395 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x105>
 3ec12e8:      	movq	(%rbp), %r14
 3ec12ec:      	cmpq	%rax, %r13
 3ec12ef:      	jne	0x3ec12d0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x40>
 3ec12f1:      	movq	%r13, %r15
 3ec12f4:      	subq	%r8, %r15
 3ec12f7:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 3ec1301:      	cmpq	%rax, %r15
 3ec1304:      	je	0x3ec1764 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4d4>
 3ec130a:      	movq	%r15, %rax
 3ec130d:      	sarq	$0x3, %rax
 3ec1311:      	movl	$0x1, %ecx
 3ec1316:      	cmpq	%r8, %r13
 3ec1319:      	je	0x3ec131e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x8e>
 3ec131b:      	movq	%rax, %rcx
 3ec131e:      	movq	%r8, %rbx
 3ec1321:      	leaq	(%rcx,%rax), %r13
 3ec1325:      	cmpq	%rsi, %r13
 3ec1328:      	jb	0x3ec132d <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x9d>
 3ec132a:      	movq	%rsi, %r13
 3ec132d:      	addq	%rax, %rcx
 3ec1330:      	cmovbq	%rsi, %r13
 3ec1334:      	leaq	(,%r13,8), %rdi
 3ec133c:      	callq	0x828a620 <_Znwm@plt>
 3ec1341:      	movq	%rax, %r12
 3ec1344:      	movq	%r14, (%rax,%r15)
 3ec1348:      	testq	%r15, %r15
 3ec134b:      	jle	0x3ec135b <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0xcb>
 3ec134d:      	movq	%r12, %rdi
 3ec1350:      	movq	%rbx, %rsi
 3ec1353:      	movq	%r15, %rdx
 3ec1356:      	callq	0x828ac50 <memcpy@plt>
 3ec135b:      	testq	%rbx, %rbx
 3ec135e:      	je	0x3ec136b <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0xdb>
 3ec1360:      	movq	%rbx, %rdi
 3ec1363:      	movq	%r15, %rsi
 3ec1366:      	callq	0x828a660 <_ZdlPvm@plt>
 3ec136b:      	addq	%r12, %r15
 3ec136e:      	leaq	(%r12,%r13,8), %rax
 3ec1372:      	movq	%r12, %r8
 3ec1375:      	movq	0x8(%rsp), %rdx
 3ec137a:      	movabsq	$0xfffffffffffffff, %rsi # imm = 0xFFFFFFFFFFFFFFF
 3ec1384:      	leaq	0x8(%r15), %r13
 3ec1388:      	addq	$0x8, %rbp
 3ec138c:      	cmpq	%rdx, %rbp
 3ec138f:      	jne	0x3ec12e8 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x58>
 3ec1395:      	cmpq	%r13, %r8
 3ec1398:      	je	0x3ec1742 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4b2>
 3ec139e:      	movq	%rax, 0x10(%rsp)
 3ec13a3:      	movq	%r13, %r14
 3ec13a6:      	subq	%r8, %r14
 3ec13a9:      	movq	%r14, %rax
 3ec13ac:      	sarq	$0x3, %rax
 3ec13b0:      	bsrq	%rax, %rdx
 3ec13b4:      	xorl	$0x3f, %edx
 3ec13b7:      	addl	%edx, %edx
 3ec13b9:      	xorq	$0x7e, %rdx
 3ec13bd:      	movq	%r8, %rdi
 3ec13c0:      	movq	%r13, %rsi
 3ec13c3:      	movq	%r8, 0x8(%rsp)
 3ec13c8:      	callq	0x3ec5870 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPN12_GLOBAL__N_111COFFSectionESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZN4llvm13WinCOFFWriter19writeSectionHeadersEvE3$_0EEEvT_SG_T0_T1_>
 3ec13cd:      	movq	0x8(%rsp), %r8
 3ec13d2:      	leaq	0x8(%r8), %rbx
 3ec13d6:      	cmpq	$0x81, %r14
 3ec13dd:      	jl	0x3ec13f1 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x161>
 3ec13df:      	leaq	0x8(%r8), %r14
 3ec13e3:      	movl	$0x8, %r12d
 3ec13e9:      	movq	%r8, %rdi
 3ec13ec:      	jmp	0x3ec14b7 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x227>
 3ec13f1:      	cmpq	%r15, %r8
 3ec13f4:      	je	0x3ec1532 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec13fa:      	movq	%r8, %r14
 3ec13fd:      	jmp	0x3ec143e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1ae>
 3ec13ff:      	nop
 3ec1400:      	movq	%r14, %rdx
 3ec1403:      	subq	%r8, %rdx
 3ec1406:      	movq	%rdx, %rax
 3ec1409:      	sarq	$0x3, %rax
 3ec140d:      	cmpq	$0x2, %rax
 3ec1411:      	jl	0x3ec1482 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1f2>
 3ec1413:      	shlq	$0x3, %rax
 3ec1417:      	subq	%rax, %rdi
 3ec141a:      	addq	$0x10, %rdi
 3ec141e:      	movq	%r8, %rsi
 3ec1421:      	callq	0x828abc0 <memmove@plt>
 3ec1426:      	movq	0x8(%rsp), %r8
 3ec142b:      	movq	%r8, %rax
 3ec142e:      	movq	%r12, (%rax)
 3ec1431:      	leaq	0x8(%r14), %rbx
 3ec1435:      	cmpq	%r15, %r14
 3ec1438:      	je	0x3ec1532 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec143e:      	movq	%r14, %rdi
 3ec1441:      	movq	%rbx, %r14
 3ec1444:      	movq	(%rbx), %r12
 3ec1447:      	movq	(%r8), %rsi
 3ec144a:      	movl	0x48(%r12), %ecx
 3ec144f:      	cmpl	0x48(%rsi), %ecx
 3ec1452:      	jl	0x3ec1400 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x170>
 3ec1454:      	movq	(%rdi), %rdx
 3ec1457:      	movq	%r14, %rax
 3ec145a:      	cmpl	0x48(%rdx), %ecx
 3ec145d:      	jge	0x3ec142e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec145f:      	movq	%r14, %rax
 3ec1462:      	nopw	%cs:(%rax,%rax)
 3ec146c:      	nopl	(%rax)
 3ec1470:      	movq	%rdx, (%rax)
 3ec1473:      	movq	-0x10(%rax), %rdx
 3ec1477:      	addq	$-0x8, %rax
 3ec147b:      	cmpl	0x48(%rdx), %ecx
 3ec147e:      	jl	0x3ec1470 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1e0>
 3ec1480:      	jmp	0x3ec142e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec1482:      	movq	%r8, %rax
 3ec1485:      	cmpq	$0x8, %rdx
 3ec1489:      	jne	0x3ec142e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec148b:      	movq	%rsi, 0x8(%rdi)
 3ec148f:      	jmp	0x3ec142b <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19b>
 3ec1491:      	movq	%rdx, 0x8(%rcx)
 3ec1495:      	nopw	%cs:(%rax,%rax)
 3ec149f:      	nop
 3ec14a0:      	movq	%r8, %rcx
 3ec14a3:      	movq	%rbp, (%rcx)
 3ec14a6:      	addq	$0x8, %r12
 3ec14aa:      	addq	$0x8, %r14
 3ec14ae:      	cmpq	$0x80, %r12
 3ec14b5:      	je	0x3ec1522 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x292>
 3ec14b7:      	movq	%rdi, %rcx
 3ec14ba:      	leaq	(%r8,%r12), %rdi
 3ec14be:      	movq	(%r8,%r12), %rbp
 3ec14c2:      	movq	(%r8), %rdx
 3ec14c5:      	movl	0x48(%rbp), %eax
 3ec14c8:      	cmpl	0x48(%rdx), %eax
 3ec14cb:      	jge	0x3ec1500 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x270>
 3ec14cd:      	cmpq	$0x9, %r12
 3ec14d1:      	jb	0x3ec1491 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x201>
 3ec14d3:      	movq	%rdi, 0x18(%rsp)
 3ec14d8:      	movq	%rbx, %rdi
 3ec14db:      	movq	%r8, %rsi
 3ec14de:      	movq	%r12, %rdx
 3ec14e1:      	callq	0x828abc0 <memmove@plt>
 3ec14e6:      	movq	0x18(%rsp), %rdi
 3ec14eb:      	movq	0x8(%rsp), %r8
 3ec14f0:      	jmp	0x3ec14a0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x210>
 3ec14f2:      	nopw	%cs:(%rax,%rax)
 3ec14fc:      	nopl	(%rax)
 3ec1500:      	movq	(%rcx), %rdx
 3ec1503:      	movq	%rdi, %rcx
 3ec1506:      	cmpl	0x48(%rdx), %eax
 3ec1509:      	jge	0x3ec14a3 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x213>
 3ec150b:      	movq	%r14, %rcx
 3ec150e:      	nop
 3ec1510:      	movq	%rdx, (%rcx)
 3ec1513:      	movq	-0x10(%rcx), %rdx
 3ec1517:      	addq	$-0x8, %rcx
 3ec151b:      	cmpl	0x48(%rdx), %eax
 3ec151e:      	jl	0x3ec1510 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x280>
 3ec1520:      	jmp	0x3ec14a3 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x213>
 3ec1522:      	leaq	0x80(%r8), %rax
 3ec1529:      	cmpq	%r13, %rax
 3ec152c:      	jne	0x3ec1710 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x480>
 3ec1532:      	leaq	-0x8(%r8), %r12
 3ec1536:      	leaq	0x4(%rsp), %r13
 3ec153b:      	movq	0x10(%rsp), %rax
 3ec1540:      	movq	0x20(%rsp), %rbx
 3ec1545:      	jmp	0x3ec16b8 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x428>
 3ec154a:      	nopw	(%rax,%rax)
 3ec1550:      	movq	0x8(%rbx), %rdi
 3ec1554:      	movl	$0x8, %edx
 3ec1559:      	movq	%rbp, %rsi
 3ec155c:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1561:      	movl	0x8(%rbp), %eax
 3ec1564:      	movq	0x8(%rbx), %rdi
 3ec1568:      	cmpl	$0x1, 0x10(%rbx)
 3ec156c:      	movl	%eax, %ecx
 3ec156e:      	bswapl	%ecx
 3ec1570:      	cmovel	%eax, %ecx
 3ec1573:      	movl	%ecx, 0x4(%rsp)
 3ec1577:      	movl	$0x4, %edx
 3ec157c:      	movq	%r13, %rsi
 3ec157f:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1584:      	movl	0xc(%rbp), %eax
 3ec1587:      	movq	0x8(%rbx), %rdi
 3ec158b:      	cmpl	$0x1, 0x10(%rbx)
 3ec158f:      	movl	%eax, %ecx
 3ec1591:      	bswapl	%ecx
 3ec1593:      	cmovel	%eax, %ecx
 3ec1596:      	movl	%ecx, 0x4(%rsp)
 3ec159a:      	movl	$0x4, %edx
 3ec159f:      	movq	%r13, %rsi
 3ec15a2:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec15a7:      	movl	0x10(%rbp), %eax
 3ec15aa:      	movq	0x8(%rbx), %rdi
 3ec15ae:      	cmpl	$0x1, 0x10(%rbx)
 3ec15b2:      	movl	%eax, %ecx
 3ec15b4:      	bswapl	%ecx
 3ec15b6:      	cmovel	%eax, %ecx
 3ec15b9:      	movl	%ecx, 0x4(%rsp)
 3ec15bd:      	movl	$0x4, %edx
 3ec15c2:      	movq	%r13, %rsi
 3ec15c5:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec15ca:      	movl	0x14(%rbp), %eax
 3ec15cd:      	movq	0x8(%rbx), %rdi
 3ec15d1:      	cmpl	$0x1, 0x10(%rbx)
 3ec15d5:      	movl	%eax, %ecx
 3ec15d7:      	bswapl	%ecx
 3ec15d9:      	cmovel	%eax, %ecx
 3ec15dc:      	movl	%ecx, 0x4(%rsp)
 3ec15e0:      	movl	$0x4, %edx
 3ec15e5:      	movq	%r13, %rsi
 3ec15e8:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec15ed:      	movl	0x18(%rbp), %eax
 3ec15f0:      	movq	0x8(%rbx), %rdi
 3ec15f4:      	cmpl	$0x1, 0x10(%rbx)
 3ec15f8:      	movl	%eax, %ecx
 3ec15fa:      	bswapl	%ecx
 3ec15fc:      	cmovel	%eax, %ecx
 3ec15ff:      	movl	%ecx, 0x4(%rsp)
 3ec1603:      	movl	$0x4, %edx
 3ec1608:      	movq	%r13, %rsi
 3ec160b:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1610:      	movl	0x1c(%rbp), %eax
 3ec1613:      	movq	0x8(%rbx), %rdi
 3ec1617:      	cmpl	$0x1, 0x10(%rbx)
 3ec161b:      	movl	%eax, %ecx
 3ec161d:      	bswapl	%ecx
 3ec161f:      	cmovel	%eax, %ecx
 3ec1622:      	movl	%ecx, 0x4(%rsp)
 3ec1626:      	movl	$0x4, %edx
 3ec162b:      	movq	%r13, %rsi
 3ec162e:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1633:      	movl	0x20(%rbp), %eax
 3ec1636:      	movl	%eax, %ecx
 3ec1638:      	rolw	$0x8, %cx
 3ec163c:      	cmpl	$0x1, 0x10(%rbx)
 3ec1640:      	movq	0x8(%rbx), %rdi
 3ec1644:      	cmovel	%eax, %ecx
 3ec1647:      	movw	%cx, 0x4(%rsp)
 3ec164c:      	movl	$0x2, %edx
 3ec1651:      	movq	%r13, %rsi
 3ec1654:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1659:      	movzwl	0x22(%rbp), %eax
 3ec165d:      	movl	%eax, %ecx
 3ec165f:      	rolw	$0x8, %cx
 3ec1663:      	cmpl	$0x1, 0x10(%rbx)
 3ec1667:      	movq	0x8(%rbx), %rdi
 3ec166b:      	cmovel	%eax, %ecx
 3ec166e:      	movw	%cx, 0x4(%rsp)
 3ec1673:      	movl	$0x2, %edx
 3ec1678:      	movq	%r13, %rsi
 3ec167b:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1680:      	movl	0x24(%rbp), %eax
 3ec1683:      	movq	0x8(%rbx), %rdi
 3ec1687:      	cmpl	$0x1, 0x10(%rbx)
 3ec168b:      	movl	%eax, %ecx
 3ec168d:      	bswapl	%ecx
 3ec168f:      	cmovel	%eax, %ecx
 3ec1692:      	movl	%ecx, 0x4(%rsp)
 3ec1696:      	movl	$0x4, %edx
 3ec169b:      	movq	%r13, %rsi
 3ec169e:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec16a3:      	movq	0x8(%rsp), %r8
 3ec16a8:      	movq	%r14, %rax
 3ec16ab:      	addq	$0x8, %r12
 3ec16af:      	cmpq	%r15, %r12
 3ec16b2:      	je	0x3ec1742 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4b2>
 3ec16b8:      	movq	0x8(%r12), %rbp
 3ec16bd:      	cmpl	$-0x1, 0x48(%rbp)
 3ec16c1:      	je	0x3ec16ab <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x41b>
 3ec16c3:      	movq	%rax, %r14
 3ec16c6:      	movq	0x68(%rbp), %rax
 3ec16ca:      	subq	0x60(%rbp), %rax
 3ec16ce:      	sarq	$0x3, %rax
 3ec16d2:      	movabsq	$-0x5555555555555555, %rcx # imm = 0xAAAAAAAAAAAAAAAB
 3ec16dc:      	imulq	%rcx, %rax
 3ec16e0:      	cmpq	$0xffff, %rax           # imm = 0xFFFF
 3ec16e6:      	jb	0x3ec1550 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2c0>
 3ec16ec:      	orb	$0x1, 0x27(%rbp)
 3ec16f0:      	jmp	0x3ec1550 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2c0>
 3ec16f5:      	nopw	%cs:(%rax,%rax)
 3ec16ff:      	nop
 3ec1700:      	movq	%rcx, (%rdi)
 3ec1703:      	cmpq	%r15, %rax
 3ec1706:      	leaq	0x8(%rax), %rax
 3ec170a:      	je	0x3ec1532 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec1710:      	movq	-0x8(%rax), %rdx
 3ec1714:      	movq	(%rax), %rcx
 3ec1717:      	movl	0x48(%rcx), %esi
 3ec171a:      	movq	%rax, %rdi
 3ec171d:      	cmpl	0x48(%rdx), %esi
 3ec1720:      	jge	0x3ec1700 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x470>
 3ec1722:      	movq	%rax, %rdi
 3ec1725:      	nopw	%cs:(%rax,%rax)
 3ec172f:      	nop
 3ec1730:      	movq	%rdx, (%rdi)
 3ec1733:      	movq	-0x10(%rdi), %rdx
 3ec1737:      	addq	$-0x8, %rdi
 3ec173b:      	cmpl	0x48(%rdx), %esi
 3ec173e:      	jl	0x3ec1730 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4a0>
 3ec1740:      	jmp	0x3ec1700 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x470>
 3ec1742:      	testq	%r8, %r8
 3ec1745:      	je	0x3ec1755 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4c5>
 3ec1747:      	subq	%r8, %rax
 3ec174a:      	movq	%r8, %rdi
 3ec174d:      	movq	%rax, %rsi
 3ec1750:      	callq	0x828a660 <_ZdlPvm@plt>
 3ec1755:      	addq	$0x28, %rsp
 3ec1759:      	popq	%rbx
 3ec175a:      	popq	%r12
 3ec175c:      	popq	%r13
 3ec175e:      	popq	%r14
 3ec1760:      	popq	%r15
 3ec1762:      	popq	%rbp
 3ec1763:      	retq
 3ec1764:      	leaq	-0x3226d81(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 3ec176b:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
