from setuptools import setup
import os
long_description = 'Add a fallback short description here'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
setup(name='pyterminal',
      version='0.4',
      description='Make your text appear with the speed of normal handwriting',
      url='http://github.com/dr34mwh1t3/pyterminal',
      author='Dreamwhite',
      author_email='officialdreamwhite@gmail.com',
      license='GPL',
      packages=['pyterminal'],
      zip_safe=False)
