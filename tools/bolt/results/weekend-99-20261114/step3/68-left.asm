
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000006c66210 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE>:
 6c66210:      	pushq	%rbp
 6c66211:      	pushq	%r15
 6c66213:      	pushq	%r14
 6c66215:      	pushq	%r13
 6c66217:      	pushq	%r12
 6c66219:      	pushq	%rbx
 6c6621a:      	subq	$0x288, %rsp            # imm = 0x288
 6c66221:      	movq	%rdx, 0x98(%rsp)
 6c66229:      	movq	%rsi, %rbx
 6c6622c:      	movq	$0x1, 0x48(%rsp)
 6c66235:      	movq	$-0x1000, 0x50(%rsp)    # imm = 0xF000
 6c6623e:      	movq	$-0x1000, 0x60(%rsp)    # imm = 0xF000
 6c66247:      	movq	$-0x1000, 0x70(%rsp)    # imm = 0xF000
 6c66250:      	movq	$-0x1000, 0x80(%rsp)    # imm = 0xF000
 6c6625c:      	leaq	0x188(%rsp), %rax
 6c66264:      	movq	%rax, 0x178(%rsp)
 6c6626c:      	movabsq	$0x1000000000, %rax     # imm = 0x1000000000
 6c66276:      	movq	%rax, 0x180(%rsp)
 6c6627e:      	movq	%rdi, (%rsp)
 6c66282:      	movq	0x30(%rdi), %rax
 6c66286:      	andq	$-0x8, %rax
 6c6628a:      	movq	0x8(%rax), %rax
 6c6628e:      	andq	$-0x10, %rax
 6c66292:      	movq	(%rax), %rax
 6c66295:      	movq	0x8(%rax), %rax
 6c66299:      	andq	$-0x10, %rax
 6c6629d:      	movq	(%rax), %rax
 6c662a0:      	movzbl	0x10(%rax), %ecx
 6c662a4:      	leal	-0x2e(%rcx), %edx
 6c662a7:      	cmpb	$0x3, %dl
 6c662aa:      	setb	%dl
 6c662ad:      	testq	%rax, %rax
 6c662b0:      	setne	%sil
 6c662b4:      	leal	-0x2f(%rcx), %edi
 6c662b7:      	cmpb	$0x2, %dil
 6c662bb:      	setb	%dil
 6c662bf:      	andb	%dl, %dil
 6c662c2:      	andb	%sil, %dil
 6c662c5:      	cmpb	$0x1, %dil
 6c662c9:      	movq	%rbx, 0x18(%rsp)
 6c662ce:      	jne	0x6c6631e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x10e>
 6c662d0:      	movq	0x18(%rax), %r14
 6c662d4:      	cmpb	$0x30, %cl
 6c662d7:      	jne	0x6c662e8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xd8>
 6c662d9:      	movl	0x1c(%r14), %eax
 6c662dd:      	andl	$0x7f, %eax
 6c662e0:      	addl	$-0x3b, %eax
 6c662e3:      	cmpl	$0x2, %eax
 6c662e6:      	ja	0x6c6631e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x10e>
 6c662e8:      	movq	0x80(%r14), %rax
 6c662ef:      	testq	%rax, %rax
 6c662f2:      	jne	0x6c66311 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x101>
 6c662f4:      	movq	0x68(%r14), %rsi
 6c662f8:      	leaq	0x60(%rsi), %rdi
 6c662fc:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 6c66301:      	movq	0x80(%r14), %rax
 6c66308:      	testq	%rax, %rax
 6c6630b:      	je	0x6c66c69 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa59>
 6c66311:      	movq	0x58(%rax), %rax
 6c66315:      	testq	%rax, %rax
 6c66318:      	cmovneq	%rax, %r14
 6c6631c:      	jmp	0x6c66321 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x111>
 6c6631e:      	xorl	%r14d, %r14d
 6c66321:      	movq	%r14, %rax
 6c66324:      	nopw	%cs:(%rax,%rax)
 6c6632e:      	nop
 6c66330:      	movq	%rax, %rbx
 6c66333:      	testb	$-0x80, 0x48(%rax)
 6c66337:      	je	0x6c66347 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x137>
 6c66339:      	testb	$0x8, 0x4b(%rbx)
 6c6633d:      	jne	0x6c66347 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x137>
 6c6633f:      	movq	%rbx, %rdi
 6c66342:      	callq	0x75500b0 <_ZNK5clang10RecordDecl29LoadFieldsFromExternalStorageEv>
 6c66347:      	movq	%rbx, %rdi
 6c6634a:      	callq	0x754de40 <_ZNK5clang7TagDecl13getDefinitionEv>
 6c6634f:      	testq	%rax, %rax
 6c66352:      	je	0x6c66359 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x149>
 6c66354:      	cmpq	%rbx, %rax
 6c66357:      	jne	0x6c66330 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x120>
 6c66359:      	movq	%r14, 0x10(%rsp)
 6c6635e:      	movq	0x50(%rbx), %r12
 6c66362:      	testq	%r12, %r12
 6c66365:      	je	0x6c6638f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x17f>
 6c66367:      	nopw	(%rax,%rax)
 6c66370:      	movl	0x1c(%r12), %eax
 6c66375:      	andl	$0x7f, %eax
 6c66378:      	addl	$-0x31, %eax
 6c6637b:      	cmpl	$0x2, %eax
 6c6637e:      	jbe	0x6c66650 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x440>
 6c66384:      	movq	0x8(%r12), %r12
 6c66389:      	andq	$-0x8, %r12
 6c6638d:      	jne	0x6c66370 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x160>
 6c6638f:      	movq	(%rsp), %rax
 6c66393:      	movq	0x10(%rax), %rbx
 6c66397:      	movq	0x18(%rax), %rax
 6c6639b:      	subq	%rbx, %rax
 6c6639e:      	movabsq	$0x7fffffff8, %r14      # imm = 0x7FFFFFFF8
 6c663a8:      	andq	%rax, %r14
 6c663ab:      	je	0x6c66535 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x325>
 6c663b1:      	addq	%rbx, %r14
 6c663b4:      	movl	$0xfffe, %ebp           # imm = 0xFFFE
 6c663b9:      	xorl	%r13d, %r13d
 6c663bc:      	movl	$0x4, %r15d
 6c663c2:      	leaq	0x178(%rsp), %r12
 6c663ca:      	jmp	0x6c663fd <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1ed>
 6c663cc:      	movq	0x178(%rsp), %rcx
 6c663d4:      	shlq	$0x4, %rax
 6c663d8:      	movl	%esi, (%rcx,%rax)
 6c663db:      	movq	%rdx, 0x8(%rcx,%rax)
 6c663e0:      	incl	0x180(%rsp)
 6c663e7:      	nopw	(%rax,%rax)
 6c663f0:      	addq	$0x8, %rbx
 6c663f4:      	cmpq	%r14, %rbx
 6c663f7:      	je	0x6c66535 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x325>
 6c663fd:      	movq	(%rbx), %rdx
 6c66400:      	testq	%rdx, %rdx
 6c66403:      	je	0x6c663f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66405:      	movzwl	(%rdx), %eax
 6c66408:      	andl	$0x1ff, %eax            # imm = 0x1FF
 6c6640d:      	cmpw	$0x45, %ax
 6c66411:      	jne	0x6c663f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66413:      	movl	0x14(%rdx), %eax
 6c66416:      	andl	%ebp, %eax
 6c66418:      	cmpl	$0x2, %eax
 6c6641b:      	jne	0x6c66ab1 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8a1>
 6c66421:      	movq	0x18(%rdx), %rax
 6c66425:      	movq	0x8(%rax), %rax
 6c66429:      	testb	$0x1, %al
 6c6642b:      	jne	0x6c66440 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x230>
 6c6642d:      	movq	0x28(%rax), %rax
 6c66431:      	movl	%eax, %ecx
 6c66433:      	andq	$-0x8, %rax
 6c66437:      	testb	$0x7, %cl
 6c6643a:      	cmovneq	%r13, %rax
 6c6643e:      	jmp	0x6c66444 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x234>
 6c66440:      	andq	$-0x2, %rax
 6c66444:      	testb	$0x1, 0x48(%rsp)
 6c66449:      	movq	0x50(%rsp), %rcx
 6c6644e:      	leaq	0x50(%rsp), %rsi
 6c66453:      	cmovneq	%rsi, %rcx
 6c66457:      	movl	0x58(%rsp), %esi
 6c6645b:      	cmovnel	%r15d, %esi
 6c6645f:      	testl	%esi, %esi
 6c66461:      	je	0x6c663f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66463:      	movl	%eax, %r8d
 6c66466:      	shrl	$0x4, %r8d
 6c6646a:      	movl	%eax, %edi
 6c6646c:      	shrl	$0x9, %edi
 6c6646f:      	xorl	%r8d, %edi
 6c66472:      	leal	-0x1(%rsi), %r8d
 6c66476:      	andl	%r8d, %edi
 6c66479:      	movl	%edi, %r10d
 6c6647c:      	shll	$0x4, %r10d
 6c66480:      	movq	(%rcx,%r10), %r9
 6c66484:      	cmpq	%r9, %rax
 6c66487:      	jne	0x6c664b4 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2a4>
 6c66489:      	addq	%r10, %rcx
 6c6648c:      	movq	%rcx, %r11
 6c6648f:      	movl	0x8(%r11), %esi
 6c66493:      	movl	0x180(%rsp), %eax
 6c6649a:      	cmpl	0x184(%rsp), %eax
 6c664a1:      	jb	0x6c663cc <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1bc>
 6c664a7:      	movq	%r12, %rdi
 6c664aa:      	callq	0x6c67250 <_ZN4llvm23SmallVectorTemplateBaseIZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS3_12InitListExprEPNS3_18DesignatedInitExprEjRNS3_8QualTypeEPNS3_11DeclContext22specific_decl_iteratorINS3_9FieldDeclEEEPNS_6APSIntERjS8_SK_bbENK3$_0clERNS3_8SemaBase21SemaDiagnosticBuilderEE11ReorderInfoLb1EE18growAndEmplaceBackIJSP_EEERSP_DpOT_>
 6c664af:      	jmp	0x6c663f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c664b4:      	movl	$0x1, 0x8(%rsp)
 6c664bc:      	movq	%r9, %r10
 6c664bf:      	movl	%edi, %r11d
 6c664c2:      	cmpq	$-0x1000, %r10          # imm = 0xF000
 6c664c9:      	je	0x6c663f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c664cf:      	movq	%r11, %r10
 6c664d2:      	movl	0x8(%rsp), %r11d
 6c664d7:      	addl	%r11d, %r10d
 6c664da:      	incl	%r11d
 6c664dd:      	movl	%r11d, 0x8(%rsp)
 6c664e2:      	andl	%r8d, %r10d
 6c664e5:      	movq	%r10, %r11
 6c664e8:      	shlq	$0x4, %r10
 6c664ec:      	movq	(%rcx,%r10), %r10
 6c664f0:      	cmpq	%r10, %rax
 6c664f3:      	jne	0x6c664c2 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2b2>
 6c664f5:      	movl	$0x1, %r10d
 6c664fb:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 6c66502:      	je	0x6c66527 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x317>
 6c66504:      	addl	%r10d, %edi
 6c66507:      	incl	%r10d
 6c6650a:      	andl	%r8d, %edi
 6c6650d:      	movq	%rdi, %r9
 6c66510:      	shlq	$0x4, %r9
 6c66514:      	leaq	(%rcx,%r9), %r11
 6c66518:      	movq	(%rcx,%r9), %r9
 6c6651c:      	cmpq	%r9, %rax
 6c6651f:      	je	0x6c6648f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x27f>
 6c66525:      	jmp	0x6c664fb <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2eb>
 6c66527:      	movl	%esi, %eax
 6c66529:      	shlq	$0x4, %rax
 6c6652d:      	addq	%rax, %rcx
 6c66530:      	jmp	0x6c6648c <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x27c>
 6c66535:      	movl	0x180(%rsp), %ebx
 6c6653c:      	testq	%rbx, %rbx
 6c6653f:      	je	0x6c66815 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66545:      	movq	0x178(%rsp), %r12
 6c6654d:      	movq	%rbx, %r13
 6c66550:      	shlq	$0x4, %r13
 6c66554:      	addq	%r12, %r13
 6c66557:      	bsrq	%rbx, %rdx
 6c6655b:      	xorl	$0x3f, %edx
 6c6655e:      	addl	%edx, %edx
 6c66560:      	xorq	$0x7e, %rdx
 6c66564:      	movq	%r12, %rdi
 6c66567:      	movq	%r13, %rsi
 6c6656a:      	callq	0x6c672b0 <_ZSt16__introsort_loopIPZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS2_12InitListExprEPNS2_18DesignatedInitExprEjRNS2_8QualTypeEPNS2_11DeclContext22specific_decl_iteratorINS2_9FieldDeclEEEPN4llvm6APSIntERjS7_SK_bbENK3$_0clERNS2_8SemaBase21SemaDiagnosticBuilderEE11ReorderInfolN9__gnu_cxx5__ops15_Iter_comp_iterIZZNS1_26CheckDesignatedInitializerES5_S7_S9_jSB_SG_SJ_SK_S7_SK_bbENKSL_clESO_EUlRKSP_SV_E_EEEvT_SY_T0_T1_>
 6c6656f:      	leaq	0x10(%r12), %rbp
 6c66574:      	cmpl	$0x11, %ebx
 6c66577:      	jb	0x6c6680c <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5fc>
 6c6657d:      	movl	$0x10, %r15d
 6c66583:      	movq	%rbp, %rbx
 6c66586:      	movq	%r12, %rax
 6c66589:      	jmp	0x6c665c0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3b0>
 6c6658b:      	nopl	(%rax,%rax)
 6c66590:      	movl	%ecx, (%rdx)
 6c66592:      	movq	0xa0(%rsp), %rax
 6c6659a:      	movq	%rax, 0x4(%rdx)
 6c6659e:      	movl	0xa8(%rsp), %eax
 6c665a5:      	movl	%eax, 0xc(%rdx)
 6c665a8:      	addq	$0x10, %r15
 6c665ac:      	addq	$0x10, %rbx
 6c665b0:      	movq	%r14, %rax
 6c665b3:      	cmpq	$0x100, %r15            # imm = 0x100
 6c665ba:      	je	0x6c66b00 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8f0>
 6c665c0:      	leaq	(%r12,%r15), %r14
 6c665c4:      	movl	(%r12,%r15), %ecx
 6c665c8:      	cmpl	(%r12), %ecx
 6c665cc:      	jge	0x6c66600 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3f0>
 6c665ce:      	movups	(%r14), %xmm0
 6c665d2:      	movaps	%xmm0, 0xa0(%rsp)
 6c665da:      	cmpq	$0x11, %r15
 6c665de:      	jb	0x6c66645 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x435>
 6c665e0:      	movq	%rbp, %rdi
 6c665e3:      	movq	%r12, %rsi
 6c665e6:      	movq	%r15, %rdx
 6c665e9:      	callq	0x828ac50 <memmove@plt>
 6c665ee:      	movaps	0xa0(%rsp), %xmm0
 6c665f6:      	movups	%xmm0, (%r12)
 6c665fb:      	jmp	0x6c665a8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x398>
 6c665fd:      	nopl	(%rax)
 6c66600:      	movl	0x1c(%rax), %edx
 6c66603:      	movl	%edx, 0xa8(%rsp)
 6c6660a:      	movq	0x14(%rax), %rdx
 6c6660e:      	movq	%rdx, 0xa0(%rsp)
 6c66616:      	movq	%r14, %rdx
 6c66619:      	cmpl	(%rax), %ecx
 6c6661b:      	jge	0x6c66590 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x380>
 6c66621:      	movq	%rbx, %rdx
 6c66624:      	nopw	%cs:(%rax,%rax)
 6c6662e:      	nop
 6c66630:      	movups	-0x10(%rdx), %xmm0
 6c66634:      	movups	%xmm0, (%rdx)
 6c66637:      	cmpl	-0x20(%rdx), %ecx
 6c6663a:      	leaq	-0x10(%rdx), %rdx
 6c6663e:      	jl	0x6c66630 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x420>
 6c66640:      	jmp	0x6c66590 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x380>
 6c66645:      	movups	(%r12), %xmm0
 6c6664a:      	movups	%xmm0, 0x10(%rax)
 6c6664e:      	jmp	0x6c665ee <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3de>
 6c66650:      	xorl	%r13d, %r13d
 6c66653:      	movl	$0x4, %r14d
 6c66659:      	jmp	0x6c66669 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x459>
 6c6665b:      	nopl	(%rax,%rax)
 6c66660:      	testq	%r12, %r12
 6c66663:      	je	0x6c6638f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x17f>
 6c66669:      	testb	$-0x80, 0x1d(%r12)
 6c6666f:      	movq	%r12, %rbx
 6c66672:      	je	0x6c6667f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x46f>
 6c66674:      	movq	%r12, %rdi
 6c66677:      	callq	0x753cfe0 <_ZN5clang20getPrimaryMergedDeclEPNS_4DeclE>
 6c6667c:      	movq	%rax, %rbx
 6c6667f:      	movl	0x44(%rbx), %r15d
 6c66683:      	cmpl	$0xf, %r15d
 6c66687:      	ja	0x6c66695 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x485>
 6c66689:      	movq	%rbx, %rdi
 6c6668c:      	callq	0x754d840 <_ZNK5clang9FieldDecl19setCachedFieldIndexEv>
 6c66691:      	movl	0x44(%rbx), %r15d
 6c66695:      	movq	0x28(%r12), %rbp
 6c6669a:      	movl	%ebp, %eax
 6c6669c:      	andq	$-0x8, %rbp
 6c666a0:      	testb	$0x7, %al
 6c666a2:      	cmovneq	%r13, %rbp
 6c666a6:      	movl	0x48(%rsp), %eax
 6c666aa:      	movl	%eax, %ecx
 6c666ac:      	andl	$0x1, %ecx
 6c666af:      	movq	0x50(%rsp), %rdi
 6c666b4:      	leaq	0x50(%rsp), %rdx
 6c666b9:      	cmovneq	%rdx, %rdi
 6c666bd:      	movl	0x58(%rsp), %esi
 6c666c1:      	cmovnel	%r14d, %esi
 6c666c5:      	movl	$0x0, %edx
 6c666ca:      	testl	%esi, %esi
 6c666cc:      	je	0x6c66750 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x540>
 6c666d2:      	movl	%ebp, %edx
 6c666d4:      	shrl	$0x4, %edx
 6c666d7:      	movl	%ebp, %r8d
 6c666da:      	shrl	$0x9, %r8d
 6c666de:      	xorl	%edx, %r8d
 6c666e1:      	leal	-0x1(%rsi), %r9d
 6c666e5:      	andl	%r9d, %r8d
 6c666e8:      	movl	%r8d, %r10d
 6c666eb:      	shll	$0x4, %r10d
 6c666ef:      	leaq	(%rdi,%r10), %rdx
 6c666f3:      	movq	(%rdi,%r10), %rbx
 6c666f7:      	cmpq	%rbx, %rbp
 6c666fa:      	je	0x6c667a3 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x593>
 6c66700:      	movl	$0x1, %r10d
 6c66706:      	xorl	%r11d, %r11d
 6c66709:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 6c66710:      	je	0x6c6673f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x52f>
 6c66712:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 6c66719:      	orq	%r11, %rbx
 6c6671c:      	cmoveq	%rdx, %r11
 6c66720:      	addl	%r10d, %r8d
 6c66723:      	incl	%r10d
 6c66726:      	andl	%r9d, %r8d
 6c66729:      	movq	%r8, %rbx
 6c6672c:      	shlq	$0x4, %rbx
 6c66730:      	leaq	(%rdi,%rbx), %rdx
 6c66734:      	movq	(%rdi,%rbx), %rbx
 6c66738:      	cmpq	%rbx, %rbp
 6c6673b:      	je	0x6c667a3 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x593>
 6c6673d:      	jmp	0x6c66709 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x4f9>
 6c6673f:      	testq	%r11, %r11
 6c66742:      	cmovneq	%r11, %rdx
 6c66746:      	nopw	%cs:(%rax,%rax)
 6c66750:      	movq	%rdx, 0xa0(%rsp)
 6c66758:      	movl	%eax, %edi
 6c6675a:      	shrl	%edi
 6c6675c:      	leal	0x4(,%rdi,4), %r8d
 6c66764:      	leal	(%rsi,%rsi,2), %r9d
 6c66768:      	cmpl	%r9d, %r8d
 6c6676b:      	jae	0x6c667d4 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5c4>
 6c6676d:      	notl	%edi
 6c6676f:      	addl	%esi, %edi
 6c66771:      	subl	0x4c(%rsp), %edi
 6c66775:      	movl	%esi, %r8d
 6c66778:      	shrl	$0x3, %r8d
 6c6677c:      	cmpl	%r8d, %edi
 6c6677f:      	jbe	0x6c667d6 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5c6>
 6c66781:      	andl	$-0x2, %eax
 6c66784:      	leal	0x2(%rax,%rcx), %eax
 6c66788:      	movl	%eax, 0x48(%rsp)
 6c6678c:      	cmpq	$-0x1000, (%rdx)        # imm = 0xF000
 6c66793:      	je	0x6c66799 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x589>
 6c66795:      	decl	0x4c(%rsp)
 6c66799:      	movq	%rbp, (%rdx)
 6c6679c:      	movl	$0x0, 0x8(%rdx)
 6c667a3:      	shrl	$0x4, %r15d
 6c667a7:      	decl	%r15d
 6c667aa:      	movl	%r15d, 0x8(%rdx)
 6c667ae:      	nop
 6c667b0:      	movq	0x8(%r12), %r12
 6c667b5:      	andq	$-0x8, %r12
 6c667b9:      	je	0x6c66660 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x450>
 6c667bf:      	movl	0x1c(%r12), %eax
 6c667c4:      	andl	$0x7f, %eax
 6c667c7:      	addl	$-0x31, %eax
 6c667ca:      	cmpl	$0x3, %eax
 6c667cd:      	jae	0x6c667b0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5a0>
 6c667cf:      	jmp	0x6c66660 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x450>
 6c667d4:      	addl	%esi, %esi
 6c667d6:      	leaq	0x48(%rsp), %rbx
 6c667db:      	movq	%rbx, %rdi
 6c667de:      	callq	0x6c66e50 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPN5clang14IdentifierInfoEiLj4ENS_12DenseMapInfoIS4_vEENS_6detail12DenseMapPairIS4_iEEEES4_iS6_S9_E4growEj>
 6c667e3:      	movq	%rbx, %rdi
 6c667e6:      	movq	%rbp, %rsi
 6c667e9:      	leaq	0xa0(%rsp), %rdx
 6c667f1:      	callq	0x6c66db0 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPN5clang14IdentifierInfoEiLj4ENS_12DenseMapInfoIS4_vEENS_6detail12DenseMapPairIS4_iEEEES4_iS6_S9_E15LookupBucketForIS4_EEbRKT_RPS9_>
 6c667f6:      	movl	0x48(%rsp), %eax
 6c667fa:      	movq	0xa0(%rsp), %rdx
 6c66802:      	movl	%eax, %ecx
 6c66804:      	andl	$0x1, %ecx
 6c66807:      	jmp	0x6c66781 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x571>
 6c6680c:      	cmpl	$0x1, %ebx
 6c6680f:      	jne	0x6c66b72 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x962>
 6c66815:      	leaq	0xb8(%rsp), %rax
 6c6681d:      	xorps	%xmm0, %xmm0
 6c66820:      	movups	%xmm0, 0x128(%rsp)
 6c66828:      	movups	%xmm0, 0x118(%rsp)
 6c66830:      	movups	%xmm0, 0x108(%rsp)
 6c66838:      	movups	%xmm0, 0xf8(%rsp)
 6c66840:      	movups	%xmm0, 0xe8(%rsp)
 6c66848:      	movups	%xmm0, 0xd8(%rsp)
 6c66850:      	movups	%xmm0, 0xc8(%rsp)
 6c66858:      	movups	%xmm0, 0xb8(%rsp)
 6c66860:      	movq	%rax, 0xa0(%rsp)
 6c66868:      	movq	$0x0, 0xa8(%rsp)
 6c66874:      	movq	$0x80, 0xb0(%rsp)
 6c66880:      	movq	0x18(%rsp), %rax
 6c66885:      	movq	(%rax), %rax
 6c66888:      	movq	0xe8(%rax), %rcx
 6c6688f:      	movq	%rcx, 0x18(%rsp)
 6c66894:      	movq	0x110(%rax), %rax
 6c6689b:      	movq	%rax, 0x8(%rsp)
 6c668a0:      	movq	(%rsp), %rax
 6c668a4:      	movq	0x10(%rax), %rbx
 6c668a8:      	movq	0x18(%rax), %rax
 6c668ac:      	subq	%rbx, %rax
 6c668af:      	shrq	$0x3, %rax
 6c668b3:      	movl	%eax, %r15d
 6c668b6:      	movq	0x10(%rsp), %r14
 6c668bb:      	movq	0x68(%r14), %rsi
 6c668bf:      	leaq	0x60(%rsi), %rdi
 6c668c3:      	callq	0x43c4840 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 6c668c8:      	movq	0x80(%r14), %rax
 6c668cf:      	movl	0x10(%rax), %eax
 6c668d2:      	movl	0x180(%rsp), %ecx
 6c668d9:      	cmpq	%rax, %r15
 6c668dc:      	setne	%dl
 6c668df:      	testl	%ecx, %ecx
 6c668e1:      	setne	%sil
 6c668e5:      	andb	%dl, %sil
 6c668e8:      	cmpb	$0x1, %sil
 6c668ec:      	jne	0x6c66a97 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x887>
 6c668f2:      	movq	%r15, %rdi
 6c668f5:      	movq	0x178(%rsp), %rdx
 6c668fd:      	movq	%rdx, 0x10(%rsp)
 6c66902:      	movl	%ecx, %r12d
 6c66905:      	shlq	$0x4, %r12
 6c66909:      	leaq	(%rbx,%rax,8), %rcx
 6c6690d:      	movq	%rcx, 0x90(%rsp)
 6c66915:      	shlq	$0x3, %rax
 6c66919:      	leaq	0x38(%rsp), %r14
 6c6691e:      	shlq	$0x3, %rdi
 6c66922:      	subq	%rax, %rdi
 6c66925:      	addq	$-0x8, %rdi
 6c66929:      	movq	%rdi, (%rsp)
 6c6692d:      	addq	$-0x10, %r12
 6c66931:      	xorl	%r15d, %r15d
 6c66934:      	nopw	%cs:(%rax,%rax)
 6c6693e:      	nop
 6c66940:      	movq	0x10(%rsp), %rax
 6c66945:      	movq	0x8(%rax,%r15,2), %rdi
 6c6694a:      	callq	0x7b8fbd0 <_ZNK5clang4Stmt14getSourceRangeEv>
 6c6694f:      	movq	%rax, %rdi
 6c66952:      	movl	$0x1, %esi
 6c66957:      	movq	0x8(%rsp), %rdx
 6c6695c:      	movq	0x18(%rsp), %rcx
 6c66961:      	xorl	%r8d, %r8d
 6c66964:      	callq	0x7d60aa0 <_ZN5clang5Lexer13getSourceTextENS_15CharSourceRangeERKNS_13SourceManagerERKNS_11LangOptionsEPb>
 6c66969:      	movq	%rax, %rbp
 6c6696c:      	movq	%rdx, %rbx
 6c6696f:      	movq	0x90(%rsp), %rax
 6c66977:      	movq	(%rax,%r15), %rdi
 6c6697b:      	callq	0x7b8fbd0 <_ZNK5clang4Stmt14getSourceRangeEv>
 6c66980:      	movq	%rax, %r13
 6c66983:      	movq	%r14, 0x28(%rsp)
 6c66988:      	testq	%rbp, %rbp
 6c6698b:      	je	0x6c669d0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7c0>
 6c6698d:      	movq	%rbx, 0x20(%rsp)
 6c66992:      	movq	%r14, %rax
 6c66995:      	cmpq	$0x10, %rbx
 6c66999:      	jb	0x6c669bb <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ab>
 6c6699b:      	leaq	0x28(%rsp), %rdi
 6c669a0:      	leaq	0x20(%rsp), %rsi
 6c669a5:      	xorl	%edx, %edx
 6c669a7:      	callq	0x828a710 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_createERmm@plt>
 6c669ac:      	movq	%rax, 0x28(%rsp)
 6c669b1:      	movq	0x20(%rsp), %rcx
 6c669b6:      	movq	%rcx, 0x38(%rsp)
 6c669bb:      	testq	%rbx, %rbx
 6c669be:      	je	0x6c669fe <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ee>
 6c669c0:      	cmpq	$0x1, %rbx
 6c669c4:      	jne	0x6c669f0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7e0>
 6c669c6:      	movzbl	(%rbp), %ecx
 6c669ca:      	movb	%cl, (%rax)
 6c669cc:      	jmp	0x6c669fe <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ee>
 6c669ce:      	nop
 6c669d0:      	movq	$0x0, 0x30(%rsp)
 6c669d9:      	movb	$0x0, 0x38(%rsp)
 6c669de:      	xorl	%r8d, %r8d
 6c669e1:      	movq	%r14, %rcx
 6c669e4:      	jmp	0x6c66a1b <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x80b>
 6c669e6:      	nopw	%cs:(%rax,%rax)
 6c669f0:      	movq	%rax, %rdi
 6c669f3:      	movq	%rbp, %rsi
 6c669f6:      	movq	%rbx, %rdx
 6c669f9:      	callq	0x828ace0 <memcpy@plt>
 6c669fe:      	movq	0x20(%rsp), %rax
 6c66a03:      	movq	%rax, 0x30(%rsp)
 6c66a08:      	movq	0x28(%rsp), %rcx
 6c66a0d:      	movb	$0x0, (%rcx,%rax)
 6c66a11:      	movq	0x28(%rsp), %rcx
 6c66a16:      	movq	0x30(%rsp), %r8
 6c66a1b:      	leaq	0x138(%rsp), %rbx
 6c66a23:      	movq	%rbx, %rdi
 6c66a26:      	movq	%r13, %rsi
 6c66a29:      	movl	$0x1, %edx
 6c66a2e:      	callq	0x43f8890 <_ZN5clang9FixItHint17CreateReplacementENS_15CharSourceRangeEN4llvm9StringRefE>
 6c66a33:      	movq	0x98(%rsp), %rdi
 6c66a3b:      	movq	%rbx, %rsi
 6c66a3e:      	callq	0x66d3160 <_ZNK5clang8SemaBase21SemaDiagnosticBuilderlsINS_9FixItHintEvEERKS1_OT_>
 6c66a43:      	movq	0x150(%rsp), %rdi
 6c66a4b:      	leaq	0x160(%rsp), %rax
 6c66a53:      	cmpq	%rax, %rdi
 6c66a56:      	je	0x6c66a68 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x858>
 6c66a58:      	movq	0x160(%rsp), %rsi
 6c66a60:      	incq	%rsi
 6c66a63:      	callq	0x828a6f0 <_ZdlPvm@plt>
 6c66a68:      	movq	0x28(%rsp), %rdi
 6c66a6d:      	cmpq	%r14, %rdi
 6c66a70:      	je	0x6c66a7f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x86f>
 6c66a72:      	movq	0x38(%rsp), %rsi
 6c66a77:      	incq	%rsi
 6c66a7a:      	callq	0x828a6f0 <_ZdlPvm@plt>
 6c66a7f:      	cmpq	%r15, (%rsp)
 6c66a83:      	je	0x6c66a97 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x887>
 6c66a85:      	addq	$0x8, %r15
 6c66a89:      	testq	%r12, %r12
 6c66a8c:      	leaq	-0x10(%r12), %r12
 6c66a91:      	jne	0x6c66940 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x730>
 6c66a97:      	movq	0xa0(%rsp), %rdi
 6c66a9f:      	leaq	0xb8(%rsp), %rax
 6c66aa7:      	cmpq	%rax, %rdi
 6c66aaa:      	je	0x6c66ab1 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8a1>
 6c66aac:      	callq	0x828a6d0 <free@plt>
 6c66ab1:      	movq	0x178(%rsp), %rdi
 6c66ab9:      	leaq	0x188(%rsp), %rax
 6c66ac1:      	cmpq	%rax, %rdi
 6c66ac4:      	je	0x6c66acb <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8bb>
 6c66ac6:      	callq	0x828a6d0 <free@plt>
 6c66acb:      	testb	$0x1, 0x48(%rsp)
 6c66ad0:      	jne	0x6c66aee <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8de>
 6c66ad2:      	movl	0x58(%rsp), %esi
 6c66ad6:      	testq	%rsi, %rsi
 6c66ad9:      	je	0x6c66aee <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8de>
 6c66adb:      	movq	0x50(%rsp), %rdi
 6c66ae0:      	shlq	$0x4, %rsi
 6c66ae4:      	movl	$0x8, %edx
 6c66ae9:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 6c66aee:      	addq	$0x288, %rsp            # imm = 0x288
 6c66af5:      	popq	%rbx
 6c66af6:      	popq	%r12
 6c66af8:      	popq	%r13
 6c66afa:      	popq	%r14
 6c66afc:      	popq	%r15
 6c66afe:      	popq	%rbp
 6c66aff:      	retq
 6c66b00:      	addq	$0x100, %r12            # imm = 0x100
 6c66b07:      	jmp	0x6c66b35 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x925>
 6c66b09:      	nopl	(%rax)
 6c66b10:      	movl	%eax, (%rcx)
 6c66b12:      	movq	0xa0(%rsp), %rax
 6c66b1a:      	movq	%rax, 0x4(%rcx)
 6c66b1e:      	movl	0xa8(%rsp), %eax
 6c66b25:      	movl	%eax, 0xc(%rcx)
 6c66b28:      	addq	$0x10, %r12
 6c66b2c:      	cmpq	%r13, %r12
 6c66b2f:      	je	0x6c66815 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66b35:      	movl	(%r12), %eax
 6c66b39:      	movl	0xc(%r12), %ecx
 6c66b3e:      	movl	%ecx, 0xa8(%rsp)
 6c66b45:      	movq	0x4(%r12), %rcx
 6c66b4a:      	movq	%rcx, 0xa0(%rsp)
 6c66b52:      	movq	%r12, %rcx
 6c66b55:      	cmpl	-0x10(%r12), %eax
 6c66b5a:      	jge	0x6c66b10 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x900>
 6c66b5c:      	movq	%r12, %rcx
 6c66b5f:      	nop
 6c66b60:      	movups	-0x10(%rcx), %xmm0
 6c66b64:      	movups	%xmm0, (%rcx)
 6c66b67:      	cmpl	-0x20(%rcx), %eax
 6c66b6a:      	leaq	-0x10(%rcx), %rcx
 6c66b6e:      	jl	0x6c66b60 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x950>
 6c66b70:      	jmp	0x6c66b10 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x900>
 6c66b72:      	movq	%r12, %rdi
 6c66b75:      	jmp	0x6c66ba8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x998>
 6c66b77:      	nopw	(%rax,%rax)
 6c66b80:      	movl	%eax, (%rcx)
 6c66b82:      	movq	0xa0(%rsp), %rax
 6c66b8a:      	movq	%rax, 0x4(%rcx)
 6c66b8e:      	movl	0xa8(%rsp), %eax
 6c66b95:      	movl	%eax, 0xc(%rcx)
 6c66b98:      	leaq	0x10(%rbx), %rbp
 6c66b9c:      	movq	%rbx, %rdi
 6c66b9f:      	cmpq	%r13, %rbp
 6c66ba2:      	je	0x6c66815 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66ba8:      	movq	%rbp, %rbx
 6c66bab:      	movl	(%rbp), %eax
 6c66bae:      	cmpl	(%r12), %eax
 6c66bb2:      	jge	0x6c66c10 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa00>
 6c66bb4:      	movups	(%rbx), %xmm0
 6c66bb7:      	movaps	%xmm0, 0xa0(%rsp)
 6c66bbf:      	movq	%rbx, %rdx
 6c66bc2:      	subq	%r12, %rdx
 6c66bc5:      	movq	%rdx, %rax
 6c66bc8:      	sarq	$0x4, %rax
 6c66bcc:      	cmpq	$0x2, %rax
 6c66bd0:      	jl	0x6c66c55 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa45>
 6c66bd6:      	shlq	$0x4, %rax
 6c66bda:      	subq	%rax, %rdi
 6c66bdd:      	addq	$0x20, %rdi
 6c66be1:      	movq	%r12, %rsi
 6c66be4:      	callq	0x828ac50 <memmove@plt>
 6c66be9:      	movaps	0xa0(%rsp), %xmm0
 6c66bf1:      	movups	%xmm0, (%r12)
 6c66bf6:      	leaq	0x10(%rbx), %rbp
 6c66bfa:      	movq	%rbx, %rdi
 6c66bfd:      	cmpq	%r13, %rbp
 6c66c00:      	jne	0x6c66ba8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x998>
 6c66c02:      	jmp	0x6c66815 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66c07:      	nopw	(%rax,%rax)
 6c66c10:      	movl	0x1c(%rdi), %ecx
 6c66c13:      	movl	%ecx, 0xa8(%rsp)
 6c66c1a:      	movq	0x14(%rdi), %rcx
 6c66c1e:      	movq	%rcx, 0xa0(%rsp)
 6c66c26:      	movq	%rbx, %rcx
 6c66c29:      	cmpl	(%rdi), %eax
 6c66c2b:      	jge	0x6c66b80 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x970>
 6c66c31:      	movq	%rbx, %rcx
 6c66c34:      	nopw	%cs:(%rax,%rax)
 6c66c3e:      	nop
 6c66c40:      	movups	-0x10(%rcx), %xmm0
 6c66c44:      	movups	%xmm0, (%rcx)
 6c66c47:      	cmpl	-0x20(%rcx), %eax
 6c66c4a:      	leaq	-0x10(%rcx), %rcx
 6c66c4e:      	jl	0x6c66c40 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa30>
 6c66c50:      	jmp	0x6c66b80 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x970>
 6c66c55:      	cmpq	$0x10, %rdx
 6c66c59:      	jne	0x6c66be9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x9d9>
 6c66c5b:      	movups	(%r12), %xmm0
 6c66c60:      	movups	%xmm0, 0x10(%rdi)
 6c66c64:      	jmp	0x6c66be9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x9d9>
 6c66c69:      	xorl	%eax, %eax
 6c66c6b:      	jmp	0x6c66315 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x105>
