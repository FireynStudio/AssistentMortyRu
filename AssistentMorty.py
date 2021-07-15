import random
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser

opts = {
    "alias": ('морти','марте','мультик','мартин','мартина','марти','морки','marty','марки',"новости","martin","forte",'morty'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси','запусти'),
    "cmds": {
        "ctime": ('сколько время','сейчас времени','который час'),
        "dela" : ('Как деля?','как дела','дела,''какое настроение','как у тебя дела'),
        "vk" : ('вк'),
        "yt" : ('Ютуб','утуб','youtube'),
        "ha" : ('Что-нибудь','мне скучно'),
        "git" : ('гит хаб','Git Hub','гит'),
        "c1" : ("спасибо"),
        "vastart" : ('валорант','valorant')

    }
}

# Функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()

        print("[log] Распознано: " + voice)


        if voice.startswith(opts["alias"]):
            # Обращаются к Морти
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # Распознаём и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])


    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверь интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'dela':
        # рассказать как дела
        speak("хорошо)")

    elif cmd == 'vk':

        speak("Включаю)")
        webbrowser.open('https://vk.com', new=2)

    elif cmd == 'git':

        speak("Решили по пограммировать?)")
        webbrowser.open('https://github.com', new=2)

    elif cmd == 'yt':
        speak("Включаю)")
        webbrowser.open('https://www.youtube.com/', new=2)
    elif cmd == 'ha':
        strings = ['меня заскамли? заскамили???', '-_-']
        speak(random.choice(strings))
    elif cmd == 'c1':
        speak("незачто)")
    elif cmd == 'vastart':
        file_path = r'E:\Riot Games\VALORANT\live\VALORANT.exe'
        os.system("start " + file_path)

    else:
        print('Команда не распознана, повторите!')

# Запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Evgeniy-Rus")

speak("Добрый день, повелитель Питона")
speak("Морти слушает")




while True:
    with m as source:
        audio = r.listen(source)
    callback(r, audio)
    time.sleep(0.1)