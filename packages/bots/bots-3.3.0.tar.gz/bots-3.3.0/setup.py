# -*- coding: utf-8 -*-
"""A setuptools based setup module.

For more information, please see
- https://pypi.python.org/pypi/setuptools
- https://pythonhosted.org/setuptools
- https://python-packaging-user-guide.readthedocs.io/en/latest/distributing/
- https://packaging.python.org/en/latest/distributing.html
- https://github.com/pypa/sampleproject

"""
from __future__ import absolute_import, division, print_function

import io
import os
import setuptools

#from distutils.core import setup
#from distutils.command.install import INSTALL_SCHEMES


def read(*names, **kwargs):
    """Return the contents of a file.

    Default encoding is UTF-8, unless specified otherwise.

    Args:
        - names (list, required): list of strings, parts of the path.
          the path might be relative to the current file.

    Keyword Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
      String containing the content of the file.

    Examples:
        >>> read('docs/readme.rst')
            u'Overview\n--------\n...'

        >>> read('docs', 'readme.rst')
            u'Overview\n--------\n...'

    """
    fn = os.path.join(os.path.dirname(__file__), *names)
    with io.open(fn, encoding=kwargs.get('encoding', 'utf8')) as fd:
        return fd.read()


version = '3.3.0'

long_description = (
    read('readme.rst') +
    '\n\n' +
    read('changes.rst')
    #'\n\n' +
    #read('docs', 'contributors.rst')
    )




##install data file in the same way as *.py
#for scheme in INSTALL_SCHEMES.values():
    #scheme['data'] = scheme['purelib']


#def fullsplit(path, result=None):
#    '''
#    Split a pathname into components (the opposite of os.path.join) in a
#    platform-neutral way.
#    '''
#    if result is None:
#        result = []
#    head, tail = os.path.split(path)
#    if head == '':
#        return [tail] + result
#    if head == path:
#        return result
#    return fullsplit(head, [tail] + result)


## Compile the list of packages available, because distutils doesn't have
## an easy way to do this.
#packages, data_files = [], []
#root_dir = os.path.dirname(__file__)
#if root_dir != '':
    #os.chdir(root_dir)

#for dirpath, dirnames, filenames in os.walk('bots'):
    ## Ignore dirnames that start with '.'
    ##~ for i, dirname in enumerate(dirnames):
        ##~ if dirname.startswith('.'): del dirnames[i]
    #if '__init__.py' in filenames:
        #packages.append('.'.join(fullsplit(dirpath)))
        #if len(filenames) > 1:
            #data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames if not f.endswith('.pyc') and not f.endswith('.py')]])
    #elif filenames:
        #data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames if not f.endswith('.pyc') and not f.endswith('.py')]])


setuptools.setup(
    name = 'bots',
    version = version,
    author = 'hjebbers',
    author_email = 'hjebbers@gmail.com',
    url = 'https://github.com/bots-edi/bots',
    description = 'Bots open source edi translator',
    long_description = long_description,
    platforms = 'OS Independent (Written in an interpreted language)',
    license = 'GNU General Public License (GPL)',
    keywords='edi edifact x12 tradacoms xml fixedfile csv',
    packages=setuptools.find_packages(exclude=['ez_setup', 'tests']),
    #packages=setuptools.find_packages('src'),
    #package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Communications',
        'Environment :: Console',
        'Environment :: Web Environment',
        ],
    scripts = [
        'bots-webserver.py',
        'bots-engine.py',
        'bots-grammarcheck.py',
        'bots-xml2botsgrammar.py',
        'bots-updatedb.py',
        'bots-dirmonitor.py',
        'bots-jobqueueserver.py',
        'bots-plugoutindex.py',
        'bots-job2queue.py',
        ],
    #packages = packages,
    #data_files = data_files,
    )
