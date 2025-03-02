import re

import spacy
import os
import sys
from textblob import TextBlob
import pandas as pd

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

def extract_info_from_url(url):
    parts = url.split('/')

    if len(parts) > 4:
        return [parts[3], parts[4]]
    elif len(parts) > 3:
        return [parts[3]]
    
    return None
    
output_dir = os.path.join(os.path.dirname(__file__), '../../processed_data')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for df_item in load_item_data():
    df_item = df_item.fillna('')
    df_item = df_item.drop_duplicates()
    df_item['title'] = df_item['title'].apply(limpar_texto)
    df_item['body'] = df_item['body'].apply(limpar_texto)
    df_item['caption'] = df_item['caption'].apply(limpar_texto)
    df_item['sentimento_titulo'] = df_item['title'].apply(analisar_sentimento)
    df_item['sentimento_corpo'] = df_item['body'].apply(analisar_sentimento)
    df_item['palavras_chave'] = ''

    for index, row in df_item.iterrows():
        resultado = taggiar_noticia(row['title'], row['body'], row['caption'])
        df_item.at[index, 'palavras_chave'] = resultado['tags']


df_item['palavras_chave'] = df_item['palavras_chave'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df_item['palavras_chave']+= df_item['url'].apply(extract_info_from_url)
df_item['issued'] = pd.to_datetime(df_item['issued'], errors='coerce').dt.tz_localize(None)
df_item['recencia'] = (pd.Timestamp('now') - df_item['issued']).dt.days

df_item.to_csv(f'{output_dir}/itens.csv', index=False)
print("Script de pré-processamento concluído com sucesso!")
