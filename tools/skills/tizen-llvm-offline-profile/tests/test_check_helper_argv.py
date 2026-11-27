import argparse
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_helper_argv import helper_parser, invocations, parse_invocations, shell_words


class HelperArguments(unittest.TestCase):
    def test_bash_preserves_word_boundaries_and_leaves_redirect_inert(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(shell_words('"$PWD/a b"--bolt-profile "bolt profile" > marker', root),
                             [str(root/"a b")+"--bolt-profile", "bolt profile"])
            self.assertEqual(shell_words('"$PWD/a b" --bolt-profile "bolt profile"', root),
                             [str(root/"a b"), "--bolt-profile", "bolt profile"])
            self.assertFalse((root/"marker").exists())
            self.assertEqual(shell_words("asset#1 # comment", root), ["asset#1"])

    def test_command_substitution_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for fragment in ('"$(touch marker)"', chr(96)+"touch marker"+chr(96), "arg\n: > marker"):
                with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                    shell_words(fragment, root)
            self.assertFalse((root/"marker").exists())

    def test_uses_the_helper_parser_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            helper = Path(tmp)/"clang-bolt-helper.py"
            helper.write_text(
                "import argparse\n"
                "def main():\n"
                "    parser = argparse.ArgumentParser()\n"
                "    parser.add_argument('path')\n"
                "    args = parser.parse_args()\n"
                "    raise AssertionError('unexpected dispatch')\n"
            )
            self.assertEqual(helper_parser(helper).parse_args(["a b"]).path,"a b")

    def test_profile_arguments_and_forwarded_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = root/"clang-bolt-helper.py"
            parser = argparse.ArgumentParser()
            sub = parser.add_subparsers(dest="cmd",required=True)
            prepare = sub.add_parser("pgo-prepare")
            for name in ("manifest","project","work","profile"):
                prepare.add_argument(name)
            prepare.add_argument("--bolt-profile")
            sub.add_parser("pgo-check-ninja")
            sub.add_parser("pipeline").add_argument("--debug-symbols",action="store_true")
            sub.add_parser("post")
            manifest, pgo, fdata = [root/name for name in ("manifest","train.profdata.xz","train.fdata.xz")]
            launcher = f"python3 -B {helper} "
            sample = [f'{launcher}pgo-prepare "{manifest}" T "$PWD/pgo-profiles" "{pgo}"{{sep}}--bolt-profile "{fdata}" || exit 1',
                      launcher+"pgo-check-ninja",launcher+"pipeline --debug-symbols",launcher+"post"]
            for sep in ("", " "):
                expanded = "\n".join(sample).replace("{sep}",sep)
                calls, errors = parse_invocations(expanded,helper,parser,root,"T",True,True,pgo,fdata,manifest)
                self.assertEqual(len(calls),4)
                if not sep:
                    self.assertIn("unrecognized arguments",errors[0]["error"])
                else:
                    self.assertEqual(errors,[])
            template = ('BOLT_WORK="$PWD/log area"\n'
                        f' bolt_checked "$bolt_stage" "$BOLT_WORK/log" {launcher}'
                        'run-step "$bolt_stage" "$BOLT_WORK/log" -- "$@"\n'
                        'bolt_step relink /bin/echo "quoted child argument"\n')
            row, = invocations(template,helper,root)
            self.assertEqual(row[3], ["run-step","relink",str(root/"log area/log"),
                                      "--","/bin/echo","quoted child argument"])


if __name__=="__main__":
    unittest.main()
