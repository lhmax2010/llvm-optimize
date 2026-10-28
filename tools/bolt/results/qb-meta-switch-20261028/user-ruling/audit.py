"""Offline log/provider audit. No builds, network, or project-config changes."""
import collections, gzip, hashlib, json, pathlib, re, xml.etree.ElementTree as ET
HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
RESULTS = E.parent
INPUTS = {}
def read(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    INPUTS[str(p.relative_to(RESULTS))] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    return b
def js(p): return json.loads(read(p))
def log(p): return gzip.decompress(read(p)).decode().splitlines()
def save(name, data): (HERE/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
def excerpt(name, ls, ranges):
    with (HERE/name).open('w') as f:
        for a,b in ranges:
            f.write(f'--- original lines {a}-{b} ---\n')
            for i in range(a,b+1): f.write(f'L{i}: {ls[i-1]}\n')
logs = {
'1202084': log(RESULTS/'qb-timeout-20261021/child/1202084-full-log.txt.gz'),
'1211018': log(RESULTS/'qb-fail-20261028/1211014/1211018-child-full-log.txt.gz'),
}
for n in ('1209720','1209725','1209726','1209727'):
    logs[n]=log(E/f'qb/{n}-full-log.txt.gz')
excerpt('1202084-cross-spec.txt',logs['1202084'],[(648,660),(713,719),(753,757),(793,797),(987,991),(1015,1019),(1094,1108),(1339,1348),(1421,1430)])
ls=logs['1211018']; starts=[i for i,l in enumerate(ls,1) if re.search(r'check package (?:gcc|binutils)(?:-(?:armv7hl|armv7l|aarch64|riscv64))?$',l)]
excerpt('1211018-cross-spec.txt',ls,[(i,i+22 if 'gcc' in ls[i-1] else i+18) for i in starts])
for n in ('1202084','1211018'):
    data=js(RESULTS/f'qb-fail-20261028/meta/buildconf/{n}-package-lists.json')
    save(n+'-repo-entries.json',data if not isinstance(data,list) else [{k:v for k,v in x.items() if k not in ('packages','build_pkg_list_dic')} | {'gcc_binutils': {k:v for k,v in x.get('packages',x.get('build_pkg_list_dic',{})).items() if k in ('platform/upstream/gcc','platform/upstream/binutils')}} for x in data])
# Missing provider rows: recompute from raw primary-derived package lists, including provides and files.
old=js(E/'repos/toolchain/packages-all.json'); new=js(E/'repos/base/packages-all.json')
def providers(pkgs, name, arch):
    return sorted({p['name']+'.'+p['arch'] for p in pkgs if p['arch'] in (arch,'noarch') and (p['name']==name or name in p.get('files',[]) or any(x['name']==name for x in p['provides']))})
waivers=[]
for x in js(E/'base-config-providers.json'):
    if not x['providers']:
        a=providers(old,x['name'],x['arch']); b=providers(new,x['name'],x['arch'])
        assert a==x['old_same_arch_providers'] and b==[]
        waivers.append(dict(x,old_recomputed=a,new_recomputed=b,ruling='pre-existing absence; waived' if not a else 'NEW REGRESSION'))
save('provider-waivers.json',waivers)
with (HERE/'provider-waivers.tsv').open('w') as f:
    f.write('architecture\tdirective\tname\tconfig_lines\told_providers\tnew_providers\truling\n')
    for x in waivers:f.write('\t'.join([x['arch'],x['directive'],x['name'],','.join(map(str,x['config_lines'])),str(x['old_recomputed']),str(x['new_recomputed']),x['ruling']])+'\n')
rels=[{k:p[k] for k in ('name','arch','ver','rel','source','location','checksum','vcs')} for p in old if p['name'] in ('gcc','binutils','gcc-armv7hl','binutils-armv7hl') and p['arch'] in ('x86_64','armv7l','aarch64')]
save('old-release-comparison.json',rels)
# Positive mechanism evidence plus explicit bounds on what it proves.
excerpt('1209720-mechanism.txt',logs['1209720'],[(1154,1172),(1290,1294),(2334,2344),(3386,3391),(3424,3466),(3911,3920),(3922,3934),(6278,6283)])
excerpt('1209727-mechanism.txt',logs['1209727'],[(315,352),(387,394),(430,434)])
excerpt('1211018-mechanism.txt',logs['1211018'],[(312,350),(389,401),(428,442),(509,510)])
patterns = {
 'snapshot_info': r'\bsnapshot_info\b',
 'manifest_url': r'https?://[^\s\'\"]*(?:manifest|\.xml)(?:\b|/)',
 'project_config': r'\bproject_config\b',
 'build_conf_assembly': r'(?:append|concatenat|cat\s)[^\n]{0,120}?(?:project_config|build\.conf)|(?:project_config|build\.conf)[^\n]{0,120}?(?:append|concatenat|bytes|size)',
 'manifest_input_label': r'\b(?:MANIFEST_ORIG|MANIFEST_REF|Manifest_URL)\b',
}
search={}
for n,ls in logs.items():
    search[n]={k:[{'line':i,'text':l} for i,l in enumerate(ls,1) if re.search(p,l,re.I)] for k,p in patterns.items()}
save('mechanism-search.json',{'patterns':patterns,'results':search})
q=js(E/'qb/1209720-packages.json')[0]['packages']
manifest_checks=[]
for p in (E/'repos/unified-toolchain/tizen-unified-toolchain_20261016.052151_standard.xml',E/'metadata/Tizen-Unified-Toolchain/manifest.xml'):
    root=ET.fromstring(read(p)); m={x.attrib['name']:x.attrib.get('revision') for x in root.iter('project')}
    manifest_checks.append({'file':str(p.relative_to(RESULTS)),'repos':len(m),'same_revision':sum(q.get(n)==v for n,v in m.items()),'missing_from_log':sorted(set(m)-set(q)),'extra_in_log':sorted(set(q)-set(m)),'changed':[{ 'repo':n,'manifest':v,'qb':q.get(n)} for n,v in m.items() if q.get(n)!=v]})
# Parent pre-resolved MANIFEST_REF/ORIG, before explicit user revision override.
blocks={}
ls=logs['1209720']
for label,a,b in [('MANIFEST_ORIG',1292,2337),('MANIFEST_REF',2341,3386)]:
    d={}
    for i in range(a,b+1):
        s=ls[i-1].split('INFO  - ',1)[-1]; n,rev=s.rsplit('@',1);d[n]=rev
    blocks[label]={'count':len(d),'same_as_snapshot':d=={x.attrib['name']:x.attrib['revision'] for x in ET.fromstring(read(E/'repos/unified-toolchain/tizen-unified-toolchain_20261016.052151_standard.xml')).iter('project')}}
save('manifest-ambiguity.json',{'comparisons':manifest_checks,'resolved_blocks':blocks,'conclusion':'Reference snapshot and meta manifest have identical repo/revision maps. Logs show resolved manifest variables, not the manifest loading URL or its selection code; cannot distinguish origins.'})
save('input-sha256.json',INPUTS)
print(json.dumps({'waived_rows':len(waivers),'new_regressions':sum(bool(x['old_recomputed']) for x in waivers),'manifest_comparisons':manifest_checks,'resolved_blocks':blocks},ensure_ascii=False,indent=2))
