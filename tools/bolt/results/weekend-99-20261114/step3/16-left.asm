
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000054d29d0 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_>:
 54d29d0:      	pushq	%rbp
 54d29d1:      	pushq	%r15
 54d29d3:      	pushq	%r14
 54d29d5:      	pushq	%r13
 54d29d7:      	pushq	%r12
 54d29d9:      	pushq	%rbx
 54d29da:      	subq	$0x118, %rsp            # imm = 0x118
 54d29e1:      	movq	%rdi, 0x40(%rsp)
 54d29e6:      	testl	%esi, %esi
 54d29e8:      	je	0x54d2b1e <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x14e>
 54d29ee:      	movq	%rdx, %r12
 54d29f1:      	movl	%esi, %r13d
 54d29f4:      	movq	%rcx, 0x20(%rsp)
 54d29f9:      	leaq	0x58(%rsp), %r15
 54d29fe:      	movq	%r15, 0x48(%rsp)
 54d2a03:      	movq	$-0x1, 0x58(%rsp)
 54d2a0c:      	movabsq	$0x600000001, %rbx      # imm = 0x600000001
 54d2a16:      	movq	%rbx, 0x50(%rsp)
 54d2a1b:      	movq	$-0x1000, 0x90(%rsp)    # imm = 0xF000
 54d2a27:      	leaq	0x98(%rsp), %rdi
 54d2a2f:      	leaq	0xa8(%rsp), %rax
 54d2a37:      	movq	%rax, 0x98(%rsp)
 54d2a3f:      	movabsq	$0x600000000, %r14      # imm = 0x600000000
 54d2a49:      	movq	%r14, 0xa0(%rsp)
 54d2a51:      	leaq	0x48(%rsp), %rsi
 54d2a56:      	callq	0x54d2630 <_ZN4llvm15SmallVectorImplIPNS_9sandboxir5ValueEEaSEOS4_>
 54d2a5b:      	movq	0x48(%rsp), %rdi
 54d2a60:      	cmpq	%r15, %rdi
 54d2a63:      	je	0x54d2a6a <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x9a>
 54d2a65:      	callq	0x828a6d0 <free@plt>
 54d2a6a:      	leaq	0xe8(%rsp), %r15
 54d2a72:      	movq	%r15, 0xd8(%rsp)
 54d2a7a:      	movq	$-0x2, 0xe8(%rsp)
 54d2a86:      	movq	%rbx, 0xe0(%rsp)
 54d2a8e:      	movq	$-0x2000, 0x48(%rsp)    # imm = 0xE000
 54d2a97:      	leaq	0x50(%rsp), %rdi
 54d2a9c:      	leaq	0x60(%rsp), %rax
 54d2aa1:      	movq	%rax, 0x50(%rsp)
 54d2aa6:      	movq	%r14, 0x58(%rsp)
 54d2aab:      	leaq	0xd8(%rsp), %rsi
 54d2ab3:      	callq	0x54d2630 <_ZN4llvm15SmallVectorImplIPNS_9sandboxir5ValueEEaSEOS4_>
 54d2ab8:      	movq	0xd8(%rsp), %rdi
 54d2ac0:      	cmpq	%r15, %rdi
 54d2ac3:      	je	0x54d2aca <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0xfa>
 54d2ac5:      	callq	0x828a6d0 <free@plt>
 54d2aca:      	movabsq	$-0xae502812ab8d92, %r8 # imm = 0xFF51AFD7ED54726E
 54d2ad4:      	movq	(%r12), %rcx
 54d2ad8:      	movq	0x8(%r12), %rdi
 54d2add:      	movl	%ecx, %eax
 54d2adf:      	shrl	$0x4, %eax
 54d2ae2:      	movl	%ecx, %ebx
 54d2ae4:      	shrl	$0x9, %ebx
 54d2ae7:      	xorl	%eax, %ebx
 54d2ae9:      	movl	0x10(%r12), %eax
 54d2aee:      	leaq	(,%rax,8), %rsi
 54d2af6:      	cmpq	$0x8, %rax
 54d2afa:      	ja	0x54d2b2c <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x15c>
 54d2afc:      	addq	$0x11a5f, %r8           # imm = 0x11A5F
 54d2b03:      	movq	%r8, %rdx
 54d2b06:      	callq	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 54d2b0b:      	movq	(%r12), %rdx
 54d2b0f:      	movq	0x8(%r12), %rdi
 54d2b14:      	movl	0x10(%r12), %r11d
 54d2b19:      	jmp	0x54d2ee2 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x512>
 54d2b1e:      	movq	$0x0, (%rcx)
 54d2b25:      	xorl	%ebx, %ebx
 54d2b27:      	jmp	0x54d3089 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6b9>
 54d2b2c:      	movq	%rbx, 0x38(%rsp)
 54d2b31:      	movq	%rax, 0x8(%rsp)
 54d2b36:      	movq	%rcx, 0x28(%rsp)
 54d2b3b:      	movl	%r13d, 0x4(%rsp)
 54d2b40:      	movabsq	$-0x4b6d499041670d8d, %r11 # imm = 0xB492B66FBE98F273
 54d2b4a:      	movabsq	$0x544962662a7ee1a4, %rax # imm = 0x544962662A7EE1A4
 54d2b54:      	movq	%rsi, %rbx
 54d2b57:      	andq	$-0x40, %rbx
 54d2b5b:      	movq	0x8(%rdi), %r13
 54d2b5f:      	movq	0x10(%rdi), %rcx
 54d2b63:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 54d2b6d:      	addq	%r13, %rdx
 54d2b70:      	rolq	$0x1b, %rdx
 54d2b74:      	imulq	%r11, %rdx
 54d2b78:      	movq	0x30(%rdi), %r9
 54d2b7c:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 54d2b86:      	addq	%r9, %r10
 54d2b89:      	rolq	$0x16, %r10
 54d2b8d:      	imulq	%r11, %r10
 54d2b91:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 54d2b9b:      	xorq	%rdx, %rbp
 54d2b9e:      	movq	0x28(%rdi), %r12
 54d2ba2:      	movq	%rdi, %rsi
 54d2ba5:      	movabsq	$-0x7323d61940a0da1f, %rdi # imm = 0x8CDC29E6BF5F25E1
 54d2baf:      	addq	%r12, %rdi
 54d2bb2:      	addq	%r10, %rdi
 54d2bb5:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 54d2bbf:      	addq	(%rsi), %r10
 54d2bc2:      	movq	0x18(%rsi), %r11
 54d2bc6:      	addq	%r10, %r8
 54d2bc9:      	addq	%r11, %r8
 54d2bcc:      	addq	%rbp, %r8
 54d2bcf:      	rolq	$0x2b, %r8
 54d2bd3:      	addq	%rcx, %r13
 54d2bd6:      	addq	%r10, %r13
 54d2bd9:      	movq	%r13, %rdx
 54d2bdc:      	rolq	$0x14, %rdx
 54d2be0:      	addq	%r10, %rdx
 54d2be3:      	addq	%r8, %rdx
 54d2be6:      	movabsq	$0x4bf62cb950c3753a, %r8 # imm = 0x4BF62CB950C3753A
 54d2bf0:      	addq	0x20(%rsi), %r8
 54d2bf4:      	addq	%r11, %r13
 54d2bf7:      	movq	%rsi, 0x30(%rsp)
 54d2bfc:      	movq	0x38(%rsi), %r10
 54d2c00:      	addq	%r8, %rcx
 54d2c03:      	addq	%r10, %rcx
 54d2c06:      	addq	%rdi, %rcx
 54d2c09:      	rolq	$0x2b, %rcx
 54d2c0d:      	addq	%r9, %r12
 54d2c10:      	addq	%r8, %r12
 54d2c13:      	movq	%r12, %r9
 54d2c16:      	rolq	$0x14, %r9
 54d2c1a:      	addq	%r8, %r9
 54d2c1d:      	addq	%rcx, %r9
 54d2c20:      	addq	%r10, %r12
 54d2c23:      	movq	%rbx, 0x10(%rsp)
 54d2c28:      	cmpq	$0x40, %rbx
 54d2c2c:      	jne	0x54d2c42 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x272>
 54d2c2e:      	movq	%r9, %rcx
 54d2c31:      	movq	%r12, %r8
 54d2c34:      	movq	%rdx, %r14
 54d2c37:      	movq	%r13, %r10
 54d2c3a:      	movq	%rbp, %rsi
 54d2c3d:      	jmp	0x54d2d2d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x35d>
 54d2c42:      	addq	$-0x40, 0x10(%rsp)
 54d2c48:      	xorl	%ebx, %ebx
 54d2c4a:      	movq	0x30(%rsp), %r11
 54d2c4f:      	nop
 54d2c50:      	addq	%rdi, %rax
 54d2c53:      	addq	%r13, %rax
 54d2c56:      	movq	0x48(%r11,%rbx), %r10
 54d2c5b:      	movq	0x50(%r11,%rbx), %r15
 54d2c60:      	addq	%r10, %rax
 54d2c63:      	rolq	$0x1b, %rax
 54d2c67:      	movabsq	$-0x4b6d499041670d8d, %rcx # imm = 0xB492B66FBE98F273
 54d2c71:      	imulq	%rcx, %rax
 54d2c75:      	addq	%rdx, %rdi
 54d2c78:      	movq	0x70(%r11,%rbx), %rsi
 54d2c7d:      	movq	%rsi, 0x18(%rsp)
 54d2c82:      	addq	%rsi, %rdi
 54d2c85:      	rolq	$0x16, %rdi
 54d2c89:      	imulq	%rcx, %rdi
 54d2c8d:      	movq	%rax, %rsi
 54d2c90:      	xorq	%r9, %rsi
 54d2c93:      	movq	0x68(%r11,%rbx), %r8
 54d2c98:      	addq	%r8, %r13
 54d2c9b:      	addq	%r12, %rbp
 54d2c9e:      	rolq	$0x1f, %rbp
 54d2ca2:      	addq	%r13, %rdi
 54d2ca5:      	imulq	%rcx, %rdx
 54d2ca9:      	addq	0x40(%r11,%rbx), %rdx
 54d2cae:      	movq	%rbp, %rax
 54d2cb1:      	movq	0x58(%r11,%rbx), %r13
 54d2cb6:      	addq	%rdx, %r12
 54d2cb9:      	addq	%r13, %r12
 54d2cbc:      	addq	%rsi, %r12
 54d2cbf:      	rolq	$0x2b, %r12
 54d2cc3:      	addq	%r15, %r10
 54d2cc6:      	addq	%rdx, %r10
 54d2cc9:      	movq	%r10, %r14
 54d2ccc:      	rolq	$0x14, %r14
 54d2cd0:      	imulq	%rcx, %rax
 54d2cd4:      	addq	%rdx, %r14
 54d2cd7:      	addq	%r12, %r14
 54d2cda:      	addq	%rax, %r9
 54d2cdd:      	addq	%rdi, %r15
 54d2ce0:      	addq	0x60(%r11,%rbx), %r9
 54d2ce5:      	movq	0x78(%r11,%rbx), %rdx
 54d2cea:      	addq	%r9, %r15
 54d2ced:      	addq	%rdx, %r15
 54d2cf0:      	rolq	$0x2b, %r15
 54d2cf4:      	addq	%r13, %r10
 54d2cf7:      	addq	0x18(%rsp), %r8
 54d2cfc:      	addq	%r9, %r8
 54d2cff:      	movq	%r8, %rcx
 54d2d02:      	rolq	$0x14, %rcx
 54d2d06:      	addq	%r9, %rcx
 54d2d09:      	addq	%r15, %rcx
 54d2d0c:      	addq	%rdx, %r8
 54d2d0f:      	addq	$0x40, %rbx
 54d2d13:      	movq	%rsi, %rbp
 54d2d16:      	movq	%r10, %r13
 54d2d19:      	movq	%r14, %rdx
 54d2d1c:      	movq	%r8, %r12
 54d2d1f:      	movq	%rcx, %r9
 54d2d22:      	cmpq	%rbx, 0x10(%rsp)
 54d2d27:      	jne	0x54d2c50 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x280>
 54d2d2d:      	movq	0x8(%rsp), %r11
 54d2d32:      	testb	$0x7, %r11b
 54d2d36:      	je	0x54d2e29 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x459>
 54d2d3c:      	leaq	(%rdi,%r10), %r9
 54d2d40:      	movq	0x30(%rsp), %r13
 54d2d45:      	movq	-0x38(%r13,%r11,8), %rdx
 54d2d4a:      	movq	-0x30(%r13,%r11,8), %r12
 54d2d4f:      	addq	%rdx, %rax
 54d2d52:      	addq	%r9, %rax
 54d2d55:      	rolq	$0x1b, %rax
 54d2d59:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 54d2d63:      	imulq	%rbp, %rax
 54d2d67:      	addq	%r14, %rdi
 54d2d6a:      	movq	-0x10(%r13,%r11,8), %rbx
 54d2d6f:      	addq	%rbx, %rdi
 54d2d72:      	rolq	$0x16, %rdi
 54d2d76:      	imulq	%rbp, %rdi
 54d2d7a:      	xorq	%rcx, %rax
 54d2d7d:      	movq	-0x18(%r13,%r11,8), %r9
 54d2d82:      	addq	%r9, %r10
 54d2d85:      	addq	%r10, %rdi
 54d2d88:      	addq	%r8, %rsi
 54d2d8b:      	rolq	$0x1f, %rsi
 54d2d8f:      	movq	%rsi, %r15
 54d2d92:      	imulq	%rbp, %r14
 54d2d96:      	addq	%rax, %r8
 54d2d99:      	addq	-0x40(%r13,%r11,8), %r14
 54d2d9e:      	movq	0x8(%rsp), %rsi
 54d2da3:      	movq	-0x28(%r13,%rsi,8), %r11
 54d2da8:      	addq	%r11, %r8
 54d2dab:      	addq	%r14, %r8
 54d2dae:      	rolq	$0x2b, %r8
 54d2db2:      	imulq	%rbp, %r15
 54d2db6:      	addq	%r12, %rdx
 54d2db9:      	addq	%r14, %rdx
 54d2dbc:      	movq	%rdx, %r10
 54d2dbf:      	rolq	$0x14, %r10
 54d2dc3:      	addq	%r14, %r10
 54d2dc6:      	addq	%r8, %r10
 54d2dc9:      	addq	%r11, %rdx
 54d2dcc:      	addq	%r15, %rcx
 54d2dcf:      	movq	0x8(%rsp), %rsi
 54d2dd4:      	addq	-0x20(%r13,%rsi,8), %rcx
 54d2dd9:      	addq	%rdi, %r12
 54d2ddc:      	movq	0x8(%rsp), %rsi
 54d2de1:      	movq	-0x8(%r13,%rsi,8), %r8
 54d2de6:      	addq	%r8, %r12
 54d2de9:      	addq	%rcx, %r12
 54d2dec:      	rolq	$0x2b, %r12
 54d2df0:      	addq	%rbx, %r9
 54d2df3:      	addq	%rcx, %r9
 54d2df6:      	movq	%r9, %r11
 54d2df9:      	rolq	$0x14, %r11
 54d2dfd:      	addq	%rcx, %r11
 54d2e00:      	addq	%r12, %r11
 54d2e03:      	addq	%r8, %r9
 54d2e06:      	movq	%r11, %rcx
 54d2e09:      	movq	0x8(%rsp), %r11
 54d2e0e:      	movq	%r9, %r8
 54d2e11:      	movq	%r10, %r14
 54d2e14:      	movq	%rdx, %r10
 54d2e17:      	movq	%rax, %rsi
 54d2e1a:      	movq	%r15, %rax
 54d2e1d:      	movl	0x4(%rsp), %r13d
 54d2e22:      	movq	0x38(%rsp), %rbx
 54d2e27:      	jmp	0x54d2e3d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x46d>
 54d2e29:      	movl	0x4(%rsp), %r13d
 54d2e2e:      	movq	0x38(%rsp), %rbx
 54d2e33:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 54d2e3d:      	xorq	%r8, %r10
 54d2e40:      	movabsq	$-0x622015f714c7d297, %rdx # imm = 0x9DDFEA08EB382D69
 54d2e4a:      	imulq	%rdx, %r10
 54d2e4e:      	xorq	%r10, %r8
 54d2e51:      	shrq	$0x2f, %r10
 54d2e55:      	xorq	%r8, %r10
 54d2e58:      	imulq	%rdx, %r10
 54d2e5c:      	movq	%r10, %r8
 54d2e5f:      	shrq	$0x2f, %r8
 54d2e63:      	xorq	%r10, %r8
 54d2e66:      	imulq	%rdx, %r8
 54d2e6a:      	movq	%rdi, %r9
 54d2e6d:      	shrq	$0x2f, %r9
 54d2e71:      	xorq	%rdi, %r9
 54d2e74:      	imulq	%rbp, %r9
 54d2e78:      	addq	%rsi, %r9
 54d2e7b:      	addq	%r8, %r9
 54d2e7e:      	xorq	%rcx, %r14
 54d2e81:      	imulq	%rdx, %r14
 54d2e85:      	xorq	%r14, %rcx
 54d2e88:      	shrq	$0x2f, %r14
 54d2e8c:      	xorq	%rcx, %r14
 54d2e8f:      	imulq	%rdx, %r14
 54d2e93:      	movq	%r14, %rcx
 54d2e96:      	shrq	$0x2f, %rcx
 54d2e9a:      	xorq	%r14, %rcx
 54d2e9d:      	imulq	%rdx, %rcx
 54d2ea1:      	movabsq	$-0x5b6a4c820b386c68, %rdi # imm = 0xA495B37DF4C79398
 54d2eab:      	imulq	%r11, %rdi
 54d2eaf:      	addq	%rax, %rdi
 54d2eb2:      	addq	%rcx, %rdi
 54d2eb5:      	xorq	%rdi, %r9
 54d2eb8:      	imulq	%rdx, %r9
 54d2ebc:      	xorq	%r9, %rdi
 54d2ebf:      	shrq	$0x2f, %r9
 54d2ec3:      	xorq	%rdi, %r9
 54d2ec6:      	imulq	%rdx, %r9
 54d2eca:      	movq	%r9, %rax
 54d2ecd:      	shrq	$0x2f, %rax
 54d2ed1:      	xorq	%r9, %rax
 54d2ed4:      	imulq	%rdx, %rax
 54d2ed8:      	movq	0x28(%rsp), %rdx
 54d2edd:      	movq	0x30(%rsp), %rdi
 54d2ee2:      	shlq	$0x20, %rbx
 54d2ee6:      	movl	%eax, %eax
 54d2ee8:      	orq	%rbx, %rax
 54d2eeb:      	movabsq	$-0x40a7b892e31b1a47, %rcx # imm = 0xBF58476D1CE4E5B9
 54d2ef5:      	imulq	%rax, %rcx
 54d2ef9:      	movq	%rcx, %rbp
 54d2efc:      	shrq	$0x1f, %rbp
 54d2f00:      	xorl	%ecx, %ebp
 54d2f02:      	decl	%r13d
 54d2f05:      	movl	%r13d, 0x4(%rsp)
 54d2f0a:      	andl	%r13d, %ebp
 54d2f0d:      	testl	%r11d, %r11d
 54d2f10:      	je	0x54d2fd7 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x607>
 54d2f16:      	movl	%r11d, %r13d
 54d2f19:      	shlq	$0x3, %r13
 54d2f1d:      	movl	$0x1, 0x10(%rsp)
 54d2f25:      	movq	$0x0, 0x18(%rsp)
 54d2f2e:      	movl	%ebp, %eax
 54d2f30:      	imulq	$0x98, %rax, %rax
 54d2f37:      	movq	0x40(%rsp), %rcx
 54d2f3c:      	leaq	(%rcx,%rax), %r12
 54d2f40:      	movq	%rdx, %r15
 54d2f43:      	cmpq	(%rcx,%rax), %rdx
 54d2f47:      	jne	0x54d2f73 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x5a3>
 54d2f49:      	cmpl	0x10(%r12), %r11d
 54d2f4e:      	jne	0x54d2f73 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x5a3>
 54d2f50:      	movq	0x8(%r12), %rsi
 54d2f55:      	movq	%rdi, %rbx
 54d2f58:      	movq	%r13, %rdx
 54d2f5b:      	movq	%r11, %r14
 54d2f5e:      	callq	0x828a750 <bcmp@plt>
 54d2f63:      	movq	%r14, %r11
 54d2f66:      	movq	%rbx, %rdi
 54d2f69:      	movb	$0x1, %bl
 54d2f6b:      	testl	%eax, %eax
 54d2f6d:      	je	0x54d3053 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x683>
 54d2f73:      	movq	%r11, 0x8(%rsp)
 54d2f78:      	movq	%rdi, %rbx
 54d2f7b:      	movq	%r12, %rdi
 54d2f7e:      	leaq	0x90(%rsp), %rsi
 54d2f86:      	callq	0x54d2990 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2f8b:      	testb	%al, %al
 54d2f8d:      	jne	0x54d309d <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6cd>
 54d2f93:      	movq	%r12, %rdi
 54d2f96:      	leaq	0x48(%rsp), %rsi
 54d2f9b:      	callq	0x54d2990 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d2fa0:      	movq	0x18(%rsp), %rcx
 54d2fa5:      	testq	%rcx, %rcx
 54d2fa8:      	cmovneq	%rcx, %r12
 54d2fac:      	testb	%al, %al
 54d2fae:      	cmovneq	%r12, %rcx
 54d2fb2:      	movq	%rcx, 0x18(%rsp)
 54d2fb7:      	movl	0x10(%rsp), %eax
 54d2fbb:      	addl	%eax, %ebp
 54d2fbd:      	incl	%eax
 54d2fbf:      	movl	%eax, 0x10(%rsp)
 54d2fc3:      	andl	0x4(%rsp), %ebp
 54d2fc7:      	movq	%r15, %rdx
 54d2fca:      	movq	%rbx, %rdi
 54d2fcd:      	movq	0x8(%rsp), %r11
 54d2fd2:      	jmp	0x54d2f2e <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x55e>
 54d2fd7:      	movl	$0x1, %r14d
 54d2fdd:      	xorl	%r15d, %r15d
 54d2fe0:      	leaq	0x90(%rsp), %rsi
 54d2fe8:      	leaq	0x48(%rsp), %r13
 54d2fed:      	movl	%ebp, %eax
 54d2fef:      	imulq	$0x98, %rax, %rax
 54d2ff6:      	movq	0x40(%rsp), %rcx
 54d2ffb:      	leaq	(%rcx,%rax), %r12
 54d2fff:      	cmpq	(%rcx,%rax), %rdx
 54d3003:      	jne	0x54d300f <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x63f>
 54d3005:      	movb	$0x1, %bl
 54d3007:      	cmpl	$0x0, 0x10(%r12)
 54d300d:      	je	0x54d3053 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x683>
 54d300f:      	movq	%rdx, 0x28(%rsp)
 54d3014:      	movq	%r12, %rdi
 54d3017:      	movq	%rsi, %rbx
 54d301a:      	callq	0x54d2990 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d301f:      	testb	%al, %al
 54d3021:      	jne	0x54d30a9 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6d9>
 54d3027:      	movq	%r12, %rdi
 54d302a:      	movq	%r13, %rsi
 54d302d:      	callq	0x54d2990 <_ZN4llvm12DenseMapInfoISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS2_5ValueELj6EEEEvE7isEqualERKS9_SC_>
 54d3032:      	testq	%r15, %r15
 54d3035:      	cmovneq	%r15, %r12
 54d3039:      	testb	%al, %al
 54d303b:      	cmovneq	%r12, %r15
 54d303f:      	addl	%r14d, %ebp
 54d3042:      	incl	%r14d
 54d3045:      	andl	0x4(%rsp), %ebp
 54d3049:      	movq	0x28(%rsp), %rdx
 54d304e:      	movq	%rbx, %rsi
 54d3051:      	jmp	0x54d2fed <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x61d>
 54d3053:      	movq	0x20(%rsp), %rax
 54d3058:      	movq	%r12, (%rax)
 54d305b:      	movq	0x50(%rsp), %rdi
 54d3060:      	leaq	0x60(%rsp), %rax
 54d3065:      	cmpq	%rax, %rdi
 54d3068:      	je	0x54d306f <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x69f>
 54d306a:      	callq	0x828a6d0 <free@plt>
 54d306f:      	movq	0x98(%rsp), %rdi
 54d3077:      	leaq	0xa8(%rsp), %rax
 54d307f:      	cmpq	%rax, %rdi
 54d3082:      	je	0x54d3089 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6b9>
 54d3084:      	callq	0x828a6d0 <free@plt>
 54d3089:      	movl	%ebx, %eax
 54d308b:      	addq	$0x118, %rsp            # imm = 0x118
 54d3092:      	popq	%rbx
 54d3093:      	popq	%r12
 54d3095:      	popq	%r13
 54d3097:      	popq	%r14
 54d3099:      	popq	%r15
 54d309b:      	popq	%rbp
 54d309c:      	retq
 54d309d:      	movq	0x20(%rsp), %rax
 54d30a2:      	movq	0x18(%rsp), %r15
 54d30a7:      	jmp	0x54d30ae <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x6de>
 54d30a9:      	movq	0x20(%rsp), %rax
 54d30ae:      	testq	%r15, %r15
 54d30b1:      	cmovneq	%r15, %r12
 54d30b5:      	xorl	%ebx, %ebx
 54d30b7:      	jmp	0x54d3058 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_9sandboxir10BasicBlockENS_11SmallVectorIPNS3_5ValueELj6EEEENS6_INS6_IPNS3_11InstructionELj6EEELj1EEENS_12DenseMapInfoISA_vEENS_6detail12DenseMapPairISA_SE_EEEESA_SE_SG_SJ_E15LookupBucketForISA_EEbRKT_RPSJ_+0x688>
