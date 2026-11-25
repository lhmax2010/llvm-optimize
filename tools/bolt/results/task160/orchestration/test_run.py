from pathlib import Path
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.argv[1:]=["/workspace","/evidence","/archive"]
import dispatch
from handoff import confined, cleanup, SUFFIX
from policy import GIB, admit, blocked, disk_limits, oom_killed, stop_line, terminal

class RunPlan(unittest.TestCase):
    def test_disk_floor_includes_decimal_30gb(self):
        self.assertEqual(disk_limits(222650722030)["G4"],302154457695)
        self.assertNotIn("N2",disk_limits(222650722030))
        self.assertEqual(disk_limits(1)["G6"],4948119552+15*GIB+30_000_000_000)

    def test_new_admission_waits(self):
        self.assertEqual(dispatch.admission_timeout("G4"),10800)
        self.assertEqual(dispatch.admission_timeout("G5"),3600)
        self.assertEqual(dispatch.G6_DEADLINE.isoformat(),"2026-11-27T06:00:00-08:00")

    def test_preferred_fallback_floor(self):
        self.assertEqual(admit("G6",22*GIB)["tier"],"preferred")
        self.assertEqual(admit("G6",22*GIB)["memory_max"],18*GIB)
        result=admit("G6",39*GIB//2)
        self.assertEqual((result["tier"],result["memory_max"],result["admitted"]),("fallback",16*GIB,True))
        self.assertFalse(admit("G6",39*GIB//2-1)["admitted"])
        self.assertEqual(admit("G6",50*GIB)["memory_max"],24*GIB)

    def test_g6_oom_is_terminal(self):
        self.assertTrue(oom_killed({"memory.events":"oom 2\noom_kill 1"},""))
        self.assertTrue(oom_killed({},"Result=oom-kill"))
        self.assertFalse(oom_killed({"memory.events":"oom 2\noom_kill 0"},""))
        self.assertEqual(terminal("G6","fallback","FAIL",{},True),("FAIL","fallback cgroup OOM; no retry"))
        self.assertTrue(blocked("G7",True))
        self.assertFalse(blocked("G5",False))

    def test_watchdog_followed_by_cleanup_and_admission(self):
        sample={"mem_available":3*GIB,"home_available":15*GIB-1}
        self.assertTrue(stop_line(sample))
        status,reason=terminal("G4","dynamic","FAIL",sample,False)
        self.assertEqual(status,"INTERRUPTED")
        before={"mem_available":3*GIB,"home_available":15*GIB-1}
        after={"mem_available":22*GIB,"home_available":350*GIB}
        row={"step":"G4","status":status,"watchdog":sample}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"G4").mkdir()
            with patch.object(dispatch,"A",root),patch.object(dispatch,"resources",side_effect=[before,after]),patch.object(dispatch,"cleanup",return_value=[]) as remove:
                dispatch.finish_stage(row)
            remove.assert_called_once_with(root/"G4",root)
            self.assertGreater(row["cleanup"]["df_delta"],0)
        self.assertFalse(blocked("G5",False))
        self.assertTrue(admit("G5",after["mem_available"])["admitted"])

    def test_step_cleanup_preserves_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            p=root/"N2"/SUFFIX
            p.mkdir(parents=True)
            (p/"object.o").write_bytes(b"object")
            (p/"saved.rpm").write_bytes(b"package")
            (p/".build.log").write_text("evidence")
            records=cleanup(root/"N2",root)
            self.assertEqual(records[0]["entries_removed"],1)
            self.assertTrue((p/"saved.rpm").is_file())
            self.assertTrue((p/".build.log").is_file())
            self.assertFalse((p/"object.o").exists())

    def test_whitelist_and_mounts(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            owner=base/"run"
            owner.mkdir()
            sibling=base/"foreign"
            sibling.mkdir()
            target=owner/"root"
            target.mkdir()
            jump=owner/"jump"
            jump.symlink_to(sibling,target_is_directory=True)
            self.assertEqual(confined(target,owner,set()),target)
            for bad in (owner,sibling,jump):
                with self.assertRaises(ValueError):
                    confined(bad,owner,set())
            with self.assertRaises(ValueError):
                confined(target,owner,{target/"mount"})

if __name__=="__main__":
    unittest.main(argv=[sys.argv[0]],verbosity=2)
