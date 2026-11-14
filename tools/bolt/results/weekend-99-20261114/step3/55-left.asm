
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005303b10 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE>:
 5303b10:      	pushq	%rbp
 5303b11:      	pushq	%r15
 5303b13:      	pushq	%r14
 5303b15:      	pushq	%r13
 5303b17:      	pushq	%r12
 5303b19:      	pushq	%rbx
 5303b1a:      	subq	$0x1e8, %rsp            # imm = 0x1E8
 5303b21:      	leaq	0xe8(%rsp), %rax
 5303b29:      	movq	%rax, 0xd8(%rsp)
 5303b31:      	movabsq	$0x2000000000, %rax     # imm = 0x2000000000
 5303b3b:      	movq	%rax, 0xe0(%rsp)
 5303b43:      	leaq	0xd8(%rsp), %rcx
 5303b4b:      	movq	%rdi, (%rsp)
 5303b4f:      	movl	$0x1, %edx
 5303b54:      	callq	0x5303a80 <_ZN4llvm8coverage24CounterExpressionBuilder12extractTermsENS0_7CounterEiRNS_15SmallVectorImplINS1_4TermEEE>
 5303b59:      	movl	0xe0(%rsp), %r14d
 5303b61:      	movq	0xd8(%rsp), %rbx
 5303b69:      	testq	%r14, %r14
 5303b6c:      	je	0x5303bbd <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xad>
 5303b6e:      	leaq	(%rbx,%r14,8), %r15
 5303b72:      	bsrq	%r14, %rdx
 5303b76:      	xorl	$0x3f, %edx
 5303b79:      	addl	%edx, %edx
 5303b7b:      	xorq	$0x7e, %rdx
 5303b7f:      	movq	%rbx, %rdi
 5303b82:      	movq	%r15, %rsi
 5303b85:      	callq	0x5316080 <_ZSt16__introsort_loopIPN4llvm8coverage24CounterExpressionBuilder4TermElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS2_8simplifyENS1_7CounterEE3$_0EEEvT_SB_T0_T1_>
 5303b8a:      	leaq	0x8(%rbx), %r12
 5303b8e:      	cmpl	$0x11, %r14d
 5303b92:      	movq	%rbx, 0x8(%rsp)
 5303b97:      	jb	0x5303bc8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb8>
 5303b99:      	movq	%r15, 0x20(%rsp)
 5303b9e:      	shlq	$0x3, %r14
 5303ba2:      	movq	%r14, 0x18(%rsp)
 5303ba7:      	movl	$0x8, %r13d
 5303bad:      	movq	%r12, %r14
 5303bb0:      	movq	%rbx, %rbp
 5303bb3:      	movq	0x8(%rsp), %r15
 5303bb8:      	jmp	0x5303c94 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x184>
 5303bbd:      	xorl	%r15d, %r15d
 5303bc0:      	xorl	%r13d, %r13d
 5303bc3:      	jmp	0x5304715 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 5303bc8:      	cmpl	$0x1, %r14d
 5303bcc:      	je	0x5303dd2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303bd2:      	movq	0x8(%rsp), %rbx
 5303bd7:      	jmp	0x5303c19 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x109>
 5303bd9:      	nopl	(%rax)
 5303be0:      	movq	%rbx, %rdx
 5303be3:      	subq	%r12, %rdx
 5303be6:      	movq	%rdx, %rax
 5303be9:      	sarq	$0x3, %rax
 5303bed:      	cmpq	$0x2, %rax
 5303bf1:      	jl	0x5303c53 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x143>
 5303bf3:      	shlq	$0x3, %rax
 5303bf7:      	subq	%rax, %rdi
 5303bfa:      	addq	$0x10, %rdi
 5303bfe:      	movq	%r12, %rsi
 5303c01:      	callq	0x828ac50 <memmove@plt>
 5303c06:      	movq	%r12, %rax
 5303c09:      	movq	%r14, (%rax)
 5303c0c:      	leaq	0x8(%rbx), %r12
 5303c10:      	cmpq	%r15, %r12
 5303c13:      	je	0x5303dd2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303c19:      	movq	%rbx, %rdi
 5303c1c:      	movq	%r12, %rbx
 5303c1f:      	movl	(%r12), %eax
 5303c23:      	movq	(%r12), %r14
 5303c27:      	movq	0x8(%rsp), %r12
 5303c2c:      	cmpl	(%r12), %eax
 5303c30:      	jb	0x5303be0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xd0>
 5303c32:      	movq	%rbx, %rax
 5303c35:      	cmpl	%r14d, (%rdi)
 5303c38:      	jbe	0x5303c09 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303c3a:      	movq	%rbx, %rax
 5303c3d:      	nopl	(%rax)
 5303c40:      	movq	-0x8(%rax), %rcx
 5303c44:      	movq	%rcx, (%rax)
 5303c47:      	cmpl	%r14d, -0x10(%rax)
 5303c4b:      	leaq	-0x8(%rax), %rax
 5303c4f:      	ja	0x5303c40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x130>
 5303c51:      	jmp	0x5303c09 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303c53:      	movq	%r12, %rax
 5303c56:      	cmpq	$0x8, %rdx
 5303c5a:      	jne	0x5303c09 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303c5c:      	movq	0x8(%rsp), %rcx
 5303c61:      	movq	(%rcx), %rax
 5303c64:      	movq	%rax, 0x8(%rdi)
 5303c68:      	movq	%rcx, %rax
 5303c6b:      	jmp	0x5303c09 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303c6d:      	movq	0x8(%rsp), %rdx
 5303c72:      	movq	(%rdx), %rcx
 5303c75:      	movq	%rcx, 0x8(%rax)
 5303c79:      	movq	%rdx, %rcx
 5303c7c:      	nopl	(%rax)
 5303c80:      	movq	%rbx, (%rcx)
 5303c83:      	addq	$0x8, %r13
 5303c87:      	addq	$0x8, %r14
 5303c8b:      	cmpq	$0x80, %r13
 5303c92:      	je	0x5303cf2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1e2>
 5303c94:      	movq	%rbp, %rax
 5303c97:      	movq	0x8(%rsp), %rdx
 5303c9c:      	leaq	(%rdx,%r13), %rbp
 5303ca0:      	movl	(%rdx,%r13), %ecx
 5303ca4:      	movq	(%rdx,%r13), %rbx
 5303ca8:      	cmpl	(%rdx), %ecx
 5303caa:      	jae	0x5303cd0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1c0>
 5303cac:      	cmpq	$0x9, %r13
 5303cb0:      	jb	0x5303c6d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x15d>
 5303cb2:      	movq	%r12, %rdi
 5303cb5:      	movq	%r15, %rsi
 5303cb8:      	movq	%r13, %rdx
 5303cbb:      	callq	0x828ac50 <memmove@plt>
 5303cc0:      	movq	%r15, %rcx
 5303cc3:      	jmp	0x5303c80 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303cc5:      	nopw	%cs:(%rax,%rax)
 5303ccf:      	nop
 5303cd0:      	movq	%rbp, %rcx
 5303cd3:      	cmpl	%ebx, (%rax)
 5303cd5:      	jbe	0x5303c80 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303cd7:      	movq	%r14, %rcx
 5303cda:      	nopw	(%rax,%rax)
 5303ce0:      	movq	-0x8(%rcx), %rax
 5303ce4:      	movq	%rax, (%rcx)
 5303ce7:      	cmpl	%ebx, -0x10(%rcx)
 5303cea:      	leaq	-0x8(%rcx), %rcx
 5303cee:      	ja	0x5303ce0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1d0>
 5303cf0:      	jmp	0x5303c80 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303cf2:      	movq	0x8(%rsp), %rsi
 5303cf7:      	leaq	0x80(%rsi), %rax
 5303cfe:      	movq	0x18(%rsp), %rdi
 5303d03:      	addq	$-0x88, %rdi
 5303d0a:      	testb	$0x8, %dil
 5303d0e:      	jne	0x5303d54 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x244>
 5303d10:      	movq	0x80(%rsi), %rcx
 5303d17:      	cmpl	%ecx, 0x78(%rsi)
 5303d1a:      	movq	0x20(%rsp), %r8
 5303d1f:      	jbe	0x5303d40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x230>
 5303d21:      	nopw	%cs:(%rax,%rax)
 5303d2b:      	nopl	(%rax,%rax)
 5303d30:      	movq	-0x8(%rax), %rdx
 5303d34:      	movq	%rdx, (%rax)
 5303d37:      	cmpl	%ecx, -0x10(%rax)
 5303d3a:      	leaq	-0x8(%rax), %rax
 5303d3e:      	ja	0x5303d30 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x220>
 5303d40:      	movq	%rcx, (%rax)
 5303d43:      	addq	$0x88, %rsi
 5303d4a:      	movq	%rsi, %rax
 5303d4d:      	testq	%rdi, %rdi
 5303d50:      	jne	0x5303d5e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x24e>
 5303d52:      	jmp	0x5303dd2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303d54:      	movq	0x20(%rsp), %r8
 5303d59:      	testq	%rdi, %rdi
 5303d5c:      	je	0x5303dd2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303d5e:      	leaq	0x8(%rax), %rcx
 5303d62:      	jmp	0x5303d84 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x274>
 5303d64:      	nopw	%cs:(%rax,%rax)
 5303d6e:      	nop
 5303d70:      	leaq	0x8(%rax), %rsi
 5303d74:      	movq	%rdx, (%rsi)
 5303d77:      	addq	$0x10, %rax
 5303d7b:      	addq	$0x10, %rcx
 5303d7f:      	cmpq	%r8, %rax
 5303d82:      	je	0x5303dd2 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303d84:      	movq	(%rax), %rdx
 5303d87:      	movq	%rax, %rsi
 5303d8a:      	cmpl	%edx, -0x8(%rax)
 5303d8d:      	jbe	0x5303db0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2a0>
 5303d8f:      	movq	%rax, %rsi
 5303d92:      	nopw	%cs:(%rax,%rax)
 5303d9c:      	nopl	(%rax)
 5303da0:      	movq	-0x8(%rsi), %rdi
 5303da4:      	movq	%rdi, (%rsi)
 5303da7:      	cmpl	%edx, -0x10(%rsi)
 5303daa:      	leaq	-0x8(%rsi), %rsi
 5303dae:      	ja	0x5303da0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x290>
 5303db0:      	movq	%rdx, (%rsi)
 5303db3:      	movq	0x8(%rax), %rdx
 5303db7:      	cmpl	%edx, (%rax)
 5303db9:      	jbe	0x5303d70 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x260>
 5303dbb:      	movq	%rcx, %rsi
 5303dbe:      	nop
 5303dc0:      	movq	-0x8(%rsi), %rdi
 5303dc4:      	movq	%rdi, (%rsi)
 5303dc7:      	cmpl	%edx, -0x10(%rsi)
 5303dca:      	leaq	-0x8(%rsi), %rsi
 5303dce:      	ja	0x5303dc0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2b0>
 5303dd0:      	jmp	0x5303d74 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x264>
 5303dd2:      	movq	0xd8(%rsp), %rbx
 5303dda:      	movl	0xe0(%rsp), %esi
 5303de1:      	movq	%rbx, %rax
 5303de4:      	cmpq	$0x1, %rsi
 5303de8:      	jne	0x530429b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x78b>
 5303dee:      	subq	%rbx, %rax
 5303df1:      	addq	$0x8, %rax
 5303df5:      	movq	%rax, %rcx
 5303df8:      	shrq	$0x3, %rcx
 5303dfc:      	movl	%ecx, 0xe0(%rsp)
 5303e03:      	movabsq	$0x7fffffff8, %rdx      # imm = 0x7FFFFFFF8
 5303e0d:      	andq	%rax, %rdx
 5303e10:      	je	0x53042ce <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7be>
 5303e16:      	addq	%rbx, %rdx
 5303e19:      	movq	(%rsp), %r8
 5303e1d:      	leaq	0x18(%r8), %rax
 5303e21:      	movq	%rax, 0x40(%rsp)
 5303e26:      	xorl	%r13d, %r13d
 5303e29:      	xorl	%r15d, %r15d
 5303e2c:      	movq	%rdx, 0x48(%rsp)
 5303e31:      	jmp	0x5303e57 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x347>
 5303e33:      	nopw	%cs:(%rax,%rax)
 5303e3d:      	nopl	(%rax)
 5303e40:      	movq	0x8(%rsp), %rbx
 5303e45:      	addq	$0x8, %rbx
 5303e49:      	movq	0x48(%rsp), %rdx
 5303e4e:      	cmpq	%rdx, %rbx
 5303e51:      	je	0x5304283 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x773>
 5303e57:      	movl	0x4(%rbx), %r9d
 5303e5b:      	testl	%r9d, %r9d
 5303e5e:      	movq	%rbx, 0x8(%rsp)
 5303e63:      	jle	0x5303e40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 5303e65:      	movl	(%rbx), %r10d
 5303e68:      	movq	%r10, %rax
 5303e6b:      	shlq	$0x20, %rax
 5303e6f:      	incq	%rax
 5303e72:      	movq	%rax, 0x20(%rsp)
 5303e77:      	xorl	%r14d, %r14d
 5303e7a:      	movl	%r9d, 0x18(%rsp)
 5303e7f:      	movq	%r10, 0x10(%rsp)
 5303e84:      	jmp	0x5303f60 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 5303e89:      	nopl	(%rax)
 5303e90:      	movl	%eax, %esi
 5303e92:      	leaq	(%rsi,%rsi,2), %rsi
 5303e96:      	leaq	(%r11,%rsi,8), %r12
 5303e9a:      	movl	(%r11,%rsi,8), %esi
 5303e9e:      	cmpl	$0x1, %esi
 5303ea1:      	jne	0x5303ef4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3e4>
 5303ea3:      	movl	0x4(%r12), %esi
 5303ea8:      	movl	0x8(%r12), %edi
 5303ead:      	cmpl	%esi, %r13d
 5303eb0:      	movl	0x18(%rsp), %r9d
 5303eb5:      	movq	0x10(%rsp), %r10
 5303eba:      	jne	0x5303ed4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303ebc:      	cmpl	%edi, %r15d
 5303ebf:      	jne	0x5303ed4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303ec1:      	cmpl	$0x1, 0xc(%r12)
 5303ec7:      	jne	0x5303ed4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303ec9:      	cmpl	0x10(%r12), %r10d
 5303ece:      	je	0x53041e0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6d0>
 5303ed4:      	xorl	$0x1, %esi
 5303ed7:      	notl	%edi
 5303ed9:      	orl	%esi, %edi
 5303edb:      	jne	0x5303f28 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x418>
 5303edd:      	movl	0xc(%r12), %esi
 5303ee2:      	movl	0x10(%r12), %edi
 5303ee7:      	xorl	$0x1, %esi
 5303eea:      	notl	%edi
 5303eec:      	orl	%esi, %edi
 5303eee:      	sete	%sil
 5303ef2:      	jmp	0x5303f2a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303ef4:      	testl	%esi, %esi
 5303ef6:      	movl	0x18(%rsp), %r9d
 5303efb:      	movq	0x10(%rsp), %r10
 5303f00:      	jne	0x5303f28 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x418>
 5303f02:      	xorl	%esi, %esi
 5303f04:      	cmpl	$0x1, 0x4(%r12)
 5303f0a:      	jne	0x5303f2a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303f0c:      	cmpl	$-0x1, 0x8(%r12)
 5303f12:      	jne	0x5303f2a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303f14:      	xorl	%esi, %esi
 5303f16:      	cmpl	$0x1, 0xc(%r12)
 5303f1c:      	jne	0x5303f2a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303f1e:      	cmpl	$-0x1, 0x10(%r12)
 5303f24:      	je	0x5303f43 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x433>
 5303f26:      	jmp	0x5303f2a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303f28:      	xorl	%esi, %esi
 5303f2a:      	testq	%rcx, %rcx
 5303f2d:      	cmovneq	%rcx, %r12
 5303f31:      	testb	%sil, %sil
 5303f34:      	cmovneq	%r12, %rcx
 5303f38:      	addl	%edx, %eax
 5303f3a:      	incl	%edx
 5303f3c:      	andl	%ebx, %eax
 5303f3e:      	jmp	0x5303e90 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x380>
 5303f43:      	testq	%rcx, %rcx
 5303f46:      	cmovneq	%rcx, %r12
 5303f4a:      	movl	0x28(%r8), %esi
 5303f4e:      	jmp	0x5304055 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x545>
 5303f53:      	nopw	%cs:(%rax,%rax)
 5303f5d:      	nopl	(%rax)
 5303f60:      	testl	%r13d, %r13d
 5303f63:      	je	0x5304030 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x520>
 5303f69:      	movq	%r15, %rax
 5303f6c:      	shlq	$0x20, %rax
 5303f70:      	movl	%r13d, %ecx
 5303f73:      	orq	%rax, %rcx
 5303f76:      	movl	$0x1, 0x2c(%rsp)
 5303f7e:      	movq	%rcx, 0x30(%rsp)
 5303f83:      	movq	0x20(%rsp), %rax
 5303f88:      	movq	%rax, 0x38(%rsp)
 5303f8d:      	movq	0x8(%r8), %rbp
 5303f91:      	subq	(%r8), %rbp
 5303f94:      	movl	0x28(%r8), %ebx
 5303f98:      	testl	%ebx, %ebx
 5303f9a:      	je	0x5304050 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x540>
 5303fa0:      	movq	0x18(%r8), %r12
 5303fa4:      	leaq	0x98(%rsp), %rcx
 5303fac:      	xorps	%xmm0, %xmm0
 5303faf:      	movups	%xmm0, 0x20(%rcx)
 5303fb3:      	movups	%xmm0, 0x10(%rcx)
 5303fb7:      	movups	%xmm0, (%rcx)
 5303fba:      	movups	%xmm0, -0x10(%rcx)
 5303fbe:      	movups	%xmm0, -0x20(%rcx)
 5303fc2:      	movups	%xmm0, -0x30(%rcx)
 5303fc6:      	movq	$0x0, 0x30(%rcx)
 5303fce:      	movabsq	$-0xae502812aa7333, %rax # imm = 0xFF51AFD7ED558CCD
 5303fd8:      	movq	%rax, 0xd0(%rsp)
 5303fe0:      	movl	$0x1, 0x58(%rsp)
 5303fe8:      	movl	%r13d, 0x5c(%rsp)
 5303fed:      	movl	%r15d, 0x60(%rsp)
 5303ff2:      	movl	$0x1, 0x64(%rsp)
 5303ffa:      	movl	%r10d, 0x68(%rsp)
 5303fff:      	leaq	0x58(%rsp), %rdi
 5304004:      	xorl	%esi, %esi
 5304006:      	leaq	0x6c(%rsp), %rdx
 530400b:      	callq	0x2ac8df0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 5304010:      	movq	%r12, %r11
 5304013:      	movq	(%rsp), %r8
 5304017:      	decl	%ebx
 5304019:      	andl	%ebx, %eax
 530401b:      	movl	$0x1, %edx
 5304020:      	xorl	%ecx, %ecx
 5304022:      	jmp	0x5303e90 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x380>
 5304027:      	nopw	(%rax,%rax)
 5304030:      	movl	$0x1, %r13d
 5304036:      	movl	%r10d, %r15d
 5304039:      	incl	%r14d
 530403c:      	cmpl	%r9d, %r14d
 530403f:      	jne	0x5303f60 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 5304045:      	jmp	0x5303e40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 530404a:      	nopw	(%rax,%rax)
 5304050:      	xorl	%esi, %esi
 5304052:      	xorl	%r12d, %r12d
 5304055:      	movq	%r12, 0x58(%rsp)
 530405a:      	movl	0x20(%r8), %eax
 530405e:      	leal	0x4(,%rax,4), %ecx
 5304065:      	leal	(%rsi,%rsi,2), %edx
 5304068:      	cmpl	%edx, %ecx
 530406a:      	jae	0x53041fc <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6ec>
 5304070:      	movl	%eax, %ecx
 5304072:      	notl	%ecx
 5304074:      	addl	%esi, %ecx
 5304076:      	subl	0x24(%r8), %ecx
 530407a:      	movl	%esi, %edx
 530407c:      	shrl	$0x3, %edx
 530407f:      	cmpl	%edx, %ecx
 5304081:      	jbe	0x53041fe <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6ee>
 5304087:      	incl	%eax
 5304089:      	movl	%eax, 0x20(%r8)
 530408d:      	cmpl	$0x0, (%r12)
 5304092:      	je	0x530424e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x73e>
 5304098:      	decl	0x24(%r8)
 530409c:      	sarq	$0x2, %rbp
 53040a0:      	movabsq	$-0x3333333333333333, %rax # imm = 0xCCCCCCCCCCCCCCCD
 53040aa:      	imulq	%rax, %rbp
 53040ae:      	movl	0x3c(%rsp), %eax
 53040b2:      	movl	%eax, 0x10(%r12)
 53040b7:      	movups	0x2c(%rsp), %xmm0
 53040bc:      	movups	%xmm0, (%r12)
 53040c1:      	movl	%ebp, 0x14(%r12)
 53040c6:      	movq	0x8(%r8), %rbx
 53040ca:      	cmpq	0x10(%r8), %rbx
 53040ce:      	je	0x53040e9 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x5d9>
 53040d0:      	movl	0x3c(%rsp), %eax
 53040d4:      	movl	%eax, 0x10(%rbx)
 53040d7:      	movups	0x2c(%rsp), %xmm0
 53040dc:      	movups	%xmm0, (%rbx)
 53040df:      	addq	$0x14, 0x8(%r8)
 53040e4:      	jmp	0x53041e0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6d0>
 53040e9:      	movq	(%r8), %rbp
 53040ec:      	movq	%rbx, %r13
 53040ef:      	subq	%rbp, %r13
 53040f2:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 53040fc:      	cmpq	%rax, %r13
 53040ff:      	je	0x53047cd <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcbd>
 5304105:      	movq	%r13, %rax
 5304108:      	sarq	$0x2, %rax
 530410c:      	movabsq	$-0x3333333333333333, %rcx # imm = 0xCCCCCCCCCCCCCCCD
 5304116:      	imulq	%rcx, %rax
 530411a:      	cmpq	$0x1, %rax
 530411e:      	movq	%rax, %rcx
 5304121:      	adcq	$0x0, %rcx
 5304125:      	leaq	(%rcx,%rax), %rsi
 5304129:      	movabsq	$0x666666666666666, %rdx # imm = 0x666666666666666
 5304133:      	cmpq	%rdx, %rsi
 5304136:      	cmovaeq	%rdx, %rsi
 530413a:      	addq	%rax, %rcx
 530413d:      	cmovbq	%rdx, %rsi
 5304141:      	movq	%rsi, 0x50(%rsp)
 5304146:      	leaq	(,%rsi,4), %rax
 530414e:      	leaq	(%rax,%rax,4), %rdi
 5304152:      	callq	0x828a6b0 <_Znwm@plt>
 5304157:      	movq	%rax, %rdx
 530415a:      	movups	0x2c(%rsp), %xmm0
 530415f:      	movups	%xmm0, (%rax,%r13)
 5304164:      	movl	0x3c(%rsp), %eax
 5304168:      	movl	%eax, 0x10(%rdx,%r13)
 530416d:      	movq	%rdx, %r15
 5304170:      	cmpq	%rbx, %rbp
 5304173:      	je	0x530419b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x68b>
 5304175:      	movq	%rdx, %r15
 5304178:      	movq	%rbp, %rax
 530417b:      	nopl	(%rax,%rax)
 5304180:      	movl	0x10(%rax), %ecx
 5304183:      	movl	%ecx, 0x10(%r15)
 5304187:      	movups	(%rax), %xmm0
 530418a:      	movups	%xmm0, (%r15)
 530418e:      	addq	$0x14, %rax
 5304192:      	addq	$0x14, %r15
 5304196:      	cmpq	%rbx, %rax
 5304199:      	jne	0x5304180 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x670>
 530419b:      	testq	%rbp, %rbp
 530419e:      	je	0x53041b1 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6a1>
 53041a0:      	movq	%rbp, %rdi
 53041a3:      	movq	%r13, %rsi
 53041a6:      	movq	%rdx, %rbx
 53041a9:      	callq	0x828a6f0 <_ZdlPvm@plt>
 53041ae:      	movq	%rbx, %rdx
 53041b1:      	addq	$0x14, %r15
 53041b5:      	movq	(%rsp), %r8
 53041b9:      	movq	%rdx, (%r8)
 53041bc:      	movq	%r15, 0x8(%r8)
 53041c0:      	movq	0x50(%rsp), %rax
 53041c5:      	leaq	(%rax,%rax,4), %rax
 53041c9:      	leaq	(%rdx,%rax,4), %rax
 53041cd:      	movq	%rax, 0x10(%r8)
 53041d1:      	movl	0x18(%rsp), %r9d
 53041d6:      	movq	0x10(%rsp), %r10
 53041db:      	nopl	(%rax,%rax)
 53041e0:      	movl	0x14(%r12), %r15d
 53041e5:      	movl	$0x2, %r13d
 53041eb:      	incl	%r14d
 53041ee:      	cmpl	%r9d, %r14d
 53041f1:      	jne	0x5303f60 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 53041f7:      	jmp	0x5303e40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 53041fc:      	addl	%esi, %esi
 53041fe:      	movq	0x40(%rsp), %rdi
 5304203:      	callq	0x5315da0 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E4growEj>
 5304208:      	movq	(%rsp), %rax
 530420c:      	movq	0x18(%rax), %rdi
 5304210:      	movq	(%rsp), %rax
 5304214:      	movl	0x28(%rax), %esi
 5304217:      	leaq	0x2c(%rsp), %rdx
 530421c:      	leaq	0x58(%rsp), %rcx
 5304221:      	callq	0x5315c30 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E15LookupBucketForIS3_EEbRKT_RPS8_>
 5304226:      	movq	0x10(%rsp), %r10
 530422b:      	movl	0x18(%rsp), %r9d
 5304230:      	movq	(%rsp), %r8
 5304234:      	movl	0x20(%r8), %eax
 5304238:      	movq	0x58(%rsp), %r12
 530423d:      	incl	%eax
 530423f:      	movl	%eax, 0x20(%r8)
 5304243:      	cmpl	$0x0, (%r12)
 5304248:      	jne	0x5304098 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 530424e:      	cmpl	$0x1, 0x4(%r12)
 5304254:      	jne	0x5304098 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 530425a:      	cmpl	$-0x1, 0x8(%r12)
 5304260:      	jne	0x5304098 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 5304266:      	cmpl	$0x1, 0xc(%r12)
 530426c:      	jne	0x5304098 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 5304272:      	cmpl	$-0x1, 0x10(%r12)
 5304278:      	je	0x530409c <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x58c>
 530427e:      	jmp	0x5304098 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 5304283:      	movq	0xd8(%rsp), %rbx
 530428b:      	movl	0xe0(%rsp), %ecx
 5304292:      	testl	%ecx, %ecx
 5304294:      	jne	0x53042e0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7d0>
 5304296:      	jmp	0x5304715 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 530429b:      	leaq	0x8(%rbx), %rdx
 530429f:      	movl	(%rbx), %ecx
 53042a1:      	testb	$0x1, %sil
 53042a5:      	jne	0x5304746 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc36>
 53042ab:      	cmpl	%ecx, (%rdx)
 53042ad:      	jne	0x530475a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc4a>
 53042b3:      	movl	0xc(%rbx), %eax
 53042b6:      	addl	%eax, 0x4(%rbx)
 53042b9:      	movq	%rbx, %rax
 53042bc:      	leaq	0x10(%rbx), %r8
 53042c0:      	cmpl	$0x2, %esi
 53042c3:      	jne	0x530476e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc5e>
 53042c9:      	jmp	0x5303dee <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 53042ce:      	xorl	%r15d, %r15d
 53042d1:      	xorl	%r13d, %r13d
 53042d4:      	movq	(%rsp), %r8
 53042d8:      	testl	%ecx, %ecx
 53042da:      	je	0x5304715 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 53042e0:      	movl	%ecx, %eax
 53042e2:      	leaq	(%rbx,%rax,8), %rax
 53042e6:      	leaq	0x18(%r8), %rcx
 53042ea:      	movq	%rcx, 0x40(%rsp)
 53042ef:      	movq	%rax, 0x48(%rsp)
 53042f4:      	jmp	0x530431d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x80d>
 53042f6:      	nopw	%cs:(%rax,%rax)
 5304300:      	movl	$0x2, %r13d
 5304306:      	movq	0x8(%rsp), %rbx
 530430b:      	movq	0x48(%rsp), %rax
 5304310:      	addq	$0x8, %rbx
 5304314:      	cmpq	%rax, %rbx
 5304317:      	je	0x530470d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xbfd>
 530431d:      	movl	0x4(%rbx), %r9d
 5304321:      	testl	%r9d, %r9d
 5304324:      	jns	0x5304310 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x800>
 5304326:      	movq	%rbx, 0x8(%rsp)
 530432b:      	movl	(%rbx), %eax
 530432d:      	movl	%eax, 0x20(%rsp)
 5304331:      	negl	%r9d
 5304334:      	shlq	$0x20, %rax
 5304338:      	incq	%rax
 530433b:      	movq	%rax, 0x18(%rsp)
 5304340:      	movl	%r13d, %ebp
 5304343:      	cmpl	$0x2, %r9d
 5304347:      	movl	$0x1, %eax
 530434c:      	cmovll	%eax, %r9d
 5304350:      	xorl	%r14d, %r14d
 5304353:      	movl	%r9d, 0x10(%rsp)
 5304358:      	jmp	0x530442a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x91a>
 530435d:      	nopl	(%rax)
 5304360:      	movl	%eax, %esi
 5304362:      	leaq	(%rsi,%rsi,2), %rsi
 5304366:      	leaq	(%r10,%rsi,8), %r12
 530436a:      	movl	(%r10,%rsi,8), %esi
 530436e:      	testl	%esi, %esi
 5304370:      	jne	0x53043c7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8b7>
 5304372:      	movl	0x4(%r12), %r8d
 5304377:      	movl	0x8(%r12), %edi
 530437c:      	cmpl	%ebp, %r8d
 530437f:      	movl	0x10(%rsp), %r9d
 5304384:      	jne	0x530439e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 5304386:      	cmpl	%edi, %r15d
 5304389:      	jne	0x530439e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 530438b:      	cmpl	$0x1, 0xc(%r12)
 5304391:      	jne	0x530439e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 5304393:      	movl	0x20(%rsp), %esi
 5304397:      	cmpl	0x10(%r12), %esi
 530439c:      	je	0x5304410 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x900>
 530439e:      	xorl	%esi, %esi
 53043a0:      	cmpl	$0x1, %r8d
 53043a4:      	jne	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043a6:      	cmpl	$-0x1, %edi
 53043a9:      	movq	(%rsp), %r8
 53043ad:      	jne	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043af:      	xorl	%esi, %esi
 53043b1:      	cmpl	$0x1, 0xc(%r12)
 53043b7:      	jne	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043b9:      	cmpl	$-0x1, 0x10(%r12)
 53043bf:      	je	0x530467b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb6b>
 53043c5:      	jmp	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043c7:      	cmpl	$0x1, %esi
 53043ca:      	jne	0x53043f5 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e5>
 53043cc:      	xorl	%esi, %esi
 53043ce:      	cmpl	$0x1, 0x4(%r12)
 53043d4:      	jne	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043d6:      	cmpl	$-0x1, 0x8(%r12)
 53043dc:      	jne	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043de:      	movl	0xc(%r12), %esi
 53043e3:      	movl	0x10(%r12), %edi
 53043e8:      	xorl	$0x1, %esi
 53043eb:      	notl	%edi
 53043ed:      	orl	%esi, %edi
 53043ef:      	sete	%sil
 53043f3:      	jmp	0x53043f7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 53043f5:      	xorl	%esi, %esi
 53043f7:      	testq	%rcx, %rcx
 53043fa:      	cmovneq	%rcx, %r12
 53043fe:      	testb	%sil, %sil
 5304401:      	cmovneq	%r12, %rcx
 5304405:      	addl	%edx, %eax
 5304407:      	incl	%edx
 5304409:      	andl	%ebx, %eax
 530440b:      	jmp	0x5304360 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x850>
 5304410:      	movq	(%rsp), %r8
 5304414:      	movl	0x14(%r12), %r15d
 5304419:      	incl	%r14d
 530441c:      	movl	$0x2, %ebp
 5304421:      	cmpl	%r9d, %r14d
 5304424:      	je	0x5304300 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7f0>
 530442a:      	movq	%r15, %rax
 530442d:      	shlq	$0x20, %rax
 5304431:      	orq	%rbp, %rax
 5304434:      	movl	$0x0, 0x2c(%rsp)
 530443c:      	movq	%rax, 0x30(%rsp)
 5304441:      	movq	0x18(%rsp), %rax
 5304446:      	movq	%rax, 0x38(%rsp)
 530444b:      	movq	0x8(%r8), %r13
 530444f:      	subq	(%r8), %r13
 5304452:      	movl	0x28(%r8), %ebx
 5304456:      	testl	%ebx, %ebx
 5304458:      	je	0x53044f0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x9e0>
 530445e:      	movq	0x18(%r8), %r12
 5304462:      	leaq	0x98(%rsp), %rcx
 530446a:      	xorps	%xmm0, %xmm0
 530446d:      	movups	%xmm0, 0x20(%rcx)
 5304471:      	movups	%xmm0, 0x10(%rcx)
 5304475:      	movups	%xmm0, (%rcx)
 5304478:      	movups	%xmm0, -0x10(%rcx)
 530447c:      	movups	%xmm0, -0x20(%rcx)
 5304480:      	movups	%xmm0, -0x30(%rcx)
 5304484:      	movq	$0x0, 0x30(%rcx)
 530448c:      	movabsq	$-0xae502812aa7333, %rax # imm = 0xFF51AFD7ED558CCD
 5304496:      	movq	%rax, 0xd0(%rsp)
 530449e:      	movl	$0x0, 0x58(%rsp)
 53044a6:      	movl	%ebp, 0x5c(%rsp)
 53044aa:      	movl	%r15d, 0x60(%rsp)
 53044af:      	movl	$0x1, 0x64(%rsp)
 53044b7:      	movl	0x20(%rsp), %eax
 53044bb:      	movl	%eax, 0x68(%rsp)
 53044bf:      	leaq	0x58(%rsp), %rdi
 53044c4:      	xorl	%esi, %esi
 53044c6:      	leaq	0x6c(%rsp), %rdx
 53044cb:      	callq	0x2ac8df0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 53044d0:      	movq	%r12, %r10
 53044d3:      	decl	%ebx
 53044d5:      	andl	%ebx, %eax
 53044d7:      	movl	$0x1, %edx
 53044dc:      	xorl	%ecx, %ecx
 53044de:      	jmp	0x5304360 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x850>
 53044e3:      	nopw	%cs:(%rax,%rax)
 53044ed:      	nopl	(%rax)
 53044f0:      	xorl	%esi, %esi
 53044f2:      	xorl	%r12d, %r12d
 53044f5:      	movq	%r12, 0x58(%rsp)
 53044fa:      	movl	0x20(%r8), %eax
 53044fe:      	leal	0x4(,%rax,4), %ecx
 5304505:      	leal	(%rsi,%rsi,2), %edx
 5304508:      	cmpl	%edx, %ecx
 530450a:      	jae	0x530468b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb7b>
 5304510:      	movl	%eax, %ecx
 5304512:      	notl	%ecx
 5304514:      	addl	%esi, %ecx
 5304516:      	subl	0x24(%r8), %ecx
 530451a:      	movl	%esi, %edx
 530451c:      	shrl	$0x3, %edx
 530451f:      	cmpl	%edx, %ecx
 5304521:      	jbe	0x530468d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb7d>
 5304527:      	incl	%eax
 5304529:      	movl	%eax, 0x20(%r8)
 530452d:      	cmpl	$0x0, (%r12)
 5304532:      	je	0x53046d8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xbc8>
 5304538:      	decl	0x24(%r8)
 530453c:      	sarq	$0x2, %r13
 5304540:      	movabsq	$-0x3333333333333333, %rax # imm = 0xCCCCCCCCCCCCCCCD
 530454a:      	imulq	%rax, %r13
 530454e:      	movl	0x3c(%rsp), %eax
 5304552:      	movl	%eax, 0x10(%r12)
 5304557:      	movups	0x2c(%rsp), %xmm0
 530455c:      	movups	%xmm0, (%r12)
 5304561:      	movl	%r13d, 0x14(%r12)
 5304566:      	movq	0x8(%r8), %rbx
 530456a:      	cmpq	0x10(%r8), %rbx
 530456e:      	je	0x5304589 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa79>
 5304570:      	movl	0x3c(%rsp), %eax
 5304574:      	movl	%eax, 0x10(%rbx)
 5304577:      	movups	0x2c(%rsp), %xmm0
 530457c:      	movups	%xmm0, (%rbx)
 530457f:      	addq	$0x14, 0x8(%r8)
 5304584:      	jmp	0x5304414 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x904>
 5304589:      	movq	(%r8), %rbp
 530458c:      	movq	%rbx, %r13
 530458f:      	subq	%rbp, %r13
 5304592:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 530459c:      	cmpq	%rax, %r13
 530459f:      	je	0x53047cd <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcbd>
 53045a5:      	movq	%r13, %rax
 53045a8:      	sarq	$0x2, %rax
 53045ac:      	movabsq	$-0x3333333333333333, %rcx # imm = 0xCCCCCCCCCCCCCCCD
 53045b6:      	imulq	%rcx, %rax
 53045ba:      	cmpq	$0x1, %rax
 53045be:      	movq	%rax, %rcx
 53045c1:      	adcq	$0x0, %rcx
 53045c5:      	leaq	(%rcx,%rax), %rsi
 53045c9:      	movabsq	$0x666666666666666, %rdx # imm = 0x666666666666666
 53045d3:      	cmpq	%rdx, %rsi
 53045d6:      	cmovaeq	%rdx, %rsi
 53045da:      	addq	%rax, %rcx
 53045dd:      	cmovbq	%rdx, %rsi
 53045e1:      	movq	%rsi, 0x50(%rsp)
 53045e6:      	leaq	(,%rsi,4), %rax
 53045ee:      	leaq	(%rax,%rax,4), %rdi
 53045f2:      	callq	0x828a6b0 <_Znwm@plt>
 53045f7:      	movq	%rax, %rdx
 53045fa:      	movups	0x2c(%rsp), %xmm0
 53045ff:      	movups	%xmm0, (%rax,%r13)
 5304604:      	movl	0x3c(%rsp), %eax
 5304608:      	movl	%eax, 0x10(%rdx,%r13)
 530460d:      	movq	%rdx, %r15
 5304610:      	cmpq	%rbx, %rbp
 5304613:      	je	0x530463b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb2b>
 5304615:      	movq	%rdx, %r15
 5304618:      	movq	%rbp, %rax
 530461b:      	nopl	(%rax,%rax)
 5304620:      	movl	0x10(%rax), %ecx
 5304623:      	movl	%ecx, 0x10(%r15)
 5304627:      	movups	(%rax), %xmm0
 530462a:      	movups	%xmm0, (%r15)
 530462e:      	addq	$0x14, %rax
 5304632:      	addq	$0x14, %r15
 5304636:      	cmpq	%rbx, %rax
 5304639:      	jne	0x5304620 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb10>
 530463b:      	testq	%rbp, %rbp
 530463e:      	je	0x5304651 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb41>
 5304640:      	movq	%rbp, %rdi
 5304643:      	movq	%r13, %rsi
 5304646:      	movq	%rdx, %rbx
 5304649:      	callq	0x828a6f0 <_ZdlPvm@plt>
 530464e:      	movq	%rbx, %rdx
 5304651:      	addq	$0x14, %r15
 5304655:      	movq	(%rsp), %r8
 5304659:      	movq	%rdx, (%r8)
 530465c:      	movq	%r15, 0x8(%r8)
 5304660:      	movq	0x50(%rsp), %rax
 5304665:      	leaq	(%rax,%rax,4), %rax
 5304669:      	leaq	(%rdx,%rax,4), %rax
 530466d:      	movq	%rax, 0x10(%r8)
 5304671:      	movl	0x10(%rsp), %r9d
 5304676:      	jmp	0x5304414 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x904>
 530467b:      	testq	%rcx, %rcx
 530467e:      	cmovneq	%rcx, %r12
 5304682:      	movl	0x28(%r8), %esi
 5304686:      	jmp	0x53044f5 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x9e5>
 530468b:      	addl	%esi, %esi
 530468d:      	movq	0x40(%rsp), %rdi
 5304692:      	callq	0x5315da0 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E4growEj>
 5304697:      	movq	(%rsp), %rax
 530469b:      	movq	0x18(%rax), %rdi
 530469f:      	movq	(%rsp), %rax
 53046a3:      	movl	0x28(%rax), %esi
 53046a6:      	leaq	0x2c(%rsp), %rdx
 53046ab:      	leaq	0x58(%rsp), %rcx
 53046b0:      	callq	0x5315c30 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E15LookupBucketForIS3_EEbRKT_RPS8_>
 53046b5:      	movl	0x10(%rsp), %r9d
 53046ba:      	movq	(%rsp), %r8
 53046be:      	movl	0x20(%r8), %eax
 53046c2:      	movq	0x58(%rsp), %r12
 53046c7:      	incl	%eax
 53046c9:      	movl	%eax, 0x20(%r8)
 53046cd:      	cmpl	$0x0, (%r12)
 53046d2:      	jne	0x5304538 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 53046d8:      	cmpl	$0x1, 0x4(%r12)
 53046de:      	jne	0x5304538 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 53046e4:      	cmpl	$-0x1, 0x8(%r12)
 53046ea:      	jne	0x5304538 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 53046f0:      	cmpl	$0x1, 0xc(%r12)
 53046f6:      	jne	0x5304538 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 53046fc:      	cmpl	$-0x1, 0x10(%r12)
 5304702:      	je	0x530453c <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa2c>
 5304708:      	jmp	0x5304538 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 530470d:      	movq	0xd8(%rsp), %rbx
 5304715:      	leaq	0xe8(%rsp), %rax
 530471d:      	cmpq	%rax, %rbx
 5304720:      	je	0x530472a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc1a>
 5304722:      	movq	%rbx, %rdi
 5304725:      	callq	0x828a6d0 <free@plt>
 530472a:      	shlq	$0x20, %r15
 530472e:      	movl	%r13d, %eax
 5304731:      	orq	%r15, %rax
 5304734:      	addq	$0x1e8, %rsp            # imm = 0x1E8
 530473b:      	popq	%rbx
 530473c:      	popq	%r12
 530473e:      	popq	%r13
 5304740:      	popq	%r14
 5304742:      	popq	%r15
 5304744:      	popq	%rbp
 5304745:      	retq
 5304746:      	movq	%rdx, %r8
 5304749:      	movq	%rbx, %rax
 530474c:      	movq	%rbx, %rdx
 530474f:      	cmpl	$0x2, %esi
 5304752:      	je	0x5303dee <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 5304758:      	jmp	0x530476e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc5e>
 530475a:      	leaq	0x8(%rbx), %rax
 530475e:      	movl	0x8(%rbx), %ecx
 5304761:      	leaq	0x10(%rbx), %r8
 5304765:      	cmpl	$0x2, %esi
 5304768:      	je	0x5303dee <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 530476e:      	leaq	(%rbx,%rsi,8), %rsi
 5304772:      	addq	$0x8, %r8
 5304776:      	jmp	0x530479a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc8a>
 5304778:      	nopl	(%rax,%rax)
 5304780:      	movl	0x4(%rdi), %edx
 5304783:      	addl	%edx, 0x4(%rax)
 5304786:      	leaq	0x10(%rdi), %r8
 530478a:      	leaq	0x8(%rdi), %r9
 530478e:      	movq	%rdi, %rdx
 5304791:      	cmpq	%rsi, %r9
 5304794:      	je	0x5303dee <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 530479a:      	movq	%r8, %rdi
 530479d:      	cmpl	%ecx, -0x8(%r8)
 53047a1:      	jne	0x53047b0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xca0>
 53047a3:      	movl	0xc(%rdx), %edx
 53047a6:      	addl	%edx, 0x4(%rax)
 53047a9:      	cmpl	%ecx, (%rdi)
 53047ab:      	je	0x5304780 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc70>
 53047ad:      	jmp	0x53047c0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcb0>
 53047af:      	nop
 53047b0:      	movq	-0x8(%rdi), %rcx
 53047b4:      	movq	%rcx, 0x8(%rax)
 53047b8:      	addq	$0x8, %rax
 53047bc:      	cmpl	%ecx, (%rdi)
 53047be:      	je	0x5304780 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc70>
 53047c0:      	movq	(%rdi), %rcx
 53047c3:      	movq	%rcx, 0x8(%rax)
 53047c7:      	addq	$0x8, %rax
 53047cb:      	jmp	0x5304786 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc76>
 53047cd:      	leaq	-0x4669dea(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 53047d4:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
