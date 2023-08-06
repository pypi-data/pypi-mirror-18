import os

from static_import import __version__, __email__, __owner__, __license__
from setuptools import find_packages, setup

short_description = 'Add static files never was so easy.'
packages = find_packages()
package_data = { 'static_import': ['templates/*'] }

current_dir = os.path.dirname(os.path.abspath(__file__))
long_description = open(os.path.join(os.path.dirname(__file__), "README.md"), "r").read()


setup(
    name='django_staticimport',
    version=__version__,
    url='https://github.com/leoxnidas/django_staticimport',
    download_url='https://github.com/leoxnidas/django_staticimport',
    license=__license__,
    description=short_description,
    long_description=long_description,
    author=__owner__,
    author_email=__email__,
    packages=packages,
    package_data=package_data,
    keywords='django_staticimport static_import static files static django',
    platforms=['any'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
