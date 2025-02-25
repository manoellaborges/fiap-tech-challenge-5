import re

import spacy
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import os
import sys
import unicodedata
from textblob import TextBlob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.functions import load_item_data


def analisar_sentimento(texto):
    if isinstance(texto, str):
        analysis = TextBlob(texto)
        return analysis.sentiment.polarity  # Retorna a polaridade
    else:
        return 0
    
def gerar_tags(texto):
    """Gera tags dinamicamente a partir das entidades nomeadas."""
    doc = nlp(texto)
    tags = set()

    for ent in doc.ents:
        tags.add(ent.text)
    
    return list(tags)[:20]

def taggiar_noticia(titulo, caption, texto):
    """Catalogar uma notícia, sugerindo categorias e gerando tags."""
    tags_geradas = gerar_tags(titulo + " " + caption + " " +  texto)

    return {
        "tags": tags_geradas
    }


try:
    nlp = spacy.load("pt_core_news_md")
    print("Modelo 'pt_core_news_sm' carregado com sucesso!")
except OSError as e:
    print(f"Erro ao carregar o modelo: {e}")

    
def limpar_texto(texto):
    if isinstance(texto, str):
        conectores = r'\\b(também|mas|porém|portanto|logo|se|quando|em|de|para)\\b'

        texto = texto.lower()
        texto = re.sub(r'<[^>]+>', '', texto)
        texto = re.sub(r'[^a-zA-Z0-9\sàáâãéèêíìîóòõôúùûç]', '', texto)
        texto = re.sub(conectores, '', texto, flags=re.IGNORECASE)
        
        texto.replace(' e ', '')
        texto.replace(' a ', '')
        texto.replace(' o ', '')
        return texto
    else:
        return None
    
output_dir = os.path.join(os.path.dirname(__file__), '../../processed_data')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

i = 0
for df_item in load_item_data():
    print('inicio')
    print(len(df_item))
    # df_item = df_item.fillna('')
    # df_item = df_item.drop_duplicates()
    # df_item['title'] = df_item['title'].apply(limpar_texto)
    # df_item['body'] = df_item['body'].apply(limpar_texto)
    # df_item['caption'] = df_item['caption'].apply(limpar_texto)
    # df_item['sentimento_titulo'] = df_item['title'].apply(analisar_sentimento)
    # df_item['sentimento_corpo'] = df_item['body'].apply(analisar_sentimento)
    # df_item['palavras_chave'] = ''

    # for index, row in df_item.iterrows():
    #     resultado = taggiar_noticia(row['title'], row['body'], row['caption'])
    #     df_item.at[index, 'palavras_chave'] = resultado['tags']

    # df_item.to_csv(f'{output_dir}/item_data{i}.csv', index=False)
    i+=0
