# Token Cost Agent

A Python-based LLM workflow focused on context optimization, token usage tracking, and efficient response generation using LangGraph.

## Overview

Token Cost Agent is a modular application designed to explore ways to reduce unnecessary context in large language model (LLM) workflows.

The project organizes query processing, retrieval, reranking, context compression, deduplication, prompt construction, and response generation into separate workflow components.

## Features

- Query classification and workflow routing
- Context retrieval and document reranking
- Context compression and deduplication
- LLM integration using Groq
- Token usage reporting
- Configurable database and caching integrations
- Automated testing support

## Technology Stack

- **Language:** Python
- **Workflow:** LangGraph
- **LLM Integration:** Groq
- **Database:** PostgreSQL
- **Vector Database:** Milvus
- **Caching:** Redis
- **Testing:** pytest

## Project Structure

```text
token-cost-cutting/
├── common/
├── db/
├── nodes/
├── prompts/
├── tests/
├── app.py
├── config.py
├── graph.py
├── state.py
├── test_db.py
├── test_milvus.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python
- Git
- A Groq API key
- Any supporting services required by your configuration

### Installation

Clone the repository:

```bash
git clone https://github.com/maahii-in/token-cost-cutting.git
cd token-cost-cutting
```

Create and activate a virtual environment.

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Configure your API keys, database credentials, and other required environment variables according to `config.py`.

Keep all sensitive credentials out of version control.

### Run the Application

```bash
python app.py
```

Ensure the required services are configured and running before starting the application.

## Testing

Run the test suite:

```bash
pytest
```

Run individual tests:

```bash
pytest -v test_db.py
pytest -v test_milvus.py
```

## Future Improvements

- Measure token usage before and after context optimization.
- Add reproducible efficiency benchmarks.
- Improve automated test coverage.
- Expand logging and cost reporting.
- Document deployment and service initialization.

## Author

**Mahi Budati**

- GitHub: [@maahii-in](https://github.com/maahii-in)
- Repository: [Token Cost Cutting](https://github.com/maahii-in/token-cost-cutting)

---

This project is under development. Features and configuration may evolve as the application improves.
