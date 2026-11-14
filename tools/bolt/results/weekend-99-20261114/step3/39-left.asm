
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003fa60e0 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_>:
 3fa60e0:      	movq	%rsi, %rcx
 3fa60e3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3fa60ed:      	subq	%rdi, %rsi
 3fa60f0:      	cmpq	$0x40, %rsi
 3fa60f4:      	ja	0x3fa6104 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x24>
 3fa60f6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3fa60fc:      	movq	%rax, %rdx
 3fa60ff:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3fa6104:      	pushq	%rbp
 3fa6105:      	pushq	%r15
 3fa6107:      	pushq	%r14
 3fa6109:      	pushq	%r13
 3fa610b:      	pushq	%r12
 3fa610d:      	pushq	%rbx
 3fa610e:      	movq	%rcx, -0x18(%rsp)
 3fa6113:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3fa611d:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3fa6127:      	movq	%rsi, -0x10(%rsp)
 3fa612c:      	movq	%rsi, %r14
 3fa612f:      	andq	$-0x40, %r14
 3fa6133:      	movq	0x8(%rdi), %r13
 3fa6137:      	movq	0x10(%rdi), %rcx
 3fa613b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3fa6145:      	addq	%r13, %rdx
 3fa6148:      	rolq	$0x1b, %rdx
 3fa614c:      	imulq	%r9, %rdx
 3fa6150:      	movq	0x30(%rdi), %rsi
 3fa6154:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3fa615e:      	addq	%rsi, %r10
 3fa6161:      	rolq	$0x16, %r10
 3fa6165:      	imulq	%r9, %r10
 3fa6169:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3fa6173:      	xorq	%rdx, %rbp
 3fa6176:      	movq	0x28(%rdi), %r12
 3fa617a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3fa6184:      	addq	%r12, %r9
 3fa6187:      	addq	%r10, %r9
 3fa618a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3fa6194:      	addq	(%rdi), %r10
 3fa6197:      	movq	0x18(%rdi), %r11
 3fa619b:      	addq	%r10, %rax
 3fa619e:      	addq	%r11, %rax
 3fa61a1:      	addq	%rbp, %rax
 3fa61a4:      	rolq	$0x2b, %rax
 3fa61a8:      	addq	%rcx, %r13
 3fa61ab:      	addq	%r10, %r13
 3fa61ae:      	movq	%r13, %rdx
 3fa61b1:      	rolq	$0x14, %rdx
 3fa61b5:      	addq	%r10, %rdx
 3fa61b8:      	addq	%rax, %rdx
 3fa61bb:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3fa61c5:      	addq	0x20(%rdi), %rax
 3fa61c9:      	addq	%r11, %r13
 3fa61cc:      	movq	0x38(%rdi), %r10
 3fa61d0:      	addq	%rax, %rcx
 3fa61d3:      	addq	%r10, %rcx
 3fa61d6:      	addq	%r9, %rcx
 3fa61d9:      	rolq	$0x2b, %rcx
 3fa61dd:      	addq	%rsi, %r12
 3fa61e0:      	addq	%rax, %r12
 3fa61e3:      	movq	%r12, %rbx
 3fa61e6:      	rolq	$0x14, %rbx
 3fa61ea:      	addq	%rax, %rbx
 3fa61ed:      	addq	%rcx, %rbx
 3fa61f0:      	addq	%r10, %r12
 3fa61f3:      	movq	%r14, -0x20(%rsp)
 3fa61f8:      	cmpq	$0x40, %r14
 3fa61fc:      	jne	0x3fa6212 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x132>
 3fa61fe:      	movq	%rbx, %rsi
 3fa6201:      	movq	%r12, %r11
 3fa6204:      	movq	%rdx, %rax
 3fa6207:      	movq	%r13, %r14
 3fa620a:      	movq	%rbp, %r15
 3fa620d:      	jmp	0x3fa62fd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x21d>
 3fa6212:      	addq	$-0x40, -0x20(%rsp)
 3fa6218:      	xorl	%ecx, %ecx
 3fa621a:      	nopw	(%rax,%rax)
 3fa6220:      	addq	%r9, %r8
 3fa6223:      	addq	%r13, %r8
 3fa6226:      	movq	0x48(%rdi,%rcx), %r14
 3fa622b:      	movq	0x50(%rdi,%rcx), %r10
 3fa6230:      	addq	%r14, %r8
 3fa6233:      	rolq	$0x1b, %r8
 3fa6237:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3fa6241:      	imulq	%rsi, %r8
 3fa6245:      	addq	%rdx, %r9
 3fa6248:      	movq	0x70(%rdi,%rcx), %rax
 3fa624d:      	movq	%rax, -0x8(%rsp)
 3fa6252:      	addq	%rax, %r9
 3fa6255:      	rolq	$0x16, %r9
 3fa6259:      	imulq	%rsi, %r9
 3fa625d:      	movq	%r8, %r15
 3fa6260:      	xorq	%rbx, %r15
 3fa6263:      	movq	0x68(%rdi,%rcx), %r11
 3fa6268:      	addq	%r11, %r13
 3fa626b:      	addq	%r12, %rbp
 3fa626e:      	rolq	$0x1f, %rbp
 3fa6272:      	addq	%r13, %r9
 3fa6275:      	imulq	%rsi, %rdx
 3fa6279:      	addq	0x40(%rdi,%rcx), %rdx
 3fa627e:      	movq	%rbp, %r8
 3fa6281:      	movq	0x58(%rdi,%rcx), %r13
 3fa6286:      	addq	%rdx, %r12
 3fa6289:      	addq	%r13, %r12
 3fa628c:      	addq	%r15, %r12
 3fa628f:      	rolq	$0x2b, %r12
 3fa6293:      	addq	%r10, %r14
 3fa6296:      	addq	%rdx, %r14
 3fa6299:      	movq	%r14, %rax
 3fa629c:      	rolq	$0x14, %rax
 3fa62a0:      	imulq	%rsi, %r8
 3fa62a4:      	addq	%rdx, %rax
 3fa62a7:      	addq	%r12, %rax
 3fa62aa:      	addq	%r8, %rbx
 3fa62ad:      	addq	%r9, %r10
 3fa62b0:      	addq	0x60(%rdi,%rcx), %rbx
 3fa62b5:      	movq	0x78(%rdi,%rcx), %rdx
 3fa62ba:      	addq	%rbx, %r10
 3fa62bd:      	addq	%rdx, %r10
 3fa62c0:      	rolq	$0x2b, %r10
 3fa62c4:      	addq	%r13, %r14
 3fa62c7:      	addq	-0x8(%rsp), %r11
 3fa62cc:      	addq	%rbx, %r11
 3fa62cf:      	movq	%r11, %rsi
 3fa62d2:      	rolq	$0x14, %rsi
 3fa62d6:      	addq	%rbx, %rsi
 3fa62d9:      	addq	%r10, %rsi
 3fa62dc:      	addq	%rdx, %r11
 3fa62df:      	addq	$0x40, %rcx
 3fa62e3:      	movq	%r15, %rbp
 3fa62e6:      	movq	%r14, %r13
 3fa62e9:      	movq	%rax, %rdx
 3fa62ec:      	movq	%r11, %r12
 3fa62ef:      	movq	%rsi, %rbx
 3fa62f2:      	cmpq	%rcx, -0x20(%rsp)
 3fa62f7:      	jne	0x3fa6220 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x140>
 3fa62fd:      	movq	-0x10(%rsp), %r12
 3fa6302:      	testb	$0x3f, %r12b
 3fa6306:      	je	0x3fa63d3 <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x2f3>
 3fa630c:      	leaq	(%r9,%r14), %rdi
 3fa6310:      	movq	-0x18(%rsp), %rbp
 3fa6315:      	movq	-0x38(%rbp), %rcx
 3fa6319:      	movq	-0x30(%rbp), %rdx
 3fa631d:      	addq	%rcx, %r8
 3fa6320:      	addq	%rdi, %r8
 3fa6323:      	rolq	$0x1b, %r8
 3fa6327:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3fa6331:      	imulq	%r13, %r8
 3fa6335:      	addq	%rax, %r9
 3fa6338:      	movq	-0x10(%rbp), %r10
 3fa633c:      	addq	%r10, %r9
 3fa633f:      	rolq	$0x16, %r9
 3fa6343:      	imulq	%r13, %r9
 3fa6347:      	xorq	%rsi, %r8
 3fa634a:      	movq	-0x18(%rbp), %rdi
 3fa634e:      	addq	%rdi, %r14
 3fa6351:      	addq	%r14, %r9
 3fa6354:      	addq	%r11, %r15
 3fa6357:      	rolq	$0x1f, %r15
 3fa635b:      	movq	%r15, %rbx
 3fa635e:      	imulq	%r13, %rax
 3fa6362:      	addq	%r8, %r11
 3fa6365:      	addq	-0x40(%rbp), %rax
 3fa6369:      	movq	-0x28(%rbp), %r15
 3fa636d:      	addq	%r15, %r11
 3fa6370:      	addq	%rax, %r11
 3fa6373:      	rolq	$0x2b, %r11
 3fa6377:      	imulq	%r13, %rbx
 3fa637b:      	addq	%rdx, %rcx
 3fa637e:      	addq	%rax, %rcx
 3fa6381:      	movq	%rcx, %r14
 3fa6384:      	rolq	$0x14, %r14
 3fa6388:      	addq	%rax, %r14
 3fa638b:      	addq	%r11, %r14
 3fa638e:      	addq	%r15, %rcx
 3fa6391:      	addq	%rbx, %rsi
 3fa6394:      	addq	-0x20(%rbp), %rsi
 3fa6398:      	addq	%r9, %rdx
 3fa639b:      	movq	-0x8(%rbp), %rax
 3fa639f:      	addq	%rax, %rdx
 3fa63a2:      	addq	%rsi, %rdx
 3fa63a5:      	rolq	$0x2b, %rdx
 3fa63a9:      	addq	%r10, %rdi
 3fa63ac:      	addq	%rsi, %rdi
 3fa63af:      	movq	%rdi, %r10
 3fa63b2:      	rolq	$0x14, %r10
 3fa63b6:      	addq	%rsi, %r10
 3fa63b9:      	addq	%rdx, %r10
 3fa63bc:      	addq	%rax, %rdi
 3fa63bf:      	movq	%r10, %rsi
 3fa63c2:      	movq	%rdi, %r11
 3fa63c5:      	movq	%r14, %rax
 3fa63c8:      	movq	%rcx, %r14
 3fa63cb:      	movq	%r8, %r15
 3fa63ce:      	movq	%rbx, %r8
 3fa63d1:      	jmp	0x3fa63dd <_ZN4llvm7hashing6detail23hash_combine_range_implIKPKNS_4SCEVEEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS8_SC_+0x2fd>
 3fa63d3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3fa63dd:      	xorq	%r11, %r14
 3fa63e0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3fa63ea:      	imulq	%rcx, %r14
 3fa63ee:      	xorq	%r14, %r11
 3fa63f1:      	shrq	$0x2f, %r14
 3fa63f5:      	xorq	%r11, %r14
 3fa63f8:      	imulq	%rcx, %r14
 3fa63fc:      	movq	%r14, %rdi
 3fa63ff:      	shrq	$0x2f, %rdi
 3fa6403:      	xorq	%r14, %rdi
 3fa6406:      	imulq	%rcx, %rdi
 3fa640a:      	movq	%r9, %rdx
 3fa640d:      	shrq	$0x2f, %rdx
 3fa6411:      	xorq	%r9, %rdx
 3fa6414:      	imulq	%r13, %rdx
 3fa6418:      	addq	%r15, %rdx
 3fa641b:      	addq	%rdi, %rdx
 3fa641e:      	xorq	%rsi, %rax
 3fa6421:      	imulq	%rcx, %rax
 3fa6425:      	xorq	%rax, %rsi
 3fa6428:      	shrq	$0x2f, %rax
 3fa642c:      	xorq	%rsi, %rax
 3fa642f:      	imulq	%rcx, %rax
 3fa6433:      	movq	%rax, %rsi
 3fa6436:      	shrq	$0x2f, %rsi
 3fa643a:      	xorq	%rax, %rsi
 3fa643d:      	imulq	%rcx, %rsi
 3fa6441:      	movq	%r12, %rax
 3fa6444:      	shrq	$0x2f, %rax
 3fa6448:      	xorq	%r12, %rax
 3fa644b:      	imulq	%r13, %rax
 3fa644f:      	addq	%r8, %rax
 3fa6452:      	addq	%rsi, %rax
 3fa6455:      	xorq	%rax, %rdx
 3fa6458:      	imulq	%rcx, %rdx
 3fa645c:      	xorq	%rdx, %rax
 3fa645f:      	shrq	$0x2f, %rdx
 3fa6463:      	xorq	%rax, %rdx
 3fa6466:      	imulq	%rcx, %rdx
 3fa646a:      	movq	%rdx, %rax
 3fa646d:      	shrq	$0x2f, %rax
 3fa6471:      	xorq	%rdx, %rax
 3fa6474:      	imulq	%rcx, %rax
 3fa6478:      	popq	%rbx
 3fa6479:      	popq	%r12
 3fa647b:      	popq	%r13
 3fa647d:      	popq	%r14
 3fa647f:      	popq	%r15
 3fa6481:      	popq	%rbp
 3fa6482:      	retq
