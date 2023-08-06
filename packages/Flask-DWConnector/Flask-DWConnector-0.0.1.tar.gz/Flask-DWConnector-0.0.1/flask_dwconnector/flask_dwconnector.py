from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

import requests, base64, json

class DWConnector(object):

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
        if hasattr(ctx, 'dwrestheaders'):
            ctx.dwrestheaders = {}

    def connect(self):
        usrPass = "%s:%s" % (current_app.config['DWRESTUSR'], current_app.config['DWRESTPASS'])
        b64Val = base64.b64encode(usrPass)
        return {"Authorization": "Basic %s" % b64Val}

    def getLastCut(self, app, task):
        requestPath = '/control/cutdt/' + app + '/' + task
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            cutDt = json.loads(response.content)
            return cutDt
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def insertSyncControl(self, app, task, syncTask):
        requestPath = '/control/synccontrol/' + app + '/' + task
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(syncTask, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data['mongo_sync_control_id']
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getTask(self, taskId):
        requestPath = '/control/task/' + taskId
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            data = json.loads(response.content)
            return data['result']
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getTaskStatus(self, taskId):
        requestPath = '/control/taskstatus/' + taskId
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getSyncTask(self, _id):
        requestPath = '/control/synctask/' + _id
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            data = json.loads(json.loads(response.content))
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def delSyncTask(self, _id):
        requestPath = '/control/synctask/' + _id
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.delete(requestUrl, headers=self.headers)
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getSyncTasks(self, app, task, params):
        requestPath = '/control/synctasks/' + app + '/' + task
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(params, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def reSyncOrdersChain(self, _id):
        requestPath = '/control/taskcmd/resyncorderschain'
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps({"_id": _id}, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def updateSyncTask(self, _id, entities):
        requestPath = '/control/synctask/' + _id
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(entities, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(json.loads(response.content))
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def syncOrder(self, feOrderId ,order):
        requestPath = '/backoffice/order/' + feOrderId
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(order, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def getOrder(self, feOrderId):
        requestPath = '/backoffice/order/' + feOrderId
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.get(requestUrl, headers=self.headers)
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    def updateOrderStatus(self, feOrderId, orderStatus):
        requestPath = '/backoffice/orderstatus/' + feOrderId
        requestUrl = current_app.config['DWRESTENDPOINT'] + requestPath
        response = requests.put(
                                    requestUrl,
                                    headers=self.headers,
                                    data=json.dumps(orderStatus, ensure_ascii=False),
                                    timeout=60,
                                    verify=True
                                )
        if response.status_code == 201:
            data = json.loads(response.content)
            return data
        else:
            current_app.logger.error(response.content)
            raise Exception(response.content)

    @property
    def headers(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'dwrestheaders'):
                ctx.dwrestheaders = self.connect()
            return ctx.dwrestheaders
