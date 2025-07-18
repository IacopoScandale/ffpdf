# ffpdf
## Fast PDF, Image and Video File Operations

<!-- Badges -->
![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Platform](https://img.shields.io/badge/platform-Linux,%20Windows,%20macOS-green) ![FFmpeg](https://img.shields.io/badge/dependency-ffmpeg-critical) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**ffpdf** is a command-line tool designed to easily perform file operations like merging PDFs or images, slicing PDFs, and converting between images and PDFs.


## Table of Contents

- [Commands](#commands)
  - [Examples](#examples)
    - [Merge](#merge)
    - [Slice](#slice)
    - [Count](#count)
    - [Convert](#convert)
    - [Img](#img)
    - [Vid](#vid)
- [Download](#download)
  - [Base Env (Easier)](#base-env-easier)
  - [Virtual Env (Recommended)](#virtual-env-recommended)
    - [1. Dependencies](#1-dependencies)
      - [uv](#uv)
      - [pip](#pip)
    - [2. ffpdf bin file](#2-ffpdf-bin-file)
      - [Linux and macOS](#linux-and-macos)
      - [Windows](#windows)
- [External Dependencies](#external-dependencies)



# Commands
Show command usages
```sh
ffpdf

Commands:              Times Used:
——————————————————————————————————————
   1. ffpdf                     33
   2. merge                     32
   3. slice                     14
   4. count                     26
   5. convert                   12
   6. img                       81
   7. vid                       22
——————————————————————————————————————
      Total:                   220
```


|Subcommand|Description|
|-|-|
|`merge`|Merge the input files (PDFs or images) in an output PDF|
|`slice`|Extract pages from a PDF|
|`count`|Count the pages of every PDF in input|
|`convert`|Convert input files in the specified format (image or pdf)|
|`img`|Show relevant image infos for the input files|
|`vid`|Show relevant video infos for the input files|

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

Pages          Size    Filename
——————————————————————————————————————————————————
    5       2.27 MB    'a.pdf'                          
```

```sh
ffpdf count *.pdf

Pages          Size    Filename
——————————————————————————————————————————————————
    5       2.27 MB    'a.pdf'                                        
    5     875.49 KB    'b.pdf'                                        
    0       0.00 B     'c.pdf' (empty file)
    7     741.03 KB    'd.pdf'                                        
——————————————————————————————————————————————————
   17       3.84 MB    '4 files'                                       
```
### Convert
Convert input files in the specified format (image or pdf)
```sh
ffpdf convert a.pdf b.jpg c.png -e .png

Converted 'a.pdf' (4 pages) to '.png'
Converted 'b.jpg' to 'b.jpg(3).png'
Skipped   'c.png' (no conversion is needed)
```

### Img
Show relevant image infos for the input files
```sh
ffpdf img *.jpg

      Size     Dimensions       Ratio    Filename
——————————————————————————————————————————————————
   0.00 B                                'a.jpg'
   1.72 MB      4160×2336      130:73    'b.jpg'
 107.78 KB       1080×825       72:55    'c.jpg'
—————————————————————————————————————————————————— 
   1.83 MB                               '3 files'
```

### Vid
Show relevant video infos for the input files (requires ffmpeg)
```sh
ffpdf vid *.mp4

      Size     Dimensions  Duration   Framerate     Bitrate  Filename
————————————————————————————————————————————————————————————————————————————————
   1.31 GB       1280×720     13:20   29.97 fps     13 Mb/s  'VID_20240101_180705.mp4'     
 386.29 MB       1280×720     03:49    30.0 fps     13 Mb/s  'VID_20240211_213153.mp4'     
  75.42 MB      1920×1080     00:31    30.0 fps     19 Mb/s  'VID_20241102_164408.mp4'     
————————————————————————————————————————————————————————————————————————————————
   1.76 GB                    17:40                          '3 files'
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

# External Dependencies
`ffmpeg` is required for the `vid` command, but it is not mandatory for the other `ffpdf` commands.
- **Linux / macOS:**
  Example installation using *apt*:
  ```sh
  sudo apt install ffmpeg
  ```
- **Windows:**
  Manual installation at https://ffmpeg.org/

