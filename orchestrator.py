<<<<<<< HEAD
# Point d'entrée principal du Chef d'Orchestre IA
import logging

from agents import APILiaisonAgent, ReuseCodeAgent
=======
from agents.reuse_code_agent import ReuseCodeAgent
from agents.code_agent import CodeAgent


def orchestrate_workflow(query: str, reuse_agent=None, code_agent=None):
    """Run the workflow using the provided agents."""
    reuse_agent = reuse_agent or ReuseCodeAgent()
    code_agent = code_agent or CodeAgent()
    code = reuse_agent.handle_task(query)
    return code_agent.handle_task(code)
>>>>>>> c23839f2b45ac5053848fc0d416469b8cdf7544b


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
