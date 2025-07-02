// 📁 src/data/questionsCECRLJaponais.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Bonjour' en japonais (le matin) ?",
    options: [
      { text: "おはようございます", isCorrect: true },
      { text: "こんばんは", isCorrect: false },
      { text: "ありがとう", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis : Je m'appelle Yann.",
    correction: "私はヤンと申します。"
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la bonne formule pour commander un café ?",
    options: [
      { text: "コーヒーをください", isCorrect: true },
      { text: "コーヒーが好きです", isCorrect: false },
      { text: "コーヒーがあります", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime ton opinion sur l'apprentissage des langues.",
    correction: "言語を学ぶことはとても大切だと思います。"
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Complète : '雨が降っても、...'",
    audio: "雨が降っても、...",
    options: [
      { text: "散歩します", isCorrect: true },
      { text: "きれいです", isCorrect: false },
      { text: "好きです", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'livre' en japonais ?",
    options: [
      { text: "本", isCorrect: true },
      { text: "水", isCorrect: false },
      { text: "花", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète : 私は学生___。",
    correction: "です"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon mot pour 'professeur' ?",
    options: [
      { text: "先生", isCorrect: true },
      { text: "学生", isCorrect: false },
      { text: "友達", isCorrect: false }
    ]
  }
];
