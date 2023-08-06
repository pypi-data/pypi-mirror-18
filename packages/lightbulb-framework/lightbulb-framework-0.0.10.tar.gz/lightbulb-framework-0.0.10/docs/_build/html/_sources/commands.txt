.. highlightlang:: python

Commands Usage
============

Main interface commands:
-----------------------------

=================  ====================================
Command            Description
=================  ====================================
core               Shows available core modules
info  \<module\>   Prints module information
library            Enters library
modules            Shows available application modules
use \<module\>     Enters module
help               Prints help
complete           Prints bash completion command
=================  ====================================
Module commands:
-----------------------------

=============================  ====================================
Command                        Description
=============================  ====================================
back                           Go back to main menu
info                           Prints  current module information
library                        Enters library
options                        Shows available options
define \<option\>  \<value\>   Set an option value
start                          Initiate algoritm
complete                       Prints bash completion command
=============================  ====================================

Library commands:
-----------------------------

=============================  ====================================
Command                        Description
=============================  ====================================
back                           Go back to main menu
info \<folder\\module\>        Prints requested module information (folder must be located in lightbulb/data/)
cat \<folder\\module\>         Prints requested module  (folder must be located in lightbulb/data/)
modules  \<folder\>            Shows available library modules in the requested folder (folder must be located in lightbulb/data/)
search  \<keywords\>           Searches available library modules using comma separated keywords
complete                       Prints bash completion command
=============================  ====================================