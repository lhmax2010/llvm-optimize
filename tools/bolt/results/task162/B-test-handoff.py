from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import os
import sys
import unittest

A=Path(__file__).resolve().parent
RUN=A.parent/"task160/run"
sys.path.insert(0,str(RUN/"orchestration"))
from handoff import BUILD, SUFFIX, attach_g4, namespace_command, preserve_clang, receipt, verify_handoff


class HandoffTest(unittest.TestCase):
    def setUp(self):
        temp=TemporaryDirectory(dir=A)
        self.addCleanup(temp.cleanup)
        self.archive=Path(temp.name)
        self.stage=self.archive/"G4"
        self.root=self.stage/SUFFIX
        self.build=self.root/BUILD
        (self.build/"bin").mkdir(parents=True)
        self.clang=self.build/"bin/clang-22"
        self.clang.write_bytes(b"executable")
        self.graph=self.build/"build.ninja"
        self.graph.write_text("ninja_required_version = 1.13\n")
        self.rpm=self.stage/"gbs-driver/local/repos/test.rpm"
        self.rpm.parent.mkdir(parents=True)
        self.rpm.write_bytes(b"package")
        (self.stage/"pgo-clang.json").write_text(json.dumps(receipt(self.clang)))

    def test_attach_does_not_move_root_or_rpms(self):
        before=self.root.stat().st_ino
        result=preserve_clang(self.archive)
        self.assertEqual(verify_handoff(self.archive),self.root)
        self.assertEqual(self.root.stat().st_ino,before)
        self.assertFalse((self.archive/"G5"/SUFFIX).exists())
        self.assertEqual(self.rpm.read_bytes(),b"package")
        self.assertEqual(result["sha256"],receipt(self.clang)["sha256"])

    def test_changed_graph_or_clang_blocks_handoff(self):
        attach_g4(self.archive,receipt(self.clang))
        self.graph.write_text("changed\n")
        with self.assertRaisesRegex(ValueError,"Ninja graph"):
            verify_handoff(self.archive)
        attach_g4(self.archive,receipt(self.clang))
        self.clang.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"clang changed"):
            verify_handoff(self.archive)

    def test_namespace_uses_current_uid_and_original_working_directory(self):
        command=namespace_command(self.root,["/usr/bin/ninja","-t","query","bin/clang-22"])
        self.assertEqual(command[0],"/usr/bin/bwrap")
        self.assertEqual(command[command.index("--uid")+1],str(os.getuid()))
        self.assertEqual(command[command.index("--chdir")+1],"/"+str(BUILD))
        self.assertEqual(command[command.index("--ro-bind")+1],str(self.root))
        writable=namespace_command(self.root,["/usr/bin/ninja"],writable=True)
        self.assertEqual(writable[writable.index("--bind")+1],str(self.root))

    def test_failed_g5_keeps_g4_root_and_rpm(self):
        with patch.object(sys,"argv",["dispatch","/workspace","/evidence",str(self.archive)]):
            import dispatch
        (self.archive/"G5").mkdir()
        row={"step":"G5","status":"FAIL"}
        with patch.object(dispatch,"A",self.archive):
            dispatch.finish_stage(row)
        self.assertTrue(self.clang.is_file())
        self.assertTrue(self.rpm.is_file())


if __name__=="__main__":
    unittest.main()
