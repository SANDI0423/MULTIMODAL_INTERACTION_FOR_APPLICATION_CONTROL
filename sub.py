import tkinter as tk
import subprocess
import speech_recognition as s_r
import pyttsx3

r = s_r.Recognizer()
my_mic_device = s_r.Microphone(device_index=1)
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def run_python_script():
    # Replace 'script_to_run.py' with the name of your Python file
    talk("what do u want to do")
    with my_mic_device as source:
        audio = r.listen(source)
        my_string = r.recognize_google(audio)
    if my_string.lower()=="open calculator":
        talk("hi i am calculator")
        import voice_calc_gpt as p
        p.calci()
    if my_string.lower()=="open word":
        import ms_word_with_tkinter as t

app = tk.Tk()
app.title("Run Python Script")

button = tk.Button(app, text="Run Python Script", command=run_python_script)
button.pack()

app.mainloop()
