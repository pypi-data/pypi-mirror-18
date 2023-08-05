# Quark 1.0.452 run at 2016-11-10 20:29:10.299603
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.spi_api_tracing")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark.error
import quark
import quark.concurrent



def quote(str):
    if (((str).find(u"\\")) >= (0)):
        str = (u"\\\\").join((str).split(u"\\"))

    if (((str).find(u"\n")) >= (0)):
        str = (u"\\n").join((str).split(u"\n"))

    if (((str).find(u"\"")) >= (0)):
        str = (u"\\\"").join((str).split(u"\""))

    return ((u"\"") + (str)) + (u"\"")


def quote_error(error):
    return ((((quark.reflect.Class.get(_getClass(error))).getName()) + (u"(")) + (quote((error).getMessage()))) + (u")")

class Identificator(_QObject):
    def _init(self):
        self.lock = _Lock()
        self.seq = 0

    def __init__(self): self._init()

    def next(self, basename):
        (self.lock).acquire();
        n = self.seq;
        self.seq = (self.seq) + (1)
        (self.lock).release();
        return ((basename) + (u"$")) + (_toString(n))

    def _getClass(self):
        return u"quark.spi_api_tracing.Identificator"

    def _getField(self, name):
        if ((name) == (u"lock")):
            return (self).lock

        if ((name) == (u"seq")):
            return (self).seq

        return None

    def _setField(self, name, value):
        if ((name) == (u"lock")):
            (self).lock = _cast(value, lambda: _Lock)

        if ((name) == (u"seq")):
            (self).seq = _cast(value, lambda: int)


Identificator.quark_spi_api_tracing_Identificator_ref = None
class Identifiable(_QObject):
    def _init(self):
        self.id = None
        self.log = None

    def __init__(self, log, basename):
        self._init()
        (self).id = (Identifiable.namer).next(basename)
        (self).log = log

    def _getClass(self):
        return u"quark.spi_api_tracing.Identifiable"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value


Identifiable.namer = Identificator()
Identifiable.quark_spi_api_tracing_Identifiable_ref = None
class ServletProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.servlet_impl = None
        self.real_runtime = None

    def __init__(self, log, basename, real_runtime, servlet_impl):
        super(ServletProxy, self).__init__(log, basename);
        (self).real_runtime = real_runtime
        (self).servlet_impl = servlet_impl

    def onServletInit(self, url, runtime):
        ((self).log).debug(((((((self).id) + (u".onServletInit(")) + (quote(url))) + (u", ")) + ((self.real_runtime).id)) + (u")"));
        (self.servlet_impl).onServletInit(url, self.real_runtime);

    def onServletError(self, url, error):
        ((self).log).debug(((((((self).id) + (u".onServletError(")) + (quote(url))) + (u", ")) + (quote_error(error))) + (u")"));
        (self.servlet_impl).onServletError(url, error);

    def onServletEnd(self, url):
        ((self).log).debug(((((self).id) + (u".onServletEnd(")) + (quote(url))) + (u")"));
        (self.servlet_impl).onServletEnd(url);

    def _getClass(self):
        return u"quark.spi_api_tracing.ServletProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: RuntimeProxy)


ServletProxy.quark_spi_api_tracing_ServletProxy_ref = None
class HTTPRequestProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.request_impl = None

    def __init__(self, log, request_impl):
        super(HTTPRequestProxy, self).__init__(log, u"HTTPRequest");
        (self).request_impl = request_impl

    def getUrl(self):
        return (self.request_impl).getUrl()

    def setMethod(self, method):
        (self.request_impl).setMethod(method);

    def getMethod(self):
        return (self.request_impl).getMethod()

    def setBody(self, data):
        (self.request_impl).setBody(data);

    def getBody(self):
        return (self.request_impl).getBody()

    def setHeader(self, key, value):
        (self.request_impl).setHeader(key, value);

    def getHeader(self, key):
        return (self.request_impl).getHeader(key)

    def getHeaders(self):
        return (self.request_impl).getHeaders()

    def _getClass(self):
        return u"quark.spi_api_tracing.HTTPRequestProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"request_impl")):
            return (self).request_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"request_impl")):
            (self).request_impl = _cast(value, lambda: quark.HTTPRequest)


