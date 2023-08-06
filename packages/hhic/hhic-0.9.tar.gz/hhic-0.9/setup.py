from setuptools import setup

setup(name='hhic',
      version='0.9',
      description='(homomorphic hash integrity checker) integrity checker for homomorphic ciphers with homomorphic hashes',
      url='',
      author='Samim Faiz',
      author_email='mhsamim.faiz@gmail.com',
      packages=['hhic'],
      install_requires=[
          'gensafeprime==1.5', 'rsa==3.4.2', 'phe==1.2.3,',
      ],
      zip_safe=False)