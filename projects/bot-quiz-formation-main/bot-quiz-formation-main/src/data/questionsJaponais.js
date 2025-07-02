// 📁 src/data/questionsJaponais.js — Quiz conforme au plan du cours Word

const questionsJaponais = {
  chapitre1: [
    {
      type: "qcm",
      question: "Comment dit-on 'Bonjour' ?",
      options: [
        { text: "おはようございます", isCorrect: true, explanation: "Formule polie du matin." },
        { text: "さようなら", isCorrect: false, explanation: "Cela veut dire 'au revoir'." },
        { text: "ありがとう", isCorrect: false, explanation: "Cela veut dire 'merci'." }
      ]
    },
    {
      type: "ouverte",
      question: "Traduis : Bonjour, comment vas-tu ? — Très bien, merci.",
      correction: `おはようございます、お元気ですか？— はい、元気です。ありがとう。`
    }
  ],
  chapitre2: [
    {
      type: "ouverte",
      question: "Présente-toi (nom + prénom).",
      correction: `はじめまして。マリと申します。`
    },
    {
      type: "qcm",
      question: "Que veut dire 'おなまえは？' ?",
      options: [
        { text: "Quel est ton nom ?", isCorrect: true, explanation: "Traduction correcte." },
        { text: "Comment vas-tu ?", isCorrect: false, explanation: "C’est 'お元気ですか？'" },
        { text: "Tu parles japonais ?", isCorrect: false, explanation: "C’est '日本語を話せますか？'" }
      ]
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Traduis : Je suis français(e). J’habite à Paris.",
      correction: `フランス人です。パリに住んでいます。`
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Traduis : Je parle français et un peu japonais.",
      correction: `フランス語を話します。日本語も少し話せます。`
    }
  ],
  chapitre5: [
    {
      type: "ouverte",
      question: "Présente ta famille (3 membres).",
      correction: `母と父と兄がいます。`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Traduis : J’ai 20 ans. Je suis étudiant(e).",
      correction: `二十歳です。学生です。`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Décris une journée type (lever, activité, coucher).",
      correction: `朝7時に起きて、午後に勉強して、夜11時に寝ます。`
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Exprime ce que tu aimes (langue, culture, nourriture).",
      correction: `日本語、日本の文化と寿司が好きです。`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Passe une commande simple dans un café.",
      correction: `すみません、コーヒーとサンドイッチをください。`
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Exprime ton opinion sur les cours de japonais.",
      correction: `日本語の授業はとても面白くて役に立ちます。`
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Simule une demande polie (réservation ou question simple).",
      correction: `明日の予約をお願いできますか？`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Exprime ce que tu as appris jusqu’ici en japonais.",
      correction: `自己紹介、注文、日常会話ができるようになりました。`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsJaponais;