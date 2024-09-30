# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
from typing import Any, Optional
from reapy import (
    connect,
    reascript_api as RPR
)

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType

from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage


REAPER_PROMPT_TEMPLATE = """######## START OF RPP FILE ########
{rpp_content}
######## END OF RPP FILE ########

You are a code co-pilot, writing Python code to controll the digital audio workstation Reaper through its Python API.
Given the existing (potientially empty) Reaper project in the RPP file above, write Python code that edits the Reaper project according to the instruction below.
A Reaper Python API method `method_name` can be called with this line of code: `RPR.method_name` (see examples below).
Output code according to the examples below.
Output nothing else than the Python code.

{examples}

INSTRUCTION: {instruction}
RPP PROJECT PATH: {rpp_path}"""

PROMPT_EXAMPLE_TEMPLATE = """Here is an example:
Instruction: {instruction}
RPP project path: /Documents/my_reaper_projects/my_reaper_project.RPP
Output:
{answer_code}"""


EXAMPLES_DATA = [
    {
        "instruction": "Create a new track with the file '/Documents/reaper_material/vocals.wav'",
        "answer_file": "new_media_track.py"
    },
    {
        "instruction": "Mute the track at index 0",
        "answer_file": "mute_track_by_index.py"
    },
    {
        "instruction": "Mute all tracks",
        "answer_file": "mute_all_tracks.py"
    },
    {
        "instruction": "Solo the track at index 0",
        "answer_file": "solo_track_by_index.py"
    },
    {
        "instruction": "Mute the track with the name 'my_track_name'",
        "answer_file": "mute_track_by_name.py"
    },
    {
        "instruction": "Decrease the volume of the track at index 0 by 50%",
        "answer_file": "track_volume.py"
    },
    {
        "instruction": "Change panning of the track at index 0 to 50% left",
        "answer_file": "track_pan.py"
    },
    {
        "instruction": "Increase the volume of the master track by 100%",
        "answer_file": "master_volume.py"
    },
    {
        "instruction": "Change panning of the master track to 75% right",
        "answer_file": "master_pan.py"
    },
    {
        "instruction": "For the track at index 0: add an equalization (EQ) with three bands:\n-A hipass filter: frequency 100 Hz, gain +6 dB, bandwidth 1.0 oct\n-A loshelf filter: frequency 1000 Hz, gain -3 dB, bandwidth 1.0 oct\n-A band filter: frequency 8000 Hz, gain +2 dB, bandwidth 1.0 oct",
        "answer_file": "track_eq.py"
    },
    {
        "instruction": "Disable the first bandpass filter on the track at index 0",
        "answer_file": "track_eq_disable_band.py"
    },
    {
        "instruction": "Disable the equalizer of the track at index 0",
        "answer_file": "track_eq_disable.py"
    },
    {
        "instruction": "Remove the EQ of the track at index 0",
        "answer_file": "track_eq_remove.py"
    } 
]

LLM_PYTHON_ANSWER_PATTERN = r"```python\s*(.*?)\s*```"


def file_content(path: str):
    with open(path, "r") as file:
        content = file.read()
    return content


def build_examples_str(examples_data=EXAMPLES_DATA):
    examples_sb = []
    for example_data in examples_data:
        instruction = example_data.get("instruction", "")
        answer_file = example_data["answer_file"]
        answer_file_path = os.path.join(os.path.dirname(__file__), answer_file)
        answer_code = file_content(answer_file_path)
        example_str = PROMPT_EXAMPLE_TEMPLATE.format(
            instruction=instruction,
            answer_code=answer_code
        )
        examples_sb.append(example_str)
    examples_str = "\n\n".join(examples_sb)
    return examples_str


EXAMPLES_STR = build_examples_str()


def render_rpp_project(rpp_path, audio_format="wav", render_path=None):
    if render_path:
        audio_format = render_path.split(".")[-1]
    else:
        render_path = rpp_path.replace(".RPP", f".{audio_format}")

    output_dir = os.path.dirname(render_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if audio_format == 'mp3':
        audio_format_coding = 'l3pm'
    else:  # set to wav encoding
        audio_format_coding = 'evaw'

    RPR.GetSetProjectInfo_String(0, "RENDER_FORMAT", audio_format_coding, True)  # Set render format
    RPR.GetSetProjectInfo_String(0, "RENDER_FILE", os.path.dirname(render_path), True)  # Set output directory
    RPR.GetSetProjectInfo_String(0, "RENDER_PATTERN", os.path.basename(render_path), True)  # Set output file name
    
    # Additional rendering options can be set here using RPR.GetSetProjectInfo_* functions
    # For example, to set sample rate, you could use RPR.GetSetProjectInfo(PROJECT_INDEX, "RENDER_SRATE", 44100, True)

    RPR.Main_OnCommand(41824, 0)  # Command 41824 corresponds to the "File: Render project, using the most recent render settings" action
    return render_path


class ReaperController(
    BaseComponent,
    component_name="Reaper Controller",
    component_description="""Controlls Reaper (a digital audio workstation (DAW)) by natural language. Opens a Reaper project, edits it, and creates a new audio file.
Inputs:
  `RPP path` (str): The server path to the Reaper project.
  `Instruction` (str): Instruction (in natural language) on how to edit the Reaper project.
  `Audio output path` (str): Path to the audio file to be created. The file extension specifies the file format (`.wav` or `.mp3` is supported). Set as empty string to create an .wav file with same name as the RPP file.
Output (str): The path of the new audio file.
NOTE: this component assumes that Reaper is open in the background and that reapy has been installed (`pip install python-reapy`) according to its install instructions (including running the Python code `import reapy\nreapy.configure_reaper()`)""",
    input_types={
        "rpp_path": DataType.TEXT,
        "instruction": DataType.TEMPLATE,
        "audio_output_path": DataType.TEXT
    },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
    openai_api_version="$LUNARENV::REAPER_OPENAI_API_VERSION",
    deployment_name="$LUNARENV::REAPER_DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::REAPER_OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::REAPER_AZURE_OPENAI_ENDPOINT",
    audio_format="wav",                    # If `Audio path` (output file) is provided, this will be overwritten by the file extension
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        if not self.configuration["openai_api_key"]:
            self.configuration["openai_api_key"] = os.environ.get("OPENAI_API_KEY", "")
        if not self.configuration["azure_endpoint"]:
            self.configuration["azure_endpoint"] = os.environ.get("AZURE_ENDPOINT", "")

        openai_config = self.configuration.copy()
        openai_config.pop('audio_format')
        self._client = AzureChatOpenAI(**openai_config)

    def run(self, rpp_path: str, instruction: str, audio_output_path: str):
        rpp_content = file_content(rpp_path)

        prompt = PromptTemplate(                                                        # TODO: put outside method?
            input_variables=[
                "rpp_content",
                "examples",
                "instruction",
                "rpp_path"
            ],
            template=REAPER_PROMPT_TEMPLATE
        )

        message = HumanMessage(
            content=prompt.format(
                rpp_content=rpp_content,
                examples=EXAMPLES_STR,
                instruction=instruction,
                rpp_path=rpp_path
            )
        )
        result = self._client([message]).content
        llm_ans_python = str(result).strip("\n").strip().replace('"', "'")
        
        matches = re.findall(LLM_PYTHON_ANSWER_PATTERN, llm_ans_python, re.DOTALL)
        python_code = matches[0] if matches else llm_ans_python

        exec(python_code, globals())

        render_path = render_rpp_project(rpp_path, self.configuration["audio_format"], audio_output_path)

        return render_path
