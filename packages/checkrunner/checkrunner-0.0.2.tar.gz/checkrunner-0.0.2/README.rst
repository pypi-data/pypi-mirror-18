python-checkrunner
==================
A very simple check runner for Python. I use this in projects where I need to run a suite of checks before performing some action (usually on invocation). In this way, the checks are kept together in one class, and no special logic is needed to run them all individually.

Supports Python 2 and 3 (tested on 2.7 and 3.4).

Usage
-----
Create a sub-class of CheckRunner and declare your checks::

    from checkrunner import CheckRunner

    class MyChecks(CheckRunner):
        @staticmethod
        def check_that_passes():
            return True, 'this check passed!'

        @staticmethod
        def check_that_fails():
            return False, 'this check failed!'

    print(MyChecks.run())
    # (False, ['this check failed!'])

    print(MyChecks.run(return_passed=True))
    # (False, ['this check passed!', 'this check failed!'])


When all checks pass it will return True with an empty list (unless you set return_passed)::

    from checkrunner import CheckRunner

    class MyChecks(CheckRunner):
        @staticmethod
        def check_that_passes():
            return True, 'this check passed!'

    print(MyChecks.run())
    # (True, [])


You can pass keyword arguments to the checks (they will be sent to each and every check)::

    from checkrunner import CheckRunner

    class MyChecks(CheckRunner):
        @staticmethod
        def check_foo(foo=None):
            if foo:
                return True, foo
            else:
                return False, foo

    print(MyChecks.run(foo='bar', return_passed=True))
    # (True, ['bar'])

Class methods also work::

    from checkrunner import CheckRunner


    class MyChecks(CheckRunner):
        foo = 'bar'

        @classmethod
        def check_class(cls):
            return True, cls.foo

    print(MyChecks.run(return_passed=True))
    # (True, ['bar'])

You can also return whatever you like in the second parameter, it does not have to be a string.


Testing
-------
Testing uses vagrant, tox and pytest. If you already have Vagrant, running the tests yourself is as simple as::

    $ vagrant up
    $ vagrant ssh
    (dev) vagrant@debian-8:~$ cd ~/src
    (dev) vagrant@debian-8:~/src$ tox

