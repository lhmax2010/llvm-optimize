
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000041056c0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 41056c0:      	movq	%rsi, %rcx
 41056c3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 41056cd:      	subq	%rdi, %rsi
 41056d0:      	cmpq	$0x40, %rsi
 41056d4:      	ja	0x41056e4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 41056d6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 41056dc:      	movq	%rax, %rdx
 41056df:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 41056e4:      	pushq	%rbp
 41056e5:      	pushq	%r15
 41056e7:      	pushq	%r14
 41056e9:      	pushq	%r13
 41056eb:      	pushq	%r12
 41056ed:      	pushq	%rbx
 41056ee:      	movq	%rcx, -0x18(%rsp)
 41056f3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 41056fd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 4105707:      	movq	%rsi, -0x10(%rsp)
 410570c:      	movq	%rsi, %r14
 410570f:      	andq	$-0x40, %r14
 4105713:      	movq	0x8(%rdi), %r13
 4105717:      	movq	0x10(%rdi), %rcx
 410571b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 4105725:      	addq	%r13, %rdx
 4105728:      	rolq	$0x1b, %rdx
 410572c:      	imulq	%r9, %rdx
 4105730:      	movq	0x30(%rdi), %rsi
 4105734:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 410573e:      	addq	%rsi, %r10
 4105741:      	rolq	$0x16, %r10
 4105745:      	imulq	%r9, %r10
 4105749:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 4105753:      	xorq	%rdx, %rbp
 4105756:      	movq	0x28(%rdi), %r12
 410575a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 4105764:      	addq	%r12, %r9
 4105767:      	addq	%r10, %r9
 410576a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 4105774:      	addq	(%rdi), %r10
 4105777:      	movq	0x18(%rdi), %r11
 410577b:      	addq	%r10, %rax
 410577e:      	addq	%r11, %rax
 4105781:      	addq	%rbp, %rax
 4105784:      	rolq	$0x2b, %rax
 4105788:      	addq	%rcx, %r13
 410578b:      	addq	%r10, %r13
 410578e:      	movq	%r13, %rdx
 4105791:      	rolq	$0x14, %rdx
 4105795:      	addq	%r10, %rdx
 4105798:      	addq	%rax, %rdx
 410579b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 41057a5:      	addq	0x20(%rdi), %rax
 41057a9:      	addq	%r11, %r13
 41057ac:      	movq	0x38(%rdi), %r10
 41057b0:      	addq	%rax, %rcx
 41057b3:      	addq	%r10, %rcx
 41057b6:      	addq	%r9, %rcx
 41057b9:      	rolq	$0x2b, %rcx
 41057bd:      	addq	%rsi, %r12
 41057c0:      	addq	%rax, %r12
 41057c3:      	movq	%r12, %rbx
 41057c6:      	rolq	$0x14, %rbx
 41057ca:      	addq	%rax, %rbx
 41057cd:      	addq	%rcx, %rbx
 41057d0:      	addq	%r10, %r12
 41057d3:      	movq	%r14, -0x20(%rsp)
 41057d8:      	cmpq	$0x40, %r14
 41057dc:      	jne	0x41057f2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 41057de:      	movq	%rbx, %rsi
 41057e1:      	movq	%r12, %r11
 41057e4:      	movq	%rdx, %rax
 41057e7:      	movq	%r13, %r14
 41057ea:      	movq	%rbp, %r15
 41057ed:      	jmp	0x41058dd <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 41057f2:      	addq	$-0x40, -0x20(%rsp)
 41057f8:      	xorl	%ecx, %ecx
 41057fa:      	nopw	(%rax,%rax)
 4105800:      	addq	%r9, %r8
 4105803:      	addq	%r13, %r8
 4105806:      	movq	0x48(%rdi,%rcx), %r14
 410580b:      	movq	0x50(%rdi,%rcx), %r10
 4105810:      	addq	%r14, %r8
 4105813:      	rolq	$0x1b, %r8
 4105817:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 4105821:      	imulq	%rsi, %r8
 4105825:      	addq	%rdx, %r9
 4105828:      	movq	0x70(%rdi,%rcx), %rax
 410582d:      	movq	%rax, -0x8(%rsp)
 4105832:      	addq	%rax, %r9
 4105835:      	rolq	$0x16, %r9
 4105839:      	imulq	%rsi, %r9
 410583d:      	movq	%r8, %r15
 4105840:      	xorq	%rbx, %r15
 4105843:      	movq	0x68(%rdi,%rcx), %r11
 4105848:      	addq	%r11, %r13
 410584b:      	addq	%r12, %rbp
 410584e:      	rolq	$0x1f, %rbp
 4105852:      	addq	%r13, %r9
 4105855:      	imulq	%rsi, %rdx
 4105859:      	addq	0x40(%rdi,%rcx), %rdx
 410585e:      	movq	%rbp, %r8
 4105861:      	movq	0x58(%rdi,%rcx), %r13
 4105866:      	addq	%rdx, %r12
 4105869:      	addq	%r13, %r12
 410586c:      	addq	%r15, %r12
 410586f:      	rolq	$0x2b, %r12
 4105873:      	addq	%r10, %r14
 4105876:      	addq	%rdx, %r14
 4105879:      	movq	%r14, %rax
 410587c:      	rolq	$0x14, %rax
 4105880:      	imulq	%rsi, %r8
 4105884:      	addq	%rdx, %rax
 4105887:      	addq	%r12, %rax
 410588a:      	addq	%r8, %rbx
 410588d:      	addq	%r9, %r10
 4105890:      	addq	0x60(%rdi,%rcx), %rbx
 4105895:      	movq	0x78(%rdi,%rcx), %rdx
 410589a:      	addq	%rbx, %r10
 410589d:      	addq	%rdx, %r10
 41058a0:      	rolq	$0x2b, %r10
 41058a4:      	addq	%r13, %r14
 41058a7:      	addq	-0x8(%rsp), %r11
 41058ac:      	addq	%rbx, %r11
 41058af:      	movq	%r11, %rsi
 41058b2:      	rolq	$0x14, %rsi
 41058b6:      	addq	%rbx, %rsi
 41058b9:      	addq	%r10, %rsi
 41058bc:      	addq	%rdx, %r11
 41058bf:      	addq	$0x40, %rcx
 41058c3:      	movq	%r15, %rbp
 41058c6:      	movq	%r14, %r13
 41058c9:      	movq	%rax, %rdx
 41058cc:      	movq	%r11, %r12
 41058cf:      	movq	%rsi, %rbx
 41058d2:      	cmpq	%rcx, -0x20(%rsp)
 41058d7:      	jne	0x4105800 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 41058dd:      	movq	-0x10(%rsp), %r12
 41058e2:      	testb	$0x3f, %r12b
 41058e6:      	je	0x41059b3 <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f3>
 41058ec:      	leaq	(%r9,%r14), %rdi
 41058f0:      	movq	-0x18(%rsp), %rbp
 41058f5:      	movq	-0x38(%rbp), %rcx
 41058f9:      	movq	-0x30(%rbp), %rdx
 41058fd:      	addq	%rcx, %r8
 4105900:      	addq	%rdi, %r8
 4105903:      	rolq	$0x1b, %r8
 4105907:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 4105911:      	imulq	%r13, %r8
 4105915:      	addq	%rax, %r9
 4105918:      	movq	-0x10(%rbp), %r10
 410591c:      	addq	%r10, %r9
 410591f:      	rolq	$0x16, %r9
 4105923:      	imulq	%r13, %r9
 4105927:      	xorq	%rsi, %r8
 410592a:      	movq	-0x18(%rbp), %rdi
 410592e:      	addq	%rdi, %r14
 4105931:      	addq	%r14, %r9
 4105934:      	addq	%r11, %r15
 4105937:      	rolq	$0x1f, %r15
 410593b:      	movq	%r15, %rbx
 410593e:      	imulq	%r13, %rax
 4105942:      	addq	%r8, %r11
 4105945:      	addq	-0x40(%rbp), %rax
 4105949:      	movq	-0x28(%rbp), %r15
 410594d:      	addq	%r15, %r11
 4105950:      	addq	%rax, %r11
 4105953:      	rolq	$0x2b, %r11
 4105957:      	imulq	%r13, %rbx
 410595b:      	addq	%rdx, %rcx
 410595e:      	addq	%rax, %rcx
 4105961:      	movq	%rcx, %r14
 4105964:      	rolq	$0x14, %r14
 4105968:      	addq	%rax, %r14
 410596b:      	addq	%r11, %r14
 410596e:      	addq	%r15, %rcx
 4105971:      	addq	%rbx, %rsi
 4105974:      	addq	-0x20(%rbp), %rsi
 4105978:      	addq	%r9, %rdx
 410597b:      	movq	-0x8(%rbp), %rax
 410597f:      	addq	%rax, %rdx
 4105982:      	addq	%rsi, %rdx
 4105985:      	rolq	$0x2b, %rdx
 4105989:      	addq	%r10, %rdi
 410598c:      	addq	%rsi, %rdi
 410598f:      	movq	%rdi, %r10
 4105992:      	rolq	$0x14, %r10
 4105996:      	addq	%rsi, %r10
 4105999:      	addq	%rdx, %r10
 410599c:      	addq	%rax, %rdi
 410599f:      	movq	%r10, %rsi
 41059a2:      	movq	%rdi, %r11
 41059a5:      	movq	%r14, %rax
 41059a8:      	movq	%rcx, %r14
 41059ab:      	movq	%r8, %r15
 41059ae:      	movq	%rbx, %r8
 41059b1:      	jmp	0x41059bd <_ZN4llvm7hashing6detail23hash_combine_range_implIKcEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fd>
 41059b3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 41059bd:      	xorq	%r11, %r14
 41059c0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 41059ca:      	imulq	%rcx, %r14
 41059ce:      	xorq	%r14, %r11
 41059d1:      	shrq	$0x2f, %r14
 41059d5:      	xorq	%r11, %r14
 41059d8:      	imulq	%rcx, %r14
 41059dc:      	movq	%r14, %rdi
 41059df:      	shrq	$0x2f, %rdi
 41059e3:      	xorq	%r14, %rdi
 41059e6:      	imulq	%rcx, %rdi
 41059ea:      	movq	%r9, %rdx
 41059ed:      	shrq	$0x2f, %rdx
 41059f1:      	xorq	%r9, %rdx
 41059f4:      	imulq	%r13, %rdx
 41059f8:      	addq	%r15, %rdx
 41059fb:      	addq	%rdi, %rdx
 41059fe:      	xorq	%rsi, %rax
 4105a01:      	imulq	%rcx, %rax
 4105a05:      	xorq	%rax, %rsi
 4105a08:      	shrq	$0x2f, %rax
 4105a0c:      	xorq	%rsi, %rax
 4105a0f:      	imulq	%rcx, %rax
 4105a13:      	movq	%rax, %rsi
 4105a16:      	shrq	$0x2f, %rsi
 4105a1a:      	xorq	%rax, %rsi
 4105a1d:      	imulq	%rcx, %rsi
 4105a21:      	movq	%r12, %rax
 4105a24:      	shrq	$0x2f, %rax
 4105a28:      	xorq	%r12, %rax
 4105a2b:      	imulq	%r13, %rax
 4105a2f:      	addq	%r8, %rax
 4105a32:      	addq	%rsi, %rax
 4105a35:      	xorq	%rax, %rdx
 4105a38:      	imulq	%rcx, %rdx
 4105a3c:      	xorq	%rdx, %rax
 4105a3f:      	shrq	$0x2f, %rdx
 4105a43:      	xorq	%rax, %rdx
 4105a46:      	imulq	%rcx, %rdx
 4105a4a:      	movq	%rdx, %rax
 4105a4d:      	shrq	$0x2f, %rax
 4105a51:      	xorq	%rdx, %rax
 4105a54:      	imulq	%rcx, %rax
 4105a58:      	popq	%rbx
 4105a59:      	popq	%r12
 4105a5b:      	popq	%r13
 4105a5d:      	popq	%r14
 4105a5f:      	popq	%r15
 4105a61:      	popq	%rbp
 4105a62:      	retq
