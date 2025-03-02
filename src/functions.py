import os
import pandas as pd


def load_item_data() -> list:
    """
    Loads item data from CSV files located in the 'data/itens/itens' directory.
    This function reads three CSV files from the specified directory and returns their contents as a list of pandas DataFrames.
    Returns:
        list: A list containing three pandas DataFrames, each representing the data from one of the CSV files.
    """
    pasta_itens = 'data/itens/itens'
    arquivos_itens = [os.path.join(pasta_itens, f) for f in os.listdir(pasta_itens) if f.endswith('.csv')]
    itens_data_0 = pd.read_csv(arquivos_itens[0])
    itens_data_1 = pd.read_csv(arquivos_itens[1])
    itens_data_2 = pd.read_csv(arquivos_itens[2])
    
    return [itens_data_0, itens_data_1, itens_data_2]


def load_user_data() -> pd.DataFrame:
    """
    Loads user data from CSV files located in the 'data/files/treino' directory.
    This function reads all CSV files in the specified directory, concatenates them into a single
    pandas DataFrame, and returns the combined data.
    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from all CSV files in the directory.
    """
    pasta_treino = 'data/files/treino'
    arquivos_user = [os.path.join(pasta_treino, f) for f in os.listdir(pasta_treino) if f.endswith('.csv')]
    user_data = pd.concat((pd.read_csv(f) for f in arquivos_user), ignore_index=True)
    
    return user_data
