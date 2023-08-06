.. highlightlang:: python

API Reference
============

The framework offers a number of built-in query handlers for enhancing the membership queries:

The **HTTP Handler**:
-----------------------------
    To initialize the handler::

        from lightbulb.core.utils.http_handler import HTTPHandler as _HTTPHandler
        httphandler = _HTTPHandler(URL, REQUEST_TYPE, PARAM, BLOCK, BYPASS, PROXY_SCHEME, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD, USER_AGENT, REFERER)


    To perform a query::

        httphandler.query(string)


The **SQL Handler**:
-----------------------------
    To initialize the handler::

        from lightbulb.core.utils.sql_handler import SQLHandler as _SQLHandler
        sqlserver = _SQLHandler(HOST, PORT, USERNAME, PASSWORD, DATABASE, PREFIX_QUERY, SQLPARSES)


    To perform a query::


        sqlserver.query(string)


The **Browser Handler**:
-----------------------------
    To initialize the handler::


        from lightbulb.core.utils.browsersocket_hander import BrowserSocketHandler as _BrowserSocketHandler
        browser_socket_handler = _BrowserSocketHandler(WSPORT, WBPORT, BROWSERPARSES)


    To perform a query::


        browser_socket_handler.query(string)


The **Options Parser**:
-----------------------------
    To initialize the handler::

        from lightbulb.core.base import options_as_dictionary


    To perform a query::


        module_config = options_as_dictionary(configuration)


The **Alphabet**:
-----------------------------
    To initialize the handler::

        from lightbulb.core.base import createalphabet


    To retrieve alphabet::


        createalphabet()