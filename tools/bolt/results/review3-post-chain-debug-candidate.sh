    /usr/lib/rpm/find-debuginfo.sh \
    -j40 \
     \
     \
     \
     \
    --build-id-seed "22.1.8-1" \
     \
    --unique-debug-src-base "llvm-22.1.8-1.x86_64" \
     \
     \
     \
     \
    -S debugsourcefiles.list \
    "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8"\
    
   cp /usr/lib/rpm/debug.manifest /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/llvm-debuginfo.manifest 
   cp /usr/lib/rpm/debug.manifest /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/llvm-debugsource.manifest 
 

    /usr/lib/rpm/check-buildroot
    
    /usr/lib/rpm//brp-compress 
    
     
    /usr/lib/rpm/brp-strip-static-archive /bin/strip 
#    /usr/lib/rpm/brp-strip-comment-note /bin/strip /bin/objdump 

    /usr/lib/rpm/brp-python-hardlink 
    /usr/lib/rpm/tizen/find-docs.sh /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILDROOT 

    
    /usr/lib/rpm/tizen/find-isufiles.sh /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/isu.list 

    
    /etc/hal/rootstrap/hal-rootstrap-checker.sh /home/abuild/bolt-work/bolt-v4-20261015-review3 /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILDROOT x86_64 

    
    /etc/app-rootstrap/app-rootstrap-checker.sh /home/abuild/bolt-work/bolt-v4-20261015-review3 /home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILDROOT x86_64 

 
    python3 /home/abuild/bolt-work/bolt-v4-20261015-review3/clang-bolt-helper.py post "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILDROOT" "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/build/clang-bolt/install-state.json" "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/build/clang-bolt/ordinary-clang-22" "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILD/llvm-22.1.8/build/clang-bolt/post-gate" --resource-dir "/home/abuild/bolt-work/bolt-v4-20261015-review3/post-capture/BUILDROOT/usr/lib64/clang/22" || exit 1 
    echo BOLT_POST_GATE_PASS