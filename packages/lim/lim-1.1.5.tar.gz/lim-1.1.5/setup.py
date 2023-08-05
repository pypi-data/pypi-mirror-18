from __future__ import unicode_literals

import os
import sys

from setuptools import find_packages, setup


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner>=2.9'] if needs_pytest else []

    setup_requires = ['cffi>=1.7'] + pytest_runner
    install_requires = [
        'pytest>=2.9', 'scipy>=0.17', 'numpy>=1.10', 'cffi>=1.7',
        'limix_math>=1.1.8', 'progressbar2>=3.10', 'h5py>=2.6',
        'pandas>=0.18', 'nose>=1.3', 'tabulate>=0.7', 'six', 'optimix>=1.0.12',
        'limix_util>=1.0.2', 'cachetools>=2.0'
    ]
    tests_require = install_requires

    metadata = dict(
        name='lim',
        version='1.1.5',
        maintainer="Limix Developers",
        maintainer_email="horta@ebi.ac.uk",
        license="MIT",
        url='http://pmbio.github.io/limix/',
        packages=find_packages(),
        zip_safe=True,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        include_package_data=True,
        cffi_modules=['liknorm_build.py:liknorm'])

    try:
        from distutils.command.bdist_conda import CondaDistribution
    except ImportError:
        pass
    else:
        metadata['distclass'] = CondaDistribution
        metadata['conda_buildnum'] = 1
        metadata['conda_features'] = ['mkl']

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)


if __name__ == '__main__':
    setup_package()
