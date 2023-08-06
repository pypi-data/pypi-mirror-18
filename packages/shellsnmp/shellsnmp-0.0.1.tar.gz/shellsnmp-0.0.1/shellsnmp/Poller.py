from subprocess import Popen, PIPE
import re

import arrow

class SNMP(object):
    def __init__(self, host='', community='public'):
        assert host
        self.host = host
        self.community = community

    def _cast(self, text):
        if re.search(r'^\s*\d+\s*$', text):
            # Integer
            return int(text)
        elif re.search(r'^\s*\d+\.\d+\.\d+\.\d+\s*$', text):
            # IP Address
            return str(text)
        else:
            return str(text)

    def _parse(self, text):
        """Parse the output of bulkwalk()"""
        retval = dict()
        for line in text.splitlines():
            vals = re.split('\s+', line)
            retval[self._cast(vals[0].split('.')[-1])] = self._cast(vals[1])
        return retval

    def pivot_table(self, vals1, vals2):
        """Use the common oid index values to combine into one table"""
        assert vals1
        assert vals2
        retval = dict()
        for idx, val1 in vals1.items():
            retval[val1] =vals2.get(idx)
        return retval

    def bulkwalk(self, mibfile="", oidspec=""):
        assert mibfile
        assert oidspec
        cmd = 'snmpbulkwalk -v 2c -m ./{0} -c {1} -Oxsq {2} {3}'.format(
            mibfile, self.community, self.host, oidspec)
        proc = Popen(cmd, shell=True, stdout=PIPE)
        return self._parse(proc.stdout.read()), arrow.now()
        
if __name__=='__main__':
    snmp = SNMP(community='publicfoo', host='172.16.1.3')
    val2 = snmp.bulkwalk(mibfile='IF-MIB.my', oidspec='ifOperStatus')[0]
    val1 = snmp.bulkwalk(mibfile='IF-MIB.my', oidspec='ifDescr')[0]
    print snmp.pivot_table(val1, val2)
