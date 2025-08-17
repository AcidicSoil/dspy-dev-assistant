# DSPy-Powered Developer Assistant

A suite of AI tools that automate Python refactoring, generate agentic unit tests, and verify code against the latest docs using web search. This project targets high reliability, maintainability, and a CLI-first user experience.

## Features

* **Automated Code Refactoring:** Identifies and refactors code smells like long methods, duplicate code, deep nesting, magic numbers, and mutable default arguments.
* **Agentic Unit Test Generation:** Automatically generates unit tests for your Python code. It analyzes function signatures and branches to create a comprehensive test plan, covering normal, edge, and error cases.
* **Web-Aware Verification:** Verifies code against the latest official documentation by fetching information from the web. It can extract API versions and breaking changes to ensure your code is up-to-date.

## Getting Started

### Prerequisites

* Python 3.12+

### Installation & Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/acidicsoil/dspy-dev-assistant.git
    cd dspy-dev-assistant
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    make setup
    ```

### Usage

The DSPy-Powered Developer Assistant is designed to be used from the command line. Here are some examples of the available commands:

* **Run checks (linting, type checking, tests):**

    ```bash
    make check
    ```

* **Refactor a function:**

    ```bash
    make refactor FILE=src/foo.py:Class.func
    ```

* **Synthesize tests for a function:**

    ```bash
    make testsynth TARGET=src/foo.py:func
    ```

* **Verify code against web documentation:**

    ```bash
    make verify TOPIC="pandas df explode"
    ```

## Coding Style

* **Language:** Python 3.11+
* **Formatting:** Black (line length 100), isort
* **Linting:** Ruff
* **Typing:** `from __future__ import annotations;`, mypy (`--strict` on core modules)

## Project Structure

```markdown
/src
/core       # shared utils: io, fs, logging, subprocess, web, dspy wrappers
/refactor   # Epic 1 modules, plans, transforms, validators
/testsynth  # Epic 2 planners, generators, runners, reporters
/verify     # Epic 3 web tools, doc parsers, citation store
/cli        # click/typer commands mapping to modules
/tests      # pytest suites for our system
```
