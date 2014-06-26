#!/usr/bin/env python
# Copyright (c) 2014, Paessler AG <support@paessler.com>
#All rights reserved.

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import sys
import time

conf = {}
restrict_answer = True

#Read config file
with open('./qosreflect.conf') as config:
    for line in config:
        if not line.startswith('#'):
            conf[line.split(":")[0]] = line.split(":")[1].rstrip()
print 'Read config done'
if conf['host'] == 'All':
    HOST = ''  # Empty host means bind to all available interfaces
else:
    HOST = conf['host']
PORT = int(conf['port'])

if conf['replyip'] == 'None':
    restrict_answer = False

# receive data from client (data, addr)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'
while 1:
    d = s.recvfrom(4096)
    if d and not restrict_answer:
        data = d[0]
        addr = (d[1][0], PORT)
        reply = data
        s.sendto(reply, addr)
    elif d and restrict_answer:
        if d[1][0] == conf['replyip']:
            data = d[0]
            addr = (d[1][0], PORT)
            reply = data
            s.sendto(reply, addr)
        else:
            pass
    else:
        print 'Waiting for data'
        time.sleep(0.1)
s.close()
