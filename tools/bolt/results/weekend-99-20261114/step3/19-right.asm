
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000040626b0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv>:
 40626b0:      	pushq	%rbp
 40626b1:      	pushq	%r15
 40626b3:      	pushq	%r14
 40626b5:      	pushq	%r13
 40626b7:      	pushq	%r12
 40626b9:      	pushq	%rbx
 40626ba:      	subq	$0xa8, %rsp
 40626c1:      	movq	%rdi, %rbx
 40626c4:      	movq	0x38(%rdi), %rax
 40626c8:      	cmpq	%rax, 0x40(%rdi)
 40626cc:      	je	0x40626d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x22>
 40626ce:      	movq	%rax, 0x40(%rbx)
 40626d2:      	movq	0x58(%rbx), %r15
 40626d6:      	cmpq	%r15, 0x50(%rbx)
 40626da:      	je	0x40644ea <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e3a>
 40626e0:      	leaq	0x8(%rbx), %rax
 40626e4:      	movq	%rax, 0x78(%rsp)
 40626e9:      	movq	%rbx, 0x28(%rsp)
 40626ee:      	jmp	0x4062710 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 40626f0:      	movq	%rbx, %rdx
 40626f3:      	movq	0x28(%rsp), %rbx
 40626f8:      	movq	%rbx, %rdi
 40626fb:      	movq	%rbp, %rsi
 40626fe:      	callq	0x4061f30 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE11DFSVisitOneES9_>
 4062703:      	movq	0x58(%rbx), %r15
 4062707:      	nopw	(%rax,%rax)
 4062710:      	movq	-0x60(%r15), %rcx
 4062714:      	movq	-0x58(%r15), %rax
 4062718:      	movq	%rax, 0x58(%rsp)
 406271d:      	movq	(%rcx), %rdx
 4062720:      	movl	%edx, %edi
 4062722:      	shrl	%edi
 4062724:      	andl	$0x2, %edi
 4062727:      	movq	%rdi, %r13
 406272a:      	orq	%rcx, %r13
 406272d:      	movq	%rdx, %r14
 4062730:      	andq	$-0x8, %rdx
 4062734:      	movq	0x30(%rdx), %rax
 4062738:      	addq	$0x30, %rdx
 406273c:      	cmpq	%rax, %rdx
 406273f:      	movq	%r15, 0x30(%rsp)
 4062744:      	je	0x4062800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x150>
 406274a:      	leaq	-0x18(%rax), %rbx
 406274e:      	movzbl	-0x18(%rax), %r9d
 4062753:      	leal	-0x1e(%r9), %r10d
 4062757:      	cmpb	$0xb, %r10b
 406275b:      	movl	$0x0, %ebp
 4062760:      	cmovbq	%rbx, %rbp
 4062764:      	movq	%rcx, %r11
 4062767:      	andq	$-0x8, %r11
 406276b:      	testq	%rdi, %rdi
 406276e:      	jne	0x406282a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x17a>
 4062774:      	cmpb	$0xa, %r10b
 4062778:      	ja	0x4062910 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 406277e:      	movzbl	%r9b, %edi
 4062782:      	leal	-0x1e(%rdi), %r8d
 4062786:      	leaq	-0x25c42d9(%rip), %rsi  # 0x1a9e4b4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0xb4>
 406278d:      	movslq	(%rsi,%r8,4), %r8
 4062791:      	addq	%rsi, %r8
 4062794:      	jmpq	*%r8
 4062797:      	movl	-0x14(%rax), %r8d
 406279b:      	movl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 40627a0:      	andl	%esi, %r8d
 40627a3:      	decl	%r8d
 40627a6:      	testl	%r8d, %r8d
 40627a9:      	je	0x4062910 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 40627af:      	movq	0x8(%r11), %r9
 40627b3:      	movq	0x20(%r9), %r10
 40627b7:      	leaq	-0x16(%rax), %rsi
 40627bb:      	movq	%rsi, 0x50(%rsp)
 40627c0:      	leaq	-0x14(%rax), %r9
 40627c4:      	leaq	-0x20(%rax), %rsi
 40627c8:      	movq	%rsi, 0x38(%rsp)
 40627cd:      	leaq	0x40(%rax), %rsi
 40627d1:      	movq	%rsi, 0x18(%rsp)
 40627d6:      	movl	%r8d, %r15d
 40627d9:      	leal	-0x20(%rdi), %r11d
 40627dd:      	leaq	-0x25c4304(%rip), %rsi  # 0x1a9e4e0 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0xe0>
 40627e4:      	movslq	(%rsi,%r11,4), %r11
 40627e8:      	addq	%rsi, %r11
 40627eb:      	jmpq	*%r11
 40627ee:      	leaq	-0x20(%rax), %rsi
 40627f2:      	movq	(%rsi), %r11
 40627f5:      	movq	0x20(%r11), %r11
 40627f9:      	jmp	0x4063f50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a0>
 40627fe:      	nop
 4062800:      	testq	%rdi, %rdi
 4062803:      	jne	0x4062821 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x171>
 4062805:      	andl	$0x4, %r14d
 4062809:      	orq	%rcx, %r14
 406280c:      	movq	%r14, 0x48(%rsp)
 4062811:      	movq	$0x0, 0x8(%rsp)
 406281a:      	xorl	%ebp, %ebp
 406281c:      	jmp	0x4062950 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 4062821:      	movq	%rcx, %r11
 4062824:      	andq	$-0x8, %r11
 4062828:      	xorl	%ebp, %ebp
 406282a:      	movq	0x8(%r11), %rsi
 406282e:      	movq	0x20(%rsi), %rsi
 4062832:      	movq	%rcx, %rdi
 4062835:      	orq	$0x4, %rdi
 4062839:      	cmpq	0x20(%r11), %rsi
 406283d:      	cmoveq	%rdi, %r13
 4062841:      	movq	$0x0, 0x8(%rsp)
 406284a:      	andl	$0x4, %r14d
 406284e:      	orq	%rcx, %r14
 4062851:      	movq	%r14, 0x48(%rsp)
 4062856:      	cmpq	%rax, %rdx
 4062859:      	je	0x4062950 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 406285f:      	movzbl	-0x18(%rax), %r9d
 4062864:      	leal	-0x1e(%r9), %r10d
 4062868:      	cmpb	$0xa, %r10b
 406286c:      	ja	0x4062950 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 4062872:      	jmp	0x406292b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x27b>
 4062877:      	movq	0x8(%r11), %r8
 406287b:      	movq	0x20(%r8), %r10
 406287f:      	leaq	-0x16(%rax), %rsi
 4062883:      	movq	%rsi, 0x50(%rsp)
 4062888:      	leaq	-0x14(%rax), %r9
 406288c:      	leaq	-0x38(%rax), %rsi
 4062890:      	leaq	-0x20(%rax), %r8
 4062894:      	movq	%r8, 0x38(%rsp)
 4062899:      	leaq	0x40(%rax), %r8
 406289d:      	movq	%r8, 0x18(%rsp)
 40628a2:      	movl	$0x1, %r8d
 40628a8:      	movl	$0x1, %r15d
 40628ae:      	movq	(%rsi), %r11
 40628b1:      	jmp	0x4063f54 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a4>
 40628b6:      	movq	0x8(%r11), %r8
 40628ba:      	movq	0x20(%r8), %r10
 40628be:      	leaq	-0x16(%rax), %rsi
 40628c2:      	movq	%rsi, 0x50(%rsp)
 40628c7:      	leaq	-0x14(%rax), %r9
 40628cb:      	leaq	-0x38(%rax), %rsi
 40628cf:      	leaq	-0x20(%rax), %r8
 40628d3:      	movq	%r8, 0x38(%rsp)
 40628d8:      	leaq	0x40(%rax), %r8
 40628dc:      	movq	%r8, 0x18(%rsp)
 40628e1:      	movl	$0x2, %r8d
 40628e7:      	movl	$0x2, %r15d
 40628ed:      	movq	-0x78(%rax), %r11
 40628f1:      	jmp	0x4063f54 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a4>
 40628f6:      	movl	0x40(%rax), %r8d
 40628fa:      	incl	%r8d
 40628fd:      	testl	%r8d, %r8d
 4062900:      	jne	0x40627af <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xff>
 4062906:      	nopw	%cs:(%rax,%rax)
 4062910:      	andl	$0x4, %r14d
 4062914:      	orq	%rcx, %r14
 4062917:      	movq	%r14, 0x48(%rsp)
 406291c:      	movq	$0x0, 0x8(%rsp)
 4062925:      	cmpb	$0xa, %r10b
 4062929:      	ja	0x4062950 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 406292b:      	movzbl	%r9b, %ecx
 406292f:      	addl	$-0x1e, %ecx
 4062932:      	leaq	-0x25c440d(%rip), %rdx  # 0x1a9e52c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x12c>
 4062939:      	movslq	(%rdx,%rcx,4), %rcx
 406293d:      	addq	%rdx, %rcx
 4062940:      	jmpq	*%rcx
 4062942:      	nopw	%cs:(%rax,%rax)
 406294c:      	nopl	(%rax)
 4062950:      	xorl	%esi, %esi
 4062952:      	cmpq	$0x0, 0x58(%rsp)
 4062958:      	leaq	0x2171(%rip), %rcx      # 0x4064ad0 <_ZN12_GLOBAL__N_114SubGraphTraits9filterSetERKSt4pairIPN4llvm10RegionNodeEPNS2_13SmallDenseSetIS4_Lj4ENS2_12DenseMapInfoIS4_vEEEEE>
 406295f:      	leaq	0x21da(%rip), %rax      # 0x4064b40 <_ZN12_GLOBAL__N_114SubGraphTraits9filterAllERKSt4pairIPN4llvm10RegionNodeEPNS2_13SmallDenseSetIS4_Lj4ENS2_12DenseMapInfoIS4_vEEEEE>
 4062966:      	cmoveq	%rax, %rcx
 406296a:      	movq	%rcx, 0x38(%rsp)
 406296f:      	movl	%r13d, %eax
 4062972:      	xorl	0x48(%rsp), %eax
 4062976:      	xorl	%ecx, %ecx
 4062978:      	testb	$0x6, %al
 406297a:      	setne	%cl
 406297d:      	xorl	%edx, %edx
 406297f:      	movl	%esi, 0x18(%rsp)
 4062983:      	cmpl	%esi, 0x8(%rsp)
 4062987:      	setne	%dl
 406298a:      	testb	$0x6, %r13b
 406298e:      	sete	%al
 4062991:      	cmovel	%edx, %ecx
 4062994:      	cmpb	$0x1, %cl
 4062997:      	jne	0x4063020 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x970>
 406299d:      	movq	0x48(%rsp), %rcx
 40629a2:      	andl	$0x6, %ecx
 40629a5:      	movq	%rcx, 0x50(%rsp)
 40629aa:      	leaq	-0x20(%rbp), %rcx
 40629ae:      	movq	%rcx, 0x20(%rsp)
 40629b3:      	movq	%rbp, 0x10(%rsp)
 40629b8:      	movq	0x8(%rsp), %rcx
 40629bd:      	leal	0x1(%rcx), %esi
 40629c0:      	movq	%rsi, 0x88(%rsp)
 40629c8:      	xorl	%edx, %edx
 40629ca:      	movl	%ecx, %edi
 40629cc:      	subl	$0x1, %edi
 40629cf:      	setae	%dl
 40629d2:      	shll	$0x5, %edx
 40629d5:      	addq	$-0x60, %rdx
 40629d9:      	movq	%rdx, 0xa0(%rsp)
 40629e1:      	movl	%ecx, %ecx
 40629e3:      	movq	%rcx, 0x80(%rsp)
 40629eb:      	shlq	$0x5, %rcx
 40629ef:      	movq	0x20(%rsp), %rdx
 40629f4:      	movq	%rdx, %r8
 40629f7:      	subq	%rcx, %r8
 40629fa:      	movq	%r8, 0x98(%rsp)
 4062a02:      	shlq	$0x5, %rdi
 4062a06:      	addq	%rdx, %rdi
 4062a09:      	movq	%rdi, 0x90(%rsp)
 4062a11:      	shlq	$0x5, %rsi
 4062a15:      	movq	%rsi, 0x70(%rsp)
 4062a1a:      	nopw	(%rax,%rax)
 4062a20:      	testb	$0x1, %al
 4062a22:      	je	0x4062a50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x3a0>
 4062a24:      	movzbl	(%rbp), %eax
 4062a28:      	addl	$-0x1f, %eax
 4062a2b:      	leaq	-0x25c44da(%rip), %rcx  # 0x1a9e558 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x158>
 4062a32:      	movslq	(%rcx,%rax,4), %rax
 4062a36:      	addq	%rcx, %rax
 4062a39:      	jmpq	*%rax
 4062a3b:      	movq	-0x8(%rbp), %rax
 4062a3f:      	movq	0x70(%rsp), %rcx
 4062a44:      	movq	(%rax,%rcx), %r14
 4062a48:      	jmp	0x4062aca <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x41a>
 4062a4d:      	nopl	(%rax)
 4062a50:      	movq	%r13, %rax
 4062a53:      	andq	$-0x8, %rax
 4062a57:      	movq	0x20(%rax), %r14
 4062a5b:      	jmp	0x4062ad1 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x421>
 4062a5d:      	movq	0xa0(%rsp), %rax
 4062a65:      	movq	(%rbp,%rax), %r14
 4062a6a:      	jmp	0x4062aca <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x41a>
 4062a6c:      	cmpl	$0x0, 0x8(%rsp)
 4062a71:      	je	0x4062ab8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x408>
 4062a73:      	movl	0x58(%rbp), %eax
 4062a76:      	shlq	$0x5, %rax
 4062a7a:      	movq	0x90(%rsp), %rcx
 4062a82:      	subq	%rax, %rcx
 4062a85:      	movq	(%rcx), %r14
 4062a88:      	jmp	0x4062aca <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x41a>
 4062a8a:      	testb	$0x1, 0x2(%rbp)
 4062a8e:      	jne	0x4062aa6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x3f6>
 4062a90:      	xorl	%r14d, %r14d
 4062a93:      	jmp	0x4062aca <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x41a>
 4062a95:      	movq	0x98(%rsp), %rax
 4062a9d:      	jmp	0x4062ac7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x417>
 4062a9f:      	movq	0x20(%rsp), %rax
 4062aa4:      	jmp	0x4062ac7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x417>
 4062aa6:      	movl	0x4(%rbp), %eax
 4062aa9:      	shll	$0x5, %eax
 4062aac:      	movq	%rbp, %rcx
 4062aaf:      	subq	%rax, %rcx
 4062ab2:      	movq	0x20(%rcx), %r14
 4062ab6:      	jmp	0x4062aca <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x41a>
 4062ab8:      	movl	0x58(%rbp), %eax
 4062abb:      	shlq	$0x5, %rax
 4062abf:      	negq	%rax
 4062ac2:      	leaq	-0x40(%rbp,%rax), %rax
 4062ac7:      	movq	(%rax), %r14
 4062aca:      	movq	%r13, %rax
 4062acd:      	andq	$-0x8, %rax
 4062ad1:      	movq	0x8(%rax), %r12
 4062ad5:      	movq	0x10(%r12), %rax
 4062ada:      	movl	0x38(%rax), %ecx
 4062add:      	testl	%ecx, %ecx
 4062adf:      	je	0x4062b4c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x49c>
 4062ae1:      	movq	0x28(%rax), %rax
 4062ae5:      	movl	%r14d, %esi
 4062ae8:      	shrl	$0x4, %esi
 4062aeb:      	movl	%r14d, %edx
 4062aee:      	shrl	$0x9, %edx
 4062af1:      	xorl	%esi, %edx
 4062af3:      	decl	%ecx
 4062af5:      	andl	%ecx, %edx
 4062af7:      	movl	%edx, %esi
 4062af9:      	shll	$0x4, %esi
 4062afc:      	movq	(%rax,%rsi), %rdi
 4062b00:      	cmpq	%rdi, %r14
 4062b03:      	jne	0x4062cb2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x602>
 4062b09:      	shlq	$0x4, %rdx
 4062b0d:      	movq	0x8(%rax,%rdx), %rax
 4062b12:      	testq	%rax, %rax
 4062b15:      	je	0x4062b4c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x49c>
 4062b17:      	cmpq	%r12, %rax
 4062b1a:      	je	0x4062b4c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x49c>
 4062b1c:      	nopl	(%rax)
 4062b20:      	movq	%rax, %rbx
 4062b23:      	movq	0x8(%rax), %rsi
 4062b27:      	movq	%r12, %rdi
 4062b2a:      	callq	0x3361620 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 4062b2f:      	testb	%al, %al
 4062b31:      	je	0x4062b3c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x48c>
 4062b33:      	movq	0x8(%rbx), %rax
 4062b37:      	cmpq	%r12, %rax
 4062b3a:      	jne	0x4062b20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x470>
 4062b3c:      	movq	(%rbx), %rax
 4062b3f:      	andq	$-0x8, %rax
 4062b43:      	cmpq	%rax, %r14
 4062b46:      	je	0x4062c72 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5c2>
 4062b4c:      	movq	%r13, 0x40(%rsp)
 4062b51:      	movq	0x50(%r12), %rax
 4062b56:      	leaq	0x48(%r12), %rbp
 4062b5b:      	movq	%rbp, %r13
 4062b5e:      	testq	%rax, %rax
 4062b61:      	je	0x4062b96 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4e6>
 4062b63:      	movq	%rbp, %r13
 4062b66:      	nopw	%cs:(%rax,%rax)
 4062b70:      	xorl	%ecx, %ecx
 4062b72:      	cmpq	%r14, 0x20(%rax)
 4062b76:      	setb	%cl
 4062b79:      	cmovaeq	%rax, %r13
 4062b7d:      	movq	0x10(%rax,%rcx,8), %rax
 4062b82:      	testq	%rax, %rax
 4062b85:      	jne	0x4062b70 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4c0>
 4062b87:      	cmpq	%rbp, %r13
 4062b8a:      	je	0x4062b96 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4e6>
 4062b8c:      	cmpq	0x20(%r13), %r14
 4062b90:      	jae	0x4062c64 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5b4>
 4062b96:      	movq	%r13, %rbx
 4062b99:      	leaq	0x40(%r12), %r15
 4062b9e:      	movl	$0x30, %edi
 4062ba3:      	callq	0x828a620 <_Znwm@plt>
 4062ba8:      	movq	%rax, %r13
 4062bab:      	addq	$0x20, %rax
 4062baf:      	movq	%r14, 0x20(%r13)
 4062bb3:      	movq	$0x0, 0x28(%r13)
 4062bbb:      	movq	%r15, %rdi
 4062bbe:      	movq	%rax, %r15
 4062bc1:      	movq	%rbx, %rsi
 4062bc4:      	movq	%rax, %rdx
 4062bc7:      	callq	0x3369160 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 4062bcc:      	movq	%rax, %rbx
 4062bcf:      	testq	%rdx, %rdx
 4062bd2:      	je	0x4062c10 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x560>
 4062bd4:      	testq	%rbx, %rbx
 4062bd7:      	setne	%al
 4062bda:      	cmpq	%rbp, %rdx
 4062bdd:      	sete	%cl
 4062be0:      	orb	%al, %cl
 4062be2:      	movb	$0x1, %al
 4062be4:      	jne	0x4062bf0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x540>
 4062be6:      	movq	(%r15), %rax
 4062be9:      	cmpq	0x20(%rdx), %rax
 4062bed:      	setb	%al
 4062bf0:      	movzbl	%al, %edi
 4062bf3:      	movq	%r13, %rsi
 4062bf6:      	movq	%rbp, %rcx
 4062bf9:      	callq	0x828a750 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 4062bfe:      	incq	0x68(%r12)
 4062c03:      	jmp	0x4062c33 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x583>
 4062c05:      	nopw	%cs:(%rax,%rax)
 4062c0f:      	nop
 4062c10:      	movq	0x28(%r13), %rdi
 4062c14:      	testq	%rdi, %rdi
 4062c17:      	je	0x4062c23 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x573>
 4062c19:      	movl	$0x10, %esi
 4062c1e:      	callq	0x828a660 <_ZdlPvm@plt>
 4062c23:      	movl	$0x30, %esi
 4062c28:      	movq	%r13, %rdi
 4062c2b:      	callq	0x828a660 <_ZdlPvm@plt>
 4062c30:      	movq	%rbx, %r13
 4062c33:      	movq	0x30(%rsp), %r15
 4062c38:      	movl	$0x10, %edi
 4062c3d:      	callq	0x828a620 <_Znwm@plt>
 4062c42:      	andq	$-0x5, %r14
 4062c46:      	movq	%r14, (%rax)
 4062c49:      	movq	%r12, 0x8(%rax)
 4062c4d:      	movq	0x28(%r13), %rdi
 4062c51:      	movq	%rax, 0x28(%r13)
 4062c55:      	testq	%rdi, %rdi
 4062c58:      	je	0x4062c64 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5b4>
 4062c5a:      	movl	$0x10, %esi
 4062c5f:      	callq	0x828a660 <_ZdlPvm@plt>
 4062c64:      	movq	0x28(%r13), %rbx
 4062c68:      	movq	0x40(%rsp), %r13
 4062c6d:      	movq	0x10(%rsp), %rbp
 4062c72:      	movq	%rbx, 0x60(%rsp)
 4062c77:      	movq	0x58(%rsp), %rax
 4062c7c:      	movq	%rax, 0x68(%rsp)
 4062c81:      	leaq	0x60(%rsp), %rdi
 4062c86:      	callq	*0x38(%rsp)
 4062c8a:      	testb	%al, %al
 4062c8c:      	jne	0x4063020 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x970>
 4062c92:      	testb	$0x6, %r13b
 4062c96:      	je	0x4062ce0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x630>
 4062c98:      	andq	$-0x7, %r13
 4062c9c:      	orq	$0x4, %r13
 4062ca0:      	xorl	%eax, %eax
 4062ca2:      	cmpl	$0x4, 0x50(%rsp)
 4062ca7:      	jne	0x4062a20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x370>
 4062cad:      	jmp	0x4063020 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x970>
 4062cb2:      	movl	$0x1, %esi
 4062cb7:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4062cbe:      	je	0x4062b4c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x49c>
 4062cc4:      	addl	%esi, %edx
 4062cc6:      	incl	%esi
 4062cc8:      	andl	%ecx, %edx
 4062cca:      	movq	%rdx, %rdi
 4062ccd:      	shlq	$0x4, %rdi
 4062cd1:      	movq	(%rax,%rdi), %rdi
 4062cd5:      	cmpq	%rdi, %r14
 4062cd8:      	je	0x4062b09 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x459>
 4062cde:      	jmp	0x4062cb7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x607>
 4062ce0:      	movq	%r13, %rax
 4062ce3:      	andq	$-0x8, %rax
 4062ce7:      	movq	(%rax), %rdx
 4062cea:      	andq	$-0x8, %rdx
 4062cee:      	movq	0x30(%rdx), %rcx
 4062cf2:      	addq	$0x30, %rdx
 4062cf6:      	cmpq	%rcx, %rdx
 4062cf9:      	movq	0x88(%rsp), %r8
 4062d01:      	je	0x4062d35 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x685>
 4062d03:      	movzbl	-0x18(%rcx), %edx
 4062d07:      	leal	-0x1e(%rdx), %esi
 4062d0a:      	cmpb	$0xb, %sil
 4062d0e:      	jae	0x4062e00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x750>
 4062d14:      	addl	$-0x1e, %edx
 4062d17:      	leaq	-0x25c4776(%rip), %rsi  # 0x1a9e5a8 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x1a8>
 4062d1e:      	movslq	(%rsi,%rdx,4), %rdx
 4062d22:      	addq	%rsi, %rdx
 4062d25:      	jmpq	*%rdx
 4062d27:      	movq	$0x0, 0x8(%rsp)
 4062d30:      	jmp	0x4062efe <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x84e>
 4062d35:      	movq	0x80(%rsp), %r8
 4062d3d:      	leaq	0x1(%r8), %rcx
 4062d41:      	shlq	$0x5, %r8
 4062d45:      	addq	0x20(%rsp), %r8
 4062d4a:      	movl	0x18(%rsp), %edx
 4062d4e:      	jmp	0x4062d85 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6d5>
 4062d50:      	movq	-0x40(%rbp), %rdx
 4062d54:      	nopw	%cs:(%rax,%rax)
 4062d5e:      	nop
 4062d60:      	movq	0x8(%rax), %rsi
 4062d64:      	incq	%rcx
 4062d67:      	addq	$0x20, %r8
 4062d6b:      	movq	0x8(%rsp), %rdi
 4062d70:      	incl	%edi
 4062d72:      	movq	%rdi, 0x8(%rsp)
 4062d77:      	cmpq	%rdx, 0x20(%rsi)
 4062d7b:      	movl	0x18(%rsp), %edx
 4062d7f:      	jne	0x4062ff0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x940>
 4062d85:      	testl	%ecx, %ecx
 4062d87:      	je	0x4062ebc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x80c>
 4062d8d:      	movzbl	(%rbp), %edx
 4062d91:      	addl	$-0x1f, %edx
 4062d94:      	leaq	-0x25c479f(%rip), %rsi  # 0x1a9e5fc <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x1fc>
 4062d9b:      	movslq	(%rsi,%rdx,4), %rdx
 4062d9f:      	addq	%rsi, %rdx
 4062da2:      	jmpq	*%rdx
 4062da4:      	leal	0x1(%rcx), %edx
 4062da7:      	movq	-0x8(%rbp), %rsi
 4062dab:      	shlq	$0x5, %rdx
 4062daf:      	movq	(%rsi,%rdx), %rdx
 4062db3:      	jmp	0x4062d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6b0>
 4062db5:      	movl	0x58(%rbp), %edx
 4062db8:      	shlq	$0x5, %rdx
 4062dbc:      	movq	%r8, %rsi
 4062dbf:      	jmp	0x4062dd6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x726>
 4062dc1:      	testb	$0x1, 0x2(%rbp)
 4062dc5:      	jne	0x4062deb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x73b>
 4062dc7:      	xorl	%edx, %edx
 4062dc9:      	jmp	0x4062d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6b0>
 4062dcb:      	movl	%ecx, %edx
 4062dcd:      	shlq	$0x5, %rdx
 4062dd1:      	movq	0x20(%rsp), %rsi
 4062dd6:      	subq	%rdx, %rsi
 4062dd9:      	movq	(%rsi), %rdx
 4062ddc:      	jmp	0x4062d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6b0>
 4062dde:      	movq	0x20(%rsp), %rdx
 4062de3:      	movq	(%rdx), %rdx
 4062de6:      	jmp	0x4062d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6b0>
 4062deb:      	movl	0x4(%rbp), %edx
 4062dee:      	shll	$0x5, %edx
 4062df1:      	movq	%rbp, %rsi
 4062df4:      	subq	%rdx, %rsi
 4062df7:      	movq	0x20(%rsi), %rdx
 4062dfb:      	jmp	0x4062d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6b0>
 4062e00:      	movq	0x80(%rsp), %r8
 4062e08:      	leaq	0x1(%r8), %rcx
 4062e0c:      	shlq	$0x5, %r8
 4062e10:      	addq	0x20(%rsp), %r8
 4062e15:      	movl	0x18(%rsp), %edx
 4062e19:      	jmp	0x4062e45 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x795>
 4062e1b:      	movq	-0x40(%rbp), %rdx
 4062e1f:      	nop
 4062e20:      	movq	0x8(%rax), %rsi
 4062e24:      	incq	%rcx
 4062e27:      	addq	$0x20, %r8
 4062e2b:      	movq	0x8(%rsp), %rdi
 4062e30:      	incl	%edi
 4062e32:      	movq	%rdi, 0x8(%rsp)
 4062e37:      	cmpq	%rdx, 0x20(%rsi)
 4062e3b:      	movl	0x18(%rsp), %edx
 4062e3f:      	jne	0x4062ff0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x940>
 4062e45:      	testl	%ecx, %ecx
 4062e47:      	je	0x4062ebc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x80c>
 4062e49:      	movzbl	(%rbp), %edx
 4062e4d:      	addl	$-0x1f, %edx
 4062e50:      	leaq	-0x25c48d7(%rip), %rsi  # 0x1a9e580 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x180>
 4062e57:      	movslq	(%rsi,%rdx,4), %rdx
 4062e5b:      	addq	%rsi, %rdx
 4062e5e:      	jmpq	*%rdx
 4062e60:      	leal	0x1(%rcx), %edx
 4062e63:      	movq	-0x8(%rbp), %rsi
 4062e67:      	shlq	$0x5, %rdx
 4062e6b:      	movq	(%rsi,%rdx), %rdx
 4062e6f:      	jmp	0x4062e20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x770>
 4062e71:      	movl	0x58(%rbp), %edx
 4062e74:      	shlq	$0x5, %rdx
 4062e78:      	movq	%r8, %rsi
 4062e7b:      	jmp	0x4062e92 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x7e2>
 4062e7d:      	testb	$0x1, 0x2(%rbp)
 4062e81:      	jne	0x4062ea7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x7f7>
 4062e83:      	xorl	%edx, %edx
 4062e85:      	jmp	0x4062e20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x770>
 4062e87:      	movl	%ecx, %edx
 4062e89:      	shlq	$0x5, %rdx
 4062e8d:      	movq	0x20(%rsp), %rsi
 4062e92:      	subq	%rdx, %rsi
 4062e95:      	movq	(%rsi), %rdx
 4062e98:      	jmp	0x4062e20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x770>
 4062e9a:      	movq	0x20(%rsp), %rdx
 4062e9f:      	movq	(%rdx), %rdx
 4062ea2:      	jmp	0x4062e20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x770>
 4062ea7:      	movl	0x4(%rbp), %edx
 4062eaa:      	shll	$0x5, %edx
 4062ead:      	movq	%rbp, %rsi
 4062eb0:      	subq	%rdx, %rsi
 4062eb3:      	movq	0x20(%rsi), %rdx
 4062eb7:      	jmp	0x4062e20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x770>
 4062ebc:      	movq	$0x0, 0x8(%rsp)
 4062ec5:      	jmp	0x4062ff0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x940>
 4062eca:      	movl	-0x14(%rcx), %edx
 4062ecd:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4062ed2:      	andl	%ecx, %edx
 4062ed4:      	decl	%edx
 4062ed6:      	movq	%rdx, 0x8(%rsp)
 4062edb:      	jmp	0x4062efe <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x84e>
 4062edd:      	movl	$0x1, %ecx
 4062ee2:      	jmp	0x4062ef9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x849>
 4062ee4:      	movl	$0x2, %ecx
 4062ee9:      	jmp	0x4062ef9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x849>
 4062eeb:      	movl	0x40(%rcx), %ecx
 4062eee:      	incl	%ecx
 4062ef0:      	jmp	0x4062ef9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x849>
 4062ef2:      	movzwl	-0x16(%rcx), %ecx
 4062ef6:      	andl	$0x1, %ecx
 4062ef9:      	movq	%rcx, 0x8(%rsp)
 4062efe:      	movl	0x18(%rsp), %edx
 4062f02:      	jmp	0x4062f35 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x885>
 4062f04:      	xorl	%ecx, %ecx
 4062f06:      	testl	%r8d, %r8d
 4062f09:      	setne	%cl
 4062f0c:      	shll	$0x5, %ecx
 4062f0f:      	movq	-0x60(%rcx,%rbp), %rcx
 4062f14:      	nopw	%cs:(%rax,%rax)
 4062f1e:      	nop
 4062f20:      	movq	0x8(%rax), %rdx
 4062f24:      	incl	%r8d
 4062f27:      	cmpq	%rcx, 0x20(%rdx)
 4062f2b:      	movl	0x18(%rsp), %edx
 4062f2f:      	jne	0x4062fe1 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x931>
 4062f35:      	cmpl	%r8d, 0x8(%rsp)
 4062f3a:      	je	0x4062ff0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x940>
 4062f40:      	movzbl	(%rbp), %ecx
 4062f44:      	addl	$-0x1f, %ecx
 4062f47:      	leaq	-0x25c497a(%rip), %rdx  # 0x1a9e5d4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x1d4>
 4062f4e:      	movslq	(%rdx,%rcx,4), %rcx
 4062f52:      	addq	%rdx, %rcx
 4062f55:      	jmpq	*%rcx
 4062f57:      	leal	0x1(%r8), %ecx
 4062f5b:      	movq	-0x8(%rbp), %rdx
 4062f5f:      	shlq	$0x5, %rcx
 4062f63:      	movq	(%rdx,%rcx), %rcx
 4062f67:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062f69:      	leal	-0x1(%r8), %ecx
 4062f6d:      	movl	0x58(%rbp), %edx
 4062f70:      	shlq	$0x5, %rdx
 4062f74:      	movq	%rbp, %rsi
 4062f77:      	subq	%rdx, %rsi
 4062f7a:      	addq	$-0x40, %rsi
 4062f7e:      	movq	0x20(%rsp), %rdi
 4062f83:      	subq	%rdx, %rdi
 4062f86:      	movl	%ecx, %ecx
 4062f88:      	shlq	$0x5, %rcx
 4062f8c:      	addq	%rdi, %rcx
 4062f8f:      	testl	%r8d, %r8d
 4062f92:      	cmoveq	%rsi, %rcx
 4062f96:      	movq	(%rcx), %rcx
 4062f99:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062f9b:      	testb	$0x1, 0x2(%rbp)
 4062f9f:      	jne	0x4062fcc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x91c>
 4062fa1:      	xorl	%ecx, %ecx
 4062fa3:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062fa8:      	movl	%r8d, %ecx
 4062fab:      	shlq	$0x5, %rcx
 4062faf:      	movq	0x20(%rsp), %rdx
 4062fb4:      	subq	%rcx, %rdx
 4062fb7:      	movq	(%rdx), %rcx
 4062fba:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062fbf:      	movq	0x20(%rsp), %rcx
 4062fc4:      	movq	(%rcx), %rcx
 4062fc7:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062fcc:      	movl	0x4(%rbp), %ecx
 4062fcf:      	shll	$0x5, %ecx
 4062fd2:      	movq	%rbp, %rdx
 4062fd5:      	subq	%rcx, %rdx
 4062fd8:      	movq	0x20(%rdx), %rcx
 4062fdc:      	jmp	0x4062f20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x870>
 4062fe1:      	decl	%r8d
 4062fe4:      	movl	%r8d, %eax
 4062fe7:      	movq	%rax, 0x8(%rsp)
 4062fec:      	nopl	(%rax)
 4062ff0:      	movb	$0x1, %al
 4062ff2:      	cmpl	%edx, 0x8(%rsp)
 4062ff6:      	jne	0x40629b8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x308>
 4062ffc:      	jmp	0x4063020 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x970>
 4062ffe:      	movl	-0x14(%rcx), %ecx
 4063001:      	movl	$0x7ffffff, %edx        # imm = 0x7FFFFFF
 4063006:      	andl	%edx, %ecx
 4063008:      	xorl	%edx, %edx
 406300a:      	cmpl	$0x3, %ecx
 406300d:      	sete	%dl
 4063010:      	incl	%edx
 4063012:      	movq	%rdx, 0x8(%rsp)
 4063017:      	jmp	0x4062efe <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x84e>
 406301c:      	nopl	(%rax)
 4063020:      	movq	-0x50(%r15), %rax
 4063024:      	movl	%eax, %ecx
 4063026:      	xorl	0x48(%rsp), %eax
 406302a:      	xorl	%edx, %edx
 406302c:      	testb	$0x6, %al
 406302e:      	setne	%dl
 4063031:      	xorl	%eax, %eax
 4063033:      	movl	0x18(%rsp), %esi
 4063037:      	cmpl	%esi, -0x40(%r15)
 406303b:      	setne	%al
 406303e:      	testb	$0x6, %cl
 4063041:      	cmovel	%eax, %edx
 4063044:      	movq	0x28(%rsp), %rcx
 4063049:      	movq	0x58(%rcx), %r12
 406304d:      	cmpb	$0x1, %dl
 4063050:      	jne	0x40631e0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb30>
 4063056:      	movq	-0x50(%r12), %r15
 406305b:      	movl	-0x40(%r12), %ebx
 4063060:      	movq	-0x38(%r12), %rax
 4063065:      	movq	%rax, 0x10(%rsp)
 406306a:      	testb	$0x6, %r15b
 406306e:      	movq	%r12, 0x8(%rsp)
 4063073:      	je	0x406323b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb8b>
 4063079:      	movq	%r15, %rax
 406307c:      	andq	$-0x7, %rax
 4063080:      	orq	$0x4, %rax
 4063084:      	movq	%rax, -0x50(%r12)
 4063089:      	movl	-0x30(%r12), %ecx
 406308e:      	andl	$0x6, %ecx
 4063091:      	cmpl	$0x4, %ecx
 4063094:      	jne	0x40633e3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd33>
 406309a:      	andq	$-0x8, %r15
 406309e:      	movq	0x20(%r15), %r12
 40630a2:      	movq	0x10(%rsp), %rbx
 40630a7:      	movq	0x8(%r15), %r13
 40630ab:      	movq	0x10(%r13), %rax
 40630af:      	movl	0x38(%rax), %ecx
 40630b2:      	testl	%ecx, %ecx
 40630b4:      	je	0x406312d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa7d>
 40630b6:      	movq	0x28(%rax), %rax
 40630ba:      	movl	%r12d, %esi
 40630bd:      	shrl	$0x4, %esi
 40630c0:      	movl	%r12d, %edx
 40630c3:      	shrl	$0x9, %edx
 40630c6:      	xorl	%esi, %edx
 40630c8:      	decl	%ecx
 40630ca:      	andl	%ecx, %edx
 40630cc:      	movl	%edx, %esi
 40630ce:      	shll	$0x4, %esi
 40630d1:      	movq	(%rax,%rsi), %rdi
 40630d5:      	cmpq	%rdi, %r12
 40630d8:      	jne	0x4063fe8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1938>
 40630de:      	shlq	$0x4, %rdx
 40630e2:      	movq	0x8(%rax,%rdx), %rax
 40630e7:      	testq	%rax, %rax
 40630ea:      	je	0x406312d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa7d>
 40630ec:      	cmpq	%r13, %rax
 40630ef:      	je	0x406312d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa7d>
 40630f1:      	nopw	%cs:(%rax,%rax)
 40630fb:      	nopl	(%rax,%rax)
 4063100:      	movq	%rax, %rbp
 4063103:      	movq	0x8(%rax), %rsi
 4063107:      	movq	%r13, %rdi
 406310a:      	callq	0x3361620 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 406310f:      	testb	%al, %al
 4063111:      	je	0x406311c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa6c>
 4063113:      	movq	0x8(%rbp), %rax
 4063117:      	cmpq	%r13, %rax
 406311a:      	jne	0x4063100 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa50>
 406311c:      	movq	(%rbp), %rax
 4063120:      	andq	$-0x8, %rax
 4063124:      	cmpq	%rax, %r12
 4063127:      	je	0x40638a3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11f3>
 406312d:      	movq	0x50(%r13), %rax
 4063131:      	leaq	0x48(%r13), %r14
 4063135:      	movq	%r14, %rbp
 4063138:      	testq	%rax, %rax
 406313b:      	je	0x4063166 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xab6>
 406313d:      	movq	%r14, %rbp
 4063140:      	xorl	%ecx, %ecx
 4063142:      	cmpq	%r12, 0x20(%rax)
 4063146:      	setb	%cl
 4063149:      	cmovaeq	%rax, %rbp
 406314d:      	movq	0x10(%rax,%rcx,8), %rax
 4063152:      	testq	%rax, %rax
 4063155:      	jne	0x4063140 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa90>
 4063157:      	cmpq	%r14, %rbp
 406315a:      	je	0x4063166 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xab6>
 406315c:      	cmpq	0x20(%rbp), %r12
 4063160:      	jae	0x406389f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ef>
 4063166:      	movq	%rbp, %rbx
 4063169:      	leaq	0x40(%r13), %r15
 406316d:      	movl	$0x30, %edi
 4063172:      	callq	0x828a620 <_Znwm@plt>
 4063177:      	movq	%rax, %rbp
 406317a:      	addq	$0x20, %rax
 406317e:      	movq	%r12, 0x20(%rbp)
 4063182:      	movq	$0x0, 0x28(%rbp)
 406318a:      	movq	%r15, %rdi
 406318d:      	movq	%rax, %r15
 4063190:      	movq	%rbx, %rsi
 4063193:      	movq	%rax, %rdx
 4063196:      	callq	0x3369160 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 406319b:      	movq	%rax, %rbx
 406319e:      	testq	%rdx, %rdx
 40631a1:      	je	0x406384b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x119b>
 40631a7:      	testq	%rbx, %rbx
 40631aa:      	setne	%al
 40631ad:      	cmpq	%r14, %rdx
 40631b0:      	sete	%cl
 40631b3:      	orb	%al, %cl
 40631b5:      	movb	$0x1, %al
 40631b7:      	jne	0x40631c3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb13>
 40631b9:      	movq	(%r15), %rax
 40631bc:      	cmpq	0x20(%rdx), %rax
 40631c0:      	setb	%al
 40631c3:      	movzbl	%al, %edi
 40631c6:      	movq	%rbp, %rsi
 40631c9:      	movq	%r14, %rcx
 40631cc:      	callq	0x828a750 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 40631d1:      	incq	0x68(%r13)
 40631d5:      	jmp	0x406386e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11be>
 40631da:      	nopw	(%rax,%rax)
 40631e0:      	leaq	-0x60(%r12), %rax
 40631e5:      	movq	-0x60(%r12), %r15
 40631ea:      	movq	-0x58(%r12), %rbp
 40631ef:      	movl	-0x8(%r12), %ebx
 40631f4:      	movq	%rax, 0x58(%rcx)
 40631f8:      	cmpq	%rax, 0x50(%rcx)
 40631fc:      	je	0x406320a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb5a>
 40631fe:      	cmpl	%ebx, -0x68(%r12)
 4063203:      	jbe	0x406320a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb5a>
 4063205:      	movl	%ebx, -0x68(%r12)
 406320a:      	movq	0x78(%rsp), %rdi
 406320f:      	movq	%r15, %rsi
 4063212:      	movq	%rbp, %rdx
 4063215:      	callq	0x4064510 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS4_Lj4ENS_12DenseMapInfoIS4_vEEEEEjNS6_ISA_vEENS_6detail12DenseMapPairISA_jEEEESA_jSB_SE_E24lookupOrInsertIntoBucketIRKSA_JEEES2_IPSE_bEOT_DpOT0_>
 406321a:      	cmpl	0x10(%rax), %ebx
 406321d:      	je	0x4064165 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ab5>
 4063223:      	movq	0x28(%rsp), %rbx
 4063228:      	movq	0x58(%rbx), %r15
 406322c:      	cmpq	%r15, 0x50(%rbx)
 4063230:      	jne	0x4062710 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 4063236:      	jmp	0x40644ea <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e3a>
 406323b:      	movq	-0x48(%r12), %r14
 4063240:      	movq	%r15, %rbp
 4063243:      	andq	$-0x8, %rbp
 4063247:      	leaq	-0x20(%r14), %rax
 406324b:      	movq	%rax, 0x30(%rsp)
 4063250:      	leal	0x1(%rbx), %edx
 4063253:      	jmp	0x4063281 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd1>
 4063255:      	xorl	%ecx, %ecx
 4063257:      	testl	%eax, %eax
 4063259:      	setne	%cl
 406325c:      	shll	$0x5, %ecx
 406325f:      	movq	-0x60(%rcx,%r14), %rcx
 4063264:      	nopw	%cs:(%rax,%rax)
 406326e:      	nop
 4063270:      	movq	0x8(%rbp), %rsi
 4063274:      	leal	0x1(%rax), %edx
 4063277:      	cmpq	%rcx, 0x20(%rsi)
 406327b:      	jne	0x40633ab <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xcfb>
 4063281:      	movl	%edx, %eax
 4063283:      	movl	%edx, -0x40(%r12)
 4063288:      	movq	(%rbp), %rsi
 406328c:      	andq	$-0x8, %rsi
 4063290:      	movq	0x30(%rsi), %rdx
 4063294:      	addq	$0x30, %rsi
 4063298:      	xorl	%ecx, %ecx
 406329a:      	cmpq	%rdx, %rsi
 406329d:      	je	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 406329f:      	movzbl	-0x18(%rdx), %esi
 40632a3:      	leal	-0x1e(%rsi), %edi
 40632a6:      	cmpb	$0xa, %dil
 40632aa:      	ja	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 40632ac:      	addl	$-0x1e, %esi
 40632af:      	leaq	-0x25c4c16(%rip), %rdi  # 0x1a9e6a0 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x2a0>
 40632b6:      	movslq	(%rdi,%rsi,4), %rsi
 40632ba:      	addq	%rdi, %rsi
 40632bd:      	jmpq	*%rsi
 40632bf:      	movl	-0x14(%rdx), %ecx
 40632c2:      	movl	$0x7ffffff, %edx        # imm = 0x7FFFFFF
 40632c7:      	andl	%edx, %ecx
 40632c9:      	decl	%ecx
 40632cb:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 40632cd:      	movl	$0x1, %ecx
 40632d2:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 40632d4:      	movl	$0x2, %ecx
 40632d9:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 40632db:      	movl	0x40(%rdx), %ecx
 40632de:      	jmp	0x40632fb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc4b>
 40632e0:      	movzwl	-0x16(%rdx), %ecx
 40632e4:      	andl	$0x1, %ecx
 40632e7:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc50>
 40632e9:      	movl	-0x14(%rdx), %edx
 40632ec:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 40632f1:      	andl	%ecx, %edx
 40632f3:      	xorl	%ecx, %ecx
 40632f5:      	cmpl	$0x3, %edx
 40632f8:      	sete	%cl
 40632fb:      	incl	%ecx
 40632fd:      	nopl	(%rax)
 4063300:      	cmpl	%ecx, %eax
 4063302:      	je	0x40633ab <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xcfb>
 4063308:      	movzbl	(%r14), %ecx
 406330c:      	addl	$-0x1f, %ecx
 406330f:      	leaq	-0x25c4c4a(%rip), %rdx  # 0x1a9e6cc <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x2cc>
 4063316:      	movslq	(%rdx,%rcx,4), %rcx
 406331a:      	addq	%rdx, %rcx
 406331d:      	jmpq	*%rcx
 406331f:      	leal	0x1(%rax), %ecx
 4063322:      	movq	-0x8(%r14), %rdx
 4063326:      	shlq	$0x5, %rcx
 406332a:      	movq	(%rdx,%rcx), %rcx
 406332e:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 4063333:      	leal	-0x1(%rax), %ecx
 4063336:      	movl	0x58(%r14), %edx
 406333a:      	shlq	$0x5, %rdx
 406333e:      	movq	%r14, %rsi
 4063341:      	subq	%rdx, %rsi
 4063344:      	addq	$-0x40, %rsi
 4063348:      	leaq	-0x20(%r14), %rdi
 406334c:      	subq	%rdx, %rdi
 406334f:      	movl	%ecx, %ecx
 4063351:      	shlq	$0x5, %rcx
 4063355:      	addq	%rdi, %rcx
 4063358:      	testl	%eax, %eax
 406335a:      	cmoveq	%rsi, %rcx
 406335e:      	movq	(%rcx), %rcx
 4063361:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 4063366:      	testb	$0x1, 0x2(%r14)
 406336b:      	jne	0x4063395 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xce5>
 406336d:      	xorl	%ecx, %ecx
 406336f:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 4063374:      	movl	%eax, %ecx
 4063376:      	shlq	$0x5, %rcx
 406337a:      	leaq	-0x20(%r14), %rdx
 406337e:      	subq	%rcx, %rdx
 4063381:      	movq	(%rdx), %rcx
 4063384:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 4063389:      	leaq	-0x20(%r14), %rcx
 406338d:      	movq	(%rcx), %rcx
 4063390:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 4063395:      	movl	0x4(%r14), %ecx
 4063399:      	shll	$0x5, %ecx
 406339c:      	movq	%r14, %rdx
 406339f:      	subq	%rcx, %rdx
 40633a2:      	movq	0x20(%rdx), %rcx
 40633a6:      	jmp	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbc0>
 40633ab:      	cmpl	%eax, -0x20(%r12)
 40633b0:      	jne	0x406391b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x126b>
 40633b6:      	movzbl	(%r14), %eax
 40633ba:      	addl	$-0x1f, %eax
 40633bd:      	leaq	-0x25c4c54(%rip), %rcx  # 0x1a9e770 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x370>
 40633c4:      	movslq	(%rcx,%rax,4), %rax
 40633c8:      	addq	%rcx, %rax
 40633cb:      	jmpq	*%rax
 40633cd:      	incl	%ebx
 40633cf:      	movq	-0x8(%r14), %rax
 40633d3:      	shlq	$0x5, %rbx
 40633d7:      	movq	(%rax,%rbx), %r12
 40633db:      	movq	%rbp, %r15
 40633de:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 40633e3:      	xorl	%ecx, %ecx
 40633e5:      	movq	%r15, 0x58(%rsp)
 40633ea:      	jmp	0x40633fb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd4b>
 40633ec:      	nopl	(%rax)
 40633f0:      	cmpl	%ebx, -0x20(%r12)
 40633f5:      	je	0x406309a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9ea>
 40633fb:      	movq	-0x10(%r12), %rbp
 4063400:      	testb	$0x1, %cl
 4063403:      	je	0x4063430 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd80>
 4063405:      	movq	-0x48(%r12), %rcx
 406340a:      	movzbl	(%rcx), %edx
 406340d:      	addl	$-0x1f, %edx
 4063410:      	leaq	-0x25c4df3(%rip), %rsi  # 0x1a9e624 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x224>
 4063417:      	movslq	(%rsi,%rdx,4), %rdx
 406341b:      	addq	%rsi, %rdx
 406341e:      	jmpq	*%rdx
 4063420:      	incl	%ebx
 4063422:      	movq	-0x8(%rcx), %rcx
 4063426:      	shlq	$0x5, %rbx
 406342a:      	movq	(%rcx,%rbx), %rbx
 406342e:      	jmp	0x40634a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf0>
 4063430:      	andq	$-0x8, %rax
 4063434:      	movq	0x20(%rax), %rbx
 4063438:      	jmp	0x40634a4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf4>
 406343a:      	testl	%ebx, %ebx
 406343c:      	je	0x406348e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdde>
 406343e:      	decl	%ebx
 4063440:      	movl	0x58(%rcx), %edx
 4063443:      	shlq	$0x5, %rdx
 4063447:      	subq	%rdx, %rcx
 406344a:      	shlq	$0x5, %rbx
 406344e:      	leaq	-0x20(%rbx,%rcx), %rcx
 4063453:      	jmp	0x406349d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xded>
 4063455:      	movl	%ebx, %edx
 4063457:      	shlq	$0x5, %rdx
 406345b:      	subq	%rdx, %rcx
 406345e:      	movq	-0x20(%rcx), %rbx
 4063462:      	jmp	0x40634a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf0>
 4063464:      	testb	$0x1, 0x2(%rcx)
 4063468:      	jne	0x406347f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdcf>
 406346a:      	xorl	%ebx, %ebx
 406346c:      	jmp	0x40634a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf0>
 406346e:      	xorl	%edx, %edx
 4063470:      	testl	%ebx, %ebx
 4063472:      	setne	%dl
 4063475:      	shll	$0x5, %edx
 4063478:      	movq	-0x60(%rdx,%rcx), %rbx
 406347d:      	jmp	0x40634a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf0>
 406347f:      	movl	0x4(%rcx), %edx
 4063482:      	shll	$0x5, %edx
 4063485:      	subq	%rdx, %rcx
 4063488:      	movq	0x20(%rcx), %rbx
 406348c:      	jmp	0x40634a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdf0>
 406348e:      	movl	0x58(%rcx), %edx
 4063491:      	shlq	$0x5, %rdx
 4063495:      	negq	%rdx
 4063498:      	leaq	-0x40(%rcx,%rdx), %rcx
 406349d:      	movq	(%rcx), %rbx
 40634a0:      	andq	$-0x8, %rax
 40634a4:      	movq	0x8(%rax), %r13
 40634a8:      	movq	0x10(%r13), %rax
 40634ac:      	movl	0x38(%rax), %ecx
 40634af:      	testl	%ecx, %ecx
 40634b1:      	je	0x406351c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe6c>
 40634b3:      	movq	0x28(%rax), %rax
 40634b7:      	movl	%ebx, %esi
 40634b9:      	shrl	$0x4, %esi
 40634bc:      	movl	%ebx, %edx
 40634be:      	shrl	$0x9, %edx
 40634c1:      	xorl	%esi, %edx
 40634c3:      	decl	%ecx
 40634c5:      	andl	%ecx, %edx
 40634c7:      	movl	%edx, %esi
 40634c9:      	shll	$0x4, %esi
 40634cc:      	movq	(%rax,%rsi), %rdi
 40634d0:      	cmpq	%rdi, %rbx
 40634d3:      	jne	0x406381d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x116d>
 40634d9:      	shlq	$0x4, %rdx
 40634dd:      	movq	0x8(%rax,%rdx), %rax
 40634e2:      	testq	%rax, %rax
 40634e5:      	je	0x406351c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe6c>
 40634e7:      	cmpq	%r13, %rax
 40634ea:      	je	0x406351c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe6c>
 40634ec:      	nopl	(%rax)
 40634f0:      	movq	%rax, %r14
 40634f3:      	movq	0x8(%rax), %rsi
 40634f7:      	movq	%r13, %rdi
 40634fa:      	callq	0x3361620 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 40634ff:      	testb	%al, %al
 4063501:      	je	0x406350c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe5c>
 4063503:      	movq	0x8(%r14), %rax
 4063507:      	cmpq	%r13, %rax
 406350a:      	jne	0x40634f0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe40>
 406350c:      	movq	(%r14), %rax
 406350f:      	andq	$-0x8, %rax
 4063513:      	cmpq	%rax, %rbx
 4063516:      	je	0x4063635 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf85>
 406351c:      	movq	%rbp, 0x40(%rsp)
 4063521:      	movq	0x50(%r13), %rax
 4063525:      	leaq	0x48(%r13), %r14
 4063529:      	movq	%r14, %rbp
 406352c:      	testq	%rax, %rax
 406352f:      	je	0x4063566 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xeb6>
 4063531:      	movq	%r14, %rbp
 4063534:      	nopw	%cs:(%rax,%rax)
 406353e:      	nop
 4063540:      	xorl	%ecx, %ecx
 4063542:      	cmpq	%rbx, 0x20(%rax)
 4063546:      	setb	%cl
 4063549:      	cmovaeq	%rax, %rbp
 406354d:      	movq	0x10(%rax,%rcx,8), %rax
 4063552:      	testq	%rax, %rax
 4063555:      	jne	0x4063540 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe90>
 4063557:      	cmpq	%r14, %rbp
 406355a:      	je	0x4063566 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xeb6>
 406355c:      	cmpq	0x20(%rbp), %rbx
 4063560:      	jae	0x406362c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf7c>
 4063566:      	movq	%rbp, %r15
 4063569:      	leaq	0x40(%r13), %r12
 406356d:      	movl	$0x30, %edi
 4063572:      	callq	0x828a620 <_Znwm@plt>
 4063577:      	movq	%rax, %rbp
 406357a:      	addq	$0x20, %rax
 406357e:      	movq	%rbx, 0x20(%rbp)
 4063582:      	movq	$0x0, 0x28(%rbp)
 406358a:      	movq	%r12, %rdi
 406358d:      	movq	%r15, %rsi
 4063590:      	movq	%rax, %r15
 4063593:      	movq	%rax, %rdx
 4063596:      	callq	0x3369160 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 406359b:      	testq	%rdx, %rdx
 406359e:      	je	0x40635d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf20>
 40635a0:      	testq	%rax, %rax
 40635a3:      	setne	%al
 40635a6:      	cmpq	%r14, %rdx
 40635a9:      	sete	%cl
 40635ac:      	orb	%al, %cl
 40635ae:      	movb	$0x1, %al
 40635b0:      	jne	0x40635bc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf0c>
 40635b2:      	movq	(%r15), %rax
 40635b5:      	cmpq	0x20(%rdx), %rax
 40635b9:      	setb	%al
 40635bc:      	movzbl	%al, %edi
 40635bf:      	movq	%rbp, %rsi
 40635c2:      	movq	%r14, %rcx
 40635c5:      	callq	0x828a750 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 40635ca:      	incq	0x68(%r13)
 40635ce:      	jmp	0x40635f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf46>
 40635d0:      	movq	%rax, %r14
 40635d3:      	movq	0x28(%rbp), %rdi
 40635d7:      	testq	%rdi, %rdi
 40635da:      	je	0x40635e6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf36>
 40635dc:      	movl	$0x10, %esi
 40635e1:      	callq	0x828a660 <_ZdlPvm@plt>
 40635e6:      	movl	$0x30, %esi
 40635eb:      	movq	%rbp, %rdi
 40635ee:      	callq	0x828a660 <_ZdlPvm@plt>
 40635f3:      	movq	%r14, %rbp
 40635f6:      	movq	0x8(%rsp), %r12
 40635fb:      	movq	0x58(%rsp), %r15
 4063600:      	movl	$0x10, %edi
 4063605:      	callq	0x828a620 <_Znwm@plt>
 406360a:      	andq	$-0x5, %rbx
 406360e:      	movq	%rbx, (%rax)
 4063611:      	movq	%r13, 0x8(%rax)
 4063615:      	movq	0x28(%rbp), %rdi
 4063619:      	movq	%rax, 0x28(%rbp)
 406361d:      	testq	%rdi, %rdi
 4063620:      	je	0x406362c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf7c>
 4063622:      	movl	$0x10, %esi
 4063627:      	callq	0x828a660 <_ZdlPvm@plt>
 406362c:      	movq	0x28(%rbp), %r14
 4063630:      	movq	0x40(%rsp), %rbp
 4063635:      	movq	-0x38(%r12), %rax
 406363a:      	movq	%r14, 0x60(%rsp)
 406363f:      	movq	%rax, 0x68(%rsp)
 4063644:      	leaq	0x60(%rsp), %rdi
 4063649:      	callq	*%rbp
 406364b:      	testb	%al, %al
 406364d:      	jne	0x406309a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9ea>
 4063653:      	movq	-0x50(%r12), %rax
 4063658:      	testb	$0x6, %al
 406365a:      	sete	%cl
 406365d:      	je	0x4063690 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xfe0>
 406365f:      	andq	$-0x7, %rax
 4063663:      	orq	$0x4, %rax
 4063667:      	movq	%rax, -0x50(%r12)
 406366c:      	movl	-0x40(%r12), %ebx
 4063671:      	movl	-0x30(%r12), %edx
 4063676:      	andl	$0x6, %edx
 4063679:      	cmpl	$0x4, %edx
 406367c:      	jne	0x40633fb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd4b>
 4063682:      	jmp	0x406309a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9ea>
 4063687:      	nopw	(%rax,%rax)
 4063690:      	movq	%rax, %rdx
 4063693:      	andq	$-0x8, %rdx
 4063697:      	movq	-0x48(%r12), %rsi
 406369c:      	movl	-0x40(%r12), %r9d
 40636a1:      	leaq	-0x20(%rsi), %rdi
 40636a5:      	incl	%r9d
 40636a8:      	jmp	0x40636d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1022>
 40636aa:      	xorl	%r8d, %r8d
 40636ad:      	testl	%ebx, %ebx
 40636af:      	setne	%r8b
 40636b3:      	shll	$0x5, %r8d
 40636b7:      	movq	-0x60(%r8,%rsi), %r8
 40636bc:      	nopl	(%rax)
 40636c0:      	movq	0x8(%rdx), %r10
 40636c4:      	leal	0x1(%rbx), %r9d
 40636c8:      	cmpq	%r8, 0x20(%r10)
 40636cc:      	jne	0x40633f0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd40>
 40636d2:      	movl	%r9d, %ebx
 40636d5:      	movl	%r9d, -0x40(%r12)
 40636da:      	movq	(%rdx), %r10
 40636dd:      	andq	$-0x8, %r10
 40636e1:      	movq	0x30(%r10), %r9
 40636e5:      	addq	$0x30, %r10
 40636e9:      	xorl	%r8d, %r8d
 40636ec:      	cmpq	%r9, %r10
 40636ef:      	je	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 40636f1:      	movzbl	-0x18(%r9), %r10d
 40636f6:      	leal	-0x1e(%r10), %r11d
 40636fa:      	cmpb	$0xa, %r11b
 40636fe:      	ja	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 4063700:      	addl	$-0x1e, %r10d
 4063704:      	leaq	-0x25c50bf(%rip), %r11  # 0x1a9e64c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x24c>
 406370b:      	movslq	(%r11,%r10,4), %r10
 406370f:      	addq	%r11, %r10
 4063712:      	jmpq	*%r10
 4063715:      	movl	-0x14(%r9), %r8d
 4063719:      	movl	$0x7ffffff, %r9d        # imm = 0x7FFFFFF
 406371f:      	andl	%r9d, %r8d
 4063722:      	decl	%r8d
 4063725:      	jmp	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 4063727:      	movl	$0x1, %r8d
 406372d:      	jmp	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 406372f:      	movl	$0x2, %r8d
 4063735:      	jmp	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 4063737:      	movl	0x40(%r9), %r8d
 406373b:      	jmp	0x4063760 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10b0>
 406373d:      	movzwl	-0x16(%r9), %r8d
 4063742:      	andl	$0x1, %r8d
 4063746:      	jmp	0x4063770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 4063748:      	movl	-0x14(%r9), %r9d
 406374c:      	movl	$0x7ffffff, %r8d        # imm = 0x7FFFFFF
 4063752:      	andl	%r8d, %r9d
 4063755:      	xorl	%r8d, %r8d
 4063758:      	cmpl	$0x3, %r9d
 406375c:      	sete	%r8b
 4063760:      	incl	%r8d
 4063763:      	nopw	%cs:(%rax,%rax)
 406376d:      	nopl	(%rax)
 4063770:      	cmpl	%r8d, %ebx
 4063773:      	je	0x40633f0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd40>
 4063779:      	movzbl	(%rsi), %r8d
 406377d:      	addl	$-0x1f, %r8d
 4063781:      	leaq	-0x25c5110(%rip), %r9   # 0x1a9e678 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x278>
 4063788:      	movslq	(%r9,%r8,4), %r8
 406378c:      	addq	%r9, %r8
 406378f:      	jmpq	*%r8
 4063792:      	leal	0x1(%rbx), %r8d
 4063796:      	movq	-0x8(%rsi), %r9
 406379a:      	shlq	$0x5, %r8
 406379e:      	movq	(%r9,%r8), %r8
 40637a2:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 40637a7:      	leal	-0x1(%rbx), %r8d
 40637ab:      	movl	0x58(%rsi), %r9d
 40637af:      	shlq	$0x5, %r9
 40637b3:      	movq	%rsi, %r10
 40637b6:      	subq	%r9, %r10
 40637b9:      	addq	$-0x40, %r10
 40637bd:      	movq	%rdi, %r11
 40637c0:      	subq	%r9, %r11
 40637c3:      	movl	%r8d, %r8d
 40637c6:      	shlq	$0x5, %r8
 40637ca:      	addq	%r11, %r8
 40637cd:      	testl	%ebx, %ebx
 40637cf:      	cmoveq	%r10, %r8
 40637d3:      	movq	(%r8), %r8
 40637d6:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 40637db:      	testb	$0x1, 0x2(%rsi)
 40637df:      	jne	0x4063806 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1156>
 40637e1:      	xorl	%r8d, %r8d
 40637e4:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 40637e9:      	movl	%ebx, %r8d
 40637ec:      	shlq	$0x5, %r8
 40637f0:      	movq	%rdi, %r9
 40637f3:      	subq	%r8, %r9
 40637f6:      	movq	(%r9), %r8
 40637f9:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 40637fe:      	movq	(%rdi), %r8
 4063801:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 4063806:      	movl	0x4(%rsi), %r8d
 406380a:      	shll	$0x5, %r8d
 406380e:      	movq	%rsi, %r9
 4063811:      	subq	%r8, %r9
 4063814:      	movq	0x20(%r9), %r8
 4063818:      	jmp	0x40636c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1010>
 406381d:      	movl	$0x1, %esi
 4063822:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4063829:      	je	0x406351c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe6c>
 406382f:      	addl	%esi, %edx
 4063831:      	incl	%esi
 4063833:      	andl	%ecx, %edx
 4063835:      	movq	%rdx, %rdi
 4063838:      	shlq	$0x4, %rdi
 406383c:      	movq	(%rax,%rdi), %rdi
 4063840:      	cmpq	%rdi, %rbx
 4063843:      	je	0x40634d9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe29>
 4063849:      	jmp	0x4063822 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1172>
 406384b:      	movq	0x28(%rbp), %rdi
 406384f:      	testq	%rdi, %rdi
 4063852:      	je	0x406385e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ae>
 4063854:      	movl	$0x10, %esi
 4063859:      	callq	0x828a660 <_ZdlPvm@plt>
 406385e:      	movl	$0x30, %esi
 4063863:      	movq	%rbp, %rdi
 4063866:      	callq	0x828a660 <_ZdlPvm@plt>
 406386b:      	movq	%rbx, %rbp
 406386e:      	movq	0x10(%rsp), %rbx
 4063873:      	movl	$0x10, %edi
 4063878:      	callq	0x828a620 <_Znwm@plt>
 406387d:      	andq	$-0x5, %r12
 4063881:      	movq	%r12, (%rax)
 4063884:      	movq	%r13, 0x8(%rax)
 4063888:      	movq	0x28(%rbp), %rdi
 406388c:      	movq	%rax, 0x28(%rbp)
 4063890:      	testq	%rdi, %rdi
 4063893:      	je	0x406389f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ef>
 4063895:      	movl	$0x10, %esi
 406389a:      	callq	0x828a660 <_ZdlPvm@plt>
 406389f:      	movq	0x28(%rbp), %rbp
 40638a3:      	movq	0x28(%rsp), %rcx
 40638a8:      	movq	0x8(%rcx), %rax
 40638ac:      	movl	0x18(%rcx), %ecx
 40638af:      	testq	%rcx, %rcx
 40638b2:      	je	0x4064050 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a0>
 40638b8:      	movl	%ebp, %edx
 40638ba:      	shrl	$0x4, %edx
 40638bd:      	movl	%ebp, %esi
 40638bf:      	shrl	$0x9, %esi
 40638c2:      	xorl	%edx, %esi
 40638c4:      	movl	%ebx, %edx
 40638c6:      	shrl	$0x4, %edx
 40638c9:      	movl	%ebx, %edi
 40638cb:      	shrl	$0x9, %edi
 40638ce:      	xorl	%edx, %edi
 40638d0:      	shlq	$0x20, %rsi
 40638d4:      	orq	%rsi, %rdi
 40638d7:      	movabsq	$-0x40a7b892e31b1a47, %rdx # imm = 0xBF58476D1CE4E5B9
 40638e1:      	imulq	%rdx, %rdi
 40638e5:      	movq	%rdi, %rdx
 40638e8:      	shrq	$0x1f, %rdx
 40638ec:      	xorl	%edi, %edx
 40638ee:      	leal	-0x1(%rcx), %esi
 40638f1:      	andl	%esi, %edx
 40638f3:      	leaq	(%rdx,%rdx,2), %rdi
 40638f7:      	movq	(%rax,%rdi,8), %r9
 40638fb:      	movq	0x8(%rax,%rdi,8), %r8
 4063900:      	cmpq	%r9, %rbp
 4063903:      	jne	0x4064016 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1966>
 4063909:      	cmpq	%r8, %rbx
 406390c:      	jne	0x4064016 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1966>
 4063912:      	leaq	(%rax,%rdi,8), %r10
 4063916:      	jmp	0x4064058 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a8>
 406391b:      	movb	$0x1, %cl
 406391d:      	movq	%r14, 0x38(%rsp)
 4063922:      	movq	%rbp, 0x50(%rsp)
 4063927:      	jmp	0x406393b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x128b>
 4063929:      	nopl	(%rax)
 4063930:      	cmpl	%eax, -0x20(%r12)
 4063935:      	je	0x40633b6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd06>
 406393b:      	movq	-0x10(%r12), %rdi
 4063940:      	testb	$0x1, %cl
 4063943:      	movq	%rdi, 0x40(%rsp)
 4063948:      	je	0x4063980 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x12d0>
 406394a:      	movq	-0x48(%r12), %rcx
 406394f:      	movzbl	(%rcx), %edx
 4063952:      	addl	$-0x1f, %edx
 4063955:      	leaq	-0x25c5268(%rip), %rsi  # 0x1a9e6f4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x2f4>
 406395c:      	movslq	(%rsi,%rdx,4), %rdx
 4063960:      	addq	%rsi, %rdx
 4063963:      	jmpq	*%rdx
 4063965:      	incl	%eax
 4063967:      	movq	-0x8(%rcx), %rcx
 406396b:      	shlq	$0x5, %rax
 406396f:      	movq	(%rcx,%rax), %r14
 4063973:      	jmp	0x4063a00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1350>
 4063978:      	nopl	(%rax,%rax)
 4063980:      	andq	$-0x8, %r15
 4063984:      	movq	0x20(%r15), %r14
 4063988:      	jmp	0x4063a04 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1354>
 406398a:      	testl	%eax, %eax
 406398c:      	je	0x40639df <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x132f>
 406398e:      	decl	%eax
 4063990:      	movl	0x58(%rcx), %edx
 4063993:      	shlq	$0x5, %rdx
 4063997:      	subq	%rdx, %rcx
 406399a:      	shlq	$0x5, %rax
 406399e:      	leaq	-0x20(%rax,%rcx), %rax
 40639a3:      	jmp	0x40639ee <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x133e>
 40639a5:      	movl	%eax, %eax
 40639a7:      	shlq	$0x5, %rax
 40639ab:      	subq	%rax, %rcx
 40639ae:      	movq	-0x20(%rcx), %r14
 40639b2:      	jmp	0x4063a00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1350>
 40639b4:      	testb	$0x1, 0x2(%rcx)
 40639b8:      	jne	0x40639d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1320>
 40639ba:      	xorl	%r14d, %r14d
 40639bd:      	jmp	0x4063a00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1350>
 40639bf:      	xorl	%edx, %edx
 40639c1:      	testl	%eax, %eax
 40639c3:      	setne	%dl
 40639c6:      	shll	$0x5, %edx
 40639c9:      	movq	-0x60(%rdx,%rcx), %r14
 40639ce:      	jmp	0x4063a00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1350>
 40639d0:      	movl	0x4(%rcx), %eax
 40639d3:      	shll	$0x5, %eax
 40639d6:      	subq	%rax, %rcx
 40639d9:      	movq	0x20(%rcx), %r14
 40639dd:      	jmp	0x4063a00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1350>
 40639df:      	movl	0x58(%rcx), %eax
 40639e2:      	shlq	$0x5, %rax
 40639e6:      	negq	%rax
 40639e9:      	leaq	-0x40(%rcx,%rax), %rax
 40639ee:      	movq	(%rax), %r14
 40639f1:      	nopw	%cs:(%rax,%rax)
 40639fb:      	nopl	(%rax,%rax)
 4063a00:      	andq	$-0x8, %r15
 4063a04:      	movq	0x8(%r15), %r13
 4063a08:      	movq	0x10(%r13), %rax
 4063a0c:      	movl	0x38(%rax), %ecx
 4063a0f:      	testl	%ecx, %ecx
 4063a11:      	je	0x4063a7c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13cc>
 4063a13:      	movq	0x28(%rax), %rax
 4063a17:      	movl	%r14d, %esi
 4063a1a:      	shrl	$0x4, %esi
 4063a1d:      	movl	%r14d, %edx
 4063a20:      	shrl	$0x9, %edx
 4063a23:      	xorl	%esi, %edx
 4063a25:      	decl	%ecx
 4063a27:      	andl	%ecx, %edx
 4063a29:      	movl	%edx, %esi
 4063a2b:      	shll	$0x4, %esi
 4063a2e:      	movq	(%rax,%rsi), %rdi
 4063a32:      	cmpq	%rdi, %r14
 4063a35:      	jne	0x4063d7d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16cd>
 4063a3b:      	shlq	$0x4, %rdx
 4063a3f:      	movq	0x8(%rax,%rdx), %rax
 4063a44:      	testq	%rax, %rax
 4063a47:      	je	0x4063a7c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13cc>
 4063a49:      	cmpq	%r13, %rax
 4063a4c:      	je	0x4063a7c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13cc>
 4063a4e:      	nop
 4063a50:      	movq	%rax, %r15
 4063a53:      	movq	0x8(%rax), %rsi
 4063a57:      	movq	%r13, %rdi
 4063a5a:      	callq	0x3361620 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 4063a5f:      	testb	%al, %al
 4063a61:      	je	0x4063a6c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13bc>
 4063a63:      	movq	0x8(%r15), %rax
 4063a67:      	cmpq	%r13, %rax
 4063a6a:      	jne	0x4063a50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13a0>
 4063a6c:      	movq	(%r15), %rax
 4063a6f:      	andq	$-0x8, %rax
 4063a73:      	cmpq	%rax, %r14
 4063a76:      	je	0x4063b90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14e0>
 4063a7c:      	movq	0x50(%r13), %rax
 4063a80:      	leaq	0x48(%r13), %rdx
 4063a84:      	movq	%rdx, %rbp
 4063a87:      	testq	%rax, %rax
 4063a8a:      	je	0x4063ab6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1406>
 4063a8c:      	movq	%rdx, %rbp
 4063a8f:      	nop
 4063a90:      	xorl	%ecx, %ecx
 4063a92:      	cmpq	%r14, 0x20(%rax)
 4063a96:      	setb	%cl
 4063a99:      	cmovaeq	%rax, %rbp
 4063a9d:      	movq	0x10(%rax,%rcx,8), %rax
 4063aa2:      	testq	%rax, %rax
 4063aa5:      	jne	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13e0>
 4063aa7:      	cmpq	%rdx, %rbp
 4063aaa:      	je	0x4063ab6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1406>
 4063aac:      	cmpq	0x20(%rbp), %r14
 4063ab0:      	jae	0x4063b87 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14d7>
 4063ab6:      	movq	%rbp, %r15
 4063ab9:      	leaq	0x40(%r13), %r12
 4063abd:      	movl	$0x30, %edi
 4063ac2:      	callq	0x828a620 <_Znwm@plt>
 4063ac7:      	movq	%rax, %rbp
 4063aca:      	addq	$0x20, %rax
 4063ace:      	movq	%r14, 0x20(%rbp)
 4063ad2:      	movq	$0x0, 0x28(%rbp)
 4063ada:      	movq	%r12, %rdi
 4063add:      	movq	%r15, %rsi
 4063ae0:      	movq	%rax, %r15
 4063ae3:      	movq	%rax, %rdx
 4063ae6:      	callq	0x3369160 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 4063aeb:      	testq	%rdx, %rdx
 4063aee:      	je	0x4063b30 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1480>
 4063af0:      	testq	%rax, %rax
 4063af3:      	setne	%al
 4063af6:      	leaq	0x48(%r13), %rcx
 4063afa:      	cmpq	%rcx, %rdx
 4063afd:      	sete	%sil
 4063b01:      	orb	%al, %sil
 4063b04:      	movb	$0x1, %al
 4063b06:      	jne	0x4063b12 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1462>
 4063b08:      	movq	(%r15), %rax
 4063b0b:      	cmpq	0x20(%rdx), %rax
 4063b0f:      	setb	%al
 4063b12:      	movzbl	%al, %edi
 4063b15:      	movq	%rbp, %rsi
 4063b18:      	callq	0x828a750 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 4063b1d:      	incq	0x68(%r13)
 4063b21:      	jmp	0x4063b56 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14a6>
 4063b23:      	nopw	%cs:(%rax,%rax)
 4063b2d:      	nopl	(%rax)
 4063b30:      	movq	%rax, %r15
 4063b33:      	movq	0x28(%rbp), %rdi
 4063b37:      	testq	%rdi, %rdi
 4063b3a:      	je	0x4063b46 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1496>
 4063b3c:      	movl	$0x10, %esi
 4063b41:      	callq	0x828a660 <_ZdlPvm@plt>
 4063b46:      	movl	$0x30, %esi
 4063b4b:      	movq	%rbp, %rdi
 4063b4e:      	callq	0x828a660 <_ZdlPvm@plt>
 4063b53:      	movq	%r15, %rbp
 4063b56:      	movq	0x8(%rsp), %r12
 4063b5b:      	movl	$0x10, %edi
 4063b60:      	callq	0x828a620 <_Znwm@plt>
 4063b65:      	andq	$-0x5, %r14
 4063b69:      	movq	%r14, (%rax)
 4063b6c:      	movq	%r13, 0x8(%rax)
 4063b70:      	movq	0x28(%rbp), %rdi
 4063b74:      	movq	%rax, 0x28(%rbp)
 4063b78:      	testq	%rdi, %rdi
 4063b7b:      	je	0x4063b87 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14d7>
 4063b7d:      	movl	$0x10, %esi
 4063b82:      	callq	0x828a660 <_ZdlPvm@plt>
 4063b87:      	movq	0x28(%rbp), %r15
 4063b8b:      	movq	0x50(%rsp), %rbp
 4063b90:      	movq	-0x38(%r12), %rax
 4063b95:      	movq	%r15, 0x60(%rsp)
 4063b9a:      	movq	%rax, 0x68(%rsp)
 4063b9f:      	leaq	0x60(%rsp), %rdi
 4063ba4:      	callq	*0x40(%rsp)
 4063ba8:      	testb	%al, %al
 4063baa:      	movq	0x38(%rsp), %r14
 4063baf:      	jne	0x40633b6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd06>
 4063bb5:      	movq	-0x50(%r12), %r15
 4063bba:      	testb	$0x6, %r15b
 4063bbe:      	sete	%cl
 4063bc1:      	je	0x4063bf0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1540>
 4063bc3:      	andq	$-0x7, %r15
 4063bc7:      	orq	$0x4, %r15
 4063bcb:      	movq	%r15, -0x50(%r12)
 4063bd0:      	movl	-0x40(%r12), %eax
 4063bd5:      	movl	-0x30(%r12), %edx
 4063bda:      	andl	$0x6, %edx
 4063bdd:      	cmpl	$0x4, %edx
 4063be0:      	jne	0x406393b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x128b>
 4063be6:      	jmp	0x40633b6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd06>
 4063beb:      	nopl	(%rax,%rax)
 4063bf0:      	movq	%r15, %rdx
 4063bf3:      	andq	$-0x8, %rdx
 4063bf7:      	movq	-0x48(%r12), %rsi
 4063bfc:      	movl	-0x40(%r12), %r9d
 4063c01:      	leaq	-0x20(%rsi), %rdi
 4063c05:      	incl	%r9d
 4063c08:      	jmp	0x4063c32 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1582>
 4063c0a:      	xorl	%r8d, %r8d
 4063c0d:      	testl	%eax, %eax
 4063c0f:      	setne	%r8b
 4063c13:      	shll	$0x5, %r8d
 4063c17:      	movq	-0x60(%r8,%rsi), %r8
 4063c1c:      	nopl	(%rax)
 4063c20:      	movq	0x8(%rdx), %r10
 4063c24:      	leal	0x1(%rax), %r9d
 4063c28:      	cmpq	%r8, 0x20(%r10)
 4063c2c:      	jne	0x4063930 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1280>
 4063c32:      	movl	%r9d, %eax
 4063c35:      	movl	%r9d, -0x40(%r12)
 4063c3a:      	movq	(%rdx), %r10
 4063c3d:      	andq	$-0x8, %r10
 4063c41:      	movq	0x30(%r10), %r9
 4063c45:      	addq	$0x30, %r10
 4063c49:      	xorl	%r8d, %r8d
 4063c4c:      	cmpq	%r9, %r10
 4063c4f:      	je	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063c51:      	movzbl	-0x18(%r9), %r10d
 4063c56:      	leal	-0x1e(%r10), %r11d
 4063c5a:      	cmpb	$0xa, %r11b
 4063c5e:      	ja	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063c60:      	addl	$-0x1e, %r10d
 4063c64:      	leaq	-0x25c554f(%rip), %r11  # 0x1a9e71c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x31c>
 4063c6b:      	movslq	(%r11,%r10,4), %r10
 4063c6f:      	addq	%r11, %r10
 4063c72:      	jmpq	*%r10
 4063c75:      	movl	-0x14(%r9), %r8d
 4063c79:      	movl	$0x7ffffff, %r9d        # imm = 0x7FFFFFF
 4063c7f:      	andl	%r9d, %r8d
 4063c82:      	decl	%r8d
 4063c85:      	jmp	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063c87:      	movl	$0x1, %r8d
 4063c8d:      	jmp	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063c8f:      	movl	$0x2, %r8d
 4063c95:      	jmp	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063c97:      	movl	0x40(%r9), %r8d
 4063c9b:      	jmp	0x4063cc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1610>
 4063c9d:      	movzwl	-0x16(%r9), %r8d
 4063ca2:      	andl	$0x1, %r8d
 4063ca6:      	jmp	0x4063cd0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063ca8:      	movl	-0x14(%r9), %r9d
 4063cac:      	movl	$0x7ffffff, %r8d        # imm = 0x7FFFFFF
 4063cb2:      	andl	%r8d, %r9d
 4063cb5:      	xorl	%r8d, %r8d
 4063cb8:      	cmpl	$0x3, %r9d
 4063cbc:      	sete	%r8b
 4063cc0:      	incl	%r8d
 4063cc3:      	nopw	%cs:(%rax,%rax)
 4063ccd:      	nopl	(%rax)
 4063cd0:      	cmpl	%r8d, %eax
 4063cd3:      	je	0x4063930 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1280>
 4063cd9:      	movzbl	(%rsi), %r8d
 4063cdd:      	addl	$-0x1f, %r8d
 4063ce1:      	leaq	-0x25c55a0(%rip), %r9   # 0x1a9e748 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x348>
 4063ce8:      	movslq	(%r9,%r8,4), %r8
 4063cec:      	addq	%r9, %r8
 4063cef:      	jmpq	*%r8
 4063cf2:      	leal	0x1(%rax), %r8d
 4063cf6:      	movq	-0x8(%rsi), %r9
 4063cfa:      	shlq	$0x5, %r8
 4063cfe:      	movq	(%r9,%r8), %r8
 4063d02:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d07:      	leal	-0x1(%rax), %r8d
 4063d0b:      	movl	0x58(%rsi), %r9d
 4063d0f:      	shlq	$0x5, %r9
 4063d13:      	movq	%rsi, %r10
 4063d16:      	subq	%r9, %r10
 4063d19:      	addq	$-0x40, %r10
 4063d1d:      	movq	%rdi, %r11
 4063d20:      	subq	%r9, %r11
 4063d23:      	movl	%r8d, %r8d
 4063d26:      	shlq	$0x5, %r8
 4063d2a:      	addq	%r11, %r8
 4063d2d:      	testl	%eax, %eax
 4063d2f:      	cmoveq	%r10, %r8
 4063d33:      	movq	(%r8), %r8
 4063d36:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d3b:      	testb	$0x1, 0x2(%rsi)
 4063d3f:      	jne	0x4063d66 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16b6>
 4063d41:      	xorl	%r8d, %r8d
 4063d44:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d49:      	movl	%eax, %r8d
 4063d4c:      	shlq	$0x5, %r8
 4063d50:      	movq	%rdi, %r9
 4063d53:      	subq	%r8, %r9
 4063d56:      	movq	(%r9), %r8
 4063d59:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d5e:      	movq	(%rdi), %r8
 4063d61:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d66:      	movl	0x4(%rsi), %r8d
 4063d6a:      	shll	$0x5, %r8d
 4063d6e:      	movq	%rsi, %r9
 4063d71:      	subq	%r8, %r9
 4063d74:      	movq	0x20(%r9), %r8
 4063d78:      	jmp	0x4063c20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1570>
 4063d7d:      	movl	$0x1, %esi
 4063d82:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4063d89:      	je	0x4063a7c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13cc>
 4063d8f:      	addl	%esi, %edx
 4063d91:      	incl	%esi
 4063d93:      	andl	%ecx, %edx
 4063d95:      	movq	%rdx, %rdi
 4063d98:      	shlq	$0x4, %rdi
 4063d9c:      	movq	(%rax,%rdi), %rdi
 4063da0:      	cmpq	%rdi, %r14
 4063da3:      	je	0x4063a3b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x138b>
 4063da9:      	jmp	0x4063d82 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16d2>
 4063dab:      	movl	-0x14(%rax), %esi
 4063dae:      	movl	$0x7ffffff, %eax        # imm = 0x7FFFFFF
 4063db3:      	andl	%eax, %esi
 4063db5:      	decl	%esi
 4063db7:      	jmp	0x4062952 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063dbc:      	movl	$0x1, %esi
 4063dc1:      	jmp	0x4062952 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063dc6:      	movl	$0x2, %esi
 4063dcb:      	jmp	0x4062952 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063dd0:      	movl	0x40(%rax), %esi
 4063dd3:      	jmp	0x4063df4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1744>
 4063dd5:      	movzwl	-0x16(%rax), %esi
 4063dd9:      	andl	$0x1, %esi
 4063ddc:      	jmp	0x4062952 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063de1:      	movl	-0x14(%rax), %eax
 4063de4:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4063de9:      	andl	%ecx, %eax
 4063deb:      	xorl	%esi, %esi
 4063ded:      	cmpl	$0x3, %eax
 4063df0:      	sete	%sil
 4063df4:      	incl	%esi
 4063df6:      	jmp	0x4062952 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063dfb:      	xorl	%eax, %eax
 4063dfd:      	testl	%ebx, %ebx
 4063dff:      	setne	%al
 4063e02:      	shll	$0x5, %eax
 4063e05:      	movq	-0x60(%rax,%r14), %r12
 4063e0a:      	movq	%rbp, %r15
 4063e0d:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 4063e12:      	testl	%ebx, %ebx
 4063e14:      	je	0x4063eea <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x183a>
 4063e1a:      	decl	%ebx
 4063e1c:      	movl	0x58(%r14), %eax
 4063e20:      	shlq	$0x5, %rax
 4063e24:      	movq	0x30(%rsp), %rcx
 4063e29:      	subq	%rax, %rcx
 4063e2c:      	shlq	$0x5, %rbx
 4063e30:      	addq	%rcx, %rbx
 4063e33:      	jmp	0x4063efa <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x184a>
 4063e38:      	testb	$0x1, 0x2(%r14)
 4063e3d:      	jne	0x4063ed4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1824>
 4063e43:      	movq	%rbp, %r15
 4063e46:      	xorl	%r12d, %r12d
 4063e49:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 4063e4e:      	shlq	$0x5, %rbx
 4063e52:      	movq	0x30(%rsp), %rax
 4063e57:      	subq	%rbx, %rax
 4063e5a:      	jmp	0x4063e61 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x17b1>
 4063e5c:      	movq	0x30(%rsp), %rax
 4063e61:      	movq	(%rax), %r12
 4063e64:      	movq	%rbp, %r15
 4063e67:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 4063e6c:      	movzwl	-0x16(%rax), %r8d
 4063e71:      	andl	$0x1, %r8d
 4063e75:      	testl	%r8d, %r8d
 4063e78:      	jne	0x40627af <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xff>
 4063e7e:      	jmp	0x4062910 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 4063e83:      	leaq	-0x14(%rax), %r9
 4063e87:      	movl	-0x14(%rax), %r8d
 4063e8b:      	movl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 4063e90:      	andl	%esi, %r8d
 4063e93:      	xorl	%r15d, %r15d
 4063e96:      	cmpl	$0x3, %r8d
 4063e9a:      	sete	%r15b
 4063e9e:      	incl	%r15d
 4063ea1:      	movq	0x8(%r11), %r8
 4063ea5:      	movq	0x20(%r8), %r10
 4063ea9:      	leaq	-0x16(%rax), %rsi
 4063ead:      	movq	%rsi, 0x50(%rsp)
 4063eb2:      	leaq	-0x38(%rax), %rsi
 4063eb6:      	leaq	-0x20(%rax), %r8
 4063eba:      	movq	%r8, 0x38(%rsp)
 4063ebf:      	leaq	0x40(%rax), %r8
 4063ec3:      	movq	%r8, 0x18(%rsp)
 4063ec8:      	movq	-0x38(%rax), %r11
 4063ecc:      	movl	%r15d, %r8d
 4063ecf:      	jmp	0x4063f54 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a4>
 4063ed4:      	movl	0x4(%r14), %eax
 4063ed8:      	shll	$0x5, %eax
 4063edb:      	subq	%rax, %r14
 4063ede:      	movq	0x20(%r14), %r12
 4063ee2:      	movq	%rbp, %r15
 4063ee5:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 4063eea:      	movl	0x58(%r14), %eax
 4063eee:      	shlq	$0x5, %rax
 4063ef2:      	negq	%rax
 4063ef5:      	leaq	-0x40(%r14,%rax), %rbx
 4063efa:      	movq	(%rbx), %r12
 4063efd:      	movq	%rbp, %r15
 4063f00:      	jmp	0x40630a2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x9f2>
 4063f05:      	leaq	-0x38(%rax), %rsi
 4063f09:      	movq	-0x78(%rax), %r11
 4063f0d:      	jmp	0x4063f54 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a4>
 4063f0f:      	leaq	-0x38(%rax), %rsi
 4063f13:      	movq	(%rsi), %r11
 4063f16:      	jmp	0x4063f54 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a4>
 4063f18:      	leaq	-0x16(%rax), %rsi
 4063f1c:      	testb	$0x1, (%rsi)
 4063f1f:      	jne	0x4063f3e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x188e>
 4063f21:      	xorl	%r11d, %r11d
 4063f24:      	jmp	0x4063f50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a0>
 4063f26:      	leaq	0x40(%rax), %rsi
 4063f2a:      	movl	(%rsi), %r11d
 4063f2d:      	shlq	$0x5, %r11
 4063f31:      	movq	%rbx, %r12
 4063f34:      	subq	%r11, %r12
 4063f37:      	movq	-0x40(%r12), %r11
 4063f3c:      	jmp	0x4063f50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18a0>
 4063f3e:      	movl	(%r9), %r11d
 4063f41:      	shll	$0x5, %r11d
 4063f45:      	movq	%rbx, %r12
 4063f48:      	subq	%r11, %r12
 4063f4b:      	movq	0x20(%r12), %r11
 4063f50:      	leaq	-0x38(%rax), %rsi
 4063f54:      	movq	$0x0, 0x8(%rsp)
 4063f5d:      	cmpq	%r11, %r10
 4063f60:      	je	0x4063f6c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18bc>
 4063f62:      	movq	0x30(%rsp), %r15
 4063f67:      	jmp	0x406284a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a>
 4063f6c:      	cmpl	$0x1, %r8d
 4063f70:      	jne	0x4063fa8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18f8>
 4063f72:      	andl	$0x4, %r14d
 4063f76:      	orq	%rcx, %r14
 4063f79:      	movq	%r14, 0x48(%rsp)
 4063f7e:      	movl	$0x1, %ecx
 4063f83:      	movq	%rcx, 0x8(%rsp)
 4063f88:      	movq	%rbx, %rbp
 4063f8b:      	movq	0x30(%rsp), %r15
 4063f90:      	movzbl	-0x18(%rax), %r9d
 4063f95:      	leal	-0x1e(%r9), %r10d
 4063f99:      	cmpb	$0xa, %r10b
 4063f9d:      	ja	0x4062950 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 4063fa3:      	jmp	0x406292b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x27b>
 4063fa8:      	movq	%rbp, 0x10(%rsp)
 4063fad:      	movq	%r13, 0x40(%rsp)
 4063fb2:      	movq	%rsi, 0x48(%rsp)
 4063fb7:      	leaq	-0x20(%rsi), %r13
 4063fbb:      	movl	$0x1, %esi
 4063fc0:      	movq	%rsi, 0x8(%rsp)
 4063fc5:      	movl	$0x40, %ebp
 4063fca:      	addl	$-0x1f, %edi
 4063fcd:      	leaq	-0x25c5ad0(%rip), %rsi  # 0x1a9e504 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x104>
 4063fd4:      	movslq	(%rsi,%rdi,4), %r12
 4063fd8:      	addq	%rsi, %r12
 4063fdb:      	movabsq	$0x100000000, %r11      # imm = 0x100000000
 4063fe5:      	jmpq	*%r12
 4063fe8:      	movl	$0x1, %esi
 4063fed:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4063ff4:      	je	0x406312d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa7d>
 4063ffa:      	addl	%esi, %edx
 4063ffc:      	incl	%esi
 4063ffe:      	andl	%ecx, %edx
 4064000:      	movq	%rdx, %rdi
 4064003:      	shlq	$0x4, %rdi
 4064007:      	movq	(%rax,%rdi), %rdi
 406400b:      	cmpq	%rdi, %r12
 406400e:      	je	0x40630de <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa2e>
 4064014:      	jmp	0x4063fed <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x193d>
 4064016:      	movl	$0x1, %edi
 406401b:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 4064022:      	jne	0x406402d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x197d>
 4064024:      	cmpq	$-0x1000, %r8           # imm = 0xF000
 406402b:      	je	0x4064050 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a0>
 406402d:      	addl	%edi, %edx
 406402f:      	incl	%edi
 4064031:      	andl	%esi, %edx
 4064033:      	leaq	(%rdx,%rdx,2), %r10
 4064037:      	movq	(%rax,%r10,8), %r9
 406403b:      	movq	0x8(%rax,%r10,8), %r8
 4064040:      	cmpq	%r9, %rbp
 4064043:      	jne	0x406401b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x196b>
 4064045:      	leaq	(%rax,%r10,8), %r10
 4064049:      	cmpq	%r8, %rbx
 406404c:      	je	0x4064058 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a8>
 406404e:      	jmp	0x406401b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x196b>
 4064050:      	leaq	(%rcx,%rcx,2), %rdx
 4064054:      	leaq	(%rax,%rdx,8), %r10
 4064058:      	leaq	(%rcx,%rcx,2), %rcx
 406405c:      	leaq	(%rax,%rcx,8), %rax
 4064060:      	cmpq	%rax, %r10
 4064063:      	je	0x40626f0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x40>
 4064069:      	movl	0x10(%r10), %eax
 406406d:      	movq	0x28(%rsp), %rbx
 4064072:      	movq	0x58(%rbx), %r15
 4064076:      	cmpl	%eax, -0x8(%r15)
 406407a:      	jbe	0x4062710 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 4064080:      	movl	%eax, -0x8(%r15)
 4064084:      	jmp	0x4062710 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 4064089:      	nopl	(%rax)
 4064090:      	movq	0x8(%rsp), %r12
 4064095:      	incq	%r12
 4064098:      	movq	%r12, 0x8(%rsp)
 406409d:      	cmpq	%r12, %r15
 40640a0:      	je	0x406415b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1aab>
 40640a6:      	incq	%r11
 40640a9:      	addq	$0x20, %rbp
 40640ad:      	addq	$-0x20, %r13
 40640b1:      	leaq	-0x25c5bb4(%rip), %rsi  # 0x1a9e504 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3048921120990494372+0x104>
 40640b8:      	movslq	(%rsi,%rdi,4), %r12
 40640bc:      	addq	%rsi, %r12
 40640bf:      	jmpq	*%r12
 40640c2:      	movq	0x38(%rsp), %rsi
 40640c7:      	movq	(%rsi), %r12
 40640ca:      	movq	(%r12,%rbp), %r12
 40640ce:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 40640d0:      	movq	(%r13), %r12
 40640d4:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 40640d6:      	movq	0x48(%rsp), %rsi
 40640db:      	movq	(%rsi), %r12
 40640de:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 40640e0:      	movq	-0x58(%rax), %r12
 40640e4:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 40640e6:      	movq	0x50(%rsp), %rsi
 40640eb:      	testb	$0x1, (%rsi)
 40640ee:      	jne	0x40640f5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a45>
 40640f0:      	xorl	%r12d, %r12d
 40640f3:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 40640f5:      	movl	(%r9), %r12d
 40640f8:      	shll	$0x5, %r12d
 40640fc:      	movq	%rbx, %rsi
 40640ff:      	subq	%r12, %rsi
 4064102:      	movq	0x20(%rsi), %r12
 4064106:      	nopw	%cs:(%rax,%rax)
 4064110:      	cmpq	%r12, %r10
 4064113:      	je	0x4064090 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19e0>
 4064119:      	movq	0x30(%rsp), %r15
 406411e:      	movq	0x40(%rsp), %r13
 4064123:      	movq	0x10(%rsp), %rbp
 4064128:      	jmp	0x406284a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19a>
 406412d:      	movq	0x38(%rsp), %rsi
 4064132:      	movq	(%rsi), %rsi
 4064135:      	movq	(%rsi,%rbp), %r12
 4064139:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 406413b:      	movq	0x18(%rsp), %rsi
 4064140:      	movl	(%rsi), %esi
 4064142:      	shlq	$0x5, %rsi
 4064146:      	movq	0x48(%rsp), %r12
 406414b:      	subq	%rsi, %r12
 406414e:      	movl	%r11d, %esi
 4064151:      	shlq	$0x5, %rsi
 4064155:      	movq	(%r12,%rsi), %r12
 4064159:      	jmp	0x4064110 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a60>
 406415b:      	movl	%r8d, %esi
 406415e:      	movq	%rsi, 0x8(%rsp)
 4064163:      	jmp	0x4064119 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a69>
 4064165:      	movq	0x28(%rsp), %rcx
 406416a:      	movq	0x40(%rcx), %r13
 406416e:      	movq	%r15, 0x40(%rsp)
 4064173:      	movq	%rbp, 0x8(%rsp)
 4064178:      	nopl	(%rax,%rax)
 4064180:      	movq	0x28(%rcx), %rbx
 4064184:      	addq	$-0x10, %rbx
 4064188:      	cmpq	0x48(%rcx), %r13
 406418c:      	je	0x4064290 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1be0>
 4064192:      	movups	(%rbx), %xmm0
 4064195:      	movups	%xmm0, (%r13)
 406419a:      	movq	0x40(%rcx), %r13
 406419e:      	addq	$0x10, %r13
 40641a2:      	movq	%r13, 0x40(%rcx)
 40641a6:      	addq	$-0x10, 0x28(%rcx)
 40641ab:      	movl	0x18(%rcx), %esi
 40641ae:      	testl	%esi, %esi
 40641b0:      	je	0x4064358 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ca8>
 40641b6:      	movq	0x8(%rcx), %rdx
 40641ba:      	movq	-0x10(%r13), %rcx
 40641be:      	movq	-0x8(%r13), %rdi
 40641c2:      	movl	%ecx, %eax
 40641c4:      	shrl	$0x4, %eax
 40641c7:      	movl	%ecx, %r8d
 40641ca:      	shrl	$0x9, %r8d
 40641ce:      	xorl	%eax, %r8d
 40641d1:      	movl	%edi, %eax
 40641d3:      	shrl	$0x4, %eax
 40641d6:      	movl	%edi, %r9d
 40641d9:      	shrl	$0x9, %r9d
 40641dd:      	xorl	%eax, %r9d
 40641e0:      	shlq	$0x20, %r8
 40641e4:      	orq	%r8, %r9
 40641e7:      	movabsq	$-0x40a7b892e31b1a47, %rax # imm = 0xBF58476D1CE4E5B9
 40641f1:      	imulq	%rax, %r9
 40641f5:      	movq	%r9, %r8
 40641f8:      	shrq	$0x1f, %r8
 40641fc:      	xorl	%r9d, %r8d
 40641ff:      	leal	-0x1(%rsi), %r9d
 4064203:      	andl	%r9d, %r8d
 4064206:      	leaq	(%r8,%r8,2), %r10
 406420a:      	leaq	(%rdx,%r10,8), %rax
 406420e:      	movq	(%rdx,%r10,8), %r14
 4064212:      	movq	0x8(%rdx,%r10,8), %rbx
 4064217:      	cmpq	%r14, %rcx
 406421a:      	jne	0x4064225 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b75>
 406421c:      	cmpq	%rbx, %rdi
 406421f:      	je	0x40643b2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d02>
 4064225:      	movl	$0x1, %r10d
 406422b:      	xorl	%r11d, %r11d
 406422e:      	cmpq	$-0x1000, %r14          # imm = 0xF000
 4064235:      	jne	0x4064244 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b94>
 4064237:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 406423e:      	je	0x40643d6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d26>
 4064244:      	xorq	$-0x2000, %r14          # imm = 0xE000
 406424b:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 4064252:      	orq	%r14, %rbx
 4064255:      	orq	%r11, %rbx
 4064258:      	cmoveq	%rax, %r11
 406425c:      	addl	%r10d, %r8d
 406425f:      	incl	%r10d
 4064262:      	andl	%r9d, %r8d
 4064265:      	leaq	(%r8,%r8,2), %rbx
 4064269:      	leaq	(%rdx,%rbx,8), %rax
 406426d:      	movq	(%rdx,%rbx,8), %r14
 4064271:      	movq	0x8(%rdx,%rbx,8), %rbx
 4064276:      	cmpq	%r14, %rcx
 4064279:      	jne	0x406422e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b7e>
 406427b:      	cmpq	%rbx, %rdi
 406427e:      	je	0x40643b2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d02>
 4064284:      	jmp	0x406422e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b7e>
 4064286:      	nopw	%cs:(%rax,%rax)
 4064290:      	movq	0x38(%rcx), %r14
 4064294:      	movq	%r13, %r15
 4064297:      	subq	%r14, %r15
 406429a:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 40642a4:      	cmpq	%rax, %r15
 40642a7:      	je	0x40644fc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e4c>
 40642ad:      	movq	%r15, %rax
 40642b0:      	sarq	$0x4, %rax
 40642b4:      	cmpq	$0x1, %rax
 40642b8:      	movq	%rax, %rcx
 40642bb:      	adcq	$0x0, %rcx
 40642bf:      	leaq	(%rcx,%rax), %rbp
 40642c3:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 40642cd:      	cmpq	%rdx, %rbp
 40642d0:      	cmovaeq	%rdx, %rbp
 40642d4:      	addq	%rax, %rcx
 40642d7:      	cmovbq	%rdx, %rbp
 40642db:      	shlq	$0x4, %rbp
 40642df:      	movq	%rbp, %rdi
 40642e2:      	callq	0x828a620 <_Znwm@plt>
 40642e7:      	movq	%rax, %r12
 40642ea:      	movups	(%rbx), %xmm0
 40642ed:      	movups	%xmm0, (%rax,%r15)
 40642f2:      	movq	%rax, %rbx
 40642f5:      	cmpq	%r13, %r14
 40642f8:      	je	0x4064313 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c63>
 40642fa:      	movq	%r12, %rbx
 40642fd:      	movq	%r14, %rax
 4064300:      	movups	(%rax), %xmm0
 4064303:      	movups	%xmm0, (%rbx)
 4064306:      	addq	$0x10, %rax
 406430a:      	addq	$0x10, %rbx
 406430e:      	cmpq	%r13, %rax
 4064311:      	jne	0x4064300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c50>
 4064313:      	testq	%r14, %r14
 4064316:      	je	0x4064323 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c73>
 4064318:      	movq	%r14, %rdi
 406431b:      	movq	%r15, %rsi
 406431e:      	callq	0x828a660 <_ZdlPvm@plt>
 4064323:      	addq	$0x10, %rbx
 4064327:      	movq	0x28(%rsp), %rcx
 406432c:      	movq	%r12, 0x38(%rcx)
 4064330:      	movq	%rbx, 0x40(%rcx)
 4064334:      	addq	%rbp, %r12
 4064337:      	movq	%r12, 0x48(%rcx)
 406433b:      	movq	%rbx, %r13
 406433e:      	movq	0x40(%rsp), %r15
 4064343:      	movq	0x8(%rsp), %rbp
 4064348:      	addq	$-0x10, 0x28(%rcx)
 406434d:      	movl	0x18(%rcx), %esi
 4064350:      	testl	%esi, %esi
 4064352:      	jne	0x40641b6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b06>
 4064358:      	xorl	%eax, %eax
 406435a:      	movq	%rcx, %rbx
 406435d:      	movl	0x10(%rcx), %ecx
 4064360:      	leal	0x4(,%rcx,4), %edx
 4064367:      	leal	(%rsi,%rsi,2), %edi
 406436a:      	cmpl	%edi, %edx
 406436c:      	jae	0x40643e7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d37>
 406436e:      	movl	%ecx, %edx
 4064370:      	notl	%edx
 4064372:      	addl	%esi, %edx
 4064374:      	subl	0x14(%rbx), %edx
 4064377:      	movl	%esi, %edi
 4064379:      	shrl	$0x3, %edi
 406437c:      	cmpl	%edi, %edx
 406437e:      	jbe	0x40643e9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d39>
 4064380:      	incl	%ecx
 4064382:      	movl	%ecx, 0x10(%rbx)
 4064385:      	cmpq	$-0x1000, (%rax)        # imm = 0xF000
 406438c:      	jne	0x4064398 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ce8>
 406438e:      	cmpq	$-0x1000, 0x8(%rax)     # imm = 0xF000
 4064396:      	je	0x406439b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ceb>
 4064398:      	decl	0x14(%rbx)
 406439b:      	movups	-0x10(%r13), %xmm0
 40643a0:      	movups	%xmm0, (%rax)
 40643a3:      	movl	$0x0, 0x10(%rax)
 40643aa:      	movq	0x40(%rbx), %r13
 40643ae:      	movq	-0x10(%r13), %rcx
 40643b2:      	movl	$0xffffffff, 0x10(%rax) # imm = 0xFFFFFFFF
 40643b9:      	cmpq	%r15, %rcx
 40643bc:      	movq	0x28(%rsp), %rcx
 40643c1:      	jne	0x4064180 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ad0>
 40643c7:      	cmpq	%rbp, -0x8(%r13)
 40643cb:      	jne	0x4064180 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ad0>
 40643d1:      	jmp	0x40644ea <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e3a>
 40643d6:      	testq	%r11, %r11
 40643d9:      	cmovneq	%r11, %rax
 40643dd:      	movq	0x28(%rsp), %rcx
 40643e2:      	jmp	0x406435a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1caa>
 40643e7:      	addl	%esi, %esi
 40643e9:      	movq	0x78(%rsp), %rdi
 40643ee:      	callq	0x4064790 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS4_Lj4ENS_12DenseMapInfoIS4_vEEEEEjNS6_ISA_vEENS_6detail12DenseMapPairISA_jEEEESA_jSB_SE_E4growEj>
 40643f3:      	movl	0x18(%rbx), %ecx
 40643f6:      	testl	%ecx, %ecx
 40643f8:      	je	0x40644c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e10>
 40643fe:      	movq	0x8(%rbx), %rdx
 4064402:      	movq	-0x10(%r13), %rsi
 4064406:      	movq	-0x8(%r13), %rdi
 406440a:      	movl	%esi, %eax
 406440c:      	shrl	$0x4, %eax
 406440f:      	movl	%esi, %r8d
 4064412:      	shrl	$0x9, %r8d
 4064416:      	xorl	%eax, %r8d
 4064419:      	movl	%edi, %eax
 406441b:      	shrl	$0x4, %eax
 406441e:      	movl	%edi, %r9d
 4064421:      	shrl	$0x9, %r9d
 4064425:      	xorl	%eax, %r9d
 4064428:      	shlq	$0x20, %r8
 406442c:      	orq	%r8, %r9
 406442f:      	movabsq	$-0x40a7b892e31b1a47, %rax # imm = 0xBF58476D1CE4E5B9
 4064439:      	imulq	%rax, %r9
 406443d:      	movq	%r9, %r8
 4064440:      	shrq	$0x1f, %r8
 4064444:      	xorl	%r9d, %r8d
 4064447:      	decl	%ecx
 4064449:      	andl	%ecx, %r8d
 406444c:      	leaq	(%r8,%r8,2), %r9
 4064450:      	leaq	(%rdx,%r9,8), %rax
 4064454:      	movq	(%rdx,%r9,8), %rbx
 4064458:      	movq	0x8(%rdx,%r9,8), %r11
 406445d:      	cmpq	%rbx, %rsi
 4064460:      	jne	0x4064467 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1db7>
 4064462:      	cmpq	%r11, %rdi
 4064465:      	je	0x40644c2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e12>
 4064467:      	movl	$0x1, %r9d
 406446d:      	xorl	%r10d, %r10d
 4064470:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 4064477:      	jne	0x4064482 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dd2>
 4064479:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 4064480:      	je	0x40644e1 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e31>
 4064482:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 4064489:      	xorq	$-0x2000, %r11          # imm = 0xE000
 4064490:      	orq	%rbx, %r11
 4064493:      	orq	%r10, %r11
 4064496:      	cmoveq	%rax, %r10
 406449a:      	addl	%r9d, %r8d
 406449d:      	incl	%r9d
 40644a0:      	andl	%ecx, %r8d
 40644a3:      	leaq	(%r8,%r8,2), %r11
 40644a7:      	leaq	(%rdx,%r11,8), %rax
 40644ab:      	movq	(%rdx,%r11,8), %rbx
 40644af:      	movq	0x8(%rdx,%r11,8), %r11
 40644b4:      	cmpq	%rbx, %rsi
 40644b7:      	jne	0x4064470 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dc0>
 40644b9:      	cmpq	%r11, %rdi
 40644bc:      	je	0x40644c2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e12>
 40644be:      	jmp	0x4064470 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dc0>
 40644c0:      	xorl	%eax, %eax
 40644c2:      	movq	0x28(%rsp), %rbx
 40644c7:      	movl	0x10(%rbx), %ecx
 40644ca:      	incl	%ecx
 40644cc:      	movl	%ecx, 0x10(%rbx)
 40644cf:      	cmpq	$-0x1000, (%rax)        # imm = 0xF000
 40644d6:      	je	0x406438e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cde>
 40644dc:      	jmp	0x4064398 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ce8>
 40644e1:      	testq	%r10, %r10
 40644e4:      	cmovneq	%r10, %rax
 40644e8:      	jmp	0x40644c2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e12>
 40644ea:      	addq	$0xa8, %rsp
 40644f1:      	popq	%rbx
 40644f2:      	popq	%r12
 40644f4:      	popq	%r13
 40644f6:      	popq	%r14
 40644f8:      	popq	%r15
 40644fa:      	popq	%rbp
 40644fb:      	retq
 40644fc:      	leaq	-0x33c9b19(%rip), %rdi  # 0xc9a9ea <.str.llvm.15025770437922220468>
 4064503:      	callq	0x828a730 <_ZSt20__throw_length_errorPKc@plt>
