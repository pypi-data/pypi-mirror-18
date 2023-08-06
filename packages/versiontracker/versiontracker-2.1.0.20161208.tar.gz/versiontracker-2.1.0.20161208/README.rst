Version Tracker
===============

`Version Tracker <https://gitlab.com/gallaecio/versiontracker>`_ is a project
that provides both a command-line tool and a Python library to query the latest
stable versions of different software products using web scrapping.

For example::

    $ versiontracker vlc
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/


It is currently being used to detect obsolete packages in `Chakra
<http://chakralinux.org/>`_ [1]_ and to feed updated software version
information to `Wikidata <http://wikidata.org/>`_ [2]_.

.. [1] `chakraversiontracker <http://chakra-version-tracker.rtfd.io/>`_
.. [2] `Shyde <http://goo.gl/HBBWsC>`_

Requirements
------------

Version Tracker requires `Python 3 <https://docs.python.org/3/>`_ and the
following Python packages:

- `python-dateutil <https://labix.org/python-dateutil>`_

- `pyxdg <https://www.freedesktop.org/wiki/Software/pyxdg/>`_

- `Scrapy <https://doc.scrapy.org/en/latest/>`_

- `termcolor <https://pypi.python.org/pypi/termcolor>`_

To build the offline documentation, you also need:

- `sphinx-argparse <https://sphinx-argparse.readthedocs.io/en/latest/>`_

And the tools that we use to develop Version Tracker itself also require:

- `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_

- `requests <http://docs.python-requests.org/en/master/>`_


Installation
------------

Use `pip <https://pip.pypa.io/en/stable/quickstart/>`_ to install::

    pip install versiontracker


Basic Command-Line Usage
------------------------

To use the :ref:`versiontracker <cli_reference>` command-line application pass
it a list of software IDs::

    $ versiontracker vlc xfce
    vlc: 2.2.2 (2016-07-06) @ http://get.videolan.org/vlc/
    xfce: 4.12 (2015-02-28) @ http://archive.xfce.org/xfce/

You can use the `-l` option to get a list of supported software IDs::

    $ versiontracker -l
    0ad
    4kslideshowmaker
    …

.. _library-usage:

Basic Library Usage
-------------------

Use :func:`version_info() <versiontracker.version_info>` to get information
about the latest stable version of a single product::

    >>> from pprint import pprint
    >>> from versiontracker import version_info
    >>> pprint(version_info('vlc'))
    {'id': 'vlc',
     'date': datetime.datetime(2016, 7, 6, 10, 10),
     'url': 'http://get.videolan.org/vlc/',
     'version': '2.2.2'}

Use :func:`iter_version_info() <versiontracker.iter_version_info>` to iterate
through the version information of several products::

    >>> from versiontracker import iter_version_info
    >>> for version_data in iter_version_info(('vlc', 'xfce')):
    ...     pprint(version_data)
    ...
    {'id': 'vlc',
     'date': datetime.datetime(2016, 7, 6, 10, 10),
     'url': 'http://get.videolan.org/vlc/',
     'version': '2.2.2'}
    {'id': 'xfce',
     'date': datetime.datetime(2015, 2, 28, 21, 7),
     'url': 'http://archive.xfce.org/xfce/',
     'version': '4.12'}

Use :func:`supported_software() <versiontracker.supported_software>` to get a
list of supported software IDs::

    >>> from versiontracker import supported_software
    >>> supported_software()
    ['kde-l10n-ca', 'kdiamond', 'kontactinterface', 'entropy', …]


Extending Software Support
--------------------------

Version Tracker is not designed to let each user keep their custom software
tracking data or code. Changes require you to *fork* the source code. If you
do, we encourage you to `send us back your changes
<https://gitlab.com/gallaecio/versiontracker/merge_requests>`_ so that everyone
can benefit from them.

Use the following to clone the Git repository and install in development mode,
so that your changes have effect on your system as soon as you save them:

.. code-block:: bash

    # If you have versiontracker installed:
    sudo pip3 uninstall versiontracker

    git clone https://gitlab.com/gallaecio/versiontracker.git
    cd versiontracker
    sudo python3 setup.py develop

You can now work directly on the newly created folder, and whenever you execute
:code:`versiontracker` the code in that folder will be executed.

The following documents describe in details how to extend software support:

-   :doc:`/extending_data` describes how to add new software entries to the
    :code:`data.json` file.

    This is how you extend software support, as long as you can use one of the
    existing spiders for the software that you want to support.

-   :doc:`/creating_spiders` describes how to write your own spider, a Python
    class that can fetch version information of one or more software products.

.. _cli_reference:

Command Line Help
-----------------

..  argparse::
    :module: versiontracker.cli
    :func: build_argument_parser
    :prog: versiontracker
    :nodefault:

..  tip:: The Version Tracker command-line interface supports autocompletion of
    software IDs and spider names, you just need to `activate autocompletion
    support <https://argcomplete.readthedocs.io/en/latest/>`_.


API Reference
-------------

- :ref:`versiontracker`

- :ref:`versiontracker.spiders`


Credits and License
-------------------

Version Tracker may be used under the terms of the :doc:`GNU Affero General
Public License version 3 </license>` or later (AGPLv3+).

For a list of authors who should be credited, see :doc:`/authors`.

.. toctree::
   :hidden:

   self
   extending_data
   creating_spiders
   versiontracker
   license
   authors
