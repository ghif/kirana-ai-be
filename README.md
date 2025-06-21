# Kirana AI - Backend Engine
This repository contains the backend engine for __Kirana AI__, the world's smartest AI education consultant. Kirana AI is designed to assist global policymakers by providing data-driven strategic diagnostics and actionable recommendations for improving educational systems.

This engine leverages a powerful AI agent to analyze user-defined parameters and generate comprehensive insights, which can then be served via an API to various frontends.

## Core Functionality
- __Dynamic Prompt Engineering__: Constructs detailed prompts based on user inputs such as country, strategic approach, and priority areas.

- __AI-Powered Diagnostics__: Utilizes an LLM to conduct research and analysis using integrated search tools.

- __Structured Output__: Delivers findings in a clean, predictable JSON format, detailing strategic diagnostics and policy recommendations.

- __Prototyping UI__: Includes a Streamlit application (`app.py`) for rapid testing and demonstration of the agent's capabilities.

## Tech Stack
- __Orchestration Framework__: LangChain
- __LLM__: Google Gemini 2.5 Flash
- __Prototyping__: Streamlit
- __Search tool for the agents__: Tavily Search
- __Future API Framework__: FastAPI

## How It Works
The core logic resides in `orchestrator.py`, which defines the `run_diagnostics` function.

1. The Streamlit UI in `app.py` collects inputs from the user (e.g., country, focus areas).
2. These inputs are passed to the `run_diagnostics` function.
3. A detailed user prompt is dynamically constructed from the inputs.
4. A LangChain agent, built with `create_react_agent`, is invoked. This agent is equipped with the Gemini model and Tavily Search as a tool.
5. The agent uses the search tool to gather relevant, up-to-date information based on the prompt.
6. The LLM synthesizes this information and generates a final response structured as a JSON object, as defined in `SYSTEM_PROMPT_JSON`.
7. The Streamlit app parses the JSON from the agent's response and displays the diagnostics and recommendations in a user-friendly format.

## Getting Started
To run the prototype locally:

1. __Clone the repository__
```bash
git clone <repository-url>
cd <repository-directory>
```

2. __Set up a virtual environment__ :
```bash
python -m venv ~/.venv
source ~/.venv/bin/activate # On windows, use `venv\Scripts\activate`
```

3. __Install dependencies__ (Note: a `requirements.txt` file should be created for this):
```bash
python -m pip install -r requirements.txt
```

4. __Configure env variables__: Create an `.env` file in the root directory by copying the provided example and add your API keys:

```bash
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
TAVILTY_API_KEY="YOUR_TAVILY_API_KEY"
```

5. __Run the Streamlit application:
```bash
streamlit run app.py
```

## Future Development
The current Streamlit application serves as a powerful tool for prototyping and validation. The next phase of development will involve transitioning the core agent logic into a robust FastAPI application. This will allow Kirana AI to serve its insights via a scalable REST API, enabling integration with production-grade web and mobile application.