
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004302a30 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_>:
 4302a30:      	pushq	%rbp
 4302a31:      	pushq	%r15
 4302a33:      	pushq	%r14
 4302a35:      	pushq	%r13
 4302a37:      	pushq	%r12
 4302a39:      	pushq	%rbx
 4302a3a:      	subq	$0x68, %rsp
 4302a3e:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 4302a48:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302a52:      	movq	(%rdi), %rax
 4302a55:      	movq	0x30(%rax), %rax
 4302a59:      	movq	-0x38(%rax), %rax
 4302a5d:      	movq	%rax, 0x10(%rsp)
 4302a62:      	leaq	0x38(%rsp), %r12
 4302a67:      	movq	%r12, 0x28(%rsp)
 4302a6c:      	movabsq	$0x600000000, %rcx      # imm = 0x600000000
 4302a76:      	movq	%rcx, 0x30(%rsp)
 4302a7b:      	leaq	0x30(%rax), %rcx
 4302a7f:      	cmpq	0x30(%rax), %rcx
 4302a83:      	je	0x4302b06 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xd6>
 4302a89:      	movq	0x38(%rax), %r15
 4302a8d:      	cmpb	$0x55, -0x18(%r15)
 4302a92:      	jne	0x4302b06 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xd6>
 4302a94:      	movq	%rdi, %r14
 4302a97:      	addq	$-0x18, %r15
 4302a9b:      	leaq	0x10(%rsp), %r12
 4302aa0:      	leaq	0x28(%rsp), %rbx
 4302aa5:      	nopw	%cs:(%rax,%rax)
 4302aaf:      	nop
 4302ab0:      	movq	0x8(%r14), %rdi
 4302ab4:      	movq	%r15, %rsi
 4302ab7:      	callq	0x4302770 <_ZN4llvm12DenseMapBaseINS_8DenseMapIPNS_7PHINodeENS_13SmallDenseMapIPNS_10BasicBlockEPNS_5ValueELj8ENS_12DenseMapInfoIS6_vEENS_6detail12DenseMapPairIS6_S8_EEEENS9_IS3_vEENSC_IS3_SE_EEEES3_SE_SF_SG_E24lookupOrInsertIntoBucketIS3_JEEESt4pairIPSG_bEOT_DpOT0_>
 4302abc:      	leaq	0x8(%rax), %rdi
 4302ac0:      	movq	%r12, %rsi
 4302ac3:      	callq	0x43028f0 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPNS_10BasicBlockEPNS_5ValueELj8ENS_12DenseMapInfoIS3_vEENS_6detail12DenseMapPairIS3_S5_EEEES3_S5_S7_SA_E24lookupOrInsertIntoBucketIRKS3_JEEESt4pairIPSA_bEOT_DpOT0_>
 4302ac8:      	addq	$0x8, %rax
 4302acc:      	movl	0x30(%rsp), %ecx
 4302ad0:      	cmpl	0x34(%rsp), %ecx
 4302ad4:      	jae	0x4302af9 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xc9>
 4302ad6:      	movq	0x28(%rsp), %rdx
 4302adb:      	movq	(%rax), %rax
 4302ade:      	movq	%rax, (%rdx,%rcx,8)
 4302ae2:      	leal	0x1(%rcx), %eax
 4302ae5:      	movl	%eax, 0x30(%rsp)
 4302ae9:      	movq	0x20(%r15), %rax
 4302aed:      	leaq	-0x18(%rax), %r15
 4302af1:      	cmpb	$0x55, -0x18(%rax)
 4302af5:      	je	0x4302ab0 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x80>
 4302af7:      	jmp	0x4302b6d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x13d>
 4302af9:      	movq	%rbx, %rdi
 4302afc:      	movq	%rax, %rsi
 4302aff:      	callq	0x3dae6c0 <_ZN4llvm23SmallVectorTemplateBaseIPNS_5ValueELb1EE18growAndEmplaceBackIJRS2_EEES5_DpOT_>
 4302b04:      	jmp	0x4302ae9 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xb9>
 4302b06:      	xorl	%esi, %esi
 4302b08:      	movq	%r12, %rdi
 4302b0b:      	movq	%rbp, %rdx
 4302b0e:      	callq	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 4302b13:      	movq	0x28(%rsp), %rdi
 4302b18:      	movq	0x10(%rsp), %rbx
 4302b1d:      	cmpq	%r12, %rdi
 4302b20:      	je	0x4302b2d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xfd>
 4302b22:      	movq	%rax, %r14
 4302b25:      	callq	0x828a640 <free@plt>
 4302b2a:      	movq	%r14, %rax
 4302b2d:      	leaq	0x10(%rax), %rcx
 4302b31:      	rolq	$0x30, %rcx
 4302b35:      	xorq	%rcx, %rbx
 4302b38:      	xorq	%rbp, %rbx
 4302b3b:      	imulq	%r13, %rbx
 4302b3f:      	xorq	%rbx, %rcx
 4302b42:      	shrq	$0x2f, %rbx
 4302b46:      	xorq	%rcx, %rbx
 4302b49:      	imulq	%r13, %rbx
 4302b4d:      	movq	%rbx, %rcx
 4302b50:      	shrq	$0x2f, %rcx
 4302b54:      	xorl	%ebx, %ecx
 4302b56:      	imull	$0xeb382d69, %ecx, %ecx # imm = 0xEB382D69
 4302b5c:      	xorl	%ecx, %eax
 4302b5e:      	addq	$0x68, %rsp
 4302b62:      	popq	%rbx
 4302b63:      	popq	%r12
 4302b65:      	popq	%r13
 4302b67:      	popq	%r14
 4302b69:      	popq	%r15
 4302b6b:      	popq	%rbp
 4302b6c:      	retq
 4302b6d:      	movq	0x28(%rsp), %rdi
 4302b72:      	movl	0x30(%rsp), %eax
 4302b76:      	leaq	(,%rax,8), %rsi
 4302b7e:      	cmpq	$0x8, %rax
 4302b82:      	ja	0x4302b8b <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x15b>
 4302b84:      	leaq	0x38(%rsp), %r12
 4302b89:      	jmp	0x4302b0b <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xdb>
 4302b8b:      	movq	%rax, (%rsp)
 4302b8f:      	movabsq	$-0x4b6d499041670d8d, %r8 # imm = 0xB492B66FBE98F273
 4302b99:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 4302ba3:      	andq	$-0x40, %rsi
 4302ba7:      	movq	0x8(%rdi), %rbx
 4302bab:      	movq	0x10(%rdi), %rax
 4302baf:      	movabsq	$-0x73d22641534b4d52, %r10 # imm = 0x8C2DD9BEACB4B2AE
 4302bb9:      	addq	%rbx, %r10
 4302bbc:      	rolq	$0x1b, %r10
 4302bc0:      	imulq	%r8, %r10
 4302bc4:      	movq	0x30(%rdi), %rdx
 4302bc8:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 4302bd2:      	addq	%rdx, %r9
 4302bd5:      	rolq	$0x16, %r9
 4302bd9:      	imulq	%r8, %r9
 4302bdd:      	movabsq	$-0x85335acd9bb6c6a, %r15 # imm = 0xF7ACCA5326449396
 4302be7:      	xorq	%r10, %r15
 4302bea:      	movq	0x28(%rdi), %r12
 4302bee:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 4302bf8:      	addq	%r12, %r8
 4302bfb:      	addq	%r9, %r8
 4302bfe:      	movabsq	$0x298df016a9f64655, %r14 # imm = 0x298DF016A9F64655
 4302c08:      	addq	(%rdi), %r14
 4302c0b:      	leaq	(%rbp,%r14), %r9
 4302c10:      	addq	%r15, %r9
 4302c13:      	movq	0x18(%rdi), %r10
 4302c17:      	leaq	-0x11a5f(%r10,%r9), %r11
 4302c1f:      	rolq	$0x2b, %r11
 4302c23:      	addq	%rax, %rbx
 4302c26:      	addq	%r14, %rbx
 4302c29:      	movq	%rbx, %r9
 4302c2c:      	rolq	$0x14, %r9
 4302c30:      	addq	%r14, %r9
 4302c33:      	addq	%r11, %r9
 4302c36:      	movabsq	$0x4bf62cb950c3753a, %r14 # imm = 0x4BF62CB950C3753A
 4302c40:      	addq	0x20(%rdi), %r14
 4302c44:      	addq	%r10, %rbx
 4302c47:      	movq	%rdi, 0x8(%rsp)
 4302c4c:      	movq	0x38(%rdi), %r10
 4302c50:      	addq	%r14, %rax
 4302c53:      	addq	%r10, %rax
 4302c56:      	addq	%r8, %rax
 4302c59:      	rolq	$0x2b, %rax
 4302c5d:      	addq	%rdx, %r12
 4302c60:      	addq	%r14, %r12
 4302c63:      	movq	%r12, %r11
 4302c66:      	rolq	$0x14, %r11
 4302c6a:      	addq	%r14, %r11
 4302c6d:      	addq	%rax, %r11
 4302c70:      	addq	%r10, %r12
 4302c73:      	cmpq	$0x40, %rsi
 4302c77:      	jne	0x4302c8d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x25d>
 4302c79:      	movq	%r11, %rdx
 4302c7c:      	movq	%r12, %r10
 4302c7f:      	movq	%r9, %rbp
 4302c82:      	movq	%rbx, %r14
 4302c85:      	movq	%r15, %rsi
 4302c88:      	jmp	0x4302d7d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x34d>
 4302c8d:      	addq	$-0x40, %rsi
 4302c91:      	movq	%rsi, 0x18(%rsp)
 4302c96:      	xorl	%eax, %eax
 4302c98:      	movq	0x8(%rsp), %rdi
 4302c9d:      	nopl	(%rax)
 4302ca0:      	addq	%r8, %rcx
 4302ca3:      	addq	%rbx, %rcx
 4302ca6:      	movq	0x48(%rdi,%rax), %r14
 4302cab:      	movq	0x50(%rdi,%rax), %r13
 4302cb0:      	addq	%r14, %rcx
 4302cb3:      	rolq	$0x1b, %rcx
 4302cb7:      	movabsq	$-0x4b6d499041670d8d, %rdx # imm = 0xB492B66FBE98F273
 4302cc1:      	imulq	%rdx, %rcx
 4302cc5:      	addq	%r9, %r8
 4302cc8:      	movq	0x70(%rdi,%rax), %rsi
 4302ccd:      	movq	%rsi, 0x20(%rsp)
 4302cd2:      	addq	%rsi, %r8
 4302cd5:      	rolq	$0x16, %r8
 4302cd9:      	imulq	%rdx, %r8
 4302cdd:      	movq	%rcx, %rsi
 4302ce0:      	xorq	%r11, %rsi
 4302ce3:      	movq	0x68(%rdi,%rax), %r10
 4302ce8:      	addq	%r10, %rbx
 4302ceb:      	addq	%r12, %r15
 4302cee:      	rolq	$0x1f, %r15
 4302cf2:      	addq	%rbx, %r8
 4302cf5:      	imulq	%rdx, %r9
 4302cf9:      	addq	0x40(%rdi,%rax), %r9
 4302cfe:      	movq	%r15, %rcx
 4302d01:      	movq	0x58(%rdi,%rax), %rbx
 4302d06:      	addq	%r9, %r12
 4302d09:      	addq	%rbx, %r12
 4302d0c:      	addq	%rsi, %r12
 4302d0f:      	rolq	$0x2b, %r12
 4302d13:      	addq	%r13, %r14
 4302d16:      	addq	%r9, %r14
 4302d19:      	movq	%r14, %rbp
 4302d1c:      	rolq	$0x14, %rbp
 4302d20:      	imulq	%rdx, %rcx
 4302d24:      	addq	%r9, %rbp
 4302d27:      	addq	%r12, %rbp
 4302d2a:      	addq	%rcx, %r11
 4302d2d:      	addq	%r8, %r13
 4302d30:      	addq	0x60(%rdi,%rax), %r11
 4302d35:      	movq	0x78(%rdi,%rax), %r9
 4302d3a:      	addq	%r11, %r13
 4302d3d:      	addq	%r9, %r13
 4302d40:      	rolq	$0x2b, %r13
 4302d44:      	addq	%rbx, %r14
 4302d47:      	addq	0x20(%rsp), %r10
 4302d4c:      	addq	%r11, %r10
 4302d4f:      	movq	%r10, %rdx
 4302d52:      	rolq	$0x14, %rdx
 4302d56:      	addq	%r11, %rdx
 4302d59:      	addq	%r13, %rdx
 4302d5c:      	addq	%r9, %r10
 4302d5f:      	addq	$0x40, %rax
 4302d63:      	movq	%rsi, %r15
 4302d66:      	movq	%r14, %rbx
 4302d69:      	movq	%rbp, %r9
 4302d6c:      	movq	%r10, %r12
 4302d6f:      	movq	%rdx, %r11
 4302d72:      	cmpq	%rax, 0x18(%rsp)
 4302d77:      	jne	0x4302ca0 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x270>
 4302d7d:      	movq	(%rsp), %rbx
 4302d81:      	testb	$0x7, %bl
 4302d84:      	je	0x4302e86 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x456>
 4302d8a:      	movq	0x8(%rsp), %rdi
 4302d8f:      	movq	-0x38(%rdi,%rbx,8), %rax
 4302d94:      	movq	-0x30(%rdi,%rbx,8), %r9
 4302d99:      	addq	%rax, %rcx
 4302d9c:      	addq	%r8, %rcx
 4302d9f:      	addq	%r14, %rcx
 4302da2:      	rolq	$0x1b, %rcx
 4302da6:      	movabsq	$-0x4b6d499041670d8d, %r12 # imm = 0xB492B66FBE98F273
 4302db0:      	imulq	%r12, %rcx
 4302db4:      	addq	%rbp, %r8
 4302db7:      	movq	(%rsp), %r11
 4302dbb:      	movq	-0x10(%rdi,%r11,8), %rbx
 4302dc0:      	addq	%rbx, %r8
 4302dc3:      	rolq	$0x16, %r8
 4302dc7:      	imulq	%r12, %r8
 4302dcb:      	xorq	%rdx, %rcx
 4302dce:      	movq	(%rsp), %r11
 4302dd2:      	movq	-0x18(%rdi,%r11,8), %r11
 4302dd7:      	addq	%r11, %r14
 4302dda:      	addq	%r14, %r8
 4302ddd:      	addq	%r10, %rsi
 4302de0:      	rolq	$0x1f, %rsi
 4302de4:      	movq	%rsi, %r15
 4302de7:      	imulq	%r12, %rbp
 4302deb:      	addq	%rcx, %r10
 4302dee:      	movq	(%rsp), %rsi
 4302df2:      	addq	-0x40(%rdi,%rsi,8), %rbp
 4302df7:      	movq	(%rsp), %rsi
 4302dfb:      	movq	-0x28(%rdi,%rsi,8), %r14
 4302e00:      	addq	%r14, %r10
 4302e03:      	addq	%rbp, %r10
 4302e06:      	rolq	$0x2b, %r10
 4302e0a:      	imulq	%r12, %r15
 4302e0e:      	addq	%r9, %rax
 4302e11:      	addq	%rbp, %rax
 4302e14:      	movq	%rax, %rsi
 4302e17:      	rolq	$0x14, %rsi
 4302e1b:      	addq	%rbp, %rsi
 4302e1e:      	addq	%r10, %rsi
 4302e21:      	addq	%r14, %rax
 4302e24:      	addq	%r15, %rdx
 4302e27:      	movq	(%rsp), %r10
 4302e2b:      	addq	-0x20(%rdi,%r10,8), %rdx
 4302e30:      	addq	%r8, %r9
 4302e33:      	movq	(%rsp), %r10
 4302e37:      	movq	-0x8(%rdi,%r10,8), %r10
 4302e3c:      	addq	%r10, %r9
 4302e3f:      	addq	%rdx, %r9
 4302e42:      	rolq	$0x2b, %r9
 4302e46:      	addq	%rbx, %r11
 4302e49:      	addq	%rdx, %r11
 4302e4c:      	movq	%r11, %rbx
 4302e4f:      	rolq	$0x14, %rbx
 4302e53:      	addq	%rdx, %rbx
 4302e56:      	addq	%r9, %rbx
 4302e59:      	addq	%r10, %r11
 4302e5c:      	movq	%rbx, %rdx
 4302e5f:      	movq	(%rsp), %rbx
 4302e63:      	movq	%r11, %r10
 4302e66:      	movq	%rsi, %rbp
 4302e69:      	movq	%rax, %r14
 4302e6c:      	movq	%rcx, %rsi
 4302e6f:      	movq	%r15, %rcx
 4302e72:      	movq	%r12, %r11
 4302e75:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302e7f:      	leaq	0x38(%rsp), %r12
 4302e84:      	jmp	0x4302e9f <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0x46f>
 4302e86:      	movabsq	$-0x622015f714c7d297, %r13 # imm = 0x9DDFEA08EB382D69
 4302e90:      	leaq	0x38(%rsp), %r12
 4302e95:      	movabsq	$-0x4b6d499041670d8d, %r11 # imm = 0xB492B66FBE98F273
 4302e9f:      	xorq	%r10, %r14
 4302ea2:      	imulq	%r13, %r14
 4302ea6:      	xorq	%r14, %r10
 4302ea9:      	shrq	$0x2f, %r14
 4302ead:      	xorq	%r10, %r14
 4302eb0:      	imulq	%r13, %r14
 4302eb4:      	movq	%r14, %rax
 4302eb7:      	shrq	$0x2f, %rax
 4302ebb:      	xorq	%r14, %rax
 4302ebe:      	imulq	%r13, %rax
 4302ec2:      	movq	%r8, %r9
 4302ec5:      	shrq	$0x2f, %r9
 4302ec9:      	xorq	%r8, %r9
 4302ecc:      	imulq	%r11, %r9
 4302ed0:      	addq	%rsi, %r9
 4302ed3:      	addq	%rax, %r9
 4302ed6:      	xorq	%rdx, %rbp
 4302ed9:      	imulq	%r13, %rbp
 4302edd:      	xorq	%rbp, %rdx
 4302ee0:      	shrq	$0x2f, %rbp
 4302ee4:      	xorq	%rdx, %rbp
 4302ee7:      	imulq	%r13, %rbp
 4302eeb:      	movq	%rbp, %rax
 4302eee:      	shrq	$0x2f, %rax
 4302ef2:      	xorq	%rbp, %rax
 4302ef5:      	imulq	%r13, %rax
 4302ef9:      	movabsq	$-0x5b6a4c820b386c68, %rdx # imm = 0xA495B37DF4C79398
 4302f03:      	imulq	%rdx, %rbx
 4302f07:      	addq	%rcx, %rbx
 4302f0a:      	addq	%rax, %rbx
 4302f0d:      	xorq	%rbx, %r9
 4302f10:      	imulq	%r13, %r9
 4302f14:      	xorq	%r9, %rbx
 4302f17:      	shrq	$0x2f, %r9
 4302f1b:      	xorq	%rbx, %r9
 4302f1e:      	imulq	%r13, %r9
 4302f22:      	movq	%r9, %rax
 4302f25:      	shrq	$0x2f, %rax
 4302f29:      	xorq	%r9, %rax
 4302f2c:      	imulq	%r13, %rax
 4302f30:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 4302f3a:      	movq	0x8(%rsp), %rdi
 4302f3f:      	movq	0x10(%rsp), %rbx
 4302f44:      	cmpq	%r12, %rdi
 4302f47:      	jne	0x4302b22 <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xf2>
 4302f4d:      	jmp	0x4302b2d <_ZN4llvm12DenseMapInfoIPK17SwitchSuccWrappervE12getHashValueES3_+0xfd>
