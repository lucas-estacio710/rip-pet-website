# -*- coding: utf-8 -*-
"""
build_vale.py — Gera a LP do Vale do Paraíba a partir do template Santos.

Estratégia: substituições CIRÚRGICAS por string literal exata.
NUNCA faz replace global de "Santos" porque a seção de Unidades e os reviews
de Santos no dedicatoriasData devem permanecer (Santos é 1 das 7 unidades).

Cada par (old, new) é validado: se `old` não existir no arquivo, o script
aborta avisando — assim nenhuma substituição passa silenciosamente.

Uso:
    python scripts/build_vale.py
"""
import sys
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "santos" / "index.html"
DST = ROOT / "vale-do-paraiba" / "index.html"

# ----------------------------------------------------------------------------
# DADOS DO VALE DO PARAÍBA
# ----------------------------------------------------------------------------
WA_VALE = "5512997996543"          # WhatsApp Matriz/Vale (CLAUDE.md)
WA_SANTOS = "5513998068262"        # número do template a substituir
TEL_FMT_VALE = "(12) 99799-6543"   # formato exibido
TEL_FMT_SANTOS = "(13) 99806-8262"
# Schema âncora = São José dos Campos (escolha do Lucão)
# geo aproximado do centro de SJC — REFINAR com o endereço exato da unidade
GEO_LAT = "-23.2237"
GEO_LON = "-45.9009"
CEP_SJC = "12245-010"                  # CEP unidade SJC (informado pelo Lucão)
RATING_COUNT = "348"                   # avaliações Google da âncora SJC (Lucão)
# >>> PENDENTE: Lucão vai criar a conta Google Ads de SJC e passar o AW.
AW_VALE = "AW-11117665288"            # ID de conversão da conta Google Ads de SJC/Vale

