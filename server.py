#-*- coding:utf-8 -*-
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from werkzeug.exceptions import abort
from jsonrpc import JSONRPCResponseManager, dispatcher
from flask import Flask, request, render_template

app = Flask(__name__)
address = '0.0.0.0'
port = 8000

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', **dict(address=address, port=port))


@dispatcher.add_method
def add(**params):
    return params['x'] + params['y']


@app.route('/rpc')
def rpc():
    ws = request.environ.get('wsgi.websocket') or abort(400)
    while True:
        message = ws.receive()
        response = JSONRPCResponseManager.handle(message, dispatcher)
        if response is not None:
            ws.send(response.json)


if __name__ == '__main__':
    print('listening on {}:{}'.format(address, port))
    http_server = WSGIServer((address, port), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
