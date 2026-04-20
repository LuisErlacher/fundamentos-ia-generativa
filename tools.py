from templates import (
    GENERIC_INSTRUCTIONS,
    GENERIC_OPTION,
    LOAD_TEMPLATE_RESPONSE,
    TEMPLATE_NAMES,
    TEMPLATES,
    TOOL_OPTION_HINT,
    template_label,
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "load_template",
            "description": (
                "Carrega o template e as instruções de preenchimento para a opção "
                "escolhida pelo colaborador. Chame ASSIM QUE identificar qual "
                "template o usuário quer (por número, nome ou descrição). É "
                "obrigatório chamar esta função antes de tentar redigir o texto — "
                "você não conhece o skeleton até recebê-lo via esta função."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "option": {
                        "type": "integer",
                        "description": f"Número da opção escolhida. {TOOL_OPTION_HINT}.",
                        "minimum": 1,
                        "maximum": GENERIC_OPTION,
                    },
                },
                "required": ["option"],
                "additionalProperties": False,
            },
        },
    },
]


def execute_load_template(option: int) -> str:
    if option == GENERIC_OPTION:
        return GENERIC_INSTRUCTIONS

    name = template_label(option)
    if name not in TEMPLATES:
        return f"Opção inválida: {option}. Peça ao usuário para escolher de 1 a {GENERIC_OPTION}."

    tpl = TEMPLATES[name]
    return LOAD_TEMPLATE_RESPONSE.format(
        name=name,
        descricao=tpl["descricao"],
        campos_requeridos=tpl["campos_requeridos"],
        skeleton=tpl["skeleton"],
    )


def dispatch_tool(name: str, args: dict) -> str:
    if name == "load_template":
        return execute_load_template(int(args.get("option", 0)))
    return f"Tool desconhecida: {name}"
