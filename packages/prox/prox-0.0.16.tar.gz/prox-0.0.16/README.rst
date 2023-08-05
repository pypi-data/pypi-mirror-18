Prox - the tool to check how bad your proxy list is
===================================================

Installation
------------

.. code:: bash

    pip3 install -U prox


How to check the proxy list
---------------------------

You have to provide at least the type and location of proxy list.

If the proxylist located at http://example.com/abc.txt:

.. code:: bash

    prox_check socks URL http://example.com/abc.txt

If the list is in local file:

.. code:: bash

    prox_check socks path/to/file.txt


How to check multiple lists
---------------------------

Create file foo.yml like:

.. code:: text
    
    config:
      save: 1

    task:
      - proxy_type: socks
        plist_url: var/plist1.txt
        limit: 100

      - proxy_type: http
        plist_url: http://example.com/servers.txt
        limit: 100

It should by YML list of tasks. Each task contains key names same
as check_plist.py command line arguments.

Run the command:

.. code:: bash

    prox_task foo.yml

The tool to filter proxy list by countries
------------------------------------------

Use `prox_geo` command with `--stat` option to see number of proxies grouped by country.

Use `prox_geo` command with `-i`, `-x` and `--exclude-list` options to filter proxy list
