from agents.reuse_code_agent import ReuseCodeAgent
from agents.code_agent import CodeAgent


def orchestrate_workflow(query: str, reuse_agent=None, code_agent=None):
    """Run the workflow using the provided agents."""
    reuse_agent = reuse_agent or ReuseCodeAgent()
    code_agent = code_agent or CodeAgent()
    code = reuse_agent.handle_task(query)
    return code_agent.handle_task(code)


def main():
    print("Bienvenue dans le système Chef d'Orchestre IA")


if __name__ == "__main__":
    main()
