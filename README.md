CuraServer
===========
[![Build Status](https://travis-ci.org/jonnor/CuraServer.png?branch=master)](https://travis-ci.org/jonnor/CuraServer)

Provides a HTTP API for slicing 3d-models, using the same backend as [Cura](http://github.com/daid/Cura).
This allows the slicing to happen on a more powerful computer, great for embedded or mobile use.

Pre-requisite for to using [noflo-3dprint](http://github.com/jonnor/noflo-3dprint) slicing components.

Note: This project does not aim to provide an API for the printer control parts of Cura (only slicing).
Instead use [OctoPrint](https://github.com/foosel/OctoPrint) for that.

Status
-------
**UNMAINTAINED DEMO**.

* Not updated since 2014
* No API authentication
* Probably broken with newer Cura/CuraEngine versions

Use the code however you see fit.
If you want help to build a web-enabled 3d-printer slicer, I am available for consulting.

Install & Run
--------
Note: only tested on GNU/Linux :)

Install Cura from http://software.ultimaker.com or your distro.

Install Python modules

    pip install -r requirements.txt # Or get from your distro

Run

    python2 cura-server.py

Open http://localhost:8888 to see the trivial API demo

Api
----

    POST /slice
        Slice provided STL file, using the computer-wide settings for Cura.

License
-------
Affero GPL, like Cura itself.
