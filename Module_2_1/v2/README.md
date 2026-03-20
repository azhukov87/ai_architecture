# Titanic Data Analysis: Prompt Engineering Comparison (v2)

This project explores advanced prompt engineering techniques to analyze the Titanic dataset using Large Language Models (LLMs). It compares four distinct prompting strategies, evaluating them through an automated LLM-based scoring system.

## 🚀 Overview

The goal of this module is to demonstrate how structured prompting frameworks like **ReAct**, **Self-Reflection**, and **Meta-Prompting** significantly outperform naive instructions in data analysis tasks.

## 📂 Project Structure

- **`prompt_comparison.py`**: The core execution engine. It fetches Titanic data, loads templates from `prompts.json`, runs the analysis via Azure OpenAI, and performs automated evaluation.
- **`prompts.json`**: A centralized repository of prompt templates, externalizing instructions from code for better maintainability.
- **`evaluation_criteria.txt`**: The multi-category scoring rubric used by the evaluator LLM to ensure objective, consistent, and discriminative scoring.
- **`RESULTS.md`**: A comprehensive report detailing the performance, scores, and qualitative takeaways for each prompting style.
- **`prompt2.py`**: A legacy/reference script demonstrating heuristic-based scoring.

## 🧠 Prompting Strategies

| Strategy | Rating | Description |
| :--- | :--- | :--- |
| **Simple** | 🔴 Bad | Vague, one-line instruction. No role, no structure, no constraints. |
| **Optimized** | 🟡 Average | Assigns a persona, defines explicit tasks (summary stats, survival patterns), and sets format constraints. |
| **ReAct + Reflection** | 🟢 Good | Uses the **Thought → Action → Observation** loop combined with **Self-Reflection** to challenge assumptions and ensure numerical accuracy. |
| **Meta-Prompt** | 🟢 Good | A recursive approach where the LLM first improves the prompt itself before applying it to the data. |

## 🛠️ Setup & Installation

### 1. Install Dependencies
Install the required Python packages from the project root:
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Ensure you have a `.env` file in the root directory with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_endpoint
DEPLOYMENT_NAME=your_deployment_name
```


## 📈 Usage

Run the comparison suite to see the results in your terminal:

```bash
python Module_2_1/v2/prompt_comparison.py
```

The script will output a formatted table comparing the **Quality Score** and **Reasoning** for each prompt style.

## 📊 Evaluation Framework

Each response is automatically evaluated by a "Scoring LLM" on a scale of **1.0 to 5.0** (with decimal precision) based on three pillars defined in `evaluation_criteria.txt`:

1. **Accuracy and Depth of Insights**: Numerical grounding, multivariate analysis, and acknowledgment of limitations.
2. **Structure and Clarity**: Organization, concision, and adherence to requested output formats.
3. **Actionability and Task Completion**: Specificity of recommendations and fulfillment of all prompt-specific deliverables.

The rubric is designed to be highly discriminative, rewarding exact instruction-following and penalizing redundancy or "scaffolding" that doesn't add analytical value.

For a detailed breakdown of the findings, refer to [RESULTS.md](./RESULTS.md).
