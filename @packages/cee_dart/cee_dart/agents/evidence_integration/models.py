from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from cee_dart.utils.metrics import TokenUsage, AgentExecution, WorkflowMetrics
from cee_dart.utils.models import EvaluationStatus

class UserInput(BaseModel):
    """User input for the unified biomedical evidence interpretation workflow."""
    context: str  # Study context, background information
    question: str  # User's specific question
    evidence: str = ""  # Combined evidence string from civic, pharmGKB, and gene enrichment analyses
    
    class Config:
        # Allow loading from JSON with field names (Pydantic V2)
        populate_by_name = True

class ConsolidatedEvidence(BaseModel):
    """Consolidated evidence from all three analysis systems."""
    civic_evidence: str = ""
    pharmgkb_evidence: str = ""
    gene_enrichment_evidence: str = ""
    combined_evidence: str = ""
    total_genes_civic: int = 0
    total_genes_pharmgkb: int = 0
    total_gene_sets_enrichment: int = 0

class ReportComposerOutput(BaseModel):
    """Structured output from the Report Composer agent."""
    potential_novel_biomarkers: str = Field(
        description="Analysis of potential novel biomarkers identified from the evidence"
    )
    implications: str = Field(
        description="Clinical and biological implications of the findings"
    )
    well_known_interactions: str = Field(
        description="Summary of well-established interactions and mechanisms"
    )
    conclusions: str = Field(
        description="Overall conclusions and recommendations"
    )
    iteration: int = 1

class EvaluatorOutput(BaseModel):
    """Structured output from the Evaluator agent."""
    status: EvaluationStatus
    feedback_points: List[str] = Field(
        default_factory=list,
        description="Specific feedback items for structural integrity and content quality"
    )

class CriticOutput(BaseModel):
    """Structured output from the Critic agent."""
    status: EvaluationStatus
    feedback_points: List[str] = Field(
        default_factory=list,
        description="Critical analysis feedback including bias identification and alternative interpretations"
    )

class DeliberationOutput(BaseModel):
    """Structured output from the Deliberation & Counterfactual Reasoner agent."""
    status: EvaluationStatus
    feedback_points: List[str] = Field(
        default_factory=list,
        description="Counterfactual reasoning and what-if scenario feedback"
    )

class FeedbackCollection(BaseModel):
    """Collection of feedback from all reviewing agents."""
    evaluator_feedback: EvaluatorOutput
    critic_feedback: CriticOutput
    deliberation_feedback: DeliberationOutput
    
    @property
    def all_approved(self) -> bool:
        """Check if all feedback agents have approved."""
        return (self.evaluator_feedback.status == EvaluationStatus.APPROVED and
                self.critic_feedback.status == EvaluationStatus.APPROVED and
                self.deliberation_feedback.status == EvaluationStatus.APPROVED)
    
    @property
    def combined_feedback(self) -> str:
        """Combine all feedback into a single string."""
        feedback_sections = []
        
        if self.evaluator_feedback.feedback_points:
            feedback_sections.append("CONTENT VALIDATOR FEEDBACK:\n" + 
                                    "\n".join(f"- {point}" for point in self.evaluator_feedback.feedback_points))
        
        if self.critic_feedback.feedback_points:
            feedback_sections.append("CRITICAL REVIEWER FEEDBACK:\n" + 
                                    "\n".join(f"- {point}" for point in self.critic_feedback.feedback_points))
        
        if self.deliberation_feedback.feedback_points:
            feedback_sections.append("RELEVANCE VALIDATOR FEEDBACK:\n" + 
                                    "\n".join(f"- {point}" for point in self.deliberation_feedback.feedback_points))
        
        return "\n\n".join(feedback_sections)

class UnifiedReport(BaseModel):
    """Final unified report structure."""
    potential_novel_biomarkers: str
    implications: str
    well_known_interactions: str
    conclusions: str
    
    def to_formatted_string(self) -> str:
        """Convert to formatted string representation with proper bullet point formatting."""
        sections = []
        
        if self.potential_novel_biomarkers:
            # Ensure proper bullet point formatting
            formatted_biomarkers = self._format_bullet_points(self.potential_novel_biomarkers)
            sections.append(f"## Potential Novel Biomarkers\n{formatted_biomarkers}")
        
        if self.implications:
            formatted_implications = self._format_bullet_points(self.implications)
            sections.append(f"## Implications\n{formatted_implications}")
        
        if self.well_known_interactions:
            formatted_interactions = self._format_bullet_points(self.well_known_interactions)
            sections.append(f"## Well-Known Interactions\n{formatted_interactions}")
        
        if self.conclusions:
            formatted_conclusions = self._format_bullet_points(self.conclusions)
            sections.append(f"## Conclusions\n{formatted_conclusions}")
        
        return "\n\n".join(sections)
    
    def _format_bullet_points(self, text: str) -> str:
        """Ensure text is properly formatted with bullet points."""
        if not text:
            return ""
        
        # Split by newlines and ensure each line starts with a bullet point
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Add bullet point if not already present
                if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                    line = f"• {line}"
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)

class WorkflowResult(BaseModel):
    """Final result of the evidence integration workflow."""
    unified_report: UnifiedReport
    total_iterations: int
    feedback_history: List[FeedbackCollection] = Field(
        default_factory=list,
        description="History of all feedback collections from each iteration"
    )
    report_composer_history: List[ReportComposerOutput] = Field(
        default_factory=list,
        description="History of all Report Composer outputs from each iteration"
    )
    final_status: EvaluationStatus
    user_input: UserInput
    consolidated_evidence: ConsolidatedEvidence
    metrics: WorkflowMetrics = Field(default_factory=WorkflowMetrics)
    
    @property
    def final_report_string(self) -> str:
        """Get the final report as a formatted string."""
        return self.unified_report.to_formatted_string()
