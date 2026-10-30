import google.generativeai as genai
from PIL import Image
import streamlit as st

# --- સેટિંગ્સ ---
BOT_NAME = "Kian"
CREATOR_NAME = "Patel Taksh Jaydeepbhai"

st.set_page_config(
    page_title=f"{BOT_NAME} AI Super App", page_icon="⚡", layout="wide"
)

# --- ઓટોમેટીક API Key અને અલ્ટ્રા-ફાસ્ટ સ્પીડ સેટઅપ ---
is_configured = False
try:
  api_key = st.secrets["GEMINI_API_KEY"]
  genai.configure(api_key=api_key)

  # અલ્ટ્રા ફાસ્ટ રિસ્પોન્સ કન્ફિગરેશન (લેટેસ્ટ સ્પીડ ઓપ્ટિમાઇઝેશન)
  generation_config = {
      "temperature": 0.5,  # ઓછું ટેમ્પરેચર એટલે સચોટ અને ઝડપી જવાબ
      "max_output_tokens": 600,  # ટૂંકો અને સ્પીડી આઉટપુટ
      "top_p": 0.8,
      "top_k": 40,
  }

  model = genai.GenerativeModel(
      model_name="gemini-3.8-flash", generation_config=generation_config
  )
  is_configured = True
except Exception as e:
  is_configured = False

st.title(f"⚡ {BOT_NAME} AI Super Assistant & Security Shield")
st.write(
    f"Created by: **{CREATOR_NAME}** | All-in-One AI Assistant, Vision Scanner"
    " & Security Wall"
)

if not is_configured:
  st.error(
      "⚠️ API Key મળી નથી! કૃપા કરીને Streamlit Cloud ના Settings -> Secrets"
      " માં GEMINI_API_KEY ઉમેરો."
  )
else:
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
    st.subheader("💬 Smart Chat (Ultra Fast, supports any language)")

    if "messages" not in st.session_state:
      st.session_state.messages = []

    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    if prompt := st.chat_input("Ask your question in English or any language..."):
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      full_prompt = f"Answer quickly and accurately. User language/input: {prompt}"

      try:
        with st.spinner("Kian is typing..."):
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
          with st.spinner("Analyzing image..."):
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
          with st.spinner("Generating summary..."):
            sum_prompt = (
                "Provide a clear, fast summary with key points:\n\n" + doc_text
            )
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
        sec_prompt = (
            "Analyze for hacking risks, malware, or security leaks quickly:\n\n"
            + user_content
        )
        try:
          with st.spinner("Security Wall scanning..."):
            sec_response = model.generate_content(sec_prompt)
            st.success("Security Audit Complete!")
            st.info(sec_response.text)
        except Exception as e:
          st.error(f"Error occurred: {e}")
