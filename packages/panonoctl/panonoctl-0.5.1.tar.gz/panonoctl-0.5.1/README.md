panonoctl
========

Python API to interact with the [PANONO](https://www.panono.com) 360-camera.

Install
=======

To install, execute:

```
pip install panonoctl
```

Documentation
=============

### Status
[panonoctl](https://github.com/florianl/panonoctl) is tested under API version 3.8.

### Connect
```python
>>> from panonoctl import panono
>>> cam = panono()
>>> cam.connect()
```

### Authenticate
```python
>>> cam.auth()
```
You need to authenticate. Otherwise your commands will _not_ be executed.

### Take a Picture
```python
>>> cam.capture()
```

### Get the status of your Panono.
```python
>>> cam.getStatus()
```
Returns a JSON object.

### Get the options of your Panono.
```python
>>> cam.getOptions()
```
Returns a JSON object.

### Get the UPFs (Unstitched Panorama Format) from your Panono.
```python
>>> cam.getUpfs()
```
Returns a JSON object.

### Disconnect
```python
>>> cam.disconnect()
```

### Other Features
[PANONO](https://www.panono.com) provides more features, than those listed above.
If you are interested in trying your own commands take a look [here](Experimental.md) for further information.

License
=======

Copyright 2016 Florian Lehner

Licensed under the Apache License, Version 2.0: [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
