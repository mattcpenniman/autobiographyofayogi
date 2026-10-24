#!/usr/bin/env python3
"""Package only the self-contained public pages and their Apache policy."""

import argparse
from pathlib import Path
import tarfile


PUBLIC_FILES = ("index.html", "reader.html", ".htaccess")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New .tar.gz artifact outside the source tree")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if output == source or source in output.parents:
        parser.error("write the artifact outside the source tree")
    for name in PUBLIC_FILES:
        path = source / name
        if path.is_symlink() or not path.is_file():
            parser.error(f"missing public file or symlink: {name}")
    # Exclusive creation avoids overwriting an existing artifact.
    with output.open("xb") as stream:
        with tarfile.open(fileobj=stream, mode="w:gz") as archive:
            for name in PUBLIC_FILES:
                archive.add(source / name, arcname=name, recursive=False)
    print(f"Packaged {', '.join(PUBLIC_FILES)} into {output}")


if __name__ == "__main__":
    main()
