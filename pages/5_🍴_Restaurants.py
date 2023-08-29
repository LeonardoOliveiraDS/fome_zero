# ===========================================================
# ||||||||||||||||||||| === LIBRARY === |||||||||||||||||||||
# ===========================================================

import pandas as pd
import inflection
import streamlit as st
import folium
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from PIL import Image
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# :fork_and_knife: - emoji file_nime
st.set_page_config( page_icon='🍴', layout='wide' )

# ===========================================================
# |||||||||||||||||| === FUNCTIONS === ||||||||||||||||||||||
# ===========================================================
# ===============================::
# ================|| Clean Code ||
#                    ----------

def clean_code(dataframe):
    df = dataframe.copy()

    # ===========================::
    # ========|| Rename Columns ||
    #            --------------
    
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    # ===============================::
    # ===|| Create - Col. 'country' ||
    #       -----------------------
    
    COUNTRIES = {
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
    
    def country_name(country_id):
        return COUNTRIES[country_id]
        
    df['country'] = df['country_code'].apply(lambda x: country_name(x))

    # ==================================::
    # ===|| Create - Col. 'price_type' ||
    #       --------------------------
    
    def create_price_type(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
            
    df['price_type'] = df['price_range'].apply(create_price_type)

    # =============================::
    # ===|| Create - Col. 'color' ||
    #       -----------------------
    
    COLORS = {
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
        
    df['color'] = df['rating_color'].apply(lambda x: color_name(x))

    # ========================::
    # ===|| Clean rows 'NaN' ||
    #       ----------------
    
    df.dropna(subset=['cuisines'], inplace=True)
    
    # ==================================::
    # ===|| One cuisine per restaurant ||
    #       --------------------------
    df["cuisines"] = df["cuisines"].apply(lambda x: x.split(",")[0])

    # =====================================::
    # ===|| Drop column with unique value ||
    #       -----------------------------
    
    cols = df.columns
    df = df.loc[:, cols != 'switch_to_order_menu']
    
    # =======================::
    # ===|| Drop duplicates ||
    #       ---------------
    
    df.drop_duplicates(keep='first', inplace=True)
    
    # ==================================::
    # ===|| Create - Col. 'region' ||
    #       ----------------------
    
    REGIONS = {
        'Philippines': ['Asia'],
        'Singapure': ['Asia'],
        'United Arab Emirates': ['Asia'],
        'India': ['Asia'],
        'Indonesia': ['Asia'],
        'Qatar': ['Asia'],
        'Sri Lanka': ['Asia'],
        'Turkey': ['Asia'],
        'Brazil': ['South America'],
        'Australia': ['Oceania'],
        'New Zeland': ['Oceania'],
        'United States of America': ['North America'],
        'Canada': ['North America'],
        'England': ['Europe'],
        'South Africa': ['Africa'] }
        

    def regions_col(country):
        return REGIONS[country]

    df['region'] = df['country'].apply(lambda x: regions_col(x))

    return df
 
# ======================== :::: =============================
# ======================== :::: =============================



# ===========================================================
# |||||| === INICIO DA ESTRUTURA LÓGICA DO CÓDIGO === |||||||
# ===========================================================
# ===============================::
# ============|| Import Dataset ||
#                --------------

df = pd.read_csv( 'dataset/zomato.csv' )

# ==============================::
# ============|| Clean Dataset ||
#                -------------

df1 = clean_code( df )

# ===========================================================
# ||||||||||||||||||||| === SIDEBAR === |||||||||||||||||||||
# ===========================================================

image = Image.open( 'logo.png' )
st.sidebar.image( image, use_column_width=True )

st.header( 'View by restaurant' )

# ==================================== ::

st.sidebar.markdown( """___""" )

# Dicionário de continentes e seus países correspondentes
continent_countries = {
    'Asia': ['Philippines', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'Qatar', 'Sri Lanka', 'Turkey'],
    'South America': ['Brazil'],
    'Oceania': ['Australia', 'New Zeland'],
    'North America': ['United States of America', 'Canada'],
    'Europe': ['England'],
    'Africa': ['South Africa']}

rerun_button = st.sidebar.button('Rerun data')
if rerun_button:
    st.experimental_rerun()

df1 = pd.DataFrame()
df1 = clean_code( df )

# Definir a região 'Asia' como selecionada por padrão
default_selected_continents = ['Asia']

# Sidebar com checkboxes para cada continente
st.sidebar.header('Display by continents:')
selected_continents = []
df1 = pd.DataFrame()
df1 = clean_code( df )

for continent, countries in continent_countries.items():
    checkbox_value = st.sidebar.checkbox(continent, key=continent, value=(continent in default_selected_continents))
    if checkbox_value:
        selected_continents.extend(countries)
        

# Filtrar o DataFrame com base nos países dos continentes selecionados
filtered_df1 = df1[df1['country'].isin(selected_continents)]

# Obter os países presentes em filtered_df1
default_country_options = filtered_df1['country'].unique()

# Sidebar com multiselect para seleção de países
st.sidebar.markdown('## Selected Countries:')
country_options = st.sidebar.multiselect(
    '* Remove country ',
    default_country_options,
    default=default_country_options
)

# Aplicar o filtro de países no DataFrame filtrado pelo primeiro filtro
filtered_df2 = filtered_df1[filtered_df1['country'].isin(country_options)]

# Atualizar o filtro de países no DataFrame filtrado pelo segundo filtro
filtered_df2 = filtered_df2[filtered_df2['country'].isin(country_options)]

df1 = filtered_df2

### ------------------------------------#####

st.sidebar.markdown( """___""" )
# Botão no sidebar para download do DataFrame tratado
if st.sidebar.button("Gerar CSV para do DataFrame Atual"):
    # Criar um DataFrame temporário apenas com as colunas que você deseja exportar
    df_export = df1[['restaurant_id', 'restaurant_name', 'country_code', 'city', 'address',
       'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines',
       'average_cost_for_two', 'currency', 'has_table_booking',
       'has_online_delivery', 'is_delivering_now', 'price_range',
       'aggregate_rating', 'rating_color', 'rating_text', 'votes', 'country',
       'price_type', 'color']]  # Substitua pelas colunas que deseja exportar

    # Converter o DataFrame em um arquivo CSV
    csv_file = df_export.to_csv(index=False)

    # Configurar o link para download
    st.sidebar.download_button(
        label="Download CSV",
        data=csv_file,
        file_name='df_export.csv',
        mime='text/csv'
    )

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by Leonardo Oliveira de Sousa' )

# ===========================================================
# |||||||||||||| === LAYOUT NO STREAMLIT === ||||||||||||||||
# ===========================================================

tab1, tab2 = st.tabs( ['Visão Restaurantes', '-'] )

with tab1:
    with st.container():
        st.subheader('Restaurant more aggregate ratings TOP 50')
        aux = df1.groupby(['country', 'restaurant_name'])['votes'].sum().reset_index()
        aux = aux.sort_values(by='votes', ascending=False)              
        aux = aux.head(50)
        fig = px.bar( aux, x='restaurant_name', y='votes', color='votes',  labels={'restaurant_name':'Restaurant name', 'votes':'Votes', 'country':'Countries'}, height=400)
        st.plotly_chart( fig, use_container_width=True )
        st.markdown( """___""" )

# -------------------------------------------------------

    with st.container():
        st.subheader('Restaurant highest ratings TOP 50')
        aux = df1.groupby('restaurant_name')['aggregate_rating'].mean().reset_index()
        aux = aux.sort_values(by='aggregate_rating', ascending=False)
        aux = aux.head(50)
        fig = px.bar( aux, x='restaurant_name', y='aggregate_rating', labels={'restaurant_name':'Restaurant name', 'aggregate_rating':'Ratings'}, height=500)
        st.plotly_chart( fig, use_container_width=True )
        st.markdown( """___""" )
            
# ------------------------------------------------------------

    with st.container():
        st.subheader('Restaurant highest cost average for two TOP 50')
        tx_cambio = {
    'Botswana Pula(P)': 13.53,
    'Brazilian Real(R$)': 4.90,
    'Dollar($)': 1,
    'Emirati Diram(AED)': 3.67,
    'Indian Rupees(Rs.)': 82.92,
    'Indonesian Rupiah(IDR)': 15214.00,
    'NewZealand($)': 1.64,
    'Pounds(£)': 0.78,
    'Qatari Rial(QR)': 3.64,
    'Rand(R)': 18.98,
    'Sri Lankan Rupee(LKR)': 319.09,
    'Turkish Lira(TL)': 27.01
}

        df_aux = df1.copy()

        df_aux = df_aux.loc[df1['average_cost_for_two'] != 25000017]

        # Aplicar conversão de moeda e calcular média por cidade
        df_aux['average_cost_for_two_usd'] = df_aux.apply(lambda row: row['average_cost_for_two'] / tx_cambio.get(row['currency'], 1), axis=1)
        df_aux['average_cost_for_two_usd'] = df_aux['average_cost_for_two_usd'].round(2)  # Limitar a duas casas decimais
        df_aux.loc[df_aux['currency'] == 'Dollar($)', 'average_cost_for_two_usd'] = df_aux['average_cost_for_two']  # Manter valor se a moeda já for USD
        mean_rest = df_aux.groupby('restaurant_name')['average_cost_for_two_usd'].mean().reset_index()
        
        mean_rest = df_aux.sort_values(by='average_cost_for_two_usd', ascending=False )
        mean_rest = mean_rest.head(50)
        
        fig = px.bar( mean_rest, x='restaurant_name', y='average_cost_for_two_usd',color='average_cost_for_two_usd', labels={'average_cost_for_two_usd':'Cost for two (Dollar)', 'restaurant_name':'Restaurant Name'}, height=500)
        st.plotly_chart( fig, use_container_width=True )

# ------------------------------------------------------------











        