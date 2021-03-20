import glob
import time
import subprocess
from pathlib import Path

NINJA_HEADER = """
rule org2md
  command = output=`emacs --batch -l ~/.emacs.d/init.el -l publish.el --eval \"(jethro/publish \\"$in\\")" 2>&1` || echo $output
  description = org2md $in
"""

def get_files():
    return set(glob.glob("roam/zettel/*.org") + glob.glob("roam/lit/*.org"))

def write_build(files):
    with open('build.ninja', 'w') as ninja_file:
        ninja_file.write(NINJA_HEADER)
        ninja_file.write("\n")
        for f in files:
            if f.endswith("setup.org"):
                continue
            path = Path(f)
            output_file = f"content/posts/{path.with_suffix('.md').name}"
            ninja_file.write(f"build {output_file}: org2md {path}\n")

def ninja(files):
    write_build(files)
    time.sleep(5)
    while True:
        try:
            subprocess.check_call(["ninja"])
            break
        except:
            print("failed, trying again soon")
            time.sleep(10)


if __name__ == "__main__":
    files = get_files()
    ninja(files)
