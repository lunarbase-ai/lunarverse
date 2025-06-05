#!/usr/bin/env python3
"""
Workflow runner that can be used both as CLI and as importable module.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import AzureOpenAI
from cee_dart.agents.evidence_integration.models import UserInput, WorkflowResult, ConsolidatedEvidence
from cee_dart.agents.evidence_integration.workflow import WorkflowEngine
from cee_dart.agents.evidence_integration.config import Config
# Import EvaluationStatus from utils
from cee_dart.utils.models import EvaluationStatus


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class NoveltyWorkflowRunner:
    """Main workflow runner that can be used programmatically or via CLI."""
    
    def __init__(self, debug: bool = False, progress_callback=None, client: AzureOpenAI = None):
        self.debug = debug
        self.progress_callback = progress_callback
        self.workflow_engine = WorkflowEngine(progress_callback=progress_callback, client=client)
    
    def _validate_input(self, context: str, question: str) -> None:
        """Validate that required input fields are provided.
        
        Args:
            context: The study context
            question: The user's question
            
        Raises:
            ValidationError: If required fields are missing or empty
        """
        if not context or not context.strip():
            raise ValidationError("Context is required. Please provide study context before running the analysis.")
        
        if not question or not question.strip():
            raise ValidationError("Question/Prompt is required. Please provide a question before running the analysis.")
    
    def _validate_file_exists(self, filepath: str, file_type: str) -> None:
        """Validate that a file exists."""
        if not os.path.exists(filepath):
            raise ValidationError(f"{file_type} file not found: {filepath}")
    
    def _extract_metadata_from_file(self, filepath: str) -> Dict[str, Any]:
        """Extract metadata from a consolidated analysis file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('metadata', {})
        except Exception as e:
            print(f"Warning: Could not extract metadata from {filepath}: {e}")
            return {}
    
    def run_from_files(self, civic_file: str, pharmgkb_file: str, gene_enrichment_file: str,
                      context: str, question: str) -> WorkflowResult:
        """
        Run evidence integration workflow from consolidated analysis files.
        
        Args:
            civic_file: Path to CIVIC analysis consolidated JSON file
            pharmgkb_file: Path to PharmGKB analysis consolidated JSON file
            gene_enrichment_file: Path to Gene Enrichment analysis consolidated JSON file
            context: Study context and background information
            question: User's specific research question
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
            
        Raises:
            ValidationError: If input validation fails
            FileNotFoundError: If any of the input files don't exist
        """
        # Validate inputs
        self._validate_input(context, question)
        self._validate_file_exists(civic_file, "CIVIC")
        self._validate_file_exists(pharmgkb_file, "PharmGKB")
        self._validate_file_exists(gene_enrichment_file, "Gene Enrichment")
        
        print(f"Starting evidence integration workflow...")
        print(f"CIVIC file: {civic_file}")
        print(f"PharmGKB file: {pharmgkb_file}")
        print(f"Gene Enrichment file: {gene_enrichment_file}")
        print(f"Context: {context[:100]}...")
        print(f"Question: {question}")
        
        # Run the workflow
        result = self.workflow_engine.run_workflow_from_files(
            civic_file=civic_file,
            pharmgkb_file=pharmgkb_file,
            gene_enrichment_file=gene_enrichment_file,
            context=context,
            question=question
        )
        
        return result
    
    def run_from_app_data(self, app_data: Dict[str, Any]) -> WorkflowResult:
        """
        Run evidence integration workflow from app data structure.
        
        Args:
            app_data: Dictionary containing analysis results from all three systems
                     Expected structure:
                     {
                         'civic_results': WorkflowResult or dict,
                         'pharmgkb_results': WorkflowResult or dict, 
                         'gene_enrichment_results': WorkflowResult or dict,
                         'context': str,
                         'question': str
                     }
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
            
        Raises:
            ValidationError: If input validation fails or required data is missing
        """
        print("DEBUG: Starting evidence integration run_from_app_data")
        
        # Extract context and question
        context = app_data.get('context', '')
        question = app_data.get('question', '')
        
        print(f"DEBUG: Context: {context[:100]}...")
        print(f"DEBUG: Question: {question}")
        
        # Validate inputs
        self._validate_input(context, question)
        print("DEBUG: Input validation passed")
        
        # Check for required data
        if 'civic_results' not in app_data:
            raise ValidationError("CIVIC results not found in app data")
        if 'pharmgkb_results' not in app_data:
            raise ValidationError("PharmGKB results not found in app data")
        if 'gene_enrichment_results' not in app_data:
            raise ValidationError("Gene Enrichment results not found in app data")
        
        print("DEBUG: All required data found")
        
        # Convert WorkflowResult objects to dictionaries if needed
        def convert_to_dict(data):
            if hasattr(data, 'model_dump'):
                return data.model_dump()
            elif hasattr(data, 'dict'):
                return data.dict()
            else:
                return data
        
        civic_data = convert_to_dict(app_data['civic_results'])
        pharmgkb_data = convert_to_dict(app_data['pharmgkb_results'])
        gene_enrichment_data = convert_to_dict(app_data['gene_enrichment_results'])
        
        print(f"DEBUG: Converted data types - civic: {type(civic_data)}, pharmgkb: {type(pharmgkb_data)}, gene_enrichment: {type(gene_enrichment_data)}")
        
        # Add detailed debug information about the content
        print("=== NOVELTY WORKFLOW DEBUG - EVIDENCE CONTENT ===")
        print(f"CIVIC data keys: {list(civic_data.keys()) if isinstance(civic_data, dict) else 'Not a dict'}")
        print(f"CIVIC data content preview: {str(civic_data)[:300]}...")
        print(f"CIVIC data has final_analysis: {'final_analysis' in civic_data if isinstance(civic_data, dict) else False}")
        
        print(f"PharmGKB data keys: {list(pharmgkb_data.keys()) if isinstance(pharmgkb_data, dict) else 'Not a dict'}")
        print(f"PharmGKB data content preview: {str(pharmgkb_data)[:300]}...")
        print(f"PharmGKB data has final_analysis: {'final_analysis' in pharmgkb_data if isinstance(pharmgkb_data, dict) else False}")
        
        print(f"Gene enrichment data keys: {list(gene_enrichment_data.keys()) if isinstance(gene_enrichment_data, dict) else 'Not a dict'}")
        print(f"Gene enrichment data content preview: {str(gene_enrichment_data)[:300]}...")
        print(f"Gene enrichment data has final_analysis: {'final_analysis' in gene_enrichment_data if isinstance(gene_enrichment_data, dict) else False}")
        print("=== END NOVELTY WORKFLOW DEBUG ===")
        
        # Transform the data structure to match what OrchestratorAgent expects
        def transform_to_expected_format(data, analysis_type):
            """Transform the data to the format expected by OrchestratorAgent."""
            if isinstance(data, dict) and 'final_analysis' in data:
                final_analysis = data['final_analysis']
                total_iterations = data.get('total_iterations', 1)
                
                # Extract actual gene counts from the data
                if analysis_type == 'civic':
                    total_genes = data.get('total_genes', 1)  # Use actual count or default to 1
                    return {
                        'gene_analyses': {
                            'CIVIC_Consolidated_Analysis': {  # More meaningful name
                                'final_analysis': final_analysis
                            }
                        },
                        'summary_stats': {
                            'total_genes': total_genes
                        }
                    }
                elif analysis_type == 'pharmgkb':
                    total_genes = data.get('total_genes', 1)  # Use actual count or default to 1
                    return {
                        'gene_analyses': {
                            'PharmGKB_Consolidated_Analysis': {  # More meaningful name
                                'final_analysis': final_analysis
                            }
                        },
                        'summary_stats': {
                            'total_genes': total_genes
                        }
                    }
                elif analysis_type == 'gene_enrichment':
                    total_gene_sets = data.get('total_gene_sets', 1)  # Use actual count or default to 1
                    return {
                        'gene_set_analyses': {
                            'Gene_Enrichment_Consolidated_Analysis': {  # More meaningful name
                                'final_analysis': final_analysis
                            }
                        },
                        'summary_stats': {
                            'total_gene_sets': total_gene_sets
                        }
                    }
            return data
        
        # Transform the data to the expected format
        civic_data_transformed = transform_to_expected_format(civic_data, 'civic')
        pharmgkb_data_transformed = transform_to_expected_format(pharmgkb_data, 'pharmgkb')
        gene_enrichment_data_transformed = transform_to_expected_format(gene_enrichment_data, 'gene_enrichment')
        
        print("=== TRANSFORMED DATA DEBUG ===")
        print(f"CIVIC transformed keys: {list(civic_data_transformed.keys()) if isinstance(civic_data_transformed, dict) else 'Not a dict'}")
        print(f"PharmGKB transformed keys: {list(pharmgkb_data_transformed.keys()) if isinstance(pharmgkb_data_transformed, dict) else 'Not a dict'}")
        print(f"Gene enrichment transformed keys: {list(gene_enrichment_data_transformed.keys()) if isinstance(gene_enrichment_data_transformed, dict) else 'Not a dict'}")
        print("=== END TRANSFORMED DATA DEBUG ===")
        
        # Check if any of the data is empty
        civic_empty = not civic_data or (isinstance(civic_data, dict) and not any(civic_data.values()))
        pharmgkb_empty = not pharmgkb_data or (isinstance(pharmgkb_data, dict) and not any(pharmgkb_data.values()))
        gene_enrichment_empty = not gene_enrichment_data or (isinstance(gene_enrichment_data, dict) and not any(gene_enrichment_data.values()))
        
        print(f"DEBUG: Data empty status - civic: {civic_empty}, pharmgkb: {pharmgkb_empty}, gene_enrichment: {gene_enrichment_empty}")
        
        if civic_empty and pharmgkb_empty and gene_enrichment_empty:
            raise ValidationError("All evidence data is empty. Cannot proceed with evidence integration.")
        
        # Create temporary files for the workflow
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_civic_file = f"temp_civic_{timestamp}.json"
        temp_pharmgkb_file = f"temp_pharmgkb_{timestamp}.json"
        temp_gene_enrichment_file = f"temp_gene_enrichment_{timestamp}.json"
        
        print(f"DEBUG: Creating temporary files: {temp_civic_file}, {temp_pharmgkb_file}, {temp_gene_enrichment_file}")
        
        try:
            # Write temporary files with the transformed data structure
            with open(temp_civic_file, 'w', encoding='utf-8') as f:
                json.dump(civic_data_transformed, f, indent=2, ensure_ascii=False, default=str)
            
            with open(temp_pharmgkb_file, 'w', encoding='utf-8') as f:
                json.dump(pharmgkb_data_transformed, f, indent=2, ensure_ascii=False, default=str)
            
            with open(temp_gene_enrichment_file, 'w', encoding='utf-8') as f:
                json.dump(gene_enrichment_data_transformed, f, indent=2, ensure_ascii=False, default=str)
            
            print("DEBUG: Temporary files created successfully")
            
            # Run the workflow
            print("DEBUG: Calling run_from_files")
            result = self.run_from_files(
                civic_file=temp_civic_file,
                pharmgkb_file=temp_pharmgkb_file,
                gene_enrichment_file=temp_gene_enrichment_file,
                context=context,
                question=question
            )
            
            print("DEBUG: run_from_files completed successfully")
            return result
            
        finally:
            # Clean up temporary files
            for temp_file in [temp_civic_file, temp_pharmgkb_file, temp_gene_enrichment_file]:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        print(f"DEBUG: Removed temporary file: {temp_file}")
                except Exception as e:
                    print(f"Warning: Could not remove temporary file {temp_file}: {e}")
    
    def run_from_json_file(self, json_file: str) -> WorkflowResult:
        """
        Run evidence integration workflow from a JSON file containing file paths and parameters.
        
        Args:
            json_file: Path to JSON file with structure:
                      {
                          "civic_file": "path/to/civic_analysis.json",
                          "pharmgkb_file": "path/to/pharmgkb_analysis.json", 
                          "gene_enrichment_file": "path/to/gene_enrichment_analysis.json",
                          "context": "Study context...",
                          "question": "Research question..."
                      }
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
            
        Raises:
            ValidationError: If input validation fails
            FileNotFoundError: If JSON file or referenced files don't exist
        """
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in file {json_file}: {e}")
        
        # Extract required fields
        required_fields = ['civic_file', 'pharmgkb_file', 'gene_enrichment_file', 'context', 'question']
        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required field '{field}' in JSON file")
        
        return self.run_from_files(
            civic_file=config['civic_file'],
            pharmgkb_file=config['pharmgkb_file'],
            gene_enrichment_file=config['gene_enrichment_file'],
            context=config['context'],
            question=config['question']
        )
    
    def create_sample_config(self, output_file: str = "evidence_integration_config.json") -> str:
        """
        Create a sample configuration file for the evidence integration workflow.
        
        Args:
            output_file: Path where to save the sample configuration
            
        Returns:
            str: Path to the created sample configuration file
        """
        sample_config = {
            "civic_file": "civic_analysis_consolidated_20250526_223159.json",
            "pharmgkb_file": "pharmgkb_analysis_consolidated_20250526_210558.json",
            "gene_enrichment_file": "gene_enrichment_analysis_consolidated_20250526_223219.json",
            "context": "The aim here is to identify differences between responders (pCR) and non-responders (RD) in the two different treatment arms (T-DM1, DHP). The Breast cancer team in the group suggest that non-responding patients have activation of alternative signaling pathways and responding patients have increased anti-tumor immune activity during HER2-targeted treatment. We discovered a significant differences in interactions between the genes when comparing responders vs non-responders.",
            "question": "To what extend the evidence related to these genes explain the fact that one group responds to the treatment?"
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        
        print(f"Sample configuration created: {output_file}")
        return output_file
    
    def get_input_payload_json(self, output_dict: Dict[str, Any]) -> str:
        """Generate JSON string for the input payload sent to AI analysis."""
        return json.dumps(output_dict, indent=2, ensure_ascii=False, default=str)
    
    def get_full_results_json(self, result: WorkflowResult) -> str:
        """Generate comprehensive JSON string for full results including all agent interactions, prompts, responses, and feedback from each iteration."""
        
        # Import prompts for reference
        try:
            from .prompts import (ORCHESTRATOR_PROMPT, REPORT_COMPOSER_PROMPT, 
                                 CONTENT_VALIDATOR_PROMPT, CRITICAL_REVIEWER_PROMPT, RELEVANCE_VALIDATOR_PROMPT)
        except ImportError:
            from prompts import (ORCHESTRATOR_PROMPT, REPORT_COMPOSER_PROMPT, 
                               CONTENT_VALIDATOR_PROMPT, CRITICAL_REVIEWER_PROMPT, RELEVANCE_VALIDATOR_PROMPT)
        
        full_results = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "workflow_type": "Evidence Integration - Evidence Integration",
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "description": "Complete workflow execution trace with all agent interactions, prompts, and responses"
            },
            
            "input_data": {
                "context": result.user_input.context,
                "question": result.user_input.question,
                "evidence_summary": {
                    "total_evidence_length": len(result.user_input.evidence),
                    "civic_evidence_length": len(result.consolidated_evidence.civic_evidence),
                    "pharmgkb_evidence_length": len(result.consolidated_evidence.pharmgkb_evidence),
                    "gene_enrichment_evidence_length": len(result.consolidated_evidence.gene_enrichment_evidence),
                    "total_genes_civic": result.consolidated_evidence.total_genes_civic,
                    "total_genes_pharmgkb": result.consolidated_evidence.total_genes_pharmgkb,
                    "total_gene_sets_enrichment": result.consolidated_evidence.total_gene_sets_enrichment
                }
            },
            
            "system_prompts": {
                "orchestrator": ORCHESTRATOR_PROMPT,
                "report_composer": REPORT_COMPOSER_PROMPT,
                "content_validator": CONTENT_VALIDATOR_PROMPT,
                "critical_reviewer": CRITICAL_REVIEWER_PROMPT,
                "relevance_validator": RELEVANCE_VALIDATOR_PROMPT
            },
            
            "workflow_execution": {
                "orchestrator_coordination": {
                    "description": "Orchestrator coordinates workflow and consolidates evidence",
                    "evidence_sources_integrated": [
                        f"CIVIC: {result.consolidated_evidence.total_genes_civic} genes",
                        f"PharmGKB: {result.consolidated_evidence.total_genes_pharmgkb} genes", 
                        f"Gene Enrichment: {result.consolidated_evidence.total_gene_sets_enrichment} gene sets"
                    ],
                    "combined_evidence_preview": result.user_input.evidence[:500] + "..." if len(result.user_input.evidence) > 500 else result.user_input.evidence
                },
                
                "iterations": []
            },
            
            "final_unified_report": {
                "potential_novel_biomarkers": result.unified_report.potential_novel_biomarkers,
                "implications": result.unified_report.implications,
                "well_known_interactions": result.unified_report.well_known_interactions,
                "conclusions": result.unified_report.conclusions
            },
            
            "workflow_metrics": {
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "agent_executions": []
            }
        }
        
        # Add metrics if available
        if hasattr(result, 'metrics') and result.metrics:
            full_results["workflow_metrics"]["execution_time_seconds"] = result.metrics.total_execution_time_seconds
            full_results["workflow_metrics"]["total_tokens_used"] = {
                "prompt_tokens": result.metrics.total_tokens_used.prompt_tokens,
                "completion_tokens": result.metrics.total_tokens_used.completion_tokens,
                "total_tokens": result.metrics.total_tokens_used.total_tokens
            }
            
            # Add individual agent executions
            for execution in result.metrics.agent_executions:
                full_results["workflow_metrics"]["agent_executions"].append({
                    "agent_name": execution.agent_name,
                    "start_time": execution.start_time.isoformat() if execution.start_time else None,
                    "end_time": execution.end_time.isoformat() if execution.end_time else None,
                    "execution_time_seconds": execution.execution_time_seconds,
                    "tokens_used": {
                        "prompt_tokens": execution.token_usage.prompt_tokens,
                        "completion_tokens": execution.token_usage.completion_tokens,
                        "total_tokens": execution.token_usage.total_tokens
                    }
                })
        
        # Process each iteration with detailed agent interactions
        for iteration_num in range(1, result.total_iterations + 1):
            iteration_data = {
                "iteration_number": iteration_num,
                "report_composer": {},
                "feedback_agents": {},
                "iteration_summary": {}
            }
            
            # Get Report Composer output for this iteration
            if iteration_num <= len(result.report_composer_history):
                report_output = result.report_composer_history[iteration_num - 1]
                
                # Construct the prompt that was sent to Report Composer
                if iteration_num == 1:
                    # First iteration - initial analysis
                    composer_prompt = f"""Context: {result.user_input.context}

Question: {result.user_input.question}

Consolidated Evidence from Three Analysis Systems:
{result.user_input.evidence}

As the Report Composer Agent, create a unified report that integrates evidence from CIVIC, PharmGKB, and Gene Enrichment analyses. Structure your response with the four required sections and provide comprehensive analysis that addresses the research question."""
                    
                    iteration_data["report_composer"] = {
                        "agent_name": "ReportComposer",
                        "system_prompt": REPORT_COMPOSER_PROMPT,
                        "user_prompt": composer_prompt,
                        "prompt_type": "initial_analysis",
                        "response": {
                            "potential_novel_biomarkers": report_output.potential_novel_biomarkers,
                            "implications": report_output.implications,
                            "well_known_interactions": report_output.well_known_interactions,
                            "conclusions": report_output.conclusions,
                            "iteration": report_output.iteration
                        }
                    }
                else:
                    # Revision based on feedback
                    prev_feedback = result.feedback_history[iteration_num - 2]
                    prev_report = result.report_composer_history[iteration_num - 2]
                    
                    composer_prompt = f"""Please revise your previous unified report based on the feedback from all reviewing agents.

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Consolidated Evidence:
{result.user_input.evidence}

Previous Report (Iteration {prev_report.iteration}):
Potential Novel Biomarkers: {prev_report.potential_novel_biomarkers}
Implications: {prev_report.implications}
Well-Known Interactions: {prev_report.well_known_interactions}
Conclusions: {prev_report.conclusions}

Combined Feedback from All Agents:
{prev_feedback.combined_feedback}

Please provide an improved, structured report addressing all feedback points while maintaining the required sections."""
                    
                    iteration_data["report_composer"] = {
                        "agent_name": "ReportComposer",
                        "system_prompt": REPORT_COMPOSER_PROMPT,
                        "user_prompt": composer_prompt,
                        "prompt_type": "revision_based_on_feedback",
                        "previous_report": {
                            "potential_novel_biomarkers": prev_report.potential_novel_biomarkers,
                            "implications": prev_report.implications,
                            "well_known_interactions": prev_report.well_known_interactions,
                            "conclusions": prev_report.conclusions,
                            "iteration": prev_report.iteration
                        },
                        "feedback_received": prev_feedback.combined_feedback,
                        "response": {
                            "potential_novel_biomarkers": report_output.potential_novel_biomarkers,
                            "implications": report_output.implications,
                            "well_known_interactions": report_output.well_known_interactions,
                            "conclusions": report_output.conclusions,
                            "iteration": report_output.iteration
                        }
                    }
            
            # Get feedback for this iteration
            if iteration_num <= len(result.feedback_history):
                feedback_collection = result.feedback_history[iteration_num - 1]
                report_for_feedback = result.report_composer_history[iteration_num - 1]
                
                # Content Validator Agent
                evaluator_prompt = f"""Please evaluate the following unified biomedical report:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {result.consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {result.consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {result.consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_for_feedback.iteration}):

Potential Novel Biomarkers:
{report_for_feedback.potential_novel_biomarkers}

Implications:
{report_for_feedback.implications}

Well-Known Interactions:
{report_for_feedback.well_known_interactions}

Conclusions:
{report_for_feedback.conclusions}

Evaluate for structural integrity, content quality, and completeness. Respond with "APPROVED" or "NOT APPROVED" followed by specific feedback if needed."""
                
                # Critical Reviewer Agent
                critic_prompt = f"""Please provide critical analysis of the following unified biomedical report:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {result.consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {result.consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {result.consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_for_feedback.iteration}):

Potential Novel Biomarkers:
{report_for_feedback.potential_novel_biomarkers}

Implications:
{report_for_feedback.implications}

Well-Known Interactions:
{report_for_feedback.well_known_interactions}

Conclusions:
{report_for_feedback.conclusions}

Analyze for potential biases, unsupported claims, and alternative interpretations. Respond with "APPROVED" or "NOT APPROVED" followed by specific critical feedback if needed."""
                
                # Relevance Validator Agent
                deliberation_prompt = f"""Please provide critical deliberation analysis focusing on whether this report truly answers the user's question and the basis for novelty assessments:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {result.consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {result.consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {result.consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_for_feedback.iteration}):

Potential Novel Biomarkers:
{report_for_feedback.potential_novel_biomarkers}

Implications:
{report_for_feedback.implications}

Well-Known Interactions:
{report_for_feedback.well_known_interactions}

Conclusions:
{report_for_feedback.conclusions}

CRITICAL EVALUATION FOCUS:
1. Does this report actually answer the user's specific question: "{result.user_input.question}"?
2. What is the basis for classifying evidence as "novel" vs "well-known"?
3. Are the conclusions logically supported by the evidence?

Respond with "APPROVED" or "NOT APPROVED" followed by specific deliberation feedback focusing on question alignment and novelty assessment basis."""
                
                iteration_data["feedback_agents"] = {
                    "content_validator": {
                        "agent_name": "Content Validator",
                        "system_prompt": CONTENT_VALIDATOR_PROMPT,
                        "user_prompt": evaluator_prompt,
                        "response": {
                            "status": feedback_collection.evaluator_feedback.status.value,
                            "feedback_points": feedback_collection.evaluator_feedback.feedback_points
                        }
                    },
                    "critical_reviewer": {
                        "agent_name": "Critical Reviewer",
                        "system_prompt": CRITICAL_REVIEWER_PROMPT,
                        "user_prompt": critic_prompt,
                        "response": {
                            "status": feedback_collection.critic_feedback.status.value,
                            "feedback_points": feedback_collection.critic_feedback.feedback_points
                        }
                    },
                    "relevance_validator": {
                        "agent_name": "Relevance Validator",
                        "system_prompt": RELEVANCE_VALIDATOR_PROMPT,
                        "user_prompt": deliberation_prompt,
                        "response": {
                            "status": feedback_collection.deliberation_feedback.status.value,
                            "feedback_points": feedback_collection.deliberation_feedback.feedback_points
                        }
                    },
                    "combined_feedback": feedback_collection.combined_feedback,
                    "all_approved": feedback_collection.all_approved
                }
            
            # Iteration summary
            iteration_data["iteration_summary"] = {
                "iteration_number": iteration_num,
                "report_composer_completed": iteration_num <= len(result.report_composer_history),
                "feedback_completed": iteration_num <= len(result.feedback_history),
                "all_agents_approved": feedback_collection.all_approved if iteration_num <= len(result.feedback_history) else False,
                "workflow_continues": not (feedback_collection.all_approved if iteration_num <= len(result.feedback_history) else False)
            }
            
            full_results["workflow_execution"]["iterations"].append(iteration_data)
        
        # Add workflow completion summary
        full_results["workflow_completion"] = {
            "completed_successfully": result.final_status == EvaluationStatus.APPROVED,
            "final_status": result.final_status.value,
            "total_iterations_required": result.total_iterations,
            "reason_for_completion": "All feedback agents approved the final report" if result.final_status == EvaluationStatus.APPROVED else "Maximum iterations reached or workflow terminated"
        }
        
        return json.dumps(full_results, indent=2, ensure_ascii=False, default=str)
    
    def get_consolidated_data_json(self, result: WorkflowResult) -> str:
        """Generate JSON string for consolidated analysis results."""
        consolidated_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "context": result.user_input.context,
                "question": result.user_input.question,
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "evidence_sources": {
                    "civic_genes": result.consolidated_evidence.total_genes_civic,
                    "pharmgkb_genes": result.consolidated_evidence.total_genes_pharmgkb,
                    "gene_sets": result.consolidated_evidence.total_gene_sets_enrichment
                }
            },
            "unified_report": {
                "potential_novel_biomarkers": result.unified_report.potential_novel_biomarkers,
                "implications": result.unified_report.implications,
                "well_known_interactions": result.unified_report.well_known_interactions,
                "conclusions": result.unified_report.conclusions
            },
            "summary_stats": {
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "evidence_integration": "CIVIC + PharmGKB + Gene Enrichment",
                "report_sections_completed": sum(1 for section in [
                    result.unified_report.potential_novel_biomarkers,
                    result.unified_report.implications,
                    result.unified_report.well_known_interactions,
                    result.unified_report.conclusions
                ] if section and section.strip())
            }
        }
        
        return json.dumps(consolidated_data, indent=2, ensure_ascii=False, default=str)
    
    def get_prompts_json(self, result: WorkflowResult, input_payload: Dict[str, Any]) -> str:
        """Generate JSON string for all prompts sent to LLM agents during analysis."""
        from .prompts import (ORCHESTRATOR_PROMPT, REPORT_COMPOSER_PROMPT, 
                             CONTENT_VALIDATOR_PROMPT, CRITICAL_REVIEWER_PROMPT, RELEVANCE_VALIDATOR_PROMPT)
        
        prompts_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_iterations": result.total_iterations,
                "description": "Full prompts sent to LLM agents during evidence integration",
                "note": "Each agent call includes both system prompt and user message. Evidence from all three systems is integrated."
            },
            "system_prompts": {
                "orchestrator": ORCHESTRATOR_PROMPT,
                "report_composer": REPORT_COMPOSER_PROMPT,
                "content_validator": CONTENT_VALIDATOR_PROMPT,
                "critical_reviewer": CRITICAL_REVIEWER_PROMPT,
                "relevance_validator": RELEVANCE_VALIDATOR_PROMPT
            },
            "workflow_prompts": {
                "context": result.user_input.context,
                "question": result.user_input.question,
                "evidence_length": len(result.user_input.evidence),
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "evidence_sources": {
                    "civic_evidence_length": len(result.consolidated_evidence.civic_evidence),
                    "pharmgkb_evidence_length": len(result.consolidated_evidence.pharmgkb_evidence),
                    "gene_enrichment_evidence_length": len(result.consolidated_evidence.gene_enrichment_evidence)
                },
                "report_composer_prompts": [],
                "content_validator_prompts": [],
                "critical_reviewer_prompts": [],
                "relevance_validator_prompts": []
            }
        }
        
        # Add prompts for each iteration
        for i, report_output in enumerate(result.report_composer_history, 1):
            # Report Composer prompt
            if i == 1:
                # First iteration
                composer_prompt = f"""
Context: {result.user_input.context}
Question: {result.user_input.question}

Consolidated Evidence from Three Systems:
{result.user_input.evidence}

As the Report Composer Agent, create a unified report integrating evidence from CIVIC, PharmGKB, and Gene Enrichment analyses. Structure your response with the four mandatory sections: Potential Novel Biomarkers, Implications, Well-Known Interactions, and Conclusions.
"""
            else:
                # Revision based on feedback
                prev_feedback = result.feedback_history[i-2]
                composer_prompt = f"""
Please revise your previous unified report based on feedback from all three reviewing agents.

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Consolidated Evidence:
{result.user_input.evidence}

Previous Report (Iteration {i-1}):
{result.report_composer_history[i-2].potential_novel_biomarkers}

Combined Feedback:
{prev_feedback.combined_feedback}

Please provide an improved unified report addressing all feedback points.
"""
            
            prompts_data["workflow_prompts"]["report_composer_prompts"].append({
                "iteration": i,
                "type": "initial_analysis" if i == 1 else "revision",
                "user_message": composer_prompt
            })
        
        # Add feedback agent prompts for each iteration
        for i, feedback in enumerate(result.feedback_history, 1):
            report_output = result.report_composer_history[i-1]
            
            # Content Validator prompt
            evaluator_prompt = f"""
Please evaluate the following unified biomedical report:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence Provided:
{result.user_input.evidence}

Report Composer Output (Iteration {i}):
Potential Novel Biomarkers: {report_output.potential_novel_biomarkers}
Implications: {report_output.implications}
Well-Known Interactions: {report_output.well_known_interactions}
Conclusions: {report_output.conclusions}

Evaluate for structural integrity, content quality, and completeness. Respond with "APPROVED" or "NOT APPROVED" followed by specific feedback.
"""
            
            # Critical Reviewer prompt
            critic_prompt = f"""
Please provide critical analysis of the following unified biomedical report:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence Provided:
{result.user_input.evidence}

Report Composer Output (Iteration {i}):
{report_output.potential_novel_biomarkers}

Identify potential biases, unsupported claims, and alternative interpretations. Respond with "APPROVED" or "NOT APPROVED" followed by critical feedback.
"""
            
            # Relevance Validator prompt
            deliberation_prompt = f"""
Please evaluate whether this report truly answers the user's question and examine the basis for novelty assessments:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence Provided:
{result.user_input.evidence}

Report Composer Output (Iteration {i}):
{report_output.potential_novel_biomarkers}

Focus on question alignment and novelty classification. Respond with "APPROVED" or "NOT APPROVED" followed by deliberation feedback.
"""
            
            prompts_data["workflow_prompts"]["content_validator_prompts"].append({
                "iteration": i,
                "user_message": evaluator_prompt
            })
            
            prompts_data["workflow_prompts"]["critical_reviewer_prompts"].append({
                "iteration": i,
                "user_message": critic_prompt
            })
            
            prompts_data["workflow_prompts"]["relevance_validator_prompts"].append({
                "iteration": i,
                "user_message": deliberation_prompt
            })
        
        return json.dumps(prompts_data, indent=2, ensure_ascii=False, default=str)

