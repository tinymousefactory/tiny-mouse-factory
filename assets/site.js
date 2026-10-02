document.addEventListener('DOMContentLoaded', () => {
  const faviconLinks = [
    { rel: 'icon', href: '/favicon.ico', sizes: 'any' },
    { rel: 'icon', href: '/favicon-32x32.png', type: 'image/png', sizes: '32x32' },
    { rel: 'icon', href: '/favicon-16x16.png', type: 'image/png', sizes: '16x16' },
    { rel: 'apple-touch-icon', href: '/apple-touch-icon.png', sizes: '180x180' }
  ];

  faviconLinks.forEach((attrs) => {
    const link = document.createElement('link');
    Object.entries(attrs).forEach(([key, value]) => link.setAttribute(key, value));
    document.head.appendChild(link);
  });

  const mobileNavStyle = document.createElement('style');
  mobileNavStyle.textContent = `
    .mobile-menu-toggle{display:none;border:0;background:transparent;color:var(--ink);padding:10px 0;font:inherit;font-size:10px;letter-spacing:.16em;cursor:pointer}
    .mobile-note{display:none!important}
    @media(max-width:620px){
      .nav{position:relative}
      .mobile-menu-toggle{display:block}
      .menu{display:none;position:absolute;top:100%;left:0;right:0;z-index:40;flex-direction:column;gap:0;background:rgba(11,11,11,.98);border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.1);padding:8px 0 12px;box-shadow:0 18px 35px rgba(0,0,0,.38)}
      .menu.is-open{display:flex}
      .menu a{display:block;padding:12px 4px;font-size:12px;letter-spacing:.16em;border-bottom:1px solid rgba(255,255,255,.06)}
      .menu a:last-child{border-bottom:0}
    }
  `;
  document.head.appendChild(mobileNavStyle);

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
