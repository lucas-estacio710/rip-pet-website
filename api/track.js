// Vercel Serverless Function - Rastreia cliques de Google Ads
// Os logs ficam disponíveis em: Vercel Dashboard → Logs → Functions

export default function handler(req, res) {
  // Permitir CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Captura IP (Vercel fornece via headers)
  const ip = req.headers['x-forwarded-for']?.split(',')[0]?.trim()
    || req.headers['x-real-ip']
    || req.connection?.remoteAddress
    || 'unknown';

  // Dados do request
  const data = {
    timestamp: new Date().toISOString(),
    ip: ip,
    userAgent: req.headers['user-agent'] || 'unknown',
    referer: req.headers['referer'] || 'direct',
    // Dados enviados pelo frontend
    page: req.body?.page || '/',
    utmSource: req.body?.utm_source || '',
    utmMedium: req.body?.utm_medium || '',
    utmCampaign: req.body?.utm_campaign || '',
    utmContent: req.body?.utm_content || '',
    utmTerm: req.body?.utm_term || '',
    gclid: req.body?.gclid || '', // Google Click ID
  };

  // Log no console da Vercel (aparece em Functions logs)
  console.log('🎯 CLICK TRACKED:', JSON.stringify(data, null, 2));

  // Resposta
  return res.status(200).json({
    success: true,
    tracked: true,
    ip: ip // Retorna o IP para debug
  });
}
