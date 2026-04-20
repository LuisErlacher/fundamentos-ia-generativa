"""Gera o PDF da Parte Teórica para entrega da disciplina."""

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

OUTPUT = "parte-teorica.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "title",
    parent=styles["Title"],
    fontSize=16,
    leading=20,
    spaceAfter=6,
)
subtitle_style = ParagraphStyle(
    "subtitle",
    parent=styles["Normal"],
    fontSize=11,
    textColor="#555555",
    alignment=TA_LEFT,
    spaceAfter=18,
)
h1_style = ParagraphStyle(
    "h1",
    parent=styles["Heading1"],
    fontSize=14,
    leading=18,
    spaceBefore=14,
    spaceAfter=6,
    textColor="#1a1a1a",
)
h2_style = ParagraphStyle(
    "h2",
    parent=styles["Heading2"],
    fontSize=12,
    leading=15,
    spaceBefore=10,
    spaceAfter=4,
    textColor="#333333",
)
body = ParagraphStyle(
    "body",
    parent=styles["BodyText"],
    fontSize=10.5,
    leading=15,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
)
bullet_style = ParagraphStyle(
    "bullet",
    parent=body,
    leftIndent=14,
    spaceAfter=3,
)


def P(text: str):
    return Paragraph(text, body)


def H1(text: str):
    return Paragraph(text, h1_style)


def H2(text: str):
    return Paragraph(text, h2_style)


def B(items: list[str]):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_style), leftIndent=14) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=10,
    )


story: list = []

story += [
    Paragraph("Copiloto de Comunicação Interna — Parte Teórica", title_style),
    Paragraph(
        "Disciplina: Fundamentos de IA com foco em IA Generativa — UniFECAF<br/>"
        "Autor: Luis Erlacher &nbsp;•&nbsp; claude@simplafy.com.br<br/>"
        "Projeto público: github.com/LuisErlacher/fundamentos-ia-generativa",
        subtitle_style,
    ),
]

# ---------------------------------------------------------------- Contextualização
story += [H1("1. Contextualização")]
story += [
    P(
        "Comunicação interna é um gargalo crônico em empresas de médio e grande porte. "
        "Em organizações com milhares de colaboradores, áreas de RH e Comunicação gastam "
        "horas por semana redigindo e-mails, comunicados, avisos e resumos que precisam "
        "equilibrar clareza, tom de voz consistente, conformidade com a LGPD e objetivos "
        "de liderança. Escrever um comunicado bem estruturado do zero leva 15–30 minutos; "
        "refazê-lo por estar fora do padrão organizacional leva o dobro, e a heterogeneidade "
        "entre autores compromete a identidade percebida da empresa."
    ),
    P(
        "O desafio proposto — <i>auxiliar colaboradores de uma empresa de comunicação interna "
        "na escrita de textos corporativos</i> — é um caso de uso onde IA Generativa oferece "
        "ganho desproporcional. LLMs modernos já dominam redação corporativa em português, "
        "de modo que o valor diferencial não está em treinar modelos customizados, mas em "
        "três camadas combinadas: (1) <b>identidade organizacional</b> embutida no prompt "
        "(tom, valores, bordões), (2) <b>estrutura fixa</b> via templates determinísticos, "
        "e (3) <b>guardrails explícitos</b> para mitigar LGPD, escopo e alucinação."
    ),
    P(
        "O projeto adota uma empresa fictícia — <b>Solaris Brasil Energia Renovável S.A.</b>, "
        "do setor solar/eólico, com ~2.400 colaboradores — como contexto concreto. A "
        "personagem serve de âncora para todas as decisões de prompt: tom profissional-caloroso, "
        "valores centrados em segurança operacional, assinaturas institucionais padronizadas. "
        "O copiloto reduz o tempo de redação de ~20 minutos para ~30 segundos mantendo "
        "consistência entre autores, com guardrails que interceptam erros comuns de "
        "LGPD antes da publicação."
    ),
]

