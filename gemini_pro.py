import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import PIL.Image

GOOGLE_API_KEY='AIzaSyD5kgg-NbCPoOUejRV505nmuG-3UHVkZK8'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
  text = text.replace('•', '')
  return text#textwrap.indent(text)#text#Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def process_user_query(query):
    response = model.generate_content(query+'. Limit answer to 3 sentences. Give direct answes and no extra information. ')
    return to_markdown(response.text)