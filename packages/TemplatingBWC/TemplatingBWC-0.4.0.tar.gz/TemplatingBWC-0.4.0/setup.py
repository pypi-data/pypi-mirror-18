import os
from setuptools import setup, find_packages

import templatingbwc

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(cdir, 'readme.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'changelog.rst')).read()
VERSION = open(os.path.join(cdir, 'templatingbwc', 'version.txt')).read().strip()

setup(
    name = "TemplatingBWC",
    version = VERSION,
    description = "A BlazeWeb component with template themes",
    long_description=README + '\n\n' + CHANGELOG,
    author = "Randy Syring",
    author_email = "randy.syring@level12.io",
    url='https://github.com/blazelibs/templatingbwc/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP'
      ],
    license='BSD',
    packages=find_packages(exclude=['templatingbwc_*']),
    include_package_data = True,
    install_requires = [
        'BlazeForm>=0.3.0',
        'BlazeWeb>0.4.4',
    ],
    zip_safe=False
)
