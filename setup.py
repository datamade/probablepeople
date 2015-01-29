try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    version='0.1',
    url='https://github.com/datamade/name_parser',
    description='Parse romanized names using advanced NLP methods',
    name='name_parser',
    packages=['name_parser'],
    package_data={'usaddress' : ['learned_settings.crfsuite']},
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=[
        'python-crfsuite>=0.7',
        'metaphone>=0.4'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    long_description="""
        name_parser is a python library for parsing unstructured romanized 
        name strings into name components, using conditional random fields.

        From the python interpreter:

        >>> import name_parser
        >>> name_parser.parse('Mr George "Gob" Bluth II')  
        [('Mr', 'PrefixMarital'), 
         ('George', 'GivenName'), 
         ('"Gob"', 'Nickname'), 
         ('Bluth', 'Surname'), 
         ('II', 'SuffixGenerational')]
        """
    )
