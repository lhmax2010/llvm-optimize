from pathlib import Path
sroot=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/review-20261102/source')
p=sroot/'packaging/llvm.spec';s=p.read_text()
s=s.replace('tizen_llvm_flags()\n',"TIZEN_LLVM_EXPECTED_DROPPED=${TIZEN_LLVM_EXPECTED_DROPPED-'-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4'}\ntizen_llvm_flags()\n",1)
s=s.replace('    tizen_llvm_release=$3\n','''    tizen_llvm_release=$3
    case $tizen_llvm_release in 0|1) ;; *)
        echo "TIZEN_LLVM_FIXED_FLAGS_FAILED invalid TIZEN_LLVM_RELEASE=$tizen_llvm_release" >&2
        return 1 ;;
    esac
    tizen_llvm_debug_sequence=
    tizen_llvm_unreviewed=
''')
a=s.index('    tizen_llvm_saved_ifs=$IFS');b=s.index('    case $- in',a)
s=s[:a]+'''    tizen_llvm_ifs_set=${IFS+x}
    tizen_llvm_saved_ifs=${IFS-}
    unset IFS
'''+s[b:]
s=s.replace('            -m64|-march=*', '''            -march=native|-mtune=native)
                tizen_llvm_unreviewed="${tizen_llvm_unreviewed}${tizen_llvm_unreviewed:+ }$tizen_llvm_token"
                continue ;;
            -m64|-march=*''')
s=s.replace('|-gsplit-*','')
s=s.replace('                if test "$tizen_llvm_release" = 0; then','''                tizen_llvm_debug_sequence="${tizen_llvm_debug_sequence}${tizen_llvm_debug_sequence:+ }$tizen_llvm_token"
                if test "$tizen_llvm_release" = 0; then''',1)
s=s.replace('            *) TIZEN_LLVM_DROPPED="${TIZEN_LLVM_DROPPED}${TIZEN_LLVM_DROPPED:+ }$tizen_llvm_token" ;;','''            *)
                TIZEN_LLVM_DROPPED="${TIZEN_LLVM_DROPPED}${TIZEN_LLVM_DROPPED:+ }$tizen_llvm_token"
                case " $TIZEN_LLVM_EXPECTED_DROPPED " in
                    *" $tizen_llvm_token "*) ;;
                    *) tizen_llvm_unreviewed="${tizen_llvm_unreviewed}${tizen_llvm_unreviewed:+ }$tizen_llvm_token" ;;
                esac ;;
''')
s=s.replace('    IFS=$tizen_llvm_saved_ifs','    if test "$tizen_llvm_ifs_set" = x; then IFS=$tizen_llvm_saved_ifs; else unset IFS; fi',1)
s=s.replace('    case $tizen_llvm_kind in\n','''    if test -n "$tizen_llvm_unreviewed"; then
        echo "TIZEN_LLVM_FIXED_FLAGS_FAILED unreviewed=[$tizen_llvm_unreviewed]; 逐个评审后，加入固定参数集或预期丢弃清单" >&2
        return 1
    fi
    case $tizen_llvm_kind:$tizen_llvm_release in
        CFLAGS:0|CXXFLAGS:0)
            if test "$tizen_llvm_debug_sequence" != '-g2 -gdwarf-4 -g'; then
                echo "TIZEN_LLVM_FIXED_FLAGS_FAILED debug sequence=[$tizen_llvm_debug_sequence] expected=[-g2 -gdwarf-4 -g]; recertification required" >&2
                return 1
            fi ;;
    esac
    case $tizen_llvm_kind in
''',1)
s=s.replace('        LDFLAGS)\n','''        LDFLAGS)
            # Executable/shared linker flags are explicit in the spec, not read
            # from LDFLAGS. CMAKE_MODULE_LINKER_FLAGS is initialized from this
            # environment value, unchanged from the Toolchain project value.
''',1)
for k in ('CFLAGS','CXXFLAGS','LDFLAGS'):
 s=s.replace(f'tizen_llvm_flags {k} "${k}" "$TIZEN_LLVM_RELEASE"',f'tizen_llvm_flags {k} "${k}" "$TIZEN_LLVM_RELEASE" || exit 1')
s=s.replace('    --arch x86_64 \\\n','    --arch x86_64 --debug-info %{?llvm_release_build:%{lua:print(tonumber(rpm.expand("%{llvm_release_build}")) == 1 and "no" or "yes")}} \\\n')
# Use ordinary RPM conditionals rather than a Lua dependency.
s=s.replace('    --arch x86_64 --debug-info %{?llvm_release_build:%{lua:print(tonumber(rpm.expand("%{llvm_release_build}")) == 1 and "no" or "yes")}} \\\n','''    --arch x86_64 \\
%if %{llvm_release_build}
    --debug-info no \\
%else
    --debug-info yes \\
%endif
''')
p.write_text(s)
p=sroot/'packaging/llvm-static-archives-native.py';s=p.read_text()
s=s.replace("def ir_settings(lines, require_recorded_options=True, arch='x86_64'):","def ir_settings(lines, require_recorded_options=True, arch='x86_64', debug_info=None):")
s=s.replace('    policy = classify_options(recorded_command, arch)','''    found_debug = 'yes' if any(token.startswith('-g') for token in recorded_command) else 'no'
    if debug_info is not None and debug_info != found_debug:
        raise ValueError('debug-info expected='+str(debug_info)+' found='+found_debug)
    policy = classify_options(recorded_command, arch)''',1)
s=s.replace('address_space_bytes=4*1024**3, command=None):','address_space_bytes=4*1024**3, command=None, debug_info=None):',1)
s=s.replace("    reset_evidence(root, output, build)","    if debug_info not in ('yes', 'no'):\n        raise ValueError('debug-info expected=yes|no found='+str(debug_info))\n    reset_evidence(root, output, build)",1)
s=s.replace("status='CONVERTING', missing_symbols_by_type={})","status='CONVERTING', debug_info=debug_info, missing_symbols_by_type={})",1)
s=s.replace("        summary['native_archives_skipped'] = sum(not data['bitcode'] for archive, data in archives)","        summary['native_archives_skipped'] = sum(not data['bitcode'] for archive, data in archives)\n        # Preserved native members retain their bytes, including any debug sections.\n        summary['native_members_preserved'] = sum(data['machine'] for archive, data in archives)",1)
s=s.replace('settings = ir_settings(lines, arch=arch)','settings = ir_settings(lines, arch=arch, debug_info=debug_info)',1)
s=s.replace('address_space_bytes=4*1024**3):\n    root, output = Path(root).resolve()', 'address_space_bytes=4*1024**3, debug_info=None):\n    root, output = Path(root).resolve()',1)
s=s.replace('arch, jobs, address_space_bytes, command)','arch, jobs, address_space_bytes, command, debug_info)',1)
s=s.replace("    parser.add_argument('--arch', choices=['x86_64'], required=True)","    parser.add_argument('--arch', choices=['x86_64'], required=True)\n    parser.add_argument('--debug-info', choices=['yes', 'no'], required=True)",1)
s=s.replace('args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes)','args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes, args.debug_info)',1)
p.write_text(s)
