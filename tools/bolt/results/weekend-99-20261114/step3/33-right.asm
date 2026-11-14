
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000534bf00 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE>:
 534bf00:      	pushq	%rbp
 534bf01:      	pushq	%r15
 534bf03:      	pushq	%r14
 534bf05:      	pushq	%r13
 534bf07:      	pushq	%r12
 534bf09:      	pushq	%rbx
 534bf0a:      	subq	$0x28, %rsp
 534bf0e:      	movq	%rdx, %r12
 534bf11:      	movq	%rsi, 0x18(%rsp)
 534bf16:      	movq	%rdx, 0x20(%rsp)
 534bf1b:      	movslq	%r12d, %r13
 534bf1e:      	pxor	%xmm0, %xmm0
 534bf22:      	movdqu	%xmm0, (%rdi)
 534bf26:      	movq	%rdi, 0x8(%rsp)
 534bf2b:      	movq	$0x0, 0x10(%rdi)
 534bf33:      	movq	%r13, %rax
 534bf36:      	shrq	$0x3d, %rax
 534bf3a:      	jne	0x534c29a <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x39a>
 534bf40:      	movq	%r12, %rdi
 534bf43:      	shlq	$0x20, %rdi
 534bf47:      	je	0x534c286 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534bf4d:      	movq	%rsi, %r14
 534bf50:      	sarq	$0x1e, %rdi
 534bf54:      	callq	0x828a620 <_Znwm@plt>
 534bf59:      	movq	%rax, %r15
 534bf5c:      	movq	0x8(%rsp), %rcx
 534bf61:      	movq	%rax, (%rcx)
 534bf64:      	leaq	(%rax,%r13,4), %rax
 534bf68:      	movq	%rax, 0x10(%rcx)
 534bf6c:      	cmpq	$0x8, %r13
 534bf70:      	jae	0x534bfa9 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0xa9>
 534bf72:      	xorl	%eax, %eax
 534bf74:      	xorl	%ecx, %ecx
 534bf76:      	movl	%ecx, (%r15,%rax)
 534bf7a:      	leaq	0x4(%rax), %rdx
 534bf7e:      	cmpl	$0x2, %r13d
 534bf82:      	jb	0x534c01c <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x11c>
 534bf88:      	leal	0x1(%rcx), %esi
 534bf8b:      	movl	%esi, 0x4(%r15,%rax)
 534bf90:      	leaq	0x8(%rax), %rsi
 534bf94:      	cmpl	$0x2, %r13d
 534bf98:      	jne	0x534c021 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x121>
 534bf9e:      	movq	%rdx, %rbp
 534bfa1:      	movq	%rsi, %rax
 534bfa4:      	jmp	0x534c08e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534bfa9:      	andl	$0x7, %r12d
 534bfad:      	subq	%r12, %r13
 534bfb0:      	leaq	(,%r13,4), %rax
 534bfb8:      	movl	%r13d, %ecx
 534bfbb:      	movdqa	-0x4535c53(%rip), %xmm0 # 0xe16370 <.L__const._ZNK12_GLOBAL__N_19OpenMPOpt9printICVsEv.ICVs>
 534bfc3:      	xorl	%edx, %edx
 534bfc5:      	movdqa	-0x453529d(%rip), %xmm1 # 0xe16d30 <.LCPI9_1>
 534bfcd:      	movdqa	-0x4538fa5(%rip), %xmm2 # 0xe13030 <.LCPI9_2>
 534bfd5:      	nopw	%cs:(%rax,%rax)
 534bfdf:      	nop
 534bfe0:      	movdqa	%xmm0, %xmm3
 534bfe4:      	paddd	%xmm1, %xmm3
 534bfe8:      	movdqu	%xmm0, (%r15,%rdx,4)
 534bfee:      	movdqu	%xmm3, 0x10(%r15,%rdx,4)
 534bff5:      	addq	$0x8, %rdx
 534bff9:      	paddd	%xmm2, %xmm0
 534bffd:      	cmpq	%rdx, %r13
 534c000:      	jne	0x534bfe0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0xe0>
 534c002:      	testq	%r12, %r12
 534c005:      	je	0x534c082 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x182>
 534c007:      	movq	%r12, %r13
 534c00a:      	movl	%ecx, (%r15,%rax)
 534c00e:      	leaq	0x4(%rax), %rdx
 534c012:      	cmpl	$0x2, %r13d
 534c016:      	jae	0x534bf88 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x88>
 534c01c:      	movq	%rax, %rbp
 534c01f:      	jmp	0x534c08b <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18b>
 534c021:      	leal	0x2(%rcx), %edx
 534c024:      	movl	%edx, 0x8(%r15,%rax)
 534c029:      	leaq	0xc(%rax), %rdx
 534c02d:      	cmpl	$0x4, %r13d
 534c031:      	jb	0x534c088 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x188>
 534c033:      	leal	0x3(%rcx), %esi
 534c036:      	movl	%esi, 0xc(%r15,%rax)
 534c03b:      	leaq	0x10(%rax), %rsi
 534c03f:      	cmpl	$0x4, %r13d
 534c043:      	je	0x534bf9e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x9e>
 534c049:      	leal	0x4(%rcx), %edx
 534c04c:      	movl	%edx, 0x10(%r15,%rax)
 534c051:      	leaq	0x14(%rax), %rdx
 534c055:      	cmpl	$0x6, %r13d
 534c059:      	jb	0x534c088 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x188>
 534c05b:      	leal	0x5(%rcx), %esi
 534c05e:      	movl	%esi, 0x14(%r15,%rax)
 534c063:      	leaq	0x18(%rax), %rsi
 534c067:      	cmpl	$0x7, %r13d
 534c06b:      	jne	0x534bf9e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x9e>
 534c071:      	addl	$0x6, %ecx
 534c074:      	movl	%ecx, 0x18(%r15,%rax)
 534c079:      	addq	$0x1c, %rax
 534c07d:      	movq	%rsi, %rbp
 534c080:      	jmp	0x534c08e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534c082:      	leaq	-0x4(%rax), %rbp
 534c086:      	jmp	0x534c08e <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x18e>
 534c088:      	movq	%rsi, %rbp
 534c08b:      	movq	%rdx, %rax
 534c08e:      	leaq	(%r15,%rax), %rbx
 534c092:      	movq	0x8(%rsp), %rcx
 534c097:      	movq	%rbx, 0x8(%rcx)
 534c09b:      	shrq	$0x2, %rax
 534c09f:      	bsrq	%rax, %rdx
 534c0a3:      	xorl	$0x3f, %edx
 534c0a6:      	addl	%edx, %edx
 534c0a8:      	xorq	$0x7e, %rdx
 534c0ac:      	leaq	0x18(%rsp), %rcx
 534c0b1:      	movq	%r15, %rdi
 534c0b4:      	movq	%rbx, %rsi
 534c0b7:      	callq	0x5355620 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEElNS0_5__ops15_Iter_comp_iterIZN4llvm3lto23generateModulesOrderingENS9_8ArrayRefIPNS9_13BitcodeModuleEEEE3$_0EEEvT_SH_T0_T1_>
 534c0bc:      	leaq	0x4(%r15), %r8
 534c0c0:      	cmpq	$0x40, %rbp
 534c0c4:      	jb	0x534c0dc <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x1dc>
 534c0c6:      	movq	%rbx, 0x10(%rsp)
 534c0cb:      	leaq	0x4(%r15), %rbx
 534c0cf:      	movl	$0x4, %ebp
 534c0d4:      	movq	%r15, %rdi
 534c0d7:      	jmp	0x534c1a8 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x2a8>
 534c0dc:      	testq	%rbp, %rbp
 534c0df:      	je	0x534c286 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c0e5:      	addq	%r15, %rbp
 534c0e8:      	movq	%r15, %r12
 534c0eb:      	jmp	0x534c129 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x229>
 534c0ed:      	nopl	(%rax)
 534c0f0:      	movq	%r12, %rdx
 534c0f3:      	subq	%r15, %rdx
 534c0f6:      	movq	%rdx, %rax
 534c0f9:      	sarq	$0x2, %rax
 534c0fd:      	cmpq	$0x2, %rax
 534c101:      	jl	0x534c176 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x276>
 534c103:      	shlq	$0x2, %rax
 534c107:      	subq	%rax, %rdi
 534c10a:      	addq	$0x8, %rdi
 534c10e:      	movq	%r15, %rsi
 534c111:      	callq	0x828abc0 <memmove@plt>
 534c116:      	movq	%r15, %rcx
 534c119:      	movl	%ebx, (%rcx)
 534c11b:      	leaq	0x4(%r12), %r8
 534c120:      	cmpq	%rbp, %r12
 534c123:      	je	0x534c286 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c129:      	movq	%r12, %rdi
 534c12c:      	movq	%r8, %r12
 534c12f:      	movslq	(%r8), %rbx
 534c132:      	movslq	(%r15), %rsi
 534c135:      	movq	(%r14,%rbx,8), %rax
 534c139:      	movq	0x8(%rax), %rax
 534c13d:      	movq	(%r14,%rsi,8), %rcx
 534c141:      	cmpq	0x8(%rcx), %rax
 534c145:      	ja	0x534c0f0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x1f0>
 534c147:      	movslq	(%rdi), %rdx
 534c14a:      	movq	(%r14,%rdx,8), %rsi
 534c14e:      	movq	%r12, %rcx
 534c151:      	cmpq	0x8(%rsi), %rax
 534c155:      	jbe	0x534c119 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c157:      	movq	%r12, %rcx
 534c15a:      	nopw	(%rax,%rax)
 534c160:      	movl	%edx, (%rcx)
 534c162:      	movslq	-0x8(%rcx), %rdx
 534c166:      	movq	(%r14,%rdx,8), %rsi
 534c16a:      	addq	$-0x4, %rcx
 534c16e:      	cmpq	0x8(%rsi), %rax
 534c172:      	ja	0x534c160 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x260>
 534c174:      	jmp	0x534c119 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c176:      	movq	%r15, %rcx
 534c179:      	cmpq	$0x4, %rdx
 534c17d:      	jne	0x534c119 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x219>
 534c17f:      	movl	%esi, 0x4(%rdi)
 534c182:      	jmp	0x534c116 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x216>
 534c184:      	movl	%edx, 0x4(%rcx)
 534c187:      	nopw	(%rax,%rax)
 534c190:      	movq	%r15, %rcx
 534c193:      	movl	%r13d, (%rcx)
 534c196:      	addq	$0x4, %rbp
 534c19a:      	addq	$0x4, %rbx
 534c19e:      	cmpq	$0x40, %rbp
 534c1a2:      	je	0x534c229 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x329>
 534c1a8:      	movq	%rdi, %rcx
 534c1ab:      	leaq	(%r15,%rbp), %rdi
 534c1af:      	movslq	(%r15,%rbp), %r13
 534c1b3:      	movslq	(%r15), %rdx
 534c1b6:      	movq	(%r14,%r13,8), %rax
 534c1ba:      	movq	0x8(%rax), %rax
 534c1be:      	movq	(%r14,%rdx,8), %rsi
 534c1c2:      	cmpq	0x8(%rsi), %rax
 534c1c6:      	jbe	0x534c1f0 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x2f0>
 534c1c8:      	cmpq	$0x5, %rbp
 534c1cc:      	jb	0x534c184 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x284>
 534c1ce:      	movq	%r8, %rdi
 534c1d1:      	movq	%r15, %rsi
 534c1d4:      	movq	%rbp, %rdx
 534c1d7:      	movq	%r8, %r12
 534c1da:      	callq	0x828abc0 <memmove@plt>
 534c1df:      	leaq	(%r15,%rbp), %rdi
 534c1e3:      	movq	%r12, %r8
 534c1e6:      	jmp	0x534c190 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x290>
 534c1e8:      	nopl	(%rax,%rax)
 534c1f0:      	movslq	(%rcx), %rdx
 534c1f3:      	movq	(%r14,%rdx,8), %rsi
 534c1f7:      	movq	%rdi, %rcx
 534c1fa:      	cmpq	0x8(%rsi), %rax
 534c1fe:      	jbe	0x534c193 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x293>
 534c200:      	movq	%rbx, %rcx
 534c203:      	nopw	%cs:(%rax,%rax)
 534c20d:      	nopl	(%rax)
 534c210:      	movl	%edx, (%rcx)
 534c212:      	movslq	-0x8(%rcx), %rdx
 534c216:      	movq	(%r14,%rdx,8), %rsi
 534c21a:      	addq	$-0x4, %rcx
 534c21e:      	cmpq	0x8(%rsi), %rax
 534c222:      	ja	0x534c210 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x310>
 534c224:      	jmp	0x534c193 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x293>
 534c229:      	addq	$0x40, %r15
 534c22d:      	movq	0x10(%rsp), %r8
 534c232:      	jmp	0x534c24b <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x34b>
 534c234:      	nopw	%cs:(%rax,%rax)
 534c23e:      	nop
 534c240:      	movl	%eax, (%rsi)
 534c242:      	addq	$0x4, %r15
 534c246:      	cmpq	%r8, %r15
 534c249:      	je	0x534c286 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x386>
 534c24b:      	movslq	(%r15), %rax
 534c24e:      	movq	(%r14,%rax,8), %rcx
 534c252:      	movq	0x8(%rcx), %rcx
 534c256:      	movslq	-0x4(%r15), %rdx
 534c25a:      	movq	(%r14,%rdx,8), %rdi
 534c25e:      	movq	%r15, %rsi
 534c261:      	cmpq	0x8(%rdi), %rcx
 534c265:      	jbe	0x534c240 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x340>
 534c267:      	movq	%r15, %rsi
 534c26a:      	nopw	(%rax,%rax)
 534c270:      	movl	%edx, (%rsi)
 534c272:      	movslq	-0x8(%rsi), %rdx
 534c276:      	movq	(%r14,%rdx,8), %rdi
 534c27a:      	addq	$-0x4, %rsi
 534c27e:      	cmpq	0x8(%rdi), %rcx
 534c282:      	ja	0x534c270 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x370>
 534c284:      	jmp	0x534c240 <_ZN4llvm3lto23generateModulesOrderingENS_8ArrayRefIPNS_13BitcodeModuleEEE+0x340>
 534c286:      	movq	0x8(%rsp), %rax
 534c28b:      	addq	$0x28, %rsp
 534c28f:      	popq	%rbx
 534c290:      	popq	%r12
 534c292:      	popq	%r13
 534c294:      	popq	%r14
 534c296:      	popq	%r15
 534c298:      	popq	%rbp
 534c299:      	retq
 534c29a:      	leaq	-0x455740f(%rip), %rdi  # 0xdf4e92 <.str.51.llvm.11973330662442186590>
 534c2a1:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
