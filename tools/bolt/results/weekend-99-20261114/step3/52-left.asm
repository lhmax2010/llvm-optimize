
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000003660cb0 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_>:
 3660cb0:      	movq	%rsi, %rcx
 3660cb3:      	movabsq	$-0xae502812ab8d92, %rax # imm = 0xFF51AFD7ED54726E
 3660cbd:      	subq	%rdi, %rsi
 3660cc0:      	cmpq	$0x40, %rsi
 3660cc4:      	ja	0x3660cd4 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x24>
 3660cc6:      	addq	$0x11a5f, %rax          # imm = 0x11A5F
 3660ccc:      	movq	%rax, %rdx
 3660ccf:      	jmp	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 3660cd4:      	pushq	%rbp
 3660cd5:      	pushq	%r15
 3660cd7:      	pushq	%r14
 3660cd9:      	pushq	%r13
 3660cdb:      	pushq	%r12
 3660cdd:      	pushq	%rbx
 3660cde:      	movq	%rcx, -0x18(%rsp)
 3660ce3:      	movabsq	$-0x4b6d499041670d8d, %r9 # imm = 0xB492B66FBE98F273
 3660ced:      	movabsq	$0x544962662a7ee1a4, %r8 # imm = 0x544962662A7EE1A4
 3660cf7:      	movq	%rsi, -0x10(%rsp)
 3660cfc:      	movq	%rsi, %r14
 3660cff:      	andq	$-0x40, %r14
 3660d03:      	movq	0x8(%rdi), %r13
 3660d07:      	movq	0x10(%rdi), %rcx
 3660d0b:      	movabsq	$-0x73d22641534b4d52, %rdx # imm = 0x8C2DD9BEACB4B2AE
 3660d15:      	addq	%r13, %rdx
 3660d18:      	rolq	$0x1b, %rdx
 3660d1c:      	imulq	%r9, %rdx
 3660d20:      	movq	0x30(%rdi), %rsi
 3660d24:      	movabsq	$-0x414bff9ed66a691c, %r10 # imm = 0xBEB40061299596E4
 3660d2e:      	addq	%rsi, %r10
 3660d31:      	rolq	$0x16, %r10
 3660d35:      	imulq	%r9, %r10
 3660d39:      	movabsq	$-0x85335acd9bb6c6a, %rbp # imm = 0xF7ACCA5326449396
 3660d43:      	xorq	%rdx, %rbp
 3660d46:      	movq	0x28(%rdi), %r12
 3660d4a:      	movabsq	$-0x7323d61940a0da1f, %r9 # imm = 0x8CDC29E6BF5F25E1
 3660d54:      	addq	%r12, %r9
 3660d57:      	addq	%r10, %r9
 3660d5a:      	movabsq	$0x298df016a9f64655, %r10 # imm = 0x298DF016A9F64655
 3660d64:      	addq	(%rdi), %r10
 3660d67:      	movq	0x18(%rdi), %r11
 3660d6b:      	addq	%r10, %rax
 3660d6e:      	addq	%r11, %rax
 3660d71:      	addq	%rbp, %rax
 3660d74:      	rolq	$0x2b, %rax
 3660d78:      	addq	%rcx, %r13
 3660d7b:      	addq	%r10, %r13
 3660d7e:      	movq	%r13, %rdx
 3660d81:      	rolq	$0x14, %rdx
 3660d85:      	addq	%r10, %rdx
 3660d88:      	addq	%rax, %rdx
 3660d8b:      	movabsq	$0x4bf62cb950c3753a, %rax # imm = 0x4BF62CB950C3753A
 3660d95:      	addq	0x20(%rdi), %rax
 3660d99:      	addq	%r11, %r13
 3660d9c:      	movq	0x38(%rdi), %r10
 3660da0:      	addq	%rax, %rcx
 3660da3:      	addq	%r10, %rcx
 3660da6:      	addq	%r9, %rcx
 3660da9:      	rolq	$0x2b, %rcx
 3660dad:      	addq	%rsi, %r12
 3660db0:      	addq	%rax, %r12
 3660db3:      	movq	%r12, %rbx
 3660db6:      	rolq	$0x14, %rbx
 3660dba:      	addq	%rax, %rbx
 3660dbd:      	addq	%rcx, %rbx
 3660dc0:      	addq	%r10, %r12
 3660dc3:      	movq	%r14, -0x20(%rsp)
 3660dc8:      	cmpq	$0x40, %r14
 3660dcc:      	jne	0x3660de2 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x132>
 3660dce:      	movq	%rbx, %rsi
 3660dd1:      	movq	%r12, %r11
 3660dd4:      	movq	%rdx, %rax
 3660dd7:      	movq	%r13, %r14
 3660dda:      	movq	%rbp, %r15
 3660ddd:      	jmp	0x3660ecd <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x21d>
 3660de2:      	addq	$-0x40, -0x20(%rsp)
 3660de8:      	xorl	%ecx, %ecx
 3660dea:      	nopw	(%rax,%rax)
 3660df0:      	addq	%r9, %r8
 3660df3:      	addq	%r13, %r8
 3660df6:      	movq	0x48(%rdi,%rcx), %r14
 3660dfb:      	movq	0x50(%rdi,%rcx), %r10
 3660e00:      	addq	%r14, %r8
 3660e03:      	rolq	$0x1b, %r8
 3660e07:      	movabsq	$-0x4b6d499041670d8d, %rsi # imm = 0xB492B66FBE98F273
 3660e11:      	imulq	%rsi, %r8
 3660e15:      	addq	%rdx, %r9
 3660e18:      	movq	0x70(%rdi,%rcx), %rax
 3660e1d:      	movq	%rax, -0x8(%rsp)
 3660e22:      	addq	%rax, %r9
 3660e25:      	rolq	$0x16, %r9
 3660e29:      	imulq	%rsi, %r9
 3660e2d:      	movq	%r8, %r15
 3660e30:      	xorq	%rbx, %r15
 3660e33:      	movq	0x68(%rdi,%rcx), %r11
 3660e38:      	addq	%r11, %r13
 3660e3b:      	addq	%r12, %rbp
 3660e3e:      	rolq	$0x1f, %rbp
 3660e42:      	addq	%r13, %r9
 3660e45:      	imulq	%rsi, %rdx
 3660e49:      	addq	0x40(%rdi,%rcx), %rdx
 3660e4e:      	movq	%rbp, %r8
 3660e51:      	movq	0x58(%rdi,%rcx), %r13
 3660e56:      	addq	%rdx, %r12
 3660e59:      	addq	%r13, %r12
 3660e5c:      	addq	%r15, %r12
 3660e5f:      	rolq	$0x2b, %r12
 3660e63:      	addq	%r10, %r14
 3660e66:      	addq	%rdx, %r14
 3660e69:      	movq	%r14, %rax
 3660e6c:      	rolq	$0x14, %rax
 3660e70:      	imulq	%rsi, %r8
 3660e74:      	addq	%rdx, %rax
 3660e77:      	addq	%r12, %rax
 3660e7a:      	addq	%r8, %rbx
 3660e7d:      	addq	%r9, %r10
 3660e80:      	addq	0x60(%rdi,%rcx), %rbx
 3660e85:      	movq	0x78(%rdi,%rcx), %rdx
 3660e8a:      	addq	%rbx, %r10
 3660e8d:      	addq	%rdx, %r10
 3660e90:      	rolq	$0x2b, %r10
 3660e94:      	addq	%r13, %r14
 3660e97:      	addq	-0x8(%rsp), %r11
 3660e9c:      	addq	%rbx, %r11
 3660e9f:      	movq	%r11, %rsi
 3660ea2:      	rolq	$0x14, %rsi
 3660ea6:      	addq	%rbx, %rsi
 3660ea9:      	addq	%r10, %rsi
 3660eac:      	addq	%rdx, %r11
 3660eaf:      	addq	$0x40, %rcx
 3660eb3:      	movq	%r15, %rbp
 3660eb6:      	movq	%r14, %r13
 3660eb9:      	movq	%rax, %rdx
 3660ebc:      	movq	%r11, %r12
 3660ebf:      	movq	%rsi, %rbx
 3660ec2:      	cmpq	%rcx, -0x20(%rsp)
 3660ec7:      	jne	0x3660df0 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x140>
 3660ecd:      	movq	-0x10(%rsp), %r12
 3660ed2:      	testb	$0x3f, %r12b
 3660ed6:      	je	0x3660fa3 <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2f3>
 3660edc:      	leaq	(%r9,%r14), %rdi
 3660ee0:      	movq	-0x18(%rsp), %rbp
 3660ee5:      	movq	-0x38(%rbp), %rcx
 3660ee9:      	movq	-0x30(%rbp), %rdx
 3660eed:      	addq	%rcx, %r8
 3660ef0:      	addq	%rdi, %r8
 3660ef3:      	rolq	$0x1b, %r8
 3660ef7:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3660f01:      	imulq	%r13, %r8
 3660f05:      	addq	%rax, %r9
 3660f08:      	movq	-0x10(%rbp), %r10
 3660f0c:      	addq	%r10, %r9
 3660f0f:      	rolq	$0x16, %r9
 3660f13:      	imulq	%r13, %r9
 3660f17:      	xorq	%rsi, %r8
 3660f1a:      	movq	-0x18(%rbp), %rdi
 3660f1e:      	addq	%rdi, %r14
 3660f21:      	addq	%r14, %r9
 3660f24:      	addq	%r11, %r15
 3660f27:      	rolq	$0x1f, %r15
 3660f2b:      	movq	%r15, %rbx
 3660f2e:      	imulq	%r13, %rax
 3660f32:      	addq	%r8, %r11
 3660f35:      	addq	-0x40(%rbp), %rax
 3660f39:      	movq	-0x28(%rbp), %r15
 3660f3d:      	addq	%r15, %r11
 3660f40:      	addq	%rax, %r11
 3660f43:      	rolq	$0x2b, %r11
 3660f47:      	imulq	%r13, %rbx
 3660f4b:      	addq	%rdx, %rcx
 3660f4e:      	addq	%rax, %rcx
 3660f51:      	movq	%rcx, %r14
 3660f54:      	rolq	$0x14, %r14
 3660f58:      	addq	%rax, %r14
 3660f5b:      	addq	%r11, %r14
 3660f5e:      	addq	%r15, %rcx
 3660f61:      	addq	%rbx, %rsi
 3660f64:      	addq	-0x20(%rbp), %rsi
 3660f68:      	addq	%r9, %rdx
 3660f6b:      	movq	-0x8(%rbp), %rax
 3660f6f:      	addq	%rax, %rdx
 3660f72:      	addq	%rsi, %rdx
 3660f75:      	rolq	$0x2b, %rdx
 3660f79:      	addq	%r10, %rdi
 3660f7c:      	addq	%rsi, %rdi
 3660f7f:      	movq	%rdi, %r10
 3660f82:      	rolq	$0x14, %r10
 3660f86:      	addq	%rsi, %r10
 3660f89:      	addq	%rdx, %r10
 3660f8c:      	addq	%rax, %rdi
 3660f8f:      	movq	%r10, %rsi
 3660f92:      	movq	%rdi, %r11
 3660f95:      	movq	%r14, %rax
 3660f98:      	movq	%rcx, %r14
 3660f9b:      	movq	%r8, %r15
 3660f9e:      	movq	%rbx, %r8
 3660fa1:      	jmp	0x3660fad <_ZN4llvm7hashing6detail23hash_combine_range_implImEENSt9enable_ifIXsr16is_hashable_dataIT_EE5valueENS_9hash_codeEE4typeEPS4_S8_+0x2fd>
 3660fa3:      	movabsq	$-0x4b6d499041670d8d, %r13 # imm = 0xB492B66FBE98F273
 3660fad:      	xorq	%r11, %r14
 3660fb0:      	movabsq	$-0x622015f714c7d297, %rcx # imm = 0x9DDFEA08EB382D69
 3660fba:      	imulq	%rcx, %r14
 3660fbe:      	xorq	%r14, %r11
 3660fc1:      	shrq	$0x2f, %r14
 3660fc5:      	xorq	%r11, %r14
 3660fc8:      	imulq	%rcx, %r14
 3660fcc:      	movq	%r14, %rdi
 3660fcf:      	shrq	$0x2f, %rdi
 3660fd3:      	xorq	%r14, %rdi
 3660fd6:      	imulq	%rcx, %rdi
 3660fda:      	movq	%r9, %rdx
 3660fdd:      	shrq	$0x2f, %rdx
 3660fe1:      	xorq	%r9, %rdx
 3660fe4:      	imulq	%r13, %rdx
 3660fe8:      	addq	%r15, %rdx
 3660feb:      	addq	%rdi, %rdx
 3660fee:      	xorq	%rsi, %rax
 3660ff1:      	imulq	%rcx, %rax
 3660ff5:      	xorq	%rax, %rsi
 3660ff8:      	shrq	$0x2f, %rax
 3660ffc:      	xorq	%rsi, %rax
 3660fff:      	imulq	%rcx, %rax
 3661003:      	movq	%rax, %rsi
 3661006:      	shrq	$0x2f, %rsi
 366100a:      	xorq	%rax, %rsi
 366100d:      	imulq	%rcx, %rsi
 3661011:      	movq	%r12, %rax
 3661014:      	shrq	$0x2f, %rax
 3661018:      	xorq	%r12, %rax
 366101b:      	imulq	%r13, %rax
 366101f:      	addq	%r8, %rax
 3661022:      	addq	%rsi, %rax
 3661025:      	xorq	%rax, %rdx
 3661028:      	imulq	%rcx, %rdx
 366102c:      	xorq	%rdx, %rax
 366102f:      	shrq	$0x2f, %rdx
 3661033:      	xorq	%rax, %rdx
 3661036:      	imulq	%rcx, %rdx
 366103a:      	movq	%rdx, %rax
 366103d:      	shrq	$0x2f, %rax
 3661041:      	xorq	%rdx, %rax
 3661044:      	imulq	%rcx, %rax
 3661048:      	popq	%rbx
 3661049:      	popq	%r12
 366104b:      	popq	%r13
 366104d:      	popq	%r14
 366104f:      	popq	%r15
 3661051:      	popq	%rbp
 3661052:      	retq
