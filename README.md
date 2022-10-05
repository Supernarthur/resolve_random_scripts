# Random resolve scripts
Small archive of python scripts leveraging DaVinci Resolve's python API

## Script list

+ `reset_tc` : Resets the timecode of all the clips in the current bin and its
  subfolders to 00:00:00:00. Will prompt the user before doing the change.
  Surprisingly, this is something that you can undo with `Ctrl / Cmd + Z`, but
  clip by clip.
  Tested in version 18

## Installation

These scripts are written in Python 3, usually compatible with python 3.6 since
that's what resolve likes. Although since version 18 of resolve, sometimes
resolve is able to levearage more recent versions.
(I'm able to use the default 3.10 python that's installed on Fedora 36 at the
moment)

### Script documentation

To see where to install scripts, you can check the developper documentation
directly in resolve, by going to the `Help` Menu and selecting `Documentation`,
and then `Developer`. This will open a file browser to the right location. The
doc is then located in the `Scripting` folder, on the `README.txt` file.

This file will list the folders in which you can copy the python scripts
depending on your operating system and whether you want to install it for all
users of you computer or just you.


