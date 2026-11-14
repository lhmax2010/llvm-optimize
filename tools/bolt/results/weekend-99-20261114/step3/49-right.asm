
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000037ced30 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_>:
 37ced30:      	movq	%rsi, %rcx
 37ced33:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 37ced3d:      	subq	%rdi, %rsi
 37ced40:      	cmpq	$0x40, %rsi
 37ced44:      	ja	0x37ced54 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x24>
 37ced46:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 37ced4c:      	movq	%rax, %rdx
 37ced4f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 37ced54:      	pushq	%rbp
 37ced55:      	pushq	%r15
 37ced57:      	pushq	%r14
 37ced59:      	pushq	%r13
 37ced5b:      	pushq	%r12
 37ced5d:      	pushq	%rbx
 37ced5e:      	movq	%rcx, -0x18(%rsp)
 37ced63:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 37ced6d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 37ced77:      	movq	%rsi, -0x10(%rsp)
 37ced7c:      	movq	%rsi, %r14
 37ced7f:      	andq	$-0x40, %r14
 37ced83:      	movq	0x8(%rdi), %r13
 37ced87:      	movq	0x10(%rdi), %rcx
 37ced8b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 37ced95:      	addq	%r13, %rdx
 37ced98:      	rolq	$0x1b, %rdx
 37ced9c:      	imulq	%r9, %rdx
 37ceda0:      	movq	0x30(%rdi), %rsi
 37ceda4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 37cedae:      	addq	%rsi, %r10
 37cedb1:      	rolq	$0x16, %r10
 37cedb5:      	imulq	%r9, %r10
 37cedb9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 37cedc3:      	xorq	%rdx, %rbp
 37cedc6:      	movq	0x28(%rdi), %r12
 37cedca:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 37cedd4:      	addq	%r12, %r9
 37cedd7:      	addq	%r10, %r9
 37cedda:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 37cede4:      	addq	(%rdi), %r10
 37cede7:      	movq	0x18(%rdi), %r11
 37cedeb:      	addq	%r10, %rax
 37cedee:      	addq	%r11, %rax
 37cedf1:      	addq	%rbp, %rax
 37cedf4:      	rolq	$0x2b, %rax
 37cedf8:      	addq	%rcx, %r13
 37cedfb:      	addq	%r10, %r13
 37cedfe:      	movq	%r13, %rdx
 37cee01:      	rolq	$0x14, %rdx
 37cee05:      	addq	%r10, %rdx
 37cee08:      	addq	%rax, %rdx
 37cee0b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 37cee15:      	addq	0x20(%rdi), %rax
 37cee19:      	addq	%r11, %r13
 37cee1c:      	movq	0x38(%rdi), %r10
 37cee20:      	addq	%rax, %rcx
 37cee23:      	addq	%r10, %rcx
 37cee26:      	addq	%r9, %rcx
 37cee29:      	rolq	$0x2b, %rcx
 37cee2d:      	addq	%rsi, %r12
 37cee30:      	addq	%rax, %r12
 37cee33:      	movq	%r12, %rbx
 37cee36:      	rolq	$0x14, %rbx
 37cee3a:      	addq	%rax, %rbx
 37cee3d:      	addq	%rcx, %rbx
 37cee40:      	addq	%r10, %r12
 37cee43:      	movq	%r14, -0x20(%rsp)
 37cee48:      	cmpq	$0x40, %r14
 37cee4c:      	jne	0x37cee62 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x132>
 37cee4e:      	movq	%rbx, %rsi
 37cee51:      	movq	%r12, %r11
 37cee54:      	movq	%rdx, %rax
 37cee57:      	movq	%r13, %r14
 37cee5a:      	movq	%rbp, %r15
 37cee5d:      	jmp	0x37cef4d <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x21d>
 37cee62:      	addq	$-0x40, -0x20(%rsp)
 37cee68:      	xorl	%ecx, %ecx
 37cee6a:      	nopw	(%rax,%rax)
 37cee70:      	addq	%r9, %r8
 37cee73:      	addq	%r13, %r8
 37cee76:      	movq	0x48(%rdi,%rcx), %r14
 37cee7b:      	movq	0x50(%rdi,%rcx), %r10
 37cee80:      	addq	%r14, %r8
 37cee83:      	rolq	$0x1b, %r8
 37cee87:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 37cee91:      	imulq	%rsi, %r8
 37cee95:      	addq	%rdx, %r9
 37cee98:      	movq	0x70(%rdi,%rcx), %rax
 37cee9d:      	movq	%rax, -0x8(%rsp)
 37ceea2:      	addq	%rax, %r9
 37ceea5:      	rolq	$0x16, %r9
 37ceea9:      	imulq	%rsi, %r9
 37ceead:      	movq	%r8, %r15
 37ceeb0:      	xorq	%rbx, %r15
 37ceeb3:      	movq	0x68(%rdi,%rcx), %r11
 37ceeb8:      	addq	%r11, %r13
 37ceebb:      	addq	%r12, %rbp
 37ceebe:      	rolq	$0x1f, %rbp
 37ceec2:      	addq	%r13, %r9
 37ceec5:      	imulq	%rsi, %rdx
 37ceec9:      	addq	0x40(%rdi,%rcx), %rdx
 37ceece:      	movq	%rbp, %r8
 37ceed1:      	movq	0x58(%rdi,%rcx), %r13
 37ceed6:      	addq	%rdx, %r12
 37ceed9:      	addq	%r13, %r12
 37ceedc:      	addq	%r15, %r12
 37ceedf:      	rolq	$0x2b, %r12
 37ceee3:      	addq	%r10, %r14
 37ceee6:      	addq	%rdx, %r14
 37ceee9:      	movq	%r14, %rax
 37ceeec:      	rolq	$0x14, %rax
 37ceef0:      	imulq	%rsi, %r8
 37ceef4:      	addq	%rdx, %rax
 37ceef7:      	addq	%r12, %rax
 37ceefa:      	addq	%r8, %rbx
 37ceefd:      	addq	%r9, %r10
 37cef00:      	addq	0x60(%rdi,%rcx), %rbx
 37cef05:      	movq	0x78(%rdi,%rcx), %rdx
 37cef0a:      	addq	%rbx, %r10
 37cef0d:      	addq	%rdx, %r10
 37cef10:      	rolq	$0x2b, %r10
 37cef14:      	addq	%r13, %r14
 37cef17:      	addq	-0x8(%rsp), %r11
 37cef1c:      	addq	%rbx, %r11
 37cef1f:      	movq	%r11, %rsi
 37cef22:      	rolq	$0x14, %rsi
 37cef26:      	addq	%rbx, %rsi
 37cef29:      	addq	%r10, %rsi
 37cef2c:      	addq	%rdx, %r11
 37cef2f:      	addq	$0x40, %rcx
 37cef33:      	movq	%r15, %rbp
 37cef36:      	movq	%r14, %r13
 37cef39:      	movq	%rax, %rdx
 37cef3c:      	movq	%r11, %r12
 37cef3f:      	movq	%rsi, %rbx
 37cef42:      	cmpq	%rcx, -0x20(%rsp)
 37cef47:      	jne	0x37cee70 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x140>
 37cef4d:      	movq	-0x10(%rsp), %r12
 37cef52:      	testb	$0x3f, %r12b
 37cef56:      	je	0x37cf022 <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2f2>
 37cef5c:      	movq	-0x18(%rsp), %rbp
 37cef61:      	movq	-0x38(%rbp), %rcx
 37cef65:      	movq	-0x30(%rbp), %rdx
 37cef69:      	addq	%rcx, %r8
 37cef6c:      	addq	%r9, %r8
 37cef6f:      	addq	%r14, %r8
 37cef72:      	rolq	$0x1b, %r8
 37cef76:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 37cef80:      	imulq	%r13, %r8
 37cef84:      	addq	%rax, %r9
 37cef87:      	movq	-0x10(%rbp), %r10
 37cef8b:      	addq	%r10, %r9
 37cef8e:      	rolq	$0x16, %r9
 37cef92:      	imulq	%r13, %r9
 37cef96:      	xorq	%rsi, %r8
 37cef99:      	movq	-0x18(%rbp), %rdi
 37cef9d:      	addq	%rdi, %r14
 37cefa0:      	addq	%r14, %r9
 37cefa3:      	addq	%r11, %r15
 37cefa6:      	rolq	$0x1f, %r15
 37cefaa:      	movq	%r15, %rbx
 37cefad:      	imulq	%r13, %rax
 37cefb1:      	addq	%r8, %r11
 37cefb4:      	addq	-0x40(%rbp), %rax
 37cefb8:      	movq	-0x28(%rbp), %r15
 37cefbc:      	addq	%r15, %r11
 37cefbf:      	addq	%rax, %r11
 37cefc2:      	rolq	$0x2b, %r11
 37cefc6:      	imulq	%r13, %rbx
 37cefca:      	addq	%rdx, %rcx
 37cefcd:      	addq	%rax, %rcx
 37cefd0:      	movq	%rcx, %r14
 37cefd3:      	rolq	$0x14, %r14
 37cefd7:      	addq	%rax, %r14
 37cefda:      	addq	%r11, %r14
 37cefdd:      	addq	%r15, %rcx
 37cefe0:      	addq	%rbx, %rsi
 37cefe3:      	addq	-0x20(%rbp), %rsi
 37cefe7:      	addq	%r9, %rdx
 37cefea:      	movq	-0x8(%rbp), %rax
 37cefee:      	addq	%rax, %rdx
 37ceff1:      	addq	%rsi, %rdx
 37ceff4:      	rolq	$0x2b, %rdx
 37ceff8:      	addq	%r10, %rdi
 37ceffb:      	addq	%rsi, %rdi
 37ceffe:      	movq	%rdi, %r10
 37cf001:      	rolq	$0x14, %r10
 37cf005:      	addq	%rsi, %r10
 37cf008:      	addq	%rdx, %r10
 37cf00b:      	addq	%rax, %rdi
 37cf00e:      	movq	%r10, %rsi
 37cf011:      	movq	%rdi, %r11
 37cf014:      	movq	%r14, %rax
 37cf017:      	movq	%rcx, %r14
 37cf01a:      	movq	%r8, %r15
 37cf01d:      	movq	%rbx, %r8
 37cf020:      	jmp	0x37cf02c <_ZN4llvm7hashing6detail23hash_combine_range_implIKmEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS5_S9_+0x2fc>
 37cf022:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 37cf02c:      	xorq	%r11, %r14
 37cf02f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 37cf039:      	imulq	%rcx, %r14
 37cf03d:      	xorq	%r14, %r11
 37cf040:      	shrq	$0x2f, %r14
 37cf044:      	xorq	%r11, %r14
 37cf047:      	imulq	%rcx, %r14
 37cf04b:      	movq	%r14, %rdi
 37cf04e:      	shrq	$0x2f, %rdi
 37cf052:      	xorq	%r14, %rdi
 37cf055:      	imulq	%rcx, %rdi
 37cf059:      	movq	%r9, %rdx
 37cf05c:      	shrq	$0x2f, %rdx
 37cf060:      	xorq	%r9, %rdx
 37cf063:      	imulq	%r13, %rdx
 37cf067:      	addq	%r15, %rdx
 37cf06a:      	addq	%rdi, %rdx
 37cf06d:      	xorq	%rsi, %rax
 37cf070:      	imulq	%rcx, %rax
 37cf074:      	xorq	%rax, %rsi
 37cf077:      	shrq	$0x2f, %rax
 37cf07b:      	xorq	%rsi, %rax
 37cf07e:      	imulq	%rcx, %rax
 37cf082:      	movq	%rax, %rsi
 37cf085:      	shrq	$0x2f, %rsi
 37cf089:      	xorq	%rax, %rsi
 37cf08c:      	imulq	%rcx, %rsi
 37cf090:      	movq	%r12, %rax
 37cf093:      	shrq	$0x2f, %rax
 37cf097:      	xorq	%r12, %rax
 37cf09a:      	imulq	%r13, %rax
 37cf09e:      	addq	%r8, %rax
 37cf0a1:      	addq	%rsi, %rax
 37cf0a4:      	xorq	%rax, %rdx
 37cf0a7:      	imulq	%rcx, %rdx
 37cf0ab:      	xorq	%rdx, %rax
 37cf0ae:      	shrq	$0x2f, %rdx
 37cf0b2:      	xorq	%rax, %rdx
 37cf0b5:      	imulq	%rcx, %rdx
 37cf0b9:      	movq	%rdx, %rax
 37cf0bc:      	shrq	$0x2f, %rax
 37cf0c0:      	xorq	%rdx, %rax
 37cf0c3:      	imulq	%rcx, %rax
 37cf0c7:      	popq	%rbx
 37cf0c8:      	popq	%r12
 37cf0ca:      	popq	%r13
 37cf0cc:      	popq	%r14
 37cf0ce:      	popq	%r15
 37cf0d0:      	popq	%rbp
 37cf0d1:      	retq
