import re


_SCALE_VERSION_RE = re.compile(
    r'^(?P<major>\d{2})\.(?P<minor>\d{2})(?:\.(?P<patch>\d+))?(?:-?(?P<pre>RC|BETA)\.?(?P<pre_n>\d+)?)?$'
)


def _scale_version_key(version):
    match = _SCALE_VERSION_RE.match(version or '')
    if not match:
        raise ValueError(f'Invalid scale version: {version!r}')

    pre = match.group('pre')
    pre_order = {'BETA': 0, 'RC': 1, None: 2}
    return (
        int(match.group('major')),
        int(match.group('minor')),
        int(match.group('patch') or 0),
        pre_order[pre],
        int(match.group('pre_n') or 0),
    )


def can_update(current_version, new_version):
    return _scale_version_key(current_version) <= _scale_version_key(new_version)


def validate_filters(filters):
    if not isinstance(filters, (list, tuple)):
        raise ValueError('Filters must be a list or tuple')

    for index, f in enumerate(filters):
        if isinstance(f, str):
            # Logical operators are commonly represented as strings between filters.
            continue

        if not isinstance(f, (list, tuple)):
            raise ValueError(f'Filter at index {index} must be a list/tuple')

        if len(f) != 3:
            raise ValueError(f'Filter at index {index} must have 3 elements')
