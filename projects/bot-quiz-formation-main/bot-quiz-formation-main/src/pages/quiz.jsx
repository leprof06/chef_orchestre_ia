// 📁 src/pages/quiz.jsx — Page principale visible par les élèves
import QuizInteractif from "../components/QuizInteractif";

export default function QuizPage() {
  return (
    <div className="min-h-screen bg-white p-6 flex flex-col items-center">
      <header className="mb-6 text-center">
        <h1 className="text-3xl font-bold">🧠 Quiz interactif - Support & Learn with Yann</h1>
        <p className="text-gray-600 mt-2">Choisissez un chapitre pour tester vos connaissances !</p>
      </header>

      <main className="w-full max-w-2xl">
        <QuizInteractif />
      </main>

      <footer className="mt-12 text-sm text-gray-400 text-center">
        © Yann Martinez - Support & Learn with Yann {new Date().getFullYear()}
      </footer>
    </div>
  );
}