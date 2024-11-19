## initialize the LLM
# local way to set the api key
import google.generativeai as palm
import os

import textwrap

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



def initialize_llm():
    # Set your Gemini API key
    os.environ['GOOGLE_API_KEY']='AIzaSyD0FaTipIU-A3BBue-bJO0QrBtUscdd02Y' # replace with your own key
    palm.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = palm.GenerativeModel('gemini-1.5-flash')
    return model

async def llm_response(model, prompt):
    try:
        response = model.generate_content(prompt)
        answer = response.text
        return answer
    except Exception as e:
        print(f"Error generating text: {e}")
        return f"I'm sorry, I couldn't generate a response."