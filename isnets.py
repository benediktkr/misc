# coding utf-8
#
# -v: remove routes
# -v: print some stuff

from urllib2 import urlopen
import re, sys, os

if os.getuid() is not 0:
    sys.exit('error: run as root')

# The last line in the file is empty
isnets = urlopen('http://www.rix.is/is-net.txt').read().split('\n')[:-1]
router = '192.168.1.1'

if len(sys.argv) > 1:
    router = sys.argv[1]
else:
    sys.exit('error: ip to router')

verbose = '-v' in sys.argv

# Clean out the routes
if "-r" in sys.argv[1:]:
    for network in isnets:
        os.system('ip route del %s' % (network))
        if verbose: print 'deleting %s' % (network)


# Add routes
else:
    for network in isnets:
        os.system('ip route add %s via %s' % (network, router) )
        if "-v" in sys.argv: print network

        

