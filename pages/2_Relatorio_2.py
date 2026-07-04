import streamlit as st
import pandas as pd
import numpy as np

u_m = 0.1/(2 * np.sqrt(3))  # Incerteza da balança digital (kg)
massas = {
    "Quantidade": [1, 1, 1, 1],
    "Formato": ["Paralelepípedo", "Cilindro", "Cilindro", "Cilindro"],
    "Material": ["Cu", "Cu", "Al (X)", "Al (1)"],
    "Massa (g)": [1066.09, 836.96, 258.73, 258.55],
    "Incerteza Anotada (g)": [0.03, 0.03, 0.03, 0.03],
    "Incerteza da Balança (g)": [u_m, u_m, u_m, u_m] # Erro calculado anteriormente
}
df_massas = pd.DataFrame(massas)
st.subheader("Massa dos Sólidos")
st.dataframe(
    df_massas,
    use_container_width=True,
    column_config={
        "Massa (g)": st.column_config.NumberColumn(format="%.6f"),
        "Incerteza Anotada (g)": st.column_config.NumberColumn(format="%.2f"),
        "Incerteza da Balança (g)": st.column_config.NumberColumn(format="%.4f"),
    }
)

m1 = massas["Massa (g)"][0]
m2 = massas["Massa (g)"][1]
m3 = massas["Massa (g)"][2]
m4 = massas["Massa (g)"][3]






# ==========================================
# CONFIGURAÇÃO DE VARIÁVEIS E INICIALIZAÇÃO
# ==========================================
st.set_page_config(page_title="Experimento 2 - ESTO017-17", layout="wide")

st.title("ESTO017-17 - Métodos Experimentais em Engenharia")
st.subheader("Experimento 2: Constante Elástica de uma Mola")

# --- DADOS DOS INSTRUMENTOS (EXIBIDOS NA PÁGINA) ---
st.subheader("Dados dos Instrumentos")
st.markdown("Anote para todos instrumentos: marca, fundo de escala, etc.")

col_inst1, col_inst2, col_inst3 = st.columns(3)

with col_inst1:
    res_regua = 0.05    
    st.metric("Menor divisão da Régua (m)", value=0.001, format="%.4f")
with col_inst2:
    res_balanca = 0.0001
    st.metric("Resolução da Balança (kg)", value=0.0001, format="%.5f")
with col_inst3:
    res_cronometro = 0.01
    st.metric("Resolução do Cronômetro (s)", value=0.01, format="%.3f")

u_regua = res_regua / 2  # Incerteza da régua (metade da menor divisão)
u_balanca = res_balanca / (2 * np.sqrt(3))  # Incerteza da balança digital
u_cronometro = res_cronometro / (2 * np.sqrt(3))  # Incerteza do cronômetro digital

# ==========================================
# MÉTODO A - ESTÁTICO
# ==========================================
st.header("Método A: Lei de Hooke (Estático)")

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Posição Inicial da Mola (m)", value=0, format="%.2f")
    st.latex(r"F_0 = 0 \text{ (dinamômetro zerado)}")

with col2:
    st.markdown("**Tabela de Dados (F x Deformação)**")
    # DataFrame inicial vazio para preenchimento pelo usuário    


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
            0.142,    # x0
            0.151,  # x1
            0.161,  # x2
            0.174,  # x3
            0.185,  # x4
            0.195   # x5
        ]
    })


    F_lida = np.array(df_a["Força_Lida_F (N)"])
    x_lido = np.array(df_a["Posição_x (m)"])
    m_adicionada = np.array(df_a["m"]/1000)  # Convertendo para kg
    dm = np.array(df_a["dm"]/1000)  # Convertendo para kg
    # Deformação: delta_x = x - x0
    # Definição do x0 (primeira leitura do array)
    dx0 = x_lido[0]
    dx1 = x_lido[1] - dx0
    dx2 = x_lido[2] - dx0
    dx3 = x_lido[3] - dx0
    dx4 = x_lido[4] - dx0
    dx5 = x_lido[5] - dx0
    delta_x = [dx0, dx1, dx2, dx3, dx4, dx5]    
    
    # Incerteza do Dinamômetro: 0,5% do valor + 0,2 N
    u_dinamometro = (0.005 * F_lida) + 0.2
    
    # Propagação da incerteza para a deformação L = x - x0 -> u_L = sqrt(u_x^2 + u_x0^2)
    u_delta_x = np.sqrt(u_regua**2 + u_regua**2) * np.ones_like(delta_x)
    
    st.write("### Resultados Calculados")
    res_df_a = pd.DataFrame({
        "Força (N)": F_lida,
        "Massa Adicionada (kg)": m_adicionada,
        "delta M (kg)": dm,
        "Incerteza F (N)": u_dinamometro,
        "Deformação Δx (m)": delta_x,
        "Incerteza Δx (m)": u_delta_x
    })
    st.dataframe(res_df_a, use_container_width=True)
    st.info("Utilize os dados acima no LAB Fit para ajustar a reta e obter o valor de K e $\mu_k$.")

