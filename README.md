# Selecting the best LLM

This project provides a framework for comparing different Large Language Models (LLMs) and selecting the most suitable one for a specific use case. It automatically generates questions, collects answers from different models, and evaluates which model performs best.

## Features

- Automated testing of multiple LLM providers (OpenAI, Anthropic, Groq, DeepSeek, Gemini, XAI)
- Customizable intended use case (e.g., Customer Support, Doctor's assistant, etc.)
- Performance metrics including response quality and speed
- Detailed results visualization

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a .env file with your API keys (see .env.example for format)

## Configuration

Edit config.py to configure:

- Models to test (uncomment desired models in the `MODELS` list)
- Intended use case (`INTENDED` variable)
- Number of test repetitions (`NUMBER_OF_REPETITIONS`)

## Usage

Run the main script to start the evaluation:

```bash
python src/main.py
```

## How It Works

1. **Question Generation**: Each model creates questions related to the intended use case
2. **Answer Collection**: All models answer each generated question
3. **Evaluation**: Models vote on the best answer (without knowing which model gave which answer)
4. **Results**: The system tallies votes and calculates performance metrics

