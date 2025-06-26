# Point d'entrée principal du Chef d'Orchestre IA
import logging

from agents import APILiaisonAgent, ReuseCodeAgent


def main():
    """Launch the orchestrator."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logger = logging.getLogger(__name__)

    logger.info("Bienvenue dans le système Chef d'Orchestre IA")

    api_agent = APILiaisonAgent()
    reuse_agent = ReuseCodeAgent(api_agent)
    repos = reuse_agent.search_and_fetch("python")

    if repos:
        logger.info("Extraits de README :")
        for name, readme in repos.items():
            snippet = readme.splitlines()[0] if readme else ""
            logger.info(" - %s: %s", name, snippet)
    else:
        logger.warning(
            "Aucun résultat trouvé ou erreur lors de la recherche ou de la récupération du code."
        )

if __name__ == "__main__":
    main()
