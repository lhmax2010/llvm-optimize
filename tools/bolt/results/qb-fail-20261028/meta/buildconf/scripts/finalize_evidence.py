from pathlib import Path
import json,hashlib,re,urllib.parse,shutil,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';F=B/'tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots'
(E/'scripts').mkdir(exist_ok=True)
for n in ['start.py','classify.py','extra_evidence.py','specs.py','fallback.py','exact_specs.py','scan_specs.py','coverage.py','render_report.py','finalize_evidence.py']:
 shutil.copyfile(D/n,E/'scripts'/n)
for n in ['specs.log','exact-specs.log','exact-specs-extra.log']:
 shutil.copyfile(D/n,E/n)
shutil.copyfile(D/'report-body.md',E/'scripts/report-body.md')
shutil.copyfile(D/'docs45-before-buildconf.md',E/'scripts/docs45-before-buildconf.md')
vals=json.loads((E/'validation.json').read_text());vals['config_sha256']={side:hashlib.sha256((F/side/'build.conf').read_bytes()).hexdigest() for side in ['toolchain','base']}
assert vals['config_sha256']=={'toolchain':'e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945','base':'840ef6de94c6d73e3fcced27dc777a399df435a0f2e4017347191a296f5f1975'}
links=[];missing=[];p=B/'docs/bolt/45_qb_meta_fix_and_snapshot.md'
for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
 if '://' in url or url.startswith('#'):continue
 target=(p.parent/urllib.parse.unquote(url.split('#')[0])).resolve();links.append(url)
 if not target.is_file():missing.append(url)
assert not missing,missing
vals['report_local_links_checked']=len(links);vals['missing_report_links']=missing
vals['meta_local_commit']=subprocess.check_output(['git','-C',str(W/'temp/qb-meta-20261028/repo'),'rev-parse','HEAD'],text=True).strip()
vals['paused_llvm_local_commit']=subprocess.check_output(['git','-C',str(W/'temp/debuglink-tb20261026/source'),'rev-parse','HEAD'],text=True).strip()
assert vals['meta_local_commit']=='fd60db96806a372404bd4f04e68d4ba586290147'
assert vals['paused_llvm_local_commit']=='569d734d0ccb2959e3f33494593c5cd46a01c347'
(E/'validation.json').write_text(json.dumps(vals,indent=2)+'\n')
(E/'README.md').write_text('''# build.conf project-wide audit, 2026-10-28

Read-only investigation; no package build, no Gerrit/QB changes.
Report: `docs/bolt/45_qb_meta_fix_and_snapshot.md`, sections 6–10.

- `config-classification.{json,tsv}`: all changed directives/macros, original line numbers and architecture conditions. Full input configs and diff remain in `../../../../qb-meta-fix-and-snapshot-20261028/snapshots/` (repository path: tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots).
- `source-index-1.html`, `srpm-list.txt`, `spec-acquisition.json`, `specs/`: all 365 indexed SRPM recipes, 256 source package names. HTTP streams stop after the header-listed specs; prefix digest is NOT the entire RPM digest. `content_length` is the server-reported RPM length; each extracted spec has a full SHA256.
- `git-spec-provenance.json`, `git-specs/`: supplementary tizen_base branch reads; branch lookup and archive are separately recorded.
- `git-qb-spec-provenance.json`, `qb-specs/`: missing or version-mismatching recipes retrieved by explicit QB commit. No source scripts executed.
- `project-spec-coverage.json`: 245 current manifest repositories and 251 actual QB repositories; union 252. The 251 actual repositories all have matching-commit recipes. tensorflow2 appears only in the current manifest.
- `spec-macro-usage.*`: all 403 retained spec records, exact lines and comment flags; old and current variants intentionally coexist. `package-impact.*` has 285 labels, NOT 285 distinct current project repositories (source-package labels and Gerrit repository labels overlap).
- `project-impact.json`: 252 repository rows corresponding to the report; effects are conditional static analysis, not build outcomes.
- `critical-spec-excerpts.txt`, `macro-coverage.json`: branch-specific text and all 31 changed macro names, including zero direct matches.
- `query-*`, `query-results.json`: 24 read-only queryconfig calls, not RPM spec/build certification.
- `*-config-flow.txt`: original log line numbers. `toolchain-*`, `repository-*`, `*-history*`, `*-diffs.txt`: metadata and history evidence. `tools-override-example.txt` preserves an initial wrong-path lookup error; the corrected Tools files are named `tools-example-*`.
- `validation.json`: source completeness/SHA, local report links and preserved local commits.
- `scripts/`: collection/analysis scripts retained for inspection, with original absolute local paths. They write evidence locally, do not build packages or change project configuration. Not a portable installation script.

No evidence establishes the final NGBS merged RPM macro set. The unchanged Toolchain project_config and Base get_build_conf_text URL must not be conflated. No credentials/cookies/authentication headers are collected.
''')
# Correct concise relative link text; the repository path above is authoritative.
p=E/'README.md';p.write_text(p.read_text().replace('../../../../qb-meta-fix-and-snapshot-20261028/snapshots/','../../../qb-meta-fix-and-snapshot-20261028/snapshots/'))
paths=sorted(p for p in E.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
(E/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(E))+'\n' for p in paths))
print(json.dumps({'files':len(paths),'bytes':sum(p.stat().st_size for p in paths),'links':len(links),'validation':'PASS'},indent=2))
