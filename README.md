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
2. Install the required dependencies. Only the `requests` package is needed:

   ```bash
   pip install requests
