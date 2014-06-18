#!/usr/bin/env python
import os
import tempfile
import subprocess
import sys

import requests


BASEDIR = os.path.abspath(os.path.dirname(__file__))

COMMANDS = {
    'linux2': {
        'browser': 'x-www-browser {0}',
        'screenshot': 'gnome-screenshot -a -f {0}'
    },
    'darwin': {
        'browser': 'open {0}',
        'screenshot': 'screencapture -s {0}'
    },
    'win32': {
        'browser': 'start {0}',
        'screenshot': os.path.join(BASEDIR, 'boxcutter.exe') + ' {0}'
    }
}

PROXIES = {
    #'http': 'full_proxy_url'
}

SERVER = {
    'host': 'http://ahye.zzzz.io',
    'port': 80,
    'path': '/upload',
    'auth': () # empty, or in the form ('username', 'password')
}

VERSION = '1.0'


if __name__ == '__main__':
    tmp_file = tempfile.mkstemp(suffix='.png')[1]
    command = COMMANDS[sys.platform]['screenshot'].format(tmp_file).split(' ')
    subprocess.call(command)
    files = {'imagedata': open(tmp_file, 'rb')}
    headers = {'User-Agent': 'ahye-python {0}'.format(VERSION)}
    url = '{0}:{1}{2}'.format(SERVER['host'], SERVER['port'], SERVER['path'])
    resp = requests.post(url, auth=SERVER['auth'], headers=headers,
                         files=files, proxies=PROXIES, verify=False)
    command = COMMANDS[sys.platform]['browser'].format(resp.text).split(' ')
    subprocess.Popen(command)
    os.remove(tmp_file)
