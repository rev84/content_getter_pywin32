# coding: utf-8

"""
The MIT License (MIT)

Copyright (c) 2018 Revin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import win32service
import win32serviceutil
import win32event
import datetime
import servicemanager
import socket
import time
import logging

import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import re
import urllib2
import json

IS_DEBUG = False

if IS_DEBUG:
  logging.basicConfig(
      filename = 'F:\\Dropbox\\git\\content_getter_pywin32\\debug.log',
      level = logging.DEBUG,
      format="%(asctime)s %(levelname)s %(message)s"
  )

class WebContentGetterService(win32serviceutil.ServiceFramework):
  _svc_name_ = "Web Content Getter"
  _svc_display_name_ = "Web Content Getter"
  _svc_description_ = 'Web Content Getter'

  def __init__(self, args):
    win32serviceutil.ServiceFramework.__init__(self, args)
    self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

  def SvcStop(self):
    self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
    win32event.SetEvent(self.hWaitStop)

  def SvcDoRun(self):
    PORT = 7777
    Handler = MyRequestHandler
    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

    print "serving at port", PORT
    httpd.serve_forever()

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    # クエリをURLと見て取得
    url = re.sub(r'^/', '', self.path)
    fp = urllib2.urlopen(url)
    fres = fp.read()
    fp.close()

    # 結果を返すためのdic
    res = {
      "response": fres
    }

    # 結果のJSON
    res_json = json.dumps(res)
    
    self.send_response(200)
    self.send_header('Content-type', 'application/json; charset=UTF-8')
    self.send_header('Content-length', len(res_json))
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(res_json)

    if IS_DEBUG:
      logging.info('[Request method] GET')
      logging.info('[Request headers]\n' + str(self.headers))
      logging.info('[Request path]\n' + url)
      logging.info('[Request body]\n' + res_json)

if __name__=='__main__':
  win32serviceutil.HandleCommandLine(WebContentGetterService)