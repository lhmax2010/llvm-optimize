#!/bin/sh
# One graphical prompt only, including sudo authentication retries.
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
session_dir=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261015-install-rehearsal
if ! mkdir "$session_dir/askpass-used" 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='BOLT %install 演练：仅本次 overlay 挂载与清理需要 sudo'
