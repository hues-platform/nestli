from setuptools import setup

setup(name='dtpy',
      description='Digital Twin in python',
      packages=['dtpy'],
      package_dir={'':'src'},
      version="0.1.0",
      install_requires=[
        'mosaik',
        'pandas',
        'fmpy',
        'pytest',
        'pyyaml',
        'tables',
        'h5py'   
      ]
     )