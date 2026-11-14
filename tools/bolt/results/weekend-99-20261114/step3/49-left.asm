
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000037cedc0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 37cedc0:      	movq	%rsi, %rcx
 37cedc3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 37cedcd:      	subq	%rdi, %rsi
 37cedd0:      	cmpq	$0x40, %rsi
 37cedd4:      	ja	0x37cede4 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 37cedd6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 37ceddc:      	movq	%rax, %rdx
 37ceddf:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 37cede4:      	pushq	%rbp
 37cede5:      	pushq	%r15
 37cede7:      	pushq	%r14
 37cede9:      	pushq	%r13
 37cedeb:      	pushq	%r12
 37ceded:      	pushq	%rbx
 37cedee:      	movq	%rcx, -0x18(%rsp)
 37cedf3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 37cedfd:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 37cee07:      	movq	%rsi, -0x10(%rsp)
 37cee0c:      	movq	%rsi, %r14
 37cee0f:      	andq	$-0x40, %r14
 37cee13:      	movq	0x8(%rdi), %r13
 37cee17:      	movq	0x10(%rdi), %rcx
 37cee1b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 37cee25:      	addq	%r13, %rdx
 37cee28:      	rolq	$0x1b, %rdx
 37cee2c:      	imulq	%r9, %rdx
 37cee30:      	movq	0x30(%rdi), %rsi
 37cee34:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 37cee3e:      	addq	%rsi, %r10
 37cee41:      	rolq	$0x16, %r10
 37cee45:      	imulq	%r9, %r10
 37cee49:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 37cee53:      	xorq	%rdx, %rbp
 37cee56:      	movq	0x28(%rdi), %r12
 37cee5a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 37cee64:      	addq	%r12, %r9
 37cee67:      	addq	%r10, %r9
 37cee6a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 37cee74:      	addq	(%rdi), %r10
 37cee77:      	movq	0x18(%rdi), %r11
 37cee7b:      	addq	%r10, %rax
 37cee7e:      	addq	%r11, %rax
 37cee81:      	addq	%rbp, %rax
 37cee84:      	rolq	$0x2b, %rax
 37cee88:      	addq	%rcx, %r13
 37cee8b:      	addq	%r10, %r13
 37cee8e:      	movq	%r13, %rdx
 37cee91:      	rolq	$0x14, %rdx
 37cee95:      	addq	%r10, %rdx
 37cee98:      	addq	%rax, %rdx
 37cee9b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 37ceea5:      	addq	0x20(%rdi), %rax
 37ceea9:      	addq	%r11, %r13
 37ceeac:      	movq	0x38(%rdi), %r10
 37ceeb0:      	addq	%rax, %rcx
 37ceeb3:      	addq	%r10, %rcx
 37ceeb6:      	addq	%r9, %rcx
 37ceeb9:      	rolq	$0x2b, %rcx
 37ceebd:      	addq	%rsi, %r12
 37ceec0:      	addq	%rax, %r12
 37ceec3:      	movq	%r12, %rbx
 37ceec6:      	rolq	$0x14, %rbx
 37ceeca:      	addq	%rax, %rbx
 37ceecd:      	addq	%rcx, %rbx
 37ceed0:      	addq	%r10, %r12
 37ceed3:      	movq	%r14, -0x20(%rsp)
 37ceed8:      	cmpq	$0x40, %r14
 37ceedc:      	jne	0x37ceef2 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 37ceede:      	movq	%rbx, %rsi
 37ceee1:      	movq	%r12, %r11
 37ceee4:      	movq	%rdx, %rax
 37ceee7:      	movq	%r13, %r14
 37ceeea:      	movq	%rbp, %r15
 37ceeed:      	jmp	0x37cefdd <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 37ceef2:      	addq	$-0x40, -0x20(%rsp)
 37ceef8:      	xorl	%ecx, %ecx
 37ceefa:      	nopw	(%rax,%rax)
 37cef00:      	addq	%r9, %r8
 37cef03:      	addq	%r13, %r8
 37cef06:      	movq	0x48(%rdi,%rcx), %r14
 37cef0b:      	movq	0x50(%rdi,%rcx), %r10
 37cef10:      	addq	%r14, %r8
 37cef13:      	rolq	$0x1b, %r8
 37cef17:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 37cef21:      	imulq	%rsi, %r8
 37cef25:      	addq	%rdx, %r9
 37cef28:      	movq	0x70(%rdi,%rcx), %rax
 37cef2d:      	movq	%rax, -0x8(%rsp)
 37cef32:      	addq	%rax, %r9
 37cef35:      	rolq	$0x16, %r9
 37cef39:      	imulq	%rsi, %r9
 37cef3d:      	movq	%r8, %r15
 37cef40:      	xorq	%rbx, %r15
 37cef43:      	movq	0x68(%rdi,%rcx), %r11
 37cef48:      	addq	%r11, %r13
 37cef4b:      	addq	%r12, %rbp
 37cef4e:      	rolq	$0x1f, %rbp
 37cef52:      	addq	%r13, %r9
 37cef55:      	imulq	%rsi, %rdx
 37cef59:      	addq	0x40(%rdi,%rcx), %rdx
 37cef5e:      	movq	%rbp, %r8
 37cef61:      	movq	0x58(%rdi,%rcx), %r13
 37cef66:      	addq	%rdx, %r12
 37cef69:      	addq	%r13, %r12
 37cef6c:      	addq	%r15, %r12
 37cef6f:      	rolq	$0x2b, %r12
 37cef73:      	addq	%r10, %r14
 37cef76:      	addq	%rdx, %r14
 37cef79:      	movq	%r14, %rax
 37cef7c:      	rolq	$0x14, %rax
 37cef80:      	imulq	%rsi, %r8
 37cef84:      	addq	%rdx, %rax
 37cef87:      	addq	%r12, %rax
 37cef8a:      	addq	%r8, %rbx
 37cef8d:      	addq	%r9, %r10
 37cef90:      	addq	0x60(%rdi,%rcx), %rbx
 37cef95:      	movq	0x78(%rdi,%rcx), %rdx
 37cef9a:      	addq	%rbx, %r10
 37cef9d:      	addq	%rdx, %r10
 37cefa0:      	rolq	$0x2b, %r10
 37cefa4:      	addq	%r13, %r14
 37cefa7:      	addq	-0x8(%rsp), %r11
 37cefac:      	addq	%rbx, %r11
 37cefaf:      	movq	%r11, %rsi
 37cefb2:      	rolq	$0x14, %rsi
 37cefb6:      	addq	%rbx, %rsi
 37cefb9:      	addq	%r10, %rsi
 37cefbc:      	addq	%rdx, %r11
 37cefbf:      	addq	$0x40, %rcx
 37cefc3:      	movq	%r15, %rbp
 37cefc6:      	movq	%r14, %r13
 37cefc9:      	movq	%rax, %rdx
 37cefcc:      	movq	%r11, %r12
 37cefcf:      	movq	%rsi, %rbx
 37cefd2:      	cmpq	%rcx, -0x20(%rsp)
 37cefd7:      	jne	0x37cef00 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 37cefdd:      	movq	-0x10(%rsp), %r12
 37cefe2:      	testb	$0x3f, %r12b
 37cefe6:      	je	0x37cf0b3 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f3>
 37cefec:      	leaq	(%r9,%r14), %rdi
 37ceff0:      	movq	-0x18(%rsp), %rbp
 37ceff5:      	movq	-0x38(%rbp), %rcx
 37ceff9:      	movq	-0x30(%rbp), %rdx
 37ceffd:      	addq	%rcx, %r8
 37cf000:      	addq	%rdi, %r8
 37cf003:      	rolq	$0x1b, %r8
 37cf007:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 37cf011:      	imulq	%r13, %r8
 37cf015:      	addq	%rax, %r9
 37cf018:      	movq	-0x10(%rbp), %r10
 37cf01c:      	addq	%r10, %r9
 37cf01f:      	rolq	$0x16, %r9
 37cf023:      	imulq	%r13, %r9
 37cf027:      	xorq	%rsi, %r8
 37cf02a:      	movq	-0x18(%rbp), %rdi
 37cf02e:      	addq	%rdi, %r14
 37cf031:      	addq	%r14, %r9
 37cf034:      	addq	%r11, %r15
 37cf037:      	rolq	$0x1f, %r15
 37cf03b:      	movq	%r15, %rbx
 37cf03e:      	imulq	%r13, %rax
 37cf042:      	addq	%r8, %r11
 37cf045:      	addq	-0x40(%rbp), %rax
 37cf049:      	movq	-0x28(%rbp), %r15
 37cf04d:      	addq	%r15, %r11
 37cf050:      	addq	%rax, %r11
 37cf053:      	rolq	$0x2b, %r11
 37cf057:      	imulq	%r13, %rbx
 37cf05b:      	addq	%rdx, %rcx
 37cf05e:      	addq	%rax, %rcx
 37cf061:      	movq	%rcx, %r14
 37cf064:      	rolq	$0x14, %r14
 37cf068:      	addq	%rax, %r14
 37cf06b:      	addq	%r11, %r14
 37cf06e:      	addq	%r15, %rcx
 37cf071:      	addq	%rbx, %rsi
 37cf074:      	addq	-0x20(%rbp), %rsi
 37cf078:      	addq	%r9, %rdx
 37cf07b:      	movq	-0x8(%rbp), %rax
 37cf07f:      	addq	%rax, %rdx
 37cf082:      	addq	%rsi, %rdx
 37cf085:      	rolq	$0x2b, %rdx
 37cf089:      	addq	%r10, %rdi
 37cf08c:      	addq	%rsi, %rdi
 37cf08f:      	movq	%rdi, %r10
 37cf092:      	rolq	$0x14, %r10
 37cf096:      	addq	%rsi, %r10
 37cf099:      	addq	%rdx, %r10
 37cf09c:      	addq	%rax, %rdi
 37cf09f:      	movq	%r10, %rsi
 37cf0a2:      	movq	%rdi, %r11
 37cf0a5:      	movq	%r14, %rax
 37cf0a8:      	movq	%rcx, %r14
 37cf0ab:      	movq	%r8, %r15
 37cf0ae:      	movq	%rbx, %r8
 37cf0b1:      	jmp	0x37cf0bd <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fd>
 37cf0b3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 37cf0bd:      	xorq	%r11, %r14
 37cf0c0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 37cf0ca:      	imulq	%rcx, %r14
 37cf0ce:      	xorq	%r14, %r11
 37cf0d1:      	shrq	$0x2f, %r14
 37cf0d5:      	xorq	%r11, %r14
 37cf0d8:      	imulq	%rcx, %r14
 37cf0dc:      	movq	%r14, %rdi
 37cf0df:      	shrq	$0x2f, %rdi
 37cf0e3:      	xorq	%r14, %rdi
 37cf0e6:      	imulq	%rcx, %rdi
 37cf0ea:      	movq	%r9, %rdx
 37cf0ed:      	shrq	$0x2f, %rdx
 37cf0f1:      	xorq	%r9, %rdx
 37cf0f4:      	imulq	%r13, %rdx
 37cf0f8:      	addq	%r15, %rdx
 37cf0fb:      	addq	%rdi, %rdx
 37cf0fe:      	xorq	%rsi, %rax
 37cf101:      	imulq	%rcx, %rax
 37cf105:      	xorq	%rax, %rsi
 37cf108:      	shrq	$0x2f, %rax
 37cf10c:      	xorq	%rsi, %rax
 37cf10f:      	imulq	%rcx, %rax
 37cf113:      	movq	%rax, %rsi
 37cf116:      	shrq	$0x2f, %rsi
 37cf11a:      	xorq	%rax, %rsi
 37cf11d:      	imulq	%rcx, %rsi
 37cf121:      	movq	%r12, %rax
 37cf124:      	shrq	$0x2f, %rax
 37cf128:      	xorq	%r12, %rax
 37cf12b:      	imulq	%r13, %rax
 37cf12f:      	addq	%r8, %rax
 37cf132:      	addq	%rsi, %rax
 37cf135:      	xorq	%rax, %rdx
 37cf138:      	imulq	%rcx, %rdx
 37cf13c:      	xorq	%rdx, %rax
 37cf13f:      	shrq	$0x2f, %rdx
 37cf143:      	xorq	%rax, %rdx
 37cf146:      	imulq	%rcx, %rdx
 37cf14a:      	movq	%rdx, %rax
 37cf14d:      	shrq	$0x2f, %rax
 37cf151:      	xorq	%rdx, %rax
 37cf154:      	imulq	%rcx, %rax
 37cf158:      	popq	%rbx
 37cf159:      	popq	%r12
 37cf15b:      	popq	%r13
 37cf15d:      	popq	%r14
 37cf15f:      	popq	%r15
 37cf161:      	popq	%rbp
 37cf162:      	retq
