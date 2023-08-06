=================
ejabberd-htpasswd
=================

Yet another ejabberd authentication bridge that uses apache-style
.htpasswd files.

.. WARNING::

  Currently, **ONLY** bcrypt-type hash passwords are supported in the
  htpasswd file, i.e. hashes that start with ``$2a$`` or ``$2y$``.


Project
=======

* Homepage: https://github.com/metagriffin/ejabberd-htpasswd
* Bugs: https://github.com/metagriffin/ejabberd-htpasswd/issues


Installation
============

.. code:: bash

  $ sudo apt-get install libffi-dev
  $ pip install ejabberd-htpasswd


Configuration
=============

Update the authentication configuration in your
``/etc/ejabberd/ejabberd.cfg`` file:

.. code:: erlang

  {auth_method, external}.
  {extauth_program, "/usr/local/bin/ejabberd-htpasswd /path/to/htpasswd"}.
  %% optional -- update as appropriate
  %% {extauth_instances, 2}.
  %% {extauth_cache, 300}.


Options
=======

The `ejabberd-htpasswd` script takes one optional positional argument,
the fully-qualified path to the ".htpasswd" file, and several optional
parameters:

* ``-d``, ``--debug``:

  Enable debug mode for more stuff in the log files.

* ``-l {FILENAME}``, ``--log-file {FILENAME}``:

  The log file name, which will be rotated as defined by ``-s`` and
  ``-c``; default: ``/var/log/ejabberd/auth-htpasswd.log``.

* ``-s BYTES``, ``--log-size BYTES``:

  specify the maximum size of the log file in bytes before the log
  file is rotated; default: 1048576 (1 MB).

* ``-c NUMBER``, ``--log-count NUMBER``:

  specify the maximum number of log rotation files; default: 10.

* ``-t EXPR``, ``--domain-transform EXPR``:

  specify a "sed"-style substitution expression for domain name
  transformation; example: ``/.*\.example\.com$/example\.com/``. Note
  that when placed in the ejabberd config file, several layers of
  escaping must be done, so you'll need something like this to
  accomplish the above:

  .. code:: erlang

    {extauth_program,
      "/usr/local/bin/ejabberd-htpasswd \\
        -t /.*\\\\.example\\\\.com$/example.com/ \\
        /path/to/htpasswd"}.
