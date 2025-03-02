# Recomendação de notícias

## Índice

- [Recomendação de notícias](#recomendação-de-notícias)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Pré-requisitos](#pré-requisitos)
  - [Configuração do Ambiente](#configuração-do-ambiente)
    - [Instalação do Docker](#instalação-do-docker)
    - [Instalação do Python](#instalação-do-python)
    - [Instruções para Construção e Execução](#instruções-para-construção-e-execução)
      - [Construir a Imagem Docker](#construir-a-imagem-docker)
    - [Executar o Contêiner Docker](#executar-o-contêiner-docker)
  - [Uso da API](#uso-da-api)
    - [API de Predição (predict)](#api-de-predição-predict)
      - [Endpoint - Predict](#endpoint---predict)
      - [Descrição - Predict](#descrição---predict)
      - [Exemplo de Requisição - Predict](#exemplo-de-requisição---predict)
      - [Exemplo de Resposta - Predict](#exemplo-de-resposta---predict)

## Visão Geral

Bem-vindo à documentação da API de Recomendação de notícias, desenvolvida como parte de um desafio tecnológico da faculdade FIAP. Esta solução utiliza o algorítmo LightGBM para prever as notícias mais relevantes para um determinado usuário.

## Pré-requisitos

- **Python 3.10 ou superior**: O projeto utiliza funcionalidades compatíveis com esta versão.
- **Docker**: Para construção e execução de contêineres.

## Configuração do Ambiente

### Instalação do Docker

Para instalar o Docker, siga as instruções do [site oficial do Docker](https://www.docker.com/products/docker-desktop).

### Instalação do Python

Recomenda-se o uso do `pyenv` para gerenciar versões de Python. Instale o `pyenv` e configure a versão correta do Python:

```bash
pyenv install 3.10.2
pyenv local 3.10.2
```

### Instruções para Construção e Execução

#### Construir a Imagem Docker

Navegue até o diretório raiz do projeto (onde o Dockerfile está localizado) e execute:

```bash
docker build -t sistema-recomendacao:latest .
```

### Executar o Contêiner Docker

Para iniciar o contêiner e expor a API:

```bash
docker run -p 8000:8000 sistema-recomendacao:latest
```

A API estará acessível em `http://localhost:8000`.

## Uso da API

### API de Predição (predict)

#### Endpoint - Predict

`POST /predict`

#### Descrição - Predict

 A API `predict` é projetada para utilizar o modelo LightGBM previamente treinado com dados da interação entre usuarios e noticias para realizar recomendações de notícias.

#### Exemplo de Requisição - Predict

```bash
curl --request POST \
  --url 'http://localhost:8000/predict' \
  --data '{
  "userId": "ff0e8ea01cca9c2abef4b4d582ac7bca5ebb63e861508f2fef3f47048328ad47"
}'
```

#### Exemplo de Resposta - Predict

```json
{
  "recommendedNews": [
    "7161674b-b8ce-45ba-85da-2fc997b83b73",
    "c31f681b-7a9d-4199-a68c-7a1e3b51d160"
    "..."
    ]
}
```
