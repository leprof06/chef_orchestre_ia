// 📁 components/Quiz.js — Affiche un quiz chapitre par chapitre
import React, { useState } from 'react';
import AttestationFinFormation from './AttestationFinFormation';

export default function Quiz({ questionsParChapitre, langue }) {
  const chapitres = Object.keys(questionsParChapitre);
  const [chapitreActuel, setChapitreActuel] = useState(chapitres[0]);
  const questions = questionsParChapitre[chapitreActuel];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2 justify-center">
        {chapitres.map((chap) => (
          <button
            key={chap}
            onClick={() => setChapitreActuel(chap)}
            className={`px-3 py-1 rounded ${chap === chapitreActuel ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            {chap}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {questions.map((question, idx) => {
          if (question.type === 'attestation') {
            return <AttestationFinFormation langue={langue} key={idx} />;
          }
          return (
            <div key={idx} className="border p-4 rounded bg-white shadow">
              {/* Ton rendu de question ici, qcm / ouverte */}
              <p><strong>Question :</strong> {question.question}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
