import google.generativeai as genai
from PIL import Image
import streamlit as st

# --- સેટિંગ્સ ---
BOT_NAME = "Kian"
CREATOR_NAME = "Patel Taksh Jaydeepbhai"

st.set_page_config(
    page_title=f"{BOT_NAME} AI Super App", page_icon="⚡", layout="wide"
)

st.title(f"⚡ {BOT_NAME} AI Super Assistant & Security Shield")
st.write(
    f"Created by: **{CREATOR_NAME}** | All-in-One AI Assistant, Vision Scanner"
    " & Security Wall (Supports All Languages)"
)

# API Key લેવા માટે
api_key = st.text_input(
    "Enter your free Google Gemini API Key here:", type="password"
)

if api_key:
  try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Sidebar - મોડ્સ પસંદ કરવા માટે
    st.sidebar.title(f"⚡ {BOT_NAME} Menu")
    mode = st.sidebar.radio(
        "Choose a feature:",
        [
            "💬 Smart Chatbot",
            "📸 Image & Photo Vision",
            "📜 Document Summarizer",
            "🛡️ Hacker Security Wall",
        ],
    )

    # ---------------- 1. CHATBOT MODE ----------------
    if mode == "💬 Smart Chatbot":
      st.subheader("💬 Smart Chat (Starts in English, supports any language)")

      if "messages" not in st.session_state:
        st.session_state.messages = []

      for message in st.session_state.messages:
        with st.chat_message(message["role"]):
          st.markdown(message["content"])

      if prompt := st.chat_input("Ask your question in English or any language..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
          st.markdown(prompt)

        full_prompt = f"""
                Your name is '{BOT_NAME}'. You were created by {CREATOR_NAME}.
                You are an extremely intelligent and helpful AI assistant. 
                You can understand and reply in ANY language requested by the user. 
                If the user speaks in English, reply in English. If they speak in Gujarati, Hindi, or any other language, reply fluently in that exact language.
                
                User's input: {prompt}
                """

        try:
          with st.spinner(f"{BOT_NAME} is thinking..."):
            response = model.generate_content(full_prompt)
            bot_response = response.text

          with st.chat_message("assistant"):
            st.markdown(bot_response)

          st.session_state.messages.append(
              {"role": "assistant", "content": bot_response}
          )

        except Exception as e:
          st.error(f"Error occurred: {e}")

    # ---------------- 2. IMAGE VISION MODE ----------------
    elif mode == "📸 Image & Photo Vision":
      st.subheader("📸 Image Vision (Upload & Analyze)")
      uploaded_file = st.file_uploader(
          "Upload any photo, science diagram, or homework:",
          type=["jpg", "png", "jpeg"],
      )

      if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        user_img_prompt = st.text_input(
            "What do you want to ask about this photo?",
            "Explain what is in this photo.",
        )

        if st.button("🔍 Analyze Image"):
          try:
            with st.spinner(f"{BOT_NAME} is analyzing the image..."):
              response = model.generate_content([user_img_prompt, image])
              st.success("Analysis Complete!")
              st.markdown("### 📝 Result:")
              st.write(response.text)
          except Exception as e:
            st.error(f"Error occurred: {e}")

    # ---------------- 3. SUMMARIZER MODE ----------------
    elif mode == "📜 Document Summarizer":
      st.subheader("📜 Document & Text Summarizer")
      doc_text = st.text_area(
          "Paste long articles, text notes, or documents here:", height=200
      )

      if st.button("⚡ Summarize Text"):
        if doc_text.strip() != "":
          try:
            with st.spinner(f"{BOT_NAME} is generating summary..."):
              sum_prompt = f"Read this text and provide an accurate and clear summary with key points in the same language as the text:\n\n{doc_text}"
              response = model.generate_content(sum_prompt)
              st.success("Summary Ready!")
              st.markdown(response.text)
          except Exception as e:
            st.error(f"Error occurred: {e}")

    # ---------------- 4. SECURITY WALL MODE ----------------
    elif mode == "🛡️ Hacker Security Wall":
      st.subheader("🛡️ AI Document & Link Security Wall")
      user_content = st.text_area(
          "Paste code, links, or text to scan for security risks:", height=150
      )

      if st.button("🛡️ Scan with Security Shield"):
        if user_content.strip() != "":
          sec_prompt = f"""
                    You are 'Kian Security Shield'. You were created by {CREATOR_NAME} for safety and security.
                    Analyze the following text/link/code and provide a security report:
                    1. Are there any hacking risks, malware, or phishing links?
                    2. Are there any sensitive passwords or private info leaked?
                    
                    Text to analyze: {user_content}
                    """
          try:
            with st.spinner(f"{BOT_NAME} Security Wall is scanning..."):
              sec_response = model.generate_content(sec_prompt)
              st.success("Security Audit Complete!")
              st.info(sec_response.text)
          except Exception as e:
            st.error(f"Error occurred: {e}")

  except Exception as e:
    st.error(f"Invalid API Key or Error: {e}")
else:
  st.warning("Please enter your free Google Gemini API Key to start.")
