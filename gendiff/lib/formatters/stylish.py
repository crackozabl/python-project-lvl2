import os

INDENT_SPACE = ' ' * 4
INDENT_PLUS = INDENT_SPACE.removesuffix('  ') + '+ '
INDENT_MINUS = INDENT_SPACE.removesuffix('  ') + '- '


def format(diff):
    formatted_result = _format(diff, '')
    return f'{{{os.linesep}{formatted_result}{os.linesep}}}'


def _format(diff, prefix=''):
    result = []

    for key in diff.keys():
        result.append(_format_node(key, diff[key], prefix))

    return '\n'.join(result)


def _format_node(key, node, prefix):
    result = []
    status = node['status']

    if status == 'PARENT':
        nested = _format(node['children'], prefix + INDENT_SPACE)
        result.append(f'{prefix}{INDENT_SPACE}{key}: {{')
        result.append(f'{nested}')
        result.append(f'{prefix}{INDENT_SPACE}}}')

    elif status == 'ADDED':
        formatted_value = _format_value(node['value'], f'{prefix}{INDENT_SPACE}')
        result.append(
            f'{prefix}{INDENT_PLUS}{key}: {formatted_value}')

    elif status == 'REMOVED':
        formatted_value = _format_value(node['value'], f'{prefix}{INDENT_SPACE}')
        result.append(
            f'{prefix}{INDENT_MINUS}{key}: {formatted_value}')

    elif status == 'CHANGED':
        formatted_from = _format_value(node['from'], f'{prefix}{INDENT_SPACE}')
        formatted_to = _format_value(node['to'], f'{prefix}{INDENT_SPACE}')
        result.append(
            f'{prefix}{INDENT_MINUS}{key}: {formatted_from}')
        result.append(
            f'{prefix}{INDENT_PLUS}{key}: {formatted_to}')

    elif status == 'UNCHANGED':
        formatted_value = _format_value(node['value'], f'{prefix}{INDENT_SPACE}')
        result.append(
            f'{prefix}{INDENT_SPACE}{key}: {formatted_value}')

    return os.linesep.join(result)


def _format_value(value, prefix):
    if isinstance(value, dict):
        result = ['{']

        for k,v in value.items():
            print(f'{k=}, {v=}')
            result.append(f'{prefix}{INDENT_SPACE}{k}: {_format_value(v, prefix + INDENT_SPACE)}')

        result.append(f'{prefix}}}')
        return '\n'.join(result)
        # return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'

    return value
