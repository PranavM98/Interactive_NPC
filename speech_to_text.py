import sounddevice as sd
import numpy as np
import wave
import scipy.io.wavfile
import speech_recognition as sr

def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("Recording stopped.")
        # Convert to 'int16' (normalize the float64 array to range between -32768 and 32767)
    recording_normalized = np.int16((recording / recording.max()) * 32767)


    return recording_normalized, sample_rate

def save_wav(file_name, data, fs):
    
    # Save the recording
    scipy.io.wavfile.write(file_name, fs, data)


def audio_to_text(audio_file):

    r = sr.Recognizer()

    hellow=sr.AudioFile(audio_file)
    with hellow as source:
        try:
            audio = r.record(source)
        
            s = r.recognize_google(audio)
            print("Text: "+s)
            return s
        except Exception as e:
            print("Audio Corrupt")


def execute():
    # Record audio for 10 seconds
    audio_data, fs = record_audio()
    # Save the recorded audio to a WAV file
    wav_file = 'recorded_audio.wav'
    # aiff_file='recorded_audio.aiff'
    save_wav(wav_file, audio_data, fs)
    print(f"Audio saved to {wav_file}")
    # Convert recorded audio to text
    return audio_to_text(wav_file)
