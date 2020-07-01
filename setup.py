from setuptools import setup

with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name = 'pyhomebridge',
    packages = ['homebridge'],
    version = '0.0.3',
    license='MIT',
    description = 'Control a homebridge server',
    long_description=README,
    long_description_content_type="text/markdown",
    author = 'mroelandts',
    author_email = 'matthias_10@hotmail.com',
    url = 'https://github.com/mroelandts/pyhomebridge',
    #download_url = 'https://github.com/mroelandts/pyhomebridge/archive/v_001.tar.gz',
    keywords = ['HomeBridge', 'HomeKit'],
    install_requires=['requests', 'argparse'],
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
