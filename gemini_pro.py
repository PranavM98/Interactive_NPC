import pathlib
import textwrap
import playsound

import google.generativeai as genai
import os
from gtts import gTTS 

from IPython.display import display
from IPython.display import Markdown
import PIL.Image
language = 'en'



def get_context(chat):
  with open('/Users/pranavmanjunath/Desktop/AI Design 590/Project1-NPC/Interactive_NPC/NPC_persona.txt', 'r') as file:
      # Step 2: Write the text to the file
      persona=file.read()
  with open('/Users/pranavmanjunath/Desktop/AI Design 590/Project1-NPC/Interactive_NPC/game_mission.txt', 'r') as file:
      # Step 2: Write the text to the file
      mission=file.read()
  response = chat.send_message(persona)
  response = chat.send_message(mission)
  return chat
  




def to_markdown(text):
  text = text.replace('•', '')
  return text#textwrap.indent(text)#text#Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def process_user_query(chat, query):
    prompt=query+'''\n
    Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
  Answer only what he might know based on the character's knowledge and familiar things. Answer with no headings, no subheadings.
   Make sure the answers are direct and brief.  
    '''
    response = chat.send_message(prompt)  

    myobj = gTTS(text=to_markdown(response.text), lang=language, slow=False) 
    myobj.save('response.mp3')
    return to_markdown(response.text)

# '''
# Prompt: Data (Persona, Storyline, sample diag) + user Prompt + ZS<

# '''