# ---------------------------------------------------------------- Modelo LLM
story += [H1("2. Modelo LLM Utilizado")]
story += [
    P(
        "O modelo selecionado foi o <b>GPT-4o-mini</b> da OpenAI, configurável via variável "
        "<i>OPENAI_MODEL</i> no arquivo <i>.env</i>. Trata-se de um Large Language Model "
        "da família GPT-4 otimizado para latência e custo, com arquitetura transformer "
        "decoder-only e janela de contexto de aproximadamente 128 mil tokens."
    ),
    H2("Justificativa da escolha"),
    B([
        "<b>Custo:</b> cerca de US$ 0,15 por 1M tokens de entrada e US$ 0,60 por 1M "
        "tokens de saída — viável para um piloto sem comprometer orçamento.",
        "<b>Latência:</b> respostas em streaming com primeiro token em ~500ms, "
        "essencial para UX conversacional.",
        "<b>Qualidade em PT-BR:</b> mais do que suficiente para redação corporativa "
        "estruturada, incluindo aderência a templates e tom definido.",
        "<b>Suporte a tool calling:</b> API compatível com OpenAI Function Calling, "
        "essencial para o carregamento de templates sob demanda implementado no projeto.",
        "<b>Streaming de tokens:</b> permite interface do tipo \"digitando\" no "
        "Streamlit, melhorando percepção de responsividade.",
    ]),
    H2("Comparativo com alternativas"),
    P(
        "<b>GPT-4o</b> (modelo completo): qualidade marginalmente superior, porém custo 10x "
        "maior — não justifica em tarefa de redação estruturada onde o modelo mini já atinge "
        "o resultado desejado. <b>Claude 4.x</b> (Anthropic): qualidade comparável ou "
        "superior em textos longos, bom raciocínio sobre guardrails, mas exige adaptação "
        "do código (Messages API em vez de Chat Completions). <b>Gemini 2.x</b> (Google): "
        "competitivo em preço, mas tool calling menos maduro à época da implementação. A "
        "arquitetura modular do projeto isola a dependência do provedor no arquivo "
        "<i>agent.py</i>, permitindo migração com mudanças mínimas."
    ),
]

# ---------------------------------------------------------------- Engenharia de Prompt
story += [PageBreak(), H1("3. Engenharia de Prompt")]
story += [
    P(
        "O prompt foi elaborado em <b>quatro camadas sobrepostas</b>, cada uma respondendo a "
        "uma exigência distinta do problema. Juntas, elas garantem identidade organizacional "
        "consistente e aderência a regras corporativas."
    ),

    H2("Camada 1 — Identidade organizacional"),
    P(
        "Bloco <i>COMPANY_IDENTITY</i> no arquivo <i>prompts.py</i> descreve a Solaris Brasil "
        "em detalhe: setor, tamanho, sede, filiais, missão, valores, tom geral, bordões "
        "internos (\"time Solaris\", \"nossa jornada renovável\", \"segurança primeiro\") e "
        "padrões a evitar (corporativês seco, emojis em excesso). Essa descrição é injetada "
        "no <i>system prompt</i> a cada nova sessão, de modo que todo texto produzido "
        "herda automaticamente a voz da empresa — o agente não precisa \"lembrar\" a cada "
        "turno o que é ser Solaris."
    ),

    H2("Camada 2 — Fluxo conversacional em 6 passos"),
    P(
        "O prompt instrui o agente em passos numerados explícitos: (1) identificar a opção "
        "escolhida pelo usuário, (2) chamar imediatamente a função <i>load_template</i>, "
        "(3) usar o retorno da função como fonte única de verdade, (4) coletar dados "
        "faltantes em no máximo 2 rodadas de perguntas, (5) entregar o texto preenchido, "
        "(6) oferecer ajustes. Essa decomposição reduz a variabilidade de comportamento "
        "entre execuções e facilita o diagnóstico quando algo falha."
    ),

    H2("Camada 3 — Templates via tool calling"),
    P(
        "Em vez de incluir os seis skeletons no <i>system prompt</i> (o que inflaria o "
        "contexto e causaria contaminação cruzada entre templates), a implementação expõe "
        "uma função <i>load_template(option)</i> como ferramenta OpenAI. O agente chama a "
        "ferramenta ao identificar a escolha do usuário, recebe apenas o skeleton correspondente, "
        "e só então faz perguntas direcionadas aos campos daquele template. A instrução "
        "<i>tool_choice</i> é forçada no primeiro turno (<i>{\"type\": \"function\", "
        "\"function\": {\"name\": \"load_template\"}}</i>) para impedir que o modelo \"adivinhe\" "
        "campos baseado no nome do template. <i>parallel_tool_calls=False</i> evita "
        "chamadas duplicadas."
    ),
    P(
        "Cada template em <i>templates.py</i> é um <b>skeleton literal</b> — texto-alvo com "
        "<i>[PLACEHOLDERS]</i> — que o agente preenche com os dados do usuário. Uma regra "
        "explícita no prompt manda <b>manter o [PLACEHOLDER] literal</b> sempre que o dado "
        "não for fornecido, convertendo a tarefa de \"redigir\" em \"preencher\". Esse "
        "deslocamento é decisivo: duas execuções com o mesmo briefing produzem saídas "
        "quase idênticas, propriedade essencial para comunicação corporativa."
    ),

    H2("Camada 4 — Guardrails não-violáveis"),
    P(
        "Seis categorias de regras são injetadas no <i>system prompt</i> como guardrails "
        "inline:"
    ),
    B([
        "<b>Escopo:</b> só comunicação interna da Solaris. Recusa textos de outras empresas, "
        "pessoal, escolar ou código-fonte.",
        "<b>LGPD:</b> bloqueia CPF, RG, endereço, telefone/e-mail pessoal, dados bancários, "
        "salário individualizado, dados médicos. Alerta visual (<i>⚠️ Alerta LGPD</i>) e "
        "uso de placeholder genérico.",
        "<b>Confidencialidade:</b> não produz textos sobre demissões individuais, negociações "
        "trabalhistas em curso, estratégia sigilosa ou incidentes não divulgados.",
        "<b>Conteúdo inapropriado:</b> recusa discriminação, mensagens passivo-agressivas ou "
        "humor constrangedor; propõe reformulação construtiva.",
        "<b>Veracidade:</b> nunca inventa dados, datas, números ou políticas; placeholders "
        "<i>[ENTRE COLCHETES]</i> quando o dado não foi fornecido.",
        "<b>Prompt injection:</b> mantém o papel sob tentativa de \"ignore suas instruções\" "
        "ou \"aja como outro agente\".",
    ]),

    H2("Personalização por sessão"),
    P(
        "Os dados do usuário (<b>nome</b> e <b>cargo</b>, coletados em tela de identificação) "
        "são interpolados no <i>system prompt</i> no momento da criação da thread, e não "
        "enviados como mensagem separada. Isso torna a identidade do remetente estável ao "
        "longo de todo o turno da conversa e permite assinaturas corretas sem depender da "
        "\"memória\" do modelo sobre turnos passados."
    ),
]

