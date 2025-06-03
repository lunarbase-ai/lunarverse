"""
Novelty Agents - AI workflow for unified biomedical evidence integration
"""

from .workflow_runner import NoveltyWorkflowRunner
from .models import UserInput, WorkflowResult
from .workflow import create_workflow_engine

# Create alias for compatibility with other agent systems
WorkflowRunner = NoveltyWorkflowRunner

__all__ = ["WorkflowRunner", "NoveltyWorkflowRunner", "UserInput", "WorkflowResult", "create_workflow_engine"] 