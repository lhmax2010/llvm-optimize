#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
session_dir=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261016-source-order
if ! mkdir "$session_dir/askpass-used" 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='LLVM Source 顺序修复：只读 overlay 中验证 RPM 解析'
