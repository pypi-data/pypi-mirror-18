APIdou - Python communication with APIdou
========================================================================
This module based on PyGATT (by Chris Peplin) makes easier to communicate
over BLE with APIdou, the connected plush (www.apidou.fr).

Example code :
```python
from apidou import APIdou
# create an APIdou object using gatttool and a given MAC address
device = APIdou("linux", "AA:BB:CC:DD:EE:FF")
device.connect()

device.setVibration(True)
time.sleep(0.1)
device.setVibration(False)

device.disconnect()
```

More examples on the [other repository](https://github.com/iadjedj/APIdouExamples/tree/master/python)
