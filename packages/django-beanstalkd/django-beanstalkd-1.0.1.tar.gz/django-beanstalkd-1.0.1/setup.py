# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


version = '1.0.1'


setup(
    name='django-beanstalkd',
    version=version,
    description='A convenience wrapper for beanstalkd clients and workers in Django using the beanstalkc library for Python',
    long_description=open('README.md').read(),
    author='Kimi Huang',
    author_email='kimi.huang@brightcells.com',
    url='https://github.com/beanstalkdclub/django-beanstalkd',
    license='MPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyyaml', 'beanstalkc', 'django_six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
