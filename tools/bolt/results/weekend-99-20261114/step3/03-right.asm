
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000002957ee0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>:
 2957ee0:      	pushq	%rbp
 2957ee1:      	pushq	%r15
 2957ee3:      	pushq	%r14
 2957ee5:      	pushq	%r13
 2957ee7:      	pushq	%r12
 2957ee9:      	pushq	%rbx
 2957eea:      	subq	$0x1d8, %rsp            # imm = 0x1D8
 2957ef1:      	movl	%r9d, %r11d
 2957ef4:      	movq	%r8, %rbp
 2957ef7:      	movq	%rdx, %rbx
 2957efa:      	movq	%rsi, %r12
 2957efd:      	movq	0x230(%rsp), %r15
 2957f05:      	movq	0x228(%rsp), %r14
 2957f0d:      	movq	0x220(%rsp), %r10
 2957f15:      	leaq	0x210(%rsp), %rdx
 2957f1d:      	movzwl	%cx, %eax
 2957f20:      	cmpl	$0x5d, %eax
 2957f23:      	jg	0x2958642 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x762>
 2957f29:      	cmpl	$0x30, %eax
 2957f2c:      	movq	%rdi, (%rsp)
 2957f30:      	je	0x2958737 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x857>
 2957f36:      	cmpl	$0x3e, %eax
 2957f39:      	jne	0x2958cc6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xde6>
 2957f3f:      	movq	%r15, %rax
 2957f42:      	movq	(%rdx), %r15
 2957f45:      	movl	0x8(%rdx), %r13d
 2957f49:      	movl	0xc(%rdx), %ecx
 2957f4c:      	movl	%ecx, 0x18(%rsp)
 2957f50:      	subq	$0x8, %rsp
 2957f54:      	movl	$0x3e, %esi
 2957f59:      	movq	%rbp, %rdx
 2957f5c:      	movl	%r11d, %ecx
 2957f5f:      	movq	%r15, %r8
 2957f62:      	movl	%r13d, %r9d
 2957f65:      	pushq	%rax
 2957f66:      	pushq	%r14
 2957f68:      	pushq	%r10
 2957f6a:      	pushq	%rbx
 2957f6b:      	pushq	%r12
 2957f6d:      	movq	%r12, %r14
 2957f70:      	movl	%r11d, %r12d
 2957f73:      	callq	0x296d960 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2957f78:      	addq	$0x30, %rsp
 2957f7c:      	testq	%rax, %rax
 2957f7f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2957f85:      	movq	%r15, 0x20(%rsp)
 2957f8a:      	movl	%r13d, 0x58(%rsp)
 2957f8f:      	movq	%rbx, 0x28(%rsp)
 2957f94:      	movq	(%rsp), %r15
 2957f98:      	movq	%r15, %rdi
 2957f9b:      	movl	$0x3e, %esi
 2957fa0:      	movq	%rbp, %rdx
 2957fa3:      	movl	%r12d, %ecx
 2957fa6:      	movq	%r14, %r8
 2957fa9:      	movq	0x220(%rsp), %r9
 2957fb1:      	pushq	0x230(%rsp)
 2957fb8:      	movq	0x230(%rsp), %r13
 2957fc0:      	pushq	%r13
 2957fc2:      	callq	0x2971550 <_ZL21lowerShuffleWithVPMOVRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2957fc7:      	addq	$0x10, %rsp
 2957fcb:      	testq	%rax, %rax
 2957fce:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2957fd4:      	movq	%rbp, 0x10(%rsp)
 2957fd9:      	movq	0x28(%rsp), %r11
 2957fde:      	testq	%r11, %r11
 2957fe1:      	movq	%r15, %rdi
 2957fe4:      	movl	%r12d, %ecx
 2957fe7:      	movq	%r14, %r12
 2957fea:      	movq	%r13, %rbx
 2957fed:      	movq	0x220(%rsp), %r10
 2957ff5:      	movq	0x20(%rsp), %r14
 2957ffa:      	je	0x295a50b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x262b>
 2958000:      	leaq	(,%r11,4), %r8
 2958008:      	addq	$-0x4, %r8
 295800c:      	xorl	%ebp, %ebp
 295800e:      	movq	%r12, %rax
 2958011:      	cmpq	$0x1c, %r8
 2958015:      	jb	0x2958085 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1a5>
 2958017:      	shrq	$0x2, %r8
 295801b:      	incq	%r8
 295801e:      	movq	%r8, %rdx
 2958021:      	andq	$-0x8, %rdx
 2958025:      	leaq	(%r12,%rdx,4), %rax
 2958029:      	pxor	%xmm0, %xmm0
 295802d:      	xorl	%esi, %esi
 295802f:      	movdqa	-0x1b39a47(%rip), %xmm2 # 0xe1e5f0 <.LCPI649_0>
 2958037:      	pxor	%xmm1, %xmm1
 295803b:      	nopl	(%rax,%rax)
 2958040:      	movdqu	(%r12,%rsi,4), %xmm3
 2958046:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 295804d:      	pcmpgtd	%xmm2, %xmm3
 2958051:      	psubd	%xmm3, %xmm1
 2958055:      	pcmpgtd	%xmm2, %xmm4
 2958059:      	psubd	%xmm4, %xmm0
 295805d:      	addq	$0x8, %rsi
 2958061:      	cmpq	%rsi, %rdx
 2958064:      	jne	0x2958040 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x160>
 2958066:      	paddd	%xmm1, %xmm0
 295806a:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295806f:      	paddd	%xmm0, %xmm1
 2958073:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2958078:      	paddd	%xmm1, %xmm0
 295807c:      	movd	%xmm0, %ebp
 2958080:      	cmpq	%rdx, %r8
 2958083:      	je	0x29580a3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c3>
 2958085:      	leaq	(%r12,%r11,4), %rsi
 2958089:      	nopl	(%rax)
 2958090:      	xorl	%edx, %edx
 2958092:      	cmpl	$0x8, (%rax)
 2958095:      	setge	%dl
 2958098:      	addl	%edx, %ebp
 295809a:      	addq	$0x4, %rax
 295809e:      	cmpq	%rsi, %rax
 29580a1:      	jne	0x2958090 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b0>
 29580a3:      	testl	%ebp, %ebp
 29580a5:      	je	0x295a50b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x262b>
 29580ab:      	movl	$0x3e, %esi
 29580b0:      	movq	0x10(%rsp), %rdx
 29580b5:      	movq	%r14, %r8
 29580b8:      	movl	0x58(%rsp), %r15d
 29580bd:      	movl	%r15d, %r9d
 29580c0:      	pushq	$0x0
 29580c2:      	pushq	0x238(%rsp)
 29580c9:      	pushq	%rbx
 29580ca:      	pushq	%r10
 29580cc:      	pushq	%r11
 29580ce:      	pushq	%r12
 29580d0:      	movl	%ecx, %r13d
 29580d3:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 29580d8:      	addq	$0x30, %rsp
 29580dc:      	testq	%rax, %rax
 29580df:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29580e5:      	movl	%r13d, 0xc(%rsp)
 29580ea:      	movq	0x228(%rsp), %rbx
 29580f2:      	cmpb	$0x1, 0x1c6(%rbx)
 29580f9:      	jne	0x2958147 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x267>
 29580fb:      	movq	0x220(%rsp), %r10
 2958103:      	movl	0x8(%r10), %eax
 2958107:      	subq	$0x8, %rsp
 295810b:      	movq	0x8(%rsp), %rdi
 2958110:      	movl	$0x3e, %esi
 2958115:      	movq	0x18(%rsp), %rdx
 295811a:      	movl	0x14(%rsp), %ecx
 295811e:      	movq	%r14, %r8
 2958121:      	movl	%r15d, %r9d
 2958124:      	pushq	0x238(%rsp)
 295812b:      	pushq	%rax
 295812c:      	pushq	(%r10)
 295812f:      	pushq	0x48(%rsp)
 2958133:      	pushq	%r12
 2958135:      	callq	0x2973ed0 <_ZL21lowerShuffleWithSSE4ARKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGE>
 295813a:      	addq	$0x30, %rsp
 295813e:      	testq	%rax, %rax
 2958141:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958147:      	cmpl	$0x1, %ebp
 295814a:      	movq	0x10(%rsp), %rbp
 295814f:      	jne	0x2958197 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b7>
 2958151:      	movq	0x220(%rsp), %r10
 2958159:      	movl	0x8(%r10), %eax
 295815d:      	movq	(%rsp), %rdi
 2958161:      	movl	$0x3e, %esi
 2958166:      	movq	%rbp, %rdx
 2958169:      	movl	0xc(%rsp), %ecx
 295816d:      	movq	%r14, %r8
 2958170:      	movl	%r15d, %r9d
 2958173:      	pushq	0x230(%rsp)
 295817a:      	pushq	%rbx
 295817b:      	pushq	%rax
 295817c:      	pushq	(%r10)
 295817f:      	pushq	0x48(%rsp)
 2958183:      	pushq	%r12
 2958185:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295818a:      	addq	$0x30, %rsp
 295818e:      	testq	%rax, %rax
 2958191:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958197:      	movl	0x148(%rbx), %r13d
 295819e:      	cmpl	$0x5, %r13d
 29581a2:      	jl	0x29581e6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x306>
 29581a4:      	subq	$0x8, %rsp
 29581a8:      	movq	0x8(%rsp), %rdi
 29581ad:      	movl	$0x3e, %esi
 29581b2:      	movq	%rbp, %rdx
 29581b5:      	movl	0x14(%rsp), %ecx
 29581b9:      	movq	%r14, %r8
 29581bc:      	movl	%r15d, %r9d
 29581bf:      	pushq	0x238(%rsp)
 29581c6:      	pushq	%rbx
 29581c7:      	pushq	0x238(%rsp)
 29581ce:      	pushq	0x48(%rsp)
 29581d2:      	pushq	%r12
 29581d4:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29581d9:      	addq	$0x30, %rsp
 29581dd:      	testq	%rax, %rax
 29581e0:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29581e6:      	movl	%r13d, 0x9c(%rsp)
 29581ee:      	movl	0x1e4(%rbx), %eax
 29581f4:      	subq	$0x8, %rsp
 29581f8:      	movq	0x8(%rsp), %r13
 29581fd:      	movq	%r13, %rdi
 2958200:      	movl	$0x3e, %esi
 2958205:      	movq	%rbp, %rdx
 2958208:      	movl	%r15d, %r9d
 295820b:      	movl	0x14(%rsp), %r15d
 2958210:      	movl	%r15d, %ecx
 2958213:      	movq	%r14, %r8
 2958216:      	movq	0x238(%rsp), %rbp
 295821e:      	pushq	%rbp
 295821f:      	pushq	%rax
 2958220:      	pushq	0x238(%rsp)
 2958227:      	movq	0x48(%rsp), %rbp
 295822c:      	pushq	%rbp
 295822d:      	pushq	%r12
 295822f:      	callq	0x2969d50 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958234:      	addq	$0x30, %rsp
 2958238:      	testq	%rax, %rax
 295823b:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958241:      	subq	$0x8, %rsp
 2958245:      	movq	%r13, %rdi
 2958248:      	movl	$0x3e, %esi
 295824d:      	movq	0x18(%rsp), %rdx
 2958252:      	movl	%r15d, %ecx
 2958255:      	movq	%r14, %r8
 2958258:      	movl	0x60(%rsp), %r9d
 295825d:      	pushq	0x238(%rsp)
 2958264:      	pushq	%rbp
 2958265:      	pushq	%r12
 2958267:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295826c:      	addq	$0x20, %rsp
 2958270:      	testq	%rax, %rax
 2958273:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958279:      	movq	%r13, %rdi
 295827c:      	movl	$0x3e, %esi
 2958281:      	movq	0x10(%rsp), %rdx
 2958286:      	movl	%r15d, %ecx
 2958289:      	movq	%r14, %r8
 295828c:      	movl	0x58(%rsp), %r9d
 2958291:      	pushq	0x230(%rsp)
 2958298:      	pushq	%rbx
 2958299:      	pushq	%rbp
 295829a:      	pushq	%r12
 295829c:      	callq	0x2971bb0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29582a1:      	addq	$0x20, %rsp
 29582a5:      	testq	%rax, %rax
 29582a8:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29582ae:      	movq	%r13, %rdi
 29582b1:      	movl	$0x3e, %esi
 29582b6:      	movq	0x10(%rsp), %rdx
 29582bb:      	movl	%r15d, %ecx
 29582be:      	movq	%r14, %r8
 29582c1:      	movl	0x58(%rsp), %r9d
 29582c6:      	pushq	0x230(%rsp)
 29582cd:      	movq	%rbx, %r13
 29582d0:      	pushq	%rbx
 29582d1:      	pushq	0x230(%rsp)
 29582d8:      	movq	%r12, %r15
 29582db:      	pushq	%r12
 29582dd:      	callq	0x2974330 <_ZL20lowerShuffleAsVTRUNCRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29582e2:      	addq	$0x20, %rsp
 29582e6:      	testq	%rax, %rax
 29582e9:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29582ef:      	movq	(%rsp), %rdi
 29582f3:      	movl	$0x3e, %esi
 29582f8:      	movq	0x10(%rsp), %rdx
 29582fd:      	movl	0xc(%rsp), %ecx
 2958301:      	movq	0x20(%rsp), %r8
 2958306:      	movl	0x58(%rsp), %r9d
 295830b:      	pushq	0x230(%rsp)
 2958312:      	pushq	%r13
 2958314:      	pushq	0x38(%rsp)
 2958318:      	pushq	%r15
 295831a:      	callq	0x2966110 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295831f:      	addq	$0x20, %rsp
 2958323:      	testq	%rax, %rax
 2958326:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295832c:      	subq	$0x8, %rsp
 2958330:      	movq	0x8(%rsp), %rdi
 2958335:      	movl	$0x3e, %esi
 295833a:      	movq	0x18(%rsp), %rdx
 295833f:      	movl	0x14(%rsp), %ecx
 2958343:      	movq	0x28(%rsp), %r8
 2958348:      	movl	0x60(%rsp), %r9d
 295834d:      	pushq	0x238(%rsp)
 2958354:      	pushq	0x38(%rsp)
 2958358:      	pushq	%r15
 295835a:      	callq	0x296a5b0 <_ZL22lowerShuffleAsBitBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295835f:      	addq	$0x20, %rsp
 2958363:      	testq	%rax, %rax
 2958366:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295836c:      	subq	$0x8, %rsp
 2958370:      	movq	0x8(%rsp), %rdi
 2958375:      	movl	$0x3e, %esi
 295837a:      	movq	0x18(%rsp), %rdx
 295837f:      	movl	0x14(%rsp), %ecx
 2958383:      	movq	0x28(%rsp), %r8
 2958388:      	movl	0x60(%rsp), %r9d
 295838d:      	pushq	0x238(%rsp)
 2958394:      	pushq	%r13
 2958396:      	pushq	0x238(%rsp)
 295839d:      	pushq	0x48(%rsp)
 29583a1:      	pushq	%r15
 29583a3:      	callq	0x2974b80 <_ZL27lowerShuffleAsByteShiftMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29583a8:      	addq	$0x30, %rsp
 29583ac:      	testq	%rax, %rax
 29583af:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29583b5:      	movq	%r15, %rdi
 29583b8:      	movq	0x28(%rsp), %rsi
 29583bd:      	movl	$0x1, %edx
 29583c2:      	xorl	%ecx, %ecx
 29583c4:      	callq	0x29754b0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 29583c9:      	movl	%eax, %ebx
 29583cb:      	cmpl	$0x1, %eax
 29583ce:      	je	0x295c14a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x426a>
 29583d4:      	cmpl	$0x2, %ebx
 29583d7:      	jne	0x295c158 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4278>
 29583dd:      	movl	0x148(%r13), %eax
 29583e4:      	cmpl	$0x5, %eax
 29583e7:      	jl	0x295c158 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4278>
 29583ed:      	cmpb	$0x0, 0x1d1(%r13)
 29583f5:      	jne	0x295c158 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4278>
 29583fb:      	movb	$0x1, %r15b
 29583fe:      	cmpl	$0x8, %eax
 2958401:      	jb	0x295c76b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x488b>
 2958407:      	movq	0x10(%rsp), %rax
 295840c:      	movl	0x18(%rax), %eax
 295840f:      	cmpl	$0xf3, %eax
 2958414:      	jne	0x295842c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54c>
 2958416:      	movq	0x10(%rsp), %rcx
 295841b:      	movq	0x28(%rcx), %rax
 295841f:      	movq	(%rax), %rcx
 2958422:      	movl	0x18(%rcx), %eax
 2958425:      	cmpl	$0xf3, %eax
 295842a:      	je	0x295841b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x53b>
 295842c:      	cmpl	$0xa5, %eax
 2958431:      	jne	0x295c76b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x488b>
 2958437:      	movq	0x20(%rsp), %rax
 295843c:      	movl	0x18(%rax), %eax
 295843f:      	cmpl	$0xf3, %eax
 2958444:      	jne	0x295845c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x57c>
 2958446:      	movq	0x20(%rsp), %rcx
 295844b:      	movq	0x28(%rcx), %rax
 295844f:      	movq	(%rax), %rcx
 2958452:      	movl	0x18(%rcx), %eax
 2958455:      	cmpl	$0xf3, %eax
 295845a:      	je	0x295844b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x56b>
 295845c:      	cmpl	$0xa5, %eax
 2958461:      	jne	0x295c76b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x488b>
 2958467:      	movq	0x10(%rsp), %rdi
 295846c:      	movl	0xc(%rsp), %esi
 2958470:      	movq	0x20(%rsp), %rdx
 2958475:      	movl	0x58(%rsp), %ecx
 2958479:      	movq	0x230(%rsp), %rbx
 2958481:      	movq	%rbx, %r8
 2958484:      	movq	(%rsp), %r14
 2958488:      	movq	%r14, %r9
 295848b:      	callq	0x284b410 <_ZL16concatSubVectorsN4llvm7SDValueES0_RNS_12SelectionDAGERKNS_5SDLocE>
 2958490:      	movq	%rax, %r15
 2958493:      	movl	%edx, %ebp
 2958495:      	movl	0x148(%r13), %esi
 295849c:      	movl	$0x3f, %edi
 29584a1:      	movq	%rbx, %rdx
 29584a4:      	movq	%r14, %rcx
 29584a7:      	callq	0x2842550 <_ZL13getZeroVectorN4llvm3MVTERKNS_12X86SubtargetERNS_12SelectionDAGERKNS_5SDLocE>
 29584ac:      	movq	%rax, %r13
 29584af:      	movl	%edx, %r12d
 29584b2:      	subq	$0x8, %rsp
 29584b6:      	movq	$0x0, 0x18(%rsp)
 29584bf:      	movl	$0xee, %esi
 29584c4:      	movq	%rbx, %rdi
 29584c7:      	movq	%r14, %rdx
 29584ca:      	movl	$0x5, %ecx
 29584cf:      	xorl	%r8d, %r8d
 29584d2:      	movl	$0x1, %r9d
 29584d8:      	pushq	$0x0
 29584da:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 29584df:      	addq	$0x10, %rsp
 29584e3:      	movq	%rax, 0xa0(%rsp)
 29584eb:      	movl	%edx, 0xa8(%rsp)
 29584f2:      	movq	%r13, 0x30(%rsp)
 29584f7:      	movl	%r12d, 0x38(%rsp)
 29584fc:      	movq	%r15, 0x70(%rsp)
 2958501:      	movl	%ebp, 0x78(%rsp)
 2958505:      	movq	0x3b0(%rbx), %rax
 295850c:      	movl	$0x0, %r9d
 2958512:      	testq	%rax, %rax
 2958515:      	je	0x295851b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x63b>
 2958517:      	movl	0x8(%rax), %r9d
 295851b:      	subq	$0x30, %rsp
 295851f:      	movups	0xd0(%rsp), %xmm0
 2958527:      	movups	%xmm0, 0x20(%rsp)
 295852c:      	movups	0x60(%rsp), %xmm0
 2958531:      	movups	%xmm0, 0x10(%rsp)
 2958536:      	movups	0xa0(%rsp), %xmm0
 295853e:      	movups	%xmm0, (%rsp)
 2958542:      	movq	0x260(%rsp), %r15
 295854a:      	movq	%r15, %rdi
 295854d:      	movl	$0x239, %esi            # imm = 0x239
 2958552:      	movq	0x30(%rsp), %rbx
 2958557:      	movq	%rbx, %rdx
 295855a:      	movl	$0x3f, %ecx
 295855f:      	xorl	%r8d, %r8d
 2958562:      	callq	0x5e2ac90 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 2958567:      	addq	$0x30, %rsp
 295856b:      	movl	%edx, %r8d
 295856e:      	movq	%r15, %rdi
 2958571:      	movl	$0x4d, %esi
 2958576:      	xorl	%edx, %edx
 2958578:      	movq	%rax, %rcx
 295857b:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2958580:      	movq	%rax, %r14
 2958583:      	movl	%edx, %ebp
 2958585:      	movq	%rax, %rdi
 2958588:      	movl	%edx, %esi
 295858a:      	xorl	%edx, %edx
 295858c:      	movq	%r15, %rcx
 295858f:      	movq	%rbx, %r8
 2958592:      	movl	$0x80, %r9d
 2958598:      	callq	0x28e5b50 <_ZL16extractSubVectorN4llvm7SDValueEjRNS_12SelectionDAGERKNS_5SDLocEj>
 295859d:      	movq	%rax, %r13
 29585a0:      	movl	%edx, %r12d
 29585a3:      	movq	%r14, %rdi
 29585a6:      	movl	%ebp, %esi
 29585a8:      	movl	$0x4, %edx
 29585ad:      	movq	%r15, %rcx
 29585b0:      	movq	%rbx, %r8
 29585b3:      	movl	$0x80, %r9d
 29585b9:      	callq	0x28e5b50 <_ZL16extractSubVectorN4llvm7SDValueEjRNS_12SelectionDAGERKNS_5SDLocEj>
 29585be:      	movq	%rax, 0xa0(%rsp)
 29585c6:      	movl	%edx, 0xa8(%rsp)
 29585cd:      	movl	0x18(%rsp), %eax
 29585d1:      	movl	%eax, 0xac(%rsp)
 29585d8:      	movq	%r13, 0x30(%rsp)
 29585dd:      	movl	%r12d, 0x38(%rsp)
 29585e2:      	movq	0x3b0(%r15), %rax
 29585e9:      	testq	%rax, %rax
 29585ec:      	je	0x29585f6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x716>
 29585ee:      	movl	0x8(%rax), %eax
 29585f1:      	movq	%rax, 0x10(%rsp)
 29585f6:      	subq	$0x20, %rsp
 29585fa:      	movups	0xc0(%rsp), %xmm0
 2958602:      	movups	%xmm0, 0x10(%rsp)
 2958607:      	movdqu	0x50(%rsp), %xmm0
 295860d:      	movdqu	%xmm0, (%rsp)
 2958612:      	movq	0x250(%rsp), %rdi
 295861a:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295861f:      	movq	0x20(%rsp), %rdx
 2958624:      	movl	$0x3e, %ecx
 2958629:      	xorl	%r8d, %r8d
 295862c:      	movq	0x30(%rsp), %r9
 2958631:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 2958636:      	addq	$0x20, %rsp
 295863a:      	movl	%edx, %r8d
 295863d:      	jmp	0x295ca6c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4b8c>
 2958642:      	addl	$-0x6f, %eax
 2958645:      	cmpl	$0x27, %eax
 2958648:      	ja	0x2958e63 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf83>
 295864e:      	leaq	-0x1a865b9(%rip), %rcx  # 0xed209c <.LCPI63_2+0xb5fc>
 2958655:      	movslq	(%rcx,%rax,4), %rax
 2958659:      	addq	%rcx, %rax
 295865c:      	jmpq	*%rax
 295865e:      	movq	%rdi, (%rsp)
 2958662:      	movdqu	(%rdx), %xmm0
 2958666:      	movdqa	%xmm0, 0x80(%rsp)
 295866f:      	testq	%rbx, %rbx
 2958672:      	je	0x2959a4d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b6d>
 2958678:      	leaq	(,%rbx,4), %rcx
 2958680:      	addq	$-0x4, %rcx
 2958684:      	xorl	%edx, %edx
 2958686:      	movq	%r12, %rax
 2958689:      	cmpq	$0x1c, %rcx
 295868d:      	jb	0x2958705 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x825>
 295868f:      	shrq	$0x2, %rcx
 2958693:      	incq	%rcx
 2958696:      	movq	%rcx, %rsi
 2958699:      	andq	$-0x8, %rsi
 295869d:      	leaq	(%r12,%rsi,4), %rax
 29586a1:      	pxor	%xmm0, %xmm0
 29586a5:      	xorl	%edx, %edx
 29586a7:      	movdqa	-0x1b3a0bf(%rip), %xmm2 # 0xe1e5f0 <.LCPI649_0>
 29586af:      	pxor	%xmm1, %xmm1
 29586b3:      	nopw	%cs:(%rax,%rax)
 29586bd:      	nopl	(%rax)
 29586c0:      	movdqu	(%r12,%rdx,4), %xmm3
 29586c6:      	movdqu	0x10(%r12,%rdx,4), %xmm4
 29586cd:      	pcmpgtd	%xmm2, %xmm3
 29586d1:      	psubd	%xmm3, %xmm1
 29586d5:      	pcmpgtd	%xmm2, %xmm4
 29586d9:      	psubd	%xmm4, %xmm0
 29586dd:      	addq	$0x8, %rdx
 29586e1:      	cmpq	%rdx, %rsi
 29586e4:      	jne	0x29586c0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x7e0>
 29586e6:      	paddd	%xmm1, %xmm0
 29586ea:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 29586ef:      	paddd	%xmm0, %xmm1
 29586f3:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 29586f8:      	paddd	%xmm1, %xmm0
 29586fc:      	movd	%xmm0, %edx
 2958700:      	cmpq	%rsi, %rcx
 2958703:      	je	0x2958724 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x844>
 2958705:      	leaq	(%r12,%rbx,4), %rcx
 2958709:      	nopl	(%rax)
 2958710:      	xorl	%esi, %esi
 2958712:      	cmpl	$0x8, (%rax)
 2958715:      	setge	%sil
 2958719:      	addl	%esi, %edx
 295871b:      	addq	$0x4, %rax
 295871f:      	cmpq	%rcx, %rax
 2958722:      	jne	0x2958710 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x830>
 2958724:      	cmpb	$0x1, 0x181(%r14)
 295872c:      	je	0x2959a5d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b7d>
 2958732:      	jmp	0x295a251 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2371>
 2958737:      	movdqu	(%rdx), %xmm0
 295873b:      	movdqa	%xmm0, 0x170(%rsp)
 2958744:      	movq	%r12, 0x130(%rsp)
 295874c:      	movq	%rbx, 0x138(%rsp)
 2958754:      	movq	%rbp, 0x60(%rsp)
 2958759:      	movl	%r11d, 0x68(%rsp)
 295875e:      	movq	0x170(%rsp), %r13
 2958766:      	movq	%r14, %rax
 2958769:      	movl	0x178(%rsp), %r14d
 2958771:      	movl	$0x30, %esi
 2958776:      	movq	%rbp, %rdx
 2958779:      	movl	%r11d, %ecx
 295877c:      	movq	%r13, %r8
 295877f:      	movl	%r14d, %r9d
 2958782:      	pushq	$0x0
 2958784:      	pushq	%r15
 2958786:      	pushq	%rax
 2958787:      	pushq	%r10
 2958789:      	pushq	%rbx
 295878a:      	pushq	%r12
 295878c:      	movq	%rbp, %r15
 295878f:      	movl	%r11d, %ebp
 2958792:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2958797:      	addq	$0x30, %rsp
 295879b:      	testq	%rax, %rax
 295879e:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29587a4:      	movq	(%rsp), %rdi
 29587a8:      	movl	$0x30, %esi
 29587ad:      	movq	%r15, %rdx
 29587b0:      	movl	%ebp, %ecx
 29587b2:      	movq	%r13, %r8
 29587b5:      	movl	%r14d, %r9d
 29587b8:      	pushq	0x230(%rsp)
 29587bf:      	pushq	0x230(%rsp)
 29587c6:      	pushq	%rbx
 29587c7:      	pushq	%r12
 29587c9:      	callq	0x2966110 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29587ce:      	addq	$0x20, %rsp
 29587d2:      	testq	%rax, %rax
 29587d5:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29587db:      	movq	(%rsp), %rdi
 29587df:      	movl	$0x30, %esi
 29587e4:      	movq	%r15, %rdx
 29587e7:      	movl	%ebp, %ecx
 29587e9:      	movq	%r13, %r8
 29587ec:      	movl	%r14d, %r9d
 29587ef:      	pushq	0x230(%rsp)
 29587f6:      	pushq	0x230(%rsp)
 29587fd:      	pushq	%rbx
 29587fe:      	pushq	%r12
 2958800:      	callq	0x2971bb0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958805:      	addq	$0x20, %rsp
 2958809:      	testq	%rax, %rax
 295880c:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958812:      	subq	$0x8, %rsp
 2958816:      	movq	0x8(%rsp), %rdi
 295881b:      	movl	$0x30, %esi
 2958820:      	movq	%r15, %rdx
 2958823:      	movl	%ebp, %ecx
 2958825:      	movq	%r13, %r8
 2958828:      	movl	%r14d, %r9d
 295882b:      	pushq	0x238(%rsp)
 2958832:      	pushq	0x238(%rsp)
 2958839:      	movq	0x238(%rsp), %rax
 2958841:      	pushq	%rax
 2958842:      	pushq	%rbx
 2958843:      	pushq	%r12
 2958845:      	callq	0x296d960 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295884a:      	addq	$0x30, %rsp
 295884e:      	testq	%rax, %rax
 2958851:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958857:      	movq	%r13, 0x18(%rsp)
 295885c:      	movl	%r14d, 0x20(%rsp)
 2958861:      	movq	(%rsp), %rdi
 2958865:      	movl	$0x30, %esi
 295886a:      	movq	%r15, %rdx
 295886d:      	movl	%ebp, %ecx
 295886f:      	movq	%r12, %r8
 2958872:      	movq	0x220(%rsp), %r13
 295887a:      	movq	%r13, %r9
 295887d:      	pushq	0x230(%rsp)
 2958884:      	movq	0x230(%rsp), %r14
 295888c:      	pushq	%r14
 295888e:      	callq	0x2971550 <_ZL21lowerShuffleWithVPMOVRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958893:      	addq	$0x10, %rsp
 2958897:      	testq	%rax, %rax
 295889a:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29588a0:      	movq	(%rsp), %rdi
 29588a4:      	movl	$0x30, %esi
 29588a9:      	movq	%r15, %rdx
 29588ac:      	movl	%ebp, %ecx
 29588ae:      	movq	0x18(%rsp), %r8
 29588b3:      	movl	0x20(%rsp), %r9d
 29588b8:      	pushq	0x230(%rsp)
 29588bf:      	pushq	%r14
 29588c1:      	pushq	%r13
 29588c3:      	pushq	%r12
 29588c5:      	callq	0x2974330 <_ZL20lowerShuffleAsVTRUNCRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29588ca:      	addq	$0x20, %rsp
 29588ce:      	testq	%rax, %rax
 29588d1:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29588d7:      	movq	0x230(%rsp), %r11
 29588df:      	movl	%ebp, 0xc(%rsp)
 29588e3:      	cmpb	$0x1, 0x1c6(%r14)
 29588eb:      	movq	%r15, %rbp
 29588ee:      	jne	0x2958936 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xa56>
 29588f0:      	movq	0x220(%rsp), %r10
 29588f8:      	movl	0x8(%r10), %eax
 29588fc:      	subq	$0x8, %rsp
 2958900:      	movq	0x8(%rsp), %rdi
 2958905:      	movl	$0x30, %esi
 295890a:      	movq	%rbp, %rdx
 295890d:      	movl	0x14(%rsp), %ecx
 2958911:      	movq	0x20(%rsp), %r8
 2958916:      	movl	0x28(%rsp), %r9d
 295891b:      	pushq	%r11
 295891d:      	pushq	%rax
 295891e:      	pushq	(%r10)
 2958921:      	pushq	%rbx
 2958922:      	pushq	%r12
 2958924:      	callq	0x2973ed0 <_ZL21lowerShuffleWithSSE4ARKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGE>
 2958929:      	addq	$0x30, %rsp
 295892d:      	testq	%rax, %rax
 2958930:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958936:      	testq	%rbx, %rbx
 2958939:      	movq	(%rsp), %rdi
 295893d:      	movl	0xc(%rsp), %ecx
 2958941:      	movl	0x20(%rsp), %r9d
 2958946:      	movq	0x18(%rsp), %r8
 295894b:      	je	0x295bb91 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3cb1>
 2958951:      	leaq	(,%rbx,4), %r10
 2958959:      	addq	$-0x4, %r10
 295895d:      	xorl	%r15d, %r15d
 2958960:      	movq	%r12, %rax
 2958963:      	cmpq	$0x1c, %r10
 2958967:      	jb	0x29589d7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xaf7>
 2958969:      	shrq	$0x2, %r10
 295896d:      	incq	%r10
 2958970:      	movq	%r10, %rdx
 2958973:      	andq	$-0x8, %rdx
 2958977:      	leaq	(%r12,%rdx,4), %rax
 295897b:      	pxor	%xmm0, %xmm0
 295897f:      	xorl	%esi, %esi
 2958981:      	movdqa	-0x1b413d9(%rip), %xmm2 # 0xe175b0 <.LCPI774_0>
 2958989:      	pxor	%xmm1, %xmm1
 295898d:      	movdqu	(%r12,%rsi,4), %xmm3
 2958993:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 295899a:      	pcmpgtd	%xmm2, %xmm3
 295899e:      	psubd	%xmm3, %xmm1
 29589a2:      	pcmpgtd	%xmm2, %xmm4
 29589a6:      	psubd	%xmm4, %xmm0
 29589aa:      	addq	$0x8, %rsi
 29589ae:      	cmpq	%rsi, %rdx
 29589b1:      	jne	0x295898d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xaad>
 29589b3:      	paddd	%xmm1, %xmm0
 29589b7:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 29589bc:      	paddd	%xmm0, %xmm1
 29589c0:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 29589c5:      	paddd	%xmm1, %xmm0
 29589c9:      	movd	%xmm0, %r15d
 29589ce:      	cmpq	%rdx, %r10
 29589d1:      	movq	(%rsp), %rdi
 29589d5:      	je	0x29589ef <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xb0f>
 29589d7:      	leaq	(%r12,%rbx,4), %rsi
 29589db:      	xorl	%edx, %edx
 29589dd:      	cmpl	$0x10, (%rax)
 29589e0:      	setge	%dl
 29589e3:      	addl	%edx, %r15d
 29589e6:      	addq	$0x4, %rax
 29589ea:      	cmpq	%rsi, %rax
 29589ed:      	jne	0x29589db <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xafb>
 29589ef:      	testl	%r15d, %r15d
 29589f2:      	je	0x295bb91 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3cb1>
 29589f8:      	movl	0x1e4(%r14), %eax
 29589ff:      	subq	$0x8, %rsp
 2958a03:      	movl	$0x30, %esi
 2958a08:      	movq	%rbp, %rdx
 2958a0b:      	movq	%r14, %rbp
 2958a0e:      	movl	%r9d, %r14d
 2958a11:      	movq	%r8, %r13
 2958a14:      	movq	0x238(%rsp), %r10
 2958a1c:      	pushq	%r10
 2958a1e:      	pushq	%rax
 2958a1f:      	pushq	0x238(%rsp)
 2958a26:      	pushq	%rbx
 2958a27:      	pushq	%r12
 2958a29:      	callq	0x2969d50 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958a2e:      	addq	$0x30, %rsp
 2958a32:      	testq	%rax, %rax
 2958a35:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958a3b:      	movq	0x60(%rsp), %rdx
 2958a40:      	movl	0x68(%rsp), %ecx
 2958a44:      	movdqu	0x130(%rsp), %xmm0
 2958a4d:      	subq	$0x20, %rsp
 2958a51:      	movq	0x250(%rsp), %rax
 2958a59:      	movq	%rax, 0x10(%rsp)
 2958a5e:      	movdqu	%xmm0, (%rsp)
 2958a63:      	movq	0x20(%rsp), %rdi
 2958a68:      	movl	$0x30, %esi
 2958a6d:      	movq	%r13, %r8
 2958a70:      	movl	%r14d, %r9d
 2958a73:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2958a78:      	addq	$0x20, %rsp
 2958a7c:      	testq	%rax, %rax
 2958a7f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958a85:      	movq	0x60(%rsp), %rdx
 2958a8a:      	movl	0x68(%rsp), %ecx
 2958a8e:      	movdqu	0x130(%rsp), %xmm0
 2958a97:      	subq	$0x30, %rsp
 2958a9b:      	movq	0x260(%rsp), %rax
 2958aa3:      	movq	%rax, 0x20(%rsp)
 2958aa8:      	movq	%rbp, 0x18(%rsp)
 2958aad:      	movq	0x250(%rsp), %rax
 2958ab5:      	movq	%rax, 0x10(%rsp)
 2958aba:      	movdqu	%xmm0, (%rsp)
 2958abf:      	movq	0x30(%rsp), %rdi
 2958ac4:      	movl	$0x30, %esi
 2958ac9:      	movq	0x48(%rsp), %r8
 2958ace:      	movl	0x50(%rsp), %r9d
 2958ad3:      	callq	0x2974b80 <_ZL27lowerShuffleAsByteShiftMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958ad8:      	addq	$0x30, %rsp
 2958adc:      	testq	%rax, %rax
 2958adf:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958ae5:      	movq	0x18(%rsp), %rax
 2958aea:      	movl	0x18(%rax), %eax
 2958aed:      	addl	$-0x35, %eax
 2958af0:      	xorl	%r12d, %r12d
 2958af3:      	movl	%eax, 0x10(%rsp)
 2958af7:      	cmpl	$0x2, %eax
 2958afa:      	setb	%r12b
 2958afe:      	movq	0x130(%rsp), %rbx
 2958b06:      	movq	0x138(%rsp), %r14
 2958b0e:      	movq	%rbx, %rdi
 2958b11:      	movq	%r14, %rsi
 2958b14:      	movl	$0x1, %edx
 2958b19:      	movl	%r12d, %ecx
 2958b1c:      	callq	0x29754b0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 2958b21:      	movl	%eax, %r13d
 2958b24:      	cmpl	$0x1, %eax
 2958b27:      	setne	%al
 2958b2a:      	cmpl	$0x4, 0x148(%rbp)
 2958b31:      	jl	0x295be82 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3fa2>
 2958b37:      	orb	%al, %r12b
 2958b3a:      	je	0x295be82 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3fa2>
 2958b40:      	movb	$0x0, 0x30(%rsp)
 2958b45:      	movb	$0x0, 0x70(%rsp)
 2958b4a:      	movq	0x60(%rsp), %rdx
 2958b4f:      	movl	0x68(%rsp), %ecx
 2958b53:      	leaq	0x70(%rsp), %rax
 2958b58:      	leaq	0x30(%rsp), %r10
 2958b5d:      	movq	(%rsp), %rdi
 2958b61:      	movl	$0x30, %esi
 2958b66:      	movq	0x18(%rsp), %r8
 2958b6b:      	movl	0x20(%rsp), %r9d
 2958b70:      	pushq	%rax
 2958b71:      	pushq	%r10
 2958b73:      	pushq	0x240(%rsp)
 2958b7a:      	pushq	0x238(%rsp)
 2958b81:      	pushq	%r14
 2958b83:      	pushq	%rbx
 2958b84:      	callq	0x2975580 <_ZL28lowerShuffleAsBlendOfPSHUFBsRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGERbSC_>
 2958b89:      	addq	$0x30, %rsp
 2958b8d:      	movq	%rax, %rbx
 2958b90:      	movl	%edx, %r14d
 2958b93:      	cmpb	$0x1, 0x30(%rsp)
 2958b98:      	jne	0x295d7e2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5902>
 2958b9e:      	cmpb	$0x0, 0x70(%rsp)
 2958ba3:      	je	0x295d7e2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5902>
 2958ba9:      	cmpl	$0x5, 0x148(%rbp)
 2958bb0:      	jl	0x2958c12 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xd32>
 2958bb2:      	movq	0x60(%rsp), %rdx
 2958bb7:      	movl	0x68(%rsp), %ecx
 2958bbb:      	movdqu	0x130(%rsp), %xmm0
 2958bc4:      	subq	$0x30, %rsp
 2958bc8:      	movq	0x260(%rsp), %rax
 2958bd0:      	movq	%rax, 0x20(%rsp)
 2958bd5:      	movq	%rbp, 0x18(%rsp)
 2958bda:      	movq	0x250(%rsp), %rax
 2958be2:      	movq	%rax, 0x10(%rsp)
 2958be7:      	movdqu	%xmm0, (%rsp)
 2958bec:      	movq	0x30(%rsp), %rdi
 2958bf1:      	movl	$0x30, %esi
 2958bf6:      	movq	0x48(%rsp), %r8
 2958bfb:      	movl	0x50(%rsp), %r9d
 2958c00:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958c05:      	addq	$0x30, %rsp
 2958c09:      	testq	%rax, %rax
 2958c0c:      	jne	0x295d7dc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58fc>
 2958c12:      	movq	0x60(%rsp), %rdx
 2958c17:      	movl	0x68(%rsp), %ecx
 2958c1b:      	movdqu	0x130(%rsp), %xmm0
 2958c24:      	subq	$0x20, %rsp
 2958c28:      	movq	0x250(%rsp), %rax
 2958c30:      	movq	%rax, 0x10(%rsp)
 2958c35:      	movdqu	%xmm0, (%rsp)
 2958c3a:      	movq	0x20(%rsp), %rdi
 2958c3f:      	movl	$0x30, %esi
 2958c44:      	movq	0x38(%rsp), %r8
 2958c49:      	movl	0x40(%rsp), %r9d
 2958c4e:      	callq	0x296b390 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958c53:      	addq	$0x20, %rsp
 2958c57:      	testq	%rax, %rax
 2958c5a:      	jne	0x295d7dc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58fc>
 2958c60:      	cmpb	$0x1, 0x1cf(%rbp)
 2958c67:      	jne	0x295c613 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4733>
 2958c6d:      	movq	0x130(%rsp), %rdx
 2958c75:      	movq	0x138(%rsp), %rcx
 2958c7d:      	movq	0x60(%rsp), %r8
 2958c82:      	movl	0x68(%rsp), %r9d
 2958c87:      	subq	$0x20, %rsp
 2958c8b:      	leaq	0x230(%rsp), %rax
 2958c93:      	movdqu	(%rax), %xmm0
 2958c97:      	movdqu	%xmm0, (%rsp)
 2958c9c:      	movq	0x250(%rsp), %rax
 2958ca4:      	movq	%rax, 0x18(%rsp)
 2958ca9:      	movq	%rbp, 0x10(%rsp)
 2958cae:      	movq	0x20(%rsp), %rdi
 2958cb3:      	movl	$0x30, %esi
 2958cb8:      	callq	0x2981f40 <_ZL21lowerShuffleWithPERMVRKN4llvm5SDLocENS_3MVTENS_8ArrayRefIiEENS_7SDValueES6_RKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958cbd:      	addq	$0x20, %rsp
 2958cc1:      	jmp	0x295d7dc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58fc>
 2958cc6:      	movq	%r14, %rax
 2958cc9:      	movq	(%rdx), %r14
 2958ccc:      	movl	0x8(%rdx), %r13d
 2958cd0:      	subq	$0x8, %rsp
 2958cd4:      	movl	$0x49, %esi
 2958cd9:      	movq	%rbp, %rdx
 2958cdc:      	movl	%r11d, %ecx
 2958cdf:      	movq	%r14, %r8
 2958ce2:      	movl	%r13d, %r9d
 2958ce5:      	pushq	%r15
 2958ce7:      	pushq	%rax
 2958ce8:      	pushq	%r10
 2958cea:      	pushq	%rbx
 2958ceb:      	pushq	%r12
 2958ced:      	movq	%rbp, %r15
 2958cf0:      	movl	%r11d, %ebp
 2958cf3:      	callq	0x296d960 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958cf8:      	addq	$0x30, %rsp
 2958cfc:      	testq	%rax, %rax
 2958cff:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958d05:      	movq	%r13, 0x18(%rsp)
 2958d0a:      	movq	0x228(%rsp), %rsi
 2958d12:      	movq	%r14, 0x20(%rsp)
 2958d17:      	movq	%r15, 0x10(%rsp)
 2958d1c:      	movl	%ebp, 0xc(%rsp)
 2958d20:      	leaq	(,%rbx,4), %r9
 2958d28:      	leaq	(%r12,%rbx,4), %rbp
 2958d2c:      	movq	%rbx, %r13
 2958d2f:      	testq	%rbx, %rbx
 2958d32:      	je	0x2959ab7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1bd7>
 2958d38:      	leaq	-0x4(%r9), %rdi
 2958d3c:      	xorl	%r15d, %r15d
 2958d3f:      	movq	%r12, %r11
 2958d42:      	cmpq	$0x1c, %rdi
 2958d46:      	movl	0xc(%rsp), %ecx
 2958d4a:      	movq	0x220(%rsp), %r10
 2958d52:      	movq	%rsi, %r14
 2958d55:      	jb	0x2958dd0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xef0>
 2958d57:      	shrq	$0x2, %rdi
 2958d5b:      	incq	%rdi
 2958d5e:      	movq	%rdi, %rdx
 2958d61:      	andq	$-0x8, %rdx
 2958d65:      	movq	%r11, %r8
 2958d68:      	leaq	(%r11,%rdx,4), %r12
 2958d6c:      	pxor	%xmm0, %xmm0
 2958d70:      	xorl	%esi, %esi
 2958d72:      	movdqa	-0x1b3d1da(%rip), %xmm2 # 0xe1bba0 <.LCPI702_0>
 2958d7a:      	pxor	%xmm1, %xmm1
 2958d7e:      	nop
 2958d80:      	movdqu	(%r8,%rsi,4), %xmm3
 2958d86:      	movdqu	0x10(%r8,%rsi,4), %xmm4
 2958d8d:      	pcmpgtd	%xmm2, %xmm3
 2958d91:      	psubd	%xmm3, %xmm1
 2958d95:      	pcmpgtd	%xmm2, %xmm4
 2958d99:      	psubd	%xmm4, %xmm0
 2958d9d:      	addq	$0x8, %rsi
 2958da1:      	cmpq	%rsi, %rdx
 2958da4:      	jne	0x2958d80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xea0>
 2958da6:      	paddd	%xmm1, %xmm0
 2958daa:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 2958daf:      	paddd	%xmm0, %xmm1
 2958db3:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2958db8:      	paddd	%xmm1, %xmm0
 2958dbc:      	movd	%xmm0, %r15d
 2958dc1:      	cmpq	%rdx, %rdi
 2958dc4:      	je	0x2958de6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xf06>
 2958dc6:      	nopw	%cs:(%rax,%rax)
 2958dd0:      	xorl	%edx, %edx
 2958dd2:      	cmpl	$0x4, (%r12)
 2958dd7:      	setge	%dl
 2958dda:      	addl	%edx, %r15d
 2958ddd:      	addq	$0x4, %r12
 2958de1:      	cmpq	%rbp, %r12
 2958de4:      	jne	0x2958dd0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xef0>
 2958de6:      	cmpb	$0x0, 0x1f7(%r14)
 2958dee:      	movq	(%rsp), %rdi
 2958df2:      	je	0x2959c98 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1db8>
 2958df8:      	movq	%r9, %rbx
 2958dfb:      	movl	$0x49, %esi
 2958e00:      	movq	0x10(%rsp), %rdx
 2958e05:      	movq	0x20(%rsp), %r8
 2958e0a:      	movq	0x18(%rsp), %r9
 2958e0f:      	pushq	$0x1
 2958e11:      	pushq	0x238(%rsp)
 2958e18:      	pushq	%r14
 2958e1a:      	pushq	%r10
 2958e1c:      	pushq	%r13
 2958e1e:      	movq	%r11, %r12
 2958e21:      	pushq	%r11
 2958e23:      	movq	%r13, %r14
 2958e26:      	movl	%ecx, %r13d
 2958e29:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2958e2e:      	addq	$0x30, %rsp
 2958e32:      	testq	%rax, %rax
 2958e35:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958e3b:      	testl	%r15d, %r15d
 2958e3e:      	movq	(%rsp), %rdi
 2958e42:      	movl	%r13d, %ecx
 2958e45:      	movq	0x220(%rsp), %r10
 2958e4d:      	movq	%r14, %r13
 2958e50:      	movq	0x228(%rsp), %r14
 2958e58:      	jne	0x2959ca4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1dc4>
 2958e5e:      	jmp	0x2959b19 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c39>
 2958e63:      	movdqu	(%rdx), %xmm0
 2958e67:      	movdqa	%xmm0, 0x80(%rsp)
 2958e70:      	movq	0x80(%rsp), %r15
 2958e78:      	movl	0x18(%r15), %eax
 2958e7c:      	addl	$-0x35, %eax
 2958e7f:      	cmpl	$0x1, %eax
 2958e82:      	ja	0x29591d5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x12f5>
 2958e88:      	movl	0x88(%rsp), %r9d
 2958e90:      	movq	%rdi, %r13
 2958e93:      	movl	$0x5e, %esi
 2958e98:      	movq	%rbp, %rdx
 2958e9b:      	movl	%r11d, %ecx
 2958e9e:      	movq	%r15, %r8
 2958ea1:      	movq	0x230(%rsp), %r15
 2958ea9:      	pushq	%r15
 2958eab:      	pushq	%r14
 2958ead:      	pushq	%rbx
 2958eae:      	pushq	%r12
 2958eb0:      	movq	%r12, %rbx
 2958eb3:      	movq	%rbp, %r12
 2958eb6:      	movl	%r11d, %ebp
 2958eb9:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958ebe:      	addq	$0x20, %rsp
 2958ec2:      	testq	%rax, %rax
 2958ec5:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958ecb:      	movq	%rbx, %r14
 2958ece:      	movq	%r13, (%rsp)
 2958ed2:      	movq	0x30(%r12), %rax
 2958ed7:      	movl	%ebp, %ecx
 2958ed9:      	shlq	$0x4, %rcx
 2958edd:      	cmpw	$0x49, (%rax,%rcx)
 2958ee2:      	movl	%ebp, %r13d
 2958ee5:      	jne	0x295a6d5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x27f5>
 2958eeb:      	movq	%r12, %rbp
 2958eee:      	jmp	0x295aee5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3005>
 2958ef3:      	movq	(%rdx), %r15
 2958ef6:      	movl	0x8(%rdx), %r9d
 2958efa:      	movl	0x18(%r15), %eax
 2958efe:      	addl	$-0x35, %eax
 2958f01:      	cmpl	$0x1, %eax
 2958f04:      	ja	0x29594d0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x15f0>
 2958f0a:      	movq	%rdi, %r13
 2958f0d:      	movl	$0x96, %esi
 2958f12:      	movq	%rbp, %rdx
 2958f15:      	movl	%r11d, %ecx
 2958f18:      	movq	%r15, %r8
 2958f1b:      	movq	0x230(%rsp), %r15
 2958f23:      	pushq	%r15
 2958f25:      	pushq	%r14
 2958f27:      	pushq	%rbx
 2958f28:      	pushq	%r12
 2958f2a:      	movq	%r12, %rbx
 2958f2d:      	movq	%rbp, %r12
 2958f30:      	movl	%r11d, %ebp
 2958f33:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2958f38:      	addq	$0x20, %rsp
 2958f3c:      	testq	%rax, %rax
 2958f3f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2958f45:      	movq	%r12, 0x10(%rsp)
 2958f4a:      	movl	(%rbx), %ecx
 2958f4c:      	movl	0x4(%rbx), %eax
 2958f4f:      	xorl	%edx, %edx
 2958f51:      	cmpl	$0x1, %ecx
 2958f54:      	sete	%dl
 2958f57:      	xorl	%esi, %esi
 2958f59:      	cmpl	$0x1, %eax
 2958f5c:      	sete	%sil
 2958f60:      	movq	%r14, %rdi
 2958f63:      	leal	(%rdx,%rsi,2), %r14d
 2958f67:      	cmpl	$0x7, 0x148(%rdi)
 2958f6e:      	jl	0x295a716 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2836>
 2958f74:      	movl	%r14d, %esi
 2958f77:      	subq	$0x8, %rsp
 2958f7b:      	xorl	%ebx, %ebx
 2958f7d:      	movq	%r15, %rdi
 2958f80:      	movq	%r13, %rdx
 2958f83:      	movl	$0x5, %ecx
 2958f88:      	xorl	%r8d, %r8d
 2958f8b:      	movl	$0x1, %r9d
 2958f91:      	pushq	$0x0
 2958f93:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 2958f98:      	addq	$0x10, %rsp
 2958f9c:      	movq	%rax, 0xa0(%rsp)
 2958fa4:      	movl	%edx, 0xa8(%rsp)
 2958fab:      	movq	0x10(%rsp), %rax
 2958fb0:      	movq	%rax, 0x30(%rsp)
 2958fb5:      	movl	%ebp, 0x38(%rsp)
 2958fb9:      	movq	0x3b0(%r15), %rax
 2958fc0:      	testq	%rax, %rax
 2958fc3:      	je	0x2958fc8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x10e8>
 2958fc5:      	movl	0x8(%rax), %ebx
 2958fc8:      	subq	$0x20, %rsp
 2958fcc:      	movups	0xc0(%rsp), %xmm0
 2958fd4:      	movups	%xmm0, 0x10(%rsp)
 2958fd9:      	movdqu	0x50(%rsp), %xmm0
 2958fdf:      	movdqu	%xmm0, (%rsp)
 2958fe4:      	movq	%r15, %rdi
 2958fe7:      	movl	$0x2cb, %esi            # imm = 0x2CB
 2958fec:      	movq	%r13, %rdx
 2958fef:      	movl	$0x96, %ecx
 2958ff4:      	jmp	0x2959c71 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d91>
 2958ff9:      	movq	0x30(%rbp), %rax
 2958ffd:      	movl	%r11d, %ecx
 2959000:      	shlq	$0x4, %rcx
 2959004:      	cmpw	$0x3e, (%rax,%rcx)
 2959009:      	movq	%rdi, (%rsp)
 295900d:      	jne	0x2959816 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1936>
 2959013:      	movq	%rbx, %r13
 2959016:      	jmp	0x295a04f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x216f>
 295901b:      	movdqu	(%rdx), %xmm0
 295901f:      	movdqa	%xmm0, 0x60(%rsp)
 2959025:      	cmpl	$0x5, 0x148(%r14)
 295902d:      	jl	0x295908c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x11ac>
 295902f:      	movq	0x60(%rsp), %r8
 2959034:      	movl	0x68(%rsp), %r9d
 2959039:      	subq	$0x8, %rsp
 295903d:      	movq	%r15, %rax
 2959040:      	movq	%rbx, %r15
 2959043:      	movq	%rdi, %rbx
 2959046:      	movl	$0x84, %esi
 295904b:      	movq	%rbp, %rdx
 295904e:      	movl	%r11d, %ecx
 2959051:      	pushq	%rax
 2959052:      	pushq	%r14
 2959054:      	pushq	%r10
 2959056:      	pushq	%r15
 2959058:      	pushq	%r12
 295905a:      	movq	%rbp, %r14
 295905d:      	movl	%r11d, %ebp
 2959060:      	movq	%r10, %r13
 2959063:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959068:      	movq	%r13, %r10
 295906b:      	movl	%ebp, %r11d
 295906e:      	movq	%r14, %rbp
 2959071:      	movq	0x258(%rsp), %r14
 2959079:      	movq	%rbx, %rdi
 295907c:      	movq	%r15, %rbx
 295907f:      	addq	$0x30, %rsp
 2959083:      	testq	%rax, %rax
 2959086:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295908c:      	testq	%rbx, %rbx
 295908f:      	je	0x295985f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x197f>
 2959095:      	leaq	(,%rbx,4), %rcx
 295909d:      	addq	$-0x4, %rcx
 29590a1:      	xorl	%r15d, %r15d
 29590a4:      	movq	%r12, %rax
 29590a7:      	cmpq	$0x1c, %rcx
 29590ab:      	jb	0x2959126 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1246>
 29590ad:      	shrq	$0x2, %rcx
 29590b1:      	incq	%rcx
 29590b4:      	movq	%rcx, %rdx
 29590b7:      	andq	$-0x8, %rdx
 29590bb:      	leaq	(%r12,%rdx,4), %rax
 29590bf:      	pxor	%xmm0, %xmm0
 29590c3:      	xorl	%esi, %esi
 29590c5:      	movdqa	-0x1b3d52d(%rip), %xmm2 # 0xe1bba0 <.LCPI702_0>
 29590cd:      	pxor	%xmm1, %xmm1
 29590d1:      	nopw	%cs:(%rax,%rax)
 29590db:      	nopl	(%rax,%rax)
 29590e0:      	movdqu	(%r12,%rsi,4), %xmm3
 29590e6:      	movdqu	0x10(%r12,%rsi,4), %xmm4
 29590ed:      	pcmpgtd	%xmm2, %xmm3
 29590f1:      	psubd	%xmm3, %xmm1
 29590f5:      	pcmpgtd	%xmm2, %xmm4
 29590f9:      	psubd	%xmm4, %xmm0
 29590fd:      	addq	$0x8, %rsi
 2959101:      	cmpq	%rsi, %rdx
 2959104:      	jne	0x29590e0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1200>
 2959106:      	paddd	%xmm1, %xmm0
 295910a:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295910f:      	paddd	%xmm0, %xmm1
 2959113:      	pshufd	$0x55, %xmm1, %xmm0     # xmm0 = xmm1[1,1,1,1]
 2959118:      	paddd	%xmm1, %xmm0
 295911c:      	movd	%xmm0, %r15d
 2959121:      	cmpq	%rdx, %rcx
 2959124:      	je	0x2959144 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1264>
 2959126:      	leaq	(%r12,%rbx,4), %rcx
 295912a:      	nopw	(%rax,%rax)
 2959130:      	xorl	%edx, %edx
 2959132:      	cmpl	$0x4, (%rax)
 2959135:      	setge	%dl
 2959138:      	addl	%edx, %r15d
 295913b:      	addq	$0x4, %rax
 295913f:      	cmpq	%rcx, %rax
 2959142:      	jne	0x2959130 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1250>
 2959144:      	testl	%r15d, %r15d
 2959147:      	je	0x295985f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x197f>
 295914d:      	movq	%rbx, 0x28(%rsp)
 2959152:      	cmpl	$0x2, 0x148(%r14)
 295915a:      	jl	0x295a915 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2a35>
 2959160:      	movq	0x60(%rsp), %r13
 2959165:      	movl	0x68(%rsp), %ebx
 2959169:      	subq	$0x8, %rsp
 295916d:      	movq	%rdi, 0x8(%rsp)
 2959172:      	movl	$0x49, %esi
 2959177:      	movq	%rbp, %rdx
 295917a:      	movl	%r11d, %ecx
 295917d:      	movq	%r13, %r8
 2959180:      	movl	%ebx, %r9d
 2959183:      	movq	0x238(%rsp), %rax
 295918b:      	pushq	%rax
 295918c:      	pushq	%r14
 295918e:      	pushq	%r10
 2959190:      	pushq	0x48(%rsp)
 2959194:      	pushq	%r12
 2959196:      	movq	%r12, 0x88(%rsp)
 295919e:      	movq	%rbp, %r12
 29591a1:      	movl	%r11d, %ebp
 29591a4:      	callq	0x296d960 <_ZL29lowerShuffleAsZeroOrAnyExtendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29591a9:      	addq	$0x30, %rsp
 29591ad:      	testq	%rax, %rax
 29591b0:      	je	0x295a8b7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29d7>
 29591b6:      	movl	%edx, %r8d
 29591b9:      	movq	0x230(%rsp), %rdi
 29591c1:      	movl	$0x84, %esi
 29591c6:      	xorl	%edx, %edx
 29591c8:      	movq	%rax, %rcx
 29591cb:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 29591d0:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29591d5:      	movq	%rbx, 0x28(%rsp)
 29591da:      	cmpl	$0x8, 0x148(%r14)
 29591e2:      	movl	0x88(%rsp), %r13d
 29591ea:      	jl	0x295923a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x135a>
 29591ec:      	movq	%rdi, %rbx
 29591ef:      	movq	%rbp, %rsi
 29591f2:      	movl	%r11d, %edx
 29591f5:      	movq	%r15, %rcx
 29591f8:      	movl	%r13d, %r8d
 29591fb:      	movq	%r12, %r9
 29591fe:      	pushq	0x230(%rsp)
 2959205:      	pushq	0x30(%rsp)
 2959209:      	movq	%rbp, %r14
 295920c:      	movl	%r11d, %ebp
 295920f:      	callq	0x2962b00 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959214:      	movq	0x230(%rsp), %r10
 295921c:      	movl	%ebp, %r11d
 295921f:      	movq	%r14, %rbp
 2959222:      	movq	0x238(%rsp), %r14
 295922a:      	movq	%rbx, %rdi
 295922d:      	addq	$0x10, %rsp
 2959231:      	testq	%rax, %rax
 2959234:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295923a:      	movl	%r11d, 0xc(%rsp)
 295923f:      	movq	%rbp, 0x10(%rsp)
 2959244:      	movq	%rdi, (%rsp)
 2959248:      	movl	$0x5e, %esi
 295924d:      	movq	%rbp, %rdx
 2959250:      	movl	%r11d, %ecx
 2959253:      	movq	%r15, %r8
 2959256:      	movl	%r13d, %r9d
 2959259:      	pushq	$0x0
 295925b:      	movq	0x238(%rsp), %rbp
 2959263:      	movq	%r12, %rbx
 2959266:      	pushq	%rbp
 2959267:      	pushq	%r14
 2959269:      	pushq	%r10
 295926b:      	movl	%r13d, %r12d
 295926e:      	movq	0x48(%rsp), %r13
 2959273:      	pushq	%r13
 2959275:      	pushq	%rbx
 2959276:      	movq	%r10, %rbp
 2959279:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 295927e:      	addq	$0x30, %rsp
 2959282:      	testq	%rax, %rax
 2959285:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295928b:      	movl	0x8(%rbp), %eax
 295928e:      	movq	(%rsp), %rdi
 2959292:      	movl	$0x5e, %esi
 2959297:      	movq	0x10(%rsp), %rdx
 295929c:      	movl	0xc(%rsp), %ecx
 29592a0:      	movq	%r15, %r8
 29592a3:      	movl	%r12d, %r9d
 29592a6:      	pushq	0x230(%rsp)
 29592ad:      	pushq	%r14
 29592af:      	pushq	%rax
 29592b0:      	pushq	(%rbp)
 29592b3:      	pushq	%r13
 29592b5:      	pushq	%rbx
 29592b6:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29592bb:      	addq	$0x30, %rsp
 29592bf:      	testq	%rax, %rax
 29592c2:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29592c8:      	movabsq	$0x200000002, %rax      # imm = 0x200000002
 29592d2:      	xorq	(%rbx), %rax
 29592d5:      	movq	%rax, 0x30(%rsp)
 29592da:      	movl	0x8(%rbp), %eax
 29592dd:      	leaq	0x30(%rsp), %r10
 29592e2:      	movq	(%rsp), %rdi
 29592e6:      	movl	$0x5e, %esi
 29592eb:      	movq	%r15, %rdx
 29592ee:      	movl	%r12d, %ecx
 29592f1:      	movq	0x10(%rsp), %r8
 29592f6:      	movl	0xc(%rsp), %r9d
 29592fb:      	pushq	0x230(%rsp)
 2959302:      	pushq	%r14
 2959304:      	pushq	%rax
 2959305:      	pushq	(%rbp)
 2959308:      	pushq	$0x2
 295930a:      	pushq	%r10
 295930c:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959311:      	addq	$0x30, %rsp
 2959315:      	testq	%rax, %rax
 2959318:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295931e:      	movl	%r12d, 0x18(%rsp)
 2959323:      	movq	0x10(%rsp), %r12
 2959328:      	movl	0xc(%rsp), %ebp
 295932c:      	movl	0x148(%r14), %eax
 2959333:      	movl	%eax, 0x20(%rsp)
 2959337:      	cmpl	$0x5, %eax
 295933a:      	movq	%rbx, %r13
 295933d:      	movq	0x28(%rsp), %rbx
 2959342:      	jl	0x2959384 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x14a4>
 2959344:      	subq	$0x8, %rsp
 2959348:      	movq	0x8(%rsp), %rdi
 295934d:      	movl	$0x5e, %esi
 2959352:      	movq	%r12, %rdx
 2959355:      	movl	%ebp, %ecx
 2959357:      	movq	%r15, %r8
 295935a:      	movl	0x20(%rsp), %r9d
 295935f:      	pushq	0x238(%rsp)
 2959366:      	pushq	%r14
 2959368:      	pushq	0x238(%rsp)
 295936f:      	pushq	%rbx
 2959370:      	pushq	%r13
 2959372:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959377:      	addq	$0x30, %rsp
 295937b:      	testq	%rax, %rax
 295937e:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959384:      	subq	$0x8, %rsp
 2959388:      	movq	0x8(%rsp), %rdi
 295938d:      	movl	$0x5e, %esi
 2959392:      	movq	%r12, %rdx
 2959395:      	movl	%ebp, %ecx
 2959397:      	movq	%r15, %r8
 295939a:      	movl	0x20(%rsp), %r9d
 295939f:      	pushq	0x238(%rsp)
 29593a6:      	pushq	%rbx
 29593a7:      	pushq	%r13
 29593a9:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 29593ae:      	addq	$0x20, %rsp
 29593b2:      	testq	%rax, %rax
 29593b5:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29593bb:      	movq	%r13, 0x58(%rsp)
 29593c0:      	movl	0x148(%r14), %eax
 29593c7:      	cmpl	$0x4, %eax
 29593ca:      	jl	0x295945a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x157a>
 29593d0:      	cmpb	$0x1, 0x1d1(%r14)
 29593d8:      	movq	(%rsp), %rdi
 29593dc:      	movl	%ebp, %ecx
 29593de:      	movq	0x58(%rsp), %r10
 29593e3:      	jne	0x295942c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x154c>
 29593e5:      	subq	$0x8, %rsp
 29593e9:      	movl	$0x5e, %esi
 29593ee:      	movq	%r12, %rdx
 29593f1:      	movq	%r15, %r8
 29593f4:      	movl	0x20(%rsp), %r9d
 29593f9:      	pushq	0x238(%rsp)
 2959400:      	pushq	%rax
 2959401:      	pushq	0x238(%rsp)
 2959408:      	pushq	%rbx
 2959409:      	pushq	%r10
 295940b:      	callq	0x2965b00 <_ZL20lowerShuffleAsVALIGNRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959410:      	movq	0x88(%rsp), %r10
 2959418:      	movl	%ebp, %ecx
 295941a:      	movq	0x30(%rsp), %rdi
 295941f:      	addq	$0x30, %rsp
 2959423:      	testq	%rax, %rax
 2959426:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295942c:      	movl	$0x5e, %esi
 2959431:      	movq	%r12, %rdx
 2959434:      	movq	%r15, %r8
 2959437:      	movl	0x18(%rsp), %r9d
 295943c:      	pushq	0x230(%rsp)
 2959443:      	pushq	%r14
 2959445:      	pushq	%rbx
 2959446:      	pushq	%r10
 2959448:      	callq	0x2966110 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295944d:      	addq	$0x20, %rsp
 2959451:      	testq	%rax, %rax
 2959454:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295945a:      	cmpl	$0x5, 0x20(%rsp)
 295945f:      	jl	0x295bd0d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e2d>
 2959465:      	movq	0x58(%rsp), %rax
 295946a:      	movq	%rax, 0xa0(%rsp)
 2959472:      	movq	%rbx, 0xa8(%rsp)
 295947a:      	subq	$0x30, %rsp
 295947e:      	movdqu	0xd0(%rsp), %xmm0
 2959487:      	movdqu	%xmm0, (%rsp)
 295948c:      	movq	0x260(%rsp), %rax
 2959494:      	movq	%rax, 0x20(%rsp)
 2959499:      	movq	%r14, 0x18(%rsp)
 295949e:      	movq	0x250(%rsp), %rax
 29594a6:      	movq	%rax, 0x10(%rsp)
 29594ab:      	movq	0x30(%rsp), %rdi
 29594b0:      	movl	$0x5e, %esi
 29594b5:      	movq	%r12, %rdx
 29594b8:      	movl	%ebp, %ecx
 29594ba:      	movq	%r15, %r8
 29594bd:      	movl	0x48(%rsp), %r9d
 29594c2:      	callq	0x2966760 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29594c7:      	addq	$0x30, %rsp
 29594cb:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29594d0:      	cmpl	$0x8, 0x148(%r14)
 29594d8:      	movq	%rdi, (%rsp)
 29594dc:      	jl	0x295953b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x165b>
 29594de:      	movq	%rbx, %r13
 29594e1:      	movq	%rbp, %rsi
 29594e4:      	movl	%r11d, %edx
 29594e7:      	movq	%r15, %rcx
 29594ea:      	movl	%r9d, %r8d
 29594ed:      	movq	%r15, %rbx
 29594f0:      	movl	%r9d, %r15d
 29594f3:      	movq	%r12, %r9
 29594f6:      	pushq	0x230(%rsp)
 29594fd:      	pushq	%r13
 29594ff:      	movq	%rbp, %r14
 2959502:      	movl	%r11d, %ebp
 2959505:      	callq	0x2962b00 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295950a:      	movl	%r15d, %r9d
 295950d:      	movq	%rbx, %r15
 2959510:      	movq	0x230(%rsp), %r10
 2959518:      	movl	%ebp, %r11d
 295951b:      	movq	%r14, %rbp
 295951e:      	movq	0x238(%rsp), %r14
 2959526:      	movq	0x10(%rsp), %rdi
 295952b:      	movq	%r13, %rbx
 295952e:      	addq	$0x10, %rsp
 2959532:      	testq	%rax, %rax
 2959535:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295953b:      	movq	%rbp, 0x10(%rsp)
 2959540:      	movl	0x8(%r10), %eax
 2959544:      	movl	$0x96, %esi
 2959549:      	movq	%rbp, %rdx
 295954c:      	movl	%r11d, %ecx
 295954f:      	movq	%r15, %r8
 2959552:      	movl	%r9d, 0x18(%rsp)
 2959557:      	movq	%r10, %r13
 295955a:      	movq	0x230(%rsp), %r10
 2959562:      	pushq	%r10
 2959564:      	pushq	%r14
 2959566:      	pushq	%rax
 2959567:      	pushq	(%r13)
 295956b:      	pushq	%rbx
 295956c:      	pushq	%r12
 295956e:      	movl	%r11d, %ebp
 2959571:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959576:      	addq	$0x30, %rsp
 295957a:      	testq	%rax, %rax
 295957d:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959583:      	movq	(%r12), %xmm0
 2959589:      	movdqa	-0x1b46551(%rip), %xmm1 # 0xe13040 <.LCPI91_1>
 2959591:      	pxor	%xmm0, %xmm1
 2959595:      	pcmpeqd	%xmm2, %xmm2
 2959599:      	pcmpgtd	%xmm2, %xmm0
 295959d:      	pxor	%xmm2, %xmm0
 29595a1:      	por	%xmm1, %xmm0
 29595a5:      	movq	%xmm0, 0x70(%rsp)
 29595ab:      	movl	0x8(%r13), %eax
 29595af:      	leaq	0x70(%rsp), %r10
 29595b4:      	movq	(%rsp), %rdi
 29595b8:      	movl	$0x96, %esi
 29595bd:      	movq	%r15, %rdx
 29595c0:      	movl	0x18(%rsp), %ecx
 29595c4:      	movq	0x10(%rsp), %r8
 29595c9:      	movl	%ebp, %r9d
 29595cc:      	pushq	0x230(%rsp)
 29595d3:      	pushq	%r14
 29595d5:      	pushq	%rax
 29595d6:      	pushq	(%r13)
 29595da:      	pushq	$0x2
 29595dc:      	pushq	%r10
 29595de:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29595e3:      	addq	$0x30, %rsp
 29595e7:      	testq	%rax, %rax
 29595ea:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29595f0:      	movl	%ebp, 0xc(%rsp)
 29595f4:      	cmpq	$0x2, %rbx
 29595f8:      	movq	0x10(%rsp), %rbp
 29595fd:      	jne	0x295ad4f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e6f>
 2959603:      	movl	(%r12), %eax
 2959607:      	testl	%eax, %eax
 2959609:      	jle	0x2959647 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1767>
 295960b:      	xorl	%ecx, %ecx
 295960d:      	cmpl	$0x1, %eax
 2959610:      	sete	%cl
 2959613:      	movq	%r15, %rsi
 2959616:      	cmoveq	%rbp, %rsi
 295961a:      	movl	0x18(%rsp), %edx
 295961e:      	movl	0xc(%rsp), %r8d
 2959623:      	cmovel	%r8d, %edx
 2959627:      	leal	-0x2(%rax,%rcx,2), %r9d
 295962c:      	subq	$0x8, %rsp
 2959630:      	movl	$0x2, %edi
 2959635:      	movq	%rbp, %rcx
 2959638:      	pushq	$0x0
 295963a:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295963f:      	addq	$0x10, %rsp
 2959643:      	testb	%al, %al
 2959645:      	je	0x295969f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x17bf>
 2959647:      	movl	0x4(%r12), %eax
 295964c:      	testl	%eax, %eax
 295964e:      	sets	%cl
 2959651:      	cmpl	$0x3, %eax
 2959654:      	sete	%dl
 2959657:      	orb	%cl, %dl
 2959659:      	jne	0x2959746 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1866>
 295965f:      	xorl	%ecx, %ecx
 2959661:      	cmpl	$0x2, %eax
 2959664:      	setb	%cl
 2959667:      	movq	%r15, %rsi
 295966a:      	cmovbq	%rbp, %rsi
 295966e:      	movl	0x18(%rsp), %r8d
 2959673:      	movl	%r8d, %edx
 2959676:      	cmovbl	0xc(%rsp), %edx
 295967b:      	leal	-0x2(%rax,%rcx,2), %r9d
 2959680:      	subq	$0x8, %rsp
 2959684:      	movl	$0x2, %edi
 2959689:      	movq	%r15, %rcx
 295968c:      	pushq	$0x1
 295968e:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959693:      	addq	$0x10, %rsp
 2959697:      	testb	%al, %al
 2959699:      	jne	0x2959746 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1866>
 295969f:      	movl	(%r12), %eax
 29596a3:      	testl	%eax, %eax
 29596a5:      	sets	%cl
 29596a8:      	cmpl	$0x1, %eax
 29596ab:      	sete	%dl
 29596ae:      	orb	%cl, %dl
 29596b0:      	jne	0x29596f2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1812>
 29596b2:      	xorl	%ecx, %ecx
 29596b4:      	cmpl	$0x2, %eax
 29596b7:      	setb	%cl
 29596ba:      	movq	%r15, %rsi
 29596bd:      	cmovbq	%rbp, %rsi
 29596c1:      	movl	0x18(%rsp), %edx
 29596c5:      	movl	0xc(%rsp), %r8d
 29596ca:      	cmovbl	%r8d, %edx
 29596ce:      	leal	-0x2(%rax,%rcx,2), %r9d
 29596d3:      	subq	$0x8, %rsp
 29596d7:      	movl	$0x2, %edi
 29596dc:      	movq	%rbp, %rcx
 29596df:      	pushq	$0x1
 29596e1:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 29596e6:      	addq	$0x10, %rsp
 29596ea:      	testb	%al, %al
 29596ec:      	je	0x295ad4f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e6f>
 29596f2:      	movl	0x4(%r12), %eax
 29596f7:      	testl	%eax, %eax
 29596f9:      	sets	%cl
 29596fc:      	cmpl	$0x3, %eax
 29596ff:      	sete	%dl
 2959702:      	orb	%cl, %dl
 2959704:      	jne	0x2959746 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1866>
 2959706:      	xorl	%ecx, %ecx
 2959708:      	cmpl	$0x2, %eax
 295970b:      	setb	%cl
 295970e:      	movq	%r15, %rsi
 2959711:      	cmovbq	%rbp, %rsi
 2959715:      	movl	0x18(%rsp), %r8d
 295971a:      	movl	%r8d, %edx
 295971d:      	cmovbl	0xc(%rsp), %edx
 2959722:      	leal	-0x2(%rax,%rcx,2), %r9d
 2959727:      	subq	$0x8, %rsp
 295972b:      	movl	$0x2, %edi
 2959730:      	movq	%r15, %rcx
 2959733:      	pushq	$0x1
 2959735:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295973a:      	addq	$0x10, %rsp
 295973e:      	testb	%al, %al
 2959740:      	je	0x295ad4f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e6f>
 2959746:      	movl	(%r12), %edx
 295974a:      	movq	%rbp, %rdi
 295974d:      	movl	0xc(%rsp), %esi
 2959751:      	movq	0x230(%rsp), %rcx
 2959759:      	callq	0x2968f80 <_ZL30getScalarValueForVectorElementN4llvm7SDValueEiRNS_12SelectionDAGE>
 295975e:      	testq	%rax, %rax
 2959761:      	je	0x295ad4f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2e6f>
 2959767:      	movq	%rax, 0xa0(%rsp)
 295976f:      	movl	%edx, 0xa8(%rsp)
 2959776:      	movq	0x230(%rsp), %r14
 295977e:      	movq	0x3b0(%r14), %rax
 2959785:      	xorl	%ebx, %ebx
 2959787:      	movl	$0x0, %r9d
 295978d:      	testq	%rax, %rax
 2959790:      	je	0x2959796 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x18b6>
 2959792:      	movl	0x8(%rax), %r9d
 2959796:      	subq	$0x10, %rsp
 295979a:      	movups	0xb0(%rsp), %xmm0
 29597a2:      	movups	%xmm0, (%rsp)
 29597a6:      	movq	%r14, %rdi
 29597a9:      	movl	$0xac, %esi
 29597ae:      	movq	0x10(%rsp), %rdx
 29597b3:      	movl	$0x96, %ecx
 29597b8:      	xorl	%r8d, %r8d
 29597bb:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 29597c0:      	addq	$0x10, %rsp
 29597c4:      	movq	%rax, 0xa0(%rsp)
 29597cc:      	movl	%edx, 0xa8(%rsp)
 29597d3:      	movq	0x3b0(%r14), %rax
 29597da:      	testq	%rax, %rax
 29597dd:      	je	0x29597e2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1902>
 29597df:      	movl	0x8(%rax), %ebx
 29597e2:      	subq	$0x20, %rsp
 29597e6:      	movups	0xc0(%rsp), %xmm0
 29597ee:      	movups	%xmm0, 0x10(%rsp)
 29597f3:      	leaq	0x230(%rsp), %rax
 29597fb:      	movdqu	(%rax), %xmm0
 29597ff:      	movdqu	%xmm0, (%rsp)
 2959804:      	movq	%r14, %rdi
 2959807:      	movl	$0x2c5, %esi            # imm = 0x2C5
 295980c:      	movq	0x20(%rsp), %rdx
 2959811:      	jmp	0x2958fef <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x110f>
 2959816:      	movq	0x48(%rbp), %rsi
 295981a:      	movq	%rsi, 0x30(%rsp)
 295981f:      	testq	%rsi, %rsi
 2959822:      	je	0x295983f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x195f>
 2959824:      	leaq	0x30(%rsp), %rdi
 2959829:      	movl	$0x1, %edx
 295982e:      	movq	%rbx, %r14
 2959831:      	movl	%r11d, %ebx
 2959834:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 2959839:      	movl	%ebx, %r11d
 295983c:      	movq	%r14, %rbx
 295983f:      	movl	0x44(%rbp), %eax
 2959842:      	movl	%eax, 0x38(%rsp)
 2959846:      	movq	0x3b0(%r15), %rax
 295984d:      	testq	%rax, %rax
 2959850:      	je	0x2959fe3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2103>
 2959856:      	movl	0x8(%rax), %r9d
 295985a:      	jmp	0x2959fe6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2106>
 295985f:      	movq	%rdi, (%rsp)
 2959863:      	movq	0x60(%rsp), %r8
 2959868:      	movl	0x68(%rsp), %r13d
 295986d:      	movl	$0x84, %esi
 2959872:      	movq	%rbp, %rdx
 2959875:      	movl	%r11d, %ecx
 2959878:      	movq	%r8, 0x18(%rsp)
 295987d:      	movl	%r13d, %r9d
 2959880:      	movq	0x230(%rsp), %r15
 2959888:      	pushq	%r15
 295988a:      	pushq	%r14
 295988c:      	pushq	%rbx
 295988d:      	pushq	%r12
 295988f:      	movq	%rbx, %r15
 2959892:      	movq	%r12, %rbx
 2959895:      	movq	%rbp, %r12
 2959898:      	movl	%r11d, %ebp
 295989b:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 29598a0:      	addq	$0x20, %rsp
 29598a4:      	testq	%rax, %rax
 29598a7:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 29598ad:      	movq	%r13, 0x20(%rsp)
 29598b2:      	movq	0x18(%rsp), %r13
 29598b7:      	movq	%r15, 0x28(%rsp)
 29598bc:      	movq	%r14, %rax
 29598bf:      	movq	%rbx, %r14
 29598c2:      	movl	%ebp, %ebx
 29598c4:      	movq	%rax, %r15
 29598c7:      	movl	0x148(%rax), %eax
 29598cd:      	cmpl	$0x3, %eax
 29598d0:      	jl	0x295a8ac <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29cc>
 29598d6:      	cmpq	$0x4, 0x28(%rsp)
 29598dc:      	movl	%ebx, %r8d
 29598df:      	movq	%r13, %rbp
 29598e2:      	jne	0x295b58c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36ac>
 29598e8:      	movl	(%r14), %eax
 29598eb:      	testl	%eax, %eax
 29598ed:      	movq	%r12, %r13
 29598f0:      	jle	0x2959931 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1a51>
 29598f2:      	xorl	%ecx, %ecx
 29598f4:      	cmpl	$0x4, %eax
 29598f7:      	setb	%cl
 29598fa:      	movq	%rbp, %rsi
 29598fd:      	cmovbq	%r13, %rsi
 2959901:      	movq	0x20(%rsp), %rdx
 2959906:      	cmovbl	%r8d, %edx
 295990a:      	leal	-0x4(%rax,%rcx,4), %r9d
 295990f:      	subq	$0x8, %rsp
 2959913:      	movl	$0x4, %edi
 2959918:      	movq	%r13, %rcx
 295991b:      	pushq	$0x0
 295991d:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959922:      	movl	%ebx, %r8d
 2959925:      	addq	$0x10, %rsp
 2959929:      	testb	%al, %al
 295992b:      	je	0x295b0a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31c6>
 2959931:      	movl	0x4(%r14), %eax
 2959935:      	testl	%eax, %eax
 2959937:      	jle	0x2959978 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1a98>
 2959939:      	xorl	%ecx, %ecx
 295993b:      	cmpl	$0x4, %eax
 295993e:      	setb	%cl
 2959941:      	movq	%rbp, %rsi
 2959944:      	cmovbq	%r13, %rsi
 2959948:      	movq	0x20(%rsp), %rdx
 295994d:      	cmovbl	%r8d, %edx
 2959951:      	leal	-0x4(%rax,%rcx,4), %r9d
 2959956:      	subq	$0x8, %rsp
 295995a:      	movl	$0x4, %edi
 295995f:      	movq	%r13, %rcx
 2959962:      	pushq	$0x0
 2959964:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959969:      	movl	%ebx, %r8d
 295996c:      	addq	$0x10, %rsp
 2959970:      	testb	%al, %al
 2959972:      	je	0x295b0a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31c6>
 2959978:      	movl	0x8(%r14), %eax
 295997c:      	testl	%eax, %eax
 295997e:      	sets	%cl
 2959981:      	cmpl	$0x2, %eax
 2959984:      	sete	%dl
 2959987:      	orb	%cl, %dl
 2959989:      	jne	0x29599ca <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1aea>
 295998b:      	xorl	%ecx, %ecx
 295998d:      	cmpl	$0x4, %eax
 2959990:      	setb	%cl
 2959993:      	movq	%rbp, %rsi
 2959996:      	cmovbq	%r13, %rsi
 295999a:      	movq	0x20(%rsp), %rdx
 295999f:      	cmovbl	%r8d, %edx
 29599a3:      	leal	-0x4(%rax,%rcx,4), %r9d
 29599a8:      	subq	$0x8, %rsp
 29599ac:      	movl	$0x4, %edi
 29599b1:      	movq	%r13, %rcx
 29599b4:      	pushq	$0x2
 29599b6:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 29599bb:      	movl	%ebx, %r8d
 29599be:      	addq	$0x10, %rsp
 29599c2:      	testb	%al, %al
 29599c4:      	je	0x295b0a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31c6>
 29599ca:      	movl	0xc(%r14), %eax
 29599ce:      	testl	%eax, %eax
 29599d0:      	sets	%cl
 29599d3:      	cmpl	$0x2, %eax
 29599d6:      	sete	%dl
 29599d9:      	orb	%cl, %dl
 29599db:      	jne	0x2959a1c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1b3c>
 29599dd:      	xorl	%ecx, %ecx
 29599df:      	cmpl	$0x4, %eax
 29599e2:      	setb	%cl
 29599e5:      	movq	%rbp, %rsi
 29599e8:      	cmovbq	%r13, %rsi
 29599ec:      	movq	0x20(%rsp), %rdx
 29599f1:      	cmovbl	%r8d, %edx
 29599f5:      	leal	-0x4(%rax,%rcx,4), %r9d
 29599fa:      	subq	$0x8, %rsp
 29599fe:      	movl	$0x4, %edi
 2959a03:      	movq	%r13, %rcx
 2959a06:      	pushq	$0x2
 2959a08:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 2959a0d:      	movl	%ebx, %r8d
 2959a10:      	addq	$0x10, %rsp
 2959a14:      	testb	%al, %al
 2959a16:      	je	0x295b0a6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x31c6>
 2959a1c:      	movq	%r13, 0xa0(%rsp)
 2959a24:      	movl	%r8d, 0xa8(%rsp)
 2959a2c:      	movq	0x230(%rsp), %rdi
 2959a34:      	movq	0x3b0(%rdi), %rax
 2959a3b:      	testq	%rax, %rax
 2959a3e:      	je	0x295bae0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c00>
 2959a44:      	movl	0x8(%rax), %r9d
 2959a48:      	jmp	0x295bae3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c03>
 2959a4d:      	xorl	%edx, %edx
 2959a4f:      	cmpb	$0x1, 0x181(%r14)
 2959a57:      	jne	0x295a251 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2371>
 2959a5d:      	cmpl	$0x1, %edx
 2959a60:      	je	0x295a1fe <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x231e>
 2959a66:      	testl	%edx, %edx
 2959a68:      	jne	0x295a251 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2371>
 2959a6e:      	movq	0x80(%rsp), %r8
 2959a76:      	movl	0x88(%rsp), %r9d
 2959a7e:      	movq	(%rsp), %rdi
 2959a82:      	movl	$0x6f, %esi
 2959a87:      	movq	%rbp, %rdx
 2959a8a:      	movl	%r11d, %ecx
 2959a8d:      	pushq	%r15
 2959a8f:      	pushq	%r14
 2959a91:      	pushq	%rbx
 2959a92:      	pushq	%r12
 2959a94:      	movq	%rbx, %r14
 2959a97:      	movl	%r11d, %ebx
 2959a9a:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959a9f:      	movl	%ebx, %r11d
 2959aa2:      	movq	%r14, %rbx
 2959aa5:      	addq	$0x20, %rsp
 2959aa9:      	testq	%rax, %rax
 2959aac:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959ab2:      	jmp	0x295a251 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2371>
 2959ab7:      	cmpb	$0x0, 0x1f7(%rsi)
 2959abe:      	movq	(%rsp), %rdi
 2959ac2:      	movl	0xc(%rsp), %ecx
 2959ac6:      	movq	0x220(%rsp), %rax
 2959ace:      	je	0x2959b6a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1c8a>
 2959ad4:      	movq	%rsi, %r14
 2959ad7:      	movl	$0x49, %esi
 2959adc:      	movq	0x10(%rsp), %rdx
 2959ae1:      	movq	0x20(%rsp), %r8
 2959ae6:      	movq	%r9, %rbx
 2959ae9:      	movq	0x18(%rsp), %r9
 2959aee:      	pushq	$0x1
 2959af0:      	pushq	0x238(%rsp)
 2959af7:      	pushq	%r14
 2959af9:      	pushq	%rax
 2959afa:      	pushq	$0x0
 2959afc:      	pushq	%r12
 2959afe:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2959b03:      	movl	0x3c(%rsp), %ecx
 2959b07:      	movq	0x30(%rsp), %rdi
 2959b0c:      	addq	$0x30, %rsp
 2959b10:      	testq	%rax, %rax
 2959b13:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959b19:      	movl	0x148(%r14), %eax
 2959b20:      	movzbl	0x1db(%r14), %r10d
 2959b28:      	subq	$0x8, %rsp
 2959b2c:      	movl	$0x49, %esi
 2959b31:      	movq	0x18(%rsp), %rdx
 2959b36:      	movq	%r12, %r8
 2959b39:      	movq	%r13, %r9
 2959b3c:      	pushq	0x238(%rsp)
 2959b43:      	pushq	%r10
 2959b45:      	pushq	%rax
 2959b46:      	movl	%ecx, %r15d
 2959b49:      	callq	0x296ff60 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959b4e:      	addq	$0x20, %rsp
 2959b52:      	testq	%rax, %rax
 2959b55:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959b5b:      	testq	%r13, %r13
 2959b5e:      	movl	%r15d, %ecx
 2959b61:      	movq	%rbx, %r9
 2959b64:      	jne	0x295a887 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29a7>
 2959b6a:      	movq	%r13, %rbp
 2959b6d:      	movaps	-0x1b39854(%rip), %xmm0 # 0xe20320 <.Lswitch.table._ZN4llvm5XCOFF25parseParmsTypeWithVecInfoEjjjj.10>
 2959b74:      	movaps	%xmm0, 0x70(%rsp)
 2959b79:      	movaps	-0x1b41b70(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 2959b80:      	movaps	%xmm0, 0x80(%rsp)
 2959b88:      	movq	0x230(%rsp), %r15
 2959b90:      	movq	0x10(%rsp), %r13
 2959b95:      	movaps	-0x1b41b8c(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 2959b9c:      	movaps	%xmm0, 0xa0(%rsp)
 2959ba4:      	leaq	0xa0(%rsp), %rdx
 2959bac:      	movl	$0x4, %ebx
 2959bb1:      	movl	$0x4, %ecx
 2959bb6:      	movq	%r12, %rdi
 2959bb9:      	movq	%rbp, %rsi
 2959bbc:      	movq	%r13, %r8
 2959bbf:      	movl	0xc(%rsp), %r9d
 2959bc4:      	pushq	0x18(%rsp)
 2959bc8:      	pushq	0x28(%rsp)
 2959bcc:      	callq	0x2961a40 <_ZL19isShuffleEquivalentN4llvm8ArrayRefIiEES1_NS_7SDValueES2_>
 2959bd1:      	addq	$0x10, %rsp
 2959bd5:      	testb	%al, %al
 2959bd7:      	leaq	0x80(%rsp), %rdi
 2959bdf:      	cmoveq	%r12, %rdi
 2959be3:      	cmoveq	%rbp, %rbx
 2959be7:      	movq	%rbx, %rsi
 2959bea:      	callq	0x2962840 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 2959bef:      	movl	%eax, %esi
 2959bf1:      	subq	$0x8, %rsp
 2959bf5:      	xorl	%ebx, %ebx
 2959bf7:      	movq	%r15, %rdi
 2959bfa:      	movq	0x8(%rsp), %rdx
 2959bff:      	movl	$0x5, %ecx
 2959c04:      	xorl	%r8d, %r8d
 2959c07:      	movl	$0x1, %r9d
 2959c0d:      	pushq	$0x0
 2959c0f:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 2959c14:      	addq	$0x10, %rsp
 2959c18:      	movq	%rax, 0xa0(%rsp)
 2959c20:      	movl	%edx, 0xa8(%rsp)
 2959c27:      	movq	%r13, 0x30(%rsp)
 2959c2c:      	movl	0xc(%rsp), %eax
 2959c30:      	movl	%eax, 0x38(%rsp)
 2959c34:      	movq	0x3b0(%r15), %rax
 2959c3b:      	testq	%rax, %rax
 2959c3e:      	je	0x2959c43 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d63>
 2959c40:      	movl	0x8(%rax), %ebx
 2959c43:      	subq	$0x20, %rsp
 2959c47:      	movups	0xc0(%rsp), %xmm0
 2959c4f:      	movups	%xmm0, 0x10(%rsp)
 2959c54:      	movdqu	0x50(%rsp), %xmm0
 2959c5a:      	movdqu	%xmm0, (%rsp)
 2959c5f:      	movq	%r15, %rdi
 2959c62:      	movl	$0x2b9, %esi            # imm = 0x2B9
 2959c67:      	movq	0x20(%rsp), %rdx
 2959c6c:      	movl	$0x49, %ecx
 2959c71:      	xorl	%r8d, %r8d
 2959c74:      	movl	%ebx, %r9d
 2959c77:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 2959c7c:      	addq	$0x20, %rsp
 2959c80:      	movl	%edx, %r8d
 2959c83:      	movl	%r8d, %edx
 2959c86:      	addq	$0x1d8, %rsp            # imm = 0x1D8
 2959c8d:      	popq	%rbx
 2959c8e:      	popq	%r12
 2959c90:      	popq	%r13
 2959c92:      	popq	%r14
 2959c94:      	popq	%r15
 2959c96:      	popq	%rbp
 2959c97:      	retq
 2959c98:      	testl	%r15d, %r15d
 2959c9b:      	movq	%r11, %r12
 2959c9e:      	je	0x295a887 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x29a7>
 2959ca4:      	movq	%r12, 0x58(%rsp)
 2959ca9:      	cmpl	$0x8, 0x148(%r14)
 2959cb1:      	movq	0x10(%rsp), %r12
 2959cb6:      	movq	0x20(%rsp), %rbp
 2959cbb:      	jl	0x2959cf7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1e17>
 2959cbd:      	movq	%r12, %rsi
 2959cc0:      	movl	%ecx, %edx
 2959cc2:      	movq	%rbp, %rcx
 2959cc5:      	movq	0x18(%rsp), %r8
 2959cca:      	movq	0x58(%rsp), %r9
 2959ccf:      	pushq	0x230(%rsp)
 2959cd6:      	pushq	%r13
 2959cd8:      	callq	0x2962b00 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959cdd:      	movq	0x230(%rsp), %r10
 2959ce5:      	movl	0x1c(%rsp), %ecx
 2959ce9:      	movq	0x10(%rsp), %rdi
 2959cee:      	addq	$0x10, %rsp
 2959cf2:      	testq	%rax, %rax
 2959cf5:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959cf7:      	movl	$0x49, %esi
 2959cfc:      	movq	%r12, %rdx
 2959cff:      	movq	%rbp, %r8
 2959d02:      	movq	0x18(%rsp), %r9
 2959d07:      	pushq	$0x0
 2959d09:      	movq	%r13, %r12
 2959d0c:      	movq	%r14, %r13
 2959d0f:      	movq	%rbp, %r14
 2959d12:      	movq	0x238(%rsp), %rbp
 2959d1a:      	pushq	%rbp
 2959d1b:      	pushq	%r13
 2959d1d:      	pushq	%r10
 2959d1f:      	pushq	%r12
 2959d21:      	movq	0x80(%rsp), %rbx
 2959d29:      	pushq	%rbx
 2959d2a:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 2959d2f:      	addq	$0x30, %rsp
 2959d33:      	testq	%rax, %rax
 2959d36:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959d3c:      	movq	%r12, 0x28(%rsp)
 2959d41:      	cmpl	$0x1, %r15d
 2959d45:      	movq	%rbp, %r12
 2959d48:      	movq	%r14, %r15
 2959d4b:      	jne	0x2959d92 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1eb2>
 2959d4d:      	movq	0x220(%rsp), %r10
 2959d55:      	movl	0x8(%r10), %eax
 2959d59:      	movq	(%rsp), %rdi
 2959d5d:      	movl	$0x49, %esi
 2959d62:      	movq	0x10(%rsp), %rdx
 2959d67:      	movl	0xc(%rsp), %ecx
 2959d6b:      	movq	%r15, %r8
 2959d6e:      	movq	0x18(%rsp), %r9
 2959d73:      	pushq	%r12
 2959d75:      	pushq	%r13
 2959d77:      	pushq	%rax
 2959d78:      	pushq	(%r10)
 2959d7b:      	pushq	0x48(%rsp)
 2959d7f:      	pushq	%rbx
 2959d80:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959d85:      	addq	$0x30, %rsp
 2959d89:      	testq	%rax, %rax
 2959d8c:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959d92:      	movl	0x148(%r13), %ebp
 2959d99:      	cmpl	$0x5, %ebp
 2959d9c:      	movq	0x18(%rsp), %rbx
 2959da1:      	jl	0x2959de8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1f08>
 2959da3:      	subq	$0x8, %rsp
 2959da7:      	movq	0x8(%rsp), %rdi
 2959dac:      	movl	$0x49, %esi
 2959db1:      	movq	0x18(%rsp), %rdx
 2959db6:      	movl	0x14(%rsp), %ecx
 2959dba:      	movq	%r15, %r8
 2959dbd:      	movl	%ebx, %r9d
 2959dc0:      	pushq	%r12
 2959dc2:      	pushq	%r13
 2959dc4:      	pushq	0x238(%rsp)
 2959dcb:      	pushq	0x48(%rsp)
 2959dcf:      	pushq	0x80(%rsp)
 2959dd6:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959ddb:      	addq	$0x30, %rsp
 2959ddf:      	testq	%rax, %rax
 2959de2:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959de8:      	movl	%ebp, 0x9c(%rsp)
 2959def:      	movl	0x1e4(%r13), %eax
 2959df6:      	subq	$0x8, %rsp
 2959dfa:      	movq	0x8(%rsp), %rdi
 2959dff:      	movl	$0x49, %esi
 2959e04:      	movq	%r15, %r8
 2959e07:      	movq	0x18(%rsp), %rbp
 2959e0c:      	movq	%rbp, %rdx
 2959e0f:      	movl	0x14(%rsp), %r15d
 2959e14:      	movl	%r15d, %ecx
 2959e17:      	movq	%r8, %r14
 2959e1a:      	movl	%ebx, %r9d
 2959e1d:      	pushq	%r12
 2959e1f:      	pushq	%rax
 2959e20:      	pushq	0x238(%rsp)
 2959e27:      	movq	%rbx, %r13
 2959e2a:      	movq	0x48(%rsp), %rbx
 2959e2f:      	pushq	%rbx
 2959e30:      	movq	0x80(%rsp), %r12
 2959e38:      	pushq	%r12
 2959e3a:      	callq	0x2969d50 <_ZL21lowerShuffleAsBitMaskRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959e3f:      	addq	$0x30, %rsp
 2959e43:      	testq	%rax, %rax
 2959e46:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959e4c:      	subq	$0x8, %rsp
 2959e50:      	movq	0x8(%rsp), %rdi
 2959e55:      	movl	$0x49, %esi
 2959e5a:      	movq	%rbp, %rdx
 2959e5d:      	movl	%r15d, %ecx
 2959e60:      	movq	%r14, %r8
 2959e63:      	movl	%r13d, %r9d
 2959e66:      	movq	0x238(%rsp), %r13
 2959e6e:      	pushq	%r13
 2959e70:      	pushq	%rbx
 2959e71:      	pushq	%r12
 2959e73:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 2959e78:      	addq	$0x20, %rsp
 2959e7c:      	testq	%rax, %rax
 2959e7f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959e85:      	movq	%r14, %r15
 2959e88:      	movq	0x228(%rsp), %r14
 2959e90:      	movl	0x148(%r14), %eax
 2959e97:      	cmpl	$0x4, %eax
 2959e9a:      	movq	%r13, %r12
 2959e9d:      	jl	0x2959f25 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2045>
 2959ea3:      	cmpb	$0x1, 0x1d1(%r14)
 2959eab:      	jne	0x2959ef0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2010>
 2959ead:      	subq	$0x8, %rsp
 2959eb1:      	movq	0x8(%rsp), %rdi
 2959eb6:      	movl	$0x49, %esi
 2959ebb:      	movq	0x18(%rsp), %rdx
 2959ec0:      	movl	0x14(%rsp), %ecx
 2959ec4:      	movq	%r15, %r8
 2959ec7:      	movq	0x20(%rsp), %r9
 2959ecc:      	pushq	%r12
 2959ece:      	pushq	%rax
 2959ecf:      	pushq	0x238(%rsp)
 2959ed6:      	pushq	%rbx
 2959ed7:      	pushq	0x80(%rsp)
 2959ede:      	callq	0x2965b00 <_ZL20lowerShuffleAsVALIGNRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959ee3:      	addq	$0x30, %rsp
 2959ee7:      	testq	%rax, %rax
 2959eea:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959ef0:      	movq	(%rsp), %rdi
 2959ef4:      	movl	$0x49, %esi
 2959ef9:      	movq	0x10(%rsp), %rdx
 2959efe:      	movl	0xc(%rsp), %ecx
 2959f02:      	movq	%r15, %r8
 2959f05:      	movq	0x18(%rsp), %r9
 2959f0a:      	pushq	%r12
 2959f0c:      	pushq	%r14
 2959f0e:      	pushq	%rbx
 2959f0f:      	pushq	0x70(%rsp)
 2959f13:      	callq	0x2966110 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 2959f18:      	addq	$0x20, %rsp
 2959f1c:      	testq	%rax, %rax
 2959f1f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959f25:      	movq	0x58(%rsp), %r15
 2959f2a:      	movq	%r15, %rdi
 2959f2d:      	callq	0x29676e0 <_ZL18isSingleSHUFPSMaskN4llvm8ArrayRefIiEE>
 2959f32:      	testb	%al, %al
 2959f34:      	je	0x295bdc5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ee5>
 2959f3a:      	movq	%r12, %rdi
 2959f3d:      	movl	$0x84, %esi
 2959f42:      	xorl	%edx, %edx
 2959f44:      	movq	0x10(%rsp), %rcx
 2959f49:      	movl	0xc(%rsp), %r8d
 2959f4e:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959f53:      	movq	%rax, %rbx
 2959f56:      	movl	%edx, %ebp
 2959f58:      	movq	%r12, %rdi
 2959f5b:      	movl	$0x84, %esi
 2959f60:      	xorl	%edx, %edx
 2959f62:      	movq	0x20(%rsp), %rcx
 2959f67:      	movq	0x18(%rsp), %r8
 2959f6c:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959f71:      	movq	%rax, 0xa0(%rsp)
 2959f79:      	movl	%edx, 0xa8(%rsp)
 2959f80:      	movq	%r15, 0x30(%rsp)
 2959f85:      	movq	0x28(%rsp), %rax
 2959f8a:      	movq	%rax, 0x38(%rsp)
 2959f8f:      	subq	$0x20, %rsp
 2959f93:      	movups	0x50(%rsp), %xmm0
 2959f98:      	movups	%xmm0, 0x10(%rsp)
 2959f9d:      	movdqu	0xc0(%rsp), %xmm0
 2959fa6:      	movdqu	%xmm0, (%rsp)
 2959fab:      	movq	%r12, %rdi
 2959fae:      	movl	$0x84, %esi
 2959fb3:      	xorl	%edx, %edx
 2959fb5:      	movq	0x20(%rsp), %rcx
 2959fba:      	movq	%rbx, %r8
 2959fbd:      	movl	%ebp, %r9d
 2959fc0:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 2959fc5:      	addq	$0x20, %rsp
 2959fc9:      	movl	%edx, %r8d
 2959fcc:      	movq	%r12, %rdi
 2959fcf:      	movl	$0x49, %esi
 2959fd4:      	xorl	%edx, %edx
 2959fd6:      	movq	%rax, %rcx
 2959fd9:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 2959fde:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 2959fe3:      	xorl	%r9d, %r9d
 2959fe6:      	movq	%rbx, %r13
 2959fe9:      	movq	%rbp, 0xa0(%rsp)
 2959ff1:      	movl	%r11d, 0xa8(%rsp)
 2959ff9:      	subq	$0x10, %rsp
 2959ffd:      	movups	0xb0(%rsp), %xmm0
 295a005:      	movups	%xmm0, (%rsp)
 295a009:      	leaq	0x40(%rsp), %rdx
 295a00e:      	movq	%r15, %rdi
 295a011:      	movl	$0xf3, %esi
 295a016:      	movl	$0x3e, %ecx
 295a01b:      	xorl	%r8d, %r8d
 295a01e:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a023:      	addq	$0x10, %rsp
 295a027:      	movq	%rax, %rbp
 295a02a:      	movl	%edx, %r11d
 295a02d:      	movq	0x30(%rsp), %rsi
 295a032:      	testq	%rsi, %rsi
 295a035:      	je	0x295a047 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2167>
 295a037:      	leaq	0x30(%rsp), %rdi
 295a03c:      	movl	%r11d, %ebx
 295a03f:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a044:      	movl	%ebx, %r11d
 295a047:      	leaq	0x210(%rsp), %rdx
 295a04f:      	movq	(%rdx), %r14
 295a052:      	movl	0x8(%rdx), %ebx
 295a055:      	movq	0x30(%r14), %rax
 295a059:      	movq	%rbx, %rcx
 295a05c:      	shlq	$0x4, %rcx
 295a060:      	cmpw	$0x3e, (%rax,%rcx)
 295a065:      	je	0x295a119 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2239>
 295a06b:      	movq	%rbp, 0x10(%rsp)
 295a070:      	movq	0x48(%r14), %rsi
 295a074:      	movq	%rsi, 0x30(%rsp)
 295a079:      	testq	%rsi, %rsi
 295a07c:      	je	0x295a093 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21b3>
 295a07e:      	leaq	0x30(%rsp), %rdi
 295a083:      	movl	$0x1, %edx
 295a088:      	movl	%r11d, %ebp
 295a08b:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a090:      	movl	%ebp, %r11d
 295a093:      	movl	0x44(%r14), %eax
 295a097:      	movl	%eax, 0x38(%rsp)
 295a09b:      	movq	0x3b0(%r15), %rax
 295a0a2:      	movl	%r11d, %ebp
 295a0a5:      	testq	%rax, %rax
 295a0a8:      	je	0x295a0b0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21d0>
 295a0aa:      	movl	0x8(%rax), %r9d
 295a0ae:      	jmp	0x295a0b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x21d3>
 295a0b0:      	xorl	%r9d, %r9d
 295a0b3:      	movq	%r14, 0xa0(%rsp)
 295a0bb:      	movl	%ebx, 0xa8(%rsp)
 295a0c2:      	subq	$0x10, %rsp
 295a0c6:      	movups	0xb0(%rsp), %xmm0
 295a0ce:      	movups	%xmm0, (%rsp)
 295a0d2:      	leaq	0x40(%rsp), %rdx
 295a0d7:      	movq	%r15, %rdi
 295a0da:      	movl	$0xf3, %esi
 295a0df:      	movl	$0x3e, %ecx
 295a0e4:      	xorl	%r8d, %r8d
 295a0e7:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a0ec:      	addq	$0x10, %rsp
 295a0f0:      	movq	%rax, %r14
 295a0f3:      	movl	%edx, %ebx
 295a0f5:      	movq	0x30(%rsp), %rsi
 295a0fa:      	testq	%rsi, %rsi
 295a0fd:      	je	0x295a109 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2229>
 295a0ff:      	leaq	0x30(%rsp), %rdi
 295a104:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a109:      	movl	%ebp, %r11d
 295a10c:      	movq	0x10(%rsp), %rbp
 295a111:      	leaq	0x210(%rsp), %rdx
 295a119:      	movq	%r14, (%rdx)
 295a11c:      	movl	%ebx, 0x8(%rdx)
 295a11f:      	movq	%r12, 0x198(%rsp)
 295a127:      	movq	%r13, 0x1a0(%rsp)
 295a12f:      	subq	$0x20, %rsp
 295a133:      	movups	0x1b8(%rsp), %xmm0
 295a13b:      	movups	%xmm0, 0x10(%rsp)
 295a140:      	movdqu	(%rdx), %xmm0
 295a144:      	movdqu	%xmm0, (%rsp)
 295a149:      	movq	%r15, %rdi
 295a14c:      	movl	$0x3e, %esi
 295a151:      	xorl	%edx, %edx
 295a153:      	movq	0x20(%rsp), %rcx
 295a158:      	movq	%rbp, %r8
 295a15b:      	movl	%r11d, %r9d
 295a15e:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295a163:      	addq	$0x20, %rsp
 295a167:      	movl	%edx, %r8d
 295a16a:      	movq	0x30(%rax), %rdx
 295a16e:      	movl	%r8d, %ecx
 295a171:      	shlq	$0x4, %rcx
 295a175:      	cmpw	$0x7b, (%rdx,%rcx)
 295a17a:      	je	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295a180:      	movq	0x48(%rax), %rsi
 295a184:      	movq	%rsi, 0x30(%rsp)
 295a189:      	testq	%rsi, %rsi
 295a18c:      	je	0x295a1a9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22c9>
 295a18e:      	leaq	0x30(%rsp), %rdi
 295a193:      	movl	$0x1, %edx
 295a198:      	movq	%rax, %rbx
 295a19b:      	movl	%r8d, %ebp
 295a19e:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a1a3:      	movl	%ebp, %r8d
 295a1a6:      	movq	%rbx, %rax
 295a1a9:      	movl	0x44(%rax), %ecx
 295a1ac:      	movl	%ecx, 0x38(%rsp)
 295a1b0:      	movq	0x3b0(%r15), %rcx
 295a1b7:      	testq	%rcx, %rcx
 295a1ba:      	je	0x295a1c2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22e2>
 295a1bc:      	movl	0x8(%rcx), %r9d
 295a1c0:      	jmp	0x295a1c5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x22e5>
 295a1c2:      	xorl	%r9d, %r9d
 295a1c5:      	movq	%rax, 0xa0(%rsp)
 295a1cd:      	movl	%r8d, 0xa8(%rsp)
 295a1d5:      	subq	$0x10, %rsp
 295a1d9:      	movdqu	0xb0(%rsp), %xmm0
 295a1e2:      	movdqu	%xmm0, (%rsp)
 295a1e7:      	leaq	0x40(%rsp), %rdx
 295a1ec:      	movq	%r15, %rdi
 295a1ef:      	movl	$0xf3, %esi
 295a1f4:      	movl	$0x7b, %ecx
 295a1f9:      	jmp	0x295a4d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25f3>
 295a1fe:      	cmpl	$0x8, (%r12)
 295a203:      	jl	0x295a251 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2371>
 295a205:      	movq	0x80(%rsp), %r8
 295a20d:      	movl	0x88(%rsp), %r9d
 295a215:      	movl	0x8(%r10), %eax
 295a219:      	movq	(%rsp), %rdi
 295a21d:      	movl	$0x6f, %esi
 295a222:      	movq	%rbp, %rdx
 295a225:      	movl	%r11d, %ecx
 295a228:      	pushq	%r15
 295a22a:      	pushq	%r14
 295a22c:      	pushq	%rax
 295a22d:      	pushq	(%r10)
 295a230:      	pushq	%rbx
 295a231:      	pushq	%r12
 295a233:      	movq	%rbx, %r14
 295a236:      	movl	%r11d, %ebx
 295a239:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a23e:      	movl	%ebx, %r11d
 295a241:      	movq	%r14, %rbx
 295a244:      	addq	$0x30, %rsp
 295a248:      	testq	%rax, %rax
 295a24b:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a251:      	movq	0x30(%rbp), %rax
 295a255:      	movl	%r11d, %ecx
 295a258:      	shlq	$0x4, %rcx
 295a25c:      	cmpw	$0x3e, (%rax,%rcx)
 295a261:      	jne	0x295a26b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x238b>
 295a263:      	movq	%rbx, %r13
 295a266:      	jmp	0x295a313 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2433>
 295a26b:      	movq	0x48(%rbp), %rsi
 295a26f:      	movq	%rsi, 0x30(%rsp)
 295a274:      	testq	%rsi, %rsi
 295a277:      	je	0x295a294 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23b4>
 295a279:      	leaq	0x30(%rsp), %rdi
 295a27e:      	movl	$0x1, %edx
 295a283:      	movq	%rbx, %r14
 295a286:      	movl	%r11d, %ebx
 295a289:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a28e:      	movl	%ebx, %r11d
 295a291:      	movq	%r14, %rbx
 295a294:      	movl	0x44(%rbp), %eax
 295a297:      	movl	%eax, 0x38(%rsp)
 295a29b:      	movq	0x3b0(%r15), %rax
 295a2a2:      	testq	%rax, %rax
 295a2a5:      	je	0x295a2ad <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23cd>
 295a2a7:      	movl	0x8(%rax), %r9d
 295a2ab:      	jmp	0x295a2b0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x23d0>
 295a2ad:      	xorl	%r9d, %r9d
 295a2b0:      	movq	%rbx, %r13
 295a2b3:      	movq	%rbp, 0xa0(%rsp)
 295a2bb:      	movl	%r11d, 0xa8(%rsp)
 295a2c3:      	subq	$0x10, %rsp
 295a2c7:      	movdqu	0xb0(%rsp), %xmm0
 295a2d0:      	movdqu	%xmm0, (%rsp)
 295a2d5:      	leaq	0x40(%rsp), %rdx
 295a2da:      	movq	%r15, %rdi
 295a2dd:      	movl	$0xf3, %esi
 295a2e2:      	movl	$0x3e, %ecx
 295a2e7:      	xorl	%r8d, %r8d
 295a2ea:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a2ef:      	addq	$0x10, %rsp
 295a2f3:      	movq	%rax, %rbp
 295a2f6:      	movl	%edx, %r11d
 295a2f9:      	movq	0x30(%rsp), %rsi
 295a2fe:      	testq	%rsi, %rsi
 295a301:      	je	0x295a313 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2433>
 295a303:      	leaq	0x30(%rsp), %rdi
 295a308:      	movl	%r11d, %ebx
 295a30b:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a310:      	movl	%ebx, %r11d
 295a313:      	movq	0x80(%rsp), %r14
 295a31b:      	movl	0x88(%rsp), %ebx
 295a322:      	movq	0x30(%r14), %rax
 295a326:      	movq	%rbx, %rcx
 295a329:      	shlq	$0x4, %rcx
 295a32d:      	cmpw	$0x3e, (%rax,%rcx)
 295a332:      	je	0x295a3eb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x250b>
 295a338:      	movq	%rbp, %r15
 295a33b:      	movq	0x48(%r14), %rsi
 295a33f:      	movq	%rsi, 0x30(%rsp)
 295a344:      	testq	%rsi, %rsi
 295a347:      	movl	%r11d, %ebp
 295a34a:      	je	0x295a35b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x247b>
 295a34c:      	leaq	0x30(%rsp), %rdi
 295a351:      	movl	$0x1, %edx
 295a356:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a35b:      	movl	0x44(%r14), %eax
 295a35f:      	movl	%eax, 0x38(%rsp)
 295a363:      	movq	0x230(%rsp), %rax
 295a36b:      	movq	0x3b0(%rax), %rax
 295a372:      	testq	%rax, %rax
 295a375:      	je	0x295a37d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x249d>
 295a377:      	movl	0x8(%rax), %r9d
 295a37b:      	jmp	0x295a380 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x24a0>
 295a37d:      	xorl	%r9d, %r9d
 295a380:      	movq	%r14, 0xa0(%rsp)
 295a388:      	movl	%ebx, 0xa8(%rsp)
 295a38f:      	subq	$0x10, %rsp
 295a393:      	movdqu	0xb0(%rsp), %xmm0
 295a39c:      	movdqu	%xmm0, (%rsp)
 295a3a1:      	leaq	0x40(%rsp), %rdx
 295a3a6:      	movq	0x240(%rsp), %rdi
 295a3ae:      	movl	$0xf3, %esi
 295a3b3:      	movl	$0x3e, %ecx
 295a3b8:      	xorl	%r8d, %r8d
 295a3bb:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a3c0:      	addq	$0x10, %rsp
 295a3c4:      	movq	%rax, %r14
 295a3c7:      	movl	%edx, %ebx
 295a3c9:      	movq	0x30(%rsp), %rsi
 295a3ce:      	testq	%rsi, %rsi
 295a3d1:      	je	0x295a3dd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x24fd>
 295a3d3:      	leaq	0x30(%rsp), %rdi
 295a3d8:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a3dd:      	movl	%ebp, %r11d
 295a3e0:      	movq	%r15, %rbp
 295a3e3:      	movq	0x230(%rsp), %r15
 295a3eb:      	movq	%r14, 0x80(%rsp)
 295a3f3:      	movl	%ebx, 0x88(%rsp)
 295a3fa:      	movq	%r12, 0x70(%rsp)
 295a3ff:      	movq	%r13, 0x78(%rsp)
 295a404:      	subq	$0x20, %rsp
 295a408:      	movups	0x90(%rsp), %xmm0
 295a410:      	movups	%xmm0, 0x10(%rsp)
 295a415:      	movdqa	0xa0(%rsp), %xmm0
 295a41e:      	movdqu	%xmm0, (%rsp)
 295a423:      	movq	%r15, %rdi
 295a426:      	movl	$0x3e, %esi
 295a42b:      	xorl	%edx, %edx
 295a42d:      	movq	0x20(%rsp), %rcx
 295a432:      	movq	%rbp, %r8
 295a435:      	movl	%r11d, %r9d
 295a438:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295a43d:      	addq	$0x20, %rsp
 295a441:      	movl	%edx, %r8d
 295a444:      	movq	0x30(%rax), %rdx
 295a448:      	movl	%r8d, %ecx
 295a44b:      	shlq	$0x4, %rcx
 295a44f:      	cmpw	$0x6f, (%rdx,%rcx)
 295a454:      	je	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295a45a:      	movq	0x48(%rax), %rsi
 295a45e:      	movq	%rsi, 0x30(%rsp)
 295a463:      	testq	%rsi, %rsi
 295a466:      	je	0x295a483 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25a3>
 295a468:      	leaq	0x30(%rsp), %rdi
 295a46d:      	movl	$0x1, %edx
 295a472:      	movq	%rax, %rbx
 295a475:      	movl	%r8d, %ebp
 295a478:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a47d:      	movl	%ebp, %r8d
 295a480:      	movq	%rbx, %rax
 295a483:      	movl	0x44(%rax), %ecx
 295a486:      	movl	%ecx, 0x38(%rsp)
 295a48a:      	movq	0x3b0(%r15), %rcx
 295a491:      	testq	%rcx, %rcx
 295a494:      	je	0x295a49c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25bc>
 295a496:      	movl	0x8(%rcx), %r9d
 295a49a:      	jmp	0x295a49f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25bf>
 295a49c:      	xorl	%r9d, %r9d
 295a49f:      	movq	%rax, 0xa0(%rsp)
 295a4a7:      	movl	%r8d, 0xa8(%rsp)
 295a4af:      	subq	$0x10, %rsp
 295a4b3:      	movdqu	0xb0(%rsp), %xmm0
 295a4bc:      	movdqu	%xmm0, (%rsp)
 295a4c1:      	leaq	0x40(%rsp), %rdx
 295a4c6:      	movq	%r15, %rdi
 295a4c9:      	movl	$0xf3, %esi
 295a4ce:      	movl	$0x6f, %ecx
 295a4d3:      	xorl	%r8d, %r8d
 295a4d6:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295a4db:      	addq	$0x10, %rsp
 295a4df:      	movl	%edx, %r8d
 295a4e2:      	movq	0x30(%rsp), %rsi
 295a4e7:      	testq	%rsi, %rsi
 295a4ea:      	je	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295a4f0:      	leaq	0x30(%rsp), %rdi
 295a4f5:      	movq	%rax, %rbx
 295a4f8:      	movl	%r8d, %ebp
 295a4fb:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a500:      	movl	%ebp, %r8d
 295a503:      	movq	%rbx, %rax
 295a506:      	jmp	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295a50b:      	movl	$0x3e, %esi
 295a510:      	movq	0x10(%rsp), %r13
 295a515:      	movq	%r13, %rdx
 295a518:      	movq	%r13, %r8
 295a51b:      	movl	%ecx, %r9d
 295a51e:      	pushq	$0x0
 295a520:      	movq	0x238(%rsp), %r15
 295a528:      	pushq	%r15
 295a52a:      	pushq	%rbx
 295a52b:      	pushq	%r10
 295a52d:      	pushq	%r11
 295a52f:      	pushq	%r12
 295a531:      	movl	%ecx, %ebp
 295a533:      	movq	%r11, %r15
 295a536:      	callq	0x2963010 <_ZL19lowerShuffleAsShiftRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGEb>
 295a53b:      	addq	$0x30, %rsp
 295a53f:      	testq	%rax, %rax
 295a542:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a548:      	movq	(%rsp), %rdi
 295a54c:      	movl	$0x3e, %esi
 295a551:      	movq	%r13, %rdx
 295a554:      	movl	%ebp, %ecx
 295a556:      	movq	%r14, %r8
 295a559:      	movl	0x58(%rsp), %r9d
 295a55e:      	pushq	0x230(%rsp)
 295a565:      	pushq	%rbx
 295a566:      	pushq	%r15
 295a568:      	pushq	%r12
 295a56a:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a56f:      	addq	$0x20, %rsp
 295a573:      	testq	%rax, %rax
 295a576:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a57c:      	movl	0x148(%rbx), %eax
 295a582:      	movzbl	0x1db(%rbx), %r10d
 295a58a:      	subq	$0x8, %rsp
 295a58e:      	movq	0x8(%rsp), %rdi
 295a593:      	movl	$0x3e, %esi
 295a598:      	movq	%r13, %rdx
 295a59b:      	movl	%ebp, %ecx
 295a59d:      	movq	%r12, %r8
 295a5a0:      	movq	%r15, %r9
 295a5a3:      	pushq	0x238(%rsp)
 295a5aa:      	pushq	%r10
 295a5ac:      	pushq	%rax
 295a5ad:      	callq	0x296ff60 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a5b2:      	addq	$0x20, %rsp
 295a5b6:      	testq	%rax, %rax
 295a5b9:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a5bf:      	subq	$0x8, %rsp
 295a5c3:      	movq	0x8(%rsp), %rdi
 295a5c8:      	movl	$0x3e, %esi
 295a5cd:      	movq	%r13, %rdx
 295a5d0:      	movl	%ebp, %ecx
 295a5d2:      	movq	%r14, %r8
 295a5d5:      	movq	%r14, %rbx
 295a5d8:      	movl	0x60(%rsp), %r14d
 295a5dd:      	movl	%r14d, %r9d
 295a5e0:      	pushq	0x238(%rsp)
 295a5e7:      	pushq	%r15
 295a5e9:      	pushq	%r12
 295a5eb:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295a5f0:      	addq	$0x20, %rsp
 295a5f4:      	testq	%rax, %rax
 295a5f7:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a5fd:      	movq	(%rsp), %rdi
 295a601:      	movl	$0x3e, %esi
 295a606:      	movq	%r13, %rdx
 295a609:      	movl	%ebp, %ecx
 295a60b:      	movq	%rbx, %r8
 295a60e:      	movl	%r14d, %r9d
 295a611:      	pushq	0x230(%rsp)
 295a618:      	movq	0x230(%rsp), %rbx
 295a620:      	pushq	%rbx
 295a621:      	pushq	%r15
 295a623:      	pushq	%r12
 295a625:      	callq	0x2971bb0 <_ZL20lowerShuffleWithPACKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a62a:      	addq	$0x20, %rsp
 295a62e:      	testq	%rax, %rax
 295a631:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a637:      	movq	(%rsp), %rdi
 295a63b:      	movl	$0x3e, %esi
 295a640:      	movq	%r13, %rdx
 295a643:      	movl	%ebp, %ecx
 295a645:      	movq	%r13, %r8
 295a648:      	movl	%ebp, %r9d
 295a64b:      	pushq	0x230(%rsp)
 295a652:      	pushq	%rbx
 295a653:      	pushq	%r15
 295a655:      	pushq	%r12
 295a657:      	callq	0x2966110 <_ZL24lowerShuffleAsByteRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a65c:      	addq	$0x20, %rsp
 295a660:      	testq	%rax, %rax
 295a663:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a669:      	leaq	0xa0(%rsp), %rdi
 295a671:      	movq	%r12, %rsi
 295a674:      	movq	%r15, %rdx
 295a677:      	callq	0x2954010 <_ZN4llvm11SmallVectorIiLj8EEC2IivEENS_8ArrayRefIT_EE>
 295a67c:      	movq	0xa0(%rsp), %r8
 295a684:      	movl	0xa8(%rsp), %r9d
 295a68c:      	movq	(%rsp), %rdi
 295a690:      	movl	$0x3e, %esi
 295a695:      	movq	%r13, %rdx
 295a698:      	movl	%ebp, %ecx
 295a69a:      	pushq	0x230(%rsp)
 295a6a1:      	pushq	%rbx
 295a6a2:      	callq	0x2971fe0 <_ZL35lowerV8I16GeneralSingleInputShuffleRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_15MutableArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a6a7:      	addq	$0x10, %rsp
 295a6ab:      	movq	%rax, %rbx
 295a6ae:      	movl	%edx, %ebp
 295a6b0:      	movq	0xa0(%rsp), %rdi
 295a6b8:      	leaq	0xb0(%rsp), %rax
 295a6c0:      	cmpq	%rax, %rdi
 295a6c3:      	je	0x295a6ca <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x27ea>
 295a6c5:      	callq	0x828a640 <free@plt>
 295a6ca:      	movq	%rbx, %rax
 295a6cd:      	movl	%ebp, %r8d
 295a6d0:      	jmp	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295a6d5:      	movq	0x48(%r12), %rsi
 295a6da:      	movq	%rsi, 0x30(%rsp)
 295a6df:      	testq	%rsi, %rsi
 295a6e2:      	movq	%r12, %rbx
 295a6e5:      	je	0x295a6f6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2816>
 295a6e7:      	leaq	0x30(%rsp), %rdi
 295a6ec:      	movl	$0x1, %edx
 295a6f1:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295a6f6:      	movl	0x44(%rbx), %eax
 295a6f9:      	movl	%eax, 0x38(%rsp)
 295a6fd:      	movq	0x3b0(%r15), %rax
 295a704:      	testq	%rax, %rax
 295a707:      	je	0x295ae88 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2fa8>
 295a70d:      	movl	0x8(%rax), %r9d
 295a711:      	jmp	0x295ae8b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2fab>
 295a716:      	movq	%rbx, %r12
 295a719:      	movq	0x10(%rsp), %rdx
 295a71e:      	movq	%rdx, 0x28(%rsp)
 295a723:      	movl	%ebp, %r10d
 295a726:      	movl	%ebp, %ebx
 295a728:      	cmpl	$-0x1, %ecx
 295a72b:      	jne	0x295a77e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x289e>
 295a72d:      	xorps	%xmm0, %xmm0
 295a730:      	movaps	%xmm0, 0xa0(%rsp)
 295a738:      	leaq	0xa0(%rsp), %rdx
 295a740:      	movq	%r15, %rdi
 295a743:      	movl	$0x35, %esi
 295a748:      	movl	$0x96, %ecx
 295a74d:      	xorl	%r8d, %r8d
 295a750:      	callq	0x5e1ec00 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTE>
 295a755:      	movq	%rax, 0x28(%rsp)
 295a75a:      	movl	%edx, %ebx
 295a75c:      	movq	0xa0(%rsp), %rsi
 295a764:      	testq	%rsi, %rsi
 295a767:      	je	0x295a776 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2896>
 295a769:      	leaq	0xa0(%rsp), %rdi
 295a771:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a776:      	movl	0x4(%r12), %eax
 295a77b:      	movl	%ebp, %r10d
 295a77e:      	cmpl	$-0x1, %eax
 295a781:      	jne	0x295a7d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x28f3>
 295a783:      	xorps	%xmm0, %xmm0
 295a786:      	movaps	%xmm0, 0xa0(%rsp)
 295a78e:      	leaq	0xa0(%rsp), %rdx
 295a796:      	movq	%r15, %rdi
 295a799:      	movl	$0x35, %esi
 295a79e:      	movl	$0x96, %ecx
 295a7a3:      	xorl	%r8d, %r8d
 295a7a6:      	callq	0x5e1ec00 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTE>
 295a7ab:      	movq	%rax, 0x10(%rsp)
 295a7b0:      	movl	%edx, %r10d
 295a7b3:      	movq	0xa0(%rsp), %rsi
 295a7bb:      	testq	%rsi, %rsi
 295a7be:      	je	0x295a7d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x28f3>
 295a7c0:      	leaq	0xa0(%rsp), %rdi
 295a7c8:      	movl	%r10d, %ebp
 295a7cb:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295a7d0:      	movl	%ebp, %r10d
 295a7d3:      	movl	%r14d, %esi
 295a7d6:      	subq	$0x8, %rsp
 295a7da:      	xorl	%r14d, %r14d
 295a7dd:      	movq	%r15, %rdi
 295a7e0:      	movq	%r13, %rdx
 295a7e3:      	movl	$0x5, %ecx
 295a7e8:      	xorl	%r8d, %r8d
 295a7eb:      	movl	$0x1, %r9d
 295a7f1:      	pushq	$0x0
 295a7f3:      	movl	%r10d, %ebp
 295a7f6:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295a7fb:      	addq	$0x10, %rsp
 295a7ff:      	movq	%rax, 0xa0(%rsp)
 295a807:      	movl	%edx, 0xa8(%rsp)
 295a80e:      	movq	0x10(%rsp), %rax
 295a813:      	movq	%rax, 0x30(%rsp)
 295a818:      	movl	%ebp, 0x38(%rsp)
 295a81c:      	movq	0x28(%rsp), %rax
 295a821:      	movq	%rax, 0x70(%rsp)
 295a826:      	movl	%ebx, 0x78(%rsp)
 295a82a:      	movq	0x3b0(%r15), %rax
 295a831:      	testq	%rax, %rax
 295a834:      	je	0x295a83a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x295a>
 295a836:      	movl	0x8(%rax), %r14d
 295a83a:      	subq	$0x30, %rsp
 295a83e:      	movups	0xd0(%rsp), %xmm0
 295a846:      	movups	%xmm0, 0x20(%rsp)
 295a84b:      	movups	0x60(%rsp), %xmm0
 295a850:      	movups	%xmm0, 0x10(%rsp)
 295a855:      	movdqu	0xa0(%rsp), %xmm0
 295a85e:      	movdqu	%xmm0, (%rsp)
 295a863:      	movq	%r15, %rdi
 295a866:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295a86b:      	movq	%r13, %rdx
 295a86e:      	movl	$0x96, %ecx
 295a873:      	xorl	%r8d, %r8d
 295a876:      	movl	%r14d, %r9d
 295a879:      	callq	0x5e2ac90 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295a87e:      	addq	$0x30, %rsp
 295a882:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a887:      	leaq	-0x4(%r9), %rdi
 295a88b:      	cmpq	$0xc, %rdi
 295a88f:      	movq	%r13, 0x28(%rsp)
 295a894:      	jae	0x295aa70 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b90>
 295a89a:      	xorl	%esi, %esi
 295a89c:      	movq	%r12, %rax
 295a89f:      	movq	0x230(%rsp), %r15
 295a8a7:      	jmp	0x295ab20 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c40>
 295a8ac:      	movl	%ebx, %r8d
 295a8af:      	movq	%r13, %rbp
 295a8b2:      	jmp	0x295b636 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3756>
 295a8b7:      	cmpl	$0x8, 0x148(%r14)
 295a8bf:      	movq	(%rsp), %rdi
 295a8c3:      	movl	%ebp, %r11d
 295a8c6:      	movq	%r12, %rbp
 295a8c9:      	movq	0x58(%rsp), %r12
 295a8ce:      	movq	0x220(%rsp), %r10
 295a8d6:      	jl	0x295a915 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2a35>
 295a8d8:      	movq	%rbp, %rsi
 295a8db:      	movl	%r11d, %edx
 295a8de:      	movq	%r13, %rcx
 295a8e1:      	movl	%ebx, %r8d
 295a8e4:      	movq	%r12, %r9
 295a8e7:      	pushq	0x230(%rsp)
 295a8ee:      	pushq	0x30(%rsp)
 295a8f2:      	movl	%r11d, %ebx
 295a8f5:      	movq	%r10, %r13
 295a8f8:      	callq	0x2962b00 <_ZL29lowerShuffleOfExtractsAsVpermRKN4llvm5SDLocENS_7SDValueES3_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295a8fd:      	movq	%r13, %r10
 295a900:      	movl	%ebx, %r11d
 295a903:      	movq	0x10(%rsp), %rdi
 295a908:      	addq	$0x10, %rsp
 295a90c:      	testq	%rax, %rax
 295a90f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a915:      	cmpl	$0x1, %r15d
 295a919:      	movq	0x230(%rsp), %r15
 295a921:      	jne	0x295a986 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2aa6>
 295a923:      	cmpl	$0x4, (%r12)
 295a928:      	jl	0x295a986 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2aa6>
 295a92a:      	movq	0x60(%rsp), %r8
 295a92f:      	movl	0x68(%rsp), %r9d
 295a934:      	movl	0x8(%r10), %eax
 295a938:      	movq	%rdi, %rbx
 295a93b:      	movl	$0x84, %esi
 295a940:      	movq	%rbp, %rdx
 295a943:      	movl	%r11d, %ecx
 295a946:      	pushq	%r15
 295a948:      	pushq	0x230(%rsp)
 295a94f:      	pushq	%rax
 295a950:      	pushq	(%r10)
 295a953:      	pushq	0x48(%rsp)
 295a957:      	pushq	%r12
 295a959:      	movq	%r15, %r13
 295a95c:      	movq	%rbp, %r14
 295a95f:      	movl	%r11d, %ebp
 295a962:      	movq	%r10, %r15
 295a965:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295a96a:      	movq	%r15, %r10
 295a96d:      	movl	%ebp, %r11d
 295a970:      	movq	%r14, %rbp
 295a973:      	movq	%r13, %r15
 295a976:      	movq	%rbx, %rdi
 295a979:      	addq	$0x30, %rsp
 295a97d:      	testq	%rax, %rax
 295a980:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295a986:      	movq	0x228(%rsp), %rax
 295a98e:      	movl	0x148(%rax), %eax
 295a994:      	cmpl	$0x4, %eax
 295a997:      	jle	0x295a9eb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b0b>
 295a999:      	movl	(%r12), %eax
 295a99d:      	testl	%eax, %eax
 295a99f:      	js	0x295a9be <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ade>
 295a9a1:      	movl	0x4(%r12), %ecx
 295a9a6:      	testl	%ecx, %ecx
 295a9a8:      	js	0x295a9be <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ade>
 295a9aa:      	cmpl	$0x4, %eax
 295a9ad:      	setb	%al
 295a9b0:      	cmpl	$0x4, %ecx
 295a9b3:      	setae	%cl
 295a9b6:      	cmpb	%cl, %al
 295a9b8:      	je	0x295b21e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x333e>
 295a9be:      	movl	0x8(%r12), %eax
 295a9c3:      	testl	%eax, %eax
 295a9c5:      	js	0x295a9e4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b04>
 295a9c7:      	movl	0xc(%r12), %ecx
 295a9cc:      	testl	%ecx, %ecx
 295a9ce:      	js	0x295a9e4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b04>
 295a9d0:      	cmpl	$0x4, %eax
 295a9d3:      	setb	%al
 295a9d6:      	cmpl	$0x4, %ecx
 295a9d9:      	setae	%cl
 295a9dc:      	xorb	%al, %cl
 295a9de:      	je	0x295b21e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x333e>
 295a9e4:      	movq	0x60(%rsp), %r8
 295a9e9:      	jmp	0x295a9f9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b19>
 295a9eb:      	movq	0x60(%rsp), %r8
 295a9f0:      	cmpl	$0x2, %eax
 295a9f3:      	jl	0x295b3bd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x34dd>
 295a9f9:      	movl	0x68(%rsp), %ebx
 295a9fd:      	subq	$0x8, %rsp
 295aa01:      	movq	%rdi, %r13
 295aa04:      	movl	$0x84, %esi
 295aa09:      	movq	%rbp, %rdx
 295aa0c:      	movl	%r11d, %ecx
 295aa0f:      	movl	%ebx, %r9d
 295aa12:      	movq	%r15, %r14
 295aa15:      	pushq	%r15
 295aa17:      	movq	0x38(%rsp), %r15
 295aa1c:      	pushq	%r15
 295aa1e:      	pushq	%r12
 295aa20:      	movq	%r12, %rbx
 295aa23:      	movq	%rbp, %r12
 295aa26:      	movl	%r11d, %ebp
 295aa29:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295aa2e:      	addq	$0x20, %rsp
 295aa32:      	testq	%rax, %rax
 295aa35:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295aa3b:      	subq	$0x20, %rsp
 295aa3f:      	movdqa	0x80(%rsp), %xmm0
 295aa48:      	movdqu	%xmm0, (%rsp)
 295aa4d:      	movq	%r14, 0x10(%rsp)
 295aa52:      	movq	%r13, %rdi
 295aa55:      	movl	$0x84, %esi
 295aa5a:      	movq	%rbx, %rdx
 295aa5d:      	movq	%r15, %rcx
 295aa60:      	movq	%r12, %r8
 295aa63:      	movl	%ebp, %r9d
 295aa66:      	callq	0x2970650 <_ZL22lowerShuffleWithSHUFPSRKN4llvm5SDLocENS_3MVTENS_8ArrayRefIiEENS_7SDValueES6_RNS_12SelectionDAGE>
 295aa6b:      	jmp	0x2959c7c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d9c>
 295aa70:      	shrq	$0x2, %rdi
 295aa74:      	incq	%rdi
 295aa77:      	movabsq	$0x7ffffffffffffff8, %rdx # imm = 0x7FFFFFFFFFFFFFF8
 295aa81:      	orq	$0x4, %rdx
 295aa85:      	andq	%rdi, %rdx
 295aa88:      	leaq	(%r12,%rdx,4), %rax
 295aa8c:      	pxor	%xmm0, %xmm0
 295aa90:      	xorl	%esi, %esi
 295aa92:      	movdqa	-0x1b3baaa(%rip), %xmm1 # 0xe1eff0 <.LCPI91_5>
 295aa9a:      	pcmpeqd	%xmm2, %xmm2
 295aa9e:      	movdqa	-0x1b377a6(%rip), %xmm4 # 0xe23300 <.LCPI91_4>
 295aaa6:      	pxor	%xmm3, %xmm3
 295aaaa:      	movq	(%r12,%rsi,4), %xmm5
 295aab0:      	movq	0x8(%r12,%rsi,4), %xmm6
 295aab7:      	movdqa	%xmm5, %xmm7
 295aabb:      	pmaxud	%xmm1, %xmm7
 295aac0:      	pcmpeqd	%xmm5, %xmm7
 295aac4:      	pxor	%xmm2, %xmm7
 295aac8:      	pmovzxdq	%xmm7, %xmm5            # xmm5 = xmm7[0],zero,xmm7[1],zero
 295aacd:      	pand	%xmm4, %xmm5
 295aad1:      	paddq	%xmm5, %xmm3
 295aad5:      	movdqa	%xmm6, %xmm5
 295aad9:      	pmaxud	%xmm1, %xmm5
 295aade:      	pcmpeqd	%xmm6, %xmm5
 295aae2:      	pxor	%xmm2, %xmm5
 295aae6:      	pmovzxdq	%xmm5, %xmm5            # xmm5 = xmm5[0],zero,xmm5[1],zero
 295aaeb:      	pand	%xmm4, %xmm5
 295aaef:      	paddq	%xmm5, %xmm0
 295aaf3:      	addq	$0x4, %rsi
 295aaf7:      	cmpq	%rsi, %rdx
 295aafa:      	jne	0x295aaaa <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2bca>
 295aafc:      	paddq	%xmm3, %xmm0
 295ab00:      	pshufd	$0xee, %xmm0, %xmm1     # xmm1 = xmm0[2,3,2,3]
 295ab05:      	paddq	%xmm0, %xmm1
 295ab09:      	movq	%xmm1, %rsi
 295ab0e:      	cmpq	%rdx, %rdi
 295ab11:      	movq	0x230(%rsp), %r15
 295ab19:      	je	0x295ab30 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c50>
 295ab1b:      	nopl	(%rax,%rax)
 295ab20:      	cmpl	$0x4, (%rax)
 295ab23:      	adcq	$0x0, %rsi
 295ab27:      	addq	$0x4, %rax
 295ab2b:      	cmpq	%rbp, %rax
 295ab2e:      	jne	0x295ab20 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c40>
 295ab30:      	cmpq	$0x2, %rsi
 295ab34:      	movq	0x10(%rsp), %r13
 295ab39:      	movq	0x20(%rsp), %r8
 295ab3e:      	jb	0x295ab73 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2c93>
 295ab40:      	movq	(%rsp), %rdi
 295ab44:      	movl	$0x49, %esi
 295ab49:      	movq	%r13, %rdx
 295ab4c:      	movq	%r9, %rbx
 295ab4f:      	movq	0x18(%rsp), %r9
 295ab54:      	pushq	%r15
 295ab56:      	pushq	%r14
 295ab58:      	pushq	0x38(%rsp)
 295ab5c:      	pushq	%r12
 295ab5e:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295ab63:      	movq	%rbx, %r9
 295ab66:      	addq	$0x20, %rsp
 295ab6a:      	testq	%rax, %rax
 295ab6d:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295ab73:      	movaps	-0x1b3a85a(%rip), %xmm0 # 0xe20320 <.Lswitch.table._ZN4llvm5XCOFF25parseParmsTypeWithVecInfoEjjjj.10>
 295ab7a:      	movaps	%xmm0, 0x70(%rsp)
 295ab7f:      	movaps	-0x1b42b76(%rip), %xmm0 # 0xe18010 <.L__const._ZL17lowerV4I32ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGE.UnpackHiMask>
 295ab86:      	movaps	%xmm0, 0x80(%rsp)
 295ab8e:      	xorl	%eax, %eax
 295ab90:      	xorl	%ecx, %ecx
 295ab92:      	xorl	%edx, %edx
 295ab94:      	jmp	0x295aba6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cc6>
 295ab96:      	incq	%rcx
 295ab99:      	movl	%edi, %esi
 295ab9b:      	addq	$0x4, %rax
 295ab9f:      	movl	%esi, %edi
 295aba1:      	cmpq	%rax, %r9
 295aba4:      	je	0x295abc0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ce0>
 295aba6:      	movl	(%r12,%rax), %esi
 295abaa:      	cmpl	$-0x1, %esi
 295abad:      	je	0x295ab96 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cb6>
 295abaf:      	cmpb	$0x1, %dl
 295abb2:      	jne	0x295abbc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cdc>
 295abb4:      	movb	$0x1, %dl
 295abb6:      	cmpl	%esi, %edi
 295abb8:      	je	0x295ab9b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cbb>
 295abba:      	jmp	0x295abdf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cff>
 295abbc:      	movb	$0x1, %dl
 295abbe:      	jmp	0x295ab9b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cbb>
 295abc0:      	movq	0x28(%rsp), %rax
 295abc5:      	shrq	%rax
 295abc8:      	cmpq	%rax, %rcx
 295abcb:      	setbe	%al
 295abce:      	testb	%dl, %al
 295abd0:      	je	0x295abdf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2cff>
 295abd2:      	movq	%r12, %rdi
 295abd5:      	movq	0x28(%rsp), %rbx
 295abda:      	jmp	0x2959be7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d07>
 295abdf:      	movq	0x28(%rsp), %rax
 295abe4:      	movq	%rax, %rbp
 295abe7:      	cmpq	$0x4, %rax
 295abeb:      	jne	0x2959b95 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cb5>
 295abf1:      	movl	(%r12), %eax
 295abf5:      	testl	%eax, %eax
 295abf7:      	jle	0x295ac3c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2d5c>
 295abf9:      	xorl	%ecx, %ecx
 295abfb:      	cmpl	$0x4, %eax
 295abfe:      	setb	%cl
 295ac01:      	movq	0x20(%rsp), %rsi
 295ac06:      	cmovbq	%r13, %rsi
 295ac0a:      	movq	0x18(%rsp), %rdx
 295ac0f:      	movl	0xc(%rsp), %r8d
 295ac14:      	cmovbl	%r8d, %edx
 295ac18:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ac1d:      	subq	$0x8, %rsp
 295ac21:      	movl	$0x4, %edi
 295ac26:      	movq	%r13, %rcx
 295ac29:      	pushq	$0x0
 295ac2b:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ac30:      	addq	$0x10, %rsp
 295ac34:      	testb	%al, %al
 295ac36:      	je	0x2959b95 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cb5>
 295ac3c:      	movl	0x4(%r12), %eax
 295ac41:      	testl	%eax, %eax
 295ac43:      	jle	0x295ac88 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2da8>
 295ac45:      	xorl	%ecx, %ecx
 295ac47:      	cmpl	$0x4, %eax
 295ac4a:      	setb	%cl
 295ac4d:      	movq	0x20(%rsp), %rsi
 295ac52:      	cmovbq	%r13, %rsi
 295ac56:      	movq	0x18(%rsp), %rdx
 295ac5b:      	movl	0xc(%rsp), %r8d
 295ac60:      	cmovbl	%r8d, %edx
 295ac64:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ac69:      	subq	$0x8, %rsp
 295ac6d:      	movl	$0x4, %edi
 295ac72:      	movq	%r13, %rcx
 295ac75:      	pushq	$0x0
 295ac77:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ac7c:      	addq	$0x10, %rsp
 295ac80:      	testb	%al, %al
 295ac82:      	je	0x2959b95 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cb5>
 295ac88:      	movl	0x8(%r12), %eax
 295ac8d:      	testl	%eax, %eax
 295ac8f:      	sets	%cl
 295ac92:      	cmpl	$0x1, %eax
 295ac95:      	sete	%dl
 295ac98:      	orb	%cl, %dl
 295ac9a:      	jne	0x295acdf <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2dff>
 295ac9c:      	xorl	%ecx, %ecx
 295ac9e:      	cmpl	$0x4, %eax
 295aca1:      	setb	%cl
 295aca4:      	movq	0x20(%rsp), %rsi
 295aca9:      	cmovbq	%r13, %rsi
 295acad:      	movq	0x18(%rsp), %rdx
 295acb2:      	movl	0xc(%rsp), %r8d
 295acb7:      	cmovbl	%r8d, %edx
 295acbb:      	leal	-0x4(%rax,%rcx,4), %r9d
 295acc0:      	subq	$0x8, %rsp
 295acc4:      	movl	$0x4, %edi
 295acc9:      	movq	%r13, %rcx
 295accc:      	pushq	$0x1
 295acce:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295acd3:      	addq	$0x10, %rsp
 295acd7:      	testb	%al, %al
 295acd9:      	je	0x2959b95 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cb5>
 295acdf:      	movl	0xc(%r12), %eax
 295ace4:      	testl	%eax, %eax
 295ace6:      	sets	%cl
 295ace9:      	cmpl	$0x1, %eax
 295acec:      	sete	%dl
 295acef:      	orb	%cl, %dl
 295acf1:      	movl	$0x4, %ebx
 295acf6:      	leaq	0x70(%rsp), %rdi
 295acfb:      	jne	0x2959be7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d07>
 295ad01:      	xorl	%ecx, %ecx
 295ad03:      	cmpl	$0x4, %eax
 295ad06:      	setb	%cl
 295ad09:      	movq	0x20(%rsp), %rsi
 295ad0e:      	cmovbq	%r13, %rsi
 295ad12:      	movq	0x18(%rsp), %rdx
 295ad17:      	movl	0xc(%rsp), %r8d
 295ad1c:      	cmovbl	%r8d, %edx
 295ad20:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ad25:      	subq	$0x8, %rsp
 295ad29:      	movq	%rdi, %r14
 295ad2c:      	movl	$0x4, %edi
 295ad31:      	movq	%r13, %rcx
 295ad34:      	pushq	$0x1
 295ad36:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ad3b:      	movq	%r14, %rdi
 295ad3e:      	addq	$0x10, %rsp
 295ad42:      	testb	%al, %al
 295ad44:      	je	0x2959b95 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1cb5>
 295ad4a:      	jmp	0x2959be7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d07>
 295ad4f:      	cmpl	$0x5, 0x148(%r14)
 295ad57:      	jl	0x295ad9b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2ebb>
 295ad59:      	subq	$0x8, %rsp
 295ad5d:      	movq	0x8(%rsp), %rdi
 295ad62:      	movl	$0x96, %esi
 295ad67:      	movq	%rbp, %rdx
 295ad6a:      	movl	0x14(%rsp), %ecx
 295ad6e:      	movq	%r15, %r8
 295ad71:      	movl	0x20(%rsp), %r9d
 295ad76:      	pushq	0x238(%rsp)
 295ad7d:      	pushq	%r14
 295ad7f:      	pushq	0x238(%rsp)
 295ad86:      	pushq	%rbx
 295ad87:      	pushq	%r12
 295ad89:      	callq	0x2964320 <_ZL19lowerShuffleAsBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295ad8e:      	addq	$0x30, %rsp
 295ad92:      	testq	%rax, %rax
 295ad95:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295ad9b:      	subq	$0x8, %rsp
 295ad9f:      	movq	0x8(%rsp), %r13
 295ada4:      	movq	%r13, %rdi
 295ada7:      	movl	$0x96, %esi
 295adac:      	movq	%rbp, %rdx
 295adaf:      	movq	%rbx, %rax
 295adb2:      	movq	%r12, %rbx
 295adb5:      	movq	%rbp, %r12
 295adb8:      	movl	0x14(%rsp), %ebp
 295adbc:      	movl	%ebp, %ecx
 295adbe:      	movq	%r15, %r8
 295adc1:      	movl	0x20(%rsp), %r9d
 295adc6:      	movq	0x238(%rsp), %r15
 295adce:      	pushq	%r15
 295add0:      	pushq	%rax
 295add1:      	pushq	%rbx
 295add2:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295add7:      	addq	$0x20, %rsp
 295addb:      	testq	%rax, %rax
 295adde:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295ade4:      	xorl	%eax, %eax
 295ade6:      	cmpl	$0x1, (%rbx)
 295ade9:      	sete	%al
 295adec:      	xorl	%ecx, %ecx
 295adee:      	cmpl	$0x3, 0x4(%rbx)
 295adf2:      	sete	%cl
 295adf5:      	leaq	(%rax,%rcx,2), %rsi
 295adf9:      	subq	$0x8, %rsp
 295adfd:      	xorl	%ebx, %ebx
 295adff:      	movq	%r15, %rdi
 295ae02:      	movq	%r13, %rdx
 295ae05:      	movl	$0x5, %ecx
 295ae0a:      	xorl	%r8d, %r8d
 295ae0d:      	movl	$0x1, %r9d
 295ae13:      	pushq	$0x0
 295ae15:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295ae1a:      	addq	$0x10, %rsp
 295ae1e:      	movq	%rax, 0xa0(%rsp)
 295ae26:      	movl	%edx, 0xa8(%rsp)
 295ae2d:      	movq	%r12, 0x30(%rsp)
 295ae32:      	movl	%ebp, 0x38(%rsp)
 295ae36:      	movq	0x3b0(%r15), %rax
 295ae3d:      	testq	%rax, %rax
 295ae40:      	je	0x295ae45 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2f65>
 295ae42:      	movl	0x8(%rax), %ebx
 295ae45:      	subq	$0x30, %rsp
 295ae49:      	movups	0xd0(%rsp), %xmm0
 295ae51:      	movups	%xmm0, 0x20(%rsp)
 295ae56:      	leaq	0x240(%rsp), %rax
 295ae5e:      	movups	(%rax), %xmm0
 295ae61:      	movups	%xmm0, 0x10(%rsp)
 295ae66:      	movdqu	0x60(%rsp), %xmm0
 295ae6c:      	movdqu	%xmm0, (%rsp)
 295ae71:      	movq	%r15, %rdi
 295ae74:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295ae79:      	movq	0x30(%rsp), %rdx
 295ae7e:      	movl	$0x96, %ecx
 295ae83:      	jmp	0x295b8d9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x39f9>
 295ae88:      	xorl	%r9d, %r9d
 295ae8b:      	movq	%rbx, 0xa0(%rsp)
 295ae93:      	movl	%r13d, 0xa8(%rsp)
 295ae9b:      	subq	$0x10, %rsp
 295ae9f:      	movdqu	0xb0(%rsp), %xmm0
 295aea8:      	movdqu	%xmm0, (%rsp)
 295aead:      	leaq	0x40(%rsp), %rdx
 295aeb2:      	movq	%r15, %rdi
 295aeb5:      	movl	$0xf3, %esi
 295aeba:      	movl	$0x49, %ecx
 295aebf:      	xorl	%r8d, %r8d
 295aec2:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295aec7:      	addq	$0x10, %rsp
 295aecb:      	movq	%rax, %rbp
 295aece:      	movl	%edx, %r13d
 295aed1:      	movq	0x30(%rsp), %rsi
 295aed6:      	testq	%rsi, %rsi
 295aed9:      	je	0x295aee5 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3005>
 295aedb:      	leaq	0x30(%rsp), %rdi
 295aee0:      	callq	0x3bd6c10 <_ZN4llvm16MetadataTracking7untrackEPvRNS_8MetadataE>
 295aee5:      	movl	(%r14), %eax
 295aee8:      	leal	(%rax,%rax), %ecx
 295aeeb:      	testl	%eax, %eax
 295aeed:      	leal	0x1(%rax,%rax), %eax
 295aef1:      	movl	$0xffffffff, %edx       # imm = 0xFFFFFFFF
 295aef6:      	cmovsl	%edx, %ecx
 295aef9:      	cmovsl	%edx, %eax
 295aefc:      	movl	%ecx, 0x70(%rsp)
 295af00:      	movl	%eax, 0x74(%rsp)
 295af04:      	movl	0x4(%r14), %eax
 295af08:      	leal	(%rax,%rax), %ecx
 295af0b:      	testl	%eax, %eax
 295af0d:      	leal	0x1(%rax,%rax), %eax
 295af11:      	cmovsl	%edx, %ecx
 295af14:      	cmovsl	%edx, %eax
 295af17:      	movl	%ecx, 0x78(%rsp)
 295af1b:      	movl	%eax, 0x7c(%rsp)
 295af1f:      	leaq	0x70(%rsp), %rdi
 295af24:      	movl	$0x4, %esi
 295af29:      	callq	0x2962840 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295af2e:      	movl	%eax, %eax
 295af30:      	movl	$0x8, 0xa8(%rsp)
 295af3b:      	movq	%rax, 0xa0(%rsp)
 295af43:      	movq	0x40(%r15), %rdi
 295af47:      	leaq	0xa0(%rsp), %rsi
 295af4f:      	callq	0x3ae88a0 <_ZN4llvm11ConstantInt3getERNS_11LLVMContextERKNS_5APIntE>
 295af54:      	subq	$0x8, %rsp
 295af58:      	xorl	%ebx, %ebx
 295af5a:      	movq	%r15, %rdi
 295af5d:      	movq	%rax, %rsi
 295af60:      	movq	0x8(%rsp), %rdx
 295af65:      	movl	$0x5, %ecx
 295af6a:      	xorl	%r8d, %r8d
 295af6d:      	movl	$0x1, %r9d
 295af73:      	pushq	$0x0
 295af75:      	callq	0x5e00fe0 <_ZN4llvm12SelectionDAG11getConstantERKNS_11ConstantIntERKNS_5SDLocENS_3EVTEbb>
 295af7a:      	addq	$0x10, %rsp
 295af7e:      	cmpl	$0x41, 0xa8(%rsp)
 295af86:      	jb	0x295afaa <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x30ca>
 295af88:      	movq	0xa0(%rsp), %rdi
 295af90:      	testq	%rdi, %rdi
 295af93:      	je	0x295afaa <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x30ca>
 295af95:      	movq	%rax, %r14
 295af98:      	movq	%rbp, %r12
 295af9b:      	movl	%edx, %ebp
 295af9d:      	callq	0x828a7b0 <_ZdaPv@plt>
 295afa2:      	movl	%ebp, %edx
 295afa4:      	movq	%r12, %rbp
 295afa7:      	movq	%r14, %rax
 295afaa:      	movq	%rax, 0xa0(%rsp)
 295afb2:      	movl	%edx, 0xa8(%rsp)
 295afb9:      	movq	%rbp, 0x30(%rsp)
 295afbe:      	movl	%r13d, 0x38(%rsp)
 295afc3:      	movq	0x3b0(%r15), %rax
 295afca:      	testq	%rax, %rax
 295afcd:      	je	0x295afd2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x30f2>
 295afcf:      	movl	0x8(%rax), %ebx
 295afd2:      	subq	$0x20, %rsp
 295afd6:      	movups	0xc0(%rsp), %xmm0
 295afde:      	movups	%xmm0, 0x10(%rsp)
 295afe3:      	movdqu	0x50(%rsp), %xmm0
 295afe9:      	movdqu	%xmm0, (%rsp)
 295afee:      	movq	%r15, %rdi
 295aff1:      	movl	$0x2b9, %esi            # imm = 0x2B9
 295aff6:      	movq	0x20(%rsp), %rdx
 295affb:      	movl	$0x49, %ecx
 295b000:      	xorl	%r8d, %r8d
 295b003:      	movl	%ebx, %r9d
 295b006:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295b00b:      	addq	$0x20, %rsp
 295b00f:      	movl	%edx, %r8d
 295b012:      	movq	0x30(%rax), %rdx
 295b016:      	movl	%r8d, %ecx
 295b019:      	shlq	$0x4, %rcx
 295b01d:      	cmpw	$0x5e, (%rdx,%rcx)
 295b022:      	je	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295b028:      	movq	0x48(%rax), %rsi
 295b02c:      	movq	%rsi, 0x30(%rsp)
 295b031:      	testq	%rsi, %rsi
 295b034:      	je	0x295b051 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3171>
 295b036:      	leaq	0x30(%rsp), %rdi
 295b03b:      	movl	$0x1, %edx
 295b040:      	movq	%rax, %rbx
 295b043:      	movl	%r8d, %ebp
 295b046:      	callq	0x3bd6a00 <_ZN4llvm16MetadataTracking5trackEPvRNS_8MetadataENS_12PointerUnionIJPNS_15MetadataAsValueEPS2_PNS_14DebugValueUserEEEE>
 295b04b:      	movl	%ebp, %r8d
 295b04e:      	movq	%rbx, %rax
 295b051:      	movl	0x44(%rax), %ecx
 295b054:      	movl	%ecx, 0x38(%rsp)
 295b058:      	movq	0x3b0(%r15), %rcx
 295b05f:      	testq	%rcx, %rcx
 295b062:      	je	0x295b06a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x318a>
 295b064:      	movl	0x8(%rcx), %r9d
 295b068:      	jmp	0x295b06d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x318d>
 295b06a:      	xorl	%r9d, %r9d
 295b06d:      	movq	%rax, 0xa0(%rsp)
 295b075:      	movl	%r8d, 0xa8(%rsp)
 295b07d:      	subq	$0x10, %rsp
 295b081:      	movdqu	0xb0(%rsp), %xmm0
 295b08a:      	movdqu	%xmm0, (%rsp)
 295b08f:      	leaq	0x40(%rsp), %rdx
 295b094:      	movq	%r15, %rdi
 295b097:      	movl	$0xf3, %esi
 295b09c:      	movl	$0x5e, %ecx
 295b0a1:      	jmp	0x295a4d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x25f3>
 295b0a6:      	movl	(%r14), %eax
 295b0a9:      	testl	%eax, %eax
 295b0ab:      	sets	%cl
 295b0ae:      	cmpl	$0x1, %eax
 295b0b1:      	sete	%dl
 295b0b4:      	orb	%cl, %dl
 295b0b6:      	jne	0x295b0f7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3217>
 295b0b8:      	xorl	%ecx, %ecx
 295b0ba:      	cmpl	$0x4, %eax
 295b0bd:      	setb	%cl
 295b0c0:      	movq	%rbp, %rsi
 295b0c3:      	cmovbq	%r13, %rsi
 295b0c7:      	movq	0x20(%rsp), %rdx
 295b0cc:      	cmovbl	%r8d, %edx
 295b0d0:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b0d5:      	subq	$0x8, %rsp
 295b0d9:      	movl	$0x4, %edi
 295b0de:      	movq	%r13, %rcx
 295b0e1:      	pushq	$0x1
 295b0e3:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b0e8:      	movl	%ebx, %r8d
 295b0eb:      	addq	$0x10, %rsp
 295b0ef:      	testb	%al, %al
 295b0f1:      	je	0x295b585 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36a5>
 295b0f7:      	movl	0x4(%r14), %eax
 295b0fb:      	testl	%eax, %eax
 295b0fd:      	sets	%cl
 295b100:      	cmpl	$0x1, %eax
 295b103:      	sete	%dl
 295b106:      	orb	%cl, %dl
 295b108:      	jne	0x295b149 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3269>
 295b10a:      	xorl	%ecx, %ecx
 295b10c:      	cmpl	$0x4, %eax
 295b10f:      	setb	%cl
 295b112:      	movq	%rbp, %rsi
 295b115:      	cmovbq	%r13, %rsi
 295b119:      	movq	0x20(%rsp), %rdx
 295b11e:      	cmovbl	%r8d, %edx
 295b122:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b127:      	subq	$0x8, %rsp
 295b12b:      	movl	$0x4, %edi
 295b130:      	movq	%r13, %rcx
 295b133:      	pushq	$0x1
 295b135:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b13a:      	movl	%ebx, %r8d
 295b13d:      	addq	$0x10, %rsp
 295b141:      	testb	%al, %al
 295b143:      	je	0x295b585 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36a5>
 295b149:      	movl	0x8(%r14), %eax
 295b14d:      	testl	%eax, %eax
 295b14f:      	sets	%cl
 295b152:      	cmpl	$0x3, %eax
 295b155:      	sete	%dl
 295b158:      	orb	%cl, %dl
 295b15a:      	jne	0x295b19b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x32bb>
 295b15c:      	xorl	%ecx, %ecx
 295b15e:      	cmpl	$0x4, %eax
 295b161:      	setb	%cl
 295b164:      	movq	%rbp, %rsi
 295b167:      	cmovbq	%r13, %rsi
 295b16b:      	movq	0x20(%rsp), %rdx
 295b170:      	cmovbl	%r8d, %edx
 295b174:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b179:      	subq	$0x8, %rsp
 295b17d:      	movl	$0x4, %edi
 295b182:      	movq	%r13, %rcx
 295b185:      	pushq	$0x3
 295b187:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b18c:      	movl	%ebx, %r8d
 295b18f:      	addq	$0x10, %rsp
 295b193:      	testb	%al, %al
 295b195:      	je	0x295b585 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36a5>
 295b19b:      	movl	0xc(%r14), %eax
 295b19f:      	testl	%eax, %eax
 295b1a1:      	sets	%cl
 295b1a4:      	cmpl	$0x3, %eax
 295b1a7:      	sete	%dl
 295b1aa:      	orb	%cl, %dl
 295b1ac:      	jne	0x295b1ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x330d>
 295b1ae:      	xorl	%ecx, %ecx
 295b1b0:      	cmpl	$0x4, %eax
 295b1b3:      	setb	%cl
 295b1b6:      	movq	%rbp, %rsi
 295b1b9:      	cmovbq	%r13, %rsi
 295b1bd:      	movq	0x20(%rsp), %rdx
 295b1c2:      	cmovbl	%r8d, %edx
 295b1c6:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b1cb:      	subq	$0x8, %rsp
 295b1cf:      	movl	$0x4, %edi
 295b1d4:      	movq	%r13, %rcx
 295b1d7:      	pushq	$0x3
 295b1d9:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b1de:      	movl	%ebx, %r8d
 295b1e1:      	addq	$0x10, %rsp
 295b1e5:      	testb	%al, %al
 295b1e7:      	je	0x295b585 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x36a5>
 295b1ed:      	movq	%r13, 0xa0(%rsp)
 295b1f5:      	movl	%r8d, 0xa8(%rsp)
 295b1fd:      	movq	0x230(%rsp), %rdi
 295b205:      	movq	0x3b0(%rdi), %rax
 295b20c:      	testq	%rax, %rax
 295b20f:      	je	0x295bafc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c1c>
 295b215:      	movl	0x8(%rax), %r9d
 295b219:      	jmp	0x295baff <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c1f>
 295b21e:      	movq	%rdi, %r14
 295b221:      	movq	0x60(%rsp), %rax
 295b226:      	movl	0x68(%rsp), %ecx
 295b22a:      	movq	%r12, %r8
 295b22d:      	movq	%rbp, %r12
 295b230:      	movq	%rbp, 0x80(%rsp)
 295b238:      	movl	%r11d, %ebp
 295b23b:      	movl	%r11d, 0x88(%rsp)
 295b243:      	movq	%rax, %r13
 295b246:      	movq	%rax, 0x130(%rsp)
 295b24e:      	movl	%ecx, 0x18(%rsp)
 295b252:      	movl	%ecx, 0x138(%rsp)
 295b259:      	movl	$0x0, 0x188(%rsp)
 295b264:      	subq	$0x8, %rsp
 295b268:      	leaq	0x88(%rsp), %rdi
 295b270:      	leaq	0x138(%rsp), %rsi
 295b278:      	leaq	0x190(%rsp), %rdx
 295b280:      	movq	%r10, %rcx
 295b283:      	movq	%r8, 0x60(%rsp)
 295b288:      	movq	0x30(%rsp), %rbx
 295b28d:      	movq	%rbx, %r9
 295b290:      	pushq	%r15
 295b292:      	callq	0x2971010 <_ZL22matchShuffleAsInsertPSRN4llvm7SDValueES1_RjRKNS_5APIntENS_8ArrayRefIiEERNS_12SelectionDAGE>
 295b297:      	addq	$0x10, %rsp
 295b29b:      	testb	%al, %al
 295b29d:      	je	0x295b365 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3485>
 295b2a3:      	movups	0x80(%rsp), %xmm0
 295b2ab:      	movaps	%xmm0, 0x70(%rsp)
 295b2b0:      	movups	0x130(%rsp), %xmm0
 295b2b8:      	movaps	%xmm0, 0x30(%rsp)
 295b2bd:      	movl	0x188(%rsp), %esi
 295b2c4:      	subq	$0x8, %rsp
 295b2c8:      	xorl	%ebx, %ebx
 295b2ca:      	movq	%r15, %rdi
 295b2cd:      	movq	%r14, %rdx
 295b2d0:      	movl	$0x5, %ecx
 295b2d5:      	xorl	%r8d, %r8d
 295b2d8:      	movl	$0x1, %r9d
 295b2de:      	pushq	$0x0
 295b2e0:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b2e5:      	addq	$0x10, %rsp
 295b2e9:      	movq	%rax, 0xa0(%rsp)
 295b2f1:      	movl	%edx, 0xa8(%rsp)
 295b2f8:      	movq	0x3b0(%r15), %rax
 295b2ff:      	testq	%rax, %rax
 295b302:      	je	0x295b307 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3427>
 295b304:      	movl	0x8(%rax), %ebx
 295b307:      	subq	$0x30, %rsp
 295b30b:      	movups	0xd0(%rsp), %xmm0
 295b313:      	movups	%xmm0, 0x20(%rsp)
 295b318:      	movaps	0x60(%rsp), %xmm0
 295b31d:      	movups	%xmm0, 0x10(%rsp)
 295b322:      	movdqa	0xa0(%rsp), %xmm0
 295b32b:      	movdqu	%xmm0, (%rsp)
 295b330:      	movq	0x260(%rsp), %r15
 295b338:      	movq	%r15, %rdi
 295b33b:      	movl	$0x232, %esi            # imm = 0x232
 295b340:      	movq	%r14, %rdx
 295b343:      	movl	$0x84, %ecx
 295b348:      	xorl	%r8d, %r8d
 295b34b:      	movl	%ebx, %r9d
 295b34e:      	callq	0x5e2ac90 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295b353:      	addq	$0x30, %rsp
 295b357:      	testq	%rax, %rax
 295b35a:      	movq	0x28(%rsp), %rbx
 295b35f:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295b365:      	movq	%r14, %rdi
 295b368:      	movl	$0x84, %esi
 295b36d:      	movq	%r12, %rdx
 295b370:      	movl	%ebp, %ecx
 295b372:      	movq	%r13, %r8
 295b375:      	movl	0x18(%rsp), %r9d
 295b37a:      	pushq	$0x0
 295b37c:      	pushq	%r15
 295b37e:      	pushq	%rbx
 295b37f:      	movq	0x70(%rsp), %rbx
 295b384:      	pushq	%rbx
 295b385:      	callq	0x296c400 <_ZL29lowerShuffleAsBlendAndPermuteRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGEb>
 295b38a:      	addq	$0x20, %rsp
 295b38e:      	testq	%rax, %rax
 295b391:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295b397:      	movq	0x228(%rsp), %rax
 295b39f:      	movl	0x148(%rax), %eax
 295b3a5:      	movq	%r14, %rdi
 295b3a8:      	movl	%ebp, %r11d
 295b3ab:      	movq	%r12, %rbp
 295b3ae:      	movq	%rbx, %r12
 295b3b1:      	movq	%r13, %r8
 295b3b4:      	cmpl	$0x2, %eax
 295b3b7:      	jge	0x295a9f9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b19>
 295b3bd:      	movl	0x68(%rsp), %ebx
 295b3c1:      	cmpq	$0x4, 0x28(%rsp)
 295b3c7:      	jne	0x295a9fd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b1d>
 295b3cd:      	movq	%rdi, (%rsp)
 295b3d1:      	movl	(%r12), %eax
 295b3d5:      	testl	%eax, %eax
 295b3d7:      	movq	%r8, %r14
 295b3da:      	jle	0x295b42d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x354d>
 295b3dc:      	xorl	%ecx, %ecx
 295b3de:      	cmpl	$0x4, %eax
 295b3e1:      	setb	%cl
 295b3e4:      	movq	%r8, %rsi
 295b3e7:      	cmovbq	%rbp, %rsi
 295b3eb:      	movl	%ebx, %edx
 295b3ed:      	cmovbl	%r11d, %edx
 295b3f1:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b3f6:      	subq	$0x8, %rsp
 295b3fa:      	movl	$0x4, %edi
 295b3ff:      	movq	%rbp, %rcx
 295b402:      	movl	%r11d, %r8d
 295b405:      	pushq	$0x0
 295b407:      	movq	%r12, %r13
 295b40a:      	movq	%rbp, %r12
 295b40d:      	movl	%r11d, %ebp
 295b410:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b415:      	movq	%r14, %r8
 295b418:      	movl	%ebp, %r11d
 295b41b:      	movq	%r12, %rbp
 295b41e:      	movq	%r13, %r12
 295b421:      	addq	$0x10, %rsp
 295b425:      	testb	%al, %al
 295b427:      	je	0x295b8ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a0d>
 295b42d:      	movl	0x4(%r12), %eax
 295b432:      	testl	%eax, %eax
 295b434:      	sets	%cl
 295b437:      	cmpl	$0x1, %eax
 295b43a:      	sete	%dl
 295b43d:      	orb	%cl, %dl
 295b43f:      	jne	0x295b492 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x35b2>
 295b441:      	xorl	%ecx, %ecx
 295b443:      	cmpl	$0x4, %eax
 295b446:      	setb	%cl
 295b449:      	movq	%r8, %rsi
 295b44c:      	cmovbq	%rbp, %rsi
 295b450:      	movl	%ebx, %edx
 295b452:      	cmovbl	%r11d, %edx
 295b456:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b45b:      	subq	$0x8, %rsp
 295b45f:      	movl	$0x4, %edi
 295b464:      	movq	%rbp, %rcx
 295b467:      	movl	%r11d, %r8d
 295b46a:      	pushq	$0x1
 295b46c:      	movq	%r12, %r13
 295b46f:      	movq	%rbp, %r12
 295b472:      	movl	%r11d, %ebp
 295b475:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b47a:      	movq	%r14, %r8
 295b47d:      	movl	%ebp, %r11d
 295b480:      	movq	%r12, %rbp
 295b483:      	movq	%r13, %r12
 295b486:      	addq	$0x10, %rsp
 295b48a:      	testb	%al, %al
 295b48c:      	je	0x295b8ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a0d>
 295b492:      	movl	0x8(%r12), %eax
 295b497:      	testl	%eax, %eax
 295b499:      	sets	%cl
 295b49c:      	cmpl	$0x4, %eax
 295b49f:      	sete	%dl
 295b4a2:      	orb	%cl, %dl
 295b4a4:      	jne	0x295b4f7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3617>
 295b4a6:      	xorl	%ecx, %ecx
 295b4a8:      	cmpl	$0x4, %eax
 295b4ab:      	setb	%cl
 295b4ae:      	movq	%r8, %rsi
 295b4b1:      	cmovbq	%rbp, %rsi
 295b4b5:      	movl	%ebx, %edx
 295b4b7:      	cmovbl	%r11d, %edx
 295b4bb:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b4c0:      	subq	$0x8, %rsp
 295b4c4:      	movl	$0x4, %edi
 295b4c9:      	movq	%r8, %rcx
 295b4cc:      	movl	%ebx, %r8d
 295b4cf:      	pushq	$0x0
 295b4d1:      	movq	%r12, %r13
 295b4d4:      	movq	%rbp, %r12
 295b4d7:      	movl	%r11d, %ebp
 295b4da:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b4df:      	movq	%r14, %r8
 295b4e2:      	movl	%ebp, %r11d
 295b4e5:      	movq	%r12, %rbp
 295b4e8:      	movq	%r13, %r12
 295b4eb:      	addq	$0x10, %rsp
 295b4ef:      	testb	%al, %al
 295b4f1:      	je	0x295b8ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a0d>
 295b4f7:      	movl	0xc(%r12), %eax
 295b4fc:      	testl	%eax, %eax
 295b4fe:      	sets	%cl
 295b501:      	cmpl	$0x5, %eax
 295b504:      	sete	%dl
 295b507:      	orb	%cl, %dl
 295b509:      	jne	0x295b55c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x367c>
 295b50b:      	xorl	%ecx, %ecx
 295b50d:      	cmpl	$0x4, %eax
 295b510:      	setb	%cl
 295b513:      	movq	%r8, %rsi
 295b516:      	cmovbq	%rbp, %rsi
 295b51a:      	movl	%ebx, %edx
 295b51c:      	cmovbl	%r11d, %edx
 295b520:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b525:      	subq	$0x8, %rsp
 295b529:      	movl	$0x4, %edi
 295b52e:      	movq	%r8, %rcx
 295b531:      	movl	%ebx, %r8d
 295b534:      	pushq	$0x1
 295b536:      	movq	%r12, %r13
 295b539:      	movq	%rbp, %r12
 295b53c:      	movl	%r11d, %ebp
 295b53f:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b544:      	movq	%r14, %r8
 295b547:      	movl	%ebp, %r11d
 295b54a:      	movq	%r12, %rbp
 295b54d:      	movq	%r13, %r12
 295b550:      	addq	$0x10, %rsp
 295b554:      	testb	%al, %al
 295b556:      	je	0x295b8ed <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a0d>
 295b55c:      	movq	%rbp, 0xa0(%rsp)
 295b564:      	movl	%r11d, 0xa8(%rsp)
 295b56c:      	movq	0x3b0(%r15), %rax
 295b573:      	testq	%rax, %rax
 295b576:      	je	0x295bb52 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c72>
 295b57c:      	movl	0x8(%rax), %r9d
 295b580:      	jmp	0x295bb55 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c75>
 295b585:      	movl	0x148(%r15), %eax
 295b58c:      	cmpl	$0x7, %eax
 295b58f:      	jl	0x295b636 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3756>
 295b595:      	movq	%r14, %rdi
 295b598:      	movq	0x28(%rsp), %rsi
 295b59d:      	movl	%r8d, %ebp
 295b5a0:      	callq	0x2962840 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295b5a5:      	movl	%eax, %esi
 295b5a7:      	subq	$0x8, %rsp
 295b5ab:      	xorl	%ebx, %ebx
 295b5ad:      	movq	0x238(%rsp), %r14
 295b5b5:      	movq	%r14, %rdi
 295b5b8:      	movq	0x8(%rsp), %rdx
 295b5bd:      	movl	$0x5, %ecx
 295b5c2:      	xorl	%r8d, %r8d
 295b5c5:      	movl	$0x1, %r9d
 295b5cb:      	pushq	$0x0
 295b5cd:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b5d2:      	addq	$0x10, %rsp
 295b5d6:      	movq	%rax, 0xa0(%rsp)
 295b5de:      	movl	%edx, 0xa8(%rsp)
 295b5e5:      	movq	%r12, 0x30(%rsp)
 295b5ea:      	movl	%ebp, 0x38(%rsp)
 295b5ee:      	movq	0x3b0(%r14), %rax
 295b5f5:      	testq	%rax, %rax
 295b5f8:      	je	0x295b5fd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x371d>
 295b5fa:      	movl	0x8(%rax), %ebx
 295b5fd:      	subq	$0x20, %rsp
 295b601:      	movups	0xc0(%rsp), %xmm0
 295b609:      	movups	%xmm0, 0x10(%rsp)
 295b60e:      	movdqu	0x50(%rsp), %xmm0
 295b614:      	movdqu	%xmm0, (%rsp)
 295b619:      	movq	%r14, %rdi
 295b61c:      	movl	$0x2cb, %esi            # imm = 0x2CB
 295b621:      	movq	0x20(%rsp), %rdx
 295b626:      	movl	$0x84, %ecx
 295b62b:      	xorl	%r8d, %r8d
 295b62e:      	movl	%ebx, %r9d
 295b631:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295b636:      	cmpl	$0x1, %eax
 295b639:      	jg	0x295b82d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x394d>
 295b63f:      	cmpq	$0x4, 0x28(%rsp)
 295b645:      	movq	%r12, %r13
 295b648:      	movq	0x20(%rsp), %r15
 295b64d:      	jne	0x295b7b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38d3>
 295b653:      	movl	(%r14), %eax
 295b656:      	testl	%eax, %eax
 295b658:      	jle	0x295b697 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x37b7>
 295b65a:      	xorl	%ecx, %ecx
 295b65c:      	cmpl	$0x4, %eax
 295b65f:      	setb	%cl
 295b662:      	movq	%rbp, %rsi
 295b665:      	cmovbq	%r13, %rsi
 295b669:      	movl	%r15d, %edx
 295b66c:      	cmovbl	%r8d, %edx
 295b670:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b675:      	subq	$0x8, %rsp
 295b679:      	movl	$0x4, %edi
 295b67e:      	movq	%r13, %rcx
 295b681:      	pushq	$0x0
 295b683:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b688:      	movl	%ebx, %r8d
 295b68b:      	addq	$0x10, %rsp
 295b68f:      	testb	%al, %al
 295b691:      	je	0x295b7b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38d3>
 295b697:      	movl	0x4(%r14), %eax
 295b69b:      	testl	%eax, %eax
 295b69d:      	sets	%cl
 295b6a0:      	cmpl	$0x1, %eax
 295b6a3:      	sete	%dl
 295b6a6:      	orb	%cl, %dl
 295b6a8:      	jne	0x295b6e7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3807>
 295b6aa:      	xorl	%ecx, %ecx
 295b6ac:      	cmpl	$0x4, %eax
 295b6af:      	setb	%cl
 295b6b2:      	movq	%rbp, %rsi
 295b6b5:      	cmovbq	%r13, %rsi
 295b6b9:      	movl	%r15d, %edx
 295b6bc:      	cmovbl	%r8d, %edx
 295b6c0:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b6c5:      	subq	$0x8, %rsp
 295b6c9:      	movl	$0x4, %edi
 295b6ce:      	movq	%r13, %rcx
 295b6d1:      	pushq	$0x1
 295b6d3:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b6d8:      	movl	%ebx, %r8d
 295b6db:      	addq	$0x10, %rsp
 295b6df:      	testb	%al, %al
 295b6e1:      	je	0x295b7b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38d3>
 295b6e7:      	movl	0x8(%r14), %eax
 295b6eb:      	testl	%eax, %eax
 295b6ed:      	jle	0x295b72c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x384c>
 295b6ef:      	xorl	%ecx, %ecx
 295b6f1:      	cmpl	$0x4, %eax
 295b6f4:      	setb	%cl
 295b6f7:      	movq	%rbp, %rsi
 295b6fa:      	cmovbq	%r13, %rsi
 295b6fe:      	movl	%r15d, %edx
 295b701:      	cmovbl	%r8d, %edx
 295b705:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b70a:      	subq	$0x8, %rsp
 295b70e:      	movl	$0x4, %edi
 295b713:      	movq	%r13, %rcx
 295b716:      	pushq	$0x0
 295b718:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b71d:      	movl	%ebx, %r8d
 295b720:      	addq	$0x10, %rsp
 295b724:      	testb	%al, %al
 295b726:      	je	0x295b7b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38d3>
 295b72c:      	movl	0xc(%r14), %eax
 295b730:      	testl	%eax, %eax
 295b732:      	sets	%cl
 295b735:      	cmpl	$0x1, %eax
 295b738:      	sete	%dl
 295b73b:      	orb	%cl, %dl
 295b73d:      	jne	0x295b778 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3898>
 295b73f:      	xorl	%ecx, %ecx
 295b741:      	cmpl	$0x4, %eax
 295b744:      	setb	%cl
 295b747:      	movq	%rbp, %rsi
 295b74a:      	cmovbq	%r13, %rsi
 295b74e:      	movl	%r15d, %edx
 295b751:      	cmovbl	%r8d, %edx
 295b755:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b75a:      	subq	$0x8, %rsp
 295b75e:      	movl	$0x4, %edi
 295b763:      	movq	%r13, %rcx
 295b766:      	pushq	$0x1
 295b768:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b76d:      	movl	%ebx, %r8d
 295b770:      	addq	$0x10, %rsp
 295b774:      	testb	%al, %al
 295b776:      	je	0x295b7b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x38d3>
 295b778:      	movq	%r13, 0xa0(%rsp)
 295b780:      	movl	%r8d, 0xa8(%rsp)
 295b788:      	movq	%r13, 0x30(%rsp)
 295b78d:      	movl	%r8d, 0x38(%rsp)
 295b792:      	movq	0x230(%rsp), %rdi
 295b79a:      	movq	0x3b0(%rdi), %rax
 295b7a1:      	testq	%rax, %rax
 295b7a4:      	je	0x295bb31 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c51>
 295b7aa:      	movl	0x8(%rax), %r9d
 295b7ae:      	jmp	0x295bb34 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c54>
 295b7b3:      	movdqa	-0x1b36f5b(%rip), %xmm0 # 0xe24860 <.LCPI989_7>
 295b7bb:      	movdqa	%xmm0, 0xa0(%rsp)
 295b7c4:      	leaq	0xa0(%rsp), %rdx
 295b7cc:      	movl	$0x4, %ecx
 295b7d1:      	movq	%r14, %rdi
 295b7d4:      	movq	0x28(%rsp), %rsi
 295b7d9:      	movl	%r8d, %r9d
 295b7dc:      	movq	%r13, %r8
 295b7df:      	pushq	%r15
 295b7e1:      	pushq	%rbp
 295b7e2:      	callq	0x2961a40 <_ZL19isShuffleEquivalentN4llvm8ArrayRefIiEES1_NS_7SDValueES2_>
 295b7e7:      	movl	%ebx, %r8d
 295b7ea:      	addq	$0x10, %rsp
 295b7ee:      	testb	%al, %al
 295b7f0:      	je	0x295b82d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x394d>
 295b7f2:      	movq	%r12, 0xa0(%rsp)
 295b7fa:      	movl	%r8d, 0xa8(%rsp)
 295b802:      	movq	%r12, 0x30(%rsp)
 295b807:      	movl	%r8d, 0x38(%rsp)
 295b80c:      	movq	0x230(%rsp), %rdi
 295b814:      	movq	0x3b0(%rdi), %rax
 295b81b:      	testq	%rax, %rax
 295b81e:      	je	0x295baae <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bce>
 295b824:      	movl	0x8(%rax), %r9d
 295b828:      	jmp	0x295bab1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bd1>
 295b82d:      	movq	%r14, %rdi
 295b830:      	movq	0x28(%rsp), %rsi
 295b835:      	movl	%r8d, %ebp
 295b838:      	callq	0x2962840 <_ZL18getV4X86ShuffleImmN4llvm8ArrayRefIiEE>
 295b83d:      	movl	%eax, %esi
 295b83f:      	subq	$0x8, %rsp
 295b843:      	xorl	%ebx, %ebx
 295b845:      	movq	0x238(%rsp), %r14
 295b84d:      	movq	%r14, %rdi
 295b850:      	movq	0x8(%rsp), %rdx
 295b855:      	movl	$0x5, %ecx
 295b85a:      	xorl	%r8d, %r8d
 295b85d:      	movl	$0x1, %r9d
 295b863:      	pushq	$0x0
 295b865:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295b86a:      	addq	$0x10, %rsp
 295b86e:      	movq	%rax, 0xa0(%rsp)
 295b876:      	movl	%edx, 0xa8(%rsp)
 295b87d:      	movq	%r12, 0x30(%rsp)
 295b882:      	movl	%ebp, 0x38(%rsp)
 295b886:      	movq	%r12, 0x70(%rsp)
 295b88b:      	movl	%ebp, 0x78(%rsp)
 295b88f:      	movq	0x3b0(%r14), %rax
 295b896:      	testq	%rax, %rax
 295b899:      	je	0x295b89e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x39be>
 295b89b:      	movl	0x8(%rax), %ebx
 295b89e:      	subq	$0x30, %rsp
 295b8a2:      	movups	0xd0(%rsp), %xmm0
 295b8aa:      	movups	%xmm0, 0x20(%rsp)
 295b8af:      	movups	0x60(%rsp), %xmm0
 295b8b4:      	movups	%xmm0, 0x10(%rsp)
 295b8b9:      	movdqu	0xa0(%rsp), %xmm0
 295b8c2:      	movdqu	%xmm0, (%rsp)
 295b8c7:      	movq	%r14, %rdi
 295b8ca:      	movl	$0x2bc, %esi            # imm = 0x2BC
 295b8cf:      	movq	0x30(%rsp), %rdx
 295b8d4:      	movl	$0x84, %ecx
 295b8d9:      	xorl	%r8d, %r8d
 295b8dc:      	movl	%ebx, %r9d
 295b8df:      	callq	0x5e2ac90 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295b8e4:      	addq	$0x30, %rsp
 295b8e8:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295b8ed:      	movl	(%r12), %eax
 295b8f1:      	testl	%eax, %eax
 295b8f3:      	sets	%cl
 295b8f6:      	cmpl	$0x2, %eax
 295b8f9:      	sete	%dl
 295b8fc:      	orb	%cl, %dl
 295b8fe:      	jne	0x295b951 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3a71>
 295b900:      	xorl	%ecx, %ecx
 295b902:      	cmpl	$0x4, %eax
 295b905:      	setb	%cl
 295b908:      	movq	%r8, %rsi
 295b90b:      	cmovbq	%rbp, %rsi
 295b90f:      	movl	%ebx, %edx
 295b911:      	cmovbl	%r11d, %edx
 295b915:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b91a:      	subq	$0x8, %rsp
 295b91e:      	movl	$0x4, %edi
 295b923:      	movq	%rbp, %rcx
 295b926:      	movl	%r11d, %r8d
 295b929:      	pushq	$0x2
 295b92b:      	movq	%r12, %r13
 295b92e:      	movq	%rbp, %r12
 295b931:      	movl	%r11d, %ebp
 295b934:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b939:      	movq	%r14, %r8
 295b93c:      	movl	%ebp, %r11d
 295b93f:      	movq	%r12, %rbp
 295b942:      	movq	%r13, %r12
 295b945:      	addq	$0x10, %rsp
 295b949:      	testb	%al, %al
 295b94b:      	je	0x295bad7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bf7>
 295b951:      	movl	0x4(%r12), %eax
 295b956:      	testl	%eax, %eax
 295b958:      	sets	%cl
 295b95b:      	cmpl	$0x3, %eax
 295b95e:      	sete	%dl
 295b961:      	orb	%cl, %dl
 295b963:      	jne	0x295b9b6 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ad6>
 295b965:      	xorl	%ecx, %ecx
 295b967:      	cmpl	$0x4, %eax
 295b96a:      	setb	%cl
 295b96d:      	movq	%r8, %rsi
 295b970:      	cmovbq	%rbp, %rsi
 295b974:      	movl	%ebx, %edx
 295b976:      	cmovbl	%r11d, %edx
 295b97a:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b97f:      	subq	$0x8, %rsp
 295b983:      	movl	$0x4, %edi
 295b988:      	movq	%rbp, %rcx
 295b98b:      	movl	%r11d, %r8d
 295b98e:      	pushq	$0x3
 295b990:      	movq	%r12, %r13
 295b993:      	movq	%rbp, %r12
 295b996:      	movl	%r11d, %ebp
 295b999:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295b99e:      	movq	%r14, %r8
 295b9a1:      	movl	%ebp, %r11d
 295b9a4:      	movq	%r12, %rbp
 295b9a7:      	movq	%r13, %r12
 295b9aa:      	addq	$0x10, %rsp
 295b9ae:      	testb	%al, %al
 295b9b0:      	je	0x295bad7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bf7>
 295b9b6:      	movl	0x8(%r12), %eax
 295b9bb:      	testl	%eax, %eax
 295b9bd:      	sets	%cl
 295b9c0:      	cmpl	$0x6, %eax
 295b9c3:      	sete	%dl
 295b9c6:      	orb	%cl, %dl
 295b9c8:      	jne	0x295ba1b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3b3b>
 295b9ca:      	xorl	%ecx, %ecx
 295b9cc:      	cmpl	$0x4, %eax
 295b9cf:      	setb	%cl
 295b9d2:      	movq	%r8, %rsi
 295b9d5:      	cmovbq	%rbp, %rsi
 295b9d9:      	movl	%ebx, %edx
 295b9db:      	cmovbl	%r11d, %edx
 295b9df:      	leal	-0x4(%rax,%rcx,4), %r9d
 295b9e4:      	subq	$0x8, %rsp
 295b9e8:      	movl	$0x4, %edi
 295b9ed:      	movq	%r8, %rcx
 295b9f0:      	movl	%ebx, %r8d
 295b9f3:      	pushq	$0x2
 295b9f5:      	movq	%r12, %r13
 295b9f8:      	movq	%rbp, %r12
 295b9fb:      	movl	%r11d, %ebp
 295b9fe:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ba03:      	movq	%r14, %r8
 295ba06:      	movl	%ebp, %r11d
 295ba09:      	movq	%r12, %rbp
 295ba0c:      	movq	%r13, %r12
 295ba0f:      	addq	$0x10, %rsp
 295ba13:      	testb	%al, %al
 295ba15:      	je	0x295bad7 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bf7>
 295ba1b:      	movl	0xc(%r12), %eax
 295ba20:      	testl	%eax, %eax
 295ba22:      	sets	%cl
 295ba25:      	cmpl	$0x7, %eax
 295ba28:      	sete	%dl
 295ba2b:      	orb	%cl, %dl
 295ba2d:      	jne	0x295ba85 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ba5>
 295ba2f:      	xorl	%ecx, %ecx
 295ba31:      	cmpl	$0x4, %eax
 295ba34:      	setb	%cl
 295ba37:      	movq	%r8, %rsi
 295ba3a:      	cmovbq	%rbp, %rsi
 295ba3e:      	movl	%ebx, %edx
 295ba40:      	cmovbl	%r11d, %edx
 295ba44:      	leal	-0x4(%rax,%rcx,4), %r9d
 295ba49:      	subq	$0x8, %rsp
 295ba4d:      	movl	$0x4, %edi
 295ba52:      	movq	%r8, %rcx
 295ba55:      	movl	%ebx, %r8d
 295ba58:      	pushq	$0x3
 295ba5a:      	movq	%r12, %r13
 295ba5d:      	movq	%rbp, %r12
 295ba60:      	movl	%r11d, %ebp
 295ba63:      	callq	0x2961b10 <_ZL19IsElementEquivalentiN4llvm7SDValueES0_ii>
 295ba68:      	movq	%r14, %r8
 295ba6b:      	movl	%ebp, %r11d
 295ba6e:      	movq	%r12, %rbp
 295ba71:      	movq	%r13, %r12
 295ba74:      	movq	0x10(%rsp), %rdi
 295ba79:      	addq	$0x10, %rsp
 295ba7d:      	testb	%al, %al
 295ba7f:      	je	0x295a9fd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b1d>
 295ba85:      	movq	%rbp, 0xa0(%rsp)
 295ba8d:      	movl	%r11d, 0xa8(%rsp)
 295ba95:      	movq	0x3b0(%r15), %rax
 295ba9c:      	testq	%rax, %rax
 295ba9f:      	je	0x295bce0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e00>
 295baa5:      	movl	0x8(%rax), %r9d
 295baa9:      	jmp	0x295bce3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3e03>
 295baae:      	xorl	%r9d, %r9d
 295bab1:      	subq	$0x20, %rsp
 295bab5:      	movups	0xc0(%rsp), %xmm0
 295babd:      	movups	%xmm0, 0x10(%rsp)
 295bac2:      	movdqu	0x50(%rsp), %xmm0
 295bac8:      	movdqu	%xmm0, (%rsp)
 295bacd:      	movl	$0x2c4, %esi            # imm = 0x2C4
 295bad2:      	jmp	0x295bb7f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c9f>
 295bad7:      	movq	(%rsp), %rdi
 295badb:      	jmp	0x295a9fd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x2b1d>
 295bae0:      	xorl	%r9d, %r9d
 295bae3:      	subq	$0x10, %rsp
 295bae7:      	movdqu	0xb0(%rsp), %xmm0
 295baf0:      	movdqu	%xmm0, (%rsp)
 295baf5:      	movl	$0x2c2, %esi            # imm = 0x2C2
 295bafa:      	jmp	0x295bb16 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c36>
 295bafc:      	xorl	%r9d, %r9d
 295baff:      	subq	$0x10, %rsp
 295bb03:      	movdqu	0xb0(%rsp), %xmm0
 295bb0c:      	movdqu	%xmm0, (%rsp)
 295bb11:      	movl	$0x2c1, %esi            # imm = 0x2C1
 295bb16:      	movq	0x10(%rsp), %rdx
 295bb1b:      	movl	$0x84, %ecx
 295bb20:      	xorl	%r8d, %r8d
 295bb23:      	callq	0x5e1efc0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueENS_11SDNodeFlagsE>
 295bb28:      	addq	$0x10, %rsp
 295bb2c:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bb31:      	xorl	%r9d, %r9d
 295bb34:      	subq	$0x20, %rsp
 295bb38:      	movups	0xc0(%rsp), %xmm0
 295bb40:      	movups	%xmm0, 0x10(%rsp)
 295bb45:      	movdqu	0x50(%rsp), %xmm0
 295bb4b:      	movdqu	%xmm0, (%rsp)
 295bb50:      	jmp	0x295bb7a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3c9a>
 295bb52:      	xorl	%r9d, %r9d
 295bb55:      	subq	$0x20, %rsp
 295bb59:      	leaq	0x230(%rsp), %rax
 295bb61:      	movups	(%rax), %xmm0
 295bb64:      	movups	%xmm0, 0x10(%rsp)
 295bb69:      	movdqu	0xc0(%rsp), %xmm0
 295bb72:      	movdqu	%xmm0, (%rsp)
 295bb77:      	movq	%r15, %rdi
 295bb7a:      	movl	$0x2c3, %esi            # imm = 0x2C3
 295bb7f:      	movq	0x20(%rsp), %rdx
 295bb84:      	movl	$0x84, %ecx
 295bb89:      	xorl	%r8d, %r8d
 295bb8c:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295bb91:      	movq	%rdi, %r13
 295bb94:      	movl	$0x30, %esi
 295bb99:      	movq	%rbp, %rdx
 295bb9c:      	movq	0x230(%rsp), %r15
 295bba4:      	pushq	%r15
 295bba6:      	pushq	%r14
 295bba8:      	pushq	%rbx
 295bba9:      	pushq	%r12
 295bbab:      	movq	%rbx, %r15
 295bbae:      	movq	%r12, %rbx
 295bbb1:      	movl	%ecx, %r12d
 295bbb4:      	callq	0x2954260 <_ZL23lowerShuffleAsBroadcastRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295bbb9:      	addq	$0x20, %rsp
 295bbbd:      	testq	%rax, %rax
 295bbc0:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bbc6:      	movl	0x148(%r14), %eax
 295bbcd:      	movzbl	0x1db(%r14), %r10d
 295bbd5:      	subq	$0x8, %rsp
 295bbd9:      	movq	%r13, %rdi
 295bbdc:      	movl	$0x30, %esi
 295bbe1:      	movq	%rbp, %r13
 295bbe4:      	movq	%rbp, %rdx
 295bbe7:      	movl	%r12d, %ecx
 295bbea:      	movq	%rbx, %r12
 295bbed:      	movq	%rbx, %r8
 295bbf0:      	movq	%r15, %rbx
 295bbf3:      	movq	%r15, %r9
 295bbf6:      	pushq	0x238(%rsp)
 295bbfd:      	pushq	%r10
 295bbff:      	pushq	%rax
 295bc00:      	callq	0x296ff60 <_ZL23lowerShuffleAsBitRotateRKN4llvm5SDLocENS_3MVTENS_7SDValueENS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295bc05:      	addq	$0x20, %rsp
 295bc09:      	testq	%rax, %rax
 295bc0c:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bc12:      	subq	$0x8, %rsp
 295bc16:      	movq	0x8(%rsp), %rdi
 295bc1b:      	movl	$0x30, %esi
 295bc20:      	movq	%r13, %rdx
 295bc23:      	movl	0x14(%rsp), %ecx
 295bc27:      	movq	0x20(%rsp), %r8
 295bc2c:      	movl	0x28(%rsp), %r9d
 295bc31:      	pushq	0x238(%rsp)
 295bc38:      	pushq	%rbx
 295bc39:      	pushq	%r12
 295bc3b:      	callq	0x29651f0 <_ZL21lowerShuffleWithUNPCKRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295bc40:      	addq	$0x20, %rsp
 295bc44:      	testq	%rax, %rax
 295bc47:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bc4d:      	leaq	0x30(%rsp), %rax
 295bc52:      	movq	%rax, 0xa0(%rsp)
 295bc5a:      	leaq	0x130(%rsp), %rax
 295bc62:      	movq	%rax, 0xa8(%rsp)
 295bc6a:      	leaq	0x60(%rsp), %rax
 295bc6f:      	movq	%rax, 0xb0(%rsp)
 295bc77:      	movq	0x230(%rsp), %rax
 295bc7f:      	movq	%rax, 0xb8(%rsp)
 295bc87:      	movq	(%rsp), %rax
 295bc8b:      	movq	%rax, 0xc0(%rsp)
 295bc93:      	leaq	0xa0(%rsp), %rdi
 295bc9b:      	callq	0x2986570 <_ZZL17lowerV16I8ShuffleRKN4llvm5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueES8_RKNS_12X86SubtargetERNS_12SelectionDAGEENK3$_1clEv>
 295bca0:      	testq	%rax, %rax
 295bca3:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bca9:      	movq	0x60(%rsp), %rbp
 295bcae:      	movl	0x68(%rsp), %ecx
 295bcb2:      	movq	0x130(%rsp), %r12
 295bcba:      	movq	0x138(%rsp), %rbx
 295bcc2:      	xorl	%r15d, %r15d
 295bcc5:      	movq	(%rsp), %rdi
 295bcc9:      	movq	0x228(%rsp), %r14
 295bcd1:      	movl	0x20(%rsp), %r9d
 295bcd6:      	movq	0x18(%rsp), %r8
 295bcdb:      	jmp	0x29589f8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0xb18>
 295bce0:      	xorl	%r9d, %r9d
 295bce3:      	subq	$0x20, %rsp
 295bce7:      	movups	0xc0(%rsp), %xmm0
 295bcef:      	movups	%xmm0, 0x10(%rsp)
 295bcf4:      	leaq	0x230(%rsp), %rax
 295bcfc:      	movdqu	(%rax), %xmm0
 295bd00:      	movdqu	%xmm0, (%rsp)
 295bd05:      	movq	%r15, %rdi
 295bd08:      	jmp	0x295bacd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3bed>
 295bd0d:      	movq	0x230(%rsp), %r13
 295bd15:      	movq	%r13, %rdi
 295bd18:      	movl	$0x96, %esi
 295bd1d:      	xorl	%edx, %edx
 295bd1f:      	movq	%r12, %rcx
 295bd22:      	movl	%ebp, %r8d
 295bd25:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bd2a:      	movq	%rbx, %r12
 295bd2d:      	movq	%rax, %rbx
 295bd30:      	movl	%edx, %r14d
 295bd33:      	movq	%r13, %rdi
 295bd36:      	movl	$0x96, %esi
 295bd3b:      	xorl	%edx, %edx
 295bd3d:      	movq	%r15, %rcx
 295bd40:      	movl	0x18(%rsp), %r8d
 295bd45:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bd4a:      	movq	%rax, 0x80(%rsp)
 295bd52:      	movl	%edx, 0x88(%rsp)
 295bd59:      	movq	0x58(%rsp), %rax
 295bd5e:      	movq	%rax, 0xa0(%rsp)
 295bd66:      	movq	%r12, 0xa8(%rsp)
 295bd6e:      	subq	$0x20, %rsp
 295bd72:      	movups	0xc0(%rsp), %xmm0
 295bd7a:      	movups	%xmm0, 0x10(%rsp)
 295bd7f:      	movdqa	0xa0(%rsp), %xmm0
 295bd88:      	movdqu	%xmm0, (%rsp)
 295bd8d:      	movq	%r13, %rdi
 295bd90:      	movl	$0x96, %esi
 295bd95:      	xorl	%edx, %edx
 295bd97:      	movq	0x20(%rsp), %rcx
 295bd9c:      	movq	%rbx, %r8
 295bd9f:      	movl	%r14d, %r9d
 295bda2:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295bda7:      	addq	$0x20, %rsp
 295bdab:      	movl	%edx, %r8d
 295bdae:      	movq	%r13, %rdi
 295bdb1:      	movl	$0x5e, %esi
 295bdb6:      	xorl	%edx, %edx
 295bdb8:      	movq	%rax, %rcx
 295bdbb:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295bdc0:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bdc5:      	cmpl	$0x5, 0x9c(%rsp)
 295bdcd:      	jl	0x295be3d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3f5d>
 295bdcf:      	movq	0x58(%rsp), %rax
 295bdd4:      	movq	%rax, 0xa0(%rsp)
 295bddc:      	movq	0x28(%rsp), %rax
 295bde1:      	movq	%rax, 0xa8(%rsp)
 295bde9:      	subq	$0x30, %rsp
 295bded:      	movdqu	0xd0(%rsp), %xmm0
 295bdf6:      	movdqu	%xmm0, (%rsp)
 295bdfb:      	movq	%r12, 0x20(%rsp)
 295be00:      	movq	%r14, 0x18(%rsp)
 295be05:      	movq	0x250(%rsp), %rax
 295be0d:      	movq	%rax, 0x10(%rsp)
 295be12:      	movq	0x30(%rsp), %rdi
 295be17:      	movl	$0x49, %esi
 295be1c:      	movq	0x40(%rsp), %rdx
 295be21:      	movl	0x3c(%rsp), %ecx
 295be25:      	movq	0x50(%rsp), %r8
 295be2a:      	movq	0x48(%rsp), %r9
 295be2f:      	callq	0x2966760 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295be34:      	addq	$0x30, %rsp
 295be38:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295be3d:      	subq	$0x8, %rsp
 295be41:      	movq	0x8(%rsp), %rdi
 295be46:      	movl	$0x49, %esi
 295be4b:      	movq	0x18(%rsp), %rdx
 295be50:      	movl	0x14(%rsp), %ecx
 295be54:      	movq	0x28(%rsp), %r8
 295be59:      	movq	0x20(%rsp), %r9
 295be5e:      	pushq	%r12
 295be60:      	pushq	0x38(%rsp)
 295be64:      	movq	0x70(%rsp), %r15
 295be69:      	pushq	%r15
 295be6b:      	callq	0x296b390 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295be70:      	addq	$0x20, %rsp
 295be74:      	testq	%rax, %rax
 295be77:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295be7d:      	jmp	0x2959f3a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x205a>
 295be82:      	cmpl	$0x1, %r15d
 295be86:      	jne	0x295bee1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4001>
 295be88:      	movq	0x60(%rsp), %rdx
 295be8d:      	movl	0x68(%rsp), %ecx
 295be91:      	movq	0x220(%rsp), %r10
 295be99:      	movl	0x8(%r10), %eax
 295be9d:      	movq	(%rsp), %rdi
 295bea1:      	movl	$0x30, %esi
 295bea6:      	movq	0x18(%rsp), %r8
 295beab:      	movl	0x20(%rsp), %r9d
 295beb0:      	pushq	0x230(%rsp)
 295beb7:      	pushq	%rbp
 295beb8:      	pushq	%rax
 295beb9:      	pushq	(%r10)
 295bebc:      	pushq	%r14
 295bebe:      	pushq	%rbx
 295bebf:      	callq	0x2963370 <_ZL30lowerShuffleAsElementInsertionRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295bec4:      	addq	$0x30, %rsp
 295bec8:      	testq	%rax, %rax
 295becb:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bed1:      	movq	0x130(%rsp), %rbx
 295bed9:      	movq	0x138(%rsp), %r14
 295bee1:      	movq	0x60(%rsp), %rdx
 295bee6:      	movl	0x68(%rsp), %ecx
 295beea:      	subq	$0x8, %rsp
 295beee:      	movq	0x8(%rsp), %rdi
 295bef3:      	movl	$0x30, %esi
 295bef8:      	movq	0x20(%rsp), %r8
 295befd:      	movl	0x28(%rsp), %r9d
 295bf02:      	pushq	0x238(%rsp)
 295bf09:      	pushq	%r14
 295bf0b:      	pushq	%rbx
 295bf0c:      	callq	0x296a5b0 <_ZL22lowerShuffleAsBitBlendRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERNS_12SelectionDAGE>
 295bf11:      	addq	$0x20, %rsp
 295bf15:      	testq	%rax, %rax
 295bf18:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295bf1e:      	testl	%r13d, %r13d
 295bf21:      	je	0x295c457 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4577>
 295bf27:      	subq	$0x8, %rsp
 295bf2b:      	xorl	%ebx, %ebx
 295bf2d:      	movq	0x238(%rsp), %rdi
 295bf35:      	xorl	%esi, %esi
 295bf37:      	movq	0x8(%rsp), %rdx
 295bf3c:      	movl	$0x6, %ecx
 295bf41:      	xorl	%r8d, %r8d
 295bf44:      	xorl	%r9d, %r9d
 295bf47:      	pushq	$0x0
 295bf49:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295bf4e:      	addq	$0x10, %rsp
 295bf52:      	leaq	0xb0(%rsp), %rcx
 295bf5a:      	movq	%rcx, 0xa0(%rsp)
 295bf62:      	movl	$0x8, 0xac(%rsp)
 295bf6d:      	movq	%rax, 0xb0(%rsp)
 295bf75:      	movl	%edx, 0xb8(%rsp)
 295bf7c:      	movq	%rax, 0xc0(%rsp)
 295bf84:      	movl	%edx, 0xc8(%rsp)
 295bf8b:      	movq	%rax, 0xd0(%rsp)
 295bf93:      	movl	%edx, 0xd8(%rsp)
 295bf9a:      	movq	%rax, 0xe0(%rsp)
 295bfa2:      	movl	%edx, 0xe8(%rsp)
 295bfa9:      	movq	%rax, 0xf0(%rsp)
 295bfb1:      	movl	%edx, 0xf8(%rsp)
 295bfb8:      	movq	%rax, 0x100(%rsp)
 295bfc0:      	movl	%edx, 0x108(%rsp)
 295bfc7:      	movq	%rax, 0x110(%rsp)
 295bfcf:      	movl	%edx, 0x118(%rsp)
 295bfd6:      	movq	%rax, 0x120(%rsp)
 295bfde:      	movl	%edx, 0x128(%rsp)
 295bfe5:      	movl	$0x8, 0xa8(%rsp)
 295bff0:      	leal	-0x1(%r13), %ecx
 295bff4:      	movl	$0x1, %ebp
 295bff9:      	shll	%cl, %ebp
 295bffb:      	subq	$0x8, %rsp
 295bfff:      	movl	$0xff, %esi
 295c004:      	movq	0x238(%rsp), %rdi
 295c00c:      	movq	0x8(%rsp), %rdx
 295c011:      	movl	$0x6, %ecx
 295c016:      	xorl	%r8d, %r8d
 295c019:      	xorl	%r9d, %r9d
 295c01c:      	pushq	$0x0
 295c01e:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c023:      	addq	$0x10, %rsp
 295c027:      	movl	%ebx, %esi
 295c029:      	movq	0xa0(%rsp), %rcx
 295c031:      	shlq	$0x4, %rsi
 295c035:      	movq	%rax, (%rcx,%rsi)
 295c039:      	movl	%edx, 0x8(%rcx,%rsi)
 295c03d:      	addl	%ebp, %ebx
 295c03f:      	cmpl	$0x8, %ebx
 295c042:      	jne	0x295bffb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x411b>
 295c044:      	movl	0xa8(%rsp), %eax
 295c04b:      	movq	%rcx, 0x30(%rsp)
 295c050:      	movq	%rax, 0x38(%rsp)
 295c055:      	movq	0x230(%rsp), %rax
 295c05d:      	movq	0x3b0(%rax), %rax
 295c064:      	xorl	%r14d, %r14d
 295c067:      	movl	$0x0, %r9d
 295c06d:      	testq	%rax, %rax
 295c070:      	je	0x295c076 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4196>
 295c072:      	movl	0x8(%rax), %r9d
 295c076:      	subq	$0x10, %rsp
 295c07a:      	movups	0x40(%rsp), %xmm0
 295c07f:      	movups	%xmm0, (%rsp)
 295c083:      	movq	0x240(%rsp), %r15
 295c08b:      	movq	%r15, %rdi
 295c08e:      	movl	$0xa0, %esi
 295c093:      	movq	0x10(%rsp), %rdx
 295c098:      	movl	$0x3e, %ecx
 295c09d:      	xorl	%r8d, %r8d
 295c0a0:      	callq	0x5e264a0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_8ArrayRefINS_7SDValueEEENS_11SDNodeFlagsE>
 295c0a5:      	addq	$0x10, %rsp
 295c0a9:      	movq	%rax, %rbx
 295c0ac:      	movl	%edx, %ebp
 295c0ae:      	movq	0x60(%rsp), %rcx
 295c0b3:      	movl	0x68(%rsp), %r8d
 295c0b8:      	movq	%r15, %rdi
 295c0bb:      	movl	$0x3e, %esi
 295c0c0:      	xorl	%edx, %edx
 295c0c2:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c0c7:      	movq	%rbx, 0x30(%rsp)
 295c0cc:      	movl	%ebp, 0x38(%rsp)
 295c0d0:      	movq	%rax, 0x70(%rsp)
 295c0d5:      	movl	%edx, 0x78(%rsp)
 295c0d9:      	movq	0x3b0(%r15), %rax
 295c0e0:      	testq	%rax, %rax
 295c0e3:      	je	0x295c0e9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4209>
 295c0e5:      	movl	0x8(%rax), %r14d
 295c0e9:      	subq	$0x20, %rsp
 295c0ed:      	movups	0x50(%rsp), %xmm0
 295c0f2:      	movups	%xmm0, 0x10(%rsp)
 295c0f7:      	movups	0x90(%rsp), %xmm0
 295c0ff:      	movups	%xmm0, (%rsp)
 295c103:      	xorl	%r12d, %r12d
 295c106:      	movq	0x250(%rsp), %rdi
 295c10e:      	movl	$0xbf, %esi
 295c113:      	movq	0x20(%rsp), %rdx
 295c118:      	movl	$0x3e, %ecx
 295c11d:      	xorl	%r8d, %r8d
 295c120:      	movl	%r14d, %r9d
 295c123:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c128:      	addq	$0x20, %rsp
 295c12c:      	movq	%rax, 0x60(%rsp)
 295c131:      	movl	%edx, 0x68(%rsp)
 295c135:      	cmpl	$0x2, 0x10(%rsp)
 295c13a:      	jae	0x295c55f <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x467f>
 295c140:      	leaq	0x60(%rsp), %rax
 295c145:      	jmp	0x295c5f9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4719>
 295c14a:      	cmpb	$0x0, 0x1d1(%r13)
 295c152:      	je	0x295c758 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4878>
 295c158:      	movq	$0x0, 0x160(%rsp)
 295c164:      	movq	%r15, %rdi
 295c167:      	movq	0x28(%rsp), %rsi
 295c16c:      	xorl	%edx, %edx
 295c16e:      	xorl	%ecx, %ecx
 295c170:      	callq	0x29754b0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 295c175:      	cmpl	$0x1, %eax
 295c178:      	jne	0x295c3b1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x44d1>
 295c17e:      	movl	0x148(%r13), %r15d
 295c185:      	xorl	%ebx, %ebx
 295c187:      	cmpl	$0x5, %r15d
 295c18b:      	setge	%bl
 295c18e:      	xorl	$0x293, %ebx            # imm = 0x293
 295c194:      	movq	0x230(%rsp), %r12
 295c19c:      	movq	%r12, %rdi
 295c19f:      	movl	$0x49, %esi
 295c1a4:      	xorl	%edx, %edx
 295c1a6:      	movq	0x10(%rsp), %rcx
 295c1ab:      	movl	0xc(%rsp), %r8d
 295c1b0:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c1b5:      	movq	%rax, %r14
 295c1b8:      	movl	%edx, %ebp
 295c1ba:      	subq	$0x8, %rsp
 295c1be:      	movl	$0x10, %esi
 295c1c3:      	movq	%r12, %rdi
 295c1c6:      	movq	0x8(%rsp), %rdx
 295c1cb:      	movl	$0x5, %ecx
 295c1d0:      	xorl	%r8d, %r8d
 295c1d3:      	movl	$0x1, %r9d
 295c1d9:      	pushq	$0x0
 295c1db:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c1e0:      	addq	$0x10, %rsp
 295c1e4:      	movq	%rax, 0xa0(%rsp)
 295c1ec:      	movl	%edx, 0xa8(%rsp)
 295c1f3:      	movq	%r14, 0x30(%rsp)
 295c1f8:      	movl	%ebp, 0x38(%rsp)
 295c1fc:      	movq	0x3b0(%r12), %rax
 295c204:      	testq	%rax, %rax
 295c207:      	je	0x295c214 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4334>
 295c209:      	movl	0x8(%rax), %eax
 295c20c:      	movq	%rax, 0x160(%rsp)
 295c214:      	subq	$0x20, %rsp
 295c218:      	movups	0xc0(%rsp), %xmm0
 295c220:      	movups	%xmm0, 0x10(%rsp)
 295c225:      	movups	0x50(%rsp), %xmm0
 295c22a:      	movups	%xmm0, (%rsp)
 295c22e:      	movq	$0x0, 0x30(%rsp)
 295c237:      	movq	0x250(%rsp), %r14
 295c23f:      	movq	%r14, %rdi
 295c242:      	movl	%ebx, %esi
 295c244:      	movq	0x20(%rsp), %rbp
 295c249:      	movq	%rbp, %rdx
 295c24c:      	movl	$0x49, %ecx
 295c251:      	xorl	%r8d, %r8d
 295c254:      	movq	0x180(%rsp), %r9
 295c25c:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c261:      	addq	$0x20, %rsp
 295c265:      	movq	%rax, 0x28(%rsp)
 295c26a:      	movl	%edx, 0xc(%rsp)
 295c26e:      	movq	%r14, %rdi
 295c271:      	movl	$0x49, %esi
 295c276:      	xorl	%edx, %edx
 295c278:      	movq	0x20(%rsp), %rcx
 295c27d:      	movl	0x58(%rsp), %r8d
 295c282:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c287:      	movq	%rax, %r12
 295c28a:      	movl	%edx, %r13d
 295c28d:      	subq	$0x8, %rsp
 295c291:      	movl	$0x10, %esi
 295c296:      	movq	%r14, %rdi
 295c299:      	movq	%rbp, %rdx
 295c29c:      	movl	$0x5, %ecx
 295c2a1:      	xorl	%r8d, %r8d
 295c2a4:      	movl	$0x1, %r9d
 295c2aa:      	pushq	$0x0
 295c2ac:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c2b1:      	addq	$0x10, %rsp
 295c2b5:      	movq	%rax, 0xa0(%rsp)
 295c2bd:      	movl	%edx, 0xa8(%rsp)
 295c2c4:      	movq	%r12, 0x30(%rsp)
 295c2c9:      	movl	%r13d, 0x38(%rsp)
 295c2ce:      	movq	0x3b0(%r14), %rax
 295c2d5:      	movl	$0x0, %r9d
 295c2db:      	testq	%rax, %rax
 295c2de:      	je	0x295c2e4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4404>
 295c2e0:      	movl	0x8(%rax), %r9d
 295c2e4:      	xorl	%r12d, %r12d
 295c2e7:      	cmpl	$0x5, %r15d
 295c2eb:      	setge	%r12b
 295c2ef:      	subq	$0x20, %rsp
 295c2f3:      	movups	0xc0(%rsp), %xmm0
 295c2fb:      	movups	%xmm0, 0x10(%rsp)
 295c300:      	movups	0x50(%rsp), %xmm0
 295c305:      	movups	%xmm0, (%rsp)
 295c309:      	movq	0x250(%rsp), %r14
 295c311:      	movq	%r14, %rdi
 295c314:      	movl	%ebx, %esi
 295c316:      	movq	0x20(%rsp), %rdx
 295c31b:      	movl	$0x49, %ecx
 295c320:      	xorl	%r8d, %r8d
 295c323:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c328:      	addq	$0x20, %rsp
 295c32c:      	addl	$0x2b5, %r12d           # imm = 0x2B5
 295c333:      	movq	%rax, 0xa0(%rsp)
 295c33b:      	movl	%edx, 0xa8(%rsp)
 295c342:      	movl	0x18(%rsp), %eax
 295c346:      	movl	%eax, 0xac(%rsp)
 295c34d:      	movq	0x28(%rsp), %rax
 295c352:      	movq	%rax, 0x30(%rsp)
 295c357:      	movl	0xc(%rsp), %eax
 295c35b:      	movl	%eax, 0x38(%rsp)
 295c35f:      	movq	0x3b0(%r14), %rax
 295c366:      	testq	%rax, %rax
 295c369:      	je	0x295c373 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4493>
 295c36b:      	movl	0x8(%rax), %eax
 295c36e:      	movq	%rax, 0x10(%rsp)
 295c373:      	subq	$0x20, %rsp
 295c377:      	movups	0xc0(%rsp), %xmm0
 295c37f:      	movups	%xmm0, 0x10(%rsp)
 295c384:      	movdqu	0x50(%rsp), %xmm0
 295c38a:      	movdqu	%xmm0, (%rsp)
 295c38f:      	movq	0x250(%rsp), %rdi
 295c397:      	movl	%r12d, %esi
 295c39a:      	movq	0x20(%rsp), %rdx
 295c39f:      	movl	$0x3e, %ecx
 295c3a4:      	xorl	%r8d, %r8d
 295c3a7:      	movq	0x30(%rsp), %r9
 295c3ac:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295c3b1:      	subq	$0x8, %rsp
 295c3b5:      	movq	0x8(%rsp), %rdi
 295c3ba:      	movl	$0x3e, %esi
 295c3bf:      	movq	0x18(%rsp), %rdx
 295c3c4:      	movl	0x14(%rsp), %ecx
 295c3c8:      	movq	0x28(%rsp), %r8
 295c3cd:      	movl	0x60(%rsp), %r9d
 295c3d2:      	pushq	0x238(%rsp)
 295c3d9:      	pushq	0x38(%rsp)
 295c3dd:      	pushq	%r15
 295c3df:      	callq	0x296b390 <_ZL30lowerShuffleAsPermuteAndUnpackRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295c3e4:      	addq	$0x20, %rsp
 295c3e8:      	testq	%rax, %rax
 295c3eb:      	jne	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295c3f1:      	cmpl	$0x4, 0x9c(%rsp)
 295c3f9:      	jg	0x295cfa9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x50c9>
 295c3ff:      	cmpl	$0x4, 0x148(%r13)
 295c407:      	jl	0x295cfa9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x50c9>
 295c40d:      	leaq	0x30(%rsp), %rax
 295c412:      	leaq	0xa0(%rsp), %r10
 295c41a:      	movq	(%rsp), %rdi
 295c41e:      	movl	$0x3e, %esi
 295c423:      	movq	0x10(%rsp), %rdx
 295c428:      	movl	0xc(%rsp), %ecx
 295c42c:      	movq	0x20(%rsp), %r8
 295c431:      	movl	0x58(%rsp), %r9d
 295c436:      	pushq	%rax
 295c437:      	pushq	%r10
 295c439:      	pushq	0x240(%rsp)
 295c440:      	pushq	0x238(%rsp)
 295c447:      	pushq	0x48(%rsp)
 295c44b:      	pushq	%r15
 295c44d:      	callq	0x2975580 <_ZL28lowerShuffleAsBlendOfPSHUFBsRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERNS_12SelectionDAGERbSC_>
 295c452:      	jmp	0x295d014 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5134>
 295c457:      	xorl	%ecx, %ecx
 295c459:      	cmpl	$0x2, 0x10(%rsp)
 295c45e:      	setb	%cl
 295c461:      	movq	0x130(%rsp), %rbx
 295c469:      	movq	0x138(%rsp), %rsi
 295c471:      	xorl	%r14d, %r14d
 295c474:      	movq	%rbx, %rdi
 295c477:      	xorl	%edx, %edx
 295c479:      	callq	0x29754b0 <_ZL26canLowerByDroppingElementsN4llvm8ArrayRefIiEEbb>
 295c47e:      	cmpl	$0x1, %eax
 295c481:      	jne	0x295caf0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4c10>
 295c487:      	movq	0x60(%rsp), %rcx
 295c48c:      	movl	0x68(%rsp), %r8d
 295c491:      	movq	0x230(%rsp), %r15
 295c499:      	movq	%r15, %rdi
 295c49c:      	movl	$0x3e, %esi
 295c4a1:      	xorl	%edx, %edx
 295c4a3:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c4a8:      	movq	%rax, %rbx
 295c4ab:      	movl	%edx, %ebp
 295c4ad:      	subq	$0x8, %rsp
 295c4b1:      	movl	$0x8, %esi
 295c4b6:      	movq	%r15, %rdi
 295c4b9:      	movq	0x8(%rsp), %rdx
 295c4be:      	movl	$0x5, %ecx
 295c4c3:      	xorl	%r8d, %r8d
 295c4c6:      	movl	$0x1, %r9d
 295c4cc:      	pushq	$0x0
 295c4ce:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c4d3:      	addq	$0x10, %rsp
 295c4d7:      	movq	%rax, 0xa0(%rsp)
 295c4df:      	movl	%edx, 0xa8(%rsp)
 295c4e6:      	movq	%rbx, 0x30(%rsp)
 295c4eb:      	movl	%ebp, 0x38(%rsp)
 295c4ef:      	movq	0x3b0(%r15), %rax
 295c4f6:      	testq	%rax, %rax
 295c4f9:      	je	0x295c4ff <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x461f>
 295c4fb:      	movl	0x8(%rax), %r14d
 295c4ff:      	subq	$0x20, %rsp
 295c503:      	movups	0xc0(%rsp), %xmm0
 295c50b:      	movups	%xmm0, 0x10(%rsp)
 295c510:      	movups	0x50(%rsp), %xmm0
 295c515:      	movups	%xmm0, (%rsp)
 295c519:      	xorl	%ebx, %ebx
 295c51b:      	movq	0x250(%rsp), %rdi
 295c523:      	movl	$0x292, %esi            # imm = 0x292
 295c528:      	movq	0x20(%rsp), %rdx
 295c52d:      	movl	$0x3e, %ecx
 295c532:      	xorl	%r8d, %r8d
 295c535:      	movl	%r14d, %r9d
 295c538:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c53d:      	addq	$0x20, %rsp
 295c541:      	movq	%rax, 0x60(%rsp)
 295c546:      	movl	%edx, 0x68(%rsp)
 295c54a:      	cmpl	$0x2, 0x10(%rsp)
 295c54f:      	jae	0x295ceba <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4fda>
 295c555:      	leaq	0x60(%rsp), %rax
 295c55a:      	jmp	0x295cf88 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x50a8>
 295c55f:      	movq	0x230(%rsp), %r14
 295c567:      	movq	%r14, %rdi
 295c56a:      	movl	$0x3e, %esi
 295c56f:      	xorl	%edx, %edx
 295c571:      	movq	0x18(%rsp), %rcx
 295c576:      	movl	0x20(%rsp), %r8d
 295c57b:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c580:      	movq	%rbx, 0x30(%rsp)
 295c585:      	movl	%ebp, 0x38(%rsp)
 295c589:      	movq	%rax, 0x70(%rsp)
 295c58e:      	movl	%edx, 0x78(%rsp)
 295c592:      	movq	0x3b0(%r14), %rax
 295c599:      	testq	%rax, %rax
 295c59c:      	je	0x295c5a2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x46c2>
 295c59e:      	movl	0x8(%rax), %r12d
 295c5a2:      	subq	$0x20, %rsp
 295c5a6:      	movups	0x50(%rsp), %xmm0
 295c5ab:      	movups	%xmm0, 0x10(%rsp)
 295c5b0:      	movups	0x90(%rsp), %xmm0
 295c5b8:      	movups	%xmm0, (%rsp)
 295c5bc:      	movq	0x250(%rsp), %rdi
 295c5c4:      	movl	$0xbf, %esi
 295c5c9:      	movq	0x20(%rsp), %rdx
 295c5ce:      	movl	$0x3e, %ecx
 295c5d3:      	xorl	%r8d, %r8d
 295c5d6:      	movl	%r12d, %r9d
 295c5d9:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c5de:      	addq	$0x20, %rsp
 295c5e2:      	movq	%rax, 0x170(%rsp)
 295c5ea:      	movl	%edx, 0x178(%rsp)
 295c5f1:      	leaq	0x170(%rsp), %rax
 295c5f9:      	movq	0x230(%rsp), %rcx
 295c601:      	movq	0x3b0(%rcx), %rcx
 295c608:      	testq	%rcx, %rcx
 295c60b:      	je	0x295c669 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4789>
 295c60d:      	movl	0x8(%rcx), %r9d
 295c611:      	jmp	0x295c66c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x478c>
 295c613:      	cmpb	$0x1, 0x1db(%rbp)
 295c61a:      	jne	0x295cb60 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4c80>
 295c620:      	movq	0x130(%rsp), %rdi
 295c628:      	movl	$0x30, %esi
 295c62d:      	movq	0x230(%rsp), %rbx
 295c635:      	movq	%rbx, %rdx
 295c638:      	movq	(%rsp), %rcx
 295c63c:      	callq	0x28e6890 <_ZL14getConstVectorN4llvm8ArrayRefIiEENS_3MVTERNS_12SelectionDAGERKNS_5SDLocEb>
 295c641:      	movq	%rax, 0xa0(%rsp)
 295c649:      	movl	%edx, 0xa8(%rsp)
 295c650:      	movq	0x3b0(%rbx), %rax
 295c657:      	testq	%rax, %rax
 295c65a:      	je	0x295d787 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58a7>
 295c660:      	movl	0x8(%rax), %r9d
 295c664:      	jmp	0x295d78a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58aa>
 295c669:      	xorl	%r9d, %r9d
 295c66c:      	subq	$0x20, %rsp
 295c670:      	movups	(%rax), %xmm0
 295c673:      	movups	%xmm0, 0x10(%rsp)
 295c678:      	movdqu	0x80(%rsp), %xmm0
 295c681:      	movdqu	%xmm0, (%rsp)
 295c686:      	movq	0x250(%rsp), %rdi
 295c68e:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295c693:      	movq	0x20(%rsp), %rdx
 295c698:      	movl	$0x30, %ecx
 295c69d:      	xorl	%r8d, %r8d
 295c6a0:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c6a5:      	addq	$0x20, %rsp
 295c6a9:      	movq	%rax, %rbx
 295c6ac:      	movl	%edx, %ebp
 295c6ae:      	cmpl	$0x1, %r13d
 295c6b2:      	je	0x295a6b0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x27d0>
 295c6b8:      	decl	%r13d
 295c6bb:      	jmp	0x295c70a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x482a>
 295c6bd:      	subq	$0x20, %rsp
 295c6c1:      	movups	0x50(%rsp), %xmm0
 295c6c6:      	movups	%xmm0, 0x10(%rsp)
 295c6cb:      	movdqu	0x90(%rsp), %xmm0
 295c6d4:      	movdqu	%xmm0, (%rsp)
 295c6d9:      	movq	0x250(%rsp), %rdi
 295c6e1:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295c6e6:      	movq	0x20(%rsp), %rdx
 295c6eb:      	movl	$0x30, %ecx
 295c6f0:      	xorl	%r8d, %r8d
 295c6f3:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c6f8:      	addq	$0x20, %rsp
 295c6fc:      	movq	%rax, %rbx
 295c6ff:      	movl	%edx, %ebp
 295c701:      	decl	%r13d
 295c704:      	je	0x295a6b0 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x27d0>
 295c70a:      	movq	0x230(%rsp), %r15
 295c712:      	movq	%r15, %rdi
 295c715:      	movl	$0x3e, %esi
 295c71a:      	xorl	%edx, %edx
 295c71c:      	movq	%rbx, %rcx
 295c71f:      	movl	%ebp, %r8d
 295c722:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c727:      	movq	%rax, 0x30(%rsp)
 295c72c:      	movl	%edx, 0x38(%rsp)
 295c730:      	movq	%rax, 0x70(%rsp)
 295c735:      	movl	%edx, 0x78(%rsp)
 295c739:      	movq	0x3b0(%r15), %rax
 295c740:      	movl	$0x0, %r9d
 295c746:      	testq	%rax, %rax
 295c749:      	je	0x295c6bd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x47dd>
 295c74f:      	movl	0x8(%rax), %r9d
 295c753:      	jmp	0x295c6bd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x47dd>
 295c758:      	movl	0x148(%r13), %eax
 295c75f:      	cmpl	$0x5, %eax
 295c762:      	jl	0x295cbc8 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4ce8>
 295c768:      	xorl	%r15d, %r15d
 295c76b:      	subq	$0x8, %rsp
 295c76f:      	xorl	%r14d, %r14d
 295c772:      	movq	0x238(%rsp), %rdi
 295c77a:      	xorl	%esi, %esi
 295c77c:      	movq	0x8(%rsp), %rdx
 295c781:      	movl	$0x7, %ecx
 295c786:      	xorl	%r8d, %r8d
 295c789:      	xorl	%r9d, %r9d
 295c78c:      	pushq	$0x0
 295c78e:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c793:      	addq	$0x10, %rsp
 295c797:      	leaq	0xb0(%rsp), %rcx
 295c79f:      	movq	%rcx, 0xa0(%rsp)
 295c7a7:      	movq	%rax, 0xb0(%rsp)
 295c7af:      	movl	%edx, 0xb8(%rsp)
 295c7b6:      	movq	%rax, 0xc0(%rsp)
 295c7be:      	movl	%edx, 0xc8(%rsp)
 295c7c5:      	movq	%rax, 0xd0(%rsp)
 295c7cd:      	movl	%edx, 0xd8(%rsp)
 295c7d4:      	movq	%rax, 0xe0(%rsp)
 295c7dc:      	movl	%edx, 0xe8(%rsp)
 295c7e3:      	movabsq	$0x400000004, %rax      # imm = 0x400000004
 295c7ed:      	movq	%rax, 0xa8(%rsp)
 295c7f5:      	decb	%bl
 295c7f7:      	movl	$0x1, %ebp
 295c7fc:      	movl	%ebx, %ecx
 295c7fe:      	shll	%cl, %ebp
 295c800:      	subq	$0x8, %rsp
 295c804:      	movl	$0xffff, %esi           # imm = 0xFFFF
 295c809:      	movq	0x238(%rsp), %rdi
 295c811:      	movq	0x8(%rsp), %rdx
 295c816:      	movl	$0x7, %ecx
 295c81b:      	xorl	%r8d, %r8d
 295c81e:      	xorl	%r9d, %r9d
 295c821:      	pushq	$0x0
 295c823:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295c828:      	addq	$0x10, %rsp
 295c82c:      	movl	%r14d, %esi
 295c82f:      	movq	0xa0(%rsp), %rcx
 295c837:      	shlq	$0x4, %rsi
 295c83b:      	movq	%rax, (%rcx,%rsi)
 295c83f:      	movl	%edx, 0x8(%rcx,%rsi)
 295c843:      	addl	%ebp, %r14d
 295c846:      	cmpl	$0x4, %r14d
 295c84a:      	jne	0x295c800 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4920>
 295c84c:      	movl	0xa8(%rsp), %eax
 295c853:      	movq	%rcx, 0x30(%rsp)
 295c858:      	movq	%rax, 0x38(%rsp)
 295c85d:      	movq	0x230(%rsp), %rax
 295c865:      	movq	0x3b0(%rax), %rax
 295c86c:      	xorl	%ebx, %ebx
 295c86e:      	movl	$0x0, %r9d
 295c874:      	testq	%rax, %rax
 295c877:      	je	0x295c87d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x499d>
 295c879:      	movl	0x8(%rax), %r9d
 295c87d:      	subq	$0x10, %rsp
 295c881:      	movups	0x40(%rsp), %xmm0
 295c886:      	movups	%xmm0, (%rsp)
 295c88a:      	movq	0x240(%rsp), %r12
 295c892:      	movq	%r12, %rdi
 295c895:      	movl	$0xa0, %esi
 295c89a:      	movq	0x10(%rsp), %rdx
 295c89f:      	movl	$0x49, %ecx
 295c8a4:      	xorl	%r8d, %r8d
 295c8a7:      	callq	0x5e264a0 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_8ArrayRefINS_7SDValueEEENS_11SDNodeFlagsE>
 295c8ac:      	addq	$0x10, %rsp
 295c8b0:      	movq	%rax, %r14
 295c8b3:      	movl	%edx, %r13d
 295c8b6:      	movq	%r12, %rdi
 295c8b9:      	movl	$0x49, %esi
 295c8be:      	xorl	%edx, %edx
 295c8c0:      	movq	0x10(%rsp), %rcx
 295c8c5:      	movl	0xc(%rsp), %r8d
 295c8ca:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c8cf:      	movq	%r14, 0x30(%rsp)
 295c8d4:      	movl	%r13d, 0x38(%rsp)
 295c8d9:      	movq	%rax, 0x70(%rsp)
 295c8de:      	movl	%edx, 0x78(%rsp)
 295c8e2:      	movq	0x3b0(%r12), %rax
 295c8ea:      	testq	%rax, %rax
 295c8ed:      	je	0x295c8f2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4a12>
 295c8ef:      	movl	0x8(%rax), %ebx
 295c8f2:      	subq	$0x20, %rsp
 295c8f6:      	movups	0x50(%rsp), %xmm0
 295c8fb:      	movups	%xmm0, 0x10(%rsp)
 295c900:      	movups	0x90(%rsp), %xmm0
 295c908:      	movups	%xmm0, (%rsp)
 295c90c:      	xorl	%r12d, %r12d
 295c90f:      	movq	0x250(%rsp), %rbp
 295c917:      	movq	%rbp, %rdi
 295c91a:      	movl	$0xbf, %esi
 295c91f:      	movq	0x20(%rsp), %rdx
 295c924:      	movl	$0x49, %ecx
 295c929:      	xorl	%r8d, %r8d
 295c92c:      	movl	%ebx, %r9d
 295c92f:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c934:      	addq	$0x20, %rsp
 295c938:      	movq	%rax, %rbx
 295c93b:      	movl	%edx, 0x10(%rsp)
 295c93f:      	movq	%rbp, %rdi
 295c942:      	movl	$0x49, %esi
 295c947:      	xorl	%edx, %edx
 295c949:      	movq	0x20(%rsp), %rcx
 295c94e:      	movl	0x58(%rsp), %r8d
 295c953:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295c958:      	movq	%r14, 0x30(%rsp)
 295c95d:      	movl	%r13d, 0x38(%rsp)
 295c962:      	movq	%rax, 0x70(%rsp)
 295c967:      	movl	%edx, 0x78(%rsp)
 295c96b:      	movq	0x3b0(%rbp), %rax
 295c972:      	testq	%rax, %rax
 295c975:      	je	0x295c97b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4a9b>
 295c977:      	movl	0x8(%rax), %r12d
 295c97b:      	subq	$0x20, %rsp
 295c97f:      	movups	0x50(%rsp), %xmm0
 295c984:      	movups	%xmm0, 0x10(%rsp)
 295c989:      	movups	0x90(%rsp), %xmm0
 295c991:      	movups	%xmm0, (%rsp)
 295c995:      	xorl	%r14d, %r14d
 295c998:      	movq	0x250(%rsp), %rdi
 295c9a0:      	movl	$0xbf, %esi
 295c9a5:      	movq	0x20(%rsp), %rdx
 295c9aa:      	movl	$0x49, %ecx
 295c9af:      	xorl	%r8d, %r8d
 295c9b2:      	movl	%r12d, %r9d
 295c9b5:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295c9ba:      	addq	$0x20, %rsp
 295c9be:      	movq	%rax, %r13
 295c9c1:      	movl	%edx, %r12d
 295c9c4:      	movq	0xa0(%rsp), %rdi
 295c9cc:      	leaq	0xb0(%rsp), %rax
 295c9d4:      	cmpq	%rax, %rdi
 295c9d7:      	je	0x295c9de <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4afe>
 295c9d9:      	callq	0x828a640 <free@plt>
 295c9de:      	movq	%r13, 0xa0(%rsp)
 295c9e6:      	movl	%r12d, 0xa8(%rsp)
 295c9ee:      	movl	0x18(%rsp), %eax
 295c9f2:      	movl	%eax, 0xac(%rsp)
 295c9f9:      	movq	%rbx, 0x30(%rsp)
 295c9fe:      	movl	0x10(%rsp), %eax
 295ca02:      	movl	%eax, 0x38(%rsp)
 295ca06:      	movq	0x230(%rsp), %rax
 295ca0e:      	movq	0x3b0(%rax), %rax
 295ca15:      	testq	%rax, %rax
 295ca18:      	je	0x295ca1e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4b3e>
 295ca1a:      	movl	0x8(%rax), %r14d
 295ca1e:      	subq	$0x20, %rsp
 295ca22:      	movups	0xc0(%rsp), %xmm0
 295ca2a:      	movups	%xmm0, 0x10(%rsp)
 295ca2f:      	movdqu	0x50(%rsp), %xmm0
 295ca35:      	movdqu	%xmm0, (%rsp)
 295ca3a:      	movq	0x250(%rsp), %rdi
 295ca42:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295ca47:      	movq	0x20(%rsp), %rdx
 295ca4c:      	movl	$0x3e, %ecx
 295ca51:      	xorl	%r8d, %r8d
 295ca54:      	movl	%r14d, %r9d
 295ca57:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ca5c:      	addq	$0x20, %rsp
 295ca60:      	movl	%edx, %r8d
 295ca63:      	testb	%r15b, %r15b
 295ca66:      	je	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
 295ca6c:      	xorl	%r13d, %r13d
 295ca6f:      	movq	0x230(%rsp), %r12
 295ca77:      	movq	%r12, %rdi
 295ca7a:      	movl	$0x49, %esi
 295ca7f:      	xorl	%edx, %edx
 295ca81:      	movq	%rax, %rcx
 295ca84:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295ca89:      	movq	%rax, 0xa0(%rsp)
 295ca91:      	movl	%edx, 0xa8(%rsp)
 295ca98:      	movq	%rax, 0x30(%rsp)
 295ca9d:      	movl	%edx, 0x38(%rsp)
 295caa1:      	movq	0x3b0(%r12), %rax
 295caa9:      	testq	%rax, %rax
 295caac:      	je	0x295cab2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4bd2>
 295caae:      	movl	0x8(%rax), %r13d
 295cab2:      	subq	$0x20, %rsp
 295cab6:      	movups	0xc0(%rsp), %xmm0
 295cabe:      	movups	%xmm0, 0x10(%rsp)
 295cac3:      	movdqu	0x50(%rsp), %xmm0
 295cac9:      	movdqu	%xmm0, (%rsp)
 295cace:      	movq	0x250(%rsp), %rdi
 295cad6:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295cadb:      	movq	0x20(%rsp), %rdx
 295cae0:      	movl	$0x3e, %ecx
 295cae5:      	xorl	%r8d, %r8d
 295cae8:      	movl	%r13d, %r9d
 295caeb:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295caf0:      	movq	0x60(%rsp), %r14
 295caf5:      	movl	0x68(%rsp), %eax
 295caf9:      	movl	%eax, 0x10(%rsp)
 295cafd:      	testl	%r15d, %r15d
 295cb00:      	jle	0x295d01d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x513d>
 295cb06:      	subq	$0x30, %rsp
 295cb0a:      	movdqu	0x160(%rsp), %xmm0
 295cb13:      	movdqu	%xmm0, (%rsp)
 295cb18:      	movq	0x260(%rsp), %rax
 295cb20:      	movq	%rax, 0x20(%rsp)
 295cb25:      	movq	%rbp, 0x18(%rsp)
 295cb2a:      	movq	0x250(%rsp), %rax
 295cb32:      	movq	%rax, 0x10(%rsp)
 295cb37:      	movq	0x30(%rsp), %rdi
 295cb3c:      	movl	$0x30, %esi
 295cb41:      	movq	%r14, %rdx
 295cb44:      	movl	0x40(%rsp), %ecx
 295cb48:      	movq	0x48(%rsp), %r8
 295cb4d:      	movl	0x50(%rsp), %r9d
 295cb52:      	callq	0x2966760 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295cb57:      	addq	$0x30, %rsp
 295cb5b:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295cb60:      	movq	0x60(%rsp), %rdx
 295cb65:      	movl	0x68(%rsp), %ecx
 295cb69:      	movl	0x148(%rbp), %eax
 295cb6f:      	movzbl	0x16a(%rbp), %esi
 295cb76:      	subq	$0x30, %rsp
 295cb7a:      	movdqu	0x160(%rsp), %xmm0
 295cb83:      	movdqu	%xmm0, (%rsp)
 295cb88:      	movq	0x260(%rsp), %rdi
 295cb90:      	movq	%rdi, 0x20(%rsp)
 295cb95:      	movl	%esi, 0x18(%rsp)
 295cb99:      	movl	%eax, 0x10(%rsp)
 295cb9d:      	movq	0x30(%rsp), %rdi
 295cba2:      	movl	$0x30, %esi
 295cba7:      	movq	0x48(%rsp), %r8
 295cbac:      	movl	0x50(%rsp), %r9d
 295cbb1:      	callq	0x296cde0 <_ZL34lowerShuffleAsByteRotateAndPermuteRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295cbb6:      	addq	$0x30, %rsp
 295cbba:      	testq	%rax, %rax
 295cbbd:      	jne	0x295d7dc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x58fc>
 295cbc3:      	jmp	0x295d7e2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5902>
 295cbc8:      	cmpl	$0x4, %eax
 295cbcb:      	je	0x295c158 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4278>
 295cbd1:      	subq	$0x8, %rsp
 295cbd5:      	xorl	%r15d, %r15d
 295cbd8:      	movl	$0x10, %esi
 295cbdd:      	movq	0x238(%rsp), %r14
 295cbe5:      	movq	%r14, %rdi
 295cbe8:      	movq	0x8(%rsp), %rdx
 295cbed:      	movl	$0x5, %ecx
 295cbf2:      	xorl	%r8d, %r8d
 295cbf5:      	movl	$0x1, %r9d
 295cbfb:      	pushq	$0x0
 295cbfd:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295cc02:      	addq	$0x10, %rsp
 295cc06:      	movq	%rax, %rbx
 295cc09:      	movl	%edx, %ebp
 295cc0b:      	movq	%r14, %rdi
 295cc0e:      	movl	$0x49, %esi
 295cc13:      	xorl	%edx, %edx
 295cc15:      	movq	0x10(%rsp), %rcx
 295cc1a:      	movl	0xc(%rsp), %r8d
 295cc1f:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cc24:      	movq	%rax, %r12
 295cc27:      	movl	%edx, %r13d
 295cc2a:      	movq	%r14, %rdi
 295cc2d:      	movl	$0x49, %esi
 295cc32:      	xorl	%edx, %edx
 295cc34:      	movq	0x20(%rsp), %rcx
 295cc39:      	movl	0x58(%rsp), %r8d
 295cc3e:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cc43:      	movq	%rax, 0x10(%rsp)
 295cc48:      	movl	%edx, 0xc(%rsp)
 295cc4c:      	movq	%rbx, 0xa0(%rsp)
 295cc54:      	movl	%ebp, 0xa8(%rsp)
 295cc5b:      	movq	%r12, 0x30(%rsp)
 295cc60:      	movl	%r13d, 0x38(%rsp)
 295cc65:      	movq	0x3b0(%r14), %rax
 295cc6c:      	movl	$0x0, %r9d
 295cc72:      	testq	%rax, %rax
 295cc75:      	je	0x295cc7b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4d9b>
 295cc77:      	movl	0x8(%rax), %r9d
 295cc7b:      	subq	$0x20, %rsp
 295cc7f:      	movups	0xc0(%rsp), %xmm0
 295cc87:      	movups	%xmm0, 0x10(%rsp)
 295cc8c:      	movups	0x50(%rsp), %xmm0
 295cc91:      	movups	%xmm0, (%rsp)
 295cc95:      	movq	0x250(%rsp), %r14
 295cc9d:      	movq	%r14, %rdi
 295cca0:      	movl	$0x291, %esi            # imm = 0x291
 295cca5:      	movq	0x20(%rsp), %rdx
 295ccaa:      	movl	$0x49, %ecx
 295ccaf:      	xorl	%r8d, %r8d
 295ccb2:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ccb7:      	addq	$0x20, %rsp
 295ccbb:      	movq	%rax, 0x28(%rsp)
 295ccc0:      	movl	%edx, %r13d
 295ccc3:      	movq	%rbx, 0xa0(%rsp)
 295cccb:      	movl	%ebp, 0xa8(%rsp)
 295ccd2:      	movq	0x10(%rsp), %rax
 295ccd7:      	movq	%rax, 0x30(%rsp)
 295ccdc:      	movl	0xc(%rsp), %eax
 295cce0:      	movl	%eax, 0x38(%rsp)
 295cce4:      	movl	0x18(%rsp), %eax
 295cce8:      	movl	%eax, 0x3c(%rsp)
 295ccec:      	movq	0x3b0(%r14), %rax
 295ccf3:      	testq	%rax, %rax
 295ccf6:      	je	0x295ccfc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4e1c>
 295ccf8:      	movl	0x8(%rax), %r15d
 295ccfc:      	subq	$0x20, %rsp
 295cd00:      	movups	0xc0(%rsp), %xmm0
 295cd08:      	movups	%xmm0, 0x10(%rsp)
 295cd0d:      	movups	0x50(%rsp), %xmm0
 295cd12:      	movups	%xmm0, (%rsp)
 295cd16:      	movq	$0x0, 0x30(%rsp)
 295cd1f:      	movq	0x250(%rsp), %r12
 295cd27:      	movq	%r12, %rdi
 295cd2a:      	movl	$0x291, %esi            # imm = 0x291
 295cd2f:      	movq	0x20(%rsp), %rdx
 295cd34:      	movl	$0x49, %ecx
 295cd39:      	xorl	%r8d, %r8d
 295cd3c:      	movl	%r15d, %r9d
 295cd3f:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cd44:      	addq	$0x20, %rsp
 295cd48:      	movq	%rax, %r15
 295cd4b:      	movl	%edx, 0xc(%rsp)
 295cd4f:      	movq	%rbx, 0xa0(%rsp)
 295cd57:      	movl	%ebp, 0xa8(%rsp)
 295cd5e:      	movq	0x28(%rsp), %rax
 295cd63:      	movq	%rax, 0x30(%rsp)
 295cd68:      	movl	%r13d, 0x38(%rsp)
 295cd6d:      	movq	0x3b0(%r12), %rax
 295cd75:      	movl	$0x0, %r9d
 295cd7b:      	testq	%rax, %rax
 295cd7e:      	je	0x295cd84 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4ea4>
 295cd80:      	movl	0x8(%rax), %r9d
 295cd84:      	subq	$0x20, %rsp
 295cd88:      	movups	0xc0(%rsp), %xmm0
 295cd90:      	movups	%xmm0, 0x10(%rsp)
 295cd95:      	movups	0x50(%rsp), %xmm0
 295cd9a:      	movups	%xmm0, (%rsp)
 295cd9e:      	movq	0x250(%rsp), %r14
 295cda6:      	movq	%r14, %rdi
 295cda9:      	movl	$0x293, %esi            # imm = 0x293
 295cdae:      	movq	0x20(%rsp), %rdx
 295cdb3:      	movl	$0x49, %ecx
 295cdb8:      	xorl	%r8d, %r8d
 295cdbb:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cdc0:      	addq	$0x20, %rsp
 295cdc4:      	movq	%rax, %r12
 295cdc7:      	movl	%edx, %r13d
 295cdca:      	movq	%rbx, 0xa0(%rsp)
 295cdd2:      	movl	%ebp, 0xa8(%rsp)
 295cdd9:      	movq	%r15, 0x30(%rsp)
 295cdde:      	movl	0xc(%rsp), %eax
 295cde2:      	movl	%eax, 0x38(%rsp)
 295cde6:      	movl	0x18(%rsp), %eax
 295cdea:      	movl	%eax, 0x3c(%rsp)
 295cdee:      	movq	0x3b0(%r14), %rax
 295cdf5:      	testq	%rax, %rax
 295cdf8:      	je	0x295ce02 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4f22>
 295cdfa:      	movl	0x8(%rax), %eax
 295cdfd:      	movq	%rax, 0x10(%rsp)
 295ce02:      	subq	$0x20, %rsp
 295ce06:      	movups	0xc0(%rsp), %xmm0
 295ce0e:      	movups	%xmm0, 0x10(%rsp)
 295ce13:      	movups	0x50(%rsp), %xmm0
 295ce18:      	movups	%xmm0, (%rsp)
 295ce1c:      	xorl	%ebx, %ebx
 295ce1e:      	movq	0x250(%rsp), %r14
 295ce26:      	movq	%r14, %rdi
 295ce29:      	movl	$0x293, %esi            # imm = 0x293
 295ce2e:      	movq	0x20(%rsp), %rdx
 295ce33:      	movl	$0x49, %ecx
 295ce38:      	xorl	%r8d, %r8d
 295ce3b:      	movq	0x30(%rsp), %r9
 295ce40:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295ce45:      	addq	$0x20, %rsp
 295ce49:      	movq	%rax, 0xa0(%rsp)
 295ce51:      	movl	%edx, 0xa8(%rsp)
 295ce58:      	movl	0x18(%rsp), %eax
 295ce5c:      	movl	%eax, 0xac(%rsp)
 295ce63:      	movq	%r12, 0x30(%rsp)
 295ce68:      	movl	%r13d, 0x38(%rsp)
 295ce6d:      	movq	0x3b0(%r14), %rax
 295ce74:      	testq	%rax, %rax
 295ce77:      	je	0x295ce7c <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x4f9c>
 295ce79:      	movl	0x8(%rax), %ebx
 295ce7c:      	subq	$0x20, %rsp
 295ce80:      	movups	0xc0(%rsp), %xmm0
 295ce88:      	movups	%xmm0, 0x10(%rsp)
 295ce8d:      	movdqu	0x50(%rsp), %xmm0
 295ce93:      	movdqu	%xmm0, (%rsp)
 295ce98:      	movq	0x250(%rsp), %rdi
 295cea0:      	movl	$0x2b5, %esi            # imm = 0x2B5
 295cea5:      	movq	0x20(%rsp), %rdx
 295ceaa:      	movl	$0x3e, %ecx
 295ceaf:      	xorl	%r8d, %r8d
 295ceb2:      	movl	%ebx, %r9d
 295ceb5:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295ceba:      	movq	0x230(%rsp), %r15
 295cec2:      	movq	%r15, %rdi
 295cec5:      	movl	$0x3e, %esi
 295ceca:      	xorl	%edx, %edx
 295cecc:      	movq	0x18(%rsp), %rcx
 295ced1:      	movl	0x20(%rsp), %r8d
 295ced6:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295cedb:      	movq	%rax, %r14
 295cede:      	movl	%edx, %ebp
 295cee0:      	subq	$0x8, %rsp
 295cee4:      	movl	$0x8, %esi
 295cee9:      	movq	%r15, %rdi
 295ceec:      	movq	0x8(%rsp), %rdx
 295cef1:      	movl	$0x5, %ecx
 295cef6:      	xorl	%r8d, %r8d
 295cef9:      	movl	$0x1, %r9d
 295ceff:      	pushq	$0x0
 295cf01:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295cf06:      	addq	$0x10, %rsp
 295cf0a:      	movq	%rax, 0xa0(%rsp)
 295cf12:      	movl	%edx, 0xa8(%rsp)
 295cf19:      	movq	%r14, 0x30(%rsp)
 295cf1e:      	movl	%ebp, 0x38(%rsp)
 295cf22:      	movq	0x3b0(%r15), %rax
 295cf29:      	testq	%rax, %rax
 295cf2c:      	je	0x295cf31 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5051>
 295cf2e:      	movl	0x8(%rax), %ebx
 295cf31:      	subq	$0x20, %rsp
 295cf35:      	movups	0xc0(%rsp), %xmm0
 295cf3d:      	movups	%xmm0, 0x10(%rsp)
 295cf42:      	movups	0x50(%rsp), %xmm0
 295cf47:      	movups	%xmm0, (%rsp)
 295cf4b:      	movq	0x250(%rsp), %rdi
 295cf53:      	movl	$0x292, %esi            # imm = 0x292
 295cf58:      	movq	0x20(%rsp), %rdx
 295cf5d:      	movl	$0x3e, %ecx
 295cf62:      	xorl	%r8d, %r8d
 295cf65:      	movl	%ebx, %r9d
 295cf68:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295cf6d:      	addq	$0x20, %rsp
 295cf71:      	movq	%rax, 0x170(%rsp)
 295cf79:      	movl	%edx, 0x178(%rsp)
 295cf80:      	leaq	0x170(%rsp), %rax
 295cf88:      	movq	0x230(%rsp), %rcx
 295cf90:      	movq	0x3b0(%rcx), %rcx
 295cf97:      	testq	%rcx, %rcx
 295cf9a:      	je	0x295d47a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x559a>
 295cfa0:      	movl	0x8(%rcx), %r9d
 295cfa4:      	jmp	0x295d47d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x559d>
 295cfa9:      	movq	%r15, 0xa0(%rsp)
 295cfb1:      	movq	0x28(%rsp), %rax
 295cfb6:      	movq	%rax, 0xa8(%rsp)
 295cfbe:      	subq	$0x30, %rsp
 295cfc2:      	movdqu	0xd0(%rsp), %xmm0
 295cfcb:      	movdqu	%xmm0, (%rsp)
 295cfd0:      	movq	0x260(%rsp), %rax
 295cfd8:      	movq	%rax, 0x20(%rsp)
 295cfdd:      	movq	%r13, 0x18(%rsp)
 295cfe2:      	movq	0x250(%rsp), %rax
 295cfea:      	movq	%rax, 0x10(%rsp)
 295cfef:      	movq	0x30(%rsp), %rdi
 295cff4:      	movl	$0x3e, %esi
 295cff9:      	movq	0x40(%rsp), %rdx
 295cffe:      	movl	0x3c(%rsp), %ecx
 295d002:      	movq	0x50(%rsp), %r8
 295d007:      	movl	0x88(%rsp), %r9d
 295d00f:      	callq	0x2966760 <_ZL36lowerShuffleAsDecomposedShuffleMergeRKN4llvm5SDLocENS_3MVTENS_7SDValueES4_NS_8ArrayRefIiEERKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE>
 295d014:      	addq	$0x30, %rsp
 295d018:      	jmp	0x2959c80 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da0>
 295d01d:      	movl	0x6c(%rsp), %eax
 295d021:      	movl	%eax, 0x28(%rsp)
 295d025:      	pcmpeqd	%xmm0, %xmm0
 295d029:      	movdqa	%xmm0, 0xb0(%rsp)
 295d032:      	movdqa	%xmm0, 0xa0(%rsp)
 295d03b:      	movdqa	%xmm0, 0x40(%rsp)
 295d041:      	movdqa	%xmm0, 0x30(%rsp)
 295d047:      	movl	(%rbx), %eax
 295d049:      	movl	$0xffffffff, 0xc(%rsp)  # imm = 0xFFFFFFFF
 295d051:      	movl	$0xffffffff, 0x20(%rsp) # imm = 0xFFFFFFFF
 295d059:      	testl	%eax, %eax
 295d05b:      	js	0x295d068 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5188>
 295d05d:      	movl	%eax, 0xa0(%rsp)
 295d064:      	movl	%eax, 0x20(%rsp)
 295d068:      	movl	0x4(%rbx), %eax
 295d06b:      	testl	%eax, %eax
 295d06d:      	js	0x295d07a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x519a>
 295d06f:      	movl	%eax, 0xa4(%rsp)
 295d076:      	movl	%eax, 0xc(%rsp)
 295d07a:      	movl	0x8(%rbx), %eax
 295d07d:      	movl	$0xffffffff, 0x18(%rsp) # imm = 0xFFFFFFFF
 295d085:      	movl	$0xffffffff, 0x9c(%rsp) # imm = 0xFFFFFFFF
 295d090:      	testl	%eax, %eax
 295d092:      	js	0x295d0a2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x51c2>
 295d094:      	movl	%eax, 0xa8(%rsp)
 295d09b:      	movl	%eax, 0x9c(%rsp)
 295d0a2:      	movl	0xc(%rbx), %eax
 295d0a5:      	testl	%eax, %eax
 295d0a7:      	js	0x295d0b4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x51d4>
 295d0a9:      	movl	%eax, 0xac(%rsp)
 295d0b0:      	movl	%eax, 0x18(%rsp)
 295d0b4:      	movl	0x10(%rbx), %eax
 295d0b7:      	movl	$0xffffffff, 0x58(%rsp) # imm = 0xFFFFFFFF
 295d0bf:      	movl	$0xffffffff, 0x15c(%rsp) # imm = 0xFFFFFFFF
 295d0ca:      	testl	%eax, %eax
 295d0cc:      	js	0x295d0dc <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x51fc>
 295d0ce:      	movl	%eax, 0xb0(%rsp)
 295d0d5:      	movl	%eax, 0x15c(%rsp)
 295d0dc:      	movl	0x14(%rbx), %eax
 295d0df:      	testl	%eax, %eax
 295d0e1:      	js	0x295d0ee <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x520e>
 295d0e3:      	movl	%eax, 0xb4(%rsp)
 295d0ea:      	movl	%eax, 0x58(%rsp)
 295d0ee:      	movl	0x18(%rbx), %eax
 295d0f1:      	movl	$0xffffffff, 0x160(%rsp) # imm = 0xFFFFFFFF
 295d0fc:      	movl	$0xffffffff, 0x154(%rsp) # imm = 0xFFFFFFFF
 295d107:      	testl	%eax, %eax
 295d109:      	js	0x295d119 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5239>
 295d10b:      	movl	%eax, 0xb8(%rsp)
 295d112:      	movl	%eax, 0x154(%rsp)
 295d119:      	movl	0x1c(%rbx), %eax
 295d11c:      	testl	%eax, %eax
 295d11e:      	js	0x295d12e <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x524e>
 295d120:      	movl	%eax, 0xbc(%rsp)
 295d127:      	movl	%eax, 0x160(%rsp)
 295d12e:      	movl	0x20(%rbx), %eax
 295d131:      	movl	$0xffffffff, 0x158(%rsp) # imm = 0xFFFFFFFF
 295d13c:      	movl	$0xffffffff, 0x14c(%rsp) # imm = 0xFFFFFFFF
 295d147:      	testl	%eax, %eax
 295d149:      	js	0x295d156 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5276>
 295d14b:      	movl	%eax, 0x30(%rsp)
 295d14f:      	movl	%eax, 0x14c(%rsp)
 295d156:      	movl	0x24(%rbx), %eax
 295d159:      	testl	%eax, %eax
 295d15b:      	js	0x295d168 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5288>
 295d15d:      	movl	%eax, 0x34(%rsp)
 295d161:      	movl	%eax, 0x158(%rsp)
 295d168:      	movl	0x28(%rbx), %eax
 295d16b:      	movl	$0xffffffff, 0x150(%rsp) # imm = 0xFFFFFFFF
 295d176:      	movl	$0xffffffff, 0x140(%rsp) # imm = 0xFFFFFFFF
 295d181:      	testl	%eax, %eax
 295d183:      	js	0x295d190 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52b0>
 295d185:      	movl	%eax, 0x38(%rsp)
 295d189:      	movl	%eax, 0x140(%rsp)
 295d190:      	movl	0x2c(%rbx), %eax
 295d193:      	testl	%eax, %eax
 295d195:      	js	0x295d1a2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52c2>
 295d197:      	movl	%eax, 0x3c(%rsp)
 295d19b:      	movl	%eax, 0x150(%rsp)
 295d1a2:      	movl	0x30(%rbx), %eax
 295d1a5:      	movl	$0xffffffff, 0x148(%rsp) # imm = 0xFFFFFFFF
 295d1b0:      	movl	$0xffffffff, %r13d      # imm = 0xFFFFFFFF
 295d1b6:      	testl	%eax, %eax
 295d1b8:      	js	0x295d1c1 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52e1>
 295d1ba:      	movl	%eax, 0x40(%rsp)
 295d1be:      	movl	%eax, %r13d
 295d1c1:      	movl	0x34(%rbx), %eax
 295d1c4:      	testl	%eax, %eax
 295d1c6:      	js	0x295d1d3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x52f3>
 295d1c8:      	movl	%eax, 0x44(%rsp)
 295d1cc:      	movl	%eax, 0x148(%rsp)
 295d1d3:      	movl	0x38(%rbx), %eax
 295d1d6:      	movl	$0xffffffff, 0x144(%rsp) # imm = 0xFFFFFFFF
 295d1e1:      	movl	$0xffffffff, %r15d      # imm = 0xFFFFFFFF
 295d1e7:      	testl	%eax, %eax
 295d1e9:      	js	0x295d1f2 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5312>
 295d1eb:      	movl	%eax, 0x48(%rsp)
 295d1ef:      	movl	%eax, %r15d
 295d1f2:      	movl	0x3c(%rbx), %eax
 295d1f5:      	testl	%eax, %eax
 295d1f7:      	js	0x295d204 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5324>
 295d1f9:      	movl	%eax, 0x4c(%rsp)
 295d1fd:      	movl	%eax, 0x144(%rsp)
 295d204:      	leaq	0xa0(%rsp), %rdi
 295d20c:      	callq	0x2987680 <_ZN4llvm7none_ofIRSt5arrayIiLm8EEZL17lowerV16I8ShuffleRKNS_5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueESC_RKNS_12X86SubtargetERNS_12SelectionDAGEE3$_2EEbOT_T0_>
 295d211:      	testb	%al, %al
 295d213:      	je	0x295d4b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55d3>
 295d219:      	leaq	0x30(%rsp), %rdi
 295d21e:      	callq	0x2987700 <_ZN4llvm7none_ofIRSt5arrayIiLm8EEZL17lowerV16I8ShuffleRKNS_5SDLocENS_8ArrayRefIiEERKNS_5APIntENS_7SDValueESC_RKNS_12X86SubtargetERNS_12SelectionDAGEE3$_3EEbOT_T0_>
 295d223:      	testb	%al, %al
 295d225:      	je	0x295d4b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x55d3>
 295d22b:      	movq	$0x0, 0x28(%rsp)
 295d234:      	movq	0x230(%rsp), %r12
 295d23c:      	movq	%r12, %rdi
 295d23f:      	movl	$0x3e, %esi
 295d244:      	xorl	%edx, %edx
 295d246:      	movq	%r14, %rcx
 295d249:      	movl	0x10(%rsp), %r8d
 295d24e:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d253:      	movq	%rax, %rbx
 295d256:      	movl	%edx, %ebp
 295d258:      	subq	$0x8, %rsp
 295d25c:      	movl	$0xff, %esi
 295d261:      	movq	%r12, %rdi
 295d264:      	movq	0x8(%rsp), %rdx
 295d269:      	movl	$0x3e, %ecx
 295d26e:      	xorl	%r8d, %r8d
 295d271:      	xorl	%r9d, %r9d
 295d274:      	pushq	$0x0
 295d276:      	callq	0x5dfff80 <_ZN4llvm12SelectionDAG11getConstantEmRKNS_5SDLocENS_3EVTEbb>
 295d27b:      	addq	$0x10, %rsp
 295d27f:      	movq	%rax, 0x70(%rsp)
 295d284:      	movl	%edx, 0x78(%rsp)
 295d288:      	movq	%rbx, 0x80(%rsp)
 295d290:      	movl	%ebp, 0x88(%rsp)
 295d297:      	movq	0x3b0(%r12), %rax
 295d29f:      	testq	%rax, %rax
 295d2a2:      	je	0x295d2ac <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x53cc>
 295d2a4:      	movl	0x8(%rax), %eax
 295d2a7:      	movq	%rax, 0x28(%rsp)
 295d2ac:      	subq	$0x20, %rsp
 295d2b0:      	movups	0x90(%rsp), %xmm0
 295d2b8:      	movups	%xmm0, 0x10(%rsp)
 295d2bd:      	movups	0xa0(%rsp), %xmm0
 295d2c5:      	movups	%xmm0, (%rsp)
 295d2c9:      	movq	0x250(%rsp), %rbx
 295d2d1:      	movq	%rbx, %rdi
 295d2d4:      	movl	$0xbf, %esi
 295d2d9:      	movq	0x20(%rsp), %rdx
 295d2de:      	movl	$0x3e, %ecx
 295d2e3:      	xorl	%r8d, %r8d
 295d2e6:      	movq	0x48(%rsp), %r9
 295d2eb:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d2f0:      	addq	$0x20, %rsp
 295d2f4:      	movq	%rax, 0x180(%rsp)
 295d2fc:      	movl	%edx, 0x16c(%rsp)
 295d303:      	movq	%rbx, %rdi
 295d306:      	movl	$0x3e, %esi
 295d30b:      	xorl	%edx, %edx
 295d30d:      	callq	0x2842500 <_ZN4llvm12SelectionDAG8getUNDEFENS_3EVTE>
 295d312:      	movq	%rax, %rcx
 295d315:      	cmpl	$0x0, 0x20(%rsp)
 295d31a:      	js	0x295d329 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5449>
 295d31c:      	movl	0x20(%rsp), %eax
 295d320:      	shrl	%eax
 295d322:      	movl	%eax, 0xa0(%rsp)
 295d329:      	cmpl	$0x0, 0xc(%rsp)
 295d32e:      	js	0x295d33d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x545d>
 295d330:      	movl	0xc(%rsp), %eax
 295d334:      	shrl	%eax
 295d336:      	movl	%eax, 0xa4(%rsp)
 295d33d:      	cmpl	$0x0, 0x9c(%rsp)
 295d345:      	js	0x295d357 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5477>
 295d347:      	movl	0x9c(%rsp), %eax
 295d34e:      	shrl	%eax
 295d350:      	movl	%eax, 0xa8(%rsp)
 295d357:      	cmpl	$0x0, 0x18(%rsp)
 295d35c:      	js	0x295d36b <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x548b>
 295d35e:      	movl	0x18(%rsp), %eax
 295d362:      	shrl	%eax
 295d364:      	movl	%eax, 0xac(%rsp)
 295d36b:      	cmpl	$0x0, 0x15c(%rsp)
 295d373:      	js	0x295d385 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54a5>
 295d375:      	movl	0x15c(%rsp), %eax
 295d37c:      	shrl	%eax
 295d37e:      	movl	%eax, 0xb0(%rsp)
 295d385:      	cmpl	$0x0, 0x58(%rsp)
 295d38a:      	js	0x295d399 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54b9>
 295d38c:      	movl	0x58(%rsp), %eax
 295d390:      	shrl	%eax
 295d392:      	movl	%eax, 0xb4(%rsp)
 295d399:      	cmpl	$0x0, 0x154(%rsp)
 295d3a1:      	js	0x295d3b3 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54d3>
 295d3a3:      	movl	0x154(%rsp), %eax
 295d3aa:      	shrl	%eax
 295d3ac:      	movl	%eax, 0xb8(%rsp)
 295d3b3:      	cmpl	$0x0, 0x160(%rsp)
 295d3bb:      	js	0x295d3cd <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x54ed>
 295d3bd:      	movl	0x160(%rsp), %eax
 295d3c4:      	shrl	%eax
 295d3c6:      	movl	%eax, 0xbc(%rsp)
 295d3cd:      	cmpl	$0x0, 0x14c(%rsp)
 295d3d5:      	js	0x295d3e4 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5504>
 295d3d7:      	movl	0x14c(%rsp), %eax
 295d3de:      	shrl	%eax
 295d3e0:      	movl	%eax, 0x30(%rsp)
 295d3e4:      	cmpl	$0x0, 0x158(%rsp)
 295d3ec:      	js	0x295d3fb <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x551b>
 295d3ee:      	movl	0x158(%rsp), %eax
 295d3f5:      	shrl	%eax
 295d3f7:      	movl	%eax, 0x34(%rsp)
 295d3fb:      	cmpl	$0x0, 0x140(%rsp)
 295d403:      	js	0x295d412 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5532>
 295d405:      	movl	0x140(%rsp), %eax
 295d40c:      	shrl	%eax
 295d40e:      	movl	%eax, 0x38(%rsp)
 295d412:      	cmpl	$0x0, 0x150(%rsp)
 295d41a:      	js	0x295d429 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5549>
 295d41c:      	movl	0x150(%rsp), %eax
 295d423:      	shrl	%eax
 295d425:      	movl	%eax, 0x3c(%rsp)
 295d429:      	testl	%r13d, %r13d
 295d42c:      	js	0x295d436 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5556>
 295d42e:      	shrl	%r13d
 295d431:      	movl	%r13d, 0x40(%rsp)
 295d436:      	cmpl	$0x0, 0x148(%rsp)
 295d43e:      	js	0x295d44d <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x556d>
 295d440:      	movl	0x148(%rsp), %eax
 295d447:      	shrl	%eax
 295d449:      	movl	%eax, 0x44(%rsp)
 295d44d:      	testl	%r15d, %r15d
 295d450:      	js	0x295d45a <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x557a>
 295d452:      	shrl	%r15d
 295d455:      	movl	%r15d, 0x48(%rsp)
 295d45a:      	cmpl	$0x0, 0x144(%rsp)
 295d462:      	js	0x295d617 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5737>
 295d468:      	movl	0x144(%rsp), %eax
 295d46f:      	shrl	%eax
 295d471:      	movl	%eax, 0x4c(%rsp)
 295d475:      	jmp	0x295d617 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5737>
 295d47a:      	xorl	%r9d, %r9d
 295d47d:      	subq	$0x20, %rsp
 295d481:      	movups	(%rax), %xmm0
 295d484:      	movups	%xmm0, 0x10(%rsp)
 295d489:      	movdqu	0x80(%rsp), %xmm0
 295d492:      	movdqu	%xmm0, (%rsp)
 295d497:      	movq	0x250(%rsp), %rdi
 295d49f:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295d4a4:      	movq	0x20(%rsp), %rdx
 295d4a9:      	movl	$0x30, %ecx
 295d4ae:      	jmp	0x295bb89 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x3ca9>
 295d4b3:      	movl	0x148(%rbp), %esi
 295d4b9:      	movl	$0x30, %edi
 295d4be:      	movq	0x230(%rsp), %r12
 295d4c6:      	movq	%r12, %rdx
 295d4c9:      	movq	(%rsp), %rcx
 295d4cd:      	callq	0x2842550 <_ZL13getZeroVectorN4llvm3MVTERKNS_12X86SubtargetERNS_12SelectionDAGERKNS_5SDLocE>
 295d4d2:      	movq	%rax, %rbx
 295d4d5:      	movl	%edx, %r15d
 295d4d8:      	movq	%rax, 0x70(%rsp)
 295d4dd:      	movl	%edx, 0x78(%rsp)
 295d4e1:      	movq	%r14, 0x80(%rsp)
 295d4e9:      	movl	0x10(%rsp), %eax
 295d4ed:      	movl	%eax, 0x88(%rsp)
 295d4f4:      	movl	0x28(%rsp), %eax
 295d4f8:      	movl	%eax, 0x8c(%rsp)
 295d4ff:      	movq	0x3b0(%r12), %rax
 295d507:      	xorl	%r13d, %r13d
 295d50a:      	movl	$0x0, %r9d
 295d510:      	testq	%rax, %rax
 295d513:      	je	0x295d519 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5639>
 295d515:      	movl	0x8(%rax), %r9d
 295d519:      	subq	$0x20, %rsp
 295d51d:      	movups	0x90(%rsp), %xmm0
 295d525:      	movups	%xmm0, 0x10(%rsp)
 295d52a:      	movups	0xa0(%rsp), %xmm0
 295d532:      	movups	%xmm0, (%rsp)
 295d536:      	movq	0x250(%rsp), %r12
 295d53e:      	movq	%r12, %rdi
 295d541:      	movl	$0x2c8, %esi            # imm = 0x2C8
 295d546:      	movq	0x20(%rsp), %rdx
 295d54b:      	movl	$0x30, %ecx
 295d550:      	xorl	%r8d, %r8d
 295d553:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d558:      	addq	$0x20, %rsp
 295d55c:      	movl	%edx, %r8d
 295d55f:      	movq	%r12, %rdi
 295d562:      	movl	$0x3e, %esi
 295d567:      	xorl	%edx, %edx
 295d569:      	movq	%rax, %rcx
 295d56c:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d571:      	movq	%rax, 0x180(%rsp)
 295d579:      	movl	%edx, 0x16c(%rsp)
 295d580:      	movq	%rbx, 0x70(%rsp)
 295d585:      	movl	%r15d, 0x78(%rsp)
 295d58a:      	movq	%r14, 0x80(%rsp)
 295d592:      	movl	0x10(%rsp), %eax
 295d596:      	movl	%eax, 0x88(%rsp)
 295d59d:      	movl	0x28(%rsp), %eax
 295d5a1:      	movl	%eax, 0x8c(%rsp)
 295d5a8:      	movq	0x3b0(%r12), %rax
 295d5b0:      	testq	%rax, %rax
 295d5b3:      	je	0x295d5b9 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x56d9>
 295d5b5:      	movl	0x8(%rax), %r13d
 295d5b9:      	subq	$0x20, %rsp
 295d5bd:      	movups	0x90(%rsp), %xmm0
 295d5c5:      	movups	%xmm0, 0x10(%rsp)
 295d5ca:      	movups	0xa0(%rsp), %xmm0
 295d5d2:      	movups	%xmm0, (%rsp)
 295d5d6:      	movq	0x250(%rsp), %rbx
 295d5de:      	movq	%rbx, %rdi
 295d5e1:      	movl	$0x2c9, %esi            # imm = 0x2C9
 295d5e6:      	movq	0x20(%rsp), %rdx
 295d5eb:      	movl	$0x30, %ecx
 295d5f0:      	xorl	%r8d, %r8d
 295d5f3:      	movl	%r13d, %r9d
 295d5f6:      	callq	0x5e27910 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_NS_11SDNodeFlagsE>
 295d5fb:      	addq	$0x20, %rsp
 295d5ff:      	movl	%edx, %r8d
 295d602:      	movq	%rbx, %rdi
 295d605:      	movl	$0x3e, %esi
 295d60a:      	xorl	%edx, %edx
 295d60c:      	movq	%rax, %rcx
 295d60f:      	callq	0x5dfee50 <_ZN4llvm12SelectionDAG10getBitcastENS_3EVTENS_7SDValueE>
 295d614:      	movq	%rax, %rcx
 295d617:      	movq	%rcx, %r15
 295d61a:      	movq	%rcx, 0x188(%rsp)
 295d622:      	movl	%edx, %r13d
 295d625:      	movl	%edx, 0x190(%rsp)
 295d62c:      	leaq	0xa0(%rsp), %rax
 295d634:      	movq	%rax, 0x1c8(%rsp)
 295d63c:      	movq	$0x8, 0x1d0(%rsp)
 295d648:      	subq	$0x20, %rsp
 295d64c:      	movups	0x1e8(%rsp), %xmm0
 295d654:      	movups	%xmm0, 0x10(%rsp)
 295d659:      	movups	0x1a8(%rsp), %xmm0
 295d661:      	movups	%xmm0, (%rsp)
 295d665:      	movq	$0x0, 0x30(%rsp)
 295d66e:      	movq	0x250(%rsp), %rdi
 295d676:      	movl	$0x3e, %esi
 295d67b:      	xorl	%edx, %edx
 295d67d:      	movq	0x20(%rsp), %r14
 295d682:      	movq	%r14, %rcx
 295d685:      	movq	0x1a0(%rsp), %rbp
 295d68d:      	movq	%rbp, %r8
 295d690:      	movl	0x18c(%rsp), %ebx
 295d697:      	movl	%ebx, %r9d
 295d69a:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295d69f:      	addq	$0x20, %rsp
 295d6a3:      	movq	%rax, %r12
 295d6a6:      	movl	%edx, 0x28(%rsp)
 295d6aa:      	movq	%r15, 0x1b8(%rsp)
 295d6b2:      	movl	%r13d, 0x1c0(%rsp)
 295d6ba:      	leaq	0x30(%rsp), %rax
 295d6bf:      	movq	%rax, 0x1a8(%rsp)
 295d6c7:      	movq	$0x8, 0x1b0(%rsp)
 295d6d3:      	subq	$0x20, %rsp
 295d6d7:      	movups	0x1c8(%rsp), %xmm0
 295d6df:      	movups	%xmm0, 0x10(%rsp)
 295d6e4:      	movups	0x1d8(%rsp), %xmm0
 295d6ec:      	movups	%xmm0, (%rsp)
 295d6f0:      	movq	0x250(%rsp), %r15
 295d6f8:      	movq	%r15, %rdi
 295d6fb:      	movl	$0x3e, %esi
 295d700:      	xorl	%edx, %edx
 295d702:      	movq	%r14, %rcx
 295d705:      	movq	%rbp, %r8
 295d708:      	movl	%ebx, %r9d
 295d70b:      	callq	0x5e07800 <_ZN4llvm12SelectionDAG16getVectorShuffleENS_3EVTERKNS_5SDLocENS_7SDValueES5_NS_8ArrayRefIiEE>
 295d710:      	addq	$0x20, %rsp
 295d714:      	movq	%rax, 0x70(%rsp)
 295d719:      	movl	%edx, 0x78(%rsp)
 295d71d:      	movq	%r12, 0x80(%rsp)
 295d725:      	movl	0x28(%rsp), %eax
 295d729:      	movl	%eax, 0x88(%rsp)
 295d730:      	movq	0x3b0(%r15), %rax
 295d737:      	testq	%rax, %rax
 295d73a:      	je	0x295d744 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x5864>
 295d73c:      	movl	0x8(%rax), %eax
 295d73f:      	movq	%rax, 0x10(%rsp)
 295d744:      	subq	$0x20, %rsp
 295d748:      	movups	0x90(%rsp), %xmm0
 295d750:      	movups	%xmm0, 0x10(%rsp)
 295d755:      	movdqu	0xa0(%rsp), %xmm0
 295d75e:      	movdqu	%xmm0, (%rsp)
 295d763:      	movq	0x250(%rsp), %rdi
 295d76b:      	movl	$0x2b6, %esi            # imm = 0x2B6
 295d770:      	movq	0x20(%rsp), %rdx
 295d775:      	movl	$0x30, %ecx
 295d77a:      	xorl	%r8d, %r8d
 295d77d:      	movq	0x30(%rsp), %r9
 295d782:      	jmp	0x2959c77 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1d97>
 295d787:      	xorl	%r9d, %r9d
 295d78a:      	subq	$0x30, %rsp
 295d78e:      	movups	0xd0(%rsp), %xmm0
 295d796:      	movups	%xmm0, 0x20(%rsp)
 295d79b:      	leaq	0x240(%rsp), %rax
 295d7a3:      	movups	(%rax), %xmm0
 295d7a6:      	movups	%xmm0, 0x10(%rsp)
 295d7ab:      	movdqu	0x90(%rsp), %xmm0
 295d7b4:      	movdqu	%xmm0, (%rsp)
 295d7b9:      	movq	0x260(%rsp), %rdi
 295d7c1:      	movl	$0x2eb, %esi            # imm = 0x2EB
 295d7c6:      	movq	0x30(%rsp), %rdx
 295d7cb:      	movl	$0x30, %ecx
 295d7d0:      	xorl	%r8d, %r8d
 295d7d3:      	callq	0x5e2ac90 <_ZN4llvm12SelectionDAG7getNodeEjRKNS_5SDLocENS_3EVTENS_7SDValueES5_S5_NS_11SDNodeFlagsE>
 295d7d8:      	addq	$0x30, %rsp
 295d7dc:      	movq	%rax, %rbx
 295d7df:      	movl	%edx, %r14d
 295d7e2:      	movq	%rbx, %rax
 295d7e5:      	movl	%r14d, %r8d
 295d7e8:      	jmp	0x2959c83 <_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE+0x1da3>
