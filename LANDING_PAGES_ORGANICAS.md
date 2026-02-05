# Landing Pages Orgânicas - RIP PET

> Documentação para geração de landing pages SEO para a Baixada Santista.
> Criado em: 2026-02-05

---

## Visão Geral

Foram criadas **52 landing pages orgânicas** para SEO, divididas em 4 categorias:

| Categoria | Páginas | Foco do conteúdo |
|-----------|---------|------------------|
| Cremação/Crematório | 24 | Texto com **bairros** da região |
| Funeral | 8 | Texto sobre o **processo** de cremação |
| Crematório-de | 8 | Texto sobre o **processo** de cremação |
| Meu Pet Morreu | 12 | Texto **"O que fazer?"** com 3 opções |

---

## Estrutura de Arquivos

```
SITE_RIP_PET_PRODUCTION/
├── scripts/
│   ├── gerar_lps_organicas.py    ← 24 páginas (bairros)
│   ├── gerar_lps_processo.py      ← 16 páginas (processo)
│   └── gerar_lps_oquefahazer.py   ← 12 páginas (meu pet morreu)
├── organic-base/                   ← Páginas geradas
│   ├── cremacao-pet-santos/
│   ├── meu-cachorro-morreu-guaruja/
│   └── ... (52 pastas)
├── santos/index.html               ← TEMPLATE BASE
├── vercel.json                     ← Rewrites das URLs
└── sitemap.xml                     ← URLs para indexação
```

---

## Scripts de Geração

### 1. `gerar_lps_organicas.py`

**Gera:** 24 páginas (cremacao/crematorio × pet/cachorro/gato × 4 cidades)

**Texto Nossa História:** Foco nos **bairros** de cada cidade

**URLs geradas:**
- `/cremacao-pet-guaruja/`
- `/cremacao-cachorro-santos/`
- `/crematorio-gato-praia-grande/`
- etc.

**Rodar:**
```bash
cd C:\Users\kel_v\LUCAS_ATELLIAR\SITE_RIP_PET_PRODUCTION
python scripts/gerar_lps_organicas.py
```

---

### 2. `gerar_lps_processo.py`

**Gera:** 16 páginas (funeral/crematorio-de × cachorro/gato × 4 cidades)

**Texto Nossa História:** Foco no **processo** de cremação (individual e coletiva)

**URLs geradas:**
- `/funeral-cachorro-guaruja/`
- `/funeral-gato-santos/`
- `/crematorio-de-cachorro-praia-grande/`
- etc.

**Rodar:**
```bash
python scripts/gerar_lps_processo.py
```

---

### 3. `gerar_lps_oquefahazer.py`

**Gera:** 12 páginas (meu-pet/cachorro/gato-morreu × 4 cidades)

**Texto Nossa História:** Explica as **3 formas de destinação**:
1. Sepultamento (cemitérios regulamentados)
2. Incineração (dejetos infectantes, sem acompanhamento)
3. Cremação (individual ou coletiva, com transparência)

**Diferencial:**
- H1 otimizado: "Meu **cachorro** morreu. O que fazer?"
- Título seção: "Amor não se descarta"

**URLs geradas:**
- `/meu-pet-morreu-guaruja/`
- `/meu-cachorro-morreu-santos/`
- `/meu-gato-morreu-praia-grande/`
- etc.

**Rodar:**
```bash
python scripts/gerar_lps_oquefahazer.py
```

---

## Configurações das Cidades

Definidas nos scripts (dicionário `CIDADES`):

```python
CIDADES = {
    "guaruja": {
        "nome": "Guarujá",
        "preposicao": "no",  # no Guarujá
        "coordenadas": {"lat": "-23.9934", "lng": "-46.2569"},
        "texto_nossa_historia": "às praias Pitangueiras, Enseada..."
    },
    "praia-grande": {
        "nome": "Praia Grande",
        "preposicao": "em",  # em Praia Grande
        ...
    },
    "sao-vicente": {
        "nome": "São Vicente",
        "preposicao": "em",
        ...
    },
    "santos": {
        "nome": "Santos",
        "preposicao": "em",
        "usa_unico": True  # "Único em Santos" ao invés de "O Melhor"
        ...
    }
}
```

