
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000811edb0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE>:
 811edb0:      	pushq	%rbp
 811edb1:      	pushq	%r15
 811edb3:      	pushq	%r14
 811edb5:      	pushq	%r13
 811edb7:      	pushq	%r12
 811edb9:      	pushq	%rbx
 811edba:      	subq	$0x28, %rsp
 811edbe:      	movq	%rsi, %r12
 811edc1:      	movq	%rdi, %rbx
 811edc4:      	movq	%rdx, 0x30(%rsi)
 811edc8:      	movups	(%rcx), %xmm0
 811edcb:      	movups	%xmm0, 0x20(%rsi)
 811edcf:      	movq	0x20(%rsi), %rdx
 811edd3:      	movq	0x28(%rsi), %rsi
 811edd7:      	movq	(%rsi), %rax
 811edda:      	leaq	0x10(%rsp), %rdi
 811eddf:      	callq	*0xb0(%rax)
 811ede5:      	testb	$0x1, 0x20(%rsp)
 811edea:      	je	0x811edf6 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x46>
 811edec:      	movq	0x10(%rsp), %r12
 811edf1:      	jmp	0x811f15a <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3aa>
 811edf6:      	movq	%rbx, (%rsp)
 811edfa:      	movups	0x10(%rsp), %xmm0
 811edff:      	movl	$0x1, 0x8(%r12)
 811ee08:      	movups	%xmm0, 0x10(%r12)
 811ee0e:      	movq	0x20(%r12), %rsi
 811ee13:      	movq	0x30(%r12), %rdi
 811ee18:      	callq	0x811be90 <_ZNK4llvm6object14COFFObjectFile14getRelocationsEPKNS0_12coff_sectionE>
 811ee1d:      	movq	%rax, %r13
 811ee20:      	movq	%rdx, %rbp
 811ee23:      	movq	0x38(%r12), %r15
 811ee28:      	movq	0x48(%r12), %r14
 811ee2d:      	movq	%r14, %rdx
 811ee30:      	subq	%r15, %rdx
 811ee33:      	movq	%rdx, %rax
 811ee36:      	sarq	$0x3, %rax
 811ee3a:      	cmpq	%rbp, %rax
 811ee3d:      	movq	%r12, %rcx
 811ee40:      	movq	%r12, 0x8(%rsp)
 811ee45:      	jae	0x811eea7 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xf7>
 811ee47:      	movq	%rdx, %r12
 811ee4a:      	movq	0x40(%rcx), %rbx
 811ee4e:      	subq	%r15, %rbx
 811ee51:      	leaq	(,%rbp,8), %rdi
 811ee59:      	callq	0x828a620 <_Znwm@plt>
 811ee5e:      	testq	%rbx, %rbx
 811ee61:      	jle	0x811ee77 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xc7>
 811ee63:      	movq	%rax, %r14
 811ee66:      	movq	%rax, %rdi
 811ee69:      	movq	%r15, %rsi
 811ee6c:      	movq	%rbx, %rdx
 811ee6f:      	callq	0x828ac50 <memcpy@plt>
 811ee74:      	movq	%r14, %rax
 811ee77:      	testq	%r15, %r15
 811ee7a:      	je	0x811ee8d <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xdd>
 811ee7c:      	movq	%rax, %r14
 811ee7f:      	movq	%r15, %rdi
 811ee82:      	movq	%r12, %rsi
 811ee85:      	callq	0x828a660 <_ZdlPvm@plt>
 811ee8a:      	movq	%r14, %rax
 811ee8d:      	movq	0x8(%rsp), %rcx
 811ee92:      	movq	%rax, 0x38(%rcx)
 811ee96:      	addq	%rax, %rbx
 811ee99:      	movq	%rbx, 0x40(%rcx)
 811ee9d:      	leaq	(%rax,%rbp,8), %r14
 811eea1:      	movq	%r14, 0x48(%rcx)
 811eea5:      	jmp	0x811eeb7 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x107>
 811eea7:      	movq	0x40(%rcx), %rbx
 811eeab:      	movq	%r15, %rax
 811eeae:      	testq	%rbp, %rbp
 811eeb1:      	je	0x811efa1 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1f1>
 811eeb7:      	addq	%rbp, %rbp
 811eeba:      	leaq	(%rbp,%rbp,4), %r12
 811eebf:      	movabsq	$0xfffffffffffffff, %rbp # imm = 0xFFFFFFFFFFFFFFF
 811eec9:      	jmp	0x811eeec <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x13c>
 811eecb:      	nopl	(%rax,%rax)
 811eed0:      	movq	%r13, (%rbx)
 811eed3:      	addq	$0x8, %rbx
 811eed7:      	movq	%rbx, 0x40(%rcx)
 811eedb:      	movq	%rax, %r15
 811eede:      	addq	$0xa, %r13
 811eee2:      	addq	$-0xa, %r12
 811eee6:      	je	0x811efa1 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1f1>
 811eeec:      	cmpq	%r14, %rbx
 811eeef:      	jne	0x811eed0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x120>
 811eef1:      	subq	%rax, %r14
 811eef4:      	movabsq	$0x7ffffffffffffff8, %rcx # imm = 0x7FFFFFFFFFFFFFF8
 811eefe:      	cmpq	%rcx, %r14
 811ef01:      	je	0x811f16f <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3bf>
 811ef07:      	movq	%r14, %rsi
 811ef0a:      	sarq	$0x3, %rsi
 811ef0e:      	cmpq	$0x1, %rsi
 811ef12:      	movq	%rsi, %rcx
 811ef15:      	adcq	$0x0, %rcx
 811ef19:      	leaq	(%rcx,%rsi), %rdx
 811ef1d:      	cmpq	%rbp, %rdx
 811ef20:      	jb	0x811ef25 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x175>
 811ef22:      	movq	%rbp, %rdx
 811ef25:      	movq	%rax, %rbx
 811ef28:      	addq	%rsi, %rcx
 811ef2b:      	jb	0x811ef30 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x180>
 811ef2d:      	movq	%rdx, %rbp
 811ef30:      	leaq	(,%rbp,8), %rdi
 811ef38:      	callq	0x828a620 <_Znwm@plt>
 811ef3d:      	movq	%rax, %r15
 811ef40:      	movq	%r13, (%rax,%r14)
 811ef44:      	testq	%r14, %r14
 811ef47:      	jle	0x811ef57 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1a7>
 811ef49:      	movq	%r15, %rdi
 811ef4c:      	movq	%rbx, %rsi
 811ef4f:      	movq	%r14, %rdx
 811ef52:      	callq	0x828ac50 <memcpy@plt>
 811ef57:      	testq	%rbx, %rbx
 811ef5a:      	je	0x811ef67 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1b7>
 811ef5c:      	movq	%rbx, %rdi
 811ef5f:      	movq	%r14, %rsi
 811ef62:      	callq	0x828a660 <_ZdlPvm@plt>
 811ef67:      	addq	%r15, %r14
 811ef6a:      	movq	%r14, %rbx
 811ef6d:      	addq	$0x8, %rbx
 811ef71:      	movq	0x8(%rsp), %rcx
 811ef76:      	movq	%r15, 0x38(%rcx)
 811ef7a:      	movq	%rbx, 0x40(%rcx)
 811ef7e:      	leaq	(%r15,%rbp,8), %r14
 811ef82:      	movq	%r14, 0x48(%rcx)
 811ef86:      	movq	%r15, %rax
 811ef89:      	movabsq	$0xfffffffffffffff, %rbp # imm = 0xFFFFFFFFFFFFFFF
 811ef93:      	addq	$0xa, %r13
 811ef97:      	addq	$-0xa, %r12
 811ef9b:      	jne	0x811eeec <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x13c>
 811efa1:      	cmpq	%rbx, %r15
 811efa4:      	je	0x811f153 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811efaa:      	movq	%rbx, %r12
 811efad:      	subq	%r15, %r12
 811efb0:      	movq	%r12, %rax
 811efb3:      	sarq	$0x3, %rax
 811efb7:      	bsrq	%rax, %rdx
 811efbb:      	xorl	$0x3f, %edx
 811efbe:      	addl	%edx, %edx
 811efc0:      	xorq	$0x7e, %rdx
 811efc4:      	movq	%r15, %rdi
 811efc7:      	movq	%rbx, %rsi
 811efca:      	callq	0x811fad0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN4llvm6object15coff_relocationESt6vectorIS6_SaIS6_EEEElNS0_5__ops15_Iter_comp_iterIZNS3_18ResourceSectionRef4loadEPKNS3_14COFFObjectFileERKNS3_10SectionRefEE3$_0EEEvT_SN_T0_T1_>
 811efcf:      	leaq	0x8(%r15), %r14
 811efd3:      	cmpq	$0x81, %r12
 811efda:      	jl	0x811efee <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x23e>
 811efdc:      	leaq	0x8(%r15), %r13
 811efe0:      	movl	$0x8, %r12d
 811efe6:      	movq	%r15, %rsi
 811efe9:      	jmp	0x811f0a7 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2f7>
 811efee:      	cmpq	%rbx, %r14
 811eff1:      	je	0x811f153 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811eff7:      	xorl	%r12d, %r12d
 811effa:      	movq	%r15, %r13
 811effd:      	jmp	0x811f039 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x289>
 811efff:      	nop
 811f000:      	movq	%r13, %rdx
 811f003:      	subq	%r15, %rdx
 811f006:      	movq	%rdx, %rax
 811f009:      	sarq	$0x3, %rax
 811f00d:      	cmpq	$0x2, %rax
 811f011:      	jl	0x811f074 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2c4>
 811f013:      	shlq	$0x3, %rax
 811f017:      	subq	%rax, %rdi
 811f01a:      	addq	$0x10, %rdi
 811f01e:      	movq	%r15, %rsi
 811f021:      	callq	0x828abc0 <memmove@plt>
 811f026:      	movq	%r15, %rax
 811f029:      	movq	%r14, (%rax)
 811f02c:      	leaq	0x8(%r13), %r14
 811f030:      	cmpq	%rbx, %r14
 811f033:      	je	0x811f156 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a6>
 811f039:      	movq	%r13, %rdi
 811f03c:      	movq	%r14, %r13
 811f03f:      	movq	(%r14), %r14
 811f042:      	movq	(%r15), %rcx
 811f045:      	movl	(%r14), %edx
 811f048:      	cmpl	(%rcx), %edx
 811f04a:      	jb	0x811f000 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x250>
 811f04c:      	movq	(%rdi), %rcx
 811f04f:      	movq	%r13, %rax
 811f052:      	cmpl	(%rcx), %edx
 811f054:      	jae	0x811f029 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f056:      	movq	%r13, %rax
 811f059:      	nopl	(%rax)
 811f060:      	movq	%rcx, (%rax)
 811f063:      	movl	(%r14), %edx
 811f066:      	movq	-0x10(%rax), %rcx
 811f06a:      	addq	$-0x8, %rax
 811f06e:      	cmpl	(%rcx), %edx
 811f070:      	jb	0x811f060 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2b0>
 811f072:      	jmp	0x811f029 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f074:      	movq	%r15, %rax
 811f077:      	cmpq	$0x8, %rdx
 811f07b:      	jne	0x811f029 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f07d:      	movq	%rcx, 0x8(%rdi)
 811f081:      	jmp	0x811f026 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x276>
 811f083:      	movq	%rcx, 0x8(%rax)
 811f087:      	nopw	(%rax,%rax)
 811f090:      	movq	%r15, %rax
 811f093:      	movq	%rbp, (%rax)
 811f096:      	addq	$0x8, %r12
 811f09a:      	addq	$0x8, %r13
 811f09e:      	cmpq	$0x80, %r12
 811f0a5:      	je	0x811f104 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x354>
 811f0a7:      	movq	%rsi, %rax
 811f0aa:      	leaq	(%r15,%r12), %rsi
 811f0ae:      	movq	(%r15,%r12), %rbp
 811f0b2:      	movq	(%r15), %rcx
 811f0b5:      	movl	(%rbp), %edx
 811f0b8:      	cmpl	(%rcx), %edx
 811f0ba:      	jae	0x811f0e0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x330>
 811f0bc:      	cmpq	$0x9, %r12
 811f0c0:      	jb	0x811f083 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2d3>
 811f0c2:      	movq	%r14, %rdi
 811f0c5:      	movq	%r15, %rsi
 811f0c8:      	movq	%r12, %rdx
 811f0cb:      	callq	0x828abc0 <memmove@plt>
 811f0d0:      	leaq	(%r15,%r12), %rsi
 811f0d4:      	jmp	0x811f090 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e0>
 811f0d6:      	nopw	%cs:(%rax,%rax)
 811f0e0:      	movq	(%rax), %rcx
 811f0e3:      	movq	%rsi, %rax
 811f0e6:      	cmpl	(%rcx), %edx
 811f0e8:      	jae	0x811f093 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e3>
 811f0ea:      	movq	%r13, %rax
 811f0ed:      	nopl	(%rax)
 811f0f0:      	movq	%rcx, (%rax)
 811f0f3:      	movl	(%rbp), %edx
 811f0f6:      	movq	-0x10(%rax), %rcx
 811f0fa:      	addq	$-0x8, %rax
 811f0fe:      	cmpl	(%rcx), %edx
 811f100:      	jb	0x811f0f0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x340>
 811f102:      	jmp	0x811f093 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e3>
 811f104:      	subq	$-0x80, %r15
 811f108:      	cmpq	%rbx, %r15
 811f10b:      	je	0x811f153 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811f10d:      	xorl	%r12d, %r12d
 811f110:      	jmp	0x811f12c <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x37c>
 811f112:      	nopw	%cs:(%rax,%rax)
 811f11c:      	nopl	(%rax)
 811f120:      	movq	%rax, (%rdx)
 811f123:      	addq	$0x8, %r15
 811f127:      	cmpq	%rbx, %r15
 811f12a:      	je	0x811f156 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a6>
 811f12c:      	movq	-0x8(%r15), %rcx
 811f130:      	movq	(%r15), %rax
 811f133:      	movl	(%rax), %esi
 811f135:      	movq	%r15, %rdx
 811f138:      	cmpl	(%rcx), %esi
 811f13a:      	jae	0x811f120 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x370>
 811f13c:      	movq	%r15, %rdx
 811f13f:      	nop
 811f140:      	movq	%rcx, (%rdx)
 811f143:      	movl	(%rax), %esi
 811f145:      	movq	-0x10(%rdx), %rcx
 811f149:      	addq	$-0x8, %rdx
 811f14d:      	cmpl	(%rcx), %esi
 811f14f:      	jb	0x811f140 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x390>
 811f151:      	jmp	0x811f120 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x370>
 811f153:      	xorl	%r12d, %r12d
 811f156:      	movq	(%rsp), %rbx
 811f15a:      	movq	%r12, (%rbx)
 811f15d:      	movq	%rbx, %rax
 811f160:      	addq	$0x28, %rsp
 811f164:      	popq	%rbx
 811f165:      	popq	%r12
 811f167:      	popq	%r13
 811f169:      	popq	%r14
 811f16b:      	popq	%r15
 811f16d:      	popq	%rbp
 811f16e:      	retq
 811f16f:      	leaq	-0x748478c(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 811f176:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
