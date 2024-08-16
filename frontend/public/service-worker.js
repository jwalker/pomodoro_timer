self.addEventListener('install', event => {
    console.log('Service Worker installing.');
    event.waitUntil(
      caches.open('pomodoro-v1').then(cache => {
        return cache.addAll([
          '/',
          '/index.html',
          '/manifest.json',
          '/favicon.ico',
          '/logo192.png',
          '/logo512.png',
          '/metal_gong.mp3',
          '/css/app.css',
          '/js/app.js'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', event => {
    console.log('Fetching:', event.request.url);
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request);
      })
    );
  });
  