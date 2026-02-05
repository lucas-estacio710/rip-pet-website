#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar Landing Pages orgânicas da RIP PET
Replica a LP de Santos e altera apenas os elementos específicos para SEO

Uso: python gerar_lps_organicas.py
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
        "preposicao": "no",  # no Guarujá
        "coordenadas": {
            "lat": "-23.9934",
            "lng": "-46.2569"
        },
        "texto_nossa_historia": "às praias <strong>Pitangueiras, Enseada, Astúrias, Tombo, Pernambuco, Guaíba, Praia do Éden, Praia Branca, Praia do Perequê, Praia de São Pedro, Praia do Góes, Iporanga, Praia Preta</strong>, aos bairros <strong>Jardim Acapulco, Jardim Boa Esperança, Jardim Virgínia, Jardim Las Palmas, Jardim Praiano, Mar e Céu, Santa Rosa, Vila Áurea, Vila Zilda, Vila Lígia, Vila Rã, Santo Antônio, Morrinhos, Cachoeira, Perequê, Parque Estuário, Jardim Três Marias, Jardim Cunhambebe, Vicente de Carvalho, Paecará, Sitio Conceiçãozinha, Jardim Santa Maria, Balneário Cidade Atlântica</strong> e toda a ilha"
    },
    "praia-grande": {
        "nome": "Praia Grande",
        "preposicao": "em",  # em Praia Grande
        "coordenadas": {
            "lat": "-24.0058",
            "lng": "-46.4028"
        },
        "texto_nossa_historia": "às praias <strong>Aviação, Boqueirão, Guilhermina, Canto do Forte, Ocian, Tupi, Mirim, Maracanã, Real, Flórida, Jardim Real, Vila Mirim, Balneário Flórida, Xixová, Forte</strong>, aos bairros <strong>Vila Caiçara, Vila Sônia, Anhanguera, Cidade da Criança, Jardim Imperador, Samambaia, Solemar, Ribeirópolis, Quietude, Melvi, Vila Alice, Esmeralda, Nova Mirim, Jardim Trevo, Jardim Glória, Antártica, Balneário Maracanã, Jardim Princesa, Vila São Jorge, Tupiry, Jardim Melvi, Sítio do Campo, Jardim Anhanguera, Jardim Guaramar, Cidade Ocean</strong> e toda a cidade"
    },
    "sao-vicente": {
        "nome": "São Vicente",
        "preposicao": "em",  # em São Vicente
        "coordenadas": {
            "lat": "-23.9634",
            "lng": "-46.3882"
        },
        "texto_nossa_historia": "às praias <strong>Gonzaguinha, Itararé, Milionários, Praia dos Milionários, Praia do Gonzaguinha, Praia do Itararé</strong>, aos bairros <strong>Centro, Vila Margarida, Parque Bitaru, Jardim Independência, Catiapoã, Náutica, Parque das Bandeiras, Vila Voturuá, Jardim Guassu, Vila Valença, Humaitá, Japuí, Parque São Vicente, Vila Melo, Cidade Náutica, Esplanada dos Barreiros, Vila Cascatinha, Jóquei Clube, Jardim Rio Branco, Vila São Jorge, Parque Continental, Vila Nossa Senhora de Fátima, Jardim Paraíso, Vila Matias, Gonzaga, Samaritá, Quarentenário, Pompeba, Tivoli</strong> e toda a cidade"
    },
    # Santos tem tratamento especial - usa "Único" ao invés de "O Melhor"
    "santos": {
        "nome": "Santos",
        "preposicao": "em",  # em Santos
        "coordenadas": {
            "lat": "-23.9618",
            "lng": "-46.3336"
        },
        "texto_nossa_historia": "às praias <strong>Gonzaga, José Menino, Boqueirão, Embaré, Aparecida, Ponta da Praia</strong>, aos bairros <strong>Centro, Vila Mathias, Vila Belmiro, Marapé, Campo Grande, Encruzilhada, Macuco, Estuário, Rádio Clube, Saboó, Jabaquara, Paquetá, Santa Maria, Morros, Chico de Paula, Areia Branca, Castelo, Morro da Nova Cintra, Morro do São Bento, Morro da Penha, Vila Nova, Valongo</strong> e toda a cidade",
        "usa_unico": True  # Santos usa "Único em Santos"
    }
}

# Tipos de página
TIPOS_SERVICO = ["cremacao", "crematorio"]

