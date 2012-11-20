#!/usr/bin/env python

import pickle
import mechanize

def requestToStr(req):
    url = req.get_full_url()
    headers = req.header_items()
    data = req.data
    return pickle.dumps((url, headers, data))

def strToRequest(strReq):
    (url, headers, data) = pickle.loads(strReq)
    # The space causes mechanize to POST instead of GET
    req = mechanize.Request(url, " ")
    for (header_name, header_value) in headers:
        req.add_header(header_name, header_value)
    req.data = data
    return req

