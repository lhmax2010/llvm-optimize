
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/toolchain/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000055f3ff0 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE>:
 55f3ff0:      	pushq	%rbp
 55f3ff1:      	pushq	%r15
 55f3ff3:      	pushq	%r14
 55f3ff5:      	pushq	%r13
 55f3ff7:      	pushq	%r12
 55f3ff9:      	pushq	%rbx
 55f3ffa:      	subq	$0x128, %rsp            # imm = 0x128
 55f4001:      	movq	%rdi, %rbx
 55f4004:      	movq	0x50(%rdi), %rdi
 55f4008:      	callq	0x556ed30 <_ZNK4llvm11VPBlockBase7getPlanEv>
 55f400d:      	leaq	0x100(%rsp), %rdi
 55f4015:      	movq	%rax, %rsi
 55f4018:      	callq	0x55a8110 <_ZN4llvm14VPTypeAnalysisC2ERKNS_5VPlanE>
 55f401d:      	movzbl	0x8(%rbx), %edx
 55f4021:      	cmpl	$0x5, %edx
 55f4024:      	setne	%al
 55f4027:      	testq	%rbx, %rbx
 55f402a:      	sete	%cl
 55f402d:      	orb	%al, %cl
 55f402f:      	movq	%rdx, 0x30(%rsp)
 55f4034:      	je	0x55f405b <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6b>
 55f4036:      	leal	-0xa(%rdx), %eax
 55f4039:      	cmpl	$0xd, %eax
 55f403c:      	ja	0x55f4704 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x714>
 55f4042:      	leaq	-0x38a81cd(%rip), %rcx  # 0x1d4be7c <_ZTSN4llvm18VPExpandSCEVRecipeE+0x16f0>
 55f4049:      	movslq	(%rcx,%rax,4), %rax
 55f404d:      	addq	%rcx, %rax
 55f4050:      	jmpq	*%rax
 55f4052:      	movl	0xe8(%rbx), %r14d
 55f4059:      	jmp	0x55f4063 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x73>
 55f405b:      	movzbl	0xe8(%rbx), %r14d
 55f4063:      	shlq	$0x20, %r14
 55f4067:      	movb	$0x1, 0xe(%rsp)
 55f406c:      	movq	$0x0, 0x10(%rsp)
 55f4075:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 55f407f:      	movabsq	$-0x622015f714c7d297, %r12 # imm = 0x9DDFEA08EB382D69
 55f4089:      	leaq	0x60(%rbx), %r15
 55f408d:      	leaq	0x100(%rsp), %rdi
 55f4095:      	movq	%r15, %rsi
 55f4098:      	callq	0x55a82f0 <_ZN4llvm14VPTypeAnalysis15inferScalarTypeEPKNS_7VPValueE>
 55f409d:      	movq	%rax, 0x70(%rsp)
 55f40a2:      	movq	%r15, %rdi
 55f40a5:      	callq	0x55a5250 <_ZN4llvm7vputils14isSingleScalarEPKNS_7VPValueE>
 55f40aa:      	movb	%al, 0xf(%rsp)
 55f40ae:      	movq	0x30(%rbx), %rdi
 55f40b2:      	movl	0x38(%rbx), %eax
 55f40b5:      	leaq	(,%rax,8), %rsi
 55f40bd:      	cmpq	$0x8, %rax
 55f40c1:      	ja	0x55f40d8 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0xe8>
 55f40c3:      	movq	%rbp, %rdx
 55f40c6:      	callq	0x2ac8fc0 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 55f40cb:      	movq	%rax, %r13
 55f40ce:      	movq	0x30(%rsp), %r9
 55f40d3:      	jmp	0x55f4483 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x493>
 55f40d8:      	movq	%rax, 0x60(%rsp)
 55f40dd:      	movq	%r14, 0x38(%rsp)
 55f40e2:      	movq	%rbx, 0x68(%rsp)
 55f40e7:      	movabsq	$-0x4b6d499041670d8d, %r8 # imm = 0xB492B66FBE98F273
 55f40f1:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 55f40fb:      	movq	%rsi, %r15
 55f40fe:      	andq	$-0x40, %r15
 55f4102:      	movq	0x8(%rdi), %r14
 55f4106:      	movq	0x10(%rdi), %rax
 55f410a:      	movabsq	$-0x73d22641534b4d52, %rsi # imm = 0x8C2DD9BEACB4B2AE
 55f4114:      	addq	%r14, %rsi
 55f4117:      	rolq	$0x1b, %rsi
 55f411b:      	imulq	%r8, %rsi
 55f411f:      	movq	0x30(%rdi), %rdx
 55f4123:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 55f412d:      	addq	%rdx, %r9
 55f4130:      	rolq	$0x16, %r9
 55f4134:      	imulq	%r8, %r9
 55f4138:      	movabsq	$-0x85335acd9bb6c6a, %r13 # imm = 0xF7ACCA5326449396
 55f4142:      	xorq	%rsi, %r13
 55f4145:      	movq	0x28(%rdi), %r10
 55f4149:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 55f4153:      	addq	%r10, %r8
 55f4156:      	addq	%r9, %r8
 55f4159:      	movabsq	$0x298df016a9f64655, %rsi # imm = 0x298DF016A9F64655
 55f4163:      	addq	(%rdi), %rsi
 55f4166:      	leaq	(%rbp,%rsi), %r9
 55f416b:      	addq	%r13, %r9
 55f416e:      	movq	0x18(%rdi), %r11
 55f4172:      	leaq	-0x11a5f(%r11,%r9), %rbx
 55f417a:      	rolq	$0x2b, %rbx
 55f417e:      	addq	%rax, %r14
 55f4181:      	addq	%rsi, %r14
 55f4184:      	movq	%r14, %r9
 55f4187:      	rolq	$0x14, %r9
 55f418b:      	addq	%rsi, %r9
 55f418e:      	addq	%rbx, %r9
 55f4191:      	movabsq	$0x4bf62cb950c3753a, %rsi # imm = 0x4BF62CB950C3753A
 55f419b:      	addq	0x20(%rdi), %rsi
 55f419f:      	addq	%r11, %r14
 55f41a2:      	movq	%rdi, 0x40(%rsp)
 55f41a7:      	movq	0x38(%rdi), %r11
 55f41ab:      	addq	%rsi, %rax
 55f41ae:      	addq	%r11, %rax
 55f41b1:      	addq	%r8, %rax
 55f41b4:      	rolq	$0x2b, %rax
 55f41b8:      	addq	%rdx, %r10
 55f41bb:      	addq	%rsi, %r10
 55f41be:      	movq	%r10, %r12
 55f41c1:      	rolq	$0x14, %r12
 55f41c5:      	addq	%rsi, %r12
 55f41c8:      	addq	%rax, %r12
 55f41cb:      	addq	%r11, %r10
 55f41ce:      	movq	%r15, 0x48(%rsp)
 55f41d3:      	cmpq	$0x40, %r15
 55f41d7:      	jne	0x55f41ed <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x1fd>
 55f41d9:      	movq	%r12, %rdx
 55f41dc:      	movq	%r10, %r11
 55f41df:      	movq	%r9, %rbx
 55f41e2:      	movq	%r14, %r15
 55f41e5:      	movq	%r13, %rsi
 55f41e8:      	jmp	0x55f42dd <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x2ed>
 55f41ed:      	addq	$-0x40, 0x48(%rsp)
 55f41f3:      	xorl	%eax, %eax
 55f41f5:      	movq	0x40(%rsp), %rdi
 55f41fa:      	nopw	(%rax,%rax)
 55f4200:      	addq	%r8, %rcx
 55f4203:      	addq	%r14, %rcx
 55f4206:      	movq	0x48(%rdi,%rax), %r15
 55f420b:      	movq	0x50(%rdi,%rax), %rbp
 55f4210:      	addq	%r15, %rcx
 55f4213:      	rolq	$0x1b, %rcx
 55f4217:      	movabsq	$-0x4b6d499041670d8d, %rdx # imm = 0xB492B66FBE98F273
 55f4221:      	imulq	%rdx, %rcx
 55f4225:      	addq	%r9, %r8
 55f4228:      	movq	0x70(%rdi,%rax), %rsi
 55f422d:      	movq	%rsi, 0x78(%rsp)
 55f4232:      	addq	%rsi, %r8
 55f4235:      	rolq	$0x16, %r8
 55f4239:      	imulq	%rdx, %r8
 55f423d:      	movq	%rcx, %rsi
 55f4240:      	xorq	%r12, %rsi
 55f4243:      	movq	0x68(%rdi,%rax), %r11
 55f4248:      	addq	%r11, %r14
 55f424b:      	addq	%r10, %r13
 55f424e:      	rolq	$0x1f, %r13
 55f4252:      	addq	%r14, %r8
 55f4255:      	imulq	%rdx, %r9
 55f4259:      	addq	0x40(%rdi,%rax), %r9
 55f425e:      	movq	%r13, %rcx
 55f4261:      	movq	0x58(%rdi,%rax), %r14
 55f4266:      	addq	%r9, %r10
 55f4269:      	addq	%r14, %r10
 55f426c:      	addq	%rsi, %r10
 55f426f:      	rolq	$0x2b, %r10
 55f4273:      	addq	%rbp, %r15
 55f4276:      	addq	%r9, %r15
 55f4279:      	movq	%r15, %rbx
 55f427c:      	rolq	$0x14, %rbx
 55f4280:      	imulq	%rdx, %rcx
 55f4284:      	addq	%r9, %rbx
 55f4287:      	addq	%r10, %rbx
 55f428a:      	addq	%rcx, %r12
 55f428d:      	addq	%r8, %rbp
 55f4290:      	addq	0x60(%rdi,%rax), %r12
 55f4295:      	movq	0x78(%rdi,%rax), %r9
 55f429a:      	addq	%r12, %rbp
 55f429d:      	addq	%r9, %rbp
 55f42a0:      	rolq	$0x2b, %rbp
 55f42a4:      	addq	%r14, %r15
 55f42a7:      	addq	0x78(%rsp), %r11
 55f42ac:      	addq	%r12, %r11
 55f42af:      	movq	%r11, %rdx
 55f42b2:      	rolq	$0x14, %rdx
 55f42b6:      	addq	%r12, %rdx
 55f42b9:      	addq	%rbp, %rdx
 55f42bc:      	addq	%r9, %r11
 55f42bf:      	addq	$0x40, %rax
 55f42c3:      	movq	%rsi, %r13
 55f42c6:      	movq	%r15, %r14
 55f42c9:      	movq	%rbx, %r9
 55f42cc:      	movq	%r11, %r10
 55f42cf:      	movq	%rdx, %r12
 55f42d2:      	cmpq	%rax, 0x48(%rsp)
 55f42d7:      	jne	0x55f4200 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x210>
 55f42dd:      	movq	0x60(%rsp), %r13
 55f42e2:      	testb	$0x7, %r13b
 55f42e6:      	je	0x55f43c5 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x3d5>
 55f42ec:      	leaq	(%r8,%r15), %r10
 55f42f0:      	movq	0x40(%rsp), %rdi
 55f42f5:      	movq	-0x38(%rdi,%r13,8), %rax
 55f42fa:      	movq	-0x30(%rdi,%r13,8), %r9
 55f42ff:      	addq	%rax, %rcx
 55f4302:      	addq	%r10, %rcx
 55f4305:      	rolq	$0x1b, %rcx
 55f4309:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 55f4313:      	imulq	%rbp, %rcx
 55f4317:      	addq	%rbx, %r8
 55f431a:      	movq	-0x10(%rdi,%r13,8), %r14
 55f431f:      	addq	%r14, %r8
 55f4322:      	rolq	$0x16, %r8
 55f4326:      	imulq	%rbp, %r8
 55f432a:      	xorq	%rdx, %rcx
 55f432d:      	movq	-0x18(%rdi,%r13,8), %r10
 55f4332:      	addq	%r10, %r15
 55f4335:      	addq	%r15, %r8
 55f4338:      	addq	%r11, %rsi
 55f433b:      	rolq	$0x1f, %rsi
 55f433f:      	movq	%rsi, %r12
 55f4342:      	imulq	%rbp, %rbx
 55f4346:      	addq	%rcx, %r11
 55f4349:      	addq	-0x40(%rdi,%r13,8), %rbx
 55f434e:      	movq	-0x28(%rdi,%r13,8), %r15
 55f4353:      	addq	%r15, %r11
 55f4356:      	addq	%rbx, %r11
 55f4359:      	rolq	$0x2b, %r11
 55f435d:      	imulq	%rbp, %r12
 55f4361:      	addq	%r9, %rax
 55f4364:      	addq	%rbx, %rax
 55f4367:      	movq	%rax, %rsi
 55f436a:      	rolq	$0x14, %rsi
 55f436e:      	addq	%rbx, %rsi
 55f4371:      	addq	%r11, %rsi
 55f4374:      	addq	%r15, %rax
 55f4377:      	addq	%r12, %rdx
 55f437a:      	addq	-0x20(%rdi,%r13,8), %rdx
 55f437f:      	addq	%r8, %r9
 55f4382:      	movq	-0x8(%rdi,%r13,8), %rdi
 55f4387:      	addq	%rdi, %r9
 55f438a:      	addq	%rdx, %r9
 55f438d:      	rolq	$0x2b, %r9
 55f4391:      	addq	%r14, %r10
 55f4394:      	addq	%rdx, %r10
 55f4397:      	movq	%r10, %r11
 55f439a:      	rolq	$0x14, %r11
 55f439e:      	addq	%rdx, %r11
 55f43a1:      	addq	%r9, %r11
 55f43a4:      	addq	%rdi, %r10
 55f43a7:      	movq	%r11, %rdx
 55f43aa:      	movq	%r10, %r11
 55f43ad:      	movq	%rsi, %rbx
 55f43b0:      	movq	%rax, %r15
 55f43b3:      	movq	%rcx, %rsi
 55f43b6:      	movq	%r12, %rcx
 55f43b9:      	movq	0x30(%rsp), %r9
 55f43be:      	movq	0x38(%rsp), %r14
 55f43c3:      	jmp	0x55f43d9 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x3e9>
 55f43c5:      	movq	0x30(%rsp), %r9
 55f43ca:      	movq	0x38(%rsp), %r14
 55f43cf:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 55f43d9:      	xorq	%r11, %r15
 55f43dc:      	movabsq	$-0x622015f714c7d297, %r12 # imm = 0x9DDFEA08EB382D69
 55f43e6:      	imulq	%r12, %r15
 55f43ea:      	xorq	%r15, %r11
 55f43ed:      	shrq	$0x2f, %r15
 55f43f1:      	xorq	%r11, %r15
 55f43f4:      	imulq	%r12, %r15
 55f43f8:      	movq	%r15, %rdi
 55f43fb:      	shrq	$0x2f, %rdi
 55f43ff:      	xorq	%r15, %rdi
 55f4402:      	imulq	%r12, %rdi
 55f4406:      	movq	%r8, %rax
 55f4409:      	shrq	$0x2f, %rax
 55f440d:      	xorq	%r8, %rax
 55f4410:      	imulq	%rbp, %rax
 55f4414:      	addq	%rsi, %rax
 55f4417:      	addq	%rdi, %rax
 55f441a:      	xorq	%rdx, %rbx
 55f441d:      	imulq	%r12, %rbx
 55f4421:      	xorq	%rbx, %rdx
 55f4424:      	shrq	$0x2f, %rbx
 55f4428:      	xorq	%rdx, %rbx
 55f442b:      	imulq	%r12, %rbx
 55f442f:      	movq	%rbx, %rdx
 55f4432:      	shrq	$0x2f, %rdx
 55f4436:      	xorq	%rbx, %rdx
 55f4439:      	imulq	%r12, %rdx
 55f443d:      	movabsq	$-0x5b6a4c820b386c68, %rsi # imm = 0xA495B37DF4C79398
 55f4447:      	imulq	%rsi, %r13
 55f444b:      	addq	%rcx, %r13
 55f444e:      	addq	%rdx, %r13
 55f4451:      	xorq	%r13, %rax
 55f4454:      	imulq	%r12, %rax
 55f4458:      	xorq	%rax, %r13
 55f445b:      	shrq	$0x2f, %rax
 55f445f:      	xorq	%r13, %rax
 55f4462:      	imulq	%r12, %rax
 55f4466:      	movq	%rax, %r13
 55f4469:      	shrq	$0x2f, %r13
 55f446d:      	xorq	%rax, %r13
 55f4470:      	imulq	%r12, %r13
 55f4474:      	movq	0x68(%rsp), %rbx
 55f4479:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 55f4483:      	xorps	%xmm0, %xmm0
 55f4486:      	movups	%xmm0, 0xe8(%rsp)
 55f448e:      	movups	%xmm0, 0xd8(%rsp)
 55f4496:      	movups	%xmm0, 0xc8(%rsp)
 55f449e:      	movups	%xmm0, 0xb8(%rsp)
 55f44a6:      	movups	%xmm0, 0xa8(%rsp)
 55f44ae:      	movups	%xmm0, 0x98(%rsp)
 55f44b6:      	movups	%xmm0, 0x88(%rsp)
 55f44be:      	movq	%rbp, 0xf8(%rsp)
 55f44c6:      	leaq	0xc0(%rsp), %r15
 55f44ce:      	movl	%r9d, 0x80(%rsp)
 55f44d6:      	cmpb	$0x0, 0xe(%rsp)
 55f44db:      	je	0x55f4563 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x573>
 55f44e1:      	movb	$0x1, 0x20(%rsp)
 55f44e6:      	movb	%r14b, 0x18(%rsp)
 55f44eb:      	shrq	$0x20, %r14
 55f44ef:      	movl	%r14d, 0x19(%rsp)
 55f44f4:      	movl	0x18(%rsp), %eax
 55f44f8:      	leaq	0x5(,%rax,8), %rcx
 55f4500:      	xorq	%rbp, %r14
 55f4503:      	xorq	%r14, %rcx
 55f4506:      	imulq	%r12, %rcx
 55f450a:      	xorq	%rcx, %r14
 55f450d:      	shrq	$0x2f, %rcx
 55f4511:      	xorq	%r14, %rcx
 55f4514:      	imulq	%r12, %rcx
 55f4518:      	movq	%rcx, %rax
 55f451b:      	shrq	$0x2f, %rax
 55f451f:      	xorq	%rcx, %rax
 55f4522:      	imulq	%r12, %rax
 55f4526:      	movq	%rax, 0x21(%rsp)
 55f452b:      	leaq	0x9(%rax), %rcx
 55f452f:      	rolq	$0x37, %rcx
 55f4533:      	movq	0x20(%rsp), %rdx
 55f4538:      	xorq	%rcx, %rdx
 55f453b:      	xorq	%rbp, %rdx
 55f453e:      	imulq	%r12, %rdx
 55f4542:      	xorq	%rdx, %rcx
 55f4545:      	shrq	$0x2f, %rdx
 55f4549:      	xorq	%rcx, %rdx
 55f454c:      	imulq	%r12, %rdx
 55f4550:      	movq	%rdx, %rcx
 55f4553:      	shrq	$0x2f, %rcx
 55f4557:      	xorq	%rdx, %rcx
 55f455a:      	imulq	%r12, %rcx
 55f455e:      	xorq	%rax, %rcx
 55f4561:      	jmp	0x55f456d <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x57d>
 55f4563:      	movabsq	$-0x4d4db097723be9b3, %rcx # imm = 0xB2B24F688DC4164D
 55f456d:      	leaq	0x8c(%rsp), %rdx
 55f4575:      	movq	%rcx, 0x84(%rsp)
 55f457d:      	movq	$0x0, 0x50(%rsp)
 55f4586:      	leaq	0x80(%rsp), %rbp
 55f458e:      	leaq	0x50(%rsp), %rsi
 55f4593:      	movq	%rbp, %rdi
 55f4596:      	movq	%r15, %rcx
 55f4599:      	movq	0x10(%rsp), %r8
 55f459e:      	callq	0x3b017b0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIPNS_4TypeEEEPcRmS6_S6_T_>
 55f45a3:      	movq	0x50(%rsp), %rcx
 55f45a8:      	movq	%rcx, 0x58(%rsp)
 55f45ad:      	leaq	0x58(%rsp), %rsi
 55f45b2:      	movq	%rbp, %rdi
 55f45b5:      	movq	%rax, %rdx
 55f45b8:      	movq	%r15, %rcx
 55f45bb:      	movq	0x70(%rsp), %r8
 55f45c0:      	callq	0x3b017b0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIPNS_4TypeEEEPcRmS6_S6_T_>
 55f45c5:      	movq	0x58(%rsp), %rcx
 55f45ca:      	movq	%rcx, 0x18(%rsp)
 55f45cf:      	movzbl	0xf(%rsp), %r8d
 55f45d5:      	leaq	0x18(%rsp), %rsi
 55f45da:      	movq	%rbp, %rdi
 55f45dd:      	movq	%rax, %rdx
 55f45e0:      	movq	%r15, %rcx
 55f45e3:      	callq	0x36843d0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIbEEPcRmS4_S4_T_>
 55f45e8:      	movq	0x18(%rsp), %rcx
 55f45ed:      	movq	%rcx, 0x20(%rsp)
 55f45f2:      	leaq	0x20(%rsp), %rsi
 55f45f7:      	movq	%rbp, %rdi
 55f45fa:      	movq	%rax, %rdx
 55f45fd:      	movq	%r15, %rcx
 55f4600:      	movq	%r13, %r8
 55f4603:      	callq	0x2ac8b20 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataImEEPcRmS4_S4_T_>
 55f4608:      	movq	0x20(%rsp), %rsi
 55f460d:      	movq	%rbp, %rdi
 55f4610:      	movq	%rax, %rdx
 55f4613:      	movq	%r15, %rcx
 55f4616:      	callq	0x2ac8df0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 55f461b:      	movq	%rax, %r15
 55f461e:      	movzbl	0x8(%rbx), %eax
 55f4622:      	cmpl	$0x17, %eax
 55f4625:      	ja	0x55f4695 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a5>
 55f4627:      	movl	$0x877720, %ecx         # imm = 0x877720
 55f462c:      	btl	%eax, %ecx
 55f462f:      	jae	0x55f4695 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a5>
 55f4631:      	cmpb	$0x1, 0x98(%rbx)
 55f4638:      	ja	0x55f4695 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a5>
 55f463a:      	movl	0x9c(%rbx), %eax
 55f4640:      	movq	%r15, 0x80(%rsp)
 55f4648:      	movl	%eax, 0x88(%rsp)
 55f464f:      	movq	0x84(%rsp), %rax
 55f4657:      	leaq	0xc(%rax), %rcx
 55f465b:      	rolq	$0x34, %rcx
 55f465f:      	movabsq	$-0xae502812aa7333, %rdx # imm = 0xFF51AFD7ED558CCD
 55f4669:      	xorq	%rcx, %rdx
 55f466c:      	xorq	%rdx, %r15
 55f466f:      	imulq	%r12, %r15
 55f4673:      	xorq	%r15, %rcx
 55f4676:      	shrq	$0x2f, %r15
 55f467a:      	xorq	%rcx, %r15
 55f467d:      	imulq	%r12, %r15
 55f4681:      	movq	%r15, %rcx
 55f4684:      	shrq	$0x2f, %rcx
 55f4688:      	xorq	%r15, %rcx
 55f468b:      	imulq	%r12, %rcx
 55f468f:      	xorq	%rax, %rcx
 55f4692:      	movq	%rcx, %r15
 55f4695:      	movq	0x100(%rsp), %rdi
 55f469d:      	movl	0x110(%rsp), %esi
 55f46a4:      	shlq	$0x4, %rsi
 55f46a8:      	movl	$0x8, %edx
 55f46ad:      	callq	0x828af90 <_ZdlPvmSt11align_val_t@plt>
 55f46b2:      	movl	%r15d, %eax
 55f46b5:      	addq	$0x128, %rsp            # imm = 0x128
 55f46bc:      	popq	%rbx
 55f46bd:      	popq	%r12
 55f46bf:      	popq	%r13
 55f46c1:      	popq	%r14
 55f46c3:      	popq	%r15
 55f46c5:      	popq	%rbp
 55f46c6:      	retq
 55f46c7:      	movl	0xe8(%rbx), %r14d
 55f46ce:      	shlq	$0x20, %r14
 55f46d2:      	incq	%r14
 55f46d5:      	jmp	0x55f4067 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x77>
 55f46da:      	movq	0x88(%rbx), %rax
 55f46e1:      	movzbl	(%rax), %eax
 55f46e4:      	shlq	$0x20, %rax
 55f46e8:      	movabsq	$-0x1d00000000, %r14    # imm = 0xFFFFFFE300000000
 55f46f2:      	addq	%rax, %r14
 55f46f5:      	movb	$0x1, 0xe(%rsp)
 55f46fa:      	testq	%rbx, %rbx
 55f46fd:      	jne	0x55f4731 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x741>
 55f46ff:      	jmp	0x55f406c <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f4704:      	testq	%rbx, %rbx
 55f4707:      	sete	%al
 55f470a:      	movabsq	$0x8400000000, %r14     # imm = 0x8400000000
 55f4714:      	cmpl	$0x1c, %edx
 55f4717:      	sete	0xe(%rsp)
 55f471c:      	cmpl	$0xa, %edx
 55f471f:      	setne	%cl
 55f4722:      	orb	%al, %cl
 55f4724:      	je	0x55f4731 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x741>
 55f4726:      	cmpl	$0xc, %edx
 55f4729:      	jne	0x55f406c <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f472f:      	jmp	0x55f475e <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x76e>
 55f4731:      	movq	0x88(%rbx), %rax
 55f4738:      	cmpb	$0x3f, (%rax)
 55f473b:      	jne	0x55f406c <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f4741:      	movq	0x48(%rax), %rax
 55f4745:      	movq	%rax, 0x10(%rsp)
 55f474a:      	jmp	0x55f4075 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
 55f474f:      	movabsq	$0x7400000000, %r14     # imm = 0x7400000000
 55f4759:      	movb	$0x1, 0xe(%rsp)
 55f475e:      	movq	0xa8(%rbx), %rax
 55f4765:      	movq	%rax, 0x10(%rsp)
 55f476a:      	jmp	0x55f4075 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
 55f476f:      	movq	0xa8(%rbx), %rax
 55f4776:      	movq	%rax, 0x10(%rsp)
 55f477b:      	movb	$0x1, 0xe(%rsp)
 55f4780:      	movabsq	$0x2200000000, %r14     # imm = 0x2200000000
 55f478a:      	jmp	0x55f4075 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
