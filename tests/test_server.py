import json
import utils as testtools

### Tests ###
baseurl = 'http://localhost:8888'

# TODO: automatically start/stop server
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
    files = [ ('stl', 'invalid.stl', open('invalid.stl', 'r').read()) ]
    response = testtools.postRequest(baseurl+'/slice', files)

    testtools.assertEqual(response.status_code, 400)
    content_type = testtools.getHeader(response, 'content-type')
    testtools.assertEqual(content_type, 'application/json')
    res = json.loads(response.read())
    assert res['error']
    assert len(res['error']) > 10


def testSliceSimpleAsciiStlFile():
    files = [ ('stl', 'trivial_ascii.stl', open('trivial_ascii.stl', 'r').read()) ]
    response = testtools.postRequest(baseurl+'/slice', files)

    testtools.assertEqual(response.status_code, 200)
    r = response.read()
    lines = r.split('\n')
    assert len(lines) > 1000
    assert lines[0].startswith('M109 T0')
    open('trivial.out.gcode', 'w').write(r)

def testSliceSimpleAsciiStlField():
    fields = [ ('stl', open('trivial_ascii.stl', 'r').read()) ]
    response = testtools.postRequest(baseurl+'/slice', fields=fields)

    testtools.assertEqual(response.status_code, 200)
    r = response.read()
    lines = r.split('\n')
    assert len(lines) > 1000
    assert lines[0].startswith('M109 T0')
    open('trivial.out.gcode', 'w').write(r)
