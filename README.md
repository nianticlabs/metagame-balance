# Pokémon VGC AI Framework

(Legacy repository: https://gitlab.com/DracoStriker/simplified-pokemon-environment)

## Installation

1. Install Python 3.6.8 or higher.

2. Clone this project.

3. Install the requirements.txt

4. Use you preferred Interactive Development Environment.

Alternatively you may use the Dockerfile to create a ready to run container. All dependencies
are installed in the venv vgc-env and project is found in the /vgc-ai folder. User root has
vgc as password. A SSH server is installed and run on the container boot.

## Project Organization

In the competitor module you can store your developed agents to be used as plugins. There is a 
small provided example.

In the example module can be found multiple how to use the framework examples  to train or test
isolated agents or behaviours or run full ecosystems.

In the framework module is the core implementation of the VGC AI Framework.

In the test module is contained some unit tests from the core framework modules.

## Documentation

All the documentation from Applicational Programming Interface and Framework architecture can be
found in the [wiki](https://gitlab.com/DracoStriker/pokemon-vgc-engine/-/wikis/home).

## TODO

* Graphical User Interface and Rendering
* Agents as inter-process clients
* Meta-Game Structure
* Balance Evaluation and Criteria
* Re-tune challenge difficulty
* Restriction Language Implementation
* Add Baseline Agents
* Prepare easy entry points for training and testing and running the competition