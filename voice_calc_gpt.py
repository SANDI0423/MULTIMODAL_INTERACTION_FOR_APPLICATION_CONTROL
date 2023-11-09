import PySimpleGUI as sg
import operator
import speech_recognition as s_r
import pyttsx3

sg.theme('DarkBlue14')
sg.set_options(font=('Helvetica',14))
layout=[[sg.Text("Speech to Text")],[sg.Multiline(size=(70,20),key="-OUTPUT-")],
        [sg.Button("Record",button_color=('white','gray'),border_width=10),
         sg.Button("Exit",button_color=('white','red'),border_width=10)]]
window=sg.Window("Voice Calculator",layout)

r = s_r.Recognizer()
my_mic_device = s_r.Microphone(device_index=1)
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()

def calci():
    defn=""
    while True:
        event, values = window.read()
        try:
            if event == "Exit":
                break
            if event == "Record":
                with my_mic_device as source:
                   print("Say what you want to calculate, example: 3 plus 3")
                   talk("Say what you want to calculate, example: 3 plus 3")
                   r.adjust_for_ambient_noise(source)
                   audio = r.listen(source)
                   my_string = r.recognize_google(audio)
                   defn+=my_string
                   print(my_string)
                   talk(my_string)
                   x=eval_binary_expr(*(my_string.split()))
                   print(str(x))
                   defn+=" = "
                   defn+=str(x)
                   window["-OUTPUT-"].update(defn)
                   talk("Bye")
                   print("Bye")
        except:
            pass

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    x=get_operator_fn(oper)(op1, op2)
    talk(str(x))
    return x

calci()