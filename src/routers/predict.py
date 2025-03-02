import os
import sys
from fastapi import APIRouter, HTTPException
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel
import lightgbm as lgb


router = APIRouter()

# Carregar o modelo LightGBM
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
model_path = 'models/lgbm_model.txt'
lgbm = lgb.Booster(model_file=model_path)

# Carregar os LabelEncoders
encoders = joblib.load('models/encoders.joblib')

# Carregar a lista de noticias
df_noticias = pd.read_csv('processed_data/itens.csv') # Supondo que você tenha um arquivo com as noticias


class UserRequest(BaseModel):
    userId: str

@router.post("")
def predict(user_request: UserRequest):
    try:
        try:
            user_id_encoded = encoders['userId'].transform([user_request.userId])[0]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"UserId desconhecido: {user_request.userId}")

        df_recommend = pd.DataFrame({
            'userId': [user_id_encoded] * len(df_noticias),
            'noticiaId': encoders['noticiaId'].transform(df_noticias['page'].tolist())
        })
        
        # Fazer a previsão usando predict
        raw_predictions = lgbm.predict(df_recommend, raw_score=True, predict_disable_shape_check=True)

        # Calcular as probabilidades usando a função sigmóide
        probabilities = 1 / (1 + np.exp(-raw_predictions))

        # probabilities = lgbm.predict_proba(df_recommend)[:, 1]
        df_recommend['probability'] = probabilities
        df_recommend = df_recommend.sort_values('probability', ascending=False)
        recommended_news = encoders['noticiaId'].inverse_transform(df_recommend['noticiaId'].tolist())

        recommended_news = recommended_news[:10]

        # Limitar a lista de noticias recomendadas para as 10 primeiras
        recommended_news = recommended_news[:10]

        return {'recommendedNews': recommended_news.tolist()}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Chave ausente: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    