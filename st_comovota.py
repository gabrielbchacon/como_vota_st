from get_data import get_data

import json
import pandas as pd

import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st


#Data Load and preparation
file = './data/deputado_None'
data = None
with open(file, 'r') as f:
    data = json.load(f)

lista_deputados = []
for deputado in data['dados']:
    lista_deputados.append(deputado['nome'])


add_sidebar = st.sidebar.selectbox('Visualização',('Deputado','Partido'))

if add_sidebar == 'Deputado':
    deputado_escolhido = st.sidebar.selectbox('Escolha um deputado',(lista_deputados))
    relatorio = st.sidebar.radio("Escolha em relatório", ('Despesas', 'Participações'))


    agg_filtered = next(item for item in data['dados'] if item["nome"] == deputado_escolhido)
    deputado_escolhido_id = agg_filtered['id']
    st.header(agg_filtered['nome'])

    col1, col2 = st.columns(2)

    with col1:
        foto = agg_filtered['urlFoto']
        st.image(foto, width= 160)
    
    with col2:
        partido = agg_filtered['siglaPartido']
        deputado_por = agg_filtered['siglaUf']
        email = agg_filtered['email']

        st.write(f'Partido: {partido}')
        st.write(f'Deputado por: {deputado_por}')
        st.write(f'E-mail: {email}')
    
    if relatorio == 'Despesas':
        #Data Preparation
        ## Carregando Despesas do Deputado
        despesas_arquivo = f'./data/despesas/despesas_{deputado_escolhido_id}'
        despesas_deputado = None
        with open(despesas_arquivo, 'r') as f:
            despesas_deputado = json.load(f)
        despesas_df = pd.DataFrame(despesas_deputado)

        ##Carregando Despesas Totais
        despesas_totais_arquivo = f'./data/despesas/despesas_totais'
        despesas_deputados_totais = None
        with open(despesas_totais_arquivo, 'r') as f:
            despesas_deputados_totais = json.load(f)
        despesas_totais_df = pd.DataFrame(despesas_deputados_totais)

        media_despesas = round(despesas_totais_df['total_despesas'].mean(), 2)


        total_despesas = round(despesas_df['valorLiquido'].sum(),2)
        total_vs_media = (round(total_despesas / media_despesas,2) *100) -100
        media_despesas = round(despesas_df['valorLiquido'].mean(),2)
        maior_despesa_nome = despesas_df.iloc[despesas_df['valorLiquido'].idxmax(axis=0)].nomeFornecedor
        maior_despesa_valor = despesas_df.iloc[despesas_df['valorLiquido'].idxmax(axis=0)].valorLiquido

        a = despesas_df.groupby(['tipoDespesa', 'nomeFornecedor'])[['valorLiquido']].sum().reset_index()
        fig = px.treemap(a, path=['tipoDespesa', 'nomeFornecedor'],values='valorLiquido', width=800, height=400)
        fig.update_layout(
            margin = dict(t=50, l=25, r=25, b=25))

        #Data to print
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Valor total de Despesas', f'R$ {total_despesas:,}', delta=f'{total_vs_media} % vs média da casa', delta_color='off')
            st.metric(f'Maior Despesa:\n{maior_despesa_nome}', f'R$ {maior_despesa_valor:,}')
        with col2:
            st.metric('Valor médio de Despesas', f'R$ {media_despesas:,}')

        st.plotly_chart(fig, use_container_width=True)
        st.subheader('Tabela de despesas do parlamentar:')
        st.dataframe(despesas_df)
    else:
        st.write('Participações')
# %%
