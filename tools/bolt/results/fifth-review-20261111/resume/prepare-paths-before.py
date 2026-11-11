from pathlib import Path
def rewrite(text, root):
    return text.replace("Path(__file__).parent/'results", "Path("+repr(str(root))+")/'")
