# -*- coding: utf-8 -*-

import http.server
import os
import posixpath
import urllib.parse

import click


class LogbookHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    http.server.SimpleHTTPRequestHandler.extensions_map.update({'': 'text/html'})

    def translate_path(self, path):

        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'

        if os.path.isdir(path):
            for ext in '', '.html', '.htm':
                index = '{}/index{}'.format(path, ext)
                if os.path.isfile(index):
                    return index
            self.send_error(404)

        return path


class LogbookHTTPServer(http.server.HTTPServer):
    def __init__(self, base_path, host_name, port, *args, **kwargs):
        http.server.HTTPServer.__init__(self, (host_name, port), LogbookHTTPRequestHandler, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


def run_server(root, port):
    httpd = LogbookHTTPServer(root, 'localhost', port)

    click.echo('Serving path : "{}" at [http://localhost:{}]'.format(root, port))
    click.echo('Press <Ctrl-C> to exit.'.format(root, port))
    httpd.serve_forever()
