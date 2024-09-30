import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project
TRACK_INDEX_TO_SOLO = 0  # Index of the track to solo (0-based)

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the track to solo
track = RPR.GetTrack(PROJECT_INDEX, TRACK_INDEX_TO_SOLO)

# Solo the track
RPR.SetMediaTrackInfo_Value(track, "I_SOLO", 1)  # 1 ==> Solos the track (2 ==> Solo-in-place, 0 ==> Unsolo, 5 ==> safe solo, 6 ==> safe solo-in-place)

# Save project
RPR.Main_SaveProject(0, False)  # True ==> 'Save As' window