
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000043177d0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_>:
 43177d0:      	testq	%rsi, %rsi
 43177d3:      	je	0x431796a <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x19a>
 43177d9:      	pushq	%rbp
 43177da:      	pushq	%r15
 43177dc:      	pushq	%r14
 43177de:      	pushq	%r13
 43177e0:      	pushq	%r12
 43177e2:      	pushq	%rbx
 43177e3:      	pushq	%rax
 43177e4:      	movq	%rsi, %r14
 43177e7:      	movq	%rdi, %r12
 43177ea:      	leaq	(%rdi,%rsi), %rbx
 43177ee:      	bsrq	%rsi, %rdx
 43177f2:      	xorl	$0x3f, %edx
 43177f5:      	addl	%edx, %edx
 43177f7:      	xorq	$0x7e, %rdx
 43177fb:      	movq	%rbx, %rsi
 43177fe:      	callq	0x4324d90 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPcNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEElNS0_5__ops15_Iter_less_iterEEvT_SC_T0_T1_>
 4317803:      	cmpq	$0x11, %r14
 4317807:      	jl	0x4317820 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x50>
 4317809:      	movq	%r14, (%rsp)
 431780d:      	leaq	0x1(%r12), %rbp
 4317812:      	movl	$0x1, %r13d
 4317818:      	movq	%r12, %r14
 431781b:      	jmp	0x43178d2 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x102>
 4317820:      	cmpq	$0x1, %r14
 4317824:      	je	0x431795c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 431782a:      	leaq	0x1(%r12), %rax
 431782f:      	movq	%r12, %r14
 4317832:      	jmp	0x431786c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x9c>
 4317834:      	nopw	%cs:(%rax,%rax)
 431783e:      	nop
 4317840:      	movq	%r14, %rdx
 4317843:      	subq	%r12, %rdx
 4317846:      	cmpq	$0x2, %rdx
 431784a:      	jl	0x43178a0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xd0>
 431784c:      	leaq	0x1(%r12), %rdi
 4317851:      	movq	%r12, %rsi
 4317854:      	callq	0x828abc0 <memmove@plt>
 4317859:      	movq	%r12, %rax
 431785c:      	movb	%bpl, (%rax)
 431785f:      	leaq	0x1(%r14), %rax
 4317863:      	cmpq	%rbx, %rax
 4317866:      	je	0x431795c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 431786c:      	movq	%r14, %rcx
 431786f:      	movq	%rax, %r14
 4317872:      	movzbl	0x1(%rcx), %ebp
 4317876:      	movzbl	(%r12), %esi
 431787b:      	cmpb	%sil, %bpl
 431787e:      	jl	0x4317840 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x70>
 4317880:      	movzbl	(%rcx), %ecx
 4317883:      	movq	%r14, %rax
 4317886:      	cmpb	%cl, %bpl
 4317889:      	jge	0x431785c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8c>
 431788b:      	movq	%r14, %rax
 431788e:      	nop
 4317890:      	movb	%cl, (%rax)
 4317892:      	movzbl	-0x2(%rax), %ecx
 4317896:      	decq	%rax
 4317899:      	cmpb	%cl, %bpl
 431789c:      	jl	0x4317890 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xc0>
 431789e:      	jmp	0x431785c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8c>
 43178a0:      	movq	%r12, %rax
 43178a3:      	cmpq	$0x1, %rdx
 43178a7:      	jne	0x431785c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8c>
 43178a9:      	movb	%sil, 0x1(%rcx)
 43178ad:      	jmp	0x4317859 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x89>
 43178af:      	movb	%cl, 0x1(%rax)
 43178b2:      	nopw	%cs:(%rax,%rax)
 43178bc:      	nopl	(%rax)
 43178c0:      	movq	%r12, %rax
 43178c3:      	movb	%r15b, (%rax)
 43178c6:      	incq	%r13
 43178c9:      	incq	%rbp
 43178cc:      	cmpq	$0x10, %r13
 43178d0:      	je	0x4317920 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x150>
 43178d2:      	movq	%r14, %rax
 43178d5:      	leaq	(%r12,%r13), %r14
 43178d9:      	movzbl	(%r12,%r13), %r15d
 43178de:      	movzbl	(%r12), %ecx
 43178e3:      	cmpb	%cl, %r15b
 43178e6:      	jge	0x4317900 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x130>
 43178e8:      	cmpq	$0x2, %r13
 43178ec:      	jb	0x43178af <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xdf>
 43178ee:      	leaq	0x1(%r12), %rdi
 43178f3:      	movq	%r12, %rsi
 43178f6:      	movq	%r13, %rdx
 43178f9:      	callq	0x828abc0 <memmove@plt>
 43178fe:      	jmp	0x43178c0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf0>
 4317900:      	movzbl	(%rax), %ecx
 4317903:      	movq	%r14, %rax
 4317906:      	cmpb	%cl, %r15b
 4317909:      	jge	0x43178c3 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf3>
 431790b:      	movq	%rbp, %rax
 431790e:      	nop
 4317910:      	movb	%cl, (%rax)
 4317912:      	movzbl	-0x2(%rax), %ecx
 4317916:      	decq	%rax
 4317919:      	cmpb	%cl, %r15b
 431791c:      	jl	0x4317910 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x140>
 431791e:      	jmp	0x43178c3 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf3>
 4317920:      	leaq	0x10(%r12), %rax
 4317925:      	movq	(%rsp), %rsi
 4317929:      	testb	$0x1, %sil
 431792d:      	je	0x4317956 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x186>
 431792f:      	movzbl	0xf(%r12), %edx
 4317935:      	movzbl	0x10(%r12), %ecx
 431793b:      	cmpb	%dl, %cl
 431793d:      	jge	0x431794d <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x17d>
 431793f:      	nop
 4317940:      	movb	%dl, (%rax)
 4317942:      	movzbl	-0x2(%rax), %edx
 4317946:      	decq	%rax
 4317949:      	cmpb	%dl, %cl
 431794b:      	jl	0x4317940 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x170>
 431794d:      	movb	%cl, (%rax)
 431794f:      	addq	$0x11, %r12
 4317953:      	movq	%r12, %rax
 4317956:      	cmpq	$0x11, %rsi
 431795a:      	jne	0x431796b <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x19b>
 431795c:      	addq	$0x8, %rsp
 4317960:      	popq	%rbx
 4317961:      	popq	%r12
 4317963:      	popq	%r13
 4317965:      	popq	%r14
 4317967:      	popq	%r15
 4317969:      	popq	%rbp
 431796a:      	retq
 431796b:      	leaq	0x1(%rax), %rcx
 431796f:      	jmp	0x4317993 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1c3>
 4317971:      	nopw	%cs:(%rax,%rax)
 431797b:      	nopl	(%rax,%rax)
 4317980:      	leaq	0x1(%rax), %rsi
 4317984:      	movb	%dl, (%rsi)
 4317986:      	addq	$0x2, %rax
 431798a:      	addq	$0x2, %rcx
 431798e:      	cmpq	%rbx, %rax
 4317991:      	je	0x431795c <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 4317993:      	movzbl	-0x1(%rax), %esi
 4317997:      	movzbl	(%rax), %edx
 431799a:      	movq	%rax, %rdi
 431799d:      	cmpb	%sil, %dl
 43179a0:      	jge	0x43179bf <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1ef>
 43179a2:      	movq	%rax, %rdi
 43179a5:      	nopw	%cs:(%rax,%rax)
 43179af:      	nop
 43179b0:      	movb	%sil, (%rdi)
 43179b3:      	movzbl	-0x2(%rdi), %esi
 43179b7:      	decq	%rdi
 43179ba:      	cmpb	%sil, %dl
 43179bd:      	jl	0x43179b0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1e0>
 43179bf:      	movb	%dl, (%rdi)
 43179c1:      	movzbl	(%rax), %edi
 43179c4:      	movzbl	0x1(%rax), %edx
 43179c8:      	cmpb	%dil, %dl
 43179cb:      	jge	0x4317980 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1b0>
 43179cd:      	movq	%rcx, %rsi
 43179d0:      	movb	%dil, (%rsi)
 43179d3:      	movzbl	-0x2(%rsi), %edi
 43179d7:      	decq	%rsi
 43179da:      	cmpb	%dil, %dl
 43179dd:      	jl	0x43179d0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x200>
 43179df:      	jmp	0x4317984 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1b4>
