// 📁 src/data/questionsCECRLRusse.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Bonjour' en russe ?",
    options: [
      { text: "Здравствуйте", isCorrect: true },
      { text: "Спасибо", isCorrect: false },
      { text: "Пока", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis : Je m'appelle Yann.",
    correction: "Меня зовут Ян."
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la bonne phrase pour commander un café ?",
    options: [
      { text: "Я бы хотел кофе, пожалуйста", isCorrect: true },
      { text: "У меня есть кофе", isCorrect: false },
      { text: "Кофе нравится мне", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime ton opinion sur l'apprentissage des langues.",
    correction: "Я считаю, что изучение языков очень важно."
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Complète : 'Хотя идёт дождь, ...'",
    audio: "Хотя идёт дождь, ...",
    options: [
      { text: "я всё равно иду гулять", isCorrect: true },
      { text: "это красиво", isCorrect: false },
      { text: "я не знаю", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'eau' en russe ?",
    options: [
      { text: "вода", isCorrect: true },
      { text: "молоко", isCorrect: false },
      { text: "хлеб", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète : Я ___ студент.",
    correction: "есть"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon mot pour 'professeur' ?",
    options: [
      { text: "учитель", isCorrect: true },
      { text: "студент", isCorrect: false },
      { text: "врач", isCorrect: false }
    ]
  }
];
