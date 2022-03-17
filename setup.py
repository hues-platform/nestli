from setuptools import setup

setup(name='dtpy',
      description='Digital Twin in python',
      packages=['dtpy'],
      package_dir={'':'src'},
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