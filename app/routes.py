from fastapi import APIRouter
from app.models import SumRequest

router = APIRouter()

@router.post("/sum")
def calculate_sum(request: SumRequest):
    result = request.value1 + request.value2
    return {"sum": result}
