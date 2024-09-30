import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project
TRACK_INDEX = 0  # Index of the track to adjust volume (0-based)
VOLUME_INCREASE_FACTOR = 0.5  # Decrease volume by 50%  (0.5 ==> -6dB, 2 ==> +6dB, etc., negative if take polarity is flipped)

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the track at index TRACK_INDEX
track = RPR.GetTrack(PROJECT_INDEX, TRACK_INDEX)

# Get the current volume of the track
ok, track_str, current_volume, current_pan = RPR.GetTrackUIVolPan(track, 0, 0)

# Compute the new volume value
new_volume = current_volume * VOLUME_INCREASE_FACTOR

# Set the new volume for the track
RPR.SetMediaTrackInfo_Value(track, "D_VOL", new_volume)

# Save project
RPR.Main_SaveProject(0, False)  # False ==> No 'Save As' window