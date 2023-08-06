# -*- coding: utf-8 -*-


import os
from subprocess import Popen, PIPE
from setuptools import setup

import lex


thisdir = os.path.dirname(os.path.abspath(__file__))

readme = os.path.join(thisdir, "README.md")
if os.path.isfile(readme):
    cmd = "pandoc --from=markdown --to=rst " + readme
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception("pandoc conversion failed: " + err)
    long_description = out
else:
    long_description = ""

keywords = [
    "luigi", "workflow", "pipeline", "remote", "submission", "grid"
]

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Information Technology",
    "Topic :: System :: Monitoring"
]

install_requires = []
with open(os.path.join(thisdir, "requirements.txt"), "r") as f:
    install_requires.extend(line.strip() for line in f.readlines() if line.strip())

setup(
    name             = "law",#lex.__name__,
    version          = "0.0.1",#lex.__version__,
    author           = lex.__author__,
    author_email     = lex.__email__,
    description      = lex.__doc__.strip(),
    license          = lex.__license__,
    url              = lex.__contact__,
    py_modules       = [lex.__name__],
    keywords         = keywords,
    classifiers      = classifiers,
    long_description = long_description,
    data_files       = ["LICENSE", "requirements.txt"],
    install_requires = install_requires,
    entry_points     = {
        "console_scripts": []
    }
)
