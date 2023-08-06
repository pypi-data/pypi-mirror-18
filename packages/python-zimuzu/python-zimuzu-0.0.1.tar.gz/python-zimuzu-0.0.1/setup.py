# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

import zimuzu

with open('README.md', 'rb') as readme_file:
    readme = readme_file.read().decode('utf-8')
with open('HISTORY.md', 'rb') as history_file:
    history = history_file.read().decode('utf-8')
with open('requirements.txt', 'rb') as fp:
    install_requires = fp.read().decode('utf-8').split()

setup(
    name=zimuzu.__title__,
    version=zimuzu.__version__,
    license=zimuzu.__license__,
    description=zimuzu.__doc__,
    long_description=readme + '\n\n' + history,
    url='https://github.com/er1iang/python-zimuzu',
    keywords=('zimuzu', 'api', 'sdk', 'service'),

    packages=find_packages(),
    platforms='any',
    python_requires='>=3.3',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'zimuzu=zimuzu.command:cli',
        ],
    },
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: SDK',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
