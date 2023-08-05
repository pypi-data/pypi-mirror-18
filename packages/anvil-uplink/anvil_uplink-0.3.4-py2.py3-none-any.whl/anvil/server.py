from __future__ import unicode_literals
import threading, time, json, random, string

from ws4py.client.threadedclient import WebSocketClient

from . import _server, _serialise, _threaded_server
from ._threaded_server import register, callable, callable_as, live_object_backend, LazyMedia

_threaded_server.send_reqresp = lambda r: _get_connection().send_reqresp(r)

__author__ = 'Meredydd Luff <meredydd@anvil.works>'

_url = 'wss://anvil.works/uplink'


_connection = None
_connection_lock = threading.Lock()

_backends = {}

_fatal_error = None

def reconnect(closed_connection):
    global _connection
    with _connection_lock:
        if _connection != closed_connection:
            return
        _connection = None

    def retry():
        time.sleep(1)
        print("Reconnecting...")
        _get_connection()

    try:
        _threaded_server.kill_outstanding_requests('Connection to server lost')

    finally:
        threading.Thread(target=retry).start()


class _Connection(WebSocketClient):
    def __init__(self):
        print("Connecting to " + _url)
        WebSocketClient.__init__(self, _url)

        self._ready_notify = threading.Condition()
        self._ready = False
        self._sending_lock = threading.RLock()

    def is_ready(self):
        return self._ready

    def wait_until_ready(self):
        with self._ready_notify:
            while not self._ready:
                self._ready_notify.wait()

    def _signal_ready(self):
        self._ready = True
        with self._ready_notify:
            self._ready_notify.notifyAll()

    def opened(self):
        print("Anvil websocket open")
        self.send(json.dumps({'key': _key, 'v': 3}))
        for r in _threaded_server.registrations.keys():
            self.send(json.dumps({'type': 'REGISTER', 'name': r}))
        for b in _threaded_server.backends.keys():
            self.send(json.dumps({'type': 'REGISTER_LIVE_OBJECT_BACKEND', 'backend': b}))

    def closed(self, code, reason=None):
        print("Anvil websocket closed (code %s, reason=%s)" % (code, reason))
        self._signal_ready()
        reconnect(self)

    def received_message(self, message):
        global _fatal_error

        if message.is_binary:
            _serialise.process_blob(message.data)

        else:
            data = json.loads(message.data.decode())

            #print "Got message: " + repr(data)

            type = data["type"] if 'type' in data else None

            if 'auth' in data:
                print("Authenticated OK")
                self._signal_ready()
            elif 'output' in data:
                print("Anvil server: " + data['output'].rstrip("\n"))
            elif type == "CALL":
                _threaded_server.IncomingRequest(data)
            elif type == "CHUNK_HEADER":
                _serialise.process_blob_header(data)
            elif type is None and "id" in data and ("response" in data or "error" in data):
                _threaded_server.IncomingResponse(data)
            elif type is None and "error" in data:
                _fatal_error = data["error"]
                print("Fatal error from Anvil server: " + str(_fatal_error))
            else:
                print("Anvil websocket got unrecognised message: "+repr(data))

    def send(self, payload, binary=False):
        with self._sending_lock:
            return WebSocketClient.send(self, payload, binary)

    def send_with_header(self, json_data, blob=None):
        try:
            with self._sending_lock:
                WebSocketClient.send(self, json.dumps(json_data), False)
                if blob is not None:
                    WebSocketClient.send(self, blob, True)
        except TypeError:
            raise _server.AnvilSerializationError("Value must be JSON serializable")

    def send_reqresp(self, reqresp):
        if not self._ready:
            raise RuntimeError("Websocket connection not ready to send request")

        _serialise.serialise(reqresp, self.send_with_header)


_key = None


def _reset_connection():
    global _connection

    _connection = None


def _get_connection():
    global _connection

    if _key is None:
        raise Exception("You must use anvil.server.connect(key) before anvil.server.call()")

    with _connection_lock:
        if _connection is None:
            _connection = _Connection()
            _connection.connect()
            _connection.wait_until_ready()
    return _connection


def connect(key, url='wss://anvil.works/uplink'):
    global _key, _url, _fatal_error
    _key = key
    _url = url
    _fatal_error = None # Reset because of reconnection attempt
    _get_connection()


def run_forever():
    while True:
        time.sleep(1)


def _on_register(name, is_live_object):
    if _connection is not None and _connection.is_ready():
        if is_live_object:
            _connection.send_reqresp({'type': 'REGISTER_LIVE_OBJECT_BACKEND', 'backend': name})
        else:
            _connection.send_reqresp({'type': 'REGISTER', 'name': name})


_threaded_server.on_register = _on_register


def _do_call(args, kwargs, fn_name=None, lo_call=None): # Yes, I do mean args and kwargs without *s
    if _fatal_error is not None:
        raise Exception("Anvil fatal error: " + str(_fatal_error))

    return _threaded_server.do_call(args, kwargs, fn_name, lo_call)


_server._do_call = _do_call


def call(fn_name, *args, **kwargs):
    try:
        return _do_call(args, kwargs, fn_name=fn_name)
    except _server.AnvilWrappedError as e:
        # We need to re-raise here so that the right amount of traceback gets cut off by _report_exception
        raise _server.AnvilWrappedError(e.error_obj)

def wait_forever():
    _get_connection()
    while True:
        try:
            if _fatal_error is not None:
                raise Exception("Anvil fatal error: " + str(_fatal_error))
            call("anvil.private.echo", "keep-alive")
            time.sleep(30)
        except:
            if _fatal_error is None:
                _reset_connection()
                print("Anvil uplink disconnected; attempting to reconnect in 10 seconds.")
                # Give ourselves a chance to reconnect
                time.sleep(10)
                print("Reconnecting...")
