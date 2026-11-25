import json
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import after_154 as after

class QueueTest(unittest.TestCase):
    def test_active_154_child_defers_g4(self):
        r=CompletedProcess([],0,"llvm-opt-task154-full-build-1.service loaded active running\n","")
        with patch.object(after,"call",return_value=r):
            self.assertIn("active:",after.ready()[1])

    def test_published_final_is_required(self):
        r=CompletedProcess([],0,"","")
        with TemporaryDirectory() as temp, patch.object(after,"W",Path(temp)), patch.object(after,"call",return_value=r):
            self.assertEqual(after.ready(),(False,"154-B published receipt is missing"))

    def test_remote_ancestry_check(self):
        with TemporaryDirectory() as temp, patch.object(after,"W",Path(temp)):
            p=Path(temp)/"archive/task154"
            p.mkdir(parents=True)
            (p/"published-final.sha").write_text("f"*40+"\n")
            cmds=[CompletedProcess([],0,"",""),CompletedProcess([],0,"a"*40+"\trefs/heads/bolt-v4\n",""),
                  CompletedProcess([],0,"",""),CompletedProcess([],1,"","")]
            with patch.object(after,"call",return_value=CompletedProcess([],0,"","")),patch.object(after,"git",side_effect=cmds):
                self.assertEqual(after.ready(),(False,"154-B final receipt is not published on the evidence branch"))

if __name__=="__main__":
    unittest.main()
