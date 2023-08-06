# Quark 1.0.452 run at 2016-11-17 17:07:48.071308
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_protocol")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent
import mdk_runtime.actors
import mdk_runtime
import quark.error



def contains(values, value):
    """
    Returns whether a list contains a given value.
    """
    idx = 0;
    while ((idx) < (len(values))):
        if ((value) == ((values)[idx])):
            return True

        idx = (idx) + (1)

    return False

class Serializable(_QObject):
    """
    JSON serializable object.

    If it has have a String field called _json_type, that will be set as the
    'type' field in serialized JSON.

    """
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def decodeClassName(name, encoded):
        """
        Decode JSON into a particular class. XXX TURN INTO FUNCTION
        """
        json = _JSONObject.parse(encoded);
        clazz = quark.reflect.Class.get(name);
        obj = _cast((clazz).construct(_List([])), lambda: Serializable);
        if ((obj) == (None)):
            raise Exception((((u"could not construct ") + ((clazz).getName())) + (u" from this json: ")) + (encoded));

        quark.fromJSON(clazz, obj, json);
        return obj

    def encode(self):
        clazz = quark.reflect.Class.get(_getClass(self));
        json = quark.toJSON(self, clazz);
        jsonType = _cast((self)._getField(u"_json_type"), lambda: unicode);
        if ((jsonType) != (None)):
            (json).setObjectItem((u"type"), ((_JSONObject()).setString(jsonType)));

        encoded = (json).toString();
        return encoded

    def _getClass(self):
        return u"mdk_protocol.Serializable"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
Serializable.mdk_protocol_Serializable_ref = None
class LamportClock(Serializable):
    """
    A Lamport Clock is a logical structure meant to allow partial causal ordering. Ours is a list of
    integers such that adding an integer implies adding a new level to the causality tree.

    Within a level, time is indicated by incrementing the clock, so

    [1,2,3] comes before [1,2,4] which comes before [1,2,5]

    Adding an element to the clock implies causality, so [1,2,4,1-N] is _by definition_ a sequence that was
    _caused by_ the sequence of [1,2,1-3].

    Note that LamportClock is lowish-level support. SharedContext puts some more structure around this, too.

    """
    def _init(self):
        Serializable._init(self)
        self._mutex = _Lock()
        self.clocks = _List([])

    def __init__(self):
        super(LamportClock, self).__init__();

    @staticmethod
    def decode(encoded):
        return _cast(Serializable.decodeClassName(u"mdk_protocol.LamportClock", encoded), lambda: LamportClock)

    def key(self):
        """
        Return a neatly-formatted list of all of our clock elements (e.g. 1,2,4,1) for use as a name or
        a key.

        """
        (self._mutex).acquire();
        tmp = _List([]);
        i = 0;
        while ((i) < (len((self).clocks))):
            (tmp).append(_toString(((self).clocks)[i]));
            i = (i) + (1)

        str = (u",").join(tmp);
        (self._mutex).release();
        return str

    def toString(self):
        (self._mutex).acquire();
        str = ((u"<LamportClock ") + ((self).key())) + (u">");
        (self._mutex).release();
        return str

    def enter(self):
        """
        Enter a new level of causality. Returns the value to pass to later pass to leave to get back to the
        current level of causality.

        """
        (self._mutex).acquire();
        current = -(1);
        ((self).clocks).append(0);
        current = len((self).clocks)
        (self._mutex).release();
        return current

    def leave(self, popTo):
        """
        Leave deeper levels of causality. popTo should be the value returned when you enter()d this level.

        """
        (self._mutex).acquire();
        current = -(1);
        (self).clocks = (quark.ListUtil()).slice((self).clocks, 0, popTo)
        current = len((self).clocks)
        (self._mutex).release();
        return current

    def tick(self):
        """
        Increment the clock for our current level of causality (which is always the last element in the list).
        If there are no elements in our clock, do nothing.

        """
        (self._mutex).acquire();
        current = len((self).clocks);
        if ((current) > (0)):
            ((self).clocks)[(current) - (1)] = ((((self).clocks)[(current) - (1)]) + (1));

        (self._mutex).release();

    def _getClass(self):
        return u"mdk_protocol.LamportClock"

    def _getField(self, name):
        if ((name) == (u"_mutex")):
            return (self)._mutex

        if ((name) == (u"clocks")):
            return (self).clocks

        return None

    def _setField(self, name, value):
        if ((name) == (u"_mutex")):
            (self)._mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"clocks")):
            (self).clocks = _cast(value, lambda: _List)