def create_workflow_runner(progress_callback=None) -> NoveltyWorkflowRunner:
    """Create a new workflow runner instance."""
    return NoveltyWorkflowRunner(progress_callback=progress_callback)

# Main execution for testing
if __name__ == "__main__":
    import sys
    
    def simple_progress_callback(message: str):
        """Simple progress callback for testing."""
        print(f"Progress: {message}")
    
    runner = NoveltyWorkflowRunner(progress_callback=simple_progress_callback)
    
    if len(sys.argv) == 2:
        # Run from JSON config file
        try:
            result = runner.run_from_json_file(sys.argv[1])
            print(f"\nWorkflow completed successfully!")
            print(f"Final status: {result.final_status.value}")
            print(f"Total iterations: {result.total_iterations}")
            print(f"Evidence sources: CIVIC({result.consolidated_evidence.total_genes_civic}), "
                  f"PharmGKB({result.consolidated_evidence.total_genes_pharmgkb}), "
                  f"Gene sets({result.consolidated_evidence.total_gene_sets_enrichment})")
        except (ValidationError, FileNotFoundError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif len(sys.argv) == 6:
        # Run with individual file arguments
        civic_file, pharmgkb_file, gene_enrichment_file, context, question = sys.argv[1:6]
        try:
            result = runner.run_from_files(civic_file, pharmgkb_file, gene_enrichment_file, context, question)
            print(f"\nWorkflow completed successfully!")
            print(f"Final status: {result.final_status.value}")
            print(f"Total iterations: {result.total_iterations}")
        except (ValidationError, FileNotFoundError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Create sample config and show usage
        sample_file = runner.create_sample_config()
        print(f"\nUsage:")
        print(f"  python workflow_runner.py <config.json>")
        print(f"  python workflow_runner.py <civic_file> <pharmgkb_file> <gene_enrichment_file> <context> <question>")
        print(f"\nExample:")
        print(f"  python workflow_runner.py {sample_file}")
        print(f"\nEdit {sample_file} with your actual file paths and run the workflow.") 