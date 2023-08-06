=========
shellsnmp
=========

| Shamelessly (ab)using NET-SNMP commands for a quick-and-dirty Python SNMP lib

Usage
-----

Be sure you have MIB files loaded on your system.::

    from shellsnmp.Poller import SNMP

    snmp = SNMP(community='public', host='172.16.1.3')
    status, time = snmp.bulkwalk(mibfile='/path/to/IF-MIB.my', 
        oidspec='ifOperStatus')


Note that only `bulkwalk()` has been implemented at this time.

License and Copyright
---------------------

Licensed MIT

Copyright 2016 - David Michael Pennington (mike /|at|\ pennington.net)


