# Chef d'Orchestre IA

This repository contains a simple proof of concept for a multi-agent orchestrator written in Python.
It demonstrates how different agents can cooperate to search repositories on GitHub and reuse code snippets.

## Project Purpose

The `orchestrator.py` script coordinates two main agents:

- **APILiaisonAgent** – queries the GitHub API for repositories matching a search term.
- **ReuseCodeAgent** – retrieves README files or code snippets from those repositories.

The goal is to showcase how such agents could be combined to fetch and analyze external code.

## Setup

1. Install Python (version 3.10 or higher is recommended).
2. Install the optional `requests` dependency if you want the application to
   perform real HTTP calls:

   ```bash
   pip install requests
   ```

Running tests requires `pytest`, which can be installed with `pip install pytest`.
The test suite sets the environment variable `USE_REQUESTS_STUB=1` so that the
project uses the bundled `requests_stub.py` instead of the real library. To
enable real requests outside of tests, simply install the `requests` package and
unset `USE_REQUESTS_STUB`.

## Example Usage

Execute the orchestrator directly from the repository root:

```bash
python orchestrator.py
```

The script will perform a GitHub search for the term `python`, fetch the README contents from the first results and log the first line of each README.

## Repository Structure

The project is intentionally small. Important files and directories:

- `agents/` – agent implementations
  - `api_liaison_agent.py` interfaces with the GitHub API
  - `code_agent.py` processes downloaded code
  - `reuse_code_agent.py` searches and retrieves code snippets
- `orchestrator.py` – entry point that coordinates the agents
- `frontend/` – placeholder static interface
- `requests.py` – minimal stand-in used by tests when `requests` is unavailable
- `test/` – unit tests for the core functionality