LamportClock.mdk_protocol_LamportClock_ref = None
class OperationalEnvironment(Serializable):
    """
    An isolated environment with a name, and optionally a fallback environment.

    By default the environment will be 'sandbox'.

    """
    def _init(self):
        Serializable._init(self)
        self.name = u"sandbox"
        self.fallbackName = None

    def __init__(self):
        super(OperationalEnvironment, self).__init__();

    def getFallback(self):
        """
        Return the fallback Environment, or null if there isn't one.
        """
        if (((self).fallbackName) == (None)):
            return _cast(None, lambda: OperationalEnvironment)

        result = OperationalEnvironment();
        (result).name = (self).fallbackName
        (result).fallbackName = _cast(None, lambda: unicode)
        return result

    def _getClass(self):
        return u"mdk_protocol.OperationalEnvironment"

    def _getField(self, name):
        if ((name) == (u"name")):
            return (self).name

        if ((name) == (u"fallbackName")):
            return (self).fallbackName

        return None

    def _setField(self, name, value):
        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)

        if ((name) == (u"fallbackName")):
            (self).fallbackName = _cast(value, lambda: unicode)


OperationalEnvironment.mdk_protocol_OperationalEnvironment_ref = None
class SharedContext(Serializable):
    def _init(self):
        Serializable._init(self)
        self.traceId = (quark.concurrent.Context.runtime()).uuid()
        self.clock = LamportClock()
        self.properties = {}
        self.environment = OperationalEnvironment()
        self._lastEntry = 0

    def __init__(self):
        super(SharedContext, self).__init__();
        (self)._lastEntry = ((self).clock).enter()

    def withTraceId(self, traceId):
        """
        Set the traceId for this SharedContext.
        """
        (self).traceId = traceId
        return self

    @staticmethod
    def decode(encoded):
        return _cast(Serializable.decodeClassName(u"mdk_protocol.SharedContext", encoded), lambda: SharedContext)

    def clockStr(self, pfx):
        cs = u"";
        if (((self).clock) != (None)):
            cs = (pfx) + (((self).clock).key())

        return cs

    def key(self):
        return ((self).traceId) + ((self).clockStr(u":"))

    def toString(self):
        return (((u"<SCTX t:") + ((self).traceId)) + ((self).clockStr(u" c:"))) + (u">")

    def tick(self):
        """
        Tick the clock at our current causality level.

        """
        ((self).clock).tick();

    def start_span(self):
        """
        Return a SharedContext one level deeper in causality.

        NOTE WELL: THIS RETURNS A NEW SharedContext RATHER THAN MODIFYING THIS ONE. It is NOT SUPPORTED
        to modify the causality level of a SharedContext in place.

        """
        (self).tick();
        newContext = SharedContext.decode((self).encode());
        (newContext)._lastEntry = ((newContext).clock).enter()
        return newContext

    def finish_span(self):
        """
        Return a SharedContext one level higher in causality. In practice, most callers should probably stop
        using this context, and the new one, after calling this method.

        NOTE WELL: THIS RETURNS A NEW SharedContext RATHER THAN MODIFYING THIS ONE. It is NOT SUPPORTED
        to modify the causality level of a SharedContext in place.

        """
        newContext = SharedContext.decode((self).encode());
        (newContext)._lastEntry = ((newContext).clock).leave((newContext)._lastEntry)
        return newContext

    def copy(self):
        """
        Return a copy of a SharedContext.
        """
        return SharedContext.decode((self).encode())

    def _getClass(self):
        return u"mdk_protocol.SharedContext"

    def _getField(self, name):
        if ((name) == (u"traceId")):
            return (self).traceId

        if ((name) == (u"clock")):
            return (self).clock

        if ((name) == (u"properties")):
            return (self).properties

        if ((name) == (u"environment")):
            return (self).environment

        if ((name) == (u"_lastEntry")):
            return (self)._lastEntry

        return None

    def _setField(self, name, value):
        if ((name) == (u"traceId")):
            (self).traceId = _cast(value, lambda: unicode)

        if ((name) == (u"clock")):
            (self).clock = _cast(value, lambda: LamportClock)

        if ((name) == (u"properties")):
            (self).properties = _cast(value, lambda: _Map)

        if ((name) == (u"environment")):
            (self).environment = _cast(value, lambda: OperationalEnvironment)

        if ((name) == (u"_lastEntry")):
            (self)._lastEntry = _cast(value, lambda: int)


