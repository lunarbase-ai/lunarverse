
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent
from openai import AzureOpenAI
from typing import Any
from cee_dart.agents.pharmgkb.workflow_runner import WorkflowRunner as PharmGKBWorkflowRunner
import os


class PharmGKBAnalysis(
    LunarComponent,
    component_name="PharmGKB Analysis",
    component_description="Analyzes PharmGKB evidence.",
    input_types={"context": DataType.TEXT, "question": DataType.TEXT, "pharmgkb_evidence": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.BIOMEDICAL,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

        self.client = AzureOpenAI(
            api_version=self.configuration["openai_api_version"],
            azure_endpoint=self.configuration["azure_endpoint"],
            api_key=self.configuration["openai_api_key"],
        )

        self.runner = PharmGKBWorkflowRunner(client=self.client)

    def run(self, context: str, question: str, pharmgkb_evidence: dict) -> dict:
        data = {
            "Context": context,
            "Question": question,
            "pharmGKB Analysis": pharmgkb_evidence,
        }
        return self.runner.run_from_dict(data)


