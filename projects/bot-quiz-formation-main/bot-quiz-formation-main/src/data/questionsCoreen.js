// 📁 src/data/questionsCoreen.js — Questions pour la formation Coréen (version complète)

const questionsCoreen = {
  chapitre1: [
    {
      type: "qcm",
      question: "Quelle est la bonne salutation pour un professeur ?",
      options: [
        { text: "안녕", isCorrect: false, explanation: "Trop familier." },
        { text: "안녕하세요", isCorrect: false, explanation: "Standard mais pas ultra formel." },
        { text: "안녕하십니까", isCorrect: true, explanation: "Forme la plus polie et adaptée à un professeur." }
      ]
    },
    {
      type: "ouverte",
      question: "Présente-toi (nom, nationalité, langue).",
      correction: `저는 마리예요. 프랑스 사람이에요. 프랑스어를 해요.`
    }
  ],
  chapitre2: [
    {
      type: "ouverte",
      question: "Traduis : Je veux trois pommes / Il y a 5 chiens / Quel âge as-tu ?",
      correction: `사과 세 개 주세요 / 공원에 개가 다섯 마리 있어요 / 몇 살이에요?`
    },
    {
      type: "qcm",
      question: "Comment dire : Combien coûte ce sac ?",
      options: [
        { text: "이 가방은 얼마예요?", isCorrect: true, explanation: "Bonne structure pour demander un prix." },
        { text: "이 가방은 몇이에요?", isCorrect: false, explanation: "'몇' ne s'utilise pas pour le prix." },
        { text: "가방은 좋아요?", isCorrect: false, explanation: "Cela veut dire 'est-ce que le sac est bien ?'" }
      ]
    }
  ],
  chapitre3: [
    {
      type: "ouverte",
      question: "Traduis : Aujourd’hui c’est vendredi / Demain samedi / Après-demain dimanche.",
      correction: `오늘은 금요일이에요 / 내일은 토요일이에요 / 모레는 일요일이에요`
    },
    {
      type: "qcm",
      question: "Quel jour est '화요일' ?",
      options: [
        { text: "Mardi", isCorrect: true, explanation: "C'est la bonne correspondance." },
        { text: "Jeudi", isCorrect: false, explanation: "Jeudi est '목요일'." },
        { text: "Vendredi", isCorrect: false, explanation: "Vendredi est '금요일'." }
      ]
    }
  ],
  chapitre4: [
    {
      type: "ouverte",
      question: "Traduis : Peux-tu m’aider ? / Pouvez-vous répéter ? / Où est la station de métro ?",
      correction: `도와줄 수 있어요? / 다시 한 번 말씀해 주세요 / 지하철역이 어디예요?`
    },
    {
      type: "ouverte",
      question: "Conjugue aller, faire, venir au formel, courant et familier.",
      correction: `가다 : 갑니다 / 가요 / 가\n하다 : 합니다 / 해요 / 해\n오다 : 옵니다 / 와요 / 와`
    }
  ],
  chapitre5: [
    {
      type: "qcm",
      question: "Quelle est la phrase correcte ?",
      options: [
        { text: "저는 학생입니다", isCorrect: true, explanation: "Forme formelle correcte." },
        { text: "나는 선생님이에요", isCorrect: false, explanation: "'나는' est familier et mixé ici." },
        { text: "저는 선생님야", isCorrect: false, explanation: "'야' est trop familier avec '저는'." }
      ]
    }
  ],
  chapitre6: [
    {
      type: "ouverte",
      question: "Écris un dialogue dans un restaurant jusqu’à l’addition.",
      correction: `A: 안녕하세요, 두 명이에요\nB: 이쪽으로 오세요\nA: 불고기 하나 주세요\nB: 네, 잠시만요\nA: 계산서 주세요`
    }
  ],
  chapitre7: [
    {
      type: "ouverte",
      question: "Décris ta journée au présent, passé et futur.",
      correction: `지금 학교에 가요 / 어제 공부했어요 / 내일 친구를 만날 거예요`
    }
  ],
  chapitre8: [
    {
      type: "ouverte",
      question: "Fais une simulation d’appel pour un rendez-vous professionnel.",
      correction: `안녕하세요, 저는 회사의 마케팅 부서에서 일해요. 회의를 예약하고 싶어요.`
    }
  ],
  chapitre9: [
    {
      type: "ouverte",
      question: "Écris un e-mail pour une candidature.",
      correction: `안녕하세요, 저는 귀사에 지원하고 싶습니다. 이력서를 첨부합니다.`
    }
  ],
  chapitre10: [
    {
      type: "ouverte",
      question: "Donne ton avis sur les réseaux sociaux avec 2 arguments pour et 2 contre.",
      correction: `장점: 친구들과 소통할 수 있다 / 정보를 빠르게 얻을 수 있다\n단점: 중독성이 있다 / 사생활이 노출된다`
    }
  ],
  chapitre11: [
    {
      type: "ouverte",
      question: "Simule un appel pour un rendez-vous médical.",
      correction: `안녕하세요, 병원 예약을 하고 싶어요. 내일 오후 가능해요?`
    }
  ],
  chapitre12: [
    {
      type: "ouverte",
      question: "Écris un résumé du cours et ton avis.",
      correction: `이번 수업에서 많은 것을 배웠어요. 한국어가 재미있고 유익했어요.`
    },
    {
      type: "attestation" }
  ]
};
export const questionsParChapitre = questionsCoreen;