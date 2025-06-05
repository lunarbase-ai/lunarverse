
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent
from openai import AzureOpenAI
from typing import Any
from cee_dart.agents.evidence_integration.workflow_runner import NoveltyWorkflowRunner



class CeeDartAnalysisEvidenceIntegrator(
    LunarComponent,
    component_name="Cee Dart Evidence Integrator",
    component_description="Analyzes CIViC, PharmGKB, and Gene Enrichment evidence.",
    input_types={
        "context": DataType.TEXT,
        "question": DataType.TEXT,
        "civic_consolidated": DataType.JSON,
        "pharmgkb_consolidated": DataType.JSON,
        "gene_enrichment_consolidated": DataType.JSON
    },
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

        self.runner = NoveltyWorkflowRunner(client=self.client)

    def run(self, civic_consolidated: dict, pharmgkb_consolidated: dict, gene_enrichment_consolidated: dict, context: str, question: str) -> dict:
        return self.runner.run_from_dict(
            civic_consolidated=civic_consolidated,
            pharmgkb_consolidated=pharmgkb_consolidated,
            gene_enrichment_consolidated=gene_enrichment_consolidated,
            context=context,
            question=question,
        ).model_dump()


