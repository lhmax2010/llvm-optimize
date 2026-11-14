
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000534bf90 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE>:
 534bf90:      	pushq	%rbp
 534bf91:      	pushq	%r15
 534bf93:      	pushq	%r14
 534bf95:      	pushq	%r13
 534bf97:      	pushq	%r12
 534bf99:      	pushq	%rbx
 534bf9a:      	subq	$0x28, %rsp
 534bf9e:      	movq	%rdx, %r12
 534bfa1:      	movq	%rsi, 0x18(%rsp)
 534bfa6:      	movq	%rdx, 0x20(%rsp)
 534bfab:      	movslq	%r12d, %r13
 534bfae:      	pxor	%xmm0, %xmm0
 534bfb2:      	movdqu	%xmm0, (%rdi)
 534bfb6:      	movq	%rdi, 0x8(%rsp)
 534bfbb:      	movq	$0x0, 0x10(%rdi)
 534bfc3:      	movq	%r13, %rax
 534bfc6:      	shrq	$0x3d, %rax
 534bfca:      	jne	0x534c32a <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x39a>
 534bfd0:      	movq	%r12, %rdi
 534bfd3:      	shlq	$0x20, %rdi
 534bfd7:      	je	0x534c316 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534bfdd:      	movq	%rsi, %r14
 534bfe0:      	sarq	$0x1e, %rdi
 534bfe4:      	callq	0x828a6b0 <_Znwm@plt>
 534bfe9:      	movq	%rax, %r15
 534bfec:      	movq	0x8(%rsp), %rcx
 534bff1:      	movq	%rax, (%rcx)
 534bff4:      	leaq	(%rax,%r13,4), %rax
 534bff8:      	movq	%rax, 0x10(%rcx)
 534bffc:      	cmpq	$0x8, %r13
 534c000:      	jae	0x534c039 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0xa9>
 534c002:      	xorl	%eax, %eax
 534c004:      	xorl	%ecx, %ecx
 534c006:      	movl	%ecx, (%r15,%rax)
 534c00a:      	leaq	0x4(%rax), %rdx
 534c00e:      	cmpl	$0x2, %r13d
 534c012:      	jb	0x534c0ac <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x11c>
 534c018:      	leal	0x1(%rcx), %esi
 534c01b:      	movl	%esi, 0x4(%r15,%rax)
 534c020:      	leaq	0x8(%rax), %rsi
 534c024:      	cmpl	$0x2, %r13d
 534c028:      	jne	0x534c0b1 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x121>
 534c02e:      	movq	%rdx, %rbp
 534c031:      	movq	%rsi, %rax
 534c034:      	jmp	0x534c11e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534c039:      	andl	$0x7, %r12d
 534c03d:      	subq	%r12, %r13
 534c040:      	leaq	(,%r13,4), %rax
 534c048:      	movl	%r13d, %ecx
 534c04b:      	movdqa	-0x4535ce3(%rip), %xmm0 # 0xe16370 <.L__const._ZNK12_GLOBAL__N_19OpenMPOpt9printICVsEv.ICVs>
 534c053:      	xorl	%edx, %edx
 534c055:      	movdqa	-0x453532d(%rip), %xmm1 # 0xe16d30 <.LCPI9_1>
 534c05d:      	movdqa	-0x4539035(%rip), %xmm2 # 0xe13030 <.LCPI9_2>
 534c065:      	nopw	%cs:(%rax,%rax)
 534c06f:      	nop
 534c070:      	movdqa	%xmm0, %xmm3
 534c074:      	paddd	%xmm1, %xmm3
 534c078:      	movdqu	%xmm0, (%r15,%rdx,4)
 534c07e:      	movdqu	%xmm3, 0x10(%r15,%rdx,4)
 534c085:      	addq	$0x8, %rdx
 534c089:      	paddd	%xmm2, %xmm0
 534c08d:      	cmpq	%rdx, %r13
 534c090:      	jne	0x534c070 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0xe0>
 534c092:      	testq	%r12, %r12
 534c095:      	je	0x534c112 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x182>
 534c097:      	movq	%r12, %r13
 534c09a:      	movl	%ecx, (%r15,%rax)
 534c09e:      	leaq	0x4(%rax), %rdx
 534c0a2:      	cmpl	$0x2, %r13d
 534c0a6:      	jae	0x534c018 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x88>
 534c0ac:      	movq	%rax, %rbp
 534c0af:      	jmp	0x534c11b <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18b>
 534c0b1:      	leal	0x2(%rcx), %edx
 534c0b4:      	movl	%edx, 0x8(%r15,%rax)
 534c0b9:      	leaq	0xc(%rax), %rdx
 534c0bd:      	cmpl	$0x4, %r13d
 534c0c1:      	jb	0x534c118 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x188>
 534c0c3:      	leal	0x3(%rcx), %esi
 534c0c6:      	movl	%esi, 0xc(%r15,%rax)
 534c0cb:      	leaq	0x10(%rax), %rsi
 534c0cf:      	cmpl	$0x4, %r13d
 534c0d3:      	je	0x534c02e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x9e>
 534c0d9:      	leal	0x4(%rcx), %edx
 534c0dc:      	movl	%edx, 0x10(%r15,%rax)
 534c0e1:      	leaq	0x14(%rax), %rdx
 534c0e5:      	cmpl	$0x6, %r13d
 534c0e9:      	jb	0x534c118 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x188>
 534c0eb:      	leal	0x5(%rcx), %esi
 534c0ee:      	movl	%esi, 0x14(%r15,%rax)
 534c0f3:      	leaq	0x18(%rax), %rsi
 534c0f7:      	cmpl	$0x7, %r13d
 534c0fb:      	jne	0x534c02e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x9e>
 534c101:      	addl	$0x6, %ecx
 534c104:      	movl	%ecx, 0x18(%r15,%rax)
 534c109:      	addq	$0x1c, %rax
 534c10d:      	movq	%rsi, %rbp
 534c110:      	jmp	0x534c11e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534c112:      	leaq	-0x4(%rax), %rbp
 534c116:      	jmp	0x534c11e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534c118:      	movq	%rsi, %rbp
 534c11b:      	movq	%rdx, %rax
 534c11e:      	leaq	(%r15,%rax), %rbx
 534c122:      	movq	0x8(%rsp), %rcx
 534c127:      	movq	%rbx, 0x8(%rcx)
 534c12b:      	shrq	$0x2, %rax
 534c12f:      	bsrq	%rax, %rdx
 534c133:      	xorl	$0x3f, %edx
 534c136:      	addl	%edx, %edx
 534c138:      	xorq	$0x7e, %rdx
 534c13c:      	leaq	0x18(%rsp), %rcx
 534c141:      	movq	%r15, %rdi
 534c144:      	movq	%rbx, %rsi
 534c147:      	callq	0x53556b0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEElNS0_5__ops15_Iter_comp_iterIZN4llvm3lto23generateModulesOrderingENS9_8ArrayRefIPNS9_13BitcodeModuleEEEE3$_0EEEvT_SH_T0_T1_>
 534c14c:      	leaq	0x4(%r15), %r8
 534c150:      	cmpq	$0x40, %rbp
 534c154:      	jb	0x534c16b <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x1db>
 534c156:      	movq	%rbx, 0x10(%rsp)
 534c15b:      	movl	$0x4, %ebp
 534c160:      	movq	%r8, %r13
 534c163:      	movq	%r15, %rdi
 534c166:      	jmp	0x534c237 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x2a7>
 534c16b:      	testq	%rbp, %rbp
 534c16e:      	je	0x534c316 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c174:      	addq	%r15, %rbp
 534c177:      	movq	%r15, %r12
 534c17a:      	jmp	0x534c1b9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x229>
 534c17c:      	nopl	(%rax)
 534c180:      	movq	%r12, %rdx
 534c183:      	subq	%r15, %rdx
 534c186:      	movq	%rdx, %rax
 534c189:      	sarq	$0x2, %rax
 534c18d:      	cmpq	$0x2, %rax
 534c191:      	jl	0x534c206 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x276>
 534c193:      	shlq	$0x2, %rax
 534c197:      	subq	%rax, %rdi
 534c19a:      	addq	$0x8, %rdi
 534c19e:      	movq	%r15, %rsi
 534c1a1:      	callq	0x828ac50 <memmove@plt>
 534c1a6:      	movq	%r15, %rcx
 534c1a9:      	movl	%ebx, (%rcx)
 534c1ab:      	leaq	0x4(%r12), %r8
 534c1b0:      	cmpq	%rbp, %r12
 534c1b3:      	je	0x534c316 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c1b9:      	movq	%r12, %rdi
 534c1bc:      	movq	%r8, %r12
 534c1bf:      	movslq	(%r8), %rbx
 534c1c2:      	movslq	(%r15), %rsi
 534c1c5:      	movq	(%r14,%rbx,8), %rax
 534c1c9:      	movq	0x8(%rax), %rax
 534c1cd:      	movq	(%r14,%rsi,8), %rcx
 534c1d1:      	cmpq	0x8(%rcx), %rax
 534c1d5:      	ja	0x534c180 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x1f0>
 534c1d7:      	movslq	(%rdi), %rdx
 534c1da:      	movq	(%r14,%rdx,8), %rsi
 534c1de:      	movq	%r12, %rcx
 534c1e1:      	cmpq	0x8(%rsi), %rax
 534c1e5:      	jbe	0x534c1a9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c1e7:      	movq	%r12, %rcx
 534c1ea:      	nopw	(%rax,%rax)
 534c1f0:      	movl	%edx, (%rcx)
 534c1f2:      	movslq	-0x8(%rcx), %rdx
 534c1f6:      	movq	(%r14,%rdx,8), %rsi
 534c1fa:      	addq	$-0x4, %rcx
 534c1fe:      	cmpq	0x8(%rsi), %rax
 534c202:      	ja	0x534c1f0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x260>
 534c204:      	jmp	0x534c1a9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c206:      	movq	%r15, %rcx
 534c209:      	cmpq	$0x4, %rdx
 534c20d:      	jne	0x534c1a9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c20f:      	movl	%esi, 0x4(%rdi)
 534c212:      	jmp	0x534c1a6 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x216>
 534c214:      	movl	%edx, 0x4(%rcx)
 534c217:      	nopw	(%rax,%rax)
 534c220:      	movq	%r15, %rcx
 534c223:      	movl	%ebx, (%rcx)
 534c225:      	addq	$0x4, %rbp
 534c229:      	addq	$0x4, %r13
 534c22d:      	cmpq	$0x40, %rbp
 534c231:      	je	0x534c2b9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x329>
 534c237:      	movq	%rdi, %rcx
 534c23a:      	leaq	(%r15,%rbp), %rdi
 534c23e:      	movslq	(%r15,%rbp), %rbx
 534c242:      	movslq	(%r15), %rdx
 534c245:      	movq	(%r14,%rbx,8), %rax
 534c249:      	movq	0x8(%rax), %rax
 534c24d:      	movq	(%r14,%rdx,8), %rsi
 534c251:      	cmpq	0x8(%rsi), %rax
 534c255:      	jbe	0x534c280 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x2f0>
 534c257:      	cmpq	$0x5, %rbp
 534c25b:      	jb	0x534c214 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x284>
 534c25d:      	movq	%r8, %rdi
 534c260:      	movq	%r15, %rsi
 534c263:      	movq	%rbp, %rdx
 534c266:      	movq	%r8, %r12
 534c269:      	callq	0x828ac50 <memmove@plt>
 534c26e:      	leaq	(%r15,%rbp), %rdi
 534c272:      	movq	%r12, %r8
 534c275:      	jmp	0x534c220 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x290>
 534c277:      	nopw	(%rax,%rax)
 534c280:      	movslq	(%rcx), %rdx
 534c283:      	movq	(%r14,%rdx,8), %rsi
 534c287:      	movq	%rdi, %rcx
 534c28a:      	cmpq	0x8(%rsi), %rax
 534c28e:      	jbe	0x534c223 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x293>
 534c290:      	movq	%r13, %rcx
 534c293:      	nopw	%cs:(%rax,%rax)
 534c29d:      	nopl	(%rax)
 534c2a0:      	movl	%edx, (%rcx)
 534c2a2:      	movslq	-0x8(%rcx), %rdx
 534c2a6:      	movq	(%r14,%rdx,8), %rsi
 534c2aa:      	addq	$-0x4, %rcx
 534c2ae:      	cmpq	0x8(%rsi), %rax
 534c2b2:      	ja	0x534c2a0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x310>
 534c2b4:      	jmp	0x534c223 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x293>
 534c2b9:      	addq	$0x40, %r15
 534c2bd:      	movq	0x10(%rsp), %r8
 534c2c2:      	jmp	0x534c2db <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x34b>
 534c2c4:      	nopw	%cs:(%rax,%rax)
 534c2ce:      	nop
 534c2d0:      	movl	%eax, (%rsi)
 534c2d2:      	addq	$0x4, %r15
 534c2d6:      	cmpq	%r8, %r15
 534c2d9:      	je	0x534c316 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c2db:      	movslq	(%r15), %rax
 534c2de:      	movq	(%r14,%rax,8), %rcx
 534c2e2:      	movq	0x8(%rcx), %rcx
 534c2e6:      	movslq	-0x4(%r15), %rdx
 534c2ea:      	movq	(%r14,%rdx,8), %rdi
 534c2ee:      	movq	%r15, %rsi
 534c2f1:      	cmpq	0x8(%rdi), %rcx
 534c2f5:      	jbe	0x534c2d0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x340>
 534c2f7:      	movq	%r15, %rsi
 534c2fa:      	nopw	(%rax,%rax)
 534c300:      	movl	%edx, (%rsi)
 534c302:      	movslq	-0x8(%rsi), %rdx
 534c306:      	movq	(%r14,%rdx,8), %rdi
 534c30a:      	addq	$-0x4, %rsi
 534c30e:      	cmpq	0x8(%rdi), %rcx
 534c312:      	ja	0x534c300 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x370>
 534c314:      	jmp	0x534c2d0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x340>
 534c316:      	movq	0x8(%rsp), %rax
 534c31b:      	addq	$0x28, %rsp
 534c31f:      	popq	%rbx
 534c320:      	popq	%r12
 534c322:      	popq	%r13
 534c324:      	popq	%r14
 534c326:      	popq	%r15
 534c328:      	popq	%rbp
 534c329:      	retq
 534c32a:      	leaq	-0x455749f(%rip), %rdi  # 0xdf4e92 <.str.51.llvm.10292854006899487944>
 534c331:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
