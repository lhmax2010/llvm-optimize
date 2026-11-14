
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004105630 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 4105630:      	movq	%rsi, %rcx
 4105633:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 410563d:      	subq	%rdi, %rsi
 4105640:      	cmpq	$0x40, %rsi
 4105644:      	ja	0x4105654 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 4105646:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 410564c:      	movq	%rax, %rdx
 410564f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 4105654:      	pushq	%rbp
 4105655:      	pushq	%r15
 4105657:      	pushq	%r14
 4105659:      	pushq	%r13
 410565b:      	pushq	%r12
 410565d:      	pushq	%rbx
 410565e:      	movq	%rcx, -0x18(%rsp)
 4105663:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 410566d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 4105677:      	movq	%rsi, -0x10(%rsp)
 410567c:      	movq	%rsi, %r14
 410567f:      	andq	$-0x40, %r14
 4105683:      	movq	0x8(%rdi), %r13
 4105687:      	movq	0x10(%rdi), %rcx
 410568b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 4105695:      	addq	%r13, %rdx
 4105698:      	rolq	$0x1b, %rdx
 410569c:      	imulq	%r9, %rdx
 41056a0:      	movq	0x30(%rdi), %rsi
 41056a4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 41056ae:      	addq	%rsi, %r10
 41056b1:      	rolq	$0x16, %r10
 41056b5:      	imulq	%r9, %r10
 41056b9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 41056c3:      	xorq	%rdx, %rbp
 41056c6:      	movq	0x28(%rdi), %r12
 41056ca:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 41056d4:      	addq	%r12, %r9
 41056d7:      	addq	%r10, %r9
 41056da:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 41056e4:      	addq	(%rdi), %r10
 41056e7:      	movq	0x18(%rdi), %r11
 41056eb:      	addq	%r10, %rax
 41056ee:      	addq	%r11, %rax
 41056f1:      	addq	%rbp, %rax
 41056f4:      	rolq	$0x2b, %rax
 41056f8:      	addq	%rcx, %r13
 41056fb:      	addq	%r10, %r13
 41056fe:      	movq	%r13, %rdx
 4105701:      	rolq	$0x14, %rdx
 4105705:      	addq	%r10, %rdx
 4105708:      	addq	%rax, %rdx
 410570b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 4105715:      	addq	0x20(%rdi), %rax
 4105719:      	addq	%r11, %r13
 410571c:      	movq	0x38(%rdi), %r10
 4105720:      	addq	%rax, %rcx
 4105723:      	addq	%r10, %rcx
 4105726:      	addq	%r9, %rcx
 4105729:      	rolq	$0x2b, %rcx
 410572d:      	addq	%rsi, %r12
 4105730:      	addq	%rax, %r12
 4105733:      	movq	%r12, %rbx
 4105736:      	rolq	$0x14, %rbx
 410573a:      	addq	%rax, %rbx
 410573d:      	addq	%rcx, %rbx
 4105740:      	addq	%r10, %r12
 4105743:      	movq	%r14, -0x20(%rsp)
 4105748:      	cmpq	$0x40, %r14
 410574c:      	jne	0x4105762 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 410574e:      	movq	%rbx, %rsi
 4105751:      	movq	%r12, %r11
 4105754:      	movq	%rdx, %rax
 4105757:      	movq	%r13, %r14
 410575a:      	movq	%rbp, %r15
 410575d:      	jmp	0x410584d <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 4105762:      	addq	$-0x40, -0x20(%rsp)
 4105768:      	xorl	%ecx, %ecx
 410576a:      	nopw	(%rax,%rax)
 4105770:      	addq	%r9, %r8
 4105773:      	addq	%r13, %r8
 4105776:      	movq	0x48(%rdi,%rcx), %r14
 410577b:      	movq	0x50(%rdi,%rcx), %r10
 4105780:      	addq	%r14, %r8
 4105783:      	rolq	$0x1b, %r8
 4105787:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 4105791:      	imulq	%rsi, %r8
 4105795:      	addq	%rdx, %r9
 4105798:      	movq	0x70(%rdi,%rcx), %rax
 410579d:      	movq	%rax, -0x8(%rsp)
 41057a2:      	addq	%rax, %r9
 41057a5:      	rolq	$0x16, %r9
 41057a9:      	imulq	%rsi, %r9
 41057ad:      	movq	%r8, %r15
 41057b0:      	xorq	%rbx, %r15
 41057b3:      	movq	0x68(%rdi,%rcx), %r11
 41057b8:      	addq	%r11, %r13
 41057bb:      	addq	%r12, %rbp
 41057be:      	rolq	$0x1f, %rbp
 41057c2:      	addq	%r13, %r9
 41057c5:      	imulq	%rsi, %rdx
 41057c9:      	addq	0x40(%rdi,%rcx), %rdx
 41057ce:      	movq	%rbp, %r8
 41057d1:      	movq	0x58(%rdi,%rcx), %r13
 41057d6:      	addq	%rdx, %r12
 41057d9:      	addq	%r13, %r12
 41057dc:      	addq	%r15, %r12
 41057df:      	rolq	$0x2b, %r12
 41057e3:      	addq	%r10, %r14
 41057e6:      	addq	%rdx, %r14
 41057e9:      	movq	%r14, %rax
 41057ec:      	rolq	$0x14, %rax
 41057f0:      	imulq	%rsi, %r8
 41057f4:      	addq	%rdx, %rax
 41057f7:      	addq	%r12, %rax
 41057fa:      	addq	%r8, %rbx
 41057fd:      	addq	%r9, %r10
 4105800:      	addq	0x60(%rdi,%rcx), %rbx
 4105805:      	movq	0x78(%rdi,%rcx), %rdx
 410580a:      	addq	%rbx, %r10
 410580d:      	addq	%rdx, %r10
 4105810:      	rolq	$0x2b, %r10
 4105814:      	addq	%r13, %r14
 4105817:      	addq	-0x8(%rsp), %r11
 410581c:      	addq	%rbx, %r11
 410581f:      	movq	%r11, %rsi
 4105822:      	rolq	$0x14, %rsi
 4105826:      	addq	%rbx, %rsi
 4105829:      	addq	%r10, %rsi
 410582c:      	addq	%rdx, %r11
 410582f:      	addq	$0x40, %rcx
 4105833:      	movq	%r15, %rbp
 4105836:      	movq	%r14, %r13
 4105839:      	movq	%rax, %rdx
 410583c:      	movq	%r11, %r12
 410583f:      	movq	%rsi, %rbx
 4105842:      	cmpq	%rcx, -0x20(%rsp)
 4105847:      	jne	0x4105770 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 410584d:      	movq	-0x10(%rsp), %r12
 4105852:      	testb	$0x3f, %r12b
 4105856:      	je	0x4105922 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f2>
 410585c:      	movq	-0x18(%rsp), %rbp
 4105861:      	movq	-0x38(%rbp), %rcx
 4105865:      	movq	-0x30(%rbp), %rdx
 4105869:      	addq	%rcx, %r8
 410586c:      	addq	%r9, %r8
 410586f:      	addq	%r14, %r8
 4105872:      	rolq	$0x1b, %r8
 4105876:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 4105880:      	imulq	%r13, %r8
 4105884:      	addq	%rax, %r9
 4105887:      	movq	-0x10(%rbp), %r10
 410588b:      	addq	%r10, %r9
 410588e:      	rolq	$0x16, %r9
 4105892:      	imulq	%r13, %r9
 4105896:      	xorq	%rsi, %r8
 4105899:      	movq	-0x18(%rbp), %rdi
 410589d:      	addq	%rdi, %r14
 41058a0:      	addq	%r14, %r9
 41058a3:      	addq	%r11, %r15
 41058a6:      	rolq	$0x1f, %r15
 41058aa:      	movq	%r15, %rbx
 41058ad:      	imulq	%r13, %rax
 41058b1:      	addq	%r8, %r11
 41058b4:      	addq	-0x40(%rbp), %rax
 41058b8:      	movq	-0x28(%rbp), %r15
 41058bc:      	addq	%r15, %r11
 41058bf:      	addq	%rax, %r11
 41058c2:      	rolq	$0x2b, %r11
 41058c6:      	imulq	%r13, %rbx
 41058ca:      	addq	%rdx, %rcx
 41058cd:      	addq	%rax, %rcx
 41058d0:      	movq	%rcx, %r14
 41058d3:      	rolq	$0x14, %r14
 41058d7:      	addq	%rax, %r14
 41058da:      	addq	%r11, %r14
 41058dd:      	addq	%r15, %rcx
 41058e0:      	addq	%rbx, %rsi
 41058e3:      	addq	-0x20(%rbp), %rsi
 41058e7:      	addq	%r9, %rdx
 41058ea:      	movq	-0x8(%rbp), %rax
 41058ee:      	addq	%rax, %rdx
 41058f1:      	addq	%rsi, %rdx
 41058f4:      	rolq	$0x2b, %rdx
 41058f8:      	addq	%r10, %rdi
 41058fb:      	addq	%rsi, %rdi
 41058fe:      	movq	%rdi, %r10
 4105901:      	rolq	$0x14, %r10
 4105905:      	addq	%rsi, %r10
 4105908:      	addq	%rdx, %r10
 410590b:      	addq	%rax, %rdi
 410590e:      	movq	%r10, %rsi
 4105911:      	movq	%rdi, %r11
 4105914:      	movq	%r14, %rax
 4105917:      	movq	%rcx, %r14
 410591a:      	movq	%r8, %r15
 410591d:      	movq	%rbx, %r8
 4105920:      	jmp	0x410592c <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fc>
 4105922:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 410592c:      	xorq	%r11, %r14
 410592f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 4105939:      	imulq	%rcx, %r14
 410593d:      	xorq	%r14, %r11
 4105940:      	shrq	$0x2f, %r14
 4105944:      	xorq	%r11, %r14
 4105947:      	imulq	%rcx, %r14
 410594b:      	movq	%r14, %rdi
 410594e:      	shrq	$0x2f, %rdi
 4105952:      	xorq	%r14, %rdi
 4105955:      	imulq	%rcx, %rdi
 4105959:      	movq	%r9, %rdx
 410595c:      	shrq	$0x2f, %rdx
 4105960:      	xorq	%r9, %rdx
 4105963:      	imulq	%r13, %rdx
 4105967:      	addq	%r15, %rdx
 410596a:      	addq	%rdi, %rdx
 410596d:      	xorq	%rsi, %rax
 4105970:      	imulq	%rcx, %rax
 4105974:      	xorq	%rax, %rsi
 4105977:      	shrq	$0x2f, %rax
 410597b:      	xorq	%rsi, %rax
 410597e:      	imulq	%rcx, %rax
 4105982:      	movq	%rax, %rsi
 4105985:      	shrq	$0x2f, %rsi
 4105989:      	xorq	%rax, %rsi
 410598c:      	imulq	%rcx, %rsi
 4105990:      	movq	%r12, %rax
 4105993:      	shrq	$0x2f, %rax
 4105997:      	xorq	%r12, %rax
 410599a:      	imulq	%r13, %rax
 410599e:      	addq	%r8, %rax
 41059a1:      	addq	%rsi, %rax
 41059a4:      	xorq	%rax, %rdx
 41059a7:      	imulq	%rcx, %rdx
 41059ab:      	xorq	%rdx, %rax
 41059ae:      	shrq	$0x2f, %rdx
 41059b2:      	xorq	%rax, %rdx
 41059b5:      	imulq	%rcx, %rdx
 41059b9:      	movq	%rdx, %rax
 41059bc:      	shrq	$0x2f, %rax
 41059c0:      	xorq	%rdx, %rax
 41059c3:      	imulq	%rcx, %rax
 41059c7:      	popq	%rbx
 41059c8:      	popq	%r12
 41059ca:      	popq	%r13
 41059cc:      	popq	%r14
 41059ce:      	popq	%r15
 41059d0:      	popq	%rbp
 41059d1:      	retq
