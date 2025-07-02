// 📁 src/data/questionsCECRLEspagnol.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Bonjour' en espagnol ?",
    options: [
      { text: "Hola", isCorrect: true },
      { text: "Gracias", isCorrect: false },
      { text: "Adiós", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis : Bonjour, je m'appelle Yann.",
    correction: "Hola, me llamo Yann."
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la bonne formule pour commander un café ?",
    options: [
      { text: "Quisiera un café, por favor", isCorrect: true },
      { text: "Tengo un café", isCorrect: false },
      { text: "Me gusta café", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime ton opinion sur l'apprentissage des langues.",
    correction: "Creo que aprender idiomas es muy importante."
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Complète : 'Aunque llueve, ...'",
    audio: "Aunque llueve, ...",
    options: [
      { text: "salgo a caminar", isCorrect: true },
      { text: "es bonito", isCorrect: false },
      { text: "me gusta", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'chat' en espagnol ?",
    options: [
      { text: "Gato", isCorrect: true },
      { text: "Perro", isCorrect: false },
      { text: "Casa", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète la phrase : Yo ___ estudiante.",
    correction: "soy"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon article défini pour 'libro' ?",
    options: [
      { text: "el", isCorrect: true },
      { text: "la", isCorrect: false },
      { text: "los", isCorrect: false }
    ]
  }
];
