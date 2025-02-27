import streamlit as st
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
        .stButton>button {
            color: white !important;
            background-color: #007BFF !important;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-size: 16px;
        }
        input {
            color: black !important;
            background-color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Tabelas de pontuação com TODAS as faixas etárias
tabela_cintura = {
    "M": [(85, 10), (90, 8), (95, 6), (100, 4), (float("inf"), 2)],
    "F": [(70, 10), (75, 8), (80, 6), (85, 4), (float("inf"), 2)]
}

tabela_flexao_braco = {
    (20, 24): {"M": [(50, 10), (45, 9), (40, 8), (35, 7), (30, 6), (0, 4)], "F": [(40, 10), (35, 9), (30, 8), (25, 7), (20, 6), (0, 4)]},
    (25, 29): {"M": [(48, 10), (43, 9), (38, 8), (33, 7), (28, 6), (0, 4)], "F": [(38, 10), (33, 9), (28, 8), (23, 7), (18, 6), (0, 4)]},
    (30, 34): {"M": [(45, 10), (40, 9), (35, 8), (30, 7), (25, 6), (0, 4)], "F": [(35, 10), (30, 9), (25, 8), (20, 7), (15, 6), (0, 4)]},
    (35, 39): {"M": [(42, 10), (37, 9), (32, 8), (27, 7), (22, 6), (0, 4)], "F": [(32, 10), (27, 9), (22, 8), (17, 7), (12, 6), (0, 4)]},
    (40, 44): {"M": [(40, 10), (35, 9), (30, 8), (25, 7), (20, 6), (0, 4)], "F": [(30, 10), (25, 9), (20, 8), (15, 7), (10, 6), (0, 4)]},
    (45, 49): {"M": [(38, 10), (33, 9), (28, 8), (23, 7), (18, 6), (0, 4)], "F": [(28, 10), (23, 9), (18, 8), (13, 7), (8, 6), (0, 4)]},
    (50, 53): {"M": [(35, 10), (30, 9), (25, 8), (20, 7), (15, 6), (0, 4)], "F": [(25, 10), (20, 9), (15, 8), (10, 7), (5, 6), (0, 4)]}
}

tabela_flexao_tronco = tabela_flexao_braco
tabela_corrida = {
    (20, 24): {"M": [(3000, 10), (2800, 9), (2600, 8), (2400, 7), (2200, 6), (0, 4)], "F": [(2700, 10), (2500, 9), (2300, 8), (2100, 7), (1900, 6), (0, 4)]},
    (25, 29): {"M": [(2900, 10), (2700, 9), (2500, 8), (2300, 7), (2100, 6), (0, 4)], "F": [(2600, 10), (2400, 9), (2200, 8), (2000, 7), (1800, 6), (0, 4)]},
    (30, 34): {"M": [(2800, 10), (2600, 9), (2400, 8), (2200, 7), (2000, 6), (0, 4)], "F": [(2500, 10), (2300, 9), (2100, 8), (1900, 7), (1700, 6), (0, 4)]},
    (35, 39): {"M": [(2700, 10), (2500, 9), (2300, 8), (2100, 7), (1900, 6), (0, 4)], "F": [(2400, 10), (2200, 9), (2000, 8), (1800, 7), (1600, 6), (0, 4)]},
    (40, 44): {"M": [(2600, 10), (2400, 9), (2200, 8), (2000, 7), (1800, 6), (0, 4)], "F": [(2300, 10), (2100, 9), (1900, 8), (1700, 7), (1500, 6), (0, 4)]},
    (45, 49): {"M": [(2500, 10), (2300, 9), (2100, 8), (1900, 7), (1700, 6), (0, 4)], "F": [(2200, 10), (2000, 9), (1800, 8), (1600, 7), (1400, 6), (0, 4)]},
    (50, 53): {"M": [(2400, 10), (2200, 9), (2000, 8), (1800, 7), (1600, 6), (0, 4)], "F": [(2100, 10), (1900, 9), (1700, 8), (1500, 7), (1300, 6), (0, 4)]}
}

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
    st.markdown("### **Você luta como treina!** 💪🔥")
