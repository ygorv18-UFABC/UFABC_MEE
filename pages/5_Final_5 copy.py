import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import streamlit as st
import pandas as pd


# 1. Dados experimentais extraídos das Tabelas 4, 5 e 6
n_dados = np.arange(1, 11)

# Ângulos críticos lidos pelo App Celular (em graus)
theta_A = np.array([13.4, 12.6, 12.7, 11.9, 10.5, 11.1, 9.9, 10.8, 10.1, 9.8])
theta_B = np.array([6.5, 5.9, 6.1, 5.8, 5.6, 5.8, 5.5, 5.5, 5.1, 5.1])
theta_BA = np.array([5.8, 5.9, 5.5, 5.7, 5.2, 5.5, 5.2, 5.2, 5.3, 5.0])
pi = np.pi
tan_A = np.tan(theta_A*pi/180)
tan_B = np.tan(theta_B*pi/180)
tan_BA = np.tan(theta_BA*pi/180)
#st.metric(label="tan",value=tan_A)
st.dataframe(tan_A)
st.dataframe(tan_B)
st.dataframe(tan_BA)



# Incerteza instrumental do App (resolução nominal)
incerteza_app = 0.58
incerteza_tan = 0.01
# 2. Definição dos modelos matemáticos
def modelo_linear(x, a, b):
    """Modelo para as tendências de queda (desgaste) dos discos B e B+A"""
    return a * x + b

def modelo_reto(x, b):
    """Modelo forçado para a hipótese inicial de constante (a=0) para o disco A"""
    return 0 * x + b

# 3. Execução do curve_fit
popt_B, pcov_B = curve_fit(modelo_linear, n_dados, theta_B)
popt_BA, pcov_BA = curve_fit(modelo_linear, n_dados, theta_BA)
popt_A, pcov_A = curve_fit(modelo_linear, n_dados, theta_A)

# Gerando os dados para as linhas contínuas de ajuste
n_curva = np.linspace(min(n_dados), max(n_dados), 100)
fit_B = modelo_linear(n_curva, *popt_B)
fit_BA = modelo_linear(n_curva, *popt_BA)
fit_A = modelo_linear(n_curva, *popt_A)

# 4. Construção do Gráfico
plt.figure(figsize=(10, 6))

# Plotagem dos dados dispersos (Scatters)
plt.scatter(n_dados, theta_A, color='red', marker='o', s=30, label='Dados Experimentais A')
plt.scatter(n_dados, theta_B, color='black', marker='o', s=30, label='Dados Experimentais B')
plt.scatter(n_dados, theta_BA, color='green', marker='o', s=30, label='Dados Experimentais B + A')

# Plotagem das barras de erro (conforme trecho de código fornecido)
plt.errorbar(
    n_dados, theta_B, 
    yerr=incerteza_app, 
    fmt='none', # 'none' para não desenhar linha nem marcador extra, já temos o scatter
    ecolor='black', 
    capsize=4, 
    label=f'Erro Instrumental ($\pm {incerteza_app}^\circ$)'
)
# Aplicando errorbar para as outras séries sem adicionar nova legenda
plt.errorbar(n_dados, theta_A, yerr=incerteza_app, fmt='none', ecolor='red', capsize=4)
plt.errorbar(n_dados, theta_BA, yerr=incerteza_app, fmt='none', ecolor='green', capsize=4)

# Plotagem das linhas de ajuste (Curve Fit)
plt.plot(n_curva, fit_A, color='red', linewidth=3, 
         label=f'Ajuste A hipótese: $y = {popt_A[0]:.4f}X + {popt_A[1]:.4f}$')

plt.plot(n_curva, fit_B, color='blue', linewidth=1.5, 
         label=f'Ajuste B: $y = {popt_B[0]:.4f}X + {popt_B[1]:.4f}$')

plt.plot(n_curva, fit_BA, color='cyan', linewidth=1.5, 
         label=f'Ajuste B + A: $y = {popt_BA[0]:.4f}X + {popt_BA[1]:.4f}$')

