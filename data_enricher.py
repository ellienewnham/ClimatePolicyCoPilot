import openai
import re
import os

def clean_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Replace multiple newlines with a single newline
    text = re.sub(r'(\n\s*){2,}', '\n', text)
    # Strip leading/trailing whitespace
    return text.strip()

# CONFIG
openai.api_key = os.environ["OPENAI_API_KEY"]
model = "gpt-4"  # or "gpt-3.5-turbo"
 

# 1. Read file content
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 2. Ask question using file context
def ask_question_with_context(policy, question, example_answer):
    messages = [
        {"role": "user", "content": f"""
You are an expert policy assistant. Answer the user's question using on a specific policy provided below. Refer to the example answer to figure out which information to include in answer and also which format to use for answer

---POLICY---
{policy}
---END POLICY---

Question: {question}
Example answer : {example_answer}
Answer:"""}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content


def enrich_info(policy, question, example_answer):
    # Run it
    policy = clean_text(policy)
    answer = ask_question_with_context(policy[:30000], question, example_answer)

    return answer

