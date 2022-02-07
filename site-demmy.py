#coding: utf-8
# Desenvolvimento do site .... 
# Demmily Falcão Fernandes


import backend as bk
import requests
import json 
import pandas as pd 
import os
import glob
import streamlit as st
import matplotlib.pyplot as plt
import calmap
import calplot
import numpy as np

data = bk.dados()
states = bk.retornaestados()


st.title("Dados estações - INMET")
#st.markdown("Projeto de estágio")


estadoEstacao = st.sidebar.selectbox(
    "Selecione o estado da estação desejada:",
    (states.keys())
)
#estadoEstacao = st.sidebar.text_input("Estado da estação - Exemplo: PB:", "").upper()
dataInicio = st.sidebar.date_input("data inicial")
dataFim = st.sidebar.date_input("data final")
variavel = st.sidebar.selectbox("Selecione a variável desejada:", ['Temperatura e Umidade', 'Precipitação'])
formRes=st.sidebar.button("SUBMIT")


def acionaSite(estadoEstacao):
    codigosEstacoes = bk.codigosEstacoes(data, estadoEstacao)
    for i in range(len(codigosEstacoes)):
        link = bk.preparaLink(codigosEstacoes[i], dataInicio, dataFim)
        dados = requests.get(link)
        dat = json.loads(dados.text)
        df = pd.json_normalize(dat)
        df = bk.converte(df)

        Dfmax = df[['DC_NOME','DT_MEDICAO', 'TEM_MAX', 'UMD_MAX']].groupby('DT_MEDICAO').max()
        Dfmin = df[['DT_MEDICAO', 'TEM_MIN', 'UMD_MIN']].groupby('DT_MEDICAO').min()
        dfsite = pd.merge(Dfmax, Dfmin, on=['DT_MEDICAO'])

        Acumchuva = df[['DT_MEDICAO','DATETIME','DC_NOME','CHUVA']]
        tabela = Acumchuva.set_index(["DATETIME"])
        acumdia = tabela['CHUVA'].astype('float').resample('d').sum()
        chuvasite = pd.merge(tabela['DC_NOME'], acumdia, on=['DATETIME'])
      
      
        #ax = chuvasite.plot.bar(x='DC_NOME', y='CHUVA',rot=0)

        chuva = pd.Series(tabela['CHUVA'])
        #plt.figure(figsize=(16,8))
        #calmap.yearplot(data=chuva, year=2014)
        #plt.suptitle('teste', y=.65, fontsize=20)

        if(variavel =='Temperatura e Umidade'):
            st.dataframe(dfsite)
        else:
            st.write(tabela['DC_NOME'][0])
            st.bar_chart(data=acumdia)
            #st.pyplot(ax)
            #st.dataframe(chuvasite)
            #st.dataframe(acumdia)
            #calplot.calplot(chuva, cmap='Reds', figsize=(16,8))
            #plt.suptitle('Calendar Heatmap', y=1.0, fontsize=20)
            

if formRes: acionaSite(estadoEstacao)