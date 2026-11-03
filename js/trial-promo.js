/* Пробный VPN за 10 ₽ на 3 дня: плашка сверху и карточка под заголовком. Один файл для glushilok.net и goida.win. */
(function () {
  if (window.__trialPromo) return;
  window.__trialPromo = true;
  var URL = 'https://t.me/Geodema_bot?start=p_2f9f6fab';
  var IMG = '/assets/trial-10rub-phone.webp';
  var css =
    '.tp-bar{background:#161616;color:#fff;border-bottom:3px solid #ff7500;font:600 14px/1.35 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;position:relative;z-index:50}' +
    '.tp-bar-in{max-width:1100px;margin:0 auto;padding:8px 14px;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;text-align:center}' +
    '.tp-bar b{color:#ff7500}' +
    '.tp-btn{display:inline-block;background:#ff7500;color:#fff!important;text-decoration:none!important;font-weight:800;text-transform:uppercase;letter-spacing:.04em;font-size:12px;padding:7px 14px;border:0;white-space:nowrap}' +
    '.tp-btn:hover{background:#fff;color:#ff7500!important}' +
    '.tp-card{background:#161616;color:#fff;border-left:5px solid #ff7500;margin:18px auto;max-width:760px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;padding:14px;font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;text-align:left}' +
    '.tp-card img{display:block;width:100%;max-width:330px;height:auto;flex:0 0 auto}' +
    '.tp-card .tp-txt{flex:1 1 240px;min-width:220px}' +
    '.tp-card h3{margin:0 0 6px;font-size:20px;line-height:1.2;color:#fff;border:0;background:none;text-shadow:none}' +
    '.tp-card h3 span{color:#ff7500}' +
    '.tp-card p{margin:0 0 10px;color:#ddd}' +
    '.tp-card ul{margin:0 0 12px;padding:0;list-style:none}' +
    '.tp-card li{margin:0 0 4px;color:#fff}' +
    '.tp-card li:before{content:"✓ ";color:#2fd35a;font-weight:800}' +
    '@media(max-width:560px){.tp-card img{max-width:100%}}';
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }
  function init() {
    if (!document.body) return;
    var st = el('style');
    st.textContent = css;
    document.head.appendChild(st);

    var bar = el('div', 'tp-bar', '<div class="tp-bar-in"><span>Вернули пробный тариф: <b>VPN за 10 ₽ на 3 дня</b><span class="tp-more"> · все Premium-серверы, 5 ГБ для обхода белых списков</span></span><a class="tp-btn" href="' + URL + '" data-track="trial_bar_click" rel="sponsored noopener">Попробовать за 10 ₽</a></div>');
    document.body.insertBefore(bar, document.body.firstChild);

    var h1 = document.querySelector('h1');
    if (!h1) return;
    var card = el('div', 'tp-card',
      '<a href="' + URL + '" data-track="trial_card_img_click" rel="sponsored noopener" tabindex="-1" aria-hidden="true"><img src="' + IMG + '" width="1200" height="800" loading="lazy" decoding="async" alt="Пробный VPN: 10 рублей на 3 дня, все Premium-серверы, 5 ГБ для обхода белых списков"></a>' +
      '<div class="tp-txt"><h3>VPN за <span>10 ₽</span> на 3 дня</h3>' +
      '<p>Вернули пробный тариф. Хотели попробовать, но не были уверены? Проверьте скорость, стабильность и возможности VPN.</p>' +
      '<ul><li>Полный доступ ко всем Premium-серверам</li><li>5 ГБ трафика для обхода белых списков</li><li>3 дня использования всего за 10 ₽</li></ul>' +
      '<a class="tp-btn" href="' + URL + '" data-track="trial_card_click" rel="sponsored noopener">Попробовать за 10 ₽ &gt;&gt;&gt;</a></div>');
    h1.parentNode.insertBefore(card, h1.nextSibling);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
