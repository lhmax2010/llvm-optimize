
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000004062730 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv>:
 4062730:      	pushq	%rbp
 4062731:      	pushq	%r15
 4062733:      	pushq	%r14
 4062735:      	pushq	%r13
 4062737:      	pushq	%r12
 4062739:      	pushq	%rbx
 406273a:      	subq	$0xa8, %rsp
 4062741:      	movq	%rdi, %rbx
 4062744:      	movq	0x38(%rdi), %rax
 4062748:      	cmpq	%rax, 0x40(%rdi)
 406274c:      	je	0x4062752 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x22>
 406274e:      	movq	%rax, 0x40(%rbx)
 4062752:      	movq	0x58(%rbx), %r15
 4062756:      	cmpq	%r15, 0x50(%rbx)
 406275a:      	je	0x4064579 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e49>
 4062760:      	leaq	0x8(%rbx), %rax
 4062764:      	movq	%rax, 0x78(%rsp)
 4062769:      	movq	%rbx, 0x20(%rsp)
 406276e:      	jmp	0x4062790 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 4062770:      	movq	%rbx, %rdx
 4062773:      	movq	0x20(%rsp), %rbx
 4062778:      	movq	%rbx, %rdi
 406277b:      	movq	%rbp, %rsi
 406277e:      	callq	0x4061fb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE11DFSVisitOneES9_>
 4062783:      	movq	0x58(%rbx), %r15
 4062787:      	nopw	(%rax,%rax)
 4062790:      	movq	-0x60(%r15), %rcx
 4062794:      	movq	-0x58(%r15), %rax
 4062798:      	movq	%rax, 0x50(%rsp)
 406279d:      	movq	(%rcx), %rdx
 40627a0:      	movl	%edx, %edi
 40627a2:      	shrl	%edi
 40627a4:      	andl	$0x2, %edi
 40627a7:      	movq	%rdi, %r13
 40627aa:      	orq	%rcx, %r13
 40627ad:      	movq	%rdx, %r14
 40627b0:      	andq	$-0x8, %rdx
 40627b4:      	movq	0x30(%rdx), %rax
 40627b8:      	addq	$0x30, %rdx
 40627bc:      	cmpq	%rax, %rdx
 40627bf:      	movq	%r15, 0x28(%rsp)
 40627c4:      	je	0x4062880 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x150>
 40627ca:      	leaq	-0x18(%rax), %rbx
 40627ce:      	movzbl	-0x18(%rax), %r9d
 40627d3:      	leal	-0x1e(%r9), %r10d
 40627d7:      	cmpb	$0xb, %r10b
 40627db:      	movl	$0x0, %ebp
 40627e0:      	cmovbq	%rbx, %rbp
 40627e4:      	movq	%rcx, %r11
 40627e7:      	andq	$-0x8, %r11
 40627eb:      	testq	%rdi, %rdi
 40627ee:      	jne	0x40628a9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x179>
 40627f4:      	cmpb	$0xa, %r10b
 40627f8:      	ja	0x4062990 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 40627fe:      	movzbl	%r9b, %edi
 4062802:      	leal	-0x1e(%rdi), %r8d
 4062806:      	leaq	-0x25c4359(%rip), %rsi  # 0x1a9e4b4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0xb4>
 406280d:      	movslq	(%rsi,%r8,4), %r8
 4062811:      	addq	%rsi, %r8
 4062814:      	jmpq	*%r8
 4062817:      	movl	-0x14(%rax), %r8d
 406281b:      	movl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 4062820:      	andl	%esi, %r8d
 4062823:      	decl	%r8d
 4062826:      	testl	%r8d, %r8d
 4062829:      	je	0x4062990 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 406282f:      	movq	0x8(%r11), %r9
 4062833:      	movq	0x20(%r9), %r10
 4062837:      	leaq	-0x16(%rax), %rsi
 406283b:      	movq	%rsi, 0x48(%rsp)
 4062840:      	leaq	-0x14(%rax), %r9
 4062844:      	leaq	-0x20(%rax), %rsi
 4062848:      	movq	%rsi, 0x30(%rsp)
 406284d:      	leaq	0x40(%rax), %rsi
 4062851:      	movq	%rsi, 0x10(%rsp)
 4062856:      	movl	%r8d, %r15d
 4062859:      	leal	-0x20(%rdi), %r11d
 406285d:      	leaq	-0x25c4384(%rip), %rsi  # 0x1a9e4e0 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0xe0>
 4062864:      	movslq	(%rsi,%r11,4), %r11
 4062868:      	addq	%rsi, %r11
 406286b:      	jmpq	*%r11
 406286e:      	leaq	-0x20(%rax), %rsi
 4062872:      	movq	(%rsi), %r11
 4062875:      	movq	0x20(%r11), %r11
 4062879:      	jmp	0x4063fe0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b0>
 406287e:      	nop
 4062880:      	testq	%rdi, %rdi
 4062883:      	jne	0x40628a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x170>
 4062885:      	andl	$0x4, %r14d
 4062889:      	orq	%rcx, %r14
 406288c:      	movq	%r14, 0x40(%rsp)
 4062891:      	movq	$0x0, (%rsp)
 4062899:      	xorl	%ebp, %ebp
 406289b:      	jmp	0x40629d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 40628a0:      	movq	%rcx, %r11
 40628a3:      	andq	$-0x8, %r11
 40628a7:      	xorl	%ebp, %ebp
 40628a9:      	movq	0x8(%r11), %rsi
 40628ad:      	movq	0x20(%rsi), %rsi
 40628b1:      	movq	%rcx, %rdi
 40628b4:      	orq	$0x4, %rdi
 40628b8:      	cmpq	0x20(%r11), %rsi
 40628bc:      	cmoveq	%rdi, %r13
 40628c0:      	movq	$0x0, (%rsp)
 40628c8:      	andl	$0x4, %r14d
 40628cc:      	orq	%rcx, %r14
 40628cf:      	movq	%r14, 0x40(%rsp)
 40628d4:      	cmpq	%rax, %rdx
 40628d7:      	je	0x40629d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 40628dd:      	movzbl	-0x18(%rax), %r9d
 40628e2:      	leal	-0x1e(%r9), %r10d
 40628e6:      	cmpb	$0xa, %r10b
 40628ea:      	ja	0x40629d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 40628f0:      	jmp	0x40629aa <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x27a>
 40628f5:      	movq	0x8(%r11), %r8
 40628f9:      	movq	0x20(%r8), %r10
 40628fd:      	leaq	-0x16(%rax), %rsi
 4062901:      	movq	%rsi, 0x48(%rsp)
 4062906:      	leaq	-0x14(%rax), %r9
 406290a:      	leaq	-0x38(%rax), %rsi
 406290e:      	leaq	-0x20(%rax), %r8
 4062912:      	movq	%r8, 0x30(%rsp)
 4062917:      	leaq	0x40(%rax), %r8
 406291b:      	movq	%r8, 0x10(%rsp)
 4062920:      	movl	$0x1, %r8d
 4062926:      	movl	$0x1, %r15d
 406292c:      	movq	(%rsi), %r11
 406292f:      	jmp	0x4063fe4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b4>
 4062934:      	movq	0x8(%r11), %r8
 4062938:      	movq	0x20(%r8), %r10
 406293c:      	leaq	-0x16(%rax), %rsi
 4062940:      	movq	%rsi, 0x48(%rsp)
 4062945:      	leaq	-0x14(%rax), %r9
 4062949:      	leaq	-0x38(%rax), %rsi
 406294d:      	leaq	-0x20(%rax), %r8
 4062951:      	movq	%r8, 0x30(%rsp)
 4062956:      	leaq	0x40(%rax), %r8
 406295a:      	movq	%r8, 0x10(%rsp)
 406295f:      	movl	$0x2, %r8d
 4062965:      	movl	$0x2, %r15d
 406296b:      	movq	-0x78(%rax), %r11
 406296f:      	jmp	0x4063fe4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b4>
 4062974:      	movl	0x40(%rax), %r8d
 4062978:      	incl	%r8d
 406297b:      	testl	%r8d, %r8d
 406297e:      	jne	0x406282f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xff>
 4062984:      	nopw	%cs:(%rax,%rax)
 406298e:      	nop
 4062990:      	andl	$0x4, %r14d
 4062994:      	orq	%rcx, %r14
 4062997:      	movq	%r14, 0x40(%rsp)
 406299c:      	movq	$0x0, (%rsp)
 40629a4:      	cmpb	$0xa, %r10b
 40629a8:      	ja	0x40629d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 40629aa:      	movzbl	%r9b, %ecx
 40629ae:      	addl	$-0x1e, %ecx
 40629b1:      	leaq	-0x25c448c(%rip), %rdx  # 0x1a9e52c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x12c>
 40629b8:      	movslq	(%rdx,%rcx,4), %rcx
 40629bc:      	addq	%rdx, %rcx
 40629bf:      	jmpq	*%rcx
 40629c1:      	nopw	%cs:(%rax,%rax)
 40629cb:      	nopl	(%rax,%rax)
 40629d0:      	xorl	%esi, %esi
 40629d2:      	cmpq	$0x0, 0x50(%rsp)
 40629d8:      	leaq	0x2181(%rip), %rcx      # 0x4064b60 <_ZN12_GLOBAL__N_114SubGraphTraits9filterSetERKSt4pairIPN4llvm10RegionNodeEPNS2_13SmallDenseSetIS4_Lj4ENS2_12DenseMapInfoIS4_vEEEEE>
 40629df:      	leaq	0x21ea(%rip), %rax      # 0x4064bd0 <_ZN12_GLOBAL__N_114SubGraphTraits9filterAllERKSt4pairIPN4llvm10RegionNodeEPNS2_13SmallDenseSetIS4_Lj4ENS2_12DenseMapInfoIS4_vEEEEE>
 40629e6:      	cmoveq	%rax, %rcx
 40629ea:      	movq	%rcx, 0x30(%rsp)
 40629ef:      	movl	%r13d, %eax
 40629f2:      	xorl	0x40(%rsp), %eax
 40629f6:      	xorl	%ecx, %ecx
 40629f8:      	testb	$0x6, %al
 40629fa:      	setne	%cl
 40629fd:      	xorl	%edx, %edx
 40629ff:      	movl	%esi, 0x10(%rsp)
 4062a03:      	cmpl	%esi, (%rsp)
 4062a06:      	setne	%dl
 4062a09:      	testb	$0x6, %r13b
 4062a0d:      	sete	%al
 4062a10:      	cmovel	%edx, %ecx
 4062a13:      	cmpb	$0x1, %cl
 4062a16:      	jne	0x40630c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x990>
 4062a1c:      	movq	0x40(%rsp), %rcx
 4062a21:      	andl	$0x6, %ecx
 4062a24:      	movq	%rcx, 0x48(%rsp)
 4062a29:      	leaq	-0x20(%rbp), %rcx
 4062a2d:      	movq	%rcx, 0x18(%rsp)
 4062a32:      	movq	%rbp, 0x8(%rsp)
 4062a37:      	movq	(%rsp), %rcx
 4062a3b:      	leal	0x1(%rcx), %edx
 4062a3e:      	movq	%rdx, 0x88(%rsp)
 4062a46:      	xorl	%esi, %esi
 4062a48:      	movl	%ecx, %edi
 4062a4a:      	subl	$0x1, %edi
 4062a4d:      	setae	%sil
 4062a51:      	shll	$0x5, %esi
 4062a54:      	addq	$-0x60, %rsi
 4062a58:      	movq	%rsi, 0xa0(%rsp)
 4062a60:      	movl	%ecx, %ecx
 4062a62:      	movq	%rcx, 0x80(%rsp)
 4062a6a:      	movq	%rcx, %rsi
 4062a6d:      	shlq	$0x5, %rsi
 4062a71:      	movq	0x18(%rsp), %rcx
 4062a76:      	movq	%rcx, %r8
 4062a79:      	movq	%rsi, 0x58(%rsp)
 4062a7e:      	subq	%rsi, %r8
 4062a81:      	movq	%r8, 0x98(%rsp)
 4062a89:      	shlq	$0x5, %rdi
 4062a8d:      	addq	%rcx, %rdi
 4062a90:      	movq	%rdi, 0x90(%rsp)
 4062a98:      	shlq	$0x5, %rdx
 4062a9c:      	movq	%rdx, 0x70(%rsp)
 4062aa1:      	nopw	%cs:(%rax,%rax)
 4062aab:      	nopl	(%rax,%rax)
 4062ab0:      	testb	$0x1, %al
 4062ab2:      	je	0x4062ae0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x3b0>
 4062ab4:      	movzbl	(%rbp), %eax
 4062ab8:      	addl	$-0x1f, %eax
 4062abb:      	leaq	-0x25c456a(%rip), %rcx  # 0x1a9e558 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x158>
 4062ac2:      	movslq	(%rcx,%rax,4), %rax
 4062ac6:      	addq	%rcx, %rax
 4062ac9:      	jmpq	*%rax
 4062acb:      	movq	-0x8(%rbp), %rax
 4062acf:      	movq	0x70(%rsp), %rcx
 4062ad4:      	movq	(%rax,%rcx), %r14
 4062ad8:      	jmp	0x4062b59 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x429>
 4062ada:      	nopw	(%rax,%rax)
 4062ae0:      	movq	%r13, %rax
 4062ae3:      	andq	$-0x8, %rax
 4062ae7:      	movq	0x20(%rax), %r14
 4062aeb:      	jmp	0x4062b60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x430>
 4062aed:      	movq	0xa0(%rsp), %rax
 4062af5:      	movq	(%rbp,%rax), %r14
 4062afa:      	jmp	0x4062b59 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x429>
 4062afc:      	cmpl	$0x0, (%rsp)
 4062b00:      	je	0x4062b47 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x417>
 4062b02:      	movl	0x58(%rbp), %eax
 4062b05:      	shlq	$0x5, %rax
 4062b09:      	movq	0x90(%rsp), %rcx
 4062b11:      	subq	%rax, %rcx
 4062b14:      	movq	(%rcx), %r14
 4062b17:      	jmp	0x4062b59 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x429>
 4062b19:      	testb	$0x1, 0x2(%rbp)
 4062b1d:      	jne	0x4062b35 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x405>
 4062b1f:      	xorl	%r14d, %r14d
 4062b22:      	jmp	0x4062b59 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x429>
 4062b24:      	movq	0x98(%rsp), %rax
 4062b2c:      	jmp	0x4062b56 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x426>
 4062b2e:      	movq	0x18(%rsp), %rax
 4062b33:      	jmp	0x4062b56 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x426>
 4062b35:      	movl	0x4(%rbp), %eax
 4062b38:      	shll	$0x5, %eax
 4062b3b:      	movq	%rbp, %rcx
 4062b3e:      	subq	%rax, %rcx
 4062b41:      	movq	0x20(%rcx), %r14
 4062b45:      	jmp	0x4062b59 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x429>
 4062b47:      	movl	0x58(%rbp), %eax
 4062b4a:      	shlq	$0x5, %rax
 4062b4e:      	negq	%rax
 4062b51:      	leaq	-0x40(%rbp,%rax), %rax
 4062b56:      	movq	(%rax), %r14
 4062b59:      	movq	%r13, %rax
 4062b5c:      	andq	$-0x8, %rax
 4062b60:      	movq	0x8(%rax), %r12
 4062b64:      	movq	0x10(%r12), %rax
 4062b69:      	movl	0x38(%rax), %ecx
 4062b6c:      	testl	%ecx, %ecx
 4062b6e:      	je	0x4062bdc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4ac>
 4062b70:      	movq	0x28(%rax), %rax
 4062b74:      	movl	%r14d, %esi
 4062b77:      	shrl	$0x4, %esi
 4062b7a:      	movl	%r14d, %edx
 4062b7d:      	shrl	$0x9, %edx
 4062b80:      	xorl	%esi, %edx
 4062b82:      	decl	%ecx
 4062b84:      	andl	%ecx, %edx
 4062b86:      	movl	%edx, %esi
 4062b88:      	shll	$0x4, %esi
 4062b8b:      	movq	(%rax,%rsi), %rdi
 4062b8f:      	cmpq	%rdi, %r14
 4062b92:      	jne	0x4062d42 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x612>
 4062b98:      	shlq	$0x4, %rdx
 4062b9c:      	movq	0x8(%rax,%rdx), %rax
 4062ba1:      	testq	%rax, %rax
 4062ba4:      	je	0x4062bdc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4ac>
 4062ba6:      	cmpq	%r12, %rax
 4062ba9:      	je	0x4062bdc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4ac>
 4062bab:      	nopl	(%rax,%rax)
 4062bb0:      	movq	%rax, %rbx
 4062bb3:      	movq	0x8(%rax), %rsi
 4062bb7:      	movq	%r12, %rdi
 4062bba:      	callq	0x3361660 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 4062bbf:      	testb	%al, %al
 4062bc1:      	je	0x4062bcc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x49c>
 4062bc3:      	movq	0x8(%rbx), %rax
 4062bc7:      	cmpq	%r12, %rax
 4062bca:      	jne	0x4062bb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x480>
 4062bcc:      	movq	(%rbx), %rax
 4062bcf:      	andq	$-0x8, %rax
 4062bd3:      	cmpq	%rax, %r14
 4062bd6:      	je	0x4062d02 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5d2>
 4062bdc:      	movq	%r13, 0x38(%rsp)
 4062be1:      	movq	0x50(%r12), %rax
 4062be6:      	leaq	0x48(%r12), %rbp
 4062beb:      	movq	%rbp, %r13
 4062bee:      	testq	%rax, %rax
 4062bf1:      	je	0x4062c26 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4f6>
 4062bf3:      	movq	%rbp, %r13
 4062bf6:      	nopw	%cs:(%rax,%rax)
 4062c00:      	xorl	%ecx, %ecx
 4062c02:      	cmpq	%r14, 0x20(%rax)
 4062c06:      	setb	%cl
 4062c09:      	cmovaeq	%rax, %r13
 4062c0d:      	movq	0x10(%rax,%rcx,8), %rax
 4062c12:      	testq	%rax, %rax
 4062c15:      	jne	0x4062c00 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4d0>
 4062c17:      	cmpq	%rbp, %r13
 4062c1a:      	je	0x4062c26 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4f6>
 4062c1c:      	cmpq	0x20(%r13), %r14
 4062c20:      	jae	0x4062cf4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5c4>
 4062c26:      	movq	%r13, %rbx
 4062c29:      	leaq	0x40(%r12), %r15
 4062c2e:      	movl	$0x30, %edi
 4062c33:      	callq	0x828a6b0 <_Znwm@plt>
 4062c38:      	movq	%rax, %r13
 4062c3b:      	addq	$0x20, %rax
 4062c3f:      	movq	%r14, 0x20(%r13)
 4062c43:      	movq	$0x0, 0x28(%r13)
 4062c4b:      	movq	%r15, %rdi
 4062c4e:      	movq	%rax, %r15
 4062c51:      	movq	%rbx, %rsi
 4062c54:      	movq	%rax, %rdx
 4062c57:      	callq	0x33691a0 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 4062c5c:      	movq	%rax, %rbx
 4062c5f:      	testq	%rdx, %rdx
 4062c62:      	je	0x4062ca0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x570>
 4062c64:      	testq	%rbx, %rbx
 4062c67:      	setne	%al
 4062c6a:      	cmpq	%rbp, %rdx
 4062c6d:      	sete	%cl
 4062c70:      	orb	%al, %cl
 4062c72:      	movb	$0x1, %al
 4062c74:      	jne	0x4062c80 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x550>
 4062c76:      	movq	(%r15), %rax
 4062c79:      	cmpq	0x20(%rdx), %rax
 4062c7d:      	setb	%al
 4062c80:      	movzbl	%al, %edi
 4062c83:      	movq	%r13, %rsi
 4062c86:      	movq	%rbp, %rcx
 4062c89:      	callq	0x828a7e0 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 4062c8e:      	incq	0x68(%r12)
 4062c93:      	jmp	0x4062cc3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x593>
 4062c95:      	nopw	%cs:(%rax,%rax)
 4062c9f:      	nop
 4062ca0:      	movq	0x28(%r13), %rdi
 4062ca4:      	testq	%rdi, %rdi
 4062ca7:      	je	0x4062cb3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x583>
 4062ca9:      	movl	$0x10, %esi
 4062cae:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4062cb3:      	movl	$0x30, %esi
 4062cb8:      	movq	%r13, %rdi
 4062cbb:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4062cc0:      	movq	%rbx, %r13
 4062cc3:      	movq	0x28(%rsp), %r15
 4062cc8:      	movl	$0x10, %edi
 4062ccd:      	callq	0x828a6b0 <_Znwm@plt>
 4062cd2:      	andq	$-0x5, %r14
 4062cd6:      	movq	%r14, (%rax)
 4062cd9:      	movq	%r12, 0x8(%rax)
 4062cdd:      	movq	0x28(%r13), %rdi
 4062ce1:      	movq	%rax, 0x28(%r13)
 4062ce5:      	testq	%rdi, %rdi
 4062ce8:      	je	0x4062cf4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x5c4>
 4062cea:      	movl	$0x10, %esi
 4062cef:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4062cf4:      	movq	0x28(%r13), %rbx
 4062cf8:      	movq	0x38(%rsp), %r13
 4062cfd:      	movq	0x8(%rsp), %rbp
 4062d02:      	movq	%rbx, 0x60(%rsp)
 4062d07:      	movq	0x50(%rsp), %rax
 4062d0c:      	movq	%rax, 0x68(%rsp)
 4062d11:      	leaq	0x60(%rsp), %rdi
 4062d16:      	callq	*0x30(%rsp)
 4062d1a:      	testb	%al, %al
 4062d1c:      	jne	0x40630c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x990>
 4062d22:      	testb	$0x6, %r13b
 4062d26:      	je	0x4062d70 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x640>
 4062d28:      	andq	$-0x7, %r13
 4062d2c:      	orq	$0x4, %r13
 4062d30:      	xorl	%eax, %eax
 4062d32:      	cmpl	$0x4, 0x48(%rsp)
 4062d37:      	jne	0x4062ab0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x380>
 4062d3d:      	jmp	0x40630c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x990>
 4062d42:      	movl	$0x1, %esi
 4062d47:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4062d4e:      	je	0x4062bdc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x4ac>
 4062d54:      	addl	%esi, %edx
 4062d56:      	incl	%esi
 4062d58:      	andl	%ecx, %edx
 4062d5a:      	movq	%rdx, %rdi
 4062d5d:      	shlq	$0x4, %rdi
 4062d61:      	movq	(%rax,%rdi), %rdi
 4062d65:      	cmpq	%rdi, %r14
 4062d68:      	je	0x4062b98 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x468>
 4062d6e:      	jmp	0x4062d47 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x617>
 4062d70:      	movq	%r13, %rax
 4062d73:      	andq	$-0x8, %rax
 4062d77:      	movq	(%rax), %rdx
 4062d7a:      	andq	$-0x8, %rdx
 4062d7e:      	movq	0x30(%rdx), %rcx
 4062d82:      	addq	$0x30, %rdx
 4062d86:      	cmpq	%rcx, %rdx
 4062d89:      	movq	0x88(%rsp), %r8
 4062d91:      	je	0x4062dc4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x694>
 4062d93:      	movzbl	-0x18(%rcx), %edx
 4062d97:      	leal	-0x1e(%rdx), %esi
 4062d9a:      	cmpb	$0xb, %sil
 4062d9e:      	jae	0x4062e8e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x75e>
 4062da4:      	addl	$-0x1e, %edx
 4062da7:      	leaq	-0x25c4806(%rip), %rsi  # 0x1a9e5a8 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x1a8>
 4062dae:      	movslq	(%rsi,%rdx,4), %rdx
 4062db2:      	addq	%rsi, %rdx
 4062db5:      	jmpq	*%rdx
 4062db7:      	movq	$0x0, (%rsp)
 4062dbf:      	jmp	0x4062f9d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x86d>
 4062dc4:      	movq	0x80(%rsp), %r8
 4062dcc:      	leaq	0x1(%r8), %rcx
 4062dd0:      	shlq	$0x5, %r8
 4062dd4:      	addq	0x18(%rsp), %r8
 4062dd9:      	movl	0x10(%rsp), %edx
 4062ddd:      	jmp	0x4062e13 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6e3>
 4062ddf:      	movq	-0x40(%rbp), %rdx
 4062de3:      	nopw	%cs:(%rax,%rax)
 4062ded:      	nopl	(%rax)
 4062df0:      	movq	0x8(%rax), %rsi
 4062df4:      	incq	%rcx
 4062df7:      	addq	$0x20, %r8
 4062dfb:      	movq	(%rsp), %rdi
 4062dff:      	incl	%edi
 4062e01:      	movq	%rdi, (%rsp)
 4062e05:      	cmpq	%rdx, 0x20(%rsi)
 4062e09:      	movl	0x10(%rsp), %edx
 4062e0d:      	jne	0x4063090 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x960>
 4062e13:      	testl	%ecx, %ecx
 4062e15:      	je	0x4062f5e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x82e>
 4062e1b:      	movzbl	(%rbp), %edx
 4062e1f:      	addl	$-0x1f, %edx
 4062e22:      	leaq	-0x25c482d(%rip), %rsi  # 0x1a9e5fc <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x1fc>
 4062e29:      	movslq	(%rsi,%rdx,4), %rdx
 4062e2d:      	addq	%rsi, %rdx
 4062e30:      	jmpq	*%rdx
 4062e32:      	leal	0x1(%rcx), %edx
 4062e35:      	movq	-0x8(%rbp), %rsi
 4062e39:      	shlq	$0x5, %rdx
 4062e3d:      	movq	(%rsi,%rdx), %rdx
 4062e41:      	jmp	0x4062df0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6c0>
 4062e43:      	movl	0x58(%rbp), %edx
 4062e46:      	shlq	$0x5, %rdx
 4062e4a:      	movq	%r8, %rsi
 4062e4d:      	jmp	0x4062e64 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x734>
 4062e4f:      	testb	$0x1, 0x2(%rbp)
 4062e53:      	jne	0x4062e79 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x749>
 4062e55:      	xorl	%edx, %edx
 4062e57:      	jmp	0x4062df0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6c0>
 4062e59:      	movl	%ecx, %edx
 4062e5b:      	shlq	$0x5, %rdx
 4062e5f:      	movq	0x18(%rsp), %rsi
 4062e64:      	subq	%rdx, %rsi
 4062e67:      	movq	(%rsi), %rdx
 4062e6a:      	jmp	0x4062df0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6c0>
 4062e6c:      	movq	0x18(%rsp), %rdx
 4062e71:      	movq	(%rdx), %rdx
 4062e74:      	jmp	0x4062df0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6c0>
 4062e79:      	movl	0x4(%rbp), %edx
 4062e7c:      	shll	$0x5, %edx
 4062e7f:      	movq	%rbp, %rsi
 4062e82:      	subq	%rdx, %rsi
 4062e85:      	movq	0x20(%rsi), %rdx
 4062e89:      	jmp	0x4062df0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x6c0>
 4062e8e:      	movq	0x80(%rsp), %rcx
 4062e96:      	incq	%rcx
 4062e99:      	movq	0x58(%rsp), %rdx
 4062e9e:      	addq	0x18(%rsp), %rdx
 4062ea3:      	movq	%rdx, 0x58(%rsp)
 4062ea8:      	movl	0x10(%rsp), %edx
 4062eac:      	jmp	0x4062ee5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x7b5>
 4062eae:      	movq	-0x40(%rbp), %rdx
 4062eb2:      	nopw	%cs:(%rax,%rax)
 4062ebc:      	nopl	(%rax)
 4062ec0:      	movq	0x8(%rax), %rsi
 4062ec4:      	incq	%rcx
 4062ec7:      	addq	$0x20, 0x58(%rsp)
 4062ecd:      	movq	(%rsp), %rdi
 4062ed1:      	incl	%edi
 4062ed3:      	movq	%rdi, (%rsp)
 4062ed7:      	cmpq	%rdx, 0x20(%rsi)
 4062edb:      	movl	0x10(%rsp), %edx
 4062edf:      	jne	0x4063090 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x960>
 4062ee5:      	testl	%ecx, %ecx
 4062ee7:      	je	0x4062f5e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x82e>
 4062ee9:      	movzbl	(%rbp), %edx
 4062eed:      	addl	$-0x1f, %edx
 4062ef0:      	leaq	-0x25c4977(%rip), %rsi  # 0x1a9e580 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x180>
 4062ef7:      	movslq	(%rsi,%rdx,4), %rdx
 4062efb:      	addq	%rsi, %rdx
 4062efe:      	jmpq	*%rdx
 4062f00:      	leal	0x1(%rcx), %edx
 4062f03:      	movq	-0x8(%rbp), %rsi
 4062f07:      	shlq	$0x5, %rdx
 4062f0b:      	movq	(%rsi,%rdx), %rdx
 4062f0f:      	jmp	0x4062ec0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x790>
 4062f11:      	movl	0x58(%rbp), %edx
 4062f14:      	shlq	$0x5, %rdx
 4062f18:      	movq	0x58(%rsp), %rsi
 4062f1d:      	jmp	0x4062f34 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x804>
 4062f1f:      	testb	$0x1, 0x2(%rbp)
 4062f23:      	jne	0x4062f49 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x819>
 4062f25:      	xorl	%edx, %edx
 4062f27:      	jmp	0x4062ec0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x790>
 4062f29:      	movl	%ecx, %edx
 4062f2b:      	shlq	$0x5, %rdx
 4062f2f:      	movq	0x18(%rsp), %rsi
 4062f34:      	subq	%rdx, %rsi
 4062f37:      	movq	(%rsi), %rdx
 4062f3a:      	jmp	0x4062ec0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x790>
 4062f3c:      	movq	0x18(%rsp), %rdx
 4062f41:      	movq	(%rdx), %rdx
 4062f44:      	jmp	0x4062ec0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x790>
 4062f49:      	movl	0x4(%rbp), %edx
 4062f4c:      	shll	$0x5, %edx
 4062f4f:      	movq	%rbp, %rsi
 4062f52:      	subq	%rdx, %rsi
 4062f55:      	movq	0x20(%rsi), %rdx
 4062f59:      	jmp	0x4062ec0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x790>
 4062f5e:      	movq	$0x0, (%rsp)
 4062f66:      	jmp	0x4063090 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x960>
 4062f6b:      	movl	-0x14(%rcx), %edx
 4062f6e:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4062f73:      	andl	%ecx, %edx
 4062f75:      	decl	%edx
 4062f77:      	movq	%rdx, (%rsp)
 4062f7b:      	jmp	0x4062f9d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x86d>
 4062f7d:      	movl	$0x1, %ecx
 4062f82:      	jmp	0x4062f99 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x869>
 4062f84:      	movl	$0x2, %ecx
 4062f89:      	jmp	0x4062f99 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x869>
 4062f8b:      	movl	0x40(%rcx), %ecx
 4062f8e:      	incl	%ecx
 4062f90:      	jmp	0x4062f99 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x869>
 4062f92:      	movzwl	-0x16(%rcx), %ecx
 4062f96:      	andl	$0x1, %ecx
 4062f99:      	movq	%rcx, (%rsp)
 4062f9d:      	movl	0x10(%rsp), %edx
 4062fa1:      	jmp	0x4062fd5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x8a5>
 4062fa3:      	xorl	%ecx, %ecx
 4062fa5:      	testl	%r8d, %r8d
 4062fa8:      	setne	%cl
 4062fab:      	shll	$0x5, %ecx
 4062fae:      	movq	-0x60(%rcx,%rbp), %rcx
 4062fb3:      	nopw	%cs:(%rax,%rax)
 4062fbd:      	nopl	(%rax)
 4062fc0:      	movq	0x8(%rax), %rdx
 4062fc4:      	incl	%r8d
 4062fc7:      	cmpq	%rcx, 0x20(%rdx)
 4062fcb:      	movl	0x10(%rsp), %edx
 4062fcf:      	jne	0x4063080 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x950>
 4062fd5:      	cmpl	%r8d, (%rsp)
 4062fd9:      	je	0x4063090 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x960>
 4062fdf:      	movzbl	(%rbp), %ecx
 4062fe3:      	addl	$-0x1f, %ecx
 4062fe6:      	leaq	-0x25c4a19(%rip), %rdx  # 0x1a9e5d4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x1d4>
 4062fed:      	movslq	(%rdx,%rcx,4), %rcx
 4062ff1:      	addq	%rdx, %rcx
 4062ff4:      	jmpq	*%rcx
 4062ff6:      	leal	0x1(%r8), %ecx
 4062ffa:      	movq	-0x8(%rbp), %rdx
 4062ffe:      	shlq	$0x5, %rcx
 4063002:      	movq	(%rdx,%rcx), %rcx
 4063006:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 4063008:      	leal	-0x1(%r8), %ecx
 406300c:      	movl	0x58(%rbp), %edx
 406300f:      	shlq	$0x5, %rdx
 4063013:      	movq	%rbp, %rsi
 4063016:      	subq	%rdx, %rsi
 4063019:      	addq	$-0x40, %rsi
 406301d:      	movq	0x18(%rsp), %rdi
 4063022:      	subq	%rdx, %rdi
 4063025:      	movl	%ecx, %ecx
 4063027:      	shlq	$0x5, %rcx
 406302b:      	addq	%rdi, %rcx
 406302e:      	testl	%r8d, %r8d
 4063031:      	cmoveq	%rsi, %rcx
 4063035:      	movq	(%rcx), %rcx
 4063038:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 406303a:      	testb	$0x1, 0x2(%rbp)
 406303e:      	jne	0x406306b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x93b>
 4063040:      	xorl	%ecx, %ecx
 4063042:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 4063047:      	movl	%r8d, %ecx
 406304a:      	shlq	$0x5, %rcx
 406304e:      	movq	0x18(%rsp), %rdx
 4063053:      	subq	%rcx, %rdx
 4063056:      	movq	(%rdx), %rcx
 4063059:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 406305e:      	movq	0x18(%rsp), %rcx
 4063063:      	movq	(%rcx), %rcx
 4063066:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 406306b:      	movl	0x4(%rbp), %ecx
 406306e:      	shll	$0x5, %ecx
 4063071:      	movq	%rbp, %rdx
 4063074:      	subq	%rcx, %rdx
 4063077:      	movq	0x20(%rdx), %rcx
 406307b:      	jmp	0x4062fc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x890>
 4063080:      	decl	%r8d
 4063083:      	movl	%r8d, %eax
 4063086:      	movq	%rax, (%rsp)
 406308a:      	nopw	(%rax,%rax)
 4063090:      	movb	$0x1, %al
 4063092:      	cmpl	%edx, (%rsp)
 4063095:      	jne	0x4062a37 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x307>
 406309b:      	jmp	0x40630c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x990>
 406309d:      	movl	-0x14(%rcx), %ecx
 40630a0:      	movl	$0x7ffffff, %edx        # imm = 0x7FFFFFF
 40630a5:      	andl	%edx, %ecx
 40630a7:      	xorl	%edx, %edx
 40630a9:      	cmpl	$0x3, %ecx
 40630ac:      	sete	%dl
 40630af:      	incl	%edx
 40630b1:      	movq	%rdx, (%rsp)
 40630b5:      	jmp	0x4062f9d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x86d>
 40630ba:      	nopw	(%rax,%rax)
 40630c0:      	movq	-0x50(%r15), %rax
 40630c4:      	movl	%eax, %ecx
 40630c6:      	xorl	0x40(%rsp), %eax
 40630ca:      	xorl	%edx, %edx
 40630cc:      	testb	$0x6, %al
 40630ce:      	setne	%dl
 40630d1:      	xorl	%eax, %eax
 40630d3:      	movl	0x10(%rsp), %esi
 40630d7:      	cmpl	%esi, -0x40(%r15)
 40630db:      	setne	%al
 40630de:      	testb	$0x6, %cl
 40630e1:      	cmovel	%eax, %edx
 40630e4:      	movq	0x20(%rsp), %rcx
 40630e9:      	movq	0x58(%rcx), %r12
 40630ed:      	cmpb	$0x1, %dl
 40630f0:      	jne	0x4063270 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb40>
 40630f6:      	movq	-0x50(%r12), %r15
 40630fb:      	movl	-0x40(%r12), %ebx
 4063100:      	movq	-0x38(%r12), %rax
 4063105:      	movq	%rax, 0x8(%rsp)
 406310a:      	testb	$0x6, %r15b
 406310e:      	movq	%r12, (%rsp)
 4063112:      	je	0x40632cb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb9b>
 4063118:      	movq	%r15, %rax
 406311b:      	andq	$-0x7, %rax
 406311f:      	orq	$0x4, %rax
 4063123:      	movq	%rax, -0x50(%r12)
 4063128:      	movl	-0x30(%r12), %ecx
 406312d:      	andl	$0x6, %ecx
 4063130:      	cmpl	$0x4, %ecx
 4063133:      	jne	0x4063473 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd43>
 4063139:      	andq	$-0x8, %r15
 406313d:      	movq	0x20(%r15), %r12
 4063141:      	movq	0x8(%rsp), %rbx
 4063146:      	movq	0x8(%r15), %r13
 406314a:      	movq	0x10(%r13), %rax
 406314e:      	movl	0x38(%rax), %ecx
 4063151:      	testl	%ecx, %ecx
 4063153:      	je	0x40631bd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa8d>
 4063155:      	movq	0x28(%rax), %rax
 4063159:      	movl	%r12d, %esi
 406315c:      	shrl	$0x4, %esi
 406315f:      	movl	%r12d, %edx
 4063162:      	shrl	$0x9, %edx
 4063165:      	xorl	%esi, %edx
 4063167:      	decl	%ecx
 4063169:      	andl	%ecx, %edx
 406316b:      	movl	%edx, %esi
 406316d:      	shll	$0x4, %esi
 4063170:      	movq	(%rax,%rsi), %rdi
 4063174:      	cmpq	%rdi, %r12
 4063177:      	jne	0x4064075 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1945>
 406317d:      	shlq	$0x4, %rdx
 4063181:      	movq	0x8(%rax,%rdx), %rax
 4063186:      	testq	%rax, %rax
 4063189:      	je	0x40631bd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa8d>
 406318b:      	cmpq	%r13, %rax
 406318e:      	je	0x40631bd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa8d>
 4063190:      	movq	%rax, %rbp
 4063193:      	movq	0x8(%rax), %rsi
 4063197:      	movq	%r13, %rdi
 406319a:      	callq	0x3361660 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 406319f:      	testb	%al, %al
 40631a1:      	je	0x40631ac <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa7c>
 40631a3:      	movq	0x8(%rbp), %rax
 40631a7:      	cmpq	%r13, %rax
 40631aa:      	jne	0x4063190 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa60>
 40631ac:      	movq	(%rbp), %rax
 40631b0:      	andq	$-0x8, %rax
 40631b4:      	cmpq	%rax, %r12
 40631b7:      	je	0x4063933 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1203>
 40631bd:      	movq	0x50(%r13), %rax
 40631c1:      	leaq	0x48(%r13), %r14
 40631c5:      	movq	%r14, %rbp
 40631c8:      	testq	%rax, %rax
 40631cb:      	je	0x40631f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xac6>
 40631cd:      	movq	%r14, %rbp
 40631d0:      	xorl	%ecx, %ecx
 40631d2:      	cmpq	%r12, 0x20(%rax)
 40631d6:      	setb	%cl
 40631d9:      	cmovaeq	%rax, %rbp
 40631dd:      	movq	0x10(%rax,%rcx,8), %rax
 40631e2:      	testq	%rax, %rax
 40631e5:      	jne	0x40631d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xaa0>
 40631e7:      	cmpq	%r14, %rbp
 40631ea:      	je	0x40631f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xac6>
 40631ec:      	cmpq	0x20(%rbp), %r12
 40631f0:      	jae	0x406392f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ff>
 40631f6:      	movq	%rbp, %rbx
 40631f9:      	leaq	0x40(%r13), %r15
 40631fd:      	movl	$0x30, %edi
 4063202:      	callq	0x828a6b0 <_Znwm@plt>
 4063207:      	movq	%rax, %rbp
 406320a:      	addq	$0x20, %rax
 406320e:      	movq	%r12, 0x20(%rbp)
 4063212:      	movq	$0x0, 0x28(%rbp)
 406321a:      	movq	%r15, %rdi
 406321d:      	movq	%rax, %r15
 4063220:      	movq	%rbx, %rsi
 4063223:      	movq	%rax, %rdx
 4063226:      	callq	0x33691a0 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 406322b:      	movq	%rax, %rbx
 406322e:      	testq	%rdx, %rdx
 4063231:      	je	0x40638db <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ab>
 4063237:      	testq	%rbx, %rbx
 406323a:      	setne	%al
 406323d:      	cmpq	%r14, %rdx
 4063240:      	sete	%cl
 4063243:      	orb	%al, %cl
 4063245:      	movb	$0x1, %al
 4063247:      	jne	0x4063253 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb23>
 4063249:      	movq	(%r15), %rax
 406324c:      	cmpq	0x20(%rdx), %rax
 4063250:      	setb	%al
 4063253:      	movzbl	%al, %edi
 4063256:      	movq	%rbp, %rsi
 4063259:      	movq	%r14, %rcx
 406325c:      	callq	0x828a7e0 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 4063261:      	incq	0x68(%r13)
 4063265:      	jmp	0x40638fe <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ce>
 406326a:      	nopw	(%rax,%rax)
 4063270:      	leaq	-0x60(%r12), %rax
 4063275:      	movq	-0x60(%r12), %r15
 406327a:      	movq	-0x58(%r12), %rbp
 406327f:      	movl	-0x8(%r12), %ebx
 4063284:      	movq	%rax, 0x58(%rcx)
 4063288:      	cmpq	%rax, 0x50(%rcx)
 406328c:      	je	0x406329a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb6a>
 406328e:      	cmpl	%ebx, -0x68(%r12)
 4063293:      	jbe	0x406329a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xb6a>
 4063295:      	movl	%ebx, -0x68(%r12)
 406329a:      	movq	0x78(%rsp), %rdi
 406329f:      	movq	%r15, %rsi
 40632a2:      	movq	%rbp, %rdx
 40632a5:      	callq	0x40645a0 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS4_Lj4ENS_12DenseMapInfoIS4_vEEEEEjNS6_ISA_vEENS_6detail12DenseMapPairISA_jEEEESA_jSB_SE_E24lookupOrInsertIntoBucketIRKSA_JEEES2_IPSE_bEOT_DpOT0_>
 40632aa:      	cmpl	0x10(%rax), %ebx
 40632ad:      	je	0x40641f4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ac4>
 40632b3:      	movq	0x20(%rsp), %rbx
 40632b8:      	movq	0x58(%rbx), %r15
 40632bc:      	cmpq	%r15, 0x50(%rbx)
 40632c0:      	jne	0x4062790 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 40632c6:      	jmp	0x4064579 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e49>
 40632cb:      	movq	-0x48(%r12), %r14
 40632d0:      	movq	%r15, %rbp
 40632d3:      	andq	$-0x8, %rbp
 40632d7:      	leaq	-0x20(%r14), %rax
 40632db:      	movq	%rax, 0x28(%rsp)
 40632e0:      	leal	0x1(%rbx), %edx
 40632e3:      	jmp	0x4063311 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbe1>
 40632e5:      	xorl	%ecx, %ecx
 40632e7:      	testl	%eax, %eax
 40632e9:      	setne	%cl
 40632ec:      	shll	$0x5, %ecx
 40632ef:      	movq	-0x60(%rcx,%r14), %rcx
 40632f4:      	nopw	%cs:(%rax,%rax)
 40632fe:      	nop
 4063300:      	movq	0x8(%rbp), %rsi
 4063304:      	leal	0x1(%rax), %edx
 4063307:      	cmpq	%rcx, 0x20(%rsi)
 406330b:      	jne	0x406343b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd0b>
 4063311:      	movl	%edx, %eax
 4063313:      	movl	%edx, -0x40(%r12)
 4063318:      	movq	(%rbp), %rsi
 406331c:      	andq	$-0x8, %rsi
 4063320:      	movq	0x30(%rsi), %rdx
 4063324:      	addq	$0x30, %rsi
 4063328:      	xorl	%ecx, %ecx
 406332a:      	cmpq	%rdx, %rsi
 406332d:      	je	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 406332f:      	movzbl	-0x18(%rdx), %esi
 4063333:      	leal	-0x1e(%rsi), %edi
 4063336:      	cmpb	$0xa, %dil
 406333a:      	ja	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 406333c:      	addl	$-0x1e, %esi
 406333f:      	leaq	-0x25c4ca6(%rip), %rdi  # 0x1a9e6a0 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x2a0>
 4063346:      	movslq	(%rdi,%rsi,4), %rsi
 406334a:      	addq	%rdi, %rsi
 406334d:      	jmpq	*%rsi
 406334f:      	movl	-0x14(%rdx), %ecx
 4063352:      	movl	$0x7ffffff, %edx        # imm = 0x7FFFFFF
 4063357:      	andl	%edx, %ecx
 4063359:      	decl	%ecx
 406335b:      	jmp	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 406335d:      	movl	$0x1, %ecx
 4063362:      	jmp	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 4063364:      	movl	$0x2, %ecx
 4063369:      	jmp	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 406336b:      	movl	0x40(%rdx), %ecx
 406336e:      	jmp	0x406338b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc5b>
 4063370:      	movzwl	-0x16(%rdx), %ecx
 4063374:      	andl	$0x1, %ecx
 4063377:      	jmp	0x4063390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xc60>
 4063379:      	movl	-0x14(%rdx), %edx
 406337c:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4063381:      	andl	%ecx, %edx
 4063383:      	xorl	%ecx, %ecx
 4063385:      	cmpl	$0x3, %edx
 4063388:      	sete	%cl
 406338b:      	incl	%ecx
 406338d:      	nopl	(%rax)
 4063390:      	cmpl	%ecx, %eax
 4063392:      	je	0x406343b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd0b>
 4063398:      	movzbl	(%r14), %ecx
 406339c:      	addl	$-0x1f, %ecx
 406339f:      	leaq	-0x25c4cda(%rip), %rdx  # 0x1a9e6cc <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x2cc>
 40633a6:      	movslq	(%rdx,%rcx,4), %rcx
 40633aa:      	addq	%rdx, %rcx
 40633ad:      	jmpq	*%rcx
 40633af:      	leal	0x1(%rax), %ecx
 40633b2:      	movq	-0x8(%r14), %rdx
 40633b6:      	shlq	$0x5, %rcx
 40633ba:      	movq	(%rdx,%rcx), %rcx
 40633be:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 40633c3:      	leal	-0x1(%rax), %ecx
 40633c6:      	movl	0x58(%r14), %edx
 40633ca:      	shlq	$0x5, %rdx
 40633ce:      	movq	%r14, %rsi
 40633d1:      	subq	%rdx, %rsi
 40633d4:      	addq	$-0x40, %rsi
 40633d8:      	leaq	-0x20(%r14), %rdi
 40633dc:      	subq	%rdx, %rdi
 40633df:      	movl	%ecx, %ecx
 40633e1:      	shlq	$0x5, %rcx
 40633e5:      	addq	%rdi, %rcx
 40633e8:      	testl	%eax, %eax
 40633ea:      	cmoveq	%rsi, %rcx
 40633ee:      	movq	(%rcx), %rcx
 40633f1:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 40633f6:      	testb	$0x1, 0x2(%r14)
 40633fb:      	jne	0x4063425 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xcf5>
 40633fd:      	xorl	%ecx, %ecx
 40633ff:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 4063404:      	movl	%eax, %ecx
 4063406:      	shlq	$0x5, %rcx
 406340a:      	leaq	-0x20(%r14), %rdx
 406340e:      	subq	%rcx, %rdx
 4063411:      	movq	(%rdx), %rcx
 4063414:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 4063419:      	leaq	-0x20(%r14), %rcx
 406341d:      	movq	(%rcx), %rcx
 4063420:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 4063425:      	movl	0x4(%r14), %ecx
 4063429:      	shll	$0x5, %ecx
 406342c:      	movq	%r14, %rdx
 406342f:      	subq	%rcx, %rdx
 4063432:      	movq	0x20(%rdx), %rcx
 4063436:      	jmp	0x4063300 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xbd0>
 406343b:      	cmpl	%eax, -0x20(%r12)
 4063440:      	jne	0x40639ab <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x127b>
 4063446:      	movzbl	(%r14), %eax
 406344a:      	addl	$-0x1f, %eax
 406344d:      	leaq	-0x25c4ce4(%rip), %rcx  # 0x1a9e770 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x370>
 4063454:      	movslq	(%rcx,%rax,4), %rax
 4063458:      	addq	%rcx, %rax
 406345b:      	jmpq	*%rax
 406345d:      	incl	%ebx
 406345f:      	movq	-0x8(%r14), %rax
 4063463:      	shlq	$0x5, %rbx
 4063467:      	movq	(%rax,%rbx), %r12
 406346b:      	movq	%rbp, %r15
 406346e:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063473:      	xorl	%ecx, %ecx
 4063475:      	movq	%r15, 0x50(%rsp)
 406347a:      	jmp	0x406348b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd5b>
 406347c:      	nopl	(%rax)
 4063480:      	cmpl	%ebx, -0x20(%r12)
 4063485:      	je	0x4063139 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa09>
 406348b:      	movq	-0x10(%r12), %rbp
 4063490:      	testb	$0x1, %cl
 4063493:      	je	0x40634c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd90>
 4063495:      	movq	-0x48(%r12), %rcx
 406349a:      	movzbl	(%rcx), %edx
 406349d:      	addl	$-0x1f, %edx
 40634a0:      	leaq	-0x25c4e83(%rip), %rsi  # 0x1a9e624 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x224>
 40634a7:      	movslq	(%rsi,%rdx,4), %rdx
 40634ab:      	addq	%rsi, %rdx
 40634ae:      	jmpq	*%rdx
 40634b0:      	incl	%ebx
 40634b2:      	movq	-0x8(%rcx), %rcx
 40634b6:      	shlq	$0x5, %rbx
 40634ba:      	movq	(%rcx,%rbx), %rbx
 40634be:      	jmp	0x4063530 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe00>
 40634c0:      	andq	$-0x8, %rax
 40634c4:      	movq	0x20(%rax), %rbx
 40634c8:      	jmp	0x4063534 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe04>
 40634ca:      	testl	%ebx, %ebx
 40634cc:      	je	0x406351e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdee>
 40634ce:      	decl	%ebx
 40634d0:      	movl	0x58(%rcx), %edx
 40634d3:      	shlq	$0x5, %rdx
 40634d7:      	subq	%rdx, %rcx
 40634da:      	shlq	$0x5, %rbx
 40634de:      	leaq	-0x20(%rbx,%rcx), %rcx
 40634e3:      	jmp	0x406352d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xdfd>
 40634e5:      	movl	%ebx, %edx
 40634e7:      	shlq	$0x5, %rdx
 40634eb:      	subq	%rdx, %rcx
 40634ee:      	movq	-0x20(%rcx), %rbx
 40634f2:      	jmp	0x4063530 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe00>
 40634f4:      	testb	$0x1, 0x2(%rcx)
 40634f8:      	jne	0x406350f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xddf>
 40634fa:      	xorl	%ebx, %ebx
 40634fc:      	jmp	0x4063530 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe00>
 40634fe:      	xorl	%edx, %edx
 4063500:      	testl	%ebx, %ebx
 4063502:      	setne	%dl
 4063505:      	shll	$0x5, %edx
 4063508:      	movq	-0x60(%rdx,%rcx), %rbx
 406350d:      	jmp	0x4063530 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe00>
 406350f:      	movl	0x4(%rcx), %edx
 4063512:      	shll	$0x5, %edx
 4063515:      	subq	%rdx, %rcx
 4063518:      	movq	0x20(%rcx), %rbx
 406351c:      	jmp	0x4063530 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe00>
 406351e:      	movl	0x58(%rcx), %edx
 4063521:      	shlq	$0x5, %rdx
 4063525:      	negq	%rdx
 4063528:      	leaq	-0x40(%rcx,%rdx), %rcx
 406352d:      	movq	(%rcx), %rbx
 4063530:      	andq	$-0x8, %rax
 4063534:      	movq	0x8(%rax), %r13
 4063538:      	movq	0x10(%r13), %rax
 406353c:      	movl	0x38(%rax), %ecx
 406353f:      	testl	%ecx, %ecx
 4063541:      	je	0x40635ac <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe7c>
 4063543:      	movq	0x28(%rax), %rax
 4063547:      	movl	%ebx, %esi
 4063549:      	shrl	$0x4, %esi
 406354c:      	movl	%ebx, %edx
 406354e:      	shrl	$0x9, %edx
 4063551:      	xorl	%esi, %edx
 4063553:      	decl	%ecx
 4063555:      	andl	%ecx, %edx
 4063557:      	movl	%edx, %esi
 4063559:      	shll	$0x4, %esi
 406355c:      	movq	(%rax,%rsi), %rdi
 4063560:      	cmpq	%rdi, %rbx
 4063563:      	jne	0x40638ad <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x117d>
 4063569:      	shlq	$0x4, %rdx
 406356d:      	movq	0x8(%rax,%rdx), %rax
 4063572:      	testq	%rax, %rax
 4063575:      	je	0x40635ac <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe7c>
 4063577:      	cmpq	%r13, %rax
 406357a:      	je	0x40635ac <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe7c>
 406357c:      	nopl	(%rax)
 4063580:      	movq	%rax, %r14
 4063583:      	movq	0x8(%rax), %rsi
 4063587:      	movq	%r13, %rdi
 406358a:      	callq	0x3361660 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 406358f:      	testb	%al, %al
 4063591:      	je	0x406359c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe6c>
 4063593:      	movq	0x8(%r14), %rax
 4063597:      	cmpq	%r13, %rax
 406359a:      	jne	0x4063580 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe50>
 406359c:      	movq	(%r14), %rax
 406359f:      	andq	$-0x8, %rax
 40635a3:      	cmpq	%rax, %rbx
 40635a6:      	je	0x40636c4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf94>
 40635ac:      	movq	%rbp, 0x38(%rsp)
 40635b1:      	movq	0x50(%r13), %rax
 40635b5:      	leaq	0x48(%r13), %r14
 40635b9:      	movq	%r14, %rbp
 40635bc:      	testq	%rax, %rax
 40635bf:      	je	0x40635f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xec6>
 40635c1:      	movq	%r14, %rbp
 40635c4:      	nopw	%cs:(%rax,%rax)
 40635ce:      	nop
 40635d0:      	xorl	%ecx, %ecx
 40635d2:      	cmpq	%rbx, 0x20(%rax)
 40635d6:      	setb	%cl
 40635d9:      	cmovaeq	%rax, %rbp
 40635dd:      	movq	0x10(%rax,%rcx,8), %rax
 40635e2:      	testq	%rax, %rax
 40635e5:      	jne	0x40635d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xea0>
 40635e7:      	cmpq	%r14, %rbp
 40635ea:      	je	0x40635f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xec6>
 40635ec:      	cmpq	0x20(%rbp), %rbx
 40635f0:      	jae	0x40636bb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf8b>
 40635f6:      	movq	%rbp, %r15
 40635f9:      	leaq	0x40(%r13), %r12
 40635fd:      	movl	$0x30, %edi
 4063602:      	callq	0x828a6b0 <_Znwm@plt>
 4063607:      	movq	%rax, %rbp
 406360a:      	addq	$0x20, %rax
 406360e:      	movq	%rbx, 0x20(%rbp)
 4063612:      	movq	$0x0, 0x28(%rbp)
 406361a:      	movq	%r12, %rdi
 406361d:      	movq	%r15, %rsi
 4063620:      	movq	%rax, %r15
 4063623:      	movq	%rax, %rdx
 4063626:      	callq	0x33691a0 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 406362b:      	testq	%rdx, %rdx
 406362e:      	je	0x4063660 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf30>
 4063630:      	testq	%rax, %rax
 4063633:      	setne	%al
 4063636:      	cmpq	%r14, %rdx
 4063639:      	sete	%cl
 406363c:      	orb	%al, %cl
 406363e:      	movb	$0x1, %al
 4063640:      	jne	0x406364c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf1c>
 4063642:      	movq	(%r15), %rax
 4063645:      	cmpq	0x20(%rdx), %rax
 4063649:      	setb	%al
 406364c:      	movzbl	%al, %edi
 406364f:      	movq	%rbp, %rsi
 4063652:      	movq	%r14, %rcx
 4063655:      	callq	0x828a7e0 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 406365a:      	incq	0x68(%r13)
 406365e:      	jmp	0x4063686 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf56>
 4063660:      	movq	%rax, %r14
 4063663:      	movq	0x28(%rbp), %rdi
 4063667:      	testq	%rdi, %rdi
 406366a:      	je	0x4063676 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf46>
 406366c:      	movl	$0x10, %esi
 4063671:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4063676:      	movl	$0x30, %esi
 406367b:      	movq	%rbp, %rdi
 406367e:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4063683:      	movq	%r14, %rbp
 4063686:      	movq	(%rsp), %r12
 406368a:      	movq	0x50(%rsp), %r15
 406368f:      	movl	$0x10, %edi
 4063694:      	callq	0x828a6b0 <_Znwm@plt>
 4063699:      	andq	$-0x5, %rbx
 406369d:      	movq	%rbx, (%rax)
 40636a0:      	movq	%r13, 0x8(%rax)
 40636a4:      	movq	0x28(%rbp), %rdi
 40636a8:      	movq	%rax, 0x28(%rbp)
 40636ac:      	testq	%rdi, %rdi
 40636af:      	je	0x40636bb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xf8b>
 40636b1:      	movl	$0x10, %esi
 40636b6:      	callq	0x828a6f0 <_ZdlPvm@plt>
 40636bb:      	movq	0x28(%rbp), %r14
 40636bf:      	movq	0x38(%rsp), %rbp
 40636c4:      	movq	-0x38(%r12), %rax
 40636c9:      	movq	%r14, 0x60(%rsp)
 40636ce:      	movq	%rax, 0x68(%rsp)
 40636d3:      	leaq	0x60(%rsp), %rdi
 40636d8:      	callq	*%rbp
 40636da:      	testb	%al, %al
 40636dc:      	jne	0x4063139 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa09>
 40636e2:      	movq	-0x50(%r12), %rax
 40636e7:      	testb	$0x6, %al
 40636e9:      	sete	%cl
 40636ec:      	je	0x4063720 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xff0>
 40636ee:      	andq	$-0x7, %rax
 40636f2:      	orq	$0x4, %rax
 40636f6:      	movq	%rax, -0x50(%r12)
 40636fb:      	movl	-0x40(%r12), %ebx
 4063700:      	movl	-0x30(%r12), %edx
 4063705:      	andl	$0x6, %edx
 4063708:      	cmpl	$0x4, %edx
 406370b:      	jne	0x406348b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd5b>
 4063711:      	jmp	0x4063139 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa09>
 4063716:      	nopw	%cs:(%rax,%rax)
 4063720:      	movq	%rax, %rdx
 4063723:      	andq	$-0x8, %rdx
 4063727:      	movq	-0x48(%r12), %rsi
 406372c:      	movl	-0x40(%r12), %r9d
 4063731:      	leaq	-0x20(%rsi), %rdi
 4063735:      	incl	%r9d
 4063738:      	jmp	0x4063762 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1032>
 406373a:      	xorl	%r8d, %r8d
 406373d:      	testl	%ebx, %ebx
 406373f:      	setne	%r8b
 4063743:      	shll	$0x5, %r8d
 4063747:      	movq	-0x60(%r8,%rsi), %r8
 406374c:      	nopl	(%rax)
 4063750:      	movq	0x8(%rdx), %r10
 4063754:      	leal	0x1(%rbx), %r9d
 4063758:      	cmpq	%r8, 0x20(%r10)
 406375c:      	jne	0x4063480 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd50>
 4063762:      	movl	%r9d, %ebx
 4063765:      	movl	%r9d, -0x40(%r12)
 406376a:      	movq	(%rdx), %r10
 406376d:      	andq	$-0x8, %r10
 4063771:      	movq	0x30(%r10), %r9
 4063775:      	addq	$0x30, %r10
 4063779:      	xorl	%r8d, %r8d
 406377c:      	cmpq	%r9, %r10
 406377f:      	je	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 4063781:      	movzbl	-0x18(%r9), %r10d
 4063786:      	leal	-0x1e(%r10), %r11d
 406378a:      	cmpb	$0xa, %r11b
 406378e:      	ja	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 4063790:      	addl	$-0x1e, %r10d
 4063794:      	leaq	-0x25c514f(%rip), %r11  # 0x1a9e64c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x24c>
 406379b:      	movslq	(%r11,%r10,4), %r10
 406379f:      	addq	%r11, %r10
 40637a2:      	jmpq	*%r10
 40637a5:      	movl	-0x14(%r9), %r8d
 40637a9:      	movl	$0x7ffffff, %r9d        # imm = 0x7FFFFFF
 40637af:      	andl	%r9d, %r8d
 40637b2:      	decl	%r8d
 40637b5:      	jmp	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 40637b7:      	movl	$0x1, %r8d
 40637bd:      	jmp	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 40637bf:      	movl	$0x2, %r8d
 40637c5:      	jmp	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 40637c7:      	movl	0x40(%r9), %r8d
 40637cb:      	jmp	0x40637f0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10c0>
 40637cd:      	movzwl	-0x16(%r9), %r8d
 40637d2:      	andl	$0x1, %r8d
 40637d6:      	jmp	0x4063800 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x10d0>
 40637d8:      	movl	-0x14(%r9), %r9d
 40637dc:      	movl	$0x7ffffff, %r8d        # imm = 0x7FFFFFF
 40637e2:      	andl	%r8d, %r9d
 40637e5:      	xorl	%r8d, %r8d
 40637e8:      	cmpl	$0x3, %r9d
 40637ec:      	sete	%r8b
 40637f0:      	incl	%r8d
 40637f3:      	nopw	%cs:(%rax,%rax)
 40637fd:      	nopl	(%rax)
 4063800:      	cmpl	%r8d, %ebx
 4063803:      	je	0x4063480 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd50>
 4063809:      	movzbl	(%rsi), %r8d
 406380d:      	addl	$-0x1f, %r8d
 4063811:      	leaq	-0x25c51a0(%rip), %r9   # 0x1a9e678 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x278>
 4063818:      	movslq	(%r9,%r8,4), %r8
 406381c:      	addq	%r9, %r8
 406381f:      	jmpq	*%r8
 4063822:      	leal	0x1(%rbx), %r8d
 4063826:      	movq	-0x8(%rsi), %r9
 406382a:      	shlq	$0x5, %r8
 406382e:      	movq	(%r9,%r8), %r8
 4063832:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 4063837:      	leal	-0x1(%rbx), %r8d
 406383b:      	movl	0x58(%rsi), %r9d
 406383f:      	shlq	$0x5, %r9
 4063843:      	movq	%rsi, %r10
 4063846:      	subq	%r9, %r10
 4063849:      	addq	$-0x40, %r10
 406384d:      	movq	%rdi, %r11
 4063850:      	subq	%r9, %r11
 4063853:      	movl	%r8d, %r8d
 4063856:      	shlq	$0x5, %r8
 406385a:      	addq	%r11, %r8
 406385d:      	testl	%ebx, %ebx
 406385f:      	cmoveq	%r10, %r8
 4063863:      	movq	(%r8), %r8
 4063866:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 406386b:      	testb	$0x1, 0x2(%rsi)
 406386f:      	jne	0x4063896 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1166>
 4063871:      	xorl	%r8d, %r8d
 4063874:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 4063879:      	movl	%ebx, %r8d
 406387c:      	shlq	$0x5, %r8
 4063880:      	movq	%rdi, %r9
 4063883:      	subq	%r8, %r9
 4063886:      	movq	(%r9), %r8
 4063889:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 406388e:      	movq	(%rdi), %r8
 4063891:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 4063896:      	movl	0x4(%rsi), %r8d
 406389a:      	shll	$0x5, %r8d
 406389e:      	movq	%rsi, %r9
 40638a1:      	subq	%r8, %r9
 40638a4:      	movq	0x20(%r9), %r8
 40638a8:      	jmp	0x4063750 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1020>
 40638ad:      	movl	$0x1, %esi
 40638b2:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 40638b9:      	je	0x40635ac <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe7c>
 40638bf:      	addl	%esi, %edx
 40638c1:      	incl	%esi
 40638c3:      	andl	%ecx, %edx
 40638c5:      	movq	%rdx, %rdi
 40638c8:      	shlq	$0x4, %rdi
 40638cc:      	movq	(%rax,%rdi), %rdi
 40638d0:      	cmpq	%rdi, %rbx
 40638d3:      	je	0x4063569 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xe39>
 40638d9:      	jmp	0x40638b2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1182>
 40638db:      	movq	0x28(%rbp), %rdi
 40638df:      	testq	%rdi, %rdi
 40638e2:      	je	0x40638ee <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11be>
 40638e4:      	movl	$0x10, %esi
 40638e9:      	callq	0x828a6f0 <_ZdlPvm@plt>
 40638ee:      	movl	$0x30, %esi
 40638f3:      	movq	%rbp, %rdi
 40638f6:      	callq	0x828a6f0 <_ZdlPvm@plt>
 40638fb:      	movq	%rbx, %rbp
 40638fe:      	movq	0x8(%rsp), %rbx
 4063903:      	movl	$0x10, %edi
 4063908:      	callq	0x828a6b0 <_Znwm@plt>
 406390d:      	andq	$-0x5, %r12
 4063911:      	movq	%r12, (%rax)
 4063914:      	movq	%r13, 0x8(%rax)
 4063918:      	movq	0x28(%rbp), %rdi
 406391c:      	movq	%rax, 0x28(%rbp)
 4063920:      	testq	%rdi, %rdi
 4063923:      	je	0x406392f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x11ff>
 4063925:      	movl	$0x10, %esi
 406392a:      	callq	0x828a6f0 <_ZdlPvm@plt>
 406392f:      	movq	0x28(%rbp), %rbp
 4063933:      	movq	0x20(%rsp), %rcx
 4063938:      	movq	0x8(%rcx), %rax
 406393c:      	movl	0x18(%rcx), %ecx
 406393f:      	testq	%rcx, %rcx
 4063942:      	je	0x40640dd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19ad>
 4063948:      	movl	%ebp, %edx
 406394a:      	shrl	$0x4, %edx
 406394d:      	movl	%ebp, %esi
 406394f:      	shrl	$0x9, %esi
 4063952:      	xorl	%edx, %esi
 4063954:      	movl	%ebx, %edx
 4063956:      	shrl	$0x4, %edx
 4063959:      	movl	%ebx, %edi
 406395b:      	shrl	$0x9, %edi
 406395e:      	xorl	%edx, %edi
 4063960:      	shlq	$0x20, %rsi
 4063964:      	orq	%rsi, %rdi
 4063967:      	movabsq	$-0x40a7b892e31b1a47, %rdx # imm = 0xBF58476D1CE4E5B9
 4063971:      	imulq	%rdx, %rdi
 4063975:      	movq	%rdi, %rdx
 4063978:      	shrq	$0x1f, %rdx
 406397c:      	xorl	%edi, %edx
 406397e:      	leal	-0x1(%rcx), %esi
 4063981:      	andl	%esi, %edx
 4063983:      	leaq	(%rdx,%rdx,2), %rdi
 4063987:      	movq	(%rax,%rdi,8), %r9
 406398b:      	movq	0x8(%rax,%rdi,8), %r8
 4063990:      	cmpq	%r9, %rbp
 4063993:      	jne	0x40640a3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1973>
 4063999:      	cmpq	%r8, %rbx
 406399c:      	jne	0x40640a3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1973>
 40639a2:      	leaq	(%rax,%rdi,8), %r10
 40639a6:      	jmp	0x40640e5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19b5>
 40639ab:      	movb	$0x1, %cl
 40639ad:      	movq	%r14, 0x30(%rsp)
 40639b2:      	movq	%rbp, 0x48(%rsp)
 40639b7:      	jmp	0x40639cb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x129b>
 40639b9:      	nopl	(%rax)
 40639c0:      	cmpl	%eax, -0x20(%r12)
 40639c5:      	je	0x4063446 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd16>
 40639cb:      	movq	-0x10(%r12), %rdi
 40639d0:      	testb	$0x1, %cl
 40639d3:      	movq	%rdi, 0x38(%rsp)
 40639d8:      	je	0x4063a10 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x12e0>
 40639da:      	movq	-0x48(%r12), %rcx
 40639df:      	movzbl	(%rcx), %edx
 40639e2:      	addl	$-0x1f, %edx
 40639e5:      	leaq	-0x25c52f8(%rip), %rsi  # 0x1a9e6f4 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x2f4>
 40639ec:      	movslq	(%rsi,%rdx,4), %rdx
 40639f0:      	addq	%rsi, %rdx
 40639f3:      	jmpq	*%rdx
 40639f5:      	incl	%eax
 40639f7:      	movq	-0x8(%rcx), %rcx
 40639fb:      	shlq	$0x5, %rax
 40639ff:      	movq	(%rcx,%rax), %r14
 4063a03:      	jmp	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1360>
 4063a08:      	nopl	(%rax,%rax)
 4063a10:      	andq	$-0x8, %r15
 4063a14:      	movq	0x20(%r15), %r14
 4063a18:      	jmp	0x4063a94 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1364>
 4063a1a:      	testl	%eax, %eax
 4063a1c:      	je	0x4063a6f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x133f>
 4063a1e:      	decl	%eax
 4063a20:      	movl	0x58(%rcx), %edx
 4063a23:      	shlq	$0x5, %rdx
 4063a27:      	subq	%rdx, %rcx
 4063a2a:      	shlq	$0x5, %rax
 4063a2e:      	leaq	-0x20(%rax,%rcx), %rax
 4063a33:      	jmp	0x4063a7e <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x134e>
 4063a35:      	movl	%eax, %eax
 4063a37:      	shlq	$0x5, %rax
 4063a3b:      	subq	%rax, %rcx
 4063a3e:      	movq	-0x20(%rcx), %r14
 4063a42:      	jmp	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1360>
 4063a44:      	testb	$0x1, 0x2(%rcx)
 4063a48:      	jne	0x4063a60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1330>
 4063a4a:      	xorl	%r14d, %r14d
 4063a4d:      	jmp	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1360>
 4063a4f:      	xorl	%edx, %edx
 4063a51:      	testl	%eax, %eax
 4063a53:      	setne	%dl
 4063a56:      	shll	$0x5, %edx
 4063a59:      	movq	-0x60(%rdx,%rcx), %r14
 4063a5e:      	jmp	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1360>
 4063a60:      	movl	0x4(%rcx), %eax
 4063a63:      	shll	$0x5, %eax
 4063a66:      	subq	%rax, %rcx
 4063a69:      	movq	0x20(%rcx), %r14
 4063a6d:      	jmp	0x4063a90 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1360>
 4063a6f:      	movl	0x58(%rcx), %eax
 4063a72:      	shlq	$0x5, %rax
 4063a76:      	negq	%rax
 4063a79:      	leaq	-0x40(%rcx,%rax), %rax
 4063a7e:      	movq	(%rax), %r14
 4063a81:      	nopw	%cs:(%rax,%rax)
 4063a8b:      	nopl	(%rax,%rax)
 4063a90:      	andq	$-0x8, %r15
 4063a94:      	movq	0x8(%r15), %r13
 4063a98:      	movq	0x10(%r13), %rax
 4063a9c:      	movl	0x38(%rax), %ecx
 4063a9f:      	testl	%ecx, %ecx
 4063aa1:      	je	0x4063b0c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13dc>
 4063aa3:      	movq	0x28(%rax), %rax
 4063aa7:      	movl	%r14d, %esi
 4063aaa:      	shrl	$0x4, %esi
 4063aad:      	movl	%r14d, %edx
 4063ab0:      	shrl	$0x9, %edx
 4063ab3:      	xorl	%esi, %edx
 4063ab5:      	decl	%ecx
 4063ab7:      	andl	%ecx, %edx
 4063ab9:      	movl	%edx, %esi
 4063abb:      	shll	$0x4, %esi
 4063abe:      	movq	(%rax,%rsi), %rdi
 4063ac2:      	cmpq	%rdi, %r14
 4063ac5:      	jne	0x4063e0d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16dd>
 4063acb:      	shlq	$0x4, %rdx
 4063acf:      	movq	0x8(%rax,%rdx), %rax
 4063ad4:      	testq	%rax, %rax
 4063ad7:      	je	0x4063b0c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13dc>
 4063ad9:      	cmpq	%r13, %rax
 4063adc:      	je	0x4063b0c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13dc>
 4063ade:      	nop
 4063ae0:      	movq	%rax, %r15
 4063ae3:      	movq	0x8(%rax), %rsi
 4063ae7:      	movq	%r13, %rdi
 4063aea:      	callq	0x3361660 <_ZNK4llvm10RegionBaseINS_12RegionTraitsINS_8FunctionEEEE8containsEPKNS_6RegionE>
 4063aef:      	testb	%al, %al
 4063af1:      	je	0x4063afc <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13cc>
 4063af3:      	movq	0x8(%r15), %rax
 4063af7:      	cmpq	%r13, %rax
 4063afa:      	jne	0x4063ae0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13b0>
 4063afc:      	movq	(%r15), %rax
 4063aff:      	andq	$-0x8, %rax
 4063b03:      	cmpq	%rax, %r14
 4063b06:      	je	0x4063c1f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14ef>
 4063b0c:      	movq	0x50(%r13), %rax
 4063b10:      	leaq	0x48(%r13), %rdx
 4063b14:      	movq	%rdx, %rbp
 4063b17:      	testq	%rax, %rax
 4063b1a:      	je	0x4063b46 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1416>
 4063b1c:      	movq	%rdx, %rbp
 4063b1f:      	nop
 4063b20:      	xorl	%ecx, %ecx
 4063b22:      	cmpq	%r14, 0x20(%rax)
 4063b26:      	setb	%cl
 4063b29:      	cmovaeq	%rax, %rbp
 4063b2d:      	movq	0x10(%rax,%rcx,8), %rax
 4063b32:      	testq	%rax, %rax
 4063b35:      	jne	0x4063b20 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13f0>
 4063b37:      	cmpq	%rdx, %rbp
 4063b3a:      	je	0x4063b46 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1416>
 4063b3c:      	cmpq	0x20(%rbp), %r14
 4063b40:      	jae	0x4063c16 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14e6>
 4063b46:      	movq	%rbp, %r15
 4063b49:      	leaq	0x40(%r13), %r12
 4063b4d:      	movl	$0x30, %edi
 4063b52:      	callq	0x828a6b0 <_Znwm@plt>
 4063b57:      	movq	%rax, %rbp
 4063b5a:      	addq	$0x20, %rax
 4063b5e:      	movq	%r14, 0x20(%rbp)
 4063b62:      	movq	$0x0, 0x28(%rbp)
 4063b6a:      	movq	%r12, %rdi
 4063b6d:      	movq	%r15, %rsi
 4063b70:      	movq	%rax, %r15
 4063b73:      	movq	%rax, %rdx
 4063b76:      	callq	0x33691a0 <_ZNSt8_Rb_treeIPN4llvm10BasicBlockESt4pairIKS2_St10unique_ptrINS0_10RegionNodeESt14default_deleteIS6_EEESt10_Select1stISA_ESt4lessIS2_ESaISA_EE29_M_get_insert_hint_unique_posESt23_Rb_tree_const_iteratorISA_ERS4_>
 4063b7b:      	testq	%rdx, %rdx
 4063b7e:      	je	0x4063bc0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1490>
 4063b80:      	testq	%rax, %rax
 4063b83:      	setne	%al
 4063b86:      	leaq	0x48(%r13), %rcx
 4063b8a:      	cmpq	%rcx, %rdx
 4063b8d:      	sete	%sil
 4063b91:      	orb	%al, %sil
 4063b94:      	movb	$0x1, %al
 4063b96:      	jne	0x4063ba2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1472>
 4063b98:      	movq	(%r15), %rax
 4063b9b:      	cmpq	0x20(%rdx), %rax
 4063b9f:      	setb	%al
 4063ba2:      	movzbl	%al, %edi
 4063ba5:      	movq	%rbp, %rsi
 4063ba8:      	callq	0x828a7e0 <_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_@plt>
 4063bad:      	incq	0x68(%r13)
 4063bb1:      	jmp	0x4063be6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14b6>
 4063bb3:      	nopw	%cs:(%rax,%rax)
 4063bbd:      	nopl	(%rax)
 4063bc0:      	movq	%rax, %r15
 4063bc3:      	movq	0x28(%rbp), %rdi
 4063bc7:      	testq	%rdi, %rdi
 4063bca:      	je	0x4063bd6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14a6>
 4063bcc:      	movl	$0x10, %esi
 4063bd1:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4063bd6:      	movl	$0x30, %esi
 4063bdb:      	movq	%rbp, %rdi
 4063bde:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4063be3:      	movq	%r15, %rbp
 4063be6:      	movq	(%rsp), %r12
 4063bea:      	movl	$0x10, %edi
 4063bef:      	callq	0x828a6b0 <_Znwm@plt>
 4063bf4:      	andq	$-0x5, %r14
 4063bf8:      	movq	%r14, (%rax)
 4063bfb:      	movq	%r13, 0x8(%rax)
 4063bff:      	movq	0x28(%rbp), %rdi
 4063c03:      	movq	%rax, 0x28(%rbp)
 4063c07:      	testq	%rdi, %rdi
 4063c0a:      	je	0x4063c16 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x14e6>
 4063c0c:      	movl	$0x10, %esi
 4063c11:      	callq	0x828a6f0 <_ZdlPvm@plt>
 4063c16:      	movq	0x28(%rbp), %r15
 4063c1a:      	movq	0x48(%rsp), %rbp
 4063c1f:      	movq	-0x38(%r12), %rax
 4063c24:      	movq	%r15, 0x60(%rsp)
 4063c29:      	movq	%rax, 0x68(%rsp)
 4063c2e:      	leaq	0x60(%rsp), %rdi
 4063c33:      	callq	*0x38(%rsp)
 4063c37:      	testb	%al, %al
 4063c39:      	movq	0x30(%rsp), %r14
 4063c3e:      	jne	0x4063446 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd16>
 4063c44:      	movq	-0x50(%r12), %r15
 4063c49:      	testb	$0x6, %r15b
 4063c4d:      	sete	%cl
 4063c50:      	je	0x4063c80 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1550>
 4063c52:      	andq	$-0x7, %r15
 4063c56:      	orq	$0x4, %r15
 4063c5a:      	movq	%r15, -0x50(%r12)
 4063c5f:      	movl	-0x40(%r12), %eax
 4063c64:      	movl	-0x30(%r12), %edx
 4063c69:      	andl	$0x6, %edx
 4063c6c:      	cmpl	$0x4, %edx
 4063c6f:      	jne	0x40639cb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x129b>
 4063c75:      	jmp	0x4063446 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xd16>
 4063c7a:      	nopw	(%rax,%rax)
 4063c80:      	movq	%r15, %rdx
 4063c83:      	andq	$-0x8, %rdx
 4063c87:      	movq	-0x48(%r12), %rsi
 4063c8c:      	movl	-0x40(%r12), %r9d
 4063c91:      	leaq	-0x20(%rsi), %rdi
 4063c95:      	incl	%r9d
 4063c98:      	jmp	0x4063cc2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1592>
 4063c9a:      	xorl	%r8d, %r8d
 4063c9d:      	testl	%eax, %eax
 4063c9f:      	setne	%r8b
 4063ca3:      	shll	$0x5, %r8d
 4063ca7:      	movq	-0x60(%r8,%rsi), %r8
 4063cac:      	nopl	(%rax)
 4063cb0:      	movq	0x8(%rdx), %r10
 4063cb4:      	leal	0x1(%rax), %r9d
 4063cb8:      	cmpq	%r8, 0x20(%r10)
 4063cbc:      	jne	0x40639c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1290>
 4063cc2:      	movl	%r9d, %eax
 4063cc5:      	movl	%r9d, -0x40(%r12)
 4063cca:      	movq	(%rdx), %r10
 4063ccd:      	andq	$-0x8, %r10
 4063cd1:      	movq	0x30(%r10), %r9
 4063cd5:      	addq	$0x30, %r10
 4063cd9:      	xorl	%r8d, %r8d
 4063cdc:      	cmpq	%r9, %r10
 4063cdf:      	je	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063ce1:      	movzbl	-0x18(%r9), %r10d
 4063ce6:      	leal	-0x1e(%r10), %r11d
 4063cea:      	cmpb	$0xa, %r11b
 4063cee:      	ja	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063cf0:      	addl	$-0x1e, %r10d
 4063cf4:      	leaq	-0x25c55df(%rip), %r11  # 0x1a9e71c <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x31c>
 4063cfb:      	movslq	(%r11,%r10,4), %r10
 4063cff:      	addq	%r11, %r10
 4063d02:      	jmpq	*%r10
 4063d05:      	movl	-0x14(%r9), %r8d
 4063d09:      	movl	$0x7ffffff, %r9d        # imm = 0x7FFFFFF
 4063d0f:      	andl	%r9d, %r8d
 4063d12:      	decl	%r8d
 4063d15:      	jmp	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063d17:      	movl	$0x1, %r8d
 4063d1d:      	jmp	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063d1f:      	movl	$0x2, %r8d
 4063d25:      	jmp	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063d27:      	movl	0x40(%r9), %r8d
 4063d2b:      	jmp	0x4063d50 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1620>
 4063d2d:      	movzwl	-0x16(%r9), %r8d
 4063d32:      	andl	$0x1, %r8d
 4063d36:      	jmp	0x4063d60 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1630>
 4063d38:      	movl	-0x14(%r9), %r9d
 4063d3c:      	movl	$0x7ffffff, %r8d        # imm = 0x7FFFFFF
 4063d42:      	andl	%r8d, %r9d
 4063d45:      	xorl	%r8d, %r8d
 4063d48:      	cmpl	$0x3, %r9d
 4063d4c:      	sete	%r8b
 4063d50:      	incl	%r8d
 4063d53:      	nopw	%cs:(%rax,%rax)
 4063d5d:      	nopl	(%rax)
 4063d60:      	cmpl	%r8d, %eax
 4063d63:      	je	0x40639c0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1290>
 4063d69:      	movzbl	(%rsi), %r8d
 4063d6d:      	addl	$-0x1f, %r8d
 4063d71:      	leaq	-0x25c5630(%rip), %r9   # 0x1a9e748 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x348>
 4063d78:      	movslq	(%r9,%r8,4), %r8
 4063d7c:      	addq	%r9, %r8
 4063d7f:      	jmpq	*%r8
 4063d82:      	leal	0x1(%rax), %r8d
 4063d86:      	movq	-0x8(%rsi), %r9
 4063d8a:      	shlq	$0x5, %r8
 4063d8e:      	movq	(%r9,%r8), %r8
 4063d92:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063d97:      	leal	-0x1(%rax), %r8d
 4063d9b:      	movl	0x58(%rsi), %r9d
 4063d9f:      	shlq	$0x5, %r9
 4063da3:      	movq	%rsi, %r10
 4063da6:      	subq	%r9, %r10
 4063da9:      	addq	$-0x40, %r10
 4063dad:      	movq	%rdi, %r11
 4063db0:      	subq	%r9, %r11
 4063db3:      	movl	%r8d, %r8d
 4063db6:      	shlq	$0x5, %r8
 4063dba:      	addq	%r11, %r8
 4063dbd:      	testl	%eax, %eax
 4063dbf:      	cmoveq	%r10, %r8
 4063dc3:      	movq	(%r8), %r8
 4063dc6:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063dcb:      	testb	$0x1, 0x2(%rsi)
 4063dcf:      	jne	0x4063df6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16c6>
 4063dd1:      	xorl	%r8d, %r8d
 4063dd4:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063dd9:      	movl	%eax, %r8d
 4063ddc:      	shlq	$0x5, %r8
 4063de0:      	movq	%rdi, %r9
 4063de3:      	subq	%r8, %r9
 4063de6:      	movq	(%r9), %r8
 4063de9:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063dee:      	movq	(%rdi), %r8
 4063df1:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063df6:      	movl	0x4(%rsi), %r8d
 4063dfa:      	shll	$0x5, %r8d
 4063dfe:      	movq	%rsi, %r9
 4063e01:      	subq	%r8, %r9
 4063e04:      	movq	0x20(%r9), %r8
 4063e08:      	jmp	0x4063cb0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1580>
 4063e0d:      	movl	$0x1, %esi
 4063e12:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4063e19:      	je	0x4063b0c <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x13dc>
 4063e1f:      	addl	%esi, %edx
 4063e21:      	incl	%esi
 4063e23:      	andl	%ecx, %edx
 4063e25:      	movq	%rdx, %rdi
 4063e28:      	shlq	$0x4, %rdi
 4063e2c:      	movq	(%rax,%rdi), %rdi
 4063e30:      	cmpq	%rdi, %r14
 4063e33:      	je	0x4063acb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x139b>
 4063e39:      	jmp	0x4063e12 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x16e2>
 4063e3b:      	movl	-0x14(%rax), %esi
 4063e3e:      	movl	$0x7ffffff, %eax        # imm = 0x7FFFFFF
 4063e43:      	andl	%eax, %esi
 4063e45:      	decl	%esi
 4063e47:      	jmp	0x40629d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063e4c:      	movl	$0x1, %esi
 4063e51:      	jmp	0x40629d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063e56:      	movl	$0x2, %esi
 4063e5b:      	jmp	0x40629d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063e60:      	movl	0x40(%rax), %esi
 4063e63:      	jmp	0x4063e84 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1754>
 4063e65:      	movzwl	-0x16(%rax), %esi
 4063e69:      	andl	$0x1, %esi
 4063e6c:      	jmp	0x40629d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063e71:      	movl	-0x14(%rax), %eax
 4063e74:      	movl	$0x7ffffff, %ecx        # imm = 0x7FFFFFF
 4063e79:      	andl	%ecx, %eax
 4063e7b:      	xorl	%esi, %esi
 4063e7d:      	cmpl	$0x3, %eax
 4063e80:      	sete	%sil
 4063e84:      	incl	%esi
 4063e86:      	jmp	0x40629d2 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a2>
 4063e8b:      	xorl	%eax, %eax
 4063e8d:      	testl	%ebx, %ebx
 4063e8f:      	setne	%al
 4063e92:      	shll	$0x5, %eax
 4063e95:      	movq	-0x60(%rax,%r14), %r12
 4063e9a:      	movq	%rbp, %r15
 4063e9d:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063ea2:      	testl	%ebx, %ebx
 4063ea4:      	je	0x4063f7a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x184a>
 4063eaa:      	decl	%ebx
 4063eac:      	movl	0x58(%r14), %eax
 4063eb0:      	shlq	$0x5, %rax
 4063eb4:      	movq	0x28(%rsp), %rcx
 4063eb9:      	subq	%rax, %rcx
 4063ebc:      	shlq	$0x5, %rbx
 4063ec0:      	addq	%rcx, %rbx
 4063ec3:      	jmp	0x4063f8a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x185a>
 4063ec8:      	testb	$0x1, 0x2(%r14)
 4063ecd:      	jne	0x4063f64 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1834>
 4063ed3:      	movq	%rbp, %r15
 4063ed6:      	xorl	%r12d, %r12d
 4063ed9:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063ede:      	shlq	$0x5, %rbx
 4063ee2:      	movq	0x28(%rsp), %rax
 4063ee7:      	subq	%rbx, %rax
 4063eea:      	jmp	0x4063ef1 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x17c1>
 4063eec:      	movq	0x28(%rsp), %rax
 4063ef1:      	movq	(%rax), %r12
 4063ef4:      	movq	%rbp, %r15
 4063ef7:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063efc:      	movzwl	-0x16(%rax), %r8d
 4063f01:      	andl	$0x1, %r8d
 4063f05:      	testl	%r8d, %r8d
 4063f08:      	jne	0x406282f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xff>
 4063f0e:      	jmp	0x4062990 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x260>
 4063f13:      	leaq	-0x14(%rax), %r9
 4063f17:      	movl	-0x14(%rax), %r8d
 4063f1b:      	movl	$0x7ffffff, %esi        # imm = 0x7FFFFFF
 4063f20:      	andl	%esi, %r8d
 4063f23:      	xorl	%r15d, %r15d
 4063f26:      	cmpl	$0x3, %r8d
 4063f2a:      	sete	%r15b
 4063f2e:      	incl	%r15d
 4063f31:      	movq	0x8(%r11), %r8
 4063f35:      	movq	0x20(%r8), %r10
 4063f39:      	leaq	-0x16(%rax), %rsi
 4063f3d:      	movq	%rsi, 0x48(%rsp)
 4063f42:      	leaq	-0x38(%rax), %rsi
 4063f46:      	leaq	-0x20(%rax), %r8
 4063f4a:      	movq	%r8, 0x30(%rsp)
 4063f4f:      	leaq	0x40(%rax), %r8
 4063f53:      	movq	%r8, 0x10(%rsp)
 4063f58:      	movq	-0x38(%rax), %r11
 4063f5c:      	movl	%r15d, %r8d
 4063f5f:      	jmp	0x4063fe4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b4>
 4063f64:      	movl	0x4(%r14), %eax
 4063f68:      	shll	$0x5, %eax
 4063f6b:      	subq	%rax, %r14
 4063f6e:      	movq	0x20(%r14), %r12
 4063f72:      	movq	%rbp, %r15
 4063f75:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063f7a:      	movl	0x58(%r14), %eax
 4063f7e:      	shlq	$0x5, %rax
 4063f82:      	negq	%rax
 4063f85:      	leaq	-0x40(%r14,%rax), %rbx
 4063f8a:      	movq	(%rbx), %r12
 4063f8d:      	movq	%rbp, %r15
 4063f90:      	jmp	0x4063141 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa11>
 4063f95:      	leaq	-0x38(%rax), %rsi
 4063f99:      	movq	-0x78(%rax), %r11
 4063f9d:      	jmp	0x4063fe4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b4>
 4063f9f:      	leaq	-0x38(%rax), %rsi
 4063fa3:      	movq	(%rsi), %r11
 4063fa6:      	jmp	0x4063fe4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b4>
 4063fa8:      	leaq	-0x16(%rax), %rsi
 4063fac:      	testb	$0x1, (%rsi)
 4063faf:      	jne	0x4063fce <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x189e>
 4063fb1:      	xorl	%r11d, %r11d
 4063fb4:      	jmp	0x4063fe0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b0>
 4063fb6:      	leaq	0x40(%rax), %rsi
 4063fba:      	movl	(%rsi), %r11d
 4063fbd:      	shlq	$0x5, %r11
 4063fc1:      	movq	%rbx, %r12
 4063fc4:      	subq	%r11, %r12
 4063fc7:      	movq	-0x40(%r12), %r11
 4063fcc:      	jmp	0x4063fe0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18b0>
 4063fce:      	movl	(%r9), %r11d
 4063fd1:      	shll	$0x5, %r11d
 4063fd5:      	movq	%rbx, %r12
 4063fd8:      	subq	%r11, %r12
 4063fdb:      	movq	0x20(%r12), %r11
 4063fe0:      	leaq	-0x38(%rax), %rsi
 4063fe4:      	movq	$0x0, (%rsp)
 4063fec:      	cmpq	%r11, %r10
 4063fef:      	je	0x4063ffb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x18cb>
 4063ff1:      	movq	0x28(%rsp), %r15
 4063ff6:      	jmp	0x40628c8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x198>
 4063ffb:      	cmpl	$0x1, %r8d
 4063fff:      	jne	0x4064036 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1906>
 4064001:      	andl	$0x4, %r14d
 4064005:      	orq	%rcx, %r14
 4064008:      	movq	%r14, 0x40(%rsp)
 406400d:      	movl	$0x1, %ecx
 4064012:      	movq	%rcx, (%rsp)
 4064016:      	movq	%rbx, %rbp
 4064019:      	movq	0x28(%rsp), %r15
 406401e:      	movzbl	-0x18(%rax), %r9d
 4064023:      	leal	-0x1e(%r9), %r10d
 4064027:      	cmpb	$0xa, %r10b
 406402b:      	ja	0x40629d0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x2a0>
 4064031:      	jmp	0x40629aa <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x27a>
 4064036:      	movq	%rbp, 0x8(%rsp)
 406403b:      	movq	%r13, 0x38(%rsp)
 4064040:      	movq	%rsi, 0x40(%rsp)
 4064045:      	leaq	-0x20(%rsi), %r13
 4064049:      	movl	$0x1, %esi
 406404e:      	movq	%rsi, (%rsp)
 4064052:      	movl	$0x40, %ebp
 4064057:      	addl	$-0x1f, %edi
 406405a:      	leaq	-0x25c5b5d(%rip), %rsi  # 0x1a9e504 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x104>
 4064061:      	movslq	(%rsi,%rdi,4), %r12
 4064065:      	addq	%rsi, %r12
 4064068:      	movabsq	$0x100000000, %r11      # imm = 0x100000000
 4064072:      	jmpq	*%r12
 4064075:      	movl	$0x1, %esi
 406407a:      	cmpq	$-0x1000, %rdi          # imm = 0xF000
 4064081:      	je	0x40631bd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa8d>
 4064087:      	addl	%esi, %edx
 4064089:      	incl	%esi
 406408b:      	andl	%ecx, %edx
 406408d:      	movq	%rdx, %rdi
 4064090:      	shlq	$0x4, %rdi
 4064094:      	movq	(%rax,%rdi), %rdi
 4064098:      	cmpq	%rdi, %r12
 406409b:      	je	0x406317d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0xa4d>
 40640a1:      	jmp	0x406407a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x194a>
 40640a3:      	movl	$0x1, %edi
 40640a8:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 40640af:      	jne	0x40640ba <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x198a>
 40640b1:      	cmpq	$-0x1000, %r8           # imm = 0xF000
 40640b8:      	je	0x40640dd <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19ad>
 40640ba:      	addl	%edi, %edx
 40640bc:      	incl	%edi
 40640be:      	andl	%esi, %edx
 40640c0:      	leaq	(%rdx,%rdx,2), %r10
 40640c4:      	movq	(%rax,%r10,8), %r9
 40640c8:      	movq	0x8(%rax,%r10,8), %r8
 40640cd:      	cmpq	%r9, %rbp
 40640d0:      	jne	0x40640a8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1978>
 40640d2:      	leaq	(%rax,%r10,8), %r10
 40640d6:      	cmpq	%r8, %rbx
 40640d9:      	je	0x40640e5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19b5>
 40640db:      	jmp	0x40640a8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1978>
 40640dd:      	leaq	(%rcx,%rcx,2), %rdx
 40640e1:      	leaq	(%rax,%rdx,8), %r10
 40640e5:      	leaq	(%rcx,%rcx,2), %rcx
 40640e9:      	leaq	(%rax,%rcx,8), %rax
 40640ed:      	cmpq	%rax, %r10
 40640f0:      	je	0x4062770 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x40>
 40640f6:      	movl	0x10(%r10), %eax
 40640fa:      	movq	0x20(%rsp), %rbx
 40640ff:      	movq	0x58(%rbx), %r15
 4064103:      	cmpl	%eax, -0x8(%r15)
 4064107:      	jbe	0x4062790 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 406410d:      	movl	%eax, -0x8(%r15)
 4064111:      	jmp	0x4062790 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x60>
 4064116:      	nopw	%cs:(%rax,%rax)
 4064120:      	movq	(%rsp), %r12
 4064124:      	incq	%r12
 4064127:      	movq	%r12, (%rsp)
 406412b:      	cmpq	%r12, %r15
 406412e:      	je	0x40641eb <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1abb>
 4064134:      	incq	%r11
 4064137:      	addq	$0x20, %rbp
 406413b:      	addq	$-0x20, %r13
 406413f:      	leaq	-0x25c5c42(%rip), %rsi  # 0x1a9e504 <_ZTSN12_GLOBAL__N_136StraightLineStrengthReduceLegacyPassE.llvm.3408246754568883774+0x104>
 4064146:      	movslq	(%rsi,%rdi,4), %r12
 406414a:      	addq	%rsi, %r12
 406414d:      	jmpq	*%r12
 4064150:      	movq	0x30(%rsp), %rsi
 4064155:      	movq	(%rsi), %r12
 4064158:      	movq	(%r12,%rbp), %r12
 406415c:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 406415e:      	movq	(%r13), %r12
 4064162:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 4064164:      	movq	0x40(%rsp), %rsi
 4064169:      	movq	(%rsi), %r12
 406416c:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 406416e:      	movq	-0x58(%rax), %r12
 4064172:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 4064174:      	movq	0x48(%rsp), %rsi
 4064179:      	testb	$0x1, (%rsi)
 406417c:      	jne	0x4064183 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a53>
 406417e:      	xorl	%r12d, %r12d
 4064181:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 4064183:      	movl	(%r9), %r12d
 4064186:      	shll	$0x5, %r12d
 406418a:      	movq	%rbx, %rsi
 406418d:      	subq	%r12, %rsi
 4064190:      	movq	0x20(%rsi), %r12
 4064194:      	nopw	%cs:(%rax,%rax)
 406419e:      	nop
 40641a0:      	cmpq	%r12, %r10
 40641a3:      	je	0x4064120 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x19f0>
 40641a9:      	movq	0x28(%rsp), %r15
 40641ae:      	movq	0x38(%rsp), %r13
 40641b3:      	movq	0x8(%rsp), %rbp
 40641b8:      	jmp	0x40628c8 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x198>
 40641bd:      	movq	0x30(%rsp), %rsi
 40641c2:      	movq	(%rsi), %rsi
 40641c5:      	movq	(%rsi,%rbp), %r12
 40641c9:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 40641cb:      	movq	0x10(%rsp), %rsi
 40641d0:      	movl	(%rsi), %esi
 40641d2:      	shlq	$0x5, %rsi
 40641d6:      	movq	0x40(%rsp), %r12
 40641db:      	subq	%rsi, %r12
 40641de:      	movl	%r11d, %esi
 40641e1:      	shlq	$0x5, %rsi
 40641e5:      	movq	(%r12,%rsi), %r12
 40641e9:      	jmp	0x40641a0 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a70>
 40641eb:      	movl	%r8d, %esi
 40641ee:      	movq	%rsi, (%rsp)
 40641f2:      	jmp	0x40641a9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1a79>
 40641f4:      	movq	0x20(%rsp), %rcx
 40641f9:      	movq	0x40(%rcx), %r13
 40641fd:      	movq	%r15, 0x38(%rsp)
 4064202:      	movq	%rbp, (%rsp)
 4064206:      	nopw	%cs:(%rax,%rax)
 4064210:      	movq	0x28(%rcx), %rbx
 4064214:      	addq	$-0x10, %rbx
 4064218:      	cmpq	0x48(%rcx), %r13
 406421c:      	je	0x4064320 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1bf0>
 4064222:      	movups	(%rbx), %xmm0
 4064225:      	movups	%xmm0, (%r13)
 406422a:      	movq	0x40(%rcx), %r13
 406422e:      	addq	$0x10, %r13
 4064232:      	movq	%r13, 0x40(%rcx)
 4064236:      	addq	$-0x10, 0x28(%rcx)
 406423b:      	movl	0x18(%rcx), %esi
 406423e:      	testl	%esi, %esi
 4064240:      	je	0x40643e7 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cb7>
 4064246:      	movq	0x8(%rcx), %rdx
 406424a:      	movq	-0x10(%r13), %rcx
 406424e:      	movq	-0x8(%r13), %rdi
 4064252:      	movl	%ecx, %eax
 4064254:      	shrl	$0x4, %eax
 4064257:      	movl	%ecx, %r8d
 406425a:      	shrl	$0x9, %r8d
 406425e:      	xorl	%eax, %r8d
 4064261:      	movl	%edi, %eax
 4064263:      	shrl	$0x4, %eax
 4064266:      	movl	%edi, %r9d
 4064269:      	shrl	$0x9, %r9d
 406426d:      	xorl	%eax, %r9d
 4064270:      	shlq	$0x20, %r8
 4064274:      	orq	%r8, %r9
 4064277:      	movabsq	$-0x40a7b892e31b1a47, %rax # imm = 0xBF58476D1CE4E5B9
 4064281:      	imulq	%rax, %r9
 4064285:      	movq	%r9, %r8
 4064288:      	shrq	$0x1f, %r8
 406428c:      	xorl	%r9d, %r8d
 406428f:      	leal	-0x1(%rsi), %r9d
 4064293:      	andl	%r9d, %r8d
 4064296:      	leaq	(%r8,%r8,2), %r10
 406429a:      	leaq	(%rdx,%r10,8), %rax
 406429e:      	movq	(%rdx,%r10,8), %r14
 40642a2:      	movq	0x8(%rdx,%r10,8), %rbx
 40642a7:      	cmpq	%r14, %rcx
 40642aa:      	jne	0x40642b5 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b85>
 40642ac:      	cmpq	%rbx, %rdi
 40642af:      	je	0x4064441 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d11>
 40642b5:      	movl	$0x1, %r10d
 40642bb:      	xorl	%r11d, %r11d
 40642be:      	cmpq	$-0x1000, %r14          # imm = 0xF000
 40642c5:      	jne	0x40642d4 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ba4>
 40642c7:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 40642ce:      	je	0x4064465 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d35>
 40642d4:      	xorq	$-0x2000, %r14          # imm = 0xE000
 40642db:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 40642e2:      	orq	%r14, %rbx
 40642e5:      	orq	%r11, %rbx
 40642e8:      	cmoveq	%rax, %r11
 40642ec:      	addl	%r10d, %r8d
 40642ef:      	incl	%r10d
 40642f2:      	andl	%r9d, %r8d
 40642f5:      	leaq	(%r8,%r8,2), %rbx
 40642f9:      	leaq	(%rdx,%rbx,8), %rax
 40642fd:      	movq	(%rdx,%rbx,8), %r14
 4064301:      	movq	0x8(%rdx,%rbx,8), %rbx
 4064306:      	cmpq	%r14, %rcx
 4064309:      	jne	0x40642be <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b8e>
 406430b:      	cmpq	%rbx, %rdi
 406430e:      	je	0x4064441 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d11>
 4064314:      	jmp	0x40642be <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b8e>
 4064316:      	nopw	%cs:(%rax,%rax)
 4064320:      	movq	0x38(%rcx), %r14
 4064324:      	movq	%r13, %r15
 4064327:      	subq	%r14, %r15
 406432a:      	movabsq	$0x7ffffffffffffff0, %rax # imm = 0x7FFFFFFFFFFFFFF0
 4064334:      	cmpq	%rax, %r15
 4064337:      	je	0x406458b <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e5b>
 406433d:      	movq	%r15, %rax
 4064340:      	sarq	$0x4, %rax
 4064344:      	cmpq	$0x1, %rax
 4064348:      	movq	%rax, %rcx
 406434b:      	adcq	$0x0, %rcx
 406434f:      	leaq	(%rcx,%rax), %rbp
 4064353:      	movabsq	$0x7ffffffffffffff, %rdx # imm = 0x7FFFFFFFFFFFFFF
 406435d:      	cmpq	%rdx, %rbp
 4064360:      	cmovaeq	%rdx, %rbp
 4064364:      	addq	%rax, %rcx
 4064367:      	cmovbq	%rdx, %rbp
 406436b:      	shlq	$0x4, %rbp
 406436f:      	movq	%rbp, %rdi
 4064372:      	callq	0x828a6b0 <_Znwm@plt>
 4064377:      	movq	%rax, %r12
 406437a:      	movups	(%rbx), %xmm0
 406437d:      	movups	%xmm0, (%rax,%r15)
 4064382:      	movq	%rax, %rbx
 4064385:      	cmpq	%r13, %r14
 4064388:      	je	0x40643a3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c73>
 406438a:      	movq	%r12, %rbx
 406438d:      	movq	%r14, %rax
 4064390:      	movups	(%rax), %xmm0
 4064393:      	movups	%xmm0, (%rbx)
 4064396:      	addq	$0x10, %rax
 406439a:      	addq	$0x10, %rbx
 406439e:      	cmpq	%r13, %rax
 40643a1:      	jne	0x4064390 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c60>
 40643a3:      	testq	%r14, %r14
 40643a6:      	je	0x40643b3 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1c83>
 40643a8:      	movq	%r14, %rdi
 40643ab:      	movq	%r15, %rsi
 40643ae:      	callq	0x828a6f0 <_ZdlPvm@plt>
 40643b3:      	addq	$0x10, %rbx
 40643b7:      	movq	0x20(%rsp), %rcx
 40643bc:      	movq	%r12, 0x38(%rcx)
 40643c0:      	movq	%rbx, 0x40(%rcx)
 40643c4:      	addq	%rbp, %r12
 40643c7:      	movq	%r12, 0x48(%rcx)
 40643cb:      	movq	%rbx, %r13
 40643ce:      	movq	0x38(%rsp), %r15
 40643d3:      	movq	(%rsp), %rbp
 40643d7:      	addq	$-0x10, 0x28(%rcx)
 40643dc:      	movl	0x18(%rcx), %esi
 40643df:      	testl	%esi, %esi
 40643e1:      	jne	0x4064246 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1b16>
 40643e7:      	xorl	%eax, %eax
 40643e9:      	movq	%rcx, %rbx
 40643ec:      	movl	0x10(%rcx), %ecx
 40643ef:      	leal	0x4(,%rcx,4), %edx
 40643f6:      	leal	(%rsi,%rsi,2), %edi
 40643f9:      	cmpl	%edi, %edx
 40643fb:      	jae	0x4064476 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d46>
 40643fd:      	movl	%ecx, %edx
 40643ff:      	notl	%edx
 4064401:      	addl	%esi, %edx
 4064403:      	subl	0x14(%rbx), %edx
 4064406:      	movl	%esi, %edi
 4064408:      	shrl	$0x3, %edi
 406440b:      	cmpl	%edi, %edx
 406440d:      	jbe	0x4064478 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1d48>
 406440f:      	incl	%ecx
 4064411:      	movl	%ecx, 0x10(%rbx)
 4064414:      	cmpq	$-0x1000, (%rax)        # imm = 0xF000
 406441b:      	jne	0x4064427 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cf7>
 406441d:      	cmpq	$-0x1000, 0x8(%rax)     # imm = 0xF000
 4064425:      	je	0x406442a <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cfa>
 4064427:      	decl	0x14(%rbx)
 406442a:      	movups	-0x10(%r13), %xmm0
 406442f:      	movups	%xmm0, (%rax)
 4064432:      	movl	$0x0, 0x10(%rax)
 4064439:      	movq	0x40(%rbx), %r13
 406443d:      	movq	-0x10(%r13), %rcx
 4064441:      	movl	$0xffffffff, 0x10(%rax) # imm = 0xFFFFFFFF
 4064448:      	cmpq	%r15, %rcx
 406444b:      	movq	0x20(%rsp), %rcx
 4064450:      	jne	0x4064210 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ae0>
 4064456:      	cmpq	%rbp, -0x8(%r13)
 406445a:      	jne	0x4064210 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ae0>
 4064460:      	jmp	0x4064579 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e49>
 4064465:      	testq	%r11, %r11
 4064468:      	cmovneq	%r11, %rax
 406446c:      	movq	0x20(%rsp), %rcx
 4064471:      	jmp	0x40643e9 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cb9>
 4064476:      	addl	%esi, %esi
 4064478:      	movq	0x78(%rsp), %rdi
 406447d:      	callq	0x4064820 <_ZN4llvm12DenseMapBaseINS_8DenseMapISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS4_Lj4ENS_12DenseMapInfoIS4_vEEEEEjNS6_ISA_vEENS_6detail12DenseMapPairISA_jEEEESA_jSB_SE_E4growEj>
 4064482:      	movl	0x18(%rbx), %ecx
 4064485:      	testl	%ecx, %ecx
 4064487:      	je	0x406454f <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e1f>
 406448d:      	movq	0x8(%rbx), %rdx
 4064491:      	movq	-0x10(%r13), %rsi
 4064495:      	movq	-0x8(%r13), %rdi
 4064499:      	movl	%esi, %eax
 406449b:      	shrl	$0x4, %eax
 406449e:      	movl	%esi, %r8d
 40644a1:      	shrl	$0x9, %r8d
 40644a5:      	xorl	%eax, %r8d
 40644a8:      	movl	%edi, %eax
 40644aa:      	shrl	$0x4, %eax
 40644ad:      	movl	%edi, %r9d
 40644b0:      	shrl	$0x9, %r9d
 40644b4:      	xorl	%eax, %r9d
 40644b7:      	shlq	$0x20, %r8
 40644bb:      	orq	%r8, %r9
 40644be:      	movabsq	$-0x40a7b892e31b1a47, %rax # imm = 0xBF58476D1CE4E5B9
 40644c8:      	imulq	%rax, %r9
 40644cc:      	movq	%r9, %r8
 40644cf:      	shrq	$0x1f, %r8
 40644d3:      	xorl	%r9d, %r8d
 40644d6:      	decl	%ecx
 40644d8:      	andl	%ecx, %r8d
 40644db:      	leaq	(%r8,%r8,2), %r9
 40644df:      	leaq	(%rdx,%r9,8), %rax
 40644e3:      	movq	(%rdx,%r9,8), %rbx
 40644e7:      	movq	0x8(%rdx,%r9,8), %r11
 40644ec:      	cmpq	%rbx, %rsi
 40644ef:      	jne	0x40644f6 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dc6>
 40644f1:      	cmpq	%r11, %rdi
 40644f4:      	je	0x4064551 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e21>
 40644f6:      	movl	$0x1, %r9d
 40644fc:      	xorl	%r10d, %r10d
 40644ff:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 4064506:      	jne	0x4064511 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1de1>
 4064508:      	cmpq	$-0x1000, %r11          # imm = 0xF000
 406450f:      	je	0x4064570 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e40>
 4064511:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 4064518:      	xorq	$-0x2000, %r11          # imm = 0xE000
 406451f:      	orq	%rbx, %r11
 4064522:      	orq	%r10, %r11
 4064525:      	cmoveq	%rax, %r10
 4064529:      	addl	%r9d, %r8d
 406452c:      	incl	%r9d
 406452f:      	andl	%ecx, %r8d
 4064532:      	leaq	(%r8,%r8,2), %r11
 4064536:      	leaq	(%rdx,%r11,8), %rax
 406453a:      	movq	(%rdx,%r11,8), %rbx
 406453e:      	movq	0x8(%rdx,%r11,8), %r11
 4064543:      	cmpq	%rbx, %rsi
 4064546:      	jne	0x40644ff <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dcf>
 4064548:      	cmpq	%r11, %rdi
 406454b:      	je	0x4064551 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e21>
 406454d:      	jmp	0x40644ff <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1dcf>
 406454f:      	xorl	%eax, %eax
 4064551:      	movq	0x20(%rsp), %rbx
 4064556:      	movl	0x10(%rbx), %ecx
 4064559:      	incl	%ecx
 406455b:      	movl	%ecx, 0x10(%rbx)
 406455e:      	cmpq	$-0x1000, (%rax)        # imm = 0xF000
 4064565:      	je	0x406441d <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1ced>
 406456b:      	jmp	0x4064427 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1cf7>
 4064570:      	testq	%r10, %r10
 4064573:      	cmovneq	%r10, %rax
 4064577:      	jmp	0x4064551 <_ZN4llvm12scc_iteratorISt4pairIPNS_10RegionNodeEPNS_13SmallDenseSetIS3_Lj4ENS_12DenseMapInfoIS3_vEEEEEN12_GLOBAL__N_114SubGraphTraitsEE10GetNextSCCEv+0x1e21>
 4064579:      	addq	$0xa8, %rsp
 4064580:      	popq	%rbx
 4064581:      	popq	%r12
 4064583:      	popq	%r13
 4064585:      	popq	%r14
 4064587:      	popq	%r15
 4064589:      	popq	%rbp
 406458a:      	retq
 406458b:      	leaq	-0x33c9ba8(%rip), %rdi  # 0xc9a9ea <.str.llvm.15102873539259085389>
 4064592:      	callq	0x828a7c0 <_ZSt20__throw_length_errorPKc@plt>
