
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004242ec0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_>:
 4242ec0:      	pushq	%rbp
 4242ec1:      	pushq	%r15
 4242ec3:      	pushq	%r14
 4242ec5:      	pushq	%r13
 4242ec7:      	pushq	%r12
 4242ec9:      	pushq	%rbx
 4242eca:      	subq	$0x48, %rsp
 4242ece:      	movq	%rcx, %r12
 4242ed1:      	testl	%esi, %esi
 4242ed3:      	je	0x4242f00 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x40>
 4242ed5:      	movq	%rdx, %r15
 4242ed8:      	movl	%esi, %ebp
 4242eda:      	movq	%rdi, %r14
 4242edd:      	movq	(%rdx), %rbx
 4242ee0:      	movl	0x4(%rbx), %esi
 4242ee3:      	testl	$0x40000000, %esi       # imm = 0x40000000
 4242ee9:      	jne	0x4242f09 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x49>
 4242eeb:      	movl	%esi, %eax
 4242eed:      	andl	$0x7ffffff, %eax        # imm = 0x7FFFFFF
 4242ef2:      	shll	$0x5, %esi
 4242ef5:      	movq	%rbx, %rdi
 4242ef8:      	subq	%rsi, %rdi
 4242efb:      	movq	%rax, %rsi
 4242efe:      	jmp	0x4242f13 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x53>
 4242f00:      	xorl	%ebx, %ebx
 4242f02:      	xorl	%eax, %eax
 4242f04:      	jmp	0x4243477 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b7>
 4242f09:      	movq	-0x8(%rbx), %rdi
 4242f0d:      	andl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 4242f13:      	movabsq	$-0xae502812aa7333, %r13 # imm = 0xFF51AFD7ED558CCD
 4242f1d:      	shll	$0x5, %esi
 4242f20:      	addq	%rdi, %rsi
 4242f23:      	callq	0x3f42500 <_ZN4llvm7hashing6detail23hash_combine_range_implINS_4User17value_op_iteratorEEENS_9hash_codeET_S6_>
 4242f28:      	movq	%rax, 0x38(%rsp)
 4242f2d:      	movq	-0x8(%rbx), %rax
 4242f31:      	movl	0x48(%rbx), %edx
 4242f34:      	shlq	$0x5, %rdx
 4242f38:      	leaq	(%rax,%rdx), %rdi
 4242f3c:      	movl	0x4(%rbx), %ecx
 4242f3f:      	andl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4242f45:      	leal	(,%rcx,8), %esi
 4242f4c:      	cmpl	$0x8, %ecx
 4242f4f:      	ja	0x4242f6e <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0xae>
 4242f51:      	movq	%r13, %rdx
 4242f54:      	callq	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 4242f59:      	movq	%r13, %rdx
 4242f5c:      	movq	%rax, %r13
 4242f5f:      	movabsq	$-0x622015f714c7d297, %rdi # imm = 0x9DDFEA08EB382D69
 4242f69:      	jmp	0x4243343 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x483>
 4242f6e:      	movq	%rcx, (%rsp)
 4242f72:      	movq	%r15, 0x20(%rsp)
 4242f77:      	movq	%r14, 0x18(%rsp)
 4242f7c:      	movl	%ebp, 0xc(%rsp)
 4242f80:      	movq	%r12, 0x10(%rsp)
 4242f85:      	movabsq	$-0x4b6d499041670d8d, %r10 # imm = 0xB492B66FBE98F273
 4242f8f:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 4242f99:      	movq	%r13, %r15
 4242f9c:      	movq	%rsi, %r13
 4242f9f:      	andl	$-0x40, %r13d
 4242fa3:      	movq	0x8(%rdi), %rbx
 4242fa7:      	movq	0x10(%rdi), %rsi
 4242fab:      	movabsq	$-0x73d22641534b4d52, %r8 # imm = 0x8C2DD9BEACB4B2AE
 4242fb5:      	addq	%rbx, %r8
 4242fb8:      	rolq	$0x1b, %r8
 4242fbc:      	imulq	%r10, %r8
 4242fc0:      	movq	%rdi, %rbp
 4242fc3:      	movq	0x30(%rdi), %rdi
 4242fc7:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 4242fd1:      	addq	%rdi, %r9
 4242fd4:      	rolq	$0x16, %r9
 4242fd8:      	imulq	%r10, %r9
 4242fdc:      	movabsq	$-0x85335acd9bb6c6a, %r14 # imm = 0xF7ACCA5326449396
 4242fe6:      	xorq	%r8, %r14
 4242fe9:      	movq	0x28(%rbp), %r10
 4242fed:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 4242ff7:      	addq	%r10, %r8
 4242ffa:      	addq	%r9, %r8
 4242ffd:      	movabsq	$0x298df016a9f64655, %r11 # imm = 0x298DF016A9F64655
 4243007:      	addq	(%rbp), %r11
 424300b:      	leaq	(%r15,%r11), %r9
 424300f:      	addq	%r14, %r9
 4243012:      	movq	0x18(%rbp), %r15
 4243016:      	leaq	-0x11a5f(%r15,%r9), %r12
 424301e:      	rolq	$0x2b, %r12
 4243022:      	addq	%rsi, %rbx
 4243025:      	addq	%r11, %rbx
 4243028:      	movq	%rbx, %r9
 424302b:      	rolq	$0x14, %r9
 424302f:      	addq	%r11, %r9
 4243032:      	addq	%r12, %r9
 4243035:      	movabsq	$0x4bf62cb950c3753a, %r11 # imm = 0x4BF62CB950C3753A
 424303f:      	addq	0x20(%rbp), %r11
 4243043:      	addq	%r15, %rbx
 4243046:      	movq	%rbp, 0x30(%rsp)
 424304b:      	movq	0x38(%rbp), %r12
 424304f:      	addq	%r11, %rsi
 4243052:      	addq	%r12, %rsi
 4243055:      	addq	%r8, %rsi
 4243058:      	rolq	$0x2b, %rsi
 424305c:      	addq	%rdi, %r10
 424305f:      	addq	%r11, %r10
 4243062:      	movq	%r10, %r15
 4243065:      	rolq	$0x14, %r15
 4243069:      	addq	%r11, %r15
 424306c:      	addq	%rsi, %r15
 424306f:      	addq	%r12, %r10
 4243072:      	movq	%r13, 0x28(%rsp)
 4243077:      	cmpq	$0x40, %r13
 424307b:      	jne	0x4243091 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x1d1>
 424307d:      	movq	%r15, %r12
 4243080:      	movq	%r10, %r11
 4243083:      	movq	%r9, %rax
 4243086:      	movq	%rbx, %r13
 4243089:      	movq	%r14, %rbp
 424308c:      	jmp	0x424317c <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x2bc>
 4243091:      	leaq	0x78(%rdx,%rax), %rsi
 4243096:      	addq	$-0x40, 0x28(%rsp)
 424309c:      	xorl	%edx, %edx
 424309e:      	nop
 42430a0:      	addq	%r8, %rcx
 42430a3:      	addq	%rbx, %rcx
 42430a6:      	movq	-0x30(%rsi,%rdx), %r13
 42430ab:      	movq	-0x28(%rsi,%rdx), %rdi
 42430b0:      	addq	%r13, %rcx
 42430b3:      	rolq	$0x1b, %rcx
 42430b7:      	movabsq	$-0x4b6d499041670d8d, %r12 # imm = 0xB492B66FBE98F273
 42430c1:      	imulq	%r12, %rcx
 42430c5:      	addq	%r9, %r8
 42430c8:      	movq	-0x8(%rsi,%rdx), %rax
 42430cd:      	movq	%rax, 0x40(%rsp)
 42430d2:      	addq	%rax, %r8
 42430d5:      	rolq	$0x16, %r8
 42430d9:      	imulq	%r12, %r8
 42430dd:      	movq	%rcx, %rbp
 42430e0:      	xorq	%r15, %rbp
 42430e3:      	movq	-0x10(%rsi,%rdx), %r11
 42430e8:      	addq	%r11, %rbx
 42430eb:      	addq	%r10, %r14
 42430ee:      	rolq	$0x1f, %r14
 42430f2:      	addq	%rbx, %r8
 42430f5:      	imulq	%r12, %r9
 42430f9:      	addq	-0x38(%rsi,%rdx), %r9
 42430fe:      	movq	%r14, %rcx
 4243101:      	movq	-0x20(%rsi,%rdx), %rbx
 4243106:      	addq	%r9, %r10
 4243109:      	addq	%rbx, %r10
 424310c:      	addq	%rbp, %r10
 424310f:      	rolq	$0x2b, %r10
 4243113:      	addq	%rdi, %r13
 4243116:      	addq	%r9, %r13
 4243119:      	movq	%r13, %rax
 424311c:      	rolq	$0x14, %rax
 4243120:      	imulq	%r12, %rcx
 4243124:      	addq	%r9, %rax
 4243127:      	addq	%r10, %rax
 424312a:      	addq	%rcx, %r15
 424312d:      	addq	%r8, %rdi
 4243130:      	addq	-0x18(%rsi,%rdx), %r15
 4243135:      	movq	(%rsi,%rdx), %r9
 4243139:      	addq	%r15, %rdi
 424313c:      	addq	%r9, %rdi
 424313f:      	rolq	$0x2b, %rdi
 4243143:      	addq	%rbx, %r13
 4243146:      	addq	0x40(%rsp), %r11
 424314b:      	addq	%r15, %r11
 424314e:      	movq	%r11, %r12
 4243151:      	rolq	$0x14, %r12
 4243155:      	addq	%r15, %r12
 4243158:      	addq	%rdi, %r12
 424315b:      	addq	%r9, %r11
 424315e:      	addq	$0x40, %rdx
 4243162:      	movq	%rbp, %r14
 4243165:      	movq	%r13, %rbx
 4243168:      	movq	%rax, %r9
 424316b:      	movq	%r11, %r10
 424316e:      	movq	%r12, %r15
 4243171:      	cmpq	%rdx, 0x28(%rsp)
 4243176:      	jne	0x42430a0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x1e0>
 424317c:      	movq	(%rsp), %r9
 4243180:      	testb	$0x7, %r9b
 4243184:      	je	0x4243281 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x3c1>
 424318a:      	movq	0x30(%rsp), %r14
 424318f:      	movq	-0x38(%r14,%r9,8), %rdx
 4243194:      	movq	-0x30(%r14,%r9,8), %rsi
 4243199:      	addq	%rdx, %rcx
 424319c:      	addq	%r8, %rcx
 424319f:      	addq	%r13, %rcx
 42431a2:      	rolq	$0x1b, %rcx
 42431a6:      	movabsq	$-0x4b6d499041670d8d, %r15 # imm = 0xB492B66FBE98F273
 42431b0:      	imulq	%r15, %rcx
 42431b4:      	addq	%rax, %r8
 42431b7:      	movq	(%rsp), %rdi
 42431bb:      	movq	-0x10(%r14,%rdi,8), %r9
 42431c0:      	addq	%r9, %r8
 42431c3:      	rolq	$0x16, %r8
 42431c7:      	imulq	%r15, %r8
 42431cb:      	xorq	%r12, %rcx
 42431ce:      	movq	(%rsp), %rdi
 42431d2:      	movq	-0x18(%r14,%rdi,8), %rdi
 42431d7:      	addq	%rdi, %r13
 42431da:      	addq	%r13, %r8
 42431dd:      	addq	%r11, %rbp
 42431e0:      	rolq	$0x1f, %rbp
 42431e4:      	movq	%rbp, %r10
 42431e7:      	imulq	%r15, %rax
 42431eb:      	addq	%rcx, %r11
 42431ee:      	movq	(%rsp), %rbx
 42431f2:      	addq	-0x40(%r14,%rbx,8), %rax
 42431f7:      	movq	(%rsp), %rbx
 42431fb:      	movq	-0x28(%r14,%rbx,8), %r13
 4243200:      	addq	%r13, %r11
 4243203:      	addq	%rax, %r11
 4243206:      	rolq	$0x2b, %r11
 424320a:      	imulq	%r15, %r10
 424320e:      	addq	%rsi, %rdx
 4243211:      	addq	%rax, %rdx
 4243214:      	movq	%rdx, %rbx
 4243217:      	rolq	$0x14, %rbx
 424321b:      	addq	%rax, %rbx
 424321e:      	addq	%r11, %rbx
 4243221:      	addq	%r13, %rdx
 4243224:      	addq	%r10, %r12
 4243227:      	movq	(%rsp), %rax
 424322b:      	addq	-0x20(%r14,%rax,8), %r12
 4243230:      	addq	%r8, %rsi
 4243233:      	movq	(%rsp), %rax
 4243237:      	movq	-0x8(%r14,%rax,8), %rax
 424323c:      	addq	%rax, %rsi
 424323f:      	addq	%r12, %rsi
 4243242:      	rolq	$0x2b, %rsi
 4243246:      	addq	%r9, %rdi
 4243249:      	addq	%r12, %rdi
 424324c:      	movq	%rdi, %r9
 424324f:      	rolq	$0x14, %r9
 4243253:      	addq	%r12, %r9
 4243256:      	addq	%rsi, %r9
 4243259:      	addq	%rax, %rdi
 424325c:      	movq	%r9, %r12
 424325f:      	movq	(%rsp), %r9
 4243263:      	movq	%rdi, %r11
 4243266:      	movq	%rbx, %rax
 4243269:      	movq	%rdx, %r13
 424326c:      	movq	%rcx, %rbp
 424326f:      	movq	%r10, %rcx
 4243272:      	movq	%r15, %r10
 4243275:      	movq	0x18(%rsp), %r14
 424327a:      	movq	0x20(%rsp), %r15
 424327f:      	jmp	0x4243295 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x3d5>
 4243281:      	movq	0x18(%rsp), %r14
 4243286:      	movq	0x20(%rsp), %r15
 424328b:      	movabsq	$-0x4b6d499041670d8d, %r10 # imm = 0xB492B66FBE98F273
 4243295:      	xorq	%r11, %r13
 4243298:      	movabsq	$-0x622015f714c7d297, %rdi # imm = 0x9DDFEA08EB382D69
 42432a2:      	imulq	%rdi, %r13
 42432a6:      	xorq	%r13, %r11
 42432a9:      	shrq	$0x2f, %r13
 42432ad:      	xorq	%r11, %r13
 42432b0:      	imulq	%rdi, %r13
 42432b4:      	movq	%r13, %rsi
 42432b7:      	shrq	$0x2f, %rsi
 42432bb:      	xorq	%r13, %rsi
 42432be:      	imulq	%rdi, %rsi
 42432c2:      	movq	%r8, %rdx
 42432c5:      	shrq	$0x2f, %rdx
 42432c9:      	xorq	%r8, %rdx
 42432cc:      	imulq	%r10, %rdx
 42432d0:      	addq	%rbp, %rdx
 42432d3:      	addq	%rsi, %rdx
 42432d6:      	xorq	%r12, %rax
 42432d9:      	imulq	%rdi, %rax
 42432dd:      	xorq	%rax, %r12
 42432e0:      	shrq	$0x2f, %rax
 42432e4:      	xorq	%r12, %rax
 42432e7:      	imulq	%rdi, %rax
 42432eb:      	movq	%rax, %rsi
 42432ee:      	shrq	$0x2f, %rsi
 42432f2:      	xorq	%rax, %rsi
 42432f5:      	imulq	%rdi, %rsi
 42432f9:      	movabsq	$-0x5b6a4c820b386c68, %rax # imm = 0xA495B37DF4C79398
 4243303:      	imulq	%rax, %r9
 4243307:      	addq	%rcx, %r9
 424330a:      	addq	%rsi, %r9
 424330d:      	xorq	%r9, %rdx
 4243310:      	imulq	%rdi, %rdx
 4243314:      	xorq	%rdx, %r9
 4243317:      	shrq	$0x2f, %rdx
 424331b:      	xorq	%r9, %rdx
 424331e:      	imulq	%rdi, %rdx
 4243322:      	movq	%rdx, %r13
 4243325:      	shrq	$0x2f, %r13
 4243329:      	xorq	%rdx, %r13
 424332c:      	imulq	%rdi, %r13
 4243330:      	movq	0x10(%rsp), %r12
 4243335:      	movl	0xc(%rsp), %ebp
 4243339:      	movabsq	$-0xae502812aa7333, %rdx # imm = 0xFF51AFD7ED558CCD
 4243343:      	leaq	0x10(%r13), %rax
 4243347:      	rolq	$0x30, %rax
 424334b:      	movq	0x38(%rsp), %rcx
 4243350:      	xorq	%rdx, %rcx
 4243353:      	xorq	%rax, %rcx
 4243356:      	imulq	%rdi, %rcx
 424335a:      	xorq	%rcx, %rax
 424335d:      	shrq	$0x2f, %rcx
 4243361:      	xorq	%rax, %rcx
 4243364:      	imulq	%rdi, %rcx
 4243368:      	movq	%rcx, %rax
 424336b:      	shrq	$0x2f, %rax
 424336f:      	xorl	%ecx, %eax
 4243371:      	imull	$0xeb382d69, %eax, %eax # imm = 0xEB382D69
 4243377:      	xorl	%eax, %r13d
 424337a:      	decl	%ebp
 424337c:      	andl	%ebp, %r13d
 424337f:      	movq	(%r15), %r15
 4243382:      	movq	%r15, %rax
 4243385:      	orq	$0x1000, %rax           # imm = 0x1000
 424338b:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 4243391:      	jne	0x42433e6 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x526>
 4243393:      	movl	%r13d, %eax
 4243396:      	leaq	(%r14,%rax,8), %rbx
 424339a:      	movq	(%r14,%rax,8), %rdx
 424339e:      	movb	$0x1, %al
 42433a0:      	cmpq	%rdx, %r15
 42433a3:      	je	0x4243477 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b7>
 42433a9:      	movl	$0x1, %ecx
 42433ae:      	xorl	%esi, %esi
 42433b0:      	cmpq	$-0x1000, %rdx          # imm = 0xF000
 42433b7:      	je	0x424348f <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5cf>
 42433bd:      	xorq	$-0x2000, %rdx          # imm = 0xE000
 42433c4:      	orq	%rsi, %rdx
 42433c7:      	cmoveq	%rbx, %rsi
 42433cb:      	addl	%ecx, %r13d
 42433ce:      	incl	%ecx
 42433d0:      	andl	%ebp, %r13d
 42433d3:      	leaq	(%r14,%r13,8), %rbx
 42433d7:      	movq	(%r14,%r13,8), %rdx
 42433db:      	cmpq	%rdx, %r15
 42433de:      	je	0x4243477 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b7>
 42433e4:      	jmp	0x42433b0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x4f0>
 42433e6:      	movq	%r14, 0x18(%rsp)
 42433eb:      	movl	%ebp, 0xc(%rsp)
 42433ef:      	movq	%r12, 0x10(%rsp)
 42433f4:      	movl	$0x1, %r14d
 42433fa:      	xorl	%esi, %esi
 42433fc:      	movl	%r13d, %eax
 42433ff:      	movq	0x18(%rsp), %rcx
 4243404:      	leaq	(%rcx,%rax,8), %rbx
 4243408:      	movq	(%rcx,%rax,8), %r12
 424340c:      	movq	%r12, %rax
 424340f:      	orq	$0x1000, %rax           # imm = 0x1000
 4243415:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 424341b:      	jne	0x4243426 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x566>
 424341d:      	movb	$0x1, %al
 424341f:      	cmpq	%r12, %r15
 4243422:      	je	0x4243472 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b2>
 4243424:      	jmp	0x424344e <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x58e>
 4243426:      	movq	%r15, %rdi
 4243429:      	movq	%rsi, %rbp
 424342c:      	movq	%r12, %rsi
 424342f:      	xorl	%edx, %edx
 4243431:      	callq	0x3b95af0 <_ZNK4llvm11Instruction24isIdenticalToWhenDefinedEPKS0_b>
 4243436:      	movq	%rbp, %rsi
 4243439:      	testb	%al, %al
 424343b:      	je	0x424344e <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x58e>
 424343d:      	movzbl	0x1(%r12), %ecx
 4243443:      	xorb	0x1(%r15), %cl
 4243447:      	movb	$0x1, %al
 4243449:      	cmpb	$0x2, %cl
 424344c:      	jb	0x4243472 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b2>
 424344e:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 4243455:      	je	0x424348a <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5ca>
 4243457:      	xorq	$-0x2000, %r12          # imm = 0xE000
 424345e:      	orq	%rsi, %r12
 4243461:      	cmoveq	%rbx, %rsi
 4243465:      	addl	%r14d, %r13d
 4243468:      	incl	%r14d
 424346b:      	andl	0xc(%rsp), %r13d
 4243470:      	jmp	0x42433fc <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x53c>
 4243472:      	movq	0x10(%rsp), %r12
 4243477:      	movq	%rbx, (%r12)
 424347b:      	addq	$0x48, %rsp
 424347f:      	popq	%rbx
 4243480:      	popq	%r12
 4243482:      	popq	%r13
 4243484:      	popq	%r14
 4243486:      	popq	%r15
 4243488:      	popq	%rbp
 4243489:      	retq
 424348a:      	movq	0x10(%rsp), %r12
 424348f:      	testq	%rsi, %rsi
 4243492:      	cmovneq	%rsi, %rbx
 4243496:      	jmp	0x4242f02 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x42>
