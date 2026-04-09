/**
 * =====================================================
 * RIP PET - LEAD CAPTURE POPUP (v3 — FUNIL COMPLETO)
 * =====================================================
 *
 * Tracking completo:
 *   - Session: toda visita registrada (geo, device, UTM, engajamento)
 *   - Funnel events: cada step do popup logado com duração
 *   - Abandonos: salvos no Supabase (não só GA4)
 *   - Leads parciais: criados ao abrir popup, atualizados a cada step
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
 * =====================================================
 */

(function () {
  'use strict';

  // ===== CONFIG =====
  var SUPABASE_URL = 'https://eniplfcuwvhovxybyuey.supabase.co';
  var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVuaXBsZmN1d3Zob3Z4eWJ5dWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk5MDM1MjIsImV4cCI6MjA3NTQ3OTUyMn0.VFftjEVtd4_Vwa2KnrY0YizC_9xBATpe0z14X-7I6Is';

  // Config por unidade (definida antes do script via window.LEAD_CAPTURE_CONFIG)
  var cfg = window.LEAD_CAPTURE_CONFIG || {};
  var UNIDADE = cfg.unidade || 'Santos';
  var CIDADES = cfg.cidades || [
    'Santos', 'Praia Grande', 'Guarujá',
    'São Vicente', 'Cubatão', 'Itanhaém',
    'Mongaguá', 'Bertioga', 'Peruíbe'
  ];
  var PHONE_FALLBACK = cfg.phoneFallback || '5513998068262';
  var PHONE_PLACEHOLDER = cfg.phonePlaceholder || '(13) 99999-0000';
  var UNIDADE_CODE = cfg.unidadeCode || 'ST';  // 2 chars: ST=Santos, SP=São Paulo
  var ASK_CIDADE = cfg.askCidade !== undefined ? cfg.askCidade : true;
  var ASK_GRANDE_PORTE = cfg.askGrandePorte !== undefined ? cfg.askGrandePorte : true;

  // ===== ESTADO =====
  var capturedParams = {};
  var currentChannel = null;    // 'whatsapp' | 'telefone'
  var originalHref = null;
  var originalElement = null;
  var pageLoadTime = Date.now();
  var popupOpenCount = 0;
  var popupOpenTime = 0;         // timestamp de quando abriu o popup
  var lastStepTime = 0;          // timestamp do último step (para calcular duração)
  var stepsCompleted = 0;
  var lastStepName = '';
  var funnelEvents = [];         // buffer de eventos para batch insert
  var popupCompleted = false;    // flag para evitar salvar abandono após completar

  // Dados do lead (preenchidos durante a conversa)
  var leadNome = '';
  var leadTipo = '';             // 'emergencial' | 'preventivo'
  var leadCidade = '';
  var leadEspecie = '';          // 'cachorro' | 'gato' | 'exotico'
  var leadGrandePorte = null;    // true | false | null
  var leadTelefone = '';          // telefone do lead (fluxo telefone)

  // ===== SESSION & VISITOR IDs =====
  var visitorId = '';
  var sessionId = '';

  function initIds() {
    try {
      visitorId = localStorage.getItem('rp_visitor_id');
      if (!visitorId) {
        visitorId = generateUUID();
        localStorage.setItem('rp_visitor_id', visitorId);
      }
      sessionId = sessionStorage.getItem('rp_session_id');
      if (!sessionId) {
        sessionId = generateUUID();
        sessionStorage.setItem('rp_session_id', sessionId);
      }
    } catch (e) {
      visitorId = generateUUID();
      sessionId = generateUUID();
    }
  }

  function generateUUID() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  // ===== GEOLOCALIZAÇÃO POR IP =====
  var geoData = { city: null, state: null, timezone: null };

  function detectGeo() {
    try {
      var cached = sessionStorage.getItem('rp_geo');
      if (cached) { geoData = JSON.parse(cached); return; }
    } catch (e) { }

    fetch('https://ipwho.is/?fields=city,region,timezone.id&lang=pt-BR')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.success !== false) {
          geoData.city = data.city || null;
          geoData.state = data.region || null;
          geoData.timezone = (data.timezone && data.timezone.id) || null;
          try { sessionStorage.setItem('rp_geo', JSON.stringify(geoData)); } catch (e) { }
        }
      })
      .catch(function () { });
  }

  // ===== DEVICE INFO =====
  function getDeviceType() {
    var w = window.innerWidth;
    if (w < 768) return 'mobile';
    if (w < 1024) return 'tablet';
    return 'desktop';
  }

  function getBrowser() {
    var ua = navigator.userAgent;
    if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) return 'Chrome';
    if (ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') === -1) return 'Safari';
    if (ua.indexOf('Firefox') > -1) return 'Firefox';
    if (ua.indexOf('Edg') > -1) return 'Edge';
    return 'Outro';
  }

  function getOS() {
    var ua = navigator.userAgent;
    if (ua.indexOf('Android') > -1) return 'Android';
    if (/iPhone|iPad|iPod/.test(ua)) return 'iOS';
    if (ua.indexOf('Windows') > -1) return 'Windows';
    if (ua.indexOf('Mac') > -1) return 'macOS';
    if (ua.indexOf('Linux') > -1) return 'Linux';
    return 'Outro';
  }

  // ===== MÉTRICAS DE ENGAJAMENTO =====
  var maxScrollDepth = 0;
  var pageViews = 1;
  var sectionsViewed = [];

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

  // Seções vistas (IntersectionObserver)
  function trackSections() {
    if (!('IntersectionObserver' in window)) return;
    var sections = document.querySelectorAll('section[id], div[id].section, [id$="-section"]');
    if (!sections.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
          var id = entry.target.id;
          if (id && sectionsViewed.indexOf(id) === -1) {
            sectionsViewed.push(id);
          }
        }
      });
    }, { threshold: 0.3 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  // Detectar seção do CTA clicado
  function detectSection(el) {
    if (!el) return null;
    var section = el.closest('section[id], div[id]');
    if (section && section.id) return section.id;
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

  // ===== SUPABASE HELPERS =====
  function supabaseRPC(fnName, payload) {
    try {
      return fetch(SUPABASE_URL + '/rest/v1/rpc/' + fnName, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(function (res) { return res.json(); })
      .catch(function () { return null; });
    } catch (e) {
      return Promise.resolve(null);
    }
  }

  // sendBeacon para garantir envio mesmo ao sair da página
  function supabaseBeacon(fnName, payload) {
    try {
      var url = SUPABASE_URL + '/rest/v1/rpc/' + fnName;
      var body = JSON.stringify(payload);
      if (navigator.sendBeacon) {
        var blob = new Blob([body], { type: 'application/json' });
        // sendBeacon não suporta headers custom, usar fetch com keepalive
        fetch(url, {
          method: 'POST',
          headers: { 'apikey': SUPABASE_KEY, 'Content-Type': 'application/json' },
          body: body,
          keepalive: true
        }).catch(function () { });
      } else {
        fetch(url, {
          method: 'POST',
          headers: { 'apikey': SUPABASE_KEY, 'Content-Type': 'application/json' },
          body: body
        }).catch(function () { });
      }
    } catch (e) { }
  }

  // ===== SESSION TRACKING =====
  function saveSession(ctaData) {
    var data = {
      visitor_id: visitorId,
      session_id: sessionId,
      landing_page: window.location.pathname + window.location.search,
      referrer: document.referrer || null,
      utm_source: capturedParams.utm_source || null,
      utm_medium: capturedParams.utm_medium || null,
      utm_campaign: capturedParams.utm_campaign || null,
      utm_term: capturedParams.utm_term || null,
      gclid: capturedParams.gclid || null,
      device_type: getDeviceType(),
      browser: getBrowser(),
      os: getOS(),
      screen_resolution: screen.width + 'x' + screen.height,
      viewport: window.innerWidth + 'x' + window.innerHeight,
      user_language: navigator.language || null,
      geo_city: geoData.city,
      geo_state: geoData.state,
      geo_timezone: geoData.timezone,
      max_scroll_depth: maxScrollDepth,
      time_on_page_sec: Math.round((Date.now() - pageLoadTime) / 1000),
      page_views: pageViews,
      sections_viewed: sectionsViewed,
      unidade_code: UNIDADE_CODE
    };

    // Adicionar dados de CTA se passou
    if (ctaData) {
      data.cta_clicked = true;
      data.cta_channel = ctaData.channel;
      data.cta_section = ctaData.section;
      data.cta_clicked_at = new Date().toISOString();
      data.popup_opened_count = popupOpenCount;
    }

    return supabaseRPC('upsert_session', { session_data: data });
  }

  // Salvar session periodicamente e ao sair
  var sessionSaveInterval = null;

  function startSessionTracking() {
    // Salvar session inicial (sem CTA)
    setTimeout(function () { saveSession(null); }, 2000);

    // Atualizar engajamento a cada 30s
    sessionSaveInterval = setInterval(function () {
      saveSession(null);
    }, 30000);

    // Salvar ao sair da página
    window.addEventListener('beforeunload', function () {
      supabaseBeacon('upsert_session', {
        session_data: {
          visitor_id: visitorId,
          session_id: sessionId,
          max_scroll_depth: maxScrollDepth,
          time_on_page_sec: Math.round((Date.now() - pageLoadTime) / 1000),
          page_views: pageViews,
          sections_viewed: sectionsViewed
        }
      });
    });
  }

  // ===== FUNNEL EVENTS =====
  function logFunnelEvent(eventType, eventValue, metadata) {
    var now = Date.now();
    var duration = lastStepTime ? now - lastStepTime : 0;
    lastStepTime = now;

    var event = {
      session_id: sessionId,
      event_type: eventType,
      event_value: eventValue || null,
      step_duration_ms: duration > 0 ? duration : null,
      metadata: metadata || null
    };

    funnelEvents.push(event);

    // Flush imediatamente para eventos importantes
    if (eventType === 'popup_abandoned' || eventType === 'popup_completed') {
      flushFunnelEvents();
    }
  }

  function flushFunnelEvents() {
    if (!funnelEvents.length) return;
    var batch = funnelEvents.slice();
    funnelEvents = [];
    supabaseBeacon('insert_funnel_events', { events: batch });
  }

  // ===== SALVAR LEAD COMPLETO (RPC — retorna protocolo) =====
  function saveLead() {
    var body = {
      nome: leadNome || null,
      cidade: leadCidade,
      canal: currentChannel,
      telefone_destino: extractPhone(originalHref),
      tipo_atendimento: leadTipo || null,
      especie_pet: leadEspecie || null,
      grande_porte: leadGrandePorte,
      telefone_lead: leadTelefone || null,
      gclid: capturedParams.gclid || null,
      utm_source: capturedParams.utm_source || null,
      utm_medium: capturedParams.utm_medium || null,
      utm_campaign: capturedParams.utm_campaign || null,
      utm_term: capturedParams.utm_term || null,
      pagina_origem: window.location.pathname,
      dispositivo: getDeviceType(),
      tempo_pagina_seg: Math.round((Date.now() - pageLoadTime) / 1000),
      scroll_depth: maxScrollDepth,
      page_views: pageViews,
      secao_clique: detectSection(originalElement),
      // Novos campos v3
      unidade_code: UNIDADE_CODE,
      status: 'completo',
      session_id: sessionId,
      visitor_id: visitorId,
      geo_city: geoData.city,
      geo_state: geoData.state,
      steps_completed: stepsCompleted,
      last_step: currentChannel === 'telefone' ? 'telefone' : 'nome',
      popup_duration_sec: Math.round((Date.now() - popupOpenTime) / 1000),
      funnel_duration_sec: Math.round((Date.now() - pageLoadTime) / 1000)
    };

    return supabaseRPC('insert_lead', { lead_data: body })
      .then(function (protocolo) {
        return (typeof protocolo === 'string') ? protocolo : null;
      });
  }

  // ===== SALVAR LEAD PARCIAL (abandono) =====
  function savePartialLead(abandonedAtStep) {
    var body = {
      canal: currentChannel,
      telefone_destino: extractPhone(originalHref),
      tipo_atendimento: leadTipo || null,
      especie_pet: leadEspecie || null,
      grande_porte: leadGrandePorte,
      telefone_lead: leadTelefone || null,
      nome: leadNome || null,
      cidade: leadCidade || null,
      gclid: capturedParams.gclid || null,
      utm_source: capturedParams.utm_source || null,
      utm_medium: capturedParams.utm_medium || null,
      utm_campaign: capturedParams.utm_campaign || null,
      utm_term: capturedParams.utm_term || null,
      pagina_origem: window.location.pathname,
      dispositivo: getDeviceType(),
      tempo_pagina_seg: Math.round((Date.now() - pageLoadTime) / 1000),
      scroll_depth: maxScrollDepth,
      page_views: pageViews,
      secao_clique: detectSection(originalElement),
      unidade_code: UNIDADE_CODE,
      status: 'abandonado',
      session_id: sessionId,
      visitor_id: visitorId,
      geo_city: geoData.city,
      geo_state: geoData.state,
      steps_completed: stepsCompleted,
      last_step: lastStepName || null,
      abandoned_at_step: abandonedAtStep,
      popup_duration_sec: Math.round((Date.now() - popupOpenTime) / 1000),
      funnel_duration_sec: Math.round((Date.now() - pageLoadTime) / 1000)
    };

    supabaseBeacon('save_partial_lead', { lead_data: body });
  }

  // ===== MONTAR MENSAGEM WHATSAPP =====
  function buildWhatsAppMessage(protocolo) {
    var msg;

    // Lead direto (pulou o popup)
    if (!leadTipo) {
      msg = 'Olá, vim pelo site da R.I.P. Pet ' + UNIDADE + ' e preciso de atendimento.';

    // Emergencial completo
    } else if (leadTipo === 'emergencial') {
      var especieLabel = leadEspecie === 'cachorro' ? 'cachorro'
        : leadEspecie === 'gato' ? 'gato'
        : 'pet exótico';

      msg = 'Olá, meu nome é ' + leadNome
        + ', estava no site da R.I.P. Pet ' + UNIDADE + ' e preciso de atendimento emergencial para meu '
        + especieLabel + '.';

      if (leadGrandePorte === true) {
        msg += ' Ele é de grande porte.';
      }

      if (leadCidade && leadCidade !== '-') {
        msg += ' Estou em ' + leadCidade + '.';
      }

    // Preventivo completo
    } else {
      msg = 'Olá, meu nome é ' + leadNome
        + ', estava no site da R.I.P. Pet ' + UNIDADE + ' e preciso de informações sobre os planos preventivos que oferecem.';
      if (leadCidade && leadCidade !== '-') {
        msg += ' Sou de ' + leadCidade + '.';
      }
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
      var phone = extractPhone(originalHref) || PHONE_FALLBACK;
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
      + '    <div style="color:#fff;font-weight:600;font-size:15px">R.I.P. Pet ' + UNIDADE + '</div>'
      + '    <div style="color:#8ABBB0;font-size:12px">Atendimento 24h</div>'
      + '  </div>'
      + '  <button id="leadCaptureClose" style="background:none;border:none;color:#fff;font-size:24px;cursor:pointer;padding:4px 8px;line-height:1" aria-label="Fechar">&times;</button>'
      + '</div>'
      // Chat area
      + '<div id="leadCaptureChat" style="background:#ECE5DD;padding:16px 16px 12px;overflow-y:auto;display:flex;flex-direction:column;gap:8px">'
      + '</div>'
      // Input area — nome (WhatsApp)
      + '<div id="leadCaptureInput" style="background:#F0F0F0;padding:10px 12px;display:none;flex-direction:column;gap:6px">'
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
      // Input area — telefone (fluxo telefone)
      + '<div id="leadCapturePhoneInput" style="background:#F0F0F0;padding:10px 12px;display:none;flex-direction:column;gap:6px">'
      + '  <div style="display:flex;gap:8px;align-items:center">'
      + '    <input id="leadPhoneInput" type="tel" placeholder="Ex: ' + PHONE_PLACEHOLDER + '" maxlength="20" '
      + '      style="flex:1;padding:10px 16px;border-radius:24px;border:none;font-size:15px;font-family:Poppins,sans-serif;outline:none;background:#fff" '
      + '      autocomplete="tel">'
      + '    <button id="leadPhoneSend" style="width:44px;height:44px;border-radius:50%;background:#075E54;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0">'
      + '      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="#fff"/></svg>'
      + '    </button>'
      + '  </div>'
      + '  <a id="leadPhoneSkip" style="display:none;text-align:center;font-size:12px;color:#075E54;text-decoration:underline;cursor:pointer;padding:2px 0;font-family:Poppins,sans-serif">Pular e ligar direto</a>'
      + '  <p style="text-align:center;font-size:10px;color:#999;margin:0;padding:2px 0;font-family:Poppins,sans-serif">Ao prosseguir, você concorda com nossa <a href="/politica-de-privacidade" target="_blank" style="color:#075E54;text-decoration:underline">Política de Privacidade</a></p>'
      + '</div>'
      // Skip link persistente (aparece desde o 1o step na 2a+ abertura)
      + '<div id="leadCaptureSkip" style="background:#F0F0F0;padding:6px 12px;display:none;text-align:center">'
      + '  <a id="leadSkipLink" style="font-size:12px;color:#075E54;text-decoration:underline;cursor:pointer;padding:2px 0;font-family:Poppins,sans-serif">Pular e falar direto</a>'
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
        wrapper.querySelectorAll('button').forEach(function (b) {
          b.disabled = true;
          b.style.opacity = '0.5';
          b.style.cursor = 'default';
        });
        this.style.background = '#075E54';
        this.style.color = '#fff';
        this.style.opacity = '1';

        onSelect(opt.value);
      });
      wrapper.appendChild(btn);
    });

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

    // Helper para "lockar" o grid após qualquer escolha
    function lockGrid(selectedBtn) {
      grid.querySelectorAll('button').forEach(function (b) {
        b.disabled = true;
        b.style.opacity = '0.5';
        b.style.cursor = 'default';
      });
      if (selectedBtn) {
        selectedBtn.style.background = '#075E54';
        selectedBtn.style.color = '#fff';
        selectedBtn.style.opacity = '1';
      }
    }

    // Cria botão estilizado padrão
    function makeBtn(label) {
      var btn = document.createElement('button');
      btn.textContent = label;
      btn.style.cssText = 'padding:10px 6px;border-radius:10px;border:2px solid #075E54;background:#fff;color:#075E54;font-size:13px;font-weight:600;cursor:pointer;font-family:Poppins,sans-serif;transition:all 0.2s;line-height:1.2';
      btn.addEventListener('mouseenter', function () {
        if (this.disabled) return;
        this.style.background = '#075E54';
        this.style.color = '#fff';
      });
      btn.addEventListener('mouseleave', function () {
        if (this.disabled) return;
        this.style.background = '#fff';
        this.style.color = '#075E54';
      });
      return btn;
    }

    CIDADES.forEach(function (cidade) {
      var btn = makeBtn(cidade);
      btn.addEventListener('click', function () {
        lockGrid(this);
        onSelect(cidade);
      });
      grid.appendChild(btn);
    });

    // Botão "Outro" — abre input livre
    var outroBtn = makeBtn('Outro');
    outroBtn.addEventListener('click', function () {
      lockGrid(this);
      showCityFreeInput(onSelect);
    });
    grid.appendChild(outroBtn);

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

  // ===== INPUT LIVRE DE CIDADE (após clicar em "Outro") =====
  function showCityFreeInput(onSelect) {
    var chat = document.getElementById('leadCaptureChat');
    if (!chat) return;

    var wrapper = document.createElement('div');
    wrapper.style.cssText = 'display:flex;gap:8px;align-items:center;padding:4px 0;width:100%';

    var input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Digite sua cidade';
    input.maxLength = 60;
    input.style.cssText = 'flex:1;padding:10px 16px;border-radius:24px;border:2px solid #075E54;font-size:14px;font-family:Poppins,sans-serif;outline:none;background:#fff';

    var sendBtn = document.createElement('button');
    sendBtn.style.cssText = 'width:40px;height:40px;border-radius:50%;background:#075E54;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0';
    sendBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="#fff"/></svg>';

    function submit() {
      var val = (input.value || '').trim();
      if (val.length < 2) {
        input.style.borderColor = '#d9534f';
        input.focus();
        return;
      }
      input.disabled = true;
      sendBtn.disabled = true;
      sendBtn.style.opacity = '0.5';
      onSelect(val);
    }

    sendBtn.addEventListener('click', submit);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); submit(); }
    });

    wrapper.appendChild(input);
    wrapper.appendChild(sendBtn);
    chat.appendChild(wrapper);
    chat.scrollTop = chat.scrollHeight;

    setTimeout(function () { try { input.focus(); } catch (e) { } }, 100);
  }

  // ===========================================================
  // FLUXO DA CONVERSA
  // ===========================================================

  // STEP 1: Saudação + tipo de atendimento (botões)
  function stepSaudacao() {
    var saudacao = currentChannel === 'telefone'
      ? 'Olá, aqui é da R.I.P. Pet ' + UNIDADE + '. Já vamos te conectar com nossa linha direta. Só precisamos de algumas informações rápidas.'
      : 'Olá, aqui é da R.I.P. Pet ' + UNIDADE + '. Estamos aqui para oferecer todo suporte que precisar.';

    addBubble(saudacao, true, function () {
      addBubble('Como podemos te ajudar?', true, function () {
        lastStepTime = Date.now();
        showOptionButtons([
          { label: 'Emergência / Falecimento', value: 'emergencial' },
          { label: 'Planos Preventivos', value: 'preventivo' }
        ], function (tipo) {
          leadTipo = tipo;
          stepsCompleted++;
          lastStepName = 'tipo';
          logFunnelEvent('step_tipo', tipo);
          addBubble(tipo === 'emergencial' ? 'Emergência / Falecimento' : 'Planos Preventivos', false);

          if (currentChannel === 'telefone' && tipo === 'emergencial') {
            setTimeout(stepSentimentosTelefone, 500);
          } else if (currentChannel === 'telefone') {
            setTimeout(stepTelefone, 500);
          } else if (tipo === 'emergencial') {
            setTimeout(stepSentimentosEmergencial, 500);
          } else {
            if (ASK_CIDADE) {
              setTimeout(stepCidadePreventivo, 500);
            } else {
              setTimeout(stepNome, 500);
            }
          }
        });
      });
    });
  }

  // STEP: Sentimentos (emergencial WhatsApp) → cidade ou espécie
  function stepSentimentosEmergencial() {
    addBubble('Nossos sentimentos pelo momento \uD83D\uDE4F\uD83C\uDFFB\uD83E\uDE75', true, function () {
      if (ASK_CIDADE) {
        setTimeout(stepCidadeEmergencial, 500);
      } else {
        setTimeout(stepEspecie, 500);
      }
    });
  }

  // STEP 2a: Cidade (emergencial)
  function stepCidadeEmergencial() {
    addBubble('Em qual cidade precisa do atendimento?', true, function () {
      lastStepTime = Date.now();
      showCityGrid(function (cidade) {
        leadCidade = cidade;
        stepsCompleted++;
        lastStepName = 'cidade';
        logFunnelEvent('step_cidade', cidade);
        addBubble(cidade, false);
        setTimeout(stepEspecie, 500);
      });
    });
  }

  // STEP 2b: Cidade (preventivo) → nome ou telefone
  function stepCidadePreventivo() {
    addBubble('Qual sua cidade?', true, function () {
      lastStepTime = Date.now();
      showCityGrid(function (cidade) {
        leadCidade = cidade;
        stepsCompleted++;
        lastStepName = 'cidade';
        logFunnelEvent('step_cidade', cidade);
        addBubble(cidade, false);
        setTimeout(currentChannel === 'telefone' ? stepTelefone : stepNome, 500);
      });
    });
  }

  // STEP 3: Espécie do pet (só emergencial WhatsApp)
  function stepEspecie() {
    addBubble('O petzinho é um:', true, function () {
      lastStepTime = Date.now();
      showOptionButtons([
        { label: 'Cachorro', value: 'cachorro' },
        { label: 'Gato', value: 'gato' },
        { label: 'Exótico', value: 'exotico' }
      ], function (especie) {
        leadEspecie = especie;
        stepsCompleted++;
        lastStepName = 'especie';
        logFunnelEvent('step_especie', especie);
        var label = especie === 'cachorro' ? 'Cachorro' : especie === 'gato' ? 'Gato' : 'Exótico';
        addBubble(label, false);

        if (especie === 'cachorro' && ASK_GRANDE_PORTE) {
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
      lastStepTime = Date.now();
      showOptionButtons([
        { label: 'Sim', value: 'sim' },
        { label: 'Não', value: 'nao' }
      ], function (resposta) {
        leadGrandePorte = resposta === 'sim';
        stepsCompleted++;
        lastStepName = 'grande_porte';
        logFunnelEvent('step_grande_porte', resposta);
        addBubble(resposta === 'sim' ? 'Sim' : 'Não', false);
        setTimeout(stepNome, 500);
      });
    });
  }

  // STEP: Sentimentos + telefone (emergencial telefone — sem cidade)
  function stepSentimentosTelefone() {
    addBubble('Nossos sentimentos pelo momento \uD83D\uDE4F\uD83C\uDFFB\uD83E\uDE75', true, function () {
      addBubble('Vamos te conectar com nossa equipe o mais rápido possível.', true, function () {
        setTimeout(stepTelefone, 500);
      });
    });
  }

  // STEP 5: Nome (campo de texto — por último)
  function stepNome() {
    var nameInput = document.getElementById('leadNameInput');
    if (nameInput) nameInput.value = '';

    addBubble('Para iniciarmos seu atendimento, qual seu nome?', true, function () {
      lastStepTime = Date.now();
      // Esconder skip persistente (o input de nome tem seu próprio "Fale diretamente")
      var skipArea = document.getElementById('leadCaptureSkip');
      if (skipArea) skipArea.style.display = 'none';
      var inputArea = document.getElementById('leadCaptureInput');
      if (inputArea) inputArea.style.display = 'flex';
      if (nameInput) nameInput.focus();
    });
  }

  // STEP 5b: Telefone (fluxo telefone — em vez de nome)
  function stepTelefone() {
    var phoneInput = document.getElementById('leadPhoneInput');
    if (phoneInput) phoneInput.value = '';

    addBubble('Uma última informação: Se por algum motivo não conseguir completar a ligação, deixe seu telefone e ligaremos o mais breve possível.', true, function () {
      lastStepTime = Date.now();
      // Esconder skip persistente (o input de telefone tem seu próprio "Pular e ligar direto")
      var skipArea = document.getElementById('leadCaptureSkip');
      if (skipArea) skipArea.style.display = 'none';
      var phoneArea = document.getElementById('leadCapturePhoneInput');
      if (phoneArea) phoneArea.style.display = 'flex';
      if (phoneInput) phoneInput.focus();
    });
  }

  // STEP FINAL: Salvar + countdown + protocolo + redirect
  function stepFinalizar() {
    popupCompleted = true;

    // Log funnel event
    logFunnelEvent('popup_completed', currentChannel);

    // Track lead completo (GA4 + Meta Pixel)
    try {
      if (window.gtag) {
        // Evento específico por unidade (Golden Conversion p/ Google Ads)
        var unitSlug = {
          'ST': 'santos',
          'SP': 'saopaulo',
          'CA': 'campinas',
          'RE': 'resende',
          'PA': 'pouso_alegre',
          'PI': 'pindamonhangaba',
          'SJ': 'sjc'
        }[UNIDADE_CODE] || UNIDADE_CODE.toLowerCase();

        window.gtag('event', 'popup_lead_completed_' + unitSlug, {
          event_category: 'lead_capture',
          canal: currentChannel,
          tipo: leadTipo,
          cidade: leadCidade,
          unidade: UNIDADE,
          unidade_code: UNIDADE_CODE
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
        ? 'Vamos te conectar direto com nossa equipe.'
        : '\u00D3timo! Conectando sua ligação.';
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
    popupOpenTime = Date.now();
    lastStepTime = Date.now();
    stepsCompleted = 0;
    lastStepName = '';
    popupCompleted = false;
    funnelEvents = [];

    // Reset estado
    leadNome = '';
    leadTipo = '';
    leadCidade = '';
    leadEspecie = '';
    leadGrandePorte = null;
    leadTelefone = '';

    // Atualizar session com dados de CTA
    saveSession({
      channel: channel,
      section: detectSection(element)
    });

    // Log funnel event
    logFunnelEvent('popup_opened', channel, {
      popup_number: popupOpenCount,
      cta_section: detectSection(element)
    });

    // Criar popup se não existe
    if (!document.getElementById('leadCaptureOverlay')) {
      createPopupHTML();
      setupPopupEvents();
    }

    // Limpar chat anterior
    var chat = document.getElementById('leadCaptureChat');
    if (chat) chat.innerHTML = '';

    // Esconder inputs até a hora certa
    var inputArea = document.getElementById('leadCaptureInput');
    if (inputArea) inputArea.style.display = 'none';
    var phoneArea = document.getElementById('leadCapturePhoneInput');
    if (phoneArea) phoneArea.style.display = 'none';

    // "Fale diretamente" / "Pular e ligar direto" — só a partir da 2a abertura
    var directLink = document.getElementById('leadDirectLink');
    if (directLink) {
      directLink.style.display = popupOpenCount >= 2 ? 'block' : 'none';
    }
    var phoneSkip = document.getElementById('leadPhoneSkip');
    if (phoneSkip) {
      phoneSkip.style.display = popupOpenCount >= 2 ? 'block' : 'none';
    }
    // Skip link persistente — visível desde o 1o step na 2a+ abertura
    var skipArea = document.getElementById('leadCaptureSkip');
    if (skipArea) {
      skipArea.style.display = popupOpenCount >= 2 ? 'block' : 'none';
      var skipLinkEl = document.getElementById('leadSkipLink');
      if (skipLinkEl) {
        skipLinkEl.textContent = channel === 'telefone' ? 'Pular e ligar direto' : 'Pular e falar direto no WhatsApp';
      }
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
    // Determinar step de abandono baseado no próximo step esperado
    var abandonStep;
    if (!leadTipo) {
      abandonStep = 'tipo';
    } else if (currentChannel === 'telefone') {
      // Telefone: tipo → (sentimentos se emergencial) → telefone
      abandonStep = !leadTelefone ? 'telefone' : 'finalizar';
    } else if (ASK_CIDADE && !leadCidade) {
      abandonStep = 'cidade';
    } else if (leadTipo === 'emergencial' && !leadEspecie) {
      abandonStep = 'especie';
    } else if (leadTipo === 'emergencial' && leadEspecie === 'cachorro' && ASK_GRANDE_PORTE && leadGrandePorte === null) {
      abandonStep = 'grande_porte';
    } else if (!leadNome) {
      abandonStep = 'nome';
    } else {
      abandonStep = 'finalizar';
    }

    // Salvar abandono no Supabase (se não completou)
    if (!popupCompleted && currentChannel) {
      logFunnelEvent('popup_abandoned', abandonStep, {
        method: 'close_button',
        steps_completed: stepsCompleted
      });
      savePartialLead(abandonStep);
    }

    // Track abandono (GA4)
    try {
      if (window.gtag) {
        window.gtag('event', 'popup_lead_abandoned', {
          event_category: 'lead_capture',
          canal: currentChannel,
          step_abandonado: abandonStep
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
    stepsCompleted++;
    lastStepName = 'nome';
    logFunnelEvent('step_nome', nome);

    // Esconder input
    var inputArea = document.getElementById('leadCaptureInput');
    if (inputArea) inputArea.style.display = 'none';

    // Mostrar resposta do user
    addBubble(nome, false);

    // Próximo passo — nome é o último step antes de finalizar
    setTimeout(stepFinalizar, 500);
  }

  // ===== HANDLER: TELEFONE ENVIADO =====
  function onPhoneSubmit() {
    var input = document.getElementById('leadPhoneInput');
    if (!input) return;

    var tel = input.value.trim().replace(/\D/g, '');
    if (tel.length < 10) {
      input.focus();
      input.style.boxShadow = '0 0 0 2px #e74c3c';
      setTimeout(function () { input.style.boxShadow = 'none'; }, 1500);
      return;
    }

    leadTelefone = input.value.trim();
    stepsCompleted++;
    lastStepName = 'telefone';
    logFunnelEvent('step_telefone', leadTelefone);

    // Esconder input
    var phoneArea = document.getElementById('leadCapturePhoneInput');
    if (phoneArea) phoneArea.style.display = 'none';

    // Mostrar resposta do user
    addBubble(leadTelefone, false);

    // Finalizar
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

    // Telefone input events
    var phoneSendBtn = document.getElementById('leadPhoneSend');
    if (phoneSendBtn) phoneSendBtn.addEventListener('click', onPhoneSubmit);

    var phoneInput = document.getElementById('leadPhoneInput');
    if (phoneInput) {
      phoneInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          onPhoneSubmit();
        }
      });
    }

    // "Pular e ligar direto" — vai pro redirect sem salvar telefone
    var phoneSkip = document.getElementById('leadPhoneSkip');
    if (phoneSkip) {
      phoneSkip.addEventListener('click', function () {
        logFunnelEvent('phone_skip_clicked', currentChannel);
        var phoneArea = document.getElementById('leadCapturePhoneInput');
        if (phoneArea) phoneArea.style.display = 'none';
        stepsCompleted++;
        lastStepName = 'telefone_skip';
        setTimeout(stepFinalizar, 300);
      });
    }

    // Skip link persistente (visível desde o início na 2a+ abertura)
    var skipLink = document.getElementById('leadSkipLink');
    if (skipLink) {
      skipLink.addEventListener('click', function () {
        logFunnelEvent('skip_link_clicked', currentChannel, { from: 'persistent' });

        // Preencher placeholders
        leadNome = leadNome || '-';
        leadCidade = leadCidade || '-';

        popupCompleted = true;

        if (currentChannel === 'telefone') {
          // Telefone: redireciona direto
          closePopup();
          doRedirect(null);
        } else {
          // WhatsApp: salva lead parcial e redireciona com protocolo
          var savePromise = saveLead();
          savePromise.then(function (protocolo) {
            closePopup();
            doRedirect(protocolo);
          });
        }
      });
    }

    // "Fale diretamente" — salva lead parcial com tracking + protocolo, redireciona
    var directLink = document.getElementById('leadDirectLink');
    if (directLink) {
      directLink.addEventListener('click', function () {
        logFunnelEvent('direct_link_clicked', currentChannel);

        // Preencher com placeholders o que não foi respondido
        leadNome = leadNome || '-';
        leadCidade = leadCidade || '-';

        popupCompleted = true; // evitar duplo save de abandono

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
    initIds();
    captureUrlParams();
    detectGeo();

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        interceptClicks();
        trackSections();
      });
    } else {
      interceptClicks();
      trackSections();
    }

    var observer = new MutationObserver(interceptClicks);
    observer.observe(document.body || document.documentElement, { childList: true, subtree: true });

    // Iniciar session tracking
    startSessionTracking();
  }

  init();
})();
