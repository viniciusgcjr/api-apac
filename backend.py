import requests
import json 
import pandas as pd 
import streamlit as st
import datetime


# Formata a string que representa o link que será usado para download das estacoes.
@st.cache
def preparaLink(codigoEstacao, dataInicio, dataFim):
    url = 'https://apitempo.inmet.gov.br/estacao/'
    urlfim = url + "/" + str(dataInicio) + "/" +  str(dataFim) + "/" + codigoEstacao
    return urlfim


# Prepara o arquivo json que foi gerado a partir do download dos dados direto no site do INMET
@st.cache
def dados( link = "https://apitempo.inmet.gov.br/estacoes/T"):
    resp = requests.get(link)
    return json.loads(resp.text)
    
    
#Extrai todos os estados das estações
def retornaestados():
    estados = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'}
    return estados
    

# Retorna uma lista com o codigo de cada estacao referente ao Estado selecionado
def codigosEstacoes(data, estadoEstacao):
    codigos_estacoes =  []
    for dic in range(len(data)):
        if(data[dic]["SG_ESTADO"] == estadoEstacao):
            dict = data[dic]
            codigos_estacoes.append(dict['CD_ESTACAO'])
    return codigos_estacoes


def converte(df):

    for convert in range(len(df.columns)):
        try:
            if(df[df.columns[convert]] != "HR_MEDICAO"):
                pd.to_numeric(df[df.columns[convert]])
        except:
            continue

    df = df.rename(columns={"HR_MEDICAO":"DATETIME"})
    df["DATETIME"] = pd.to_datetime(df["DT_MEDICAO"] + " " + df["DATETIME"])

    return df

        