# Tipos de animal
TIPOS_ANIMAL = ["pet", "cachorro", "gato"]


def carregar_template():
    """Carrega o arquivo template de Santos"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def gerar_slug(cidade_key, tipo_servico, tipo_animal):
    """Gera o slug da URL: cremacao-pet-guaruja, cremacao-cachorro-guaruja, etc."""
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
    # Santos usa "Único", outras cidades usam "O Melhor"
    if cidade.get("usa_unico"):
        hero_subtitle = f"Único {prep} {nome}"
    else:
        hero_subtitle = f"O Melhor {prep} {nome}"

    # Mapeamento de animal para textos
    animal_map = {
        "pet": {"singular": "Pet", "singular_lower": "pet", "plural": "Animais", "plural_lower": "animais"},
        "cachorro": {"singular": "Cachorro", "singular_lower": "cachorro", "plural": "Cachorros", "plural_lower": "cachorros"},
        "gato": {"singular": "Gato", "singular_lower": "gato", "plural": "Gatos", "plural_lower": "gatos"},
    }
    animal = animal_map[tipo_animal]

    # Título baseado no tipo de serviço e animal
    if tipo_servico == "cremacao":
        titulo_principal = f"Cremação de {animal['singular']} {nome} 24h | Transparência Total | RIP PET"
        titulo_h1 = f"Cremação de {animal['plural']}<br>{prep} <span class=\"script\">{nome}</span>"
        titulo_servicos = f"Cremação de {animal['singular']}<br>{prep} {nome}"
        titulo_strip = f"{prep.capitalize()} <span class=\"script\"><strong>{nome}</strong></span>, o Maior <strong>Crematório de Animais</strong> do <span class=\"script\"><strong>Brasil</strong></span>"
    else:
        titulo_principal = f"Crematório de {animal['singular']} {nome} 24h | Transparência Total | RIP PET"
        titulo_h1 = f"Crematório de {animal['plural']}<br>{prep} <span class=\"script\">{nome}</span>"
        titulo_servicos = f"Crematório de {animal['singular']}<br>{prep} {nome}"
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
    tipo_texto = "Cremação" if tipo_servico == "cremacao" else "Crematório"
    conteudo = re.sub(
        r'<meta name="description" content="Cremação de pets em Santos com total transparência[^"]*">',
        f'<meta name="description" content="{tipo_texto} de {animal['singular_lower']} {prep} {nome} com total transparência. Acompanhe o processo presencialmente ou por vídeo. Atendimento 24h em toda Baixada Santista. ⭐5.0/5 (429 avaliações)">',
        conteudo
    )

    # Meta keywords
    nome_lower = nome.lower()
    conteudo = re.sub(
        r'<meta name="keywords" content="cremação pet santos[^"]*">',
        f'<meta name="keywords" content="{tipo_servico} {animal['singular_lower']} {nome_lower}, cremar {animal['singular_lower']} {nome_lower}, funerária {animal['singular_lower']} {nome_lower}, {tipo_servico} {animal['singular_lower']} {nome_lower} 24h, cremação de {animal['singular_lower']} {nome_lower}">',
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

    # Reordenar areaServed para colocar a cidade atual primeiro
    # (mantém Santos no address porque é a localização física)

    # Schema Service provider
    conteudo = re.sub(
        r'"name": "RIP PET Santos"\s*\}',
        f'"name": "RIP PET {nome}"\n      }}',
        conteudo
    )

    # ===== NAVBAR =====
    # Mantém "Unidade Santos" em todas as páginas pois é a unidade física que atende a região
    # Não alteramos a navbar

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
    # IMPORTANTE: Esta substituição deve acontecer ANTES da substituição do animal
    conteudo = re.sub(
        r'<span style="display: block; text-align: center;">Único em Santos com <strong>Crematório Próprio e Exclusivo</strong>\.</span>',
        f'<span style="display: block; text-align: center;">{hero_subtitle} com <strong>Crematório Próprio e Exclusivo</strong>.</span>',
        conteudo
    )

    # Substituir "Pet" por animal específico em textos visíveis (se não for pet)
    # IMPORTANTE: Esta substituição deve acontecer DEPOIS da substituição do hero subtitle
    if tipo_animal != "pet":
        conteudo = conteudo.replace(
            'Crematório Próprio e Exclusivo',
            'Crematório Próprio e Exclusivo'
        )

    # ===== NOSSA HISTÓRIA =====

    # Título strip
    conteudo = re.sub(
        r'<h2>Em <span class="script"><strong>Santos</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>',
        f'<h2>{titulo_strip}</h2>',
        conteudo
    )

    # Texto Nossa História com bairros
    texto_bairros = cidade["texto_nossa_historia"]
    conteudo = re.sub(
        r'Atendemos à <strong>Baixada Santista</strong> desde 2018\. Nossa unidade <strong>R\.I\.P\. Pet Santos</strong> foi inaugurada em 2023, para trazer mais proximidade e agilidade do <strong>melhor Serviço Funerário Pet do Brasil</strong>, presente nas nossas 9 cidades com <strong>Carinho, Respeito e Transparência</strong>, sendo o único instalado na região que possui <strong>equipamentos crematórios próprios</strong>\.',
        f'Atendemos {"ao" if prep == "no" else "a"} <strong>{nome}</strong> e toda <strong>Baixada Santista</strong> desde 2018. Nossa unidade <strong>R.I.P. Pet</strong> está pronta para trazer mais proximidade e agilidade do <strong>melhor Serviço Funerário Pet do Brasil</strong> {texto_bairros}, com <strong>Carinho, Respeito e Transparência</strong>, sendo o único na região que possui <strong>equipamentos crematórios próprios</strong>.',
        conteudo
    )

    # ===== SEÇÃO SERVIÇOS =====

    conteudo = re.sub(
        r'<h2>Cremação Pet<br>em Santos</h2>',
        f'<h2>{titulo_servicos}</h2>',
        conteudo
    )

    # ===== CTAs E WHATSAPP =====

    # WhatsApp messages - mensagens escritas manualmente para cada combinação
    # Chave: (cidade, tipo_servico, tipo_animal)
    # Formato: mensagem original + contexto da URL

    # Mapeamento de preposições e nomes para mensagens
    msg_cidades = {
        "guaruja": ("no", "Guarujá"),
        "praia-grande": ("em", "Praia%20Grande"),
        "sao-vicente": ("em", "São%20Vicente"),
        "santos": ("em", "Santos"),
    }

    msg_servicos = {
        "cremacao": "cremação",
        "crematorio": "crematório",
    }

    msg_animais = {
        "pet": "pet",
        "cachorro": "de%20cachorro",
        "gato": "de%20gato",
    }

    # Construir mensagem específica
    prep_msg, nome_msg = msg_cidades[cidade_key]
    servico_msg = msg_servicos[tipo_servico]
    animal_msg = msg_animais[tipo_animal]

    msg_whatsapp = f"Olá,%20estava%20no%20site%20da%20R.I.P.%20Pet%20Santos%20e%20preciso%20de%20mais%20informações%20sobre%20{servico_msg}%20{animal_msg}%20{prep_msg}%20{nome_msg}."

    # Substituir a mensagem original do WhatsApp
    conteudo = conteudo.replace(
        'text=Olá,%20estava%20no%20site%20da%20R.I.P.%20Pet%20Santos%20e%20preciso%20de%20mais%20informações.',
        f'text={msg_whatsapp}'
    )

    # Event labels - incluir animal no tracking
    label_suffix = f"{cidade_key.replace('-', '_')}_{tipo_animal}"
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

    # Aria labels - mantém referência a Santos (unidade física)
    # mas adiciona contexto da cidade na descrição
    conteudo = conteudo.replace(
        'aria-label="Ligar para R.I.P. Pet Santos"',
        f'aria-label="Ligar para R.I.P. Pet - Atendimento {prep} {nome}"'
    )
    conteudo = conteudo.replace(
        'aria-label="Falar no WhatsApp Santos"',
        f'aria-label="WhatsApp R.I.P. Pet - Atendimento {prep} {nome}"'
    )

    # ===== FAQ =====

    # Resposta do FAQ sobre trazer pet
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
    print("GERADOR DE LANDING PAGES ORGÂNICAS - RIP PET")
    print("=" * 60)
    print()

    # Verifica se o template existe
    if not TEMPLATE_FILE.exists():
        print(f"ERRO: Template não encontrado em {TEMPLATE_FILE}")
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
    print(f"CONCLUÍDO! {len(paginas_geradas)} páginas geradas:")
    print("=" * 60)
    for slug in paginas_geradas:
        print(f"  - rippet.com.br/{slug}/")
    print()
    print("Não se esqueça de verificar o vercel.json para os rewrites!")


if __name__ == "__main__":
    main()
