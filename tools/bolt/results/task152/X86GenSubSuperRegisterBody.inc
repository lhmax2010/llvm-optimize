// Body mirrored from llvm/lib/Target/X86/MCTargetDesc/X86MCTargetDesc.cpp
{
#define DEFAULT_NOREG                                                          \
  default:                                                                     \
    return X86::NoRegister;
#define SUB_SUPER(R1, R2, R3, R4, R)                                           \
  case X86::R1:                                                                \
  case X86::R2:                                                                \
  case X86::R3:                                                                \
  case X86::R4:                                                                \
    return X86::R;
#define A_SUB_SUPER(R)                                                         \
  case X86::AH:                                                                \
    SUB_SUPER(AL, AX, EAX, RAX, R)
#define D_SUB_SUPER(R)                                                         \
  case X86::DH:                                                                \
    SUB_SUPER(DL, DX, EDX, RDX, R)
#define C_SUB_SUPER(R)                                                         \
  case X86::CH:                                                                \
    SUB_SUPER(CL, CX, ECX, RCX, R)
#define B_SUB_SUPER(R)                                                         \
  case X86::BH:                                                                \
    SUB_SUPER(BL, BX, EBX, RBX, R)
#define SI_SUB_SUPER(R) SUB_SUPER(SIL, SI, ESI, RSI, R)
#define DI_SUB_SUPER(R) SUB_SUPER(DIL, DI, EDI, RDI, R)
#define BP_SUB_SUPER(R) SUB_SUPER(BPL, BP, EBP, RBP, R)
#define SP_SUB_SUPER(R) SUB_SUPER(SPL, SP, ESP, RSP, R)
#define NO_SUB_SUPER(NO, REG)                                                  \
  SUB_SUPER(R##NO##B, R##NO##W, R##NO##D, R##NO, REG)
#define NO_SUB_SUPER_B(NO) NO_SUB_SUPER(NO, R##NO##B)
#define NO_SUB_SUPER_W(NO) NO_SUB_SUPER(NO, R##NO##W)
#define NO_SUB_SUPER_D(NO) NO_SUB_SUPER(NO, R##NO##D)
#define NO_SUB_SUPER_Q(NO) NO_SUB_SUPER(NO, R##NO)
  switch (Size) {
  default:
    llvm_unreachable("illegal register size");
  case 8:
    if (High) {
      switch (Reg.id()) {
        DEFAULT_NOREG
        A_SUB_SUPER(AH)
        D_SUB_SUPER(DH)
        C_SUB_SUPER(CH)
        B_SUB_SUPER(BH)
      }
    } else {
      switch (Reg.id()) {
        DEFAULT_NOREG
        A_SUB_SUPER(AL)
        D_SUB_SUPER(DL)
        C_SUB_SUPER(CL)
        B_SUB_SUPER(BL)
        SI_SUB_SUPER(SIL)
        DI_SUB_SUPER(DIL)
        BP_SUB_SUPER(BPL)
        SP_SUB_SUPER(SPL)
        NO_SUB_SUPER_B(8)
        NO_SUB_SUPER_B(9)
        NO_SUB_SUPER_B(10)
        NO_SUB_SUPER_B(11)
        NO_SUB_SUPER_B(12)
        NO_SUB_SUPER_B(13)
        NO_SUB_SUPER_B(14)
        NO_SUB_SUPER_B(15)
        NO_SUB_SUPER_B(16)
        NO_SUB_SUPER_B(17)
        NO_SUB_SUPER_B(18)
        NO_SUB_SUPER_B(19)
        NO_SUB_SUPER_B(20)
        NO_SUB_SUPER_B(21)
        NO_SUB_SUPER_B(22)
        NO_SUB_SUPER_B(23)
        NO_SUB_SUPER_B(24)
        NO_SUB_SUPER_B(25)
        NO_SUB_SUPER_B(26)
        NO_SUB_SUPER_B(27)
        NO_SUB_SUPER_B(28)
        NO_SUB_SUPER_B(29)
        NO_SUB_SUPER_B(30)
        NO_SUB_SUPER_B(31)
      }
    }
  case 16:
    switch (Reg.id()) {
      DEFAULT_NOREG
      A_SUB_SUPER(AX)
      D_SUB_SUPER(DX)
      C_SUB_SUPER(CX)
      B_SUB_SUPER(BX)
      SI_SUB_SUPER(SI)
      DI_SUB_SUPER(DI)
      BP_SUB_SUPER(BP)
      SP_SUB_SUPER(SP)
      NO_SUB_SUPER_W(8)
      NO_SUB_SUPER_W(9)
      NO_SUB_SUPER_W(10)
      NO_SUB_SUPER_W(11)
      NO_SUB_SUPER_W(12)
      NO_SUB_SUPER_W(13)
      NO_SUB_SUPER_W(14)
      NO_SUB_SUPER_W(15)
      NO_SUB_SUPER_W(16)
      NO_SUB_SUPER_W(17)
      NO_SUB_SUPER_W(18)
      NO_SUB_SUPER_W(19)
      NO_SUB_SUPER_W(20)
      NO_SUB_SUPER_W(21)
      NO_SUB_SUPER_W(22)
      NO_SUB_SUPER_W(23)
      NO_SUB_SUPER_W(24)
      NO_SUB_SUPER_W(25)
      NO_SUB_SUPER_W(26)
      NO_SUB_SUPER_W(27)
      NO_SUB_SUPER_W(28)
      NO_SUB_SUPER_W(29)
      NO_SUB_SUPER_W(30)
      NO_SUB_SUPER_W(31)
    }
  case 32:
    switch (Reg.id()) {
      DEFAULT_NOREG
      A_SUB_SUPER(EAX)
      D_SUB_SUPER(EDX)
      C_SUB_SUPER(ECX)
      B_SUB_SUPER(EBX)
      SI_SUB_SUPER(ESI)
      DI_SUB_SUPER(EDI)
      BP_SUB_SUPER(EBP)
      SP_SUB_SUPER(ESP)
      NO_SUB_SUPER_D(8)
      NO_SUB_SUPER_D(9)
      NO_SUB_SUPER_D(10)
      NO_SUB_SUPER_D(11)
      NO_SUB_SUPER_D(12)
      NO_SUB_SUPER_D(13)
      NO_SUB_SUPER_D(14)
      NO_SUB_SUPER_D(15)
      NO_SUB_SUPER_D(16)
      NO_SUB_SUPER_D(17)
      NO_SUB_SUPER_D(18)
      NO_SUB_SUPER_D(19)
      NO_SUB_SUPER_D(20)
      NO_SUB_SUPER_D(21)
      NO_SUB_SUPER_D(22)
      NO_SUB_SUPER_D(23)
      NO_SUB_SUPER_D(24)
      NO_SUB_SUPER_D(25)
      NO_SUB_SUPER_D(26)
      NO_SUB_SUPER_D(27)
      NO_SUB_SUPER_D(28)
      NO_SUB_SUPER_D(29)
      NO_SUB_SUPER_D(30)
      NO_SUB_SUPER_D(31)
    }
  case 64:
    switch (Reg.id()) {
      DEFAULT_NOREG
      A_SUB_SUPER(RAX)
      D_SUB_SUPER(RDX)
      C_SUB_SUPER(RCX)
      B_SUB_SUPER(RBX)
      SI_SUB_SUPER(RSI)
      DI_SUB_SUPER(RDI)
      BP_SUB_SUPER(RBP)
      SP_SUB_SUPER(RSP)
      NO_SUB_SUPER_Q(8)
      NO_SUB_SUPER_Q(9)
      NO_SUB_SUPER_Q(10)
      NO_SUB_SUPER_Q(11)
      NO_SUB_SUPER_Q(12)
      NO_SUB_SUPER_Q(13)
      NO_SUB_SUPER_Q(14)
      NO_SUB_SUPER_Q(15)
      NO_SUB_SUPER_Q(16)
      NO_SUB_SUPER_Q(17)
      NO_SUB_SUPER_Q(18)
      NO_SUB_SUPER_Q(19)
      NO_SUB_SUPER_Q(20)
      NO_SUB_SUPER_Q(21)
      NO_SUB_SUPER_Q(22)
      NO_SUB_SUPER_Q(23)
      NO_SUB_SUPER_Q(24)
      NO_SUB_SUPER_Q(25)
      NO_SUB_SUPER_Q(26)
      NO_SUB_SUPER_Q(27)
      NO_SUB_SUPER_Q(28)
      NO_SUB_SUPER_Q(29)
      NO_SUB_SUPER_Q(30)
      NO_SUB_SUPER_Q(31)
    }
  }
}
