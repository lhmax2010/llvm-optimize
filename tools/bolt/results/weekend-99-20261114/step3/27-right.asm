
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000007fe6da0 <_ZN4llvm17DWARFDebugAranges9constructEv>:
 7fe6da0:      	pushq	%rbp
 7fe6da1:      	pushq	%r15
 7fe6da3:      	pushq	%r14
 7fe6da5:      	pushq	%r13
 7fe6da7:      	pushq	%r12
 7fe6da9:      	pushq	%rbx
 7fe6daa:      	subq	$0x78, %rsp
 7fe6dae:      	leaq	0x28(%rsp), %rax
 7fe6db3:      	movl	$0x0, 0x28(%rsp)
 7fe6dbb:      	movq	$0x0, 0x30(%rsp)
 7fe6dc4:      	movq	%rax, 0x38(%rsp)
 7fe6dc9:      	movq	%rax, 0x40(%rsp)
 7fe6dce:      	movq	$0x0, 0x48(%rsp)
 7fe6dd7:      	movq	(%rdi), %r15
 7fe6dda:      	movq	0x8(%rdi), %r12
 7fe6dde:      	cmpq	%r12, %r15
 7fe6de1:      	je	0x7fe73ad <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe6de7:      	movq	%rdi, 0x50(%rsp)
 7fe6dec:      	movq	%r12, %rbx
 7fe6def:      	subq	%r15, %rbx
 7fe6df2:      	movq	%rbx, %rax
 7fe6df5:      	sarq	$0x3, %rax
 7fe6df9:      	movabsq	$-0x5555555555555555, %r14 # imm = 0xAAAAAAAAAAAAAAAB
 7fe6e03:      	imulq	%r14, %rax
 7fe6e07:      	bsrq	%rax, %rdx
 7fe6e0b:      	xorl	$0x3f, %edx
 7fe6e0e:      	addl	%edx, %edx
 7fe6e10:      	xorq	$0x7e, %rdx
 7fe6e14:      	movq	%r15, %rdi
 7fe6e17:      	movq	%r12, %rsi
 7fe6e1a:      	callq	0x7fe7470 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPN4llvm17DWARFDebugAranges13RangeEndpointESt6vectorIS4_SaIS4_EEEElNS0_5__ops15_Iter_less_iterEEvT_SC_T0_T1_>
 7fe6e1f:      	leaq	0x18(%r15), %r13
 7fe6e23:      	cmpq	$0x181, %rbx            # imm = 0x181
 7fe6e2a:      	jl	0x7fe6eff <_ZN4llvm17DWARFDebugAranges9constructEv+0x15f>
 7fe6e30:      	leaq	0x18(%r15), %rbx
 7fe6e34:      	movl	$0x18, %ebp
 7fe6e39:      	movq	%r15, %rax
 7fe6e3c:      	jmp	0x7fe6e6b <_ZN4llvm17DWARFDebugAranges9constructEv+0xcb>
 7fe6e3e:      	nop
 7fe6e40:      	movq	%rcx, (%rdx)
 7fe6e43:      	movq	(%rsp), %rax
 7fe6e47:      	movq	%rax, 0x8(%rdx)
 7fe6e4b:      	movzbl	0x8(%rsp), %eax
 7fe6e50:      	movb	%al, 0x10(%rdx)
 7fe6e53:      	addq	$0x18, %rbp
 7fe6e57:      	addq	$0x18, %rbx
 7fe6e5b:      	movq	%r14, %rax
 7fe6e5e:      	cmpq	$0x180, %rbp            # imm = 0x180
 7fe6e65:      	je	0x7fe6ff5 <_ZN4llvm17DWARFDebugAranges9constructEv+0x255>
 7fe6e6b:      	leaq	(%r15,%rbp), %r14
 7fe6e6f:      	movq	(%r15,%rbp), %rcx
 7fe6e73:      	cmpq	(%r15), %rcx
 7fe6e76:      	jae	0x7fe6eb0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x110>
 7fe6e78:      	movq	0x10(%r14), %rcx
 7fe6e7c:      	movq	%rcx, 0x10(%rsp)
 7fe6e81:      	movups	(%r14), %xmm0
 7fe6e85:      	movaps	%xmm0, (%rsp)
 7fe6e89:      	cmpq	$0x19, %rbp
 7fe6e8d:      	jb	0x7fe6eed <_ZN4llvm17DWARFDebugAranges9constructEv+0x14d>
 7fe6e8f:      	movq	%r13, %rdi
 7fe6e92:      	movq	%r15, %rsi
 7fe6e95:      	movq	%rbp, %rdx
 7fe6e98:      	callq	0x828abc0 <memmove@plt>
 7fe6e9d:      	movzbl	0x10(%rsp), %eax
 7fe6ea2:      	movb	%al, 0x10(%r15)
 7fe6ea6:      	movaps	(%rsp), %xmm0
 7fe6eaa:      	movups	%xmm0, (%r15)
 7fe6eae:      	jmp	0x7fe6e53 <_ZN4llvm17DWARFDebugAranges9constructEv+0xb3>
 7fe6eb0:      	movups	0x20(%rax), %xmm0
 7fe6eb4:      	movaps	%xmm0, (%rsp)
 7fe6eb8:      	movq	%r14, %rdx
 7fe6ebb:      	cmpq	(%rax), %rcx
 7fe6ebe:      	jae	0x7fe6e40 <_ZN4llvm17DWARFDebugAranges9constructEv+0xa0>
 7fe6ec0:      	movq	%rbx, %rdx
 7fe6ec3:      	nopw	%cs:(%rax,%rax)
 7fe6ecd:      	nopl	(%rax)
 7fe6ed0:      	movzbl	-0x8(%rdx), %eax
 7fe6ed4:      	movb	%al, 0x10(%rdx)
 7fe6ed7:      	movups	-0x18(%rdx), %xmm0
 7fe6edb:      	movups	%xmm0, (%rdx)
 7fe6ede:      	cmpq	-0x30(%rdx), %rcx
 7fe6ee2:      	leaq	-0x18(%rdx), %rdx
 7fe6ee6:      	jb	0x7fe6ed0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x130>
 7fe6ee8:      	jmp	0x7fe6e40 <_ZN4llvm17DWARFDebugAranges9constructEv+0xa0>
 7fe6eed:      	movzbl	0x10(%r15), %ecx
 7fe6ef2:      	movb	%cl, 0x28(%rax)
 7fe6ef5:      	movups	(%r15), %xmm0
 7fe6ef9:      	movups	%xmm0, 0x18(%rax)
 7fe6efd:      	jmp	0x7fe6e9d <_ZN4llvm17DWARFDebugAranges9constructEv+0xfd>
 7fe6eff:      	cmpq	%r12, %r13
 7fe6f02:      	je	0x7fe705a <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe6f08:      	movq	%r15, %rax
 7fe6f0b:      	jmp	0x7fe6f33 <_ZN4llvm17DWARFDebugAranges9constructEv+0x193>
 7fe6f0d:      	nopl	(%rax)
 7fe6f10:      	movq	%rcx, (%rdx)
 7fe6f13:      	movq	(%rsp), %rax
 7fe6f17:      	movq	%rax, 0x8(%rdx)
 7fe6f1b:      	movzbl	0x8(%rsp), %eax
 7fe6f20:      	movb	%al, 0x10(%rdx)
 7fe6f23:      	leaq	0x18(%rbx), %r13
 7fe6f27:      	movq	%rbx, %rax
 7fe6f2a:      	cmpq	%r12, %r13
 7fe6f2d:      	je	0x7fe705a <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe6f33:      	movq	%r13, %rbx
 7fe6f36:      	movq	(%r13), %rcx
 7fe6f3a:      	cmpq	(%r15), %rcx
 7fe6f3d:      	jae	0x7fe6fa0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x200>
 7fe6f3f:      	movq	0x10(%rbx), %rcx
 7fe6f43:      	movq	%rcx, 0x10(%rsp)
 7fe6f48:      	movups	(%rbx), %xmm0
 7fe6f4b:      	movaps	%xmm0, (%rsp)
 7fe6f4f:      	movq	%rbx, %rdx
 7fe6f52:      	subq	%r15, %rdx
 7fe6f55:      	cmpq	$0x19, %rdx
 7fe6f59:      	jl	0x7fe6fdd <_ZN4llvm17DWARFDebugAranges9constructEv+0x23d>
 7fe6f5f:      	movq	%rdx, %rcx
 7fe6f62:      	shrq	$0x3, %rcx
 7fe6f66:      	imulq	%r14, %rcx
 7fe6f6a:      	negq	%rcx
 7fe6f6d:      	leaq	(%rcx,%rcx,2), %rcx
 7fe6f71:      	leaq	0x30(%rax,%rcx,8), %rdi
 7fe6f76:      	movq	%r15, %rsi
 7fe6f79:      	callq	0x828abc0 <memmove@plt>
 7fe6f7e:      	movzbl	0x10(%rsp), %eax
 7fe6f83:      	movb	%al, 0x10(%r15)
 7fe6f87:      	movaps	(%rsp), %xmm0
 7fe6f8b:      	movups	%xmm0, (%r15)
 7fe6f8f:      	leaq	0x18(%rbx), %r13
 7fe6f93:      	movq	%rbx, %rax
 7fe6f96:      	cmpq	%r12, %r13
 7fe6f99:      	jne	0x7fe6f33 <_ZN4llvm17DWARFDebugAranges9constructEv+0x193>
 7fe6f9b:      	jmp	0x7fe705a <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe6fa0:      	movups	0x20(%rax), %xmm0
 7fe6fa4:      	movaps	%xmm0, (%rsp)
 7fe6fa8:      	movq	%rbx, %rdx
 7fe6fab:      	cmpq	(%rax), %rcx
 7fe6fae:      	jae	0x7fe6f10 <_ZN4llvm17DWARFDebugAranges9constructEv+0x170>
 7fe6fb4:      	movq	%rbx, %rdx
 7fe6fb7:      	nopw	(%rax,%rax)
 7fe6fc0:      	movzbl	-0x8(%rdx), %eax
 7fe6fc4:      	movb	%al, 0x10(%rdx)
 7fe6fc7:      	movups	-0x18(%rdx), %xmm0
 7fe6fcb:      	movups	%xmm0, (%rdx)
 7fe6fce:      	cmpq	-0x30(%rdx), %rcx
 7fe6fd2:      	leaq	-0x18(%rdx), %rdx
 7fe6fd6:      	jb	0x7fe6fc0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x220>
 7fe6fd8:      	jmp	0x7fe6f10 <_ZN4llvm17DWARFDebugAranges9constructEv+0x170>
 7fe6fdd:      	cmpq	$0x18, %rdx
 7fe6fe1:      	jne	0x7fe6f7e <_ZN4llvm17DWARFDebugAranges9constructEv+0x1de>
 7fe6fe3:      	movzbl	0x10(%r15), %ecx
 7fe6fe8:      	movb	%cl, 0x28(%rax)
 7fe6feb:      	movups	(%r15), %xmm0
 7fe6fef:      	movups	%xmm0, 0x18(%rax)
 7fe6ff3:      	jmp	0x7fe6f7e <_ZN4llvm17DWARFDebugAranges9constructEv+0x1de>
 7fe6ff5:      	addq	$0x180, %r15            # imm = 0x180
 7fe6ffc:      	jmp	0x7fe7017 <_ZN4llvm17DWARFDebugAranges9constructEv+0x277>
 7fe6ffe:      	nop
 7fe7000:      	movq	%rax, (%rcx)
 7fe7003:      	movq	(%rsp), %rax
 7fe7007:      	movq	%rax, 0x8(%rcx)
 7fe700b:      	movzbl	0x8(%rsp), %eax
 7fe7010:      	movb	%al, 0x10(%rcx)
 7fe7013:      	addq	$0x18, %r15
 7fe7017:      	cmpq	%r12, %r15
 7fe701a:      	je	0x7fe705a <_ZN4llvm17DWARFDebugAranges9constructEv+0x2ba>
 7fe701c:      	movq	(%r15), %rax
 7fe701f:      	movups	0x8(%r15), %xmm0
 7fe7024:      	movaps	%xmm0, (%rsp)
 7fe7028:      	movq	%r15, %rcx
 7fe702b:      	cmpq	-0x18(%r15), %rax
 7fe702f:      	jae	0x7fe7000 <_ZN4llvm17DWARFDebugAranges9constructEv+0x260>
 7fe7031:      	movq	%r15, %rcx
 7fe7034:      	nopw	%cs:(%rax,%rax)
 7fe703e:      	nop
 7fe7040:      	movzbl	-0x8(%rcx), %edx
 7fe7044:      	movb	%dl, 0x10(%rcx)
 7fe7047:      	movups	-0x18(%rcx), %xmm0
 7fe704b:      	movups	%xmm0, (%rcx)
 7fe704e:      	cmpq	-0x30(%rcx), %rax
 7fe7052:      	leaq	-0x18(%rcx), %rcx
 7fe7056:      	jb	0x7fe7040 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2a0>
 7fe7058:      	jmp	0x7fe7000 <_ZN4llvm17DWARFDebugAranges9constructEv+0x260>
 7fe705a:      	movq	0x50(%rsp), %r13
 7fe705f:      	movq	(%r13), %rbp
 7fe7063:      	movq	0x8(%r13), %rax
 7fe7067:      	movq	%rax, 0x70(%rsp)
 7fe706c:      	cmpq	%rax, %rbp
 7fe706f:      	je	0x7fe73ad <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe7075:      	movq	$-0x1, %rbx
 7fe707c:      	movq	0x48(%rsp), %rcx
 7fe7081:      	leaq	0x28(%rsp), %r12
 7fe7086:      	jmp	0x7fe70c9 <_ZN4llvm17DWARFDebugAranges9constructEv+0x329>
 7fe7088:      	nopl	(%rax,%rax)
 7fe7090:      	movq	%r12, %rsi
 7fe7093:      	callq	0x828a850 <_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_@plt>
 7fe7098:      	movl	$0x28, %esi
 7fe709d:      	movq	%rax, %rdi
 7fe70a0:      	callq	0x828a660 <_ZdlPvm@plt>
 7fe70a5:      	movq	$-0x1, %rcx
 7fe70ac:      	addq	0x48(%rsp), %rcx
 7fe70b1:      	movq	%rcx, 0x48(%rsp)
 7fe70b6:      	movq	(%rbp), %rbx
 7fe70ba:      	addq	$0x18, %rbp
 7fe70be:      	cmpq	0x70(%rsp), %rbp
 7fe70c3:      	je	0x7fe739f <_ZN4llvm17DWARFDebugAranges9constructEv+0x5ff>
 7fe70c9:      	movq	(%rbp), %rax
 7fe70cd:      	movq	%rax, %r15
 7fe70d0:      	subq	%rbx, %r15
 7fe70d3:      	jbe	0x7fe7293 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4f3>
 7fe70d9:      	testq	%rcx, %rcx
 7fe70dc:      	je	0x7fe7293 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4f3>
 7fe70e2:      	movq	0x18(%r13), %r11
 7fe70e6:      	movq	0x20(%r13), %r12
 7fe70ea:      	cmpq	%r12, %r11
 7fe70ed:      	je	0x7fe7170 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe70f3:      	movq	-0x18(%r12), %rcx
 7fe70f8:      	movq	-0x10(%r12), %rdx
 7fe70fd:      	leaq	(%rcx,%rdx), %rsi
 7fe7101:      	cmpq	$0x1, %rdx
 7fe7105:      	movl	$0x0, %edx
 7fe710a:      	sbbq	%rdx, %rdx
 7fe710d:      	orq	%rsi, %rdx
 7fe7110:      	cmpq	%rbx, %rdx
 7fe7113:      	jne	0x7fe7170 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe7115:      	movq	0x30(%rsp), %r9
 7fe711a:      	testq	%r9, %r9
 7fe711d:      	je	0x7fe7170 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe711f:      	movq	-0x8(%r12), %rdx
 7fe7124:      	leaq	0x28(%rsp), %r10
 7fe7129:      	nopl	(%rax)
 7fe7130:      	movq	%r10, %rsi
 7fe7133:      	movq	%r9, %rdi
 7fe7136:      	movq	0x20(%r9), %r8
 7fe713a:      	xorl	%r9d, %r9d
 7fe713d:      	cmpq	%rdx, %r8
 7fe7140:      	setb	%r9b
 7fe7144:      	movq	%rdi, %r10
 7fe7147:      	cmovbq	%rsi, %r10
 7fe714b:      	movq	0x10(%rdi,%r9,8), %r9
 7fe7150:      	testq	%r9, %r9
 7fe7153:      	jne	0x7fe7130 <_ZN4llvm17DWARFDebugAranges9constructEv+0x390>
 7fe7155:      	leaq	0x28(%rsp), %r9
 7fe715a:      	cmpq	%r9, %r10
 7fe715d:      	je	0x7fe7170 <_ZN4llvm17DWARFDebugAranges9constructEv+0x3d0>
 7fe715f:      	cmpq	%rdx, %r8
 7fe7162:      	cmovbq	%rsi, %rdi
 7fe7166:      	cmpq	0x20(%rdi), %rdx
 7fe716a:      	jae	0x7fe7377 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5d7>
 7fe7170:      	movq	0x38(%rsp), %rax
 7fe7175:      	movq	0x20(%rax), %rax
 7fe7179:      	cmpq	0x28(%r13), %r12
 7fe717d:      	je	0x7fe719a <_ZN4llvm17DWARFDebugAranges9constructEv+0x3fa>
 7fe717f:      	movq	%rbx, (%r12)
 7fe7183:      	movq	%r15, 0x8(%r12)
 7fe7188:      	movq	%rax, 0x10(%r12)
 7fe718d:      	addq	$0x18, %r12
 7fe7191:      	movq	%r12, 0x20(%r13)
 7fe7195:      	jmp	0x7fe728e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe719a:      	movq	%rax, 0x68(%rsp)
 7fe719f:      	movq	%r12, %r14
 7fe71a2:      	subq	%r11, %r14
 7fe71a5:      	movabsq	$0x7ffffffffffffff8, %rax # imm = 0x7FFFFFFFFFFFFFF8
 7fe71af:      	cmpq	%rax, %r14
 7fe71b2:      	movq	%r11, 0x60(%rsp)
 7fe71b7:      	je	0x7fe73cb <_ZN4llvm17DWARFDebugAranges9constructEv+0x62b>
 7fe71bd:      	movq	%r14, %rax
 7fe71c0:      	sarq	$0x3, %rax
 7fe71c4:      	movabsq	$-0x5555555555555555, %rcx # imm = 0xAAAAAAAAAAAAAAAB
 7fe71ce:      	imulq	%rcx, %rax
 7fe71d2:      	cmpq	$0x1, %rax
 7fe71d6:      	movq	%rax, %rcx
 7fe71d9:      	adcq	$0x0, %rcx
 7fe71dd:      	leaq	(%rcx,%rax), %rsi
 7fe71e1:      	movabsq	$0x555555555555555, %rdx # imm = 0x555555555555555
 7fe71eb:      	cmpq	%rdx, %rsi
 7fe71ee:      	cmovaeq	%rdx, %rsi
 7fe71f2:      	addq	%rax, %rcx
 7fe71f5:      	cmovbq	%rdx, %rsi
 7fe71f9:      	movq	%rsi, 0x58(%rsp)
 7fe71fe:      	leaq	(,%rsi,8), %rax
 7fe7206:      	leaq	(%rax,%rax,2), %rdi
 7fe720a:      	callq	0x828a620 <_Znwm@plt>
 7fe720f:      	movq	%rax, %r13
 7fe7212:      	movq	%rbx, (%rax,%r14)
 7fe7216:      	movq	%r15, 0x8(%rax,%r14)
 7fe721b:      	movq	0x68(%rsp), %rax
 7fe7220:      	movq	%rax, 0x10(%r13,%r14)
 7fe7225:      	movq	%r13, %rbx
 7fe7228:      	movq	0x60(%rsp), %rdi
 7fe722d:      	cmpq	%r12, %rdi
 7fe7230:      	je	0x7fe725b <_ZN4llvm17DWARFDebugAranges9constructEv+0x4bb>
 7fe7232:      	movq	%r13, %rbx
 7fe7235:      	movq	%rdi, %rax
 7fe7238:      	nopl	(%rax,%rax)
 7fe7240:      	movq	0x10(%rax), %rcx
 7fe7244:      	movq	%rcx, 0x10(%rbx)
 7fe7248:      	movups	(%rax), %xmm0
 7fe724b:      	movups	%xmm0, (%rbx)
 7fe724e:      	addq	$0x18, %rax
 7fe7252:      	addq	$0x18, %rbx
 7fe7256:      	cmpq	%r12, %rax
 7fe7259:      	jne	0x7fe7240 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4a0>
 7fe725b:      	testq	%rdi, %rdi
 7fe725e:      	je	0x7fe7268 <_ZN4llvm17DWARFDebugAranges9constructEv+0x4c8>
 7fe7260:      	movq	%r14, %rsi
 7fe7263:      	callq	0x828a660 <_ZdlPvm@plt>
 7fe7268:      	addq	$0x18, %rbx
 7fe726c:      	movq	0x50(%rsp), %rcx
 7fe7271:      	movq	%r13, 0x18(%rcx)
 7fe7275:      	movq	%rbx, 0x20(%rcx)
 7fe7279:      	movq	0x58(%rsp), %rax
 7fe727e:      	leaq	(%rax,%rax,2), %rax
 7fe7282:      	leaq	(%r13,%rax,8), %rax
 7fe7287:      	movq	%rcx, %r13
 7fe728a:      	movq	%rax, 0x28(%rcx)
 7fe728e:      	leaq	0x28(%rsp), %r12
 7fe7293:      	cmpb	$0x1, 0x10(%rbp)
 7fe7297:      	jne	0x7fe72e0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x540>
 7fe7299:      	movq	0x30(%rsp), %rcx
 7fe729e:      	movq	0x8(%rbp), %rbx
 7fe72a2:      	testq	%rcx, %rcx
 7fe72a5:      	je	0x7fe7347 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5a7>
 7fe72ab:      	nopl	(%rax,%rax)
 7fe72b0:      	movq	%rcx, %r15
 7fe72b3:      	movq	0x20(%rcx), %rax
 7fe72b7:      	xorl	%ecx, %ecx
 7fe72b9:      	cmpq	%rax, %rbx
 7fe72bc:      	setae	%cl
 7fe72bf:      	movq	0x10(%r15,%rcx,8), %rcx
 7fe72c4:      	testq	%rcx, %rcx
 7fe72c7:      	jne	0x7fe72b0 <_ZN4llvm17DWARFDebugAranges9constructEv+0x510>
 7fe72c9:      	cmpq	%rax, %rbx
 7fe72cc:      	setb	%al
 7fe72cf:      	cmpq	%r12, %r15
 7fe72d2:      	sete	%r14b
 7fe72d6:      	orb	%al, %r14b
 7fe72d9:      	jmp	0x7fe734d <_ZN4llvm17DWARFDebugAranges9constructEv+0x5ad>
 7fe72db:      	nopl	(%rax,%rax)
 7fe72e0:      	movq	0x30(%rsp), %r9
 7fe72e5:      	movq	%r12, %rdi
 7fe72e8:      	testq	%r9, %r9
 7fe72eb:      	je	0x7fe7090 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe72f1:      	movq	0x8(%rbp), %rax
 7fe72f5:      	movq	%r12, %rsi
 7fe72f8:      	nopl	(%rax,%rax)
 7fe7300:      	movq	%rsi, %rcx
 7fe7303:      	movq	%r9, %rdx
 7fe7306:      	movq	0x20(%r9), %r8
 7fe730a:      	xorl	%edi, %edi
 7fe730c:      	cmpq	%rax, %r8
 7fe730f:      	setb	%dil
 7fe7313:      	movq	%r9, %rsi
 7fe7316:      	cmovbq	%rcx, %rsi
 7fe731a:      	movq	0x10(%r9,%rdi,8), %r9
 7fe731f:      	testq	%r9, %r9
 7fe7322:      	jne	0x7fe7300 <_ZN4llvm17DWARFDebugAranges9constructEv+0x560>
 7fe7324:      	movq	%r12, %rdi
 7fe7327:      	cmpq	%r12, %rsi
 7fe732a:      	je	0x7fe7090 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe7330:      	cmpq	%rax, %r8
 7fe7333:      	cmovbq	%rcx, %rdx
 7fe7337:      	cmpq	0x20(%rdx), %rax
 7fe733b:      	cmovbq	%r12, %rsi
 7fe733f:      	movq	%rsi, %rdi
 7fe7342:      	jmp	0x7fe7090 <_ZN4llvm17DWARFDebugAranges9constructEv+0x2f0>
 7fe7347:      	movb	$0x1, %r14b
 7fe734a:      	movq	%r12, %r15
 7fe734d:      	movl	$0x28, %edi
 7fe7352:      	callq	0x828a620 <_Znwm@plt>
 7fe7357:      	movq	%rbx, 0x20(%rax)
 7fe735b:      	movzbl	%r14b, %edi
 7fe735f:      	movq	%rax, %rsi
 7fe7362:      	movq	%r15, %rdx
 7fe7365:      	movq	%r12, %rcx
 7fe7368:      	callq	0x828a750 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 7fe736d:      	movl	$0x1, %ecx
 7fe7372:      	jmp	0x7fe70ac <_ZN4llvm17DWARFDebugAranges9constructEv+0x30c>
 7fe7377:      	cmpq	$-0x1, %rax
 7fe737b:      	je	0x7fe7393 <_ZN4llvm17DWARFDebugAranges9constructEv+0x5f3>
 7fe737d:      	subq	%rcx, %rax
 7fe7380:      	movl	$0x0, %ecx
 7fe7385:      	cmovaeq	%rax, %rcx
 7fe7389:      	movq	%rcx, -0x10(%r12)
 7fe738e:      	jmp	0x7fe728e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe7393:      	xorl	%ecx, %ecx
 7fe7395:      	movq	%rcx, -0x10(%r12)
 7fe739a:      	jmp	0x7fe728e <_ZN4llvm17DWARFDebugAranges9constructEv+0x4ee>
 7fe739f:      	movq	(%r13), %rax
 7fe73a3:      	cmpq	%rax, 0x8(%r13)
 7fe73a7:      	je	0x7fe73ad <_ZN4llvm17DWARFDebugAranges9constructEv+0x60d>
 7fe73a9:      	movq	%rax, 0x8(%r13)
 7fe73ad:      	movq	0x30(%rsp), %rsi
 7fe73b2:      	leaq	0x20(%rsp), %rdi
 7fe73b7:      	callq	0x49e88b0 <_ZNSt8_Rb_treeImmSt9_IdentityImESt4lessImESaImEE8_M_eraseEPSt13_Rb_tree_nodeImE>
 7fe73bc:      	addq	$0x78, %rsp
 7fe73c0:      	popq	%rbx
 7fe73c1:      	popq	%r12
 7fe73c3:      	popq	%r13
 7fe73c5:      	popq	%r14
 7fe73c7:      	popq	%r15
 7fe73c9:      	popq	%rbp
 7fe73ca:      	retq
 7fe73cb:      	leaq	-0x734c9e8(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 7fe73d2:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
