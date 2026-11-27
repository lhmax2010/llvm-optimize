"""Archive the shell argument regression and the verified sandbox receipt."""
import difflib
from pathlib import Path
import shutil
import sys

from prepare import A, W, B, D, PREVIOUS, S, c

sys.path.insert(0,str(W/"archive/task161"))
from coordination import publication
from review_packet import commit_push

E=B/"tools/bolt/results/task170"
DOC=B/"docs/bolt/170_pgo_bolt_argv_fix.md"
SKILL=B/"tools/skills/tizen-llvm-offline-profile"
LINK="../../tools/bolt/results/task170/"
TICK=chr(96)


def validate(r):
    assert r["status"]=="PASS"
    assert r["ls_remote"].split()==[r["test"],"refs/heads/"+r["branch"]]
    matrix=c.read(D/"argv-fixed/result.json")
    assert len(matrix["matrix"])==8
    assert sum(len(x["calls"]) for x in matrix["matrix"].values())==118
    c.require_argv_receipt(D,r["test"])
    try:
        c.require_argv_receipt(D,PREVIOUS)
    except RuntimeError as exc:
        assert c.SPEC in str(exc) and "candidate blob" in str(exc)
        (A/"receipt-binding.txt").write_text("Fixed test commit: PASS\nOld test commit: "+str(exc)+"\n")
    else:
        raise RuntimeError("the fixed tokenization receipt wrongly qualified the old commit")


def save_in(path,name=None):
    output=E/(name or path.name)
    output.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(path,output)


def archive_artifacts():
    files=("argv-before-final.json","argv-before-final.stderr.txt","argv-before-final.stdout.txt","preparation.txt",
           "r-argv.json","r-argv.stdout.txt","r-spec.diff","integration-spec.diff","test-only.diff",
           "test-vs-previous.diff","skill-tests.txt","skill-validator.txt","skill-text-scan.txt","rpm.json",
           "result.json","push-attempt.json","receipt-binding.txt","prepare.py","report.py")
    for name in files:
        save_in(A/name)
    for group, root in (("before",A/"argv-original"),("recipe",A/"argv-recipe"),("fixed",D/"argv-fixed")):
        for source in root.iterdir():
            if source.suffix in (".txt",".json"):
                save_in(source,f"argv/{group}/{source.name}")
    for sub in D.iterdir():
        if sub.is_file() and sub.suffix in (".txt",".json",".cmake"):
            save_in(sub,"candidate/"+sub.name)
    for msg in (D/"messages").glob("*.txt"):
        save_in(msg,"candidate/messages/"+msg.name)
    save_in(D/"assets/llvm-profiles.manifest","candidate/llvm-profiles.manifest")
    patch="".join(difflib.unified_diff((A/"candidate.before.py").read_text().splitlines(True),
                (S/"candidate.py").read_text().splitlines(True),"candidate.py before","candidate.py after"))
    (E/"candidate-prepush-gate.diff").write_text(patch)


def render(r):
    q=lambda x:TICK+str(x)+TICK
    lines=["# 170 · 修正 PGO+BOLT 的参数分词","",
           f"**新 QB 验证分支已创建，远端指向 {q(r['test'])}。**",
           f" [远端回执]({LINK}candidate/sandbox-after.stdout.txt)","",
           f"- 分支 {q(r['branch'])}",
           f"- 修正后的集成提交 {q(r['integration'])}",
           f"- QB 测试提交 {q(r['test'])}",
           f"- R 配方提交 {q(r['recipe'])}","",
           "## Spec 修正","",
           "在 Source1202 的闭引号与可选宏之间插入一个空格。R 和集成提交的产品 diff 各为一行。"
           "新 QB 测试提交的树相对上一版测试提交也只有这一个空格变化。","",
           TICK*3+"diff",(A/"integration-spec.diff").read_text().rstrip(),TICK*3,"",
           f"[R diff]({LINK}r-spec.diff) · [集成 diff]({LINK}integration-spec.diff) · "
           f"[QB 测试提交内容]({LINK}test-only.diff) · [与前一测试提交的 diff]({LINK}test-vs-previous.diff)","",
           "## 真实 shell 参数矩阵","",
           "Tizen RPM 4.14.1 对 x86_64 展开 T、D 与 PGO/BOLT 开关的八种组合。检查显式展开安装后置宏，"
           "遍历直接调用及逐调用点转发的 bolt_step。Bash 仅求值参数，导入的产品 helper 提供真实 argparse parser。"
           "PGO 参数逐项核对 manifest、项目、work、profdata 和可选 BOLT profile。"
           "两种项目的 PGO+BOLT 旧版都在实际拼接处报错，修正后候选的 118 条调用均解析成功。"
           "R 的八种组合也通过。", "",
           "### 修正前原文","",TICK*3+"text",
           (A/"argv-before-final.stdout.txt").read_text().rstrip(),TICK*3,"",
           "### 修正后原文","",TICK*3+"text",
           "\n".join(line for line in (A/"preparation.txt").read_text().splitlines()
                     if line.startswith(("RPM version ","PASS "))),TICK*3,"",
           f"[旧版逐调用 argv]({LINK}argv/before/result.json) · [修正版逐调用 argv]({LINK}argv/fixed/result.json) · "
           f"[R 逐调用 argv]({LINK}argv/recipe/result.json)","",
           "技能 64 项单测通过，技能校验器通过，共享文本扫描零命中。候选推送前强制要求八项 PASS，"
           "将检查收据绑定到候选中的 spec 和 helper 两个 blob。旧候选使用新收据会因 SHA256 不匹配被拒绝。",
           f" [候选推送门禁改动]({LINK}candidate-prepush-gate.diff) · [绑定证明]({LINK}receipt-binding.txt)","",
           "## QB 候选静态核对","",
           "157-B 的三架构展开、profile SHA256 和压缩前身份、清单与 BOLT 参数核对均通过。"
           "打包继续使用配对 fdata 和 -stale-threshold=5。提交说明和新增行的对外文本门禁零命中。"
           "集成提交的 UNQUALIFIED 清单仍被生产 READY 门禁拒绝，QB 测试提交仅放宽状态检查。"
           "当前清单只含 T 映射，D 的矩阵结果覆盖参数解析。"
           f" [核对回执]({LINK}result.json) · [推送原文]({LINK}candidate/sandbox-push.stdout.txt)",""]
    return "\n".join(lines)


if __name__=="__main__":
    result=c.read(A/"result.json")
    validate(result)
    with publication():
        archive_artifacts()
        DOC.write_text(render(result))
        rev=commit_push("docs: verify profile argv before QB candidate publication",DOC,E,
            SKILL/"SKILL.md",SKILL/"references/gates.md",SKILL/"scripts/check_helper_argv.py",
            SKILL/"tests/test_check_helper_argv.py")
    (A/"published.sha").write_text(rev+"\n")
    print(rev,flush=True)
