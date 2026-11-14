
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004317860 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_>:
 4317860:      	testq	%rsi, %rsi
 4317863:      	je	0x43179fa <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x19a>
 4317869:      	pushq	%rbp
 431786a:      	pushq	%r15
 431786c:      	pushq	%r14
 431786e:      	pushq	%r13
 4317870:      	pushq	%r12
 4317872:      	pushq	%rbx
 4317873:      	pushq	%rax
 4317874:      	movq	%rsi, %r12
 4317877:      	movq	%rdi, %r15
 431787a:      	leaq	(%rdi,%rsi), %rbx
 431787e:      	bsrq	%rsi, %rdx
 4317882:      	xorl	$0x3f, %edx
 4317885:      	addl	%edx, %edx
 4317887:      	xorq	$0x7e, %rdx
 431788b:      	movq	%rbx, %rsi
 431788e:      	callq	0x4324e20 <_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPcNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEElNS0_5__ops15_Iter_less_iterEEvT_SC_T0_T1_>
 4317893:      	leaq	0x1(%r15), %r14
 4317897:      	cmpq	$0x11, %r12
 431789b:      	jl	0x43178b2 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x52>
 431789d:      	movq	%r12, (%rsp)
 43178a1:      	movl	$0x1, %r13d
 43178a7:      	movq	%r14, %rbp
 43178aa:      	movq	%r15, %r14
 43178ad:      	jmp	0x4317962 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x102>
 43178b2:      	cmpq	$0x1, %r12
 43178b6:      	je	0x43179ec <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 43178bc:      	movq	%r14, %rax
 43178bf:      	movq	%r15, %r12
 43178c2:      	jmp	0x43178fb <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x9b>
 43178c4:      	nopw	%cs:(%rax,%rax)
 43178ce:      	nop
 43178d0:      	movq	%r12, %rdx
 43178d3:      	subq	%r15, %rdx
 43178d6:      	cmpq	$0x2, %rdx
 43178da:      	jl	0x4317930 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xd0>
 43178dc:      	movq	%r14, %rdi
 43178df:      	movq	%r15, %rsi
 43178e2:      	callq	0x828ac50 <memmove@plt>
 43178e7:      	movq	%r15, %rax
 43178ea:      	movb	%bpl, (%rax)
 43178ed:      	leaq	0x1(%r12), %rax
 43178f2:      	cmpq	%rbx, %rax
 43178f5:      	je	0x43179ec <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 43178fb:      	movq	%r12, %rcx
 43178fe:      	movq	%rax, %r12
 4317901:      	movzbl	(%rax), %ebp
 4317904:      	movzbl	(%r15), %esi
 4317908:      	cmpb	%sil, %bpl
 431790b:      	jl	0x43178d0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x70>
 431790d:      	movzbl	(%rcx), %ecx
 4317910:      	movq	%r12, %rax
 4317913:      	cmpb	%cl, %bpl
 4317916:      	jge	0x43178ea <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8a>
 4317918:      	movq	%r12, %rax
 431791b:      	nopl	(%rax,%rax)
 4317920:      	movb	%cl, (%rax)
 4317922:      	movzbl	-0x2(%rax), %ecx
 4317926:      	decq	%rax
 4317929:      	cmpb	%cl, %bpl
 431792c:      	jl	0x4317920 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xc0>
 431792e:      	jmp	0x43178ea <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8a>
 4317930:      	movq	%r15, %rax
 4317933:      	cmpq	$0x1, %rdx
 4317937:      	jne	0x43178ea <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x8a>
 4317939:      	movb	%sil, 0x1(%rcx)
 431793d:      	jmp	0x43178e7 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x87>
 431793f:      	movb	%cl, 0x1(%rax)
 4317942:      	nopw	%cs:(%rax,%rax)
 431794c:      	nopl	(%rax)
 4317950:      	movq	%r15, %rax
 4317953:      	movb	%r12b, (%rax)
 4317956:      	incq	%r13
 4317959:      	incq	%rbp
 431795c:      	cmpq	$0x10, %r13
 4317960:      	je	0x43179b0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x150>
 4317962:      	movq	%r14, %rax
 4317965:      	leaq	(%r15,%r13), %r14
 4317969:      	movzbl	(%r15,%r13), %r12d
 431796e:      	movzbl	(%r15), %ecx
 4317972:      	cmpb	%cl, %r12b
 4317975:      	jge	0x4317990 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x130>
 4317977:      	cmpq	$0x2, %r13
 431797b:      	jb	0x431793f <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xdf>
 431797d:      	leaq	0x1(%r15), %rdi
 4317981:      	movq	%r15, %rsi
 4317984:      	movq	%r13, %rdx
 4317987:      	callq	0x828ac50 <memmove@plt>
 431798c:      	jmp	0x4317950 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf0>
 431798e:      	nop
 4317990:      	movzbl	(%rax), %ecx
 4317993:      	movq	%r14, %rax
 4317996:      	cmpb	%cl, %r12b
 4317999:      	jge	0x4317953 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf3>
 431799b:      	movq	%rbp, %rax
 431799e:      	nop
 43179a0:      	movb	%cl, (%rax)
 43179a2:      	movzbl	-0x2(%rax), %ecx
 43179a6:      	decq	%rax
 43179a9:      	cmpb	%cl, %r12b
 43179ac:      	jl	0x43179a0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x140>
 43179ae:      	jmp	0x4317953 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0xf3>
 43179b0:      	leaq	0x10(%r15), %rax
 43179b4:      	movq	(%rsp), %rsi
 43179b8:      	testb	$0x1, %sil
 43179bc:      	je	0x43179e6 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x186>
 43179be:      	movzbl	0xf(%r15), %edx
 43179c3:      	movzbl	0x10(%r15), %ecx
 43179c8:      	cmpb	%dl, %cl
 43179ca:      	jge	0x43179dd <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x17d>
 43179cc:      	nopl	(%rax)
 43179d0:      	movb	%dl, (%rax)
 43179d2:      	movzbl	-0x2(%rax), %edx
 43179d6:      	decq	%rax
 43179d9:      	cmpb	%dl, %cl
 43179db:      	jl	0x43179d0 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x170>
 43179dd:      	movb	%cl, (%rax)
 43179df:      	addq	$0x11, %r15
 43179e3:      	movq	%r15, %rax
 43179e6:      	cmpq	$0x11, %rsi
 43179ea:      	jne	0x43179fb <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x19b>
 43179ec:      	addq	$0x8, %rsp
 43179f0:      	popq	%rbx
 43179f1:      	popq	%r12
 43179f3:      	popq	%r13
 43179f5:      	popq	%r14
 43179f7:      	popq	%r15
 43179f9:      	popq	%rbp
 43179fa:      	retq
 43179fb:      	leaq	0x1(%rax), %rcx
 43179ff:      	jmp	0x4317a23 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1c3>
 4317a01:      	nopw	%cs:(%rax,%rax)
 4317a0b:      	nopl	(%rax,%rax)
 4317a10:      	leaq	0x1(%rax), %rsi
 4317a14:      	movb	%dl, (%rsi)
 4317a16:      	addq	$0x2, %rax
 4317a1a:      	addq	$0x2, %rcx
 4317a1e:      	cmpq	%rbx, %rax
 4317a21:      	je	0x43179ec <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x18c>
 4317a23:      	movzbl	-0x1(%rax), %esi
 4317a27:      	movzbl	(%rax), %edx
 4317a2a:      	movq	%rax, %rdi
 4317a2d:      	cmpb	%sil, %dl
 4317a30:      	jge	0x4317a4f <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1ef>
 4317a32:      	movq	%rax, %rdi
 4317a35:      	nopw	%cs:(%rax,%rax)
 4317a3f:      	nop
 4317a40:      	movb	%sil, (%rdi)
 4317a43:      	movzbl	-0x2(%rdi), %esi
 4317a47:      	decq	%rdi
 4317a4a:      	cmpb	%sil, %dl
 4317a4d:      	jl	0x4317a40 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1e0>
 4317a4f:      	movb	%dl, (%rdi)
 4317a51:      	movzbl	(%rax), %edi
 4317a54:      	movzbl	0x1(%rax), %edx
 4317a58:      	cmpb	%dil, %dl
 4317a5b:      	jge	0x4317a10 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1b0>
 4317a5d:      	movq	%rcx, %rsi
 4317a60:      	movb	%dil, (%rsi)
 4317a63:      	movzbl	-0x2(%rsi), %edi
 4317a67:      	decq	%rsi
 4317a6a:      	cmpb	%dil, %dl
 4317a6d:      	jl	0x4317a60 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x200>
 4317a6f:      	jmp	0x4317a14 <_ZN4llvm4sortIRNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEvOT_+0x1b4>
