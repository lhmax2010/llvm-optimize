#!/usr/bin/python3
import os,sys
from pathlib import Path
Path(sys.argv[1]).write_bytes(Path(os.environ["MESSAGE_FILE"]).read_bytes())
