
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003fa6060 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_>:
 3fa6060:      	movq	%rsi, %rcx
 3fa6063:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3fa606d:      	subq	%rdi, %rsi
 3fa6070:      	cmpq	$0x40, %rsi
 3fa6074:      	ja	0x3fa6084 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x24>
 3fa6076:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3fa607c:      	movq	%rax, %rdx
 3fa607f:      	jmp	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3fa6084:      	pushq	%rbp
 3fa6085:      	pushq	%r15
 3fa6087:      	pushq	%r14
 3fa6089:      	pushq	%r13
 3fa608b:      	pushq	%r12
 3fa608d:      	pushq	%rbx
 3fa608e:      	movq	%rcx, -0x18(%rsp)
 3fa6093:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3fa609d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3fa60a7:      	movq	%rsi, -0x10(%rsp)
 3fa60ac:      	movq	%rsi, %r14
 3fa60af:      	andq	$-0x40, %r14
 3fa60b3:      	movq	0x8(%rdi), %r13
 3fa60b7:      	movq	0x10(%rdi), %rcx
 3fa60bb:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3fa60c5:      	addq	%r13, %rdx
 3fa60c8:      	rolq	$0x1b, %rdx
 3fa60cc:      	imulq	%r9, %rdx
 3fa60d0:      	movq	0x30(%rdi), %rsi
 3fa60d4:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3fa60de:      	addq	%rsi, %r10
 3fa60e1:      	rolq	$0x16, %r10
 3fa60e5:      	imulq	%r9, %r10
 3fa60e9:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3fa60f3:      	xorq	%rdx, %rbp
 3fa60f6:      	movq	0x28(%rdi), %r12
 3fa60fa:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3fa6104:      	addq	%r12, %r9
 3fa6107:      	addq	%r10, %r9
 3fa610a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3fa6114:      	addq	(%rdi), %r10
 3fa6117:      	movq	0x18(%rdi), %r11
 3fa611b:      	addq	%r10, %rax
 3fa611e:      	addq	%r11, %rax
 3fa6121:      	addq	%rbp, %rax
 3fa6124:      	rolq	$0x2b, %rax
 3fa6128:      	addq	%rcx, %r13
 3fa612b:      	addq	%r10, %r13
 3fa612e:      	movq	%r13, %rdx
 3fa6131:      	rolq	$0x14, %rdx
 3fa6135:      	addq	%r10, %rdx
 3fa6138:      	addq	%rax, %rdx
 3fa613b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3fa6145:      	addq	0x20(%rdi), %rax
 3fa6149:      	addq	%r11, %r13
 3fa614c:      	movq	0x38(%rdi), %r10
 3fa6150:      	addq	%rax, %rcx
 3fa6153:      	addq	%r10, %rcx
 3fa6156:      	addq	%r9, %rcx
 3fa6159:      	rolq	$0x2b, %rcx
 3fa615d:      	addq	%rsi, %r12
 3fa6160:      	addq	%rax, %r12
 3fa6163:      	movq	%r12, %rbx
 3fa6166:      	rolq	$0x14, %rbx
 3fa616a:      	addq	%rax, %rbx
 3fa616d:      	addq	%rcx, %rbx
 3fa6170:      	addq	%r10, %r12
 3fa6173:      	movq	%r14, -0x20(%rsp)
 3fa6178:      	cmpq	$0x40, %r14
 3fa617c:      	jne	0x3fa6192 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x132>
 3fa617e:      	movq	%rbx, %rsi
 3fa6181:      	movq	%r12, %r11
 3fa6184:      	movq	%rdx, %rax
 3fa6187:      	movq	%r13, %r14
 3fa618a:      	movq	%rbp, %r15
 3fa618d:      	jmp	0x3fa627d <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x21d>
 3fa6192:      	addq	$-0x40, -0x20(%rsp)
 3fa6198:      	xorl	%ecx, %ecx
 3fa619a:      	nopw	(%rax,%rax)
 3fa61a0:      	addq	%r9, %r8
 3fa61a3:      	addq	%r13, %r8
 3fa61a6:      	movq	0x48(%rdi,%rcx), %r14
 3fa61ab:      	movq	0x50(%rdi,%rcx), %r10
 3fa61b0:      	addq	%r14, %r8
 3fa61b3:      	rolq	$0x1b, %r8
 3fa61b7:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3fa61c1:      	imulq	%rsi, %r8
 3fa61c5:      	addq	%rdx, %r9
 3fa61c8:      	movq	0x70(%rdi,%rcx), %rax
 3fa61cd:      	movq	%rax, -0x8(%rsp)
 3fa61d2:      	addq	%rax, %r9
 3fa61d5:      	rolq	$0x16, %r9
 3fa61d9:      	imulq	%rsi, %r9
 3fa61dd:      	movq	%r8, %r15
 3fa61e0:      	xorq	%rbx, %r15
 3fa61e3:      	movq	0x68(%rdi,%rcx), %r11
 3fa61e8:      	addq	%r11, %r13
 3fa61eb:      	addq	%r12, %rbp
 3fa61ee:      	rolq	$0x1f, %rbp
 3fa61f2:      	addq	%r13, %r9
 3fa61f5:      	imulq	%rsi, %rdx
 3fa61f9:      	addq	0x40(%rdi,%rcx), %rdx
 3fa61fe:      	movq	%rbp, %r8
 3fa6201:      	movq	0x58(%rdi,%rcx), %r13
 3fa6206:      	addq	%rdx, %r12
 3fa6209:      	addq	%r13, %r12
 3fa620c:      	addq	%r15, %r12
 3fa620f:      	rolq	$0x2b, %r12
 3fa6213:      	addq	%r10, %r14
 3fa6216:      	addq	%rdx, %r14
 3fa6219:      	movq	%r14, %rax
 3fa621c:      	rolq	$0x14, %rax
 3fa6220:      	imulq	%rsi, %r8
 3fa6224:      	addq	%rdx, %rax
 3fa6227:      	addq	%r12, %rax
 3fa622a:      	addq	%r8, %rbx
 3fa622d:      	addq	%r9, %r10
 3fa6230:      	addq	0x60(%rdi,%rcx), %rbx
 3fa6235:      	movq	0x78(%rdi,%rcx), %rdx
 3fa623a:      	addq	%rbx, %r10
 3fa623d:      	addq	%rdx, %r10
 3fa6240:      	rolq	$0x2b, %r10
 3fa6244:      	addq	%r13, %r14
 3fa6247:      	addq	-0x8(%rsp), %r11
 3fa624c:      	addq	%rbx, %r11
 3fa624f:      	movq	%r11, %rsi
 3fa6252:      	rolq	$0x14, %rsi
 3fa6256:      	addq	%rbx, %rsi
 3fa6259:      	addq	%r10, %rsi
 3fa625c:      	addq	%rdx, %r11
 3fa625f:      	addq	$0x40, %rcx
 3fa6263:      	movq	%r15, %rbp
 3fa6266:      	movq	%r14, %r13
 3fa6269:      	movq	%rax, %rdx
 3fa626c:      	movq	%r11, %r12
 3fa626f:      	movq	%rsi, %rbx
 3fa6272:      	cmpq	%rcx, -0x20(%rsp)
 3fa6277:      	jne	0x3fa61a0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x140>
 3fa627d:      	movq	-0x10(%rsp), %r12
 3fa6282:      	testb	$0x3f, %r12b
 3fa6286:      	je	0x3fa6352 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x2f2>
 3fa628c:      	movq	-0x18(%rsp), %rbp
 3fa6291:      	movq	-0x38(%rbp), %rcx
 3fa6295:      	movq	-0x30(%rbp), %rdx
 3fa6299:      	addq	%rcx, %r8
 3fa629c:      	addq	%r9, %r8
 3fa629f:      	addq	%r14, %r8
 3fa62a2:      	rolq	$0x1b, %r8
 3fa62a6:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3fa62b0:      	imulq	%r13, %r8
 3fa62b4:      	addq	%rax, %r9
 3fa62b7:      	movq	-0x10(%rbp), %r10
 3fa62bb:      	addq	%r10, %r9
 3fa62be:      	rolq	$0x16, %r9
 3fa62c2:      	imulq	%r13, %r9
 3fa62c6:      	xorq	%rsi, %r8
 3fa62c9:      	movq	-0x18(%rbp), %rdi
 3fa62cd:      	addq	%rdi, %r14
 3fa62d0:      	addq	%r14, %r9
 3fa62d3:      	addq	%r11, %r15
 3fa62d6:      	rolq	$0x1f, %r15
 3fa62da:      	movq	%r15, %rbx
 3fa62dd:      	imulq	%r13, %rax
 3fa62e1:      	addq	%r8, %r11
 3fa62e4:      	addq	-0x40(%rbp), %rax
 3fa62e8:      	movq	-0x28(%rbp), %r15
 3fa62ec:      	addq	%r15, %r11
 3fa62ef:      	addq	%rax, %r11
 3fa62f2:      	rolq	$0x2b, %r11
 3fa62f6:      	imulq	%r13, %rbx
 3fa62fa:      	addq	%rdx, %rcx
 3fa62fd:      	addq	%rax, %rcx
 3fa6300:      	movq	%rcx, %r14
 3fa6303:      	rolq	$0x14, %r14
 3fa6307:      	addq	%rax, %r14
 3fa630a:      	addq	%r11, %r14
 3fa630d:      	addq	%r15, %rcx
 3fa6310:      	addq	%rbx, %rsi
 3fa6313:      	addq	-0x20(%rbp), %rsi
 3fa6317:      	addq	%r9, %rdx
 3fa631a:      	movq	-0x8(%rbp), %rax
 3fa631e:      	addq	%rax, %rdx
 3fa6321:      	addq	%rsi, %rdx
 3fa6324:      	rolq	$0x2b, %rdx
 3fa6328:      	addq	%r10, %rdi
 3fa632b:      	addq	%rsi, %rdi
 3fa632e:      	movq	%rdi, %r10
 3fa6331:      	rolq	$0x14, %r10
 3fa6335:      	addq	%rsi, %r10
 3fa6338:      	addq	%rdx, %r10
 3fa633b:      	addq	%rax, %rdi
 3fa633e:      	movq	%r10, %rsi
 3fa6341:      	movq	%rdi, %r11
 3fa6344:      	movq	%r14, %rax
 3fa6347:      	movq	%rcx, %r14
 3fa634a:      	movq	%r8, %r15
 3fa634d:      	movq	%rbx, %r8
 3fa6350:      	jmp	0x3fa635c <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x2fc>
 3fa6352:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3fa635c:      	xorq	%r11, %r14
 3fa635f:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3fa6369:      	imulq	%rcx, %r14
 3fa636d:      	xorq	%r14, %r11
 3fa6370:      	shrq	$0x2f, %r14
 3fa6374:      	xorq	%r11, %r14
 3fa6377:      	imulq	%rcx, %r14
 3fa637b:      	movq	%r14, %rdi
 3fa637e:      	shrq	$0x2f, %rdi
 3fa6382:      	xorq	%r14, %rdi
 3fa6385:      	imulq	%rcx, %rdi
 3fa6389:      	movq	%r9, %rdx
 3fa638c:      	shrq	$0x2f, %rdx
 3fa6390:      	xorq	%r9, %rdx
 3fa6393:      	imulq	%r13, %rdx
 3fa6397:      	addq	%r15, %rdx
 3fa639a:      	addq	%rdi, %rdx
 3fa639d:      	xorq	%rsi, %rax
 3fa63a0:      	imulq	%rcx, %rax
 3fa63a4:      	xorq	%rax, %rsi
 3fa63a7:      	shrq	$0x2f, %rax
 3fa63ab:      	xorq	%rsi, %rax
 3fa63ae:      	imulq	%rcx, %rax
 3fa63b2:      	movq	%rax, %rsi
 3fa63b5:      	shrq	$0x2f, %rsi
 3fa63b9:      	xorq	%rax, %rsi
 3fa63bc:      	imulq	%rcx, %rsi
 3fa63c0:      	movq	%r12, %rax
 3fa63c3:      	shrq	$0x2f, %rax
 3fa63c7:      	xorq	%r12, %rax
 3fa63ca:      	imulq	%r13, %rax
 3fa63ce:      	addq	%r8, %rax
 3fa63d1:      	addq	%rsi, %rax
 3fa63d4:      	xorq	%rax, %rdx
 3fa63d7:      	imulq	%rcx, %rdx
 3fa63db:      	xorq	%rdx, %rax
 3fa63de:      	shrq	$0x2f, %rdx
 3fa63e2:      	xorq	%rax, %rdx
 3fa63e5:      	imulq	%rcx, %rdx
 3fa63e9:      	movq	%rdx, %rax
 3fa63ec:      	shrq	$0x2f, %rax
 3fa63f0:      	xorq	%rdx, %rax
 3fa63f3:      	imulq	%rcx, %rax
 3fa63f7:      	popq	%rbx
 3fa63f8:      	popq	%r12
 3fa63fa:      	popq	%r13
 3fa63fc:      	popq	%r14
 3fa63fe:      	popq	%r15
 3fa6400:      	popq	%rbp
 3fa6401:      	retq
