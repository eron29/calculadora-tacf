import streamlit as st

# Configuração do tema escuro
st.set_page_config(page_title="Calculadora TACF - FAB", page_icon="✈", layout="centered")
st.markdown("""
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
    """, unsafe_allow_html=True)

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
        (40, 49): {"M": [(40, 10), (35, 9), (30, 8), (25, 7), (20, 6), (0, 4)], "F": [(30, 10), (25, 9), (20, 8), (15, 7), (10, 6), (0, 4)]},
        (50, 53): {"M": [(35, 10), (30, 9), (25, 8), (20, 7), (15, 6), (0, 4)], "F": [(25, 10), (20, 9), (15, 8), (10, 7), (5, 6), (0, 4)]}
    }
    
    tabela_flexao_tronco = tabela_flexao_braco
    tabela_corrida = {
        (20, 53): {"M": [(3000, 10), (2800, 9), (2600, 8), (2400, 7), (2200, 6), (0, 4)], "F": [(2700, 10), (2500, 9), (2300, 8), (2100, 7), (1900, 6), (0, 4)]}
    }
    
    faixa_idade = next(faixa for faixa in tabela_flexao_braco if faixa[0] <= idade <= faixa[1])
    pontos_cintura = next(p for l, p in tabela_cintura[sexo] if cintura <= l)
    pontos_flexao_braco = next(p for l, p in tabela_flexao_braco[faixa_idade][sexo] if flexao_braco >= l)
    pontos_flexao_tronco = next(p for l, p in tabela_flexao_tronco[faixa_idade][sexo] if flexao_tronco >= l)
    pontos_corrida = next(p for l, p in tabela_corrida[faixa_idade][sexo] if corrida >= l)
    
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

if st.button("Calcular"):
    grau_final, conceito_global = calcular_tacf(sexo, idade, cintura, flexao_braco, flexao_tronco, corrida)
    st.write(f"**Grau Final:** {grau_final:.2f}")
    st.write(f"**Conceito Global:** {conceito_global}")
    st.markdown("## VOCÊ LUTA COMO TREINOU!  SELVA BRASIL!")

if "contador" not in st.session_state:
    st.session_state["contador"] = 0
st.session_state["contador"] += 1
st.write(f"Número de acessos: {st.session_state['contador']}")
