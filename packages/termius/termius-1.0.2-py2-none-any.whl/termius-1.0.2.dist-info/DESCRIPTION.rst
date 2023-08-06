Termius CLI utility
===================

|Build status| |Code Climate| |Test Coverage|

Provides command line interface for cross-platform terminal Termius.

[this project used to be named serverauditor-sshconfig in the past]

Demo
----

|demo|

Installation
------------

For macOS users, there is a `Homebrew <http://brew.sh/>`__ formulae.
Usage:

.. code:: bash

    $ brew install termius

**Note**: By default, the command above installs bash and zsh
completions.

For Linux users, there is a ``bootstrap.sh`` script. Usage:

.. code:: bash

    $ curl -sSL https://raw.githubusercontent.com/Crystalnix/termius-cli/master/bootstrap.sh | bash

Termius CLI utility can be installed via
`pip <http://www.pip-installer.org/en/latest/index.html>`__:

.. code:: bash

    pip install -U termius

or `easy\_install <http://pythonhosted.org/distribute/>`__:

.. code:: bash

    easy_install -U termius

Usage
-----

Login to termius.com

.. code:: bash

    termius login

Pull data from termius.com

.. code:: bash

    termius pull

Create host

.. code:: bash

    termius host --address localhost --label myhost

Connect to host

::

    termius connect myhost

Push data to termius.com

.. code:: bash

    termius push

Create hosts from ssh config

.. code:: bash

    termius sync ssh

License
-------

Please see
`LICENSE <https://github.com/Crystalnix/termius-cli/blob/master/LICENSE>`__.

.. |Build status| image:: https://travis-ci.org/Crystalnix/termius-cli.svg?branch=master
   :target: https://travis-ci.org/Crystalnix/termius-cli
.. |Code Climate| image:: https://codeclimate.com/github/Crystalnix/termius-cli/badges/gpa.svg
   :target: https://codeclimate.com/github/Crystalnix/termius-cli
.. |Test Coverage| image:: https://codeclimate.com/github/Crystalnix/termius-cli/badges/coverage.svg
   :target: https://codeclimate.com/github/Crystalnix/termius-cli/coverage
.. |demo| image:: https://asciinema.org/a/9v8xuygkowzau16y3zp19u0ov.png
   :target: https://asciinema.org/a/9v8xuygkowzau16y3zp19u0ov?autoplay=1


