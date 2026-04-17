// Vercel Serverless Function - RIP Shield (v2)
// Rastreia cliques de Google Ads e persiste IP + fingerprint no Supabase

const SUPABASE_URL = 'https://eniplfcuwvhovxybyuey.supabase.co';
const SUPABASE_KEY = 'sb_publishable_G1KKmfdmtgssnvQa_e7KQQ_p-klSYY0';

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Captura IP
  const ip = req.headers['x-forwarded-for']?.split(',')[0]?.trim()
    || req.headers['x-real-ip']
    || req.connection?.remoteAddress
    || 'unknown';

  const body = req.body || {};

  // Log (mantém compatibilidade com monitoramento via Vercel logs)
  console.log('🎯 CLICK TRACKED:', JSON.stringify({
    timestamp: new Date().toISOString(),
    ip,
    page: body.page,
    gclid: body.gclid,
    fingerprint: body.fingerprint,
    visitor_id: body.visitor_id,
    session_id: body.session_id,
    unidade_code: body.unidade_code
  }));

  // Persistir no Supabase via RPC patch_session_ip
  if (body.session_id && body.visitor_id) {
    try {
      await fetch(`${SUPABASE_URL}/rest/v1/rpc/patch_session_ip`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        },
        body: JSON.stringify({
          p_session_id: body.session_id,
          p_visitor_id: body.visitor_id,
          p_ip: ip,
          p_fingerprint: body.fingerprint || null,
          p_unidade_code: body.unidade_code || null
        })
      });
    } catch (e) {
      console.error('Supabase patch_session_ip error:', e.message);
    }
  }

  return res.status(200).json({
    success: true,
    tracked: true,
    ip: ip
  });
}