# Cada item: (descrição, old, new, count_esperado)
#   count_esperado = "all" para replace_all, ou int para exigir N ocorrências
REPLACEMENTS = [

    # ---- base / canonical / urls -------------------------------------------
    ('base href', '<base href="/santos/">', '<base href="/vale-do-paraiba/">', 1),
    ('urls rippet/santos', 'rippet.com.br/santos', 'rippet.com.br/vale-do-paraiba', "all"),

    # ---- telefone (global, seguro: substring cobre tel:+ e wa.me) ----------
    ('whatsapp/tel num', WA_SANTOS, WA_VALE, "all"),
    ('telefone formatado', TEL_FMT_SANTOS, TEL_FMT_VALE, "all"),

    # ---- texto da mensagem pré-preenchida do WhatsApp ----------------------
    ('msg whatsapp', 'R.I.P.%20Pet%20Santos', 'R.I.P.%20Pet', "all"),

    # ---- TITLE / META ------------------------------------------------------
    ('title tag',
     '<title>Cremação Pet Santos 24h | Transparência Total | RIP PET</title>',
     '<title>Cremação Pet Vale do Paraíba 24h | Transparência Total | RIP PET</title>', 1),
    ('meta title',
     '<meta name="title" content="Cremação Pet Santos 24h | Transparência Total | RIP PET">',
     '<meta name="title" content="Cremação Pet Vale do Paraíba 24h | Transparência Total | RIP PET">', 1),
    ('meta description',
     'Cremação pet 24h com amor e respeito. Único em Santos com crematório próprio. Urnas e Recordações inclusas, parcele em 12x. ⭐5/5 (+480 na Baixada Santista)',
     'Cremação pet 24h com amor e respeito. Crematório próprio no Vale do Paraíba, atendendo SJC, Taubaté, Jacareí, Pinda e região. Urnas e Recordações inclusas, em até 8x.', 1),
    ('meta keywords',
     'cremação pet santos, cremar pet santos, funerária pet santos, cremação animal santos 24h, cremação cachorro santos, cremação gato santos',
     'cremação pet vale do paraíba, cremação pet são josé dos campos, cremação pet taubaté, cremação pet jacareí, cremação pet pindamonhangaba, funerária pet vale do paraíba, cremação cachorro vale do paraíba, cremação gato sjc', 1),

    # ---- GEO ---------------------------------------------------------------
    ('geo placename',
     '<meta name="geo.placename" content="Santos, São Paulo, Brasil">',
     '<meta name="geo.placename" content="São José dos Campos, São Paulo, Brasil">', 1),
    ('geo position',
     '<meta name="geo.position" content="-23.9618;-46.3336">',
     f'<meta name="geo.position" content="{GEO_LAT};{GEO_LON}">', 1),
    ('geo ICBM',
     '<meta name="ICBM" content="-23.9618, -46.3336">',
     f'<meta name="ICBM" content="{GEO_LAT}, {GEO_LON}">', 1),

    # ---- OPEN GRAPH / TWITTER ----------------------------------------------
    ('og title',
     '<meta property="og:title" content="Cremação Pet Santos 24h | Transparência Total">',
     '<meta property="og:title" content="Cremação Pet Vale do Paraíba 24h | Transparência Total">', 1),
    ('og description',
     '<meta property="og:description" content="Cremação com amor e respeito. Único em Santos com crematório próprio. Urnas e Recordações inclusas, parcele em até 12x sem juros.">',
     '<meta property="og:description" content="Cremação com amor e respeito. Crematório próprio no Vale do Paraíba. Urnas e Recordações inclusas, parcele em até 8x sem juros.">', 1),
    ('twitter title',
     '<meta name="twitter:title" content="Cremação Pet Santos 24h">',
     '<meta name="twitter:title" content="Cremação Pet Vale do Paraíba 24h">', 1),

    # ---- HEADER (label da unidade no topo) ---------------------------------
    # Top bar: a unidade do Vale não usa label de cidade na navbar (decisão Lucão)
    ('header label nav',
     '<span class="unidade-label-nav">Unidade Santos</span>',
     '', "all"),

    # ---- HERO --------------------------------------------------------------
    ('hero h1',
     '<h1 class="hero-h1-desktop">Cremação Pet em <span class="script">Santos</span><span class="hero-h1-sub">Funerária e Crematório de animais de estimação</span></h1>',
     '<h1 class="hero-h1-desktop">Cremação Pet no <span class="script">Vale do Paraíba</span><span class="hero-h1-sub">Funerária e Crematório de animais de estimação</span></h1>', 1),
    ('hero frase secundaria',
     'A <strong>RIP Pet</strong> é especialista em <strong>cremação pet em Santos</strong>, atendendo toda a <strong>Baixada Santista 24h</strong>, com <strong>estrutura completa de verdade</strong>, <strong>urnas e recordações inclusas</strong> em até <strong>12x sem juros</strong>.',
     'A <strong>RIP Pet</strong> é especialista em <strong>cremação pet no Vale do Paraíba</strong>, atendendo <strong>São José dos Campos, Taubaté, Jacareí, Pinda e região 24h</strong>, com <strong>estrutura completa de verdade</strong>, <strong>urnas e recordações inclusas</strong> em até <strong>8x sem juros</strong>.', 1),
    ('hero subtitle',
     '<span style="display: block; text-align: center;">1º <strong>Cerimonial Pet</strong> na <strong>Baixada Santista</strong></span>',
     '<span style="display: block; text-align: center;">1º <strong>Cerimonial Pet</strong> do <strong>Vale do Paraíba</strong></span>', 1),

    # ---- H1: alargar a coluna do hero (desktop) ----------------------------
    # "Vale do Paraíba" é mais largo que "Santos"; a .hero-coluna tinha
    # max-width 55% e o H1 quebrava ao bater nesse limite, mesmo com espaço
    # livre à direita. Sobe p/ 65% (texto SEO e fonte mantidos intactos).
    ('hero coluna max-width',
     '''        .hero-coluna {
            position: absolute;
            top: calc(var(--navbar-height, 80px) + 1.5rem);
            left: 5%;
            transform: none;
            max-width: 55%;''',
     '''        .hero-coluna {
            position: absolute;
            top: calc(var(--navbar-height, 80px) + 1.5rem);
            left: 5%;
            transform: none;
            max-width: 65%;''', 1),

    # ---- Frase secundária do hero: justificada e ocupando a coluna toda ----
    ('hero frase secundaria largura',
     '''        .hero-coluna .hero-frase-secundaria {
            max-width: 560px;
            margin: 0;
            font-size: clamp(0.95rem, 1vw + 0.3rem, 1.15rem);
        }''',
     '''        .hero-coluna .hero-frase-secundaria {
            max-width: 100%;
            margin: 0;
            font-size: clamp(0.95rem, 1vw + 0.3rem, 1.15rem);
            text-align: justify;
        }''', 1),

    # ---- LEAD CAPTURE CONFIG ----------------------------------------------
    ("lead config unidade", "unidade: 'Santos',", "unidade: 'Vale do Paraíba',", 1),
    ("lead config code", "unidadeCode: 'ST',", "unidadeCode: 'VP',", 1),
    # Cidades ordenadas por porte até Pinda, depois Guará/Caçapava/Tremembé e o
    # restante; "Outra" NÃO entra aqui — é a flag allowOtherCity (igual Campinas).
    ("lead config cidades",
     "cidades: ['Santos', 'Praia Grande', 'Guarujá', 'São Vicente', 'Cubatão', 'Itanhaém', 'Mongaguá', 'Bertioga', 'Peruíbe'],",
     "cidades: ['São José dos Campos', 'Taubaté', 'Jacareí', 'Pindamonhangaba', 'Guaratinguetá', 'Caçapava', 'Tremembé', 'Caraguatatuba', 'Ubatuba', 'São Sebastião', 'Lorena', 'Campos do Jordão'],", 1),
    # placeholder de telefone: DDD do Vale (12), não o de Santos (13)
    ("lead config placeholder",
     "phonePlaceholder: '(13) 99999-0000',",
     "phonePlaceholder: '(12) 99999-0000',", 1),
    # habilita botão "Outra" com input livre (igual Campinas)
    ("lead config allowOtherCity",
     "askGrandePorte: true\n    };",
     "askGrandePorte: true,\n      allowOtherCity: true\n    };", 1),
    # phoneFallback já é coberto pelo replace global de WA_SANTOS (5513998068262)

    # ========================================================================
    # PEDAÇO 2 — SEO ESTRUTURADO (schema LocalBusiness / Service / FAQ / história)
    # ========================================================================

    # ---- Schema LocalBusiness ----------------------------------------------
    ('schema name',
     '"name": "RIP PET Santos - Cremação Pet 24h",',
     '"name": "RIP PET Vale do Paraíba - Cremação Pet 24h",', 1),
    ('schema description',
     '"description": "Crematório pet em Santos cuidando da sua família com amor e respeito. Único em Santos com crematório próprio, atendendo a Baixada Santista 24h. Cremação individual ou coletiva, com Urnas e Recordações inclusas, em até 12x sem juros.",',
     '"description": "Crematório pet no Vale do Paraíba cuidando da sua família com amor e respeito. Crematório próprio atendendo São José dos Campos, Taubaté, Jacareí, Pindamonhangaba e região 24h. Cremação individual ou coletiva, com Urnas e Recordações inclusas, em até 8x sem juros.",', 1),
    ('schema image fachada',
     '"https://rippet.com.br/images/fachada-santos.jpg",\n        "https://rippet.com.br/images/velorio-pet-santos.webp",',
     '"https://rippet.com.br/images/unidade-crematorio-sao-jose-campos.webp",\n        "https://rippet.com.br/images/unidade-crematorio-pindamonhangaba.webp",', 1),
    ('schema foundingDate',
     '"foundingDate": "2023",',
     '"foundingDate": "2013",', 1),
    ('schema streetAddress',
     '"streetAddress": "Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia",',
     '"streetAddress": "Av. Dr. Ademar de Barros, 1257 - Vila Ema",', 1),
    ('schema addressLocality',
     '"addressLocality": "Santos",',
     '"addressLocality": "São José dos Campos",', 1),
    ('schema postalCode',
     '"postalCode": "11035-002",',
     f'"postalCode": "{CEP_SJC}",', 1),
    ('schema areaServed cities',
     '''"areaServed": [
        {"@type": "City", "name": "Santos"},
        {"@type": "City", "name": "Guarujá"},
        {"@type": "City", "name": "São Vicente"},
        {"@type": "City", "name": "Praia Grande"},
        {"@type": "City", "name": "Cubatão"},
        {"@type": "City", "name": "Bertioga"},
        {"@type": "City", "name": "Mongaguá"},
        {"@type": "City", "name": "Itanhaém"},
        {"@type": "City", "name": "Peruíbe"}
      ],''',
     '''"areaServed": [
        {"@type": "City", "name": "São José dos Campos"},
        {"@type": "City", "name": "Taubaté"},
        {"@type": "City", "name": "Jacareí"},
        {"@type": "City", "name": "Pindamonhangaba"},
        {"@type": "City", "name": "Guaratinguetá"},
        {"@type": "City", "name": "Caçapava"},
        {"@type": "City", "name": "Tremembé"},
        {"@type": "City", "name": "Caraguatatuba"},
        {"@type": "City", "name": "Ubatuba"},
        {"@type": "City", "name": "São Sebastião"},
        {"@type": "City", "name": "Lorena"},
        {"@type": "City", "name": "Campos do Jordão"}
      ],''', 1),
    ('schema ratingCount',
     '"ratingCount": "480"',
     f'"ratingCount": "{RATING_COUNT}"', 1),
    ('schema hasMap',
     '"hasMap": "https://maps.google.com/?q=RIP+Pet+Funeral+Crematório+Santos"',
     '"hasMap": "https://maps.google.com/?q=RIP+Pet+Crematório+São+José+dos+Campos"', 1),

    # ---- Schema Service ----------------------------------------------------
    ('service provider name',
     '"name": "RIP PET Santos"',
     '"name": "RIP PET Vale do Paraíba"', 1),
    ('service areaServed',
     '"name": "Baixada Santista, SP"',
     '"name": "Vale do Paraíba, SP"', 1),

    # ---- FAQ (schema + visível usam textos quase iguais) -------------------
    ('faq schema levar pet',
     'Sim, você pode trazer seu pet diretamente à nossa unidade em Santos, na Ponta da Praia. Funcionamos 24 horas, todos os dias. Pedimos apenas que entre em contato antes de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige.',
     'Sim, você pode trazer seu pet diretamente à nossa unidade em São José dos Campos. Funcionamos 24 horas, todos os dias. Pedimos apenas que entre em contato antes de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige.', 1),
    ('faq schema busca cidades',
     'Sim, realizamos busca domiciliar em toda a Baixada Santista: Santos, Guarujá, São Vicente, Praia Grande, Cubatão, Bertioga, Mongaguá, Itanhaém e Peruíbe. O serviço funciona 24 horas com veículo identificado e equipe treinada para esse momento delicado.',
     'Sim, realizamos busca domiciliar em todo o Vale do Paraíba: São José dos Campos, Taubaté, Jacareí, Pindamonhangaba, Caçapava, Tremembé, Lorena, Guaratinguetá e região. O serviço funciona 24 horas com veículo identificado e equipe treinada para esse momento delicado.', 1),
    ('faq visivel levar pet',
     'Sim, você pode trazer seu pet diretamente à nossa <strong style="color: #10b981;">unidade em Santos</strong>, na Ponta da Praia. Funcionamos <strong style="color: #10b981;">24 horas</strong>, todos os dias. Pedimos apenas que <strong style="color: #10b981;">entre em contato antes</strong> de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige.',
     'Sim, você pode trazer seu pet diretamente à nossa <strong style="color: #10b981;">unidade em São José dos Campos</strong>. Funcionamos <strong style="color: #10b981;">24 horas</strong>, todos os dias. Pedimos apenas que <strong style="color: #10b981;">entre em contato antes</strong> de vir para que nossa equipe possa recebê-lo com todo acolhimento e atenção que o momento exige.', 1),
    ('faq visivel busca cidades',
     'Sim, realizamos <strong style="color: #10b981;">busca domiciliar</strong> em toda a Baixada Santista: Santos, Guarujá, São Vicente, Praia Grande, Cubatão, Bertioga, Mongaguá, Itanhaém e Peruíbe. O serviço funciona <strong style="color: #10b981;">24 horas</strong> com veículo identificado e equipe treinada para esse momento delicado.',
     'Sim, realizamos <strong style="color: #10b981;">busca domiciliar</strong> em todo o Vale do Paraíba: São José dos Campos, Taubaté, Jacareí, Pindamonhangaba, Caçapava, Tremembé, Lorena, Guaratinguetá e região. O serviço funciona <strong style="color: #10b981;">24 horas</strong> com veículo identificado e equipe treinada para esse momento delicado.', 1),

    # ---- Seção História ----------------------------------------------------
    ('historia h2',
     '<h2>Em <span class="script"><strong>Santos</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>',
     '<h2>No <span class="script"><strong>Vale do Paraíba</strong></span>, o Maior <strong>Crematório Pet</strong> do <span class="script"><strong>Brasil</strong></span></h2>', 1),
    ('historia paragrafo regiao',
     'Atendemos à <strong>Baixada Santista</strong> desde 2018. Nossa unidade <strong>R.I.P. Pet Santos</strong> foi inaugurada em 2023, para trazer mais proximidade e agilidade do <strong>melhor Serviço Funerário Pet do Brasil</strong>, presente nas nossas 9 cidades (Santos, São Vicente, Praia Grande, Guarujá, Cubatão, Itanhaém, Peruíbe, Bertioga e Mongaguá) com <strong>Carinho, Respeito e Transparência</strong>, sendo o único instalado na região que possui <strong>equipamentos crematórios próprios</strong>.',
     'Atendemos o <strong>Vale do Paraíba</strong> há mais de 10 anos. Com nossa <strong>matriz em Pindamonhangaba</strong> e a unidade <strong>R.I.P. Pet São José dos Campos</strong>, levamos o <strong>melhor Serviço Funerário Pet do Brasil</strong> a toda a região (São José dos Campos, Taubaté, Jacareí, Pindamonhangaba, Caçapava, Lorena, Guaratinguetá e cidades vizinhas) com <strong>Carinho, Respeito e Transparência</strong>, sendo a única rede da região com <strong>equipamentos crematórios próprios</strong>.', 1),

    # ---- Imagens do HERO (atmosféricas de Santos -> Vale) -------------------
    # Preload aponta p/ a imagem de ABERTURA do hero (bg-1 = LCP) = imagem nova.
    ('preload header linhas',
     '<link rel="preload" href="/images/header-santos-linhas.webp" as="image" type="image/webp" fetchpriority="high">',
     '<link rel="preload" href="/images/LP_Vale/carrossel_vale_cachorro_cremacao_opt.webp" as="image" type="image/webp" fetchpriority="high">', 1),
    # Imagem 1 do carrossel (abertura/LCP): aparece 2x (critical CSS + bg-1).
    ('hero bg-1 abertura',
     "url('/images/homem-cachorro-atual.webp')",
     "url('/images/LP_Vale/carrossel_vale_cachorro_cremacao_opt.webp')", "all"),
    ('hero bg-2 header',
     "url('/images/header-santos.webp');",
     "url('/images/LP_Vale/carrossel_vale_campos_cachorro_cremacao_opt.webp');", 1),
    # Ancora a 2ª imagem (campos) no bottom — desktop (sobrescreve o center 25%
    # herdado de .hero-bg) e mobile (sobrescreve o center 50%).
    ('hero bg-2 position desktop',
     '''                url('/images/LP_Vale/carrossel_vale_campos_cachorro_cremacao_opt.webp');
            animation: crossfade3-2 18s linear infinite;
        }''',
     '''                url('/images/LP_Vale/carrossel_vale_campos_cachorro_cremacao_opt.webp');
            background-position: center bottom;
            animation: crossfade3-2 18s linear infinite;
        }''', 1),
    ('hero bg-2 position mobile',
     '''            .hero-bg-2 {
                display: block !important;
                background-position: center 50% !important;
                animation: crossfade3-2 18s linear infinite !important;
            }''',
     '''            .hero-bg-2 {
                display: block !important;
                background-position: 90% bottom !important;
                animation: crossfade3-2 18s linear infinite !important;
            }''', 1),
    # bg-1 (cachorro) no mobile: +20% p/ direita (30% -> 50%).
    ('hero bg-1 position mobile',
     '''            .hero-bg-1 {
                background-position: 30% 50% !important;
                animation: crossfade3-1 18s linear infinite !important;
            }''',
     '''            .hero-bg-1 {
                background-position: 50% 50% !important;
                animation: crossfade3-1 18s linear infinite !important;
            }''', 1),
    # bg-3 (shihtzu) no mobile: +40% p/ direita (center=50% -> 90%).
    ('hero bg-3 position mobile',
     '''            .hero-bg-3 {
                display: block !important;
                background-position: center 50% !important;
                animation: crossfade3-3 18s linear infinite !important;
            }''',
     '''            .hero-bg-3 {
                display: block !important;
                background-position: 90% 50% !important;
                animation: crossfade3-3 18s linear infinite !important;
            }''', 1),
    ('hero bg-3 litoral',
     "url('/images/cachorro-litoral-noite.webp');",
     "url('/images/LP_Vale/menina_shihtzu_cremacao_praia_opt.webp');", 1),

    # ========================================================================
    # PEDAÇO 3 — SEÇÃO UNIDADES: SJC vira a aba ativa + conteúdo padrão.
    # Santos sai das abas principais e vai pro grupo "outras unidades".
    # OBS: estes `old` refletem o estado PÓS pedaços 1-2 (data-tel já = (12)).
    # ========================================================================

    # ---- Aba principal ativa: Santos -> São José dos Campos ----------------
    ('aba principal ativa',
     '<button class="unidade-tab active" data-tab="santos" data-nome="Unidade Santos" data-img="/images/unidade-crematorio-santos.webp" data-desc="Inaugurada em 2023, nossa unidade em Santos fica em uma &lt;strong&gt;casa clássica no canal 6&lt;/strong&gt;, o mais tranquilo da cidade, com detalhes sutis e acolhedores. A localização oferece fácil acesso à balsa e à perimetral, permitindo atender &lt;strong&gt;toda a Baixada Santista&lt;/strong&gt; com agilidade. Com &lt;strong&gt;atendimento 24h&lt;/strong&gt;, o espaço conta com estacionamento próprio, acessibilidade e uma sala de despedida pensada para proporcionar conforto e privacidade às famílias." data-endereco="Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia" data-cidade="Santos/SP" data-cep="11035-002" data-tel="(12) 99799-6543" data-mapsq="RIP+Pet+Funeral+Crematório+Santos">Unidade Santos</button>',
     '<button class="unidade-tab active" data-tab="sjc" data-nome="São José dos Campos" data-img="/images/unidade-crematorio-sao-jose-campos.webp" data-desc="Nossa unidade em São José dos Campos fica em &lt;strong&gt;ponto estratégico da capital do Vale do Paraíba&lt;/strong&gt;. Com &lt;strong&gt;atendimento 24h&lt;/strong&gt;, atendemos toda a região, incluindo o &lt;strong&gt;Litoral Norte, Campos do Jordão e a Serra da Mantiqueira&lt;/strong&gt;. Todas as cremações são feitas em nossa &lt;strong&gt;matriz própria em Pindamonhangaba&lt;/strong&gt;." data-endereco="Av. Dr. Ademar de Barros, 1257 - Vila Ema" data-cidade="São José dos Campos/SP" data-cep="' + CEP_SJC + '" data-tel="(12) 99799-6543" data-mapsq="RIP+Pet+Crematório+São+José+dos+Campos">São José dos Campos</button>', 1),

    # ---- Aba "outras": São José dos Campos -> Santos (com LP própria) ------
    ('aba outras sjc->santos',
     '<button class="unidade-tab" data-tab="sjc" data-nome="São José dos Campos" data-img="/images/unidade-crematorio-sao-jose-campos.webp" data-desc="Nossa unidade em São José dos Campos fica em &lt;strong&gt;ponto estratégico da capital do Vale do Paraíba&lt;/strong&gt;. Com &lt;strong&gt;atendimento 24h&lt;/strong&gt;, atendemos toda a região, incluindo o &lt;strong&gt;Litoral Norte, Campos do Jordão e a Serra da Mantiqueira&lt;/strong&gt;." data-endereco="Av. Dr. Ademar de Barros, 1257 - Vila Ema" data-mapsq="RIP+Pet+Crematório+São+José+dos+Campos">São José dos Campos</button>',
     '<button class="unidade-tab" data-tab="santos" data-lp="../santos/" data-nome="Santos" data-img="/images/unidade-crematorio-santos.webp" data-desc="Inaugurada em 2023, nossa unidade em Santos fica em uma &lt;strong&gt;casa clássica no canal 6&lt;/strong&gt;, atendendo toda a &lt;strong&gt;Baixada Santista&lt;/strong&gt; com agilidade. Com &lt;strong&gt;atendimento 24h&lt;/strong&gt;, conta com estacionamento próprio, acessibilidade e sala de despedida." data-endereco="Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia" data-mapsq="RIP+Pet+Funeral+Crematório+Santos">Santos</button>', 1),

    # ---- Conteúdo padrão (server-render): Santos -> São José dos Campos ----
    ('conteudo padrao unidade',
     '''<div class="unidade-content" id="unidade-santos" data-unidade="santos">
                <div class="unidade-text">
                    <h3 class="unidade-nome">Unidade <br class="mobile-only">Santos</h3>
                    <p class="unidade-descricao">Inaugurada em 2023, nossa unidade em Santos fica em uma <strong>casa clássica no canal 6</strong>, o mais tranquilo da cidade, com detalhes sutis e acolhedores. A localização oferece fácil acesso à balsa e à perimetral, permitindo atender <strong>toda a Baixada Santista</strong> com agilidade. Com <strong>atendimento 24h</strong>, o espaço conta com estacionamento próprio, acessibilidade e uma sala de despedida pensada para proporcionar conforto e privacidade às famílias.</p>
                    <div class="unidade-info">
                        <p class="unidade-endereco">📍 <span class="endereco-text">Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia</span></p>
                    </div>
                    <div class="unidade-mapa">
                        <iframe class="mapa-iframe" src="https://www.google.com/maps?q=RIP+Pet+Funeral+Crematório+Santos&z=15&output=embed" width="100%" height="200" style="border:0; border-radius: 10px;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                    <div class="unidade-acoes-mobile">
                        <button class="btn-acao-mobile btn-navegar" data-mapsq="RIP+Pet+Funeral+Crematório+Santos" data-nome="Unidade Santos" data-endereco="Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia">
                            <i class="fas fa-route"></i> Como chegar
                        </button>
                        <button class="btn-acao-mobile btn-compartilhar">
                            <i class="fas fa-share-alt"></i> Compartilhar
                        </button>
                    </div>
                    <div class="unidade-crosslink" id="unidade-crosslink">
                        <a href="" rel="noopener">Conheça a página dessa unidade <i class="fas fa-arrow-right" style="font-size: 0.75rem;"></i></a>
                    </div>
                </div>
                <div class="unidade-image">
                    <img src="/images/unidade-crematorio-santos.webp" alt="Unidade Santos" class="unidade-foto" loading="lazy">
                </div>
            </div>''',
     '''<div class="unidade-content" id="unidade-sjc" data-unidade="sjc">
                <div class="unidade-text">
                    <h3 class="unidade-nome">São José dos Campos</h3>
                    <p class="unidade-descricao">Nossa unidade em São José dos Campos fica em <strong>ponto estratégico da capital do Vale do Paraíba</strong>. Com <strong>atendimento 24h</strong>, atendemos toda a região, incluindo o <strong>Litoral Norte, Campos do Jordão e a Serra da Mantiqueira</strong>. Todas as cremações são realizadas em nossa <strong>matriz própria em Pindamonhangaba</strong>, com total transparência e cuidado.</p>
                    <div class="unidade-info">
                        <p class="unidade-endereco">📍 <span class="endereco-text">Av. Dr. Ademar de Barros, 1257 - Vila Ema</span></p>
                    </div>
                    <div class="unidade-mapa">
                        <iframe class="mapa-iframe" src="https://www.google.com/maps?q=RIP+Pet+Crematório+São+José+dos+Campos&z=15&output=embed" width="100%" height="200" style="border:0; border-radius: 10px;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                    <div class="unidade-acoes-mobile">
                        <button class="btn-acao-mobile btn-navegar" data-mapsq="RIP+Pet+Crematório+São+José+dos+Campos" data-nome="São José dos Campos" data-endereco="Av. Dr. Ademar de Barros, 1257 - Vila Ema">
                            <i class="fas fa-route"></i> Como chegar
                        </button>
                        <button class="btn-acao-mobile btn-compartilhar">
                            <i class="fas fa-share-alt"></i> Compartilhar
                        </button>
                    </div>
                    <div class="unidade-crosslink" id="unidade-crosslink">
                        <a href="" rel="noopener">Conheça a página dessa unidade <i class="fas fa-arrow-right" style="font-size: 0.75rem;"></i></a>
                    </div>
                </div>
                <div class="unidade-image">
                    <img src="/images/unidade-crematorio-sao-jose-campos.webp" alt="Unidade São José dos Campos" class="unidade-foto" loading="lazy">
                </div>
            </div>''', 1),

    # ========================================================================
    # PEDAÇO 4 — TRACKING: remover tag de conversão do Santos.
    # A conta Google Ads de SJC ainda será criada pelo Lucão -> placeholder.
    # GA4 (G-04KMEL26PC) é mantido (analytics geral do site).
    # ========================================================================
    ('aw conversao Santos->SJC',
     "gtag('config', 'AW-11267032942');",
     f"gtag('config', '{AW_VALE}'); // Google Ads SJC/Vale do Paraíba",
     1),

    # ---- Foto do card "Sala de velório" (Santos -> genérica da rede) -------
    # SJC e a matriz Pinda têm sala própria; foto genérica (capela) é honesta.
    ('card velorio foto',
     '<img src="/images/velorio-pet-santos.webp" alt="Salas de velório"',
     '<img src="/images/capela-crematorio-pet.webp" alt="Sala de velório"',
     1),

    # ========================================================================
    # PEDAÇO 5 — PARCELAMENTO: SJC parcela em até 8x (template Santos = 12x).
    # As 3 frases de copy (meta/og/hero/schema desc) já saem com 8x acima.
    # Aqui tratamos as menções que vêm 12x direto do template:
    # FAQ pagamento (schema + visível), mini-card e os 2 cards de preço.
    # Cards de preço: total mantido (12×107,50=1290 -> 8×161,25;
    # 12×74,17≈890 -> 8×111,25).
    # ========================================================================
    ('faq schema pagamento 12x',
     'O pagamento pode ser parcelado em até 12x no cartão.',
     'O pagamento pode ser parcelado em até 8x no cartão.', 1),
    ('faq visivel pagamento 12x',
     'parcelado em até 12x</strong> no cartão.',
     'parcelado em até 8x</strong> no cartão.', 1),
    ('mini-card 12x',
     '<span>Até <strong>12x</strong><br>sem juros</span>',
     '<span>Até <strong>8x</strong><br>sem juros</span>', 1),
    ('card preco individual',
     '<span class="servico-preco">12x de <strong>R$ 107,50</strong></span>',
     '<span class="servico-preco">8x de <strong>R$ 161,25</strong></span>', 1),
    ('card preco coletiva',
     '<span class="servico-preco">12x de <strong>R$ 74,17</strong></span>',
     '<span class="servico-preco">8x de <strong>R$ 111,25</strong></span>', 1),

    # ---- Card "Sala de velório" -> plural ----------------------------------
    # São várias salas nas duas unidades (SJC + matriz Pinda) — plural honesto.
    ('card velorio titulo',
     '<h3>Sala de velório</h3>',
     '<h3>Salas de velório</h3>', 1),
    ('card velorio texto',
     '<p>Nossa unidade possui sala de velório privativa, planejada em cada detalhe para um momento reservado e único com seu pet</p>',
     '<p>Nossas unidades possuem salas de velório privativas, planejadas em cada detalhe para um momento reservado e único com seu pet</p>', 1),

    # ---- Carrossel "Nossa História": slides 2 e 3 (eram de Santos) ----------
    # Slide 0 (fundadores) e 3 (matriz) mantidos; troca slide 1 (fachada-santos)
    # e slide 2 (carro-praia-grande) por fotos do Vale.
    ('historia slide 1 -> recepcao sjc',
     '<img src="/images/fachada-santos.jpg" alt="Unidade RIP Pet Santos" class="historia-slide">',
     '<img src="/images/LP_Vale/recepcao_crematorio_animais_sjc_opt.webp" alt="Recepção RIP Pet São José dos Campos" class="historia-slide">', 1),
    ('historia slide 2 -> matriz pinda2',
     '<img src="/images/LP_Santos/carro-praia-grande.webp" alt="Carro RIP Pet na orla" class="historia-slide">',
     '<img src="/images/matriz_pinda2_opt.webp" alt="Matriz RIP Pet Pindamonhangaba" class="historia-slide">', 1),
    # Foto extra do mobile (historia-foto-carro): carro na orla de Santos -> recepção SJC.
    ('historia foto mobile -> recepcao sjc',
     '<img src="/images/LP_Santos/carro-praia-grande.webp" alt="Carro RIP Pet na orla da praia" class="mobile-only historia-foto-carro">',
     '<img src="/images/LP_Vale/recepcao_crematorio_animais_sjc_opt.webp" alt="Recepção RIP Pet São José dos Campos" class="mobile-only historia-foto-carro">', 1),
]


def main():
    if not SRC.exists():
        sys.exit(f"ERRO: template não encontrado: {SRC}")
    html = SRC.read_text(encoding="utf-8")
    DST.parent.mkdir(parents=True, exist_ok=True)

    errors = []
    for desc, old, new, expected in REPLACEMENTS:
        if new is None:
            continue  # entradas-placeholder
        n = html.count(old)
        if expected == "all":
            if n == 0:
                errors.append(f"[NÃO ENCONTRADO] {desc}: {old[:60]!r}")
                continue
            html = html.replace(old, new)
            print(f"  ok  {desc}: {n}x")
        else:
            if n != expected:
                errors.append(f"[COUNT {n}!={expected}] {desc}: {old[:60]!r}")
                continue
            html = html.replace(old, new)
            print(f"  ok  {desc}: {n}x")

    if errors:
        print("\n=== FALHAS (nada foi escrito) ===")
        for e in errors:
            print("  " + e)
        sys.exit(1)

    DST.write_text(html, encoding="utf-8")
    print(f"\nGerado: {DST}")
    # avisos de pendências
    print(f"\nPENDENTES no arquivo: RATING_COUNT={RATING_COUNT}  AW={AW_VALE}")


if __name__ == "__main__":
    main()
