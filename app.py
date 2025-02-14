import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuração do Streamlit
st.set_page_config(page_title="Análise do Preço do Petróleo", layout="wide")

# 🔹 Criando o Menu na Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Navegação",  # Nome do menu
        options=["Introdução", "Análise Exploratória", "Dados Históricos", "Modelo Preditivo"],  # Páginas
        icons=["book", "graph-up", "clock-history", "cpu"],  # Ícones
        menu_icon="cast",
        default_index=0
    )

# 🔹 PÁGINA 1: Introdução
if selected == "Introdução":
    st.title("Bem-vindo à Análise do Preço do Petróleo")
    st.write(
        """
        Este dashboard interativo permite explorar a evolução do preço do petróleo Brent ao longo do tempo, 
        analisar padrões históricos e realizar previsões futuras com modelos de Machine Learning.
        """
    )
    st.subheader("📌 Funcionalidades do Dashboard:")
    st.markdown("""
    - **Análise Exploratória**: Visualização de preços médios, máximos e mínimos ao longo dos anos.
    - **Dados Históricos**: Identificação de eventos históricos e crises que afetaram o preço do petróleo.
    - **Modelo Preditivo**: Forecasting do preço do petróleo utilizando algoritmos de Machine Learning.
    """)

# 🔹 PÁGINA 2: Análise Exploratória
elif selected == "Análise Exploratória":
    st.title("📊 Análise Exploratória do Preço do Petróleo")

    # 🔹 Carregamento dos Dados
    @st.cache_data
    def get_data():
        brent_data = yf.Ticker("BZ=F")
        df = pd.DataFrame(brent_data.history(period="max"))
        df['Date'] = pd.to_datetime(df.index, format='%Y-%m-%d')
        df.index = df['Date']
        df = df[['Close']].rename(columns={'Close': 'Preço'})
        return df

    df = get_data()

    # 🔹 Filtros de Período
    data_min = df.index.min().date()
    data_max = df.index.max().date()
    periodo = st.sidebar.date_input("Selecione o período", [data_min, data_max], min_value=data_min, max_value=data_max)

    if len(periodo) == 2:
        df_filtrado = df.loc[periodo[0]:periodo[1]]
    else:
        df_filtrado = df.copy()

    # 🔹 Estatísticas Anuais
    df_filtrado['Ano'] = df_filtrado.index.year
    estatisticas_anual = df_filtrado.groupby('Ano')['Preço'].agg(['max', 'min', 'mean']).reset_index()

    # 🔹 Opções de Métricas
    opcoes = {"Preço Máximo": "max", "Preço Mínimo": "min", "Preço Médio": "mean"}
    selecao = st.sidebar.multiselect("Escolha as métricas", list(opcoes.keys()), default=list(opcoes.keys()))

    estatisticas_anual = estatisticas_anual[['Ano'] + [opcoes[opcao] for opcao in selecao]]

    # 🔹 Gráfico de Barras Interativo
    fig = px.bar(
        estatisticas_anual.melt(id_vars=['Ano'], var_name="Métrica", value_name="Preço"),
        x="Ano",
        y="Preço",
        color="Métrica",
        barmode="group",
        labels={"Preço": "Preço do Petróleo (USD)", "Ano": "Ano", "Métrica": "Tipo de Preço"},
        title="Evolução do Preço do Petróleo por Ano"
    )
    st.plotly_chart(fig, use_container_width=True)

# 🔹 PÁGINA 3: Dados Históricos
elif selected == "Dados Históricos":
    st.title("📜 Dados Históricos do Preço do Petróleo")

    # 🔹 Crises Históricas
    crises = {
        "Crise Financeira de 2008": pd.Timestamp("2008-07-01"),
        "Queda do Petróleo em 2014": pd.Timestamp("2014-06-01"),
        "Pandemia COVID-19 (2020)": pd.Timestamp("2020-03-01")
    }

    fig = px.line(df, x=df.index, y="Preço", title="Variação Histórica do Preço do Petróleo",
                  labels={"Preço": "Preço do Petróleo (USD)", "index": "Ano"})

    # 🔹 Adicionando Linhas Verticais para Crises
    for crise, data in crises.items():
        fig.add_vline(x=data, line_dash="dash", line_color="red", annotation_text=crise)

    st.plotly_chart(fig, use_container_width=True)

# 🔹 PÁGINA 4: Modelo Preditivo
elif selected == "Modelo Preditivo":
    st.title("📈 Modelo de Previsão do Preço do Petróleo")
    st.write("Aqui será inserida a previsão baseada no melhor modelo.")
