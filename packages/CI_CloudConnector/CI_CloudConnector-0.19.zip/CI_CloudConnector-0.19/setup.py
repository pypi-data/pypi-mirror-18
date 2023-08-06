from distutils.core import setup
setup(name='CI_CloudConnector',
      version='0.19',
      py_modules=['CI_CloudConnector' , 'CI_LC_BL'],
	  packages=['CI_CloudConnector',],
	  package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['ci_cloudConnectorService', 'runCloudConnector.sh', 'SetupCloudConnector.sh']
	  },
	  include_package_data = True,
	  description="IOT application that collect data from PLC (ModBus or AnB Ethernet/IP) and send to cloud using https",
	  author="Ido Peles",
	  author_email="idop@contel.co.il",
      install_requires=['pymodbus' , 'cpppo'],
	  url = "http://www.contel.co.il/en/",
	  long_description=open('README.txt').read(),
      )
	  
