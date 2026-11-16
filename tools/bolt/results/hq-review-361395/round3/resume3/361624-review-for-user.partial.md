# Partial review: in-tree BOLT configuration

An in-tree configuration currently fails on X86BoltMnemonicTables.cpp.
The file is added to LLVMBOLT_TARGET_X86_SOURCES only for a standalone
build, but it is not listed in LLVM_OPTIONAL_SOURCES. LLVM's source-list
check therefore rejects the whole-LLVM configuration.

Please register the standalone-only translation unit as optional for
the in-tree build. I have not applied a fix to this patch.

This blocks the remaining link-plan verification. The removal of
DISABLE_LLVM_LINK_LLVM_DYLIB also affects in-tree BOLT targets, so that
linking mode still needs to be checked after configuration succeeds.
