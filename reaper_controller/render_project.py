import os
from reapy import (
    connect,
    reascript_api as RPR
)

RPR_PROJECT_FILE_PATH = "/Documents/my_reaper_projects/my_reaper_project.RPP"
RENDER_OUTPUT_PATH = "/Documents/my_audio_files/my_rendered_audio_file.mp3"
PROJECT_INDEX = 0  # 0 indicates the active project

# Connect to API and open project
connect()
RPR.Main_openProject(RPR_PROJECT_FILE_PATH)

# Function to render the project to a WAV or MP3 file
def render_project(render_output_path, audio_format="wav"):
    """Renders the entire project to a specified WAV or MP3 file."""
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(render_output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if audio_format == 'mp3':
        audio_format_coding = 'l3pm'
    else:  # set to WAV encoding
        audio_format_coding = 'evaw'

    # Set rendering parameters
    RPR.GetSetProjectInfo_String(PROJECT_INDEX, "RENDER_FORMAT", audio_format_coding, True)  # Set render format
    RPR.GetSetProjectInfo_String(PROJECT_INDEX, "RENDER_FILE", os.path.dirname(render_output_path), True)  # Set output directory
    RPR.GetSetProjectInfo_String(PROJECT_INDEX, "RENDER_PATTERN", os.path.basename(render_output_path), True)  # Set output file name
    
    # Additional rendering options can be set here using RPR.GetSetProjectInfo_* functions
    # For example, to set sample rate, you could use RPR.GetSetProjectInfo(PROJECT_INDEX, "RENDER_SRATE", 44100, True)

    # Render the project
    render_success = RPR.Main_OnCommand(41824, 0)  # Command 41824 corresponds to the "File: Render project, using the most recent render settings" action
    
    if render_success:
        print(f"Project rendered successfully to {render_output_path}")
    else:
        print("Rendering failed.")

# Call the function to render the project
render_project(RENDER_OUTPUT_PATH)