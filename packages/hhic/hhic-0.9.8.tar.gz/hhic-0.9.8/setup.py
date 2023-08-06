from setuptools import setup

setup(name='hhic',
      version='0.9.8',
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
            ['connection/ca.key',
             'connection/ca.pem',
             'connection/ca.srl',
             'connection/client.key'
             'connection/client.pem'
             'connection/client.csr'
             'connection/server.key'
             'connection/server.pem'
             'connection/server.csr'
            ],
      'demp':
            [
             'demo/log1.txt'
             'demo/log2.txt'
             'demo/log3.txt'
            ],
      },
      zip_safe=False)