# 5. Configurações visuais (semelhante ao estilo do gráfico em anexo)
plt.title('Ajuste linear: $\\Theta_n$ em função de $n$', fontsize=14)
plt.xlabel('Número do experimento ($n$)', fontsize=12)
plt.ylabel('Ângulo de Deslizamento ($\\theta_c$)', fontsize=12)

# Grid estilizado
plt.grid(True, linestyle='--', alpha=0.7, linewidth=1)

# Legenda com fundo branco
plt.legend(loc='upper right', framealpha=1.0, edgecolor='black', fontsize=10)

# Ajuste de layout
plt.tight_layout()

# Exibir gráfico
st.pyplot(plt)





#---------------------------------



# 3. Execução do curve_fit
tpopt_B, tpcov_B = curve_fit(modelo_linear, n_dados, tan_B)
tpopt_BA, tpcov_BA = curve_fit(modelo_linear, n_dados, tan_BA)
tpopt_A, tpcov_A = curve_fit(modelo_linear, n_dados, tan_A)

# Gerando os dados para as linhas contínuas de ajuste
n_curva = np.linspace(min(n_dados), max(n_dados), 100)
tfit_B = modelo_linear(n_curva, *tpopt_B)
tfit_BA = modelo_linear(n_curva, *tpopt_BA)
tfit_A = modelo_linear(n_curva, *tpopt_A)

# 4. Construção do Gráfico
plt.figure(figsize=(10, 6))

# Plotagem dos dados dispersos (Scatters)
plt.scatter(n_dados, tan_A, color='red', marker='o', s=30, label='Dados Experimentais A')
plt.scatter(n_dados, tan_B, color='black', marker='o', s=30, label='Dados Experimentais B')
plt.scatter(n_dados, tan_BA, color='green', marker='o', s=30, label='Dados Experimentais B + A')

# Plotagem das barras de erro (conforme trecho de código fornecido)
plt.errorbar(
    n_dados, tan_B, 
    yerr=incerteza_tan, 
    fmt='none', # 'none' para não desenhar linha nem marcador extra, já temos o scatter
    ecolor='black', 
    capsize=4, 
    label=f'Erro Instrumental ({incerteza_tan})'
)
# Aplicando errorbar para as outras séries sem adicionar nova legenda
plt.errorbar(n_dados, tan_A, yerr=incerteza_tan, fmt='none', ecolor='red', capsize=4)
plt.errorbar(n_dados, tan_BA, yerr=incerteza_tan, fmt='none', ecolor='green', capsize=4)

# Plotagem das linhas de ajuste (Curve Fit)
plt.plot(n_curva, tfit_A, color='red', linewidth=3, 
         label=f'Ajuste A hipótese: $y = {tpopt_A[0]:.4f}X + {tpopt_A[1]:.4f}$')

plt.plot(n_curva, tfit_B, color='blue', linewidth=1.5, 
         label=f'Ajuste B: $y = {tpopt_B[0]:.4f}X + {tpopt_B[1]:.4f}$')

plt.plot(n_curva, tfit_BA, color='cyan', linewidth=1.5, 
         label=f'Ajuste B + A: $y = {tpopt_BA[0]:.4f}X + {tpopt_BA[1]:.4f}$')

# 5. Configurações visuais (semelhante ao estilo do gráfico em anexo)
plt.title('Ajuste linear: $tan(\\Theta_n$) em função de $n$', fontsize=14)
plt.xlabel('Número do experimento ($n$)', fontsize=12)
plt.ylabel('Tangente do angulo de Deslizamento tan($\\theta_c$)', fontsize=12)

# Grid estilizado
plt.grid(True, linestyle='--', alpha=0.7, linewidth=1)

# Legenda com fundo branco
plt.legend(loc='upper right', framealpha=1.0, edgecolor='black', fontsize=10)

# Ajuste de layout
plt.tight_layout()

# Exibir gráfico
st.pyplot(plt)