# -*- coding: utf-8 -*-

from random import randint

from mock import Mock, call
from toolz import cons

from railroad import actions, lift, result


def test_result_return_state():
    r = result([1, 2, 3], 'state')

    assert r == 'state'


def test_run_lifted_function_return_intermediate_state_crate():
    f = Mock()
    f.__name__ = 'f'
    lifted = lift(f)
    prepered = lifted()

    result = prepered('foo')

    assert result['answer'] == f.return_value
    assert result['state'] == f.return_value


def test_lift_call_state_fn():
    f = Mock()
    f.__name__ = 'f'
    state_fn = Mock()
    lifted = lift(state_fn=state_fn)(f)
    prepered = lifted()

    prepered('foo')

    assert state_fn.called
    assert state_fn.call_args == call('foo')


def test_actions_call_done_with_state_and_values():

    def f(a, b):
        return '%s%d' % (a, b)

    fl = lift(f)
    instructions = [fl(i) for i in range(randint(1, 1000))]

    run = actions(instructions, result)
    r = run('seed')

    expect = ''.join(cons('seed', [str(i) for i in range(len(instructions))]))

    assert r == expect
