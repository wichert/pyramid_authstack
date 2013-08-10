from setuptools import setup
from setuptools import find_packages

version = '1.0.1'

install_requires = [
        'pyramid',
        'zope.interface',
    ]

test_requires = [
        'nose',
        'mock',
    ]

setup(name='pyramid_authstack',
      version=version,
      description='Use multiple authentication policies with pyramid',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Pyramid',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      author='Simplon B.V. - Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://github.com/wichert/pyramid_authstack',
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
