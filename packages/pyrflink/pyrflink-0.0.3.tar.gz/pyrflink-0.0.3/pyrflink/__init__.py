# This file is part of pyRFLink, a Python library to communicate with
# the RFLink family of devices from http://www.nemcon.nl/blog2/
# See https://pypi.python.org/pypi/pyrflink for the latest version.
#
# MIT License
#
# Copyright (c) 2016 mjj4791
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides the base implementation for pyRFLink
"""
from __future__ import print_function
import logging
import serial
import serial.threaded
from threading import Timer, Thread, Event
from time import sleep
import pyrflink
from . import test
from . import lowlevel
from . import dummyserial

RFLINK_BAUD_RATE = 57600
RFLINK_TIMEOUT = 1

STATE_UNKNOWN = 0
STATE_RESETTING = 1
STATE_VERSION = 2
STATE_INIT = 3
STATE_NORMAL = 4

def getlogger(name=None):
    if name:
        return logging.getLogger("{0}.{1}".format(__name__, name))
    else:
        return logging.getLogger(__name__)

def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
        
class RFLinkException(Exception): pass
class RFLinkWriteException(RFLinkException): 
    """ A write call to the RFLink device failed (device diconnected?): connection closed """
    pass
class RFLinkPongException(RFLinkException): 
    """ A PING/PONG call timed out. COnnection lost? """
    pass
class RFLinkConnectionLostException(RFLinkException): 
    """ The connection to the RFLink device is lost; connection closed. """
    pass

        
class RFLinkVersion(object):
    """ Generic RFLink version  """
    def __init__(self,versionstring, versionevent):
        self.versionstring = versionstring
        self.versionevent = versionevent
        self.version = float(versionevent.version)
        self.revision = int(versionevent.revision)
        self.build = int(versionevent.build)
        
    def __str__(self):
        return "RFLinkVersion: {0}, {1}.{2}.{3}".format(self.versionstring, self.version, self.revision, self.build )
        
class RFLinkReader(serial.threaded.LineReader):
    """
    Main class for reading and writing events/commands to/format
    the RFLink device.
    """    

    def __init__(self):
        super().__init__()   
        self.TERMINATOR = b'\r\n'
        self.ENCODING = 'utf-8'
        self.UNICODE_HANDLING = 'replace'   
        
        self.version_string = '?'           # RFLink version string, received during connect
        self.version = None                 # RFLinkVersion object
        
        self.state = STATE_RESETTING        # True when we are resetting (or initially connecting)
        
        self.__keepalive_stop = None        # threading.Event for stopping the keepalive thread
        self.keepalive_interval = 5         # Keepalive interval (in seconds)
        
        self.__set_interface_event = None   # threading.Event to stop ant wait for the set<IF> command to be finished
                                            # before issuing the next
        
        self.__event_callback = None         # (subclass of) RFLinkCallback to send events to
        
    def set_eventcallback(self, event_callback):
        self.__event_callback = event_callback
    def set_init(self, init=[]):
        self.__init = init
    def connection_made(self, transport):
        super().connection_made(transport)
        getlogger(self.__class__.__name__).info("Connected to device ({0}).".format( transport.__str__() ))
        self.wait_for_data()
        
    @threaded
    def wait_for_data(self):
        """
        Watchdog thread to wait for the initial output from RFLink device
        eg: '20;00;Nodo RadioFrequencyLink - RFLink Gateway V1.1 - R45;'
        """
        # wait for 2 * keepalive interval
        sleep(2*self.keepalive_interval)
        
        # if we are still in resetting state, something is wrong
        if self.state==STATE_RESETTING: 
            getlogger(self.__class__.__name__).error("No communication with device! Resetting...)")
            self.reset()
    
    def connection_lost(self, exc):
        if exc:
            if (self.__event_callback):
                exc2 = RFLinkConnectionLostException
                exc2.__cause__ = exc
                self.__event_callback.onRFLinkException(exc2)
            else:
                getlogger(self.__class__.__name__).error("Exception occured! {0}".format(str(exc) ))
        getlogger(self.__class__.__name__).info("Disconnected from device." )
        self.__stop_ping()
    
    @threaded
    def __initRFLink(self):
        """
        initialize the RFLink interface base don the specified init commands;
        for example:
          10;setNodoNRF=on;
          10;setMilight=on;
          10;setBLE=on;
          10;setMySensors=on;
          10;setLivingColors=on;
          10;setAnsluta=on;
          10;setGPIO=on;
        """
        getlogger(self.__class__.__name__).debug("__initRFLink".format(self.__init) )
        self.__set_interface_event = Event()
        for cmd in self.__init:
            self.write_line(cmd)
            self.__set_interface_event.wait(10)     # defaults to wait 10 secs
        
        # when done, set the state to normal operation:
        self.__setState(STATE_NORMAL)
        
    def __setState(self, state):
        """
        Set the internal connection state to STATE_NORMAL
        and trigger an RFLinkVersionEvent
        """
        getlogger(self.__class__.__name__).debug("__setState: {0}".format(state) )
        self.state = state
        if state == STATE_NORMAL:
            self.__start_ping()
            if self.__event_callback:
                self.__event_callback.onRFLinkEvent(self.version.versionevent)
    
    def handle_line(self, data):
        getlogger(self.__class__.__name__).debug("handle_line: {0}".format(data) )
        callback = None
        if self.state==STATE_RESETTING:
            # store the version string and request the complete version:
            self.__setState(STATE_VERSION)
            self.version_string = data.split(';')[2]
            self.write_line('10;VERSION;')
        else:
            if lowlevel.RFLinkEvent.is_event(data):
                event_class = lowlevel.RFLinkEvent.get_event_class(data)
                pkt = event_class()
                if self.__event_callback:
                    callback = self.__event_callback.onRFLinkEvent
            elif lowlevel.RFLinkCommand.is_command(data):
                getlogger(self.__class__.__name__).info("parseRFLinkCommand")
                pkt =  lowlevel.RFLinkCommand()
                if self.__event_callback:
                    callback = self.__event_callback.onRFLinkCommand
            else:
                pkt =  lowlevel.RFLinkPacket()
                if self.__event_callback:
                    callback = self.__event_callback.onRFLinkPacket
                
            pkt.load_receive(data)
            getlogger(self.__class__.__name__).debug("{0}".format(pkt.__str__()))
            
            if isinstance(pkt,lowlevel.PongEvent):
                self._pong_received = True
            if isinstance(pkt,lowlevel.VersionEvent):
                self.version = RFLinkVersion(self.version_string, pkt)
                if self.state == STATE_VERSION:
                    self.__setState(STATE_INIT)
                    self.__initRFLink()
            elif self.state == STATE_INIT:
                self.__set_interface_event.set()
                
            if callback and self.state==STATE_NORMAL:
                # only raise events when we are connected and initialization is done:
                callback(pkt)
                
    def write_line(self,text):
        """
        Write a line into the RFLink device
        """
        getlogger(self.__class__.__name__).debug("write_line: {0}".format(text))
        try:
            super().write_line(text)
        except:
            getlogger(self.__class__.__name__).exception("Error writing to RFLink device!")
            self.__stop_ping()
            if (self.__event_callback):
                self.__event_callback.onRFLinkException(RFLinkWriteException("A write call to the RFLink device failed (device diconnected?): connection closed"))
    
    def repeat(self,event):
        """
        Send out/repeat a received event, by issueing the command 
        that was used to trigger the event
        """
        getlogger(self.__class__.__name__).debug("{0}".format(str(event)))
        try:
            if ( isinstance(event,lowlevel.LightEvent) or
                 isinstance(event,lowlevel.SwitchEvent) or
                 isinstance(event,lowlevel.RollerEvent) ):
                cmd = event.get_command()
                getlogger(self.__class__.__name__).debug("cmd: {0}".format(str(cmd)))
                if cmd:
                    self.write_line(cmd)
        except:
            getlogger(self.__class__.__name__).exception("ERROR!")
        
    @threaded
    def keepalive(self):
        """ KeepAlive thread; monitors timely PING/PONG events """
        if not self.__keepalive_stop:
            getlogger(self.__class__.__name__).debug("Starting keepalive...")
            self.__keepalive_stop = Event()
            self._pong_received = True
            while not self.__keepalive_stop.wait(self.keepalive_interval):
                if not self._pong_received:
                    # no ping received in this loop; timeout....
                    getlogger(self.__class__.__name__).warning("No pong received...")
                    self.__pong_error()
                
                self._pong_received = None
                if not self.__keepalive_stop.is_set():
                    #getlogger(self.__class__.__name__).debug("sending ping...")
                    self.ping()
            
            getlogger(self.__class__.__name__).debug("Ending keepalive.")        
            self.__keepalive_stop = None
    
    def __pong_error(self):
        """ pong timed-out """
        getlogger(self.__class__.__name__).error("PONG timed-out!")
        self.__stop_ping()
        
        if (self.__event_callback):
                self.__event_callback.onRFLinkException(RFLinkPongException("A PING/PONG call timed out; connection lost?"))
        
    def __start_ping(self):
        """ start ping thread """
        getlogger(self.__class__.__name__).debug("Starting PING...")
        self.keepalive()
        
    def __stop_ping(self):
        """ stop ping thread """
        getlogger(self.__class__.__name__).debug("Stopping PING...")
        if self.__keepalive_stop:
            getlogger(self.__class__.__name__).debug("Stopped PING...")
            self.__keepalive_stop.set()
            
    def RFDebug(self, on=True):
        if on:
            self.write_line("10;RFDEBUG=ON;")
        else:
            self.write_line("10;RFDEBUG=OFF;")
    def RFUDebug(self, on=True):
        if on:
            self.write_line("10;RFUDEBUG=ON;")
        else:
            self.write_line("10;RFUDEBUG=OFF;")
    def QRFDebug(self, on=True):
        if on:
            self.write_line("10;QRFDEBUG=ON;")
        else:
            self.write_line("10;QRFDEBUG=OFF;")
    def RTSClean(self, index=None):
        if index:
            try:
                index = int(index)
            except:
                raise RFLinkException("RTSClean: index is not a number!")
                
            if index in range(0,15):
                self.write_line("10;RTSRECCLEAN={0};".format(index))
            else:
                raise RFLinkException("RTSClean: index not in range [0..15]!")
        else:
            self.write_line("10;RTSCCLEAN;")
    def RTSShow(self):
        self.write_line("10;RTSSHOW;")
    def ping(self):
        self.write_line("10;PING;")
    
    def turn_on(self,name,id,switch=None, brightness=None, rgb_color=None):
        if switch:
            if 'MiLight' in name:
                if brightness==None:
                    brightness=100
                if rgb_color==None:
                    rgb_color=255
                self.write_line("10;{0};{1};{2};{3:2x}{4:2x};ON;".format(name,id,switch, brightness, rgb_color))
            
            else:
                if brightness:
                    self.write_line("10;{0};{1};{2};{3};".format(name,id,switch, int(brightness*15/255)))
                else:
                    self.write_line("10;{0};{1};{2};ON;".format(name,id,switch))
        else:
            self.write_line("10;{0};{1};ON;".format(name,id))
    
    def turn_off(self,name,id,switch=None):
        if switch:
            self.write_line("10;{0};{1};{2};OFF;".format(name,id,switch))
        else:
            self.write_line("10;{0};{1};OFF;".format(name,id))
    
    def up(self,name,id,switch=None):
        if switch:
            self.write_line("10;{0};{1};{2};UP;".format(name,id,switch))
        else:
            self.write_line("10;{0};{1};UP;".format(name,id))
    def down(self,name,id,switch=None):
        if switch:
            self.write_line("10;{0};{1};{2};DOWN;".format(name,id,switch))
        else:
            self.write_line("10;{0};{1};DOWN;".format(name,id))
    def stop(self,name,id,switch=None):
        if switch:
            self.write_line("10;{0};{1};{2};STOP;".format(name,id,switch))
        else:
            self.write_line("10;{0};{1};STOP;".format(name,id))
    
    def reset(self):
        getlogger(self.__class__.__name__).debug("Resetting device...")
        self.resetting = True
        self.__stop_ping()
        self.write_line("10;REBOOT;")
        
        self.wait_for_data()
        
class RFLinkCallback(object):
    def onRFLinkException(self, exc):
        """ 
        called with an instance of RFLinkException
        """
        raise NotImplementedError()
    def onRFLinkEvent(self, event):
        """
        Called with an instance of RFLinkEvent
        """
        raise NotImplementedError()
    def onRFLinkCommand(self, cmd):
        """
        Called with an instance of RFLinkCommand
        """
        raise NotImplementedError()
    def onRFLinkPacket(self, pkt):
        """
        Called with an instance of RFLinkPacket
        """
        raise NotImplementedError()

class Connect(object):
    """ 
    The main class for pyrflink.
    Has methods for retrieving sensors.
    """
    
    def __init__(self, device, reconnect=True, event_callback=None, init=[]):
        """ 
        device:         port to open for reading RFLink data.
                        - use 'test:<filepath>' to generate dummy RFLink data using the RFLinkDummySerial class
                                                events/commands will be read from <filepath>
                        - use a real port name to connect to the actual device:
                            - 'COM3', '/dev/ttyUSB0'
                            - '/dev/ttyUSB-RFLink' (persistend USB device: 'https://www.domoticz.com/wiki/PersistentUSBDevices')
                            - 'rfc2217://<host>:<port>' (untested!)
        event_callback: (optional) instance of a subclass of RFLink.RFLinkCallback
        init:           (optional) list of commands to execute as initialization of the RFLink device
        """
        getlogger(self.__class__.__name__).debug("Creating serial port for '{0}'...".format(device))
        self._device = device
        self.__reconnect = reconnect
        self.__event_callback = []
        self.__init = init
        if event_callback:
            self.addEventCallback(event_callback)
            
        self.__connecting = False
        self.__stop__connecting = False
        self.reader = None
    
    @property
    def connecting(self):
        return self.__connecting
    @threaded
    def connect(self):
        if not self.__connecting:
            self.__connecting = True
            if self.reader:
                getlogger(self.__class__.__name__).debug("Closing connection...")
                self.reader.close()
                self.reader = None
                
            getlogger(self.__class__.__name__).info("Connecting to {0}...".format(self._device))
            while not self.reader and not self.__stop__connecting:
                try:
                    port = self.get_port()
                    if port:
                        self.reader = serial.threaded.ReaderThread(port, RFLinkReader)
                        self.reader.start()
                        while not self.reader.protocol:
                            # just to be sure the thread is up and running
                            sleep(1)
                        if self.reader.protocol:
                            if self.reader.protocol.set_init:
                                self.reader.protocol.set_init(self.__init)
                                
                            if self.reader.protocol.set_eventcallback:
                                getlogger(self.__class__.__name__).debug("Setting event callback...")
                                self.reader.protocol.set_eventcallback(self)
                        
                        self.__connecting = False
                        return
                except:
                    getlogger(self.__class__.__name__).exception('Unable to (re)connect.... sleeping...')
                    #pass
                
                getlogger(self.__class__.__name__).debug('Unable to (re)connect.... sleeping...')
                sleep(5)
        else:
            # already connection
            getlogger(self.__class__.__name__).warning('Already connecting!')
            
    def get_port(self):
        if self._device.startswith('test:'):
            port = dummyserial.RFLinkDummySerial(self._device)
        else:
            port = serial.serial_for_url(self._device)
        #TODO: handle serial-over-IP ports as well
        if isinstance(port, serial.Serial):
            getlogger(self.__class__.__name__).debug("Setting parameters for local serial port '{0}'...".format(self._device))
            port.baudrate = RFLINK_BAUD_RATE
            port.timeout = RFLINK_TIMEOUT
        return port
               
    def onRFLinkException(self, exc):
        """ 
        Internal exception handling
        
        Intercept Pong and ConnectionLost events, to implement reconnect-mechanism
        """
        try:
            raise exc
        except RFLinkConnectionLostException:
            getlogger(self.__class__.__name__).warning('RFLinkConnectionLostException...')
            if self.__reconnect:
                self.connect()
        except RFLinkPongException:
            getlogger(self.__class__.__name__).warning('RFLinkPongException: closing connection...')
            if self.__reconnect:
                self.connect()
            else:
                self.close_connection()        
        except:
            getlogger(self.__class__.__name__).exception('...')
            pass
        
        self.__fire_onRFLinkException(exc)
        
    def onRFLinkEvent(self, event):
        """ Pass RFLink events through to external handler """ 
        event.rflink=self
        self.__fire_onRFLinkEvent(event)
        
    def onRFLinkCommand(self, cmd):
        """ Pass RFLink commands  through to external handler """ 
        cmd.rflink=self
        self.__fire_onRFLinkCommand(cmd)
        
    def onRFLinkPacket(self, pkt):
        """ Pass RFLink packets through to external handler """ 
        pkt.rflink=self
        self.__fire_onRFLinkPacket(pkt)
        
    def addEventCallback(self,event_callback):
        self.__event_callback.append(event_callback)
    def removeEventCallback(self,event_callback):
        if event_callback in self.__event_callback:
            try:
                self.__event_callback.remove(event_callback)       
            except: pass
            
    @threaded
    def __fire_onRFLinkException(self,exc):
        if self.__event_callback:
            for event_callback in self.__event_callback:
                try:
                    event_callback.onRFLinkException(exc)
                except: pass
    @threaded
    def __fire_onRFLinkEvent(self,event):
        if self.__event_callback:
            for event_callback in self.__event_callback:
                try:
                    event_callback.onRFLinkEvent(event)
                except: pass
    @threaded
    def __fire_onRFLinkCommand(self,cmd):
        if self.__event_callback:
            for event_callback in self.__event_callback:
                try:
                    event_callback.onRFLinkCommand(cmd)
                except: pass
    @threaded
    def __fire_onRFLinkPacket(self,pck):
        if self.__event_callback:
            for event_callback in self.__event_callback:
                try:
                    event_callback.onRFLinkPacket(pck)
                except: pass
                     
    def RFDebug(self, on=True):
        if self.reader and self.reader.protocol:
            self.reader.protocol.RFDebug(on)
    def RFUDebug(self, on=True):
        if self.reader and self.reader.protocol:
            self.reader.protocol.RFUDebug(on)
    def QRFDebug(self, on=True):
        if self.reader and self.reader.protocol:
            self.reader.protocol.QRFDebug(on)
    def RTSClean(self, index=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.RTSClean(index)
    def RTSShow(self):
        if self.reader and self.reader.protocol:
            self.reader.protocol.RTSShow()
    def ping(self):
        if self.reader and self.reader.protocol:
            self.reader.protocol.ping()
    def reset(self):
        if self.reader and self.reader.protocol:
            self.reader.protocol.reset()
    def version(self):
        if self.reader and self.reader.protocol:
            return self.reader.protocol.version
    def turn_on(self, name, id, switch=None, brightness=None, rgb_color=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.turn_on(name,id,switch, brightness, rgb_color)
    def turn_off(self, name, id, switch=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.turn_off(name,id,switch)
    def up(self, name, id, switch=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.up(name,id,switch)
    def down(self, name, id, switch=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.down(name,id,switch)
    def stop(self, name, id, switch=None):
        if self.reader and self.reader.protocol:
            self.reader.protocol.stop(name,id,switch)
    
    def repeat(self, event):
        if self.reader and self.reader.protocol:
            self.reader.protocol.repeat(event)
            
    def close_connection(self):
        """ Close connection to device """
        self.__stop__connecting = True
        self.reader.close()
