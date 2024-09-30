import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0  # 0 is the active project
TARGET_TRACK_NAME = 'my_track_name'  # Name of the track to mute

def get_track_index_by_name(target_name):
    # Get the total number of tracks in the current project
    num_tracks = RPR.CountTracks(PROJECT_INDEX)
    
    # Loop through all tracks to find the one with the target name
    for i in range(num_tracks):
        # Get the track at index i
        track = RPR.GetTrack(PROJECT_INDEX, i)
        
        # Get the track's name
        track_name = RPR.GetSetMediaTrackInfo_String(track, "P_NAME", "", False)
        
        # Check if the track name matches the target name
        if track_name == target_name:
            return i  # Return the index of the track if the name matches
    
    return -1  # Return -1 if no track with the given name was found

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Get the index of the track with the target name
track_index = get_track_index_by_name(TARGET_TRACK_NAME)

# Check if the track was found
if track_index != -1:
    # Get the track to mute
    track = RPR.GetTrack(PROJECT_INDEX, track_index)
    
    # Mute the track
    RPR.SetMediaTrackInfo_Value(track, "B_MUTE", 1)  # 1 ==> Mutes the track
    
# Save project
RPR.Main_SaveProject(0, False)  # False ==> No 'Save As' window