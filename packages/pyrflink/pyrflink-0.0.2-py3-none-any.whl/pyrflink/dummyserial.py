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
import RFLink 
from threading import Event
import os

        
class RFLinkDummySerial(object):
    """ Dummy serial class for testing"""
    def __init__(self, device):
        if device.startswith('test:'):
            filepath = device[5:]
            
            if os.path.isfile(filepath):
                self._device = device
                self._filepath = filepath
            else:
                raise Exception("Illegal device ({0}); File does not exist ({1}).".format(device, filepath))
        else:
            raise Exception("Illegal device; device must start with 'test:' ({0})".format(device))
            
        self._read_num = 0
        self.timeout = 1
        self.is_open = True
        self.__define_data()
        
        self.queue = []
        self.event = Event()
        
        if len(self.queue)==0:
            self.__fill_queue()
            # generic version string
            self.queue.insert(0,"20;0;RFLinkDummySerial2 VersionString\r\n".encode('utf-8'))
    
    def write(self, data):
        """Dummy function for writing to the 'port'."""
        str = data.decode('utf-8')
        
        specials = ['VERSION', 'PING' ]
        response = ['20;12;VER=0.1;REV=a;BUILD=1;\r\n','20;12;PONG;\r\n']
        
        for i in range(len(specials)):
            if specials[i] in str:
                # add response to front of the response queue:
                self.queue.insert(0,response[i].encode('utf-8'))
                return
        
    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        if len(self.queue)==0:
            self.__fill_queue()
        return len(self.queue[0])
                
    def read(self, size=1):
        """ Dummy function for reading"""
        self.event.wait(1)
        
        if self.event.is_set():
            self.event.clear()
        
        return self.queue.pop(0)
            
    def close(self):
        """ close connection to rflink device """
        self.event.set()
        self.is_open = False
    
    def __fill_queue(self):
        if len(self.queue)<10:
            for element in self.data:
                self.queue.append(element)
        
    def __define_data(self):
        """ Define the data the dummy serial port will 'read'... """
        self.data=[]
        with open(self._filepath, 'r') as ins:
            for line in ins:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.data.append(line)
                        
        # encode into bytes:
        for i in range(len(self.data)):
            if not self.data[i].endswith("\r\n"):
                self.data[i] += "\r\n"
            self.data[i] = self.data[i].encode('utf-8')
        
        
