from pathlib import Path
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import bench

class BenchTests(unittest.TestCase):
    def test_affinity_validation(self):
        self.assertEqual(bench.parse_cpus("2,4-6",set(range(8))),[2,4,5,6])
        for v in ("1-5","3-2","8","2;ls","2,"):
            with self.subTest(v=v), self.assertRaises(ValueError):
                bench.parse_cpus(v,set(range(8)))

    def test_rotation(self):
        variants=["V0","V1","V2","V3"]
        self.assertEqual([bench.rotation(variants,i)[0] for i in range(5)],["V0","V1","V2","V3","V0"])

    def test_quartiles(self):
        self.assertIsNone(bench.quartiles([]))
        self.assertEqual(bench.quartiles([3])["iqr"],0)
        self.assertEqual(bench.quartiles([5,9,1])["median"],5)
        self.assertEqual(bench.quartiles([5,9,1])["iqr"],4)

    def test_memory_wait(self):
        with patch("bench.available",side_effect=[bench.MIN_AVAILABLE-1,bench.MIN_AVAILABLE]),                 patch("bench.time.sleep") as sleep, patch("bench.time.monotonic",side_effect=[5,15]),                 patch("bench.sys.stderr"):
            self.assertEqual(bench.memory_guard(),10)
            sleep.assert_called_once_with(10)

    def test_argv_is_compile_only(self):
        variant={"loader":"/r/loader","library_path":["/r/lib","/r/usr/lib"],"clang":"/r/clang"}
        tu={"flags":["--target=x86_64-tizen-linux-gnu","-O2"],"language":"c++","path":"/d/space folder/unit.ii"}
        cmd=bench.argv_for(variant,tu,Path("/out/sample.o"))
        self.assertEqual(cmd[:5],["/r/loader","--inhibit-cache","--library-path","/r/lib:/r/usr/lib","/r/clang"])
        self.assertEqual(cmd[-5:],["c++-cpp-output","-c","/d/space folder/unit.ii","-o","/out/sample.o"])
        self.assertIn("-fintegrated-cc1",cmd)

    def test_objects_compare_bytes_and_mark_difference(self):
        with tempfile.TemporaryDirectory() as where:
            base=Path(where)/"a"
            other=Path(where)/"b"
            base.write_bytes(b"AAA")
            other.write_bytes(b"BBB")
            os.utime(other,ns=(base.stat().st_atime_ns,base.stat().st_mtime_ns))
            row={"variants":{"V0":{"measurements":[{"tu":"x","object":{"path":str(base)}}]},
                             "V1":{"measurements":[{"tu":"x","object":{"path":str(other)}}]}}}
            self.assertEqual(bench.compare_round(row,"V0")[0]["status"],"DIFFERENT")
            row["variants"]["V1"]["measurements"][0].pop("object")
            self.assertEqual(bench.compare_round(row,"V0")[0]["status"],"UNVERIFIED")

    def test_statistics_skip_failed_rounds(self):
        def block(wall,status):
            return {"tu_wall_seconds_sum":wall,"tu_cpu_seconds_sum":wall/2,
                    "elapsed_seconds":wall,"all_passed":status=="PASS",
                    "measurements":[{"tu":"a","wall_seconds":wall,"status":status}]}
        rows=[{"variants":{"V0":block(2,"PASS"),"V1":block(1,"PASS")},"comparisons":[]},
              {"variants":{"V0":block(10,"FAIL"),"V1":block(9,"FAIL")},"comparisons":[]}]
        data=bench.summarize(rows,["V0","V1"],"V0",1)
        self.assertEqual(data["V1"]["total_seconds"]["count"],1)
        self.assertEqual(data["V1"]["speedup_vs_baseline"],2)
        self.assertEqual(data["V1"]["per_tu_speedup"],{"a":2})

    def test_two_rounds_parallel_json_and_markdown(self):
        cpus=sorted(os.sched_getaffinity(0))[:2]
        with tempfile.TemporaryDirectory() as where:
            d=Path(where)
            loader=d/"loader"
            loader.write_text("#!/usr/bin/python3\nimport pathlib,sys\n"
                "args=sys.argv[1:]\nvariant=pathlib.Path(args[3]).name\n"
                "out=pathlib.Path(args[args.index('-o')+1])\n"
                "out.write_bytes(b'changed' if variant=='V1' and out.stem=='b' else b'object')\n")
            loader.chmod(0o755)
            variants={}
            for n in ("V0","V1"):
                p=d/n
                p.write_text(n)
                variants[n]={"status":"PASS","loader":str(loader),"library_path":[str(d)],
                             "clang":str(p),"sha256":bench.digest(p)}
            inputs=[]
            for n in ("a","b"):
                p=d/(n+".i")
                p.write_text("int hello;\n")
                inputs.append({"id":n,"path":str(p),"sha256":bench.digest(p),"flags":["-O2"],"language":"c","package":"test"})
            with patch("bench.available",return_value=bench.MIN_AVAILABLE):
                bench.run_bench({"inputs":inputs,"variants":variants},d/"out",rounds=2,jobs=len(cpus),cpus=cpus,
                                variants=["V0","V1"],label="test",timeout=10,other_comm=[])
            result=json.loads((d/"out/results.json").read_text())
            self.assertEqual(result["rounds"][1]["order"],["V1","V0"])
            self.assertEqual(result["summary"]["V1"]["object_comparisons"],{"IDENTICAL":2,"DIFFERENT":2})
            self.assertIn("🔴",(d/"out/results.md").read_text())
            self.assertIn("max_rss_bytes",result["rounds"][0]["variants"]["V0"]["measurements"][0])

if __name__=="__main__":
    unittest.main()
