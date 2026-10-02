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

  const addStructuredData = (data) => {
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(data);
    document.head.appendChild(script);
  };

  const path = window.location.pathname.replace(/\/+$/, '') || '/';
  const organizationId = 'https://tiny-mouse.net/#organization';
  const personId = 'https://tiny-mouse.net/about.html#yuki-nishiyama';

  if (path === '/' || path === '/index.html') {
    addStructuredData({
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'WebSite',
          '@id': 'https://tiny-mouse.net/#website',
          url: 'https://tiny-mouse.net/',
          name: 'Tiny Mouse Factory',
          inLanguage: 'ja-JP',
          publisher: { '@id': organizationId }
        },
        {
          '@type': 'Organization',
          '@id': organizationId,
          name: 'Tiny Mouse Factory',
          url: 'https://tiny-mouse.net/',
          logo: {
            '@type': 'ImageObject',
            url: 'https://tiny-mouse.net/assets/images/tmf-logo-white.jpg'
          },
          description: 'ドキュメンタリー映画、映像制作、撮影、ドローン、VR・360°、編集、音楽制作を手がける制作拠点。',
          founder: { '@id': personId }
        },
        {
          '@type': 'Person',
          '@id': personId,
          name: 'にしやまゆうき',
          alternateName: 'Yuki Nishiyama',
          url: 'https://tiny-mouse.net/about.html',
          jobTitle: 'Film Director / Filmmaker / Composer / Drone Operator'
        }
      ]
    });
  }

  if (path === '/about.html') {
    addStructuredData({
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'ProfilePage',
          '@id': 'https://tiny-mouse.net/about.html#profilepage',
          url: 'https://tiny-mouse.net/about.html',
          name: 'にしやまゆうき｜Tiny Mouse Factory',
          inLanguage: 'ja-JP',
          mainEntity: { '@id': personId }
        },
        {
          '@type': 'Person',
          '@id': personId,
          name: 'にしやまゆうき',
          alternateName: 'Yuki Nishiyama',
          url: 'https://tiny-mouse.net/about.html',
          image: 'https://tiny-mouse.net/assets/images/about-director.jpg',
          jobTitle: 'Film Director / Filmmaker / Composer / Drone Operator',
          description: 'ドキュメンタリー映画監督、映像制作者、作編曲家、ドローンオペレーター。Tiny Mouse Factory主宰。',
          worksFor: { '@id': organizationId },
          knowsAbout: [
            'Documentary Film',
            'Film Direction',
            'Cinematography',
            'Drone Cinematography',
            'VR / 360 Video',
            'Editing',
            'Music Composition',
            'Music Arrangement'
          ]
        },
        {
          '@type': 'Organization',
          '@id': organizationId,
          name: 'Tiny Mouse Factory',
          url: 'https://tiny-mouse.net/'
        }
      ]
    });
  }

  if (path === '/films/yuragi.html') {
    addStructuredData({
      '@context': 'https://schema.org',
      '@type': 'Movie',
      '@id': 'https://tiny-mouse.net/films/yuragi.html#movie',
      url: 'https://tiny-mouse.net/films/yuragi.html',
      name: '揺らぎの聲',
      alternateName: 'Forging a Prayer – Voice of the KATANA',
      description: '備前長船で約一世紀ぶりに行われた「神前打ち」から始まる奉納刀作りの一年。刀鍛冶・川島一城を追うドキュメンタリー映画。',
      image: 'https://tiny-mouse.net/assets/images/yuragi-poster.jpg',
      duration: 'PT66M',
      inLanguage: 'ja',
      director: {
        '@type': 'Person',
        '@id': personId,
        name: 'にしやまゆうき',
        alternateName: 'Yuki Nishiyama',
        url: 'https://tiny-mouse.net/about.html'
      },
      productionCompany: {
        '@type': 'Organization',
        '@id': organizationId,
        name: 'Tiny Mouse Factory',
        url: 'https://tiny-mouse.net/'
      },
      about: {
        '@type': 'Person',
        name: '川島一城',
        alternateName: 'Kazuki Kawashima',
        jobTitle: 'Japanese Swordsmith'
      }
    });
  }

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
