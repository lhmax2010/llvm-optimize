
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007fe6e30 <_ZN4llvm17DWARFDebugAranges9constructEv>:
 7fe6e30:      	pushq	%rbp
 7fe6e31:      	pushq	%r15
 7fe6e33:      	pushq	%r14
 7fe6e35:      	pushq	%r13
 7fe6e37:      	pushq	%r12
 7fe6e39:      	pushq	%rbx
 7fe6e3a:      	subq	$0x78, %rsp
 7fe6e3e:      	leaq	0x28(%rsp), %rax
 7fe6e43:      	movl	$0x0, 0x28(%rsp)
 7fe6e4b:      	movq	$0x0, 0x30(%rsp)
 7fe6e54:      	movq	%rax, 0x38(%rsp)
 7fe6e59:      	movq	%rax, 0x40(%rsp)
 7fe6e5e:      	movq	$0x0, 0x48(%rsp)
 7fe6e67:      	movq	(%rdi), %r15
 7fe6e6a:      	movq	0x8(%rdi), %r12
 7fe6e6e:      	cmpq	%r12, %r15
 7fe6e71:      	je	0x7fe743d <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe6e77:      	movq	%rdi, 0x50(%rsp)
 7fe6e7c:      	movq	%r12, %rbx
 7fe6e7f:      	subq	%r15, %rbx
 7fe6e82:      	movq	%rbx, %rax
 7fe6e85:      	sarq	$0x3, %rax
 7fe6e89:      	movabsq	$-0x5555555555555555, %r14 # imm = 0xAAAAAAAAAAAAAAAB
 7fe6e93:      	imulq	%r14, %rax
 7fe6e97:      	bsrq	%rax, %rdx
 7fe6e9b:      	xorl	$0x3f, %edx
 7fe6e9e:      	addl	%edx, %edx
 7fe6ea0:      	xorq	$0x7e, %rdx
 7fe6ea4:      	movq	%r15, %rdi
 7fe6ea7:      	movq	%r12, %rsi
 7fe6eaa:      	callq	0x7fe7500 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm17DWARFDebugAranges13RangeEndpointESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_less_iterEEvT_SC_T0_T1_>
 7fe6eaf:      	leaq	0x18(%r15), %r13
 7fe6eb3:      	cmpq	$0x181, %rbx            # imm = 0x181
 7fe6eba:      	jl	0x7fe6f8f <_ZN4llvm17DWARFDebugAranges9constructEv+0x15f>
 7fe6ec0:      	movl	$0x18, %ebp
 7fe6ec5:      	movq	%r13, %rbx
 7fe6ec8:      	movq	%r15, %rax
 7fe6ecb:      	jmp	0x7fe6efb <_ZN4llvm17DWARFDebugAranges9constructEv+0xcb>
 7fe6ecd:      	nopl	(%rax)
 7fe6ed0:      	movq	%rcx, (%rdx)
 7fe6ed3:      	movq	(%rsp), %rax
 7fe6ed7:      	movq	%rax, 0x8(%rdx)
 7fe6edb:      	movzbl	0x8(%rsp), %eax
 7fe6ee0:      	movb	%al, 0x10(%rdx)
 7fe6ee3:      	addq	$0x18, %rbp
 7fe6ee7:      	addq	$0x18, %rbx
 7fe6eeb:      	movq	%r14, %rax
 7fe6eee:      	cmpq	$0x180, %rbp            # imm = 0x180
 7fe6ef5:      	je	0x7fe7085 <_ZN4llvm17DWARFDebugAranges9constructEv+0x255>
 7fe6efb:      	leaq	(%r15,%rbp), %r14
 7fe6eff:      	movq	(%r15,%rbp), %rcx
 7fe6f03:      	cmpq	(%r15), %rcx
 7fe6f06:      	jae	0x7fe6f40 <_ZN4llvm17DWARFDebugAranges9constructEv+0x110>
 7fe6f08:      	movq	0x10(%r14), %rcx
 7fe6f0c:      	movq	%rcx, 0x10(%rsp)
 7fe6f11:      	movups	(%r14), %xmm0
 7fe6f15:      	movaps	%xmm0, (%rsp)
 7fe6f19:      	cmpq	$0x19, %rbp
 7fe6f1d:      	jb	0x7fe6f7d <_ZN4llvm17DWARFDebugAranges9constructEv+0x14d>
 7fe6f1f:      	movq	%r13, %rdi
 7fe6f22:      	movq	%r15, %rsi
 7fe6f25:      	movq	%rbp, %rdx
 7fe6f28:      	callq	0x828ac50 <memmove@plt>
 7fe6f2d:      	movzbl	0x10(%rsp), %eax
 7fe6f32:      	movb	%al, 0x10(%r15)
 7fe6f36:      	movaps	(%rsp), %xmm0
 7fe6f3a:      	movups	%xmm0, (%r15)
 7fe6f3e:      	jmp	0x7fe6ee3 <_ZN4llvm17DWARFDebugAranges9constructEv+0xb3>
 7fe6f40:      	movups	0x20(%rax), %xmm0
 7fe6f44:      	movaps	%xmm0, (%rsp)
 7fe6f48:      	movq	%r14, %rdx
 7fe6f4b:      	cmpq	(%rax), %rcx
 7fe6f4e:      	jae	0x7fe6ed0 <_ZN4llvm17DWARFDebugAranges9constructEv+0xa0>
 7fe6f50:      	movq	%rbx, %rdx
 7fe6f53:      	nopw	%cs:(%rax,%rax)
 7fe6f5d:      	nopl	(%rax)
 7fe6f60:      	movzbl	-0x8(%rdx), %eax
 7fe6f64:      	movb	%al, 0x10(%rdx)
 7fe6f67:      	movups	-0x18(%rdx), %xmm0
 7fe6f6b:      	movups	%xmm0, (%rdx)
 7fe6f6e:      	cmpq	-0x30(%rdx), %rcx
 7fe6f72:      	leaq	-0x18(%rdx), %rdx
 7fe6f76:      	jb	0x7fe6f60 <_ZN4llvm17DWARFDebugAranges9constructEv+0x130>
 7fe6f78:      	jmp	0x7fe6ed0 <_ZN4llvm17DWARFDebugAranges9constructEv+0xa0>
 7fe6f7d:      	movzbl	0x10(%r15), %ecx
 7fe6f82:      	movb	%cl, 0x28(%rax)
 7fe6f85:      	movups	(%r15), %xmm0
 7fe6f89:      	movups	%xmm0, 0x18(%rax)
 7fe6f8d:      	jmp	0x7fe6f2d <_ZN4llvm17DWARFDebugAranges9constructEv+0xfd>
 7fe6f8f:      	cmpq	%r12, %r13
 7fe6f92:      	je	0x7fe70ea <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe6f98:      	movq	%r15, %rax
 7fe6f9b:      	jmp	0x7fe6fc3 <_ZN4llvm17DWARFDebugAranges9constructEv+0x193>
 7fe6f9d:      	nopl	(%rax)
 7fe6fa0:      	movq	%rcx, (%rdx)
 7fe6fa3:      	movq	(%rsp), %rax
 7fe6fa7:      	movq	%rax, 0x8(%rdx)
 7fe6fab:      	movzbl	0x8(%rsp), %eax
 7fe6fb0:      	movb	%al, 0x10(%rdx)
 7fe6fb3:      	leaq	0x18(%rbx), %r13
 7fe6fb7:      	movq	%rbx, %rax
 7fe6fba:      	cmpq	%r12, %r13
 7fe6fbd:      	je	0x7fe70ea <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe6fc3:      	movq	%r13, %rbx
 7fe6fc6:      	movq	(%r13), %rcx
 7fe6fca:      	cmpq	(%r15), %rcx
 7fe6fcd:      	jae	0x7fe7030 <_ZN4llvm17DWARFDebugAranges9constructEv+0x200>
 7fe6fcf:      	movq	0x10(%rbx), %rcx
 7fe6fd3:      	movq	%rcx, 0x10(%rsp)
 7fe6fd8:      	movups	(%rbx), %xmm0
 7fe6fdb:      	movaps	%xmm0, (%rsp)
 7fe6fdf:      	movq	%rbx, %rdx
 7fe6fe2:      	subq	%r15, %rdx
 7fe6fe5:      	cmpq	$0x19, %rdx
 7fe6fe9:      	jl	0x7fe706d <_ZN4llvm17DWARFDebugAranges9constructEv+0x23d>
 7fe6fef:      	movq	%rdx, %rcx
 7fe6ff2:      	shrq	$0x3, %rcx
 7fe6ff6:      	imulq	%r14, %rcx
 7fe6ffa:      	negq	%rcx
 7fe6ffd:      	leaq	(%rcx,%rcx,2), %rcx
 7fe7001:      	leaq	0x30(%rax,%rcx,8), %rdi
 7fe7006:      	movq	%r15, %rsi
 7fe7009:      	callq	0x828ac50 <memmove@plt>
 7fe700e:      	movzbl	0x10(%rsp), %eax
 7fe7013:      	movb	%al, 0x10(%r15)
 7fe7017:      	movaps	(%rsp), %xmm0
 7fe701b:      	movups	%xmm0, (%r15)
 7fe701f:      	leaq	0x18(%rbx), %r13
 7fe7023:      	movq	%rbx, %rax
 7fe7026:      	cmpq	%r12, %r13
 7fe7029:      	jne	0x7fe6fc3 <_ZN4llvm17DWARFDebugAranges9constructEv+0x193>
 7fe702b:      	jmp	0x7fe70ea <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe7030:      	movups	0x20(%rax), %xmm0
 7fe7034:      	movaps	%xmm0, (%rsp)
 7fe7038:      	movq	%rbx, %rdx
 7fe703b:      	cmpq	(%rax), %rcx
 7fe703e:      	jae	0x7fe6fa0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x170>
 7fe7044:      	movq	%rbx, %rdx
 7fe7047:      	nopw	(%rax,%rax)
 7fe7050:      	movzbl	-0x8(%rdx), %eax
 7fe7054:      	movb	%al, 0x10(%rdx)
 7fe7057:      	movups	-0x18(%rdx), %xmm0
 7fe705b:      	movups	%xmm0, (%rdx)
 7fe705e:      	cmpq	-0x30(%rdx), %rcx
 7fe7062:      	leaq	-0x18(%rdx), %rdx
 7fe7066:      	jb	0x7fe7050 <_ZN4llvm17DWARFDebugAranges9constructEv+0x220>
 7fe7068:      	jmp	0x7fe6fa0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x170>
 7fe706d:      	cmpq	$0x18, %rdx
 7fe7071:      	jne	0x7fe700e <_ZN4llvm17DWARFDebugAranges9constructEv+0x1de>
 7fe7073:      	movzbl	0x10(%r15), %ecx
 7fe7078:      	movb	%cl, 0x28(%rax)
 7fe707b:      	movups	(%r15), %xmm0
 7fe707f:      	movups	%xmm0, 0x18(%rax)
 7fe7083:      	jmp	0x7fe700e <_ZN4llvm17DWARFDebugAranges9constructEv+0x1de>
 7fe7085:      	addq	$0x180, %r15            # imm = 0x180
 7fe708c:      	jmp	0x7fe70a7 <_ZN4llvm17DWARFDebugAranges9constructEv+0x277>
 7fe708e:      	nop
 7fe7090:      	movq	%rax, (%rcx)
 7fe7093:      	movq	(%rsp), %rax
 7fe7097:      	movq	%rax, 0x8(%rcx)
 7fe709b:      	movzbl	0x8(%rsp), %eax
 7fe70a0:      	movb	%al, 0x10(%rcx)
 7fe70a3:      	addq	$0x18, %r15
 7fe70a7:      	cmpq	%r12, %r15
 7fe70aa:      	je	0x7fe70ea <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe70ac:      	movq	(%r15), %rax
 7fe70af:      	movups	0x8(%r15), %xmm0
 7fe70b4:      	movaps	%xmm0, (%rsp)
 7fe70b8:      	movq	%r15, %rcx
 7fe70bb:      	cmpq	-0x18(%r15), %rax
 7fe70bf:      	jae	0x7fe7090 <_ZN4llvm17DWARFDebugAranges9constructEv+0x260>
 7fe70c1:      	movq	%r15, %rcx
 7fe70c4:      	nopw	%cs:(%rax,%rax)
 7fe70ce:      	nop
 7fe70d0:      	movzbl	-0x8(%rcx), %edx
 7fe70d4:      	movb	%dl, 0x10(%rcx)
 7fe70d7:      	movups	-0x18(%rcx), %xmm0
 7fe70db:      	movups	%xmm0, (%rcx)
 7fe70de:      	cmpq	-0x30(%rcx), %rax
 7fe70e2:      	leaq	-0x18(%rcx), %rcx
 7fe70e6:      	jb	0x7fe70d0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2a0>
 7fe70e8:      	jmp	0x7fe7090 <_ZN4llvm17DWARFDebugAranges9constructEv+0x260>
 7fe70ea:      	movq	0x50(%rsp), %r13
 7fe70ef:      	movq	(%r13), %rbp
 7fe70f3:      	movq	0x8(%r13), %rax
 7fe70f7:      	movq	%rax, 0x70(%rsp)
 7fe70fc:      	cmpq	%rax, %rbp
 7fe70ff:      	je	0x7fe743d <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe7105:      	movq	$-0x1, %rbx
 7fe710c:      	movq	0x48(%rsp), %rcx
 7fe7111:      	leaq	0x28(%rsp), %r12
 7fe7116:      	jmp	0x7fe7159 <_ZN4llvm17DWARFDebugAranges9constructEv+0x329>
 7fe7118:      	nopl	(%rax,%rax)
 7fe7120:      	movq	%r12, %rsi
 7fe7123:      	callq	0x828a8e0 <_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_@plt>
 7fe7128:      	movl	$0x28, %esi
 7fe712d:      	movq	%rax, %rdi
 7fe7130:      	callq	0x828a6f0 <_ZdlPvm@plt>
 7fe7135:      	movq	$-0x1, %rcx
 7fe713c:      	addq	0x48(%rsp), %rcx
 7fe7141:      	movq	%rcx, 0x48(%rsp)
 7fe7146:      	movq	(%rbp), %rbx
 7fe714a:      	addq	$0x18, %rbp
 7fe714e:      	cmpq	0x70(%rsp), %rbp
 7fe7153:      	je	0x7fe742f <_ZN4llvm17DWARFDebugAranges9constructEv+0x5ff>
 7fe7159:      	movq	(%rbp), %rax
 7fe715d:      	movq	%rax, %r15
 7fe7160:      	subq	%rbx, %r15
 7fe7163:      	jbe	0x7fe7323 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4f3>
 7fe7169:      	testq	%rcx, %rcx
 7fe716c:      	je	0x7fe7323 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4f3>
 7fe7172:      	movq	0x18(%r13), %r11
 7fe7176:      	movq	0x20(%r13), %r12
 7fe717a:      	cmpq	%r12, %r11
 7fe717d:      	je	0x7fe7200 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe7183:      	movq	-0x18(%r12), %rcx
 7fe7188:      	movq	-0x10(%r12), %rdx
 7fe718d:      	leaq	(%rcx,%rdx), %rsi
 7fe7191:      	cmpq	$0x1, %rdx
 7fe7195:      	movl	$0x0, %edx
 7fe719a:      	sbbq	%rdx, %rdx
 7fe719d:      	orq	%rsi, %rdx
 7fe71a0:      	cmpq	%rbx, %rdx
 7fe71a3:      	jne	0x7fe7200 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe71a5:      	movq	0x30(%rsp), %r9
 7fe71aa:      	testq	%r9, %r9
 7fe71ad:      	je	0x7fe7200 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe71af:      	movq	-0x8(%r12), %rdx
 7fe71b4:      	leaq	0x28(%rsp), %r10
 7fe71b9:      	nopl	(%rax)
 7fe71c0:      	movq	%r10, %rsi
 7fe71c3:      	movq	%r9, %rdi
 7fe71c6:      	movq	0x20(%r9), %r8
 7fe71ca:      	xorl	%r9d, %r9d
 7fe71cd:      	cmpq	%rdx, %r8
 7fe71d0:      	setb	%r9b
 7fe71d4:      	movq	%rdi, %r10
 7fe71d7:      	cmovbq	%rsi, %r10
 7fe71db:      	movq	0x10(%rdi,%r9,8), %r9
 7fe71e0:      	testq	%r9, %r9
 7fe71e3:      	jne	0x7fe71c0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x390>
 7fe71e5:      	leaq	0x28(%rsp), %r9
 7fe71ea:      	cmpq	%r9, %r10
 7fe71ed:      	je	0x7fe7200 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe71ef:      	cmpq	%rdx, %r8
 7fe71f2:      	cmovbq	%rsi, %rdi
 7fe71f6:      	cmpq	0x20(%rdi), %rdx
 7fe71fa:      	jae	0x7fe7407 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5d7>
 7fe7200:      	movq	0x38(%rsp), %rax
 7fe7205:      	movq	0x20(%rax), %rax
 7fe7209:      	cmpq	0x28(%r13), %r12
 7fe720d:      	je	0x7fe722a <_ZN4llvm17DWARFDebugAranges9constructEv+0x3fa>
 7fe720f:      	movq	%rbx, (%r12)
 7fe7213:      	movq	%r15, 0x8(%r12)
 7fe7218:      	movq	%rax, 0x10(%r12)
 7fe721d:      	addq	$0x18, %r12
 7fe7221:      	movq	%r12, 0x20(%r13)
 7fe7225:      	jmp	0x7fe731e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe722a:      	movq	%rax, 0x68(%rsp)
 7fe722f:      	movq	%r12, %r14
 7fe7232:      	subq	%r11, %r14
 7fe7235:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 7fe723f:      	cmpq	%rax, %r14
 7fe7242:      	movq	%r11, 0x60(%rsp)
 7fe7247:      	je	0x7fe745b <_ZN4llvm17DWARFDebugAranges9constructEv+0x62b>
 7fe724d:      	movq	%r14, %rax
 7fe7250:      	sarq	$0x3, %rax
 7fe7254:      	movabsq	$-0x5555555555555555, %rcx # imm = 0xAAAAAAAAAAAAAAAB
 7fe725e:      	imulq	%rcx, %rax
 7fe7262:      	cmpq	$0x1, %rax
 7fe7266:      	movq	%rax, %rcx
 7fe7269:      	adcq	$0x0, %rcx
 7fe726d:      	leaq	(%rcx,%rax), %rsi
 7fe7271:      	movabsq	$0x555555555555555, %rdx # imm = 0x555555555555555
 7fe727b:      	cmpq	%rdx, %rsi
 7fe727e:      	cmovaeq	%rdx, %rsi
 7fe7282:      	addq	%rax, %rcx
 7fe7285:      	cmovbq	%rdx, %rsi
 7fe7289:      	movq	%rsi, 0x58(%rsp)
 7fe728e:      	leaq	(,%rsi,8), %rax
 7fe7296:      	leaq	(%rax,%rax,2), %rdi
 7fe729a:      	callq	0x828a6b0 <_Znwm@plt>
 7fe729f:      	movq	%rax, %r13
 7fe72a2:      	movq	%rbx, (%rax,%r14)
 7fe72a6:      	movq	%r15, 0x8(%rax,%r14)
 7fe72ab:      	movq	0x68(%rsp), %rax
 7fe72b0:      	movq	%rax, 0x10(%r13,%r14)
 7fe72b5:      	movq	%r13, %rbx
 7fe72b8:      	movq	0x60(%rsp), %rdi
 7fe72bd:      	cmpq	%r12, %rdi
 7fe72c0:      	je	0x7fe72eb <_ZN4llvm17DWARFDebugAranges9constructEv+0x4bb>
 7fe72c2:      	movq	%r13, %rbx
 7fe72c5:      	movq	%rdi, %rax
 7fe72c8:      	nopl	(%rax,%rax)
 7fe72d0:      	movq	0x10(%rax), %rcx
 7fe72d4:      	movq	%rcx, 0x10(%rbx)
 7fe72d8:      	movups	(%rax), %xmm0
 7fe72db:      	movups	%xmm0, (%rbx)
 7fe72de:      	addq	$0x18, %rax
 7fe72e2:      	addq	$0x18, %rbx
 7fe72e6:      	cmpq	%r12, %rax
 7fe72e9:      	jne	0x7fe72d0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4a0>
 7fe72eb:      	testq	%rdi, %rdi
 7fe72ee:      	je	0x7fe72f8 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4c8>
 7fe72f0:      	movq	%r14, %rsi
 7fe72f3:      	callq	0x828a6f0 <_ZdlPvm@plt>
 7fe72f8:      	addq	$0x18, %rbx
 7fe72fc:      	movq	0x50(%rsp), %rcx
 7fe7301:      	movq	%r13, 0x18(%rcx)
 7fe7305:      	movq	%rbx, 0x20(%rcx)
 7fe7309:      	movq	0x58(%rsp), %rax
 7fe730e:      	leaq	(%rax,%rax,2), %rax
 7fe7312:      	leaq	(%r13,%rax,8), %rax
 7fe7317:      	movq	%rcx, %r13
 7fe731a:      	movq	%rax, 0x28(%rcx)
 7fe731e:      	leaq	0x28(%rsp), %r12
 7fe7323:      	cmpb	$0x1, 0x10(%rbp)
 7fe7327:      	jne	0x7fe7370 <_ZN4llvm17DWARFDebugAranges9constructEv+0x540>
 7fe7329:      	movq	0x30(%rsp), %rcx
 7fe732e:      	movq	0x8(%rbp), %rbx
 7fe7332:      	testq	%rcx, %rcx
 7fe7335:      	je	0x7fe73d7 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5a7>
 7fe733b:      	nopl	(%rax,%rax)
 7fe7340:      	movq	%rcx, %r15
 7fe7343:      	movq	0x20(%rcx), %rax
 7fe7347:      	xorl	%ecx, %ecx
 7fe7349:      	cmpq	%rax, %rbx
 7fe734c:      	setae	%cl
 7fe734f:      	movq	0x10(%r15,%rcx,8), %rcx
 7fe7354:      	testq	%rcx, %rcx
 7fe7357:      	jne	0x7fe7340 <_ZN4llvm17DWARFDebugAranges9constructEv+0x510>
 7fe7359:      	cmpq	%rax, %rbx
 7fe735c:      	setb	%al
 7fe735f:      	cmpq	%r12, %r15
 7fe7362:      	sete	%r14b
 7fe7366:      	orb	%al, %r14b
 7fe7369:      	jmp	0x7fe73dd <_ZN4llvm17DWARFDebugAranges9constructEv+0x5ad>
 7fe736b:      	nopl	(%rax,%rax)
 7fe7370:      	movq	0x30(%rsp), %r9
 7fe7375:      	movq	%r12, %rdi
 7fe7378:      	testq	%r9, %r9
 7fe737b:      	je	0x7fe7120 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe7381:      	movq	0x8(%rbp), %rax
 7fe7385:      	movq	%r12, %rsi
 7fe7388:      	nopl	(%rax,%rax)
 7fe7390:      	movq	%rsi, %rcx
 7fe7393:      	movq	%r9, %rdx
 7fe7396:      	movq	0x20(%r9), %r8
 7fe739a:      	xorl	%edi, %edi
 7fe739c:      	cmpq	%rax, %r8
 7fe739f:      	setb	%dil
 7fe73a3:      	movq	%r9, %rsi
 7fe73a6:      	cmovbq	%rcx, %rsi
 7fe73aa:      	movq	0x10(%r9,%rdi,8), %r9
 7fe73af:      	testq	%r9, %r9
 7fe73b2:      	jne	0x7fe7390 <_ZN4llvm17DWARFDebugAranges9constructEv+0x560>
 7fe73b4:      	movq	%r12, %rdi
 7fe73b7:      	cmpq	%r12, %rsi
 7fe73ba:      	je	0x7fe7120 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe73c0:      	cmpq	%rax, %r8
 7fe73c3:      	cmovbq	%rcx, %rdx
 7fe73c7:      	cmpq	0x20(%rdx), %rax
 7fe73cb:      	cmovbq	%r12, %rsi
 7fe73cf:      	movq	%rsi, %rdi
 7fe73d2:      	jmp	0x7fe7120 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe73d7:      	movb	$0x1, %r14b
 7fe73da:      	movq	%r12, %r15
 7fe73dd:      	movl	$0x28, %edi
 7fe73e2:      	callq	0x828a6b0 <_Znwm@plt>
 7fe73e7:      	movq	%rbx, 0x20(%rax)
 7fe73eb:      	movzbl	%r14b, %edi
 7fe73ef:      	movq	%rax, %rsi
 7fe73f2:      	movq	%r15, %rdx
 7fe73f5:      	movq	%r12, %rcx
 7fe73f8:      	callq	0x828a7e0 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 7fe73fd:      	movl	$0x1, %ecx
 7fe7402:      	jmp	0x7fe713c <_ZN4llvm17DWARFDebugAranges9constructEv+0x30c>
 7fe7407:      	cmpq	$-0x1, %rax
 7fe740b:      	je	0x7fe7423 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5f3>
 7fe740d:      	subq	%rcx, %rax
 7fe7410:      	movl	$0x0, %ecx
 7fe7415:      	cmovaeq	%rax, %rcx
 7fe7419:      	movq	%rcx, -0x10(%r12)
 7fe741e:      	jmp	0x7fe731e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe7423:      	xorl	%ecx, %ecx
 7fe7425:      	movq	%rcx, -0x10(%r12)
 7fe742a:      	jmp	0x7fe731e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe742f:      	movq	(%r13), %rax
 7fe7433:      	cmpq	%rax, 0x8(%r13)
 7fe7437:      	je	0x7fe743d <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe7439:      	movq	%rax, 0x8(%r13)
 7fe743d:      	movq	0x30(%rsp), %rsi
 7fe7442:      	leaq	0x20(%rsp), %rdi
 7fe7447:      	callq	0x49e8940 <_ZNSt8_Rb_treeImmSt9_IdentityImESt4lessImESaImEE8_M_eraseEPSt13_Rb_tree_nodeImE>
 7fe744c:      	addq	$0x78, %rsp
 7fe7450:      	popq	%rbx
 7fe7451:      	popq	%r12
 7fe7453:      	popq	%r13
 7fe7455:      	popq	%r14
 7fe7457:      	popq	%r15
 7fe7459:      	popq	%rbp
 7fe745a:      	retq
 7fe745b:      	leaq	-0x734ca78(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 7fe7462:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