HTTPRequestProxy.quark_spi_api_tracing_HTTPRequestProxy_ref = None
class HTTPResponseProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.response_impl = None

    def __init__(self, log, response_impl):
        super(HTTPResponseProxy, self).__init__(log, u"HTTPResponse");
        (self).response_impl = response_impl

    def getCode(self):
        return (self.response_impl).getCode()

    def setCode(self, code):
        (self.response_impl).setCode(code);

    def setBody(self, data):
        (self.response_impl).setBody(data);

    def getBody(self):
        return (self.response_impl).getBody()

    def setHeader(self, key, value):
        (self.response_impl).setHeader(key, value);

    def getHeader(self, key):
        return (self.response_impl).getHeader(key)

    def getHeaders(self):
        return (self.response_impl).getHeaders()

    def _getClass(self):
        return u"quark.spi_api_tracing.HTTPResponseProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"response_impl")):
            return (self).response_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"response_impl")):
            (self).response_impl = _cast(value, lambda: quark.HTTPResponse)


HTTPResponseProxy.quark_spi_api_tracing_HTTPResponseProxy_ref = None
class HTTPServletProxy(ServletProxy):
    def _init(self):
        ServletProxy._init(self)
        self.http_servlet_impl = None

    def __init__(self, log, real_runtime, http_servlet_impl):
        super(HTTPServletProxy, self).__init__(log, u"HTTPServlet", real_runtime, http_servlet_impl);
        (self).http_servlet_impl = http_servlet_impl

    def onHTTPRequest(self, request, response):
        wrapped_request = HTTPRequestProxy((self).log, request);
        wrapped_response = HTTPResponseProxy((self).log, response);
        ((self).log).debug(((((((((((self).id) + (u".onHTTPRequest(")) + ((wrapped_request).id)) + (u" ")) + ((request).getMethod())) + (u" ")) + (quote((request).getUrl()))) + (u", ")) + ((wrapped_response).id)) + (u")"));
        (self.http_servlet_impl).onHTTPRequest(wrapped_request, wrapped_response);

    def _getClass(self):
        return u"quark.spi_api_tracing.HTTPServletProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        if ((name) == (u"http_servlet_impl")):
            return (self).http_servlet_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: RuntimeProxy)

        if ((name) == (u"http_servlet_impl")):
            (self).http_servlet_impl = _cast(value, lambda: quark.HTTPServlet)

    def serveHTTP(self, url):
        (quark.concurrent.Context.runtime()).serveHTTP(url, self);

HTTPServletProxy.quark_spi_api_tracing_HTTPServletProxy_ref = None
class WSServletProxy(ServletProxy):
    def _init(self):
        ServletProxy._init(self)
        self.ws_servlet_impl = None

    def __init__(self, log, real_runtime, ws_servlet_impl):
        super(WSServletProxy, self).__init__(log, u"WSServlet", real_runtime, ws_servlet_impl);
        (self).ws_servlet_impl = ws_servlet_impl

    def onWSConnect(self, request):
        wrapped_request = HTTPRequestProxy((self).log, request);
        ((self).log).debug(((((((((self).id) + (u".onWSConnect(")) + ((wrapped_request).id)) + (u" ")) + ((request).getMethod())) + (u" ")) + (quote((request).getUrl()))) + (u")..."));
        handler = (self.ws_servlet_impl).onWSConnect(wrapped_request);
        if ((handler) == (None)):
            ((self).log).debug(((((((self).id) + (u".onWSConnect(")) + ((wrapped_request).id)) + (u")")) + (u" -> ")) + (u"null"));
            return handler
        else:
            wrapped_handler = WSHandlerProxy((self).log, handler);
            ((self).log).debug(((((((self).id) + (u".onWSConnect(")) + ((wrapped_request).id)) + (u")")) + (u" -> ")) + ((wrapped_handler).id));
            return wrapped_handler

    def _getClass(self):
        return u"quark.spi_api_tracing.WSServletProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        if ((name) == (u"ws_servlet_impl")):
            return (self).ws_servlet_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: RuntimeProxy)

        if ((name) == (u"ws_servlet_impl")):
            (self).ws_servlet_impl = _cast(value, lambda: quark.WSServlet)

    def serveWS(self, url):
        (quark.concurrent.Context.runtime()).serveWS(url, self);

