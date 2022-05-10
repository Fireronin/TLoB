# TLoB:ALttc
Legend of Bluespec: A Link to the components.

This is a tool for quick generation of high-level Bluespec SystemVerilog components. This repository also has a related repository with files for rendering GUI. It is meant to run as a desktop application, and not as a cloud one.

# Installation
If you are reading this then you have probably unpacked the repository.
Good job, but double check if you are on Windows wsl2 that directory with this code is case-sensitive.

This code assumes that there is a Bluespec compiler installed and symbolically linked to the directory:

    /opt/tools/bsc/latest/bin/bluetcl

Some examples use Flute libraries and assume that there is a source directory "Flute" with a copy of https://github.com/CTSRD-CHERI/Flute in it and libraries are compiled. (To save time I keep a copy of it)
To compile Flute, you might also need to have a copy of the BlueSpec compiler from CHERI (again to just unpack bsc.tar.gz and link it to the above-mentioned folder).


## GUI
GUI is kept as a separate directory due to performance reasons.
(I developed this project on Windows using WSL2 and if the files are kept in /mnt/* then time node_modules become very slow to install etc.)

To install it you just need to do:

    yarn install

(If you are unlucky you might also need to update the node engine to 16 as Ubuntu has a tendency to install node 9.0 by default.)

## Python packages:
Main packages that need to be installed with python 3.9:

- lark
- sympy
- pexpect
- pypy
- tqdm
- thefuzz
- colorama
- wrapt_timeout_decorator

For GUI
- Django (for GUI)

To generate graphs in dissertation
- plotly.express
- pandas

# Running
## JSON interface
    python jsonInterface.py --json_file example.json

Use --help for more information.
   
## GUI
    cd src/tlob
    Python - manage.py runserver

Then go to the directory with JS and run:

    yarn start

## Debugging
    python main*.py

These scripts mirror example json files, but they are also very simple as they don't need to parse JSON files.

# Testing
To run tests, use one that must be installed:

- pytest
- pytest-cov

To run tests use (there is already made config):

    pytest

Tests are used to check integration of the code, and they are not very detailed unit tests, but they produce high code coverage and due to how the code is structured errors should propagate and cause crashes of the program. If an error occurs while parsing files saved/failed_*.json will be generated with sections of bluetcl output that have produced errors.
