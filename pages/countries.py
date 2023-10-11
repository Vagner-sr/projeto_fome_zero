# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# Bibliotecas necessarias
import folium
import pandas as pd
from datetime import datetime
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Countries', layout='wide')

# --------------------------
# Import dataset
# --------------------------
df_raw = pd.read_csv('dataset/fome_zero.csv')
df = df_raw.copy()

# --------------------------
# Funções e limpeza do dataset
# --------------------------

# Adicionando coluna: SIM/NÃO para online booking
def has_online_booking(x):
  if x == 0:
    return "No"
  else:
    return 'Yes'

# Retirando as linhas com Restaurants IDs duplicados
df = df.drop_duplicates(subset='Restaurant ID')

# Retirando as linhas com valores = 0
novas_linhas = df['Aggregate rating'] != 0.0
df = df.loc[novas_linhas,:]

novas_linhas2 = df['Average Cost for two'] != 0.0
df = df.loc[novas_linhas2,:]

# Adicionando coluna com o nome dos paises
countries = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

# Adicionando coluna Country name
def country_name(country_id):
  return countries[country_id]
df['Country name'] = df['Country Code'].apply(lambda x: country_name(x))

# Adicionando coluna com Yes ou No se o restaurante tem online booking
df['Has Table booking Y/N'] = df['Has Table booking'].apply(lambda x: has_online_booking(x))


# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
   return "expensive"
  else:
    return "gourmet"


# Criação do nome das Cores
colors = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
  return COLORS[color_code]


# Renomear as colunas do DataFrame
def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df


# ---------Inicio da Estrutura logica do codigo

# --------------------------
# Barra Lateral
# --------------------------

imagem = Image.open('logo.png')
st.sidebar.image(imagem, width=120)

st.sidebar.markdown('#### A melhor plataforma de avaliação de restaurantes')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')
st.sidebar.markdown('#### Seleciones os países para visualizar os restaurantes')


country_select = st.sidebar.multiselect(
    'Selecione os países', ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'], default = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'United Arab Emirates', 'India'])


# Filtro countries
linhas_selecionadas = df['Country name'].isin(country_select)
df = df.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")

# ========================
# Layout no Streamleat
# ========================

st.markdown('# Countries')

with st.container():
    # Quantidade de restaurantes registrados por país
    st.markdown('#### Quantidade de restastaurantes registrados por país')
    
    df_aux = df.loc[:,['Country name', 'Restaurant ID']].groupby('Country name').nunique().sort_values('Restaurant ID', ascending = False).reset_index()
    df_aux.columns = ['Country name', 'Restaurant Quantity']
    # Gráfico
    fig = px.bar(df_aux, x = 'Country name', y = 'Restaurant Quantity')
    st.plotly_chart(fig, use_container_width = True)

    
with st.container():
    # Quantidade de cidades registradas por país
    st.markdown('#### Quantidade de cidades registradas por país')
    
    cidades_por_pais = df.loc[:, ['City', 'Country name']].groupby('Country name').nunique().sort_values('City', ascending = False).reset_index()
    cidades_por_pais.columns = ['Country name', 'City Quantity']
    # Gráfico
    fig = px.bar(cidades_por_pais, x = 'Country name', y = 'City Quantity')
    st.plotly_chart(fig, use_container_width = True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Média de avaliações feitas por país')
        
        df_aux6 = df.loc[:,['Country name', 'Votes']].groupby('Country name').mean().sort_values('Votes', ascending = False).round(2).reset_index()
        
        #Gráfico
        fig = px.bar(df_aux6, x= 'Country name', y= 'Votes')
        st.plotly_chart(fig, use_container_width = True)

    with col2:
        st.markdown("#### Média de preço de um prato para duas pessoas")

        df_aux9 = ( df.loc[:,['Country name', 'Average Cost for two']]
                   .groupby('Country name').mean().sort_values('Average Cost for two', ascending = False).round(2).reset_index() )
        df_aux9 = px.bar(df_aux9, x = 'Country name', y = 'Average Cost for two')
        st.plotly_chart(df_aux9, use_container_width = True)