WSServletProxy.quark_spi_api_tracing_WSServletProxy_ref = None
class TaskProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.task_impl = None
        self.real_runtime = None

    def __init__(self, log, real_runtime, task_impl):
        super(TaskProxy, self).__init__(log, u"Task");
        (self).task_impl = task_impl
        (self).real_runtime = real_runtime

    def onExecute(self, runtime):
        ((self).log).debug(((((self).id) + (u".onExecute(")) + ((self.real_runtime).id)) + (u")"));
        (self.task_impl).onExecute(self.real_runtime);

    def _getClass(self):
        return u"quark.spi_api_tracing.TaskProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"task_impl")):
            return (self).task_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"task_impl")):
            (self).task_impl = _cast(value, lambda: quark.Task)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: RuntimeProxy)


TaskProxy.quark_spi_api_tracing_TaskProxy_ref = None
class WebSocketProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.socket_impl = None

    def __init__(self, log, socket_impl):
        super(WebSocketProxy, self).__init__(log, u"WebSocket");
        (self).socket_impl = socket_impl

    def send(self, message):
        ((self).log).debug(((((self).id) + (u".send(")) + (quote(message))) + (u")..."));
        ret = (self.socket_impl).send(message);
        ((self).log).debug((((((self).id) + (u".send(")) + (u")")) + (u" -> ")) + (_toString(ret).lower()));
        return ret

    def sendBinary(self, message):
        ((self).log).debug(((((self).id) + (u".sendBinary(")) + (((quark.concurrent.Context.runtime()).codec()).toHexdump(message, 0, (message).capacity(), 4))) + (u")..."));
        ret = (self.socket_impl).sendBinary(message);
        ((self).log).debug((((((self).id) + (u".sendBinary(")) + (u")")) + (u" -> ")) + (_toString(ret).lower()));
        return ret

    def close(self):
        ((self).log).debug((((self).id) + (u".close(")) + (u")..."));
        ret = (self.socket_impl).close();
        ((self).log).debug((((((self).id) + (u".close(")) + (u")")) + (u" -> ")) + (_toString(ret).lower()));
        return ret

    def _getClass(self):
        return u"quark.spi_api_tracing.WebSocketProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"socket_impl")):
            return (self).socket_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"socket_impl")):
            (self).socket_impl = _cast(value, lambda: quark.WebSocket)


