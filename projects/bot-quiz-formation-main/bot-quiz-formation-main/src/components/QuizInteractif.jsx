// 📁 src/components/QuizInteractif.jsx — Composant quiz avec navigation dynamique

import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

import { questionsParChapitre as allemand } from "../data/questionsAllemand";
import { questionsParChapitre as anglais } from "../data/questionsAnglais";
import { questionsParChapitre as espagnol } from "../data/questionsEspagnol";
import { questionsParChapitre as japonais } from "../data/questionsJaponais";
import { questionsParChapitre as russe } from "../data/questionsRusse";
import { questionsParChapitre as chinois } from "../data/questionsChinois";
import { questionsParChapitre as coreen } from "../data/questionsCoreen";
import AttestationFinFormation from "./AttestationFinFormation";

const banques = {
  allemand, anglais, espagnol, japonais, russe, chinois, coreen
};

export default function QuizInteractif() {
  const router = useRouter();
  const { lang } = router.query;
  const questionsParChapitre = banques[lang] || {};

  const [chapitreSelectionne, setChapitreSelectionne] = useState(null);
  const [current, setCurrent] = useState(0);
  const [showFeedback, setShowFeedback] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [inputText, setInputText] = useState("");
  const [score, setScore] = useState(0);
  const [quizTermine, setQuizTermine] = useState(false);

  const handleStartChapitre = (slug) => {
    setChapitreSelectionne(slug);
    setCurrent(0);
    setShowFeedback(false);
    setSelectedOption(null);
    setInputText("");
    setScore(0);
    setQuizTermine(false);
  };

  const questions = chapitreSelectionne ? questionsParChapitre[chapitreSelectionne] : [];

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    setShowFeedback(true);
    if (option.isCorrect) setScore(score + 1);
  };

  const handleOpenQuestionSubmit = () => {
    setShowFeedback(true);
  };

  const handleNext = () => {
    setShowFeedback(false);
    setSelectedOption(null);
    setInputText("");
    if (current + 1 >= questions.length) {
      setQuizTermine(true);
    } else {
      setCurrent(current + 1);
    }
  };

  const handleReset = () => {
    setChapitreSelectionne(null);
    setScore(0);
    setCurrent(0);
    setQuizTermine(false);
  };

  if (!lang) {
    return <p className="text-center p-6">Langue non spécifiée. <Link className="text-blue-500 underline" href="/">Retour à l'accueil</Link></p>;
  }

  if (!chapitreSelectionne) {
    return (
      <div className="p-4">
        <div className="mb-4">
          <Link href="/" className="text-blue-500 underline">← Retour à l’accueil</Link>
        </div>
        <h2 className="text-xl font-bold mb-4">Choisissez un chapitre :</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Object.keys(questionsParChapitre).map((slug) => (
            <button
              key={slug}
              className="p-4 border rounded-xl hover:bg-gray-100"
              onClick={() => handleStartChapitre(slug)}
            >
              📘 {slug.replace("chapitre", "Chapitre ")}
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (quizTermine) {
    const derniere = questions[questions.length - 1];
    if (derniere?.type === "attestation") {
      return <AttestationFinFormation nomFormation={lang} />;
    }
    return (
      <div className="text-center p-6">
        <h2 className="text-2xl font-semibold mb-2">🎉 Quiz terminé !</h2>
        <p className="mb-4">Votre score : {score} / {questions.length}</p>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded"
          onClick={handleReset}
        >
          Retour au menu du chapitre
        </button>
      </div>
    );
  }

  const q = questions[current];

  const handlePlayAudio = () => {
    const utterance = new SpeechSynthesisUtterance(q.question);
    const voices = speechSynthesis.getVoices();
    const langVoices = voices.filter(v => v.lang.toLowerCase().includes(lang));
    utterance.voice = langVoices.length > 0 ? langVoices[0] : voices[0];
    speechSynthesis.speak(utterance);
  };

  return (
    <div className="max-w-xl mx-auto p-4 border rounded-xl shadow-lg">
      <div className="mb-2">
        <button onClick={handleReset} className="text-sm text-blue-500 underline">← Retour aux chapitres</button>
        <span className="ml-4">
          <Link href="/" className="text-sm text-blue-500 underline">🏠 Accueil</Link>
        </span>
      </div>

      <h2 className="text-xl font-semibold mb-4">
        {q.type === "qcm" ? `Question ${current + 1} :` : `Exercice ${current + 1}`} ({chapitreSelectionne.replace("chapitre", "Chapitre ")})
      </h2>
      <p className="mb-4">{q.question}</p>
      {q.type !== "attestation" && (
        <button onClick={handlePlayAudio} className="mb-4 bg-gray-200 px-2 py-1 rounded">🔊 Écouter</button>
      )}

      {q.type === "qcm" ? (
        <div className="space-y-2">
          {q.options.map((opt, idx) => (
            <button
              key={idx}
              className={`w-full text-left px-4 py-2 rounded-lg border ${
                showFeedback && selectedOption === opt
                  ? opt.isCorrect
                    ? "bg-green-200 border-green-400"
                    : "bg-red-200 border-red-400"
                  : "hover:bg-gray-100"
              }`}
              onClick={() => handleOptionClick(opt)}
              disabled={showFeedback}
            >
              {opt.text}
            </button>
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="w-full border rounded p-2"
            rows={4}
            disabled={showFeedback}
          />
          {!showFeedback && (
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded"
              onClick={handleOpenQuestionSubmit}
            >Valider</button>
          )}
          {showFeedback && (
            <div className="mt-2 text-sm text-gray-700">
              ✅ Correction suggérée : <pre className="bg-gray-100 p-2 mt-1 whitespace-pre-wrap">{q.correction}</pre>
            </div>
          )}
        </div>
      )}

      {showFeedback && (
        <div className="mt-4">
          {q.type === "qcm" && (
            <p className="text-sm text-gray-600 italic">
              {selectedOption.isCorrect ? "✅ Bonne réponse !" : "❌ Mauvaise réponse."} {selectedOption.explanation}
            </p>
          )}
          <button
            className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
            onClick={handleNext}
          >
            {current + 1 >= questions.length ? "Terminer" : "Suivant"}
          </button>
        </div>
      )}
    </div>
  );
}
