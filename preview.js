// Presence preview — the interest form is intentionally non-collecting.
// No network request is made, nothing is stored, and no success is reported.
(function () {
  var form = document.getElementById('interest');
  var msg = document.getElementById('form-msg');
  if (!form || !msg) return;
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    msg.hidden = false;
    msg.setAttribute('tabindex', '-1');
    msg.focus();
  });
})();
