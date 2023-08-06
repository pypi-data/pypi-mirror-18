import os
import xml.sax.saxutils

from setuptools import setup


def read(*rnames):
    text = open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    text = unicode(text, 'utf-8').encode('ascii', 'xmlcharrefreplace')
    return xml.sax.saxutils.escape(text)

setup(
    name='ejabberdctl.py',
    version='0.1',
    description='Python client for Ejabberd XML-RPC Administration API',
    long_description=('{}{}{}'.format(read('README.rst'),
                                      '\n\n-----\n\n',
                                      read('CHANGELOG.rst'))),
    author='Marek Kuziel',
    author_email='marek@kuziel.nz',
    license='MIT',
    url='https://gitlab.com/markuz/ejabberdctl.py',
    packages=['ejabberdctl'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Communications'],
    keywords='ejabberd xmlrpc administration api'
)
