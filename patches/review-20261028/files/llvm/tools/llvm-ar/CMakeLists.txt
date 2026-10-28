set(LLVM_LINK_COMPONENTS
  AllTargetsAsmParsers
  AllTargetsDescs
  AllTargetsInfos
  BinaryFormat
  Core
  DlltoolDriver
  LibDriver
  Object
  Support
  TargetParser
  )

set(tizen_static_link)
if(TIZEN_HYBRID_LINK)
  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
  endif()
  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
  set(USE_SHARED "")
endif()

add_llvm_tool(llvm-ar
  ${tizen_static_link}
  llvm-ar.cpp

  DEPENDS
  intrinsics_gen
  GENERATE_DRIVER
  )

if(TIZEN_HYBRID_LINK)
  set_property(TARGET llvm-ar PROPERTY TIZEN_STATIC_LLVM ON)
endif()

add_llvm_tool_symlink(llvm-ranlib llvm-ar)
add_llvm_tool_symlink(llvm-lib llvm-ar)
add_llvm_tool_symlink(llvm-dlltool llvm-ar)

if(LLVM_INSTALL_BINUTILS_SYMLINKS)
  add_llvm_tool_symlink(ar llvm-ar)
  add_llvm_tool_symlink(dlltool llvm-ar)
  add_llvm_tool_symlink(ranlib llvm-ar)
endif()
