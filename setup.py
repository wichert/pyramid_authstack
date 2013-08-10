from setuptools import setup
from setuptools import find_packages

version = '1.0.0'

install_requires = [
        'pyramid',
        'zope.interface',
    ]

test_requires = [
        'mock',
    ]

setup(name='pyramid_multiauth',
      version=version,
      description='Use multiple authentication policies with pyramid',
      long_description=open('README.rst').read(),
      author='Simplon B.V. - Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://github.com/wichert/pyramid_multiauth',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      tests_require=test_requires,
      extras_require={
          'tests': test_requires,
      },
      )
