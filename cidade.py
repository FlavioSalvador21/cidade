import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cidade Dorme: Host & Papéis", page_icon="⚖️", layout="centered")

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
    
    st.divider()
    st.subheader("👥 Definição de Papéis")
    
    # Prefeito é fixo em 1
    st.write("📌 **Prefeito/Host:** 1 (Fixo)")
    
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        n_assassinos = st.number_input("Assassinos", min_value=1, max_value=total//2, value=1)
        n_detetives = st.number_input("Detetives", min_value=1, max_value=total//2, value=1)
    with col_cfg2:
        n_anjos = st.number_input("Anjos", min_value=1, max_value=total//2, value=1)
        
    # Cálculo automático de cidadãos (Total - papéis especiais - 1 do Prefeito)
    n_cidadaos = total - (n_assassinos + n_detetives + n_anjos + 1)
    
    if n_cidadaos < 0:
        st.error("⚠️ Erro: A soma excede o total!")
    else:
        st.info(f"🏠 Cidadãos restantes: {n_cidadaos}")
        
    if st.button("🚀 Gerar Nova Partida"):
        # Criar a lista de papéis (incluindo exatamente UM prefeito)
        papeis = (["PREFEITO (HOST)"] * 1 + 
                  ["ASSASSINO"] * n_assassinos + 
                  ["DETETIVE"] * n_detetives + 
                  ["ANJO"] * n_anjos + 
                  ["CIDADÃO"] * n_cidadaos)
        
        # Embaralhar para ninguém saber quem é o prefeito ou assassino
        random.shuffle(papeis)
        
        # Gerar IDs dos jogadores e atribuir papéis
        ids_jogadores = [f"Jogador {i+1}" for i in range(total)]
        st.session_state.dados_jogadores = dict(zip(ids_jogadores, papeis))
        
        st.session_state.jogo_ativo = True
        st.session_state.seletor_jogador = ids_jogadores[0]
        st.success("Partida Gerada!")
        st.rerun()

# --- TELA PRINCIPAL ---
st.title("🏙️ Cidade Dorme")

if st.session_state.jogo_ativo:
    st.write(f"### 📢 Vez de: **{st.session_state.seletor_jogador}**")
    st.caption("Veja seu papel e limpe a tela antes de passar para o próximo.")

    lista_nomes = list(st.session_state.dados_jogadores.keys())
    
    escolha = st.selectbox(
        "Selecione seu número:", 
        options=lista_nomes, 
        key="seletor_jogador"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"👁️ Revelar Papel", key=f"btn_{escolha}"):
            papel = st.session_state.dados_jogadores[escolha]
            
            # Estilização baseada no papel
            if papel == "PREFEITO (HOST)":
                st.subheader(f"🏛️ Você é o {papel}!")
                st.write("Sua função é mediar o jogo, narrar a noite e organizar as votações.")
                
            elif papel == "ASSASSINO":
                st.error(f"🔪 Você é o **{papel}**!")
                st.write("Objetivo: Eliminar todos sem ser descoberto.")
                
            elif papel == "DETETIVE":
                st.info(f"🔎 Você é o **{papel}**!")
                st.write("Objetivo: Investigar um jogador por noite para saber seu papel.")
                
            elif papel == "ANJO":
                st.success(f"👼 Você é o **{papel}**!")
                st.write("Objetivo: Escolher uma pessoa para proteger da morte nesta noite.")
                
            else:
                st.warning(f"🏠 Você é um **{papel}**!")
                st.write("Objetivo: Sobreviver e votar corretamente para expulsar o assassino.")

    with col2:
        st.button("Limpar e Próximo ➡️", on_click=proximo_jogador_callback)

    st.divider()
    
else:
    st.warning("Aguardando configuração... Use o menu lateral para começar!")
