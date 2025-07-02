// 📁 pages/cecrl/allemand.js
import React from 'react';
import TestCECRL from '../../components/TestCECRL';
import { questionsCECRL } from '../../data/questionsCECRLAllemand';

const CECRLAllemand = () => {
  const questions = questionsCECRL.map((q, idx) => ({
    ...q,
    ordre: idx + 1,
    langCode: 'de-DE'
  }));

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <h1 className="text-3xl text-center font-bold mb-6">Test CECRL – Allemand</h1>
      <TestCECRL questions={questions} />
    </div>
  );
};

export default CECRLAllemand;
