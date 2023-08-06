from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pi_gcs',

    version='0.1',

    description='Unofficial python wrapper for Physik Instrumente General Command Set API',
    long_description=long_description,

    url='https://github.com/lbusoni/pi_gcs',

    author='Lorenzo Busoni',
    author_email='lbusoni@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='PI GCS2 GCS',

    packages=['pi_gcs'],
    include_package_data=True,
)
