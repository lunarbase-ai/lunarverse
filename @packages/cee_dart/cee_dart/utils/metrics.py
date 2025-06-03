from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TokenUsage(BaseModel):
    """Token usage tracking for LLM calls."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class AgentExecution(BaseModel):
    """Execution details for an agent."""
    agent_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    
    @property
    def execution_time_seconds(self) -> float:
        """Calculate execution time in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

class WorkflowMetrics(BaseModel):
    """Comprehensive workflow execution metrics."""
    total_execution_time_seconds: float = 0.0
    total_tokens_used: TokenUsage = Field(default_factory=TokenUsage)
    agent_executions: List[AgentExecution] = Field(default_factory=list)
    
    def add_agent_execution(self, execution: AgentExecution):
        """Add an agent execution and update totals."""
        self.agent_executions.append(execution)
        if execution.end_time:
            self.total_execution_time_seconds += execution.execution_time_seconds
        self.total_tokens_used.prompt_tokens += execution.token_usage.prompt_tokens
        self.total_tokens_used.completion_tokens += execution.token_usage.completion_tokens
        self.total_tokens_used.total_tokens += execution.token_usage.total_tokens 