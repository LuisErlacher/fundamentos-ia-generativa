import os

import streamlit as st
from dotenv import load_dotenv

from agent import MODEL, run_agent_turn
from prompts import build_system_prompt, build_welcome_message

load_dotenv()

st.set_page_config(
    page_title="Copiloto Solaris Brasil",
    page_icon="☀️",
    layout="centered",
)

if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ Configure a variável `OPENAI_API_KEY` no arquivo `.env` antes de rodar.")
    st.stop()


def reset_session() -> None:
    for key in ("nome", "cargo", "messages"):
        st.session_state.pop(key, None)


def identificado() -> bool:
    return bool(st.session_state.get("nome")) and bool(st.session_state.get("cargo"))


def start_conversation(nome: str, cargo: str) -> None:
    st.session_state.nome = nome
    st.session_state.cargo = cargo
    st.session_state.messages = [
        {"role": "system", "content": build_system_prompt(nome, cargo)},
        {"role": "assistant", "content": build_welcome_message(nome)},
    ]


def render_sidebar() -> None:
    with st.sidebar:
        st.title("☀️ Solaris Brasil")
        st.caption("Copiloto de Comunicação Interna — RH & Comunicação")
        st.divider()
        st.markdown(f"**Modelo:** `{MODEL}`")
        if identificado():
            st.markdown(f"**Colaborador:** {st.session_state.nome}")
            st.markdown(f"**Cargo:** {st.session_state.cargo}")
            st.caption(f"Mensagens na thread: {len(st.session_state.messages) - 1}")
            st.divider()
            if st.button("🔄 Nova sessão", use_container_width=True, type="primary"):
                reset_session()
                st.rerun()
        st.divider()
        st.caption(
            "Este assistente segue guardrails explícitos de LGPD, "
            "confidencialidade e escopo corporativo. Templates carregados "
            "sob demanda via tool calling — zero contaminação entre sessões."
        )


def render_identification_form() -> None:
    st.subheader("👋 Antes de começar, se identifica")
    st.caption(
        "Seus dados ficam apenas nesta sessão do navegador. "
        "Usados só pra personalizar saudações e assinaturas."
    )
    with st.form("identificacao", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            nome_input = st.text_input("Seu nome completo *", placeholder="Ex: Ana Ribeiro")
        with col2:
            cargo_input = st.text_input(
                "Seu cargo / departamento *",
                placeholder="Ex: Analista de RH Sr.",
            )
        submitted = st.form_submit_button(
            "Entrar no copiloto →", type="primary", use_container_width=True
        )

    if submitted:
        if not nome_input.strip() or not cargo_input.strip():
            st.error("Preenche nome e cargo pra continuar.")
        else:
            start_conversation(nome_input.strip(), cargo_input.strip())
            st.rerun()


def render_history() -> None:
    for msg in st.session_state.messages:
        role = msg["role"]
        if role in ("system", "tool"):
            continue
        if role == "assistant" and not msg.get("content"):
            continue
        with st.chat_message(role):
            st.markdown(msg["content"])


render_sidebar()

st.title("Copiloto de Comunicação Interna")
st.caption("Solaris Brasil — Energia Renovável • RH & Comunicação")

if not identificado():
    render_identification_form()
    st.stop()

render_history()

if user_input := st.chat_input("Responde com número, nome do template ou descreva livremente..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    run_agent_turn(st.session_state.messages)
