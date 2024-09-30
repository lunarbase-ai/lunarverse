# SPDX-FileCopyrightText: Copyright © 2024 Patricio Jaime Porras <contact@patriciojaime.dev>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.core.component import BaseComponent
from langchain_openai import ChatOpenAI

from typing import Optional, Any, Dict
import pandas as pd

from .causal_inference_llm import CausalInferenceAgentLLM


class CausalInferenceLLM(
    BaseComponent,
    component_name="Causal Inference with a LLM",
    component_description="""
    Run Causal Inference with the help of a LLM to run different methods (DoWhy and CausalPy)
    
    Inputs:
        Data Path (str): Path to the file
        Data Separator (str): Separator of the file
        Background Graph (str): Node-Link formatted Graph
        Context (str): Context for the causal inference methods
        Log File Name (str): Name of the log file to store the step-by-step reasoning of the LLM and results
        
    Outputs:
        Results (JSON):
            - Agent output (str): Output of the LLM
            - Dowhy results (str): Results of the causal inference methods
            - CausalPy results (str): Results of the causal inference methods
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
    openai_api_key="$LUNARENV::CAUSAL_INFERENCE_OPENAI_API_KEY",
    model_name="$LUNARENV::CAUSAL_INFERENCE_MODEL_NAME",
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
        try:
            df = pd.read_csv(data_path, sep=data_separator)
        except Exception as e:
            raise Exception(f"Error getting dataset: {e}")

        cdAgent = CausalInferenceAgentLLM(
            client=self._client,
            data=df,
            bg_knowledge=background_graph,
        )

        result = cdAgent.determine_causal_inference(context=context)
        out = result["agent_output"]
        dowhy = result["dowhy"]
        causalpy = result["causalpy"]
        full_log = result["full_log"]

        try:
            self._file_connector.delete_file(f"{log_file_name}.txt")
        except:
            pass
        self._file_connector.create_file(
            file_name=f"{log_file_name}.txt", content=full_log
        )

        return {"agent": str(out), "dowhy": str(dowhy), "causalpy": str(causalpy)}
