//===-- X86BoltMnemonicTables.cpp - X86 tables & helpers for BOLT -*- C++ -*-=//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// Upstream compiles X86GenMnemonicTables.inc (llvm::X86::isNOP/isADD/...)
// and the X86 target-internal helpers below into LLVMX86Desc. Standalone
// BOLT links a reduced LLVM that neither exports them from libLLVM.so nor
// ships linkable static archives, so mirror them here. The generated code
// must be included at global scope (like llvm's X86MnemonicTables.cpp) to
// resolve opcode enums, hence this standalone TU. Keep in sync with
// upstream when rebasing.
//
//===----------------------------------------------------------------------===//

#include "MCTargetDesc/X86BaseInfo.h"
#include "MCTargetDesc/X86EncodingOptimization.h"
#include "MCTargetDesc/X86MCTargetDesc.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCRegister.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"

#ifdef BOLT_STANDALONE_X86_TABLES

#define GET_REGINFO_MC_DESC
#include "X86GenRegisterInfo.inc"

#define GET_X86_MNEMONIC_TABLES_CPP
#include "X86GenMnemonicTables.inc"

namespace llvm {

unsigned X86::getOpcodeForShortImmediateForm(unsigned Opcode) {
#define ENTRY(LONG, SHORT)                                                     \
  case X86::LONG:                                                              \
    return X86::SHORT;
  switch (Opcode) {
  default:
    return Opcode;
#include "MCTargetDesc/X86EncodingOptimizationForImmediate.def"
  }
}

MCRegister getX86SubSuperRegister(MCRegister Reg, unsigned Size, bool High) {
#include "X86GenSubSuperRegisterBody.inc"
}

namespace X86_MC {

static bool isMemOperand(const MCInst &MI, unsigned Op, unsigned RegClassID) {
  const MCOperand &Base = MI.getOperand(Op + X86::AddrBaseReg);
  const MCOperand &Index = MI.getOperand(Op + X86::AddrIndexReg);
  const MCRegisterClass &RC = X86MCRegisterClasses[RegClassID];

  return (Base.isReg() && Base.getReg() && RC.contains(Base.getReg())) ||
         (Index.isReg() && Index.getReg() && RC.contains(Index.getReg()));
}

bool is16BitMemOperand(const MCInst &MI, unsigned Op,
                              const MCSubtargetInfo &STI) {
  const MCOperand &Base = MI.getOperand(Op + X86::AddrBaseReg);
  const MCOperand &Index = MI.getOperand(Op + X86::AddrIndexReg);

  if (STI.hasFeature(X86::Is16Bit) && Base.isReg() && !Base.getReg() &&
      Index.isReg() && !Index.getReg())
    return true;
  return isMemOperand(MI, Op, X86::GR16RegClassID);
}

bool is32BitMemOperand(const MCInst &MI, unsigned Op) {
  const MCOperand &Base = MI.getOperand(Op + X86::AddrBaseReg);
  const MCOperand &Index = MI.getOperand(Op + X86::AddrIndexReg);
  if (Base.isReg() && Base.getReg() == X86::EIP) {
    assert(Index.isReg() && !Index.getReg() && "Invalid eip-based address");
    return true;
  }
  if (Index.isReg() && Index.getReg() == X86::EIZ)
    return true;
  return isMemOperand(MI, Op, X86::GR32RegClassID);
}

bool is64BitMemOperand(const MCInst &MI, unsigned Op) {
  return isMemOperand(MI, Op, X86::GR64RegClassID);
}

bool needsAddressSizeOverride(const MCInst &MI, const MCSubtargetInfo &STI,
                              int MemoryOperand, uint64_t TSFlags) {
#include "X86GenNeedsAddressSizeOverrideBody.inc"
}

} // namespace X86_MC
} // namespace llvm
#endif
