from setuptools import setup, find_packages

setup(name='citrination',
      version='1.0.7',
      url='http://github.com/CitrineInformatics/python-citrination-cli',
      description='Command line interface for interacting with Citrination sites',
      packages=find_packages(),
      install_requires=[
            'argparse',
            'pyCLI==2.0.3',
            'citrination-client==1.1.16'
      ],
      entry_points={
            'console_scripts': [
                  'citrination=citrination.__main__:main'
            ]
      })
