import pipes
import sys

import gflags
import requests

from .key import credentials 

FLAGS = gflags.FLAGS

gflags.DEFINE_string(
    'register',
    None,
    'Register a new account for an email address')

gflags.DEFINE_bool(
    'invalidate',
    False,
    'Invalidate and reissue a new API key')

gflags.register_validator(
    'register',
    lambda x:x or (not x and not FLAGS.key),
    "Don't provide a `--key` when regsitering")



def register():
    if "i accept" != raw_input(
            ("  Enter 'I ACCEPT' if you accept our terms of service at\n"
             "  https://idempotence.herokuapp.com/tos.html and agree to\n"
             "  occationally receive emails announcing product, service\n"
             "  and tos changes.\n\n>>> ")).lower().replace("'","").strip():
        print "Sorry, you have to accept the TOS to use this application"
        return 0
    resp = requests.post(FLAGS.api + "register", data=dict(email=FLAGS.register))
    if resp.status_code < 400:
        print "Great, your API key is on its way."
        return 0
    else:
        print "Opps, there was an error: ", resp.status_code
        print resp.text
        return 1
        

def invalidate():
    email, key = credentials()
    if not email or not key:
        print "Can't invalidate - you are not currently configured with a valid set of credentials."
        print "Reregister with idempotent --register <your email> to get your current creds, set them"
        print "up and try again."
        return 1
    response = requests.post(FLAGS.api + "invalidate", data = {'email': email, 'key': key})
    if response.status_code < 400:
        print "Great, your new API key is on its way."
        return 0
    print "Looks like your current credentials are not any good"
    print "Reissue your current credentials:"
    print "  # idempotent --register=%s" % pipes.quote(email)
    print "and then invalidate them:"
    print "  # idempotent --invalidate"
        
    return 0
