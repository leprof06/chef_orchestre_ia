// 📁 src/data/questionsAnglais.js — Toutes les questions de la formation Anglais

 const questionsAnglais = {
  chapitre1: [
    {
      type: "ouverte",
      question: "Write a mini dialogue between two people meeting for the first time using classroom vocabulary.",
      correction: `A: Hi! My name is Sophie.\nB: Hello! I'm Max.\nA: Nice to meet you, Max.\nB: Nice to meet you too.`
    }
  ],
  chapitre2: [
    {
      type: "qcm",
      question: "How do you say '11h45' in English?",
      options: [
        { text: "A quarter to twelve", isCorrect: true, explanation: "Correct : 11h45 signifie un quart d’heure avant midi." },
        { text: "A quarter past eleven", isCorrect: false, explanation: "Cela signifie 11h15." },
        { text: "Eleven forty-five", isCorrect: false, explanation: "Acceptable mais moins courant à l'oral en classe." }
      ]
    },
    {
      type: "ouverte",
      question: "Write a shopping dialogue using expressions seen in class.",
      correction: `Customer: Hello, I’d like a loaf of bread.\nShopkeeper: Sure, anything else?\nCustomer: Yes, a bottle of water, please.\nShopkeeper: That will be 3 dollars.`
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Translate the following dates into English: Monday 2 September, Wednesday 15 August, Thursday 25 March.",
      correction: `Monday, the second of September; Wednesday, the fifteenth of August; Thursday, the twenty-fifth of March.`
    },
    {
      type: "qcm",
      question: "Translate: 'La fenêtre est ouverte'",
      options: [
        { text: "The window is open", isCorrect: true, explanation: "Bonne traduction." },
        { text: "The window is opened", isCorrect: false, explanation: "'Opened' est un participe passé, pas un adjectif ici." },
        { text: "Window is open", isCorrect: false, explanation: "Il manque l'article 'The'." }
      ]
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Translate the following: 'Je ne comprends pas ce que tu veux dire.', 'How do you pronounce this word?', 'Qu’as-tu dit ?', 'Do you understand English?', 'Tournez à droite à côté du cimetière.'",
      correction: `I don't understand what you mean. / How do you pronounce this word? / What did you say? / Do you understand English? / Turn right next to the cemetery.`
    }
  ],
  chapitre5: [
    {
      type: "ouverte",
      question: "Translate these: 'Mon frère est maigre', 'Son T-shirt est bon marché', 'He is ugly', 'C’est un pantalon épais', 'Elle va dehors avec sa mère'.",
      correction: `My brother is skinny. / His T-shirt is cheap. / He is ugly. / These are thick trousers. / She goes outside with her mother.`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Create a dialogue in a restaurant with reservation, order and asking for the bill.",
      correction: `A: Hello, I have a reservation for two.\nB: Right this way.\n...\nA: Could we have the bill, please?`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Tell your day in the present, past and future tenses.",
      correction: `I wake up at 7 AM. Yesterday, I went to school. Tomorrow, I will study English.`
    },
    {
      type: "qcm",
      question: "Choose the correct tag question: 'You don't like coffee, ...?'",
      options: [
        { text: "do you?", isCorrect: true, explanation: "Bonne structure pour une phrase négative." },
        { text: "don't you?", isCorrect: false, explanation: "La phrase est déjà négative, il faut un auxiliaire positif." },
        { text: "aren’t you?", isCorrect: false, explanation: "Ne correspond pas au verbe 'like'." }
      ]
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Simulate a phone conversation to plan a meeting for your boss and ask about the weather. Include at least one subordinate clause.",
      correction: `Hello, I would like to schedule a meeting for my manager. Can you tell me what the weather will be like on Monday?`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Write an email to apply for a job and simulate an interview.",
      correction: `Dear Sir or Madam, I am writing to apply for the position of... / Interview: Tell me about yourself...`
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Give your opinion on any topic with two arguments for and two against.",
      correction: `I think social media is useful because it connects people. However, it can also waste time and cause stress.`
    },
    {
      type: "qcm",
      question: "Transform to conditional: 'I am in the mall'",
      options: [
        { text: "I would be in the mall", isCorrect: true, explanation: "Bonne transformation au conditionnel." },
        { text: "I am going to the mall", isCorrect: false, explanation: "C’est du futur, pas du conditionnel." },
        { text: "I was in the mall", isCorrect: false, explanation: "C’est du passé simple." }
      ]
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Simulate a phone call to schedule a medical appointment.",
      correction: `Hello, I would like to book an appointment with Dr. Smith. What times are available?`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Write a short summary and your opinion on the course.",
      correction: `The lessons were very helpful. I learned a lot and enjoyed the activities.`
    },
    {
      type: "attestation" }
  ]
};

export const questionsParChapitre = questionsAnglais;