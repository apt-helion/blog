#!/usr/bin/env python

import os
import requests
import json


class Exist(object):
    """
    This is a module for `https://exist.io`.

    It appends custom tags to the user's custom tags according to what work has
    been done on the blog for the day (whether a new article has been made).

    This requires your `https://exist.io` developer token to be located in a
    .env.{local, production} (or as a normal env var) file as:

        EXIST_TOKEN=<token>

    Look at `http://developer.exist.io/` for a full API reference.
    """

    _custom_url = 'https://exist.io/api/1/attributes/custom/append/'

    @staticmethod
    def update_exist_tags():
        token = os.environ.get('EXIST_TOKEN')

        headers = { 'Authorization': f'Bearer {token}', 'Content-Type': 'application/json' }
        payload = json.dumps({ 'value': 'blogpost' })

        re = requests.post(Exist._custom_url, headers=headers, data=payload)

        return json.loads(re.text)
