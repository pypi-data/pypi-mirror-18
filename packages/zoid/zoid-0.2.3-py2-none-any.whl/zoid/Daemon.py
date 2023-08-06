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

import sys
import os
import subprocess

from zoid import Util, API

LOG = None

def get_pid():
    if os.name == "nt":
        for e in Util.get_processes():
            if "zoid-daemon.exe" in e["cmd"]:
                return e["pid"]
    return 0

def is_running():
    return get_pid() != 0

def main():
    import threading
    import time

    LOG.info("+main()")

    try:
        api_server = API.ApiServer(API.API_ADDRESS)
        api_server.daemon = True

        ipc_server = API.IpcServer(API.IPC_ADDRESS)
        ipc_server.daemon = True

        def on_ipc_message(message):
            LOG.info("IPC message: %s", message)

        ipc_server.on_message = on_ipc_message

        LOG.info("starting API server")
        api_server.start()

        LOG.info("starting IPC server")
        ipc_server.start()

        while threading.active_count() > 0:
            time.sleep(0.1)
    except:
        LOG.exception("error in main() function")

    LOG.info("-main()")

def start():
    if is_running():
        return

    path = os.path.dirname(sys.path[0])
    if os.name == "nt":
        with open(os.path.join(path, "daemon.vbs"), "w") as fp:
            fp.write('CreateObject("Wscript.Shell").Run "zoid-daemon.exe --run", 0, True\n')
    else:
        raise NotImplementedError()

    subprocess.Popen(["start", "daemon.vbs"], cwd=path, shell=True, creationflags=8, close_fds=True)

def kill():
    pid = get_pid()
    if pid == 0:
        return
    if os.name == "nt":
        os.system("taskkill /F /PID %s" % pid)
    else:
        raise NotImplementedError()