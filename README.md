# mpollinate
A tiny and portable python implementation of a [pollinate](https://github.com/dustinkirkland/pollinate) client

## Rational
There are three reassons behind this.

    1. The official pollinate client only work on Ubuntu.
    2. The official client leaks a bunch of information about OS version, uptime etc to the pollinate server.
    3. The official client does not bump the entropy count in the kernel, so after using it /dev/random still blocks.
