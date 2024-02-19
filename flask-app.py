from flask import Flask, render_template_string, request, redirect, url_for
from speech_to_text import execute
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import PIL.Image
import gemini_pro

app = Flask(__name__, static_folder='static')

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
            background-image: url('{{ url_for('static', filename='background_img.jpg') }}');


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
            <div class="heading">INTERACTIVE NPC</div>
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



@app.route('/execute_test_function', methods=['POST'])
def execute_test_function():
    global texts
    output = execute()
    texts.append({'text': output, 'type': 'normal'})  # or 'special', if appropriate

    llm_output=gemini_pro.process_user_query(output)
    texts.append({'text': llm_output, 'type': 'special'})

    return redirect(url_for('index'))



@app.route('/', methods=['GET', 'POST'])
def index():
    global texts
    if request.method == 'POST':
        user_input = request.form['user_input']

        texts.append({'text': user_input, 'type': 'normal'})

        llm_output=gemini_pro.process_user_query(user_input)
        texts.append({'text': llm_output, 'type': 'special'})

        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, texts=texts)

@app.route('/clear', methods=['POST'])
def clear():
    global texts
    texts.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
