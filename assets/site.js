document.addEventListener('DOMContentLoaded', () => {
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
      status.textContent = '送信できませんでした。時間をおいて再度お試しいただくか、下記メールアドレスからご連絡ください。';
      status.classList.add('error');
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
    }
  });
});
