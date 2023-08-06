import dj_database_url

__version__ = "0.1.0"


def get_bool(env, name, default=False):
    """Get a boolean value from the environment

    If ``name`` is not found in ``env``, return ``True`` if ``default``
    evaluates to ``True``, otherwise return ``False``.

    The following values are considered ``False``:

        * ``'False'``
        * ``'false'``
        * ``'Off'``
        * ``'off'``
        * ``'0'``
        * ``'No'``
        * ``'no'``
        * ``''``

    Any other value is considered ``True``.
    """
    if name not in env:
        return bool(default)
    value = env[name]
    if value in ['False', 'false', 'Off', 'off', '0', 'No', 'no', '']:
        return False
    return True


def get_list(env, name, default=None):
    """Get a list from the environment

    The input is assumed to be a comma-separated list of strings.

    If ``name`` is not found in ``env``, return ``default``. Note
    that ``default`` is returned as-is, so you should usually specify it as a
    list::

        ALLOWED_HOSTS = get_list(os.environ, 'ALLOWED_HOSTS', ['localhost', ])
    """
    if default is None:
        default = []
    if name not in env:
        return default
    return env[name].split(',')


def get_db_url(env, name, default=''):
    """Get a ``settings.DATABASES`` entry from a URL in the environment

    This is just a thin convenience wrapper around dj-database-url.

    If ``name`` is not found in ``env``, return the result of parsing
    ``default``.


    .. code-block:: python

        DATABASES = {
            'default': get_db_url(
                os.environ,
                'DATABASE_URL',
                default='postgres://myuser:mypassword@localhost/myproject'
            )
        }
    """
    if name not in env:
        return dj_database_url.parse(default)
    return dj_database_url.parse(env[name])
