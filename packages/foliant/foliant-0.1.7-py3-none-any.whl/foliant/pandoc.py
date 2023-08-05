from __future__ import print_function

import subprocess
from . import gitutils

PANDOC_PATH = "pandoc"
FROM_PARAMS = "-f markdown_strict+simple_tables+multiline_tables+grid_tables+pipe_tables+table_captions+fenced_code_blocks+line_blocks+definition_lists+all_symbols_escapable+strikeout+superscript+subscript+lists_without_preceding_blankline+implicit_figures+raw_tex+citations+tex_math_dollars+header_attributes+auto_identifiers+startnum+footnotes+inline_notes+fenced_code_attributes+intraword_underscores+escaped_line_breaks"
LATEX_PARAMS = "--no-tex-ligatures --smart --normalize --listings --latex-engine=xelatex"

def generate_variable(key, value):
    return '--variable "%s"="%s"' % (key, value)

def generate_command(params, output_file, src_file, cfg):
    params = ["-o " + output_file, FROM_PARAMS, LATEX_PARAMS, params]

    for key, value in cfg.items():
        if key in ("title", "second_title", "year", "date", "title_page", "tof", "toc"):
            params.append(generate_variable(key, value))
        elif key == "template":
            params.append('--template="%s.tex"' % value)
        elif key == "lang":
            if value in ("russian", "english"):
                params.append(generate_variable(value, "true"))
            else:
                params.append(generate_variable("russian", "true"))
        elif key == "version":
            if value == "auto":
                params.append(generate_variable(key, gitutils.get_version()))
            else:
                params.append(generate_variable(key, value))
        elif key == "company":
            if value in ("restream", "undev"):
                params.append(generate_variable(value, "true"))
            else:
                raise RuntimeError("Unsupported company: %s" % value)
        elif key in ("type", "alt_doc_type"):
            if value:
                params.append(generate_variable(key, value))
        elif key == "filters":
            for filt in value:
                params.append("-F %s" % filt)
        else:
            print("Unsupported config key: %s" % key)

    return ' '.join([PANDOC_PATH] + params + [src_file])

def run(command, src_dir):
    print("Baking output... ", end='')
    try:
        proc = subprocess.check_output(
            command,
            cwd=src_dir,
            stderr=subprocess.PIPE
        )

        print("Done!")

    except subprocess.CalledProcessError as e:
        quit(e.stderr.decode())

def to_pdf(src_file, output_file, tmp_path, cfg):
    pandoc_command = generate_command(
        "-t latex",
        output_file,
        src_file,
        cfg
    )
    run(pandoc_command, tmp_path)

def to_docx(src_file, output_file, tmp_path, cfg):
    pandoc_command = generate_command(
        '--reference-docx="ref.docx"',
        output_file,
        src_file,
        cfg
    )
    run(pandoc_command, tmp_path)

def to_tex(src_file, output_file, tmp_path, cfg):
    pandoc_command = generate_command(
        "-t latex",
        output_file,
        src_file,
        cfg
    )
    run(pandoc_command, tmp_path)
