// 📁 src/data/questionsChinois.js — Quiz basé sur l’ordre des chapitres du cours de chinois

const questionsChinois  = {
  chapitre1: [
    {
      type: "qcm",
      question: "Comment dit-on 'Bonjour' en chinois ?",
      options: [
        { text: "你好 (nǐ hǎo)", isCorrect: true, explanation: "C’est la salutation standard." },
        { text: "谢谢 (xièxiè)", isCorrect: false, explanation: "Cela veut dire 'merci'." },
        { text: "再见 (zàijiàn)", isCorrect: false, explanation: "Cela veut dire 'au revoir'." }
      ]
    },
    {
      type: "ouverte",
      question: "Traduis : Bonjour, comment vas-tu ? — Très bien, merci.",
      correction: `你好，你好吗？— 我很好，谢谢。`
    }
  ],
  chapitre2: [
    {
      type: "ouverte",
      question: "Présente-toi (nom + prénom) en chinois.",
      correction: `我叫马丽。`
    },
    {
      type: "qcm",
      question: "Que signifie '你叫什么名字？' ?",
      options: [
        { text: "Comment tu t’appelles ?", isCorrect: true, explanation: "Bonne traduction." },
        { text: "Où habites-tu ?", isCorrect: false, explanation: "C’est 你住在哪儿？" },
        { text: "Quel âge as-tu ?", isCorrect: false, explanation: "C’est 你几岁？" }
      ]
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Dis ta nationalité et ton lieu d’habitation en chinois.",
      correction: `我是法国人。我住在巴黎。`
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Traduis : Je parle français et un peu chinois.",
      correction: `我会说法语，也会说一点汉语。`
    }
  ],
  chapitre5: [
    {
      type: "ouverte",
      question: "Présente ta famille : mère, père, frère ou sœur.",
      correction: `我有妈妈，爸爸和姐姐。`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Traduis : J’ai 20 ans. Je suis étudiant(e).",
      correction: `我二十岁。我是学生。`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Décris une journée type : lever, manger, dormir.",
      correction: `我早上七点起床，中午吃饭，晚上十点睡觉。`
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Exprime ce que tu aimes (langue, nourriture, culture).",
      correction: `我喜欢汉语，也喜欢中国菜和中国文化。`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Passe une commande simple dans un restaurant.",
      correction: `请给我一杯茶，一个包子。`
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Exprime ton opinion sur le chinois.",
      correction: `我觉得汉语很有意思，有点难但是很好听。`
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Fais une demande polie (réservation ou question simple).",
      correction: `请问，明天可以预订吗？`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Exprime ce que tu as appris jusqu’ici en chinois.",
      correction: `我学了很多词汇，会用中文介绍自己，点菜，聊天。`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsChinois;