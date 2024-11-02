import pandas as pd
import streamlit as st
import plotly.express as px


from unidecode import unidecode

st.set_page_config(layout="wide", page_title="Estatísticas Mobiliários")

st.title("Estatísticas Mobiliários")

data_default = "COPIA_MAPAS_GERAIS.xlsx"

data_input_value = st.file_uploader(label="Escolher arquivo atualizado")

#Tentar fazer funcionar a importacao de uma base de dados mais atualizada

if not data_input_value:
    df = pd.read_excel("COPIA_MAPAS_GERAIS.xlsx")
else:
    df = pd.read_excel(data_input_value, sheet_name="MAPAS GERAIS 2024 (OFICIAL)")


df["MUNÍCIPIO"] = df['MUNÍCIPIO'].str.upper().apply(unidecode)

df['ESCOLA'] = df['ESCOLA'].str.upper().apply(unidecode)

df['ESCOLA'] = df['ESCOLA'].str.upper().apply(unidecode)

df["DATA"] = pd.to_datetime(df["DATA"])

df = df.sort_values(by="DATA")


sre_options = df['SUPERINTENDENCIA'].str.upper().unique()
city_options = df['MUNÍCIPIO'].str.upper().unique()
school_options = df['ESCOLA'].apply(unidecode).unique()
items = df['OBJETO'].unique()

service_forms = ['TODOS', 'RM', 'MAPA']

df['MESES'] = df['DATA'].apply(lambda x: "0"+str(x.month) + "/" + str(x.year))

filtered_df = df



# Add a selectbox to the sidebar:
st.sidebar.header("Filtros")

city_select = st.sidebar.selectbox("Município", ["TODOS"] + list(city_options))

sre_select = st.sidebar.selectbox("SRE",["TODAS"] + list(sre_options) )

school_select = st.sidebar.selectbox('Escolas', ['TODAS'] + list(school_options))

items_select = st.sidebar.selectbox('Itens', ['TODOS'] + list(items) )

service_form_select = st.sidebar.selectbox('Forma de atendimento',service_forms)

month_select = st.sidebar.selectbox("Mês", ['TODO PERÍODO'] + df['MESES'].unique().tolist())

if(service_form_select == "RM"):
    filtered_df = df[df['FORMA DE ATENDIMENTO'].str.contains('RM', case=False, na=False)]
elif(service_form_select == 'MAPA'):
    filtered_df = df[df['FORMA DE ATENDIMENTO'].str.contains('MAPA', case=False, na=False)]

if city_select != "TODOS":
    filtered_df = filtered_df[filtered_df['MUNÍCIPIO'] == city_select]

if sre_select != 'TODAS':
    filtered_df = filtered_df[filtered_df['SUPERINTENDENCIA'] == sre_select]

if school_select != 'TODAS':
    filtered_df = filtered_df[filtered_df['ESCOLA'] == school_select]

if items_select != 'TODOS':
    filtered_df = filtered_df[filtered_df['OBJETO']== items_select]
if month_select != 'TODO PERÍODO':
    filtered_df = filtered_df[filtered_df['MESES'] == month_select]

filtered_df

#Agrupa por objetos
grouped_df = filtered_df.groupby('OBJETO')["QUANT."].sum().reset_index(name='TOTAL DE ITENS')
grouped_df = grouped_df.sort_values(by="TOTAL DE ITENS", ascending=False)

top_10_items = grouped_df.head(10)

total_items = grouped_df["TOTAL DE ITENS"].sum()

#Agrupa as escolas e soma as quantidades de itens
grouped_for_school = filtered_df.groupby("ESCOLA")["QUANT."].sum().reset_index()

grouped_for_school["QUANT."] = pd.to_numeric(grouped_for_school["QUANT."], errors='coerce')

total_attend_schools = grouped_for_school["ESCOLA"].nunique()




#Organiza de forma decrescente
grouped_for_school_ranking = grouped_for_school.sort_values(by="QUANT.", ascending=False)

top_10 = grouped_for_school_ranking.head(10)

fig_ranking_school = px.bar(top_10, x="ESCOLA", y="QUANT.",  title=f"Top 10 escolas mais atendidas (Total de de escolas antendidas: {total_attend_schools})", height=500,)

fig_ranking_items = px.bar(top_10_items, x="OBJETO", y="TOTAL DE ITENS", title=f"Total de Itens entregues: {total_items}")

#plota os gráficos
st.plotly_chart(fig_ranking_school, use_container_width=True)
st.plotly_chart(fig_ranking_items, use_container_width=True)













