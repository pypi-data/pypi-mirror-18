

NEW: Clickable references in docx!


pandoc-tablenos 0.15
====================

*pandoc-tablenos* is a [pandoc] filter for numbering tables and table references in processed markdown documents.  A cross-referencing syntax is added to markdown for this purpose.

Demonstration: Processing [demo3.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf3], [tex][tex3], [html][html3], [epub][epub3], [docx][docx3] and other formats.

This version of pandoc-tablenos was tested using pandoc 1.15 - 1.19.  It works under linux, Mac OS X and Windows.  Older versions and other platforms can be supported on request.  I am pleased to receive bug reports and feature requests on the project's [Issues tracker].

If you find pandoc-tablenos useful, then please encourage further development by giving it a star [on GitHub].

See also: [pandoc-fignos], [pandoc-eqnos]

[pandoc]: http://pandoc.org/
[Issues tracker]: https://github.com/tomduck/pandoc-tablenos/issues
[on GitHub]: https://github.com/tomduck/pandoc-tablenos
[pandoc-fignos]: https://github.com/tomduck/pandoc-fignos
[pandoc-eqnos]: https://github.com/tomduck/pandoc-eqnos


Contents
--------

 1. [Usage](#usage)
 2. [Markdown Syntax](#markdown-syntax)
 3. [Customization](#customization)
 4. [Details](#details)
 5. [Installation](#installation)
 6. [Getting Help](#getting-help)


Usage
-----

To apply the filter during document processing, use the following option with pandoc:

    --filter pandoc-tablenos

Note that any use of `--filter pandoc-citeproc` or `--bibliography=FILE` should come *after* the pandoc-tablenos filter call.


Markdown Syntax
---------------

The markdown syntax extension used by pandoc-tablenos was worked out in [pandoc Issue #813] -- see [this post] by [@scaramouche1].

To mark a table for numbering, add the label `tbl:id` to the attributes of its caption:

    A B
    - -
    0 1

    Table: Caption. {#tbl:id}

The prefix `#tbl:` is required. `id` should be replaced with a unique identifier composed of letters, numbers, dashes, slashes and underscores.  If `id` is omitted then the figure will be numbered but unreferenceable.

To reference the table, use

    @tbl:id

or

    {@tbl:id}

Curly braces around a reference are stripped from the output.

Demonstration: Processing [demo.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf], [tex], [html], [epub], [docx] and other formats.

[pandoc Issue #813]: https://github.com/jgm/pandoc/issues/813
[this post]: https://github.com/jgm/pandoc/issues/813#issuecomment-70423503
[@scaramouche1]: https://github.com/scaramouche1
[demo.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo.md
[pdf]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo.pdf
[tex]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo.tex
[html]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo.html
[epub]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo.epub
[docx]: https://github.com/tomduck/pandoc-tablenos/blob/master/demos/out/demo.docx


#### Clever References ####

Writing markdown like

    See table @tbl:id.

seems a bit redundant.  Pandoc-tablenos supports "clever referencing" via single-character modifiers in front of a reference.  You can write

     See +@tbl:id.

to have the reference name (i.e., "table") automatically generated.  The above form is used mid-sentence.  At the beginning of a sentence, use

     *@tbl:id

instead.  If clever referencing is enabled by default (see [Customization](#customization), below), you can disable it for a given reference using<sup>[1](#footnote1)</sup>

    !@tbl:id

Demonstration: Processing [demo2.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf2], [tex][tex2], [html][html2], [epub][epub2], [docx][docx2] and other formats.

Note: If you use `*tbl:id` and emphasis (e.g., `*italics*`) in the same sentence, then you must backslash escape the `*` in the clever reference; e.g., `\*tbl:id`.

[demo2.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo2.md
[pdf2]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo2.pdf
[tex2]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo2.tex
[html2]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo2.html
[epub2]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo2.epub
[docx2]: https://github.com/tomduck/pandoc-tablenos/blob/master/demos/out/demo2.docx


#### Tagged Tables ####

You may optionally override the table number by placing a tag in a table's attributes block as follows:

    A B
    - -
    0 1

    Table: Caption. {#tbl:id tag="B.1"}

The tag may be arbitrary text, or an inline equation such as `$\text{B.1}'$`.  Mixtures of the two are not currently supported.


Customization
-------------

Pandoc-tablenos may be customized by setting variables in the [metadata block] or on the command line (using `-M KEY=VAL`).  The following variables are supported:

  * `tablenos-caption-name` - Sets the name at the beginning of a
    caption (e.g., change it from "Table to "Tab.");

  * `tablenos-cleveref` or just `cleveref` - Set to `On` to assume
    "+" clever references by default;

  * `tablenos-plus-name` - Sets the name of a "+" reference 
    (e.g., change it from "table" to "tab."); and

  * `tablenos-star-name` - Sets the name of a "*" reference 
    (e.g., change it from "Table" to "Tab.").

[metadata block]: http://pandoc.org/README.html#extension-yaml_metadata_block

Demonstration: Processing [demo3.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf3], [tex][tex3], [html][html3], [epub][epub3], [docx][docx3] and other formats.

[demo3.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo3.md
[pdf3]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo3.pdf
[tex3]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo3.tex
[html3]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo3.html
[epub3]: https://rawgit.com/tomduck/pandoc-tablenos/master/demos/out/demo3.epub
[docx3]: https://github.com/tomduck/pandoc-tablenos/blob/master/demos/out/demo3.docx


#### Pandoc Flags ####

Some of pandoc's command-line flags impact table numbering:

  * `-N`, `--number-sections`: Numbers section (or chapter) headings
    in LaTeX/pdf, ConTeXt, html, and epub output.  Table numbers are
    given in X.Y format, where X is the section (or chapter) number
    and Y is the figure number.  Table numbers restart at 1 for each
    section (or chapter).  See also pandoc's `--top-level-division`
    flag and `documentclass` meta variable.


#### Latex/PDF Specializations ####

To make the table caption label bold, add `\usepackage[labelfont=bf]{caption}` to the `header-includes` field of your document's YAML metadata.  See the [LaTeX caption package] documentation for additional features.

[LaTeX caption package]: https://www.ctan.org/pkg/caption


Details
-------

TeX/pdf:

  * The `\label` and `\ref` macros are used for table labels and
    references;
  * `\figurename` is set for the caption name;
  * Tags are supported by temporarily redefining `\thetable` around 
    a table; and
  * The clever referencing macros `\cref` and `\Cref` are used
    if they are available (i.e. included in your LaTeX template via
    `\usepackage{cleveref}`), otherwise they are faked.  Set the 
    meta variable `xnos-cleveref-fake` to `Off` to disable cleveref
    faking.

Other formats:

  * Links to figures use html's and docx's native capabilities; and

  * The numbers, caption name, and (clever) references are hard-coded
    into the output.


Installation
------------

Pandoc-tablenos requires [python], a programming language that comes pre-installed on linux and Mac OS X, and which is easily installed on Windows.  Either python 2.7 or 3.x will do.

[python]: https://www.python.org/


#### Standard installation ####

Install pandoc-tablenos as root using the shell command

    pip install pandoc-tablenos 

To upgrade to the most recent release, use

    pip install --upgrade pandoc-tablenos 

Pip is a program that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution.

[PyPI]: https://pypi.python.org/pypi


#### Installing on linux ####

If you are running linux, pip may be packaged separately from python.  On Debian-based systems (including Ubuntu), you can install pip as root using

    apt-get update
    apt-get install python-pip

During the install you may be asked to run

    easy_install -U setuptools

owing to the ancient version of setuptools that Debian provides.  The command should be executed as root.  You may now follow the [standard installation] procedure given above.

[standard installation]: #standard-installation


#### Installing on Windows ####

It is easy to install python on Windows.  First, [download] the latest release.  Run the installer and complete the following steps:

 1. Install Python pane: Check "Add Python 3.5 to path" then
    click "Customize installation".

 2. Optional Features pane: Click "Next".

 3. Advanced Options pane: Optionally check "Install for all
    users" and customize the install location, then click "Install".

Once python is installed, start the "Command Prompt" program.  Depending on where you installed python, you may need elevate your privileges by right-clicking the "Command Prompt" program and selecting "Run as administrator".  You may now follow the [standard installation] procedure given above.  Be sure to close the Command Prompt program when you have finished.

[download]: https://www.python.org/downloads/windows/


Getting Help
------------

If you have any difficulties with pandoc-tablenos, or would like to see a new feature, please [file an Issue] on github.

[file an Issue]: https://github.com/tomduck/pandoc-tablenos/issues


----

**Footnotes**

<a name="footnote1">1</a>: The disabling modifier "!" is used instead of "-" because [pandoc unnecessarily drops minus signs] in front of references.

[pandoc unnecessarily drops minus signs]: https://github.com/jgm/pandoc/issues/2901
