#!/usr/bin/env python3
"""Entry program for news-image-20261118.

Copies the front-page image held in this repository to the output
directory the grader provides. Standard library only, no network,
fully deterministic: the same bytes are written on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Fail loudly instead of handing the grader a truncated copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png copy is incomplete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
