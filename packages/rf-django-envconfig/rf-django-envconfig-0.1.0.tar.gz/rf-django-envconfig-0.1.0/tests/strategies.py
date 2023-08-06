import hypothesis.strategies as st

UPPERCASE = [chr(x) for x in range(65, 91)]
LOWERCASE = [chr(x) for x in range(97, 123)]
DIGITS = [chr(x) for x in range(48, 58)]

RFC_3986_UNRESERVED = UPPERCASE + LOWERCASE + DIGITS + [
    '-', '_', '.', '~',
]


DB_SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'mysql-connector': 'mysql.connector.django',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
    'oraclegis': 'django.contrib.gis.db.backends.oracle',
}


@st.composite
def comma_separated_values(draw, elements=st.text()):
    """Return a strategy to generate comma-separated values"""
    xs = draw(st.lists(elements, average_size=5))
    return ','.join(xs)


@st.composite
def non_memory_db_url(draw):
    scheme = draw(st.sampled_from(DB_SCHEMES.keys()))
    user = draw(st.text(alphabet=RFC_3986_UNRESERVED))
    password = draw(st.text(alphabet=RFC_3986_UNRESERVED))
    hostname = draw(st.text(min_size=1, alphabet=RFC_3986_UNRESERVED))
    port = draw(st.integers(min_value=1, max_value=65535))
    database = draw(st.text(min_size=1, alphabet=RFC_3986_UNRESERVED))
    url = '%s://%s:%s@%s:%s/%s' % (scheme, user, password,
                                   hostname, port, database)
    return (url, {
        'ENGINE': DB_SCHEMES[scheme],
        'USER': user,
        'PASSWORD': password,
        'HOST': hostname,
        'PORT': port,
        'NAME': database,
    })


@st.composite
def db_url(draw):
    """Return a strategy to generate valid DB URLs

       The strategy will return 2-tuples. The first element of each tuple is
       the generated URL. The second element is a dict with information about
       the parts (engine, user, password and so on) that were used to build the
       URL.
    """
    return draw(st.one_of(
        non_memory_db_url(),
        st.just((
            'sqlite://:memory:',
            {'ENGINE': DB_SCHEMES['sqlite'], 'NAME': ':memory:'},
        ))
    ))
