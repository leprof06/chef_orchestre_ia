// 📁 pages/cecrl/chinois.js
import React from 'react';
import TestCECRL from '../../components/TestCECRL';
import { questionsCECRL } from '../../data/questionsCECRLChinois';

const CECRLChinois = () => {
  const questions = questionsCECRL.map((q, idx) => ({
    ...q,
    ordre: idx + 1,
    langCode: 'zh-CN'
  }));

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <h1 className="text-3xl text-center font-bold mb-6">Test CECRL – Chinois</h1>
      <TestCECRL questions={questions} />
    </div>
  );
};

export default CECRLChinois;
