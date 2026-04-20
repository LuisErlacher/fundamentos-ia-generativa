"""Catálogo de templates de comunicação interna da Solaris Brasil.

Cada template carrega um `skeleton` literal — texto-alvo com `[PLACEHOLDERS]`
que o agente preenche com os dados do usuário. A ordem das chaves define a
ordem do menu apresentado ao colaborador.
"""

TEMPLATES = {
    "Email formal (interno)": {
        "descricao": "E-mail corporativo interno com abertura, contexto, CTA e assinatura.",
        "campos_requeridos": "assunto, público-alvo, contexto, chamada à ação (com prazo ou link)",
        "skeleton": """**Assunto:** [ASSUNTO CURTO E INFORMATIVO — MÁX. 60 CARACTERES]

Olá, [PÚBLICO-ALVO],

[PARÁGRAFO DE CONTEXTO — 2 a 4 linhas explicando o motivo do e-mail]

[PARÁGRAFO ADICIONAL COM DETALHES OU BULLETS, SE NECESSÁRIO]

**Próximo passo:** [CHAMADA À AÇÃO COM PRAZO OU LINK]

Qualquer dúvida, pode me chamar.

Abraço,
[NOME DO REMETENTE] — [CARGO]""",
    },
    "Comunicado oficial de RH": {
        "descricao": "Comunicado institucional com tom neutro-informativo, aplicável a toda a empresa.",
        "campos_requeridos": "assunto, o que muda, data/vigência, quem é impactado, orientações práticas, canal de contato",
        "skeleton": """**COMUNICADO — [ASSUNTO]**

[PARÁGRAFO DE CONTEXTO EXPLICANDO O MOTIVO DO COMUNICADO — 2 a 3 linhas]

**O que muda:**
- **O quê:** [DESCRIÇÃO]
- **Quando:** [DATA / VIGÊNCIA]
- **Quem é impactado:** [PÚBLICO]
- **Onde se aplica:** [LOCAL / ÁREA]

**Orientações práticas:**
1. [PASSO 1]
2. [PASSO 2]
3. [PASSO 3]

Em caso de dúvidas, procure [CANAL DE CONTATO RH].

Equipe de Comunicação Interna | Solaris Brasil ☀️""",
    },
    "Resumo executivo de reunião": {
        "descricao": "Ata enxuta para compartilhar no Teams/Slack após reuniões.",
        "campos_requeridos": "nome da reunião, data, participantes, decisões, próximos passos (com responsável e prazo), link de material",
        "skeleton": """**📌 Resumo — [NOME DA REUNIÃO]**
**Data:** [DATA] • **Participantes:** [LISTA DE PARTICIPANTES]

**✅ Decisões tomadas**
- [DECISÃO 1]
- [DECISÃO 2]

**🔄 Pontos em aberto / próximos passos**
| Item | Responsável | Prazo |
|---|---|---|
| [AÇÃO 1] | [NOME] | [DATA] |
| [AÇÃO 2] | [NOME] | [DATA] |

**📎 Materiais:** [LINK OU REFERÊNCIA]

— [NOME DO REMETENTE], [CARGO]""",
    },
    "Mensagem para Teams/WhatsApp corporativo": {
        "descricao": "Mensagem curta, direta, emoji pontual, ideal para grupos internos.",
        "campos_requeridos": "canal (Teams/WhatsApp), público, mensagem principal, CTA opcional",
        "skeleton": """Oi, time! 👋

[MENSAGEM PRINCIPAL — 2 a 4 linhas, direto ao ponto]

[CTA OU PERGUNTA FINAL, SE APLICÁVEL]

— [PRIMEIRO NOME DO REMETENTE]""",
    },
    "Aviso de segurança operacional": {
        "descricao": "Aviso direcionado a times de campo/usinas, linguagem firme e clara sobre segurança.",
        "campos_requeridos": "motivo do alerta, procedimentos obrigatórios, responsável SST",
        "skeleton": """**⚠️ ATENÇÃO — SEGURANÇA: [TÍTULO CURTO DO ALERTA]**

[PARÁGRAFO EXPLICANDO O MOTIVO DO ALERTA — o que aconteceu ou o que muda, e por quê]

**Procedimentos obrigatórios:**
1. [AÇÃO OBRIGATÓRIA 1]
2. [AÇÃO OBRIGATÓRIA 2]
3. [AÇÃO OBRIGATÓRIA 3]

**Responsável SST:** [NOME / CONTATO]

**Segurança primeiro. Sempre.**

— [NOME DO REMETENTE], [CARGO]""",
    },
    "Post para mural / canal interno": {
        "descricao": "Post curto e motivacional para canais de engajamento interno.",
        "campos_requeridos": "tema, valor a reforçar, canal, CTA opcional",
        "skeleton": """**[TÍTULO CHAMATIVO] [EMOJI TEMÁTICO]**

[TEXTO DE 3 A 5 LINHAS — motivacional, próximo, reforça valor ou celebração]

[CTA CURTO OU CONVITE, SE APLICÁVEL]

#TimeSolaris #[HASHTAG TEMÁTICA]""",
    },
}

