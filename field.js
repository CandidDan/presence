// Presence — background "field": you (black dot) on the column seam, people nearby (grey dots)
// scattered around. Scrolling re-aims a single connection from one person to the next.
// Variants for comparison: ?v=line (default) · ?v=thread · ?v=ripple
(function () {
  var svg = document.getElementById('field');
  if (!svg) return;
  var NS = 'http://www.w3.org/2000/svg';
  var variant = (new URLSearchParams(location.search).get('v') || 'line').toLowerCase();
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n);
    return n;
  }
  function rng(seed) { // mulberry32
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var ease = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  var me, people, targets, nodes, line, ring, waveA, waveB, meNode;
  var shown = 0, goal = 0, raf = 0, lastOn = -1;

  function layout() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var W = window.innerWidth, H = window.innerHeight;
    var desktop = W >= 1024;
    var left = document.querySelector('.left');
    me = desktop
      ? { x: left.getBoundingClientRect().right, y: H * 0.5 }
      : { x: W - 14, y: Math.min(120, H * 0.16) };
    // Keep lines clear of the left column's text on desktop.
    var avoid = desktop ? Array.prototype.map.call(document.querySelectorAll('.left-mid, .left-top'), function (n) {
      var b = n.getBoundingClientRect(); return { x0: b.left - 16, y0: b.top - 16, x1: b.right + 16, y1: b.bottom + 16 };
    }) : [];
    function crosses(q) {
      for (var s = 1; s <= 24; s++) {
        var x = me.x + (q.x - me.x) * s / 24, y = me.y + (q.y - me.y) * s / 24;
        for (var a = 0; a < avoid.length; a++) if (x > avoid[a].x0 && x < avoid[a].x1 && y > avoid[a].y0 && y < avoid[a].y1) return true;
      }
      return false;
    }

    var r = rng(7), minD = desktop ? 150 : 92, margin = 22;
    people = [];
    for (var i = 0; i < 900 && people.length < (desktop ? 34 : 18); i++) {
      var p = { x: margin + r() * (W - 2 * margin), y: margin + r() * (H - 2 * margin) };
      if (Math.hypot(p.x - me.x, p.y - me.y) < 110) continue;
      var ok = true;
      for (var j = 0; j < people.length; j++) if (Math.hypot(p.x - people[j].x, p.y - people[j].y) < minD) { ok = false; break; }
      if (ok) people.push(p);
    }

    // Pick a sequence of targets: comfortable distance, each in a clearly different direction.
    var maxLen = Math.max(W, H) * (desktop ? 0.42 : 0.6);
    var pool = people.map(function (p, i) { return i; }).filter(function (i) {
      var d = Math.hypot(people[i].x - me.x, people[i].y - me.y);
      return d > (desktop ? 150 : 110) && d < maxLen && !crosses(people[i]);
    });
    var r2 = rng(11);
    pool.sort(function () { return r2() - 0.5; });
    targets = [];
    var prevA = null;
    while (targets.length < 7 && pool.length) {
      var pick = -1;
      for (var k = 0; k < pool.length; k++) {
        var q = people[pool[k]], a = Math.atan2(q.y - me.y, q.x - me.x);
        var diff = prevA === null ? Math.PI : Math.abs(Math.atan2(Math.sin(a - prevA), Math.cos(a - prevA)));
        if (diff > 1.05) { pick = k; prevA = a; break; }
      }
      if (pick < 0) pick = 0;
      targets.push(pool.splice(pick, 1)[0]);
    }

    if (variant === 'ripple') {
      waveA = el('circle', { class: 'wave', cx: me.x, cy: me.y, r: 0, opacity: 0 });
      waveB = el('circle', { class: 'wave t', cx: 0, cy: 0, r: 0, opacity: 0 });
    } else {
      line = el('path', { class: 'ln', d: '' });
    }
    svg.classList.toggle('compact', !desktop);
    nodes = people.map(function (p) { return el('circle', { class: 'p', cx: p.x, cy: p.y, r: desktop ? 6 : 4 }); });
    ring = el('circle', { class: 'ring', cx: 0, cy: 0, r: 0, opacity: 0 });
    meNode = el('circle', { class: 'me', cx: me.x, cy: me.y, r: desktop ? 16 : 7 });
    lastOn = -1;
    goal = phaseFromScroll();
    shown = reduce.matches ? snap(goal) : goal;
    draw();
  }

  // phase: k + 0.5 = holding a connection to targets[k]
  function phaseFromScroll() {
    var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    var p = clamp(window.scrollY / max, 0, 1);
    return 0.5 + p * (targets.length - 1);
  }
  function snap(ph) { return Math.floor(ph) + 0.5; }

  function draw() {
    if (!targets.length) return;
    var k = clamp(Math.floor(shown), 0, targets.length - 1);
    var u = shown - k;
    // 0–.32 reach out · .32–.68 connected · .68–1 let go
    var ext = u < 0.32 ? ease(u / 0.32) : u > 0.68 ? 1 - ease((u - 0.68) / 0.32) : 1;
    var t = people[targets[k]];
    var dx = t.x - me.x, dy = t.y - me.y, len = Math.hypot(dx, dy);
    var ex = me.x + dx * ext, ey = me.y + dy * ext;

    if (variant === 'thread') {
      // A slack thread that tightens as it reaches: sag falls to zero on connection.
      var sag = (1 - ext) * 0.22 * len + (ext < 1 ? 6 : 0);
      var mx = (me.x + ex) / 2 - (dy / len) * sag, my = (me.y + ey) / 2 + (dx / len) * sag;
      line.setAttribute('d', ext < 0.01 ? '' : 'M' + me.x + ',' + me.y + ' Q' + mx + ',' + my + ' ' + ex + ',' + ey);
    } else if (variant === 'ripple') {
      // Both people send out a signal; it counts when the two meet in the middle.
      var half = (len / 2) * ext;
      waveA.setAttribute('r', half); waveA.setAttribute('opacity', ext < 0.02 ? 0 : 0.55);
      waveB.setAttribute('cx', t.x); waveB.setAttribute('cy', t.y);
      waveB.setAttribute('r', half); waveB.setAttribute('opacity', ext < 0.02 ? 0 : 0.8);
    } else {
      line.setAttribute('d', ext < 0.01 ? '' : 'M' + me.x + ',' + me.y + ' L' + ex + ',' + ey);
    }

    var on = ext > 0.985 ? targets[k] : -1;
    if (on !== lastOn) {
      if (lastOn >= 0) { nodes[lastOn].classList.remove('on'); nodes[lastOn].classList.add('met'); }
      if (on >= 0) {
        nodes[on].classList.add('on');
        pulse(people[on]);
      }
      lastOn = on;
    }
  }

  function pulse(p) {
    if (reduce.matches || !ring.animate) return;
    ring.setAttribute('cx', p.x); ring.setAttribute('cy', p.y);
    ring.animate([{ r: 6, opacity: 0.9 }, { r: 34, opacity: 0 }], { duration: 900, easing: 'cubic-bezier(.2,.8,.3,1)' });
  }

  function tick() {
    raf = 0;
    if (reduce.matches) { shown = snap(goal); draw(); return; }
    shown += (goal - shown) * 0.14;
    if (Math.abs(goal - shown) < 0.0008) shown = goal;
    draw();
    if (shown !== goal) raf = requestAnimationFrame(tick);
  }
  function onScroll() { goal = phaseFromScroll(); if (!raf) raf = requestAnimationFrame(tick); }

  var resizeT;
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { clearTimeout(resizeT); resizeT = setTimeout(layout, 150); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout); else layout();
  layout();
})();
