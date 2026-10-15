from common import *
revs={'old':'e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f','new':'2737f3bf78ed33be4333114c0e5c741a1deca467'}
for side,rev in revs.items():
 fetch(f'https://git.tizen.org/cgit/platform/upstream/qemu-accel/plain/packaging/qemu-accel-armv7l.spec?h=tizen&id={rev}',RAW/f'qemu-accel_{side}_armv7l_retry.spec')
 fetch(f'https://git.tizen.org/cgit/platform/upstream/qemu-accel/commit/?id={rev}',RAW/f'qemu-accel_{side}_commit.html')
fetch(f'https://git.tizen.org/cgit/platform/upstream/qemu-accel/log/?id={revs["old"]}&qt=range&q={revs["new"]}..{revs["old"]}&showmsg=1',RAW/'qemu-accel_reverse_range_log.html')
