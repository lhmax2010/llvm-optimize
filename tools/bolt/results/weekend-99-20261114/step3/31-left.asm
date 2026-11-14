
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003bd70f0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv>:
 3bd70f0:      	pushq	%rbp
 3bd70f1:      	pushq	%r15
 3bd70f3:      	pushq	%r14
 3bd70f5:      	pushq	%r13
 3bd70f7:      	pushq	%r12
 3bd70f9:      	pushq	%rbx
 3bd70fa:      	subq	$0x58, %rsp
 3bd70fe:      	movq	%rdi, 0x50(%rsp)
 3bd7103:      	leaq	0x20(%rsp), %rax
 3bd7108:      	movq	%rax, 0x10(%rsp)
 3bd710d:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd7117:      	movq	%r14, 0x18(%rsp)
 3bd711c:      	movl	0x10(%rsi), %edi
 3bd711f:      	leaq	0x18(%rsi), %rax
 3bd7123:      	testb	$0x1, %dil
 3bd7127:      	cmoveq	0x18(%rsi), %rax
 3bd712c:      	movl	$0x4, %ecx
 3bd7131:      	movq	%rsi, %rbx
 3bd7134:      	cmovel	0x20(%rsi), %ecx
 3bd7138:      	leaq	(,%rcx,8), %rdx
 3bd7140:      	leaq	(%rdx,%rdx,2), %rdx
 3bd7144:      	leaq	(%rax,%rdx), %r13
 3bd7148:      	movq	%r13, %rbp
 3bd714b:      	cmpl	$0x2, %edi
 3bd714e:      	jb	0x3bd717a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x8a>
 3bd7150:      	movq	%rax, %rbp
 3bd7153:      	testq	%rcx, %rcx
 3bd7156:      	je	0x3bd717a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x8a>
 3bd7158:      	movl	$0x1000, %esi           # imm = 0x1000
 3bd715d:      	movq	%rax, %rbp
 3bd7160:      	movq	(%rbp), %rdi
 3bd7164:      	orq	%rsi, %rdi
 3bd7167:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 3bd716e:      	jne	0x3bd717a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x8a>
 3bd7170:      	addq	$0x18, %rbp
 3bd7174:      	addq	$-0x18, %rdx
 3bd7178:      	jne	0x3bd7160 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x70>
 3bd717a:      	leaq	(%rcx,%rcx,2), %rcx
 3bd717e:      	leaq	(%rax,%rcx,8), %r15
 3bd7182:      	cmpq	%r15, %rbp
 3bd7185:      	je	0x3bd7299 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1a9>
 3bd718b:      	addq	$0x10, %rbx
 3bd718f:      	xorl	%r12d, %r12d
 3bd7192:      	movl	$0x1000, %r14d          # imm = 0x1000
 3bd7198:      	jmp	0x3bd71a9 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xb9>
 3bd719a:      	nopw	(%rax,%rax)
 3bd71a0:      	cmpq	%r15, %rbp
 3bd71a3:      	je	0x3bd723d <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x14d>
 3bd71a9:      	movq	0x8(%rbp), %rax
 3bd71ad:      	cmpq	$0x4, %rax
 3bd71b1:      	setb	%cl
 3bd71b4:      	movl	%eax, %edx
 3bd71b6:      	andl	$0x3, %edx
 3bd71b9:      	cmpl	$0x1, %edx
 3bd71bc:      	setne	%dl
 3bd71bf:      	orb	%cl, %dl
 3bd71c1:      	jne	0x3bd7200 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x110>
 3bd71c3:      	andq	$-0x4, %rax
 3bd71c7:      	cmpb	$0x4, (%rax)
 3bd71ca:      	jne	0x3bd7200 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x110>
 3bd71cc:      	movq	(%rbp), %rsi
 3bd71d0:      	movq	%rbx, %rdi
 3bd71d3:      	callq	0x3beb290 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPvSt4pairINS_12PointerUnionIJPNS_15MetadataAsValueEPNS_8MetadataEPNS_14DebugValueUserEEEEmELj4ENS_12DenseMapInfoIS2_vEENS_6detail12DenseMapPairIS2_SC_EEEES2_SC_SE_SH_E24lookupOrInsertIntoBucketIRKS2_JEEES3_IPSH_bEOT_DpOT0_>
 3bd71d8:      	movl	0x18(%rsp), %edx
 3bd71dc:      	cmpl	0x1c(%rsp), %edx
 3bd71e0:      	jae	0x3bd721a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x12a>
 3bd71e2:      	addq	$0x8, %rax
 3bd71e6:      	movq	0x10(%rsp), %rcx
 3bd71eb:      	movl	%edx, %edx
 3bd71ed:      	movq	%rax, (%rcx,%rdx,8)
 3bd71f1:      	movl	0x18(%rsp), %r12d
 3bd71f6:      	incl	%r12d
 3bd71f9:      	movl	%r12d, 0x18(%rsp)
 3bd71fe:      	nop
 3bd7200:      	addq	$0x18, %rbp
 3bd7204:      	cmpq	%r13, %rbp
 3bd7207:      	je	0x3bd71a0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xb0>
 3bd7209:      	movq	(%rbp), %rax
 3bd720d:      	orq	%r14, %rax
 3bd7210:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 3bd7216:      	je	0x3bd7200 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x110>
 3bd7218:      	jmp	0x3bd71a0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xb0>
 3bd721a:      	incq	%rdx
 3bd721d:      	movl	$0x8, %ecx
 3bd7222:      	leaq	0x10(%rsp), %rdi
 3bd7227:      	leaq	0x20(%rsp), %rsi
 3bd722c:      	movq	%rax, %r12
 3bd722f:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd7234:      	movq	%r12, %rax
 3bd7237:      	movl	0x18(%rsp), %edx
 3bd723b:      	jmp	0x3bd71e2 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0xf2>
 3bd723d:      	testl	%r12d, %r12d
 3bd7240:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd724a:      	je	0x3bd7299 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1a9>
 3bd724c:      	movq	0x10(%rsp), %r15
 3bd7251:      	movl	%r12d, %eax
 3bd7254:      	leaq	(%r15,%rax,8), %rbp
 3bd7258:      	bsrq	%rax, %rdx
 3bd725c:      	xorl	$0x3f, %edx
 3bd725f:      	addl	%edx, %edx
 3bd7261:      	xorq	$0x7e, %rdx
 3bd7265:      	movq	%r15, %rdi
 3bd7268:      	movq	%rbp, %rsi
 3bd726b:      	callq	0x3beb8a0 <_ZSt16__introsort_loopIPPSt4pairIN4llvm12PointerUnionIJPNS1_15MetadataAsValueEPNS1_8MetadataEPNS1_14DebugValueUserEEEEmElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS1_23ReplaceableMetadataImpl18getAllArgListUsersEvE3$_0EEEvT_SJ_T0_T1_>
 3bd7270:      	leaq	0x8(%r15), %r13
 3bd7274:      	cmpl	$0x11, %r12d
 3bd7278:      	jb	0x3bd728f <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x19f>
 3bd727a:      	movq	%rbp, 0x8(%rsp)
 3bd727f:      	movl	$0x8, %ebp
 3bd7284:      	movq	%r13, %r12
 3bd7287:      	movq	%r15, %r14
 3bd728a:      	jmp	0x3bd73f7 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x307>
 3bd728f:      	cmpl	$0x1, %r12d
 3bd7293:      	jne	0x3bd7342 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x252>
 3bd7299:      	movq	0x50(%rsp), %rbp
 3bd729e:      	leaq	0x10(%rbp), %r15
 3bd72a2:      	movq	%r15, (%rbp)
 3bd72a6:      	movq	%r14, 0x8(%rbp)
 3bd72aa:      	movq	0x10(%rsp), %rdi
 3bd72af:      	movl	0x18(%rsp), %r14d
 3bd72b4:      	leaq	0x20(%rsp), %r13
 3bd72b9:      	testq	%r14, %r14
 3bd72bc:      	je	0x3bd7326 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x236>
 3bd72be:      	shlq	$0x3, %r14
 3bd72c2:      	xorl	%eax, %eax
 3bd72c4:      	xorl	%r12d, %r12d
 3bd72c7:      	nopw	(%rax,%rax)
 3bd72d0:      	movq	(%rdi,%r12), %rcx
 3bd72d4:      	movq	(%rcx), %rbx
 3bd72d7:      	cmpl	0xc(%rbp), %eax
 3bd72da:      	jae	0x3bd72fd <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x20d>
 3bd72dc:      	andq	$-0x4, %rbx
 3bd72e0:      	movq	(%rbp), %rcx
 3bd72e4:      	movl	%eax, %eax
 3bd72e6:      	movq	%rbx, (%rcx,%rax,8)
 3bd72ea:      	movl	0x8(%rbp), %eax
 3bd72ed:      	incl	%eax
 3bd72ef:      	movl	%eax, 0x8(%rbp)
 3bd72f2:      	addq	$0x8, %r12
 3bd72f6:      	cmpq	%r12, %r14
 3bd72f9:      	jne	0x3bd72d0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1e0>
 3bd72fb:      	jmp	0x3bd7321 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x231>
 3bd72fd:      	movl	%eax, %edx
 3bd72ff:      	incq	%rdx
 3bd7302:      	movl	$0x8, %ecx
 3bd7307:      	movq	%rdi, 0x8(%rsp)
 3bd730c:      	movq	%rbp, %rdi
 3bd730f:      	movq	%r15, %rsi
 3bd7312:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 3bd7317:      	movq	0x8(%rsp), %rdi
 3bd731c:      	movl	0x8(%rbp), %eax
 3bd731f:      	jmp	0x3bd72dc <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1ec>
 3bd7321:      	movq	0x10(%rsp), %rdi
 3bd7326:      	cmpq	%r13, %rdi
 3bd7329:      	je	0x3bd7330 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x240>
 3bd732b:      	callq	0x828a6d0 <free@plt>
 3bd7330:      	movq	%rbp, %rax
 3bd7333:      	addq	$0x58, %rsp
 3bd7337:      	popq	%rbx
 3bd7338:      	popq	%r12
 3bd733a:      	popq	%r13
 3bd733c:      	popq	%r14
 3bd733e:      	popq	%r15
 3bd7340:      	popq	%rbp
 3bd7341:      	retq
 3bd7342:      	movq	%r15, %r12
 3bd7345:      	jmp	0x3bd738a <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x29a>
 3bd7347:      	nopw	(%rax,%rax)
 3bd7350:      	movq	%r12, %rdx
 3bd7353:      	subq	%r15, %rdx
 3bd7356:      	movq	%rdx, %rax
 3bd7359:      	sarq	$0x3, %rax
 3bd735d:      	cmpq	$0x2, %rax
 3bd7361:      	jl	0x3bd73c3 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2d3>
 3bd7363:      	shlq	$0x3, %rax
 3bd7367:      	subq	%rax, %rdi
 3bd736a:      	addq	$0x10, %rdi
 3bd736e:      	movq	%r15, %rsi
 3bd7371:      	callq	0x828ac50 <memmove@plt>
 3bd7376:      	movq	%r15, %rax
 3bd7379:      	movq	%r13, (%rax)
 3bd737c:      	leaq	0x8(%r12), %r13
 3bd7381:      	cmpq	%rbp, %r13
 3bd7384:      	je	0x3bd7299 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1a9>
 3bd738a:      	movq	%r12, %rdi
 3bd738d:      	movq	%r13, %r12
 3bd7390:      	movq	(%r13), %r13
 3bd7394:      	movq	(%r15), %rsi
 3bd7397:      	movq	0x8(%r13), %rcx
 3bd739b:      	cmpq	0x8(%rsi), %rcx
 3bd739f:      	jb	0x3bd7350 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x260>
 3bd73a1:      	movq	(%rdi), %rdx
 3bd73a4:      	movq	%r12, %rax
 3bd73a7:      	cmpq	0x8(%rdx), %rcx
 3bd73ab:      	jae	0x3bd7379 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x289>
 3bd73ad:      	movq	%r12, %rax
 3bd73b0:      	movq	%rdx, (%rax)
 3bd73b3:      	movq	-0x10(%rax), %rdx
 3bd73b7:      	addq	$-0x8, %rax
 3bd73bb:      	cmpq	0x8(%rdx), %rcx
 3bd73bf:      	jb	0x3bd73b0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2c0>
 3bd73c1:      	jmp	0x3bd7379 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x289>
 3bd73c3:      	movq	%r15, %rax
 3bd73c6:      	cmpq	$0x8, %rdx
 3bd73ca:      	jne	0x3bd7379 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x289>
 3bd73cc:      	movq	%rsi, 0x8(%rdi)
 3bd73d0:      	jmp	0x3bd7376 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x286>
 3bd73d2:      	movq	%rdx, 0x8(%rcx)
 3bd73d6:      	nopw	%cs:(%rax,%rax)
 3bd73e0:      	movq	%r15, %rcx
 3bd73e3:      	movq	%rbx, (%rcx)
 3bd73e6:      	addq	$0x8, %rbp
 3bd73ea:      	addq	$0x8, %r12
 3bd73ee:      	cmpq	$0x80, %rbp
 3bd73f5:      	je	0x3bd7453 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x363>
 3bd73f7:      	movq	%r14, %rcx
 3bd73fa:      	leaq	(%r15,%rbp), %r14
 3bd73fe:      	movq	(%r15,%rbp), %rbx
 3bd7402:      	movq	(%r15), %rdx
 3bd7405:      	movq	0x8(%rbx), %rax
 3bd7409:      	cmpq	0x8(%rdx), %rax
 3bd740d:      	jae	0x3bd7430 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x340>
 3bd740f:      	cmpq	$0x9, %rbp
 3bd7413:      	jb	0x3bd73d2 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2e2>
 3bd7415:      	movq	%r13, %rdi
 3bd7418:      	movq	%r15, %rsi
 3bd741b:      	movq	%rbp, %rdx
 3bd741e:      	callq	0x828ac50 <memmove@plt>
 3bd7423:      	jmp	0x3bd73e0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2f0>
 3bd7425:      	nopw	%cs:(%rax,%rax)
 3bd742f:      	nop
 3bd7430:      	movq	(%rcx), %rdx
 3bd7433:      	movq	%r14, %rcx
 3bd7436:      	cmpq	0x8(%rdx), %rax
 3bd743a:      	jae	0x3bd73e3 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2f3>
 3bd743c:      	movq	%r12, %rcx
 3bd743f:      	nop
 3bd7440:      	movq	%rdx, (%rcx)
 3bd7443:      	movq	-0x10(%rcx), %rdx
 3bd7447:      	addq	$-0x8, %rcx
 3bd744b:      	cmpq	0x8(%rdx), %rax
 3bd744f:      	jb	0x3bd7440 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x350>
 3bd7451:      	jmp	0x3bd73e3 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x2f3>
 3bd7453:      	subq	$-0x80, %r15
 3bd7457:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 3bd7461:      	movq	0x8(%rsp), %rdi
 3bd7466:      	jmp	0x3bd7480 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x390>
 3bd7468:      	nopl	(%rax,%rax)
 3bd7470:      	movq	%rax, (%rsi)
 3bd7473:      	addq	$0x8, %r15
 3bd7477:      	cmpq	%rdi, %r15
 3bd747a:      	je	0x3bd7299 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x1a9>
 3bd7480:      	movq	-0x8(%r15), %rcx
 3bd7484:      	movq	(%r15), %rax
 3bd7487:      	movq	0x8(%rax), %rdx
 3bd748b:      	movq	%r15, %rsi
 3bd748e:      	cmpq	0x8(%rcx), %rdx
 3bd7492:      	jae	0x3bd7470 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x380>
 3bd7494:      	movq	%r15, %rsi
 3bd7497:      	nopw	(%rax,%rax)
 3bd74a0:      	movq	%rcx, (%rsi)
 3bd74a3:      	movq	-0x10(%rsi), %rcx
 3bd74a7:      	addq	$-0x8, %rsi
 3bd74ab:      	cmpq	0x8(%rcx), %rdx
 3bd74af:      	jb	0x3bd74a0 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x3b0>
 3bd74b1:      	jmp	0x3bd7470 <_ZN4llvm23ReplaceableMetadataImpl18getAllArgListUsersEv+0x380>
