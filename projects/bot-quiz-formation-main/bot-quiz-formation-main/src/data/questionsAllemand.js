// 📁 src/data/questionsAllemand.js — Toutes les questions de la formation Allemand

const questionsAllemand = {
  chapitre1: [
    {
      type: "ouverte",
      question: "Écris un mini dialogue entre deux personnes qui se rencontrent pour la première fois.",
      correction: `A: Hallo! Ich heiße Sophie.\nB: Guten Tag! Ich bin Max.\nA: Freut mich, Max.\nB: Freut mich auch.`
    }
  ],
  chapitre2: [
    {
      type: "qcm",
      question: "Comment dit-on '11h45' en allemand ?",
      options: [
        { text: "Viertel vor zwölf", isCorrect: true, explanation: "C’est un quart d’heure avant midi." },
        { text: "Viertel nach elf", isCorrect: false, explanation: "Cela signifie 11h15." },
        { text: "Elf Uhr fünfundvierzig", isCorrect: false, explanation: "Correct mais peu courant à l’oral." }
      ]
    },
    {
      type: "ouverte",
      question: "Écris un dialogue de shopping avec les phrases vues en cours.",
      correction: `A: Guten Tag, ich hätte gern ein Brötchen.\nB: Gerne. Noch etwas?\nA: Ja, ein Kaffee bitte.\nB: Das macht 3 Euro.`
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Donne les dates suivantes en allemand : Lundi 2 septembre, Mercredi 15 août, Jeudi 25 mars.",
      correction: `Montag, der zweite September; Mittwoch, der fünfzehnte August; Donnerstag, der fünfundzwanzigste März.`
    },
    {
      type: "qcm",
      question: "Comment traduit-on : 'La fenêtre est ouverte' ?",
      options: [
        { text: "Das Fenster ist offen", isCorrect: true, explanation: "C'est correct." },
        { text: "Der Fenster ist geöffnet", isCorrect: false, explanation: "Faux genre (der au lieu de das)." },
        { text: "Die Fenster ist offen", isCorrect: false, explanation: "Faux article (die pour Fenster singulier)." }
      ]
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Traduis les phrases suivantes en allemand : Je ne comprends pas ce que tu veux dire, Qu’as-tu dit ?, Verstehst du Deutsch?",
      correction: `Ich verstehe nicht, was du meinst. / Was hast du gesagt? / Verstehst du Deutsch?`
    }
  ],
  chapitre5: [
    {
      type: "ouverte",
      question: "Traduis ces phrases : Mon frère est mince. Son t-shirt est bon marché. Elle va dehors avec sa mère.",
      correction: `Mein Bruder ist dünn. Sein T-Shirt ist billig. Sie geht mit ihrer Mutter nach draußen.`
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Recrée un dialogue au restaurant avec réservation et jusqu’à l’addition.",
      correction: `Guten Tag, ich habe einen Tisch für zwei reserviert.\nNatürlich. Folgen Sie mir bitte.\n...\nDie Rechnung bitte.`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Raconte ta journée au présent, passé et futur.",
      correction: `Ich stehe um 7 Uhr auf... Gestern habe ich... Morgen werde ich...`
    },
    {
      type: "qcm",
      question: "Transforme : Ich bin im Einkaufzentrum (au conditionnel)",
      options: [
        { text: "Ich wäre im Einkaufzentrum", isCorrect: true, explanation: "Correct pour Konjunktiv II." },
        { text: "Ich bin im Einkaufzentrum gewesen", isCorrect: false, explanation: "Ceci est du parfait, pas du conditionnel." },
        { text: "Ich wurde im Einkaufzentrum", isCorrect: false, explanation: "Faux usage du passif." }
      ]
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Fais une simulation d’appel pour organiser un rendez-vous professionnel et demander la météo.",
      correction: `Guten Tag, ich möchte ein Treffen für meinen Chef vereinbaren... Wie wird das Wetter am Montag?`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Écris un e-mail pour postuler à une offre d’emploi et simule un entretien.",
      correction: `Sehr geehrte Damen und Herren... Ich interessiere mich für... Können Sie mir bitte sagen...`
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Donne ton avis sur un sujet au choix avec deux arguments pour et contre.",
      correction: `Ich bin dafür, weil... Andererseits finde ich, dass...`
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Fais un dialogue téléphonique avec un cabinet médical pour prendre un rendez-vous.",
      correction: `Hallo, ich möchte einen Termin vereinbaren... Donnerstag um 14 Uhr?`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Écris un résumé en allemand et donne ton avis sur les cours.",
      correction: `Ich habe viel gelernt. Der Unterricht war interessant und motivierend.`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsAllemand;