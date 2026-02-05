#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar Landing Pages com seção "Meu [pet] morreu. O que fazer?"
Matriz: pet/cachorro/gato × 4 cidades = 12 páginas

Uso: python gerar_lps_oquefahazer.py
"""

import os
import re
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_FILE = BASE_DIR / "santos" / "index.html"
OUTPUT_DIR = BASE_DIR / "organic-base"

# Configurações das cidades
CIDADES = {
    "guaruja": {
        "nome": "Guarujá",
        "preposicao": "no",
        "coordenadas": {"lat": "-23.9934", "lng": "-46.2569"}
    },
    "praia-grande": {
        "nome": "Praia Grande",
        "preposicao": "em",
        "coordenadas": {"lat": "-24.0058", "lng": "-46.4028"}
    },
    "sao-vicente": {
        "nome": "São Vicente",
        "preposicao": "em",
        "coordenadas": {"lat": "-23.9634", "lng": "-46.3882"}
    },
    "santos": {
        "nome": "Santos",
        "preposicao": "em",
        "coordenadas": {"lat": "-23.9618", "lng": "-46.3336"},
        "usa_unico": True
    }
}

# Tipo de serviço para esta variação
TIPO_SERVICO = "funeral"

# Tipos de animal
TIPOS_ANIMAL = ["pet", "cachorro", "gato"]

# Textos do "O que fazer" por animal
TEXTOS_OQUEFAZER = {
    "pet": {
        "titulo_secao": "Meu pet morreu. O que fazer?",
        "paragrafo1": """Existem 3 formas de destinação do corpinho do seu <strong>pet</strong> em óbito: o <strong><u>sepultamento</u></strong> em cemitérios pet regulamentados (lóculo ou cova), onde o corpo leva anos para se decompor naturalmente; a <strong><u>incineração</u></strong>, realizada por órgãos públicos, serviços hospitalares e funerárias de animais de baixo custo junto com outros dejetos infectantes (agulhas, seringas, etc), sem possibilidade de acompanhamento; e a <strong><u>cremação</u></strong>, uma despedida digna que pode ser <strong>individual</strong> (com cinzas 100% do seu companheiro devolvidas) ou <strong>coletiva</strong> (com cinzas espalhadas em jardim memorial).""",
        "paragrafo2": """Na <strong>R.I.P. Pet</strong>, oferecemos <strong>transparência total</strong>: você pode acompanhar todo o processo <strong>presencialmente ou por vídeo</strong> — somos o único crematório da região com essa possibilidade, sem nenhum custo adicional. Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>, somos <strong>a maior rede de cremação pet do Brasil</strong>, com atendimento <strong>24 horas</strong> {PREP_CIDADE} <strong>{CIDADE}</strong>, busca domiciliar e uma equipe preparada para acolher sua família neste momento difícil. Aqui, seu melhor amigo recebe a homenagem e o descanso que merece.""",
        "msg_animal": "meu%20pet"
    },
    "cachorro": {
        "titulo_secao": "Meu cachorro morreu. O que fazer?",
        "paragrafo1": """Existem 3 formas de destinação do corpinho do seu <strong>cachorro</strong> em óbito: o <strong><u>sepultamento</u></strong> em cemitérios pet regulamentados (lóculo ou cova), onde o corpo leva anos para se decompor naturalmente; a <strong><u>incineração</u></strong>, realizada por órgãos públicos, serviços hospitalares e funerárias de animais de baixo custo junto com outros dejetos infectantes (agulhas, seringas, etc), sem possibilidade de acompanhamento; e a <strong><u>cremação</u></strong>, uma despedida digna que pode ser <strong>individual</strong> (com cinzas 100% do seu companheiro devolvidas) ou <strong>coletiva</strong> (com cinzas espalhadas em jardim memorial).""",
        "paragrafo2": """Na <strong>R.I.P. Pet</strong>, oferecemos <strong>transparência total</strong>: você pode acompanhar todo o processo <strong>presencialmente ou por vídeo</strong> — somos o único crematório da região com essa possibilidade, sem nenhum custo adicional. Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>, somos <strong>a maior rede de cremação pet do Brasil</strong>, com atendimento <strong>24 horas</strong> {PREP_CIDADE} <strong>{CIDADE}</strong>, busca domiciliar e uma equipe preparada para acolher sua família neste momento difícil. Aqui, seu melhor amigo recebe a homenagem e o descanso que merece.""",
        "msg_animal": "meu%20cachorro"
    },
    "gato": {
        "titulo_secao": "Meu gato morreu. O que fazer?",
        "paragrafo1": """Existem 3 formas de destinação do corpinho do seu <strong>gato</strong> em óbito: o <strong><u>sepultamento</u></strong> em cemitérios pet regulamentados (lóculo ou cova), onde o corpo leva anos para se decompor naturalmente; a <strong><u>incineração</u></strong>, realizada por órgãos públicos, serviços hospitalares e funerárias de animais de baixo custo junto com outros dejetos infectantes (agulhas, seringas, etc), sem possibilidade de acompanhamento; e a <strong><u>cremação</u></strong>, uma despedida digna que pode ser <strong>individual</strong> (com cinzas 100% do seu companheiro devolvidas) ou <strong>coletiva</strong> (com cinzas espalhadas em jardim memorial).""",
        "paragrafo2": """Na <strong>R.I.P. Pet</strong>, oferecemos <strong>transparência total</strong>: você pode acompanhar todo o processo <strong>presencialmente ou por vídeo</strong> — somos o único crematório da região com essa possibilidade, sem nenhum custo adicional. Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>, somos <strong>a maior rede de cremação pet do Brasil</strong>, com atendimento <strong>24 horas</strong> {PREP_CIDADE} <strong>{CIDADE}</strong>, busca domiciliar e uma equipe preparada para acolher sua família neste momento difícil. Aqui, seu melhor amigo recebe a homenagem e o descanso que merece.""",
        "msg_animal": "meu%20gato"
    }
}


def carregar_template():
    """Carrega o arquivo template de Santos"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def gerar_slug(cidade_key, tipo_animal):
    """Gera o slug da URL: meu-cachorro-morreu-guaruja, etc."""
    return f"meu-{tipo_animal}-morreu-{cidade_key}"


