mete0r.recipe.sshtunnel
=======================

a `zc.buildout`_ recipe to make on-demand ssh tunnels i.e. ``ssh -L``,
using systemd `socket activation`_.

.. _zc.buildout: https://pypi.python.org/pypi/zc.buildout
.. _socket activation: http://0pointer.de/blog/projects/socket-activation.html


Requirements
------------

=========== ===========
Local side  Remote side
----------- -----------
``systemd``    ``sshd``
``ssh``        ``nc``
=========== ===========


Usage example
-------------

.. attention::

   This package is in its planning stage. Everything can be changed at any time.

In your ``buildout.cfg``, define a `zc.recipe.deployment`_ section::

   [buildout]
   parts =
      tunnel

   [foo]
   recipe = zc.recipe.deployment
   prefix = FOO-DIR
   etc-user = MY-USERNAME
   user = MY-USERNAME
   ...

.. _zc.recipe.deployment: https://pypi.python.org/pypi/zc.recipe.deployment


Then define a tunnel socket in the deployment::

   [foo-db]
   recipe = mete0r.recipe.sshtunnel
   deployment = foo
   socket.name = mysql.sock
   ssh.process.user = MY-USERNAME
   ssh.hostname = 192.168.0.2
   remote.bind = 127.0.0.1:3306

On buildout run, two systemd unit files will be created::

   $ ls -l ~/.config/systemd/user/
   foo-db.socket
   foo-db@.service

Then you can start the listening socket::

   $ systemctl --user start foo-db.socket
   $ systemctl --user list-sockets --all
   LISTEN                         UNIT          ACTIVATES
   FOO-DIR/var/run/foo/mysql.sock foo-db.socket foo-db@0.service

Test it::

   $ mysql --socket=FOO-DIR/var/run/foo/mysql.sock

Enable it to persist::

   $ systemctl --user enable foo-db.socket


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make
