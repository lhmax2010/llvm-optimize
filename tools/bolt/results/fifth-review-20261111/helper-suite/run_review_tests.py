#!/usr/bin/env python3
"""Run the review fixtures against an explicitly selected production helper."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import sys
import unittest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--helper', required=True, type=Path)
    parser.add_argument('--pattern', default='test_*.py')
    args = parser.parse_args()
    path = args.helper.resolve(strict=True)
    print('REVIEW_HELPER path=%s sha256=%s' %
          (path, hashlib.sha256(path.read_bytes()).hexdigest()), flush=True)
    spec = importlib.util.spec_from_file_location('bolt_helper', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['bolt_helper'] = module
    spec.loader.exec_module(module)
    tests = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern=args.pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
