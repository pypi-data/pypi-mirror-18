MakePath
========

MakePath is a small library which aims to facilitate paths building from various locations.

MakePath is released under the `LGPL v3 license <https://www.gnu.org/licenses/lgpl-3.0.en.html>`_.

How to use it
-------------

Here is how to make a path from root :

.. code-block:: python

    >>> import makepath
    >>> makepath.from_root("usr", "local", "bin")
    '/usr/local/bin'

You can of course make paths from other locations. See the `project's documentation`_ for more information.

.. _`project's documentation`: http://makepath.okozak.ovh/