WebSocketProxy.quark_spi_api_tracing_WebSocketProxy_ref = None
class WSHandlerProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.handler_impl = None
        self._wrapped_socket = None

    def __init__(self, log, handler_impl):
        super(WSHandlerProxy, self).__init__(log, u"WSHandler");
        (self).handler_impl = handler_impl
        (self)._wrapped_socket = _cast(None, lambda: WebSocketProxy)

    def _wrap_socket(self, socket):
        if ((self._wrapped_socket) == (None)):
            self._wrapped_socket = WebSocketProxy((self).log, socket)

        return self._wrapped_socket

    def onWSInit(self, socket):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((self).id) + (u".onWSInit(")) + ((wrapped_socket).id)) + (u")"));
        (self.handler_impl).onWSInit(wrapped_socket);

    def onWSConnected(self, socket):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((self).id) + (u".onWSConnected(")) + ((wrapped_socket).id)) + (u")"));
        (self.handler_impl).onWSConnected(wrapped_socket);

    def onWSMessage(self, socket, message):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((((self).id) + (u".onWSMessage(")) + ((wrapped_socket).id)) + (u", ")) + (quote(message))) + (u")"));
        (self.handler_impl).onWSMessage(wrapped_socket, message);

    def onWSBinary(self, socket, message):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((((self).id) + (u".onWSBinary(")) + ((wrapped_socket).id)) + (u", ")) + (((quark.concurrent.Context.runtime()).codec()).toHexdump(message, 0, (message).capacity(), 4))) + (u")"));
        (self.handler_impl).onWSBinary(wrapped_socket, message);

    def onWSClosed(self, socket):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((self).id) + (u".onWSClosed(")) + ((wrapped_socket).id)) + (u")"));
        (self.handler_impl).onWSClosed(wrapped_socket);

    def onWSError(self, socket, error):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((((self).id) + (u".onWSError(")) + ((wrapped_socket).id)) + (u", ")) + (quote_error(error))) + (u")"));
        (self.handler_impl).onWSError(wrapped_socket, error);

    def onWSFinal(self, socket):
        wrapped_socket = self._wrap_socket(socket);
        ((self).log).debug(((((self).id) + (u".onWSFinal(")) + ((wrapped_socket).id)) + (u")"));
        (self.handler_impl).onWSFinal(wrapped_socket);

    def _getClass(self):
        return u"quark.spi_api_tracing.WSHandlerProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"handler_impl")):
            return (self).handler_impl

        if ((name) == (u"_wrapped_socket")):
            return (self)._wrapped_socket

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"handler_impl")):
            (self).handler_impl = _cast(value, lambda: quark.WSHandler)

        if ((name) == (u"_wrapped_socket")):
            (self)._wrapped_socket = _cast(value, lambda: WebSocketProxy)


WSHandlerProxy.quark_spi_api_tracing_WSHandlerProxy_ref = None
class HTTPHandlerProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.handler_impl = None
        self.wrapped_request = None

    def __init__(self, log, wrapped_request, handler_impl):
        super(HTTPHandlerProxy, self).__init__(log, u"HTTPHandler");
        (self).wrapped_request = wrapped_request
        (self).handler_impl = handler_impl

    def onHTTPInit(self, request):
        ((self).log).debug(((((self).id) + (u".onHTTPInit(")) + ((self.wrapped_request).id)) + (u")"));
        ((self).handler_impl).onHTTPInit(request);

    def onHTTPResponse(self, request, response):
        ((self).log).debug(((((((((self).id) + (u".onHTTPResponse(")) + ((self.wrapped_request).id)) + (u", ")) + (_toString((response).getCode()))) + (u" ")) + (quote((response).getBody()))) + (u")"));
        ((self).handler_impl).onHTTPResponse(request, response);

    def onHTTPError(self, request, error):
        ((self).log).debug(((((((self).id) + (u".onHTTPError(")) + ((self.wrapped_request).id)) + (u", ")) + (quote_error(error))) + (u")"));
        ((self).handler_impl).onHTTPError(request, error);

    def onHTTPFinal(self, request):
        ((self).log).debug(((((self).id) + (u".onHTTPFinal(")) + ((self.wrapped_request).id)) + (u")"));
        ((self).handler_impl).onHTTPFinal(request);

    def _getClass(self):
        return u"quark.spi_api_tracing.HTTPHandlerProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"handler_impl")):
            return (self).handler_impl

        if ((name) == (u"wrapped_request")):
            return (self).wrapped_request

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"handler_impl")):
            (self).handler_impl = _cast(value, lambda: quark.HTTPHandler)

        if ((name) == (u"wrapped_request")):
            (self).wrapped_request = _cast(value, lambda: HTTPRequestProxy)


