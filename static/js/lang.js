let currentLang = localStorage.getItem('lang') || 'en';
const langFiles = {
  en: '/static/lang/lang_en.json',
  fr: '/static/lang/lang_fr.json',
  de: '/static/lang/lang_de.json',
  zh: '/static/lang/lang_zh.json'
};
let translations = {};

function loadLang(lang, callback) {
  fetch(langFiles[lang])
    .then(res => res.json())
    .then(data => {
      translations = data;
      currentLang = lang;
      localStorage.setItem('lang', lang);
      applyTranslations();
      if (callback) callback();
    });
}

// --- Custom Dropdown for language switch ---
document.addEventListener('DOMContentLoaded', () => {
  const langBtn = document.getElementById('lang-btn');
  const langList = document.getElementById('lang-list');
  const langCurrent = document.getElementById('lang-current');

  if (langBtn && langList) {
    langBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      langBtn.parentNode.classList.toggle('open');
    });
    langList.querySelectorAll('li').forEach(item => {
      item.addEventListener('click', () => {
        loadLang(item.getAttribute('data-lang'));
        langBtn.parentNode.classList.remove('open');
      });
    });
    // Actualise le label (icône + abréviation)
    function updateLangDisplay() {
      const cur = localStorage.getItem('lang') || 'en';
      let flag = '🌐', name = 'EN';
      if (cur === 'fr') { flag = '🇫🇷'; name = 'FR'; }
      if (cur === 'de') { flag = '🇩🇪'; name = 'DE'; }
      if (cur === 'zh') { flag = '🇨🇳'; name = '中文'; }
      langCurrent.textContent = `${flag} ${name}`;
    }
    updateLangDisplay();
    document.addEventListener('click', () => langBtn.parentNode.classList.remove('open'));
    window.loadLang = (lang) => {
      fetch(langFiles[lang])
        .then(res => res.json())
        .then(data => {
          translations = data;
          currentLang = lang;
          localStorage.setItem('lang', lang);
          applyTranslations();
          updateLangDisplay();
        });
    };
  }
});

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translations[key]) el.innerText = translations[key];
  });
  // Optionnel: placeholder
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (translations[key]) el.placeholder = translations[key];
  });
}

// Changement de langue
document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('select-lang');
  if (select) {
    select.value = currentLang;
    select.addEventListener('change', (e) => {
      loadLang(e.target.value);
    });
  }
  loadLang(currentLang);
});
