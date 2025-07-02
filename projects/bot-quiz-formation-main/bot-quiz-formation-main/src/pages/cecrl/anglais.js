// 📁 pages/cecrl/anglais.js
import React from 'react';
import TestCECRL from '../../components/TestCECRL';
import { questionsCECRL } from '../../data/questionsCECRLAnglais';

export default function CECRLAnglais() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <h1 className="text-3xl text-center font-bold mb-6">
        Test CECRL – Anglais
      </h1>
      <TestCECRL questions={questionsCECRL} />
    </div>
  );
}
