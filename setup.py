import os
from setuptools import setup

setup(
    name='django-searchable-select',
    version='0.5',
    description='django-searchable-select - a better and faster multiple selection widget with suggestions for Django',
    long_description='A better and faster multiple selection widget with suggestions for Django. Provides replacement for standard widget of ManyToManyField.',
    author="Andrew Dunai",
    author_email='andrew@dun.ai',
    url='https://github.com/and3rson/django-searchable-select',
    license='GPLv2',
    packages=['searchableselect'],
    include_package_data=True,
    install_requires=['setuptools', 'django'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='django,admin,suit,select,multiple,faster,choice',
)
