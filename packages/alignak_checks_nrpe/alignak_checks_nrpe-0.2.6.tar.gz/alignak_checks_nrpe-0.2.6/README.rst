Alignak checks package for NRPE
===============================

Checks pack for monitoring hosts with NRPE


Installation
------------

From PyPI
~~~~~~~~~
To install the package from PyPI:
::
   pip install alignak-checks-nrpe


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::
   git clone https://github.com/Alignak-monitoring-contrib/alignak-checks-nrpe
   cd alignak-checks-nrpe
   sudo python setup.py install


Documentation
-------------

Configuration
~~~~~~~~~~~~~

**Note**: this pack embeds the ``check_nrpe`` binary from the Nagios plugins, this to avoid to have a complete Nagios installation on your Alignak server!

The embedded version of ``check_nrpe`` is only compatible with Linux distros. For Unix (FreeBSD), you can simply install the NRPE plugin:
::

   # Simple NRPE
   pkg install nrpe

   # NRPE with SSL
   pkg install nrpe-ssl

If you wish to use the Nagios ``check_nrpe`` plugin, you must install from your system repository:
::

   # Install local NRPE plugin
   apt-get install nagios-nrpe-plugin
   # Note: This may install all the Nagios stuff on your machine...


After installation, the plugins are commonly installed in the */usr/local/libexec/nagios* directory.

The */usr/local/etc/alignak/arbiter/packs/resource.d/nrpe.cfg* file defines a global macro
that contains the NRPE check plugin installation path. If you do not want to use the installed
plugin (eg. use the Nagios one...), edit this file to update the path
::

    #-- NRPE check plugin installation directory
    # Default is to use the Alignak plugins directory
    $NRPE_PLUGINS_DIR$=$PLUGINS_DIR$
    #--



Prepare monitored hosts
~~~~~~~~~~~~~~~~~~~~~~~
Some operations are necessary on the monitored hosts if NRPE remote access is not yet activated.
::
   # Install local NRPE server
   su -
   apt-get update
   apt-get install nagios-nrpe-server
   apt-get install nagios-plugins

   # Allow Alignak as a remote host
   vi /etc/nagios/nrpe.cfg
   =>
      allowed_hosts = X.X.X.X

   # Restart NRPE daemon
   /etc/init.d/nagios-nrpe-server start

Test remote access with the plugins files:
::
   /usr/local/var/libexec/alignak/check_nrpe -H 127.0.0.1 -t 9 -u -c check_load

**Note**: This configuration is the default Nagios NRPE daemon configuration. Thus it does not
allow to define arguments in the NRPE commands and, as of it, the warning / critical threshold are
defined on the
server side.

Alignak configuration
~~~~~~~~~~~~~~~~~~~~~

You simply have to tag the concerned hosts with the template ``linux-nrpe``.
::

    define host{
        use                     linux-nrpe
        host_name               linux_nrpe
        address                 127.0.0.1
    }



The main ``linux-nrpe`` template only declares the default NRPE commands configured on the server.
You can easily adapt the configuration defined in the ``services.cfg`` and ``commands.cfg.parse`` files.


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... issues in the project repository are
the common way to raise an information.

License
-------

Alignak Pack Checks NRPE is available under the `GPL version 3 license`_.

.. _GPL version 3 license: http://opensource.org/licenses/GPL-3.0