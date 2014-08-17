import gevent
from gevent import subprocess
import bottle
import gevent.monkey
gevent.monkey.patch_all();

import sys, os
import tempfile
import shutil

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

    slicer = CliSlicer(workdir)
    ret = slicer.slice(stlpath)
    if not ret:
        response.status = 400
        ret = {'error': 'Could not slice file'}
    shutil.rmtree(workdir)
    return ret

def main():
    bottle.run(host='0.0.0.0', port=8888, server='gevent')

if __name__ == '__main__':
    main()
