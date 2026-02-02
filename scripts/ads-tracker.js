/**
 * RIP PET - Google Ads Click Tracker
 * Rastreia cliques vindos do Google Ads para identificar IPs maliciosos
 *
 * Os logs ficam em: Vercel Dashboard → Logs → Functions
 * Filtrar por: "CLICK TRACKED"
 */

(function() {
  'use strict';

  // Pega parâmetros da URL
  function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_content: params.get('utm_content') || '',
      utm_term: params.get('utm_term') || '',
      gclid: params.get('gclid') || '', // Google Click ID - presente em cliques do Ads
    };
  }

  // Verifica se é tráfego do Google Ads
  function isGoogleAds(params) {
    return (
      params.gclid || // Tem Google Click ID
      params.utm_source?.toLowerCase() === 'google' ||
      params.utm_medium?.toLowerCase() === 'cpc' ||
      params.utm_medium?.toLowerCase() === 'ppc'
    );
  }

  // Envia dados para a API
  async function trackClick(params) {
    try {
      const response = await fetch('/api/track', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          page: window.location.pathname,
          ...params
        }),
      });

      const data = await response.json();

      // Log local para debug (pode remover em produção)
      if (data.success) {
        console.log('📊 Ads Tracker: IP registrado -', data.ip);
      }
    } catch (error) {
      // Silencioso em produção
      console.error('Ads Tracker error:', error);
    }
  }

  // Executa
  function init() {
    const params = getUrlParams();

    // Só rastreia se for tráfego do Google Ads
    if (isGoogleAds(params)) {
      console.log('🎯 Tráfego Google Ads detectado');
      trackClick(params);

      // Salva no sessionStorage para rastrear navegação interna
      sessionStorage.setItem('ads_visitor', 'true');
      sessionStorage.setItem('ads_params', JSON.stringify(params));
    }
    // Se já foi marcado como visitante de Ads, continua rastreando
    else if (sessionStorage.getItem('ads_visitor') === 'true') {
      const savedParams = JSON.parse(sessionStorage.getItem('ads_params') || '{}');
      trackClick(savedParams);
    }
  }

  // Inicia quando DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
