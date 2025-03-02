import pandas as pd


def interacted_with_news(usuario, noticia):
    return noticia in usuario['history']

df_user = pd.read_csv('processed_data/users.csv')
df_noticias = pd.read_csv('processed_data/itens.csv')

data = []

# Combinar os dados de usuários e notícias
for _, usuario in df_user.iterrows():
    # Garante que 'history' e 'numberOfClicksHistory' sejam listas
    history = usuario['history'] if isinstance(usuario['history'], list) else []
    number_of_clicks_history = usuario['numberOfClicksHistory'] if isinstance(usuario['numberOfClicksHistory'], list) else []
    time_on_page_history = usuario['timeOnPageHistory'] if isinstance(usuario['timeOnPageHistory'], list) else []

    # Criar um dicionário que mapeia cada notícia no histórico para o número de cliques correspondente
    cliques_por_noticia = dict(zip(history, number_of_clicks_history))
    tempo_na_pagina_por_noticia = dict(zip(history, time_on_page_history))

    for _, noticia in df_noticias.iterrows():  # Iterar sobre as notícias
        noticia_id = noticia['page']  #pagina é o id da noticia
        interacted = interacted_with_news(usuario, noticia_id)

        # Obter o número de cliques para esta notícia, se estiver no histórico do usuário
        cliques = cliques_por_noticia.get(noticia_id, 0)  # Retorna 0 se a notícia não estiver no histórico
        tempo_na_pagina = tempo_na_pagina_por_noticia.get(noticia_id, 0)  # Retorna 0 se a notícia não estiver no histórico

        data.append({
            'userId': usuario['userId'],
            'noticiaId': noticia_id,
            'interacted': 1 if interacted else 0,
            'userType': usuario['userType'],
            'historySize': usuario['historySize'],
            'recencia': noticia['recencia'],
            'categoria': noticia['palavras_chave'],
            'clicou': cliques,
            'tempo_na_pagina': tempo_na_pagina
        })

df = pd.DataFrame(data)

df.to_csv('interacoes.csv', index=False)
print('Arquivo salvo com sucesso!')
