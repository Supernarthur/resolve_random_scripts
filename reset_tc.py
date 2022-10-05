#!/usr/bin/env python3

###
# reset_tc.py
# reset the timecode of all the clips in a folder tree (inc. subfolders) to 00:00:00:00
# made to speedup conform when for some reason people stripped proxies of their TC
#
# by Arthur Desplanches (github.com/supernarthur)
# Do What the Fuck You Want to Public License (wtfpl.net)

# If you are in python2, this should make the script work (not tested unfortunately)
from __future__ import print_function

def GetResolve():
    """
    Creates the python object using DaVinciResolveScript library. It will import it from the default locations
        and return a resolve object

    Returns
    -------
    resolve object

    """
    import sys
    if sys.platform.startswith("darwin"):
        expectedPath = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
    elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
        import os
        expectedPath = os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
    elif sys.platform.startswith("linux"):
        expectedPath = "/opt/resolve/Developer/Scripting/Modules/"
        # expectedPath = "/opt/resolve/libs/Fusion/Modules/"
    try:
        import imp
        bmd = imp.load_source('DaVinciResolveScript', expectedPath + "DaVinciResolveScript.py")
    except ImportError:
        print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
        print("For a default DaVinci Resolve installation, the module is expected to be located in: " + expectedPath)
        sys.exit()
    return bmd.scriptapp("Resolve")

def build_all_clips(resolve_folder):
    """
    Traverses a folder tree recursively in resolve and returns a list of all the clips in the tree
    
    Parameters
    ----------
    resolve_folder: object
        a mediapool folder object

    Returns
    -------
    list: A list of all the clip objects found in the folder tree
    """
    subfolders = resolve_folder.GetSubFolderList()
    if subfolders == []:
        return resolve_folder.GetClipList()
    else:
        clip_list = resolve_folder.GetClipList()
        for subfolder in subfolders:
            clip_list += build_all_clips(subfolder)
        return clip_list 

def is_timeline(mediapool_item):
    """
    Will check if a media pool item is a timeline or not
    
    Parameters
    ----------
    mediapool_item: object
        a mediapool item object

    Returns
    -------
    bool: True if mediapool_item is a Timeline, False otherwise
    """
    return mediapool_item.GetClipProperty(propertyName="Type") == "Timeline"

def main():
    """
    Will traverse the currently opened bin and prompt the user to reset
    the timecode of all the clips (not the timelines) found to 00:00:00:00
    """
    resolve = GetResolve()
    if resolve is not None:
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        media_pool = project.GetMediaPool()
        current_folder = media_pool.GetCurrentFolder()
        clips = build_all_clips(current_folder)
        clips = [clip for clip in clips if not is_timeline(clip)]

        fusion = resolve.Fusion()
        comp = fusion.NewComp()
        warn_message = "This will reset the timecode on all {} clips in the bin {} and its subfolders".format(len(clips), current_folder.GetName())
        dialog_options = {}
        dialog_options[1] = {
            1: "text",
            2: "Text",
            "Name": "",
            "ReadOnly": True,
            "Wrap": True,
            "Default": warn_message,
        }
        dialog_options[2] = {
            1: "checkbox",
            2: "Checkbox",
            "Name": "Reset all TC",
            "Default": 0,
        }
        output = comp.AskUser("Warning", dialog_options)
        if output is None:
            print("Operation cancelled")
        elif output.get("checkbox") == 0.0:
            print("Operation cancelled")
        elif output.get("checkbox") == 1.0:
            for clip in clips:
                clip.SetClipProperty("Start TC", "00:00:00:00")
                print("Reset TC to 00:00:00:00 for clip {}".format(clip.GetName()))

if __name__ == "__main__":
    main()

