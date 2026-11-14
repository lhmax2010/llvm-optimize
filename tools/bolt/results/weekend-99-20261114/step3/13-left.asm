
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005286ea0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv>:
 5286ea0:      	pushq	%rbp
 5286ea1:      	pushq	%r15
 5286ea3:      	pushq	%r14
 5286ea5:      	pushq	%r13
 5286ea7:      	pushq	%r12
 5286ea9:      	pushq	%rbx
 5286eaa:      	subq	$0xc8, %rsp
 5286eb1:      	movq	0x298(%rdi), %rbx
 5286eb8:      	movq	0x2a0(%rdi), %r13
 5286ebf:      	cmpq	%r13, %rbx
 5286ec2:      	je	0x528821a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x137a>
 5286ec8:      	movq	%rdi, 0x38(%rsp)
 5286ecd:      	xorps	%xmm0, %xmm0
 5286ed0:      	movaps	%xmm0, 0x40(%rsp)
 5286ed5:      	movl	$0x0, 0x50(%rsp)
 5286edd:      	leaq	0x68(%rsp), %rax
 5286ee2:      	movq	%rax, 0x58(%rsp)
 5286ee7:      	movq	$0x0, 0x60(%rsp)
 5286ef0:      	leaq	0x32e5899(%rip), %r14   # 0x856c790 <_ZN4llvm8MCSymbol22AbsolutePseudoFragmentE>
 5286ef7:      	leaq	0x40(%rsp), %r15
 5286efc:      	leaq	0x90(%rsp), %r12
 5286f04:      	nopw	%cs:(%rax,%rax)
 5286f0e:      	nop
 5286f10:      	movq	(%rbx), %rbp
 5286f13:      	movq	(%rbp), %rax
 5286f17:      	testq	%rax, %rax
 5286f1a:      	je	0x5286f50 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb0>
 5286f1c:      	testq	%rax, %rax
 5286f1f:      	je	0x5286f80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286f21:      	cmpq	(%r14), %rax
 5286f24:      	je	0x5286f80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286f26:      	movq	(%rbx), %rbp
 5286f29:      	movq	(%rbp), %rax
 5286f2d:      	testq	%rax, %rax
 5286f30:      	jne	0x5286f3f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x9f>
 5286f32:      	movq	0x10(%rbp), %rdi
 5286f36:      	callq	0x3e5bd00 <_ZNK4llvm6MCExpr22findAssociatedFragmentEv>
 5286f3b:      	movq	%rax, (%rbp)
 5286f3f:      	movq	0x8(%rax), %rax
 5286f43:      	movq	%rax, 0x90(%rsp)
 5286f4b:      	jmp	0x5286f8c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xec>
 5286f4d:      	nopl	(%rax)
 5286f50:      	movl	0x8(%rbp), %eax
 5286f53:      	movl	$0x103, %ecx            # imm = 0x103
 5286f58:      	andl	%ecx, %eax
 5286f5a:      	cmpl	$0x1, %eax
 5286f5d:      	jne	0x5286f80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xe0>
 5286f5f:      	movq	0x10(%rbp), %rdi
 5286f63:      	callq	0x3e5bd00 <_ZNK4llvm6MCExpr22findAssociatedFragmentEv>
 5286f68:      	movq	%rax, (%rbp)
 5286f6c:      	testq	%rax, %rax
 5286f6f:      	jne	0x5286f21 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x81>
 5286f71:      	nopw	%cs:(%rax,%rax)
 5286f7b:      	nopl	(%rax,%rax)
 5286f80:      	movq	$0x0, 0x90(%rsp)
 5286f8c:      	movq	%r15, %rdi
 5286f8f:      	movq	%r12, %rsi
 5286f92:      	callq	0x3e1e320 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_9MCSectionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E24lookupOrInsertIntoBucketIRKS3_JEEESt4pairIPS8_bEOT_DpOT0_>
 5286f97:      	cmpb	$0x1, %dl
 5286f9a:      	jne	0x5287000 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x160>
 5286f9c:      	movl	0x60(%rsp), %ecx
 5286fa0:      	movl	%ecx, 0x8(%rax)
 5286fa3:      	cmpl	0x64(%rsp), %ecx
 5286fa7:      	jae	0x528705e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1be>
 5286fad:      	movq	0x58(%rsp), %rax
 5286fb2:      	imulq	$0x98, %rcx, %rcx
 5286fb9:      	movq	0x90(%rsp), %rdx
 5286fc1:      	movq	%rdx, (%rax,%rcx)
 5286fc5:      	leaq	0x18(%rax,%rcx), %rdx
 5286fca:      	movq	%rdx, 0x8(%rax,%rcx)
 5286fcf:      	movabsq	$0x800000000, %rdx      # imm = 0x800000000
 5286fd9:      	movq	%rdx, 0x10(%rax,%rcx)
 5286fde:      	movl	0x60(%rsp), %eax
 5286fe2:      	incl	%eax
 5286fe4:      	movl	%eax, 0x60(%rsp)
 5286fe8:      	movq	0x58(%rsp), %rcx
 5286fed:      	movl	%eax, %eax
 5286fef:      	imulq	$0x98, %rax, %rax
 5286ff6:      	leaq	-0x98(%rcx,%rax), %rbp
 5286ffe:      	jmp	0x528700f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x16f>
 5287000:      	movl	0x8(%rax), %eax
 5287003:      	imulq	$0x98, %rax, %rbp
 528700a:      	addq	0x58(%rsp), %rbp
 528700f:      	movups	(%rbx), %xmm0
 5287012:      	movl	0x10(%rbp), %edx
 5287015:      	cmpl	0x14(%rbp), %edx
 5287018:      	jae	0x528703a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x19a>
 528701a:      	movq	0x8(%rbp), %rax
 528701e:      	movl	%edx, %ecx
 5287020:      	shlq	$0x4, %rcx
 5287024:      	movups	%xmm0, (%rax,%rcx)
 5287028:      	incl	0x10(%rbp)
 528702b:      	addq	$0x10, %rbx
 528702f:      	cmpq	%r13, %rbx
 5287032:      	jne	0x5286f10 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x70>
 5287038:      	jmp	0x5287074 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1d4>
 528703a:      	leaq	0x8(%rbp), %rdi
 528703e:      	incq	%rdx
 5287041:      	leaq	0x18(%rbp), %rsi
 5287045:      	movl	$0x10, %ecx
 528704a:      	movaps	%xmm0, 0x70(%rsp)
 528704f:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 5287054:      	movaps	0x70(%rsp), %xmm0
 5287059:      	movl	0x10(%rbp), %edx
 528705c:      	jmp	0x528701a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x17a>
 528705e:      	leaq	0x58(%rsp), %rdi
 5287063:      	movq	%r12, %rsi
 5287066:      	callq	0x52a77b0 <_ZN4llvm23SmallVectorTemplateBaseISt4pairIPNS_9MCSectionENS_11SmallVectorINS_8SymbolCUELj8EEEELb0EE18growAndEmplaceBackIJRKSt21piecewise_construct_tSt5tupleIJRKS3_EESD_IJEEEEERS7_DpOT_>
 528706b:      	movl	0x60(%rsp), %eax
 528706f:      	jmp	0x5286fe8 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x148>
 5287074:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 528707e:      	movq	%rax, 0x80(%rsp)
 5287086:      	xorps	%xmm0, %xmm0
 5287089:      	movaps	%xmm0, 0x10(%rsp)
 528708e:      	movl	$0x0, 0x20(%rsp)
 5287096:      	movl	0x60(%rsp), %eax
 528709a:      	testq	%rax, %rax
 528709d:      	je	0x528771e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x87e>
 52870a3:      	movq	0x58(%rsp), %r15
 52870a8:      	imulq	$0x98, %rax, %rax
 52870af:      	addq	%r15, %rax
 52870b2:      	movq	%rax, 0xb8(%rsp)
 52870ba:      	movq	0x38(%rsp), %r14
 52870bf:      	jmp	0x52870ed <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x24d>
 52870c1:      	nopw	%cs:(%rax,%rax)
 52870cb:      	nopl	(%rax,%rax)
 52870d0:      	movq	0x88(%rsp), %r15
 52870d8:      	addq	$0x98, %r15
 52870df:      	cmpq	0xb8(%rsp), %r15
 52870e7:      	je	0x528770a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x86a>
 52870ed:      	movq	(%r15), %rsi
 52870f0:      	testq	%rsi, %rsi
 52870f3:      	movq	%r15, 0x88(%rsp)
 52870fb:      	je	0x5287430 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x590>
 5287101:      	leaq	0x8(%r15), %r13
 5287105:      	movq	0x8(%r14), %rax
 5287109:      	movq	0x50(%rax), %rdi
 528710d:      	callq	0x3e7cb30 <_ZN4llvm10MCStreamer10endSectionEPNS_9MCSectionE>
 5287112:      	movl	0x10(%r15), %edx
 5287116:      	cmpl	0x14(%r15), %edx
 528711a:      	jae	0x52876e7 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x847>
 5287120:      	movq	0x8(%r15), %rcx
 5287124:      	movl	%edx, %edx
 5287126:      	shlq	$0x4, %rdx
 528712a:      	movq	%rax, (%rcx,%rdx)
 528712e:      	movq	$0x0, 0x8(%rcx,%rdx)
 5287137:      	movl	0x10(%r15), %ebp
 528713b:      	incl	%ebp
 528713d:      	movl	%ebp, 0x10(%r15)
 5287141:      	cmpl	$0x2, %ebp
 5287144:      	jb	0x52870d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 5287146:      	movq	(%r13), %rax
 528714a:      	movq	(%rax), %r11
 528714d:      	movl	$0x1, %ebx
 5287152:      	movq	%r13, 0x28(%rsp)
 5287157:      	movq	%rbp, 0xc0(%rsp)
 528715f:      	jmp	0x5287195 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2f5>
 5287161:      	nopw	%cs:(%rax,%rax)
 528716b:      	nopl	(%rax,%rax)
 5287170:      	movq	%r11, (%r12)
 5287174:      	movq	0x70(%rsp), %rax
 5287179:      	movq	%rax, 0x8(%r12)
 528717e:      	addq	$0x10, %r12
 5287182:      	movq	%r12, 0x10(%r10)
 5287186:      	movq	(%r15), %r11
 5287189:      	incq	%rbx
 528718c:      	cmpq	%rbp, %rbx
 528718f:      	je	0x52870d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 5287195:      	movq	(%r13), %r15
 5287199:      	movq	%rbx, %rcx
 528719c:      	shlq	$0x4, %rcx
 52871a0:      	movq	-0x8(%r15,%rcx), %rax
 52871a5:      	cmpq	%rax, 0x8(%r15,%rcx)
 52871aa:      	je	0x5287189 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2e9>
 52871ac:      	addq	%rcx, %r15
 52871af:      	movq	(%r15), %rcx
 52871b2:      	movq	%rcx, 0x70(%rsp)
 52871b7:      	movl	0x20(%rsp), %esi
 52871bb:      	testl	%esi, %esi
 52871bd:      	je	0x5287230 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x390>
 52871bf:      	movq	0x10(%rsp), %rcx
 52871c4:      	movl	%eax, %edi
 52871c6:      	shrl	$0x4, %edi
 52871c9:      	movl	%eax, %edx
 52871cb:      	shrl	$0x9, %edx
 52871ce:      	xorl	%edi, %edx
 52871d0:      	leal	-0x1(%rsi), %edi
 52871d3:      	andl	%edi, %edx
 52871d5:      	movq	%rdx, %r8
 52871d8:      	shlq	$0x5, %r8
 52871dc:      	leaq	(%rcx,%r8), %r10
 52871e0:      	movq	(%rcx,%r8), %r12
 52871e4:      	cmpq	%r12, %rax
 52871e7:      	je	0x528728a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3ea>
 52871ed:      	movl	$0x1, %r8d
 52871f3:      	xorl	%r9d, %r9d
 52871f6:      	cmpq	$-0x1000, %r12          # imm = 0xF000
 52871fd:      	je	0x5287364 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4c4>
 5287203:      	xorq	$-0x2000, %r12          # imm = 0xE000
 528720a:      	orq	%r9, %r12
 528720d:      	cmoveq	%r10, %r9
 5287211:      	addl	%r8d, %edx
 5287214:      	incl	%r8d
 5287217:      	andl	%edi, %edx
 5287219:      	movq	%rdx, %r12
 528721c:      	shlq	$0x5, %r12
 5287220:      	leaq	(%rcx,%r12), %r10
 5287224:      	movq	(%rcx,%r12), %r12
 5287228:      	cmpq	%r12, %rax
 528722b:      	je	0x528728a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3ea>
 528722d:      	jmp	0x52871f6 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x356>
 528722f:      	nop
 5287230:      	xorl	%r10d, %r10d
 5287233:      	movl	0x18(%rsp), %eax
 5287237:      	leal	0x4(,%rax,4), %ecx
 528723e:      	leal	(%rsi,%rsi,2), %edx
 5287241:      	cmpl	%edx, %ecx
 5287243:      	jae	0x5287370 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4d0>
 5287249:      	movl	%eax, %ecx
 528724b:      	notl	%ecx
 528724d:      	addl	%esi, %ecx
 528724f:      	subl	0x1c(%rsp), %ecx
 5287253:      	movl	%esi, %edx
 5287255:      	shrl	$0x3, %edx
 5287258:      	cmpl	%edx, %ecx
 528725a:      	jbe	0x5287372 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x4d2>
 5287260:      	incl	%eax
 5287262:      	movl	%eax, 0x18(%rsp)
 5287266:      	cmpq	$-0x1000, (%r10)        # imm = 0xF000
 528726d:      	je	0x5287273 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3d3>
 528726f:      	decl	0x1c(%rsp)
 5287273:      	movq	-0x8(%r15), %rax
 5287277:      	movq	%rax, (%r10)
 528727a:      	xorps	%xmm0, %xmm0
 528727d:      	movups	%xmm0, 0x8(%r10)
 5287282:      	movq	$0x0, 0x18(%r10)
 528728a:      	movq	0x10(%r10), %r12
 528728e:      	cmpq	0x18(%r10), %r12
 5287292:      	jne	0x5287170 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2d0>
 5287298:      	movq	%r15, 0x8(%rsp)
 528729d:      	movq	%r10, 0x30(%rsp)
 52872a2:      	movq	0x8(%r10), %rbp
 52872a6:      	subq	%rbp, %r12
 52872a9:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 52872b3:      	cmpq	%rax, %r12
 52872b6:      	je	0x528822c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 52872bc:      	movq	%r11, %r15
 52872bf:      	movq	%r12, %rax
 52872c2:      	sarq	$0x4, %rax
 52872c6:      	cmpq	$0x1, %rax
 52872ca:      	movq	%rax, %rcx
 52872cd:      	adcq	$0x0, %rcx
 52872d1:      	leaq	(%rcx,%rax), %r13
 52872d5:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 52872df:      	cmpq	%rdx, %r13
 52872e2:      	cmovaeq	%rdx, %r13
 52872e6:      	addq	%rax, %rcx
 52872e9:      	cmovbq	%rdx, %r13
 52872ed:      	shlq	$0x4, %r13
 52872f1:      	movq	%r13, %rdi
 52872f4:      	callq	0x828a6b0 <_Znwm@plt>
 52872f9:      	movq	%rax, %r14
 52872fc:      	movq	%r15, (%rax,%r12)
 5287300:      	movq	0x70(%rsp), %rax
 5287305:      	movq	%rax, 0x8(%r14,%r12)
 528730a:      	testq	%r12, %r12
 528730d:      	jle	0x528731d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x47d>
 528730f:      	movq	%r14, %rdi
 5287312:      	movq	%rbp, %rsi
 5287315:      	movq	%r12, %rdx
 5287318:      	callq	0x828ace0 <memcpy@plt>
 528731d:      	testq	%rbp, %rbp
 5287320:      	movq	0x8(%rsp), %r15
 5287325:      	je	0x5287332 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x492>
 5287327:      	movq	%rbp, %rdi
 528732a:      	movq	%r12, %rsi
 528732d:      	callq	0x828a6f0 <_ZdlPvm@plt>
 5287332:      	addq	%r14, %r12
 5287335:      	addq	$0x10, %r12
 5287339:      	movq	0x30(%rsp), %rax
 528733e:      	movq	%r14, 0x8(%rax)
 5287342:      	movq	%r12, 0x10(%rax)
 5287346:      	addq	%r14, %r13
 5287349:      	movq	%r13, 0x18(%rax)
 528734d:      	movq	0x38(%rsp), %r14
 5287352:      	movq	0x28(%rsp), %r13
 5287357:      	movq	0xc0(%rsp), %rbp
 528735f:      	jmp	0x5287186 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x2e6>
 5287364:      	testq	%r9, %r9
 5287367:      	cmovneq	%r9, %r10
 528736b:      	jmp	0x5287233 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x393>
 5287370:      	addl	%esi, %esi
 5287372:      	movq	%r11, %r12
 5287375:      	leaq	0x10(%rsp), %rdi
 528737a:      	callq	0x52a7a10 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 528737f:      	movl	0x20(%rsp), %eax
 5287383:      	testl	%eax, %eax
 5287385:      	je	0x52873f7 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x557>
 5287387:      	movq	0x10(%rsp), %rcx
 528738c:      	movq	-0x8(%r15), %rdx
 5287390:      	movl	%edx, %edi
 5287392:      	shrl	$0x4, %edi
 5287395:      	movl	%edx, %esi
 5287397:      	shrl	$0x9, %esi
 528739a:      	xorl	%edi, %esi
 528739c:      	decl	%eax
 528739e:      	andl	%eax, %esi
 52873a0:      	movq	%rsi, %rdi
 52873a3:      	shlq	$0x5, %rdi
 52873a7:      	leaq	(%rcx,%rdi), %r10
 52873ab:      	movq	(%rcx,%rdi), %r9
 52873af:      	cmpq	%r9, %rdx
 52873b2:      	je	0x52873fa <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55a>
 52873b4:      	movl	$0x1, %edi
 52873b9:      	xorl	%r8d, %r8d
 52873bc:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 52873c3:      	je	0x5287419 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x579>
 52873c5:      	xorq	$-0x2000, %r9           # imm = 0xE000
 52873cc:      	orq	%r8, %r9
 52873cf:      	cmoveq	%r10, %r8
 52873d3:      	addl	%edi, %esi
 52873d5:      	incl	%edi
 52873d7:      	andl	%eax, %esi
 52873d9:      	movq	%rsi, %r9
 52873dc:      	shlq	$0x5, %r9
 52873e0:      	leaq	(%rcx,%r9), %r10
 52873e4:      	movq	(%rcx,%r9), %r9
 52873e8:      	cmpq	%r9, %rdx
 52873eb:      	movq	0x38(%rsp), %r14
 52873f0:      	movq	%r12, %r11
 52873f3:      	je	0x52873fd <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55d>
 52873f5:      	jmp	0x52873bc <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x51c>
 52873f7:      	xorl	%r10d, %r10d
 52873fa:      	movq	%r12, %r11
 52873fd:      	movl	0x18(%rsp), %eax
 5287401:      	incl	%eax
 5287403:      	movl	%eax, 0x18(%rsp)
 5287407:      	cmpq	$-0x1000, (%r10)        # imm = 0xF000
 528740e:      	jne	0x528726f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3cf>
 5287414:      	jmp	0x5287273 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x3d3>
 5287419:      	testq	%r8, %r8
 528741c:      	cmovneq	%r8, %r10
 5287420:      	movq	0x38(%rsp), %r14
 5287425:      	jmp	0x52873fa <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x55a>
 5287427:      	nopw	(%rax,%rax)
 5287430:      	movl	0x10(%r15), %r12d
 5287434:      	testq	%r12, %r12
 5287437:      	je	0x52870d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 528743d:      	movq	0x88(%rsp), %rax
 5287445:      	movq	0x8(%rax), %rbx
 5287449:      	shlq	$0x4, %r12
 528744d:      	addq	%rbx, %r12
 5287450:      	movq	0x10(%rsp), %r10
 5287455:      	movq	%r12, 0x30(%rsp)
 528745a:      	jmp	0x5287485 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5e5>
 528745c:      	nopl	(%rax)
 5287460:      	movq	%r13, (%r15)
 5287463:      	movq	$0x0, 0x8(%r15)
 528746b:      	addq	$0x10, %r15
 528746f:      	movq	%r15, 0x10(%r14)
 5287473:      	addq	$0x10, %rbx
 5287477:      	cmpq	%r12, %rbx
 528747a:      	movq	0x38(%rsp), %r14
 528747f:      	je	0x52870d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 5287485:      	movq	(%rbx), %r13
 5287488:      	movl	0x20(%rsp), %esi
 528748c:      	testl	%esi, %esi
 528748e:      	je	0x5287500 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x660>
 5287490:      	movq	0x8(%rbx), %rax
 5287494:      	movl	%eax, %edx
 5287496:      	shrl	$0x4, %edx
 5287499:      	movl	%eax, %ecx
 528749b:      	shrl	$0x9, %ecx
 528749e:      	xorl	%edx, %ecx
 52874a0:      	leal	-0x1(%rsi), %edx
 52874a3:      	andl	%edx, %ecx
 52874a5:      	movq	%rcx, %rdi
 52874a8:      	shlq	$0x5, %rdi
 52874ac:      	leaq	(%r10,%rdi), %r14
 52874b0:      	movq	(%r10,%rdi), %r9
 52874b4:      	cmpq	%r9, %rax
 52874b7:      	je	0x528755a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6ba>
 52874bd:      	movl	$0x1, %edi
 52874c2:      	xorl	%r8d, %r8d
 52874c5:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 52874cc:      	je	0x5287638 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x798>
 52874d2:      	xorq	$-0x2000, %r9           # imm = 0xE000
 52874d9:      	orq	%r8, %r9
 52874dc:      	cmoveq	%r14, %r8
 52874e0:      	addl	%edi, %ecx
 52874e2:      	incl	%edi
 52874e4:      	andl	%edx, %ecx
 52874e6:      	movq	%rcx, %r9
 52874e9:      	shlq	$0x5, %r9
 52874ed:      	leaq	(%r10,%r9), %r14
 52874f1:      	movq	(%r10,%r9), %r9
 52874f5:      	cmpq	%r9, %rax
 52874f8:      	je	0x528755a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6ba>
 52874fa:      	jmp	0x52874c5 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x625>
 52874fc:      	nopl	(%rax)
 5287500:      	xorl	%r14d, %r14d
 5287503:      	movl	0x18(%rsp), %eax
 5287507:      	leal	0x4(,%rax,4), %ecx
 528750e:      	leal	(%rsi,%rsi,2), %edx
 5287511:      	cmpl	%edx, %ecx
 5287513:      	jae	0x5287644 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7a4>
 5287519:      	movl	%eax, %ecx
 528751b:      	notl	%ecx
 528751d:      	addl	%esi, %ecx
 528751f:      	subl	0x1c(%rsp), %ecx
 5287523:      	movl	%esi, %edx
 5287525:      	shrl	$0x3, %edx
 5287528:      	cmpl	%edx, %ecx
 528752a:      	jbe	0x5287646 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7a6>
 5287530:      	incl	%eax
 5287532:      	movl	%eax, 0x18(%rsp)
 5287536:      	cmpq	$-0x1000, (%r14)        # imm = 0xF000
 528753d:      	je	0x5287543 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6a3>
 528753f:      	decl	0x1c(%rsp)
 5287543:      	movq	0x8(%rbx), %rax
 5287547:      	movq	%rax, (%r14)
 528754a:      	xorps	%xmm0, %xmm0
 528754d:      	movups	%xmm0, 0x8(%r14)
 5287552:      	movq	$0x0, 0x18(%r14)
 528755a:      	movq	0x10(%r14), %r15
 528755e:      	cmpq	0x18(%r14), %r15
 5287562:      	jne	0x5287460 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5c0>
 5287568:      	movq	%rbx, 0x8(%rsp)
 528756d:      	movq	%r13, %rbx
 5287570:      	movq	%r10, 0x70(%rsp)
 5287575:      	movq	0x8(%r14), %r13
 5287579:      	subq	%r13, %r15
 528757c:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 5287586:      	cmpq	%rax, %r15
 5287589:      	je	0x528822c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 528758f:      	movq	%r15, %rax
 5287592:      	sarq	$0x4, %rax
 5287596:      	cmpq	$0x1, %rax
 528759a:      	movq	%rax, %rcx
 528759d:      	adcq	$0x0, %rcx
 52875a1:      	leaq	(%rcx,%rax), %r12
 52875a5:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 52875af:      	cmpq	%rdx, %r12
 52875b2:      	cmovaeq	%rdx, %r12
 52875b6:      	addq	%rax, %rcx
 52875b9:      	cmovbq	%rdx, %r12
 52875bd:      	shlq	$0x4, %r12
 52875c1:      	movq	%r12, %rdi
 52875c4:      	callq	0x828a6b0 <_Znwm@plt>
 52875c9:      	movq	%rax, %rbp
 52875cc:      	movq	%rbx, (%rax,%r15)
 52875d0:      	movq	$0x0, 0x8(%rax,%r15)
 52875d9:      	testq	%r15, %r15
 52875dc:      	jle	0x52875ec <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x74c>
 52875de:      	movq	%rbp, %rdi
 52875e1:      	movq	%r13, %rsi
 52875e4:      	movq	%r15, %rdx
 52875e7:      	callq	0x828ace0 <memcpy@plt>
 52875ec:      	testq	%r13, %r13
 52875ef:      	movq	0x8(%rsp), %rbx
 52875f4:      	je	0x5287601 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x761>
 52875f6:      	movq	%r13, %rdi
 52875f9:      	movq	%r15, %rsi
 52875fc:      	callq	0x828a6f0 <_ZdlPvm@plt>
 5287601:      	addq	%rbp, %r15
 5287604:      	addq	$0x10, %r15
 5287608:      	movq	%rbp, 0x8(%r14)
 528760c:      	movq	%r15, 0x10(%r14)
 5287610:      	addq	%rbp, %r12
 5287613:      	movq	%r12, 0x18(%r14)
 5287617:      	movq	0x30(%rsp), %r12
 528761c:      	movq	0x70(%rsp), %r10
 5287621:      	addq	$0x10, %rbx
 5287625:      	cmpq	%r12, %rbx
 5287628:      	movq	0x38(%rsp), %r14
 528762d:      	jne	0x5287485 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x5e5>
 5287633:      	jmp	0x52870d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x230>
 5287638:      	testq	%r8, %r8
 528763b:      	cmovneq	%r8, %r14
 528763f:      	jmp	0x5287503 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x663>
 5287644:      	addl	%esi, %esi
 5287646:      	leaq	0x10(%rsp), %rdi
 528764b:      	callq	0x52a7a10 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 5287650:      	movq	0x10(%rsp), %r10
 5287655:      	movl	0x20(%rsp), %eax
 5287659:      	testl	%eax, %eax
 528765b:      	je	0x52876bf <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x81f>
 528765d:      	movq	0x8(%rbx), %rcx
 5287661:      	movl	%ecx, %esi
 5287663:      	shrl	$0x4, %esi
 5287666:      	movl	%ecx, %edx
 5287668:      	shrl	$0x9, %edx
 528766b:      	xorl	%esi, %edx
 528766d:      	decl	%eax
 528766f:      	andl	%eax, %edx
 5287671:      	movq	%rdx, %rsi
 5287674:      	shlq	$0x5, %rsi
 5287678:      	leaq	(%r10,%rsi), %r14
 528767c:      	movq	(%r10,%rsi), %r8
 5287680:      	cmpq	%r8, %rcx
 5287683:      	je	0x52876c2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 5287685:      	movl	$0x1, %esi
 528768a:      	xorl	%edi, %edi
 528768c:      	cmpq	$-0x1000, %r8           # imm = 0xF000
 5287693:      	je	0x52876de <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x83e>
 5287695:      	xorq	$-0x2000, %r8           # imm = 0xE000
 528769c:      	orq	%rdi, %r8
 528769f:      	cmoveq	%r14, %rdi
 52876a3:      	addl	%esi, %edx
 52876a5:      	incl	%esi
 52876a7:      	andl	%eax, %edx
 52876a9:      	movq	%rdx, %r8
 52876ac:      	shlq	$0x5, %r8
 52876b0:      	leaq	(%r10,%r8), %r14
 52876b4:      	movq	(%r10,%r8), %r8
 52876b8:      	cmpq	%r8, %rcx
 52876bb:      	je	0x52876c2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 52876bd:      	jmp	0x528768c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x7ec>
 52876bf:      	xorl	%r14d, %r14d
 52876c2:      	movl	0x18(%rsp), %eax
 52876c6:      	incl	%eax
 52876c8:      	movl	%eax, 0x18(%rsp)
 52876cc:      	cmpq	$-0x1000, (%r14)        # imm = 0xF000
 52876d3:      	jne	0x528753f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x69f>
 52876d9:      	jmp	0x5287543 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x6a3>
 52876de:      	testq	%rdi, %rdi
 52876e1:      	cmovneq	%rdi, %r14
 52876e5:      	jmp	0x52876c2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x822>
 52876e7:      	incq	%rdx
 52876ea:      	leaq	0x18(%r15), %rsi
 52876ee:      	movl	$0x10, %ecx
 52876f3:      	movq	%r13, %rdi
 52876f6:      	movq	%rax, %rbx
 52876f9:      	callq	0x40f8640 <_ZN4llvm15SmallVectorBaseIjE8grow_podEPvmm>
 52876fe:      	movq	%rbx, %rax
 5287701:      	movl	0x10(%r15), %edx
 5287705:      	jmp	0x5287120 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x280>
 528770a:      	movq	0x10(%rsp), %r12
 528770f:      	movl	0x20(%rsp), %r15d
 5287714:      	cmpl	$0x0, 0x18(%rsp)
 5287719:      	sete	%bl
 528771c:      	jmp	0x528772b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x88b>
 528771e:      	xorl	%r15d, %r15d
 5287721:      	movb	$0x1, %bl
 5287723:      	xorl	%r12d, %r12d
 5287726:      	movq	0x38(%rsp), %r14
 528772b:      	movq	0x8(%r14), %rax
 528772f:      	movq	0x38(%rax), %rdi
 5287733:      	movq	0x50(%rax), %r14
 5287737:      	movq	(%rdi), %rax
 528773a:      	callq	*0x18(%rax)
 528773d:      	movq	0xa0(%rax), %rsi
 5287744:      	movq	(%r14), %rax
 5287747:      	movq	%r14, %rdi
 528774a:      	xorl	%edx, %edx
 528774c:      	callq	*0xb0(%rax)
 5287752:      	movl	%r15d, %eax
 5287755:      	movq	%rax, %rcx
 5287758:      	shlq	$0x5, %rcx
 528775c:      	leaq	(%r12,%rcx), %r15
 5287760:      	movq	%r15, %rbp
 5287763:      	testb	%bl, %bl
 5287765:      	movq	%r12, %rdi
 5287768:      	jne	0x528779d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 528776a:      	movq	%rdi, %rbp
 528776d:      	testq	%rax, %rax
 5287770:      	je	0x528779d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 5287772:      	movl	$0x1000, %edx           # imm = 0x1000
 5287777:      	movq	%rdi, %rbp
 528777a:      	nopw	(%rax,%rax)
 5287780:      	movq	(%rbp), %rsi
 5287784:      	orq	%rdx, %rsi
 5287787:      	cmpq	$-0x1000, %rsi          # imm = 0xF000
 528778e:      	jne	0x528779d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8fd>
 5287790:      	addq	$0x20, %rbp
 5287794:      	addq	$-0x20, %rcx
 5287798:      	jne	0x5287780 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x8e0>
 528779a:      	movq	%r15, %rbp
 528779d:      	shlq	$0x5, %rax
 52877a1:      	addq	%rax, %rdi
 52877a4:      	cmpq	%rdi, %rbp
 52877a7:      	je	0x528813c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x129c>
 52877ad:      	movq	0x38(%rsp), %r14
 52877b2:      	movq	0x8(%r14), %rax
 52877b6:      	movq	0x40(%rax), %rax
 52877ba:      	movslq	0x8(%rax), %rax
 52877be:      	movq	%rax, 0x70(%rsp)
 52877c3:      	xorl	%r12d, %r12d
 52877c6:      	addq	$0x8, 0x80(%rsp)
 52877cf:      	movl	$0x1000, %ebx           # imm = 0x1000
 52877d4:      	xorl	%r13d, %r13d
 52877d7:      	xorl	%ecx, %ecx
 52877d9:      	movq	%rdi, 0x28(%rsp)
 52877de:      	jmp	0x52877ed <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x94d>
 52877e0:      	leaq	0x8(%rdx), %r13
 52877e4:      	cmpq	%rdi, %rbp
 52877e7:      	je	0x52878e1 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa41>
 52877ed:      	movq	(%rbp), %rax
 52877f1:      	cmpq	%rcx, %r13
 52877f4:      	je	0x5287810 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x970>
 52877f6:      	movq	%rax, (%r13)
 52877fa:      	movq	%r13, %rdx
 52877fd:      	jmp	0x52878c0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa20>
 5287802:      	nopw	%cs:(%rax,%rax)
 528780c:      	nopl	(%rax)
 5287810:      	movq	%rax, 0x30(%rsp)
 5287815:      	movq	%r12, 0x8(%rsp)
 528781a:      	subq	%r12, %r13
 528781d:      	cmpq	0x80(%rsp), %r13
 5287825:      	je	0x528822c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x138c>
 528782b:      	movq	%r13, %rax
 528782e:      	sarq	$0x3, %rax
 5287832:      	cmpq	$0x1, %rax
 5287836:      	movq	%rax, %rcx
 5287839:      	adcq	$0x0, %rcx
 528783d:      	leaq	(%rcx,%rax), %r14
 5287841:      	movabsq	$0xfffffffffffffff, %rdx # imm = 0xFFFFFFFFFFFFFFF
 528784b:      	cmpq	%rdx, %r14
 528784e:      	cmovaeq	%rdx, %r14
 5287852:      	addq	%rax, %rcx
 5287855:      	cmovbq	%rdx, %r14
 5287859:      	leaq	(,%r14,8), %rdi
 5287861:      	callq	0x828a6b0 <_Znwm@plt>
 5287866:      	movq	%rax, %r12
 5287869:      	movq	0x30(%rsp), %rax
 528786e:      	movq	%rax, (%r12,%r13)
 5287872:      	testq	%r13, %r13
 5287875:      	movq	0x8(%rsp), %rax
 528787a:      	jle	0x5287891 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x9f1>
 528787c:      	movq	%r12, %rdi
 528787f:      	movq	0x8(%rsp), %rsi
 5287884:      	movq	%r13, %rdx
 5287887:      	callq	0x828ace0 <memcpy@plt>
 528788c:      	movq	0x8(%rsp), %rax
 5287891:      	testq	%rax, %rax
 5287894:      	je	0x52878a1 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa01>
 5287896:      	movq	%rax, %rdi
 5287899:      	movq	%r13, %rsi
 528789c:      	callq	0x828a6f0 <_ZdlPvm@plt>
 52878a1:      	addq	%r12, %r13
 52878a4:      	leaq	(%r12,%r14,8), %rcx
 52878a8:      	movq	%r13, %rdx
 52878ab:      	movq	0x38(%rsp), %r14
 52878b0:      	movq	0x28(%rsp), %rdi
 52878b5:      	nopw	%cs:(%rax,%rax)
 52878bf:      	nop
 52878c0:      	addq	$0x20, %rbp
 52878c4:      	cmpq	%r15, %rbp
 52878c7:      	je	0x52877e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x940>
 52878cd:      	movq	(%rbp), %rax
 52878d1:      	orq	%rbx, %rax
 52878d4:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 52878da:      	je	0x52878c0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xa20>
 52878dc:      	jmp	0x52877e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x940>
 52878e1:      	movq	%rcx, 0x80(%rsp)
 52878e9:      	movq	%r12, 0x8(%rsp)
 52878ee:      	cmpq	%r13, %r12
 52878f1:      	movq	0x70(%rsp), %rbp
 52878f6:      	je	0x5288122 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1282>
 52878fc:      	movq	%rdx, 0x28(%rsp)
 5287901:      	movq	%r13, %rbx
 5287904:      	movq	0x8(%rsp), %r15
 5287909:      	subq	%r15, %rbx
 528790c:      	movq	%rbx, %rax
 528790f:      	sarq	$0x3, %rax
 5287913:      	bsrq	%rax, %rdx
 5287917:      	xorl	$0x3f, %edx
 528791a:      	addl	%edx, %edx
 528791c:      	xorq	$0x7e, %rdx
 5287920:      	movq	%r15, %rdi
 5287923:      	movq	%r13, %rsi
 5287926:      	callq	0x52a7c50 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPN4llvm16DwarfCompileUnitESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZNS2_10DwarfDebug16emitDebugARangesEvE3$_0EEEvT_SF_T0_T1_>
 528792b:      	leaq	0x8(%r15), %r9
 528792f:      	cmpq	$0x81, %rbx
 5287936:      	jl	0x52879d8 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb38>
 528793c:      	movl	$0x8, %r12d
 5287942:      	movq	%r9, %rbx
 5287945:      	movq	%r15, %rdi
 5287948:      	movq	0x28(%rsp), %r8
 528794d:      	jmp	0x528799b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xafb>
 528794f:      	nop
 5287950:      	cmpq	$0x9, %r12
 5287954:      	jb	0x52879d2 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb32>
 5287956:      	movq	%rdi, 0x30(%rsp)
 528795b:      	movq	%r9, %rdi
 528795e:      	movq	0x8(%rsp), %rsi
 5287963:      	movq	%r12, %rdx
 5287966:      	movq	%r9, %r15
 5287969:      	callq	0x828ac50 <memmove@plt>
 528796e:      	movq	0x30(%rsp), %rdi
 5287973:      	movq	%r15, %r9
 5287976:      	movq	0x28(%rsp), %r8
 528797b:      	movq	0x8(%rsp), %r15
 5287980:      	movq	%r15, %rcx
 5287983:      	movq	%rbp, (%rcx)
 5287986:      	addq	$0x8, %r12
 528798a:      	addq	$0x8, %rbx
 528798e:      	cmpq	$0x80, %r12
 5287995:      	je	0x5287a85 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbe5>
 528799b:      	movq	%rdi, %rcx
 528799e:      	leaq	(%r15,%r12), %rdi
 52879a2:      	movq	(%r15,%r12), %rbp
 52879a6:      	movq	(%r15), %rdx
 52879a9:      	movl	0x48(%rbp), %eax
 52879ac:      	cmpl	0x48(%rdx), %eax
 52879af:      	jb	0x5287950 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xab0>
 52879b1:      	movq	(%rcx), %rdx
 52879b4:      	movq	%rdi, %rcx
 52879b7:      	cmpl	0x48(%rdx), %eax
 52879ba:      	jae	0x5287983 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae3>
 52879bc:      	movq	%rbx, %rcx
 52879bf:      	nop
 52879c0:      	movq	%rdx, (%rcx)
 52879c3:      	movq	-0x10(%rcx), %rdx
 52879c7:      	addq	$-0x8, %rcx
 52879cb:      	cmpl	0x48(%rdx), %eax
 52879ce:      	jb	0x52879c0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb20>
 52879d0:      	jmp	0x5287983 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae3>
 52879d2:      	movq	%rdx, 0x8(%rcx)
 52879d6:      	jmp	0x5287980 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xae0>
 52879d8:      	movq	0x28(%rsp), %r8
 52879dd:      	cmpq	%r8, %r15
 52879e0:      	je	0x5287a9a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 52879e6:      	movq	0x8(%rsp), %rbx
 52879eb:      	jmp	0x5287a28 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb88>
 52879ed:      	nopl	(%rax)
 52879f0:      	movq	%rbx, %rdx
 52879f3:      	subq	%r12, %rdx
 52879f6:      	movq	%rdx, %rax
 52879f9:      	sarq	$0x3, %rax
 52879fd:      	cmpq	$0x2, %rax
 5287a01:      	jl	0x5287a74 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbd4>
 5287a03:      	shlq	$0x3, %rax
 5287a07:      	subq	%rax, %rdi
 5287a0a:      	addq	$0x10, %rdi
 5287a0e:      	movq	%r12, %rsi
 5287a11:      	callq	0x828ac50 <memmove@plt>
 5287a16:      	movq	0x28(%rsp), %r8
 5287a1b:      	movq	%r15, (%r12)
 5287a1f:      	leaq	0x8(%rbx), %r9
 5287a23:      	cmpq	%r8, %rbx
 5287a26:      	je	0x5287a9a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 5287a28:      	movq	%rbx, %rdi
 5287a2b:      	movq	%r9, %rbx
 5287a2e:      	movq	(%r9), %r15
 5287a31:      	movq	0x8(%rsp), %r12
 5287a36:      	movq	(%r12), %rsi
 5287a3a:      	movl	0x48(%r15), %ecx
 5287a3e:      	cmpl	0x48(%rsi), %ecx
 5287a41:      	jb	0x52879f0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb50>
 5287a43:      	movq	(%rdi), %rdx
 5287a46:      	movq	%rbx, %r12
 5287a49:      	cmpl	0x48(%rdx), %ecx
 5287a4c:      	jae	0x5287a1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 5287a4e:      	movq	%rbx, %r12
 5287a51:      	nopw	%cs:(%rax,%rax)
 5287a5b:      	nopl	(%rax,%rax)
 5287a60:      	movq	%rdx, (%r12)
 5287a64:      	movq	-0x10(%r12), %rdx
 5287a69:      	addq	$-0x8, %r12
 5287a6d:      	cmpl	0x48(%rdx), %ecx
 5287a70:      	jb	0x5287a60 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbc0>
 5287a72:      	jmp	0x5287a1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 5287a74:      	cmpq	$0x8, %rdx
 5287a78:      	jne	0x5287a1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 5287a7a:      	movq	%rsi, 0x8(%rdi)
 5287a7e:      	movq	0x8(%rsp), %r12
 5287a83:      	jmp	0x5287a1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xb7b>
 5287a85:      	leaq	0x80(%r15), %rax
 5287a8c:      	cmpq	%r13, %rax
 5287a8f:      	movq	0x70(%rsp), %rbp
 5287a94:      	jne	0x52880f0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1250>
 5287a9a:      	leal	(%rbp,%rbp), %eax
 5287a9e:      	movl	$0x7f, %ecx
 5287aa3:      	movq	%rax, 0xc0(%rsp)
 5287aab:      	bsrq	%rax, %rcx
 5287aaf:      	xorl	$0x3f, %ecx
 5287ab2:      	notb	%cl
 5287ab4:      	movl	$0x1, %eax
 5287ab9:      	shlq	%cl, %rax
 5287abc:      	leaq	-0x1(%rax), %rcx
 5287ac0:      	movq	%rcx, 0xb8(%rsp)
 5287ac8:      	negq	%rax
 5287acb:      	movq	%rax, 0x88(%rsp)
 5287ad3:      	movq	0x8(%rsp), %r15
 5287ad8:      	jmp	0x5287b4d <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xcad>
 5287ada:      	nopw	(%rax,%rax)
 5287ae0:      	movq	0x8(%r14), %rax
 5287ae4:      	movq	0x50(%rax), %rdi
 5287ae8:      	leaq	-0x45f2cfc(%rip), %rax  # 0xc94df3 <.L.str.97>
 5287aef:      	movq	%rax, 0x90(%rsp)
 5287af7:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287b01:      	movq	(%rdi), %rax
 5287b04:      	leaq	0x90(%rsp), %rsi
 5287b0c:      	movl	$0x1, %edx
 5287b11:      	callq	*0x78(%rax)
 5287b14:      	movq	0x8(%r14), %rax
 5287b18:      	movq	0x50(%rax), %rdi
 5287b1c:      	movq	(%rdi), %rax
 5287b1f:      	xorl	%esi, %esi
 5287b21:      	movl	%ebp, %edx
 5287b23:      	callq	*0x210(%rax)
 5287b29:      	movq	0x8(%r14), %rax
 5287b2d:      	movq	0x50(%rax), %rdi
 5287b31:      	movq	(%rdi), %rax
 5287b34:      	xorl	%esi, %esi
 5287b36:      	movl	%ebp, %edx
 5287b38:      	callq	*0x210(%rax)
 5287b3e:      	cmpq	0x28(%rsp), %r15
 5287b43:      	leaq	0x8(%r15), %r15
 5287b47:      	je	0x5288122 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1282>
 5287b4d:      	movq	%r15, 0x30(%rsp)
 5287b52:      	movq	(%r15), %r13
 5287b55:      	movl	0x20(%rsp), %esi
 5287b59:      	testl	%esi, %esi
 5287b5b:      	je	0x5287bd0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd30>
 5287b5d:      	movq	0x10(%rsp), %rax
 5287b62:      	movl	%r13d, %edx
 5287b65:      	shrl	$0x4, %edx
 5287b68:      	movl	%r13d, %ecx
 5287b6b:      	shrl	$0x9, %ecx
 5287b6e:      	xorl	%edx, %ecx
 5287b70:      	leal	-0x1(%rsi), %edx
 5287b73:      	andl	%edx, %ecx
 5287b75:      	movq	%rcx, %rdi
 5287b78:      	shlq	$0x5, %rdi
 5287b7c:      	leaq	(%rax,%rdi), %r15
 5287b80:      	movq	(%rax,%rdi), %r9
 5287b84:      	cmpq	%r9, %r13
 5287b87:      	je	0x5287c2e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd8e>
 5287b8d:      	movl	$0x1, %edi
 5287b92:      	xorl	%r8d, %r8d
 5287b95:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 5287b9c:      	je	0x5288060 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11c0>
 5287ba2:      	xorq	$-0x2000, %r9           # imm = 0xE000
 5287ba9:      	orq	%r8, %r9
 5287bac:      	cmoveq	%r15, %r8
 5287bb0:      	addl	%edi, %ecx
 5287bb2:      	incl	%edi
 5287bb4:      	andl	%edx, %ecx
 5287bb6:      	movq	%rcx, %r9
 5287bb9:      	shlq	$0x5, %r9
 5287bbd:      	leaq	(%rax,%r9), %r15
 5287bc1:      	movq	(%rax,%r9), %r9
 5287bc5:      	cmpq	%r9, %r13
 5287bc8:      	je	0x5287c2e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd8e>
 5287bca:      	jmp	0x5287b95 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xcf5>
 5287bcc:      	nopl	(%rax)
 5287bd0:      	xorl	%r15d, %r15d
 5287bd3:      	movq	%r15, 0x90(%rsp)
 5287bdb:      	movl	0x18(%rsp), %eax
 5287bdf:      	leal	0x4(,%rax,4), %ecx
 5287be6:      	leal	(%rsi,%rsi,2), %edx
 5287be9:      	cmpl	%edx, %ecx
 5287beb:      	jae	0x5288096 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11f6>
 5287bf1:      	movl	%eax, %ecx
 5287bf3:      	notl	%ecx
 5287bf5:      	addl	%esi, %ecx
 5287bf7:      	subl	0x1c(%rsp), %ecx
 5287bfb:      	movl	%esi, %edx
 5287bfd:      	shrl	$0x3, %edx
 5287c00:      	cmpl	%edx, %ecx
 5287c02:      	jbe	0x5288098 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11f8>
 5287c08:      	incl	%eax
 5287c0a:      	movl	%eax, 0x18(%rsp)
 5287c0e:      	cmpq	$-0x1000, (%r15)        # imm = 0xF000
 5287c15:      	je	0x5287c1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd7b>
 5287c17:      	decl	0x1c(%rsp)
 5287c1b:      	movq	%r13, (%r15)
 5287c1e:      	xorps	%xmm0, %xmm0
 5287c21:      	movups	%xmm0, 0x8(%r15)
 5287c26:      	movq	$0x0, 0x18(%r15)
 5287c2e:      	movq	0x158(%r13), %r12
 5287c35:      	testq	%r12, %r12
 5287c38:      	cmoveq	%r13, %r12
 5287c3c:      	movq	0x8(%r14), %rax
 5287c40:      	movq	0x50(%rax), %rdi
 5287c44:      	movq	0x8(%rdi), %rax
 5287c48:      	xorl	%ecx, %ecx
 5287c4a:      	cmpb	$0x0, 0x75a(%rax)
 5287c51:      	setne	%cl
 5287c54:      	movl	$0x18, %eax
 5287c59:      	movl	$0xc, %edx
 5287c5e:      	cmoveq	%rdx, %rax
 5287c62:      	movq	0xb8(%rsp), %rdx
 5287c6a:      	leaq	(%rdx,%rax), %r13
 5287c6e:      	andq	0x88(%rsp), %r13
 5287c76:      	subq	%rax, %r13
 5287c79:      	movq	0x10(%r15), %rax
 5287c7d:      	subq	0x8(%r15), %rax
 5287c81:      	leal	(%r13,%rcx,4), %ecx
 5287c86:      	shrq	$0x4, %rax
 5287c8a:      	incl	%eax
 5287c8c:      	imull	0xc0(%rsp), %eax
 5287c94:      	leal	0x8(%rax,%rcx), %esi
 5287c98:      	leaq	-0x4542ca9(%rip), %rax  # 0xd44ff6 <.L.str.92>
 5287c9f:      	movq	%rax, 0x90(%rsp)
 5287ca7:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287cb1:      	movq	(%rdi), %rax
 5287cb4:      	leaq	0x90(%rsp), %rbx
 5287cbc:      	movq	%rbx, %rdx
 5287cbf:      	callq	*0x4e8(%rax)
 5287cc5:      	movq	0x8(%r14), %rax
 5287cc9:      	movq	0x50(%rax), %rdi
 5287ccd:      	leaq	-0x4599ef4(%rip), %rax  # 0xcedde0 <.L.str.93>
 5287cd4:      	movq	%rax, 0x90(%rsp)
 5287cdc:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287ce6:      	movq	(%rdi), %rax
 5287ce9:      	movq	%rbx, %rsi
 5287cec:      	movl	$0x1, %edx
 5287cf1:      	callq	*0x78(%rax)
 5287cf4:      	movq	0x8(%r14), %rax
 5287cf8:      	movq	0x50(%rax), %rdi
 5287cfc:      	movq	(%rdi), %rax
 5287cff:      	movl	$0x2, %esi
 5287d04:      	movl	$0x2, %edx
 5287d09:      	callq	*0x210(%rax)
 5287d0f:      	movq	0x8(%r14), %rax
 5287d13:      	movq	0x50(%rax), %rdi
 5287d17:      	leaq	-0x45c5c91(%rip), %rax  # 0xcc208d <.L.str.94>
 5287d1e:      	movq	%rax, 0x90(%rsp)
 5287d26:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287d30:      	movq	(%rdi), %rax
 5287d33:      	movq	%rbx, %rsi
 5287d36:      	movl	$0x1, %edx
 5287d3b:      	callq	*0x78(%rax)
 5287d3e:      	movq	0x8(%r14), %rdi
 5287d42:      	cmpb	$0x1, 0xe21(%r14)
 5287d4a:      	jne	0x5287d80 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xee0>
 5287d4c:      	movq	0x38(%r12), %rax
 5287d51:      	movq	0x40(%r12), %rdx
 5287d56:      	movq	0x8(%rax), %rsi
 5287d5a:      	movq	0x50(%rdi), %rax
 5287d5e:      	movq	0x8(%rax), %rax
 5287d62:      	xorl	%ecx, %ecx
 5287d64:      	cmpb	$0x0, 0x75a(%rax)
 5287d6b:      	setne	%cl
 5287d6e:      	leal	0x4(,%rcx,4), %ecx
 5287d75:      	xorl	%r8d, %r8d
 5287d78:      	callq	0x5261fd0 <_ZNK4llvm10AsmPrinter19emitLabelPlusOffsetEPKNS_8MCSymbolEmjb>
 5287d7d:      	jmp	0x5287d8f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xeef>
 5287d7f:      	nop
 5287d80:      	movq	0xc0(%r12), %rsi
 5287d88:      	xorl	%edx, %edx
 5287d8a:      	callq	0x526e5e0 <_ZNK4llvm10AsmPrinter24emitDwarfSymbolReferenceEPKNS_8MCSymbolEb>
 5287d8f:      	movq	0x8(%r14), %rax
 5287d93:      	movq	0x50(%rax), %rdi
 5287d97:      	leaq	-0x44fc968(%rip), %rax  # 0xd8b436 <.L.str.95>
 5287d9e:      	movq	%rax, 0x90(%rsp)
 5287da6:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287db0:      	movq	(%rdi), %rax
 5287db3:      	leaq	0x90(%rsp), %rbx
 5287dbb:      	movq	%rbx, %rsi
 5287dbe:      	movl	$0x1, %edx
 5287dc3:      	callq	*0x78(%rax)
 5287dc6:      	movq	0x8(%r14), %rax
 5287dca:      	movq	0x50(%rax), %rdi
 5287dce:      	movq	(%rdi), %rax
 5287dd1:      	movq	%rbp, %rsi
 5287dd4:      	movl	$0x1, %edx
 5287dd9:      	callq	*0x210(%rax)
 5287ddf:      	movq	0x8(%r14), %rax
 5287de3:      	movq	0x50(%rax), %rdi
 5287de7:      	leaq	-0x456fca7(%rip), %rax  # 0xd18147 <.L.str.96>
 5287dee:      	movq	%rax, 0x90(%rsp)
 5287df6:      	movw	$0x103, 0xb0(%rsp)      # imm = 0x103
 5287e00:      	movq	(%rdi), %rax
 5287e03:      	movq	%rbx, %rsi
 5287e06:      	movl	$0x1, %edx
 5287e0b:      	callq	*0x78(%rax)
 5287e0e:      	movq	0x8(%r14), %rax
 5287e12:      	movq	0x50(%rax), %rdi
 5287e16:      	movq	(%rdi), %rax
 5287e19:      	xorl	%esi, %esi
 5287e1b:      	movl	$0x1, %edx
 5287e20:      	callq	*0x210(%rax)
 5287e26:      	movl	$0xffffffff, %eax       # imm = 0xFFFFFFFF
 5287e2b:      	andq	%rax, %r13
 5287e2e:      	je	0x5287ea0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1000>
 5287e30:      	movq	0x8(%r14), %rax
 5287e34:      	movq	0x50(%rax), %rdi
 5287e38:      	movq	0x8(%rdi), %rcx
 5287e3c:      	addq	$0x18, 0x110(%rcx)
 5287e44:      	leaq	0xc0(%rcx), %rax
 5287e4b:      	movq	0xc0(%rcx), %rsi
 5287e52:      	testq	%rsi, %rsi
 5287e55:      	je	0x528806c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11cc>
 5287e5b:      	addq	$0x7, %rsi
 5287e5f:      	andq	$-0x8, %rsi
 5287e63:      	leaq	0x18(%rsi), %rdx
 5287e67:      	cmpq	0xc8(%rcx), %rdx
 5287e6e:      	ja	0x528806c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11cc>
 5287e74:      	movq	%rdx, (%rax)
 5287e77:      	movb	$0x1, (%rsi)
 5287e7a:      	movzbl	0x4(%rsi), %eax
 5287e7e:      	shll	$0x18, %eax
 5287e81:      	movl	%eax, 0x1(%rsi)
 5287e84:      	movq	$0x0, 0x8(%rsi)
 5287e8c:      	movq	%r13, 0x10(%rsi)
 5287e90:      	movq	(%rdi), %rax
 5287e93:      	movl	$0xff, %edx
 5287e98:      	xorl	%ecx, %ecx
 5287e9a:      	callq	*0x240(%rax)
 5287ea0:      	movq	0x8(%r15), %r13
 5287ea4:      	movq	0x10(%r15), %rbx
 5287ea8:      	cmpq	%rbx, %r13
 5287eab:      	movq	0x30(%rsp), %r15
 5287eb0:      	jne	0x5287ef1 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1051>
 5287eb2:      	jmp	0x5287ae0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5287eb7:      	nopw	(%rax,%rax)
 5287ec0:      	movq	0x8(%r13), %rax
 5287ec4:      	testq	%rax, %rax
 5287ec7:      	je	0x528801a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x117a>
 5287ecd:      	movq	0x8(%r14), %rcx
 5287ed1:      	movq	0x50(%rcx), %rdi
 5287ed5:      	movq	(%rdi), %r8
 5287ed8:      	movq	%rax, %rsi
 5287edb:      	movl	%ebp, %ecx
 5287edd:      	callq	*0x330(%r8)
 5287ee4:      	addq	$0x10, %r13
 5287ee8:      	cmpq	%rbx, %r13
 5287eeb:      	je	0x5287ae0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5287ef1:      	movq	0x8(%r14), %r12
 5287ef5:      	movq	(%r13), %rbp
 5287ef9:      	movq	0x48(%r12), %rax
 5287efe:      	addq	$0x18, 0x110(%rax)
 5287f06:      	leaq	0xc0(%rax), %rdi
 5287f0d:      	movq	0xc0(%rax), %rsi
 5287f14:      	testq	%rsi, %rsi
 5287f17:      	je	0x5288044 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11a4>
 5287f1d:      	addq	$0x7, %rsi
 5287f21:      	andq	$-0x8, %rsi
 5287f25:      	leaq	0x18(%rsi), %rcx
 5287f29:      	cmpq	0xc8(%rax), %rcx
 5287f30:      	ja	0x5288044 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x11a4>
 5287f36:      	movq	%rcx, (%rdi)
 5287f39:      	testq	%rsi, %rsi
 5287f3c:      	je	0x5287f60 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x10c0>
 5287f3e:      	movb	$0x2, (%rsi)
 5287f41:      	movzbl	0x4(%rsi), %eax
 5287f45:      	shll	$0x18, %eax
 5287f48:      	movl	%eax, 0x1(%rsi)
 5287f4b:      	movq	$0x0, 0x8(%rsi)
 5287f53:      	movq	%rbp, 0x10(%rsi)
 5287f57:      	jmp	0x5287f62 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x10c2>
 5287f59:      	nopl	(%rax)
 5287f60:      	xorl	%esi, %esi
 5287f62:      	movq	0x50(%r12), %rdi
 5287f67:      	movq	(%rdi), %rax
 5287f6a:      	movq	0x70(%rsp), %rbp
 5287f6f:      	movl	%ebp, %edx
 5287f71:      	xorl	%ecx, %ecx
 5287f73:      	callq	*0x208(%rax)
 5287f79:      	movq	(%r13), %rdx
 5287f7d:      	movq	0x2b0(%r14), %rax
 5287f84:      	movl	0x2c0(%r14), %ecx
 5287f8b:      	testq	%rcx, %rcx
 5287f8e:      	je	0x5287fe0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1140>
 5287f90:      	movl	%edx, %edi
 5287f92:      	shrl	$0x4, %edi
 5287f95:      	movl	%edx, %esi
 5287f97:      	shrl	$0x9, %esi
 5287f9a:      	xorl	%edi, %esi
 5287f9c:      	leal	-0x1(%rcx), %edi
 5287f9f:      	andl	%edi, %esi
 5287fa1:      	movl	%esi, %r8d
 5287fa4:      	shll	$0x4, %r8d
 5287fa8:      	movq	(%rax,%r8), %r10
 5287fac:      	cmpq	%r10, %rdx
 5287faf:      	je	0x5287fe7 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1147>
 5287fb1:      	movl	$0x1, %r9d
 5287fb7:      	cmpq	$-0x1000, %r10          # imm = 0xF000
 5287fbe:      	je	0x5287fe0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1140>
 5287fc0:      	addl	%r9d, %esi
 5287fc3:      	incl	%r9d
 5287fc6:      	andl	%edi, %esi
 5287fc8:      	movq	%rsi, %r10
 5287fcb:      	shlq	$0x4, %r10
 5287fcf:      	leaq	(%rax,%r10), %r8
 5287fd3:      	movq	(%rax,%r10), %r10
 5287fd7:      	cmpq	%r10, %rdx
 5287fda:      	je	0x5287fea <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x114a>
 5287fdc:      	jmp	0x5287fb7 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1117>
 5287fde:      	nop
 5287fe0:      	movq	%rcx, %r8
 5287fe3:      	shlq	$0x4, %r8
 5287fe7:      	addq	%rax, %r8
 5287fea:      	shlq	$0x4, %rcx
 5287fee:      	addq	%rcx, %rax
 5287ff1:      	cmpq	%rax, %r8
 5287ff4:      	je	0x5287ec0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1020>
 5287ffa:      	movq	0x8(%r8), %rsi
 5287ffe:      	testq	%rsi, %rsi
 5288001:      	je	0x5288010 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1170>
 5288003:      	movq	0x8(%r13), %rax
 5288007:      	testq	%rax, %rax
 528800a:      	jne	0x5287ecd <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x102d>
 5288010:      	cmpq	$0x1, %rsi
 5288014:      	adcq	$0x0, %rsi
 5288018:      	jmp	0x528801f <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x117f>
 528801a:      	movl	$0x1, %esi
 528801f:      	movq	0x8(%r14), %rax
 5288023:      	movq	0x50(%rax), %rdi
 5288027:      	movq	(%rdi), %rax
 528802a:      	movl	%ebp, %edx
 528802c:      	callq	*0x210(%rax)
 5288032:      	addq	$0x10, %r13
 5288036:      	cmpq	%rbx, %r13
 5288039:      	jne	0x5287ef1 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1051>
 528803f:      	jmp	0x5287ae0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xc40>
 5288044:      	movl	$0x18, %esi
 5288049:      	movl	$0x18, %edx
 528804e:      	movl	$0x3, %ecx
 5288053:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 5288058:      	movq	%rax, %rsi
 528805b:      	jmp	0x5287f3e <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x109e>
 5288060:      	testq	%r8, %r8
 5288063:      	cmovneq	%r8, %r15
 5288067:      	jmp	0x5287bd3 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd33>
 528806c:      	movl	$0x18, %esi
 5288071:      	movl	$0x18, %edx
 5288076:      	movq	%rdi, %r14
 5288079:      	movq	%rax, %rdi
 528807c:      	movl	$0x3, %ecx
 5288081:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 5288086:      	movq	%r14, %rdi
 5288089:      	movq	0x38(%rsp), %r14
 528808e:      	movq	%rax, %rsi
 5288091:      	jmp	0x5287e77 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xfd7>
 5288096:      	addl	%esi, %esi
 5288098:      	leaq	0x10(%rsp), %rdi
 528809d:      	callq	0x52a7a10 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E4growEj>
 52880a2:      	movq	0x10(%rsp), %rdi
 52880a7:      	movl	0x20(%rsp), %esi
 52880ab:      	movq	%r13, %rdx
 52880ae:      	leaq	0x90(%rsp), %rcx
 52880b6:      	callq	0x52a7990 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_16DwarfCompileUnitESt6vectorI10ArangeSpanSaIS5_EENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S7_EEEES3_S7_S9_SC_E15LookupBucketForIS3_EEbRKT_RPSC_>
 52880bb:      	movl	0x18(%rsp), %eax
 52880bf:      	movq	0x90(%rsp), %r15
 52880c7:      	incl	%eax
 52880c9:      	movl	%eax, 0x18(%rsp)
 52880cd:      	cmpq	$-0x1000, (%r15)        # imm = 0xF000
 52880d4:      	jne	0x5287c17 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd77>
 52880da:      	jmp	0x5287c1b <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xd7b>
 52880df:      	nop
 52880e0:      	movq	%rcx, (%rdi)
 52880e3:      	cmpq	%r8, %rax
 52880e6:      	leaq	0x8(%rax), %rax
 52880ea:      	je	0x5287a9a <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0xbfa>
 52880f0:      	movq	-0x8(%rax), %rdx
 52880f4:      	movq	(%rax), %rcx
 52880f7:      	movl	0x48(%rcx), %esi
 52880fa:      	movq	%rax, %rdi
 52880fd:      	cmpl	0x48(%rdx), %esi
 5288100:      	jae	0x52880e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1240>
 5288102:      	movq	%rax, %rdi
 5288105:      	nopw	%cs:(%rax,%rax)
 528810f:      	nop
 5288110:      	movq	%rdx, (%rdi)
 5288113:      	movq	-0x10(%rdi), %rdx
 5288117:      	addq	$-0x8, %rdi
 528811b:      	cmpl	0x48(%rdx), %esi
 528811e:      	jb	0x5288110 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1270>
 5288120:      	jmp	0x52880e0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1240>
 5288122:      	movq	0x8(%rsp), %rdi
 5288127:      	testq	%rdi, %rdi
 528812a:      	je	0x528813c <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x129c>
 528812c:      	movq	0x80(%rsp), %rsi
 5288134:      	subq	%rdi, %rsi
 5288137:      	callq	0x828a6f0 <_ZdlPvm@plt>
 528813c:      	movl	0x20(%rsp), %ebx
 5288140:      	movq	0x10(%rsp), %r14
 5288145:      	testq	%rbx, %rbx
 5288148:      	je	0x5288191 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12f1>
 528814a:      	shlq	$0x5, %rbx
 528814e:      	xorl	%r15d, %r15d
 5288151:      	movl	$0x1000, %r12d          # imm = 0x1000
 5288157:      	leaq	0x68(%rsp), %r13
 528815c:      	jmp	0x5288169 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c9>
 528815e:      	nop
 5288160:      	addq	$0x20, %r15
 5288164:      	cmpq	%r15, %rbx
 5288167:      	je	0x5288198 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12f8>
 5288169:      	movq	(%r14,%r15), %rax
 528816d:      	orq	%r12, %rax
 5288170:      	cmpq	$-0x1000, %rax          # imm = 0xF000
 5288176:      	je	0x5288160 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 5288178:      	movq	0x8(%r14,%r15), %rdi
 528817d:      	testq	%rdi, %rdi
 5288180:      	je	0x5288160 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 5288182:      	movq	0x18(%r14,%r15), %rsi
 5288187:      	subq	%rdi, %rsi
 528818a:      	callq	0x828a6f0 <_ZdlPvm@plt>
 528818f:      	jmp	0x5288160 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x12c0>
 5288191:      	xorl	%ebx, %ebx
 5288193:      	leaq	0x68(%rsp), %r13
 5288198:      	movl	$0x8, %edx
 528819d:      	movq	%r14, %rdi
 52881a0:      	movq	%rbx, %rsi
 52881a3:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 52881a8:      	movq	0x58(%rsp), %rbx
 52881ad:      	movl	0x60(%rsp), %eax
 52881b1:      	testq	%rax, %rax
 52881b4:      	je	0x52881f6 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1356>
 52881b6:      	imulq	$0x98, %rax, %r14
 52881bd:      	leaq	-0x80(%rbx), %r15
 52881c1:      	jmp	0x52881d9 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1339>
 52881c3:      	nopw	%cs:(%rax,%rax)
 52881cd:      	nopl	(%rax)
 52881d0:      	addq	$-0x98, %r14
 52881d7:      	je	0x52881f1 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1351>
 52881d9:      	movq	-0x90(%rbx,%r14), %rdi
 52881e1:      	leaq	(%r15,%r14), %rax
 52881e5:      	cmpq	%rdi, %rax
 52881e8:      	je	0x52881d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1330>
 52881ea:      	callq	0x828a6d0 <free@plt>
 52881ef:      	jmp	0x52881d0 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1330>
 52881f1:      	movq	0x58(%rsp), %rbx
 52881f6:      	cmpq	%r13, %rbx
 52881f9:      	je	0x5288203 <_ZN4llvm10DwarfDebug16emitDebugARangesEv+0x1363>
 52881fb:      	movq	%rbx, %rdi
 52881fe:      	callq	0x828a6d0 <free@plt>
 5288203:      	movq	0x40(%rsp), %rdi
 5288208:      	movl	0x50(%rsp), %esi
 528820c:      	shlq	$0x4, %rsi
 5288210:      	movl	$0x8, %edx
 5288215:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 528821a:      	addq	$0xc8, %rsp
 5288221:      	popq	%rbx
 5288222:      	popq	%r12
 5288224:      	popq	%r13
 5288226:      	popq	%r14
 5288228:      	popq	%r15
 528822a:      	popq	%rbp
 528822b:      	retq
 528822c:      	leaq	-0x45ed849(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 5288233:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
