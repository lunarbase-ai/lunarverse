import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Mute all tracks
RPR.MuteAllTracks(1)  # 1 ==> Mutes all tracks (0 ==> Unmutes all tracks)

# Save project
RPR.Main_SaveProject(0, False)  # True ==> 'Save As' window