from pydantic import BaseModel

class BugReport(BaseModel):
    id: str
    bug_line: int
    explanation: str
