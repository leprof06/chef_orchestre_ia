// 📁 src/components/AudioCECRL.jsx — Composant audio multilingue pour test CECRL

import { useEffect, useRef } from "react";

const voixParLangue = {
  allemand: "de-DE",
  anglais: "en-GB",
  espagnol: "es-ES",
  japonais: "ja-JP",
  russe: "ru-RU",
  chinois: "zh-CN",
  coreen: "ko-KR"
};

export default function AudioCECRL({ text, lang }) {
  const utteranceRef = useRef(null);

  const playAudio = () => {
    if (utteranceRef.current) {
      window.speechSynthesis.cancel();
    }
    const voixLocale = voixParLangue[lang] || "fr-FR";
    const utterance = new SpeechSynthesisUtterance(text);
    const voixTrouvee = window.speechSynthesis.getVoices().find(v => v.lang === voixLocale);
    if (voixTrouvee) utterance.voice = voixTrouvee;
    utterance.lang = voixLocale;
    utterance.rate = 0.9;
    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    // Précharger les voix au montage si nécessaire
    window.speechSynthesis.getVoices();
  }, []);

  return (
    <button onClick={playAudio} className="mt-2 px-3 py-1 bg-blue-100 rounded text-sm text-blue-700">
      🔊 Écouter l'audio
    </button>
  );
}
