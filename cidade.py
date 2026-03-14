import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Detetive & Assassino", page_icon="🕵️‍♂️", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'jogo_ativo' not in st.session_state:
    st.session_state.jogo_ativo = False
    st.session_state.dados_jogadores = {}
    st.session_state.seletor_jogador = "Jogador 1"

# --- FUNÇÃO CALLBACK: PRÓXIMO JOGADOR ---
def proximo_jogador_callback():
    lista_nomes = list(st.session_state.dados_jogadores.keys())
    nome_atual = st.session_state.seletor_jogador
    
    try:
        indice_atual = lista_nomes.index(nome_atual)
        proximo_indice = (indice_atual + 1) % len(lista_nomes)
        st.session_state.seletor_jogador = lista_nomes[proximo_indice]
    except ValueError:
        st.session_state.seletor_jogador = lista_nomes[0]

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.header("⚙️ Configuração da Partida")
    total = st.number_input("Total de Jogadores", min_value=4, max_value=30, value=8)
    
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        n_assassinos = st.number_input("Assassinos", min_value=1, max_value=total//2, value=1)
        n_detetives = st.number_input("Detetives", min_value=1, max_value=total//2, value=1)
    with col_cfg2:
        n_anjos = st.number_input("Anjos", min_value=1, max_value=total//2, value=1)
        
    # Cálculo automático de cidadãos
    n_cidadaos = total - (n_assassinos + n_detetives + n_anjos)
    
    if n_cidadaos < 0:
        st.error("A soma dos papéis excede o total de jogadores!")
    else:
        st.info(f"Cidadãos restantes: {n_cidadaos}")
        
    if st.button("🚀 Gerar Nova Partida"):
        # Criar a lista de papéis
        papeis = (["ASSASSINO"] * n_assassinos + 
                  ["DETETIVE"] * n_detetives + 
                  ["ANJO"] * n_anjos + 
                  ["CIDADÃO"] * n_cidadaos)
        
        random.shuffle(papeis)
        
        # Gerar IDs dos jogadores e atribuir papéis
        ids_jogadores = [f"Jogador {i+1}" for i in range(total)]
        st.session_state.dados_jogadores = dict(zip(ids_jogadores, papeis))
        
        st.session_state.jogo_ativo = True
        st.session_state.seletor_jogador = ids_jogadores[0]
        st.success("Papéis sorteados! Recolha o menu.")
        st.rerun()

# --- TELA PRINCIPAL ---
st.title("🕵️‍♂️ Detetive, Anjo e Assassino")

if st.session_state.jogo_ativo:
    st.write("### 📢 Distribuição de Papéis")
    st.caption("Cada jogador deve selecionar seu número, ver seu papel e clicar em 'Limpar' antes de passar o celular.")

    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    # Selectbox controlado pelo estado
    escolha = st.selectbox(
        "Quem é você?", 
        options=lista_nomes, 
        key="seletor_jogador"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"👁️ Revelar Papel", key=f"btn_{escolha}"):
            papel = st.session_state.dados_jogadores[escolha]
            
            # Estilização baseada no papel
            if papel == "ASSASSINO":
                st.error(f"🔪 Você é o **{papel}**!")
                st.write("Objetivo: Eliminar todos sem ser descoberto.")
            elif papel == "DETETIVE":
                st.info(f"🔎 Você é o **{papel}**!")
                st.write("Objetivo: Descobrir quem é o assassino.")
            elif papel == "ANJO":
                st.success(f"👼 Você é o **{papel}**!")
                st.write("Objetivo: Proteger alguém de ser eliminado.")
            else:
                st.warning(f"🏠 Você é um **{papel}**!")
                st.write("Objetivo: Sobreviver e ajudar o detetive.")

    with col2:
        st.button("Limpar e Próximo ➡️", on_click=proximo_jogador_callback)

    st.divider()
    with st.expander("📖 Regras Rápidas"):
        st.write("""
        1. **Noite:** O Assassino escolhe alguém para matar, o Anjo escolhe alguém para salvar e o Detetive escolhe alguém para investigar.
        2. **Dia:** Todos discutem quem pode ser o assassino e votam para eliminar alguém.
        """)

else:
    st.warning("Aguardando configuração... Use o menu lateral para definir os jogadores e iniciar!")
