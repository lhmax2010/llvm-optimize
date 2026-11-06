from pathlib import Path
import sys
Path(sys.argv[1]).write_bytes(Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/rebase-359934-20261106-r2/amend-message.txt').read_bytes())
