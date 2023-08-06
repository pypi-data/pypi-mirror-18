echo create folder
sudo mkdir /home/pi/ci_cc

echo copy starscript
sudo cp /usr/local/lib/python2.7/dist-packages/CI_CloudConnector/runCloudConnector.sh /home/pi/ci_cc

sudo chmod 755 /home/pi/ci_cc/runCloudConnector.sh
#sudo chown root:root /home/pi/ci_cc/runCloudConnector.sh

echo copy autostartScript to init.d
sudo cp /usr/local/lib/python2.7/dist-packages/CI_CloudConnector/ci_cloudConnectorService /etc/init.d
sudo chmod 755 /etc/init.d/ci_cloudConnectorService
#sudo chown root:root /etc/init.d/ci_cloudConnectorService
sudo update-rc.d ci_cloudConnectorService  remove
sudo update-rc.d ci_cloudConnectorService defaults




