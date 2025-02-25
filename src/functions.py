import ast
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import scipy.sparse as sp
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

import pandas as pd

# nltk.download('stopwords')
# from nltk.corpus import stopwords


def load_item_data():
    pasta_itens = 'data/itens/itens'
    arquivos_itens = [os.path.join(pasta_itens, f) for f in os.listdir(pasta_itens) if f.endswith('.csv')]
    itens_data_0 = pd.read_csv(arquivos_itens[0])
    itens_data_1 = pd.read_csv(arquivos_itens[1])
    itens_data_2 = pd.read_csv(arquivos_itens[2])
    
    return [itens_data_0]


def load_user_data():
    pasta_treino = 'data/files/treino'
    arquivos_treino = [os.path.join(pasta_treino, f) for f in os.listdir(pasta_treino) if f.endswith('.csv')]
    training_data = pd.concat((pd.read_csv(f) for f in arquivos_treino), ignore_index=True)
    
    return training_data


def convert_history_to_list(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return x.split(',')
    return x


def preprocess_item_data(itens_data):
    itens_data['extracted_url'] = itens_data['url'].apply(lambda x: x.split('/', 1)[1] if '/' in x else x)
    print(itens_data['extracted_url'])


# training_data, itens_data = load_data()
# preprocess_item_data(itens_data)


def preprocess_data(training_data, itens_data):
    training_data['history'] = training_data['history'].apply(convert_history_to_list)
    training_data = training_data.explode('history')
    
    training_data = training_data.merge(itens_data, left_on='history', right_on='page', how='left')
    
    for col in ['issued', 'modified']:
        itens_data[col] = pd.to_datetime(itens_data[col], errors='coerce').dt.tz_localize(None)
        
    itens_data['news_age'] = (datetime.now() - itens_data['issued']).dt.days
    itens_data['modification_frequency'] = (itens_data['modified'] - itens_data['issued']).dt.days

    training_data['timestampHistory'] = pd.to_numeric(
        training_data['timestampHistory'].astype(str).str.extract(r'(\d+)')[0],
        errors='coerce'
    )
    
    training_data['timestampHistory'] = pd.to_datetime(training_data['timestampHistory'], unit='ms')
    
    num_cols = ['timeOnPageHistory', 'numberOfClicksHistory', 'scrollPercentageHistory', 'pageVisitsCountHistory']
    training_data[num_cols] = training_data[num_cols].apply(pd.to_numeric, errors='coerce')
    
    training_data['total_news_read'] = training_data.groupby('userId')['history'].transform('count')
    training_data['mean_time_on_page'] = training_data.groupby('userId')['timeOnPageHistory'].transform('mean')
    training_data['var_time_on_page'] = training_data.groupby('userId')['timeOnPageHistory'].transform('var')
    training_data['recency'] = (datetime.now() - training_data['timestampHistory']).dt.days
    
    itens_data['issued'] = pd.to_datetime(itens_data['issued']).dt.tz_localize(None)
    itens_data['modified'] = pd.to_datetime(itens_data['modified']).dt.tz_localize(None)

    itens_data['news_age'] = (datetime.now() - itens_data['issued']).dt.days
    itens_data['modification_frequency'] = (itens_data['modified'] - itens_data['issued']).dt.days

    # stop_words = list(stopwords.words('portuguese'))
    
    # tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    # tfidf_matrix = tfidf_vectorizer.fit_transform(itens_data['body'].fillna(''))
    
    # user_feature_cols = ['total_news_read', 'mean_time_on_page', 'var_time_on_page', 'recency']
    # user_features = training_data[['userId'] + user_feature_cols].drop_duplicates()
    
    # tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    # tfidf_matrix = tfidf_vectorizer.fit_transform(itens_data['body'].fillna(''))
    
    feature_cols = ['news_age', 'modification_frequency']
    itens_data_features = itens_data[feature_cols].fillna(0)
    scaler = MinMaxScaler()
    itens_data_features_scaled = scaler.fit_transform(itens_data_features)
    
    scaler_user = MinMaxScaler()
    # user_features_scaled = scaler_user.fit_transform(user_features[user_feature_cols])
    
    encoder = OneHotEncoder(handle_unknown='ignore')
    # categorias_encoded = encoder.fit_transform(itens_data[['category']])
    
    # tfidf_plus_features_users = sp.hstack((tfidf_matrix, itens_data_features_scaled, categorias_encoded))

    # similaridade_completa = cosine_similarity(tfidf_plus_features_users)
    
    return training_data, itens_data
    
# extract_data()
