#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar Landing Pages com texto focado no PROCESSO de cremação
Variação: funeral e crematório para cachorro e gato (16 páginas)

Uso: python gerar_lps_processo.py
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

# Tipos de página para esta variação
# funeral = novo tipo
# crematorio-de = variação do crematório com texto de processo (diferente de crematorio-cachorro que tem bairros)
TIPOS_SERVICO = ["funeral", "crematorio-de"]

# Apenas cachorro e gato (não pet)
TIPOS_ANIMAL = ["cachorro", "gato"]

# Textos do Nossa História focados no PROCESSO (não nos bairros)
TEXTOS_NOSSA_HISTORIA_PROCESSO = {
    "cachorro": """Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>, a R.I.P. Pet nasceu para transformar despedidas em homenagens com <strong>amor e gratidão</strong>. Hoje, nos orgulhamos de ser <strong>a maior organização de Cremação Pet do Brasil</strong> e de fazer parte da história de <strong>milhares de famílias</strong>.</p>
                                        <p>A partida de um <strong>cachorro</strong> é a despedida de um <strong>membro querido da família</strong>, um <strong>anjinho de quatro patas</strong> que nos deu anos de amor incondicional e alegria. Na R.I.P. Pet, entendemos essa dor e cuidamos de todo o processo com <strong>carinho, respeito e transparência</strong>. Oferecemos <strong>cremação individual</strong> — onde as cinzas devolvidas são <strong>100% do seu companheiro</strong> — e <strong>cremação coletiva</strong>, com as cinzas espalhadas em nosso jardim memorial. Todo o processo pode ser <strong>acompanhado presencialmente ou por vídeo</strong>, para que você tenha a certeza de que seu melhor amigo recebeu a homenagem que merecia.""",

    "gato": """Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>, a R.I.P. Pet nasceu para transformar despedidas em homenagens com <strong>amor e gratidão</strong>. Hoje, nos orgulhamos de ser <strong>a maior organização de Cremação Pet do Brasil</strong> e de fazer parte da história de <strong>milhares de famílias</strong>.</p>
                                        <p>A partida de um <strong>gato</strong> é a despedida de um <strong>membro querido da família</strong>, um <strong>anjinho de quatro patas</strong> que nos deu anos de amor incondicional e companhia. Na R.I.P. Pet, entendemos essa dor e cuidamos de todo o processo com <strong>carinho, respeito e transparência</strong>. Oferecemos <strong>cremação individual</strong> — onde as cinzas devolvidas são <strong>100% do seu companheiro</strong> — e <strong>cremação coletiva</strong>, com as cinzas espalhadas em nosso jardim memorial. Todo o processo pode ser <strong>acompanhado presencialmente ou por vídeo</strong>, para que você tenha a certeza de que seu felino recebeu a homenagem que merecia."""
}


