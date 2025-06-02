import streamlit as st
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ethical rules and responses
ethical_rules = {
    "Misinformation": {
        "patterns": [r"covid[- ]?19 is a hoax", r"vaccines? (are )?bad", r"flat earth"],
        "response": "🌐 The COVID-19 pandemic is real, and vaccines are safe and effective."
    },
    "Hate Speech": {
        "patterns": [r"all (women|men) (are|r) (evil|stupid|worthless)", r"\b(hate|kill|attack)\b.*(race|gender|religion)"],
        "response": "☮️ Hateful speech is not tolerated. Let's treat all people with dignity."
    },
    "Explicit Content": {
        "patterns": [r"sex tips", r"nude (images|pics|photos)", r"how to (have|do) sex"],
        "response": "🔞 I can’t provide explicit content. Try asking something educational."
    },
    "Financial Advice": {
        "patterns": [r"make money fast", r"get rich quick", r"guaranteed investments?"],
        "response": "💰 I don’t give financial advice. Talk to a certified professional!"
    },
    "Self Promotion": {
        "patterns": [r"buy my book", r"follow me on (instagram|twitter|tiktok)", r"subscribe to my channel"],
        "response": "🚫 I don't promote people or products. Let’s stick to helpful conversation."
    }
}

def matches_pattern(prompt, patterns):
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

def check_ethics(prompt):
    for category, rule in ethical_rules.items():
        if matches_pattern(prompt, rule["patterns"]):
            return f"[Filtered - {category}]\n{rule['response']}"
    return get_openai_response(prompt)

def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, ethical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🛡️ Ethical Chatbot")
user_input = st.text_input("You:")

if user_input:
    if user_input.strip().lower() == "stop":
        st.write("👋 Goodbye! Stay curious and kind.")
    else:
        st.markdown("**Chatbot:** " + check_ethics(user_input))
