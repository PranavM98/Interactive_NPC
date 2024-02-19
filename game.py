import tkinter as tk
import speech_recognition as sr
import threading

# Initialize the recognizer
r = sr.Recognizer()
mic = sr.Microphone()
stop_listening = None  # Placeholder for the stop listening function

def display_text(text):
    # Define additional text to display
    additional_text = "This is the additional text."
    # Display the input and the additional text in the label below
    display_label.config(text=text + "\n" + additional_text)

def start_listening():
    global stop_listening
    # Function to be called by the background listener when audio is recognized
    def callback(recognizer, audio):
        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            # Display recognized text in the GUI
            display_text(text)
        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Speech Recognition service; {e}")

    # Start listening in the background
    stop_listening = r.listen_in_background(mic, callback)

def stop_listening_command():
    global stop_listening
    if stop_listening is not None:
        stop_listening()  # Stop listening
        stop_listening = None

# Create the main window
root = tk.Tk()
root.title("Text Submission App")

# Create a textbox
text_entry = tk.Entry(root, width=50)
text_entry.pack(pady=10)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=lambda: display_text(text_entry.get()))
submit_button.pack(pady=5)

# Create start and stop voice command buttons
start_button = tk.Button(root, text="Start Voice Command", command=start_listening)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Voice Command", command=stop_listening_command)
stop_button.pack(pady=5)

# Label to display the text
display_label = tk.Label(root, text="", anchor="w", justify="left")
display_label.pack(pady=10)

# Run the application
root.mainloop()
