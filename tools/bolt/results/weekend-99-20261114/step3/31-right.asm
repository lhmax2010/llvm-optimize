
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bd7060 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv>:
 3bd7060:      	pushq	%rbp
 3bd7061:      	pushq	%r15
 3bd7063:      	pushq	%r14
 3bd7065:      	pushq	%r13
 3bd7067:      	pushq	%r12
 3bd7069:      	pushq	%rbx
 3bd706a:      	subq	$0x58, %rsp
 3bd706e:      	movq	%rdi, 0x10(%rsp)
 3bd7073:      	leaq	0x28(%rsp), %rax
 3bd7078:      	movq	%rax, 0x18(%rsp)
 3bd707d:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd7087:      	movq	%r14, 0x20(%rsp)
 3bd708c:      	movl	0x10(%rsi), %edi
 3bd708f:      	leaq	0x18(%rsi), %rax
 3bd7093:      	testb	$0x1, %dil
 3bd7097:      	cmoveq	0x18(%rsi), %rax
 3bd709c:      	movl	$0x4, %ecx
 3bd70a1:      	movq	%rsi, 0x8(%rsp)
 3bd70a6:      	cmovel	0x20(%rsi), %ecx
 3bd70aa:      	leaq	(,%rcx,8), %rdx
 3bd70b2:      	leaq	(%rdx,%rdx,2), %rdx
 3bd70b6:      	leaq	(%rax,%rdx), %r13
 3bd70ba:      	movq	%r13, %rbp
 3bd70bd:      	cmpl	$0x2, %edi
 3bd70c0:      	jb	0x3bd70fa <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x9a>
 3bd70c2:      	movq	%rax, %rbp
 3bd70c5:      	testq	%rcx, %rcx
 3bd70c8:      	je	0x3bd70fa <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x9a>
 3bd70ca:      	movl	$0x1000, %esi           # imm = 0x1000
 3bd70cf:      	movq	%rax, %rbp
 3bd70d2:      	nopw	%cs:(%rax,%rax)
 3bd70dc:      	nopl	(%rax)
 3bd70e0:      	movq	(%rbp), %rdi
 3bd70e4:      	orq	%rsi, %rdi
 3bd70e7:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 3bd70ee:      	jne	0x3bd70fa <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x9a>
 3bd70f0:      	addq	$0x18, %rbp
 3bd70f4:      	addq	$-0x18, %rdx
 3bd70f8:      	jne	0x3bd70e0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x80>
 3bd70fa:      	leaq	(%rcx,%rcx,2), %rcx
 3bd70fe:      	leaq	(%rax,%rcx,8), %r15
 3bd7102:      	cmpq	%r15, %rbp
 3bd7105:      	je	0x3bd721a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1ba>
 3bd710b:      	addq	$0x10, 0x8(%rsp)
 3bd7111:      	xorl	%r12d, %r12d
 3bd7114:      	movl	$0x1000, %r14d          # imm = 0x1000
 3bd711a:      	jmp	0x3bd7129 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xc9>
 3bd711c:      	nopl	(%rax)
 3bd7120:      	cmpq	%r15, %rbp
 3bd7123:      	je	0x3bd71bd <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x15d>
 3bd7129:      	movq	0x8(%rbp), %rax
 3bd712d:      	cmpq	$0x4, %rax
 3bd7131:      	setb	%cl
 3bd7134:      	movl	%eax, %edx
 3bd7136:      	andl	$0x3, %edx
 3bd7139:      	cmpl	$0x1, %edx
 3bd713c:      	setne	%dl
 3bd713f:      	orb	%cl, %dl
 3bd7141:      	jne	0x3bd7180 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x120>
 3bd7143:      	andq	$-0x4, %rax
 3bd7147:      	cmpb	$0x4, (%rax)
 3bd714a:      	jne	0x3bd7180 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x120>
 3bd714c:      	movq	(%rbp), %rsi
 3bd7150:      	movq	0x8(%rsp), %rdi
 3bd7155:      	callq	0x3beb210 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPvSt4pairINS_12PointerUnionIJPNS_15MetadataAsValueEPNS_8MetadataEPNS_14DebugValueUserEEEEmELj4ENS_12DenseMapInfoIS2_vEENS_6detail12DenseMapPairIS2_SC_EEEES2_SC_SE_SH_E24lookupOrInsertIntoBucketIRKS2_JEEES3_IPSH_bEOT_DpOT0_>
 3bd715a:      	movl	0x20(%rsp), %edx
 3bd715e:      	cmpl	0x24(%rsp), %edx
 3bd7162:      	jae	0x3bd719a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x13a>
 3bd7164:      	addq	$0x8, %rax
 3bd7168:      	movq	0x18(%rsp), %rcx
 3bd716d:      	movl	%edx, %edx
 3bd716f:      	movq	%rax, (%rcx,%rdx,8)
 3bd7173:      	movl	0x20(%rsp), %r12d
 3bd7178:      	incl	%r12d
 3bd717b:      	movl	%r12d, 0x20(%rsp)
 3bd7180:      	addq	$0x18, %rbp
 3bd7184:      	cmpq	%r13, %rbp
 3bd7187:      	je	0x3bd7120 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xc0>
 3bd7189:      	movq	(%rbp), %rax
 3bd718d:      	orq	%r14, %rax
 3bd7190:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 3bd7196:      	je	0x3bd7180 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x120>
 3bd7198:      	jmp	0x3bd7120 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xc0>
 3bd719a:      	incq	%rdx
 3bd719d:      	movl	$0x8, %ecx
 3bd71a2:      	leaq	0x18(%rsp), %rdi
 3bd71a7:      	leaq	0x28(%rsp), %rsi
 3bd71ac:      	movq	%rax, %r12
 3bd71af:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd71b4:      	movq	%r12, %rax
 3bd71b7:      	movl	0x20(%rsp), %edx
 3bd71bb:      	jmp	0x3bd7164 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x104>
 3bd71bd:      	testl	%r12d, %r12d
 3bd71c0:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd71ca:      	je	0x3bd721a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1ba>
 3bd71cc:      	movq	0x18(%rsp), %r15
 3bd71d1:      	movl	%r12d, %eax
 3bd71d4:      	leaq	(%r15,%rax,8), %rbp
 3bd71d8:      	bsrq	%rax, %rdx
 3bd71dc:      	xorl	$0x3f, %edx
 3bd71df:      	addl	%edx, %edx
 3bd71e1:      	xorq	$0x7e, %rdx
 3bd71e5:      	movq	%r15, %rdi
 3bd71e8:      	movq	%rbp, %rsi
 3bd71eb:      	callq	0x3beb820 <_ZSt16__introsort_loopIPPSt4pairIN4llvm12PointerUnionIJPNS1_15MetadataAsValueEPNS1_8MetadataEPNS1_14DebugValueUserEEEEmElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_23ReplaceableMetadataImpl18getAllArgListUsersEvE3$_0EEEvT_SJ_T0_T1_>
 3bd71f0:      	leaq	0x8(%r15), %rbx
 3bd71f4:      	cmpl	$0x11, %r12d
 3bd71f8:      	jb	0x3bd7210 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1b0>
 3bd71fa:      	movq	%rbp, 0x8(%rsp)
 3bd71ff:      	leaq	0x8(%r15), %r12
 3bd7203:      	movl	$0x8, %ebp
 3bd7208:      	movq	%r15, %r14
 3bd720b:      	jmp	0x3bd7377 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x317>
 3bd7210:      	cmpl	$0x1, %r12d
 3bd7214:      	jne	0x3bd72c9 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x269>
 3bd721a:      	movq	0x10(%rsp), %rbx
 3bd721f:      	leaq	0x10(%rbx), %r15
 3bd7223:      	movq	%r15, (%rbx)
 3bd7226:      	movq	%r14, 0x8(%rbx)
 3bd722a:      	movq	0x18(%rsp), %rdi
 3bd722f:      	movl	0x20(%rsp), %r14d
 3bd7234:      	testq	%r14, %r14
 3bd7237:      	je	0x3bd72a8 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x248>
 3bd7239:      	shlq	$0x3, %r14
 3bd723d:      	xorl	%eax, %eax
 3bd723f:      	xorl	%r12d, %r12d
 3bd7242:      	nopw	%cs:(%rax,%rax)
 3bd724c:      	nopl	(%rax)
 3bd7250:      	movq	(%rdi,%r12), %rcx
 3bd7254:      	movq	(%rcx), %r13
 3bd7257:      	cmpl	0xc(%rbx), %eax
 3bd725a:      	jae	0x3bd727c <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x21c>
 3bd725c:      	andq	$-0x4, %r13
 3bd7260:      	movq	(%rbx), %rcx
 3bd7263:      	movl	%eax, %eax
 3bd7265:      	movq	%r13, (%rcx,%rax,8)
 3bd7269:      	movl	0x8(%rbx), %eax
 3bd726c:      	incl	%eax
 3bd726e:      	movl	%eax, 0x8(%rbx)
 3bd7271:      	addq	$0x8, %r12
 3bd7275:      	cmpq	%r12, %r14
 3bd7278:      	jne	0x3bd7250 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1f0>
 3bd727a:      	jmp	0x3bd72a3 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x243>
 3bd727c:      	movl	%eax, %edx
 3bd727e:      	incq	%rdx
 3bd7281:      	movl	$0x8, %ecx
 3bd7286:      	movq	%rdi, %rbp
 3bd7289:      	movq	0x10(%rsp), %rdi
 3bd728e:      	movq	%r15, %rsi
 3bd7291:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd7296:      	movq	%rbp, %rdi
 3bd7299:      	movq	0x10(%rsp), %rbx
 3bd729e:      	movl	0x8(%rbx), %eax
 3bd72a1:      	jmp	0x3bd725c <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1fc>
 3bd72a3:      	movq	0x18(%rsp), %rdi
 3bd72a8:      	leaq	0x28(%rsp), %rax
 3bd72ad:      	cmpq	%rax, %rdi
 3bd72b0:      	je	0x3bd72b7 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x257>
 3bd72b2:      	callq	0x828a640 <free@plt>
 3bd72b7:      	movq	%rbx, %rax
 3bd72ba:      	addq	$0x58, %rsp
 3bd72be:      	popq	%rbx
 3bd72bf:      	popq	%r12
 3bd72c1:      	popq	%r13
 3bd72c3:      	popq	%r14
 3bd72c5:      	popq	%r15
 3bd72c7:      	popq	%rbp
 3bd72c8:      	retq
 3bd72c9:      	movq	%r15, %r12
 3bd72cc:      	jmp	0x3bd730a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2aa>
 3bd72ce:      	nop
 3bd72d0:      	movq	%r12, %rdx
 3bd72d3:      	subq	%r15, %rdx
 3bd72d6:      	movq	%rdx, %rax
 3bd72d9:      	sarq	$0x3, %rax
 3bd72dd:      	cmpq	$0x2, %rax
 3bd72e1:      	jl	0x3bd7343 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2e3>
 3bd72e3:      	shlq	$0x3, %rax
 3bd72e7:      	subq	%rax, %rdi
 3bd72ea:      	addq	$0x10, %rdi
 3bd72ee:      	movq	%r15, %rsi
 3bd72f1:      	callq	0x828abc0 <memmove@plt>
 3bd72f6:      	movq	%r15, %rax
 3bd72f9:      	movq	%r13, (%rax)
 3bd72fc:      	leaq	0x8(%r12), %rbx
 3bd7301:      	cmpq	%rbp, %rbx
 3bd7304:      	je	0x3bd721a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1ba>
 3bd730a:      	movq	%r12, %rdi
 3bd730d:      	movq	%rbx, %r12
 3bd7310:      	movq	(%rbx), %r13
 3bd7313:      	movq	(%r15), %rsi
 3bd7316:      	movq	0x8(%r13), %rcx
 3bd731a:      	cmpq	0x8(%rsi), %rcx
 3bd731e:      	jb	0x3bd72d0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x270>
 3bd7320:      	movq	(%rdi), %rdx
 3bd7323:      	movq	%r12, %rax
 3bd7326:      	cmpq	0x8(%rdx), %rcx
 3bd732a:      	jae	0x3bd72f9 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x299>
 3bd732c:      	movq	%r12, %rax
 3bd732f:      	nop
 3bd7330:      	movq	%rdx, (%rax)
 3bd7333:      	movq	-0x10(%rax), %rdx
 3bd7337:      	addq	$-0x8, %rax
 3bd733b:      	cmpq	0x8(%rdx), %rcx
 3bd733f:      	jb	0x3bd7330 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2d0>
 3bd7341:      	jmp	0x3bd72f9 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x299>
 3bd7343:      	movq	%r15, %rax
 3bd7346:      	cmpq	$0x8, %rdx
 3bd734a:      	jne	0x3bd72f9 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x299>
 3bd734c:      	movq	%rsi, 0x8(%rdi)
 3bd7350:      	jmp	0x3bd72f6 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x296>
 3bd7352:      	movq	%rdx, 0x8(%rcx)
 3bd7356:      	nopw	%cs:(%rax,%rax)
 3bd7360:      	movq	%r15, %rcx
 3bd7363:      	movq	%r13, (%rcx)
 3bd7366:      	addq	$0x8, %rbp
 3bd736a:      	addq	$0x8, %r12
 3bd736e:      	cmpq	$0x80, %rbp
 3bd7375:      	je	0x3bd73d3 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x373>
 3bd7377:      	movq	%r14, %rcx
 3bd737a:      	leaq	(%r15,%rbp), %r14
 3bd737e:      	movq	(%r15,%rbp), %r13
 3bd7382:      	movq	(%r15), %rdx
 3bd7385:      	movq	0x8(%r13), %rax
 3bd7389:      	cmpq	0x8(%rdx), %rax
 3bd738d:      	jae	0x3bd73b0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x350>
 3bd738f:      	cmpq	$0x9, %rbp
 3bd7393:      	jb	0x3bd7352 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2f2>
 3bd7395:      	movq	%rbx, %rdi
 3bd7398:      	movq	%r15, %rsi
 3bd739b:      	movq	%rbp, %rdx
 3bd739e:      	callq	0x828abc0 <memmove@plt>
 3bd73a3:      	jmp	0x3bd7360 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x300>
 3bd73a5:      	nopw	%cs:(%rax,%rax)
 3bd73af:      	nop
 3bd73b0:      	movq	(%rcx), %rdx
 3bd73b3:      	movq	%r14, %rcx
 3bd73b6:      	cmpq	0x8(%rdx), %rax
 3bd73ba:      	jae	0x3bd7363 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x303>
 3bd73bc:      	movq	%r12, %rcx
 3bd73bf:      	nop
 3bd73c0:      	movq	%rdx, (%rcx)
 3bd73c3:      	movq	-0x10(%rcx), %rdx
 3bd73c7:      	addq	$-0x8, %rcx
 3bd73cb:      	cmpq	0x8(%rdx), %rax
 3bd73cf:      	jb	0x3bd73c0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x360>
 3bd73d1:      	jmp	0x3bd7363 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x303>
 3bd73d3:      	subq	$-0x80, %r15
 3bd73d7:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd73e1:      	movq	0x8(%rsp), %rdi
 3bd73e6:      	jmp	0x3bd7400 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x3a0>
 3bd73e8:      	nopl	(%rax,%rax)
 3bd73f0:      	movq	%rax, (%rsi)
 3bd73f3:      	addq	$0x8, %r15
 3bd73f7:      	cmpq	%rdi, %r15
 3bd73fa:      	je	0x3bd721a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1ba>
 3bd7400:      	movq	-0x8(%r15), %rcx
 3bd7404:      	movq	(%r15), %rax
 3bd7407:      	movq	0x8(%rax), %rdx
 3bd740b:      	movq	%r15, %rsi
 3bd740e:      	cmpq	0x8(%rcx), %rdx
 3bd7412:      	jae	0x3bd73f0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x390>
 3bd7414:      	movq	%r15, %rsi
 3bd7417:      	nopw	(%rax,%rax)
 3bd7420:      	movq	%rcx, (%rsi)
 3bd7423:      	movq	-0x10(%rsi), %rcx
 3bd7427:      	addq	$-0x8, %rsi
 3bd742b:      	cmpq	0x8(%rcx), %rdx
 3bd742f:      	jb	0x3bd7420 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x3c0>
 3bd7431:      	jmp	0x3bd73f0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x390>
