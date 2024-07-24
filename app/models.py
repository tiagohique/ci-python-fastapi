from pydantic import BaseModel

class SumRequest(BaseModel):
    value1: float
    value2: float
