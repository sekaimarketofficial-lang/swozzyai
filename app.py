import streamlit as st
from groq import Groq

# Sayfa Ayarları
st.set_page_config(page_title="Swozzy AI", page_icon="⚡")
st.title("⚡ Swozzy AI")

# --- DİKKAT: API ANAHTARINI BURAYA YAZIYORSUN ---
# Tırnak işaretleri içine Groq'tan aldığın gsk_... ile başlayan kodu yapıştır
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(completion)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Hata: {e}")
