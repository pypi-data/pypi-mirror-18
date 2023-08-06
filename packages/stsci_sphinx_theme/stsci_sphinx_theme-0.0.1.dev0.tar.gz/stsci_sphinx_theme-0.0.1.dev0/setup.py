import os
from setuptools import setup

setup(
    name='stsci_sphinx_theme',
    version='0.0.1-dev',
    author='Justin Ely',
    author_email='ely@stsci.edu',
    packages=['stsci_sphinx_theme'],
    package_data={'stsci_sphinx_theme': [
                 'theme.conf',
                 '*.html',
                 'static/*'
    ]},
    include_package_data=True,
    url='https://github.com/spacetelescope/stsci_sphinx_theme/',
    license='BSD',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=('sphinx>=1.1', )
)
