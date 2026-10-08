// Presence — background "field": you (black dot) among a small neighbourhood of people (grey dots).
// Scrolling re-aims one connection from person to person.
// Desktop: you sit on the column seam; the field stays behind everything at low opacity.
// Tablet/phone: the cluster is the hero illustration above the headline, then fades back behind content.
// Variants: ?v=line (default) · ?v=thread · ?v=ripple
(function () {
  var svg = document.getElementById('field');
  if (!svg) return;
  var NS = 'http://www.w3.org/2000/svg';
  var variant = (new URLSearchParams(location.search).get('v') || 'line').toLowerCase();
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    svg.appendChild(n);
    return n;
  }
  function rng(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var ease = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  var mode, me, people, targets, nodes, line, halo, waveA, waveB, heroH;
  var shown = 0, goal = 0, raf = 0, lastOn = -1;
  var arrival;
  var pulled = -1;

  function layout() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    if (arrival) arrival.cancel();
    svg.setAttribute('data-reduced-motion', String(reduce.matches));
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var W = window.innerWidth, H = window.innerHeight;
    mode = W >= 1024 ? 'desktop' : W >= 640 ? 'tablet' : 'phone';
    svg.setAttribute('data-mode', mode);
    var left = document.querySelector('.left');
    var cfg;

    if (mode === 'desktop') {
      me = { x: left.getBoundingClientRect().right, y: H * 0.5 };
      cfg = { count: 16, minD: 74, rx: Math.min(W * 0.27, 420), ry: Math.min(H * 0.4, 360), dot: 6, meR: 15 };
    } else {
      // Centre the cluster in the open space between the top bar and the headline.
      var top = document.querySelector('.left-top').getBoundingClientRect().bottom + window.scrollY;
      var mid = document.querySelector('.left-mid').getBoundingClientRect().top + window.scrollY;
      var space = Math.max(160, mid - top);
      me = { x: W * (mode === 'tablet' ? 0.56 : 0.5), y: top + space * 0.5 };
      heroH = left.offsetHeight;
      cfg = mode === 'tablet'
        ? { count: 13, minD: 62, rx: Math.min(W * 0.36, 300), ry: space * 0.42, dot: 5, meR: 12 }
        : { count: 10, minD: 46, rx: W * 0.4, ry: space * 0.42, dot: 4, meR: 10 };
    }

    // A loose neighbourhood: points inside an ellipse around you, evenly spaced.
    var r = rng(7);
    people = [];
    for (var i = 0; i < 2000 && people.length < cfg.count; i++) {
      var a = r() * Math.PI * 2, d = Math.sqrt(0.08 + r() * 0.92);
      var p = { x: me.x + Math.cos(a) * cfg.rx * d, y: me.y + Math.sin(a) * cfg.ry * d };
      if (p.x < 16 || p.x > W - 16 || p.y < 16 || p.y > H - 16) continue;
      if (Math.hypot(p.x - me.x, p.y - me.y) < cfg.minD * 1.2) continue;
      var ok = true;
      for (var j = 0; j < people.length; j++) if (Math.hypot(p.x - people[j].x, p.y - people[j].y) < cfg.minD) { ok = false; break; }
      if (ok) people.push(p);
    }

    // Seven targets, each in a clearly different direction from the last.
    var r2 = rng(11);
    var pool = people.map(function (p, i) { return i; }).sort(function () { return r2() - 0.5; });
    targets = [];
    var prevA = null;
    while (targets.length < Math.min(7, people.length) && pool.length) {
      var pick = 0;
      for (var k = 0; k < pool.length; k++) {
        var q = people[pool[k]], ang = Math.atan2(q.y - me.y, q.x - me.x);
        var diff = prevA === null ? Math.PI : Math.abs(Math.atan2(Math.sin(ang - prevA), Math.cos(ang - prevA)));
        if (diff > 1.0) { pick = k; break; }
      }
      var chosen = pool.splice(pick, 1)[0];
      prevA = Math.atan2(people[chosen].y - me.y, people[chosen].x - me.x);
      targets.push(chosen);
    }

    if (variant === 'ripple') {
      waveA = el('circle', { class: 'wave', cx: me.x, cy: me.y, r: 0, opacity: 0 });
      waveB = el('circle', { class: 'wave t', cx: 0, cy: 0, r: 0, opacity: 0 });
    } else {
      line = el('path', { class: 'ln', d: '' });
    }
    nodes = people.map(function (p) { return el('circle', { class: 'p', cx: p.x, cy: p.y, r: cfg.dot }); });
    halo = el('circle', { class: 'target-halo', cx: 0, cy: 0, r: cfg.dot * 2.8 });
    el('circle', { class: 'me', cx: me.x, cy: me.y, r: cfg.meR });
    lastOn = -1;
    pulled = -1;
    goal = phaseFromScroll();
    shown = goal;
    fade();
    draw();
  }

  function phaseFromScroll() {
    // A single static connection for reduced motion, independent of scroll.
    if (reduce.matches) return 0.5;
    var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    return 0.5 + clamp(window.scrollY / max, 0, 1) * (targets.length - 1);
  }

  // On tablet/phone the field is the hero image at full strength, then recedes behind the content.
  function fade() {
    if (reduce.matches) { svg.style.opacity = ''; svg.style.transform = ''; return; }
    if (mode === 'desktop') { svg.style.opacity = ''; svg.style.transform = ''; return; }
    var y = window.scrollY;
    var t = clamp(y / (heroH * 0.4), 0, 1);
    svg.style.opacity = String(1 - t * 0.86);
    // Drift up with the hero so the cluster never sits on the headline, then rest as a faint backdrop.
    svg.style.transform = 'translate3d(0,' + (-Math.min(y, heroH * 0.5) * 0.6).toFixed(1) + 'px,0)';
  }

  function draw() {
    if (!targets.length) return;
    var k = clamp(Math.floor(shown), 0, targets.length - 1);
    var u = shown - k;
    // Ease into the person, then hold through most of this scroll interval.
    // Only the illustration settles: never change the reader's scroll position.
    var ext = u < 0.22 ? 1 - Math.pow(1 - u / 0.22, 3) : u > 0.84 ? 1 - ease((u - 0.84) / 0.16) : 1;
    if (ext > 0.995) ext = 1;
    var t = people[targets[k]];
    var dx = t.x - me.x, dy = t.y - me.y, len = Math.hypot(dx, dy) || 1;
    // The person resists briefly, then returns to rest as the line releases.
    // Rebuild from original coordinates each frame: reverse/fast scrolling
    // must not leave a previous person displaced.
    if (pulled >= 0 && pulled !== targets[k]) {
      nodes[pulled].setAttribute('cx', people[pulled].x);
      nodes[pulled].setAttribute('cy', people[pulled].y);
      nodes[pulled].style.removeProperty('--target-scale');
    }
    var tension = reduce.matches ? 0 : u < 0.78 ? 0 : u <= 0.84
      ? ease((u - 0.78) / 0.06)
      : 1 - ease(clamp((u - 0.84) / 0.1, 0, 1));
    var pull = tension * (mode === 'desktop' ? 4 : 3);
    var tx = t.x + dx / len * pull, ty = t.y + dy / len * pull;
    var target = nodes[targets[k]];
    target.setAttribute('cx', tx);
    target.setAttribute('cy', ty);
    target.style.setProperty('--target-scale', String(1.25 + tension * 0.15));
    pulled = targets[k];
    var ex = me.x + (tx - me.x) * ext, ey = me.y + (ty - me.y) * ext;
    halo.setAttribute('cx', tx);
    halo.setAttribute('cy', ty);
    var haloOpacity = u < 0.22 ? ease(clamp((u - 0.06) / 0.16, 0, 1))
      : u > 0.84 ? 1 - ease((u - 0.84) / 0.16) : 1;
    halo.style.opacity = String(haloOpacity * 0.55);

    if (variant === 'thread') {
      var sag = (1 - ext) * 0.22 * len + (ext < 1 ? 6 : 0);
      var mx = (me.x + ex) / 2 - (dy / len) * sag, my = (me.y + ey) / 2 + (dx / len) * sag;
      line.setAttribute('d', ext < 0.01 ? '' : 'M' + me.x + ',' + me.y + ' Q' + mx + ',' + my + ' ' + ex + ',' + ey);
    } else if (variant === 'ripple') {
      var half = (len / 2) * ext;
      waveA.setAttribute('r', half); waveA.setAttribute('opacity', ext < 0.02 ? 0 : 0.55);
      waveB.setAttribute('cx', tx); waveB.setAttribute('cy', ty);
      waveB.setAttribute('r', half); waveB.setAttribute('opacity', ext < 0.02 ? 0 : 0.8);
    } else {
      line.setAttribute('d', ext < 0.01 ? '' : 'M' + me.x + ',' + me.y + ' L' + ex + ',' + ey);
    }

    var on = ext === 1 ? targets[k] : -1;
    if (on !== lastOn) {
      if (arrival) arrival.cancel();
      if (lastOn >= 0) { nodes[lastOn].classList.remove('on'); nodes[lastOn].classList.add('met'); }
      if (on >= 0) {
        nodes[on].classList.add('on');
        if (!reduce.matches && nodes[on].animate) {
          arrival = nodes[on].animate([
            { transform: 'scale(1)' },
            { transform: 'scale(1.6)', offset: 0.55 },
            { transform: 'scale(1.25)' }
          ], { duration: 420, easing: 'cubic-bezier(.2,.8,.3,1)' });
        }
      }
      lastOn = on;
    }
  }

  function tick() {
    raf = 0;
    if (reduce.matches) return;
    shown += (goal - shown) * 0.14;
    if (Math.abs(goal - shown) < 0.0008) shown = goal;
    draw();
    if (shown !== goal) raf = requestAnimationFrame(tick);
  }
  function onScroll() {
    if (reduce.matches) return;
    goal = phaseFromScroll(); fade(); if (!raf) raf = requestAnimationFrame(tick);
  }

  var resizeT, lastW = window.innerWidth;
  window.addEventListener('scroll', onScroll, { passive: true });
  reduce.addEventListener('change', layout);
  // Ignore height-only resizes (mobile address bar showing/hiding) so the field doesn't jump.
  window.addEventListener('resize', function () {
    if (window.innerWidth === lastW && mode !== 'desktop') return;
    lastW = window.innerWidth; clearTimeout(resizeT); resizeT = setTimeout(layout, 150);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  layout();
})();
