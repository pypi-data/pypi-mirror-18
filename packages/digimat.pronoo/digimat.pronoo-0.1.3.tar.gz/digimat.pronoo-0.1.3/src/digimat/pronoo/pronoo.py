import time
from Queue import Queue
import json
import requests
from requests.auth import HTTPBasicAuth

import datetime

# pip install python-dateutil
import dateutil.parser


class UniqueQueue(Queue):
    def put(self, item, block=True, timeout=None):
        if item not in self.queue:  # fix join bug
            Queue.put(self, item, block, timeout)

    def _init(self, maxsize):
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()


class PronooPayload(object):
    def __init__(self, data=None):
        self._data=data
        self.onInit()

    def onInit(self):
        pass

    @property
    def data(self):
        return self._data

    @property
    def ptype(self):
        try:
            return self.data['payloadType']
        except:
            pass

    @property
    def content(self):
        try:
            return self.data['payload']
        except:
            pass

    def isType(self, ptype):
        if self.ptype==ptype:
            return True


class PronooTopic(object):
    def __init__(self, path):
        self._path=path
        self._items=path[2:].split('/')

    def item(self, n):
        try:
            return self._items[n]
        except:
            pass

    @property
    def path(self):
        return self._path

    @property
    def root(self):
        return self.item(0)

    @property
    def platform(self):
        return self.item(1)

    @property
    def device(self):
        return self.item(2)

    @property
    def group(self):
        return self.item(3)

    @property
    def channel(self):
        return self.item(4)

    @property
    def name(self):
        return self._items[-1]


class PronooQuality(object):
    GoodNonSpecific = 0x800000
    GoodLocalOverwrite = 0x809600
    GoodSubstitute = 0x809100
    GoodComputed = 0x809200
    UncertainNonSpecific = 0x400000
    UncertainLastUsableValue = 0x409000
    UncertainSubstitute = 0x409100
    UncertainSensorNotAccurate = 0x409300
    UncertainEngineeringUnitsExceeded = 0x409400
    UncertainSubNormal = 0x409500
    BadNonSpecific = 0x000000
    BadConfigurationError = 0x001000
    BadNotConnected = 0x00D000
    BadValueNotComputed = 0x00E000
    BadValueNotFound = 0x00E100
    BadDeviceFailure = 0x008B00
    BadSensorFailure = 0x008C00
    BadCommunicationError = 0x005000
    BadOutOfService = 0x00BF00
    BadObjectNotReadable = 0x003A00
    BadObjectNotWriteable = 0x003B00
    BadObjectNotFound = 0x003E00
    BadObjectDeleted = 0x003F00

    def __init__(self, value):
        try:
            self._value=int(value)
        except:
            self._value=self.BadNonSpecific

    @property
    def value(self):
        return self._value

    def isGood(self):
        if self.value>=self.GoodNonSpecific:
            return True
        return False

    def isBad(self):
        if self.value<self.UncertainNonSpecific:
            return True
        return False

    def isNotBad(self):
        if self.value>=self.UncertainNonSpecific:
            return True
        return False

    def isUncertain(self):
        if self.value>=self.UncertainNonSpecific and self.value<self.GoodNonSpecific:
            return True
        return False


class PronooData(object):
    def __init__(self, data):
        self._data=data
        self._timestamp=None

    @property
    def data(self):
        return self._data

    def get(self, name, defaultValue=None):
        try:
            return self.data[name]
        except:
            pass
        return defaultValue

    @property
    def value(self):
        return self.get('Value')

    @property
    def quality(self):
        return PronooQuality(self.get('Quality'))

    @property
    def timestamp(self):
        try:
            # caching
            if not self._timestamp:
                self._timestamp=dateutil.parser.parse(self.get('TimeStamp'))
            return self._timestamp
        except:
            return None

    def meta(self, key, defaultValue=None):
        try:
            return self.get('MetaData')['MetaKey.%s' % key]
        except:
            pass
        return defaultValue

    @property
    def topic(self):
        return PronooTopic(self.meta('Topic'))

    @property
    def identifier(self):
        return self.meta('Identifier')

    @property
    def category(self):
        return self.meta('Category')

    @property
    def nature(self):
        return self.meta('Nature')


class PronooChannel(object):
    def __init__(self, pronoo, name, refreshRate=60):
        self._pronoo=pronoo
        self._name=name
        self._refreshRate=refreshRate
        self._topic=None
        self._identifier=None
        self._pdata=None
        self._stampData=0
        self._timeoutQuery=0
        self._timeoutWatchdog=180.0
        self._pendingPublishData=None
        self._timeoutPublish=0

    @property
    def pronoo(self):
        return self._pronoo

    @property
    def pdata(self):
        return self._pdata

    @property
    def name(self):
        if self._identifier:
            return self._identifier
        return self._name

    @property
    def topic(self):
        return self._topic

    @property
    def identifier(self):
        return self._identifier

    def age(self):
        return time.time()-self._stampData

    def load(self, pdata):
        try:
            if pdata:
                self._pdata=pdata
                self._stampData=time.time()
                self._timeoutWatchdog=time.time()+3*self._refreshRate+3.0
                if not self.topic or not self.identifier:
                    self._identifier=pdata.identifier
                    self._topic=pdata.topic
                    self.pronoo.registerChannel(self)
        except:
            pass

    def manager(self):
        if self.age()>=self._refreshRate and time.time()>=self._timeoutQuery:
            self._timeoutQuery=time.time()+10.0
            self.pronoo.submitChannelQuery(self)

        if self._pendingPublishData and time.time()>=self._timeoutPublish:
            self._timeoutPublish=time.time()+10.0
            self.pronoo.submitChannelPublish(self)

    @property
    def value(self):
        try:
            return self.pdata.value
        except:
            pass

    def set(self, value, valid=True, timestamp=None):
        try:
            if not timestamp:
                timestamp=datetime.datetime.utcnow()

            quality=PronooQuality.BadNonSpecific
            if valid:
                quality=PronooQuality.GoodNonSpecific

            self._pendingPublishData={'value': str(value), 'quality': quality, 'timeStamp': timestamp.isoformat()}
            self.pronoo.submitChannelPublish(self)
        except:
            pass

    def getPendingPublishData(self):
        return self._pendingPublishData

    def clearPendingPublishData(self):
        self._pendingPublishData=None


