import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error


def train_lgbm_model():
    df_interacoes = pd.read_csv('processed_data/interacoes.csv')
    
    # Criar um LabelEncoder para cada coluna categórica
    encoders = {}
    for col in ['userId', 'noticiaId', 'categoria']:
        encoders[col] = LabelEncoder()
        df_interacoes[col] = encoders[col].fit_transform(df_interacoes[col])

    # Preparar os dados para o LightGBM
    X = df_interacoes.drop('interacted', axis=1)
    y = df_interacoes['interacted']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Criar o modelo LightGBM
    lgbm = lgb.LGBMClassifier(
        objective='binary',
        metric='binary_logloss',
        n_estimators=100,  
        num_leaves=31,      
        learning_rate=0.04, 
        n_jobs=-1,          
        random_state=42
    )

    # Treinar o modelo com early stopping
    lgbm.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)]
    )

    # Avaliar o modelo
    print(f"Acurácia: {lgbm.score(X_test, y_test)}")

    # Calcular MAE
    y_pred = lgbm.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE: {mae}")

    # Salvar o modelo treinado
    model_path = 'models/lgbm_model.txt'
    lgbm.booster_.save_model(model_path)
    print(f"Modelo salvo em: {model_path}")
    