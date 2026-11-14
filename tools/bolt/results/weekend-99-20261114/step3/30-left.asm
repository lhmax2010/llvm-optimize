
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003e6b800 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb>:
 3e6b800:      	pushq	%rbp
 3e6b801:      	pushq	%r15
 3e6b803:      	pushq	%r14
 3e6b805:      	pushq	%r13
 3e6b807:      	pushq	%r12
 3e6b809:      	pushq	%rbx
 3e6b80a:      	subq	$0x68, %rsp
 3e6b80e:      	movq	%rsi, 0x128(%rdi)
 3e6b815:      	leaq	(%rsi,%rdx), %r13
 3e6b819:      	movq	%r13, 0x130(%rdi)
 3e6b820:      	testq	%rdx, %rdx
 3e6b823:      	je	0x3e6bce3 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4e3>
 3e6b829:      	movl	%ecx, %ebp
 3e6b82b:      	xorl	%eax, %eax
 3e6b82d:      	movq	%rsi, %rdx
 3e6b830:      	leaq	0x8(%rdx), %rcx
 3e6b834:      	cmpq	%r13, %rcx
 3e6b837:      	ja	0x3e6bcdb <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b83d:      	movq	%rcx, 0x128(%rdi)
 3e6b844:      	addq	$0x10, %rdx
 3e6b848:      	xorl	%r14d, %r14d
 3e6b84b:      	cmpq	%r13, %rdx
 3e6b84e:      	ja	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6b854:      	movq	%rdx, 0x128(%rdi)
 3e6b85b:      	xorl	%ebx, %ebx
 3e6b85d:      	movq	%rdx, %r8
 3e6b860:      	movzbl	(%r8), %r9d
 3e6b864:      	movl	%r9d, %r10d
 3e6b867:      	andl	$0x7f, %r10d
 3e6b86b:      	cmpl	$0x3f, %r14d
 3e6b86f:      	jae	0x3e6b888 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x88>
 3e6b871:      	movl	%r14d, %ecx
 3e6b874:      	shlq	%cl, %r10
 3e6b877:      	addq	%r10, %rbx
 3e6b87a:      	addl	$0x7, %r14d
 3e6b87e:      	incq	%r8
 3e6b881:      	testb	%r9b, %r9b
 3e6b884:      	js	0x3e6b860 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x60>
 3e6b886:      	jmp	0x3e6b8b0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0xb0>
 3e6b888:      	xorl	%ecx, %ecx
 3e6b88a:      	cmpb	$0x2, %r10b
 3e6b88e:      	setae	%cl
 3e6b891:      	xorl	%r11d, %r11d
 3e6b894:      	testb	%r10b, %r10b
 3e6b897:      	setne	%r11b
 3e6b89b:      	cmpl	$0x3f, %r14d
 3e6b89f:      	cmovel	%ecx, %r11d
 3e6b8a3:      	testb	%r11b, %r11b
 3e6b8a6:      	je	0x3e6b871 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x71>
 3e6b8a8:      	xorl	%ebx, %ebx
 3e6b8aa:      	jmp	0x3e6b8bd <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0xbd>
 3e6b8ac:      	nopl	(%rax)
 3e6b8b0:      	movq	%rbx, %rcx
 3e6b8b3:      	shrq	$0x20, %rcx
 3e6b8b7:      	jne	0x3e6bcdb <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b8bd:      	subl	%edx, %r8d
 3e6b8c0:      	addq	%rdx, %r8
 3e6b8c3:      	cmpq	%r13, %r8
 3e6b8c6:      	ja	0x3e6bcdb <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b8cc:      	movq	%r8, 0x128(%rdi)
 3e6b8d3:      	addq	%r8, %rbx
 3e6b8d6:      	cmpq	%r13, %rbx
 3e6b8d9:      	ja	0x3e6bcdb <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b8df:      	movq	%rbx, 0x128(%rdi)
 3e6b8e6:      	incl	%eax
 3e6b8e8:      	movq	%rbx, %rdx
 3e6b8eb:      	cmpq	%r13, %rbx
 3e6b8ee:      	jb	0x3e6b830 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x30>
 3e6b8f4:      	movl	%ebp, 0xc(%rsp)
 3e6b8f8:      	movl	%eax, %r14d
 3e6b8fb:      	movq	0x68(%rdi), %rbx
 3e6b8ff:      	movq	0x78(%rdi), %r15
 3e6b903:      	subq	%rbx, %r15
 3e6b906:      	movq	%r15, %rax
 3e6b909:      	sarq	$0x5, %rax
 3e6b90d:      	cmpq	%r14, %rax
 3e6b910:      	movq	%rdi, 0x50(%rsp)
 3e6b915:      	jae	0x3e6b98d <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x18d>
 3e6b917:      	movq	%rsi, 0x30(%rsp)
 3e6b91c:      	movq	0x70(%rdi), %rbp
 3e6b920:      	shlq	$0x5, %r14
 3e6b924:      	movq	%r14, %rdi
 3e6b927:      	callq	0x828a6b0 <_Znwm@plt>
 3e6b92c:      	movq	%rbp, %r12
 3e6b92f:      	subq	%rbx, %r12
 3e6b932:      	je	0x3e6b95b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x15b>
 3e6b934:      	movq	%rax, %rdx
 3e6b937:      	movq	%rbx, %rcx
 3e6b93a:      	nopw	(%rax,%rax)
 3e6b940:      	movups	(%rcx), %xmm0
 3e6b943:      	movups	0x10(%rcx), %xmm1
 3e6b947:      	movups	%xmm1, 0x10(%rdx)
 3e6b94b:      	movups	%xmm0, (%rdx)
 3e6b94e:      	addq	$0x20, %rcx
 3e6b952:      	addq	$0x20, %rdx
 3e6b956:      	cmpq	%rbp, %rcx
 3e6b959:      	jne	0x3e6b940 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x140>
 3e6b95b:      	testq	%rbx, %rbx
 3e6b95e:      	je	0x3e6b971 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x171>
 3e6b960:      	movq	%rbx, %rdi
 3e6b963:      	movq	%r15, %rsi
 3e6b966:      	movq	%rax, %rbx
 3e6b969:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3e6b96e:      	movq	%rbx, %rax
 3e6b971:      	movq	0x50(%rsp), %rdi
 3e6b976:      	movq	%rax, 0x68(%rdi)
 3e6b97a:      	addq	%rax, %r12
 3e6b97d:      	movq	%r12, 0x70(%rdi)
 3e6b981:      	addq	%rax, %r14
 3e6b984:      	movq	%r14, 0x78(%rdi)
 3e6b988:      	movq	0x30(%rsp), %rsi
 3e6b98d:      	leaq	0x68(%rdi), %r15
 3e6b991:      	movq	%rsi, 0x128(%rdi)
 3e6b998:      	movq	%r13, 0x130(%rdi)
 3e6b99f:      	leaq	0x80(%rdi), %rax
 3e6b9a6:      	movq	%rax, 0x48(%rsp)
 3e6b9ab:      	movq	%rdi, %r14
 3e6b9ae:      	movl	0xc(%rsp), %ebx
 3e6b9b2:      	movq	%r15, 0x58(%rsp)
 3e6b9b7:      	jmp	0x3e6ba01 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x201>
 3e6b9b9:      	nopl	(%rax)
 3e6b9c0:      	movq	0x38(%rsp), %rax
 3e6b9c5:      	movq	%rax, (%rbp)
 3e6b9c9:      	movq	0x40(%rsp), %rax
 3e6b9ce:      	movq	%rax, 0x8(%rbp)
 3e6b9d2:      	movq	%r13, 0x10(%rbp)
 3e6b9d6:      	movq	%r12, 0x18(%rbp)
 3e6b9da:      	addq	$0x20, %rbp
 3e6b9de:      	movq	%rbp, 0x70(%r14)
 3e6b9e2:      	movq	%rbp, %r12
 3e6b9e5:      	movq	0x30(%rsp), %rbp
 3e6b9ea:      	movq	0x128(%r14), %rsi
 3e6b9f1:      	movq	0x130(%r14), %r13
 3e6b9f8:      	cmpq	%r13, %rsi
 3e6b9fb:      	jae	0x3e6bcee <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4ee>
 3e6ba01:      	leaq	0x8(%rsi), %rcx
 3e6ba05:      	cmpq	%r13, %rcx
 3e6ba08:      	jbe	0x3e6ba40 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x240>
 3e6ba0a:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6ba14:      	andq	%rax, 0x38(%rsp)
 3e6ba19:      	movq	%rsi, %rcx
 3e6ba1c:      	leaq	0x8(%rcx), %rax
 3e6ba20:      	cmpq	%r13, %rax
 3e6ba23:      	ja	0x3e6ba58 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x258>
 3e6ba25:      	movq	(%rcx), %rcx
 3e6ba28:      	movq	%rcx, 0x40(%rsp)
 3e6ba2d:      	movq	%rax, 0x128(%r14)
 3e6ba34:      	jmp	0x3e6ba6a <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x26a>
 3e6ba36:      	nopw	%cs:(%rax,%rax)
 3e6ba40:      	movq	(%rsi), %rax
 3e6ba43:      	movq	%rax, 0x38(%rsp)
 3e6ba48:      	movq	%rcx, 0x128(%r14)
 3e6ba4f:      	leaq	0x8(%rcx), %rax
 3e6ba53:      	cmpq	%r13, %rax
 3e6ba56:      	jbe	0x3e6ba25 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x225>
 3e6ba58:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6ba62:      	andq	%rax, 0x40(%rsp)
 3e6ba67:      	movq	%rcx, %rax
 3e6ba6a:      	xorl	%r12d, %r12d
 3e6ba6d:      	xorl	%ecx, %ecx
 3e6ba6f:      	movq	%rax, %rdx
 3e6ba72:      	nopw	%cs:(%rax,%rax)
 3e6ba7c:      	nopl	(%rax)
 3e6ba80:      	testq	%rdx, %rdx
 3e6ba83:      	je	0x3e6bb11 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x311>
 3e6ba89:      	movzbl	(%rdx), %esi
 3e6ba8c:      	movl	%esi, %edi
 3e6ba8e:      	andl	$0x7f, %edi
 3e6ba91:      	cmpl	$0x3f, %ecx
 3e6ba94:      	jae	0x3e6baa9 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2a9>
 3e6ba96:      	shlq	%cl, %rdi
 3e6ba99:      	addq	%rdi, %r12
 3e6ba9c:      	addl	$0x7, %ecx
 3e6ba9f:      	incq	%rdx
 3e6baa2:      	testb	%sil, %sil
 3e6baa5:      	js	0x3e6ba80 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x280>
 3e6baa7:      	jmp	0x3e6bad0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2d0>
 3e6baa9:      	xorl	%r8d, %r8d
 3e6baac:      	cmpb	$0x2, %dil
 3e6bab0:      	setae	%r8b
 3e6bab4:      	xorl	%r9d, %r9d
 3e6bab7:      	testb	%dil, %dil
 3e6baba:      	setne	%r9b
 3e6babe:      	cmpl	$0x3f, %ecx
 3e6bac1:      	cmovel	%r8d, %r9d
 3e6bac5:      	testb	%r9b, %r9b
 3e6bac8:      	je	0x3e6ba96 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x296>
 3e6baca:      	jmp	0x3e6bb13 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x313>
 3e6bacc:      	nopl	(%rax)
 3e6bad0:      	movq	%r12, %rcx
 3e6bad3:      	shrq	$0x20, %rcx
 3e6bad7:      	jne	0x3e6bae3 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2e3>
 3e6bad9:      	subl	%eax, %edx
 3e6badb:      	addq	%rax, %rdx
 3e6bade:      	cmpq	%r13, %rdx
 3e6bae1:      	jbe	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x320>
 3e6bae3:      	xorl	%r12d, %r12d
 3e6bae6:      	leaq	(%rax,%r12), %rcx
 3e6baea:      	cmpq	%r13, %rcx
 3e6baed:      	jbe	0x3e6bb33 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x333>
 3e6baef:      	callq	0x828a800 <_ZNSt3_V215system_categoryEv@plt>
 3e6baf4:      	movq	%rax, %r12
 3e6baf7:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6bb01:      	andq	%rax, %rbp
 3e6bb04:      	movq	%rbp, %r13
 3e6bb07:      	testb	%bl, %bl
 3e6bb09:      	jne	0x3e6bba0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bb0f:      	jmp	0x3e6bb44 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x344>
 3e6bb11:      	xorl	%edx, %edx
 3e6bb13:      	xorl	%r12d, %r12d
 3e6bb16:      	subl	%eax, %edx
 3e6bb18:      	addq	%rax, %rdx
 3e6bb1b:      	cmpq	%r13, %rdx
 3e6bb1e:      	ja	0x3e6bae3 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2e3>
 3e6bb20:      	movq	%rdx, 0x128(%r14)
 3e6bb27:      	movq	%rdx, %rax
 3e6bb2a:      	leaq	(%rax,%r12), %rcx
 3e6bb2e:      	cmpq	%r13, %rcx
 3e6bb31:      	ja	0x3e6baef <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2ef>
 3e6bb33:      	movq	%rcx, 0x128(%r14)
 3e6bb3a:      	movq	%rax, %rbp
 3e6bb3d:      	movq	%rbp, %r13
 3e6bb40:      	testb	%bl, %bl
 3e6bb42:      	jne	0x3e6bba0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bb44:      	testq	%r12, %r12
 3e6bb47:      	je	0x3e6bb93 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x393>
 3e6bb49:      	addq	%r12, 0xd0(%r14)
 3e6bb50:      	movq	0x80(%r14), %r13
 3e6bb57:      	testq	%r13, %r13
 3e6bb5a:      	je	0x3e6bca5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4a5>
 3e6bb60:      	leaq	(%r12,%r13), %rax
 3e6bb64:      	cmpq	0x88(%r14), %rax
 3e6bb6b:      	ja	0x3e6bca5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4a5>
 3e6bb71:      	movq	0x48(%rsp), %rcx
 3e6bb76:      	movq	%rax, (%rcx)
 3e6bb79:      	cmpq	$0x2, %r12
 3e6bb7d:      	jl	0x3e6bcc4 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4c4>
 3e6bb83:      	movq	%r13, %rdi
 3e6bb86:      	movq	%rbp, %rsi
 3e6bb89:      	movq	%r12, %rdx
 3e6bb8c:      	callq	0x828ac50 <memmove@plt>
 3e6bb91:      	jmp	0x3e6bba0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bb93:      	xorl	%r13d, %r13d
 3e6bb96:      	nopw	%cs:(%rax,%rax)
 3e6bba0:      	movq	%rbp, 0x30(%rsp)
 3e6bba5:      	movq	0x70(%r14), %rbp
 3e6bba9:      	cmpq	0x78(%r14), %rbp
 3e6bbad:      	jne	0x3e6b9c0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x1c0>
 3e6bbb3:      	movq	%r13, 0x60(%rsp)
 3e6bbb8:      	movq	(%r15), %r13
 3e6bbbb:      	movq	%rbp, %r14
 3e6bbbe:      	subq	%r13, %r14
 3e6bbc1:      	movabsq	$0x7fffffffffffffe0, %rax # imm = 0x7FFFFFFFFFFFFFE0
 3e6bbcb:      	cmpq	%rax, %r14
 3e6bbce:      	je	0x3e6bfbd <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7bd>
 3e6bbd4:      	movq	%r14, %rax
 3e6bbd7:      	sarq	$0x5, %rax
 3e6bbdb:      	cmpq	$0x1, %rax
 3e6bbdf:      	movq	%rax, %rcx
 3e6bbe2:      	adcq	$0x0, %rcx
 3e6bbe6:      	leaq	(%rcx,%rax), %r15
 3e6bbea:      	movabsq	$0x3ffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFF
 3e6bbf4:      	cmpq	%rdx, %r15
 3e6bbf7:      	cmovaeq	%rdx, %r15
 3e6bbfb:      	addq	%rax, %rcx
 3e6bbfe:      	cmovbq	%rdx, %r15
 3e6bc02:      	shlq	$0x5, %r15
 3e6bc06:      	movq	%r15, %rdi
 3e6bc09:      	callq	0x828a6b0 <_Znwm@plt>
 3e6bc0e:      	movq	%rax, %rbx
 3e6bc11:      	movq	0x38(%rsp), %rax
 3e6bc16:      	movq	%rax, (%rbx,%r14)
 3e6bc1a:      	movq	0x40(%rsp), %rax
 3e6bc1f:      	movq	%rax, 0x8(%rbx,%r14)
 3e6bc24:      	movq	0x60(%rsp), %rax
 3e6bc29:      	movq	%rax, 0x10(%rbx,%r14)
 3e6bc2e:      	movq	%r12, 0x18(%rbx,%r14)
 3e6bc33:      	movq	%rbx, %r12
 3e6bc36:      	cmpq	%rbp, %r13
 3e6bc39:      	je	0x3e6bc6f <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x46f>
 3e6bc3b:      	movq	%rbx, %r12
 3e6bc3e:      	movq	%r13, %rax
 3e6bc41:      	nopw	%cs:(%rax,%rax)
 3e6bc4b:      	nopl	(%rax,%rax)
 3e6bc50:      	movups	(%rax), %xmm0
 3e6bc53:      	movups	0x10(%rax), %xmm1
 3e6bc57:      	movups	%xmm1, 0x10(%r12)
 3e6bc5d:      	movups	%xmm0, (%r12)
 3e6bc62:      	addq	$0x20, %rax
 3e6bc66:      	addq	$0x20, %r12
 3e6bc6a:      	cmpq	%rbp, %rax
 3e6bc6d:      	jne	0x3e6bc50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x450>
 3e6bc6f:      	testq	%r13, %r13
 3e6bc72:      	je	0x3e6bc7f <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x47f>
 3e6bc74:      	movq	%r13, %rdi
 3e6bc77:      	movq	%r14, %rsi
 3e6bc7a:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3e6bc7f:      	addq	$0x20, %r12
 3e6bc83:      	movq	0x50(%rsp), %r14
 3e6bc88:      	movq	%rbx, 0x68(%r14)
 3e6bc8c:      	movq	%r12, 0x70(%r14)
 3e6bc90:      	addq	%r15, %rbx
 3e6bc93:      	movq	%rbx, 0x78(%r14)
 3e6bc97:      	movl	0xc(%rsp), %ebx
 3e6bc9b:      	movq	0x58(%rsp), %r15
 3e6bca0:      	jmp	0x3e6b9e5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x1e5>
 3e6bca5:      	movq	0x48(%rsp), %rdi
 3e6bcaa:      	movq	%r12, %rsi
 3e6bcad:      	movq	%r12, %rdx
 3e6bcb0:      	xorl	%ecx, %ecx
 3e6bcb2:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 3e6bcb7:      	movq	%rax, %r13
 3e6bcba:      	cmpq	$0x2, %r12
 3e6bcbe:      	jge	0x3e6bb83 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x383>
 3e6bcc4:      	cmpq	$0x1, %r12
 3e6bcc8:      	jne	0x3e6bba0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bcce:      	movzbl	(%rbp), %eax
 3e6bcd2:      	movb	%al, (%r13)
 3e6bcd6:      	jmp	0x3e6bba0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bcdb:      	xorl	%r14d, %r14d
 3e6bcde:      	jmp	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bce3:      	movq	0x70(%rdi), %r12
 3e6bce7:      	addq	$0x68, %rdi
 3e6bceb:      	movq	%rdi, %r15
 3e6bcee:      	movq	(%r15), %rbx
 3e6bcf1:      	movb	$0x1, %r14b
 3e6bcf4:      	cmpq	%r12, %rbx
 3e6bcf7:      	je	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bcfd:      	movq	%r12, %r15
 3e6bd00:      	subq	%rbx, %r15
 3e6bd03:      	movq	%r15, %rax
 3e6bd06:      	sarq	$0x5, %rax
 3e6bd0a:      	bsrq	%rax, %rdx
 3e6bd0e:      	xorl	$0x3f, %edx
 3e6bd11:      	addl	%edx, %edx
 3e6bd13:      	xorq	$0x7e, %rdx
 3e6bd17:      	movq	%rbx, %rdi
 3e6bd1a:      	movq	%r12, %rsi
 3e6bd1d:      	callq	0x3e6f2f0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm21MCPseudoProbeFuncDescESt6vectorIS3_SaIS3_EEEElNS0_5__ops15_Iter_comp_iterIZNS2_20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmbE3$_0EEEvT_SG_T0_T1_>
 3e6bd22:      	leaq	0x20(%rbx), %rsi
 3e6bd26:      	cmpq	$0x201, %r15            # imm = 0x201
 3e6bd2d:      	jl	0x3e6be2f <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x62f>
 3e6bd33:      	movl	$0x20, %r13d
 3e6bd39:      	movq	%rsi, %rbp
 3e6bd3c:      	movq	%rbx, %rax
 3e6bd3f:      	jmp	0x3e6bd7d <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x57d>
 3e6bd41:      	nopw	%cs:(%rax,%rax)
 3e6bd4b:      	nopl	(%rax,%rax)
 3e6bd50:      	movq	%rcx, (%rdx)
 3e6bd53:      	movaps	0x10(%rsp), %xmm0
 3e6bd58:      	movups	%xmm0, 0x8(%rdx)
 3e6bd5c:      	movq	0x20(%rsp), %rax
 3e6bd61:      	movq	%rax, 0x18(%rdx)
 3e6bd65:      	addq	$0x20, %r13
 3e6bd69:      	addq	$0x20, %rbp
 3e6bd6d:      	movq	%r15, %rax
 3e6bd70:      	cmpq	$0x200, %r13            # imm = 0x200
 3e6bd77:      	je	0x3e6bf38 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x738>
 3e6bd7d:      	leaq	(%rbx,%r13), %r15
 3e6bd81:      	movq	(%rbx,%r13), %rcx
 3e6bd85:      	cmpq	(%rbx), %rcx
 3e6bd88:      	jae	0x3e6bdd0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x5d0>
 3e6bd8a:      	movups	(%r15), %xmm0
 3e6bd8e:      	movups	0x10(%r15), %xmm1
 3e6bd93:      	movaps	%xmm1, 0x20(%rsp)
 3e6bd98:      	movaps	%xmm0, 0x10(%rsp)
 3e6bd9d:      	cmpq	$0x21, %r13
 3e6bda1:      	jb	0x3e6be1e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x61e>
 3e6bda3:      	movq	%rsi, %rdi
 3e6bda6:      	movq	%rbx, %rsi
 3e6bda9:      	movq	%r13, %rdx
 3e6bdac:      	callq	0x828ac50 <memmove@plt>
 3e6bdb1:      	leaq	0x20(%rbx), %rsi
 3e6bdb5:      	movaps	0x10(%rsp), %xmm0
 3e6bdba:      	movaps	0x20(%rsp), %xmm1
 3e6bdbf:      	movups	%xmm1, 0x10(%rbx)
 3e6bdc3:      	movups	%xmm0, (%rbx)
 3e6bdc6:      	jmp	0x3e6bd65 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x565>
 3e6bdc8:      	nopl	(%rax,%rax)
 3e6bdd0:      	movq	0x38(%rax), %rdx
 3e6bdd4:      	movq	%rdx, 0x20(%rsp)
 3e6bdd9:      	movups	0x28(%rax), %xmm0
 3e6bddd:      	movaps	%xmm0, 0x10(%rsp)
 3e6bde2:      	movq	%r15, %rdx
 3e6bde5:      	cmpq	(%rax), %rcx
 3e6bde8:      	jae	0x3e6bd50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x550>
 3e6bdee:      	movq	%rbp, %rdx
 3e6bdf1:      	nopw	%cs:(%rax,%rax)
 3e6bdfb:      	nopl	(%rax,%rax)
 3e6be00:      	movups	-0x20(%rdx), %xmm0
 3e6be04:      	movups	-0x10(%rdx), %xmm1
 3e6be08:      	movups	%xmm1, 0x10(%rdx)
 3e6be0c:      	movups	%xmm0, (%rdx)
 3e6be0f:      	cmpq	-0x40(%rdx), %rcx
 3e6be13:      	leaq	-0x20(%rdx), %rdx
 3e6be17:      	jb	0x3e6be00 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x600>
 3e6be19:      	jmp	0x3e6bd50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x550>
 3e6be1e:      	movups	(%rbx), %xmm0
 3e6be21:      	movups	0x10(%rbx), %xmm1
 3e6be25:      	movups	%xmm1, 0x30(%rax)
 3e6be29:      	movups	%xmm0, 0x20(%rax)
 3e6be2d:      	jmp	0x3e6bdb5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x5b5>
 3e6be2f:      	cmpq	%r12, %rsi
 3e6be32:      	je	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6be38:      	movq	%rbx, %rdi
 3e6be3b:      	jmp	0x3e6be65 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x665>
 3e6be3d:      	nopl	(%rax)
 3e6be40:      	movq	%rax, (%rcx)
 3e6be43:      	movaps	0x10(%rsp), %xmm0
 3e6be48:      	movups	%xmm0, 0x8(%rcx)
 3e6be4c:      	movq	0x20(%rsp), %rax
 3e6be51:      	movq	%rax, 0x18(%rcx)
 3e6be55:      	leaq	0x20(%r13), %rsi
 3e6be59:      	movq	%r13, %rdi
 3e6be5c:      	cmpq	%r12, %rsi
 3e6be5f:      	je	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6be65:      	movq	%rsi, %r13
 3e6be68:      	movq	(%rsi), %rax
 3e6be6b:      	cmpq	(%rbx), %rax
 3e6be6e:      	jae	0x3e6bed0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6d0>
 3e6be70:      	movups	(%r13), %xmm0
 3e6be75:      	movups	0x10(%r13), %xmm1
 3e6be7a:      	movaps	%xmm1, 0x20(%rsp)
 3e6be7f:      	movaps	%xmm0, 0x10(%rsp)
 3e6be84:      	movq	%r13, %rdx
 3e6be87:      	subq	%rbx, %rdx
 3e6be8a:      	movq	%rdx, %rax
 3e6be8d:      	sarq	$0x5, %rax
 3e6be91:      	cmpq	$0x2, %rax
 3e6be95:      	jl	0x3e6bf1e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x71e>
 3e6be9b:      	shlq	$0x5, %rax
 3e6be9f:      	subq	%rax, %rdi
 3e6bea2:      	addq	$0x40, %rdi
 3e6bea6:      	movq	%rbx, %rsi
 3e6bea9:      	callq	0x828ac50 <memmove@plt>
 3e6beae:      	movaps	0x10(%rsp), %xmm0
 3e6beb3:      	movaps	0x20(%rsp), %xmm1
 3e6beb8:      	movups	%xmm1, 0x10(%rbx)
 3e6bebc:      	movups	%xmm0, (%rbx)
 3e6bebf:      	leaq	0x20(%r13), %rsi
 3e6bec3:      	movq	%r13, %rdi
 3e6bec6:      	cmpq	%r12, %rsi
 3e6bec9:      	jne	0x3e6be65 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x665>
 3e6becb:      	jmp	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bed0:      	movq	0x38(%rdi), %rcx
 3e6bed4:      	movq	%rcx, 0x20(%rsp)
 3e6bed9:      	movups	0x28(%rdi), %xmm0
 3e6bedd:      	movaps	%xmm0, 0x10(%rsp)
 3e6bee2:      	movq	%r13, %rcx
 3e6bee5:      	cmpq	(%rdi), %rax
 3e6bee8:      	jae	0x3e6be40 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x640>
 3e6beee:      	movq	%r13, %rcx
 3e6bef1:      	nopw	%cs:(%rax,%rax)
 3e6befb:      	nopl	(%rax,%rax)
 3e6bf00:      	movups	-0x20(%rcx), %xmm0
 3e6bf04:      	movups	-0x10(%rcx), %xmm1
 3e6bf08:      	movups	%xmm1, 0x10(%rcx)
 3e6bf0c:      	movups	%xmm0, (%rcx)
 3e6bf0f:      	cmpq	-0x40(%rcx), %rax
 3e6bf13:      	leaq	-0x20(%rcx), %rcx
 3e6bf17:      	jb	0x3e6bf00 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x700>
 3e6bf19:      	jmp	0x3e6be40 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x640>
 3e6bf1e:      	cmpq	$0x20, %rdx
 3e6bf22:      	jne	0x3e6beae <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6ae>
 3e6bf24:      	movups	(%rbx), %xmm0
 3e6bf27:      	movups	0x10(%rbx), %xmm1
 3e6bf2b:      	movups	%xmm1, 0x30(%rdi)
 3e6bf2f:      	movups	%xmm0, 0x20(%rdi)
 3e6bf33:      	jmp	0x3e6beae <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6ae>
 3e6bf38:      	addq	$0x200, %rbx            # imm = 0x200
 3e6bf3f:      	jmp	0x3e6bf69 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x769>
 3e6bf41:      	nopw	%cs:(%rax,%rax)
 3e6bf4b:      	nopl	(%rax,%rax)
 3e6bf50:      	movq	%rax, (%rcx)
 3e6bf53:      	movaps	0x10(%rsp), %xmm0
 3e6bf58:      	movups	%xmm0, 0x8(%rcx)
 3e6bf5c:      	movq	0x20(%rsp), %rax
 3e6bf61:      	movq	%rax, 0x18(%rcx)
 3e6bf65:      	addq	$0x20, %rbx
 3e6bf69:      	cmpq	%r12, %rbx
 3e6bf6c:      	je	0x3e6bfab <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bf6e:      	movq	(%rbx), %rax
 3e6bf71:      	movq	0x18(%rbx), %rcx
 3e6bf75:      	movq	%rcx, 0x20(%rsp)
 3e6bf7a:      	movups	0x8(%rbx), %xmm0
 3e6bf7e:      	movaps	%xmm0, 0x10(%rsp)
 3e6bf83:      	movq	%rbx, %rcx
 3e6bf86:      	cmpq	-0x20(%rbx), %rax
 3e6bf8a:      	jae	0x3e6bf50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x750>
 3e6bf8c:      	movq	%rbx, %rcx
 3e6bf8f:      	nop
 3e6bf90:      	movups	-0x20(%rcx), %xmm0
 3e6bf94:      	movups	-0x10(%rcx), %xmm1
 3e6bf98:      	movups	%xmm1, 0x10(%rcx)
 3e6bf9c:      	movups	%xmm0, (%rcx)
 3e6bf9f:      	cmpq	-0x40(%rcx), %rax
 3e6bfa3:      	leaq	-0x20(%rcx), %rcx
 3e6bfa7:      	jb	0x3e6bf90 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x790>
 3e6bfa9:      	jmp	0x3e6bf50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x750>
 3e6bfab:      	movl	%r14d, %eax
 3e6bfae:      	addq	$0x68, %rsp
 3e6bfb2:      	popq	%rbx
 3e6bfb3:      	popq	%r12
 3e6bfb5:      	popq	%r13
 3e6bfb7:      	popq	%r14
 3e6bfb9:      	popq	%r15
 3e6bfbb:      	popq	%rbp
 3e6bfbc:      	retq
 3e6bfbd:      	leaq	-0x31d15da(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 3e6bfc4:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
