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
This module provides low level packet parsing and generation code for the
RFLink.
"""
from __future__ import division
import logging
import math
#import hashlib
import base64
from time import sleep
from threading import Thread
import pyrflink

def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

UTF8='utf-8'

def htosi(val):
    uintval = int(val,16)
    # check sign bit
    check = int('8' + '0'*(len(val)-1) ,16)
    if (uintval & check) == check:
        uintval -= check
        uintval = -uintval
    return uintval
    
def getlogger(name=None):
    if name:
        return logging.getLogger("{0}.{1}".format(__name__, name))
    else:
        return logging.getLogger(__name__)
 
class RFLinkPacket(object):
    """
    Abstract superclass for all rflink packets
    """
    TYPE_UNKNOWN = -1
    TYPE_COMMAND = 10
    TYPE_COMMAND_CREATE = 11
    TYPE_EVENT = 20
    
    
    def __init__(self):
        # class variables:
        self.data = None                # the raw data string as received
        self.type = self.TYPE_UNKNOWN        # data type 
        self.rflink=None
    
    def load_receive(self, data):
        """Load data from a bytearray; speciofic implementation in subclasses!"""
        self.data = data
        getlogger(self.__class__.__name__).debug("data={0}".format(self.data))
        self.data2=data.split(';')
        
        # parse the type of the command:
        try:
            t=int(self.data2[0])
            if t==self.TYPE_COMMAND:
                self.type = self.TYPE_COMMAND
            elif t==self.TYPE_COMMAND_CREATE:
                self.type = self.TYPE_COMMAND_CREATE
            elif t==self.TYPE_EVENT:
                self.type = self.TYPE_EVENT
            else:
                self.type = self.TYPE_UNKNOWN            
        except:
            self.type = self.TYPE_UNKNOWN
        
        
    def has_value(self, name):
        """Return True if the event supports the given attribute/value.
        sensor.has_value('TEMP') is identical to calling
        sensor.has_TEMP().
        """
        return hasattr(self, name)
    
    def value(self, name):
        """Return the :class:`SensorValue` for the given name.
        sensor.value('TEMP') is identical to calling
        sensor.TEMP().
        """
        return getattr(self, name, None)
    
    def __getattr__(self, name):
        typename = name.replace("has_", "", 1)
        if not name == typename:
            return lambda: self.has_value(typename)
        raise AttributeError(name)
        
    def __str__(self):
        return ("RFLinkPacket [type={0}, data={1}]".format(self.type, self.data))
        
class RFLinkCommand(RFLinkPacket):
    """
    Data class for RFLink command packet type (code 10)
    
    Special commands:
    10;REBOOT; => Reboot RFLink Gateway hardware
    10;PING; => a "keep alive" function. Is replied with: 20;99;PONG;
    10;VERSION; => Version and build indicator. Is replied with: 20;99;"RFLink Gateway software version";
    10;RFDEBUG=ON; => ON/OFF to Enable/Disable showing of RF packets. Is replied with: 20;99;RFDEBUG="state";
    10;RFUDEBUG=ON; => ON/OFF to Enable/Disable showing of undecoded RF packets. Is replied with: 20;99;RFUDEBUG="state";
    10;QRFDEBUG=ON; => ON/OFF to Enable/Disable showing of undecoded RF packets. Is replied with: 20;99;QRFDEBUG="state";
    QRFDEBUG is a faster version of RFUDEBUG but all pulse times are shown in hexadecimal and need to be multiplied by 30
    10;RTSCLEAN; => Clean Rolling code table stored in internal EEPROM
    10;RTSRECCLEAN=9 => Clean Rolling code record number (value from 0 - 15)
    10;RTSSHOW; => Show Rolling code table stored in internal EEPROM

    Packet structure - To Send data via RF:
    10;Protocol Name;device address,button number;action;
    """
    UNKNOWN_ID = -1
    
    def __init__(self):
        super().__init__()
        
        self.name = None             # name of the command
        self.id = None               # the device address
        self.switch = None           # the button number
        self.action = None           # the action
        self.__deviceid = None
        
    def load_receive(self, data):
        """Load data from a bytearray"""
        getlogger(self.__class__.__name__).debug("data={0}".format(data))
        super().load_receive(data)
        
        if self.type != self.TYPE_COMMAND and self.type != self.TYPE_COMMAND_CREATE:
            raise AttributeError("Not an RFLinkCommand: data contains type={0}".format(self.type))
        
        for index in range(1, len(self.data2)):
            if index==1:
                # the name
                self.name = self.data2[index]
            
            if index==2:
                # the device address
                self.id = self.data2[index]
                
            if index==3:
                # the button number
                self.switch = self.data2[index]
                
            if index==4:
                # the action
                if self.name=='MiLightv1':
                    self.action = "{0};{1}".format(self.data2[index], self.data2[index+1])
                else:
                    self.action = self.data2[index]
                
    @staticmethod
    def is_command(data):
        data2=data.split(';')
        # data2= '10;special_command;'                  10;VERSION;
        # data2= '10;protocol;address;switch;command;'  10;EV1527;000080;0;ON; 
        return data2[0]=='10' and len(data2)>=3
        
    def device(self):
        if self.switch:
            if self.action in "ON|OFF|ALLON|ALLOFF":
                return RFLinkSwitchDevice(name=self.name, id=self.id, switch=self.switch, deviceid=self.deviceid, rflink=self.rflink)
            elif self.action in "UP|DOWN":
                return RFLinkRollerDevice(name=self.name, id=self.id, switch=self.switch, deviceid=self.deviceid, rflink=self.rflink)
            elif self.action in "COLOR|BRIGHT|DISCO+|DISCO-|MODE0|MODE1|MODE2|MODE3|MODE4|MODE5|MODE6|MODE7|MODE8":
                return RFLinkLightDevice(name=self.name, id=self.id, switch=self.switch, deviceid=self.deviceid, rflink=self.rflink)
            else:
                return RFLinkDevice(name=self.name, id=self.id, switch=self.switch, deviceid=self.deviceid, rflink=self.rflink)
        else:
            return RFLinkDevice(name=self.name, id=self.id, deviceid=self.deviceid, rflink=self.rflink)
            
    def deviceid(self):
        if self.__deviceid==None:
            if self.has_value('switch'):
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id,self.switch)
            else:
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id)
        return self.__deviceid
        
    def __str__(self):
        return ("RFLinkCommand [type={0}, name={1}, address={2}, switch={3}, action={4}, data={5}".format(self.type, self.name, self.id, self.switch, self.action, self.data))

class RFLinkEvent(RFLinkPacket):
    """
    Data class for RFLink event packet type (code 20)
    
    Packet structure - Received data from RF:
    20;ID=9999;Name;LABEL=data;
    """
    UNKNOWN_ID = -1
    
    def __init__(self):
        super().__init__()
        self.id = self.UNKNOWN_ID         # command unique id
        self.name = None             # name of the event
        self.attributes=[]           # list of added attribute-names
        
    def load_receive(self, data):
        """Load data from a bytearray"""
        getlogger(self.__class__.__name__).debug("data={0}".format(data))
        super().load_receive(data)
        #print("{0} : {1} : data={2}".format(super().type,self.type, self.data))
        
        if self.type != self.TYPE_EVENT:
            raise AttributeError("Not an RFLinkEvent: data contains type={0}".format(self.type))
        
        
        for index in range(1, len(self.data2)):
            if index==1:
                # the identifier
                try:
                    self.eventid = int(self.data2[index],16)
                except:
                    self.eventid = self.UNKNOWN_ID
            if index==2:
                self.name = self.data2[index]
                
            if index>2:
                # LABEL=VALUE data from RFLINK:
                fields = self.data2[index].split('=',1)
                if len(fields)==2:
                    # a <LABEL=data> field
                    lbl = fields[0]
                    val=fields[1]
                else:
                    # not a <LABEL=data> field; assuming all to be a keys
                    lbl = fields[0]
                    val = None
                self.attributes.append(lbl)
                setattr(self,lbl,val)
        
        if self.has_value('ID'):
            # ID=9999 => device ID (often a rolling code and/or device channel number) (Hexadecimal)
            self.id = self.value('ID')
            
        if self.has_value('BAT'):
            self.battery = self.BAT
        
    @staticmethod
    def is_event(data):
        data2=data.split(';')
        # data2= '20;eventid;name;LABEL=VALUE;'
        # data2= '20;eventid;name;'
        return data2[0]=='20' and len(data2)>=4
    
    def get_command(self):
        return None
        
    @staticmethod
    def get_event_class(data):
        """
        elif RFLinkEvent.is_weather_event(data):
            return WeatherEvent
        elif RFLinkEvent.is_ringer_event(data):
            return RingerEvent
        elif RFLinkEvent.is_alarm_event(data):
            return AlarmEvent
        elif RFLinkEvent.is_sound_event(data):
            return SoundEvent
        elif RFLinkEvent.is_electric_event(data):
            return ElectricEvent
        elif RFLinkEvent.is_distance_event(data):
            return DistanceEvent
        elif RFLinkEvent.is_meter_event(data):
            return MeterEvent
        """
        if RFLinkEvent.is_version_event(data):
            return VersionEvent
        elif RFLinkEvent.is_light_event(data):
            # NOTE: LightEvent MUST be tested before SwitchEvent (due to subclassing)!
            return LightEvent
        elif RFLinkEvent.is_switch_event(data):
            return SwitchEvent
        elif RFLinkEvent.is_roller_event(data):
            return RollerEvent
        elif RFLinkEvent.is_sensor_event(data):
            return SensorEvent
        elif RFLinkEvent.is_pong_event(data):
            return PongEvent
        elif RFLinkEvent.is_special_event(data):
            return SpecialEvent
        else:
            return RFLinkEvent
            
    @staticmethod
    def data_contains(data, attrs):
        for atr in attrs:
            if atr in data:
                return True
        return False      
    @staticmethod
    def is_special_event(data):
        # 10;PING;          ==>     20;08;PONG;                     --> PongEvent
        # 10;VERSION;       ==>     20;0A;VER=1.1;REV=43;BUILD=0a;  --> VersionEvent
        # 10;RFDEBUG=ON;    ==>     20;0B;RFDEBUG=ON;
        # 10;RFUDEBUG=ON;   ==>     20;0E;RFUDEBUG=ON;
        # 10;QRFDEBUG=ON;   ==>     20;10;QRFDEBUG=ON;
        # 10;RTSCLEAN;      ==>     20;06;RTS CLEANED;
        # 10;RTSRECCLEAN=9  ==>     20;07;RECORD 09 CLEANED
        # 10:RTSSHOW        ==>     RTS Record: 0 Address: 000000 RC: 0000.....
        attrs = ['RFDEBUG=', 'RFUDEBUG=', 'QRFDEBUG=', 'RTS Record', 'RTS CLEANED']
        return RFLinkEvent.data_contains(data, attrs) or ('RECORD ' in data and ' CLEANED;' in data)
    @staticmethod
    def is_pong_event(data):
        attrs = ['PONG']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_version_event(data):
        attrs = ['VER=', 'REV=', 'BUILD=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_light_event(data):
        attrs = ['RGBW=']
        
        if RFLinkEvent.data_contains(data, attrs):
            return True
        if 'CMD' in data:
            return 'SET_LEVEL' in data or 'DISCO' in data or 'MODE' in data
        return False
    @staticmethod
    def is_roller_event(data):
        return RFLinkEvent.data_contains(data, ['CMD=UP', 'CMD=DOWN', 'CMD=STOP']) and RFLinkEvent.data_contains(data, ['SWITCH='])
    @staticmethod
    def is_switch_event(data):
        rgbw = False
        rgbw=RFLinkEvent.data_contains(data, ['RGBW='])
        if 'CMD=ON' in data or 'CMD=OFF' in data or 'ALLON' in data or 'ALLOFF' in data:
            # this is a light event if RGBW= has been set; otherwise a switch event
            return not rgbw    
        return False
    @staticmethod  
    def is_sensor_event(data):
        attrs = ['METER=', 'DIST=', 'KWATT=','WATT=','CURRENT=','CURRENT2=','CURRENT3=','VOLT=', 'SOUND=', 'SMOKEALERT=', 'CO2=', 'PIR=','CHIME=','TEMP=','HUM=','BARO=','HSTATUS=','BFORECAST=','UV=','LUX=','RAIN=','RAINRATE=','WINSP=','AWINSP=','WINGS=','WINDIR=','WINCHL=','WINTMP=']
        return RFLinkEvent.data_contains(data, attrs)
    
    """
    @staticmethod  
    def is_weather_event(data):
        attrs = ['TEMP=','HUM=','BARO=','HSTATUS=','BFORECAST=','UV=','LUX=','RAIN=','RAINRATE=','WINSP=','AWINSP=','WINGS=','WINDIR=','WINCHL=','WINTMP=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod   
    def is_ringer_event(data):
        attrs = ['CHIME=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_alarm_event(data):
        attrs = ['SMOKEALERT=', 'CO2=', 'PIR=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_sound_event(data):
        attrs = ['SOUND=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_electric_event(data):
        attrs = ['KWATT=','WATT=','CURRENT=','CURRENT2=','CURRENT3=','VOLT=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_distance_event(data):
        attrs = ['DIST=']
        return RFLinkEvent.data_contains(data, attrs)
    @staticmethod
    def is_meter_event(data):
        attrs = ['METER=']
        return RFLinkEvent.data_contains(data, attrs)
    """
    def __str__(self):
        attrstr = ''
        for atr in self.attributes:
            if len(attrstr)>0: 
                attrstr += ', '
            attrstr += "{0} : {1}".format(atr, getattr(self,atr)) 
        if self.has_value('battery'):
            return ("RFLinkEvent type={0}, eventid={1}, name={2}, id={3}, battery={4}, attributes=<{5}>, data={6}".format(self.type, self.eventid, self.name, self.id, self.battery, attrstr, self.data))
        else:
            return ("RFLinkEvent type={0}, eventid={1}, name={2}, id={3}, attributes=<{4}>, data={5}".format(self.type, self.eventid, self.name, self.id, attrstr, self.data))
       
class RFLinkDevice(object):
    """
    Class representing a RFLink device which has been "seen"
    """
    def __init__(self, name=None, id=None, switch=None, deviceid=None, rflink=None):
        self.__name = name
        self.__id = id
        self.__switch = switch
        self.__deviceid = deviceid
        self.__rflink=rflink
    
    @property
    def name(self):
        return self.__name
    @property
    def id(self):
        return self.__id
    @property
    def switch(self):
        return self.__switch
    @property
    def deviceid(self):
        if not self.__deviceid:
            self.__deviceid = RFLinkDevice.get_deviceid(self.__name,self.__id,self.__switch)
        
        return self.__deviceid
        
    @property
    def rflink(self):
        return self.__rflink
        
    @staticmethod
    def get_deviceid(name,id,switch=None):
        if switch and len(switch)>0:
            return base64.b64encode("{0};{1};{2}".format(name,id,switch).encode(UTF8)).decode(UTF8)
        else:
            return base64.b64encode("{0};{1};".format(name,id).encode(UTF8)).decode(UTF8)
        
    @staticmethod
    def get_device_from_id(deviceid, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid
        """
        return RFLinkDevice.get_device_from_id_(deviceid,RFLinkDevice,rflink)

    def get_device_from_id_(deviceid, devclass, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid and the specified class
        """
        props = base64.b64decode(deviceid).decode(UTF8).split(';')
        if len(props)==3:
            return devclass(name=props[0],id=props[1],switch=props[2], deviceid=deviceid,rflink=rflink)
        else:
            return devclass(name=props[0],id=props[1],deviceid=deviceid,rflink=rflink)
        
    def __str__(self):
        return "RFLinkDevice: name={0}, id={1}, switch={2}, device_id={3}".format(self.__name, self.__id, self.__switch, self.__deviceid)
        
class RFLinkRollerDevice(RFLinkDevice):
    @staticmethod
    def get_device_from_id(deviceid, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid
        """
        return RFLinkDevice.get_device_from_id_(deviceid,RFLinkRollerDevice,rflink)
    
    @threaded
    def up(self, signal_repetitions=1): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.up(self.name, self.id, self.switch)
                sleep(0.1)
    @threaded
    def down(self, signal_repetitions=1): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.down(self.name, self.id, self.switch)
                sleep(0.1)
    @threaded
    def stop(self, signal_repetitions=1): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.stop(self.name, self.id, self.switch)
                sleep(0.1)
    
    
    def __str__(self):
        return super().__str__().replace('RFLinkDevice', 'RFLinkRollerDevice')
     
class RFLinkSensorDevice(RFLinkDevice):
    @staticmethod
    def get_device_from_id(deviceid, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid
        """
        return RFLinkDevice.get_device_from_id_(deviceid,RFLinkSensorDevice,rflink)
    
    def __str__(self):
        return super().__str__().replace('RFLinkDevice', 'RFLinkSensorDevice')

class RFLinkSwitchDevice(RFLinkDevice):
    @staticmethod
    def get_device_from_id(deviceid, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid
        """
        return RFLinkDevice.get_device_from_id_(deviceid,RFLinkSwitchDevice,rflink)
    
    @threaded
    def turn_on(self, signal_repetitions=1): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.turn_on(self.name, self.id, self.switch)
                sleep(0.1)
        
    @threaded
    def turn_off(self, signal_repetitions=1): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.turn_off(self.name, self.id, self.switch)
                sleep(0.1)
        
    def __str__(self):
        return super().__str__().replace('RFLinkDevice', 'RFLinkSwitchDevice')

class RFLinkLightDevice(RFLinkSwitchDevice):
    @staticmethod
    def get_device_from_id(deviceid, rflink=None):
        """
        Get a RFLink device (or subclass) based on the deviceid
        """
        return RFLinkDevice.get_device_from_id_(deviceid,RFLinkLightDevice,rflink)

    @threaded
    def turn_on(self, signal_repetitions=1, brightness=None, color=None): 
        #pass
        if self.rflink:
            for index in range(signal_repetitions):
                self.rflink.turn_on(self.name, self.id, self.switch, brightness, color)
                sleep(0.1)
                
            
    def __str__(self):
        return super().__str__().replace('RFLinkSwitchDevice', 'RFLinkLightDevice')
        
class PongEvent(RFLinkEvent):
    """
    Pong event
    """
    def __init__(self):
        super().__init__()
        
    def load_receive(self, data):
        super().load_receive(data);
    
    def get_command(self):
        return '10;PING;'
        
    def __str__(self):
        return "PongEvent {0}".format(super().__str__().replace('RFLinkEvent', '')) 

class SpecialEvent(RFLinkEvent):
    """
    Special Command Event
    
    10;RFDEBUG=ON;    ==>     20;0B;RFDEBUG=ON;
    10;RFUDEBUG=ON;   ==>     20;0E;RFUDEBUG=ON;
    10;QRFDEBUG=ON;   ==>     20;10;QRFDEBUG=ON;
    10;RTSCLEAN;      ==>     20;06;RTS CLEANED;
    10;RTSRECCLEAN=9  ==>     20;07;RECORD 09 CLEANED
    10;RTSSHOW        ==>     RTS Record: 0 Address: 000000 RC: 0000
                                RTS Record: 1 Address: 000000 RC: 0000
                                RTS Record: 2 Address: 000000 RC: 0000
                                RTS Record: 3 Address: 000000 RC: 0000
                                RTS Record: 4 Address: 000000 RC: 0000
                                RTS Record: 5 Address: 000000 RC: 0000
                                RTS Record: 6 Address: 000000 RC: 0000
                                RTS Record: 7 Address: 000000 RC: 0000
                                RTS Record: 8 Address: 000000 RC: 0000
                                RTS Record: 9 Address: 000000 RC: 0000
                                RTS Record: 10 Address: 000000 RC: 0000
                                RTS Record: 11 Address: 000000 RC: 0000
                                RTS Record: 12 Address: 000000 RC: 0000
                                RTS Record: 13 Address: 000000 RC: 0000
                                RTS Record: 14 Address: 000000 RC: 0000
                                RTS Record: 15 Address: 000000 RC: 0000
    """
    def __init__(self):
        super().__init__()
    
    def get_command(self):
        cmd = None
        if self.has_value('rfdebug'):
            cmd= "10;RFDEBUG={0};".format(self.rfdebug)
        if self.has_value('rfudebug'):
            cmd="RFUDEBUG={0};".format(self.rfudebug)
        if self.has_value('qrfdebug'):
            cmd="QRFDEBUG={0};".format(self.qrfdebug)
        if self.has_value('rtscleaned'):
            if self.rtsrecord>0:
                cmd="10;RTSRECCLEAN={0};".format(self.rtsrecord)
            else:
                cmd="10;RTSCLEAN;"
        if self.has_value('rtsshow'):
            cmd="10;RTSSHOW;"
        
        return cmd
     
    def load_receive(self, data):
        super().load_receive(data);
        
        # correct; special event does not specify a Name part:
        fields = self.name.split('=',1)
        if len(fields)==2:
            setattr(self,fields[0],fields[1])
        else:
            if 'RTS Record:' in self.name:
                setattr(self,'rtsshow',fields[1])
                
        if self.has_value('RFDEBUG'):
            self.rfdebug = (self.RFDEBUG == 'ON')
        if self.has_value('RFUDEBUG'):
            self.rfudebug = (self.RFUDEBUG == 'ON')
        if self.has_value('QRFDEBUG'):
            self.qrfdebug = (self.QRFDEBUG == 'ON')
        if self.name == 'RTS CLEANED':
            self.rtscleaned = True
            self.rtsrecord = -1
        if 'RECORD' in self.name and 'CLEANED' in self.name:
            # not nice, but prevents the use of re.match()...
            self.rtscleaned = True
            self.rtsrecord = int(self.name.split(' ')[1])
            
        
    def __str__(self):
        props=''
        if self.has_value('rfdebug'):
            props += "rfdebug={0} ".format(self.rfdebug)
        if self.has_value('rfudebug'):
            props += "rfudebug={0} ".format(self.rfudebug)
        if self.has_value('qrfdebug'):
            props += "qrfdebug={0} ".format(self.qrfdebug)
        if self.has_value('rtscleaned'):
            props += "rtscleaned={0} rtsrecord={1} ".format(self.rtscleaned, self.rtsrecord)
        if self.has_value('rtsshow'):
            props += "rtsshow={0} ".format(self.rtsshow)
        
        return "SpecialEvent {0}{1}".format(props, super().__str__().replace('RFLinkEvent', '')) 
    
class VersionEvent(RFLinkEvent):
    """
    Version info event
    """
    def __init__(self):
        super().__init__()
        self.version = '?'
        self.revision = '?'
        self.build = '?'
        
    def load_receive(self, data):
        super().load_receive(data);
        
        # correct; version event does not specify a Name part:
        try:
            self.VER = self.name.split('=',1)[1]
        except:
            pass
            
        if self.has_value('VER'):
            self.version = self.VER
        if self.has_value('REV'):
            self.revision = self.REV
        if self.has_value('BUILD'):
            self.build = self.BUILD
    
    def get_command(self):
        return "10;VERSION;"
        
    def __str__(self):
        return "VersionEvent version={0}, revision={1}, build={2} {3}".format(self.version, self.revision, self.build, super().__str__().replace('RFLinkEvent', '')) 
    
class SensorEvent(RFLinkEvent):
    """
    Base class for all sensors; 
    should not be used directly; use one of its subclasses!
    """
    #_data_types = ['meter', 'distance', 'watt', 'current', 'current2', 'current3', 'volt', 'noiselevel', 'alarm', 'smokealert', 'movementalert', 'co2alert', 'chime', 'temperature', 'hum', 'baro', 'hstatus', 'hstatus_desc', 'forecast', 'forecast_desc', 'uv', 'lux', 'rain', 'raintot', 'rainrate', 'windspeed', 'awindspeed', 'windgust', 'winddirection', 'windchill', 'windtemp']
    data_types = {
        'battery':          { 'unit_of_measurement': '' }, 
        'meter':            { 'unit_of_measurement': '' }, 
        'distance':         { 'unit_of_measurement': 'm' }, 
        'watt':             { 'unit_of_measurement': 'W' }, 
        'current':          { 'unit_of_measurement': 'A' }, 
        'current2':         { 'unit_of_measurement': 'A' }, 
        'current3':         { 'unit_of_measurement': 'A' }, 
        'volt':             { 'unit_of_measurement': 'V' }, 
        'noiselevel':       { 'unit_of_measurement': 'dB' }, 
        'alarm':            { 'unit_of_measurement': '' }, 
        'smokealert':       { 'unit_of_measurement': '' }, 
        'movementalert':    { 'unit_of_measurement': '' }, 
        'co2alert':         { 'unit_of_measurement': '' }, 
        'chime':            { 'unit_of_measurement': '' }, 
        'temperature':      { 'unit_of_measurement': 'ºC' }, 
        'humidity':         { 'unit_of_measurement': '%' }, 
        'pressure':         { 'unit_of_measurement': 'mbar' }, 
        'hstatus':          { 'unit_of_measurement': '' }, 
        'hstatus_desc':     { 'unit_of_measurement': '' }, 
        'forecast':         { 'unit_of_measurement': '' }, 
        'forecast_desc':    { 'unit_of_measurement': '' }, 
        'uv':               { 'unit_of_measurement': 'mW/cm2' }, 
        'lux':              { 'unit_of_measurement': 'lux' }, 
        'rain':             { 'unit_of_measurement': 'mm' }, 
        'raintot':          { 'unit_of_measurement': 'mm' }, 
        'rainrate':         { 'unit_of_measurement': 'mm' }, 
        'windspeed':        { 'unit_of_measurement': 'km/h' }, 
        'awindspeed':       { 'unit_of_measurement': 'km/h' }, 
        'windgust':         { 'unit_of_measurement': 'km/h' }, 
        'winddirection':    { 'unit_of_measurement': 'º' }, 
        'windchill':        { 'unit_of_measurement': 'ºC' }, 
        'windtemp':         { 'unit_of_measurement': 'ºC' }
        }
    
    def __init__(self):
        super().__init__()
        self.__deviceid=None
        
    def load_receive(self, data):
        super().load_receive(data);
        # meter event
        if self.has_value('METER'):
            # METER=1234 => Meter values (water/electricity etc.)
            try:
                self.meter = int(self.METER)
            except: 
                pass
        # distance
        if self.has_value('DIST'):
            # DIST=1234 => Distance
            try:
                self.distance = int(self.DIST)
            except: 
                pass
        # electric
        # 'KWATT=','WATT=','CURRENT=','CURRENT2=','CURRENT3=','VOLT='
        if self.has_value('KWATT'):
            # KWATT=9999 => KWatt (hexadecimal)
            try:
                self.watt = int(self.KWATT,16) * 1000
            except: 
                pass
        if self.has_value('WATT'):
            # WATT=9999 => Watt (hexadecimal)
            try:
                self.watt = int(self.WATT,16)
            except:
                pass
        if self.has_value('CURRENT'):
            # CURRENT=1234 => Current phase 1
            try:
                self.current = int(self.CURRENT)
            except:
                pass
        if self.has_value('CURRENT2'):
            # CURRENT2=1234 => Current phase 2 (CM113)
            try:
                self.current2 = int(self.CURRENT2)
            except:
                pass
        if self.has_value('CURRENT3'):
            # CURRENT2=1234 => Current phase 3 (CM113)
            try:
                self.current3 = int(self.CURRENT3)
            except:
                pass
        if self.has_value('VOLT'):
            # VOLT=1234 => Voltage
            try:
                self.volt = int(self.VOLT)
            except:
                pass
        # Sound
        if self.has_value('SOUND'):
            # SOUND=1234 => Noise level
            try:
                self.noiselevel = int(self.SOUND)
            except:
                pass
        # Alarm 
        if self.has_value('SMOKEALERT'):
            # SMOKEALERT=ON => ON/OFF
            self.smokealert = (self.SMOKEALERT!='OFF')
            self.alert=True
        if self.has_value('PIR'):
            # PIR=ON => ON/OFF
            self.movementalert = (self.PIR!='OFF')
            self.alert=True
        if self.has_value('CO2'):
            # CO2=1234 => CO2 air quality
            try:
                self.co2alert = int(self.CO2)
            except:
                pass
            self.alert=True
        # ringer
        if self.has_value('CHIME'):
            #CHIME=123 => Chime/Doorbell melody number
            try:
                self.chime = int(self.CHIME)
            except:
                # probably not a number...
                pass
        # weather
        if self.has_value('TEMP'):
            # TEMP=9999 => Temperature (hexadecimal), high bit contains negative sign, needs division by 10 (0xC0 = 192 decimal = 19.2 degrees)
            try:
                self.temperature = htosi(self.TEMP)/10
            except:
                pass
        if self.has_value('HUM'):
            # HUM=99 => Humidity (decimal value: 0-100 to indicate relative humidity in %)
            try:
                self.humidity = int(self.HUM)
            except:
                pass
        if self.has_value('BARO'):
            # BARO=9999 => Barometric pressure (hexadecimal)
            try:
                self.pressure = int(self.BARO,16)
            except:
                pass
        if self.has_value('HSTATUS'):
            self.hstatus = int(self.HSTATUS)
            # HSTATUS=99 => 0=Normal, 1=Comfortable, 2=Dry, 3=Wet
            if self.hstatus==0:
                self.hstatus_desc="Normal"
            elif self.hstatus==1:
                self.hstatus_desc="Comfortable"
            elif self.hstatus==2:
                self.hstatus_desc="Dry"
            elif self.hstatus==3:
                self.hstatus_desc="Wet"
            else:
                self.hstatus_desc="Unknown"
                
        if self.has_value('BFORECAST'):
            # BFORECAST=99 => 0=No Info/Unknown, 1=Sunny, 2=Partly Cloudy, 3=Cloudy, 4=Rain
            try:
                self.forecast=int(self.BFORECAST)
                if self.forecast == 0:
                    self.forecast_desc = "No Info/Unknown"
                elif self.forecast == 1:
                    self.forecast_desc = "Sunny"
                elif self.forecast == 2:
                    self.forecast_desc = "Partly Cloudy"
                elif self.forecast == 3:
                    self.forecast_desc = "Cloudy"
                elif self.forecast == 4:
                    self.forecast_desc = "Rain"
                else:
                    self.forecast_desc = "Unknown"
            except:
                self.forecast_desc = "Error"
                pass
            
        if self.has_value('UV'):
            # UV=9999 => UV intensity (hexadecimal)
            try:
                self.uv = int(self.UV,16)
            except:
                pass
        if self.has_value('LUX'):
            # LUX=9999 => Light intensity (hexadecimal)
            try:
                self.lux = int(self.LUX,16)
            except:
                pass
        if self.has_value('RAIN'):
            # RAIN=1234 => Total rain in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.rain = int(self.RAIN,16)/10
            except:
                pass
        if self.has_value('RAINTOT'):
            # RAINTOT=1234 => Total rain in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.raintot = int(self.RAINTOT,16)/10
            except:
                pass
        if self.has_value('RAINRATE'):
            # RAINRATE=1234 => Rain rate in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.rainrate = int(self.RAINRATE,16)/10
            except:
                pass
        if self.has_value('WINSP'):
            # WINSP=9999 => Wind speed in km. p/h (hexadecimal) needs division by 10
            try:
                self.windspeed = int(self.WINSP,16)/10
            except:
                pass
        if self.has_value('AWINSP'):
            # AWINSP=9999 => Average Wind speed in km. p/h (hexadecimal) needs division by 10
            try:
                self.awindspeed = int(self.AWINSP,16)/10
            except:
                pass
        if self.has_value('WINGS'):
            # WINGS=9999 => Wind Gust in km. p/h (hexadecimal)
            try:
                self.windgust = int(self.WINGS,16)/10
            except:
                pass
        if self.has_value('WINDIR'):
            # WINDIR=123 => Wind direction (integer value from 0-15) reflecting 0-360 degrees in 22.5 degree steps
            try:
                self.winddirection = int(self.WINDIR) * 22.5
            except:
                pass
        if self.has_value('WINCHL'):
            # WINCHL => wind chill (hexadecimal, see TEMP)
            try:
                self.windchill = htosi(self.WINCHL)/10
            except:
                pass
        if self.has_value('WINTMP'):
            # WINTMP=1234 => Wind meter temperature reading (hexadecimal, see TEMP)
            try:
                self.windtemp = htosi(self.WINTMP)/10
            except:
                pass
                
    def get_command(self):
        raise Exception('Method get_command not supported for SensorEvent!')
                
    def device(self):
        return RFLinkSensorDevice(name=self.name, id=self.id, deviceid=self.deviceid(), rflink=self.rflink)
    def deviceid(self):
        if self.__deviceid==None:
            if self.has_value('switch'):
                self.__deviceid = RFLinkDevice.get_deviceid(self.name, self.id, self.switch)
            else:
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id)
                
        return self.__deviceid
        
    def supported_datatypes(self):
        dt={}
        for datatype, properties in self.data_types.items():
            if self.has_value(datatype):
                dt[datatype] = properties
        return dt
    
    
    def __str__(self):
        str = ""
        for datatype, properties in self.data_types.items():
            if self.has_value(datatype):
                str +=", {0}={1}{2}".format(datatype, self.value(datatype), properties['unit_of_measurement'])
        
        return super().__str__().replace('RFLinkEvent','SensorEvent') + str
        
"""
class MeterEvent(SensorEvent):
    #  Base class for meter related events
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('METER'):
            # METER=1234 => Meter values (water/electricity etc.)
            try:
                self.meter = int(self.METER)
            except: 
                pass
    def __str__(self):
        return "MeterEvent Meter={0}, {1}".format(self.meter , super().__str__().replace('SensorEvent', '')) 
               
class DistanceEvent(SensorEvent):
    # Base class for distance related events
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('DIST'):
            # DIST=1234 => Distance
            try:
                self.distance = int(self.DIST)
            except: 
                pass
    def __str__(self):
        return "DistanceEvent distance={0}, {1}".format(self.distance , super().__str__().replace('SensorEvent', '')) 
       
class ElectricEvent(SensorEvent):
    # Base class for electric related events
    
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        # 'KWATT=','WATT=','CURRENT=','CURRENT2=','CURRENT3=','VOLT='
        if self.has_value('KWATT'):
            # KWATT=9999 => KWatt (hexadecimal)
            try:
                self.watt = int(self.KWATT,16) * 1000
            except: 
                pass
        if self.has_value('WATT'):
            # WATT=9999 => Watt (hexadecimal)
            try:
                self.watt = int(self.WATT,16)
            except:
                pass
        if self.has_value('CURRENT'):
            # CURRENT=1234 => Current phase 1
            try:
                self.current = int(self.CURRENT)
            except:
                pass
        if self.has_value('CURRENT2'):
            # CURRENT2=1234 => Current phase 2 (CM113)
            try:
                self.current2 = int(self.CURRENT2)
            except:
                pass
        if self.has_value('CURRENT3'):
            # CURRENT2=1234 => Current phase 3 (CM113)
            try:
                self.current3 = int(self.CURRENT3)
            except:
                pass
        if self.has_value('VOLT'):
            # VOLT=1234 => Voltage
            try:
                self.volt = int(self.VOLT)
            except:
                pass

    def __str__(self):
        props=''
        if self.has_value('watt'):
            # WATT=9999 => Watt (hexadecimal)
            props += "watt={0}".format(self.watt)
        if self.has_value('current'):
            # CURRENT=1234 => Current phase 1
            props += "current={0}".format(self.current)
        if self.has_value('current2'):
            # CURRENT2=1234 => Current phase 2 (CM113)
            props += "current2={0}".format(self.current2)
        if self.has_value('current3'):
            # CURRENT2=1234 => Current phase 3 (CM113)
            props += "current3={0}".format(self.current3)
        if self.has_value('volt'):
            # VOLT=1234 => Voltage
            props += "volt={0}".format(self.volt)
            
        return "ElectricEvent {0}, {1}".format(props , super().__str__().replace('SensorEvent', '')) 
      
class SoundEvent(SensorEvent):
    # Base class for sound related events
    
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('SOUND'):
            # SOUND=1234 => Noise level
            try:
                self.noiselevel = int(self.SOUND)
            except:
                pass
    def __str__(self):
        return "SoundEvent noiselevel={0}, {1}".format(self.noiselevel , super().__str__().replace('SensorEvent', '')) 
     
class AlarmEvent(SensorEvent):
    # Base class for alarm related events     (SMOKEALERT, CO2=, PIR)
    
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('SMOKEALERT'):
            # SMOKEALERT=ON => ON/OFF
            self.smokealert = (self.SMOKEALERT!='OFF')
            self.alert=True
        if self.has_value('PIR'):
            # PIR=ON => ON/OFF
            self.movementalert = (self.PIR!='OFF')
            self.alert=True
        if self.has_value('PIR'):
            # CO2=1234 => CO2 air quality
            try:
                self.co2alert = int(self.CO2)
            except:
                pass
            self.alert=True
    
    def __str__(self):
        props=''
        if self.has_value('smokealert'):
            # SMOKEALERT=ON => ON/OFF
            props+="smokealert={0} ".format(self.smokealert )
        if self.has_value('movementalert'):
            # PIR=ON => ON/OFF
            props+="movementalert={0} ".format(self.movementalert)
        if self.has_value('co2alert'):
            # CO2=1234 => CO2 air quality
            props+="co2alert={0} ".format(self.co2alert)
        props+="alert={0} ".format(self.alert)
    
        return "AlarmEvent {0}, {1}".format(props , super().__str__().replace('SensorEvent', '')) 

class RingerEvent(SensorEvent):
    # Base class for ringer related events

    def __init__(self):
        super().__init__()
    
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('CHIME'):
            #CHIME=123 => Chime/Doorbell melody number
            try:
                self.chime = int(self.CHIME)
            except:
                # probably not a number...
                pass

    def __str__(self):            
        return "RingerEvent chime={0}, {1}".format(self.chime, super().__str__().replace('SensorEvent', ''))         

class WeatherEvent(SensorEvent):
    # Base class for all weather related events (temperature, humidity, pressure, rain, etc.)
    
    def __init__(self):
        super().__init__()
    
    def load_receive(self, data):
        super().load_receive(data);
    
        if self.has_value('TEMP'):
            # TEMP=9999 => Temperature (hexadecimal), high bit contains negative sign, needs division by 10 (0xC0 = 192 decimal = 19.2 degrees)
            try:
                self.temperature = htosi(self.TEMP)/10
            except:
                pass
        if self.has_value('HUM'):
            # HUM=99 => Humidity (decimal value: 0-100 to indicate relative humidity in %)
            try:
                self.humidity = int(self.HUM)
            except:
                pass
        if self.has_value('BARO'):
            # BARO=9999 => Barometric pressure (hexadecimal)
            try:
                self.pressure = int(self.BARO,16)
            except:
                pass
        if self.has_value('HSTATUS'):
            self.hstatus = int(self.HSTATUS)
            # HSTATUS=99 => 0=Normal, 1=Comfortable, 2=Dry, 3=Wet
            if self.hstatus==0:
                self.hstatus_desc="Normal"
            elif self.hstatus==1:
                self.hstatus_desc="Comfortable"
            elif self.hstatus==2:
                self.hstatus_desc="Dry"
            elif self.hstatus==3:
                self.hstatus_desc="Wet"
            else:
                self.hstatus_desc="Unknown"
                
        if self.has_value('BFORECAST'):
            # BFORECAST=99 => 0=No Info/Unknown, 1=Sunny, 2=Partly Cloudy, 3=Cloudy, 4=Rain
            try:
                self.forecast=int(self.BFORECAST)
                if self.forecast == 0:
                    self.forecast_desc = "No Info/Unknown"
                elif self.forecast == 1:
                    self.forecast_desc = "Sunny"
                elif self.forecast == 2:
                    self.forecast_desc = "Partly Cloudy"
                elif self.forecast == 3:
                    self.forecast_desc = "Cloudy"
                elif self.forecast == 4:
                    self.forecast_desc = "Rain"
                else:
                    self.forecast_desc = "Unknown"
            except:
                self.forecast_desc = "Error"
                pass
            
        if self.has_value('UV'):
            # UV=9999 => UV intensity (hexadecimal)
            try:
                self.uv = int(self.UV,16)
            except:
                pass
        if self.has_value('LUX'):
            # LUX=9999 => Light intensity (hexadecimal)
            try:
                self.lux = int(self.LUX,16)
            except:
                pass
        if self.has_value('RAIN'):
            # RAIN=1234 => Total rain in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.rain = int(self.RAIN,16)/10
            except:
                pass
        if self.has_value('RAINTOT'):
            # RAINTOT=1234 => Total rain in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.raintot = int(self.RAINTOT,16)/10
            except:
                pass
        if self.has_value('RAINRATE'):
            # RAINRATE=1234 => Rain rate in mm. (hexadecimal) 0x8d = 141 decimal = 14.1 mm (needs division by 10)
            try:
                self.rainrate = int(self.RAINRATE,16)/10
            except:
                pass
        if self.has_value('WINSP'):
            # WINSP=9999 => Wind speed in km. p/h (hexadecimal) needs division by 10
            try:
                self.windspeed = int(self.WINSP,16)/10
            except:
                pass
        if self.has_value('AWINSP'):
            # AWINSP=9999 => Average Wind speed in km. p/h (hexadecimal) needs division by 10
            try:
                self.awindspeed = int(self.AWINSP,16)/10
            except:
                pass
        if self.has_value('WINGS'):
            # WINGS=9999 => Wind Gust in km. p/h (hexadecimal)
            try:
                self.windgust = int(self.WINGS,16)/10
            except:
                pass
        if self.has_value('WINDIR'):
            # WINDIR=123 => Wind direction (integer value from 0-15) reflecting 0-360 degrees in 22.5 degree steps
            try:
                self.winddirection = int(self.WINDIR) * 22.5
            except:
                pass
        if self.has_value('WINCHL'):
            # WINCHL => wind chill (hexadecimal, see TEMP)
            try:
                self.windchill = htosi(self.WINCHL)/10
            except:
                pass
        if self.has_value('WINTMP'):
            # WINTMP=1234 => Wind meter temperature reading (hexadecimal, see TEMP)
            try:
                self.windtemp = htosi(self.WINTMP)/10
            except:
                pass
    
    def __str__(self):
        props=''
        
        if self.has_value('temperature'):
            props+= "temperature={0} ".format(self.temperature)
        if self.has_value('humidity'):
            props+= "humidity={0} ".format(self.humidity)
        if self.has_value('pressure'):
            props+= "pressure={0} ".format(self.pressure)
        if self.has_value('hstatus'):
            props+= "hstatus={0} hstatus_desc={1}".format(self.hstatus, self.hstatus_desc)
        if self.has_value('forecast'):
            props+= "forecast={0} forecast_desc={1}".format(self.forecast, self.forecast_desc)
        if self.has_value('uv'):
            props+= "uv={0} ".format(self.uv)
        if self.has_value('lux'):
            props+= "lux={0} ".format(self.lux)
        if self.has_value('rain'):
            props+= "rain={0} ".format(self.rain)
        if self.has_value('raintot'):
            props+= "raintot={0} ".format(self.raintot)
        if self.has_value('rainrate'):
            props+= "rainrate={0} ".format(self.rainrate)
        if self.has_value('windspeed'):
            props+= "windspeed={0} ".format(self.windspeed)
        if self.has_value('awindspeed'):
            props+= "awindspeed={0} ".format(self.awindspeed)
        if self.has_value('windgust'):
            props+= "windgust={0} ".format(self.windgust)
        if self.has_value('winddirection'):
            props+= "winddirection={0} ".format(self.winddirection)
        if self.has_value('windchill'):
            props+= "windchill={0} ".format(self.windchill)
        if self.has_value('windtemp'):
            props+= "windtemp={0} ".format(self.windtemp)
        return "WeatherEvent {0}, {1}".format(props, super().__str__().replace('SensorEvent', '')) 
        
"""

class SwitchEvent(RFLinkEvent):
    """
    Base class for switch related events
    """
    def __init__(self):
        super().__init__()
        self.__deviceid=None
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('SWITCH'):
            # SWITCH=A16 => House/Unit code like A1, P2, B16 or a button number etc.
            self.switch = self.SWITCH

        if self.has_value('CMD'):
            # CMD=ON => Command (ON/OFF/ALLON/ALLOFF) Additional for Milight: DISCO+/DISCO-/MODE0 - MODE8    
            if (self.CMD=="ON" or self.CMD=="ALLON"):
                if self.name=='FA500' and self.switch=='00':
                    self.allon = True
                else:
                    self.on = True
            else:
                if self.name=='FA500' and self.switch=='00':
                    self.allon = False
                else:
                    self.on = False
            
            if 'MODE' in self.CMD:
                self.mode = self.CMD.replace('MODE','')
                try:
                    self.mode = int(self.mode)
                except:
                    # unable to convert
                    pass

            if self.CMD=='DISCO+':
                self.disco=True
            if self.CMD=='DISCO-':
                self.disco=False

    def get_command(self):
        cmd = "10;{0};{1};{2};{3};".format(self.name, self.id, self.switch, self.CMD)
        return cmd
        
    def device(self):
        if self.has_value('switch'):
            return RFLinkSwitchDevice(name=self.name,id=self.id, switch=self.switch,deviceid=self.deviceid(), rflink=self.rflink)
        else:
            return RFLinkSwitchDevice(name=self.name,id=self.id, switch=self.switch,deviceid=self.deviceid(), rflink=self.rflink)
    def deviceid(self):
        if self.__deviceid==None:
            if self.has_value('switch'):
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id,self.switch)
            else:
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id)
        return self.__deviceid
        
    def __str__(self):
        props=''
        if self.has_value('mode'):
            props+="mode={0} ".format(self.mode)
        if self.has_value('disco'):
            props+="disco={0}".format(self.disco)
        if self.has_value('switch'):
            props+="switch={0} ".format(self.switch)
        if self.has_value('on'):
            props+="on={0}".format(self.on)
        if self.has_value('allon'):
            props+="allon={0} ".format(self.allon)
        
        return "SwitchEvent {0} {1}".format(props, super().__str__().replace('RFLinkEvent', '')) 
    
class RollerEvent(RFLinkEvent):
    """
    Base class for roller related events (up/down)
    """
    def __init__(self):
        super().__init__()
        self.__deviceid=None
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('SWITCH'):
            # SWITCH=A16 => House/Unit code like A1, P2, B16 or a button number etc.
            self.switch = self.SWITCH

        if self.has_value('CMD'):
            # CMD=ON => Command (ON/OFF/ALLON/ALLOFF) Additional for Milight: DISCO+/DISCO-/MODE0 - MODE8    
            if self.CMD=="UP":
                self.up = True
            else:
                self.up = False
    
    def get_command(self):
        cmd = "10;{0};{1};{2};{3};".format(self.name, self.id, self.switch, self.CMD)
        return cmd
    
    def device(self):
        if self.has_value('switch'):
            return RFLinkRollerDevice(name=self.name, id=self.id, switch=self.switch, deviceid=self.deviceid(), rflink=self.rflink)
        else:
            return RFLinkRollerDevice(name=self.name, id=self.id, deviceid=self.deviceid(), rflink=self.rflink)
    def deviceid(self):
        if self.__deviceid==None:
            if self.has_value('switch'):
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id,self.switch)
            else:
                self.__deviceid = RFLinkDevice.get_deviceid(self.name,self.id)
        return self.__deviceid    
    def __str__(self):
        props=''
        if self.has_value('switch'):
            props+="switch={0} ".format(self.switch)
        if self.has_value('up'):
            props+="up={0}".format(self.up)
        
        return "RollerEvent {0} {1}".format(props, super().__str__().replace('RFLinkEvent', '')) 

class LightEvent(SwitchEvent):
    """
    Base class for light related events
    
    adds:
    - brightness : int 0-100%
    - color :      int 0-255  -> TODO: meaning unknown for now...
    """
    def __init__(self):
        super().__init__()
    def load_receive(self, data):
        super().load_receive(data);
        
        if self.has_value('RGBW'):
            # RGBW=9999 => Milight: provides 1 byte color and 1 byte brightness value
            try:
                self.color = int(self.RGBW[:2],16)
            except:
                pass
            try:
                self.brightness = int(self.RGBW[2:],16)*100/255
            except:
                pass
                
        if self.has_value('SET_LEVEL') or (self.has_value('CMD') and 'SET_LEVEL' in self.CMD):
            # SET_LEVEL=15 => Direct dimming level setting value (decimal value: 0-15)
            if self.has_value('SET_LEVEL'):
                self.brightness = int(self.SET_LEVEL)*100/15
            if (self.has_value('CMD') and 'SET_LEVEL' in self.CMD):
                self.brightness = int(self.CMD.replace('SET_LEVEL=','')) * 100/15
    
    def get_command(self):
        if self.has_value('RGBW'):
            cmd = "10;{0};{1};{2};{3};{4};".format(self.name, self.id, self.switch, self.RGBW, self.CMD)
        else:
            if 'SET_LEVEL=' in self.CMD:
                lvl = self.CMD.split('=')
                cmd = "10;{0};{1};{2};{3};".format(self.name, self.id, self.switch, lvl[1])
            else:
                cmd = "10;{0};{1};{2};{3};".format(self.name, self.id, self.switch, self.CMD)
        return cmd
    
    def device(self):
        if self.has_value('switch'):
            return RFLinkLightDevice(name=self.name,id=self.id, switch=self.switch,deviceid=self.deviceid(), rflink=self.rflink)
        else:
            return RFLinkLightDevice(name=self.name,id=self.id, switch=self.switch,deviceid=self.deviceid(), rflink=self.rflink)
            
    def __str__(self):
        props=''
        if self.has_value('color'):
            props+="color={0} ".format(self.color)
        if self.has_value(',self.brightness'):
            props+="brightness={0} ".format(self.brightness)
        
        return "LightEvent {0}, {1}".format(props, super().__str__().replace('SwitchEvent', '')) 
       
                   
