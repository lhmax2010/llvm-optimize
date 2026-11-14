
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000033ee690 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 33ee690:      	movq	%rsi, %rcx
 33ee693:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 33ee69d:      	subq	%rdi, %rsi
 33ee6a0:      	cmpq	$0x40, %rsi
 33ee6a4:      	ja	0x33ee6b4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 33ee6a6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 33ee6ac:      	movq	%rax, %rdx
 33ee6af:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 33ee6b4:      	pushq	%rbp
 33ee6b5:      	pushq	%r15
 33ee6b7:      	pushq	%r14
 33ee6b9:      	pushq	%r13
 33ee6bb:      	pushq	%r12
 33ee6bd:      	pushq	%rbx
 33ee6be:      	movq	%rcx, -0x18(%rsp)
 33ee6c3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 33ee6cd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 33ee6d7:      	movq	%rsi, -0x10(%rsp)
 33ee6dc:      	movq	%rsi, %r14
 33ee6df:      	andq	$-0x40, %r14
 33ee6e3:      	movq	0x8(%rdi), %r13
 33ee6e7:      	movq	0x10(%rdi), %rcx
 33ee6eb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 33ee6f5:      	addq	%r13, %rdx
 33ee6f8:      	rolq	$0x1b, %rdx
 33ee6fc:      	imulq	%r9, %rdx
 33ee700:      	movq	0x30(%rdi), %rsi
 33ee704:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 33ee70e:      	addq	%rsi, %r10
 33ee711:      	rolq	$0x16, %r10
 33ee715:      	imulq	%r9, %r10
 33ee719:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 33ee723:      	xorq	%rdx, %rbp
 33ee726:      	movq	0x28(%rdi), %r12
 33ee72a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 33ee734:      	addq	%r12, %r9
 33ee737:      	addq	%r10, %r9
 33ee73a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 33ee744:      	addq	(%rdi), %r10
 33ee747:      	movq	0x18(%rdi), %r11
 33ee74b:      	addq	%r10, %rax
 33ee74e:      	addq	%r11, %rax
 33ee751:      	addq	%rbp, %rax
 33ee754:      	rolq	$0x2b, %rax
 33ee758:      	addq	%rcx, %r13
 33ee75b:      	addq	%r10, %r13
 33ee75e:      	movq	%r13, %rdx
 33ee761:      	rolq	$0x14, %rdx
 33ee765:      	addq	%r10, %rdx
 33ee768:      	addq	%rax, %rdx
 33ee76b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 33ee775:      	addq	0x20(%rdi), %rax
 33ee779:      	addq	%r11, %r13
 33ee77c:      	movq	0x38(%rdi), %r10
 33ee780:      	addq	%rax, %rcx
 33ee783:      	addq	%r10, %rcx
 33ee786:      	addq	%r9, %rcx
 33ee789:      	rolq	$0x2b, %rcx
 33ee78d:      	addq	%rsi, %r12
 33ee790:      	addq	%rax, %r12
 33ee793:      	movq	%r12, %rbx
 33ee796:      	rolq	$0x14, %rbx
 33ee79a:      	addq	%rax, %rbx
 33ee79d:      	addq	%rcx, %rbx
 33ee7a0:      	addq	%r10, %r12
 33ee7a3:      	movq	%r14, -0x20(%rsp)
 33ee7a8:      	cmpq	$0x40, %r14
 33ee7ac:      	jne	0x33ee7c2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 33ee7ae:      	movq	%rbx, %rsi
 33ee7b1:      	movq	%r12, %r11
 33ee7b4:      	movq	%rdx, %rax
 33ee7b7:      	movq	%r13, %r14
 33ee7ba:      	movq	%rbp, %r15
 33ee7bd:      	jmp	0x33ee8ad <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 33ee7c2:      	addq	$-0x40, -0x20(%rsp)
 33ee7c8:      	xorl	%ecx, %ecx
 33ee7ca:      	nopw	(%rax,%rax)
 33ee7d0:      	addq	%r9, %r8
 33ee7d3:      	addq	%r13, %r8
 33ee7d6:      	movq	0x48(%rdi,%rcx), %r14
 33ee7db:      	movq	0x50(%rdi,%rcx), %r10
 33ee7e0:      	addq	%r14, %r8
 33ee7e3:      	rolq	$0x1b, %r8
 33ee7e7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 33ee7f1:      	imulq	%rsi, %r8
 33ee7f5:      	addq	%rdx, %r9
 33ee7f8:      	movq	0x70(%rdi,%rcx), %rax
 33ee7fd:      	movq	%rax, -0x8(%rsp)
 33ee802:      	addq	%rax, %r9
 33ee805:      	rolq	$0x16, %r9
 33ee809:      	imulq	%rsi, %r9
 33ee80d:      	movq	%r8, %r15
 33ee810:      	xorq	%rbx, %r15
 33ee813:      	movq	0x68(%rdi,%rcx), %r11
 33ee818:      	addq	%r11, %r13
 33ee81b:      	addq	%r12, %rbp
 33ee81e:      	rolq	$0x1f, %rbp
 33ee822:      	addq	%r13, %r9
 33ee825:      	imulq	%rsi, %rdx
 33ee829:      	addq	0x40(%rdi,%rcx), %rdx
 33ee82e:      	movq	%rbp, %r8
 33ee831:      	movq	0x58(%rdi,%rcx), %r13
 33ee836:      	addq	%rdx, %r12
 33ee839:      	addq	%r13, %r12
 33ee83c:      	addq	%r15, %r12
 33ee83f:      	rolq	$0x2b, %r12
 33ee843:      	addq	%r10, %r14
 33ee846:      	addq	%rdx, %r14
 33ee849:      	movq	%r14, %rax
 33ee84c:      	rolq	$0x14, %rax
 33ee850:      	imulq	%rsi, %r8
 33ee854:      	addq	%rdx, %rax
 33ee857:      	addq	%r12, %rax
 33ee85a:      	addq	%r8, %rbx
 33ee85d:      	addq	%r9, %r10
 33ee860:      	addq	0x60(%rdi,%rcx), %rbx
 33ee865:      	movq	0x78(%rdi,%rcx), %rdx
 33ee86a:      	addq	%rbx, %r10
 33ee86d:      	addq	%rdx, %r10
 33ee870:      	rolq	$0x2b, %r10
 33ee874:      	addq	%r13, %r14
 33ee877:      	addq	-0x8(%rsp), %r11
 33ee87c:      	addq	%rbx, %r11
 33ee87f:      	movq	%r11, %rsi
 33ee882:      	rolq	$0x14, %rsi
 33ee886:      	addq	%rbx, %rsi
 33ee889:      	addq	%r10, %rsi
 33ee88c:      	addq	%rdx, %r11
 33ee88f:      	addq	$0x40, %rcx
 33ee893:      	movq	%r15, %rbp
 33ee896:      	movq	%r14, %r13
 33ee899:      	movq	%rax, %rdx
 33ee89c:      	movq	%r11, %r12
 33ee89f:      	movq	%rsi, %rbx
 33ee8a2:      	cmpq	%rcx, -0x20(%rsp)
 33ee8a7:      	jne	0x33ee7d0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 33ee8ad:      	movq	-0x10(%rsp), %r12
 33ee8b2:      	testb	$0x3f, %r12b
 33ee8b6:      	je	0x33ee982 <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f2>
 33ee8bc:      	movq	-0x18(%rsp), %rbp
 33ee8c1:      	movq	-0x38(%rbp), %rcx
 33ee8c5:      	movq	-0x30(%rbp), %rdx
 33ee8c9:      	addq	%rcx, %r8
 33ee8cc:      	addq	%r9, %r8
 33ee8cf:      	addq	%r14, %r8
 33ee8d2:      	rolq	$0x1b, %r8
 33ee8d6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 33ee8e0:      	imulq	%r13, %r8
 33ee8e4:      	addq	%rax, %r9
 33ee8e7:      	movq	-0x10(%rbp), %r10
 33ee8eb:      	addq	%r10, %r9
 33ee8ee:      	rolq	$0x16, %r9
 33ee8f2:      	imulq	%r13, %r9
 33ee8f6:      	xorq	%rsi, %r8
 33ee8f9:      	movq	-0x18(%rbp), %rdi
 33ee8fd:      	addq	%rdi, %r14
 33ee900:      	addq	%r14, %r9
 33ee903:      	addq	%r11, %r15
 33ee906:      	rolq	$0x1f, %r15
 33ee90a:      	movq	%r15, %rbx
 33ee90d:      	imulq	%r13, %rax
 33ee911:      	addq	%r8, %r11
 33ee914:      	addq	-0x40(%rbp), %rax
 33ee918:      	movq	-0x28(%rbp), %r15
 33ee91c:      	addq	%r15, %r11
 33ee91f:      	addq	%rax, %r11
 33ee922:      	rolq	$0x2b, %r11
 33ee926:      	imulq	%r13, %rbx
 33ee92a:      	addq	%rdx, %rcx
 33ee92d:      	addq	%rax, %rcx
 33ee930:      	movq	%rcx, %r14
 33ee933:      	rolq	$0x14, %r14
 33ee937:      	addq	%rax, %r14
 33ee93a:      	addq	%r11, %r14
 33ee93d:      	addq	%r15, %rcx
 33ee940:      	addq	%rbx, %rsi
 33ee943:      	addq	-0x20(%rbp), %rsi
 33ee947:      	addq	%r9, %rdx
 33ee94a:      	movq	-0x8(%rbp), %rax
 33ee94e:      	addq	%rax, %rdx
 33ee951:      	addq	%rsi, %rdx
 33ee954:      	rolq	$0x2b, %rdx
 33ee958:      	addq	%r10, %rdi
 33ee95b:      	addq	%rsi, %rdi
 33ee95e:      	movq	%rdi, %r10
 33ee961:      	rolq	$0x14, %r10
 33ee965:      	addq	%rsi, %r10
 33ee968:      	addq	%rdx, %r10
 33ee96b:      	addq	%rax, %rdi
 33ee96e:      	movq	%r10, %rsi
 33ee971:      	movq	%rdi, %r11
 33ee974:      	movq	%r14, %rax
 33ee977:      	movq	%rcx, %r14
 33ee97a:      	movq	%r8, %r15
 33ee97d:      	movq	%rbx, %r8
 33ee980:      	jmp	0x33ee98c <_ZN4llvm7hashing6detail23hash_combine_range_implIKjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fc>
 33ee982:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 33ee98c:      	xorq	%r11, %r14
 33ee98f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 33ee999:      	imulq	%rcx, %r14
 33ee99d:      	xorq	%r14, %r11
 33ee9a0:      	shrq	$0x2f, %r14
 33ee9a4:      	xorq	%r11, %r14
 33ee9a7:      	imulq	%rcx, %r14
 33ee9ab:      	movq	%r14, %rdi
 33ee9ae:      	shrq	$0x2f, %rdi
 33ee9b2:      	xorq	%r14, %rdi
 33ee9b5:      	imulq	%rcx, %rdi
 33ee9b9:      	movq	%r9, %rdx
 33ee9bc:      	shrq	$0x2f, %rdx
 33ee9c0:      	xorq	%r9, %rdx
 33ee9c3:      	imulq	%r13, %rdx
 33ee9c7:      	addq	%r15, %rdx
 33ee9ca:      	addq	%rdi, %rdx
 33ee9cd:      	xorq	%rsi, %rax
 33ee9d0:      	imulq	%rcx, %rax
 33ee9d4:      	xorq	%rax, %rsi
 33ee9d7:      	shrq	$0x2f, %rax
 33ee9db:      	xorq	%rsi, %rax
 33ee9de:      	imulq	%rcx, %rax
 33ee9e2:      	movq	%rax, %rsi
 33ee9e5:      	shrq	$0x2f, %rsi
 33ee9e9:      	xorq	%rax, %rsi
 33ee9ec:      	imulq	%rcx, %rsi
 33ee9f0:      	movq	%r12, %rax
 33ee9f3:      	shrq	$0x2f, %rax
 33ee9f7:      	xorq	%r12, %rax
 33ee9fa:      	imulq	%r13, %rax
 33ee9fe:      	addq	%r8, %rax
 33eea01:      	addq	%rsi, %rax
 33eea04:      	xorq	%rax, %rdx
 33eea07:      	imulq	%rcx, %rdx
 33eea0b:      	xorq	%rdx, %rax
 33eea0e:      	shrq	$0x2f, %rdx
 33eea12:      	xorq	%rax, %rdx
 33eea15:      	imulq	%rcx, %rdx
 33eea19:      	movq	%rdx, %rax
 33eea1c:      	shrq	$0x2f, %rax
 33eea20:      	xorq	%rdx, %rax
 33eea23:      	imulq	%rcx, %rax
 33eea27:      	popq	%rbx
 33eea28:      	popq	%r12
 33eea2a:      	popq	%r13
 33eea2c:      	popq	%r14
 33eea2e:      	popq	%r15
 33eea30:      	popq	%rbp
 33eea31:      	retq
