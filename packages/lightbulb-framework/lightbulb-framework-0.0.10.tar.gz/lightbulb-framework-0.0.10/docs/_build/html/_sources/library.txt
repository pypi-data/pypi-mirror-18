.. highlightlang:: python

Library Modules
============
A library module consists of two files:

* A file (ending in .y or .json) that contains the actual grammar, regular expression or json configuration. It can also be a folder.
* A file (ending in .py) having the same name, that describes the previous file

The file (ending in .py) must have the following form::


    META = {
        'author': 'Module Author',
        'description': 'File/Folder containing ...',
        'type':'Regex/Grammar/Folder/Configuration',
        'comments': []
    }
