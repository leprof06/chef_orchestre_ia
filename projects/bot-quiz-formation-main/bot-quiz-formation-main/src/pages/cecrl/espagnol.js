// 📁 pages/cecrl/espagnol.js
import React from 'react';
import TestCECRL from '../../components/TestCECRL';
import { questionsCECRL } from '../../data/questionsCECRLEspagnol';

const CECRLEspagnol = () => {
  const questions = questionsCECRL.map((q, idx) => ({
    ...q,
    ordre: idx + 1,
    langCode: 'es-ES'
  }));

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <h1 className="text-3xl text-center font-bold mb-6">Test CECRL – Espagnol</h1>
      <TestCECRL questions={questions} />
    </div>
  );
};

export default CECRLEspagnol;