SharedContext.mdk_protocol_SharedContext_ref = None
class Open(Serializable):
    """
    A message sent whenever a new connection is opened, by both sides.
    """
    def _init(self):
        Serializable._init(self)
        self.version = u"2.0.0"
        self.properties = {}
        self.nodeId = None
        self.environment = OperationalEnvironment()

    def __init__(self):
        super(Open, self).__init__();

    def _getClass(self):
        return u"mdk_protocol.Open"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Open._json_type

        if ((name) == (u"version")):
            return (self).version

        if ((name) == (u"properties")):
            return (self).properties

        if ((name) == (u"nodeId")):
            return (self).nodeId

        if ((name) == (u"environment")):
            return (self).environment

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Open._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"version")):
            (self).version = _cast(value, lambda: unicode)

        if ((name) == (u"properties")):
            (self).properties = _cast(value, lambda: _Map)

        if ((name) == (u"nodeId")):
            (self).nodeId = _cast(value, lambda: unicode)

        if ((name) == (u"environment")):
            (self).environment = _cast(value, lambda: OperationalEnvironment)


Open._json_type = u"open"
Open.mdk_protocol_Open_ref = None
class ProtocolError(_QObject):
    """
    A value class for sending error informationto a remote peer.
    """
    def _init(self):
        self.code = None
        self.title = None
        self.detail = None
        self.id = None

    def __init__(self): self._init()

    def toString(self):
        return (((((((u"ID:") + (self.id)) + (u" code:")) + (self.code)) + (u" ")) + (self.title)) + (u"\n")) + (self.detail)

    def _getClass(self):
        return u"mdk_protocol.ProtocolError"

    def _getField(self, name):
        if ((name) == (u"code")):
            return (self).code

        if ((name) == (u"title")):
            return (self).title

        if ((name) == (u"detail")):
            return (self).detail

        if ((name) == (u"id")):
            return (self).id

        return None

    def _setField(self, name, value):
        if ((name) == (u"code")):
            (self).code = _cast(value, lambda: unicode)

        if ((name) == (u"title")):
            (self).title = _cast(value, lambda: unicode)

        if ((name) == (u"detail")):
            (self).detail = _cast(value, lambda: unicode)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)


ProtocolError.mdk_protocol_ProtocolError_ref = None
class Close(Serializable):
    """
    Close the event stream.
    """
    def _init(self):
        Serializable._init(self)
        self.error = None

    def __init__(self):
        super(Close, self).__init__();

    def _getClass(self):
        return u"mdk_protocol.Close"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Close._json_type

        if ((name) == (u"error")):
            return (self).error

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Close._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"error")):
            (self).error = _cast(value, lambda: ProtocolError)


