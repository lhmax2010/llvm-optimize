
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000054d2940 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_>:
 54d2940:      	pushq	%rbp
 54d2941:      	pushq	%r15
 54d2943:      	pushq	%r14
 54d2945:      	pushq	%r13
 54d2947:      	pushq	%r12
 54d2949:      	pushq	%rbx
 54d294a:      	subq	$0x118, %rsp            # imm = 0x118
 54d2951:      	movq	%rdi, 0x40(%rsp)
 54d2956:      	testl	%esi, %esi
 54d2958:      	je	0x54d2a8e <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x14e>
 54d295e:      	movq	%rdx, %r12
 54d2961:      	movl	%esi, %r13d
 54d2964:      	movq	%rcx, 0x20(%rsp)
 54d2969:      	leaq	0x58(%rsp), %r15
 54d296e:      	movq	%r15, 0x48(%rsp)
 54d2973:      	movq	$-0x1, 0x58(%rsp)
 54d297c:      	movabsq	$0x600000001, %rbx      # imm = 0x600000001
 54d2986:      	movq	%rbx, 0x50(%rsp)
 54d298b:      	movq	$-0x1000, 0x90(%rsp)    # imm = 0xF000
 54d2997:      	leaq	0x98(%rsp), %rdi
 54d299f:      	leaq	0xa8(%rsp), %rax
 54d29a7:      	movq	%rax, 0x98(%rsp)
 54d29af:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 54d29b9:      	movq	%r14, 0xa0(%rsp)
 54d29c1:      	leaq	0x48(%rsp), %rsi
 54d29c6:      	callq	0x54d25a0 <_ZN4llvm15SmallVectorImplIPNS_9sandboxir5ValueEEaSEOS4_>
 54d29cb:      	movq	0x48(%rsp), %rdi
 54d29d0:      	cmpq	%r15, %rdi
 54d29d3:      	je	0x54d29da <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x9a>
 54d29d5:      	callq	0x828a640 <free@plt>
 54d29da:      	leaq	0xe8(%rsp), %r15
 54d29e2:      	movq	%r15, 0xd8(%rsp)
 54d29ea:      	movq	$-0x2, 0xe8(%rsp)
 54d29f6:      	movq	%rbx, 0xe0(%rsp)
 54d29fe:      	movq	$-0x2000, 0x48(%rsp)    # imm = 0xE000
 54d2a07:      	leaq	0x50(%rsp), %rdi
 54d2a0c:      	leaq	0x60(%rsp), %rax
 54d2a11:      	movq	%rax, 0x50(%rsp)
 54d2a16:      	movq	%r14, 0x58(%rsp)
 54d2a1b:      	leaq	0xd8(%rsp), %rsi
 54d2a23:      	callq	0x54d25a0 <_ZN4llvm15SmallVectorImplIPNS_9sandboxir5ValueEEaSEOS4_>
 54d2a28:      	movq	0xd8(%rsp), %rdi
 54d2a30:      	cmpq	%r15, %rdi
 54d2a33:      	je	0x54d2a3a <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0xfa>
 54d2a35:      	callq	0x828a640 <free@plt>
 54d2a3a:      	movabsq	$-0xae502812ab8d92, %r8 # imm = 0xFF51AFD7ED54726E
 54d2a44:      	movq	(%r12), %rcx
 54d2a48:      	movq	0x8(%r12), %rdi
 54d2a4d:      	movl	%ecx, %eax
 54d2a4f:      	shrl	$0x4, %eax
 54d2a52:      	movl	%ecx, %ebx
 54d2a54:      	shrl	$0x9, %ebx
 54d2a57:      	xorl	%eax, %ebx
 54d2a59:      	movl	0x10(%r12), %eax
 54d2a5e:      	leaq	(,%rax,8), %rsi
 54d2a66:      	cmpq	$0x8, %rax
 54d2a6a:      	ja	0x54d2a9c <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x15c>
 54d2a6c:      	addq	$0x11a5f, %r8           # imm = 0x11A5F
 54d2a73:      	movq	%r8, %rdx
 54d2a76:      	callq	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 54d2a7b:      	movq	(%r12), %rdx
 54d2a7f:      	movq	0x8(%r12), %rdi
 54d2a84:      	movl	0x10(%r12), %r11d
 54d2a89:      	jmp	0x54d2e51 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x511>
 54d2a8e:      	movq	$0x0, (%rcx)
 54d2a95:      	xorl	%ebx, %ebx
 54d2a97:      	jmp	0x54d2ff8 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6b8>
 54d2a9c:      	movq	%rbx, 0x38(%rsp)
 54d2aa1:      	movq	%rax, 0x8(%rsp)
 54d2aa6:      	movq	%rcx, 0x28(%rsp)
 54d2aab:      	movl	%r13d, 0x4(%rsp)
 54d2ab0:      	movabsq	$-0x4b6d499041670d8d, %r11 # imm = 0xB492B66FBE98F273
 54d2aba:      	movabsq	$0x544962662a7ee1a4, %rax # imm = 0x544962662A7EE1A4
 54d2ac4:      	movq	%rsi, %rbx
 54d2ac7:      	andq	$-0x40, %rbx
 54d2acb:      	movq	0x8(%rdi), %r13
 54d2acf:      	movq	0x10(%rdi), %rcx
 54d2ad3:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 54d2add:      	addq	%r13, %rdx
 54d2ae0:      	rolq	$0x1b, %rdx
 54d2ae4:      	imulq	%r11, %rdx
 54d2ae8:      	movq	0x30(%rdi), %r9
 54d2aec:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 54d2af6:      	addq	%r9, %r10
 54d2af9:      	rolq	$0x16, %r10
 54d2afd:      	imulq	%r11, %r10
 54d2b01:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 54d2b0b:      	xorq	%rdx, %rbp
 54d2b0e:      	movq	0x28(%rdi), %r12
 54d2b12:      	movq	%rdi, %rsi
 54d2b15:      	movabsq	$-0x7323d61940a0da1f, %rdi # imm = 0x8CDC29E6BF5F25E1
 54d2b1f:      	addq	%r12, %rdi
 54d2b22:      	addq	%r10, %rdi
 54d2b25:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 54d2b2f:      	addq	(%rsi), %r10
 54d2b32:      	movq	0x18(%rsi), %r11
 54d2b36:      	addq	%r10, %r8
 54d2b39:      	addq	%r11, %r8
 54d2b3c:      	addq	%rbp, %r8
 54d2b3f:      	rolq	$0x2b, %r8
 54d2b43:      	addq	%rcx, %r13
 54d2b46:      	addq	%r10, %r13
 54d2b49:      	movq	%r13, %rdx
 54d2b4c:      	rolq	$0x14, %rdx
 54d2b50:      	addq	%r10, %rdx
 54d2b53:      	addq	%r8, %rdx
 54d2b56:      	movabsq	$0x4bf62cb950c3753a, %r8 # imm = 0x4BF62CB950C3753A
 54d2b60:      	addq	0x20(%rsi), %r8
 54d2b64:      	addq	%r11, %r13
 54d2b67:      	movq	%rsi, 0x30(%rsp)
 54d2b6c:      	movq	0x38(%rsi), %r10
 54d2b70:      	addq	%r8, %rcx
 54d2b73:      	addq	%r10, %rcx
 54d2b76:      	addq	%rdi, %rcx
 54d2b79:      	rolq	$0x2b, %rcx
 54d2b7d:      	addq	%r9, %r12
 54d2b80:      	addq	%r8, %r12
 54d2b83:      	movq	%r12, %r9
 54d2b86:      	rolq	$0x14, %r9
 54d2b8a:      	addq	%r8, %r9
 54d2b8d:      	addq	%rcx, %r9
 54d2b90:      	addq	%r10, %r12
 54d2b93:      	movq	%rbx, 0x10(%rsp)
 54d2b98:      	cmpq	$0x40, %rbx
 54d2b9c:      	jne	0x54d2bb2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x272>
 54d2b9e:      	movq	%r9, %rcx
 54d2ba1:      	movq	%r12, %r8
 54d2ba4:      	movq	%rdx, %r14
 54d2ba7:      	movq	%r13, %r10
 54d2baa:      	movq	%rbp, %rsi
 54d2bad:      	jmp	0x54d2c9d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x35d>
 54d2bb2:      	addq	$-0x40, 0x10(%rsp)
 54d2bb8:      	xorl	%ebx, %ebx
 54d2bba:      	movq	0x30(%rsp), %r11
 54d2bbf:      	nop
 54d2bc0:      	addq	%rdi, %rax
 54d2bc3:      	addq	%r13, %rax
 54d2bc6:      	movq	0x48(%r11,%rbx), %r10
 54d2bcb:      	movq	0x50(%r11,%rbx), %r15
 54d2bd0:      	addq	%r10, %rax
 54d2bd3:      	rolq	$0x1b, %rax
 54d2bd7:      	movabsq	$-0x4b6d499041670d8d, %rcx # imm = 0xB492B66FBE98F273
 54d2be1:      	imulq	%rcx, %rax
 54d2be5:      	addq	%rdx, %rdi
 54d2be8:      	movq	0x70(%r11,%rbx), %rsi
 54d2bed:      	movq	%rsi, 0x18(%rsp)
 54d2bf2:      	addq	%rsi, %rdi
 54d2bf5:      	rolq	$0x16, %rdi
 54d2bf9:      	imulq	%rcx, %rdi
 54d2bfd:      	movq	%rax, %rsi
 54d2c00:      	xorq	%r9, %rsi
 54d2c03:      	movq	0x68(%r11,%rbx), %r8
 54d2c08:      	addq	%r8, %r13
 54d2c0b:      	addq	%r12, %rbp
 54d2c0e:      	rolq	$0x1f, %rbp
 54d2c12:      	addq	%r13, %rdi
 54d2c15:      	imulq	%rcx, %rdx
 54d2c19:      	addq	0x40(%r11,%rbx), %rdx
 54d2c1e:      	movq	%rbp, %rax
 54d2c21:      	movq	0x58(%r11,%rbx), %r13
 54d2c26:      	addq	%rdx, %r12
 54d2c29:      	addq	%r13, %r12
 54d2c2c:      	addq	%rsi, %r12
 54d2c2f:      	rolq	$0x2b, %r12
 54d2c33:      	addq	%r15, %r10
 54d2c36:      	addq	%rdx, %r10
 54d2c39:      	movq	%r10, %r14
 54d2c3c:      	rolq	$0x14, %r14
 54d2c40:      	imulq	%rcx, %rax
 54d2c44:      	addq	%rdx, %r14
 54d2c47:      	addq	%r12, %r14
 54d2c4a:      	addq	%rax, %r9
 54d2c4d:      	addq	%rdi, %r15
 54d2c50:      	addq	0x60(%r11,%rbx), %r9
 54d2c55:      	movq	0x78(%r11,%rbx), %rdx
 54d2c5a:      	addq	%r9, %r15
 54d2c5d:      	addq	%rdx, %r15
 54d2c60:      	rolq	$0x2b, %r15
 54d2c64:      	addq	%r13, %r10
 54d2c67:      	addq	0x18(%rsp), %r8
 54d2c6c:      	addq	%r9, %r8
 54d2c6f:      	movq	%r8, %rcx
 54d2c72:      	rolq	$0x14, %rcx
 54d2c76:      	addq	%r9, %rcx
 54d2c79:      	addq	%r15, %rcx
 54d2c7c:      	addq	%rdx, %r8
 54d2c7f:      	addq	$0x40, %rbx
 54d2c83:      	movq	%rsi, %rbp
 54d2c86:      	movq	%r10, %r13
 54d2c89:      	movq	%r14, %rdx
 54d2c8c:      	movq	%r8, %r12
 54d2c8f:      	movq	%rcx, %r9
 54d2c92:      	cmpq	%rbx, 0x10(%rsp)
 54d2c97:      	jne	0x54d2bc0 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x280>
 54d2c9d:      	movq	0x8(%rsp), %r11
 54d2ca2:      	testb	$0x7, %r11b
 54d2ca6:      	je	0x54d2d98 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x458>
 54d2cac:      	movq	0x30(%rsp), %r13
 54d2cb1:      	movq	-0x38(%r13,%r11,8), %rdx
 54d2cb6:      	movq	-0x30(%r13,%r11,8), %r12
 54d2cbb:      	addq	%rdx, %rax
 54d2cbe:      	addq	%rdi, %rax
 54d2cc1:      	addq	%r10, %rax
 54d2cc4:      	rolq	$0x1b, %rax
 54d2cc8:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 54d2cd2:      	imulq	%rbp, %rax
 54d2cd6:      	addq	%r14, %rdi
 54d2cd9:      	movq	-0x10(%r13,%r11,8), %rbx
 54d2cde:      	addq	%rbx, %rdi
 54d2ce1:      	rolq	$0x16, %rdi
 54d2ce5:      	imulq	%rbp, %rdi
 54d2ce9:      	xorq	%rcx, %rax
 54d2cec:      	movq	-0x18(%r13,%r11,8), %r9
 54d2cf1:      	addq	%r9, %r10
 54d2cf4:      	addq	%r10, %rdi
 54d2cf7:      	addq	%r8, %rsi
 54d2cfa:      	rolq	$0x1f, %rsi
 54d2cfe:      	movq	%rsi, %r15
 54d2d01:      	imulq	%rbp, %r14
 54d2d05:      	addq	%rax, %r8
 54d2d08:      	addq	-0x40(%r13,%r11,8), %r14
 54d2d0d:      	movq	0x8(%rsp), %rsi
 54d2d12:      	movq	-0x28(%r13,%rsi,8), %r11
 54d2d17:      	addq	%r11, %r8
 54d2d1a:      	addq	%r14, %r8
 54d2d1d:      	rolq	$0x2b, %r8
 54d2d21:      	imulq	%rbp, %r15
 54d2d25:      	addq	%r12, %rdx
 54d2d28:      	addq	%r14, %rdx
 54d2d2b:      	movq	%rdx, %r10
 54d2d2e:      	rolq	$0x14, %r10
 54d2d32:      	addq	%r14, %r10
 54d2d35:      	addq	%r8, %r10
 54d2d38:      	addq	%r11, %rdx
 54d2d3b:      	addq	%r15, %rcx
 54d2d3e:      	movq	0x8(%rsp), %rsi
 54d2d43:      	addq	-0x20(%r13,%rsi,8), %rcx
 54d2d48:      	addq	%rdi, %r12
 54d2d4b:      	movq	0x8(%rsp), %rsi
 54d2d50:      	movq	-0x8(%r13,%rsi,8), %r8
 54d2d55:      	addq	%r8, %r12
 54d2d58:      	addq	%rcx, %r12
 54d2d5b:      	rolq	$0x2b, %r12
 54d2d5f:      	addq	%rbx, %r9
 54d2d62:      	addq	%rcx, %r9
 54d2d65:      	movq	%r9, %r11
 54d2d68:      	rolq	$0x14, %r11
 54d2d6c:      	addq	%rcx, %r11
 54d2d6f:      	addq	%r12, %r11
 54d2d72:      	addq	%r8, %r9
 54d2d75:      	movq	%r11, %rcx
 54d2d78:      	movq	0x8(%rsp), %r11
 54d2d7d:      	movq	%r9, %r8
 54d2d80:      	movq	%r10, %r14
 54d2d83:      	movq	%rdx, %r10
 54d2d86:      	movq	%rax, %rsi
 54d2d89:      	movq	%r15, %rax
 54d2d8c:      	movl	0x4(%rsp), %r13d
 54d2d91:      	movq	0x38(%rsp), %rbx
 54d2d96:      	jmp	0x54d2dac <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x46c>
 54d2d98:      	movl	0x4(%rsp), %r13d
 54d2d9d:      	movq	0x38(%rsp), %rbx
 54d2da2:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 54d2dac:      	xorq	%r8, %r10
 54d2daf:      	movabsq	$-0x622015f714c7d297, %rdx # imm = 0x9DDFEA08EB382D69
 54d2db9:      	imulq	%rdx, %r10
 54d2dbd:      	xorq	%r10, %r8
 54d2dc0:      	shrq	$0x2f, %r10
 54d2dc4:      	xorq	%r8, %r10
 54d2dc7:      	imulq	%rdx, %r10
 54d2dcb:      	movq	%r10, %r8
 54d2dce:      	shrq	$0x2f, %r8
 54d2dd2:      	xorq	%r10, %r8
 54d2dd5:      	imulq	%rdx, %r8
 54d2dd9:      	movq	%rdi, %r9
 54d2ddc:      	shrq	$0x2f, %r9
 54d2de0:      	xorq	%rdi, %r9
 54d2de3:      	imulq	%rbp, %r9
 54d2de7:      	addq	%rsi, %r9
 54d2dea:      	addq	%r8, %r9
 54d2ded:      	xorq	%rcx, %r14
 54d2df0:      	imulq	%rdx, %r14
 54d2df4:      	xorq	%r14, %rcx
 54d2df7:      	shrq	$0x2f, %r14
 54d2dfb:      	xorq	%rcx, %r14
 54d2dfe:      	imulq	%rdx, %r14
 54d2e02:      	movq	%r14, %rcx
 54d2e05:      	shrq	$0x2f, %rcx
 54d2e09:      	xorq	%r14, %rcx
 54d2e0c:      	imulq	%rdx, %rcx
 54d2e10:      	movabsq	$-0x5b6a4c820b386c68, %rdi # imm = 0xA495B37DF4C79398
 54d2e1a:      	imulq	%r11, %rdi
 54d2e1e:      	addq	%rax, %rdi
 54d2e21:      	addq	%rcx, %rdi
 54d2e24:      	xorq	%rdi, %r9
 54d2e27:      	imulq	%rdx, %r9
 54d2e2b:      	xorq	%r9, %rdi
 54d2e2e:      	shrq	$0x2f, %r9
 54d2e32:      	xorq	%rdi, %r9
 54d2e35:      	imulq	%rdx, %r9
 54d2e39:      	movq	%r9, %rax
 54d2e3c:      	shrq	$0x2f, %rax
 54d2e40:      	xorq	%r9, %rax
 54d2e43:      	imulq	%rdx, %rax
 54d2e47:      	movq	0x28(%rsp), %rdx
 54d2e4c:      	movq	0x30(%rsp), %rdi
 54d2e51:      	shlq	$0x20, %rbx
 54d2e55:      	movl	%eax, %eax
 54d2e57:      	orq	%rbx, %rax
 54d2e5a:      	movabsq	$-0x40a7b892e31b1a47, %rcx # imm = 0xBF58476D1CE4E5B9
 54d2e64:      	imulq	%rax, %rcx
 54d2e68:      	movq	%rcx, %rbp
 54d2e6b:      	shrq	$0x1f, %rbp
 54d2e6f:      	xorl	%ecx, %ebp
 54d2e71:      	decl	%r13d
 54d2e74:      	movl	%r13d, 0x4(%rsp)
 54d2e79:      	andl	%r13d, %ebp
 54d2e7c:      	testl	%r11d, %r11d
 54d2e7f:      	je	0x54d2f46 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x606>
 54d2e85:      	movl	%r11d, %r13d
 54d2e88:      	shlq	$0x3, %r13
 54d2e8c:      	movl	$0x1, 0x10(%rsp)
 54d2e94:      	movq	$0x0, 0x18(%rsp)
 54d2e9d:      	movl	%ebp, %eax
 54d2e9f:      	imulq	$0x98, %rax, %rax
 54d2ea6:      	movq	0x40(%rsp), %rcx
 54d2eab:      	leaq	(%rcx,%rax), %r12
 54d2eaf:      	movq	%rdx, %r15
 54d2eb2:      	cmpq	(%rcx,%rax), %rdx
 54d2eb6:      	jne	0x54d2ee2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x5a2>
 54d2eb8:      	cmpl	0x10(%r12), %r11d
 54d2ebd:      	jne	0x54d2ee2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x5a2>
 54d2ebf:      	movq	0x8(%r12), %rsi
 54d2ec4:      	movq	%rdi, %rbx
 54d2ec7:      	movq	%r13, %rdx
 54d2eca:      	movq	%r11, %r14
 54d2ecd:      	callq	0x828a6c0 <bcmp@plt>
 54d2ed2:      	movq	%r14, %r11
 54d2ed5:      	movq	%rbx, %rdi
 54d2ed8:      	movb	$0x1, %bl
 54d2eda:      	testl	%eax, %eax
 54d2edc:      	je	0x54d2fc2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x682>
 54d2ee2:      	movq	%r11, 0x8(%rsp)
 54d2ee7:      	movq	%rdi, %rbx
 54d2eea:      	movq	%r12, %rdi
 54d2eed:      	leaq	0x90(%rsp), %rsi
 54d2ef5:      	callq	0x54d2900 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2efa:      	testb	%al, %al
 54d2efc:      	jne	0x54d300c <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6cc>
 54d2f02:      	movq	%r12, %rdi
 54d2f05:      	leaq	0x48(%rsp), %rsi
 54d2f0a:      	callq	0x54d2900 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2f0f:      	movq	0x18(%rsp), %rcx
 54d2f14:      	testq	%rcx, %rcx
 54d2f17:      	cmovneq	%rcx, %r12
 54d2f1b:      	testb	%al, %al
 54d2f1d:      	cmovneq	%r12, %rcx
 54d2f21:      	movq	%rcx, 0x18(%rsp)
 54d2f26:      	movl	0x10(%rsp), %eax
 54d2f2a:      	addl	%eax, %ebp
 54d2f2c:      	incl	%eax
 54d2f2e:      	movl	%eax, 0x10(%rsp)
 54d2f32:      	andl	0x4(%rsp), %ebp
 54d2f36:      	movq	%r15, %rdx
 54d2f39:      	movq	%rbx, %rdi
 54d2f3c:      	movq	0x8(%rsp), %r11
 54d2f41:      	jmp	0x54d2e9d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x55d>
 54d2f46:      	movl	$0x1, %r14d
 54d2f4c:      	xorl	%r15d, %r15d
 54d2f4f:      	leaq	0x90(%rsp), %rsi
 54d2f57:      	leaq	0x48(%rsp), %r13
 54d2f5c:      	movl	%ebp, %eax
 54d2f5e:      	imulq	$0x98, %rax, %rax
 54d2f65:      	movq	0x40(%rsp), %rcx
 54d2f6a:      	leaq	(%rcx,%rax), %r12
 54d2f6e:      	cmpq	(%rcx,%rax), %rdx
 54d2f72:      	jne	0x54d2f7e <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x63e>
 54d2f74:      	movb	$0x1, %bl
 54d2f76:      	cmpl	$0x0, 0x10(%r12)
 54d2f7c:      	je	0x54d2fc2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x682>
 54d2f7e:      	movq	%rdx, 0x28(%rsp)
 54d2f83:      	movq	%r12, %rdi
 54d2f86:      	movq	%rsi, %rbx
 54d2f89:      	callq	0x54d2900 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2f8e:      	testb	%al, %al
 54d2f90:      	jne	0x54d3018 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6d8>
 54d2f96:      	movq	%r12, %rdi
 54d2f99:      	movq	%r13, %rsi
 54d2f9c:      	callq	0x54d2900 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2fa1:      	testq	%r15, %r15
 54d2fa4:      	cmovneq	%r15, %r12
 54d2fa8:      	testb	%al, %al
 54d2faa:      	cmovneq	%r12, %r15
 54d2fae:      	addl	%r14d, %ebp
 54d2fb1:      	incl	%r14d
 54d2fb4:      	andl	0x4(%rsp), %ebp
 54d2fb8:      	movq	0x28(%rsp), %rdx
 54d2fbd:      	movq	%rbx, %rsi
 54d2fc0:      	jmp	0x54d2f5c <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x61c>
 54d2fc2:      	movq	0x20(%rsp), %rax
 54d2fc7:      	movq	%r12, (%rax)
 54d2fca:      	movq	0x50(%rsp), %rdi
 54d2fcf:      	leaq	0x60(%rsp), %rax
 54d2fd4:      	cmpq	%rax, %rdi
 54d2fd7:      	je	0x54d2fde <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x69e>
 54d2fd9:      	callq	0x828a640 <free@plt>
 54d2fde:      	movq	0x98(%rsp), %rdi
 54d2fe6:      	leaq	0xa8(%rsp), %rax
 54d2fee:      	cmpq	%rax, %rdi
 54d2ff1:      	je	0x54d2ff8 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6b8>
 54d2ff3:      	callq	0x828a640 <free@plt>
 54d2ff8:      	movl	%ebx, %eax
 54d2ffa:      	addq	$0x118, %rsp            # imm = 0x118
 54d3001:      	popq	%rbx
 54d3002:      	popq	%r12
 54d3004:      	popq	%r13
 54d3006:      	popq	%r14
 54d3008:      	popq	%r15
 54d300a:      	popq	%rbp
 54d300b:      	retq
 54d300c:      	movq	0x20(%rsp), %rax
 54d3011:      	movq	0x18(%rsp), %r15
 54d3016:      	jmp	0x54d301d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6dd>
 54d3018:      	movq	0x20(%rsp), %rax
 54d301d:      	testq	%r15, %r15
 54d3020:      	cmovneq	%r15, %r12
 54d3024:      	xorl	%ebx, %ebx
 54d3026:      	jmp	0x54d2fc7 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x687>
