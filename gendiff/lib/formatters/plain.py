

def format(diff):
    return _format(diff)


def _format(diff, prefix=''):
    result = []

    for key in diff.keys():

        status = diff[key]['status']
        path = f'\'{prefix}{key}\''

        if status == 'PARENT':
            result.append(
                _format(diff[key]['children'], f'{prefix}{key}.'))

        elif status == 'ADDED':
            formatted_value = _format_value(diff[key]['value'])
            result.append(
                f'Property {path} was added with value: '
                f'{formatted_value}.')

        elif status == 'REMOVED':
            result.append(
                f'Property {path} was removed')

        elif status == 'CHANGED':
            formatted_from = _format_value(diff[key]['from'])
            formatted_to = _format_value(diff[key]['to'])
            result.append(
                f'Property {path} was updated. '
                f'From {formatted_from} to {formatted_to}')

    return '\n'.join(result)


def _format_value(value):

    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return f'\'{value}\''
    if value is None:
        return 'null'

    return value
