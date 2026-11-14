
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000005f85a30 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_>:
 5f85a30:      	pushq	%rbp
 5f85a31:      	pushq	%r15
 5f85a33:      	pushq	%r14
 5f85a35:      	pushq	%r13
 5f85a37:      	pushq	%r12
 5f85a39:      	pushq	%rbx
 5f85a3a:      	subq	$0x1c8, %rsp            # imm = 0x1C8
 5f85a41:      	movq	%rcx, 0x1c0(%rsp)
 5f85a49:      	movq	%rsi, %rbp
 5f85a4c:      	movq	%rdi, %r14
 5f85a4f:      	xorps	%xmm0, %xmm0
 5f85a52:      	movaps	%xmm0, 0x1b0(%rsp)
 5f85a5a:      	movaps	%xmm0, 0x1a0(%rsp)
 5f85a62:      	movq	0x10(%rdx), %rax
 5f85a66:      	testq	%rax, %rax
 5f85a69:      	movq	%rsi, 0x138(%rsp)
 5f85a71:      	movl	%r8d, 0xc(%rsp)
 5f85a76:      	movq	%rdx, 0x140(%rsp)
 5f85a7e:      	je	0x5f85bf4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1c4>
 5f85a84:      	movq	%rdx, %r15
 5f85a87:      	leaq	0x1a0(%rsp), %rdi
 5f85a8f:      	movq	%rdx, %rsi
 5f85a92:      	movl	$0x2, %edx
 5f85a97:      	callq	*%rax
 5f85a99:      	movups	0x10(%r15), %xmm0
 5f85a9e:      	movq	0x10(%r15), %rax
 5f85aa2:      	movaps	%xmm0, 0x1b0(%rsp)
 5f85aaa:      	shlq	$0x4, %rbp
 5f85aae:      	addq	%r14, %rbp
 5f85ab1:      	xorps	%xmm0, %xmm0
 5f85ab4:      	movaps	%xmm0, 0x90(%rsp)
 5f85abc:      	movaps	%xmm0, 0x80(%rsp)
 5f85ac4:      	testq	%rax, %rax
 5f85ac7:      	je	0x5f85c0b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1db>
 5f85acd:      	leaq	0x80(%rsp), %rdi
 5f85ad5:      	leaq	0x1a0(%rsp), %rsi
 5f85add:      	movl	$0x2, %edx
 5f85ae2:      	callq	*%rax
 5f85ae4:      	movaps	0x1b0(%rsp), %xmm0
 5f85aec:      	movq	0x1b0(%rsp), %rax
 5f85af4:      	movaps	%xmm0, 0x90(%rsp)
 5f85afc:      	xorps	%xmm0, %xmm0
 5f85aff:      	movaps	%xmm0, 0xf0(%rsp)
 5f85b07:      	movaps	%xmm0, 0xe0(%rsp)
 5f85b0f:      	testq	%rax, %rax
 5f85b12:      	je	0x5f85c1b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1eb>
 5f85b18:      	leaq	0xe0(%rsp), %rdi
 5f85b20:      	leaq	0x80(%rsp), %rsi
 5f85b28:      	movl	$0x2, %edx
 5f85b2d:      	callq	*%rax
 5f85b2f:      	movq	0x90(%rsp), %rcx
 5f85b37:      	movq	0x98(%rsp), %rax
 5f85b3f:      	movq	%rax, 0xf8(%rsp)
 5f85b47:      	movq	%rcx, 0xf0(%rsp)
 5f85b4f:      	testq	%rcx, %rcx
 5f85b52:      	je	0x5f85c1d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x1ed>
 5f85b58:      	leaq	0xf0(%rsp), %rdx
 5f85b60:      	xorps	%xmm1, %xmm1
 5f85b63:      	movups	%xmm1, (%rdx)
 5f85b66:      	movaps	0xe0(%rsp), %xmm0
 5f85b6e:      	movaps	%xmm0, 0xb0(%rsp)
 5f85b76:      	movq	%rcx, 0xc0(%rsp)
 5f85b7e:      	movq	%rax, 0xc8(%rsp)
 5f85b86:      	movaps	%xmm1, 0x120(%rsp)
 5f85b8e:      	movaps	%xmm1, 0x110(%rsp)
 5f85b96:      	leaq	0x110(%rsp), %rdi
 5f85b9e:      	leaq	0xb0(%rsp), %rsi
 5f85ba6:      	movl	$0x2, %edx
 5f85bab:      	callq	*%rcx
 5f85bad:      	movq	0xc0(%rsp), %rcx
 5f85bb5:      	movq	0xc8(%rsp), %rax
 5f85bbd:      	movq	%rax, 0x128(%rsp)
 5f85bc5:      	movq	%rcx, 0x120(%rsp)
 5f85bcd:      	testq	%rcx, %rcx
 5f85bd0:      	je	0x5f85c4e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x21e>
 5f85bd2:      	leaq	0x120(%rsp), %rdx
 5f85bda:      	xorps	%xmm0, %xmm0
 5f85bdd:      	movups	%xmm0, (%rdx)
 5f85be0:      	movaps	0x110(%rsp), %xmm0
 5f85be8:      	movaps	%xmm0, 0x10(%rsp)
 5f85bed:      	movq	%rcx, 0x20(%rsp)
 5f85bf2:      	jmp	0x5f85c5f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x22f>
 5f85bf4:      	shlq	$0x4, %rbp
 5f85bf8:      	addq	%r14, %rbp
 5f85bfb:      	movaps	%xmm0, 0x90(%rsp)
 5f85c03:      	movaps	%xmm0, 0x80(%rsp)
 5f85c0b:      	movaps	%xmm0, 0xf0(%rsp)
 5f85c13:      	movaps	%xmm0, 0xe0(%rsp)
 5f85c1b:      	xorl	%eax, %eax
 5f85c1d:      	xorps	%xmm0, %xmm0
 5f85c20:      	movaps	%xmm0, 0xb0(%rsp)
 5f85c28:      	movq	$0x0, 0xc0(%rsp)
 5f85c34:      	movq	%rax, 0xc8(%rsp)
 5f85c3c:      	movaps	%xmm0, 0x120(%rsp)
 5f85c44:      	movaps	%xmm0, 0x110(%rsp)
 5f85c4c:      	xorl	%eax, %eax
 5f85c4e:      	xorps	%xmm0, %xmm0
 5f85c51:      	movaps	%xmm0, 0x10(%rsp)
 5f85c56:      	movq	$0x0, 0x20(%rsp)
 5f85c5f:      	movq	%rax, 0x28(%rsp)
 5f85c64:      	movq	%rbp, %rax
 5f85c67:      	subq	%r14, %rax
 5f85c6a:      	movq	%rax, %r15
 5f85c6d:      	sarq	$0x6, %r15
 5f85c71:      	movq	%rax, %r13
 5f85c74:      	movq	%r14, %r12
 5f85c77:      	testq	%r15, %r15
 5f85c7a:      	movq	%rbp, 0x38(%rsp)
 5f85c7f:      	movq	%rax, 0x148(%rsp)
 5f85c87:      	jle	0x5f85d88 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x358>
 5f85c8d:      	incq	%r15
 5f85c90:      	leaq	0x20(%r14), %rbx
 5f85c94:      	leaq	0x10(%rsp), %r12
 5f85c99:      	leaq	0x50(%rsp), %rbp
 5f85c9e:      	movq	%rax, %r13
 5f85ca1:      	nopw	%cs:(%rax,%rax)
 5f85cab:      	nopl	(%rax,%rax)
 5f85cb0:      	movq	-0x20(%rbx), %rax
 5f85cb4:      	movl	-0x18(%rbx), %ecx
 5f85cb7:      	movq	%rax, 0x50(%rsp)
 5f85cbc:      	movl	%ecx, 0x58(%rsp)
 5f85cc0:      	cmpq	$0x0, 0x20(%rsp)
 5f85cc6:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85ccc:      	movq	%r12, %rdi
 5f85ccf:      	movq	%rbp, %rsi
 5f85cd2:      	callq	*0x28(%rsp)
 5f85cd6:      	testb	%al, %al
 5f85cd8:      	je	0x5f85e20 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3f0>
 5f85cde:      	movq	-0x10(%rbx), %rax
 5f85ce2:      	movl	-0x8(%rbx), %ecx
 5f85ce5:      	movq	%rax, 0x50(%rsp)
 5f85cea:      	movl	%ecx, 0x58(%rsp)
 5f85cee:      	cmpq	$0x0, 0x20(%rsp)
 5f85cf4:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85cfa:      	movq	%r12, %rdi
 5f85cfd:      	movq	%rbp, %rsi
 5f85d00:      	callq	*0x28(%rsp)
 5f85d04:      	testb	%al, %al
 5f85d06:      	je	0x5f85e26 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3f6>
 5f85d0c:      	movq	(%rbx), %rax
 5f85d0f:      	movl	0x8(%rbx), %ecx
 5f85d12:      	movq	%rax, 0x50(%rsp)
 5f85d17:      	movl	%ecx, 0x58(%rsp)
 5f85d1b:      	cmpq	$0x0, 0x20(%rsp)
 5f85d21:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85d27:      	movq	%r12, %rdi
 5f85d2a:      	movq	%rbp, %rsi
 5f85d2d:      	callq	*0x28(%rsp)
 5f85d31:      	testb	%al, %al
 5f85d33:      	je	0x5f85e6a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x43a>
 5f85d39:      	movq	0x10(%rbx), %rax
 5f85d3d:      	movl	0x18(%rbx), %ecx
 5f85d40:      	movq	%rax, 0x50(%rsp)
 5f85d45:      	movl	%ecx, 0x58(%rsp)
 5f85d49:      	cmpq	$0x0, 0x20(%rsp)
 5f85d4f:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85d55:      	movq	%r12, %rdi
 5f85d58:      	movq	%rbp, %rsi
 5f85d5b:      	callq	*0x28(%rsp)
 5f85d5f:      	testb	%al, %al
 5f85d61:      	je	0x5f85e66 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x436>
 5f85d67:      	decq	%r15
 5f85d6a:      	addq	$0x40, %rbx
 5f85d6e:      	addq	$-0x40, %r13
 5f85d72:      	cmpq	$0x1, %r15
 5f85d76:      	jg	0x5f85cb0 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x280>
 5f85d7c:      	addq	$-0x20, %rbx
 5f85d80:      	movq	%rbx, %r12
 5f85d83:      	movq	0x38(%rsp), %rbp
 5f85d88:      	sarq	$0x4, %r13
 5f85d8c:      	cmpq	$0x1, %r13
 5f85d90:      	je	0x5f85e2c <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3fc>
 5f85d96:      	cmpq	$0x2, %r13
 5f85d9a:      	movl	0xc(%rsp), %r15d
 5f85d9f:      	je	0x5f85de2 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3b2>
 5f85da1:      	movq	%rbp, %rbx
 5f85da4:      	cmpq	$0x3, %r13
 5f85da8:      	jne	0x5f85e74 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x444>
 5f85dae:      	movq	(%r12), %rax
 5f85db2:      	movl	0x8(%r12), %ecx
 5f85db7:      	movq	%rax, 0x50(%rsp)
 5f85dbc:      	movl	%ecx, 0x58(%rsp)
 5f85dc0:      	cmpq	$0x0, 0x20(%rsp)
 5f85dc6:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85dcc:      	leaq	0x10(%rsp), %rdi
 5f85dd1:      	leaq	0x50(%rsp), %rsi
 5f85dd6:      	callq	*0x28(%rsp)
 5f85dda:      	testb	%al, %al
 5f85ddc:      	je	0x5f85e1b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3eb>
 5f85dde:      	addq	$0x10, %r12
 5f85de2:      	movq	(%r12), %rax
 5f85de6:      	movl	0x8(%r12), %ecx
 5f85deb:      	movq	%rax, 0x50(%rsp)
 5f85df0:      	movl	%ecx, 0x58(%rsp)
 5f85df4:      	cmpq	$0x0, 0x20(%rsp)
 5f85dfa:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85e00:      	leaq	0x10(%rsp), %rdi
 5f85e05:      	leaq	0x50(%rsp), %rsi
 5f85e0a:      	callq	*0x28(%rsp)
 5f85e0e:      	testb	%al, %al
 5f85e10:      	je	0x5f85e1b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x3eb>
 5f85e12:      	addq	$0x10, %r12
 5f85e16:      	movq	%r12, %rbx
 5f85e19:      	jmp	0x5f85e34 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x404>
 5f85e1b:      	movq	%r12, %rbx
 5f85e1e:      	jmp	0x5f85e74 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x444>
 5f85e20:      	addq	$-0x20, %rbx
 5f85e24:      	jmp	0x5f85e6a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x43a>
 5f85e26:      	addq	$-0x10, %rbx
 5f85e2a:      	jmp	0x5f85e6a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x43a>
 5f85e2c:      	movq	%r12, %rbx
 5f85e2f:      	movl	0xc(%rsp), %r15d
 5f85e34:      	movq	(%rbx), %rax
 5f85e37:      	movl	0x8(%rbx), %ecx
 5f85e3a:      	movq	%rax, 0x50(%rsp)
 5f85e3f:      	movl	%ecx, 0x58(%rsp)
 5f85e43:      	cmpq	$0x0, 0x20(%rsp)
 5f85e49:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f85e4f:      	leaq	0x10(%rsp), %rdi
 5f85e54:      	leaq	0x50(%rsp), %rsi
 5f85e59:      	callq	*0x28(%rsp)
 5f85e5d:      	testb	%al, %al
 5f85e5f:      	je	0x5f85e74 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x444>
 5f85e61:      	movq	%rbp, %rbx
 5f85e64:      	jmp	0x5f85e74 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x444>
 5f85e66:      	addq	$0x10, %rbx
 5f85e6a:      	movl	0xc(%rsp), %r15d
 5f85e6f:      	movq	0x38(%rsp), %rbp
 5f85e74:      	movq	0x20(%rsp), %rax
 5f85e79:      	testq	%rax, %rax
 5f85e7c:      	je	0x5f85e8d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x45d>
 5f85e7e:      	leaq	0x10(%rsp), %rdi
 5f85e83:      	movq	%rdi, %rsi
 5f85e86:      	movl	$0x3, %edx
 5f85e8b:      	callq	*%rax
 5f85e8d:      	movq	0x120(%rsp), %rax
 5f85e95:      	testq	%rax, %rax
 5f85e98:      	movq	0x140(%rsp), %r12
 5f85ea0:      	je	0x5f85eb4 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x484>
 5f85ea2:      	leaq	0x110(%rsp), %rdi
 5f85eaa:      	movq	%rdi, %rsi
 5f85ead:      	movl	$0x3, %edx
 5f85eb2:      	callq	*%rax
 5f85eb4:      	movq	0xc0(%rsp), %rax
 5f85ebc:      	testq	%rax, %rax
 5f85ebf:      	je	0x5f85ed3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4a3>
 5f85ec1:      	leaq	0xb0(%rsp), %rdi
 5f85ec9:      	movq	%rdi, %rsi
 5f85ecc:      	movl	$0x3, %edx
 5f85ed1:      	callq	*%rax
 5f85ed3:      	movq	0xf0(%rsp), %rax
 5f85edb:      	testq	%rax, %rax
 5f85ede:      	je	0x5f85ef2 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4c2>
 5f85ee0:      	leaq	0xe0(%rsp), %rdi
 5f85ee8:      	movq	%rdi, %rsi
 5f85eeb:      	movl	$0x3, %edx
 5f85ef0:      	callq	*%rax
 5f85ef2:      	movq	0x90(%rsp), %rax
 5f85efa:      	testq	%rax, %rax
 5f85efd:      	je	0x5f85f11 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x4e1>
 5f85eff:      	leaq	0x80(%rsp), %rdi
 5f85f07:      	movq	%rdi, %rsi
 5f85f0a:      	movl	$0x3, %edx
 5f85f0f:      	callq	*%rax
 5f85f11:      	movq	0x1b0(%rsp), %rax
 5f85f19:      	testq	%rax, %rax
 5f85f1c:      	je	0x5f85f30 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x500>
 5f85f1e:      	leaq	0x1a0(%rsp), %rdi
 5f85f26:      	movq	%rdi, %rsi
 5f85f29:      	movl	$0x3, %edx
 5f85f2e:      	callq	*%rax
 5f85f30:      	cmpq	%rbp, %rbx
 5f85f33:      	je	0x5f86582 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb52>
 5f85f39:      	xorps	%xmm0, %xmm0
 5f85f3c:      	movaps	%xmm0, 0x160(%rsp)
 5f85f44:      	movaps	%xmm0, 0x150(%rsp)
 5f85f4c:      	movq	0x10(%r12), %rax
 5f85f51:      	testq	%rax, %rax
 5f85f54:      	je	0x5f8614a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x71a>
 5f85f5a:      	leaq	0x150(%rsp), %rdi
 5f85f62:      	movq	%r12, %rsi
 5f85f65:      	movl	$0x2, %edx
 5f85f6a:      	callq	*%rax
 5f85f6c:      	movups	0x10(%r12), %xmm0
 5f85f72:      	movq	0x10(%r12), %rax
 5f85f77:      	movaps	%xmm0, 0x160(%rsp)
 5f85f7f:      	movq	%rbx, 0x170(%rsp)
 5f85f87:      	xorps	%xmm0, %xmm0
 5f85f8a:      	movaps	%xmm0, 0x60(%rsp)
 5f85f8f:      	movaps	%xmm0, 0x50(%rsp)
 5f85f94:      	testq	%rax, %rax
 5f85f97:      	je	0x5f8615c <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x72c>
 5f85f9d:      	leaq	0x50(%rsp), %rdi
 5f85fa2:      	leaq	0x150(%rsp), %rsi
 5f85faa:      	movl	$0x2, %edx
 5f85faf:      	callq	*%rax
 5f85fb1:      	movaps	0x160(%rsp), %xmm0
 5f85fb9:      	movq	0x160(%rsp), %rcx
 5f85fc1:      	movq	0x170(%rsp), %rax
 5f85fc9:      	movaps	%xmm0, 0x60(%rsp)
 5f85fce:      	movq	%rax, 0x70(%rsp)
 5f85fd3:      	xorps	%xmm0, %xmm0
 5f85fd6:      	movaps	%xmm0, 0x90(%rsp)
 5f85fde:      	movaps	%xmm0, 0x80(%rsp)
 5f85fe6:      	testq	%rcx, %rcx
 5f85fe9:      	je	0x5f86174 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x744>
 5f85fef:      	leaq	0x80(%rsp), %rdi
 5f85ff7:      	leaq	0x50(%rsp), %rsi
 5f85ffc:      	movl	$0x2, %edx
 5f86001:      	callq	*%rcx
 5f86003:      	movaps	0x60(%rsp), %xmm0
 5f86008:      	movq	0x60(%rsp), %rcx
 5f8600d:      	movq	0x70(%rsp), %rax
 5f86012:      	movaps	%xmm0, 0x90(%rsp)
 5f8601a:      	movq	%rax, 0xa0(%rsp)
 5f86022:      	xorps	%xmm0, %xmm0
 5f86025:      	movaps	%xmm0, 0xf0(%rsp)
 5f8602d:      	movaps	%xmm0, 0xe0(%rsp)
 5f86035:      	testq	%rcx, %rcx
 5f86038:      	je	0x5f8618c <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x75c>
 5f8603e:      	leaq	0xe0(%rsp), %rdi
 5f86046:      	leaq	0x80(%rsp), %rsi
 5f8604e:      	movl	$0x2, %edx
 5f86053:      	callq	*%rcx
 5f86055:      	movq	0x90(%rsp), %r8
 5f8605d:      	movq	0x98(%rsp), %rcx
 5f86065:      	movq	%rcx, 0xf8(%rsp)
 5f8606d:      	movq	%r8, 0xf0(%rsp)
 5f86075:      	movq	0xa0(%rsp), %rax
 5f8607d:      	movq	%rax, 0x100(%rsp)
 5f86085:      	testq	%r8, %r8
 5f86088:      	je	0x5f86196 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x766>
 5f8608e:      	leaq	0xf0(%rsp), %rdx
 5f86096:      	xorps	%xmm1, %xmm1
 5f86099:      	movups	%xmm1, (%rdx)
 5f8609c:      	movaps	0xe0(%rsp), %xmm0
 5f860a4:      	movaps	%xmm0, 0xb0(%rsp)
 5f860ac:      	movq	%r8, 0xc0(%rsp)
 5f860b4:      	movq	%rcx, 0xc8(%rsp)
 5f860bc:      	movq	%rax, 0xd0(%rsp)
 5f860c4:      	movaps	%xmm1, 0x120(%rsp)
 5f860cc:      	movaps	%xmm1, 0x110(%rsp)
 5f860d4:      	leaq	0x110(%rsp), %rdi
 5f860dc:      	leaq	0xb0(%rsp), %rsi
 5f860e4:      	movl	$0x2, %edx
 5f860e9:      	callq	*%r8
 5f860ec:      	movq	0xc0(%rsp), %rdx
 5f860f4:      	movq	0xc8(%rsp), %rcx
 5f860fc:      	movq	%rcx, 0x128(%rsp)
 5f86104:      	movq	%rdx, 0x120(%rsp)
 5f8610c:      	movq	0xd0(%rsp), %rax
 5f86114:      	movq	%rax, 0x130(%rsp)
 5f8611c:      	testq	%rdx, %rdx
 5f8611f:      	je	0x5f861d7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7a7>
 5f86125:      	leaq	0x120(%rsp), %rsi
 5f8612d:      	xorps	%xmm0, %xmm0
 5f86130:      	movups	%xmm0, (%rsi)
 5f86133:      	movaps	0x110(%rsp), %xmm0
 5f8613b:      	movaps	%xmm0, 0x10(%rsp)
 5f86140:      	movq	%rdx, 0x20(%rsp)
 5f86145:      	jmp	0x5f861e8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7b8>
 5f8614a:      	movq	%rbx, 0x170(%rsp)
 5f86152:      	movaps	%xmm0, 0x60(%rsp)
 5f86157:      	movaps	%xmm0, 0x50(%rsp)
 5f8615c:      	movq	%rbx, 0x70(%rsp)
 5f86161:      	movaps	%xmm0, 0x90(%rsp)
 5f86169:      	movaps	%xmm0, 0x80(%rsp)
 5f86171:      	movq	%rbx, %rax
 5f86174:      	movq	%rax, 0xa0(%rsp)
 5f8617c:      	movaps	%xmm0, 0xf0(%rsp)
 5f86184:      	movaps	%xmm0, 0xe0(%rsp)
 5f8618c:      	movq	%rax, 0x100(%rsp)
 5f86194:      	xorl	%ecx, %ecx
 5f86196:      	xorps	%xmm0, %xmm0
 5f86199:      	movaps	%xmm0, 0xb0(%rsp)
 5f861a1:      	movq	$0x0, 0xc0(%rsp)
 5f861ad:      	movq	%rcx, 0xc8(%rsp)
 5f861b5:      	movq	%rax, 0xd0(%rsp)
 5f861bd:      	movaps	%xmm0, 0x120(%rsp)
 5f861c5:      	movaps	%xmm0, 0x110(%rsp)
 5f861cd:      	movq	%rax, 0x130(%rsp)
 5f861d5:      	xorl	%ecx, %ecx
 5f861d7:      	xorps	%xmm0, %xmm0
 5f861da:      	movaps	%xmm0, 0x10(%rsp)
 5f861df:      	movq	$0x0, 0x20(%rsp)
 5f861e8:      	movq	%rcx, 0x28(%rsp)
 5f861ed:      	movq	%rax, 0x30(%rsp)
 5f861f2:      	movq	0x138(%rsp), %rax
 5f861fa:      	movq	%rax, %rbp
 5f861fd:      	shrq	$0x2, %rbp
 5f86201:      	movq	%r14, %r12
 5f86204:      	je	0x5f8638e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x95e>
 5f8620a:      	incq	%rbp
 5f8620d:      	leaq	0x20(%r14), %r13
 5f86211:      	leaq	0x40(%rsp), %r12
 5f86216:      	jmp	0x5f8623a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x80a>
 5f86218:      	nopl	(%rax,%rax)
 5f86220:      	decq	%rbp
 5f86223:      	addq	$0x40, %r13
 5f86227:      	addq	$-0x40, 0x148(%rsp)
 5f86230:      	cmpq	$0x1, %rbp
 5f86234:      	jle	0x5f8637b <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x94b>
 5f8623a:      	movq	-0x20(%r13), %rcx
 5f8623e:      	movl	-0x18(%r13), %eax
 5f86242:      	movq	0x30(%rsp), %rdx
 5f86247:      	cmpq	(%rdx), %rcx
 5f8624a:      	jne	0x5f86251 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x821>
 5f8624c:      	cmpl	0x8(%rdx), %eax
 5f8624f:      	je	0x5f86285 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x855>
 5f86251:      	movq	%rcx, 0x40(%rsp)
 5f86256:      	movl	%eax, 0x48(%rsp)
 5f8625a:      	cmpq	$0x0, 0x20(%rsp)
 5f86260:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f86266:      	leaq	0x10(%rsp), %rdi
 5f8626b:      	movq	%r12, %rsi
 5f8626e:      	callq	*0x28(%rsp)
 5f86272:      	testb	%al, %al
 5f86274:      	je	0x5f86499 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa69>
 5f8627a:      	movq	0x30(%rsp), %rax
 5f8627f:      	movq	(%rax), %rcx
 5f86282:      	movl	0x8(%rax), %eax
 5f86285:      	movq	-0x10(%r13), %rdx
 5f86289:      	movl	-0x8(%r13), %esi
 5f8628d:      	cmpq	%rcx, %rdx
 5f86290:      	sete	%dil
 5f86294:      	cmpl	%eax, %esi
 5f86296:      	sete	%r8b
 5f8629a:      	testb	%r8b, %dil
 5f8629d:      	jne	0x5f862d3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8a3>
 5f8629f:      	movq	%rdx, 0x40(%rsp)
 5f862a4:      	movl	%esi, 0x48(%rsp)
 5f862a8:      	cmpq	$0x0, 0x20(%rsp)
 5f862ae:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f862b4:      	leaq	0x10(%rsp), %rdi
 5f862b9:      	movq	%r12, %rsi
 5f862bc:      	callq	*0x28(%rsp)
 5f862c0:      	testb	%al, %al
 5f862c2:      	je	0x5f8649f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa6f>
 5f862c8:      	movq	0x30(%rsp), %rax
 5f862cd:      	movq	(%rax), %rcx
 5f862d0:      	movl	0x8(%rax), %eax
 5f862d3:      	movq	(%r13), %rdx
 5f862d7:      	movl	0x8(%r13), %esi
 5f862db:      	cmpq	%rcx, %rdx
 5f862de:      	jne	0x5f86300 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8d0>
 5f862e0:      	cmpl	%eax, %esi
 5f862e2:      	jne	0x5f86300 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x8d0>
 5f862e4:      	movq	0x10(%r13), %rdx
 5f862e8:      	movl	0x18(%r13), %esi
 5f862ec:      	cmpq	%rcx, %rdx
 5f862ef:      	je	0x5f86341 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x911>
 5f862f1:      	jmp	0x5f86349 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x919>
 5f862f3:      	nopw	%cs:(%rax,%rax)
 5f862fd:      	nopl	(%rax)
 5f86300:      	movq	%rdx, 0x40(%rsp)
 5f86305:      	movl	%esi, 0x48(%rsp)
 5f86309:      	cmpq	$0x0, 0x20(%rsp)
 5f8630f:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f86315:      	leaq	0x10(%rsp), %rdi
 5f8631a:      	movq	%r12, %rsi
 5f8631d:      	callq	*0x28(%rsp)
 5f86321:      	testb	%al, %al
 5f86323:      	je	0x5f864a3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa73>
 5f86329:      	movq	0x30(%rsp), %rax
 5f8632e:      	movq	(%rax), %rcx
 5f86331:      	movl	0x8(%rax), %eax
 5f86334:      	movq	0x10(%r13), %rdx
 5f86338:      	movl	0x18(%r13), %esi
 5f8633c:      	cmpq	%rcx, %rdx
 5f8633f:      	jne	0x5f86349 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x919>
 5f86341:      	cmpl	%eax, %esi
 5f86343:      	je	0x5f86220 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7f0>
 5f86349:      	movq	%rdx, 0x40(%rsp)
 5f8634e:      	movl	%esi, 0x48(%rsp)
 5f86352:      	cmpq	$0x0, 0x20(%rsp)
 5f86358:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f8635e:      	leaq	0x10(%rsp), %rdi
 5f86363:      	movq	%r12, %rsi
 5f86366:      	callq	*0x28(%rsp)
 5f8636a:      	testb	%al, %al
 5f8636c:      	jne	0x5f86220 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x7f0>
 5f86372:      	addq	$0x10, %r13
 5f86376:      	jmp	0x5f864a3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa73>
 5f8637b:      	movq	0x148(%rsp), %rax
 5f86383:      	sarq	$0x4, %rax
 5f86387:      	addq	$-0x20, %r13
 5f8638b:      	movq	%r13, %r12
 5f8638e:      	cmpq	$0x1, %rax
 5f86392:      	je	0x5f86440 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa10>
 5f86398:      	cmpq	$0x2, %rax
 5f8639c:      	movq	0x38(%rsp), %rbp
 5f863a1:      	je	0x5f863f7 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9c7>
 5f863a3:      	movq	%rbp, %r13
 5f863a6:      	cmpq	$0x3, %rax
 5f863aa:      	jne	0x5f864a8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa78>
 5f863b0:      	movq	(%r12), %rax
 5f863b4:      	movl	0x8(%r12), %ecx
 5f863b9:      	movq	0x30(%rsp), %rdx
 5f863be:      	cmpq	(%rdx), %rax
 5f863c1:      	jne	0x5f863c8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x998>
 5f863c3:      	cmpl	0x8(%rdx), %ecx
 5f863c6:      	je	0x5f863f3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9c3>
 5f863c8:      	movq	%rax, 0x40(%rsp)
 5f863cd:      	movl	%ecx, 0x48(%rsp)
 5f863d1:      	cmpq	$0x0, 0x20(%rsp)
 5f863d7:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f863dd:      	leaq	0x10(%rsp), %rdi
 5f863e2:      	leaq	0x40(%rsp), %rsi
 5f863e7:      	callq	*0x28(%rsp)
 5f863eb:      	testb	%al, %al
 5f863ed:      	je	0x5f8667f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc4f>
 5f863f3:      	addq	$0x10, %r12
 5f863f7:      	movq	(%r12), %rax
 5f863fb:      	movl	0x8(%r12), %ecx
 5f86400:      	movq	0x30(%rsp), %rdx
 5f86405:      	cmpq	(%rdx), %rax
 5f86408:      	jne	0x5f8640f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0x9df>
 5f8640a:      	cmpl	0x8(%rdx), %ecx
 5f8640d:      	je	0x5f8643a <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa0a>
 5f8640f:      	movq	%rax, 0x40(%rsp)
 5f86414:      	movl	%ecx, 0x48(%rsp)
 5f86418:      	cmpq	$0x0, 0x20(%rsp)
 5f8641e:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f86424:      	leaq	0x10(%rsp), %rdi
 5f86429:      	leaq	0x40(%rsp), %rsi
 5f8642e:      	callq	*0x28(%rsp)
 5f86432:      	testb	%al, %al
 5f86434:      	je	0x5f8667f <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc4f>
 5f8643a:      	addq	$0x10, %r12
 5f8643e:      	jmp	0x5f86445 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa15>
 5f86440:      	movq	0x38(%rsp), %rbp
 5f86445:      	movq	(%r12), %rax
 5f86449:      	movl	0x8(%r12), %ecx
 5f8644e:      	movq	0x30(%rsp), %rdx
 5f86453:      	cmpq	(%rdx), %rax
 5f86456:      	jne	0x5f86460 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa30>
 5f86458:      	movq	%rbp, %r13
 5f8645b:      	cmpl	0x8(%rdx), %ecx
 5f8645e:      	je	0x5f864a8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa78>
 5f86460:      	movq	%rax, 0x40(%rsp)
 5f86465:      	movl	%ecx, 0x48(%rsp)
 5f86469:      	cmpq	$0x0, 0x20(%rsp)
 5f8646f:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f86475:      	leaq	0x10(%rsp), %rdi
 5f8647a:      	leaq	0x40(%rsp), %rsi
 5f8647f:      	callq	*0x28(%rsp)
 5f86483:      	movq	%r12, %r13
 5f86486:      	testb	%al, %al
 5f86488:      	je	0x5f864a8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa78>
 5f8648a:      	movq	%rbp, %r13
 5f8648d:      	movq	0x20(%rsp), %rax
 5f86492:      	testq	%rax, %rax
 5f86495:      	jne	0x5f864b2 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa82>
 5f86497:      	jmp	0x5f864c1 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa91>
 5f86499:      	addq	$-0x20, %r13
 5f8649d:      	jmp	0x5f864a3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa73>
 5f8649f:      	addq	$-0x10, %r13
 5f864a3:      	movq	0x38(%rsp), %rbp
 5f864a8:      	movq	0x20(%rsp), %rax
 5f864ad:      	testq	%rax, %rax
 5f864b0:      	je	0x5f864c1 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa91>
 5f864b2:      	leaq	0x10(%rsp), %rdi
 5f864b7:      	movq	%rdi, %rsi
 5f864ba:      	movl	$0x3, %edx
 5f864bf:      	callq	*%rax
 5f864c1:      	movq	0x120(%rsp), %rax
 5f864c9:      	testq	%rax, %rax
 5f864cc:      	movq	0x140(%rsp), %r12
 5f864d4:      	je	0x5f864e8 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xab8>
 5f864d6:      	leaq	0x110(%rsp), %rdi
 5f864de:      	movq	%rdi, %rsi
 5f864e1:      	movl	$0x3, %edx
 5f864e6:      	callq	*%rax
 5f864e8:      	movq	0xc0(%rsp), %rax
 5f864f0:      	testq	%rax, %rax
 5f864f3:      	je	0x5f86507 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xad7>
 5f864f5:      	leaq	0xb0(%rsp), %rdi
 5f864fd:      	movq	%rdi, %rsi
 5f86500:      	movl	$0x3, %edx
 5f86505:      	callq	*%rax
 5f86507:      	movq	0xf0(%rsp), %rax
 5f8650f:      	testq	%rax, %rax
 5f86512:      	je	0x5f86526 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xaf6>
 5f86514:      	leaq	0xe0(%rsp), %rdi
 5f8651c:      	movq	%rdi, %rsi
 5f8651f:      	movl	$0x3, %edx
 5f86524:      	callq	*%rax
 5f86526:      	movq	0x90(%rsp), %rax
 5f8652e:      	testq	%rax, %rax
 5f86531:      	je	0x5f86545 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb15>
 5f86533:      	leaq	0x80(%rsp), %rdi
 5f8653b:      	movq	%rdi, %rsi
 5f8653e:      	movl	$0x3, %edx
 5f86543:      	callq	*%rax
 5f86545:      	movq	0x60(%rsp), %rax
 5f8654a:      	testq	%rax, %rax
 5f8654d:      	je	0x5f8655e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb2e>
 5f8654f:      	leaq	0x50(%rsp), %rdi
 5f86554:      	movq	%rdi, %rsi
 5f86557:      	movl	$0x3, %edx
 5f8655c:      	callq	*%rax
 5f8655e:      	movq	0x160(%rsp), %rax
 5f86566:      	testq	%rax, %rax
 5f86569:      	je	0x5f8657d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb4d>
 5f8656b:      	leaq	0x150(%rsp), %rdi
 5f86573:      	movq	%rdi, %rsi
 5f86576:      	movl	$0x3, %edx
 5f8657b:      	callq	*%rax
 5f8657d:      	cmpq	%r13, %rbp
 5f86580:      	je	0x5f86594 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb64>
 5f86582:      	movq	0x1c0(%rsp), %rbx
 5f8658a:      	testq	%rbx, %rbx
 5f8658d:      	jne	0x5f865a3 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb73>
 5f8658f:      	jmp	0x5f8666d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc3d>
 5f86594:      	movq	(%rbx), %rax
 5f86597:      	testq	%rax, %rax
 5f8659a:      	je	0x5f86582 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xb52>
 5f8659c:      	movl	0x8(%rbx), %r15d
 5f865a0:      	movq	%rax, %rbx
 5f865a3:      	xorps	%xmm0, %xmm0
 5f865a6:      	movaps	%xmm0, 0x190(%rsp)
 5f865ae:      	movaps	%xmm0, 0x180(%rsp)
 5f865b6:      	movq	0x10(%r12), %rax
 5f865bb:      	testq	%rax, %rax
 5f865be:      	je	0x5f865f2 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbc2>
 5f865c0:      	leaq	0x180(%rsp), %rdi
 5f865c8:      	movq	%r12, %rsi
 5f865cb:      	movl	$0x2, %edx
 5f865d0:      	callq	*%rax
 5f865d2:      	movups	0x10(%r12), %xmm0
 5f865d8:      	movq	0x10(%r12), %rax
 5f865dd:      	movaps	%xmm0, 0x190(%rsp)
 5f865e5:      	cmpq	$0x0, 0x138(%rsp)
 5f865ee:      	jne	0x5f865ff <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbcf>
 5f865f0:      	jmp	0x5f86656 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc26>
 5f865f2:      	xorl	%eax, %eax
 5f865f4:      	cmpq	$0x0, 0x138(%rsp)
 5f865fd:      	je	0x5f86656 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc26>
 5f865ff:      	leaq	0x180(%rsp), %r12
 5f86607:      	leaq	0x10(%rsp), %r13
 5f8660c:      	jmp	0x5f86619 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbe9>
 5f8660e:      	nop
 5f86610:      	addq	$0x10, %r14
 5f86614:      	cmpq	%rbp, %r14
 5f86617:      	je	0x5f8664e <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc1e>
 5f86619:      	movq	(%r14), %rax
 5f8661c:      	movl	0x8(%r14), %ecx
 5f86620:      	movq	%rax, 0x10(%rsp)
 5f86625:      	movl	%ecx, 0x18(%rsp)
 5f86629:      	cmpq	$0x0, 0x190(%rsp)
 5f86632:      	je	0x5f86695 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc65>
 5f86634:      	movq	%r12, %rdi
 5f86637:      	movq	%r13, %rsi
 5f8663a:      	callq	*0x198(%rsp)
 5f86641:      	testb	%al, %al
 5f86643:      	je	0x5f86610 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbe0>
 5f86645:      	movq	%rbx, (%r14)
 5f86648:      	movl	%r15d, 0x8(%r14)
 5f8664c:      	jmp	0x5f86610 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xbe0>
 5f8664e:      	movq	0x190(%rsp), %rax
 5f86656:      	testq	%rax, %rax
 5f86659:      	je	0x5f8666d <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xc3d>
 5f8665b:      	leaq	0x180(%rsp), %rdi
 5f86663:      	movq	%rdi, %rsi
 5f86666:      	movl	$0x3, %edx
 5f8666b:      	callq	*%rax
 5f8666d:      	addq	$0x1c8, %rsp            # imm = 0x1C8
 5f86674:      	popq	%rbx
 5f86675:      	popq	%r12
 5f86677:      	popq	%r13
 5f86679:      	popq	%r14
 5f8667b:      	popq	%r15
 5f8667d:      	popq	%rbp
 5f8667e:      	retq
 5f8667f:      	movq	%r12, %r13
 5f86682:      	movq	0x20(%rsp), %rax
 5f86687:      	testq	%rax, %rax
 5f8668a:      	jne	0x5f864b2 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa82>
 5f86690:      	jmp	0x5f864c1 <_ZL25turnVectorIntoSplatVectorN4llvm15MutableArrayRefINS_7SDValueEEESt8functionIFbS1_EES1_+0xa91>
 5f86695:      	callq	0x828a940 <_ZSt25__throw_bad_function_callv@plt>
