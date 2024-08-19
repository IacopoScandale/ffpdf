# PDF Commands

> package name: *pdf_commands*

Some useful line commands to manage files, especially pdfs.


# Download
Recommended install is by executing install files respectively .bat for windows and ??? for linux. 

This will install this package and dependencies in a virtual environment. Then all commands will be put in Commands folder that will automaticly added to path variable. In this way commands will always loaded on terminal. All this is done in the scrypt `post_install.py`. 

If you only want to install the package, just use this command inside the package folder: 
``` 
pip install -e .
```

## Windows
Just double click on `setup.bat` file. If you want to uninstall just double click on `uninstall.bat` file. Easy peasy.

## Linux
work in progress


# Commands:
|command|description|
|-|-|
|`pdf_commands`|shows all commands|
|`fname_format`|format all file names within a folder|
|`merge_pdf`|merges all pdfs passed as arguments|
|`slice_pdf`|slice a pdf according to given slice|

Type `command_name -h` or `command_name --help` for more info