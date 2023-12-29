import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

st.markdown("<h2 style='text-align: center; color:#a7c5bd;'>INSE (Indicador de Nível Socioeconômico)<br>SAEB 2021</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color:#a7c5bd;'>"
                "O Indicador de Nível Socioeconômico (Inse), construído pela Diretoria de Avaliação da Educação "
                "Básica (Daeb), com base nos resultados do questionário do(a) aluno(a) do Saeb (Inse do Saeb), tem como "
                "objetivo contextualizar resultados obtidos em avaliações e exames aplicados por este Instituto no "
                "âmbito da educação básica. Dessa forma, possibilita-se conhecer a realidade social de escolas e redes "
                "de ensino, bem como auxiliar na implementação, no monitoramento e na avaliação de políticas públicas, "
                "visando ao aumento da qualidade e da equidade educacional.<br>"
                "<b>Fonte: </b><a href='https://download.inep.gov.br/areas_de_atuacao/Indicadores_de_nivel_Nota_tenica_2021.pdf'>https://download.inep.gov.br/areas_de_atuacao/Indicadores_de_nivel_Nota_tenica_2021.pdf</a>"
            "</p>", unsafe_allow_html=True)

colunas = ['ID_SAEB', 'ID_REGIAO', 'ID_UF', 
           'ID_AREA', 'ID_ESCOLA', 'IN_PUBLICA', 'ID_LOCALIZACAO',
           'NIVEL_SOCIO_ECONOMICO']


df_saeb = pd.read_csv('dados/TS_ESCOLA.csv', sep=';', encoding='ISO-8859-1', usecols=colunas)

coluna_regiao = {
    1 : 'Norte',
    2 : 'Nordeste',
    3 : 'Sudeste',
    4 : 'Sul',
    5 : 'Centro-Oeste'
}

coluna_estado = {
    11:"RO",
    12:"AC",
    13:"AM",
    14:"RR",
    15:"PA",
    16:"AP",
    17:"TO",
    21:"MA",
    22:"PI",
    23:"CE",
    24:"RN",
    25:"PB",
    26:"PE",
    27:"AL",
    28:"SE",
    29:"BA",
    31:"MG",
    32:"ES",
    33:"RJ",
    35:"SP",
    41:"PR",
    42:"SC",
    43:"RS",
    50:"MS",
    51:"MT",
    52:"GO",
    53:"DF"
}

coluna_area = {
    1 : 'Capital',
    2 : 'Interior',

}

coluna_publica = {
    0 : 'Privada',
    1 : 'Pública'

}

coluna_localizacao = {
    1 : 'Urbana',
    2 : 'Rural'
}

df_saeb['ID_REGIAO'] = df_saeb['ID_REGIAO'].map(coluna_regiao)
df_saeb['ID_UF'] = df_saeb['ID_UF'].map(coluna_estado)
df_saeb['ID_AREA'] = df_saeb['ID_AREA'].map(coluna_area)
df_saeb['IN_PUBLICA'] = df_saeb['IN_PUBLICA'].map(coluna_publica)
df_saeb['ID_LOCALIZACAO'] = df_saeb['ID_LOCALIZACAO'].map(coluna_localizacao)

selecao = df_saeb['NIVEL_SOCIO_ECONOMICO'].notna()
df_saeb = df_saeb[selecao]
df_saeb = df_saeb.sort_values('NIVEL_SOCIO_ECONOMICO')

nivel_socioeconomico = st.sidebar.selectbox('Indicador de Nível Socioeconômico (INSE)', df_saeb['NIVEL_SOCIO_ECONOMICO'].unique())

with st.sidebar:
    st.write('Nível I - Este é o nível inferior da escala, no qual os estudantes têm dois ou mais desvios-padrão abaixo da média nacional do Inse.')
    st.write('Nível II - Neste nível, os estudantes estão entre um e dois desvios-padrão abaixo da média nacional do Inse.')
    st.write('Nível III - Neste nível, os estudantes estão entre meio e um desvio-padrão abaixo da média nacional do Inse.')
    st.write('Nível IV - Neste nível, os estudantes estão até meio desvio-padrão abaixo da média nacional do Inse.')
    st.write('Nível V - Neste nível, os estudantes estão até meio desvio-padrão acima da média nacional do Inse.')
    st.write('Nível VI - Neste nível, os estudantes estão de meio a um desvio-padrão acima da média nacional do Inse.')
    st.write('Nível VII - Neste nível, os estudantes estão de um a dois desvios-padrão acima da média nacional do Inse.')
        
df_filtrado = df_saeb[df_saeb['NIVEL_SOCIO_ECONOMICO'] == nivel_socioeconomico]

col1, col2 = st.columns(2)

df_regiao = df_filtrado.groupby('ID_REGIAO')[['ID_REGIAO']].value_counts().reset_index().sort_values('count', ascending=False)
fig_regiao = px.bar(df_regiao, x='ID_REGIAO', 
                    y='count', title='INSE por Região',
                    labels={'count':'quantidade de escolas', 'ID_REGIAO':'região'}, 
                    color_discrete_sequence=px.colors.qualitative.T10)
#col1.plotly_chart(fig_regiao, use_container_width=True)
fig_regiao.update_layout(title_x=0.5)
fig_regiao

df_uf = df_filtrado.groupby('ID_UF')[['ID_UF']].value_counts().reset_index().sort_values('count', ascending=False)
fig_uf = px.bar(df_uf, x='ID_UF', 
                    y='count', title='INSE por UF',
                    labels={'count':'quantidade de escolas', 'ID_UF':'estado'}, 
                    color_discrete_sequence=px.colors.qualitative.Set2)
#col1.plotly_chart(fig_regiao, use_container_width=True)
fig_uf.update_layout(title_x=0.5)
fig_uf