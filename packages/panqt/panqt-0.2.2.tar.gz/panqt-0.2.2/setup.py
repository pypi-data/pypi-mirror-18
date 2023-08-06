

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import re
import sys

has_qt4 = True
try:
    # TODO: sip is only needed for PyQt4, they should be imported together.
    import PyQt4
    import sip
except ImportError as e:
    has_qt4 = False

try:
    import PySide
except ImportError as e:
    # TODO: try to import PySide.
    if not has_qt4:
        #We know we failed to import PyQt4/sip...
        #And we failed to import pyside.
        raise ImportError( "\n\ninstall PyQt4 and sip or PySide")
    else:
        print("Using PyQt4")



here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'panqt', '__init__.py'), 'rU')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [ line.strip() for line in version_file if '__version__' in line ].pop(0)
)
version_file.close()

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

tests_require = ['easygui', 'pandas == 0.17.1', 'pyside', 'pytest', 'pytest-cov', 'pytest-qt', 'python-magic==0.4.6']
setup(
    name='panqt',
    version=__version__,
    url='https://github.com/datalyze-solutions/panqt',
    license='MIT License',
    namespace_packages = ['panqt'],
    author='Matthias Ludwig, Marcel Radischat',
    tests_require=tests_require,
    install_requires=['easygui', 'pandas==0.17.1', 'pytest', 'pytest-qt==1.2.2', 'pytest-cov', 'python-magic==0.4.6'],
    cmdclass={'test': PyTest},
    author_email='m.Ludwig@datalyze-solutions.com',
    description='Utilities to use pandas (the data analysis / manipulation library for Python) with Qt.',
    long_description=long_description,

    include_package_data=True,
    packages=['panqt'],

    platforms='any',
    test_suite='tests',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: German',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces'
        ],
    extras_require={
        'testing': tests_require,
    }
)
