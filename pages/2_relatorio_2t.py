import streamlit as st
import pandas as pd
import numpy as np

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
res_df_a = res_df_a.drop(index=0)  # Removendo a primeira linha (onde Δx = 0)
media_k = res_df_a['k'].mean()
media_Km = res_df_a['k*'].mean()
st.metric("Média de k (N/m)", f"{media_k:.4f}")
st.metric("Média de k* (N/m)", f"{media_Km:.4f}")

#----------------B------------------------
m_oscilante = 2100.64/1000  # Convertendo para kg
N_osc = 40
u_operador = 0.2
tempos = np.array([ 23.3, 24.12, 21.30, 21.97])
    
st.metric("Massa do Oscilador (kg)", value=m_oscilante)
st.metric("Número de Oscilações (N)", value=N_osc)
st.metric("Incerteza do Operador (s)", value=u_operador)

# Cálculo de K_B para cada tempo medido
# k = (4 * pi^2 * m * N^2) / T_N^2
k_b = [((4 * np.pi**2 * m_oscilante * (N_osc**2)) / (t**2)) for t in tempos]
k_b_media = np.mean(k_b)

res_df_b = pd.DataFrame({
    "Tempo (s)": tempos,
    "k_B (N/m)": k_b
})

st.dataframe(res_df_b,
    use_container_width=True,
    column_config={
        "Tempo (s)": st.column_config.NumberColumn(format="%.2f"),
        "k_B (N/m)": st.column_config.NumberColumn(format="%.4f"),
    }
)

st.metric("massa do oscilador (kg)", value=m_oscilante)
st.metric("Número de Oscilações (N)", value=N_osc)
st.metric("Incerteza do Operador (s)", value=u_operador)
st.metric("Média de k_B (N/m)", f"{k_b_media:.8f}")
        
