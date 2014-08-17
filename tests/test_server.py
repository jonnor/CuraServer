import time
import json
import utils as testtools
from gevent import subprocess

### Tests ###
baseurl = 'http://localhost:8888'
server_process = None

def setUp():
    global server_process
    py = testtools.findPython()
    server_process = subprocess.Popen([py, "cura-server.py"])
    time.sleep(1) # FIXME: racy, check stdout instead?

def tearDown():
    server_process.kill()

def testMissingStl():
    files = []
    response = testtools.postRequest(baseurl+'/slice', files)

    testtools.assertEqual(response.status_code, 400)
    content_type = testtools.getHeader(response, 'content-type')
    testtools.assertEqual(content_type, 'application/json')
    res = json.loads(response.read())
    assert res['error']
    assert len(res['error']) > 10

def testSliceInvalidStlFile():
    files = [ ('stl', 'invalid.stl', testtools.dataFile('invalid.stl')) ]
    response = testtools.postRequest(baseurl+'/slice', files)

    testtools.assertEqual(response.status_code, 400)
    content_type = testtools.getHeader(response, 'content-type')
    testtools.assertEqual(content_type, 'application/json')
    res = json.loads(response.read())
    assert res['error']
    assert len(res['error']) > 10


def testSliceSimpleAsciiStlFile():
    files = [ ('stl', 'trivial_ascii.stl', testtools.dataFile('trivial_ascii.stl')) ]
    response = testtools.postRequest(baseurl+'/slice', files)

    testtools.assertEqual(response.status_code, 200)
    r = response.read()
    lines = r.split('\n')
    assert len(lines) > 1000
    assert lines[0].startswith('M109 T0')

def testSliceSimpleAsciiStlField():
    fields = [ ('stl', testtools.dataFile('trivial_ascii.stl')) ]
    response = testtools.postRequest(baseurl+'/slice', fields=fields)

    testtools.assertEqual(response.status_code, 200)
    r = response.read()
    lines = r.split('\n')
    assert len(lines) > 1000
    assert lines[0].startswith('M109 T0')
