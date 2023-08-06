# -*- coding: utf-8 -*-

import pytest

from mock import Mock, call

from railroad import guard, GuardError


def fn(a, b, c, d='foo'):
    return (a, b, c, d)


def test_guard_call_guarded_function():
    def fn(a):
        return a

    guarded = guard('a', lambda a: True)(fn)
    result = guarded('foo')

    assert result == 'foo'


def test_guard_pass_only_selected_paramters_to_guardian():
    guardian = Mock()

    guarded = guard(['b', 'a'], guardian)(fn)
    guarded(1, 2, 3, 4)

    assert guardian.called
    assert guardian.call_args == call(a=1, b=2)


def test_guard_raise_exception_when_guardian_return_false():
    def fn(a):
        return a

    guarded = guard('a', lambda a: False)(fn)

    with pytest.raises(GuardError):
        guarded('foo')


def test_guard_raise_custom_exception():
    def fn(a):
        return a

    class MyError(Exception):
        pass

    guarded = guard('a', lambda a: False, MyError)(fn)

    with pytest.raises(MyError):
        guarded('foo')


def test_guard_called_with_pramas_as_string():
    def fn(a, ab):
        return ab

    guarded = guard('ab', lambda ab: True)(fn)
    result = guarded(1, 'foo')

    assert result == 'foo'


def test_combined_guard_call_each_guarded_function():
    g1 = Mock()
    g2 = Mock()

    @guard('a', g1)
    @guard('b', g2)
    def fn(a, b, c):
        return (a, b, c)

    fn(1, 2, 3)

    assert g1.called
    assert g1.call_args == call(a=1)
    assert g2.called
    assert g2.call_args == call(b=2)
