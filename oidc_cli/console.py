import asyncio
import os
import socket
import tempfile
import webbrowser
from time import sleep

import cherrypy
from oidcrp import RPHandler, DEFAULT_RP_KEY_DEFS

from oidc_cli.argument import setup
from .callback import Callback

import logging


def run():
    adjust_key_jar_path()
    port = pick_free_port()
    baseurl = f'http://localhost:{port}'
    rp = RPHandler(base_url=baseurl, client_configs={
        'this': config(baseurl)
    })

    info = rp.begin('this')
    issuer = rp.do_provider_info(state=info['state'])
    result = do_auth(info['url'], port)
    rp.finalize(issuer, result)

    print(result['id_token'])


def adjust_key_jar_path():
    tmpdir = tempfile.mkdtemp()
    DEFAULT_RP_KEY_DEFS.update({
        'private_path': os.path.join(tmpdir, 'private'),
        'public_path': os.path.join(tmpdir, 'public')
    })


def pick_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]
    finally:
        sock.close()


def do_auth(login_url: str, callback_port: int):
    auth_result = asyncio.Future()

    cherrypy.config.update({
        'server.socket_port': callback_port,
        'log.screen': False,
        'log.access_file': '',
        'log.error_file': ''
    })
    cherrypy.tree.mount(Callback(auth_result), '/')
    cherrypy.engine.start()
    webbrowser.open(login_url)

    while not auth_result.done():
        sleep(1)

    cherrypy.engine.stop()
    return auth_result.result()


def config(baseurl):
    result = setup()
    result.update({'redirect_uris': [baseurl]})
    return result


if __name__ == '__main__':
    run()
