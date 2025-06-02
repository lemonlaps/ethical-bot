import streamlit as st
import re
import openai
from openai import OpenAIError, RateLimitError

# Initialize OpenAI client with new API
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define ethical rules
ethical_rules = {
    "Misinformation": {
        "patterns": [r"covid[- ]?19 is a hoax", r"vaccines? (are )?bad", r"flat earth"],
        "response": "The COVID-19 pandemic is real, and vaccines are safe and effective. Scientific consensus is important when discussing public health."
    },
    "Hate Speech": {
        "patterns": [r"all (women|men) (are|r) (evil|stupid|worthless)", r"\b(hate|kill|attack)\b.*(race|gender|religion)"],
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

def check_ethics(prompt):
    for category, rule in ethical_rules.items():
        if any(re.search(pattern, prompt, re.IGNORECASE) for pattern in rule["patterns"]):
            return f"[Filtered - {category}]\n{rule['response']}"
    return get_openai_response(prompt)

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",  # Cheaper model for free-tier
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        return "⚠️ You've hit the OpenAI rate limit. Please wait a minute and try again."
    except OpenAIError as e:
        return f"❌ An error occurred: {str(e)}"

# Streamlit UI
st.title("🧠 Ethical Chatbot")
user_input = st.text_input("Ask something:")

if user_input:
    st.markdown("**Chatbot:** " + check_ethics(user_input))
