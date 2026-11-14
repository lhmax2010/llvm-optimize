
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002957ec0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>:
 2957ec0:      	pushq	%rbp
 2957ec1:      	pushq	%r15
 2957ec3:      	pushq	%r14
 2957ec5:      	pushq	%r13
 2957ec7:      	pushq	%r12
 2957ec9:      	pushq	%rbx
 2957eca:      	subq	$0x1d8, %rsp            # imm = 0x1D8
 2957ed1:      	movl	%r9d, %r11d
 2957ed4:      	movq	%r8, %rbp
 2957ed7:      	movq	%rdx, %rbx
 2957eda:      	movq	%rsi, %r12
 2957edd:      	movq	0x230(%rsp), %r15
 2957ee5:      	movq	0x228(%rsp), %r14
 2957eed:      	movq	0x220(%rsp), %r10
 2957ef5:      	leaq	0x210(%rsp), %rdx
 2957efd:      	movzwl	%cx, %eax
 2957f00:      	cmpl	$0x5d, %eax
 2957f03:      	jg	0x2958622 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x762>
 2957f09:      	cmpl	$0x30, %eax
 2957f0c:      	movq	%rdi, (%rsp)
 2957f10:      	je	0x2958717 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x857>
 2957f16:      	cmpl	$0x3e, %eax
 2957f19:      	jne	0x2958ca7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xde7>
 2957f1f:      	movq	%r15, %rax
 2957f22:      	movq	(%rdx), %r15
 2957f25:      	movl	0x8(%rdx), %r13d
 2957f29:      	movl	0xc(%rdx), %ecx
 2957f2c:      	movl	%ecx, 0x18(%rsp)
 2957f30:      	subq	$0x8, %rsp
 2957f34:      	movl	$0x3e, %esi
 2957f39:      	movq	%rbp, %rdx
 2957f3c:      	movl	%r11d, %ecx
 2957f3f:      	movq	%r15, %r8
 2957f42:      	movl	%r13d, %r9d
 2957f45:      	pushq	%rax
 2957f46:      	pushq	%r14
 2957f48:      	pushq	%r10
 2957f4a:      	pushq	%rbx
 2957f4b:      	pushq	%r12
 2957f4d:      	movq	%r12, %r14
 2957f50:      	movl	%r11d, %r12d
 2957f53:      	callq	0x296d980 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2957f58:      	addq	$0x30, %rsp
 2957f5c:      	testq	%rax, %rax
 2957f5f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2957f65:      	movq	%r15, 0x28(%rsp)
 2957f6a:      	movl	%r13d, 0x58(%rsp)
 2957f6f:      	movq	%rbx, 0x20(%rsp)
 2957f74:      	movq	(%rsp), %r15
 2957f78:      	movq	%r15, %rdi
 2957f7b:      	movl	$0x3e, %esi
 2957f80:      	movq	%rbp, %rdx
 2957f83:      	movl	%r12d, %ecx
 2957f86:      	movq	%r14, %r8
 2957f89:      	movq	0x220(%rsp), %r9
 2957f91:      	pushq	0x230(%rsp)
 2957f98:      	movq	0x230(%rsp), %r13
 2957fa0:      	pushq	%r13
 2957fa2:      	callq	0x2971570 <_ZL21lowerShuffleWithVPMOVRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2957fa7:      	addq	$0x10, %rsp
 2957fab:      	testq	%rax, %rax
 2957fae:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2957fb4:      	movq	%rbp, 0x10(%rsp)
 2957fb9:      	movq	0x20(%rsp), %r11
 2957fbe:      	testq	%r11, %r11
 2957fc1:      	movq	%r15, %rdi
 2957fc4:      	movl	%r12d, %ecx
 2957fc7:      	movq	%r14, %r12
 2957fca:      	movq	%r13, %rbx
 2957fcd:      	movq	0x220(%rsp), %r10
 2957fd5:      	movq	0x28(%rsp), %r14
 2957fda:      	je	0x295a4fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x263b>
 2957fe0:      	leaq	(,%r11,4), %r8
 2957fe8:      	addq	$-0x4, %r8
 2957fec:      	xorl	%ebp, %ebp
 2957fee:      	movq	%r12, %rax
 2957ff1:      	cmpq	$0x1c, %r8
 2957ff5:      	jb	0x2958065 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1a5>
 2957ff7:      	shrq	$0x2, %r8
 2957ffb:      	incq	%r8
 2957ffe:      	movq	%r8, %rdx
 2958001:      	andq	$-0x8, %rdx
 2958005:      	leaq	(%r12,%rdx,4), %rax
 2958009:      	pxor	%xmm0, %xmm0
 295800d:      	xorl	%esi, %esi
 295800f:      	movdqa	-0x1b39a27(%rip), %xmm2 # 0xe1e5f0 <.LCPI649_0>
 2958017:      	pxor	%xmm1, %xmm1
 295801b:      	nopl	(%rax,%rax)
 2958020:      	movdqu	(%r12,%rsi,4), %xmm3
 2958026:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 295802d:      	pcmpgtd	%xmm2, %xmm3
 2958031:      	psubd	%xmm3, %xmm1
 2958035:      	pcmpgtd	%xmm2, %xmm4
 2958039:      	psubd	%xmm4, %xmm0
 295803d:      	addq	$0x8, %rsi
 2958041:      	cmpq	%rsi, %rdx
 2958044:      	jne	0x2958020 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x160>
 2958046:      	paddd	%xmm1, %xmm0
 295804a:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295804f:      	paddd	%xmm0, %xmm1
 2958053:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2958058:      	paddd	%xmm1, %xmm0
 295805c:      	movd	%xmm0, %ebp
 2958060:      	cmpq	%rdx, %r8
 2958063:      	je	0x2958083 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c3>
 2958065:      	leaq	(%r12,%r11,4), %rsi
 2958069:      	nopl	(%rax)
 2958070:      	xorl	%edx, %edx
 2958072:      	cmpl	$0x8, (%rax)
 2958075:      	setge	%dl
 2958078:      	addl	%edx, %ebp
 295807a:      	addq	$0x4, %rax
 295807e:      	cmpq	%rsi, %rax
 2958081:      	jne	0x2958070 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b0>
 2958083:      	testl	%ebp, %ebp
 2958085:      	je	0x295a4fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x263b>
 295808b:      	movl	$0x3e, %esi
 2958090:      	movq	0x10(%rsp), %rdx
 2958095:      	movq	%r14, %r8
 2958098:      	movl	0x58(%rsp), %r15d
 295809d:      	movl	%r15d, %r9d
 29580a0:      	pushq	$0x0
 29580a2:      	pushq	0x238(%rsp)
 29580a9:      	pushq	%rbx
 29580aa:      	pushq	%r10
 29580ac:      	pushq	%r11
 29580ae:      	pushq	%r12
 29580b0:      	movl	%ecx, %r13d
 29580b3:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 29580b8:      	addq	$0x30, %rsp
 29580bc:      	testq	%rax, %rax
 29580bf:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29580c5:      	movl	%r13d, 0xc(%rsp)
 29580ca:      	movq	0x228(%rsp), %rbx
 29580d2:      	cmpb	$0x1, 0x1c6(%rbx)
 29580d9:      	jne	0x2958127 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x267>
 29580db:      	movq	0x220(%rsp), %r10
 29580e3:      	movl	0x8(%r10), %eax
 29580e7:      	subq	$0x8, %rsp
 29580eb:      	movq	0x8(%rsp), %rdi
 29580f0:      	movl	$0x3e, %esi
 29580f5:      	movq	0x18(%rsp), %rdx
 29580fa:      	movl	0x14(%rsp), %ecx
 29580fe:      	movq	%r14, %r8
 2958101:      	movl	%r15d, %r9d
 2958104:      	pushq	0x238(%rsp)
 295810b:      	pushq	%rax
 295810c:      	pushq	(%r10)
 295810f:      	pushq	0x40(%rsp)
 2958113:      	pushq	%r12
 2958115:      	callq	0x2973ef0 <_ZL21lowerShuffleWithSSE4ARKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGE>
 295811a:      	addq	$0x30, %rsp
 295811e:      	testq	%rax, %rax
 2958121:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958127:      	cmpl	$0x1, %ebp
 295812a:      	movq	0x10(%rsp), %rbp
 295812f:      	jne	0x2958177 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b7>
 2958131:      	movq	0x220(%rsp), %r10
 2958139:      	movl	0x8(%r10), %eax
 295813d:      	movq	(%rsp), %rdi
 2958141:      	movl	$0x3e, %esi
 2958146:      	movq	%rbp, %rdx
 2958149:      	movl	0xc(%rsp), %ecx
 295814d:      	movq	%r14, %r8
 2958150:      	movl	%r15d, %r9d
 2958153:      	pushq	0x230(%rsp)
 295815a:      	pushq	%rbx
 295815b:      	pushq	%rax
 295815c:      	pushq	(%r10)
 295815f:      	pushq	0x40(%rsp)
 2958163:      	pushq	%r12
 2958165:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295816a:      	addq	$0x30, %rsp
 295816e:      	testq	%rax, %rax
 2958171:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958177:      	movl	0x148(%rbx), %r13d
 295817e:      	cmpl	$0x5, %r13d
 2958182:      	jl	0x29581c6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x306>
 2958184:      	subq	$0x8, %rsp
 2958188:      	movq	0x8(%rsp), %rdi
 295818d:      	movl	$0x3e, %esi
 2958192:      	movq	%rbp, %rdx
 2958195:      	movl	0x14(%rsp), %ecx
 2958199:      	movq	%r14, %r8
 295819c:      	movl	%r15d, %r9d
 295819f:      	pushq	0x238(%rsp)
 29581a6:      	pushq	%rbx
 29581a7:      	pushq	0x238(%rsp)
 29581ae:      	pushq	0x40(%rsp)
 29581b2:      	pushq	%r12
 29581b4:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29581b9:      	addq	$0x30, %rsp
 29581bd:      	testq	%rax, %rax
 29581c0:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29581c6:      	movl	%r13d, 0x9c(%rsp)
 29581ce:      	movl	0x1e4(%rbx), %eax
 29581d4:      	subq	$0x8, %rsp
 29581d8:      	movq	0x8(%rsp), %r13
 29581dd:      	movq	%r13, %rdi
 29581e0:      	movl	$0x3e, %esi
 29581e5:      	movq	%rbp, %rdx
 29581e8:      	movl	%r15d, %r9d
 29581eb:      	movl	0x14(%rsp), %r15d
 29581f0:      	movl	%r15d, %ecx
 29581f3:      	movq	%r14, %r8
 29581f6:      	movq	0x238(%rsp), %rbp
 29581fe:      	pushq	%rbp
 29581ff:      	pushq	%rax
 2958200:      	pushq	0x238(%rsp)
 2958207:      	movq	0x40(%rsp), %rbp
 295820c:      	pushq	%rbp
 295820d:      	pushq	%r12
 295820f:      	callq	0x2969d70 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958214:      	addq	$0x30, %rsp
 2958218:      	testq	%rax, %rax
 295821b:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958221:      	subq	$0x8, %rsp
 2958225:      	movq	%r13, %rdi
 2958228:      	movl	$0x3e, %esi
 295822d:      	movq	0x18(%rsp), %rdx
 2958232:      	movl	%r15d, %ecx
 2958235:      	movq	%r14, %r8
 2958238:      	movl	0x60(%rsp), %r9d
 295823d:      	pushq	0x238(%rsp)
 2958244:      	pushq	%rbp
 2958245:      	pushq	%r12
 2958247:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295824c:      	addq	$0x20, %rsp
 2958250:      	testq	%rax, %rax
 2958253:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958259:      	movq	%r13, %rdi
 295825c:      	movl	$0x3e, %esi
 2958261:      	movq	0x10(%rsp), %rdx
 2958266:      	movl	%r15d, %ecx
 2958269:      	movq	%r14, %r8
 295826c:      	movl	0x58(%rsp), %r9d
 2958271:      	pushq	0x230(%rsp)
 2958278:      	pushq	%rbx
 2958279:      	pushq	%rbp
 295827a:      	pushq	%r12
 295827c:      	callq	0x2971bd0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958281:      	addq	$0x20, %rsp
 2958285:      	testq	%rax, %rax
 2958288:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295828e:      	movq	%r13, %rdi
 2958291:      	movl	$0x3e, %esi
 2958296:      	movq	0x10(%rsp), %rdx
 295829b:      	movl	%r15d, %ecx
 295829e:      	movq	%r14, %r8
 29582a1:      	movl	0x58(%rsp), %r9d
 29582a6:      	pushq	0x230(%rsp)
 29582ad:      	movq	%rbx, %r13
 29582b0:      	pushq	%rbx
 29582b1:      	pushq	0x230(%rsp)
 29582b8:      	movq	%r12, %r15
 29582bb:      	pushq	%r12
 29582bd:      	callq	0x2974350 <_ZL20lowerShuffleAsVTRUNCRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29582c2:      	addq	$0x20, %rsp
 29582c6:      	testq	%rax, %rax
 29582c9:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29582cf:      	movq	(%rsp), %rdi
 29582d3:      	movl	$0x3e, %esi
 29582d8:      	movq	0x10(%rsp), %rdx
 29582dd:      	movl	0xc(%rsp), %ecx
 29582e1:      	movq	0x28(%rsp), %r8
 29582e6:      	movl	0x58(%rsp), %r9d
 29582eb:      	pushq	0x230(%rsp)
 29582f2:      	pushq	%r13
 29582f4:      	pushq	0x30(%rsp)
 29582f8:      	pushq	%r15
 29582fa:      	callq	0x2966130 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29582ff:      	addq	$0x20, %rsp
 2958303:      	testq	%rax, %rax
 2958306:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295830c:      	subq	$0x8, %rsp
 2958310:      	movq	0x8(%rsp), %rdi
 2958315:      	movl	$0x3e, %esi
 295831a:      	movq	0x18(%rsp), %rdx
 295831f:      	movl	0x14(%rsp), %ecx
 2958323:      	movq	0x30(%rsp), %r8
 2958328:      	movl	0x60(%rsp), %r9d
 295832d:      	pushq	0x238(%rsp)
 2958334:      	pushq	0x30(%rsp)
 2958338:      	pushq	%r15
 295833a:      	callq	0x296a5d0 <_ZL22lowerShuffleAsBitBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295833f:      	addq	$0x20, %rsp
 2958343:      	testq	%rax, %rax
 2958346:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295834c:      	subq	$0x8, %rsp
 2958350:      	movq	0x8(%rsp), %rdi
 2958355:      	movl	$0x3e, %esi
 295835a:      	movq	0x18(%rsp), %rdx
 295835f:      	movl	0x14(%rsp), %ecx
 2958363:      	movq	0x30(%rsp), %r8
 2958368:      	movl	0x60(%rsp), %r9d
 295836d:      	pushq	0x238(%rsp)
 2958374:      	pushq	%r13
 2958376:      	pushq	0x238(%rsp)
 295837d:      	pushq	0x40(%rsp)
 2958381:      	pushq	%r15
 2958383:      	callq	0x2974ba0 <_ZL27lowerShuffleAsByteShiftMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958388:      	addq	$0x30, %rsp
 295838c:      	testq	%rax, %rax
 295838f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958395:      	movq	%r15, %rdi
 2958398:      	movq	0x20(%rsp), %rsi
 295839d:      	movl	$0x1, %edx
 29583a2:      	xorl	%ecx, %ecx
 29583a4:      	callq	0x29754d0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 29583a9:      	movl	%eax, %ebx
 29583ab:      	cmpl	$0x1, %eax
 29583ae:      	je	0x295c14c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x428c>
 29583b4:      	cmpl	$0x2, %ebx
 29583b7:      	jne	0x295c15a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x429a>
 29583bd:      	movl	0x148(%r13), %eax
 29583c4:      	cmpl	$0x5, %eax
 29583c7:      	jl	0x295c15a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x429a>
 29583cd:      	cmpb	$0x0, 0x1d1(%r13)
 29583d5:      	jne	0x295c15a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x429a>
 29583db:      	movb	$0x1, %r15b
 29583de:      	cmpl	$0x8, %eax
 29583e1:      	jb	0x295c78a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x48ca>
 29583e7:      	movq	0x10(%rsp), %rax
 29583ec:      	movl	0x18(%rax), %eax
 29583ef:      	cmpl	$0xf3, %eax
 29583f4:      	jne	0x295840c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54c>
 29583f6:      	movq	0x10(%rsp), %rcx
 29583fb:      	movq	0x28(%rcx), %rax
 29583ff:      	movq	(%rax), %rcx
 2958402:      	movl	0x18(%rcx), %eax
 2958405:      	cmpl	$0xf3, %eax
 295840a:      	je	0x29583fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x53b>
 295840c:      	cmpl	$0xa5, %eax
 2958411:      	jne	0x295c78a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x48ca>
 2958417:      	movq	0x28(%rsp), %rax
 295841c:      	movl	0x18(%rax), %eax
 295841f:      	cmpl	$0xf3, %eax
 2958424:      	jne	0x295843c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x57c>
 2958426:      	movq	0x28(%rsp), %rcx
 295842b:      	movq	0x28(%rcx), %rax
 295842f:      	movq	(%rax), %rcx
 2958432:      	movl	0x18(%rcx), %eax
 2958435:      	cmpl	$0xf3, %eax
 295843a:      	je	0x295842b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x56b>
 295843c:      	cmpl	$0xa5, %eax
 2958441:      	jne	0x295c78a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x48ca>
 2958447:      	movq	0x10(%rsp), %rdi
 295844c:      	movl	0xc(%rsp), %esi
 2958450:      	movq	0x28(%rsp), %rdx
 2958455:      	movl	0x58(%rsp), %ecx
 2958459:      	movq	0x230(%rsp), %rbx
 2958461:      	movq	%rbx, %r8
 2958464:      	movq	(%rsp), %r14
 2958468:      	movq	%r14, %r9
 295846b:      	callq	0x284b3f0 <_ZL16concatSubVectorsN4llvm7SDValueES0_RNS_12SelectionDAGERKNS_5SDLocE>
 2958470:      	movq	%rax, %r15
 2958473:      	movl	%edx, %ebp
 2958475:      	movl	0x148(%r13), %esi
 295847c:      	movl	$0x3f, %edi
 2958481:      	movq	%rbx, %rdx
 2958484:      	movq	%r14, %rcx
 2958487:      	callq	0x2842530 <_ZL13getZeroVectorN4llvm3MVTERKNS_12X86SubtargetERNS_12SelectionDAGERKNS_5SDLocE>
 295848c:      	movq	%rax, %r13
 295848f:      	movl	%edx, %r12d
 2958492:      	subq	$0x8, %rsp
 2958496:      	movq	$0x0, 0x18(%rsp)
 295849f:      	movl	$0xee, %esi
 29584a4:      	movq	%rbx, %rdi
 29584a7:      	movq	%r14, %rdx
 29584aa:      	movl	$0x5, %ecx
 29584af:      	xorl	%r8d, %r8d
 29584b2:      	movl	$0x1, %r9d
 29584b8:      	pushq	$0x0
 29584ba:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 29584bf:      	addq	$0x10, %rsp
 29584c3:      	movq	%rax, 0xa0(%rsp)
 29584cb:      	movl	%edx, 0xa8(%rsp)
 29584d2:      	movq	%r13, 0x30(%rsp)
 29584d7:      	movl	%r12d, 0x38(%rsp)
 29584dc:      	movq	%r15, 0x70(%rsp)
 29584e1:      	movl	%ebp, 0x78(%rsp)
 29584e5:      	movq	0x3b0(%rbx), %rax
 29584ec:      	movl	$0x0, %r9d
 29584f2:      	testq	%rax, %rax
 29584f5:      	je	0x29584fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x63b>
 29584f7:      	movl	0x8(%rax), %r9d
 29584fb:      	subq	$0x30, %rsp
 29584ff:      	movups	0xd0(%rsp), %xmm0
 2958507:      	movups	%xmm0, 0x20(%rsp)
 295850c:      	movups	0x60(%rsp), %xmm0
 2958511:      	movups	%xmm0, 0x10(%rsp)
 2958516:      	movups	0xa0(%rsp), %xmm0
 295851e:      	movups	%xmm0, (%rsp)
 2958522:      	movq	0x260(%rsp), %r15
 295852a:      	movq	%r15, %rdi
 295852d:      	movl	$0x239, %esi            # imm = 0x239
 2958532:      	movq	0x30(%rsp), %rbx
 2958537:      	movq	%rbx, %rdx
 295853a:      	movl	$0x3f, %ecx
 295853f:      	xorl	%r8d, %r8d
 2958542:      	callq	0x5e2ad10 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 2958547:      	addq	$0x30, %rsp
 295854b:      	movl	%edx, %r8d
 295854e:      	movq	%r15, %rdi
 2958551:      	movl	$0x4d, %esi
 2958556:      	xorl	%edx, %edx
 2958558:      	movq	%rax, %rcx
 295855b:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2958560:      	movq	%rax, %r14
 2958563:      	movl	%edx, %ebp
 2958565:      	movq	%rax, %rdi
 2958568:      	movl	%edx, %esi
 295856a:      	xorl	%edx, %edx
 295856c:      	movq	%r15, %rcx
 295856f:      	movq	%rbx, %r8
 2958572:      	movl	$0x80, %r9d
 2958578:      	callq	0x28e5b30 <_ZL16extractSubVectorN4llvm7SDValueEjRNS_12SelectionDAGERKNS_5SDLocEj>
 295857d:      	movq	%rax, %r13
 2958580:      	movl	%edx, %r12d
 2958583:      	movq	%r14, %rdi
 2958586:      	movl	%ebp, %esi
 2958588:      	movl	$0x4, %edx
 295858d:      	movq	%r15, %rcx
 2958590:      	movq	%rbx, %r8
 2958593:      	movl	$0x80, %r9d
 2958599:      	callq	0x28e5b30 <_ZL16extractSubVectorN4llvm7SDValueEjRNS_12SelectionDAGERKNS_5SDLocEj>
 295859e:      	movq	%rax, 0xa0(%rsp)
 29585a6:      	movl	%edx, 0xa8(%rsp)
 29585ad:      	movl	0x18(%rsp), %eax
 29585b1:      	movl	%eax, 0xac(%rsp)
 29585b8:      	movq	%r13, 0x30(%rsp)
 29585bd:      	movl	%r12d, 0x38(%rsp)
 29585c2:      	movq	0x3b0(%r15), %rax
 29585c9:      	testq	%rax, %rax
 29585cc:      	je	0x29585d6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x716>
 29585ce:      	movl	0x8(%rax), %eax
 29585d1:      	movq	%rax, 0x10(%rsp)
 29585d6:      	subq	$0x20, %rsp
 29585da:      	movups	0xc0(%rsp), %xmm0
 29585e2:      	movups	%xmm0, 0x10(%rsp)
 29585e7:      	movdqu	0x50(%rsp), %xmm0
 29585ed:      	movdqu	%xmm0, (%rsp)
 29585f2:      	movq	0x250(%rsp), %rdi
 29585fa:      	movl	$0x2b6, %esi            # imm = 0x2B6
 29585ff:      	movq	0x20(%rsp), %rdx
 2958604:      	movl	$0x3e, %ecx
 2958609:      	xorl	%r8d, %r8d
 295860c:      	movq	0x30(%rsp), %r9
 2958611:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 2958616:      	addq	$0x20, %rsp
 295861a:      	movl	%edx, %r8d
 295861d:      	jmp	0x295ca8b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4bcb>
 2958622:      	addl	$-0x6f, %eax
 2958625:      	cmpl	$0x27, %eax
 2958628:      	ja	0x2958e53 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf93>
 295862e:      	leaq	-0x1a86599(%rip), %rcx  # 0xed209c <.LCPI63_2+0xb5fc>
 2958635:      	movslq	(%rcx,%rax,4), %rax
 2958639:      	addq	%rcx, %rax
 295863c:      	jmpq	*%rax
 295863e:      	movq	%rdi, (%rsp)
 2958642:      	movdqu	(%rdx), %xmm0
 2958646:      	movdqa	%xmm0, 0x80(%rsp)
 295864f:      	testq	%rbx, %rbx
 2958652:      	je	0x2959a3d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b7d>
 2958658:      	leaq	(,%rbx,4), %rcx
 2958660:      	addq	$-0x4, %rcx
 2958664:      	xorl	%edx, %edx
 2958666:      	movq	%r12, %rax
 2958669:      	cmpq	$0x1c, %rcx
 295866d:      	jb	0x29586e5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x825>
 295866f:      	shrq	$0x2, %rcx
 2958673:      	incq	%rcx
 2958676:      	movq	%rcx, %rsi
 2958679:      	andq	$-0x8, %rsi
 295867d:      	leaq	(%r12,%rsi,4), %rax
 2958681:      	pxor	%xmm0, %xmm0
 2958685:      	xorl	%edx, %edx
 2958687:      	movdqa	-0x1b3a09f(%rip), %xmm2 # 0xe1e5f0 <.LCPI649_0>
 295868f:      	pxor	%xmm1, %xmm1
 2958693:      	nopw	%cs:(%rax,%rax)
 295869d:      	nopl	(%rax)
 29586a0:      	movdqu	(%r12,%rdx,4), %xmm3
 29586a6:      	movdqu	0x10(%r12,%rdx,4), %xmm4
 29586ad:      	pcmpgtd	%xmm2, %xmm3
 29586b1:      	psubd	%xmm3, %xmm1
 29586b5:      	pcmpgtd	%xmm2, %xmm4
 29586b9:      	psubd	%xmm4, %xmm0
 29586bd:      	addq	$0x8, %rdx
 29586c1:      	cmpq	%rdx, %rsi
 29586c4:      	jne	0x29586a0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x7e0>
 29586c6:      	paddd	%xmm1, %xmm0
 29586ca:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 29586cf:      	paddd	%xmm0, %xmm1
 29586d3:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 29586d8:      	paddd	%xmm1, %xmm0
 29586dc:      	movd	%xmm0, %edx
 29586e0:      	cmpq	%rsi, %rcx
 29586e3:      	je	0x2958704 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x844>
 29586e5:      	leaq	(%r12,%rbx,4), %rcx
 29586e9:      	nopl	(%rax)
 29586f0:      	xorl	%esi, %esi
 29586f2:      	cmpl	$0x8, (%rax)
 29586f5:      	setge	%sil
 29586f9:      	addl	%esi, %edx
 29586fb:      	addq	$0x4, %rax
 29586ff:      	cmpq	%rcx, %rax
 2958702:      	jne	0x29586f0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x830>
 2958704:      	cmpb	$0x1, 0x181(%r14)
 295870c:      	je	0x2959a4d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b8d>
 2958712:      	jmp	0x295a241 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2381>
 2958717:      	movdqu	(%rdx), %xmm0
 295871b:      	movdqa	%xmm0, 0x170(%rsp)
 2958724:      	movq	%r12, 0x130(%rsp)
 295872c:      	movq	%rbx, 0x138(%rsp)
 2958734:      	movq	%rbp, 0x60(%rsp)
 2958739:      	movl	%r11d, 0x68(%rsp)
 295873e:      	movq	0x170(%rsp), %r13
 2958746:      	movq	%r14, %rax
 2958749:      	movl	0x178(%rsp), %r14d
 2958751:      	movl	$0x30, %esi
 2958756:      	movq	%rbp, %rdx
 2958759:      	movl	%r11d, %ecx
 295875c:      	movq	%r13, %r8
 295875f:      	movl	%r14d, %r9d
 2958762:      	pushq	$0x0
 2958764:      	pushq	%r15
 2958766:      	pushq	%rax
 2958767:      	pushq	%r10
 2958769:      	pushq	%rbx
 295876a:      	pushq	%r12
 295876c:      	movq	%rbp, %r15
 295876f:      	movl	%r11d, %ebp
 2958772:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2958777:      	addq	$0x30, %rsp
 295877b:      	testq	%rax, %rax
 295877e:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958784:      	movq	(%rsp), %rdi
 2958788:      	movl	$0x30, %esi
 295878d:      	movq	%r15, %rdx
 2958790:      	movl	%ebp, %ecx
 2958792:      	movq	%r13, %r8
 2958795:      	movl	%r14d, %r9d
 2958798:      	pushq	0x230(%rsp)
 295879f:      	pushq	0x230(%rsp)
 29587a6:      	pushq	%rbx
 29587a7:      	pushq	%r12
 29587a9:      	callq	0x2966130 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29587ae:      	addq	$0x20, %rsp
 29587b2:      	testq	%rax, %rax
 29587b5:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29587bb:      	movq	(%rsp), %rdi
 29587bf:      	movl	$0x30, %esi
 29587c4:      	movq	%r15, %rdx
 29587c7:      	movl	%ebp, %ecx
 29587c9:      	movq	%r13, %r8
 29587cc:      	movl	%r14d, %r9d
 29587cf:      	pushq	0x230(%rsp)
 29587d6:      	pushq	0x230(%rsp)
 29587dd:      	pushq	%rbx
 29587de:      	pushq	%r12
 29587e0:      	callq	0x2971bd0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29587e5:      	addq	$0x20, %rsp
 29587e9:      	testq	%rax, %rax
 29587ec:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29587f2:      	subq	$0x8, %rsp
 29587f6:      	movq	0x8(%rsp), %rdi
 29587fb:      	movl	$0x30, %esi
 2958800:      	movq	%r15, %rdx
 2958803:      	movl	%ebp, %ecx
 2958805:      	movq	%r13, %r8
 2958808:      	movl	%r14d, %r9d
 295880b:      	pushq	0x238(%rsp)
 2958812:      	pushq	0x238(%rsp)
 2958819:      	movq	0x238(%rsp), %rax
 2958821:      	pushq	%rax
 2958822:      	pushq	%rbx
 2958823:      	pushq	%r12
 2958825:      	callq	0x296d980 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295882a:      	addq	$0x30, %rsp
 295882e:      	testq	%rax, %rax
 2958831:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958837:      	movq	%r13, 0x18(%rsp)
 295883c:      	movl	%r14d, 0x28(%rsp)
 2958841:      	movq	(%rsp), %rdi
 2958845:      	movl	$0x30, %esi
 295884a:      	movq	%r15, %rdx
 295884d:      	movl	%ebp, %ecx
 295884f:      	movq	%r12, %r8
 2958852:      	movq	0x220(%rsp), %r13
 295885a:      	movq	%r13, %r9
 295885d:      	pushq	0x230(%rsp)
 2958864:      	movq	0x230(%rsp), %r14
 295886c:      	pushq	%r14
 295886e:      	callq	0x2971570 <_ZL21lowerShuffleWithVPMOVRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958873:      	addq	$0x10, %rsp
 2958877:      	testq	%rax, %rax
 295887a:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958880:      	movq	(%rsp), %rdi
 2958884:      	movl	$0x30, %esi
 2958889:      	movq	%r15, %rdx
 295888c:      	movl	%ebp, %ecx
 295888e:      	movq	0x18(%rsp), %r8
 2958893:      	movl	0x28(%rsp), %r9d
 2958898:      	pushq	0x230(%rsp)
 295889f:      	pushq	%r14
 29588a1:      	pushq	%r13
 29588a3:      	pushq	%r12
 29588a5:      	callq	0x2974350 <_ZL20lowerShuffleAsVTRUNCRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29588aa:      	addq	$0x20, %rsp
 29588ae:      	testq	%rax, %rax
 29588b1:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29588b7:      	movq	0x230(%rsp), %r11
 29588bf:      	movl	%ebp, 0xc(%rsp)
 29588c3:      	cmpb	$0x1, 0x1c6(%r14)
 29588cb:      	movq	%r15, %rbp
 29588ce:      	jne	0x2958916 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xa56>
 29588d0:      	movq	0x220(%rsp), %r10
 29588d8:      	movl	0x8(%r10), %eax
 29588dc:      	subq	$0x8, %rsp
 29588e0:      	movq	0x8(%rsp), %rdi
 29588e5:      	movl	$0x30, %esi
 29588ea:      	movq	%rbp, %rdx
 29588ed:      	movl	0x14(%rsp), %ecx
 29588f1:      	movq	0x20(%rsp), %r8
 29588f6:      	movl	0x30(%rsp), %r9d
 29588fb:      	pushq	%r11
 29588fd:      	pushq	%rax
 29588fe:      	pushq	(%r10)
 2958901:      	pushq	%rbx
 2958902:      	pushq	%r12
 2958904:      	callq	0x2973ef0 <_ZL21lowerShuffleWithSSE4ARKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGE>
 2958909:      	addq	$0x30, %rsp
 295890d:      	testq	%rax, %rax
 2958910:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958916:      	testq	%rbx, %rbx
 2958919:      	movq	(%rsp), %rdi
 295891d:      	movl	0xc(%rsp), %ecx
 2958921:      	movl	0x28(%rsp), %r9d
 2958926:      	movq	0x18(%rsp), %r8
 295892b:      	je	0x295bb81 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3cc1>
 2958931:      	leaq	(,%rbx,4), %r10
 2958939:      	addq	$-0x4, %r10
 295893d:      	xorl	%r15d, %r15d
 2958940:      	movq	%r12, %rax
 2958943:      	cmpq	$0x1c, %r10
 2958947:      	jb	0x29589b7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xaf7>
 2958949:      	shrq	$0x2, %r10
 295894d:      	incq	%r10
 2958950:      	movq	%r10, %rdx
 2958953:      	andq	$-0x8, %rdx
 2958957:      	leaq	(%r12,%rdx,4), %rax
 295895b:      	pxor	%xmm0, %xmm0
 295895f:      	xorl	%esi, %esi
 2958961:      	movdqa	-0x1b413b9(%rip), %xmm2 # 0xe175b0 <.LCPI774_0>
 2958969:      	pxor	%xmm1, %xmm1
 295896d:      	movdqu	(%r12,%rsi,4), %xmm3
 2958973:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 295897a:      	pcmpgtd	%xmm2, %xmm3
 295897e:      	psubd	%xmm3, %xmm1
 2958982:      	pcmpgtd	%xmm2, %xmm4
 2958986:      	psubd	%xmm4, %xmm0
 295898a:      	addq	$0x8, %rsi
 295898e:      	cmpq	%rsi, %rdx
 2958991:      	jne	0x295896d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xaad>
 2958993:      	paddd	%xmm1, %xmm0
 2958997:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295899c:      	paddd	%xmm0, %xmm1
 29589a0:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 29589a5:      	paddd	%xmm1, %xmm0
 29589a9:      	movd	%xmm0, %r15d
 29589ae:      	cmpq	%rdx, %r10
 29589b1:      	movq	(%rsp), %rdi
 29589b5:      	je	0x29589cf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xb0f>
 29589b7:      	leaq	(%r12,%rbx,4), %rsi
 29589bb:      	xorl	%edx, %edx
 29589bd:      	cmpl	$0x10, (%rax)
 29589c0:      	setge	%dl
 29589c3:      	addl	%edx, %r15d
 29589c6:      	addq	$0x4, %rax
 29589ca:      	cmpq	%rsi, %rax
 29589cd:      	jne	0x29589bb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xafb>
 29589cf:      	testl	%r15d, %r15d
 29589d2:      	je	0x295bb81 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3cc1>
 29589d8:      	movl	0x1e4(%r14), %eax
 29589df:      	subq	$0x8, %rsp
 29589e3:      	movl	$0x30, %esi
 29589e8:      	movq	%rbp, %rdx
 29589eb:      	movq	%r14, %rbp
 29589ee:      	movl	%r9d, %r14d
 29589f1:      	movq	%r8, %r13
 29589f4:      	movq	0x238(%rsp), %r10
 29589fc:      	pushq	%r10
 29589fe:      	pushq	%rax
 29589ff:      	pushq	0x238(%rsp)
 2958a06:      	pushq	%rbx
 2958a07:      	pushq	%r12
 2958a09:      	callq	0x2969d70 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958a0e:      	addq	$0x30, %rsp
 2958a12:      	testq	%rax, %rax
 2958a15:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958a1b:      	movq	0x60(%rsp), %rdx
 2958a20:      	movl	0x68(%rsp), %ecx
 2958a24:      	movdqu	0x130(%rsp), %xmm0
 2958a2d:      	subq	$0x20, %rsp
 2958a31:      	movq	0x250(%rsp), %rax
 2958a39:      	movq	%rax, 0x10(%rsp)
 2958a3e:      	movdqu	%xmm0, (%rsp)
 2958a43:      	movq	0x20(%rsp), %rdi
 2958a48:      	movl	$0x30, %esi
 2958a4d:      	movq	%r13, %r8
 2958a50:      	movl	%r14d, %r9d
 2958a53:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2958a58:      	addq	$0x20, %rsp
 2958a5c:      	testq	%rax, %rax
 2958a5f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958a65:      	movq	0x60(%rsp), %rdx
 2958a6a:      	movl	0x68(%rsp), %ecx
 2958a6e:      	movdqu	0x130(%rsp), %xmm0
 2958a77:      	subq	$0x30, %rsp
 2958a7b:      	movq	0x260(%rsp), %rax
 2958a83:      	movq	%rax, 0x20(%rsp)
 2958a88:      	movq	%rbp, 0x18(%rsp)
 2958a8d:      	movq	0x250(%rsp), %rax
 2958a95:      	movq	%rax, 0x10(%rsp)
 2958a9a:      	movdqu	%xmm0, (%rsp)
 2958a9f:      	movq	0x30(%rsp), %rdi
 2958aa4:      	movl	$0x30, %esi
 2958aa9:      	movq	0x48(%rsp), %r8
 2958aae:      	movl	0x58(%rsp), %r9d
 2958ab3:      	callq	0x2974ba0 <_ZL27lowerShuffleAsByteShiftMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958ab8:      	addq	$0x30, %rsp
 2958abc:      	testq	%rax, %rax
 2958abf:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958ac5:      	movq	0x18(%rsp), %rax
 2958aca:      	movl	0x18(%rax), %r13d
 2958ace:      	addl	$-0x35, %r13d
 2958ad2:      	xorl	%r12d, %r12d
 2958ad5:      	cmpl	$0x2, %r13d
 2958ad9:      	setb	%r12b
 2958add:      	movq	0x130(%rsp), %rbx
 2958ae5:      	movq	0x138(%rsp), %r14
 2958aed:      	movq	%rbx, %rdi
 2958af0:      	movq	%r14, %rsi
 2958af3:      	movl	$0x1, %edx
 2958af8:      	movl	%r12d, %ecx
 2958afb:      	callq	0x29754d0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 2958b00:      	movq	%rax, 0x10(%rsp)
 2958b05:      	cmpl	$0x1, %eax
 2958b08:      	setne	%al
 2958b0b:      	cmpl	$0x4, 0x148(%rbp)
 2958b12:      	jl	0x295be72 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3fb2>
 2958b18:      	orb	%al, %r12b
 2958b1b:      	je	0x295be72 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3fb2>
 2958b21:      	movb	$0x0, 0x30(%rsp)
 2958b26:      	movb	$0x0, 0x70(%rsp)
 2958b2b:      	movq	0x60(%rsp), %rdx
 2958b30:      	movl	0x68(%rsp), %ecx
 2958b34:      	leaq	0x70(%rsp), %rax
 2958b39:      	leaq	0x30(%rsp), %r10
 2958b3e:      	movq	(%rsp), %rdi
 2958b42:      	movl	$0x30, %esi
 2958b47:      	movq	0x18(%rsp), %r8
 2958b4c:      	movl	0x28(%rsp), %r9d
 2958b51:      	pushq	%rax
 2958b52:      	pushq	%r10
 2958b54:      	pushq	0x240(%rsp)
 2958b5b:      	pushq	0x238(%rsp)
 2958b62:      	pushq	%r14
 2958b64:      	pushq	%rbx
 2958b65:      	callq	0x29755a0 <_ZL28lowerShuffleAsBlendOfPSHUFBsRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGERbSC_>
 2958b6a:      	addq	$0x30, %rsp
 2958b6e:      	movq	%rax, %rbx
 2958b71:      	movl	%edx, %r14d
 2958b74:      	cmpb	$0x1, 0x30(%rsp)
 2958b79:      	jne	0x295d801 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5941>
 2958b7f:      	cmpb	$0x0, 0x70(%rsp)
 2958b84:      	je	0x295d801 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5941>
 2958b8a:      	cmpl	$0x5, 0x148(%rbp)
 2958b91:      	jl	0x2958bf3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xd33>
 2958b93:      	movq	0x60(%rsp), %rdx
 2958b98:      	movl	0x68(%rsp), %ecx
 2958b9c:      	movdqu	0x130(%rsp), %xmm0
 2958ba5:      	subq	$0x30, %rsp
 2958ba9:      	movq	0x260(%rsp), %rax
 2958bb1:      	movq	%rax, 0x20(%rsp)
 2958bb6:      	movq	%rbp, 0x18(%rsp)
 2958bbb:      	movq	0x250(%rsp), %rax
 2958bc3:      	movq	%rax, 0x10(%rsp)
 2958bc8:      	movdqu	%xmm0, (%rsp)
 2958bcd:      	movq	0x30(%rsp), %rdi
 2958bd2:      	movl	$0x30, %esi
 2958bd7:      	movq	0x48(%rsp), %r8
 2958bdc:      	movl	0x58(%rsp), %r9d
 2958be1:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958be6:      	addq	$0x30, %rsp
 2958bea:      	testq	%rax, %rax
 2958bed:      	jne	0x295d7fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x593b>
 2958bf3:      	movq	0x60(%rsp), %rdx
 2958bf8:      	movl	0x68(%rsp), %ecx
 2958bfc:      	movdqu	0x130(%rsp), %xmm0
 2958c05:      	subq	$0x20, %rsp
 2958c09:      	movq	0x250(%rsp), %rax
 2958c11:      	movq	%rax, 0x10(%rsp)
 2958c16:      	movdqu	%xmm0, (%rsp)
 2958c1b:      	movq	0x20(%rsp), %rdi
 2958c20:      	movl	$0x30, %esi
 2958c25:      	movq	0x38(%rsp), %r8
 2958c2a:      	movl	0x48(%rsp), %r9d
 2958c2f:      	callq	0x296b3b0 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958c34:      	addq	$0x20, %rsp
 2958c38:      	testq	%rax, %rax
 2958c3b:      	jne	0x295d7fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x593b>
 2958c41:      	cmpb	$0x1, 0x1cf(%rbp)
 2958c48:      	jne	0x295c61a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x475a>
 2958c4e:      	movq	0x130(%rsp), %rdx
 2958c56:      	movq	0x138(%rsp), %rcx
 2958c5e:      	movq	0x60(%rsp), %r8
 2958c63:      	movl	0x68(%rsp), %r9d
 2958c68:      	subq	$0x20, %rsp
 2958c6c:      	leaq	0x230(%rsp), %rax
 2958c74:      	movdqu	(%rax), %xmm0
 2958c78:      	movdqu	%xmm0, (%rsp)
 2958c7d:      	movq	0x250(%rsp), %rax
 2958c85:      	movq	%rax, 0x18(%rsp)
 2958c8a:      	movq	%rbp, 0x10(%rsp)
 2958c8f:      	movq	0x20(%rsp), %rdi
 2958c94:      	movl	$0x30, %esi
 2958c99:      	callq	0x2981f60 <_ZL21lowerShuffleWithPERMVRKN4llvm5SDLocENS_3MVTENS_8ArrayRefIiEENS_7SDValueES6_RKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958c9e:      	addq	$0x20, %rsp
 2958ca2:      	jmp	0x295d7fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x593b>
 2958ca7:      	movq	%r14, %rax
 2958caa:      	movq	(%rdx), %r14
 2958cad:      	movl	0x8(%rdx), %r13d
 2958cb1:      	subq	$0x8, %rsp
 2958cb5:      	movl	$0x49, %esi
 2958cba:      	movq	%rbp, %rdx
 2958cbd:      	movl	%r11d, %ecx
 2958cc0:      	movq	%r14, %r8
 2958cc3:      	movl	%r13d, %r9d
 2958cc6:      	pushq	%r15
 2958cc8:      	pushq	%rax
 2958cc9:      	pushq	%r10
 2958ccb:      	pushq	%rbx
 2958ccc:      	pushq	%r12
 2958cce:      	movq	%rbp, %r15
 2958cd1:      	movl	%r11d, %ebp
 2958cd4:      	callq	0x296d980 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958cd9:      	addq	$0x30, %rsp
 2958cdd:      	testq	%rax, %rax
 2958ce0:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958ce6:      	movq	%r13, 0x18(%rsp)
 2958ceb:      	movq	0x228(%rsp), %rsi
 2958cf3:      	movq	%r14, 0x28(%rsp)
 2958cf8:      	movq	%r15, 0x10(%rsp)
 2958cfd:      	movl	%ebp, 0xc(%rsp)
 2958d01:      	leaq	(,%rbx,4), %r9
 2958d09:      	leaq	(%r12,%rbx,4), %rbp
 2958d0d:      	movq	%rbx, %r13
 2958d10:      	testq	%rbx, %rbx
 2958d13:      	je	0x2959aa7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1be7>
 2958d19:      	leaq	-0x4(%r9), %rdi
 2958d1d:      	xorl	%r15d, %r15d
 2958d20:      	movq	%r12, %r11
 2958d23:      	cmpq	$0x1c, %rdi
 2958d27:      	movl	0xc(%rsp), %ecx
 2958d2b:      	movq	0x220(%rsp), %r10
 2958d33:      	movq	%rsi, %r14
 2958d36:      	jb	0x2958dc0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf00>
 2958d3c:      	shrq	$0x2, %rdi
 2958d40:      	incq	%rdi
 2958d43:      	movq	%rdi, %rdx
 2958d46:      	andq	$-0x8, %rdx
 2958d4a:      	movq	%r11, %r8
 2958d4d:      	leaq	(%r11,%rdx,4), %r12
 2958d51:      	pxor	%xmm0, %xmm0
 2958d55:      	xorl	%esi, %esi
 2958d57:      	movdqa	-0x1b3d1bf(%rip), %xmm2 # 0xe1bba0 <.LCPI702_0>
 2958d5f:      	pxor	%xmm1, %xmm1
 2958d63:      	nopw	%cs:(%rax,%rax)
 2958d6d:      	nopl	(%rax)
 2958d70:      	movdqu	(%r8,%rsi,4), %xmm3
 2958d76:      	movdqu	0x10(%r8,%rsi,4), %xmm4
 2958d7d:      	pcmpgtd	%xmm2, %xmm3
 2958d81:      	psubd	%xmm3, %xmm1
 2958d85:      	pcmpgtd	%xmm2, %xmm4
 2958d89:      	psubd	%xmm4, %xmm0
 2958d8d:      	addq	$0x8, %rsi
 2958d91:      	cmpq	%rsi, %rdx
 2958d94:      	jne	0x2958d70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xeb0>
 2958d96:      	paddd	%xmm1, %xmm0
 2958d9a:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 2958d9f:      	paddd	%xmm0, %xmm1
 2958da3:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2958da8:      	paddd	%xmm1, %xmm0
 2958dac:      	movd	%xmm0, %r15d
 2958db1:      	cmpq	%rdx, %rdi
 2958db4:      	je	0x2958dd6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf16>
 2958db6:      	nopw	%cs:(%rax,%rax)
 2958dc0:      	xorl	%edx, %edx
 2958dc2:      	cmpl	$0x4, (%r12)
 2958dc7:      	setge	%dl
 2958dca:      	addl	%edx, %r15d
 2958dcd:      	addq	$0x4, %r12
 2958dd1:      	cmpq	%rbp, %r12
 2958dd4:      	jne	0x2958dc0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf00>
 2958dd6:      	cmpb	$0x0, 0x1f7(%r14)
 2958dde:      	movq	(%rsp), %rdi
 2958de2:      	je	0x2959c88 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1dc8>
 2958de8:      	movq	%r9, %rbx
 2958deb:      	movl	$0x49, %esi
 2958df0:      	movq	0x10(%rsp), %rdx
 2958df5:      	movq	0x28(%rsp), %r8
 2958dfa:      	movq	0x18(%rsp), %r9
 2958dff:      	pushq	$0x1
 2958e01:      	pushq	0x238(%rsp)
 2958e08:      	pushq	%r14
 2958e0a:      	pushq	%r10
 2958e0c:      	pushq	%r13
 2958e0e:      	movq	%r11, %r12
 2958e11:      	pushq	%r11
 2958e13:      	movq	%r13, %r14
 2958e16:      	movl	%ecx, %r13d
 2958e19:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2958e1e:      	addq	$0x30, %rsp
 2958e22:      	testq	%rax, %rax
 2958e25:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958e2b:      	testl	%r15d, %r15d
 2958e2e:      	movq	(%rsp), %rdi
 2958e32:      	movl	%r13d, %ecx
 2958e35:      	movq	0x220(%rsp), %r10
 2958e3d:      	movq	%r14, %r13
 2958e40:      	movq	0x228(%rsp), %r14
 2958e48:      	jne	0x2959c94 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1dd4>
 2958e4e:      	jmp	0x2959b09 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c49>
 2958e53:      	movdqu	(%rdx), %xmm0
 2958e57:      	movdqa	%xmm0, 0x80(%rsp)
 2958e60:      	movq	0x80(%rsp), %r15
 2958e68:      	movl	0x18(%r15), %eax
 2958e6c:      	addl	$-0x35, %eax
 2958e6f:      	cmpl	$0x1, %eax
 2958e72:      	ja	0x29591c5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1305>
 2958e78:      	movl	0x88(%rsp), %r9d
 2958e80:      	movq	%rdi, %r13
 2958e83:      	movl	$0x5e, %esi
 2958e88:      	movq	%rbp, %rdx
 2958e8b:      	movl	%r11d, %ecx
 2958e8e:      	movq	%r15, %r8
 2958e91:      	movq	0x230(%rsp), %r15
 2958e99:      	pushq	%r15
 2958e9b:      	pushq	%r14
 2958e9d:      	pushq	%rbx
 2958e9e:      	pushq	%r12
 2958ea0:      	movq	%r12, %rbx
 2958ea3:      	movq	%rbp, %r12
 2958ea6:      	movl	%r11d, %ebp
 2958ea9:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958eae:      	addq	$0x20, %rsp
 2958eb2:      	testq	%rax, %rax
 2958eb5:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958ebb:      	movq	%rbx, %r14
 2958ebe:      	movq	%r13, (%rsp)
 2958ec2:      	movq	0x30(%r12), %rax
 2958ec7:      	movl	%ebp, %ecx
 2958ec9:      	shlq	$0x4, %rcx
 2958ecd:      	cmpw	$0x49, (%rax,%rcx)
 2958ed2:      	movl	%ebp, %r13d
 2958ed5:      	jne	0x295a6c5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2805>
 2958edb:      	movq	%r12, %rbp
 2958ede:      	jmp	0x295aed5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3015>
 2958ee3:      	movq	(%rdx), %r15
 2958ee6:      	movl	0x8(%rdx), %r9d
 2958eea:      	movl	0x18(%r15), %eax
 2958eee:      	addl	$-0x35, %eax
 2958ef1:      	cmpl	$0x1, %eax
 2958ef4:      	ja	0x29594c0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1600>
 2958efa:      	movq	%rdi, %r13
 2958efd:      	movl	$0x96, %esi
 2958f02:      	movq	%rbp, %rdx
 2958f05:      	movl	%r11d, %ecx
 2958f08:      	movq	%r15, %r8
 2958f0b:      	movq	0x230(%rsp), %r15
 2958f13:      	pushq	%r15
 2958f15:      	pushq	%r14
 2958f17:      	pushq	%rbx
 2958f18:      	pushq	%r12
 2958f1a:      	movq	%r12, %rbx
 2958f1d:      	movq	%rbp, %r12
 2958f20:      	movl	%r11d, %ebp
 2958f23:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958f28:      	addq	$0x20, %rsp
 2958f2c:      	testq	%rax, %rax
 2958f2f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2958f35:      	movq	%r12, 0x10(%rsp)
 2958f3a:      	movl	(%rbx), %ecx
 2958f3c:      	movl	0x4(%rbx), %eax
 2958f3f:      	xorl	%edx, %edx
 2958f41:      	cmpl	$0x1, %ecx
 2958f44:      	sete	%dl
 2958f47:      	xorl	%esi, %esi
 2958f49:      	cmpl	$0x1, %eax
 2958f4c:      	sete	%sil
 2958f50:      	movq	%r14, %rdi
 2958f53:      	leal	(%rdx,%rsi,2), %r14d
 2958f57:      	cmpl	$0x7, 0x148(%rdi)
 2958f5e:      	jl	0x295a706 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2846>
 2958f64:      	movl	%r14d, %esi
 2958f67:      	subq	$0x8, %rsp
 2958f6b:      	xorl	%ebx, %ebx
 2958f6d:      	movq	%r15, %rdi
 2958f70:      	movq	%r13, %rdx
 2958f73:      	movl	$0x5, %ecx
 2958f78:      	xorl	%r8d, %r8d
 2958f7b:      	movl	$0x1, %r9d
 2958f81:      	pushq	$0x0
 2958f83:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 2958f88:      	addq	$0x10, %rsp
 2958f8c:      	movq	%rax, 0xa0(%rsp)
 2958f94:      	movl	%edx, 0xa8(%rsp)
 2958f9b:      	movq	0x10(%rsp), %rax
 2958fa0:      	movq	%rax, 0x30(%rsp)
 2958fa5:      	movl	%ebp, 0x38(%rsp)
 2958fa9:      	movq	0x3b0(%r15), %rax
 2958fb0:      	testq	%rax, %rax
 2958fb3:      	je	0x2958fb8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x10f8>
 2958fb5:      	movl	0x8(%rax), %ebx
 2958fb8:      	subq	$0x20, %rsp
 2958fbc:      	movups	0xc0(%rsp), %xmm0
 2958fc4:      	movups	%xmm0, 0x10(%rsp)
 2958fc9:      	movdqu	0x50(%rsp), %xmm0
 2958fcf:      	movdqu	%xmm0, (%rsp)
 2958fd4:      	movq	%r15, %rdi
 2958fd7:      	movl	$0x2cb, %esi            # imm = 0x2CB
 2958fdc:      	movq	%r13, %rdx
 2958fdf:      	movl	$0x96, %ecx
 2958fe4:      	jmp	0x2959c61 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da1>
 2958fe9:      	movq	0x30(%rbp), %rax
 2958fed:      	movl	%r11d, %ecx
 2958ff0:      	shlq	$0x4, %rcx
 2958ff4:      	cmpw	$0x3e, (%rax,%rcx)
 2958ff9:      	movq	%rdi, (%rsp)
 2958ffd:      	jne	0x2959806 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1946>
 2959003:      	movq	%rbx, %r13
 2959006:      	jmp	0x295a03f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x217f>
 295900b:      	movdqu	(%rdx), %xmm0
 295900f:      	movdqa	%xmm0, 0x60(%rsp)
 2959015:      	cmpl	$0x5, 0x148(%r14)
 295901d:      	jl	0x295907c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x11bc>
 295901f:      	movq	0x60(%rsp), %r8
 2959024:      	movl	0x68(%rsp), %r9d
 2959029:      	subq	$0x8, %rsp
 295902d:      	movq	%r15, %rax
 2959030:      	movq	%rbx, %r15
 2959033:      	movq	%rdi, %rbx
 2959036:      	movl	$0x84, %esi
 295903b:      	movq	%rbp, %rdx
 295903e:      	movl	%r11d, %ecx
 2959041:      	pushq	%rax
 2959042:      	pushq	%r14
 2959044:      	pushq	%r10
 2959046:      	pushq	%r15
 2959048:      	pushq	%r12
 295904a:      	movq	%rbp, %r14
 295904d:      	movl	%r11d, %ebp
 2959050:      	movq	%r10, %r13
 2959053:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959058:      	movq	%r13, %r10
 295905b:      	movl	%ebp, %r11d
 295905e:      	movq	%r14, %rbp
 2959061:      	movq	0x258(%rsp), %r14
 2959069:      	movq	%rbx, %rdi
 295906c:      	movq	%r15, %rbx
 295906f:      	addq	$0x30, %rsp
 2959073:      	testq	%rax, %rax
 2959076:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295907c:      	testq	%rbx, %rbx
 295907f:      	je	0x295984f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x198f>
 2959085:      	leaq	(,%rbx,4), %rcx
 295908d:      	addq	$-0x4, %rcx
 2959091:      	xorl	%r15d, %r15d
 2959094:      	movq	%r12, %rax
 2959097:      	cmpq	$0x1c, %rcx
 295909b:      	jb	0x2959116 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1256>
 295909d:      	shrq	$0x2, %rcx
 29590a1:      	incq	%rcx
 29590a4:      	movq	%rcx, %rdx
 29590a7:      	andq	$-0x8, %rdx
 29590ab:      	leaq	(%r12,%rdx,4), %rax
 29590af:      	pxor	%xmm0, %xmm0
 29590b3:      	xorl	%esi, %esi
 29590b5:      	movdqa	-0x1b3d51d(%rip), %xmm2 # 0xe1bba0 <.LCPI702_0>
 29590bd:      	pxor	%xmm1, %xmm1
 29590c1:      	nopw	%cs:(%rax,%rax)
 29590cb:      	nopl	(%rax,%rax)
 29590d0:      	movdqu	(%r12,%rsi,4), %xmm3
 29590d6:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 29590dd:      	pcmpgtd	%xmm2, %xmm3
 29590e1:      	psubd	%xmm3, %xmm1
 29590e5:      	pcmpgtd	%xmm2, %xmm4
 29590e9:      	psubd	%xmm4, %xmm0
 29590ed:      	addq	$0x8, %rsi
 29590f1:      	cmpq	%rsi, %rdx
 29590f4:      	jne	0x29590d0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1210>
 29590f6:      	paddd	%xmm1, %xmm0
 29590fa:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 29590ff:      	paddd	%xmm0, %xmm1
 2959103:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2959108:      	paddd	%xmm1, %xmm0
 295910c:      	movd	%xmm0, %r15d
 2959111:      	cmpq	%rdx, %rcx
 2959114:      	je	0x2959134 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1274>
 2959116:      	leaq	(%r12,%rbx,4), %rcx
 295911a:      	nopw	(%rax,%rax)
 2959120:      	xorl	%edx, %edx
 2959122:      	cmpl	$0x4, (%rax)
 2959125:      	setge	%dl
 2959128:      	addl	%edx, %r15d
 295912b:      	addq	$0x4, %rax
 295912f:      	cmpq	%rcx, %rax
 2959132:      	jne	0x2959120 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1260>
 2959134:      	testl	%r15d, %r15d
 2959137:      	je	0x295984f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x198f>
 295913d:      	movq	%rbx, 0x20(%rsp)
 2959142:      	cmpl	$0x2, 0x148(%r14)
 295914a:      	jl	0x295a905 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2a45>
 2959150:      	movq	0x60(%rsp), %r13
 2959155:      	movl	0x68(%rsp), %ebx
 2959159:      	subq	$0x8, %rsp
 295915d:      	movq	%rdi, 0x8(%rsp)
 2959162:      	movl	$0x49, %esi
 2959167:      	movq	%rbp, %rdx
 295916a:      	movl	%r11d, %ecx
 295916d:      	movq	%r13, %r8
 2959170:      	movl	%ebx, %r9d
 2959173:      	movq	0x238(%rsp), %rax
 295917b:      	pushq	%rax
 295917c:      	pushq	%r14
 295917e:      	pushq	%r10
 2959180:      	pushq	0x40(%rsp)
 2959184:      	pushq	%r12
 2959186:      	movq	%r12, 0x88(%rsp)
 295918e:      	movq	%rbp, %r12
 2959191:      	movl	%r11d, %ebp
 2959194:      	callq	0x296d980 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959199:      	addq	$0x30, %rsp
 295919d:      	testq	%rax, %rax
 29591a0:      	je	0x295a8a7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29e7>
 29591a6:      	movl	%edx, %r8d
 29591a9:      	movq	0x230(%rsp), %rdi
 29591b1:      	movl	$0x84, %esi
 29591b6:      	xorl	%edx, %edx
 29591b8:      	movq	%rax, %rcx
 29591bb:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 29591c0:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29591c5:      	movq	%rbx, 0x20(%rsp)
 29591ca:      	cmpl	$0x8, 0x148(%r14)
 29591d2:      	movl	0x88(%rsp), %r13d
 29591da:      	jl	0x295922a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x136a>
 29591dc:      	movq	%rdi, %rbx
 29591df:      	movq	%rbp, %rsi
 29591e2:      	movl	%r11d, %edx
 29591e5:      	movq	%r15, %rcx
 29591e8:      	movl	%r13d, %r8d
 29591eb:      	movq	%r12, %r9
 29591ee:      	pushq	0x230(%rsp)
 29591f5:      	pushq	0x28(%rsp)
 29591f9:      	movq	%rbp, %r14
 29591fc:      	movl	%r11d, %ebp
 29591ff:      	callq	0x2962b20 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959204:      	movq	0x230(%rsp), %r10
 295920c:      	movl	%ebp, %r11d
 295920f:      	movq	%r14, %rbp
 2959212:      	movq	0x238(%rsp), %r14
 295921a:      	movq	%rbx, %rdi
 295921d:      	addq	$0x10, %rsp
 2959221:      	testq	%rax, %rax
 2959224:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295922a:      	movl	%r11d, 0xc(%rsp)
 295922f:      	movq	%rbp, 0x10(%rsp)
 2959234:      	movq	%rdi, (%rsp)
 2959238:      	movl	$0x5e, %esi
 295923d:      	movq	%rbp, %rdx
 2959240:      	movl	%r11d, %ecx
 2959243:      	movq	%r15, %r8
 2959246:      	movl	%r13d, %r9d
 2959249:      	pushq	$0x0
 295924b:      	movq	0x238(%rsp), %rbp
 2959253:      	movq	%r12, %rbx
 2959256:      	pushq	%rbp
 2959257:      	pushq	%r14
 2959259:      	pushq	%r10
 295925b:      	movl	%r13d, %r12d
 295925e:      	movq	0x40(%rsp), %r13
 2959263:      	pushq	%r13
 2959265:      	pushq	%rbx
 2959266:      	movq	%r10, %rbp
 2959269:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 295926e:      	addq	$0x30, %rsp
 2959272:      	testq	%rax, %rax
 2959275:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295927b:      	movl	0x8(%rbp), %eax
 295927e:      	movq	(%rsp), %rdi
 2959282:      	movl	$0x5e, %esi
 2959287:      	movq	0x10(%rsp), %rdx
 295928c:      	movl	0xc(%rsp), %ecx
 2959290:      	movq	%r15, %r8
 2959293:      	movl	%r12d, %r9d
 2959296:      	pushq	0x230(%rsp)
 295929d:      	pushq	%r14
 295929f:      	pushq	%rax
 29592a0:      	pushq	(%rbp)
 29592a3:      	pushq	%r13
 29592a5:      	pushq	%rbx
 29592a6:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29592ab:      	addq	$0x30, %rsp
 29592af:      	testq	%rax, %rax
 29592b2:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29592b8:      	movabsq	$0x200000002, %rax      # imm = 0x200000002
 29592c2:      	xorq	(%rbx), %rax
 29592c5:      	movq	%rax, 0x30(%rsp)
 29592ca:      	movl	0x8(%rbp), %eax
 29592cd:      	leaq	0x30(%rsp), %r10
 29592d2:      	movq	(%rsp), %rdi
 29592d6:      	movl	$0x5e, %esi
 29592db:      	movq	%r15, %rdx
 29592de:      	movl	%r12d, %ecx
 29592e1:      	movq	0x10(%rsp), %r8
 29592e6:      	movl	0xc(%rsp), %r9d
 29592eb:      	pushq	0x230(%rsp)
 29592f2:      	pushq	%r14
 29592f4:      	pushq	%rax
 29592f5:      	pushq	(%rbp)
 29592f8:      	pushq	$0x2
 29592fa:      	pushq	%r10
 29592fc:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959301:      	addq	$0x30, %rsp
 2959305:      	testq	%rax, %rax
 2959308:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295930e:      	movl	%r12d, 0x18(%rsp)
 2959313:      	movq	0x10(%rsp), %r12
 2959318:      	movl	0xc(%rsp), %ebp
 295931c:      	movl	0x148(%r14), %eax
 2959323:      	movl	%eax, 0x28(%rsp)
 2959327:      	cmpl	$0x5, %eax
 295932a:      	movq	%rbx, %r13
 295932d:      	movq	0x20(%rsp), %rbx
 2959332:      	jl	0x2959374 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x14b4>
 2959334:      	subq	$0x8, %rsp
 2959338:      	movq	0x8(%rsp), %rdi
 295933d:      	movl	$0x5e, %esi
 2959342:      	movq	%r12, %rdx
 2959345:      	movl	%ebp, %ecx
 2959347:      	movq	%r15, %r8
 295934a:      	movl	0x20(%rsp), %r9d
 295934f:      	pushq	0x238(%rsp)
 2959356:      	pushq	%r14
 2959358:      	pushq	0x238(%rsp)
 295935f:      	pushq	%rbx
 2959360:      	pushq	%r13
 2959362:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959367:      	addq	$0x30, %rsp
 295936b:      	testq	%rax, %rax
 295936e:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959374:      	subq	$0x8, %rsp
 2959378:      	movq	0x8(%rsp), %rdi
 295937d:      	movl	$0x5e, %esi
 2959382:      	movq	%r12, %rdx
 2959385:      	movl	%ebp, %ecx
 2959387:      	movq	%r15, %r8
 295938a:      	movl	0x20(%rsp), %r9d
 295938f:      	pushq	0x238(%rsp)
 2959396:      	pushq	%rbx
 2959397:      	pushq	%r13
 2959399:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295939e:      	addq	$0x20, %rsp
 29593a2:      	testq	%rax, %rax
 29593a5:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29593ab:      	movq	%r13, 0x58(%rsp)
 29593b0:      	movl	0x148(%r14), %eax
 29593b7:      	cmpl	$0x4, %eax
 29593ba:      	jl	0x295944a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x158a>
 29593c0:      	cmpb	$0x1, 0x1d1(%r14)
 29593c8:      	movq	(%rsp), %rdi
 29593cc:      	movl	%ebp, %ecx
 29593ce:      	movq	0x58(%rsp), %r10
 29593d3:      	jne	0x295941c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x155c>
 29593d5:      	subq	$0x8, %rsp
 29593d9:      	movl	$0x5e, %esi
 29593de:      	movq	%r12, %rdx
 29593e1:      	movq	%r15, %r8
 29593e4:      	movl	0x20(%rsp), %r9d
 29593e9:      	pushq	0x238(%rsp)
 29593f0:      	pushq	%rax
 29593f1:      	pushq	0x238(%rsp)
 29593f8:      	pushq	%rbx
 29593f9:      	pushq	%r10
 29593fb:      	callq	0x2965b20 <_ZL20lowerShuffleAsVALIGNRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959400:      	movq	0x88(%rsp), %r10
 2959408:      	movl	%ebp, %ecx
 295940a:      	movq	0x30(%rsp), %rdi
 295940f:      	addq	$0x30, %rsp
 2959413:      	testq	%rax, %rax
 2959416:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295941c:      	movl	$0x5e, %esi
 2959421:      	movq	%r12, %rdx
 2959424:      	movq	%r15, %r8
 2959427:      	movl	0x18(%rsp), %r9d
 295942c:      	pushq	0x230(%rsp)
 2959433:      	pushq	%r14
 2959435:      	pushq	%rbx
 2959436:      	pushq	%r10
 2959438:      	callq	0x2966130 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295943d:      	addq	$0x20, %rsp
 2959441:      	testq	%rax, %rax
 2959444:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295944a:      	cmpl	$0x5, 0x28(%rsp)
 295944f:      	jl	0x295bcfd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e3d>
 2959455:      	movq	0x58(%rsp), %rax
 295945a:      	movq	%rax, 0xa0(%rsp)
 2959462:      	movq	%rbx, 0xa8(%rsp)
 295946a:      	subq	$0x30, %rsp
 295946e:      	movdqu	0xd0(%rsp), %xmm0
 2959477:      	movdqu	%xmm0, (%rsp)
 295947c:      	movq	0x260(%rsp), %rax
 2959484:      	movq	%rax, 0x20(%rsp)
 2959489:      	movq	%r14, 0x18(%rsp)
 295948e:      	movq	0x250(%rsp), %rax
 2959496:      	movq	%rax, 0x10(%rsp)
 295949b:      	movq	0x30(%rsp), %rdi
 29594a0:      	movl	$0x5e, %esi
 29594a5:      	movq	%r12, %rdx
 29594a8:      	movl	%ebp, %ecx
 29594aa:      	movq	%r15, %r8
 29594ad:      	movl	0x48(%rsp), %r9d
 29594b2:      	callq	0x2966780 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29594b7:      	addq	$0x30, %rsp
 29594bb:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29594c0:      	cmpl	$0x8, 0x148(%r14)
 29594c8:      	movq	%rdi, (%rsp)
 29594cc:      	jl	0x295952b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x166b>
 29594ce:      	movq	%rbx, %r13
 29594d1:      	movq	%rbp, %rsi
 29594d4:      	movl	%r11d, %edx
 29594d7:      	movq	%r15, %rcx
 29594da:      	movl	%r9d, %r8d
 29594dd:      	movq	%r15, %rbx
 29594e0:      	movl	%r9d, %r15d
 29594e3:      	movq	%r12, %r9
 29594e6:      	pushq	0x230(%rsp)
 29594ed:      	pushq	%r13
 29594ef:      	movq	%rbp, %r14
 29594f2:      	movl	%r11d, %ebp
 29594f5:      	callq	0x2962b20 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 29594fa:      	movl	%r15d, %r9d
 29594fd:      	movq	%rbx, %r15
 2959500:      	movq	0x230(%rsp), %r10
 2959508:      	movl	%ebp, %r11d
 295950b:      	movq	%r14, %rbp
 295950e:      	movq	0x238(%rsp), %r14
 2959516:      	movq	0x10(%rsp), %rdi
 295951b:      	movq	%r13, %rbx
 295951e:      	addq	$0x10, %rsp
 2959522:      	testq	%rax, %rax
 2959525:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295952b:      	movq	%rbp, 0x10(%rsp)
 2959530:      	movl	0x8(%r10), %eax
 2959534:      	movl	$0x96, %esi
 2959539:      	movq	%rbp, %rdx
 295953c:      	movl	%r11d, %ecx
 295953f:      	movq	%r15, %r8
 2959542:      	movl	%r9d, 0x18(%rsp)
 2959547:      	movq	%r10, %r13
 295954a:      	movq	0x230(%rsp), %r10
 2959552:      	pushq	%r10
 2959554:      	pushq	%r14
 2959556:      	pushq	%rax
 2959557:      	pushq	(%r13)
 295955b:      	pushq	%rbx
 295955c:      	pushq	%r12
 295955e:      	movl	%r11d, %ebp
 2959561:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959566:      	addq	$0x30, %rsp
 295956a:      	testq	%rax, %rax
 295956d:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959573:      	movq	(%r12), %xmm0
 2959579:      	movdqa	-0x1b46541(%rip), %xmm1 # 0xe13040 <.LCPI91_1>
 2959581:      	pxor	%xmm0, %xmm1
 2959585:      	pcmpeqd	%xmm2, %xmm2
 2959589:      	pcmpgtd	%xmm2, %xmm0
 295958d:      	pxor	%xmm2, %xmm0
 2959591:      	por	%xmm1, %xmm0
 2959595:      	movq	%xmm0, 0x70(%rsp)
 295959b:      	movl	0x8(%r13), %eax
 295959f:      	leaq	0x70(%rsp), %r10
 29595a4:      	movq	(%rsp), %rdi
 29595a8:      	movl	$0x96, %esi
 29595ad:      	movq	%r15, %rdx
 29595b0:      	movl	0x18(%rsp), %ecx
 29595b4:      	movq	0x10(%rsp), %r8
 29595b9:      	movl	%ebp, %r9d
 29595bc:      	pushq	0x230(%rsp)
 29595c3:      	pushq	%r14
 29595c5:      	pushq	%rax
 29595c6:      	pushq	(%r13)
 29595ca:      	pushq	$0x2
 29595cc:      	pushq	%r10
 29595ce:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29595d3:      	addq	$0x30, %rsp
 29595d7:      	testq	%rax, %rax
 29595da:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 29595e0:      	movl	%ebp, 0xc(%rsp)
 29595e4:      	cmpq	$0x2, %rbx
 29595e8:      	movq	0x10(%rsp), %rbp
 29595ed:      	jne	0x295ad3f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e7f>
 29595f3:      	movl	(%r12), %eax
 29595f7:      	testl	%eax, %eax
 29595f9:      	jle	0x2959637 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1777>
 29595fb:      	xorl	%ecx, %ecx
 29595fd:      	cmpl	$0x1, %eax
 2959600:      	sete	%cl
 2959603:      	movq	%r15, %rsi
 2959606:      	cmoveq	%rbp, %rsi
 295960a:      	movl	0x18(%rsp), %edx
 295960e:      	movl	0xc(%rsp), %r8d
 2959613:      	cmovel	%r8d, %edx
 2959617:      	leal	-0x2(%rax,%rcx,2), %r9d
 295961c:      	subq	$0x8, %rsp
 2959620:      	movl	$0x2, %edi
 2959625:      	movq	%rbp, %rcx
 2959628:      	pushq	$0x0
 295962a:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295962f:      	addq	$0x10, %rsp
 2959633:      	testb	%al, %al
 2959635:      	je	0x295968f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x17cf>
 2959637:      	movl	0x4(%r12), %eax
 295963c:      	testl	%eax, %eax
 295963e:      	sets	%cl
 2959641:      	cmpl	$0x3, %eax
 2959644:      	sete	%dl
 2959647:      	orb	%cl, %dl
 2959649:      	jne	0x2959736 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1876>
 295964f:      	xorl	%ecx, %ecx
 2959651:      	cmpl	$0x2, %eax
 2959654:      	setb	%cl
 2959657:      	movq	%r15, %rsi
 295965a:      	cmovbq	%rbp, %rsi
 295965e:      	movl	0x18(%rsp), %r8d
 2959663:      	movl	%r8d, %edx
 2959666:      	cmovbl	0xc(%rsp), %edx
 295966b:      	leal	-0x2(%rax,%rcx,2), %r9d
 2959670:      	subq	$0x8, %rsp
 2959674:      	movl	$0x2, %edi
 2959679:      	movq	%r15, %rcx
 295967c:      	pushq	$0x1
 295967e:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959683:      	addq	$0x10, %rsp
 2959687:      	testb	%al, %al
 2959689:      	jne	0x2959736 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1876>
 295968f:      	movl	(%r12), %eax
 2959693:      	testl	%eax, %eax
 2959695:      	sets	%cl
 2959698:      	cmpl	$0x1, %eax
 295969b:      	sete	%dl
 295969e:      	orb	%cl, %dl
 29596a0:      	jne	0x29596e2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1822>
 29596a2:      	xorl	%ecx, %ecx
 29596a4:      	cmpl	$0x2, %eax
 29596a7:      	setb	%cl
 29596aa:      	movq	%r15, %rsi
 29596ad:      	cmovbq	%rbp, %rsi
 29596b1:      	movl	0x18(%rsp), %edx
 29596b5:      	movl	0xc(%rsp), %r8d
 29596ba:      	cmovbl	%r8d, %edx
 29596be:      	leal	-0x2(%rax,%rcx,2), %r9d
 29596c3:      	subq	$0x8, %rsp
 29596c7:      	movl	$0x2, %edi
 29596cc:      	movq	%rbp, %rcx
 29596cf:      	pushq	$0x1
 29596d1:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 29596d6:      	addq	$0x10, %rsp
 29596da:      	testb	%al, %al
 29596dc:      	je	0x295ad3f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e7f>
 29596e2:      	movl	0x4(%r12), %eax
 29596e7:      	testl	%eax, %eax
 29596e9:      	sets	%cl
 29596ec:      	cmpl	$0x3, %eax
 29596ef:      	sete	%dl
 29596f2:      	orb	%cl, %dl
 29596f4:      	jne	0x2959736 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1876>
 29596f6:      	xorl	%ecx, %ecx
 29596f8:      	cmpl	$0x2, %eax
 29596fb:      	setb	%cl
 29596fe:      	movq	%r15, %rsi
 2959701:      	cmovbq	%rbp, %rsi
 2959705:      	movl	0x18(%rsp), %r8d
 295970a:      	movl	%r8d, %edx
 295970d:      	cmovbl	0xc(%rsp), %edx
 2959712:      	leal	-0x2(%rax,%rcx,2), %r9d
 2959717:      	subq	$0x8, %rsp
 295971b:      	movl	$0x2, %edi
 2959720:      	movq	%r15, %rcx
 2959723:      	pushq	$0x1
 2959725:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295972a:      	addq	$0x10, %rsp
 295972e:      	testb	%al, %al
 2959730:      	je	0x295ad3f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e7f>
 2959736:      	movl	(%r12), %edx
 295973a:      	movq	%rbp, %rdi
 295973d:      	movl	0xc(%rsp), %esi
 2959741:      	movq	0x230(%rsp), %rcx
 2959749:      	callq	0x2968fa0 <_ZL30getScalarValueForVectorElementN4llvm7SDValueEiRNS_12SelectionDAGE>
 295974e:      	testq	%rax, %rax
 2959751:      	je	0x295ad3f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e7f>
 2959757:      	movq	%rax, 0xa0(%rsp)
 295975f:      	movl	%edx, 0xa8(%rsp)
 2959766:      	movq	0x230(%rsp), %r14
 295976e:      	movq	0x3b0(%r14), %rax
 2959775:      	xorl	%ebx, %ebx
 2959777:      	movl	$0x0, %r9d
 295977d:      	testq	%rax, %rax
 2959780:      	je	0x2959786 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x18c6>
 2959782:      	movl	0x8(%rax), %r9d
 2959786:      	subq	$0x10, %rsp
 295978a:      	movups	0xb0(%rsp), %xmm0
 2959792:      	movups	%xmm0, (%rsp)
 2959796:      	movq	%r14, %rdi
 2959799:      	movl	$0xac, %esi
 295979e:      	movq	0x10(%rsp), %rdx
 29597a3:      	movl	$0x96, %ecx
 29597a8:      	xorl	%r8d, %r8d
 29597ab:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 29597b0:      	addq	$0x10, %rsp
 29597b4:      	movq	%rax, 0xa0(%rsp)
 29597bc:      	movl	%edx, 0xa8(%rsp)
 29597c3:      	movq	0x3b0(%r14), %rax
 29597ca:      	testq	%rax, %rax
 29597cd:      	je	0x29597d2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1912>
 29597cf:      	movl	0x8(%rax), %ebx
 29597d2:      	subq	$0x20, %rsp
 29597d6:      	movups	0xc0(%rsp), %xmm0
 29597de:      	movups	%xmm0, 0x10(%rsp)
 29597e3:      	leaq	0x230(%rsp), %rax
 29597eb:      	movdqu	(%rax), %xmm0
 29597ef:      	movdqu	%xmm0, (%rsp)
 29597f4:      	movq	%r14, %rdi
 29597f7:      	movl	$0x2c5, %esi            # imm = 0x2C5
 29597fc:      	movq	0x20(%rsp), %rdx
 2959801:      	jmp	0x2958fdf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x111f>
 2959806:      	movq	0x48(%rbp), %rsi
 295980a:      	movq	%rsi, 0x30(%rsp)
 295980f:      	testq	%rsi, %rsi
 2959812:      	je	0x295982f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x196f>
 2959814:      	leaq	0x30(%rsp), %rdi
 2959819:      	movl	$0x1, %edx
 295981e:      	movq	%rbx, %r14
 2959821:      	movl	%r11d, %ebx
 2959824:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2959829:      	movl	%ebx, %r11d
 295982c:      	movq	%r14, %rbx
 295982f:      	movl	0x44(%rbp), %eax
 2959832:      	movl	%eax, 0x38(%rsp)
 2959836:      	movq	0x3b0(%r15), %rax
 295983d:      	testq	%rax, %rax
 2959840:      	je	0x2959fd3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2113>
 2959846:      	movl	0x8(%rax), %r9d
 295984a:      	jmp	0x2959fd6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2116>
 295984f:      	movq	%rdi, (%rsp)
 2959853:      	movq	0x60(%rsp), %r8
 2959858:      	movl	0x68(%rsp), %r13d
 295985d:      	movl	$0x84, %esi
 2959862:      	movq	%rbp, %rdx
 2959865:      	movl	%r11d, %ecx
 2959868:      	movq	%r8, 0x18(%rsp)
 295986d:      	movl	%r13d, %r9d
 2959870:      	movq	0x230(%rsp), %r15
 2959878:      	pushq	%r15
 295987a:      	pushq	%r14
 295987c:      	pushq	%rbx
 295987d:      	pushq	%r12
 295987f:      	movq	%rbx, %r15
 2959882:      	movq	%r12, %rbx
 2959885:      	movq	%rbp, %r12
 2959888:      	movl	%r11d, %ebp
 295988b:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959890:      	addq	$0x20, %rsp
 2959894:      	testq	%rax, %rax
 2959897:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295989d:      	movq	%r13, 0x28(%rsp)
 29598a2:      	movq	0x18(%rsp), %r13
 29598a7:      	movq	%r15, 0x20(%rsp)
 29598ac:      	movq	%r14, %rax
 29598af:      	movq	%rbx, %r14
 29598b2:      	movl	%ebp, %ebx
 29598b4:      	movq	%rax, %r15
 29598b7:      	movl	0x148(%rax), %eax
 29598bd:      	cmpl	$0x3, %eax
 29598c0:      	jl	0x295a89c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29dc>
 29598c6:      	cmpq	$0x4, 0x20(%rsp)
 29598cc:      	movl	%ebx, %r8d
 29598cf:      	movq	%r13, %rbp
 29598d2:      	jne	0x295b57c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36bc>
 29598d8:      	movl	(%r14), %eax
 29598db:      	testl	%eax, %eax
 29598dd:      	movq	%r12, %r13
 29598e0:      	jle	0x2959921 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1a61>
 29598e2:      	xorl	%ecx, %ecx
 29598e4:      	cmpl	$0x4, %eax
 29598e7:      	setb	%cl
 29598ea:      	movq	%rbp, %rsi
 29598ed:      	cmovbq	%r13, %rsi
 29598f1:      	movq	0x28(%rsp), %rdx
 29598f6:      	cmovbl	%r8d, %edx
 29598fa:      	leal	-0x4(%rax,%rcx,4), %r9d
 29598ff:      	subq	$0x8, %rsp
 2959903:      	movl	$0x4, %edi
 2959908:      	movq	%r13, %rcx
 295990b:      	pushq	$0x0
 295990d:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959912:      	movl	%ebx, %r8d
 2959915:      	addq	$0x10, %rsp
 2959919:      	testb	%al, %al
 295991b:      	je	0x295b096 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31d6>
 2959921:      	movl	0x4(%r14), %eax
 2959925:      	testl	%eax, %eax
 2959927:      	jle	0x2959968 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1aa8>
 2959929:      	xorl	%ecx, %ecx
 295992b:      	cmpl	$0x4, %eax
 295992e:      	setb	%cl
 2959931:      	movq	%rbp, %rsi
 2959934:      	cmovbq	%r13, %rsi
 2959938:      	movq	0x28(%rsp), %rdx
 295993d:      	cmovbl	%r8d, %edx
 2959941:      	leal	-0x4(%rax,%rcx,4), %r9d
 2959946:      	subq	$0x8, %rsp
 295994a:      	movl	$0x4, %edi
 295994f:      	movq	%r13, %rcx
 2959952:      	pushq	$0x0
 2959954:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959959:      	movl	%ebx, %r8d
 295995c:      	addq	$0x10, %rsp
 2959960:      	testb	%al, %al
 2959962:      	je	0x295b096 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31d6>
 2959968:      	movl	0x8(%r14), %eax
 295996c:      	testl	%eax, %eax
 295996e:      	sets	%cl
 2959971:      	cmpl	$0x2, %eax
 2959974:      	sete	%dl
 2959977:      	orb	%cl, %dl
 2959979:      	jne	0x29599ba <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1afa>
 295997b:      	xorl	%ecx, %ecx
 295997d:      	cmpl	$0x4, %eax
 2959980:      	setb	%cl
 2959983:      	movq	%rbp, %rsi
 2959986:      	cmovbq	%r13, %rsi
 295998a:      	movq	0x28(%rsp), %rdx
 295998f:      	cmovbl	%r8d, %edx
 2959993:      	leal	-0x4(%rax,%rcx,4), %r9d
 2959998:      	subq	$0x8, %rsp
 295999c:      	movl	$0x4, %edi
 29599a1:      	movq	%r13, %rcx
 29599a4:      	pushq	$0x2
 29599a6:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 29599ab:      	movl	%ebx, %r8d
 29599ae:      	addq	$0x10, %rsp
 29599b2:      	testb	%al, %al
 29599b4:      	je	0x295b096 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31d6>
 29599ba:      	movl	0xc(%r14), %eax
 29599be:      	testl	%eax, %eax
 29599c0:      	sets	%cl
 29599c3:      	cmpl	$0x2, %eax
 29599c6:      	sete	%dl
 29599c9:      	orb	%cl, %dl
 29599cb:      	jne	0x2959a0c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b4c>
 29599cd:      	xorl	%ecx, %ecx
 29599cf:      	cmpl	$0x4, %eax
 29599d2:      	setb	%cl
 29599d5:      	movq	%rbp, %rsi
 29599d8:      	cmovbq	%r13, %rsi
 29599dc:      	movq	0x28(%rsp), %rdx
 29599e1:      	cmovbl	%r8d, %edx
 29599e5:      	leal	-0x4(%rax,%rcx,4), %r9d
 29599ea:      	subq	$0x8, %rsp
 29599ee:      	movl	$0x4, %edi
 29599f3:      	movq	%r13, %rcx
 29599f6:      	pushq	$0x2
 29599f8:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 29599fd:      	movl	%ebx, %r8d
 2959a00:      	addq	$0x10, %rsp
 2959a04:      	testb	%al, %al
 2959a06:      	je	0x295b096 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31d6>
 2959a0c:      	movq	%r13, 0xa0(%rsp)
 2959a14:      	movl	%r8d, 0xa8(%rsp)
 2959a1c:      	movq	0x230(%rsp), %rdi
 2959a24:      	movq	0x3b0(%rdi), %rax
 2959a2b:      	testq	%rax, %rax
 2959a2e:      	je	0x295bad0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c10>
 2959a34:      	movl	0x8(%rax), %r9d
 2959a38:      	jmp	0x295bad3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c13>
 2959a3d:      	xorl	%edx, %edx
 2959a3f:      	cmpb	$0x1, 0x181(%r14)
 2959a47:      	jne	0x295a241 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2381>
 2959a4d:      	cmpl	$0x1, %edx
 2959a50:      	je	0x295a1ee <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x232e>
 2959a56:      	testl	%edx, %edx
 2959a58:      	jne	0x295a241 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2381>
 2959a5e:      	movq	0x80(%rsp), %r8
 2959a66:      	movl	0x88(%rsp), %r9d
 2959a6e:      	movq	(%rsp), %rdi
 2959a72:      	movl	$0x6f, %esi
 2959a77:      	movq	%rbp, %rdx
 2959a7a:      	movl	%r11d, %ecx
 2959a7d:      	pushq	%r15
 2959a7f:      	pushq	%r14
 2959a81:      	pushq	%rbx
 2959a82:      	pushq	%r12
 2959a84:      	movq	%rbx, %r14
 2959a87:      	movl	%r11d, %ebx
 2959a8a:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959a8f:      	movl	%ebx, %r11d
 2959a92:      	movq	%r14, %rbx
 2959a95:      	addq	$0x20, %rsp
 2959a99:      	testq	%rax, %rax
 2959a9c:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959aa2:      	jmp	0x295a241 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2381>
 2959aa7:      	cmpb	$0x0, 0x1f7(%rsi)
 2959aae:      	movq	(%rsp), %rdi
 2959ab2:      	movl	0xc(%rsp), %ecx
 2959ab6:      	movq	0x220(%rsp), %rax
 2959abe:      	je	0x2959b5a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c9a>
 2959ac4:      	movq	%rsi, %r14
 2959ac7:      	movl	$0x49, %esi
 2959acc:      	movq	0x10(%rsp), %rdx
 2959ad1:      	movq	0x28(%rsp), %r8
 2959ad6:      	movq	%r9, %rbx
 2959ad9:      	movq	0x18(%rsp), %r9
 2959ade:      	pushq	$0x1
 2959ae0:      	pushq	0x238(%rsp)
 2959ae7:      	pushq	%r14
 2959ae9:      	pushq	%rax
 2959aea:      	pushq	$0x0
 2959aec:      	pushq	%r12
 2959aee:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2959af3:      	movl	0x3c(%rsp), %ecx
 2959af7:      	movq	0x30(%rsp), %rdi
 2959afc:      	addq	$0x30, %rsp
 2959b00:      	testq	%rax, %rax
 2959b03:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959b09:      	movl	0x148(%r14), %eax
 2959b10:      	movzbl	0x1db(%r14), %r10d
 2959b18:      	subq	$0x8, %rsp
 2959b1c:      	movl	$0x49, %esi
 2959b21:      	movq	0x18(%rsp), %rdx
 2959b26:      	movq	%r12, %r8
 2959b29:      	movq	%r13, %r9
 2959b2c:      	pushq	0x238(%rsp)
 2959b33:      	pushq	%r10
 2959b35:      	pushq	%rax
 2959b36:      	movl	%ecx, %r15d
 2959b39:      	callq	0x296ff80 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959b3e:      	addq	$0x20, %rsp
 2959b42:      	testq	%rax, %rax
 2959b45:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959b4b:      	testq	%r13, %r13
 2959b4e:      	movl	%r15d, %ecx
 2959b51:      	movq	%rbx, %r9
 2959b54:      	jne	0x295a877 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29b7>
 2959b5a:      	movq	%r13, %rbp
 2959b5d:      	movaps	-0x1b39844(%rip), %xmm0 # 0xe20320 <.Lswitch.table._ZN4llvm5XCOFF25parseParmsTypeWithVecInfoEjjjj.10>
 2959b64:      	movaps	%xmm0, 0x70(%rsp)
 2959b69:      	movaps	-0x1b41b60(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 2959b70:      	movaps	%xmm0, 0x80(%rsp)
 2959b78:      	movq	0x230(%rsp), %r15
 2959b80:      	movq	0x10(%rsp), %r13
 2959b85:      	movaps	-0x1b41b7c(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 2959b8c:      	movaps	%xmm0, 0xa0(%rsp)
 2959b94:      	leaq	0xa0(%rsp), %rdx
 2959b9c:      	movl	$0x4, %ebx
 2959ba1:      	movl	$0x4, %ecx
 2959ba6:      	movq	%r12, %rdi
 2959ba9:      	movq	%rbp, %rsi
 2959bac:      	movq	%r13, %r8
 2959baf:      	movl	0xc(%rsp), %r9d
 2959bb4:      	pushq	0x18(%rsp)
 2959bb8:      	pushq	0x30(%rsp)
 2959bbc:      	callq	0x2961a60 <_ZL19isShuffleEquivalentN4llvm8ArrayRefIiEES1_NS_7SDValueES2_>
 2959bc1:      	addq	$0x10, %rsp
 2959bc5:      	testb	%al, %al
 2959bc7:      	leaq	0x80(%rsp), %rdi
 2959bcf:      	cmoveq	%r12, %rdi
 2959bd3:      	cmoveq	%rbp, %rbx
 2959bd7:      	movq	%rbx, %rsi
 2959bda:      	callq	0x2962860 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 2959bdf:      	movl	%eax, %esi
 2959be1:      	subq	$0x8, %rsp
 2959be5:      	xorl	%ebx, %ebx
 2959be7:      	movq	%r15, %rdi
 2959bea:      	movq	0x8(%rsp), %rdx
 2959bef:      	movl	$0x5, %ecx
 2959bf4:      	xorl	%r8d, %r8d
 2959bf7:      	movl	$0x1, %r9d
 2959bfd:      	pushq	$0x0
 2959bff:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 2959c04:      	addq	$0x10, %rsp
 2959c08:      	movq	%rax, 0xa0(%rsp)
 2959c10:      	movl	%edx, 0xa8(%rsp)
 2959c17:      	movq	%r13, 0x30(%rsp)
 2959c1c:      	movl	0xc(%rsp), %eax
 2959c20:      	movl	%eax, 0x38(%rsp)
 2959c24:      	movq	0x3b0(%r15), %rax
 2959c2b:      	testq	%rax, %rax
 2959c2e:      	je	0x2959c33 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d73>
 2959c30:      	movl	0x8(%rax), %ebx
 2959c33:      	subq	$0x20, %rsp
 2959c37:      	movups	0xc0(%rsp), %xmm0
 2959c3f:      	movups	%xmm0, 0x10(%rsp)
 2959c44:      	movdqu	0x50(%rsp), %xmm0
 2959c4a:      	movdqu	%xmm0, (%rsp)
 2959c4f:      	movq	%r15, %rdi
 2959c52:      	movl	$0x2b9, %esi            # imm = 0x2B9
 2959c57:      	movq	0x20(%rsp), %rdx
 2959c5c:      	movl	$0x49, %ecx
 2959c61:      	xorl	%r8d, %r8d
 2959c64:      	movl	%ebx, %r9d
 2959c67:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 2959c6c:      	addq	$0x20, %rsp
 2959c70:      	movl	%edx, %r8d
 2959c73:      	movl	%r8d, %edx
 2959c76:      	addq	$0x1d8, %rsp            # imm = 0x1D8
 2959c7d:      	popq	%rbx
 2959c7e:      	popq	%r12
 2959c80:      	popq	%r13
 2959c82:      	popq	%r14
 2959c84:      	popq	%r15
 2959c86:      	popq	%rbp
 2959c87:      	retq
 2959c88:      	testl	%r15d, %r15d
 2959c8b:      	movq	%r11, %r12
 2959c8e:      	je	0x295a877 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29b7>
 2959c94:      	movq	%r12, 0x58(%rsp)
 2959c99:      	cmpl	$0x8, 0x148(%r14)
 2959ca1:      	movq	0x10(%rsp), %r12
 2959ca6:      	movq	0x28(%rsp), %rbp
 2959cab:      	jl	0x2959ce7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1e27>
 2959cad:      	movq	%r12, %rsi
 2959cb0:      	movl	%ecx, %edx
 2959cb2:      	movq	%rbp, %rcx
 2959cb5:      	movq	0x18(%rsp), %r8
 2959cba:      	movq	0x58(%rsp), %r9
 2959cbf:      	pushq	0x230(%rsp)
 2959cc6:      	pushq	%r13
 2959cc8:      	callq	0x2962b20 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959ccd:      	movq	0x230(%rsp), %r10
 2959cd5:      	movl	0x1c(%rsp), %ecx
 2959cd9:      	movq	0x10(%rsp), %rdi
 2959cde:      	addq	$0x10, %rsp
 2959ce2:      	testq	%rax, %rax
 2959ce5:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959ce7:      	movl	$0x49, %esi
 2959cec:      	movq	%r12, %rdx
 2959cef:      	movq	%rbp, %r8
 2959cf2:      	movq	0x18(%rsp), %r9
 2959cf7:      	pushq	$0x0
 2959cf9:      	movq	%r13, %r12
 2959cfc:      	movq	%r14, %r13
 2959cff:      	movq	%rbp, %r14
 2959d02:      	movq	0x238(%rsp), %rbp
 2959d0a:      	pushq	%rbp
 2959d0b:      	pushq	%r13
 2959d0d:      	pushq	%r10
 2959d0f:      	pushq	%r12
 2959d11:      	movq	0x80(%rsp), %rbx
 2959d19:      	pushq	%rbx
 2959d1a:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2959d1f:      	addq	$0x30, %rsp
 2959d23:      	testq	%rax, %rax
 2959d26:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959d2c:      	movq	%r12, 0x20(%rsp)
 2959d31:      	cmpl	$0x1, %r15d
 2959d35:      	movq	%rbp, %r12
 2959d38:      	movq	%r14, %r15
 2959d3b:      	jne	0x2959d82 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1ec2>
 2959d3d:      	movq	0x220(%rsp), %r10
 2959d45:      	movl	0x8(%r10), %eax
 2959d49:      	movq	(%rsp), %rdi
 2959d4d:      	movl	$0x49, %esi
 2959d52:      	movq	0x10(%rsp), %rdx
 2959d57:      	movl	0xc(%rsp), %ecx
 2959d5b:      	movq	%r15, %r8
 2959d5e:      	movq	0x18(%rsp), %r9
 2959d63:      	pushq	%r12
 2959d65:      	pushq	%r13
 2959d67:      	pushq	%rax
 2959d68:      	pushq	(%r10)
 2959d6b:      	pushq	0x40(%rsp)
 2959d6f:      	pushq	%rbx
 2959d70:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959d75:      	addq	$0x30, %rsp
 2959d79:      	testq	%rax, %rax
 2959d7c:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959d82:      	movl	0x148(%r13), %ebp
 2959d89:      	cmpl	$0x5, %ebp
 2959d8c:      	movq	0x18(%rsp), %rbx
 2959d91:      	jl	0x2959dd8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1f18>
 2959d93:      	subq	$0x8, %rsp
 2959d97:      	movq	0x8(%rsp), %rdi
 2959d9c:      	movl	$0x49, %esi
 2959da1:      	movq	0x18(%rsp), %rdx
 2959da6:      	movl	0x14(%rsp), %ecx
 2959daa:      	movq	%r15, %r8
 2959dad:      	movl	%ebx, %r9d
 2959db0:      	pushq	%r12
 2959db2:      	pushq	%r13
 2959db4:      	pushq	0x238(%rsp)
 2959dbb:      	pushq	0x40(%rsp)
 2959dbf:      	pushq	0x80(%rsp)
 2959dc6:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959dcb:      	addq	$0x30, %rsp
 2959dcf:      	testq	%rax, %rax
 2959dd2:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959dd8:      	movl	%ebp, 0x9c(%rsp)
 2959ddf:      	movl	0x1e4(%r13), %eax
 2959de6:      	subq	$0x8, %rsp
 2959dea:      	movq	0x8(%rsp), %rdi
 2959def:      	movl	$0x49, %esi
 2959df4:      	movq	%r15, %r8
 2959df7:      	movq	0x18(%rsp), %rbp
 2959dfc:      	movq	%rbp, %rdx
 2959dff:      	movl	0x14(%rsp), %r15d
 2959e04:      	movl	%r15d, %ecx
 2959e07:      	movq	%r8, %r14
 2959e0a:      	movl	%ebx, %r9d
 2959e0d:      	pushq	%r12
 2959e0f:      	pushq	%rax
 2959e10:      	pushq	0x238(%rsp)
 2959e17:      	movq	%rbx, %r13
 2959e1a:      	movq	0x40(%rsp), %rbx
 2959e1f:      	pushq	%rbx
 2959e20:      	movq	0x80(%rsp), %r12
 2959e28:      	pushq	%r12
 2959e2a:      	callq	0x2969d70 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959e2f:      	addq	$0x30, %rsp
 2959e33:      	testq	%rax, %rax
 2959e36:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959e3c:      	subq	$0x8, %rsp
 2959e40:      	movq	0x8(%rsp), %rdi
 2959e45:      	movl	$0x49, %esi
 2959e4a:      	movq	%rbp, %rdx
 2959e4d:      	movl	%r15d, %ecx
 2959e50:      	movq	%r14, %r8
 2959e53:      	movl	%r13d, %r9d
 2959e56:      	movq	0x238(%rsp), %r13
 2959e5e:      	pushq	%r13
 2959e60:      	pushq	%rbx
 2959e61:      	pushq	%r12
 2959e63:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959e68:      	addq	$0x20, %rsp
 2959e6c:      	testq	%rax, %rax
 2959e6f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959e75:      	movq	%r14, %r15
 2959e78:      	movq	0x228(%rsp), %r14
 2959e80:      	movl	0x148(%r14), %eax
 2959e87:      	cmpl	$0x4, %eax
 2959e8a:      	movq	%r13, %r12
 2959e8d:      	jl	0x2959f15 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2055>
 2959e93:      	cmpb	$0x1, 0x1d1(%r14)
 2959e9b:      	jne	0x2959ee0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2020>
 2959e9d:      	subq	$0x8, %rsp
 2959ea1:      	movq	0x8(%rsp), %rdi
 2959ea6:      	movl	$0x49, %esi
 2959eab:      	movq	0x18(%rsp), %rdx
 2959eb0:      	movl	0x14(%rsp), %ecx
 2959eb4:      	movq	%r15, %r8
 2959eb7:      	movq	0x20(%rsp), %r9
 2959ebc:      	pushq	%r12
 2959ebe:      	pushq	%rax
 2959ebf:      	pushq	0x238(%rsp)
 2959ec6:      	pushq	%rbx
 2959ec7:      	pushq	0x80(%rsp)
 2959ece:      	callq	0x2965b20 <_ZL20lowerShuffleAsVALIGNRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959ed3:      	addq	$0x30, %rsp
 2959ed7:      	testq	%rax, %rax
 2959eda:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959ee0:      	movq	(%rsp), %rdi
 2959ee4:      	movl	$0x49, %esi
 2959ee9:      	movq	0x10(%rsp), %rdx
 2959eee:      	movl	0xc(%rsp), %ecx
 2959ef2:      	movq	%r15, %r8
 2959ef5:      	movq	0x18(%rsp), %r9
 2959efa:      	pushq	%r12
 2959efc:      	pushq	%r14
 2959efe:      	pushq	%rbx
 2959eff:      	pushq	0x70(%rsp)
 2959f03:      	callq	0x2966130 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959f08:      	addq	$0x20, %rsp
 2959f0c:      	testq	%rax, %rax
 2959f0f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959f15:      	movq	0x58(%rsp), %r15
 2959f1a:      	movq	%r15, %rdi
 2959f1d:      	callq	0x2967700 <_ZL18isSingleSHUFPSMaskN4llvm8ArrayRefIiEE>
 2959f22:      	testb	%al, %al
 2959f24:      	je	0x295bdb5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ef5>
 2959f2a:      	movq	%r12, %rdi
 2959f2d:      	movl	$0x84, %esi
 2959f32:      	xorl	%edx, %edx
 2959f34:      	movq	0x10(%rsp), %rcx
 2959f39:      	movl	0xc(%rsp), %r8d
 2959f3e:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959f43:      	movq	%rax, %rbx
 2959f46:      	movl	%edx, %ebp
 2959f48:      	movq	%r12, %rdi
 2959f4b:      	movl	$0x84, %esi
 2959f50:      	xorl	%edx, %edx
 2959f52:      	movq	0x28(%rsp), %rcx
 2959f57:      	movq	0x18(%rsp), %r8
 2959f5c:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959f61:      	movq	%rax, 0xa0(%rsp)
 2959f69:      	movl	%edx, 0xa8(%rsp)
 2959f70:      	movq	%r15, 0x30(%rsp)
 2959f75:      	movq	0x20(%rsp), %rax
 2959f7a:      	movq	%rax, 0x38(%rsp)
 2959f7f:      	subq	$0x20, %rsp
 2959f83:      	movups	0x50(%rsp), %xmm0
 2959f88:      	movups	%xmm0, 0x10(%rsp)
 2959f8d:      	movdqu	0xc0(%rsp), %xmm0
 2959f96:      	movdqu	%xmm0, (%rsp)
 2959f9b:      	movq	%r12, %rdi
 2959f9e:      	movl	$0x84, %esi
 2959fa3:      	xorl	%edx, %edx
 2959fa5:      	movq	0x20(%rsp), %rcx
 2959faa:      	movq	%rbx, %r8
 2959fad:      	movl	%ebp, %r9d
 2959fb0:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 2959fb5:      	addq	$0x20, %rsp
 2959fb9:      	movl	%edx, %r8d
 2959fbc:      	movq	%r12, %rdi
 2959fbf:      	movl	$0x49, %esi
 2959fc4:      	xorl	%edx, %edx
 2959fc6:      	movq	%rax, %rcx
 2959fc9:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959fce:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 2959fd3:      	xorl	%r9d, %r9d
 2959fd6:      	movq	%rbx, %r13
 2959fd9:      	movq	%rbp, 0xa0(%rsp)
 2959fe1:      	movl	%r11d, 0xa8(%rsp)
 2959fe9:      	subq	$0x10, %rsp
 2959fed:      	movups	0xb0(%rsp), %xmm0
 2959ff5:      	movups	%xmm0, (%rsp)
 2959ff9:      	leaq	0x40(%rsp), %rdx
 2959ffe:      	movq	%r15, %rdi
 295a001:      	movl	$0xf3, %esi
 295a006:      	movl	$0x3e, %ecx
 295a00b:      	xorl	%r8d, %r8d
 295a00e:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a013:      	addq	$0x10, %rsp
 295a017:      	movq	%rax, %rbp
 295a01a:      	movl	%edx, %r11d
 295a01d:      	movq	0x30(%rsp), %rsi
 295a022:      	testq	%rsi, %rsi
 295a025:      	je	0x295a037 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2177>
 295a027:      	leaq	0x30(%rsp), %rdi
 295a02c:      	movl	%r11d, %ebx
 295a02f:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a034:      	movl	%ebx, %r11d
 295a037:      	leaq	0x210(%rsp), %rdx
 295a03f:      	movq	(%rdx), %r14
 295a042:      	movl	0x8(%rdx), %ebx
 295a045:      	movq	0x30(%r14), %rax
 295a049:      	movq	%rbx, %rcx
 295a04c:      	shlq	$0x4, %rcx
 295a050:      	cmpw	$0x3e, (%rax,%rcx)
 295a055:      	je	0x295a109 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2249>
 295a05b:      	movq	%rbp, 0x10(%rsp)
 295a060:      	movq	0x48(%r14), %rsi
 295a064:      	movq	%rsi, 0x30(%rsp)
 295a069:      	testq	%rsi, %rsi
 295a06c:      	je	0x295a083 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21c3>
 295a06e:      	leaq	0x30(%rsp), %rdi
 295a073:      	movl	$0x1, %edx
 295a078:      	movl	%r11d, %ebp
 295a07b:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a080:      	movl	%ebp, %r11d
 295a083:      	movl	0x44(%r14), %eax
 295a087:      	movl	%eax, 0x38(%rsp)
 295a08b:      	movq	0x3b0(%r15), %rax
 295a092:      	movl	%r11d, %ebp
 295a095:      	testq	%rax, %rax
 295a098:      	je	0x295a0a0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21e0>
 295a09a:      	movl	0x8(%rax), %r9d
 295a09e:      	jmp	0x295a0a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21e3>
 295a0a0:      	xorl	%r9d, %r9d
 295a0a3:      	movq	%r14, 0xa0(%rsp)
 295a0ab:      	movl	%ebx, 0xa8(%rsp)
 295a0b2:      	subq	$0x10, %rsp
 295a0b6:      	movups	0xb0(%rsp), %xmm0
 295a0be:      	movups	%xmm0, (%rsp)
 295a0c2:      	leaq	0x40(%rsp), %rdx
 295a0c7:      	movq	%r15, %rdi
 295a0ca:      	movl	$0xf3, %esi
 295a0cf:      	movl	$0x3e, %ecx
 295a0d4:      	xorl	%r8d, %r8d
 295a0d7:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a0dc:      	addq	$0x10, %rsp
 295a0e0:      	movq	%rax, %r14
 295a0e3:      	movl	%edx, %ebx
 295a0e5:      	movq	0x30(%rsp), %rsi
 295a0ea:      	testq	%rsi, %rsi
 295a0ed:      	je	0x295a0f9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2239>
 295a0ef:      	leaq	0x30(%rsp), %rdi
 295a0f4:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a0f9:      	movl	%ebp, %r11d
 295a0fc:      	movq	0x10(%rsp), %rbp
 295a101:      	leaq	0x210(%rsp), %rdx
 295a109:      	movq	%r14, (%rdx)
 295a10c:      	movl	%ebx, 0x8(%rdx)
 295a10f:      	movq	%r12, 0x198(%rsp)
 295a117:      	movq	%r13, 0x1a0(%rsp)
 295a11f:      	subq	$0x20, %rsp
 295a123:      	movups	0x1b8(%rsp), %xmm0
 295a12b:      	movups	%xmm0, 0x10(%rsp)
 295a130:      	movdqu	(%rdx), %xmm0
 295a134:      	movdqu	%xmm0, (%rsp)
 295a139:      	movq	%r15, %rdi
 295a13c:      	movl	$0x3e, %esi
 295a141:      	xorl	%edx, %edx
 295a143:      	movq	0x20(%rsp), %rcx
 295a148:      	movq	%rbp, %r8
 295a14b:      	movl	%r11d, %r9d
 295a14e:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295a153:      	addq	$0x20, %rsp
 295a157:      	movl	%edx, %r8d
 295a15a:      	movq	0x30(%rax), %rdx
 295a15e:      	movl	%r8d, %ecx
 295a161:      	shlq	$0x4, %rcx
 295a165:      	cmpw	$0x7b, (%rdx,%rcx)
 295a16a:      	je	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295a170:      	movq	0x48(%rax), %rsi
 295a174:      	movq	%rsi, 0x30(%rsp)
 295a179:      	testq	%rsi, %rsi
 295a17c:      	je	0x295a199 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22d9>
 295a17e:      	leaq	0x30(%rsp), %rdi
 295a183:      	movl	$0x1, %edx
 295a188:      	movq	%rax, %rbx
 295a18b:      	movl	%r8d, %ebp
 295a18e:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a193:      	movl	%ebp, %r8d
 295a196:      	movq	%rbx, %rax
 295a199:      	movl	0x44(%rax), %ecx
 295a19c:      	movl	%ecx, 0x38(%rsp)
 295a1a0:      	movq	0x3b0(%r15), %rcx
 295a1a7:      	testq	%rcx, %rcx
 295a1aa:      	je	0x295a1b2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22f2>
 295a1ac:      	movl	0x8(%rcx), %r9d
 295a1b0:      	jmp	0x295a1b5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22f5>
 295a1b2:      	xorl	%r9d, %r9d
 295a1b5:      	movq	%rax, 0xa0(%rsp)
 295a1bd:      	movl	%r8d, 0xa8(%rsp)
 295a1c5:      	subq	$0x10, %rsp
 295a1c9:      	movdqu	0xb0(%rsp), %xmm0
 295a1d2:      	movdqu	%xmm0, (%rsp)
 295a1d7:      	leaq	0x40(%rsp), %rdx
 295a1dc:      	movq	%r15, %rdi
 295a1df:      	movl	$0xf3, %esi
 295a1e4:      	movl	$0x7b, %ecx
 295a1e9:      	jmp	0x295a4c3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2603>
 295a1ee:      	cmpl	$0x8, (%r12)
 295a1f3:      	jl	0x295a241 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2381>
 295a1f5:      	movq	0x80(%rsp), %r8
 295a1fd:      	movl	0x88(%rsp), %r9d
 295a205:      	movl	0x8(%r10), %eax
 295a209:      	movq	(%rsp), %rdi
 295a20d:      	movl	$0x6f, %esi
 295a212:      	movq	%rbp, %rdx
 295a215:      	movl	%r11d, %ecx
 295a218:      	pushq	%r15
 295a21a:      	pushq	%r14
 295a21c:      	pushq	%rax
 295a21d:      	pushq	(%r10)
 295a220:      	pushq	%rbx
 295a221:      	pushq	%r12
 295a223:      	movq	%rbx, %r14
 295a226:      	movl	%r11d, %ebx
 295a229:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a22e:      	movl	%ebx, %r11d
 295a231:      	movq	%r14, %rbx
 295a234:      	addq	$0x30, %rsp
 295a238:      	testq	%rax, %rax
 295a23b:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a241:      	movq	0x30(%rbp), %rax
 295a245:      	movl	%r11d, %ecx
 295a248:      	shlq	$0x4, %rcx
 295a24c:      	cmpw	$0x3e, (%rax,%rcx)
 295a251:      	jne	0x295a25b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x239b>
 295a253:      	movq	%rbx, %r13
 295a256:      	jmp	0x295a303 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2443>
 295a25b:      	movq	0x48(%rbp), %rsi
 295a25f:      	movq	%rsi, 0x30(%rsp)
 295a264:      	testq	%rsi, %rsi
 295a267:      	je	0x295a284 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23c4>
 295a269:      	leaq	0x30(%rsp), %rdi
 295a26e:      	movl	$0x1, %edx
 295a273:      	movq	%rbx, %r14
 295a276:      	movl	%r11d, %ebx
 295a279:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a27e:      	movl	%ebx, %r11d
 295a281:      	movq	%r14, %rbx
 295a284:      	movl	0x44(%rbp), %eax
 295a287:      	movl	%eax, 0x38(%rsp)
 295a28b:      	movq	0x3b0(%r15), %rax
 295a292:      	testq	%rax, %rax
 295a295:      	je	0x295a29d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23dd>
 295a297:      	movl	0x8(%rax), %r9d
 295a29b:      	jmp	0x295a2a0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23e0>
 295a29d:      	xorl	%r9d, %r9d
 295a2a0:      	movq	%rbx, %r13
 295a2a3:      	movq	%rbp, 0xa0(%rsp)
 295a2ab:      	movl	%r11d, 0xa8(%rsp)
 295a2b3:      	subq	$0x10, %rsp
 295a2b7:      	movdqu	0xb0(%rsp), %xmm0
 295a2c0:      	movdqu	%xmm0, (%rsp)
 295a2c5:      	leaq	0x40(%rsp), %rdx
 295a2ca:      	movq	%r15, %rdi
 295a2cd:      	movl	$0xf3, %esi
 295a2d2:      	movl	$0x3e, %ecx
 295a2d7:      	xorl	%r8d, %r8d
 295a2da:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a2df:      	addq	$0x10, %rsp
 295a2e3:      	movq	%rax, %rbp
 295a2e6:      	movl	%edx, %r11d
 295a2e9:      	movq	0x30(%rsp), %rsi
 295a2ee:      	testq	%rsi, %rsi
 295a2f1:      	je	0x295a303 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2443>
 295a2f3:      	leaq	0x30(%rsp), %rdi
 295a2f8:      	movl	%r11d, %ebx
 295a2fb:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a300:      	movl	%ebx, %r11d
 295a303:      	movq	0x80(%rsp), %r14
 295a30b:      	movl	0x88(%rsp), %ebx
 295a312:      	movq	0x30(%r14), %rax
 295a316:      	movq	%rbx, %rcx
 295a319:      	shlq	$0x4, %rcx
 295a31d:      	cmpw	$0x3e, (%rax,%rcx)
 295a322:      	je	0x295a3db <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x251b>
 295a328:      	movq	%rbp, %r15
 295a32b:      	movq	0x48(%r14), %rsi
 295a32f:      	movq	%rsi, 0x30(%rsp)
 295a334:      	testq	%rsi, %rsi
 295a337:      	movl	%r11d, %ebp
 295a33a:      	je	0x295a34b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x248b>
 295a33c:      	leaq	0x30(%rsp), %rdi
 295a341:      	movl	$0x1, %edx
 295a346:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a34b:      	movl	0x44(%r14), %eax
 295a34f:      	movl	%eax, 0x38(%rsp)
 295a353:      	movq	0x230(%rsp), %rax
 295a35b:      	movq	0x3b0(%rax), %rax
 295a362:      	testq	%rax, %rax
 295a365:      	je	0x295a36d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x24ad>
 295a367:      	movl	0x8(%rax), %r9d
 295a36b:      	jmp	0x295a370 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x24b0>
 295a36d:      	xorl	%r9d, %r9d
 295a370:      	movq	%r14, 0xa0(%rsp)
 295a378:      	movl	%ebx, 0xa8(%rsp)
 295a37f:      	subq	$0x10, %rsp
 295a383:      	movdqu	0xb0(%rsp), %xmm0
 295a38c:      	movdqu	%xmm0, (%rsp)
 295a391:      	leaq	0x40(%rsp), %rdx
 295a396:      	movq	0x240(%rsp), %rdi
 295a39e:      	movl	$0xf3, %esi
 295a3a3:      	movl	$0x3e, %ecx
 295a3a8:      	xorl	%r8d, %r8d
 295a3ab:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a3b0:      	addq	$0x10, %rsp
 295a3b4:      	movq	%rax, %r14
 295a3b7:      	movl	%edx, %ebx
 295a3b9:      	movq	0x30(%rsp), %rsi
 295a3be:      	testq	%rsi, %rsi
 295a3c1:      	je	0x295a3cd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x250d>
 295a3c3:      	leaq	0x30(%rsp), %rdi
 295a3c8:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a3cd:      	movl	%ebp, %r11d
 295a3d0:      	movq	%r15, %rbp
 295a3d3:      	movq	0x230(%rsp), %r15
 295a3db:      	movq	%r14, 0x80(%rsp)
 295a3e3:      	movl	%ebx, 0x88(%rsp)
 295a3ea:      	movq	%r12, 0x70(%rsp)
 295a3ef:      	movq	%r13, 0x78(%rsp)
 295a3f4:      	subq	$0x20, %rsp
 295a3f8:      	movups	0x90(%rsp), %xmm0
 295a400:      	movups	%xmm0, 0x10(%rsp)
 295a405:      	movdqa	0xa0(%rsp), %xmm0
 295a40e:      	movdqu	%xmm0, (%rsp)
 295a413:      	movq	%r15, %rdi
 295a416:      	movl	$0x3e, %esi
 295a41b:      	xorl	%edx, %edx
 295a41d:      	movq	0x20(%rsp), %rcx
 295a422:      	movq	%rbp, %r8
 295a425:      	movl	%r11d, %r9d
 295a428:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295a42d:      	addq	$0x20, %rsp
 295a431:      	movl	%edx, %r8d
 295a434:      	movq	0x30(%rax), %rdx
 295a438:      	movl	%r8d, %ecx
 295a43b:      	shlq	$0x4, %rcx
 295a43f:      	cmpw	$0x6f, (%rdx,%rcx)
 295a444:      	je	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295a44a:      	movq	0x48(%rax), %rsi
 295a44e:      	movq	%rsi, 0x30(%rsp)
 295a453:      	testq	%rsi, %rsi
 295a456:      	je	0x295a473 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25b3>
 295a458:      	leaq	0x30(%rsp), %rdi
 295a45d:      	movl	$0x1, %edx
 295a462:      	movq	%rax, %rbx
 295a465:      	movl	%r8d, %ebp
 295a468:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a46d:      	movl	%ebp, %r8d
 295a470:      	movq	%rbx, %rax
 295a473:      	movl	0x44(%rax), %ecx
 295a476:      	movl	%ecx, 0x38(%rsp)
 295a47a:      	movq	0x3b0(%r15), %rcx
 295a481:      	testq	%rcx, %rcx
 295a484:      	je	0x295a48c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25cc>
 295a486:      	movl	0x8(%rcx), %r9d
 295a48a:      	jmp	0x295a48f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25cf>
 295a48c:      	xorl	%r9d, %r9d
 295a48f:      	movq	%rax, 0xa0(%rsp)
 295a497:      	movl	%r8d, 0xa8(%rsp)
 295a49f:      	subq	$0x10, %rsp
 295a4a3:      	movdqu	0xb0(%rsp), %xmm0
 295a4ac:      	movdqu	%xmm0, (%rsp)
 295a4b1:      	leaq	0x40(%rsp), %rdx
 295a4b6:      	movq	%r15, %rdi
 295a4b9:      	movl	$0xf3, %esi
 295a4be:      	movl	$0x6f, %ecx
 295a4c3:      	xorl	%r8d, %r8d
 295a4c6:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a4cb:      	addq	$0x10, %rsp
 295a4cf:      	movl	%edx, %r8d
 295a4d2:      	movq	0x30(%rsp), %rsi
 295a4d7:      	testq	%rsi, %rsi
 295a4da:      	je	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295a4e0:      	leaq	0x30(%rsp), %rdi
 295a4e5:      	movq	%rax, %rbx
 295a4e8:      	movl	%r8d, %ebp
 295a4eb:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a4f0:      	movl	%ebp, %r8d
 295a4f3:      	movq	%rbx, %rax
 295a4f6:      	jmp	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295a4fb:      	movl	$0x3e, %esi
 295a500:      	movq	0x10(%rsp), %r13
 295a505:      	movq	%r13, %rdx
 295a508:      	movq	%r13, %r8
 295a50b:      	movl	%ecx, %r9d
 295a50e:      	pushq	$0x0
 295a510:      	movq	0x238(%rsp), %r15
 295a518:      	pushq	%r15
 295a51a:      	pushq	%rbx
 295a51b:      	pushq	%r10
 295a51d:      	pushq	%r11
 295a51f:      	pushq	%r12
 295a521:      	movl	%ecx, %ebp
 295a523:      	movq	%r11, %r15
 295a526:      	callq	0x2963030 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 295a52b:      	addq	$0x30, %rsp
 295a52f:      	testq	%rax, %rax
 295a532:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a538:      	movq	(%rsp), %rdi
 295a53c:      	movl	$0x3e, %esi
 295a541:      	movq	%r13, %rdx
 295a544:      	movl	%ebp, %ecx
 295a546:      	movq	%r14, %r8
 295a549:      	movl	0x58(%rsp), %r9d
 295a54e:      	pushq	0x230(%rsp)
 295a555:      	pushq	%rbx
 295a556:      	pushq	%r15
 295a558:      	pushq	%r12
 295a55a:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a55f:      	addq	$0x20, %rsp
 295a563:      	testq	%rax, %rax
 295a566:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a56c:      	movl	0x148(%rbx), %eax
 295a572:      	movzbl	0x1db(%rbx), %r10d
 295a57a:      	subq	$0x8, %rsp
 295a57e:      	movq	0x8(%rsp), %rdi
 295a583:      	movl	$0x3e, %esi
 295a588:      	movq	%r13, %rdx
 295a58b:      	movl	%ebp, %ecx
 295a58d:      	movq	%r12, %r8
 295a590:      	movq	%r15, %r9
 295a593:      	pushq	0x238(%rsp)
 295a59a:      	pushq	%r10
 295a59c:      	pushq	%rax
 295a59d:      	callq	0x296ff80 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a5a2:      	addq	$0x20, %rsp
 295a5a6:      	testq	%rax, %rax
 295a5a9:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a5af:      	subq	$0x8, %rsp
 295a5b3:      	movq	0x8(%rsp), %rdi
 295a5b8:      	movl	$0x3e, %esi
 295a5bd:      	movq	%r13, %rdx
 295a5c0:      	movl	%ebp, %ecx
 295a5c2:      	movq	%r14, %r8
 295a5c5:      	movq	%r14, %rbx
 295a5c8:      	movl	0x60(%rsp), %r14d
 295a5cd:      	movl	%r14d, %r9d
 295a5d0:      	pushq	0x238(%rsp)
 295a5d7:      	pushq	%r15
 295a5d9:      	pushq	%r12
 295a5db:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295a5e0:      	addq	$0x20, %rsp
 295a5e4:      	testq	%rax, %rax
 295a5e7:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a5ed:      	movq	(%rsp), %rdi
 295a5f1:      	movl	$0x3e, %esi
 295a5f6:      	movq	%r13, %rdx
 295a5f9:      	movl	%ebp, %ecx
 295a5fb:      	movq	%rbx, %r8
 295a5fe:      	movl	%r14d, %r9d
 295a601:      	pushq	0x230(%rsp)
 295a608:      	movq	0x230(%rsp), %rbx
 295a610:      	pushq	%rbx
 295a611:      	pushq	%r15
 295a613:      	pushq	%r12
 295a615:      	callq	0x2971bd0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a61a:      	addq	$0x20, %rsp
 295a61e:      	testq	%rax, %rax
 295a621:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a627:      	movq	(%rsp), %rdi
 295a62b:      	movl	$0x3e, %esi
 295a630:      	movq	%r13, %rdx
 295a633:      	movl	%ebp, %ecx
 295a635:      	movq	%r13, %r8
 295a638:      	movl	%ebp, %r9d
 295a63b:      	pushq	0x230(%rsp)
 295a642:      	pushq	%rbx
 295a643:      	pushq	%r15
 295a645:      	pushq	%r12
 295a647:      	callq	0x2966130 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a64c:      	addq	$0x20, %rsp
 295a650:      	testq	%rax, %rax
 295a653:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a659:      	leaq	0xa0(%rsp), %rdi
 295a661:      	movq	%r12, %rsi
 295a664:      	movq	%r15, %rdx
 295a667:      	callq	0x2953ff0 <_ZN4llvm11SmallVectorIiLj8EEC2IivEENS_8ArrayRefIT_EE>
 295a66c:      	movq	0xa0(%rsp), %r8
 295a674:      	movl	0xa8(%rsp), %r9d
 295a67c:      	movq	(%rsp), %rdi
 295a680:      	movl	$0x3e, %esi
 295a685:      	movq	%r13, %rdx
 295a688:      	movl	%ebp, %ecx
 295a68a:      	pushq	0x230(%rsp)
 295a691:      	pushq	%rbx
 295a692:      	callq	0x2972000 <_ZL35lowerV8I16GeneralSingleInputShuffleRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_15MutableArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a697:      	addq	$0x10, %rsp
 295a69b:      	movq	%rax, %rbx
 295a69e:      	movl	%edx, %ebp
 295a6a0:      	movq	0xa0(%rsp), %rdi
 295a6a8:      	leaq	0xb0(%rsp), %rax
 295a6b0:      	cmpq	%rax, %rdi
 295a6b3:      	je	0x295a6ba <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x27fa>
 295a6b5:      	callq	0x828a6d0 <free@plt>
 295a6ba:      	movq	%rbx, %rax
 295a6bd:      	movl	%ebp, %r8d
 295a6c0:      	jmp	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295a6c5:      	movq	0x48(%r12), %rsi
 295a6ca:      	movq	%rsi, 0x30(%rsp)
 295a6cf:      	testq	%rsi, %rsi
 295a6d2:      	movq	%r12, %rbx
 295a6d5:      	je	0x295a6e6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2826>
 295a6d7:      	leaq	0x30(%rsp), %rdi
 295a6dc:      	movl	$0x1, %edx
 295a6e1:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a6e6:      	movl	0x44(%rbx), %eax
 295a6e9:      	movl	%eax, 0x38(%rsp)
 295a6ed:      	movq	0x3b0(%r15), %rax
 295a6f4:      	testq	%rax, %rax
 295a6f7:      	je	0x295ae78 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2fb8>
 295a6fd:      	movl	0x8(%rax), %r9d
 295a701:      	jmp	0x295ae7b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2fbb>
 295a706:      	movq	%rbx, %r12
 295a709:      	movq	0x10(%rsp), %rdx
 295a70e:      	movq	%rdx, 0x20(%rsp)
 295a713:      	movl	%ebp, %r10d
 295a716:      	movl	%ebp, %ebx
 295a718:      	cmpl	$-0x1, %ecx
 295a71b:      	jne	0x295a76e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x28ae>
 295a71d:      	xorps	%xmm0, %xmm0
 295a720:      	movaps	%xmm0, 0xa0(%rsp)
 295a728:      	leaq	0xa0(%rsp), %rdx
 295a730:      	movq	%r15, %rdi
 295a733:      	movl	$0x35, %esi
 295a738:      	movl	$0x96, %ecx
 295a73d:      	xorl	%r8d, %r8d
 295a740:      	callq	0x5e1ec80 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTE>
 295a745:      	movq	%rax, 0x20(%rsp)
 295a74a:      	movl	%edx, %ebx
 295a74c:      	movq	0xa0(%rsp), %rsi
 295a754:      	testq	%rsi, %rsi
 295a757:      	je	0x295a766 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x28a6>
 295a759:      	leaq	0xa0(%rsp), %rdi
 295a761:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a766:      	movl	0x4(%r12), %eax
 295a76b:      	movl	%ebp, %r10d
 295a76e:      	cmpl	$-0x1, %eax
 295a771:      	jne	0x295a7c3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2903>
 295a773:      	xorps	%xmm0, %xmm0
 295a776:      	movaps	%xmm0, 0xa0(%rsp)
 295a77e:      	leaq	0xa0(%rsp), %rdx
 295a786:      	movq	%r15, %rdi
 295a789:      	movl	$0x35, %esi
 295a78e:      	movl	$0x96, %ecx
 295a793:      	xorl	%r8d, %r8d
 295a796:      	callq	0x5e1ec80 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTE>
 295a79b:      	movq	%rax, 0x10(%rsp)
 295a7a0:      	movl	%edx, %r10d
 295a7a3:      	movq	0xa0(%rsp), %rsi
 295a7ab:      	testq	%rsi, %rsi
 295a7ae:      	je	0x295a7c3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2903>
 295a7b0:      	leaq	0xa0(%rsp), %rdi
 295a7b8:      	movl	%r10d, %ebp
 295a7bb:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a7c0:      	movl	%ebp, %r10d
 295a7c3:      	movl	%r14d, %esi
 295a7c6:      	subq	$0x8, %rsp
 295a7ca:      	xorl	%r14d, %r14d
 295a7cd:      	movq	%r15, %rdi
 295a7d0:      	movq	%r13, %rdx
 295a7d3:      	movl	$0x5, %ecx
 295a7d8:      	xorl	%r8d, %r8d
 295a7db:      	movl	$0x1, %r9d
 295a7e1:      	pushq	$0x0
 295a7e3:      	movl	%r10d, %ebp
 295a7e6:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295a7eb:      	addq	$0x10, %rsp
 295a7ef:      	movq	%rax, 0xa0(%rsp)
 295a7f7:      	movl	%edx, 0xa8(%rsp)
 295a7fe:      	movq	0x10(%rsp), %rax
 295a803:      	movq	%rax, 0x30(%rsp)
 295a808:      	movl	%ebp, 0x38(%rsp)
 295a80c:      	movq	0x20(%rsp), %rax
 295a811:      	movq	%rax, 0x70(%rsp)
 295a816:      	movl	%ebx, 0x78(%rsp)
 295a81a:      	movq	0x3b0(%r15), %rax
 295a821:      	testq	%rax, %rax
 295a824:      	je	0x295a82a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x296a>
 295a826:      	movl	0x8(%rax), %r14d
 295a82a:      	subq	$0x30, %rsp
 295a82e:      	movups	0xd0(%rsp), %xmm0
 295a836:      	movups	%xmm0, 0x20(%rsp)
 295a83b:      	movups	0x60(%rsp), %xmm0
 295a840:      	movups	%xmm0, 0x10(%rsp)
 295a845:      	movdqu	0xa0(%rsp), %xmm0
 295a84e:      	movdqu	%xmm0, (%rsp)
 295a853:      	movq	%r15, %rdi
 295a856:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295a85b:      	movq	%r13, %rdx
 295a85e:      	movl	$0x96, %ecx
 295a863:      	xorl	%r8d, %r8d
 295a866:      	movl	%r14d, %r9d
 295a869:      	callq	0x5e2ad10 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295a86e:      	addq	$0x30, %rsp
 295a872:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a877:      	leaq	-0x4(%r9), %rdi
 295a87b:      	cmpq	$0xc, %rdi
 295a87f:      	movq	%r13, 0x20(%rsp)
 295a884:      	jae	0x295aa60 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ba0>
 295a88a:      	xorl	%esi, %esi
 295a88c:      	movq	%r12, %rax
 295a88f:      	movq	0x230(%rsp), %r15
 295a897:      	jmp	0x295ab10 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c50>
 295a89c:      	movl	%ebx, %r8d
 295a89f:      	movq	%r13, %rbp
 295a8a2:      	jmp	0x295b626 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3766>
 295a8a7:      	cmpl	$0x8, 0x148(%r14)
 295a8af:      	movq	(%rsp), %rdi
 295a8b3:      	movl	%ebp, %r11d
 295a8b6:      	movq	%r12, %rbp
 295a8b9:      	movq	0x58(%rsp), %r12
 295a8be:      	movq	0x220(%rsp), %r10
 295a8c6:      	jl	0x295a905 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2a45>
 295a8c8:      	movq	%rbp, %rsi
 295a8cb:      	movl	%r11d, %edx
 295a8ce:      	movq	%r13, %rcx
 295a8d1:      	movl	%ebx, %r8d
 295a8d4:      	movq	%r12, %r9
 295a8d7:      	pushq	0x230(%rsp)
 295a8de:      	pushq	0x28(%rsp)
 295a8e2:      	movl	%r11d, %ebx
 295a8e5:      	movq	%r10, %r13
 295a8e8:      	callq	0x2962b20 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295a8ed:      	movq	%r13, %r10
 295a8f0:      	movl	%ebx, %r11d
 295a8f3:      	movq	0x10(%rsp), %rdi
 295a8f8:      	addq	$0x10, %rsp
 295a8fc:      	testq	%rax, %rax
 295a8ff:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a905:      	cmpl	$0x1, %r15d
 295a909:      	movq	0x230(%rsp), %r15
 295a911:      	jne	0x295a976 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ab6>
 295a913:      	cmpl	$0x4, (%r12)
 295a918:      	jl	0x295a976 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ab6>
 295a91a:      	movq	0x60(%rsp), %r8
 295a91f:      	movl	0x68(%rsp), %r9d
 295a924:      	movl	0x8(%r10), %eax
 295a928:      	movq	%rdi, %rbx
 295a92b:      	movl	$0x84, %esi
 295a930:      	movq	%rbp, %rdx
 295a933:      	movl	%r11d, %ecx
 295a936:      	pushq	%r15
 295a938:      	pushq	0x230(%rsp)
 295a93f:      	pushq	%rax
 295a940:      	pushq	(%r10)
 295a943:      	pushq	0x40(%rsp)
 295a947:      	pushq	%r12
 295a949:      	movq	%r15, %r13
 295a94c:      	movq	%rbp, %r14
 295a94f:      	movl	%r11d, %ebp
 295a952:      	movq	%r10, %r15
 295a955:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a95a:      	movq	%r15, %r10
 295a95d:      	movl	%ebp, %r11d
 295a960:      	movq	%r14, %rbp
 295a963:      	movq	%r13, %r15
 295a966:      	movq	%rbx, %rdi
 295a969:      	addq	$0x30, %rsp
 295a96d:      	testq	%rax, %rax
 295a970:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295a976:      	movq	0x228(%rsp), %rax
 295a97e:      	movl	0x148(%rax), %eax
 295a984:      	cmpl	$0x4, %eax
 295a987:      	jle	0x295a9db <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b1b>
 295a989:      	movl	(%r12), %eax
 295a98d:      	testl	%eax, %eax
 295a98f:      	js	0x295a9ae <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2aee>
 295a991:      	movl	0x4(%r12), %ecx
 295a996:      	testl	%ecx, %ecx
 295a998:      	js	0x295a9ae <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2aee>
 295a99a:      	cmpl	$0x4, %eax
 295a99d:      	setb	%al
 295a9a0:      	cmpl	$0x4, %ecx
 295a9a3:      	setae	%cl
 295a9a6:      	cmpb	%cl, %al
 295a9a8:      	je	0x295b20e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x334e>
 295a9ae:      	movl	0x8(%r12), %eax
 295a9b3:      	testl	%eax, %eax
 295a9b5:      	js	0x295a9d4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b14>
 295a9b7:      	movl	0xc(%r12), %ecx
 295a9bc:      	testl	%ecx, %ecx
 295a9be:      	js	0x295a9d4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b14>
 295a9c0:      	cmpl	$0x4, %eax
 295a9c3:      	setb	%al
 295a9c6:      	cmpl	$0x4, %ecx
 295a9c9:      	setae	%cl
 295a9cc:      	xorb	%al, %cl
 295a9ce:      	je	0x295b20e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x334e>
 295a9d4:      	movq	0x60(%rsp), %r8
 295a9d9:      	jmp	0x295a9e9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b29>
 295a9db:      	movq	0x60(%rsp), %r8
 295a9e0:      	cmpl	$0x2, %eax
 295a9e3:      	jl	0x295b3ad <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x34ed>
 295a9e9:      	movl	0x68(%rsp), %ebx
 295a9ed:      	subq	$0x8, %rsp
 295a9f1:      	movq	%rdi, %r13
 295a9f4:      	movl	$0x84, %esi
 295a9f9:      	movq	%rbp, %rdx
 295a9fc:      	movl	%r11d, %ecx
 295a9ff:      	movl	%ebx, %r9d
 295aa02:      	movq	%r15, %r14
 295aa05:      	pushq	%r15
 295aa07:      	movq	0x30(%rsp), %r15
 295aa0c:      	pushq	%r15
 295aa0e:      	pushq	%r12
 295aa10:      	movq	%r12, %rbx
 295aa13:      	movq	%rbp, %r12
 295aa16:      	movl	%r11d, %ebp
 295aa19:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295aa1e:      	addq	$0x20, %rsp
 295aa22:      	testq	%rax, %rax
 295aa25:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295aa2b:      	subq	$0x20, %rsp
 295aa2f:      	movdqa	0x80(%rsp), %xmm0
 295aa38:      	movdqu	%xmm0, (%rsp)
 295aa3d:      	movq	%r14, 0x10(%rsp)
 295aa42:      	movq	%r13, %rdi
 295aa45:      	movl	$0x84, %esi
 295aa4a:      	movq	%rbx, %rdx
 295aa4d:      	movq	%r15, %rcx
 295aa50:      	movq	%r12, %r8
 295aa53:      	movl	%ebp, %r9d
 295aa56:      	callq	0x2970670 <_ZL22lowerShuffleWithSHUFPSRKN4llvm5SDLocENS_3MVTENS_8ArrayRefIiEENS_7SDValueES6_RNS_12SelectionDAGE>
 295aa5b:      	jmp	0x2959c6c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1dac>
 295aa60:      	shrq	$0x2, %rdi
 295aa64:      	incq	%rdi
 295aa67:      	movabsq	$0x7ffffffffffffff8, %rdx # imm = 0x7FFFFFFFFFFFFFF8
 295aa71:      	orq	$0x4, %rdx
 295aa75:      	andq	%rdi, %rdx
 295aa78:      	leaq	(%r12,%rdx,4), %rax
 295aa7c:      	pxor	%xmm0, %xmm0
 295aa80:      	xorl	%esi, %esi
 295aa82:      	movdqa	-0x1b3ba9a(%rip), %xmm1 # 0xe1eff0 <.LCPI91_5>
 295aa8a:      	pcmpeqd	%xmm2, %xmm2
 295aa8e:      	movdqa	-0x1b37796(%rip), %xmm4 # 0xe23300 <.LCPI91_4>
 295aa96:      	pxor	%xmm3, %xmm3
 295aa9a:      	movq	(%r12,%rsi,4), %xmm5
 295aaa0:      	movq	0x8(%r12,%rsi,4), %xmm6
 295aaa7:      	movdqa	%xmm5, %xmm7
 295aaab:      	pmaxud	%xmm1, %xmm7
 295aab0:      	pcmpeqd	%xmm5, %xmm7
 295aab4:      	pxor	%xmm2, %xmm7
 295aab8:      	pmovzxdq	%xmm7, %xmm5            # xmm5 = xmm7[0],zero,xmm7[1],zero
 295aabd:      	pand	%xmm4, %xmm5
 295aac1:      	paddq	%xmm5, %xmm3
 295aac5:      	movdqa	%xmm6, %xmm5
 295aac9:      	pmaxud	%xmm1, %xmm5
 295aace:      	pcmpeqd	%xmm6, %xmm5
 295aad2:      	pxor	%xmm2, %xmm5
 295aad6:      	pmovzxdq	%xmm5, %xmm5            # xmm5 = xmm5[0],zero,xmm5[1],zero
 295aadb:      	pand	%xmm4, %xmm5
 295aadf:      	paddq	%xmm5, %xmm0
 295aae3:      	addq	$0x4, %rsi
 295aae7:      	cmpq	%rsi, %rdx
 295aaea:      	jne	0x295aa9a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2bda>
 295aaec:      	paddq	%xmm3, %xmm0
 295aaf0:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295aaf5:      	paddq	%xmm0, %xmm1
 295aaf9:      	movq	%xmm1, %rsi
 295aafe:      	cmpq	%rdx, %rdi
 295ab01:      	movq	0x230(%rsp), %r15
 295ab09:      	je	0x295ab20 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c60>
 295ab0b:      	nopl	(%rax,%rax)
 295ab10:      	cmpl	$0x4, (%rax)
 295ab13:      	adcq	$0x0, %rsi
 295ab17:      	addq	$0x4, %rax
 295ab1b:      	cmpq	%rbp, %rax
 295ab1e:      	jne	0x295ab10 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c50>
 295ab20:      	cmpq	$0x2, %rsi
 295ab24:      	movq	0x10(%rsp), %r13
 295ab29:      	movq	0x28(%rsp), %r8
 295ab2e:      	jb	0x295ab63 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ca3>
 295ab30:      	movq	(%rsp), %rdi
 295ab34:      	movl	$0x49, %esi
 295ab39:      	movq	%r13, %rdx
 295ab3c:      	movq	%r9, %rbx
 295ab3f:      	movq	0x18(%rsp), %r9
 295ab44:      	pushq	%r15
 295ab46:      	pushq	%r14
 295ab48:      	pushq	0x30(%rsp)
 295ab4c:      	pushq	%r12
 295ab4e:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295ab53:      	movq	%rbx, %r9
 295ab56:      	addq	$0x20, %rsp
 295ab5a:      	testq	%rax, %rax
 295ab5d:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295ab63:      	movaps	-0x1b3a84a(%rip), %xmm0 # 0xe20320 <.Lswitch.table._ZN4llvm5XCOFF25parseParmsTypeWithVecInfoEjjjj.10>
 295ab6a:      	movaps	%xmm0, 0x70(%rsp)
 295ab6f:      	movaps	-0x1b42b66(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 295ab76:      	movaps	%xmm0, 0x80(%rsp)
 295ab7e:      	xorl	%eax, %eax
 295ab80:      	xorl	%ecx, %ecx
 295ab82:      	xorl	%edx, %edx
 295ab84:      	jmp	0x295ab96 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cd6>
 295ab86:      	incq	%rcx
 295ab89:      	movl	%edi, %esi
 295ab8b:      	addq	$0x4, %rax
 295ab8f:      	movl	%esi, %edi
 295ab91:      	cmpq	%rax, %r9
 295ab94:      	je	0x295abb0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cf0>
 295ab96:      	movl	(%r12,%rax), %esi
 295ab9a:      	cmpl	$-0x1, %esi
 295ab9d:      	je	0x295ab86 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cc6>
 295ab9f:      	cmpb	$0x1, %dl
 295aba2:      	jne	0x295abac <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cec>
 295aba4:      	movb	$0x1, %dl
 295aba6:      	cmpl	%esi, %edi
 295aba8:      	je	0x295ab8b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ccb>
 295abaa:      	jmp	0x295abcf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2d0f>
 295abac:      	movb	$0x1, %dl
 295abae:      	jmp	0x295ab8b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ccb>
 295abb0:      	movq	0x20(%rsp), %rax
 295abb5:      	shrq	%rax
 295abb8:      	cmpq	%rax, %rcx
 295abbb:      	setbe	%al
 295abbe:      	testb	%dl, %al
 295abc0:      	je	0x295abcf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2d0f>
 295abc2:      	movq	%r12, %rdi
 295abc5:      	movq	0x20(%rsp), %rbx
 295abca:      	jmp	0x2959bd7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d17>
 295abcf:      	movq	0x20(%rsp), %rax
 295abd4:      	movq	%rax, %rbp
 295abd7:      	cmpq	$0x4, %rax
 295abdb:      	jne	0x2959b85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cc5>
 295abe1:      	movl	(%r12), %eax
 295abe5:      	testl	%eax, %eax
 295abe7:      	jle	0x295ac2c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2d6c>
 295abe9:      	xorl	%ecx, %ecx
 295abeb:      	cmpl	$0x4, %eax
 295abee:      	setb	%cl
 295abf1:      	movq	0x28(%rsp), %rsi
 295abf6:      	cmovbq	%r13, %rsi
 295abfa:      	movq	0x18(%rsp), %rdx
 295abff:      	movl	0xc(%rsp), %r8d
 295ac04:      	cmovbl	%r8d, %edx
 295ac08:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ac0d:      	subq	$0x8, %rsp
 295ac11:      	movl	$0x4, %edi
 295ac16:      	movq	%r13, %rcx
 295ac19:      	pushq	$0x0
 295ac1b:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ac20:      	addq	$0x10, %rsp
 295ac24:      	testb	%al, %al
 295ac26:      	je	0x2959b85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cc5>
 295ac2c:      	movl	0x4(%r12), %eax
 295ac31:      	testl	%eax, %eax
 295ac33:      	jle	0x295ac78 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2db8>
 295ac35:      	xorl	%ecx, %ecx
 295ac37:      	cmpl	$0x4, %eax
 295ac3a:      	setb	%cl
 295ac3d:      	movq	0x28(%rsp), %rsi
 295ac42:      	cmovbq	%r13, %rsi
 295ac46:      	movq	0x18(%rsp), %rdx
 295ac4b:      	movl	0xc(%rsp), %r8d
 295ac50:      	cmovbl	%r8d, %edx
 295ac54:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ac59:      	subq	$0x8, %rsp
 295ac5d:      	movl	$0x4, %edi
 295ac62:      	movq	%r13, %rcx
 295ac65:      	pushq	$0x0
 295ac67:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ac6c:      	addq	$0x10, %rsp
 295ac70:      	testb	%al, %al
 295ac72:      	je	0x2959b85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cc5>
 295ac78:      	movl	0x8(%r12), %eax
 295ac7d:      	testl	%eax, %eax
 295ac7f:      	sets	%cl
 295ac82:      	cmpl	$0x1, %eax
 295ac85:      	sete	%dl
 295ac88:      	orb	%cl, %dl
 295ac8a:      	jne	0x295accf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e0f>
 295ac8c:      	xorl	%ecx, %ecx
 295ac8e:      	cmpl	$0x4, %eax
 295ac91:      	setb	%cl
 295ac94:      	movq	0x28(%rsp), %rsi
 295ac99:      	cmovbq	%r13, %rsi
 295ac9d:      	movq	0x18(%rsp), %rdx
 295aca2:      	movl	0xc(%rsp), %r8d
 295aca7:      	cmovbl	%r8d, %edx
 295acab:      	leal	-0x4(%rax,%rcx,4), %r9d
 295acb0:      	subq	$0x8, %rsp
 295acb4:      	movl	$0x4, %edi
 295acb9:      	movq	%r13, %rcx
 295acbc:      	pushq	$0x1
 295acbe:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295acc3:      	addq	$0x10, %rsp
 295acc7:      	testb	%al, %al
 295acc9:      	je	0x2959b85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cc5>
 295accf:      	movl	0xc(%r12), %eax
 295acd4:      	testl	%eax, %eax
 295acd6:      	sets	%cl
 295acd9:      	cmpl	$0x1, %eax
 295acdc:      	sete	%dl
 295acdf:      	orb	%cl, %dl
 295ace1:      	movl	$0x4, %ebx
 295ace6:      	leaq	0x70(%rsp), %rdi
 295aceb:      	jne	0x2959bd7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d17>
 295acf1:      	xorl	%ecx, %ecx
 295acf3:      	cmpl	$0x4, %eax
 295acf6:      	setb	%cl
 295acf9:      	movq	0x28(%rsp), %rsi
 295acfe:      	cmovbq	%r13, %rsi
 295ad02:      	movq	0x18(%rsp), %rdx
 295ad07:      	movl	0xc(%rsp), %r8d
 295ad0c:      	cmovbl	%r8d, %edx
 295ad10:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ad15:      	subq	$0x8, %rsp
 295ad19:      	movq	%rdi, %r14
 295ad1c:      	movl	$0x4, %edi
 295ad21:      	movq	%r13, %rcx
 295ad24:      	pushq	$0x1
 295ad26:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ad2b:      	movq	%r14, %rdi
 295ad2e:      	addq	$0x10, %rsp
 295ad32:      	testb	%al, %al
 295ad34:      	je	0x2959b85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cc5>
 295ad3a:      	jmp	0x2959bd7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d17>
 295ad3f:      	cmpl	$0x5, 0x148(%r14)
 295ad47:      	jl	0x295ad8b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ecb>
 295ad49:      	subq	$0x8, %rsp
 295ad4d:      	movq	0x8(%rsp), %rdi
 295ad52:      	movl	$0x96, %esi
 295ad57:      	movq	%rbp, %rdx
 295ad5a:      	movl	0x14(%rsp), %ecx
 295ad5e:      	movq	%r15, %r8
 295ad61:      	movl	0x20(%rsp), %r9d
 295ad66:      	pushq	0x238(%rsp)
 295ad6d:      	pushq	%r14
 295ad6f:      	pushq	0x238(%rsp)
 295ad76:      	pushq	%rbx
 295ad77:      	pushq	%r12
 295ad79:      	callq	0x2964340 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295ad7e:      	addq	$0x30, %rsp
 295ad82:      	testq	%rax, %rax
 295ad85:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295ad8b:      	subq	$0x8, %rsp
 295ad8f:      	movq	0x8(%rsp), %r13
 295ad94:      	movq	%r13, %rdi
 295ad97:      	movl	$0x96, %esi
 295ad9c:      	movq	%rbp, %rdx
 295ad9f:      	movq	%rbx, %rax
 295ada2:      	movq	%r12, %rbx
 295ada5:      	movq	%rbp, %r12
 295ada8:      	movl	0x14(%rsp), %ebp
 295adac:      	movl	%ebp, %ecx
 295adae:      	movq	%r15, %r8
 295adb1:      	movl	0x20(%rsp), %r9d
 295adb6:      	movq	0x238(%rsp), %r15
 295adbe:      	pushq	%r15
 295adc0:      	pushq	%rax
 295adc1:      	pushq	%rbx
 295adc2:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295adc7:      	addq	$0x20, %rsp
 295adcb:      	testq	%rax, %rax
 295adce:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295add4:      	xorl	%eax, %eax
 295add6:      	cmpl	$0x1, (%rbx)
 295add9:      	sete	%al
 295addc:      	xorl	%ecx, %ecx
 295adde:      	cmpl	$0x3, 0x4(%rbx)
 295ade2:      	sete	%cl
 295ade5:      	leaq	(%rax,%rcx,2), %rsi
 295ade9:      	subq	$0x8, %rsp
 295aded:      	xorl	%ebx, %ebx
 295adef:      	movq	%r15, %rdi
 295adf2:      	movq	%r13, %rdx
 295adf5:      	movl	$0x5, %ecx
 295adfa:      	xorl	%r8d, %r8d
 295adfd:      	movl	$0x1, %r9d
 295ae03:      	pushq	$0x0
 295ae05:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295ae0a:      	addq	$0x10, %rsp
 295ae0e:      	movq	%rax, 0xa0(%rsp)
 295ae16:      	movl	%edx, 0xa8(%rsp)
 295ae1d:      	movq	%r12, 0x30(%rsp)
 295ae22:      	movl	%ebp, 0x38(%rsp)
 295ae26:      	movq	0x3b0(%r15), %rax
 295ae2d:      	testq	%rax, %rax
 295ae30:      	je	0x295ae35 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2f75>
 295ae32:      	movl	0x8(%rax), %ebx
 295ae35:      	subq	$0x30, %rsp
 295ae39:      	movups	0xd0(%rsp), %xmm0
 295ae41:      	movups	%xmm0, 0x20(%rsp)
 295ae46:      	leaq	0x240(%rsp), %rax
 295ae4e:      	movups	(%rax), %xmm0
 295ae51:      	movups	%xmm0, 0x10(%rsp)
 295ae56:      	movdqu	0x60(%rsp), %xmm0
 295ae5c:      	movdqu	%xmm0, (%rsp)
 295ae61:      	movq	%r15, %rdi
 295ae64:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295ae69:      	movq	0x30(%rsp), %rdx
 295ae6e:      	movl	$0x96, %ecx
 295ae73:      	jmp	0x295b8c9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a09>
 295ae78:      	xorl	%r9d, %r9d
 295ae7b:      	movq	%rbx, 0xa0(%rsp)
 295ae83:      	movl	%r13d, 0xa8(%rsp)
 295ae8b:      	subq	$0x10, %rsp
 295ae8f:      	movdqu	0xb0(%rsp), %xmm0
 295ae98:      	movdqu	%xmm0, (%rsp)
 295ae9d:      	leaq	0x40(%rsp), %rdx
 295aea2:      	movq	%r15, %rdi
 295aea5:      	movl	$0xf3, %esi
 295aeaa:      	movl	$0x49, %ecx
 295aeaf:      	xorl	%r8d, %r8d
 295aeb2:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295aeb7:      	addq	$0x10, %rsp
 295aebb:      	movq	%rax, %rbp
 295aebe:      	movl	%edx, %r13d
 295aec1:      	movq	0x30(%rsp), %rsi
 295aec6:      	testq	%rsi, %rsi
 295aec9:      	je	0x295aed5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3015>
 295aecb:      	leaq	0x30(%rsp), %rdi
 295aed0:      	callq	0x3bd6ca0 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295aed5:      	movl	(%r14), %eax
 295aed8:      	leal	(%rax,%rax), %ecx
 295aedb:      	testl	%eax, %eax
 295aedd:      	leal	0x1(%rax,%rax), %eax
 295aee1:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 295aee6:      	cmovsl	%edx, %ecx
 295aee9:      	cmovsl	%edx, %eax
 295aeec:      	movl	%ecx, 0x70(%rsp)
 295aef0:      	movl	%eax, 0x74(%rsp)
 295aef4:      	movl	0x4(%r14), %eax
 295aef8:      	leal	(%rax,%rax), %ecx
 295aefb:      	testl	%eax, %eax
 295aefd:      	leal	0x1(%rax,%rax), %eax
 295af01:      	cmovsl	%edx, %ecx
 295af04:      	cmovsl	%edx, %eax
 295af07:      	movl	%ecx, 0x78(%rsp)
 295af0b:      	movl	%eax, 0x7c(%rsp)
 295af0f:      	leaq	0x70(%rsp), %rdi
 295af14:      	movl	$0x4, %esi
 295af19:      	callq	0x2962860 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295af1e:      	movl	%eax, %eax
 295af20:      	movl	$0x8, 0xa8(%rsp)
 295af2b:      	movq	%rax, 0xa0(%rsp)
 295af33:      	movq	0x40(%r15), %rdi
 295af37:      	leaq	0xa0(%rsp), %rsi
 295af3f:      	callq	0x3ae8930 <_ZN4llvm11ConstantInt3getERNS_11LLVMContextERKNS_5APIntE>
 295af44:      	subq	$0x8, %rsp
 295af48:      	xorl	%ebx, %ebx
 295af4a:      	movq	%r15, %rdi
 295af4d:      	movq	%rax, %rsi
 295af50:      	movq	0x8(%rsp), %rdx
 295af55:      	movl	$0x5, %ecx
 295af5a:      	xorl	%r8d, %r8d
 295af5d:      	movl	$0x1, %r9d
 295af63:      	pushq	$0x0
 295af65:      	callq	0x5e01060 <_ZN4llvm12SelectionDAG11getConstantERKNS_11ConstantIntERKNS_5SDLocENS_3EVTEbb>
 295af6a:      	addq	$0x10, %rsp
 295af6e:      	cmpl	$0x41, 0xa8(%rsp)
 295af76:      	jb	0x295af9a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x30da>
 295af78:      	movq	0xa0(%rsp), %rdi
 295af80:      	testq	%rdi, %rdi
 295af83:      	je	0x295af9a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x30da>
 295af85:      	movq	%rax, %r14
 295af88:      	movq	%rbp, %r12
 295af8b:      	movl	%edx, %ebp
 295af8d:      	callq	0x828a840 <_ZdaPv@plt>
 295af92:      	movl	%ebp, %edx
 295af94:      	movq	%r12, %rbp
 295af97:      	movq	%r14, %rax
 295af9a:      	movq	%rax, 0xa0(%rsp)
 295afa2:      	movl	%edx, 0xa8(%rsp)
 295afa9:      	movq	%rbp, 0x30(%rsp)
 295afae:      	movl	%r13d, 0x38(%rsp)
 295afb3:      	movq	0x3b0(%r15), %rax
 295afba:      	testq	%rax, %rax
 295afbd:      	je	0x295afc2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3102>
 295afbf:      	movl	0x8(%rax), %ebx
 295afc2:      	subq	$0x20, %rsp
 295afc6:      	movups	0xc0(%rsp), %xmm0
 295afce:      	movups	%xmm0, 0x10(%rsp)
 295afd3:      	movdqu	0x50(%rsp), %xmm0
 295afd9:      	movdqu	%xmm0, (%rsp)
 295afde:      	movq	%r15, %rdi
 295afe1:      	movl	$0x2b9, %esi            # imm = 0x2B9
 295afe6:      	movq	0x20(%rsp), %rdx
 295afeb:      	movl	$0x49, %ecx
 295aff0:      	xorl	%r8d, %r8d
 295aff3:      	movl	%ebx, %r9d
 295aff6:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295affb:      	addq	$0x20, %rsp
 295afff:      	movl	%edx, %r8d
 295b002:      	movq	0x30(%rax), %rdx
 295b006:      	movl	%r8d, %ecx
 295b009:      	shlq	$0x4, %rcx
 295b00d:      	cmpw	$0x5e, (%rdx,%rcx)
 295b012:      	je	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295b018:      	movq	0x48(%rax), %rsi
 295b01c:      	movq	%rsi, 0x30(%rsp)
 295b021:      	testq	%rsi, %rsi
 295b024:      	je	0x295b041 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3181>
 295b026:      	leaq	0x30(%rsp), %rdi
 295b02b:      	movl	$0x1, %edx
 295b030:      	movq	%rax, %rbx
 295b033:      	movl	%r8d, %ebp
 295b036:      	callq	0x3bd6a90 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295b03b:      	movl	%ebp, %r8d
 295b03e:      	movq	%rbx, %rax
 295b041:      	movl	0x44(%rax), %ecx
 295b044:      	movl	%ecx, 0x38(%rsp)
 295b048:      	movq	0x3b0(%r15), %rcx
 295b04f:      	testq	%rcx, %rcx
 295b052:      	je	0x295b05a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x319a>
 295b054:      	movl	0x8(%rcx), %r9d
 295b058:      	jmp	0x295b05d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x319d>
 295b05a:      	xorl	%r9d, %r9d
 295b05d:      	movq	%rax, 0xa0(%rsp)
 295b065:      	movl	%r8d, 0xa8(%rsp)
 295b06d:      	subq	$0x10, %rsp
 295b071:      	movdqu	0xb0(%rsp), %xmm0
 295b07a:      	movdqu	%xmm0, (%rsp)
 295b07f:      	leaq	0x40(%rsp), %rdx
 295b084:      	movq	%r15, %rdi
 295b087:      	movl	$0xf3, %esi
 295b08c:      	movl	$0x5e, %ecx
 295b091:      	jmp	0x295a4c3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2603>
 295b096:      	movl	(%r14), %eax
 295b099:      	testl	%eax, %eax
 295b09b:      	sets	%cl
 295b09e:      	cmpl	$0x1, %eax
 295b0a1:      	sete	%dl
 295b0a4:      	orb	%cl, %dl
 295b0a6:      	jne	0x295b0e7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3227>
 295b0a8:      	xorl	%ecx, %ecx
 295b0aa:      	cmpl	$0x4, %eax
 295b0ad:      	setb	%cl
 295b0b0:      	movq	%rbp, %rsi
 295b0b3:      	cmovbq	%r13, %rsi
 295b0b7:      	movq	0x28(%rsp), %rdx
 295b0bc:      	cmovbl	%r8d, %edx
 295b0c0:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b0c5:      	subq	$0x8, %rsp
 295b0c9:      	movl	$0x4, %edi
 295b0ce:      	movq	%r13, %rcx
 295b0d1:      	pushq	$0x1
 295b0d3:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b0d8:      	movl	%ebx, %r8d
 295b0db:      	addq	$0x10, %rsp
 295b0df:      	testb	%al, %al
 295b0e1:      	je	0x295b575 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36b5>
 295b0e7:      	movl	0x4(%r14), %eax
 295b0eb:      	testl	%eax, %eax
 295b0ed:      	sets	%cl
 295b0f0:      	cmpl	$0x1, %eax
 295b0f3:      	sete	%dl
 295b0f6:      	orb	%cl, %dl
 295b0f8:      	jne	0x295b139 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3279>
 295b0fa:      	xorl	%ecx, %ecx
 295b0fc:      	cmpl	$0x4, %eax
 295b0ff:      	setb	%cl
 295b102:      	movq	%rbp, %rsi
 295b105:      	cmovbq	%r13, %rsi
 295b109:      	movq	0x28(%rsp), %rdx
 295b10e:      	cmovbl	%r8d, %edx
 295b112:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b117:      	subq	$0x8, %rsp
 295b11b:      	movl	$0x4, %edi
 295b120:      	movq	%r13, %rcx
 295b123:      	pushq	$0x1
 295b125:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b12a:      	movl	%ebx, %r8d
 295b12d:      	addq	$0x10, %rsp
 295b131:      	testb	%al, %al
 295b133:      	je	0x295b575 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36b5>
 295b139:      	movl	0x8(%r14), %eax
 295b13d:      	testl	%eax, %eax
 295b13f:      	sets	%cl
 295b142:      	cmpl	$0x3, %eax
 295b145:      	sete	%dl
 295b148:      	orb	%cl, %dl
 295b14a:      	jne	0x295b18b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x32cb>
 295b14c:      	xorl	%ecx, %ecx
 295b14e:      	cmpl	$0x4, %eax
 295b151:      	setb	%cl
 295b154:      	movq	%rbp, %rsi
 295b157:      	cmovbq	%r13, %rsi
 295b15b:      	movq	0x28(%rsp), %rdx
 295b160:      	cmovbl	%r8d, %edx
 295b164:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b169:      	subq	$0x8, %rsp
 295b16d:      	movl	$0x4, %edi
 295b172:      	movq	%r13, %rcx
 295b175:      	pushq	$0x3
 295b177:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b17c:      	movl	%ebx, %r8d
 295b17f:      	addq	$0x10, %rsp
 295b183:      	testb	%al, %al
 295b185:      	je	0x295b575 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36b5>
 295b18b:      	movl	0xc(%r14), %eax
 295b18f:      	testl	%eax, %eax
 295b191:      	sets	%cl
 295b194:      	cmpl	$0x3, %eax
 295b197:      	sete	%dl
 295b19a:      	orb	%cl, %dl
 295b19c:      	jne	0x295b1dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x331d>
 295b19e:      	xorl	%ecx, %ecx
 295b1a0:      	cmpl	$0x4, %eax
 295b1a3:      	setb	%cl
 295b1a6:      	movq	%rbp, %rsi
 295b1a9:      	cmovbq	%r13, %rsi
 295b1ad:      	movq	0x28(%rsp), %rdx
 295b1b2:      	cmovbl	%r8d, %edx
 295b1b6:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b1bb:      	subq	$0x8, %rsp
 295b1bf:      	movl	$0x4, %edi
 295b1c4:      	movq	%r13, %rcx
 295b1c7:      	pushq	$0x3
 295b1c9:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b1ce:      	movl	%ebx, %r8d
 295b1d1:      	addq	$0x10, %rsp
 295b1d5:      	testb	%al, %al
 295b1d7:      	je	0x295b575 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36b5>
 295b1dd:      	movq	%r13, 0xa0(%rsp)
 295b1e5:      	movl	%r8d, 0xa8(%rsp)
 295b1ed:      	movq	0x230(%rsp), %rdi
 295b1f5:      	movq	0x3b0(%rdi), %rax
 295b1fc:      	testq	%rax, %rax
 295b1ff:      	je	0x295baec <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c2c>
 295b205:      	movl	0x8(%rax), %r9d
 295b209:      	jmp	0x295baef <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c2f>
 295b20e:      	movq	%rdi, %r14
 295b211:      	movq	0x60(%rsp), %rax
 295b216:      	movl	0x68(%rsp), %ecx
 295b21a:      	movq	%r12, %r8
 295b21d:      	movq	%rbp, %r12
 295b220:      	movq	%rbp, 0x80(%rsp)
 295b228:      	movl	%r11d, %ebp
 295b22b:      	movl	%r11d, 0x88(%rsp)
 295b233:      	movq	%rax, %r13
 295b236:      	movq	%rax, 0x130(%rsp)
 295b23e:      	movl	%ecx, 0x18(%rsp)
 295b242:      	movl	%ecx, 0x138(%rsp)
 295b249:      	movl	$0x0, 0x188(%rsp)
 295b254:      	subq	$0x8, %rsp
 295b258:      	leaq	0x88(%rsp), %rdi
 295b260:      	leaq	0x138(%rsp), %rsi
 295b268:      	leaq	0x190(%rsp), %rdx
 295b270:      	movq	%r10, %rcx
 295b273:      	movq	%r8, 0x60(%rsp)
 295b278:      	movq	0x28(%rsp), %rbx
 295b27d:      	movq	%rbx, %r9
 295b280:      	pushq	%r15
 295b282:      	callq	0x2971030 <_ZL22matchShuffleAsInsertPSRN4llvm7SDValueES1_RjRKNS_5APIntENS_8ArrayRefIiEERNS_12SelectionDAGE>
 295b287:      	addq	$0x10, %rsp
 295b28b:      	testb	%al, %al
 295b28d:      	je	0x295b355 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3495>
 295b293:      	movups	0x80(%rsp), %xmm0
 295b29b:      	movaps	%xmm0, 0x70(%rsp)
 295b2a0:      	movups	0x130(%rsp), %xmm0
 295b2a8:      	movaps	%xmm0, 0x30(%rsp)
 295b2ad:      	movl	0x188(%rsp), %esi
 295b2b4:      	subq	$0x8, %rsp
 295b2b8:      	xorl	%ebx, %ebx
 295b2ba:      	movq	%r15, %rdi
 295b2bd:      	movq	%r14, %rdx
 295b2c0:      	movl	$0x5, %ecx
 295b2c5:      	xorl	%r8d, %r8d
 295b2c8:      	movl	$0x1, %r9d
 295b2ce:      	pushq	$0x0
 295b2d0:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b2d5:      	addq	$0x10, %rsp
 295b2d9:      	movq	%rax, 0xa0(%rsp)
 295b2e1:      	movl	%edx, 0xa8(%rsp)
 295b2e8:      	movq	0x3b0(%r15), %rax
 295b2ef:      	testq	%rax, %rax
 295b2f2:      	je	0x295b2f7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3437>
 295b2f4:      	movl	0x8(%rax), %ebx
 295b2f7:      	subq	$0x30, %rsp
 295b2fb:      	movups	0xd0(%rsp), %xmm0
 295b303:      	movups	%xmm0, 0x20(%rsp)
 295b308:      	movaps	0x60(%rsp), %xmm0
 295b30d:      	movups	%xmm0, 0x10(%rsp)
 295b312:      	movdqa	0xa0(%rsp), %xmm0
 295b31b:      	movdqu	%xmm0, (%rsp)
 295b320:      	movq	0x260(%rsp), %r15
 295b328:      	movq	%r15, %rdi
 295b32b:      	movl	$0x232, %esi            # imm = 0x232
 295b330:      	movq	%r14, %rdx
 295b333:      	movl	$0x84, %ecx
 295b338:      	xorl	%r8d, %r8d
 295b33b:      	movl	%ebx, %r9d
 295b33e:      	callq	0x5e2ad10 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295b343:      	addq	$0x30, %rsp
 295b347:      	testq	%rax, %rax
 295b34a:      	movq	0x20(%rsp), %rbx
 295b34f:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295b355:      	movq	%r14, %rdi
 295b358:      	movl	$0x84, %esi
 295b35d:      	movq	%r12, %rdx
 295b360:      	movl	%ebp, %ecx
 295b362:      	movq	%r13, %r8
 295b365:      	movl	0x18(%rsp), %r9d
 295b36a:      	pushq	$0x0
 295b36c:      	pushq	%r15
 295b36e:      	pushq	%rbx
 295b36f:      	movq	0x70(%rsp), %rbx
 295b374:      	pushq	%rbx
 295b375:      	callq	0x296c420 <_ZL29lowerShuffleAsBlendAndPermuteRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGEb>
 295b37a:      	addq	$0x20, %rsp
 295b37e:      	testq	%rax, %rax
 295b381:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295b387:      	movq	0x228(%rsp), %rax
 295b38f:      	movl	0x148(%rax), %eax
 295b395:      	movq	%r14, %rdi
 295b398:      	movl	%ebp, %r11d
 295b39b:      	movq	%r12, %rbp
 295b39e:      	movq	%rbx, %r12
 295b3a1:      	movq	%r13, %r8
 295b3a4:      	cmpl	$0x2, %eax
 295b3a7:      	jge	0x295a9e9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b29>
 295b3ad:      	movl	0x68(%rsp), %ebx
 295b3b1:      	cmpq	$0x4, 0x20(%rsp)
 295b3b7:      	jne	0x295a9ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b2d>
 295b3bd:      	movq	%rdi, (%rsp)
 295b3c1:      	movl	(%r12), %eax
 295b3c5:      	testl	%eax, %eax
 295b3c7:      	movq	%r8, %r14
 295b3ca:      	jle	0x295b41d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x355d>
 295b3cc:      	xorl	%ecx, %ecx
 295b3ce:      	cmpl	$0x4, %eax
 295b3d1:      	setb	%cl
 295b3d4:      	movq	%r8, %rsi
 295b3d7:      	cmovbq	%rbp, %rsi
 295b3db:      	movl	%ebx, %edx
 295b3dd:      	cmovbl	%r11d, %edx
 295b3e1:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b3e6:      	subq	$0x8, %rsp
 295b3ea:      	movl	$0x4, %edi
 295b3ef:      	movq	%rbp, %rcx
 295b3f2:      	movl	%r11d, %r8d
 295b3f5:      	pushq	$0x0
 295b3f7:      	movq	%r12, %r13
 295b3fa:      	movq	%rbp, %r12
 295b3fd:      	movl	%r11d, %ebp
 295b400:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b405:      	movq	%r14, %r8
 295b408:      	movl	%ebp, %r11d
 295b40b:      	movq	%r12, %rbp
 295b40e:      	movq	%r13, %r12
 295b411:      	addq	$0x10, %rsp
 295b415:      	testb	%al, %al
 295b417:      	je	0x295b8dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a1d>
 295b41d:      	movl	0x4(%r12), %eax
 295b422:      	testl	%eax, %eax
 295b424:      	sets	%cl
 295b427:      	cmpl	$0x1, %eax
 295b42a:      	sete	%dl
 295b42d:      	orb	%cl, %dl
 295b42f:      	jne	0x295b482 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x35c2>
 295b431:      	xorl	%ecx, %ecx
 295b433:      	cmpl	$0x4, %eax
 295b436:      	setb	%cl
 295b439:      	movq	%r8, %rsi
 295b43c:      	cmovbq	%rbp, %rsi
 295b440:      	movl	%ebx, %edx
 295b442:      	cmovbl	%r11d, %edx
 295b446:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b44b:      	subq	$0x8, %rsp
 295b44f:      	movl	$0x4, %edi
 295b454:      	movq	%rbp, %rcx
 295b457:      	movl	%r11d, %r8d
 295b45a:      	pushq	$0x1
 295b45c:      	movq	%r12, %r13
 295b45f:      	movq	%rbp, %r12
 295b462:      	movl	%r11d, %ebp
 295b465:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b46a:      	movq	%r14, %r8
 295b46d:      	movl	%ebp, %r11d
 295b470:      	movq	%r12, %rbp
 295b473:      	movq	%r13, %r12
 295b476:      	addq	$0x10, %rsp
 295b47a:      	testb	%al, %al
 295b47c:      	je	0x295b8dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a1d>
 295b482:      	movl	0x8(%r12), %eax
 295b487:      	testl	%eax, %eax
 295b489:      	sets	%cl
 295b48c:      	cmpl	$0x4, %eax
 295b48f:      	sete	%dl
 295b492:      	orb	%cl, %dl
 295b494:      	jne	0x295b4e7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3627>
 295b496:      	xorl	%ecx, %ecx
 295b498:      	cmpl	$0x4, %eax
 295b49b:      	setb	%cl
 295b49e:      	movq	%r8, %rsi
 295b4a1:      	cmovbq	%rbp, %rsi
 295b4a5:      	movl	%ebx, %edx
 295b4a7:      	cmovbl	%r11d, %edx
 295b4ab:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b4b0:      	subq	$0x8, %rsp
 295b4b4:      	movl	$0x4, %edi
 295b4b9:      	movq	%r8, %rcx
 295b4bc:      	movl	%ebx, %r8d
 295b4bf:      	pushq	$0x0
 295b4c1:      	movq	%r12, %r13
 295b4c4:      	movq	%rbp, %r12
 295b4c7:      	movl	%r11d, %ebp
 295b4ca:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b4cf:      	movq	%r14, %r8
 295b4d2:      	movl	%ebp, %r11d
 295b4d5:      	movq	%r12, %rbp
 295b4d8:      	movq	%r13, %r12
 295b4db:      	addq	$0x10, %rsp
 295b4df:      	testb	%al, %al
 295b4e1:      	je	0x295b8dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a1d>
 295b4e7:      	movl	0xc(%r12), %eax
 295b4ec:      	testl	%eax, %eax
 295b4ee:      	sets	%cl
 295b4f1:      	cmpl	$0x5, %eax
 295b4f4:      	sete	%dl
 295b4f7:      	orb	%cl, %dl
 295b4f9:      	jne	0x295b54c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x368c>
 295b4fb:      	xorl	%ecx, %ecx
 295b4fd:      	cmpl	$0x4, %eax
 295b500:      	setb	%cl
 295b503:      	movq	%r8, %rsi
 295b506:      	cmovbq	%rbp, %rsi
 295b50a:      	movl	%ebx, %edx
 295b50c:      	cmovbl	%r11d, %edx
 295b510:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b515:      	subq	$0x8, %rsp
 295b519:      	movl	$0x4, %edi
 295b51e:      	movq	%r8, %rcx
 295b521:      	movl	%ebx, %r8d
 295b524:      	pushq	$0x1
 295b526:      	movq	%r12, %r13
 295b529:      	movq	%rbp, %r12
 295b52c:      	movl	%r11d, %ebp
 295b52f:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b534:      	movq	%r14, %r8
 295b537:      	movl	%ebp, %r11d
 295b53a:      	movq	%r12, %rbp
 295b53d:      	movq	%r13, %r12
 295b540:      	addq	$0x10, %rsp
 295b544:      	testb	%al, %al
 295b546:      	je	0x295b8dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a1d>
 295b54c:      	movq	%rbp, 0xa0(%rsp)
 295b554:      	movl	%r11d, 0xa8(%rsp)
 295b55c:      	movq	0x3b0(%r15), %rax
 295b563:      	testq	%rax, %rax
 295b566:      	je	0x295bb42 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c82>
 295b56c:      	movl	0x8(%rax), %r9d
 295b570:      	jmp	0x295bb45 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c85>
 295b575:      	movl	0x148(%r15), %eax
 295b57c:      	cmpl	$0x7, %eax
 295b57f:      	jl	0x295b626 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3766>
 295b585:      	movq	%r14, %rdi
 295b588:      	movq	0x20(%rsp), %rsi
 295b58d:      	movl	%r8d, %ebp
 295b590:      	callq	0x2962860 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295b595:      	movl	%eax, %esi
 295b597:      	subq	$0x8, %rsp
 295b59b:      	xorl	%ebx, %ebx
 295b59d:      	movq	0x238(%rsp), %r14
 295b5a5:      	movq	%r14, %rdi
 295b5a8:      	movq	0x8(%rsp), %rdx
 295b5ad:      	movl	$0x5, %ecx
 295b5b2:      	xorl	%r8d, %r8d
 295b5b5:      	movl	$0x1, %r9d
 295b5bb:      	pushq	$0x0
 295b5bd:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b5c2:      	addq	$0x10, %rsp
 295b5c6:      	movq	%rax, 0xa0(%rsp)
 295b5ce:      	movl	%edx, 0xa8(%rsp)
 295b5d5:      	movq	%r12, 0x30(%rsp)
 295b5da:      	movl	%ebp, 0x38(%rsp)
 295b5de:      	movq	0x3b0(%r14), %rax
 295b5e5:      	testq	%rax, %rax
 295b5e8:      	je	0x295b5ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x372d>
 295b5ea:      	movl	0x8(%rax), %ebx
 295b5ed:      	subq	$0x20, %rsp
 295b5f1:      	movups	0xc0(%rsp), %xmm0
 295b5f9:      	movups	%xmm0, 0x10(%rsp)
 295b5fe:      	movdqu	0x50(%rsp), %xmm0
 295b604:      	movdqu	%xmm0, (%rsp)
 295b609:      	movq	%r14, %rdi
 295b60c:      	movl	$0x2cb, %esi            # imm = 0x2CB
 295b611:      	movq	0x20(%rsp), %rdx
 295b616:      	movl	$0x84, %ecx
 295b61b:      	xorl	%r8d, %r8d
 295b61e:      	movl	%ebx, %r9d
 295b621:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295b626:      	cmpl	$0x1, %eax
 295b629:      	jg	0x295b81d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x395d>
 295b62f:      	cmpq	$0x4, 0x20(%rsp)
 295b635:      	movq	%r12, %r13
 295b638:      	movq	0x28(%rsp), %r15
 295b63d:      	jne	0x295b7a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38e3>
 295b643:      	movl	(%r14), %eax
 295b646:      	testl	%eax, %eax
 295b648:      	jle	0x295b687 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x37c7>
 295b64a:      	xorl	%ecx, %ecx
 295b64c:      	cmpl	$0x4, %eax
 295b64f:      	setb	%cl
 295b652:      	movq	%rbp, %rsi
 295b655:      	cmovbq	%r13, %rsi
 295b659:      	movl	%r15d, %edx
 295b65c:      	cmovbl	%r8d, %edx
 295b660:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b665:      	subq	$0x8, %rsp
 295b669:      	movl	$0x4, %edi
 295b66e:      	movq	%r13, %rcx
 295b671:      	pushq	$0x0
 295b673:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b678:      	movl	%ebx, %r8d
 295b67b:      	addq	$0x10, %rsp
 295b67f:      	testb	%al, %al
 295b681:      	je	0x295b7a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38e3>
 295b687:      	movl	0x4(%r14), %eax
 295b68b:      	testl	%eax, %eax
 295b68d:      	sets	%cl
 295b690:      	cmpl	$0x1, %eax
 295b693:      	sete	%dl
 295b696:      	orb	%cl, %dl
 295b698:      	jne	0x295b6d7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3817>
 295b69a:      	xorl	%ecx, %ecx
 295b69c:      	cmpl	$0x4, %eax
 295b69f:      	setb	%cl
 295b6a2:      	movq	%rbp, %rsi
 295b6a5:      	cmovbq	%r13, %rsi
 295b6a9:      	movl	%r15d, %edx
 295b6ac:      	cmovbl	%r8d, %edx
 295b6b0:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b6b5:      	subq	$0x8, %rsp
 295b6b9:      	movl	$0x4, %edi
 295b6be:      	movq	%r13, %rcx
 295b6c1:      	pushq	$0x1
 295b6c3:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b6c8:      	movl	%ebx, %r8d
 295b6cb:      	addq	$0x10, %rsp
 295b6cf:      	testb	%al, %al
 295b6d1:      	je	0x295b7a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38e3>
 295b6d7:      	movl	0x8(%r14), %eax
 295b6db:      	testl	%eax, %eax
 295b6dd:      	jle	0x295b71c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x385c>
 295b6df:      	xorl	%ecx, %ecx
 295b6e1:      	cmpl	$0x4, %eax
 295b6e4:      	setb	%cl
 295b6e7:      	movq	%rbp, %rsi
 295b6ea:      	cmovbq	%r13, %rsi
 295b6ee:      	movl	%r15d, %edx
 295b6f1:      	cmovbl	%r8d, %edx
 295b6f5:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b6fa:      	subq	$0x8, %rsp
 295b6fe:      	movl	$0x4, %edi
 295b703:      	movq	%r13, %rcx
 295b706:      	pushq	$0x0
 295b708:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b70d:      	movl	%ebx, %r8d
 295b710:      	addq	$0x10, %rsp
 295b714:      	testb	%al, %al
 295b716:      	je	0x295b7a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38e3>
 295b71c:      	movl	0xc(%r14), %eax
 295b720:      	testl	%eax, %eax
 295b722:      	sets	%cl
 295b725:      	cmpl	$0x1, %eax
 295b728:      	sete	%dl
 295b72b:      	orb	%cl, %dl
 295b72d:      	jne	0x295b768 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38a8>
 295b72f:      	xorl	%ecx, %ecx
 295b731:      	cmpl	$0x4, %eax
 295b734:      	setb	%cl
 295b737:      	movq	%rbp, %rsi
 295b73a:      	cmovbq	%r13, %rsi
 295b73e:      	movl	%r15d, %edx
 295b741:      	cmovbl	%r8d, %edx
 295b745:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b74a:      	subq	$0x8, %rsp
 295b74e:      	movl	$0x4, %edi
 295b753:      	movq	%r13, %rcx
 295b756:      	pushq	$0x1
 295b758:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b75d:      	movl	%ebx, %r8d
 295b760:      	addq	$0x10, %rsp
 295b764:      	testb	%al, %al
 295b766:      	je	0x295b7a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38e3>
 295b768:      	movq	%r13, 0xa0(%rsp)
 295b770:      	movl	%r8d, 0xa8(%rsp)
 295b778:      	movq	%r13, 0x30(%rsp)
 295b77d:      	movl	%r8d, 0x38(%rsp)
 295b782:      	movq	0x230(%rsp), %rdi
 295b78a:      	movq	0x3b0(%rdi), %rax
 295b791:      	testq	%rax, %rax
 295b794:      	je	0x295bb21 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c61>
 295b79a:      	movl	0x8(%rax), %r9d
 295b79e:      	jmp	0x295bb24 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c64>
 295b7a3:      	movdqa	-0x1b36f4b(%rip), %xmm0 # 0xe24860 <.LCPI989_7>
 295b7ab:      	movdqa	%xmm0, 0xa0(%rsp)
 295b7b4:      	leaq	0xa0(%rsp), %rdx
 295b7bc:      	movl	$0x4, %ecx
 295b7c1:      	movq	%r14, %rdi
 295b7c4:      	movq	0x20(%rsp), %rsi
 295b7c9:      	movl	%r8d, %r9d
 295b7cc:      	movq	%r13, %r8
 295b7cf:      	pushq	%r15
 295b7d1:      	pushq	%rbp
 295b7d2:      	callq	0x2961a60 <_ZL19isShuffleEquivalentN4llvm8ArrayRefIiEES1_NS_7SDValueES2_>
 295b7d7:      	movl	%ebx, %r8d
 295b7da:      	addq	$0x10, %rsp
 295b7de:      	testb	%al, %al
 295b7e0:      	je	0x295b81d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x395d>
 295b7e2:      	movq	%r12, 0xa0(%rsp)
 295b7ea:      	movl	%r8d, 0xa8(%rsp)
 295b7f2:      	movq	%r12, 0x30(%rsp)
 295b7f7:      	movl	%r8d, 0x38(%rsp)
 295b7fc:      	movq	0x230(%rsp), %rdi
 295b804:      	movq	0x3b0(%rdi), %rax
 295b80b:      	testq	%rax, %rax
 295b80e:      	je	0x295ba9e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bde>
 295b814:      	movl	0x8(%rax), %r9d
 295b818:      	jmp	0x295baa1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3be1>
 295b81d:      	movq	%r14, %rdi
 295b820:      	movq	0x20(%rsp), %rsi
 295b825:      	movl	%r8d, %ebp
 295b828:      	callq	0x2962860 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295b82d:      	movl	%eax, %esi
 295b82f:      	subq	$0x8, %rsp
 295b833:      	xorl	%ebx, %ebx
 295b835:      	movq	0x238(%rsp), %r14
 295b83d:      	movq	%r14, %rdi
 295b840:      	movq	0x8(%rsp), %rdx
 295b845:      	movl	$0x5, %ecx
 295b84a:      	xorl	%r8d, %r8d
 295b84d:      	movl	$0x1, %r9d
 295b853:      	pushq	$0x0
 295b855:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b85a:      	addq	$0x10, %rsp
 295b85e:      	movq	%rax, 0xa0(%rsp)
 295b866:      	movl	%edx, 0xa8(%rsp)
 295b86d:      	movq	%r12, 0x30(%rsp)
 295b872:      	movl	%ebp, 0x38(%rsp)
 295b876:      	movq	%r12, 0x70(%rsp)
 295b87b:      	movl	%ebp, 0x78(%rsp)
 295b87f:      	movq	0x3b0(%r14), %rax
 295b886:      	testq	%rax, %rax
 295b889:      	je	0x295b88e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x39ce>
 295b88b:      	movl	0x8(%rax), %ebx
 295b88e:      	subq	$0x30, %rsp
 295b892:      	movups	0xd0(%rsp), %xmm0
 295b89a:      	movups	%xmm0, 0x20(%rsp)
 295b89f:      	movups	0x60(%rsp), %xmm0
 295b8a4:      	movups	%xmm0, 0x10(%rsp)
 295b8a9:      	movdqu	0xa0(%rsp), %xmm0
 295b8b2:      	movdqu	%xmm0, (%rsp)
 295b8b7:      	movq	%r14, %rdi
 295b8ba:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295b8bf:      	movq	0x30(%rsp), %rdx
 295b8c4:      	movl	$0x84, %ecx
 295b8c9:      	xorl	%r8d, %r8d
 295b8cc:      	movl	%ebx, %r9d
 295b8cf:      	callq	0x5e2ad10 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295b8d4:      	addq	$0x30, %rsp
 295b8d8:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295b8dd:      	movl	(%r12), %eax
 295b8e1:      	testl	%eax, %eax
 295b8e3:      	sets	%cl
 295b8e6:      	cmpl	$0x2, %eax
 295b8e9:      	sete	%dl
 295b8ec:      	orb	%cl, %dl
 295b8ee:      	jne	0x295b941 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a81>
 295b8f0:      	xorl	%ecx, %ecx
 295b8f2:      	cmpl	$0x4, %eax
 295b8f5:      	setb	%cl
 295b8f8:      	movq	%r8, %rsi
 295b8fb:      	cmovbq	%rbp, %rsi
 295b8ff:      	movl	%ebx, %edx
 295b901:      	cmovbl	%r11d, %edx
 295b905:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b90a:      	subq	$0x8, %rsp
 295b90e:      	movl	$0x4, %edi
 295b913:      	movq	%rbp, %rcx
 295b916:      	movl	%r11d, %r8d
 295b919:      	pushq	$0x2
 295b91b:      	movq	%r12, %r13
 295b91e:      	movq	%rbp, %r12
 295b921:      	movl	%r11d, %ebp
 295b924:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b929:      	movq	%r14, %r8
 295b92c:      	movl	%ebp, %r11d
 295b92f:      	movq	%r12, %rbp
 295b932:      	movq	%r13, %r12
 295b935:      	addq	$0x10, %rsp
 295b939:      	testb	%al, %al
 295b93b:      	je	0x295bac7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c07>
 295b941:      	movl	0x4(%r12), %eax
 295b946:      	testl	%eax, %eax
 295b948:      	sets	%cl
 295b94b:      	cmpl	$0x3, %eax
 295b94e:      	sete	%dl
 295b951:      	orb	%cl, %dl
 295b953:      	jne	0x295b9a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ae6>
 295b955:      	xorl	%ecx, %ecx
 295b957:      	cmpl	$0x4, %eax
 295b95a:      	setb	%cl
 295b95d:      	movq	%r8, %rsi
 295b960:      	cmovbq	%rbp, %rsi
 295b964:      	movl	%ebx, %edx
 295b966:      	cmovbl	%r11d, %edx
 295b96a:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b96f:      	subq	$0x8, %rsp
 295b973:      	movl	$0x4, %edi
 295b978:      	movq	%rbp, %rcx
 295b97b:      	movl	%r11d, %r8d
 295b97e:      	pushq	$0x3
 295b980:      	movq	%r12, %r13
 295b983:      	movq	%rbp, %r12
 295b986:      	movl	%r11d, %ebp
 295b989:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b98e:      	movq	%r14, %r8
 295b991:      	movl	%ebp, %r11d
 295b994:      	movq	%r12, %rbp
 295b997:      	movq	%r13, %r12
 295b99a:      	addq	$0x10, %rsp
 295b99e:      	testb	%al, %al
 295b9a0:      	je	0x295bac7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c07>
 295b9a6:      	movl	0x8(%r12), %eax
 295b9ab:      	testl	%eax, %eax
 295b9ad:      	sets	%cl
 295b9b0:      	cmpl	$0x6, %eax
 295b9b3:      	sete	%dl
 295b9b6:      	orb	%cl, %dl
 295b9b8:      	jne	0x295ba0b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3b4b>
 295b9ba:      	xorl	%ecx, %ecx
 295b9bc:      	cmpl	$0x4, %eax
 295b9bf:      	setb	%cl
 295b9c2:      	movq	%r8, %rsi
 295b9c5:      	cmovbq	%rbp, %rsi
 295b9c9:      	movl	%ebx, %edx
 295b9cb:      	cmovbl	%r11d, %edx
 295b9cf:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b9d4:      	subq	$0x8, %rsp
 295b9d8:      	movl	$0x4, %edi
 295b9dd:      	movq	%r8, %rcx
 295b9e0:      	movl	%ebx, %r8d
 295b9e3:      	pushq	$0x2
 295b9e5:      	movq	%r12, %r13
 295b9e8:      	movq	%rbp, %r12
 295b9eb:      	movl	%r11d, %ebp
 295b9ee:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b9f3:      	movq	%r14, %r8
 295b9f6:      	movl	%ebp, %r11d
 295b9f9:      	movq	%r12, %rbp
 295b9fc:      	movq	%r13, %r12
 295b9ff:      	addq	$0x10, %rsp
 295ba03:      	testb	%al, %al
 295ba05:      	je	0x295bac7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c07>
 295ba0b:      	movl	0xc(%r12), %eax
 295ba10:      	testl	%eax, %eax
 295ba12:      	sets	%cl
 295ba15:      	cmpl	$0x7, %eax
 295ba18:      	sete	%dl
 295ba1b:      	orb	%cl, %dl
 295ba1d:      	jne	0x295ba75 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bb5>
 295ba1f:      	xorl	%ecx, %ecx
 295ba21:      	cmpl	$0x4, %eax
 295ba24:      	setb	%cl
 295ba27:      	movq	%r8, %rsi
 295ba2a:      	cmovbq	%rbp, %rsi
 295ba2e:      	movl	%ebx, %edx
 295ba30:      	cmovbl	%r11d, %edx
 295ba34:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ba39:      	subq	$0x8, %rsp
 295ba3d:      	movl	$0x4, %edi
 295ba42:      	movq	%r8, %rcx
 295ba45:      	movl	%ebx, %r8d
 295ba48:      	pushq	$0x3
 295ba4a:      	movq	%r12, %r13
 295ba4d:      	movq	%rbp, %r12
 295ba50:      	movl	%r11d, %ebp
 295ba53:      	callq	0x2961b30 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ba58:      	movq	%r14, %r8
 295ba5b:      	movl	%ebp, %r11d
 295ba5e:      	movq	%r12, %rbp
 295ba61:      	movq	%r13, %r12
 295ba64:      	movq	0x10(%rsp), %rdi
 295ba69:      	addq	$0x10, %rsp
 295ba6d:      	testb	%al, %al
 295ba6f:      	je	0x295a9ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b2d>
 295ba75:      	movq	%rbp, 0xa0(%rsp)
 295ba7d:      	movl	%r11d, 0xa8(%rsp)
 295ba85:      	movq	0x3b0(%r15), %rax
 295ba8c:      	testq	%rax, %rax
 295ba8f:      	je	0x295bcd0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e10>
 295ba95:      	movl	0x8(%rax), %r9d
 295ba99:      	jmp	0x295bcd3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e13>
 295ba9e:      	xorl	%r9d, %r9d
 295baa1:      	subq	$0x20, %rsp
 295baa5:      	movups	0xc0(%rsp), %xmm0
 295baad:      	movups	%xmm0, 0x10(%rsp)
 295bab2:      	movdqu	0x50(%rsp), %xmm0
 295bab8:      	movdqu	%xmm0, (%rsp)
 295babd:      	movl	$0x2c4, %esi            # imm = 0x2C4
 295bac2:      	jmp	0x295bb6f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3caf>
 295bac7:      	movq	(%rsp), %rdi
 295bacb:      	jmp	0x295a9ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b2d>
 295bad0:      	xorl	%r9d, %r9d
 295bad3:      	subq	$0x10, %rsp
 295bad7:      	movdqu	0xb0(%rsp), %xmm0
 295bae0:      	movdqu	%xmm0, (%rsp)
 295bae5:      	movl	$0x2c2, %esi            # imm = 0x2C2
 295baea:      	jmp	0x295bb06 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c46>
 295baec:      	xorl	%r9d, %r9d
 295baef:      	subq	$0x10, %rsp
 295baf3:      	movdqu	0xb0(%rsp), %xmm0
 295bafc:      	movdqu	%xmm0, (%rsp)
 295bb01:      	movl	$0x2c1, %esi            # imm = 0x2C1
 295bb06:      	movq	0x10(%rsp), %rdx
 295bb0b:      	movl	$0x84, %ecx
 295bb10:      	xorl	%r8d, %r8d
 295bb13:      	callq	0x5e1f040 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295bb18:      	addq	$0x10, %rsp
 295bb1c:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bb21:      	xorl	%r9d, %r9d
 295bb24:      	subq	$0x20, %rsp
 295bb28:      	movups	0xc0(%rsp), %xmm0
 295bb30:      	movups	%xmm0, 0x10(%rsp)
 295bb35:      	movdqu	0x50(%rsp), %xmm0
 295bb3b:      	movdqu	%xmm0, (%rsp)
 295bb40:      	jmp	0x295bb6a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3caa>
 295bb42:      	xorl	%r9d, %r9d
 295bb45:      	subq	$0x20, %rsp
 295bb49:      	leaq	0x230(%rsp), %rax
 295bb51:      	movups	(%rax), %xmm0
 295bb54:      	movups	%xmm0, 0x10(%rsp)
 295bb59:      	movdqu	0xc0(%rsp), %xmm0
 295bb62:      	movdqu	%xmm0, (%rsp)
 295bb67:      	movq	%r15, %rdi
 295bb6a:      	movl	$0x2c3, %esi            # imm = 0x2C3
 295bb6f:      	movq	0x20(%rsp), %rdx
 295bb74:      	movl	$0x84, %ecx
 295bb79:      	xorl	%r8d, %r8d
 295bb7c:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295bb81:      	movq	%rdi, %r13
 295bb84:      	movl	$0x30, %esi
 295bb89:      	movq	%rbp, %rdx
 295bb8c:      	movq	0x230(%rsp), %r15
 295bb94:      	pushq	%r15
 295bb96:      	pushq	%r14
 295bb98:      	pushq	%rbx
 295bb99:      	pushq	%r12
 295bb9b:      	movq	%rbx, %r15
 295bb9e:      	movq	%r12, %rbx
 295bba1:      	movl	%ecx, %r12d
 295bba4:      	callq	0x2954240 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295bba9:      	addq	$0x20, %rsp
 295bbad:      	testq	%rax, %rax
 295bbb0:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bbb6:      	movl	0x148(%r14), %eax
 295bbbd:      	movzbl	0x1db(%r14), %r10d
 295bbc5:      	subq	$0x8, %rsp
 295bbc9:      	movq	%r13, %rdi
 295bbcc:      	movl	$0x30, %esi
 295bbd1:      	movq	%rbp, %r13
 295bbd4:      	movq	%rbp, %rdx
 295bbd7:      	movl	%r12d, %ecx
 295bbda:      	movq	%rbx, %r12
 295bbdd:      	movq	%rbx, %r8
 295bbe0:      	movq	%r15, %rbx
 295bbe3:      	movq	%r15, %r9
 295bbe6:      	pushq	0x238(%rsp)
 295bbed:      	pushq	%r10
 295bbef:      	pushq	%rax
 295bbf0:      	callq	0x296ff80 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295bbf5:      	addq	$0x20, %rsp
 295bbf9:      	testq	%rax, %rax
 295bbfc:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bc02:      	subq	$0x8, %rsp
 295bc06:      	movq	0x8(%rsp), %rdi
 295bc0b:      	movl	$0x30, %esi
 295bc10:      	movq	%r13, %rdx
 295bc13:      	movl	0x14(%rsp), %ecx
 295bc17:      	movq	0x20(%rsp), %r8
 295bc1c:      	movl	0x30(%rsp), %r9d
 295bc21:      	pushq	0x238(%rsp)
 295bc28:      	pushq	%rbx
 295bc29:      	pushq	%r12
 295bc2b:      	callq	0x2965210 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295bc30:      	addq	$0x20, %rsp
 295bc34:      	testq	%rax, %rax
 295bc37:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bc3d:      	leaq	0x30(%rsp), %rax
 295bc42:      	movq	%rax, 0xa0(%rsp)
 295bc4a:      	leaq	0x130(%rsp), %rax
 295bc52:      	movq	%rax, 0xa8(%rsp)
 295bc5a:      	leaq	0x60(%rsp), %rax
 295bc5f:      	movq	%rax, 0xb0(%rsp)
 295bc67:      	movq	0x230(%rsp), %rax
 295bc6f:      	movq	%rax, 0xb8(%rsp)
 295bc77:      	movq	(%rsp), %rax
 295bc7b:      	movq	%rax, 0xc0(%rsp)
 295bc83:      	leaq	0xa0(%rsp), %rdi
 295bc8b:      	callq	0x2986590 <_ZZL17lowerV16I8ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGEENK3$_1clEv>
 295bc90:      	testq	%rax, %rax
 295bc93:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bc99:      	movq	0x60(%rsp), %rbp
 295bc9e:      	movl	0x68(%rsp), %ecx
 295bca2:      	movq	0x130(%rsp), %r12
 295bcaa:      	movq	0x138(%rsp), %rbx
 295bcb2:      	xorl	%r15d, %r15d
 295bcb5:      	movq	(%rsp), %rdi
 295bcb9:      	movq	0x228(%rsp), %r14
 295bcc1:      	movl	0x28(%rsp), %r9d
 295bcc6:      	movq	0x18(%rsp), %r8
 295bccb:      	jmp	0x29589d8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xb18>
 295bcd0:      	xorl	%r9d, %r9d
 295bcd3:      	subq	$0x20, %rsp
 295bcd7:      	movups	0xc0(%rsp), %xmm0
 295bcdf:      	movups	%xmm0, 0x10(%rsp)
 295bce4:      	leaq	0x230(%rsp), %rax
 295bcec:      	movdqu	(%rax), %xmm0
 295bcf0:      	movdqu	%xmm0, (%rsp)
 295bcf5:      	movq	%r15, %rdi
 295bcf8:      	jmp	0x295babd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bfd>
 295bcfd:      	movq	0x230(%rsp), %r13
 295bd05:      	movq	%r13, %rdi
 295bd08:      	movl	$0x96, %esi
 295bd0d:      	xorl	%edx, %edx
 295bd0f:      	movq	%r12, %rcx
 295bd12:      	movl	%ebp, %r8d
 295bd15:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bd1a:      	movq	%rbx, %r12
 295bd1d:      	movq	%rax, %rbx
 295bd20:      	movl	%edx, %r14d
 295bd23:      	movq	%r13, %rdi
 295bd26:      	movl	$0x96, %esi
 295bd2b:      	xorl	%edx, %edx
 295bd2d:      	movq	%r15, %rcx
 295bd30:      	movl	0x18(%rsp), %r8d
 295bd35:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bd3a:      	movq	%rax, 0x80(%rsp)
 295bd42:      	movl	%edx, 0x88(%rsp)
 295bd49:      	movq	0x58(%rsp), %rax
 295bd4e:      	movq	%rax, 0xa0(%rsp)
 295bd56:      	movq	%r12, 0xa8(%rsp)
 295bd5e:      	subq	$0x20, %rsp
 295bd62:      	movups	0xc0(%rsp), %xmm0
 295bd6a:      	movups	%xmm0, 0x10(%rsp)
 295bd6f:      	movdqa	0xa0(%rsp), %xmm0
 295bd78:      	movdqu	%xmm0, (%rsp)
 295bd7d:      	movq	%r13, %rdi
 295bd80:      	movl	$0x96, %esi
 295bd85:      	xorl	%edx, %edx
 295bd87:      	movq	0x20(%rsp), %rcx
 295bd8c:      	movq	%rbx, %r8
 295bd8f:      	movl	%r14d, %r9d
 295bd92:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295bd97:      	addq	$0x20, %rsp
 295bd9b:      	movl	%edx, %r8d
 295bd9e:      	movq	%r13, %rdi
 295bda1:      	movl	$0x5e, %esi
 295bda6:      	xorl	%edx, %edx
 295bda8:      	movq	%rax, %rcx
 295bdab:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bdb0:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bdb5:      	cmpl	$0x5, 0x9c(%rsp)
 295bdbd:      	jl	0x295be2d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3f6d>
 295bdbf:      	movq	0x58(%rsp), %rax
 295bdc4:      	movq	%rax, 0xa0(%rsp)
 295bdcc:      	movq	0x20(%rsp), %rax
 295bdd1:      	movq	%rax, 0xa8(%rsp)
 295bdd9:      	subq	$0x30, %rsp
 295bddd:      	movdqu	0xd0(%rsp), %xmm0
 295bde6:      	movdqu	%xmm0, (%rsp)
 295bdeb:      	movq	%r12, 0x20(%rsp)
 295bdf0:      	movq	%r14, 0x18(%rsp)
 295bdf5:      	movq	0x250(%rsp), %rax
 295bdfd:      	movq	%rax, 0x10(%rsp)
 295be02:      	movq	0x30(%rsp), %rdi
 295be07:      	movl	$0x49, %esi
 295be0c:      	movq	0x40(%rsp), %rdx
 295be11:      	movl	0x3c(%rsp), %ecx
 295be15:      	movq	0x58(%rsp), %r8
 295be1a:      	movq	0x48(%rsp), %r9
 295be1f:      	callq	0x2966780 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295be24:      	addq	$0x30, %rsp
 295be28:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295be2d:      	subq	$0x8, %rsp
 295be31:      	movq	0x8(%rsp), %rdi
 295be36:      	movl	$0x49, %esi
 295be3b:      	movq	0x18(%rsp), %rdx
 295be40:      	movl	0x14(%rsp), %ecx
 295be44:      	movq	0x30(%rsp), %r8
 295be49:      	movq	0x20(%rsp), %r9
 295be4e:      	pushq	%r12
 295be50:      	pushq	0x30(%rsp)
 295be54:      	movq	0x70(%rsp), %r15
 295be59:      	pushq	%r15
 295be5b:      	callq	0x296b3b0 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295be60:      	addq	$0x20, %rsp
 295be64:      	testq	%rax, %rax
 295be67:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295be6d:      	jmp	0x2959f2a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x206a>
 295be72:      	cmpl	$0x1, %r15d
 295be76:      	jne	0x295bed1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4011>
 295be78:      	movq	0x60(%rsp), %rdx
 295be7d:      	movl	0x68(%rsp), %ecx
 295be81:      	movq	0x220(%rsp), %r10
 295be89:      	movl	0x8(%r10), %eax
 295be8d:      	movq	(%rsp), %rdi
 295be91:      	movl	$0x30, %esi
 295be96:      	movq	0x18(%rsp), %r8
 295be9b:      	movl	0x28(%rsp), %r9d
 295bea0:      	pushq	0x230(%rsp)
 295bea7:      	pushq	%rbp
 295bea8:      	pushq	%rax
 295bea9:      	pushq	(%r10)
 295beac:      	pushq	%r14
 295beae:      	pushq	%rbx
 295beaf:      	callq	0x2963390 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295beb4:      	addq	$0x30, %rsp
 295beb8:      	testq	%rax, %rax
 295bebb:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bec1:      	movq	0x130(%rsp), %rbx
 295bec9:      	movq	0x138(%rsp), %r14
 295bed1:      	movq	0x60(%rsp), %rdx
 295bed6:      	movl	0x68(%rsp), %ecx
 295beda:      	subq	$0x8, %rsp
 295bede:      	movq	0x8(%rsp), %rdi
 295bee3:      	movl	$0x30, %esi
 295bee8:      	movq	0x20(%rsp), %r8
 295beed:      	movl	0x30(%rsp), %r9d
 295bef2:      	pushq	0x238(%rsp)
 295bef9:      	pushq	%r14
 295befb:      	pushq	%rbx
 295befc:      	callq	0x296a5d0 <_ZL22lowerShuffleAsBitBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295bf01:      	addq	$0x20, %rsp
 295bf05:      	testq	%rax, %rax
 295bf08:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295bf0e:      	cmpl	$0x0, 0x10(%rsp)
 295bf13:      	je	0x295c459 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4599>
 295bf19:      	subq	$0x8, %rsp
 295bf1d:      	xorl	%ebx, %ebx
 295bf1f:      	movq	0x238(%rsp), %rdi
 295bf27:      	xorl	%esi, %esi
 295bf29:      	movq	0x8(%rsp), %rdx
 295bf2e:      	movl	$0x6, %ecx
 295bf33:      	xorl	%r8d, %r8d
 295bf36:      	xorl	%r9d, %r9d
 295bf39:      	pushq	$0x0
 295bf3b:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295bf40:      	addq	$0x10, %rsp
 295bf44:      	leaq	0xb0(%rsp), %rcx
 295bf4c:      	movq	%rcx, 0xa0(%rsp)
 295bf54:      	movl	$0x8, 0xac(%rsp)
 295bf5f:      	movq	%rax, 0xb0(%rsp)
 295bf67:      	movl	%edx, 0xb8(%rsp)
 295bf6e:      	movq	%rax, 0xc0(%rsp)
 295bf76:      	movl	%edx, 0xc8(%rsp)
 295bf7d:      	movq	%rax, 0xd0(%rsp)
 295bf85:      	movl	%edx, 0xd8(%rsp)
 295bf8c:      	movq	%rax, 0xe0(%rsp)
 295bf94:      	movl	%edx, 0xe8(%rsp)
 295bf9b:      	movq	%rax, 0xf0(%rsp)
 295bfa3:      	movl	%edx, 0xf8(%rsp)
 295bfaa:      	movq	%rax, 0x100(%rsp)
 295bfb2:      	movl	%edx, 0x108(%rsp)
 295bfb9:      	movq	%rax, 0x110(%rsp)
 295bfc1:      	movl	%edx, 0x118(%rsp)
 295bfc8:      	movq	%rax, 0x120(%rsp)
 295bfd0:      	movl	%edx, 0x128(%rsp)
 295bfd7:      	movl	$0x8, 0xa8(%rsp)
 295bfe2:      	movq	0x10(%rsp), %rax
 295bfe7:      	leal	-0x1(%rax), %ebp
 295bfea:      	movl	$0x1, %r14d
 295bff0:      	movl	%ebp, %ecx
 295bff2:      	shll	%cl, %r14d
 295bff5:      	subq	$0x8, %rsp
 295bff9:      	movl	$0xff, %esi
 295bffe:      	movq	0x238(%rsp), %rdi
 295c006:      	movq	0x8(%rsp), %rdx
 295c00b:      	movl	$0x6, %ecx
 295c010:      	xorl	%r8d, %r8d
 295c013:      	xorl	%r9d, %r9d
 295c016:      	pushq	$0x0
 295c018:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c01d:      	addq	$0x10, %rsp
 295c021:      	movl	%ebx, %esi
 295c023:      	movq	0xa0(%rsp), %rcx
 295c02b:      	shlq	$0x4, %rsi
 295c02f:      	movq	%rax, (%rcx,%rsi)
 295c033:      	movl	%edx, 0x8(%rcx,%rsi)
 295c037:      	addl	%r14d, %ebx
 295c03a:      	cmpl	$0x8, %ebx
 295c03d:      	jne	0x295bff5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4135>
 295c03f:      	movl	0xa8(%rsp), %eax
 295c046:      	movq	%rcx, 0x30(%rsp)
 295c04b:      	movq	%rax, 0x38(%rsp)
 295c050:      	movq	0x230(%rsp), %rax
 295c058:      	movq	0x3b0(%rax), %rax
 295c05f:      	xorl	%r12d, %r12d
 295c062:      	movl	$0x0, %r9d
 295c068:      	testq	%rax, %rax
 295c06b:      	je	0x295c071 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x41b1>
 295c06d:      	movl	0x8(%rax), %r9d
 295c071:      	subq	$0x10, %rsp
 295c075:      	movups	0x40(%rsp), %xmm0
 295c07a:      	movups	%xmm0, (%rsp)
 295c07e:      	movq	0x240(%rsp), %r15
 295c086:      	movq	%r15, %rdi
 295c089:      	movl	$0xa0, %esi
 295c08e:      	movq	0x10(%rsp), %rdx
 295c093:      	movl	$0x3e, %ecx
 295c098:      	xorl	%r8d, %r8d
 295c09b:      	callq	0x5e26520 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_8ArrayRefINS_7SDValueEEENS_11SDNodeFlagsE>
 295c0a0:      	addq	$0x10, %rsp
 295c0a4:      	movq	%rax, %rbx
 295c0a7:      	movl	%edx, %r14d
 295c0aa:      	movq	0x60(%rsp), %rcx
 295c0af:      	movl	0x68(%rsp), %r8d
 295c0b4:      	movq	%r15, %rdi
 295c0b7:      	movl	$0x3e, %esi
 295c0bc:      	xorl	%edx, %edx
 295c0be:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c0c3:      	movq	%rbx, 0x30(%rsp)
 295c0c8:      	movl	%r14d, 0x38(%rsp)
 295c0cd:      	movq	%rax, 0x70(%rsp)
 295c0d2:      	movl	%edx, 0x78(%rsp)
 295c0d6:      	movq	0x3b0(%r15), %rax
 295c0dd:      	testq	%rax, %rax
 295c0e0:      	je	0x295c0e6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4226>
 295c0e2:      	movl	0x8(%rax), %r12d
 295c0e6:      	subq	$0x20, %rsp
 295c0ea:      	movups	0x50(%rsp), %xmm0
 295c0ef:      	movups	%xmm0, 0x10(%rsp)
 295c0f4:      	movups	0x90(%rsp), %xmm0
 295c0fc:      	movups	%xmm0, (%rsp)
 295c100:      	movq	$0x0, 0x40(%rsp)
 295c109:      	movq	0x250(%rsp), %rdi
 295c111:      	movl	$0xbf, %esi
 295c116:      	movq	0x20(%rsp), %rdx
 295c11b:      	movl	$0x3e, %ecx
 295c120:      	xorl	%r8d, %r8d
 295c123:      	movl	%r12d, %r9d
 295c126:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c12b:      	addq	$0x20, %rsp
 295c12f:      	movq	%rax, 0x60(%rsp)
 295c134:      	movl	%edx, 0x68(%rsp)
 295c138:      	cmpl	$0x2, %r13d
 295c13c:      	jae	0x295c55f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x469f>
 295c142:      	leaq	0x60(%rsp), %rax
 295c147:      	jmp	0x295c600 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4740>
 295c14c:      	cmpb	$0x0, 0x1d1(%r13)
 295c154:      	je	0x295c777 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x48b7>
 295c15a:      	movq	$0x0, 0x160(%rsp)
 295c166:      	movq	%r15, %rdi
 295c169:      	movq	0x20(%rsp), %rsi
 295c16e:      	xorl	%edx, %edx
 295c170:      	xorl	%ecx, %ecx
 295c172:      	callq	0x29754d0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 295c177:      	cmpl	$0x1, %eax
 295c17a:      	jne	0x295c3b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x44f3>
 295c180:      	movl	0x148(%r13), %r15d
 295c187:      	xorl	%ebx, %ebx
 295c189:      	cmpl	$0x5, %r15d
 295c18d:      	setge	%bl
 295c190:      	xorl	$0x293, %ebx            # imm = 0x293
 295c196:      	movq	0x230(%rsp), %r12
 295c19e:      	movq	%r12, %rdi
 295c1a1:      	movl	$0x49, %esi
 295c1a6:      	xorl	%edx, %edx
 295c1a8:      	movq	0x10(%rsp), %rcx
 295c1ad:      	movl	0xc(%rsp), %r8d
 295c1b2:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c1b7:      	movq	%rax, %r14
 295c1ba:      	movl	%edx, %ebp
 295c1bc:      	subq	$0x8, %rsp
 295c1c0:      	movl	$0x10, %esi
 295c1c5:      	movq	%r12, %rdi
 295c1c8:      	movq	0x8(%rsp), %rdx
 295c1cd:      	movl	$0x5, %ecx
 295c1d2:      	xorl	%r8d, %r8d
 295c1d5:      	movl	$0x1, %r9d
 295c1db:      	pushq	$0x0
 295c1dd:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c1e2:      	addq	$0x10, %rsp
 295c1e6:      	movq	%rax, 0xa0(%rsp)
 295c1ee:      	movl	%edx, 0xa8(%rsp)
 295c1f5:      	movq	%r14, 0x30(%rsp)
 295c1fa:      	movl	%ebp, 0x38(%rsp)
 295c1fe:      	movq	0x3b0(%r12), %rax
 295c206:      	testq	%rax, %rax
 295c209:      	je	0x295c216 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4356>
 295c20b:      	movl	0x8(%rax), %eax
 295c20e:      	movq	%rax, 0x160(%rsp)
 295c216:      	subq	$0x20, %rsp
 295c21a:      	movups	0xc0(%rsp), %xmm0
 295c222:      	movups	%xmm0, 0x10(%rsp)
 295c227:      	movups	0x50(%rsp), %xmm0
 295c22c:      	movups	%xmm0, (%rsp)
 295c230:      	movq	$0x0, 0x30(%rsp)
 295c239:      	movq	0x250(%rsp), %r14
 295c241:      	movq	%r14, %rdi
 295c244:      	movl	%ebx, %esi
 295c246:      	movq	0x20(%rsp), %rbp
 295c24b:      	movq	%rbp, %rdx
 295c24e:      	movl	$0x49, %ecx
 295c253:      	xorl	%r8d, %r8d
 295c256:      	movq	0x180(%rsp), %r9
 295c25e:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c263:      	addq	$0x20, %rsp
 295c267:      	movq	%rax, 0x20(%rsp)
 295c26c:      	movl	%edx, 0xc(%rsp)
 295c270:      	movq	%r14, %rdi
 295c273:      	movl	$0x49, %esi
 295c278:      	xorl	%edx, %edx
 295c27a:      	movq	0x28(%rsp), %rcx
 295c27f:      	movl	0x58(%rsp), %r8d
 295c284:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c289:      	movq	%rax, %r12
 295c28c:      	movl	%edx, %r13d
 295c28f:      	subq	$0x8, %rsp
 295c293:      	movl	$0x10, %esi
 295c298:      	movq	%r14, %rdi
 295c29b:      	movq	%rbp, %rdx
 295c29e:      	movl	$0x5, %ecx
 295c2a3:      	xorl	%r8d, %r8d
 295c2a6:      	movl	$0x1, %r9d
 295c2ac:      	pushq	$0x0
 295c2ae:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c2b3:      	addq	$0x10, %rsp
 295c2b7:      	movq	%rax, 0xa0(%rsp)
 295c2bf:      	movl	%edx, 0xa8(%rsp)
 295c2c6:      	movq	%r12, 0x30(%rsp)
 295c2cb:      	movl	%r13d, 0x38(%rsp)
 295c2d0:      	movq	0x3b0(%r14), %rax
 295c2d7:      	movl	$0x0, %r9d
 295c2dd:      	testq	%rax, %rax
 295c2e0:      	je	0x295c2e6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4426>
 295c2e2:      	movl	0x8(%rax), %r9d
 295c2e6:      	xorl	%r12d, %r12d
 295c2e9:      	cmpl	$0x5, %r15d
 295c2ed:      	setge	%r12b
 295c2f1:      	subq	$0x20, %rsp
 295c2f5:      	movups	0xc0(%rsp), %xmm0
 295c2fd:      	movups	%xmm0, 0x10(%rsp)
 295c302:      	movups	0x50(%rsp), %xmm0
 295c307:      	movups	%xmm0, (%rsp)
 295c30b:      	movq	0x250(%rsp), %r14
 295c313:      	movq	%r14, %rdi
 295c316:      	movl	%ebx, %esi
 295c318:      	movq	0x20(%rsp), %rdx
 295c31d:      	movl	$0x49, %ecx
 295c322:      	xorl	%r8d, %r8d
 295c325:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c32a:      	addq	$0x20, %rsp
 295c32e:      	addl	$0x2b5, %r12d           # imm = 0x2B5
 295c335:      	movq	%rax, 0xa0(%rsp)
 295c33d:      	movl	%edx, 0xa8(%rsp)
 295c344:      	movl	0x18(%rsp), %eax
 295c348:      	movl	%eax, 0xac(%rsp)
 295c34f:      	movq	0x20(%rsp), %rax
 295c354:      	movq	%rax, 0x30(%rsp)
 295c359:      	movl	0xc(%rsp), %eax
 295c35d:      	movl	%eax, 0x38(%rsp)
 295c361:      	movq	0x3b0(%r14), %rax
 295c368:      	testq	%rax, %rax
 295c36b:      	je	0x295c375 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x44b5>
 295c36d:      	movl	0x8(%rax), %eax
 295c370:      	movq	%rax, 0x10(%rsp)
 295c375:      	subq	$0x20, %rsp
 295c379:      	movups	0xc0(%rsp), %xmm0
 295c381:      	movups	%xmm0, 0x10(%rsp)
 295c386:      	movdqu	0x50(%rsp), %xmm0
 295c38c:      	movdqu	%xmm0, (%rsp)
 295c391:      	movq	0x250(%rsp), %rdi
 295c399:      	movl	%r12d, %esi
 295c39c:      	movq	0x20(%rsp), %rdx
 295c3a1:      	movl	$0x3e, %ecx
 295c3a6:      	xorl	%r8d, %r8d
 295c3a9:      	movq	0x30(%rsp), %r9
 295c3ae:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295c3b3:      	subq	$0x8, %rsp
 295c3b7:      	movq	0x8(%rsp), %rdi
 295c3bc:      	movl	$0x3e, %esi
 295c3c1:      	movq	0x18(%rsp), %rdx
 295c3c6:      	movl	0x14(%rsp), %ecx
 295c3ca:      	movq	0x30(%rsp), %r8
 295c3cf:      	movl	0x60(%rsp), %r9d
 295c3d4:      	pushq	0x238(%rsp)
 295c3db:      	pushq	0x30(%rsp)
 295c3df:      	pushq	%r15
 295c3e1:      	callq	0x296b3b0 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295c3e6:      	addq	$0x20, %rsp
 295c3ea:      	testq	%rax, %rax
 295c3ed:      	jne	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295c3f3:      	cmpl	$0x4, 0x9c(%rsp)
 295c3fb:      	jg	0x295cfc8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5108>
 295c401:      	cmpl	$0x4, 0x148(%r13)
 295c409:      	jl	0x295cfc8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5108>
 295c40f:      	leaq	0x30(%rsp), %rax
 295c414:      	leaq	0xa0(%rsp), %r10
 295c41c:      	movq	(%rsp), %rdi
 295c420:      	movl	$0x3e, %esi
 295c425:      	movq	0x10(%rsp), %rdx
 295c42a:      	movl	0xc(%rsp), %ecx
 295c42e:      	movq	0x28(%rsp), %r8
 295c433:      	movl	0x58(%rsp), %r9d
 295c438:      	pushq	%rax
 295c439:      	pushq	%r10
 295c43b:      	pushq	0x240(%rsp)
 295c442:      	pushq	0x238(%rsp)
 295c449:      	pushq	0x40(%rsp)
 295c44d:      	pushq	%r15
 295c44f:      	callq	0x29755a0 <_ZL28lowerShuffleAsBlendOfPSHUFBsRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGERbSC_>
 295c454:      	jmp	0x295d033 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5173>
 295c459:      	xorl	%ecx, %ecx
 295c45b:      	cmpl	$0x2, %r13d
 295c45f:      	setb	%cl
 295c462:      	movq	0x130(%rsp), %rbx
 295c46a:      	movq	0x138(%rsp), %rsi
 295c472:      	xorl	%r14d, %r14d
 295c475:      	movq	%rbx, %rdi
 295c478:      	xorl	%edx, %edx
 295c47a:      	callq	0x29754d0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 295c47f:      	cmpl	$0x1, %eax
 295c482:      	jne	0x295cb0f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4c4f>
 295c488:      	movq	0x60(%rsp), %rcx
 295c48d:      	movl	0x68(%rsp), %r8d
 295c492:      	movq	0x230(%rsp), %r15
 295c49a:      	movq	%r15, %rdi
 295c49d:      	movl	$0x3e, %esi
 295c4a2:      	xorl	%edx, %edx
 295c4a4:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c4a9:      	movq	%rax, %rbx
 295c4ac:      	movl	%edx, %ebp
 295c4ae:      	subq	$0x8, %rsp
 295c4b2:      	movl	$0x8, %esi
 295c4b7:      	movq	%r15, %rdi
 295c4ba:      	movq	0x8(%rsp), %rdx
 295c4bf:      	movl	$0x5, %ecx
 295c4c4:      	xorl	%r8d, %r8d
 295c4c7:      	movl	$0x1, %r9d
 295c4cd:      	pushq	$0x0
 295c4cf:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c4d4:      	addq	$0x10, %rsp
 295c4d8:      	movq	%rax, 0xa0(%rsp)
 295c4e0:      	movl	%edx, 0xa8(%rsp)
 295c4e7:      	movq	%rbx, 0x30(%rsp)
 295c4ec:      	movl	%ebp, 0x38(%rsp)
 295c4f0:      	movq	0x3b0(%r15), %rax
 295c4f7:      	testq	%rax, %rax
 295c4fa:      	je	0x295c500 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4640>
 295c4fc:      	movl	0x8(%rax), %r14d
 295c500:      	subq	$0x20, %rsp
 295c504:      	movups	0xc0(%rsp), %xmm0
 295c50c:      	movups	%xmm0, 0x10(%rsp)
 295c511:      	movups	0x50(%rsp), %xmm0
 295c516:      	movups	%xmm0, (%rsp)
 295c51a:      	xorl	%ebx, %ebx
 295c51c:      	movq	0x250(%rsp), %rdi
 295c524:      	movl	$0x292, %esi            # imm = 0x292
 295c529:      	movq	0x20(%rsp), %rdx
 295c52e:      	movl	$0x3e, %ecx
 295c533:      	xorl	%r8d, %r8d
 295c536:      	movl	%r14d, %r9d
 295c539:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c53e:      	addq	$0x20, %rsp
 295c542:      	movq	%rax, 0x60(%rsp)
 295c547:      	movl	%edx, 0x68(%rsp)
 295c54b:      	cmpl	$0x2, %r13d
 295c54f:      	jae	0x295ced9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5019>
 295c555:      	leaq	0x60(%rsp), %rax
 295c55a:      	jmp	0x295cfa7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x50e7>
 295c55f:      	movq	0x230(%rsp), %r15
 295c567:      	movq	%r15, %rdi
 295c56a:      	movl	$0x3e, %esi
 295c56f:      	xorl	%edx, %edx
 295c571:      	movq	0x18(%rsp), %rcx
 295c576:      	movl	0x28(%rsp), %r8d
 295c57b:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c580:      	movq	%rbx, 0x30(%rsp)
 295c585:      	movl	%r14d, 0x38(%rsp)
 295c58a:      	movq	%rax, 0x70(%rsp)
 295c58f:      	movl	%edx, 0x78(%rsp)
 295c593:      	movq	0x3b0(%r15), %rax
 295c59a:      	testq	%rax, %rax
 295c59d:      	je	0x295c5a7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x46e7>
 295c59f:      	movl	0x8(%rax), %eax
 295c5a2:      	movq	%rax, 0x20(%rsp)
 295c5a7:      	subq	$0x20, %rsp
 295c5ab:      	movups	0x50(%rsp), %xmm0
 295c5b0:      	movups	%xmm0, 0x10(%rsp)
 295c5b5:      	movups	0x90(%rsp), %xmm0
 295c5bd:      	movups	%xmm0, (%rsp)
 295c5c1:      	movq	0x250(%rsp), %rdi
 295c5c9:      	movl	$0xbf, %esi
 295c5ce:      	movq	0x20(%rsp), %rdx
 295c5d3:      	movl	$0x3e, %ecx
 295c5d8:      	xorl	%r8d, %r8d
 295c5db:      	movq	0x40(%rsp), %r9
 295c5e0:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c5e5:      	addq	$0x20, %rsp
 295c5e9:      	movq	%rax, 0x170(%rsp)
 295c5f1:      	movl	%edx, 0x178(%rsp)
 295c5f8:      	leaq	0x170(%rsp), %rax
 295c600:      	movq	0x230(%rsp), %rcx
 295c608:      	movq	0x3b0(%rcx), %rcx
 295c60f:      	testq	%rcx, %rcx
 295c612:      	je	0x295c670 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x47b0>
 295c614:      	movl	0x8(%rcx), %r9d
 295c618:      	jmp	0x295c673 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x47b3>
 295c61a:      	cmpb	$0x1, 0x1db(%rbp)
 295c621:      	jne	0x295cb7f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4cbf>
 295c627:      	movq	0x130(%rsp), %rdi
 295c62f:      	movl	$0x30, %esi
 295c634:      	movq	0x230(%rsp), %rbx
 295c63c:      	movq	%rbx, %rdx
 295c63f:      	movq	(%rsp), %rcx
 295c643:      	callq	0x28e6870 <_ZL14getConstVectorN4llvm8ArrayRefIiEENS_3MVTERNS_12SelectionDAGERKNS_5SDLocEb>
 295c648:      	movq	%rax, 0xa0(%rsp)
 295c650:      	movl	%edx, 0xa8(%rsp)
 295c657:      	movq	0x3b0(%rbx), %rax
 295c65e:      	testq	%rax, %rax
 295c661:      	je	0x295d7a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58e6>
 295c667:      	movl	0x8(%rax), %r9d
 295c66b:      	jmp	0x295d7a9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58e9>
 295c670:      	xorl	%r9d, %r9d
 295c673:      	subq	$0x20, %rsp
 295c677:      	movups	(%rax), %xmm0
 295c67a:      	movups	%xmm0, 0x10(%rsp)
 295c67f:      	movdqu	0x80(%rsp), %xmm0
 295c688:      	movdqu	%xmm0, (%rsp)
 295c68d:      	movq	0x250(%rsp), %rdi
 295c695:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295c69a:      	movq	0x20(%rsp), %rdx
 295c69f:      	movl	$0x30, %ecx
 295c6a4:      	xorl	%r8d, %r8d
 295c6a7:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c6ac:      	addq	$0x20, %rsp
 295c6b0:      	movq	%rax, %rbx
 295c6b3:      	movl	%edx, %r14d
 295c6b6:      	cmpl	$0x1, 0x10(%rsp)
 295c6bb:      	jne	0x295c729 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4869>
 295c6bd:      	movq	0xa0(%rsp), %rdi
 295c6c5:      	leaq	0xb0(%rsp), %rax
 295c6cd:      	cmpq	%rax, %rdi
 295c6d0:      	je	0x295d801 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5941>
 295c6d6:      	callq	0x828a6d0 <free@plt>
 295c6db:      	jmp	0x295d801 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5941>
 295c6e0:      	subq	$0x20, %rsp
 295c6e4:      	movups	0x50(%rsp), %xmm0
 295c6e9:      	movups	%xmm0, 0x10(%rsp)
 295c6ee:      	movdqu	0x90(%rsp), %xmm0
 295c6f7:      	movdqu	%xmm0, (%rsp)
 295c6fc:      	movq	0x250(%rsp), %rdi
 295c704:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295c709:      	movq	0x20(%rsp), %rdx
 295c70e:      	movl	$0x30, %ecx
 295c713:      	xorl	%r8d, %r8d
 295c716:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c71b:      	addq	$0x20, %rsp
 295c71f:      	movq	%rax, %rbx
 295c722:      	movl	%edx, %r14d
 295c725:      	decl	%ebp
 295c727:      	je	0x295c6bd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x47fd>
 295c729:      	movq	0x230(%rsp), %r15
 295c731:      	movq	%r15, %rdi
 295c734:      	movl	$0x3e, %esi
 295c739:      	xorl	%edx, %edx
 295c73b:      	movq	%rbx, %rcx
 295c73e:      	movl	%r14d, %r8d
 295c741:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c746:      	movq	%rax, 0x30(%rsp)
 295c74b:      	movl	%edx, 0x38(%rsp)
 295c74f:      	movq	%rax, 0x70(%rsp)
 295c754:      	movl	%edx, 0x78(%rsp)
 295c758:      	movq	0x3b0(%r15), %rax
 295c75f:      	movl	$0x0, %r9d
 295c765:      	testq	%rax, %rax
 295c768:      	je	0x295c6e0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4820>
 295c76e:      	movl	0x8(%rax), %r9d
 295c772:      	jmp	0x295c6e0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4820>
 295c777:      	movl	0x148(%r13), %eax
 295c77e:      	cmpl	$0x5, %eax
 295c781:      	jl	0x295cbe7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4d27>
 295c787:      	xorl	%r15d, %r15d
 295c78a:      	subq	$0x8, %rsp
 295c78e:      	xorl	%r14d, %r14d
 295c791:      	movq	0x238(%rsp), %rdi
 295c799:      	xorl	%esi, %esi
 295c79b:      	movq	0x8(%rsp), %rdx
 295c7a0:      	movl	$0x7, %ecx
 295c7a5:      	xorl	%r8d, %r8d
 295c7a8:      	xorl	%r9d, %r9d
 295c7ab:      	pushq	$0x0
 295c7ad:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c7b2:      	addq	$0x10, %rsp
 295c7b6:      	leaq	0xb0(%rsp), %rcx
 295c7be:      	movq	%rcx, 0xa0(%rsp)
 295c7c6:      	movq	%rax, 0xb0(%rsp)
 295c7ce:      	movl	%edx, 0xb8(%rsp)
 295c7d5:      	movq	%rax, 0xc0(%rsp)
 295c7dd:      	movl	%edx, 0xc8(%rsp)
 295c7e4:      	movq	%rax, 0xd0(%rsp)
 295c7ec:      	movl	%edx, 0xd8(%rsp)
 295c7f3:      	movq	%rax, 0xe0(%rsp)
 295c7fb:      	movl	%edx, 0xe8(%rsp)
 295c802:      	movabsq	$0x400000004, %rax      # imm = 0x400000004
 295c80c:      	movq	%rax, 0xa8(%rsp)
 295c814:      	decb	%bl
 295c816:      	movl	$0x1, %ebp
 295c81b:      	movl	%ebx, %ecx
 295c81d:      	shll	%cl, %ebp
 295c81f:      	subq	$0x8, %rsp
 295c823:      	movl	$0xffff, %esi           # imm = 0xFFFF
 295c828:      	movq	0x238(%rsp), %rdi
 295c830:      	movq	0x8(%rsp), %rdx
 295c835:      	movl	$0x7, %ecx
 295c83a:      	xorl	%r8d, %r8d
 295c83d:      	xorl	%r9d, %r9d
 295c840:      	pushq	$0x0
 295c842:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c847:      	addq	$0x10, %rsp
 295c84b:      	movl	%r14d, %esi
 295c84e:      	movq	0xa0(%rsp), %rcx
 295c856:      	shlq	$0x4, %rsi
 295c85a:      	movq	%rax, (%rcx,%rsi)
 295c85e:      	movl	%edx, 0x8(%rcx,%rsi)
 295c862:      	addl	%ebp, %r14d
 295c865:      	cmpl	$0x4, %r14d
 295c869:      	jne	0x295c81f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x495f>
 295c86b:      	movl	0xa8(%rsp), %eax
 295c872:      	movq	%rcx, 0x30(%rsp)
 295c877:      	movq	%rax, 0x38(%rsp)
 295c87c:      	movq	0x230(%rsp), %rax
 295c884:      	movq	0x3b0(%rax), %rax
 295c88b:      	xorl	%ebx, %ebx
 295c88d:      	movl	$0x0, %r9d
 295c893:      	testq	%rax, %rax
 295c896:      	je	0x295c89c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x49dc>
 295c898:      	movl	0x8(%rax), %r9d
 295c89c:      	subq	$0x10, %rsp
 295c8a0:      	movups	0x40(%rsp), %xmm0
 295c8a5:      	movups	%xmm0, (%rsp)
 295c8a9:      	movq	0x240(%rsp), %r12
 295c8b1:      	movq	%r12, %rdi
 295c8b4:      	movl	$0xa0, %esi
 295c8b9:      	movq	0x10(%rsp), %rdx
 295c8be:      	movl	$0x49, %ecx
 295c8c3:      	xorl	%r8d, %r8d
 295c8c6:      	callq	0x5e26520 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_8ArrayRefINS_7SDValueEEENS_11SDNodeFlagsE>
 295c8cb:      	addq	$0x10, %rsp
 295c8cf:      	movq	%rax, %r14
 295c8d2:      	movl	%edx, %r13d
 295c8d5:      	movq	%r12, %rdi
 295c8d8:      	movl	$0x49, %esi
 295c8dd:      	xorl	%edx, %edx
 295c8df:      	movq	0x10(%rsp), %rcx
 295c8e4:      	movl	0xc(%rsp), %r8d
 295c8e9:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c8ee:      	movq	%r14, 0x30(%rsp)
 295c8f3:      	movl	%r13d, 0x38(%rsp)
 295c8f8:      	movq	%rax, 0x70(%rsp)
 295c8fd:      	movl	%edx, 0x78(%rsp)
 295c901:      	movq	0x3b0(%r12), %rax
 295c909:      	testq	%rax, %rax
 295c90c:      	je	0x295c911 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4a51>
 295c90e:      	movl	0x8(%rax), %ebx
 295c911:      	subq	$0x20, %rsp
 295c915:      	movups	0x50(%rsp), %xmm0
 295c91a:      	movups	%xmm0, 0x10(%rsp)
 295c91f:      	movups	0x90(%rsp), %xmm0
 295c927:      	movups	%xmm0, (%rsp)
 295c92b:      	xorl	%r12d, %r12d
 295c92e:      	movq	0x250(%rsp), %rbp
 295c936:      	movq	%rbp, %rdi
 295c939:      	movl	$0xbf, %esi
 295c93e:      	movq	0x20(%rsp), %rdx
 295c943:      	movl	$0x49, %ecx
 295c948:      	xorl	%r8d, %r8d
 295c94b:      	movl	%ebx, %r9d
 295c94e:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c953:      	addq	$0x20, %rsp
 295c957:      	movq	%rax, %rbx
 295c95a:      	movl	%edx, 0x10(%rsp)
 295c95e:      	movq	%rbp, %rdi
 295c961:      	movl	$0x49, %esi
 295c966:      	xorl	%edx, %edx
 295c968:      	movq	0x28(%rsp), %rcx
 295c96d:      	movl	0x58(%rsp), %r8d
 295c972:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c977:      	movq	%r14, 0x30(%rsp)
 295c97c:      	movl	%r13d, 0x38(%rsp)
 295c981:      	movq	%rax, 0x70(%rsp)
 295c986:      	movl	%edx, 0x78(%rsp)
 295c98a:      	movq	0x3b0(%rbp), %rax
 295c991:      	testq	%rax, %rax
 295c994:      	je	0x295c99a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4ada>
 295c996:      	movl	0x8(%rax), %r12d
 295c99a:      	subq	$0x20, %rsp
 295c99e:      	movups	0x50(%rsp), %xmm0
 295c9a3:      	movups	%xmm0, 0x10(%rsp)
 295c9a8:      	movups	0x90(%rsp), %xmm0
 295c9b0:      	movups	%xmm0, (%rsp)
 295c9b4:      	xorl	%r14d, %r14d
 295c9b7:      	movq	0x250(%rsp), %rdi
 295c9bf:      	movl	$0xbf, %esi
 295c9c4:      	movq	0x20(%rsp), %rdx
 295c9c9:      	movl	$0x49, %ecx
 295c9ce:      	xorl	%r8d, %r8d
 295c9d1:      	movl	%r12d, %r9d
 295c9d4:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c9d9:      	addq	$0x20, %rsp
 295c9dd:      	movq	%rax, %r13
 295c9e0:      	movl	%edx, %r12d
 295c9e3:      	movq	0xa0(%rsp), %rdi
 295c9eb:      	leaq	0xb0(%rsp), %rax
 295c9f3:      	cmpq	%rax, %rdi
 295c9f6:      	je	0x295c9fd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4b3d>
 295c9f8:      	callq	0x828a6d0 <free@plt>
 295c9fd:      	movq	%r13, 0xa0(%rsp)
 295ca05:      	movl	%r12d, 0xa8(%rsp)
 295ca0d:      	movl	0x18(%rsp), %eax
 295ca11:      	movl	%eax, 0xac(%rsp)
 295ca18:      	movq	%rbx, 0x30(%rsp)
 295ca1d:      	movl	0x10(%rsp), %eax
 295ca21:      	movl	%eax, 0x38(%rsp)
 295ca25:      	movq	0x230(%rsp), %rax
 295ca2d:      	movq	0x3b0(%rax), %rax
 295ca34:      	testq	%rax, %rax
 295ca37:      	je	0x295ca3d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4b7d>
 295ca39:      	movl	0x8(%rax), %r14d
 295ca3d:      	subq	$0x20, %rsp
 295ca41:      	movups	0xc0(%rsp), %xmm0
 295ca49:      	movups	%xmm0, 0x10(%rsp)
 295ca4e:      	movdqu	0x50(%rsp), %xmm0
 295ca54:      	movdqu	%xmm0, (%rsp)
 295ca59:      	movq	0x250(%rsp), %rdi
 295ca61:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295ca66:      	movq	0x20(%rsp), %rdx
 295ca6b:      	movl	$0x3e, %ecx
 295ca70:      	xorl	%r8d, %r8d
 295ca73:      	movl	%r14d, %r9d
 295ca76:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ca7b:      	addq	$0x20, %rsp
 295ca7f:      	movl	%edx, %r8d
 295ca82:      	testb	%r15b, %r15b
 295ca85:      	je	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
 295ca8b:      	xorl	%r13d, %r13d
 295ca8e:      	movq	0x230(%rsp), %r12
 295ca96:      	movq	%r12, %rdi
 295ca99:      	movl	$0x49, %esi
 295ca9e:      	xorl	%edx, %edx
 295caa0:      	movq	%rax, %rcx
 295caa3:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295caa8:      	movq	%rax, 0xa0(%rsp)
 295cab0:      	movl	%edx, 0xa8(%rsp)
 295cab7:      	movq	%rax, 0x30(%rsp)
 295cabc:      	movl	%edx, 0x38(%rsp)
 295cac0:      	movq	0x3b0(%r12), %rax
 295cac8:      	testq	%rax, %rax
 295cacb:      	je	0x295cad1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4c11>
 295cacd:      	movl	0x8(%rax), %r13d
 295cad1:      	subq	$0x20, %rsp
 295cad5:      	movups	0xc0(%rsp), %xmm0
 295cadd:      	movups	%xmm0, 0x10(%rsp)
 295cae2:      	movdqu	0x50(%rsp), %xmm0
 295cae8:      	movdqu	%xmm0, (%rsp)
 295caed:      	movq	0x250(%rsp), %rdi
 295caf5:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295cafa:      	movq	0x20(%rsp), %rdx
 295caff:      	movl	$0x3e, %ecx
 295cb04:      	xorl	%r8d, %r8d
 295cb07:      	movl	%r13d, %r9d
 295cb0a:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295cb0f:      	movq	0x60(%rsp), %r14
 295cb14:      	movl	0x68(%rsp), %eax
 295cb18:      	movl	%eax, 0x10(%rsp)
 295cb1c:      	testl	%r15d, %r15d
 295cb1f:      	jle	0x295d03c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x517c>
 295cb25:      	subq	$0x30, %rsp
 295cb29:      	movdqu	0x160(%rsp), %xmm0
 295cb32:      	movdqu	%xmm0, (%rsp)
 295cb37:      	movq	0x260(%rsp), %rax
 295cb3f:      	movq	%rax, 0x20(%rsp)
 295cb44:      	movq	%rbp, 0x18(%rsp)
 295cb49:      	movq	0x250(%rsp), %rax
 295cb51:      	movq	%rax, 0x10(%rsp)
 295cb56:      	movq	0x30(%rsp), %rdi
 295cb5b:      	movl	$0x30, %esi
 295cb60:      	movq	%r14, %rdx
 295cb63:      	movl	0x40(%rsp), %ecx
 295cb67:      	movq	0x48(%rsp), %r8
 295cb6c:      	movl	0x58(%rsp), %r9d
 295cb71:      	callq	0x2966780 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295cb76:      	addq	$0x30, %rsp
 295cb7a:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295cb7f:      	movq	0x60(%rsp), %rdx
 295cb84:      	movl	0x68(%rsp), %ecx
 295cb88:      	movl	0x148(%rbp), %eax
 295cb8e:      	movzbl	0x16a(%rbp), %esi
 295cb95:      	subq	$0x30, %rsp
 295cb99:      	movdqu	0x160(%rsp), %xmm0
 295cba2:      	movdqu	%xmm0, (%rsp)
 295cba7:      	movq	0x260(%rsp), %rdi
 295cbaf:      	movq	%rdi, 0x20(%rsp)
 295cbb4:      	movl	%esi, 0x18(%rsp)
 295cbb8:      	movl	%eax, 0x10(%rsp)
 295cbbc:      	movq	0x30(%rsp), %rdi
 295cbc1:      	movl	$0x30, %esi
 295cbc6:      	movq	0x48(%rsp), %r8
 295cbcb:      	movl	0x58(%rsp), %r9d
 295cbd0:      	callq	0x296ce00 <_ZL34lowerShuffleAsByteRotateAndPermuteRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295cbd5:      	addq	$0x30, %rsp
 295cbd9:      	testq	%rax, %rax
 295cbdc:      	jne	0x295d7fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x593b>
 295cbe2:      	jmp	0x295d801 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5941>
 295cbe7:      	cmpl	$0x4, %eax
 295cbea:      	je	0x295c15a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x429a>
 295cbf0:      	subq	$0x8, %rsp
 295cbf4:      	xorl	%r15d, %r15d
 295cbf7:      	movl	$0x10, %esi
 295cbfc:      	movq	0x238(%rsp), %r14
 295cc04:      	movq	%r14, %rdi
 295cc07:      	movq	0x8(%rsp), %rdx
 295cc0c:      	movl	$0x5, %ecx
 295cc11:      	xorl	%r8d, %r8d
 295cc14:      	movl	$0x1, %r9d
 295cc1a:      	pushq	$0x0
 295cc1c:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295cc21:      	addq	$0x10, %rsp
 295cc25:      	movq	%rax, %rbx
 295cc28:      	movl	%edx, %ebp
 295cc2a:      	movq	%r14, %rdi
 295cc2d:      	movl	$0x49, %esi
 295cc32:      	xorl	%edx, %edx
 295cc34:      	movq	0x10(%rsp), %rcx
 295cc39:      	movl	0xc(%rsp), %r8d
 295cc3e:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cc43:      	movq	%rax, %r12
 295cc46:      	movl	%edx, %r13d
 295cc49:      	movq	%r14, %rdi
 295cc4c:      	movl	$0x49, %esi
 295cc51:      	xorl	%edx, %edx
 295cc53:      	movq	0x28(%rsp), %rcx
 295cc58:      	movl	0x58(%rsp), %r8d
 295cc5d:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cc62:      	movq	%rax, 0x10(%rsp)
 295cc67:      	movl	%edx, 0xc(%rsp)
 295cc6b:      	movq	%rbx, 0xa0(%rsp)
 295cc73:      	movl	%ebp, 0xa8(%rsp)
 295cc7a:      	movq	%r12, 0x30(%rsp)
 295cc7f:      	movl	%r13d, 0x38(%rsp)
 295cc84:      	movq	0x3b0(%r14), %rax
 295cc8b:      	movl	$0x0, %r9d
 295cc91:      	testq	%rax, %rax
 295cc94:      	je	0x295cc9a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4dda>
 295cc96:      	movl	0x8(%rax), %r9d
 295cc9a:      	subq	$0x20, %rsp
 295cc9e:      	movups	0xc0(%rsp), %xmm0
 295cca6:      	movups	%xmm0, 0x10(%rsp)
 295ccab:      	movups	0x50(%rsp), %xmm0
 295ccb0:      	movups	%xmm0, (%rsp)
 295ccb4:      	movq	0x250(%rsp), %r14
 295ccbc:      	movq	%r14, %rdi
 295ccbf:      	movl	$0x291, %esi            # imm = 0x291
 295ccc4:      	movq	0x20(%rsp), %rdx
 295ccc9:      	movl	$0x49, %ecx
 295ccce:      	xorl	%r8d, %r8d
 295ccd1:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ccd6:      	addq	$0x20, %rsp
 295ccda:      	movq	%rax, 0x20(%rsp)
 295ccdf:      	movl	%edx, %r13d
 295cce2:      	movq	%rbx, 0xa0(%rsp)
 295ccea:      	movl	%ebp, 0xa8(%rsp)
 295ccf1:      	movq	0x10(%rsp), %rax
 295ccf6:      	movq	%rax, 0x30(%rsp)
 295ccfb:      	movl	0xc(%rsp), %eax
 295ccff:      	movl	%eax, 0x38(%rsp)
 295cd03:      	movl	0x18(%rsp), %eax
 295cd07:      	movl	%eax, 0x3c(%rsp)
 295cd0b:      	movq	0x3b0(%r14), %rax
 295cd12:      	testq	%rax, %rax
 295cd15:      	je	0x295cd1b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4e5b>
 295cd17:      	movl	0x8(%rax), %r15d
 295cd1b:      	subq	$0x20, %rsp
 295cd1f:      	movups	0xc0(%rsp), %xmm0
 295cd27:      	movups	%xmm0, 0x10(%rsp)
 295cd2c:      	movups	0x50(%rsp), %xmm0
 295cd31:      	movups	%xmm0, (%rsp)
 295cd35:      	movq	$0x0, 0x30(%rsp)
 295cd3e:      	movq	0x250(%rsp), %r12
 295cd46:      	movq	%r12, %rdi
 295cd49:      	movl	$0x291, %esi            # imm = 0x291
 295cd4e:      	movq	0x20(%rsp), %rdx
 295cd53:      	movl	$0x49, %ecx
 295cd58:      	xorl	%r8d, %r8d
 295cd5b:      	movl	%r15d, %r9d
 295cd5e:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cd63:      	addq	$0x20, %rsp
 295cd67:      	movq	%rax, %r15
 295cd6a:      	movl	%edx, 0xc(%rsp)
 295cd6e:      	movq	%rbx, 0xa0(%rsp)
 295cd76:      	movl	%ebp, 0xa8(%rsp)
 295cd7d:      	movq	0x20(%rsp), %rax
 295cd82:      	movq	%rax, 0x30(%rsp)
 295cd87:      	movl	%r13d, 0x38(%rsp)
 295cd8c:      	movq	0x3b0(%r12), %rax
 295cd94:      	movl	$0x0, %r9d
 295cd9a:      	testq	%rax, %rax
 295cd9d:      	je	0x295cda3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4ee3>
 295cd9f:      	movl	0x8(%rax), %r9d
 295cda3:      	subq	$0x20, %rsp
 295cda7:      	movups	0xc0(%rsp), %xmm0
 295cdaf:      	movups	%xmm0, 0x10(%rsp)
 295cdb4:      	movups	0x50(%rsp), %xmm0
 295cdb9:      	movups	%xmm0, (%rsp)
 295cdbd:      	movq	0x250(%rsp), %r14
 295cdc5:      	movq	%r14, %rdi
 295cdc8:      	movl	$0x293, %esi            # imm = 0x293
 295cdcd:      	movq	0x20(%rsp), %rdx
 295cdd2:      	movl	$0x49, %ecx
 295cdd7:      	xorl	%r8d, %r8d
 295cdda:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cddf:      	addq	$0x20, %rsp
 295cde3:      	movq	%rax, %r12
 295cde6:      	movl	%edx, %r13d
 295cde9:      	movq	%rbx, 0xa0(%rsp)
 295cdf1:      	movl	%ebp, 0xa8(%rsp)
 295cdf8:      	movq	%r15, 0x30(%rsp)
 295cdfd:      	movl	0xc(%rsp), %eax
 295ce01:      	movl	%eax, 0x38(%rsp)
 295ce05:      	movl	0x18(%rsp), %eax
 295ce09:      	movl	%eax, 0x3c(%rsp)
 295ce0d:      	movq	0x3b0(%r14), %rax
 295ce14:      	testq	%rax, %rax
 295ce17:      	je	0x295ce21 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4f61>
 295ce19:      	movl	0x8(%rax), %eax
 295ce1c:      	movq	%rax, 0x10(%rsp)
 295ce21:      	subq	$0x20, %rsp
 295ce25:      	movups	0xc0(%rsp), %xmm0
 295ce2d:      	movups	%xmm0, 0x10(%rsp)
 295ce32:      	movups	0x50(%rsp), %xmm0
 295ce37:      	movups	%xmm0, (%rsp)
 295ce3b:      	xorl	%ebx, %ebx
 295ce3d:      	movq	0x250(%rsp), %r14
 295ce45:      	movq	%r14, %rdi
 295ce48:      	movl	$0x293, %esi            # imm = 0x293
 295ce4d:      	movq	0x20(%rsp), %rdx
 295ce52:      	movl	$0x49, %ecx
 295ce57:      	xorl	%r8d, %r8d
 295ce5a:      	movq	0x30(%rsp), %r9
 295ce5f:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ce64:      	addq	$0x20, %rsp
 295ce68:      	movq	%rax, 0xa0(%rsp)
 295ce70:      	movl	%edx, 0xa8(%rsp)
 295ce77:      	movl	0x18(%rsp), %eax
 295ce7b:      	movl	%eax, 0xac(%rsp)
 295ce82:      	movq	%r12, 0x30(%rsp)
 295ce87:      	movl	%r13d, 0x38(%rsp)
 295ce8c:      	movq	0x3b0(%r14), %rax
 295ce93:      	testq	%rax, %rax
 295ce96:      	je	0x295ce9b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4fdb>
 295ce98:      	movl	0x8(%rax), %ebx
 295ce9b:      	subq	$0x20, %rsp
 295ce9f:      	movups	0xc0(%rsp), %xmm0
 295cea7:      	movups	%xmm0, 0x10(%rsp)
 295ceac:      	movdqu	0x50(%rsp), %xmm0
 295ceb2:      	movdqu	%xmm0, (%rsp)
 295ceb7:      	movq	0x250(%rsp), %rdi
 295cebf:      	movl	$0x2b5, %esi            # imm = 0x2B5
 295cec4:      	movq	0x20(%rsp), %rdx
 295cec9:      	movl	$0x3e, %ecx
 295cece:      	xorl	%r8d, %r8d
 295ced1:      	movl	%ebx, %r9d
 295ced4:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295ced9:      	movq	0x230(%rsp), %r15
 295cee1:      	movq	%r15, %rdi
 295cee4:      	movl	$0x3e, %esi
 295cee9:      	xorl	%edx, %edx
 295ceeb:      	movq	0x18(%rsp), %rcx
 295cef0:      	movl	0x28(%rsp), %r8d
 295cef5:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cefa:      	movq	%rax, %r14
 295cefd:      	movl	%edx, %ebp
 295ceff:      	subq	$0x8, %rsp
 295cf03:      	movl	$0x8, %esi
 295cf08:      	movq	%r15, %rdi
 295cf0b:      	movq	0x8(%rsp), %rdx
 295cf10:      	movl	$0x5, %ecx
 295cf15:      	xorl	%r8d, %r8d
 295cf18:      	movl	$0x1, %r9d
 295cf1e:      	pushq	$0x0
 295cf20:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295cf25:      	addq	$0x10, %rsp
 295cf29:      	movq	%rax, 0xa0(%rsp)
 295cf31:      	movl	%edx, 0xa8(%rsp)
 295cf38:      	movq	%r14, 0x30(%rsp)
 295cf3d:      	movl	%ebp, 0x38(%rsp)
 295cf41:      	movq	0x3b0(%r15), %rax
 295cf48:      	testq	%rax, %rax
 295cf4b:      	je	0x295cf50 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5090>
 295cf4d:      	movl	0x8(%rax), %ebx
 295cf50:      	subq	$0x20, %rsp
 295cf54:      	movups	0xc0(%rsp), %xmm0
 295cf5c:      	movups	%xmm0, 0x10(%rsp)
 295cf61:      	movups	0x50(%rsp), %xmm0
 295cf66:      	movups	%xmm0, (%rsp)
 295cf6a:      	movq	0x250(%rsp), %rdi
 295cf72:      	movl	$0x292, %esi            # imm = 0x292
 295cf77:      	movq	0x20(%rsp), %rdx
 295cf7c:      	movl	$0x3e, %ecx
 295cf81:      	xorl	%r8d, %r8d
 295cf84:      	movl	%ebx, %r9d
 295cf87:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cf8c:      	addq	$0x20, %rsp
 295cf90:      	movq	%rax, 0x170(%rsp)
 295cf98:      	movl	%edx, 0x178(%rsp)
 295cf9f:      	leaq	0x170(%rsp), %rax
 295cfa7:      	movq	0x230(%rsp), %rcx
 295cfaf:      	movq	0x3b0(%rcx), %rcx
 295cfb6:      	testq	%rcx, %rcx
 295cfb9:      	je	0x295d499 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55d9>
 295cfbf:      	movl	0x8(%rcx), %r9d
 295cfc3:      	jmp	0x295d49c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55dc>
 295cfc8:      	movq	%r15, 0xa0(%rsp)
 295cfd0:      	movq	0x20(%rsp), %rax
 295cfd5:      	movq	%rax, 0xa8(%rsp)
 295cfdd:      	subq	$0x30, %rsp
 295cfe1:      	movdqu	0xd0(%rsp), %xmm0
 295cfea:      	movdqu	%xmm0, (%rsp)
 295cfef:      	movq	0x260(%rsp), %rax
 295cff7:      	movq	%rax, 0x20(%rsp)
 295cffc:      	movq	%r13, 0x18(%rsp)
 295d001:      	movq	0x250(%rsp), %rax
 295d009:      	movq	%rax, 0x10(%rsp)
 295d00e:      	movq	0x30(%rsp), %rdi
 295d013:      	movl	$0x3e, %esi
 295d018:      	movq	0x40(%rsp), %rdx
 295d01d:      	movl	0x3c(%rsp), %ecx
 295d021:      	movq	0x58(%rsp), %r8
 295d026:      	movl	0x88(%rsp), %r9d
 295d02e:      	callq	0x2966780 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295d033:      	addq	$0x30, %rsp
 295d037:      	jmp	0x2959c70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db0>
 295d03c:      	movl	0x6c(%rsp), %eax
 295d040:      	movl	%eax, 0x20(%rsp)
 295d044:      	pcmpeqd	%xmm0, %xmm0
 295d048:      	movdqa	%xmm0, 0xb0(%rsp)
 295d051:      	movdqa	%xmm0, 0xa0(%rsp)
 295d05a:      	movdqa	%xmm0, 0x40(%rsp)
 295d060:      	movdqa	%xmm0, 0x30(%rsp)
 295d066:      	movl	(%rbx), %eax
 295d068:      	movl	$0xffffffff, 0xc(%rsp)  # imm = 0xFFFFFFFF
 295d070:      	movl	$0xffffffff, 0x28(%rsp) # imm = 0xFFFFFFFF
 295d078:      	testl	%eax, %eax
 295d07a:      	js	0x295d087 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x51c7>
 295d07c:      	movl	%eax, 0xa0(%rsp)
 295d083:      	movl	%eax, 0x28(%rsp)
 295d087:      	movl	0x4(%rbx), %eax
 295d08a:      	testl	%eax, %eax
 295d08c:      	js	0x295d099 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x51d9>
 295d08e:      	movl	%eax, 0xa4(%rsp)
 295d095:      	movl	%eax, 0xc(%rsp)
 295d099:      	movl	0x8(%rbx), %eax
 295d09c:      	movl	$0xffffffff, 0x18(%rsp) # imm = 0xFFFFFFFF
 295d0a4:      	movl	$0xffffffff, 0x9c(%rsp) # imm = 0xFFFFFFFF
 295d0af:      	testl	%eax, %eax
 295d0b1:      	js	0x295d0c1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5201>
 295d0b3:      	movl	%eax, 0xa8(%rsp)
 295d0ba:      	movl	%eax, 0x9c(%rsp)
 295d0c1:      	movl	0xc(%rbx), %eax
 295d0c4:      	testl	%eax, %eax
 295d0c6:      	js	0x295d0d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5213>
 295d0c8:      	movl	%eax, 0xac(%rsp)
 295d0cf:      	movl	%eax, 0x18(%rsp)
 295d0d3:      	movl	0x10(%rbx), %eax
 295d0d6:      	movl	$0xffffffff, 0x58(%rsp) # imm = 0xFFFFFFFF
 295d0de:      	movl	$0xffffffff, 0x15c(%rsp) # imm = 0xFFFFFFFF
 295d0e9:      	testl	%eax, %eax
 295d0eb:      	js	0x295d0fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x523b>
 295d0ed:      	movl	%eax, 0xb0(%rsp)
 295d0f4:      	movl	%eax, 0x15c(%rsp)
 295d0fb:      	movl	0x14(%rbx), %eax
 295d0fe:      	testl	%eax, %eax
 295d100:      	js	0x295d10d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x524d>
 295d102:      	movl	%eax, 0xb4(%rsp)
 295d109:      	movl	%eax, 0x58(%rsp)
 295d10d:      	movl	0x18(%rbx), %eax
 295d110:      	movl	$0xffffffff, 0x160(%rsp) # imm = 0xFFFFFFFF
 295d11b:      	movl	$0xffffffff, 0x154(%rsp) # imm = 0xFFFFFFFF
 295d126:      	testl	%eax, %eax
 295d128:      	js	0x295d138 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5278>
 295d12a:      	movl	%eax, 0xb8(%rsp)
 295d131:      	movl	%eax, 0x154(%rsp)
 295d138:      	movl	0x1c(%rbx), %eax
 295d13b:      	testl	%eax, %eax
 295d13d:      	js	0x295d14d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x528d>
 295d13f:      	movl	%eax, 0xbc(%rsp)
 295d146:      	movl	%eax, 0x160(%rsp)
 295d14d:      	movl	0x20(%rbx), %eax
 295d150:      	movl	$0xffffffff, 0x158(%rsp) # imm = 0xFFFFFFFF
 295d15b:      	movl	$0xffffffff, 0x14c(%rsp) # imm = 0xFFFFFFFF
 295d166:      	testl	%eax, %eax
 295d168:      	js	0x295d175 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52b5>
 295d16a:      	movl	%eax, 0x30(%rsp)
 295d16e:      	movl	%eax, 0x14c(%rsp)
 295d175:      	movl	0x24(%rbx), %eax
 295d178:      	testl	%eax, %eax
 295d17a:      	js	0x295d187 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52c7>
 295d17c:      	movl	%eax, 0x34(%rsp)
 295d180:      	movl	%eax, 0x158(%rsp)
 295d187:      	movl	0x28(%rbx), %eax
 295d18a:      	movl	$0xffffffff, 0x150(%rsp) # imm = 0xFFFFFFFF
 295d195:      	movl	$0xffffffff, 0x140(%rsp) # imm = 0xFFFFFFFF
 295d1a0:      	testl	%eax, %eax
 295d1a2:      	js	0x295d1af <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52ef>
 295d1a4:      	movl	%eax, 0x38(%rsp)
 295d1a8:      	movl	%eax, 0x140(%rsp)
 295d1af:      	movl	0x2c(%rbx), %eax
 295d1b2:      	testl	%eax, %eax
 295d1b4:      	js	0x295d1c1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5301>
 295d1b6:      	movl	%eax, 0x3c(%rsp)
 295d1ba:      	movl	%eax, 0x150(%rsp)
 295d1c1:      	movl	0x30(%rbx), %eax
 295d1c4:      	movl	$0xffffffff, 0x148(%rsp) # imm = 0xFFFFFFFF
 295d1cf:      	movl	$0xffffffff, %r13d      # imm = 0xFFFFFFFF
 295d1d5:      	testl	%eax, %eax
 295d1d7:      	js	0x295d1e0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5320>
 295d1d9:      	movl	%eax, 0x40(%rsp)
 295d1dd:      	movl	%eax, %r13d
 295d1e0:      	movl	0x34(%rbx), %eax
 295d1e3:      	testl	%eax, %eax
 295d1e5:      	js	0x295d1f2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5332>
 295d1e7:      	movl	%eax, 0x44(%rsp)
 295d1eb:      	movl	%eax, 0x148(%rsp)
 295d1f2:      	movl	0x38(%rbx), %eax
 295d1f5:      	movl	$0xffffffff, 0x144(%rsp) # imm = 0xFFFFFFFF
 295d200:      	movl	$0xffffffff, %r15d      # imm = 0xFFFFFFFF
 295d206:      	testl	%eax, %eax
 295d208:      	js	0x295d211 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5351>
 295d20a:      	movl	%eax, 0x48(%rsp)
 295d20e:      	movl	%eax, %r15d
 295d211:      	movl	0x3c(%rbx), %eax
 295d214:      	testl	%eax, %eax
 295d216:      	js	0x295d223 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5363>
 295d218:      	movl	%eax, 0x4c(%rsp)
 295d21c:      	movl	%eax, 0x144(%rsp)
 295d223:      	leaq	0xa0(%rsp), %rdi
 295d22b:      	callq	0x29876a0 <_ZN4llvm7none_ofIRSt5arrayIiLm8EEZL17lowerV16I8ShuffleRKNS_5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueESC_RKNS_12X86SubtargetERNS_12SelectionDAGEE3$_2EEbOT_T0_>
 295d230:      	testb	%al, %al
 295d232:      	je	0x295d4d2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5612>
 295d238:      	leaq	0x30(%rsp), %rdi
 295d23d:      	callq	0x2987720 <_ZN4llvm7none_ofIRSt5arrayIiLm8EEZL17lowerV16I8ShuffleRKNS_5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueESC_RKNS_12X86SubtargetERNS_12SelectionDAGEE3$_3EEbOT_T0_>
 295d242:      	testb	%al, %al
 295d244:      	je	0x295d4d2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5612>
 295d24a:      	movq	$0x0, 0x20(%rsp)
 295d253:      	movq	0x230(%rsp), %r12
 295d25b:      	movq	%r12, %rdi
 295d25e:      	movl	$0x3e, %esi
 295d263:      	xorl	%edx, %edx
 295d265:      	movq	%r14, %rcx
 295d268:      	movl	0x10(%rsp), %r8d
 295d26d:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d272:      	movq	%rax, %rbx
 295d275:      	movl	%edx, %ebp
 295d277:      	subq	$0x8, %rsp
 295d27b:      	movl	$0xff, %esi
 295d280:      	movq	%r12, %rdi
 295d283:      	movq	0x8(%rsp), %rdx
 295d288:      	movl	$0x3e, %ecx
 295d28d:      	xorl	%r8d, %r8d
 295d290:      	xorl	%r9d, %r9d
 295d293:      	pushq	$0x0
 295d295:      	callq	0x5e00000 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295d29a:      	addq	$0x10, %rsp
 295d29e:      	movq	%rax, 0x70(%rsp)
 295d2a3:      	movl	%edx, 0x78(%rsp)
 295d2a7:      	movq	%rbx, 0x80(%rsp)
 295d2af:      	movl	%ebp, 0x88(%rsp)
 295d2b6:      	movq	0x3b0(%r12), %rax
 295d2be:      	testq	%rax, %rax
 295d2c1:      	je	0x295d2cb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x540b>
 295d2c3:      	movl	0x8(%rax), %eax
 295d2c6:      	movq	%rax, 0x20(%rsp)
 295d2cb:      	subq	$0x20, %rsp
 295d2cf:      	movups	0x90(%rsp), %xmm0
 295d2d7:      	movups	%xmm0, 0x10(%rsp)
 295d2dc:      	movups	0xa0(%rsp), %xmm0
 295d2e4:      	movups	%xmm0, (%rsp)
 295d2e8:      	movq	0x250(%rsp), %rbx
 295d2f0:      	movq	%rbx, %rdi
 295d2f3:      	movl	$0xbf, %esi
 295d2f8:      	movq	0x20(%rsp), %rdx
 295d2fd:      	movl	$0x3e, %ecx
 295d302:      	xorl	%r8d, %r8d
 295d305:      	movq	0x40(%rsp), %r9
 295d30a:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d30f:      	addq	$0x20, %rsp
 295d313:      	movq	%rax, 0x180(%rsp)
 295d31b:      	movl	%edx, 0x16c(%rsp)
 295d322:      	movq	%rbx, %rdi
 295d325:      	movl	$0x3e, %esi
 295d32a:      	xorl	%edx, %edx
 295d32c:      	callq	0x28424e0 <_ZN4llvm12SelectionDAG8getUNDEFENS_3EVTE>
 295d331:      	movq	%rax, %rcx
 295d334:      	cmpl	$0x0, 0x28(%rsp)
 295d339:      	js	0x295d348 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5488>
 295d33b:      	movl	0x28(%rsp), %eax
 295d33f:      	shrl	%eax
 295d341:      	movl	%eax, 0xa0(%rsp)
 295d348:      	cmpl	$0x0, 0xc(%rsp)
 295d34d:      	js	0x295d35c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x549c>
 295d34f:      	movl	0xc(%rsp), %eax
 295d353:      	shrl	%eax
 295d355:      	movl	%eax, 0xa4(%rsp)
 295d35c:      	cmpl	$0x0, 0x9c(%rsp)
 295d364:      	js	0x295d376 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54b6>
 295d366:      	movl	0x9c(%rsp), %eax
 295d36d:      	shrl	%eax
 295d36f:      	movl	%eax, 0xa8(%rsp)
 295d376:      	cmpl	$0x0, 0x18(%rsp)
 295d37b:      	js	0x295d38a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54ca>
 295d37d:      	movl	0x18(%rsp), %eax
 295d381:      	shrl	%eax
 295d383:      	movl	%eax, 0xac(%rsp)
 295d38a:      	cmpl	$0x0, 0x15c(%rsp)
 295d392:      	js	0x295d3a4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54e4>
 295d394:      	movl	0x15c(%rsp), %eax
 295d39b:      	shrl	%eax
 295d39d:      	movl	%eax, 0xb0(%rsp)
 295d3a4:      	cmpl	$0x0, 0x58(%rsp)
 295d3a9:      	js	0x295d3b8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54f8>
 295d3ab:      	movl	0x58(%rsp), %eax
 295d3af:      	shrl	%eax
 295d3b1:      	movl	%eax, 0xb4(%rsp)
 295d3b8:      	cmpl	$0x0, 0x154(%rsp)
 295d3c0:      	js	0x295d3d2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5512>
 295d3c2:      	movl	0x154(%rsp), %eax
 295d3c9:      	shrl	%eax
 295d3cb:      	movl	%eax, 0xb8(%rsp)
 295d3d2:      	cmpl	$0x0, 0x160(%rsp)
 295d3da:      	js	0x295d3ec <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x552c>
 295d3dc:      	movl	0x160(%rsp), %eax
 295d3e3:      	shrl	%eax
 295d3e5:      	movl	%eax, 0xbc(%rsp)
 295d3ec:      	cmpl	$0x0, 0x14c(%rsp)
 295d3f4:      	js	0x295d403 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5543>
 295d3f6:      	movl	0x14c(%rsp), %eax
 295d3fd:      	shrl	%eax
 295d3ff:      	movl	%eax, 0x30(%rsp)
 295d403:      	cmpl	$0x0, 0x158(%rsp)
 295d40b:      	js	0x295d41a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x555a>
 295d40d:      	movl	0x158(%rsp), %eax
 295d414:      	shrl	%eax
 295d416:      	movl	%eax, 0x34(%rsp)
 295d41a:      	cmpl	$0x0, 0x140(%rsp)
 295d422:      	js	0x295d431 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5571>
 295d424:      	movl	0x140(%rsp), %eax
 295d42b:      	shrl	%eax
 295d42d:      	movl	%eax, 0x38(%rsp)
 295d431:      	cmpl	$0x0, 0x150(%rsp)
 295d439:      	js	0x295d448 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5588>
 295d43b:      	movl	0x150(%rsp), %eax
 295d442:      	shrl	%eax
 295d444:      	movl	%eax, 0x3c(%rsp)
 295d448:      	testl	%r13d, %r13d
 295d44b:      	js	0x295d455 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5595>
 295d44d:      	shrl	%r13d
 295d450:      	movl	%r13d, 0x40(%rsp)
 295d455:      	cmpl	$0x0, 0x148(%rsp)
 295d45d:      	js	0x295d46c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55ac>
 295d45f:      	movl	0x148(%rsp), %eax
 295d466:      	shrl	%eax
 295d468:      	movl	%eax, 0x44(%rsp)
 295d46c:      	testl	%r15d, %r15d
 295d46f:      	js	0x295d479 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55b9>
 295d471:      	shrl	%r15d
 295d474:      	movl	%r15d, 0x48(%rsp)
 295d479:      	cmpl	$0x0, 0x144(%rsp)
 295d481:      	js	0x295d636 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5776>
 295d487:      	movl	0x144(%rsp), %eax
 295d48e:      	shrl	%eax
 295d490:      	movl	%eax, 0x4c(%rsp)
 295d494:      	jmp	0x295d636 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5776>
 295d499:      	xorl	%r9d, %r9d
 295d49c:      	subq	$0x20, %rsp
 295d4a0:      	movups	(%rax), %xmm0
 295d4a3:      	movups	%xmm0, 0x10(%rsp)
 295d4a8:      	movdqu	0x80(%rsp), %xmm0
 295d4b1:      	movdqu	%xmm0, (%rsp)
 295d4b6:      	movq	0x250(%rsp), %rdi
 295d4be:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295d4c3:      	movq	0x20(%rsp), %rdx
 295d4c8:      	movl	$0x30, %ecx
 295d4cd:      	jmp	0x295bb79 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3cb9>
 295d4d2:      	movl	0x148(%rbp), %esi
 295d4d8:      	movl	$0x30, %edi
 295d4dd:      	movq	0x230(%rsp), %r12
 295d4e5:      	movq	%r12, %rdx
 295d4e8:      	movq	(%rsp), %rcx
 295d4ec:      	callq	0x2842530 <_ZL13getZeroVectorN4llvm3MVTERKNS_12X86SubtargetERNS_12SelectionDAGERKNS_5SDLocE>
 295d4f1:      	movq	%rax, %rbx
 295d4f4:      	movl	%edx, %r15d
 295d4f7:      	movq	%rax, 0x70(%rsp)
 295d4fc:      	movl	%edx, 0x78(%rsp)
 295d500:      	movq	%r14, 0x80(%rsp)
 295d508:      	movl	0x10(%rsp), %eax
 295d50c:      	movl	%eax, 0x88(%rsp)
 295d513:      	movl	0x20(%rsp), %eax
 295d517:      	movl	%eax, 0x8c(%rsp)
 295d51e:      	movq	0x3b0(%r12), %rax
 295d526:      	xorl	%r13d, %r13d
 295d529:      	movl	$0x0, %r9d
 295d52f:      	testq	%rax, %rax
 295d532:      	je	0x295d538 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5678>
 295d534:      	movl	0x8(%rax), %r9d
 295d538:      	subq	$0x20, %rsp
 295d53c:      	movups	0x90(%rsp), %xmm0
 295d544:      	movups	%xmm0, 0x10(%rsp)
 295d549:      	movups	0xa0(%rsp), %xmm0
 295d551:      	movups	%xmm0, (%rsp)
 295d555:      	movq	0x250(%rsp), %r12
 295d55d:      	movq	%r12, %rdi
 295d560:      	movl	$0x2c8, %esi            # imm = 0x2C8
 295d565:      	movq	0x20(%rsp), %rdx
 295d56a:      	movl	$0x30, %ecx
 295d56f:      	xorl	%r8d, %r8d
 295d572:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d577:      	addq	$0x20, %rsp
 295d57b:      	movl	%edx, %r8d
 295d57e:      	movq	%r12, %rdi
 295d581:      	movl	$0x3e, %esi
 295d586:      	xorl	%edx, %edx
 295d588:      	movq	%rax, %rcx
 295d58b:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d590:      	movq	%rax, 0x180(%rsp)
 295d598:      	movl	%edx, 0x16c(%rsp)
 295d59f:      	movq	%rbx, 0x70(%rsp)
 295d5a4:      	movl	%r15d, 0x78(%rsp)
 295d5a9:      	movq	%r14, 0x80(%rsp)
 295d5b1:      	movl	0x10(%rsp), %eax
 295d5b5:      	movl	%eax, 0x88(%rsp)
 295d5bc:      	movl	0x20(%rsp), %eax
 295d5c0:      	movl	%eax, 0x8c(%rsp)
 295d5c7:      	movq	0x3b0(%r12), %rax
 295d5cf:      	testq	%rax, %rax
 295d5d2:      	je	0x295d5d8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5718>
 295d5d4:      	movl	0x8(%rax), %r13d
 295d5d8:      	subq	$0x20, %rsp
 295d5dc:      	movups	0x90(%rsp), %xmm0
 295d5e4:      	movups	%xmm0, 0x10(%rsp)
 295d5e9:      	movups	0xa0(%rsp), %xmm0
 295d5f1:      	movups	%xmm0, (%rsp)
 295d5f5:      	movq	0x250(%rsp), %rbx
 295d5fd:      	movq	%rbx, %rdi
 295d600:      	movl	$0x2c9, %esi            # imm = 0x2C9
 295d605:      	movq	0x20(%rsp), %rdx
 295d60a:      	movl	$0x30, %ecx
 295d60f:      	xorl	%r8d, %r8d
 295d612:      	movl	%r13d, %r9d
 295d615:      	callq	0x5e27990 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d61a:      	addq	$0x20, %rsp
 295d61e:      	movl	%edx, %r8d
 295d621:      	movq	%rbx, %rdi
 295d624:      	movl	$0x3e, %esi
 295d629:      	xorl	%edx, %edx
 295d62b:      	movq	%rax, %rcx
 295d62e:      	callq	0x5dfeed0 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d633:      	movq	%rax, %rcx
 295d636:      	movq	%rcx, %r15
 295d639:      	movq	%rcx, 0x188(%rsp)
 295d641:      	movl	%edx, %r13d
 295d644:      	movl	%edx, 0x190(%rsp)
 295d64b:      	leaq	0xa0(%rsp), %rax
 295d653:      	movq	%rax, 0x1c8(%rsp)
 295d65b:      	movq	$0x8, 0x1d0(%rsp)
 295d667:      	subq	$0x20, %rsp
 295d66b:      	movups	0x1e8(%rsp), %xmm0
 295d673:      	movups	%xmm0, 0x10(%rsp)
 295d678:      	movups	0x1a8(%rsp), %xmm0
 295d680:      	movups	%xmm0, (%rsp)
 295d684:      	movq	$0x0, 0x30(%rsp)
 295d68d:      	movq	0x250(%rsp), %rdi
 295d695:      	movl	$0x3e, %esi
 295d69a:      	xorl	%edx, %edx
 295d69c:      	movq	0x20(%rsp), %r14
 295d6a1:      	movq	%r14, %rcx
 295d6a4:      	movq	0x1a0(%rsp), %rbp
 295d6ac:      	movq	%rbp, %r8
 295d6af:      	movl	0x18c(%rsp), %ebx
 295d6b6:      	movl	%ebx, %r9d
 295d6b9:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295d6be:      	addq	$0x20, %rsp
 295d6c2:      	movq	%rax, %r12
 295d6c5:      	movl	%edx, 0x20(%rsp)
 295d6c9:      	movq	%r15, 0x1b8(%rsp)
 295d6d1:      	movl	%r13d, 0x1c0(%rsp)
 295d6d9:      	leaq	0x30(%rsp), %rax
 295d6de:      	movq	%rax, 0x1a8(%rsp)
 295d6e6:      	movq	$0x8, 0x1b0(%rsp)
 295d6f2:      	subq	$0x20, %rsp
 295d6f6:      	movups	0x1c8(%rsp), %xmm0
 295d6fe:      	movups	%xmm0, 0x10(%rsp)
 295d703:      	movups	0x1d8(%rsp), %xmm0
 295d70b:      	movups	%xmm0, (%rsp)
 295d70f:      	movq	0x250(%rsp), %r15
 295d717:      	movq	%r15, %rdi
 295d71a:      	movl	$0x3e, %esi
 295d71f:      	xorl	%edx, %edx
 295d721:      	movq	%r14, %rcx
 295d724:      	movq	%rbp, %r8
 295d727:      	movl	%ebx, %r9d
 295d72a:      	callq	0x5e07880 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295d72f:      	addq	$0x20, %rsp
 295d733:      	movq	%rax, 0x70(%rsp)
 295d738:      	movl	%edx, 0x78(%rsp)
 295d73c:      	movq	%r12, 0x80(%rsp)
 295d744:      	movl	0x20(%rsp), %eax
 295d748:      	movl	%eax, 0x88(%rsp)
 295d74f:      	movq	0x3b0(%r15), %rax
 295d756:      	testq	%rax, %rax
 295d759:      	je	0x295d763 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58a3>
 295d75b:      	movl	0x8(%rax), %eax
 295d75e:      	movq	%rax, 0x10(%rsp)
 295d763:      	subq	$0x20, %rsp
 295d767:      	movups	0x90(%rsp), %xmm0
 295d76f:      	movups	%xmm0, 0x10(%rsp)
 295d774:      	movdqu	0xa0(%rsp), %xmm0
 295d77d:      	movdqu	%xmm0, (%rsp)
 295d782:      	movq	0x250(%rsp), %rdi
 295d78a:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295d78f:      	movq	0x20(%rsp), %rdx
 295d794:      	movl	$0x30, %ecx
 295d799:      	xorl	%r8d, %r8d
 295d79c:      	movq	0x30(%rsp), %r9
 295d7a1:      	jmp	0x2959c67 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da7>
 295d7a6:      	xorl	%r9d, %r9d
 295d7a9:      	subq	$0x30, %rsp
 295d7ad:      	movups	0xd0(%rsp), %xmm0
 295d7b5:      	movups	%xmm0, 0x20(%rsp)
 295d7ba:      	leaq	0x240(%rsp), %rax
 295d7c2:      	movups	(%rax), %xmm0
 295d7c5:      	movups	%xmm0, 0x10(%rsp)
 295d7ca:      	movdqu	0x90(%rsp), %xmm0
 295d7d3:      	movdqu	%xmm0, (%rsp)
 295d7d8:      	movq	0x260(%rsp), %rdi
 295d7e0:      	movl	$0x2eb, %esi            # imm = 0x2EB
 295d7e5:      	movq	0x30(%rsp), %rdx
 295d7ea:      	movl	$0x30, %ecx
 295d7ef:      	xorl	%r8d, %r8d
 295d7f2:      	callq	0x5e2ad10 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295d7f7:      	addq	$0x30, %rsp
 295d7fb:      	movq	%rax, %rbx
 295d7fe:      	movl	%edx, %r14d
 295d801:      	movq	%rbx, %rax
 295d804:      	movl	%r14d, %r8d
 295d807:      	jmp	0x2959c73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db3>
