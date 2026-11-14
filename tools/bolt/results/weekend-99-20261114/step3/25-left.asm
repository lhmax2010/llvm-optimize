
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000052caa10 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b>:
 52caa10:      	cmpl	$0x0, 0xc(%rdi)
 52caa14:      	je	0x52cae46 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x436>
 52caa1a:      	pushq	%rbp
 52caa1b:      	pushq	%r15
 52caa1d:      	pushq	%r14
 52caa1f:      	pushq	%r13
 52caa21:      	pushq	%r12
 52caa23:      	pushq	%rbx
 52caa24:      	subq	$0x268, %rsp            # imm = 0x268
 52caa2b:      	movq	%rsi, %rbx
 52caa2e:      	movq	%rdi, %r14
 52caa31:      	movq	%rcx, 0x28(%rsp)
 52caa36:      	movl	%r8d, 0x14(%rsp)
 52caa3b:      	movq	0x50(%rsi), %rdi
 52caa3f:      	movq	(%rdi), %rax
 52caa42:      	movq	%rdx, %rsi
 52caa45:      	xorl	%edx, %edx
 52caa47:      	callq	*0xb0(%rax)
 52caa4d:      	movq	(%r14), %rax
 52caa50:      	movq	%r14, 0x18(%rsp)
 52caa55:      	movl	0x8(%r14), %ecx
 52caa59:      	movq	%rax, %r15
 52caa5c:      	testq	%rcx, %rcx
 52caa5f:      	je	0x52caa82 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x72>
 52caa61:      	movq	%rax, %r15
 52caa64:      	jmp	0x52caa74 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x64>
 52caa66:      	nopw	%cs:(%rax,%rax)
 52caa70:      	addq	$0x8, %r15
 52caa74:      	movq	(%r15), %rdx
 52caa77:      	testq	%rdx, %rdx
 52caa7a:      	je	0x52caa70 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x60>
 52caa7c:      	cmpq	$-0x8, %rdx
 52caa80:      	je	0x52caa70 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x60>
 52caa82:      	movq	%rbx, 0x8(%rsp)
 52caa87:      	leaq	(%rax,%rcx,8), %rbp
 52caa8b:      	leaq	0x68(%rsp), %rax
 52caa90:      	movq	%rax, 0x58(%rsp)
 52caa95:      	movabsq	$0x4000000000, %rax     # imm = 0x4000000000
 52caa9f:      	movq	%rax, 0x60(%rsp)
 52caaa4:      	cmpq	%rbp, %r15
 52caaa7:      	je	0x52cac58 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52caaad:      	xorl	%r14d, %r14d
 52caab0:      	movq	%r15, %rcx
 52caab3:      	nopw	%cs:(%rax,%rax)
 52caabd:      	nopl	(%rax)
 52caac0:      	movq	%r14, %rax
 52caac3:      	nopw	%cs:(%rax,%rax)
 52caacd:      	nopl	(%rax)
 52caad0:      	addq	$0x8, %rcx
 52caad4:      	movq	(%rcx), %rdx
 52caad7:      	testq	%rdx, %rdx
 52caada:      	je	0x52caad0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xc0>
 52caadc:      	cmpq	$-0x8, %rdx
 52caae0:      	je	0x52caad0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xc0>
 52caae2:      	leaq	0x1(%rax), %r14
 52caae6:      	cmpq	%rbp, %rcx
 52caae9:      	jne	0x52caac0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0xb0>
 52caaeb:      	xorl	%r12d, %r12d
 52caaee:      	leaq	0x68(%rsp), %r13
 52caaf3:      	cmpq	$0x40, %rax
 52caaf7:      	jb	0x52cab1a <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x10a>
 52caaf9:      	leaq	0x58(%rsp), %rdi
 52caafe:      	movl	$0x8, %ecx
 52cab03:      	leaq	0x68(%rsp), %rsi
 52cab08:      	movq	%r14, %rdx
 52cab0b:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 52cab10:      	movl	0x60(%rsp), %r12d
 52cab15:      	movq	0x58(%rsp), %r13
 52cab1a:      	movl	%r12d, %eax
 52cab1d:      	leaq	(%r13,%rax,8), %rax
 52cab22:      	movq	(%r15), %rcx
 52cab25:      	nopw	%cs:(%rax,%rax)
 52cab2f:      	nop
 52cab30:      	movq	%rcx, (%rax)
 52cab33:      	nopw	%cs:(%rax,%rax)
 52cab3d:      	nopl	(%rax)
 52cab40:      	addq	$0x8, %r15
 52cab44:      	movq	(%r15), %rcx
 52cab47:      	testq	%rcx, %rcx
 52cab4a:      	je	0x52cab40 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x130>
 52cab4c:      	cmpq	$-0x8, %rcx
 52cab50:      	je	0x52cab40 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x130>
 52cab52:      	addq	$0x8, %rax
 52cab56:      	cmpq	%rbp, %r15
 52cab59:      	jne	0x52cab30 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x120>
 52cab5b:      	addl	%r14d, %r12d
 52cab5e:      	movl	%r12d, 0x60(%rsp)
 52cab63:      	je	0x52cac58 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52cab69:      	leaq	(%r13,%r12,8), %rbx
 52cab6e:      	bsrq	%r12, %rdx
 52cab72:      	xorl	$0x3f, %edx
 52cab75:      	addl	%edx, %edx
 52cab77:      	xorq	$0x7e, %rdx
 52cab7b:      	movq	%r13, %rdi
 52cab7e:      	movq	%rbx, %rsi
 52cab81:      	callq	0x52cb0a0 <_ZSt16__introsort_loopIPPKN4llvm14StringMapEntryINS0_20DwarfStringPoolEntryEEElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS0_15DwarfStringPool4emitERNS0_10AsmPrinterEPNS0_9MCSectionESE_bE3$_0EEEvT_SH_T0_T1_>
 52cab86:      	leaq	0x8(%r13), %rbp
 52cab8a:      	cmpl	$0x11, %r12d
 52cab8e:      	jb	0x52caba6 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x196>
 52cab90:      	movq	%rbx, 0x20(%rsp)
 52cab95:      	movl	$0x8, %r15d
 52cab9b:      	movq	%rbp, %r12
 52cab9e:      	movq	%r13, %r14
 52caba1:      	jmp	0x52caf07 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4f7>
 52caba6:      	cmpl	$0x1, %r12d
 52cabaa:      	jne	0x52cae47 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x437>
 52cabb0:      	movl	0x60(%rsp), %r15d
 52cabb5:      	testq	%r15, %r15
 52cabb8:      	je	0x52cac58 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52cabbe:      	shlq	$0x3, %r15
 52cabc2:      	movq	0x58(%rsp), %r12
 52cabc7:      	xorl	%r13d, %r13d
 52cabca:      	leaq	-0x4529c27(%rip), %rbp  # 0xda0faa <.L.str.10>
 52cabd1:      	leaq	0x30(%rsp), %r14
 52cabd6:      	movq	0x8(%rsp), %rbx
 52cabdb:      	jmp	0x52cac2f <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x21f>
 52cabdd:      	nopl	(%rax)
 52cabe0:      	movq	0x50(%rbx), %rdi
 52cabe4:      	movq	(%r12,%r13), %rax
 52cabe8:      	movq	0x10(%rax), %rax
 52cabec:      	movq	%rbp, 0x30(%rsp)
 52cabf1:      	movq	%rax, 0x40(%rsp)
 52cabf6:      	movw	$0xb03, 0x50(%rsp)      # imm = 0xB03
 52cabfd:      	movq	(%rdi), %rax
 52cac00:      	movq	%r14, %rsi
 52cac03:      	movl	$0x1, %edx
 52cac08:      	callq	*0x78(%rax)
 52cac0b:      	movq	0x50(%rbx), %rdi
 52cac0f:      	movq	(%r12,%r13), %rsi
 52cac13:      	movq	(%rsi), %rdx
 52cac16:      	addq	$0x20, %rsi
 52cac1a:      	incq	%rdx
 52cac1d:      	movq	(%rdi), %rax
 52cac20:      	callq	*0x1f8(%rax)
 52cac26:      	addq	$0x8, %r13
 52cac2a:      	cmpq	%r13, %r15
 52cac2d:      	je	0x52cac58 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x248>
 52cac2f:      	movq	0x18(%rsp), %rax
 52cac34:      	cmpb	$0x1, 0x3c(%rax)
 52cac38:      	jne	0x52cabe0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1d0>
 52cac3a:      	movq	0x8(%rsp), %rax
 52cac3f:      	movq	0x50(%rax), %rdi
 52cac43:      	movq	(%r12,%r13), %rax
 52cac47:      	movq	0x8(%rax), %rsi
 52cac4b:      	movq	(%rdi), %rax
 52cac4e:      	xorl	%edx, %edx
 52cac50:      	callq	*0xc8(%rax)
 52cac56:      	jmp	0x52cabe0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1d0>
 52cac58:      	movq	0x28(%rsp), %rbx
 52cac5d:      	testq	%rbx, %rbx
 52cac60:      	movq	0x8(%rsp), %r12
 52cac65:      	je	0x52cae21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cac6b:      	movq	0x18(%rsp), %r15
 52cac70:      	movl	0x38(%r15), %r14d
 52cac74:      	movl	0x60(%rsp), %eax
 52cac78:      	cmpl	%eax, %r14d
 52cac7b:      	je	0x52caccb <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2bb>
 52cac7d:      	jb	0x52cacc6 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2b6>
 52cac7f:      	cmpl	0x64(%rsp), %r14d
 52cac84:      	jbe	0x52caca1 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x291>
 52cac86:      	leaq	0x58(%rsp), %rdi
 52cac8b:      	movl	$0x8, %ecx
 52cac90:      	leaq	0x68(%rsp), %rsi
 52cac95:      	movq	%r14, %rdx
 52cac98:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 52cac9d:      	movl	0x60(%rsp), %eax
 52caca1:      	cmpl	%eax, %r14d
 52caca4:      	je	0x52cacc6 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2b6>
 52caca6:      	movl	%eax, %eax
 52caca8:      	leaq	(,%rax,8), %rdi
 52cacb0:      	addq	0x58(%rsp), %rdi
 52cacb5:      	movq	%r14, %rdx
 52cacb8:      	subq	%rax, %rdx
 52cacbb:      	shlq	$0x3, %rdx
 52cacbf:      	xorl	%esi, %esi
 52cacc1:      	callq	0x828ac20 <memset@plt>
 52cacc6:      	movl	%r14d, 0x60(%rsp)
 52caccb:      	movq	(%r15), %rcx
 52cacce:      	movl	0x8(%r15), %edx
 52cacd2:      	movq	%rcx, %rax
 52cacd5:      	testq	%rdx, %rdx
 52cacd8:      	je	0x52cacf2 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2e2>
 52cacda:      	movq	%rcx, %rax
 52cacdd:      	jmp	0x52cace4 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d4>
 52cacdf:      	nop
 52cace0:      	addq	$0x8, %rax
 52cace4:      	movq	(%rax), %rsi
 52cace7:      	testq	%rsi, %rsi
 52cacea:      	je	0x52cace0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d0>
 52cacec:      	cmpq	$-0x8, %rsi
 52cacf0:      	je	0x52cace0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x2d0>
 52cacf2:      	leaq	(%rcx,%rdx,8), %rcx
 52cacf6:      	cmpq	%rcx, %rax
 52cacf9:      	je	0x52cad37 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x327>
 52cacfb:      	movq	0x58(%rsp), %rdx
 52cad00:      	movq	(%rax), %rdi
 52cad03:      	movl	$0xffffffff, %esi       # imm = 0xFFFFFFFF
 52cad08:      	nopl	(%rax,%rax)
 52cad10:      	movl	0x18(%rdi), %r8d
 52cad14:      	cmpq	%rsi, %r8
 52cad17:      	je	0x52cad20 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52cad19:      	movq	%rdi, (%rdx,%r8,8)
 52cad1d:      	nopl	(%rax)
 52cad20:      	addq	$0x8, %rax
 52cad24:      	movq	(%rax), %rdi
 52cad27:      	testq	%rdi, %rdi
 52cad2a:      	je	0x52cad20 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52cad2c:      	cmpq	$-0x8, %rdi
 52cad30:      	je	0x52cad20 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x310>
 52cad32:      	cmpq	%rcx, %rax
 52cad35:      	jne	0x52cad10 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x300>
 52cad37:      	movq	0x50(%r12), %rdi
 52cad3c:      	movq	(%rdi), %rax
 52cad3f:      	movq	%rbx, %rsi
 52cad42:      	xorl	%edx, %edx
 52cad44:      	callq	*0xb0(%rax)
 52cad4a:      	movq	0x50(%r12), %rax
 52cad4f:      	movq	0x8(%rax), %rcx
 52cad53:      	xorl	%eax, %eax
 52cad55:      	cmpb	$0x0, 0x75a(%rcx)
 52cad5c:      	setne	%cl
 52cad5f:      	movl	0x60(%rsp), %r14d
 52cad64:      	testq	%r14, %r14
 52cad67:      	je	0x52cae21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cad6d:      	movq	0x58(%rsp), %r15
 52cad72:      	shlq	$0x3, %r14
 52cad76:      	cmpb	$0x0, 0x14(%rsp)
 52cad7b:      	je	0x52cadea <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3da>
 52cad7d:      	xorl	%ebx, %ebx
 52cad7f:      	jmp	0x52cadc2 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3b2>
 52cad81:      	nopw	%cs:(%rax,%rax)
 52cad8b:      	nopl	(%rax,%rax)
 52cad90:      	movq	0x10(%rax), %rsi
 52cad94:      	movq	0x50(%r12), %rdi
 52cad99:      	movq	(%rdi), %rax
 52cad9c:      	movq	0x8(%rdi), %rcx
 52cada0:      	xorl	%edx, %edx
 52cada2:      	cmpb	$0x0, 0x75a(%rcx)
 52cada9:      	setne	%dl
 52cadac:      	leal	0x4(,%rdx,4), %edx
 52cadb3:      	callq	*0x210(%rax)
 52cadb9:      	addq	$0x8, %rbx
 52cadbd:      	cmpq	%rbx, %r14
 52cadc0:      	je	0x52cae21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cadc2:      	movq	(%r15,%rbx), %rax
 52cadc6:      	cmpb	$0x1, 0x330(%r12)
 52cadcf:      	jne	0x52cad90 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x380>
 52cadd1:      	movq	0x8(%rax), %rsi
 52cadd5:      	movq	%r12, %rdi
 52cadd8:      	xorl	%edx, %edx
 52cadda:      	callq	0x526e5e0 <_ZNK4llvm10AsmPrinter24emitDwarfSymbolReferenceEPKNS_8MCSymbolEb>
 52caddf:      	addq	$0x8, %rbx
 52cade3:      	cmpq	%rbx, %r14
 52cade6:      	jne	0x52cadc2 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3b2>
 52cade8:      	jmp	0x52cae21 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x411>
 52cadea:      	movb	%cl, %al
 52cadec:      	leal	0x4(,%rax,4), %ebp
 52cadf3:      	xorl	%ebx, %ebx
 52cadf5:      	nopw	%cs:(%rax,%rax)
 52cadff:      	nop
 52cae00:      	movq	0x50(%r12), %rdi
 52cae05:      	movq	(%r15,%rbx), %rax
 52cae09:      	movq	0x10(%rax), %rsi
 52cae0d:      	movq	(%rdi), %rax
 52cae10:      	movl	%ebp, %edx
 52cae12:      	callq	*0x210(%rax)
 52cae18:      	addq	$0x8, %rbx
 52cae1c:      	cmpq	%rbx, %r14
 52cae1f:      	jne	0x52cae00 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x3f0>
 52cae21:      	movq	0x58(%rsp), %rdi
 52cae26:      	leaq	0x68(%rsp), %rax
 52cae2b:      	cmpq	%rax, %rdi
 52cae2e:      	je	0x52cae35 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x425>
 52cae30:      	callq	0x828a6d0 <free@plt>
 52cae35:      	addq	$0x268, %rsp            # imm = 0x268
 52cae3c:      	popq	%rbx
 52cae3d:      	popq	%r12
 52cae3f:      	popq	%r13
 52cae41:      	popq	%r14
 52cae43:      	popq	%r15
 52cae45:      	popq	%rbp
 52cae46:      	retq
 52cae47:      	movq	%r13, %r15
 52cae4a:      	jmp	0x52cae89 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x479>
 52cae4c:      	nopl	(%rax)
 52cae50:      	movq	%r15, %rdx
 52cae53:      	subq	%r13, %rdx
 52cae56:      	movq	%rdx, %rax
 52cae59:      	sarq	$0x3, %rax
 52cae5d:      	cmpq	$0x2, %rax
 52cae61:      	jl	0x52caed3 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4c3>
 52cae63:      	shlq	$0x3, %rax
 52cae67:      	subq	%rax, %rdi
 52cae6a:      	addq	$0x10, %rdi
 52cae6e:      	movq	%r13, %rsi
 52cae71:      	callq	0x828ac50 <memmove@plt>
 52cae76:      	movq	%r13, %rax
 52cae79:      	movq	%r12, (%rax)
 52cae7c:      	leaq	0x8(%r15), %rbp
 52cae80:      	cmpq	%rbx, %rbp
 52cae83:      	je	0x52cabb0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1a0>
 52cae89:      	movq	%r15, %rdi
 52cae8c:      	movq	%rbp, %r15
 52cae8f:      	movq	(%rbp), %r12
 52cae93:      	movq	(%r13), %rsi
 52cae97:      	movq	0x10(%r12), %rcx
 52cae9c:      	cmpq	0x10(%rsi), %rcx
 52caea0:      	jb	0x52cae50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x440>
 52caea2:      	movq	(%rdi), %rdx
 52caea5:      	movq	%r15, %rax
 52caea8:      	cmpq	0x10(%rdx), %rcx
 52caeac:      	jae	0x52cae79 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52caeae:      	movq	%r15, %rax
 52caeb1:      	nopw	%cs:(%rax,%rax)
 52caebb:      	nopl	(%rax,%rax)
 52caec0:      	movq	%rdx, (%rax)
 52caec3:      	movq	-0x10(%rax), %rdx
 52caec7:      	addq	$-0x8, %rax
 52caecb:      	cmpq	0x10(%rdx), %rcx
 52caecf:      	jb	0x52caec0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4b0>
 52caed1:      	jmp	0x52cae79 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52caed3:      	movq	%r13, %rax
 52caed6:      	cmpq	$0x8, %rdx
 52caeda:      	jne	0x52cae79 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x469>
 52caedc:      	movq	%rsi, 0x8(%rdi)
 52caee0:      	jmp	0x52cae76 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x466>
 52caee2:      	movq	%rdx, 0x8(%rcx)
 52caee6:      	nopw	%cs:(%rax,%rax)
 52caef0:      	movq	%r13, %rcx
 52caef3:      	movq	%rbx, (%rcx)
 52caef6:      	addq	$0x8, %r15
 52caefa:      	addq	$0x8, %r12
 52caefe:      	cmpq	$0x80, %r15
 52caf05:      	je	0x52caf63 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x553>
 52caf07:      	movq	%r14, %rcx
 52caf0a:      	leaq	(%r13,%r15), %r14
 52caf0f:      	movq	(%r13,%r15), %rbx
 52caf14:      	movq	(%r13), %rdx
 52caf18:      	movq	0x10(%rbx), %rax
 52caf1c:      	cmpq	0x10(%rdx), %rax
 52caf20:      	jae	0x52caf40 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x530>
 52caf22:      	cmpq	$0x9, %r15
 52caf26:      	jb	0x52caee2 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4d2>
 52caf28:      	movq	%rbp, %rdi
 52caf2b:      	movq	%r13, %rsi
 52caf2e:      	movq	%r15, %rdx
 52caf31:      	callq	0x828ac50 <memmove@plt>
 52caf36:      	jmp	0x52caef0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e0>
 52caf38:      	nopl	(%rax,%rax)
 52caf40:      	movq	(%rcx), %rdx
 52caf43:      	movq	%r14, %rcx
 52caf46:      	cmpq	0x10(%rdx), %rax
 52caf4a:      	jae	0x52caef3 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e3>
 52caf4c:      	movq	%r12, %rcx
 52caf4f:      	nop
 52caf50:      	movq	%rdx, (%rcx)
 52caf53:      	movq	-0x10(%rcx), %rdx
 52caf57:      	addq	$-0x8, %rcx
 52caf5b:      	cmpq	0x10(%rdx), %rax
 52caf5f:      	jb	0x52caf50 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x540>
 52caf61:      	jmp	0x52caef3 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x4e3>
 52caf63:      	subq	$-0x80, %r13
 52caf67:      	movq	0x20(%rsp), %rdi
 52caf6c:      	jmp	0x52caf80 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x570>
 52caf6e:      	nop
 52caf70:      	movq	%rax, (%rsi)
 52caf73:      	addq	$0x8, %r13
 52caf77:      	cmpq	%rdi, %r13
 52caf7a:      	je	0x52cabb0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x1a0>
 52caf80:      	movq	-0x8(%r13), %rcx
 52caf84:      	movq	(%r13), %rax
 52caf88:      	movq	0x10(%rax), %rdx
 52caf8c:      	movq	%r13, %rsi
 52caf8f:      	cmpq	0x10(%rcx), %rdx
 52caf93:      	jae	0x52caf70 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x560>
 52caf95:      	movq	%r13, %rsi
 52caf98:      	nopl	(%rax,%rax)
 52cafa0:      	movq	%rcx, (%rsi)
 52cafa3:      	movq	-0x10(%rsi), %rcx
 52cafa7:      	addq	$-0x8, %rsi
 52cafab:      	cmpq	0x10(%rcx), %rdx
 52cafaf:      	jb	0x52cafa0 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x590>
 52cafb1:      	jmp	0x52caf70 <_ZN4llvm15DwarfStringPool4emitERNS_10AsmPrinterEPNS_9MCSectionES4_b+0x560>
