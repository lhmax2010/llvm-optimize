from pathlib import Path
import subprocess,re,difflib,ast,json
E=Path(__file__).resolve().parent;S=E.parents[3].parent/'llvm-optimize/temp/hardening-ps4-20261114/source'
# Use explicit source path; the evidence depth is not a repository contract.
S=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114/source')
D=E/'drafts';files=['packaging/clang-bolt-helper.py','packaging/llvm-static-archives-native.py','packaging/llvm.spec'];base={f:subprocess.check_output(['git','-C',str(S),'show','8ec86c3e:'+f],text=True) for f in files};new=dict(base)
for tag in ['H1','H2','H3','H4']:
 lines=(D/(tag+'.diff')).read_text().splitlines(True);i=0;filename=None
 while i<len(lines):
  if lines[i].startswith('+++ b/'):filename=lines[i][6:].strip();i+=1;continue
  if not lines[i].startswith('@@ '):i+=1;continue
  i+=1;before=[];after=[]
  while i<len(lines) and not lines[i].startswith(('@@ ','--- a/','+++ b/')):
   line=lines[i]
   if line.startswith((' ','-')):before.append(line[1:])
   if line.startswith((' ','+')):after.append(line[1:])
   i+=1
  a=''.join(before);b=''.join(after);assert new[filename].count(a)==1,(tag,filename);new[filename]=new[filename].replace(a,b,1)
c=files[1];before=new[c]
old="def install_main():\n    global _CANCEL_SIGNAL\n    _CANCEL_SIGNAL = None\n    log_startup_context()\n"
assert before.count(old)==1
new[c]=before.replace(old,'def _install_main():\n',1)
reset="    if signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL:\n        signal.signal(signal.SIGCHLD, signal.SIG_DFL)\n        print('NATIVE_ARCHIVES_SIGCHLD_RESET inherited handler -> SIG_DFL', flush=True)\n"
assert new[c].count(reset)==1;new[c]=new[c].replace(reset,'',1)
wrapper="""def install_main():
    global _CANCEL_SIGNAL
    _CANCEL_SIGNAL = None
    log_startup_context()
    previous = signal.getsignal(signal.SIGCHLD)
    try:
        if previous != signal.SIG_DFL:
            signal.signal(signal.SIGCHLD, signal.SIG_DFL)
            print('NATIVE_ARCHIVES_SIGCHLD_RESET inherited handler -> SIG_DFL', flush=True)
        return _install_main()
    finally:
        if previous != signal.SIG_DFL:
            signal.signal(signal.SIGCHLD, previous)


"""
marker="if __name__ == '__main__':";assert new[c].count(marker)==1;new[c]=new[c].replace(marker,wrapper+marker)
(D/'H5.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),new[c].splitlines(True),fromfile='a/'+c,tofile='b/'+c)))
combined=''
for f in files:
 if f.endswith('.py'):ast.parse(new[f])
 combined+=''.join(difflib.unified_diff(base[f].splitlines(True),new[f].splitlines(True),fromfile='a/'+f,tofile='b/'+f))
(D/'combined-on-PS4.diff').write_text(combined)
(E/'draft-generation.json').write_text(json.dumps(dict(base='8ec86c3e',applied=False,syntax_only=True,tests_run=False,files=files,preparation_corrections=1),indent=2)+'\n')
print('Drafts syntax PASS, product untouched')
