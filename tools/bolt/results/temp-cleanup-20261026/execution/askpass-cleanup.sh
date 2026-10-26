#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH
set -C
if ! ( : > "$CLEANUP_ASKPASS_MARKER" ) 2>/dev/null; then exit 1; fi
exec /usr/bin/zenity --password --title='LLVM 清理：仅删除用户批准的精确目录'
