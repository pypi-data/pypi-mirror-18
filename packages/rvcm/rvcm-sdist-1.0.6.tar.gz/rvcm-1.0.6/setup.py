from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rvcm',
    version='1.0.6',
    description='Control RV6688BCM router',
    long_description=long_description,
    url='https://github.com/reddec/router-control',
    author='Baryshnikov Alexander',
    author_email='dev@baryshnikov.net',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='RV6688BCM router-control gpon rvcm',
    install_requires=['click', 'requests', 'lxml'],
    entry_points={
        'console_scripts': [
            'rvcm=rvcm.cli:cli'
        ]
    }
)
