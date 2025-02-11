import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Configuração do Streamlit
st.set_page_config(page_title="Análise do Preço do Petróleo", layout="wide")

# 🔹 Função para carregar os dados do petróleo Brent
@st.cache_data
def get_data():
    brent_data = yf.Ticker("BZ=F")
    df = pd.DataFrame(brent_data.history(period="max"))

    # 🔹 Ajustando o índice para não mostrar horas
    df['Date'] = pd.to_datetime(df.index, format='%Y-%m-%d').date
    df.index = df['Date']

    # 🔹 Selecionando as colunas relevantes
    df = df[['Close']].rename(columns={'Close': 'Preço'})

    return df

df = get_data()

if df is None or df.empty:
    st.error("Erro ao carregar os dados do petróleo Brent. Verifique a API do Yahoo Finance.")
    st.stop()  # Para a execução se os dados não carregarem corretamente

# 🔹 Barra lateral para navegação
st.sidebar.title("Menu de Navegação")
pagina = st.sidebar.radio("Escolha a Página", ["📊 Análise Exploratória", "📜 Dados Históricos", "📈 Modelo Preditivo"])

# 🔹 📊 Página 1: Análise Exploratória
if pagina == "📊 Análise Exploratória":
    st.title("Análise Exploratória do Preço do Petróleo")

    # 🔹 Filtro de período
    data_min = df.index.min()
    data_max = df.index.max()

    periodo = st.sidebar.date_input("Selecione o período", [data_min, data_max], min_value=data_min, max_value=data_max)

    # 🔹 Filtrando os dados corretamente
    df_filtrado = df.loc[periodo[0]:periodo[1]]

    # 🔹 Criando DataFrame com estatísticas anuais
    df_filtrado['Ano'] = pd.to_datetime(df_filtrado.index).year
    estatisticas_anual = df_filtrado.groupby('Ano')['Preço'].agg(['max', 'min', 'mean']).reset_index()

    # 🔹 Criando a caixa de seleção para o usuário escolher quais métricas visualizar
    opcoes = {
        "Preço Máximo": "max",
        "Preço Mínimo": "min",
        "Preço Médio": "mean"
    }
    
    selecao = st.sidebar.multiselect(
        "Escolha quais métricas deseja visualizar",
        options=list(opcoes.keys()), 
        default=["Preço Médio", "Preço Máximo", "Preço Mínimo"]  # Exibe todas as métricas por padrão
    )

    # 🔹 Filtrando apenas as colunas selecionadas
    estatisticas_anual = estatisticas_anual[['Ano'] + [opcoes[opcao] for opcao in selecao]]

    # 🔹 Criando gráfico de barras interativo com Plotly
    fig = px.bar(
        estatisticas_anual.melt(id_vars=['Ano'], var_name="Métrica", value_name="Preço"),
        x="Ano",
        y="Preço",
        color="Métrica",
        barmode="group",
        labels={"Preço": "Preço do Petróleo (USD)", "Ano": "Ano", "Métrica": "Tipo de Preço"},
        title="Evolução do Preço do Petróleo por Ano"
    )

    # 🔹 Exibindo o gráfico interativo no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # 🔹 Gráfico de linha: preço real ao longo do tempo
    st.line_chart(df_filtrado['Preço'])

# 🔹 📜 Página 2: Dados Históricos
elif pagina == "📜 Dados Históricos":
    st.title("Dados Históricos do Preço do Petróleo")

    # 🔹 Criação de um gráfico destacando períodos de crise
    crises = {
        "Crise Financeira de 2008": "2008-07-01",
        "Queda do Petróleo em 2014": "2014-06-01",
        "Pandemia COVID-19 (2020)": "2020-03-01"
    }

    fig = px.line(
        df, x=df.index, y="Preço", title="Variação Histórica do Preço do Petróleo",
        labels={"Preço": "Preço do Petróleo (USD)", "index": "Ano"}
    )

    # 🔹 Adicionando as linhas verticais para crises
    for crise, data in crises.items():
        fig.add_vline(x=pd.to_datetime(data), line_dash="dash", line_color="red", annotation_text=crise)

    st.plotly_chart(fig, use_container_width=True)

# 🔹 📈 Página 3: Modelo Preditivo
elif pagina == "📈 Modelo Preditivo":
    st.title("Modelo de Previsão do Preço do Petróleo")

    st.write("Aqui será inserida a previsão baseada no melhor modelo.")

# 🔹 Tratamento para evitar erro caso nenhuma opção seja escolhida
else:
    st.write("Selecione uma página no menu lateral para visualizar os dados.")
