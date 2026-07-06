import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

u_mb = 0.1/(2 * np.sqrt(3))  # Incerteza da balança digital (kg)
u_xb = 0.001/(2)  # Incerteza da régua (m)
u_dxb = u_xb*np.sqrt(2)  # Incerteza da diferença de posição (m)

col1, col2 = st.columns([1, 2])
st.metric("Incerteza da Balança Digital (kg)", value=u_mb, format="%.6f")
st.metric("Incerteza da Diferença de Posição (m)", value=u_dxb, format="%.6f")
st.metric("Incerteza da Régua (m)", value=u_xb, format="%.6f")

massas = {
    "Quantidade": [1, 1, 1, 1],
    "Formato": ["Paralelepípedo", "Cilindro", "Cilindro", "Cilindro"],
    "Material": ["Cu", "Cu", "Al (X)", "Al (1)"],
    "m": [1066.09, 836.96, 258.73, 258.55],
    "u_m": [u_mb, u_mb, u_mb, u_mb] # Erro calculado anteriormente
}
massas_df = pd.DataFrame(massas)
massas_df["m"] = massas_df["m"]/1000 # Convertendo de g para kg
st.subheader("Massa dos Sólidos")
st.dataframe( massas_df,
             use_container_width=True,
    column_config={
        "m": st.column_config.NumberColumn(format="%.6f"),
        "u_m": st.column_config.NumberColumn(format="%.4f"),
    }
)

m1 = massas_df["m"][0]
m2 = massas_df["m"][1]
m3 = massas_df["m"][2]
m4 = massas_df["m"][3]


df_a = pd.DataFrame({
        "Massa_Adicionada": [
            "1 Cu", 
            "1 Cu + 1 Al", 
            "1 Cu + 2 Al", 
            "2 Cu", 
            "2 Cu + 1 Al", 
            "2 Cu + 2 Al"
        ],

        "m":[
            m1,
            m1 + m3,
            m1 + m3 + m4,
            m1 + m2,
            m1 + m2 + m3,
            m1 + m2 + m3 + m4
        ],
        "dm": [
            0,
            m3,
            m3 + m4,
            m2,
            m2 + m3,
            m2 + m3 + m4
        ],
        "Força_Lida_F (N)": [
            0.0,    # F0
            2.4,    # F1
            4.8,    # F2
            8.0,    # F3
            10.4,   # F4
            13.9    # F5
        ],
        "Posição_x (m)": [
            0.142,  # x0
            0.151,  # x1
            0.161,  # x2
            0.174,  # x3
            0.185,  # x4
            0.195   # x5
        ]
    })


força_lida = np.array(df_a["Força_Lida_F (N)"])
u_Fb = np.array((força_lida*0.005) + 0.2)  # Incerteza da força (N)
x_lido = np.array(df_a["Posição_x (m)"])
delta_m = np.array(df_a["dm"])
dx0 = x_lido[0]
dx1 = x_lido[1] - dx0
dx2 = x_lido[2] - dx0
dx3 = x_lido[3] - dx0
dx4 = x_lido[4] - dx0
dx5 = x_lido[5] - dx0
delta_x = np.array([dx0, dx1, dx2, dx3, dx4, dx5])    


# 1. Cálculo das derivadas parciais
dK_dF = 1/delta_x
dK_ddx = força_lida / (delta_x**2)
# 2. Cálculo da incerteza propagada (u_K)
u_K = np.sqrt((dK_dF * u_Fb)**2 + (dK_ddx * u_dxb)**2)
# 3. Arredondamento para cima (aplicando a regra de limite de casas decimais)
# Exemplo para 2 casas decimais: multiplica por 100, aplica ceil, divide por 100
u_K_c = np.ceil(u_K * 100) / 100


res_df_a = pd.DataFrame({
    "F" : força_lida,
    "u_F" : u_Fb,
    "dm" : delta_m,
    "x" : x_lido,
    "Δx" : delta_x
})

res_df_a['k'] = res_df_a['F'] / res_df_a['Δx']
res_df_a['u_k'] = u_K
res_df_a['u_kc'] = u_K_c
res_df_a['k/g'] = res_df_a['dm']/ res_df_a['Δx']
res_df_a['k*'] = res_df_a['k/g'] * 9.81  # Convertendo para N/m

