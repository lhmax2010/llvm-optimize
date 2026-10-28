#!/bin/sh
set -e
cd "$1/usr"
(test ! -d lib/debug || find lib/debug ! -type d) | sed "s,^,/usr/,"