res_df_a['k'] = res_df_a['Força (N)'] / res_df_a['Deformação Δx (m)']
res_df_a['k/g'] = res_df_a['delta M (kg)']/ res_df_a['Deformação Δx (m)']
res_df_a['k*'] = res_df_a['k/g'] * 9.81  # Convertendo para N/m
st.dataframe(res_df_a[['k', 'k/g', 'k*']], use_container_width=True, hide_index=True)    


st.divider()

# ==========================================
# MÉTODO B - MHS (DINÂMICO)
# ==========================================
st.header("Método B: Oscilador Harmônico (MHS)")

col_b1, col_b2 = st.columns(2)

with col_b1:
    m_oscilante = 2100.64/1000  # Convertendo para kg
    st.metric("Massa do Oscilador (kg)", value=m_oscilante)
    N_osc = 40
    st.metric("Número de Oscilações (N)", value=N_osc)
    u_operador = 0.2
    st.metric("Incerteza do Operador (s)", value=u_operador)



with col_b2:
    st.markdown("**Medições de Tempo ($T_N$)**")
    tempos_str = [
        23.3,
        24.12,
        21.30,
        21.97]
    

    try:
        t_list = tempos_str
        t_array = np.array(t_list)
        n_medidas = len(t_array)
        
        # Média e incerteza Tipo A
        t_media = np.mean(t_array)
        s_t = np.std(t_array, ddof=1) # Desvio padrão experimental
        u_tipo_A = s_t / np.sqrt(n_medidas) # Incerteza tipo A da amostra
        
        # Incerteza combinada do período
        u_T = np.sqrt(u_tipo_A**2 + u_operador**2 + u_cronometro**2)
        
        # Cálculo de K_B para cada tempo medido
        # k = (4 * pi^2 * m * N^2) / T_N^2
        k_b = [(4 * np.pi**2 * m_oscilante * (N_osc**2)) / (t**2) for t in t_list]
        k_b_media = np.mean(k_b)
        
        # Propagação de incertezas para G = f(m, T_N)
        dk_dm = (4 * np.pi**2 * (N_osc**2)) / (t_media**2)
        dk_dt = -2 * (4 * np.pi**2 * m_oscilante * (N_osc**2)) / (t_media**3)
        
        u_kb = np.sqrt((dk_dm * u_balanca)**2 + (dk_dt * u_T)**2)
        
        st.write("### Resultados Calculados")
        st.latex(rf"\mu_T = \sqrt{{(\mu_{{TIPO\_A}})^2 + (\mu_{{OPERADOR}})^2 + (\mu_{{CRONOMETRO}})^2}}")
        
        st.markdown(f"""
        * **Tempo Médio ($T_N$)**: {t_media:.3f} s
        * **Incerteza Tipo A ($\mu_{{tipo~A}}$)**: {u_tipo_A:.4f} s
        * **Incerteza Combinada ($\mu_T$)**: {u_T:.4f} s
        * **Constantes $k_B$ por tempo**: {', '.join(f'{val:.2f}' for val in k_b)} N/m
        * **Constante $k_B$ média**: {k_b_media:.2f} N/m
        * **Incerteza $u_{{kB}}$**: {u_kb:.2f} N/m
        """)
        
    except ValueError:
        st.error("Por favor, insira apenas números separados por vírgula para os tempos.")

st.divider()

# ==========================================
# VERIFICAÇÃO DE COMPATIBILIDADE (Z-Score)
# ==========================================
st.header("Verificação de Compatibilidade entre Medições")
st.latex(r"Z' = \frac{|V_a - V_b|}{\sqrt{(u_{Va})^2 + (u_{Vb})^2}}")

col_z1, col_z2 = st.columns(2)

with col_z1:
    k_a_input = st.number_input("Valor de k (Método A)", value=0.0)
    uka_input = st.number_input("Incerteza de k (Método A)", value=0.0)

with col_z2:
    try:
        k_b_input = st.number_input("Valor de k (Método B)", value=k_b_media if t_list else 0.0)
        ukb_input = st.number_input("Incerteza de k (Método B)", value=u_kb if t_list else 0.0)
    except NameError:
         k_b_input = st.number_input("Valor de k (Método B)", value=0.0)
         ukb_input = st.number_input("Incerteza de k (Método B)", value=0.0)

if st.button("Calcular Z-Score") and (uka_input > 0 or ukb_input > 0):
    z_score = abs(k_a_input - k_b_input) / np.sqrt(uka_input**2 + ukb_input**2)
    st.subheader(f"Resultado Z-Score: {z_score:.2f}")
    
    if z_score <= 2:
        st.success("Medições compatíveis (Z' <= 2).")
    elif z_score > 3:
        st.error("Medições incompatíveis (Z' > 3).")
    else:
        st.warning("Recomenda-se que as medições sejam refeitas para um melhor diagnóstico (2 < Z' <= 3).")

# Regra de arredondamento inserida como rodapé
st.caption("Nota sobre Incertezas: O arredondamento da incerteza é sempre para cima e deve possuir no máximo 2 algarismos.")