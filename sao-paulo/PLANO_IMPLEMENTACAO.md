# Plano de Implementação - Landing Page São Paulo

## Status: CRIADA COM VALORES GENÉRICOS

A landing page foi criada! Abaixo está o que foi feito e o que você precisa ajustar manualmente.

---

## O QUE FOI FEITO (Concluído)

### 1. Estrutura de Arquivos
- [x] Pasta `sao-paulo/` criada
- [x] `index.html` copiado de Santos e adaptado

### 2. Substituições Automáticas Realizadas
- [x] URLs: `/santos` → `/sao-paulo`
- [x] Base href: `/santos/` → `/sao-paulo/`
- [x] WhatsApp: `5513998068262` → `5511991603041`
- [x] Textos: "Santos" → "São Paulo" (na maioria dos lugares)
- [x] Região: "Baixada Santista" → "Grande São Paulo"
- [x] Coordenadas: `-23.9618;-46.3336` → `-23.5505;-46.6333`
- [x] Event labels: `hero_santos` → `hero_sao_paulo`, etc.

### 3. Cidades Atendidas (Schema.org e Menu Mobile)
- [x] Santos → São Paulo
- [x] Guarujá → Guarulhos
- [x] São Vicente → Osasco
- [x] Praia Grande → Santo André
- [x] Cubatão → São Bernardo do Campo
- [x] Bertioga → Diadema
- [x] Mongaguá → Mauá (no FAQ)
- [x] Itanhaém → Taboão da Serra (no FAQ)

---

## O QUE VOCÊ PRECISA AJUSTAR MANUALMENTE

### 1. ENDEREÇO (CRÍTICO!)
Procurar e substituir no arquivo:
```
[ATUALIZAR ENDEREÇO] - São Paulo, SP
```
Substituir pelo endereço real da unidade.

### 2. CEP
Procurar:
```
[CEP]
```
Substituir pelo CEP real.

### 3. Google Maps (iframe e links)
Atualmente usa busca genérica: `RIP+Pet+Crematorio+Sao+Paulo`

Se tiver o nome exato do estabelecimento no Google Maps, substituir nos locais:
- iframe do mapa na seção de unidade
- Botão "Como chegar"
- Schema.org hasMap

### 4. IMAGENS - Usando imagens de Santos temporariamente
Buscar por `<!-- TODO:` no HTML para ver os locais que precisam de imagens de SP:

| Imagem atual | O que colocar |
|--------------|---------------|
| `/images/fachada-santos.jpg` | Fachada da unidade SP |
| `/images/unidade-crematorio-santos.webp` | Foto da unidade SP |
| `/images/header-santos.webp` | Imagem hero de SP (ou manter genérica) |

### 5. Texto "Sobre a Unidade"
Localização: Seção de unidades
Texto atual (genérico):
> "Nossa unidade em São Paulo atende toda a Capital e Grande São Paulo..."

Ajustar com informações reais:
- Data de inauguração
- Localização/bairro
- Diferenciais da unidade

### 6. Coordenadas Exatas (opcional)
As coordenadas atuais são do centro de SP:
```
-23.5505;-46.6333
```
Se souber as coordenadas exatas da unidade, atualizar em:
- `<meta name="geo.position">`
- `<meta name="ICBM">`
- Schema.org `geo.latitude` e `geo.longitude`

### 7. Número de Avaliações Google
Procurar: `429 avaliações`
Se a unidade SP tiver número diferente de avaliações, atualizar.

---

## COMO BUSCAR E SUBSTITUIR

No VS Code:
1. `Ctrl+H` (Find and Replace)
2. Procurar: `[ATUALIZAR ENDEREÇO]`
3. Substituir pelo endereço real
4. Repetir para `[CEP]`

Para encontrar TODOs:
1. `Ctrl+F`
2. Procurar: `TODO:`

---

## ARQUIVOS QUE PRECISAM SER ATUALIZADOS NA RAIZ

### 1. sitemap.xml
Adicionar a URL de São Paulo:
```xml
<url>
  <loc>https://rippet.com.br/sao-paulo</loc>
  <lastmod>2026-01-30</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
```

### 2. vercel.json (se necessário)
Verificar se precisa de redirects ou configurações especiais.

---

## CHECKLIST ANTES DO DEPLOY

- [ ] Endereço atualizado
- [ ] CEP atualizado
- [ ] Testar WhatsApp (deve abrir com número 11 99160-3041)
- [ ] Verificar imagens (trocar por fotos de SP se tiver)
- [ ] Testar no mobile
- [ ] Atualizar sitemap.xml
- [ ] Commit e push

---

## REFERÊNCIAS ÚTEIS

- WhatsApp SP: `5511991603041`
- Telefone formatado: (11) 99160-3041
- URL: `https://rippet.com.br/sao-paulo`
- Canonical: `https://rippet.com.br/sao-paulo`

---

**Pronto para ajustes, Lucão!**
