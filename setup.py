try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    version='0.5.2',
    url='https://github.com/datamade/probablepeople',
    description='Parse romanized names & companies using advanced NLP methods',
    name='probablepeople',
    packages=['probablepeople'],
    package_data={'probablepeople' : ['generic_learned_settings.crfsuite',
                                      'person_learned_settings.crfsuite',
                                      'company_learned_settings.crfsuite']},
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=[
        'python-crfsuite>=0.8',
        'probableparsing',
        'future',
        'doublemetaphone'],
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    long_description="""
        probablepeople is a python library for parsing unstructured romanized name or company strings into components, using conditional random fields.

        From the python interpreter:

        >>> import probablepeople
        >>> probablepeople.parse('Mr George "Gob" Bluth II') 
        [('Mr', 'PrefixMarital'), 
         ('George', 'GivenName'), 
         ('"Gob"', 'Nickname'), 
         ('Bluth', 'Surname'), 
         ('II', 'SuffixGenerational')]
        >>> probablepeople.parse('Sitwell Housing Inc')
        [('Sitwell', 'CorporationName'),
         ('Housing', 'CorporationName'),
         ('Inc', 'CorporationLegalType')]
        """
    )
