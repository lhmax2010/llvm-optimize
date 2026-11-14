
/home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22:	file format elf64-x86-64

Disassembly of section .text:

00000000055f3f60 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE>:
 55f3f60:      	pushq	%rbp
 55f3f61:      	pushq	%r15
 55f3f63:      	pushq	%r14
 55f3f65:      	pushq	%r13
 55f3f67:      	pushq	%r12
 55f3f69:      	pushq	%rbx
 55f3f6a:      	subq	$0x128, %rsp            # imm = 0x128
 55f3f71:      	movq	%rdi, %rbx
 55f3f74:      	movq	0x50(%rdi), %rdi
 55f3f78:      	callq	0x556eca0 <_ZNK4llvm11VPBlockBase7getPlanEv>
 55f3f7d:      	leaq	0x100(%rsp), %rdi
 55f3f85:      	movq	%rax, %rsi
 55f3f88:      	callq	0x55a8080 <_ZN4llvm14VPTypeAnalysisC2ERKNS_5VPlanE>
 55f3f8d:      	movzbl	0x8(%rbx), %edx
 55f3f91:      	cmpl	$0x5, %edx
 55f3f94:      	setne	%al
 55f3f97:      	testq	%rbx, %rbx
 55f3f9a:      	sete	%cl
 55f3f9d:      	orb	%al, %cl
 55f3f9f:      	movq	%rdx, 0x30(%rsp)
 55f3fa4:      	je	0x55f3fcb <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6b>
 55f3fa6:      	leal	-0xa(%rdx), %eax
 55f3fa9:      	cmpl	$0xd, %eax
 55f3fac:      	ja	0x55f4673 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x713>
 55f3fb2:      	leaq	-0x38a813d(%rip), %rcx  # 0x1d4be7c <_ZTSN4llvm18VPExpandSCEVRecipeE+0x16f0>
 55f3fb9:      	movslq	(%rcx,%rax,4), %rax
 55f3fbd:      	addq	%rcx, %rax
 55f3fc0:      	jmpq	*%rax
 55f3fc2:      	movl	0xe8(%rbx), %r14d
 55f3fc9:      	jmp	0x55f3fd3 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x73>
 55f3fcb:      	movzbl	0xe8(%rbx), %r14d
 55f3fd3:      	shlq	$0x20, %r14
 55f3fd7:      	movb	$0x1, 0xe(%rsp)
 55f3fdc:      	movq	$0x0, 0x10(%rsp)
 55f3fe5:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 55f3fef:      	movabsq	$-0x622015f714c7d297, %r12 # imm = 0x9DDFEA08EB382D69
 55f3ff9:      	leaq	0x60(%rbx), %r15
 55f3ffd:      	leaq	0x100(%rsp), %rdi
 55f4005:      	movq	%r15, %rsi
 55f4008:      	callq	0x55a8260 <_ZN4llvm14VPTypeAnalysis15inferScalarTypeEPKNS_7VPValueE>
 55f400d:      	movq	%rax, 0x70(%rsp)
 55f4012:      	movq	%r15, %rdi
 55f4015:      	callq	0x55a51c0 <_ZN4llvm7vputils14isSingleScalarEPKNS_7VPValueE>
 55f401a:      	movb	%al, 0xf(%rsp)
 55f401e:      	movq	0x30(%rbx), %rdi
 55f4022:      	movl	0x38(%rbx), %eax
 55f4025:      	leaq	(,%rax,8), %rsi
 55f402d:      	cmpq	$0x8, %rax
 55f4031:      	ja	0x55f4048 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0xe8>
 55f4033:      	movq	%rbp, %rdx
 55f4036:      	callq	0x2ac8f60 <_ZN4llvm7hashing6detail10hash_shortEPKcmm>
 55f403b:      	movq	%rax, %r13
 55f403e:      	movq	0x30(%rsp), %r9
 55f4043:      	jmp	0x55f43f2 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x492>
 55f4048:      	movq	%rax, 0x60(%rsp)
 55f404d:      	movq	%r14, 0x38(%rsp)
 55f4052:      	movq	%rbx, 0x68(%rsp)
 55f4057:      	movabsq	$-0x4b6d499041670d8d, %r8 # imm = 0xB492B66FBE98F273
 55f4061:      	movabsq	$0x544962662a7ee1a4, %rcx # imm = 0x544962662A7EE1A4
 55f406b:      	movq	%rsi, %r15
 55f406e:      	andq	$-0x40, %r15
 55f4072:      	movq	0x8(%rdi), %r14
 55f4076:      	movq	0x10(%rdi), %rax
 55f407a:      	movabsq	$-0x73d22641534b4d52, %rsi # imm = 0x8C2DD9BEACB4B2AE
 55f4084:      	addq	%r14, %rsi
 55f4087:      	rolq	$0x1b, %rsi
 55f408b:      	imulq	%r8, %rsi
 55f408f:      	movq	0x30(%rdi), %rdx
 55f4093:      	movabsq	$-0x414bff9ed66a691c, %r9 # imm = 0xBEB40061299596E4
 55f409d:      	addq	%rdx, %r9
 55f40a0:      	rolq	$0x16, %r9
 55f40a4:      	imulq	%r8, %r9
 55f40a8:      	movabsq	$-0x85335acd9bb6c6a, %r13 # imm = 0xF7ACCA5326449396
 55f40b2:      	xorq	%rsi, %r13
 55f40b5:      	movq	0x28(%rdi), %r10
 55f40b9:      	movabsq	$-0x7323d61940a0da1f, %r8 # imm = 0x8CDC29E6BF5F25E1
 55f40c3:      	addq	%r10, %r8
 55f40c6:      	addq	%r9, %r8
 55f40c9:      	movabsq	$0x298df016a9f64655, %rsi # imm = 0x298DF016A9F64655
 55f40d3:      	addq	(%rdi), %rsi
 55f40d6:      	leaq	(%rbp,%rsi), %r9
 55f40db:      	addq	%r13, %r9
 55f40de:      	movq	0x18(%rdi), %r11
 55f40e2:      	leaq	-0x11a5f(%r11,%r9), %rbx
 55f40ea:      	rolq	$0x2b, %rbx
 55f40ee:      	addq	%rax, %r14
 55f40f1:      	addq	%rsi, %r14
 55f40f4:      	movq	%r14, %r9
 55f40f7:      	rolq	$0x14, %r9
 55f40fb:      	addq	%rsi, %r9
 55f40fe:      	addq	%rbx, %r9
 55f4101:      	movabsq	$0x4bf62cb950c3753a, %rsi # imm = 0x4BF62CB950C3753A
 55f410b:      	addq	0x20(%rdi), %rsi
 55f410f:      	addq	%r11, %r14
 55f4112:      	movq	%rdi, 0x40(%rsp)
 55f4117:      	movq	0x38(%rdi), %r11
 55f411b:      	addq	%rsi, %rax
 55f411e:      	addq	%r11, %rax
 55f4121:      	addq	%r8, %rax
 55f4124:      	rolq	$0x2b, %rax
 55f4128:      	addq	%rdx, %r10
 55f412b:      	addq	%rsi, %r10
 55f412e:      	movq	%r10, %r12
 55f4131:      	rolq	$0x14, %r12
 55f4135:      	addq	%rsi, %r12
 55f4138:      	addq	%rax, %r12
 55f413b:      	addq	%r11, %r10
 55f413e:      	movq	%r15, 0x48(%rsp)
 55f4143:      	cmpq	$0x40, %r15
 55f4147:      	jne	0x55f415d <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x1fd>
 55f4149:      	movq	%r12, %rdx
 55f414c:      	movq	%r10, %r11
 55f414f:      	movq	%r9, %rbx
 55f4152:      	movq	%r14, %r15
 55f4155:      	movq	%r13, %rsi
 55f4158:      	jmp	0x55f424d <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x2ed>
 55f415d:      	addq	$-0x40, 0x48(%rsp)
 55f4163:      	xorl	%eax, %eax
 55f4165:      	movq	0x40(%rsp), %rdi
 55f416a:      	nopw	(%rax,%rax)
 55f4170:      	addq	%r8, %rcx
 55f4173:      	addq	%r14, %rcx
 55f4176:      	movq	0x48(%rdi,%rax), %r15
 55f417b:      	movq	0x50(%rdi,%rax), %rbp
 55f4180:      	addq	%r15, %rcx
 55f4183:      	rolq	$0x1b, %rcx
 55f4187:      	movabsq	$-0x4b6d499041670d8d, %rdx # imm = 0xB492B66FBE98F273
 55f4191:      	imulq	%rdx, %rcx
 55f4195:      	addq	%r9, %r8
 55f4198:      	movq	0x70(%rdi,%rax), %rsi
 55f419d:      	movq	%rsi, 0x78(%rsp)
 55f41a2:      	addq	%rsi, %r8
 55f41a5:      	rolq	$0x16, %r8
 55f41a9:      	imulq	%rdx, %r8
 55f41ad:      	movq	%rcx, %rsi
 55f41b0:      	xorq	%r12, %rsi
 55f41b3:      	movq	0x68(%rdi,%rax), %r11
 55f41b8:      	addq	%r11, %r14
 55f41bb:      	addq	%r10, %r13
 55f41be:      	rolq	$0x1f, %r13
 55f41c2:      	addq	%r14, %r8
 55f41c5:      	imulq	%rdx, %r9
 55f41c9:      	addq	0x40(%rdi,%rax), %r9
 55f41ce:      	movq	%r13, %rcx
 55f41d1:      	movq	0x58(%rdi,%rax), %r14
 55f41d6:      	addq	%r9, %r10
 55f41d9:      	addq	%r14, %r10
 55f41dc:      	addq	%rsi, %r10
 55f41df:      	rolq	$0x2b, %r10
 55f41e3:      	addq	%rbp, %r15
 55f41e6:      	addq	%r9, %r15
 55f41e9:      	movq	%r15, %rbx
 55f41ec:      	rolq	$0x14, %rbx
 55f41f0:      	imulq	%rdx, %rcx
 55f41f4:      	addq	%r9, %rbx
 55f41f7:      	addq	%r10, %rbx
 55f41fa:      	addq	%rcx, %r12
 55f41fd:      	addq	%r8, %rbp
 55f4200:      	addq	0x60(%rdi,%rax), %r12
 55f4205:      	movq	0x78(%rdi,%rax), %r9
 55f420a:      	addq	%r12, %rbp
 55f420d:      	addq	%r9, %rbp
 55f4210:      	rolq	$0x2b, %rbp
 55f4214:      	addq	%r14, %r15
 55f4217:      	addq	0x78(%rsp), %r11
 55f421c:      	addq	%r12, %r11
 55f421f:      	movq	%r11, %rdx
 55f4222:      	rolq	$0x14, %rdx
 55f4226:      	addq	%r12, %rdx
 55f4229:      	addq	%rbp, %rdx
 55f422c:      	addq	%r9, %r11
 55f422f:      	addq	$0x40, %rax
 55f4233:      	movq	%rsi, %r13
 55f4236:      	movq	%r15, %r14
 55f4239:      	movq	%rbx, %r9
 55f423c:      	movq	%r11, %r10
 55f423f:      	movq	%rdx, %r12
 55f4242:      	cmpq	%rax, 0x48(%rsp)
 55f4247:      	jne	0x55f4170 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x210>
 55f424d:      	movq	0x60(%rsp), %r13
 55f4252:      	testb	$0x7, %r13b
 55f4256:      	je	0x55f4334 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x3d4>
 55f425c:      	movq	0x40(%rsp), %rdi
 55f4261:      	movq	-0x38(%rdi,%r13,8), %rax
 55f4266:      	movq	-0x30(%rdi,%r13,8), %r9
 55f426b:      	addq	%rax, %rcx
 55f426e:      	addq	%r8, %rcx
 55f4271:      	addq	%r15, %rcx
 55f4274:      	rolq	$0x1b, %rcx
 55f4278:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 55f4282:      	imulq	%rbp, %rcx
 55f4286:      	addq	%rbx, %r8
 55f4289:      	movq	-0x10(%rdi,%r13,8), %r14
 55f428e:      	addq	%r14, %r8
 55f4291:      	rolq	$0x16, %r8
 55f4295:      	imulq	%rbp, %r8
 55f4299:      	xorq	%rdx, %rcx
 55f429c:      	movq	-0x18(%rdi,%r13,8), %r10
 55f42a1:      	addq	%r10, %r15
 55f42a4:      	addq	%r15, %r8
 55f42a7:      	addq	%r11, %rsi
 55f42aa:      	rolq	$0x1f, %rsi
 55f42ae:      	movq	%rsi, %r12
 55f42b1:      	imulq	%rbp, %rbx
 55f42b5:      	addq	%rcx, %r11
 55f42b8:      	addq	-0x40(%rdi,%r13,8), %rbx
 55f42bd:      	movq	-0x28(%rdi,%r13,8), %r15
 55f42c2:      	addq	%r15, %r11
 55f42c5:      	addq	%rbx, %r11
 55f42c8:      	rolq	$0x2b, %r11
 55f42cc:      	imulq	%rbp, %r12
 55f42d0:      	addq	%r9, %rax
 55f42d3:      	addq	%rbx, %rax
 55f42d6:      	movq	%rax, %rsi
 55f42d9:      	rolq	$0x14, %rsi
 55f42dd:      	addq	%rbx, %rsi
 55f42e0:      	addq	%r11, %rsi
 55f42e3:      	addq	%r15, %rax
 55f42e6:      	addq	%r12, %rdx
 55f42e9:      	addq	-0x20(%rdi,%r13,8), %rdx
 55f42ee:      	addq	%r8, %r9
 55f42f1:      	movq	-0x8(%rdi,%r13,8), %rdi
 55f42f6:      	addq	%rdi, %r9
 55f42f9:      	addq	%rdx, %r9
 55f42fc:      	rolq	$0x2b, %r9
 55f4300:      	addq	%r14, %r10
 55f4303:      	addq	%rdx, %r10
 55f4306:      	movq	%r10, %r11
 55f4309:      	rolq	$0x14, %r11
 55f430d:      	addq	%rdx, %r11
 55f4310:      	addq	%r9, %r11
 55f4313:      	addq	%rdi, %r10
 55f4316:      	movq	%r11, %rdx
 55f4319:      	movq	%r10, %r11
 55f431c:      	movq	%rsi, %rbx
 55f431f:      	movq	%rax, %r15
 55f4322:      	movq	%rcx, %rsi
 55f4325:      	movq	%r12, %rcx
 55f4328:      	movq	0x30(%rsp), %r9
 55f432d:      	movq	0x38(%rsp), %r14
 55f4332:      	jmp	0x55f4348 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x3e8>
 55f4334:      	movq	0x30(%rsp), %r9
 55f4339:      	movq	0x38(%rsp), %r14
 55f433e:      	movabsq	$-0x4b6d499041670d8d, %rbp # imm = 0xB492B66FBE98F273
 55f4348:      	xorq	%r11, %r15
 55f434b:      	movabsq	$-0x622015f714c7d297, %r12 # imm = 0x9DDFEA08EB382D69
 55f4355:      	imulq	%r12, %r15
 55f4359:      	xorq	%r15, %r11
 55f435c:      	shrq	$0x2f, %r15
 55f4360:      	xorq	%r11, %r15
 55f4363:      	imulq	%r12, %r15
 55f4367:      	movq	%r15, %rdi
 55f436a:      	shrq	$0x2f, %rdi
 55f436e:      	xorq	%r15, %rdi
 55f4371:      	imulq	%r12, %rdi
 55f4375:      	movq	%r8, %rax
 55f4378:      	shrq	$0x2f, %rax
 55f437c:      	xorq	%r8, %rax
 55f437f:      	imulq	%rbp, %rax
 55f4383:      	addq	%rsi, %rax
 55f4386:      	addq	%rdi, %rax
 55f4389:      	xorq	%rdx, %rbx
 55f438c:      	imulq	%r12, %rbx
 55f4390:      	xorq	%rbx, %rdx
 55f4393:      	shrq	$0x2f, %rbx
 55f4397:      	xorq	%rdx, %rbx
 55f439a:      	imulq	%r12, %rbx
 55f439e:      	movq	%rbx, %rdx
 55f43a1:      	shrq	$0x2f, %rdx
 55f43a5:      	xorq	%rbx, %rdx
 55f43a8:      	imulq	%r12, %rdx
 55f43ac:      	movabsq	$-0x5b6a4c820b386c68, %rsi # imm = 0xA495B37DF4C79398
 55f43b6:      	imulq	%rsi, %r13
 55f43ba:      	addq	%rcx, %r13
 55f43bd:      	addq	%rdx, %r13
 55f43c0:      	xorq	%r13, %rax
 55f43c3:      	imulq	%r12, %rax
 55f43c7:      	xorq	%rax, %r13
 55f43ca:      	shrq	$0x2f, %rax
 55f43ce:      	xorq	%r13, %rax
 55f43d1:      	imulq	%r12, %rax
 55f43d5:      	movq	%rax, %r13
 55f43d8:      	shrq	$0x2f, %r13
 55f43dc:      	xorq	%rax, %r13
 55f43df:      	imulq	%r12, %r13
 55f43e3:      	movq	0x68(%rsp), %rbx
 55f43e8:      	movabsq	$-0xae502812aa7333, %rbp # imm = 0xFF51AFD7ED558CCD
 55f43f2:      	xorps	%xmm0, %xmm0
 55f43f5:      	movups	%xmm0, 0xe8(%rsp)
 55f43fd:      	movups	%xmm0, 0xd8(%rsp)
 55f4405:      	movups	%xmm0, 0xc8(%rsp)
 55f440d:      	movups	%xmm0, 0xb8(%rsp)
 55f4415:      	movups	%xmm0, 0xa8(%rsp)
 55f441d:      	movups	%xmm0, 0x98(%rsp)
 55f4425:      	movups	%xmm0, 0x88(%rsp)
 55f442d:      	movq	%rbp, 0xf8(%rsp)
 55f4435:      	leaq	0xc0(%rsp), %r15
 55f443d:      	movl	%r9d, 0x80(%rsp)
 55f4445:      	cmpb	$0x0, 0xe(%rsp)
 55f444a:      	je	0x55f44d2 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x572>
 55f4450:      	movb	$0x1, 0x20(%rsp)
 55f4455:      	movb	%r14b, 0x18(%rsp)
 55f445a:      	shrq	$0x20, %r14
 55f445e:      	movl	%r14d, 0x19(%rsp)
 55f4463:      	movl	0x18(%rsp), %eax
 55f4467:      	leaq	0x5(,%rax,8), %rcx
 55f446f:      	xorq	%rbp, %r14
 55f4472:      	xorq	%r14, %rcx
 55f4475:      	imulq	%r12, %rcx
 55f4479:      	xorq	%rcx, %r14
 55f447c:      	shrq	$0x2f, %rcx
 55f4480:      	xorq	%r14, %rcx
 55f4483:      	imulq	%r12, %rcx
 55f4487:      	movq	%rcx, %rax
 55f448a:      	shrq	$0x2f, %rax
 55f448e:      	xorq	%rcx, %rax
 55f4491:      	imulq	%r12, %rax
 55f4495:      	movq	%rax, 0x21(%rsp)
 55f449a:      	leaq	0x9(%rax), %rcx
 55f449e:      	rolq	$0x37, %rcx
 55f44a2:      	movq	0x20(%rsp), %rdx
 55f44a7:      	xorq	%rcx, %rdx
 55f44aa:      	xorq	%rbp, %rdx
 55f44ad:      	imulq	%r12, %rdx
 55f44b1:      	xorq	%rdx, %rcx
 55f44b4:      	shrq	$0x2f, %rdx
 55f44b8:      	xorq	%rcx, %rdx
 55f44bb:      	imulq	%r12, %rdx
 55f44bf:      	movq	%rdx, %rcx
 55f44c2:      	shrq	$0x2f, %rcx
 55f44c6:      	xorq	%rdx, %rcx
 55f44c9:      	imulq	%r12, %rcx
 55f44cd:      	xorq	%rax, %rcx
 55f44d0:      	jmp	0x55f44dc <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x57c>
 55f44d2:      	movabsq	$-0x4d4db097723be9b3, %rcx # imm = 0xB2B24F688DC4164D
 55f44dc:      	leaq	0x8c(%rsp), %rdx
 55f44e4:      	movq	%rcx, 0x84(%rsp)
 55f44ec:      	movq	$0x0, 0x50(%rsp)
 55f44f5:      	leaq	0x80(%rsp), %rbp
 55f44fd:      	leaq	0x50(%rsp), %rsi
 55f4502:      	movq	%rbp, %rdi
 55f4505:      	movq	%r15, %rcx
 55f4508:      	movq	0x10(%rsp), %r8
 55f450d:      	callq	0x3b01720 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIPNS_4TypeEEEPcRmS6_S6_T_>
 55f4512:      	movq	0x50(%rsp), %rcx
 55f4517:      	movq	%rcx, 0x58(%rsp)
 55f451c:      	leaq	0x58(%rsp), %rsi
 55f4521:      	movq	%rbp, %rdi
 55f4524:      	movq	%rax, %rdx
 55f4527:      	movq	%r15, %rcx
 55f452a:      	movq	0x70(%rsp), %r8
 55f452f:      	callq	0x3b01720 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIPNS_4TypeEEEPcRmS6_S6_T_>
 55f4534:      	movq	0x58(%rsp), %rcx
 55f4539:      	movq	%rcx, 0x18(%rsp)
 55f453e:      	movzbl	0xf(%rsp), %r8d
 55f4544:      	leaq	0x18(%rsp), %rsi
 55f4549:      	movq	%rbp, %rdi
 55f454c:      	movq	%rax, %rdx
 55f454f:      	movq	%r15, %rcx
 55f4552:      	callq	0x3684340 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataIbEEPcRmS4_S4_T_>
 55f4557:      	movq	0x18(%rsp), %rcx
 55f455c:      	movq	%rcx, 0x20(%rsp)
 55f4561:      	leaq	0x20(%rsp), %rsi
 55f4566:      	movq	%rbp, %rdi
 55f4569:      	movq	%rax, %rdx
 55f456c:      	movq	%r15, %rcx
 55f456f:      	movq	%r13, %r8
 55f4572:      	callq	0x2ac8ac0 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper12combine_dataImEEPcRmS4_S4_T_>
 55f4577:      	movq	0x20(%rsp), %rsi
 55f457c:      	movq	%rbp, %rdi
 55f457f:      	movq	%rax, %rdx
 55f4582:      	movq	%r15, %rcx
 55f4585:      	callq	0x2ac8d90 <_ZN4llvm7hashing6detail29hash_combine_recursive_helper7combineEmPcS3_>
 55f458a:      	movq	%rax, %r15
 55f458d:      	movzbl	0x8(%rbx), %eax
 55f4591:      	cmpl	$0x17, %eax
 55f4594:      	ja	0x55f4604 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a4>
 55f4596:      	movl	$0x877720, %ecx         # imm = 0x877720
 55f459b:      	btl	%eax, %ecx
 55f459e:      	jae	0x55f4604 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a4>
 55f45a0:      	cmpb	$0x1, 0x98(%rbx)
 55f45a7:      	ja	0x55f4604 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x6a4>
 55f45a9:      	movl	0x9c(%rbx), %eax
 55f45af:      	movq	%r15, 0x80(%rsp)
 55f45b7:      	movl	%eax, 0x88(%rsp)
 55f45be:      	movq	0x84(%rsp), %rax
 55f45c6:      	leaq	0xc(%rax), %rcx
 55f45ca:      	rolq	$0x34, %rcx
 55f45ce:      	movabsq	$-0xae502812aa7333, %rdx # imm = 0xFF51AFD7ED558CCD
 55f45d8:      	xorq	%rcx, %rdx
 55f45db:      	xorq	%rdx, %r15
 55f45de:      	imulq	%r12, %r15
 55f45e2:      	xorq	%r15, %rcx
 55f45e5:      	shrq	$0x2f, %r15
 55f45e9:      	xorq	%rcx, %r15
 55f45ec:      	imulq	%r12, %r15
 55f45f0:      	movq	%r15, %rcx
 55f45f3:      	shrq	$0x2f, %rcx
 55f45f7:      	xorq	%r15, %rcx
 55f45fa:      	imulq	%r12, %rcx
 55f45fe:      	xorq	%rax, %rcx
 55f4601:      	movq	%rcx, %r15
 55f4604:      	movq	0x100(%rsp), %rdi
 55f460c:      	movl	0x110(%rsp), %esi
 55f4613:      	shlq	$0x4, %rsi
 55f4617:      	movl	$0x8, %edx
 55f461c:      	callq	0x828af00 <_ZdlPvmSt11align_val_t@plt>
 55f4621:      	movl	%r15d, %eax
 55f4624:      	addq	$0x128, %rsp            # imm = 0x128
 55f462b:      	popq	%rbx
 55f462c:      	popq	%r12
 55f462e:      	popq	%r13
 55f4630:      	popq	%r14
 55f4632:      	popq	%r15
 55f4634:      	popq	%rbp
 55f4635:      	retq
 55f4636:      	movl	0xe8(%rbx), %r14d
 55f463d:      	shlq	$0x20, %r14
 55f4641:      	incq	%r14
 55f4644:      	jmp	0x55f3fd7 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x77>
 55f4649:      	movq	0x88(%rbx), %rax
 55f4650:      	movzbl	(%rax), %eax
 55f4653:      	shlq	$0x20, %rax
 55f4657:      	movabsq	$-0x1d00000000, %r14    # imm = 0xFFFFFFE300000000
 55f4661:      	addq	%rax, %r14
 55f4664:      	movb	$0x1, 0xe(%rsp)
 55f4669:      	testq	%rbx, %rbx
 55f466c:      	jne	0x55f46a0 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x740>
 55f466e:      	jmp	0x55f3fdc <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f4673:      	testq	%rbx, %rbx
 55f4676:      	sete	%al
 55f4679:      	movabsq	$0x8400000000, %r14     # imm = 0x8400000000
 55f4683:      	cmpl	$0x1c, %edx
 55f4686:      	sete	0xe(%rsp)
 55f468b:      	cmpl	$0xa, %edx
 55f468e:      	setne	%cl
 55f4691:      	orb	%al, %cl
 55f4693:      	je	0x55f46a0 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x740>
 55f4695:      	cmpl	$0xc, %edx
 55f4698:      	jne	0x55f3fdc <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f469e:      	jmp	0x55f46cd <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x76d>
 55f46a0:      	movq	0x88(%rbx), %rax
 55f46a7:      	cmpb	$0x3f, (%rax)
 55f46aa:      	jne	0x55f3fdc <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x7c>
 55f46b0:      	movq	0x48(%rax), %rax
 55f46b4:      	movq	%rax, 0x10(%rsp)
 55f46b9:      	jmp	0x55f3fe5 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
 55f46be:      	movabsq	$0x7400000000, %r14     # imm = 0x7400000000
 55f46c8:      	movb	$0x1, 0xe(%rsp)
 55f46cd:      	movq	0xa8(%rbx), %rax
 55f46d4:      	movq	%rax, 0x10(%rsp)
 55f46d9:      	jmp	0x55f3fe5 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
 55f46de:      	movq	0xa8(%rbx), %rax
 55f46e5:      	movq	%rax, 0x10(%rsp)
 55f46ea:      	movb	$0x1, 0xe(%rsp)
 55f46ef:      	movabsq	$0x2200000000, %r14     # imm = 0x2200000000
 55f46f9:      	jmp	0x55f3fe5 <_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE+0x85>
