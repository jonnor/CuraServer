CuraServer
===========
[![Build Status](https://travis-ci.org/jonnor/CuraServer.png?branch=master)](https://travis-ci.org/jonnor/CuraServer)

Provides a HTTP API for slicing 3d-models, using the same backend as [Cura](http://github.com/daid/Cura).

Required to use [noflo-3dprint](http://github.com/jonnor/noflo-3dprint) slicing components.

Install & Run
--------
Note: only tested on GNU/Linux :)

Install Cura from http://software.ultimaker.com or your distro.

Install Python modules

    pip install -r requirements.txt # Or get from your distro

Run

    python2 cura-server.py

Open http://localhost:8888 to see the trivial API demo

License
-------
Affero GPL, like Cura itself.
