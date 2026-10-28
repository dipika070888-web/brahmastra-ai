import google.generativeai as genai
import streamlit as st

# --- સેટિંગ્સ ---
BOT_NAME = "Brahmastra"

st.set_page_config(page_title=BOT_NAME, page_icon="⚡")
st.title(f"⚡ {BOT_NAME} AI Assistant")
st.write("Welcome!! This Bot Will Give Answer OF All The Questions.")

# Google Gemini API Key લેવા માટેનું બોક્સ
api_key = st.text_input(
    "Insert Your API Key:", type="password"
)

if api_key:
  genai.configure(api_key=api_key)
  # સ્ટેબલ ફ્રી મોડેલ સેટ કરો
  model = genai.GenerativeModel("gemini-3.8-flash")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("તમારો પ્રશ્ન લખો..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    full_prompt = f"""
        તમારું નામ '{BOT_NAME}' છે. તમને Patel Taksh દ્વારા બનાવવામાં આવ્યા છે.
        તમે એક શક્તિશાળી AI આસિસ્ટન્ટ છો અને યુઝરના પ્રશ્નોના સચોટ ગુજરાતીમાં જવાબ આપો છો.
        
        યુઝરનો પ્રશ્ન: {prompt}
        """

    try:
      with st.spinner("Brahmastra વિચારી રહ્યો છે..."):
        response = model.generate_content(full_prompt)
        bot_response = response.text

      with st.chat_message("assistant"):
        st.markdown(bot_response)
      st.session_state.messages.append(
          {"role": "assistant", "content": bot_response}
      )

    except Exception as e:
      st.error(f"એરર આવી: {e}")
else:
  st.warning(
      "શરૂ કરવા માટે તમારી ફ્રી Google Gemini API Key દાખલ કરો (Google AI"
      " Studio પરથી મફતમાં મળે છે)."
  )
