document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.nav');
  const menu = nav ? nav.querySelector('.menu') : null;

  if (nav && menu) {
    const oldNote = nav.querySelector('.mobile-note');
    if (oldNote) oldNote.remove();

    const toggle = document.createElement('button');
    toggle.className = 'mobile-menu-toggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'メニューを開く');
    toggle.textContent = 'MENU';
    nav.appendChild(toggle);

    const setMenuOpen = (open) => {
      menu.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      toggle.textContent = open ? 'CLOSE' : 'MENU';
    };

    toggle.addEventListener('click', () => {
      setMenuOpen(!menu.classList.contains('is-open'));
    });

    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenuOpen(false));
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setMenuOpen(false);
    });

    document.addEventListener('click', (event) => {
      if (menu.classList.contains('is-open') && !nav.contains(event.target)) {
        setMenuOpen(false);
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 620) setMenuOpen(false);
    });
  }

  const form = document.querySelector('form[data-formspark]');
  if (!form) return;

  const status = form.querySelector('.form-status');
  const button = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const originalLabel = button.textContent;
    button.disabled = true;
    button.textContent = 'SENDING...';
    status.textContent = '';
    status.className = 'form-status';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      });

      if (!response.ok) throw new Error('Submission failed');

      form.reset();
      status.textContent = 'お問い合わせを送信しました。ありがとうございます。';
      status.classList.add('success');
    } catch (error) {
      status.textContent = '送信できませんでした。時間をおいて再度お試しください。';
      status.classList.add('error');
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
    }
  });
});