def substituir_conteudo(template, cidade_key, tipo_animal):
    """Aplica todas as substituições necessárias no template"""

    cidade = CIDADES[cidade_key]
    nome = cidade["nome"]
    prep = cidade["preposicao"]
    lat = cidade["coordenadas"]["lat"]
    lng = cidade["coordenadas"]["lng"]
    slug = gerar_slug(cidade_key, tipo_animal)

    # Define o texto do hero subtitle
    if cidade.get("usa_unico"):
        hero_subtitle = f"Único {prep} {nome}"
    else:
        hero_subtitle = f"O Melhor {prep} {nome}"

    # Mapeamento de animal para textos
    animal_map = {
        "pet": {"singular": "Pet", "singular_lower": "pet", "plural": "Pets", "plural_lower": "pets"},
        "cachorro": {"singular": "Cachorro", "singular_lower": "cachorro", "plural": "Cachorros", "plural_lower": "cachorros"},
        "gato": {"singular": "Gato", "singular_lower": "gato", "plural": "Gatos", "plural_lower": "gatos"},
    }
    animal = animal_map[tipo_animal]
    textos = TEXTOS_OQUEFAZER[tipo_animal]

    # Títulos
    titulo_principal = f"Meu {animal['singular']} Morreu - O Que Fazer? | Cremação {prep} {nome} | RIP PET"
    titulo_h1 = f"Funeral de {animal['plural']}<br>{prep} <span class=\"script\">{nome}</span>"
    titulo_servicos = f"Funeral de {animal['singular']}<br>{prep} {nome}"
    titulo_strip = f"{prep.capitalize()} <span class=\"script\"><strong>{nome}</strong></span>, o Maior <strong>Crematório de Animais</strong> do <span class=\"script\"><strong>Brasil</strong></span>"

    conteudo = template

    # ===== META TAGS =====

    # Base href
    conteudo = conteudo.replace(
        '<base href="/santos/">',
        f'<base href="/{slug}/">'
    )

    # Comentário Primary Meta Tags
    conteudo = conteudo.replace(
        '<!-- Primary Meta Tags - OTIMIZADO PARA SANTOS -->',
        f'<!-- Primary Meta Tags - OTIMIZADO PARA {nome.upper()} -->'
    )

    # Title
    conteudo = re.sub(
        r'<title>Cremação Pet Santos 24h \| Transparência Total \| RIP PET</title>',
        f'<title>{titulo_principal}</title>',
        conteudo
    )

    # Meta title
    conteudo = re.sub(
        r'<meta name="title" content="Cremação Pet Santos 24h \| Transparência Total \| RIP PET">',
        f'<meta name="title" content="{titulo_principal}">',
        conteudo
    )

    # Meta description
    conteudo = re.sub(
        r'<meta name="description" content="Cremação de pets em Santos com total transparência[^"]*">',
        f'<meta name="description" content="Meu {animal["singular_lower"]} morreu, o que fazer? A RIP Pet oferece cremação {prep} {nome} com total transparência. Acompanhe presencialmente ou por vídeo. Atendimento 24h.">',
        conteudo
    )

    # Meta keywords
    nome_lower = nome.lower()
    conteudo = re.sub(
        r'<meta name="keywords" content="cremação pet santos[^"]*">',
        f'<meta name="keywords" content="meu {animal["singular_lower"]} morreu o que fazer, {animal["singular_lower"]} morreu {nome_lower}, funeral {animal["singular_lower"]} {nome_lower}, cremação {animal["singular_lower"]} {nome_lower}, onde cremar {animal["singular_lower"]} {nome_lower}">',
        conteudo
    )

    # Canonical URL
    conteudo = re.sub(
        r'<link rel="canonical" href="https://rippet\.com\.br/santos">',
        f'<link rel="canonical" href="https://rippet.com.br/{slug}/">',
        conteudo
    )

    # Geo tags comentário
    conteudo = conteudo.replace(
        '<!-- Language & Geo Tags - SANTOS -->',
        f'<!-- Language & Geo Tags - {nome.upper()} -->'
    )

    # Geo placename
    conteudo = re.sub(
        r'<meta name="geo\.placename" content="Santos, São Paulo, Brasil">',
        f'<meta name="geo.placename" content="{nome}, São Paulo, Brasil">',
        conteudo
    )

    # Geo position
    conteudo = re.sub(
        r'<meta name="geo\.position" content="-23\.9618;-46\.3336">',
        f'<meta name="geo.position" content="{lat};{lng}">',
        conteudo
    )

    # ICBM
    conteudo = re.sub(
        r'<meta name="ICBM" content="-23\.9618, -46\.3336">',
        f'<meta name="ICBM" content="{lat}, {lng}">',
        conteudo
    )

    # ===== OPEN GRAPH =====

    conteudo = conteudo.replace(
        '<!-- Open Graph / Facebook / WhatsApp - SANTOS -->',
        f'<!-- Open Graph / Facebook / WhatsApp - {nome.upper()} -->'
    )

    conteudo = re.sub(
        r'<meta property="og:url" content="https://rippet\.com\.br/santos">',
        f'<meta property="og:url" content="https://rippet.com.br/{slug}/">',
        conteudo
    )

    conteudo = re.sub(
        r'<meta property="og:title" content="Cremação Pet Santos 24h \| Transparência Total">',
        f'<meta property="og:title" content="Meu {animal["singular"]} Morreu - O Que Fazer? | RIP PET {nome}">',
        conteudo
    )

    conteudo = re.sub(
        r'<meta property="og:description" content="Acompanhe o processo de cremação do seu pet\. Transparência total, atendimento 24h em Santos e região\.">',
        f'<meta property="og:description" content="Meu {animal["singular_lower"]} morreu, o que fazer? Cremação com transparência total, atendimento 24h {prep} {nome} e região.">',
        conteudo
    )

    # Twitter
    conteudo = re.sub(
        r'<meta name="twitter:title" content="Cremação Pet Santos 24h">',
        f'<meta name="twitter:title" content="Meu {animal["singular"]} Morreu - O Que Fazer?">',
        conteudo
    )

    # ===== SCHEMA LOCAL BUSINESS =====

    conteudo = conteudo.replace(
        '<!-- Schema.org LocalBusiness - SANTOS -->',
        f'<!-- Schema.org LocalBusiness - {nome.upper()} -->'
    )

    conteudo = re.sub(
        r'"name": "RIP PET Santos - Cremação Pet 24h"',
        f'"name": "RIP PET {nome} - Funeral de {animal["singular"]} 24h"',
        conteudo
    )

    conteudo = re.sub(
        r'"description": "Crematório pet em Santos com transparência total[^"]*"',
        f'"description": "Meu {animal["singular_lower"]} morreu, o que fazer? Funeral e cremação de {animal["singular_lower"]} {prep} {nome} com transparência total. Maior rede de crematórios pet do Brasil. Atendimento 24h."',
        conteudo
    )

    conteudo = re.sub(
        r'"@id": "https://rippet\.com\.br/santos"',
        f'"@id": "https://rippet.com.br/{slug}/"',
        conteudo
    )

    conteudo = re.sub(
        r'"url": "https://rippet\.com\.br/santos"',
        f'"url": "https://rippet.com.br/{slug}/"',
        conteudo
    )

    # Geo no Schema
    conteudo = re.sub(
        r'"latitude": -23\.9618,\s*"longitude": -46\.3336',
        f'"latitude": {lat},\n        "longitude": {lng}',
        conteudo
    )

    # Schema Service provider
    conteudo = re.sub(
        r'"name": "RIP PET Santos"\s*\}',
        f'"name": "RIP PET {nome}"\n      }}',
        conteudo
    )

    # ===== HERO SECTION =====

    conteudo = conteudo.replace(
        '<!-- HERO SECTION - Personalizado para Santos -->',
        f'<!-- HERO SECTION - Personalizado para {nome} -->'
    )

    # H1 Desktop
    conteudo = re.sub(
        r'<h1 class="hero-h1-desktop">Cremação de Animais<br>em <span class="script">Santos</span></h1>',
        f'<h1 class="hero-h1-desktop">{titulo_h1}</h1>',
        conteudo
    )

    # Hero subtitle - "Único em Santos" ou "O Melhor no Guarujá"
    conteudo = re.sub(
        r'<span style="display: block; text-align: center;">Único em Santos com <strong>Crematório Próprio e Exclusivo</strong>\.</span>',
        f'<span style="display: block; text-align: center;">{hero_subtitle} com <strong>Crematório Próprio e Exclusivo</strong>.</span>',
        conteudo
    )

    # ===== NOSSA HISTÓRIA - NOVO FORMATO "O QUE FAZER" =====

    # Título strip
    conteudo = re.sub(
        r'<h2>Em <span class="script"><strong>Santos</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>',
        f'<h2>{titulo_strip}</h2>',
        conteudo
    )

    # Título da seção "Nossa história" -> "Amor não se descarta"
    conteudo = re.sub(
        r'<h2 class="historia-title">Nossa história</h2>',
        '<h2 class="historia-title">Amor não se descarta</h2>',
        conteudo
    )

    # Hero atendimento -> "Conheça as opções <em>corretas</em>"
    conteudo = re.sub(
        r'<p class="hero-atendimento">Atendimento <strong>24h</strong> todos os dias</p>',
        '<p class="hero-atendimento">Conheça as opções <em>corretas</em></p>',
        conteudo
    )

    # H1 do hero -> "Meu [pet] morreu. O que fazer?" (animal em negrito)
    conteudo = re.sub(
        r'<h1 class="hero-h1-desktop">Funeral de .*?</h1>',
        f'<h1 class="hero-h1-desktop">Meu <strong>{animal["singular_lower"]}</strong> morreu.<br>O que fazer?</h1>',
        conteudo
    )


    # Substituir os dois parágrafos de Nossa História
    # Padrão para encontrar os parágrafos originais
    padrao_paragrafos = r'<p>Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>.*?<strong>equipamentos crematórios próprios</strong>\.</p>'

    novo_texto = f"""<p>{textos["paragrafo1"]}</p>
                                    <br>
                                    <p>{textos["paragrafo2"]}</p>"""

    # Substituir placeholders de cidade no texto
    novo_texto = novo_texto.replace("{PREP_CIDADE}", prep)
    novo_texto = novo_texto.replace("{CIDADE}", nome)

    conteudo = re.sub(
        padrao_paragrafos,
        novo_texto,
        conteudo,
        flags=re.DOTALL
    )

    # ===== SEÇÃO SERVIÇOS =====

    conteudo = re.sub(
        r'<h2>Cremação Pet<br>em Santos</h2>',
        f'<h2>{titulo_servicos}</h2>',
        conteudo
    )

    # ===== CTAs E WHATSAPP =====

    # Mensagem WhatsApp personalizada
    # Santos: "Olá, meu pet faleceu e gostaria de saber mais sobre o atendimento da RIP Pet Santos."
    # Outras: "Olá, meu pet faleceu e gostaria de saber mais sobre o atendimento da RIP Pet Santos em [cidade]."

    msg_animal = textos["msg_animal"]

    if cidade_key == "santos":
        msg_whatsapp = f"Olá,%20{msg_animal}%20faleceu%20e%20gostaria%20de%20saber%20mais%20sobre%20o%20atendimento%20da%20RIP%20Pet%20Santos."
    else:
        msg_whatsapp = f"Olá,%20{msg_animal}%20faleceu%20e%20gostaria%20de%20saber%20mais%20sobre%20o%20atendimento%20da%20RIP%20Pet%20Santos%20{prep}%20{nome}."

    # Substituir a mensagem original do WhatsApp
    conteudo = conteudo.replace(
        'text=Olá,%20estava%20no%20site%20da%20R.I.P.%20Pet%20Santos%20e%20preciso%20de%20mais%20informações.',
        f'text={msg_whatsapp}'
    )

    # Event labels
    label_suffix = f"{cidade_key.replace('-', '_')}_{tipo_animal}_oquefazer"
    conteudo = conteudo.replace(
        "'hero_santos'",
        f"'hero_{label_suffix}'"
    )
    conteudo = conteudo.replace(
        "'floating_button_santos'",
        f"'floating_button_{label_suffix}'"
    )
    conteudo = conteudo.replace(
        "'fale_conosco_santos'",
        f"'fale_conosco_{label_suffix}'"
    )

    # Aria labels
    conteudo = conteudo.replace(
        'aria-label="Ligar para R.I.P. Pet Santos"',
        f'aria-label="Ligar para R.I.P. Pet - Atendimento {prep} {nome}"'
    )
    conteudo = conteudo.replace(
        'aria-label="Falar no WhatsApp Santos"',
        f'aria-label="WhatsApp R.I.P. Pet - Atendimento {prep} {nome}"'
    )

    # ===== FAQ =====

    conteudo = re.sub(
        r'à nossa unidade em Santos',
        f'à nossa unidade que atende {"o" if prep == "no" else ""} {nome}',
        conteudo
    )

    return conteudo


