# -*- coding: utf-8 -*-

from pykyu import Kyu, KyuState


def _prepare_default():
    def log_to_cursor(what):
        def wrapper(state: KyuState):
            state.data['log'].append(what)

        return wrapper

    def setup(state: KyuState):
        state.data['log'] = list()
        state.data['log'].append('! setup')

    fetch_people = log_to_cursor('> fetch_people')
    fetch_roles = log_to_cursor('> fetch_roles')
    fetch_orders = log_to_cursor('> fetch_orders')
    display_json = log_to_cursor('> display_json')

    def display_decision(state: KyuState):
        state.data['log'].append('+ display_decision')
        state.cursor.kyu.group('present').hook(display_json)

    kyu = Kyu('default')
    with kyu.group('setup') as group:
        group.hook(setup)
    with kyu.group('data') as group:
        group.hook(fetch_people)
        group.hook(fetch_roles, priority=30)
        group.hook(fetch_orders)

    with kyu.group('present') as group:
        group.hook(display_decision, priority=10)

    return kyu


def test_build_order():
    kyu = _prepare_default()

    # after running the cursor, the state is returned, which will
    # be populated with the ordered log items
    assert kyu.run(KyuState()).data == {
        'log': [
            '! setup',
            '> fetch_roles',
            '> fetch_people',
            '> fetch_orders',
            '+ display_decision',
            '> display_json',
        ]
    }


def test_dynamic_list():
    kyu = Kyu('test')

    def setup_a(s: KyuState):
        s.data['log'] = list()
        s.data['log'].append('setup_a > skipping setup_b, setup_b')

        # this will skip setup_b and setup_c
        print('skip_group!')
        s.cursor.skip_group()

    def setup_b(s: KyuState):
        s.data['log'].append('setup_b ! ignored')

    def setup_c(s: KyuState):
        s.data['log'].append('setup_c ! ignored')

    def fetch_a(s: KyuState):
        s.data['log'].append('fetch_a > nothing')

    def fetch_b(s: KyuState):
        s.data['log'].append('fetch_b > assert current and previous')
        assert s.cursor.current.callback is fetch_b
        assert s.cursor.peek_previous.callback is fetch_a

    def display_a(s: KyuState):
        s.data['log'].append('display_a > add display_b')
        assert s.cursor.peek_next is None
        s.cursor.kyu.group('display').hook(display_b)
        assert s.cursor.peek_next.callback is display_b

    def display_b(s: KyuState):
        s.data['log'].append('display_b > nothing')

    with kyu.group('setup') as g:
        g.hook(setup_a)
        g.hook(setup_b)
        g.hook(setup_c)
    with kyu.group('fetch') as g:
        g.hook(fetch_b)
        g.hook(fetch_a, priority=10)
    with kyu.group('display') as g:
        g.hook(display_a)

    expected_result = [
        'setup_a',
        'setup_b',
        'setup_c',
        'fetch_a',
        'fetch_b',
        'display_a',
    ]

    assert [x[1].name.split('.')[-1] for x in kyu.flatten()] == expected_result

    cursor = kyu.cursor(KyuState())
    assert 'setup_a' in cursor.current.name
    assert cursor.peek_previous is None
    assert 'setup_b' in cursor.peek_next.name

    assert [x.name.split('.')[-1] for x in iter(cursor)] == expected_result

    assert kyu.run(KyuState()).data['log'] == [
        'setup_a > skipping setup_b, setup_b',
        'fetch_a > nothing',
        'fetch_b > assert current and previous',
        'display_a > add display_b',
        'display_b > nothing',
    ]


def test_skipping():
    kyu = Kyu('test')

    def setup_a(s: KyuState):
        s.data['log'] = list()
        s.data['log'].append('setup_a')

        # this will skip setup_b and setup_c
        print('skip_group!')
        s.cursor.skip_group()

    def setup_b(s: KyuState):
        s.data['log'].append('setup_b ! ignored')

    def setup_c(s: KyuState):
        s.data['log'].append('setup_c ! ignored')

    def fetch_a(s: KyuState):
        # simulate some error, we need to skip to the end
        s.data['log'].append('fetch_a')
        s.cursor.skip_to_end()

    def fetch_b(s: KyuState):
        s.data['log'].append('fetch_b')

    def display_a(s: KyuState):
        s.data['log'].append('display_a')

    with kyu.group('setup') as g:
        g.hook(setup_a)
        g.hook(setup_b)
        g.hook(setup_c)
    with kyu.group('fetch') as g:
        g.hook(fetch_b)
        g.hook(fetch_a, priority=10)
    with kyu.group('display') as g:
        g.hook(display_a)

    assert [x[1].name.split('.')[-1] for x in kyu.flatten()] == [
        'setup_a',
        'setup_b',
        'setup_c',
        'fetch_a',
        'fetch_b',
        'display_a',
    ]

    assert kyu.run(KyuState()).data['log'] == [
        'setup_a',
        'fetch_a',
    ]