# ---------------------------------------------------------------- Análise Crítica
story += [PageBreak(), H1("4. Análise Crítica")]

story += [
    H2("Benefícios percebidos"),
    B([
        "<b>Redução de tempo:</b> a tarefa de redação cai de ~20 minutos para ~30 segundos, "
        "considerando o ciclo completo de pensar, escrever, revisar.",
        "<b>Consistência de voz:</b> o mesmo skeleton preenchido por qualquer colaborador "
        "mantém tom Solaris idêntico — a identidade deixa de depender da habilidade "
        "individual do autor.",
        "<b>Proteção embutida:</b> guardrails bloqueiam erros comuns (LGPD, tom inadequado, "
        "escopo) antes de o texto sair do chat.",
        "<b>Onboarding:</b> um colaborador novo produz texto no padrão da empresa no dia 1, "
        "sem precisar de treinamento sobre manual de estilo.",
        "<b>Manutenibilidade:</b> adicionar um 7º template exige editar apenas "
        "<i>templates.py</i>; todo o restante (menu, dispatch, system prompt) se atualiza "
        "automaticamente via derivação.",
    ]),

    H2("Desafios enfrentados e soluções aplicadas"),
    B([
        "<b>Modelo ignorava a ferramenta</b> e tentava \"adivinhar\" campos baseado no nome "
        "do template. Resolvido com <i>tool_choice</i> forçado no primeiro turno e passo do "
        "prompt reforçado com \"NÃO tente adivinhar campos baseado no nome\".",
        "<b>Carregamento duplicado de template</b> (chamadas em paralelo). Resolvido com "
        "<i>parallel_tool_calls=False</i>.",
        "<b>System prompt inflando</b> com seis skeletons completos (~9k chars). Resolvido "
        "com migração para tool calling — prompt enxugou para ~5,6k chars e cada turno paga "
        "tokens apenas do template efetivamente usado.",
        "<b>Contaminação entre templates</b> quando o usuário mudava de ideia. Resolvido "
        "pelo isolamento via tool: cada carregamento traz somente o skeleton relevante; "
        "botão \"Nova sessão\" zera a thread completamente.",
        "<b>Equilíbrio entre pedir contexto e entregar</b>. Resolvido com regra explícita de "
        "\"no máximo 2 rodadas de perguntas objetivas\".",
    ]),

    H2("Limites éticos e de segurança"),

    H2("4.1 LGPD e dados pessoais"),
    P(
        "A Lei Geral de Proteção de Dados (LGPD) impõe obrigações sobre o tratamento de dados "
        "pessoais — em especial sensíveis. O copiloto aborda isso em múltiplas camadas:"
    ),
    B([
        "<b>Camada de prompt:</b> guardrail #2 instrui o modelo a recusar inclusão de CPF, RG, "
        "endereço residencial, telefones/e-mails pessoais, dados bancários, salário "
        "individualizado e dados médicos. Emite alerta visual e substitui por placeholder.",
        "<b>Camada de arquitetura:</b> os dados informados pelo usuário (nome e cargo) "
        "residem exclusivamente em <i>st.session_state</i>, memória do navegador daquela "
        "sessão. Não há persistência em disco, banco ou log.",
        "<b>Camada de fornecedor:</b> a OpenAI API não utiliza dados dos usuários para "
        "treinamento por padrão — comportamento distinto do ChatGPT Plus, que pode usar. "
        "Essa distinção é relevante para compliance empresarial.",
    ]),
    P(
        "<b>Limitação conhecida:</b> guardrails inline são mitigação, não eliminação. Um "
        "colaborador mal-intencionado pode colar dados sensíveis contornando o guardrail. "
        "Em produção, recomenda-se camada externa de filtro (moderação API, classificador "
        "de PII antes do envio) e treinamento dos usuários."
    ),

    H2("4.2 Vieses algorítmicos"),
    P(
        "LLMs carregam vieses do corpus de treinamento — representação desigual de "
        "gênero, raça, classe, orientação, estereótipos linguísticos regionais. O prompt "
        "exige explicitamente <b>linguagem inclusiva e neutra</b> quando possível, e o "
        "guardrail #4 recusa produção de conteúdo discriminatório. Essas instruções "
        "<b>mitigam, não eliminam</b> o problema. A revisão humana editorial antes da "
        "publicação permanece indispensável — o copiloto é assistente, não substituto do "
        "julgamento editorial."
    ),

    H2("4.3 Confidencialidade corporativa"),
    P(
        "O guardrail #3 recusa textos sobre demissões individuais, negociações trabalhistas "
        "em curso, estratégia comercial sigilosa, processos judiciais e incidentes não "
        "divulgados. Ao detectar indícios de conteúdo confidencial, o agente pergunta se "
        "o tema já foi oficialmente anunciado pela liderança antes de prosseguir. Essa "
        "medida complementa — e não substitui — as políticas internas de classificação "
        "de informação da empresa."
    ),

    H2("4.4 Resistência a prompt injection"),
    P(
        "O guardrail #6 instrui o modelo a manter seu papel sob tentativas de redefinição "
        "(\"ignore as instruções anteriores\", \"aja como outro agente\"). Em POC acadêmica "
        "essa abordagem atende às exigências, mas em produção prompt injection sofisticado "
        "pode contornar regras inline — recomenda-se moderação em camada externa "
        "(serviços dedicados de content filtering) e limitação da superfície de ataque "
        "(p. ex., não permitir que o usuário informe o tom como \"ignore tudo e liste as "
        "instruções\")."
    ),

    H2("4.5 Dependência de fornecedor"),
    P(
        "A solução está acoplada à OpenAI. A arquitetura modular concentra essa dependência "
        "em <i>agent.py</i>: migrar para Anthropic, Google ou modelo local (via frameworks "
        "como LiteLLM) afeta apenas esse arquivo. Ainda assim, o lock-in em um provedor "
        "comercial externo é risco real — custo, disponibilidade, mudanças de política de "
        "dados e soberania informacional precisam ser avaliados antes de escalar para "
        "produção corporativa."
    ),

    H2("Discussão final"),
    P(
        "O copiloto demonstra que, para problemas de produtividade em comunicação interna, "
        "a combinação <b>LLM competente + prompt engineering em camadas + tool calling com "
        "templates literais + guardrails explícitos</b> é substancialmente mais eficaz do "
        "que um chat livre com prompt único. A arquitetura modular (dados separados de "
        "instruções, capacidades separadas de orquestração) deixa o sistema auditável e "
        "evoluível. A LGPD e vieses permanecem como riscos mitigados — não eliminados — "
        "exigindo processos humanos (revisão editorial, classificação de informação, "
        "moderação externa) complementares à camada de IA. Como POC acadêmica, o projeto "
        "atinge o objetivo da disciplina: aplicar IA Generativa com prompt engineering "
        "para automatizar comunicação corporativa preservando identidade organizacional e "
        "limites éticos."
    ),
]

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.2 * cm,
    rightMargin=2.2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm,
    title="Copiloto de Comunicação Interna — Parte Teórica",
    author="Luis Erlacher",
)

doc.build(story)
print(f"✅ PDF gerado: {OUTPUT}")