---

## Como Adicionar Novas Cidades

### Passo 1: Editar os scripts

Adicionar a nova cidade no dicionário `CIDADES` de cada script:

```python
"nova-cidade": {
    "nome": "Nova Cidade",
    "preposicao": "em",  # ou "no" se masculino
    "coordenadas": {"lat": "-XX.XXXX", "lng": "-XX.XXXX"},
    "texto_nossa_historia": "aos bairros X, Y, Z..."
}
```

### Passo 2: Rodar os scripts

```bash
python scripts/gerar_lps_organicas.py
python scripts/gerar_lps_processo.py
python scripts/gerar_lps_oquefahazer.py
```

### Passo 3: Atualizar `vercel.json`

Adicionar os rewrites para cada nova URL:

```json
{
  "source": "/cremacao-pet-nova-cidade",
  "destination": "/organic-base/cremacao-pet-nova-cidade/index.html"
}
```

### Passo 4: Atualizar `sitemap.xml`

Adicionar as novas URLs:

```xml
<url>
    <loc>https://rippet.com.br/cremacao-pet-nova-cidade/</loc>
    <lastmod>2026-02-05</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
</url>
```

### Passo 5: Deploy

```bash
git add .
git commit -m "Adicionar landing pages para Nova Cidade"
git push
```

---

## Template Base

Todas as páginas são geradas a partir de:

```
C:\Users\kel_v\LUCAS_ATELLIAR\SITE_RIP_PET_PRODUCTION\santos\index.html
```

**Importante:** Qualquer alteração no template de Santos será refletida nas próximas gerações de páginas orgânicas.

---

## Elementos Personalizados por Página

| Elemento | Onde | O que muda |
|----------|------|------------|
| `<title>` | Head | Cidade + tipo de serviço |
| `<meta description>` | Head | Cidade + animal |
| `<meta keywords>` | Head | Keywords locais |
| `<link canonical>` | Head | URL da página |
| Geo tags | Head | Coordenadas da cidade |
| Open Graph | Head | Título e descrição |
| Schema.org | Head | LocalBusiness com cidade |
| H1 | Hero | Título principal |
| Hero subtitle | Hero | "Único em Santos" ou "O Melhor no Guarujá" |
| Nossa História | Seção | Texto específico (bairros/processo/3 formas) |
| WhatsApp | CTAs | Mensagem personalizada |
| Analytics labels | CTAs | Tracking por cidade/animal |

---

## Mensagens do WhatsApp

Cada tipo de página tem uma mensagem diferente:

**Páginas de bairros:**
> Olá, estava no site da R.I.P. Pet Santos e preciso de mais informações sobre cremação pet no Guarujá.

**Páginas "Meu Pet Morreu":**
> Olá, meu cachorro faleceu e gostaria de saber mais sobre o atendimento da RIP Pet Santos no Guarujá.

---

## Checklist de Deploy

- [ ] Rodar scripts de geração
- [ ] Verificar se todas as pastas foram criadas em `organic-base/`
- [ ] Verificar `vercel.json` (rewrites)
- [ ] Verificar `sitemap.xml` (URLs)
- [ ] `git add` dos arquivos
- [ ] `git commit`
- [ ] `git push`
- [ ] Aguardar deploy da Vercel (~1 min)
- [ ] Testar algumas URLs no ar
- [ ] Submeter sitemap no Google Search Console

---

## Indexação

1. Acessar [Google Search Console](https://search.google.com/search-console)
2. Ir em "Sitemaps"
3. Submeter: `https://rippet.com.br/sitemap.xml`

Ou indexar individualmente:
1. "Inspeção de URL"
2. Colar a URL
3. "Solicitar indexação"

---

## Contagem de Páginas

| Script | Fórmula | Total |
|--------|---------|-------|
| organicas | 2 tipos × 3 animais × 4 cidades | 24 |
| processo | 2 tipos × 2 animais × 4 cidades | 16 |
| oquefahazer | 1 tipo × 3 animais × 4 cidades | 12 |
| **TOTAL** | | **52** |

---

*Última atualização: 2026-02-05*
