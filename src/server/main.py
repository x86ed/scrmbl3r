#! /usr/bin/python

import base64
import Cookie
import os
import re
import tornado.httpserver
import tornado.ioloop
import tornado.template
import tornado.web
import helpers
import session
import chat

from controllers import SSLController, MainController

import config

 # Do _not_ touch anything below this line.

settings = dict(
        template_path=config.TEMPLATE_DIR
)

application = tornado.web.Application(
    [
        (r"/", MainController),
    ],
    **settings
)

application.session_manager = session.TornadoSessionManager(config.SESSION_SECRET, config.SESSION_DIR)

redirector = tornado.web.Application([
    (r"/", SSLController),
])

HTTP_SERVER = tornado.httpserver.HTTPServer(application)
REDIRECT_SERVER = tornado.httpserver.HTTPServer(redirector)
HTTPS_SERVER = tornado.httpserver.HTTPServer(application, ssl_options={"certfile": os.path.join(config.CERT_DIR, "certificate.pem"),"keyfile": os.path.join(config.CERT_DIR, "privatekey.pem"),})

def main():
    if config.SSL:
        REDIRECT_SERVER.listen(80)
    else:
        HTTP_SERVER.listen(80)
    HTTPS_SERVER.listen(443)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()