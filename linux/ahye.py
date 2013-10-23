import os
import tempfile
import subprocess

import requests


COMMANDS = {
    'browser': 'x-www-browser {url}',
    'screenshot': 'gnome-screenshot -a -f {filename}'
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
    subprocess.call(COMMANDS['screenshot'].format(filename=tmp_file).split(' '))
    files = {'imagedata': open(tmp_file, 'rb')}
    headers = {'User-Agent': 'ahye-python {0}'.format(VERSION)}
    url = '{0}:{1}{2}'.format(SERVER['host'], SERVER['port'], SERVER['path'])
    resp = requests.post(url, auth=SERVER['auth'], headers=headers,
                         files=files, proxies=PROXIES)
    subprocess.Popen(COMMANDS['browser'].format(url=resp.text).split(' '))
    os.remove(tmp_file)
