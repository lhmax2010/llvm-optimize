
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bbb910 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_>:
 3bbb910:      	movq	%rsi, %rcx
 3bbb913:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3bbb91d:      	subq	%rdi, %rsi
 3bbb920:      	cmpq	$0x40, %rsi
 3bbb924:      	ja	0x3bbb934 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x24>
 3bbb926:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3bbb92c:      	movq	%rax, %rdx
 3bbb92f:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3bbb934:      	pushq	%rbp
 3bbb935:      	pushq	%r15
 3bbb937:      	pushq	%r14
 3bbb939:      	pushq	%r13
 3bbb93b:      	pushq	%r12
 3bbb93d:      	pushq	%rbx
 3bbb93e:      	movq	%rcx, -0x18(%rsp)
 3bbb943:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3bbb94d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3bbb957:      	movq	%rsi, -0x10(%rsp)
 3bbb95c:      	movq	%rsi, %r14
 3bbb95f:      	andq	$-0x40, %r14
 3bbb963:      	movq	0x8(%rdi), %r13
 3bbb967:      	movq	0x10(%rdi), %rcx
 3bbb96b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3bbb975:      	addq	%r13, %rdx
 3bbb978:      	rolq	$0x1b, %rdx
 3bbb97c:      	imulq	%r9, %rdx
 3bbb980:      	movq	0x30(%rdi), %rsi
 3bbb984:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3bbb98e:      	addq	%rsi, %r10
 3bbb991:      	rolq	$0x16, %r10
 3bbb995:      	imulq	%r9, %r10
 3bbb999:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3bbb9a3:      	xorq	%rdx, %rbp
 3bbb9a6:      	movq	0x28(%rdi), %r12
 3bbb9aa:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3bbb9b4:      	addq	%r12, %r9
 3bbb9b7:      	addq	%r10, %r9
 3bbb9ba:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3bbb9c4:      	addq	(%rdi), %r10
 3bbb9c7:      	movq	0x18(%rdi), %r11
 3bbb9cb:      	addq	%r10, %rax
 3bbb9ce:      	addq	%r11, %rax
 3bbb9d1:      	addq	%rbp, %rax
 3bbb9d4:      	rolq	$0x2b, %rax
 3bbb9d8:      	addq	%rcx, %r13
 3bbb9db:      	addq	%r10, %r13
 3bbb9de:      	movq	%r13, %rdx
 3bbb9e1:      	rolq	$0x14, %rdx
 3bbb9e5:      	addq	%r10, %rdx
 3bbb9e8:      	addq	%rax, %rdx
 3bbb9eb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3bbb9f5:      	addq	0x20(%rdi), %rax
 3bbb9f9:      	addq	%r11, %r13
 3bbb9fc:      	movq	0x38(%rdi), %r10
 3bbba00:      	addq	%rax, %rcx
 3bbba03:      	addq	%r10, %rcx
 3bbba06:      	addq	%r9, %rcx
 3bbba09:      	rolq	$0x2b, %rcx
 3bbba0d:      	addq	%rsi, %r12
 3bbba10:      	addq	%rax, %r12
 3bbba13:      	movq	%r12, %rbx
 3bbba16:      	rolq	$0x14, %rbx
 3bbba1a:      	addq	%rax, %rbx
 3bbba1d:      	addq	%rcx, %rbx
 3bbba20:      	addq	%r10, %r12
 3bbba23:      	movq	%r14, -0x20(%rsp)
 3bbba28:      	cmpq	$0x40, %r14
 3bbba2c:      	jne	0x3bbba42 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x132>
 3bbba2e:      	movq	%rbx, %rsi
 3bbba31:      	movq	%r12, %r11
 3bbba34:      	movq	%rdx, %rax
 3bbba37:      	movq	%r13, %r14
 3bbba3a:      	movq	%rbp, %r15
 3bbba3d:      	jmp	0x3bbbb2d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x21d>
 3bbba42:      	addq	$-0x40, -0x20(%rsp)
 3bbba48:      	xorl	%ecx, %ecx
 3bbba4a:      	nopw	(%rax,%rax)
 3bbba50:      	addq	%r9, %r8
 3bbba53:      	addq	%r13, %r8
 3bbba56:      	movq	0x48(%rdi,%rcx), %r14
 3bbba5b:      	movq	0x50(%rdi,%rcx), %r10
 3bbba60:      	addq	%r14, %r8
 3bbba63:      	rolq	$0x1b, %r8
 3bbba67:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3bbba71:      	imulq	%rsi, %r8
 3bbba75:      	addq	%rdx, %r9
 3bbba78:      	movq	0x70(%rdi,%rcx), %rax
 3bbba7d:      	movq	%rax, -0x8(%rsp)
 3bbba82:      	addq	%rax, %r9
 3bbba85:      	rolq	$0x16, %r9
 3bbba89:      	imulq	%rsi, %r9
 3bbba8d:      	movq	%r8, %r15
 3bbba90:      	xorq	%rbx, %r15
 3bbba93:      	movq	0x68(%rdi,%rcx), %r11
 3bbba98:      	addq	%r11, %r13
 3bbba9b:      	addq	%r12, %rbp
 3bbba9e:      	rolq	$0x1f, %rbp
 3bbbaa2:      	addq	%r13, %r9
 3bbbaa5:      	imulq	%rsi, %rdx
 3bbbaa9:      	addq	0x40(%rdi,%rcx), %rdx
 3bbbaae:      	movq	%rbp, %r8
 3bbbab1:      	movq	0x58(%rdi,%rcx), %r13
 3bbbab6:      	addq	%rdx, %r12
 3bbbab9:      	addq	%r13, %r12
 3bbbabc:      	addq	%r15, %r12
 3bbbabf:      	rolq	$0x2b, %r12
 3bbbac3:      	addq	%r10, %r14
 3bbbac6:      	addq	%rdx, %r14
 3bbbac9:      	movq	%r14, %rax
 3bbbacc:      	rolq	$0x14, %rax
 3bbbad0:      	imulq	%rsi, %r8
 3bbbad4:      	addq	%rdx, %rax
 3bbbad7:      	addq	%r12, %rax
 3bbbada:      	addq	%r8, %rbx
 3bbbadd:      	addq	%r9, %r10
 3bbbae0:      	addq	0x60(%rdi,%rcx), %rbx
 3bbbae5:      	movq	0x78(%rdi,%rcx), %rdx
 3bbbaea:      	addq	%rbx, %r10
 3bbbaed:      	addq	%rdx, %r10
 3bbbaf0:      	rolq	$0x2b, %r10
 3bbbaf4:      	addq	%r13, %r14
 3bbbaf7:      	addq	-0x8(%rsp), %r11
 3bbbafc:      	addq	%rbx, %r11
 3bbbaff:      	movq	%r11, %rsi
 3bbbb02:      	rolq	$0x14, %rsi
 3bbbb06:      	addq	%rbx, %rsi
 3bbbb09:      	addq	%r10, %rsi
 3bbbb0c:      	addq	%rdx, %r11
 3bbbb0f:      	addq	$0x40, %rcx
 3bbbb13:      	movq	%r15, %rbp
 3bbbb16:      	movq	%r14, %r13
 3bbbb19:      	movq	%rax, %rdx
 3bbbb1c:      	movq	%r11, %r12
 3bbbb1f:      	movq	%rsi, %rbx
 3bbbb22:      	cmpq	%rcx, -0x20(%rsp)
 3bbbb27:      	jne	0x3bbba50 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x140>
 3bbbb2d:      	movq	-0x10(%rsp), %r12
 3bbbb32:      	testb	$0x3f, %r12b
 3bbbb36:      	je	0x3bbbc03 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2f3>
 3bbbb3c:      	leaq	(%r9,%r14), %rdi
 3bbbb40:      	movq	-0x18(%rsp), %rbp
 3bbbb45:      	movq	-0x38(%rbp), %rcx
 3bbbb49:      	movq	-0x30(%rbp), %rdx
 3bbbb4d:      	addq	%rcx, %r8
 3bbbb50:      	addq	%rdi, %r8
 3bbbb53:      	rolq	$0x1b, %r8
 3bbbb57:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3bbbb61:      	imulq	%r13, %r8
 3bbbb65:      	addq	%rax, %r9
 3bbbb68:      	movq	-0x10(%rbp), %r10
 3bbbb6c:      	addq	%r10, %r9
 3bbbb6f:      	rolq	$0x16, %r9
 3bbbb73:      	imulq	%r13, %r9
 3bbbb77:      	xorq	%rsi, %r8
 3bbbb7a:      	movq	-0x18(%rbp), %rdi
 3bbbb7e:      	addq	%rdi, %r14
 3bbbb81:      	addq	%r14, %r9
 3bbbb84:      	addq	%r11, %r15
 3bbbb87:      	rolq	$0x1f, %r15
 3bbbb8b:      	movq	%r15, %rbx
 3bbbb8e:      	imulq	%r13, %rax
 3bbbb92:      	addq	%r8, %r11
 3bbbb95:      	addq	-0x40(%rbp), %rax
 3bbbb99:      	movq	-0x28(%rbp), %r15
 3bbbb9d:      	addq	%r15, %r11
 3bbbba0:      	addq	%rax, %r11
 3bbbba3:      	rolq	$0x2b, %r11
 3bbbba7:      	imulq	%r13, %rbx
 3bbbbab:      	addq	%rdx, %rcx
 3bbbbae:      	addq	%rax, %rcx
 3bbbbb1:      	movq	%rcx, %r14
 3bbbbb4:      	rolq	$0x14, %r14
 3bbbbb8:      	addq	%rax, %r14
 3bbbbbb:      	addq	%r11, %r14
 3bbbbbe:      	addq	%r15, %rcx
 3bbbbc1:      	addq	%rbx, %rsi
 3bbbbc4:      	addq	-0x20(%rbp), %rsi
 3bbbbc8:      	addq	%r9, %rdx
 3bbbbcb:      	movq	-0x8(%rbp), %rax
 3bbbbcf:      	addq	%rax, %rdx
 3bbbbd2:      	addq	%rsi, %rdx
 3bbbbd5:      	rolq	$0x2b, %rdx
 3bbbbd9:      	addq	%r10, %rdi
 3bbbbdc:      	addq	%rsi, %rdi
 3bbbbdf:      	movq	%rdi, %r10
 3bbbbe2:      	rolq	$0x14, %r10
 3bbbbe6:      	addq	%rsi, %r10
 3bbbbe9:      	addq	%rdx, %r10
 3bbbbec:      	addq	%rax, %rdi
 3bbbbef:      	movq	%r10, %rsi
 3bbbbf2:      	movq	%rdi, %r11
 3bbbbf5:      	movq	%r14, %rax
 3bbbbf8:      	movq	%rcx, %r14
 3bbbbfb:      	movq	%r8, %r15
 3bbbbfe:      	movq	%rbx, %r8
 3bbbc01:      	jmp	0x3bbbc0d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPNS_8MetadataEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS7_SB_+0x2fd>
 3bbbc03:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3bbbc0d:      	xorq	%r11, %r14
 3bbbc10:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3bbbc1a:      	imulq	%rcx, %r14
 3bbbc1e:      	xorq	%r14, %r11
 3bbbc21:      	shrq	$0x2f, %r14
 3bbbc25:      	xorq	%r11, %r14
 3bbbc28:      	imulq	%rcx, %r14
 3bbbc2c:      	movq	%r14, %rdi
 3bbbc2f:      	shrq	$0x2f, %rdi
 3bbbc33:      	xorq	%r14, %rdi
 3bbbc36:      	imulq	%rcx, %rdi
 3bbbc3a:      	movq	%r9, %rdx
 3bbbc3d:      	shrq	$0x2f, %rdx
 3bbbc41:      	xorq	%r9, %rdx
 3bbbc44:      	imulq	%r13, %rdx
 3bbbc48:      	addq	%r15, %rdx
 3bbbc4b:      	addq	%rdi, %rdx
 3bbbc4e:      	xorq	%rsi, %rax
 3bbbc51:      	imulq	%rcx, %rax
 3bbbc55:      	xorq	%rax, %rsi
 3bbbc58:      	shrq	$0x2f, %rax
 3bbbc5c:      	xorq	%rsi, %rax
 3bbbc5f:      	imulq	%rcx, %rax
 3bbbc63:      	movq	%rax, %rsi
 3bbbc66:      	shrq	$0x2f, %rsi
 3bbbc6a:      	xorq	%rax, %rsi
 3bbbc6d:      	imulq	%rcx, %rsi
 3bbbc71:      	movq	%r12, %rax
 3bbbc74:      	shrq	$0x2f, %rax
 3bbbc78:      	xorq	%r12, %rax
 3bbbc7b:      	imulq	%r13, %rax
 3bbbc7f:      	addq	%r8, %rax
 3bbbc82:      	addq	%rsi, %rax
 3bbbc85:      	xorq	%rax, %rdx
 3bbbc88:      	imulq	%rcx, %rdx
 3bbbc8c:      	xorq	%rdx, %rax
 3bbbc8f:      	shrq	$0x2f, %rdx
 3bbbc93:      	xorq	%rax, %rdx
 3bbbc96:      	imulq	%rcx, %rdx
 3bbbc9a:      	movq	%rdx, %rax
 3bbbc9d:      	shrq	$0x2f, %rax
 3bbbca1:      	xorq	%rdx, %rax
 3bbbca4:      	imulq	%rcx, %rax
 3bbbca8:      	popq	%rbx
 3bbbca9:      	popq	%r12
 3bbbcab:      	popq	%r13
 3bbbcad:      	popq	%r14
 3bbbcaf:      	popq	%r15
 3bbbcb1:      	popq	%rbp
 3bbbcb2:      	retq
