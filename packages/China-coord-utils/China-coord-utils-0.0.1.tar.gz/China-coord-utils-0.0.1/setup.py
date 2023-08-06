#!/usr/bin/env python

from setuptools import setup


setup(
    name='China-coord-utils',
    version='0.0.1',
    url='https://coding.net/u/lvzhaoxing/p/China-coord-utils',
    license='MIT',
    author='Lv Zhaoxing',
    author_email='lvzhaoxing@qq.com',
    description='Convenient utils for China coordinate.',
    long_description='Convenient utils for China coordinate. Please visit: https://coding.net/u/lvzhaoxing/p/China-coord-utils',
    py_modules=['China_coord_utils'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    keywords='gcj',
    #packages=[],
    package_data={'': ['LICENSE']},
    install_requires=[
        'setuptools'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
