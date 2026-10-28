from pathlib import Path
import json,hashlib,subprocess,shutil,re,urllib.parse,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';R=W/'temp/qb-meta-20261028/repo';(E/'scripts').mkdir(exist_ok=True)
for p in D.glob('*.py'):shutil.copyfile(p,E/'scripts'/p.name)
for n in ['repos.log','base-checks.log','mlgo.log','unified-checks.log']:shutil.copyfile(D/n,E/n.replace('.log','.stdout.txt'))
prov=json.loads((E/'metadata-provenance.json').read_text());assert len(prov)==24
for r in prov:
 data=(E/r['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==r['sha256'];orig=subprocess.check_output(['git','-C',str(R),'show',r['git_commit']+':'+r['git_path']]);assert data==orig
 if Path(r['file']).name in ['project_meta','snapshot_info','manifest.xml','candidate_snapshot']:X.fromstring(data)
assert subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()=='fd60db96806a372404bd4f04e68d4ba586290147'
assert not subprocess.check_output(['git','-C',str(R),'status','--porcelain'],text=True).strip()
tests=json.loads((E/'mlgo/tests.json').read_text());assert len(tests)==4 and all(x['rc']==0 and x['object_bytes']>0 for x in tests)
for r in tests:assert (E/'mlgo'/r['stderr']).stat().st_size==0
base=json.loads((E/'base-missing-dependencies.json').read_text());assert all(len(r['missing_packages'])==11 and len(r['spec_hits'])==1 for r in base.values())
reference=X.parse(E/'unified-reference-build.xml').getroot().findtext('id');assert reference=='tizen-unified_20261027.231956'
readme='''# QB metadata switch: pre-upload evidence (2026-10-28)

Both reviews STOPPED and NOT UPLOADED. No Gerrit review IDs were created.
See docs/bolt/46_qb_meta_toolchain_switch.md for exact scope and stop conditions.

- metadata/: all original files for four relevant projects at master 7b2f2ae; SHA/path provenance in metadata-provenance.json. All project_config files unchanged.
- repos/: fixed snapshot metadata and package indexes. Base/Toolchain primary originals are already committed under tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots; their all-architecture parses are kept here. Unified primary checksums were verified against repomd.xml.
- base-missing-dependencies.json: raw and simple-macro-expanded spec dependencies, conditions, provides-name matches, versioned old binary Requires, and unresolved macro lines. Not a full RPM dependency solver.
- base-config-providers.* and unified-config-providers.*: all evaluated config directive RHS names and provider evidence. Substitute LHS names are triggers, not packages that must be installed. Keep and untriggered rules must not be equated with mandatory dependencies.
- unified-fixed-source-comparison.json / unified-repository-changes.tsv: fixed standard manifest vs current Toolchain and actual QB inventory. Metadata-only manifest comparison also retained; emulator-only repositories explain its different count.
- unified-missing-dependencies.json: old Unified RPM package names and Requires compared with new Unified and the hypothetical Unified+Base union. This union does not establish that QB can create the second DOD. Full Unified spec dependency certification was NOT RUN after the topology/source stop.
- qb/: authenticated overview and four complete read-only log downloads, gzip compressed. Only post-login rendered text/screenshot and download URLs are saved. No cookies/auth headers/forms. Actual recent job was GBS, no DOD creation command.
- mlgo/: four minimal C compile results, ELF outputs' identities, actual runtime loader listings, full stdout/stderr, URLs and checksums. RPM payloads stay under this task's temp directory, not committed. No RPM script/install, no linking or package build.
- debug-discovery.json / debug-layout.json: debug uses flat RPM files under debug/. Guessed debug/<arch>/ URLs returned404 and were corrected by inspecting the parent index; not a missing-debug verdict.
- scripts/: readonly collection/analysis and temporary compile scripts, tied to original local paths. They are evidence, not portable installers. No code/config mutations or upload logic.

The existing local fd60db96 two-line diff is base-existing.diff; no rebase or second local change was made. Debuglink work remains paused and excluded from this commit.
'''
(E/'README.md').write_text(readme)
validation=dict(metadata_files=len(prov),metadata_sha_and_git_bytes='PASS',original_xml='PASS',meta_worktree_clean=True,meta_local_head='fd60db96806a372404bd4f04e68d4ba586290147',mlgo_tests_passed=4,base_missing_per_arch={a:len(r['missing_packages']) for a,r in base.items()},base_spec_dependency_hit_per_arch={a:len(r['spec_hits']) for a,r in base.items()},unified_reference=reference,gerrit_push_attempted=False,base_review='STOP',unified_review='STOP',full_unified_spec_certification='NOT RUN after earlier stop conditions',qb_browser_closed=True)
(E/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
# Check report links after creating the checksum file.
(E/'SHA256SUMS').write_text('')
p=B/'docs/bolt/46_qb_meta_toolchain_switch.md';links=re.findall(r'\]\(([^)]+)\)',p.read_text());bad=[]
for url in links:
 if '://' in url or url.startswith('#'):continue
 if not (p.parent/urllib.parse.unquote(url.split('#')[0])).resolve().exists():bad.append(url)
assert not bad,bad
files=sorted(x for x in E.rglob('*') if x.is_file() and x.name!='SHA256SUMS')
(E/'SHA256SUMS').write_text(''.join(hashlib.sha256(x.read_bytes()).hexdigest()+'  '+str(x.relative_to(E))+'\n' for x in files))
print(json.dumps(dict(files=len(files)+1,bytes=sum(p.stat().st_size for p in files),max_file_bytes=max(p.stat().st_size for p in files),report_links=len(links),result='PASS (evidence validation only, not review gates)'),indent=2))
