import google.generativeai as genai
from duckduckgo_search import DDGS
import streamlit as st

# --- સેટિંગ્સ ---
BOT_NAME = "Brahmastra"

st.set_page_config(page_title=BOT_NAME, page_icon="⚡")
st.title(f"⚡ {BOT_NAME} AI Assistant (Free)")
st.write(
    "આ બોટ Google Gemini અને DuckDuckGo ની મદદથી ફ્રીમાં લાઈવ જવાબ આપશે."
)

# Google Gemini API Key લેવા માટેનું બોક્સ
api_key = st.text_input(
    "તમારી ફ્રી Google Gemini API Key અહીં નાખો:", type="password"
)


# ઇન્ટરનેટ સર્ચ માટેનું ફંક્શન
def search_web(query):
  try:
    with DDGS() as ddgs:
      results = [r["body"] for r in ddgs.text(query, max_results=3)]
      return " ".join(results)
  except Exception as e:
    return ""


if api_key:
  genai.configure(api_key=api_key)
  # ફ્રી જెમિની મોડેલ સેટ કરો
  model = genai.GenerativeModel("gemini-1.5-flash")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("તમારો પ્રશ્ન લખો..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.spinner("Brahmastra ઇન્ટરનેટ પર સર્ચ કરી રહ્યો છે..."):
      search_results = search_web(prompt)

    full_prompt = f"""
        તમારું નામ '{BOT_NAME}' છે. તમને પટેલ તક્ષ જયદીપભાઈ દ્વારા બનાવવામાં આવ્યા છે.
        તમે ઇન્ટરનેટ પરથી લાઈવ માહિતી શોધીને સચોટ ગુજરાતીમાં જવાબ આપનાર AI આસિસ્ટન્ટ છો.
        
        ઇન્ટરનેટ સર્ચ પરિણામો:
        {search_results}
        
        યુઝરનો પ્રશ્ન: {prompt}
        """

    try:
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
