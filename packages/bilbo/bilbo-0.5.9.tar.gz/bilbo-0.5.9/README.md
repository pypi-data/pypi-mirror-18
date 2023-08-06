bilbo
=====

*Commands to help build and maintain a gollum wiki*.

Usage
=====

    bilbo template [-s <pathToSettingsFile>]
    bilbo tasks [-s <pathToSettingsFile>]
    bilbo tidy [-s <pathToSettingsFile>]
    bilbo scaffold [-s <pathToSettingsFile>]
    bilbo blog [-s <pathToSettingsFile>]

    COMMANDS
    ========
    template              populate the wiki with template content and cleanup file names
    tasks                 add projects from wikis to taskpaper files to keep track of project tasks
    tidy                  tidy up the gollum wiki, updating lists, sidebars, footer, headers, cleaning filenames and md metadata
    scaffold              add and maintain sidebars, footers, headers and various listing pages in a gollum wiki
    blog                  take pages that have been flagged to be posted as a Jekyll blog post, format them correctly and post them

    OPTIONS
    =======
    -h, --help            show this help message
    -s, --settings        the settings file

Documentation
=============

Documentation for bilbo is hosted by [Read the
Docs](http://bilbo.readthedocs.org/en/stable/) (last [stable
version](http://bilbo.readthedocs.org/en/stable/) and [latest
version](http://bilbo.readthedocs.org/en/latest/)).

Installation
============

The easiest way to install bilbo us to use `pip`:

    pip install bilbo

Or you can clone the [github
repo](https://github.com/thespacedoctor/bilbo) and install from a local
version of the code:

    git clone git@github.com:thespacedoctor/bilbo.git
    cd bilbo
    python setup.py install

To upgrade to the latest version of bilbo use the command:

    pip install bilbo --upgrade

Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

    git clone git@github.com:thespacedoctor/bilbo.git
    cd bilbo
    python setup.py develop

[Pull requests](https://github.com/thespacedoctor/bilbo/pulls) are
welcomed!

Issues
------

Please report any issues
[here](https://github.com/thespacedoctor/bilbo/issues).

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
