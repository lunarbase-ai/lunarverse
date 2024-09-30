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

# Get or add ReaEQ
eq_index = RPR.TrackFX_GetEQ(track, True)

def db_to_gain_param(db_value):
    """
    Converts a dB value to the corresponding gain parameter value for ReaEQ.
    
    Args:
    db_value (float): The desired gain in dB.
    
    Returns:
    float: The gain parameter value to be used in ReaEQ.
    """
    # Calculate the gain parameter value using the formula
    gain_param_value = pow(2, db_value / 6.02)
    
    return gain_param_value

# Define a function to set EQ band parameters in ReaEQ
def set_eq_band(track, eq_index, bandtype, bandidx, freq, gain, q, isnorm):
    """Sets the EQ band parameters using either normalized or absolute values."""
    
    # Set frequency, gain, and Q factor for the EQ band
    # Parameters:
    # - track: The track where the effect is applied.
    # - fxidx: The index of the effect (ReaEQ).
    # - bandtype: The type of EQ band (-1=master gain, 0=hipass, 1=loshelf, 2=band, 3=notch, 4=hishelf, 5=lopass, 6=bandpass, 7=parallel bandpass).
    # - bandidx: Index of the band to target (e.g., 0=target first band matching bandtype, 1=target 2nd band matching bandtype, etc.).
    # - paramtype: Type of parameter to set (0=freq, 1=gain, 2=Q).
    # - val: The value to set for the parameter. Normalized if isnorm is True.
    #    - Note: for paramtype 1=gain, val=1 ==> 0 dB, val=2 ==> 6.02 dB, val=4 ==> 12.04 dB, val=8 ==> 18.06 dB, etc., val<0 ==> -inf dB
    # - isnorm: Whether the value is normalized (True) or absolute (False).

    # Set frequency, gain, and Q factor for the specified EQ band
    RPR.TrackFX_SetEQParam(track, eq_index, bandtype, bandidx, 0, freq, isnorm)   # Frequency
    RPR.TrackFX_SetEQParam(track, eq_index, bandtype, bandidx, 1, gain, isnorm)   # Gain
    RPR.TrackFX_SetEQParam(track, eq_index, bandtype, bandidx, 2, q, isnorm)      # Q Factor (bandwidth [oct])

# Values for setting EQ bands:
# Band type: -1=master gain, 0=hipass, 1=loshelf, 2=band, 3=notch, 4=hishelf, 5=lopass, 6=bandpass, 7=parallel bandpass
# Band index: 0 = first band of the type, 1 = second band, etc.
# Using absolute values (isnorm=False) here

# Set parameters for the three bands
set_eq_band(track, eq_index, 0, 0, 100, db_to_gain_param(8), 1.0, False)    # Hipass filter, frequency 100 Hz, gain +6 dB, Q=1.0 oct
set_eq_band(track, eq_index, 1, 0, 1000, db_to_gain_param(-3), 1.0, False)  # Loshelf filter, frequency 1000 Hz, gain -3 dB, Q=1.0 oct
set_eq_band(track, eq_index, 2, 0, 8000, db_to_gain_param(2), 1.0, False)   # Band filter, frequency 8000 Hz, gain +2 dB, Q=1.0 oct

# Save project
RPR.Main_SaveProject(0, False)  # Save the project without opening the 'Save As' dialog