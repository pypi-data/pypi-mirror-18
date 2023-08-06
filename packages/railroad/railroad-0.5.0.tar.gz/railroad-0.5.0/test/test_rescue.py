# -*- coding: utf-8 -*-

import pytest

from mock import Mock, call

from railroad import rescue


def test_rescue_call_original_function():
    on_success = Mock()
    f = Mock()

    rescue(f, on_success)(1, 2, 'foo')  # call f function

    assert f.called
    assert f.call_args == call(1, 2, 'foo')


def test_rescue_call_on_success_with_function_return_value_as_parameter():
    on_success = Mock()
    f = Mock()

    rescue(f, on_success)()  # call f function

    assert on_success.called
    assert on_success.call_args == call(f.return_value)


def test_rescue_return_on_success_result():
    on_success = Mock()
    f = Mock()

    result = rescue(f, on_success)()  # call f function

    assert result == on_success.return_value


def test_rescue_in_default_reraise_exception():
    on_success = Mock()
    f = Mock()

    class MyException(Exception):
        pass

    f.side_effect = MyException

    with pytest.raises(MyException):
        rescue(f, on_success)()  # call f function


def test_rescue_call_on_error_when_exception():
    on_success = Mock()
    f = Mock()
    f.side_effect = Exception

    def on_error(e):
        assert e.__class__ == Exception

    rescue(f, on_success, on_error)()  # call f function


def test_rescue_return_on_error_value():
    on_success = Mock()
    on_error = Mock()
    f = Mock()
    f.side_effect = Exception

    result = rescue(f, on_success, on_error)()  # call f function

    assert result == on_error.return_value


def test_rescue_call_on_complete():
    on_complete = Mock()

    rescue(Mock(), Mock(), Mock(), on_complete)()  # call f function

    assert on_complete.called
