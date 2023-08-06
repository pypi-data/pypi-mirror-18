from __future__ import print_function
import logging

__author__ = 'al4'
logger = logging.getLogger(__name__)


class CheckRunner(object):
    """ A suite of checks

    You should create a subclass of this class which contains the checks you
    want to run as functions. Then call MyChecks.run() (there is no need to
    instantiate the class). See the readme for more information.
    """
    def __init__(self):
        """ To allow instantiation, we would have to detect whether we are an
        instance and pass the self argument. At this time, I deem this not
        necessary.
        """
        raise NotImplementedError(
            "CheckRunner should not be instantiated"
        )

    @classmethod
    def run(cls, return_passed=False, **kwargs):
        """
        Run the checks

        If you use return_passed, be sure to make whatever string or object
        you return also indicates the pass/fail state, as only one boolean is
        returned.

        :param return_passed: Also return checks that passed in the output
        :return tuple: Tuple consisting of a boolean (which is True if all
            tests passed and False if any of them failed), and a list of the
            return values from the checks
        """
        methods = cls._get_check_methods()
        logger.debug('Found methods: {}'.format([
            m.__name__ for m in methods
        ]))

        results = []
        for check_function in methods:
            logger.debug('Running check_function {}'.format(
                check_function.__name__))
            if kwargs:
                results.append(check_function(**kwargs))
            else:
                results.append(check_function())
        logger.debug('Results: {}'.format(results))

        if all([result for result, message in results]) \
                or not results:
            # All are true or empty list
            logger.debug('All checks passed')
            if return_passed:
                return True, [message for _, message in results]
            return True, []
        else:
            failed = [message for result, message in results if result is False]
            logger.debug('Checks failed: {}'.format(failed))
            if return_passed:
                return False, [message for _, message in results]
            else:
                return False, failed

    @classmethod
    def _get_check_methods(cls):
        """
        Fetch the methods declared in this class (usually a sub-class)

        By comparing to the base class. We exclude private methods that
        start with an underscore.
        """
        my_class = None
        for subclass in CheckRunner.__subclasses__():
            if subclass == cls:
                my_class = subclass

        if not my_class:
            # not a subclass?
            return []
        else:
            methods = list(set(dir(my_class)) - set(dir(CheckRunner)))
            logger.debug('All methods: {}'.format(methods))
            return [
                getattr(cls, m) for m in methods if not m.startswith('_')
            ]

