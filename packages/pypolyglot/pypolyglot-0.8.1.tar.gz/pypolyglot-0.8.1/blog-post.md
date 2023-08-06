polyglot
========

<img src="http://i.imgur.com/eifuDPP.png" alt="image" width="300" />

*A python package and command-line tools for translating documents and webpages to various markup languages and document formats (html, epub, mobi ..)*.

Here’s a summary of what’s included in the python package:

Command-Line Usage
==================

``` sourceCode
Documentation for polyglot can be found here: http://pypolyglot.readthedocs.org/en/stable

Translate documents and webpages to various markup languages and document formats (html, epub, mobi ..)

Usage:
    polyglot init
    polyglot [-oc] (pdf|html|epub|mobi) <url> [<destinationFolder> -f <filename> -s <pathToSettingsFile>]
    polyglot kindle <url> [-f <filename> -s <pathToSettingsFile>]
    polyglot [-o] (epub|mobi) <docx> [<destinationFolder> -f <filename> -s <pathToSettingsFile>]
    polyglot kindle <docx> [-f <filename> -s <pathToSettingsFile>]
    polyglot [-o] kindleNB2MD <notebook> [<destinationFolder> -s <pathToSettingsFile>]

Options:
    init                                                            setup the polyglot settings file for the first time
    pdf                                                             print webpage to pdf
    html                                                            parse and download webpage to a local HTML document
    epub                                                            generate an epub format book from a webpage URL
    kindle                                                          send webpage article straight to kindle

    -h, --help                                                      show this help message
    -v, --version                                                   show version
    -o, --open                                                      open the document after creation
    -c, --clean                                                     add polyglot's clean styling to the output document
    <url>                                                           the url of the article's webpage
    <docx>                                                          path to a DOCX file
    -s <pathToSettingsFile>, --settings <pathToSettingsFile>        path to alternative settings file (optional)
    <destinationFolder>                                             the folder to save the parsed PDF or HTML document to (optional)
    -f <filename>, --filename <filename>                            the name of the file to save, otherwise use webpage title as filename (optional)
```

Installation
============

The easiest way to install polyglot us to use `pip`:

``` sourceCode
pip install polyglot
```

Or you can clone the [github repo](https://github.com/thespacedoctor/polyglot) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/polyglot.git
cd polyglot
python setup.py install
```

To upgrade to the latest version of polyglot use the command:

``` sourceCode
pip install polyglot --upgrade
```

Documentation
=============

Documentation for polyglot is hosted by [Read the Docs](http://pypolyglot.readthedocs.org/en/stable/) (last [stable version](http://pypolyglot.readthedocs.org/en/stable/) and [latest version](http://pypolyglot.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

Before you begin using polyglot you will need to populate some custom settings within the polyglot settings file.

To setup the default settings file at `~/.config/polyglot/polyglot.yaml` run the command:

``` sourceCode
polyglot init
```

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an `XXX` placeholder).

polyglot often relies on a bunch on other excellent tools to get it’s results like [electron-pdf](https://github.com/fraserxu/electron-pdf), [pandoc](http://pandoc.org) and [kidlegen](https://www.amazon.com/gp/feature.html?docId=1000765211). Depending on how you use polyglot, these tools may need to be install on your system.

To read the basic usage intructions just run `polyglot -h`.

Webpage Article to HTML document
--------------------------------

To generate a parsed, cleaned local HTML document from a webpage at a given URL use polyglot’s `html` command:

``` sourceCode
polyglot html https://en.wikipedia.org/wiki/Volkswagen
```

The filename for the output file is take from the webpage’s title and output in the current directory. [Here’s the result.](_static/examples/Volkswagen.html)

To instead give both a destination output and a specified filename for the resulting document:

``` sourceCode
polyglot html https://en.wikipedia.org/wiki/Volkswagen ~/Desktop -f cars_and_stuff
```

To style the result with polyglots simple styling and easy to read fonts, use the -c flag:

``` sourceCode
polyglot -c html https://en.wikipedia.org/wiki/Volkswagen -f Volkswagen_Styled
```

[See the result here.](_static/examples/Volkswagen_Styled.html)

Webpage Article to PDF
----------------------

To instead print the webpage to PDF, you can either just print the original webpage:

``` sourceCode
polyglot pdf https://en.wikipedia.org/wiki/Volkswagen
```

[with this result](_static/examples/Volkswagen.pdf), or you can choose again to use polyglot’s styling:

``` sourceCode
polyglot -c pdf https://en.wikipedia.org/wiki/Volkswagen -f Volkswagen_Styled
```

[resulting in this PDF.](_static/examples/Volkswagen_Styled.pdf)

Note if you are going to be running polyglot in a windowless environment, to generate the PDFs with [electron-pdf](%60https://github.com/fraserxu/electron-pdf%60) you will need to install [xvfb](https://www.x.org/archive/X11R7.6/doc/man/man1/Xvfb.1.xhtml). To install and setup do something similar to the following (depending on your flavour of OS):

``` sourceCode
sudo apt-get install xvfb
```

then in whatever bash scripts you write add this before any polyglot commands:

``` sourceCode
export DISPLAY=':99.0'
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
```

Webpage Article to eBook
------------------------

To generate an epub book from a webpage article run the command:

``` sourceCode
polyglot epub http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html 
```

Here is the [output of this command.](_static/examples/mysqlSucker.epub)

If you prefer a mobi output, use the command:

``` sourceCode
polyglot mobi http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html 
```

To get [this mobi book.](_static/examples/mysqlSucker.mobi)

Send a Webpage Article Straight to Your Kindle
----------------------------------------------

Polyglot can go even further than creating a mobi ebook from the web-article; it can also send the ebook straight to your kindle device or smart phone app (or both at the same time) as long as you have the email settings populated in the polyglot settings file.

``` sourceCode
polyglot kindle http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html 
```

And here’s the book appearing on a smart phone kindle app:

<img src="https://i.imgur.com/RQpvBZu.png" alt="image" width="300" />

Converting Kindle Notebook HTML Exports to Markdown
---------------------------------------------------

On the Kindle app for iOS you can export an HTML document of your notes and annotations via email.

The colors of the annotation convert to markdown with the following color-key:

“blue”: “code”,
“yellow”: “text”,
“orange”: “quote”,
“pink”: “header”
