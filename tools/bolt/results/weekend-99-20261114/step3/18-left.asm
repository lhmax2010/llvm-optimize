
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004302ac0 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_>:
 4302ac0:      	pushq	%rbp
 4302ac1:      	pushq	%r15
 4302ac3:      	pushq	%r14
 4302ac5:      	pushq	%r13
 4302ac7:      	pushq	%r12
 4302ac9:      	pushq	%rbx
 4302aca:      	subq	$0x68, %rsp
 4302ace:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 4302ad8:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302ae2:      	movq	(%rdi), %rax
 4302ae5:      	movq	0x30(%rax), %rax
 4302ae9:      	movq	-0x38(%rax), %rax
 4302aed:      	movq	%rax, 0x10(%rsp)
 4302af2:      	leaq	0x38(%rsp), %r12
 4302af7:      	movq	%r12, 0x28(%rsp)
 4302afc:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 4302b06:      	movq	%rcx, 0x30(%rsp)
 4302b0b:      	leaq	0x30(%rax), %rcx
 4302b0f:      	cmpq	0x30(%rax), %rcx
 4302b13:      	je	0x4302b96 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xd6>
 4302b19:      	movq	0x38(%rax), %r15
 4302b1d:      	cmpb	$0x55, -0x18(%r15)
 4302b22:      	jne	0x4302b96 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xd6>
 4302b24:      	movq	%rdi, %r14
 4302b27:      	addq	$-0x18, %r15
 4302b2b:      	leaq	0x10(%rsp), %r12
 4302b30:      	leaq	0x28(%rsp), %rbx
 4302b35:      	nopw	%cs:(%rax,%rax)
 4302b3f:      	nop
 4302b40:      	movq	0x8(%r14), %rdi
 4302b44:      	movq	%r15, %rsi
 4302b47:      	callq	0x4302800 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_13SmallDenseMapIPNS_10BasicBlockEPNS_5ValueELj8ENS_12DenseMapInfoIS6_vEENS_6detail12DenseMapPairIS6_S8_EEEENS9_IS3_vEENSC_IS3_SE_EEEES3_SE_SF_SG_E24lookupOrInsertIntoBucketIS3_JEEESt4pairIPSG_bEOT_DpOT0_>
 4302b4c:      	leaq	0x8(%rax), %rdi
 4302b50:      	movq	%r12, %rsi
 4302b53:      	callq	0x4302980 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPNS_10BasicBlockEPNS_5ValueELj8ENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S5_EEEES3_S5_S7_SA_E24lookupOrInsertIntoBucketIRKS3_JEEESt4pairIPSA_bEOT_DpOT0_>
 4302b58:      	addq	$0x8, %rax
 4302b5c:      	movl	0x30(%rsp), %ecx
 4302b60:      	cmpl	0x34(%rsp), %ecx
 4302b64:      	jae	0x4302b89 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xc9>
 4302b66:      	movq	0x28(%rsp), %rdx
 4302b6b:      	movq	(%rax), %rax
 4302b6e:      	movq	%rax, (%rdx,%rcx,8)
 4302b72:      	leal	0x1(%rcx), %eax
 4302b75:      	movl	%eax, 0x30(%rsp)
 4302b79:      	movq	0x20(%r15), %rax
 4302b7d:      	leaq	-0x18(%rax), %r15
 4302b81:      	cmpb	$0x55, -0x18(%rax)
 4302b85:      	je	0x4302b40 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x80>
 4302b87:      	jmp	0x4302bfd <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x13d>
 4302b89:      	movq	%rbx, %rdi
 4302b8c:      	movq	%rax, %rsi
 4302b8f:      	callq	0x3dae740 <_ZN4llvm23SmallVectorTemplateBaseIPNS_5ValueELb1EE18growAndEmplaceBackIJRS2_EEES5_DpOT_>
 4302b94:      	jmp	0x4302b79 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xb9>
 4302b96:      	xorl	%esi, %esi
 4302b98:      	movq	%r12, %rdi
 4302b9b:      	movq	%rbp, %rdx
 4302b9e:      	callq	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 4302ba3:      	movq	0x28(%rsp), %rdi
 4302ba8:      	movq	0x10(%rsp), %rbx
 4302bad:      	cmpq	%r12, %rdi
 4302bb0:      	je	0x4302bbd <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xfd>
 4302bb2:      	movq	%rax, %r14
 4302bb5:      	callq	0x828a6d0 <free@plt>
 4302bba:      	movq	%r14, %rax
 4302bbd:      	leaq	0x10(%rax), %rcx
 4302bc1:      	rolq	$0x30, %rcx
 4302bc5:      	xorq	%rcx, %rbx
 4302bc8:      	xorq	%rbp, %rbx
 4302bcb:      	imulq	%r13, %rbx
 4302bcf:      	xorq	%rbx, %rcx
 4302bd2:      	shrq	$0x2f, %rbx
 4302bd6:      	xorq	%rcx, %rbx
 4302bd9:      	imulq	%r13, %rbx
 4302bdd:      	movq	%rbx, %rcx
 4302be0:      	shrq	$0x2f, %rcx
 4302be4:      	xorl	%ebx, %ecx
 4302be6:      	imull	$0xeb382d69, %ecx, %ecx # imm = 0xEB382D69
 4302bec:      	xorl	%ecx, %eax
 4302bee:      	addq	$0x68, %rsp
 4302bf2:      	popq	%rbx
 4302bf3:      	popq	%r12
 4302bf5:      	popq	%r13
 4302bf7:      	popq	%r14
 4302bf9:      	popq	%r15
 4302bfb:      	popq	%rbp
 4302bfc:      	retq
 4302bfd:      	movq	0x28(%rsp), %rdi
 4302c02:      	movl	0x30(%rsp), %eax
 4302c06:      	leaq	(,%rax,8), %rsi
 4302c0e:      	cmpq	$0x8, %rax
 4302c12:      	ja	0x4302c1b <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x15b>
 4302c14:      	leaq	0x38(%rsp), %r12
 4302c19:      	jmp	0x4302b9b <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xdb>
 4302c1b:      	movq	%rax, (%rsp)
 4302c1f:      	movabsq	$-0x4b6d499041670d8d, %r8 # imm = 0xB492B66FBE98F273
 4302c29:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 4302c33:      	andq	$-0x40, %rsi
 4302c37:      	movq	0x8(%rdi), %rbx
 4302c3b:      	movq	0x10(%rdi), %rax
 4302c3f:      	movabsq	$-0x73d22641534b4d52, %r10 # imm = 0x8C2DD9BEACB4B2AE
 4302c49:      	addq	%rbx, %r10
 4302c4c:      	rolq	$0x1b, %r10
 4302c50:      	imulq	%r8, %r10
 4302c54:      	movq	0x30(%rdi), %rdx
 4302c58:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 4302c62:      	addq	%rdx, %r9
 4302c65:      	rolq	$0x16, %r9
 4302c69:      	imulq	%r8, %r9
 4302c6d:      	movabsq	$-0x85335acd9bb6c6a, %r15 # imm = 0xF7ACCA5326449396
 4302c77:      	xorq	%r10, %r15
 4302c7a:      	movq	0x28(%rdi), %r12
 4302c7e:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 4302c88:      	addq	%r12, %r8
 4302c8b:      	addq	%r9, %r8
 4302c8e:      	movabsq	$0x298df016a9f64655, %r14 # imm = 0x298DF016A9F64655
 4302c98:      	addq	(%rdi), %r14
 4302c9b:      	leaq	(%rbp,%r14), %r9
 4302ca0:      	addq	%r15, %r9
 4302ca3:      	movq	0x18(%rdi), %r10
 4302ca7:      	leaq	-0x11a5f(%r10,%r9), %r11
 4302caf:      	rolq	$0x2b, %r11
 4302cb3:      	addq	%rax, %rbx
 4302cb6:      	addq	%r14, %rbx
 4302cb9:      	movq	%rbx, %r9
 4302cbc:      	rolq	$0x14, %r9
 4302cc0:      	addq	%r14, %r9
 4302cc3:      	addq	%r11, %r9
 4302cc6:      	movabsq	$0x4bf62cb950c3753a, %r14 # imm = 0x4BF62CB950C3753A
 4302cd0:      	addq	0x20(%rdi), %r14
 4302cd4:      	addq	%r10, %rbx
 4302cd7:      	movq	%rdi, 0x8(%rsp)
 4302cdc:      	movq	0x38(%rdi), %r10
 4302ce0:      	addq	%r14, %rax
 4302ce3:      	addq	%r10, %rax
 4302ce6:      	addq	%r8, %rax
 4302ce9:      	rolq	$0x2b, %rax
 4302ced:      	addq	%rdx, %r12
 4302cf0:      	addq	%r14, %r12
 4302cf3:      	movq	%r12, %r11
 4302cf6:      	rolq	$0x14, %r11
 4302cfa:      	addq	%r14, %r11
 4302cfd:      	addq	%rax, %r11
 4302d00:      	addq	%r10, %r12
 4302d03:      	cmpq	$0x40, %rsi
 4302d07:      	jne	0x4302d1d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x25d>
 4302d09:      	movq	%r11, %rdx
 4302d0c:      	movq	%r12, %r10
 4302d0f:      	movq	%r9, %rbp
 4302d12:      	movq	%rbx, %r14
 4302d15:      	movq	%r15, %rsi
 4302d18:      	jmp	0x4302e0d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x34d>
 4302d1d:      	addq	$-0x40, %rsi
 4302d21:      	movq	%rsi, 0x18(%rsp)
 4302d26:      	xorl	%eax, %eax
 4302d28:      	movq	0x8(%rsp), %rdi
 4302d2d:      	nopl	(%rax)
 4302d30:      	addq	%r8, %rcx
 4302d33:      	addq	%rbx, %rcx
 4302d36:      	movq	0x48(%rdi,%rax), %r14
 4302d3b:      	movq	0x50(%rdi,%rax), %r13
 4302d40:      	addq	%r14, %rcx
 4302d43:      	rolq	$0x1b, %rcx
 4302d47:      	movabsq	$-0x4b6d499041670d8d, %rdx # imm = 0xB492B66FBE98F273
 4302d51:      	imulq	%rdx, %rcx
 4302d55:      	addq	%r9, %r8
 4302d58:      	movq	0x70(%rdi,%rax), %rsi
 4302d5d:      	movq	%rsi, 0x20(%rsp)
 4302d62:      	addq	%rsi, %r8
 4302d65:      	rolq	$0x16, %r8
 4302d69:      	imulq	%rdx, %r8
 4302d6d:      	movq	%rcx, %rsi
 4302d70:      	xorq	%r11, %rsi
 4302d73:      	movq	0x68(%rdi,%rax), %r10
 4302d78:      	addq	%r10, %rbx
 4302d7b:      	addq	%r12, %r15
 4302d7e:      	rolq	$0x1f, %r15
 4302d82:      	addq	%rbx, %r8
 4302d85:      	imulq	%rdx, %r9
 4302d89:      	addq	0x40(%rdi,%rax), %r9
 4302d8e:      	movq	%r15, %rcx
 4302d91:      	movq	0x58(%rdi,%rax), %rbx
 4302d96:      	addq	%r9, %r12
 4302d99:      	addq	%rbx, %r12
 4302d9c:      	addq	%rsi, %r12
 4302d9f:      	rolq	$0x2b, %r12
 4302da3:      	addq	%r13, %r14
 4302da6:      	addq	%r9, %r14
 4302da9:      	movq	%r14, %rbp
 4302dac:      	rolq	$0x14, %rbp
 4302db0:      	imulq	%rdx, %rcx
 4302db4:      	addq	%r9, %rbp
 4302db7:      	addq	%r12, %rbp
 4302dba:      	addq	%rcx, %r11
 4302dbd:      	addq	%r8, %r13
 4302dc0:      	addq	0x60(%rdi,%rax), %r11
 4302dc5:      	movq	0x78(%rdi,%rax), %r9
 4302dca:      	addq	%r11, %r13
 4302dcd:      	addq	%r9, %r13
 4302dd0:      	rolq	$0x2b, %r13
 4302dd4:      	addq	%rbx, %r14
 4302dd7:      	addq	0x20(%rsp), %r10
 4302ddc:      	addq	%r11, %r10
 4302ddf:      	movq	%r10, %rdx
 4302de2:      	rolq	$0x14, %rdx
 4302de6:      	addq	%r11, %rdx
 4302de9:      	addq	%r13, %rdx
 4302dec:      	addq	%r9, %r10
 4302def:      	addq	$0x40, %rax
 4302df3:      	movq	%rsi, %r15
 4302df6:      	movq	%r14, %rbx
 4302df9:      	movq	%rbp, %r9
 4302dfc:      	movq	%r10, %r12
 4302dff:      	movq	%rdx, %r11
 4302e02:      	cmpq	%rax, 0x18(%rsp)
 4302e07:      	jne	0x4302d30 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x270>
 4302e0d:      	movq	(%rsp), %rbx
 4302e11:      	testb	$0x7, %bl
 4302e14:      	je	0x4302f17 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x457>
 4302e1a:      	leaq	(%r8,%r14), %r11
 4302e1e:      	movq	0x8(%rsp), %rdi
 4302e23:      	movq	-0x38(%rdi,%rbx,8), %rax
 4302e28:      	movq	-0x30(%rdi,%rbx,8), %r9
 4302e2d:      	addq	%rax, %rcx
 4302e30:      	addq	%r11, %rcx
 4302e33:      	rolq	$0x1b, %rcx
 4302e37:      	movabsq	$-0x4b6d499041670d8d, %r12 # imm = 0xB492B66FBE98F273
 4302e41:      	imulq	%r12, %rcx
 4302e45:      	addq	%rbp, %r8
 4302e48:      	movq	(%rsp), %r11
 4302e4c:      	movq	-0x10(%rdi,%r11,8), %rbx
 4302e51:      	addq	%rbx, %r8
 4302e54:      	rolq	$0x16, %r8
 4302e58:      	imulq	%r12, %r8
 4302e5c:      	xorq	%rdx, %rcx
 4302e5f:      	movq	(%rsp), %r11
 4302e63:      	movq	-0x18(%rdi,%r11,8), %r11
 4302e68:      	addq	%r11, %r14
 4302e6b:      	addq	%r14, %r8
 4302e6e:      	addq	%r10, %rsi
 4302e71:      	rolq	$0x1f, %rsi
 4302e75:      	movq	%rsi, %r15
 4302e78:      	imulq	%r12, %rbp
 4302e7c:      	addq	%rcx, %r10
 4302e7f:      	movq	(%rsp), %rsi
 4302e83:      	addq	-0x40(%rdi,%rsi,8), %rbp
 4302e88:      	movq	(%rsp), %rsi
 4302e8c:      	movq	-0x28(%rdi,%rsi,8), %r14
 4302e91:      	addq	%r14, %r10
 4302e94:      	addq	%rbp, %r10
 4302e97:      	rolq	$0x2b, %r10
 4302e9b:      	imulq	%r12, %r15
 4302e9f:      	addq	%r9, %rax
 4302ea2:      	addq	%rbp, %rax
 4302ea5:      	movq	%rax, %rsi
 4302ea8:      	rolq	$0x14, %rsi
 4302eac:      	addq	%rbp, %rsi
 4302eaf:      	addq	%r10, %rsi
 4302eb2:      	addq	%r14, %rax
 4302eb5:      	addq	%r15, %rdx
 4302eb8:      	movq	(%rsp), %r10
 4302ebc:      	addq	-0x20(%rdi,%r10,8), %rdx
 4302ec1:      	addq	%r8, %r9
 4302ec4:      	movq	(%rsp), %r10
 4302ec8:      	movq	-0x8(%rdi,%r10,8), %r10
 4302ecd:      	addq	%r10, %r9
 4302ed0:      	addq	%rdx, %r9
 4302ed3:      	rolq	$0x2b, %r9
 4302ed7:      	addq	%rbx, %r11
 4302eda:      	addq	%rdx, %r11
 4302edd:      	movq	%r11, %rbx
 4302ee0:      	rolq	$0x14, %rbx
 4302ee4:      	addq	%rdx, %rbx
 4302ee7:      	addq	%r9, %rbx
 4302eea:      	addq	%r10, %r11
 4302eed:      	movq	%rbx, %rdx
 4302ef0:      	movq	(%rsp), %rbx
 4302ef4:      	movq	%r11, %r10
 4302ef7:      	movq	%rsi, %rbp
 4302efa:      	movq	%rax, %r14
 4302efd:      	movq	%rcx, %rsi
 4302f00:      	movq	%r15, %rcx
 4302f03:      	movq	%r12, %r11
 4302f06:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302f10:      	leaq	0x38(%rsp), %r12
 4302f15:      	jmp	0x4302f30 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x470>
 4302f17:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302f21:      	leaq	0x38(%rsp), %r12
 4302f26:      	movabsq	$-0x4b6d499041670d8d, %r11 # imm = 0xB492B66FBE98F273
 4302f30:      	xorq	%r10, %r14
 4302f33:      	imulq	%r13, %r14
 4302f37:      	xorq	%r14, %r10
 4302f3a:      	shrq	$0x2f, %r14
 4302f3e:      	xorq	%r10, %r14
 4302f41:      	imulq	%r13, %r14
 4302f45:      	movq	%r14, %rax
 4302f48:      	shrq	$0x2f, %rax
 4302f4c:      	xorq	%r14, %rax
 4302f4f:      	imulq	%r13, %rax
 4302f53:      	movq	%r8, %r9
 4302f56:      	shrq	$0x2f, %r9
 4302f5a:      	xorq	%r8, %r9
 4302f5d:      	imulq	%r11, %r9
 4302f61:      	addq	%rsi, %r9
 4302f64:      	addq	%rax, %r9
 4302f67:      	xorq	%rdx, %rbp
 4302f6a:      	imulq	%r13, %rbp
 4302f6e:      	xorq	%rbp, %rdx
 4302f71:      	shrq	$0x2f, %rbp
 4302f75:      	xorq	%rdx, %rbp
 4302f78:      	imulq	%r13, %rbp
 4302f7c:      	movq	%rbp, %rax
 4302f7f:      	shrq	$0x2f, %rax
 4302f83:      	xorq	%rbp, %rax
 4302f86:      	imulq	%r13, %rax
 4302f8a:      	movabsq	$-0x5b6a4c820b386c68, %rdx # imm = 0xA495B37DF4C79398
 4302f94:      	imulq	%rdx, %rbx
 4302f98:      	addq	%rcx, %rbx
 4302f9b:      	addq	%rax, %rbx
 4302f9e:      	xorq	%rbx, %r9
 4302fa1:      	imulq	%r13, %r9
 4302fa5:      	xorq	%r9, %rbx
 4302fa8:      	shrq	$0x2f, %r9
 4302fac:      	xorq	%rbx, %r9
 4302faf:      	imulq	%r13, %r9
 4302fb3:      	movq	%r9, %rax
 4302fb6:      	shrq	$0x2f, %rax
 4302fba:      	xorq	%r9, %rax
 4302fbd:      	imulq	%r13, %rax
 4302fc1:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 4302fcb:      	movq	0x8(%rsp), %rdi
 4302fd0:      	movq	0x10(%rsp), %rbx
 4302fd5:      	cmpq	%r12, %rdi
 4302fd8:      	jne	0x4302bb2 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xf2>
 4302fde:      	jmp	0x4302bbd <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xfd>
