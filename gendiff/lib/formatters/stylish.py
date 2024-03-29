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

    return os.linesep.join(result)


def _format_node(key, node, prefix):
    result = []
    status = node['status']
    prefix_space = f'{prefix}{INDENT_SPACE}'

    if status == 'PARENT':
        nested = _format(node['children'], prefix + INDENT_SPACE)
        result.append(f'{prefix_space}{key}: {{')
        result.append(f'{nested}')
        result.append(f'{prefix_space}}}')

    elif status == 'ADDED':
        formatted_value = _format_value(node['value'], f'{prefix_space}')
        result.append(
            f'{prefix}{INDENT_PLUS}{key}: {formatted_value}')

    elif status == 'REMOVED':
        formatted_value = _format_value(node['value'], f'{prefix_space}')
        result.append(
            f'{prefix}{INDENT_MINUS}{key}: {formatted_value}')

    elif status == 'CHANGED':
        formatted_from = _format_value(node['from'], f'{prefix_space}')
        formatted_to = _format_value(node['to'], f'{prefix_space}')
        result.append(
            f'{prefix}{INDENT_MINUS}{key}: {formatted_from}')
        result.append(
            f'{prefix}{INDENT_PLUS}{key}: {formatted_to}')

    elif status == 'UNCHANGED':
        formatted_value = _format_value(node['value'], f'{prefix_space}')
        result.append(
            f'{prefix_space}{key}: {formatted_value}')

    return os.linesep.join(result)


def _format_value(value, prefix):

    if isinstance(value, dict):
        result = ['{']

        for key, value in value.items():
            prefix_space = f'{prefix}{INDENT_SPACE}'
            formatted_key_value = _format_value(value, prefix_space)
            result.append(
                f'{prefix_space}{key}: {formatted_key_value}')

        result.append(f'{prefix}}}')
        return os.linesep.join(result)
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'

    return value
