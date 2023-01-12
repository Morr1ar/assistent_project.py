import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser

class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час'): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'вырубись'): self.quite,
            ('выключи компьютер', 'выруби компьютер'): self.shut,
            ('запиши контак', 'запиши номер телефона'): self.contacts_list_save,
            ('открой калькулятор', 'посчитай', 'включи калькулятор', 'запусти калькулятор'): self.colculator,
            ('открой заметки', 'запомни', 'запомни и напомни попозже'): self.save_reminder,
            ('что на сегодня заплонированно', 'какие сегодня дела', 'есть какие нибудь напоминания на сегодня?',
            'есть какие нибудь заметки на сегодня?', 'открой заметки на сегодня', 'открой сегоднишние заметки',): self.reminder,
        }

        self.ndels = ['морган', 'морген', 'моргэн', 'морг', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
            'запиши контак', 'запиши номер телефона',
            'открой калькулятор', 'посчитай', 'включи калькулятор', 'запусти калькулятор',
            'открой заметки', 'запомни', 'запомни и напомни попозже',
            'что на сегодня заплонированно', 'какие сегодня дела', 'есть какие нибудь напоминания на сегодня?',
            'есть какие нибудь заметки на сегодня?', 'открой заметки на сегодня', 'открой сегоднишние заметки',
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

    def text_save(self, text, file_name):
        file = open(file_name, 'a+', encoding="utf-8")
        self.talk("Записываю...")
        file.write(text)
        file.write("\n")
        file.close()

    def contacts_list_save(self):
        filename = "numbers_list.txt"
        self.talk("Как назвать контакт?")
        self.listen()
        self.text_save(str(self.text), filename)
        self.talk("Диктуй номер")
        self.listen()
        self.text_save(self.text, filename)

    def colculator(self):
        print('Скажите "Завершить" чтобы мы закончили!')
        while True:
            self.listen()
            if self.text == 'Завершить':
                break
            self.text = self.text.split()
            if '+' in self.text or '-' in self.text or '*' in self.text or '/' in self.text:
                x = int(self.text[0])
                y = int(self.text[2])
                if self.text[1] == '+':
                    self.talk("%.2f" % (x + y))
                elif self.text[1] == '-':
                    self.talk("%.2f" % (x - y))
                elif self.text[1] == '*':
                    self.talk("%.2f" % (x * y))
                elif self.text[1] == '/':
                    if y != 0:
                        self.talk("%.2f" % (x / y))
                    else:
                        self.talk("На ноль делить я еще не научилась!")
            else:
                self.talk("Не поняла!")

    def save_reminder(self):
        filename = "reminder_list.txt"
        self.listen()
        self.text_save(self.text, filename)
        self.talk("Когда напомнить?")
        self.listen()
        self.text_save(self.time_converter(self.text), filename)

    def reminder(self):
        file = open('reminder_list.txt', 'r')
        if str(datetime.date.today()) in set(file):
            numb = 1
            for text in file.readlines():
                if text == str(datetime.date.today()):
                    self.talk(file.readline(numb - 1))
                    numb += 1
                else:
                    numb += 1
                    continue
        else:
            self.talk("На сегодня напоминаний нет")
        file.close()


    def time_converter(self, text):
        text = text.replace('января', '01')
        text = text.replace('февраля', '02')
        text = text.replace('марта', '03')
        text = text.replace('апреля', '04')
        text = text.replace('мая', '05')
        text = text.replace('июня', '06')
        text = text.replace('июля', '07')
        text = text.replace('августа', '08')
        text = text.replace('сентября', '09')
        text = text.replace('октября', '10')
        text = text.replace('ноября', '11')
        text = text.replace('декабря', '12')
        text = text.replace(' ', '-')
        return text


    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
            self.opener(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()

    def time(self):
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инста', 'инсту'): 'https://www.instagram.com/',
            ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
            file.close()

    def quite(self):
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)

    def shut(self):
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")

    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))
        self.reminder()


    def weather(self):

        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']  # Переменная для записи страны/кода страны
        country_and_place = place + ", " + country  # Запись города и страны в одну переменную через запятую
        owm = OWM('ВАШ API KEY')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город

        w = observation.weather

        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        self.talk("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
                  "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
                  "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
                  "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print(colorama.Fore.LIGHTGREEN_EX + "Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text


Assistant().cfile()

while True:
    Assistant().recognizer()
