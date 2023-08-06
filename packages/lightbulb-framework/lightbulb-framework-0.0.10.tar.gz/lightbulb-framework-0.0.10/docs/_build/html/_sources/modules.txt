.. highlightlang:: python
Modules
============

Core Modules Design
-----------------------------
A core module complies with the following template::


    META = {
            'author': 'Module Author',
            'description': 'Module Description',
            'comments': ['Sample comment']
        }

    class MODULE_UNIQUE_NAME():

        def __init__(self, params):
            ...

        def getresult(self):
            """
            Returns the resulting string
            Args:
               None
            Returns:
               str: The resulting string
            """

        def learn(self):
            """Performs algorithm"""

        def stats(self):
            """Prints execution statistics"""
            return [('NAME', VALUE)]



Application Modules Design
-----------------------------
For application modules the minimum functions that is required to be declared::

    from lightbulb.core.base import CORE, options_as_dictionary

    META = {
            'author': 'Module Author',
            'description': 'Module Description',
            'type':'Algorithm type',
            'options': [
                ('Option name', value, (BOOL) REQUIRED, 'Option description'),
            ],
            'comments': ['Sample comment']
        }

    class Module(CORE['COREMODULE']):

        def __init__(self, configuration):
            self.module_config = options_as_dictionary(configuration)
            super(Module, self).__init__(self.module_config['Option name'])

        def learn(self):
            ...

        def stats(self):
            return  [("NAME",VALUE)]

        def getresult(self):
            return  "NAME", VALUE


The framework also supports execution in parallel for two core modules. Then. the "Module_A" and "Module_B" classes should be declared instead of the "Module" class::

    class Module_A(CORE['COREMODULE']):

        def __init__(self, configuration, channel, cross):
            self.module_config = options_as_dictionary(configuration)
            super(Module, self).__init__(self.module_config['Option name'])

        def learn(self):
            ...

        def stats(self):
            return  [("NAME",VALUE)]

        def getresult(self):
            return  "NAME", VALUE

    class Module_B(CORE['COREMODULE']):

        def __init__(self, configuration, channel, cross):
            self.module_config = options_as_dictionary(configuration)
            super(Module, self).__init__(self.module_config['Option name'])

        def learn(self):
            ...

        def stats(self):
            return  [("NAME",VALUE)]

        def getresult(self):
            return  "NAME", VALUE



Using SFALearner and SFADiff Core Modules
-----------------------------

Currently, the framework supports two core modules, the **'SFALearner'** and the **'SFADiff'**. The the **'SFADiff'** works exaclty as the **'SFALearner'** core module, but allows two parallel instances to communicate and exchange their learned model during the equivalence query functionality. These core modules already define learn(), stats(), and getresult() functions. However, they declare the _query() function that is required to be overriden.

For **SFALearner** the "Module" class should be used and the minimum functions that are required to be overridden are the following::


    class Module(CORE['SFALearner']):

        def __init__(self, configuration):
            ...
            super(Module, self).__init__(alphabet, file, file_type,  preload)

        def _query(self, string):
            """
            Performs a membership query
            Args:
                string: The string to be tested
            Returns:
                bool: A boolean value indicating that the target parser accepts or rejects the input
            """
            return VALUE


For **SFADiff** the "Module_A" and "Module_B" classes should be used and the minimum functions that are required to be overridden are the following::


    class Module_A(CORE['SFADiff']):

        def __init__(self, configuration, channel, cross):
            ...
            super(Module_A, self).__init__(alphabet, file, file_type, channel, cross, classic,left, right, preload)

        def _query(self, string):
            """
            Performs a membership query
            Args:
                string: The string to be tested
            Returns:
                bool: A boolean value indicating that the target parser accepts or rejects the input
            """
            return VALUE

    class Module_B(CORE['SFADiff']):

        def __init__(self, configuration, channel, cross):
            ...
            super(Module_B, self).__init__(alphabet, file, file_type, channel, cross, classic,left, right, preload)

        def _query(self, string):
            """
            Performs a membership query
            Args:
                string: The string to be tested
            Returns:
                bool: A boolean value indicating that the target parser accepts or rejects the input
            """
            return VALUE

