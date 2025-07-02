// 📁 src/pages/niveau.jsx — Page pour les tests de niveau CECRL par langue

import Link from "next/link";

export default function PageNiveauLangue() {
  const langues = [
    { code: "allemand", label: "🇩🇪 Allemand" },
    { code: "anglais", label: "🇬🇧 Anglais" },
    { code: "espagnol", label: "🇪🇸 Espagnol" },
    { code: "japonais", label: "🇯🇵 Japonais" },
    { code: "russe", label: "🇷🇺 Russe" },
    { code: "chinois", label: "🇨🇳 Chinois" },
    { code: "coreen", label: "🇰🇷 Coréen" }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">🔍 Test de niveau CECRL</h1>
      <p className="mb-4 text-gray-700 text-center">
        Sélectionnez la langue pour passer le test et évaluer votre niveau.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {langues.map(({ code, label }) => (
          <Link
            key={code}
            href={`/niveau/${code}`}
            className="bg-blue-100 hover:bg-blue-200 transition p-4 rounded-xl text-center shadow"
          >
            <span className="text-lg font-semibold">{label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
