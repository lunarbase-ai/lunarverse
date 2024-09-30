import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 indicates the active project
TRACK_INDEX = 0  # Index of the track to which the EQ will be added (0-based)

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the track at index TRACK_INDEX
track = RPR.GetTrack(PROJECT_INDEX, TRACK_INDEX)

# Get the index of ReaEQ in the track FX chain, and add it if it doesn't exist
# Parameters:
# - track: The track on which to check or add ReaEQ.
# - instantiate: Set to True to insert ReaEQ if it is not already in the chain.
# Returns:
# - The index of ReaEQ in the track FX chain, or -1 if ReaEQ could not be added.

# Get index of EQ if exists
eq_index = RPR.TrackFX_GetEQ(track, False)

# Remove EQ if found
if eq_index >= 0:
    RPR.TrackFX_Delete(track, eq_index)

# Save project
RPR.Main_SaveProject(0, False)  # Save the project without opening the 'Save As' dialog