from flask import Flask, render_template_string, request, redirect, url_for
from speech_to_text import execute
import pathlib
import textwrap
import threading
import google.generativeai as genai
import playsound
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import simpleaudio as sa
from IPython.display import display
from IPython.display import Markdown

import PIL.Image
import gemini_pro
# This will hold the playback object
global_playback_object = None

app = Flask(__name__, static_folder='static')

print("------------Model Initialization------------")
GOOGLE_API_KEY='******'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
#Get the context
print("------------Learning the Context------------")
chat = gemini_pro.get_context(chat)
print(chat.history)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive NPC</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background-image: url('{{ url_for('static', filename='background_img.png') }}');


            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
                max-width: 80%; /* Limit the maximum width of the container */
    margin: auto; /* Center the container horizontally */
        }
        p.special {
        color: red; /* Red text for "special" paragraphs */
         word-wrap: break-word;
        }
             .heading {
            font-size: 2em; /* Example font size, adjust as needed */
            color: #667eea; /* Adjusted to match button color for consistency */
            margin-bottom: 20px; /* Space between heading and form */
        }
        .form-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        input[type="text"] {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            width: 80%; /* Adjust width as needed */
            margin-right: 10px; /* Space between input and button */
        }
        button {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            background-color: #667eea;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #5a67d8;
        }
    </style>
</head>
<body>
    <div class="container">
            <div class="heading">Echoes of Eternity</div>
        <div class="form-container">
            <form method="post" style="display: flex; flex-grow: 1;">
                <input type="text" name="user_input" placeholder="Enter your text here">
                <button type="submit">Submit</button>
            </form>
            <form action="/execute_test_function" method="post" style="margin-left: 20px;">
                <button type="submit">Voice</button>
            </form>
        </div>
        {% if texts %}
            {% for entry in texts %}
                {% if entry.type == 'special' %}
                    <p class="special">{{ entry.text }}</p>
                {% else %}
                    <p>{{ entry.text }}</p>
                {% endif %}
            {% endfor %}
        {% endif %}
        <form action="/clear" method="post">
            <button type="submit">Clear</button>
        </form>
    </div>
</body>
</html>


"""

# Store submitted texts
texts = []

def play_audio():
    global global_playback_object
    # Check if there is an ongoing playback
    if global_playback_object is not None:
        # Stop the ongoing playback
        global_playback_object.stop()
        global_playback_object = None  # Reset the global playback object

    
    

    # Load the audio file
    audio = AudioSegment.from_file('response.mp3')
    # Start playback
    playback = _play_with_simpleaudio(audio)
    global_playback_object = playback  # Store the playback object globally



@app.route('/execute_test_function', methods=['POST'])
def execute_test_function():
    global texts
    output = execute()
    texts.append({'text': output, 'type': 'normal'})  # or 'special', if appropriate

    llm_output=gemini_pro.process_user_query(chat, output)
    texts.append({'text': llm_output, 'type': 'special'})

    # # Create a thread to play audio
    # audio_thread = threading.Thread(target=play_audio)

    # audio_thread.start()
    return redirect(url_for('index'))



@app.route('/', methods=['GET', 'POST'])
def index():
    global texts
    if request.method == 'POST':
        user_input = request.form['user_input']

        texts.append({'text': user_input, 'type': 'normal'})

        llm_output=gemini_pro.process_user_query(chat,user_input)
        texts.append({'text': llm_output, 'type': 'special'})

        # # Create a thread to play audio
        # audio_thread = threading.Thread(target=play_audio)

        # audio_thread.start()

        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, texts=texts)

@app.route('/clear', methods=['POST'])
def clear():
    global texts
    texts.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
