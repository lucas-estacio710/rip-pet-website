/**
 * RIP PET - Google Ads Click Tracker (v2 — RIP Shield)
 * Rastreia cliques do Google Ads com fingerprint e persiste no Supabase.
 * Trabalha em conjunto com lead-capture.js (compartilham visitor_id e session_id).
 */

(function() {
  'use strict';

  // ===== UTILS =====

  function generateUUID() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  function getOrCreateId(storage, key) {
    try {
      var id = storage.getItem(key);
      if (!id) {
        id = generateUUID();
        storage.setItem(key, id);
      }
      return id;
    } catch (e) {
      return generateUUID();
    }
  }

  // ===== FINGERPRINT =====

  function generateFingerprint() {
    var components = [
      navigator.userAgent,
      screen.width + 'x' + screen.height,
      screen.colorDepth,
      navigator.language,
      navigator.hardwareConcurrency || '',
      navigator.platform || ''
    ];

    // Timezone
    try {
      components.push(Intl.DateTimeFormat().resolvedOptions().timeZone);
    } catch (e) {}

    // Canvas fingerprint
    try {
      var canvas = document.createElement('canvas');
      canvas.width = 200;
      canvas.height = 50;
      var ctx = canvas.getContext('2d');
      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillStyle = '#a7e189';
      ctx.fillRect(0, 0, 200, 50);
      ctx.fillStyle = '#02243c';
      ctx.fillText('RIPShield2026', 2, 2);
      components.push(canvas.toDataURL().slice(-50));
    } catch (e) {}

    // Hash simples (djb2)
    var str = components.join('|');
    var hash = 5381;
    for (var i = 0; i < str.length; i++) {
      hash = ((hash << 5) + hash) + str.charCodeAt(i);
    }
    return 'fp_' + (hash >>> 0).toString(36);
  }

  // ===== URL PARAMS =====

  function getUrlParams() {
    var params = new URLSearchParams(window.location.search);
    return {
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_content: params.get('utm_content') || '',
      utm_term: params.get('utm_term') || '',
      gclid: params.get('gclid') || ''
    };
  }

  function isGoogleAds(params) {
    return !!(
      params.gclid ||
      (params.utm_source && params.utm_source.toLowerCase() === 'google') ||
      (params.utm_medium && (params.utm_medium.toLowerCase() === 'cpc' || params.utm_medium.toLowerCase() === 'ppc'))
    );
  }

  // ===== TRACKING =====

  function trackClick(params, fingerprint, visitorId, sessionId, unidadeCode) {
    try {
      fetch('/api/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          page: window.location.pathname,
          fingerprint: fingerprint,
          visitor_id: visitorId,
          session_id: sessionId,
          unidade_code: unidadeCode,
          utm_source: params.utm_source,
          utm_medium: params.utm_medium,
          utm_campaign: params.utm_campaign,
          utm_content: params.utm_content,
          utm_term: params.utm_term,
          gclid: params.gclid
        })
      });
    } catch (e) {}
  }

  // ===== INIT =====

  function init() {
    var params = getUrlParams();
    var isAds = isGoogleAds(params);
    var wasAds = false;

    try { wasAds = sessionStorage.getItem('ads_visitor') === 'true'; } catch (e) {}

    if (!isAds && !wasAds) return;

    // IDs compartilhados com lead-capture.js
    var visitorId = getOrCreateId(localStorage, 'rp_visitor_id');
    var sessionId = getOrCreateId(sessionStorage, 'rp_session_id');

    // Unidade da config (definida antes deste script no HTML)
    var cfg = window.LEAD_CAPTURE_CONFIG || {};
    var unidadeCode = cfg.unidadeCode || 'ST';

    // Fingerprint
    var fingerprint = generateFingerprint();

    // Marcar como visitante de Ads
    if (isAds) {
      try {
        sessionStorage.setItem('ads_visitor', 'true');
        sessionStorage.setItem('ads_params', JSON.stringify(params));
      } catch (e) {}
    } else {
      // Recuperar params da sessão anterior
      try {
        params = JSON.parse(sessionStorage.getItem('ads_params') || '{}');
      } catch (e) { params = {}; }
    }

    trackClick(params, fingerprint, visitorId, sessionId, unidadeCode);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
