# ffpdf
## Fast PDF and Image File Operations

<!-- Badges -->
![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Platform](https://img.shields.io/badge/platform-Linux,%20Windows,%20macOS-green) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**ffpdf** is a command-line tool designed to easily perform file operations like merging PDFs or images, slicing PDFs, and converting between images and PDFs.


## Table of Contents

- [Commands](#commands)
  - [Examples](#examples)
    - [Merge](#merge)
    - [Slice](#slice)
    - [Count](#count)
    - [Convert](#convert)
- [Download](#download)
  - [Base Env (Easier)](#base-env-easier)
  - [Virtual Env (Recommended)](#virtual-env-recommended)
    - [1. Dependencies](#1-dependencies)
      - [uv](#uv)
      - [pip](#pip)
    - [2. ffpdf bin file](#2-ffpdf-bin-file)
      - [Linux and macOS](#linux-and-macos)
      - [Windows](#windows)



# Commands
Show command usages
```sh
ffpdf

Commands:              Times Used:
——————————————————————————————————————
   1. merge                     32
   2. slice                     13
   3. count                      9
   4. convert                   15
——————————————————————————————————————
      Total:                    69
```


|Subcommand|Description|
|-|-|
|`merge`|Merge the input files (PDFs or images) in an output PDF|
|`slice`|Extract pages from a PDF|
|`count`|Count the pages of every PDF in input|
|`convert`|Convert input files in the specified format (image or pdf)|

## Examples
### Merge
Merge the input files (PDFs or images) in an output PDF
```sh
ffpdf merge a.pdf b.pdf -o ab.pdf
```
### Slice
Extract pages from a PDF
```sh
ffpdf slice in.pdf 1,3,5-8 out.pdf

# out.pdf has only the pages number 1,3,5,6,7,8 of the in.pdf
```

### Count
Count the pages of every PDF in input
```sh
ffpdf count a.pdf

Pages    Filename                   
——————————————————————————————————————————————————
    4    'a.pdf'                           
```

```sh
ffpdf count *.pdf

Pages    Filename                   
——————————————————————————————————————————————————
   42    'a.pdf'                                 
    1    'b.pdf'                                 
    0    'c.pdf' (empty file)
    4    'd.pdf'                                        
```
### Convert
Convert input files in the specified format (image or pdf)
```sh
ffpdf convert a.pdf b.jpg c.png -e .png

Converted 'a.pdf' (4 pages) to '.png'
Converted 'b.jpg' to 'b.jpg(3).png'
Skipped   'c.png' (no conversion is needed)
```


# Download
There are two different ways, choose one:
- [Base Env (Easier)](#base-env-easier)
- [Virtual Env (Recommended)](#virtual-env-recommended)

## Base Env (Easier)
You can install this package (if compatible with python version and other dependencies) in your main python installation with pip. Just open a shell in the main project and type:
```sh
pip install -e .  # -e for editable mode
```
Uninstall:
```sh
pip uninstall .
```

## Virtual Env (Recommended)

### 1. Dependencies
#### [uv](https://github.com/astral-sh/uv)
```sh
uv sync
```
or
```sh
# create virtual env
uv venv

# activate env
source .venv/bin/activate  # linux or mac
.venv\Scripts\activate  # windows

# install requirements
uv pip install -e .  # -e for editable mode
```
#### pip
```sh
# create virtual env
python -m venv .venv

# activate env
source .venv/bin/activate  # linux or mac
.venv\Scripts\activate  # windows

# install requirements
pip install -e .  # -e for editable mode
```

### 2. ffpdf bin file
Once step 1. is done, the following bin file (the actual terminal command) will be created:
```sh
.venv/bin/ffpdf  # linux or mac
.venv\Scripts\ffpdf.exe  # windows
```
To have it ready-to-use in every shell you should have to copy it and paste in a directory on `PATH`. The following directories are suggested, depending on your os:

#### Linux and macOS
```sh
# current user
cp .venv/bin/ffpdf ~/.local/bin/

# or system wide:
sudo cp .venv/bin/ffpdf /usr/local/bin/
```

#### Windows
An advice is to create the linux-equivalent: `"%USERPROFILE%\.local\bin"` directory and then add it on user `PATH`.
```sh
# for current user:

# create folder
mkdir "%USERPROFILE%\.local\bin"

# add it to user path
# do it through windows settings to avoid problems...

# copy the .exe file into it
copy .venv\Scripts\ffpdf.exe "%USERPROFILE%\.local\bin\"
```
Otherwise you can copy the .exe file into some other folders that are already on `PATH`, as for example `"%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\"`.
