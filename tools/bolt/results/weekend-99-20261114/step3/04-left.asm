
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000008135c20 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm>:
 8135c20:      	pushq	%rbp
 8135c21:      	pushq	%r15
 8135c23:      	pushq	%r14
 8135c25:      	pushq	%r13
 8135c27:      	pushq	%r12
 8135c29:      	pushq	%rbx
 8135c2a:      	subq	$0x28, %rsp
 8135c2e:      	movl	%r9d, 0xc(%rsp)
 8135c33:      	movq	%r8, 0x18(%rsp)
 8135c38:      	movq	%rdx, 0x10(%rsp)
 8135c3d:      	movq	%rdi, %rbx
 8135c40:      	leal	(%rcx,%rsi), %eax
 8135c43:      	leal	0x43(%rsi,%rcx), %r12d
 8135c48:      	andl	$-0x8, %r12d
 8135c4c:      	subl	%eax, %r12d
 8135c4f:      	movq	%rcx, 0x20(%rsp)
 8135c54:      	leal	-0x3c(%r12,%rcx), %r13d
 8135c59:      	movq	(%rdi), %rax
 8135c5c:      	callq	*0x50(%rax)
 8135c5f:      	movq	%rax, %r15
 8135c62:      	movl	0x10(%rbx), %ebp
 8135c65:      	addl	0x20(%rbx), %r15d
 8135c69:      	leaq	-0x7396ebf(%rip), %rdx  # 0xd9edb1 <.L.str.23>
 8135c70:      	movq	%rbx, %rsi
 8135c73:      	movl	$0x3, %r8d
 8135c79:      	callq	0x41143c0 <_ZNK4llvm5Twine13printOneChildERNS_11raw_ostreamENS0_5ChildENS0_8NodeKindE>
 8135c7e:      	movq	%rbx, %rsi
 8135c81:      	movq	%r13, %rdx
 8135c84:      	movl	$0x9, %r8d
 8135c8a:      	callq	0x41143c0 <_ZNK4llvm5Twine13printOneChildERNS_11raw_ostreamENS0_5ChildENS0_8NodeKindE>
 8135c8f:      	movq	(%rbx), %rax
 8135c92:      	movq	%rbx, %rdi
 8135c95:      	callq	*0x50(%rax)
 8135c98:      	addl	%ebp, %eax
 8135c9a:      	addl	0x20(%rbx), %eax
 8135c9d:      	movl	0x10(%rbx), %ecx
 8135ca0:      	subl	%eax, %r15d
 8135ca3:      	leal	0x10(%r15,%rcx), %r14d
 8135ca8:      	cmpl	$0x50, %r14d
 8135cac:      	jae	0x8135cc2 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xa2>
 8135cae:      	movl	%r14d, %edx
 8135cb1:      	leaq	-0x6691188(%rip), %rsi  # 0x1aa4b30 <_ZZL13write_paddingILc32EERN4llvm11raw_ostreamES2_jE5Chars.llvm.8189526126256621287>
 8135cb8:      	movq	%rbx, %rdi
 8135cbb:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135cc0:      	jmp	0x8135cf0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xd0>
 8135cc2:      	leaq	-0x6691199(%rip), %r15  # 0x1aa4b30 <_ZZL13write_paddingILc32EERN4llvm11raw_ostreamES2_jE5Chars.llvm.8189526126256621287>
 8135cc9:      	nopl	(%rax)
 8135cd0:      	cmpl	$0x4f, %r14d
 8135cd4:      	movl	$0x4f, %ebp
 8135cd9:      	cmovbl	%r14d, %ebp
 8135cdd:      	movq	%rbx, %rdi
 8135ce0:      	movq	%r15, %rsi
 8135ce3:      	movq	%rbp, %rdx
 8135ce6:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135ceb:      	subl	%ebp, %r14d
 8135cee:      	jne	0x8135cd0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xb0>
 8135cf0:      	addl	$-0x3c, %r12d
 8135cf4:      	addq	0x70(%rsp), %r13
 8135cf9:      	movq	%rbx, %rdi
 8135cfc:      	movq	0x18(%rsp), %rsi
 8135d01:      	movl	0xc(%rsp), %edx
 8135d05:      	movl	0x60(%rsp), %ecx
 8135d09:      	movl	0x68(%rsp), %r8d
 8135d0e:      	movq	%r13, %r9
 8135d11:      	callq	0x8135de0 <_ZL23printRestOfMemberHeaderRN4llvm11raw_ostreamERKNSt6chrono10time_pointINS2_3_V212system_clockENS2_8durationIlSt5ratioILl1ELl1EEEEEEjjjm>
 8135d16:      	movq	0x18(%rbx), %rax
 8135d1a:      	movq	0x20(%rbx), %rdi
 8135d1e:      	subq	%rdi, %rax
 8135d21:      	movq	0x20(%rsp), %rdx
 8135d26:      	cmpq	%rax, %rdx
 8135d29:      	jbe	0x8135d3a <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x11a>
 8135d2b:      	movq	%rbx, %rdi
 8135d2e:      	movq	0x10(%rsp), %rsi
 8135d33:      	callq	0x4144010 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135d38:      	jmp	0x8135d50 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x130>
 8135d3a:      	testq	%rdx, %rdx
 8135d3d:      	je	0x8135d50 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x130>
 8135d3f:      	movq	0x10(%rsp), %rsi
 8135d44:      	movq	%rdx, %r14
 8135d47:      	callq	0x828ace0 <memcpy@plt>
 8135d4c:      	addq	%r14, 0x20(%rbx)
 8135d50:      	testl	%r12d, %r12d
 8135d53:      	je	0x8135dc6 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x1a6>
 8135d55:      	leaq	0xb(%rsp), %r14
 8135d5a:      	nopw	(%rax,%rax)
 8135d60:      	movq	0x20(%rbx), %rdx
 8135d64:      	cmpq	0x18(%rbx), %rdx
 8135d68:      	jae	0x8135d7c <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x15c>
 8135d6a:      	leaq	0x1(%rdx), %rax
 8135d6e:      	movq	%rax, 0x20(%rbx)
 8135d72:      	movb	$0x0, (%rdx)
 8135d75:      	decl	%r12d
 8135d78:      	jne	0x8135d60 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135d7a:      	jmp	0x8135dc6 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x1a6>
 8135d7c:      	movq	0x10(%rbx), %rsi
 8135d80:      	testq	%rsi, %rsi
 8135d83:      	je	0x8135d9b <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x17b>
 8135d85:      	subq	%rsi, %rdx
 8135d88:      	movq	%rsi, 0x20(%rbx)
 8135d8c:      	movq	(%rbx), %rax
 8135d8f:      	movq	%rbx, %rdi
 8135d92:      	callq	*0x48(%rax)
 8135d95:      	movq	0x20(%rbx), %rdx
 8135d99:      	jmp	0x8135d6a <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x14a>
 8135d9b:      	cmpl	$0x0, 0x2c(%rbx)
 8135d9f:      	je	0x8135dab <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x18b>
 8135da1:      	movq	%rbx, %rdi
 8135da4:      	callq	0x41431e0 <_ZN4llvm11raw_ostream11SetBufferedEv>
 8135da9:      	jmp	0x8135d60 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135dab:      	movb	$0x0, 0xb(%rsp)
 8135db0:      	movq	(%rbx), %rax
 8135db3:      	movl	$0x1, %edx
 8135db8:      	movq	%rbx, %rdi
 8135dbb:      	movq	%r14, %rsi
 8135dbe:      	callq	*0x48(%rax)
 8135dc1:      	decl	%r12d
 8135dc4:      	jne	0x8135d60 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135dc6:      	addq	$0x28, %rsp
 8135dca:      	popq	%rbx
 8135dcb:      	popq	%r12
 8135dcd:      	popq	%r13
 8135dcf:      	popq	%r14
 8135dd1:      	popq	%r15
 8135dd3:      	popq	%rbp
 8135dd4:      	retq
