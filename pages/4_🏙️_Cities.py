# ===========================================================
# ||||||||||||||||||||| === LIBRARY === |||||||||||||||||||||
# ===========================================================

import pandas as pd
import inflection
import streamlit as st
import folium
import plotly.express as px

from PIL import Image
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config( page_icon='🏙️', layout='wide' )

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

st.header( 'View by cities' )

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

tab1, tab2 = st.tabs( ['Visão Cidades', '-'] )

with tab1:
    with st.container():
        st.title( 'Cities more restaurant in dataset' )
        df_aux = df1.groupby(['city','country'])['restaurant_id'].nunique().reset_index()
        #df_aux = df_aux.columns['rest_city']
        #df_aux = df_aux.loc[df_aux['aggregate_rating'] > 0, :]
        df_aux = df_aux.reset_index()
        df_aux = df_aux.sort_values(by='restaurant_id', ascending=False)
        fig = px.bar( df_aux, x='city', y='restaurant_id', color='country', labels={'restaurant_id':'Restaurants', 'city':'Cities', 'country':'Countries'}, height=400)
        st.plotly_chart( fig, use_container_width=True )

# --------------------------------------------------------

    with st.container():
        col1, col2 = st.columns( 2 )

        with col1:
            st.markdown( """___""" )
            st.subheader('Aggregate rating greater than 4 by cities')
            aux = df1.loc[df1['aggregate_rating'] >= 4, :]
            df_aux = aux.groupby(['city', 'country'])['aggregate_rating'].count().reset_index()
            df_aux = df_aux.sort_values(by='aggregate_rating', ascending=False)
            fig = px.bar(df_aux, x='city', y='aggregate_rating', color='country',  labels={'aggregate_rating':'Ratings', 'city':'Cities', 'country':'Countries'}, height=400)
            st.plotly_chart( fig, use_container_width=True )

        # -----------------------------------------------

        with col2:
            st.markdown( """___""" )
            st.subheader('Aggregate rating less than 2.5 by cities')
            aux = df1.loc[df1['aggregate_rating'] < 2.5, :]
            df_aux = aux.groupby(['city', 'country'])['aggregate_rating'].count().reset_index()
            df_aux = df_aux.sort_values(by='aggregate_rating', ascending=False)
            fig = px.bar(df_aux, x='city', y='aggregate_rating', color='country',  labels={'aggregate_rating':'Ratings', 'city':'Cities', 'country':'Countries'}, height=400)
            st.plotly_chart( fig, use_container_width=True )

# --------------------------------------------------------------

    with st.container():
        st.markdown( """___""" )
        st.subheader('Cuisines distint per cities')
        aux = df1.groupby(['city', 'country'])['cuisines'].nunique().reset_index()
        aux = aux.sort_values(by='cuisines', ascending=False)
        fig = px.bar( aux, x='city', y='cuisines', color='country', labels={'cuisines':'Cuisines', 'city':'Cities', 'country':'Countries'}, height=400)
        st.plotly_chart( fig, use_container_width=True )
        
        
            













