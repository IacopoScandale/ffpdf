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
    - [Compress Img](#compress-img)
    - [Compress Vid](#compress-vid)
    - [Dim](#dim)
    - [Ext](#ext)
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
   1. ffpdf                     47    
   2. merge                     34    
   3. slice                     14    
   4. count                     33    
   5. convert                   17    
   6. img                      208    
   7. vid                       76    
   8. compress                 170    
   9. format                    59    
  10. dim                       80    
  11. ext                       22    
——————————————————————————————————————
      Total:                   760
```


|Subcommand|Description|
|-|-|
|`merge`|Merge the input files (PDFs or images) in an output PDF|
|`slice`|Extract pages from a PDF|
|`count`|Count the pages of every PDF in input|
|`convert`|Convert input files in the specified format (image or pdf)|
|`img`|Show relevant image infos for the input files|
|`vid`|Show relevant video infos for the input files|
|`compress img`|Compress images|
|`compress vid`|Apply the --ffmpeg inner command to all video files, skipping any others. Ignore files starting with 'ffpdf_' to avoid loops|
|`format`|Add, remove or replace prefixes and suffixes from filenames, or move them to the beginning or end of the filename|
|`dim`|Show perfect dimensions according to input image ratio|
|`ext`|List the frequency of file extensions|

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


### Compress Img
Compress images

- Example: compress input image to 2000x1500 px (`-s 2000x1500`) with JPEG quality 75 (`-q 75`)
  ```sh
  ffpdf compress img "20200526_134236.jpg" -s 2000x1500 -q 75

        Size —> New Size        Size %       Ratio         Dim —> New Dim     Filename
  ————————————————————————————————————————————————————————————————————————————————
    1.12 MB —> 1.18 MB        105.0 %         4:3   4608×3456 —> 2000×1500   '20200526_134236.jpg'
  ```
- Example: try to compress every file, (only images will be processed) (`*`), but filter only images with an aspect ratio of exactly 4:3 (`-r 4:3`). Final size is 2000x1500 px (smaller images won't be upscaled) (`-s 2000x1500`) with quality 80 (`-q 80`)
  ```sh
  ffpdf compress img * -r 4:3 -s 2000x1500 -q 80

        Size —> New Size        Size %       Ratio         Dim —> New Dim     Filename
  ————————————————————————————————————————————————————————————————————————————————
    1.12 MB —> 383.75 KB       33.4 %         4:3   4608×3456 —> 2000×1500   '20200526_134236.jpg'  
  797.59 KB —> 352.67 KB       44.2 %         4:3   4608×3456 —> 2000×1500   '20200526_134258.jpg'  
                                              3:4                            '20200528_182747.jpg'  
    2.03 MB —> 595.65 KB       28.7 %         4:3   4608×3456 —> 2000×1500   '20200621_165613.jpg'  
                                              3:4                            '20200711_121542.jpg'  
  ————————————————————————————————————————————————————————————————————————————————
    3.93 MB —> 1.30 MB         33.1 %                                        '3 files compressed'
  ```


### Compress Vid
Apply the --ffmpeg inner command to all video files, skipping any others. Ignore files starting with 'ffpdf_' to avoid loops

- Example: compressing personal videos using ffmpeg to save space  
  (during processing:)
  ```sh
  ffpdf compress vid *.mp4 --ffmpeg="-c:v libx264 -b:v 5000k -s 1280:720 -r 30 -c:a copy"

  # See ffmpeg output log at '/example_full_path/ffpdf/src/ffpdf/data/tmp/ffmpeg_compress_log.txt'

        Size —> New Size    Size %  Ratio         Dim —> New Dim       FPS —> New FPS    Filename
  ———————————————————————————————————————————————————————————————————————————————————————————————
   148.34 MB —> 104.15 MB   70.2 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250104185916.mp4'
    64.64 MB —> 48.90 MB    75.7 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250310110538.mp4'
  Processing 'VID20250326110315.mp4' --------------------------- ------------  69% 0:02:03
  ```
  (final result:)
  ```sh
  ffpdf compress vid *.mp4 --ffmpeg="-c:v libx264 -b:v 5000k -s 1280:720 -r 30 -c:a copy"

  # See ffmpeg output log at '/example_full_path/ffpdf/src/ffpdf/data/tmp/ffmpeg_compress_log.txt'

        Size —> New Size    Size %  Ratio         Dim —> New Dim       FPS —> New FPS    Filename
  ———————————————————————————————————————————————————————————————————————————————————————————————
   148.34 MB —> 104.15 MB   70.2 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250104185916.mp4'
    64.64 MB —> 48.90 MB    75.7 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250310110538.mp4'
    70.62 MB —> 48.74 MB    69.0 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250326110315.mp4'
   106.04 MB —> 76.28 MB    71.9 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250331202703.mp4'
     9.88 MB —> 6.97 MB     70.5 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250525150048.mp4'
    50.85 MB —> 36.38 MB    71.6 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250530140341.mp4'
    20.50 MB —> 14.15 MB    69.0 %   16:9    1280×720 —> 1280×720    29.58 —> 30.0 fps   'VID20250530141004.mp4'
  Processing 'VID20250530141004.mp4' ---------------------------------------- 100% 0:04:11 0:00:00
  ———————————————————————————————————————————————————————————————————————————————————————————————
  476.01 MB —> 339.94 MB   71.4 %                                                       '7 files'

    Notes:
    · run 'ffpdf vid *.mp4' or 'ffpdf vid *' to see results
    · See ffmpeg output log at '/example_full_path/ffpdf/src/ffpdf/data/tmp/ffmpeg_compress_log.txt'
  ```

### Dim
Show perfect dimensions according to input image ratio
```sh
ffpdf dim 4:3 -w 4185

  4164:3123    4168:3126    4172:3129    4176:3132    4180:3135    4184:3138    4188:3141  
  4192:3144    4196:3147    4200:3150  
```
```sh
ffpdf dim 16:9 --height 1356 -n 10

  2240:1260    2256:1269    2272:1278    2288:1287    2304:1296    2320:1305    2336:1314  
  2352:1323    2368:1332    2384:1341    2400:1350    2416:1359    2432:1368    2448:1377  
  2464:1386    2480:1395    2496:1404    2512:1413    2528:1422    2544:1431 
```


### Ext
List the frequency of file extensions

```sh
ffpdf ext

Extension    Count
——————————————————————————————
 (no ext)    1    
     .JPG    1    
    .jpeg    1    
     .jpg    9    
     .mp4    4    
     .pdf    2    
     .png    3    
——————————————————————————————
    7 ext    21 files
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
`ffmpeg` is required for the `vid` and `compress vid` commands, but it is not mandatory for the other `ffpdf` commands.
- **Linux / macOS:**
  Example installation using *apt*:
  ```sh
  sudo apt install ffmpeg
  ```
- **Windows:**
  Manual installation at https://ffmpeg.org/

