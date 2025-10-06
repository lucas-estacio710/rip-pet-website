# 📊 GUIA COMPLETO - CONFIGURAÇÃO DO ANALYTICS AVANÇADO RIP PET

## ✅ O QUE FOI IMPLEMENTADO

### Eventos Granulares Configurados:

1. **click_whatsapp** - Rastreia cliques no WhatsApp
   - Por unidade (São Paulo, Santos, Campinas, etc.)
   - Seção da página onde clicou
   - Valor: 10 pontos

2. **click_phone** - Rastreia cliques no telefone
   - Por unidade
   - Seção da página
   - Valor: 15 pontos (maior intenção)

3. **scroll_depth** - Acompanha scroll do usuário
   - 25%, 50%, 75%, 90%
   - Identifica engajamento

4. **section_view** - Rastreia visualização de seções
   - Serviços, Processo, Depoimentos, etc.

5. **view_pricing** - Detecta quando usuário vê preços
   - Indica interesse em compra
   - Valor: 5 pontos

6. **review_interaction** - Interações com depoimentos
   - Expandir reviews
   - Social proof engagement

7. **faq_click** - Cliques em perguntas frequentes
   - Rastreia dúvidas mais comuns

8. **time_on_page** - Tempo de permanência
   - Marcos: 30s, 1min, 2min, 5min
   - Qualidade do tráfego

9. **whatsapp_popup** - Interação com popup
   - Abrir/fechar
   - Taxa de conversão do popup

---

## 🎯 PASSO 1: CONFIGURAR CONVERSÕES NO GA4

### Como marcar eventos como conversões:

1. **Acesse Google Analytics 4**
   - Vá para: https://analytics.google.com/
   - Selecione a propriedade: **RIP PET (G-LS0H2KX8EF)**

2. **Navegue até Eventos**
   - Menu lateral: **Configurar** → **Eventos**
   - Aguarde alguns minutos após o deploy para os eventos aparecerem

3. **Marcar como Conversão**
   - Encontre os eventos listados abaixo
   - Clique no botão de **"Marcar como conversão"** em cada um

### Eventos CRÍTICOS para marcar como conversão:

✅ **click_whatsapp** - Lead quente via WhatsApp
✅ **click_phone** - Lead quente via telefone
✅ **view_pricing** - Interesse em serviços
✅ **time_on_page** (5min) - Engajamento profundo

### Eventos para NÃO marcar (são apenas de engajamento):

❌ scroll_depth
❌ section_view
❌ faq_click
❌ review_interaction

---

## 📈 PASSO 2: CRIAR RELATÓRIOS CUSTOMIZADOS

### Relatório 1: **Funil de Conversão Completo**

1. **Menu:** Explorar → **Criar nova exploração**
2. **Tipo:** Exploração de funil
3. **Configurar etapas:**

```
Etapa 1: page_view (Visita)
Etapa 2: scroll_depth (50%) (Engajamento)
Etapa 3: view_pricing (Interesse)
Etapa 4: click_whatsapp OU click_phone (Conversão)
```

4. **Dimensões secundárias:**
   - Origem/mídia
   - Dispositivo
   - Cidade

5. **Salvar como:** "Funil de Conversão RIP PET"

---

### Relatório 2: **Performance por Unidade**

1. **Explorar → Criar nova exploração**
2. **Tipo:** Exploração livre
3. **Dimensões:**
   - unit_name (unidade)
   - page_section (seção)
4. **Métricas:**
   - Contagem de eventos (click_whatsapp + click_phone)
   - Taxa de conversão
5. **Filtros:**
   - Nome do evento = click_whatsapp OU click_phone
6. **Salvar como:** "Performance por Unidade"

---

### Relatório 3: **Análise de Engajamento**

1. **Explorar → Criar nova exploração**
2. **Tipo:** Exploração livre
3. **Dimensões:**
   - Origem do tráfego
   - Tipo de dispositivo
4. **Métricas:**
   - Tempo médio de engajamento
   - Taxa de scroll (75%+)
   - Taxa de visualização de preços
