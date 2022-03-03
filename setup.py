from setuptools import setup, find_packages

setup(name='dtpy',
      description='Digital Twin in python',
      author='Aaron Bojarski',
      packages=['DTpy'],
      package_dir={'':'src'},
      install_requires=[
        'mosaik',
        'pandas',
        'fmpy',
        'pytest',
        'pyyaml'        
      ]
     )