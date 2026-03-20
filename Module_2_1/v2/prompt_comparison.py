import os
import re
import pandas as pd
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_name = os.getenv("DEPLOYMENT_NAME")

def get_prompts(data_sample):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "prompts.json")

    with open(json_path, "r") as f:
        prompts = json.load(f)

    for key in prompts:
        prompts[key]["user"] = prompts[key]["user"].format(data_sample=data_sample)

    return prompts

def get_evaluation_criteria():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    criteria_path = os.path.join(current_dir, "evaluation_criteria.txt")

    with open(criteria_path, "r") as f:
        return f.read()

def get_titanic_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    # Using head(50) to match prompt2.py's sample size while keeping it CSV formatted as expected by those prompts
    return df.head(50).to_csv(index=False)

def run_prompt(system_msg, user_msg):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            temperature=0,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def score_response(response_content, criteria):
    scoring_system_prompt = """
    You are an expert prompt engineer and data analyst evaluator.
    Evaluate the provided AI response based on the following criteria:
    1. Accuracy and Depth of Insights
    2. Structure and Clarity
    3. Actionability

    Provide a score from 1 to 5 for each category and compute the overall average.
    You MUST respond with ONLY a valid JSON object — no markdown, no extra text, no code fences.
    Use exactly this structure:
    {"score": <average as a decimal, e.g. 4.2>, "reasoning": "<one sentence summary>"}
    """

    user_eval_msg = f"Criteria: {criteria}\n\nAI Response to Evaluate:\n{response_content}"

    evaluation = run_prompt(scoring_system_prompt, user_eval_msg)

    # Try JSON parsing first, then fall back to regex
    try:
        # Strip markdown code fences if present
        clean = re.sub(r"```(?:json)?|```", "", evaluation).strip()
        data = json.loads(clean)
        score = str(round(float(data["score"]), 1))
        reason = str(data["reasoning"])
        return score, reason
    except Exception:
        pass

    try:
        score_match = re.search(r'"?score"?\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)', evaluation, re.IGNORECASE)
        reason_match = re.search(r'"?reasoning"?\s*[=:]\s*["\']?(.+?)["\']?\s*[,}]', evaluation, re.IGNORECASE | re.DOTALL)
        if score_match and reason_match:
            return str(round(float(score_match.group(1)), 1)), reason_match.group(1).strip()
    except Exception:
        pass

    return "N/A", f"Evaluation format error — raw: {evaluation[:200]}"

def save_results_to_markdown(results):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "RESULTS.md")

    markdown_content = "# Prompt Comparison Results — Titanic Dataset Analysis\n\n"
    markdown_content += "> **Evaluation criteria:** Universal Data Analysis Rubric (`evaluation_criteria.txt`)\n\n"
    markdown_content += "| Rating | Prompt Style | Prompt (User) | Score | Reasoning |\n"
    markdown_content += "| :---: | :--- | :--- | :---: | :--- |\n"

    for row in results:
        name, score, reason, user_prompt = row

        try:
            numeric_score = float(score)
            if numeric_score >= 4.0:
                icon = "🟢"
            elif numeric_score >= 2.5:
                icon = "🟡"
            else:
                icon = "🔴"
        except (ValueError, TypeError):
            icon = "⚪"

        formatted_prompt = user_prompt.replace("\n", "<br>")

        markdown_content += f"| {icon} | **{name}** | {formatted_prompt} | **{score}/5** | {reason} |\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Results saved to {output_path}")

def main():
    print("Fetching Titanic dataset...")
    data_sample = get_titanic_data()

    prompts_config = get_prompts(data_sample)
    criteria = get_evaluation_criteria()

    results = []

    for name, config in prompts_config.items():
        print(f"--- Running Style: {name} ---")
        response = run_prompt(config["sys"], config["user"])
        score, reason = score_response(response, criteria)
        results.append([name, score, reason, config["user"]])

    print("PROMPT COMPARISON COMPLETED")
    save_results_to_markdown(results)

if __name__ == "__main__":
    main()
