/* DR-USA · portada "luz del tablero" y cotización por WhatsApp
   Convenciones Index01: seguidor exponencial 1-e^(-dt·RATE) con RATE=6, sin listeners de scroll para animar. */
(function () {
  'use strict';
  var RATE = 6;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Portada: líneas de luz reflejadas sobre la chapa ---------- */
  function drawPanel(ctx, w, h, amt, cx, cy) {
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#1B2026');
    g.addColorStop(0.55, '#121519');
    g.addColorStop(1, '#0B0D10');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
    var R = Math.min(w, h) * 0.17;
    var n = Math.max(10, Math.round(h / 36));
    for (var i = 0; i < n; i++) {
      var t = (i + 0.5) / n;
      var base = h * 0.04 + t * h * 0.78;
      ctx.beginPath();
      for (var x = 0; x <= w; x += 4) {
        var y0 = base - Math.sin(x / w * Math.PI) * h * 0.035;
        var dx = x - cx, dy = y0 - cy;
        var f = Math.exp(-(dx * dx + dy * dy) / (R * R));
        var y = y0 + dy * amt * 1.6 * f + amt * R * 0.28 * f;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      var a = 0.22 + 0.6 * Math.sin(t * Math.PI);
      ctx.strokeStyle = 'rgba(243,246,248,' + a.toFixed(3) + ')';
      ctx.lineWidth = 2 + 3.4 * Math.sin(t * Math.PI);
      ctx.shadowColor = 'rgba(124,196,236,.45)';
      ctx.shadowBlur = 8;
      ctx.stroke();
    }
    ctx.shadowBlur = 0;
  }

  function fit(canvas) {
    var r = canvas.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(r.width * dpr));
    var h = Math.max(1, Math.round(r.height * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    return { w: w, h: h };
  }

  var hero = document.getElementById('hero-canvas');
  if (hero && hero.getContext) {
    var ctx = hero.getContext('2d');
    var amt = 0, target = 1, hold = 0, last = 0, visible = true, raf = 0;
    var center = function (s) { return { x: s.w * 0.7, y: s.h * 0.34 }; };

    var still = function () {
      var s = fit(hero), c = center(s);
      drawPanel(ctx, s.w, s.h, 0, c.x, c.y);
    };

    var frame = function (now) {
      if (!last) last = now;
      var dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      hold += dt;
      if (target === 1 && hold > 1.6) { target = 0; hold = 0; }
      else if (target === 0 && hold > 3.4) { target = 1; hold = 0; }
      amt += (target - amt) * (1 - Math.exp(-dt * RATE));
      var s = fit(hero), c = center(s);
      drawPanel(ctx, s.w, s.h, amt, c.x, c.y);
      raf = visible ? requestAnimationFrame(frame) : 0;
    };

    if (reduce) {
      still();
      if ('ResizeObserver' in window) new ResizeObserver(still).observe(hero);
    } else {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          visible = entries[0].isIntersecting;
          if (visible && !raf) { last = 0; raf = requestAnimationFrame(frame); }
        }).observe(hero);
      }
      raf = requestAnimationFrame(frame);
    }
  }

  /* ---------- Cotización: arma el mensaje y abre WhatsApp ---------- */
  var form = document.getElementById('quote-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var number = (document.body.getAttribute('data-whatsapp') || '').replace(/\D/g, '');
  var es = document.documentElement.lang === 'es';

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var val = function (k) { return (d.get(k) || '').toString().trim(); };
    if (!val('name') || !val('area')) {
      status.textContent = es ? 'Escribe tu nombre y tu zona para continuar.' : 'Add your name and area to continue.';
      return;
    }
    var lines = es ? [
      'Hola, quiero una cotización de DR-USA.',
      'Nombre: ' + val('name'),
      'Zona o ZIP: ' + val('area'),
      'Vehículo: ' + (val('vehicle') || 'sin indicar'),
      'Soy: ' + (val('who') || 'sin indicar'),
      '¿Toca un borde o línea de carrocería?: ' + (val('edge') || 'sin indicar'),
      '¿Pintura rajada?: ' + (val('paint') || 'sin indicar'),
      '¿Panel repintado antes?: ' + (val('repaint') || 'sin indicar'),
      val('notes') ? 'Notas: ' + val('notes') : '',
      'Te mando las fotos aquí mismo.'
    ] : [
      'Hi, I would like a quote from DR-USA.',
      'Name: ' + val('name'),
      'Area or ZIP: ' + val('area'),
      'Vehicle: ' + (val('vehicle') || 'not given'),
      'I am: ' + (val('who') || 'not given'),
      'Touches an edge or body line?: ' + (val('edge') || 'not given'),
      'Cracked paint?: ' + (val('paint') || 'not given'),
      'Panel repainted before?: ' + (val('repaint') || 'not given'),
      val('notes') ? 'Notes: ' + val('notes') : '',
      'Sending the photos right here.'
    ];
    var text = lines.filter(Boolean).join('\n');

    if (!number) {
      status.textContent = es
        ? 'El número de WhatsApp todavía no está configurado.'
        : 'The WhatsApp number is not set up yet.';
      return;
    }
    window.location.href = 'https://wa.me/' + number + '?text=' + encodeURIComponent(text);
    status.textContent = es
      ? 'Abriendo WhatsApp. Adjunta las dos fotos en el chat.'
      : 'Opening WhatsApp. Attach the two photos in the chat.';
  });
})();
