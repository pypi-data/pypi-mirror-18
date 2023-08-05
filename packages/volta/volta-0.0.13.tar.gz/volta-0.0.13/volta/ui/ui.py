# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import os
import logging
import argparse
import webbrowser
#%matplotlib inline

from pkg_resources import resource_filename

from volta.ui.handlers.barplot import BarplotBuilder
from volta.ui.handlers.lmplot import LmplotBuilder
from volta.ui.handlers.record  import Recorder
from volta.ui.handlers.plot import PlotDisplayer


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """ index page w/ buttons """
        self.render(
            resource_filename(__name__, 'handlers/templates/index.html'),
            title="Volta UI"
        )


def make_app():
    static_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/barplot", BarplotBuilder),
        (r"/lmplot", LmplotBuilder),
        (r"/record", Recorder),
        (r"/plot", PlotDisplayer),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path}),
    ])

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Configures ui tornado server.')
    parser.add_argument('--port', dest='port', default=8888, help='port for webserver (default: 8888)')
    #parser.add_argument('--plots', dest='plots', default='./plots', help='path to plots directory')
    #parser.add_argument('--logs', dest='logs', default='./logs', help='path to logs direcoty')
    args = parser.parse_args()

    work_dirs = {
        'plots' : 'plots',
        'logs' : 'logs',
    }
    for key, dirname in work_dirs.iteritems():
        try:
            os.stat(dirname)
        except:
            logging.debug('Directory %s not found, trying to create it', dirname)
            os.mkdir(dirname)
    app = make_app()
    app.listen(args.port)
    url = "http://localhost:{port}".format(port=args.port)
    webbrowser.open(url,new=2) #new=2 means open in new tab if possible
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
