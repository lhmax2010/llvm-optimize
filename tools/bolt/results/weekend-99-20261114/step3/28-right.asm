
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000035d2790 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv>:
 35d2790:      	pushq	%rbp
 35d2791:      	pushq	%r15
 35d2793:      	pushq	%r14
 35d2795:      	pushq	%r13
 35d2797:      	pushq	%r12
 35d2799:      	pushq	%rbx
 35d279a:      	subq	$0x18, %rsp
 35d279e:      	movq	%rdi, %rbp
 35d27a1:      	movq	0xb8(%rdi), %r14
 35d27a8:      	movq	0xc0(%rdi), %r15
 35d27af:      	cmpq	%r15, %r14
 35d27b2:      	je	0x35d299a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d27b8:      	movq	%r15, %rbx
 35d27bb:      	subq	%r14, %rbx
 35d27be:      	movq	%rbx, %rax
 35d27c1:      	sarq	$0x4, %rax
 35d27c5:      	bsrq	%rax, %rdx
 35d27c9:      	xorl	$0x3f, %edx
 35d27cc:      	addl	%edx, %edx
 35d27ce:      	xorq	$0x7e, %rdx
 35d27d2:      	movq	%r14, %rdi
 35d27d5:      	movq	%r15, %rsi
 35d27d8:      	callq	0x35db6c0 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm17MachineBasicBlock16RegisterMaskPairESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_comp_iterIZNS3_17sortUniqueLiveInsEvE3$_0EEEvT_SE_T0_T1_>
 35d27dd:      	leaq	0x10(%r14), %r12
 35d27e1:      	cmpq	$0x101, %rbx            # imm = 0x101
 35d27e8:      	jl	0x35d28af <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x11f>
 35d27ee:      	movq	%rbp, 0x10(%rsp)
 35d27f3:      	leaq	0x10(%r14), %rbp
 35d27f7:      	movl	$0x10, %r13d
 35d27fd:      	movq	%r14, %rax
 35d2800:      	jmp	0x35d2839 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xa9>
 35d2802:      	nopw	%cs:(%rax,%rax)
 35d280c:      	nopl	(%rax)
 35d2810:      	movl	%ecx, (%rdx)
 35d2812:      	movq	(%rsp), %rax
 35d2816:      	movq	%rax, 0x4(%rdx)
 35d281a:      	movl	0x8(%rsp), %eax
 35d281e:      	movl	%eax, 0xc(%rdx)
 35d2821:      	addq	$0x10, %r13
 35d2825:      	addq	$0x10, %rbp
 35d2829:      	movq	%rbx, %rax
 35d282c:      	cmpq	$0x100, %r13            # imm = 0x100
 35d2833:      	je	0x35d2985 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1f5>
 35d2839:      	leaq	(%r14,%r13), %rbx
 35d283d:      	movl	(%r14,%r13), %ecx
 35d2841:      	cmpl	(%r14), %ecx
 35d2844:      	jae	0x35d2870 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xe0>
 35d2846:      	movups	(%rbx), %xmm0
 35d2849:      	movaps	%xmm0, (%rsp)
 35d284d:      	cmpq	$0x11, %r13
 35d2851:      	jb	0x35d28a5 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x115>
 35d2853:      	movq	%r12, %rdi
 35d2856:      	movq	%r14, %rsi
 35d2859:      	movq	%r13, %rdx
 35d285c:      	callq	0x828abc0 <memmove@plt>
 35d2861:      	movaps	(%rsp), %xmm0
 35d2865:      	movups	%xmm0, (%r14)
 35d2869:      	jmp	0x35d2821 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x91>
 35d286b:      	nopl	(%rax,%rax)
 35d2870:      	movl	0x1c(%rax), %edx
 35d2873:      	movl	%edx, 0x8(%rsp)
 35d2877:      	movq	0x14(%rax), %rdx
 35d287b:      	movq	%rdx, (%rsp)
 35d287f:      	movq	%rbx, %rdx
 35d2882:      	cmpl	(%rax), %ecx
 35d2884:      	jae	0x35d2810 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x80>
 35d2886:      	movq	%rbp, %rdx
 35d2889:      	nopl	(%rax)
 35d2890:      	movups	-0x10(%rdx), %xmm0
 35d2894:      	movups	%xmm0, (%rdx)
 35d2897:      	cmpl	-0x20(%rdx), %ecx
 35d289a:      	leaq	-0x10(%rdx), %rdx
 35d289e:      	jb	0x35d2890 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x100>
 35d28a0:      	jmp	0x35d2810 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x80>
 35d28a5:      	movups	(%r14), %xmm0
 35d28a9:      	movups	%xmm0, 0x10(%rax)
 35d28ad:      	jmp	0x35d2861 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0xd1>
 35d28af:      	cmpq	%r15, %r12
 35d28b2:      	je	0x35d299a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d28b8:      	movq	%r14, %rdi
 35d28bb:      	jmp	0x35d28e1 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x151>
 35d28bd:      	nopl	(%rax)
 35d28c0:      	movl	%eax, (%rcx)
 35d28c2:      	movq	(%rsp), %rax
 35d28c6:      	movq	%rax, 0x4(%rcx)
 35d28ca:      	movl	0x8(%rsp), %eax
 35d28ce:      	movl	%eax, 0xc(%rcx)
 35d28d1:      	leaq	0x10(%r13), %r12
 35d28d5:      	movq	%r13, %rdi
 35d28d8:      	cmpq	%r15, %r12
 35d28db:      	je	0x35d299a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d28e1:      	movq	%r12, %r13
 35d28e4:      	movl	(%r12), %eax
 35d28e8:      	cmpl	(%r14), %eax
 35d28eb:      	jae	0x35d2940 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1b0>
 35d28ed:      	movups	(%r13), %xmm0
 35d28f2:      	movaps	%xmm0, (%rsp)
 35d28f6:      	movq	%r13, %rdx
 35d28f9:      	subq	%r14, %rdx
 35d28fc:      	movq	%rdx, %rax
 35d28ff:      	sarq	$0x4, %rax
 35d2903:      	cmpq	$0x2, %rax
 35d2907:      	jl	0x35d2975 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1e5>
 35d2909:      	shlq	$0x4, %rax
 35d290d:      	subq	%rax, %rdi
 35d2910:      	addq	$0x20, %rdi
 35d2914:      	movq	%r14, %rsi
 35d2917:      	callq	0x828abc0 <memmove@plt>
 35d291c:      	movaps	(%rsp), %xmm0
 35d2920:      	movups	%xmm0, (%r14)
 35d2924:      	leaq	0x10(%r13), %r12
 35d2928:      	movq	%r13, %rdi
 35d292b:      	cmpq	%r15, %r12
 35d292e:      	jne	0x35d28e1 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x151>
 35d2930:      	jmp	0x35d299a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2932:      	nopw	%cs:(%rax,%rax)
 35d293c:      	nopl	(%rax)
 35d2940:      	movl	0x1c(%rdi), %ecx
 35d2943:      	movl	%ecx, 0x8(%rsp)
 35d2947:      	movq	0x14(%rdi), %rcx
 35d294b:      	movq	%rcx, (%rsp)
 35d294f:      	movq	%r13, %rcx
 35d2952:      	cmpl	(%rdi), %eax
 35d2954:      	jae	0x35d28c0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x130>
 35d295a:      	movq	%r13, %rcx
 35d295d:      	nopl	(%rax)
 35d2960:      	movups	-0x10(%rcx), %xmm0
 35d2964:      	movups	%xmm0, (%rcx)
 35d2967:      	cmpl	-0x20(%rcx), %eax
 35d296a:      	leaq	-0x10(%rcx), %rcx
 35d296e:      	jb	0x35d2960 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x1d0>
 35d2970:      	jmp	0x35d28c0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x130>
 35d2975:      	cmpq	$0x10, %rdx
 35d2979:      	jne	0x35d291c <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x18c>
 35d297b:      	movups	(%r14), %xmm0
 35d297f:      	movups	%xmm0, 0x10(%rdi)
 35d2983:      	jmp	0x35d291c <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x18c>
 35d2985:      	addq	$0x100, %r14            # imm = 0x100
 35d298c:      	cmpq	%r15, %r14
 35d298f:      	movq	0x10(%rsp), %rbp
 35d2994:      	jne	0x35d2a2e <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x29e>
 35d299a:      	movq	0xb8(%rbp), %rax
 35d29a1:      	movq	0xc0(%rbp), %rcx
 35d29a8:      	cmpq	%rcx, %rax
 35d29ab:      	je	0x35d2a62 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2d2>
 35d29b1:      	movq	%rax, %rdx
 35d29b4:      	jmp	0x35d29d3 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x243>
 35d29b6:      	nopw	%cs:(%rax,%rax)
 35d29c0:      	movl	%esi, (%rax)
 35d29c2:      	movq	%rdi, 0x8(%rax)
 35d29c6:      	addq	$0x10, %rax
 35d29ca:      	cmpq	%rcx, %rdx
 35d29cd:      	je	0x35d2a62 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2d2>
 35d29d3:      	movl	(%rdx), %esi
 35d29d5:      	movq	0x8(%rdx), %rdi
 35d29d9:      	addq	$0x10, %rdx
 35d29dd:      	cmpq	%rcx, %rdx
 35d29e0:      	je	0x35d29c0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d29e2:      	nopw	%cs:(%rax,%rax)
 35d29ec:      	nopl	(%rax)
 35d29f0:      	cmpl	%esi, (%rdx)
 35d29f2:      	jne	0x35d29c0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d29f4:      	orq	0x8(%rdx), %rdi
 35d29f8:      	addq	$0x10, %rdx
 35d29fc:      	cmpq	%rcx, %rdx
 35d29ff:      	jne	0x35d29f0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x260>
 35d2a01:      	jmp	0x35d29c0 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x230>
 35d2a03:      	nopw	%cs:(%rax,%rax)
 35d2a0d:      	nopl	(%rax)
 35d2a10:      	movl	%eax, (%rcx)
 35d2a12:      	movq	(%rsp), %rax
 35d2a16:      	movq	%rax, 0x4(%rcx)
 35d2a1a:      	movl	0x8(%rsp), %eax
 35d2a1e:      	movl	%eax, 0xc(%rcx)
 35d2a21:      	addq	$0x10, %r14
 35d2a25:      	cmpq	%r15, %r14
 35d2a28:      	je	0x35d299a <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x20a>
 35d2a2e:      	movl	(%r14), %eax
 35d2a31:      	movl	0xc(%r14), %ecx
 35d2a35:      	movl	%ecx, 0x8(%rsp)
 35d2a39:      	movq	0x4(%r14), %rcx
 35d2a3d:      	movq	%rcx, (%rsp)
 35d2a41:      	movq	%r14, %rcx
 35d2a44:      	cmpl	-0x10(%r14), %eax
 35d2a48:      	jae	0x35d2a10 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x280>
 35d2a4a:      	movq	%r14, %rcx
 35d2a4d:      	nopl	(%rax)
 35d2a50:      	movups	-0x10(%rcx), %xmm0
 35d2a54:      	movups	%xmm0, (%rcx)
 35d2a57:      	cmpl	-0x20(%rcx), %eax
 35d2a5a:      	leaq	-0x10(%rcx), %rcx
 35d2a5e:      	jb	0x35d2a50 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2c0>
 35d2a60:      	jmp	0x35d2a10 <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x280>
 35d2a62:      	cmpq	%rcx, %rax
 35d2a65:      	je	0x35d2a6e <_ZN4llvm17MachineBasicBlock17sortUniqueLiveInsEv+0x2de>
 35d2a67:      	movq	%rax, 0xc0(%rbp)
 35d2a6e:      	addq	$0x18, %rsp
 35d2a72:      	popq	%rbx
 35d2a73:      	popq	%r12
 35d2a75:      	popq	%r13
 35d2a77:      	popq	%r14
 35d2a79:      	popq	%r15
 35d2a7b:      	popq	%rbp
 35d2a7c:      	retq
