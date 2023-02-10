from setuptools import setup

setup(name='nestli',
      description='Digital Twin in python',
      packages=['nestli'],
      package_dir={'':'src'},
      version="1.1.0",
      install_requires=[
        'mosaik==3.1.0',
        'pandas==1.5.2',
        'fmpy==0.3.12',
        'pytest==7.2.0',
        'pyyaml==6.0',
        'tables==3.7.0',
        'h5py==3.7.0',
        'requests==2.28.1',
        'requests_ntlm==1.1.0',
        'scipy==1.9.3'   
      ]
     )