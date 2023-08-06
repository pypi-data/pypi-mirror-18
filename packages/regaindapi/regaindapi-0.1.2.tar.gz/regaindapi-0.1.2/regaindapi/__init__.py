#!/usr/bin/env python

# Copyright (c) 2015-2016 Regaind (https://regaind.io)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import requests
import json
import collections
from PIL import Image

BASE_URL = "https://api.regaind.io/api/"

def _print_request(req):
    print('{}\n{}\n{}\n\n{}\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body[:2048] if req.body else "",
        '------------END------------',
    ))

class Client(object):
    _token = None

    def __init__(self, client_id, client_secret, debug=False):
        self._client_id = client_id
        self._client_secret = client_secret
        self._debug = debug

    def acquire_token(self):
        """Acquire a temporary OAuth2 token and use it."""
        self._token = self._auth(self._client_id, self._client_secret)

    def _call(self, method, endpoint, data={}, files={}, params={}, content_type=None):
        """Internal helper to build requests."""
        headers = {}
        kwargs = {}
        if self._token is not None:
            headers['Authorization'] = 'Bearer {}'.format(self._token)
        elif not endpoint.startswith("auth/"):
            kwargs["auth"] = (self._client_id, self._client_secret)
        if content_type is not None:
            headers["Content-Type"] = content_type
        caller = getattr(requests, method)
        resp = caller(BASE_URL + endpoint,
                      params=params, data=data, files=files,
                      headers=headers, **kwargs)
        if self._debug:
            _print_request(resp.request)
        resp.raise_for_status()
        return resp.json()

    def _get(self, *args, **kwargs):
        """Internal helper to build GET requests."""
        return self._call("get", *args, **kwargs)

    def _post(self, *args, **kwargs):
        """Internal helper to build post requests."""
        return self._call("post", *args, **kwargs)

    def _auth(self, client_id, client_secret):
        """Acquire a temporary OAuth2 token."""
        resp = self._post("auth/token/", {"client_id": client_id,
                                          "client_secret": client_secret,
                                          "grant_type": "client_credentials"})
        return resp['access_token']

    # Picture collection ("album") API calls

    def new_album(self, album_title=""):
        """Create a new album."""
        return self._post("album/new/", data={"title": album_title})["album"]

    def upload(self, album_id, client_id, url=None, filepath=None):
        """Add a photo to an album, either by url or filepath."""
        assert url is not None or filepath is not None and (url is None or filepath is None)
        if url is not None:
            return self._post("album/%(album)d/upload/" % {"album": album_id},
                              content_type="application/json",
                              data=json.dumps({"filename": os.path.basename(url),
                                               "id": client_id,
                                               "url": url}))
        else:
            return self._post("album/%(album)d/upload/" % {"album": album_id},
                              data={"filename": os.path.basename(filepath),
                                    "id": client_id},
                              files={"file": open(filepath, "rb")})

    def uploads(self, album_id, entries):
        """Add a batch of photos by URL to an album."""
        return self._post("album/%(album)d/upload/" % {"album": album_id},
                          content_type="application/json",
                          data=json.dumps({"entries": entries}))

    def make_album(self, path):
        """Helper function to create an album from a directory of photos."""
        if not os.path.exists(path) or not os.path.isdir(path):
            raise IOError("%s not found" % path)
        dirname = os.path.basename(path)
        album_id = self.new_album(dirname)
        files = os.listdir(path)
        pictures = []
        for idx, fname in enumerate(files):
            print("Uploading file {}/{}".format(idx + 1, len(files)))
            fpath = os.path.join(path, fname)
            try:
                im = Image.open(fpath)
                im.verify()
            except IOError:
                continue
            resp = self.upload(album_id, "%s_%d" % (dirname, idx), filepath=fpath)
            pictures.append(resp["id"])
        return album_id, pictures

    def metadata(self, album_id, picture_id):
        """Get metadata produced for a given picture or a list of pictures."""
        if isinstance(picture_id, collections.Iterable):
            return self._get("album/%(album)d/metadata/" % {"album": album_id},
                             content_type="application/json",
                             data=json.dumps({"entries": picture_id}))
        else:
            return self._get("album/%(album)d/metadata/%(picture)d/" % {"album": album_id, "picture": picture_id})

    def suggest(self, album_id):
        """Suggest appropriate number of photos to summarize an album."""
        return self._get("album/%(album)d/suggest/" % {"album": album_id})

    def summary_narrative(self, album_id, count):
        """Summarize an album of photos into fewer pictures."""
        return self._get("album/%(album)d/summary/narrative/%(count)d/" % {"album": album_id, "count": count})["pictures"]

    def summary_aesthetics(self, album_id, count):
        """Surface the most beautiful photos of an album."""
        return self._get("album/%(album)d/summary/aesthetics/%(count)d/" % {"album": album_id, "count": count})["pictures"]

    def book(self, album_id, selection):
        """Generate a photobook out of provided selection."""
        return self._post("album/%(album)d/book/" % {"album": album_id},
                          content_type="application/json",
                          data=json.dumps({"pictures": selection}))

    # Single-picture API calls

    def metrics(self, filepath, options, async=False):
        """Request metrics for a single picture."""
        if isinstance(filepath, list):
            return self._post("qualimetrics/",
                              content_type="application/json",
                              data=json.dumps({"options": options, "entries": filepath}))
        elif not os.path.exists(filepath):
            return self._post("qualimetrics/",
                              content_type="application/json",
                              data=json.dumps({"options": options,
                                               "url": filepath}))
        else:
            return self._post("qualimetrics/",
                              data={"options": options, "async": async},
                              files={"file": open(filepath, "rb")})

    def metrics_result(self, callid):
        """Get metrics results for the given asynchronous call(s)."""
        if isinstance(callid, collections.Iterable):
            return self._get("status/",
                             content_type="application/json",
                             data=json.dumps({"entries": callid}))
        else:
            return self._get("status/%d" % callid)


__all__ = ["Client"]
