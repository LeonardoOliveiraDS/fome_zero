import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded')
# layout='wide' faz usar todo o espaço do monitor



#image_path = '/Users/leona/Documents/repos/jupyterlab/'
#image = Image.open( 'logo.PNG' )
#st.sidebar.image( image, width=120 )
          
embed_component = {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                  <div class="badge-base LI-profile-badge" data-locale="pt_BR" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="leonardooliveirads" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/leonardooliveirads?trk=profile-badge"></a></div>
              """}

with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)


st.write( '## Análise de Dados em Python - Projeto Final' )

st.markdown( """___""" )

st.write( "# KPIs Dashboard: Fome Zero" )
st.markdown(
    """
    KPIs Dashboard foi construído para identificar pontos chaves da empresa e acompanhar as métricas dos Restaurantes da plataforma, contribuindo para insigths para o crescimento da empresa.
    
    ### Problema de Negócio:
    A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
    """)

st.markdown( """___""" )
# use_column_width ("auto", "always", "never", or bool)
with st.container():
    image = Image.open( 'recorte_maior_4.png' )
    st.image( image, use_column_width=True )

st.markdown( """___""" )
st.sidebar.markdown( '### Powered by Leonardo Oliveira de Sousa' )

#

st.markdown(
"""
### I. Premissas do Projeto:
    1. Os dados foram obtidos da plataforma Kaggle (https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv).
    2. A limpeza no código inclui a exclusão de linhas duplicadas e com dados faltantes, juntamente com a adicição de colunas com dados tratados para facilitar a manipulação.
    3. Foi feita uma conversão de valores das moedas registradas para o Dollar($), criando uma nova coluna para tratar todos restaurantes nos mesmos parâmetros em relação a sua moeda.
    4. Os KPIs foram agrupados em quatro perspectivas de negócio: Países, Cidades, Restaurantes e Culinárias.
    5. Restaurantes não avaliados ou sem registro de preço foram mantidos na base. 
    
### II. Estrutura do Dashboard:

#### Filtros Sidebar:
    - Botão "Rerun Data":
        a.recarrega a pagina selecionando o default 'Asia', continente com maior densidade de dados do Dataset.

    - Filtro 1 "Display by continents:
        a. Permite a seleção dos paises do dataset selecionando-os por continentes
        b. Os paises contidos nos continentes são exibidos no Filtro 2.

    - Filtro 2 "Selected Countries":
        a. Exibi os paises dos continentes selecionados.
        b. É possivel excluir um pais especifico da analise excluindo ele.

#### Overall Metrics:   
    - Perguntas a serem respondidas:
      a. Quantos restaurantes únicos estão registrados?
      b. Quantos países únicos estão registrados?
      c. Quantas cidades únicas estão registradas?
      d. Qual o total de avaliações feitas?
      e. Qual o total de tipos de culinária registrados?
      
    - Mapa que exibe a localização geográfica dos restaurantes.
      - Cluster usado para agrupar os restaurantes conforme o zoom é aplicado ou retirado
      - A cor do marcador do restaurante reflete a avaliação dele, sendo:
          - Darkgreen:  4.5, 4.6, 4.7, 4.8, 4.9
          - Green:      4.0, 4.1, 4.2, 4.3, 4.4
          - Ligthgreen: 3.5, 3.6, 3.7, 3.8, 3.9
          - Orange:     3.0, 3.1, 3.2, 3.3, 3.4
          - Red:        2.5, 2.6, 2.7, 2.8, 2.9
          - Darkred:    0.0, 2.1, 2.2, 2.3, 2.4
    
    
#### Visão por Países:
    - Perguntas a serem respondidas:
      a. Quantidade de cidades cadastradas por País.
      b. Quantidade de restaurantes cadastrados por País.
      c. Média da maior nota média registrada por País.
      d. País com maior quantidade de avaliações feitas. 
      e. Média da quantidade de avaliações cadastradas por País.
      f. País com maior quantidade de restaurantes que fazem entrega.

    
#### Visão por Cidades:
    - Perguntas a serem respondidas:
      a. Cidade com mais restaurantes registrados.
      b. Cidade com mais restaurantes com nota média acima de 4.
      c. Cidade com mais restaurantes com nota média abaixo de 2.5.
      d. Cidade com mais tipos de culinária distintos.
    
#### Visão por Restaurantes:
    - Perguntas a serem respondidas:
      a. Restaurante com maior quantidade de votos.
      b. Restaurante com a maior nota média.
      c. Restaurante com o maior valor de um prato para dois.
    
#### Visão por Tipos de Culinária:
    - Perguntas a serem respondidas:
      a. Culinarias presentes em mais Países.
      b. Culinaria com maior nota média.
      c. Culinaria com maior valor médio de prato para dois.
      d. Culinarias com mais restaurantes que aceitam pedidos online e fazem entrega.
      e. Culinarias com mais restaurantes que fazem reserva de mesa

### O produto final do projeto
	Painel online, hospedando em Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
	O painel pode ser acessado através desse link: https://portfolio-dashboard-kpi-fomezero.streamlit.app/

### Conclusão
	O bjetivo desse projeto foi criar um conjunto de gráficos e/ou tabelas que exibam as métricas da melhor forma possível para o CEO, permitindo a vizualização das KPIs .

### Atualizações futuras:
    - Manter continentes selecionados no chekbox do Filtro 1 após mudar de pagina, simplificando a intereação para o usuario;
    - Reduzir número de métricas
    - Adicionar novas visões de negócio
    """
    )

st.markdown( """___""" )

st.markdown( 
    """
### Ask for Help
- LinkedIn:  https://www.linkedin.com/in/leonardooliveirads/ 
- Email:     leonardooliveiradesousa@outlook.com.br
    """)
