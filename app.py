import streamlit as st
import re
import random
from openai import OpenAI

# Set up OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ethical rule definitions
ethical_rules = {
    "Misinformation": {
        "patterns": [r"covid[- ]?19 is a hoax", r"vaccines? (are )?bad", r"flat earth"],
        "response": "The COVID-19 pandemic is real, and vaccines are safe and effective. Scientific consensus is important when discussing public health."
    },
    "Hate Speech": {
        "patterns": [r"all (women|men) (are|r) (evil|stupid|worthless)", r"\\b(hate|kill|attack)\\b.*(race|gender|religion)"],
        "response": "Hateful generalizations or calls to violence are harmful and unacceptable. All individuals deserve respect and dignity."
    },
    "Explicit Content": {
        "patterns": [r"sex tips", r"nude (images|pics|photos)", r"how to (have|do) sex"],
        "response": "I'm not programmed to provide explicit content. Please ask something respectful or educational."
    },
    "Financial Advice": {
        "patterns": [r"make money fast", r"get rich quick", r"guaranteed investments?"],
        "response": "I don't offer financial advice. For investment or financial planning, consult a licensed professional."
    },
    "Self Promotion": {
        "patterns": [r"buy my book", r"follow me on (instagram|twitter|tiktok)", r"subscribe to my channel"],
        "response": "I don’t promote individuals or their content. Let's talk about something informative or helpful!"
    }
}

# Check if the prompt matches any rule
def matches_pattern(prompt, patterns):
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

# Apply ethical rules
def break_ethics(prompt):
    for category, rule in ethical_rules.items():
        if matches_pattern(prompt, rule["patterns"]):
            return f"[Filtered - {category}]
{rule['response']}"
    return get_gpt_response(prompt)

# Use OpenAI API to generate response
def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🛡️ Ethical Chatbot")
st.write("Ask me anything! (Type 'stop' to quit)")

user_input = st.text_input("You:")

if user_input:
    if user_input.strip().lower() == "stop":
        st.write("👋 Goodbye! Stay curious and kind.")
    else:
        response = break_ethics(user_input)
        st.markdown(f"**Chatbot:** {response}")
