import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import streamlit as st
import pandas as pd



# Configuração da página
st.set_page_config(page_title="Coeficiente de Restituição", layout="wide")
st.title("Coeficiente de Restituição")
st.markdown("Coleta de dados e tabelas para o Experimento 3 - Métodos Experimentais em Engenharia.")

st.divider()

# -----------------------------------------------------------------------------
# Método 1: A partir do tempo entre o 1º e o 2º impacto
# -----------------------------------------------------------------------------
st.header("1. Método 1: Tempo entre o 1º e o 2º impacto")
st.markdown("Equação: $\epsilon = \Delta t_1 / (2 t_0)$")

# Criação de um DataFrame rascunho com 5 repetições
dados_metodo_1 = {
    "Medição": [1],
    "Altura H (m)": [0.6],
    "Δt_1 (s)": [0.596],
}
 
df_m1 = pd.DataFrame(dados_metodo_1)
df_m1["t_0 calculado (s)"] = np.sqrt(2 * df_m1["Altura H (m)"] / 9.81)
df_m1["Ut0 (s)"] = 0.005/np.sqrt(2 * df_m1["Altura H (m)"] * 9.81)
df_m1["ε Calculado"] = df_m1["Δt_1 (s)"] / (2 * df_m1["t_0 calculado (s)"]) 
ut0 = df_m1["Ut0 (s)"].values[0]
t0 = df_m1["t_0 calculado (s)"].values[0]
t1 = df_m1["Δt_1 (s)"].values[0]
put0 = ((t1 * ut0) / (2 * t0 * t0))**2
put1 = (0.004 / (2 * t0))**2
ue = np.sqrt(put0 + put1)
print(f"put0 = {put0:.8f}")
print(f"put1 = {put1:.8f}")
print(f"ue = {ue:.8f}")
df_m1["Uε"] = ue
df_m1t = df_m1.T
st.dataframe(df_m1t, width=250)

st.divider()

# -----------------------------------------------------------------------------
# Método 2: A partir de dois intervalos de tempo sucessivos
# -----------------------------------------------------------------------------
st.header("2. Método 2: Dois intervalos de tempo sucessivos")
st.markdown("Equação: $\epsilon = \Delta t_{n+1} / \Delta t_n$ (Ex: $\Delta t_2 / \Delta t_1$)")

dt1 = 0.6
dt2 = 0.52
ut = 0.010


dados_metodo_2 = {
    "Medição": [1],
    "Δt_1 (s)": dt1,
    "Δt_2 (s)": dt2,
  }
df_m2 = pd.DataFrame(dados_metodo_2)
df_m2["ε Calculado"] = df_m2["Δt_2 (s)"] / df_m2["Δt_1 (s)"]
put1 = ((ut* dt2) / (dt1 * dt1))**2
put2 = (ut / dt1)**2
ue = np.sqrt(put1 + put2)
print(f"put1 = {put1:.8f}")
print(f"put2 = {put2:.8f}")
print(f"ue = {ue:.8f}")
df_m2["Ut"] = ut
df_m2["Uε"] = ue


