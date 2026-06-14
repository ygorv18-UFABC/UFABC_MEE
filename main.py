import streamlit as st

# Configuração inicial da página (deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="Métodos Experimentais",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Métodos Experimentais em Engenharia")
st.write("---")

st.markdown("""
### Bem-vindo ao aplicativo de análise de dados!
Este aplicativo foi desenvolvido para visualizar as tabelas e os gráficos dos experimentos realizados na disciplina.

**Navegação:**
Utilize o menu lateral esquerdo para acessar as páginas (abas) de cada relatório.

**Ferramentas utilizadas:**
* **Pandas:** Manipulação de tabelas de dados.
* **Streamlit:** Criação da interface e gráficos nativos.
""")

st.info("👈 Selecione um relatório no menu ao lado para começar.")