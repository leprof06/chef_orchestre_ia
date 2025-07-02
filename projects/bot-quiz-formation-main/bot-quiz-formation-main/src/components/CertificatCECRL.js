// 📁 components/CertificatCECRL.js — Certificat stylisé CECRL
import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';

export default function CertificatCECRL({ niveau, langue }) {
  const [nom, setNom] = useState('');
  const [afficher, setAfficher] = useState(false);
  const certRef = useRef(null);

  const handleCapture = async () => {
    if (certRef.current) {
      const canvas = await html2canvas(certRef.current);
      const link = document.createElement('a');
      link.download = `certificat_cecrl_${langue}.png`;
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
            Générer mon certificat
          </button>
        </div>
      ) : (
        <>
          <div
            ref={certRef}
            className="bg-white border-4 border-gray-400 p-8 max-w-xl mx-auto shadow-xl text-left font-serif"
          >
            <h1 className="text-2xl font-bold text-center mb-4 uppercase">
              Certificat de niveau en langue {langue}
            </h1>
            <p className="mb-6 text-lg">Nous certifions que :</p>
            <p className="text-xl font-bold mb-2">{nom || 'Utilisateur anonyme'}</p>
            <p>a atteint le niveau suivant selon les critères CECRL :</p>
            <p className="text-3xl text-green-700 font-bold my-4">{niveau}</p>
            <p className="text-sm text-right">Délivré le {date}</p>
            <p className="text-sm text-right italic">Support & Learn – Yann</p>
          </div>
          <button
            onClick={handleCapture}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
          >
            📥 Télécharger le certificat
          </button>
        </>
      )}
    </div>
  );
}
