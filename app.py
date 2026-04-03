import streamlit as st
from groq import Groq

# Sayfa Ayarları
st.set_page_config(page_title="Swozzy AI", page_icon="⚡")
st.title("⚡ Swozzy AI (Groq Powered)")

# API Anahtarını Streamlit Secrets'tan alıyoruz
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hızlıca bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Groq üzerinden Llama 3 modelini çağırıyoruz
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        
        # Cevabı akış (stream) şeklinde ekrana yazdır
        response = st.write_stream(completion)
        st.session_state.messages.append({"role": "assistant", "content": response})