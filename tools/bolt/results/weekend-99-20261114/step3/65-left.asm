
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007fd6fd0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE>:
 7fd6fd0:      	pushq	%rbp
 7fd6fd1:      	pushq	%r15
 7fd6fd3:      	pushq	%r14
 7fd6fd5:      	pushq	%r13
 7fd6fd7:      	pushq	%r12
 7fd6fd9:      	pushq	%rbx
 7fd6fda:      	subq	$0x28, %rsp
 7fd6fde:      	movq	%rsi, %rcx
 7fd6fe1:      	movq	%rdi, %r14
 7fd6fe4:      	movq	(%rsi), %rax
 7fd6fe7:      	leaq	-0x7272478(%rip), %rsi  # 0xd64b76 <.L.str.64>
 7fd6fee:      	movl	$0xd, %edx
 7fd6ff3:      	movq	%rcx, 0x10(%rsp)
 7fd6ff8:      	movq	%rcx, %rdi
 7fd6ffb:      	callq	*0x110(%rax)
 7fd7001:      	movq	(%r14), %rax
 7fd7004:      	movl	0x10(%r14), %ecx
 7fd7008:      	leaq	(,%rcx,8), %rdx
 7fd7010:      	leaq	(%rdx,%rdx,4), %rdx
 7fd7014:      	leaq	(%rax,%rdx), %r15
 7fd7018:      	cmpl	$0x0, 0x8(%r14)
 7fd701d:      	movq	%r15, %rbp
 7fd7020:      	je	0x7fd7047 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd7022:      	movq	%rax, %rbp
 7fd7025:      	testq	%rcx, %rcx
 7fd7028:      	je	0x7fd7047 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd702a:      	movq	%rax, %rbp
 7fd702d:      	nopl	(%rax)
 7fd7030:      	movl	0x8(%rbp), %esi
 7fd7033:      	decl	%esi
 7fd7035:      	cmpl	$-0x2, %esi
 7fd7038:      	jb	0x7fd7047 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd703a:      	addq	$0x28, %rbp
 7fd703e:      	addq	$-0x28, %rdx
 7fd7042:      	jne	0x7fd7030 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x60>
 7fd7044:      	movq	%r15, %rbp
 7fd7047:      	leaq	(%rcx,%rcx,4), %rcx
 7fd704b:      	leaq	(%rax,%rcx,8), %rdx
 7fd704f:      	cmpq	%rdx, %rbp
 7fd7052:      	je	0x7fd730c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x33c>
 7fd7058:      	xorl	%r13d, %r13d
 7fd705b:      	xorl	%r12d, %r12d
 7fd705e:      	xorl	%ecx, %ecx
 7fd7060:      	movq	%rdx, 0x8(%rsp)
 7fd7065:      	jmp	0x7fd707d <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xad>
 7fd7067:      	nopw	(%rax,%rax)
 7fd7070:      	leaq	0x8(%rbx), %r12
 7fd7074:      	cmpq	%rdx, %rbp
 7fd7077:      	je	0x7fd713c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x16c>
 7fd707d:      	cmpq	%rcx, %r12
 7fd7080:      	je	0x7fd7090 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xc0>
 7fd7082:      	movq	%rbp, (%r12)
 7fd7086:      	movq	%r12, %rbx
 7fd7089:      	jmp	0x7fd7120 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x150>
 7fd708e:      	nop
 7fd7090:      	subq	%r13, %r12
 7fd7093:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 7fd709d:      	cmpq	%rax, %r12
 7fd70a0:      	je	0x7fd7372 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x3a2>
 7fd70a6:      	movq	%r13, %r14
 7fd70a9:      	movq	%r12, %rax
 7fd70ac:      	sarq	$0x3, %rax
 7fd70b0:      	cmpq	$0x1, %rax
 7fd70b4:      	movq	%rax, %rcx
 7fd70b7:      	adcq	$0x0, %rcx
 7fd70bb:      	leaq	(%rcx,%rax), %rbx
 7fd70bf:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 7fd70c9:      	cmpq	%rdx, %rbx
 7fd70cc:      	cmovaeq	%rdx, %rbx
 7fd70d0:      	addq	%rax, %rcx
 7fd70d3:      	cmovbq	%rdx, %rbx
 7fd70d7:      	leaq	(,%rbx,8), %rdi
 7fd70df:      	callq	0x828a6b0 <_Znwm@plt>
 7fd70e4:      	movq	%rax, %r13
 7fd70e7:      	movq	%rbp, (%rax,%r12)
 7fd70eb:      	testq	%r12, %r12
 7fd70ee:      	jle	0x7fd70fe <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x12e>
 7fd70f0:      	movq	%r13, %rdi
 7fd70f3:      	movq	%r14, %rsi
 7fd70f6:      	movq	%r12, %rdx
 7fd70f9:      	callq	0x828ace0 <memcpy@plt>
 7fd70fe:      	testq	%r14, %r14
 7fd7101:      	je	0x7fd710e <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x13e>
 7fd7103:      	movq	%r14, %rdi
 7fd7106:      	movq	%r12, %rsi
 7fd7109:      	callq	0x828a6f0 <_ZdlPvm@plt>
 7fd710e:      	addq	%r13, %r12
 7fd7111:      	leaq	(%r13,%rbx,8), %rcx
 7fd7116:      	movq	%r12, %rbx
 7fd7119:      	movq	0x8(%rsp), %rdx
 7fd711e:      	nop
 7fd7120:      	addq	$0x28, %rbp
 7fd7124:      	cmpq	%r15, %rbp
 7fd7127:      	je	0x7fd7070 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xa0>
 7fd712d:      	movl	0x8(%rbp), %eax
 7fd7130:      	decl	%eax
 7fd7132:      	cmpl	$-0x2, %eax
 7fd7135:      	jae	0x7fd7120 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x150>
 7fd7137:      	jmp	0x7fd7070 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xa0>
 7fd713c:      	movq	%rcx, 0x18(%rsp)
 7fd7141:      	movq	%r13, 0x8(%rsp)
 7fd7146:      	cmpq	%r12, %r13
 7fd7149:      	movq	0x10(%rsp), %r13
 7fd714e:      	je	0x7fd72f5 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x325>
 7fd7154:      	movq	%r12, %r15
 7fd7157:      	movq	0x8(%rsp), %r14
 7fd715c:      	subq	%r14, %r15
 7fd715f:      	movq	%r15, %rax
 7fd7162:      	sarq	$0x3, %rax
 7fd7166:      	bsrq	%rax, %rdx
 7fd716a:      	xorl	$0x3f, %edx
 7fd716d:      	addl	%edx, %edx
 7fd716f:      	xorq	$0x7e, %rdx
 7fd7173:      	movq	%r14, %rdi
 7fd7176:      	movq	%r12, %rsi
 7fd7179:      	callq	0x7fdb270 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN4llvm15DWARFDebugNames6AbbrevESt6vectorIS6_SaIS6_EEEElNS0_5__ops15_Iter_comp_iterIZNKS3_9NameIndex17dumpAbbreviationsERNS2_13ScopedPrinterEE3$_0EEEvT_SJ_T0_T1_>
 7fd717e:      	movq	%r14, %rsi
 7fd7181:      	leaq	0x8(%r14), %r8
 7fd7185:      	cmpq	$0x81, %r15
 7fd718c:      	jl	0x7fd719e <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x1ce>
 7fd718e:      	movl	$0x8, %ebp
 7fd7193:      	movq	%r8, %r15
 7fd7196:      	movq	%rsi, %rdi
 7fd7199:      	jmp	0x7fd7257 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x287>
 7fd719e:      	cmpq	%rbx, %rsi
 7fd71a1:      	je	0x7fd72d3 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd71a7:      	movq	%rsi, %r15
 7fd71aa:      	jmp	0x7fd71eb <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x21b>
 7fd71ac:      	nopl	(%rax)
 7fd71b0:      	movq	%r15, %rdx
 7fd71b3:      	subq	%rsi, %rdx
 7fd71b6:      	movq	%rdx, %rax
 7fd71b9:      	sarq	$0x3, %rax
 7fd71bd:      	cmpq	$0x2, %rax
 7fd71c1:      	jl	0x7fd7222 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x252>
 7fd71c3:      	shlq	$0x3, %rax
 7fd71c7:      	subq	%rax, %rdi
 7fd71ca:      	addq	$0x10, %rdi
 7fd71ce:      	callq	0x828ac50 <memmove@plt>
 7fd71d3:      	movq	0x8(%rsp), %rsi
 7fd71d8:      	movq	%rsi, %rax
 7fd71db:      	movq	%r12, (%rax)
 7fd71de:      	leaq	0x8(%r15), %r8
 7fd71e2:      	cmpq	%rbx, %r15
 7fd71e5:      	je	0x7fd72d3 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd71eb:      	movq	%r15, %rdi
 7fd71ee:      	movq	%r8, %r15
 7fd71f1:      	movq	(%r8), %r12
 7fd71f4:      	movq	(%rsi), %r8
 7fd71f7:      	movq	(%r12), %rcx
 7fd71fb:      	cmpq	(%r8), %rcx
 7fd71fe:      	jb	0x7fd71b0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x1e0>
 7fd7200:      	movq	(%rdi), %rdx
 7fd7203:      	movq	%r15, %rax
 7fd7206:      	cmpq	(%rdx), %rcx
 7fd7209:      	jae	0x7fd71db <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd720b:      	movq	%r15, %rax
 7fd720e:      	nop
 7fd7210:      	movq	%rdx, (%rax)
 7fd7213:      	movq	-0x10(%rax), %rdx
 7fd7217:      	addq	$-0x8, %rax
 7fd721b:      	cmpq	(%rdx), %rcx
 7fd721e:      	jb	0x7fd7210 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x240>
 7fd7220:      	jmp	0x7fd71db <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd7222:      	movq	%rsi, %rax
 7fd7225:      	cmpq	$0x8, %rdx
 7fd7229:      	jne	0x7fd71db <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd722b:      	movq	%r8, 0x8(%rdi)
 7fd722f:      	jmp	0x7fd71d8 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x208>
 7fd7231:      	movq	%rdx, 0x8(%rcx)
 7fd7235:      	nopw	%cs:(%rax,%rax)
 7fd723f:      	nop
 7fd7240:      	movq	%rsi, %rcx
 7fd7243:      	movq	%r13, (%rcx)
 7fd7246:      	addq	$0x8, %rbp
 7fd724a:      	addq	$0x8, %r15
 7fd724e:      	cmpq	$0x80, %rbp
 7fd7255:      	je	0x7fd72c2 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2f2>
 7fd7257:      	movq	%rdi, %rcx
 7fd725a:      	leaq	(%rsi,%rbp), %rdi
 7fd725e:      	movq	(%rsi,%rbp), %r13
 7fd7262:      	movq	(%rsi), %rdx
 7fd7265:      	movq	(%r13), %rax
 7fd7269:      	cmpq	(%rdx), %rax
 7fd726c:      	jae	0x7fd72a0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2d0>
 7fd726e:      	cmpq	$0x9, %rbp
 7fd7272:      	jb	0x7fd7231 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x261>
 7fd7274:      	movq	%rdi, 0x20(%rsp)
 7fd7279:      	movq	%r8, %rdi
 7fd727c:      	movq	%rbp, %rdx
 7fd727f:      	movq	%rbx, %r14
 7fd7282:      	movq	%r8, %rbx
 7fd7285:      	callq	0x828ac50 <memmove@plt>
 7fd728a:      	movq	%rbx, %r8
 7fd728d:      	movq	%r14, %rbx
 7fd7290:      	movq	0x20(%rsp), %rdi
 7fd7295:      	movq	0x8(%rsp), %rsi
 7fd729a:      	jmp	0x7fd7240 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x270>
 7fd729c:      	nopl	(%rax)
 7fd72a0:      	movq	(%rcx), %rdx
 7fd72a3:      	movq	%rdi, %rcx
 7fd72a6:      	cmpq	(%rdx), %rax
 7fd72a9:      	jae	0x7fd7243 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x273>
 7fd72ab:      	movq	%r15, %rcx
 7fd72ae:      	nop
 7fd72b0:      	movq	%rdx, (%rcx)
 7fd72b3:      	movq	-0x10(%rcx), %rdx
 7fd72b7:      	addq	$-0x8, %rcx
 7fd72bb:      	cmpq	(%rdx), %rax
 7fd72be:      	jb	0x7fd72b0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2e0>
 7fd72c0:      	jmp	0x7fd7243 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x273>
 7fd72c2:      	leaq	0x80(%rsi), %rax
 7fd72c9:      	cmpq	%r12, %rax
 7fd72cc:      	movq	0x10(%rsp), %r13
 7fd72d1:      	jne	0x7fd733c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x36c>
 7fd72d3:      	leaq	-0x8(%rsi), %r15
 7fd72d7:      	nopw	(%rax,%rax)
 7fd72e0:      	movq	0x8(%r15), %rdi
 7fd72e4:      	addq	$0x8, %r15
 7fd72e8:      	movq	%r13, %rsi
 7fd72eb:      	callq	0x7fd4610 <_ZNK4llvm15DWARFDebugNames6Abbrev4dumpERNS_13ScopedPrinterE>
 7fd72f0:      	cmpq	%rbx, %r15
 7fd72f3:      	jne	0x7fd72e0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x310>
 7fd72f5:      	movq	0x8(%rsp), %rdi
 7fd72fa:      	testq	%rdi, %rdi
 7fd72fd:      	je	0x7fd730c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x33c>
 7fd72ff:      	movq	0x18(%rsp), %rsi
 7fd7304:      	subq	%rdi, %rsi
 7fd7307:      	callq	0x828a6f0 <_ZdlPvm@plt>
 7fd730c:      	movq	0x10(%rsp), %rdi
 7fd7311:      	movq	(%rdi), %rax
 7fd7314:      	addq	$0x28, %rsp
 7fd7318:      	popq	%rbx
 7fd7319:      	popq	%r12
 7fd731b:      	popq	%r13
 7fd731d:      	popq	%r14
 7fd731f:      	popq	%r15
 7fd7321:      	popq	%rbp
 7fd7322:      	jmpq	*0x118(%rax)
 7fd7328:      	nopl	(%rax,%rax)
 7fd7330:      	movq	%rcx, (%rdi)
 7fd7333:      	cmpq	%rbx, %rax
 7fd7336:      	leaq	0x8(%rax), %rax
 7fd733a:      	je	0x7fd72d3 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd733c:      	movq	-0x8(%rax), %rdx
 7fd7340:      	movq	(%rax), %rcx
 7fd7343:      	movq	(%rcx), %r8
 7fd7346:      	movq	%rax, %rdi
 7fd7349:      	cmpq	(%rdx), %r8
 7fd734c:      	jae	0x7fd7330 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x360>
 7fd734e:      	movq	%rax, %rdi
 7fd7351:      	nopw	%cs:(%rax,%rax)
 7fd735b:      	nopl	(%rax,%rax)
 7fd7360:      	movq	%rdx, (%rdi)
 7fd7363:      	movq	-0x10(%rdi), %rdx
 7fd7367:      	addq	$-0x8, %rdi
 7fd736b:      	cmpq	(%rdx), %r8
 7fd736e:      	jb	0x7fd7360 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x390>
 7fd7370:      	jmp	0x7fd7330 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x360>
 7fd7372:      	leaq	-0x733c98f(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 7fd7379:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
