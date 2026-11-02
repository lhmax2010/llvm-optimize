#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH GTK_IM_MODULE
if ! mkdir '/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/evidence/install-test-20261102-resume2/askpass-used' 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='Debuglink 第5项：一次授权完成装包、崩溃验证与卸载'
