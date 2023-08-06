import requests

from requests import Request, Session

from restipy.core.modules import RestipyModule

class RequestsModule(RestipyModule):
    def execute(self, recipe, module_params):
        request = Request(**module_params)
        session = Session()

        response = session.send(request.prepare())

        try:
            json = response.json()
        except:
            json = None

        return {
            'url': response.url,
            'status_code': response.status_code,
            'reason': response.reason,
            'headers': response.headers,
            'cookies': response.cookies,
            'text': response.text,
            'json': json
        }
