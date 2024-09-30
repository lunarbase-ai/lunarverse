import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project
VOLUME_INCREASE_FACTOR = 2  # Increase volume by 100%  (0.5 ==> -6dB, 2 ==> +6dB, etc., negative if take polarity is flipped)

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the master track
master_track = RPR.GetMasterTrack(PROJECT_INDEX)

# Get the current volume of the master track
current_volume = RPR.GetMediaTrackInfo_Value(master_track, "D_VOL")

# Compute the new volume value
new_volume = current_volume * VOLUME_INCREASE_FACTOR

# Set the new volume for the master track
RPR.SetMediaTrackInfo_Value(master_track, "D_VOL", new_volume)

# Save project
RPR.Main_SaveProject(0, False)  # False ==> No 'Save As' window