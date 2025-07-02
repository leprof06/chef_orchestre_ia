// 📁 src/data/questionsCECRLAnglais.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Que signifie cette phrase : 'She is reading a book' ?",
    options: [
      { text: "Elle lit un livre", isCorrect: true },
      { text: "Elle écrit un livre", isCorrect: false },
      { text: "Elle mange un livre", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Lis cette phrase : 'The cat is on the chair.' Que signifie-t-elle ?",
    correction: "Le chat est sur la chaise."
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Que veut dire : 'He is going to school.' ?",
    options: [
      { text: "Il va à l'école", isCorrect: true },
      { text: "Il revient de l'école", isCorrect: false },
      { text: "Il mange à l'école", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "A1",
    question: "Présente-toi en deux phrases simples.",
    correction: "My name is John. I am 25 years old."
  },
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "A2",
    question: "Écris une phrase pour dire ce que tu aimes faire.",
    correction: "I like reading books."
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "A1",
    question: "On entend : 'Hello, how are you?'. Que cela signifie-t-il ?",
    audio: "Hello, how are you?",
    options: [
      { text: "Bonjour, comment vas-tu ?", isCorrect: true },
      { text: "Quel âge as-tu ?", isCorrect: false },
      { text: "Où habites-tu ?", isCorrect: false }
    ]
  },
  {
    section: "oral",
    type: "qcm",
    niveau: "A2",
    question: "On entend : 'What is your name?'. Que cela veut dire ?",
    audio: "What is your name?",
    options: [
      { text: "Comment tu t’appelles ?", isCorrect: true },
      { text: "Comment ça va ?", isCorrect: false },
      { text: "Quel est ton âge ?", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'voiture' ?",
    options: [
      { text: "Car", isCorrect: true },
      { text: "House", isCorrect: false },
      { text: "Dog", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Traduis en anglais : une pomme, une table, un ami.",
    correction: "An apple, a table, a friend."
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel est le pronom correct pour 'je' ?",
    options: [
      { text: "I", isCorrect: true },
      { text: "Me", isCorrect: false },
      { text: "You", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A1",
    question: "Complète : I ____ a teacher.",
    correction: "I am a teacher."
  }
];
