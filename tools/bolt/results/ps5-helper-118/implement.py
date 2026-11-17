from pathlib import Path
import subprocess,json,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');S=W/'temp/ps5-helper-118/source';E=B/'tools/bolt/results/ps5-helper-118';p=S/'packaging/clang-bolt-helper.py'
rows=[]
def commit(label,title,old):
 new=p.read_text();assert old!=new
 r=subprocess.run(['git','-C',str(S),'diff'],capture_output=True,check=True);(E/(label+'.diff')).write_bytes(r.stdout)
 subprocess.run(['git','-C',str(S),'add','packaging/clang-bolt-helper.py'],check=True)
 subprocess.run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','-C',str(S),'commit','-m',title],check=True)
 sha=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD']).decode().strip()
 rows.append({'item':label,'sha':sha});(E/'working-commits.json').write_text(json.dumps(rows,indent=2));print(label,sha,flush=True)
s=p.read_text();old=s
s=s.replace('    while True:\n        errors = []\n        deadline_error = None','    errors = []\n    while True:\n        deadline_error = None',1)
s=s.replace('        if errors:\n            if deadline_error is not None:','        if errors and (not members or time.monotonic() >= deadline or deadline_error is not None):\n            if deadline_error is not None:',1)
p.write_text(s);commit('R1','helper: continue cleanup after member errors',old)
old=s
s=s.replace("                except (FileNotFoundError, ProcessLookupError):\n                    continue\n                except PermissionError as error:\n                    denied.append('%s: %s' % (entry.name, error))", "                except OSError as error:\n                    if isinstance(error, (FileNotFoundError, ProcessLookupError)) or error.errno == errno.ESRCH:\n                        continue\n                    denied.append('PID %s errno=%s: %s' %\n                                  (entry.name, errno.errorcode.get(error.errno, error.errno), error))",1)
s=s.replace("                except PermissionError as error:\n                    errors.append('PID %d: %s' % (pid, error))", "                except OSError as error:\n                    if error.errno != errno.ESRCH:\n                        errors.append('PID %d errno=%s: %s' %\n                                      (pid, errno.errorcode.get(error.errno, error.errno), error))\n                except GateError as error:\n                    errors.append('PID %d: %s' % (pid, error))",1)
p.write_text(s);commit('R2','helper: aggregate runtime member errors without mode changes',old)
old=s
start=s.index('def wait_session_exit(');end=s.index('\n\ndef kill_session(',start)
s=s[:start]+'''def session_snapshot(members):
    """Describe a complete observation for diagnostics, never for signaling."""
    observed = []
    for pid, state, starttime in members:
        try:
            comm = Path('/proc/%d/comm' % pid).read_text(errors='replace').strip()
        except OSError:
            comm = '?'
        observed.append('%d:%s (%s)' % (pid, comm, state))
    return ', '.join(observed)


def wait_session_exit(sid, timeout=10, *, kill=False, deadline=None):
    # The unreaped session leader pins the SID. Descendants that call setsid()
    # themselves escape this session and are outside this tracking model.
    # This is not cgroup containment and does not adopt/reap grandchildren.
    # Deadlines are cooperative; an individual kernel operation can overrun.
    if deadline is None:
        deadline = time.monotonic()+timeout
    errors = {}
    last_observed = []
    snapshot = ''
    complete = False

    def expired():
        detail = '; errors: '+'; '.join(errors) if errors else ''
        if complete and last_observed:
            raise LiveDescendantsError(
                'process session %d still alive at deadline; last observed members: %s%s' %
                (sid, snapshot, detail))
        raise SessionInspectionError(
            'could not verify that the session is empty; last observed snapshot: %s%s' %
            (snapshot, detail), last_observed)

    while True:
        # Do not enter a new scan with an already exhausted budget. A completed
        # observation remains diagnostic evidence, not fresh kill authority.
        if time.monotonic() >= deadline:
            expired()
        complete = False
        try:
            members = live_session_members(sid, deadline)
        except SessionInspectionError as error:
            errors[str(error)] = None
            members = error.members
            if isinstance(error, SessionDeadlineError):
                expired()
        else:
            complete = True
            last_observed = list(members)
            snapshot = session_snapshot(members)
        if kill:
            # Retry errored members on later scans, and handle newly forked
            # members. Never switch signaling mode after the capability probe.
            for pid, state, starttime in members:
                try:
                    session_deadline(deadline, members)
                    kill_session_member(sid, pid, starttime, deadline)
                except (FileNotFoundError, ProcessLookupError):
                    pass
                except SessionDeadlineError as error:
                    errors[str(error)] = None
                    expired()
                except OSError as error:
                    if error.errno != errno.ESRCH:
                        errors['PID %d errno=%s: %s' %
                               (pid, errno.errorcode.get(error.errno, error.errno), error)] = None
                except GateError as error:
                    errors['PID %d: %s' % (pid, error)] = None
        if complete and not members:
            if errors:
                raise GateError('session cleanup/check failed: '+'; '.join(errors)+
                                '; last observed snapshot: '+snapshot)
            return
        if time.monotonic() >= deadline:
            expired()
        time.sleep(min(.02, max(0, deadline-time.monotonic())))
''' +s[end:]
needle="            except LiveDescendantsError as error:\n"
assert s.count(needle)==1
s=s.replace(needle,"            except SessionInspectionError as error:\n                primary = 'COMMAND_ERROR: command exited successfully; '+str(error)\n                raise GateError(primary) from error\n"+needle,1)
p.write_text(s);commit('R3-L2','helper: retain complete session snapshots for diagnostics',old)
old=s
assert s.count('            session_retired = True\n            _ACTIVE_SESSION = None')==2
s=s.replace('            session_retired = True\n            _ACTIVE_SESSION = None','            _ACTIVE_SESSION = None\n            session_retired = True')
p.write_text(s);commit('L1','helper: clear the active handle before retiring the session',old)
old=s
s=s.replace("        mode = 'pidfd'\n        try:", "        mode = 'pidfd'\n        probe_errno = None\n        try:",1)
s=s.replace('error.errno not in (errno.ENOSYS, errno.EPERM)', 'error.errno not in (errno.ENOSYS, errno.EPERM, errno.EACCES)',1)
s=s.replace("            mode = 'fallback-recheck'\n        print('SESSION_KILL_MODE='+mode, file=sys.stderr, flush=True)", "            mode = 'fallback-recheck'\n            probe_errno = error.errno\n        suffix = ' errno='+errno.errorcode.get(probe_errno, str(probe_errno)) if probe_errno is not None else ''\n        print('SESSION_KILL_MODE='+mode+suffix, file=sys.stderr, flush=True)",1)
p.write_text(s);commit('EACCES','helper: disclose denied pidfd probes and allow EACCES fallback',old)
old=s
s=s.replace("                # and terminates immediately, without restarting its budget.", "                # and terminates immediately, without restarting its budget.\n                # This forced-exit cleanup is best effort, not containment.")
p.write_text(s);commit('wording','helper: document the best-effort forced-exit boundary',old)
compile(s,str(p),'exec')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'D1 code written')
