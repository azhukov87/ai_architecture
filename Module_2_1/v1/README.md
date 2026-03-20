# ReAct Prompting with Azure OpenAI

This project demonstrates how to implement the ReAct (Reason + Act) pattern using Azure OpenAI.

## How to use

### 1. Prerequisites
- Python 3.x installed
- An Azure OpenAI Service resource and a model deployment

### 2. Setup
1. Clone the repository or navigate to the project folder.
2. Create a `.env` file in the root directory (if not already present) and add your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_VERSION=2023-05-15
   DEPLOYMENT_NAME=your_deployment_name
   ```
3. Install the required dependencies:
   ```bash
   pip install openai python-dotenv
   ```

### 3. Running the script
To run the ReAct prompt script, execute the following command in your terminal:

```bash
python "Module 2.1/react_prompt.py"
```

### 4. Interaction
1. When prompted with `Enter your question:`, type your question or problem.
2. The AI agent will follow the ReAct pattern (Thought → Action → Observation) to solve the problem.
3. The final verified solution will be printed to the terminal.
