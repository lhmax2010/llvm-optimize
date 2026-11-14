
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002febeb0 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_>:
 2febeb0:      	movq	%rsi, %rcx
 2febeb3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 2febebd:      	subq	%rdi, %rsi
 2febec0:      	cmpq	$0x40, %rsi
 2febec4:      	ja	0x2febed4 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x24>
 2febec6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 2febecc:      	movq	%rax, %rdx
 2febecf:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 2febed4:      	pushq	%rbp
 2febed5:      	pushq	%r15
 2febed7:      	pushq	%r14
 2febed9:      	pushq	%r13
 2febedb:      	pushq	%r12
 2febedd:      	pushq	%rbx
 2febede:      	movq	%rcx, -0x18(%rsp)
 2febee3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 2febeed:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 2febef7:      	movq	%rsi, -0x10(%rsp)
 2febefc:      	movq	%rsi, %r14
 2febeff:      	andq	$-0x40, %r14
 2febf03:      	movq	0x8(%rdi), %r13
 2febf07:      	movq	0x10(%rdi), %rcx
 2febf0b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 2febf15:      	addq	%r13, %rdx
 2febf18:      	rolq	$0x1b, %rdx
 2febf1c:      	imulq	%r9, %rdx
 2febf20:      	movq	0x30(%rdi), %rsi
 2febf24:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 2febf2e:      	addq	%rsi, %r10
 2febf31:      	rolq	$0x16, %r10
 2febf35:      	imulq	%r9, %r10
 2febf39:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 2febf43:      	xorq	%rdx, %rbp
 2febf46:      	movq	0x28(%rdi), %r12
 2febf4a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 2febf54:      	addq	%r12, %r9
 2febf57:      	addq	%r10, %r9
 2febf5a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 2febf64:      	addq	(%rdi), %r10
 2febf67:      	movq	0x18(%rdi), %r11
 2febf6b:      	addq	%r10, %rax
 2febf6e:      	addq	%r11, %rax
 2febf71:      	addq	%rbp, %rax
 2febf74:      	rolq	$0x2b, %rax
 2febf78:      	addq	%rcx, %r13
 2febf7b:      	addq	%r10, %r13
 2febf7e:      	movq	%r13, %rdx
 2febf81:      	rolq	$0x14, %rdx
 2febf85:      	addq	%r10, %rdx
 2febf88:      	addq	%rax, %rdx
 2febf8b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 2febf95:      	addq	0x20(%rdi), %rax
 2febf99:      	addq	%r11, %r13
 2febf9c:      	movq	0x38(%rdi), %r10
 2febfa0:      	addq	%rax, %rcx
 2febfa3:      	addq	%r10, %rcx
 2febfa6:      	addq	%r9, %rcx
 2febfa9:      	rolq	$0x2b, %rcx
 2febfad:      	addq	%rsi, %r12
 2febfb0:      	addq	%rax, %r12
 2febfb3:      	movq	%r12, %rbx
 2febfb6:      	rolq	$0x14, %rbx
 2febfba:      	addq	%rax, %rbx
 2febfbd:      	addq	%rcx, %rbx
 2febfc0:      	addq	%r10, %r12
 2febfc3:      	movq	%r14, -0x20(%rsp)
 2febfc8:      	cmpq	$0x40, %r14
 2febfcc:      	jne	0x2febfe2 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x132>
 2febfce:      	movq	%rbx, %rsi
 2febfd1:      	movq	%r12, %r11
 2febfd4:      	movq	%rdx, %rax
 2febfd7:      	movq	%r13, %r14
 2febfda:      	movq	%rbp, %r15
 2febfdd:      	jmp	0x2fec0cd <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x21d>
 2febfe2:      	addq	$-0x40, -0x20(%rsp)
 2febfe8:      	xorl	%ecx, %ecx
 2febfea:      	nopw	(%rax,%rax)
 2febff0:      	addq	%r9, %r8
 2febff3:      	addq	%r13, %r8
 2febff6:      	movq	0x48(%rdi,%rcx), %r14
 2febffb:      	movq	0x50(%rdi,%rcx), %r10
 2fec000:      	addq	%r14, %r8
 2fec003:      	rolq	$0x1b, %r8
 2fec007:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 2fec011:      	imulq	%rsi, %r8
 2fec015:      	addq	%rdx, %r9
 2fec018:      	movq	0x70(%rdi,%rcx), %rax
 2fec01d:      	movq	%rax, -0x8(%rsp)
 2fec022:      	addq	%rax, %r9
 2fec025:      	rolq	$0x16, %r9
 2fec029:      	imulq	%rsi, %r9
 2fec02d:      	movq	%r8, %r15
 2fec030:      	xorq	%rbx, %r15
 2fec033:      	movq	0x68(%rdi,%rcx), %r11
 2fec038:      	addq	%r11, %r13
 2fec03b:      	addq	%r12, %rbp
 2fec03e:      	rolq	$0x1f, %rbp
 2fec042:      	addq	%r13, %r9
 2fec045:      	imulq	%rsi, %rdx
 2fec049:      	addq	0x40(%rdi,%rcx), %rdx
 2fec04e:      	movq	%rbp, %r8
 2fec051:      	movq	0x58(%rdi,%rcx), %r13
 2fec056:      	addq	%rdx, %r12
 2fec059:      	addq	%r13, %r12
 2fec05c:      	addq	%r15, %r12
 2fec05f:      	rolq	$0x2b, %r12
 2fec063:      	addq	%r10, %r14
 2fec066:      	addq	%rdx, %r14
 2fec069:      	movq	%r14, %rax
 2fec06c:      	rolq	$0x14, %rax
 2fec070:      	imulq	%rsi, %r8
 2fec074:      	addq	%rdx, %rax
 2fec077:      	addq	%r12, %rax
 2fec07a:      	addq	%r8, %rbx
 2fec07d:      	addq	%r9, %r10
 2fec080:      	addq	0x60(%rdi,%rcx), %rbx
 2fec085:      	movq	0x78(%rdi,%rcx), %rdx
 2fec08a:      	addq	%rbx, %r10
 2fec08d:      	addq	%rdx, %r10
 2fec090:      	rolq	$0x2b, %r10
 2fec094:      	addq	%r13, %r14
 2fec097:      	addq	-0x8(%rsp), %r11
 2fec09c:      	addq	%rbx, %r11
 2fec09f:      	movq	%r11, %rsi
 2fec0a2:      	rolq	$0x14, %rsi
 2fec0a6:      	addq	%rbx, %rsi
 2fec0a9:      	addq	%r10, %rsi
 2fec0ac:      	addq	%rdx, %r11
 2fec0af:      	addq	$0x40, %rcx
 2fec0b3:      	movq	%r15, %rbp
 2fec0b6:      	movq	%r14, %r13
 2fec0b9:      	movq	%rax, %rdx
 2fec0bc:      	movq	%r11, %r12
 2fec0bf:      	movq	%rsi, %rbx
 2fec0c2:      	cmpq	%rcx, -0x20(%rsp)
 2fec0c7:      	jne	0x2febff0 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x140>
 2fec0cd:      	movq	-0x10(%rsp), %r12
 2fec0d2:      	testb	$0x3f, %r12b
 2fec0d6:      	je	0x2fec1a3 <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2f3>
 2fec0dc:      	leaq	(%r9,%r14), %rdi
 2fec0e0:      	movq	-0x18(%rsp), %rbp
 2fec0e5:      	movq	-0x38(%rbp), %rcx
 2fec0e9:      	movq	-0x30(%rbp), %rdx
 2fec0ed:      	addq	%rcx, %r8
 2fec0f0:      	addq	%rdi, %r8
 2fec0f3:      	rolq	$0x1b, %r8
 2fec0f7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 2fec101:      	imulq	%r13, %r8
 2fec105:      	addq	%rax, %r9
 2fec108:      	movq	-0x10(%rbp), %r10
 2fec10c:      	addq	%r10, %r9
 2fec10f:      	rolq	$0x16, %r9
 2fec113:      	imulq	%r13, %r9
 2fec117:      	xorq	%rsi, %r8
 2fec11a:      	movq	-0x18(%rbp), %rdi
 2fec11e:      	addq	%rdi, %r14
 2fec121:      	addq	%r14, %r9
 2fec124:      	addq	%r11, %r15
 2fec127:      	rolq	$0x1f, %r15
 2fec12b:      	movq	%r15, %rbx
 2fec12e:      	imulq	%r13, %rax
 2fec132:      	addq	%r8, %r11
 2fec135:      	addq	-0x40(%rbp), %rax
 2fec139:      	movq	-0x28(%rbp), %r15
 2fec13d:      	addq	%r15, %r11
 2fec140:      	addq	%rax, %r11
 2fec143:      	rolq	$0x2b, %r11
 2fec147:      	imulq	%r13, %rbx
 2fec14b:      	addq	%rdx, %rcx
 2fec14e:      	addq	%rax, %rcx
 2fec151:      	movq	%rcx, %r14
 2fec154:      	rolq	$0x14, %r14
 2fec158:      	addq	%rax, %r14
 2fec15b:      	addq	%r11, %r14
 2fec15e:      	addq	%r15, %rcx
 2fec161:      	addq	%rbx, %rsi
 2fec164:      	addq	-0x20(%rbp), %rsi
 2fec168:      	addq	%r9, %rdx
 2fec16b:      	movq	-0x8(%rbp), %rax
 2fec16f:      	addq	%rax, %rdx
 2fec172:      	addq	%rsi, %rdx
 2fec175:      	rolq	$0x2b, %rdx
 2fec179:      	addq	%r10, %rdi
 2fec17c:      	addq	%rsi, %rdi
 2fec17f:      	movq	%rdi, %r10
 2fec182:      	rolq	$0x14, %r10
 2fec186:      	addq	%rsi, %r10
 2fec189:      	addq	%rdx, %r10
 2fec18c:      	addq	%rax, %rdi
 2fec18f:      	movq	%r10, %rsi
 2fec192:      	movq	%rdi, %r11
 2fec195:      	movq	%r14, %rax
 2fec198:      	movq	%rcx, %r14
 2fec19b:      	movq	%r8, %r15
 2fec19e:      	movq	%rbx, %r8
 2fec1a1:      	jmp	0x2fec1ad <_ZN4llvm7hashing6detail23hash_combine_range_implIjEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2fd>
 2fec1a3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 2fec1ad:      	xorq	%r11, %r14
 2fec1b0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 2fec1ba:      	imulq	%rcx, %r14
 2fec1be:      	xorq	%r14, %r11
 2fec1c1:      	shrq	$0x2f, %r14
 2fec1c5:      	xorq	%r11, %r14
 2fec1c8:      	imulq	%rcx, %r14
 2fec1cc:      	movq	%r14, %rdi
 2fec1cf:      	shrq	$0x2f, %rdi
 2fec1d3:      	xorq	%r14, %rdi
 2fec1d6:      	imulq	%rcx, %rdi
 2fec1da:      	movq	%r9, %rdx
 2fec1dd:      	shrq	$0x2f, %rdx
 2fec1e1:      	xorq	%r9, %rdx
 2fec1e4:      	imulq	%r13, %rdx
 2fec1e8:      	addq	%r15, %rdx
 2fec1eb:      	addq	%rdi, %rdx
 2fec1ee:      	xorq	%rsi, %rax
 2fec1f1:      	imulq	%rcx, %rax
 2fec1f5:      	xorq	%rax, %rsi
 2fec1f8:      	shrq	$0x2f, %rax
 2fec1fc:      	xorq	%rsi, %rax
 2fec1ff:      	imulq	%rcx, %rax
 2fec203:      	movq	%rax, %rsi
 2fec206:      	shrq	$0x2f, %rsi
 2fec20a:      	xorq	%rax, %rsi
 2fec20d:      	imulq	%rcx, %rsi
 2fec211:      	movq	%r12, %rax
 2fec214:      	shrq	$0x2f, %rax
 2fec218:      	xorq	%r12, %rax
 2fec21b:      	imulq	%r13, %rax
 2fec21f:      	addq	%r8, %rax
 2fec222:      	addq	%rsi, %rax
 2fec225:      	xorq	%rax, %rdx
 2fec228:      	imulq	%rcx, %rdx
 2fec22c:      	xorq	%rdx, %rax
 2fec22f:      	shrq	$0x2f, %rdx
 2fec233:      	xorq	%rax, %rdx
 2fec236:      	imulq	%rcx, %rdx
 2fec23a:      	movq	%rdx, %rax
 2fec23d:      	shrq	$0x2f, %rax
 2fec241:      	xorq	%rdx, %rax
 2fec244:      	imulq	%rcx, %rax
 2fec248:      	popq	%rbx
 2fec249:      	popq	%r12
 2fec24b:      	popq	%r13
 2fec24d:      	popq	%r14
 2fec24f:      	popq	%r15
 2fec251:      	popq	%rbp
 2fec252:      	retq
