from __future__ import print_function
import logging
from unittest import TestCase
from checkrunner import CheckRunner

__author__ = 'al4'
# logging.basicConfig(level=logging.DEBUG)


class ExampleChecks(object):
    """ Example checks which we use in the tests """
    @classmethod
    def passing_check(cls):
        return True, 'always passes'

    @classmethod
    def failing_check(cls):
        return False, 'always fails'

    @classmethod
    def exception_raising_check(cls):
        raise Exception('test exception')

    @classmethod
    def _private_method(cls):
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
        passing_check = ExampleChecks.passing_check


class TestFailing(TestCase, CommonTests, FailureTests):
    """ All checks fail """
    class MyChecks(CheckRunner):
        failing_check = ExampleChecks.failing_check


class TestMixed(TestCase, CommonTests, FailureTests):
    """ Both passing and failing checks """
    class MyChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
        failing_check = ExampleChecks.failing_check

    def test_mixed_returns_false(self):
        """ Result of a test with some failed checks is fail """
        result, out = self.MyChecks.run()
        self.assertFalse(result)


class TestPrivateMethods(TestCase, CommonTests):
    """ Tests with a private method present
    """
    class MyChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
        failing_check = ExampleChecks.failing_check
        _excluded_method = ExampleChecks._private_method

    def test_get_methods_excludes_private(self):
        """ Test that we exclude private methods
        """
        methods = self.MyChecks._get_check_methods()
        self.assertNotIn(self.MyChecks._excluded_method, methods)


class TestReturnPassed(TestCase):
    """ Test with return_passed=True """
    class MyChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
        # failing_check = ExampleChecks.failing_check

    def test_includes_passed(self):
        result, out = self.MyChecks.run(return_passed=True)
        self.assertIn('always passes', out)
