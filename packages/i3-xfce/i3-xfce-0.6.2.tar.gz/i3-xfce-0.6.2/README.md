# i3-xfce
[![Build Status](https://travis-ci.org/aacebedo/i3-xfce.svg?branch=master)](https://travis-ci.org/aacebedo/i3-xfce)
This tool will install packages and scripts in order to use i3 with xfce. Amongst other things, it replaces
the builtin windows manager (xfwm4) and disable the builtin desktop (xfdesktop).
It has been designed to work with deb packages system and more specifically with ubuntu flavor.
It has been successfully tested with ubuntu 15.04/15.10/16.04 and xubuntu 15.04/15.10/16.04.

### Dependencies
- *Ubuntu 15.04/15.10/16.04
- Python2 >=2.7.0
- python-yaml
- python-progressbar
- python-ansible
- python-pathlib


### Install dependencies
Installl pip and python using the package manager tool of your distribution.
For ubuntu the command to execute is:
```
$> apt install python python-pip
```

Then install the i3-xfce dependencies:
```
$> pip install -r ./requirements.txt
```

### Install and configure
```
$> ./setup.py install -prefix=<install path>
```
or
```
$> pip install i3-xfce
```

### Usage
##### Install all
```
$> i3-xfce install
```
##### Install parts
```
$> i3-xfce install -p <parts>
```
##### Install help
```
$> i3-xfce install -h
```
##### Uninstall all
```
$> i3-xfce uninstall
```
##### Uninstall parts
```
$> i3-xfce uninstall -p <part1> -p <part2> ... 
```
##### Uninstall help
```
$> i3-xfce uninstall -h
```

### Screenshots
![alt tag](https://raw.github.com/aacebedo/i3-xfce/master/screenshot.png)
### License
LGPL
