import glob
import time
import subprocess
from pathlib import Path

NINJA_HEADER = """
rule org2md
  command = emacs --batch -l ~/.emacs.d/init.el -l publish.el --eval \"(jethro/publish \\"$in\\")"
  description = org2md $in
"""

def get_files():
    return set(glob.glob("roam/**.org"))

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
    subprocess.call(["ninja"])


def monitor():
    # TODO: can use kernel hooks, but seems to interact weirdly with some things.
    files = None
    while True:
        new_files = get_files()
        if files is None or files != new_files:
            files = new_files
            ninja(new_files)
        time.sleep(10)



if __name__ == "__main__":
    subprocess.Popen(["hugo", "server", "--port", "1111"])
    print("starting monitor.")
    monitor()