class Pronoo(object):
    def __init__(self, urlAPI, user, password, timeout=5.0):
        self._url=urlAPI
        self._user=user
        self._password=password
        self._session=None
        self._timeout=timeout
        self._channels=[]
        self._indexChannels={}
        self._queueChannelPublish=UniqueQueue()
        self._queueChannelQuery=UniqueQueue()

    @property
    def session(self):
        if self._session:
            return self._session
        self._session=requests.Session()
        return self._session

    def close(self):
        self._session=None

    def doesIdentifierLooksLikeTopic(self, identifier):
        try:
            if identifier[0:2]=='//':
                return True
        except:
            pass

    def identifierType(self, identifier):
        if self.doesIdentifierLooksLikeTopic(identifier):
            return 'topic'
        return 'identifier'

    def urlFromService(self, service):
        return '/'.join([self._url, service])

    def post(self, service, data=None):
        try:
            auth=HTTPBasicAuth(self._user, self._password)
            print "-->POST", service, data
            r=self.session.post(self.urlFromService(service),
                                auth=auth,
                                timeout=self._timeout,
                                data=data)
            print "<--", r
            return r
        except:
            pass

    # unused yet
    def get(self, service, data=None):
        try:
            auth=HTTPBasicAuth(self._user, self._password)
            r=self.session.get(self.urlFromService(service),
                        auth=auth,
                        timeout=self._timeout,
                        data=data)
            if r and r.status_code==requests.codes.ok:
                return json.loads(r.json())
        except:
            pass

    def queryChannels(self, channels):
        try:
            if channels:
                request=[]
                if not isinstance(channels, list):
                    channels=[channels]
                for channel in channels:
                    request.append({self.identifierType(channel.name): channel.name})

                data={'request': json.dumps(request)}
                r=self.post('Query', data)
                if r and r.status_code==requests.codes.ok:
                    # TODO: a bit curious here
                    rdata=json.loads(r.json())
                    payload=PronooPayload(rdata)
                    if payload.isType('data'):
                        for data in payload.content:
                            try:
                                pdata=PronooData(data)
                                channel=self.channel(pdata.identifier)
                                channel.load(pdata)
                                print "VALUE", channel.identifier, channel.topic.path, channel.value
                                print channel.pdata.timestamp
                                print pdata.data
                                print "-"*60
                            except:
                                pass
        except:
            pass

    def publishChannels(self, channels):
        try:
            if channels:
                request=[]
                if not isinstance(channels, list):
                    channels=[channels]
                for channel in channels:
                    data={'data': channel.getPendingPublishData()}
                    data[self.identifierType(channel.name)]=channel.name
                    request.append(data)

                data={'request': json.dumps(request)}
                r=self.post('Publish', data)
                if r and r.status_code==requests.codes.ok:
                    for channel in channels:
                        # clear request
                        channel.clearPendingPublishData()
                        self.submitChannelQuery(channel)
        except:
            pass

    # def browse(self):
        # return self.get('GeneralRequest')

    def channel(self, name):
        try:
            return self._indexChannels[name]
        except:
            pass

    def channels(self):
        return self._channels

    def createChannel(self, name):
        channel=self.channel(name)
        if not channel:
            channel=PronooChannel(self, name)
            self._channels.append(channel)
            self._indexChannels[name]=channel
        return channel

    def registerChannel(self, channel):
        try:
            self._indexChannels[channel.topic.path]=channel
        except:
            pass

        try:
            self._indexChannels[channel.identifier]=channel
        except:
            pass

    def submitChannelQuery(self, channel):
        self._queueChannelQuery.put(channel)

    def submitChannelPublish(self, channel):
        self._queueChannelPublish.put(channel)

    def manager(self):
        for channel in self._channels:
            channel.manager()

        # write
        if not self._queueChannelPublish.empty():
            print "WRITE MANAGER"
            channels=[]
            try:
                while True:
                    channel=self._queueChannelPublish.get(False)
                    channels.append(channel)
            except:
                pass
            self.publishChannels(channels)

        # read
        if not self._queueChannelQuery.empty():
            print "READ MANAGER"
            channels=[]
            try:
                while True:
                    channel=self._queueChannelQuery.get(False)
                    channels.append(channel)
            except:
                pass
            self.queryChannels(channels)


if __name__=='__main__':
    pass
