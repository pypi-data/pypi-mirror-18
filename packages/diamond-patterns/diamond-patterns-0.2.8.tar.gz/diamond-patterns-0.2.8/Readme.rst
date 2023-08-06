Diamond-Patterns
================

**Diamond-Patterns**  scaffolds projects according to patterns.

Installation
^^^^^^^^^^^^

Option 1: Install inside a virtual environment.

::

    mkvirtualenv my-project
    pip install diamond-patterns

Option 2: Install system-wide with Homebrew.

::

    export REPO=https://raw.github.com/iandennismiller/diamond-patterns/master
    export FILE=/etc/diamond-patterns.rb
    brew install ${REPO}${FILE}


Usage
^^^^^

::

    mkdir ~/Documents/my-article
    cd ~/Documents/my-article
    diamond --skel article scaffold
