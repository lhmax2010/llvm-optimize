
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005286e10 <_ZN4llvm10DwarfDebug16emitDebugARangesEv>:
 5286e10:      	pushq	%rbp
 5286e11:      	pushq	%r15
 5286e13:      	pushq	%r14
 5286e15:      	pushq	%r13
 5286e17:      	pushq	%r12
 5286e19:      	pushq	%rbx
 5286e1a:      	subq	$0xc8, %rsp
 5286e21:      	movq	0x298(%rdi), %rbx
 5286e28:      	movq	0x2a0(%rdi), %r13
 5286e2f:      	cmpq	%r13, %rbx
 5286e32:      	je	0x528818a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x137a>
 5286e38:      	movq	%rdi, 0x38(%rsp)
 5286e3d:      	xorps	%xmm0, %xmm0
 5286e40:      	movaps	%xmm0, 0x40(%rsp)
 5286e45:      	movl	$0x0, 0x50(%rsp)
 5286e4d:      	leaq	0x68(%rsp), %rax
 5286e52:      	movq	%rax, 0x58(%rsp)
 5286e57:      	movq	$0x0, 0x60(%rsp)
 5286e60:      	leaq	0x32e5899(%rip), %r14   # 0x856c700 <_ZN4llvm8MCSymbol22AbsolutePseudoFragmentE>
 5286e67:      	leaq	0x40(%rsp), %r15
 5286e6c:      	leaq	0x90(%rsp), %r12
 5286e74:      	nopw	%cs:(%rax,%rax)
 5286e7e:      	nop
 5286e80:      	movq	(%rbx), %rbp
 5286e83:      	movq	(%rbp), %rax
 5286e87:      	testq	%rax, %rax
 5286e8a:      	je	0x5286ec0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb0>
 5286e8c:      	testq	%rax, %rax
 5286e8f:      	je	0x5286ef0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286e91:      	cmpq	(%r14), %rax
 5286e94:      	je	0x5286ef0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286e96:      	movq	(%rbx), %rbp
 5286e99:      	movq	(%rbp), %rax
 5286e9d:      	testq	%rax, %rax
 5286ea0:      	jne	0x5286eaf <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x9f>
 5286ea2:      	movq	0x10(%rbp), %rdi
 5286ea6:      	callq	0x3e5bc80 <_ZNK4llvm6MCExpr22findAssociatedFragmentEv>
 5286eab:      	movq	%rax, (%rbp)
 5286eaf:      	movq	0x8(%rax), %rax
 5286eb3:      	movq	%rax, 0x90(%rsp)
 5286ebb:      	jmp	0x5286efc <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xec>
 5286ebd:      	nopl	(%rax)
 5286ec0:      	movl	0x8(%rbp), %eax
 5286ec3:      	movl	$0x103, %ecx            # imm = 0x103
 5286ec8:      	andl	%ecx, %eax
 5286eca:      	cmpl	$0x1, %eax
 5286ecd:      	jne	0x5286ef0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286ecf:      	movq	0x10(%rbp), %rdi
 5286ed3:      	callq	0x3e5bc80 <_ZNK4llvm6MCExpr22findAssociatedFragmentEv>
 5286ed8:      	movq	%rax, (%rbp)
 5286edc:      	testq	%rax, %rax
 5286edf:      	jne	0x5286e91 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x81>
 5286ee1:      	nopw	%cs:(%rax,%rax)
 5286eeb:      	nopl	(%rax,%rax)
 5286ef0:      	movq	$0x0, 0x90(%rsp)
 5286efc:      	movq	%r15, %rdi
 5286eff:      	movq	%r12, %rsi
 5286f02:      	callq	0x3e1e2a0 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_9MCSectionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E24lookupOrInsertIntoBucketIRKS3_JEEESt4pairIPS8_bEOT_DpOT0_>
 5286f07:      	cmpb	$0x1, %dl
 5286f0a:      	jne	0x5286f70 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x160>
 5286f0c:      	movl	0x60(%rsp), %ecx
 5286f10:      	movl	%ecx, 0x8(%rax)
 5286f13:      	cmpl	0x64(%rsp), %ecx
 5286f17:      	jae	0x5286fce <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1be>
 5286f1d:      	movq	0x58(%rsp), %rax
 5286f22:      	imulq	$0x98, %rcx, %rcx
 5286f29:      	movq	0x90(%rsp), %rdx
 5286f31:      	movq	%rdx, (%rax,%rcx)
 5286f35:      	leaq	0x18(%rax,%rcx), %rdx
 5286f3a:      	movq	%rdx, 0x8(%rax,%rcx)
 5286f3f:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 5286f49:      	movq	%rdx, 0x10(%rax,%rcx)
 5286f4e:      	movl	0x60(%rsp), %eax
 5286f52:      	incl	%eax
 5286f54:      	movl	%eax, 0x60(%rsp)
 5286f58:      	movq	0x58(%rsp), %rcx
 5286f5d:      	movl	%eax, %eax
 5286f5f:      	imulq	$0x98, %rax, %rax
 5286f66:      	leaq	-0x98(%rcx,%rax), %rbp
 5286f6e:      	jmp	0x5286f7f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x16f>
 5286f70:      	movl	0x8(%rax), %eax
 5286f73:      	imulq	$0x98, %rax, %rbp
 5286f7a:      	addq	0x58(%rsp), %rbp
 5286f7f:      	movups	(%rbx), %xmm0
 5286f82:      	movl	0x10(%rbp), %edx
 5286f85:      	cmpl	0x14(%rbp), %edx
 5286f88:      	jae	0x5286faa <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x19a>
 5286f8a:      	movq	0x8(%rbp), %rax
 5286f8e:      	movl	%edx, %ecx
 5286f90:      	shlq	$0x4, %rcx
 5286f94:      	movups	%xmm0, (%rax,%rcx)
 5286f98:      	incl	0x10(%rbp)
 5286f9b:      	addq	$0x10, %rbx
 5286f9f:      	cmpq	%r13, %rbx
 5286fa2:      	jne	0x5286e80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x70>
 5286fa8:      	jmp	0x5286fe4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1d4>
 5286faa:      	leaq	0x8(%rbp), %rdi
 5286fae:      	incq	%rdx
 5286fb1:      	leaq	0x18(%rbp), %rsi
 5286fb5:      	movl	$0x10, %ecx
 5286fba:      	movaps	%xmm0, 0x70(%rsp)
 5286fbf:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 5286fc4:      	movaps	0x70(%rsp), %xmm0
 5286fc9:      	movl	0x10(%rbp), %edx
 5286fcc:      	jmp	0x5286f8a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x17a>
 5286fce:      	leaq	0x58(%rsp), %rdi
 5286fd3:      	movq	%r12, %rsi
 5286fd6:      	callq	0x52a7720 <_ZN4llvm23SmallVectorTemplateBaseISt4pairIPNS_9MCSectionENS_11SmallVectorINS_8SymbolCUELj8EEEELb0EE18growAndEmplaceBackIJRKSt21piecewise_construct_tSt5tupleIJRKS3_EESD_IJEEEEERS7_DpOT_>
 5286fdb:      	movl	0x60(%rsp), %eax
 5286fdf:      	jmp	0x5286f58 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x148>
 5286fe4:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 5286fee:      	movq	%rax, 0x80(%rsp)
 5286ff6:      	xorps	%xmm0, %xmm0
 5286ff9:      	movaps	%xmm0, 0x10(%rsp)
 5286ffe:      	movl	$0x0, 0x20(%rsp)
 5287006:      	movl	0x60(%rsp), %eax
 528700a:      	testq	%rax, %rax
 528700d:      	je	0x528768e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x87e>
 5287013:      	movq	0x58(%rsp), %r15
 5287018:      	imulq	$0x98, %rax, %rax
 528701f:      	addq	%r15, %rax
 5287022:      	movq	%rax, 0xb8(%rsp)
 528702a:      	movq	0x38(%rsp), %r14
 528702f:      	jmp	0x528705d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x24d>
 5287031:      	nopw	%cs:(%rax,%rax)
 528703b:      	nopl	(%rax,%rax)
 5287040:      	movq	0x88(%rsp), %r15
 5287048:      	addq	$0x98, %r15
 528704f:      	cmpq	0xb8(%rsp), %r15
 5287057:      	je	0x528767a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x86a>
 528705d:      	movq	(%r15), %rsi
 5287060:      	testq	%rsi, %rsi
 5287063:      	movq	%r15, 0x88(%rsp)
 528706b:      	je	0x52873a0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x590>
 5287071:      	leaq	0x8(%r15), %r13
 5287075:      	movq	0x8(%r14), %rax
 5287079:      	movq	0x50(%rax), %rdi
 528707d:      	callq	0x3e7cab0 <_ZN4llvm10MCStreamer10endSectionEPNS_9MCSectionE>
 5287082:      	movl	0x10(%r15), %edx
 5287086:      	cmpl	0x14(%r15), %edx
 528708a:      	jae	0x5287657 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x847>
 5287090:      	movq	0x8(%r15), %rcx
 5287094:      	movl	%edx, %edx
 5287096:      	shlq	$0x4, %rdx
 528709a:      	movq	%rax, (%rcx,%rdx)
 528709e:      	movq	$0x0, 0x8(%rcx,%rdx)
 52870a7:      	movl	0x10(%r15), %ebp
 52870ab:      	incl	%ebp
 52870ad:      	movl	%ebp, 0x10(%r15)
 52870b1:      	cmpl	$0x2, %ebp
 52870b4:      	jb	0x5287040 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 52870b6:      	movq	(%r13), %rax
 52870ba:      	movq	(%rax), %r11
 52870bd:      	movl	$0x1, %ebx
 52870c2:      	movq	%r13, 0x28(%rsp)
 52870c7:      	movq	%rbp, 0xc0(%rsp)
 52870cf:      	jmp	0x5287105 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2f5>
 52870d1:      	nopw	%cs:(%rax,%rax)
 52870db:      	nopl	(%rax,%rax)
 52870e0:      	movq	%r11, (%r12)
 52870e4:      	movq	0x70(%rsp), %rax
 52870e9:      	movq	%rax, 0x8(%r12)
 52870ee:      	addq	$0x10, %r12
 52870f2:      	movq	%r12, 0x10(%r10)
 52870f6:      	movq	(%r15), %r11
 52870f9:      	incq	%rbx
 52870fc:      	cmpq	%rbp, %rbx
 52870ff:      	je	0x5287040 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 5287105:      	movq	(%r13), %r15
 5287109:      	movq	%rbx, %rcx
 528710c:      	shlq	$0x4, %rcx
 5287110:      	movq	-0x8(%r15,%rcx), %rax
 5287115:      	cmpq	%rax, 0x8(%r15,%rcx)
 528711a:      	je	0x52870f9 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2e9>
 528711c:      	addq	%rcx, %r15
 528711f:      	movq	(%r15), %rcx
 5287122:      	movq	%rcx, 0x70(%rsp)
 5287127:      	movl	0x20(%rsp), %esi
 528712b:      	testl	%esi, %esi
 528712d:      	je	0x52871a0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x390>
 528712f:      	movq	0x10(%rsp), %rcx
 5287134:      	movl	%eax, %edi
 5287136:      	shrl	$0x4, %edi
 5287139:      	movl	%eax, %edx
 528713b:      	shrl	$0x9, %edx
 528713e:      	xorl	%edi, %edx
 5287140:      	leal	-0x1(%rsi), %edi
 5287143:      	andl	%edi, %edx
 5287145:      	movq	%rdx, %r8
 5287148:      	shlq	$0x5, %r8
 528714c:      	leaq	(%rcx,%r8), %r10
 5287150:      	movq	(%rcx,%r8), %r12
 5287154:      	cmpq	%r12, %rax
 5287157:      	je	0x52871fa <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3ea>
 528715d:      	movl	$0x1, %r8d
 5287163:      	xorl	%r9d, %r9d
 5287166:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 528716d:      	je	0x52872d4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4c4>
 5287173:      	xorq	$-0x2000, %r12          # imm = 0xE000
 528717a:      	orq	%r9, %r12
 528717d:      	cmoveq	%r10, %r9
 5287181:      	addl	%r8d, %edx
 5287184:      	incl	%r8d
 5287187:      	andl	%edi, %edx
 5287189:      	movq	%rdx, %r12
 528718c:      	shlq	$0x5, %r12
 5287190:      	leaq	(%rcx,%r12), %r10
 5287194:      	movq	(%rcx,%r12), %r12
 5287198:      	cmpq	%r12, %rax
 528719b:      	je	0x52871fa <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3ea>
 528719d:      	jmp	0x5287166 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x356>
 528719f:      	nop
 52871a0:      	xorl	%r10d, %r10d
 52871a3:      	movl	0x18(%rsp), %eax
 52871a7:      	leal	0x4(,%rax,4), %ecx
 52871ae:      	leal	(%rsi,%rsi,2), %edx
 52871b1:      	cmpl	%edx, %ecx
 52871b3:      	jae	0x52872e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4d0>
 52871b9:      	movl	%eax, %ecx
 52871bb:      	notl	%ecx
 52871bd:      	addl	%esi, %ecx
 52871bf:      	subl	0x1c(%rsp), %ecx
 52871c3:      	movl	%esi, %edx
 52871c5:      	shrl	$0x3, %edx
 52871c8:      	cmpl	%edx, %ecx
 52871ca:      	jbe	0x52872e2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4d2>
 52871d0:      	incl	%eax
 52871d2:      	movl	%eax, 0x18(%rsp)
 52871d6:      	cmpq	$-0x1000, (%r10)        # imm = 0xF000
 52871dd:      	je	0x52871e3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3d3>
 52871df:      	decl	0x1c(%rsp)
 52871e3:      	movq	-0x8(%r15), %rax
 52871e7:      	movq	%rax, (%r10)
 52871ea:      	xorps	%xmm0, %xmm0
 52871ed:      	movups	%xmm0, 0x8(%r10)
 52871f2:      	movq	$0x0, 0x18(%r10)
 52871fa:      	movq	0x10(%r10), %r12
 52871fe:      	cmpq	0x18(%r10), %r12
 5287202:      	jne	0x52870e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2d0>
 5287208:      	movq	%r15, 0x8(%rsp)
 528720d:      	movq	%r10, 0x30(%rsp)
 5287212:      	movq	0x8(%r10), %rbp
 5287216:      	subq	%rbp, %r12
 5287219:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 5287223:      	cmpq	%rax, %r12
 5287226:      	je	0x528819c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 528722c:      	movq	%r11, %r15
 528722f:      	movq	%r12, %rax
 5287232:      	sarq	$0x4, %rax
 5287236:      	cmpq	$0x1, %rax
 528723a:      	movq	%rax, %rcx
 528723d:      	adcq	$0x0, %rcx
 5287241:      	leaq	(%rcx,%rax), %r13
 5287245:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 528724f:      	cmpq	%rdx, %r13
 5287252:      	cmovaeq	%rdx, %r13
 5287256:      	addq	%rax, %rcx
 5287259:      	cmovbq	%rdx, %r13
 528725d:      	shlq	$0x4, %r13
 5287261:      	movq	%r13, %rdi
 5287264:      	callq	0x828a620 <_Znwm@plt>
 5287269:      	movq	%rax, %r14
 528726c:      	movq	%r15, (%rax,%r12)
 5287270:      	movq	0x70(%rsp), %rax
 5287275:      	movq	%rax, 0x8(%r14,%r12)
 528727a:      	testq	%r12, %r12
 528727d:      	jle	0x528728d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x47d>
 528727f:      	movq	%r14, %rdi
 5287282:      	movq	%rbp, %rsi
 5287285:      	movq	%r12, %rdx
 5287288:      	callq	0x828ac50 <memcpy@plt>
 528728d:      	testq	%rbp, %rbp
 5287290:      	movq	0x8(%rsp), %r15
 5287295:      	je	0x52872a2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x492>
 5287297:      	movq	%rbp, %rdi
 528729a:      	movq	%r12, %rsi
 528729d:      	callq	0x828a660 <_ZdlPvm@plt>
 52872a2:      	addq	%r14, %r12
 52872a5:      	addq	$0x10, %r12
 52872a9:      	movq	0x30(%rsp), %rax
 52872ae:      	movq	%r14, 0x8(%rax)
 52872b2:      	movq	%r12, 0x10(%rax)
 52872b6:      	addq	%r14, %r13
 52872b9:      	movq	%r13, 0x18(%rax)
 52872bd:      	movq	0x38(%rsp), %r14
 52872c2:      	movq	0x28(%rsp), %r13
 52872c7:      	movq	0xc0(%rsp), %rbp
 52872cf:      	jmp	0x52870f6 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2e6>
 52872d4:      	testq	%r9, %r9
 52872d7:      	cmovneq	%r9, %r10
 52872db:      	jmp	0x52871a3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x393>
 52872e0:      	addl	%esi, %esi
 52872e2:      	movq	%r11, %r12
 52872e5:      	leaq	0x10(%rsp), %rdi
 52872ea:      	callq	0x52a7980 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 52872ef:      	movl	0x20(%rsp), %eax
 52872f3:      	testl	%eax, %eax
 52872f5:      	je	0x5287367 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x557>
 52872f7:      	movq	0x10(%rsp), %rcx
 52872fc:      	movq	-0x8(%r15), %rdx
 5287300:      	movl	%edx, %edi
 5287302:      	shrl	$0x4, %edi
 5287305:      	movl	%edx, %esi
 5287307:      	shrl	$0x9, %esi
 528730a:      	xorl	%edi, %esi
 528730c:      	decl	%eax
 528730e:      	andl	%eax, %esi
 5287310:      	movq	%rsi, %rdi
 5287313:      	shlq	$0x5, %rdi
 5287317:      	leaq	(%rcx,%rdi), %r10
 528731b:      	movq	(%rcx,%rdi), %r9
 528731f:      	cmpq	%r9, %rdx
 5287322:      	je	0x528736a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55a>
 5287324:      	movl	$0x1, %edi
 5287329:      	xorl	%r8d, %r8d
 528732c:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 5287333:      	je	0x5287389 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x579>
 5287335:      	xorq	$-0x2000, %r9           # imm = 0xE000
 528733c:      	orq	%r8, %r9
 528733f:      	cmoveq	%r10, %r8
 5287343:      	addl	%edi, %esi
 5287345:      	incl	%edi
 5287347:      	andl	%eax, %esi
 5287349:      	movq	%rsi, %r9
 528734c:      	shlq	$0x5, %r9
 5287350:      	leaq	(%rcx,%r9), %r10
 5287354:      	movq	(%rcx,%r9), %r9
 5287358:      	cmpq	%r9, %rdx
 528735b:      	movq	0x38(%rsp), %r14
 5287360:      	movq	%r12, %r11
 5287363:      	je	0x528736d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55d>
 5287365:      	jmp	0x528732c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x51c>
 5287367:      	xorl	%r10d, %r10d
 528736a:      	movq	%r12, %r11
 528736d:      	movl	0x18(%rsp), %eax
 5287371:      	incl	%eax
 5287373:      	movl	%eax, 0x18(%rsp)
 5287377:      	cmpq	$-0x1000, (%r10)        # imm = 0xF000
 528737e:      	jne	0x52871df <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3cf>
 5287384:      	jmp	0x52871e3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3d3>
 5287389:      	testq	%r8, %r8
 528738c:      	cmovneq	%r8, %r10
 5287390:      	movq	0x38(%rsp), %r14
 5287395:      	jmp	0x528736a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55a>
 5287397:      	nopw	(%rax,%rax)
 52873a0:      	movl	0x10(%r15), %r12d
 52873a4:      	testq	%r12, %r12
 52873a7:      	je	0x5287040 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 52873ad:      	movq	0x88(%rsp), %rax
 52873b5:      	movq	0x8(%rax), %rbx
 52873b9:      	shlq	$0x4, %r12
 52873bd:      	addq	%rbx, %r12
 52873c0:      	movq	0x10(%rsp), %r10
 52873c5:      	movq	%r12, 0x30(%rsp)
 52873ca:      	jmp	0x52873f5 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5e5>
 52873cc:      	nopl	(%rax)
 52873d0:      	movq	%r13, (%r15)
 52873d3:      	movq	$0x0, 0x8(%r15)
 52873db:      	addq	$0x10, %r15
 52873df:      	movq	%r15, 0x10(%r14)
 52873e3:      	addq	$0x10, %rbx
 52873e7:      	cmpq	%r12, %rbx
 52873ea:      	movq	0x38(%rsp), %r14
 52873ef:      	je	0x5287040 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 52873f5:      	movq	(%rbx), %r13
 52873f8:      	movl	0x20(%rsp), %esi
 52873fc:      	testl	%esi, %esi
 52873fe:      	je	0x5287470 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x660>
 5287400:      	movq	0x8(%rbx), %rax
 5287404:      	movl	%eax, %edx
 5287406:      	shrl	$0x4, %edx
 5287409:      	movl	%eax, %ecx
 528740b:      	shrl	$0x9, %ecx
 528740e:      	xorl	%edx, %ecx
 5287410:      	leal	-0x1(%rsi), %edx
 5287413:      	andl	%edx, %ecx
 5287415:      	movq	%rcx, %rdi
 5287418:      	shlq	$0x5, %rdi
 528741c:      	leaq	(%r10,%rdi), %r14
 5287420:      	movq	(%r10,%rdi), %r9
 5287424:      	cmpq	%r9, %rax
 5287427:      	je	0x52874ca <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6ba>
 528742d:      	movl	$0x1, %edi
 5287432:      	xorl	%r8d, %r8d
 5287435:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 528743c:      	je	0x52875a8 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x798>
 5287442:      	xorq	$-0x2000, %r9           # imm = 0xE000
 5287449:      	orq	%r8, %r9
 528744c:      	cmoveq	%r14, %r8
 5287450:      	addl	%edi, %ecx
 5287452:      	incl	%edi
 5287454:      	andl	%edx, %ecx
 5287456:      	movq	%rcx, %r9
 5287459:      	shlq	$0x5, %r9
 528745d:      	leaq	(%r10,%r9), %r14
 5287461:      	movq	(%r10,%r9), %r9
 5287465:      	cmpq	%r9, %rax
 5287468:      	je	0x52874ca <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6ba>
 528746a:      	jmp	0x5287435 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x625>
 528746c:      	nopl	(%rax)
 5287470:      	xorl	%r14d, %r14d
 5287473:      	movl	0x18(%rsp), %eax
 5287477:      	leal	0x4(,%rax,4), %ecx
 528747e:      	leal	(%rsi,%rsi,2), %edx
 5287481:      	cmpl	%edx, %ecx
 5287483:      	jae	0x52875b4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7a4>
 5287489:      	movl	%eax, %ecx
 528748b:      	notl	%ecx
 528748d:      	addl	%esi, %ecx
 528748f:      	subl	0x1c(%rsp), %ecx
 5287493:      	movl	%esi, %edx
 5287495:      	shrl	$0x3, %edx
 5287498:      	cmpl	%edx, %ecx
 528749a:      	jbe	0x52875b6 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7a6>
 52874a0:      	incl	%eax
 52874a2:      	movl	%eax, 0x18(%rsp)
 52874a6:      	cmpq	$-0x1000, (%r14)        # imm = 0xF000
 52874ad:      	je	0x52874b3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6a3>
 52874af:      	decl	0x1c(%rsp)
 52874b3:      	movq	0x8(%rbx), %rax
 52874b7:      	movq	%rax, (%r14)
 52874ba:      	xorps	%xmm0, %xmm0
 52874bd:      	movups	%xmm0, 0x8(%r14)
 52874c2:      	movq	$0x0, 0x18(%r14)
 52874ca:      	movq	0x10(%r14), %r15
 52874ce:      	cmpq	0x18(%r14), %r15
 52874d2:      	jne	0x52873d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5c0>
 52874d8:      	movq	%rbx, 0x8(%rsp)
 52874dd:      	movq	%r13, %rbx
 52874e0:      	movq	%r10, 0x70(%rsp)
 52874e5:      	movq	0x8(%r14), %r13
 52874e9:      	subq	%r13, %r15
 52874ec:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 52874f6:      	cmpq	%rax, %r15
 52874f9:      	je	0x528819c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 52874ff:      	movq	%r15, %rax
 5287502:      	sarq	$0x4, %rax
 5287506:      	cmpq	$0x1, %rax
 528750a:      	movq	%rax, %rcx
 528750d:      	adcq	$0x0, %rcx
 5287511:      	leaq	(%rcx,%rax), %r12
 5287515:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 528751f:      	cmpq	%rdx, %r12
 5287522:      	cmovaeq	%rdx, %r12
 5287526:      	addq	%rax, %rcx
 5287529:      	cmovbq	%rdx, %r12
 528752d:      	shlq	$0x4, %r12
 5287531:      	movq	%r12, %rdi
 5287534:      	callq	0x828a620 <_Znwm@plt>
 5287539:      	movq	%rax, %rbp
 528753c:      	movq	%rbx, (%rax,%r15)
 5287540:      	movq	$0x0, 0x8(%rax,%r15)
 5287549:      	testq	%r15, %r15
 528754c:      	jle	0x528755c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x74c>
 528754e:      	movq	%rbp, %rdi
 5287551:      	movq	%r13, %rsi
 5287554:      	movq	%r15, %rdx
 5287557:      	callq	0x828ac50 <memcpy@plt>
 528755c:      	testq	%r13, %r13
 528755f:      	movq	0x8(%rsp), %rbx
 5287564:      	je	0x5287571 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x761>
 5287566:      	movq	%r13, %rdi
 5287569:      	movq	%r15, %rsi
 528756c:      	callq	0x828a660 <_ZdlPvm@plt>
 5287571:      	addq	%rbp, %r15
 5287574:      	addq	$0x10, %r15
 5287578:      	movq	%rbp, 0x8(%r14)
 528757c:      	movq	%r15, 0x10(%r14)
 5287580:      	addq	%rbp, %r12
 5287583:      	movq	%r12, 0x18(%r14)
 5287587:      	movq	0x30(%rsp), %r12
 528758c:      	movq	0x70(%rsp), %r10
 5287591:      	addq	$0x10, %rbx
 5287595:      	cmpq	%r12, %rbx
 5287598:      	movq	0x38(%rsp), %r14
 528759d:      	jne	0x52873f5 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5e5>
 52875a3:      	jmp	0x5287040 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 52875a8:      	testq	%r8, %r8
 52875ab:      	cmovneq	%r8, %r14
 52875af:      	jmp	0x5287473 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x663>
 52875b4:      	addl	%esi, %esi
 52875b6:      	leaq	0x10(%rsp), %rdi
 52875bb:      	callq	0x52a7980 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 52875c0:      	movq	0x10(%rsp), %r10
 52875c5:      	movl	0x20(%rsp), %eax
 52875c9:      	testl	%eax, %eax
 52875cb:      	je	0x528762f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x81f>
 52875cd:      	movq	0x8(%rbx), %rcx
 52875d1:      	movl	%ecx, %esi
 52875d3:      	shrl	$0x4, %esi
 52875d6:      	movl	%ecx, %edx
 52875d8:      	shrl	$0x9, %edx
 52875db:      	xorl	%esi, %edx
 52875dd:      	decl	%eax
 52875df:      	andl	%eax, %edx
 52875e1:      	movq	%rdx, %rsi
 52875e4:      	shlq	$0x5, %rsi
 52875e8:      	leaq	(%r10,%rsi), %r14
 52875ec:      	movq	(%r10,%rsi), %r8
 52875f0:      	cmpq	%r8, %rcx
 52875f3:      	je	0x5287632 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 52875f5:      	movl	$0x1, %esi
 52875fa:      	xorl	%edi, %edi
 52875fc:      	cmpq	$-0x1000, %r8           # imm = 0xF000
 5287603:      	je	0x528764e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x83e>
 5287605:      	xorq	$-0x2000, %r8           # imm = 0xE000
 528760c:      	orq	%rdi, %r8
 528760f:      	cmoveq	%r14, %rdi
 5287613:      	addl	%esi, %edx
 5287615:      	incl	%esi
 5287617:      	andl	%eax, %edx
 5287619:      	movq	%rdx, %r8
 528761c:      	shlq	$0x5, %r8
 5287620:      	leaq	(%r10,%r8), %r14
 5287624:      	movq	(%r10,%r8), %r8
 5287628:      	cmpq	%r8, %rcx
 528762b:      	je	0x5287632 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 528762d:      	jmp	0x52875fc <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7ec>
 528762f:      	xorl	%r14d, %r14d
 5287632:      	movl	0x18(%rsp), %eax
 5287636:      	incl	%eax
 5287638:      	movl	%eax, 0x18(%rsp)
 528763c:      	cmpq	$-0x1000, (%r14)        # imm = 0xF000
 5287643:      	jne	0x52874af <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x69f>
 5287649:      	jmp	0x52874b3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6a3>
 528764e:      	testq	%rdi, %rdi
 5287651:      	cmovneq	%rdi, %r14
 5287655:      	jmp	0x5287632 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 5287657:      	incq	%rdx
 528765a:      	leaq	0x18(%r15), %rsi
 528765e:      	movl	$0x10, %ecx
 5287663:      	movq	%r13, %rdi
 5287666:      	movq	%rax, %rbx
 5287669:      	callq	0x40f85b0 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 528766e:      	movq	%rbx, %rax
 5287671:      	movl	0x10(%r15), %edx
 5287675:      	jmp	0x5287090 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x280>
 528767a:      	movq	0x10(%rsp), %r12
 528767f:      	movl	0x20(%rsp), %r15d
 5287684:      	cmpl	$0x0, 0x18(%rsp)
 5287689:      	sete	%bl
 528768c:      	jmp	0x528769b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x88b>
 528768e:      	xorl	%r15d, %r15d
 5287691:      	movb	$0x1, %bl
 5287693:      	xorl	%r12d, %r12d
 5287696:      	movq	0x38(%rsp), %r14
 528769b:      	movq	0x8(%r14), %rax
 528769f:      	movq	0x38(%rax), %rdi
 52876a3:      	movq	0x50(%rax), %r14
 52876a7:      	movq	(%rdi), %rax
 52876aa:      	callq	*0x18(%rax)
 52876ad:      	movq	0xa0(%rax), %rsi
 52876b4:      	movq	(%r14), %rax
 52876b7:      	movq	%r14, %rdi
 52876ba:      	xorl	%edx, %edx
 52876bc:      	callq	*0xb0(%rax)
 52876c2:      	movl	%r15d, %eax
 52876c5:      	movq	%rax, %rcx
 52876c8:      	shlq	$0x5, %rcx
 52876cc:      	leaq	(%r12,%rcx), %r15
 52876d0:      	movq	%r15, %rbp
 52876d3:      	testb	%bl, %bl
 52876d5:      	movq	%r12, %rdi
 52876d8:      	jne	0x528770d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 52876da:      	movq	%rdi, %rbp
 52876dd:      	testq	%rax, %rax
 52876e0:      	je	0x528770d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 52876e2:      	movl	$0x1000, %edx           # imm = 0x1000
 52876e7:      	movq	%rdi, %rbp
 52876ea:      	nopw	(%rax,%rax)
 52876f0:      	movq	(%rbp), %rsi
 52876f4:      	orq	%rdx, %rsi
 52876f7:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 52876fe:      	jne	0x528770d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 5287700:      	addq	$0x20, %rbp
 5287704:      	addq	$-0x20, %rcx
 5287708:      	jne	0x52876f0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8e0>
 528770a:      	movq	%r15, %rbp
 528770d:      	shlq	$0x5, %rax
 5287711:      	addq	%rax, %rdi
 5287714:      	cmpq	%rdi, %rbp
 5287717:      	je	0x52880ac <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x129c>
 528771d:      	movq	0x38(%rsp), %r14
 5287722:      	movq	0x8(%r14), %rax
 5287726:      	movq	0x40(%rax), %rax
 528772a:      	movslq	0x8(%rax), %rax
 528772e:      	movq	%rax, 0x70(%rsp)
 5287733:      	xorl	%r12d, %r12d
 5287736:      	addq	$0x8, 0x80(%rsp)
 528773f:      	movl	$0x1000, %ebx           # imm = 0x1000
 5287744:      	xorl	%r13d, %r13d
 5287747:      	xorl	%ecx, %ecx
 5287749:      	movq	%rdi, 0x28(%rsp)
 528774e:      	jmp	0x528775d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x94d>
 5287750:      	leaq	0x8(%rdx), %r13
 5287754:      	cmpq	%rdi, %rbp
 5287757:      	je	0x5287851 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa41>
 528775d:      	movq	(%rbp), %rax
 5287761:      	cmpq	%rcx, %r13
 5287764:      	je	0x5287780 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x970>
 5287766:      	movq	%rax, (%r13)
 528776a:      	movq	%r13, %rdx
 528776d:      	jmp	0x5287830 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa20>
 5287772:      	nopw	%cs:(%rax,%rax)
 528777c:      	nopl	(%rax)
 5287780:      	movq	%rax, 0x30(%rsp)
 5287785:      	movq	%r12, 0x8(%rsp)
 528778a:      	subq	%r12, %r13
 528778d:      	cmpq	0x80(%rsp), %r13
 5287795:      	je	0x528819c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 528779b:      	movq	%r13, %rax
 528779e:      	sarq	$0x3, %rax
 52877a2:      	cmpq	$0x1, %rax
 52877a6:      	movq	%rax, %rcx
 52877a9:      	adcq	$0x0, %rcx
 52877ad:      	leaq	(%rcx,%rax), %r14
 52877b1:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 52877bb:      	cmpq	%rdx, %r14
 52877be:      	cmovaeq	%rdx, %r14
 52877c2:      	addq	%rax, %rcx
 52877c5:      	cmovbq	%rdx, %r14
 52877c9:      	leaq	(,%r14,8), %rdi
 52877d1:      	callq	0x828a620 <_Znwm@plt>
 52877d6:      	movq	%rax, %r12
 52877d9:      	movq	0x30(%rsp), %rax
 52877de:      	movq	%rax, (%r12,%r13)
 52877e2:      	testq	%r13, %r13
 52877e5:      	movq	0x8(%rsp), %rax
 52877ea:      	jle	0x5287801 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x9f1>
 52877ec:      	movq	%r12, %rdi
 52877ef:      	movq	0x8(%rsp), %rsi
 52877f4:      	movq	%r13, %rdx
 52877f7:      	callq	0x828ac50 <memcpy@plt>
 52877fc:      	movq	0x8(%rsp), %rax
 5287801:      	testq	%rax, %rax
 5287804:      	je	0x5287811 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa01>
 5287806:      	movq	%rax, %rdi
 5287809:      	movq	%r13, %rsi
 528780c:      	callq	0x828a660 <_ZdlPvm@plt>
 5287811:      	addq	%r12, %r13
 5287814:      	leaq	(%r12,%r14,8), %rcx
 5287818:      	movq	%r13, %rdx
 528781b:      	movq	0x38(%rsp), %r14
 5287820:      	movq	0x28(%rsp), %rdi
 5287825:      	nopw	%cs:(%rax,%rax)
 528782f:      	nop
 5287830:      	addq	$0x20, %rbp
 5287834:      	cmpq	%r15, %rbp
 5287837:      	je	0x5287750 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x940>
 528783d:      	movq	(%rbp), %rax
 5287841:      	orq	%rbx, %rax
 5287844:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 528784a:      	je	0x5287830 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa20>
 528784c:      	jmp	0x5287750 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x940>
 5287851:      	movq	%rcx, 0x80(%rsp)
 5287859:      	movq	%r12, 0x8(%rsp)
 528785e:      	cmpq	%r13, %r12
 5287861:      	movq	0x70(%rsp), %rbp
 5287866:      	je	0x5288092 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1282>
 528786c:      	movq	%rdx, 0x28(%rsp)
 5287871:      	movq	%r13, %rbx
 5287874:      	movq	0x8(%rsp), %r15
 5287879:      	subq	%r15, %rbx
 528787c:      	movq	%rbx, %rax
 528787f:      	sarq	$0x3, %rax
 5287883:      	bsrq	%rax, %rdx
 5287887:      	xorl	$0x3f, %edx
 528788a:      	addl	%edx, %edx
 528788c:      	xorq	$0x7e, %rdx
 5287890:      	movq	%r15, %rdi
 5287893:      	movq	%r13, %rsi
 5287896:      	callq	0x52a7bc0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPN4llvm16DwarfCompileUnitESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZNS2_10DwarfDebug16emitDebugARangesEvE3$_0EEEvT_SF_T0_T1_>
 528789b:      	leaq	0x8(%r15), %r9
 528789f:      	cmpq	$0x81, %rbx
 52878a6:      	jl	0x5287948 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb38>
 52878ac:      	leaq	0x8(%r15), %rbx
 52878b0:      	movl	$0x8, %r12d
 52878b6:      	movq	%r15, %rdi
 52878b9:      	movq	0x28(%rsp), %r8
 52878be:      	jmp	0x528790b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xafb>
 52878c0:      	cmpq	$0x9, %r12
 52878c4:      	jb	0x5287942 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb32>
 52878c6:      	movq	%rdi, 0x30(%rsp)
 52878cb:      	movq	%r9, %rdi
 52878ce:      	movq	0x8(%rsp), %rsi
 52878d3:      	movq	%r12, %rdx
 52878d6:      	movq	%r9, %r15
 52878d9:      	callq	0x828abc0 <memmove@plt>
 52878de:      	movq	0x30(%rsp), %rdi
 52878e3:      	movq	%r15, %r9
 52878e6:      	movq	0x28(%rsp), %r8
 52878eb:      	movq	0x8(%rsp), %r15
 52878f0:      	movq	%r15, %rcx
 52878f3:      	movq	%rbp, (%rcx)
 52878f6:      	addq	$0x8, %r12
 52878fa:      	addq	$0x8, %rbx
 52878fe:      	cmpq	$0x80, %r12
 5287905:      	je	0x52879f5 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbe5>
 528790b:      	movq	%rdi, %rcx
 528790e:      	leaq	(%r15,%r12), %rdi
 5287912:      	movq	(%r15,%r12), %rbp
 5287916:      	movq	(%r15), %rdx
 5287919:      	movl	0x48(%rbp), %eax
 528791c:      	cmpl	0x48(%rdx), %eax
 528791f:      	jb	0x52878c0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xab0>
 5287921:      	movq	(%rcx), %rdx
 5287924:      	movq	%rdi, %rcx
 5287927:      	cmpl	0x48(%rdx), %eax
 528792a:      	jae	0x52878f3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae3>
 528792c:      	movq	%rbx, %rcx
 528792f:      	nop
 5287930:      	movq	%rdx, (%rcx)
 5287933:      	movq	-0x10(%rcx), %rdx
 5287937:      	addq	$-0x8, %rcx
 528793b:      	cmpl	0x48(%rdx), %eax
 528793e:      	jb	0x5287930 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb20>
 5287940:      	jmp	0x52878f3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae3>
 5287942:      	movq	%rdx, 0x8(%rcx)
 5287946:      	jmp	0x52878f0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae0>
 5287948:      	movq	0x28(%rsp), %r8
 528794d:      	cmpq	%r8, %r15
 5287950:      	je	0x5287a0a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 5287956:      	movq	0x8(%rsp), %rbx
 528795b:      	jmp	0x5287998 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb88>
 528795d:      	nopl	(%rax)
 5287960:      	movq	%rbx, %rdx
 5287963:      	subq	%r12, %rdx
 5287966:      	movq	%rdx, %rax
 5287969:      	sarq	$0x3, %rax
 528796d:      	cmpq	$0x2, %rax
 5287971:      	jl	0x52879e4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbd4>
 5287973:      	shlq	$0x3, %rax
 5287977:      	subq	%rax, %rdi
 528797a:      	addq	$0x10, %rdi
 528797e:      	movq	%r12, %rsi
 5287981:      	callq	0x828abc0 <memmove@plt>
 5287986:      	movq	0x28(%rsp), %r8
 528798b:      	movq	%r15, (%r12)
 528798f:      	leaq	0x8(%rbx), %r9
 5287993:      	cmpq	%r8, %rbx
 5287996:      	je	0x5287a0a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 5287998:      	movq	%rbx, %rdi
 528799b:      	movq	%r9, %rbx
 528799e:      	movq	(%r9), %r15
 52879a1:      	movq	0x8(%rsp), %r12
 52879a6:      	movq	(%r12), %rsi
 52879aa:      	movl	0x48(%r15), %ecx
 52879ae:      	cmpl	0x48(%rsi), %ecx
 52879b1:      	jb	0x5287960 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb50>
 52879b3:      	movq	(%rdi), %rdx
 52879b6:      	movq	%rbx, %r12
 52879b9:      	cmpl	0x48(%rdx), %ecx
 52879bc:      	jae	0x528798b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 52879be:      	movq	%rbx, %r12
 52879c1:      	nopw	%cs:(%rax,%rax)
 52879cb:      	nopl	(%rax,%rax)
 52879d0:      	movq	%rdx, (%r12)
 52879d4:      	movq	-0x10(%r12), %rdx
 52879d9:      	addq	$-0x8, %r12
 52879dd:      	cmpl	0x48(%rdx), %ecx
 52879e0:      	jb	0x52879d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbc0>
 52879e2:      	jmp	0x528798b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 52879e4:      	cmpq	$0x8, %rdx
 52879e8:      	jne	0x528798b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 52879ea:      	movq	%rsi, 0x8(%rdi)
 52879ee:      	movq	0x8(%rsp), %r12
 52879f3:      	jmp	0x528798b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 52879f5:      	leaq	0x80(%r15), %rax
 52879fc:      	cmpq	%r13, %rax
 52879ff:      	movq	0x70(%rsp), %rbp
 5287a04:      	jne	0x5288060 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1250>
 5287a0a:      	leal	(%rbp,%rbp), %eax
 5287a0e:      	movl	$0x7f, %ecx
 5287a13:      	movq	%rax, 0xc0(%rsp)
 5287a1b:      	bsrq	%rax, %rcx
 5287a1f:      	xorl	$0x3f, %ecx
 5287a22:      	notb	%cl
 5287a24:      	movl	$0x1, %eax
 5287a29:      	shlq	%cl, %rax
 5287a2c:      	leaq	-0x1(%rax), %rcx
 5287a30:      	movq	%rcx, 0xb8(%rsp)
 5287a38:      	negq	%rax
 5287a3b:      	movq	%rax, 0x88(%rsp)
 5287a43:      	movq	0x8(%rsp), %r15
 5287a48:      	jmp	0x5287abd <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xcad>
 5287a4a:      	nopw	(%rax,%rax)
 5287a50:      	movq	0x8(%r14), %rax
 5287a54:      	movq	0x50(%rax), %rdi
 5287a58:      	leaq	-0x45f2c6c(%rip), %rax  # 0xc94df3 <.L.str.97>
 5287a5f:      	movq	%rax, 0x90(%rsp)
 5287a67:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287a71:      	movq	(%rdi), %rax
 5287a74:      	leaq	0x90(%rsp), %rsi
 5287a7c:      	movl	$0x1, %edx
 5287a81:      	callq	*0x78(%rax)
 5287a84:      	movq	0x8(%r14), %rax
 5287a88:      	movq	0x50(%rax), %rdi
 5287a8c:      	movq	(%rdi), %rax
 5287a8f:      	xorl	%esi, %esi
 5287a91:      	movl	%ebp, %edx
 5287a93:      	callq	*0x210(%rax)
 5287a99:      	movq	0x8(%r14), %rax
 5287a9d:      	movq	0x50(%rax), %rdi
 5287aa1:      	movq	(%rdi), %rax
 5287aa4:      	xorl	%esi, %esi
 5287aa6:      	movl	%ebp, %edx
 5287aa8:      	callq	*0x210(%rax)
 5287aae:      	cmpq	0x28(%rsp), %r15
 5287ab3:      	leaq	0x8(%r15), %r15
 5287ab7:      	je	0x5288092 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1282>
 5287abd:      	movq	%r15, 0x30(%rsp)
 5287ac2:      	movq	(%r15), %r13
 5287ac5:      	movl	0x20(%rsp), %esi
 5287ac9:      	testl	%esi, %esi
 5287acb:      	je	0x5287b40 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd30>
 5287acd:      	movq	0x10(%rsp), %rax
 5287ad2:      	movl	%r13d, %edx
 5287ad5:      	shrl	$0x4, %edx
 5287ad8:      	movl	%r13d, %ecx
 5287adb:      	shrl	$0x9, %ecx
 5287ade:      	xorl	%edx, %ecx
 5287ae0:      	leal	-0x1(%rsi), %edx
 5287ae3:      	andl	%edx, %ecx
 5287ae5:      	movq	%rcx, %rdi
 5287ae8:      	shlq	$0x5, %rdi
 5287aec:      	leaq	(%rax,%rdi), %r15
 5287af0:      	movq	(%rax,%rdi), %r9
 5287af4:      	cmpq	%r9, %r13
 5287af7:      	je	0x5287b9e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd8e>
 5287afd:      	movl	$0x1, %edi
 5287b02:      	xorl	%r8d, %r8d
 5287b05:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 5287b0c:      	je	0x5287fd0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11c0>
 5287b12:      	xorq	$-0x2000, %r9           # imm = 0xE000
 5287b19:      	orq	%r8, %r9
 5287b1c:      	cmoveq	%r15, %r8
 5287b20:      	addl	%edi, %ecx
 5287b22:      	incl	%edi
 5287b24:      	andl	%edx, %ecx
 5287b26:      	movq	%rcx, %r9
 5287b29:      	shlq	$0x5, %r9
 5287b2d:      	leaq	(%rax,%r9), %r15
 5287b31:      	movq	(%rax,%r9), %r9
 5287b35:      	cmpq	%r9, %r13
 5287b38:      	je	0x5287b9e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd8e>
 5287b3a:      	jmp	0x5287b05 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xcf5>
 5287b3c:      	nopl	(%rax)
 5287b40:      	xorl	%r15d, %r15d
 5287b43:      	movq	%r15, 0x90(%rsp)
 5287b4b:      	movl	0x18(%rsp), %eax
 5287b4f:      	leal	0x4(,%rax,4), %ecx
 5287b56:      	leal	(%rsi,%rsi,2), %edx
 5287b59:      	cmpl	%edx, %ecx
 5287b5b:      	jae	0x5288006 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11f6>
 5287b61:      	movl	%eax, %ecx
 5287b63:      	notl	%ecx
 5287b65:      	addl	%esi, %ecx
 5287b67:      	subl	0x1c(%rsp), %ecx
 5287b6b:      	movl	%esi, %edx
 5287b6d:      	shrl	$0x3, %edx
 5287b70:      	cmpl	%edx, %ecx
 5287b72:      	jbe	0x5288008 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11f8>
 5287b78:      	incl	%eax
 5287b7a:      	movl	%eax, 0x18(%rsp)
 5287b7e:      	cmpq	$-0x1000, (%r15)        # imm = 0xF000
 5287b85:      	je	0x5287b8b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd7b>
 5287b87:      	decl	0x1c(%rsp)
 5287b8b:      	movq	%r13, (%r15)
 5287b8e:      	xorps	%xmm0, %xmm0
 5287b91:      	movups	%xmm0, 0x8(%r15)
 5287b96:      	movq	$0x0, 0x18(%r15)
 5287b9e:      	movq	0x158(%r13), %r12
 5287ba5:      	testq	%r12, %r12
 5287ba8:      	cmoveq	%r13, %r12
 5287bac:      	movq	0x8(%r14), %rax
 5287bb0:      	movq	0x50(%rax), %rdi
 5287bb4:      	movq	0x8(%rdi), %rax
 5287bb8:      	xorl	%ecx, %ecx
 5287bba:      	cmpb	$0x0, 0x75a(%rax)
 5287bc1:      	setne	%cl
 5287bc4:      	movl	$0x18, %eax
 5287bc9:      	movl	$0xc, %edx
 5287bce:      	cmoveq	%rdx, %rax
 5287bd2:      	movq	0xb8(%rsp), %rdx
 5287bda:      	leaq	(%rdx,%rax), %r13
 5287bde:      	andq	0x88(%rsp), %r13
 5287be6:      	subq	%rax, %r13
 5287be9:      	movq	0x10(%r15), %rax
 5287bed:      	subq	0x8(%r15), %rax
 5287bf1:      	leal	(%r13,%rcx,4), %ecx
 5287bf6:      	shrq	$0x4, %rax
 5287bfa:      	incl	%eax
 5287bfc:      	imull	0xc0(%rsp), %eax
 5287c04:      	leal	0x8(%rax,%rcx), %esi
 5287c08:      	leaq	-0x4542c19(%rip), %rax  # 0xd44ff6 <.L.str.92>
 5287c0f:      	movq	%rax, 0x90(%rsp)
 5287c17:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287c21:      	movq	(%rdi), %rax
 5287c24:      	leaq	0x90(%rsp), %rbx
 5287c2c:      	movq	%rbx, %rdx
 5287c2f:      	callq	*0x4e8(%rax)
 5287c35:      	movq	0x8(%r14), %rax
 5287c39:      	movq	0x50(%rax), %rdi
 5287c3d:      	leaq	-0x4599e64(%rip), %rax  # 0xcedde0 <.L.str.93>
 5287c44:      	movq	%rax, 0x90(%rsp)
 5287c4c:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287c56:      	movq	(%rdi), %rax
 5287c59:      	movq	%rbx, %rsi
 5287c5c:      	movl	$0x1, %edx
 5287c61:      	callq	*0x78(%rax)
 5287c64:      	movq	0x8(%r14), %rax
 5287c68:      	movq	0x50(%rax), %rdi
 5287c6c:      	movq	(%rdi), %rax
 5287c6f:      	movl	$0x2, %esi
 5287c74:      	movl	$0x2, %edx
 5287c79:      	callq	*0x210(%rax)
 5287c7f:      	movq	0x8(%r14), %rax
 5287c83:      	movq	0x50(%rax), %rdi
 5287c87:      	leaq	-0x45c5c01(%rip), %rax  # 0xcc208d <.L.str.94>
 5287c8e:      	movq	%rax, 0x90(%rsp)
 5287c96:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287ca0:      	movq	(%rdi), %rax
 5287ca3:      	movq	%rbx, %rsi
 5287ca6:      	movl	$0x1, %edx
 5287cab:      	callq	*0x78(%rax)
 5287cae:      	movq	0x8(%r14), %rdi
 5287cb2:      	cmpb	$0x1, 0xe21(%r14)
 5287cba:      	jne	0x5287cf0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xee0>
 5287cbc:      	movq	0x38(%r12), %rax
 5287cc1:      	movq	0x40(%r12), %rdx
 5287cc6:      	movq	0x8(%rax), %rsi
 5287cca:      	movq	0x50(%rdi), %rax
 5287cce:      	movq	0x8(%rax), %rax
 5287cd2:      	xorl	%ecx, %ecx
 5287cd4:      	cmpb	$0x0, 0x75a(%rax)
 5287cdb:      	setne	%cl
 5287cde:      	leal	0x4(,%rcx,4), %ecx
 5287ce5:      	xorl	%r8d, %r8d
 5287ce8:      	callq	0x5261f40 <_ZNK4llvm10AsmPrinter19emitLabelPlusOffsetEPKNS_8MCSymbolEmjb>
 5287ced:      	jmp	0x5287cff <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xeef>
 5287cef:      	nop
 5287cf0:      	movq	0xc0(%r12), %rsi
 5287cf8:      	xorl	%edx, %edx
 5287cfa:      	callq	0x526e550 <_ZNK4llvm10AsmPrinter24emitDwarfSymbolReferenceEPKNS_8MCSymbolEb>
 5287cff:      	movq	0x8(%r14), %rax
 5287d03:      	movq	0x50(%rax), %rdi
 5287d07:      	leaq	-0x44fc8d8(%rip), %rax  # 0xd8b436 <.L.str.95>
 5287d0e:      	movq	%rax, 0x90(%rsp)
 5287d16:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287d20:      	movq	(%rdi), %rax
 5287d23:      	leaq	0x90(%rsp), %rbx
 5287d2b:      	movq	%rbx, %rsi
 5287d2e:      	movl	$0x1, %edx
 5287d33:      	callq	*0x78(%rax)
 5287d36:      	movq	0x8(%r14), %rax
 5287d3a:      	movq	0x50(%rax), %rdi
 5287d3e:      	movq	(%rdi), %rax
 5287d41:      	movq	%rbp, %rsi
 5287d44:      	movl	$0x1, %edx
 5287d49:      	callq	*0x210(%rax)
 5287d4f:      	movq	0x8(%r14), %rax
 5287d53:      	movq	0x50(%rax), %rdi
 5287d57:      	leaq	-0x456fc17(%rip), %rax  # 0xd18147 <.L.str.96>
 5287d5e:      	movq	%rax, 0x90(%rsp)
 5287d66:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287d70:      	movq	(%rdi), %rax
 5287d73:      	movq	%rbx, %rsi
 5287d76:      	movl	$0x1, %edx
 5287d7b:      	callq	*0x78(%rax)
 5287d7e:      	movq	0x8(%r14), %rax
 5287d82:      	movq	0x50(%rax), %rdi
 5287d86:      	movq	(%rdi), %rax
 5287d89:      	xorl	%esi, %esi
 5287d8b:      	movl	$0x1, %edx
 5287d90:      	callq	*0x210(%rax)
 5287d96:      	movl	$0xffffffff, %eax       # imm = 0xFFFFFFFF
 5287d9b:      	andq	%rax, %r13
 5287d9e:      	je	0x5287e10 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1000>
 5287da0:      	movq	0x8(%r14), %rax
 5287da4:      	movq	0x50(%rax), %rdi
 5287da8:      	movq	0x8(%rdi), %rcx
 5287dac:      	addq	$0x18, 0x110(%rcx)
 5287db4:      	leaq	0xc0(%rcx), %rax
 5287dbb:      	movq	0xc0(%rcx), %rsi
 5287dc2:      	testq	%rsi, %rsi
 5287dc5:      	je	0x5287fdc <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11cc>
 5287dcb:      	addq	$0x7, %rsi
 5287dcf:      	andq	$-0x8, %rsi
 5287dd3:      	leaq	0x18(%rsi), %rdx
 5287dd7:      	cmpq	0xc8(%rcx), %rdx
 5287dde:      	ja	0x5287fdc <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11cc>
 5287de4:      	movq	%rdx, (%rax)
 5287de7:      	movb	$0x1, (%rsi)
 5287dea:      	movzbl	0x4(%rsi), %eax
 5287dee:      	shll	$0x18, %eax
 5287df1:      	movl	%eax, 0x1(%rsi)
 5287df4:      	movq	$0x0, 0x8(%rsi)
 5287dfc:      	movq	%r13, 0x10(%rsi)
 5287e00:      	movq	(%rdi), %rax
 5287e03:      	movl	$0xff, %edx
 5287e08:      	xorl	%ecx, %ecx
 5287e0a:      	callq	*0x240(%rax)
 5287e10:      	movq	0x8(%r15), %r13
 5287e14:      	movq	0x10(%r15), %rbx
 5287e18:      	cmpq	%rbx, %r13
 5287e1b:      	movq	0x30(%rsp), %r15
 5287e20:      	jne	0x5287e61 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1051>
 5287e22:      	jmp	0x5287a50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5287e27:      	nopw	(%rax,%rax)
 5287e30:      	movq	0x8(%r13), %rax
 5287e34:      	testq	%rax, %rax
 5287e37:      	je	0x5287f8a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x117a>
 5287e3d:      	movq	0x8(%r14), %rcx
 5287e41:      	movq	0x50(%rcx), %rdi
 5287e45:      	movq	(%rdi), %r8
 5287e48:      	movq	%rax, %rsi
 5287e4b:      	movl	%ebp, %ecx
 5287e4d:      	callq	*0x330(%r8)
 5287e54:      	addq	$0x10, %r13
 5287e58:      	cmpq	%rbx, %r13
 5287e5b:      	je	0x5287a50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5287e61:      	movq	0x8(%r14), %r12
 5287e65:      	movq	(%r13), %rbp
 5287e69:      	movq	0x48(%r12), %rax
 5287e6e:      	addq	$0x18, 0x110(%rax)
 5287e76:      	leaq	0xc0(%rax), %rdi
 5287e7d:      	movq	0xc0(%rax), %rsi
 5287e84:      	testq	%rsi, %rsi
 5287e87:      	je	0x5287fb4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11a4>
 5287e8d:      	addq	$0x7, %rsi
 5287e91:      	andq	$-0x8, %rsi
 5287e95:      	leaq	0x18(%rsi), %rcx
 5287e99:      	cmpq	0xc8(%rax), %rcx
 5287ea0:      	ja	0x5287fb4 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11a4>
 5287ea6:      	movq	%rcx, (%rdi)
 5287ea9:      	testq	%rsi, %rsi
 5287eac:      	je	0x5287ed0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x10c0>
 5287eae:      	movb	$0x2, (%rsi)
 5287eb1:      	movzbl	0x4(%rsi), %eax
 5287eb5:      	shll	$0x18, %eax
 5287eb8:      	movl	%eax, 0x1(%rsi)
 5287ebb:      	movq	$0x0, 0x8(%rsi)
 5287ec3:      	movq	%rbp, 0x10(%rsi)
 5287ec7:      	jmp	0x5287ed2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x10c2>
 5287ec9:      	nopl	(%rax)
 5287ed0:      	xorl	%esi, %esi
 5287ed2:      	movq	0x50(%r12), %rdi
 5287ed7:      	movq	(%rdi), %rax
 5287eda:      	movq	0x70(%rsp), %rbp
 5287edf:      	movl	%ebp, %edx
 5287ee1:      	xorl	%ecx, %ecx
 5287ee3:      	callq	*0x208(%rax)
 5287ee9:      	movq	(%r13), %rdx
 5287eed:      	movq	0x2b0(%r14), %rax
 5287ef4:      	movl	0x2c0(%r14), %ecx
 5287efb:      	testq	%rcx, %rcx
 5287efe:      	je	0x5287f50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1140>
 5287f00:      	movl	%edx, %edi
 5287f02:      	shrl	$0x4, %edi
 5287f05:      	movl	%edx, %esi
 5287f07:      	shrl	$0x9, %esi
 5287f0a:      	xorl	%edi, %esi
 5287f0c:      	leal	-0x1(%rcx), %edi
 5287f0f:      	andl	%edi, %esi
 5287f11:      	movl	%esi, %r8d
 5287f14:      	shll	$0x4, %r8d
 5287f18:      	movq	(%rax,%r8), %r10
 5287f1c:      	cmpq	%r10, %rdx
 5287f1f:      	je	0x5287f57 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1147>
 5287f21:      	movl	$0x1, %r9d
 5287f27:      	cmpq	$-0x1000, %r10          # imm = 0xF000
 5287f2e:      	je	0x5287f50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1140>
 5287f30:      	addl	%r9d, %esi
 5287f33:      	incl	%r9d
 5287f36:      	andl	%edi, %esi
 5287f38:      	movq	%rsi, %r10
 5287f3b:      	shlq	$0x4, %r10
 5287f3f:      	leaq	(%rax,%r10), %r8
 5287f43:      	movq	(%rax,%r10), %r10
 5287f47:      	cmpq	%r10, %rdx
 5287f4a:      	je	0x5287f5a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x114a>
 5287f4c:      	jmp	0x5287f27 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1117>
 5287f4e:      	nop
 5287f50:      	movq	%rcx, %r8
 5287f53:      	shlq	$0x4, %r8
 5287f57:      	addq	%rax, %r8
 5287f5a:      	shlq	$0x4, %rcx
 5287f5e:      	addq	%rcx, %rax
 5287f61:      	cmpq	%rax, %r8
 5287f64:      	je	0x5287e30 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1020>
 5287f6a:      	movq	0x8(%r8), %rsi
 5287f6e:      	testq	%rsi, %rsi
 5287f71:      	je	0x5287f80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1170>
 5287f73:      	movq	0x8(%r13), %rax
 5287f77:      	testq	%rax, %rax
 5287f7a:      	jne	0x5287e3d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x102d>
 5287f80:      	cmpq	$0x1, %rsi
 5287f84:      	adcq	$0x0, %rsi
 5287f88:      	jmp	0x5287f8f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x117f>
 5287f8a:      	movl	$0x1, %esi
 5287f8f:      	movq	0x8(%r14), %rax
 5287f93:      	movq	0x50(%rax), %rdi
 5287f97:      	movq	(%rdi), %rax
 5287f9a:      	movl	%ebp, %edx
 5287f9c:      	callq	*0x210(%rax)
 5287fa2:      	addq	$0x10, %r13
 5287fa6:      	cmpq	%rbx, %r13
 5287fa9:      	jne	0x5287e61 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1051>
 5287faf:      	jmp	0x5287a50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5287fb4:      	movl	$0x18, %esi
 5287fb9:      	movl	$0x18, %edx
 5287fbe:      	movl	$0x3, %ecx
 5287fc3:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 5287fc8:      	movq	%rax, %rsi
 5287fcb:      	jmp	0x5287eae <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x109e>
 5287fd0:      	testq	%r8, %r8
 5287fd3:      	cmovneq	%r8, %r15
 5287fd7:      	jmp	0x5287b43 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd33>
 5287fdc:      	movl	$0x18, %esi
 5287fe1:      	movl	$0x18, %edx
 5287fe6:      	movq	%rdi, %r14
 5287fe9:      	movq	%rax, %rdi
 5287fec:      	movl	$0x3, %ecx
 5287ff1:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 5287ff6:      	movq	%r14, %rdi
 5287ff9:      	movq	0x38(%rsp), %r14
 5287ffe:      	movq	%rax, %rsi
 5288001:      	jmp	0x5287de7 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xfd7>
 5288006:      	addl	%esi, %esi
 5288008:      	leaq	0x10(%rsp), %rdi
 528800d:      	callq	0x52a7980 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 5288012:      	movq	0x10(%rsp), %rdi
 5288017:      	movl	0x20(%rsp), %esi
 528801b:      	movq	%r13, %rdx
 528801e:      	leaq	0x90(%rsp), %rcx
 5288026:      	callq	0x52a7900 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E15LookupBucketForIS3_EEbRKT_RPSC_>
 528802b:      	movl	0x18(%rsp), %eax
 528802f:      	movq	0x90(%rsp), %r15
 5288037:      	incl	%eax
 5288039:      	movl	%eax, 0x18(%rsp)
 528803d:      	cmpq	$-0x1000, (%r15)        # imm = 0xF000
 5288044:      	jne	0x5287b87 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd77>
 528804a:      	jmp	0x5287b8b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd7b>
 528804f:      	nop
 5288050:      	movq	%rcx, (%rdi)
 5288053:      	cmpq	%r8, %rax
 5288056:      	leaq	0x8(%rax), %rax
 528805a:      	je	0x5287a0a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 5288060:      	movq	-0x8(%rax), %rdx
 5288064:      	movq	(%rax), %rcx
 5288067:      	movl	0x48(%rcx), %esi
 528806a:      	movq	%rax, %rdi
 528806d:      	cmpl	0x48(%rdx), %esi
 5288070:      	jae	0x5288050 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1240>
 5288072:      	movq	%rax, %rdi
 5288075:      	nopw	%cs:(%rax,%rax)
 528807f:      	nop
 5288080:      	movq	%rdx, (%rdi)
 5288083:      	movq	-0x10(%rdi), %rdx
 5288087:      	addq	$-0x8, %rdi
 528808b:      	cmpl	0x48(%rdx), %esi
 528808e:      	jb	0x5288080 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1270>
 5288090:      	jmp	0x5288050 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1240>
 5288092:      	movq	0x8(%rsp), %rdi
 5288097:      	testq	%rdi, %rdi
 528809a:      	je	0x52880ac <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x129c>
 528809c:      	movq	0x80(%rsp), %rsi
 52880a4:      	subq	%rdi, %rsi
 52880a7:      	callq	0x828a660 <_ZdlPvm@plt>
 52880ac:      	movl	0x20(%rsp), %ebx
 52880b0:      	movq	0x10(%rsp), %r14
 52880b5:      	testq	%rbx, %rbx
 52880b8:      	je	0x5288101 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12f1>
 52880ba:      	shlq	$0x5, %rbx
 52880be:      	xorl	%r15d, %r15d
 52880c1:      	movl	$0x1000, %r12d          # imm = 0x1000
 52880c7:      	leaq	0x68(%rsp), %r13
 52880cc:      	jmp	0x52880d9 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c9>
 52880ce:      	nop
 52880d0:      	addq	$0x20, %r15
 52880d4:      	cmpq	%r15, %rbx
 52880d7:      	je	0x5288108 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12f8>
 52880d9:      	movq	(%r14,%r15), %rax
 52880dd:      	orq	%r12, %rax
 52880e0:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 52880e6:      	je	0x52880d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 52880e8:      	movq	0x8(%r14,%r15), %rdi
 52880ed:      	testq	%rdi, %rdi
 52880f0:      	je	0x52880d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 52880f2:      	movq	0x18(%r14,%r15), %rsi
 52880f7:      	subq	%rdi, %rsi
 52880fa:      	callq	0x828a660 <_ZdlPvm@plt>
 52880ff:      	jmp	0x52880d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 5288101:      	xorl	%ebx, %ebx
 5288103:      	leaq	0x68(%rsp), %r13
 5288108:      	movl	$0x8, %edx
 528810d:      	movq	%r14, %rdi
 5288110:      	movq	%rbx, %rsi
 5288113:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 5288118:      	movq	0x58(%rsp), %rbx
 528811d:      	movl	0x60(%rsp), %eax
 5288121:      	testq	%rax, %rax
 5288124:      	je	0x5288166 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1356>
 5288126:      	imulq	$0x98, %rax, %r14
 528812d:      	leaq	-0x80(%rbx), %r15
 5288131:      	jmp	0x5288149 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1339>
 5288133:      	nopw	%cs:(%rax,%rax)
 528813d:      	nopl	(%rax)
 5288140:      	addq	$-0x98, %r14
 5288147:      	je	0x5288161 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1351>
 5288149:      	movq	-0x90(%rbx,%r14), %rdi
 5288151:      	leaq	(%r15,%r14), %rax
 5288155:      	cmpq	%rdi, %rax
 5288158:      	je	0x5288140 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1330>
 528815a:      	callq	0x828a640 <free@plt>
 528815f:      	jmp	0x5288140 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1330>
 5288161:      	movq	0x58(%rsp), %rbx
 5288166:      	cmpq	%r13, %rbx
 5288169:      	je	0x5288173 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1363>
 528816b:      	movq	%rbx, %rdi
 528816e:      	callq	0x828a640 <free@plt>
 5288173:      	movq	0x40(%rsp), %rdi
 5288178:      	movl	0x50(%rsp), %esi
 528817c:      	shlq	$0x4, %rsi
 5288180:      	movl	$0x8, %edx
 5288185:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 528818a:      	addq	$0xc8, %rsp
 5288191:      	popq	%rbx
 5288192:      	popq	%r12
 5288194:      	popq	%r13
 5288196:      	popq	%r14
 5288198:      	popq	%r15
 528819a:      	popq	%rbp
 528819b:      	retq
 528819c:      	leaq	-0x45ed7b9(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 52881a3:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
