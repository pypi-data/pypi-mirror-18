import os
import glob
import json
from setuptools import setup
from setuptools import find_packages
from distutils.core import setup
from Cython.Build import cythonize

# python3 setup.py register -r pypitest

# UNIX:
# rm -rf ./dist
# python3 setup.py sdist bdist_wheel
# twine upload dist/measure*
# python3 conda-recipe/conda-builder.py

# WINDOWS:
# rmdir dist /s /q
# python setup.py sdist bdist_wheel
# twine upload dist/measure*
# python conda-recipe\conda-builder.py

my_directory = os.path.realpath(os.path.dirname(__file__))

cython_glob_path = os.path.join(my_directory, '**', '*.pyx')
cython_files = cythonize(
    [p for p in glob.iglob(cython_glob_path, recursive=True)]
)

settings_path = os.path.join(my_directory, 'measurement_stats', 'settings.json')
with open(settings_path, 'r+') as f:
    settings = json.load(f)


def read_me():
    with open('README.rst') as f:
        return f.read()


def populate_extra_files():
    """
    Creates a list of non-python data files to include in package distribution
    """

    out = ['measurement_stats/settings.json']

    for entry in glob.iglob('measurement_stats/resources/**/*', recursive=True):
        out.append(entry)

    return out


setup(
    name='measurement_stats',
    version=settings['version'],
    description=
            'Measurement statistics with uncertainties and error propagation',
    long_description=read_me(),
    url='https://github.com/sernst/Measurement_Statistics',
    author='Scott Ernst',
    author_email='swernst@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={'': populate_extra_files()},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    ext_modules=cython_files,
    install_requires=[
        'pandas',
        'numpy',
        'six',
        'scipy'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    keywords='measurements statistics uncertainty error propagation',
)