st.data_editor(res_df_a,
    use_container_width=True,
    column_config={
        "F": st.column_config.NumberColumn(format="%.4f"),
        "u_F": st.column_config.NumberColumn(format="%.4f"),
        "x": st.column_config.NumberColumn(format="%.4f"),
        "Δx": st.column_config.NumberColumn(format="%.4f"),
        "k": st.column_config.NumberColumn(format="%.4f"),
        "k/g": st.column_config.NumberColumn(format="%.4f"),
        "k*": st.column_config.NumberColumn(format="%.4f"),
    }
)
res_df_a = res_df_a.drop(index=0) 
força_lida = força_lida[1:]  # Removendo a primeira linha (onde F = 0)
delta_x = delta_x[1:]  # Removendo a primeira linha (onde Δx = 0)
media_k = res_df_a['k'].mean()
media_Km = res_df_a['k*'].mean()
st.divider()
st.metric("Média de k (N/m)", f"{media_k:.4f}")
st.metric("Média de k* (N/m)", f"{media_Km:.4f}")
st.header("usar a média do grafico essa é apenas para avaliar a consistência dos dados")

st.divider()
#----------------B------------------------
m_oscilante = 2100.64/1000  # Convertendo para kg
N_osc = 40
u_operador = 0.1
u_cronometro = 0.01 / (2 * np.sqrt(3))               # Cronômetro (s)
tempos = np.array([ 23.3, 24.12, 21.30, 21.97])

# 2. INCERTEZA COMBINADA DO PERÍODO (u_T)
n_medidas = len(tempos)
t_media = np.mean(tempos)
# Incerteza Tipo A: Desvio padrão da média experimental
# ddof=1 garante o cálculo do desvio padrão amostral (n-1)
s_t = np.std(tempos, ddof=1)
u_tipo_A = s_t / np.sqrt(n_medidas)

# Cálculo da incerteza combinada do tempo
u_T = np.sqrt(u_tipo_A**2 + u_operador**2 + u_cronometro**2)

    
st.metric("Massa do Oscilador (kg)", value=m_oscilante)
st.metric("Número de Oscilações (N)", value=N_osc)
st.metric("Incerteza do Operador (s)", value=u_operador)
st.metric("Incerteza do Cronômetro (s)", value=u_cronometro)

# Cálculo de K_B para cada tempo medido
# k = (4 * pi^2 * m * N^2) / T_N^2
k_b = [((4 * np.pi**2 * m_oscilante * (N_osc**2)) / (t**2)) for t in tempos]
k_b_media = np.mean(k_b)


# 3. INCERTEZA PROPAGADA DA CONSTANTE (u_kb)

# Derivadas parciais 
dk_dm = np.array([((4 * np.pi**2 * (N_osc**2)) / (t**2)) for t in tempos])
dk_dt = np.array([((8 * np.pi**2 * m_oscilante * N_osc**2)) / (t**3) for t in tempos])
u_kb = np.sqrt((dk_dm * u_mb)**2 + (dk_dt * u_T)**2)

# ==========================================
# 4. ARREDONDAMENTO (Sempre para cima)
# ==========================================
# Arredondando para 2 casas decimais (multiplica por 100, teto, divide por 100)
u_T_arredondado = np.ceil(u_T * 100) / 100
u_kb_arredondado = np.ceil(u_kb * 100) / 100


res_df_b = pd.DataFrame({
    "Tempo (s)": tempos,
    "u_T (s)": [u_T] * len(tempos),
    "k_B (N/m)": k_b,
    "u_kb (N/m)": u_kb
})


st.dataframe(res_df_b,
    use_container_width=True,
    column_config={
        "Tempo (s)": st.column_config.NumberColumn(format="%.2f"),
        "u_T (s)": st.column_config.NumberColumn(format="%.4f"),
        "k_B (N/m)": st.column_config.NumberColumn(format="%.4f"),
        "u_kb (N/m)": st.column_config.NumberColumn(format="%.4f"),
    }
)

