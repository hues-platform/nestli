##############
Installation
##############


Local python Installation
##########################

EnergyPlus
------------
Make sure you get the correct version.

1. Install Energyplus 9.3.0
2. Add it to your PATH


Python
------------

1. Install python version 3.8 or higher.
2. Create a virtual environment: :code:`python -m venv path/to/env/nestli-venv`
3. Activate the environment.


nestli package
---------------

1. Clone the repository onto you machine
2. cd to the directory where you cloned it into
3. Install the package with: :code:`pip install -e .` 
   This will install the nestli package according to setup.py.



Docker
#######
To run the simulation in Docker you just need to have Docker installed.
Then clone the repository and navigate to it. 

You create a Docker image with:
::

    docker build . -t nestli

