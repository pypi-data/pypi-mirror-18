from setuptools import setup, Extension

from os import path
from glob import glob


def readme():
    with open('README.rst') as f:
        return f.read()


def version():
    with open('iteration_utilities/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split(r"'")[1]


cfuncs_module = Extension('iteration_utilities._cfuncs',
                          sources=[path.join('src_c', '_module.c')],
                          depends=glob(path.join('src_c', '*.c'))
                          )


setup(name='iteration_utilities',
      version=version(),

      description='Functional programming utilities for Python.',
      long_description=readme(),
      keywords=['functional', 'functools', 'generator',
                'itertools', 'iteration', 'iterator',
                'operators', 'performance', 'reduce', 'utility'],
      platforms=["Windows", "Linux"],  # maybe sometime also "Mac OS-X", "Unix"

      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],

      license='MIT',

      url='https://github.com/MSeifert04/iteration_utilities',

      author='Michael Seifert',
      author_email='michaelseifert04@yahoo.de',

      packages=[
          'iteration_utilities',
          'iteration_utilities._recipes',
          'iteration_utilities._helpers',
          ],

      install_requires=[
          'setuptools',  # actually unnecessary because it's already imported at this point.
          ],

      setup_requires=[
          'pytest-runner',
          ],

      tests_require=[
          'pytest',
          ],

      ext_modules=[cfuncs_module],

      include_package_data=True,
      zip_safe=False,
      )
