from pydantic import BaseModel
from typing import Optional


class OperationRequest(BaseModel):
    type: str
    x: int
    y: Optional[int] = 0


class OperationResponse(BaseModel):
    result: int