5. **Salvar como:** "Qualidade do Tráfego"

---

## 🎨 PASSO 3: CRIAR DASHBOARD NO LOOKER STUDIO

### Configuração do Dashboard Executivo:

1. **Acesse:** https://lookerstudio.google.com/

2. **Criar Relatório**
   - Botão **"Criar"** → **"Relatório"**
   - Conectar: Google Analytics 4
   - Selecionar propriedade: RIP PET (G-LS0H2KX8EF)

3. **Estrutura do Dashboard:**

---

#### SEÇÃO 1: KPIs PRINCIPAIS (Topo)

**Scorecards (4 colunas):**

| Métrica | Fórmula | Comparação |
|---------|---------|------------|
| Visitantes Únicos | Usuários ativos | vs mês anterior |
| Leads Totais | Contagem eventos (click_whatsapp + click_phone) | vs mês anterior |
| Taxa de Conversão | (Leads / Visitantes) × 100 | vs mês anterior |
| Tempo Médio | Tempo médio de engajamento | vs mês anterior |

---

#### SEÇÃO 2: FUNIL DE CONVERSÃO (Visual)

**Gráfico de Funil:**
- Dados: Etapas do funil
- Métrica: Contagem de usuários
- Visualização: Funil vertical com %

```
100% - Visitaram o site (page_view)
  ↓
 X% - Engajaram (scroll 50%+)
  ↓
 X% - Viram preços (view_pricing)
  ↓
 X% - Converteram (click_whatsapp/phone)
```

---

#### SEÇÃO 3: PERFORMANCE POR CANAL

**Tabela com dados:**

| Canal | Visitantes | Leads | Taxa Conv | Custo/Lead* |
|-------|------------|-------|-----------|-------------|
| Orgânico | X | X | X% | R$ - |
| Google Ads | X | X | X% | R$ XX |
| Facebook | X | X | X% | R$ XX |
| Instagram | X | X | X% | R$ XX |
| Direto | X | X | X% | R$ - |

\*Custo/Lead = Investimento em ads ÷ leads gerados

**Gráfico de Pizza:** Distribuição de leads por canal

---

#### SEÇÃO 4: PERFORMANCE POR UNIDADE

**Gráfico de Barras Horizontal:**
- Dimensão: unit_label
- Métrica: Contagem (click_whatsapp + click_phone)
- Ordenar: Decrescente

**Tabela detalhada:**

| Unidade | WhatsApp | Telefone | Total | % do Total |
|---------|----------|----------|-------|------------|
| São Paulo | X | X | X | XX% |
| Santos | X | X | X | XX% |
| Campinas | X | X | X | XX% |
| Vale Paraíba | X | X | X | XX% |
| Região Lagos | X | X | X | XX% |

---

#### SEÇÃO 5: ANÁLISE TEMPORAL

**Gráfico de Linha (Série Temporal):**
- Eixo X: Data (dia)
- Eixo Y: Leads gerados
- Linha 1: click_whatsapp
- Linha 2: click_phone
- Linha 3: Total

**Mapa de Calor (Horários):**
- Linhas: Dia da semana
- Colunas: Hora do dia
- Cor: Intensidade de conversões

**Insights:**
- Melhor dia para investir em ads
- Horário de pico de conversões
- Planejamento de equipe

---

#### SEÇÃO 6: DISPOSITIVOS E COMPORTAMENTO

**Gráfico de Rosca:**
- Mobile vs Desktop vs Tablet
- Métrica: Leads gerados

**Tabela comparativa:**

| Dispositivo | Visitantes | Taxa Conv | Tempo Médio |
|-------------|------------|-----------|-------------|
| Mobile | X | X% | Xm XXs |
| Desktop | X | X% | Xm XXs |
| Tablet | X | X% | Xm XXs |

---

#### SEÇÃO 7: ENGAJAMENTO COM CONTEÚDO

**Gráfico de Barras:**
- Seções mais visualizadas (section_view)
- Perguntas FAQ mais clicadas (faq_click)
- Reviews mais expandidos

