
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000006926000 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE>:
 6926000:      	pushq	%rbp
 6926001:      	pushq	%r15
 6926003:      	pushq	%r14
 6926005:      	pushq	%r13
 6926007:      	pushq	%r12
 6926009:      	pushq	%rbx
 692600a:      	subq	$0x128, %rsp            # imm = 0x128
 6926011:      	movq	%rdi, %r15
 6926014:      	leaq	0x80(%rsp), %rax
 692601c:      	movq	%rax, 0x68(%rsp)
 6926021:      	leaq	0x70(%rsp), %rbx
 6926026:      	movq	$0x4, 0x70(%rsp)
 692602f:      	leaq	0x74(%rsp), %r14
 6926034:      	movl	$0x0, 0x78(%rsp)
 692603c:      	movb	$0x1, 0x7c(%rsp)
 6926041:      	leaq	0x68(%rsp), %rdx
 6926046:      	callq	0x69264e0 <_ZL12checkNoThrowRN5clang4SemaEPKNS_4StmtERN4llvm15SmallPtrSetImplIPKNS_4DeclEEE>
 692604b:      	cmpb	$0x0, 0x7c(%rsp)
 6926050:      	cmoveq	%rbx, %r14
 6926054:      	movq	0x68(%rsp), %rbx
 6926059:      	movl	(%r14), %eax
 692605c:      	leaq	(%rbx,%rax,8), %r12
 6926060:      	testq	%rax, %rax
 6926063:      	je	0x6926083 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x83>
 6926065:      	shlq	$0x3, %rax
 6926069:      	nopl	(%rax)
 6926070:      	cmpq	$-0x2, (%rbx)
 6926074:      	jb	0x6926083 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x83>
 6926076:      	addq	$0x8, %rbx
 692607a:      	addq	$-0x8, %rax
 692607e:      	jne	0x6926070 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x70>
 6926080:      	movq	%r12, %rbx
 6926083:      	leaq	0x38(%rsp), %rbp
 6926088:      	movq	%rbp, 0x28(%rsp)
 692608d:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 6926097:      	movq	%rax, 0x30(%rsp)
 692609c:      	cmpq	%r12, %rbx
 692609f:      	je	0x69260ff <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xff>
 69260a1:      	xorl	%r14d, %r14d
 69260a4:      	movq	%rbx, %rax
 69260a7:      	jmp	0x69260b9 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb9>
 69260a9:      	nopl	(%rax)
 69260b0:      	leaq	0x1(%rcx), %r14
 69260b4:      	cmpq	%r12, %rax
 69260b7:      	je	0x69260d1 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xd1>
 69260b9:      	movq	%r14, %rcx
 69260bc:      	nopl	(%rax)
 69260c0:      	addq	$0x8, %rax
 69260c4:      	cmpq	%r12, %rax
 69260c7:      	je	0x69260b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb0>
 69260c9:      	cmpq	$-0x2, (%rax)
 69260cd:      	jae	0x69260c0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xc0>
 69260cf:      	jmp	0x69260b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb0>
 69260d1:      	movq	%r15, 0x58(%rsp)
 69260d6:      	cmpq	$0x4, %rcx
 69260da:      	jb	0x6926108 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x108>
 69260dc:      	leaq	0x28(%rsp), %rdi
 69260e1:      	movl	$0x8, %ecx
 69260e6:      	movq	%rbp, %rsi
 69260e9:      	movq	%r14, %rdx
 69260ec:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 69260f1:      	movl	0x30(%rsp), %eax
 69260f5:      	movq	0x28(%rsp), %rbp
 69260fa:      	movl	%eax, %r13d
 69260fd:      	jmp	0x692610d <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x10d>
 69260ff:      	movl	0x74(%rsp), %ebx
 6926103:      	jmp	0x6926228 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926108:      	xorl	%eax, %eax
 692610a:      	xorl	%r13d, %r13d
 692610d:      	leaq	(%rbp,%rax,8), %rax
 6926112:      	jmp	0x6926129 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x129>
 6926114:      	nopw	%cs:(%rax,%rax)
 692611e:      	nop
 6926120:      	addq	$0x8, %rax
 6926124:      	cmpq	%r12, %rbx
 6926127:      	je	0x6926141 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x141>
 6926129:      	movq	(%rbx), %rcx
 692612c:      	movq	%rcx, (%rax)
 692612f:      	nop
 6926130:      	addq	$0x8, %rbx
 6926134:      	cmpq	%r12, %rbx
 6926137:      	je	0x6926120 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x120>
 6926139:      	cmpq	$-0x2, (%rbx)
 692613d:      	jae	0x6926130 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x130>
 692613f:      	jmp	0x6926120 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x120>
 6926141:      	addl	%r14d, %r13d
 6926144:      	movl	%r13d, 0x30(%rsp)
 6926149:      	je	0x6926212 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x212>
 692614f:      	leaq	(%rbp,%r13,8), %rsi
 6926154:      	bsrq	%r13, %rdx
 6926158:      	xorl	$0x3f, %edx
 692615b:      	addl	%edx, %edx
 692615d:      	xorq	$0x7e, %rdx
 6926161:      	movq	%rbp, %rdi
 6926164:      	movq	%rsi, 0x20(%rsp)
 6926169:      	callq	0x692f080 <_ZSt16__introsort_loopIPPKN5clang4DeclElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_4Sema24checkFinalSuspendNoThrowEPKNS0_4StmtEE3$_0EEEvT_SE_T0_T1_>
 692616e:      	leaq	0x8(%rbp), %r14
 6926172:      	cmpl	$0x11, %r13d
 6926176:      	movq	%rbp, (%rsp)
 692617a:      	jb	0x6926193 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x193>
 692617c:      	movq	%rbp, %rax
 692617f:      	movl	$0x8, %ebp
 6926184:      	movq	%r14, 0x60(%rsp)
 6926189:      	movq	%r14, 0x18(%rsp)
 692618e:      	jmp	0x6926390 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x390>
 6926193:      	cmpl	$0x1, %r13d
 6926197:      	jne	0x6926250 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x250>
 692619d:      	movl	0x30(%rsp), %r14d
 69261a2:      	movq	0x28(%rsp), %rbp
 69261a7:      	testq	%r14, %r14
 69261aa:      	je	0x6926212 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x212>
 69261ac:      	shlq	$0x3, %r14
 69261b0:      	movq	0x58(%rsp), %r12
 69261b5:      	addq	$0x8, %r12
 69261b9:      	xorl	%r15d, %r15d
 69261bc:      	leaq	0xa0(%rsp), %rbx
 69261c4:      	leaq	0x38(%rsp), %r13
 69261c9:      	nopl	(%rax)
 69261d0:      	movq	(%rbp,%r15), %rdi
 69261d5:      	movq	(%rdi), %rax
 69261d8:      	callq	*0x10(%rax)
 69261db:      	shrq	$0x20, %rax
 69261df:      	movq	%rbx, %rdi
 69261e2:      	movq	%r12, %rsi
 69261e5:      	movl	%eax, %edx
 69261e7:      	movl	$0x171f, %ecx           # imm = 0x171F
 69261ec:      	callq	0x67cf630 <_ZN5clang8SemaBase4DiagENS_14SourceLocationEj>
 69261f1:      	movq	%rbx, %rdi
 69261f4:      	callq	0x677c910 <_ZN5clang8SemaBase21SemaDiagnosticBuilderD2Ev>
 69261f9:      	addq	$0x8, %r15
 69261fd:      	cmpq	%r15, %r14
 6926200:      	jne	0x69261d0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x1d0>
 6926202:      	movq	0x28(%rsp), %rbp
 6926207:      	movl	0x74(%rsp), %ebx
 692620b:      	cmpq	%r13, %rbp
 692620e:      	jne	0x6926220 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x220>
 6926210:      	jmp	0x6926228 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926212:      	leaq	0x38(%rsp), %r13
 6926217:      	movl	0x74(%rsp), %ebx
 692621b:      	cmpq	%r13, %rbp
 692621e:      	je	0x6926228 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926220:      	movq	%rbp, %rdi
 6926223:      	callq	0x828a6d0 <free@plt>
 6926228:      	cmpb	$0x0, 0x7c(%rsp)
 692622d:      	jne	0x6926239 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x239>
 692622f:      	movq	0x68(%rsp), %rdi
 6926234:      	callq	0x828a6d0 <free@plt>
 6926239:      	testl	%ebx, %ebx
 692623b:      	sete	%al
 692623e:      	addq	$0x128, %rsp            # imm = 0x128
 6926245:      	popq	%rbx
 6926246:      	popq	%r12
 6926248:      	popq	%r13
 692624a:      	popq	%r14
 692624c:      	popq	%r15
 692624e:      	popq	%rbp
 692624f:      	retq
 6926250:      	movq	%rbp, %r12
 6926253:      	jmp	0x69262ad <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x2ad>
 6926255:      	nopw	%cs:(%rax,%rax)
 692625f:      	nop
 6926260:      	movq	0x10(%rsp), %rdi
 6926265:      	movq	%r14, %rdx
 6926268:      	subq	%rbx, %rdx
 692626b:      	movq	%rdx, %rax
 692626e:      	sarq	$0x3, %rax
 6926272:      	cmpq	$0x2, %rax
 6926276:      	movq	%r14, %r12
 6926279:      	jl	0x6926341 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x341>
 692627f:      	shlq	$0x3, %rax
 6926283:      	subq	%rax, %rdi
 6926286:      	addq	$0x10, %rdi
 692628a:      	movq	%rbx, %rsi
 692628d:      	callq	0x828ac50 <memmove@plt>
 6926292:      	movq	%rbx, %rbp
 6926295:      	movq	%r13, (%rbp)
 6926299:      	leaq	0x8(%r12), %r14
 692629e:      	cmpq	0x20(%rsp), %r14
 69262a3:      	movq	(%rsp), %rbp
 69262a7:      	je	0x692619d <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x19d>
 69262ad:      	movq	%r12, 0x10(%rsp)
 69262b2:      	movq	(%r14), %r13
 69262b5:      	movq	%rbp, %rbx
 69262b8:      	movq	(%rbp), %rbp
 69262bc:      	movq	(%r13), %r15
 69262c0:      	movq	%r13, %rdi
 69262c3:      	callq	*0x10(%r15)
 69262c7:      	movq	%rax, %r12
 69262ca:      	shrq	$0x20, %r12
 69262ce:      	movq	(%rbp), %rax
 69262d2:      	movq	%rbp, 0x8(%rsp)
 69262d7:      	movq	%rbp, %rdi
 69262da:      	callq	*0x10(%rax)
 69262dd:      	shrq	$0x20, %rax
 69262e1:      	cmpq	%rax, %r12
 69262e4:      	jb	0x6926260 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x260>
 69262ea:      	movq	0x10(%rsp), %rax
 69262ef:      	movq	(%rax), %rbx
 69262f2:      	movq	(%rbx), %rax
 69262f5:      	movq	%rbx, %rdi
 69262f8:      	callq	*0x10(%rax)
 69262fb:      	shrq	$0x20, %rax
 69262ff:      	movq	%r14, %rbp
 6926302:      	cmpl	%eax, %r12d
 6926305:      	movq	%r14, %r12
 6926308:      	jae	0x6926295 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 692630a:      	movq	%r12, %rbp
 692630d:      	nopl	(%rax)
 6926310:      	movq	%rbx, (%rbp)
 6926314:      	movq	-0x10(%rbp), %rbx
 6926318:      	movq	%r13, %rdi
 692631b:      	callq	*0x10(%r15)
 692631f:      	movq	%rax, %r14
 6926322:      	shrq	$0x20, %r14
 6926326:      	movq	(%rbx), %rax
 6926329:      	movq	%rbx, %rdi
 692632c:      	callq	*0x10(%rax)
 692632f:      	shrq	$0x20, %rax
 6926333:      	addq	$-0x8, %rbp
 6926337:      	cmpl	%eax, %r14d
 692633a:      	jb	0x6926310 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x310>
 692633c:      	jmp	0x6926295 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 6926341:      	movq	%rbx, %rbp
 6926344:      	cmpq	$0x8, %rdx
 6926348:      	jne	0x6926295 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 692634e:      	movq	0x8(%rsp), %rax
 6926353:      	movq	%rax, 0x8(%rdi)
 6926357:      	movq	(%rsp), %rbp
 692635b:      	jmp	0x6926295 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 6926360:      	movq	%rbx, 0x8(%rax)
 6926364:      	movq	(%rsp), %r13
 6926368:      	nopl	(%rax,%rax)
 6926370:      	movq	%r14, (%r13)
 6926374:      	addq	$0x8, %rbp
 6926378:      	addq	$0x8, 0x18(%rsp)
 692637e:      	cmpq	$0x80, %rbp
 6926385:      	movq	0x10(%rsp), %rax
 692638a:      	je	0x6926451 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x451>
 6926390:      	movq	%rax, 0x8(%rsp)
 6926395:      	movq	(%rsp), %rax
 6926399:      	leaq	(%rax,%rbp), %r13
 692639d:      	movq	(%rax,%rbp), %r14
 69263a1:      	movq	(%rax), %rbx
 69263a4:      	movq	(%r14), %r15
 69263a7:      	movq	%r14, %rdi
 69263aa:      	callq	*0x10(%r15)
 69263ae:      	movq	%rax, %r12
 69263b1:      	shrq	$0x20, %r12
 69263b5:      	movq	(%rbx), %rax
 69263b8:      	movq	%rbx, %rdi
 69263bb:      	callq	*0x10(%rax)
 69263be:      	shrq	$0x20, %rax
 69263c2:      	cmpq	%rax, %r12
 69263c5:      	movq	%r13, 0x10(%rsp)
 69263ca:      	jae	0x69263f0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x3f0>
 69263cc:      	movq	0x8(%rsp), %rax
 69263d1:      	cmpq	$0x9, %rbp
 69263d5:      	jb	0x6926360 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x360>
 69263d7:      	movq	0x60(%rsp), %rdi
 69263dc:      	movq	(%rsp), %r13
 69263e0:      	movq	%r13, %rsi
 69263e3:      	movq	%rbp, %rdx
 69263e6:      	callq	0x828ac50 <memmove@plt>
 69263eb:      	jmp	0x6926370 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 69263ed:      	nopl	(%rax)
 69263f0:      	movq	0x8(%rsp), %rax
 69263f5:      	movq	(%rax), %rbx
 69263f8:      	movq	(%rbx), %rax
 69263fb:      	movq	%rbx, %rdi
 69263fe:      	callq	*0x10(%rax)
 6926401:      	shrq	$0x20, %rax
 6926405:      	cmpl	%eax, %r12d
 6926408:      	jae	0x6926370 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 692640e:      	movq	0x18(%rsp), %r13
 6926413:      	nopw	%cs:(%rax,%rax)
 692641d:      	nopl	(%rax)
 6926420:      	movq	%rbx, (%r13)
 6926424:      	movq	-0x10(%r13), %rbx
 6926428:      	movq	%r14, %rdi
 692642b:      	callq	*0x10(%r15)
 692642f:      	movq	%rax, %r12
 6926432:      	shrq	$0x20, %r12
 6926436:      	movq	(%rbx), %rax
 6926439:      	movq	%rbx, %rdi
 692643c:      	callq	*0x10(%rax)
 692643f:      	shrq	$0x20, %rax
 6926443:      	addq	$-0x8, %r13
 6926447:      	cmpl	%eax, %r12d
 692644a:      	jb	0x6926420 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x420>
 692644c:      	jmp	0x6926370 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 6926451:      	movq	(%rsp), %rbp
 6926455:      	subq	$-0x80, %rbp
 6926459:      	jmp	0x6926473 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x473>
 692645b:      	nopl	(%rax,%rax)
 6926460:      	movq	%r14, (%r12)
 6926464:      	addq	$0x8, %rbp
 6926468:      	cmpq	0x20(%rsp), %rbp
 692646d:      	je	0x692619d <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x19d>
 6926473:      	movq	-0x8(%rbp), %r13
 6926477:      	movq	(%rbp), %r14
 692647b:      	movq	(%r14), %r15
 692647e:      	movq	%r14, %rdi
 6926481:      	callq	*0x10(%r15)
 6926485:      	movq	%rax, %rbx
 6926488:      	shrq	$0x20, %rbx
 692648c:      	movq	(%r13), %rax
 6926490:      	movq	%r13, %rdi
 6926493:      	callq	*0x10(%rax)
 6926496:      	shrq	$0x20, %rax
 692649a:      	movq	%rbp, %r12
 692649d:      	cmpl	%eax, %ebx
 692649f:      	jae	0x6926460 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x460>
 69264a1:      	movq	%rbp, %r12
 69264a4:      	nopw	%cs:(%rax,%rax)
 69264ae:      	nop
 69264b0:      	movq	%r13, (%r12)
 69264b4:      	movq	-0x10(%r12), %r13
 69264b9:      	movq	%r14, %rdi
 69264bc:      	callq	*0x10(%r15)
 69264c0:      	movq	%rax, %rbx
 69264c3:      	shrq	$0x20, %rbx
 69264c7:      	movq	(%r13), %rax
 69264cb:      	movq	%r13, %rdi
 69264ce:      	callq	*0x10(%rax)
 69264d1:      	shrq	$0x20, %rax
 69264d5:      	addq	$-0x8, %r12
 69264d9:      	cmpl	%eax, %ebx
 69264db:      	jb	0x69264b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x4b0>
 69264dd:      	jmp	0x6926460 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x460>