st.metric("massa do oscilador (kg)", value=m_oscilante)
st.metric("Número de Oscilações (N)", value=N_osc)
st.metric("Incerteza do Cronômetro (s)", value=u_T)
st.metric("Média de k_B (N/m)", f"{k_b_media:.8f}")
        




#--------------------------------------graficos---------------

Fo = força_lida
u_F = u_Fb[1:]  # Incerteza do dinamômetro

# 2. MÉTODO DOS MÍNIMOS QUADRADOS (MMQ)
# ==========================================
# O np.polyfit com grau 1 faz o ajuste linear: F = K * dx + linear_b
# cov=True retorna a matriz de covariância para calcular o erro do coeficiente angular (K)
coeficientes, covariancia = np.polyfit(delta_x, Fo, 1, cov=True)

K_mmq = coeficientes[0]          # Coeficiente angular (a inclinação da reta, K)
intercepto = coeficientes[1]     # Coeficiente linear (onde cruza o eixo y)

# A incerteza de K é a raiz quadrada do primeiro elemento da diagonal da matriz de covariância
u_K_mmq = np.sqrt(covariancia[0, 0])

# Arredondando a incerteza de K para cima (ex: 1 casa decimal)
u_K_arredondado = np.ceil(u_K_mmq * 100) / 100
st.header("Resultados do Ajuste Linear (MMQ)")
st.metric("Constante Elástica Ajustada (K)", f"{K_mmq:.2f} N/m")
st.metric("Incerteza do Ajuste (u_K)", f"{u_K_arredondado:.2f} N/m")

# ==========================================
# 3. CONSTRUÇÃO DO GRÁFICO
# ==========================================
plt.figure(figsize=(10, 6))

# 3.1. Plotagem dos dados experimentais com as barras de erro
plt.errorbar(
    delta_x, Fo, 
    xerr=u_dxb, yerr=u_F, 
    fmt='o',                  # Formato do marcador (círculos)
    color='blue', 
    ecolor='red',             # Cor das barras de erro
    capsize=4,                # Tamanho do "chapéu" das barras de erro
    label='Dados Experimentais'
)

# 3.2. Plotagem da reta de tendência (MMQ)
# Criando um array contínuo de x para traçar a reta suavemente
x_reta = np.linspace(min(delta_x) - 0.005, max(delta_x) + 0.005, 100)
F_reta = K_mmq * x_reta + intercepto

plt.plot(
    x_reta, F_reta, 
    '--',                     # Linha tracejada
    color='black', 
    label=f'Ajuste MMQ: $F = {K_mmq:.2f} \cdot \Delta x {"+" if intercepto > 0 else ""} {intercepto:.2f}$'
)

# 3.3. Estilização Profissional (Padrão Acadêmico)
plt.title('Determinação da Constante Elástica (Método A)', fontsize=14)
plt.xlabel('Deformação $\Delta x$ (m)', fontsize=12)
plt.ylabel('Força Aplicada $F$ (N)', fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.7)

# Adicionando uma caixa de texto com o resultado final de K e sua incerteza
texto_resultado = f"$K = ({K_mmq:.1f} \pm {u_K_arredondado:.1f})$ N/m"
plt.text(
    0.05, 0.20, texto_resultado, 
    transform=plt.gca().transAxes, 
    fontsize=12, 
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
)

# Exibe o gráfico na tela
plt.tight_layout()
st.pyplot(plt)
# Se estiver usando o Streamlit em vez de um script Python normal, 
# substitua 'plt.show()' por 'st.pyplot(plt)'


st.title("Resultados do Experimento B")


# 2. Cálculo do desvio padrão da amostra (s)
# ddof=1 garante o uso de (n-1) no denominador, padrão para amostras experimentais
desvio_padrao = np.std(k_b, ddof=1)
incerteza_k = desvio_padrao / np.sqrt(4)
st.metric("Desvio Padrão da Amostra (s)", f"{desvio_padrao:.4f}")
st.metric("Incerteza Tipo A (u_k)", f"{incerteza_k:.4f}")




st.divider()
st.header("Item 11: Compatibilidade entre Métodos (Z-Score)")

