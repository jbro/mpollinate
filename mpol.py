#!/usr/bin/env python
import argparse
import fcntl
import getopt
import hashlib
import os
import random
import struct
import sys
import urllib
import urllib2

def add_entropy(rnd, count):
    fd = os.open("/dev/random", os.O_WRONLY)
    # struct rand_pool_info {
    # int entropy_count;
    # int buf_size;
    # __u32 buf[0];
    # };
    fmt = 'ii%is' % len(rnd)
    rand_pool_info = struct.pack(fmt, 8 * len(rnd), count, rnd)
    fcntl.ioctl(fd, 1074287107, rand_pool_info)
    os.close(fd)

DEFAULT_TIMEOUT = 60
DEFAULT_PORT = 443

parser = argparse.ArgumentParser(description='Seed /dev/random with 512 organic free-range bits')
parser.add_argument('-s', required = True, metavar = 'SERVER', help = 'Pollinate server to use')
parser.add_argument('-p', default = DEFAULT_PORT, metavar = 'PORT', help = 'Port where the pollinate server runs (default: 443)')
parser.add_argument('-t', default = DEFAULT_TIMEOUT, metavar = 'TIMEOUT', help = 'Time in seconds to wait to recieve organic free-range bits (default: %d)' % DEFAULT_TIMEOUT)
args = parser.parse_args()

try:
    challenge = "%032x" % random.getrandbits(512)
    data = urllib.urlencode({'challenge' : challenge})
    req = urllib2.Request("https://%s:%s" % (args.s, args.p), data)
    response = urllib2.urlopen(req, timeout = float(args.t))
    response, random = response.read().split('\n')[0:2]
    h = hashlib.sha512()
    h.update(challenge)
    if h.hexdigest() != response:
        print('%s does not seem to be a pollinate server' % args.s)
        sys.exit(3)
except urllib2.URLError as e:
    print e
    sys.exit(2)

add_entropy(random, 512)

