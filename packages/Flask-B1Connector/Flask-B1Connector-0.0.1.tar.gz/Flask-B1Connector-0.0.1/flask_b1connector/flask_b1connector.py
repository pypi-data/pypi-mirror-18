from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

import requests, base64, json

class B1Connector(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'b1restheaders'):
            ctx.b1restheaders = {}

    def connect(self):
        usrPass = "%s:%s" % (current_app.config['B1RESTUSR'], current_app.config['B1RESTPASS'])
        b64Val = base64.b64encode(usrPass)
        return {"Authorization": "Basic %s" % b64Val}

    def getInfo(self):
        requestPath = '/v1/info'
        requestUrl = current_app.config['B1RESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            info = json.loads(response.content)
            return info
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getBoOrderId(self, id):
        req = {
                "num": 1,
                "columns": ["DocEntry"],
                "params": {
                    (current_app.config['FEORDERIDUDF'] if current_app.config['FEORDERIDUDF'] != '' else 'NumAtCard'): {
                        'value': id
                    }
                }
            }
        requestPath = '/v1/orders'
        requestUrl = current_app.config['B1RESTENDPOINT'] + requestPath
        response = requests.post(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(req, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            boOrderid = None if len(data) == 0 else data[0]['DocEntry']
            return boOrderid
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def insertOrder(self, order):
        requestPath = '/v1/order'
        requestUrl = current_app.config['B1RESTENDPOINT'] + requestPath
        response = requests.post(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(order, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data['bo_order_id']
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    @property
    def headers(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'b1restheaders'):
                ctx.b1restheaders = self.connect()
            return ctx.b1restheaders
