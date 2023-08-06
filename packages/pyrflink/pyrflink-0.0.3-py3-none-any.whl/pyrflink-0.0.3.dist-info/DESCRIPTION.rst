A Python library for interfacing with RFLink hardware
=====================================================

This project contains a library and examples/tools for interacting with 
RFlink 433MHz transceiver.

For details regarding the RFLink hardware, see the RFLink website 
at http://www.nemcon.nl/blog2/ .

Using this library you can create  your own applications built on top of 
the RFLink tranceiver, create RF repeaters or integrate with Homeautomation 
systems.

Installation
------------

.. code-block:: bash

    $ pip install pyrflink


Version History
---------------
Version  Date       Changes
--------------------------------------------------------------------------
0.0.3    20161208   NEW: allow additional init commands on connect (to enable/disable RFLink protocols, for example)
                    CHANGED: incorrect conversion of subzero temperatures
                    CHANGED: renaming issues
                    CHANGED: Changed level of some log messages to debug
                    CHANGED: Improved Roller/Shutter detection
0.0.2    20161205   CHANGED: Renamed to pyrflink to prevent clash with rflinkpackage
0.0.1    20161205   NEW: Initial version


