miniBibServer
=============

This is a small-scale project related to managing biographies/CVs of statisticians.

It has several associated features.

1. **imscv.sty** defines a format for writing biographical CVs in LaTeX, with an example provided in **blackwell_new.tex**.
1. The **webapp** subdirectory contains a Flask application for converting CVs from this LaTeX format into HTML format for previewing purposes.
1. **distributed_update.py** contains a facility for updating a centralized repository of `.tex` and `.html` files stored on Github, based on a distributed collection of CVs hosted on webpages, routing changes through a centrally-controlled review process using pull requests.
