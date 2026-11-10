from pathlib import Path
import subprocess,sys
S=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source')
msg=subprocess.check_output(['git','-C',str(S),'show','-s','--format=%B','HEAD'],text=True).rstrip()+"\n"
old=msg
def replace(a,b):
 global msg
 assert a in msg,a
 msg=msg.replace(a,b,1)
if 'I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06' in msg:
 replace('in the validation evidence. Quickbuild verification remains pending.','in the validation evidence.')
 text="AddLLVM.cmake and AddClang.cmake are installed on every architecture,\nso the llvm-devel and clang payloads on armv7l and aarch64 carry the\nnew text. TIZEN_HYBRID_LINK is set only by the x86_64 recipe; elsewhere\nthe new function returns at once and the generated build is unchanged."
 replace('among 96 rewritten static interfaces; fail configuration if one appears.','among 96 rewritten static interfaces; fail configuration if one appears.\n\n'+text)
elif 'Ic98eab90cc017f127a66e1729b44fab8b8e8fb41' in msg:
 a=msg.index('An earlier revision completed %install');b=msg.index('\n\n',a)
 msg=msg[:a]+"Still open: accel/worker identity; cleanup cannot be guaranteed\nwithout matching /proc; performance outside LLVM workloads. The Ninja\njob limit does not cap linker memory. Maintenance notes: header of\npackaging/clang-bolt-helper.py"+msg[b:]
 a=msg.index('Handle SIGTERM, SIGHUP and SIGINT');b=msg.index('\n\n',a)
 msg=msg[:a]+"Handle SIGTERM, SIGHUP and SIGINT cooperatively and clean up the command\nprocess group before exiting; a second signal terminates immediately.\nCheck Python work and late cancellation before reporting success, and\nexit with 128+signal (129/130/143) after cancellation. Required BOLT\nsteps, the native archive conversion, optional disk reports and cache\nrelease all pass those statuses through to the RPM build instead of\nreporting a gate failure. Label cancellation separately from command\nerrors and timeouts."+msg[b:]
elif 'Ic76505ddb122f1e06271ff7462e24eceee4d400a' in msg:
 a=msg.index('Fix x86_64 compilation flags');b=msg.index('\n\n',a)
 msg=msg[:a]+"Fix x86_64 compilation flags to the effective Toolchain values recorded\nby QB 1215143. Inherit reviewed architecture flags, reject native CPU\nselection, and warn on debug sequences other than -g2 -gdwarf-4 -g.\nRelease commands contain no debug flags. Match whole tokens and\npreserve the caller's IFS state and shell options."+msg[b:]
 a=msg.index('Following review,');b=msg.index('\n\n',a)
 msg=msg[:a]+"Following review, reject -Wa, options, which PS10 accepted through its\nbroad -W branch, and report -Xassembler (already rejected) as an\nassembler option; require compiler, disassembler and nm to report the\nsame X.Y.Z version from the same directory, and record the three\nversions in the summary and in a NATIVE_ARCHIVES_TOOLS log line.\nHarden archive and relocation parsing against malformed sizes, size\nfields, long-name offsets, section tables and indexes; reject 8- and\n16-bit absolute relocations and relocation offsets outside their\ntarget section. Handle SIGHUP and process-group reaping during\nconversion, reset an inherited ignored SIGCHLD, and exit with\n128+signal after cancellation, including a signal received after the\nlast check."+msg[b:]
else:raise RuntimeError('unexpected commit')
assert max(map(len,msg.splitlines()))<=72
out=Path(__file__).parent/(msg.splitlines()[0].split(':')[0]+'-'+subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()+'.message')
out.write_text(msg)
subprocess.run(['git','-C',str(S),'-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','-F',str(out)],check=True)
