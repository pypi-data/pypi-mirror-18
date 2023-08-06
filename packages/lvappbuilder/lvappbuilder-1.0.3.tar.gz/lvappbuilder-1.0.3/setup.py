import sys
import platform
from path import Path
from setuptools import setup

#if sys.version_info >= (4,0,0):
#    sys.exit('Python < 3.0.0 is not supported.')

#if platform.system().lower() != 'windows':
#    sys.exit('Operatings systems other than Windows are not supported.')

package = 'lvappbuilder'
version = open(Path() / package / 'VERSION').read().strip()

setup(name=package,
      version=version,
      description='API for LabVIEW Application Builder.',
      url='https://github.com/gergelyk/py' + package,
      author='Grzegorz Krason',
      author_email='grzegorz@krason.biz',
      license='MIT',
      packages=[package],
      package_data = {'': ['VERSION', 'Build.vi', 'Exit.vi']},
      install_requires=[
          'xmltodict >= 0.10.2',
          'retrying >= 1.3.3',
          'regobj >= 0.2.2',
      ],
      )
