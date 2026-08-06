import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import streamlit as st
import pandas as pd



# =============================================================================
# 1. FUNÇÃO MODELO
# =============================================================================
# O modelo matemático é y = mx + k, que reflete a equação física linear
def modelo_linear(n, A, B):
    return (A*n) + B

def modelo_reto(n, B):
    return 0*n + B



n = [1,2,3,4,5,6,7,8,9,10]
a = [ 13.4, 12.6, 12.7, 11.9, 10.5, 11.1, 9.9, 10.8, 10.1, 9.8 ]
b = [6.5, 5.9, 6.1, 5.8, 5.6, 5.8, 5.5, 5.5, 5.1, 5.1 ]
ba = [5.8, 5.9, 5.5, 5.7, 5.2, 5.5, 5.2, 5.2, 5.3, 5]

list = {
    "N":n,
    "A":a,
    "B":b,
    "BA":ba,

}
df = pd.DataFrame(list)
st.dataframe(df)


n_dados = df['N']
b_dados = df["B"]
ba_dados = df["BA"]


chute_inicialb = [-0.15, 0] 
# popt: Array com os parâmetros otimizados [A, B]
# pcov: Matriz de covariância associada ao ajuste
popt, pcov = curve_fit( 
    modelo_linear, 
    n_dados, 
    b_dados,
    p0=chute_inicialb,
#    sigma=incerteza_dt,
    absolute_sigma=True,
    )

A_opt, B_opt = popt

# As incertezas padrão (desvios) são a raiz quadrada da diagonal da matriz de covariância
incertezas = np.sqrt(np.diag(pcov))
u_A, u_B = incertezas
n_curva = np.linspace(min(n_dados), max(n_dados), 100)
dt_curva = modelo_linear(n_curva, A_opt, B_opt)

chute_inicialba = [-0.15, 0] 
# popt: Array com os parâmetros otimizados [A, B]
# pcov: Matriz de covariância associada ao ajuste
popta, pcova = curve_fit( 
    modelo_linear, 
    n_dados, 
    ba_dados,
    p0=chute_inicialba,
#    sigma=incerteza_dt,
    absolute_sigma=True,
    )

Aa_opt, Ba_opt = popta

# As incertezas padrão (desvios) são a raiz quadrada da diagonal da matriz de covariância
incertezas = np.sqrt(np.diag(pcova))
u_A, u_B = incertezas
na_curva = np.linspace(min(n_dados), max(n_dados), 100)
dta_curva = modelo_linear(na_curva, Aa_opt, Ba_opt)



chute_inicial01 = [5.5] 
# popt: Array com os parâmetros otimizados [A, B]
# pcov: Matriz de covariância associada ao ajuste
popt01, pcov01 = curve_fit( 
    modelo_reto, 
    n_dados, 
    ba_dados,
    p0=chute_inicial01,
#    sigma=incerteza_dt,
    absolute_sigma=True,
    )

B01_opt = popt01[0]

# As incertezas padrão (desvios) são a raiz quadrada da diagonal da matriz de covariância
incertezas = np.sqrt(np.diag(pcova))
u_A, u_B = incertezas
n01_curva = np.linspace(min(n_dados), max(n_dados), 100)
dt01_curva = modelo_reto(n01_curva, B01_opt)

plt.figure(figsize=(8, 5))
plt.scatter(n_dados, b_dados, color='black', marker='o', s=20, label='Dados Experimentais B')
plt.scatter(n_dados, ba_dados, color='green', marker='o', s=20, label='Dados Experimentais B + A')

plt.errorbar(
    n_dados, b_dados, 
#   yerr=incerteza_dt, 
    fmt='o', 
    color='black', 
    ecolor='red', 
    capsize=4, 
    markersize=5, 
    label='Dados Exp. com Erro Instrumental ($\pm 0.02$ s)'
)
plt.plot(n_curva,dt_curva, color='blue', linewidth=1.5, label=f'Ajuste B: $y = {A_opt:.4f}X +  {B_opt:.4f}$')
plt.plot(n_curva,dta_curva, color='cyan', linewidth=1.5, label=f'Ajuste B + A: $y = {Aa_opt:.4f}X +  {Ba_opt:.4f}$')
plt.plot(n_curva,dt01_curva, color='red', linewidth=3, label=f'Ajuste A hipotese: $y = {0:.4f}X +  {B01_opt:.4f}$')
plt.title("Ajuste linear: $\Theta _n$ em função de $n$")
plt.xlabel("Número do experimento ($n$)")
plt.ylabel("Angulo de Deslizamento")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

st.pyplot(plt)
