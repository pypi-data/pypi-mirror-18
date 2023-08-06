Ducker
======

What the duck is Ducker?
------------------------

Ducker is a lightweight program that makes internet searchs with DuckDuckGo
from the command line. It can search for images, websites, videos, news and a
lot more.

Usage
-----

Just execute it in your shell with the *search string* as an argument. We call
search string what you want to search for with DuckDuckGo. The following
example searchs for classical music.

.. code-block:: bash

    $ duck classical music

There are also options to search for images, videos, audio, etc. To check out
every option execute the program with the `--help` or `-h` arguments.


Installation
------------

You can clone the repository and install Ducker with...

.. code-block:: bash

    $ python setup.py install

Or you can simply install it with pip...

.. code-block:: bash

    $ pip install ducker

Customization
-------------

You can always use your favourite command-line options of Ducker using Bash
aliases or other utilities available for your shell. Let's say we want to
add an option to search for articles in Wikipedia; we could create a Bash
alias for that.

.. code-block:: bash

    $ alias wikipedia='ducker \!w'

Calling ``wikipedia`` in the shell would open the main page of wikipedia, and
calling ``wikipedia free software`` would open the `"Free software" article
from wikipedia`_. Note that we're using `DuckDuckGo bangs`_ and that the
exclamation mark (!) must be escaped in Bash.

Similarly, you can create an alias to never use JavaScript when using Ducker.

.. code-block:: bash

    $ alias duck='ducker --no-javascript'

.. _DuckDuckGo bangs: https://duckduckgo.com/bang
.. _"Free software" article from wikipedia: https://en.wikipedia.org/wiki/Free_software
