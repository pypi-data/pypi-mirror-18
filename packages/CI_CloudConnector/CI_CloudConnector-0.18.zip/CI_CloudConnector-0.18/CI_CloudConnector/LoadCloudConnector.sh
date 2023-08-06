
#!/bin/sh

### BEGIN INIT INFO
# Provides: CI_CloudConnector
# Required-Start: 
# Required-Stop: 
# Should-Start: 
# Should-Stop: 
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start and stop CI_CloudConnector
# Description: CI_CloudConnector
### END INIT INFO

cd /
cd /usr/local/lib/python2.7/dist-packages/
export PATH="$PATH:/usr/lib/python2.7:/usr/lib/python2.7/plat-arm-linux-gnueabihf:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/home/pi/.local/lib/python2.7/site-packages:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PILcompat:/usr/lib/python2.7/dist-packages/gtk-2.0:/usr/lib/pymodules/python2.7"

sudo python CI_CloudConnector.py StartMainLoop
