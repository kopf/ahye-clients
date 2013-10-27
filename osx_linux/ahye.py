#!/usr/bin/env python
import os
import tempfile
import subprocess
import sys

import requests


COMMANDS = {
    'linux2': {
        'browser': 'x-www-browser {url}',
        'screenshot': 'gnome-screenshot -a -f {filename}'
    },
    'darwin': {
        'browser': 'open {url}',
        'screenshot': 'screencapture -s {filename}'
    }
}

PROXIES = {
    #'http': 'full_proxy_url'
}

SERVER = {
    'host': 'http://ahye.ventolin.org',
    'port': 80,
    'path': '/upload',
    'auth': () # empty, or in the form ('username', 'password')
}

VERSION = '1.0'


if __name__ == '__main__':
    tmp_file = tempfile.mkstemp(suffix='.png')[1]
    subprocess.call(COMMANDS[sys.platform]['screenshot'].format(filename=tmp_file).split(' '))
    files = {'imagedata': open(tmp_file, 'rb')}
    headers = {'User-Agent': 'ahye-python {0}'.format(VERSION)}
    url = '{0}:{1}{2}'.format(SERVER['host'], SERVER['port'], SERVER['path'])
    resp = requests.post(url, auth=SERVER['auth'], headers=headers,
                         files=files, proxies=PROXIES, verify=False)
    subprocess.Popen(COMMANDS[sys.platform]['browser'].format(url=resp.text).split(' '))
    os.remove(tmp_file)
