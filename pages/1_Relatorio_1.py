import streamlit as st
import pandas as pd
import numpy as np

# Configuração da Página
st.set_page_config(page_title="Relatório 1: Densidade", page_icon="📏", layout="wide")

st.title("📏 Relatório 1: Dimensões e Densidades de Sólidos")
st.write("""
Este relatório apresenta as medições de dimensões e massas de um sólido geométrico (Cilindro), 
a avaliação das incertezas e o cálculo final do volume e densidade para identificação do material.
""")


medidas = ["Medida 1", "Medida 2", "Medida 3", "Medida 4", "Medida 5", "Medida 6"]
medidas2 = ["Medida 1", "Medida 2", "Medida 3", "Medida 4", "Medida 5", "Medida 6","incerteza Tipo A", "incerteza Tipo B", "Incerteza da massa"]
medidas3 = ["Medida 1", "Medida 2", "Medida 3", "Medida 4", "Medida 5", "Medida 6","incerteza Tipo A", "incerteza Tipo B", "Incerteza do lado"]


st.divider()

# ==========================================
# 1. Tabela de Instrumentos
# ==========================================
st.subheader("1. Dados dos Instrumentos Utilizados")
st.write("Levantamento das características e incerteza instrumental (Tipo B).")

dados_instrumentos = {
    "Instrumento": ["Balança Digital", "Régua Milimétrica", "Paquímetro", "Micrômetro"],
    "Marca": ["SHIMADZU CORPORATION ", "Acrinil", "KINGTOOLS", "PANAMBRA TÉCNICA"],
    "Modelo": ["BL-3200H", "acrílico 30cm ", "VERNIER CALIPER", "Outside Micrometer"],
    "Fundo de Escala": ["3200 g", "300 mm", "150 mm", "25 mm"],
    "Resolução": ["0,01 g", "1 mm", "0,02 mm", "0,001 mm"],
    "Incerteza (Tipo B)": ["0,029 g", "0,5 mm", "0,02 mm", "0,001 mm"]
}
df_instrumentos = pd.DataFrame(dados_instrumentos)
st.dataframe(df_instrumentos, use_container_width=True, hide_index=True)

# ==========================================
# 2. Medidas de Massa
# ==========================================
st.subheader("2. Medidas de Massa do Objeto")

col1, col2 = st.columns([1, 1])

# Dados fictícios de medição
medidas_massa = np.array([
    58.01,
    58.02,
    58.03,
    58.02,
    58.02,
    58.02,
    ])
media_massa = np.mean(medidas_massa)
incerteza_a_massa = np.std(medidas_massa, ddof=1) / np.sqrt(len(medidas_massa)) # Desvio padrão da média
incerteza_b_massa = 0.02886751346 # Da tabela acima
incerteza_combinada_massa = np.sqrt(incerteza_a_massa**2 + incerteza_b_massa**2)
medidas_massa2 = np.append(medidas_massa, [incerteza_a_massa, incerteza_b_massa, incerteza_combinada_massa])

df_massa = pd.DataFrame({
    "Medida": medidas,
    "Massa (g)": medidas_massa
})

df_massa2 = pd.DataFrame({
    "Medida": medidas2,
    "Massa (g)": medidas_massa2
})

with col1:
    st.write("**Tabela 2: Resultados das pesagens**")
    st.dataframe(df_massa, use_container_width=True, hide_index=True)

with col2:
    st.write("**Resultados Estatísticos (Massa):**")
    st.metric("Média da Massa", f"{media_massa:.2f} g")
    st.write(f"- **Incerteza Tipo A:** {incerteza_a_massa:.4f} g")
    st.write(f"- **Incerteza Tipo B:** {incerteza_b_massa:.4f} g")
    st.info(f"**Incerteza Combinada:** {incerteza_combinada_massa:.4f} g")

st.divider()
with col1:
    st.divider()
    st.write("**para relatorio**")
    st.write("**Tabela 2: Resultados das pesagens**")
    st.dataframe(df_massa2, use_container_width=True, hide_index=True)


# ==========================================
# 3. Medidas de Dimensões (Cubo) com Paquímetro
# ==========================================
st.subheader("3. Medidas de Dimensões do lado do Cubo")
st.subheader("3.1 (Paquímetro)")
st.write("Para o cálculo do volume do cubo, medimos o lado (L) .")

# Dados fictícios
ladosp = np.array([
    19.02,
    19.08,
    19.06,
    19.00,
    19.02,
    19.08]) # paquimetro (mm)
ladosm = np.array([
    19.031,
    19.040,
    19.039,
    19.030,
    19.032,
    19.005]) # micrômetro (mm)
lador = np.array([
    18.5,
    18.5,
    19.0,
    18.5,
    19.0,
    19.0]) # regua (mm)
