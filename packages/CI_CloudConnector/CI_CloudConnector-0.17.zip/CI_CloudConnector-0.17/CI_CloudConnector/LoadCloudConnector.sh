
#!/bin/sh

cd /

cd /home/pi/CI_Projects
export PATH="$PATH:/usr/lib/python2.7:/usr/lib/python2.7/plat-arm-linux-gnueabihf:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/home/pi/.local/lib/python2.7/site-packages:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PILcompat:/usr/lib/python2.7/dist-packages/gtk-2.0:/usr/lib/pymodules/python2.7"

sudo python CI_CloudConnector.py Start

cd /