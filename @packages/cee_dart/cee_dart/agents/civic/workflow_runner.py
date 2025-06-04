#!/usr/bin/env python3
"""
Workflow runner that can be used both as CLI and as importable module.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from cee_dart.agents.civic.models import UserInput, WorkflowResult
from cee_dart.agents.civic.workflow import create_workflow_engine
from cee_dart.agents.civic.prompts import BIOEXPERT_PROMPT, EVALUATOR_PROMPT


class WorkflowRunner:
    """Main workflow runner that can be used programmatically or via CLI."""
    
    def __init__(self, debug: bool = False, progress_callback=None):
        self.debug = debug
        self.progress_callback = progress_callback
        self.workflow = create_workflow_engine(progress_callback=progress_callback)
    
    def _extract_gene_name_from_evidence(self, evidence: str, index: int) -> str:
        """Extract gene name from evidence string or use fallback naming."""
        # Try to find gene name in evidence string
        lines = evidence.split('\n')
        for line in lines:
            if line.startswith("Gene: "):
                return line.replace("Gene: ", "").strip()
            elif line.startswith("No clinical evidence available for gene "):
                return line.replace("No clinical evidence available for gene ", "").strip()
        
        # Fallback to index-based naming
        return f'Gene_{index}'
    
    def run_from_app_data(self, output_dict: Dict[str, Any]) -> tuple[List[WorkflowResult], Dict[str, Any]]:
        """Run workflow from app.py output_dict format."""
        inputs = self._convert_app_data_to_inputs(output_dict)
        # Process genes sequentially with progress tracking
        results = []
        total_genes = len(inputs)
        
        if self.progress_callback:
            self.progress_callback(f"**CIViC evidence interpretation** - Starting AI analysis for {total_genes} gene(s)")
        
        for i, inp in enumerate(inputs, 1):
            gene_name = self._extract_gene_name_from_evidence(inp.evidence, i)
            # Update progress for current gene
            if self.progress_callback:
                self.progress_callback(f"**CIViC evidence interpretation** - Processing gene {i}/{total_genes}: {gene_name}")
            
            result = self.workflow.run_workflow(inp)
            results.append(result)
            
            # Update progress after gene completion
            if self.progress_callback:
                status_emoji = "✅" if result.final_status.value == "APPROVED" else "⚠️"
                self.progress_callback(f"**CIViC evidence interpretation** - {status_emoji} Gene {i}/{total_genes} ({gene_name}) completed - {result.total_iterations} iteration(s)")
        
        # Final completion message
        if self.progress_callback:
            approved_count = sum(1 for r in results if r.final_status.value == "APPROVED")
            self.progress_callback(f"**CIViC evidence interpretation** - 🎉 All genes completed! {approved_count}/{total_genes} analyses approved")
        
        # Generate consolidated data for session state
        consolidated_data = self._generate_consolidated_data(results)
        
        # Return the first result as consolidated for metrics display
        consolidated_result = results[0] if results else None
        
        return results, consolidated_result
    
    def _load_input_from_dict(self, output_dict: Dict[str, Any]) -> List[UserInput]:
        """Load input from dictionary."""
        context = output_dict.get('Context', None)
        question = output_dict.get('Question', None)
        civic_evidence = output_dict.get('CIVIC Evidence', None)
        
        if not context or not question or not civic_evidence:
            raise ValueError("Context, Question, and CIVIC Evidence are required")
        
        inputs: List[UserInput] = []
        gene_evidence_pairs = self._process_civic_evidence_data(civic_evidence)

        for gene, combined_evidence in gene_evidence_pairs:
            evidence_parts = combined_evidence.split('\n\n')
            
            # Only create UserInput if there's at least some evidence
            if len(evidence_parts) > 1:  # More than just the gene name
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=combined_evidence
                ))
            else:
                # If no evidence, still create input but with a note
                no_evidence_text = f"Gene: {gene}\n\nNo clinical evidence available for gene {gene}"
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=no_evidence_text
                ))
        return inputs
    
    def run_from_dict(self, output_dict: Dict[str, Any]) -> tuple[List[WorkflowResult], Dict[str, Any]]:
        """Run workflow from dictionary."""
        inputs = self._load_input_from_dict(output_dict)
        results = []
        total_genes = len(inputs)
        
        for i, inp in enumerate(inputs, 1):
            gene_name = self._extract_gene_name_from_evidence(inp.evidence, i)
            
            # Update progress for current gene (if callback available)
            if self.progress_callback:
                self.progress_callback(f"**Processing gene {i}/{total_genes}: {gene_name}**")
            
            result = self.workflow.run_workflow(inp)
            results.append(result)
            
            # Update progress after gene completion (if callback available)
            if self.progress_callback:
                status_emoji = "✅" if result.final_status.value == "APPROVED" else "⚠️"
                self.progress_callback(f"{status_emoji} **Gene {i}/{total_genes} ({gene_name}) completed** - {result.total_iterations} iteration(s)")
        
        # Final completion message (if callback available)
        if self.progress_callback:
            approved_count = sum(1 for r in results if r.final_status.value == "APPROVED")
            self.progress_callback(f"🎉 **All genes completed!** {approved_count}/{total_genes} analyses approved")
        
        return results 
    
    def run_from_json_file(self, file_path: str) -> List[WorkflowResult]:
        """Run workflow from JSON file (original CLI functionality)."""
        inputs = self._load_input_from_file(file_path)
        
        # Process genes sequentially
        results = []
        total_genes = len(inputs)
        
        for i, inp in enumerate(inputs, 1):
            gene_name = self._extract_gene_name_from_evidence(inp.evidence, i)
            
            # Update progress for current gene (if callback available)
            if self.progress_callback:
                self.progress_callback(f"**Processing gene {i}/{total_genes}: {gene_name}**")
            
            result = self.workflow.run_workflow(inp)
            results.append(result)
            
            # Update progress after gene completion (if callback available)
            if self.progress_callback:
                status_emoji = "✅" if result.final_status.value == "APPROVED" else "⚠️"
                self.progress_callback(f"{status_emoji} **Gene {i}/{total_genes} ({gene_name}) completed** - {result.total_iterations} iteration(s)")
        
        # Final completion message (if callback available)
        if self.progress_callback:
            approved_count = sum(1 for r in results if r.final_status.value == "APPROVED")
            self.progress_callback(f"🎉 **All genes completed!** {approved_count}/{total_genes} analyses approved")
        
        return results
    
    
    def _process_civic_evidence_data(self, civic_evidence: dict) -> List[tuple[str, str]]:
        """Process CIVIC Evidence data into gene-evidence pairs.
        
        Args:
            civic_evidence: Dictionary of CIVIC evidence data (gene -> gene_data dict)
            
        Returns:
            List of tuples containing (gene_name, combined_evidence_string)
        """
        gene_evidence_pairs = []
        
        for gene, gene_data in civic_evidence.items():
            print(f"DEBUG: Processing gene: {gene}")
            print(f"DEBUG: gene_data type: {type(gene_data)}")
            print(f"DEBUG: gene_data content: {gene_data}")
            
            if not isinstance(gene_data, dict):
                print(f"DEBUG: Skipping {gene} - not a dict")
                continue
                
            evidence_parts = []
            
            # Add gene name as first part
            evidence_parts.append(f"Gene: {gene}")
            print(f"DEBUG: Added gene name")
            
            # Add Description and Summary
            description = gene_data.get('Description')
            summary = gene_data.get('Summary')
            
            print(f"DEBUG: Description: {description}")
            print(f"DEBUG: Summary: {summary}")
            
            if description and description.strip():
                evidence_parts.append(f"Gene Description: {description}")
            
            if summary and summary.strip():
                evidence_parts.append(f"Gene Summary: {summary}")
            
            # Add molecular profiles
            molecular_profiles = gene_data.get('Molecular_profiles', [])
            print(f"DEBUG: Molecular_profiles: {molecular_profiles}")
            if molecular_profiles:
                for i, profile in enumerate(molecular_profiles):
                    if profile and profile.strip():
                        evidence_parts.append(f"Molecular Profile {i+1}: {profile}")
            
            # Add clinical evidence
            evidence_list = gene_data.get('Evidence', [])
            print(f"DEBUG: Evidence list: {evidence_list}")
            if evidence_list:
                for i, evidence_item in enumerate(evidence_list):
                    if isinstance(evidence_item, dict):
                        evidence_str = self._format_evidence_item(evidence_item, i+1)
                        evidence_parts.append(evidence_str)
                    else:
                        evidence_parts.append(str(evidence_item))
            
            # Combine all evidence parts into a single string
            combined_evidence = "\n\n".join(evidence_parts)
            print(f"DEBUG: Combined evidence length: {len(combined_evidence)}")
            print(f"DEBUG: Combined evidence preview: {combined_evidence[:200]}...")
            
            gene_evidence_pairs.append((gene, combined_evidence))
        
        return gene_evidence_pairs

    def _convert_app_data_to_inputs(self, output_dict: Dict[str, Any]) -> List[UserInput]:
        """Convert app.py output_dict to UserInput objects."""
        context = output_dict.get('Context', '')
        question = output_dict.get('Prompt', '')  # Note: 'Prompt' in app, 'Question' in main
        civic_evidence = output_dict.get('CIVIC Evidence', {})
        
        print("DEBUG: civic_evidence keys:", list(civic_evidence.keys()) if civic_evidence else "No CIVIC Evidence")
        print("DEBUG: civic_evidence type:", type(civic_evidence))
        print("DEBUG: civic_evidence content:", civic_evidence)
        
        # You can also include other data types if needed
        gene_enrichment = output_dict.get('Gene Enrichment')
        community_enrichment = output_dict.get('Community Enrichment') 
        pharmgkb_analysis = output_dict.get('pharmGKB Analysis')
        
        inputs: List[UserInput] = []
        
        # Process CIVIC evidence data using the common method
        gene_evidence_pairs = self._process_civic_evidence_data(civic_evidence)
        
        for gene, combined_evidence in gene_evidence_pairs:
            evidence_parts = combined_evidence.split('\n\n')
            
            if len(evidence_parts) > 1:  # More than just the gene name
                print("DEBUG: Creating UserInput with evidence")
                print(f"DEBUG: Final evidence string length: {len(combined_evidence)}")
                print(f"DEBUG: Final evidence string preview: {combined_evidence[:300]}...")
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=combined_evidence
                ))
            else:
                print("DEBUG: Creating UserInput with no evidence message")
                no_evidence_text = f"Gene: {gene}\n\nNo clinical evidence available for gene {gene}"
                print(f"DEBUG: No evidence text: {no_evidence_text}")
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=no_evidence_text
                ))
        
        print(f"DEBUG: Total inputs created: {len(inputs)}")
        return inputs
    
    def _format_evidence_item(self, evidence_item: dict, index: int) -> str:
        """Format evidence dictionary into readable string."""
        statement = evidence_item.get('statement', 'N/A')
        evidence_name = evidence_item.get('evidence_name', 'N/A')
        
        return f"Statement: {statement} [{evidence_name}]"
    
    
    def _load_input_from_file(self, file_path: str) -> List[UserInput]:
        """Load sample_input.json with 'Context', 'Question', and 'CIVIC Evidence' mapping."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            context = data.get('Context', '')
            question = data.get('Question', '')
            civic = data.get('CIVIC Evidence', {})  # dict: gene -> evidence list
            
            inputs: List[UserInput] = []
            
            # Process CIVIC evidence data using the common method
            gene_evidence_pairs = self._process_civic_evidence_data(civic)
            
            for gene, combined_evidence in gene_evidence_pairs:
                evidence_parts = combined_evidence.split('\n\n')
                
                # Only create UserInput if there's at least some evidence
                if len(evidence_parts) > 1:  # More than just the gene name
                    inputs.append(UserInput(
                        context=context,
                        question=question,
                        evidence=combined_evidence
                    ))
                else:
                    # If no evidence, still create input but with a note
                    no_evidence_text = f"Gene: {gene}\n\nNo clinical evidence available for gene {gene}"
                    inputs.append(UserInput(
                        context=context,
                        question=question,
                        evidence=no_evidence_text
                    ))
            return inputs
        except FileNotFoundError:
            raise Exception(f"Input file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in input file: {e}")
        except Exception as e:
            raise Exception(f"Error loading input file: {e}")
    
    def save_results_to_files(self, results: List[WorkflowResult], 
                            output_path: Optional[str] = None,
                            consolidated_path: Optional[str] = None):
        """Save results to files."""
        if output_path:
            for i, result in enumerate(results, 1):
                # append gene name if available
                gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, i)
                suffix = gene_name if gene_name != f'Gene_{i}' else None
                out_path = Path(output_path)
                if suffix:
                    out_path = out_path.with_name(f"{out_path.stem}_{suffix}{out_path.suffix}")
                self._save_output_to_file(result, str(out_path))
        
        # Create consolidated final analysis file
        if consolidated_path:
            self._save_consolidated_final_analysis(results, consolidated_path)
        elif len(results) > 1:
            # Auto-generate consolidated file if multiple genes processed
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            consolidated_path = f"consolidated_final_analysis_{timestamp}.json"
            self._save_consolidated_final_analysis(results, consolidated_path)
    
    def _save_consolidated_final_analysis(self, results: List[WorkflowResult], file_path: str):
        """Save consolidated final analysis results to JSON file (without history)."""
        try:
            # Create consolidated data structure
            consolidated_data = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "total_genes_analyzed": len(results),
                    "context": results[0].user_input.context if results else "",
                    "question": results[0].user_input.question if results else ""
                },
                "gene_analyses": {}
            }
            
            # Add each gene's final analysis
            for result in results:
                gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
                
                consolidated_data["gene_analyses"][gene_name] = {
                    "final_analysis": result.final_analysis,
                    "final_status": result.final_status.value,
                    "total_iterations": result.total_iterations,
                    "evidence_length": len(result.user_input.evidence)
                }
            
            # Save to file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
            
            print(f"Consolidated final analysis saved to {file_path}")
            print(f"Analyzed {len(results)} genes total")
            
        except Exception as e:
            print(f"❌ Failed to save consolidated analysis: {e}")
    
    def _save_output_to_file(self, result: WorkflowResult, file_path: str):
        """Save workflow result to JSON file."""
        try:
            # Convert to dict for JSON serialization
            output_data = {
                "final_analysis": result.final_analysis,
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "user_input": {
                    "context": result.user_input.context,
                    "question": result.user_input.question,
                    "evidence": result.user_input.evidence,
                },
                "evaluation_history": [
                    {
                        "status": eval_output.status.value,
                        "feedback_points": eval_output.feedback_points,
                    }
                    for eval_output in result.evaluation_history
                ],
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving output file: {e}")
    
    def _generate_consolidated_data(self, results: List[WorkflowResult]) -> Dict[str, Any]:
        """Generate consolidated data structure without saving to file."""
        # Create consolidated data structure
        consolidated_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_genes_analyzed": len(results),
                "context": results[0].user_input.context if results else "",
                "question": results[0].user_input.question if results else ""
            },
            "gene_analyses": {},
            "summary_stats": {
                "total_genes": len(results),
                "approved_analyses": sum(1 for r in results if r.final_status.value == "APPROVED"),
                "average_iterations": sum(r.total_iterations for r in results) / len(results) if results else 0,
                "genes_with_evidence": sum(1 for r in results if r.user_input.evidence and len(r.user_input.evidence.strip()) > 0)  # Non-empty evidence
            }
        }
        
        # Add each gene's final analysis
        for result in results:
            gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
            
            consolidated_data["gene_analyses"][gene_name] = {
                "final_analysis": result.final_analysis,
                "final_status": result.final_status.value,
                "total_iterations": result.total_iterations,
                "evidence_length": len(result.user_input.evidence)
            }
        
        return consolidated_data
    
    def get_input_payload_json(self, output_dict: Dict[str, Any]) -> str:
        """Generate JSON string for the input payload sent to AI analysis."""
        return json.dumps(output_dict, indent=2, ensure_ascii=False, default=str)
    
    def get_full_results_json(self, results: List[WorkflowResult]) -> str:
        """Generate JSON string for full results including evaluation and bioexpert history."""
        results_dict = []
        for result in results:
            result_dict = {
                "final_analysis": result.final_analysis,
                "total_iterations": result.total_iterations,
                "final_status": result.final_status.value,
                "user_input": {
                    "context": result.user_input.context,
                    "question": result.user_input.question,
                    "evidence": result.user_input.evidence,
                },
                "evaluation_history": [
                    {
                        "status": eval_output.status.value,
                        "feedback_points": eval_output.feedback_points,
                    }
                    for eval_output in result.evaluation_history
                ],
                "bioexpert_history": [
                    {
                        "relevance_explanation": bio_output.relevance_explanation,
                        "summary_conclusion": bio_output.summary_conclusion,
                        "iteration": bio_output.iteration,
                    }
                    for bio_output in result.bioexpert_history
                ],
            }
            results_dict.append(result_dict)
        
        return json.dumps(results_dict, indent=2, ensure_ascii=False, default=str)
    
    def get_consolidated_data_json(self, consolidated_data) -> str:
        """Generate JSON string for consolidated analysis results."""
        # Handle both WorkflowResult objects and dictionaries
        if hasattr(consolidated_data, 'model_dump'):
            # It's a Pydantic model (WorkflowResult), convert to dict
            data_dict = consolidated_data.model_dump()
        elif hasattr(consolidated_data, 'dict'):
            # It's a Pydantic model with older method name
            data_dict = consolidated_data.dict()
        else:
            # It's already a dictionary
            data_dict = consolidated_data
        
        return json.dumps(data_dict, indent=2, ensure_ascii=False, default=str)
    
    def get_prompts_json(self, results: List[WorkflowResult], input_payload: Dict[str, Any]) -> str:
        """Generate JSON string for all prompts sent to LLM agents during analysis."""
        prompts_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_genes": len(results),
                "description": "Full prompts sent to LLM agents during AI analysis",
                "note": "Each agent call includes both system prompt and user message. Evidence text is included in all prompts."
            },
            "system_prompts": {
                "orchestrator": "Orchestrator uses pure Python routing logic - no LLM calls",
                "bioexpert": BIOEXPERT_PROMPT,
                "evaluator": EVALUATOR_PROMPT
            },
            "gene_prompts": {}
        }
        
        for result in results:
            gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
            # Handle evidence as string
            evidence_text = result.user_input.evidence if result.user_input.evidence else "No evidence provided."
            
            gene_prompts = {
                "gene_info": {
                    "gene_name": gene_name,
                    "context": result.user_input.context,
                    "question": result.user_input.question,
                    "evidence_length": len(result.user_input.evidence),
                    "total_iterations": result.total_iterations,
                    "final_status": result.final_status.value
                },
                "evidence_text": evidence_text,
                "bioexpert_prompts": [],
                "evaluator_prompts": []
            }
            
            # First iteration BioExpert prompt
            first_bioexpert_prompt = f"""
Context: {result.user_input.context}
Question: {result.user_input.question}
Evidence:
{evidence_text}

As the BioExpert Agent, analyze the evidence and answer the question in a structured format with relevance explanation and summary/conclusion. Cite evidence sources explicitly.
"""
            gene_prompts["bioexpert_prompts"].append({
                "iteration": 1,
                "type": "initial_analysis",
                "user_message": first_bioexpert_prompt
            })
            
            # Subsequent iteration prompts (if any)
            for i, bio_output in enumerate(result.bioexpert_history[1:], 2):
                if i <= len(result.evaluation_history):
                    prev_eval = result.evaluation_history[i-2]
                    prev_bio = result.bioexpert_history[i-2]
                    
                    prev_str = "\n".join([
                        f"Relevance Explanation: {prev_bio.relevance_explanation}",
                        "Summary/Conclusion:",
                        *[f"- {line}" for line in prev_bio.summary_conclusion]
                    ])
                    
                    feedback_text = "\n".join(f"- {point}" for point in prev_eval.feedback_points)
                    
                    revision_prompt = f"""
Please revise your previous analysis based on the evaluator's feedback.

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence:
{evidence_text}

Previous Analysis (Iteration {prev_bio.iteration}):
{prev_str}

Evaluator Feedback:
{feedback_text}

Please provide an improved, structured analysis addressing each point of feedback.
"""
                    gene_prompts["bioexpert_prompts"].append({
                        "iteration": i,
                        "type": "revision",
                        "user_message": revision_prompt
                    })
            
            # Evaluator prompts for each iteration
            for i, bio_output in enumerate(result.bioexpert_history, 1):
                summary_block = "\n".join(f"- {pt}" for pt in bio_output.summary_conclusion)
                evaluator_prompt = f"""
Please evaluate the following biomedical evidence analysis:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence Provided:
{evidence_text}

BioExpert Analysis (Iteration {bio_output.iteration}):
Relevance Explanation:
{bio_output.relevance_explanation}

Summary/Conclusion:
{summary_block}

Respond exactly with:
- "APPROVED" if the analysis meets quality standards
- Or "NOT APPROVED" followed by specific, actionable feedback
Focus on scientific accuracy, clarity, citation, and completeness.
"""
                gene_prompts["evaluator_prompts"].append({
                    "iteration": i,
                    "user_message": evaluator_prompt
                })
            
            prompts_data["gene_prompts"][gene_name] = gene_prompts
        
        return json.dumps(prompts_data, indent=2, ensure_ascii=False, default=str) 