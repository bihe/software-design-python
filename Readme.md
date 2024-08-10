# Software Design Python
This example shows a `typical` python project using Flask as the web-development framwork.

## Requirements

### Python
What is python?
> Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. 
(https://www.python.org/doc/essays/blurb/)

As this is a python example we need to install it. Systems typically have python installed, but not the most recent version. We are using `python 3.12.x` for this example.

Go to https://www.python.org/downloads/ and download python `3.12.*` for your system (mainly for Windows).

* Windows: Execute the installer as described in the python documentation (https://docs.python.org/3/using/windows.html).
* Mac: Use homebrew `brew install python@3.12`
* Linux: Use your favorite package manager - e.g. ubunut 24.04 `apt install python3.12 python3.12-venv`

**Windows NOTE**:  When you want to exectue python in a `shell` and the Windows App-Store opens, you need to deactive this Windows-Behavior: https://stackoverflow.com/questions/58754860/cmd-opens-windows-store-when-i-type-python

### Shell
Software development needs to interact with the system. Therefor we will encounter an number of CLI (command line interface) tools. To do this effectively we need to use a shell.

In a **Unix-like environments** like Mac/Linux typically a good shell is available out of the box (bash, zsh) in combination with a terminal (terminal, iTerm, Konsole, gnome-terminal, ...). 

For **Windows** a good combination of shell/terminal is [PowerShell](https://github.com/PowerShell/PowerShell)/[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/). 

**NOTE**: If you use [cmd.exe](https://en.wikipedia.org/wiki/Cmd.exe), you are without help. Nobody shoul use this old command-interpreter any more!

## Development
Best practise for any pyhton development is to start with a virtual environment. See how to to do in the official python documentation: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

> You benefit from the virtual environment since packages can be installed confidently and will not interfere with another project’s environment.

**NOTE**: A realtime virus scanning engine like [Windows Defender](https://www.microsoft.com/en-us/windows/comprehensive-security?r=1) sometimes gets in the way during development. As a result common development actions (compilation, execution of scripts, ..) take ages. To speed up the process it can make sense to disable realtime-scanning during compilation or excluce paths in the scan engine (be aware that this has a security impact!)

- [Deactivate Real-Time Scanning](https://support.microsoft.com/en-us/windows/turn-off-defender-antivirus-protection-in-windows-security-99e6004f-c54c-8509-773c-a4d776b77960)
- [Exclude Folder for Scanning](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26)

<hr/>

### 1. Create a new virtual environment

```bash
# or just pyhton (depending on the os/system used)
# one typically uses .venv
python3 -m venv <name-of-your-virtual-environment>

# use the environment

# unix-like (linux, mac)
source <name-of-your-virtual-environment>/bin/activate

# windows
.\<name-of-your-virtual-environment>\Scripts\activate
```

### 2. Install dependencies
We are using the standard python package management tool [pip](https://packaging.python.org/en/latest/guides/tool-recommendations/#installing-packages). There are a couple of other pyhton package managers out there which can be used as well (https://dev.to/adamghill/python-package-manager-comparison-1g98).

```bash
pip install -r requriments
```


