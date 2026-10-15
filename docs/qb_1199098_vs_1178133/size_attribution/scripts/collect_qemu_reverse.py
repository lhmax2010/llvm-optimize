from common import *
old='e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f';new='2737f3bf78ed33be4333114c0e5c741a1deca467'
fetch(f'https://git.tizen.org/cgit/platform/upstream/qemu-accel/patch/?id={old}&id2={new}',RAW/'qemu-accel_reverse_range.patch')
