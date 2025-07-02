// 📁 src/data/questionsEspagnol.js — Questions pour la formation Espagnol

const questionsEspagnol  = {
  chapitre1: [
    {
      type: "ouverte",
      question: "Présente-toi en espagnol avec ton nom, ton origine et ta langue parlée.",
      correction: `Hola, me llamo Ana. Soy francesa y hablo francés.`
    },
    {
      type: "qcm",
      question: "Comment dit-on 'Bonjour, je m'appelle Marie' ?",
      options: [
        { text: "Hola, me llamo Marie", isCorrect: true, explanation: "C'est la bonne traduction." },
        { text: "Buenos días, me llamo Marie", isCorrect: false, explanation: "Buenos días est plus formel et contextuel." },
        { text: "Hola, soy Marie llamo", isCorrect: false, explanation: "L'ordre des mots est incorrect." }
      ]
    }
  ],
  chapitre2: [
    {
      type: "ouverte",
      question: "Conjugue les verbes SER et ESTAR à la 1re personne du singulier.",
      correction: `Yo soy / Yo estoy`
    },
    {
      type: "qcm",
      question: "Quelle est la bonne traduction de 'Je suis étudiant' ?",
      options: [
        { text: "Soy estudiante", isCorrect: true, explanation: "Le verbe 'ser' est utilisé pour l'identité." },
        { text: "Estoy estudiante", isCorrect: false, explanation: "'Estar' n'est pas utilisé pour la profession ou le statut." },
        { text: "Es estudiante", isCorrect: false, explanation: "'Es' est la 3e personne du singulier." }
      ]
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Écris un dialogue dans un restaurant pour commander à manger.",
      correction: `Camarero: ¿Qué desea comer?\nCliente: Una paella, por favor.\nCamarero: ¿Y para beber?\nCliente: Una copa de vino tinto.`
    },
    {
      type: "qcm",
      question: "Comment dit-on 'l’addition, s’il vous plaît' ?",
      options: [
        { text: "La cuenta, por favor", isCorrect: true, explanation: "C’est l’expression correcte et courante." },
        { text: "El cuento, por favor", isCorrect: false, explanation: "‘Cuento’ veut dire une histoire." },
        { text: "El cuenta, por favor", isCorrect: false, explanation: "‘Cuenta’ est féminin ici." }
      ]
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Traduis ces phrases : J’ai 25 ans. / J’ai deux frères. / Il a un chien.",
      correction: `Tengo 25 años. / Tengo dos hermanos. / Él tiene un perro.`
    }
  ],
  chapitre5: [
    {
      type: "qcm",
      question: "Choisis le bon adjectif possessif : '_____ casa es grande' (ma maison)",
      options: [
        { text: "Mi", isCorrect: true, explanation: "Correct : 'Mi casa' = ma maison." },
        { text: "Su", isCorrect: false, explanation: "'Su' signifie 'sa' (à lui/elle)." },
        { text: "Tu", isCorrect: false, explanation: "'Tu' signifie 'ta'." }
      ]
    },
    {
      type: "ouverte",
      question: "Décris ta famille en 3 phrases.",
      correction: `Tengo un hermano y una hermana. Mis padres se llaman Ana y Luis. Vivimos en Lyon.`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Conjugue les verbes HABLAR, COMER et VIVIR au présent de l’indicatif.",
      correction: `Yo hablo, tú hablas, él habla / Yo como, tú comes, él come / Yo vivo, tú vives, él vive.`
    }
  ],
  chapitre7: [
    {
      type: "qcm",
      question: "Comment demande-t-on l’heure ?",
      options: [
        { text: "¿Qué hora es?", isCorrect: true, explanation: "C’est l’expression correcte." },
        { text: "¿Qué es hora?", isCorrect: false, explanation: "Structure incorrecte." },
        { text: "¿Cuál hora es?", isCorrect: false, explanation: "Ce n’est pas utilisé ainsi." }
      ]
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Donne 3 moyens de transport en espagnol et une phrase avec chacun.",
      correction: `Voy en coche. / Tomo el autobús. / Viajo en tren.`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Traduis en espagnol : Où vas-tu ? / Je vais au supermarché / Il va à l’école.",
      correction: `¿Adónde vas? / Voy al supermercado / Él va a la escuela.`
    }
  ],
  chapitre10: [
    {
      type: "qcm",
      question: "Choisis la bonne conjugaison de 'tener' à la 1re personne du singulier",
      options: [
        { text: "Tengo", isCorrect: true, explanation: "C’est la forme correcte." },
        { text: "Tienes", isCorrect: false, explanation: "C’est la 2e personne du singulier." },
        { text: "Tiene", isCorrect: false, explanation: "C’est la 3e personne." }
      ]
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Fais une description physique de toi en espagnol.",
      correction: `Soy alta, tengo el pelo largo y los ojos marrones.`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Exprime ton opinion sur les cours d’espagnol en 2 phrases.",
      correction: `Me gustan mucho las clases de español. Aprendo mucho y es divertido.`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsEspagnol;