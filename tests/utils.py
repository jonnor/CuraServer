import sys, os
import mimetypes
import unittest
import functools

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

# We want assert functions that prints the values when not matching expectations
# As we dont use unittest.TestCases, need to convert them into static functions
import unittest, functools
class FakeTestCase(unittest.TestCase):
    def runTest(*ignore):
        pass
assertEqual = functools.partial(FakeTestCase.assertEqual, FakeTestCase())
assertNotEqual = functools.partial(FakeTestCase.assertNotEqual, FakeTestCase())
assertTrue = functools.partial(FakeTestCase.assertTrue, FakeTestCase())
assertFalse = functools.partial(FakeTestCase.assertFalse, FakeTestCase())
# More functions are available,
# see http://docs.python.org/2/library/unittest.html?highlight=unittest#unittest.TestCase.assertEqual

# HTTP 
# http://code.activestate.com/recipes/146306-http-client-to-post-using-multipartform-data/
def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def postRequest(url, files=[], fields=[]):
    content_type, body = encode_multipart_formdata(fields=fields, files=files)
    headers = {'Content-Type': content_type, 'Accept': '*/*'}

    url = URL(url)
    http = HTTPClient.from_url(url)
    response = http.request('POST', url.request_uri, body=body, headers=headers)
    return response

def getHeader(response, name):
    for header, value in response.headers:
        if header == name:
            return value

def dataFile(name):
    datadir = 'tests/data'
    return open(os.path.join(datadir, name), 'r').read()
