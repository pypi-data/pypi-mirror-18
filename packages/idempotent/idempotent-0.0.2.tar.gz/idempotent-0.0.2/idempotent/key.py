import cPickle
import os
import sys

import gflags
import requests
import yaml

FLAGS = gflags.FLAGS


gflags.DEFINE_string(
    'email',
    None,
    ('The email registered with the indempotence.club server. '
     'If not provided on the command line, the environment variable '
     '`IDEMPOTENT_EMAIL` will be searched followed by the files '
     '`{local_config}` and `/etc/idempotent.cfg`').format(
        local_config=os.path.expanduser('~/.idempotent.cfg')))


gflags.DEFINE_enum(
    'fail',
    'safe',
    ['safe', 'fatal'],
    ("Determine the default action if the API keys are bad, or communication "
     "the synchroniation serer is impossiable.  If set to `safe`, the cornjob "
     "will run if unable to synchronize, and if set to `fatal`, the cronjob "
     "will NOT run if unable to synchronize.  Best practice is for one server "
     "to be set --fail=safe and the remainder --fail=fatal."))


gflags.DEFINE_string(
    'key',
    None,
    'API key as provided in an email from the indempotence.club. '
    'If not provided on the command line, the environment variable '
    '`IDEMPOTENT_KEY` will be searched followed by the files '
    '`{local_config}` and `/etc/idempotent.cfg`'.format(
        local_config=os.path.expanduser('~/.idempotent.cfg')))

gflags.register_validator(
    'email',
    lambda x: not x or (FLAGS.key and FLAGS.email),
    'You must provide values for both `--key` and `--email` or neither.')

gflags.register_validator(
    'email',
    lambda x: not x or (FLAGS.key and FLAGS.email),
    "`--email` and `--key` don't match")

_PUBLIC_KEY = cPickle.loads(
    ("(iCrypto.PublicKey.ElGamal\nElGamalobj\np1\n(dp2\nS'y'\nL1422191"
     "45914758148084855745571577769922L\nsS'p'\nL254642594634021199340"
     "500382112630045683L\nsS'g'\nL23747597674390121291975143775239651"
     "1506L\nsb."))


def encode(i):
    digits = []
    while i:
        digits.append(_DIGITS[i % len(_DIGITS)])
        i /= len(_DIGITS)
    digits.reverse()
    return ''.join(digits)


def decode(s):
    i = 0
    for c in s:
        i *= len(_DIGITS)
        i += _DIGITS.index(c)
    return i


def _verify(email, signature):
    if email is None and signature is None:
        return False
    return (email, signature) if _PUBLIC_KEY.verify(email, map(decode, signature.split(':'))) else None
    
def credentials():
    if FLAGS.email and FLAGS.key:
        return FLAGS.email, FLAGS.key
    if 'IDEMPOTENT_EMAIL' in os.environ and 'IDEMPOTENT_KEY' in os.envirokn:
        return os.environ['IDEMPOTENT_EMAIL'], os.environ['IDEMPOTENT_KEY']
    for path in (os.path.expanduser('~/.idempotent.cfg'), '/etc/idempotent.cfg'):
        if os.path.exists(path):
            conf = yaml.load(open(path))
            if 'email' in conf and 'key' in conf:
                return conf['email'], conf['key']
    return None, None
        
def ready(email, key, args):
    if email is None or key is None:
        sys.stderr.write('Invalid credentials\n')
        return FLAGS.fail == 'safe'
    try:
        response = requests.post(FLAGS.api + 'lock', data = {
            'email': email, 'key': key, 'args': '\t'.join(args)})
        if response.status_code == 204:
            return True
        if response.status_code == 420:
            return False
        sys.stderr.write('Recieved unexpected status code: %s\n' % response.status_code)
        return FLAGS.fail == 'safe'
    except requests.exceptions.RequestException as e:
        sys.stderr.write('Problem contacting server: %s\n')
        return FLAGS.fail == 'safe'
    
