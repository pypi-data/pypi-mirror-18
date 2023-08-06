from __future__ import print_function

"""Seqdiag processor."""

import os
from os.path import join
import subprocess

def process_seqdiag_block(sd_block, sd_number, src_dir, sd_dir):
    """Extract diagram definition, convert it to image,
    and return the image ref.
    """

    sd_src_filename = "%d.diag" % sd_number
    sd_content = '\n'.join(sd_block[1: -1])
    sd_caption = sd_block[0].replace("```seqdiag", '').strip()
    sd_img_ref = "![%s](%s/%d.png)" % (sd_caption, sd_dir, sd_number)
    sd_src_path = join(src_dir, sd_dir, sd_src_filename)
    sd_command = "seqdiag -a %s" % sd_src_path

    with open(sd_src_path, 'w') as sd_src_file:
        sd_src_file.writelines(sd_content)

    try:
        proc = subprocess.check_output(
            sd_command,
            stderr=subprocess.PIPE
        )

    except subprocess.CalledProcessError as e:
        pass

    return sd_img_ref

def process_diagrams(src_dir, src_file):
    """Find seqdiag code blocks, feed their content to seqdiag tool,
    and replace them with image references.
    """

    print("Drawing diagrams... ", end='')

    sd_dir = "diagrams"
    src_path = join(src_dir, src_file)
    buffer, new_source = [], []
    sd_number = 0

    os.makedirs(join(src_dir, sd_dir))

    with open(src_path) as src:
        for line in (l.rstrip() for l in src):
            if not buffer:
                if line.startswith("```seqdiag"):
                    buffer.append(line)
                else:
                    new_source.append(line)

            else:
                buffer.append(line)

                if line == "```":
                    new_source.append(
                        process_seqdiag_block(
                            buffer,
                            sd_number,
                            src_dir,
                            sd_dir
                        )
                    )
                    sd_number += 1
                    buffer = []

    with open(src_path, 'w') as src:
        src.writelines('\n'.join(new_source))

    print("Done!")
