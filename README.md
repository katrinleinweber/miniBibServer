miniBibServer
=============

This is a small-scale project related to managing biographies/CVs of statisticians.

It has several associated features.

1. **imscv.sty** defines a format for writing biographical CVs in LaTeX, with examples provided in **aitken.tex** and **blackwell.tex**.
1. The **webapp** subdirectory contains a Flask application for converting CVs from this LaTeX format into HTML format, for previewing purposes.  An instance of this application has been deployed to [ims.metameso.org](http://ims.metameso.org).
1. **distributed_update.py** contains a facility for updating a centralized repository of `.tex` and `.html` files stored on Github, based on a distributed collection of CVs hosted on webpages, routing changes through a centrally-controlled review process using pull requests.

### Workflow

1. convert original data to `.tex+bib` format using code in **ims_legacy_latex.py** (requires `ims_legacy.txt`, sold separately):
  - `python -c "import ims_legacy_latex; ims_legacy_latex.make_all()"`
2. This can be converted _en masse_ into `.html` format:
  - `python -c "import ims_legacy_html; ims_legacy_html.make_all()"`
3. This data is then uploaded to a separate (private) Github repository.
4. The repository is subsequently kept up to date via the **distributed_update.py** script.  It runs under cron to achieve the following:
  1. Poll and download copies of all files in our list
  2. Compare downloaded files to local (checked out) copies
  3. If different, submit pull request with the diff on behalf of the upstream editor

### See also

This project is related to the [BibServer project](https://github.com/holtzermann17/bibserver), and the relevant
features will be reflected there at some point.
