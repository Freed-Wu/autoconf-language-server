r"""Api
=======
"""
import os
from glob import glob
from gzip import decompress

from platformdirs import site_data_dir

START = " -- Macro: "
BEGIN = "‘"
END = "’"


def get_macro(line: str, begin: str = START, end: str = "") -> str:
    r"""Get macro.

    :param line:
    :type line: str
    :param begin:
    :type begin: str
    :param end:
    :type end: str
    :rtype: str
    """
    return line.lstrip(begin).rstrip(end).split("(")[0].strip()


def match(line: str, begin: str = START, end: str = "") -> bool:
    r"""Match.

    :param line:
    :type line: str
    :param begin:
    :type begin: str
    :param end:
    :type end: str
    :rtype: bool
    """
    return (
        line.startswith(begin)
        and line.endswith(end)
        and line.lstrip(begin).split("_")[0] in ["AC", "AM", "AH", "m4"]
    )


def reset(
    macros: dict[str, str], _macros: list[str], lines: list[str]
) -> tuple[dict[str, str], list[str], list[str]]:
    r"""Reset.

    :param macros:
    :type macros: dict[str, str]
    :param _macros:
    :type _macros: list[str]
    :param lines:
    :type lines: list[str]
    :rtype: tuple[dict[str, str], list[str], list[str]]
    """
    for macro in _macros:
        macros[macro] = "\n".join(lines)
    _macros = []
    lines = []
    return macros, _macros, lines


def get_content(filename) -> str:
    r"""Get content.

    :param filename:
    :rtype: str
    """
    filename = glob(os.path.join(site_data_dir("info"), filename + "*"))[0]
    with open(filename, "rb") as f:
        content = f.read()
        if filename.endswith(".gz"):
            content = decompress(content)
        content = content.decode()
    return content


def init_document() -> dict[str, str]:
    r"""Init document.

    :rtype: dict[str, str]
    """
    macros = {}

    _lines = get_content("autoconf.info").splitlines()
    _macros = []
    lines = []
    lastline = ""
    for line in _lines:
        # -- Macro: AC_INIT (PACKAGE, VERSION, [BUG-REPORT], [TARNAME], [URL])
        #     ...
        if match(line) and not match(lastline):
            macros, _macros, lines = reset(macros, _macros, lines)
            _macros += [get_macro(line)]
            lines += [line]
        # -- Macro: AC_CONFIG_MACRO_DIRS (DIR1 [DIR2 ... DIRN])
        # -- Macro: AC_CONFIG_MACRO_DIR (DIR)
        #     ...
        elif match(line) and match(lastline):
            _macros += [get_macro(line)]
            lines += [line]
        # ...
        #
        # ...
        # or not
        #    text indented 3 spaces is not document
        elif _macros and (len(line) < 4 or line[4] == " "):
            lines += [line]
        else:
            macros, _macros, lines = reset(macros, _macros, lines)
        lastline = line

    _lines = get_content("automake.info-1").splitlines()
    _macros = []
    lines = []
    lastline = ""
    for line in _lines:
        if match(line, BEGIN, END) and not match(lastline, BEGIN, END):
            macros, _macros, lines = reset(macros, _macros, lines)
            _macros += [get_macro(line, BEGIN, END)]
            lines += [line]
        elif match(line, BEGIN, END) and match(lastline, BEGIN, END):
            _macros += [get_macro(line, BEGIN, END)]
            lines += [line]
        elif _macros and (len(line) < 1 or line[0] == " "):
            lines += [line]
        else:
            macros, _macros, lines = reset(macros, _macros, lines)
        lastline = line
    return macros
