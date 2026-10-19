#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
if ! mkdir /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/askpass-used; then exit 1; fi
exec /usr/bin/zenity --password --title='BOLT：一次授权完成只读 overlay RPM 认证与 1 MiB 写满测试'
