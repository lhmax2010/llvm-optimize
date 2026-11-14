
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003e6b780 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb>:
 3e6b780:      	pushq	%rbp
 3e6b781:      	pushq	%r15
 3e6b783:      	pushq	%r14
 3e6b785:      	pushq	%r13
 3e6b787:      	pushq	%r12
 3e6b789:      	pushq	%rbx
 3e6b78a:      	subq	$0x68, %rsp
 3e6b78e:      	movq	%rsi, 0x128(%rdi)
 3e6b795:      	leaq	(%rsi,%rdx), %r13
 3e6b799:      	movq	%r13, 0x130(%rdi)
 3e6b7a0:      	testq	%rdx, %rdx
 3e6b7a3:      	je	0x3e6bc63 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4e3>
 3e6b7a9:      	movl	%ecx, %ebp
 3e6b7ab:      	xorl	%eax, %eax
 3e6b7ad:      	movq	%rsi, %rdx
 3e6b7b0:      	leaq	0x8(%rdx), %rcx
 3e6b7b4:      	cmpq	%r13, %rcx
 3e6b7b7:      	ja	0x3e6bc5b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b7bd:      	movq	%rcx, 0x128(%rdi)
 3e6b7c4:      	addq	$0x10, %rdx
 3e6b7c8:      	xorl	%r14d, %r14d
 3e6b7cb:      	cmpq	%r13, %rdx
 3e6b7ce:      	ja	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6b7d4:      	movq	%rdx, 0x128(%rdi)
 3e6b7db:      	xorl	%ebx, %ebx
 3e6b7dd:      	movq	%rdx, %r8
 3e6b7e0:      	movzbl	(%r8), %r9d
 3e6b7e4:      	movl	%r9d, %r10d
 3e6b7e7:      	andl	$0x7f, %r10d
 3e6b7eb:      	cmpl	$0x3f, %r14d
 3e6b7ef:      	jae	0x3e6b808 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x88>
 3e6b7f1:      	movl	%r14d, %ecx
 3e6b7f4:      	shlq	%cl, %r10
 3e6b7f7:      	addq	%r10, %rbx
 3e6b7fa:      	addl	$0x7, %r14d
 3e6b7fe:      	incq	%r8
 3e6b801:      	testb	%r9b, %r9b
 3e6b804:      	js	0x3e6b7e0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x60>
 3e6b806:      	jmp	0x3e6b830 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0xb0>
 3e6b808:      	xorl	%ecx, %ecx
 3e6b80a:      	cmpb	$0x2, %r10b
 3e6b80e:      	setae	%cl
 3e6b811:      	xorl	%r11d, %r11d
 3e6b814:      	testb	%r10b, %r10b
 3e6b817:      	setne	%r11b
 3e6b81b:      	cmpl	$0x3f, %r14d
 3e6b81f:      	cmovel	%ecx, %r11d
 3e6b823:      	testb	%r11b, %r11b
 3e6b826:      	je	0x3e6b7f1 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x71>
 3e6b828:      	xorl	%ebx, %ebx
 3e6b82a:      	jmp	0x3e6b83d <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0xbd>
 3e6b82c:      	nopl	(%rax)
 3e6b830:      	movq	%rbx, %rcx
 3e6b833:      	shrq	$0x20, %rcx
 3e6b837:      	jne	0x3e6bc5b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b83d:      	subl	%edx, %r8d
 3e6b840:      	addq	%rdx, %r8
 3e6b843:      	cmpq	%r13, %r8
 3e6b846:      	ja	0x3e6bc5b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b84c:      	movq	%r8, 0x128(%rdi)
 3e6b853:      	addq	%r8, %rbx
 3e6b856:      	cmpq	%r13, %rbx
 3e6b859:      	ja	0x3e6bc5b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4db>
 3e6b85f:      	movq	%rbx, 0x128(%rdi)
 3e6b866:      	incl	%eax
 3e6b868:      	movq	%rbx, %rdx
 3e6b86b:      	cmpq	%r13, %rbx
 3e6b86e:      	jb	0x3e6b7b0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x30>
 3e6b874:      	movl	%ebp, 0xc(%rsp)
 3e6b878:      	movl	%eax, %r14d
 3e6b87b:      	movq	0x68(%rdi), %rbx
 3e6b87f:      	movq	0x78(%rdi), %r15
 3e6b883:      	subq	%rbx, %r15
 3e6b886:      	movq	%r15, %rax
 3e6b889:      	sarq	$0x5, %rax
 3e6b88d:      	cmpq	%r14, %rax
 3e6b890:      	movq	%rdi, 0x50(%rsp)
 3e6b895:      	jae	0x3e6b90d <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x18d>
 3e6b897:      	movq	%rsi, 0x30(%rsp)
 3e6b89c:      	movq	0x70(%rdi), %rbp
 3e6b8a0:      	shlq	$0x5, %r14
 3e6b8a4:      	movq	%r14, %rdi
 3e6b8a7:      	callq	0x828a620 <_Znwm@plt>
 3e6b8ac:      	movq	%rbp, %r12
 3e6b8af:      	subq	%rbx, %r12
 3e6b8b2:      	je	0x3e6b8db <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x15b>
 3e6b8b4:      	movq	%rax, %rdx
 3e6b8b7:      	movq	%rbx, %rcx
 3e6b8ba:      	nopw	(%rax,%rax)
 3e6b8c0:      	movups	(%rcx), %xmm0
 3e6b8c3:      	movups	0x10(%rcx), %xmm1
 3e6b8c7:      	movups	%xmm1, 0x10(%rdx)
 3e6b8cb:      	movups	%xmm0, (%rdx)
 3e6b8ce:      	addq	$0x20, %rcx
 3e6b8d2:      	addq	$0x20, %rdx
 3e6b8d6:      	cmpq	%rbp, %rcx
 3e6b8d9:      	jne	0x3e6b8c0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x140>
 3e6b8db:      	testq	%rbx, %rbx
 3e6b8de:      	je	0x3e6b8f1 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x171>
 3e6b8e0:      	movq	%rbx, %rdi
 3e6b8e3:      	movq	%r15, %rsi
 3e6b8e6:      	movq	%rax, %rbx
 3e6b8e9:      	callq	0x828a660 <_ZdlPvm@plt>
 3e6b8ee:      	movq	%rbx, %rax
 3e6b8f1:      	movq	0x50(%rsp), %rdi
 3e6b8f6:      	movq	%rax, 0x68(%rdi)
 3e6b8fa:      	addq	%rax, %r12
 3e6b8fd:      	movq	%r12, 0x70(%rdi)
 3e6b901:      	addq	%rax, %r14
 3e6b904:      	movq	%r14, 0x78(%rdi)
 3e6b908:      	movq	0x30(%rsp), %rsi
 3e6b90d:      	leaq	0x68(%rdi), %r15
 3e6b911:      	movq	%rsi, 0x128(%rdi)
 3e6b918:      	movq	%r13, 0x130(%rdi)
 3e6b91f:      	leaq	0x80(%rdi), %rax
 3e6b926:      	movq	%rax, 0x48(%rsp)
 3e6b92b:      	movq	%rdi, %r14
 3e6b92e:      	movl	0xc(%rsp), %ebx
 3e6b932:      	movq	%r15, 0x58(%rsp)
 3e6b937:      	jmp	0x3e6b981 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x201>
 3e6b939:      	nopl	(%rax)
 3e6b940:      	movq	0x38(%rsp), %rax
 3e6b945:      	movq	%rax, (%rbp)
 3e6b949:      	movq	0x40(%rsp), %rax
 3e6b94e:      	movq	%rax, 0x8(%rbp)
 3e6b952:      	movq	%r13, 0x10(%rbp)
 3e6b956:      	movq	%r12, 0x18(%rbp)
 3e6b95a:      	addq	$0x20, %rbp
 3e6b95e:      	movq	%rbp, 0x70(%r14)
 3e6b962:      	movq	%rbp, %r12
 3e6b965:      	movq	0x30(%rsp), %rbp
 3e6b96a:      	movq	0x128(%r14), %rsi
 3e6b971:      	movq	0x130(%r14), %r13
 3e6b978:      	cmpq	%r13, %rsi
 3e6b97b:      	jae	0x3e6bc6e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4ee>
 3e6b981:      	leaq	0x8(%rsi), %rcx
 3e6b985:      	cmpq	%r13, %rcx
 3e6b988:      	jbe	0x3e6b9c0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x240>
 3e6b98a:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6b994:      	andq	%rax, 0x38(%rsp)
 3e6b999:      	movq	%rsi, %rcx
 3e6b99c:      	leaq	0x8(%rcx), %rax
 3e6b9a0:      	cmpq	%r13, %rax
 3e6b9a3:      	ja	0x3e6b9d8 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x258>
 3e6b9a5:      	movq	(%rcx), %rcx
 3e6b9a8:      	movq	%rcx, 0x40(%rsp)
 3e6b9ad:      	movq	%rax, 0x128(%r14)
 3e6b9b4:      	jmp	0x3e6b9ea <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x26a>
 3e6b9b6:      	nopw	%cs:(%rax,%rax)
 3e6b9c0:      	movq	(%rsi), %rax
 3e6b9c3:      	movq	%rax, 0x38(%rsp)
 3e6b9c8:      	movq	%rcx, 0x128(%r14)
 3e6b9cf:      	leaq	0x8(%rcx), %rax
 3e6b9d3:      	cmpq	%r13, %rax
 3e6b9d6:      	jbe	0x3e6b9a5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x225>
 3e6b9d8:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6b9e2:      	andq	%rax, 0x40(%rsp)
 3e6b9e7:      	movq	%rcx, %rax
 3e6b9ea:      	xorl	%r12d, %r12d
 3e6b9ed:      	xorl	%ecx, %ecx
 3e6b9ef:      	movq	%rax, %rdx
 3e6b9f2:      	nopw	%cs:(%rax,%rax)
 3e6b9fc:      	nopl	(%rax)
 3e6ba00:      	testq	%rdx, %rdx
 3e6ba03:      	je	0x3e6ba91 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x311>
 3e6ba09:      	movzbl	(%rdx), %esi
 3e6ba0c:      	movl	%esi, %edi
 3e6ba0e:      	andl	$0x7f, %edi
 3e6ba11:      	cmpl	$0x3f, %ecx
 3e6ba14:      	jae	0x3e6ba29 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2a9>
 3e6ba16:      	shlq	%cl, %rdi
 3e6ba19:      	addq	%rdi, %r12
 3e6ba1c:      	addl	$0x7, %ecx
 3e6ba1f:      	incq	%rdx
 3e6ba22:      	testb	%sil, %sil
 3e6ba25:      	js	0x3e6ba00 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x280>
 3e6ba27:      	jmp	0x3e6ba50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2d0>
 3e6ba29:      	xorl	%r8d, %r8d
 3e6ba2c:      	cmpb	$0x2, %dil
 3e6ba30:      	setae	%r8b
 3e6ba34:      	xorl	%r9d, %r9d
 3e6ba37:      	testb	%dil, %dil
 3e6ba3a:      	setne	%r9b
 3e6ba3e:      	cmpl	$0x3f, %ecx
 3e6ba41:      	cmovel	%r8d, %r9d
 3e6ba45:      	testb	%r9b, %r9b
 3e6ba48:      	je	0x3e6ba16 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x296>
 3e6ba4a:      	jmp	0x3e6ba93 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x313>
 3e6ba4c:      	nopl	(%rax)
 3e6ba50:      	movq	%r12, %rcx
 3e6ba53:      	shrq	$0x20, %rcx
 3e6ba57:      	jne	0x3e6ba63 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2e3>
 3e6ba59:      	subl	%eax, %edx
 3e6ba5b:      	addq	%rax, %rdx
 3e6ba5e:      	cmpq	%r13, %rdx
 3e6ba61:      	jbe	0x3e6baa0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x320>
 3e6ba63:      	xorl	%r12d, %r12d
 3e6ba66:      	leaq	(%rax,%r12), %rcx
 3e6ba6a:      	cmpq	%r13, %rcx
 3e6ba6d:      	jbe	0x3e6bab3 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x333>
 3e6ba6f:      	callq	0x828a770 <_ZNSt3_V215system_categoryEv@plt>
 3e6ba74:      	movq	%rax, %r12
 3e6ba77:      	movabsq	$-0x100000000, %rax     # imm = 0xFFFFFFFF00000000
 3e6ba81:      	andq	%rax, %rbp
 3e6ba84:      	movq	%rbp, %r13
 3e6ba87:      	testb	%bl, %bl
 3e6ba89:      	jne	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6ba8f:      	jmp	0x3e6bac4 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x344>
 3e6ba91:      	xorl	%edx, %edx
 3e6ba93:      	xorl	%r12d, %r12d
 3e6ba96:      	subl	%eax, %edx
 3e6ba98:      	addq	%rax, %rdx
 3e6ba9b:      	cmpq	%r13, %rdx
 3e6ba9e:      	ja	0x3e6ba63 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2e3>
 3e6baa0:      	movq	%rdx, 0x128(%r14)
 3e6baa7:      	movq	%rdx, %rax
 3e6baaa:      	leaq	(%rax,%r12), %rcx
 3e6baae:      	cmpq	%r13, %rcx
 3e6bab1:      	ja	0x3e6ba6f <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x2ef>
 3e6bab3:      	movq	%rcx, 0x128(%r14)
 3e6baba:      	movq	%rax, %rbp
 3e6babd:      	movq	%rbp, %r13
 3e6bac0:      	testb	%bl, %bl
 3e6bac2:      	jne	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bac4:      	testq	%r12, %r12
 3e6bac7:      	je	0x3e6bb13 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x393>
 3e6bac9:      	addq	%r12, 0xd0(%r14)
 3e6bad0:      	movq	0x80(%r14), %r13
 3e6bad7:      	testq	%r13, %r13
 3e6bada:      	je	0x3e6bc25 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4a5>
 3e6bae0:      	leaq	(%r12,%r13), %rax
 3e6bae4:      	cmpq	0x88(%r14), %rax
 3e6baeb:      	ja	0x3e6bc25 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4a5>
 3e6baf1:      	movq	0x48(%rsp), %rcx
 3e6baf6:      	movq	%rax, (%rcx)
 3e6baf9:      	cmpq	$0x2, %r12
 3e6bafd:      	jl	0x3e6bc44 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x4c4>
 3e6bb03:      	movq	%r13, %rdi
 3e6bb06:      	movq	%rbp, %rsi
 3e6bb09:      	movq	%r12, %rdx
 3e6bb0c:      	callq	0x828abc0 <memmove@plt>
 3e6bb11:      	jmp	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bb13:      	xorl	%r13d, %r13d
 3e6bb16:      	nopw	%cs:(%rax,%rax)
 3e6bb20:      	movq	%rbp, 0x30(%rsp)
 3e6bb25:      	movq	0x70(%r14), %rbp
 3e6bb29:      	cmpq	0x78(%r14), %rbp
 3e6bb2d:      	jne	0x3e6b940 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x1c0>
 3e6bb33:      	movq	%r13, 0x60(%rsp)
 3e6bb38:      	movq	(%r15), %r13
 3e6bb3b:      	movq	%rbp, %r14
 3e6bb3e:      	subq	%r13, %r14
 3e6bb41:      	movabsq	$0x7fffffffffffffe0, %rax # imm = 0x7FFFFFFFFFFFFFE0
 3e6bb4b:      	cmpq	%rax, %r14
 3e6bb4e:      	je	0x3e6bf3d <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7bd>
 3e6bb54:      	movq	%r14, %rax
 3e6bb57:      	sarq	$0x5, %rax
 3e6bb5b:      	cmpq	$0x1, %rax
 3e6bb5f:      	movq	%rax, %rcx
 3e6bb62:      	adcq	$0x0, %rcx
 3e6bb66:      	leaq	(%rcx,%rax), %r15
 3e6bb6a:      	movabsq	$0x3ffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFF
 3e6bb74:      	cmpq	%rdx, %r15
 3e6bb77:      	cmovaeq	%rdx, %r15
 3e6bb7b:      	addq	%rax, %rcx
 3e6bb7e:      	cmovbq	%rdx, %r15
 3e6bb82:      	shlq	$0x5, %r15
 3e6bb86:      	movq	%r15, %rdi
 3e6bb89:      	callq	0x828a620 <_Znwm@plt>
 3e6bb8e:      	movq	%rax, %rbx
 3e6bb91:      	movq	0x38(%rsp), %rax
 3e6bb96:      	movq	%rax, (%rbx,%r14)
 3e6bb9a:      	movq	0x40(%rsp), %rax
 3e6bb9f:      	movq	%rax, 0x8(%rbx,%r14)
 3e6bba4:      	movq	0x60(%rsp), %rax
 3e6bba9:      	movq	%rax, 0x10(%rbx,%r14)
 3e6bbae:      	movq	%r12, 0x18(%rbx,%r14)
 3e6bbb3:      	movq	%rbx, %r12
 3e6bbb6:      	cmpq	%rbp, %r13
 3e6bbb9:      	je	0x3e6bbef <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x46f>
 3e6bbbb:      	movq	%rbx, %r12
 3e6bbbe:      	movq	%r13, %rax
 3e6bbc1:      	nopw	%cs:(%rax,%rax)
 3e6bbcb:      	nopl	(%rax,%rax)
 3e6bbd0:      	movups	(%rax), %xmm0
 3e6bbd3:      	movups	0x10(%rax), %xmm1
 3e6bbd7:      	movups	%xmm1, 0x10(%r12)
 3e6bbdd:      	movups	%xmm0, (%r12)
 3e6bbe2:      	addq	$0x20, %rax
 3e6bbe6:      	addq	$0x20, %r12
 3e6bbea:      	cmpq	%rbp, %rax
 3e6bbed:      	jne	0x3e6bbd0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x450>
 3e6bbef:      	testq	%r13, %r13
 3e6bbf2:      	je	0x3e6bbff <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x47f>
 3e6bbf4:      	movq	%r13, %rdi
 3e6bbf7:      	movq	%r14, %rsi
 3e6bbfa:      	callq	0x828a660 <_ZdlPvm@plt>
 3e6bbff:      	addq	$0x20, %r12
 3e6bc03:      	movq	0x50(%rsp), %r14
 3e6bc08:      	movq	%rbx, 0x68(%r14)
 3e6bc0c:      	movq	%r12, 0x70(%r14)
 3e6bc10:      	addq	%r15, %rbx
 3e6bc13:      	movq	%rbx, 0x78(%r14)
 3e6bc17:      	movl	0xc(%rsp), %ebx
 3e6bc1b:      	movq	0x58(%rsp), %r15
 3e6bc20:      	jmp	0x3e6b965 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x1e5>
 3e6bc25:      	movq	0x48(%rsp), %rdi
 3e6bc2a:      	movq	%r12, %rsi
 3e6bc2d:      	movq	%r12, %rdx
 3e6bc30:      	xorl	%ecx, %ecx
 3e6bc32:      	callq	0x280e890 <_ZN4llvm20BumpPtrAllocatorImplINS_15MallocAllocatorELm4096ELm4096ELm128EE12AllocateSlowEmmNS_5AlignE>
 3e6bc37:      	movq	%rax, %r13
 3e6bc3a:      	cmpq	$0x2, %r12
 3e6bc3e:      	jge	0x3e6bb03 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x383>
 3e6bc44:      	cmpq	$0x1, %r12
 3e6bc48:      	jne	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bc4e:      	movzbl	(%rbp), %eax
 3e6bc52:      	movb	%al, (%r13)
 3e6bc56:      	jmp	0x3e6bb20 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x3a0>
 3e6bc5b:      	xorl	%r14d, %r14d
 3e6bc5e:      	jmp	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bc63:      	movq	0x70(%rdi), %r12
 3e6bc67:      	addq	$0x68, %rdi
 3e6bc6b:      	movq	%rdi, %r15
 3e6bc6e:      	movq	(%r15), %rbx
 3e6bc71:      	movb	$0x1, %r14b
 3e6bc74:      	cmpq	%r12, %rbx
 3e6bc77:      	je	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bc7d:      	movq	%r12, %r15
 3e6bc80:      	subq	%rbx, %r15
 3e6bc83:      	movq	%r15, %rax
 3e6bc86:      	sarq	$0x5, %rax
 3e6bc8a:      	bsrq	%rax, %rdx
 3e6bc8e:      	xorl	$0x3f, %edx
 3e6bc91:      	addl	%edx, %edx
 3e6bc93:      	xorq	$0x7e, %rdx
 3e6bc97:      	movq	%rbx, %rdi
 3e6bc9a:      	movq	%r12, %rsi
 3e6bc9d:      	callq	0x3e6f270 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm21MCPseudoProbeFuncDescESt6vectorIS3_SaIS3_EEEElNS0_5__ops15_Iter_comp_iterIZNS2_20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmbE3$_0EEEvT_SG_T0_T1_>
 3e6bca2:      	leaq	0x20(%rbx), %rsi
 3e6bca6:      	cmpq	$0x201, %r15            # imm = 0x201
 3e6bcad:      	jl	0x3e6bdaf <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x62f>
 3e6bcb3:      	leaq	0x20(%rbx), %rbp
 3e6bcb7:      	movl	$0x20, %r13d
 3e6bcbd:      	movq	%rbx, %rax
 3e6bcc0:      	jmp	0x3e6bcfd <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x57d>
 3e6bcc2:      	nopw	%cs:(%rax,%rax)
 3e6bccc:      	nopl	(%rax)
 3e6bcd0:      	movq	%rcx, (%rdx)
 3e6bcd3:      	movaps	0x10(%rsp), %xmm0
 3e6bcd8:      	movups	%xmm0, 0x8(%rdx)
 3e6bcdc:      	movq	0x20(%rsp), %rax
 3e6bce1:      	movq	%rax, 0x18(%rdx)
 3e6bce5:      	addq	$0x20, %r13
 3e6bce9:      	addq	$0x20, %rbp
 3e6bced:      	movq	%r15, %rax
 3e6bcf0:      	cmpq	$0x200, %r13            # imm = 0x200
 3e6bcf7:      	je	0x3e6beb8 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x738>
 3e6bcfd:      	leaq	(%rbx,%r13), %r15
 3e6bd01:      	movq	(%rbx,%r13), %rcx
 3e6bd05:      	cmpq	(%rbx), %rcx
 3e6bd08:      	jae	0x3e6bd50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x5d0>
 3e6bd0a:      	movups	(%r15), %xmm0
 3e6bd0e:      	movups	0x10(%r15), %xmm1
 3e6bd13:      	movaps	%xmm1, 0x20(%rsp)
 3e6bd18:      	movaps	%xmm0, 0x10(%rsp)
 3e6bd1d:      	cmpq	$0x21, %r13
 3e6bd21:      	jb	0x3e6bd9e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x61e>
 3e6bd23:      	movq	%rsi, %rdi
 3e6bd26:      	movq	%rbx, %rsi
 3e6bd29:      	movq	%r13, %rdx
 3e6bd2c:      	callq	0x828abc0 <memmove@plt>
 3e6bd31:      	leaq	0x20(%rbx), %rsi
 3e6bd35:      	movaps	0x10(%rsp), %xmm0
 3e6bd3a:      	movaps	0x20(%rsp), %xmm1
 3e6bd3f:      	movups	%xmm1, 0x10(%rbx)
 3e6bd43:      	movups	%xmm0, (%rbx)
 3e6bd46:      	jmp	0x3e6bce5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x565>
 3e6bd48:      	nopl	(%rax,%rax)
 3e6bd50:      	movq	0x38(%rax), %rdx
 3e6bd54:      	movq	%rdx, 0x20(%rsp)
 3e6bd59:      	movups	0x28(%rax), %xmm0
 3e6bd5d:      	movaps	%xmm0, 0x10(%rsp)
 3e6bd62:      	movq	%r15, %rdx
 3e6bd65:      	cmpq	(%rax), %rcx
 3e6bd68:      	jae	0x3e6bcd0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x550>
 3e6bd6e:      	movq	%rbp, %rdx
 3e6bd71:      	nopw	%cs:(%rax,%rax)
 3e6bd7b:      	nopl	(%rax,%rax)
 3e6bd80:      	movups	-0x20(%rdx), %xmm0
 3e6bd84:      	movups	-0x10(%rdx), %xmm1
 3e6bd88:      	movups	%xmm1, 0x10(%rdx)
 3e6bd8c:      	movups	%xmm0, (%rdx)
 3e6bd8f:      	cmpq	-0x40(%rdx), %rcx
 3e6bd93:      	leaq	-0x20(%rdx), %rdx
 3e6bd97:      	jb	0x3e6bd80 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x600>
 3e6bd99:      	jmp	0x3e6bcd0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x550>
 3e6bd9e:      	movups	(%rbx), %xmm0
 3e6bda1:      	movups	0x10(%rbx), %xmm1
 3e6bda5:      	movups	%xmm1, 0x30(%rax)
 3e6bda9:      	movups	%xmm0, 0x20(%rax)
 3e6bdad:      	jmp	0x3e6bd35 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x5b5>
 3e6bdaf:      	cmpq	%r12, %rsi
 3e6bdb2:      	je	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bdb8:      	movq	%rbx, %rdi
 3e6bdbb:      	jmp	0x3e6bde5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x665>
 3e6bdbd:      	nopl	(%rax)
 3e6bdc0:      	movq	%rax, (%rcx)
 3e6bdc3:      	movaps	0x10(%rsp), %xmm0
 3e6bdc8:      	movups	%xmm0, 0x8(%rcx)
 3e6bdcc:      	movq	0x20(%rsp), %rax
 3e6bdd1:      	movq	%rax, 0x18(%rcx)
 3e6bdd5:      	leaq	0x20(%r13), %rsi
 3e6bdd9:      	movq	%r13, %rdi
 3e6bddc:      	cmpq	%r12, %rsi
 3e6bddf:      	je	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6bde5:      	movq	%rsi, %r13
 3e6bde8:      	movq	(%rsi), %rax
 3e6bdeb:      	cmpq	(%rbx), %rax
 3e6bdee:      	jae	0x3e6be50 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6d0>
 3e6bdf0:      	movups	(%r13), %xmm0
 3e6bdf5:      	movups	0x10(%r13), %xmm1
 3e6bdfa:      	movaps	%xmm1, 0x20(%rsp)
 3e6bdff:      	movaps	%xmm0, 0x10(%rsp)
 3e6be04:      	movq	%r13, %rdx
 3e6be07:      	subq	%rbx, %rdx
 3e6be0a:      	movq	%rdx, %rax
 3e6be0d:      	sarq	$0x5, %rax
 3e6be11:      	cmpq	$0x2, %rax
 3e6be15:      	jl	0x3e6be9e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x71e>
 3e6be1b:      	shlq	$0x5, %rax
 3e6be1f:      	subq	%rax, %rdi
 3e6be22:      	addq	$0x40, %rdi
 3e6be26:      	movq	%rbx, %rsi
 3e6be29:      	callq	0x828abc0 <memmove@plt>
 3e6be2e:      	movaps	0x10(%rsp), %xmm0
 3e6be33:      	movaps	0x20(%rsp), %xmm1
 3e6be38:      	movups	%xmm1, 0x10(%rbx)
 3e6be3c:      	movups	%xmm0, (%rbx)
 3e6be3f:      	leaq	0x20(%r13), %rsi
 3e6be43:      	movq	%r13, %rdi
 3e6be46:      	cmpq	%r12, %rsi
 3e6be49:      	jne	0x3e6bde5 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x665>
 3e6be4b:      	jmp	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6be50:      	movq	0x38(%rdi), %rcx
 3e6be54:      	movq	%rcx, 0x20(%rsp)
 3e6be59:      	movups	0x28(%rdi), %xmm0
 3e6be5d:      	movaps	%xmm0, 0x10(%rsp)
 3e6be62:      	movq	%r13, %rcx
 3e6be65:      	cmpq	(%rdi), %rax
 3e6be68:      	jae	0x3e6bdc0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x640>
 3e6be6e:      	movq	%r13, %rcx
 3e6be71:      	nopw	%cs:(%rax,%rax)
 3e6be7b:      	nopl	(%rax,%rax)
 3e6be80:      	movups	-0x20(%rcx), %xmm0
 3e6be84:      	movups	-0x10(%rcx), %xmm1
 3e6be88:      	movups	%xmm1, 0x10(%rcx)
 3e6be8c:      	movups	%xmm0, (%rcx)
 3e6be8f:      	cmpq	-0x40(%rcx), %rax
 3e6be93:      	leaq	-0x20(%rcx), %rcx
 3e6be97:      	jb	0x3e6be80 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x700>
 3e6be99:      	jmp	0x3e6bdc0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x640>
 3e6be9e:      	cmpq	$0x20, %rdx
 3e6bea2:      	jne	0x3e6be2e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6ae>
 3e6bea4:      	movups	(%rbx), %xmm0
 3e6bea7:      	movups	0x10(%rbx), %xmm1
 3e6beab:      	movups	%xmm1, 0x30(%rdi)
 3e6beaf:      	movups	%xmm0, 0x20(%rdi)
 3e6beb3:      	jmp	0x3e6be2e <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x6ae>
 3e6beb8:      	addq	$0x200, %rbx            # imm = 0x200
 3e6bebf:      	jmp	0x3e6bee9 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x769>
 3e6bec1:      	nopw	%cs:(%rax,%rax)
 3e6becb:      	nopl	(%rax,%rax)
 3e6bed0:      	movq	%rax, (%rcx)
 3e6bed3:      	movaps	0x10(%rsp), %xmm0
 3e6bed8:      	movups	%xmm0, 0x8(%rcx)
 3e6bedc:      	movq	0x20(%rsp), %rax
 3e6bee1:      	movq	%rax, 0x18(%rcx)
 3e6bee5:      	addq	$0x20, %rbx
 3e6bee9:      	cmpq	%r12, %rbx
 3e6beec:      	je	0x3e6bf2b <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x7ab>
 3e6beee:      	movq	(%rbx), %rax
 3e6bef1:      	movq	0x18(%rbx), %rcx
 3e6bef5:      	movq	%rcx, 0x20(%rsp)
 3e6befa:      	movups	0x8(%rbx), %xmm0
 3e6befe:      	movaps	%xmm0, 0x10(%rsp)
 3e6bf03:      	movq	%rbx, %rcx
 3e6bf06:      	cmpq	-0x20(%rbx), %rax
 3e6bf0a:      	jae	0x3e6bed0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x750>
 3e6bf0c:      	movq	%rbx, %rcx
 3e6bf0f:      	nop
 3e6bf10:      	movups	-0x20(%rcx), %xmm0
 3e6bf14:      	movups	-0x10(%rcx), %xmm1
 3e6bf18:      	movups	%xmm1, 0x10(%rcx)
 3e6bf1c:      	movups	%xmm0, (%rcx)
 3e6bf1f:      	cmpq	-0x40(%rcx), %rax
 3e6bf23:      	leaq	-0x20(%rcx), %rcx
 3e6bf27:      	jb	0x3e6bf10 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x790>
 3e6bf29:      	jmp	0x3e6bed0 <_ZN4llvm20MCPseudoProbeDecoder21buildGUID2FuncDescMapEPKhmb+0x750>
 3e6bf2b:      	movl	%r14d, %eax
 3e6bf2e:      	addq	$0x68, %rsp
 3e6bf32:      	popq	%rbx
 3e6bf33:      	popq	%r12
 3e6bf35:      	popq	%r13
 3e6bf37:      	popq	%r14
 3e6bf39:      	popq	%r15
 3e6bf3b:      	popq	%rbp
 3e6bf3c:      	retq
 3e6bf3d:      	leaq	-0x31d155a(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 3e6bf44:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