media_lp = np.mean(ladosp)  # mm
media_lm = np.mean(ladosm)  # mm
media_lr = np.mean(lador)  # mm
incerteza_a_lp = np.std(ladosp, ddof=1) / np.sqrt(len(ladosp)) # Desvio padrão da média
incerteza_a_lm = np.std(ladosm, ddof=1) / np.sqrt(len(ladosm)) # Desvio padrão da média
incerteza_a_lr = np.std(lador, ddof=1) / np.sqrt(len(lador)) # Desvio padrão da média
incerteza_b_lp = 0.02 # mm (da tabela de instrumentos)
incerteza_b_lm = 0.001 # mm (da tabela de instrumentos)
incerteza_b_lr = 0.5 # mm (da tabela de instrumentos)
incerteza_combinada_lp = np.sqrt(incerteza_a_lp**2 + incerteza_b_lp**2)
incerteza_combinada_lm = np.sqrt(incerteza_a_lm**2 + incerteza_b_lm**2)
incerteza_combinada_lr = np.sqrt(incerteza_a_lr**2 + incerteza_b_lr**2)
ladosp2 = np.append(ladosp, [incerteza_a_lp, incerteza_b_lp, incerteza_combinada_lp])
ladosm2 = np.append(ladosm, [incerteza_a_lm, incerteza_b_lm, incerteza_combinada_lm])
lador2 = np.append(lador, [incerteza_a_lr, incerteza_b_lr, incerteza_combinada_lr])
df_dimensoesp = pd.DataFrame({
    "Medida": medidas,
    "Lado (mm)": ladosp
})

df_dimensoesm = pd.DataFrame({
    "Medida": medidas,
    "Lado (mm)": ladosm
})

df_dimensoesr = pd.DataFrame({
    "Medida": medidas,
    "Lado (mm)": lador
})

df_relatorio = pd.DataFrame({
    "Medida": medidas3,
    "Lado (mm) - Paquímetro": ladosp2,
    "Lado (mm) - Micrômetro": ladosm2,
    "Lado (mm) - Régua": lador2   
})


col3, col4 = st.columns(2)
with col3:
    st.dataframe(df_dimensoesp.style.format({"Lado (mm)": "{:.2f}"}), use_container_width=True, hide_index=True)
with col4:
    st.write("**Resultados Estatísticos (Lado):**")
    st.metric("Média do Lado", f"{media_lp:.2f} mm")
    st.write(f"- **Incerteza Tipo A:** {incerteza_a_lp:.6f} mm")
    st.write(f"- **Incerteza Tipo B:** {incerteza_b_lp:.6f} mm")
    st.info(f"**Incerteza Combinada:** {incerteza_combinada_lp:.6f} mm")

st.subheader("3.2 (Micrômetro)")
col5, col6 = st.columns(2)
with col5:
    st.dataframe(df_dimensoesm.style.format({"Lado (mm)": "{:.2f}"}), use_container_width=True, hide_index=True)
with col6:
    st.write("**Resultados Estatísticos (Lado):**")
    st.metric("Média do Lado", f"{media_lm:.2f} mm")
    st.write(f"- **Incerteza Tipo A:** {incerteza_a_lm:.6f} mm")
    st.write(f"- **Incerteza Tipo B:** {incerteza_b_lm:.6f} mm")
    st.info(f"**Incerteza Combinada:** {incerteza_combinada_lm:.6f} mm")

st.subheader("3.3 (Régua)")
col7, col8 = st.columns(2)
with col7:
    st.dataframe(df_dimensoesr.style.format({"Lado (mm)": "{:.2f}"}), use_container_width=True, hide_index=True)
with col8:
    st.write("**Resultados Estatísticos (Lado):**")
    st.metric("Média do Lado", f"{media_lr:.2f} mm")
    st.write(f"- **Incerteza Tipo A:** {incerteza_a_lr:.6f} mm")
    st.write(f"- **Incerteza Tipo B:** {incerteza_b_lr:.6f} mm")
    st.info(f"**Incerteza Combinada:** {incerteza_combinada_lr:.6f} mm")

st.subheader("3.4 Análise Comparativa dos Instrumentos")
st.dataframe(df_relatorio.style.format({
    "Lado (mm) - Paquímetro": "{:.3f}", 
    "Lado (mm) - Micrômetro": "{:.4f}", 
    "Lado (mm) - Régua": "{:.2f}"}),
    use_container_width=True, hide_index=True)

st.divider()

# ==========================================
# 4. Cálculo de Volume e Densidade
# ==========================================
st.subheader("4. Resultados Finais e Identificação do Material")

# Volume de um cubo: V = L^3
volume = media_lp**3/1000  # Convertendo de mm³ para cm³
errov = ((3) * (media_lp**2) * incerteza_combinada_lp)/1000  # Propagação do erro para V = L^3
errom = incerteza_combinada_massa
errod = np.sqrt(
    (errom/volume)**2 + 
    ((errov*media_massa)/(volume**2))**2
    )  # Propagação do erro para d = m/V 
# Densidade: d = m / V
densidade = media_massa / volume

col9, col10 = st.columns(2)

with col9:
    st.write("### Cálculos Obtidos")
    st.metric("Volume Calculado", f"{volume:.6f} cm³")
    st.metric("Erro do Volume", f"±{errov:.6f} cm³")
    st.metric("Densidade Experimental", f"{densidade:.8f} g/cm³")
    st.metric("Erro da Densidade", f"±{errod:.8f} g/cm³")
with col10:
    st.write("### Tabela I - Densidade Típica de Materiais")
    # Tabela fornecida no roteiro
    df_materiais = pd.DataFrame({
        "Material": ["Alumínio", "Latão", "Ferro", "Cobre", "Acrílico", "Polipropileno", "PVC rígido", "Nylon", "Polietileno", "Vidro"],
        "Densidade (g/cm³)": [2.70, 8.93, 7.87, 8.92, 1.19, 0.91, 1.40, 1.12, 0.95, "2.0-2.9"]
    })
    st.dataframe(df_materiais, use_container_width=True, hide_index=True)