def salvar_pagina(conteudo, slug):
    """Salva a página gerada no diretório correto"""
    output_path = OUTPUT_DIR / slug / "index.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"  [OK] Gerado: {output_path}")
    return output_path


def main():
    """Função principal"""
    print("=" * 60)
    print("GERADOR DE LPS 'MEU PET MORREU' - RIP PET")
    print("=" * 60)
    print()

    # Verifica se o template existe
    if not TEMPLATE_FILE.exists():
        print(f"ERRO: Template nao encontrado em {TEMPLATE_FILE}")
        return

    print(f"Template: {TEMPLATE_FILE}")
    print(f"Destino: {OUTPUT_DIR}")
    print()

    # Carrega o template
    template = carregar_template()
    print(f"Template carregado: {len(template):,} caracteres")
    print()

    # Gera páginas para cada cidade e tipo de animal
    paginas_geradas = []

    for cidade_key, cidade_config in CIDADES.items():
        print(f"Processando {cidade_config['nome']}...")

        for tipo_animal in TIPOS_ANIMAL:
            slug = gerar_slug(cidade_key, tipo_animal)
            conteudo = substituir_conteudo(template, cidade_key, tipo_animal)
            output_path = salvar_pagina(conteudo, slug)
            paginas_geradas.append(slug)

    print()
    print("=" * 60)
    print(f"CONCLUIDO! {len(paginas_geradas)} paginas geradas:")
    print("=" * 60)
    for slug in paginas_geradas:
        print(f"  - rippet.com.br/{slug}/")
    print()
    print("Lembre-se de adicionar os rewrites no vercel.json!")


if __name__ == "__main__":
    main()
