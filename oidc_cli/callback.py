import asyncio
import cherrypy


class Callback(object):
    result: asyncio.Future

    def __init__(self, result: asyncio.Future):
        self.result = result

    @cherrypy.expose
    def index(self, **kwargs):
        self.result.set_result(kwargs)
        return "Authentication completed, this page can be safely closed now."
