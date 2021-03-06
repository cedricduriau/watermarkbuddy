# WatermarkBuddy

![](https://github.com/cedricduriau/watermarkbuddy/workflows/Build/badge.svg?branch=master)
[![Platform](https://img.shields.io/badge/Platform-linux--64-lightgrey.svg)](https://img.shields.io/badge/Platform-linux--64-lightgrey.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-2.7%20|%203.6-blue.svg)](https://img.shields.io/badge/Python-2.7%20|%203.6-blue.svg)

## Overview

WatermarkBuddy is a tool using ffmpeg to easily add watermarks to files.

## Requirements
* [ffmpeg](https://ffmpeg.org/) (2.x, 3.x or 4.x)

## Install

If you wish to install the current master, use the following command:

`pip install git+git://github.com/cedricduriau/watermarkbuddy.git`

Or a specific release version:

`pip install git+git://github.com/cedricduriau/watermarkbuddy.git@1.1.0`


## Usage

To run `WatermarkBuddy` after installing, simply type one of the following command lines in a terminal.

### Graphical User Interface

```
watermarkbuddy-gui
```

### Command Line Interface

Adding a watermark requires three arguments.

* `-i/--input` defines which file to add the watermark to.
* `-w/--watermark` defines which file to use as watermark.
* `-o/--output` defines the output file path of the watermarked file

```
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg
```

To change the position the watermark, you can set the `-p/--position` argument.
Accepted values are: `top-left`, `top-right`, `bottom-left`, `bottom-right`.

By default, `top-left` will be used.

```
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -p top-left
```

To add an offset to the watermark, you can set the `-x/--offsetx` and `-y/offsety` arguments.
You can provide positive or negative values.

By default, `0` will be used for both `x` and  `y` offset values.

```
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -x 10
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -y 10
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -x 10  -y 10
```

To automatically scale the watermark to the width of the input file, staying aspect ratio correct, you can provide the `-a/--autoscale` flag. This flag cannot be used in combination with `-p/--position`, `-x/offsetx`, `-y/offsety`.

By default, the watermark will be applied as is, without resizing.

```
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -a
```

To use a specific blend mode, you can set the `-b/--blendmode` argument.

By default, `normal` will be used as blend mode.
See [this link](https://ffmpeg.org/ffmpeg-filters.html#blend_002c-tblend) for accepted values and more information regarding blend modes.

```
watermarkbuddy-cli -i ./examples/background.jpg -w ./examples/watermark.png -o /tmp/background.jpg -b multiply
```
