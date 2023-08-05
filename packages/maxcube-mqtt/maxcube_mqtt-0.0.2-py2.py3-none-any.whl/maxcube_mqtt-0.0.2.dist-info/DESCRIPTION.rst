Copyright (c) 2015 David Übelacker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Description: eQ-3/ELV MAX! Cube MQTT
        =============================
        
        Control your eQ-3/ELV MAX! Cube with MQTT
        
        
        Installation:
        -------------------
        
            pip install maxcube-mqtt
        
        Configuration:
        -------------------
        
        Needs a json configuration file as follows (don't forget to change ip's and credentials ;-)):
        
        .. code:: json
        
            {
                "cube_host": "192.168.0.20",
                "cube_port": "62910",
                "mqtt_client_id": "maxcube",
                "mqtt_host": "192.168.0.210",
                "mqtt_port": "1883",
                "mqtt_user": "192.168.0.210",
                "mqtt_password": "1883",
                "mqtt_topic_prefix": "halti"
            }
        
        
        
        Start:
        -------------------
        
            maxcube-mqtt config.json
        
Platform: UNKNOWN
