#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2016, David Ewelt
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import unicode_literals, print_function, division

import socket
from threading import Thread
import SocketServer
from SocketServer import ThreadingMixIn, UDPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs

import time
import threading
import json

import zoid

LOG = None

#--------------------------------------------------------------------------------------------------------------------------------
#-- Request object
#--------------------------------------------------------------------------------------------------------------------------------

class Request(object):
    def __init__(self):
        self._handler = None
        self.method = ""
        self.hostname = ""
        self.path = ""
        self.query = ""
        self.headers = []
        self.rfile = None
        self.wfile = None

    @staticmethod
    def create(handler):
        url = ("http://%s:%s" % handler.server.address) + handler.path
        r = urlparse(url)
        q = parse_qs(r.query)

        handler.server_version = "Zoid/%s" % zoid.__version__
        request = Request()
        request._handler = handler
        request.method = "GET"
        request.hostname = r.hostname
        request.path = r.path
        request.query = q
        request.headers = handler.headers
        request.rfile = handler.rfile
        request.wfile = handler.wfile
        return request

    def response(self, obj, status=200, headers=[]):
        self._handler.send_response(status)
        for k,v in headers:
            self._handler.send_header(k,v)
        self._handler.send_header("Content-Type", "application/json")
        self._handler.end_headers()
        json.dump(obj, self.wfile)

    def __str__(self, *args, **kwargs):
        return "<Request(%s %s q=%s)>" % (self.method, self.path, self.query)

#--------------------------------------------------------------------------------------------------------------------------------
#-- BaseRequestHandler
#--------------------------------------------------------------------------------------------------------------------------------

class BaseRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        if self.path == "/favicon.ico":
            return

        self.on_request(Request.create(self))

    def do_POST(self):
        if self.path == "/favicon.ico":
            return

        self.on_request(Request.create(self))

    def on_request(self, request):
        """
            @type request: Request
        """
        pass

    def log_message(self, f, *args):
        return

#--------------------------------------------------------------------------------------------------------------------------------
#-- Long Polling
#--------------------------------------------------------------------------------------------------------------------------------

class ApiRequestHandler(BaseRequestHandler):
    def get_messages(self):
        messages = []
        for message_number,channel,message in self.server.messages:
            if message_number < self.message_number:
                continue
            if channel in self.subscriptions:
                messages.append( (channel, message) )
        self.message_number = self.server.message_number
        return messages

    def on_request(self, request):
        """
            @type request: Request
        """
        if request.path == "/sub":
            self.on_subscription_request(request)
        else:
            request.response({"status": "ok"})

    def on_subscription_request(self, request):
        """
            @type request: Request
        """

        self.subscriptions = request.query.get("c", [])

        t_start = time.time()
        while True:
            messages = self.get_messages()

            if len(messages) == 0:
                if time.time() - t_start >= 5: #-- no messages published in ``timeout`` seconds, end request
                    request.response([], headers=[("Access-Control-Allow-Origin", "*")])
                    return

                time.sleep(0.1) #-- continue waiting for messages
                continue

            #-- send response with the messages
            request.response(messages, headers=[("Access-Control-Allow-Origin", "*")])
            return

class ApiServer(ThreadingMixIn, HTTPServer, Thread):
    def __init__(self, address):
        HTTPServer.__init__(self, address, ApiRequestHandler)
        Thread.__init__(self)

        self.address = address

        self.message_number = 0
        self.messages = []

    def send_message(self, channel, message):
        LOG.debug("added message #%s on channel %s: %s", self.message_number, channel, message)

        self.messages.append( (self.message_number, channel, message) )
        self.message_number += 1

        if len(self.messages) > 100:
            self.messages.pop(0)

    def run(self):
        self.allow_reuse_address = True
        self.serve_forever()

#--------------------------------------------------------------------------------------------------------------------------------
#-- Inter Process Communication
#--------------------------------------------------------------------------------------------------------------------------------

API_ADDRESS = "127.0.0.1", 13042
IPC_ADDRESS = "127.0.0.1", 14042

class IpcRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        #client_address = self.client_address
        data, sock = self.request
        message = json.loads(data)
        self.server.on_message(message)

class IpcServer(ThreadingMixIn, UDPServer, Thread):
    def __init__(self, address):
        UDPServer.__init__(self, address, IpcRequestHandler)
        Thread.__init__(self)

    def on_message(self, message):
        pass

    def run(self):
        self.allow_reuse_address = True
        self.serve_forever()

def send_ipc_message(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data), IPC_ADDRESS)