
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007fd6f40 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE>:
 7fd6f40:      	pushq	%rbp
 7fd6f41:      	pushq	%r15
 7fd6f43:      	pushq	%r14
 7fd6f45:      	pushq	%r13
 7fd6f47:      	pushq	%r12
 7fd6f49:      	pushq	%rbx
 7fd6f4a:      	subq	$0x28, %rsp
 7fd6f4e:      	movq	%rsi, %rcx
 7fd6f51:      	movq	%rdi, %r14
 7fd6f54:      	movq	(%rsi), %rax
 7fd6f57:      	leaq	-0x72723e8(%rip), %rsi  # 0xd64b76 <.L.str.64>
 7fd6f5e:      	movl	$0xd, %edx
 7fd6f63:      	movq	%rcx, 0x10(%rsp)
 7fd6f68:      	movq	%rcx, %rdi
 7fd6f6b:      	callq	*0x110(%rax)
 7fd6f71:      	movq	(%r14), %rax
 7fd6f74:      	movl	0x10(%r14), %ecx
 7fd6f78:      	leaq	(,%rcx,8), %rdx
 7fd6f80:      	leaq	(%rdx,%rdx,4), %rdx
 7fd6f84:      	leaq	(%rax,%rdx), %r15
 7fd6f88:      	cmpl	$0x0, 0x8(%r14)
 7fd6f8d:      	movq	%r15, %rbp
 7fd6f90:      	je	0x7fd6fb7 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd6f92:      	movq	%rax, %rbp
 7fd6f95:      	testq	%rcx, %rcx
 7fd6f98:      	je	0x7fd6fb7 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd6f9a:      	movq	%rax, %rbp
 7fd6f9d:      	nopl	(%rax)
 7fd6fa0:      	movl	0x8(%rbp), %esi
 7fd6fa3:      	decl	%esi
 7fd6fa5:      	cmpl	$-0x2, %esi
 7fd6fa8:      	jb	0x7fd6fb7 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x77>
 7fd6faa:      	addq	$0x28, %rbp
 7fd6fae:      	addq	$-0x28, %rdx
 7fd6fb2:      	jne	0x7fd6fa0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x60>
 7fd6fb4:      	movq	%r15, %rbp
 7fd6fb7:      	leaq	(%rcx,%rcx,4), %rcx
 7fd6fbb:      	leaq	(%rax,%rcx,8), %rdx
 7fd6fbf:      	cmpq	%rdx, %rbp
 7fd6fc2:      	je	0x7fd727c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x33c>
 7fd6fc8:      	xorl	%r13d, %r13d
 7fd6fcb:      	xorl	%r12d, %r12d
 7fd6fce:      	xorl	%ecx, %ecx
 7fd6fd0:      	movq	%rdx, 0x8(%rsp)
 7fd6fd5:      	jmp	0x7fd6fed <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xad>
 7fd6fd7:      	nopw	(%rax,%rax)
 7fd6fe0:      	leaq	0x8(%rbx), %r12
 7fd6fe4:      	cmpq	%rdx, %rbp
 7fd6fe7:      	je	0x7fd70ac <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x16c>
 7fd6fed:      	cmpq	%rcx, %r12
 7fd6ff0:      	je	0x7fd7000 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xc0>
 7fd6ff2:      	movq	%rbp, (%r12)
 7fd6ff6:      	movq	%r12, %rbx
 7fd6ff9:      	jmp	0x7fd7090 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x150>
 7fd6ffe:      	nop
 7fd7000:      	subq	%r13, %r12
 7fd7003:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 7fd700d:      	cmpq	%rax, %r12
 7fd7010:      	je	0x7fd72e2 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x3a2>
 7fd7016:      	movq	%r13, %r14
 7fd7019:      	movq	%r12, %rax
 7fd701c:      	sarq	$0x3, %rax
 7fd7020:      	cmpq	$0x1, %rax
 7fd7024:      	movq	%rax, %rcx
 7fd7027:      	adcq	$0x0, %rcx
 7fd702b:      	leaq	(%rcx,%rax), %rbx
 7fd702f:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 7fd7039:      	cmpq	%rdx, %rbx
 7fd703c:      	cmovaeq	%rdx, %rbx
 7fd7040:      	addq	%rax, %rcx
 7fd7043:      	cmovbq	%rdx, %rbx
 7fd7047:      	leaq	(,%rbx,8), %rdi
 7fd704f:      	callq	0x828a620 <_Znwm@plt>
 7fd7054:      	movq	%rax, %r13
 7fd7057:      	movq	%rbp, (%rax,%r12)
 7fd705b:      	testq	%r12, %r12
 7fd705e:      	jle	0x7fd706e <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x12e>
 7fd7060:      	movq	%r13, %rdi
 7fd7063:      	movq	%r14, %rsi
 7fd7066:      	movq	%r12, %rdx
 7fd7069:      	callq	0x828ac50 <memcpy@plt>
 7fd706e:      	testq	%r14, %r14
 7fd7071:      	je	0x7fd707e <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x13e>
 7fd7073:      	movq	%r14, %rdi
 7fd7076:      	movq	%r12, %rsi
 7fd7079:      	callq	0x828a660 <_ZdlPvm@plt>
 7fd707e:      	addq	%r13, %r12
 7fd7081:      	leaq	(%r13,%rbx,8), %rcx
 7fd7086:      	movq	%r12, %rbx
 7fd7089:      	movq	0x8(%rsp), %rdx
 7fd708e:      	nop
 7fd7090:      	addq	$0x28, %rbp
 7fd7094:      	cmpq	%r15, %rbp
 7fd7097:      	je	0x7fd6fe0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xa0>
 7fd709d:      	movl	0x8(%rbp), %eax
 7fd70a0:      	decl	%eax
 7fd70a2:      	cmpl	$-0x2, %eax
 7fd70a5:      	jae	0x7fd7090 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x150>
 7fd70a7:      	jmp	0x7fd6fe0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0xa0>
 7fd70ac:      	movq	%rcx, 0x18(%rsp)
 7fd70b1:      	movq	%r13, 0x8(%rsp)
 7fd70b6:      	cmpq	%r12, %r13
 7fd70b9:      	movq	0x10(%rsp), %r13
 7fd70be:      	je	0x7fd7265 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x325>
 7fd70c4:      	movq	%r12, %r15
 7fd70c7:      	movq	0x8(%rsp), %r14
 7fd70cc:      	subq	%r14, %r15
 7fd70cf:      	movq	%r15, %rax
 7fd70d2:      	sarq	$0x3, %rax
 7fd70d6:      	bsrq	%rax, %rdx
 7fd70da:      	xorl	$0x3f, %edx
 7fd70dd:      	addl	%edx, %edx
 7fd70df:      	xorq	$0x7e, %rdx
 7fd70e3:      	movq	%r14, %rdi
 7fd70e6:      	movq	%r12, %rsi
 7fd70e9:      	callq	0x7fdb1e0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN4llvm15DWARFDebugNames6AbbrevESt6vectorIS6_SaIS6_EEEElNS0_5__ops15_Iter_comp_iterIZNKS3_9NameIndex17dumpAbbreviationsERNS2_13ScopedPrinterEE3$_0EEEvT_SJ_T0_T1_>
 7fd70ee:      	movq	%r14, %rsi
 7fd70f1:      	leaq	0x8(%r14), %r8
 7fd70f5:      	cmpq	$0x81, %r15
 7fd70fc:      	jl	0x7fd710f <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x1cf>
 7fd70fe:      	leaq	0x8(%rsi), %r15
 7fd7102:      	movl	$0x8, %ebp
 7fd7107:      	movq	%rsi, %rdi
 7fd710a:      	jmp	0x7fd71c7 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x287>
 7fd710f:      	cmpq	%rbx, %rsi
 7fd7112:      	je	0x7fd7243 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd7118:      	movq	%rsi, %r15
 7fd711b:      	jmp	0x7fd715b <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x21b>
 7fd711d:      	nopl	(%rax)
 7fd7120:      	movq	%r15, %rdx
 7fd7123:      	subq	%rsi, %rdx
 7fd7126:      	movq	%rdx, %rax
 7fd7129:      	sarq	$0x3, %rax
 7fd712d:      	cmpq	$0x2, %rax
 7fd7131:      	jl	0x7fd7192 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x252>
 7fd7133:      	shlq	$0x3, %rax
 7fd7137:      	subq	%rax, %rdi
 7fd713a:      	addq	$0x10, %rdi
 7fd713e:      	callq	0x828abc0 <memmove@plt>
 7fd7143:      	movq	0x8(%rsp), %rsi
 7fd7148:      	movq	%rsi, %rax
 7fd714b:      	movq	%r12, (%rax)
 7fd714e:      	leaq	0x8(%r15), %r8
 7fd7152:      	cmpq	%rbx, %r15
 7fd7155:      	je	0x7fd7243 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd715b:      	movq	%r15, %rdi
 7fd715e:      	movq	%r8, %r15
 7fd7161:      	movq	(%r8), %r12
 7fd7164:      	movq	(%rsi), %r8
 7fd7167:      	movq	(%r12), %rcx
 7fd716b:      	cmpq	(%r8), %rcx
 7fd716e:      	jb	0x7fd7120 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x1e0>
 7fd7170:      	movq	(%rdi), %rdx
 7fd7173:      	movq	%r15, %rax
 7fd7176:      	cmpq	(%rdx), %rcx
 7fd7179:      	jae	0x7fd714b <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd717b:      	movq	%r15, %rax
 7fd717e:      	nop
 7fd7180:      	movq	%rdx, (%rax)
 7fd7183:      	movq	-0x10(%rax), %rdx
 7fd7187:      	addq	$-0x8, %rax
 7fd718b:      	cmpq	(%rdx), %rcx
 7fd718e:      	jb	0x7fd7180 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x240>
 7fd7190:      	jmp	0x7fd714b <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd7192:      	movq	%rsi, %rax
 7fd7195:      	cmpq	$0x8, %rdx
 7fd7199:      	jne	0x7fd714b <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x20b>
 7fd719b:      	movq	%r8, 0x8(%rdi)
 7fd719f:      	jmp	0x7fd7148 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x208>
 7fd71a1:      	movq	%rdx, 0x8(%rcx)
 7fd71a5:      	nopw	%cs:(%rax,%rax)
 7fd71af:      	nop
 7fd71b0:      	movq	%rsi, %rcx
 7fd71b3:      	movq	%r13, (%rcx)
 7fd71b6:      	addq	$0x8, %rbp
 7fd71ba:      	addq	$0x8, %r15
 7fd71be:      	cmpq	$0x80, %rbp
 7fd71c5:      	je	0x7fd7232 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2f2>
 7fd71c7:      	movq	%rdi, %rcx
 7fd71ca:      	leaq	(%rsi,%rbp), %rdi
 7fd71ce:      	movq	(%rsi,%rbp), %r13
 7fd71d2:      	movq	(%rsi), %rdx
 7fd71d5:      	movq	(%r13), %rax
 7fd71d9:      	cmpq	(%rdx), %rax
 7fd71dc:      	jae	0x7fd7210 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2d0>
 7fd71de:      	cmpq	$0x9, %rbp
 7fd71e2:      	jb	0x7fd71a1 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x261>
 7fd71e4:      	movq	%rdi, 0x20(%rsp)
 7fd71e9:      	movq	%r8, %rdi
 7fd71ec:      	movq	%rbp, %rdx
 7fd71ef:      	movq	%rbx, %r14
 7fd71f2:      	movq	%r8, %rbx
 7fd71f5:      	callq	0x828abc0 <memmove@plt>
 7fd71fa:      	movq	%rbx, %r8
 7fd71fd:      	movq	%r14, %rbx
 7fd7200:      	movq	0x20(%rsp), %rdi
 7fd7205:      	movq	0x8(%rsp), %rsi
 7fd720a:      	jmp	0x7fd71b0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x270>
 7fd720c:      	nopl	(%rax)
 7fd7210:      	movq	(%rcx), %rdx
 7fd7213:      	movq	%rdi, %rcx
 7fd7216:      	cmpq	(%rdx), %rax
 7fd7219:      	jae	0x7fd71b3 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x273>
 7fd721b:      	movq	%r15, %rcx
 7fd721e:      	nop
 7fd7220:      	movq	%rdx, (%rcx)
 7fd7223:      	movq	-0x10(%rcx), %rdx
 7fd7227:      	addq	$-0x8, %rcx
 7fd722b:      	cmpq	(%rdx), %rax
 7fd722e:      	jb	0x7fd7220 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x2e0>
 7fd7230:      	jmp	0x7fd71b3 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x273>
 7fd7232:      	leaq	0x80(%rsi), %rax
 7fd7239:      	cmpq	%r12, %rax
 7fd723c:      	movq	0x10(%rsp), %r13
 7fd7241:      	jne	0x7fd72ac <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x36c>
 7fd7243:      	leaq	-0x8(%rsi), %r15
 7fd7247:      	nopw	(%rax,%rax)
 7fd7250:      	movq	0x8(%r15), %rdi
 7fd7254:      	addq	$0x8, %r15
 7fd7258:      	movq	%r13, %rsi
 7fd725b:      	callq	0x7fd4580 <_ZNK4llvm15DWARFDebugNames6Abbrev4dumpERNS_13ScopedPrinterE>
 7fd7260:      	cmpq	%rbx, %r15
 7fd7263:      	jne	0x7fd7250 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x310>
 7fd7265:      	movq	0x8(%rsp), %rdi
 7fd726a:      	testq	%rdi, %rdi
 7fd726d:      	je	0x7fd727c <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x33c>
 7fd726f:      	movq	0x18(%rsp), %rsi
 7fd7274:      	subq	%rdi, %rsi
 7fd7277:      	callq	0x828a660 <_ZdlPvm@plt>
 7fd727c:      	movq	0x10(%rsp), %rdi
 7fd7281:      	movq	(%rdi), %rax
 7fd7284:      	addq	$0x28, %rsp
 7fd7288:      	popq	%rbx
 7fd7289:      	popq	%r12
 7fd728b:      	popq	%r13
 7fd728d:      	popq	%r14
 7fd728f:      	popq	%r15
 7fd7291:      	popq	%rbp
 7fd7292:      	jmpq	*0x118(%rax)
 7fd7298:      	nopl	(%rax,%rax)
 7fd72a0:      	movq	%rcx, (%rdi)
 7fd72a3:      	cmpq	%rbx, %rax
 7fd72a6:      	leaq	0x8(%rax), %rax
 7fd72aa:      	je	0x7fd7243 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x303>
 7fd72ac:      	movq	-0x8(%rax), %rdx
 7fd72b0:      	movq	(%rax), %rcx
 7fd72b3:      	movq	(%rcx), %r8
 7fd72b6:      	movq	%rax, %rdi
 7fd72b9:      	cmpq	(%rdx), %r8
 7fd72bc:      	jae	0x7fd72a0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x360>
 7fd72be:      	movq	%rax, %rdi
 7fd72c1:      	nopw	%cs:(%rax,%rax)
 7fd72cb:      	nopl	(%rax,%rax)
 7fd72d0:      	movq	%rdx, (%rdi)
 7fd72d3:      	movq	-0x10(%rdi), %rdx
 7fd72d7:      	addq	$-0x8, %rdi
 7fd72db:      	cmpq	(%rdx), %r8
 7fd72de:      	jb	0x7fd72d0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x390>
 7fd72e0:      	jmp	0x7fd72a0 <_ZNK4llvm15DWARFDebugNames9NameIndex17dumpAbbreviationsERNS_13ScopedPrinterE+0x360>
 7fd72e2:      	leaq	-0x733c8ff(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 7fd72e9:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
