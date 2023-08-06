========
CRAPtion
========
CRAPtion is a simple screenshot uploader for unix systems.

Features
^^^^^^^^
* Upload to Imgur, Dropbox or SSH
* Automatically copy url
* Format filename with date and random letters

Installation
^^^^^^^^^^^^

::

    $ pip install craption
    $ craption

Usage
^^^^^

::

    $ craption

Requirements
^^^^^^^^^^^^

OS X
****

- Python 2.7

Linux
*****
- Python 2.7
- scrot
- mplayer (optional)

Config
^^^^^^

Config file
***********

Config file created automatically on first run: ``~/.craptionrc``

Bind hotkey in OS X
*******************

- Open automator
- Create service
- Select run shell script
- Type ``craption``
- Save your service/workflow
- Open System Pref -> Keyboard settings -> Keyboard shortcuts
- Find your service in Services

Todo
^^^^

- Error if setting is missing
- FTP
- Libnotify/Growl
- craption dropbox/scp/imgur
