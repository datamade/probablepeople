try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    name='name_parser',
    packages=['name_parser'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    )