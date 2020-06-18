from setuptools import setup

setup(
  name = 'pyhomebridge',
  packages = ['homebridge'],
  version = '0.0.1',
  license='MIT',
  description = 'Control a homebridge server',
  author = 'MRoelandts',
  author_email = 'matthias_10@hotmail.com',
  url = 'https://github.com/MatthiasRoelandts/pyhomebridge',
  #download_url = 'https://github.com/MatthiasRoelandts/pyhomebridge/archive/v_01.tar.gz',
  keywords = ['HomeBridge', 'HomeKit'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
