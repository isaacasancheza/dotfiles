#!/usr/bin/env python3
import yaml
import json
import argparse
import requests


URI = 'https://raw.githubusercontent.com/isaacsancheza/cookiecutters/master/{cookiecutter_name}/cookiecutter.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cookiecutter_name', type=str, help='cookiecutter name')

    args = parser.parse_args()
    cookiecutter_name = args.cookiecutter_name
    
    if not cookiecutter_name:
        print('cookiecutter name cannot be empty')
        parser.exit(1)

    response = requests.get(URI.format(cookiecutter_name=cookiecutter_name), timeout=6)
    if not response.ok:
        print('cookiecutter "{cookiecutter_name}" does not exists'.format(cookiecutter_name=cookiecutter_name))
        parser.exit(1)

    cookiecutter_json = json.loads(response.text)
    cookiecutter_variables = {key: '' for key in cookiecutter_json if not key.startswith('_')}

    cookiecutter = {
        'default_context': cookiecutter_variables
    }

    with open('{cookiecutter_name}-variables.yaml'.format(cookiecutter_name=cookiecutter_name), 'w', encoding='UTF-8') as f:
        yaml.dump(cookiecutter, f, indent=4)