Close._json_type = u"close"
Close.mdk_protocol_Close_ref = None
class Pump(_QObject):
    """
    Sent to a subscriber every once in a while, to tell subscribers they can send data.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def _getClass(self):
        return u"mdk_protocol.Pump"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
Pump.mdk_protocol_Pump_ref = None
class WSConnected(_QObject):
    """
    Sent to a subscriber when connection happens.
    """
    def _init(self):
        self.websock = None

    def __init__(self, websock):
        self._init()
        (self).websock = websock

    def _getClass(self):
        return u"mdk_protocol.WSConnected"

    def _getField(self, name):
        if ((name) == (u"websock")):
            return (self).websock

        return None

    def _setField(self, name, value):
        if ((name) == (u"websock")):
            (self).websock = _cast(value, lambda: mdk_runtime.actors.Actor)


WSConnected.mdk_protocol_WSConnected_ref = None
class DecodedMessage(_QObject):
    """
    Sent to a subscriber when a message is received.
    """
    def _init(self):
        self.message = None

    def __init__(self, message):
        self._init()
        (self).message = message

    def _getClass(self):
        return u"mdk_protocol.DecodedMessage"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = value


DecodedMessage.mdk_protocol_DecodedMessage_ref = None
class WSClientSubscriber(object):
    """
    Higher-level interface for subscribers, to be utilized with _subscriberDispatch.
    """

    def onMessageFromServer(self, message):
        """
        Handle an incoming decoded JSON message received from the server.
        """
        raise NotImplementedError('`WSClientSubscriber.onMessageFromServer` is an abstract method')

    def onWSConnected(self, websocket):
        """
        Called with WebSocket actor when the WSClient connects to the server.
        """
        raise NotImplementedError('`WSClientSubscriber.onWSConnected` is an abstract method')

    def onPump(self):
        """
        Called when the WSClient notifies the subscriber it can send data.
        """
        raise NotImplementedError('`WSClientSubscriber.onPump` is an abstract method')

WSClientSubscriber.mdk_protocol_WSClientSubscriber_ref = None

def _subscriberDispatch(subscriber, message):
    """
    Dispatch actor messages to a WSClientSubscriber.

    Call this in onMessage to handle DecodedMessage, WSConnected and Pump messages
    from the WSClient.

    """
    klass = (quark.reflect.Class.get(_getClass(message))).id;
    if ((klass) == (u"mdk_protocol.WSConnected")):
        connected = _cast(message, lambda: WSConnected);
        (subscriber).onWSConnected((connected).websock);
        return

    if ((klass) == (u"mdk_protocol.Pump")):
        (subscriber).onPump();
        return

    if ((klass) == (u"mdk_protocol.DecodedMessage")):
        decoded = _cast(message, lambda: DecodedMessage);
        (subscriber).onMessageFromServer((decoded).message);
        return


class OpenCloseSubscriber(_QObject):
    """
    Handle Open and Close messages.
    """
    def _init(self):
        self._dispatcher = None
        self._wsclient = None
        self._node_id = None
        self._environment = None

    def __init__(self, client, node_id, environment):
        self._init()
        (self)._wsclient = client
        (self)._node_id = node_id
        (self)._environment = environment
        ((self)._wsclient).subscribe(self);

    def onStart(self, dispatcher):
        (self)._dispatcher = dispatcher

    def onMessage(self, origin, message):
        _subscriberDispatch(self, message);

    def onStop(self):
        pass

    def onMessageFromServer(self, message):
        type = (quark.reflect.Class.get(_getClass(message))).id;
        if ((type) == (u"mdk_protocol.Open")):
            (self).onOpen();
            return

        if ((type) == (u"mdk_protocol.Close")):
            close = _cast(message, lambda: Close);
            (self).onClose(close);
            return

    def onWSConnected(self, websocket):
        open = Open();
        (open).nodeId = (self)._node_id
        (open).environment = self._environment
        ((self)._dispatcher).tell(self, (open).encode(), websocket);

    def onPump(self):
        pass

    def onOpen(self):
        pass

    def onClose(self, close):
        ((self)._wsclient).onClose((close).error);

    def _getClass(self):
        return u"mdk_protocol.OpenCloseSubscriber"

    def _getField(self, name):
        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        if ((name) == (u"_wsclient")):
            return (self)._wsclient

        if ((name) == (u"_node_id")):
            return (self)._node_id

        if ((name) == (u"_environment")):
            return (self)._environment

        return None

    def _setField(self, name, value):
        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_wsclient")):
            (self)._wsclient = _cast(value, lambda: WSClient)

        if ((name) == (u"_node_id")):
            (self)._node_id = _cast(value, lambda: unicode)

        if ((name) == (u"_environment")):
            (self)._environment = _cast(value, lambda: OperationalEnvironment)


OpenCloseSubscriber.mdk_protocol_OpenCloseSubscriber_ref = None
class JSONParser(_QObject):
    """
    Convert JSON-encoded strings into objects.
    """
    def _init(self):
        self._typeToClass = {}

    def __init__(self): self._init()

    def register(self, type, cls):
        """
        Register a type field and the corresponding class.
        """
        ((self)._typeToClass)[type] = (cls);

    def decode(self, message):
        """
        Decode a String into an Object.
        """
        json = _JSONObject.parse(message);
        cls = ((self)._typeToClass).get(((json).getObjectItem(u"type")).getString());
        if ((cls) == (None)):
            return None

        instance = (cls).construct(_List([]));
        quark.fromJSON(cls, instance, json);
        return instance

    def _getClass(self):
        return u"mdk_protocol.JSONParser"

    def _getField(self, name):
        if ((name) == (u"_typeToClass")):
            return (self)._typeToClass

        return None

    def _setField(self, name, value):
        if ((name) == (u"_typeToClass")):
            (self)._typeToClass = _cast(value, lambda: _Map)


JSONParser.mdk_protocol_JSONParser_ref = None
class WSClient(_QObject):
    """
    Common protocol machinery for web socket based protocol clients.
    """
    def _init(self):
        self.logger = quark._getLogger(u"protocol")
        self.firstDelay = 1.0
        self.maxDelay = 16.0
        self.reconnectDelay = self.firstDelay
        self.ttl = 30.0
        self.tick = 1.0
        self.sock = None
        self.lastConnectAttempt = 0
        self.timeService = None
        self.schedulingActor = None
        self.websockets = None
        self.dispatcher = None
        self.url = None
        self.token = None
        self.subscribers = _List([])
        self._started = False
        self._parser = None

    def __init__(self, runtime, parser, url, token):
        self._init()
        (self).dispatcher = (runtime).dispatcher
        (self).timeService = (runtime).getTimeService()
        (self).schedulingActor = (runtime).getScheduleService()
        (self).websockets = (runtime).getWebSocketsService()
        (self).url = url
        (self).token = token
        (self)._parser = parser

    def subscribe(self, subscriber):
        """
        Subscribe to messages from the server.

        Do this before starting the WSClient.

        The given Actor subscribes to WSConnected, all WSMessage received by the
        WSClient, as well as a periodic Pump message.

        """
        ((self).subscribers).append(subscriber);

    def isStarted(self):
        return self._started

    def isConnected(self):
        return (self.sock) != (None)

    def schedule(self, time):
        ((self).dispatcher).tell(self, mdk_runtime.Schedule(u"wakeup", time), (self).schedulingActor);

    def scheduleReconnect(self):
        self.schedule(self.reconnectDelay);

    def onClose(self, error):
        """
        Called when the connection is closed via message by the server.
        """
        if ((error) != (None)):
            (self.logger).error((u"Server closing connection due to error: ") + ((error).toString()));

    def doBackoff(self):
        self.reconnectDelay = (2.0) * (self.reconnectDelay)
        if ((self.reconnectDelay) > (self.maxDelay)):
            self.reconnectDelay = self.maxDelay

        (self.logger).info(((u"backing off, reconnecting in ") + (repr(self.reconnectDelay))) + (u" seconds"));

    def onStart(self, dispatcher):
        (self)._started = True
        self.schedule(0.0);

    def onStop(self):
        (self)._started = False
        if (self.isConnected()):
            ((self).dispatcher).tell(self, mdk_runtime.WSClose(), self.sock);
            self.sock = _cast(None, lambda: mdk_runtime.WSActor)

    def onMessage(self, origin, message):
        typeId = (quark.reflect.Class.get(_getClass(message))).id;
        if ((typeId) == (u"mdk_runtime.Happening")):
            (self).onScheduledEvent();
            return

        if ((typeId) == (u"mdk_runtime.WSClosed")):
            (self).onWSClosed();
            return

        if ((typeId) == (u"mdk_runtime.WSMessage")):
            wsmessage = _cast(message, lambda: mdk_runtime.WSMessage);
            parsed = ((self)._parser).decode((wsmessage).body);
            if ((parsed) == (None)):
                return

            decoded = DecodedMessage(parsed);
            idx = 0;
            while ((idx) < (len((self).subscribers))):
                ((self).dispatcher).tell(self, decoded, ((self).subscribers)[idx]);
                idx = (idx) + (1)

            return

    def onScheduledEvent(self):
        rightNow = int(round((((self).timeService).time()) * (1000.0)));
        reconnectInterval = int(round((self.reconnectDelay) * (1000.0)));
        if (self.isConnected()):
            if (self.isStarted()):
                self.pump();

        else:
            if ((self.isStarted()) and (((rightNow) - (self.lastConnectAttempt)) >= (reconnectInterval))):
                self.doOpen();

        if (self.isStarted()):
            self.schedule(self.tick);

    def doOpen(self):
        self.lastConnectAttempt = int(round((((self).timeService).time()) * (1000.0)))
        sockUrl = self.url;
        if ((self.token) != (None)):
            sockUrl = ((sockUrl) + (u"?token=")) + (self.token)

        (self.logger).info((u"opening ") + (self.url));
        (((self).websockets).connect(sockUrl, self)).andEither(quark._BoundMethod(self, u"onWSConnected", _List([])), quark._BoundMethod(self, u"onWSError", _List([])));

    def startup(self):
        message = WSConnected((self).sock);
        idx = 0;
        while ((idx) < (len(self.subscribers))):
            ((self).dispatcher).tell(self, message, (self.subscribers)[idx]);
            idx = (idx) + (1)

    def pump(self):
        message = Pump();
        idx = 0;
        while ((idx) < (len(self.subscribers))):
            ((self).dispatcher).tell(self, message, (self.subscribers)[idx]);
            idx = (idx) + (1)

    def onWSConnected(self, socket):
        (self.logger).info((((u"connected to ") + (self.url)) + (u" via ")) + (_toString(socket)));
        self.reconnectDelay = self.firstDelay
        self.sock = socket
        self.startup();
        self.pump();

    def onWSError(self, error):
        (self.logger).error((u"onWSError in protocol! ") + ((error).toString()));
        self.doBackoff();

    def onWSClosed(self):
        (self.logger).info((u"closed ") + (self.url));
        self.sock = _cast(None, lambda: mdk_runtime.WSActor)

    def _getClass(self):
        return u"mdk_protocol.WSClient"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"firstDelay")):
            return (self).firstDelay

        if ((name) == (u"maxDelay")):
            return (self).maxDelay

        if ((name) == (u"reconnectDelay")):
            return (self).reconnectDelay

        if ((name) == (u"ttl")):
            return (self).ttl

        if ((name) == (u"tick")):
            return (self).tick

        if ((name) == (u"sock")):
            return (self).sock

        if ((name) == (u"lastConnectAttempt")):
            return (self).lastConnectAttempt

        if ((name) == (u"timeService")):
            return (self).timeService

        if ((name) == (u"schedulingActor")):
            return (self).schedulingActor

        if ((name) == (u"websockets")):
            return (self).websockets

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"token")):
            return (self).token

        if ((name) == (u"subscribers")):
            return (self).subscribers

        if ((name) == (u"_started")):
            return (self)._started

        if ((name) == (u"_parser")):
            return (self)._parser

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"firstDelay")):
            (self).firstDelay = _cast(value, lambda: float)

        if ((name) == (u"maxDelay")):
            (self).maxDelay = _cast(value, lambda: float)

        if ((name) == (u"reconnectDelay")):
            (self).reconnectDelay = _cast(value, lambda: float)

        if ((name) == (u"ttl")):
            (self).ttl = _cast(value, lambda: float)

        if ((name) == (u"tick")):
            (self).tick = _cast(value, lambda: float)

        if ((name) == (u"sock")):
            (self).sock = _cast(value, lambda: mdk_runtime.WSActor)

        if ((name) == (u"lastConnectAttempt")):
            (self).lastConnectAttempt = _cast(value, lambda: int)

        if ((name) == (u"timeService")):
            (self).timeService = _cast(value, lambda: mdk_runtime.Time)

        if ((name) == (u"schedulingActor")):
            (self).schedulingActor = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"websockets")):
            (self).websockets = _cast(value, lambda: mdk_runtime.WebSockets)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"token")):
            (self).token = _cast(value, lambda: unicode)

        if ((name) == (u"subscribers")):
            (self).subscribers = _cast(value, lambda: _List)

        if ((name) == (u"_started")):
            (self)._started = _cast(value, lambda: bool)

        if ((name) == (u"_parser")):
            (self)._parser = _cast(value, lambda: JSONParser)


WSClient.quark_List_mdk_runtime_actors_Actor__ref = None
WSClient.mdk_protocol_WSClient_ref = None
class AckablePayload(object):
    """
    The payload for an ackable event.
    """

    def getTimestamp(self):
        """
        When did this happen? Milliseconds since Unix epoch.
        """
        raise NotImplementedError('`AckablePayload.getTimestamp` is an abstract method')

AckablePayload.mdk_protocol_AckablePayload_ref = None
class AckableEvent(_QObject):
    """
    An event that can be acknowledged.
    """
    def _init(self):
        self.json_type = None
        self.sequence = None
        self.sync = 1
        self.payload = None

    def __init__(self, json_type, payload, sequence):
        self._init()
        (self).json_type = json_type
        (self).payload = payload
        (self).sequence = sequence

    def getTimestamp(self):
        return (self.payload).getTimestamp()

    def encode(self):
        clazz = quark.reflect.Class.get(_getClass((self).payload));
        json = quark.toJSON((self).payload, clazz);
        (json).setObjectItem((u"type"), ((_JSONObject()).setString((self).json_type)));
        (json).setObjectItem((u"sequence"), ((_JSONObject()).setNumber((self).sequence)));
        (json).setObjectItem((u"sync"), ((_JSONObject()).setNumber((self).sync)));
        encoded = (json).toString();
        return encoded

    def _getClass(self):
        return u"mdk_protocol.AckableEvent"

    def _getField(self, name):
        if ((name) == (u"json_type")):
            return (self).json_type

        if ((name) == (u"sequence")):
            return (self).sequence

        if ((name) == (u"sync")):
            return (self).sync

        if ((name) == (u"payload")):
            return (self).payload

        return None

    def _setField(self, name, value):
        if ((name) == (u"json_type")):
            (self).json_type = _cast(value, lambda: unicode)

        if ((name) == (u"sequence")):
            (self).sequence = _cast(value, lambda: int)

        if ((name) == (u"sync")):
            (self).sync = _cast(value, lambda: int)

        if ((name) == (u"payload")):
            (self).payload = _cast(value, lambda: AckablePayload)


AckableEvent.mdk_protocol_AckableEvent_ref = None
class SendAckableEvent(object):
    """
    Send a message to the other side.
    """

    def send(self, event):
        raise NotImplementedError('`SendAckableEvent.send` is an abstract method')

SendAckableEvent.mdk_protocol_SendAckableEvent_ref = None
class WSSend(_QObject):
    """
    Send using a WebSocket actor.
    """
    def _init(self):
        self.origin = None
        self.dispatcher = None
        self.sock = None

    def __init__(self, origin, dispatcher, sock):
        self._init()
        (self).origin = origin
        (self).dispatcher = dispatcher
        (self).sock = sock

    def send(self, event):
        (self.dispatcher).tell(self.origin, (event).encode(), self.sock);

    def toString(self):
        return _toString((self).sock)

    def _getClass(self):
        return u"mdk_protocol.WSSend"

    def _getField(self, name):
        if ((name) == (u"origin")):
            return (self).origin

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"sock")):
            return (self).sock

        return None

    def _setField(self, name, value):
        if ((name) == (u"origin")):
            (self).origin = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"sock")):
            (self).sock = _cast(value, lambda: mdk_runtime.actors.Actor)


WSSend.mdk_protocol_WSSend_ref = None
class SendWithAcks(_QObject):
    """
    Utility class for sending messages with a protocol that sends back acks.

    """
    def _init(self):
        self._buffered = {}
        self._inFlight = {}
        self._added = 0
        self._sent = 0
        self._recorded = 0
        self._myLog = quark._getLogger(u"SendWithAcks")

    def __init__(self): self._init()

    def _debug(self, message):
        s = ((((u"[") + (_toString(len(_List(list((self._buffered).keys())))))) + (u" buf, ")) + (_toString(len(_List(list((self._inFlight).keys())))))) + (u" inf] ");
        (self._myLog).debug((s) + (message));

    def onConnected(self, sender):
        """
        Call when (re)connected to other side.
        """
        (self._buffered).update(self._inFlight);
        self._inFlight = {}
        self.onPump(sender);

    def onPump(self, sender):
        """
        Call to send buffered messages.
        """
        seqs = _List(list((self._buffered).keys()));
        (seqs).sort();
        idx = 0;
        while ((len(seqs)) > (idx)):
            evt = _map_remove((self._buffered), ((seqs)[idx]));
            (self._inFlight)[(evt).sequence] = (evt);
            (sender).send(evt);
            idx = (idx) + (1)

    def onAck(self, sequence):
        """
        Called when receiving acknowledgement from other side.
        """
        _map_remove((self._inFlight), (sequence));
        self._recorded = (self._recorded) + ((1))
        self._debug((((u"ack #") + (_toString(sequence))) + (u", discarding #")) + (_toString(sequence)));

    def send(self, json_type, event):
        """
        Send an event.
        """
        wrapper = AckableEvent(json_type, event, self._added);
        self._added = (self._added) + ((1))
        (self._buffered)[(wrapper).sequence] = (wrapper);
        self._debug((u"logged #") + (_toString((wrapper).sequence)));

    def _getClass(self):
        return u"mdk_protocol.SendWithAcks"

    def _getField(self, name):
        if ((name) == (u"_buffered")):
            return (self)._buffered

        if ((name) == (u"_inFlight")):
            return (self)._inFlight

        if ((name) == (u"_added")):
            return (self)._added

        if ((name) == (u"_sent")):
            return (self)._sent

        if ((name) == (u"_recorded")):
            return (self)._recorded

        if ((name) == (u"_myLog")):
            return (self)._myLog

        return None

    def _setField(self, name, value):
        if ((name) == (u"_buffered")):
            (self)._buffered = _cast(value, lambda: _Map)

        if ((name) == (u"_inFlight")):
            (self)._inFlight = _cast(value, lambda: _Map)

        if ((name) == (u"_added")):
            (self)._added = _cast(value, lambda: int)

        if ((name) == (u"_sent")):
            (self)._sent = _cast(value, lambda: int)

        if ((name) == (u"_recorded")):
            (self)._recorded = _cast(value, lambda: int)

        if ((name) == (u"_myLog")):
            (self)._myLog = value


SendWithAcks.quark_Map_quark_long_mdk_protocol_AckableEvent__ref = None
SendWithAcks.mdk_protocol_SendWithAcks_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_protocol")
