from __future__ import print_function
import logging
from unittest import TestCase
from checkrunner import CheckRunner

__author__ = 'al4'
# logging.basicConfig(level=logging.DEBUG)


""" Example checks which we use in the tests

These would be under a class to suppress the "Decorator @staticmethod outside
class" warnings, but in Python2 the staticmethod decorator is not preserved
when you reference it in another class.
"""
@staticmethod
def passing_check():
    return True, 'always passes'

@staticmethod
def failing_check():
    return False, 'always fails'

@staticmethod
def exception_raising_check():
    raise Exception('test exception')

@staticmethod
def _private_method():
    """ We should always exclude private methods """
    raise NotImplementedError("This should never be run")


class CommonTests(object):
    MyChecks = None

    def test_returns_tuple(self):
        self.assertIsInstance(self.MyChecks.run(), tuple)

    def test_first_return_arg_is_boolean(self):
        self.assertIsInstance(self.MyChecks.run()[0], bool)

    def test_second_return_arg_is_list(self):
        self.assertIsInstance(self.MyChecks.run()[1], list)

    def test_output_does_not_contain_passed_message(self):
        result, out = self.MyChecks.run()
        self.assertNotIn('always passes', out)


class FailureTests(object):
    """ Test the failure scenarios """
    MyChecks = None

    def test_list_is_not_empty(self):
        self.assertEqual(
            len(self.MyChecks.run()[1]),
            1
        )

    def test_list_contains_failed(self):
        """ Test the list contains our fail string """
        self.assertEqual(
            self.MyChecks.run()[1][0],
            'always fails'
        )


# Testing the common tests against the various cases (all passing, all failing,
# mixed)
class TestPassing(TestCase, CommonTests):
    """ All checks pass """
    class MyChecks(CheckRunner):
        passing_check = passing_check


class TestFailing(TestCase, CommonTests, FailureTests):
    """ All checks fail """
    class MyChecks(CheckRunner):
        failing_check = failing_check


class TestMixed(TestCase, CommonTests, FailureTests):
    """ Both passing and failing checks """
    class MyChecks(CheckRunner):
        passing_check = passing_check
        failing_check = failing_check

    def test_mixed_returns_false(self):
        """ Result of a test with some failed checks is fail """
        result, out = self.MyChecks.run()
        self.assertFalse(result)


class TestPrivateMethods(TestCase, CommonTests):
    """ Tests with a private method present
    """
    class MyChecks(CheckRunner):
        passing_check = passing_check
        failing_check = failing_check
        _excluded_method = _private_method

    def test_get_methods_excludes_private(self):
        """ Test that we exclude private methods
        """
        methods = self.MyChecks._get_check_methods()
        self.assertNotIn(self.MyChecks._excluded_method, methods)


class TestReturnPassed(TestCase):
    """ Test with return_passed=True """
    class MyChecks(CheckRunner):
        passing_check = passing_check
        # failing_check = ExampleChecks.failing_check

    def test_includes_passed(self):
        result, out = self.MyChecks.run(return_passed=True)
        self.assertIn('always passes', out)
