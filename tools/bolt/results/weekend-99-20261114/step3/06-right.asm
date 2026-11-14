
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005f859b0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_>:
 5f859b0:      	pushq	%rbp
 5f859b1:      	pushq	%r15
 5f859b3:      	pushq	%r14
 5f859b5:      	pushq	%r13
 5f859b7:      	pushq	%r12
 5f859b9:      	pushq	%rbx
 5f859ba:      	subq	$0x1c8, %rsp            # imm = 0x1C8
 5f859c1:      	movl	%r8d, %ebx
 5f859c4:      	movq	%rcx, %rbp
 5f859c7:      	movq	%rdx, %r12
 5f859ca:      	movq	%rsi, %r15
 5f859cd:      	movq	%rdi, %r14
 5f859d0:      	xorps	%xmm0, %xmm0
 5f859d3:      	movaps	%xmm0, 0x1b0(%rsp)
 5f859db:      	movaps	%xmm0, 0x1a0(%rsp)
 5f859e3:      	movq	0x10(%rdx), %rax
 5f859e7:      	testq	%rax, %rax
 5f859ea:      	movq	%rsi, 0x140(%rsp)
 5f859f2:      	je	0x5f85b66 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1b6>
 5f859f8:      	leaq	0x1a0(%rsp), %rdi
 5f85a00:      	movq	%r12, %rsi
 5f85a03:      	movl	$0x2, %edx
 5f85a08:      	callq	*%rax
 5f85a0a:      	movups	0x10(%r12), %xmm0
 5f85a10:      	movq	0x10(%r12), %rax
 5f85a15:      	movaps	%xmm0, 0x1b0(%rsp)
 5f85a1d:      	shlq	$0x4, %r15
 5f85a21:      	addq	%r14, %r15
 5f85a24:      	xorps	%xmm0, %xmm0
 5f85a27:      	movaps	%xmm0, 0x90(%rsp)
 5f85a2f:      	movaps	%xmm0, 0x80(%rsp)
 5f85a37:      	testq	%rax, %rax
 5f85a3a:      	je	0x5f85b7d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1cd>
 5f85a40:      	leaq	0x80(%rsp), %rdi
 5f85a48:      	leaq	0x1a0(%rsp), %rsi
 5f85a50:      	movl	$0x2, %edx
 5f85a55:      	callq	*%rax
 5f85a57:      	movaps	0x1b0(%rsp), %xmm0
 5f85a5f:      	movq	0x1b0(%rsp), %rax
 5f85a67:      	movaps	%xmm0, 0x90(%rsp)
 5f85a6f:      	xorps	%xmm0, %xmm0
 5f85a72:      	movaps	%xmm0, 0xf0(%rsp)
 5f85a7a:      	movaps	%xmm0, 0xe0(%rsp)
 5f85a82:      	testq	%rax, %rax
 5f85a85:      	je	0x5f85b8d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1dd>
 5f85a8b:      	leaq	0xe0(%rsp), %rdi
 5f85a93:      	leaq	0x80(%rsp), %rsi
 5f85a9b:      	movl	$0x2, %edx
 5f85aa0:      	callq	*%rax
 5f85aa2:      	movq	0x90(%rsp), %rcx
 5f85aaa:      	movq	0x98(%rsp), %rax
 5f85ab2:      	movq	%rax, 0xf8(%rsp)
 5f85aba:      	movq	%rcx, 0xf0(%rsp)
 5f85ac2:      	testq	%rcx, %rcx
 5f85ac5:      	je	0x5f85b8f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1df>
 5f85acb:      	leaq	0xf0(%rsp), %rdx
 5f85ad3:      	xorps	%xmm1, %xmm1
 5f85ad6:      	movups	%xmm1, (%rdx)
 5f85ad9:      	movaps	0xe0(%rsp), %xmm0
 5f85ae1:      	movaps	%xmm0, 0xb0(%rsp)
 5f85ae9:      	movq	%rcx, 0xc0(%rsp)
 5f85af1:      	movq	%rax, 0xc8(%rsp)
 5f85af9:      	movaps	%xmm1, 0x120(%rsp)
 5f85b01:      	movaps	%xmm1, 0x110(%rsp)
 5f85b09:      	leaq	0x110(%rsp), %rdi
 5f85b11:      	leaq	0xb0(%rsp), %rsi
 5f85b19:      	movl	$0x2, %edx
 5f85b1e:      	callq	*%rcx
 5f85b20:      	movq	0xc0(%rsp), %rcx
 5f85b28:      	movq	0xc8(%rsp), %rax
 5f85b30:      	movq	%rax, 0x128(%rsp)
 5f85b38:      	movq	%rcx, 0x120(%rsp)
 5f85b40:      	testq	%rcx, %rcx
 5f85b43:      	je	0x5f85bc0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x210>
 5f85b45:      	leaq	0x120(%rsp), %rdx
 5f85b4d:      	xorps	%xmm0, %xmm0
 5f85b50:      	movups	%xmm0, (%rdx)
 5f85b53:      	movaps	0x110(%rsp), %xmm0
 5f85b5b:      	movaps	%xmm0, (%rsp)
 5f85b5f:      	movq	%rcx, 0x10(%rsp)
 5f85b64:      	jmp	0x5f85bd0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x220>
 5f85b66:      	shlq	$0x4, %r15
 5f85b6a:      	addq	%r14, %r15
 5f85b6d:      	movaps	%xmm0, 0x90(%rsp)
 5f85b75:      	movaps	%xmm0, 0x80(%rsp)
 5f85b7d:      	movaps	%xmm0, 0xf0(%rsp)
 5f85b85:      	movaps	%xmm0, 0xe0(%rsp)
 5f85b8d:      	xorl	%eax, %eax
 5f85b8f:      	xorps	%xmm0, %xmm0
 5f85b92:      	movaps	%xmm0, 0xb0(%rsp)
 5f85b9a:      	movq	$0x0, 0xc0(%rsp)
 5f85ba6:      	movq	%rax, 0xc8(%rsp)
 5f85bae:      	movaps	%xmm0, 0x120(%rsp)
 5f85bb6:      	movaps	%xmm0, 0x110(%rsp)
 5f85bbe:      	xorl	%eax, %eax
 5f85bc0:      	xorps	%xmm0, %xmm0
 5f85bc3:      	movaps	%xmm0, (%rsp)
 5f85bc7:      	movq	$0x0, 0x10(%rsp)
 5f85bd0:      	movq	%r12, 0x148(%rsp)
 5f85bd8:      	movq	%rax, 0x18(%rsp)
 5f85bdd:      	movq	%r15, 0x40(%rsp)
 5f85be2:      	subq	%r14, %r15
 5f85be5:      	movq	%r15, %r13
 5f85be8:      	sarq	$0x6, %r13
 5f85bec:      	testq	%r13, %r13
 5f85bef:      	movl	%ebx, 0x4c(%rsp)
 5f85bf3:      	movq	%rbp, 0x28(%rsp)
 5f85bf8:      	jle	0x5f85cf7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x347>
 5f85bfe:      	incq	%r13
 5f85c01:      	leaq	0x20(%r14), %rbx
 5f85c05:      	movq	%rsp, %r12
 5f85c08:      	leaq	0x50(%rsp), %rbp
 5f85c0d:      	nopl	(%rax)
 5f85c10:      	movq	-0x20(%rbx), %rax
 5f85c14:      	movl	-0x18(%rbx), %ecx
 5f85c17:      	movq	%rax, 0x50(%rsp)
 5f85c1c:      	movl	%ecx, 0x58(%rsp)
 5f85c20:      	cmpq	$0x0, 0x10(%rsp)
 5f85c26:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85c2c:      	movq	%r12, %rdi
 5f85c2f:      	movq	%rbp, %rsi
 5f85c32:      	callq	*0x18(%rsp)
 5f85c36:      	testb	%al, %al
 5f85c38:      	je	0x5f85dba <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x40a>
 5f85c3e:      	movq	-0x10(%rbx), %rax
 5f85c42:      	movl	-0x8(%rbx), %ecx
 5f85c45:      	movq	%rax, 0x50(%rsp)
 5f85c4a:      	movl	%ecx, 0x58(%rsp)
 5f85c4e:      	cmpq	$0x0, 0x10(%rsp)
 5f85c54:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85c5a:      	movq	%r12, %rdi
 5f85c5d:      	movq	%rbp, %rsi
 5f85c60:      	callq	*0x18(%rsp)
 5f85c64:      	testb	%al, %al
 5f85c66:      	je	0x5f85dc0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x410>
 5f85c6c:      	movq	(%rbx), %rax
 5f85c6f:      	movl	0x8(%rbx), %ecx
 5f85c72:      	movq	%rax, 0x50(%rsp)
 5f85c77:      	movl	%ecx, 0x58(%rsp)
 5f85c7b:      	cmpq	$0x0, 0x10(%rsp)
 5f85c81:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85c87:      	movq	%r12, %rdi
 5f85c8a:      	movq	%rbp, %rsi
 5f85c8d:      	callq	*0x18(%rsp)
 5f85c91:      	testb	%al, %al
 5f85c93:      	je	0x5f85dca <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41a>
 5f85c99:      	movq	0x10(%rbx), %rax
 5f85c9d:      	movl	0x18(%rbx), %ecx
 5f85ca0:      	movq	%rax, 0x50(%rsp)
 5f85ca5:      	movl	%ecx, 0x58(%rsp)
 5f85ca9:      	cmpq	$0x0, 0x10(%rsp)
 5f85caf:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85cb5:      	movq	%r12, %rdi
 5f85cb8:      	movq	%rbp, %rsi
 5f85cbb:      	callq	*0x18(%rsp)
 5f85cbf:      	testb	%al, %al
 5f85cc1:      	je	0x5f85dc6 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x416>
 5f85cc7:      	decq	%r13
 5f85cca:      	addq	$0x40, %rbx
 5f85cce:      	addq	$-0x40, %r15
 5f85cd2:      	cmpq	$0x1, %r13
 5f85cd6:      	jg	0x5f85c10 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x260>
 5f85cdc:      	addq	$-0x20, %rbx
 5f85ce0:      	movq	%rbx, %r12
 5f85ce3:      	movq	0x28(%rsp), %rbp
 5f85ce8:      	sarq	$0x4, %r15
 5f85cec:      	cmpq	$0x1, %r15
 5f85cf0:      	jne	0x5f85d04 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x354>
 5f85cf2:      	jmp	0x5f85d7d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3cd>
 5f85cf7:      	movq	%r14, %r12
 5f85cfa:      	sarq	$0x4, %r15
 5f85cfe:      	cmpq	$0x1, %r15
 5f85d02:      	je	0x5f85d7d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3cd>
 5f85d04:      	cmpq	$0x2, %r15
 5f85d08:      	je	0x5f85d4b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x39b>
 5f85d0a:      	movq	0x40(%rsp), %rbx
 5f85d0f:      	cmpq	$0x3, %r15
 5f85d13:      	jne	0x5f85dcf <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41f>
 5f85d19:      	movq	(%r12), %rax
 5f85d1d:      	movl	0x8(%r12), %ecx
 5f85d22:      	movq	%rax, 0x50(%rsp)
 5f85d27:      	movl	%ecx, 0x58(%rsp)
 5f85d2b:      	cmpq	$0x0, 0x10(%rsp)
 5f85d31:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85d37:      	movq	%rsp, %rdi
 5f85d3a:      	leaq	0x50(%rsp), %rsi
 5f85d3f:      	callq	*0x18(%rsp)
 5f85d43:      	testb	%al, %al
 5f85d45:      	je	0x5f85db5 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x405>
 5f85d47:      	addq	$0x10, %r12
 5f85d4b:      	movq	(%r12), %rax
 5f85d4f:      	movl	0x8(%r12), %ecx
 5f85d54:      	movq	%rax, 0x50(%rsp)
 5f85d59:      	movl	%ecx, 0x58(%rsp)
 5f85d5d:      	cmpq	$0x0, 0x10(%rsp)
 5f85d63:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85d69:      	movq	%rsp, %rdi
 5f85d6c:      	leaq	0x50(%rsp), %rsi
 5f85d71:      	callq	*0x18(%rsp)
 5f85d75:      	testb	%al, %al
 5f85d77:      	je	0x5f85db5 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x405>
 5f85d79:      	addq	$0x10, %r12
 5f85d7d:      	movq	%r12, %rbx
 5f85d80:      	movq	(%r12), %rax
 5f85d84:      	movl	0x8(%r12), %ecx
 5f85d89:      	movq	%rax, 0x50(%rsp)
 5f85d8e:      	movl	%ecx, 0x58(%rsp)
 5f85d92:      	cmpq	$0x0, 0x10(%rsp)
 5f85d98:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f85d9e:      	movq	%rsp, %rdi
 5f85da1:      	leaq	0x50(%rsp), %rsi
 5f85da6:      	callq	*0x18(%rsp)
 5f85daa:      	testb	%al, %al
 5f85dac:      	je	0x5f85dcf <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41f>
 5f85dae:      	movq	0x40(%rsp), %rbx
 5f85db3:      	jmp	0x5f85dcf <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41f>
 5f85db5:      	movq	%r12, %rbx
 5f85db8:      	jmp	0x5f85dcf <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41f>
 5f85dba:      	addq	$-0x20, %rbx
 5f85dbe:      	jmp	0x5f85dca <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41a>
 5f85dc0:      	addq	$-0x10, %rbx
 5f85dc4:      	jmp	0x5f85dca <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x41a>
 5f85dc6:      	addq	$0x10, %rbx
 5f85dca:      	movq	0x28(%rsp), %rbp
 5f85dcf:      	movq	0x10(%rsp), %rax
 5f85dd4:      	testq	%rax, %rax
 5f85dd7:      	je	0x5f85de6 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x436>
 5f85dd9:      	movq	%rsp, %rdi
 5f85ddc:      	movq	%rdi, %rsi
 5f85ddf:      	movl	$0x3, %edx
 5f85de4:      	callq	*%rax
 5f85de6:      	movq	0x120(%rsp), %rax
 5f85dee:      	testq	%rax, %rax
 5f85df1:      	movq	0x40(%rsp), %r15
 5f85df6:      	movq	0x148(%rsp), %r12
 5f85dfe:      	je	0x5f85e12 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x462>
 5f85e00:      	leaq	0x110(%rsp), %rdi
 5f85e08:      	movq	%rdi, %rsi
 5f85e0b:      	movl	$0x3, %edx
 5f85e10:      	callq	*%rax
 5f85e12:      	movq	0xc0(%rsp), %rax
 5f85e1a:      	testq	%rax, %rax
 5f85e1d:      	je	0x5f85e31 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x481>
 5f85e1f:      	leaq	0xb0(%rsp), %rdi
 5f85e27:      	movq	%rdi, %rsi
 5f85e2a:      	movl	$0x3, %edx
 5f85e2f:      	callq	*%rax
 5f85e31:      	movq	0xf0(%rsp), %rax
 5f85e39:      	testq	%rax, %rax
 5f85e3c:      	je	0x5f85e50 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4a0>
 5f85e3e:      	leaq	0xe0(%rsp), %rdi
 5f85e46:      	movq	%rdi, %rsi
 5f85e49:      	movl	$0x3, %edx
 5f85e4e:      	callq	*%rax
 5f85e50:      	movq	0x90(%rsp), %rax
 5f85e58:      	testq	%rax, %rax
 5f85e5b:      	je	0x5f85e6f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4bf>
 5f85e5d:      	leaq	0x80(%rsp), %rdi
 5f85e65:      	movq	%rdi, %rsi
 5f85e68:      	movl	$0x3, %edx
 5f85e6d:      	callq	*%rax
 5f85e6f:      	movq	0x1b0(%rsp), %rax
 5f85e77:      	testq	%rax, %rax
 5f85e7a:      	je	0x5f85e8e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4de>
 5f85e7c:      	leaq	0x1a0(%rsp), %rdi
 5f85e84:      	movq	%rdi, %rsi
 5f85e87:      	movl	$0x3, %edx
 5f85e8c:      	callq	*%rax
 5f85e8e:      	cmpq	%r15, %rbx
 5f85e91:      	je	0x5f864cc <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb1c>
 5f85e97:      	xorps	%xmm0, %xmm0
 5f85e9a:      	movaps	%xmm0, 0x160(%rsp)
 5f85ea2:      	movaps	%xmm0, 0x150(%rsp)
 5f85eaa:      	movq	0x10(%r12), %rax
 5f85eaf:      	testq	%rax, %rax
 5f85eb2:      	je	0x5f860a7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x6f7>
 5f85eb8:      	leaq	0x150(%rsp), %rdi
 5f85ec0:      	movq	%r12, %rsi
 5f85ec3:      	movl	$0x2, %edx
 5f85ec8:      	callq	*%rax
 5f85eca:      	movups	0x10(%r12), %xmm0
 5f85ed0:      	movq	0x10(%r12), %rax
 5f85ed5:      	movaps	%xmm0, 0x160(%rsp)
 5f85edd:      	movq	%rbx, 0x170(%rsp)
 5f85ee5:      	xorps	%xmm0, %xmm0
 5f85ee8:      	movaps	%xmm0, 0x60(%rsp)
 5f85eed:      	movaps	%xmm0, 0x50(%rsp)
 5f85ef2:      	testq	%rax, %rax
 5f85ef5:      	je	0x5f860b9 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x709>
 5f85efb:      	leaq	0x50(%rsp), %rdi
 5f85f00:      	leaq	0x150(%rsp), %rsi
 5f85f08:      	movl	$0x2, %edx
 5f85f0d:      	callq	*%rax
 5f85f0f:      	movaps	0x160(%rsp), %xmm0
 5f85f17:      	movq	0x160(%rsp), %rcx
 5f85f1f:      	movq	0x170(%rsp), %rax
 5f85f27:      	movaps	%xmm0, 0x60(%rsp)
 5f85f2c:      	movq	%rax, 0x70(%rsp)
 5f85f31:      	xorps	%xmm0, %xmm0
 5f85f34:      	movaps	%xmm0, 0x90(%rsp)
 5f85f3c:      	movaps	%xmm0, 0x80(%rsp)
 5f85f44:      	testq	%rcx, %rcx
 5f85f47:      	je	0x5f860d1 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x721>
 5f85f4d:      	leaq	0x80(%rsp), %rdi
 5f85f55:      	leaq	0x50(%rsp), %rsi
 5f85f5a:      	movl	$0x2, %edx
 5f85f5f:      	callq	*%rcx
 5f85f61:      	movaps	0x60(%rsp), %xmm0
 5f85f66:      	movq	0x60(%rsp), %rcx
 5f85f6b:      	movq	0x70(%rsp), %rax
 5f85f70:      	movaps	%xmm0, 0x90(%rsp)
 5f85f78:      	movq	%rax, 0xa0(%rsp)
 5f85f80:      	xorps	%xmm0, %xmm0
 5f85f83:      	movaps	%xmm0, 0xf0(%rsp)
 5f85f8b:      	movaps	%xmm0, 0xe0(%rsp)
 5f85f93:      	testq	%rcx, %rcx
 5f85f96:      	je	0x5f860e9 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x739>
 5f85f9c:      	leaq	0xe0(%rsp), %rdi
 5f85fa4:      	leaq	0x80(%rsp), %rsi
 5f85fac:      	movl	$0x2, %edx
 5f85fb1:      	callq	*%rcx
 5f85fb3:      	movq	0x90(%rsp), %r8
 5f85fbb:      	movq	0x98(%rsp), %rcx
 5f85fc3:      	movq	%rcx, 0xf8(%rsp)
 5f85fcb:      	movq	%r8, 0xf0(%rsp)
 5f85fd3:      	movq	0xa0(%rsp), %rax
 5f85fdb:      	movq	%rax, 0x100(%rsp)
 5f85fe3:      	testq	%r8, %r8
 5f85fe6:      	je	0x5f860f3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x743>
 5f85fec:      	leaq	0xf0(%rsp), %rdx
 5f85ff4:      	xorps	%xmm1, %xmm1
 5f85ff7:      	movups	%xmm1, (%rdx)
 5f85ffa:      	movaps	0xe0(%rsp), %xmm0
 5f86002:      	movaps	%xmm0, 0xb0(%rsp)
 5f8600a:      	movq	%r8, 0xc0(%rsp)
 5f86012:      	movq	%rcx, 0xc8(%rsp)
 5f8601a:      	movq	%rax, 0xd0(%rsp)
 5f86022:      	movaps	%xmm1, 0x120(%rsp)
 5f8602a:      	movaps	%xmm1, 0x110(%rsp)
 5f86032:      	leaq	0x110(%rsp), %rdi
 5f8603a:      	leaq	0xb0(%rsp), %rsi
 5f86042:      	movl	$0x2, %edx
 5f86047:      	callq	*%r8
 5f8604a:      	movq	0xc0(%rsp), %rdx
 5f86052:      	movq	0xc8(%rsp), %rcx
 5f8605a:      	movq	%rcx, 0x128(%rsp)
 5f86062:      	movq	%rdx, 0x120(%rsp)
 5f8606a:      	movq	0xd0(%rsp), %rax
 5f86072:      	movq	%rax, 0x130(%rsp)
 5f8607a:      	testq	%rdx, %rdx
 5f8607d:      	je	0x5f86134 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x784>
 5f86083:      	leaq	0x120(%rsp), %rsi
 5f8608b:      	xorps	%xmm0, %xmm0
 5f8608e:      	movups	%xmm0, (%rsi)
 5f86091:      	movaps	0x110(%rsp), %xmm0
 5f86099:      	movaps	%xmm0, (%rsp)
 5f8609d:      	movq	%rdx, 0x10(%rsp)
 5f860a2:      	jmp	0x5f86144 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x794>
 5f860a7:      	movq	%rbx, 0x170(%rsp)
 5f860af:      	movaps	%xmm0, 0x60(%rsp)
 5f860b4:      	movaps	%xmm0, 0x50(%rsp)
 5f860b9:      	movq	%rbx, 0x70(%rsp)
 5f860be:      	movaps	%xmm0, 0x90(%rsp)
 5f860c6:      	movaps	%xmm0, 0x80(%rsp)
 5f860ce:      	movq	%rbx, %rax
 5f860d1:      	movq	%rax, 0xa0(%rsp)
 5f860d9:      	movaps	%xmm0, 0xf0(%rsp)
 5f860e1:      	movaps	%xmm0, 0xe0(%rsp)
 5f860e9:      	movq	%rax, 0x100(%rsp)
 5f860f1:      	xorl	%ecx, %ecx
 5f860f3:      	xorps	%xmm0, %xmm0
 5f860f6:      	movaps	%xmm0, 0xb0(%rsp)
 5f860fe:      	movq	$0x0, 0xc0(%rsp)
 5f8610a:      	movq	%rcx, 0xc8(%rsp)
 5f86112:      	movq	%rax, 0xd0(%rsp)
 5f8611a:      	movaps	%xmm0, 0x120(%rsp)
 5f86122:      	movaps	%xmm0, 0x110(%rsp)
 5f8612a:      	movq	%rax, 0x130(%rsp)
 5f86132:      	xorl	%ecx, %ecx
 5f86134:      	xorps	%xmm0, %xmm0
 5f86137:      	movaps	%xmm0, (%rsp)
 5f8613b:      	movq	$0x0, 0x10(%rsp)
 5f86144:      	movq	%rcx, 0x18(%rsp)
 5f86149:      	movq	%rax, 0x20(%rsp)
 5f8614e:      	movq	0x140(%rsp), %r13
 5f86156:      	movq	%r13, %rbp
 5f86159:      	shrq	$0x2, %rbp
 5f8615d:      	movq	%r14, %r12
 5f86160:      	je	0x5f862d7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x927>
 5f86166:      	incq	%rbp
 5f86169:      	movq	%r15, %r13
 5f8616c:      	leaq	0x20(%r14), %r15
 5f86170:      	subq	%r14, %r13
 5f86173:      	leaq	0x30(%rsp), %r12
 5f86178:      	jmp	0x5f86195 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7e5>
 5f8617a:      	nopw	(%rax,%rax)
 5f86180:      	decq	%rbp
 5f86183:      	addq	$0x40, %r15
 5f86187:      	addq	$-0x40, %r13
 5f8618b:      	cmpq	$0x1, %rbp
 5f8618f:      	jle	0x5f862c7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x917>
 5f86195:      	movq	-0x20(%r15), %rcx
 5f86199:      	movl	-0x18(%r15), %eax
 5f8619d:      	movq	0x20(%rsp), %rdx
 5f861a2:      	cmpq	(%rdx), %rcx
 5f861a5:      	jne	0x5f861ac <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7fc>
 5f861a7:      	cmpl	0x8(%rdx), %eax
 5f861aa:      	je	0x5f861de <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x82e>
 5f861ac:      	movq	%rcx, 0x30(%rsp)
 5f861b1:      	movl	%eax, 0x38(%rsp)
 5f861b5:      	cmpq	$0x0, 0x10(%rsp)
 5f861bb:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f861c1:      	movq	%rsp, %rdi
 5f861c4:      	movq	%r12, %rsi
 5f861c7:      	callq	*0x18(%rsp)
 5f861cb:      	testb	%al, %al
 5f861cd:      	je	0x5f863dd <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa2d>
 5f861d3:      	movq	0x20(%rsp), %rax
 5f861d8:      	movq	(%rax), %rcx
 5f861db:      	movl	0x8(%rax), %eax
 5f861de:      	movq	-0x10(%r15), %rdx
 5f861e2:      	movl	-0x8(%r15), %esi
 5f861e6:      	cmpq	%rcx, %rdx
 5f861e9:      	sete	%dil
 5f861ed:      	cmpl	%eax, %esi
 5f861ef:      	sete	%r8b
 5f861f3:      	testb	%r8b, %dil
 5f861f6:      	jne	0x5f8622a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x87a>
 5f861f8:      	movq	%rdx, 0x30(%rsp)
 5f861fd:      	movl	%esi, 0x38(%rsp)
 5f86201:      	cmpq	$0x0, 0x10(%rsp)
 5f86207:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f8620d:      	movq	%rsp, %rdi
 5f86210:      	movq	%r12, %rsi
 5f86213:      	callq	*0x18(%rsp)
 5f86217:      	testb	%al, %al
 5f86219:      	je	0x5f863e3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa33>
 5f8621f:      	movq	0x20(%rsp), %rax
 5f86224:      	movq	(%rax), %rcx
 5f86227:      	movl	0x8(%rax), %eax
 5f8622a:      	movq	(%r15), %rdx
 5f8622d:      	movl	0x8(%r15), %esi
 5f86231:      	cmpq	%rcx, %rdx
 5f86234:      	jne	0x5f86250 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8a0>
 5f86236:      	cmpl	%eax, %esi
 5f86238:      	jne	0x5f86250 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8a0>
 5f8623a:      	movq	0x10(%r15), %rdx
 5f8623e:      	movl	0x18(%r15), %esi
 5f86242:      	cmpq	%rcx, %rdx
 5f86245:      	je	0x5f8628f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8df>
 5f86247:      	jmp	0x5f86297 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8e7>
 5f86249:      	nopl	(%rax)
 5f86250:      	movq	%rdx, 0x30(%rsp)
 5f86255:      	movl	%esi, 0x38(%rsp)
 5f86259:      	cmpq	$0x0, 0x10(%rsp)
 5f8625f:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f86265:      	movq	%rsp, %rdi
 5f86268:      	movq	%r12, %rsi
 5f8626b:      	callq	*0x18(%rsp)
 5f8626f:      	testb	%al, %al
 5f86271:      	je	0x5f863e7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa37>
 5f86277:      	movq	0x20(%rsp), %rax
 5f8627c:      	movq	(%rax), %rcx
 5f8627f:      	movl	0x8(%rax), %eax
 5f86282:      	movq	0x10(%r15), %rdx
 5f86286:      	movl	0x18(%r15), %esi
 5f8628a:      	cmpq	%rcx, %rdx
 5f8628d:      	jne	0x5f86297 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8e7>
 5f8628f:      	cmpl	%eax, %esi
 5f86291:      	je	0x5f86180 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7d0>
 5f86297:      	movq	%rdx, 0x30(%rsp)
 5f8629c:      	movl	%esi, 0x38(%rsp)
 5f862a0:      	cmpq	$0x0, 0x10(%rsp)
 5f862a6:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f862ac:      	movq	%rsp, %rdi
 5f862af:      	movq	%r12, %rsi
 5f862b2:      	callq	*0x18(%rsp)
 5f862b6:      	testb	%al, %al
 5f862b8:      	jne	0x5f86180 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7d0>
 5f862be:      	addq	$0x10, %r15
 5f862c2:      	jmp	0x5f863e7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa37>
 5f862c7:      	sarq	$0x4, %r13
 5f862cb:      	addq	$-0x20, %r15
 5f862cf:      	movq	%r15, %r12
 5f862d2:      	movq	0x40(%rsp), %r15
 5f862d7:      	cmpq	$0x1, %r13
 5f862db:      	je	0x5f86382 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9d2>
 5f862e1:      	cmpq	$0x2, %r13
 5f862e5:      	movq	0x28(%rsp), %rbp
 5f862ea:      	je	0x5f8633b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x98b>
 5f862ec:      	cmpq	$0x3, %r13
 5f862f0:      	jne	0x5f863ec <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa3c>
 5f862f6:      	movq	(%r12), %rax
 5f862fa:      	movl	0x8(%r12), %ecx
 5f862ff:      	movq	0x20(%rsp), %rdx
 5f86304:      	cmpq	(%rdx), %rax
 5f86307:      	jne	0x5f8630e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x95e>
 5f86309:      	cmpl	0x8(%rdx), %ecx
 5f8630c:      	je	0x5f86337 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x987>
 5f8630e:      	movq	%rax, 0x30(%rsp)
 5f86313:      	movl	%ecx, 0x38(%rsp)
 5f86317:      	cmpq	$0x0, 0x10(%rsp)
 5f8631d:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f86323:      	movq	%rsp, %rdi
 5f86326:      	leaq	0x30(%rsp), %rsi
 5f8632b:      	callq	*0x18(%rsp)
 5f8632f:      	testb	%al, %al
 5f86331:      	je	0x5f865ce <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc1e>
 5f86337:      	addq	$0x10, %r12
 5f8633b:      	movq	(%r12), %rax
 5f8633f:      	movl	0x8(%r12), %ecx
 5f86344:      	movq	0x20(%rsp), %rdx
 5f86349:      	cmpq	(%rdx), %rax
 5f8634c:      	jne	0x5f86353 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9a3>
 5f8634e:      	cmpl	0x8(%rdx), %ecx
 5f86351:      	je	0x5f8637c <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9cc>
 5f86353:      	movq	%rax, 0x30(%rsp)
 5f86358:      	movl	%ecx, 0x38(%rsp)
 5f8635c:      	cmpq	$0x0, 0x10(%rsp)
 5f86362:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f86368:      	movq	%rsp, %rdi
 5f8636b:      	leaq	0x30(%rsp), %rsi
 5f86370:      	callq	*0x18(%rsp)
 5f86374:      	testb	%al, %al
 5f86376:      	je	0x5f865ce <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc1e>
 5f8637c:      	addq	$0x10, %r12
 5f86380:      	jmp	0x5f86387 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9d7>
 5f86382:      	movq	0x28(%rsp), %rbp
 5f86387:      	movq	(%r12), %rax
 5f8638b:      	movl	0x8(%r12), %ecx
 5f86390:      	movq	0x20(%rsp), %rdx
 5f86395:      	cmpq	(%rdx), %rax
 5f86398:      	jne	0x5f863a4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9f4>
 5f8639a:      	movq	0x40(%rsp), %r15
 5f8639f:      	cmpl	0x8(%rdx), %ecx
 5f863a2:      	je	0x5f863ec <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa3c>
 5f863a4:      	movq	%rax, 0x30(%rsp)
 5f863a9:      	movl	%ecx, 0x38(%rsp)
 5f863ad:      	cmpq	$0x0, 0x10(%rsp)
 5f863b3:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f863b9:      	movq	%rsp, %rdi
 5f863bc:      	leaq	0x30(%rsp), %rsi
 5f863c1:      	callq	*0x18(%rsp)
 5f863c5:      	movq	%r12, %r15
 5f863c8:      	testb	%al, %al
 5f863ca:      	je	0x5f863ec <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa3c>
 5f863cc:      	movq	0x40(%rsp), %r15
 5f863d1:      	movq	0x10(%rsp), %rax
 5f863d6:      	testq	%rax, %rax
 5f863d9:      	jne	0x5f863f6 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa46>
 5f863db:      	jmp	0x5f86403 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa53>
 5f863dd:      	addq	$-0x20, %r15
 5f863e1:      	jmp	0x5f863e7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa37>
 5f863e3:      	addq	$-0x10, %r15
 5f863e7:      	movq	0x28(%rsp), %rbp
 5f863ec:      	movq	0x10(%rsp), %rax
 5f863f1:      	testq	%rax, %rax
 5f863f4:      	je	0x5f86403 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa53>
 5f863f6:      	movq	%rsp, %rdi
 5f863f9:      	movq	%rdi, %rsi
 5f863fc:      	movl	$0x3, %edx
 5f86401:      	callq	*%rax
 5f86403:      	movq	0x120(%rsp), %rax
 5f8640b:      	testq	%rax, %rax
 5f8640e:      	movq	0x148(%rsp), %r12
 5f86416:      	je	0x5f8642a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa7a>
 5f86418:      	leaq	0x110(%rsp), %rdi
 5f86420:      	movq	%rdi, %rsi
 5f86423:      	movl	$0x3, %edx
 5f86428:      	callq	*%rax
 5f8642a:      	movq	0xc0(%rsp), %rax
 5f86432:      	testq	%rax, %rax
 5f86435:      	je	0x5f86449 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa99>
 5f86437:      	leaq	0xb0(%rsp), %rdi
 5f8643f:      	movq	%rdi, %rsi
 5f86442:      	movl	$0x3, %edx
 5f86447:      	callq	*%rax
 5f86449:      	movq	0xf0(%rsp), %rax
 5f86451:      	testq	%rax, %rax
 5f86454:      	je	0x5f86468 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xab8>
 5f86456:      	leaq	0xe0(%rsp), %rdi
 5f8645e:      	movq	%rdi, %rsi
 5f86461:      	movl	$0x3, %edx
 5f86466:      	callq	*%rax
 5f86468:      	movq	0x90(%rsp), %rax
 5f86470:      	testq	%rax, %rax
 5f86473:      	je	0x5f86487 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xad7>
 5f86475:      	leaq	0x80(%rsp), %rdi
 5f8647d:      	movq	%rdi, %rsi
 5f86480:      	movl	$0x3, %edx
 5f86485:      	callq	*%rax
 5f86487:      	movq	0x60(%rsp), %rax
 5f8648c:      	testq	%rax, %rax
 5f8648f:      	je	0x5f864a0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xaf0>
 5f86491:      	leaq	0x50(%rsp), %rdi
 5f86496:      	movq	%rdi, %rsi
 5f86499:      	movl	$0x3, %edx
 5f8649e:      	callq	*%rax
 5f864a0:      	movq	0x160(%rsp), %rax
 5f864a8:      	testq	%rax, %rax
 5f864ab:      	je	0x5f864bf <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb0f>
 5f864ad:      	leaq	0x150(%rsp), %rdi
 5f864b5:      	movq	%rdi, %rsi
 5f864b8:      	movl	$0x3, %edx
 5f864bd:      	callq	*%rax
 5f864bf:      	movq	0x40(%rsp), %rax
 5f864c4:      	cmpq	%r15, %rax
 5f864c7:      	movq	%rax, %r15
 5f864ca:      	je	0x5f864d6 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb26>
 5f864cc:      	testq	%rbp, %rbp
 5f864cf:      	jne	0x5f864e8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb38>
 5f864d1:      	jmp	0x5f865bc <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc0c>
 5f864d6:      	movq	(%rbx), %rax
 5f864d9:      	testq	%rax, %rax
 5f864dc:      	je	0x5f864cc <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb1c>
 5f864de:      	movl	0x8(%rbx), %ecx
 5f864e1:      	movl	%ecx, 0x4c(%rsp)
 5f864e5:      	movq	%rax, %rbp
 5f864e8:      	xorps	%xmm0, %xmm0
 5f864eb:      	movaps	%xmm0, 0x190(%rsp)
 5f864f3:      	movaps	%xmm0, 0x180(%rsp)
 5f864fb:      	movq	0x10(%r12), %rax
 5f86500:      	testq	%rax, %rax
 5f86503:      	je	0x5f8653b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb8b>
 5f86505:      	leaq	0x180(%rsp), %rdi
 5f8650d:      	movq	%r12, %rsi
 5f86510:      	movl	$0x2, %edx
 5f86515:      	callq	*%rax
 5f86517:      	movups	0x10(%r12), %xmm0
 5f8651d:      	movq	0x10(%r12), %rax
 5f86522:      	movaps	%xmm0, 0x190(%rsp)
 5f8652a:      	movl	0x4c(%rsp), %ebx
 5f8652e:      	cmpq	$0x0, 0x140(%rsp)
 5f86537:      	jne	0x5f8654c <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb9c>
 5f86539:      	jmp	0x5f865a5 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbf5>
 5f8653b:      	xorl	%eax, %eax
 5f8653d:      	movl	0x4c(%rsp), %ebx
 5f86541:      	cmpq	$0x0, 0x140(%rsp)
 5f8654a:      	je	0x5f865a5 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbf5>
 5f8654c:      	leaq	0x180(%rsp), %r12
 5f86554:      	movq	%rsp, %r13
 5f86557:      	jmp	0x5f86569 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbb9>
 5f86559:      	nopl	(%rax)
 5f86560:      	addq	$0x10, %r14
 5f86564:      	cmpq	%r15, %r14
 5f86567:      	je	0x5f8659d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbed>
 5f86569:      	movq	(%r14), %rax
 5f8656c:      	movl	0x8(%r14), %ecx
 5f86570:      	movq	%rax, (%rsp)
 5f86574:      	movl	%ecx, 0x8(%rsp)
 5f86578:      	cmpq	$0x0, 0x190(%rsp)
 5f86581:      	je	0x5f865e4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc34>
 5f86583:      	movq	%r12, %rdi
 5f86586:      	movq	%r13, %rsi
 5f86589:      	callq	*0x198(%rsp)
 5f86590:      	testb	%al, %al
 5f86592:      	je	0x5f86560 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbb0>
 5f86594:      	movq	%rbp, (%r14)
 5f86597:      	movl	%ebx, 0x8(%r14)
 5f8659b:      	jmp	0x5f86560 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbb0>
 5f8659d:      	movq	0x190(%rsp), %rax
 5f865a5:      	testq	%rax, %rax
 5f865a8:      	je	0x5f865bc <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc0c>
 5f865aa:      	leaq	0x180(%rsp), %rdi
 5f865b2:      	movq	%rdi, %rsi
 5f865b5:      	movl	$0x3, %edx
 5f865ba:      	callq	*%rax
 5f865bc:      	addq	$0x1c8, %rsp            # imm = 0x1C8
 5f865c3:      	popq	%rbx
 5f865c4:      	popq	%r12
 5f865c6:      	popq	%r13
 5f865c8:      	popq	%r14
 5f865ca:      	popq	%r15
 5f865cc:      	popq	%rbp
 5f865cd:      	retq
 5f865ce:      	movq	%r12, %r15
 5f865d1:      	movq	0x10(%rsp), %rax
 5f865d6:      	testq	%rax, %rax
 5f865d9:      	jne	0x5f863f6 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa46>
 5f865df:      	jmp	0x5f86403 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa53>
 5f865e4:      	callq	0x828a8b0 <_ZSt25__throw_bad_function_callv@plt>
