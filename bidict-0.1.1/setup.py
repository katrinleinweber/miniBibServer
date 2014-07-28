from setuptools import setup, find_packages

version = '0.1.1'
try:
    import os
    doc_dir = os.path.join(os.path.dirname(__file__), 'docs')
    readme = open(os.path.join(doc_dir, 'README.rst'))
    long_description = readme.read()
except IOError:
    try:
        import bidict
        long_description = bidict.__doc__
    except:
        long_description = """\
bidict
======

``bidict`` provides a bidirectional mapping data structure and related
utilities (``namedbidict``, ``inverted``) to naturally model one-to-one
relations in Python. To keep the learning curve low, it introduces no new
functions to the ``dict`` API you're already familiar with. It owes its
simplicity to Python's slice syntax, which provides a handy and natural way
of expressing the inverse mapping in a ``bidict``::
    
    >>> husbands2wives = bidict({'john': 'jackie'})
    >>> husbands2wives['john'] # the forward mapping is just like with dict
    'jackie'
    >>> husbands2wives[:'jackie'] # use slice for the inverse mapping
    'john'

You can also use the unary inverse operator ``~`` on a bidict to get the
inverse mapping::

    >>> ~husbands2wives
    bidict({'jackie': 'john'})


More examples are available in the module documentation.
"""

long_description += """
----------
Background
----------

This module evolved from a November 2009 thread on comp.lang.python
(`link <http://groups.google.com/group/comp.lang.python/browse_frm/thread/785d100681f7d101/34703a66338abbd6>`_).
Thanks to Terry Reedy, Raymond Hettinger, and Francis Carr for their ideas.

Please find `bidict on bitbucket <http://bitbucket.org/jab/bidict>`_ if you
would like to collaborate.
"""

setup(
    name='bidict',
    version=version,
    author='Josh Bronson',
    author_email='jabronson@gmail.com',
    description="bidirectional (one-to-one) mapping data structure",
    long_description=long_description,
    keywords='mapping, bidirectional, bijection, injective, dict, dictionary',
    url='http://bitbucket.org/jab/bidict',
    license='MIT',
    py_modules=['bidict'],
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        ],
    )
