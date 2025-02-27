import streamlit as st

# Configuração do tema escuro
st.set_page_config(page_title="Calculadora TACF - FAB", page_icon="✈", layout="centered")
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton>button {
            color: white;
            background-color: #6200ea;
        }
        .stNumberInput>div>input {
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para calcular o TACF
def calcular_tacf(sexo: str, idade: int, cintura: float, flexao_braco: int, flexao_tronco: int, corrida: int):
    """
    Calcula o Conceito Global do TACF de acordo com a Tabela de Pontos do Anexo VI da NSCA 54-3 (2024).
    """
    
    tabela_cintura = {
        "M": [(85, 10), (90, 8), (95, 6), (100, 4), (float("inf"), 2)],
        "F": [(70, 10), (75, 8), (80, 6), (85, 4), (float("inf"), 2)]
    }
    
    tabela_flexao_braco = {
        (20, 29): {"M": [(50, 10), (45, 9), (40, 8), (35, 7), (30, 6), (0, 4)], "F": [(40, 10), (35, 9), (30, 8), (25, 7), (20, 6), (0, 4)]},
        (30, 39): {"M": [(45, 10), (40, 9), (35, 8), (30, 7), (25, 6), (0, 4)], "F": [(35, 10), (30, 9), (25, 8), (20, 7), (15, 6), (0, 4)]},
        (40, 49): {"M": [(40, 10), (35, 9), (30, 8), (25, 7), (20, 6), (0, 4)], "F": [(30, 10), (25, 9), (20, 8), (15, 7), (10, 6), (0, 4)]}
    }
    
    tabela_flexao_tronco = tabela_flexao_braco
    tabela_corrida = {
        (20, 29): {"M": [(3000, 10), (2800, 9), (2600, 8), (2400, 7), (2200, 6), (0, 4)], "F": [(2700, 10), (2500, 9), (2300, 8), (2100, 7), (1900, 6), (0, 4)]},
        (30, 39): {"M": [(2800, 10), (2600, 9), (2400, 8), (2200, 7), (2000, 6), (0, 4)], "F": [(2500, 10), (2300, 9), (2100, 8), (1900, 7), (1700, 6), (0, 4)]},
        (40, 49): {"M": [(2600, 10), (2400, 9), (2200, 8), (2000, 7), (1800, 6), (0, 4)], "F": [(2300, 10), (2100, 9), (1900, 8), (1700, 7), (1500, 6), (0, 4)]}
    }
    
    # Cálculo dos pontos para cintura
    def get_pontos_cintura(tabela, sexo, valor):
        for limite, pontos in tabela[sexo]:
            if valor <= limite:
                return pontos
        return 0

    pontos_cintura = get_pontos_cintura(tabela_cintura, sexo, cintura)

    # Cálculo dos pontos para os outros testes
    def get_pontos(tabela, idade, sexo, valor):
        for faixa, pontuacoes in tabela.items():
            if faixa[0] <= idade <= faixa[1]:
                for limite, pontos in pontuacoes[sexo]:
                    if valor >= limite:
                        return pontos
        return 0
    
    pontos_flexao_braco = get_pontos(tabela_flexao_braco, idade, sexo, flexao_braco)
    pontos_flexao_tronco = get_pontos(tabela_flexao_tronco, idade, sexo, flexao_tronco)
    pontos_corrida = get_pontos(tabela_corrida, idade, sexo, corrida)
    
    grau_final = (pontos_cintura + pontos_flexao_braco + pontos_flexao_tronco + pontos_corrida) / 4
    
    conceito_tabela = {
        (9, float("inf")): "Excelente (E)",
        (7, 9): "Muito Bom (MB)",
        (5, 7): "Bom (B)",
        (3, 5): "Satisfatório (S)",
        (0, 3): "Insatisfatório (I)"
    }
    
    conceito_global = next(v for k, v in conceito_tabela.items() if k[0] <= grau_final < k[1])
    
    return grau_final, conceito_global

# Interface do Streamlit
st.title("Calculadora TACF - FAB")
st.write("Pontuação baseada na Tabela de Pontos do Anexo VI da NSCA 54-3 de 2025")
st.download_button("Baixar NSCA 54-3", "./NSCA_54-3.pdf")

# Entradas do usuário
sexo = st.selectbox("Sexo", ["M", "F"])
idade = st.number_input("Idade", min_value=20, max_value=49, step=1)
cintura = st.number_input("Medição da Cintura (cm)", min_value=50.0, max_value=150.0, step=0.1)
flexao_braco = st.number_input("Flexão de Braço", min_value=0, max_value=100, step=1)
flexao_tronco = st.number_input("Flexão de Tronco", min_value=0, max_value=100, step=1)
corrida = st.number_input("Distância Corrida (m)", min_value=0, max_value=5000, step=10)

if st.button("Calcular"):
    grau_final, conceito_global = calcular_tacf(sexo, idade, cintura, flexao_braco, flexao_tronco, corrida)
    st.write(f"**Grau Final:** {grau_final:.2f}")
    st.write(f"**Conceito Global:** {conceito_global}")
    st.markdown("## VOCÊ LUTA COMO TREINOU!  SELVA BRASIL!")

if "contador" not in st.session_state:
    st.session_state["contador"] = 0
st.session_state["contador"] += 1
st.write(f"Número de acessos: {st.session_state['contador']}")
