
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003ec1310 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv>:
 3ec1310:      	pushq	%rbp
 3ec1311:      	pushq	%r15
 3ec1313:      	pushq	%r14
 3ec1315:      	pushq	%r13
 3ec1317:      	pushq	%r12
 3ec1319:      	pushq	%rbx
 3ec131a:      	subq	$0x28, %rsp
 3ec131e:      	movq	0x38(%rdi), %rbp
 3ec1322:      	movq	%rdi, 0x20(%rsp)
 3ec1327:      	movq	0x40(%rdi), %rdx
 3ec132b:      	cmpq	%rdx, %rbp
 3ec132e:      	je	0x3ec17d5 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4c5>
 3ec1334:      	xorl	%r8d, %r8d
 3ec1337:      	movabsq	$0xfffffffffffffff, %rsi # imm = 0xFFFFFFFFFFFFFFF
 3ec1341:      	xorl	%r13d, %r13d
 3ec1344:      	xorl	%eax, %eax
 3ec1346:      	movq	%rdx, 0x8(%rsp)
 3ec134b:      	jmp	0x3ec1368 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x58>
 3ec134d:      	nopl	(%rax)
 3ec1350:      	movq	%r14, (%r13)
 3ec1354:      	movq	%r13, %r15
 3ec1357:      	leaq	0x8(%r15), %r13
 3ec135b:      	addq	$0x8, %rbp
 3ec135f:      	cmpq	%rdx, %rbp
 3ec1362:      	je	0x3ec1415 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x105>
 3ec1368:      	movq	(%rbp), %r14
 3ec136c:      	cmpq	%rax, %r13
 3ec136f:      	jne	0x3ec1350 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x40>
 3ec1371:      	movq	%r13, %r15
 3ec1374:      	subq	%r8, %r15
 3ec1377:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 3ec1381:      	cmpq	%rax, %r15
 3ec1384:      	je	0x3ec17e4 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4d4>
 3ec138a:      	movq	%r15, %rax
 3ec138d:      	sarq	$0x3, %rax
 3ec1391:      	movl	$0x1, %ecx
 3ec1396:      	cmpq	%r8, %r13
 3ec1399:      	je	0x3ec139e <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x8e>
 3ec139b:      	movq	%rax, %rcx
 3ec139e:      	movq	%r8, %rbx
 3ec13a1:      	leaq	(%rcx,%rax), %r13
 3ec13a5:      	cmpq	%rsi, %r13
 3ec13a8:      	jb	0x3ec13ad <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x9d>
 3ec13aa:      	movq	%rsi, %r13
 3ec13ad:      	addq	%rax, %rcx
 3ec13b0:      	cmovbq	%rsi, %r13
 3ec13b4:      	leaq	(,%r13,8), %rdi
 3ec13bc:      	callq	0x828a6b0 <_Znwm@plt>
 3ec13c1:      	movq	%rax, %r12
 3ec13c4:      	movq	%r14, (%rax,%r15)
 3ec13c8:      	testq	%r15, %r15
 3ec13cb:      	jle	0x3ec13db <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0xcb>
 3ec13cd:      	movq	%r12, %rdi
 3ec13d0:      	movq	%rbx, %rsi
 3ec13d3:      	movq	%r15, %rdx
 3ec13d6:      	callq	0x828ace0 <memcpy@plt>
 3ec13db:      	testq	%rbx, %rbx
 3ec13de:      	je	0x3ec13eb <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0xdb>
 3ec13e0:      	movq	%rbx, %rdi
 3ec13e3:      	movq	%r15, %rsi
 3ec13e6:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3ec13eb:      	addq	%r12, %r15
 3ec13ee:      	leaq	(%r12,%r13,8), %rax
 3ec13f2:      	movq	%r12, %r8
 3ec13f5:      	movq	0x8(%rsp), %rdx
 3ec13fa:      	movabsq	$0xfffffffffffffff, %rsi # imm = 0xFFFFFFFFFFFFFFF
 3ec1404:      	leaq	0x8(%r15), %r13
 3ec1408:      	addq	$0x8, %rbp
 3ec140c:      	cmpq	%rdx, %rbp
 3ec140f:      	jne	0x3ec1368 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x58>
 3ec1415:      	cmpq	%r13, %r8
 3ec1418:      	je	0x3ec17c2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4b2>
 3ec141e:      	movq	%rax, 0x10(%rsp)
 3ec1423:      	movq	%r13, %r14
 3ec1426:      	subq	%r8, %r14
 3ec1429:      	movq	%r14, %rax
 3ec142c:      	sarq	$0x3, %rax
 3ec1430:      	bsrq	%rax, %rdx
 3ec1434:      	xorl	$0x3f, %edx
 3ec1437:      	addl	%edx, %edx
 3ec1439:      	xorq	$0x7e, %rdx
 3ec143d:      	movq	%r8, %rdi
 3ec1440:      	movq	%r13, %rsi
 3ec1443:      	movq	%r8, 0x8(%rsp)
 3ec1448:      	callq	0x3ec58f0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPN12_GLOBAL__N_111COFFSectionESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZN4llvm13WinCOFFWriter19writeSectionHeadersEvE3$_0EEEvT_SG_T0_T1_>
 3ec144d:      	movq	0x8(%rsp), %r8
 3ec1452:      	leaq	0x8(%r8), %rbx
 3ec1456:      	cmpq	$0x81, %r14
 3ec145d:      	jl	0x3ec1470 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x160>
 3ec145f:      	movl	$0x8, %r12d
 3ec1465:      	movq	%rbx, %r14
 3ec1468:      	movq	%r8, %rdi
 3ec146b:      	jmp	0x3ec1537 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x227>
 3ec1470:      	cmpq	%r15, %r8
 3ec1473:      	je	0x3ec15b2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec1479:      	movq	%r8, %r14
 3ec147c:      	jmp	0x3ec14be <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1ae>
 3ec147e:      	nop
 3ec1480:      	movq	%r14, %rdx
 3ec1483:      	subq	%r8, %rdx
 3ec1486:      	movq	%rdx, %rax
 3ec1489:      	sarq	$0x3, %rax
 3ec148d:      	cmpq	$0x2, %rax
 3ec1491:      	jl	0x3ec1502 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1f2>
 3ec1493:      	shlq	$0x3, %rax
 3ec1497:      	subq	%rax, %rdi
 3ec149a:      	addq	$0x10, %rdi
 3ec149e:      	movq	%r8, %rsi
 3ec14a1:      	callq	0x828ac50 <memmove@plt>
 3ec14a6:      	movq	0x8(%rsp), %r8
 3ec14ab:      	movq	%r8, %rax
 3ec14ae:      	movq	%r12, (%rax)
 3ec14b1:      	leaq	0x8(%r14), %rbx
 3ec14b5:      	cmpq	%r15, %r14
 3ec14b8:      	je	0x3ec15b2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec14be:      	movq	%r14, %rdi
 3ec14c1:      	movq	%rbx, %r14
 3ec14c4:      	movq	(%rbx), %r12
 3ec14c7:      	movq	(%r8), %rsi
 3ec14ca:      	movl	0x48(%r12), %ecx
 3ec14cf:      	cmpl	0x48(%rsi), %ecx
 3ec14d2:      	jl	0x3ec1480 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x170>
 3ec14d4:      	movq	(%rdi), %rdx
 3ec14d7:      	movq	%r14, %rax
 3ec14da:      	cmpl	0x48(%rdx), %ecx
 3ec14dd:      	jge	0x3ec14ae <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec14df:      	movq	%r14, %rax
 3ec14e2:      	nopw	%cs:(%rax,%rax)
 3ec14ec:      	nopl	(%rax)
 3ec14f0:      	movq	%rdx, (%rax)
 3ec14f3:      	movq	-0x10(%rax), %rdx
 3ec14f7:      	addq	$-0x8, %rax
 3ec14fb:      	cmpl	0x48(%rdx), %ecx
 3ec14fe:      	jl	0x3ec14f0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x1e0>
 3ec1500:      	jmp	0x3ec14ae <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec1502:      	movq	%r8, %rax
 3ec1505:      	cmpq	$0x8, %rdx
 3ec1509:      	jne	0x3ec14ae <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19e>
 3ec150b:      	movq	%rsi, 0x8(%rdi)
 3ec150f:      	jmp	0x3ec14ab <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x19b>
 3ec1511:      	movq	%rdx, 0x8(%rcx)
 3ec1515:      	nopw	%cs:(%rax,%rax)
 3ec151f:      	nop
 3ec1520:      	movq	%r8, %rcx
 3ec1523:      	movq	%rbp, (%rcx)
 3ec1526:      	addq	$0x8, %r12
 3ec152a:      	addq	$0x8, %r14
 3ec152e:      	cmpq	$0x80, %r12
 3ec1535:      	je	0x3ec15a2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x292>
 3ec1537:      	movq	%rdi, %rcx
 3ec153a:      	leaq	(%r8,%r12), %rdi
 3ec153e:      	movq	(%r8,%r12), %rbp
 3ec1542:      	movq	(%r8), %rdx
 3ec1545:      	movl	0x48(%rbp), %eax
 3ec1548:      	cmpl	0x48(%rdx), %eax
 3ec154b:      	jge	0x3ec1580 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x270>
 3ec154d:      	cmpq	$0x9, %r12
 3ec1551:      	jb	0x3ec1511 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x201>
 3ec1553:      	movq	%rdi, 0x18(%rsp)
 3ec1558:      	movq	%rbx, %rdi
 3ec155b:      	movq	%r8, %rsi
 3ec155e:      	movq	%r12, %rdx
 3ec1561:      	callq	0x828ac50 <memmove@plt>
 3ec1566:      	movq	0x18(%rsp), %rdi
 3ec156b:      	movq	0x8(%rsp), %r8
 3ec1570:      	jmp	0x3ec1520 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x210>
 3ec1572:      	nopw	%cs:(%rax,%rax)
 3ec157c:      	nopl	(%rax)
 3ec1580:      	movq	(%rcx), %rdx
 3ec1583:      	movq	%rdi, %rcx
 3ec1586:      	cmpl	0x48(%rdx), %eax
 3ec1589:      	jge	0x3ec1523 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x213>
 3ec158b:      	movq	%r14, %rcx
 3ec158e:      	nop
 3ec1590:      	movq	%rdx, (%rcx)
 3ec1593:      	movq	-0x10(%rcx), %rdx
 3ec1597:      	addq	$-0x8, %rcx
 3ec159b:      	cmpl	0x48(%rdx), %eax
 3ec159e:      	jl	0x3ec1590 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x280>
 3ec15a0:      	jmp	0x3ec1523 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x213>
 3ec15a2:      	leaq	0x80(%r8), %rax
 3ec15a9:      	cmpq	%r13, %rax
 3ec15ac:      	jne	0x3ec1790 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x480>
 3ec15b2:      	leaq	-0x8(%r8), %r12
 3ec15b6:      	leaq	0x4(%rsp), %r13
 3ec15bb:      	movq	0x10(%rsp), %rax
 3ec15c0:      	movq	0x20(%rsp), %rbx
 3ec15c5:      	jmp	0x3ec1738 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x428>
 3ec15ca:      	nopw	(%rax,%rax)
 3ec15d0:      	movq	0x8(%rbx), %rdi
 3ec15d4:      	movl	$0x8, %edx
 3ec15d9:      	movq	%rbp, %rsi
 3ec15dc:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec15e1:      	movl	0x8(%rbp), %eax
 3ec15e4:      	movq	0x8(%rbx), %rdi
 3ec15e8:      	cmpl	$0x1, 0x10(%rbx)
 3ec15ec:      	movl	%eax, %ecx
 3ec15ee:      	bswapl	%ecx
 3ec15f0:      	cmovel	%eax, %ecx
 3ec15f3:      	movl	%ecx, 0x4(%rsp)
 3ec15f7:      	movl	$0x4, %edx
 3ec15fc:      	movq	%r13, %rsi
 3ec15ff:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1604:      	movl	0xc(%rbp), %eax
 3ec1607:      	movq	0x8(%rbx), %rdi
 3ec160b:      	cmpl	$0x1, 0x10(%rbx)
 3ec160f:      	movl	%eax, %ecx
 3ec1611:      	bswapl	%ecx
 3ec1613:      	cmovel	%eax, %ecx
 3ec1616:      	movl	%ecx, 0x4(%rsp)
 3ec161a:      	movl	$0x4, %edx
 3ec161f:      	movq	%r13, %rsi
 3ec1622:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1627:      	movl	0x10(%rbp), %eax
 3ec162a:      	movq	0x8(%rbx), %rdi
 3ec162e:      	cmpl	$0x1, 0x10(%rbx)
 3ec1632:      	movl	%eax, %ecx
 3ec1634:      	bswapl	%ecx
 3ec1636:      	cmovel	%eax, %ecx
 3ec1639:      	movl	%ecx, 0x4(%rsp)
 3ec163d:      	movl	$0x4, %edx
 3ec1642:      	movq	%r13, %rsi
 3ec1645:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec164a:      	movl	0x14(%rbp), %eax
 3ec164d:      	movq	0x8(%rbx), %rdi
 3ec1651:      	cmpl	$0x1, 0x10(%rbx)
 3ec1655:      	movl	%eax, %ecx
 3ec1657:      	bswapl	%ecx
 3ec1659:      	cmovel	%eax, %ecx
 3ec165c:      	movl	%ecx, 0x4(%rsp)
 3ec1660:      	movl	$0x4, %edx
 3ec1665:      	movq	%r13, %rsi
 3ec1668:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec166d:      	movl	0x18(%rbp), %eax
 3ec1670:      	movq	0x8(%rbx), %rdi
 3ec1674:      	cmpl	$0x1, 0x10(%rbx)
 3ec1678:      	movl	%eax, %ecx
 3ec167a:      	bswapl	%ecx
 3ec167c:      	cmovel	%eax, %ecx
 3ec167f:      	movl	%ecx, 0x4(%rsp)
 3ec1683:      	movl	$0x4, %edx
 3ec1688:      	movq	%r13, %rsi
 3ec168b:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1690:      	movl	0x1c(%rbp), %eax
 3ec1693:      	movq	0x8(%rbx), %rdi
 3ec1697:      	cmpl	$0x1, 0x10(%rbx)
 3ec169b:      	movl	%eax, %ecx
 3ec169d:      	bswapl	%ecx
 3ec169f:      	cmovel	%eax, %ecx
 3ec16a2:      	movl	%ecx, 0x4(%rsp)
 3ec16a6:      	movl	$0x4, %edx
 3ec16ab:      	movq	%r13, %rsi
 3ec16ae:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec16b3:      	movl	0x20(%rbp), %eax
 3ec16b6:      	movl	%eax, %ecx
 3ec16b8:      	rolw	$0x8, %cx
 3ec16bc:      	cmpl	$0x1, 0x10(%rbx)
 3ec16c0:      	movq	0x8(%rbx), %rdi
 3ec16c4:      	cmovel	%eax, %ecx
 3ec16c7:      	movw	%cx, 0x4(%rsp)
 3ec16cc:      	movl	$0x2, %edx
 3ec16d1:      	movq	%r13, %rsi
 3ec16d4:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec16d9:      	movzwl	0x22(%rbp), %eax
 3ec16dd:      	movl	%eax, %ecx
 3ec16df:      	rolw	$0x8, %cx
 3ec16e3:      	cmpl	$0x1, 0x10(%rbx)
 3ec16e7:      	movq	0x8(%rbx), %rdi
 3ec16eb:      	cmovel	%eax, %ecx
 3ec16ee:      	movw	%cx, 0x4(%rsp)
 3ec16f3:      	movl	$0x2, %edx
 3ec16f8:      	movq	%r13, %rsi
 3ec16fb:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1700:      	movl	0x24(%rbp), %eax
 3ec1703:      	movq	0x8(%rbx), %rdi
 3ec1707:      	cmpl	$0x1, 0x10(%rbx)
 3ec170b:      	movl	%eax, %ecx
 3ec170d:      	bswapl	%ecx
 3ec170f:      	cmovel	%eax, %ecx
 3ec1712:      	movl	%ecx, 0x4(%rsp)
 3ec1716:      	movl	$0x4, %edx
 3ec171b:      	movq	%r13, %rsi
 3ec171e:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 3ec1723:      	movq	0x8(%rsp), %r8
 3ec1728:      	movq	%r14, %rax
 3ec172b:      	addq	$0x8, %r12
 3ec172f:      	cmpq	%r15, %r12
 3ec1732:      	je	0x3ec17c2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4b2>
 3ec1738:      	movq	0x8(%r12), %rbp
 3ec173d:      	cmpl	$-0x1, 0x48(%rbp)
 3ec1741:      	je	0x3ec172b <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x41b>
 3ec1743:      	movq	%rax, %r14
 3ec1746:      	movq	0x68(%rbp), %rax
 3ec174a:      	subq	0x60(%rbp), %rax
 3ec174e:      	sarq	$0x3, %rax
 3ec1752:      	movabsq	$-0x5555555555555555, %rcx # imm = 0xAAAAAAAAAAAAAAAB
 3ec175c:      	imulq	%rcx, %rax
 3ec1760:      	cmpq	$0xffff, %rax           # imm = 0xFFFF
 3ec1766:      	jb	0x3ec15d0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2c0>
 3ec176c:      	orb	$0x1, 0x27(%rbp)
 3ec1770:      	jmp	0x3ec15d0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2c0>
 3ec1775:      	nopw	%cs:(%rax,%rax)
 3ec177f:      	nop
 3ec1780:      	movq	%rcx, (%rdi)
 3ec1783:      	cmpq	%r15, %rax
 3ec1786:      	leaq	0x8(%rax), %rax
 3ec178a:      	je	0x3ec15b2 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x2a2>
 3ec1790:      	movq	-0x8(%rax), %rdx
 3ec1794:      	movq	(%rax), %rcx
 3ec1797:      	movl	0x48(%rcx), %esi
 3ec179a:      	movq	%rax, %rdi
 3ec179d:      	cmpl	0x48(%rdx), %esi
 3ec17a0:      	jge	0x3ec1780 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x470>
 3ec17a2:      	movq	%rax, %rdi
 3ec17a5:      	nopw	%cs:(%rax,%rax)
 3ec17af:      	nop
 3ec17b0:      	movq	%rdx, (%rdi)
 3ec17b3:      	movq	-0x10(%rdi), %rdx
 3ec17b7:      	addq	$-0x8, %rdi
 3ec17bb:      	cmpl	0x48(%rdx), %esi
 3ec17be:      	jl	0x3ec17b0 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4a0>
 3ec17c0:      	jmp	0x3ec1780 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x470>
 3ec17c2:      	testq	%r8, %r8
 3ec17c5:      	je	0x3ec17d5 <_ZN4llvm13WinCOFFWriter19writeSectionHeadersEv+0x4c5>
 3ec17c7:      	subq	%r8, %rax
 3ec17ca:      	movq	%r8, %rdi
 3ec17cd:      	movq	%rax, %rsi
 3ec17d0:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3ec17d5:      	addq	$0x28, %rsp
 3ec17d9:      	popq	%rbx
 3ec17da:      	popq	%r12
 3ec17dc:      	popq	%r13
 3ec17de:      	popq	%r14
 3ec17e0:      	popq	%r15
 3ec17e2:      	popq	%rbp
 3ec17e3:      	retq
 3ec17e4:      	leaq	-0x3226e01(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 3ec17eb:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
