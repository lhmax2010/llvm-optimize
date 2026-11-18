"""Prepare or run an offline PGO/BOLT pair using a separately approved N0 driver.

The default checkout supplies only dry-run inputs. The driver must implement the
resource admission/watchdog policy and return successful, qualified build outputs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import lzma
import os
import shutil
import subprocess

E = Path(__file__).resolve().parent
B = E.parents[3]
W = B.with_name('llvm-optimize')
HISTORY = B/'tools/bolt/results/pgo-bolt-followup-20261105/training.json'
ASSETS = W/'temp/bolt-aarch64-v2-20260921/profile-v2-manifest.json'
GENERATOR = W/'tools/bench_inputs/generate_synthetic.py'
STAGES = [
    ('instrumented-build', 4068.547, 7227248640, '58 §4 A'),
    ('ir-train', 201.930, 1481818112, '58 §4 B'),
    ('merge-profdata', 3.278, 1824751616, '58 §4 C'),
    ('pgo-build', 6176, 21703991296, '58 §4 D ordinary compile'),
    ('bolt-tools', 418, None, '58 §4 BOLT tools'),
    ('relink-strip-debug', None, None, '58 §4 cannot separate from failed rewrite'),
    ('bolt-instrument', 77.954, 17074352128, '59 §7'),
    ('bolt-train', 379.427, 3890348032, '59 §7'),
    ('merge-fdata', 3.396, 1585553408, '59 §7'),
    ('write-manifest', None, None, 'no historical compressed-pair measurement'),
]


def identify(path):
    with path.open('rb') as stream:
        return {'path': str(path), 'bytes': path.stat().st_size,
                'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def inputs():
    original = json.loads(HISTORY.read_text())
    if len(original) != 23 or len({row['name'] for row in original}) != 23:
        raise ValueError('training inventory must contain the 23 recorded entries')
    recipes = {}
    if ASSETS.is_file():
        for corpus in json.loads(ASSETS.read_text())['corpora']:
            for row in corpus['inputs_flags_manifest']:
                if row['name'] in ('A','B','C'):
                    recipes[row['name']] = {'scale': row['scale'], 'seed': corpus['seed']}
    result = []
    for row in original:
        path = Path(row['path'])
        if path.is_file():
            got = identify(path)
            if got['bytes'] != row['bytes'] or got['sha256'] != row['sha256']:
                raise ValueError('historical training input changed: '+str(path))
        result.append({**row, 'recorded_input_available': path.is_file(),
                       'regenerate': recipes.get(row['name']) if row['synthetic'] else None})
    return result


def dry_run(rows):
    return {
        'mode':'dry-run', 'executes_builds':False,
        'stages':[{'stage': k,'historical_seconds': sec,'historical_memory_bytes': mem,
                   'source':source} for k, sec, mem, source in STAGES],
        'known_seconds_subtotal':sum(sec for _,sec,_,_ in STAGES if sec is not None),
        'historical_peak_memory_bytes':21703991296,
        'historical_root_coexist_boundary_bytes':91275411456,
        'planned_known_disk_with_reserve_gib':125.626,
        'disk_sources':'58 §6 coexistence boundary; 59 §7 includes 30 GiB reserve',
        'admission':'approved N0 configuration/driver required; one deferred retry at most after 30 minutes',
        'unverified':['N0 normal/reduced tiers and watchdog values',
                      'PS5-specific instrumented and final build commands',
                      'same-input BOLT rewrite and package gates are separate qualification'],
        'training':rows,
    }


def train_command(argv, flags, path, target):
    if any(not Path(v.split('=',1)[1]).exists() for v in flags
           if v.startswith(('--sysroot=','-resource-dir='))):
        raise ValueError('historical training sysroot/resource directory is absent')
    return [*argv,*flags,'-c',str(path),'-o',str(target)]


def execute(config, root, rows):
    if config.get('n0_reviewed') is not True:
        raise RuntimeError('STOP: no separately reviewed N0 driver/configuration')
    driver=Path(config['n0_driver'])
    plan=Path(config['n0_plan'])
    if not (driver.is_absolute() and driver.is_file() and plan.is_absolute() and plan.is_file()):
        raise ValueError('N0 driver and plan must be existing absolute paths')
    if not root.is_absolute():
        raise ValueError('output directory must be absolute')
    root.mkdir(exist_ok=False)
    for name in ('raw','fdata','objects','inputs','logs'):
        (root/name).mkdir()

    def run(name, argv, extra_env=None, stdout_path=None):
        if not argv or not Path(argv[0]).is_absolute():
            raise ValueError('stage requires an absolute program: '+name)
        issue = [str(driver), '--plan', str(plan), '--stage', name, '--', *argv]
        env = {**os.environ, **(extra_env or {})}
        dump(root/'logs'/(name+'.argv.json'), issue)
        with (root/'logs'/(name+'.log')).open('xb') as stream:
            if stdout_path is None:
                subprocess.run(issue, cwd=root, env=env, stdout=stream,
                               stderr=subprocess.STDOUT, check=True)
            else:
                with stdout_path.open('xb') as output:
                    subprocess.run(issue, cwd=root, env=env, stdout=output, stderr=stream, check=True)

    for row in rows:
        path = Path(row['path'])
        if not path.is_file():
            recipe = row['regenerate']
            if not recipe:
                raise RuntimeError('STOP: missing training input '+str(path))
            output = root/'inputs'/row['name']
            subprocess.run(['/usr/bin/python3','-B',str(GENERATOR),str(output),
                            '--scale',str(recipe['scale']),'--seed',str(recipe['seed'])],check=True)
            path=output/(row['name']+'.cpp')
        actual=identify(path)
        if (actual['bytes'],actual['sha256'])!=(row['bytes'],row['sha256']):
            raise RuntimeError('STOP: training input does not match historical identity '+str(path))
        row['verified_input']=actual
    paths={'output':str(root),'profdata':str(root/'clang.profdata')}
    values=lambda argv:[arg.format_map(paths) for arg in argv]
    run('instrumented-build',values(config['commands']['instrumented-build']))
    tools={}
    for name in ('instrumented_clang','llvm_profdata'):
        tools[name]=identify(Path(config['tools'][name]['binary'].format_map(paths)))
        run(name+'-version',values(config['tools'][name]['argv'])+['--version'])
        tools[name]['version']=(root/'logs'/(name+'-version.log')).read_text(errors='replace')
    for index,row in enumerate(rows):
        flags=row['compiler_args']
        source=Path(row['verified_input']['path'])
        argv=train_command(values(config['tools']['instrumented_clang']['argv']),flags,source,
                           root/'objects'/f'ir-{index:02d}.o')
        run(f'ir-train-{index:02d}',argv,{'LLVM_PROFILE_FILE':str(root/'raw'/f'{index:02d}-%m-%p.profraw')})
    raw=sorted((root/'raw').glob('*.profraw'))
    if len(raw)!=23:
        raise RuntimeError('STOP: expected 23 individual IR training profiles')
    run('merge-profdata',values(config['tools']['llvm_profdata']['argv'])+
        ['merge','-o',paths['profdata'],*map(str,raw)])
    for stage in ('pgo-build','bolt-tools','relink-strip-debug'):
        run(stage,values(config['commands'][stage]))
    for name in ('llvm_bolt','merge_fdata','bolt_clang'):
        tools[name]=identify(Path(config['tools'][name]['binary'].format_map(paths))) if name!='bolt_clang' else None
        if name!='bolt_clang':
            run(name+'-version',values(config['tools'][name]['argv'])+['--version'])
            tools[name]['version']=(root/'logs'/(name+'-version.log')).read_text(errors='replace')
    relocs=Path(config['bolt_input'].format_map(paths))
    runtime=Path(config['bolt_runtime'].format_map(paths))
    instrumented=Path(config['tools']['bolt_clang']['binary'].format_map(paths))
    run('bolt-instrument',values(config['tools']['llvm_bolt']['argv'])+
        [str(relocs),'-instrument','--thread-count=1','-runtime-instrumentation-lib='+str(runtime),
         '-instrumentation-file='+str(root/'fdata/clang'),'-instrumentation-file-append-pid',
         '-instrumentation-binpath='+str(instrumented),'-o',str(instrumented)])
    tools['bolt_clang']=identify(instrumented)
    run('bolt_clang-version',values(config['tools']['bolt_clang']['argv'])+['--version'])
    tools['bolt_clang']['version']=(root/'logs/bolt_clang-version.log').read_text(errors='replace')
    for index,row in enumerate(rows):
        argv=train_command(values(config['tools']['bolt_clang']['argv']),row['compiler_args'],
                           Path(row['verified_input']['path']),root/'objects'/f'bolt-{index:02d}.o')
        run(f'bolt-train-{index:02d}',argv)
    fdata=sorted((root/'fdata').glob('clang*.fdata'))
    if len(fdata)!=23:
        raise RuntimeError('STOP: expected 23 separate BOLT training profiles')
    run('merge-fdata',values(config['tools']['merge_fdata']['argv'])+
        list(map(str,fdata)),stdout_path=root/'clang.fdata')
    assets={}
    for key, file in (('profdata','clang.profdata'),('bolt_profile','clang.fdata')):
        src=root/file
        dest=root/('clang-pgo.'+file.split('.',1)[1]+'.xz')
        with src.open('rb') as inp, lzma.open(dest,'wb',preset=6) as output:
            shutil.copyfileobj(inp,output)
        raw_id=identify(src); compressed=identify(dest)
        assets[key]={'file':dest.name,'bytes':raw_id['bytes'],'sha256':raw_id['sha256'],
                     'xz_bytes':compressed['bytes'],'xz_sha256':compressed['sha256']}
    warnings={'count':0,'first':None}
    for log in sorted((root/'logs').glob('*.log')):
        with log.open(errors='replace') as stream:
            for line in stream:
                if 'LLVM Profile Warning' in line:
                    warnings['count']+=1
                    if warnings['first'] is None:
                        warnings['first']={'file':str(log),'line':line.rstrip('\n')}
    project=config['project']
    if project not in ('T','D'):
        raise ValueError('unknown project identifier')
    dump(root/'llvm-profiles.manifest',{
        'format':1,'status':'UNQUALIFIED','llvm_version':'22.1.8',
        'source_identity':config['source_identity'], 'training':rows,
        'tools':tools,'bolt_input':identify(relocs),'bolt_instrumentation_runtime':identify(runtime),
        'instrumentation_warnings':warnings,
        'profiles':[{'project':project,'pgo':True,'bolt':False,'profdata':assets['profdata']},
                    {'project':project,'pgo':True,'bolt':True,**assets}],
    })


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--config',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rows=inputs()
    if args.dry_run:
        print(json.dumps(dry_run(rows),indent=2))
        return
    if args.config is None or args.output is None:
        parser.error('run requires approved --config and new --output')
    execute(json.loads(args.config.read_text()),args.output,rows)


if __name__=='__main__':
    main()