**Métrica de Qualidade:**
- % de usuários que scrollam 75%+
- Tempo médio na seção de serviços
- Taxa de visualização de depoimentos

---

### 4. **Configurar Filtros Globais:**

- **Período:** Últimos 30 dias (ajustável)
- **Origem/Mídia:** Todos (com opção de filtrar)
- **Dispositivo:** Todos (com opção de filtrar)

### 5. **Salvar e Compartilhar:**

- Nome: **"RIP PET - Dashboard Executivo"**
- Compartilhar com sócios (somente visualização)
- Agendar envio por email (semanal)

---

## 📧 PASSO 4: CONFIGURAR RELATÓRIOS AUTOMÁTICOS

### Relatório Semanal (Email):

1. **No Looker Studio:**
   - Abra o dashboard
   - Clique em **"Compartilhar"** → **"Agendar envio de email"**

2. **Configurações:**
   - **Frequência:** Toda segunda-feira, 9h
   - **Destinatários:** Você + sócios
   - **Formato:** PDF
   - **Assunto:** "RIP PET - Relatório Semanal de Performance"

3. **Conteúdo do Email:**
   - Resumo de KPIs da semana
   - Comparação vs semana anterior
   - Top 3 canais geradores de leads
   - Unidade com melhor performance

---

### Alertas Personalizados (GA4):

1. **Google Analytics 4:**
   - Menu: **Configurar** → **Eventos** → **Criar evento personalizado**

2. **Criar alerta: "Queda de Conversões"**
   - Condição: Leads < 70% da média semanal
   - Notificar: Email imediato
   - Destinatários: Você

3. **Criar alerta: "Pico de Tráfego"**
   - Condição: Visitantes > 150% da média diária
   - Notificar: Email
   - Uso: Detectar viralização ou problemas técnicos

---

## 🔍 PASSO 5: VERIFICAR SE ESTÁ FUNCIONANDO

### Teste Imediato (após deploy):

1. **Abra o site:** https://rippet.com.br/

2. **Abra o Console do Navegador:**
   - Pressione `F12` (Chrome/Edge)
   - Vá na aba **"Console"**

3. **Você deve ver:**
   ```
   🚀 Iniciando Analytics Avançado RIP PET...
   ✅ Analytics Avançado Configurado!
   📊 Eventos disponíveis: [...]
   ```

4. **Teste os eventos:**
   - **Scroll na página:** Deve aparecer `📜 Scroll: 25%`, `📜 Scroll: 50%`, etc.
   - **Ver seção de serviços:** `👁️ Section Viewed: servicos`
   - **Clicar em WhatsApp:** `📊 WhatsApp Click: { unit: 'São Paulo', ... }`
   - **Clicar em telefone:** `📞 Phone Click: { ... }`

5. **Verificar no GA4 (tempo real):**
   - Google Analytics 4 → **Relatórios** → **Tempo real**
   - Você deve ver os eventos sendo disparados em tempo real

---

## 📊 PASSO 6: ANALISAR DADOS E TOMAR DECISÕES

### Após 7 dias de coleta:

#### Perguntas que você consegue responder:

1. **Qual canal traz mais leads?**
   - Dashboard → Seção "Performance por Canal"
   - Decisão: Investir mais no canal vencedor

2. **Qual unidade está com baixa performance?**
   - Dashboard → Seção "Performance por Unidade"
   - Decisão: Revisar atendimento ou marketing local

3. **Mobile ou Desktop converte mais?**
   - Dashboard → Seção "Dispositivos"
   - Decisão: Otimizar experiência do dispositivo vencedor

4. **Qual horário gera mais leads?**
   - Dashboard → Mapa de Calor Temporal
   - Decisão: Agendar posts e ads nos horários de pico

5. **Onde os usuários desistem no funil?**
   - Dashboard → Funil de Conversão
   - Decisão: Otimizar etapa com maior queda

