"""Orquestração do agente: loop de chamadas à LLM com streaming e tool calling."""

import json
import os

import streamlit as st
from openai import OpenAI

from templates import template_label
from tools import TOOLS, dispatch_tool

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


FORCE_LOAD_TEMPLATE = {
    "type": "function",
    "function": {"name": "load_template"},
}


@st.cache_resource
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def _template_already_loaded(messages: list) -> bool:
    return any(m.get("role") == "tool" for m in messages)


def _accumulate_tool_call(acc: dict, delta_tc) -> None:
    """Mescla um delta de tool_call no acumulador indexado por `tc.index`."""
    entry = acc.setdefault(
        delta_tc.index, {"id": "", "name": "", "arguments": ""}
    )
    if delta_tc.id:
        entry["id"] = delta_tc.id
    if delta_tc.function:
        if delta_tc.function.name:
            entry["name"] += delta_tc.function.name
        if delta_tc.function.arguments:
            entry["arguments"] += delta_tc.function.arguments


def _build_assistant_message(content: str, tool_calls_acc: dict) -> dict:
    msg: dict = {"role": "assistant", "content": content or None}
    if tool_calls_acc:
        msg["tool_calls"] = [
            {
                "id": tc["id"],
                "type": "function",
                "function": {"name": tc["name"], "arguments": tc["arguments"]},
            }
            for tc in tool_calls_acc.values()
        ]
    return msg


def run_agent_turn(messages: list) -> None:
    """Executa turnos da LLM sobre `messages` (mutado in-place) até não haver mais tool_calls."""
    client = get_client()
    while True:
        tool_choice = "auto" if _template_already_loaded(messages) else FORCE_LOAD_TEMPLATE
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice=tool_choice,
            parallel_tool_calls=False,
            stream=True,
            temperature=0.6,
        )

        content = ""
        tool_calls_acc: dict[int, dict] = {}
        placeholder = None

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            if delta.content:
                if placeholder is None:
                    with st.chat_message("assistant"):
                        placeholder = st.empty()
                content += delta.content
                placeholder.markdown(content + "▌")

            if delta.tool_calls:
                for tc in delta.tool_calls:
                    _accumulate_tool_call(tool_calls_acc, tc)

        if placeholder is not None:
            placeholder.markdown(content)

        messages.append(_build_assistant_message(content, tool_calls_acc))

        if not tool_calls_acc:
            return

        for tc in tool_calls_acc.values():
            try:
                args = json.loads(tc["arguments"] or "{}")
            except json.JSONDecodeError:
                args = {}
            result = dispatch_tool(tc["name"], args)
            messages.append(
                {"role": "tool", "tool_call_id": tc["id"], "content": result}
            )
            if tc["name"] == "load_template" and "option" in args:
                st.caption(
                    f"🔧 Template carregado: **{template_label(args['option'])}**"
                )
