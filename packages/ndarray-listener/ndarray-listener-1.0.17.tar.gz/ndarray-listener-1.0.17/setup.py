import os
import sys
from setuptools import setup
from setuptools import find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(OSError, IOError, ImportError):
    long_description = open('README.md').read()


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner'] if needs_pytest else []

    setup_requires = [] + pytest_runner
    install_requires = ['numpy>=1.9']
    tests_require = ['pytest']

    metadata = dict(
        name='ndarray-listener',
        version='1.0.17',
        maintainer="Danilo Horta",
        maintainer_email="horta@ebi.ac.uk",
        license="MIT",
        url='https://github.com/glimix/ndarray-listener',
        packages=find_packages(),
        zip_safe=True,
        description="Implementation of the Observer pattern for NumPy arrays.",
        long_description=long_description,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        include_package_data=True,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Operating System :: OS Independent",
        ],
    )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)

if __name__ == '__main__':
    setup_package()
