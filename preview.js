// Presence previews — both interest forms are intentionally non-collecting.
// No network request is made, nothing is stored, and no success is reported.
(function () {
  document.querySelectorAll('[data-preview-form]').forEach(function (form) {
    var msg = form.querySelector('[role="status"]');
    var button = form.querySelector('button[type="submit"]');
    if (!msg || !button) return;
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      msg.hidden = false;
      msg.setAttribute('tabindex', '-1');
      msg.focus();
    });
    // Enable only after the non-collecting handler is installed.
    button.disabled = false;
  });
})();
