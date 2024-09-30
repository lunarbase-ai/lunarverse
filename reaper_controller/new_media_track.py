import os

from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
PROJECT_INDEX = 0                                                                                   # 0 is the active project
MEDIA_FILE_PATH = "new_media_track.wav"
INSERT_TIME = 0                                                                                     # time in seconds


# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Move curser to the time where media item should be inserted
RPR.SetEditCurPos(INSERT_TIME, False, False)  # False, False ==> moveview, seekplay == False, False

# Add media item to the new track
RPR.InsertMedia(MEDIA_FILE_PATH, 1)  # 1 ==> creates new track (0 ==> adds to current track)

# Add name to new track
track_index = RPR.CountTracks(PROJECT_INDEX) - 1
track = RPR.GetTrack(PROJECT_INDEX, track_index)
track_name = os.path.basename(MEDIA_FILE_PATH)
RPR.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)  # True ==> overwrites existing info

# Save project
RPR.Main_SaveProject(0, False)  # True ==> 'Save As' window