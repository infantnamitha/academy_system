/* =====================================================
   EduTrack Academy — Main JavaScript
   ===================================================== */

// ---------- Mobile Sidebar Toggle ----------
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  sidebar.classList.toggle('open');
  overlay.classList.toggle('open');
}

// ---------- Auto-hide messages after 4 seconds ----------
document.addEventListener('DOMContentLoaded', function () {
  const messages = document.querySelectorAll('.message');
  messages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = 'opacity .4s, transform .4s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-8px)';
      setTimeout(function () { msg.remove(); }, 400);
    }, 4000);
  });

  // ---------- Active nav link highlight (extra safety) ----------
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(function (link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  // ---------- Animate stat numbers on dashboard ----------
  document.querySelectorAll('.stat-value').forEach(function (el) {
    const target = parseInt(el.textContent, 10);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.max(1, Math.floor(target / 30));
    const timer = setInterval(function () {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 30);
  });

  // ---------- Course bar widths animate in ----------
  document.querySelectorAll('.course-bar-fill, .att-bar-fill').forEach(function (bar) {
    const finalWidth = bar.style.width;
    bar.style.width = '0';
    setTimeout(function () { bar.style.width = finalWidth; }, 100);
  });
});

// ---------- Confirm before delete ----------
document.querySelectorAll('.btn-danger').forEach(function (btn) {
  if (btn.type !== 'submit') return; // only form submits
  btn.closest('form') && btn.closest('form').addEventListener('submit', function (e) {
    if (!confirm('Are you sure? This action cannot be undone.')) {
      e.preventDefault();
    }
  });
});
