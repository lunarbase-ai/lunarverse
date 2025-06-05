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
        result = self.runner.run_from_dict(
            civic_consolidated=civic_consolidated,
            pharmgkb_consolidated=pharmgkb_consolidated,
            gene_enrichment_consolidated=gene_enrichment_consolidated,
            context=context,
            question=question,
        )
        
        # Convert the result to a dictionary with proper serialization
        result_dict = {
            "unified_report": {
                "potential_novel_biomarkers": result.unified_report.potential_novel_biomarkers,
                "implications": result.unified_report.implications,
                "well_known_interactions": result.unified_report.well_known_interactions,
                "conclusions": result.unified_report.conclusions
            },
            "total_iterations": result.total_iterations,
            "final_status": result.final_status.value,
            "user_input": {
                "context": result.user_input.context,
                "question": result.user_input.question,
                "evidence": result.user_input.evidence
            },
            "consolidated_evidence": {
                "civic_evidence": result.consolidated_evidence.civic_evidence,
                "pharmgkb_evidence": result.consolidated_evidence.pharmgkb_evidence,
                "gene_enrichment_evidence": result.consolidated_evidence.gene_enrichment_evidence,
                "combined_evidence": result.consolidated_evidence.combined_evidence,
                "total_genes_civic": result.consolidated_evidence.total_genes_civic,
                "total_genes_pharmgkb": result.consolidated_evidence.total_genes_pharmgkb,
                "total_gene_sets_enrichment": result.consolidated_evidence.total_gene_sets_enrichment
            },
            "feedback_history": [
                {
                    "evaluator_feedback": {
                        "status": feedback.evaluator_feedback.status.value,
                        "feedback_points": feedback.evaluator_feedback.feedback_points
                    },
                    "critic_feedback": {
                        "status": feedback.critic_feedback.status.value,
                        "feedback_points": feedback.critic_feedback.feedback_points
                    },
                    "deliberation_feedback": {
                        "status": feedback.deliberation_feedback.status.value,
                        "feedback_points": feedback.deliberation_feedback.feedback_points
                    }
                }
                for feedback in result.feedback_history
            ],
            "report_composer_history": [
                {
                    "potential_novel_biomarkers": report.potential_novel_biomarkers,
                    "implications": report.implications,
                    "well_known_interactions": report.well_known_interactions,
                    "conclusions": report.conclusions,
                    "iteration": report.iteration
                }
                for report in result.report_composer_history
            ],
            "metrics": {
                "total_execution_time_seconds": result.metrics.total_execution_time_seconds,
                "agent_executions": [
                    {
                        "agent_name": exec.agent_name,
                        "start_time": exec.start_time.isoformat() if exec.start_time else None,
                        "end_time": exec.end_time.isoformat() if exec.end_time else None,
                        "token_usage": {
                            "prompt_tokens": exec.token_usage.prompt_tokens,
                            "completion_tokens": exec.token_usage.completion_tokens,
                            "total_tokens": exec.token_usage.total_tokens
                        } if exec.token_usage else None
                    }
                    for exec in result.metrics.agent_executions
                ]
            }
        }
        
        return result_dict


