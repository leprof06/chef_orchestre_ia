// 📁 src/data/questionsCECRLChinois.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Bonjour' en chinois ?",
    options: [
      { text: "你好", isCorrect: true },
      { text: "谢谢", isCorrect: false },
      { text: "再见", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis : Je m'appelle Yann.",
    correction: "我叫Yann。"
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la bonne phrase pour commander un café ?",
    options: [
      { text: "我要一杯咖啡", isCorrect: true },
      { text: "我喜欢咖啡", isCorrect: false },
      { text: "我有咖啡", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime en chinois ton opinion sur l'apprentissage des langues.",
    correction: "我觉得学习语言非常重要。"
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Complète : '虽然下雨，...'",
    audio: "虽然下雨，...",
    options: [
      { text: "我还是出去散步。", isCorrect: true },
      { text: "我喜欢。", isCorrect: false },
      { text: "我不知道。", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'eau' en chinois ?",
    options: [
      { text: "水", isCorrect: true },
      { text: "火", isCorrect: false },
      { text: "风", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète la phrase : 我 ___ 学生。",
    correction: "是"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon classificateur pour 'livre' ?",
    options: [
      { text: "本", isCorrect: true },
      { text: "只", isCorrect: false },
      { text: "个", isCorrect: false }
    ]
  }
];
