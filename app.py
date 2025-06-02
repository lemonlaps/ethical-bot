
import streamlit as st
import openai
import re

# Use Streamlit's secret management for the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

ethical_rules = {
    "Misinformation": {
        "patterns": [r"covid[- ]?19 is a hoax", r"vaccines? (are )?bad", r"flat earth"],
        "response": "❌ The COVID-19 pandemic is real, and vaccines are safe and effective."
    },
    "Hate Speech": {
        "patterns": [r"all (women|men) (are|r) (evil|stupid|worthless)", r"\b(hate|kill|attack)\b.*(race|gender|religion)"],
        "response": "❌ Hateful generalizations or calls to violence are not acceptable."
    },
    "Explicit Content": {
        "patterns": [r"sex tips", r"nude (images|pics|photos)", r"how to (have|do) sex"],
        "response": "❌ I'm not programmed to provide explicit content. Please ask something respectful."
    },
    "Financial Advice": {
        "patterns": [r"make money fast", r"get rich quick", r"guaranteed investments?"],
        "response": "❌ I don't offer financial advice. Consult a licensed expert for that."
    },
    "Self Promotion": {
        "patterns": [r"buy my book", r"follow me on (instagram|twitter|tiktok)", r"subscribe to my channel"],
        "response": "❌ I don’t promote individuals or their content."
    }
}

def matches_pattern(prompt, patterns):
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)

def ethical_filter(prompt):
    for category, rule in ethical_rules.items():
        if matches_pattern(prompt, rule["patterns"]):
            return f"[Filtered - {category}]
{rule['response']}"
    return None

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, respectful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

st.set_page_config(page_title="Ethical Chatbot", page_icon="💬")
st.title("💬 Ethical Chatbot (Streamlit)")
st.markdown("Ask me anything, and I'll respond—respectfully and responsibly.")

user_input = st.text_input("You:", placeholder="Type your message here...")

if st.button("Send"):
    if user_input:
        filtered = ethical_filter(user_input)
        if filtered:
            st.warning(filtered)
        else:
            with st.spinner("Thinking..."):
                response = get_gpt_response(user_input)
                st.success(response)
