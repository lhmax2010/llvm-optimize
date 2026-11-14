
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000006925f50 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE>:
 6925f50:      	pushq	%rbp
 6925f51:      	pushq	%r15
 6925f53:      	pushq	%r14
 6925f55:      	pushq	%r13
 6925f57:      	pushq	%r12
 6925f59:      	pushq	%rbx
 6925f5a:      	subq	$0x128, %rsp            # imm = 0x128
 6925f61:      	movq	%rdi, %r15
 6925f64:      	leaq	0x80(%rsp), %rax
 6925f6c:      	movq	%rax, 0x68(%rsp)
 6925f71:      	leaq	0x70(%rsp), %rbx
 6925f76:      	movq	$0x4, 0x70(%rsp)
 6925f7f:      	leaq	0x74(%rsp), %r14
 6925f84:      	movl	$0x0, 0x78(%rsp)
 6925f8c:      	movb	$0x1, 0x7c(%rsp)
 6925f91:      	leaq	0x68(%rsp), %rdx
 6925f96:      	callq	0x6926430 <_ZL12checkNoThrowRN5clang4SemaEPKNS_4StmtERN4llvm15SmallPtrSetImplIPKNS_4DeclEEE>
 6925f9b:      	cmpb	$0x0, 0x7c(%rsp)
 6925fa0:      	cmoveq	%rbx, %r14
 6925fa4:      	movq	0x68(%rsp), %rbx
 6925fa9:      	movl	(%r14), %eax
 6925fac:      	leaq	(%rbx,%rax,8), %r12
 6925fb0:      	testq	%rax, %rax
 6925fb3:      	je	0x6925fd3 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x83>
 6925fb5:      	shlq	$0x3, %rax
 6925fb9:      	nopl	(%rax)
 6925fc0:      	cmpq	$-0x2, (%rbx)
 6925fc4:      	jb	0x6925fd3 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x83>
 6925fc6:      	addq	$0x8, %rbx
 6925fca:      	addq	$-0x8, %rax
 6925fce:      	jne	0x6925fc0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x70>
 6925fd0:      	movq	%r12, %rbx
 6925fd3:      	leaq	0x38(%rsp), %rbp
 6925fd8:      	movq	%rbp, 0x28(%rsp)
 6925fdd:      	movabsq	$0x400000000, %rax      # imm = 0x400000000
 6925fe7:      	movq	%rax, 0x30(%rsp)
 6925fec:      	cmpq	%r12, %rbx
 6925fef:      	je	0x692604f <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xff>
 6925ff1:      	xorl	%r14d, %r14d
 6925ff4:      	movq	%rbx, %rax
 6925ff7:      	jmp	0x6926009 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb9>
 6925ff9:      	nopl	(%rax)
 6926000:      	leaq	0x1(%rcx), %r14
 6926004:      	cmpq	%r12, %rax
 6926007:      	je	0x6926021 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xd1>
 6926009:      	movq	%r14, %rcx
 692600c:      	nopl	(%rax)
 6926010:      	addq	$0x8, %rax
 6926014:      	cmpq	%r12, %rax
 6926017:      	je	0x6926000 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb0>
 6926019:      	cmpq	$-0x2, (%rax)
 692601d:      	jae	0x6926010 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xc0>
 692601f:      	jmp	0x6926000 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0xb0>
 6926021:      	movq	%r15, 0x58(%rsp)
 6926026:      	cmpq	$0x4, %rcx
 692602a:      	jb	0x6926058 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x108>
 692602c:      	leaq	0x28(%rsp), %rdi
 6926031:      	movl	$0x8, %ecx
 6926036:      	movq	%rbp, %rsi
 6926039:      	movq	%r14, %rdx
 692603c:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 6926041:      	movl	0x30(%rsp), %eax
 6926045:      	movq	0x28(%rsp), %rbp
 692604a:      	movl	%eax, %r13d
 692604d:      	jmp	0x692605d <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x10d>
 692604f:      	movl	0x74(%rsp), %ebx
 6926053:      	jmp	0x6926178 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926058:      	xorl	%eax, %eax
 692605a:      	xorl	%r13d, %r13d
 692605d:      	leaq	(%rbp,%rax,8), %rax
 6926062:      	jmp	0x6926079 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x129>
 6926064:      	nopw	%cs:(%rax,%rax)
 692606e:      	nop
 6926070:      	addq	$0x8, %rax
 6926074:      	cmpq	%r12, %rbx
 6926077:      	je	0x6926091 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x141>
 6926079:      	movq	(%rbx), %rcx
 692607c:      	movq	%rcx, (%rax)
 692607f:      	nop
 6926080:      	addq	$0x8, %rbx
 6926084:      	cmpq	%r12, %rbx
 6926087:      	je	0x6926070 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x120>
 6926089:      	cmpq	$-0x2, (%rbx)
 692608d:      	jae	0x6926080 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x130>
 692608f:      	jmp	0x6926070 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x120>
 6926091:      	addl	%r14d, %r13d
 6926094:      	movl	%r13d, 0x30(%rsp)
 6926099:      	je	0x6926162 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x212>
 692609f:      	leaq	(%rbp,%r13,8), %rsi
 69260a4:      	bsrq	%r13, %rdx
 69260a8:      	xorl	$0x3f, %edx
 69260ab:      	addl	%edx, %edx
 69260ad:      	xorq	$0x7e, %rdx
 69260b1:      	movq	%rbp, %rdi
 69260b4:      	movq	%rsi, 0x20(%rsp)
 69260b9:      	callq	0x692efd0 <_ZSt16__introsort_loopIPPKN5clang4DeclElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_4Sema24checkFinalSuspendNoThrowEPKNS0_4StmtEE3$_0EEEvT_SE_T0_T1_>
 69260be:      	leaq	0x8(%rbp), %r14
 69260c2:      	cmpl	$0x11, %r13d
 69260c6:      	movq	%rbp, (%rsp)
 69260ca:      	jb	0x69260e7 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x197>
 69260cc:      	movq	%r14, 0x60(%rsp)
 69260d1:      	leaq	0x8(%rbp), %rax
 69260d5:      	movq	%rax, 0x18(%rsp)
 69260da:      	movq	%rbp, %rax
 69260dd:      	movl	$0x8, %ebp
 69260e2:      	jmp	0x69262e0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x390>
 69260e7:      	cmpl	$0x1, %r13d
 69260eb:      	jne	0x69261a0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x250>
 69260f1:      	movl	0x30(%rsp), %r14d
 69260f6:      	movq	0x28(%rsp), %rbp
 69260fb:      	testq	%r14, %r14
 69260fe:      	je	0x6926162 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x212>
 6926100:      	shlq	$0x3, %r14
 6926104:      	movq	0x58(%rsp), %r12
 6926109:      	addq	$0x8, %r12
 692610d:      	xorl	%r15d, %r15d
 6926110:      	leaq	0xa0(%rsp), %rbx
 6926118:      	leaq	0x38(%rsp), %r13
 692611d:      	nopl	(%rax)
 6926120:      	movq	(%rbp,%r15), %rdi
 6926125:      	movq	(%rdi), %rax
 6926128:      	callq	*0x10(%rax)
 692612b:      	shrq	$0x20, %rax
 692612f:      	movq	%rbx, %rdi
 6926132:      	movq	%r12, %rsi
 6926135:      	movl	%eax, %edx
 6926137:      	movl	$0x171f, %ecx           # imm = 0x171F
 692613c:      	callq	0x67cf580 <_ZN5clang8SemaBase4DiagENS_14SourceLocationEj>
 6926141:      	movq	%rbx, %rdi
 6926144:      	callq	0x677c860 <_ZN5clang8SemaBase21SemaDiagnosticBuilderD2Ev>
 6926149:      	addq	$0x8, %r15
 692614d:      	cmpq	%r15, %r14
 6926150:      	jne	0x6926120 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x1d0>
 6926152:      	movq	0x28(%rsp), %rbp
 6926157:      	movl	0x74(%rsp), %ebx
 692615b:      	cmpq	%r13, %rbp
 692615e:      	jne	0x6926170 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x220>
 6926160:      	jmp	0x6926178 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926162:      	leaq	0x38(%rsp), %r13
 6926167:      	movl	0x74(%rsp), %ebx
 692616b:      	cmpq	%r13, %rbp
 692616e:      	je	0x6926178 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x228>
 6926170:      	movq	%rbp, %rdi
 6926173:      	callq	0x828a640 <free@plt>
 6926178:      	cmpb	$0x0, 0x7c(%rsp)
 692617d:      	jne	0x6926189 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x239>
 692617f:      	movq	0x68(%rsp), %rdi
 6926184:      	callq	0x828a640 <free@plt>
 6926189:      	testl	%ebx, %ebx
 692618b:      	sete	%al
 692618e:      	addq	$0x128, %rsp            # imm = 0x128
 6926195:      	popq	%rbx
 6926196:      	popq	%r12
 6926198:      	popq	%r13
 692619a:      	popq	%r14
 692619c:      	popq	%r15
 692619e:      	popq	%rbp
 692619f:      	retq
 69261a0:      	movq	%rbp, %r12
 69261a3:      	jmp	0x69261fd <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x2ad>
 69261a5:      	nopw	%cs:(%rax,%rax)
 69261af:      	nop
 69261b0:      	movq	0x10(%rsp), %rdi
 69261b5:      	movq	%r14, %rdx
 69261b8:      	subq	%rbx, %rdx
 69261bb:      	movq	%rdx, %rax
 69261be:      	sarq	$0x3, %rax
 69261c2:      	cmpq	$0x2, %rax
 69261c6:      	movq	%r14, %r12
 69261c9:      	jl	0x6926291 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x341>
 69261cf:      	shlq	$0x3, %rax
 69261d3:      	subq	%rax, %rdi
 69261d6:      	addq	$0x10, %rdi
 69261da:      	movq	%rbx, %rsi
 69261dd:      	callq	0x828abc0 <memmove@plt>
 69261e2:      	movq	%rbx, %rbp
 69261e5:      	movq	%r13, (%rbp)
 69261e9:      	leaq	0x8(%r12), %r14
 69261ee:      	cmpq	0x20(%rsp), %r14
 69261f3:      	movq	(%rsp), %rbp
 69261f7:      	je	0x69260f1 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x1a1>
 69261fd:      	movq	%r12, 0x10(%rsp)
 6926202:      	movq	(%r14), %r13
 6926205:      	movq	%rbp, %rbx
 6926208:      	movq	(%rbp), %rbp
 692620c:      	movq	(%r13), %r15
 6926210:      	movq	%r13, %rdi
 6926213:      	callq	*0x10(%r15)
 6926217:      	movq	%rax, %r12
 692621a:      	shrq	$0x20, %r12
 692621e:      	movq	(%rbp), %rax
 6926222:      	movq	%rbp, 0x8(%rsp)
 6926227:      	movq	%rbp, %rdi
 692622a:      	callq	*0x10(%rax)
 692622d:      	shrq	$0x20, %rax
 6926231:      	cmpq	%rax, %r12
 6926234:      	jb	0x69261b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x260>
 692623a:      	movq	0x10(%rsp), %rax
 692623f:      	movq	(%rax), %rbx
 6926242:      	movq	(%rbx), %rax
 6926245:      	movq	%rbx, %rdi
 6926248:      	callq	*0x10(%rax)
 692624b:      	shrq	$0x20, %rax
 692624f:      	movq	%r14, %rbp
 6926252:      	cmpl	%eax, %r12d
 6926255:      	movq	%r14, %r12
 6926258:      	jae	0x69261e5 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 692625a:      	movq	%r12, %rbp
 692625d:      	nopl	(%rax)
 6926260:      	movq	%rbx, (%rbp)
 6926264:      	movq	-0x10(%rbp), %rbx
 6926268:      	movq	%r13, %rdi
 692626b:      	callq	*0x10(%r15)
 692626f:      	movq	%rax, %r14
 6926272:      	shrq	$0x20, %r14
 6926276:      	movq	(%rbx), %rax
 6926279:      	movq	%rbx, %rdi
 692627c:      	callq	*0x10(%rax)
 692627f:      	shrq	$0x20, %rax
 6926283:      	addq	$-0x8, %rbp
 6926287:      	cmpl	%eax, %r14d
 692628a:      	jb	0x6926260 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x310>
 692628c:      	jmp	0x69261e5 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 6926291:      	movq	%rbx, %rbp
 6926294:      	cmpq	$0x8, %rdx
 6926298:      	jne	0x69261e5 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 692629e:      	movq	0x8(%rsp), %rax
 69262a3:      	movq	%rax, 0x8(%rdi)
 69262a7:      	movq	(%rsp), %rbp
 69262ab:      	jmp	0x69261e5 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x295>
 69262b0:      	movq	%rbx, 0x8(%rax)
 69262b4:      	movq	(%rsp), %r13
 69262b8:      	nopl	(%rax,%rax)
 69262c0:      	movq	%r14, (%r13)
 69262c4:      	addq	$0x8, %rbp
 69262c8:      	addq	$0x8, 0x18(%rsp)
 69262ce:      	cmpq	$0x80, %rbp
 69262d5:      	movq	0x10(%rsp), %rax
 69262da:      	je	0x69263a1 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x451>
 69262e0:      	movq	%rax, 0x8(%rsp)
 69262e5:      	movq	(%rsp), %rax
 69262e9:      	leaq	(%rax,%rbp), %r13
 69262ed:      	movq	(%rax,%rbp), %r14
 69262f1:      	movq	(%rax), %rbx
 69262f4:      	movq	(%r14), %r15
 69262f7:      	movq	%r14, %rdi
 69262fa:      	callq	*0x10(%r15)
 69262fe:      	movq	%rax, %r12
 6926301:      	shrq	$0x20, %r12
 6926305:      	movq	(%rbx), %rax
 6926308:      	movq	%rbx, %rdi
 692630b:      	callq	*0x10(%rax)
 692630e:      	shrq	$0x20, %rax
 6926312:      	cmpq	%rax, %r12
 6926315:      	movq	%r13, 0x10(%rsp)
 692631a:      	jae	0x6926340 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x3f0>
 692631c:      	movq	0x8(%rsp), %rax
 6926321:      	cmpq	$0x9, %rbp
 6926325:      	jb	0x69262b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x360>
 6926327:      	movq	0x60(%rsp), %rdi
 692632c:      	movq	(%rsp), %r13
 6926330:      	movq	%r13, %rsi
 6926333:      	movq	%rbp, %rdx
 6926336:      	callq	0x828abc0 <memmove@plt>
 692633b:      	jmp	0x69262c0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 692633d:      	nopl	(%rax)
 6926340:      	movq	0x8(%rsp), %rax
 6926345:      	movq	(%rax), %rbx
 6926348:      	movq	(%rbx), %rax
 692634b:      	movq	%rbx, %rdi
 692634e:      	callq	*0x10(%rax)
 6926351:      	shrq	$0x20, %rax
 6926355:      	cmpl	%eax, %r12d
 6926358:      	jae	0x69262c0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 692635e:      	movq	0x18(%rsp), %r13
 6926363:      	nopw	%cs:(%rax,%rax)
 692636d:      	nopl	(%rax)
 6926370:      	movq	%rbx, (%r13)
 6926374:      	movq	-0x10(%r13), %rbx
 6926378:      	movq	%r14, %rdi
 692637b:      	callq	*0x10(%r15)
 692637f:      	movq	%rax, %r12
 6926382:      	shrq	$0x20, %r12
 6926386:      	movq	(%rbx), %rax
 6926389:      	movq	%rbx, %rdi
 692638c:      	callq	*0x10(%rax)
 692638f:      	shrq	$0x20, %rax
 6926393:      	addq	$-0x8, %r13
 6926397:      	cmpl	%eax, %r12d
 692639a:      	jb	0x6926370 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x420>
 692639c:      	jmp	0x69262c0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x370>
 69263a1:      	movq	(%rsp), %rbp
 69263a5:      	subq	$-0x80, %rbp
 69263a9:      	jmp	0x69263c3 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x473>
 69263ab:      	nopl	(%rax,%rax)
 69263b0:      	movq	%r14, (%r12)
 69263b4:      	addq	$0x8, %rbp
 69263b8:      	cmpq	0x20(%rsp), %rbp
 69263bd:      	je	0x69260f1 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x1a1>
 69263c3:      	movq	-0x8(%rbp), %r13
 69263c7:      	movq	(%rbp), %r14
 69263cb:      	movq	(%r14), %r15
 69263ce:      	movq	%r14, %rdi
 69263d1:      	callq	*0x10(%r15)
 69263d5:      	movq	%rax, %rbx
 69263d8:      	shrq	$0x20, %rbx
 69263dc:      	movq	(%r13), %rax
 69263e0:      	movq	%r13, %rdi
 69263e3:      	callq	*0x10(%rax)
 69263e6:      	shrq	$0x20, %rax
 69263ea:      	movq	%rbp, %r12
 69263ed:      	cmpl	%eax, %ebx
 69263ef:      	jae	0x69263b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x460>
 69263f1:      	movq	%rbp, %r12
 69263f4:      	nopw	%cs:(%rax,%rax)
 69263fe:      	nop
 6926400:      	movq	%r13, (%r12)
 6926404:      	movq	-0x10(%r12), %r13
 6926409:      	movq	%r14, %rdi
 692640c:      	callq	*0x10(%r15)
 6926410:      	movq	%rax, %rbx
 6926413:      	shrq	$0x20, %rbx
 6926417:      	movq	(%r13), %rax
 692641b:      	movq	%r13, %rdi
 692641e:      	callq	*0x10(%rax)
 6926421:      	shrq	$0x20, %rax
 6926425:      	addq	$-0x8, %r12
 6926429:      	cmpl	%eax, %ebx
 692642b:      	jb	0x6926400 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x4b0>
 692642d:      	jmp	0x69263b0 <_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE+0x460>
