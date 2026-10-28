set(LLVM_LINK_COMPONENTS
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

add_lld_tool(lld
  ${tizen_static_link}
  lld.cpp

  SUPPORT_PLUGINS
  GENERATE_DRIVER
  )
if(TIZEN_HYBRID_LINK)
  set_property(TARGET lld PROPERTY TIZEN_STATIC_LLVM ON)
endif()

export_executable_symbols_for_plugins(lld)

function(lld_target_link_libraries target type)
  if (TARGET obj.${target})
    target_link_libraries(obj.${target} ${ARGN})
  endif()

  get_property(LLVM_DRIVER_TOOLS GLOBAL PROPERTY LLVM_DRIVER_TOOLS)
  if(LLVM_TOOL_LLVM_DRIVER_BUILD AND ${target} IN_LIST LLVM_DRIVER_TOOLS)
    set(target llvm-driver)
  endif()

  target_link_libraries(${target} ${type} ${ARGN})
endfunction()

lld_target_link_libraries(lld
  PRIVATE
  lldCommon
  lldCOFF
  lldELF
  lldMachO
  lldMinGW
  lldWasm
  )

if(NOT LLD_SYMLINKS_TO_CREATE)
  set(LLD_SYMLINKS_TO_CREATE
      lld-link ld.lld ld64.lld wasm-ld)
endif()

foreach(link ${LLD_SYMLINKS_TO_CREATE})
  add_lld_symlink(${link} lld)
endforeach()

if(LLVM_TOOL_LLVM_DRIVER_BUILD)
  set_property(GLOBAL APPEND PROPERTY LLVM_DRIVER_HIDDEN_TOOL_ALIASES_lld ld)
endif()
