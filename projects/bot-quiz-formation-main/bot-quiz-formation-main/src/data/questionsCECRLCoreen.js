// 📁 src/data/questionsCECRLCoreen.js — Test CECRL standardisé (sans oral)

export const questionsCECRL = [
  // 📘 Compréhension écrite
  {
    section: "lecture",
    type: "qcm",
    niveau: "A1",
    question: "Comment dit-on 'Bonjour' en coréen ?",
    options: [
      { text: "안녕하세요", isCorrect: true },
      { text: "감사합니다", isCorrect: false },
      { text: "안녕히 계세요", isCorrect: false }
    ]
  },
  {
    section: "lecture",
    type: "ouverte",
    niveau: "A1",
    question: "Traduis en coréen : Je m'appelle Yann.",
    correction: "제 이름은 얀입니다."
  },
  {
    section: "lecture",
    type: "qcm",
    niveau: "A2",
    question: "Quelle est la phrase correcte pour dire 'Je veux du kimchi' ?",
    options: [
      { text: "김치를 먹고 싶어요", isCorrect: true },
      { text: "김치 좋아요", isCorrect: false },
      { text: "김치 예뻐요", isCorrect: false }
    ]
  },

  // ✍️ Expression écrite
  {
    section: "ecriture",
    type: "ouverte",
    niveau: "B1",
    question: "Exprime en coréen ton opinion sur la langue coréenne.",
    correction: "한국어는 아름답고 배우기 흥미로워요."
  },

  // 👂 Compréhension orale
  {
    section: "oral",
    type: "qcm",
    niveau: "B2",
    question: "Complète : '비가 오지만 ...'",
    audio: "비가 오지만 ...",
    options: [
      { text: "산책해요", isCorrect: true },
      { text: "예뻐요", isCorrect: false },
      { text: "있어요", isCorrect: false }
    ]
  },

  // 🧠 Vocabulaire et grammaire
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A1",
    question: "Quel mot signifie 'eau' en coréen ?",
    options: [
      { text: "물", isCorrect: true },
      { text: "불", isCorrect: false },
      { text: "공기", isCorrect: false }
    ]
  },
  {
    section: "vocabulaire",
    type: "ouverte",
    niveau: "A2",
    question: "Complète la phrase : 저는 학생___",
    correction: "입니다"
  },
  {
    section: "vocabulaire",
    type: "qcm",
    niveau: "A2",
    question: "Quel est le bon mot pour 'professeur' ?",
    options: [
      { text: "선생님", isCorrect: true },
      { text: "학생", isCorrect: false },
      { text: "의사", isCorrect: false }
    ]
  }
];
