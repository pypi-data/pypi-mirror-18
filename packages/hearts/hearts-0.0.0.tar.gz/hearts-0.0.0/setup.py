# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from setuptools import setup


name = 'hearts'

setup(
  name=name,
  version='0.0.0',
  license='MIT',
  author='George King',
  author_email='george.w.king@gmail.com',
  url='https://github.com/gwk/' + name,
  description='A simple charting library. Derived from https://github.com/wireservice/leather.',
  long_description=open('readme.wu').read(),
  packages=[name],
  entry_points = {'console_scripts': [
  ]},
  install_requires=[
  ],
  keywords=[
  ],
  classifiers=[ # See https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Programming Language :: Python :: 3 :: Only',
  ],
)
