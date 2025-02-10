import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Título do dashboard
st.title("Dashboard de Preços do Petróleo Brent")

# Descrição
st.write("""
Este dashboard exibe os preços históricos do petróleo Brent e permite visualizar tendências e insights.
""")

# Coletar dados do petróleo Brent usando yfinance
@st.cache_data  # Cache para melhorar performance
def load_data():
    data = yf.download("BZ=F", start="2020-01-01", end="2023-12-31")
    return data

# Carregar os dados
data = load_data()

# Exibir os dados brutos
st.write("### Dados Históricos do Petróleo Brent")
st.write(data)

# Gráfico de linha dos preços
st.write("### Variação do Preço do Petróleo Brent")
plt.figure(figsize=(10, 6))
plt.plot(data['Close'], label='Preço de Fechamento')
plt.xlabel('Data')
plt.ylabel('Preço (USD)')
plt.title('Variação do Preço do Petróleo Brent')
plt.legend()
st.pyplot(plt)

# Insights
st.write("### Insights")
st.write("1. **Pandemia de COVID-19**: Em 2020, o preço do petróleo caiu drasticamente devido à redução da demanda global.")
st.write("2. **Recuperação Econômica**: A partir de 2021, os preços começaram a subir com a retomada da economia global.")
st.write("3. **Conflitos Geopolíticos**: Aumentos repentinos no preço do petróleo podem estar relacionados a conflitos geopolíticos.")
st.write("4. **Demanda Global por Energia**: O aumento da demanda global por energia tem impulsionado o preço do petróleo.")