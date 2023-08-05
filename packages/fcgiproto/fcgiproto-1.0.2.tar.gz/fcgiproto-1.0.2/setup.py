# coding: utf-8
import os.path

from setuptools import setup, find_packages


here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = open(readme_path).read()

setup(
    name='fcgiproto',
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    description='FastCGI state-machine based protocol implementation',
    long_description=readme,
    author=u'Alex Grönholm',
    author_email='alex.gronholm@nextday.fi',
    url='https://github.com/agronholm/fcgiproto',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='fastcgi http',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=['setuptools_scm']
)
