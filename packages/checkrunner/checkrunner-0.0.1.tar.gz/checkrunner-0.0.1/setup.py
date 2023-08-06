from setuptools import setup, find_packages

setup(name='checkrunner',
      use_scm_version=True,
      description='A simple check runner for Python',
      url='https://github.com/al4/python-checkrunner',
      author='Alex Forbes',
      author_email='github@al4.co.nz',
      license='MIT',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=['tests']),
      setup_requires=[
          'setuptools_scm',
          'pytest-runner',
      ],
      tests_require=[
          'pytest',
          'tox'
      ],
      zip_safe=False)
