import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0                                                                                   # 0 is the active project
TRACK_INDEX_TO_MUTE = 0                                                                             # Index of the track to mute (0-based)

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the track to mute
track = RPR.GetTrack(PROJECT_INDEX, TRACK_INDEX_TO_MUTE)

# Mute the track
RPR.SetMediaTrackInfo_Value(track, "B_MUTE", 1)  # 1 ==> Mutes the track (0 ==> Unmutes the track)

# Save project
RPR.Main_SaveProject(0, False)  # True ==> 'Save As' window