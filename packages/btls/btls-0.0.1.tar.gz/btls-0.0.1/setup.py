# coding=utf-8
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='btls',
      version='0.0.1',
      description='brucezz\'s toolbox',
      long_description=readme(),
      keywords='python tools',
      url='https://github.com/brucezz/btls',
      author='Brucezz',
      author_email='im.brucezz@gmail.com',
      license='MIT',
      packages=['btls'],
      install_requires=[
          'yagmail'
      ],
      test_suite="tests",
      zip_safe=False,
      include_package_data=True)
