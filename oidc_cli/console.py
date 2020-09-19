import asyncio
import os
import tempfile
import webbrowser
import socket
from time import sleep

import cherrypy
from oidcrp import RPHandler, DEFAULT_RP_KEY_DEFS

from .callback import Callback


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

    cherrypy.config.update({'server.socket_port': callback_port})
    cherrypy.tree.mount(Callback(auth_result), '/')
    cherrypy.engine.start()
    webbrowser.open(login_url)

    while not auth_result.done():
        sleep(1)

    cherrypy.engine.stop()
    return auth_result.result()


def config(baseurl):
    return {
        'issuer': 'https://login.partner.microsoftonline.cn/d9b5e346-fa0c-40a4-8cec-ad494f51265e/v2.0',
        'client_id': '359a7248-c9ea-4fcc-b5be-ee4fa2d5a2f9',
        'redirect_uris': [baseurl],
        'behaviour': {
            'response_types': ['id_token'],
            'scope': ['openid']
        },
        'request_args': {
            'response_mode': 'form_post'
        },
        'allow': {
            'issuer_mismatch': True
        }
    }


if __name__ == '__main__':
    run()
