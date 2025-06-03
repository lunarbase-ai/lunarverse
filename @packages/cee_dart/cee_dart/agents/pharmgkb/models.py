from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from cee_dart.utils.metrics import TokenUsage, AgentExecution, WorkflowMetrics
from cee_dart.utils.models import EvaluationStatus

class UserInput(BaseModel):
    """User input for the biomedical evidence interpretation workflow."""
    context: str  # Study context, background information
    question: str  # User's specific question
    evidence: str = ""  # Combined biomedical evidence string for the gene
    
    class Config:
        # Allow loading from JSON with field names
        allow_population_by_field_name = True

class BioExpertOutput(BaseModel):
    """Structured output from the BioExpert agent."""
    relevance_explanation: str
    summary_conclusion: List[str] = Field(
        default_factory=list,
        description="Bullet-point conclusions, each no longer than 3 sentences"
    )
    #citations: List[str]
    #confidence_score: Optional[float] = None
    iteration: int = 1

class EvaluatorOutput(BaseModel):
    """Structured output from the Evaluator agent."""
    status: EvaluationStatus
    feedback_points: List[str] = Field(
        default_factory=list,
        description="Numbered or bullet list of specific feedback items"
    )

class WorkflowResult(BaseModel):
    """Final result of the workflow."""
    final_analysis: str  # Merged BioExpert output as single string
    total_iterations: int
    evaluation_history: List[EvaluatorOutput]
    bioexpert_history: List[BioExpertOutput] = Field(
        default_factory=list,
        description="History of all BioExpert outputs from each iteration"
    )
    final_status: EvaluationStatus
    user_input: UserInput
    metrics: WorkflowMetrics = Field(default_factory=WorkflowMetrics)
