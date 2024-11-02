import pandas as pd
import streamlit as st
import plotly.express as px


from unidecode import unidecode

st.set_page_config(layout="wide", page_title="Estatísticas Mobiliários")

st.title("Estatísticas Mobiliários")


data = st.file_uploader(label="Escolher arquivo")

df = pd.read_excel("COPIA_MAPAS_GERAIS.xlsx")

df["MUNÍCIPIO"] = df['MUNÍCIPIO'].str.upper().apply(unidecode)

df['ESCOLA'] = df['ESCOLA'].str.upper().apply(unidecode)

df['ESCOLA'] = df['ESCOLA'].str.upper().apply(unidecode)

df["DATA"] = pd.to_datetime(df["DATA"])

df = df.sort_values(by="DATA")

# df

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
total_items = grouped_df["TOTAL DE ITENS"].sum()

#Agrupa as escolas e soma as quantidades de itens
grouped_for_school = filtered_df.groupby("ESCOLA")["QUANT."].sum().reset_index()
total_attend_schools = grouped_for_school["ESCOLA"].nunique()



#Organiza de forma decrescente
grouped_for_school_ranking = grouped_for_school.sort_values(by="QUANT.", ascending=False)

fig_ranking_school = px.bar(grouped_for_school_ranking, x="ESCOLA", y="QUANT.",  title=f"Ranking das escolas (Total de escolas atendidas: {total_attend_schools})")

st.plotly_chart(fig_ranking_school, use_container_width=True)

fig_object = px.bar(grouped_df, x="OBJETO", y="TOTAL DE ITENS", title=f"Total de Itens entregues: {total_items}")

col2, col3 = st.columns([1,1])

col2.plotly_chart(fig_object)





#Pensar melhor como vai ser os filtros.












