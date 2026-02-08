#!/usr/bin/env python3
"""
Script para transformar a LP São Paulo em LP Campinas.
Aplica todas as substituições definidas no plano.
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPINAS_FILE = os.path.join(BASE_DIR, "campinas", "index.html")

def read_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    content = read_file(CAMPINAS_FILE)
    original_len = len(content)

    # ============================================================
    # FASE 2.1: URLs e base href
    # ============================================================
    content = content.replace('<base href="/sao-paulo/">', '<base href="/campinas/">')
    content = content.replace('https://rippet.com.br/sao-paulo', 'https://rippet.com.br/campinas')

    # ============================================================
    # FASE 2.2: Telefone/WhatsApp (CRITICO)
    # ============================================================
    # Substituir número principal SP -> Campinas (wa.me, tel:, href links)
    content = content.replace('5511991603041', '5519999161977')
    content = content.replace('+5511991603041', '+5519999161977')
    content = content.replace('(11) 99160-3041', '(19) 99916-1977')

    # Fix bugs herdados de Santos - mobile thumb CTA
    content = content.replace('tel:+551236441766', 'tel:+5519999161977')

    # WhatsApp text
    content = content.replace('R.I.P.%20Pet%20São%20Paulo', 'R.I.P.%20Pet%20Campinas')
    content = content.replace('R.I.P.%20Pet%20S%C3%A3o%20Paulo', 'R.I.P.%20Pet%20Campinas')

    # ============================================================
    # FASE 2.3: Coordenadas
    # ============================================================
    content = content.replace('-23.5389;-46.6528', '-22.8743698;-47.0610401')
    content = content.replace('-23.5389, -46.6528', '-22.8743698, -47.0610401')
    content = content.replace('"latitude": -23.5389', '"latitude": -22.8743698')
    content = content.replace('"longitude": -46.6528', '"longitude": -47.0610401')

    # ============================================================
    # FASE 2.4: Endereco/CEP
    # ============================================================
    content = content.replace('Rua Rosa e Silva, 150 - Santa Cecília', 'Av. Dr. Heitor Penteado, 841 - Parque Taquaral')
    content = content.replace('"addressLocality": "São Paulo"', '"addressLocality": "Campinas"')
    content = content.replace('01230-020', '13075-185')

    # ============================================================
    # FASE 2.5: Event tracking (GA4)
    # ============================================================
    content = content.replace('hero_sao_paulo', 'hero_campinas')
    content = content.replace('fale_conosco_sao_paulo', 'fale_conosco_campinas')
    content = content.replace('floating_button_sao_paulo', 'floating_button_campinas')

    # ============================================================
    # FASE 2.6: Google Maps
    # ============================================================
    content = content.replace('RIP+Pet+Funeral+Crematório+São+Paulo+Higienópolis', 'RIP+Pet+Crematório+Animais+Campinas+Parque+Taquaral')
    content = content.replace('RIP+Pet+Crematorio+Sao+Paulo', 'RIP+Pet+Crematório+Animais+Campinas+Parque+Taquaral')

    # ============================================================
    # FASE 3.1: Title e Meta Description
    # ============================================================
    content = content.replace(
        '<title>Cremação Pet São Paulo 24h | Transparência Total | RIP PET</title>',
        '<title>Cremação Pet Campinas 24h | Transparência Total | RIP PET</title>'
    )
    content = content.replace(
        '<meta name="title" content="Cremação Pet São Paulo 24h | Transparência Total | RIP PET">',
        '<meta name="title" content="Cremação Pet Campinas 24h | Transparência Total | RIP PET">'
    )
    content = content.replace(
        'content="Cremação de pets em São Paulo com total transparência. Acompanhe o processo presencialmente ou por vídeo. Atendimento 24h em toda Grande São Paulo. ⭐5.0/5 (429 avaliações)"',
        'content="Cremação de pets em Campinas com total transparência. Acompanhe o processo presencialmente ou por vídeo. Atendimento 24h em Campinas e toda Região Metropolitana. ⭐5.0/5 (816 avaliações)"'
    )
    content = content.replace(
        'content="cremação pet São Paulo, cremar pet São Paulo, funerária pet São Paulo, cremação animal São Paulo 24h, cremação cachorro São Paulo, cremação gato São Paulo, crematório pet capital, cremação pet zona sul, cremação pet zona oeste"',
        'content="cremação pet Campinas, crematório pet Campinas, cremação animal Campinas 24h, cremação cachorro Campinas, cremação gato Campinas, crematório pet Parque Taquaral, cremação pet Valinhos, cremação pet Indaiatuba, cremação pet interior SP"'
    )

    # ============================================================
    # FASE 3.2: Geo Tags
    # ============================================================
    content = content.replace(
        'content="São Paulo, SP, Brasil"',
        'content="Campinas, SP, Brasil"'
    )

    # ============================================================
    # FASE 3.3: Open Graph
    # ============================================================
    content = content.replace(
        'content="Cremação Pet São Paulo 24h | Transparência Total"',
        'content="Cremação Pet Campinas 24h | Transparência Total"'
    )
    content = content.replace(
        'content="Acompanhe o processo de cremação do seu pet. Transparência total, atendimento 24h em São Paulo e região."',
        'content="Acompanhe o processo de cremação do seu pet. Transparência total, atendimento 24h em Campinas e região."'
    )

    # ============================================================
    # FASE 3.4: Twitter Cards
    # ============================================================
    content = content.replace(
        'content="Cremação Pet São Paulo 24h"',
        'content="Cremação Pet Campinas 24h"'
    )

    # ============================================================
    # FASE 3.5: Schema.org LocalBusiness
    # ============================================================
    content = content.replace(
        '"name": "RIP PET São Paulo - Cremação Pet 24h"',
        '"name": "RIP PET Campinas - Cremação Pet 24h"'
    )
    content = content.replace(
        '"description": "Crematório pet em São Paulo com transparência total. Maior rede de crematórios pet do Brasil. Cremação individual e coletiva 24h com acompanhamento presencial ou por vídeo. Atendemos toda Grande São Paulo desde 2012."',
        '"description": "Crematório pet em Campinas com transparência total. Maior rede de crematórios pet do Brasil. Cremação individual e coletiva 24h com acompanhamento presencial ou por vídeo. Atendemos Campinas e toda Região Metropolitana desde 2020."'
    )
    content = content.replace('"telephone": "+5519999161977"', '"telephone": "+5519999161977"')  # Already replaced
    content = content.replace('"foundingDate": "2012"', '"foundingDate": "2020"')
    content = content.replace('"ratingCount": "429"', '"ratingCount": "816"')

    # Schema images
    content = content.replace(
        '"https://rippet.com.br/images/LP_SaoPaulo/recepcao-crematorio-rip-pet-sao-paulo_opt.webp"',
        '"https://rippet.com.br/images/unidade-crematorio-campinas.webp"'
    )
    content = content.replace(
        '"https://rippet.com.br/images/LP_SaoPaulo/velorio-pet-sao-paulo.webp"',
        '"https://rippet.com.br/images/sala-velorio-pet-campinas.webp"'
    )

    # areaServed - replace the entire block
    old_area = '''      "areaServed": [
        {"@type": "City", "name": "São Paulo"},
        {"@type": "City", "name": "Guarujá"},
        {"@type": "City", "name": "São Vicente"},
        {"@type": "City", "name": "Santo Andr\u00e9"},
        {"@type": "City", "name": "Cubatão"},
        {"@type": "City", "name": "São Caetano do Sul"},
        {"@type": "City", "name": "Mongaguá"},
        {"@type": "City", "name": "Itanhaém"},
        {"@type": "City", "name": "Peruíbe"}
      ]'''
    new_area = '''      "areaServed": [
        {"@type": "City", "name": "Campinas"},
        {"@type": "City", "name": "Sumaré"},
        {"@type": "City", "name": "Hortolândia"},
        {"@type": "City", "name": "Valinhos"},
        {"@type": "City", "name": "Vinhedo"},
        {"@type": "City", "name": "Indaiatuba"},
        {"@type": "City", "name": "Americana"},
        {"@type": "City", "name": "Paulínia"},
        {"@type": "City", "name": "Jundiaí"}
      ]'''
    content = content.replace(old_area, new_area)

    # hasMap
    content = content.replace(
        '"hasMap": "https://maps.google.com/?q=RIP+Pet+Crematorio+Sao+Paulo"',
        '"hasMap": "https://maps.google.com/?q=RIP+Pet+Crematório+Animais+Campinas+Parque+Taquaral"'
    )

    # ============================================================
    # FASE 3.6: Schema.org FAQPage (2 perguntas SP-especificas)
    # ============================================================
    content = content.replace(
        '"text": "Sim, você pode trazer seu pet diretamente à nossa unidade em São Paulo, na Capital. Funcionamos 24 horas, todos os dias. Pedimos apenas que entre em contato antes de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige."',
        '"text": "Sim, você pode trazer seu pet diretamente à nossa unidade em Campinas, no Parque Taquaral. Funcionamos 24 horas, todos os dias. Pedimos apenas que entre em contato antes de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige."'
    )
    content = content.replace(
        '"text": "Sim, realizamos busca domiciliar em toda a Grande São Paulo: São Paulo, Guarulhos, Osasco, Santo André, São Bernardo do Campo, São Caetano do Sul, Diadema, Mauá e Taboão da Serra. O serviço funciona 24 horas com veículo identificado e equipe treinada para esse momento delicado."',
        '"text": "Sim, realizamos busca domiciliar em Campinas e toda Região Metropolitana: Campinas (Parque Taquaral), Sumaré, Hortolândia, Valinhos, Vinhedo, Indaiatuba, Americana, Paulínia, Jundiaí, Santa Bárbara d\'Oeste e Itatiba. O serviço funciona 24 horas com veículo identificado e equipe treinada para esse momento delicado."'
    )

    # ============================================================
    # FASE 3.7: Schema.org Service
    # ============================================================
    content = content.replace('"name": "RIP PET São Paulo"', '"name": "RIP PET Campinas"')
    content = content.replace(
        '"name": "Grande São Paulo, SP"',
        '"name": "Campinas e Região Metropolitana, SP"'
    )

    # ============================================================
    # FASE 4.1: Hero Section
    # ============================================================
    content = content.replace(
        '<h1 class="hero-h1-desktop">Cremação de Animais<br>em <span class="script">São Paulo</span></h1>',
        '<h1 class="hero-h1-desktop">Cremação de Animais<br>em <span class="script">Campinas</span></h1>'
    )
    content = content.replace(
        'O Melhor em São Paulo com <strong>Crematório Próprio e Exclusivo</strong>.',
        'O Melhor em Campinas com <strong>Crematório Próprio e Exclusivo</strong>.'
    )

    # ============================================================
    # FASE 4.2: Historia/Sobre a Unidade (H2)
    # ============================================================
    content = content.replace(
        '<h2>Em <span class="script"><strong>São Paulo</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>',
        '<h2>Em <span class="script"><strong>Campinas</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>'
    )

    # Historia paragraph
    content = content.replace(
        'Em <strong>2018</strong> criamos na capital de SP o <strong>1º velório pet em região central</strong>, no bairro de <strong>Higienópolis</strong>. Por nossa posição estratégica, conseguimos atender toda a <strong>Capital e Grande São Paulo</strong> de forma rápida e eficiente. Nossa unidade possui <strong>3 salas de velório</strong> com estrutura totalmente adaptada para receber os pets e seus tutores com <strong>conforto e paz</strong>. Reconhecido por tutores e médicos veterinários como o <strong>melhor Crematório Pet do Brasil</strong>.',
        'Em <strong>2020</strong>, inauguramos nossa unidade para atender <strong>Campinas e todas as cidades da região</strong>. Localizada em bairro tranquilo e estratégico, no coração do <strong>Parque Taquaral</strong>, conseguimos atender toda <strong>Campinas e a Região Metropolitana</strong> de forma rápida e eficiente. Nossa estrutura conta com <strong>duas salas de velório</strong>, totalmente projetadas para receber os pets e seus tutores com <strong>conforto e paz</strong>. Reconhecido por tutores e médicos veterinários como o <strong>melhor Crematório Pet do Brasil</strong>.'
    )

    # Mini-card: 3 Salas -> 2 Salas
    content = content.replace('<span>3 Salas de Velório</span>', '<span>2 Salas de Velório</span>')

    # Servicos card text about salas
    content = content.replace(
        'Nossa unidade possui 3 salas de velório privativas',
        'Nossa unidade possui 2 salas de velório privativas'
    )

    # ============================================================
    # FASE 4.3: Servicos heading
    # ============================================================
    content = content.replace(
        '<h2>Cremação Pet<br>em São Paulo</h2>',
        '<h2>Cremação Pet<br>em Campinas</h2>'
    )

    # ============================================================
    # FASE 4.4: Nav label
    # ============================================================
    content = content.replace(
        '<span class="unidade-label-nav">Unidade São Paulo</span>',
        '<span class="unidade-label-nav">Unidade Campinas</span>'
    )

    # ============================================================
    # FASE 4.5: Cities Grid (6 cards no map popup) - REPLACE ENTIRE BLOCK
    # ============================================================
    old_cities = '''<h3 style="text-align: center; color: white; margin-bottom: 0.5rem; font-size: 1.8rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Atendimento 24h em Toda Grande São Paulo</h3>
            <p style="text-align: center; color: #ccc; margin-bottom: 2.5rem; font-size: 1rem; font-family: 'Nunito', sans-serif; line-height: 1.4;">Busca e remoção no conforto do seu lar, sem custo adicional</p>

            <div class="cities-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 2rem;">
                <!-- São Paulo -->
                <div style="background: rgba(185, 226, 140, 0.15); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 2px solid rgba(185, 226, 140, 0.4); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(185, 226, 140, 0.25)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(185, 226, 140, 0.15)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: #B9E28C; font-size: 1.3rem; font-weight: 600; font-family: 'Poppins', sans-serif;">São Paulo ⭐</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Zona Sul, Zona Norte, Zona Leste, Zona Oeste e Centro</p>
                </div>

                <!-- Guarulhos -->
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.18)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: white; font-size: 1.2rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Guarulhos</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.85); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Centro, Bonsucesso, Taboão e toda região</p>
                </div>

                <!-- Osasco -->
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.18)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: white; font-size: 1.2rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Osasco</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.85); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Centro, Presidente Altino, Bela Vista e região</p>
                </div>'''

    new_cities = '''<h3 style="text-align: center; color: white; margin-bottom: 0.5rem; font-size: 1.8rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Atendimento 24h em Campinas e Região</h3>
            <p style="text-align: center; color: #ccc; margin-bottom: 2.5rem; font-size: 1rem; font-family: 'Nunito', sans-serif; line-height: 1.4;">Busca e remoção no conforto do seu lar, sem custo adicional</p>

            <div class="cities-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 2rem;">
                <!-- Campinas -->
                <div style="background: rgba(185, 226, 140, 0.15); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 2px solid rgba(185, 226, 140, 0.4); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(185, 226, 140, 0.25)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(185, 226, 140, 0.15)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: #B9E28C; font-size: 1.3rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Campinas ⭐</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Parque Taquaral, Cambuí, Barão Geraldo e toda região</p>
                </div>

                <!-- Sumaré -->
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.18)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: white; font-size: 1.2rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Sumaré</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.85); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Centro, Nova Veneza, Matão e toda região</p>
                </div>

                <!-- Hortolândia -->
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.18)'; this.style.transform='translateY(-3px)';" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)';">
                    <h4 style="margin: 0 0 0.8rem 0; color: white; font-size: 1.2rem; font-weight: 600; font-family: 'Poppins', sans-serif;">Hortolândia</h4>
                    <p style="margin: 0; color: rgba(255,255,255,0.85); font-size: 0.9rem; line-height: 1.5; font-family: 'Nunito', sans-serif;">Centro, Remanso Campineiro e região</p>
                </div>'''
    content = content.replace(old_cities, new_cities)

    # Remaining 3 city cards (Santo André, São Bernardo, Diadema -> Valinhos, Vinhedo, Indaiatuba)
    content = content.replace(
        '''                <!-- Santo Andr''',
        '''                <!-- Valinhos --'''
    )
    # Note: the original has encoding issues with "André" so let's match more carefully
    content = content.replace('>Santo André</h4>', '>Valinhos</h4>')
    content = content.replace('Centro, Jardim, Vila Assunção e toda região', 'Centro, São Marcos, Ortizes e região')

    content = content.replace('<!-- São Bernardo -->', '<!-- Vinhedo -->')
    content = content.replace('>São Bernardo</h4>', '>Vinhedo</h4>')
    content = content.replace('Centro, Rudge Ramos, Assunção e região', 'Centro, Capela, São Joaquim e região')

    content = content.replace('>Diadema</h4>', '>Indaiatuba</h4>')
    content = content.replace('Centro, Conceição, Serraria e toda região', 'Centro, Cidade Nova, Jardim e região')

    # Map popup phone CTA - fix the Santos bug
    content = content.replace(
        'Ligar Agora: (13) 99806-8262',
        'Ligar Agora: (19) 99916-1977'
    )

    # ============================================================
    # FASE 4.6: FAQ HTML (mesmas 2 perguntas do schema)
    # ============================================================
    content = content.replace(
        'Sim, você pode trazer seu pet diretamente à nossa <strong style="color: #10b981;">unidade em São Paulo</strong>, na Capital.',
        'Sim, você pode trazer seu pet diretamente à nossa <strong style="color: #10b981;">unidade em Campinas</strong>, no Parque Taquaral.'
    )
    content = content.replace(
        'Sim, realizamos <strong style="color: #10b981;">busca domiciliar</strong> em toda a Grande São Paulo: São Paulo (Capital), Guarulhos, Osasco, Santo André, São Bernardo do Campo, São Caetano do Sul, Diadema, Mauá e Taboão da Serra.',
        'Sim, realizamos <strong style="color: #10b981;">busca domiciliar</strong> em Campinas e toda Região Metropolitana: Campinas (Parque Taquaral), Sumaré, Hortolândia, Valinhos, Vinhedo, Indaiatuba, Americana, Paulínia, Jundiaí, Santa Bárbara d\'Oeste e Itatiba.'
    )

    # ============================================================
    # FASE 5: Unidades (tabs e conteudo)
    # ============================================================

    # 5.1 Tab primaria: SP -> Campinas (active tab)
    content = content.replace(
        'class="unidade-tab active" data-tab="sp" data-nome="Unidade São Paulo" data-img="/images/unidade-crematorio-sao-paulo.webp" data-desc="Inaugurada em 2018, nossa unidade de São Paulo foi o &lt;strong&gt;primeiro velório pet na região central da capital paulista&lt;/strong&gt;. Localizada no bairro de Higienópolis, garante &lt;strong&gt;atendimento ágil 24h&lt;/strong&gt; para toda a cidade e região metropolitana. A estrutura conta com &lt;strong&gt;estacionamento próprio, acessibilidade e três salas reservadas&lt;/strong&gt;, pensadas para proporcionar conforto e privacidade às famílias." data-endereco="Rua Rosa e Silva, 150 - Santa Cecília" data-cidade="São Paulo/SP" data-tel="(11) 99160-3041" data-mapsq="RIP+Pet+Funeral+Crematório+São+Paulo+Higienópolis">Unidade São Paulo</button>',
        'class="unidade-tab active" data-tab="camp" data-nome="Unidade Campinas" data-img="/images/unidade-crematorio-campinas.webp" data-desc="Em 2020, inauguramos nossa unidade para atender &lt;strong&gt;Campinas e todas as cidades da região&lt;/strong&gt;. Localizada no &lt;strong&gt;coração do Parque Taquaral&lt;/strong&gt;, garante &lt;strong&gt;atendimento ágil 24h&lt;/strong&gt; para toda Campinas e a Região Metropolitana. Nossa estrutura conta com &lt;strong&gt;duas salas de velório&lt;/strong&gt;, pensadas para proporcionar conforto e privacidade às famílias." data-endereco="Av. Dr. Heitor Penteado, 841 - Parque Taquaral" data-cidade="Campinas/SP" data-tel="(19) 99916-1977" data-mapsq="RIP+Pet+Crematório+Animais+Campinas+Parque+Taquaral">Unidade Campinas</button>'
    )

    # 5.3 Tabs secundarias: Mover SP para outras, remover Campinas das outras
    # Remover Campinas das outras unidades (já é a principal)
    content = content.replace(
        '                        <button class="unidade-tab" data-tab="camp" data-nome="Campinas" data-img="/images/unidade-crematorio-campinas.webp" data-desc="Em 2020, inauguramos nossa unidade para atender &lt;strong&gt;Campinas e todas as cidades da região&lt;/strong&gt;. Localizada no &lt;strong&gt;coração do Parque Taquaral&lt;/strong&gt;. Nossa estrutura conta com &lt;strong&gt;duas salas de velório&lt;/strong&gt;." data-endereco="Av. Dr. Heitor Penteado, 841 - Parque Taquaral" data-mapsq="RIP+Pet+Crematório+Animais+Campinas+Parque+Taquaral">Campinas</button>\n',
        ''
    )

    # Adicionar SP nas outras unidades (antes de Santos)
    content = content.replace(
        '                        <button class="unidade-tab" data-tab="santos"',
        '                        <button class="unidade-tab" data-tab="sp" data-nome="São Paulo" data-img="/images/unidade-crematorio-sao-paulo.webp" data-desc="Inaugurada em 2018, nossa unidade de São Paulo foi o &lt;strong&gt;primeiro velório pet na região central da capital paulista&lt;/strong&gt;. Localizada no bairro de Higienópolis, garante &lt;strong&gt;atendimento ágil 24h&lt;/strong&gt; para toda a cidade e região metropolitana." data-endereco="Rua Rosa e Silva, 150 - Santa Cecília" data-cidade="São Paulo/SP" data-tel="(11) 99160-3041" data-mapsq="RIP+Pet+Funeral+Crematório+São+Paulo+Higienópolis">São Paulo</button>\n                        <button class="unidade-tab" data-tab="santos"'
    )

    # 5.2 Conteudo da unidade exibida
    content = content.replace(
        'id="unidade-sao-paulo" data-unidade="sp"',
        'id="unidade-campinas" data-unidade="camp"'
    )
    content = content.replace(
        '<h3 class="unidade-nome">Unidade <br class="mobile-only">São Paulo</h3>',
        '<h3 class="unidade-nome">Unidade <br class="mobile-only">Campinas</h3>'
    )
    # Descricao da unidade
    content = content.replace(
        '<p class="unidade-descricao">Inaugurada em 2018, nossa unidade de São Paulo foi o <strong>primeiro velório pet na região central da capital paulista</strong>. Localizada no bairro de Higienópolis, garante <strong>atendimento ágil 24h</strong> para toda a cidade e região metropolitana. A estrutura conta com <strong>estacionamento próprio, acessibilidade e três salas reservadas</strong>, pensadas para proporcionar conforto e privacidade às famílias.</p>',
        '<p class="unidade-descricao">Em 2020, inauguramos nossa unidade para atender <strong>Campinas e todas as cidades da região</strong>. Localizada em bairro tranquilo e estratégico, no coração do <strong>Parque Taquaral</strong>, conseguimos atender toda <strong>Campinas e a Região Metropolitana</strong> de forma rápida e eficiente. Nossa estrutura conta com <strong>duas salas de velório</strong>, totalmente projetadas para receber os pets e seus tutores com <strong>conforto e paz</strong>.</p>'
    )

    # Navigation buttons
    content = content.replace(
        'data-nome="Unidade São Paulo" data-endereco="Rua Rosa e Silva, 150 - Santa Cecília"',
        'data-nome="Unidade Campinas" data-endereco="Av. Dr. Heitor Penteado, 841 - Parque Taquaral"'
    )
    # Imagem da unidade
    content = content.replace(
        'src="/images/unidade-crematorio-sao-paulo.webp" alt="Unidade São Paulo"',
        'src="/images/unidade-crematorio-campinas.webp" alt="Unidade Campinas"'
    )

    # ============================================================
    # FASE 6: Depoimentos e Equipe
    # ============================================================

    # 6.1 Reordenar dedicatoriasData: Campinas nas posições 0-2, SP vai para 3-5
    # Replace the comment and first 6 entries
    content = content.replace(
        '        // São Paulo: posições 0-2\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-01.webp", name: "Gilberto Alves Jr.", pet: "Belinha", unidade: "São Paulo",',
        '        // Campinas: posições 0-2\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-13.webp", name: "Linda Camera", pet: "Tequila", unidade: "Campinas",'
    )

    # Now we need to swap the actual testimonial texts. This is complex because the texts are very long.
    # Instead, let's replace the entire dedicatoriasData array block.
    # First, find the old entries for positions 0-2 and 12-14
    old_depo_0 = '{ img: "/images/depoimentos/dedicatoria-pet-13.webp", name: "Linda Camera", pet: "Tequila", unidade: "Campinas", text: "Foi tudo maravilhoso'
    # Actually this approach is getting complicated. Let me use a different strategy.
    # Let me replace the entire array more surgically.

    # Strategy: Replace by finding each testimonial entry precisely

    # Position 0: was Gilberto/Belinha/SP -> Linda Camera/Tequila/Campinas
    # But we already changed the first one above partially. Let's undo that and do it properly.
    # Actually the replace above changed the img/name/pet/unidade but kept the old text.
    # Let's fix the text too.

    # The first entry now has Campinas header but Gilberto's text. We need to replace the full entry.
    # This is getting complex. Let me take a different approach - replace the entire block.

    # Actually, let me revert the partial change and do it cleanly.
    # The partial replacement above already happened. Let's find what we have now and fix it.

    # Position 0 text is still Gilberto's. We need ALL 6 positions changed.
    # Let me just do targeted replacements for each position.

    # Actually, the simplest approach: since we already partially modified position 0,
    # let's just do the full replacement of the dedicatoriasData array.

    # Find the current state after the partial edit above and replace entirely
    # Let's use a regex approach for the whole array
    old_depo_section = '''    const dedicatoriasData = [
        // Campinas: posições 0-2
        { img: "/images/depoimentos/dedicatoria-pet-13.webp", name: "Linda Camera", pet: "Tequila", unidade: "Campinas", text: "Foi tudo maravilhoso. Um momento tão difícil fica um pouco mais leve com o serviço da Rip Pet. Minha filhinha peludinha se foi, mas fiz questão que ela fosse tratada com todo carinho e respeito que ela merecia até o fim. Obrigado Rip Pet 🙏. E obrigado por toda felicidade que você trouxe a nossa família Belinha. Estamos juntos sempre, até depois do fim. ❤️🐾😍🥰" },'''

    new_depo_section = '''    const dedicatoriasData = [
        // Campinas: posições 0-2
        { img: "/images/depoimentos/dedicatoria-pet-13.webp", name: "Linda Camera", pet: "Tequila", unidade: "Campinas", text: "Eu super recomendo o R.I.P. Perdi minha Golden 15 anos e foi um momento muito difícil, eu estava sozinha e desde o primeiro contato, recebi apoio e consolo. Tudo foi esclarecido com tranquilidade e consegui, apesar da tristeza, ficar bem. Muito carinho, atenção e acolhimento. A Tequila foi super bem cuidada em todos os momentos e eu fiquei em paz. Agradeço imensamente o trabalho de vocês." },'''

    content = content.replace(old_depo_section, new_depo_section)

    # Position 1: Lívia/Polly/SP -> Rebeca Toledo/Beethoven/Campinas
    content = content.replace(
        '        { img: "/images/depoimentos/dedicatoria-pet-02.webp", name: "Lívia Spessoto", pet: "Polly", unidade: "São Paulo",',
        '        { img: "/images/depoimentos/dedicatoria-pet-14.webp", name: "Rebeca Toledo", pet: "Beethoven", unidade: "Campinas",'
    )
    # Replace Lívia's text with Rebeca's text
    old_livia_text = 'text: "Recomendaria de olhos fechados! Essa foi minha primeira perda. Quando o hospital veterinário nos deu os panfletos para ligar em crematórios, o RIP pet respondeu de prontidão, nos desejou os pêsames, explicou como seria o procedimento e em menos de 40 minutos ja estavam no hospital para retirar minha pet. Foi um momento extremamente delicado para toda a familia que amava muito a Polly, porém a RIP se mostrou uma empresa totalmente humanizada e respeitosa. Apesar de toda a tristeza do momento, tivemos muita felicidade e gratidão em saber que a Polly foi bem tratada e respeitada ate seu ultimo segundo! Em todos os momentos (desde a retirada do corpo na clinica, o velório, a cremação até a entrega) foram super compreensivos e cautelosos com nossa perda. Deixo aqui meus parabéns e obrigada a essa equipe fabulosa e humana que deram dignidade a minha Polly!! Desejo que Deus abençoe todos vocês por terem cuidado tão bem assim da minha filha. Para quem estiver lendo esse comentário, deixo aqui minha honesta sugestão de confiar no trabalho da equipe, pois não falharam em nenhum segundo!" }'
    new_rebeca_text = 'text: "Quero agrader a R.I.P. PET Crematório de Animais Campinas pelo excelente serviço me prestado, meu Beethovinho faleceu no dia 06/07/25, ainda abalada pela sua partida fui muito bem atendida. Hj, meu Beethoven virou não só uma lembrança querida, mais uma estrela, teve na sua partida muito respeito e dignidade, fui muito bem amparada e acolhida durante essa fase da despedida, e hj (31/07) recebo seu certificado que levarei para sempre o respeito que teve durante sua cremação. Muito obrigada ao todo pessoal do R.I.P Crematório, indico para todos que perderem seus animaizinho que é um membro da família, esse sim indico com maior prazer, super educados e prestativo, muito obrigada!! <)" }'
    content = content.replace(old_livia_text, new_rebeca_text)

    # Position 2: Sandra/Madona/SP -> Carla Larsson/Charlie/Campinas
    content = content.replace(
        '        { img: "/images/depoimentos/dedicatoria-pet-03.webp", name: "Sandra Pinto", pet: "Madona", unidade: "São Paulo",',
        '        { img: "/images/depoimentos/dedicatoria-pet-15.webp", name: "Carla Larsson", pet: "Charlie", unidade: "Campinas",'
    )
    # Replace Sandra's text with Carla's text
    old_sandra_start = 'text: "Eu estava a bordo de um navio qdo o meu telefone'
    old_sandra_text = content[content.index(old_sandra_start):content.index('VOCÊS MERECEM..." },') + len('VOCÊS MERECEM..." },')]
    new_carla_text = 'text: "Empresa séria e responsável, tratou do meu Charlie com muito carinho e respeito, também foram muito solidários e empáticos nesse momento difícil que é a perda de um pet. Agora tenho meu bebê sempre comigo. Recomendo muito esse serviço para todos que amam seus animais como se fossem parte da família. Mais uma vez obrigada por tudo que fizeram pelo meu bebê." },'
    content = content.replace(old_sandra_text, new_carla_text)

    # Now positions 3-5 should be SP (Gilberto, Lívia, Sandra) instead of Pindamonhangaba
    # The old Pindamonhangaba entries (positions 3-5) remain as they are - that's fine per the plan
    # Actually, the plan says: "posicoes 3-5: Gilberto/Belinha, Lívia/Polly, Sandra/Madona (São Paulo)"
    # So we need to swap Pindamonhangaba 3-5 with the original SP testimonials

    # Positions 3-5: currently Pindamonhangaba -> should be SP (Gilberto, Lívia, Sandra)
    content = content.replace(
        '        // Pindamonhangaba: posições 3-5\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-04.webp", name: "Neide Lauro", pet: "Catharina", unidade: "Pindamonhangaba",',
        '        // São Paulo: posições 3-5\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-01.webp", name: "Gilberto Alves Jr.", pet: "Belinha", unidade: "São Paulo",'
    )
    # Replace Neide's text with Gilberto's
    content = content.replace(
        'text: "Quero agradecer imensamente todo o profissionalismo, cuidado e respeito que tiveram com a minha doce Catharina Sol de Maria. Num momento de tanta dor me senti acolhida e acarinhada. O trabalho de vocês é excepcional. Muita gratidão." },',
        'text: "Foi tudo maravilhoso. Um momento tão difícil fica um pouco mais leve com o serviço da Rip Pet. Minha filhinha peludinha se foi, mas fiz questão que ela fosse tratada com todo carinho e respeito que ela merecia até o fim. Obrigado Rip Pet 🙏. E obrigado por toda felicidade que você trouxe a nossa família Belinha. Estamos juntos sempre, até depois do fim. ❤️🐾😍🥰" },'
    )

    # Position 4: Flora/Mel/Pinda -> Lívia/Polly/SP
    content = content.replace(
        '        { img: "/images/depoimentos/dedicatoria-pet-05.webp", name: "Flora Furtado", pet: "Mel", unidade: "Pindamonhangaba",',
        '        { img: "/images/depoimentos/dedicatoria-pet-02.webp", name: "Lívia Spessoto", pet: "Polly", unidade: "São Paulo",'
    )
    old_flora_text = 'text: "Infelizmente precisei usar os serviços da Rip pet com a perda da minha Mel. Eles foram impecáveis em tudo. Eu já tinha ouvido falar e quando aconteceu não tive dúvidas que seria ali. A qualidade da empresa é evidente, mas a equipe é incrível. Todos extremamente respeitosos e pacientes. A Dayane nos acolheu e conduziu todo o processo com maestria. Os meninos responsáveis pela cremação também foram incríveis e respeitosos. Trataram o corpinho dela com todo respeito a memória que ela nos deixou. Tiveram toda a paciência para que eu pudesse me despedir uma última e mais uma última vez. No dia eu não consegui expressar minha gratidão por eles, eu não tinha a menor condição. Mas hoje estou aqui para recomendar. Todo pet merece uma despedida linda como eles fazem e todo tutor merece e precisa deste acolhimento." },'
    new_livia_text = 'text: "Recomendaria de olhos fechados! Essa foi minha primeira perda. Quando o hospital veterinário nos deu os panfletos para ligar em crematórios, o RIP pet respondeu de prontidão, nos desejou os pêsames, explicou como seria o procedimento e em menos de 40 minutos ja estavam no hospital para retirar minha pet. Foi um momento extremamente delicado para toda a familia que amava muito a Polly, porém a RIP se mostrou uma empresa totalmente humanizada e respeitosa. Apesar de toda a tristeza do momento, tivemos muita felicidade e gratidão em saber que a Polly foi bem tratada e respeitada ate seu ultimo segundo! Em todos os momentos (desde a retirada do corpo na clinica, o velório, a cremação até a entrega) foram super compreensivos e cautelosos com nossa perda. Deixo aqui meus parabéns e obrigada a essa equipe fabulosa e humana que deram dignidade a minha Polly!! Desejo que Deus abençoe todos vocês por terem cuidado tão bem assim da minha filha. Para quem estiver lendo esse comentário, deixo aqui minha honesta sugestão de confiar no trabalho da equipe, pois não falharam em nenhum segundo!" },'
    content = content.replace(old_flora_text, new_livia_text)

    # Position 5: Paula/Spotti/Pinda -> Sandra/Madona/SP
    content = content.replace(
        '        { img: "/images/depoimentos/dedicatoria-pet-06.webp", name: "Paula das Neves Signoretti", pet: "Spotti", unidade: "Pindamonhangaba",',
        '        { img: "/images/depoimentos/dedicatoria-pet-03.webp", name: "Sandra Pinto", pet: "Madona", unidade: "São Paulo",'
    )
    old_paula_text = 'text: "Desde o primeiro contato a equipe da RIP Pet foi extremamente cuidadosa e profissional, trazendo um pouco de serenidade num momento de extrema dor para nós. Foram muito delicados com o nosso amado filho Spotti, com quem convivemos por 18 anos e meio. Temos a certeza que pudemos prestar nossas últimas homenagens ao nosso pequeno, com toda a transparência do serviço e atendimento, desde a retirada rápida, a cerimônia, a homenagem final e ao espalhar as cinzas próximo a capela de São Francisco em uma área verde linda. Da mesma forma como ele sempre nos ensinou o amor, tivemos a certeza que encerramos esse ciclo retribuindo a ele com o mesmo sentimento. Obrigada pelo conforto!" },'
    new_sandra_text = '''text: "Eu estava a bordo de um navio qdo o meu telefone tocou e eu recebi a notícia que a minha filha Madona faleceu. Eu entrei em desespero fiz uma busca no Google e eu encontrei vocês. Como Deus foi cuidadoso comigo eu não poderia ter encontrado uma empresa melhor. Eu recebi acolhimento amor aconchego carinho buscaram o corpinho da minha filha no hospital sem q eu tivesse pago um real. Qdo eu desembarquei do navio fui imediatamente ao escritório deles e encontrei a minha filha linda coberta com flores brancas com um pano branco lindo e com dignidade. Eu não tenho palavras para expressar a minha gratidão à esta empresa a proprietária toda a equipe desde o primeiro contato me responderam de imediato me deram todo o apoio que eu precisava neste momento. Me ligaram de video no dia da cremação além disso me enviaram o vídeo da cremação e o vídeo espalhando as cinzas dela no jardim. Eu recomendo e indico tanto essa empresa que vou efetuar o pgto p/os meus 3 doguinhos q tenho. ESSA EMPRESA É IDÔNEA HONESTA PREÇO JUSTO VOCÊS NÃO IRÃO SE ARREPENDER EM CONTRATA-LOS. SE EU PUDESSE GRITAR AO MUNDO A MINHA GRATIDÃO À VOCÊS EU GRITARIA. MUITO MUITO MUITO OBRIGADA POR TUDO QUE VOCÊS FIZERAM POR MIM E PELA MINHA FILHA MADONINHA😭NÃO TEM DINHEIRO NO MUNDO QUE PAGUE SÓ DEUS NA VIDA DE VCS. PARABÉNS! DESEJO A VOCÊS TODO O SUCESSO DO MUNDO... VOCÊS MERECEM..." },'''
    content = content.replace(old_paula_text, new_sandra_text)

    # Now, positions 6-8 stay SJC, 9-11 stay Santos
    # Old positions 12-14 (Campinas) should become Pindamonhangaba (the ones we displaced)
    content = content.replace(
        '        // Campinas: posições 12-14\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-13.webp", name: "Linda Camera", pet: "Tequila", unidade: "Campinas",',
        '        // Pindamonhangaba: posições 12-14\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-04.webp", name: "Neide Lauro", pet: "Catharina", unidade: "Pindamonhangaba",'
    )
    # Replace Linda's text (in pos 12) with Neide's text
    content = content.replace(
        'text: "Eu super recomendo o R.I.P. Perdi minha Golden 15 anos e foi um momento muito difícil, eu estava sozinha e desde o primeiro contato, recebi apoio e consolo. Tudo foi esclarecido com tranquilidade e consegui, apesar da tristeza, ficar bem. Muito carinho, atenção e acolhimento. A Tequila foi super bem cuidada em todos os momentos e eu fiquei em paz. Agradeço imensamente o trabalho de vocês." },\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-14.webp", name: "Rebeca Toledo", pet: "Beethoven", unidade: "Campinas",',
        'text: "Quero agradecer imensamente todo o profissionalismo, cuidado e respeito que tiveram com a minha doce Catharina Sol de Maria. Num momento de tanta dor me senti acolhida e acarinhada. O trabalho de vocês é excepcional. Muita gratidão." },\n'
        '        { img: "/images/depoimentos/dedicatoria-pet-05.webp", name: "Flora Furtado", pet: "Mel", unidade: "Pindamonhangaba",'
    )
    # Replace Rebeca's text (in pos 13) with Flora's text
    content = content.replace(
        '''text: "Quero agrader a R.I.P. PET Crematório de Animais Campinas pelo excelente serviço me prestado, meu Beethovinho faleceu no dia 06/07/25, ainda abalada pela sua partida fui muito bem atendida. Hj, meu Beethoven virou não só uma lembrança querida, mais uma estrela, teve na sua partida muito respeito e dignidade, fui muito bem amparada e acolhida durante essa fase da despedida, e hj (31/07) recebo seu certificado que levarei para sempre o respeito que teve durante sua cremação. Muito obrigada ao todo pessoal do R.I.P Crematório, indico para todos que perderem seus animaizinho que é um membro da família, esse sim indico com maior prazer, super educados e prestativo, muito obrigada!! <)" },
        { img: "/images/depoimentos/dedicatoria-pet-15.webp", name: "Carla Larsson", pet: "Charlie", unidade: "Campinas",''',
        '''text: "Infelizmente precisei usar os serviços da Rip pet com a perda da minha Mel. Eles foram impecáveis em tudo. Eu já tinha ouvido falar e quando aconteceu não tive dúvidas que seria ali. A qualidade da empresa é evidente, mas a equipe é incrível. Todos extremamente respeitosos e pacientes. A Dayane nos acolheu e conduziu todo o processo com maestria. Os meninos responsáveis pela cremação também foram incríveis e respeitosos. Trataram o corpinho dela com todo respeito a memória que ela nos deixou. Tiveram toda a paciência para que eu pudesse me despedir uma última e mais uma última vez. No dia eu não consegui expressar minha gratidão por eles, eu não tinha a menor condição. Mas hoje estou aqui para recomendar. Todo pet merece uma despedida linda como eles fazem e todo tutor merece e precisa deste acolhimento." },
        { img: "/images/depoimentos/dedicatoria-pet-06.webp", name: "Paula das Neves Signoretti", pet: "Spotti", unidade: "Pindamonhangaba",'''
    )
    # Replace Carla's text (in pos 14) with Paula's text
    content = content.replace(
        'text: "Empresa séria e responsável, tratou do meu Charlie com muito carinho e respeito, também foram muito solidários e empáticos nesse momento difícil que é a perda de um pet. Agora tenho meu bebê sempre comigo. Recomendo muito esse serviço para todos que amam seus animais como se fossem parte da família. Mais uma vez obrigada por tudo que fizeram pelo meu bebê." },\n        // Resende:',
        'text: "Desde o primeiro contato a equipe da RIP Pet foi extremamente cuidadosa e profissional, trazendo um pouco de serenidade num momento de extrema dor para nós. Foram muito delicados com o nosso amado filho Spotti, com quem convivemos por 18 anos e meio. Temos a certeza que pudemos prestar nossas últimas homenagens ao nosso pequeno, com toda a transparência do serviço e atendimento, desde a retirada rápida, a cerimônia, a homenagem final e ao espalhar as cinzas próximo a capela de São Francisco em uma área verde linda. Da mesma forma como ele sempre nos ensinou o amor, tivemos a certeza que encerramos esse ciclo retribuindo a ele com o mesmo sentimento. Obrigada pelo conforto!" },\n        // Resende:'
    )

    # 6.2 equipeData
    content = content.replace(
        'unidade: "Unidade São Paulo"',
        'unidade: "Unidade Campinas"'
    )

    # ============================================================
    # FASE 7: Imagens
    # ============================================================

    # 7.1 Hero backgrounds
    content = content.replace(
        "url('/images/LP_SaoPaulo/tutor-cachorro-parque-ibirapuera-sao-paulo.webp')",
        "url('/images/unidade-crematorio-campinas.webp')"
    )
    content = content.replace(
        "url('/images/LP_SaoPaulo/passeio-pet-avenida-paulista-sao-paulo.webp')",
        "url('/images/sala-velorio-pet-campinas.webp')"
    )
    content = content.replace(
        "url('/images/LP_SaoPaulo/tutor-passeio-cachorro-por-do-sol-sao-paulo.webp')",
        "url('/images/homem-cachorro-jadim.webp')"
    )

    # 7.2 Historia section images
    content = content.replace(
        'src="/images/LP_SaoPaulo/fachada-com-carro-rip-pet-sp_opt.webp" alt="Fachada RIP Pet São Paulo"',
        'src="/images/unidade-crematorio-campinas.webp" alt="Unidade RIP Pet Campinas"'
    )
    content = content.replace(
        'src="/images/LP_SaoPaulo/recepcao-crematorio-rip-pet-sao-paulo_opt.webp" alt="Recepção do crematório RIP PET São Paulo"',
        'src="/images/sala-velorio-pet-campinas.webp" alt="Sala de velório RIP PET Campinas"'
    )

    # 7.3 Servicos images
    content = content.replace(
        'src="/images/LP_SaoPaulo/carro-rip-pet-crematorio_opt.webp"',
        'src="/images/equipe-atendimento-crematorio-pet.webp"'
    )
    content = content.replace(
        'src="/images/LP_SaoPaulo/velorio-pet-sao-paulo.webp" alt="Salas de velório"',
        'src="/images/sala-velorio-pet-campinas.webp" alt="Salas de velório Campinas"'
    )

    # 7.4 Preload hero image
    content = content.replace(
        'href="/images/LP_SaoPaulo/tutor-cachorro-parque-ibirapuera-sao-paulo.webp"',
        'href="/images/unidade-crematorio-campinas.webp"'
    )

    # CSS inline hero-bg-1 reference
    content = content.replace(
        ".hero-bg-1{background-image:linear-gradient(to bottom,transparent 0%,transparent 60%,rgba(2,43,71,.7)85%,#022B47 100%),url('/images/LP_SaoPaulo/tutor-cachorro-parque-ibirapuera-sao-paulo.webp')}",
        ".hero-bg-1{background-image:linear-gradient(to bottom,transparent 0%,transparent 60%,rgba(2,43,71,.7)85%,#022B47 100%),url('/images/unidade-crematorio-campinas.webp')}"
    )

    # ============================================================
    # FASE 8: Popups WhatsApp/Telefone
    # ============================================================
    # Fix the buggy duplicate "São Paulo e Região" entry with Santos number
    # In WhatsApp popup:
    content = content.replace(
        '''                <a href="https://wa.me/5519999161977?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." target="_blank" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #25D366;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">São Paulo e Região</h4>
                        <p style="margin: 0; color: #ccc; font-size: var(--fs-sm);">(13) 99806-8262</p>
                    </div>
                    <i class="fab fa-whatsapp" style="font-size: var(--fs-icon);"></i>
                </a>
                <a href="https://wa.me/5519999161977?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." target="_blank" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #25D366;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Campinas e Região</h4>''',
        '''                <a href="https://wa.me/5513998068262?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." target="_blank" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #25D366;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Santos e Baixada Santista</h4>
                        <p style="margin: 0; color: #ccc; font-size: var(--fs-sm);">(13) 99806-8262</p>
                    </div>
                    <i class="fab fa-whatsapp" style="font-size: var(--fs-icon);"></i>
                </a>
                <a href="https://wa.me/5519999161977?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." target="_blank" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #25D366;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Campinas e Região</h4>'''
    )

    # In Phone popup: fix the same bug
    content = content.replace(
        '''                <a href="tel:+5519999161977" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #4CAF50;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">São Paulo e Região</h4>
                        <p style="margin: 0; color: #ccc; font-size: var(--fs-sm);">(13) 99806-8262</p>
                    </div>
                    <i class="fas fa-phone-alt" style="font-size: var(--fs-md);"></i>
                </a>
                <a href="tel:+5519999161977" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #4CAF50;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Campinas e Região</h4>''',
        '''                <a href="tel:+5513998068262" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #4CAF50;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Santos e Baixada Santista</h4>
                        <p style="margin: 0; color: #ccc; font-size: var(--fs-sm);">(13) 99806-8262</p>
                    </div>
                    <i class="fas fa-phone-alt" style="font-size: var(--fs-md);"></i>
                </a>
                <a href="tel:+5519999161977" style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.9rem; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: white; transition: all 0.3s ease; border-left: 4px solid #4CAF50;" onmouseover="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'; this.style.transform='translateY(0)'">
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base); font-weight: 500;">Campinas e Região</h4>'''
    )

    # Floating buttons - fix title and aria-label
    content = content.replace(
        'title="Ligar Agora (13) 99806-8262" aria-label="Ligar para R.I.P. Pet São Paulo"',
        'title="Ligar Agora (19) 99916-1977" aria-label="Ligar para R.I.P. Pet Campinas"'
    )
    content = content.replace(
        'title="WhatsApp 24h (13) 99806-8262" aria-label="Falar no WhatsApp São Paulo"',
        'title="WhatsApp 24h (19) 99916-1977" aria-label="Falar no WhatsApp Campinas"'
    )

    # ============================================================
    # FASE 7: Check for generic image that might not exist
    # ============================================================
    # Check if homem-cachorro-jadim exists; if not use another
    homem_img = os.path.join(BASE_DIR, "images", "homem-cachorro-jadim.webp")
    if not os.path.exists(homem_img):
        # Use a similar generic image
        content = content.replace(
            "url('/images/homem-cachorro-jadim.webp')",
            "url('/images/sala-velorio-pet-campinas.webp')"
        )

    # ============================================================
    # HERO SECTION comment
    # ============================================================
    content = content.replace(
        'HERO SECTION - Personalizado para São Paulo',
        'HERO SECTION - Personalizado para Campinas'
    )
    content = content.replace(
        '<!-- Primary Meta Tags - OTIMIZADO PARA SÃO PAULO -->',
        '<!-- Primary Meta Tags - OTIMIZADO PARA CAMPINAS -->'
    )
    content = content.replace(
        '<!-- Language & Geo Tags - SÃO PAULO -->',
        '<!-- Language & Geo Tags - CAMPINAS -->'
    )
    content = content.replace(
        '<!-- Open Graph / Facebook / WhatsApp - SÃO PAULO -->',
        '<!-- Open Graph / Facebook / WhatsApp - CAMPINAS -->'
    )
    content = content.replace(
        '<!-- Schema.org LocalBusiness - SÃO PAULO -->',
        '<!-- Schema.org LocalBusiness - CAMPINAS -->'
    )

    # Write result
    write_file(CAMPINAS_FILE, content)

    new_len = len(content)
    print(f"Transformação concluída!")
    print(f"Tamanho original: {original_len:,} bytes")
    print(f"Tamanho final: {new_len:,} bytes")
    print(f"Diferença: {new_len - original_len:+,} bytes")

    # ============================================================
    # Verificação final
    # ============================================================
    print("\n=== VERIFICAÇÃO FINAL ===")

    checks = [
        ("/sao-paulo", "URLs /sao-paulo"),
        ("sao_paulo", "Event labels sao_paulo"),
        ("5511991603041", "Número SP"),
        ("551236441766", "Número antigo Pinda"),
        ("01230-020", "CEP SP"),
        ("-23.5389", "Latitude SP"),
        ("LP_SaoPaulo", "Imagens LP_SaoPaulo"),
    ]

    all_passed = True
    for term, desc in checks:
        count = content.count(term)
        status = "✅ OK" if count == 0 else f"❌ ENCONTRADO {count}x"
        if count > 0:
            all_passed = False
        print(f"  {desc}: {status}")

    # São Paulo deve aparecer SOMENTE em contextos permitidos
    sp_count = content.count("São Paulo")
    print(f"\n  'São Paulo' aparece {sp_count} vezes (permitido em popups, tabs secundárias, depoimentos)")

    # Show contexts where São Paulo appears
    lines = content.split('\n')
    sp_lines = [(i+1, line.strip()[:120]) for i, line in enumerate(lines) if 'São Paulo' in line]
    for ln, text in sp_lines:
        print(f"    Linha {ln}: {text}")

    if all_passed:
        print("\n✅ TODAS AS VERIFICAÇÕES PASSARAM!")
    else:
        print("\n❌ ALGUMAS VERIFICAÇÕES FALHARAM - revisar manualmente")


if __name__ == "__main__":
    main()
