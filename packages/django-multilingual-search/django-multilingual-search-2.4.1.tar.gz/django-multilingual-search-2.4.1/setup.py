# coding: utf-8
from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Hard linking doesn't work inside VirtualBox shared folders. This means that
# you can't use tox in a directory that is being shared with Vagrant,
# since tox relies on `python setup.py sdist` which uses hard links. As a
# workaround, disable hard-linking if setup.py is a descendant of /vagrant.
# See
# https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
# for more details.
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link

setup(
    name='django-multilingual-search',
    version='2.4.1',
    packages=['multilingual'],
    url='https://github.com/sbaechler/django-multilingual-search',
    license='BSD',
    author='Simon Bächler',
    author_email='b@chler.com',
    description='A drop-in replacement for the Haystack Elasticsearch backend which allows '
                'multilingual indexes for Django.',
    long_description=read('README.rst'),
    platforms=['OS Independent'],
    install_requires=[
        'Django>=1.5',
        'django-haystack==2.4.1',
        'elasticsearch>=1.6.0,<1.8'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
