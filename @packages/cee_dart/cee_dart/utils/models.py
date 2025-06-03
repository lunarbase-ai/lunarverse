from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class EvaluationStatus(Enum):
    """Universal evaluation status for all agentic systems."""
    APPROVED = "APPROVED"
    NOT_APPROVED = "NOT_APPROVED" 