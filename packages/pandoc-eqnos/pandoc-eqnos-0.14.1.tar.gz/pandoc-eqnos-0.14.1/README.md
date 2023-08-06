

pandoc-eqnos 0.14.1
===================

*pandoc-eqnos* is a [pandoc] filter that numbers equations and equation references in processed markdown documents.  A cross-referencing syntax is added to markdown for this purpose.

Demonstration: Processing [demo.md] with `pandoc --filter pandoc-eqnos` gives numbered equations and references in [pdf], [tex], [html], [epub], [md] and other formats.

This version of pandoc-eqnos was tested using pandoc 1.15 - 1.18.  It works under linux, Mac OS X and Windows.  Older versions and other platforms can be supported on request.  I am pleased to receive bug reports and feature requests on the project's [Issues tracker].

If you find pandoc-eqnos useful, then please encourage further development by giving it a star [on GitHub].

See also: [pandoc-fignos], [pandoc-tablenos]

[pandoc]: http://pandoc.org/
[demo.md]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/demo.md
[pdf]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo.pdf
[tex]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo.tex
[html]: https://rawgit.com/tomduck/pandoc-eqnos/master/demos/out/demo.html
[epub]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo.epub
[md]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo.md
[Issues tracker]: https://github.com/tomduck/pandoc-eqnos/issues
[on GitHub]:  https://github.com/tomduck/pandoc-eqnos
[pandoc-fignos]: https://github.com/tomduck/pandoc-fignos
[pandoc-tablenos]: https://github.com/tomduck/pandoc-tablenos


Contents
--------

 1. [Usage](#usage)
 2. [Markdown Syntax](#markdown-syntax)
 3. [Customization](#customization)
 4. [Technical Details](#technical-details)
 5. [Installation](#installation)
 6. [Getting Help](#getting-help)


Usage
-----

To apply the filter during document processing, use the following option with pandoc:

    --filter pandoc-eqnos

Note that any use of `--filter pandoc-citeproc` or `--bibliography=FILE` options should come *after* the pandoc-eqnos filter call.


Markdown Syntax
---------------

The markdown syntax extension used by pandoc-eqnos was developed in [pandoc Issue #813] -- see [this post] by [@scaramouche1].

To mark an equation for numbering, add the label `eq:id` to its attributes:

    $$ y = mx + b $$ {#eq:id}

The prefix `#eq:` is required. `id` should be replaced with a unique identifier composed of letters, numbers, dashes, slashes and underscores.  If `id` is omitted then the figure will be numbered but unreferenceable.

To reference the equation, use

    @eq:id

or

    {@eq:id}

Curly braces around a reference are stripped from the output.

See [demo.md] for an example.

[pandoc Issue #813]: https://github.com/jgm/pandoc/issues/813
[this post]: https://github.com/jgm/pandoc/issues/813#issuecomment-70423503
[@scaramouche1]: https://github.com/scaramouche1


#### Clever References ####

Writing markdown like

    See eq. @eq:id.

seems a bit redundant.  Pandoc-eqnos supports "clever referencing" via single-character modifiers in front of a reference.  You can write

     See +@eq:id.

to have the reference name (i.e., "eq.") automatically generated.  The above form is used mid-sentence.  At the beginning of a sentence, use

     *@eq:id

instead.  If clever referencing is enabled by default (see [Customization](#customization), below), you can disable it for a given reference using

    !@eq:id

Demonstration: Processing [demo2.md] with `pandoc --filter pandoc-eqnos` gives numbered equations and references in [pdf][pdf2], [tex][tex2], [html][html2], [epub][epub2], [md][md2] and other formats.

Note: If you use `*eq:id` and emphasis (e.g., `*italics*`) in the same sentence, then you must backslash escape the `*` in the clever reference; e.g., `\*eq:id`.

Note: The disabling modifier "!" is used instead of "-" because [pandoc unnecessarily drops minus signs] in front of references.

[demo2.md]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/demo2.md
[pdf2]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo2.pdf
[tex2]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo2.tex
[html2]: https://rawgit.com/tomduck/pandoc-eqnos/master/demos/out/demo2.html
[epub2]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo2.epub
[md2]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo2.md
[pandoc unnecessarily drops minus signs]: https://github.com/jgm/pandoc/issues/2901


#### Tagged Equations ####

You may optionally override the equation number by placing a tag in an equation's attributes block as follows:

    $$ y = mx + b $$ {#eq:id tag="B.1"}

The tag may be arbitrary text, or an inline equation such as `$\mathrm{B.1'}$`.  Mixtures of the two are not currently supported.


Customization
-------------

Pandoc-eqnos may be customized by setting variables in the [metadata block] or on the command line (using `-M KEY=VAL`).  The following variables are supported:

  * `eqnos-cleveref` or just `cleveref` - Set to `On` to assume "+"
    clever references by default;

  * `eqnos-plus-name` - Sets the name of a "+" reference 
    (e.g., change it from "eq." to "equation"); and

  * `eqnos-star-name` - Sets the name of a "*" reference 
    (e.g., change it from "Equation" to "Eq.").

[metadata block]: http://pandoc.org/README.html#extension-yaml_metadata_block

Demonstration: Processing [demo3.md] with `pandoc --filter pandoc-eqnos` gives numbered equations and references in [pdf][pdf3], [tex][tex3], [html][html3], [epub][epub3], [md][md3] and other formats.

[demo3.md]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/demo3.md
[pdf3]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo3.pdf
[tex3]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo3.tex
[html3]: https://rawgit.com/tomduck/pandoc-eqnos/master/demos/out/demo3.html
[epub3]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo3.epub
[md3]: https://raw.githubusercontent.com/tomduck/pandoc-eqnos/master/demos/out/demo3.md


#### Pandoc Flags ####

Some of pandoc's command-line flags impact equation numbering:

  * `-N`, `--number-sections`: Numbers section (or chapter) headings
    in LaTeX/pdf, ConTeXt, html, and epub output.  Equation numbers
    are given in X.Y format, where X is the section (or chapter)
    number and Y is the equation number.  Equation numbers restart
    at 1 for each section (or chapter).  See also pandoc's
    `--top-level-division` flag and `documentclass` meta variable.


Technical Details
-----------------

For TeX/pdf output:

  * The `equation` environment is used;
  * Tagged equations make use of the `\tag` macro;
  * The `\label` and `\ref` macros are used for equation labels and
    references; and
  * The clever referencing macros `\cref` and `\Cref` are used
    if they are available (i.e. included in your LaTeX template via
    `\usepackage{cleveref}`), otherwise they are faked.  Set the 
    meta variable `xnos-cleveref-fake` to `Off` to disable cleveref
    faking.

For all other formats the numbers/tags and clever references are hanr-coded into the output.

Links are constructed for html and pdf output.


Installation
------------

Pandoc-eqnos requires [python], a programming language that comes pre-installed on linux and Mac OS X, and which is easily installed on Windows.  Either python 2.7 or 3.x will do.

[python]: https://www.python.org/


#### Standard installation ####

Install pandoc-eqnos as root using the shell command

    pip install pandoc-eqnos

To upgrade to the most recent release, use

    pip install --upgrade pandoc-eqnos 

Pip is a program that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution.

If you are prompted to upgrade `pip`, then do so.  Installation errors may occur with older versions.  The command is

    python -m pip install --upgrade pip

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

If you have any difficulties with pandoc-eqnos, or would like to see a new feature, please [file an Issue] on GitHub.

[file an issue]: https://github.com/tomduck/pandoc-eqnos/issues
