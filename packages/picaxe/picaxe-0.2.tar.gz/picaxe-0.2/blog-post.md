picaxe
======

*A python package and command-line tools for work with the Flickr API to upload images, sort images, generate MD image reference links etc*.

Here’s a summary of what’s included in the python package:

Command-Line Usage
==================

``` sourceCode
Documentation for picaxe can be found here: http://picaxe.readthedocs.org/en/stable

Usage:
    picaxe init
    picaxe auth [-s <pathToSettingsFile>]
    picaxe md <url> [-s <pathToSettingsFile>]

Options:
    init                  setup the polygot settings file for the first time
    auth                  authenticate picaxe against your flickr account
    md                    generate the MD reference link for the image in the given flickr URL
    <url>                 the flickr URL or photoid
    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
```

Installation
============

The easiest way to install picaxe us to use `pip`:

``` sourceCode
pip install picaxe
```

Or you can clone the [github repo](https://github.com/thespacedoctor/picaxe) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/picaxe.git
cd picaxe
python setup.py install
```

To upgrade to the latest version of picaxe use the command:

``` sourceCode
pip install picaxe --upgrade
```

Documentation
=============

Documentation for picaxe is hosted by [Read the Docs](http://picaxe.readthedocs.org/en/stable/) (last [stable version](http://picaxe.readthedocs.org/en/stable/) and [latest version](http://picaxe.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

Before you begin using picaxe you will need to populate some custom settings within the picaxe settings file.

To setup the default settings file at `~/.config/picaxe/picaxe.yaml` run the command:

``` sourceCode
picaxe init
```

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an `XXX` placeholder).
