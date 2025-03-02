from fastapi import APIRouter, HTTPException
from src.core.train import train_lgbm_model

router = APIRouter()

@router.post("")
async def train_model():
    """
    Treina o modelo de recomendação e salva o arquivo.
    """
    
    try:
        train_lgbm_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao treinar o modelo: {str(e)}")
    
    return {"message": "Modelo treinado com sucesso."}
