========================
Zeep: Python SOAP client 
========================

A fast and hip Python SOAP client ;-)

| Website: http://docs.python-zeep.org/
| IRC: #python-zeep on Freenode

Highlights:
 * Modern codebase compatible with Python 2.7, 3.3, 3.4, 3.5 and PyPy
 * Build on top of lxml and requests
 * Supports recursive WSDL and XSD documents.
 * Supports the xsd:choice and xsd:any elements.
 * Uses the defusedxml module for handling potential XML security issues
 * Support for WSSE (UsernameToken only for now)
 * Experimental support for HTTP bindings
 * Experimental support for WS-Addressing headers

Features still in development include:
 * WSSE x.509 support (BinarySecurityToken)
 * XML validation using lxml XMLSchema's
 * WS Policy support

Please see for more information the documentation at
http://docs.python-zeep.org/




Installation
------------

.. code-block:: bash

    pip install zeep


Usage
-----
.. code-block:: python

    from zeep import Client

    client = Client('tests/wsdl_files/example.rst')
    client.service.ping()


To quickly inspect a WSDL file use::

    python -mzeep <url-to-wsdl>


Please see the documentation at http://docs.python-zeep.org for more
information.


Support
=======

If you encounter bugs then please `let me know`_ .  A copy of the WSDL file if
possible would be most helpful. 

I'm also able to offer commercial support.  Please contact me at
info@mvantellingen.nl for more information.

.. _let me know: https://github.com/mvantellingen/python-zeep/issues


