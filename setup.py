#!/usr/bin/env python

from setuptools import setup

setup(
    name='population-estimator',
    packages=['population_estimator'],
    version='1.0.0',
    include_package_data=True,
    description='A TUI app for accessing annual population estimates',
    author='Anthony Cruz',
    author_email='cruzanta@outlook.com',
    license='MIT',
    entry_points={'console_scripts': [
        'population-estimator = population_estimator.tui_app:main']},
    url='https://github.com/cruzanta/population_estimator',
    download_url='https://github.com/cruzanta/population_estimator/archive/1.0.0.tar.gz',
    keywords=['population', 'tui', 'curses'],
    classifiers=[],
)
