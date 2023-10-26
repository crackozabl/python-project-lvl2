import json
import yaml
import os
import argparse
from gendiff.lib.formatters import json as json_formatter,\
    plain, stylish

def parse_args():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')

    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format',
                        type=str,
                        default='stylish',
                        choices=['json','stylish','plain'])

    args = parser.parse_args()
    return args

def load_content(path):
    with open(path) as file:
        return file.read()


def get_format(path):
    _, ext = os.path.splitext(path)
    return ext


def parse_content(content, file_type):
    if file_type == '.json':
        return json.loads(content)
    elif file_type in ['.yaml', '.yml']:
        return yaml.load(content, Loader=yaml.Loader)


def generate_diff(path1, path2, format_='stylish'):
    content1 = load_content(path1)
    content2 = load_content(path2)
    type1 = get_format(path1)
    type2 = get_format(path2)
    parsed_content1 = parse_content(content1, type1)
    parsed_content2 = parse_content(content2, type2)

    diff = _build_diff(parsed_content1, parsed_content2)

    if format_ == 'json':
        return json_formatter.format(diff)
    elif format_ == 'plain':
        return plain.format(diff)
    elif format_ == 'stylish':
        return stylish.format(diff)


def _build_diff(data1, data2):
    keys = sorted(set(data1.keys()) | set(data2.keys()))

    diff = {}

    for key in keys:
        diff[key] = _build_status(key, data1, data2)

    return diff


def _build_status(key, data1, data2):
    if key in data1.keys() and key in data2.keys():
        if data1[key] == data2[key]:
            return {
                'status': 'UNCHANGED',
                'value': data1[key]
            }

        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            return {
                'status': 'PARENT',
                'children': _build_diff(data1[key], data2[key])
            }

        else:
            return {
                'status': 'CHANGED',
                'from': data1[key],
                'to': data2[key]
            }

    elif key in data1.keys():
        return {'status': 'REMOVED', 'value': data1[key]}

    elif key in data2.keys():
        return {'status': 'ADDED', 'value': data2[key]}
