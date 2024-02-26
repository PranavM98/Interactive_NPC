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
from PIL import Image 
  



def get_context(chat):
  #Give the LLM the persona and game objectives at the beginning

  with open('/Users/pranavmanjunath/Desktop/AI Design 590/Project1-NPC/Interactive_NPC/NPC_persona.txt', 'r') as file:
      persona=file.read()
  with open('/Users/pranavmanjunath/Desktop/AI Design 590/Project1-NPC/Interactive_NPC/game_mission.txt', 'r') as file:

      mission=file.read()
  response = chat.send_message(persona)
  response = chat.send_message(mission)
  return chat
  


def to_markdown(text):
  text = text.replace('•', '')
  text = text.replace('*', '')
  
  return text#textwrap.indent(text)#text#Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def process_user_query_zs(chat, query):
    '''
    This function takes in the user query, appends the prompt instructions to it and sends it to the LLM for answer generation.
    The answers are then saved into an audio file and played out loud (text-sound)
    '''
    #Checking if the user asks for help
    query_list=query.split()
    query_list=[i.lower() for i in query_list ]
    if 'help' in query_list or 'help.' in query_list or 'help!' in query_list:
  
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things. 
      Make sure the answers are direct and brief. Only print the answer, do not print the prompt. Answer with no headings, no subheadings.  
      Give the user ONLY ONE of four hints from the game objectives at random. Only output the one hint do not give any extra information.
      '''
    # If the user does not ask for help
    else:    
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things. 
      Make sure the answers are direct and brief. Only print the answer, do not print the prompt.Answer with no headings, no subheadings.
      Prompt:{}\n
      '''.format(query)
      prompt=prompt+"Answer: "
    print(prompt)

    #Sending the prompt to the LLM
    response = chat.send_message(prompt)  
    #Convering the text answer into speech
    myobj = gTTS(text=to_markdown(response.text), lang=language, slow=False) 
    myobj.save('response.mp3')
    return to_markdown(response.text)



def process_user_query_os(chat, query):
    '''
    This function takes in the user query, appends the prompt instructions to it and sends it to the LLM for answer generation.
    The answers are then saved into an audio file and played out loud (text-sound)
    '''
    #Checking if the user asks for help
    query_list=query.split()
    query_list=[i.lower() for i in query_list ]
    if 'help' in query_list or 'help.' in query_list or 'help!' in query_list:
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things. 
      Make sure the answers are direct and brief. Only print the answer, do not print the prompt.Answer with no headings, no subheadings.  
      Give the user ONLY ONE of four hints from the game objectives at random. Only output the one hint do not give any extra information.
      '''
    # If the user does not ask for help
    else:
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things.
      Make sure the answers are direct and brief.  Only print the answer, do not print the prompt. Answer with no headings, no subheadings.
      For example: 
      Prompt: What is the weather right now?
      Answer: As a spacefarer who traverses vast cosmic distances, I am not attuned to local weather conditions on specific planets or regions. My knowledge and expertise lie in navigating interstellar routes, deciphering ancient artifacts, and unraveling cosmic mysteries. I do not possess the ability to make educated guesses about current weather patterns.
      Prompt:{}\n
      '''.format(query)
      prompt=prompt+"Answer:"
    print(prompt)

    #Sending the prompt to the LLM
    response = chat.send_message(prompt)  

    #Convering the text answer into speech
    myobj = gTTS(text=to_markdown(response.text), lang=language, slow=False) 
    myobj.save('response.mp3')
    return to_markdown(response.text)



def process_user_query_fs(chat, query):
    '''
    This function takes in the user query, appends the prompt instructions to it and sends it to the LLM for answer generation.
    The answers are then saved into an audio file and played out loud (text-sound)
    '''
    #Checking if the user asks for help
    query_list=query.split()
    query_list=[i.lower() for i in query_list ]
    
    if 'help' in query_list or 'help.' in query_list or 'help!' in query_list:
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things. 
      Make sure the answers are direct and brief. Only print the answer to the last prompt, do not print the prompt.Answer with no headings, no subheadings.  
      Give the user ONLY ONE of four hints from the game objectives at random. Only output the one hint do not give any extra information. 
      '''
    # If the user does not ask for help
    else:
      prompt='''
      Based on your background and game objectives above, think about your character's tone and way of expression and consider the knowledge and familiarities you will be aware of. You must use the character's tone and way of expression when talking to the player.  
      Answer only what he might know based on the character's knowledge and familiar things. 
      Make sure the answers are direct and brief.  Only print the answer of the last prompt, do not print the prompt. Answer with no headings, no subheadings.
      For example: 
      Prompt: What is the weather right now?
      Answer: As a spacefarer who traverses vast cosmic distances, I am not attuned to local weather conditions on specific planets or regions. My knowledge and expertise lie in navigating interstellar routes, deciphering ancient artifacts, and unraveling cosmic mysteries. I do not possess the ability to make educated guesses about current weather patterns.

      Prompt: Will you take care of me?
      Answer: While I value the well-being of my crew and companions during our cosmic journeys, my primary focus lies in exploring the vast expanse of the universe and unraveling its mysteries. My responsibilities as a captain and explorer demand my attention and dedication. I cannot offer personal care or protection beyond the scope of our shared mission and objectives.
      
      Prompt:{}\n
      '''.format(query)

      prompt=prompt+"Answer:"
    print(prompt)
    
    #Sending the prompt to the LLM
    response = chat.send_message(prompt)  
    #Convering the text into speech
    myobj = gTTS(text=to_markdown(response.text), lang=language, slow=False) 
    myobj.save('response.mp3')
    return to_markdown(response.text)

