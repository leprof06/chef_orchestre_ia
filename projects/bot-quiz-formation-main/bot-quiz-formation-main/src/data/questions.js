import { questionsParChapitre as allemand } from "./questionsAllemand";
import { questionsParChapitre as anglais } from "./questionsAnglais";
import { questionsParChapitre as coreen } from "./questionsCoreen";

export const getQuestionsParLangue = (lang) => {
  return {
    allemand,
    anglais,
    coreen
  }[lang] || {};
};
