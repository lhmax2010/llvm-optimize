
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000052ca980 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b>:
 52ca980:      	cmpl	$0x0, 0xc(%rdi)
 52ca984:      	je	0x52cadb6 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x436>
 52ca98a:      	pushq	%rbp
 52ca98b:      	pushq	%r15
 52ca98d:      	pushq	%r14
 52ca98f:      	pushq	%r13
 52ca991:      	pushq	%r12
 52ca993:      	pushq	%rbx
 52ca994:      	subq	$0x268, %rsp            # imm = 0x268
 52ca99b:      	movq	%rsi, %rbx
 52ca99e:      	movq	%rdi, %r14
 52ca9a1:      	movq	%rcx, 0x28(%rsp)
 52ca9a6:      	movl	%r8d, 0x14(%rsp)
 52ca9ab:      	movq	0x50(%rsi), %rdi
 52ca9af:      	movq	(%rdi), %rax
 52ca9b2:      	movq	%rdx, %rsi
 52ca9b5:      	xorl	%edx, %edx
 52ca9b7:      	callq	*0xb0(%rax)
 52ca9bd:      	movq	(%r14), %rax
 52ca9c0:      	movq	%r14, 0x18(%rsp)
 52ca9c5:      	movl	0x8(%r14), %ecx
 52ca9c9:      	movq	%rax, %r15
 52ca9cc:      	testq	%rcx, %rcx
 52ca9cf:      	je	0x52ca9f2 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x72>
 52ca9d1:      	movq	%rax, %r15
 52ca9d4:      	jmp	0x52ca9e4 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x64>
 52ca9d6:      	nopw	%cs:(%rax,%rax)
 52ca9e0:      	addq	$0x8, %r15
 52ca9e4:      	movq	(%r15), %rdx
 52ca9e7:      	testq	%rdx, %rdx
 52ca9ea:      	je	0x52ca9e0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x60>
 52ca9ec:      	cmpq	$-0x8, %rdx
 52ca9f0:      	je	0x52ca9e0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x60>
 52ca9f2:      	movq	%rbx, 0x8(%rsp)
 52ca9f7:      	leaq	(%rax,%rcx,8), %rbp
 52ca9fb:      	leaq	0x68(%rsp), %rax
 52caa00:      	movq	%rax, 0x58(%rsp)
 52caa05:      	movabsq	$0x4000000000, %rax     # imm = 0x4000000000
 52caa0f:      	movq	%rax, 0x60(%rsp)
 52caa14:      	cmpq	%rbp, %r15
 52caa17:      	je	0x52cabc8 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52caa1d:      	xorl	%r14d, %r14d
 52caa20:      	movq	%r15, %rcx
 52caa23:      	nopw	%cs:(%rax,%rax)
 52caa2d:      	nopl	(%rax)
 52caa30:      	movq	%r14, %rax
 52caa33:      	nopw	%cs:(%rax,%rax)
 52caa3d:      	nopl	(%rax)
 52caa40:      	addq	$0x8, %rcx
 52caa44:      	movq	(%rcx), %rdx
 52caa47:      	testq	%rdx, %rdx
 52caa4a:      	je	0x52caa40 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xc0>
 52caa4c:      	cmpq	$-0x8, %rdx
 52caa50:      	je	0x52caa40 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xc0>
 52caa52:      	leaq	0x1(%rax), %r14
 52caa56:      	cmpq	%rbp, %rcx
 52caa59:      	jne	0x52caa30 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xb0>
 52caa5b:      	xorl	%r12d, %r12d
 52caa5e:      	leaq	0x68(%rsp), %r13
 52caa63:      	cmpq	$0x40, %rax
 52caa67:      	jb	0x52caa8a <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x10a>
 52caa69:      	leaq	0x58(%rsp), %rdi
 52caa6e:      	movl	$0x8, %ecx
 52caa73:      	leaq	0x68(%rsp), %rsi
 52caa78:      	movq	%r14, %rdx
 52caa7b:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 52caa80:      	movl	0x60(%rsp), %r12d
 52caa85:      	movq	0x58(%rsp), %r13
 52caa8a:      	movl	%r12d, %eax
 52caa8d:      	leaq	(%r13,%rax,8), %rax
 52caa92:      	movq	(%r15), %rcx
 52caa95:      	nopw	%cs:(%rax,%rax)
 52caa9f:      	nop
 52caaa0:      	movq	%rcx, (%rax)
 52caaa3:      	nopw	%cs:(%rax,%rax)
 52caaad:      	nopl	(%rax)
 52caab0:      	addq	$0x8, %r15
 52caab4:      	movq	(%r15), %rcx
 52caab7:      	testq	%rcx, %rcx
 52caaba:      	je	0x52caab0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x130>
 52caabc:      	cmpq	$-0x8, %rcx
 52caac0:      	je	0x52caab0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x130>
 52caac2:      	addq	$0x8, %rax
 52caac6:      	cmpq	%rbp, %r15
 52caac9:      	jne	0x52caaa0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x120>
 52caacb:      	addl	%r14d, %r12d
 52caace:      	movl	%r12d, 0x60(%rsp)
 52caad3:      	je	0x52cabc8 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52caad9:      	leaq	(%r13,%r12,8), %rbx
 52caade:      	bsrq	%r12, %rdx
 52caae2:      	xorl	$0x3f, %edx
 52caae5:      	addl	%edx, %edx
 52caae7:      	xorq	$0x7e, %rdx
 52caaeb:      	movq	%r13, %rdi
 52caaee:      	movq	%rbx, %rsi
 52caaf1:      	callq	0x52cb010 <_ZSt16__introsort_loopIPPKN4llvm14StringMapEntryINS0_20DwarfStringPoolEntryEEElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_15DwarfStringPool4emitERNS0_10AsmPrinterEPNS0_9MCSectionESE_bE3$_0EEEvT_SH_T0_T1_>
 52caaf6:      	leaq	0x8(%r13), %rbp
 52caafa:      	cmpl	$0x11, %r12d
 52caafe:      	jb	0x52cab17 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x197>
 52cab00:      	movq	%rbx, 0x20(%rsp)
 52cab05:      	leaq	0x8(%r13), %r12
 52cab09:      	movl	$0x8, %r15d
 52cab0f:      	movq	%r13, %r14
 52cab12:      	jmp	0x52cae77 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4f7>
 52cab17:      	cmpl	$0x1, %r12d
 52cab1b:      	jne	0x52cadb7 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x437>
 52cab21:      	movl	0x60(%rsp), %r15d
 52cab26:      	testq	%r15, %r15
 52cab29:      	je	0x52cabc8 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52cab2f:      	shlq	$0x3, %r15
 52cab33:      	movq	0x58(%rsp), %r12
 52cab38:      	xorl	%r13d, %r13d
 52cab3b:      	leaq	-0x4529b98(%rip), %rbp  # 0xda0faa <.L.str.10>
 52cab42:      	leaq	0x30(%rsp), %r14
 52cab47:      	movq	0x8(%rsp), %rbx
 52cab4c:      	jmp	0x52cab9f <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x21f>
 52cab4e:      	nop
 52cab50:      	movq	0x50(%rbx), %rdi
 52cab54:      	movq	(%r12,%r13), %rax
 52cab58:      	movq	0x10(%rax), %rax
 52cab5c:      	movq	%rbp, 0x30(%rsp)
 52cab61:      	movq	%rax, 0x40(%rsp)
 52cab66:      	movw	$0xb03, 0x50(%rsp)      # imm = 0xB03
 52cab6d:      	movq	(%rdi), %rax
 52cab70:      	movq	%r14, %rsi
 52cab73:      	movl	$0x1, %edx
 52cab78:      	callq	*0x78(%rax)
 52cab7b:      	movq	0x50(%rbx), %rdi
 52cab7f:      	movq	(%r12,%r13), %rsi
 52cab83:      	movq	(%rsi), %rdx
 52cab86:      	addq	$0x20, %rsi
 52cab8a:      	incq	%rdx
 52cab8d:      	movq	(%rdi), %rax
 52cab90:      	callq	*0x1f8(%rax)
 52cab96:      	addq	$0x8, %r13
 52cab9a:      	cmpq	%r13, %r15
 52cab9d:      	je	0x52cabc8 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52cab9f:      	movq	0x18(%rsp), %rax
 52caba4:      	cmpb	$0x1, 0x3c(%rax)
 52caba8:      	jne	0x52cab50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1d0>
 52cabaa:      	movq	0x8(%rsp), %rax
 52cabaf:      	movq	0x50(%rax), %rdi
 52cabb3:      	movq	(%r12,%r13), %rax
 52cabb7:      	movq	0x8(%rax), %rsi
 52cabbb:      	movq	(%rdi), %rax
 52cabbe:      	xorl	%edx, %edx
 52cabc0:      	callq	*0xc8(%rax)
 52cabc6:      	jmp	0x52cab50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1d0>
 52cabc8:      	movq	0x28(%rsp), %rbx
 52cabcd:      	testq	%rbx, %rbx
 52cabd0:      	movq	0x8(%rsp), %r12
 52cabd5:      	je	0x52cad91 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cabdb:      	movq	0x18(%rsp), %r15
 52cabe0:      	movl	0x38(%r15), %r14d
 52cabe4:      	movl	0x60(%rsp), %eax
 52cabe8:      	cmpl	%eax, %r14d
 52cabeb:      	je	0x52cac3b <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2bb>
 52cabed:      	jb	0x52cac36 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2b6>
 52cabef:      	cmpl	0x64(%rsp), %r14d
 52cabf4:      	jbe	0x52cac11 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x291>
 52cabf6:      	leaq	0x58(%rsp), %rdi
 52cabfb:      	movl	$0x8, %ecx
 52cac00:      	leaq	0x68(%rsp), %rsi
 52cac05:      	movq	%r14, %rdx
 52cac08:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 52cac0d:      	movl	0x60(%rsp), %eax
 52cac11:      	cmpl	%eax, %r14d
 52cac14:      	je	0x52cac36 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2b6>
 52cac16:      	movl	%eax, %eax
 52cac18:      	leaq	(,%rax,8), %rdi
 52cac20:      	addq	0x58(%rsp), %rdi
 52cac25:      	movq	%r14, %rdx
 52cac28:      	subq	%rax, %rdx
 52cac2b:      	shlq	$0x3, %rdx
 52cac2f:      	xorl	%esi, %esi
 52cac31:      	callq	0x828ab90 <memset@plt>
 52cac36:      	movl	%r14d, 0x60(%rsp)
 52cac3b:      	movq	(%r15), %rcx
 52cac3e:      	movl	0x8(%r15), %edx
 52cac42:      	movq	%rcx, %rax
 52cac45:      	testq	%rdx, %rdx
 52cac48:      	je	0x52cac62 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2e2>
 52cac4a:      	movq	%rcx, %rax
 52cac4d:      	jmp	0x52cac54 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d4>
 52cac4f:      	nop
 52cac50:      	addq	$0x8, %rax
 52cac54:      	movq	(%rax), %rsi
 52cac57:      	testq	%rsi, %rsi
 52cac5a:      	je	0x52cac50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d0>
 52cac5c:      	cmpq	$-0x8, %rsi
 52cac60:      	je	0x52cac50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d0>
 52cac62:      	leaq	(%rcx,%rdx,8), %rcx
 52cac66:      	cmpq	%rcx, %rax
 52cac69:      	je	0x52caca7 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x327>
 52cac6b:      	movq	0x58(%rsp), %rdx
 52cac70:      	movq	(%rax), %rdi
 52cac73:      	movl	$0xffffffff, %esi       # imm = 0xFFFFFFFF
 52cac78:      	nopl	(%rax,%rax)
 52cac80:      	movl	0x18(%rdi), %r8d
 52cac84:      	cmpq	%rsi, %r8
 52cac87:      	je	0x52cac90 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52cac89:      	movq	%rdi, (%rdx,%r8,8)
 52cac8d:      	nopl	(%rax)
 52cac90:      	addq	$0x8, %rax
 52cac94:      	movq	(%rax), %rdi
 52cac97:      	testq	%rdi, %rdi
 52cac9a:      	je	0x52cac90 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52cac9c:      	cmpq	$-0x8, %rdi
 52caca0:      	je	0x52cac90 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52caca2:      	cmpq	%rcx, %rax
 52caca5:      	jne	0x52cac80 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x300>
 52caca7:      	movq	0x50(%r12), %rdi
 52cacac:      	movq	(%rdi), %rax
 52cacaf:      	movq	%rbx, %rsi
 52cacb2:      	xorl	%edx, %edx
 52cacb4:      	callq	*0xb0(%rax)
 52cacba:      	movq	0x50(%r12), %rax
 52cacbf:      	movq	0x8(%rax), %rcx
 52cacc3:      	xorl	%eax, %eax
 52cacc5:      	cmpb	$0x0, 0x75a(%rcx)
 52caccc:      	setne	%cl
 52caccf:      	movl	0x60(%rsp), %r14d
 52cacd4:      	testq	%r14, %r14
 52cacd7:      	je	0x52cad91 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cacdd:      	movq	0x58(%rsp), %r15
 52cace2:      	shlq	$0x3, %r14
 52cace6:      	cmpb	$0x0, 0x14(%rsp)
 52caceb:      	je	0x52cad5a <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3da>
 52caced:      	xorl	%ebx, %ebx
 52cacef:      	jmp	0x52cad32 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3b2>
 52cacf1:      	nopw	%cs:(%rax,%rax)
 52cacfb:      	nopl	(%rax,%rax)
 52cad00:      	movq	0x10(%rax), %rsi
 52cad04:      	movq	0x50(%r12), %rdi
 52cad09:      	movq	(%rdi), %rax
 52cad0c:      	movq	0x8(%rdi), %rcx
 52cad10:      	xorl	%edx, %edx
 52cad12:      	cmpb	$0x0, 0x75a(%rcx)
 52cad19:      	setne	%dl
 52cad1c:      	leal	0x4(,%rdx,4), %edx
 52cad23:      	callq	*0x210(%rax)
 52cad29:      	addq	$0x8, %rbx
 52cad2d:      	cmpq	%rbx, %r14
 52cad30:      	je	0x52cad91 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cad32:      	movq	(%r15,%rbx), %rax
 52cad36:      	cmpb	$0x1, 0x330(%r12)
 52cad3f:      	jne	0x52cad00 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x380>
 52cad41:      	movq	0x8(%rax), %rsi
 52cad45:      	movq	%r12, %rdi
 52cad48:      	xorl	%edx, %edx
 52cad4a:      	callq	0x526e550 <_ZNK4llvm10AsmPrinter24emitDwarfSymbolReferenceEPKNS_8MCSymbolEb>
 52cad4f:      	addq	$0x8, %rbx
 52cad53:      	cmpq	%rbx, %r14
 52cad56:      	jne	0x52cad32 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3b2>
 52cad58:      	jmp	0x52cad91 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cad5a:      	movb	%cl, %al
 52cad5c:      	leal	0x4(,%rax,4), %ebp
 52cad63:      	xorl	%ebx, %ebx
 52cad65:      	nopw	%cs:(%rax,%rax)
 52cad6f:      	nop
 52cad70:      	movq	0x50(%r12), %rdi
 52cad75:      	movq	(%r15,%rbx), %rax
 52cad79:      	movq	0x10(%rax), %rsi
 52cad7d:      	movq	(%rdi), %rax
 52cad80:      	movl	%ebp, %edx
 52cad82:      	callq	*0x210(%rax)
 52cad88:      	addq	$0x8, %rbx
 52cad8c:      	cmpq	%rbx, %r14
 52cad8f:      	jne	0x52cad70 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3f0>
 52cad91:      	movq	0x58(%rsp), %rdi
 52cad96:      	leaq	0x68(%rsp), %rax
 52cad9b:      	cmpq	%rax, %rdi
 52cad9e:      	je	0x52cada5 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x425>
 52cada0:      	callq	0x828a640 <free@plt>
 52cada5:      	addq	$0x268, %rsp            # imm = 0x268
 52cadac:      	popq	%rbx
 52cadad:      	popq	%r12
 52cadaf:      	popq	%r13
 52cadb1:      	popq	%r14
 52cadb3:      	popq	%r15
 52cadb5:      	popq	%rbp
 52cadb6:      	retq
 52cadb7:      	movq	%r13, %r15
 52cadba:      	jmp	0x52cadf9 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x479>
 52cadbc:      	nopl	(%rax)
 52cadc0:      	movq	%r15, %rdx
 52cadc3:      	subq	%r13, %rdx
 52cadc6:      	movq	%rdx, %rax
 52cadc9:      	sarq	$0x3, %rax
 52cadcd:      	cmpq	$0x2, %rax
 52cadd1:      	jl	0x52cae43 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4c3>
 52cadd3:      	shlq	$0x3, %rax
 52cadd7:      	subq	%rax, %rdi
 52cadda:      	addq	$0x10, %rdi
 52cadde:      	movq	%r13, %rsi
 52cade1:      	callq	0x828abc0 <memmove@plt>
 52cade6:      	movq	%r13, %rax
 52cade9:      	movq	%r12, (%rax)
 52cadec:      	leaq	0x8(%r15), %rbp
 52cadf0:      	cmpq	%rbx, %rbp
 52cadf3:      	je	0x52cab21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1a1>
 52cadf9:      	movq	%r15, %rdi
 52cadfc:      	movq	%rbp, %r15
 52cadff:      	movq	(%rbp), %r12
 52cae03:      	movq	(%r13), %rsi
 52cae07:      	movq	0x10(%r12), %rcx
 52cae0c:      	cmpq	0x10(%rsi), %rcx
 52cae10:      	jb	0x52cadc0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x440>
 52cae12:      	movq	(%rdi), %rdx
 52cae15:      	movq	%r15, %rax
 52cae18:      	cmpq	0x10(%rdx), %rcx
 52cae1c:      	jae	0x52cade9 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52cae1e:      	movq	%r15, %rax
 52cae21:      	nopw	%cs:(%rax,%rax)
 52cae2b:      	nopl	(%rax,%rax)
 52cae30:      	movq	%rdx, (%rax)
 52cae33:      	movq	-0x10(%rax), %rdx
 52cae37:      	addq	$-0x8, %rax
 52cae3b:      	cmpq	0x10(%rdx), %rcx
 52cae3f:      	jb	0x52cae30 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4b0>
 52cae41:      	jmp	0x52cade9 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52cae43:      	movq	%r13, %rax
 52cae46:      	cmpq	$0x8, %rdx
 52cae4a:      	jne	0x52cade9 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52cae4c:      	movq	%rsi, 0x8(%rdi)
 52cae50:      	jmp	0x52cade6 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x466>
 52cae52:      	movq	%rdx, 0x8(%rcx)
 52cae56:      	nopw	%cs:(%rax,%rax)
 52cae60:      	movq	%r13, %rcx
 52cae63:      	movq	%rbx, (%rcx)
 52cae66:      	addq	$0x8, %r15
 52cae6a:      	addq	$0x8, %r12
 52cae6e:      	cmpq	$0x80, %r15
 52cae75:      	je	0x52caed3 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x553>
 52cae77:      	movq	%r14, %rcx
 52cae7a:      	leaq	(%r13,%r15), %r14
 52cae7f:      	movq	(%r13,%r15), %rbx
 52cae84:      	movq	(%r13), %rdx
 52cae88:      	movq	0x10(%rbx), %rax
 52cae8c:      	cmpq	0x10(%rdx), %rax
 52cae90:      	jae	0x52caeb0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x530>
 52cae92:      	cmpq	$0x9, %r15
 52cae96:      	jb	0x52cae52 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4d2>
 52cae98:      	movq	%rbp, %rdi
 52cae9b:      	movq	%r13, %rsi
 52cae9e:      	movq	%r15, %rdx
 52caea1:      	callq	0x828abc0 <memmove@plt>
 52caea6:      	jmp	0x52cae60 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e0>
 52caea8:      	nopl	(%rax,%rax)
 52caeb0:      	movq	(%rcx), %rdx
 52caeb3:      	movq	%r14, %rcx
 52caeb6:      	cmpq	0x10(%rdx), %rax
 52caeba:      	jae	0x52cae63 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e3>
 52caebc:      	movq	%r12, %rcx
 52caebf:      	nop
 52caec0:      	movq	%rdx, (%rcx)
 52caec3:      	movq	-0x10(%rcx), %rdx
 52caec7:      	addq	$-0x8, %rcx
 52caecb:      	cmpq	0x10(%rdx), %rax
 52caecf:      	jb	0x52caec0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x540>
 52caed1:      	jmp	0x52cae63 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e3>
 52caed3:      	subq	$-0x80, %r13
 52caed7:      	movq	0x20(%rsp), %rdi
 52caedc:      	jmp	0x52caef0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x570>
 52caede:      	nop
 52caee0:      	movq	%rax, (%rsi)
 52caee3:      	addq	$0x8, %r13
 52caee7:      	cmpq	%rdi, %r13
 52caeea:      	je	0x52cab21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1a1>
 52caef0:      	movq	-0x8(%r13), %rcx
 52caef4:      	movq	(%r13), %rax
 52caef8:      	movq	0x10(%rax), %rdx
 52caefc:      	movq	%r13, %rsi
 52caeff:      	cmpq	0x10(%rcx), %rdx
 52caf03:      	jae	0x52caee0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x560>
 52caf05:      	movq	%r13, %rsi
 52caf08:      	nopl	(%rax,%rax)
 52caf10:      	movq	%rcx, (%rsi)
 52caf13:      	movq	-0x10(%rsi), %rcx
 52caf17:      	addq	$-0x8, %rsi
 52caf1b:      	cmpq	0x10(%rcx), %rdx
 52caf1f:      	jb	0x52caf10 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x590>
 52caf21:      	jmp	0x52caee0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x560>
