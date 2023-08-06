import hypothesis.strategies as st
from hypothesis import assume
from hypothesis import given
from strategies import DB_SCHEMES
from strategies import comma_separated_values
from strategies import db_url

from rf_django_envconfig import get_bool
from rf_django_envconfig import get_db_url
from rf_django_envconfig import get_list

FALSE_VALUES = [
    'False',
    'false',
    'Off',
    'off',
    '0',
    'No',
    'no',
    '',
]


@given(x=st.text())
def test_get_bool_true(x):
    assume(x not in FALSE_VALUES)
    env = {'test': x}
    assert get_bool(env, 'test')


@given(x=st.text())
def test_get_bool_false(x):
    assume(x in FALSE_VALUES)
    env = {'test': x}
    assert not get_bool(env, 'test')


@given(x=st.text())
def test_get_bool_default_true_value_absent(x):
    assert get_bool({}, 'test', default=True)


@given(x=st.text())
def test_get_bool_default_false_value_absent(x):
    assert not get_bool({}, 'test',  default=False)


@given(x=st.text())
def test_get_bool_default_true_value_present(x):
    assume(x in FALSE_VALUES)
    env = {'test': x}
    assert not get_bool(env, 'test',  default=True)


@given(x=st.text())
def test_get_bool_default_false_value_present(x):
    assume(x not in FALSE_VALUES)
    env = {'test': x}
    assert get_bool(env, 'test',  default=False)


@given(x=comma_separated_values())
def test_get_list(x):
    items = x.split(',')
    assert get_list({'test': x}, 'test') == items


@given(x=comma_separated_values())
def test_get_list_value_absent(x):
    assert get_list({}, 'test') == []


@given(x=comma_separated_values())
def test_get_list_value_absent_with_default(x):
    assert get_list({}, 'test', ['localhost', ]) == ['localhost', ]


@given(x=db_url())
def test_get_db_url(x):
    url, parts = x
    env = {'test': url}
    config = get_db_url(env, 'test')
    assert config['ENGINE'] == parts['ENGINE']
    assert config['NAME'] == parts['NAME']
    if parts['ENGINE'] != DB_SCHEMES['sqlite']:
        assert config['USER'] == parts['USER']
        assert config['PASSWORD'] == parts['PASSWORD']
        assert config['HOST'] == parts['HOST'].lower()
        assert config['PORT'] == parts['PORT']


@given(x=db_url())
def test_get_db_url_value_absent(x):
    url, parts = x
    config = get_db_url({}, 'test', default=url)
    assert config['ENGINE'] == parts['ENGINE']
    assert config['NAME'] == parts['NAME']
    if parts['ENGINE'] != DB_SCHEMES['sqlite']:
        assert config['USER'] == parts['USER']
        assert config['PASSWORD'] == parts['PASSWORD']
        assert config['HOST'] == parts['HOST'].lower()
        assert config['PORT'] == parts['PORT']
