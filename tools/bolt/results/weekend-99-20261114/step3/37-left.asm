
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

000000000811ee40 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE>:
 811ee40:      	pushq	%rbp
 811ee41:      	pushq	%r15
 811ee43:      	pushq	%r14
 811ee45:      	pushq	%r13
 811ee47:      	pushq	%r12
 811ee49:      	pushq	%rbx
 811ee4a:      	subq	$0x28, %rsp
 811ee4e:      	movq	%rsi, %r12
 811ee51:      	movq	%rdi, %rbx
 811ee54:      	movq	%rdx, 0x30(%rsi)
 811ee58:      	movups	(%rcx), %xmm0
 811ee5b:      	movups	%xmm0, 0x20(%rsi)
 811ee5f:      	movq	0x20(%rsi), %rdx
 811ee63:      	movq	0x28(%rsi), %rsi
 811ee67:      	movq	(%rsi), %rax
 811ee6a:      	leaq	0x10(%rsp), %rdi
 811ee6f:      	callq	*0xb0(%rax)
 811ee75:      	testb	$0x1, 0x20(%rsp)
 811ee7a:      	je	0x811ee86 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x46>
 811ee7c:      	movq	0x10(%rsp), %r12
 811ee81:      	jmp	0x811f1ea <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3aa>
 811ee86:      	movq	%rbx, (%rsp)
 811ee8a:      	movups	0x10(%rsp), %xmm0
 811ee8f:      	movl	$0x1, 0x8(%r12)
 811ee98:      	movups	%xmm0, 0x10(%r12)
 811ee9e:      	movq	0x20(%r12), %rsi
 811eea3:      	movq	0x30(%r12), %rdi
 811eea8:      	callq	0x811bf20 <_ZNK4llvm6object14COFFObjectFile14getRelocationsEPKNS0_12coff_sectionE>
 811eead:      	movq	%rax, %r13
 811eeb0:      	movq	%rdx, %rbp
 811eeb3:      	movq	0x38(%r12), %r15
 811eeb8:      	movq	0x48(%r12), %r14
 811eebd:      	movq	%r14, %rdx
 811eec0:      	subq	%r15, %rdx
 811eec3:      	movq	%rdx, %rax
 811eec6:      	sarq	$0x3, %rax
 811eeca:      	cmpq	%rbp, %rax
 811eecd:      	movq	%r12, %rcx
 811eed0:      	movq	%r12, 0x8(%rsp)
 811eed5:      	jae	0x811ef37 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xf7>
 811eed7:      	movq	%rdx, %r12
 811eeda:      	movq	0x40(%rcx), %rbx
 811eede:      	subq	%r15, %rbx
 811eee1:      	leaq	(,%rbp,8), %rdi
 811eee9:      	callq	0x828a6b0 <_Znwm@plt>
 811eeee:      	testq	%rbx, %rbx
 811eef1:      	jle	0x811ef07 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xc7>
 811eef3:      	movq	%rax, %r14
 811eef6:      	movq	%rax, %rdi
 811eef9:      	movq	%r15, %rsi
 811eefc:      	movq	%rbx, %rdx
 811eeff:      	callq	0x828ace0 <memcpy@plt>
 811ef04:      	movq	%r14, %rax
 811ef07:      	testq	%r15, %r15
 811ef0a:      	je	0x811ef1d <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0xdd>
 811ef0c:      	movq	%rax, %r14
 811ef0f:      	movq	%r15, %rdi
 811ef12:      	movq	%r12, %rsi
 811ef15:      	callq	0x828a6f0 <_ZdlPvm@plt>
 811ef1a:      	movq	%r14, %rax
 811ef1d:      	movq	0x8(%rsp), %rcx
 811ef22:      	movq	%rax, 0x38(%rcx)
 811ef26:      	addq	%rax, %rbx
 811ef29:      	movq	%rbx, 0x40(%rcx)
 811ef2d:      	leaq	(%rax,%rbp,8), %r14
 811ef31:      	movq	%r14, 0x48(%rcx)
 811ef35:      	jmp	0x811ef47 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x107>
 811ef37:      	movq	0x40(%rcx), %rbx
 811ef3b:      	movq	%r15, %rax
 811ef3e:      	testq	%rbp, %rbp
 811ef41:      	je	0x811f031 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1f1>
 811ef47:      	addq	%rbp, %rbp
 811ef4a:      	leaq	(%rbp,%rbp,4), %r12
 811ef4f:      	movabsq	$0xfffffffffffffff, %rbp # imm = 0xFFFFFFFFFFFFFFF
 811ef59:      	jmp	0x811ef7c <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x13c>
 811ef5b:      	nopl	(%rax,%rax)
 811ef60:      	movq	%r13, (%rbx)
 811ef63:      	addq	$0x8, %rbx
 811ef67:      	movq	%rbx, 0x40(%rcx)
 811ef6b:      	movq	%rax, %r15
 811ef6e:      	addq	$0xa, %r13
 811ef72:      	addq	$-0xa, %r12
 811ef76:      	je	0x811f031 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1f1>
 811ef7c:      	cmpq	%r14, %rbx
 811ef7f:      	jne	0x811ef60 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x120>
 811ef81:      	subq	%rax, %r14
 811ef84:      	movabsq	$0x7ffffffffffffff8, %rcx # imm = 0x7FFFFFFFFFFFFFF8
 811ef8e:      	cmpq	%rcx, %r14
 811ef91:      	je	0x811f1ff <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3bf>
 811ef97:      	movq	%r14, %rsi
 811ef9a:      	sarq	$0x3, %rsi
 811ef9e:      	cmpq	$0x1, %rsi
 811efa2:      	movq	%rsi, %rcx
 811efa5:      	adcq	$0x0, %rcx
 811efa9:      	leaq	(%rcx,%rsi), %rdx
 811efad:      	cmpq	%rbp, %rdx
 811efb0:      	jb	0x811efb5 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x175>
 811efb2:      	movq	%rbp, %rdx
 811efb5:      	movq	%rax, %rbx
 811efb8:      	addq	%rsi, %rcx
 811efbb:      	jb	0x811efc0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x180>
 811efbd:      	movq	%rdx, %rbp
 811efc0:      	leaq	(,%rbp,8), %rdi
 811efc8:      	callq	0x828a6b0 <_Znwm@plt>
 811efcd:      	movq	%rax, %r15
 811efd0:      	movq	%r13, (%rax,%r14)
 811efd4:      	testq	%r14, %r14
 811efd7:      	jle	0x811efe7 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1a7>
 811efd9:      	movq	%r15, %rdi
 811efdc:      	movq	%rbx, %rsi
 811efdf:      	movq	%r14, %rdx
 811efe2:      	callq	0x828ace0 <memcpy@plt>
 811efe7:      	testq	%rbx, %rbx
 811efea:      	je	0x811eff7 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x1b7>
 811efec:      	movq	%rbx, %rdi
 811efef:      	movq	%r14, %rsi
 811eff2:      	callq	0x828a6f0 <_ZdlPvm@plt>
 811eff7:      	addq	%r15, %r14
 811effa:      	movq	%r14, %rbx
 811effd:      	addq	$0x8, %rbx
 811f001:      	movq	0x8(%rsp), %rcx
 811f006:      	movq	%r15, 0x38(%rcx)
 811f00a:      	movq	%rbx, 0x40(%rcx)
 811f00e:      	leaq	(%r15,%rbp,8), %r14
 811f012:      	movq	%r14, 0x48(%rcx)
 811f016:      	movq	%r15, %rax
 811f019:      	movabsq	$0xfffffffffffffff, %rbp # imm = 0xFFFFFFFFFFFFFFF
 811f023:      	addq	$0xa, %r13
 811f027:      	addq	$-0xa, %r12
 811f02b:      	jne	0x811ef7c <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x13c>
 811f031:      	cmpq	%rbx, %r15
 811f034:      	je	0x811f1e3 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811f03a:      	movq	%rbx, %r12
 811f03d:      	subq	%r15, %r12
 811f040:      	movq	%r12, %rax
 811f043:      	sarq	$0x3, %rax
 811f047:      	bsrq	%rax, %rdx
 811f04b:      	xorl	$0x3f, %edx
 811f04e:      	addl	%edx, %edx
 811f050:      	xorq	$0x7e, %rdx
 811f054:      	movq	%r15, %rdi
 811f057:      	movq	%rbx, %rsi
 811f05a:      	callq	0x811fb60 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPPKN4llvm6object15coff_relocationESt6vectorIS6_SaIS6_EEEElNS0_5__ops15_Iter_comp_iterIZNS3_18ResourceSectionRef4loadEPKNS3_14COFFObjectFileERKNS3_10SectionRefEE3$_0EEEvT_SN_T0_T1_>
 811f05f:      	leaq	0x8(%r15), %r14
 811f063:      	cmpq	$0x81, %r12
 811f06a:      	jl	0x811f07d <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x23d>
 811f06c:      	movl	$0x8, %r12d
 811f072:      	movq	%r14, %r13
 811f075:      	movq	%r15, %rsi
 811f078:      	jmp	0x811f137 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2f7>
 811f07d:      	cmpq	%rbx, %r14
 811f080:      	je	0x811f1e3 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811f086:      	xorl	%r12d, %r12d
 811f089:      	movq	%r15, %r13
 811f08c:      	jmp	0x811f0c9 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x289>
 811f08e:      	nop
 811f090:      	movq	%r13, %rdx
 811f093:      	subq	%r15, %rdx
 811f096:      	movq	%rdx, %rax
 811f099:      	sarq	$0x3, %rax
 811f09d:      	cmpq	$0x2, %rax
 811f0a1:      	jl	0x811f104 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2c4>
 811f0a3:      	shlq	$0x3, %rax
 811f0a7:      	subq	%rax, %rdi
 811f0aa:      	addq	$0x10, %rdi
 811f0ae:      	movq	%r15, %rsi
 811f0b1:      	callq	0x828ac50 <memmove@plt>
 811f0b6:      	movq	%r15, %rax
 811f0b9:      	movq	%r14, (%rax)
 811f0bc:      	leaq	0x8(%r13), %r14
 811f0c0:      	cmpq	%rbx, %r14
 811f0c3:      	je	0x811f1e6 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a6>
 811f0c9:      	movq	%r13, %rdi
 811f0cc:      	movq	%r14, %r13
 811f0cf:      	movq	(%r14), %r14
 811f0d2:      	movq	(%r15), %rcx
 811f0d5:      	movl	(%r14), %edx
 811f0d8:      	cmpl	(%rcx), %edx
 811f0da:      	jb	0x811f090 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x250>
 811f0dc:      	movq	(%rdi), %rcx
 811f0df:      	movq	%r13, %rax
 811f0e2:      	cmpl	(%rcx), %edx
 811f0e4:      	jae	0x811f0b9 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f0e6:      	movq	%r13, %rax
 811f0e9:      	nopl	(%rax)
 811f0f0:      	movq	%rcx, (%rax)
 811f0f3:      	movl	(%r14), %edx
 811f0f6:      	movq	-0x10(%rax), %rcx
 811f0fa:      	addq	$-0x8, %rax
 811f0fe:      	cmpl	(%rcx), %edx
 811f100:      	jb	0x811f0f0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2b0>
 811f102:      	jmp	0x811f0b9 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f104:      	movq	%r15, %rax
 811f107:      	cmpq	$0x8, %rdx
 811f10b:      	jne	0x811f0b9 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x279>
 811f10d:      	movq	%rcx, 0x8(%rdi)
 811f111:      	jmp	0x811f0b6 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x276>
 811f113:      	movq	%rcx, 0x8(%rax)
 811f117:      	nopw	(%rax,%rax)
 811f120:      	movq	%r15, %rax
 811f123:      	movq	%rbp, (%rax)
 811f126:      	addq	$0x8, %r12
 811f12a:      	addq	$0x8, %r13
 811f12e:      	cmpq	$0x80, %r12
 811f135:      	je	0x811f194 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x354>
 811f137:      	movq	%rsi, %rax
 811f13a:      	leaq	(%r15,%r12), %rsi
 811f13e:      	movq	(%r15,%r12), %rbp
 811f142:      	movq	(%r15), %rcx
 811f145:      	movl	(%rbp), %edx
 811f148:      	cmpl	(%rcx), %edx
 811f14a:      	jae	0x811f170 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x330>
 811f14c:      	cmpq	$0x9, %r12
 811f150:      	jb	0x811f113 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2d3>
 811f152:      	movq	%r14, %rdi
 811f155:      	movq	%r15, %rsi
 811f158:      	movq	%r12, %rdx
 811f15b:      	callq	0x828ac50 <memmove@plt>
 811f160:      	leaq	(%r15,%r12), %rsi
 811f164:      	jmp	0x811f120 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e0>
 811f166:      	nopw	%cs:(%rax,%rax)
 811f170:      	movq	(%rax), %rcx
 811f173:      	movq	%rsi, %rax
 811f176:      	cmpl	(%rcx), %edx
 811f178:      	jae	0x811f123 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e3>
 811f17a:      	movq	%r13, %rax
 811f17d:      	nopl	(%rax)
 811f180:      	movq	%rcx, (%rax)
 811f183:      	movl	(%rbp), %edx
 811f186:      	movq	-0x10(%rax), %rcx
 811f18a:      	addq	$-0x8, %rax
 811f18e:      	cmpl	(%rcx), %edx
 811f190:      	jb	0x811f180 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x340>
 811f192:      	jmp	0x811f123 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x2e3>
 811f194:      	subq	$-0x80, %r15
 811f198:      	cmpq	%rbx, %r15
 811f19b:      	je	0x811f1e3 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a3>
 811f19d:      	xorl	%r12d, %r12d
 811f1a0:      	jmp	0x811f1bc <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x37c>
 811f1a2:      	nopw	%cs:(%rax,%rax)
 811f1ac:      	nopl	(%rax)
 811f1b0:      	movq	%rax, (%rdx)
 811f1b3:      	addq	$0x8, %r15
 811f1b7:      	cmpq	%rbx, %r15
 811f1ba:      	je	0x811f1e6 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x3a6>
 811f1bc:      	movq	-0x8(%r15), %rcx
 811f1c0:      	movq	(%r15), %rax
 811f1c3:      	movl	(%rax), %esi
 811f1c5:      	movq	%r15, %rdx
 811f1c8:      	cmpl	(%rcx), %esi
 811f1ca:      	jae	0x811f1b0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x370>
 811f1cc:      	movq	%r15, %rdx
 811f1cf:      	nop
 811f1d0:      	movq	%rcx, (%rdx)
 811f1d3:      	movl	(%rax), %esi
 811f1d5:      	movq	-0x10(%rdx), %rcx
 811f1d9:      	addq	$-0x8, %rdx
 811f1dd:      	cmpl	(%rcx), %esi
 811f1df:      	jb	0x811f1d0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x390>
 811f1e1:      	jmp	0x811f1b0 <_ZN4llvm6object18ResourceSectionRef4loadEPKNS0_14COFFObjectFileERKNS0_10SectionRefE+0x370>
 811f1e3:      	xorl	%r12d, %r12d
 811f1e6:      	movq	(%rsp), %rbx
 811f1ea:      	movq	%r12, (%rbx)
 811f1ed:      	movq	%rbx, %rax
 811f1f0:      	addq	$0x28, %rsp
 811f1f4:      	popq	%rbx
 811f1f5:      	popq	%r12
 811f1f7:      	popq	%r13
 811f1f9:      	popq	%r14
 811f1fb:      	popq	%r15
 811f1fd:      	popq	%rbp
 811f1fe:      	retq
 811f1ff:      	leaq	-0x748481c(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 811f206:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
