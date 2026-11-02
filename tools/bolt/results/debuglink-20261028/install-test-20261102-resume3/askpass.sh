#!/bin/sh
set -eu
unset LD_LIBRARY_PATH LD_PRELOAD GTK_PATH GIO_MODULE_DIR GDK_PIXBUF_MODULE_FILE GI_TYPELIB_PATH GTK_IM_MODULE
E='/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/evidence/install-test-20261102-resume3'
[ ! -e "$E/askpass-cancelled" ] || exit 1
attempt=0
if [ -f "$E/askpass-count" ]; then read -r attempt < "$E/askpass-count"; fi
case "$attempt" in 0|1|2) ;; *) exit 1 ;; esac
attempt=$((attempt + 1))
printf '%s\n' "$attempt" > "$E/askpass-count"
printf '%s attempt=%s opened\n' "$(date -Iseconds)" "$attempt" >> "$E/auth-attempts.log"
if /usr/bin/zenity --password --title='LLVM debuglink 装包测试：请输入 sudo 密码'; then
    printf '%s attempt=%s submitted\n' "$(date -Iseconds)" "$attempt" >> "$E/auth-attempts.log"
    exit 0
else
    rc=$?
    : > "$E/askpass-cancelled"
    printf '%s attempt=%s cancelled-or-dialog-error rc=%s\n' "$(date -Iseconds)" "$attempt" "$rc" >> "$E/auth-attempts.log"
    exit 1
fi
