
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004242f50 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_>:
 4242f50:      	pushq	%rbp
 4242f51:      	pushq	%r15
 4242f53:      	pushq	%r14
 4242f55:      	pushq	%r13
 4242f57:      	pushq	%r12
 4242f59:      	pushq	%rbx
 4242f5a:      	subq	$0x48, %rsp
 4242f5e:      	movq	%rcx, %r12
 4242f61:      	testl	%esi, %esi
 4242f63:      	je	0x4242f90 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x40>
 4242f65:      	movq	%rdx, %r15
 4242f68:      	movl	%esi, %ebp
 4242f6a:      	movq	%rdi, %r14
 4242f6d:      	movq	(%rdx), %rbx
 4242f70:      	movl	0x4(%rbx), %esi
 4242f73:      	testl	$0x40000000, %esi       # imm = 0x40000000
 4242f79:      	jne	0x4242f99 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x49>
 4242f7b:      	movl	%esi, %eax
 4242f7d:      	andl	$0x7ffffff, %eax        # imm = 0x7FFFFFF
 4242f82:      	shll	$0x5, %esi
 4242f85:      	movq	%rbx, %rdi
 4242f88:      	subq	%rsi, %rdi
 4242f8b:      	movq	%rax, %rsi
 4242f8e:      	jmp	0x4242fa3 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x53>
 4242f90:      	xorl	%ebx, %ebx
 4242f92:      	xorl	%eax, %eax
 4242f94:      	jmp	0x4243508 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b8>
 4242f99:      	movq	-0x8(%rbx), %rdi
 4242f9d:      	andl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 4242fa3:      	movabsq	$-0xae502812aa7333, %r13 # imm = 0xFF51AFD7ED558CCD
 4242fad:      	shll	$0x5, %esi
 4242fb0:      	addq	%rdi, %rsi
 4242fb3:      	callq	0x3f42580 <_ZN4llvm7hashing6detail23hash_combine_range_implINS_4User17value_op_iteratorEEENS_9hash_codeET_S6_>
 4242fb8:      	movq	%rax, 0x38(%rsp)
 4242fbd:      	movq	-0x8(%rbx), %rax
 4242fc1:      	movl	0x48(%rbx), %edx
 4242fc4:      	shlq	$0x5, %rdx
 4242fc8:      	leaq	(%rax,%rdx), %rdi
 4242fcc:      	movl	0x4(%rbx), %ecx
 4242fcf:      	andl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4242fd5:      	leal	(,%rcx,8), %esi
 4242fdc:      	cmpl	$0x8, %ecx
 4242fdf:      	ja	0x4242ffe <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0xae>
 4242fe1:      	movq	%r13, %rdx
 4242fe4:      	callq	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 4242fe9:      	movq	%r13, %rdx
 4242fec:      	movq	%rax, %r13
 4242fef:      	movabsq	$-0x622015f714c7d297, %rdi # imm = 0x9DDFEA08EB382D69
 4242ff9:      	jmp	0x42433d4 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x484>
 4242ffe:      	movq	%rcx, (%rsp)
 4243002:      	movq	%r15, 0x20(%rsp)
 4243007:      	movq	%r14, 0x18(%rsp)
 424300c:      	movl	%ebp, 0xc(%rsp)
 4243010:      	movq	%r12, 0x10(%rsp)
 4243015:      	movabsq	$-0x4b6d499041670d8d, %r10 # imm = 0xB492B66FBE98F273
 424301f:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 4243029:      	movq	%r13, %r15
 424302c:      	movq	%rsi, %r13
 424302f:      	andl	$-0x40, %r13d
 4243033:      	movq	0x8(%rdi), %rbx
 4243037:      	movq	0x10(%rdi), %rsi
 424303b:      	movabsq	$-0x73d22641534b4d52, %r8 # imm = 0x8C2DD9BEACB4B2AE
 4243045:      	addq	%rbx, %r8
 4243048:      	rolq	$0x1b, %r8
 424304c:      	imulq	%r10, %r8
 4243050:      	movq	%rdi, %rbp
 4243053:      	movq	0x30(%rdi), %rdi
 4243057:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 4243061:      	addq	%rdi, %r9
 4243064:      	rolq	$0x16, %r9
 4243068:      	imulq	%r10, %r9
 424306c:      	movabsq	$-0x85335acd9bb6c6a, %r14 # imm = 0xF7ACCA5326449396
 4243076:      	xorq	%r8, %r14
 4243079:      	movq	0x28(%rbp), %r10
 424307d:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 4243087:      	addq	%r10, %r8
 424308a:      	addq	%r9, %r8
 424308d:      	movabsq	$0x298df016a9f64655, %r11 # imm = 0x298DF016A9F64655
 4243097:      	addq	(%rbp), %r11
 424309b:      	leaq	(%r15,%r11), %r9
 424309f:      	addq	%r14, %r9
 42430a2:      	movq	0x18(%rbp), %r15
 42430a6:      	leaq	-0x11a5f(%r15,%r9), %r12
 42430ae:      	rolq	$0x2b, %r12
 42430b2:      	addq	%rsi, %rbx
 42430b5:      	addq	%r11, %rbx
 42430b8:      	movq	%rbx, %r9
 42430bb:      	rolq	$0x14, %r9
 42430bf:      	addq	%r11, %r9
 42430c2:      	addq	%r12, %r9
 42430c5:      	movabsq	$0x4bf62cb950c3753a, %r11 # imm = 0x4BF62CB950C3753A
 42430cf:      	addq	0x20(%rbp), %r11
 42430d3:      	addq	%r15, %rbx
 42430d6:      	movq	%rbp, 0x30(%rsp)
 42430db:      	movq	0x38(%rbp), %r12
 42430df:      	addq	%r11, %rsi
 42430e2:      	addq	%r12, %rsi
 42430e5:      	addq	%r8, %rsi
 42430e8:      	rolq	$0x2b, %rsi
 42430ec:      	addq	%rdi, %r10
 42430ef:      	addq	%r11, %r10
 42430f2:      	movq	%r10, %r15
 42430f5:      	rolq	$0x14, %r15
 42430f9:      	addq	%r11, %r15
 42430fc:      	addq	%rsi, %r15
 42430ff:      	addq	%r12, %r10
 4243102:      	movq	%r13, 0x28(%rsp)
 4243107:      	cmpq	$0x40, %r13
 424310b:      	jne	0x4243121 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x1d1>
 424310d:      	movq	%r15, %r12
 4243110:      	movq	%r10, %r11
 4243113:      	movq	%r9, %rax
 4243116:      	movq	%rbx, %r13
 4243119:      	movq	%r14, %rbp
 424311c:      	jmp	0x424320c <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x2bc>
 4243121:      	leaq	0x78(%rdx,%rax), %rsi
 4243126:      	addq	$-0x40, 0x28(%rsp)
 424312c:      	xorl	%edx, %edx
 424312e:      	nop
 4243130:      	addq	%r8, %rcx
 4243133:      	addq	%rbx, %rcx
 4243136:      	movq	-0x30(%rsi,%rdx), %r13
 424313b:      	movq	-0x28(%rsi,%rdx), %rdi
 4243140:      	addq	%r13, %rcx
 4243143:      	rolq	$0x1b, %rcx
 4243147:      	movabsq	$-0x4b6d499041670d8d, %r12 # imm = 0xB492B66FBE98F273
 4243151:      	imulq	%r12, %rcx
 4243155:      	addq	%r9, %r8
 4243158:      	movq	-0x8(%rsi,%rdx), %rax
 424315d:      	movq	%rax, 0x40(%rsp)
 4243162:      	addq	%rax, %r8
 4243165:      	rolq	$0x16, %r8
 4243169:      	imulq	%r12, %r8
 424316d:      	movq	%rcx, %rbp
 4243170:      	xorq	%r15, %rbp
 4243173:      	movq	-0x10(%rsi,%rdx), %r11
 4243178:      	addq	%r11, %rbx
 424317b:      	addq	%r10, %r14
 424317e:      	rolq	$0x1f, %r14
 4243182:      	addq	%rbx, %r8
 4243185:      	imulq	%r12, %r9
 4243189:      	addq	-0x38(%rsi,%rdx), %r9
 424318e:      	movq	%r14, %rcx
 4243191:      	movq	-0x20(%rsi,%rdx), %rbx
 4243196:      	addq	%r9, %r10
 4243199:      	addq	%rbx, %r10
 424319c:      	addq	%rbp, %r10
 424319f:      	rolq	$0x2b, %r10
 42431a3:      	addq	%rdi, %r13
 42431a6:      	addq	%r9, %r13
 42431a9:      	movq	%r13, %rax
 42431ac:      	rolq	$0x14, %rax
 42431b0:      	imulq	%r12, %rcx
 42431b4:      	addq	%r9, %rax
 42431b7:      	addq	%r10, %rax
 42431ba:      	addq	%rcx, %r15
 42431bd:      	addq	%r8, %rdi
 42431c0:      	addq	-0x18(%rsi,%rdx), %r15
 42431c5:      	movq	(%rsi,%rdx), %r9
 42431c9:      	addq	%r15, %rdi
 42431cc:      	addq	%r9, %rdi
 42431cf:      	rolq	$0x2b, %rdi
 42431d3:      	addq	%rbx, %r13
 42431d6:      	addq	0x40(%rsp), %r11
 42431db:      	addq	%r15, %r11
 42431de:      	movq	%r11, %r12
 42431e1:      	rolq	$0x14, %r12
 42431e5:      	addq	%r15, %r12
 42431e8:      	addq	%rdi, %r12
 42431eb:      	addq	%r9, %r11
 42431ee:      	addq	$0x40, %rdx
 42431f2:      	movq	%rbp, %r14
 42431f5:      	movq	%r13, %rbx
 42431f8:      	movq	%rax, %r9
 42431fb:      	movq	%r11, %r10
 42431fe:      	movq	%r12, %r15
 4243201:      	cmpq	%rdx, 0x28(%rsp)
 4243206:      	jne	0x4243130 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x1e0>
 424320c:      	movq	(%rsp), %r9
 4243210:      	testb	$0x7, %r9b
 4243214:      	je	0x4243312 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x3c2>
 424321a:      	leaq	(%r8,%r13), %rdi
 424321e:      	movq	0x30(%rsp), %r14
 4243223:      	movq	-0x38(%r14,%r9,8), %rdx
 4243228:      	movq	-0x30(%r14,%r9,8), %rsi
 424322d:      	addq	%rdx, %rcx
 4243230:      	addq	%rdi, %rcx
 4243233:      	rolq	$0x1b, %rcx
 4243237:      	movabsq	$-0x4b6d499041670d8d, %r15 # imm = 0xB492B66FBE98F273
 4243241:      	imulq	%r15, %rcx
 4243245:      	addq	%rax, %r8
 4243248:      	movq	(%rsp), %rdi
 424324c:      	movq	-0x10(%r14,%rdi,8), %r9
 4243251:      	addq	%r9, %r8
 4243254:      	rolq	$0x16, %r8
 4243258:      	imulq	%r15, %r8
 424325c:      	xorq	%r12, %rcx
 424325f:      	movq	(%rsp), %rdi
 4243263:      	movq	-0x18(%r14,%rdi,8), %rdi
 4243268:      	addq	%rdi, %r13
 424326b:      	addq	%r13, %r8
 424326e:      	addq	%r11, %rbp
 4243271:      	rolq	$0x1f, %rbp
 4243275:      	movq	%rbp, %r10
 4243278:      	imulq	%r15, %rax
 424327c:      	addq	%rcx, %r11
 424327f:      	movq	(%rsp), %rbx
 4243283:      	addq	-0x40(%r14,%rbx,8), %rax
 4243288:      	movq	(%rsp), %rbx
 424328c:      	movq	-0x28(%r14,%rbx,8), %r13
 4243291:      	addq	%r13, %r11
 4243294:      	addq	%rax, %r11
 4243297:      	rolq	$0x2b, %r11
 424329b:      	imulq	%r15, %r10
 424329f:      	addq	%rsi, %rdx
 42432a2:      	addq	%rax, %rdx
 42432a5:      	movq	%rdx, %rbx
 42432a8:      	rolq	$0x14, %rbx
 42432ac:      	addq	%rax, %rbx
 42432af:      	addq	%r11, %rbx
 42432b2:      	addq	%r13, %rdx
 42432b5:      	addq	%r10, %r12
 42432b8:      	movq	(%rsp), %rax
 42432bc:      	addq	-0x20(%r14,%rax,8), %r12
 42432c1:      	addq	%r8, %rsi
 42432c4:      	movq	(%rsp), %rax
 42432c8:      	movq	-0x8(%r14,%rax,8), %rax
 42432cd:      	addq	%rax, %rsi
 42432d0:      	addq	%r12, %rsi
 42432d3:      	rolq	$0x2b, %rsi
 42432d7:      	addq	%r9, %rdi
 42432da:      	addq	%r12, %rdi
 42432dd:      	movq	%rdi, %r9
 42432e0:      	rolq	$0x14, %r9
 42432e4:      	addq	%r12, %r9
 42432e7:      	addq	%rsi, %r9
 42432ea:      	addq	%rax, %rdi
 42432ed:      	movq	%r9, %r12
 42432f0:      	movq	(%rsp), %r9
 42432f4:      	movq	%rdi, %r11
 42432f7:      	movq	%rbx, %rax
 42432fa:      	movq	%rdx, %r13
 42432fd:      	movq	%rcx, %rbp
 4243300:      	movq	%r10, %rcx
 4243303:      	movq	%r15, %r10
 4243306:      	movq	0x18(%rsp), %r14
 424330b:      	movq	0x20(%rsp), %r15
 4243310:      	jmp	0x4243326 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x3d6>
 4243312:      	movq	0x18(%rsp), %r14
 4243317:      	movq	0x20(%rsp), %r15
 424331c:      	movabsq	$-0x4b6d499041670d8d, %r10 # imm = 0xB492B66FBE98F273
 4243326:      	xorq	%r11, %r13
 4243329:      	movabsq	$-0x622015f714c7d297, %rdi # imm = 0x9DDFEA08EB382D69
 4243333:      	imulq	%rdi, %r13
 4243337:      	xorq	%r13, %r11
 424333a:      	shrq	$0x2f, %r13
 424333e:      	xorq	%r11, %r13
 4243341:      	imulq	%rdi, %r13
 4243345:      	movq	%r13, %rsi
 4243348:      	shrq	$0x2f, %rsi
 424334c:      	xorq	%r13, %rsi
 424334f:      	imulq	%rdi, %rsi
 4243353:      	movq	%r8, %rdx
 4243356:      	shrq	$0x2f, %rdx
 424335a:      	xorq	%r8, %rdx
 424335d:      	imulq	%r10, %rdx
 4243361:      	addq	%rbp, %rdx
 4243364:      	addq	%rsi, %rdx
 4243367:      	xorq	%r12, %rax
 424336a:      	imulq	%rdi, %rax
 424336e:      	xorq	%rax, %r12
 4243371:      	shrq	$0x2f, %rax
 4243375:      	xorq	%r12, %rax
 4243378:      	imulq	%rdi, %rax
 424337c:      	movq	%rax, %rsi
 424337f:      	shrq	$0x2f, %rsi
 4243383:      	xorq	%rax, %rsi
 4243386:      	imulq	%rdi, %rsi
 424338a:      	movabsq	$-0x5b6a4c820b386c68, %rax # imm = 0xA495B37DF4C79398
 4243394:      	imulq	%rax, %r9
 4243398:      	addq	%rcx, %r9
 424339b:      	addq	%rsi, %r9
 424339e:      	xorq	%r9, %rdx
 42433a1:      	imulq	%rdi, %rdx
 42433a5:      	xorq	%rdx, %r9
 42433a8:      	shrq	$0x2f, %rdx
 42433ac:      	xorq	%r9, %rdx
 42433af:      	imulq	%rdi, %rdx
 42433b3:      	movq	%rdx, %r13
 42433b6:      	shrq	$0x2f, %r13
 42433ba:      	xorq	%rdx, %r13
 42433bd:      	imulq	%rdi, %r13
 42433c1:      	movq	0x10(%rsp), %r12
 42433c6:      	movl	0xc(%rsp), %ebp
 42433ca:      	movabsq	$-0xae502812aa7333, %rdx # imm = 0xFF51AFD7ED558CCD
 42433d4:      	leaq	0x10(%r13), %rax
 42433d8:      	rolq	$0x30, %rax
 42433dc:      	movq	0x38(%rsp), %rcx
 42433e1:      	xorq	%rdx, %rcx
 42433e4:      	xorq	%rax, %rcx
 42433e7:      	imulq	%rdi, %rcx
 42433eb:      	xorq	%rcx, %rax
 42433ee:      	shrq	$0x2f, %rcx
 42433f2:      	xorq	%rax, %rcx
 42433f5:      	imulq	%rdi, %rcx
 42433f9:      	movq	%rcx, %rax
 42433fc:      	shrq	$0x2f, %rax
 4243400:      	xorl	%ecx, %eax
 4243402:      	imull	$0xeb382d69, %eax, %eax # imm = 0xEB382D69
 4243408:      	xorl	%eax, %r13d
 424340b:      	decl	%ebp
 424340d:      	andl	%ebp, %r13d
 4243410:      	movq	(%r15), %r15
 4243413:      	movq	%r15, %rax
 4243416:      	orq	$0x1000, %rax           # imm = 0x1000
 424341c:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 4243422:      	jne	0x4243477 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x527>
 4243424:      	movl	%r13d, %eax
 4243427:      	leaq	(%r14,%rax,8), %rbx
 424342b:      	movq	(%r14,%rax,8), %rdx
 424342f:      	movb	$0x1, %al
 4243431:      	cmpq	%rdx, %r15
 4243434:      	je	0x4243508 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b8>
 424343a:      	movl	$0x1, %ecx
 424343f:      	xorl	%esi, %esi
 4243441:      	cmpq	$-0x1000, %rdx          # imm = 0xF000
 4243448:      	je	0x4243520 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5d0>
 424344e:      	xorq	$-0x2000, %rdx          # imm = 0xE000
 4243455:      	orq	%rsi, %rdx
 4243458:      	cmoveq	%rbx, %rsi
 424345c:      	addl	%ecx, %r13d
 424345f:      	incl	%ecx
 4243461:      	andl	%ebp, %r13d
 4243464:      	leaq	(%r14,%r13,8), %rbx
 4243468:      	movq	(%r14,%r13,8), %rdx
 424346c:      	cmpq	%rdx, %r15
 424346f:      	je	0x4243508 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b8>
 4243475:      	jmp	0x4243441 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x4f1>
 4243477:      	movq	%r14, 0x18(%rsp)
 424347c:      	movl	%ebp, 0xc(%rsp)
 4243480:      	movq	%r12, 0x10(%rsp)
 4243485:      	movl	$0x1, %r14d
 424348b:      	xorl	%esi, %esi
 424348d:      	movl	%r13d, %eax
 4243490:      	movq	0x18(%rsp), %rcx
 4243495:      	leaq	(%rcx,%rax,8), %rbx
 4243499:      	movq	(%rcx,%rax,8), %r12
 424349d:      	movq	%r12, %rax
 42434a0:      	orq	$0x1000, %rax           # imm = 0x1000
 42434a6:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 42434ac:      	jne	0x42434b7 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x567>
 42434ae:      	movb	$0x1, %al
 42434b0:      	cmpq	%r12, %r15
 42434b3:      	je	0x4243503 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b3>
 42434b5:      	jmp	0x42434df <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x58f>
 42434b7:      	movq	%r15, %rdi
 42434ba:      	movq	%rsi, %rbp
 42434bd:      	movq	%r12, %rsi
 42434c0:      	xorl	%edx, %edx
 42434c2:      	callq	0x3b95b80 <_ZNK4llvm11Instruction24isIdenticalToWhenDefinedEPKS0_b>
 42434c7:      	movq	%rbp, %rsi
 42434ca:      	testb	%al, %al
 42434cc:      	je	0x42434df <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x58f>
 42434ce:      	movzbl	0x1(%r12), %ecx
 42434d4:      	xorb	0x1(%r15), %cl
 42434d8:      	movb	$0x1, %al
 42434da:      	cmpb	$0x2, %cl
 42434dd:      	jb	0x4243503 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5b3>
 42434df:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 42434e6:      	je	0x424351b <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x5cb>
 42434e8:      	xorq	$-0x2000, %r12          # imm = 0xE000
 42434ef:      	orq	%rsi, %r12
 42434f2:      	cmoveq	%rbx, %rsi
 42434f6:      	addl	%r14d, %r13d
 42434f9:      	incl	%r14d
 42434fc:      	andl	0xc(%rsp), %r13d
 4243501:      	jmp	0x424348d <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x53d>
 4243503:      	movq	0x10(%rsp), %r12
 4243508:      	movq	%rbx, (%r12)
 424350c:      	addq	$0x48, %rsp
 4243510:      	popq	%rbx
 4243511:      	popq	%r12
 4243513:      	popq	%r13
 4243515:      	popq	%r14
 4243517:      	popq	%r15
 4243519:      	popq	%rbp
 424351a:      	retq
 424351b:      	movq	0x10(%rsp), %r12
 4243520:      	testq	%rsi, %rsi
 4243523:      	cmovneq	%rsi, %rbx
 4243527:      	jmp	0x4242f92 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_6detail13DenseSetEmptyEZL38EliminateDuplicatePHINodesSetBasedImplPNS_10BasicBlockERNS_15SmallPtrSetImplIS3_EEE15PHIDenseMapInfoNS4_12DenseSetPairIS3_EEEES3_S5_SB_SD_E15LookupBucketForIS3_EEbRKT_RPSD_+0x42>
