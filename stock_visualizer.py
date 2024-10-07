import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

def main():
    # Configuração da página
    st.set_page_config(page_title="Visualizador de Ações", layout="wide")

    # Título do app
    st.title("Visualizador de Ações")

    # Barra lateral para controles
    with st.sidebar:
        # Barra de pesquisa para selecionar o símbolo da ação
        stock_symbol = st.text_input("Digite o símbolo da ação (ex: AAPL, MSFT, TSLA):").upper()
        
        # Seleção de período
        period_options = {
            '1 semana': 7,
            '1 mês': 30,
            '3 meses': 90,
            '6 meses': 180,
            '1 ano': 365,
            '5 anos': 1825
        }
        selected_period = st.selectbox("Selecione o período", list(period_options.keys()))
        
        # Métrica a ser exibida
        metrics = ['Close', 'Open', 'High', 'Low', 'Volume']
        selected_metric = st.selectbox("Selecione a métrica para visualizar", metrics)

    # Função para baixar e processar dados
    @st.cache_data
    def get_stock_data(symbol, days):
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        data = yf.download(symbol, start=start_date, end=end_date)
        return data

    # Principal
    if stock_symbol:
        # Baixando os dados da ação
        days = period_options[selected_period]
        stock_data = get_stock_data(stock_symbol, days)
        
        if not stock_data.empty:
            # Criando o gráfico com Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[selected_metric],
                                     mode='lines', name=selected_metric))
            fig.update_layout(title=f'{stock_symbol} - {selected_metric}',
                              xaxis_title='Data',
                              yaxis_title=selected_metric)
            
            # Exibindo o gráfico
            st.plotly_chart(fig, use_container_width=True)
            
            # Exibindo estatísticas básicas
            st.subheader("Estatísticas Básicas")
            st.write(stock_data[selected_metric].describe())
            
            # Download dos dados
            csv = stock_data.to_csv().encode('utf-8')
            st.download_button(
                label="Download dados como CSV",
                data=csv,
                file_name=f'{stock_symbol}_stock_data.csv',
                mime='text/csv',
            )
        else:
            st.error("Não foi possível encontrar dados para o símbolo fornecido.")
    else:
        st.info("Por favor, insira um símbolo de ação para começar.")

if __name__ == "__main__":
    main()
