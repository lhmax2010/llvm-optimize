
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000008135b90 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm>:
 8135b90:      	pushq	%rbp
 8135b91:      	pushq	%r15
 8135b93:      	pushq	%r14
 8135b95:      	pushq	%r13
 8135b97:      	pushq	%r12
 8135b99:      	pushq	%rbx
 8135b9a:      	subq	$0x28, %rsp
 8135b9e:      	movl	%r9d, 0xc(%rsp)
 8135ba3:      	movq	%r8, 0x18(%rsp)
 8135ba8:      	movq	%rdx, 0x10(%rsp)
 8135bad:      	movq	%rdi, %rbx
 8135bb0:      	leal	0x43(%rsi,%rcx), %r12d
 8135bb5:      	andl	$-0x8, %r12d
 8135bb9:      	subl	%ecx, %r12d
 8135bbc:      	subl	%esi, %r12d
 8135bbf:      	movq	%rcx, 0x20(%rsp)
 8135bc4:      	leal	-0x3c(%r12,%rcx), %r13d
 8135bc9:      	movq	(%rdi), %rax
 8135bcc:      	callq	*0x50(%rax)
 8135bcf:      	movq	%rax, %r15
 8135bd2:      	movl	0x10(%rbx), %ebp
 8135bd5:      	addl	0x20(%rbx), %r15d
 8135bd9:      	leaq	-0x7396e2f(%rip), %rdx  # 0xd9edb1 <.L.str.23>
 8135be0:      	movq	%rbx, %rsi
 8135be3:      	movl	$0x3, %r8d
 8135be9:      	callq	0x4114330 <_ZNK4llvm5Twine13printOneChildERNS_11raw_ostreamENS0_5ChildENS0_8NodeKindE>
 8135bee:      	movq	%rbx, %rsi
 8135bf1:      	movq	%r13, %rdx
 8135bf4:      	movl	$0x9, %r8d
 8135bfa:      	callq	0x4114330 <_ZNK4llvm5Twine13printOneChildERNS_11raw_ostreamENS0_5ChildENS0_8NodeKindE>
 8135bff:      	movq	(%rbx), %rax
 8135c02:      	movq	%rbx, %rdi
 8135c05:      	callq	*0x50(%rax)
 8135c08:      	addl	%ebp, %eax
 8135c0a:      	addl	0x20(%rbx), %eax
 8135c0d:      	movl	0x10(%rbx), %ecx
 8135c10:      	subl	%eax, %r15d
 8135c13:      	leal	0x10(%r15,%rcx), %r14d
 8135c18:      	cmpl	$0x50, %r14d
 8135c1c:      	jae	0x8135c32 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xa2>
 8135c1e:      	movl	%r14d, %edx
 8135c21:      	leaq	-0x66910f8(%rip), %rsi  # 0x1aa4b30 <_ZZL13write_paddingILc32EERN4llvm11raw_ostreamES2_jE5Chars.llvm.13088000499810600276>
 8135c28:      	movq	%rbx, %rdi
 8135c2b:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135c30:      	jmp	0x8135c60 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xd0>
 8135c32:      	leaq	-0x6691109(%rip), %r15  # 0x1aa4b30 <_ZZL13write_paddingILc32EERN4llvm11raw_ostreamES2_jE5Chars.llvm.13088000499810600276>
 8135c39:      	nopl	(%rax)
 8135c40:      	cmpl	$0x4f, %r14d
 8135c44:      	movl	$0x4f, %ebp
 8135c49:      	cmovbl	%r14d, %ebp
 8135c4d:      	movq	%rbx, %rdi
 8135c50:      	movq	%r15, %rsi
 8135c53:      	movq	%rbp, %rdx
 8135c56:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135c5b:      	subl	%ebp, %r14d
 8135c5e:      	jne	0x8135c40 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0xb0>
 8135c60:      	addl	$-0x3c, %r12d
 8135c64:      	addq	0x70(%rsp), %r13
 8135c69:      	movq	%rbx, %rdi
 8135c6c:      	movq	0x18(%rsp), %rsi
 8135c71:      	movl	0xc(%rsp), %edx
 8135c75:      	movl	0x60(%rsp), %ecx
 8135c79:      	movl	0x68(%rsp), %r8d
 8135c7e:      	movq	%r13, %r9
 8135c81:      	callq	0x8135d50 <_ZL23printRestOfMemberHeaderRN4llvm11raw_ostreamERKNSt6chrono10time_pointINS2_3_V212system_clockENS2_8durationIlSt5ratioILl1ELl1EEEEEEjjjm>
 8135c86:      	movq	0x18(%rbx), %rax
 8135c8a:      	movq	0x20(%rbx), %rdi
 8135c8e:      	subq	%rdi, %rax
 8135c91:      	movq	0x20(%rsp), %rdx
 8135c96:      	cmpq	%rax, %rdx
 8135c99:      	jbe	0x8135caa <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x11a>
 8135c9b:      	movq	%rbx, %rdi
 8135c9e:      	movq	0x10(%rsp), %rsi
 8135ca3:      	callq	0x4143f80 <_ZN4llvm11raw_ostream5writeEPKcm>
 8135ca8:      	jmp	0x8135cc0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x130>
 8135caa:      	testq	%rdx, %rdx
 8135cad:      	je	0x8135cc0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x130>
 8135caf:      	movq	0x10(%rsp), %rsi
 8135cb4:      	movq	%rdx, %r14
 8135cb7:      	callq	0x828ac50 <memcpy@plt>
 8135cbc:      	addq	%r14, 0x20(%rbx)
 8135cc0:      	testl	%r12d, %r12d
 8135cc3:      	je	0x8135d36 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x1a6>
 8135cc5:      	leaq	0xb(%rsp), %r14
 8135cca:      	nopw	(%rax,%rax)
 8135cd0:      	movq	0x20(%rbx), %rdx
 8135cd4:      	cmpq	0x18(%rbx), %rdx
 8135cd8:      	jae	0x8135cec <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x15c>
 8135cda:      	leaq	0x1(%rdx), %rax
 8135cde:      	movq	%rax, 0x20(%rbx)
 8135ce2:      	movb	$0x0, (%rdx)
 8135ce5:      	decl	%r12d
 8135ce8:      	jne	0x8135cd0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135cea:      	jmp	0x8135d36 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x1a6>
 8135cec:      	movq	0x10(%rbx), %rsi
 8135cf0:      	testq	%rsi, %rsi
 8135cf3:      	je	0x8135d0b <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x17b>
 8135cf5:      	subq	%rsi, %rdx
 8135cf8:      	movq	%rsi, 0x20(%rbx)
 8135cfc:      	movq	(%rbx), %rax
 8135cff:      	movq	%rbx, %rdi
 8135d02:      	callq	*0x48(%rax)
 8135d05:      	movq	0x20(%rbx), %rdx
 8135d09:      	jmp	0x8135cda <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x14a>
 8135d0b:      	cmpl	$0x0, 0x2c(%rbx)
 8135d0f:      	je	0x8135d1b <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x18b>
 8135d11:      	movq	%rbx, %rdi
 8135d14:      	callq	0x4143150 <_ZN4llvm11raw_ostream11SetBufferedEv>
 8135d19:      	jmp	0x8135cd0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135d1b:      	movb	$0x0, 0xb(%rsp)
 8135d20:      	movq	(%rbx), %rax
 8135d23:      	movl	$0x1, %edx
 8135d28:      	movq	%rbx, %rdi
 8135d2b:      	movq	%r14, %rsi
 8135d2e:      	callq	*0x48(%rax)
 8135d31:      	decl	%r12d
 8135d34:      	jne	0x8135cd0 <_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm+0x140>
 8135d36:      	addq	$0x28, %rsp
 8135d3a:      	popq	%rbx
 8135d3b:      	popq	%r12
 8135d3d:      	popq	%r13
 8135d3f:      	popq	%r14
 8135d41:      	popq	%r15
 8135d43:      	popq	%rbp
 8135d44:      	retq
