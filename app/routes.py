import logging
from fastapi import APIRouter
from app.models import SumRequest

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/sum")
def calculate_sum(request: SumRequest):
    # Log no início da função
    logger.info("Recebido pedido de soma com os valores: %s, %s", request.value1, request.value2)

    # Realiza a soma
    result = request.value1 + request.value2

    # Log do resultado
    logger.info("Resultado da soma: %s", result)

    return {"sum": result}