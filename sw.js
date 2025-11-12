// Service Worker para RIP PET
// Versão 1.0 - Cache de recursos estáticos e terceiros

const CACHE_NAME = 'rippet-v2';
const THIRD_PARTY_CACHE = 'rippet-third-party-v2';

// Recursos para cachear na instalação
const STATIC_CACHE = [
  '/',
  '/index.html',
  '/assets/rippet_logo_horizontal_fundo_claro_opt.webp',
  '/images/gato_dormindo_opt.webp',
  '/fonts/Autography.woff2'
];

// Instala o service worker e cacheia recursos estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_CACHE))
      .then(() => self.skipWaiting())
  );
});

// Ativa o service worker e limpa caches antigos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== THIRD_PARTY_CACHE)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Intercepta requisições
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Facebook Pixel e Analytics - Cache com stale-while-revalidate
  if (url.hostname === 'connect.facebook.net' ||
      url.hostname === 'www.facebook.com' ||
      url.hostname === 'www.googletagmanager.com' ||
      url.hostname === 'www.google-analytics.com') {

    event.respondWith(
      caches.open(THIRD_PARTY_CACHE).then((cache) => {
        return cache.match(request).then((cachedResponse) => {
          const fetchPromise = fetch(request).then((networkResponse) => {
            // Só cacheia respostas OK
            if (networkResponse.ok) {
              cache.put(request, networkResponse.clone());
            }
            return networkResponse;
          }).catch(() => cachedResponse); // Fallback para cache em caso de erro

          // Retorna cache imediatamente, atualiza em background
          return cachedResponse || fetchPromise;
        });
      })
    );
    return;
  }

  // Fontes do Google - Cache-first
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) return cachedResponse;

        return fetch(request).then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }

  // Imagens - Cache-first com fallback
  if (request.destination === 'image') {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) return cachedResponse;

        return fetch(request).then((response) => {
          if (response.ok) {
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, response.clone());
              return response;
            });
          }
          return response;
        });
      })
    );
    return;
  }

  // Outros recursos - Network-first
  event.respondWith(
    fetch(request).catch(() => caches.match(request))
  );
});
