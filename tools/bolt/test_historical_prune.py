"""Historical audit only; never shipped as an RPM Source."""
from test_bolt_helper import Base,elf
from pathlib import Path
import bolt_helper as h
inventory=h.inventory;require=h.require

def prune_install(root, baseline, installed_paths):
    root = Path(root).absolute(); before = baseline['files']; after = inventory(root)['files']
    require(before.keys() <= after.keys(), 'ordinary install file removed before BOLT cleanup')
    added = set(after) - set(before)
    allowed = {Path(p).relative_to(root).as_posix() for p in installed_paths}
    for key in sorted(added, key=lambda x: (x.count('/'), x), reverse=True):
        path = root/key
        require(after[key]['type'] == 'dir' or key in allowed, 'unregistered install addition: '+key)
        if after[key]['type'] == 'dir':
            path.rmdir()
        else:
            path.unlink()
    now = inventory(root)['files']; require(now == before, 'install file list/type/mode differs after cleanup')
    return {'removed': sorted(added), 'file_list_equal': True}


class HistoricalPruneTests(Base):
    def root(self):
        r=self.d/"root";(r/"usr/bin").mkdir(parents=True);elf(r/"usr/bin/clang-22");return r
    def test_manifest_delta_deletes_every_registered_addition(self):
        r=self.root();before=h.inventory(r);(r/'usr/lib').mkdir();(r/'usr/lib/first.a').write_bytes(b'a');(r/'usr/lib/new-tool').symlink_to('../bin/clang-22')
        result=prune_install(r,before,[r/'usr/lib/first.a',r/'usr/lib/new-tool']);self.assertTrue(result['file_list_equal'])
    def test_unknown_addition_stops(self):
        r=self.root();before=h.inventory(r);(r/'usr/bin/unknown').write_bytes(b'x')
        with self.assertRaises(h.GateError):prune_install(r,before,[])
    def test_removed_ordinary_file_stops(self):
        r=self.root();before=h.inventory(r);(r/'usr/bin/clang-22').unlink()
        with self.assertRaises(h.GateError):prune_install(r,before,[])
