from pathlib import Path
import re
def rewrite(text, root):
    return re.sub(r"Path\(__file__\)\.parent/'results([^']*)'",
                  lambda m: "Path("+repr(str(root))+")/"+repr(m.group(1).lstrip('/')), text)