# ==========================================
# 1. ENTRADA DE DADOS (Integração)
# ==========================================
# Se as variáveis já existirem no seu código unificado, você não precisa destes inputs manuais.
# Eles estão aqui apenas para garantir que a interface funcione isoladamente.
col_z1, col_z2 = st.columns(2)

with col_z1:
    st.markdown("**Método A (Estático - MMQ)**")
    k_a = K_mmq  # Valor de K do método A (N/m)
    u_ka = u_K_mmq  # Incerteza de K do método A
    st.metric("Constante Elástica (Método A)", f"{k_a:.2f} N/m")   
    st.metric("Incerteza (Método A)", f"{u_ka:.2f} N/m")

with col_z2:
    st.markdown("**Método B (Dinâmico - MHS)**")
    k_b = k_b_media  # Valor de K do método B (N/m)
    u_kb = incerteza_k  # Incerteza de K do método B
    st.metric("Constante Elástica (Método B)", f"{k_b:.2f} N/m")
    st.metric("Incerteza (Método B)", f"{u_kb:.2f} N/m")

# ==========================================
# 2. CÁLCULO DO Z-SCORE
# ==========================================
    # Prevenção de divisão por zero caso as incertezas sejam zeradas
        # Fórmula: Z' = |Ka - Kb| / sqrt(u_Ka^2 + u_Kb^2)
z_score = abs(k_a - k_b) / np.sqrt(u_ka**2 + u_kb**2)
        
st.latex(rf"Z' = \frac{{|{k_a:.2f} - {k_b:.2f}|}}{{\sqrt{{({u_ka:.2f})^2 + ({u_kb:.2f})^2}}}}")
        
st.metric(label="Resultado Z'", value=f"{z_score:.2f}")

        # ==========================================
        # 3. INTERPRETAÇÃO DAS HIPÓTESES
        # ==========================================
st.markdown("### Conclusão do Teste de Hipótese")
        
if z_score <= 2:
    st.success("**Medições Compatíveis (Aceita-se $H_0$)** \n\nO valor de $Z' \le 2$ demonstra que a diferença entre os métodos A e B é estatisticamente insignificante frente às incertezas do experimento.")
elif z_score > 3:
    st.error("**Medições Incompatíveis (Aceita-se $H_1$)** \n\nO valor de $Z' > 3$ demonstra que há uma divergência significativa. Provavelmente ocorreu algum erro sistemático não estimado em um dos métodos.")
else:
    st.warning("**Zona de Indeterminação ($2 < Z' \le 3$)** \n\nRecomenda-se cautela. A diferença é limítrofe e, de acordo com as diretrizes, o experimento deveria ser refeito para um diagnóstico mais assertivo.")

fig, ax = plt.subplots(figsize=(10, 5))

# Eixo X de -4 a 4 (representando os desvios padrão Z)
x = np.linspace(-4, 4, 1000)
# Equação matemática da Curva Normal Padrão
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

ax.plot(x, y, color='black', linewidth=1.5)

# ZONA VERDE: Compatível (|Z| <= 2)
ax.fill_between(x, y, where=(abs(x) <= 2), color='green', alpha=0.3, label="Compatível")

# ZONA AMARELA: Indeterminado (2 < |Z| <= 3)
ax.fill_between(x, y, where=((abs(x) > 2) & (abs(x) <= 3)), color='yellow', alpha=0.3, label="Indeterminado")

# ZONA VERMELHA: Incompatível (|Z| > 3)
ax.fill_between(x, y, where=(abs(x) > 3), color='red', alpha=0.3, label="Incompatível")
# Marcação do Z-score calculado pelo experimento
# Colocamos o ponto tanto do lado positivo quanto negativo pois testamos o módulo (bicaudal)
ax.axvline(z_score, color='black', linestyle='--', linewidth=2, label=f"Seu Z' ({z_score:.2f})")

# Estilização do gráfico
ax.set_title("Distribuição do Teste de Compatibilidade (Z-Score)", fontsize=14)
ax.set_xlabel("Z' (Desvios Normalizados)", fontsize=12)
ax.set_ylabel("Densidade de Probabilidade", fontsize=12)
ax.set_yticks([]) # Oculta os números do eixo Y (não importam fisicamente aqui)
ax.legend(loc='upper right')

# Renderiza o gráfico
st.pyplot(fig)