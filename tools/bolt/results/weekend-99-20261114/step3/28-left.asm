
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000035d2820 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv>:
 35d2820:      	pushq	%rbp
 35d2821:      	pushq	%r15
 35d2823:      	pushq	%r14
 35d2825:      	pushq	%r13
 35d2827:      	pushq	%r12
 35d2829:      	pushq	%rbx
 35d282a:      	subq	$0x18, %rsp
 35d282e:      	movq	%rdi, %rbp
 35d2831:      	movq	0xb8(%rdi), %r14
 35d2838:      	movq	0xc0(%rdi), %r15
 35d283f:      	cmpq	%r15, %r14
 35d2842:      	je	0x35d2a2a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2848:      	movq	%r15, %rbx
 35d284b:      	subq	%r14, %rbx
 35d284e:      	movq	%rbx, %rax
 35d2851:      	sarq	$0x4, %rax
 35d2855:      	bsrq	%rax, %rdx
 35d2859:      	xorl	$0x3f, %edx
 35d285c:      	addl	%edx, %edx
 35d285e:      	xorq	$0x7e, %rdx
 35d2862:      	movq	%r14, %rdi
 35d2865:      	movq	%r15, %rsi
 35d2868:      	callq	0x35db750 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm17MachineBasicBlock16RegisterMaskPairESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZNS3_17sortUniqueLiveInsEvE3$_0EEEvT_SE_T0_T1_>
 35d286d:      	leaq	0x10(%r14), %r12
 35d2871:      	cmpq	$0x101, %rbx            # imm = 0x101
 35d2878:      	jl	0x35d293f <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x11f>
 35d287e:      	movq	%rbp, 0x10(%rsp)
 35d2883:      	movl	$0x10, %r13d
 35d2889:      	movq	%r12, %rbp
 35d288c:      	movq	%r14, %rax
 35d288f:      	jmp	0x35d28c9 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xa9>
 35d2891:      	nopw	%cs:(%rax,%rax)
 35d289b:      	nopl	(%rax,%rax)
 35d28a0:      	movl	%ecx, (%rdx)
 35d28a2:      	movq	(%rsp), %rax
 35d28a6:      	movq	%rax, 0x4(%rdx)
 35d28aa:      	movl	0x8(%rsp), %eax
 35d28ae:      	movl	%eax, 0xc(%rdx)
 35d28b1:      	addq	$0x10, %r13
 35d28b5:      	addq	$0x10, %rbp
 35d28b9:      	movq	%rbx, %rax
 35d28bc:      	cmpq	$0x100, %r13            # imm = 0x100
 35d28c3:      	je	0x35d2a15 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1f5>
 35d28c9:      	leaq	(%r14,%r13), %rbx
 35d28cd:      	movl	(%r14,%r13), %ecx
 35d28d1:      	cmpl	(%r14), %ecx
 35d28d4:      	jae	0x35d2900 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xe0>
 35d28d6:      	movups	(%rbx), %xmm0
 35d28d9:      	movaps	%xmm0, (%rsp)
 35d28dd:      	cmpq	$0x11, %r13
 35d28e1:      	jb	0x35d2935 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x115>
 35d28e3:      	movq	%r12, %rdi
 35d28e6:      	movq	%r14, %rsi
 35d28e9:      	movq	%r13, %rdx
 35d28ec:      	callq	0x828ac50 <memmove@plt>
 35d28f1:      	movaps	(%rsp), %xmm0
 35d28f5:      	movups	%xmm0, (%r14)
 35d28f9:      	jmp	0x35d28b1 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x91>
 35d28fb:      	nopl	(%rax,%rax)
 35d2900:      	movl	0x1c(%rax), %edx
 35d2903:      	movl	%edx, 0x8(%rsp)
 35d2907:      	movq	0x14(%rax), %rdx
 35d290b:      	movq	%rdx, (%rsp)
 35d290f:      	movq	%rbx, %rdx
 35d2912:      	cmpl	(%rax), %ecx
 35d2914:      	jae	0x35d28a0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x80>
 35d2916:      	movq	%rbp, %rdx
 35d2919:      	nopl	(%rax)
 35d2920:      	movups	-0x10(%rdx), %xmm0
 35d2924:      	movups	%xmm0, (%rdx)
 35d2927:      	cmpl	-0x20(%rdx), %ecx
 35d292a:      	leaq	-0x10(%rdx), %rdx
 35d292e:      	jb	0x35d2920 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x100>
 35d2930:      	jmp	0x35d28a0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x80>
 35d2935:      	movups	(%r14), %xmm0
 35d2939:      	movups	%xmm0, 0x10(%rax)
 35d293d:      	jmp	0x35d28f1 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xd1>
 35d293f:      	cmpq	%r15, %r12
 35d2942:      	je	0x35d2a2a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2948:      	movq	%r14, %rdi
 35d294b:      	jmp	0x35d2971 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x151>
 35d294d:      	nopl	(%rax)
 35d2950:      	movl	%eax, (%rcx)
 35d2952:      	movq	(%rsp), %rax
 35d2956:      	movq	%rax, 0x4(%rcx)
 35d295a:      	movl	0x8(%rsp), %eax
 35d295e:      	movl	%eax, 0xc(%rcx)
 35d2961:      	leaq	0x10(%r13), %r12
 35d2965:      	movq	%r13, %rdi
 35d2968:      	cmpq	%r15, %r12
 35d296b:      	je	0x35d2a2a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2971:      	movq	%r12, %r13
 35d2974:      	movl	(%r12), %eax
 35d2978:      	cmpl	(%r14), %eax
 35d297b:      	jae	0x35d29d0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1b0>
 35d297d:      	movups	(%r13), %xmm0
 35d2982:      	movaps	%xmm0, (%rsp)
 35d2986:      	movq	%r13, %rdx
 35d2989:      	subq	%r14, %rdx
 35d298c:      	movq	%rdx, %rax
 35d298f:      	sarq	$0x4, %rax
 35d2993:      	cmpq	$0x2, %rax
 35d2997:      	jl	0x35d2a05 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1e5>
 35d2999:      	shlq	$0x4, %rax
 35d299d:      	subq	%rax, %rdi
 35d29a0:      	addq	$0x20, %rdi
 35d29a4:      	movq	%r14, %rsi
 35d29a7:      	callq	0x828ac50 <memmove@plt>
 35d29ac:      	movaps	(%rsp), %xmm0
 35d29b0:      	movups	%xmm0, (%r14)
 35d29b4:      	leaq	0x10(%r13), %r12
 35d29b8:      	movq	%r13, %rdi
 35d29bb:      	cmpq	%r15, %r12
 35d29be:      	jne	0x35d2971 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x151>
 35d29c0:      	jmp	0x35d2a2a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d29c2:      	nopw	%cs:(%rax,%rax)
 35d29cc:      	nopl	(%rax)
 35d29d0:      	movl	0x1c(%rdi), %ecx
 35d29d3:      	movl	%ecx, 0x8(%rsp)
 35d29d7:      	movq	0x14(%rdi), %rcx
 35d29db:      	movq	%rcx, (%rsp)
 35d29df:      	movq	%r13, %rcx
 35d29e2:      	cmpl	(%rdi), %eax
 35d29e4:      	jae	0x35d2950 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x130>
 35d29ea:      	movq	%r13, %rcx
 35d29ed:      	nopl	(%rax)
 35d29f0:      	movups	-0x10(%rcx), %xmm0
 35d29f4:      	movups	%xmm0, (%rcx)
 35d29f7:      	cmpl	-0x20(%rcx), %eax
 35d29fa:      	leaq	-0x10(%rcx), %rcx
 35d29fe:      	jb	0x35d29f0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1d0>
 35d2a00:      	jmp	0x35d2950 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x130>
 35d2a05:      	cmpq	$0x10, %rdx
 35d2a09:      	jne	0x35d29ac <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x18c>
 35d2a0b:      	movups	(%r14), %xmm0
 35d2a0f:      	movups	%xmm0, 0x10(%rdi)
 35d2a13:      	jmp	0x35d29ac <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x18c>
 35d2a15:      	addq	$0x100, %r14            # imm = 0x100
 35d2a1c:      	cmpq	%r15, %r14
 35d2a1f:      	movq	0x10(%rsp), %rbp
 35d2a24:      	jne	0x35d2abe <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x29e>
 35d2a2a:      	movq	0xb8(%rbp), %rax
 35d2a31:      	movq	0xc0(%rbp), %rcx
 35d2a38:      	cmpq	%rcx, %rax
 35d2a3b:      	je	0x35d2af2 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2d2>
 35d2a41:      	movq	%rax, %rdx
 35d2a44:      	jmp	0x35d2a63 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x243>
 35d2a46:      	nopw	%cs:(%rax,%rax)
 35d2a50:      	movl	%esi, (%rax)
 35d2a52:      	movq	%rdi, 0x8(%rax)
 35d2a56:      	addq	$0x10, %rax
 35d2a5a:      	cmpq	%rcx, %rdx
 35d2a5d:      	je	0x35d2af2 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2d2>
 35d2a63:      	movl	(%rdx), %esi
 35d2a65:      	movq	0x8(%rdx), %rdi
 35d2a69:      	addq	$0x10, %rdx
 35d2a6d:      	cmpq	%rcx, %rdx
 35d2a70:      	je	0x35d2a50 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d2a72:      	nopw	%cs:(%rax,%rax)
 35d2a7c:      	nopl	(%rax)
 35d2a80:      	cmpl	%esi, (%rdx)
 35d2a82:      	jne	0x35d2a50 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d2a84:      	orq	0x8(%rdx), %rdi
 35d2a88:      	addq	$0x10, %rdx
 35d2a8c:      	cmpq	%rcx, %rdx
 35d2a8f:      	jne	0x35d2a80 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x260>
 35d2a91:      	jmp	0x35d2a50 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d2a93:      	nopw	%cs:(%rax,%rax)
 35d2a9d:      	nopl	(%rax)
 35d2aa0:      	movl	%eax, (%rcx)
 35d2aa2:      	movq	(%rsp), %rax
 35d2aa6:      	movq	%rax, 0x4(%rcx)
 35d2aaa:      	movl	0x8(%rsp), %eax
 35d2aae:      	movl	%eax, 0xc(%rcx)
 35d2ab1:      	addq	$0x10, %r14
 35d2ab5:      	cmpq	%r15, %r14
 35d2ab8:      	je	0x35d2a2a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2abe:      	movl	(%r14), %eax
 35d2ac1:      	movl	0xc(%r14), %ecx
 35d2ac5:      	movl	%ecx, 0x8(%rsp)
 35d2ac9:      	movq	0x4(%r14), %rcx
 35d2acd:      	movq	%rcx, (%rsp)
 35d2ad1:      	movq	%r14, %rcx
 35d2ad4:      	cmpl	-0x10(%r14), %eax
 35d2ad8:      	jae	0x35d2aa0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x280>
 35d2ada:      	movq	%r14, %rcx
 35d2add:      	nopl	(%rax)
 35d2ae0:      	movups	-0x10(%rcx), %xmm0
 35d2ae4:      	movups	%xmm0, (%rcx)
 35d2ae7:      	cmpl	-0x20(%rcx), %eax
 35d2aea:      	leaq	-0x10(%rcx), %rcx
 35d2aee:      	jb	0x35d2ae0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2c0>
 35d2af0:      	jmp	0x35d2aa0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x280>
 35d2af2:      	cmpq	%rcx, %rax
 35d2af5:      	je	0x35d2afe <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2de>
 35d2af7:      	movq	%rax, 0xc0(%rbp)
 35d2afe:      	addq	$0x18, %rsp
 35d2b02:      	popq	%rbx
 35d2b03:      	popq	%r12
 35d2b05:      	popq	%r13
 35d2b07:      	popq	%r14
 35d2b09:      	popq	%r15
 35d2b0b:      	popq	%rbp
 35d2b0c:      	retq
