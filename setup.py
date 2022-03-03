from setuptools import setup, find_packages

setup(name='dtpy',
      description='Digital Twin in python',
      packages=['dtpy'],
      package_dir={'':'src'},
      install_requires=[
        'mosaik',
        'pandas',
        'fmpy',
        'pytest',
        'pyyaml'        
      ]
     )