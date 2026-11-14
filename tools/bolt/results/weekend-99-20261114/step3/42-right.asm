
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000058883f0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 58883f0:      	movq	%rsi, %rcx
 58883f3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 58883fd:      	subq	%rdi, %rsi
 5888400:      	cmpq	$0x40, %rsi
 5888404:      	ja	0x5888414 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 5888406:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 588840c:      	movq	%rax, %rdx
 588840f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 5888414:      	pushq	%rbp
 5888415:      	pushq	%r15
 5888417:      	pushq	%r14
 5888419:      	pushq	%r13
 588841b:      	pushq	%r12
 588841d:      	pushq	%rbx
 588841e:      	movq	%rcx, -0x18(%rsp)
 5888423:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 588842d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 5888437:      	movq	%rsi, -0x10(%rsp)
 588843c:      	movq	%rsi, %r14
 588843f:      	andq	$-0x40, %r14
 5888443:      	movq	0x8(%rdi), %r13
 5888447:      	movq	0x10(%rdi), %rcx
 588844b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 5888455:      	addq	%r13, %rdx
 5888458:      	rolq	$0x1b, %rdx
 588845c:      	imulq	%r9, %rdx
 5888460:      	movq	0x30(%rdi), %rsi
 5888464:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 588846e:      	addq	%rsi, %r10
 5888471:      	rolq	$0x16, %r10
 5888475:      	imulq	%r9, %r10
 5888479:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 5888483:      	xorq	%rdx, %rbp
 5888486:      	movq	0x28(%rdi), %r12
 588848a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 5888494:      	addq	%r12, %r9
 5888497:      	addq	%r10, %r9
 588849a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 58884a4:      	addq	(%rdi), %r10
 58884a7:      	movq	0x18(%rdi), %r11
 58884ab:      	addq	%r10, %rax
 58884ae:      	addq	%r11, %rax
 58884b1:      	addq	%rbp, %rax
 58884b4:      	rolq	$0x2b, %rax
 58884b8:      	addq	%rcx, %r13
 58884bb:      	addq	%r10, %r13
 58884be:      	movq	%r13, %rdx
 58884c1:      	rolq	$0x14, %rdx
 58884c5:      	addq	%r10, %rdx
 58884c8:      	addq	%rax, %rdx
 58884cb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 58884d5:      	addq	0x20(%rdi), %rax
 58884d9:      	addq	%r11, %r13
 58884dc:      	movq	0x38(%rdi), %r10
 58884e0:      	addq	%rax, %rcx
 58884e3:      	addq	%r10, %rcx
 58884e6:      	addq	%r9, %rcx
 58884e9:      	rolq	$0x2b, %rcx
 58884ed:      	addq	%rsi, %r12
 58884f0:      	addq	%rax, %r12
 58884f3:      	movq	%r12, %rbx
 58884f6:      	rolq	$0x14, %rbx
 58884fa:      	addq	%rax, %rbx
 58884fd:      	addq	%rcx, %rbx
 5888500:      	addq	%r10, %r12
 5888503:      	movq	%r14, -0x20(%rsp)
 5888508:      	cmpq	$0x40, %r14
 588850c:      	jne	0x5888522 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 588850e:      	movq	%rbx, %rsi
 5888511:      	movq	%r12, %r11
 5888514:      	movq	%rdx, %rax
 5888517:      	movq	%r13, %r14
 588851a:      	movq	%rbp, %r15
 588851d:      	jmp	0x588860d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 5888522:      	addq	$-0x40, -0x20(%rsp)
 5888528:      	xorl	%ecx, %ecx
 588852a:      	nopw	(%rax,%rax)
 5888530:      	addq	%r9, %r8
 5888533:      	addq	%r13, %r8
 5888536:      	movq	0x48(%rdi,%rcx), %r14
 588853b:      	movq	0x50(%rdi,%rcx), %r10
 5888540:      	addq	%r14, %r8
 5888543:      	rolq	$0x1b, %r8
 5888547:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 5888551:      	imulq	%rsi, %r8
 5888555:      	addq	%rdx, %r9
 5888558:      	movq	0x70(%rdi,%rcx), %rax
 588855d:      	movq	%rax, -0x8(%rsp)
 5888562:      	addq	%rax, %r9
 5888565:      	rolq	$0x16, %r9
 5888569:      	imulq	%rsi, %r9
 588856d:      	movq	%r8, %r15
 5888570:      	xorq	%rbx, %r15
 5888573:      	movq	0x68(%rdi,%rcx), %r11
 5888578:      	addq	%r11, %r13
 588857b:      	addq	%r12, %rbp
 588857e:      	rolq	$0x1f, %rbp
 5888582:      	addq	%r13, %r9
 5888585:      	imulq	%rsi, %rdx
 5888589:      	addq	0x40(%rdi,%rcx), %rdx
 588858e:      	movq	%rbp, %r8
 5888591:      	movq	0x58(%rdi,%rcx), %r13
 5888596:      	addq	%rdx, %r12
 5888599:      	addq	%r13, %r12
 588859c:      	addq	%r15, %r12
 588859f:      	rolq	$0x2b, %r12
 58885a3:      	addq	%r10, %r14
 58885a6:      	addq	%rdx, %r14
 58885a9:      	movq	%r14, %rax
 58885ac:      	rolq	$0x14, %rax
 58885b0:      	imulq	%rsi, %r8
 58885b4:      	addq	%rdx, %rax
 58885b7:      	addq	%r12, %rax
 58885ba:      	addq	%r8, %rbx
 58885bd:      	addq	%r9, %r10
 58885c0:      	addq	0x60(%rdi,%rcx), %rbx
 58885c5:      	movq	0x78(%rdi,%rcx), %rdx
 58885ca:      	addq	%rbx, %r10
 58885cd:      	addq	%rdx, %r10
 58885d0:      	rolq	$0x2b, %r10
 58885d4:      	addq	%r13, %r14
 58885d7:      	addq	-0x8(%rsp), %r11
 58885dc:      	addq	%rbx, %r11
 58885df:      	movq	%r11, %rsi
 58885e2:      	rolq	$0x14, %rsi
 58885e6:      	addq	%rbx, %rsi
 58885e9:      	addq	%r10, %rsi
 58885ec:      	addq	%rdx, %r11
 58885ef:      	addq	$0x40, %rcx
 58885f3:      	movq	%r15, %rbp
 58885f6:      	movq	%r14, %r13
 58885f9:      	movq	%rax, %rdx
 58885fc:      	movq	%r11, %r12
 58885ff:      	movq	%rsi, %rbx
 5888602:      	cmpq	%rcx, -0x20(%rsp)
 5888607:      	jne	0x5888530 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 588860d:      	movq	-0x10(%rsp), %r12
 5888612:      	testb	$0x3f, %r12b
 5888616:      	je	0x58886e2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 588861c:      	movq	-0x18(%rsp), %rbp
 5888621:      	movq	-0x38(%rbp), %rcx
 5888625:      	movq	-0x30(%rbp), %rdx
 5888629:      	addq	%rcx, %r8
 588862c:      	addq	%r9, %r8
 588862f:      	addq	%r14, %r8
 5888632:      	rolq	$0x1b, %r8
 5888636:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 5888640:      	imulq	%r13, %r8
 5888644:      	addq	%rax, %r9
 5888647:      	movq	-0x10(%rbp), %r10
 588864b:      	addq	%r10, %r9
 588864e:      	rolq	$0x16, %r9
 5888652:      	imulq	%r13, %r9
 5888656:      	xorq	%rsi, %r8
 5888659:      	movq	-0x18(%rbp), %rdi
 588865d:      	addq	%rdi, %r14
 5888660:      	addq	%r14, %r9
 5888663:      	addq	%r11, %r15
 5888666:      	rolq	$0x1f, %r15
 588866a:      	movq	%r15, %rbx
 588866d:      	imulq	%r13, %rax
 5888671:      	addq	%r8, %r11
 5888674:      	addq	-0x40(%rbp), %rax
 5888678:      	movq	-0x28(%rbp), %r15
 588867c:      	addq	%r15, %r11
 588867f:      	addq	%rax, %r11
 5888682:      	rolq	$0x2b, %r11
 5888686:      	imulq	%r13, %rbx
 588868a:      	addq	%rdx, %rcx
 588868d:      	addq	%rax, %rcx
 5888690:      	movq	%rcx, %r14
 5888693:      	rolq	$0x14, %r14
 5888697:      	addq	%rax, %r14
 588869a:      	addq	%r11, %r14
 588869d:      	addq	%r15, %rcx
 58886a0:      	addq	%rbx, %rsi
 58886a3:      	addq	-0x20(%rbp), %rsi
 58886a7:      	addq	%r9, %rdx
 58886aa:      	movq	-0x8(%rbp), %rax
 58886ae:      	addq	%rax, %rdx
 58886b1:      	addq	%rsi, %rdx
 58886b4:      	rolq	$0x2b, %rdx
 58886b8:      	addq	%r10, %rdi
 58886bb:      	addq	%rsi, %rdi
 58886be:      	movq	%rdi, %r10
 58886c1:      	rolq	$0x14, %r10
 58886c5:      	addq	%rsi, %r10
 58886c8:      	addq	%rdx, %r10
 58886cb:      	addq	%rax, %rdi
 58886ce:      	movq	%r10, %rsi
 58886d1:      	movq	%rdi, %r11
 58886d4:      	movq	%r14, %rax
 58886d7:      	movq	%rcx, %r14
 58886da:      	movq	%r8, %r15
 58886dd:      	movq	%rbx, %r8
 58886e0:      	jmp	0x58886ec <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 58886e2:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 58886ec:      	xorq	%r11, %r14
 58886ef:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 58886f9:      	imulq	%rcx, %r14
 58886fd:      	xorq	%r14, %r11
 5888700:      	shrq	$0x2f, %r14
 5888704:      	xorq	%r11, %r14
 5888707:      	imulq	%rcx, %r14
 588870b:      	movq	%r14, %rdi
 588870e:      	shrq	$0x2f, %rdi
 5888712:      	xorq	%r14, %rdi
 5888715:      	imulq	%rcx, %rdi
 5888719:      	movq	%r9, %rdx
 588871c:      	shrq	$0x2f, %rdx
 5888720:      	xorq	%r9, %rdx
 5888723:      	imulq	%r13, %rdx
 5888727:      	addq	%r15, %rdx
 588872a:      	addq	%rdi, %rdx
 588872d:      	xorq	%rsi, %rax
 5888730:      	imulq	%rcx, %rax
 5888734:      	xorq	%rax, %rsi
 5888737:      	shrq	$0x2f, %rax
 588873b:      	xorq	%rsi, %rax
 588873e:      	imulq	%rcx, %rax
 5888742:      	movq	%rax, %rsi
 5888745:      	shrq	$0x2f, %rsi
 5888749:      	xorq	%rax, %rsi
 588874c:      	imulq	%rcx, %rsi
 5888750:      	movq	%r12, %rax
 5888753:      	shrq	$0x2f, %rax
 5888757:      	xorq	%r12, %rax
 588875a:      	imulq	%r13, %rax
 588875e:      	addq	%r8, %rax
 5888761:      	addq	%rsi, %rax
 5888764:      	xorq	%rax, %rdx
 5888767:      	imulq	%rcx, %rdx
 588876b:      	xorq	%rdx, %rax
 588876e:      	shrq	$0x2f, %rdx
 5888772:      	xorq	%rax, %rdx
 5888775:      	imulq	%rcx, %rdx
 5888779:      	movq	%rdx, %rax
 588877c:      	shrq	$0x2f, %rax
 5888780:      	xorq	%rdx, %rax
 5888783:      	imulq	%rcx, %rax
 5888787:      	popq	%rbx
 5888788:      	popq	%r12
 588878a:      	popq	%r13
 588878c:      	popq	%r14
 588878e:      	popq	%r15
 5888790:      	popq	%rbp
 5888791:      	retq
