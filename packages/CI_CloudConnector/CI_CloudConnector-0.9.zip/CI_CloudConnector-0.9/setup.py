from distutils.core import setup
setup(name='CI_CloudConnector',
      version='0.9',
      py_modules=['CI_CloudConnector' , 'CI_LC_BL'],
	  description="IOT application that collect data from PLC (ModBus or AnB Ethernet/IP) and send to cloud using https",
	  author="Ido Peles",
	  author_email="idop@contel.co.il",
          install_requires=['pymodbus' , 'cpppo', 'logging'],
      )
	  
