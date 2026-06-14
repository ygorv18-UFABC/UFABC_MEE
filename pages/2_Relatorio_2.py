import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Relatório 2", page_icon="📈")

st.title("📈 Relatório 2: Ensaio de Tração")
st.write("Análise de tensão e deformação em um corpo de prova de aço.")

# Gerando dados fictícios
deformacao = np.linspace(0, 0.05, 50)
tensao_mdf = deformacao * 200000 # Fase elástica simulada (Lei de Hooke)
tensao_mdf[25:] = tensao_mdf[24] + np.random.normal(0, 500, 25) # Simulando escoamento/quebra

df = pd.DataFrame({
    'Deformação (mm/mm)': deformacao,
    'Tensão (MPa)': tensao_mdf
})

st.write("### Gráfico Tensão-Deformação")
# Gráfico de área para visualização diferente
st.area_chart(df, x='Deformação (mm/mm)', y='Tensão (MPa)')

st.write("### Tensão Máxima Registrada")
st.metric(label="Limite de Resistência à Tração", value=f"{df['Tensão (MPa)'].max():.2f} MPa")

with st.expander("Ver dados brutos do ensaio"):
    st.table(df.head(10)) # Mostra apenas as 10 primeiras linhas de forma estática