TEMPLATE_NAMES = list(TEMPLATES.keys())

GENERIC_OPTION = len(TEMPLATE_NAMES) + 1


def template_label(option: int) -> str:
    if option == GENERIC_OPTION:
        return "Modo genérico"
    if 1 <= option <= len(TEMPLATE_NAMES):
        return TEMPLATE_NAMES[option - 1]
    return f"Opção {option}"


def _format_menu() -> str:
    lines = [
        f"{i}. **{name}** — {TEMPLATES[name]['descricao']}"
        for i, name in enumerate(TEMPLATE_NAMES, 1)
    ]
    lines.append(
        f"{GENERIC_OPTION}. **Outro / genérico** — me descreva livremente o que precisa."
    )
    return "\n".join(lines)


def _format_tool_option_hint() -> str:
    parts = [f"{i}={name}" for i, name in enumerate(TEMPLATE_NAMES, 1)]
    parts.append(f"{GENERIC_OPTION}=Genérico (pedido fora do catálogo)")
    return ", ".join(parts)


TEMPLATE_MENU = _format_menu()
TOOL_OPTION_HINT = _format_tool_option_hint()


GENERIC_INSTRUCTIONS = """**Modo genérico ativado.** O pedido do colaborador não se encaixa nos 6 templates do catálogo.

**Dados a coletar antes de redigir:**
- Qual canal? (e-mail, mensagem de grupo, comunicado, post, outro)
- Quem é o público-alvo?
- Qual o assunto principal?
- Detalhes essenciais (datas, decisões, links, restrições)
- Tom desejado (padrão: profissional-caloroso)

**Regras de redação:**
- Use markdown com estrutura adequada ao canal escolhido.
- Mantenha o tom profissional-caloroso da Solaris Brasil.
- Respeite todos os guardrails (LGPD, escopo, veracidade, confidencialidade).
- Assine com `[NOME DO REMETENTE] — [CARGO]` (você já conhece os dados do usuário desta sessão).
- Se o pedido ficou próximo de um template do catálogo, sugira no final: "Se preferir, posso refazer no formato de [template X]."
- Se o usuário não forneceu algum dado essencial, use placeholders `[ENTRE COLCHETES]` — não invente."""


LOAD_TEMPLATE_RESPONSE = """**Template carregado: {name}**

{descricao}

**Campos a coletar do usuário (faça até 2 rodadas de perguntas):**
{campos_requeridos}

**Skeleton literal a preencher — mantenha estrutura, títulos e ordem EXATOS, substitua apenas os `[PLACEHOLDERS]`:**

```
{skeleton}
```

**Regras deste template:**
- Se o usuário não forneceu algum dado, mantenha o `[PLACEHOLDER]` literal no texto final. NÃO invente.
- Personalize `[NOME DO REMETENTE]` e `[CARGO]` com os dados do usuário desta sessão.
- Não altere a estrutura, títulos ou ordem das seções.
- Depois de entregar, ofereça ajustes (mais curto, mais formal, outro tom)."""
