#!/usr/bin/env python
#Copyright (c) 2014, Paessler AG <support@paessler.com>
#All rights reserved.
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#1. Redistributions of source code must retain the above copyright notice, this list of conditions
# and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the distribution.
#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
# or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import sys
import time
if sys.version_info < (2, 7):
    print("Python Version too old. Exiting!")
    sys.exit()
else:
    import argparse

# Parsing some optional arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--port', help='Provide port defined in PRTG')
argparser.add_argument('-c', '--conf', help='Path of config file, if not provided default qosreflect.conf will be used')
argparser.add_argument('-o', '--host', help='Provide the IP address if the interface the script should bind to. '
                                            'Use ''All'' to bind to all available interfaces(recommended)')
argparser.add_argument('-r', '--replyip', help='Provide the IP address of the PRTG Probe which sends the packets. '
                                               'The reflector then will only reply to this IP')
argparser.add_argument('-t', '--replyport', help='Provide the port the packets should be bounced to')
argparser.add_argument('-n', '--nat', help='Option enables the NAT mode so packets are reflected exactly '
                                           'to the port they are received from', action='store_true')
argparser.add_argument('-d', '--debug', help='Set to turn on detailed output', action="store_true")
args = argparser.parse_args()


def read_conf(path):
    configuration = {}
    with open(path) as config:
        for line in config:
            if not line.startswith('#'):
                configuration[line.split(":")[0]] = line.split(":")[1].rstrip()
    return configuration

conf = {}
restrict_answer = True

#Read config file or from arguments
if not args.conf:
    conf['replyip'] = args.replyip
    conf['host'] = args.host
    conf['port'] = args.port
else:
    conf = read_conf(args.conf)
if args.debug:
    print(conf)
    print('Read config done')

if conf['host'] == 'All':
    HOST = ''  # Empty host means bind to all available interfaces
else:
    HOST = conf['host']
if args.replyport:
    PORT = int(args.replyport)
else:
    PORT = int(conf['port'])

if conf['replyip'] == 'None' or not conf['replyip']:
    restrict_answer = False

# receive data from client (data, addr)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if args.debug:
        print('Socket created')
except socket.error as err:
    if args.debug:
        print('Failed to create socket. Error Code : ' + err.errno + ' Message ' + err.strerror)
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as err:
    if args.debug:
        print('Bind failed. Error Code : ' + err.errno + ' Message ' + err.strerror)
    sys.exit()

if args.debug:
    print('Socket bind complete')
while 1:
    d = s.recvfrom(4096)
    if d and not restrict_answer:
        data = d[0]
        addr = (d[1][0], PORT)
        if args.nat:
            addr = (d[1][0], d[1][1])
        reply = data
        s.sendto(reply, addr)
    elif d and restrict_answer:
        if d[1][0] == conf['replyip']:
            data = d[0]
            addr = (d[1][0], PORT)
            if args.nat:
                addr = (d[1][0], d[1][1])
            reply = data
            s.sendto(reply, addr)
        else:
            pass
    else:
        if args.debug:
            print('Waiting for data')
        time.sleep(0.1)
s.close()
