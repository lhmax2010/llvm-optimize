
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

0000000006c66160 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE>:
 6c66160:      	pushq	%rbp
 6c66161:      	pushq	%r15
 6c66163:      	pushq	%r14
 6c66165:      	pushq	%r13
 6c66167:      	pushq	%r12
 6c66169:      	pushq	%rbx
 6c6616a:      	subq	$0x288, %rsp            # imm = 0x288
 6c66171:      	movq	%rdx, 0x98(%rsp)
 6c66179:      	movq	%rsi, %rbx
 6c6617c:      	movq	$0x1, 0x48(%rsp)
 6c66185:      	movq	$-0x1000, 0x50(%rsp)    # imm = 0xF000
 6c6618e:      	movq	$-0x1000, 0x60(%rsp)    # imm = 0xF000
 6c66197:      	movq	$-0x1000, 0x70(%rsp)    # imm = 0xF000
 6c661a0:      	movq	$-0x1000, 0x80(%rsp)    # imm = 0xF000
 6c661ac:      	leaq	0x188(%rsp), %rax
 6c661b4:      	movq	%rax, 0x178(%rsp)
 6c661bc:      	movabsq	$0x1000000000, %rax     # imm = 0x1000000000
 6c661c6:      	movq	%rax, 0x180(%rsp)
 6c661ce:      	movq	%rdi, (%rsp)
 6c661d2:      	movq	0x30(%rdi), %rax
 6c661d6:      	andq	$-0x8, %rax
 6c661da:      	movq	0x8(%rax), %rax
 6c661de:      	andq	$-0x10, %rax
 6c661e2:      	movq	(%rax), %rax
 6c661e5:      	movq	0x8(%rax), %rax
 6c661e9:      	andq	$-0x10, %rax
 6c661ed:      	movq	(%rax), %rax
 6c661f0:      	movzbl	0x10(%rax), %ecx
 6c661f4:      	leal	-0x2e(%rcx), %edx
 6c661f7:      	cmpb	$0x3, %dl
 6c661fa:      	setb	%dl
 6c661fd:      	testq	%rax, %rax
 6c66200:      	setne	%sil
 6c66204:      	leal	-0x2f(%rcx), %edi
 6c66207:      	cmpb	$0x2, %dil
 6c6620b:      	setb	%dil
 6c6620f:      	andb	%dl, %dil
 6c66212:      	andb	%sil, %dil
 6c66215:      	cmpb	$0x1, %dil
 6c66219:      	movq	%rbx, 0x18(%rsp)
 6c6621e:      	jne	0x6c6626e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x10e>
 6c66220:      	movq	0x18(%rax), %r14
 6c66224:      	cmpb	$0x30, %cl
 6c66227:      	jne	0x6c66238 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xd8>
 6c66229:      	movl	0x1c(%r14), %eax
 6c6622d:      	andl	$0x7f, %eax
 6c66230:      	addl	$-0x3b, %eax
 6c66233:      	cmpl	$0x2, %eax
 6c66236:      	ja	0x6c6626e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x10e>
 6c66238:      	movq	0x80(%r14), %rax
 6c6623f:      	testq	%rax, %rax
 6c66242:      	jne	0x6c66261 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x101>
 6c66244:      	movq	0x68(%r14), %rsi
 6c66248:      	leaq	0x60(%rsi), %rdi
 6c6624c:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 6c66251:      	movq	0x80(%r14), %rax
 6c66258:      	testq	%rax, %rax
 6c6625b:      	je	0x6c66bb9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa59>
 6c66261:      	movq	0x58(%rax), %rax
 6c66265:      	testq	%rax, %rax
 6c66268:      	cmovneq	%rax, %r14
 6c6626c:      	jmp	0x6c66271 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x111>
 6c6626e:      	xorl	%r14d, %r14d
 6c66271:      	movq	%r14, %rax
 6c66274:      	nopw	%cs:(%rax,%rax)
 6c6627e:      	nop
 6c66280:      	movq	%rax, %rbx
 6c66283:      	testb	$-0x80, 0x48(%rax)
 6c66287:      	je	0x6c66297 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x137>
 6c66289:      	testb	$0x8, 0x4b(%rbx)
 6c6628d:      	jne	0x6c66297 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x137>
 6c6628f:      	movq	%rbx, %rdi
 6c66292:      	callq	0x7550020 <_ZNK5clang10RecordDecl29LoadFieldsFromExternalStorageEv>
 6c66297:      	movq	%rbx, %rdi
 6c6629a:      	callq	0x754ddb0 <_ZNK5clang7TagDecl13getDefinitionEv>
 6c6629f:      	testq	%rax, %rax
 6c662a2:      	je	0x6c662a9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x149>
 6c662a4:      	cmpq	%rbx, %rax
 6c662a7:      	jne	0x6c66280 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x120>
 6c662a9:      	movq	%r14, 0x10(%rsp)
 6c662ae:      	movq	0x50(%rbx), %r12
 6c662b2:      	testq	%r12, %r12
 6c662b5:      	je	0x6c662df <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x17f>
 6c662b7:      	nopw	(%rax,%rax)
 6c662c0:      	movl	0x1c(%r12), %eax
 6c662c5:      	andl	$0x7f, %eax
 6c662c8:      	addl	$-0x31, %eax
 6c662cb:      	cmpl	$0x2, %eax
 6c662ce:      	jbe	0x6c665a0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x440>
 6c662d4:      	movq	0x8(%r12), %r12
 6c662d9:      	andq	$-0x8, %r12
 6c662dd:      	jne	0x6c662c0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x160>
 6c662df:      	movq	(%rsp), %rax
 6c662e3:      	movq	0x10(%rax), %rbx
 6c662e7:      	movq	0x18(%rax), %rax
 6c662eb:      	subq	%rbx, %rax
 6c662ee:      	movabsq	$0x7fffffff8, %r14      # imm = 0x7FFFFFFF8
 6c662f8:      	andq	%rax, %r14
 6c662fb:      	je	0x6c66485 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x325>
 6c66301:      	addq	%rbx, %r14
 6c66304:      	movl	$0xfffe, %ebp           # imm = 0xFFFE
 6c66309:      	xorl	%r13d, %r13d
 6c6630c:      	movl	$0x4, %r15d
 6c66312:      	leaq	0x178(%rsp), %r12
 6c6631a:      	jmp	0x6c6634d <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1ed>
 6c6631c:      	movq	0x178(%rsp), %rcx
 6c66324:      	shlq	$0x4, %rax
 6c66328:      	movl	%esi, (%rcx,%rax)
 6c6632b:      	movq	%rdx, 0x8(%rcx,%rax)
 6c66330:      	incl	0x180(%rsp)
 6c66337:      	nopw	(%rax,%rax)
 6c66340:      	addq	$0x8, %rbx
 6c66344:      	cmpq	%r14, %rbx
 6c66347:      	je	0x6c66485 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x325>
 6c6634d:      	movq	(%rbx), %rdx
 6c66350:      	testq	%rdx, %rdx
 6c66353:      	je	0x6c66340 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66355:      	movzwl	(%rdx), %eax
 6c66358:      	andl	$0x1ff, %eax            # imm = 0x1FF
 6c6635d:      	cmpw	$0x45, %ax
 6c66361:      	jne	0x6c66340 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66363:      	movl	0x14(%rdx), %eax
 6c66366:      	andl	%ebp, %eax
 6c66368:      	cmpl	$0x2, %eax
 6c6636b:      	jne	0x6c66a01 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8a1>
 6c66371:      	movq	0x18(%rdx), %rax
 6c66375:      	movq	0x8(%rax), %rax
 6c66379:      	testb	$0x1, %al
 6c6637b:      	jne	0x6c66390 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x230>
 6c6637d:      	movq	0x28(%rax), %rax
 6c66381:      	movl	%eax, %ecx
 6c66383:      	andq	$-0x8, %rax
 6c66387:      	testb	$0x7, %cl
 6c6638a:      	cmovneq	%r13, %rax
 6c6638e:      	jmp	0x6c66394 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x234>
 6c66390:      	andq	$-0x2, %rax
 6c66394:      	testb	$0x1, 0x48(%rsp)
 6c66399:      	movq	0x50(%rsp), %rcx
 6c6639e:      	leaq	0x50(%rsp), %rsi
 6c663a3:      	cmovneq	%rsi, %rcx
 6c663a7:      	movl	0x58(%rsp), %esi
 6c663ab:      	cmovnel	%r15d, %esi
 6c663af:      	testl	%esi, %esi
 6c663b1:      	je	0x6c66340 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c663b3:      	movl	%eax, %r8d
 6c663b6:      	shrl	$0x4, %r8d
 6c663ba:      	movl	%eax, %edi
 6c663bc:      	shrl	$0x9, %edi
 6c663bf:      	xorl	%r8d, %edi
 6c663c2:      	leal	-0x1(%rsi), %r8d
 6c663c6:      	andl	%r8d, %edi
 6c663c9:      	movl	%edi, %r10d
 6c663cc:      	shll	$0x4, %r10d
 6c663d0:      	movq	(%rcx,%r10), %r9
 6c663d4:      	cmpq	%r9, %rax
 6c663d7:      	jne	0x6c66404 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2a4>
 6c663d9:      	addq	%r10, %rcx
 6c663dc:      	movq	%rcx, %r11
 6c663df:      	movl	0x8(%r11), %esi
 6c663e3:      	movl	0x180(%rsp), %eax
 6c663ea:      	cmpl	0x184(%rsp), %eax
 6c663f1:      	jb	0x6c6631c <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1bc>
 6c663f7:      	movq	%r12, %rdi
 6c663fa:      	callq	0x6c671a0 <_ZN4llvm23SmallVectorTemplateBaseIZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS3_12InitListExprEPNS3_18DesignatedInitExprEjRNS3_8QualTypeEPNS3_11DeclContext22specific_decl_iteratorINS3_9FieldDeclEEEPNS_6APSIntERjS8_SK_bbENK3$_0clERNS3_8SemaBase21SemaDiagnosticBuilderEE11ReorderInfoLb1EE18growAndEmplaceBackIJSP_EEERSP_DpOT_>
 6c663ff:      	jmp	0x6c66340 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c66404:      	movl	$0x1, 0x8(%rsp)
 6c6640c:      	movq	%r9, %r10
 6c6640f:      	movl	%edi, %r11d
 6c66412:      	cmpq	$-0x1000, %r10          # imm = 0xF000
 6c66419:      	je	0x6c66340 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x1e0>
 6c6641f:      	movq	%r11, %r10
 6c66422:      	movl	0x8(%rsp), %r11d
 6c66427:      	addl	%r11d, %r10d
 6c6642a:      	incl	%r11d
 6c6642d:      	movl	%r11d, 0x8(%rsp)
 6c66432:      	andl	%r8d, %r10d
 6c66435:      	movq	%r10, %r11
 6c66438:      	shlq	$0x4, %r10
 6c6643c:      	movq	(%rcx,%r10), %r10
 6c66440:      	cmpq	%r10, %rax
 6c66443:      	jne	0x6c66412 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2b2>
 6c66445:      	movl	$0x1, %r10d
 6c6644b:      	cmpq	$-0x1000, %r9           # imm = 0xF000
 6c66452:      	je	0x6c66477 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x317>
 6c66454:      	addl	%r10d, %edi
 6c66457:      	incl	%r10d
 6c6645a:      	andl	%r8d, %edi
 6c6645d:      	movq	%rdi, %r9
 6c66460:      	shlq	$0x4, %r9
 6c66464:      	leaq	(%rcx,%r9), %r11
 6c66468:      	movq	(%rcx,%r9), %r9
 6c6646c:      	cmpq	%r9, %rax
 6c6646f:      	je	0x6c663df <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x27f>
 6c66475:      	jmp	0x6c6644b <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x2eb>
 6c66477:      	movl	%esi, %eax
 6c66479:      	shlq	$0x4, %rax
 6c6647d:      	addq	%rax, %rcx
 6c66480:      	jmp	0x6c663dc <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x27c>
 6c66485:      	movl	0x180(%rsp), %ebx
 6c6648c:      	testq	%rbx, %rbx
 6c6648f:      	je	0x6c66765 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66495:      	movq	0x178(%rsp), %r12
 6c6649d:      	movq	%rbx, %r13
 6c664a0:      	shlq	$0x4, %r13
 6c664a4:      	addq	%r12, %r13
 6c664a7:      	bsrq	%rbx, %rdx
 6c664ab:      	xorl	$0x3f, %edx
 6c664ae:      	addl	%edx, %edx
 6c664b0:      	xorq	$0x7e, %rdx
 6c664b4:      	movq	%r12, %rdi
 6c664b7:      	movq	%r13, %rsi
 6c664ba:      	callq	0x6c67200 <_ZSt16__introsort_loopIPZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS2_12InitListExprEPNS2_18DesignatedInitExprEjRNS2_8QualTypeEPNS2_11DeclContext22specific_decl_iteratorINS2_9FieldDeclEEEPN4llvm6APSIntERjS7_SK_bbENK3$_0clERNS2_8SemaBase21SemaDiagnosticBuilderEE11ReorderInfolN9__gnu_cxx5__ops15_Iter_comp_iterIZZNS1_26CheckDesignatedInitializerES5_S7_S9_jSB_SG_SJ_SK_S7_SK_bbENKSL_clESO_EUlRKSP_SV_E_EEEvT_SY_T0_T1_>
 6c664bf:      	leaq	0x10(%r12), %rbp
 6c664c4:      	cmpl	$0x11, %ebx
 6c664c7:      	jb	0x6c6675c <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5fc>
 6c664cd:      	leaq	0x10(%r12), %rbx
 6c664d2:      	movl	$0x10, %r15d
 6c664d8:      	movq	%r12, %rax
 6c664db:      	jmp	0x6c66510 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3b0>
 6c664dd:      	nopl	(%rax)
 6c664e0:      	movl	%ecx, (%rdx)
 6c664e2:      	movq	0xa0(%rsp), %rax
 6c664ea:      	movq	%rax, 0x4(%rdx)
 6c664ee:      	movl	0xa8(%rsp), %eax
 6c664f5:      	movl	%eax, 0xc(%rdx)
 6c664f8:      	addq	$0x10, %r15
 6c664fc:      	addq	$0x10, %rbx
 6c66500:      	movq	%r14, %rax
 6c66503:      	cmpq	$0x100, %r15            # imm = 0x100
 6c6650a:      	je	0x6c66a50 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8f0>
 6c66510:      	leaq	(%r12,%r15), %r14
 6c66514:      	movl	(%r12,%r15), %ecx
 6c66518:      	cmpl	(%r12), %ecx
 6c6651c:      	jge	0x6c66550 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3f0>
 6c6651e:      	movups	(%r14), %xmm0
 6c66522:      	movaps	%xmm0, 0xa0(%rsp)
 6c6652a:      	cmpq	$0x11, %r15
 6c6652e:      	jb	0x6c66595 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x435>
 6c66530:      	movq	%rbp, %rdi
 6c66533:      	movq	%r12, %rsi
 6c66536:      	movq	%r15, %rdx
 6c66539:      	callq	0x828abc0 <memmove@plt>
 6c6653e:      	movaps	0xa0(%rsp), %xmm0
 6c66546:      	movups	%xmm0, (%r12)
 6c6654b:      	jmp	0x6c664f8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x398>
 6c6654d:      	nopl	(%rax)
 6c66550:      	movl	0x1c(%rax), %edx
 6c66553:      	movl	%edx, 0xa8(%rsp)
 6c6655a:      	movq	0x14(%rax), %rdx
 6c6655e:      	movq	%rdx, 0xa0(%rsp)
 6c66566:      	movq	%r14, %rdx
 6c66569:      	cmpl	(%rax), %ecx
 6c6656b:      	jge	0x6c664e0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x380>
 6c66571:      	movq	%rbx, %rdx
 6c66574:      	nopw	%cs:(%rax,%rax)
 6c6657e:      	nop
 6c66580:      	movups	-0x10(%rdx), %xmm0
 6c66584:      	movups	%xmm0, (%rdx)
 6c66587:      	cmpl	-0x20(%rdx), %ecx
 6c6658a:      	leaq	-0x10(%rdx), %rdx
 6c6658e:      	jl	0x6c66580 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x420>
 6c66590:      	jmp	0x6c664e0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x380>
 6c66595:      	movups	(%r12), %xmm0
 6c6659a:      	movups	%xmm0, 0x10(%rax)
 6c6659e:      	jmp	0x6c6653e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x3de>
 6c665a0:      	xorl	%r13d, %r13d
 6c665a3:      	movl	$0x4, %r14d
 6c665a9:      	jmp	0x6c665b9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x459>
 6c665ab:      	nopl	(%rax,%rax)
 6c665b0:      	testq	%r12, %r12
 6c665b3:      	je	0x6c662df <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x17f>
 6c665b9:      	testb	$-0x80, 0x1d(%r12)
 6c665bf:      	movq	%r12, %rbx
 6c665c2:      	je	0x6c665cf <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x46f>
 6c665c4:      	movq	%r12, %rdi
 6c665c7:      	callq	0x753cf50 <_ZN5clang20getPrimaryMergedDeclEPNS_4DeclE>
 6c665cc:      	movq	%rax, %rbx
 6c665cf:      	movl	0x44(%rbx), %r15d
 6c665d3:      	cmpl	$0xf, %r15d
 6c665d7:      	ja	0x6c665e5 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x485>
 6c665d9:      	movq	%rbx, %rdi
 6c665dc:      	callq	0x754d7b0 <_ZNK5clang9FieldDecl19setCachedFieldIndexEv>
 6c665e1:      	movl	0x44(%rbx), %r15d
 6c665e5:      	movq	0x28(%r12), %rbp
 6c665ea:      	movl	%ebp, %eax
 6c665ec:      	andq	$-0x8, %rbp
 6c665f0:      	testb	$0x7, %al
 6c665f2:      	cmovneq	%r13, %rbp
 6c665f6:      	movl	0x48(%rsp), %eax
 6c665fa:      	movl	%eax, %ecx
 6c665fc:      	andl	$0x1, %ecx
 6c665ff:      	movq	0x50(%rsp), %rdi
 6c66604:      	leaq	0x50(%rsp), %rdx
 6c66609:      	cmovneq	%rdx, %rdi
 6c6660d:      	movl	0x58(%rsp), %esi
 6c66611:      	cmovnel	%r14d, %esi
 6c66615:      	movl	$0x0, %edx
 6c6661a:      	testl	%esi, %esi
 6c6661c:      	je	0x6c666a0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x540>
 6c66622:      	movl	%ebp, %edx
 6c66624:      	shrl	$0x4, %edx
 6c66627:      	movl	%ebp, %r8d
 6c6662a:      	shrl	$0x9, %r8d
 6c6662e:      	xorl	%edx, %r8d
 6c66631:      	leal	-0x1(%rsi), %r9d
 6c66635:      	andl	%r9d, %r8d
 6c66638:      	movl	%r8d, %r10d
 6c6663b:      	shll	$0x4, %r10d
 6c6663f:      	leaq	(%rdi,%r10), %rdx
 6c66643:      	movq	(%rdi,%r10), %rbx
 6c66647:      	cmpq	%rbx, %rbp
 6c6664a:      	je	0x6c666f3 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x593>
 6c66650:      	movl	$0x1, %r10d
 6c66656:      	xorl	%r11d, %r11d
 6c66659:      	cmpq	$-0x1000, %rbx          # imm = 0xF000
 6c66660:      	je	0x6c6668f <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x52f>
 6c66662:      	xorq	$-0x2000, %rbx          # imm = 0xE000
 6c66669:      	orq	%r11, %rbx
 6c6666c:      	cmoveq	%rdx, %r11
 6c66670:      	addl	%r10d, %r8d
 6c66673:      	incl	%r10d
 6c66676:      	andl	%r9d, %r8d
 6c66679:      	movq	%r8, %rbx
 6c6667c:      	shlq	$0x4, %rbx
 6c66680:      	leaq	(%rdi,%rbx), %rdx
 6c66684:      	movq	(%rdi,%rbx), %rbx
 6c66688:      	cmpq	%rbx, %rbp
 6c6668b:      	je	0x6c666f3 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x593>
 6c6668d:      	jmp	0x6c66659 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x4f9>
 6c6668f:      	testq	%r11, %r11
 6c66692:      	cmovneq	%r11, %rdx
 6c66696:      	nopw	%cs:(%rax,%rax)
 6c666a0:      	movq	%rdx, 0xa0(%rsp)
 6c666a8:      	movl	%eax, %edi
 6c666aa:      	shrl	%edi
 6c666ac:      	leal	0x4(,%rdi,4), %r8d
 6c666b4:      	leal	(%rsi,%rsi,2), %r9d
 6c666b8:      	cmpl	%r9d, %r8d
 6c666bb:      	jae	0x6c66724 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5c4>
 6c666bd:      	notl	%edi
 6c666bf:      	addl	%esi, %edi
 6c666c1:      	subl	0x4c(%rsp), %edi
 6c666c5:      	movl	%esi, %r8d
 6c666c8:      	shrl	$0x3, %r8d
 6c666cc:      	cmpl	%r8d, %edi
 6c666cf:      	jbe	0x6c66726 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5c6>
 6c666d1:      	andl	$-0x2, %eax
 6c666d4:      	leal	0x2(%rax,%rcx), %eax
 6c666d8:      	movl	%eax, 0x48(%rsp)
 6c666dc:      	cmpq	$-0x1000, (%rdx)        # imm = 0xF000
 6c666e3:      	je	0x6c666e9 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x589>
 6c666e5:      	decl	0x4c(%rsp)
 6c666e9:      	movq	%rbp, (%rdx)
 6c666ec:      	movl	$0x0, 0x8(%rdx)
 6c666f3:      	shrl	$0x4, %r15d
 6c666f7:      	decl	%r15d
 6c666fa:      	movl	%r15d, 0x8(%rdx)
 6c666fe:      	nop
 6c66700:      	movq	0x8(%r12), %r12
 6c66705:      	andq	$-0x8, %r12
 6c66709:      	je	0x6c665b0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x450>
 6c6670f:      	movl	0x1c(%r12), %eax
 6c66714:      	andl	$0x7f, %eax
 6c66717:      	addl	$-0x31, %eax
 6c6671a:      	cmpl	$0x3, %eax
 6c6671d:      	jae	0x6c66700 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x5a0>
 6c6671f:      	jmp	0x6c665b0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x450>
 6c66724:      	addl	%esi, %esi
 6c66726:      	leaq	0x48(%rsp), %rbx
 6c6672b:      	movq	%rbx, %rdi
 6c6672e:      	callq	0x6c66da0 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPN5clang14IdentifierInfoEiLj4ENS_12DenseMapInfoIS4_vEENS_6detail12DenseMapPairIS4_iEEEES4_iS6_S9_E4growEj>
 6c66733:      	movq	%rbx, %rdi
 6c66736:      	movq	%rbp, %rsi
 6c66739:      	leaq	0xa0(%rsp), %rdx
 6c66741:      	callq	0x6c66d00 <_ZN4llvm12DenseMapBaseINS_13SmallDenseMapIPN5clang14IdentifierInfoEiLj4ENS_12DenseMapInfoIS4_vEENS_6detail12DenseMapPairIS4_iEEEES4_iS6_S9_E15LookupBucketForIS4_EEbRKT_RPS9_>
 6c66746:      	movl	0x48(%rsp), %eax
 6c6674a:      	movq	0xa0(%rsp), %rdx
 6c66752:      	movl	%eax, %ecx
 6c66754:      	andl	$0x1, %ecx
 6c66757:      	jmp	0x6c666d1 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x571>
 6c6675c:      	cmpl	$0x1, %ebx
 6c6675f:      	jne	0x6c66ac2 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x962>
 6c66765:      	leaq	0xb8(%rsp), %rax
 6c6676d:      	xorps	%xmm0, %xmm0
 6c66770:      	movups	%xmm0, 0x128(%rsp)
 6c66778:      	movups	%xmm0, 0x118(%rsp)
 6c66780:      	movups	%xmm0, 0x108(%rsp)
 6c66788:      	movups	%xmm0, 0xf8(%rsp)
 6c66790:      	movups	%xmm0, 0xe8(%rsp)
 6c66798:      	movups	%xmm0, 0xd8(%rsp)
 6c667a0:      	movups	%xmm0, 0xc8(%rsp)
 6c667a8:      	movups	%xmm0, 0xb8(%rsp)
 6c667b0:      	movq	%rax, 0xa0(%rsp)
 6c667b8:      	movq	$0x0, 0xa8(%rsp)
 6c667c4:      	movq	$0x80, 0xb0(%rsp)
 6c667d0:      	movq	0x18(%rsp), %rax
 6c667d5:      	movq	(%rax), %rax
 6c667d8:      	movq	0xe8(%rax), %rcx
 6c667df:      	movq	%rcx, 0x18(%rsp)
 6c667e4:      	movq	0x110(%rax), %rax
 6c667eb:      	movq	%rax, 0x8(%rsp)
 6c667f0:      	movq	(%rsp), %rax
 6c667f4:      	movq	0x10(%rax), %rbx
 6c667f8:      	movq	0x18(%rax), %rax
 6c667fc:      	subq	%rbx, %rax
 6c667ff:      	shrq	$0x3, %rax
 6c66803:      	movl	%eax, %r15d
 6c66806:      	movq	0x10(%rsp), %r14
 6c6680b:      	movq	0x68(%r14), %rsi
 6c6680f:      	leaq	0x60(%rsi), %rdi
 6c66813:      	callq	0x43c47b0 <_ZNK5clang12RedeclarableINS_7TagDeclEE8DeclLink11getPreviousEPKS1_>
 6c66818:      	movq	0x80(%r14), %rax
 6c6681f:      	movl	0x10(%rax), %eax
 6c66822:      	movl	0x180(%rsp), %ecx
 6c66829:      	cmpq	%rax, %r15
 6c6682c:      	setne	%dl
 6c6682f:      	testl	%ecx, %ecx
 6c66831:      	setne	%sil
 6c66835:      	andb	%dl, %sil
 6c66838:      	cmpb	$0x1, %sil
 6c6683c:      	jne	0x6c669e7 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x887>
 6c66842:      	movq	%r15, %rdi
 6c66845:      	movq	0x178(%rsp), %rdx
 6c6684d:      	movq	%rdx, 0x10(%rsp)
 6c66852:      	movl	%ecx, %r12d
 6c66855:      	shlq	$0x4, %r12
 6c66859:      	leaq	(%rbx,%rax,8), %rcx
 6c6685d:      	movq	%rcx, 0x90(%rsp)
 6c66865:      	shlq	$0x3, %rax
 6c66869:      	leaq	0x38(%rsp), %r14
 6c6686e:      	shlq	$0x3, %rdi
 6c66872:      	subq	%rax, %rdi
 6c66875:      	addq	$-0x8, %rdi
 6c66879:      	movq	%rdi, (%rsp)
 6c6687d:      	addq	$-0x10, %r12
 6c66881:      	xorl	%r15d, %r15d
 6c66884:      	nopw	%cs:(%rax,%rax)
 6c6688e:      	nop
 6c66890:      	movq	0x10(%rsp), %rax
 6c66895:      	movq	0x8(%rax,%r15,2), %rdi
 6c6689a:      	callq	0x7b8fb40 <_ZNK5clang4Stmt14getSourceRangeEv>
 6c6689f:      	movq	%rax, %rdi
 6c668a2:      	movl	$0x1, %esi
 6c668a7:      	movq	0x8(%rsp), %rdx
 6c668ac:      	movq	0x18(%rsp), %rcx
 6c668b1:      	xorl	%r8d, %r8d
 6c668b4:      	callq	0x7d60a10 <_ZN5clang5Lexer13getSourceTextENS_15CharSourceRangeERKNS_13SourceManagerERKNS_11LangOptionsEPb>
 6c668b9:      	movq	%rax, %rbp
 6c668bc:      	movq	%rdx, %rbx
 6c668bf:      	movq	0x90(%rsp), %rax
 6c668c7:      	movq	(%rax,%r15), %rdi
 6c668cb:      	callq	0x7b8fb40 <_ZNK5clang4Stmt14getSourceRangeEv>
 6c668d0:      	movq	%rax, %r13
 6c668d3:      	movq	%r14, 0x28(%rsp)
 6c668d8:      	testq	%rbp, %rbp
 6c668db:      	je	0x6c66920 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7c0>
 6c668dd:      	movq	%rbx, 0x20(%rsp)
 6c668e2:      	movq	%r14, %rax
 6c668e5:      	cmpq	$0x10, %rbx
 6c668e9:      	jb	0x6c6690b <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ab>
 6c668eb:      	leaq	0x28(%rsp), %rdi
 6c668f0:      	leaq	0x20(%rsp), %rsi
 6c668f5:      	xorl	%edx, %edx
 6c668f7:      	callq	0x828a680 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_createERmm@plt>
 6c668fc:      	movq	%rax, 0x28(%rsp)
 6c66901:      	movq	0x20(%rsp), %rcx
 6c66906:      	movq	%rcx, 0x38(%rsp)
 6c6690b:      	testq	%rbx, %rbx
 6c6690e:      	je	0x6c6694e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ee>
 6c66910:      	cmpq	$0x1, %rbx
 6c66914:      	jne	0x6c66940 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7e0>
 6c66916:      	movzbl	(%rbp), %ecx
 6c6691a:      	movb	%cl, (%rax)
 6c6691c:      	jmp	0x6c6694e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x7ee>
 6c6691e:      	nop
 6c66920:      	movq	$0x0, 0x30(%rsp)
 6c66929:      	movb	$0x0, 0x38(%rsp)
 6c6692e:      	xorl	%r8d, %r8d
 6c66931:      	movq	%r14, %rcx
 6c66934:      	jmp	0x6c6696b <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x80b>
 6c66936:      	nopw	%cs:(%rax,%rax)
 6c66940:      	movq	%rax, %rdi
 6c66943:      	movq	%rbp, %rsi
 6c66946:      	movq	%rbx, %rdx
 6c66949:      	callq	0x828ac50 <memcpy@plt>
 6c6694e:      	movq	0x20(%rsp), %rax
 6c66953:      	movq	%rax, 0x30(%rsp)
 6c66958:      	movq	0x28(%rsp), %rcx
 6c6695d:      	movb	$0x0, (%rcx,%rax)
 6c66961:      	movq	0x28(%rsp), %rcx
 6c66966:      	movq	0x30(%rsp), %r8
 6c6696b:      	leaq	0x138(%rsp), %rbx
 6c66973:      	movq	%rbx, %rdi
 6c66976:      	movq	%r13, %rsi
 6c66979:      	movl	$0x1, %edx
 6c6697e:      	callq	0x43f8800 <_ZN5clang9FixItHint17CreateReplacementENS_15CharSourceRangeEN4llvm9StringRefE>
 6c66983:      	movq	0x98(%rsp), %rdi
 6c6698b:      	movq	%rbx, %rsi
 6c6698e:      	callq	0x66d30b0 <_ZNK5clang8SemaBase21SemaDiagnosticBuilderlsINS_9FixItHintEvEERKS1_OT_>
 6c66993:      	movq	0x150(%rsp), %rdi
 6c6699b:      	leaq	0x160(%rsp), %rax
 6c669a3:      	cmpq	%rax, %rdi
 6c669a6:      	je	0x6c669b8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x858>
 6c669a8:      	movq	0x160(%rsp), %rsi
 6c669b0:      	incq	%rsi
 6c669b3:      	callq	0x828a660 <_ZdlPvm@plt>
 6c669b8:      	movq	0x28(%rsp), %rdi
 6c669bd:      	cmpq	%r14, %rdi
 6c669c0:      	je	0x6c669cf <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x86f>
 6c669c2:      	movq	0x38(%rsp), %rsi
 6c669c7:      	incq	%rsi
 6c669ca:      	callq	0x828a660 <_ZdlPvm@plt>
 6c669cf:      	cmpq	%r15, (%rsp)
 6c669d3:      	je	0x6c669e7 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x887>
 6c669d5:      	addq	$0x8, %r15
 6c669d9:      	testq	%r12, %r12
 6c669dc:      	leaq	-0x10(%r12), %r12
 6c669e1:      	jne	0x6c66890 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x730>
 6c669e7:      	movq	0xa0(%rsp), %rdi
 6c669ef:      	leaq	0xb8(%rsp), %rax
 6c669f7:      	cmpq	%rax, %rdi
 6c669fa:      	je	0x6c66a01 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8a1>
 6c669fc:      	callq	0x828a640 <free@plt>
 6c66a01:      	movq	0x178(%rsp), %rdi
 6c66a09:      	leaq	0x188(%rsp), %rax
 6c66a11:      	cmpq	%rax, %rdi
 6c66a14:      	je	0x6c66a1b <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8bb>
 6c66a16:      	callq	0x828a640 <free@plt>
 6c66a1b:      	testb	$0x1, 0x48(%rsp)
 6c66a20:      	jne	0x6c66a3e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8de>
 6c66a22:      	movl	0x58(%rsp), %esi
 6c66a26:      	testq	%rsi, %rsi
 6c66a29:      	je	0x6c66a3e <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x8de>
 6c66a2b:      	movq	0x50(%rsp), %rdi
 6c66a30:      	shlq	$0x4, %rsi
 6c66a34:      	movl	$0x8, %edx
 6c66a39:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 6c66a3e:      	addq	$0x288, %rsp            # imm = 0x288
 6c66a45:      	popq	%rbx
 6c66a46:      	popq	%r12
 6c66a48:      	popq	%r13
 6c66a4a:      	popq	%r14
 6c66a4c:      	popq	%r15
 6c66a4e:      	popq	%rbp
 6c66a4f:      	retq
 6c66a50:      	addq	$0x100, %r12            # imm = 0x100
 6c66a57:      	jmp	0x6c66a85 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x925>
 6c66a59:      	nopl	(%rax)
 6c66a60:      	movl	%eax, (%rcx)
 6c66a62:      	movq	0xa0(%rsp), %rax
 6c66a6a:      	movq	%rax, 0x4(%rcx)
 6c66a6e:      	movl	0xa8(%rsp), %eax
 6c66a75:      	movl	%eax, 0xc(%rcx)
 6c66a78:      	addq	$0x10, %r12
 6c66a7c:      	cmpq	%r13, %r12
 6c66a7f:      	je	0x6c66765 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66a85:      	movl	(%r12), %eax
 6c66a89:      	movl	0xc(%r12), %ecx
 6c66a8e:      	movl	%ecx, 0xa8(%rsp)
 6c66a95:      	movq	0x4(%r12), %rcx
 6c66a9a:      	movq	%rcx, 0xa0(%rsp)
 6c66aa2:      	movq	%r12, %rcx
 6c66aa5:      	cmpl	-0x10(%r12), %eax
 6c66aaa:      	jge	0x6c66a60 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x900>
 6c66aac:      	movq	%r12, %rcx
 6c66aaf:      	nop
 6c66ab0:      	movups	-0x10(%rcx), %xmm0
 6c66ab4:      	movups	%xmm0, (%rcx)
 6c66ab7:      	cmpl	-0x20(%rcx), %eax
 6c66aba:      	leaq	-0x10(%rcx), %rcx
 6c66abe:      	jl	0x6c66ab0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x950>
 6c66ac0:      	jmp	0x6c66a60 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x900>
 6c66ac2:      	movq	%r12, %rdi
 6c66ac5:      	jmp	0x6c66af8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x998>
 6c66ac7:      	nopw	(%rax,%rax)
 6c66ad0:      	movl	%eax, (%rcx)
 6c66ad2:      	movq	0xa0(%rsp), %rax
 6c66ada:      	movq	%rax, 0x4(%rcx)
 6c66ade:      	movl	0xa8(%rsp), %eax
 6c66ae5:      	movl	%eax, 0xc(%rcx)
 6c66ae8:      	leaq	0x10(%rbx), %rbp
 6c66aec:      	movq	%rbx, %rdi
 6c66aef:      	cmpq	%r13, %rbp
 6c66af2:      	je	0x6c66765 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66af8:      	movq	%rbp, %rbx
 6c66afb:      	movl	(%rbp), %eax
 6c66afe:      	cmpl	(%r12), %eax
 6c66b02:      	jge	0x6c66b60 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa00>
 6c66b04:      	movups	(%rbx), %xmm0
 6c66b07:      	movaps	%xmm0, 0xa0(%rsp)
 6c66b0f:      	movq	%rbx, %rdx
 6c66b12:      	subq	%r12, %rdx
 6c66b15:      	movq	%rdx, %rax
 6c66b18:      	sarq	$0x4, %rax
 6c66b1c:      	cmpq	$0x2, %rax
 6c66b20:      	jl	0x6c66ba5 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa45>
 6c66b26:      	shlq	$0x4, %rax
 6c66b2a:      	subq	%rax, %rdi
 6c66b2d:      	addq	$0x20, %rdi
 6c66b31:      	movq	%r12, %rsi
 6c66b34:      	callq	0x828abc0 <memmove@plt>
 6c66b39:      	movaps	0xa0(%rsp), %xmm0
 6c66b41:      	movups	%xmm0, (%r12)
 6c66b46:      	leaq	0x10(%rbx), %rbp
 6c66b4a:      	movq	%rbx, %rdi
 6c66b4d:      	cmpq	%r13, %rbp
 6c66b50:      	jne	0x6c66af8 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x998>
 6c66b52:      	jmp	0x6c66765 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x605>
 6c66b57:      	nopw	(%rax,%rax)
 6c66b60:      	movl	0x1c(%rdi), %ecx
 6c66b63:      	movl	%ecx, 0xa8(%rsp)
 6c66b6a:      	movq	0x14(%rdi), %rcx
 6c66b6e:      	movq	%rcx, 0xa0(%rsp)
 6c66b76:      	movq	%rbx, %rcx
 6c66b79:      	cmpl	(%rdi), %eax
 6c66b7b:      	jge	0x6c66ad0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x970>
 6c66b81:      	movq	%rbx, %rcx
 6c66b84:      	nopw	%cs:(%rax,%rax)
 6c66b8e:      	nop
 6c66b90:      	movups	-0x10(%rcx), %xmm0
 6c66b94:      	movups	%xmm0, (%rcx)
 6c66b97:      	cmpl	-0x20(%rcx), %eax
 6c66b9a:      	leaq	-0x10(%rcx), %rcx
 6c66b9e:      	jl	0x6c66b90 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0xa30>
 6c66ba0:      	jmp	0x6c66ad0 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x970>
 6c66ba5:      	cmpq	$0x10, %rdx
 6c66ba9:      	jne	0x6c66b39 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x9d9>
 6c66bab:      	movups	(%r12), %xmm0
 6c66bb0:      	movups	%xmm0, 0x10(%rdi)
 6c66bb4:      	jmp	0x6c66b39 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x9d9>
 6c66bb9:      	xorl	%eax, %eax
 6c66bbb:      	jmp	0x6c66265 <_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE+0x105>
