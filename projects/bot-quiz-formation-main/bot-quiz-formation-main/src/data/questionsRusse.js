// 📁 src/data/questionsRusse.js — Quiz basé sur l’ordre des chapitres du cours Russe

const questionsRusse= {
  chapitre1: [
    {
      type: "ouverte",
      question: "Présente-toi en russe (nom, nationalité, langue parlée).",
      correction: `Здравствуйте! Меня зовут Мария. Я француженка. Я говорю по-французски.`
    },
    {
      type: "qcm",
      question: "Comment dit-on 'Bonjour' de manière formelle en russe ?",
      options: [
        { text: "Здравствуйте", isCorrect: true, explanation: "C’est la formule formelle de salutation." },
        { text: "Привет", isCorrect: false, explanation: "Forme familière pour amis ou enfants." },
        { text: "До свидания", isCorrect: false, explanation: "Cela signifie 'au revoir'." }
      ]
    }
  ],
  chapitre2: [
    {
      type: "ouverte",
      question: "Donne ton prénom et ta nationalité en russe.",
      correction: `Меня зовут Жюль. Я француз.`
    },
    {
      type: "qcm",
      question: "Choisis la bonne phrase :",
      options: [
        { text: "Я живу в Париже", isCorrect: true, explanation: "Phrase correcte pour 'je vis à Paris'." },
        { text: "Я живёт в Париже", isCorrect: false, explanation: "Verbe mal conjugué." },
        { text: "Я Париж живу", isCorrect: false, explanation: "Ordre des mots incorrect." }
      ]
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Traduis : J’habite à Nice. Je suis étudiant. J’ai 25 ans.",
      correction: `Я живу в Ницце. Я студент. Мне 25 лет.`
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Donne trois phrases avec les membres de ta famille.",
      correction: `У меня есть мама, папа и сестра. Моя мама — учитель. Мой папа работает в банке.`
    }
  ],
  chapitre5: [
    {
      type: "qcm",
      question: "Comment dit-on 'merci' en russe ?",
      options: [
        { text: "Спасибо", isCorrect: true, explanation: "Bonne réponse." },
        { text: "Пожалуйста", isCorrect: false, explanation: "Cela signifie 's’il vous plaît' ou 'je vous en prie'." },
        { text: "Здравствуйте", isCorrect: false, explanation: "C’est une salutation." }
      ]
    },
    {
      type: "ouverte",
      question: "Traduis : Bonjour, comment ça va ? — Très bien, merci.",
      correction: `Здравствуйте, как дела? — Очень хорошо, спасибо.`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Conjugue le verbe 'говорить' (parler) au présent pour je, tu, il/elle.",
      correction: `Я говорю / Ты говоришь / Он говорит`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Décris ta journée (présent).",
      correction: `Я встаю в 7 часов, завтракаю, потом иду в университет.`
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Traduis : J’étudie le russe. J’aime la langue russe. C’est intéressant.",
      correction: `Я изучаю русский язык. Я люблю русский язык. Это интересно.`
    }
  ],
  chapitre9: [
    {
      type: "qcm",
      question: "Quel est l’adjectif pour 'russe' au masculin ?",
      options: [
        { text: "русский", isCorrect: true, explanation: "Bonne forme au masculin." },
        { text: "русская", isCorrect: false, explanation: "C’est la forme féminine." },
        { text: "русские", isCorrect: false, explanation: "C’est la forme plurielle." }
      ]
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Fais une demande polie dans un café en russe.",
      correction: `Можно, пожалуйста, кофе и бутерброд?`
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Donne ton opinion sur la langue russe.",
      correction: `Русский язык трудный, но очень красивый.`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Exprime ce que tu as appris jusqu’ici.",
      correction: `Я научился читать, писать и говорить по-русски. Я понимаю простые фразы.`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsRusse;