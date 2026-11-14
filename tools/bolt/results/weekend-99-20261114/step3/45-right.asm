
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bbb880 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3bbb880:      	movq	%rsi, %rcx
 3bbb883:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3bbb88d:      	subq	%rdi, %rsi
 3bbb890:      	cmpq	$0x40, %rsi
 3bbb894:      	ja	0x3bbb8a4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3bbb896:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3bbb89c:      	movq	%rax, %rdx
 3bbb89f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3bbb8a4:      	pushq	%rbp
 3bbb8a5:      	pushq	%r15
 3bbb8a7:      	pushq	%r14
 3bbb8a9:      	pushq	%r13
 3bbb8ab:      	pushq	%r12
 3bbb8ad:      	pushq	%rbx
 3bbb8ae:      	movq	%rcx, -0x18(%rsp)
 3bbb8b3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3bbb8bd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3bbb8c7:      	movq	%rsi, -0x10(%rsp)
 3bbb8cc:      	movq	%rsi, %r14
 3bbb8cf:      	andq	$-0x40, %r14
 3bbb8d3:      	movq	0x8(%rdi), %r13
 3bbb8d7:      	movq	0x10(%rdi), %rcx
 3bbb8db:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3bbb8e5:      	addq	%r13, %rdx
 3bbb8e8:      	rolq	$0x1b, %rdx
 3bbb8ec:      	imulq	%r9, %rdx
 3bbb8f0:      	movq	0x30(%rdi), %rsi
 3bbb8f4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3bbb8fe:      	addq	%rsi, %r10
 3bbb901:      	rolq	$0x16, %r10
 3bbb905:      	imulq	%r9, %r10
 3bbb909:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3bbb913:      	xorq	%rdx, %rbp
 3bbb916:      	movq	0x28(%rdi), %r12
 3bbb91a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3bbb924:      	addq	%r12, %r9
 3bbb927:      	addq	%r10, %r9
 3bbb92a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3bbb934:      	addq	(%rdi), %r10
 3bbb937:      	movq	0x18(%rdi), %r11
 3bbb93b:      	addq	%r10, %rax
 3bbb93e:      	addq	%r11, %rax
 3bbb941:      	addq	%rbp, %rax
 3bbb944:      	rolq	$0x2b, %rax
 3bbb948:      	addq	%rcx, %r13
 3bbb94b:      	addq	%r10, %r13
 3bbb94e:      	movq	%r13, %rdx
 3bbb951:      	rolq	$0x14, %rdx
 3bbb955:      	addq	%r10, %rdx
 3bbb958:      	addq	%rax, %rdx
 3bbb95b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3bbb965:      	addq	0x20(%rdi), %rax
 3bbb969:      	addq	%r11, %r13
 3bbb96c:      	movq	0x38(%rdi), %r10
 3bbb970:      	addq	%rax, %rcx
 3bbb973:      	addq	%r10, %rcx
 3bbb976:      	addq	%r9, %rcx
 3bbb979:      	rolq	$0x2b, %rcx
 3bbb97d:      	addq	%rsi, %r12
 3bbb980:      	addq	%rax, %r12
 3bbb983:      	movq	%r12, %rbx
 3bbb986:      	rolq	$0x14, %rbx
 3bbb98a:      	addq	%rax, %rbx
 3bbb98d:      	addq	%rcx, %rbx
 3bbb990:      	addq	%r10, %r12
 3bbb993:      	movq	%r14, -0x20(%rsp)
 3bbb998:      	cmpq	$0x40, %r14
 3bbb99c:      	jne	0x3bbb9b2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3bbb99e:      	movq	%rbx, %rsi
 3bbb9a1:      	movq	%r12, %r11
 3bbb9a4:      	movq	%rdx, %rax
 3bbb9a7:      	movq	%r13, %r14
 3bbb9aa:      	movq	%rbp, %r15
 3bbb9ad:      	jmp	0x3bbba9d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3bbb9b2:      	addq	$-0x40, -0x20(%rsp)
 3bbb9b8:      	xorl	%ecx, %ecx
 3bbb9ba:      	nopw	(%rax,%rax)
 3bbb9c0:      	addq	%r9, %r8
 3bbb9c3:      	addq	%r13, %r8
 3bbb9c6:      	movq	0x48(%rdi,%rcx), %r14
 3bbb9cb:      	movq	0x50(%rdi,%rcx), %r10
 3bbb9d0:      	addq	%r14, %r8
 3bbb9d3:      	rolq	$0x1b, %r8
 3bbb9d7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3bbb9e1:      	imulq	%rsi, %r8
 3bbb9e5:      	addq	%rdx, %r9
 3bbb9e8:      	movq	0x70(%rdi,%rcx), %rax
 3bbb9ed:      	movq	%rax, -0x8(%rsp)
 3bbb9f2:      	addq	%rax, %r9
 3bbb9f5:      	rolq	$0x16, %r9
 3bbb9f9:      	imulq	%rsi, %r9
 3bbb9fd:      	movq	%r8, %r15
 3bbba00:      	xorq	%rbx, %r15
 3bbba03:      	movq	0x68(%rdi,%rcx), %r11
 3bbba08:      	addq	%r11, %r13
 3bbba0b:      	addq	%r12, %rbp
 3bbba0e:      	rolq	$0x1f, %rbp
 3bbba12:      	addq	%r13, %r9
 3bbba15:      	imulq	%rsi, %rdx
 3bbba19:      	addq	0x40(%rdi,%rcx), %rdx
 3bbba1e:      	movq	%rbp, %r8
 3bbba21:      	movq	0x58(%rdi,%rcx), %r13
 3bbba26:      	addq	%rdx, %r12
 3bbba29:      	addq	%r13, %r12
 3bbba2c:      	addq	%r15, %r12
 3bbba2f:      	rolq	$0x2b, %r12
 3bbba33:      	addq	%r10, %r14
 3bbba36:      	addq	%rdx, %r14
 3bbba39:      	movq	%r14, %rax
 3bbba3c:      	rolq	$0x14, %rax
 3bbba40:      	imulq	%rsi, %r8
 3bbba44:      	addq	%rdx, %rax
 3bbba47:      	addq	%r12, %rax
 3bbba4a:      	addq	%r8, %rbx
 3bbba4d:      	addq	%r9, %r10
 3bbba50:      	addq	0x60(%rdi,%rcx), %rbx
 3bbba55:      	movq	0x78(%rdi,%rcx), %rdx
 3bbba5a:      	addq	%rbx, %r10
 3bbba5d:      	addq	%rdx, %r10
 3bbba60:      	rolq	$0x2b, %r10
 3bbba64:      	addq	%r13, %r14
 3bbba67:      	addq	-0x8(%rsp), %r11
 3bbba6c:      	addq	%rbx, %r11
 3bbba6f:      	movq	%r11, %rsi
 3bbba72:      	rolq	$0x14, %rsi
 3bbba76:      	addq	%rbx, %rsi
 3bbba79:      	addq	%r10, %rsi
 3bbba7c:      	addq	%rdx, %r11
 3bbba7f:      	addq	$0x40, %rcx
 3bbba83:      	movq	%r15, %rbp
 3bbba86:      	movq	%r14, %r13
 3bbba89:      	movq	%rax, %rdx
 3bbba8c:      	movq	%r11, %r12
 3bbba8f:      	movq	%rsi, %rbx
 3bbba92:      	cmpq	%rcx, -0x20(%rsp)
 3bbba97:      	jne	0x3bbb9c0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3bbba9d:      	movq	-0x10(%rsp), %r12
 3bbbaa2:      	testb	$0x3f, %r12b
 3bbbaa6:      	je	0x3bbbb72 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f2>
 3bbbaac:      	movq	-0x18(%rsp), %rbp
 3bbbab1:      	movq	-0x38(%rbp), %rcx
 3bbbab5:      	movq	-0x30(%rbp), %rdx
 3bbbab9:      	addq	%rcx, %r8
 3bbbabc:      	addq	%r9, %r8
 3bbbabf:      	addq	%r14, %r8
 3bbbac2:      	rolq	$0x1b, %r8
 3bbbac6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3bbbad0:      	imulq	%r13, %r8
 3bbbad4:      	addq	%rax, %r9
 3bbbad7:      	movq	-0x10(%rbp), %r10
 3bbbadb:      	addq	%r10, %r9
 3bbbade:      	rolq	$0x16, %r9
 3bbbae2:      	imulq	%r13, %r9
 3bbbae6:      	xorq	%rsi, %r8
 3bbbae9:      	movq	-0x18(%rbp), %rdi
 3bbbaed:      	addq	%rdi, %r14
 3bbbaf0:      	addq	%r14, %r9
 3bbbaf3:      	addq	%r11, %r15
 3bbbaf6:      	rolq	$0x1f, %r15
 3bbbafa:      	movq	%r15, %rbx
 3bbbafd:      	imulq	%r13, %rax
 3bbbb01:      	addq	%r8, %r11
 3bbbb04:      	addq	-0x40(%rbp), %rax
 3bbbb08:      	movq	-0x28(%rbp), %r15
 3bbbb0c:      	addq	%r15, %r11
 3bbbb0f:      	addq	%rax, %r11
 3bbbb12:      	rolq	$0x2b, %r11
 3bbbb16:      	imulq	%r13, %rbx
 3bbbb1a:      	addq	%rdx, %rcx
 3bbbb1d:      	addq	%rax, %rcx
 3bbbb20:      	movq	%rcx, %r14
 3bbbb23:      	rolq	$0x14, %r14
 3bbbb27:      	addq	%rax, %r14
 3bbbb2a:      	addq	%r11, %r14
 3bbbb2d:      	addq	%r15, %rcx
 3bbbb30:      	addq	%rbx, %rsi
 3bbbb33:      	addq	-0x20(%rbp), %rsi
 3bbbb37:      	addq	%r9, %rdx
 3bbbb3a:      	movq	-0x8(%rbp), %rax
 3bbbb3e:      	addq	%rax, %rdx
 3bbbb41:      	addq	%rsi, %rdx
 3bbbb44:      	rolq	$0x2b, %rdx
 3bbbb48:      	addq	%r10, %rdi
 3bbbb4b:      	addq	%rsi, %rdi
 3bbbb4e:      	movq	%rdi, %r10
 3bbbb51:      	rolq	$0x14, %r10
 3bbbb55:      	addq	%rsi, %r10
 3bbbb58:      	addq	%rdx, %r10
 3bbbb5b:      	addq	%rax, %rdi
 3bbbb5e:      	movq	%r10, %rsi
 3bbbb61:      	movq	%rdi, %r11
 3bbbb64:      	movq	%r14, %rax
 3bbbb67:      	movq	%rcx, %r14
 3bbbb6a:      	movq	%r8, %r15
 3bbbb6d:      	movq	%rbx, %r8
 3bbbb70:      	jmp	0x3bbbb7c <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fc>
 3bbbb72:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3bbbb7c:      	xorq	%r11, %r14
 3bbbb7f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3bbbb89:      	imulq	%rcx, %r14
 3bbbb8d:      	xorq	%r14, %r11
 3bbbb90:      	shrq	$0x2f, %r14
 3bbbb94:      	xorq	%r11, %r14
 3bbbb97:      	imulq	%rcx, %r14
 3bbbb9b:      	movq	%r14, %rdi
 3bbbb9e:      	shrq	$0x2f, %rdi
 3bbbba2:      	xorq	%r14, %rdi
 3bbbba5:      	imulq	%rcx, %rdi
 3bbbba9:      	movq	%r9, %rdx
 3bbbbac:      	shrq	$0x2f, %rdx
 3bbbbb0:      	xorq	%r9, %rdx
 3bbbbb3:      	imulq	%r13, %rdx
 3bbbbb7:      	addq	%r15, %rdx
 3bbbbba:      	addq	%rdi, %rdx
 3bbbbbd:      	xorq	%rsi, %rax
 3bbbbc0:      	imulq	%rcx, %rax
 3bbbbc4:      	xorq	%rax, %rsi
 3bbbbc7:      	shrq	$0x2f, %rax
 3bbbbcb:      	xorq	%rsi, %rax
 3bbbbce:      	imulq	%rcx, %rax
 3bbbbd2:      	movq	%rax, %rsi
 3bbbbd5:      	shrq	$0x2f, %rsi
 3bbbbd9:      	xorq	%rax, %rsi
 3bbbbdc:      	imulq	%rcx, %rsi
 3bbbbe0:      	movq	%r12, %rax
 3bbbbe3:      	shrq	$0x2f, %rax
 3bbbbe7:      	xorq	%r12, %rax
 3bbbbea:      	imulq	%r13, %rax
 3bbbbee:      	addq	%r8, %rax
 3bbbbf1:      	addq	%rsi, %rax
 3bbbbf4:      	xorq	%rax, %rdx
 3bbbbf7:      	imulq	%rcx, %rdx
 3bbbbfb:      	xorq	%rdx, %rax
 3bbbbfe:      	shrq	$0x2f, %rdx
 3bbbc02:      	xorq	%rax, %rdx
 3bbbc05:      	imulq	%rcx, %rdx
 3bbbc09:      	movq	%rdx, %rax
 3bbbc0c:      	shrq	$0x2f, %rax
 3bbbc10:      	xorq	%rdx, %rax
 3bbbc13:      	imulq	%rcx, %rax
 3bbbc17:      	popq	%rbx
 3bbbc18:      	popq	%r12
 3bbbc1a:      	popq	%r13
 3bbbc1c:      	popq	%r14
 3bbbc1e:      	popq	%r15
 3bbbc20:      	popq	%rbp
 3bbbc21:      	retq
