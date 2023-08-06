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
This module allows testing of RFLink hardware and/or allows you to test
with a simulated RFLink.

To run:
    py  example.py device [log]

    where
      device : the device to use to connect to the RFLink device,
               such as 'COM3', '/dev/ttyUSB-RFLink', etc.
               to simulate an RFLink device, use 'test:<filepath>'
               (do not enter the quotes).
               filepath : path to a file of rflink events; these events will 
                          be 'received' one at a time. Specifty one event per line.
      log    : log level; allowed values: error, warning, info, debug

"""
from __future__ import division
import pyrflink
import logging
import sys
import time


def getLogger(name=None):
    if name:
        return logging.getLogger("{0}.{1}".format(__name__, name))
    else:
        return logging.getLogger(__name__)
        
class __RFLCallback(object):
    def __init__(self):
        super().__init__()
        self.devices = {}
        
    def list_devices(self):
        msg = "Devices:\n"
        for key, device in self.devices.items():
            msg += "{0} : {1}\n".format(key,str(device))
        
        getLogger(self.__class__.__name__).info(msg)
        
    def onRFLinkException(self, exc):
        """ 
        called with an instance of RFLinkException
        """
        try:
            raise exc
        except: 
            getLogger(self.__class__.__name__).exception("Exception received!")
        
    def onRFLinkEvent(self, event):
        """
        Called with an instance of RFLinkEvent
        """
        getLogger(self.__class__.__name__).info(str(event))
        
        try:
            deviceid = event.deviceid()
            if deviceid:
                dev = event.device()
                if isinstance(dev, pyrflink.lowlevel.RFLinkLightDevice):
                    self.devices["light_{0}".format(deviceid)] = event.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkSwitchDevice):
                    self.devices["switch_{0}".format(deviceid)] = event.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkSensorDevice):
                    self.devices["sensor_{0}".format(deviceid)] = event.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkRollerDevice):
                    self.devices["roller_{0}".format(deviceid)] = event.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkDevice):
                    self.devices["device_{0}".format(deviceid)] = event.device()
        except:
            pass
            
    def onRFLinkCommand(self, cmd):
        """
        Called with an instance of RFLinkCommand
        """
        getLogger(self.__class__.__name__).info(str(cmd))
        try:
            deviceid = cmd.deviceid()
            if deviceid:
                dev = cmd.device()
                if isinstance(dev, pyrflink.lowlevel.RFLinkLightDevice):
                    self.devices["light_{0}".format(deviceid)] = cmd.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkSwitchDevice):
                    self.devices["switch_{0}".format(deviceid)] = cmd.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkSensorDevice):
                    self.devices["sensor_{0}".format(deviceid)] = cmd.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkRollerDevice):
                    self.devices["roller_{0}".format(deviceid)] = cmd.device()
                elif isinstance(dev, pyrflink.lowlevel.RFLinkDevice):
                    self.devices["device_{0}".format(deviceid)] = cmd.device()
        except:
            getLogger(self.__class__.__name__).exception("ERROR! {0}".format(str(cmd)))
            #pass

    def onRFLinkPacket(self, pkt):
        """
        Called with an instance of RFLinkPacket
        """
        getLogger(self.__class__.__name__).info(str(pkt))

def usage():
    print("Usage:")
    print("  {0} device [log]".format(sys.argv[0]))
    print(" ")
    print("  where")
    print("  device : the device to use to connect to the RFLink device,")
    print("           such as 'COM3', '/dev/ttyUSB-RFLink', etc.")
    print("           to simulate an RFLink device, use 'test:<filepath>'")
    print("           (do not enter the quotes).")
    print("  log    : log level; allowed values: error, warning, info, debug")
    exit(1)
    
def main():   
    if len(sys.argv)<2:
        usage()
    
    device = sys.argv[1]
    
    lvl = logging.ERROR
    if len(sys.argv)>1:
        if sys.argv[2] in "error|warning|info|debug":
            # valid logging level
            levels  = {'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}
            lvl=levels[sys.argv[2]]
    
    FORMAT = '%(asctime)-15s  %(levelname)8s %(filename)s:%(name)s:%(funcName)s:  %(message)s'
    logging.basicConfig(format=FORMAT, level=lvl)

    cb = __RFLCallback()
    RFLinkObject = pyrflink.Connect(device, reconnect=True, event_callback=cb, connect=False)
    RFLinkObject.connect()
    
    while True:
        try:
            time.sleep(5)
            cb.list_devices()
        except KeyboardInterrupt:
            getLogger().info('Keyboard interrupt; closing connections...')
            RFLinkObject.close_connection()
            break
        except:
            getLogger().exception("An error occurred!")
        
            
if __name__ == "__main__":
    main()  