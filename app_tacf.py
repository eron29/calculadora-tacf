import streamlit as st
import pandas as pd
import os

# Configuração do tema claro
st.set_page_config(page_title="Calculadora TACF - FAB", page_icon="✈", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input, 
        .stSelectbox>div>div>div {
            color: black !important;
            background-color: white !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
            padding: 5px !important;
        }
        .stButton>button {
            color: white !important;
            background-color: #007BFF !important;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Tabela de conceitos globais com os intervalos do Grau Final
conceitos_df = pd.DataFrame({
    "Grau Final": ["9.0 - 10.0", "7.0 - 8.9", "5.0 - 6.9", "3.0 - 4.9", "0.0 - 2.9"],
    "Conceito Global": ["Excelente (E)", "Muito Bom (MB)", "Bom (B)", "Satisfatório (S)", "Insatisfatório (I)"]
})

# Função para determinar o conceito global baseado no Grau Final
def determinar_conceito(grau_final):
    if grau_final >= 9.0:
        return "Excelente (E)"
    elif grau_final >= 7.0:
        return "Muito Bom (MB)"
    elif grau_final >= 5.0:
        return "Bom (B)"
    elif grau_final >= 3.0:
        return "Satisfatório (S)"
    else:
        return "Insatisfatório (I)"

# Interface do Streamlit
st.title("Calculadora TACF - FAB")
st.write("Pontuação baseada na Tabela do Anexo VI da NSCA 54-3.")
st.markdown("[Baixar NSCA 54-3](https://www.sislaer.fab.mil.br/terminalcendoc/Busca/Download?codigoArquivo=4678)", unsafe_allow_html=True)

# Formulário para entrada de dados
with st.form("tacf_form"):
    sexo = st.selectbox("Sexo", ["M", "F"])
    idade = st.number_input("Idade", min_value=20, max_value=53, step=1)
    cintura = st.number_input("Medição da Cintura (cm)", min_value=50.0, max_value=150.0, step=0.1)
    flexao_braco = st.number_input("Flexão de Braço", min_value=0, max_value=100, step=1)
    flexao_tronco = st.number_input("Flexão de Tronco", min_value=0, max_value=100, step=1)
    corrida = st.number_input("Distância Corrida (m)", min_value=0, max_value=5000, step=10)
    submit = st.form_submit_button("Calcular")

if submit:
    # Simulação do cálculo do Grau Final (trocar por sua lógica real)
    grau_final = round((cintura * 0.1 + flexao_braco * 0.2 + flexao_tronco * 0.2 + corrida * 0.1) / 4, 2)
    conceito_global = determinar_conceito(grau_final)

    st.success(f"**Grau Final:** {grau_final:.2f}")
    st.info(f"**Conceito Global:** {conceito_global}")

    # Frase motivacional
    st.markdown("### **Você luta como treina!** 💪🔥")

    # Exibir tabela com os intervalos de Grau Final e Conceito Global
    st.write("### Tabela de Conceitos Globais")
    st.dataframe(conceitos_df, hide_index=True)