def carregar_template():
    """Carrega o arquivo template de Santos"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def gerar_slug(cidade_key, tipo_servico, tipo_animal):
    """Gera o slug da URL: funeral-cachorro-guaruja, etc."""
    return f"{tipo_servico}-{tipo_animal}-{cidade_key}"


def substituir_conteudo(template, cidade_key, tipo_servico, tipo_animal):
    """Aplica todas as substituições necessárias no template"""

    cidade = CIDADES[cidade_key]
    nome = cidade["nome"]
    prep = cidade["preposicao"]
    lat = cidade["coordenadas"]["lat"]
    lng = cidade["coordenadas"]["lng"]
    slug = gerar_slug(cidade_key, tipo_servico, tipo_animal)

    # Define o texto do hero subtitle
    if cidade.get("usa_unico"):
        hero_subtitle = f"Único {prep} {nome}"
    else:
        hero_subtitle = f"O Melhor {prep} {nome}"

    # Mapeamento de animal para textos
    animal_map = {
        "cachorro": {"singular": "Cachorro", "singular_lower": "cachorro", "plural": "Cachorros", "plural_lower": "cachorros"},
        "gato": {"singular": "Gato", "singular_lower": "gato", "plural": "Gatos", "plural_lower": "gatos"},
    }
    animal = animal_map[tipo_animal]

    # Título baseado no tipo de serviço e animal
    if tipo_servico == "funeral":
        titulo_principal = f"Funeral de {animal['singular']} {nome} 24h | Cremação com Transparência | RIP PET"
        titulo_h1 = f"Funeral de {animal['plural']}<br>{prep} <span class=\"script\">{nome}</span>"
        titulo_servicos = f"Funeral de {animal['singular']}<br>{prep} {nome}"
        titulo_strip = f"{prep.capitalize()} <span class=\"script\"><strong>{nome}</strong></span>, o Maior <strong>Crematório de Animais</strong> do <span class=\"script\"><strong>Brasil</strong></span>"
        tipo_texto = "Funeral"
    else:  # crematorio-de
        titulo_principal = f"Crematório de {animal['singular']} {nome} 24h | Transparência Total | RIP PET"
        titulo_h1 = f"Crematório de {animal['plural']}<br>{prep} <span class=\"script\">{nome}</span>"
        titulo_servicos = f"Crematório de {animal['singular']}<br>{prep} {nome}"
        titulo_strip = f"{prep.capitalize()} <span class=\"script\"><strong>{nome}</strong></span>, o Maior <strong>Crematório de Animais</strong> do <span class=\"script\"><strong>Brasil</strong></span>"
        tipo_texto = "Crematório"

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
        f'<meta name="description" content="{tipo_texto} de {animal["singular_lower"]} {prep} {nome} com total transparência. Cremação individual e coletiva com acompanhamento presencial ou por vídeo. Atendimento 24h. A maior rede de crematórios pet do Brasil.">',
        conteudo
    )

    # Meta keywords
    nome_lower = nome.lower()
    if tipo_servico == "funeral":
        conteudo = re.sub(
            r'<meta name="keywords" content="cremação pet santos[^"]*">',
            f'<meta name="keywords" content="funeral {animal["singular_lower"]} {nome_lower}, cremação {animal["singular_lower"]} {nome_lower}, despedida {animal["singular_lower"]} {nome_lower}, funeral pet {nome_lower}, crematório {animal["singular_lower"]} {nome_lower}">',
            conteudo
        )
    else:  # crematorio-de
        conteudo = re.sub(
            r'<meta name="keywords" content="cremação pet santos[^"]*">',
            f'<meta name="keywords" content="crematório de {animal["singular_lower"]} {nome_lower}, cremação de {animal["singular_lower"]} {nome_lower}, cremar {animal["singular_lower"]} {nome_lower}, cremação individual {animal["singular_lower"]} {nome_lower}, cremação coletiva {animal["singular_lower"]} {nome_lower}">',
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
        f'<meta property="og:title" content="{tipo_texto} de {animal["singular"]} {nome} 24h | Transparência Total">',
        conteudo
    )

    conteudo = re.sub(
        r'<meta property="og:description" content="Acompanhe o processo de cremação do seu pet\. Transparência total, atendimento 24h em Santos e região\.">',
        f'<meta property="og:description" content="Acompanhe o processo de cremação do seu {animal["singular_lower"]}. Transparência total, atendimento 24h {prep} {nome} e região.">',
        conteudo
    )

    # Twitter
    conteudo = re.sub(
        r'<meta name="twitter:title" content="Cremação Pet Santos 24h">',
        f'<meta name="twitter:title" content="{tipo_texto} de {animal["singular"]} {nome} 24h">',
        conteudo
    )

    # ===== SCHEMA LOCAL BUSINESS =====

    conteudo = conteudo.replace(
        '<!-- Schema.org LocalBusiness - SANTOS -->',
        f'<!-- Schema.org LocalBusiness - {nome.upper()} -->'
    )

    conteudo = re.sub(
        r'"name": "RIP PET Santos - Cremação Pet 24h"',
        f'"name": "RIP PET {nome} - {tipo_texto} de {animal["singular"]} 24h"',
        conteudo
    )

    conteudo = re.sub(
        r'"description": "Crematório pet em Santos com transparência total[^"]*"',
        f'"description": "{tipo_texto} de {animal["singular_lower"]} {prep} {nome} com transparência total. Maior rede de crematórios pet do Brasil. Cremação individual e coletiva 24h com acompanhamento presencial ou por vídeo. Atendemos toda Baixada Santista desde 2012."',
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

    # ===== NOSSA HISTÓRIA - TEXTO FOCADO NO PROCESSO =====

    # Título strip
    conteudo = re.sub(
        r'<h2>Em <span class="script"><strong>Santos</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>',
        f'<h2>{titulo_strip}</h2>',
        conteudo
    )

    # Substituir TODA a seção de texto Nossa História com o texto focado no processo
    texto_processo = TEXTOS_NOSSA_HISTORIA_PROCESSO[tipo_animal]

    # Padrão para encontrar o parágrafo de Nossa História (texto original com bairros)
    padrao_nossa_historia = r'Fundada em <strong>2013</strong> pelos veterinários <em>Adriele e Carlos Eduardo</em>.*?Atendemos.*?<strong>equipamentos crematórios próprios</strong>\.'

    conteudo = re.sub(
        padrao_nossa_historia,
        texto_processo,
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

    msg_cidades = {
        "guaruja": ("no", "Guarujá"),
        "praia-grande": ("em", "Praia%20Grande"),
        "sao-vicente": ("em", "São%20Vicente"),
        "santos": ("em", "Santos"),
    }

    msg_servicos = {
        "funeral": "funeral",
        "crematorio-de": "crematório",
    }

    # Construir mensagem específica
    prep_msg, nome_msg = msg_cidades[cidade_key]
    servico_msg = msg_servicos[tipo_servico]

    msg_whatsapp = f"Olá,%20estava%20no%20site%20da%20R.I.P.%20Pet%20Santos%20e%20preciso%20de%20mais%20informações%20sobre%20{servico_msg}%20de%20{tipo_animal}%20{prep_msg}%20{nome_msg}."

    # Substituir a mensagem original do WhatsApp
    conteudo = conteudo.replace(
        'text=Olá,%20estava%20no%20site%20da%20R.I.P.%20Pet%20Santos%20e%20preciso%20de%20mais%20informações.',
        f'text={msg_whatsapp}'
    )

    # Event labels
    label_suffix = f"{cidade_key.replace('-', '_')}_{tipo_animal}_{tipo_servico}"
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
    print("GERADOR DE LPS COM TEXTO FOCADO NO PROCESSO - RIP PET")
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

    # Gera páginas para cada cidade, tipo de serviço e tipo de animal
    paginas_geradas = []

    for cidade_key, cidade_config in CIDADES.items():
        print(f"Processando {cidade_config['nome']}...")

        for tipo_servico in TIPOS_SERVICO:
            for tipo_animal in TIPOS_ANIMAL:
                slug = gerar_slug(cidade_key, tipo_servico, tipo_animal)
                conteudo = substituir_conteudo(template, cidade_key, tipo_servico, tipo_animal)
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
    print()
    print("URLs a adicionar:")
    for slug in paginas_geradas:
        print(f'    {{ "source": "/{slug}", "destination": "/organic-base/{slug}/index.html" }},')


if __name__ == "__main__":
    main()
