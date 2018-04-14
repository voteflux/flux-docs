#!/usr/bin/env python3

import sys
import logging
import zipfile as z
from io import BytesIO
import os
import shutil
from contextlib import suppress
from itertools import dropwhile

import requests
import pypandoc


if os.environ.get("DEV") is not None:
    logging.basicConfig(level=logging.INFO)


flux_constitutions_url = "https://github.com/voteflux/flux/archive/master.zip"
zip_extract_dir = "./docs/constitutions/raw"
repo_contents_dir = os.path.join(zip_extract_dir, "flux-master")
const_dest_dir = "./docs/constitutions"


def reproduction_heading(n_parts):
    t = "/" + "/".join(n_parts) + " Constitution"
    underline = "=" * len(t)
    return """%s
%s

""" % (t, underline)


reproduction_warning = """.. warning::
   This document is a reproduction and not the canonical version.
   It may be different or out of date. For the canonical version please
   see `this GitHub repository <https://github.com/voteflux/flux/>`_.

"""


def copy_and_convert_constitution(from_name, to_name):
    # read in md file
    md_text = open(os.path.join(repo_contents_dir, from_name), 'r').read()
    # make replace title heading
    md_lines_no_heading = list(dropwhile(lambda l : l.strip() == "", md_text.split("\n")))[1:]
    md_text_no_opening_heading = "\n".join(md_lines_no_heading)
    # convert to rst and then save
    rst_text = pypandoc.convert_text(md_text_no_opening_heading, 'rst', format='md')
    out_file = os.path.join(const_dest_dir, to_name)
    open(out_file, 'w').write(rst_text)


def add_disclaimer_and_title(fname, name_parts):
    '''read the file, add bits, save file'''
    to_edit = os.path.join(const_dest_dir, fname)
    f = open(to_edit, 'r').read()
    f_mod = reproduction_heading(name_parts) + reproduction_warning + f
    open(to_edit, "w").write(f_mod)


def main():
    req = requests.get(flux_constitutions_url)

    if req.status_code != 200:
        logging.error("Unable to download constitutions from github")
        sys.exit(1)

    logging.info("Creating tempt zip extraction dir for constitutions")
    with suppress(Exception):
        os.mkdir(zip_extract_dir)
    zip_bytes = req.content
    z.ZipFile(BytesIO(zip_bytes)).extractall(zip_extract_dir)

    for fname in os.listdir(repo_contents_dir):
        logging.info("Examining file %s", fname)
        name_split = fname.split('.')
        if "CONSTITUTION" == name_split[0] and "md" == name_split[-1]:
            logging.info("Found a constitution: %s", fname)
            if 2 <= len(name_split) <= 3:  # then it's a constitution
                name_parts = ["AUS"] if len(name_split) == 2 else ["AUS", name_split[1].upper()]
                out_name = '-'.join(name_parts).lower() + ".rst"
                copy_and_convert_constitution(fname, out_name)
                add_disclaimer_and_title(out_name, name_parts)
                print("Added", out_name)
            else:
                logging.error("Unknown and unexpected file detected as constitution: %s", fname)
                sys.exit(1)

    logging.info("Removing temp zip extraction dir")
    shutil.rmtree(zip_extract_dir)

    print("All constitutions added")


if __name__ == "__main__":
    main()
