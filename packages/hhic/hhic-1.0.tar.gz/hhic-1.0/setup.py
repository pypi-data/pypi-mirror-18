from setuptools import setup

setup(name='hhic',
      version='1.0',
      description='(homomorphic hash integrity checker) integrity checker for homomorphic ciphers with homomorphic hashes',
      url='',
      author='Samim Faiz',
      author_email='mhsamim.faiz@gmail.com',
      packages=['hhic'],
      install_requires=[
          'gensafeprime==1.5', 'rsa==3.4.2', 'phe==1.2.3',
      ],
      include_package_data=True,
      package_date={
      'connection':
            ['hhic/connection/ca.key',
             'hhic/connection/ca.pem',
             'hhic/connection/ca.srl',
             'hhic/connection/client.key'
             'hhic/connection/client.pem'
             'hhic/connection/client.csr'
             'hhic/connection/server.key'
             'hhic/connection/server.pem'
             'hhic/connection/server.csr'
            ],
      'demp':
            [
             'hhic/demo/log1.txt'
             'hhic/demo/log2.txt'
             'hhic/demo/log3.txt'
            ],
      },
      zip_safe=False)