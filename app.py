import pandas as pd
import os
from gemini_service import extracts_keywords
import time

itens_path = os.path.join("dados", "itens")
csv_files = [f for f in os.listdir(itens_path) if f.endswith(".csv")]

news_data = {}

for csv_file in csv_files:
    file_path = os.path.join(itens_path, csv_file)
    df = pd.read_csv(file_path)

    df["primary_key"] = ""
    df["secondary_key"] = ""

    for index, row in df.head(5000).iterrows():
        body = row["body"] if "body" in df.columns else ""
        
        if body:
            primary_keywords, secondary_keywords = extracts_keywords(body)
            df.at[index, "primary_key"] = ", ".join(primary_keywords)
            df.at[index, "secondary_key"] = ", ".join(secondary_keywords)

            print(f"\nNotícia ID: {row['page']}")
            print(f"Título: {row['title']}")
            print(f"Palavras-chave primárias: {primary_keywords}")
            print(f"Palavras-chave secundárias: {secondary_keywords}")
            
            time.sleep(6) # espera 6 segundos para respeitar o limite de 10 RPM

    df.to_csv(file_path, index=False)
    print(f"Arquivo atualizado: {csv_file}")
            

print("\n Extração concluída!")


# print(f"Total de notícias carregadas: {len(news_data)}") #total de notícias: 255603

# # Salva o dicionário em um arquivo JSON
# output_path = os.path.join("dados", "news_data.json")
# with open(output_path, "w", encoding="utf-8") as json_file:
#     json.dump(news_data, json_file, ensure_ascii=False, indent=4)

# print(f"Arquivo JSON criado em: {output_path}")