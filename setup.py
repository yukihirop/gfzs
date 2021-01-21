import os, sys
import io
from setuptools import setup, Command

# local

import gfzs.info as info

HERE = os.path.abspath(os.path.dirname(__file__))

def long_description():
  with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    return '\n' + f.read()

def requires_from_file(filename):
  return open(filename).read().splitlines()


class UploadCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()

setup(
  name=info.__name__,
  version=info.__version__,
  description=info.__description__,
  long_description=long_description(),
  long_description_content_type='text/markdown',
  author=info.__author__,
  author_email=info.__author_email__,
  url=info.__url__,
  licence=info.__license__,
  keywords='google fuzzy-finder finder curses tui',
  packages=["gfzs"],
  scripts=["bin/gfzs"],
  install_requires=requires_from_file("requirements.txt"),
  include_package_data=True,
  python_requires='>=3',
  classiffiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6.1',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Environment :: Console :: Curses',
    'Topic :: Text Processing :: Filters',
    'Topic :: Utilities',
  ],
  # https://github.com/navdeep-G/setup.py/blob/master/setup.py
  # $ setup.py publish support.
  cmdclass={
        'upload': UploadCommand,
  },
  zip_safe = True
)
