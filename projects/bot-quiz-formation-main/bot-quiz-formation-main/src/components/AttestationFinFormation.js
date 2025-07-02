// 📁 components/AttestationFinFormation.js — Attestation de fin stylisée
import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';

export default function AttestationFinFormation({ langue }) {
  const [nom, setNom] = useState('');
  const [afficher, setAfficher] = useState(false);
  const attestationRef = useRef(null);

  const handleCapture = async () => {
    if (attestationRef.current) {
      const canvas = await html2canvas(attestationRef.current);
      const link = document.createElement('a');
      link.download = `attestation_fin_formation_${langue}.png`;
      link.href = canvas.toDataURL();
      link.click();
    }
  };

  const date = new Date().toLocaleDateString();

  return (
    <div className="text-center space-y-4">
      {!afficher ? (
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Entrez votre nom et prénom"
            value={nom}
            onChange={(e) => setNom(e.target.value)}
            className="border p-2 rounded w-full max-w-md"
          />
          <button
            onClick={() => setAfficher(true)}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Générer mon attestation
          </button>
        </div>
      ) : (
        <>
          <div
            ref={attestationRef}
            className="bg-white border-4 border-gray-400 p-8 max-w-xl mx-auto shadow-xl text-left font-serif relative"
          >
            <img src="/assets/logo.jpg" alt="Logo" className="w-24 mb-4" />
            <h1 className="text-2xl font-bold text-center mb-4 uppercase">
              Attestation de fin de formation en {langue}
            </h1>
            <p className="mb-6 text-lg">Nous attestons que :</p>
            <p className="text-xl font-bold mb-2">{nom || 'Utilisateur anonyme'}</p>
            <p>a suivi l’intégralité de la formation en ligne proposée pour cette langue.</p>
            <p className="text-sm text-right mt-4">Délivré le {date}</p>
            <img
              src="/assets/signature-yann.jpg"
              alt="Signature"
              className="w-32 mt-4 ml-auto"
            />
            <p className="text-sm text-right italic">Support & Learn – Yann</p>
          </div>
          <button
            onClick={handleCapture}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
          >
            📥 Télécharger l’attestation
          </button>
        </>
      )}
    </div>
  );
}
