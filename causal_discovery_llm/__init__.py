# SPDX-FileCopyrightText: Copyright © 2024 Patricio Jaime Porras <contact@patriciojaime.dev>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.core.component import BaseComponent
from langchain_openai import ChatOpenAI
from typing import List, Optional, Any, Dict
import pandas as pd

from .causal_discovery_llm import CausalDiscoveryAgentLLM

class CausalDiscoveryLLM(
    BaseComponent,
    component_name="Causal Discovery Algorithms with a LLM",
    component_description="""
    Run Causal Discovery algorithms with the help of a LLM to run different methods
    
    Inputs:
        Data Path (str): Path to the file
        Data Separator (str): Separator of the file
        Background Graph (str): Node-Link formatted Graph
        Context (str): Context for the causal discovery algorithm
        Log File Name (str): Name of the log file to store the step-by-step reasoning of the LLM and results
        
    Outputs:
        Results (JSON):
            - SEM object with the results of the causal discovery algorithm turned into a SEM description
            - Agent output 
    """,
    input_types={
        "data_path": DataType.TEXT,
        "data_separator": DataType.TEXT,
        "background_graph": DataType.JSON,
        "context": DataType.TEXT,
        "log_file_name": DataType.TEXT,
    },
    output_type=DataType.ANY,
    component_group=ComponentGroup.CAUSAL_INFERENCE,
    openai_api_key="$LUNARENV::CAUSAL_DISCOVERY_OPENAI_API_KEY",
    model_name="$LUNARENV::CAUSAL_DISCOVERY_MODEL_NAME",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        self._client = ChatOpenAI(**self.configuration)

    def run(
        self,
        data_path: str,
        data_separator: str,
        background_graph: Dict,
        context: str,
        log_file_name: str,
    ):
        ###############################
        # Get the inputs

        try:
            df = pd.read_csv(data_path, sep=data_separator)
        except Exception as e:
            raise Exception(f"Error getting dataset: {e}")

        cdAgent = CausalDiscoveryAgentLLM(
            client=self._client,
            data=df,
            bg_knowledge=background_graph,
        )

        ###############################
        # Run the causal discovery
        result = cdAgent.determine_causal_relationship(context=context)
        out = result["agent_output"]
        sem = result["sem_dict"]
        full_log = result["full_log"]
        graph = result["graph"]

        try:
            self._file_connector.delete_file(f"{log_file_name}.txt")
        except:
            pass
        self._file_connector.create_file(
            file_name=f"{log_file_name}.txt", content=full_log
        )

        return {"agent": str(out), "sem": str(sem), "graph": graph}
