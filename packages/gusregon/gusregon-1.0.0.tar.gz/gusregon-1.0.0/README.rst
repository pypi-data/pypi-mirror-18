gusregon
========

`GUS (Główny Urząd Statystyczny) REGON <https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx>`_ Internet Database client which allows to get detailed information about company based on NIP, Regon or KRS number.

It requires an **API key** to the `BIR1 service <http://bip.stat.gov.pl/dzialalnosc-statystyki-publicznej/rejestr-regon/interfejsyapi/>`_.


Quickstart
----------

Install the package via ``pip``:

.. code-block:: bash

    pip install gusregon


Usage
-----

.. code-block:: python

    from gusregon import GUS

    gus = GUS(api_key='my_api_key')
    gus.search(nip='..')


Sandbox mode for testing:

.. code-block:: python

    from gusregon import GUS

    gus = GUS(sandbox=True)
    gus.search(nip='..')
