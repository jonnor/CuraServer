import gevent
from gevent import subprocess
import bottle
import gevent.monkey
gevent.monkey.patch_all(subprocess=True);

import sys, os
import tempfile
import shutil
import json

# TODO: allow to set Cura settings over HTTP
# TODO: allow to rotate/scale over HTTP?
# TODO: API for creating preview with WebGL
# TODO: add authentication, like an API key

class Slicer(object):
    def slice(self, stl):
        """return gcode"""
        raise NotImplementedError

class CliSlicer(Slicer):
    cura_cmd = 'cura'

    def __init__(self, workdir):
        self._workdir = workdir

    def slice(self, stl):
        out = os.path.join(self._workdir, "output.gcode")
        args = [self.cura_cmd, '--slice']
        #args += ['--ini', settingsfile]
        args += ['--output', out, stl]

        #print ' '.join(args)
        try:
            subprocess.check_call(args)
        except Exception, e:
            return None

        ret = open(out, 'r')
        return ret


class ApiSlicer(Slicer):
    cura_pydir = "/usr/share/cura" # FIXME: make cross-platform

    def __init__(self, workdir):
        self._workdir = workdir

    def slice(self, stl):
        r = self._slice(stl)
        return None if not r else r.get('gcode')

    def _slice(self, stl):
        if not self.cura_pydir in sys.path:
            sys.path.append(self.cura_pydir)

        import Cura
        from Cura.util import sliceEngine
        from Cura.util import objectScene
        from Cura.util import meshLoader

        def commandlineProgressCallback(progress):
            if progress >= 0:
                #print 'Preparing: %d%%' % (progress * 100)
                pass

        try:
            scene = objectScene.Scene()
            scene.updateMachineDimensions()
            engine = sliceEngine.Engine(commandlineProgressCallback)
            for m in meshLoader.loadMeshes(stl):
                # typeof(m) == printableObjects
                scene.add(m)
            engine.runEngine(scene)
            engine.wait()
        except Exception, e:
            return None

        result = engine.getResult()
        if not result.isFinished():
            return None
        ret = {
            'gcode': result.getGCode(),
            'polygons': result._polygons,
            'filamentUse': result.getFilamentAmount(),
            'printTime': result.getPrintTime(),
        }
        return ret


# HTTP API
@bottle.hook('after_request')
def enable_cors():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'

@bottle.route('/static/<filename:path>')
def serve_static(filename):
    return bottle.static_file(filename, root='./static')

@bottle.route('/')
@bottle.route('/index.html')
def serve_static():
    return bottle.static_file('index.html', root='./static')

@bottle.route('/slice', method='POST')
def slice():
    request, response = bottle.request, bottle.response

    upload = request.files.stl
    if not upload:
        upload = request.forms.stl
    if not upload:
        response.status = 400
        return {'error': 'Missing "stl" field'}

    workdir = tempfile.mkdtemp(prefix='cura-server')
    stlpath = os.path.join(workdir, 'upload.stl')
    if hasattr(upload, 'save'):
        upload.save(stlpath)
    else:
        open(stlpath, "w").write(upload)

    slicer = CliSlicer(workdir) if False else ApiSlicer(workdir)
    ret = slicer.slice(stlpath)
    if not ret:
        response.status = 400
        ret = {'error': 'Could not slice file'}
    shutil.rmtree(workdir)
    return ret

# FIXME: stupid API, does rendering twice when you want both preview and code
@bottle.route('/preview', method='POST')
def preview():
    request, response = bottle.request, bottle.response

    upload = request.files.stl
    if not upload:
        upload = request.forms.stl
    if not upload:
        response.status = 400
        return {'error': 'Missing "stl" field'}

    workdir = tempfile.mkdtemp(prefix='cura-server')
    stlpath = os.path.join(workdir, 'upload.stl')
    if hasattr(upload, 'save'):
        upload.save(stlpath)
    else:
        open(stlpath, "w").write(upload)

    slicer = ApiSlicer(workdir)
    ret = slicer._slice(stlpath)
    if not ret:
        response.status = 400
        ret = {'error': 'Could not preview file'}
    shutil.rmtree(workdir)
    return ret

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle Numpy arrays for polygons from Cura
        import numpy
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def main():
    bottle.install(bottle.JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=CustomJsonEncoder)))
    bottle.run(host='0.0.0.0', port=8888, server='gevent')

if __name__ == '__main__':
    main()
