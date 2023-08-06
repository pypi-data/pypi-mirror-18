from distutils.core import setup
setup(name='CI_CloudConnector',
      version='0.15',
      py_modules=['CI_CloudConnector' , 'CI_LC_BL'],
	  package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
	  },
	  include_package_data = True,
	  description="IOT application that collect data from PLC (ModBus or AnB Ethernet/IP) and send to cloud using https",
	  author="Ido Peles",
	  author_email="idop@contel.co.il",
          install_requires=['pymodbus' , 'cpppo'],
      )
	  
