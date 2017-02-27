#!/usr/bin/env python
import subprocess
import argparse
import os
import time
import sys
import re


parser = argparse.ArgumentParser(description='Script ueberprueft einen Host ob dieser rebootet hat.')
parser.add_argument('hostname', metavar='HOST', type=str,
                   help='Welcher Host soll abgefragt werden')
parser.add_argument('-t', dest='timeout', metavar='timeout', type=int, default=60,
                   help='Wie lange soll versucht werden einen Reboot zu erkennen.\n defaults = 60')
args = parser.parse_args()


# how log to check the host
observe_time = args.timeout
start_time = int(time.time())


class Hoststate():
  def __init__(self, host):
      self.hostname = host 
      self.state = None
      self.state_list = []
      self.rebooted = None

  def isRebooted(self):
      if re.match(".*1[0]{2,}11.*", "".join(self.state_list)):
          self.rebooted = True
          return True
      else:
          self.rebooted = False
          return False

  def check(self):
      with open(os.devnull, 'w') as devnull:
          try:
              self.__p = subprocess.check_call(['ping', '-w', '1', '-c', '1', self.hostname], stdout=devnull, stderr=devnull)
          except subprocess.CalledProcessError:
              self.__p = None
      self.state =  1 if self.__p == 0 else 0
      self.state_list.append(str(1) if self.__p == 0 else str(0))


server=Hoststate(args.hostname)
rc = None

try:
    while True:
        server.check()
        if server.isRebooted():
            print "Server is rebooted"
            rc = 0
            break
        if ( int(time.time()) - start_time ) > observe_time:
            print "Server NOT rebooted" 
            rc = 1
            break
        time.sleep(2)
except KeyboardInterrupt:
    print server.state_list
    rc = 1
    sys.exit(rc)
finally:
    print server.state_list
    sys.exit(rc)
