from pydantic import BaseModel, EmailStr
from typing import Dict, Optional

class EmailContentModel(BaseModel):
    html: str
    subject: Optional[str] = None

class EmailsInputModel(BaseModel):
    emails_input: Dict[EmailStr, EmailContentModel]