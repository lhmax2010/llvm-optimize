
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002febe70 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_>:
 2febe70:      	movq	%rsi, %rcx
 2febe73:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 2febe7d:      	subq	%rdi, %rsi
 2febe80:      	cmpq	$0x40, %rsi
 2febe84:      	ja	0x2febe94 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x24>
 2febe86:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 2febe8c:      	movq	%rax, %rdx
 2febe8f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 2febe94:      	pushq	%rbp
 2febe95:      	pushq	%r15
 2febe97:      	pushq	%r14
 2febe99:      	pushq	%r13
 2febe9b:      	pushq	%r12
 2febe9d:      	pushq	%rbx
 2febe9e:      	movq	%rcx, -0x18(%rsp)
 2febea3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 2febead:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 2febeb7:      	movq	%rsi, -0x10(%rsp)
 2febebc:      	movq	%rsi, %r14
 2febebf:      	andq	$-0x40, %r14
 2febec3:      	movq	0x8(%rdi), %r13
 2febec7:      	movq	0x10(%rdi), %rcx
 2febecb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 2febed5:      	addq	%r13, %rdx
 2febed8:      	rolq	$0x1b, %rdx
 2febedc:      	imulq	%r9, %rdx
 2febee0:      	movq	0x30(%rdi), %rsi
 2febee4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 2febeee:      	addq	%rsi, %r10
 2febef1:      	rolq	$0x16, %r10
 2febef5:      	imulq	%r9, %r10
 2febef9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 2febf03:      	xorq	%rdx, %rbp
 2febf06:      	movq	0x28(%rdi), %r12
 2febf0a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 2febf14:      	addq	%r12, %r9
 2febf17:      	addq	%r10, %r9
 2febf1a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 2febf24:      	addq	(%rdi), %r10
 2febf27:      	movq	0x18(%rdi), %r11
 2febf2b:      	addq	%r10, %rax
 2febf2e:      	addq	%r11, %rax
 2febf31:      	addq	%rbp, %rax
 2febf34:      	rolq	$0x2b, %rax
 2febf38:      	addq	%rcx, %r13
 2febf3b:      	addq	%r10, %r13
 2febf3e:      	movq	%r13, %rdx
 2febf41:      	rolq	$0x14, %rdx
 2febf45:      	addq	%r10, %rdx
 2febf48:      	addq	%rax, %rdx
 2febf4b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 2febf55:      	addq	0x20(%rdi), %rax
 2febf59:      	addq	%r11, %r13
 2febf5c:      	movq	0x38(%rdi), %r10
 2febf60:      	addq	%rax, %rcx
 2febf63:      	addq	%r10, %rcx
 2febf66:      	addq	%r9, %rcx
 2febf69:      	rolq	$0x2b, %rcx
 2febf6d:      	addq	%rsi, %r12
 2febf70:      	addq	%rax, %r12
 2febf73:      	movq	%r12, %rbx
 2febf76:      	rolq	$0x14, %rbx
 2febf7a:      	addq	%rax, %rbx
 2febf7d:      	addq	%rcx, %rbx
 2febf80:      	addq	%r10, %r12
 2febf83:      	movq	%r14, -0x20(%rsp)
 2febf88:      	cmpq	$0x40, %r14
 2febf8c:      	jne	0x2febfa2 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x132>
 2febf8e:      	movq	%rbx, %rsi
 2febf91:      	movq	%r12, %r11
 2febf94:      	movq	%rdx, %rax
 2febf97:      	movq	%r13, %r14
 2febf9a:      	movq	%rbp, %r15
 2febf9d:      	jmp	0x2fec08d <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x21d>
 2febfa2:      	addq	$-0x40, -0x20(%rsp)
 2febfa8:      	xorl	%ecx, %ecx
 2febfaa:      	nopw	(%rax,%rax)
 2febfb0:      	addq	%r9, %r8
 2febfb3:      	addq	%r13, %r8
 2febfb6:      	movq	0x48(%rdi,%rcx), %r14
 2febfbb:      	movq	0x50(%rdi,%rcx), %r10
 2febfc0:      	addq	%r14, %r8
 2febfc3:      	rolq	$0x1b, %r8
 2febfc7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 2febfd1:      	imulq	%rsi, %r8
 2febfd5:      	addq	%rdx, %r9
 2febfd8:      	movq	0x70(%rdi,%rcx), %rax
 2febfdd:      	movq	%rax, -0x8(%rsp)
 2febfe2:      	addq	%rax, %r9
 2febfe5:      	rolq	$0x16, %r9
 2febfe9:      	imulq	%rsi, %r9
 2febfed:      	movq	%r8, %r15
 2febff0:      	xorq	%rbx, %r15
 2febff3:      	movq	0x68(%rdi,%rcx), %r11
 2febff8:      	addq	%r11, %r13
 2febffb:      	addq	%r12, %rbp
 2febffe:      	rolq	$0x1f, %rbp
 2fec002:      	addq	%r13, %r9
 2fec005:      	imulq	%rsi, %rdx
 2fec009:      	addq	0x40(%rdi,%rcx), %rdx
 2fec00e:      	movq	%rbp, %r8
 2fec011:      	movq	0x58(%rdi,%rcx), %r13
 2fec016:      	addq	%rdx, %r12
 2fec019:      	addq	%r13, %r12
 2fec01c:      	addq	%r15, %r12
 2fec01f:      	rolq	$0x2b, %r12
 2fec023:      	addq	%r10, %r14
 2fec026:      	addq	%rdx, %r14
 2fec029:      	movq	%r14, %rax
 2fec02c:      	rolq	$0x14, %rax
 2fec030:      	imulq	%rsi, %r8
 2fec034:      	addq	%rdx, %rax
 2fec037:      	addq	%r12, %rax
 2fec03a:      	addq	%r8, %rbx
 2fec03d:      	addq	%r9, %r10
 2fec040:      	addq	0x60(%rdi,%rcx), %rbx
 2fec045:      	movq	0x78(%rdi,%rcx), %rdx
 2fec04a:      	addq	%rbx, %r10
 2fec04d:      	addq	%rdx, %r10
 2fec050:      	rolq	$0x2b, %r10
 2fec054:      	addq	%r13, %r14
 2fec057:      	addq	-0x8(%rsp), %r11
 2fec05c:      	addq	%rbx, %r11
 2fec05f:      	movq	%r11, %rsi
 2fec062:      	rolq	$0x14, %rsi
 2fec066:      	addq	%rbx, %rsi
 2fec069:      	addq	%r10, %rsi
 2fec06c:      	addq	%rdx, %r11
 2fec06f:      	addq	$0x40, %rcx
 2fec073:      	movq	%r15, %rbp
 2fec076:      	movq	%r14, %r13
 2fec079:      	movq	%rax, %rdx
 2fec07c:      	movq	%r11, %r12
 2fec07f:      	movq	%rsi, %rbx
 2fec082:      	cmpq	%rcx, -0x20(%rsp)
 2fec087:      	jne	0x2febfb0 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x140>
 2fec08d:      	movq	-0x10(%rsp), %r12
 2fec092:      	testb	$0x3f, %r12b
 2fec096:      	je	0x2fec162 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2f2>
 2fec09c:      	movq	-0x18(%rsp), %rbp
 2fec0a1:      	movq	-0x38(%rbp), %rcx
 2fec0a5:      	movq	-0x30(%rbp), %rdx
 2fec0a9:      	addq	%rcx, %r8
 2fec0ac:      	addq	%r9, %r8
 2fec0af:      	addq	%r14, %r8
 2fec0b2:      	rolq	$0x1b, %r8
 2fec0b6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 2fec0c0:      	imulq	%r13, %r8
 2fec0c4:      	addq	%rax, %r9
 2fec0c7:      	movq	-0x10(%rbp), %r10
 2fec0cb:      	addq	%r10, %r9
 2fec0ce:      	rolq	$0x16, %r9
 2fec0d2:      	imulq	%r13, %r9
 2fec0d6:      	xorq	%rsi, %r8
 2fec0d9:      	movq	-0x18(%rbp), %rdi
 2fec0dd:      	addq	%rdi, %r14
 2fec0e0:      	addq	%r14, %r9
 2fec0e3:      	addq	%r11, %r15
 2fec0e6:      	rolq	$0x1f, %r15
 2fec0ea:      	movq	%r15, %rbx
 2fec0ed:      	imulq	%r13, %rax
 2fec0f1:      	addq	%r8, %r11
 2fec0f4:      	addq	-0x40(%rbp), %rax
 2fec0f8:      	movq	-0x28(%rbp), %r15
 2fec0fc:      	addq	%r15, %r11
 2fec0ff:      	addq	%rax, %r11
 2fec102:      	rolq	$0x2b, %r11
 2fec106:      	imulq	%r13, %rbx
 2fec10a:      	addq	%rdx, %rcx
 2fec10d:      	addq	%rax, %rcx
 2fec110:      	movq	%rcx, %r14
 2fec113:      	rolq	$0x14, %r14
 2fec117:      	addq	%rax, %r14
 2fec11a:      	addq	%r11, %r14
 2fec11d:      	addq	%r15, %rcx
 2fec120:      	addq	%rbx, %rsi
 2fec123:      	addq	-0x20(%rbp), %rsi
 2fec127:      	addq	%r9, %rdx
 2fec12a:      	movq	-0x8(%rbp), %rax
 2fec12e:      	addq	%rax, %rdx
 2fec131:      	addq	%rsi, %rdx
 2fec134:      	rolq	$0x2b, %rdx
 2fec138:      	addq	%r10, %rdi
 2fec13b:      	addq	%rsi, %rdi
 2fec13e:      	movq	%rdi, %r10
 2fec141:      	rolq	$0x14, %r10
 2fec145:      	addq	%rsi, %r10
 2fec148:      	addq	%rdx, %r10
 2fec14b:      	addq	%rax, %rdi
 2fec14e:      	movq	%r10, %rsi
 2fec151:      	movq	%rdi, %r11
 2fec154:      	movq	%r14, %rax
 2fec157:      	movq	%rcx, %r14
 2fec15a:      	movq	%r8, %r15
 2fec15d:      	movq	%rbx, %r8
 2fec160:      	jmp	0x2fec16c <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2fc>
 2fec162:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 2fec16c:      	xorq	%r11, %r14
 2fec16f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 2fec179:      	imulq	%rcx, %r14
 2fec17d:      	xorq	%r14, %r11
 2fec180:      	shrq	$0x2f, %r14
 2fec184:      	xorq	%r11, %r14
 2fec187:      	imulq	%rcx, %r14
 2fec18b:      	movq	%r14, %rdi
 2fec18e:      	shrq	$0x2f, %rdi
 2fec192:      	xorq	%r14, %rdi
 2fec195:      	imulq	%rcx, %rdi
 2fec199:      	movq	%r9, %rdx
 2fec19c:      	shrq	$0x2f, %rdx
 2fec1a0:      	xorq	%r9, %rdx
 2fec1a3:      	imulq	%r13, %rdx
 2fec1a7:      	addq	%r15, %rdx
 2fec1aa:      	addq	%rdi, %rdx
 2fec1ad:      	xorq	%rsi, %rax
 2fec1b0:      	imulq	%rcx, %rax
 2fec1b4:      	xorq	%rax, %rsi
 2fec1b7:      	shrq	$0x2f, %rax
 2fec1bb:      	xorq	%rsi, %rax
 2fec1be:      	imulq	%rcx, %rax
 2fec1c2:      	movq	%rax, %rsi
 2fec1c5:      	shrq	$0x2f, %rsi
 2fec1c9:      	xorq	%rax, %rsi
 2fec1cc:      	imulq	%rcx, %rsi
 2fec1d0:      	movq	%r12, %rax
 2fec1d3:      	shrq	$0x2f, %rax
 2fec1d7:      	xorq	%r12, %rax
 2fec1da:      	imulq	%r13, %rax
 2fec1de:      	addq	%r8, %rax
 2fec1e1:      	addq	%rsi, %rax
 2fec1e4:      	xorq	%rax, %rdx
 2fec1e7:      	imulq	%rcx, %rdx
 2fec1eb:      	xorq	%rdx, %rax
 2fec1ee:      	shrq	$0x2f, %rdx
 2fec1f2:      	xorq	%rax, %rdx
 2fec1f5:      	imulq	%rcx, %rdx
 2fec1f9:      	movq	%rdx, %rax
 2fec1fc:      	shrq	$0x2f, %rax
 2fec200:      	xorq	%rdx, %rax
 2fec203:      	imulq	%rcx, %rax
 2fec207:      	popq	%rbx
 2fec208:      	popq	%r12
 2fec20a:      	popq	%r13
 2fec20c:      	popq	%r14
 2fec20e:      	popq	%r15
 2fec210:      	popq	%rbp
 2fec211:      	retq
