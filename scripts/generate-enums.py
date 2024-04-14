"""Generate src/zint/generated/enums.hpp file. Run this from the root directory."""

import json
import re
import subprocess as sp
import sys
import textwrap

import clang_format as cf
import varformat as vf

re_base_define = r"^#define (\w+) +((?:0x)?\d+)"
"""`#define BARCODE_CODE128 0x01`"""

re_comment = r"\/\* ([^\n]*) \*\/"
"""`/* This is barcode documentation */`"""

re_comment_note = r"\n *\/\* (.*?)\s+?\*\/"
"""`/* Barcode note, starting from next line */`"""

re_define = re_base_define + " *" + re_comment + "(?:" + re_comment_note + ")?"


def find_line_re(pattern, source: str, start=0):
    m = re.search(pattern, source[start:], re.MULTILINE | re.DOTALL)
    if m:
        return m.start() + start

    return None


def clang_format(text: str):
    exe = cf._get_executable("clang-format")
    return sp.check_output([exe, "-"], encoding="utf-8", input=text)


def escape_string(s: str):
    """Escape a string for double quotes in C++."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def parse_enum(
    source: str,
    *,
    header: str,
    footer: str = r"^\/\*",
    prefix=None,
    suffix=None,
    blacklist=None,
):
    enum_values = {}
    enum_comments = {}

    start = find_line_re(header, source)
    start = source.find("\n", start) + 1
    end = find_line_re(footer, source, start)
    text = source[start:end]

    for m in re.finditer(re_define, text, re.MULTILINE | re.DOTALL):
        # Macro name
        name = m[1]
        if prefix is not None:
            assert name.startswith(prefix)
            name = name[len(prefix) :]

        if suffix is not None:
            assert name.endswith(suffix)
            name = name[: -len(suffix)]

        # Macro value
        value = m[2]
        if value.startswith("0x"):
            value = int(value, 16)
        else:
            value = int(value)

        # Comment
        comment = m[3]
        if m[4] is not None:  # Note after the comment
            comment = comment + ". " + m[4]

        if blacklist is not None and blacklist(name, value, comment):
            continue

        enum_values[name] = value
        enum_comments[name] = comment

    enum = [(name, enum_values[name], enum_comments[name]) for name in enum_values]
    enum.sort(key=lambda item: item[1])
    return enum


def enum_definition(enum, *, class_name: str, base_type: str = "int"):
    values = ",".join(f"{name} = {value}" for name, value, _ in enum)
    return f"enum class {class_name} : {base_type} {{ {values} }};"


def enum_binding(enum, *, class_name: str, docstring: str, arithmetic=False):
    values = "".join(
        f'.value("{name}", {class_name}::{name}, "{escape_string(comment)}")'
        for name, _, comment in enum
    )

    if arithmetic == True:
        arithmetic_tag = "py::arithmetic{},"
    else:
        arithmetic_tag = ""

    return f'py::enum_<{class_name}>(m, "{class_name}", {arithmetic_tag} "{escape_string(docstring)}") {values};'


def main():
    with open("external/zint/backend/zint.h", "r", encoding="utf-8") as f:
        source = f.read()

    # Symbology enum
    symbology_enum = parse_enum(
        source,
        header=re.escape("/* Symbologies (`symbol->symbology`) */"),
        prefix="BARCODE_",
        blacklist=lambda name, _, comment: comment == "Legacy" or name == "LAST",
    )

    output_options_enum = parse_enum(
        source,
        header=re.escape("/* Output options (`symbol->output_options`) */"),
    )

    imput_mode_enum = parse_enum(
        source,
        header=re.escape("/* Input data types (`symbol->input_mode`) */"),
        footer=r"^\/\*(?! The following may be OR-ed with above)",  # Do not terminate on a top-level comment
        suffix="_MODE",
    )

    datamatrix_options_enum = parse_enum(
        source,
        header=re.escape("/* Data Matrix specific options (`symbol->option_3`) */"),
        prefix="DM_",
    )

    qr_family_options_enum = parse_enum(
        source,
        header=re.escape(
            "/* QR, Han Xin, Grid Matrix specific options (`symbol->option_3`) */"
        ),
        prefix="ZINT_",
    )

    ultracode_options_enum = parse_enum(
        source,
        header=re.escape("/* Ultracode specific option (`symbol->option_3`) */"),
    )

    warning_level_enum = parse_enum(
        source,
        header=re.escape("/* Warning level (`symbol->warn_level`) */"),
        prefix="WARN_",
    )

    capability_flags_enum = parse_enum(
        source,
        header=re.escape("/* Capability flags (ZBarcode_Cap() `cap_flag`) */"),
        prefix="ZINT_CAP_",
    )

    # Write file -------------------------------------------------------------------------------------------------------
    template = textwrap.dedent(
        """\
        /// This file was generated automatically by scripts/generate-enums.py. Please do not edit it manually.
        #pragma once
        #include <pybind11/pybind11.h>

        namespace py = pybind11;

        ${code}

        inline void init_enum_bindings(pybind11::module_& m) {
            ${bindings}
        }
        """
    )

    text = vf.format(
        template,
        code="\n".join(
            [
                enum_definition(symbology_enum, class_name="Symbology"),
                enum_definition(output_options_enum, class_name="OutputOptions"),
                enum_definition(imput_mode_enum, class_name="InputMode"),
                enum_definition(
                    datamatrix_options_enum, class_name="DataMatrixOptions"
                ),
                enum_definition(qr_family_options_enum, class_name="QrFamilyOptions"),
                enum_definition(ultracode_options_enum, class_name="UltracodeOptions"),
                enum_definition(warning_level_enum, class_name="WarningLevel"),
                enum_definition(
                    capability_flags_enum,
                    class_name="CapabilityFlags",
                    base_type="unsigned int",
                ),
            ]
        ),
        bindings="\n".join(
            [
                enum_binding(
                    symbology_enum,
                    class_name="Symbology",
                    docstring="Values for `Symbol.symbology`",
                ),
                enum_binding(
                    output_options_enum,
                    class_name="OutputOptions",
                    docstring="Values for `Symbol.output_options`",
                    arithmetic=True,
                ),
                enum_binding(
                    imput_mode_enum,
                    class_name="InputMode",
                    docstring="Values for `Symbol.input_mode`",
                    arithmetic=True,
                ),
                enum_binding(
                    datamatrix_options_enum,
                    class_name="DataMatrixOptions",
                    docstring="Data Matrix specific options (`symbol->option_3`)",
                ),
                enum_binding(
                    qr_family_options_enum,
                    class_name="QrFamilyOptions",
                    docstring="QR, Han Xin, Grid Matrix specific options (`symbol->option_3`)",
                ),
                enum_binding(
                    ultracode_options_enum,
                    class_name="UltracodeOptions",
                    docstring="Ultracode specific option (`symbol->option_3`)",
                ),
                enum_binding(
                    warning_level_enum,
                    class_name="WarningLevel",
                    docstring="Warning level (`symbol->warn_level`)",
                ),
                enum_binding(
                    capability_flags_enum,
                    class_name="CapabilityFlags",
                    docstring="Capability flags (ZBarcode_Cap() `cap_flag`)",
                ),
            ]
        ),
    )

    text = clang_format(text)
    with open("src/zint/generated/enums.hpp", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


if __name__ == "__main__":
    sys.exit(main())
