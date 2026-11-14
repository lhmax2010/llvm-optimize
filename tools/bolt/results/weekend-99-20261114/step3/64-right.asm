
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003e709e0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE>:
 3e709e0:      	pushq	%rbp
 3e709e1:      	pushq	%r15
 3e709e3:      	pushq	%r14
 3e709e5:      	pushq	%r13
 3e709e7:      	pushq	%r12
 3e709e9:      	pushq	%rbx
 3e709ea:      	subq	$0x38, %rsp
 3e709ee:      	movl	%esi, %ecx
 3e709f0:      	movq	0xd0(%rdi), %rax
 3e709f7:      	leaq	(%rcx,%rcx,2), %rdx
 3e709fb:      	movq	(%rax,%rdx,8), %r15
 3e709ff:      	movq	0x8(%rax,%rdx,8), %r9
 3e70a04:      	cmpq	%r9, %r15
 3e70a07:      	jne	0x3e70ecf <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4ef>
 3e70a0d:      	movl	%esi, %r8d
 3e70a10:      	leaq	(%rax,%rdx,8), %rax
 3e70a14:      	movq	%rax, 0x10(%rsp)
 3e70a19:      	movq	0x8(%rdi), %rax
 3e70a1d:      	movq	0x38(%rdi), %rcx
 3e70a21:      	movl	0x10(%rax,%rdx,8), %edx
 3e70a25:      	movl	%edx, %r11d
 3e70a28:      	andl	$0xfff, %r11d           # imm = 0xFFF
 3e70a2f:      	shrl	$0xc, %edx
 3e70a32:      	leaq	(%rcx,%rdx,2), %r10
 3e70a36:      	testq	%rcx, %rcx
 3e70a39:      	movl	%esi, 0xc(%rsp)
 3e70a3d:      	je	0x3e70ada <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xfa>
 3e70a43:      	movq	0x30(%rdi), %rbx
 3e70a47:      	movq	%r10, %rdx
 3e70a4a:      	movl	%r11d, %esi
 3e70a4d:      	movl	(%rbx,%rsi,4), %r13d
 3e70a51:      	testw	%r13w, %r13w
 3e70a55:      	je	0x3e70ab0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xd0>
 3e70a57:      	movl	%r13d, %esi
 3e70a5a:      	shrl	$0x10, %esi
 3e70a5d:      	movl	%r13d, %r12d
 3e70a60:      	movzwl	%r12w, %r14d
 3e70a64:      	leaq	(%r14,%r14,2), %r10
 3e70a68:      	movl	0x8(%rax,%r10,8), %r10d
 3e70a6d:      	leaq	(%rcx,%r10,2), %rbp
 3e70a71:      	cmpl	%r14d, %r8d
 3e70a74:      	jne	0x3e70acd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xed>
 3e70a76:      	movl	%r8d, %r14d
 3e70a79:      	nopl	(%rax)
 3e70a80:      	movzwl	(%rbp), %r10d
 3e70a85:      	testl	%r10d, %r10d
 3e70a88:      	je	0x3e70aa0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xc0>
 3e70a8a:      	addl	%r10d, %r14d
 3e70a8d:      	addq	$0x2, %rbp
 3e70a91:      	movzwl	%r14w, %r10d
 3e70a95:      	cmpl	%r10d, %r8d
 3e70a98:      	je	0x3e70a80 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xa0>
 3e70a9a:      	jmp	0x3e70aca <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xea>
 3e70a9c:      	nopl	(%rax)
 3e70aa0:      	xorl	%r13d, %r13d
 3e70aa3:      	testw	%si, %si
 3e70aa6:      	movl	%esi, %r12d
 3e70aa9:      	movl	$0x0, %esi
 3e70aae:      	jne	0x3e70a60 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x80>
 3e70ab0:      	movq	%rdx, %r10
 3e70ab3:      	movswl	(%rdx), %esi
 3e70ab6:      	addq	$0x2, %r10
 3e70aba:      	addl	%esi, %r11d
 3e70abd:      	testl	%esi, %esi
 3e70abf:      	jne	0x3e70a47 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x67>
 3e70ac5:      	jmp	0x3e70c7d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70aca:      	movl	%r14d, %r12d
 3e70acd:      	movq	%rdx, %r10
 3e70ad0:      	testq	%r10, %r10
 3e70ad3:      	jne	0x3e70aeb <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x10b>
 3e70ad5:      	jmp	0x3e70c7d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70ada:      	xorl	%r13d, %r13d
 3e70add:      	xorl	%r14d, %r14d
 3e70ae0:      	xorl	%ebp, %ebp
 3e70ae2:      	testq	%r10, %r10
 3e70ae5:      	je	0x3e70c7d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70aeb:      	movq	0x10(%rsp), %rax
 3e70af0:      	movq	0x10(%rax), %rdx
 3e70af4:      	movq	%rdi, 0x20(%rsp)
 3e70af9:      	jmp	0x3e70b03 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x123>
 3e70afb:      	nopl	(%rax,%rax)
 3e70b00:      	movq	%rbx, %rdx
 3e70b03:      	cmpq	%rdx, %r9
 3e70b06:      	je	0x3e70b30 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x150>
 3e70b08:      	movq	%rdx, %rbx
 3e70b0b:      	movw	%r12w, (%r9)
 3e70b0f:      	addq	$0x2, %r9
 3e70b13:      	movq	0x10(%rsp), %rax
 3e70b18:      	movq	%r9, 0x8(%rax)
 3e70b1c:      	jmp	0x3e70bfc <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x21c>
 3e70b21:      	nopw	%cs:(%rax,%rax)
 3e70b2b:      	nopl	(%rax,%rax)
 3e70b30:      	movq	%r10, 0x28(%rsp)
 3e70b35:      	movq	%r11, 0x30(%rsp)
 3e70b3a:      	subq	%r15, %rdx
 3e70b3d:      	movabsq	$0x7ffffffffffffffe, %rax # imm = 0x7FFFFFFFFFFFFFFE
 3e70b47:      	cmpq	%rax, %rdx
 3e70b4a:      	je	0x3e70f98 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x5b8>
 3e70b50:      	movq	%rdx, %rax
 3e70b53:      	sarq	%rax
 3e70b56:      	cmpq	$0x1, %rax
 3e70b5a:      	movq	%rax, %rcx
 3e70b5d:      	adcq	$0x0, %rcx
 3e70b61:      	leaq	(%rcx,%rax), %rbx
 3e70b65:      	movq	%rdx, 0x18(%rsp)
 3e70b6a:      	movabsq	$0x3fffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFFF
 3e70b74:      	cmpq	%rdx, %rbx
 3e70b77:      	cmovaeq	%rdx, %rbx
 3e70b7b:      	addq	%rax, %rcx
 3e70b7e:      	cmovbq	%rdx, %rbx
 3e70b82:      	leaq	(%rbx,%rbx), %rdi
 3e70b86:      	callq	0x828a620 <_Znwm@plt>
 3e70b8b:      	movq	0x18(%rsp), %r9
 3e70b90:      	movw	%r12w, (%rax,%r9)
 3e70b95:      	movq	%rax, %r12
 3e70b98:      	testq	%r9, %r9
 3e70b9b:      	jle	0x3e70bb2 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x1d2>
 3e70b9d:      	movq	%r12, %rdi
 3e70ba0:      	movq	%r15, %rsi
 3e70ba3:      	movq	0x18(%rsp), %rdx
 3e70ba8:      	callq	0x828ac50 <memcpy@plt>
 3e70bad:      	movq	0x18(%rsp), %r9
 3e70bb2:      	testq	%r15, %r15
 3e70bb5:      	je	0x3e70bc7 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x1e7>
 3e70bb7:      	movq	%r15, %rdi
 3e70bba:      	movq	%r9, %rsi
 3e70bbd:      	callq	0x828a660 <_ZdlPvm@plt>
 3e70bc2:      	movq	0x18(%rsp), %r9
 3e70bc7:      	movq	%r12, %r15
 3e70bca:      	addq	%r12, %r9
 3e70bcd:      	addq	$0x2, %r9
 3e70bd1:      	movq	0x10(%rsp), %rax
 3e70bd6:      	movq	%r12, (%rax)
 3e70bd9:      	movq	%r9, 0x8(%rax)
 3e70bdd:      	leaq	(%r12,%rbx,2), %rcx
 3e70be1:      	movq	%rcx, %rbx
 3e70be4:      	movq	%rcx, 0x10(%rax)
 3e70be8:      	movl	0xc(%rsp), %r8d
 3e70bed:      	movq	0x20(%rsp), %rdi
 3e70bf2:      	movq	0x30(%rsp), %r11
 3e70bf7:      	movq	0x28(%rsp), %r10
 3e70bfc:      	movq	0x38(%rdi), %rax
 3e70c00:      	movq	0x8(%rdi), %rcx
 3e70c04:      	movq	0x30(%rdi), %rdx
 3e70c08:      	jmp	0x3e70c27 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x247>
 3e70c0a:      	nopw	(%rax,%rax)
 3e70c10:      	addl	%esi, %r14d
 3e70c13:      	addq	$0x2, %rbp
 3e70c17:      	movl	%r14d, %r12d
 3e70c1a:      	movzwl	%r12w, %esi
 3e70c1e:      	cmpl	%esi, %r8d
 3e70c21:      	jne	0x3e70b00 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x120>
 3e70c27:      	movzwl	(%rbp), %esi
 3e70c2b:      	testl	%esi, %esi
 3e70c2d:      	jne	0x3e70c10 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x230>
 3e70c2f:      	shrl	$0x10, %r13d
 3e70c33:      	je	0x3e70c49 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x269>
 3e70c35:      	movl	%r13d, %esi
 3e70c38:      	leaq	(%rsi,%rsi,2), %rsi
 3e70c3c:      	movl	0x8(%rcx,%rsi,8), %esi
 3e70c40:      	leaq	(%rax,%rsi,2), %rbp
 3e70c44:      	movl	%r13d, %r14d
 3e70c47:      	jmp	0x3e70c6c <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x28c>
 3e70c49:      	movswl	(%r10), %esi
 3e70c4d:      	testl	%esi, %esi
 3e70c4f:      	je	0x3e70c7d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70c51:      	addl	%esi, %r11d
 3e70c54:      	addq	$0x2, %r10
 3e70c58:      	movl	(%rdx,%r11,4), %r13d
 3e70c5c:      	movzwl	%r13w, %r14d
 3e70c60:      	leaq	(%r14,%r14,2), %rsi
 3e70c64:      	movl	0x8(%rcx,%rsi,8), %esi
 3e70c68:      	leaq	(%rax,%rsi,2), %rbp
 3e70c6c:      	movl	%r13d, %r12d
 3e70c6f:      	movzwl	%r12w, %esi
 3e70c73:      	cmpl	%esi, %r8d
 3e70c76:      	je	0x3e70c27 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x247>
 3e70c78:      	jmp	0x3e70b00 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x120>
 3e70c7d:      	cmpq	%r9, %r15
 3e70c80:      	movq	0x10(%rsp), %rbx
 3e70c85:      	je	0x3e70e16 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x436>
 3e70c8b:      	movq	%r9, %rbx
 3e70c8e:      	subq	%r15, %rbx
 3e70c91:      	movq	%rbx, %rax
 3e70c94:      	sarq	%rax
 3e70c97:      	bsrq	%rax, %rdx
 3e70c9b:      	xorl	$0x3f, %edx
 3e70c9e:      	addl	%edx, %edx
 3e70ca0:      	xorq	$0x7e, %rdx
 3e70ca4:      	movq	%r15, %rdi
 3e70ca7:      	movq	%r9, %rsi
 3e70caa:      	movq	%r9, %r14
 3e70cad:      	callq	0x3e71500 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPtSt6vectorItSaItEEEElNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_>
 3e70cb2:      	leaq	0x2(%r15), %r12
 3e70cb6:      	cmpq	$0x21, %rbx
 3e70cba:      	movq	%r14, 0x18(%rsp)
 3e70cbf:      	jl	0x3e70d58 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x378>
 3e70cc5:      	movq	%r14, %rsi
 3e70cc8:      	leaq	0x2(%r15), %r14
 3e70ccc:      	movl	$0x2, %r13d
 3e70cd2:      	movq	%r15, %rbp
 3e70cd5:      	movl	0xc(%rsp), %r8d
 3e70cda:      	jmp	0x3e70d16 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x336>
 3e70cdc:      	nopl	(%rax)
 3e70ce0:      	cmpq	$0x3, %r13
 3e70ce4:      	jb	0x3e70d52 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x372>
 3e70ce6:      	movq	%r12, %rdi
 3e70ce9:      	movq	%r15, %rsi
 3e70cec:      	movq	%r13, %rdx
 3e70cef:      	callq	0x828abc0 <memmove@plt>
 3e70cf4:      	movq	0x18(%rsp), %rsi
 3e70cf9:      	movl	0xc(%rsp), %r8d
 3e70cfe:      	movq	%r15, %rax
 3e70d01:      	movw	%bx, (%rax)
 3e70d04:      	addq	$0x2, %r13
 3e70d08:      	addq	$0x2, %r14
 3e70d0c:      	cmpq	$0x20, %r13
 3e70d10:      	je	0x3e70e01 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x421>
 3e70d16:      	movq	%rbp, %rax
 3e70d19:      	leaq	(%r15,%r13), %rbp
 3e70d1d:      	movzwl	(%r15,%r13), %ebx
 3e70d22:      	movzwl	(%r15), %ecx
 3e70d26:      	cmpw	%cx, %bx
 3e70d29:      	jb	0x3e70ce0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x300>
 3e70d2b:      	movzwl	(%rax), %ecx
 3e70d2e:      	movq	%rbp, %rax
 3e70d31:      	cmpw	%cx, %bx
 3e70d34:      	jae	0x3e70d01 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x321>
 3e70d36:      	movq	%r14, %rax
 3e70d39:      	nopl	(%rax)
 3e70d40:      	movw	%cx, (%rax)
 3e70d43:      	movzwl	-0x4(%rax), %ecx
 3e70d47:      	addq	$-0x2, %rax
 3e70d4b:      	cmpw	%cx, %bx
 3e70d4e:      	jb	0x3e70d40 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x360>
 3e70d50:      	jmp	0x3e70d01 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x321>
 3e70d52:      	movw	%cx, 0x2(%rax)
 3e70d56:      	jmp	0x3e70cfe <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x31e>
 3e70d58:      	cmpq	%r14, %r12
 3e70d5b:      	movq	0x10(%rsp), %rbx
 3e70d60:      	movl	0xc(%rsp), %r8d
 3e70d65:      	je	0x3e70e0f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70d6b:      	movq	%r14, %rsi
 3e70d6e:      	movq	%r15, %r14
 3e70d71:      	jmp	0x3e70dbd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3dd>
 3e70d73:      	nopw	%cs:(%rax,%rax)
 3e70d7d:      	nopl	(%rax)
 3e70d80:      	movq	%r14, %rdx
 3e70d83:      	subq	%r15, %rdx
 3e70d86:      	movq	%rdx, %rax
 3e70d89:      	sarq	%rax
 3e70d8c:      	cmpq	$0x2, %rax
 3e70d90:      	jl	0x3e70df2 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x412>
 3e70d92:      	addq	%rax, %rax
 3e70d95:      	subq	%rax, %rdi
 3e70d98:      	addq	$0x4, %rdi
 3e70d9c:      	movq	%r15, %rsi
 3e70d9f:      	callq	0x828abc0 <memmove@plt>
 3e70da4:      	movq	0x18(%rsp), %rsi
 3e70da9:      	movl	0xc(%rsp), %r8d
 3e70dae:      	movq	%r15, %rax
 3e70db1:      	movw	%bp, (%rax)
 3e70db4:      	leaq	0x2(%r14), %r12
 3e70db8:      	cmpq	%rsi, %r12
 3e70dbb:      	je	0x3e70e0f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70dbd:      	movq	%r14, %rdi
 3e70dc0:      	movq	%r12, %r14
 3e70dc3:      	movzwl	(%r12), %ebp
 3e70dc8:      	movzwl	(%r15), %ecx
 3e70dcc:      	cmpw	%cx, %bp
 3e70dcf:      	jb	0x3e70d80 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3a0>
 3e70dd1:      	movzwl	(%rdi), %ecx
 3e70dd4:      	movq	%r14, %rax
 3e70dd7:      	cmpw	%cx, %bp
 3e70dda:      	jae	0x3e70db1 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70ddc:      	movq	%r14, %rax
 3e70ddf:      	nop
 3e70de0:      	movw	%cx, (%rax)
 3e70de3:      	movzwl	-0x4(%rax), %ecx
 3e70de7:      	addq	$-0x2, %rax
 3e70deb:      	cmpw	%cx, %bp
 3e70dee:      	jb	0x3e70de0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x400>
 3e70df0:      	jmp	0x3e70db1 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70df2:      	movq	%r15, %rax
 3e70df5:      	cmpq	$0x2, %rdx
 3e70df9:      	jne	0x3e70db1 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70dfb:      	movw	%cx, 0x2(%rdi)
 3e70dff:      	jmp	0x3e70dae <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3ce>
 3e70e01:      	addq	$0x20, %r15
 3e70e05:      	cmpq	%rsi, %r15
 3e70e08:      	movq	0x10(%rsp), %rbx
 3e70e0d:      	jne	0x3e70e5c <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x47c>
 3e70e0f:      	movq	(%rbx), %r15
 3e70e12:      	movq	0x8(%rbx), %r9
 3e70e16:      	cmpq	%r9, %r15
 3e70e19:      	je	0x3e70ebd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70e1f:      	leaq	0x2(%r15), %rax
 3e70e23:      	nopw	%cs:(%rax,%rax)
 3e70e2d:      	nopl	(%rax)
 3e70e30:      	cmpq	%r9, %rax
 3e70e33:      	je	0x3e70ebd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70e39:      	movzwl	-0x2(%rax), %ecx
 3e70e3d:      	leaq	0x2(%rax), %rdx
 3e70e41:      	cmpw	(%rax), %cx
 3e70e44:      	movq	%rdx, %rax
 3e70e47:      	jne	0x3e70e30 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x450>
 3e70e49:      	leaq	-0x4(%rdx), %rax
 3e70e4d:      	jmp	0x3e70e94 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b4>
 3e70e4f:      	nop
 3e70e50:      	movw	%ax, (%rdx)
 3e70e53:      	addq	$0x2, %r15
 3e70e57:      	cmpq	%rsi, %r15
 3e70e5a:      	je	0x3e70e0f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70e5c:      	movzwl	-0x2(%r15), %ecx
 3e70e61:      	movzwl	(%r15), %eax
 3e70e65:      	movq	%r15, %rdx
 3e70e68:      	cmpw	%cx, %ax
 3e70e6b:      	jae	0x3e70e50 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x470>
 3e70e6d:      	movq	%r15, %rdx
 3e70e70:      	movw	%cx, (%rdx)
 3e70e73:      	movzwl	-0x4(%rdx), %ecx
 3e70e77:      	addq	$-0x2, %rdx
 3e70e7b:      	cmpw	%cx, %ax
 3e70e7e:      	jb	0x3e70e70 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x490>
 3e70e80:      	jmp	0x3e70e50 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x470>
 3e70e82:      	nopw	%cs:(%rax,%rax)
 3e70e8c:      	nopl	(%rax)
 3e70e90:      	addq	$0x2, %rdx
 3e70e94:      	cmpq	%r9, %rdx
 3e70e97:      	je	0x3e70ead <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4cd>
 3e70e99:      	movl	%ecx, %esi
 3e70e9b:      	movzwl	(%rdx), %ecx
 3e70e9e:      	cmpw	%cx, %si
 3e70ea1:      	je	0x3e70e90 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b0>
 3e70ea3:      	movw	%cx, 0x2(%rax)
 3e70ea7:      	addq	$0x2, %rax
 3e70eab:      	jmp	0x3e70e90 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b0>
 3e70ead:      	addq	$0x2, %rax
 3e70eb1:      	cmpq	%r9, %rax
 3e70eb4:      	je	0x3e70ebd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70eb6:      	movq	%rax, 0x8(%rbx)
 3e70eba:      	movq	%rax, %r9
 3e70ebd:      	cmpq	0x10(%rbx), %r9
 3e70ec1:      	je	0x3e70eea <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x50a>
 3e70ec3:      	movw	%r8w, (%r9)
 3e70ec7:      	addq	$0x2, %r9
 3e70ecb:      	movq	%r9, 0x8(%rbx)
 3e70ecf:      	movq	%r15, %rax
 3e70ed2:      	subq	%rax, %r9
 3e70ed5:      	sarq	%r9
 3e70ed8:      	movq	%r9, %rdx
 3e70edb:      	addq	$0x38, %rsp
 3e70edf:      	popq	%rbx
 3e70ee0:      	popq	%r12
 3e70ee2:      	popq	%r13
 3e70ee4:      	popq	%r14
 3e70ee6:      	popq	%r15
 3e70ee8:      	popq	%rbp
 3e70ee9:      	retq
 3e70eea:      	subq	%r15, %r9
 3e70eed:      	movabsq	$0x7ffffffffffffffe, %rax # imm = 0x7FFFFFFFFFFFFFFE
 3e70ef7:      	cmpq	%rax, %r9
 3e70efa:      	je	0x3e70f98 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x5b8>
 3e70f00:      	movq	%r9, %rax
 3e70f03:      	sarq	%rax
 3e70f06:      	cmpq	$0x1, %rax
 3e70f0a:      	movq	%rax, %rcx
 3e70f0d:      	adcq	$0x0, %rcx
 3e70f11:      	leaq	(%rcx,%rax), %rbx
 3e70f15:      	movabsq	$0x3fffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFFF
 3e70f1f:      	cmpq	%rdx, %rbx
 3e70f22:      	cmovaeq	%rdx, %rbx
 3e70f26:      	addq	%rax, %rcx
 3e70f29:      	cmovbq	%rdx, %rbx
 3e70f2d:      	leaq	(%rbx,%rbx), %rdi
 3e70f31:      	movq	%r9, %r12
 3e70f34:      	callq	0x828a620 <_Znwm@plt>
 3e70f39:      	movq	%r12, %rdx
 3e70f3c:      	movl	0xc(%rsp), %ecx
 3e70f40:      	movw	%cx, (%rax,%r12)
 3e70f45:      	testq	%r12, %r12
 3e70f48:      	jle	0x3e70f5e <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x57e>
 3e70f4a:      	movq	%rax, %rdi
 3e70f4d:      	movq	%r15, %rsi
 3e70f50:      	movq	%rax, %r14
 3e70f53:      	callq	0x828ac50 <memcpy@plt>
 3e70f58:      	movq	%r12, %rdx
 3e70f5b:      	movq	%r14, %rax
 3e70f5e:      	leaq	(%rax,%rdx), %r14
 3e70f62:      	testq	%r15, %r15
 3e70f65:      	je	0x3e70f78 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x598>
 3e70f67:      	movq	%r15, %rdi
 3e70f6a:      	movq	%rdx, %rsi
 3e70f6d:      	movq	%rax, %r15
 3e70f70:      	callq	0x828a660 <_ZdlPvm@plt>
 3e70f75:      	movq	%r15, %rax
 3e70f78:      	addq	$0x2, %r14
 3e70f7c:      	movq	0x10(%rsp), %rdx
 3e70f81:      	movq	%rax, (%rdx)
 3e70f84:      	movq	%r14, 0x8(%rdx)
 3e70f88:      	leaq	(%rax,%rbx,2), %rcx
 3e70f8c:      	movq	%rcx, 0x10(%rdx)
 3e70f90:      	movq	%r14, %r9
 3e70f93:      	jmp	0x3e70ed2 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4f2>
 3e70f98:      	leaq	-0x31d65b5(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 3e70f9f:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
