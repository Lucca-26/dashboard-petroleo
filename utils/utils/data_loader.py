import yfinance as yf
import pandas as pd

def get_data():
    """
    Função para carregar os dados do petróleo Brent usando yfinance.
    Retorna um DataFrame com as colunas 'Data' e 'Preço'.
    """
    df = yf.download('BZ=F', start='1987-01-01', end='2025-01-01')

    # Verificar se "Adj Close" ou "Close" está disponível
    if 'Adj Close' in df.columns:
        df = df[['Adj Close']].rename(columns={'Adj Close': 'Preço'})
    elif 'Close' in df.columns:
        df = df[['Close']].rename(columns={'Close': 'Preço'})
    else:
        raise ValueError("Erro: Nenhuma coluna de preço encontrada no dataset.")

    df = df.reset_index()
    df.rename(columns={'Date': 'Data'}, inplace=True)

    # Convertendo Data para datetime e removendo fuso horário (se houver)
    df['Data'] = pd.to_datetime(df['Data']).dt.tz_localize(None)

    return df