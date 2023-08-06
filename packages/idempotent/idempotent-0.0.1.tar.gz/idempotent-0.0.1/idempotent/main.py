import gflags
import os
import sys

from .register import register, invalidate
from .key import credentials, ready


FLAGS = gflags.FLAGS

gflags.DEFINE_string(
    'api',
    'https://idempotence.herokuapp.com/',
    'The root url to connect to.  Change this when testing')


def run():
    args = FLAGS(sys.argv)
    if FLAGS.register:
        sys.exit(register())
    elif FLAGS.invalidate:
        invalidate()
        sys.exit(0)
    elif not args:
        print "You requested indempotentification, but didn't provide anything to idempotentify!"
        sys.exit(1)
    creds = credentials()
    if ready(*creds, args=args):
        args[0] = args[1]
        os.execlp(*args)
    return sys.exit(0)
    
    
    
