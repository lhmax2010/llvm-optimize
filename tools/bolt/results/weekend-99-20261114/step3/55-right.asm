
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005303a80 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE>:
 5303a80:      	pushq	%rbp
 5303a81:      	pushq	%r15
 5303a83:      	pushq	%r14
 5303a85:      	pushq	%r13
 5303a87:      	pushq	%r12
 5303a89:      	pushq	%rbx
 5303a8a:      	subq	$0x1e8, %rsp            # imm = 0x1E8
 5303a91:      	leaq	0xe8(%rsp), %rax
 5303a99:      	movq	%rax, 0xd8(%rsp)
 5303aa1:      	movabsq	$0x2000000000, %rax     # imm = 0x2000000000
 5303aab:      	movq	%rax, 0xe0(%rsp)
 5303ab3:      	leaq	0xd8(%rsp), %rcx
 5303abb:      	movq	%rdi, (%rsp)
 5303abf:      	movl	$0x1, %edx
 5303ac4:      	callq	0x53039f0 <_ZN4llvm8coverage24CounterExpressionBuilder12extractTermsENS0_7CounterEiRNS_15SmallVectorImplINS1_4TermEEE>
 5303ac9:      	movl	0xe0(%rsp), %r14d
 5303ad1:      	movq	0xd8(%rsp), %rbx
 5303ad9:      	testq	%r14, %r14
 5303adc:      	je	0x5303b2e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xae>
 5303ade:      	leaq	(%rbx,%r14,8), %r15
 5303ae2:      	bsrq	%r14, %rdx
 5303ae6:      	xorl	$0x3f, %edx
 5303ae9:      	addl	%edx, %edx
 5303aeb:      	xorq	$0x7e, %rdx
 5303aef:      	movq	%rbx, %rdi
 5303af2:      	movq	%r15, %rsi
 5303af5:      	callq	0x5315ff0 <_ZSt16__introsort_loopIPN4llvm8coverage24CounterExpressionBuilder4TermElN9__gnu_cxx5__ops15_Iter_comp_iterIZNS2_8simplifyENS1_7CounterEE3$_0EEEvT_SB_T0_T1_>
 5303afa:      	leaq	0x8(%rbx), %r12
 5303afe:      	cmpl	$0x11, %r14d
 5303b02:      	movq	%rbx, 0x8(%rsp)
 5303b07:      	jb	0x5303b39 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb9>
 5303b09:      	movq	%r15, 0x20(%rsp)
 5303b0e:      	shlq	$0x3, %r14
 5303b12:      	movq	%r14, 0x18(%rsp)
 5303b17:      	leaq	0x8(%rbx), %r14
 5303b1b:      	movl	$0x8, %r13d
 5303b21:      	movq	%rbx, %rbp
 5303b24:      	movq	0x8(%rsp), %r15
 5303b29:      	jmp	0x5303c04 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x184>
 5303b2e:      	xorl	%r15d, %r15d
 5303b31:      	xorl	%r13d, %r13d
 5303b34:      	jmp	0x5304685 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 5303b39:      	cmpl	$0x1, %r14d
 5303b3d:      	je	0x5303d42 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303b43:      	movq	0x8(%rsp), %rbx
 5303b48:      	jmp	0x5303b89 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x109>
 5303b4a:      	nopw	(%rax,%rax)
 5303b50:      	movq	%rbx, %rdx
 5303b53:      	subq	%r12, %rdx
 5303b56:      	movq	%rdx, %rax
 5303b59:      	sarq	$0x3, %rax
 5303b5d:      	cmpq	$0x2, %rax
 5303b61:      	jl	0x5303bc3 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x143>
 5303b63:      	shlq	$0x3, %rax
 5303b67:      	subq	%rax, %rdi
 5303b6a:      	addq	$0x10, %rdi
 5303b6e:      	movq	%r12, %rsi
 5303b71:      	callq	0x828abc0 <memmove@plt>
 5303b76:      	movq	%r12, %rax
 5303b79:      	movq	%r14, (%rax)
 5303b7c:      	leaq	0x8(%rbx), %r12
 5303b80:      	cmpq	%r15, %r12
 5303b83:      	je	0x5303d42 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303b89:      	movq	%rbx, %rdi
 5303b8c:      	movq	%r12, %rbx
 5303b8f:      	movl	(%r12), %eax
 5303b93:      	movq	(%r12), %r14
 5303b97:      	movq	0x8(%rsp), %r12
 5303b9c:      	cmpl	(%r12), %eax
 5303ba0:      	jb	0x5303b50 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xd0>
 5303ba2:      	movq	%rbx, %rax
 5303ba5:      	cmpl	%r14d, (%rdi)
 5303ba8:      	jbe	0x5303b79 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303baa:      	movq	%rbx, %rax
 5303bad:      	nopl	(%rax)
 5303bb0:      	movq	-0x8(%rax), %rcx
 5303bb4:      	movq	%rcx, (%rax)
 5303bb7:      	cmpl	%r14d, -0x10(%rax)
 5303bbb:      	leaq	-0x8(%rax), %rax
 5303bbf:      	ja	0x5303bb0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x130>
 5303bc1:      	jmp	0x5303b79 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303bc3:      	movq	%r12, %rax
 5303bc6:      	cmpq	$0x8, %rdx
 5303bca:      	jne	0x5303b79 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303bcc:      	movq	0x8(%rsp), %rcx
 5303bd1:      	movq	(%rcx), %rax
 5303bd4:      	movq	%rax, 0x8(%rdi)
 5303bd8:      	movq	%rcx, %rax
 5303bdb:      	jmp	0x5303b79 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xf9>
 5303bdd:      	movq	0x8(%rsp), %rdx
 5303be2:      	movq	(%rdx), %rcx
 5303be5:      	movq	%rcx, 0x8(%rax)
 5303be9:      	movq	%rdx, %rcx
 5303bec:      	nopl	(%rax)
 5303bf0:      	movq	%rbx, (%rcx)
 5303bf3:      	addq	$0x8, %r13
 5303bf7:      	addq	$0x8, %r14
 5303bfb:      	cmpq	$0x80, %r13
 5303c02:      	je	0x5303c62 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1e2>
 5303c04:      	movq	%rbp, %rax
 5303c07:      	movq	0x8(%rsp), %rdx
 5303c0c:      	leaq	(%rdx,%r13), %rbp
 5303c10:      	movl	(%rdx,%r13), %ecx
 5303c14:      	movq	(%rdx,%r13), %rbx
 5303c18:      	cmpl	(%rdx), %ecx
 5303c1a:      	jae	0x5303c40 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1c0>
 5303c1c:      	cmpq	$0x9, %r13
 5303c20:      	jb	0x5303bdd <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x15d>
 5303c22:      	movq	%r12, %rdi
 5303c25:      	movq	%r15, %rsi
 5303c28:      	movq	%r13, %rdx
 5303c2b:      	callq	0x828abc0 <memmove@plt>
 5303c30:      	movq	%r15, %rcx
 5303c33:      	jmp	0x5303bf0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303c35:      	nopw	%cs:(%rax,%rax)
 5303c3f:      	nop
 5303c40:      	movq	%rbp, %rcx
 5303c43:      	cmpl	%ebx, (%rax)
 5303c45:      	jbe	0x5303bf0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303c47:      	movq	%r14, %rcx
 5303c4a:      	nopw	(%rax,%rax)
 5303c50:      	movq	-0x8(%rcx), %rax
 5303c54:      	movq	%rax, (%rcx)
 5303c57:      	cmpl	%ebx, -0x10(%rcx)
 5303c5a:      	leaq	-0x8(%rcx), %rcx
 5303c5e:      	ja	0x5303c50 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x1d0>
 5303c60:      	jmp	0x5303bf0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x170>
 5303c62:      	movq	0x8(%rsp), %rsi
 5303c67:      	leaq	0x80(%rsi), %rax
 5303c6e:      	movq	0x18(%rsp), %rdi
 5303c73:      	addq	$-0x88, %rdi
 5303c7a:      	testb	$0x8, %dil
 5303c7e:      	jne	0x5303cc4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x244>
 5303c80:      	movq	0x80(%rsi), %rcx
 5303c87:      	cmpl	%ecx, 0x78(%rsi)
 5303c8a:      	movq	0x20(%rsp), %r8
 5303c8f:      	jbe	0x5303cb0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x230>
 5303c91:      	nopw	%cs:(%rax,%rax)
 5303c9b:      	nopl	(%rax,%rax)
 5303ca0:      	movq	-0x8(%rax), %rdx
 5303ca4:      	movq	%rdx, (%rax)
 5303ca7:      	cmpl	%ecx, -0x10(%rax)
 5303caa:      	leaq	-0x8(%rax), %rax
 5303cae:      	ja	0x5303ca0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x220>
 5303cb0:      	movq	%rcx, (%rax)
 5303cb3:      	addq	$0x88, %rsi
 5303cba:      	movq	%rsi, %rax
 5303cbd:      	testq	%rdi, %rdi
 5303cc0:      	jne	0x5303cce <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x24e>
 5303cc2:      	jmp	0x5303d42 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303cc4:      	movq	0x20(%rsp), %r8
 5303cc9:      	testq	%rdi, %rdi
 5303ccc:      	je	0x5303d42 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303cce:      	leaq	0x8(%rax), %rcx
 5303cd2:      	jmp	0x5303cf4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x274>
 5303cd4:      	nopw	%cs:(%rax,%rax)
 5303cde:      	nop
 5303ce0:      	leaq	0x8(%rax), %rsi
 5303ce4:      	movq	%rdx, (%rsi)
 5303ce7:      	addq	$0x10, %rax
 5303ceb:      	addq	$0x10, %rcx
 5303cef:      	cmpq	%r8, %rax
 5303cf2:      	je	0x5303d42 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2c2>
 5303cf4:      	movq	(%rax), %rdx
 5303cf7:      	movq	%rax, %rsi
 5303cfa:      	cmpl	%edx, -0x8(%rax)
 5303cfd:      	jbe	0x5303d20 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2a0>
 5303cff:      	movq	%rax, %rsi
 5303d02:      	nopw	%cs:(%rax,%rax)
 5303d0c:      	nopl	(%rax)
 5303d10:      	movq	-0x8(%rsi), %rdi
 5303d14:      	movq	%rdi, (%rsi)
 5303d17:      	cmpl	%edx, -0x10(%rsi)
 5303d1a:      	leaq	-0x8(%rsi), %rsi
 5303d1e:      	ja	0x5303d10 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x290>
 5303d20:      	movq	%rdx, (%rsi)
 5303d23:      	movq	0x8(%rax), %rdx
 5303d27:      	cmpl	%edx, (%rax)
 5303d29:      	jbe	0x5303ce0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x260>
 5303d2b:      	movq	%rcx, %rsi
 5303d2e:      	nop
 5303d30:      	movq	-0x8(%rsi), %rdi
 5303d34:      	movq	%rdi, (%rsi)
 5303d37:      	cmpl	%edx, -0x10(%rsi)
 5303d3a:      	leaq	-0x8(%rsi), %rsi
 5303d3e:      	ja	0x5303d30 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2b0>
 5303d40:      	jmp	0x5303ce4 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x264>
 5303d42:      	movq	0xd8(%rsp), %rbx
 5303d4a:      	movl	0xe0(%rsp), %esi
 5303d51:      	movq	%rbx, %rax
 5303d54:      	cmpq	$0x1, %rsi
 5303d58:      	jne	0x530420b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x78b>
 5303d5e:      	subq	%rbx, %rax
 5303d61:      	addq	$0x8, %rax
 5303d65:      	movq	%rax, %rcx
 5303d68:      	shrq	$0x3, %rcx
 5303d6c:      	movl	%ecx, 0xe0(%rsp)
 5303d73:      	movabsq	$0x7fffffff8, %rdx      # imm = 0x7FFFFFFF8
 5303d7d:      	andq	%rax, %rdx
 5303d80:      	je	0x530423e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7be>
 5303d86:      	addq	%rbx, %rdx
 5303d89:      	movq	(%rsp), %r8
 5303d8d:      	leaq	0x18(%r8), %rax
 5303d91:      	movq	%rax, 0x40(%rsp)
 5303d96:      	xorl	%r13d, %r13d
 5303d99:      	xorl	%r15d, %r15d
 5303d9c:      	movq	%rdx, 0x48(%rsp)
 5303da1:      	jmp	0x5303dc7 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x347>
 5303da3:      	nopw	%cs:(%rax,%rax)
 5303dad:      	nopl	(%rax)
 5303db0:      	movq	0x8(%rsp), %rbx
 5303db5:      	addq	$0x8, %rbx
 5303db9:      	movq	0x48(%rsp), %rdx
 5303dbe:      	cmpq	%rdx, %rbx
 5303dc1:      	je	0x53041f3 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x773>
 5303dc7:      	movl	0x4(%rbx), %r9d
 5303dcb:      	testl	%r9d, %r9d
 5303dce:      	movq	%rbx, 0x8(%rsp)
 5303dd3:      	jle	0x5303db0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 5303dd5:      	movl	(%rbx), %r10d
 5303dd8:      	movq	%r10, %rax
 5303ddb:      	shlq	$0x20, %rax
 5303ddf:      	incq	%rax
 5303de2:      	movq	%rax, 0x20(%rsp)
 5303de7:      	xorl	%r14d, %r14d
 5303dea:      	movl	%r9d, 0x18(%rsp)
 5303def:      	movq	%r10, 0x10(%rsp)
 5303df4:      	jmp	0x5303ed0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 5303df9:      	nopl	(%rax)
 5303e00:      	movl	%eax, %esi
 5303e02:      	leaq	(%rsi,%rsi,2), %rsi
 5303e06:      	leaq	(%r11,%rsi,8), %r12
 5303e0a:      	movl	(%r11,%rsi,8), %esi
 5303e0e:      	cmpl	$0x1, %esi
 5303e11:      	jne	0x5303e64 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3e4>
 5303e13:      	movl	0x4(%r12), %esi
 5303e18:      	movl	0x8(%r12), %edi
 5303e1d:      	cmpl	%esi, %r13d
 5303e20:      	movl	0x18(%rsp), %r9d
 5303e25:      	movq	0x10(%rsp), %r10
 5303e2a:      	jne	0x5303e44 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303e2c:      	cmpl	%edi, %r15d
 5303e2f:      	jne	0x5303e44 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303e31:      	cmpl	$0x1, 0xc(%r12)
 5303e37:      	jne	0x5303e44 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x3c4>
 5303e39:      	cmpl	0x10(%r12), %r10d
 5303e3e:      	je	0x5304150 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6d0>
 5303e44:      	xorl	$0x1, %esi
 5303e47:      	notl	%edi
 5303e49:      	orl	%esi, %edi
 5303e4b:      	jne	0x5303e98 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x418>
 5303e4d:      	movl	0xc(%r12), %esi
 5303e52:      	movl	0x10(%r12), %edi
 5303e57:      	xorl	$0x1, %esi
 5303e5a:      	notl	%edi
 5303e5c:      	orl	%esi, %edi
 5303e5e:      	sete	%sil
 5303e62:      	jmp	0x5303e9a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303e64:      	testl	%esi, %esi
 5303e66:      	movl	0x18(%rsp), %r9d
 5303e6b:      	movq	0x10(%rsp), %r10
 5303e70:      	jne	0x5303e98 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x418>
 5303e72:      	xorl	%esi, %esi
 5303e74:      	cmpl	$0x1, 0x4(%r12)
 5303e7a:      	jne	0x5303e9a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303e7c:      	cmpl	$-0x1, 0x8(%r12)
 5303e82:      	jne	0x5303e9a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303e84:      	xorl	%esi, %esi
 5303e86:      	cmpl	$0x1, 0xc(%r12)
 5303e8c:      	jne	0x5303e9a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303e8e:      	cmpl	$-0x1, 0x10(%r12)
 5303e94:      	je	0x5303eb3 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x433>
 5303e96:      	jmp	0x5303e9a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x41a>
 5303e98:      	xorl	%esi, %esi
 5303e9a:      	testq	%rcx, %rcx
 5303e9d:      	cmovneq	%rcx, %r12
 5303ea1:      	testb	%sil, %sil
 5303ea4:      	cmovneq	%r12, %rcx
 5303ea8:      	addl	%edx, %eax
 5303eaa:      	incl	%edx
 5303eac:      	andl	%ebx, %eax
 5303eae:      	jmp	0x5303e00 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x380>
 5303eb3:      	testq	%rcx, %rcx
 5303eb6:      	cmovneq	%rcx, %r12
 5303eba:      	movl	0x28(%r8), %esi
 5303ebe:      	jmp	0x5303fc5 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x545>
 5303ec3:      	nopw	%cs:(%rax,%rax)
 5303ecd:      	nopl	(%rax)
 5303ed0:      	testl	%r13d, %r13d
 5303ed3:      	je	0x5303fa0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x520>
 5303ed9:      	movq	%r15, %rax
 5303edc:      	shlq	$0x20, %rax
 5303ee0:      	movl	%r13d, %ecx
 5303ee3:      	orq	%rax, %rcx
 5303ee6:      	movl	$0x1, 0x2c(%rsp)
 5303eee:      	movq	%rcx, 0x30(%rsp)
 5303ef3:      	movq	0x20(%rsp), %rax
 5303ef8:      	movq	%rax, 0x38(%rsp)
 5303efd:      	movq	0x8(%r8), %rbp
 5303f01:      	subq	(%r8), %rbp
 5303f04:      	movl	0x28(%r8), %ebx
 5303f08:      	testl	%ebx, %ebx
 5303f0a:      	je	0x5303fc0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x540>
 5303f10:      	movq	0x18(%r8), %r12
 5303f14:      	leaq	0x98(%rsp), %rcx
 5303f1c:      	xorps	%xmm0, %xmm0
 5303f1f:      	movups	%xmm0, 0x20(%rcx)
 5303f23:      	movups	%xmm0, 0x10(%rcx)
 5303f27:      	movups	%xmm0, (%rcx)
 5303f2a:      	movups	%xmm0, -0x10(%rcx)
 5303f2e:      	movups	%xmm0, -0x20(%rcx)
 5303f32:      	movups	%xmm0, -0x30(%rcx)
 5303f36:      	movq	$0x0, 0x30(%rcx)
 5303f3e:      	movabsq	$-0xae502812aa7333, %rax # imm = 0xFF51AFD7ED558CCD
 5303f48:      	movq	%rax, 0xd0(%rsp)
 5303f50:      	movl	$0x1, 0x58(%rsp)
 5303f58:      	movl	%r13d, 0x5c(%rsp)
 5303f5d:      	movl	%r15d, 0x60(%rsp)
 5303f62:      	movl	$0x1, 0x64(%rsp)
 5303f6a:      	movl	%r10d, 0x68(%rsp)
 5303f6f:      	leaq	0x58(%rsp), %rdi
 5303f74:      	xorl	%esi, %esi
 5303f76:      	leaq	0x6c(%rsp), %rdx
 5303f7b:      	callq	0x2ac8d90 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 5303f80:      	movq	%r12, %r11
 5303f83:      	movq	(%rsp), %r8
 5303f87:      	decl	%ebx
 5303f89:      	andl	%ebx, %eax
 5303f8b:      	movl	$0x1, %edx
 5303f90:      	xorl	%ecx, %ecx
 5303f92:      	jmp	0x5303e00 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x380>
 5303f97:      	nopw	(%rax,%rax)
 5303fa0:      	movl	$0x1, %r13d
 5303fa6:      	movl	%r10d, %r15d
 5303fa9:      	incl	%r14d
 5303fac:      	cmpl	%r9d, %r14d
 5303faf:      	jne	0x5303ed0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 5303fb5:      	jmp	0x5303db0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 5303fba:      	nopw	(%rax,%rax)
 5303fc0:      	xorl	%esi, %esi
 5303fc2:      	xorl	%r12d, %r12d
 5303fc5:      	movq	%r12, 0x58(%rsp)
 5303fca:      	movl	0x20(%r8), %eax
 5303fce:      	leal	0x4(,%rax,4), %ecx
 5303fd5:      	leal	(%rsi,%rsi,2), %edx
 5303fd8:      	cmpl	%edx, %ecx
 5303fda:      	jae	0x530416c <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6ec>
 5303fe0:      	movl	%eax, %ecx
 5303fe2:      	notl	%ecx
 5303fe4:      	addl	%esi, %ecx
 5303fe6:      	subl	0x24(%r8), %ecx
 5303fea:      	movl	%esi, %edx
 5303fec:      	shrl	$0x3, %edx
 5303fef:      	cmpl	%edx, %ecx
 5303ff1:      	jbe	0x530416e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6ee>
 5303ff7:      	incl	%eax
 5303ff9:      	movl	%eax, 0x20(%r8)
 5303ffd:      	cmpl	$0x0, (%r12)
 5304002:      	je	0x53041be <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x73e>
 5304008:      	decl	0x24(%r8)
 530400c:      	sarq	$0x2, %rbp
 5304010:      	movabsq	$-0x3333333333333333, %rax # imm = 0xCCCCCCCCCCCCCCCD
 530401a:      	imulq	%rax, %rbp
 530401e:      	movl	0x3c(%rsp), %eax
 5304022:      	movl	%eax, 0x10(%r12)
 5304027:      	movups	0x2c(%rsp), %xmm0
 530402c:      	movups	%xmm0, (%r12)
 5304031:      	movl	%ebp, 0x14(%r12)
 5304036:      	movq	0x8(%r8), %rbx
 530403a:      	cmpq	0x10(%r8), %rbx
 530403e:      	je	0x5304059 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x5d9>
 5304040:      	movl	0x3c(%rsp), %eax
 5304044:      	movl	%eax, 0x10(%rbx)
 5304047:      	movups	0x2c(%rsp), %xmm0
 530404c:      	movups	%xmm0, (%rbx)
 530404f:      	addq	$0x14, 0x8(%r8)
 5304054:      	jmp	0x5304150 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6d0>
 5304059:      	movq	(%r8), %rbp
 530405c:      	movq	%rbx, %r13
 530405f:      	subq	%rbp, %r13
 5304062:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 530406c:      	cmpq	%rax, %r13
 530406f:      	je	0x530473d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcbd>
 5304075:      	movq	%r13, %rax
 5304078:      	sarq	$0x2, %rax
 530407c:      	movabsq	$-0x3333333333333333, %rcx # imm = 0xCCCCCCCCCCCCCCCD
 5304086:      	imulq	%rcx, %rax
 530408a:      	cmpq	$0x1, %rax
 530408e:      	movq	%rax, %rcx
 5304091:      	adcq	$0x0, %rcx
 5304095:      	leaq	(%rcx,%rax), %rsi
 5304099:      	movabsq	$0x666666666666666, %rdx # imm = 0x666666666666666
 53040a3:      	cmpq	%rdx, %rsi
 53040a6:      	cmovaeq	%rdx, %rsi
 53040aa:      	addq	%rax, %rcx
 53040ad:      	cmovbq	%rdx, %rsi
 53040b1:      	movq	%rsi, 0x50(%rsp)
 53040b6:      	leaq	(,%rsi,4), %rax
 53040be:      	leaq	(%rax,%rax,4), %rdi
 53040c2:      	callq	0x828a620 <_Znwm@plt>
 53040c7:      	movq	%rax, %rdx
 53040ca:      	movups	0x2c(%rsp), %xmm0
 53040cf:      	movups	%xmm0, (%rax,%r13)
 53040d4:      	movl	0x3c(%rsp), %eax
 53040d8:      	movl	%eax, 0x10(%rdx,%r13)
 53040dd:      	movq	%rdx, %r15
 53040e0:      	cmpq	%rbx, %rbp
 53040e3:      	je	0x530410b <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x68b>
 53040e5:      	movq	%rdx, %r15
 53040e8:      	movq	%rbp, %rax
 53040eb:      	nopl	(%rax,%rax)
 53040f0:      	movl	0x10(%rax), %ecx
 53040f3:      	movl	%ecx, 0x10(%r15)
 53040f7:      	movups	(%rax), %xmm0
 53040fa:      	movups	%xmm0, (%r15)
 53040fe:      	addq	$0x14, %rax
 5304102:      	addq	$0x14, %r15
 5304106:      	cmpq	%rbx, %rax
 5304109:      	jne	0x53040f0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x670>
 530410b:      	testq	%rbp, %rbp
 530410e:      	je	0x5304121 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x6a1>
 5304110:      	movq	%rbp, %rdi
 5304113:      	movq	%r13, %rsi
 5304116:      	movq	%rdx, %rbx
 5304119:      	callq	0x828a660 <_ZdlPvm@plt>
 530411e:      	movq	%rbx, %rdx
 5304121:      	addq	$0x14, %r15
 5304125:      	movq	(%rsp), %r8
 5304129:      	movq	%rdx, (%r8)
 530412c:      	movq	%r15, 0x8(%r8)
 5304130:      	movq	0x50(%rsp), %rax
 5304135:      	leaq	(%rax,%rax,4), %rax
 5304139:      	leaq	(%rdx,%rax,4), %rax
 530413d:      	movq	%rax, 0x10(%r8)
 5304141:      	movl	0x18(%rsp), %r9d
 5304146:      	movq	0x10(%rsp), %r10
 530414b:      	nopl	(%rax,%rax)
 5304150:      	movl	0x14(%r12), %r15d
 5304155:      	movl	$0x2, %r13d
 530415b:      	incl	%r14d
 530415e:      	cmpl	%r9d, %r14d
 5304161:      	jne	0x5303ed0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x450>
 5304167:      	jmp	0x5303db0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x330>
 530416c:      	addl	%esi, %esi
 530416e:      	movq	0x40(%rsp), %rdi
 5304173:      	callq	0x5315d10 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E4growEj>
 5304178:      	movq	(%rsp), %rax
 530417c:      	movq	0x18(%rax), %rdi
 5304180:      	movq	(%rsp), %rax
 5304184:      	movl	0x28(%rax), %esi
 5304187:      	leaq	0x2c(%rsp), %rdx
 530418c:      	leaq	0x58(%rsp), %rcx
 5304191:      	callq	0x5315ba0 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E15LookupBucketForIS3_EEbRKT_RPS8_>
 5304196:      	movq	0x10(%rsp), %r10
 530419b:      	movl	0x18(%rsp), %r9d
 53041a0:      	movq	(%rsp), %r8
 53041a4:      	movl	0x20(%r8), %eax
 53041a8:      	movq	0x58(%rsp), %r12
 53041ad:      	incl	%eax
 53041af:      	movl	%eax, 0x20(%r8)
 53041b3:      	cmpl	$0x0, (%r12)
 53041b8:      	jne	0x5304008 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 53041be:      	cmpl	$0x1, 0x4(%r12)
 53041c4:      	jne	0x5304008 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 53041ca:      	cmpl	$-0x1, 0x8(%r12)
 53041d0:      	jne	0x5304008 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 53041d6:      	cmpl	$0x1, 0xc(%r12)
 53041dc:      	jne	0x5304008 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 53041e2:      	cmpl	$-0x1, 0x10(%r12)
 53041e8:      	je	0x530400c <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x58c>
 53041ee:      	jmp	0x5304008 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x588>
 53041f3:      	movq	0xd8(%rsp), %rbx
 53041fb:      	movl	0xe0(%rsp), %ecx
 5304202:      	testl	%ecx, %ecx
 5304204:      	jne	0x5304250 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7d0>
 5304206:      	jmp	0x5304685 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 530420b:      	leaq	0x8(%rbx), %rdx
 530420f:      	movl	(%rbx), %ecx
 5304211:      	testb	$0x1, %sil
 5304215:      	jne	0x53046b6 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc36>
 530421b:      	cmpl	%ecx, (%rdx)
 530421d:      	jne	0x53046ca <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc4a>
 5304223:      	movl	0xc(%rbx), %eax
 5304226:      	addl	%eax, 0x4(%rbx)
 5304229:      	movq	%rbx, %rax
 530422c:      	leaq	0x10(%rbx), %r8
 5304230:      	cmpl	$0x2, %esi
 5304233:      	jne	0x53046de <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc5e>
 5304239:      	jmp	0x5303d5e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 530423e:      	xorl	%r15d, %r15d
 5304241:      	xorl	%r13d, %r13d
 5304244:      	movq	(%rsp), %r8
 5304248:      	testl	%ecx, %ecx
 530424a:      	je	0x5304685 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc05>
 5304250:      	movl	%ecx, %eax
 5304252:      	leaq	(%rbx,%rax,8), %rax
 5304256:      	leaq	0x18(%r8), %rcx
 530425a:      	movq	%rcx, 0x40(%rsp)
 530425f:      	movq	%rax, 0x48(%rsp)
 5304264:      	jmp	0x530428d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x80d>
 5304266:      	nopw	%cs:(%rax,%rax)
 5304270:      	movl	$0x2, %r13d
 5304276:      	movq	0x8(%rsp), %rbx
 530427b:      	movq	0x48(%rsp), %rax
 5304280:      	addq	$0x8, %rbx
 5304284:      	cmpq	%rax, %rbx
 5304287:      	je	0x530467d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xbfd>
 530428d:      	movl	0x4(%rbx), %r9d
 5304291:      	testl	%r9d, %r9d
 5304294:      	jns	0x5304280 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x800>
 5304296:      	movq	%rbx, 0x8(%rsp)
 530429b:      	movl	(%rbx), %eax
 530429d:      	movl	%eax, 0x20(%rsp)
 53042a1:      	negl	%r9d
 53042a4:      	shlq	$0x20, %rax
 53042a8:      	incq	%rax
 53042ab:      	movq	%rax, 0x18(%rsp)
 53042b0:      	movl	%r13d, %ebp
 53042b3:      	cmpl	$0x2, %r9d
 53042b7:      	movl	$0x1, %eax
 53042bc:      	cmovll	%eax, %r9d
 53042c0:      	xorl	%r14d, %r14d
 53042c3:      	movl	%r9d, 0x10(%rsp)
 53042c8:      	jmp	0x530439a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x91a>
 53042cd:      	nopl	(%rax)
 53042d0:      	movl	%eax, %esi
 53042d2:      	leaq	(%rsi,%rsi,2), %rsi
 53042d6:      	leaq	(%r10,%rsi,8), %r12
 53042da:      	movl	(%r10,%rsi,8), %esi
 53042de:      	testl	%esi, %esi
 53042e0:      	jne	0x5304337 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8b7>
 53042e2:      	movl	0x4(%r12), %r8d
 53042e7:      	movl	0x8(%r12), %edi
 53042ec:      	cmpl	%ebp, %r8d
 53042ef:      	movl	0x10(%rsp), %r9d
 53042f4:      	jne	0x530430e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 53042f6:      	cmpl	%edi, %r15d
 53042f9:      	jne	0x530430e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 53042fb:      	cmpl	$0x1, 0xc(%r12)
 5304301:      	jne	0x530430e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x88e>
 5304303:      	movl	0x20(%rsp), %esi
 5304307:      	cmpl	0x10(%r12), %esi
 530430c:      	je	0x5304380 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x900>
 530430e:      	xorl	%esi, %esi
 5304310:      	cmpl	$0x1, %r8d
 5304314:      	jne	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 5304316:      	cmpl	$-0x1, %edi
 5304319:      	movq	(%rsp), %r8
 530431d:      	jne	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 530431f:      	xorl	%esi, %esi
 5304321:      	cmpl	$0x1, 0xc(%r12)
 5304327:      	jne	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 5304329:      	cmpl	$-0x1, 0x10(%r12)
 530432f:      	je	0x53045eb <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb6b>
 5304335:      	jmp	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 5304337:      	cmpl	$0x1, %esi
 530433a:      	jne	0x5304365 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e5>
 530433c:      	xorl	%esi, %esi
 530433e:      	cmpl	$0x1, 0x4(%r12)
 5304344:      	jne	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 5304346:      	cmpl	$-0x1, 0x8(%r12)
 530434c:      	jne	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 530434e:      	movl	0xc(%r12), %esi
 5304353:      	movl	0x10(%r12), %edi
 5304358:      	xorl	$0x1, %esi
 530435b:      	notl	%edi
 530435d:      	orl	%esi, %edi
 530435f:      	sete	%sil
 5304363:      	jmp	0x5304367 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x8e7>
 5304365:      	xorl	%esi, %esi
 5304367:      	testq	%rcx, %rcx
 530436a:      	cmovneq	%rcx, %r12
 530436e:      	testb	%sil, %sil
 5304371:      	cmovneq	%r12, %rcx
 5304375:      	addl	%edx, %eax
 5304377:      	incl	%edx
 5304379:      	andl	%ebx, %eax
 530437b:      	jmp	0x53042d0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x850>
 5304380:      	movq	(%rsp), %r8
 5304384:      	movl	0x14(%r12), %r15d
 5304389:      	incl	%r14d
 530438c:      	movl	$0x2, %ebp
 5304391:      	cmpl	%r9d, %r14d
 5304394:      	je	0x5304270 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x7f0>
 530439a:      	movq	%r15, %rax
 530439d:      	shlq	$0x20, %rax
 53043a1:      	orq	%rbp, %rax
 53043a4:      	movl	$0x0, 0x2c(%rsp)
 53043ac:      	movq	%rax, 0x30(%rsp)
 53043b1:      	movq	0x18(%rsp), %rax
 53043b6:      	movq	%rax, 0x38(%rsp)
 53043bb:      	movq	0x8(%r8), %r13
 53043bf:      	subq	(%r8), %r13
 53043c2:      	movl	0x28(%r8), %ebx
 53043c6:      	testl	%ebx, %ebx
 53043c8:      	je	0x5304460 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x9e0>
 53043ce:      	movq	0x18(%r8), %r12
 53043d2:      	leaq	0x98(%rsp), %rcx
 53043da:      	xorps	%xmm0, %xmm0
 53043dd:      	movups	%xmm0, 0x20(%rcx)
 53043e1:      	movups	%xmm0, 0x10(%rcx)
 53043e5:      	movups	%xmm0, (%rcx)
 53043e8:      	movups	%xmm0, -0x10(%rcx)
 53043ec:      	movups	%xmm0, -0x20(%rcx)
 53043f0:      	movups	%xmm0, -0x30(%rcx)
 53043f4:      	movq	$0x0, 0x30(%rcx)
 53043fc:      	movabsq	$-0xae502812aa7333, %rax # imm = 0xFF51AFD7ED558CCD
 5304406:      	movq	%rax, 0xd0(%rsp)
 530440e:      	movl	$0x0, 0x58(%rsp)
 5304416:      	movl	%ebp, 0x5c(%rsp)
 530441a:      	movl	%r15d, 0x60(%rsp)
 530441f:      	movl	$0x1, 0x64(%rsp)
 5304427:      	movl	0x20(%rsp), %eax
 530442b:      	movl	%eax, 0x68(%rsp)
 530442f:      	leaq	0x58(%rsp), %rdi
 5304434:      	xorl	%esi, %esi
 5304436:      	leaq	0x6c(%rsp), %rdx
 530443b:      	callq	0x2ac8d90 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 5304440:      	movq	%r12, %r10
 5304443:      	decl	%ebx
 5304445:      	andl	%ebx, %eax
 5304447:      	movl	$0x1, %edx
 530444c:      	xorl	%ecx, %ecx
 530444e:      	jmp	0x53042d0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x850>
 5304453:      	nopw	%cs:(%rax,%rax)
 530445d:      	nopl	(%rax)
 5304460:      	xorl	%esi, %esi
 5304462:      	xorl	%r12d, %r12d
 5304465:      	movq	%r12, 0x58(%rsp)
 530446a:      	movl	0x20(%r8), %eax
 530446e:      	leal	0x4(,%rax,4), %ecx
 5304475:      	leal	(%rsi,%rsi,2), %edx
 5304478:      	cmpl	%edx, %ecx
 530447a:      	jae	0x53045fb <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb7b>
 5304480:      	movl	%eax, %ecx
 5304482:      	notl	%ecx
 5304484:      	addl	%esi, %ecx
 5304486:      	subl	0x24(%r8), %ecx
 530448a:      	movl	%esi, %edx
 530448c:      	shrl	$0x3, %edx
 530448f:      	cmpl	%edx, %ecx
 5304491:      	jbe	0x53045fd <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb7d>
 5304497:      	incl	%eax
 5304499:      	movl	%eax, 0x20(%r8)
 530449d:      	cmpl	$0x0, (%r12)
 53044a2:      	je	0x5304648 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xbc8>
 53044a8:      	decl	0x24(%r8)
 53044ac:      	sarq	$0x2, %r13
 53044b0:      	movabsq	$-0x3333333333333333, %rax # imm = 0xCCCCCCCCCCCCCCCD
 53044ba:      	imulq	%rax, %r13
 53044be:      	movl	0x3c(%rsp), %eax
 53044c2:      	movl	%eax, 0x10(%r12)
 53044c7:      	movups	0x2c(%rsp), %xmm0
 53044cc:      	movups	%xmm0, (%r12)
 53044d1:      	movl	%r13d, 0x14(%r12)
 53044d6:      	movq	0x8(%r8), %rbx
 53044da:      	cmpq	0x10(%r8), %rbx
 53044de:      	je	0x53044f9 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa79>
 53044e0:      	movl	0x3c(%rsp), %eax
 53044e4:      	movl	%eax, 0x10(%rbx)
 53044e7:      	movups	0x2c(%rsp), %xmm0
 53044ec:      	movups	%xmm0, (%rbx)
 53044ef:      	addq	$0x14, 0x8(%r8)
 53044f4:      	jmp	0x5304384 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x904>
 53044f9:      	movq	(%r8), %rbp
 53044fc:      	movq	%rbx, %r13
 53044ff:      	subq	%rbp, %r13
 5304502:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 530450c:      	cmpq	%rax, %r13
 530450f:      	je	0x530473d <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcbd>
 5304515:      	movq	%r13, %rax
 5304518:      	sarq	$0x2, %rax
 530451c:      	movabsq	$-0x3333333333333333, %rcx # imm = 0xCCCCCCCCCCCCCCCD
 5304526:      	imulq	%rcx, %rax
 530452a:      	cmpq	$0x1, %rax
 530452e:      	movq	%rax, %rcx
 5304531:      	adcq	$0x0, %rcx
 5304535:      	leaq	(%rcx,%rax), %rsi
 5304539:      	movabsq	$0x666666666666666, %rdx # imm = 0x666666666666666
 5304543:      	cmpq	%rdx, %rsi
 5304546:      	cmovaeq	%rdx, %rsi
 530454a:      	addq	%rax, %rcx
 530454d:      	cmovbq	%rdx, %rsi
 5304551:      	movq	%rsi, 0x50(%rsp)
 5304556:      	leaq	(,%rsi,4), %rax
 530455e:      	leaq	(%rax,%rax,4), %rdi
 5304562:      	callq	0x828a620 <_Znwm@plt>
 5304567:      	movq	%rax, %rdx
 530456a:      	movups	0x2c(%rsp), %xmm0
 530456f:      	movups	%xmm0, (%rax,%r13)
 5304574:      	movl	0x3c(%rsp), %eax
 5304578:      	movl	%eax, 0x10(%rdx,%r13)
 530457d:      	movq	%rdx, %r15
 5304580:      	cmpq	%rbx, %rbp
 5304583:      	je	0x53045ab <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb2b>
 5304585:      	movq	%rdx, %r15
 5304588:      	movq	%rbp, %rax
 530458b:      	nopl	(%rax,%rax)
 5304590:      	movl	0x10(%rax), %ecx
 5304593:      	movl	%ecx, 0x10(%r15)
 5304597:      	movups	(%rax), %xmm0
 530459a:      	movups	%xmm0, (%r15)
 530459e:      	addq	$0x14, %rax
 53045a2:      	addq	$0x14, %r15
 53045a6:      	cmpq	%rbx, %rax
 53045a9:      	jne	0x5304590 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb10>
 53045ab:      	testq	%rbp, %rbp
 53045ae:      	je	0x53045c1 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xb41>
 53045b0:      	movq	%rbp, %rdi
 53045b3:      	movq	%r13, %rsi
 53045b6:      	movq	%rdx, %rbx
 53045b9:      	callq	0x828a660 <_ZdlPvm@plt>
 53045be:      	movq	%rbx, %rdx
 53045c1:      	addq	$0x14, %r15
 53045c5:      	movq	(%rsp), %r8
 53045c9:      	movq	%rdx, (%r8)
 53045cc:      	movq	%r15, 0x8(%r8)
 53045d0:      	movq	0x50(%rsp), %rax
 53045d5:      	leaq	(%rax,%rax,4), %rax
 53045d9:      	leaq	(%rdx,%rax,4), %rax
 53045dd:      	movq	%rax, 0x10(%r8)
 53045e1:      	movl	0x10(%rsp), %r9d
 53045e6:      	jmp	0x5304384 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x904>
 53045eb:      	testq	%rcx, %rcx
 53045ee:      	cmovneq	%rcx, %r12
 53045f2:      	movl	0x28(%r8), %esi
 53045f6:      	jmp	0x5304465 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x9e5>
 53045fb:      	addl	%esi, %esi
 53045fd:      	movq	0x40(%rsp), %rdi
 5304602:      	callq	0x5315d10 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E4growEj>
 5304607:      	movq	(%rsp), %rax
 530460b:      	movq	0x18(%rax), %rdi
 530460f:      	movq	(%rsp), %rax
 5304613:      	movl	0x28(%rax), %esi
 5304616:      	leaq	0x2c(%rsp), %rdx
 530461b:      	leaq	0x58(%rsp), %rcx
 5304620:      	callq	0x5315ba0 <_ZN4llvm12DenseMapBaseINS_8DenseMapINS_8coverage17CounterExpressionEjNS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_jEEEES3_jS5_S8_E15LookupBucketForIS3_EEbRKT_RPS8_>
 5304625:      	movl	0x10(%rsp), %r9d
 530462a:      	movq	(%rsp), %r8
 530462e:      	movl	0x20(%r8), %eax
 5304632:      	movq	0x58(%rsp), %r12
 5304637:      	incl	%eax
 5304639:      	movl	%eax, 0x20(%r8)
 530463d:      	cmpl	$0x0, (%r12)
 5304642:      	jne	0x53044a8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 5304648:      	cmpl	$0x1, 0x4(%r12)
 530464e:      	jne	0x53044a8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 5304654:      	cmpl	$-0x1, 0x8(%r12)
 530465a:      	jne	0x53044a8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 5304660:      	cmpl	$0x1, 0xc(%r12)
 5304666:      	jne	0x53044a8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 530466c:      	cmpl	$-0x1, 0x10(%r12)
 5304672:      	je	0x53044ac <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa2c>
 5304678:      	jmp	0x53044a8 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xa28>
 530467d:      	movq	0xd8(%rsp), %rbx
 5304685:      	leaq	0xe8(%rsp), %rax
 530468d:      	cmpq	%rax, %rbx
 5304690:      	je	0x530469a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc1a>
 5304692:      	movq	%rbx, %rdi
 5304695:      	callq	0x828a640 <free@plt>
 530469a:      	shlq	$0x20, %r15
 530469e:      	movl	%r13d, %eax
 53046a1:      	orq	%r15, %rax
 53046a4:      	addq	$0x1e8, %rsp            # imm = 0x1E8
 53046ab:      	popq	%rbx
 53046ac:      	popq	%r12
 53046ae:      	popq	%r13
 53046b0:      	popq	%r14
 53046b2:      	popq	%r15
 53046b4:      	popq	%rbp
 53046b5:      	retq
 53046b6:      	movq	%rdx, %r8
 53046b9:      	movq	%rbx, %rax
 53046bc:      	movq	%rbx, %rdx
 53046bf:      	cmpl	$0x2, %esi
 53046c2:      	je	0x5303d5e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 53046c8:      	jmp	0x53046de <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc5e>
 53046ca:      	leaq	0x8(%rbx), %rax
 53046ce:      	movl	0x8(%rbx), %ecx
 53046d1:      	leaq	0x10(%rbx), %r8
 53046d5:      	cmpl	$0x2, %esi
 53046d8:      	je	0x5303d5e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 53046de:      	leaq	(%rbx,%rsi,8), %rsi
 53046e2:      	addq	$0x8, %r8
 53046e6:      	jmp	0x530470a <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc8a>
 53046e8:      	nopl	(%rax,%rax)
 53046f0:      	movl	0x4(%rdi), %edx
 53046f3:      	addl	%edx, 0x4(%rax)
 53046f6:      	leaq	0x10(%rdi), %r8
 53046fa:      	leaq	0x8(%rdi), %r9
 53046fe:      	movq	%rdi, %rdx
 5304701:      	cmpq	%rsi, %r9
 5304704:      	je	0x5303d5e <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0x2de>
 530470a:      	movq	%r8, %rdi
 530470d:      	cmpl	%ecx, -0x8(%r8)
 5304711:      	jne	0x5304720 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xca0>
 5304713:      	movl	0xc(%rdx), %edx
 5304716:      	addl	%edx, 0x4(%rax)
 5304719:      	cmpl	%ecx, (%rdi)
 530471b:      	je	0x53046f0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc70>
 530471d:      	jmp	0x5304730 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xcb0>
 530471f:      	nop
 5304720:      	movq	-0x8(%rdi), %rcx
 5304724:      	movq	%rcx, 0x8(%rax)
 5304728:      	addq	$0x8, %rax
 530472c:      	cmpl	%ecx, (%rdi)
 530472e:      	je	0x53046f0 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc70>
 5304730:      	movq	(%rdi), %rcx
 5304733:      	movq	%rcx, 0x8(%rax)
 5304737:      	addq	$0x8, %rax
 530473b:      	jmp	0x53046f6 <_ZN4llvm8coverage24CounterExpressionBuilder8simplifyENS0_7CounterE+0xc76>
 530473d:      	leaq	-0x4669d5a(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 5304744:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
