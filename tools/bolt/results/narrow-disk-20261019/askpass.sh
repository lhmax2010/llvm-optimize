#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH GTK_IM_MODULE
if ! mkdir /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/askpass-used; then exit 1; fi
exec /usr/bin/zenity --password --title='BOLT 收窄修订：一次授权完成 Tizen RPM 五项只读解析'
