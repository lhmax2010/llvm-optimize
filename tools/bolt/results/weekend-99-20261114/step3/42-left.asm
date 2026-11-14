
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005888480 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 5888480:      	movq	%rsi, %rcx
 5888483:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 588848d:      	subq	%rdi, %rsi
 5888490:      	cmpq	$0x40, %rsi
 5888494:      	ja	0x58884a4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 5888496:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 588849c:      	movq	%rax, %rdx
 588849f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 58884a4:      	pushq	%rbp
 58884a5:      	pushq	%r15
 58884a7:      	pushq	%r14
 58884a9:      	pushq	%r13
 58884ab:      	pushq	%r12
 58884ad:      	pushq	%rbx
 58884ae:      	movq	%rcx, -0x18(%rsp)
 58884b3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 58884bd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 58884c7:      	movq	%rsi, -0x10(%rsp)
 58884cc:      	movq	%rsi, %r14
 58884cf:      	andq	$-0x40, %r14
 58884d3:      	movq	0x8(%rdi), %r13
 58884d7:      	movq	0x10(%rdi), %rcx
 58884db:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 58884e5:      	addq	%r13, %rdx
 58884e8:      	rolq	$0x1b, %rdx
 58884ec:      	imulq	%r9, %rdx
 58884f0:      	movq	0x30(%rdi), %rsi
 58884f4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 58884fe:      	addq	%rsi, %r10
 5888501:      	rolq	$0x16, %r10
 5888505:      	imulq	%r9, %r10
 5888509:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 5888513:      	xorq	%rdx, %rbp
 5888516:      	movq	0x28(%rdi), %r12
 588851a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 5888524:      	addq	%r12, %r9
 5888527:      	addq	%r10, %r9
 588852a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 5888534:      	addq	(%rdi), %r10
 5888537:      	movq	0x18(%rdi), %r11
 588853b:      	addq	%r10, %rax
 588853e:      	addq	%r11, %rax
 5888541:      	addq	%rbp, %rax
 5888544:      	rolq	$0x2b, %rax
 5888548:      	addq	%rcx, %r13
 588854b:      	addq	%r10, %r13
 588854e:      	movq	%r13, %rdx
 5888551:      	rolq	$0x14, %rdx
 5888555:      	addq	%r10, %rdx
 5888558:      	addq	%rax, %rdx
 588855b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 5888565:      	addq	0x20(%rdi), %rax
 5888569:      	addq	%r11, %r13
 588856c:      	movq	0x38(%rdi), %r10
 5888570:      	addq	%rax, %rcx
 5888573:      	addq	%r10, %rcx
 5888576:      	addq	%r9, %rcx
 5888579:      	rolq	$0x2b, %rcx
 588857d:      	addq	%rsi, %r12
 5888580:      	addq	%rax, %r12
 5888583:      	movq	%r12, %rbx
 5888586:      	rolq	$0x14, %rbx
 588858a:      	addq	%rax, %rbx
 588858d:      	addq	%rcx, %rbx
 5888590:      	addq	%r10, %r12
 5888593:      	movq	%r14, -0x20(%rsp)
 5888598:      	cmpq	$0x40, %r14
 588859c:      	jne	0x58885b2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 588859e:      	movq	%rbx, %rsi
 58885a1:      	movq	%r12, %r11
 58885a4:      	movq	%rdx, %rax
 58885a7:      	movq	%r13, %r14
 58885aa:      	movq	%rbp, %r15
 58885ad:      	jmp	0x588869d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 58885b2:      	addq	$-0x40, -0x20(%rsp)
 58885b8:      	xorl	%ecx, %ecx
 58885ba:      	nopw	(%rax,%rax)
 58885c0:      	addq	%r9, %r8
 58885c3:      	addq	%r13, %r8
 58885c6:      	movq	0x48(%rdi,%rcx), %r14
 58885cb:      	movq	0x50(%rdi,%rcx), %r10
 58885d0:      	addq	%r14, %r8
 58885d3:      	rolq	$0x1b, %r8
 58885d7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 58885e1:      	imulq	%rsi, %r8
 58885e5:      	addq	%rdx, %r9
 58885e8:      	movq	0x70(%rdi,%rcx), %rax
 58885ed:      	movq	%rax, -0x8(%rsp)
 58885f2:      	addq	%rax, %r9
 58885f5:      	rolq	$0x16, %r9
 58885f9:      	imulq	%rsi, %r9
 58885fd:      	movq	%r8, %r15
 5888600:      	xorq	%rbx, %r15
 5888603:      	movq	0x68(%rdi,%rcx), %r11
 5888608:      	addq	%r11, %r13
 588860b:      	addq	%r12, %rbp
 588860e:      	rolq	$0x1f, %rbp
 5888612:      	addq	%r13, %r9
 5888615:      	imulq	%rsi, %rdx
 5888619:      	addq	0x40(%rdi,%rcx), %rdx
 588861e:      	movq	%rbp, %r8
 5888621:      	movq	0x58(%rdi,%rcx), %r13
 5888626:      	addq	%rdx, %r12
 5888629:      	addq	%r13, %r12
 588862c:      	addq	%r15, %r12
 588862f:      	rolq	$0x2b, %r12
 5888633:      	addq	%r10, %r14
 5888636:      	addq	%rdx, %r14
 5888639:      	movq	%r14, %rax
 588863c:      	rolq	$0x14, %rax
 5888640:      	imulq	%rsi, %r8
 5888644:      	addq	%rdx, %rax
 5888647:      	addq	%r12, %rax
 588864a:      	addq	%r8, %rbx
 588864d:      	addq	%r9, %r10
 5888650:      	addq	0x60(%rdi,%rcx), %rbx
 5888655:      	movq	0x78(%rdi,%rcx), %rdx
 588865a:      	addq	%rbx, %r10
 588865d:      	addq	%rdx, %r10
 5888660:      	rolq	$0x2b, %r10
 5888664:      	addq	%r13, %r14
 5888667:      	addq	-0x8(%rsp), %r11
 588866c:      	addq	%rbx, %r11
 588866f:      	movq	%r11, %rsi
 5888672:      	rolq	$0x14, %rsi
 5888676:      	addq	%rbx, %rsi
 5888679:      	addq	%r10, %rsi
 588867c:      	addq	%rdx, %r11
 588867f:      	addq	$0x40, %rcx
 5888683:      	movq	%r15, %rbp
 5888686:      	movq	%r14, %r13
 5888689:      	movq	%rax, %rdx
 588868c:      	movq	%r11, %r12
 588868f:      	movq	%rsi, %rbx
 5888692:      	cmpq	%rcx, -0x20(%rsp)
 5888697:      	jne	0x58885c0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 588869d:      	movq	-0x10(%rsp), %r12
 58886a2:      	testb	$0x3f, %r12b
 58886a6:      	je	0x5888773 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 58886ac:      	leaq	(%r9,%r14), %rdi
 58886b0:      	movq	-0x18(%rsp), %rbp
 58886b5:      	movq	-0x38(%rbp), %rcx
 58886b9:      	movq	-0x30(%rbp), %rdx
 58886bd:      	addq	%rcx, %r8
 58886c0:      	addq	%rdi, %r8
 58886c3:      	rolq	$0x1b, %r8
 58886c7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 58886d1:      	imulq	%r13, %r8
 58886d5:      	addq	%rax, %r9
 58886d8:      	movq	-0x10(%rbp), %r10
 58886dc:      	addq	%r10, %r9
 58886df:      	rolq	$0x16, %r9
 58886e3:      	imulq	%r13, %r9
 58886e7:      	xorq	%rsi, %r8
 58886ea:      	movq	-0x18(%rbp), %rdi
 58886ee:      	addq	%rdi, %r14
 58886f1:      	addq	%r14, %r9
 58886f4:      	addq	%r11, %r15
 58886f7:      	rolq	$0x1f, %r15
 58886fb:      	movq	%r15, %rbx
 58886fe:      	imulq	%r13, %rax
 5888702:      	addq	%r8, %r11
 5888705:      	addq	-0x40(%rbp), %rax
 5888709:      	movq	-0x28(%rbp), %r15
 588870d:      	addq	%r15, %r11
 5888710:      	addq	%rax, %r11
 5888713:      	rolq	$0x2b, %r11
 5888717:      	imulq	%r13, %rbx
 588871b:      	addq	%rdx, %rcx
 588871e:      	addq	%rax, %rcx
 5888721:      	movq	%rcx, %r14
 5888724:      	rolq	$0x14, %r14
 5888728:      	addq	%rax, %r14
 588872b:      	addq	%r11, %r14
 588872e:      	addq	%r15, %rcx
 5888731:      	addq	%rbx, %rsi
 5888734:      	addq	-0x20(%rbp), %rsi
 5888738:      	addq	%r9, %rdx
 588873b:      	movq	-0x8(%rbp), %rax
 588873f:      	addq	%rax, %rdx
 5888742:      	addq	%rsi, %rdx
 5888745:      	rolq	$0x2b, %rdx
 5888749:      	addq	%r10, %rdi
 588874c:      	addq	%rsi, %rdi
 588874f:      	movq	%rdi, %r10
 5888752:      	rolq	$0x14, %r10
 5888756:      	addq	%rsi, %r10
 5888759:      	addq	%rdx, %r10
 588875c:      	addq	%rax, %rdi
 588875f:      	movq	%r10, %rsi
 5888762:      	movq	%rdi, %r11
 5888765:      	movq	%r14, %rax
 5888768:      	movq	%rcx, %r14
 588876b:      	movq	%r8, %r15
 588876e:      	movq	%rbx, %r8
 5888771:      	jmp	0x588877d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_5ValueEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 5888773:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 588877d:      	xorq	%r11, %r14
 5888780:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 588878a:      	imulq	%rcx, %r14
 588878e:      	xorq	%r14, %r11
 5888791:      	shrq	$0x2f, %r14
 5888795:      	xorq	%r11, %r14
 5888798:      	imulq	%rcx, %r14
 588879c:      	movq	%r14, %rdi
 588879f:      	shrq	$0x2f, %rdi
 58887a3:      	xorq	%r14, %rdi
 58887a6:      	imulq	%rcx, %rdi
 58887aa:      	movq	%r9, %rdx
 58887ad:      	shrq	$0x2f, %rdx
 58887b1:      	xorq	%r9, %rdx
 58887b4:      	imulq	%r13, %rdx
 58887b8:      	addq	%r15, %rdx
 58887bb:      	addq	%rdi, %rdx
 58887be:      	xorq	%rsi, %rax
 58887c1:      	imulq	%rcx, %rax
 58887c5:      	xorq	%rax, %rsi
 58887c8:      	shrq	$0x2f, %rax
 58887cc:      	xorq	%rsi, %rax
 58887cf:      	imulq	%rcx, %rax
 58887d3:      	movq	%rax, %rsi
 58887d6:      	shrq	$0x2f, %rsi
 58887da:      	xorq	%rax, %rsi
 58887dd:      	imulq	%rcx, %rsi
 58887e1:      	movq	%r12, %rax
 58887e4:      	shrq	$0x2f, %rax
 58887e8:      	xorq	%r12, %rax
 58887eb:      	imulq	%r13, %rax
 58887ef:      	addq	%r8, %rax
 58887f2:      	addq	%rsi, %rax
 58887f5:      	xorq	%rax, %rdx
 58887f8:      	imulq	%rcx, %rdx
 58887fc:      	xorq	%rdx, %rax
 58887ff:      	shrq	$0x2f, %rdx
 5888803:      	xorq	%rax, %rdx
 5888806:      	imulq	%rcx, %rdx
 588880a:      	movq	%rdx, %rax
 588880d:      	shrq	$0x2f, %rax
 5888811:      	xorq	%rdx, %rax
 5888814:      	imulq	%rcx, %rax
 5888818:      	popq	%rbx
 5888819:      	popq	%r12
 588881b:      	popq	%r13
 588881d:      	popq	%r14
 588881f:      	popq	%r15
 5888821:      	popq	%rbp
 5888822:      	retq
