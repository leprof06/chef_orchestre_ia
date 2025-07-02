// 📁 src/pages/index.js — Page d’accueil avec quiz + test CECRL
import Link from 'next/link';

const langues = [
  { code: 'fr', label: 'Français' },
  { code: 'anglais', label: 'Anglais' },
  { code: 'allemand', label: 'Allemand' },
  { code: 'espagnol', label: 'Espagnol' },
  { code: 'japonais', label: 'Japonais' },
  { code: 'chinois', label: 'Chinois' },
  { code: 'coreen', label: 'Coréen' },
  { code: 'russe', label: 'Russe' }
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white p-8 text-center">
      <h1 className="text-3xl font-bold mb-4">📚 Bienvenue sur Support & Learn with Yann</h1>
      <p className="mb-6 text-gray-700">Choisissez votre langue pour accéder au contenu :</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {langues.map((lang) => (
          <div key={lang.code} className="border rounded-lg p-4 shadow-md">
            <h2 className="text-xl font-semibold mb-2">{lang.label}</h2>
            <div className="space-y-2">
              <Link href={`/quiz?lang=${lang.code}`}>
                <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                  🎯 Quiz par chapitres
                </button>
              </Link>
              <Link href={`/cecrl/${lang.code}`}>
                <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
                  🧪 Test de niveau CECRL
                </button>
              </Link>
            </div>
          </div>
        ))}
      </div>

      <footer className="mt-12 text-sm text-gray-500">
        © Yann Martinez – Support & Learn with Yann {new Date().getFullYear()}
      </footer>
    </div>
  );
}
