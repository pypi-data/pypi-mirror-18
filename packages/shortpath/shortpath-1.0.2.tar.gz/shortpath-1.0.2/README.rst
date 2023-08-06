shortpath
======================================================

:Author: Gaurav Kumar <aavrug@gmail.com>

Shortpath for assigning a single string to the complete path.

Installation
======================================================

    pip install shortpath

Description
======================================================

Shortpath provides a short name for the directory path. This is userwise so if you set the shortpath for the guest user it will not work for the root user. 
If you just use the command shortpath it will create a shortpath for your current working directory and generate a random name. You can also pass custom path and custom name that you want to use.

Usage
======================================================

    shortpath --help

    shortpath --v

    shortpath --p <path from /home...> --s <any string>

    shortpath --p <path from /home...>

    shortpath --s <any string>

Homepage: https://github.com/aavrug/shortpath