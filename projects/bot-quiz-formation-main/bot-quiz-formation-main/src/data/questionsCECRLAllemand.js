// 📁 src/data/questionsCECRLAllemand.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Je m'appelle Yann' en allemand ?",
    options: [
      { text: "Ich heiße Yann", isCorrect: true },
      { text: "Ich bin Yann", isCorrect: false },
      { text: "Mein Name ist Yann", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis en allemand : Bonjour, comment ça va ?",
    correction: "Guten Tag, wie geht es dir ?"
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la bonne phrase pour commander un café ?",
    options: [
      { text: "Ich möchte einen Kaffee, bitte", isCorrect: true },
      { text: "Ich trinke einen Kaffee", isCorrect: false },
      { text: "Ich habe einen Kaffee", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime en allemand une opinion sur l'apprentissage des langues.",
    correction: "Ich finde, dass das Lernen von Sprachen sehr wichtig ist."
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Quel mot complète correctement la phrase : 'Obwohl es regnet, ... ich spazieren.'",
    audio: "Obwohl es regnet, ... ich spazieren.",
    options: [
      { text: "gehe", isCorrect: true },
      { text: "geht", isCorrect: false },
      { text: "gehen", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'pomme' en allemand ?",
    options: [
      { text: "Apfel", isCorrect: true },
      { text: "Brot", isCorrect: false },
      { text: "Milch", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète la phrase en allemand : Ich ___ müde.",
    correction: "bin"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon article défini pour 'Haus' ?",
    options: [
      { text: "das", isCorrect: true },
      { text: "der", isCorrect: false },
      { text: "die", isCorrect: false }
    ]
  }
];
