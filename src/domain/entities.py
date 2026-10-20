from enum import Enum
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"

class SecretToken(BaseModel):
    raw_value: str
    entropy_score: float
    secret_type: str

class Vulnerability(BaseModel):
    file_path: str
    line_number: int
    severity: Severity = Field(default=Severity.HIGH)
    token: SecretToken
    context_snippet: str
