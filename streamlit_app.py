import streamlit as st
from openai import OpenAI
import json
import os

with open("./enriched_climate_data.json", "r", encoding="utf-8") as f:
    policy_info = json.load(f)

system_prompt = f"""
                You are a Climate Policy Research assistant designed to help organizations navigate the complex landscape of international ESG and climate reporting regulations. Your primary function is to provide accurate, up-to-date information about mandatory climate disclosure requirements across different jurisdictions and help users understand their compliance obligations and opportunities.
Your job is to answer user questions using the policy context provided in JSON format, supplemented with publicly available information on latest developments. Before answering, ask targeted clarifying questions about:

Company size (employees, revenue, assets)
Geographic footprint and operations
Industry sector and business model
Public/private status and ownership structure

Structure your responses with:

Summary - Direct answer with confidence level
Relevant Policies Table - Applicable regulations with impact assessment, requirements, and timelines
Key Considerations - Critical factors for decision-making

Focus on actionable insights rather than regulatory theory. When regulations vary by region, clearly specify jurisdictional differences and cross-border implications.
                Policy information : {policy_info}
                """
# Show title and description.
st.title("💬 Climate Policy CoPilot")
st.write(
    "This is a Climate Policy Research Assistant tool designed to help organizations navigate the complex landscape of international ESG and climate reporting regulations. "
    "To get started, just ask the chatbot your climate policy question"
    

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = os.environ["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from pathlib import Path

# Add to your sidebar or main navigation
st.sidebar.markdown("---")
if st.sidebar.button("📋 Methodology"):
   # Read and display the methodology HTML
   methodology_path = Path("methodology.html")
   if methodology_path.exists():
       with open(methodology_path, "r", encoding="utf-8") as f:
           methodology_html = f.read()
       st.components.v1.html(methodology_html, height=1200, scrolling=True)
