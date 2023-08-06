=================================
BITalino (R)evolution Python API
=================================
The BITalino (R)evolution Python API provides the needed tools to interact with BITalino (R)evolution using Python.

Dependencies
-------------

* `Python >2.7 <https://www.python.org/downloads/>`_ or `Anaconda <https://www.continuum.io/downloads>`_
* `NumPy <https://pypi.python.org/pypi/numpy/>`_
* `pySerial <https://pypi.python.org/pypi/pyserial>`_
* `pyBluez <https://pypi.python.org/pypi/PyBluez/>`_

Installation
-------------
``pip install bitalino``

Usage Example
--------------
use your macAddress::
	
	# This example will collect data for 5 sec.
	macAddress = "00:00:00:00:00:00"
	running_time = 5
		
	batteryThreshold = 30
	acqChannels = [0, 1, 2, 3, 4, 5]
	samplingRate = 1000
	nSamples = 10
	digitalOutput = [1,1]

	# Connect to BITalino
	device = BITalino(macAddress)

	# Set battery threshold
	print device.battery(batteryThreshold)

	# Read BITalino version
	device.version()
		
	# Start Acquisition
	device.start(samplingRate, acqChannels)

	start = time.time()
	end = time.time()
	while (end - start) < running_time:
		# Read samples
		print device.read(nSamples)
		end = time.time()

	# Turn BITalino led on
	device.trigger(digitalOutput)
		
	# Stop acquisition
	device.stop()
		
	# Close connection
	device.close()
