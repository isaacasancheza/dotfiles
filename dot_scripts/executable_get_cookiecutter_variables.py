#!/usr/bin/env python3
import json

import requests


root = 'https://raw.githubusercontent.com/isaacsancheza/cookiecutters/master/%s/cookiecutter.json'
cookiecutter_name = input('cookiecutter name: ')

if not cookiecutter_name:
    print('cookiecutter name cannot be empty')
    exit(1)

response = requests.get(root % cookiecutter_name, timeout=6)
if not response.ok:
    print('cookiecutter "%s" does not exists' % cookiecutter_name)
    exit(1)

cookiecutter = json.loads(response.text)
variables = ['    %s: ' % key for key in cookiecutter if not key.startswith('_')]

with open('%s-variables' % cookiecutter_name, 'w') as f:
    f.write('default_context:\n')
    for variable in variables:
        f.write('%s\n' % variable)
