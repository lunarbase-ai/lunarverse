from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import json
from datetime import datetime
from openai import AzureOpenAI
from cee_dart.agents.evidence_integration.config import Config
from cee_dart.agents.evidence_integration.models import (UserInput, ReportComposerOutput, EvaluatorOutput, CriticOutput, 
                    DeliberationOutput, EvaluationStatus, WorkflowResult, 
                    ConsolidatedEvidence, FeedbackCollection, UnifiedReport, WorkflowMetrics)
from cee_dart.agents.evidence_integration.agents import (OrchestratorAgent, ReportComposerAgent, ContentValidatorAgent, 
                    CriticalReviewerAgent, RelevanceValidatorAgent)

class WorkflowEngine:
    """Main workflow engine that orchestrates the evidence integration process with 5 agents."""
    
    def __init__(self, console: Optional[Console] = None, progress_callback=None, client: AzureOpenAI = None):
        self.console = console or Console()
        self.progress_callback = progress_callback
        self.orchestrator = OrchestratorAgent(client)
        self.report_composer = ReportComposerAgent(client)
        self.content_validator = ContentValidatorAgent(client)
        self.critical_reviewer = CriticalReviewerAgent(client)
        self.relevance_validator = RelevanceValidatorAgent(client)
    
    def _update_progress(self, message: str):
        """Update progress via callback if available."""
        if self.progress_callback:
            self.progress_callback(message)
            # Small delay to make progress visible
            time.sleep(0.5)

    def run_workflow_from_dict(self, civic_consolidated: Dict[str, Any], pharmgkb_consolidated: Dict[str, Any], gene_enrichment_consolidated: Dict[str, Any], context: str, question: str) -> WorkflowResult:
        """
        Run the complete evidence integration workflow from consolidated analysis dictionaries.
        
        Args:
            civic_consolidated: Consolidated CIVIC analysis dictionary  
            pharm_consolidated: Consolidated PharmGKB analysis dictionary
            gene_enrichment_consolidated: Consolidated Gene Enrichment analysis dictionary
            context: Study context and background information
            question: User's specific research question
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
        """
        consolidated_evidence = self.orchestrator.extract_evidence_from_dict(
            civic_consolidated, pharmgkb_consolidated, gene_enrichment_consolidated
        )
        
        user_input = UserInput(
            context=context,
            question=question,
            evidence=consolidated_evidence.combined_evidence
        )
        
        return self.run_workflow(user_input, consolidated_evidence)
    
    
    def run_workflow_from_files(self, civic_file: str, pharmgkb_file: str, 
                               gene_enrichment_file: str, context: str, question: str) -> WorkflowResult:
        """
        Run the complete evidence integration workflow from consolidated analysis files.
        
        Args:
            civic_file: Path to CIVIC analysis consolidated JSON file
            pharmgkb_file: Path to PharmGKB analysis consolidated JSON file  
            gene_enrichment_file: Path to Gene Enrichment analysis consolidated JSON file
            context: Study context and background information
            question: User's specific research question
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
        """
        title = "Starting Evidence Integration Workflow - Evidence Integration"
        self.console.print(Panel.fit(title, style="bold blue"))
        self._update_progress("**Extracting evidence** from analysis files...")
        
        # Extract and consolidate evidence from all three systems
        consolidated_evidence = self.orchestrator.extract_evidence_from_files(
            civic_file, pharmgkb_file, gene_enrichment_file
        )
        
        # Create user input with consolidated evidence
        user_input = UserInput(
            context=context,
            question=question,
            evidence=consolidated_evidence.combined_evidence
        )
        
        return self.run_workflow(user_input, consolidated_evidence, False)
    
    def run_workflow(self, user_input: UserInput, consolidated_evidence: ConsolidatedEvidence, save_to_json: bool = True) -> WorkflowResult:
        """
        Run the complete evidence integration workflow.
        
        Args:
            user_input: User's input containing context, question, and evidence
            consolidated_evidence: Consolidated evidence from all three analysis systems
            
        Returns:
            WorkflowResult: Final unified report with analysis and workflow metadata
        """
        self._update_progress("**Starting unified report generation** from integrated evidence...")
        
        # Initialize workflow tracking
        feedback_history: List[FeedbackCollection] = []
        report_composer_history: List[ReportComposerOutput] = []
        current_report_output: Optional[ReportComposerOutput] = None
        iteration = 1
        workflow_metrics = WorkflowMetrics()
        workflow_start_time = datetime.now()
        
        # Orchestrator starts the workflow
        orchestrator_status = self.orchestrator.coordinate_workflow(consolidated_evidence)
        self.console.print(f"Orchestrator: {orchestrator_status}\n")
        
        # Main workflow loop
        while iteration <= Config.MAX_ITERATIONS:
            self.console.print(f"**Iteration {iteration}**")
            
            # Update progress for current iteration
            self._update_progress(f"**Evidence Integration System** - Iteration **{iteration}**: Report Composer creating unified report...")
            
            # Report Composer Phase
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task("Evidence Integration Report Composer creating unified report...", total=None)
                
                # Start tracking Report Composer execution
                report_composer_execution = self.report_composer.start_execution()
                
                if iteration == 1:
                    # First report composition
                    current_report_output = self.report_composer.compose_report(
                        user_input, consolidated_evidence, iteration=iteration
                    )
                else:
                    # Revision based on feedback
                    previous_feedback = feedback_history[-1]
                    combined_feedback = previous_feedback.combined_feedback
                    current_report_output = self.report_composer.compose_report(
                        user_input,
                        consolidated_evidence,
                        previous_output=current_report_output,
                        combined_feedback=combined_feedback,
                        iteration=iteration
                    )
                
                # End tracking Report Composer execution
                report_composer_execution = self.report_composer.end_execution()
                workflow_metrics.add_agent_execution(report_composer_execution)
                
                progress.update(task, description="Evidence Integration Report Composer analysis complete")
                time.sleep(0.5)  # Brief pause for visual effect
            
            # Update progress for evaluation phase
            self._update_progress(f"**Evidence Integration System** - Iteration **{iteration}**: Report complete, gathering feedback from all agents...")
            
            # Display Report Composer output
            self._display_report_output(current_report_output, iteration)
            
            # Add to history
            report_composer_history.append(current_report_output)
            
            # Parallel Feedback Phase - Get feedback from all three agents
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True
            ) as progress:
                eval_task = progress.add_task("Content Validator reviewing report...", total=None)
                
                # Content Validator feedback
                evaluator_execution = self.content_validator.start_execution()
                evaluator_feedback = self.content_validator.evaluate(
                    user_input, current_report_output, consolidated_evidence
                )
                evaluator_execution = self.content_validator.end_execution()
                workflow_metrics.add_agent_execution(evaluator_execution)
                progress.update(eval_task, description="Content Validator review complete")
                
                critic_task = progress.add_task("Critical Reviewer analyzing report...", total=None)
                
                # Critical Reviewer feedback
                critic_execution = self.critical_reviewer.start_execution()
                critic_feedback = self.critical_reviewer.critique(
                    user_input, current_report_output, consolidated_evidence
                )
                critic_execution = self.critical_reviewer.end_execution()
                workflow_metrics.add_agent_execution(critic_execution)
                progress.update(critic_task, description="Critical Reviewer analysis complete")
                
                delib_task = progress.add_task("Relevance Validator reasoning...", total=None)
                
                # Relevance Validator feedback
                deliberation_execution = self.relevance_validator.start_execution()
                deliberation_feedback = self.relevance_validator.deliberate(
                    user_input, current_report_output, consolidated_evidence
                )
                deliberation_execution = self.relevance_validator.end_execution()
                workflow_metrics.add_agent_execution(deliberation_execution)
                progress.update(delib_task, description="Relevance Validator reasoning complete")
            
            # Collect all feedback
            feedback_collection = FeedbackCollection(
                evaluator_feedback=evaluator_feedback,
                critic_feedback=critic_feedback,
                deliberation_feedback=deliberation_feedback
            )
            feedback_history.append(feedback_collection)
            
            # Display feedback from all agents
            self._display_feedback_collection(feedback_collection, iteration)
            
            # Update progress with detailed feedback status
            evaluator_status = feedback_collection.evaluator_feedback.status.value
            critic_status = feedback_collection.critic_feedback.status.value
            deliberation_status = feedback_collection.deliberation_feedback.status.value
            
            feedback_summary = f"Content Validator: {evaluator_status}, Critical Reviewer: {critic_status}, Relevance Validator: {deliberation_status}"
            
            # Check if all agents approved
            if feedback_collection.all_approved:
                self._update_progress(f"**Evidence Integration System** - Iteration **{iteration}**: All agents APPROVED the report! ({feedback_summary})")
                break
            else:
                self._update_progress(f"**Evidence Integration System** - Iteration **{iteration}**: Feedback received ({feedback_summary}), preparing iteration {iteration + 1}...")
            
            # Prepare next iteration
            iteration += 1
        
        # Final completion message
        self._update_progress(f"**Evidence Integration System** - Analysis completed after **{iteration}** iteration(s)")
        
        # Create final unified report
        unified_report = UnifiedReport(
            potential_novel_biomarkers=current_report_output.potential_novel_biomarkers,
            implications=current_report_output.implications,
            well_known_interactions=current_report_output.well_known_interactions,
            conclusions=current_report_output.conclusions
        )
        
        # Calculate total workflow time
        workflow_end_time = datetime.now()
        workflow_metrics.total_execution_time_seconds = (workflow_end_time - workflow_start_time).total_seconds()
        
        # Create final result
        result = WorkflowResult(
            unified_report=unified_report,
            total_iterations=iteration,
            feedback_history=feedback_history,
            report_composer_history=report_composer_history,
            final_status=feedback_history[-1].evaluator_feedback.status,  # Use evaluator status as final
            user_input=user_input,
            consolidated_evidence=consolidated_evidence,
            metrics=workflow_metrics
        )

        if save_to_json:
            self._save_result_to_json(result)        
            self._display_final_summary(result)
        return result

    def _save_result_to_json(self, result: WorkflowResult):
        """Save the workflow result to a JSON file."""
        def default_serializer(obj):
            # Handle enums and objects with __dict__
            if hasattr(obj, "value"):
                return obj.value
            elif hasattr(obj, "__dict__"):
                return obj.__dict__
            elif isinstance(obj, set):
                return list(obj)
            return str(obj)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"novelty_analysis_consolidated_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=default_serializer, ensure_ascii=False)
            self.console.print(f"Results saved to: {filename}")
        except Exception as e:
            self.console.print(f"Warning: Could not save results to JSON: {e}")

    def _display_report_output(self, output: ReportComposerOutput, iteration: int):
        """Display the Report Composer output in a formatted way."""
        self.console.print(Panel.fit(
            f"Report Composer Output - Iteration {iteration}",
            style="bold green"
        ))
        
        sections = [
            ("Potential Novel Biomarkers", output.potential_novel_biomarkers),
            ("Implications", output.implications),
            ("Well-Known Interactions", output.well_known_interactions),
            ("Conclusions", output.conclusions)
        ]
        
        for section_name, content in sections:
            if content:
                self.console.print(f"\n**{section_name}:**")
                # Format bullet points for better display
                display_content = content[:500] + "..." if len(content) > 500 else content
                # Ensure bullet points are properly displayed
                if '•' in display_content or '\n' in display_content:
                    lines = display_content.split('\n')
                    for line in lines[:3]:  # Show first 3 bullet points
                        if line.strip():
                            self.console.print(f"  {line.strip()}")
                    if len(lines) > 3:
                        self.console.print(f"  [dim]... and {len(lines)-3} more points[/dim]")
                else:
                    self.console.print(display_content)
            else:
                self.console.print(f"\n**{section_name}:** [dim]No content provided[/dim]")

    def _display_feedback_collection(self, feedback: FeedbackCollection, iteration: int):
        """Display feedback from all agents in a formatted way."""
        self.console.print(Panel.fit(
            f"Agent Feedback Collection - Iteration {iteration}",
            style="bold yellow"
        ))
        
        # Content Validator feedback
        status_color = "green" if feedback.evaluator_feedback.status == EvaluationStatus.APPROVED else "red"
        self.console.print(f"\n**Content Validator:** [{status_color}]{feedback.evaluator_feedback.status.value}[/{status_color}]")
        if feedback.evaluator_feedback.feedback_points:
            for point in feedback.evaluator_feedback.feedback_points[:3]:  # Show first 3 points
                self.console.print(f"  • {point}")
        
        # Critical Reviewer feedback
        status_color = "green" if feedback.critic_feedback.status == EvaluationStatus.APPROVED else "red"
        self.console.print(f"\n**Critical Reviewer:** [{status_color}]{feedback.critic_feedback.status.value}[/{status_color}]")
        if feedback.critic_feedback.feedback_points:
            for point in feedback.critic_feedback.feedback_points[:3]:  # Show first 3 points
                self.console.print(f"  • {point}")
        
        # Relevance Validator feedback
        status_color = "green" if feedback.deliberation_feedback.status == EvaluationStatus.APPROVED else "red"
        self.console.print(f"\n**Relevance Validator:** [{status_color}]{feedback.deliberation_feedback.status.value}[/{status_color}]")
        if feedback.deliberation_feedback.feedback_points:
            for point in feedback.deliberation_feedback.feedback_points[:3]:  # Show first 3 points
                self.console.print(f"  • {point}")

    def _display_final_summary(self, result: WorkflowResult):
        """Display the final workflow summary."""
        self.console.print(Panel.fit(
            "Evidence Integration Workflow Complete",
            style="bold blue"
        ))
        
        self.console.print(f"**Total Iterations:** {result.total_iterations}")
        self.console.print(f"**Final Status:** {result.final_status.value}")
        self.console.print(f"**Evidence Sources:**")
        self.console.print(f"  • CIVIC genes: {result.consolidated_evidence.total_genes_civic}")
        self.console.print(f"  • PharmGKB genes: {result.consolidated_evidence.total_genes_pharmgkb}")
        self.console.print(f"  • Gene sets: {result.consolidated_evidence.total_gene_sets_enrichment}")
        
        # Show final report sections
        self.console.print(f"\n**Final Unified Report Sections:**")
        report = result.unified_report
        sections = [
            ("Potential Novel Biomarkers", len(report.potential_novel_biomarkers)),
            ("Implications", len(report.implications)),
            ("Well-Known Interactions", len(report.well_known_interactions)),
            ("Conclusions", len(report.conclusions))
        ]
        
        for section_name, length in sections:
            status = "✓" if length > 0 else "✗"
            self.console.print(f"  {status} {section_name}: {length} characters")

def create_workflow_engine(progress_callback=None) -> WorkflowEngine:
    """Create a new workflow engine instance."""
    return WorkflowEngine(progress_callback=progress_callback)
