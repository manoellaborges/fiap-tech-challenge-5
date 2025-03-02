import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.functions import load_user_data, convert_history_to_list


output_dir = os.path.join(os.path.dirname(__file__), '../../processed_data')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def criar_features_usuario(usuarios_df):
    # userType (usuário logado ou anônimo)
    usuarios_df['userType'] = usuarios_df['userType'].apply(lambda x: 1 if x == 'logado' else 0)

    # timeOnPageHistory (tempo médio na página)
    usuarios_df['timeOnPageHistory_mean'] = usuarios_df['timeOnPageHistory'].apply(
        lambda x: np.mean([float(i) for i in x.split(',')]) if isinstance(x, str) and len(x) > 0 else 0
    )

    # scrollPercentageHistory (percentual médio de rolagem)
    usuarios_df['scrollPercentageHistory_mean'] = usuarios_df['scrollPercentageHistory'].apply(
        lambda x: np.mean([float(i) for i in x.split(',')]) if isinstance(x, str) and len(x) > 0 else 0
    )

    # pageVisitsCountHistory (número médio de visitas por página)
    usuarios_df['pageVisitsCountHistory_mean'] = usuarios_df['pageVisitsCountHistory'].apply(
        lambda x: np.mean([int(i) for i in x.split(',')]) if isinstance(x, str) and len(x) > 0 else 0
    )

    return usuarios_df

def associar_noticias_categorias(usuarios_df, noticias_df):
    # Criar um dicionário que mapeia o ID da notícia para sua categoria
    noticia_para_categoria = noticias_df.set_index('page')['palavras_chave'].to_dict()

    # Função para obter as categorias das notícias no histórico do usuário
    def obter_categorias_do_historico(historico):
        if isinstance(historico, str) and len(historico) > 0:
            ids_noticias = [i for i in historico.split(',')]
            categorias = [noticia_para_categoria.get(id_noticia, '') for id_noticia in ids_noticias]
            return categorias
        return []

    # Aplicar a função para obter as categorias do histórico de cada usuário
    usuarios_df['categorias_historico'] = usuarios_df['history'].apply(obter_categorias_do_historico)

    return usuarios_df

def calcular_categorias_preferidas(usuarios_df):
    # Função para calcular a frequência de cada categoria
    def calcular_frequencia_categorias(categorias):
        print(type(categorias))
        if isinstance(categorias, list):
            freq = {}
            for categoria in categorias:
                if categoria:
                    freq[categoria] = freq.get(categoria, 0) + 1
            return freq
        return {}

    # Calcular a frequência de cada categoria para cada usuário
    usuarios_df['frequencia_categorias'] = usuarios_df['categorias_historico'].apply(calcular_frequencia_categorias)

    # Identificar a categoria mais frequente
    usuarios_df['categoria_preferida'] = usuarios_df['frequencia_categorias'].apply(
        lambda x: max(x, key=x.get, default='') if isinstance(x, dict) and len(x) > 0 else ''
    )

    return usuarios_df


df_user = pd.read_csv('processed_data/users.csv')
df_noticias = pd.read_csv('processed_data/itens.csv')

df_user = criar_features_usuario(df_user)

# df_user = associar_noticias_categorias(df_user, df_noticias)
df_user['categorias_historico'] = df_user['categorias_historico'].apply(lambda x: x.replace('[', '').replace(']', '').replace('"', ''))
df_user['categorias_historico'] = df_user['categorias_historico'].apply(lambda x: list(eval(x)) if isinstance(x, str) else x)

# Aplicar a função para calcular as categorias preferidas
usuarios_df = calcular_categorias_preferidas(df_user)
df_user.to_csv(f'{output_dir}/users.csv', index=False)

df_user = df_user.fillna('')
df_user = df_user.drop_duplicates()

df_user.to_csv(f'{output_dir}/users.csv', index=False)
print("Script de pré-processamento concluído com sucesso!")
