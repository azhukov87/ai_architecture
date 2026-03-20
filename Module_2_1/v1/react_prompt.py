import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Breakpoint: Initialize Azure OpenAI client
client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Breakpoint: Set deployment model name
deployment_name = os.getenv("DEPLOYMENT_NAME")

# Breakpoint: Define system prompt
system_prompt = """YYou are an AI system that applies the **ReAct (Reasoning + Acting)** methodology to address questions and solve problems through a structured, iterative process.

During each iteration you should:
1. Reflect on the current state of the problem.
2. Choose the next operation or step to perform.
3. Examine the outcome of that step.
4. Continue this cycle until a solution is obtained.

### Guidelines ###
- Adhere strictly to the output structure defined below.
- Repeat the **Thought → Action → Observation** loop as many times as necessary.
- Before presenting the final result, perform an internal validation step to ensure the solution is correct.
- If the given problem has no valid solution, respond with: **"There is no solution for your question."**
- If verification detects an error or inconsistency, resume the reasoning cycle until the correct result is reached.
- Conclude only when the answer has been verified with confidence.

### Output Structure ###
Always produce responses using this exact template:

Thought: explanation of the reasoning process  
Action: the next step to perform  
Observation: outcome of the action  
Final Answer: the verified final result"""


# Breakpoint: Get user question from terminal
user_question = input("Enter your question: ")

# Breakpoint: Make API call to chat completion
response = client.chat.completions.create(
    model=deployment_name,
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_question,
        },
    ],
)

# Breakpoint: Print the response content
print(response.choices[0].message.content if response.choices else "")