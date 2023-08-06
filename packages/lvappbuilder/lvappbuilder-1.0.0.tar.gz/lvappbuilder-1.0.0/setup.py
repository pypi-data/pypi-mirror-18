import sys
import platform
from setuptools import setup

#if sys.version_info >= (4,0,0):
#    sys.exit('Python < 3.0.0 is not supported.')

#if platform.system().lower() != 'windows':
#    sys.exit('Operatings systems other than Windows are not supported.')

setup(name='lvappbuilder',
      version='1.0.0',
      description='API for LabVIEW Application Builder.',
      url='https://github.com/gergelyk/pylvappbuilder',
      author='Grzegorz Krason',
      author_email='grzegorz@krason.biz',
      license='MIT',
      packages=['lvappbuilder'],
      package_data = {'': ['Build.vi', 'Exit.vi']},
      install_requires=[
          'xmltodict >= 0.10.2',
          'retrying >= 1.3.3',
          'regobj >= 0.2.2',
      ],
      )
