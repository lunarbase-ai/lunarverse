import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project
TRACK_INDEX = 0  # Index of the track to adjust volume (0-based)
PANNING_VALUE = -0.5  # Value in range [-1, 1], where -1.0 represents full left pan, 0 is centered, and 1.0 represents full right pan

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the track at index TRACK_INDEX
track = RPR.GetTrack(PROJECT_INDEX, TRACK_INDEX)

# Set the new panning value
RPR.SetMediaTrackInfo_Value(track, "D_PAN", PANNING_VALUE)

# Save project
RPR.Main_SaveProject(0, False)  # False ==> No 'Save As' window