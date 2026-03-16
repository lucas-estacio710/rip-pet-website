/**
 * =====================================================
 * RIP PET - LEAD CAPTURE POPUP (v2)
 * =====================================================
 *
 * Árvore de conversa (WhatsApp):
 *   1. Saudação → tipo (botões)
 *   2a. EMERGÊNCIA: cidade → espécie → (se cachorro: grande porte?) → nome → redirect
 *   2b. PREVENTIVO: cidade → nome → redirect
 *
 * Árvore de conversa (Telefone — simplificado):
 *   1. Saudação → tipo (botões)
 *   2. Cidade → nome → redirect (sem espécie/porte)
 *
 * Salva no Supabase via REST (fire-and-forget).
 * Se fechar popup → redireciona direto sem salvar.
 *
 * =====================================================
 */

(function () {
  'use strict';

  // ===== CONFIG =====
  var SUPABASE_URL = 'https://eniplfcuwvhovxybyuey.supabase.co';
  var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVuaXBsZmN1d3Zob3Z4eWJ5dWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk5MDM1MjIsImV4cCI6MjA3NTQ3OTUyMn0.VFftjEVtd4_Vwa2KnrY0YizC_9xBATpe0z14X-7I6Is';

  var CIDADES = [
    'Santos', 'Praia Grande', 'Guarujá',
    'São Vicente', 'Cubatão', 'Itanhaém',
    'Mongaguá', 'Bertioga', 'Peruíbe'
  ];

  // ===== ESTADO =====
  var capturedParams = {};
  var currentChannel = null;    // 'whatsapp' | 'telefone'
  var originalHref = null;
  var originalElement = null;
  var pageLoadTime = Date.now();
  var popupOpenCount = 0;

  // Dados do lead (preenchidos durante a conversa)
  var leadNome = '';
  var leadTipo = '';             // 'emergencial' | 'preventivo'
  var leadCidade = '';
  var leadEspecie = '';          // 'cachorro' | 'gato' | 'exotico'
  var leadGrandePorte = null;    // true | false | null

  // ===== MÉTRICAS DE ENGAJAMENTO =====
  var maxScrollDepth = 0;
  var pageViews = 1;

  // Scroll depth tracker
  function trackScroll() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var docHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) - window.innerHeight;
    if (docHeight > 0) {
      var pct = Math.round((scrollTop / docHeight) * 100);
      if (pct > maxScrollDepth) maxScrollDepth = pct;
    }
  }
  window.addEventListener('scroll', trackScroll, { passive: true });

  // Page views counter (nesta sessão)
  try {
    var stored = sessionStorage.getItem('rp_page_views');
    pageViews = stored ? parseInt(stored, 10) + 1 : 1;
    sessionStorage.setItem('rp_page_views', pageViews.toString());
  } catch (e) { }

  // Detectar seção do CTA clicado
  function detectSection(el) {
    var section = el.closest('section[id], div[id]');
    if (section && section.id) return section.id;
    // Fallback: posição na página
    var rect = el.getBoundingClientRect();
    var y = rect.top + window.pageYOffset;
    var totalH = document.body.scrollHeight;
    if (y < totalH * 0.15) return 'hero';
    if (y > totalH * 0.85) return 'footer';
    return null;
  }

  // ===== CAPTURA DE GCLID/UTM =====
  function captureUrlParams() {
    var params = new URLSearchParams(window.location.search);
    var keys = ['gclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term'];

    keys.forEach(function (key) {
      var val = params.get(key);
      if (val) {
        capturedParams[key] = val;
        try { sessionStorage.setItem('rp_' + key, val); } catch (e) { }
      }
    });

    // Fallback: sessionStorage
    if (!capturedParams.gclid) {
      keys.forEach(function (key) {
        try {
          var stored = sessionStorage.getItem('rp_' + key);
          if (stored) capturedParams[key] = stored;
        } catch (e) { }
      });
    }
  }

  // ===== EXTRAIR TELEFONE =====
  function extractPhone(href) {
    if (!href) return null;
    var match = href.match(/wa\.me\/(\d+)/) || href.match(/tel:\+?(\d+)/);
    return match ? match[1] : null;
  }

  // ===== SALVAR NO SUPABASE (RPC — retorna protocolo) =====
  function saveLead() {
    var body = {
      nome: leadNome,
      cidade: leadCidade,
      canal: currentChannel,
      telefone_destino: extractPhone(originalHref),
      tipo_atendimento: leadTipo || null,
      especie_pet: leadEspecie || null,
      grande_porte: leadGrandePorte,
      gclid: capturedParams.gclid || null,
      utm_source: capturedParams.utm_source || null,
      utm_medium: capturedParams.utm_medium || null,
      utm_campaign: capturedParams.utm_campaign || null,
      utm_term: capturedParams.utm_term || null,
      pagina_origem: window.location.pathname,
      dispositivo: window.innerWidth < 768 ? 'mobile' : 'desktop',
      tempo_pagina_seg: Math.round((Date.now() - pageLoadTime) / 1000),
      scroll_depth: maxScrollDepth,
      page_views: pageViews,
      secao_clique: detectSection(originalElement)
    };

    try {
      return fetch(SUPABASE_URL + '/rest/v1/rpc/insert_lead', {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lead_data: body })
      })
      .then(function (res) { return res.json(); })
      .then(function (protocolo) {
        return (typeof protocolo === 'string') ? protocolo : null;
      })
      .catch(function () { return null; });
    } catch (e) {
      return Promise.resolve(null);
    }
  }

  // ===== MONTAR MENSAGEM WHATSAPP =====
  function buildWhatsAppMessage(protocolo) {
    var msg;

    // Lead direto (pulou o popup)
    if (!leadTipo) {
      msg = 'Olá, vim pelo site da R.I.P. Pet Santos e preciso de atendimento.';

    // Emergencial completo
    } else if (leadTipo === 'emergencial') {
      var especieLabel = leadEspecie === 'cachorro' ? 'cachorro'
        : leadEspecie === 'gato' ? 'gato'
        : 'pet exótico';

      msg = 'Olá, meu nome é ' + leadNome
        + ', estava no site da R.I.P. Pet Santos e preciso de atendimento emergencial para meu '
        + especieLabel + '.';

      if (leadGrandePorte === true) {
        msg += ' Ele é de grande porte.';
      }

      msg += ' Estou em ' + leadCidade + '.';

    // Preventivo completo
    } else {
      msg = 'Olá, meu nome é ' + leadNome
        + ', estava no site da R.I.P. Pet Santos e preciso de informações sobre os planos preventivos que oferecem. Sou de '
        + leadCidade + '.';
    }

    if (protocolo) {
      msg += ' [Protocolo: ' + protocolo + (capturedParams.gclid ? '*' : '') + ']';
    }

    return msg;
  }

  // ===== REDIRECT FINAL =====
  function doRedirect(protocolo) {
    // Analytics
    if (window.RIPPETAnalytics && originalElement) {
      if (currentChannel === 'whatsapp') {
        window.RIPPETAnalytics.trackWhatsAppClick(originalElement);
      } else {
        window.RIPPETAnalytics.trackPhoneClick(originalElement);
      }
    }

    var url;
    if (currentChannel === 'whatsapp') {
      var phone = extractPhone(originalHref) || '5513998068262';
      var msg = buildWhatsAppMessage(protocolo);
      url = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(msg);
    } else {
      url = originalHref;
    }

    window.location.href = url;
  }

  // ===== POPUP HTML =====
  function injectPopupStyles() {
    if (document.getElementById('leadCaptureStyles')) return;
    var style = document.createElement('style');
    style.id = 'leadCaptureStyles';
    style.textContent = ''
      + '#leadCaptureCard{'
      + '  position:fixed;z-index:99999;overflow:hidden;width:100%;'
      + '  box-shadow:0 4px 30px rgba(0,0,0,0.3);'
      + '  transition:transform 0.4s cubic-bezier(0.16,1,0.3,1);'
      + '  font-family:Poppins,sans-serif;'
      + '}'
      + '@media(max-width:767px){'
      + '  #leadCaptureCard{'
      + '    top:0;left:0;right:0;'
      + '    border-radius:0 0 20px 20px;'
      + '    transform:translateY(-100%);'
      + '  }'
      + '  #leadCaptureCard.lc-open{transform:translateY(0)}'
      + '  #leadCaptureChat{min-height:180px;max-height:55vh}'
      + '}'
      + '@media(min-width:768px){'
      + '  #leadCaptureCard{'
      + '    top:40px;left:50%;max-width:480px;'
      + '    border-radius:20px;'
      + '    transform:translateX(-50%) translateY(-120%);'
      + '  }'
      + '  #leadCaptureCard.lc-open{transform:translateX(-50%) translateY(0)}'
      + '  #leadCaptureChat{min-height:280px;max-height:60vh}'
      + '}';
    document.head.appendChild(style);
  }

  function createPopupHTML() {
    injectPopupStyles();

    var el = document.createElement('div');
    el.id = 'leadCaptureOverlay';
    el.innerHTML = ''
      + '<div id="leadCaptureOverlay-bg" style="position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:99998;opacity:0;transition:opacity 0.3s"></div>'
      + '<div id="leadCaptureCard">'
      // Header
      + '<div style="background:#075E54;padding:16px 20px;display:flex;align-items:center;gap:12px">'
      + '  <img src="/assets/logo_rounded.png" alt="R.I.P. Pet" style="width:40px;height:40px;border-radius:50%;object-fit:cover">'
      + '  <div style="flex:1">'
      + '    <div style="color:#fff;font-weight:600;font-size:15px">R.I.P. Pet Santos</div>'
      + '    <div style="color:#8ABBB0;font-size:12px">Atendimento 24h</div>'
      + '  </div>'
      + '  <button id="leadCaptureClose" style="background:none;border:none;color:#fff;font-size:24px;cursor:pointer;padding:4px 8px;line-height:1" aria-label="Fechar">&times;</button>'
      + '</div>'
      // Chat area
      + '<div id="leadCaptureChat" style="background:#ECE5DD;padding:16px 16px 12px;overflow-y:auto;display:flex;flex-direction:column;gap:8px">'
      + '</div>'
      // Input area (visível apenas no step do nome)
      + '<div id="leadCaptureInput" style="background:#F0F0F0;padding:10px 12px;display:flex;flex-direction:column;gap:6px">'
      + '  <div style="display:flex;gap:8px;align-items:center">'
      + '    <input id="leadNameInput" type="text" placeholder="Ex: Maria" maxlength="60" '
      + '      style="flex:1;padding:10px 16px;border-radius:24px;border:none;font-size:15px;font-family:Poppins,sans-serif;outline:none;background:#fff" '
      + '      autocomplete="given-name">'
      + '    <button id="leadNameSend" style="width:44px;height:44px;border-radius:50%;background:#075E54;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0">'
      + '      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="#fff"/></svg>'
      + '    </button>'
      + '  </div>'
      + '  <a id="leadDirectLink" style="display:none;text-align:center;font-size:12px;color:#075E54;text-decoration:underline;cursor:pointer;padding:2px 0;font-family:Poppins,sans-serif">Fale diretamente</a>'
      + '  <p id="leadLgpdNotice" style="text-align:center;font-size:10px;color:#999;margin:0;padding:2px 0;font-family:Poppins,sans-serif">Ao prosseguir, você concorda com nossa <a href="/politica-de-privacidade" target="_blank" style="color:#075E54;text-decoration:underline">Política de Privacidade</a></p>'
      + '</div>'
      + '</div>';

    document.body.appendChild(el);
    return el;
  }

  // ===== ADICIONAR BALÃO =====
  function addBubble(text, isBot, callback) {
    var chat = document.getElementById('leadCaptureChat');
    if (!chat) return;

    var bubble = document.createElement('div');
    bubble.style.cssText = isBot
      ? 'background:#fff;color:#303030;padding:10px 14px;border-radius:0 12px 12px 12px;max-width:85%;align-self:flex-start;font-size:14px;line-height:1.5;box-shadow:0 1px 2px rgba(0,0,0,0.1)'
      : 'background:#DCF8C6;color:#303030;padding:10px 14px;border-radius:12px 0 12px 12px;max-width:85%;align-self:flex-end;font-size:14px;line-height:1.5;box-shadow:0 1px 2px rgba(0,0,0,0.1)';
    bubble.textContent = text;

    bubble.style.opacity = '0';
    bubble.style.transform = 'translateY(10px)';
    bubble.style.transition = 'opacity 0.3s, transform 0.3s';
    chat.appendChild(bubble);
    chat.scrollTop = chat.scrollHeight;

    requestAnimationFrame(function () {
      bubble.style.opacity = '1';
      bubble.style.transform = 'translateY(0)';
    });

    if (callback) {
      setTimeout(callback, 400);
    }
  }

  // ===== MOSTRAR BOTÕES DE OPÇÃO =====
  function showOptionButtons(options, onSelect) {
    var chat = document.getElementById('leadCaptureChat');
    var inputArea = document.getElementById('leadCaptureInput');
    if (!chat) return;
    if (inputArea) inputArea.style.display = 'none';

    var wrapper = document.createElement('div');
    wrapper.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px;padding:4px 0;width:100%;justify-content:center';

    options.forEach(function (opt) {
      var btn = document.createElement('button');
      btn.textContent = opt.label;
      btn.style.cssText = 'padding:10px 16px;border-radius:10px;border:2px solid #075E54;background:#fff;color:#075E54;font-size:14px;font-weight:600;cursor:pointer;font-family:Poppins,sans-serif;transition:all 0.2s;line-height:1.2;min-width:120px';
      btn.addEventListener('mouseenter', function () {
        this.style.background = '#075E54';
        this.style.color = '#fff';
      });
      btn.addEventListener('mouseleave', function () {
        this.style.background = '#fff';
        this.style.color = '#075E54';
      });
      btn.addEventListener('click', function () {
        // Desabilitar todos os botões
        wrapper.querySelectorAll('button').forEach(function (b) {
          b.disabled = true;
          b.style.opacity = '0.5';
          b.style.cursor = 'default';
        });
        // Destacar o selecionado
        this.style.background = '#075E54';
        this.style.color = '#fff';
        this.style.opacity = '1';

        onSelect(opt.value);
      });
      wrapper.appendChild(btn);
    });

    // Animação
    wrapper.style.opacity = '0';
    wrapper.style.transform = 'translateY(10px)';
    wrapper.style.transition = 'opacity 0.3s, transform 0.3s';
    chat.appendChild(wrapper);
    chat.scrollTop = chat.scrollHeight;

    requestAnimationFrame(function () {
      wrapper.style.opacity = '1';
      wrapper.style.transform = 'translateY(0)';
    });
  }

  // ===== MOSTRAR GRID DE CIDADES =====
  function showCityGrid(onSelect) {
    var chat = document.getElementById('leadCaptureChat');
    var inputArea = document.getElementById('leadCaptureInput');
    if (!chat) return;
    if (inputArea) inputArea.style.display = 'none';

    var grid = document.createElement('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:4px 0;width:100%';

    CIDADES.forEach(function (cidade) {
      var btn = document.createElement('button');
      btn.textContent = cidade;
      btn.style.cssText = 'padding:10px 6px;border-radius:10px;border:2px solid #075E54;background:#fff;color:#075E54;font-size:13px;font-weight:600;cursor:pointer;font-family:Poppins,sans-serif;transition:all 0.2s;line-height:1.2';
      btn.addEventListener('mouseenter', function () {
        this.style.background = '#075E54';
        this.style.color = '#fff';
      });
      btn.addEventListener('mouseleave', function () {
        this.style.background = '#fff';
        this.style.color = '#075E54';
      });
      btn.addEventListener('click', function () {
        // Desabilitar todos
        grid.querySelectorAll('button').forEach(function (b) {
          b.disabled = true;
          b.style.opacity = '0.5';
          b.style.cursor = 'default';
        });
        this.style.background = '#075E54';
        this.style.color = '#fff';
        this.style.opacity = '1';

        onSelect(cidade);
      });
      grid.appendChild(btn);
    });

    // Animação
    grid.style.opacity = '0';
    grid.style.transform = 'translateY(10px)';
    grid.style.transition = 'opacity 0.3s, transform 0.3s';
    chat.appendChild(grid);
    chat.scrollTop = chat.scrollHeight;

    requestAnimationFrame(function () {
      grid.style.opacity = '1';
      grid.style.transform = 'translateY(0)';
    });
  }

  // ===========================================================
  // FLUXO DA CONVERSA
  // ===========================================================

  // STEP 1: Saudação + tipo de atendimento (botões)
  function stepSaudacao() {
    var saudacao = currentChannel === 'telefone'
      ? 'Olá, aqui é da R.I.P. Pet Santos. Já vamos te conectar com nossa linha direta. Só precisamos de algumas informações rápidas.'
      : 'Olá, aqui é da R.I.P. Pet Santos. Estamos aqui para oferecer todo suporte que precisar.';

    addBubble(saudacao, true, function () {
      addBubble('Como podemos te ajudar?', true, function () {
        showOptionButtons([
          { label: 'Emergência / Falecimento', value: 'emergencial' },
          { label: 'Planos Preventivos', value: 'preventivo' }
        ], function (tipo) {
          leadTipo = tipo;
          addBubble(tipo === 'emergencial' ? 'Emergência / Falecimento' : 'Planos Preventivos', false);

          if (tipo === 'emergencial') {
            setTimeout(stepCidadeEmergencial, 500);
          } else {
            setTimeout(stepCidadePreventivo, 500);
          }
        });
      });
    });
  }

  // STEP 2a: Sentimentos + Cidade (emergencial)
  function stepCidadeEmergencial() {
    addBubble('Meus sentimentos pelo momento \uD83D\uDE4F\uD83C\uDFFB\uD83E\uDE75', true, function () {
    addBubble('Em qual cidade precisa do atendimento?', true, function () {
      showCityGrid(function (cidade) {
        leadCidade = cidade;
        addBubble(cidade, false);
        // Telefone: pula espécie/porte (info não chega na ligação)
        if (currentChannel === 'telefone') {
          setTimeout(stepNome, 500);
        } else {
          setTimeout(stepEspecie, 500);
        }
      });
    });
    });
  }

  // STEP 2b: Cidade (preventivo) → nome
  function stepCidadePreventivo() {
    addBubble('Qual sua cidade?', true, function () {
      showCityGrid(function (cidade) {
        leadCidade = cidade;
        addBubble(cidade, false);
        setTimeout(stepNome, 500);
      });
    });
  }

  // STEP 3: Espécie do pet (só emergencial)
  function stepEspecie() {
    addBubble('O petzinho é um:', true, function () {
      showOptionButtons([
        { label: 'Cachorro', value: 'cachorro' },
        { label: 'Gato', value: 'gato' },
        { label: 'Exótico', value: 'exotico' }
      ], function (especie) {
        leadEspecie = especie;
        var label = especie === 'cachorro' ? 'Cachorro' : especie === 'gato' ? 'Gato' : 'Exótico';
        addBubble(label, false);

        if (especie === 'cachorro') {
          setTimeout(stepGrandePorte, 500);
        } else {
          leadGrandePorte = null;
          setTimeout(stepNome, 500);
        }
      });
    });
  }

  // STEP 4: Grande porte (só cachorro)
  function stepGrandePorte() {
    addBubble('Possui grande porte? Acima de 45kg?', true, function () {
      showOptionButtons([
        { label: 'Sim', value: 'sim' },
        { label: 'Não', value: 'nao' }
      ], function (resposta) {
        leadGrandePorte = resposta === 'sim';
        addBubble(resposta === 'sim' ? 'Sim' : 'Não', false);
        setTimeout(stepNome, 500);
      });
    });
  }

  // STEP 5: Nome (campo de texto — por último)
  function stepNome() {
    var nameInput = document.getElementById('leadNameInput');
    if (nameInput) nameInput.value = '';

    addBubble('Para finalizar, qual seu nome?', true, function () {
      var inputArea = document.getElementById('leadCaptureInput');
      if (inputArea) inputArea.style.display = 'flex';
      if (nameInput) nameInput.focus();
    });
  }

  // STEP FINAL: Salvar + countdown + protocolo + redirect
  function stepFinalizar() {
    // Track lead completo
    try {
      if (window.gtag) {
        window.gtag('event', 'popup_lead_completed', {
          event_category: 'lead_capture',
          canal: currentChannel,
          tipo: leadTipo,
          cidade: leadCidade
        });
      }
      if (window.fbq) {
        window.fbq('track', 'Lead', { content_name: 'popup_' + leadTipo });
      }
    } catch (e) { }

    // Dispara save imediatamente — 3s do countdown mascaram a latência
    var protocolo = null;
    var savePromise = saveLead();
    savePromise.then(function (p) { protocolo = p; });

    var msgFinal;
    if (currentChannel === 'telefone') {
      msgFinal = leadTipo === 'emergencial'
        ? 'Vamos te conectar direto com nossa equipe, ' + leadNome + '.'
        : '\u00D3timo, ' + leadNome + '! Conectando sua ligação.';
    } else {
      msgFinal = leadTipo === 'emergencial'
        ? 'Vamos te conectar com nossa equipe, ' + leadNome + '.'
        : '\u00D3timo, ' + leadNome + '! Vamos te conectar com nossa equipe.';
    }

    addBubble(msgFinal, true, function () {
      var chat = document.getElementById('leadCaptureChat');
      if (!chat) { closePopup(); doRedirect(null); return; }

      var bubble = document.createElement('div');
      bubble.style.cssText = 'background:#fff;color:#303030;padding:10px 14px;border-radius:0 12px 12px 12px;max-width:85%;align-self:flex-start;font-size:14px;line-height:1.5;box-shadow:0 1px 2px rgba(0,0,0,0.1)';
      chat.appendChild(bubble);
      chat.scrollTop = chat.scrollHeight;

      var count = 3;
      var countdownPrefix = currentChannel === 'telefone'
        ? 'Discando em ' : 'Conectando com nosso atendimento em ';
      bubble.textContent = countdownPrefix + count + '...';

      var interval = setInterval(function () {
        count--;
        if (count > 0) {
          bubble.textContent = countdownPrefix + count + '...';
        } else {
          clearInterval(interval);
          if (protocolo) {
            var protocoloDisplay = protocolo + (capturedParams.gclid ? '*' : '');
            bubble.textContent = 'Protocolo: ' + protocoloDisplay;
            chat.scrollTop = chat.scrollHeight;
            setTimeout(function () {
              closePopup();
              doRedirect(protocolo);
            }, 1000);
          } else {
            closePopup();
            doRedirect(null);
          }
        }
      }, 1000);
    });
  }

  // ===========================================================
  // POPUP CONTROLS
  // ===========================================================

  function openPopup(channel, href, element) {
    currentChannel = channel;
    originalHref = href;
    originalElement = element;
    popupOpenCount++;

    // Reset estado
    leadNome = '';
    leadTipo = '';
    leadCidade = '';
    leadEspecie = '';
    leadGrandePorte = null;

    // Criar popup se não existe
    if (!document.getElementById('leadCaptureOverlay')) {
      createPopupHTML();
      setupPopupEvents();
    }

    // Limpar chat anterior
    var chat = document.getElementById('leadCaptureChat');
    if (chat) chat.innerHTML = '';

    // Esconder input até a hora certa
    var inputArea = document.getElementById('leadCaptureInput');
    if (inputArea) inputArea.style.display = 'none';

    // "Fale diretamente" — só a partir da 2a abertura
    var directLink = document.getElementById('leadDirectLink');
    if (directLink) {
      directLink.style.display = popupOpenCount >= 2 ? 'block' : 'none';
    }

    // Mostrar overlay
    var overlay = document.getElementById('leadCaptureOverlay');
    if (overlay) overlay.style.display = 'block';

    // Track popup aberto (GA4 + Meta Pixel)
    try {
      if (window.gtag) {
        window.gtag('event', 'popup_lead_opened', {
          event_category: 'lead_capture',
          canal: currentChannel,
          abertura_numero: popupOpenCount
        });
      }
      if (window.fbq) {
        window.fbq('trackCustom', 'LeadPopupOpened', {
          canal: currentChannel,
          abertura: popupOpenCount
        });
      }
    } catch (e) { }

    // Animar entrada
    requestAnimationFrame(function () {
      var bg = document.getElementById('leadCaptureOverlay-bg');
      var card = document.getElementById('leadCaptureCard');
      if (bg) bg.style.opacity = '1';
      if (card) card.classList.add('lc-open');

      // Iniciar conversa
      setTimeout(stepSaudacao, 400);
    });

    document.body.style.overflow = 'hidden';
  }

  function closePopup() {
    var bg = document.getElementById('leadCaptureOverlay-bg');
    var card = document.getElementById('leadCaptureCard');
    if (bg) bg.style.opacity = '0';
    if (card) card.classList.remove('lc-open');

    setTimeout(function () {
      var overlay = document.getElementById('leadCaptureOverlay');
      if (overlay) overlay.style.display = 'none';
    }, 400);

    document.body.style.overflow = '';
  }

  function closeAndRedirect() {
    // Track abandono
    try {
      if (window.gtag) {
        window.gtag('event', 'popup_lead_abandoned', {
          event_category: 'lead_capture',
          canal: currentChannel,
          step_abandonado: !leadTipo ? 'tipo' : !leadCidade ? 'cidade' : !leadNome ? 'nome' : 'especie'
        });
      }
    } catch (e) { }
    closePopup();
  }

  // ===== HANDLER: NOME ENVIADO =====
  function onNameSubmit() {
    var input = document.getElementById('leadNameInput');
    if (!input) return;

    var nome = input.value.trim();
    if (!nome) {
      input.focus();
      input.style.boxShadow = '0 0 0 2px #e74c3c';
      setTimeout(function () { input.style.boxShadow = 'none'; }, 1500);
      return;
    }

    leadNome = nome;

    // Esconder input
    var inputArea = document.getElementById('leadCaptureInput');
    if (inputArea) inputArea.style.display = 'none';

    // Mostrar resposta do user
    addBubble(nome, false);

    // Próximo passo — nome é o último step antes de finalizar
    setTimeout(stepFinalizar, 500);
  }

  // ===== SETUP EVENTOS =====
  function setupPopupEvents() {
    var closeBtn = document.getElementById('leadCaptureClose');
    if (closeBtn) closeBtn.addEventListener('click', closeAndRedirect);

    var bg = document.getElementById('leadCaptureOverlay-bg');
    if (bg) bg.addEventListener('click', closeAndRedirect);

    var sendBtn = document.getElementById('leadNameSend');
    if (sendBtn) sendBtn.addEventListener('click', onNameSubmit);

    var nameInput = document.getElementById('leadNameInput');
    if (nameInput) {
      nameInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          onNameSubmit();
        }
      });
    }

    // "Fale diretamente" — salva lead parcial com tracking + protocolo, redireciona
    var directLink = document.getElementById('leadDirectLink');
    if (directLink) {
      directLink.addEventListener('click', function () {
        // Preencher com placeholders o que não foi respondido
        leadNome = leadNome || '-';
        leadCidade = leadCidade || '-';

        // Salvar e esperar protocolo
        var savePromise = saveLead();
        savePromise.then(function (protocolo) {
          closePopup();
          doRedirect(protocolo);
        });
      });
    }
  }

  // ===== INTERCEPTAR CLIQUES =====
  function interceptClicks() {
    // WhatsApp
    document.querySelectorAll('a[href*="wa.me"]').forEach(function (link) {
      if (link.dataset.leadIntercepted) return;
      link.dataset.leadIntercepted = 'true';

      link.addEventListener('click', function (e) {
        if (!e.isTrusted) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        openPopup('whatsapp', this.href, this);
      }, { capture: true });
    });

    // Telefone
    document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
      if (link.dataset.leadIntercepted) return;
      link.dataset.leadIntercepted = 'true';

      link.addEventListener('click', function (e) {
        if (!e.isTrusted) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        openPopup('telefone', this.href, this);
      }, { capture: true });
    });
  }

  // ===== INIT =====
  function init() {
    captureUrlParams();

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', interceptClicks);
    } else {
      interceptClicks();
    }

    var observer = new MutationObserver(interceptClicks);
    observer.observe(document.body || document.documentElement, { childList: true, subtree: true });
  }

  init();
})();
