python-checkrunner
==================
A very simple check runner for Python. I use this in projects where I need to run a suite of checks before performing some action (usually on invocation).

Usage
-----
Create a sub-class of CheckRunner and declare your checks::

    from checkrunner import CheckRunner

    class MyChecks(CheckRunner):
        @classmethod
        def check_that_passes(cls):
            return True, 'this check passed!'

        @classmethod
        def check_that_fails(cls):
            return False, 'this check failed!'

    print(MyChecks.run())
    # (False, ['this check failed!'])

    print(MyChecks.run(return_passed=True))
    # (False, ['this check passed!', 'this check failed!'])


When all checks pass it will return True with an empty list (unless you set return_passed)::

    from checkrunner import CheckRunner

    class MyChecks(CheckRunner):
        @classmethod
        def check_that_passes(cls):
            return True, 'this check passed!'

    print(MyChecks.run())
    # (True, [])

And that's it!

Testing
-------
::

    tox
