""" OpenBikes packaging instructions. """

from setuptools import setup, find_packages
from obpy import __version__, __author__, __project__, __licence__

README = 'README.md'
REQUIREMENTS = ['requests==2.11.1']


def long_description():
    """Insert README.md into the package."""
    try:
        with open(README) as readme_fd:
            return readme_fd.read()
    except IOError:
        return 'Failed to read README.md'


setup(
    name=__project__,
    version=__version__,
    url='https://github.com/OpenBikes/obpy/',
    download_url='https://github.com/openbikes/obpy/archive/1.0.0.tar.gz',
    description='OpenBikes API library',
    author=__author__,
    author_email='contact.openbikes@gmail.com',
    packages=find_packages(),
    long_description=long_description(),
    install_requires=REQUIREMENTS,
    keywords='openbikes api client sdk',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    licence=__licence__,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