6. **Qual conteúdo engaja mais?**
   - Dashboard → Engajamento com Conteúdo
   - Decisão: Destacar seções populares, melhorar as ignoradas

---

### Após 30 dias de coleta:

#### Análises Avançadas:

1. **ROI por Canal:**
   ```
   ROI = (Receita gerada - Investimento) / Investimento × 100
   ```

   Exemplo:
   - Google Ads: Investiu R$ 1.000, gerou 20 leads → R$ 50/lead
   - Orgânico: Investiu R$ 0, gerou 15 leads → R$ 0/lead
   - **Decisão:** Aumentar investimento em Google Ads se ROI > 300%

2. **Previsão de Leads Mensais:**
   - Usar tendência de 30 dias
   - Projetar próximo mês
   - Planejar capacidade de atendimento

3. **Segmentação de Público:**
   - Criar públicos personalizados:
     - "Visitou preços mas não converteu" (remarketing)
     - "Passou 3+ min no site" (público quente)
     - "Clicou WhatsApp de Campinas" (leads por região)

4. **Benchmark Interno:**
   - Taxa de conversão atual: X%
   - Meta trimestral: X% + 20%
   - Acompanhamento semanal

---

## 🎯 PRÓXIMOS PASSOS (OPCIONAL - FASE 2)

### Integrações Avançadas:

1. **Google Tag Manager**
   - Facilita mudanças sem mexer no código
   - Testes A/B mais rápidos

2. **CRM Integration**
   - Zapier ou Make.com
   - Enviar leads para planilha/CRM automaticamente
   - Fechar o ciclo: Lead → Orçamento → Venda

3. **Heatmaps (Hotjar/Clarity)**
   - Ver onde usuários clicam
   - Identificar problemas de UX
   - Otimizar layout

4. **Facebook Pixel Ativado**
   - Remarketing inteligente
   - Lookalike audiences
   - Otimização de campanhas

---

## 📞 GLOSSÁRIO DE TERMOS

- **Conversão:** Quando visitante vira lead (clica WhatsApp/telefone)
- **Taxa de Conversão:** % de visitantes que convertem
- **CAC (Custo de Aquisição de Cliente):** Quanto custa conseguir 1 cliente
- **LTV (Lifetime Value):** Valor que cliente traz ao longo do tempo
- **ROI (Return on Investment):** Retorno sobre investimento
- **Funil:** Jornada do usuário até conversão
- **Engagement:** Engajamento (scroll, tempo, interações)
- **Bounce Rate:** Taxa de rejeição (saiu sem interagir)
- **Session Duration:** Tempo de sessão/visita

---

## 🆘 TROUBLESHOOTING

### Eventos não aparecem no GA4:

1. **Aguarde 24-48h:** GA4 pode demorar para processar novos eventos
2. **Verifique Console:** Procure erros no console do navegador
3. **Teste em anônimo:** Cache pode estar atrapalhando
4. **Confirme ID correto:** G-LS0H2KX8EF deve estar no código

### Dashboard vazio:

1. **Aguarde coleta de dados:** Mínimo 7 dias para insights valiosos
2. **Verifique conexão:** Looker Studio conectado à propriedade correta
3. **Filtros:** Remova filtros de data muito restritivos

### Números não batem:

1. **Tempo real vs Relatórios:** Tempo real pode ter delay
2. **Filtros de spam:** GA4 remove bots automaticamente
3. **Amostragem:** Em alto volume, GA4 pode usar amostragem

---

## ✅ CHECKLIST FINAL

- [ ] Analytics avançado implementado e testado
- [ ] Eventos aparecem no Console do navegador
- [ ] Eventos aparecem no GA4 Tempo Real
- [ ] Conversões configuradas no GA4
- [ ] Dashboard criado no Looker Studio
- [ ] Relatório semanal agendado
- [ ] Alertas configurados
- [ ] Equipe treinada para usar dashboard

---

**Parabéns! Você agora tem um sistema de analytics de nível enterprise!** 🚀

Qualquer dúvida, consulte este guia ou verifique a documentação oficial do GA4.
