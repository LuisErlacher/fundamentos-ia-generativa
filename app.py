import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompt import SYSTEM_PROMPT

load_dotenv()

st.set_page_config(page_title="Copiloto de Comunicação Interna", page_icon="✉️", layout="centered")

API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not API_KEY:
    st.error("⚠️ Configure a variável `OPENAI_API_KEY` no arquivo `.env` antes de rodar.")
    st.stop()

client = OpenAI(api_key=API_KEY)


def init_thread():
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


if "messages" not in st.session_state:
    init_thread()

with st.sidebar:
    st.title("✉️ Copiloto de Comunicação")
    st.caption("Assistente para e-mails, avisos, resumos e mensagens corporativas.")
    st.divider()
    st.markdown(f"**Modelo:** `{MODEL}`")
    msg_counter = st.empty()
    if st.button("🔄 Resetar thread", use_container_width=True, type="primary"):
        init_thread()
        st.rerun()
    st.divider()
    st.markdown(
        "**Exemplos de prompt:**\n\n"
        "- E-mail formal avisando feriado de 21/04\n"
        "- Resumo de reunião: falamos sobre metas Q2\n"
        "- Mensagem WhatsApp convidando para happy hour\n"
        "- Comunicado sobre nova política de home office"
    )

st.title("Copiloto de Comunicação Interna")
st.caption("Descreva o que você precisa escrever. Eu entrego pronto pra copiar.")

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ex: e-mail formal avisando sobre mudança de horário do RH..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"❌ Erro na chamada à OpenAI: {e}"
            placeholder.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

msg_counter.markdown(f"**Mensagens na thread:** {len(st.session_state.messages) - 1}")
