# Software Design Python
This example shows a `typical` python project using Flask as the web-development framework.

## Requirements

### Python
What is python?
> Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. 
(https://www.python.org/doc/essays/blurb/)

As this is a python example we need to install it. Systems typically have python installed, but not the most recent version. We are using `python 3.12.x` for this example.

Go to https://www.python.org/downloads/ and download python `3.12.*` for your system (mainly for Windows).

* Windows: Execute the installer as described in the python documentation (https://docs.python.org/3/using/windows.html).
* Mac: Use homebrew `brew install python@3.12`
* Linux: Use your favorite package manager - e.g. ubuntu 24.04 `apt install python3.12 python3.12-venv`

**Windows NOTE**:  When you want to execute python in a `shell` and the Windows App-Store opens, you need to deactivate this Windows-Behavior: https://stackoverflow.com/questions/58754860/cmd-opens-windows-store-when-i-type-python

### Shell
Software development needs to interact with the system. Therefor we will encounter an number of CLI (command line interface) tools. To do this effectively we need to use a shell.

In a **Unix-like environments** like Mac/Linux typically a good shell is available out of the box (bash, zsh) in combination with a terminal (terminal, iTerm, Konsole, gnome-terminal, ...). 

For **Windows** a good combination of shell/terminal is [PowerShell](https://github.com/PowerShell/PowerShell)/[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/). 

**NOTE**: If you use [cmd.exe](https://en.wikipedia.org/wiki/Cmd.exe), you are without help. Nobody should use this old command-interpreter anymore!

## Development
Best practice for any python development is to start with a virtual environment. See how to do in the official python documentation: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

> You benefit from the virtual environment since packages can be installed confidently and will not interfere with another project’s environment.

**NOTE**: A realtime virus scanning engine like [Windows Defender](https://www.microsoft.com/en-us/windows/comprehensive-security?r=1) sometimes gets in the way during development. As a result common development actions (compilation, execution of scripts, ..) take ages. To speed up the process it can make sense to disable realtime-scanning during compilation or exclude paths in the scan engine (be aware that this has a security impact!)

- [Deactivate Real-Time Scanning](https://support.microsoft.com/en-us/windows/turn-off-defender-antivirus-protection-in-windows-security-99e6004f-c54c-8509-773c-a4d776b77960)
- [Exclude Folder for Scanning](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26)

<hr/>

### 1. Create a new virtual environment

```bash
# or just python (depending on the os/system used)
# one typically uses .venv
# either use python or python3
python -m venv <name-of-your-virtual-environment>

# use the environment

# unix-like (linux, mac)
source <name-of-your-virtual-environment>/bin/activate

# windows
.\<name-of-your-virtual-environment>\Scripts\activate

# afterwards your shell shows the activated venv!
```

### 2. Install dependencies
We are using the standard python package management tool [pip](https://packaging.python.org/en/latest/guides/tool-recommendations/#installing-packages). There are a couple of other python package managers out there which can be used as well (https://dev.to/adamghill/python-package-manager-comparison-1g98). 

Python has introduced a `standard` way how a python project should be defined (metadata and including dependencies): [pep-0621](https://peps.python.org/pep-0621/) /  [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml).

The dependencies for this project are defined within the `pyproject.toml` within the `dependencies` section. To install the dependencies the following command is used.

```bash
# install the dependencies
pip install .
# uninstall our app because we are developing it
pip uninstall restaurant_app
```

#### Optional dependencies
To generate class-diagrams from the given project we use `pyreverse` which is part of the [pylint](https://pylint.pycqa.org/en/latest/pyreverse.html) package. The application works without the optional dependency as well!

```bash
# [optional] needed to generate class-diagram
pip install pylint
```
