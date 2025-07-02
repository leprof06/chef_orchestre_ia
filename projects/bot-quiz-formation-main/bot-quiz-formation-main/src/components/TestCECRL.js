// 📁 components/TestCECRL.js
import React, { useState, useRef } from 'react';
import TTS from "./TTS";
import html2canvas from 'html2canvas';
import CertificatCECRL from './CertificatCECRL';
import { useRouter } from 'next/router';

export default function TestCECRL({ questions }) {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [niveauEstime, setNiveauEstime] = useState('');
  const resultRef = useRef(null);
  const router = useRouter();
  const langue = router.query.lang || router.pathname.split('/').pop();

  const handleChange = (questionId, value) => {
    setAnswers({ ...answers, [questionId]: value });
  };

  const handleSubmit = () => {
    setSubmitted(true);
    calculerNiveau();
  };

  const calculerNiveau = () => {
    const scoreParNiveau = {};
    const totalParNiveau = {};

    questions.forEach((q, idx) => {
      const niveau = q.niveau || 'A1';
      const reponse = answers[idx];
      const attendu = q.correction?.toLowerCase().trim();

      if (!totalParNiveau[niveau]) {
        totalParNiveau[niveau] = 0;
        scoreParNiveau[niveau] = 0;
      }
      totalParNiveau[niveau]++;

      if (q.type === 'qcm') {
        const bonne = q.options.find((opt) => opt.isCorrect)?.text;
        if (reponse === bonne) scoreParNiveau[niveau]++;
      } else if (q.type === 'ouverte') {
        if (reponse && attendu && reponse.toLowerCase().trim() === attendu) {
          scoreParNiveau[niveau]++;
        }
      }
    });

    const niveauxOrdres = ['A1', 'A2', 'B1', 'B2'];
    let meilleur = 'A1';

    for (let i = niveauxOrdres.length - 1; i >= 0; i--) {
      const n = niveauxOrdres[i];
      const total = totalParNiveau[n] || 0;
      const bons = scoreParNiveau[n] || 0;
      const taux = total > 0 ? bons / total : 0;
      if (taux >= 0.7) {
        meilleur = n;
        break;
      }
    }
    setNiveauEstime(meilleur);
  };

  const handleCapture = async () => {
    if (resultRef.current) {
      const canvas = await html2canvas(resultRef.current);
      const link = document.createElement('a');
      link.download = 'certificat_cecrl.png';
      link.href = canvas.toDataURL();
      link.click();
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-center">Test de niveau CECRL</h2>
      {questions.map((q, index) => (
        <div key={index} className="p-4 border rounded shadow">
          <p className="mb-2">
            {q.audio ? <TTS text={q.audio} langCode={q.langCode} label="🔊 Écouter l'audio" /> : q.question} 
          </p>

          {q.options ? (
            <div className="mt-2 space-y-1">
              {q.options.map((opt, i) => (
                <label key={i} className="block">
                  <input
                    type="radio"
                    name={`q-${index}`}
                    value={opt.text}
                    checked={answers[index] === opt.text}
                    onChange={() => handleChange(index, opt.text)}
                  />{' '}{opt.text}
                </label>
              ))}
            </div>
          ) : (
            <input
              type="text"
              className="mt-2 p-1 border w-full"
              value={answers[index] || ''}
              onChange={(e) => handleChange(index, e.target.value)}
            />
          )}
        </div>
      ))}

      {!submitted ? (
        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Valider mes réponses
        </button>
      ) : (
        <>
          <div
            ref={resultRef}
            className="text-center text-xl mt-4 p-6 border-2 border-dashed border-green-600 rounded bg-white"
          >
            ✅ Votre niveau estimé : <span className="font-bold text-green-700 text-2xl">{niveauEstime}</span>
            <p className="mt-2 text-sm text-gray-500">Vous pouvez faire une capture d’écran ou cliquer ci-dessous pour télécharger un certificat.</p>
          </div>
          <CertificatCECRL niveau={niveauEstime} langue={langue} />
        </>
      )}
    </div>
  );
}
