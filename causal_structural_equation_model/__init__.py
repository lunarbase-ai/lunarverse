# SPDX-FileCopyrightText: Copyright © 2024 Patricio Jaime Porras <contact@patriciojaime.dev>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.core.component import BaseComponent

from langchain.chat_models import ChatOpenAI

from .sem_llm import SEMAgentLLM, SEMEnvironment

from typing import List, Optional, Any
import pandas as pd


class StructuralEquationModel(
    BaseComponent,
    component_name="Structural Equation Model Refinement with LLM",
    component_description="Run SemoPy with an initial SEM so it can be refined and interpreted by an LLM.",
    input_types={
        "data_path": DataType.TEXT,
        "data_separator": DataType.TEXT,
        "sem": DataType.TEXT,
        "context": DataType.TEXT,
        "log_file_name": DataType.TEXT,
    },
    output_type=DataType.ANY,
    component_group=ComponentGroup.CAUSAL_INFERENCE,
    openai_api_key="$LUNARENV::STRUCTURAL_EQUATION_OPENAI_API_KEY",
    model_name="$LUNARENV::STRUCTURAL_EQUATION_MODEL_NAME",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        self._client = ChatOpenAI(**self.configuration)

    def run(
        self,
        data_path: str,
        data_separator: str,
        sem: str,
        context: str,
        log_file_name: str,
    ):
        try:
            df = pd.read_csv(data_path, header=0, sep=data_separator)
        except Exception as e:
            raise Exception(f"Error getting dataset: {e}")

        sem_env = SEMEnvironment(sem, df)
        sem_llm = SEMAgentLLM(self._client, sem_env)
        result = sem_llm.improve_sem_model(context)
        log = result["full_log"]
        try:
            self._file_connector.delete_file(f"{log_file_name}.txt")
        except:
            pass
        self._file_connector.create_file(file_name=f"{log_file_name}.txt", content=log)

        return {
            "output": result["agent_output"],
            "interpretation": result["interpretation"],
            "model": result["final_model"],
        }