HTTPHandlerProxy.quark_spi_api_tracing_HTTPHandlerProxy_ref = None
class RuntimeProxy(Identifiable):
    def _init(self):
        Identifiable._init(self)
        self.impl = None

    def __init__(self, impl):
        super(RuntimeProxy, self).__init__((impl).logger(u"api"), u"Runtime");
        (self).impl = impl

    def open(self, url, handler):
        wrapped_handler = WSHandlerProxy((self).log, handler);
        ((self).log).debug(((((((self).id) + (u".open(")) + (quote(url))) + (u", ")) + ((wrapped_handler).id)) + (u")"));
        (self.impl).open(url, wrapped_handler);

    def request(self, request, handler):
        wrapped_request = HTTPRequestProxy((self).log, request);
        wrapped_handler = HTTPHandlerProxy((self).log, wrapped_request, handler);
        ((self).log).debug(((((((((((self).id) + (u".request(")) + ((wrapped_request).id)) + (u" ")) + ((request).getMethod())) + (u" ")) + (quote((request).getUrl()))) + (u", ")) + ((wrapped_handler).id)) + (u")"));
        (self.impl).request(request, wrapped_handler);

    def schedule(self, handler, delayInSeconds):
        wrapped_handler = TaskProxy((self).log, self, handler);
        ((self).log).debug(((((((self).id) + (u".schedule(")) + ((wrapped_handler).id)) + (u", ")) + (repr(delayInSeconds))) + (u")"));
        (self.impl).schedule(wrapped_handler, delayInSeconds);

    def codec(self):
        ((self).log).debug(((self).id) + (u".codec()"));
        return (self.impl).codec()

    def now(self):
        ((self).log).debug(((self).id) + (u".now()"));
        return (self.impl).now()

    def sleep(self, seconds):
        ((self).log).debug(((((self).id) + (u".sleep(")) + (repr(seconds))) + (u")"));
        (self.impl).sleep(seconds);

    def uuid(self):
        ((self).log).debug(((self).id) + (u".uuid()"));
        return (self.impl).uuid()

    def callSafely(self, callee, defaultResult):
        ((self).log).debug(((((((self).id) + (u".callSafely(")) + (_toString(callee))) + (u", ")) + (_toString(defaultResult))) + (u")"));
        return (self.impl).callSafely(callee, defaultResult)

    def serveHTTP(self, url, servlet):
        wrapped_servlet = HTTPServletProxy((self).log, self, servlet);
        ((self).log).debug(((((((self).id) + (u".serveHTTP(")) + (quote(url))) + (u", ")) + ((wrapped_servlet).id)) + (u")"));
        (self.impl).serveHTTP(url, wrapped_servlet);

    def serveWS(self, url, servlet):
        wrapped_servlet = WSServletProxy((self).log, self, servlet);
        ((self).log).debug(((((((self).id) + (u".serveWS(")) + (quote(url))) + (u", ")) + ((wrapped_servlet).id)) + (u")"));
        (self.impl).serveWS(url, wrapped_servlet);

    def respond(self, request, response):
        wrapped_request = _cast(request, lambda: HTTPRequestProxy);
        wrapped_response = _cast(response, lambda: HTTPResponseProxy);
        ((self).log).debug(((((((((((self).id) + (u".respond(")) + ((wrapped_request).id)) + (u", ")) + ((wrapped_response).id)) + (u" ")) + (_toString((wrapped_response).getCode()))) + (u" ")) + ((wrapped_response).getBody())) + (u")"));
        (self.impl).respond((wrapped_request).request_impl, (wrapped_response).response_impl);

    def fail(self, message):
        ((self).log).info(((((self).id) + (u".fail(")) + (quote(message))) + (u")"));
        (self.impl).fail(message);

    def logger(self, topic):
        return (self.impl).logger(topic)

    def _getClass(self):
        return u"quark.spi_api_tracing.RuntimeProxy"

    def _getField(self, name):
        if ((name) == (u"namer")):
            return Identifiable.namer

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"log")):
            return (self).log

        if ((name) == (u"impl")):
            return (self).impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"namer")):
            Identifiable.namer = _cast(value, lambda: Identificator)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"log")):
            (self).log = value

        if ((name) == (u"impl")):
            (self).impl = _cast(value, lambda: quark.Runtime)


RuntimeProxy.quark_spi_api_tracing_RuntimeProxy_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.spi_api_tracing")
