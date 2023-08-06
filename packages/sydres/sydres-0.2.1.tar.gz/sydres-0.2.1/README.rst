Sydres - Redsys Client
----------------------

.. image:: https://travis-ci.org/alexbarcelo/sydres.svg?branch=master
    :target: https://travis-ci.org/alexbarcelo/sydres

.. image:: https://coveralls.io/repos/github/alexbarcelo/sydres/badge.svg?branch=master
    :target: https://coveralls.io/github/alexbarcelo/sydres

ATTENTION
---------

This is a fork of:

https://bitbucket.org/zikzakmedia/python-redsys

The focus is adding Python 3 support and some minor improvements.

Credit to the original author, which can be found in the Bitbucket URL.

Redsys client
~~~~~~~~~~~~~

Credit payments to the Redsys service.

Requirements
------------

* Python 2.7

Installation
------------

Through pip:

.. code-block:: python

    pip install redsys

or easy_install:

.. code-block:: python

    easy_install redsys
    
or download the source, un-tar/un-zip it, cd into redsys, and:

.. code-block:: python

    python setup.py install

Quick Start
-----------

.. code-block:: python

    from redsys import Client

    SANDBOX = True
    REDSYS_MERCHANT_URL = 'http://www.zikzakmedia.com'
    REDSYS_MERCHANT_NAME = "Zikzakmedia SL"
    REDSYS_MERCHANT_CODE = '000000000'
    REDSYS_SECRET_KEY = '123456'
    REDSYS_TERMINAL = u'1'
    REDSYS_CURRENCY = u'978'
    REDSYS_TRANS_TYPE = u'0'

    values = {
            'DS_MERCHANT_AMOUNT': 10.0,
            'DS_MERCHANT_CURRENCY': 978,
            'DS_MERCHANT_ORDER': 'SO001',
            'DS_MERCHANT_PRODUCTDESCRIPTION': 'ZZSaas services',
            'DS_MERCHANT_TITULAR': REDSYS_MERCHANT_NAME,
            'DS_MERCHANT_MERCHANTCODE': REDSYS_MERCHANT_CODE,
            'DS_MERCHANT_MERCHANTURL': REDSYS_MERCHANT_URL,
            'DS_MERCHANT_URLOK': 'http://localhost:5000/redsys/confirm',
            'DS_MERCHANT_URLKO': 'http://localhost:5000/redsys/cancel',
            'DS_MERCHANT_MERCHANTNAME': REDSYS_MERCHANT_NAME,
            'DS_MERCHANT_TERMINAL': REDSYS_TERMINAL,
            'DS_MERCHANT_TRANSACTIONTYPE': REDSYS_TRANS_TYPE,
        }

    redsyspayment = Client(business_code=REDSYS_MERCHANT_CODE, secret_key=REDSYS_SECRET_KEY, sandbox=SANDBOX)
    redsys_form = redsyspayment.redsys_generate_request(values)

Thanks
------

* Thanks `Eduard Carreras <https://bitbucket.org/ecarreras/>`_ to start python-sermepa package.
* Thanks `Álvaro Vélez <https://github.com/alvarovelezgalvez>`_ and `Jordi Colell <https://github.com/jordic>`_
  to develop new signature Redsys HMAC-256 (`Django-sermepa <https://github.com/alvarovelezgalvez/django-sermepa/>`_).
