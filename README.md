QoSReflect
==========

Current Status: BETA  
A simple Python Script that just bounces all incoming UDP Packets which can be used as endpoint for PRTG's QoS Roundtrip Sensor.  
At the moment this works only from a machine a MiniProbe is announced from. From the upcoming Preview version of PRTG it will be possible to define custom targets for QoS RTT sensors. 


Prerequisites
-----------------
Linux OS  
Python 2.7+  

Installation
------------
- make the file "qosreflect.py" executable (e.g. "chmod 755 qosreflect.py")
- [OPTIONAL]create a file called "qosreflect.conf" with the following contents:

host:All  
port:50000  
replyip:None  

The script can now be called with parameters to allow several instances running. Just type qosreflect.py --help to see all parameters.
Example call below:

qosreflect.py --port 50000 --host All

Additional parameters are optional. You can still use a config file, then please use parameter --conf to provide the path.

When "host" is set to "All" the script will try to bind to every available interface. Change to IP of an interface to make 
the script bind to a special interface.  
Set "port" to the same one set up in PRTG.  
If an IP is specified in "replyip" the script will only process UDP packets from this IP.  

Debugging
---------
To debug whats going on call the script with the additional parameter -d or --debug