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
