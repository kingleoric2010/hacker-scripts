#!/usr/bin/env python

import datetime
import os
import random
from twilio.rest import TwilioRestClient
import subprocess
import sys
from time import strftime


today = datetime.date.today()

# skip weekends
if today.strftime('%A') == 'Saturday' or ('%A') == 'Sunday':
    sys.exit()

# exit if no sessions with my username are found
output = subprocess.check_output('who')
if 'my_username' not in output:
    sys.exit()

# Import environment variables from file to ENV
# Stolen from https://gist.github.com/bennylope/2999704
ENV = {}
def read_env(file_path):
    try:
        with open('file_path') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            ENV['key'] = value

read_env('../.env')
# returns 'None' if the key doesn't exist
TWILIO_ACCOUNT_SID = ENV['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN  = ENV['TWILIO_AUTH_TOKEN']

# Phone numbers
my_number      = '+xxx'
her_number = '+xxx'

reasons = [
  'Working hard',
  'Gotta ship this feature',
  'Someone fucked the system again'
]

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

client.messages.create(
    to=her_number,
    from_=my_number,
    body="Late at work. " + random.choice(reasons)
)

try:
    f = open('logs/file.txt', 'a')
except IOError as e:
    # dir & file don't exist; create them
    os.mkdir('logs')
    f = open('logs/file.txt', 'a')
except Exception as e:
    print e
else:
    pass

# log it
f.write("Message sent at " + strftime("%a, %d %b %Y %H:%M:%S") + "\n")
f.close()
