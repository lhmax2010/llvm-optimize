
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003e70a60 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE>:
 3e70a60:      	pushq	%rbp
 3e70a61:      	pushq	%r15
 3e70a63:      	pushq	%r14
 3e70a65:      	pushq	%r13
 3e70a67:      	pushq	%r12
 3e70a69:      	pushq	%rbx
 3e70a6a:      	subq	$0x38, %rsp
 3e70a6e:      	movl	%esi, %ecx
 3e70a70:      	movq	0xd0(%rdi), %rax
 3e70a77:      	leaq	(%rcx,%rcx,2), %rdx
 3e70a7b:      	movq	(%rax,%rdx,8), %r15
 3e70a7f:      	movq	0x8(%rax,%rdx,8), %r9
 3e70a84:      	cmpq	%r9, %r15
 3e70a87:      	jne	0x3e70f4f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4ef>
 3e70a8d:      	movl	%esi, %r8d
 3e70a90:      	leaq	(%rax,%rdx,8), %rax
 3e70a94:      	movq	%rax, 0x10(%rsp)
 3e70a99:      	movq	0x8(%rdi), %rax
 3e70a9d:      	movq	0x38(%rdi), %rcx
 3e70aa1:      	movl	0x10(%rax,%rdx,8), %edx
 3e70aa5:      	movl	%edx, %r11d
 3e70aa8:      	andl	$0xfff, %r11d           # imm = 0xFFF
 3e70aaf:      	shrl	$0xc, %edx
 3e70ab2:      	leaq	(%rcx,%rdx,2), %r10
 3e70ab6:      	testq	%rcx, %rcx
 3e70ab9:      	movl	%esi, 0xc(%rsp)
 3e70abd:      	je	0x3e70b5a <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xfa>
 3e70ac3:      	movq	0x30(%rdi), %rbx
 3e70ac7:      	movq	%r10, %rdx
 3e70aca:      	movl	%r11d, %esi
 3e70acd:      	movl	(%rbx,%rsi,4), %r13d
 3e70ad1:      	testw	%r13w, %r13w
 3e70ad5:      	je	0x3e70b30 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xd0>
 3e70ad7:      	movl	%r13d, %esi
 3e70ada:      	shrl	$0x10, %esi
 3e70add:      	movl	%r13d, %r12d
 3e70ae0:      	movzwl	%r12w, %r14d
 3e70ae4:      	leaq	(%r14,%r14,2), %r10
 3e70ae8:      	movl	0x8(%rax,%r10,8), %r10d
 3e70aed:      	leaq	(%rcx,%r10,2), %rbp
 3e70af1:      	cmpl	%r14d, %r8d
 3e70af4:      	jne	0x3e70b4d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xed>
 3e70af6:      	movl	%r8d, %r14d
 3e70af9:      	nopl	(%rax)
 3e70b00:      	movzwl	(%rbp), %r10d
 3e70b05:      	testl	%r10d, %r10d
 3e70b08:      	je	0x3e70b20 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xc0>
 3e70b0a:      	addl	%r10d, %r14d
 3e70b0d:      	addq	$0x2, %rbp
 3e70b11:      	movzwl	%r14w, %r10d
 3e70b15:      	cmpl	%r10d, %r8d
 3e70b18:      	je	0x3e70b00 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xa0>
 3e70b1a:      	jmp	0x3e70b4a <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0xea>
 3e70b1c:      	nopl	(%rax)
 3e70b20:      	xorl	%r13d, %r13d
 3e70b23:      	testw	%si, %si
 3e70b26:      	movl	%esi, %r12d
 3e70b29:      	movl	$0x0, %esi
 3e70b2e:      	jne	0x3e70ae0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x80>
 3e70b30:      	movq	%rdx, %r10
 3e70b33:      	movswl	(%rdx), %esi
 3e70b36:      	addq	$0x2, %r10
 3e70b3a:      	addl	%esi, %r11d
 3e70b3d:      	testl	%esi, %esi
 3e70b3f:      	jne	0x3e70ac7 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x67>
 3e70b45:      	jmp	0x3e70cfd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70b4a:      	movl	%r14d, %r12d
 3e70b4d:      	movq	%rdx, %r10
 3e70b50:      	testq	%r10, %r10
 3e70b53:      	jne	0x3e70b6b <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x10b>
 3e70b55:      	jmp	0x3e70cfd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70b5a:      	xorl	%r13d, %r13d
 3e70b5d:      	xorl	%r14d, %r14d
 3e70b60:      	xorl	%ebp, %ebp
 3e70b62:      	testq	%r10, %r10
 3e70b65:      	je	0x3e70cfd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70b6b:      	movq	0x10(%rsp), %rax
 3e70b70:      	movq	0x10(%rax), %rdx
 3e70b74:      	movq	%rdi, 0x20(%rsp)
 3e70b79:      	jmp	0x3e70b83 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x123>
 3e70b7b:      	nopl	(%rax,%rax)
 3e70b80:      	movq	%rbx, %rdx
 3e70b83:      	cmpq	%rdx, %r9
 3e70b86:      	je	0x3e70bb0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x150>
 3e70b88:      	movq	%rdx, %rbx
 3e70b8b:      	movw	%r12w, (%r9)
 3e70b8f:      	addq	$0x2, %r9
 3e70b93:      	movq	0x10(%rsp), %rax
 3e70b98:      	movq	%r9, 0x8(%rax)
 3e70b9c:      	jmp	0x3e70c7c <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x21c>
 3e70ba1:      	nopw	%cs:(%rax,%rax)
 3e70bab:      	nopl	(%rax,%rax)
 3e70bb0:      	movq	%r10, 0x28(%rsp)
 3e70bb5:      	movq	%r11, 0x30(%rsp)
 3e70bba:      	subq	%r15, %rdx
 3e70bbd:      	movabsq	$0x7ffffffffffffffe, %rax # imm = 0x7FFFFFFFFFFFFFFE
 3e70bc7:      	cmpq	%rax, %rdx
 3e70bca:      	je	0x3e71018 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x5b8>
 3e70bd0:      	movq	%rdx, %rax
 3e70bd3:      	sarq	%rax
 3e70bd6:      	cmpq	$0x1, %rax
 3e70bda:      	movq	%rax, %rcx
 3e70bdd:      	adcq	$0x0, %rcx
 3e70be1:      	leaq	(%rcx,%rax), %rbx
 3e70be5:      	movq	%rdx, 0x18(%rsp)
 3e70bea:      	movabsq	$0x3fffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFFF
 3e70bf4:      	cmpq	%rdx, %rbx
 3e70bf7:      	cmovaeq	%rdx, %rbx
 3e70bfb:      	addq	%rax, %rcx
 3e70bfe:      	cmovbq	%rdx, %rbx
 3e70c02:      	leaq	(%rbx,%rbx), %rdi
 3e70c06:      	callq	0x828a6b0 <_Znwm@plt>
 3e70c0b:      	movq	0x18(%rsp), %r9
 3e70c10:      	movw	%r12w, (%rax,%r9)
 3e70c15:      	movq	%rax, %r12
 3e70c18:      	testq	%r9, %r9
 3e70c1b:      	jle	0x3e70c32 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x1d2>
 3e70c1d:      	movq	%r12, %rdi
 3e70c20:      	movq	%r15, %rsi
 3e70c23:      	movq	0x18(%rsp), %rdx
 3e70c28:      	callq	0x828ace0 <memcpy@plt>
 3e70c2d:      	movq	0x18(%rsp), %r9
 3e70c32:      	testq	%r15, %r15
 3e70c35:      	je	0x3e70c47 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x1e7>
 3e70c37:      	movq	%r15, %rdi
 3e70c3a:      	movq	%r9, %rsi
 3e70c3d:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3e70c42:      	movq	0x18(%rsp), %r9
 3e70c47:      	movq	%r12, %r15
 3e70c4a:      	addq	%r12, %r9
 3e70c4d:      	addq	$0x2, %r9
 3e70c51:      	movq	0x10(%rsp), %rax
 3e70c56:      	movq	%r12, (%rax)
 3e70c59:      	movq	%r9, 0x8(%rax)
 3e70c5d:      	leaq	(%r12,%rbx,2), %rcx
 3e70c61:      	movq	%rcx, %rbx
 3e70c64:      	movq	%rcx, 0x10(%rax)
 3e70c68:      	movl	0xc(%rsp), %r8d
 3e70c6d:      	movq	0x20(%rsp), %rdi
 3e70c72:      	movq	0x30(%rsp), %r11
 3e70c77:      	movq	0x28(%rsp), %r10
 3e70c7c:      	movq	0x38(%rdi), %rax
 3e70c80:      	movq	0x8(%rdi), %rcx
 3e70c84:      	movq	0x30(%rdi), %rdx
 3e70c88:      	jmp	0x3e70ca7 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x247>
 3e70c8a:      	nopw	(%rax,%rax)
 3e70c90:      	addl	%esi, %r14d
 3e70c93:      	addq	$0x2, %rbp
 3e70c97:      	movl	%r14d, %r12d
 3e70c9a:      	movzwl	%r12w, %esi
 3e70c9e:      	cmpl	%esi, %r8d
 3e70ca1:      	jne	0x3e70b80 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x120>
 3e70ca7:      	movzwl	(%rbp), %esi
 3e70cab:      	testl	%esi, %esi
 3e70cad:      	jne	0x3e70c90 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x230>
 3e70caf:      	shrl	$0x10, %r13d
 3e70cb3:      	je	0x3e70cc9 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x269>
 3e70cb5:      	movl	%r13d, %esi
 3e70cb8:      	leaq	(%rsi,%rsi,2), %rsi
 3e70cbc:      	movl	0x8(%rcx,%rsi,8), %esi
 3e70cc0:      	leaq	(%rax,%rsi,2), %rbp
 3e70cc4:      	movl	%r13d, %r14d
 3e70cc7:      	jmp	0x3e70cec <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x28c>
 3e70cc9:      	movswl	(%r10), %esi
 3e70ccd:      	testl	%esi, %esi
 3e70ccf:      	je	0x3e70cfd <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x29d>
 3e70cd1:      	addl	%esi, %r11d
 3e70cd4:      	addq	$0x2, %r10
 3e70cd8:      	movl	(%rdx,%r11,4), %r13d
 3e70cdc:      	movzwl	%r13w, %r14d
 3e70ce0:      	leaq	(%r14,%r14,2), %rsi
 3e70ce4:      	movl	0x8(%rcx,%rsi,8), %esi
 3e70ce8:      	leaq	(%rax,%rsi,2), %rbp
 3e70cec:      	movl	%r13d, %r12d
 3e70cef:      	movzwl	%r12w, %esi
 3e70cf3:      	cmpl	%esi, %r8d
 3e70cf6:      	je	0x3e70ca7 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x247>
 3e70cf8:      	jmp	0x3e70b80 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x120>
 3e70cfd:      	cmpq	%r9, %r15
 3e70d00:      	movq	0x10(%rsp), %rbx
 3e70d05:      	je	0x3e70e96 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x436>
 3e70d0b:      	movq	%r9, %rbx
 3e70d0e:      	subq	%r15, %rbx
 3e70d11:      	movq	%rbx, %rax
 3e70d14:      	sarq	%rax
 3e70d17:      	bsrq	%rax, %rdx
 3e70d1b:      	xorl	$0x3f, %edx
 3e70d1e:      	addl	%edx, %edx
 3e70d20:      	xorq	$0x7e, %rdx
 3e70d24:      	movq	%r15, %rdi
 3e70d27:      	movq	%r9, %rsi
 3e70d2a:      	movq	%r9, %r14
 3e70d2d:      	callq	0x3e71580 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPtSt6vectorItSaItEEEElNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_>
 3e70d32:      	leaq	0x2(%r15), %r12
 3e70d36:      	cmpq	$0x21, %rbx
 3e70d3a:      	movq	%r14, 0x18(%rsp)
 3e70d3f:      	jl	0x3e70dd8 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x378>
 3e70d45:      	movl	$0x2, %r13d
 3e70d4b:      	movq	%r14, %rsi
 3e70d4e:      	movq	%r12, %r14
 3e70d51:      	movq	%r15, %rbp
 3e70d54:      	movl	0xc(%rsp), %r8d
 3e70d59:      	jmp	0x3e70d96 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x336>
 3e70d5b:      	nopl	(%rax,%rax)
 3e70d60:      	cmpq	$0x3, %r13
 3e70d64:      	jb	0x3e70dd2 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x372>
 3e70d66:      	movq	%r12, %rdi
 3e70d69:      	movq	%r15, %rsi
 3e70d6c:      	movq	%r13, %rdx
 3e70d6f:      	callq	0x828ac50 <memmove@plt>
 3e70d74:      	movq	0x18(%rsp), %rsi
 3e70d79:      	movl	0xc(%rsp), %r8d
 3e70d7e:      	movq	%r15, %rax
 3e70d81:      	movw	%bx, (%rax)
 3e70d84:      	addq	$0x2, %r13
 3e70d88:      	addq	$0x2, %r14
 3e70d8c:      	cmpq	$0x20, %r13
 3e70d90:      	je	0x3e70e81 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x421>
 3e70d96:      	movq	%rbp, %rax
 3e70d99:      	leaq	(%r15,%r13), %rbp
 3e70d9d:      	movzwl	(%r15,%r13), %ebx
 3e70da2:      	movzwl	(%r15), %ecx
 3e70da6:      	cmpw	%cx, %bx
 3e70da9:      	jb	0x3e70d60 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x300>
 3e70dab:      	movzwl	(%rax), %ecx
 3e70dae:      	movq	%rbp, %rax
 3e70db1:      	cmpw	%cx, %bx
 3e70db4:      	jae	0x3e70d81 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x321>
 3e70db6:      	movq	%r14, %rax
 3e70db9:      	nopl	(%rax)
 3e70dc0:      	movw	%cx, (%rax)
 3e70dc3:      	movzwl	-0x4(%rax), %ecx
 3e70dc7:      	addq	$-0x2, %rax
 3e70dcb:      	cmpw	%cx, %bx
 3e70dce:      	jb	0x3e70dc0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x360>
 3e70dd0:      	jmp	0x3e70d81 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x321>
 3e70dd2:      	movw	%cx, 0x2(%rax)
 3e70dd6:      	jmp	0x3e70d7e <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x31e>
 3e70dd8:      	cmpq	%r14, %r12
 3e70ddb:      	movq	0x10(%rsp), %rbx
 3e70de0:      	movl	0xc(%rsp), %r8d
 3e70de5:      	je	0x3e70e8f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70deb:      	movq	%r14, %rsi
 3e70dee:      	movq	%r15, %r14
 3e70df1:      	jmp	0x3e70e3d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3dd>
 3e70df3:      	nopw	%cs:(%rax,%rax)
 3e70dfd:      	nopl	(%rax)
 3e70e00:      	movq	%r14, %rdx
 3e70e03:      	subq	%r15, %rdx
 3e70e06:      	movq	%rdx, %rax
 3e70e09:      	sarq	%rax
 3e70e0c:      	cmpq	$0x2, %rax
 3e70e10:      	jl	0x3e70e72 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x412>
 3e70e12:      	addq	%rax, %rax
 3e70e15:      	subq	%rax, %rdi
 3e70e18:      	addq	$0x4, %rdi
 3e70e1c:      	movq	%r15, %rsi
 3e70e1f:      	callq	0x828ac50 <memmove@plt>
 3e70e24:      	movq	0x18(%rsp), %rsi
 3e70e29:      	movl	0xc(%rsp), %r8d
 3e70e2e:      	movq	%r15, %rax
 3e70e31:      	movw	%bp, (%rax)
 3e70e34:      	leaq	0x2(%r14), %r12
 3e70e38:      	cmpq	%rsi, %r12
 3e70e3b:      	je	0x3e70e8f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70e3d:      	movq	%r14, %rdi
 3e70e40:      	movq	%r12, %r14
 3e70e43:      	movzwl	(%r12), %ebp
 3e70e48:      	movzwl	(%r15), %ecx
 3e70e4c:      	cmpw	%cx, %bp
 3e70e4f:      	jb	0x3e70e00 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3a0>
 3e70e51:      	movzwl	(%rdi), %ecx
 3e70e54:      	movq	%r14, %rax
 3e70e57:      	cmpw	%cx, %bp
 3e70e5a:      	jae	0x3e70e31 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70e5c:      	movq	%r14, %rax
 3e70e5f:      	nop
 3e70e60:      	movw	%cx, (%rax)
 3e70e63:      	movzwl	-0x4(%rax), %ecx
 3e70e67:      	addq	$-0x2, %rax
 3e70e6b:      	cmpw	%cx, %bp
 3e70e6e:      	jb	0x3e70e60 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x400>
 3e70e70:      	jmp	0x3e70e31 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70e72:      	movq	%r15, %rax
 3e70e75:      	cmpq	$0x2, %rdx
 3e70e79:      	jne	0x3e70e31 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3d1>
 3e70e7b:      	movw	%cx, 0x2(%rdi)
 3e70e7f:      	jmp	0x3e70e2e <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x3ce>
 3e70e81:      	addq	$0x20, %r15
 3e70e85:      	cmpq	%rsi, %r15
 3e70e88:      	movq	0x10(%rsp), %rbx
 3e70e8d:      	jne	0x3e70edc <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x47c>
 3e70e8f:      	movq	(%rbx), %r15
 3e70e92:      	movq	0x8(%rbx), %r9
 3e70e96:      	cmpq	%r9, %r15
 3e70e99:      	je	0x3e70f3d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70e9f:      	leaq	0x2(%r15), %rax
 3e70ea3:      	nopw	%cs:(%rax,%rax)
 3e70ead:      	nopl	(%rax)
 3e70eb0:      	cmpq	%r9, %rax
 3e70eb3:      	je	0x3e70f3d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70eb9:      	movzwl	-0x2(%rax), %ecx
 3e70ebd:      	leaq	0x2(%rax), %rdx
 3e70ec1:      	cmpw	(%rax), %cx
 3e70ec4:      	movq	%rdx, %rax
 3e70ec7:      	jne	0x3e70eb0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x450>
 3e70ec9:      	leaq	-0x4(%rdx), %rax
 3e70ecd:      	jmp	0x3e70f14 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b4>
 3e70ecf:      	nop
 3e70ed0:      	movw	%ax, (%rdx)
 3e70ed3:      	addq	$0x2, %r15
 3e70ed7:      	cmpq	%rsi, %r15
 3e70eda:      	je	0x3e70e8f <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x42f>
 3e70edc:      	movzwl	-0x2(%r15), %ecx
 3e70ee1:      	movzwl	(%r15), %eax
 3e70ee5:      	movq	%r15, %rdx
 3e70ee8:      	cmpw	%cx, %ax
 3e70eeb:      	jae	0x3e70ed0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x470>
 3e70eed:      	movq	%r15, %rdx
 3e70ef0:      	movw	%cx, (%rdx)
 3e70ef3:      	movzwl	-0x4(%rdx), %ecx
 3e70ef7:      	addq	$-0x2, %rdx
 3e70efb:      	cmpw	%cx, %ax
 3e70efe:      	jb	0x3e70ef0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x490>
 3e70f00:      	jmp	0x3e70ed0 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x470>
 3e70f02:      	nopw	%cs:(%rax,%rax)
 3e70f0c:      	nopl	(%rax)
 3e70f10:      	addq	$0x2, %rdx
 3e70f14:      	cmpq	%r9, %rdx
 3e70f17:      	je	0x3e70f2d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4cd>
 3e70f19:      	movl	%ecx, %esi
 3e70f1b:      	movzwl	(%rdx), %ecx
 3e70f1e:      	cmpw	%cx, %si
 3e70f21:      	je	0x3e70f10 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b0>
 3e70f23:      	movw	%cx, 0x2(%rax)
 3e70f27:      	addq	$0x2, %rax
 3e70f2b:      	jmp	0x3e70f10 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4b0>
 3e70f2d:      	addq	$0x2, %rax
 3e70f31:      	cmpq	%r9, %rax
 3e70f34:      	je	0x3e70f3d <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4dd>
 3e70f36:      	movq	%rax, 0x8(%rbx)
 3e70f3a:      	movq	%rax, %r9
 3e70f3d:      	cmpq	0x10(%rbx), %r9
 3e70f41:      	je	0x3e70f6a <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x50a>
 3e70f43:      	movw	%r8w, (%r9)
 3e70f47:      	addq	$0x2, %r9
 3e70f4b:      	movq	%r9, 0x8(%rbx)
 3e70f4f:      	movq	%r15, %rax
 3e70f52:      	subq	%rax, %r9
 3e70f55:      	sarq	%r9
 3e70f58:      	movq	%r9, %rdx
 3e70f5b:      	addq	$0x38, %rsp
 3e70f5f:      	popq	%rbx
 3e70f60:      	popq	%r12
 3e70f62:      	popq	%r13
 3e70f64:      	popq	%r14
 3e70f66:      	popq	%r15
 3e70f68:      	popq	%rbp
 3e70f69:      	retq
 3e70f6a:      	subq	%r15, %r9
 3e70f6d:      	movabsq	$0x7ffffffffffffffe, %rax # imm = 0x7FFFFFFFFFFFFFFE
 3e70f77:      	cmpq	%rax, %r9
 3e70f7a:      	je	0x3e71018 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x5b8>
 3e70f80:      	movq	%r9, %rax
 3e70f83:      	sarq	%rax
 3e70f86:      	cmpq	$0x1, %rax
 3e70f8a:      	movq	%rax, %rcx
 3e70f8d:      	adcq	$0x0, %rcx
 3e70f91:      	leaq	(%rcx,%rax), %rbx
 3e70f95:      	movabsq	$0x3fffffffffffffff, %rdx # imm = 0x3FFFFFFFFFFFFFFF
 3e70f9f:      	cmpq	%rdx, %rbx
 3e70fa2:      	cmovaeq	%rdx, %rbx
 3e70fa6:      	addq	%rax, %rcx
 3e70fa9:      	cmovbq	%rdx, %rbx
 3e70fad:      	leaq	(%rbx,%rbx), %rdi
 3e70fb1:      	movq	%r9, %r12
 3e70fb4:      	callq	0x828a6b0 <_Znwm@plt>
 3e70fb9:      	movq	%r12, %rdx
 3e70fbc:      	movl	0xc(%rsp), %ecx
 3e70fc0:      	movw	%cx, (%rax,%r12)
 3e70fc5:      	testq	%r12, %r12
 3e70fc8:      	jle	0x3e70fde <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x57e>
 3e70fca:      	movq	%rax, %rdi
 3e70fcd:      	movq	%r15, %rsi
 3e70fd0:      	movq	%rax, %r14
 3e70fd3:      	callq	0x828ace0 <memcpy@plt>
 3e70fd8:      	movq	%r12, %rdx
 3e70fdb:      	movq	%r14, %rax
 3e70fde:      	leaq	(%rax,%rdx), %r14
 3e70fe2:      	testq	%r15, %r15
 3e70fe5:      	je	0x3e70ff8 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x598>
 3e70fe7:      	movq	%r15, %rdi
 3e70fea:      	movq	%rdx, %rsi
 3e70fed:      	movq	%rax, %r15
 3e70ff0:      	callq	0x828a6f0 <_ZdlPvm@plt>
 3e70ff5:      	movq	%r15, %rax
 3e70ff8:      	addq	$0x2, %r14
 3e70ffc:      	movq	0x10(%rsp), %rdx
 3e71001:      	movq	%rax, (%rdx)
 3e71004:      	movq	%r14, 0x8(%rdx)
 3e71008:      	leaq	(%rax,%rbx,2), %rcx
 3e7100c:      	movq	%rcx, 0x10(%rdx)
 3e71010:      	movq	%r14, %r9
 3e71013:      	jmp	0x3e70f52 <_ZNK4llvm14MCRegisterInfo18getCachedAliasesOfENS_10MCRegisterE+0x4f2>
 3e71018:      	leaq	-0x31d6635(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 3e7101f:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