st.dataframe(df_m2, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# Método 3: A partir de n intervalos de tempo sucessivos
# -----------------------------------------------------------------------------
st.header("3. Método 3: Múltiplos (n) intervalos sucessivos")
st.markdown("Equação base: $\Delta t_n = 2 t_0 \epsilon^n$")
st.info("Atenção: Para este método, preencher os dados para a bola de pingue-pongue até n >= 10.")

# Criando tabela para n de 1 a 15
dtn={
0.600,
0.520,
0.460,
0.420,
0.400,
0.360,
0.320,
0.300,
0.260,
0.260,
0.240,
0.220,
}
dtn_df = pd.DataFrame(dtn, columns=["Δt_n (s)"])
n_valores = list(range(1, dtn_df.shape[0] + 1))

for i in range(len(n_valores)):
    if i == 0:
        dtn_df.loc[i, "e"] = np.nan
    else:
        dtn_df.loc[i, "e"] = dtn_df["Δt_n (s)"].iloc[i] / dtn_df["Δt_n (s)"].iloc[i - 1]

dados_metodo_3 = {
    "n (Número do Impacto)": n_valores,
    "Δt_n (s)": dtn_df["Δt_n (s)"],
    "e": dtn_df["e"]
}

df_m3 = pd.DataFrame(dados_metodo_3)

st.dataframe(df_m3, use_container_width=True)


st.divider()




# =============================================================================
# 1. FUNÇÃO MODELO
# =============================================================================
# O modelo matemático é y = A * B^x, que reflete a equação física dt_n = (2*t_0) * e^n
def modelo_exponencial(n, A, B):
    return A * (B ** n)

# =============================================================================
# 2. INSERÇÃO DOS DADOS REAIS
# =============================================================================
n_dados = np.array(df_m3["n (Número do Impacto)"].values)
dt_dados = np.array(df_m3["Δt_n (s)"].values) 
# Incerteza do instrumento (cursores do osciloscópio) para todos os pontos: +- 0.02s
incerteza_dt = np.full(len(n_dados), 0.02)

# =============================================================================
# 3. PLOTAGEM DOS DADOS BRUTOS (Sem Ajuste e Sem Escala Log)
# =============================================================================
plt.figure(figsize=(8, 5))
plt.scatter(n_dados, dt_dados, color='black', marker='o', s=20, label='Dados Experimentais')
plt.title("Dispersão dos Dados: $\Delta t_n$ em função de $n$")
plt.xlabel("Número do impacto ($n$)")
plt.ylabel("Intervalo de tempo $\Delta t_n$ (s)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
st.pyplot(plt)

# =============================================================================
# 4. AJUSTE DE CURVA COM RIGOR MATEMÁTICO (Scipy curve_fit)
# =============================================================================
# Fornecendo um "chute inicial" (p0) para o algoritmo convergir mais rápido
chute_inicial = [0.6, 0.9] 

# popt: Array com os parâmetros otimizados [A, B]
# pcov: Matriz de covariância associada ao ajuste
popt, pcov = curve_fit( 
    modelo_exponencial, 
    n_dados, 
    dt_dados,
    p0=chute_inicial,
    sigma=incerteza_dt,
    absolute_sigma=True,
    )

A_opt, B_opt = popt

# As incertezas padrão (desvios) são a raiz quadrada da diagonal da matriz de covariância
incertezas = np.sqrt(np.diag(pcov))
u_A, u_B = incertezas

# =============================================================================
# 5. CÁLCULO DAS GRANDEZAS FÍSICAS E PROPAGAÇÃO DE INCERTEZA
# =============================================================================
# t_0 = A / 2  -->  u_t0 = u_A / 2
t0 = A_opt / 2
u_t0 = u_A / 2

# epsilon = B  -->  u_epsilon = u_B
epsilon = B_opt
u_epsilon = u_B




# --- 3. Exibição dos Resultados na Interface ---
st.subheader("Parâmetros do Ajuste")
    
col1a, col2a, col3a, col4a = st.columns(4)
with col1a:
    st.metric(label="Parâmetro A", value=f"{A_opt:.4f}", delta=f"± {u_A:.4f}", delta_color="off")
with col2a  :
    st.metric(label="Parâmetro B", value=f"{B_opt:.4f}", delta=f"± {u_B:.4f}", delta_color="off")
with col3a:
    st.metric(label="Tempo Inicial (t₀)", value=f"{t0:.4f} s", delta=f"± {u_t0:.4f} s", delta_color="off")
with col4a:
    st.metric(label="Coef. Restituição (ε)", value=f"{epsilon:.4f}", delta=f"± {u_epsilon:.4f}", delta_color="off")

# =============================================================================
# 6. PLOTAGEM DO AJUSTE SOBRE OS DADOS
# =============================================================================
# Criar um vetor n mais denso para que a curva ajustada fique suave
n_curva = np.linspace(min(n_dados), max(n_dados), 100)
dt_curva = modelo_exponencial(n_curva, A_opt, B_opt)

plt.figure(figsize=(8, 5))
plt.scatter(n_dados, dt_dados, color='black', marker='o', s=20, label='Dados Experimentais')
plt.errorbar(
    n_dados, dt_dados, 
    yerr=incerteza_dt, 
    fmt='o', 
    color='black', 
    ecolor='red', 
    capsize=4, 
    markersize=5, 
    label='Dados Exp. com Erro Instrumental ($\pm 0.02$ s)'
)
plt.plot(n_curva, dt_curva, color='blue', linewidth=1.5, label=f'Ajuste: $y = {A_opt:.4f} \cdot {B_opt:.4f}^x$')
plt.title("Ajuste Exponencial: $\Delta t_n$ em função de $n$")
plt.xlabel("Número do impacto ($n$)")
plt.ylabel("Intervalo de tempo $\Delta t_n$ (s)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
st.pyplot(plt)









st.divider()

#logaritimo e reta
log_dt = np.log10(dt_dados)
coefs, cov = np.polyfit(n_dados, log_dt, 1, cov=True)



C_opt = coefs[0] # Coeficiente angular
D_opt = coefs[1] # Coeficiente linear

# Extraindo as incertezas estatísticas do ajuste linear
incertezas_linear = np.sqrt(np.diag(cov))
u_C = incertezas_linear[0]
u_D = incertezas_linear[1]

# =============================================================================
# 4. CONVERSÃO PARA OS PARÂMETROS FÍSICOS E PROPAGAÇÃO DE ERROS
# =============================================================================
# Cálculo de Epsilon e t0
epsilon = 10 ** C_opt
t0 = (10 ** D_opt) / 2

# Propagação de erro para logaritmos na base 10: derivada de 10^x é 10^x * ln(10)
u_epsilon = epsilon * np.log(10) * u_C
u_t0 = t0 * np.log(10) * u_D

# =============================================================================
# 5. EXIBIÇÃO NA INTERFACE STREAMLIT
# =============================================================================
st.subheader("1. Equações do Modelo Linearizado")
st.latex(r"\log(\Delta t_n) = C \cdot n + D")
st.latex(r"C = \log(\epsilon) \quad \text{e} \quad D = \log(2t_0)")

st.subheader("2. Parâmetros da Reta Ajustada (MMQ)")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Coeficiente Angular (C)", value=f"{C_opt:.4f}", delta=f"± {u_C:.4f}", delta_color="off")
with col2:
    st.metric(label="Coeficiente Linear (D)", value=f"{D_opt:.4f}", delta=f"± {u_D:.4f}", delta_color="off")

st.subheader("3. Grandezas Físicas Convertidas")
col3, col4 = st.columns(2)
with col3:
    st.metric(label="Tempo Inicial (t₀)", value=f"{t0:.4f} s", delta=f"± {u_t0:.4f} s", delta_color="off")
with col4:
    st.metric(label="Coef. Restituição (ε)", value=f"{epsilon:.4f}", delta=f"± {u_epsilon:.4f}", delta_color="off")

st.markdown("---")

# =============================================================================
# 6. PLOTAGEM DO GRÁFICO LINEARIZADO
# =============================================================================
st.subheader("Gráfico: Reta Ajustada no Eixo Logarítmico")

fig, ax = plt.subplots(figsize=(10, 6))

# Plotagem dos dados transformados
ax.scatter(n_dados, log_dt, color='teal', marker='D', s=40, label=r'Dados: $\log(\Delta t_n)$')

# Plotagem da reta do MMQ
n_reta = np.linspace(min(n_dados), max(n_dados), 100)
log_dt_reta = C_opt * n_reta + D_opt
ax.plot(n_reta, log_dt_reta, color='black', linewidth=1.5, label=f'Reta: $y = {C_opt:.4f}x {D_opt:+.4f}$')

# Formatação visual do gráfico (imitando o estilo do relatório original)
ax.set_title(r"Ajuste Linear: $\log(\Delta t_n)$ em função de $n$", fontsize=14)
ax.set_xlabel("Número do impacto ($n$)", fontsize=12)
ax.set_ylabel(r"$\log(\Delta t_n)$", fontsize=12)
ax.grid(True, which='both', linestyle='-', color='gray', alpha=0.5)
ax.legend(fontsize=11)

st.pyplot(fig)




st.divider()

# Função linear para o curve_fit
def modelo_linear(x, C, D):
    return C * x + D

# =============================================================================
# 2. CÁLCULO 1: MMQ COMUM (Sem considerar o peso das incertezas)
# =============================================================================
# Usando np.polyfit para o ajuste comum (todos os pontos têm o mesmo peso estatístico)
coefs_comum, cov_comum = np.polyfit(n_dados, log_dt, 1, cov=True)
C_comum, D_comum = coefs_comum
u_C_comum, u_D_comum = np.sqrt(np.diag(cov_comum))

# Conversão para parâmetros físicos e propagação de incerteza da conversão
eps_comum = 10 ** C_comum
t0_comum = (10 ** D_comum) / 2
u_eps_comum = eps_comum * np.log(10) * u_C_comum
u_t0_comum = t0_comum * np.log(10) * u_D_comum
# Propagação do erro para o domínio logarítmico: u_log = erro_inst / (dt * ln(10))
incerteza_log_dt = 0.02 / (dt_dados * np.log(10))
# =============================================================================
# 3. CÁLCULO 2: MMQ PONDERADO (Abordagem rigorosa tipo LABFit)
# =============================================================================
# Usando curve_fit para imputar a matriz de erros propagada (sigma)[cite: 1]
popt_pond, pcov_pond = curve_fit(
    modelo_linear, 
    n_dados, 
    log_dt, 
    sigma=incerteza_log_dt, 
    absolute_sigma=True
)
C_pond, D_pond = popt_pond
u_C_pond, u_D_pond = np.sqrt(np.diag(pcov_pond))

# Conversão para parâmetros físicos e propagação de incerteza da conversão[cite: 1]
eps_pond = 10 ** C_pond
t0_pond = (10 ** D_pond) / 2
u_eps_pond = eps_pond * np.log(10) * u_C_pond
u_t0_pond = t0_pond * np.log(10) * u_D_pond

# =============================================================================
# 4. EXIBIÇÃO DOS DADOS E GRÁFICOS NO STREAMLIT
# =============================================================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. MMQ Comum (Sem Incertezas)")
    st.markdown("O ajuste trata todos os pontos como se tivessem exata mesma precisão no domínio logarítmico.")
    st.metric("Parâmetro C (Angular)", f"{C_comum:.4f}", f"± {u_C_comum:.4f}", delta_color="off")
    st.metric("Parâmetro D (Linear)", f"{D_comum:.4f}", f"± {u_D_comum:.4f}", delta_color="off")
    st.metric("Coef. Restituição (ε)", f"{eps_comum:.4f}", f"± {u_eps_comum:.4f}", delta_color="off")
    st.metric("Tempo Inicial (t₀)", f"{t0_comum:.4f} s", f"± {u_t0_comum:.4f} s", delta_color="off")

with col_right:
    st.subheader("2. MMQ Ponderado (Com Incertezas)")
    st.markdown("O algoritmo utiliza $\sigma_{\log}$ como peso. Pontos iniciais ganham mais ancoragem do que os finais.")
    st.metric("Parâmetro C (Angular)", f"{C_pond:.4f}", f"± {u_C_pond:.4f}", delta_color="off")
    st.metric("Parâmetro D (Linear)", f"{D_pond:.4f}", f"± {u_D_pond:.4f}", delta_color="off")
    st.metric("Coef. Restituição (ε)", f"{eps_pond:.4f}", f"± {u_eps_pond:.4f}", delta_color="off")
    st.metric("Tempo Inicial (t₀)", f"{t0_pond:.4f} s", f"± {u_t0_pond:.4f} s", delta_color="off")

st.divider()

# =============================================================================
# 5. PLOTAGEM DIDÁTICA DO COMPORTAMENTO DOS ERROS NO GRÁFICO
# =============================================================================
st.subheader("Visualização do Ajuste no Espaço Logarítmico")
st.markdown("""
Observe as barras de erro em vermelho: a incerteza de $\pm 0.02 \text{ s}$ cresce significativamente nos choques finais 
($n > 8$) quando convertida para o logaritmo. A reta **Azul (Ponderada)** tenta passar mais exatamente no centro 
dos primeiros pontos, enquanto a reta **Preta (Comum)** é "puxada" para os últimos pontos indiscriminadamente.
""")

fig, ax = plt.subplots(figsize=(11, 7))

# Plotando os dados experimentais e suas barras de erro propagadas
ax.errorbar(
    n_dados, log_dt, 
    yerr=incerteza_log_dt, 
    fmt='o', 
    color='teal', 
    ecolor='red', 
    capsize=4, 
    markersize=6, 
    label=r'Dados: $\log(\Delta t_n)$ com Erro Propagado'
)

# Plotando as duas retas
n_reta = np.linspace(min(n_dados), max(n_dados), 100)
ax.plot(n_reta, modelo_linear(n_reta, C_comum, D_comum), color='black', linestyle='--', linewidth=2, label='Reta MMQ Comum')
ax.plot(n_reta, modelo_linear(n_reta, C_pond, D_pond), color='blue', linewidth=2, label='Reta MMQ Ponderado')

ax.set_title(r"Impacto dos Pesos na Regressão Linear: $\log(\Delta t_n) \times n$", fontsize=15)
ax.set_xlabel("Número do impacto ($n$)", fontsize=12)
ax.set_ylabel(r"$\log(\Delta t_n)$", fontsize=12)
ax.grid(True, which='both', linestyle='-', color='gray', alpha=0.3)
ax.legend(fontsize=12)

st.pyplot(fig)







st.divider()
st.header("4. Comparação dos Resultados (z-score)")

e1 = df_m1["ε Calculado"].mean()
e2 = df_m2["ε Calculado"].mean()
e3 = epsilon

dados_comparacao = {
    "Método": [
        "Método 1 (t_0 e Δt_1)", 
        "Método 2 (Δt_1 e Δt_2)", 
        "Método 3 (Gráfico / Regressão)"
    ],
    "ε Médio": [e1, e2, e3],
    "Incerteza Combinada (u_c)": [df_m1["Uε"], df_m2["Uε"], u_epsilon],
    "Valor Literário (Referência)": [0.85, 0.85, 0.85],
    "z-score": [np.nan, np.nan, np.nan]
}
df_comparacao = pd.DataFrame(dados_comparacao)

st.dataframe(df_comparacao, use_container_width=True)
