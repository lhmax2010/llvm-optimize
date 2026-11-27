"""Read one QB build until results are published, then run the requested audit."""
from datetime import datetime
import subprocess
import sys
import time
import traceback
from urllib.error import HTTPError, URLError

from collect import (A,E,BUILD,TERMINAL,FilesPending,overview,archive_logs,audit_logs,
                     download_rpms,elf_check,read,save,ensure_dirs)
from report import publish

POLL = 600


def status(stage, **fields):
    value={"at":datetime.now().astimezone().isoformat(),"build_id":BUILD,"stage":stage,**fields}
    save(A/"live.json",value)
    print(value,flush=True)


def wait_for_artifacts():
    meta=read(E/"build-initial.json")
    while True:
        read_error=None
        try:
            meta=overview()
        except (FilesPending, subprocess.TimeoutExpired) as error:
            read_error=str(error)
        terminal=meta["overall"] in TERMINAL
        if terminal or read_error:
            try:
                result=archive_logs()
                if read_error:
                    meta={**meta,"qb_overview_read_error":read_error}
                return meta,result
            except (FilesPending,URLError) as error:
                status("WAIT_ARTIFACTS",qb=meta,reason=str(error),qb_read_error=read_error)
        else:
            status("WAIT_QB",qb=meta)
        time.sleep(POLL)


def wait_for_rpms(meta):
    while True:
        try:
            return download_rpms()
        except (FilesPending, URLError, TimeoutError) as error:
            if isinstance(error,HTTPError) and error.code not in (404,408,429,500,502,503,504):
                raise
            status("WAIT_RPMS",qb=meta,reason=str(error))
            time.sleep(POLL)


def main():
    ensure_dirs()
    meta, logs = None, None
    try:
        meta,receipts=wait_for_artifacts()
        status("LOG_AUDIT",qb=meta)
        logs=audit_logs(receipts)
        if logs["x86_64"]["status"]=="PASS":
            status("RPM_AUDIT",qb=meta)
            rpms=wait_for_rpms(meta)
            compare=elf_check(rpms)
            if not compare["same_sha256"]:
                status("BENCHMARK",qb=meta,clang=compare)
                with (A/"benchmark-run.txt").open("wb") as log:
                    subprocess.run([sys.executable,"-B",str(A/"v3q.py")],cwd=A,stdout=log,
                                   stderr=subprocess.STDOUT,check=True)
        rev=publish(meta,logs)
        status("DONE",qb=meta,bolt_v4=rev)
    except (OSError,RuntimeError,ValueError,subprocess.SubprocessError) as error:
        raw=traceback.format_exc()
        (A/"STOP.txt").write_text(raw)
        if logs is not None:
            (E/"audit-error.txt").write_text(raw)
            meta={**meta,"local_audit_error":str(error)}
            try:
                rev=publish(meta,logs)
            except (OSError,RuntimeError,ValueError,subprocess.SubprocessError):
                rev=None
            status("STOP",qb=meta,reason=str(error),bolt_v4=rev)
        else:
            status("STOP",reason=str(error))
        raise


if __name__=="__main__":
    main()
