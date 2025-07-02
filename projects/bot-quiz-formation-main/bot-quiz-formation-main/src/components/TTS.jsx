// 📁 src/components/TTS.jsx — Composant unifié de lecture vocale multilingue

import { useEffect, useRef } from "react";

const voixParLangue = {
  allemand: "de-DE",
  anglais: "en-GB",
  espagnol: "es-ES",
  japonais: "ja-JP",
  russe: "ru-RU",
  chinois: "zh-CN",
  coreen: "ko-KR",
  francais: "fr-FR"
};

export default function TTS({ text, lang = "francais", label = "🔊 Écouter" }) {
  const utteranceRef = useRef(null);

  const playAudio = () => {
    if (utteranceRef.current) {
      window.speechSynthesis.cancel();
    }
    const voixLocale = voixParLangue[lang.toLowerCase()] || "fr-FR";
    const utterance = new SpeechSynthesisUtterance(text);
    const voixTrouvee = window.speechSynthesis.getVoices().find(v => v.lang === voixLocale);
    if (voixTrouvee) utterance.voice = voixTrouvee;
    utterance.lang = voixLocale;
    utterance.rate = 0.9;
    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    window.speechSynthesis.getVoices();
  }, []);

  return (
    <button onClick={playAudio} className="mt-2 px-3 py-1 bg-blue-100 rounded text-sm text-blue-700">
      {label}
    </button>
  );
}
