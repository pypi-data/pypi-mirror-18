from distutils.core import setup
import sys, os


setup(name='myhack',
      version='1.3',
      description="trying",
      long_description="trying",
      keywords='myhack',
      author='minus79',
      author_email='gergely06@gmail.com',
      url='https://github.com/minus79/xenon',
      download_url = 'https://github.com/minus79/xenon/tarball/0.1',
      include_package_data=True,
      zip_safe=False,
      py_modules=['myhack'],
      package_dir={'': 'myhack'}
      )
