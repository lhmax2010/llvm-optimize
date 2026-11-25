// Body mirrored from llvm/lib/Target/X86/MCTargetDesc/X86MCTargetDesc.cpp
{
  uint64_t AdSize = TSFlags & X86II::AdSizeMask;
  bool Is16BitMode = STI.hasFeature(X86::Is16Bit);
  bool Is32BitMode = STI.hasFeature(X86::Is32Bit);
  bool Is64BitMode = STI.hasFeature(X86::Is64Bit);
  if ((Is16BitMode && AdSize == X86II::AdSize32) ||
      (Is32BitMode && AdSize == X86II::AdSize16) ||
      (Is64BitMode && AdSize == X86II::AdSize32))
    return true;
  uint64_t Form = TSFlags & X86II::FormMask;
  switch (Form) {
  default:
    break;
  case X86II::RawFrmDstSrc: {
    MCRegister siReg = MI.getOperand(1).getReg();
    assert(((siReg == X86::SI && MI.getOperand(0).getReg() == X86::DI) ||
            (siReg == X86::ESI && MI.getOperand(0).getReg() == X86::EDI) ||
            (siReg == X86::RSI && MI.getOperand(0).getReg() == X86::RDI)) &&
           "SI and DI register sizes do not match");
    return (!Is32BitMode && siReg == X86::ESI) ||
           (Is32BitMode && siReg == X86::SI);
  }
  case X86II::RawFrmSrc: {
    MCRegister siReg = MI.getOperand(0).getReg();
    return (!Is32BitMode && siReg == X86::ESI) ||
           (Is32BitMode && siReg == X86::SI);
  }
  case X86II::RawFrmDst: {
    MCRegister siReg = MI.getOperand(0).getReg();
    return (!Is32BitMode && siReg == X86::EDI) ||
           (Is32BitMode && siReg == X86::DI);
  }
  }

  // Determine where the memory operand starts, if present.
  if (MemoryOperand < 0)
    return false;

  if (STI.hasFeature(X86::Is64Bit)) {
    assert(!is16BitMemOperand(MI, MemoryOperand, STI));
    return is32BitMemOperand(MI, MemoryOperand);
  }
  if (STI.hasFeature(X86::Is32Bit)) {
    assert(!is64BitMemOperand(MI, MemoryOperand));
    return is16BitMemOperand(MI, MemoryOperand, STI);
  }
  assert(STI.hasFeature(X86::Is16Bit));
  assert(!is64BitMemOperand(MI, MemoryOperand));
  return !is16BitMemOperand(MI, MemoryOperand, STI);
}
