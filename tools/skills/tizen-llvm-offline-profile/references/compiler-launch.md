# Launching a private instrumented compiler

The retained x86-64 Clang 22.1.8 used the ELF interpreter /lib64/ld-linux-x86-64.so.2. Its dependencies included libc.so.6, ld-linux-x86-64.so.2, libstdc++.so.6, libgcc_s.so.1, libm.so.6, librt.so.1, libdl.so.2 and libz.so.1. Its RUNPATH included an origin-relative library directory and the original build library directory.

| Method | Version probe | First training input |
|---|---|---|
| Build-root loader with its matching library search path | Passed | One profraw, 32,385,336 bytes |
| Direct invocation with only the target LD_LIBRARY_PATH | SIGSEGV in the target libc __libc_start_main | Skipped |
| Direct invocation of a private copy with its ELF interpreter changed to the matching loader | Passed | One profraw, 32,385,320 bytes |

The direct invocation loaded the host interpreter and the target C library. Debugging with the debugger startup shell disabled reached the inferior and captured __libc_start_main. The first training command used the complete pinned parameters plus -c and -fintegrated-cc1. Integrated cc1 prevents driver re-execution using the explicit loader as the driver path. The matching-loader approach also worked for the packaged compiler plugin probe, which compiled and linked in separate steps.

Prefer an explicit launcher for the original compiler. Use a private profile destination for every probe or training input. Keep the host measurement programs and debugger in their normal environment. Assign any target library search path to the tested process alone.

Example configuration fragment:

~~~json
{
  "tool_launchers": {
    "instrumented_clang": {
      "loader": "/path/to/tizen-loader",
      "library_path": ["/path/to/compiler-libraries", "/path/to/tizen-libraries"]
    }
  },
  "training_extra_args": {
    "ir": ["-fintegrated-cc1"]
  }
}
~~~

A retained instrumented build can be imported with --resume --recover-instrumented RECEIPT --stages ir-train. The receipt binds the source commit, tree, snapshot, recipe and build configuration to the verified compiler, profdata tool and successful build log. Use the option with a fresh output directory to keep the original build and status files intact. Add --dry-run to rehash the receipt and show the next command without creating a checkpoint.
