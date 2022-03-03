#!/usr/bin/env python3
"""
A fixer script which crawls text files and replaces smartquotes with
normal quote characters.

This fixes copy-paste from some applications which replace double-quotes with curly
quotes.

For extra credit, it handles alternate encodings of quotation marks and
dingbats.

It does *not* convert corner brackets, braile quotation marks, or angle
quotation marks. Those characters are not typically the result of copy-paste
errors, so they are allowed.

Low quotation marks vary in usage and meaning by language, and some languages
use quotation marks which are facing "outwards" (opposite facing from english).
For the most part, these and exotic characters (double-prime quotes) are
ignored.

In files with the offending marks, they are replaced and the run is marked as
failed. This makes the script suitable as a pre-commit fixer.
"""
import re
import sys

from ._common import all_filenames, codepoints2chars, parse_cli_args
from ._recorders import DiffRecorder


def codepoints2regex(codepoints):
    return re.compile("(" + "|".join(codepoints2chars(codepoints)) + ")")


# Key -> Value
# Value: Characters to be replaced
# Key: What to replace Values with
REPLACEMENTS = {
    "–": "-"
}


def gen_line_fixer(translate_map):
    def line_fixer(line: str):
        return line.translate(translate_map)

    return line_fixer


def do_all_replacements(files) -> DiffRecorder:
    """Do replacements over a set of filenames, and return a list of filenames
    where changes were made."""
    recorder = DiffRecorder()

    line_fixer = gen_line_fixer(str.maketrans(REPLACEMENTS))
    for fn in all_filenames(files):
        recorder.run_line_fixer(line_fixer, fn)
    return recorder


def parse_args(argv):
    return parse_cli_args(__doc__, argv=argv, fixer=True)


def main(*, argv=None):
    args = parse_args(argv)
    changes = do_all_replacements(
        all_filenames(args.files),
    )
    if changes:
        changes.print_changes(args.show_changes, args.color)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
