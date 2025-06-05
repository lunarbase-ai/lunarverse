#!/usr/bin/env python3
"""
Workflow runner that can be used both as CLI and as importable module.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import AzureOpenAI
# Handle imports for both module and direct execution
try:
    from .models import UserInput, WorkflowResult
    from .workflow import create_workflow_engine
    from .prompts import BIOEXPERT_PROMPT, EVALUATOR_PROMPT
except ImportError:
    # Fallback for direct execution
    from models import UserInput, WorkflowResult
    from workflow import create_workflow_engine
    from prompts import BIOEXPERT_PROMPT, EVALUATOR_PROMPT


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class WorkflowRunner:
    """Main workflow runner that can be used programmatically or via CLI."""
    
    def __init__(self, debug: bool = False, progress_callback=None, client: AzureOpenAI = None):
        self.debug = debug
        self.progress_callback = progress_callback
        self.workflow = create_workflow_engine(progress_callback=progress_callback, client=client)
    
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
    
    def _extract_gene_name_from_evidence(self, evidence: str, index: int) -> str:
        """Extract gene name from evidence string or use fallback naming."""
        # Try to find gene name in evidence string
        lines = evidence.split('\n')
        for line in lines:
            if line.startswith("Gene Set: "):
                return line.replace("Gene Set: ", "").strip()
            elif line.startswith("No gene enrichment evidence available for "):
                return line.replace("No gene enrichment evidence available for ", "").strip()
        
        # Fallback to index-based naming
        return f'GeneSet_{index}'
    
    def run_from_app_data(self, output_dict: Dict[str, Any]) -> tuple[List[WorkflowResult], Dict[str, Any]]:
        """Run workflow from app.py output_dict format."""
        # Validate input before processing
        context = output_dict.get('Context', '')
        question = output_dict.get('Prompt', '')
        self._validate_input(context, question)
        
        inputs = self._convert_app_data_to_inputs(output_dict)
        # Process gene sets sequentially with progress tracking
        results = []
        total_sets = len(inputs)
        
        if self.progress_callback:
            self.progress_callback(f"**Gene Enrichment System** - Starting AI analysis for {total_sets} gene enrichment set(s)")
        
        for i, inp in enumerate(inputs, 1):
            set_name = self._extract_gene_name_from_evidence(inp.evidence, i)
            # Update progress for current gene set
            if self.progress_callback:
                self.progress_callback(f"**Gene Enrichment System** - Processing gene set {i}/{total_sets}: {set_name}")
            
            result = self.workflow.run_workflow(inp)
            results.append(result)
            
            # Update progress after gene set completion
            if self.progress_callback:
                status_emoji = "✅" if result.final_status.value == "APPROVED" else "⚠️"
                self.progress_callback(f"**Gene Enrichment System** - {status_emoji} Gene set {i}/{total_sets} ({set_name}) completed - {result.total_iterations} iteration(s)")
        
        # Final completion message
        if self.progress_callback:
            approved_count = sum(1 for r in results if r.final_status.value == "APPROVED")
            self.progress_callback(f"**Gene Enrichment System** - 🎉 All gene sets completed! {approved_count}/{total_sets} analyses approved")
        
        # Generate consolidated data for session state
        consolidated_data = self._generate_consolidated_data(results)
        
        # Return the first result as consolidated for metrics display
        consolidated_result = results[0] if results else None
        
        return results, consolidated_result
    
    def run_from_json_file(self, file_path: str) -> List[WorkflowResult]:
        """Run workflow from JSON file (original CLI functionality)."""
        inputs = self._load_input_from_file(file_path)
        
        # Validate inputs after loading
        if inputs:
            for inp in inputs:
                self._validate_input(inp.context, inp.question)
        
        # Process gene sets sequentially
        results = []
        total_sets = len(inputs)
        
        for i, inp in enumerate(inputs, 1):
            set_name = self._extract_gene_name_from_evidence(inp.evidence, i)
            
            # Update progress for current gene set (if callback available)
            if self.progress_callback:
                self.progress_callback(f"**Processing gene set {i}/{total_sets}: {set_name}**")
            
            result = self.workflow.run_workflow(inp)
            results.append(result)
            
            # Update progress after gene set completion (if callback available)
            if self.progress_callback:
                status_emoji = "✅" if result.final_status.value == "APPROVED" else "⚠️"
                self.progress_callback(f"{status_emoji} **Gene set {i}/{total_sets} ({set_name}) completed** - {result.total_iterations} iteration(s)")
        
        # Final completion message (if callback available)
        if self.progress_callback:
            approved_count = sum(1 for r in results if r.final_status.value == "APPROVED")
            self.progress_callback(f"🎉 **All gene sets completed!** {approved_count}/{total_sets} analyses approved")
        
        return results
    
    def _process_enrichment_data(self, gene_enrichment: dict, community_enrichment: dict) -> str:
        """Process Gene Enrichment and Community Enrichment data into a combined evidence string.
        
        Args:
            gene_enrichment: Dictionary of gene enrichment pathways
            community_enrichment: Dictionary of community enrichment data (community_id -> pathways)
            
        Returns:
            Combined evidence string with all pathways formatted
        """
        evidence_parts = []
        
        # Add header
        evidence_parts.append("Gene Set: Combined Gene Enrichment and Community Enrichment Analysis")
        evidence_parts.append("")  # Empty line for separation
        
        # Process Gene Enrichment data
        if gene_enrichment:
            evidence_parts.append("=== GENE ENRICHMENT PATHWAYS ===")
            evidence_parts.append("")
            
            for pathway_name, pathway_data in gene_enrichment.items():
                if isinstance(pathway_data, dict):
                    evidence_str = self._format_gene_enrichment_item(pathway_name, pathway_data)
                    evidence_parts.append(evidence_str)
                    print(f"DEBUG: Added gene enrichment entry for: {pathway_name}")
                else:
                    evidence_parts.append(f"{pathway_name}: {str(pathway_data)}")
        
        # Process Community Enrichment data
        if community_enrichment:
            evidence_parts.append("")
            evidence_parts.append("=== COMMUNITY ENRICHMENT PATHWAYS ===")
            evidence_parts.append("")
            
            # Iterate through each community (ignore the community ID, just process the pathways)
            for community_id, community_data in community_enrichment.items():
                if isinstance(community_data, dict):
                    print(f"DEBUG: Processing community {community_id} with {len(community_data)} pathways")
                    
                    for pathway_name, pathway_data in community_data.items():
                        if isinstance(pathway_data, dict):
                            evidence_str = self._format_gene_enrichment_item(pathway_name, pathway_data)
                            evidence_parts.append(evidence_str)
                            print(f"DEBUG: Added community enrichment entry for: {pathway_name} (from community {community_id})")
                        else:
                            evidence_parts.append(f"{pathway_name}: {str(pathway_data)}")
        
        # Combine all evidence parts into a single string
        combined_evidence = "\n\n".join(evidence_parts)
        print(f"DEBUG: Combined evidence length: {len(combined_evidence)}")
        print(f"DEBUG: Combined evidence preview: {combined_evidence[:300]}...")
        
        return combined_evidence

    def _convert_app_data_to_inputs(self, output_dict: Dict[str, Any]) -> List[UserInput]:
        """Convert app.py output_dict to UserInput objects for gene enrichment and community enrichment evidence."""
        context = output_dict.get('Context', '')
        question = output_dict.get('Prompt', '')  # Note: 'Prompt' in app, 'Question' in main
        gene_enrichment = output_dict.get('Gene Enrichment', {})
        community_enrichment = output_dict.get('Community Enrichment', {})
        
        print("DEBUG: gene_enrichment keys:", list(gene_enrichment.keys()) if gene_enrichment else "No Gene Enrichment")
        print("DEBUG: gene_enrichment type:", type(gene_enrichment))
        print("DEBUG: community_enrichment keys:", list(community_enrichment.keys()) if community_enrichment else "No Community Enrichment")
        print("DEBUG: community_enrichment type:", type(community_enrichment))
        
        inputs: List[UserInput] = []
        
        # Process enrichment data using the common method
        combined_evidence = self._process_enrichment_data(gene_enrichment, community_enrichment)
        
        # Create UserInput if we have any evidence (more than just header and empty line)
        evidence_parts = combined_evidence.split('\n\n')
        if len(evidence_parts) > 2:  # More than just the header
            print("DEBUG: Creating UserInput with combined gene and community enrichment evidence")
            print(f"DEBUG: Final enrichment evidence string length: {len(combined_evidence)}")
            print(f"DEBUG: Final enrichment evidence string preview: {combined_evidence[:300]}...")
            inputs.append(UserInput(
                context=context,
                question=question,
                evidence=combined_evidence
            ))
        else:
            print("DEBUG: Creating UserInput with no enrichment evidence message")
            no_evidence_text = "Gene Set: Combined Gene Enrichment and Community Enrichment Analysis\n\nNo gene enrichment or community enrichment evidence available"
            print(f"DEBUG: No enrichment evidence text: {no_evidence_text}")
            inputs.append(UserInput(
                context=context,
                question=question,
                evidence=no_evidence_text
            ))
        
        print(f"DEBUG: Total inputs created: {len(inputs)}")
        return inputs
    
    def _format_gene_enrichment_item(self, pathway_name: str, pathway_data: dict) -> str:
        """Format gene enrichment dictionary into the specified string format.
        
        Example input:
        "NADH dehydrogenase (ubiquinone) activity": {
            "description": "Catalysis of the reaction: NADH + ubiquinone + 5 H+(in) = NAD+ + ubiquinol + 4 H+(out). [RHEA:29091]",
            "intersections": "MT-ND2, MT-ND3, MT-ND5, MT-ND4L, MT-ND4, MT-ND1",
            "native": "GO:0008137",
            "source": "GO:MF"
        }
        
        Example output:
        "NADH dehydrogenase (ubiquinone) activity; description: Catalysis of the reaction: NADH + ubiquinone + 5 H+(in) = NAD+ + ubiquinol + 4 H+(out). [RHEA:29091];  intersections: MT-ND2, MT-ND3, MT-ND5, MT-ND4L, MT-ND4, MT-ND1;  [GO:0008137]"
        """
        description = pathway_data.get('description', 'No description available')
        intersections = pathway_data.get('intersections', 'No genes listed')
        native_id = pathway_data.get('native', '')
        source = pathway_data.get('source', '')
        
        # Format according to the specified pattern
        formatted_str = f"{pathway_name}; description: {description}; Genes intersections: {intersections}"
        
        if native_id:
            formatted_str += f"; [{native_id}]"
        
        return formatted_str
    
    def _load_input_from_file(self, file_path: str) -> List[UserInput]:
        """Load sample_input.json with 'Context', 'Question', 'Gene Enrichment', and 'Community Enrichment' mapping."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            context = data.get('Context', '')
            question = data.get('Question', '')
            gene_enrichment = data.get('Gene Enrichment', {})  # dict: pathway_name -> pathway_data dict
            community_enrichment = data.get('Community Enrichment', {})  # dict: community_id -> {pathway_name -> pathway_data}
            
            inputs: List[UserInput] = []
            
            # Process enrichment data using the common method
            combined_evidence = self._process_enrichment_data(gene_enrichment, community_enrichment)
            
            # Create UserInput if we have any evidence (more than just header and empty line)
            evidence_parts = combined_evidence.split('\n\n')
            if len(evidence_parts) > 2:  # More than just the header
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=combined_evidence
                ))
            else:
                no_evidence_text = "Gene Set: Combined Gene Enrichment and Community Enrichment Analysis\n\nNo gene enrichment or community enrichment evidence available"
                inputs.append(UserInput(
                    context=context,
                    question=question,
                    evidence=no_evidence_text
                ))
            
            return inputs
        except Exception as e:
            print(f"Error loading input file: {e}")
            return []
    
    def save_results_to_files(self, results: List[WorkflowResult], 
                            output_path: Optional[str] = None,
                            consolidated_path: Optional[str] = None):
        """Save results to files."""
        if output_path:
            for i, result in enumerate(results, 1):
                # append gene name if available
                gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, i)
                suffix = gene_name if gene_name != f'GeneSet_{i}' else None
                out_path = Path(output_path)
                if suffix:
                    out_path = out_path.with_name(f"{out_path.stem}_{suffix}{out_path.suffix}")
                self._save_output_to_file(result, str(out_path))
        
        # Create consolidated final analysis file
        if consolidated_path:
            self._save_consolidated_final_analysis(results, consolidated_path)
        elif len(results) > 1:
            # Auto-generate consolidated file if multiple gene sets processed
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
                    "total_gene_sets_analyzed": len(results),
                    "context": results[0].user_input.context if results else "",
                    "question": results[0].user_input.question if results else ""
                },
                "gene_set_analyses": {}
            }
            
            # Add each gene set's final analysis
            for result in results:
                gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
                
                consolidated_data["gene_set_analyses"][gene_name] = {
                    "final_analysis": result.final_analysis,
                    "final_status": result.final_status.value,
                    "total_iterations": result.total_iterations,
                    "evidence_length": len(result.user_input.evidence)
                }
            
            # Save to file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
            
            print(f"Consolidated final analysis saved to {file_path}")
            print(f"Analyzed {len(results)} gene sets total")
            
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
                "total_gene_sets_analyzed": len(results),
                "context": results[0].user_input.context if results else "",
                "question": results[0].user_input.question if results else ""
            },
            "gene_set_analyses": {},
            "summary_stats": {
                "total_gene_sets": len(results),
                "approved_analyses": sum(1 for r in results if r.final_status.value == "APPROVED"),
                "average_iterations": sum(r.total_iterations for r in results) / len(results) if results else 0,
                "gene_sets_with_evidence": sum(1 for r in results if r.user_input.evidence and len(r.user_input.evidence.strip()) > 0)  # Non-empty evidence
            }
        }
        
        # Add each gene set's final analysis
        for result in results:
            gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
            
            consolidated_data["gene_set_analyses"][gene_name] = {
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
                "total_gene_sets": len(results),
                "description": "Full prompts sent to LLM agents during AI analysis",
                "note": "Each agent call includes both system prompt and user message. Evidence text is included in all prompts."
            },
            "system_prompts": {
                "orchestrator": "Orchestrator uses pure Python routing logic - no LLM calls",
                "bioexpert": BIOEXPERT_PROMPT,
                "evaluator": EVALUATOR_PROMPT
            },
            "gene_set_prompts": {}
        }
        
        for result in results:
            gene_name = self._extract_gene_name_from_evidence(result.user_input.evidence, results.index(result) + 1)
            # Handle evidence as string
            evidence_text = result.user_input.evidence if result.user_input.evidence else "No evidence provided."
            
            gene_prompts = {
                "gene_set_info": {
                    "gene_set_name": gene_name,
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
            
            # First iteration Gene Enrichment Expert prompt
            first_bioexpert_prompt = f"""
Context: {result.user_input.context}
Question: {result.user_input.question}
Evidence:
{evidence_text}

As the Gene Enrichment Expert Agent, analyze the pathway and biological process evidence and answer the question in a structured format with relevance explanation and summary/conclusion. Cite evidence sources explicitly using database IDs.
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
Please evaluate the following gene enrichment pathway and biological process analysis:

Original Context: {result.user_input.context}
Original Question: {result.user_input.question}

Evidence Provided:
{evidence_text}

Gene Enrichment Expert Analysis (Iteration {bio_output.iteration}):
Relevance Explanation:
{bio_output.relevance_explanation}

Summary/Conclusion:
{summary_block}

Respond exactly with:
- "APPROVED" if the analysis meets quality standards
- Or "NOT APPROVED" followed by specific, actionable feedback
Focus on biological accuracy, clarity, citation of database IDs, and completeness.
"""
                gene_prompts["evaluator_prompts"].append({
                    "iteration": i,
                    "user_message": evaluator_prompt
                })
            
            prompts_data["gene_set_prompts"][gene_name] = gene_prompts
        
        return json.dumps(prompts_data, indent=2, ensure_ascii=False, default=str) 