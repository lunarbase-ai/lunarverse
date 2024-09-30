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

# Get the index of ReaEQ in the track FX chain, if it exists
eq_index = RPR.TrackFX_GetEQ(track, False)

# Disable a specific EQ band on the track
def enable_eq_band(track, eq_index, bandtype, bandidx, enable):
    """Enables/disables a specific band in ReaEQ on the track."""
    
    # Parameters:
    # - track: The track where the effect is applied.
    # - eq_index: The index of the effect (ReaEQ).
    # - bandtype: The type of EQ band (-1=master gain, 0=hipass, 1=loshelf, 2=band, 3=notch, 4=hishelf, 5=lopass, 6=bandpass, 7=parallel bandpass).
    # - bandidx: Index of the band to target (e.g., 0 for the first band of the bandtype).
    # - enable: Set to False to disable the band.
    # Returns:
    # - True if band success
    
    # Enable/disable the specified EQ band
    success = RPR.TrackFX_SetEQBandEnabled(track, eq_index, bandtype, bandidx, enable)
    return success

# Disable the first bandpass filter (Band filter) on the track
enable_eq_band(track, eq_index, 2, 0, False)  # Disables the first bandpass filter (bandtype=2, bandidx=0)

# Save project
RPR.Main_SaveProject(0, False)  # Save the project without opening the 'Save As' dialog